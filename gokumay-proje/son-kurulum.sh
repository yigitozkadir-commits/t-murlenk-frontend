#!/bin/bash
# son-kurulum.sh — Gök Umay %4 Son Paket
# n8n workflow'ları + 30 agent eval
# Kullanım: bash son-kurulum.sh

set -e
echo "🏁 Gök Umay — Son Paket (%4)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REPO="$(cd "$(dirname "$0")" && pwd)"
N8N_DIR="$HOME/.claude/n8n-workflows"
SCRIPTS="$HOME/.claude/scripts"

# ── 1. n8n Workflow JSON'ları ──────────────────────────────────────────────────
echo ""
echo "1️⃣  n8n workflow'ları kopyalanıyor..."
mkdir -p "$N8N_DIR"

for wf in discord-bug discord-duyuru deploy-itch yayin-pipeline; do
  cp "$REPO/n8n-workflows/$wf.json" "$N8N_DIR/"
  echo "   ✅ $wf.json"
done

echo ""
echo "   📋 n8n'e aktarma talimatı:"
echo "   1. http://localhost:5678 → Workflows → Import from File"
echo "   2. Sırayla yükle (bağımlılık sırası önemli):"
echo "      a. discord-bug.json"
echo "      b. discord-duyuru.json"
echo "      c. deploy-itch.json"
echo "      d. yayin-pipeline.json"
echo "   3. Her workflow'da Settings → Activate = ON yap"
echo "   4. Ortam değişkenlerini n8n Settings → Variables'a ekle:"
echo "      GITHUB_REPO, GITHUB_TOKEN, ITCH_USERNAME, DISCORD_WEBHOOK_URL"

# Butler CLI kontrolü (deploy-itch için)
echo ""
if which butler &>/dev/null; then
  echo "   ✅ butler CLI kurulu (itch.io deploy için)"
else
  echo "   ⚠️  butler CLI yok — kur:"
  echo "       curl -L -o butler.zip https://broth.itch.ovh/butler/linux-amd64/LATEST/archive/default"
  echo "       unzip butler.zip && mv butler ~/.local/bin/"
  echo "       butler login"
fi

# ── 2. Tam Agent Evals ────────────────────────────────────────────────────────
echo ""
echo "2️⃣  Tam agent eval sistemi kuruluyor (30 agent)..."
cp "$REPO/evals/agent_evals_tam.py" "$SCRIPTS/"

# Eski agent_evals.py'yi yedekle
if [[ -f "$SCRIPTS/agent_evals.py" ]]; then
  mv "$SCRIPTS/agent_evals.py" "$SCRIPTS/agent_evals_8agent.py.bak"
  echo "   ✅ Eski eval yedeklendi: agent_evals_8agent.py.bak"
fi

# Yeni dosyayı standart isimle de kopyala
cp "$SCRIPTS/agent_evals_tam.py" "$SCRIPTS/agent_evals.py"
echo "   ✅ agent_evals.py → 30 agent (60 vaka)"

# Hızlı test
echo ""
echo "   🧪 Hızlı eval testi (5 kritik agent)..."
python3 "$SCRIPTS/agent_evals.py" --hizli 2>/dev/null | grep -E "✅|❌|Genel" || \
  echo "   ⚠️  Test çalışmadı — ANTHROPIC_API_KEY kontrol et"

# ── Özet ─────────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Son Paket Özeti"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ n8n: 4 workflow JSON → ~/.claude/n8n-workflows/"
echo "✅ Evals: 30 agent × 60 vaka (Katman 1+2+3)"
echo ""
echo "Kullanım:"
echo "  Tüm agentlar: python3 ~/.claude/scripts/agent_evals.py"
echo "  Katman bazlı: python3 ~/.claude/scripts/agent_evals.py --katman 1"
echo "  Tek agent:    python3 ~/.claude/scripts/agent_evals.py qa-tester"
echo "  Hızlı:        python3 ~/.claude/scripts/agent_evals.py --hizli"
echo ""
echo "  n8n test:     curl -X POST http://localhost:5678/webhook/discord-duyuru \\"
echo "                  -H 'Content-Type: application/json' \\"
echo "                  -d '{\"oyun\": \"Timurlenk\", \"versiyon\": \"v35\", \"ozet\": \"Test\"}'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
