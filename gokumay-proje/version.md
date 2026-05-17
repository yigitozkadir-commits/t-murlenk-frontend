---
description: Yeni versiyon geçişi — debug, geliştir, test, belgele.
tools: [read, edit, bash]
---

$ARGUMENTS dosyasını bir sonraki versiyona taşı.

ADIM 1 — MEVCUT DURUM
```bash
# Versiyon numarasını oku
grep -o "v[0-9]*" $ARGUMENTS | head -1
node --check $ARGUMENTS
```

ADIM 2 — AÇIK HATALARI LISTELE
systematic-debugger protokolüyle tara:
P0 (çöküyor), P1 (kırık özellik), P2 (görsel), P3 (kalite)

ADIM 3 — YAPILACAK İŞ
Bu versiyonda sadece şunu yap: $ARGUMENTS
(tek odak — çok şey değiştirme)

ADIM 4 — UYGULA
Değişikliği uygula.

ADIM 5 — DOĞRULA
```bash
node --check $ARGUMENTS
```
- [ ] Oyun açılıyor mu?
- [ ] AI rakip hamle yapıyor mu?
- [ ] Yeni özellik çalışıyor mu?
- [ ] Önceki özellikler kırılmadı mı?

ADIM 6 — VERSİYON ARTIR
Dosya adını v(N) → v(N+1) yap.
Değişiklik günlüğüne ekle:
```
## v[N+1] — [tarih]
- [Ne değişti]
```

ADIM 7 — CLAUDE.md GÜNCELLE
Aktif proje versiyonunu güncelle.


