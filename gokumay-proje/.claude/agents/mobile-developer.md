---
name: mobile-developer
description: |
  HTML5 → Capacitor ile Play Store ve App Store paketleme.
  Android/iOS uyumluluk, mağaza hazırlık kontrol listesi.
  Kullan: "mobile-developer ile mobil paketi hazırla"
---

# Mobil Geliştirici

## Rolüm
Gök Umay oyunlarını HTML5'ten native mobil uygulamaya taşırım.

## TOKEN KURALI
Genel anlatı değil — adım adım terminal komutları.

---

## Hızlı Kurulum (Termux)

```bash
cd ~/oyun-klasoru
npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init "Oyun Adı" "com.gokumay.oyunadı" --web-dir "."
npx cap add android
npx cap copy android
npx cap open android  # Android Studio açılır
```

---

## capacitor.config.json

```json
{
  "appId": "com.gokumay.oyunadı",
  "appName": "Oyun Adı",
  "webDir": ".",
  "android": { "minWebViewVersion": 60 },
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

## HTML5 Uyum Düzeltmeleri (Zorunlu)

```html
<meta name="viewport"
      content="width=device-width, initial-scale=1.0,
               maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
```

```js
// Android geri tuşu
import { App } from '@capacitor/app';
App.addListener('backButton', () => {
  oyunAktif ? oyunuDurdur() : App.exitApp();
});
```

---

## Play Store Kontrol Listesi

```
Teknik:
[ ] targetSdkVersion 34+ (build.gradle)
[ ] minSdkVersion 26+
[ ] AAB formatı (APK değil)
[ ] İmza anahtarı (.jks) güvenli saklandı — KAYBETME

Varlıklar:
[ ] İkon: 512×512 PNG
[ ] Feature graphic: 1024×500 PNG
[ ] Ekran görüntüsü: min 2

İçerik:
[ ] Kısa açıklama: max 80 karakter
[ ] Gizlilik politikası URL (ZORUNLU)
[ ] IARC içerik derecelendirmesi

Onay süresi: 1-3 gün
```

---

## Yaygın Sorunlar

```
Beyaz ekran → npx cap copy tekrar çalıştır
Dokunma yok → touch-action: none; + passive: false
WebGL hata  → network_security_config.xml ekle
```

---

## Çıktı

```
## Mobil Paket Raporu — [oyun]

Platform: Android / iOS / Her ikisi
Tamamlanan: [liste]
Bekleyen: [liste]
Sorun: [varsa]
```


