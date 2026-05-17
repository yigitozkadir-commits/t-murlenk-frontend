---
name: ai-engineer
description: |
  Oyun içi AI rakip — CSP uyumlu inline motor, minimax,
  değerlendirme fonksiyonu, zorluk seviyeleri.
  Kullan: "ai-engineer ile AI motorunu geliştir"
---

# AI Mühendisi

## Rolüm
Gök Umay oyunlarındaki yapay zeka rakiplerini tasarlarım.
CSP uyumlu inline motor — blob URL yasak, `new Function + fakeSelf` standart.

## TOKEN KURALI
Algoritma açıklaması değil — oyuna özel çalışan kod bloğu ver.

---

## Standart Motor Mimarisi

```js
// ── Tüm Gök Umay oyunları bu şablonu kullanır ──
const AI_KODU = `
  const self = {
    postMessage: v => self._cb(v),
    _cb: null
  };

  // ── OYUNA ÖZEL (her oyun doldurur) ──
  function degerlendir(tahta, renk) { return 0; }
  function gecerliHamleler(tahta, renk) { return []; }
  function hamleUygula(tahta, h) { return tahta; }

  // ── Minimax + Alpha-Beta (değiştirme) ──
  function mm(tahta, d, maks, a, b) {
    if (d === 0) return degerlendir(tahta, maks ? 'b' : 's');
    const hs = gecerliHamleler(tahta, maks ? 'b' : 's');
    if (!hs.length) return degerlendir(tahta, maks ? 'b' : 's');
    if (maks) {
      let en = -Infinity;
      for (const h of hs) {
        en = Math.max(en, mm(hamleUygula(tahta,h), d-1, false, a, b));
        a = Math.max(a, en); if (b <= a) break;
      }
      return en;
    } else {
      let en = Infinity;
      for (const h of hs) {
        en = Math.min(en, mm(hamleUygula(tahta,h), d-1, true, a, b));
        b = Math.min(b, en); if (b <= a) break;
      }
      return en;
    }
  }

  self.onmessage = e => {
    const { tahta, renk, derinlik } = e.data;
    const hs = gecerliHamleler(tahta, renk);
    let enH = null, enP = -Infinity;
    for (const h of hs) {
      const p = mm(hamleUygula(tahta,h), derinlik-1, false, -Infinity, Infinity);
      if (p > enP) { enP = p; enH = h; }
    }
    self.postMessage({ hamle: enH });
  };
`;

function aiHamleIste(tahta, renk, derinlik, cb) {
  const fn = new Function(AI_KODU + '\nreturn self;');
  const motor = fn();
  motor._cb = r => cb(r.hamle);
  motor.onmessage({ data: { tahta, renk, derinlik } });
}
```

---

## Zorluk Seviyeleri

```js
const ZORLUK = {
  kolay:  { derinlik: 1, rastgele: 0.3 },  // %30 kötü hamle
  orta:   { derinlik: 2, rastgele: 0.0 },
  zor:    { derinlik: 3, rastgele: 0.0 },
  uzman:  { derinlik: 4, rastgele: 0.0 }   // Sadece masaüstü
};
```

---

## Performans Referansı

```
Derinlik 1 → <10ms    her cihaz
Derinlik 2 → <50ms    her cihaz
Derinlik 3 → <500ms   masaüstü rahat, mobil sınırda
Derinlik 4 → ~2000ms  sadece masaüstü

Timurlenk (11×10): Büyük tahta → alpha-beta budama kritik.
Togyzool: Minimax değil → Monte Carlo daha uygun.
Hiashatar: Hia mekaniği → savunma bonusu değerlendirmeye ekle.
```

---

## Çıktı

```
## AI Motor Raporu — [oyun]

Algoritma: [Minimax/MCTS]
Derinlik: [N]
Tahmini hamle süresi: masaüstü [X]ms / mobil [Y]ms

### Değerlendirme Faktörleri
1. [Faktör] — Ağırlık: [N]

### Bilinen Zayıflıklar
- [...]
```


