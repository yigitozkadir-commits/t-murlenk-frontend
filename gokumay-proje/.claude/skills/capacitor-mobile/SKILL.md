---
name: capacitor-mobile
description: |
  HTML5 oyunu Capacitor ile Android/iOS uygulamasına paketler.
  Play Store ve App Store hazırlık adımları.
  Kullan: "capacitor-mobile ile mobil paketi oluştur"
---

# Capacitor Mobil Paketleme

## TOKEN KURALI
Genel Capacitor anlatısı değil — adım adım terminal komutları ver.

---

## Kurulum (Termux veya Terminal)

```bash
# Node.js gerekli
node --version  # 18+ olmalı

# Proje klasörüne gir
cd ~/oyun-klasoru

# Capacitor kur
npm init -y
npm install @capacitor/core @capacitor/cli
npm install @capacitor/android
# iOS için: npm install @capacitor/ios (Mac gerekli)

# Başlat
npx cap init "Oyun Adı" "com.gokumay.oyunadı" --web-dir "."
```

---

## capacitor.config.json

```json
{
  "appId": "com.gokumay.oyunadı",
  "appName": "Oyun Adı",
  "webDir": ".",
  "android": {
    "minWebViewVersion": 60
  },
  "plugins": {
    "SplashScreen": {
      "launchShowDuration": 1500,
      "backgroundColor": "#1a1208",
      "showSpinner": false
    }
  }
}
```

---

## Android Build Adımları

```bash
# Android platformunu ekle
npx cap add android

# Web dosyalarını kopyala
npx cap copy android

# Android Studio'yu aç
npx cap open android

# Android Studio'da:
# Build → Generate Signed Bundle/APK
# → Android App Bundle (AAB) seç — Play Store zorunluluğu
# → Keystore oluştur ve SAKLA (kaybetme!)
```

---

## HTML5 Oyun Uyumluluk Düzeltmeleri

```html
<!-- head'e ekle — zorunlu -->
<meta name="viewport"
      content="width=device-width, initial-scale=1.0,
               maximum-scale=1.0, user-scalable=no,
               viewport-fit=cover">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
```

```js
// Geri tuşu (Android)
import { App } from '@capacitor/app';
App.addListener('backButton', () => {
  if (oyunAktif) { oyunuDurdur(); }
  else { App.exitApp(); }
});

// Güvenli alan (notch/çentik)
const style = document.documentElement.style;
style.setProperty('--sat', 'env(safe-area-inset-top)');
style.setProperty('--sab', 'env(safe-area-inset-bottom)');
```

---

## Play Store Kontrol Listesi

```
Teknik:
[ ] targetSdkVersion 34+ (android/app/build.gradle)
[ ] minSdkVersion 26+ (Android 8.0)
[ ] AAB formatı (APK değil)
[ ] İmza anahtarı (.jks) güvenli yerde saklandı

Varlıklar:
[ ] İkon: 512×512 PNG (arka plan şeffaf)
[ ] Feature graphic: 1024×500 PNG
[ ] Ekran görüntüsü: min 2 adet (telefon boyutu)

İçerik:
[ ] Kısa açıklama: max 80 karakter
[ ] Tam açıklama: max 4000 karakter
[ ] Gizlilik politikası URL (ZORUNLU)
[ ] İçerik derecelendirmesi: IARC anketi
```

---

## Yaygın Sorunlar

```
WebGL çalışmıyor
→ android/app/src/main/res/xml/network_security_config.xml ekle

Dokunma çalışmıyor
→ renderer.domElement üzerinde touch-action: none; ekle
→ addEventListener'da passive: false kullan

Uygulama beyaz ekranda kalıyor
→ webDir yolunu kontrol et
→ npx cap copy tekrar çalıştır
```


