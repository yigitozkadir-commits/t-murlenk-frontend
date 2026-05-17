#!/bin/bash
# duzeltme-kurulum.sh — Gök Umay Düzeltme Paketi
# Kullanım: bash duzeltme-kurulum.sh
# Çalıştır: Repo kökünde (Katman 1+2+3 kurulu olmalı)

set -e
echo "🔧 Gök Umay — Düzeltme Paketi"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REPO="$(cd "$(dirname "$0")" && pwd)"

# ── 1. Embedding düzeltmesi ───────────────────────────────────────────────────
echo ""
echo "1️⃣  Embedding modülü kuruluyor..."
cp "$REPO/scripts/embedding.py" ~/.claude/scripts/
cp "$REPO/scripts/memory.py"    ~/.claude/scripts/
cp "$REPO/scripts/rag_client.py" ~/.claude/scripts/

# Provider seç
echo ""
echo "Embedding provider seç:"
echo "  [1] Voyage AI — önerilen (ucuz, Türkçe iyi)"
echo "  [2] OpenAI   — 1536 boyut"
read -rp "Seçim (1/2): " SECIM

if [[ "$SECIM" == "2" ]]; then
  sed -i 's/PROVIDER = os.environ.get("EMBED_PROVIDER", "voyage")/PROVIDER = os.environ.get("EMBED_PROVIDER", "openai")/' \
    ~/.claude/scripts/embedding.py
  pip install openai --break-system-packages -q
  echo "✅ OpenAI seçildi"
  echo "   >> ~/.env'e ekle: export OPENAI_API_KEY=\"sk-...\""
else
  pip install voyageai --break-system-packages -q
  echo "✅ Voyage AI seçildi"
  echo "   >> ~/.env'e ekle: export VOYAGE_API_KEY=\"pa-...\""
fi

# ── 2. Hook scriptleri ────────────────────────────────────────────────────────
echo ""
echo "2️⃣  Hook scriptleri kuruluyor..."
mkdir -p ~/.claude/hooks

for hook in block-dangerous protect-secrets node-check notify-done pre-compact-backup; do
  cp "$REPO/hooks/$hook.sh" ~/.claude/hooks/
  chmod +x ~/.claude/hooks/$hook.sh
  echo "   ✅ $hook.sh"
done

# settings.json kontrolü
SETTINGS="$HOME/.claude/settings.json"
if [[ ! -f "$SETTINGS" ]]; then
  cat > "$SETTINGS" << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/block-dangerous.sh"}]},
      {"matcher": "*", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/protect-secrets.sh"}]}
    ],
    "PostToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/node-check.sh"}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "bash ~/.claude/hooks/notify-done.sh"}]}
    ],
    "PreCompact": [
      {"hooks": [{"type": "command", "command": "bash ~/.claude/hooks/pre-compact-backup.sh"}]}
    ]
  }
}
EOF
  echo "   ✅ settings.json oluşturuldu"
else
  echo "   ℹ️  settings.json mevcut — hook'ları elle kontrol et"
fi

# ── 3. Katman 3 mod sistemi ───────────────────────────────────────────────────
echo ""
echo "3️⃣  Katman 3 mod sistemi kuruluyor..."
cp "$REPO/katman3-mod/mod-gec.sh" ~/.claude/scripts/
chmod +x ~/.claude/scripts/mod-gec.sh

cat "$REPO/katman3-mod/CLAUDE-K3-MOD-EKLENTI.md" >> ~/.claude/CLAUDE.md
echo "   ✅ mod-gec.sh kuruldu"
echo "   ✅ CLAUDE.md güncellendi"

# ── 4. Supabase schema notu ───────────────────────────────────────────────────
echo ""
echo "4️⃣  Supabase schema notu:"
cp "$REPO/scripts/schema-duzeltme.sql" ~/.claude/scripts/
echo "   📄 schema-duzeltme.sql hazır"
echo "   → Supabase SQL Editor'de çalıştır (Voyage AI kullanıyorsan)"

# ── 5. Embedding testi ────────────────────────────────────────────────────────
echo ""
echo "5️⃣  Embedding testi..."
source ~/.env 2>/dev/null || true
if python3 ~/.claude/scripts/embedding.py test 2>/dev/null; then
  echo "   ✅ Embedding çalışıyor"
else
  echo "   ⚠️  API key eksik — ~/.env'e ekle ve tekrar test et:"
  echo "      python3 ~/.claude/scripts/embedding.py test"
fi

# ── Özet ─────────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Düzeltme Özeti"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Embedding: [0.0]*1536 placeholder → gerçek API"
echo "✅ Hook scriptleri: 5 dosya kuruldu"
echo "✅ Mod sistemi: gelistirme/yayin geçişi aktif"
echo "✅ Schema: Voyage AI 1024-dim uyumu"
echo ""
echo "Sonraki adımlar:"
echo "  1. source ~/.env   (API key'leri yükle)"
echo "  2. python3 ~/.claude/scripts/embedding.py test"
echo "  3. Supabase SQL Editor → schema-duzeltme.sql çalıştır"
echo "  4. /rag-index ~/.claude/CLAUDE.md   (anayasayı indeksle)"
echo "  5. bash ~/.claude/scripts/mod-gec.sh gelistirme"
