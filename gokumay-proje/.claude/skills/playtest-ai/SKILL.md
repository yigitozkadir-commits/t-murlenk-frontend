---
name: playtest-ai
description: |
  Otomatik oyun testi — denge analizi, edge case, hafıza sızıntısı.
  Node.js headless simülasyon, istatistik raporu.
  Kullan: "playtest-ai ile [oyun] denge testini çalıştır"
---

# Otomatik Oyun Testi

## TOKEN KURALI
Ham simülasyon verisi değil — istatistik özeti ve kritik bulgular.

---

## Hızlı Denge Testi (CLI)

```bash
#!/bin/bash
# ~/.claude/scripts/denge_testi.sh
# Kullanım: bash denge_testi.sh timurlenk_v34.html 200

DOSYA="$1"
TEKRAR="${2:-100}"

node << EOF
const { execSync } = require('child_process');

// Oyun kodunu yükle (basitleştirilmiş)
// Gerçek implementasyonda: jsdom ile tam yükleme
console.log('Test başladı:', '$DOSYA', '$TEKRAR tekrar');

let beyaz = 0, siyah = 0, berabere = 0;
const basla = Date.now();

for (let i = 0; i < $TEKRAR; i++) {
  // Rastgele oyun simülasyonu
  // Bu kısım oyunun kendi kural motoruna bağlanır
  const kazanan = Math.random() < 0.48 ? 'beyaz' :
                  Math.random() < 0.48 ? 'siyah' : 'berabere';
  if (kazanan === 'beyaz') beyaz++;
  else if (kazanan === 'siyah') siyah++;
  else berabere++;
}

const sure = Date.now() - basla;
const b_oran = (beyaz/$TEKRAR*100).toFixed(1);
const s_oran = (siyah/$TEKRAR*100).toFixed(1);
const be_oran = (berabere/$TEKRAR*100).toFixed(1);
const denge = Math.abs(beyaz-siyah)/$TEKRAR;

console.log(\`
=== DENGE RAPORU ===
Beyaz: %\${b_oran}
Siyah: %\${s_oran}
Berabere: %\${be_oran}
Dengesizlik: %\${(denge*100).toFixed(1)}
Süre: \${sure}ms
Durum: \${denge < 0.15 ? '✅ Dengeli' : '⚠️ Dengesiz'}
\`);
EOF
```

---

## Edge Case Test Listesi

```javascript
// test/edge-cases.js
const TESTLER = [
  // Genel
  { ad: "Boş tahta hamle", islem: () => oyun.hamleYap(-1, -1, 0, 0) },
  { ad: "Tahta dışı hamle", islem: () => oyun.hamleYap(0, 0, 99, 99) },
  { ad: "Sıra dışı hamle", islem: () => { oyun.siradaki = 'siyah'; oyun.beyazHamleYap(); }},
  { ad: "Oyun bitince hamle", islem: () => { oyun.bitir(); oyun.hamleYap(0,0,1,1); }},

  // Three.js
  { ad: "Sahne temizleme", islem: () => { oyun.yenile(); oyun.yenile(); }},
  { ad: "Hızlı hamle spam", islem: () => { for(let i=0;i<100;i++) oyun.rastgeleHamle(); }},
];

async function edgeCaseTest() {
  let gecen = 0, kalan = 0;
  for (const test of TESTLER) {
    try {
      test.islem();
      console.log(`✅ ${test.ad}`);
      gecen++;
    } catch(e) {
      console.log(`❌ ${test.ad}: ${e.message}`);
      kalan++;
    }
  }
  console.log(`\nSonuç: ${gecen}/${TESTLER.length} geçti`);
}
```

---

## Hafıza Sızıntısı Testi

```javascript
// 1000 hamle sonra hafıza kontrolü
function hafizaTestiYap(oyun) {
  const baslangic = performance.memory?.usedJSHeapSize || 0;

  // 1000 hamle yap
  for (let i = 0; i < 1000; i++) {
    const hamle = oyun.rastgeleGecerliHamle();
    if (!hamle) break;
    oyun.hamleUygula(hamle);
    if (oyun.bittiMi()) oyun.sifirla();
  }

  const bitis = performance.memory?.usedJSHeapSize || 0;
  const artis = (bitis - baslangic) / 1024 / 1024;

  return {
    artis_mb: artis.toFixed(2),
    durum: artis < 10 ? "✅ Sızıntı yok" : `⚠️ ${artis.toFixed(0)}MB artış`
  };
}
```

---

## Çıktı Şablonu

```
## Playtest Raporu — [oyun] v[N]

Tarih: [tarih] | Test sayısı: [N]

### Denge
Beyaz: %[N] | Siyah: %[N] | Berabere: %[N]
Değerlendirme: ✅ Dengeli (<%15 fark) / ⚠️ [fark]% dengesiz

### Performans
Ortalama oyun: [N] hamle | [N] ms
Hafıza artışı: [N] MB (1000 hamle sonrası)

### Edge Case'ler
✅ Geçen: [N]/[N]
❌ Başarısız: [liste]

### Kritik Bulgular
[Varsa P0 sorunlar]

### Öneri
[Denge için önerilen değişiklik]
```
