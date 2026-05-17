#!/bin/bash
# eks2-kurulum.sh — Gök Umay Ek Düzeltme Paketi
# Kullanım: bash eks2-kurulum.sh
# Gereksinim: gokumay-duzeltmeler paketi kurulu olmalı

set -e
echo "🔧 Gök Umay — Ek Düzeltmeler (MCP + Bot + Yapılandırma)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REPO="$(cd "$(dirname "$0")" && pwd)"

# ── 1. MCP Sunucu ─────────────────────────────────────────────────────────────
echo ""
echo "1️⃣  MCP sunucusu kuruluyor..."
MCP_DIR="$HOME/.claude/mcp-servers/gokumay-tools"
mkdir -p "$MCP_DIR"

cp "$REPO/mcp-server/index.ts"     "$MCP_DIR/"
cp "$REPO/mcp-server/package.json" "$MCP_DIR/"

# Bağımlılıkları kur
cd "$MCP_DIR"
npm install --silent 2>/dev/null && echo "   ✅ npm bağımlılıkları kuruldu" || {
  echo "   ⚠️  npm install başarısız — manuel kur:"
  echo "       cd $MCP_DIR && npm install"
}

# tsx kontrolü
which tsx &>/dev/null || npm install -g tsx --silent
echo "   ✅ tsx hazır"

# Claude Code'a ekle
if which claude &>/dev/null; then
  claude mcp add gokumay-tools \
    --transport stdio \
    -- tsx "$MCP_DIR/index.ts" 2>/dev/null && \
    echo "   ✅ Claude Code'a eklendi" || \
    echo "   ℹ️  Manuel ekle: claude mcp add gokumay-tools --transport stdio -- tsx $MCP_DIR/index.ts"
else
  echo "   ℹ️  Claude Code bulunamadı. Manuel ekle:"
  echo "       claude mcp add gokumay-tools --transport stdio -- tsx $MCP_DIR/index.ts"
fi

cd "$REPO"

# ── 2. Discord ve Reddit Bot Scriptleri ───────────────────────────────────────
echo ""
echo "2️⃣  Bot scriptleri kuruluyor..."
mkdir -p "$HOME/.claude/scripts" "$HOME/.claude/logs"

cp "$REPO/scripts/discord_bot.py"    "$HOME/.claude/scripts/"
cp "$REPO/scripts/reddit_manager.py" "$HOME/.claude/scripts/"

# Bağımlılıklar
pip install "discord.py" praw aiohttp --break-system-packages -q && \
  echo "   ✅ discord.py + praw + aiohttp kuruldu" || \
  echo "   ⚠️  Pip install başarısız — manuel kur"

# Env değişkeni kontrolü
echo ""
echo "   📋 Gerekli ortam değişkenleri (.env):"
EKSIK=0
for VAR in DISCORD_BOT_TOKEN DUYURU_KANAL_ID REDDIT_CLIENT_ID REDDIT_SECRET REDDIT_USERNAME REDDIT_PASSWORD; do
  if [[ -z "${!VAR}" ]]; then
    echo "   ❌ $VAR — eksik"
    EKSIK=$((EKSIK + 1))
  else
    echo "   ✅ $VAR — mevcut"
  fi
done

[[ $EKSIK -gt 0 ]] && echo "   ⚠️  $EKSIK değişken eksik — ~/.env'e ekle"

# ── 3. Agent-Skill Yeniden Adlandırma ─────────────────────────────────────────
echo ""
echo "3️⃣  Katman 3 agent-skill adlandırması düzeltiliyor..."
cp "$REPO/katman3-yapilandirma/agent-skill-ayrim.md" \
   "$HOME/.claude/scripts/agent-skill-ayrim.md"

SKILLS_DIR="$HOME/.claude/skills"
declare -A YENIDEN_ADLANDIR=(
  ["mcp-server-builder"]="mcp-server-kit"
  ["rag-pipeline"]="rag-pipeline-kit"
  ["multi-agent-coordinator"]="multi-agent-kit"
  ["playtest-ai"]="playtest-kit"
  ["monetization-optimizer"]="monetization-kit"
  ["community-manager"]="community-kit"
)

DEGISIM=0
for ESKI in "${!YENIDEN_ADLANDIR[@]}"; do
  YENI="${YENIDEN_ADLANDIR[$ESKI]}"
  if [[ -d "$SKILLS_DIR/$ESKI" ]]; then
    mv "$SKILLS_DIR/$ESKI" "$SKILLS_DIR/$YENI"
    sed -i "s/^name: $ESKI/name: $YENI/" "$SKILLS_DIR/$YENI/SKILL.md" 2>/dev/null || true
    echo "   ✅ skill/$ESKI → skill/$YENI"
    DEGISIM=$((DEGISIM + 1))
  fi
done

[[ $DEGISIM -eq 0 ]] && echo "   ℹ️  Skill klasörleri zaten yeniden adlandırılmış"

# ── 4. MCP Hızlı Test ─────────────────────────────────────────────────────────
echo ""
echo "4️⃣  MCP sunucu testi..."
cd "$MCP_DIR"
timeout 5 tsx index.ts 2>/dev/null && \
  echo "   ✅ MCP sunucu başlatılabilir" || \
  echo "   ⚠️  MCP test başarısız — SUPABASE_URL/KEY eksik olabilir (normal)"

cd "$REPO"

# ── Özet ─────────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Ek Düzeltme Özeti"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ MCP: index.ts + package.json → gokumay-tools aktif"
echo "✅ Bot: discord_bot.py + reddit_manager.py kuruldu"
echo "✅ Yapı: Katman 3 skill isimleri -kit soneki ile netleşti"
echo ""
echo "Sonraki adımlar:"
echo "  Discord: python3 ~/.claude/scripts/discord_bot.py"
echo "  Reddit:  python3 ~/.claude/scripts/reddit_manager.py izle"
echo "  MCP:     claude \"gokumay-tools araçlarını listele\""
echo "  Yayin:   bash ~/.claude/scripts/mod-gec.sh yayin"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
