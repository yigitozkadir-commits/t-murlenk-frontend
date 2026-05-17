---
description: Güvenlik taraması — HTML5 oyun ve web uygulamaları için.
tools: [read, bash]
---

$ARGUMENTS için güvenlik taraması yap.

HIZLI TARAMA:
```bash
# API key sızıntısı
grep -n "api.key\|apiKey\|sk-\|SECRET\|Bearer" $ARGUMENTS

# XSS riski
grep -n "innerHTML\s*=" $ARGUMENTS

# eval() kullanımı (AI motoru için new Function OK)
grep -n "eval(" $ARGUMENTS | grep -v "new Function"

# HTTP (HTTPS olmalı)
grep -n "http://" $ARGUMENTS

# localStorage hassas veri
grep -n "localStorage.*token\|localStorage.*key" $ARGUMENTS
```

OWASP TOP 10 (HTML5 oyun için geçerli):
- [ ] A03 XSS: kullanıcı girdisi innerHTML'e gitmiyor
- [ ] A02 Veri: API key kaynak kodda değil
- [ ] A05 CSP: meta etiketi var mı?
- [ ] A06 Bağımlılık: CDN HTTPS, SRI hash var mı?

CSP KONTROLÜ:
```bash
grep -n "Content-Security-Policy" $ARGUMENTS
```

Capacitor ise:
```bash
grep -n "INTERNET\|CAMERA\|LOCATION" android/app/src/main/AndroidManifest.xml 2>/dev/null
```

ÇIKTI:
```
Kritik:_ Yüksek:_ Orta:_

### Kritik (yayın öncesi düzelt)
- Satır [X]: [açık] → [düzeltme]

Yayın Onayı: ✅ / ❌
```


