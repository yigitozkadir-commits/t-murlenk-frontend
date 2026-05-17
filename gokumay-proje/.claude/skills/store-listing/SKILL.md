---
name: store-listing
description: |
  Play Store, App Store, itch.io mağaza listing optimizasyonu.
  ASO (App Store Optimization) ve içerik şablonları.
  Kullan: "store-listing ile [oyun] için listing hazırla"
---

# Mağaza Listing Optimizasyonu

## TOKEN KURALI
Şablon değil — oyuna özel, platforma özel, hazır metin üret.

---

## ASO Temel Prensipler

```
Arama algoritması faktörleri (öncelik sırasıyla):
1. Uygulama adı (en yüksek ağırlık)
2. Kısa açıklama (Play Store)
3. Anahtar kelimeler (App Store — gizli alan)
4. Tam açıklama (düşük ağırlık ama dönüşüm için kritik)
5. Görsel varlıklar (dönüşüm oranı)
6. Derecelendirme ve yorum sayısı
```

---

## Play Store Listing Şablonu

```
━━━ UYGULAMA ADI (max 30 karakter) ━━━
[Oyun Adı]: [Alt başlık]
Örnek: "Timurlenk: Tarihi Satranç"

━━━ KISA AÇIKLAMA (max 80 karakter) ━━━
[Anahtar özellik] + [Fayda] + [Çağrı]
Örnek: "14. yy Timurlu satrancı. Ücretsiz, kurulum yok."

━━━ TAM AÇIKLAMA (max 4000 karakter) ━━━

[BAŞLIK — Büyük harf] (arama için)
TARİHİ TÜRK SATRANÇ VARYANTİ

[Kanca — 2 cümle]
Timurlenk Satranç, 14. yüzyıl Timurlu sarayında oynanan
tarihi bir satranç varyantıdır. 600 yılı aşkın bu oyunu
şimdi tarayıcında veya telefonunda oynayabilirsin.

[Özellikler — bullets]
★ TAM ÖZELLİKLER
• 11×10 tahta — genişletilmiş strateji alanı
• Tarihi taşlar: Deve, Zurafa ve daha fazlası
• 3D görselleştirme
• AI rakip — 4 zorluk seviyesi
• Offline çalışır — internet bağlantısı gerekmez
• Ücretsiz — reklam yok, satın alma yok

[Tarihi Bağlam]
TARİHİ ARKA PLAN
[2-3 cümle — Murray/Bell kaynağına referans]

[Teknik]
TEKNİK BİLGİ
HTML5 tabanlı, WebGL destekli cihazlarda çalışır.

[SEO — tekrar eden anahtar kelimeler]
Anahtar: satranç, chess variant, strateji oyunu,
tarihi oyun, offline satranç

━━━ ANAHTAR KELİMELER (App Store — 100 karakter) ━━━
chess,strategy,historical,turkish,medieval,board game,
offline,free,variant,3d
(virgülle, boşluksuz, max 100 karakter)
```

---

## itch.io Listing Şablonu

```markdown
# [Oyun Adı]

> [Tek cümle kanca — italik]

---

## Ne Bu Oyun?

[Paragraf 1: Tarihi bağlam — kaynaklı]
[Paragraf 2: Oyun özellikleri]

## Nasıl Oynanır?

[3-4 temel kural — kısa]

## Özellikler

- ✅ Tarayıcıda çalışır — kurulum yok
- ✅ Ücretsiz — her zaman
- ✅ 3D tahta görselleştirme
- ✅ AI rakip (4 seviye)
- ✅ Mobil uyumlu

## Tarihi Not

[Kısa şeffaf not: Ne belgelenmiş, ne rekonstrüksiyon]

## Geliştirici

Gök Umay Stüdyo — Türkî ve Orta Asya tarihi oyunları

---

**Etiketler:** chess, strategy, historical, turkish, browser,
free, board-game, 3d, [oyuna özel]
```

---

## Görsel Varlık Spesifikasyonları

```
Play Store:
  İkon:           512×512 PNG (transparan arka plan OK)
  Feature Graphic: 1024×500 PNG (metin yok — Play Store ekler)
  Ekran görüntüsü: min 2, max 8
    Telefon: 1080×1920 veya 1080×2340
    Tablet:  1200×1920 (opsiyonel)

App Store:
  İkon:           1024×1024 PNG (köşe yuvarlama App Store yapar)
  Ekran görüntüsü: min 3
    iPhone 6.9": 1320×2868 veya 1290×2796
    iPad Pro:    2064×2752 (opsiyonel)

itch.io:
  Kapak:          630×500 PNG (zorunlu)
  Ekran görüntüsü: min 1, max 10
  Gif: opsiyonel ama dönüşüm artırır
```

---

## ASO Anahtar Kelime Araştırması

```python
# Gök Umay için onaylı kelime grupları

YUKSEK_HACIM = [
    "chess", "strategy game", "board game",
    "free chess", "offline chess", "chess game"
]

NIS_YUKSEK_DONUSUM = [
    "chess variant", "historical chess",
    "tamerlane chess", "medieval chess",
    "turkish chess", "3d chess"
]

UZUN_KUYRUK = [
    "free chess variant no download",
    "historical strategy board game",
    "timurid era chess game",
    "central asian board game"
]

# Strateji: Yüksek hacim + Niş = En iyi sonuç
# Tam eşleşme > Kısmi eşleşme > Alakalı
```

---

## Dönüşüm Optimizasyonu

```
A/B Test edilebilir unsurlar:
1. İlk ekran görüntüsü (en kritik)
   Seçenek A: Tahta yakın çekim
   Seçenek B: Oyun ortasında hamle anı

2. Kısa açıklama
   Seçenek A: Tarihi odaklı
   Seçenek B: Özellik odaklı

3. İkon rengi
   Seçenek A: Altın/kahverengi (tarihi)
   Seçenek B: Koyu/modern

Ölçüm: 2 hafta × her seçenek → dönüşüm oranı karşılaştır
```

---

## Çıktı

```
## Listing Paketi — [oyun] — [platform]

Durum: Hazır / Eksik var

### Metin
Ad: ✅ [N karakter/30]
Kısa: ✅ [N karakter/80]
Tam: ✅ [N karakter/4000]

### Görsel
İkon: ✅/❌
Feature: ✅/❌
Ekran görüntüsü: [N] adet

ASO skoru tahmini: [1-10]
```
