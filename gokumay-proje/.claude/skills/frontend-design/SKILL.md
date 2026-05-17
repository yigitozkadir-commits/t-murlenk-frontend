---
name: frontend-design
description: |
  Vanilla JS + CSS3 ile UI bileşenleri ve arayüz desenleri.
  React sadece web uygulama projeleri için; oyunlarda sıfır bağımlılık.
---

# Frontend Design Skill

## Temel İlkeler
- Vanilla JS önce, framework sonra
- CSS custom properties ile tema yönetimi
- Mobile-first responsive grid
- GPU hızlandırmalı animasyonlar (transform, opacity)

## Bileşen Şablonları

### Toast Bildirimi
```js
function toast(msg, type = 'info', ms = 3000) {
  const el = Object.assign(document.createElement('div'), {
    className: `toast toast--${type}`,
    textContent: msg
  });
  document.body.appendChild(el);
  requestAnimationFrame(() => el.classList.add('toast--visible'));
  setTimeout(() => { el.classList.remove('toast--visible'); setTimeout(() => el.remove(), 300); }, ms);
}
```

### Modal
```js
function openModal(html) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `<div class="modal">${html}<button class="modal__close">✕</button></div>`;
  overlay.addEventListener('click', e => { if (e.target === overlay || e.target.closest('.modal__close')) overlay.remove(); });
  document.body.appendChild(overlay);
}
```

### CSS Değişkenleri (Tema)
```css
:root {
  --renk-altin: #d4a017;
  --renk-koyu: #1a0a00;
  --renk-acik: #f5e6c8;
  --renk-vurgu: #8b1a1a;
  --gecis: 200ms ease;
  --yari-cercik: 8px;
}
```

## Erişilebilirlik
- `aria-label` tüm ikon butonlarda zorunlu
- Klavye navigasyonu: `tabindex`, `role`, `aria-expanded`
- Kontrast oranı min 4.5:1 (normal metin)

## Performans
- `will-change` sadece aktif animasyonda
- `IntersectionObserver` ile lazy-load
- Debounce: resize/scroll olayları ≥ 100ms


