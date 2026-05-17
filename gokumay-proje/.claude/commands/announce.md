---
description: Oyun güncellemesi veya yeni yayın duyurusu — tüm kanallar.
tools: [bash, edit]
---

Duyuru hazırla: $ARGUMENTS

ADIM 1 — BAĞLAM TOPLA
```bash
# Hangi oyun, hangi versiyon?
VERSIYON=$(grep -o "v[0-9]*" *.html 2>/dev/null | sort -V | tail -1)
echo "Versiyon: $VERSIYON"

# Son değişiklikler
git log --oneline -5 2>/dev/null || echo "Git log yok"
```

ADIM 2 — voice-dna + humanizer ZİNCİRİ

Her platform için ayrı üret — voice-dna kurallarıyla:

### Discord (#güncellemeler)
```
🎮 **$ARGUMENTS $VERSIYON Yayında**

[Ne değişti — 2-3 madde, emoji ile]

🔗 [Link]

[Tarihi bilgi veya ilginç teknik detay — opsiyonel]
```

### Twitter/X
```
[Oyun adı] $VERSIYON: [tek cümle değişiklik]
[Link] #chess #indiegame #html5
```

### Reddit başlığı
```
"[$VERSIYON] $ARGUMENTS — [en önemli özellik] güncellendi"
```

### Telegram (kişisel log)
```
📝 $ARGUMENTS $VERSIYON
$(date +%Y-%m-%d)
Değişiklikler: [liste]
Sonraki: [plan]
```

ADIM 3 — N8N İLE GÖNDER (kuruluysa)
```bash
# n8n duyuru workflow'unu tetikle
curl -X POST http://localhost:5678/webhook/duyuru \
  -H "Content-Type: application/json" \
  -d "{
    \"oyun\": \"$ARGUMENTS\",
    \"versiyon\": \"$VERSIYON\",
    \"tarih\": \"$(date +%Y-%m-%d)\"
  }" 2>/dev/null && \
  echo "✅ n8n duyuru workflow tetiklendi" || \
  echo "n8n çalışmıyor — manuel paylaş"
```

ADIM 4 — HAFIZAYA KAYDET
```bash
python3 ~/.claude/scripts/memory_client.py kaydet \
  "Duyuru: $ARGUMENTS $VERSIYON" \
  "$(date +%Y-%m-%d) — Discord + Twitter + Reddit duyurusu yapıldı" \
  "proje"
```

KONU: $ARGUMENTS
