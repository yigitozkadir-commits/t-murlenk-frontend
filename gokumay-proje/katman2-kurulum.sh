#!/bin/bash
# Gök Umay — Katman 2 Kurulum Scripti
# Kullanım: bash katman2-kurulum.sh
# Mevcut Katman 1 kurulu olmalı

set -e
echo "🚀 Gök Umay Katman 2 Kurulumu"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── 1. Yeni agent'lar ─────────────────────────────
echo "📋 Agent'lar kopyalanıyor..."
cp "$REPO_DIR"/.claude/agents/n8n-orchestrator.md    ~/.claude/agents/
cp "$REPO_DIR"/.claude/agents/memory-manager.md      ~/.claude/agents/
cp "$REPO_DIR"/.claude/agents/publisher.md           ~/.claude/agents/
cp "$REPO_DIR"/.claude/agents/analytics-reporter.md  ~/.claude/agents/
echo "✅ 4 yeni agent eklendi (toplam: $(ls ~/.claude/agents/ | wc -l))"

# ── 2. Yeni skill'ler ─────────────────────────────
echo "🛠  Skill'ler kopyalanıyor..."
for skill in n8n-workflows prompt-caching supabase-memory \
             gemini-hybrid sentry-monitoring store-listing; do
  mkdir -p ~/.claude/skills/$skill
  cp "$REPO_DIR"/.claude/skills/$skill/SKILL.md \
     ~/.claude/skills/$skill/SKILL.md
done
echo "✅ 6 yeni skill eklendi (toplam: $(find ~/.claude/skills -name 'SKILL.md' | wc -l))"

# ── 3. Yeni komutlar ──────────────────────────────
echo "💬 Komutlar kopyalanıyor..."
for cmd in workflow remember recall publish deploy announce metrics cost-check; do
  cp "$REPO_DIR"/.claude/commands/$cmd.md ~/.claude/commands/
done
echo "✅ 8 yeni komut eklendi (toplam: $(ls ~/.claude/commands/ | wc -l))"

# ── 4. CLAUDE.md güncelle ─────────────────────────
echo "📄 CLAUDE.md güncelleniyor..."
cat "$REPO_DIR/CLAUDE-KATMAN2-EKLENTI.md" >> ~/.claude/CLAUDE.md
echo "✅ CLAUDE.md genişletildi"

# ── 5. Python bağımlılıkları ──────────────────────
echo "🐍 Python bağımlılıkları kontrol ediliyor..."
python3 -c "import supabase" 2>/dev/null || \
  pip install supabase --break-system-packages -q
python3 -c "import anthropic" 2>/dev/null || \
  pip install anthropic --break-system-packages -q
echo "✅ Python bağımlılıkları hazır"

# ── 6. Script klasörü ─────────────────────────────
echo "📁 Script klasörü oluşturuluyor..."
mkdir -p ~/.claude/scripts
cp "$REPO_DIR"/scripts/memory_client.py ~/.claude/scripts/
chmod +x ~/.claude/scripts/memory_client.py
echo "✅ memory_client.py eklendi"

# ── 7. n8n kontrol ────────────────────────────────
echo ""
echo "🔄 n8n durumu kontrol ediliyor..."
npm list -g n8n 2>/dev/null | grep n8n && \
  echo "✅ n8n kurulu" || \
  echo "⚠️  n8n kurulu değil → npm install -g n8n"

# ── 8. Gemini kontrol ─────────────────────────────
echo ""
echo "♊ Gemini CLI kontrol ediliyor..."
which gemini 2>/dev/null && echo "✅ Gemini kurulu" || \
  echo "⚠️  Gemini kurulu değil → npm install -g @google/gemini-cli"

# ── 9. Ortam değişkenleri kontrol ─────────────────
echo ""
echo "🔑 Ortam değişkenleri kontrol ediliyor..."
EKSIK=0
for VAR in SUPABASE_URL SUPABASE_KEY N8N_API_KEY GEMINI_API_KEY; do
  if [ -z "${!VAR}" ]; then
    echo "  ⚠️  $VAR tanımlı değil"
    EKSIK=$((EKSIK + 1))
  else
    echo "  ✅ $VAR"
  fi
done

if [ $EKSIK -gt 0 ]; then
  echo ""
  echo "  ~/.env dosyasına ekle:"
  echo "  export SUPABASE_URL='...'"
  echo "  export SUPABASE_KEY='...'"
  echo "  export N8N_API_KEY='...'"
  echo "  export GEMINI_API_KEY='...'"
fi

# ── 10. Doğrulama ─────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Katman 2 Kurulum Özeti"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AGENTS=$(ls ~/.claude/agents/ | wc -l)
SKILLS=$(find ~/.claude/skills -name "SKILL.md" | wc -l)
CMDS=$(ls ~/.claude/commands/ | wc -l)

echo "Agent'lar:  $AGENTS (Katman 1: 20, Katman 2: 4)"
echo "Skill'ler:  $SKILLS (Katman 1: 11, Katman 2: 6)"
echo "Komutlar:   $CMDS  (Katman 1: 15, Katman 2: 8)"
echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Sonraki adımlar:"
echo "  1. ~/.env → API key'leri ekle"
echo "  2. nohup n8n start & → n8n başlat"
echo "  3. claude → /cost-check → maliyet analizi"
echo "  4. claude → /recall 'ilk araştırma' → hafıza test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
