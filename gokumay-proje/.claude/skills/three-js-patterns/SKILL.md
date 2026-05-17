---
name: three-js-patterns
description: |
  Three.js ile 3D oyun geliştirme kalıpları — Gök Umay
  projelerine özel: tahta, taş, ışık, kamera, animasyon.
  Kullan: "three-js-patterns ile sahneyi kur"
---

# Three.js Oyun Geliştirme Kalıpları

## TOKEN KURALI
Genel Three.js anlatısı değil — Gök Umay'a özel, kopyala-çalıştır kod ver.

---

## Temel Sahne Kurulumu (Tek Dosya)

```js
// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // mobil sınırı
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// Sahne + Kamera
const sahne = new THREE.Scene();
sahne.fog = new THREE.Fog(0x1a1208, 20, 60);

const kamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
kamera.position.set(0, 12, 10);
kamera.lookAt(0, 0, 0);

// Işıklar
const ambiyans = new THREE.AmbientLight(0xffeedd, 0.4);
const gunes = new THREE.DirectionalLight(0xfff5e0, 1.2);
gunes.position.set(5, 10, 5);
gunes.castShadow = true;
sahne.add(ambiyans, gunes);
```

---

## Tahta Oluşturma Kalıbı

```js
function tahtaOlustur(sutun, satir, kareBoyut = 1) {
  const grup = new THREE.Group();
  const acikMat = new THREE.MeshLambertMaterial({ color: 0xc8a84b });
  const kouyMat = new THREE.MeshLambertMaterial({ color: 0x2d1f0a });
  const geo = new THREE.BoxGeometry(kareBoyut, 0.1, kareBoyut);

  for (let s = 0; s < satir; s++) {
    for (let st = 0; st < sutun; st++) {
      const mat = (s + st) % 2 === 0 ? acikMat : kouyMat;
      const kare = new THREE.Mesh(geo, mat);
      kare.position.set(
        (st - sutun / 2 + 0.5) * kareBoyut,
        0,
        (s - satir / 2 + 0.5) * kareBoyut
      );
      kare.receiveShadow = true;
      kare.userData = { sutun: st, satir: s }; // raycaster için
      grup.add(kare);
    }
  }
  return grup;
}
```

---

## Raycaster — Tıklama/Dokunma Tespiti

```js
const raycaster = new THREE.Raycaster();
const fare = new THREE.Vector2();

function tiklamaIsle(event) {
  // Hem fare hem dokunma desteği
  const x = event.clientX ?? event.touches[0].clientX;
  const y = event.clientY ?? event.touches[0].clientY;

  fare.x = (x / window.innerWidth) * 2 - 1;
  fare.y = -(y / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(fare, kamera);
  const kesisimler = raycaster.intersectObjects(tahtaKareleri, false);

  if (kesisimler.length > 0) {
    const kare = kesisimler[0].object;
    kareSecildi(kare.userData.sutun, kare.userData.satir);
  }
}

renderer.domElement.addEventListener('click', tiklamaIsle);
renderer.domElement.addEventListener('touchend', e => {
  e.preventDefault();
  tiklamaIsle(e);
}, { passive: false });
```

---

## Bellek Yönetimi (Zorunlu)

```js
function sahneTemizle() {
  sahne.traverse(nesne => {
    if (nesne.geometry) nesne.geometry.dispose();
    if (nesne.material) {
      if (Array.isArray(nesne.material)) {
        nesne.material.forEach(m => m.dispose());
      } else {
        nesne.material.dispose();
      }
    }
  });
  renderer.dispose();
}

// Oyun bitişinde veya yeniden başlatmada çağır
window.addEventListener('beforeunload', sahneTemizle);
```

---

## Animasyon Döngüsü

```js
let animasyonId;

function animate() {
  animasyonId = requestAnimationFrame(animate);
  // Oyun mantığı burada değil — sadece render
  renderer.render(sahne, kamera);
}

function animasyonuDurdur() {
  cancelAnimationFrame(animasyonId);
}

animate();
```

---

## Pencere Yeniden Boyutlandırma

```js
window.addEventListener('resize', () => {
  kamera.aspect = window.innerWidth / window.innerHeight;
  kamera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```


