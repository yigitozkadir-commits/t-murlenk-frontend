---
description: Oyun ve uygulama metriklerini getir, analiz et.
tools: [bash]
---

Metrik raporu: $ARGUMENTS

ADIM 1 — MEVCUT VERİLER
```bash
# itch.io (Butler CLI kuruluysa)
butler status gokumay/$ARGUMENTS 2>/dev/null || \
  echo "itch.io: Butler kurulu değil — dashboard'dan kontrol et"

# Sentry son 7 gün
curl -s \
  -H "Authorization: DSN $SENTRY_DSN" \
  "https://sentry.io/api/0/projects/[org]/[proje]/stats/" \
  2>/dev/null | python3 -m json.tool || \
  echo "Sentry: API bağlantısı yok"

# Supabase'deki oyun verileri (varsa)
python3 ~/.claude/scripts/memory_client.py hatirla \
  "metrik $ARGUMENTS" proje
```

ADIM 2 — analytics-reporter ile analiz et

Elimdeki verilerden şu raporu üret:

```
## Metrik Raporu — $ARGUMENTS — $(date +%Y-%m-%d)

### Bu Hafta (Özet)
| Metrik | Değer | Trend |
|--------|-------|-------|
| İndirme | [N] | [↑/↓/→] |
| Aktif kullanıcı | [N] | [↑/↓/→] |
| Hata sayısı | [N] | [↑/↓/→] |
| Ort. oturum süresi | [N] dk | [↑/↓/→] |

### Kritik Bulgular
🚨 [Acil eylem gerektiren]
⚠️  [Dikkat gerektiren]
✅ [İyi giden]

### Önerilen Eylem
1. [En yüksek etkili — bu hafta]
2. [Orta vadeli — sonraki sprint]
```

ADIM 3 — HAFIZAYA KAYDET
```bash
python3 ~/.claude/scripts/memory_client.py kaydet \
  "Metrik: $ARGUMENTS — $(date +%Y-%m-%d)" \
  "Haftalık özet kaydedildi. Kritik: [var/yok]" \
  "proje" "$ARGUMENTS"
```

OYUN: $ARGUMENTS
