---
name: systematic-debugging
description: |
  Konsol hatalarını, statik analiz bulgularını ve versiyon
  geçişi sorunlarını sistematik olarak çözer.
  Kullan: "systematic-debugging skill ile bu hatayı çöz"
---

# Sistematik Hata Çözme

## TOKEN KURALI
Dosyanın tamamını okuma. Hata mesajını al → ilgili satıra git → çöz.

---

## Hata Tipi → Çözüm Haritası

### SyntaxError
```
node --check dosya.js → satır numarasına git → parantez/virgül/tırnak bak
Yaygın: eksik }, eksik ), template literal kapanmamış
```

### ReferenceError: X is not defined
```
1. X nerede tanımlanmalı? (global mi, local mi?)
2. Tanım kullanımdan önce mi geliyor?
3. Yazım hatası var mı? (büyük/küçük harf)
```

### TypeError: Cannot read properties of undefined
```
1. Zincirleme erişim: a.b.c → a var mı? b var mı?
2. Async: await eksik mi?
3. DOM: element henüz yüklenmedi mi? → DOMContentLoaded içine al
```

### Three.js Özel
```
"Cannot read property 'geometry' of undefined"
→ Mesh sahneden kaldırıldı veya dispose edildi

"WebGL context lost"
→ Bellek doldu → geometry/material dispose etmeyi unutmuşsun

Sahne boş görünüyor
→ Kamera pozisyonu yanlış, ışık eksik, veya render döngüsü başlamadı
```

---

## Çözüm Adımları (Sırayla)

```
1. Hata mesajını oku — dosya + satır numarası al
2. O satıra git — çevresini oku (±10 satır)
3. Değişken izini geri al — nereden geliyor?
4. En basit düzeltmeyi uygula
5. node --check ile sözdizimi doğrula
6. Tarayıcı konsolunda tekrar test et
```

---

## Versiyon Geçişi Hata Kalıpları

```
Yeni fonksiyon eski ismi çakıştırıyor
→ Ctrl+F ile ismi tüm dosyada ara — çift tanım var mı?

Silinen özellik hâlâ çağrılıyor
→ Hata mesajındaki fonksiyon adını ara — kim çağırıyor?

Global değişken yanlış sıfırlanıyor
→ yeniOyun() veya resetle() fonksiyonlarını kontrol et
```

---

## Hızlı Tanı Araçları

```js
// Hangi satırda patlıyor?
console.trace('kontrol noktası');

// Nesne içeriği nedir?
console.log(JSON.stringify(nesne, null, 2));

// Three.js sahne durumu
console.log('Sahne nesneleri:', sahne.children.length);
console.log('Renderer bilgisi:', renderer.info);
```


