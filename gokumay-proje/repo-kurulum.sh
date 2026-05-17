#!/bin/bash
# Gök Umay — Repo Kurulum Scripti
# Kullanım: bash repo-kurulum.sh
# Termux veya Linux terminal

set -e
echo "🏹 Gök Umay Claude Code Kurulumu"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Klasör yapısı ──────────────────────────────
echo "📁 Klasörler oluşturuluyor..."
mkdir -p ~/.claude/agents
mkdir -p ~/.claude/commands
mkdir -p ~/.claude/session-backups
mkdir -p ~/.claude/logs

# Skills alt klasörleri
for skill in systematic-debugging owasp-security vibesec \
             three-js-patterns game-ai-engine minimax-ai \
             frontend-design notebooklm humanizer seo-geo \
             capacitor-mobile; do
  mkdir -p ~/.claude/skills/$skill
done

echo "✅ Klasörler hazır"

# ── 2. Dosyaları kopyala ──────────────────────────
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "📂 Repo: $REPO_DIR"

# CLAUDE.md ve settings
cp "$REPO_DIR/.claude/CLAUDE.md" ~/.claude/CLAUDE.md
cp "$REPO_DIR/.claude/settings.json" ~/.claude/settings.json
echo "✅ Anayasa ve ayarlar kopyalandı"

# Agents (20 dosya)
cp "$REPO_DIR"/.claude/agents/*.md ~/.claude/agents/
AGENT_COUNT=$(ls ~/.claude/agents/ | wc -l)
echo "✅ Agent'lar kopyalandı: $AGENT_COUNT dosya"

# Skills (11 klasör)
for skill in "$REPO_DIR"/.claude/skills/*/; do
  name=$(basename "$skill")
  cp "$skill/SKILL.md" ~/.claude/skills/$name/SKILL.md 2>/dev/null || true
done
SKILL_COUNT=$(find ~/.claude/skills -name "SKILL.md" | wc -l)
echo "✅ Skill'ler kopyalandı: $SKILL_COUNT dosya"

# Commands (15 dosya)
cp "$REPO_DIR"/.claude/commands/*.md ~/.claude/commands/
CMD_COUNT=$(ls ~/.claude/commands/ | wc -l)
echo "✅ Komutlar kopyalandı: $CMD_COUNT dosya"

# .claudeignore — proje köküne değil, home'a
cp "$REPO_DIR/.claudeignore" ~/.claudeignore 2>/dev/null || true
echo "✅ .claudeignore kopyalandı"

# ── 3. Hook'ları kur ──────────────────────────────
echo ""
echo "🪝 Hook'lar kuruluyor..."
bash "$REPO_DIR/kurulum-hooks.sh"

# ── 4. Doğrulama ──────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Kurulum Doğrulama"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AGENTS=$(ls ~/.claude/agents/ 2>/dev/null | wc -l)
SKILLS=$(find ~/.claude/skills -name "SKILL.md" 2>/dev/null | wc -l)
CMDS=$(ls ~/.claude/commands/ 2>/dev/null | wc -l)
HOOKS=$(ls ~/.claude/hooks/ 2>/dev/null | wc -l)

echo "Agent'lar:  $AGENTS / 20  $([ $AGENTS -eq 20 ] && echo ✅ || echo ⚠️)"
echo "Skill'ler:  $SKILLS / 11  $([ $SKILLS -eq 11 ] && echo ✅ || echo ⚠️)"
echo "Komutlar:   $CMDS / 15   $([ $CMDS -eq 15 ] && echo ✅ || echo ⚠️)"
echo "Hook'lar:   $HOOKS / 6   $([ $HOOKS -ge 5 ] && echo ✅ || echo ⚠️)"

echo ""
if [ $AGENTS -eq 20 ] && [ $SKILLS -eq 11 ] && [ $CMDS -eq 15 ]; then
  echo "🎉 Kurulum tamamlandı! Kullanım:"
  echo ""
  echo "   cd ~/oyun-projesi"
  echo "   claude"
  echo ""
  echo "   İlk komut: /weekly"
else
  echo "⚠️  Bazı dosyalar eksik. Repo yapısını kontrol et."
  echo "   Beklenen: .claude/agents/, .claude/skills/, .claude/commands/"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"


