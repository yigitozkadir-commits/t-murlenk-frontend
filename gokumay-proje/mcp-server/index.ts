// ~/.claude/mcp-servers/gokumay-tools/index.ts
// Gök Umay MCP Sunucusu — 7 Araç
// Kurulum: tsx index.ts (test) | claude mcp add ... (prod)

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { execSync } from "child_process";
import { readFileSync, existsSync } from "fs";
import { createClient } from "@supabase/supabase-js";

// ── Supabase istemcisi (opsiyonel — env yoksa araçlar graceful fail) ──────────
const supabase =
  process.env.SUPABASE_URL && process.env.SUPABASE_KEY
    ? createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY)
    : null;

const server = new Server(
  { name: "gokumay-tools", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// ── ARAÇ LİSTESİ ──────────────────────────────────────────────────────────────
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "oyun_sozdizimi_kontrol",
      description:
        "HTML5 oyun dosyasındaki <script> bloklarını node --check ile doğrula. " +
        "Kaydetmeden önce sözdizimi hatası var mı? Hızlı kontrol.",
      inputSchema: {
        type: "object",
        properties: {
          dosya_yolu: { type: "string", description: "Mutlak yol: ~/projeler/timurlenk_v35.html" },
        },
        required: ["dosya_yolu"],
      },
    },
    {
      name: "versiyon_karsilastir",
      description:
        "İki oyun versiyonu arasındaki farkı listele. " +
        "v34 → v35 geçişinde ne değişti? Kaç satır etkilendi?",
      inputSchema: {
        type: "object",
        properties: {
          eski: { type: "string", description: "Eski versiyon yolu" },
          yeni: { type: "string", description: "Yeni versiyon yolu" },
          max_satir: { type: "number", description: "Maksimum diff satırı (varsayılan 80)", default: 80 },
        },
        required: ["eski", "yeni"],
      },
    },
    {
      name: "hafiza_ara",
      description:
        "Stüdyo hafızasında metin tabanlı arama yap. " +
        "Geçmişte bu bug'ı çözdük mü? O mimari kararın gerekçesi ne?",
      inputSchema: {
        type: "object",
        properties: {
          sorgu: { type: "string", description: "Arama terimi (Türkçe)" },
          kategori: {
            type: "string",
            enum: ["bug", "mimari", "oyun", "kulturel", "proje", "genel"],
            description: "Kategori filtresi (opsiyonel)",
          },
          sayi: { type: "number", description: "Sonuç sayısı (varsayılan 5)", default: 5 },
        },
        required: ["sorgu"],
      },
    },
    {
      name: "n8n_workflow_tetikle",
      description:
        "n8n üzerindeki bir workflow'u webhook ile tetikle. " +
        "Otomatik yayın, duyuru, deploy pipeline'larını başlat.",
      inputSchema: {
        type: "object",
        properties: {
          workflow_adi: {
            type: "string",
            description: "Webhook adı: yayin-pipeline | discord-duyuru | deploy-itch",
          },
          veri: {
            type: "object",
            description: "Workflow'a gönderilecek JSON veri",
            default: {},
          },
        },
        required: ["workflow_adi"],
      },
    },
    {
      name: "itch_istatistik",
      description: "itch.io oyun istatistiklerini getir: indirme, görüntülenme, rating.",
      inputSchema: {
        type: "object",
        properties: {
          oyun_slug: {
            type: "string",
            description: "itch.io oyun slug'ı: tamerlane-chess",
          },
        },
        required: ["oyun_slug"],
      },
    },
    {
      name: "todo_listele",
      description:
        "Proje dosyalarındaki TODO ve FIXME yorumlarını tara. " +
        "Kaç açık görev var? Hangi dosyada?",
      inputSchema: {
        type: "object",
        properties: {
          klasor: {
            type: "string",
            description: "Taranacak klasör (varsayılan: HOME)",
            default: "~",
          },
          uzanti: {
            type: "string",
            description: "Dosya uzantısı filtresi: html | js | tümü",
            default: "html,js",
          },
        },
        required: [],
      },
    },
    {
      name: "agent_listele",
      description:
        "Yüklü Gök Umay agent'larını ve skill'lerini listele. " +
        "Hangi katman aktif? Sayı doğru mu?",
      inputSchema: {
        type: "object",
        properties: {},
        required: [],
      },
    },
  ],
}));

// ── ARAÇ HANDLERLARI ──────────────────────────────────────────────────────────
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {

      // 1. Sözdizimi Kontrolü ────────────────────────────────────────────────
      case "oyun_sozdizimi_kontrol": {
        const dosya = String(args?.dosya_yolu ?? "").replace("~", process.env.HOME!);
        if (!existsSync(dosya)) {
          return { content: [{ type: "text", text: `❌ Dosya bulunamadı: ${dosya}` }] };
        }

        let scriptIcerigi = "";

        if (dosya.endsWith(".html")) {
          // HTML içindeki script bloklarını çıkart
          const html = readFileSync(dosya, "utf8");
          const eslesmeler = html.match(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi) ?? [];
          scriptIcerigi = eslesmeler
            .map((b) => b.replace(/<script[^>]*>|<\/script>/gi, ""))
            .join("\n");
        } else {
          scriptIcerigi = readFileSync(dosya, "utf8");
        }

        // Geçici dosyaya yaz ve kontrol et
        const gecici = `/tmp/gokumay_check_${Date.now()}.js`;
        require("fs").writeFileSync(gecici, scriptIcerigi);

        try {
          execSync(`node --check ${gecici}`, { encoding: "utf8" });
          execSync(`rm -f ${gecici}`);
          return { content: [{ type: "text", text: `✅ Sözdizimi temiz: ${dosya}` }] };
        } catch (e: any) {
          execSync(`rm -f ${gecici}`);
          return { content: [{ type: "text", text: `⚠️ Sözdizimi hatası:\n${e.stderr ?? e.message}` }] };
        }
      }

      // 2. Versiyon Karşılaştırma ────────────────────────────────────────────
      case "versiyon_karsilastir": {
        const eski = String(args?.eski ?? "").replace("~", process.env.HOME!);
        const yeni = String(args?.yeni ?? "").replace("~", process.env.HOME!);
        const maxSatir = Number(args?.max_satir ?? 80);

        if (!existsSync(eski)) return { content: [{ type: "text", text: `❌ Bulunamadı: ${eski}` }] };
        if (!existsSync(yeni)) return { content: [{ type: "text", text: `❌ Bulunamadı: ${yeni}` }] };

        try {
          const diff = execSync(`diff "${eski}" "${yeni}" | head -${maxSatir}`, { encoding: "utf8" });
          const eklenen = (diff.match(/^>/gm) ?? []).length;
          const silinen = (diff.match(/^</gm) ?? []).length;
          return {
            content: [{
              type: "text",
              text: `📊 +${eklenen} satır eklendi, -${silinen} satır silindi\n\n${diff}`,
            }],
          };
        } catch (e: any) {
          // diff hata kodu 1 = fark var (normal)
          const cikti = e.stdout as string ?? "";
          const eklenen = (cikti.match(/^>/gm) ?? []).length;
          const silinen = (cikti.match(/^</gm) ?? []).length;
          return {
            content: [{
              type: "text",
              text: `📊 +${eklenen} satır eklendi, -${silinen} satır silindi\n\n${cikti.slice(0, maxSatir * 80)}`,
            }],
          };
        }
      }

      // 3. Hafıza Araması ────────────────────────────────────────────────────
      case "hafiza_ara": {
        if (!supabase) {
          return { content: [{ type: "text", text: "❌ SUPABASE_URL veya SUPABASE_KEY eksik" }] };
        }
        const sorgu = String(args?.sorgu ?? "");
        const kategori = args?.kategori as string | undefined;
        const sayi = Number(args?.sayi ?? 5);

        let query = supabase
          .from("studio_memory")
          .select("baslik, icerik, kategori, proje, onem")
          .or(`baslik.ilike.%${sorgu}%,icerik.ilike.%${sorgu}%`)
          .order("onem", { ascending: false })
          .limit(sayi);

        if (kategori) query = query.eq("kategori", kategori);

        const { data, error } = await query;
        if (error) return { content: [{ type: "text", text: `❌ Supabase hatası: ${error.message}` }] };
        if (!data?.length) return { content: [{ type: "text", text: "Kayıt bulunamadı." }] };

        const sonuc = data
          .map((k) => `📌 [${k.kategori}${k.proje ? "/" + k.proje : ""}] ${k.baslik}\n   ${k.icerik.slice(0, 250)}`)
          .join("\n\n");

        return { content: [{ type: "text", text: sonuc }] };
      }

      // 4. n8n Workflow Tetikleme ─────────────────────────────────────────────
      case "n8n_workflow_tetikle": {
        const n8nUrl = process.env.N8N_URL ?? "http://localhost:5678";
        const workflowAdi = String(args?.workflow_adi ?? "");
        const veri = (args?.veri ?? {}) as Record<string, unknown>;

        const response = await fetch(`${n8nUrl}/webhook/${workflowAdi}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(veri),
          signal: AbortSignal.timeout(10_000),
        });

        return {
          content: [{
            type: "text",
            text: response.ok
              ? `✅ Workflow tetiklendi: ${workflowAdi} (HTTP ${response.status})`
              : `❌ Hata: HTTP ${response.status} — ${workflowAdi}`,
          }],
        };
      }

      // 5. itch.io İstatistik ────────────────────────────────────────────────
      case "itch_istatistik": {
        const apiKey = process.env.ITCH_API_KEY;
        if (!apiKey) return { content: [{ type: "text", text: "❌ ITCH_API_KEY eksik" }] };

        const response = await fetch(`https://itch.io/api/1/${apiKey}/my-games`);
        const data = (await response.json()) as { games?: Array<{ title: string; url: string; views_count?: number; downloads_count?: number; id: number }> };

        const slug = String(args?.oyun_slug ?? "");
        const oyun = data.games?.find((g) => g.url?.includes(slug));

        if (!oyun) {
          const isimler = data.games?.map((g) => g.title).join(", ") ?? "Oyun bulunamadı";
          return { content: [{ type: "text", text: `❌ "${slug}" bulunamadı. Mevcut: ${isimler}` }] };
        }

        return {
          content: [{
            type: "text",
            text: [
              `🎮 ${oyun.title}`,
              `   Görüntülenme: ${oyun.views_count ?? "?"}`,
              `   İndirme: ${oyun.downloads_count ?? "?"}`,
              `   URL: ${oyun.url}`,
            ].join("\n"),
          }],
        };
      }

      // 6. TODO Listele ──────────────────────────────────────────────────────
      case "todo_listele": {
        const klasor = String(args?.klasor ?? "~").replace("~", process.env.HOME!);
        const uzantilar = String(args?.uzanti ?? "html,js")
          .split(",")
          .map((u) => `--include="*.${u.trim()}"`)
          .join(" ");

        try {
          const cikti = execSync(
            `grep -rn "TODO\\|FIXME\\|HACK\\|XXX" ${uzantilar} "${klasor}" 2>/dev/null | head -50`,
            { encoding: "utf8" }
          );
          const satirSayisi = cikti.trim() ? cikti.trim().split("\n").length : 0;
          return {
            content: [{
              type: "text",
              text: satirSayisi
                ? `📋 ${satirSayisi} açık görev:\n\n${cikti}`
                : "✅ Açık TODO/FIXME yok",
            }],
          };
        } catch {
          return { content: [{ type: "text", text: "✅ Açık TODO/FIXME yok" }] };
        }
      }

      // 7. Agent/Skill Listele ───────────────────────────────────────────────
      case "agent_listele": {
        const ev = process.env.HOME!;
        const agentSayisi = execSync(`ls ${ev}/.claude/agents/*.md 2>/dev/null | wc -l`, { encoding: "utf8" }).trim();
        const skillSayisi = execSync(`find ${ev}/.claude/skills -name "SKILL.md" 2>/dev/null | wc -l`, { encoding: "utf8" }).trim();
        const komutSayisi = execSync(`ls ${ev}/.claude/commands/*.md 2>/dev/null | wc -l`, { encoding: "utf8" }).trim();
        const agentListesi = execSync(`ls ${ev}/.claude/agents/*.md 2>/dev/null | xargs -I{} basename {} .md | sort`, { encoding: "utf8" }).trim();

        return {
          content: [{
            type: "text",
            text: [
              `📊 Gök Umay Sistem Durumu`,
              `   Agent:  ${agentSayisi}/30`,
              `   Skill:  ${skillSayisi}/23`,
              `   Komut:  ${komutSayisi}/28`,
              ``,
              `Agent'lar:\n${agentListesi}`,
            ].join("\n"),
          }],
        };
      }

      default:
        return { content: [{ type: "text", text: `Bilinmeyen araç: ${name}` }] };
    }
  } catch (err: unknown) {
    const mesaj = err instanceof Error ? err.message : String(err);
    return { content: [{ type: "text", text: `❌ Araç hatası (${name}): ${mesaj}` }] };
  }
});

// ── BAŞLAT ────────────────────────────────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);
