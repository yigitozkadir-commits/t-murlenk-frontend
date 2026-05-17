---
name: seo-geo
description: |
  Oyun ve uygulama sayfaları için SEO optimizasyonu.
  AI arama motorlarında görünürlük (GEO).
  Kullan: "seo-geo ile bu sayfayı optimize et"
---

# SEO & GEO Optimizasyonu

## TOKEN KURALI
Genel SEO dersi değil — sayfaya özel meta etiketleri ve içerik yaz.

---

## HTML5 Oyun Sayfası SEO Şablonu

```html
<head>
  <!-- Temel -->
  <title>Timurlenk Satranç Varyantı | Gök Umay Stüdyo</title>
  <meta name="description"
        content="Timurlu dönemine dayanan 11×10 satranç varyantı.
                 Tarayıcıda oyna, kurulum gerekmez.">

  <!-- Open Graph (sosyal paylaşım) -->
  <meta property="og:title" content="Timurlenk Satranç Varyantı">
  <meta property="og:description" content="Tarihi Türkî satranç varyantı — ücretsiz oyna.">
  <meta property="og:image" content="https://gokumay.com/timurlenk-preview.png">
  <meta property="og:type" content="website">

  <!-- Twitter/X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Timurlenk Satranç Varyantı">

  <!-- Canonical -->
  <link rel="canonical" href="https://gokumay.com/timurlenk">

  <!-- Dil -->
  <meta property="og:locale" content="tr_TR">
  <meta property="og:locale:alternate" content="en_US">
</head>
```

---

## Schema.org — Oyun İçin

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoGame",
  "name": "Timurlenk Satranç Varyantı",
  "description": "11×10 tahtalı Timurlu dönemi satranç varyantı",
  "genre": "Strategy",
  "gamePlatform": "Web Browser",
  "applicationCategory": "Game",
  "author": {
    "@type": "Organization",
    "name": "Gök Umay Stüdyo"
  },
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

---

## GEO — AI Arama Motorları İçin

AI arama motorları (ChatGPT, Claude, Perplexity) içeriği farklı işler:

```
Ne önemli:
✓ Açık, sade dil — "Timurlenk satranç varyantı nedir" sorusuna
  doğrudan cevap ver
✓ Özgün içerik — Wikipedia'yı kopyalama, kaynak ol
✓ Yapılandırılmış bilgi — SSS bölümü ekle

SSS Örneği:
Q: Timurlenk satranç varyantı normal satranç'tan farkı nedir?
A: 11×10 tahta ve Deve + Zurafa taşları eklenmiştir.
   Timurlu sarayında 14-15. yüzyılda oynandığı bilinmektedir.
```

---

## itch.io Sayfa SEO'su

```
Başlık: [Oyun Adı] — [Tek Satır Açıklama]
Örnek: "Timurlenk — Tarihi Türkî Satranç Varyantı"

Etiketler (itch.io tag'leri):
chess, strategy, historical, turkish, board-game,
free, browser, no-download

Açıklama ilk cümlesi:
"Timurlu döneminden uyarlanmış 11×10 satranç varyantı.
 Kayıt veya kurulum gerekmez."
```

---

## Anahtar Kelime Grupları

```
Türkçe:
satranç varyantı, Türk satranç, tarihi satranç,
Orta Asya oyunları, strateji oyunu

İngilizce:
chess variant, Tamerlane chess, historical chess,
Central Asian board game, free chess variant browser
```


