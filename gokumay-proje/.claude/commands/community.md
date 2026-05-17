---
description: Topluluk yönetimi — Discord bot, Reddit, içerik takvimi.
tools: [bash]
---

Topluluk görevi: $ARGUMENTS

DISCORD DURUMU:
```bash
# Bot çalışıyor mu?
pgrep -f "discord_bot.py" && echo "✅ Discord bot aktif" || \
  echo "⚠️  Bot çalışmıyor → python3 ~/.claude/scripts/discord_bot.py &"
```

REDDIT DURUMU:
```bash
python3 -c "
import praw, os
try:
    r = praw.Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID',''),
        client_secret=os.environ.get('REDDIT_SECRET',''),
        user_agent='GokUmay/1.0'
    )
    print('✅ Reddit bağlantısı OK:', r.user.me())
except Exception as e:
    print('⚠️ Reddit:', e)
" 2>/dev/null || echo "praw kurulu değil → pip install praw"
```

GÖREV YÖNLENDIR:
```
İçerik yaz   → /post [konu]
Duyuru yap   → /announce [oyun]
Bot kur      → community-manager skill → discord_bot.py
Reddit oto   → community-manager agent
Analitik     → /metrics [oyun]
```

HAFTALIK KONTROL:
```bash
# Bu hafta yanıtlanmamış yorumlar
echo "Discord: discord.com/channels/..."
echo "Reddit: reddit.com/user/GokUmay/comments"
echo "BoardGameGeek: boardgamegeek.com/..."
```

GÖREV: $ARGUMENTS
