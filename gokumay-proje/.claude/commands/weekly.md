---
description: Haftalık sprint değerlendirmesi ve sonraki hafta planı.
tools: [bash, read, edit]
---

Haftalık değerlendirme yap.

MEVCUT DURUM:
```bash
# Bu haftaki değişiklikler
git log --oneline --since="7 days ago" 2>/dev/null || \
  ls -lt *.html 2>/dev/null | head -10

# Aktif oyun dosyaları ve versiyonları
ls -la *.html 2>/dev/null

# Açık TODO'lar
grep -r "TODO\|FIXME" --include="*.html" --include="*.js" . 2>/dev/null | wc -l
```

BU HAFTA DEĞERLENDİRME:
### Tamamlanan
- [liste]

### Yarım Kalan
- [liste]

### Karşılaşılan Sorunlar
- [liste + nasıl çözüldü]

### Öğrenilenler
- [liste]

SONRAKI HAFTA PLANI:
Odak: [tek özellik veya oyun]
Agent sırası: [workflow-orchestrator formatında]

Versiyon hedefleri:
- [Oyun 1] v[N] → v[N+1]: [ne değişecek]

CLAUDE.md güncelleme gerekiyor mu?
- Aktif proje versiyonları
- Yeni altın kural
- Arşive taşınacak proje


