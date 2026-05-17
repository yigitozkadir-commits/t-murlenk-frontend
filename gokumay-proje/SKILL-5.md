---
name: minimax-ai
description: |
  Sadece değerlendirme fonksiyonu tasarımı ve oyuna özel ağırlıklar.
  Motor mimarisi için: game-ai-engine skill'ini kullan.
  Kullan: "minimax-ai ile değerlendirme fonksiyonunu güçlendir"
---

# Minimax Değerlendirme Fonksiyonu

## TOKEN KURALI
Motor kodunu buraya yazma — game-ai-engine'de var.
Sadece değerlendirme + ağırlık + optimizasyon.

---

## Değerlendirme Fonksiyonu Yapısı

```js
function degerlendir(tahta, renk) {
  // Pozitif = beyaz için iyi, negatif = siyah için iyi
  return (
    materialPuani(tahta)      * AGIRLIK.materyal    +
    konumPuani(tahta)         * AGIRLIK.konum       +
    hareketlilikPuani(tahta)  * AGIRLIK.hareketlilik +
    oyunOzelPuani(tahta)      * AGIRLIK.ozelKural
  );
}
```

---

## Oyuna Özel Ağırlık Tabloları

### Timurlenk (11×10)

```js
const AGIRLIK = {
  materyal: 100,
  konum: 10,
  hareketlilik: 5,
  ozelKural: 20   // Tuğrul bonusu
};

// Taş değerleri
const TAS_DEGERI = {
  Piyon: 1,
  At: 3,
  Fil: 3,
  Kale: 5,
  Vezir: 9,
  Deve: 7,      // Timurlenk'e özel — At'tan güçlü
  Zurafa: 8,    // Timurlenk'e özel — uzun L hareketi
  Sah: 1000
};
```

### Hiashatar (10×10)

```js
const AGIRLIK = {
  materyal: 100,
  konum: 20,         // Savunma odaklı — konum ağırlığı yüksek
  hareketlilik: 8,
  ozelKural: 30      // Hia (kalkan) koruması
};

// Hia mekaniği değerlendirmesi
function hiaPuani(tahta) {
  let puan = 0;
  for (const tas of tahta.taslari) {
    if (tas.hiaKorumasında) puan += 15; // korunan taş bonusu
    if (tas.tip === 'Hia') puan += 5;   // Hia varlığı bonusu
  }
  return puan;
}
```

### Togyzool (Tuvan Mancala)

```js
// Minimax yerine — Monte Carlo Tree Search önerilir
// Ama minimax kullanılacaksa:
const AGIRLIK = {
  tası: 10,          // toplam taş sayısı farkı
  tuzdk: 50,         // Tuzdık oluşturma = büyük avantaj
  dag: 5,            // dağılım dengesi
  bos: -20           // boş çukur cezası
};

function togyzoolDegerlendir(tahta) {
  return (
    (tahta.oyuncuTasları - tahta.rakipTasları) * AGIRLIK.tası +
    tahta.tuzdikVar ? AGIRLIK.tuzdk : 0 +
    dagitimPuani(tahta) * AGIRLIK.dag
  );
}
```

### Kurt & Koyun (Asimetrik)

```js
// İki taraf farklı değerlendirilir
function asimetrikDegerlendir(tahta, taraf) {
  if (taraf === 'kurt') {
    return koyunYenildi(tahta) * 100 +    // yenilen koyun sayısı
           kurtKonum(tahta) * 10;          // merkeze yakınlık
  } else {
    return koyunEngeli(tahta) * 50 +      // kurdu köşeye sıkıştır
           koyunSayisi(tahta) * 5;        // hayatta kalan koyun
  }
}
```

---

## Alpha-Beta Performans Optimizasyonu

### Hamle Sıralama (En Önemli Optimizasyon)

```js
// İyi hamleler önce → daha fazla budama
function hamleSirala(hamleler, tahta) {
  return hamleler.sort((a, b) => {
    const puanA = hizliDegerlendir(hamleUygula(tahta, a));
    const puanB = hizliDegerlendir(hamleUygula(tahta, b));
    return puanB - puanA; // yüksekten düşüğe
  });
}

// hizliDegerlendir → sadece materyal, konum atla
function hizliDegerlendir(tahta) {
  return materialPuani(tahta); // tek faktör, hızlı
}
```

### Transpozisyon Tablosu

```js
const transpozisyon = new Map();

function minimaksCache(tahta, derinlik, maks, a, b) {
  const anahtar = `${tahta.toString()}_${derinlik}_${maks}`;
  if (transpozisyon.has(anahtar)) return transpozisyon.get(anahtar);

  const sonuc = minimaks(tahta, derinlik, maks, a, b);
  transpozisyon.set(anahtar, sonuc);

  // Bellek kontrolü — 10000 kayıttan fazla tutma
  if (transpozisyon.size > 10000) transpozisyon.clear();
  return sonuc;
}
```

---

## Derinlik vs Süre Referans Tablosu

```
           | Timurlenk | Hiashatar | Togyzool
-----------+-----------+-----------+---------
Derinlik 1 | <5ms      | <5ms      | <5ms
Derinlik 2 | <30ms     | <20ms     | <15ms
Derinlik 3 | <300ms    | <150ms    | <100ms
Derinlik 4 | ~1500ms   | ~800ms    | ~400ms

Mobil sınırı: Derinlik 3 max
```

---

## Çıktı

```
## Değerlendirme Raporu — [oyun]

### Ağırlık Tablosu
| Faktör | Ağırlık | Gerekçe |
|--------|---------|---------|

### Güçlü Yönler
- [AI'nın iyi yaptığı]

### Zayıf Yönler
- [Kolayca kazanılabilen durum]

### Önerilen Değişiklik
[Tek faktör — tek değişiklik]
```


