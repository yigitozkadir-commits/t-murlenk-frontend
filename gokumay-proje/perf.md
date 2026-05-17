---
description: Three.js performans analizi ve FPS optimizasyonu.
tools: [read, edit, bash]
---

$ARGUMENTS dosyasında performans sorunlarını analiz et ve düzelt.

DARBOĞAZ TESPİT:
```bash
# Render döngüsünde nesne oluşturma (en pahalı hata)
grep -n "new THREE\." $ARGUMENTS | grep -v "^[0-9]*:\/\/"

# Her karede DOM sorgusu
grep -n "document\.get\|querySelector" $ARGUMENTS

# dispose çağrısı var mı?
grep -c "dispose()" $ARGUMENTS
```

MALİYET HİYERARŞİSİ:
```
1. render döngüsünde new THREE.X()  → KRİTİK
2. her karede DOM sorgusu            → ÇOK PAHALI
3. gereksiz draw call                → PAHALI
4. texture boyutu >1024 mobilde      → PAHALI
5. shadow map açık mobilde           → ORTA
```

HIZLI FPS ÖLÇÜMÜ EKLE:
```js
// Geçici — production'da sil
let _s = performance.now(), _k = 0;
// animate() içine:
_k++; const n = performance.now();
if (n - _s >= 1000) { console.log('FPS:', _k); _k = 0; _s = n; }
```

STANDART DÜZELTMELEr:
```js
// Kötü
function animate() { const v = new THREE.Vector3(); ... }

// İyi
const _v = new THREE.Vector3();
function animate() { _v.set(x,y,z); ... }

// Mobil piksel oranı
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
```

ÇIKTI:
```
FPS mevcut: [tahmini] → Hedef: 30+
Bulunan sorunlar: [N]
Tahmini kazanç: +[X] FPS
```


