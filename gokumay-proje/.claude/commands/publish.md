---
description: Oyunu tüm platformlara yayınla — tam pipeline.
tools: [bash, read, edit]
---

Yayın pipeline başlatılıyor: $ARGUMENTS

AŞAMA 1 — KALİTE KAPISI (hepsi geçmeden devam yok)
```bash
# Sözdizimi
node --check $ARGUMENTS && echo "✅ Sözdizimi" || echo "❌ Hata"

# Güvenlik
grep -n "innerHTML\s*=\|apiKey\|sk-" $ARGUMENTS | wc -l
```

qa-tester kontrol listesi:
- [ ] Oyun açılıyor
- [ ] AI hamle yapıyor
- [ ] Kazanma koşulu çalışıyor
- [ ] Konsol temiz

AŞAMA 2 — VERSİYON ONAYI
```bash
VERSIYON=$(grep -o "v[0-9]*" $ARGUMENTS | head -1)
echo "Yayınlanacak versiyon: $VERSIYON"
```

AŞAMA 3 — İÇERİK PAKETİ
publisher agent ile şunları üret:
- [ ] itch.io açıklaması (EN + TR)
- [ ] Play Store listing
- [ ] Reddit postu (r/chess veya r/boardgames)
- [ ] Discord duyurusu

AŞAMA 4 — PLATFORM YAYIMI
```bash
# GitHub Pages (anlık)
git add $ARGUMENTS
git commit -m "Yayın: $ARGUMENTS $VERSIYON"
git push origin main
echo "✅ GitHub Pages güncellendi"

# itch.io (Butler CLI)
butler push $ARGUMENTS gokumay/[oyun-adi]:html5 \
  --userversion $VERSIYON 2>/dev/null && \
  echo "✅ itch.io güncellendi" || \
  echo "⚠️ Butler kurulu değil — manuel yükle"
```

AŞAMA 5 — MOBİL (opsiyonel)
```bash
# Capacitor hazır mı?
ls capacitor.config.json 2>/dev/null && \
  echo "Capacitor: ✅ — npx cap copy && npx cap open android" || \
  echo "Capacitor: kurulu değil"
```

AŞAMA 6 — HAFIZAYA KAYDET
```bash
python3 ~/.claude/scripts/memory_client.py kaydet \
  "Yayın: $ARGUMENTS $VERSIYON — $(date +%Y-%m-%d)" \
  "Yayınlanan platformlar: GitHub Pages, itch.io. Sonraki: Play Store." \
  "proje"
```

AŞAMA 7 — ANALİTİK BAŞLAT
Sentry release'i güncelle:
```bash
# sentry-cli kuruluysa
sentry-cli releases new $VERSIYON
sentry-cli releases finalize $VERSIYON
```

YAYINLANAN: $ARGUMENTS
