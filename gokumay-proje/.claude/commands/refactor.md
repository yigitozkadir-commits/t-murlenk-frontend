---
description: Kodu temizle — davranış değiştirmeden yapıyı iyileştir.
tools: [read, edit]
---

$ARGUMENTS dosyasını refactor et.

KURALLAR:
- Davranışı kesinlikle değiştirme
- Her değişikliği tek satırda gerekçelendir
- Türkçe yorum ekle (eksikse)

ÖNCE ÖLÇÜM:
```bash
wc -l $ARGUMENTS  # Başlangıç satır sayısı
```

REFACTOR ÖNCELİK SIRASI:
1. Çift kod → fonksiyona al
2. Magic number → BÜYÜK_HARF sabit
3. İç içe if/else → erken return
4. 50+ satır fonksiyon → böl
5. Global değişken → kapsama al
6. Tekrar eden DOM seçici → değişkene al

Three.js özel:
- Paylaşılan geometry/material → tek tanım
- Render döngüsündeki nesne oluşturma → dışarı al

SONRA ÖLÇÜM:
```bash
wc -l $ARGUMENTS  # Bitiş satır sayısı
node --check $ARGUMENTS  # Sözdizimi hâlâ doğru mu?
```

ÇIKTI:
```
Önce: X satır → Sonra: Y satır (Z% azalma)
Değişiklikler:
1. [Ne] — [Neden]
Davranış değişmedi: ✅
```


