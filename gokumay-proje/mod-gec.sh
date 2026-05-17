#!/bin/bash
# mod-gec.sh — Katman 3 Geliştirme / Yayın Modu Geçişi
# Kullanım: bash mod-gec.sh [gelistirme|yayin]
# ~/.claude/scripts/mod-gec.sh

MOD="${1:-gelistirme}"
AGENT_DIR="$HOME/.claude/agents"
SCRIPT_DIR="$HOME/.claude/scripts"
LOG="$HOME/.claude/logs/mod.log"

mkdir -p "$HOME/.claude/logs"

yayina_ozel=(
  "monetization-optimizer"
  "community-manager"
)

yayin_botu_baslat() {
  # Discord botu
  if [[ -f "$SCRIPT_DIR/discord_bot.py" ]]; then
    pkill -f discord_bot.py 2>/dev/null || true
    nohup python3 "$SCRIPT_DIR/discord_bot.py" \
      > "$HOME/.claude/logs/discord.log" 2>&1 &
    echo "✅ Discord botu başlatıldı (PID: $!)"
  fi

  # Reddit botu
  if [[ -f "$SCRIPT_DIR/reddit_manager.py" ]]; then
    pkill -f reddit_manager.py 2>/dev/null || true
    nohup python3 "$SCRIPT_DIR/reddit_manager.py" \
      > "$HOME/.claude/logs/reddit.log" 2>&1 &
    echo "✅ Reddit botu başlatıldı (PID: $!)"
  fi
}

yayin_botunu_durdur() {
  pkill -f discord_bot.py 2>/dev/null && echo "🔴 Discord botu durduruldu" || true
  pkill -f reddit_manager.py 2>/dev/null && echo "🔴 Reddit botu durduruldu" || true
}

if [[ "$MOD" == "yayin" ]]; then
  echo "🚀 YAYIN MODUNA GEÇİLİYOR"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Yayına özel agent'ları aktifleştir (devre dışı klasöründen geri getir)
  DEVRE_DISI="$AGENT_DIR/_devre_disi"
  mkdir -p "$DEVRE_DISI"

  for agent in "${yayina_ozel[@]}"; do
    if [[ -f "$DEVRE_DISI/$agent.md" ]]; then
      mv "$DEVRE_DISI/$agent.md" "$AGENT_DIR/"
      echo "✅ Aktif: $agent"
    elif [[ -f "$AGENT_DIR/$agent.md" ]]; then
      echo "ℹ️  Zaten aktif: $agent"
    fi
  done

  yayin_botu_baslat
  echo "$(date): YAYIN MODU aktif" >> "$LOG"

elif [[ "$MOD" == "gelistirme" ]]; then
  echo "🔧 GELİŞTİRME MODUNA GEÇİLİYOR"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  DEVRE_DISI="$AGENT_DIR/_devre_disi"
  mkdir -p "$DEVRE_DISI"

  for agent in "${yayina_ozel[@]}"; do
    if [[ -f "$AGENT_DIR/$agent.md" ]]; then
      mv "$AGENT_DIR/$agent.md" "$DEVRE_DISI/"
      echo "🔴 Devre dışı: $agent"
    fi
  done

  yayin_botunu_durdur
  echo "$(date): GELİŞTİRME MODU aktif" >> "$LOG"

else
  echo "Kullanım: mod-gec.sh [gelistirme|yayin]"
  exit 1
fi

echo ""
echo "Aktif agent sayısı: $(ls "$AGENT_DIR"/*.md 2>/dev/null | wc -l)"
