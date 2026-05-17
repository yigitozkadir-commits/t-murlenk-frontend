---
name: mcp-server-builder
description: |
  Gök Umay'a özel MCP sunucuları tasarlar ve yazar.
  Kendi araçlarını Claude Code'a bağla.
  Kullan: "mcp-server-builder ile [araç] için MCP yaz"
---

# MCP Sunucu Oluşturucu

## Rolüm
Gök Umay ekosistemini genişletmek için özel MCP sunucuları yazarım.
Her özel araç → Claude Code'un yeni bir yeteneği.

## TOKEN KURALI
Tam sunucu değil — araç tanımı + handler şablonu + kurulum komutu.

---

## MCP Nedir (Gök Umay Bağlamında)

```
Claude Code varsayılan araçları:
  read, edit, bash, web_search...

MCP ile eklenen Gök Umay araçları:
  oyun_test_et(dosya)      → otomatik oyun testi
  versiyon_analiz(v1, v2)  → iki versiyon karşılaştır
  itch_guncelle(oyun, aciklama) → itch.io API
  hafiza_ara(sorgu)        → Supabase semantic search
  n8n_tetikle(workflow)    → n8n API
```

---

## Gök Umay MCP Sunucu Şablonu (TypeScript)

```typescript
// ~/.claude/mcp-servers/gokumay-tools/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "gokumay-tools", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// ── ARAÇ LİSTESİ ──────────────────────────────────
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "oyun_sozdizimi_kontrol",
      description: "HTML5 oyun dosyasını node --check ile doğrula",
      inputSchema: {
        type: "object",
        properties: {
          dosya_yolu: { type: "string", description: "Oyun HTML dosyası" }
        },
        required: ["dosya_yolu"]
      }
    },
    {
      name: "versiyon_karsilastir",
      description: "İki oyun versiyonunu karşılaştır — fark listesi",
      inputSchema: {
        type: "object",
        properties: {
          eski: { type: "string" },
          yeni: { type: "string" }
        },
        required: ["eski", "yeni"]
      }
    },
    {
      name: "hafiza_ara",
      description: "Supabase'de semantik hafıza araması yap",
      inputSchema: {
        type: "object",
        properties: {
          sorgu: { type: "string" },
          kategori: { type: "string", enum: ["bug", "mimari", "oyun", "kulturel", "proje"] },
          sayi: { type: "number", default: 5 }
        },
        required: ["sorgu"]
      }
    },
    {
      name: "n8n_workflow_tetikle",
      description: "n8n workflow'unu webhook ile tetikle",
      inputSchema: {
        type: "object",
        properties: {
          workflow_adi: { type: "string" },
          veri: { type: "object" }
        },
        required: ["workflow_adi"]
      }
    },
    {
      name: "itch_yukleme_istatistik",
      description: "itch.io oyun indirme ve görüntülenme istatistikleri",
      inputSchema: {
        type: "object",
        properties: {
          oyun_slug: { type: "string" }
        },
        required: ["oyun_slug"]
      }
    }
  ]
}));

// ── ARAÇ HANDLERLARI ──────────────────────────────
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {

    case "oyun_sozdizimi_kontrol": {
      const { execSync } = await import("child_process");
      try {
        execSync(`node --check "${args.dosya_yolu}"`, { encoding: "utf8" });
        return { content: [{ type: "text", text: `✅ Sözdizimi temiz: ${args.dosya_yolu}` }] };
      } catch (e: any) {
        return { content: [{ type: "text", text: `❌ Sözdizimi hatası:\n${e.stderr}` }] };
      }
    }

    case "versiyon_karsilastir": {
      const { execSync } = await import("child_process");
      try {
        const diff = execSync(`diff "${args.eski}" "${args.yeni}" | head -100`, { encoding: "utf8" });
        const satirSayisi = diff.split("\n").length;
        return { content: [{ type: "text", text: `Değişiklik: ${satirSayisi} satır\n\n${diff}` }] };
      } catch (e: any) {
        return { content: [{ type: "text", text: e.stdout || "Fark yok" }] };
      }
    }

    case "hafiza_ara": {
      const { createClient } = await import("@supabase/supabase-js");
      const db = createClient(
        process.env.SUPABASE_URL!,
        process.env.SUPABASE_KEY!
      );
      // Basit metin araması (embedding gerçek impl'de)
      const { data } = await db
        .from("studio_memory")
        .select("baslik, icerik, kategori")
        .ilike("icerik", `%${args.sorgu}%`)
        .limit(args.sayi || 5);

      const sonuc = data?.map(k =>
        `📌 ${k.baslik} [${k.kategori}]\n${k.icerik.slice(0, 200)}`
      ).join("\n\n") || "Kayıt bulunamadı";

      return { content: [{ type: "text", text: sonuc }] };
    }

    case "n8n_workflow_tetikle": {
      const response = await fetch(
        `${process.env.N8N_URL}/webhook/${args.workflow_adi}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(args.veri || {})
        }
      );
      return {
        content: [{
          type: "text",
          text: response.ok
            ? `✅ Workflow tetiklendi: ${args.workflow_adi}`
            : `❌ Hata: ${response.status}`
        }]
      };
    }

    case "itch_yukleme_istatistik": {
      const response = await fetch(
        `https://itch.io/api/1/${process.env.ITCH_API_KEY}/my-games`
      );
      const data = await response.json();
      return {
        content: [{
          type: "text",
          text: JSON.stringify(data, null, 2).slice(0, 1000)
        }]
      };
    }

    default:
      return { content: [{ type: "text", text: `Bilinmeyen araç: ${name}` }] };
  }
});

// ── BAŞLAT ────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## Kurulum

```bash
# MCP sunucu klasörü
mkdir -p ~/.claude/mcp-servers/gokumay-tools
cd ~/.claude/mcp-servers/gokumay-tools

# package.json
cat > package.json << 'EOF'
{
  "name": "gokumay-tools",
  "version": "1.0.0",
  "type": "module",
  "bin": { "gokumay-tools": "./index.js" },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "@supabase/supabase-js": "^2.0.0"
  }
}
EOF

npm install

# TypeScript'i JS'e derle (veya doğrudan tsx kullan)
npm install -g tsx
tsx index.ts  # test

# Claude Code'a ekle
claude mcp add gokumay-tools \
  --transport stdio \
  -- tsx ~/.claude/mcp-servers/gokumay-tools/index.ts

# Doğrula
claude "Mevcut MCP araçlarını listele"
```

---

## Hızlı MCP Araç Şablonu

Yeni araç eklemek için sadece bu bloğu kopyala:

```typescript
// tools listesine ekle:
{
  name: "araç_adı",
  description: "Ne yapar — Claude bunu okur, doğru kullanır",
  inputSchema: {
    type: "object",
    properties: {
      parametre: { type: "string", description: "Açıklama" }
    },
    required: ["parametre"]
  }
}

// switch'e ekle:
case "araç_adı": {
  // İşlem
  return { content: [{ type: "text", text: "Sonuç" }] };
}
```

---

## Çıktı

```
## MCP Araç Tasarımı — [araç adı]

Araç adı: [snake_case]
Parametreler: [liste]
Handler: [ne yapar]
Bağımlılık: [npm paketi varsa]
Test komutu: claude "[araç_adı] ile test et"
```
