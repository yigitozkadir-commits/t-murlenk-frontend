#!/bin/bash
# Gök Umay — Katman 3 Kurulum Scripti
# Gereksinim: Katman 1 + Katman 2 kurulu olmalı

set -e
echo "🧠 Gök Umay Katman 3 — Zeka Katmanı"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REPO="$(cd "$(dirname "$0")" && pwd)"

# ── 1. Agent'lar ──────────────────────────────────
echo "📋 Agent'lar kopyalanıyor..."
for agent in mcp-server-builder rag-pipeline multi-agent-coordinator \
             playtest-ai monetization-optimizer community-manager; do
  cp "$REPO/.claude/agents/$agent.md" ~/.claude/agents/
done
echo "✅ 6 yeni agent (toplam: $(ls ~/.claude/agents/ | wc -l))"

# ── 2. Skill'ler ──────────────────────────────────
echo "🛠  Skill'ler kopyalanıyor..."
for skill in mcp-server-builder rag-pipeline multi-agent-coordinator \
             playtest-ai monetization-optimizer community-manager; do
  mkdir -p ~/.claude/skills/$skill
  cp "$REPO/.claude/skills/$skill/SKILL.md" ~/.claude/skills/$skill/
done
echo "✅ 6 yeni skill (toplam: $(find ~/.claude/skills -name 'SKILL.md' | wc -l))"

# ── 3. Komutlar ───────────────────────────────────
echo "💬 Komutlar kopyalanıyor..."
for cmd in mcp-add rag-index playtest chain community; do
  cp "$REPO/.claude/commands/$cmd.md" ~/.claude/commands/
done
echo "✅ 5 yeni komut (toplam: $(ls ~/.claude/commands/ | wc -l))"

# ── 4. CLAUDE.md güncelle ─────────────────────────
cat "$REPO/CLAUDE-KATMAN3-EKLENTI.md" >> ~/.claude/CLAUDE.md
echo "✅ CLAUDE.md güncellendi"

# ── 5. MCP sunucu klasörü ─────────────────────────
mkdir -p ~/.claude/mcp-servers/gokumay-araclar
cat > ~/.claude/mcp-servers/gokumay-araclar/package.json << 'EOF'
{
  "name": "gokumay-araclar",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "@supabase/supabase-js": "^2.0.0"
  }
}
EOF

# ── 6. Python bağımlılıkları ──────────────────────
echo "🐍 Bağımlılıklar kontrol ediliyor..."
pip install discord.py praw aiohttp --break-system-packages -q && \
  echo "✅ discord.py + praw kuruldu" || \
  echo "⚠️  discord.py veya praw kurulamadı"

# ── 7. Script'ler ─────────────────────────────────
mkdir -p ~/.claude/scripts ~/.claude/logs
cp "$REPO/scripts/"*.py ~/.claude/scripts/ 2>/dev/null || true
echo "✅ Script'ler kopyalandı"

# ── 8. tsx kontrolü (MCP için) ────────────────────
which tsx &>/dev/null && echo "✅ tsx kurulu" || \
  (npm install -g tsx && echo "✅ tsx kuruldu")

# ── 9. Doğrulama ──────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Katman 3 Özet"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Agent:    $(ls ~/.claude/agents/  | wc -l) (hedef: 30)"
echo "Skill:    $(find ~/.claude/skills -name 'SKILL.md' | wc -l) (hedef: 23)"
echo "Komut:    $(ls ~/.claude/commands/ | wc -l) (hedef: 28)"
echo ""
echo "Sonraki adımlar:"
echo "  1. ~/.env → Discord + Reddit token'larını ekle"
echo "  2. MCP sunucusu: cd ~/.claude/mcp-servers/gokumay-araclar && npm install"
echo "  3. claude mcp add gokumay-araclar --transport stdio -- tsx index.ts"
echo "  4. /rag-index ~/.claude/CLAUDE.md → Anayasayı indeksle"
echo "  5. /playtest [oyun].html → İlk test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
