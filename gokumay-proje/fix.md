---
description: Hatayı tespit et, kök nedenini bul, düzelt, önle.
tools: [read, edit, bash]
---

Şu hatayı analiz et ve düzelt: $ARGUMENTS

ADIM 1 — TANI (5 Neden tekniği)
"Hata oluştu. Neden? ... Neden? ... Neden? ... Neden? ... Neden?"
Kök nedene ulaşana kadar devam et.

ADIM 2 — HİPOTEZLER
Olası 3 neden (basitten karmaşığa):
1. [En basit açıklama]
2. [Orta karmaşıklık]
3. [Sistemik sorun]

ADIM 3 — ELİMİNASYON
Hangi hipotezi neden eliyorum — kanıta dayalı.

ADIM 4 — DÜZELTME
```bash
node --check dosya.js  # Önce sözdizimi kontrol
```
Tam düzeltme kodunu yaz, uygula.

ADIM 5 — DOĞRULAMA
```bash
node --check dosya.js  # Tekrar kontrol
```
Tarayıcı konsolunda test adımlarını listele.

ADIM 6 — ÖNLEME
Bu hata neden tekrar oluşabilir? → Hangi kalıbı değiştirmeli?

ÇIKTI FORMATI:
```
Kök neden: [tek cümle]
Düzeltme: [kaç satır değişti]
Tekrar riski: [düşük/orta/yüksek]
```


