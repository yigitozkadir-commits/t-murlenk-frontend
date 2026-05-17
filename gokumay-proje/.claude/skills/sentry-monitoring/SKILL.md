---
name: sentry-monitoring
description: |
  Sentry hata izleme entegrasyonu — HTML5 oyunlar için kurulum,
  özel event tracking, Claude ile otomatik analiz.
  Kullan: "sentry-monitoring ile hata izlemeyi kur"
---

# Sentry Hata İzleme

## TOKEN KURALI
Kurulum kodu + oyuna özel event'lar — ikisi birlikte.

---

## Kurulum (HTML5 Oyun)

```html
<!-- head içine ekle — CDN -->
<script
  src="https://browser.sentry-cdn.com/7.x.x/bundle.min.js"
  crossorigin="anonymous"
></script>

<script>
// Oyun başlamadan önce init et
Sentry.init({
  dsn: "https://[ANAHAR]@o[ORG].ingest.sentry.io/[PROJE]",

  // Versiyon takibi — hangi sürümde hata var?
  release: "timurlenk@v34",
  environment: "production", // veya "development"

  // Performans izleme
  tracesSampleRate: 0.1, // %10 örnekleme — yeterli

  // HTML5 oyun için özel filtreler
  ignoreErrors: [
    // Tarayıcı uzantı hataları — gürültü
    'ResizeObserver loop limit exceeded',
    'Non-Error promise rejection captured',
    // Üçüncü taraf CDN hataları
    /cdn\.jsdelivr\.net/,
  ],

  // Kullanıcı gizliliği
  beforeSend(event) {
    // IP ve kişisel veri gönderme
    if (event.user) delete event.user.ip_address;
    return event;
  }
});

// Oyun versiyonunu tag olarak ekle
Sentry.setTag("oyun", "timurlenk");
Sentry.setTag("platform", "html5-browser");
</script>
```

---

## Oyun İçi Event Tracking

```js
// Oyun başlangıcı
function oyunBaslat(zorluk) {
  Sentry.addBreadcrumb({
    category: 'oyun.akis',
    message: `Yeni oyun başladı — zorluk: ${zorluk}`,
    level: 'info',
    data: { zorluk, zaman: Date.now() }
  });
}

// AI hamle hatası
function aiHamleHatasi(hata, tahta) {
  Sentry.captureException(hata, {
    tags: { kategori: 'ai-motor' },
    extra: {
      tahta_durumu: JSON.stringify(tahta).slice(0, 500),
      hamle_sayisi: tahta.hamleSayisi
    }
  });
}

// Performans ölçümü
function performansOlc() {
  const islem = Sentry.startTransaction({
    name: "AI Hamle Hesaplama",
    op: "ai.minimax"
  });

  const sure = performance.now();
  const hamle = minimaks(tahta, 3, true, -Infinity, Infinity);
  const gecenSure = performance.now() - sure;

  islem.setMeasurement("hesaplama_suresi", gecenSure, "millisecond");
  islem.finish();

  // Yavaş hamle uyarısı
  if (gecenSure > 1000) {
    Sentry.captureMessage(`Yavaş AI hamlesi: ${gecenSure}ms`, 'warning');
  }

  return hamle;
}

// WebGL hatası
window.addEventListener('webglcontextlost', (e) => {
  Sentry.captureMessage('WebGL context kayboldu', {
    level: 'error',
    tags: { hata_turu: 'webgl' },
    extra: {
      tarayici: navigator.userAgent,
      ekran: `${window.innerWidth}x${window.innerHeight}`
    }
  });
});

// Three.js render hatası
try {
  renderer.render(sahne, kamera);
} catch (hata) {
  Sentry.captureException(hata, {
    tags: { kategori: 'three-js-render' },
    extra: {
      sahne_nesneleri: sahne.children.length,
      renderer_bilgi: renderer.info.render
    }
  });
}
```

---

## n8n ile Otomatik Analiz

```
Sentry Alert tetiklenince → n8n webhook
    ↓
n8n: hata bilgisini formatla
    ↓
Claude Code (headless):
  "Bu Sentry hatasını analiz et:
   Hata: [mesaj]
   Stack: [trace]
   Etkilenen: [kullanıcı sayısı]
   systematic-debugger protokolüyle çöz."
    ↓
n8n: Telegram'a analiz gönder
    ↓ (P0 ise)
n8n: GitHub Issue otomatik aç
```

---

## Sentry Dashboard Ayarları

```
Önerilen Alert Kuralları:

1. P0 Tetikleyici (anında)
   Koşul: Hata oranı > %5 (5 dakika)
   Eylem: Telegram + n8n self-healing

2. Yeni Hata (1 saat içinde)
   Koşul: Daha önce görülmemiş hata
   Eylem: Telegram bildirim

3. Performans (günlük)
   Koşul: P95 yükleme süresi > 3 saniye
   Eylem: analytics-reporter'a bildir

4. Haftalık Özet (Pazartesi 09:00)
   Koşul: Cron
   Eylem: Haftalık hata raporu
```

---

## Ücretsiz Plan Limitleri

```
Sentry Ücretsiz:
  Hata: 5.000/ay
  Performans: 10.000 işlem/ay
  Oturum: 50.000/ay

Gök Umay için yeterli mi?
  Erken aşama (< 1000 kullanıcı): ✅ Evet
  Büyüme aşaması: Ücretli plana geç ($26/ay)
```

---

## Çıktı

```
## Sentry Kurulum Raporu — [oyun]

DSN: [kuruldu/kurulmadı]
Versiyon takibi: [aktif/pasif]
Özel event'lar: [N adet]
Alert kuralları: [N adet]

Son 7 gün:
  Hata: [N]
  Etkilenen kullanıcı: [N]
  En sık hata: [mesaj]
```
