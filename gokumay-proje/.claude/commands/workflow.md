---
description: n8n workflow oluştur veya güncelle.
tools: [bash, edit]
---

n8n workflow görevi: $ARGUMENTS

ADIM 1 — ANALIZ
"Bu görevi otomatize etmeli miyim?" testi:
- Sıklık: Haftada 3+ kez? →
- Süre: 5+ dakika? →
- Hata riski: Manuel yapınca hata oluyor? →
- Bağlantı: Birden fazla servis? →

ADIM 2 — WORKFLOW TASARIMI
Tetikleyici: [ne başlatır — webhook/cron/event]
Node zinciri:
1. [Node türü]: [ne yapar]
2. [Node türü]: [ne yapar]
...
Hata senaryosu: [ne olursa ne yapılır]

ADIM 3 — N8N DURUMU KONTROL
```bash
curl -s http://localhost:5678/healthz || echo "n8n çalışmıyor — başlat: nohup n8n start &"
```

ADIM 4 — MCP İLE OLUŞTUR
```
n8n üzerinden bu workflow'u oluştur:
[ADIM 2'deki tasarım]
```

ADIM 5 — TEST
```bash
curl -X POST http://localhost:5678/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": true, "konu": "$ARGUMENTS"}'
```

ADIM 6 — HAFIZAYA KAYDET
```bash
python3 ~/.claude/scripts/memory_client.py kaydet \
  "n8n workflow: $ARGUMENTS" \
  "Tetikleyici: [...] Node sayısı: [N] Durum: aktif" \
  "mimari" "genel"
```
