---
description: Oyun veya uygulama lansman hazırlığı — tam kontrol listesi.
tools: [read, bash, edit]
---

$ARGUMENTS için lansman hazırlığı başlat.

FAZA 1 — TEKNİK KONTROL
```bash
node --check $ARGUMENTS  # Sözdizimi
grep -n "innerHTML\s*=" $ARGUMENTS  # XSS riski
grep -n "api.key\|apiKey\|sk-" $ARGUMENTS  # Secret sızıntısı
```

FAZA 2 — KALİTE KONTROL
- [ ] Oyun başlıyor mu?
- [ ] AI hamle yapıyor mu?
- [ ] Kazanma/kaybetme çalışıyor mu?
- [ ] Yeniden başlat çalışıyor mu?
- [ ] Tarayıcı konsolu temiz mi?
- [ ] FPS 30+?

FAZA 3 — İÇERİK HAZIRLIK
voice-dna ile şunları yaz:
- [ ] Kısa açıklama (Türkçe — 80 karakter)
- [ ] Uzun açıklama (İngilizce — 200 kelime)
- [ ] 5 itch.io etiketi
- [ ] İlk Reddit postu

FAZA 4 — KANAL SIRASI
1. GitHub Pages → Anında yayın
2. itch.io → Oyun topluluğu
3. BoardGameGeek → Niş kitle
4. Reddit (r/chess veya r/IndieGaming)
5. Play Store (Capacitor ile — 1-3 gün onay)

FAZA 5 — ÖLÇÜM
İlk 2 haftada takip et:
- itch.io görüntülenme / indirme oranı
- Reddit upvote / yorum
- Play Store yükleme

LANSMAN TARIHI: [Bugün + 3 gün minimum]


