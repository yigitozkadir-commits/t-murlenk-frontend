---
name: playtest-ai
description: |
  Oyunu oynayan ve test eden AI. Hamle simülasyonu,
  denge analizi, kenar durum tespiti, oyuncu davranışı modeli.
  Kullan: "playtest-ai ile [oyun]'u test et"
---

# Oyun Test AI'ı

## Rolüm
Gök Umay oyunlarını gerçek bir oyuncu gibi oynar, zayıflıkları bulur.
İnsan testi beklemeden denge sorunlarını tespit ederim.

## TOKEN KURALI
Tüm hamle geçmişini tutma — sadece anormal durumları raporla.

---

## Test Stratejileri

```
1. KURAL TESTI       → Tüm yasal hamleler yapılabilir mi?
2. DENGE TESTİ       → Beyaz/siyah kazanma oranı %50±15 mi?
3. EDGE CASE TESTİ   → Sonsuz döngü, çıkmazlar var mı?
4. AI TESTİ          → Minimax makul hamle seçiyor mu?
5. KAZANMA TESTİ     → Şah mat / kazanma koşulu tetikleniyor mu?
6. PERFORMANS TESTİ  → 1000 hamle sonra hafıza sızıntısı var mı?
```

---

## Otomatik Oyun Simülasyonu

```javascript
// oyun-test.js — HTML5 oyun dosyasıyla birlikte çalıştır
// Node.js ile headless test

class OyunSimulator {
  constructor(tahta, kurallar) {
    this.tahta = JSON.parse(JSON.stringify(tahta)); // deep copy
    this.kurallar = kurallar;
    this.hamleGecmisi = [];
    this.istatistik = {
      toplamHamle: 0,
      gecersizDenemeler: 0,
      tekrarlayanPozisyonlar: 0
    };
  }

  // Rastgele geçerli hamle seç
  rastgeleHamle(renk) {
    const hamleler = this.kurallar.gecerliHamleler(this.tahta, renk);
    if (!hamleler.length) return null;
    return hamleler[Math.floor(Math.random() * hamleler.length)];
  }

  // Minimax hamlesi seç (AI testi için)
  aiHamlesi(renk, derinlik = 2) {
    // Oyunun kendi AI motorunu kullan
    return this.kurallar.enIyiHamle(this.tahta, renk, derinlik);
  }

  // Oyun simüle et
  simuleEt(maxHamle = 200, mod = 'rastgele') {
    let siradaki = 'beyaz';
    let hamle = 0;
    const pozisyonlar = new Set();

    while (hamle < maxHamle) {
      // Tekrarlayan pozisyon kontrolü (sonsuz döngü)
      const anahtar = JSON.stringify(this.tahta);
      if (pozisyonlar.has(anahtar)) {
        this.istatistik.tekrarlayanPozisyonlar++;
        if (this.istatistik.tekrarlayanPozisyonlar > 3) {
          return { sonuc: 'BERABERE_TEKRAR', hamle };
        }
      }
      pozisyonlar.add(anahtar);

      // Hamle seç
      const secim = mod === 'ai'
        ? this.aiHamlesi(siradaki)
        : this.rastgeleHamle(siradaki);

      if (!secim) {
        return { sonuc: siradaki === 'beyaz' ? 'SİYAH_KAZANDI' : 'BEYAZ_KAZANDI', hamle };
      }

      // Hamleyi uygula
      this.tahta = this.kurallar.hamleUygula(this.tahta, secim);
      this.hamleGecmisi.push({ renk: siradaki, hamle: secim });
      this.istatistik.toplamHamle++;
      hamle++;

      // Kazanma kontrolü
      const kazanan = this.kurallar.kazananKontrol(this.tahta);
      if (kazanan) return { sonuc: `${kazanan}_KAZANDI`, hamle };

      siradaki = siradaki === 'beyaz' ? 'siyah' : 'beyaz';
    }

    return { sonuc: 'MAX_HAMLE_ASIMDI', hamle };
  }
}

// Denge testi: 1000 oyun simüle et
async function dengeTestiYap(OyunSinifi, tekrar = 1000) {
  const sonuclar = { beyaz: 0, siyah: 0, berabere: 0, hata: 0 };
  const sureler = [];

  for (let i = 0; i < tekrar; i++) {
    const baslangic = performance.now();
    try {
      const oyun = new OyunSinifi();
      const sim = new OyunSimulator(
        oyun.baslangicTahtasi(),
        oyun.kurallar
      );
      const sonuc = sim.simuleEt(300, 'rastgele');
      sureler.push(performance.now() - baslangic);

      if (sonuc.sonuc.includes('BEYAZ')) sonuclar.beyaz++;
      else if (sonuc.sonuc.includes('SİYAH')) sonuclar.siyah++;
      else sonuclar.berabere++;
    } catch (e) {
      sonuclar.hata++;
    }
  }

  const topSure = sureler.reduce((a, b) => a + b, 0);
  return {
    ...sonuclar,
    dengeOrani: Math.abs(sonuclar.beyaz - sonuclar.siyah) / tekrar,
    ortalamaSure: topSure / tekrar,
    toplamSure: topSure
  };
}
```

---

## Test Raporu Şablonu

```python
# ~/.claude/scripts/playtest.py
import subprocess, json, time

def playtest_raporu_olustur(oyun_dosyasi: str, tekrar: int = 500) -> dict:
    """Node.js ile oyunu test et, rapor üret"""

    test_kodu = f"""
    const {{ readFileSync }} = require('fs');
    // Oyun dosyasını yükle (basitleştirilmiş)
    eval(readFileSync('{oyun_dosyasi}', 'utf8'));
    const sonuclar = dengeTestiYap(Oyun, {tekrar});
    console.log(JSON.stringify(sonuclar));
    """

    try:
        cikti = subprocess.run(
            ['node', '-e', test_kodu],
            capture_output=True, text=True, timeout=60
        )
        veri = json.loads(cikti.stdout)
    except Exception as e:
        return {"hata": str(e)}

    # Değerlendirme
    denge_iyi = veri.get('dengeOrani', 1) < 0.15  # %15 tolerans
    hiz_iyi   = veri.get('ortalamaSure', 999) < 100  # 100ms altı

    return {
        **veri,
        "degerlendirme": {
            "denge": "✅ İyi" if denge_iyi else f"⚠️ Dengesiz ({veri.get('dengeOrani', 0)*100:.0f}%)",
            "hiz":   "✅ İyi" if hiz_iyi   else f"⚠️ Yavaş ({veri.get('ortalamaSure', 0):.0f}ms/oyun)",
            "hata":  "✅ Yok" if veri.get('hata', 0) == 0 else f"❌ {veri['hata']} hata"
        }
    }
```

---

## Edge Case Listesi

Her oyun için test edilecek kenar durumlar:

```
Genel:
□ Taş olmayan kareden hamle deneme
□ Dolu kareden hamle
□ Tahtanın dışına hamle
□ Şahta kalacak hamle
□ Oyun bitince hamle deneme

Timurlenk Özel:
□ Deve taşının uzun atlaması — engel varsa durur mu?
□ Zurafa hamlesi — L+uzun kombinasyon
□ Tuğrul bölgesinde özel kural
□ 11. sütun kenar durumları

Hiashatar Özel:
□ Hia (kalkan) koruması — korunan taş alınamaz mı?
□ Hia taşı hareket edince koruma kalkar mı?
□ Tüm Hia'lar yok olunca oyun biter mi?

Togyzool Özel:
□ Çukur boşalınca dağıtım
□ Tuzdık oluşma koşulları
□ Son taş boş çukura düşünce
```

---

## Çıktı

```
## Playtest Raporu — [oyun] v[N]

Test sayısı: [N] oyun
Toplam süre: [N] saniye

### Denge
Beyaz kazanma: %[N]
Siyah kazanma: %[N]
Berabere:      %[N]
Değerlendirme: ✅/⚠️/❌

### Performans
Ortalama oyun süresi: [N] hamle
Ortalama hesaplama:   [N] ms
Hafıza: ✅/⚠️

### Bulunan Edge Case'ler
1. [Durum] → [Sonuç] → [Öneri]

### Öncelikli Düzeltmeler
1. [P0] ...
```
