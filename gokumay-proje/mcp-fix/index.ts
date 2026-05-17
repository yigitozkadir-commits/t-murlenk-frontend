// ~/.claude/mcp-servers/gokumay-tools/index.ts — DÜZELTİLMİŞ
// Değişiklik: hafiza_ara → .ilike() yerine gerçek pgvector semantik arama
// Diğer 6 araç aynı kalıyor — sadece hafiza_ara case'i güncellendi

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { execSync } from "child_process";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { createClient } from "@supabase/supabase-js";

const supabase =
  process.env.SUPABASE_URL && process.env.SUPABASE_KEY
    ? createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY)
    : null;

const server = new Server(
  { name: "gokumay-tools", version: "1.1.0" },
  { capabilities: { tools: {} } }
);

// ── Embedding — Python köprüsü ────────────────────────────────────────────────
// MCP TypeScript içinden Python embedding.py'yi çağırır.
// Ayrı bir HTTP servisi kurmaya gerek yok.
async function getEmbedding(metin: string): Promise<number[]> {
  const HOME = process.env.HOME ?? "";
  const scriptYolu = `${HOME}/.claude/scripts/embedding.py`;

  if (!existsSync(scriptYolu)) {
    throw new Error(`embedding.py bulunamadı: ${scriptYolu}`);
  }

  // Metni geçici dosyaya yaz (shell injection önlemi)
  const gecici = join(tmpdir(), `gokumay_embed_${Date.now()}.txt`);
  writeFileSync(gecici, metin, "utf8");

  try {
    const script = `
import sys, json
sys.path.insert(0, '${HOME}/.claude/scripts')
from embedding import embed
metin = open('${gecici}', encoding='utf-8').read()
print(json.dumps(embed(metin)))
`;
    const cikti = execSync(`python3 -c "${script.replace(/"/g, '\\"')}"`, {
      encoding: "utf8",
      timeout: 15_000,
      env: { ...process.env },
    });
    return JSON.parse(cikti.trim());
  } finally {
    try { execSync(`rm -f ${gecici}`); } catch {}
  }
}

// ── Araç Listesi ──────────────────────────────────────────────────────────────
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "oyun_sozdizimi_kontrol",
      description: "HTML5 oyun dosyasındaki JS bloklarını node --check ile doğrula.",
      inputSchema: {
        type: "object",
        properties: {
          dosya_yolu: { type: "string", description: "Mutlak HTML/JS dosya yolu" },
        },
        required: ["dosya_yolu"],
      },
    },
    {
      name: "versiyon_karsilastir",
      description: "İki oyun versiyonu arasındaki farkı listele.",
      inputSchema: {
        type: "object",
        properties: {
          eski: { type: "string" },
          yeni: { type: "string" },
          max_satir: { type: "number", default: 80 },
        },
        required: ["eski", "yeni"],
      },
    },
    {
      name: "hafiza_ara",
      description:
        "Stüdyo hafızasında semantik (anlam tabanlı) arama yap. " +
        "Tam kelime eşleşmesi gerekmez — kavramsal yakınlık yeterli. " +
        "Örnek: 'raycaster tıklama sorunu' → ilgili bug kayıtlarını bulur.",
      inputSchema: {
        type: "object",
        properties: {
          sorgu: { type: "string", description: "Doğal dil arama sorgusu (Türkçe)" },
          tablo: {
            type: "string",
            enum: ["studio_memory", "belgeler"],
            description: "studio_memory: kararlar/buglar | belgeler: GDD/dökümanlar",
            default: "belgeler",
          },
          kategori: {
            type: "string",
            description: "Filtre: bug | mimari | oyun | kulturel | proje",
          },
          sayi: { type: "number", default: 5 },
          min_benzerlik: { type: "number", default: 0.55 },
        },
        required: ["sorgu"],
      },
    },
    {
      name: "n8n_workflow_tetikle",
      description: "n8n workflow'unu webhook ile tetikle.",
      inputSchema: {
        type: "object",
        properties: {
          workflow_adi: { type: "string" },
          veri: { type: "object", default: {} },
        },
        required: ["workflow_adi"],
      },
    },
    {
      name: "itch_istatistik",
      description: "itch.io oyun istatistikleri: indirme, görüntülenme.",
      inputSchema: {
        type: "object",
        properties: {
          oyun_slug: { type: "string" },
        },
        required: ["oyun_slug"],
      },
    },
    {
      name: "todo_listele",
      description: "Proje dosyalarındaki açık TODO/FIXME'leri tara.",
      inputSchema: {
        type: "object",
        properties: {
          klasor: { type: "string", default: "~" },
          uzanti: { type: "string", default: "html,js" },
        },
        required: [],
      },
    },
    {
      name: "agent_listele",
      description: "Yüklü agent, skill, komut sayısını göster.",
      inputSchema: { type: "object", properties: {}, required: [] },
    },
  ],
}));

// ── Araç Handlerleri ─────────────────────────────────────────────────────────
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {

      case "oyun_sozdizimi_kontrol": {
        const dosya = String(args?.dosya_yolu ?? "").replace("~", process.env.HOME!);
        if (!existsSync(dosya)) {
          return { content: [{ type: "text", text: `❌ Dosya bulunamadı: ${dosya}` }] };
        }
        let icerik = readFileSync(dosya, "utf8");
        if (dosya.endsWith(".html")) {
          const eslesmeler = icerik.match(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi) ?? [];
          icerik = eslesmeler.map(b => b.replace(/<script[^>]*>|<\/script>/gi, "")).join("\n");
        }
        const gecici = join(tmpdir(), `check_${Date.now()}.js`);
        writeFileSync(gecici, icerik);
        try {
          execSync(`node --check ${gecici}`, { encoding: "utf8" });
          execSync(`rm -f ${gecici}`);
          return { content: [{ type: "text", text: `✅ Sözdizimi temiz: ${dosya}` }] };
        } catch (e: any) {
          execSync(`rm -f ${gecici}`);
          return { content: [{ type: "text", text: `⚠️ Sözdizimi hatası:\n${e.stderr ?? e.message}` }] };
        }
      }

      case "versiyon_karsilastir": {
        const eski = String(args?.eski ?? "").replace("~", process.env.HOME!);
        const yeni = String(args?.yeni ?? "").replace("~", process.env.HOME!);
        const maxSatir = Number(args?.max_satir ?? 80);
        try {
          const diff = execSync(`diff "${eski}" "${yeni}" | head -${maxSatir}`, { encoding: "utf8" });
          const eklenen = (diff.match(/^>/gm) ?? []).length;
          const silinen = (diff.match(/^</gm) ?? []).length;
          return { content: [{ type: "text", text: `+${eklenen} eklendi, -${silinen} silindi\n\n${diff}` }] };
        } catch (e: any) {
          const out = e.stdout as string ?? "";
          return { content: [{ type: "text", text: out || "Fark yok" }] };
        }
      }

      // ── HAFİZA ARAMA — GERÇEK SEMANTIC SEARCH ─────────────────────────────
      case "hafiza_ara": {
        if (!supabase) {
          return { content: [{ type: "text", text: "❌ SUPABASE_URL veya SUPABASE_KEY eksik" }] };
        }

        const sorgu = String(args?.sorgu ?? "");
        const tablo = String(args?.tablo ?? "belgeler") as "studio_memory" | "belgeler";
        const kategori = args?.kategori as string | undefined;
        const sayi = Number(args?.sayi ?? 5);
        const minBenzerlik = Number(args?.min_benzerlik ?? 0.55);

        // 1. Sorguyu embed et
        let embedding: number[];
        try {
          embedding = await getEmbedding(sorgu);
        } catch (e: any) {
          return { content: [{ type: "text", text: `❌ Embedding hatası: ${e.message}` }] };
        }

        // 2. pgvector semantik arama
        const fonksiyon = tablo === "studio_memory" ? "hafiza_ara" : "belge_ara";

        const rpcArgs: Record<string, unknown> = {
          sorgu_embedding: embedding,
          eslesme_sayisi: sayi,
          min_benzerlik: minBenzerlik,
        };
        if (tablo === "studio_memory" && kategori) rpcArgs.kategori_filtre = kategori;
        if (tablo === "belgeler" && kategori)      rpcArgs.tur_filtre = kategori;

        const { data, error } = await supabase.rpc(fonksiyon, rpcArgs);

        if (error) {
          return { content: [{ type: "text", text: `❌ Supabase RPC hatası: ${error.message}` }] };
        }
        if (!data?.length) {
          return { content: [{ type: "text", text: `Sonuç yok (min_benzerlik: ${minBenzerlik}). Daha düşük eşik dene.` }] };
        }

        const sonuc = (data as Array<Record<string, unknown>>)
          .map(k => {
            const benzerlik = typeof k.benzerlik === "number" ? `${(k.benzerlik * 100).toFixed(0)}%` : "?%";
            const baslik = String(k.baslik ?? "");
            const icerik = String(k.icerik ?? "").slice(0, 300);
            const kaynak = String(k.kaynak ?? k.kategori ?? "");
            return `📌 [${kaynak}] ${baslik} (${benzerlik})\n   ${icerik}`;
          })
          .join("\n\n");

        return { content: [{ type: "text", text: sonuc }] };
      }

      case "n8n_workflow_tetikle": {
        const n8nUrl = process.env.N8N_URL ?? "http://localhost:5678";
        const wf = String(args?.workflow_adi ?? "");
        const r = await fetch(`${n8nUrl}/webhook/${wf}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(args?.veri ?? {}),
          signal: AbortSignal.timeout(10_000),
        });
        return { content: [{ type: "text", text: r.ok ? `✅ Tetiklendi: ${wf}` : `❌ HTTP ${r.status}` }] };
      }

      case "itch_istatistik": {
        const key = process.env.ITCH_API_KEY;
        if (!key) return { content: [{ type: "text", text: "❌ ITCH_API_KEY eksik" }] };
        const r = await fetch(`https://itch.io/api/1/${key}/my-games`);
        const d = await r.json() as { games?: Array<{ title: string; url: string; views_count?: number; downloads_count?: number }> };
        const slug = String(args?.oyun_slug ?? "");
        const g = d.games?.find(x => x.url?.includes(slug));
        if (!g) return { content: [{ type: "text", text: `❌ "${slug}" bulunamadı` }] };
        return { content: [{ type: "text", text: `🎮 ${g.title}\n   Görüntülenme: ${g.views_count ?? "?"}\n   İndirme: ${g.downloads_count ?? "?"}` }] };
      }

      case "todo_listele": {
        const klasor = String(args?.klasor ?? "~").replace("~", process.env.HOME!);
        const uzantilar = String(args?.uzanti ?? "html,js").split(",").map(u => `--include="*.${u.trim()}"`).join(" ");
        try {
          const cikti = execSync(`grep -rn "TODO\\|FIXME\\|HACK\\|XXX" ${uzantilar} "${klasor}" 2>/dev/null | head -50`, { encoding: "utf8" });
          const n = cikti.trim() ? cikti.trim().split("\n").length : 0;
          return { content: [{ type: "text", text: n ? `📋 ${n} açık görev:\n\n${cikti}` : "✅ Açık TODO yok" }] };
        } catch { return { content: [{ type: "text", text: "✅ Açık TODO yok" }] }; }
      }

      case "agent_listele": {
        const ev = process.env.HOME!;
        const a = execSync(`ls ${ev}/.claude/agents/*.md 2>/dev/null | wc -l`, { encoding: "utf8" }).trim();
        const s = execSync(`find ${ev}/.claude/skills -name "SKILL.md" 2>/dev/null | wc -l`, { encoding: "utf8" }).trim();
        const k = execSync(`ls ${ev}/.claude/commands/*.md 2>/dev/null | wc -l`, { encoding: "utf8" }).trim();
        return { content: [{ type: "text", text: `📊 Agent: ${a}/30 | Skill: ${s}/23 | Komut: ${k}/28` }] };
      }

      default:
        return { content: [{ type: "text", text: `Bilinmeyen araç: ${name}` }] };
    }
  } catch (err: unknown) {
    return { content: [{ type: "text", text: `❌ Hata (${name}): ${err instanceof Error ? err.message : String(err)}` }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
