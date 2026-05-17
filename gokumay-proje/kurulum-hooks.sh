#!/bin/bash
# Gök Umay — Hook Kurulum Scripti
# Kullanım: bash kurulum-hooks.sh

set -e
mkdir -p ~/.claude/hooks ~/.claude/session-backups
echo "📁 Hook klasörü hazır"

# 1. TEHLİKELİ KOMUT ENGELLEYİCİ
cat > ~/.claude/hooks/block-dangerous.sh << 'EOF'
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "
import sys,json
try: print(json.load(sys.stdin).get('tool_input',{}).get('command',''))
except: print('')
")
for p in "rm -rf /" "dd if=" "mkfs" ":(){:|:&};:" "chmod 777 /"; do
  echo "$CMD" | grep -qF "$p" && \
    echo "{\"block\":true,\"message\":\"⛔ Engellendi: $p\"}" >&2 && exit 2
done
exit 0
EOF

# 2. GİZLİ BİLGİ KORUYUCU
cat > ~/.claude/hooks/protect-secrets.sh << 'EOF'
#!/bin/bash
INPUT=$(cat)
CONTENT=$(echo "$INPUT" | python3 -c "
import sys,json
try: print(str(json.load(sys.stdin).get('tool_input','')))
except: print('')
")
for p in "sk-[a-zA-Z0-9]{48}" "ghp_[a-zA-Z0-9]{36}" "AKIA[0-9A-Z]{16}"; do
  echo "$CONTENT" | grep -qE "$p" && \
    echo '{"block":true,"message":"🔐 API key tespit edildi!"}' >&2 && exit 2
done
exit 0
EOF

# 3. NODE SÖZDIZIMI KONTROLÜ
cat > ~/.claude/hooks/node-check.sh << 'EOF'
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "
import sys,json
try: print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))
except: print('')
")
if echo "$FILE" | grep -qE "\.js$" && [ -f "$FILE" ]; then
  RESULT=$(node --check "$FILE" 2>&1)
  [ $? -ne 0 ] && echo "{\"feedback\":\"⚠️ Sözdizimi:\\n$RESULT\"}" >&2
fi
exit 0
EOF

# 4. TERMUX BİLDİRİMİ
cat > ~/.claude/hooks/notify-done.sh << 'EOF'
#!/bin/bash
termux-notification \
  --title "Gök Umay ✅" \
  --content "Claude görevi tamamladı!" \
  --vibrate 300 2>/dev/null || true
exit 0
EOF

# 5. OTURUM BAŞLANGIÇ
cat > ~/.claude/hooks/session-start.sh << 'EOF'
#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━"
echo "🏹 Gök Umay | $(date '+%d %b %Y %H:%M')"
echo "📁 $(pwd)"
echo "🌿 $(git branch --show-current 2>/dev/null || echo 'git yok')"
HTML=$(ls *.html 2>/dev/null | tail -3 | tr '\n' ' ')
[ -n "$HTML" ] && echo "🎮 $HTML"
TODO=$(grep -r "TODO\|FIXME" --include="*.js" --include="*.html" . 2>/dev/null | wc -l)
[ "$TODO" -gt 0 ] && echo "📋 $TODO açık TODO"
echo "━━━━━━━━━━━━━━━━━━━━━━"
exit 0
EOF

# 6. COMPACT ÖNCESİ YEDEK
cat > ~/.claude/hooks/pre-compact-backup.sh << 'EOF'
#!/bin/bash
TRANSCRIPT=$(ls ~/.claude/projects/*/transcripts/*.jsonl 2>/dev/null | tail -1)
[ -n "$TRANSCRIPT" ] && \
  cp "$TRANSCRIPT" ~/.claude/session-backups/$(date +%Y%m%d-%H%M%S).jsonl && \
  echo "✅ Oturum yedeklendi"
exit 0
EOF

chmod +x ~/.claude/hooks/*.sh
echo ""
echo "✅ 6 hook kuruldu:"
ls ~/.claude/hooks/
echo ""
echo "Sonraki adım: settings.json → ~/.claude/settings.json"


