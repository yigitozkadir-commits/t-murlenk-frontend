---
name: game-ai-engine
description: |
  Gök Umay oyunları için CSP uyumlu inline AI motor mimarisi.
  Blob URL olmadan Web Worker benzeri davranış.
  Kullan: "game-ai-engine ile AI motorunu entegre et"
---

# Oyun AI Motor Mimarisi

## TOKEN KURALI
Tam motor kodunu yazma — mimari şablonu ver, oyuna özel kısımları işaretle.

---

## Temel Mimari: Inline Motor + fakeSelf

Blob URL CSP tarafından bloklanır → `new Function` + mesaj yolu kullan.

```js
const AI_MOTOR_KODU = `
  const self = {
    postMessage: function(veri) { self._geriCagir(veri); },
    _geriCagir: null
  };

  // OYUNA ÖZEL — her oyun kendi sürümünü yazar:
  function degerlendir(tahta, renk) { return 0; }
  function gecerliHamleler(tahta, renk) { return []; }
  function hamleUygula(tahta, hamle) { return tahta; }

  // Minimax — değiştirme, tüm oyunlar paylaşır
  function minimaks(tahta, derinlik, maks, alfa, beta) {
    if (derinlik === 0) return degerlendir(tahta, maks ? 'b' : 's');
    const hamleler = gecerliHamleler(tahta, maks ? 'b' : 's');
    if (!hamleler.length) return degerlendir(tahta, maks ? 'b' : 's');

    if (maks) {
      let en = -Infinity;
      for (const h of hamleler) {
        en = Math.max(en, minimaks(hamleUygula(tahta,h), derinlik-1, false, alfa, beta));
        alfa = Math.max(alfa, en);
        if (beta <= alfa) break;
      }
      return en;
    } else {
      let en = Infinity;
      for (const h of hamleler) {
        en = Math.min(en, minimaks(hamleUygula(tahta,h), derinlik-1, true, alfa, beta));
        beta = Math.min(beta, en);
        if (beta <= alfa) break;
      }
      return en;
    }
  }

  self.onmessage = function(e) {
    const { tahta, renk, derinlik } = e.data;
    const hamleler = gecerliHamleler(tahta, renk);
    let enIyiHamle = null, enIyiPuan = -Infinity;
    for (const h of hamleler) {
      const puan = minimaks(hamleUygula(tahta,h), derinlik-1, false, -Infinity, Infinity);
      if (puan > enIyiPuan) { enIyiPuan = puan; enIyiHamle = h; }
    }
    self.postMessage({ hamle: enIyiHamle });
  };
`;

// Ana iş parçacığı bağlayıcısı
function aiHamleIste(tahta, renk, derinlik, geriCagir) {
  const fn = new Function(AI_MOTOR_KODU + '\n return self;');
  const motorSelf = fn();
  motorSelf._geriCagir = res => geriCagir(res.hamle);
  motorSelf.onmessage({ data: { tahta, renk, derinlik } });
}
```

---

## Zorluk Seviyeleri

```js
const ZORLUK = {
  kolay:  { derinlik: 1, rastgele: 0.3 },
  orta:   { derinlik: 2, rastgele: 0.0 },
  zor:    { derinlik: 3, rastgele: 0.0 },
  uzman:  { derinlik: 4, rastgele: 0.0 }
};
```

---

## Performans Referansı

```
Derinlik 1 → <10ms   — her cihaz
Derinlik 2 → <50ms   — her cihaz
Derinlik 3 → <500ms  — masaüstü rahat, mobil sınırda
Derinlik 4 → ~2000ms — masaüstü kabul edilebilir

Kural: Mobil için max derinlik 3.
Timurlenk (11×10): Büyük tahta → alpha-beta budama kritik.
```


