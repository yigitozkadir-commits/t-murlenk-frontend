---
name: vibesec
description: |
  Hızlı güvenlik taraması — IDOR, XSS, SQL Injection, SSRF
  açıklarını önler. owasp-security'nin hafif versiyonu.
  Kullan: "vibesec ile kodu hızlıca tara"
---

# Hızlı Güvenlik Tarayıcı

## TOKEN KURALI
Kapsamlı rapor değil — sadece bulunan sorunları listele.

---

## 60 Saniyelik Tarama

Bu 5 pattern'i ara — hepsini bulursan tam tarama gerekmez:

```bash
# 1. API anahtarı sızıntısı
grep -n "api.key\|apiKey\|API_KEY\|sk-\|Bearer " dosya.html

# 2. Tehlikeli innerHTML
grep -n "innerHTML\s*=" dosya.html

# 3. eval() kullanımı
grep -n "eval(" dosya.html

# 4. HTTP (HTTPS değil) istek
grep -n "http://" dosya.html

# 5. console.log'da hassas veri
grep -n "console.log.*password\|console.log.*token\|console.log.*key" dosya.html
```

---

## Yaygın Hızlı Düzeltmeler

### innerHTML → textContent
```js
// Tehlikeli
el.innerHTML = veri;

// Güvenli
el.textContent = veri;

// HTML şart ise
el.innerHTML = veri.replace(/</g, '&lt;').replace(/>/g, '&gt;');
```

### API Anahtarı Koruma
```js
// YANLIŞ — kaynak kodda görünür
const API_KEY = 'sk-abc123';

// DOĞRU — ortam değişkeni (sunucu tarafı)
// İstemci tarafında API anahtarı saklanmaz
// Proxy endpoint kullan
```

### CDN SRI Hash
```html
<!-- Hash ekle — üçüncü taraf CDN için -->
<script src="https://cdn.jsdelivr.net/npm/three@r128/build/three.min.js"
        crossorigin="anonymous"></script>
<!-- integrity="sha384-..." — threejs.org'dan kopyala -->
```

---

## Mobil / Capacitor

```
İzin listesi kontrolü (AndroidManifest.xml):
Sadece bunlar olmalı (oyun için):
  INTERNET — evet
  CAMERA — hayır (gerekmedikçe)
  LOCATION — hayır
  READ_CONTACTS — kesinlikle hayır
```

---

## Çıktı

```
Tarama: [dosya] — [tarih]
Süre: hızlı (~1dk)

Bulunan: [N] sorun
- [Satır X]: [sorun] → [tek satır düzeltme]

Temiz: ✅ / Sorunlu: ⚠️
```


