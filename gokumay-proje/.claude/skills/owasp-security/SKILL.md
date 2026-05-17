---
name: owasp-security
description: |
  OWASP Top 10 güvenlik kontrolü — HTML5 oyunlar ve web
  uygulamaları için. XSS, CSRF, veri sızıntısı önleme.
  Kullan: "owasp-security ile kodu tara"
---

# OWASP Güvenlik Denetimi

## TOKEN KURALI
Tüm açıkları listele değil — sadece kodda bulunanları raporla.

---

## Gök Umay Projeleri İçin Kritik Kontroller

### A03 — XSS (En yaygın HTML5 riski)
```js
// YANLIŞ
element.innerHTML = kullanicıGirdisi;

// DOĞRU
element.textContent = kullanicıGirdisi;
// veya
element.innerHTML = DOMPurify.sanitize(kullanicıGirdisi);
```

### A02 — Kriptografik Başarısızlık
```js
// YANLIŞ — localStorage düz metin
localStorage.setItem('token', apiAnahtari);

// DOĞRU — hassas veri istemcide saklanmaz
// Sadece oturum kimliği sakla, anahtarı sunucuda tut
```

### A05 — Güvenlik Yanlış Yapılandırması
```html
<!-- CDN güvenliği — SRI hash zorunlu -->
<script src="https://cdn.jsdelivr.net/npm/three@0.x/build/three.min.js"
        integrity="sha384-HASH_BURAYA"
        crossorigin="anonymous"></script>

<!-- CSP header veya meta -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net;">
```

### A01 — Kırık Erişim Kontrolü
```js
// Oyun skorunu sadece istemcide tutma
// Sunucu taraflı doğrulama olmadan liderlik tablosu manipüle edilebilir
```

---

## Hızlı Tarama Komutu (Termux)

```bash
# API anahtarı sızdı mı?
grep -r "sk-\|api_key\|apiKey\|SECRET" --include="*.js" --include="*.html" .

# eval() kullanımı
grep -rn "eval(" --include="*.js" --include="*.html" .

# innerHTML tehlikeli kullanım
grep -n "innerHTML\s*=" *.html *.js 2>/dev/null
```

---

## Capacitor / Mobil Ek Kontroller

```json
// AndroidManifest.xml — gereksiz izin var mı?
// Sadece gerçekten kullanılanlar olmalı:
<uses-permission android:name="android.permission.INTERNET"/>
// KAMERA, KONUM, REHBER → oyun gerektirmiyorsa kaldır
```

---

## Çıktı Formatı

```
## Güvenlik Tarama Sonucu — [dosya]

Kritik: [N] | Yüksek: [N] | Orta: [N] | Düşük: [N]

### Kritik
- Satır [X]: [açıklama] → [düzeltme]

### Yüksek
- ...

Yayın Onayı: ✅ / ❌
```


