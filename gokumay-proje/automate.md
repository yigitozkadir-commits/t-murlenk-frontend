---
description: Tekrarlayan görevi Termux bash script'e dönüştür.
tools: [bash, edit]
---

$ARGUMENTS görevini otomatize et.

ANALİZ:
1. Bu görev ne sıklıkla yapılıyor?
2. Her seferinde kaç dakika alıyor?
3. Adımları listele (manuel olarak)
4. Sabit adımlar hangisi, değişken hangisi?

ARAÇ SEÇİMİ:
```
Basit → bash script (~/.claude/scripts/)
Zamanlanmış → cron (crontab -e)
Event-driven → Claude Code hook
Görsel → n8n (sunucu gerekir)
```

BASH SCRIPT:
```bash
#!/bin/bash
# [Görev adı] — Gök Umay otomasyonu
# Oluşturma: $(date)

set -e   # Hata olursa dur
set -u   # Tanımsız değişken kullanma

LOG="$HOME/.claude/logs/$(date +%Y%m%d).log"
mkdir -p "$(dirname $LOG)"

log() { echo "[$(date +%H:%M:%S)] $1" | tee -a "$LOG"; }

log "Başladı: $ARGUMENTS"

# [ADIM 1]
# [ADIM 2]

log "✅ Tamamlandı"
```

CRON EKLEMESİ (gerekirse):
```bash
# crontab -e
# Her gece 23:00
0 23 * * * /path/to/script.sh >> ~/.claude/logs/cron.log 2>&1
```

TEST ET:
```bash
bash -x script.sh  # Her komutu göster
```

Beklenen zaman tasarrufu: [X dakika/gün]


