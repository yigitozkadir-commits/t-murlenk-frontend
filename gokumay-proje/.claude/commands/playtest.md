---
description: Oyunu otomatik test et — denge, edge case, hafıza.
tools: [bash]
---

Playtest: $ARGUMENTS

ADIM 1 — DENGE TESTİ
```bash
bash ~/.claude/scripts/denge_testi.sh "$ARGUMENTS" 200
```

ADIM 2 — EDGE CASE TESTİ
```bash
# Edge case listesini çalıştır
node << 'EOF'
// Edge case testi — temel kontroller
const dosya = '$ARGUMENTS';
const fs = require('fs');

if (!fs.existsSync(dosya)) {
  console.log('❌ Dosya bulunamadı:', dosya);
  process.exit(1);
}

const icerik = fs.readFileSync(dosya, 'utf8');

// Kritik kalıpları kontrol et
const kontroller = [
  ['dispose()', 'Three.js bellek temizleme'],
  ['requestAnimationFrame', 'Render döngüsü'],
  ['addEventListener', 'Event listener'],
  ['try', 'Hata yönetimi'],
  ['DOMContentLoaded', 'DOM hazır kontrolü'],
];

kontroller.forEach(([kalip, aciklama]) => {
  const var_mi = icerik.includes(kalip);
  console.log(`${var_mi ? '✅' : '⚠️ '} ${aciklama}: ${var_mi ? 'Var' : 'YOK'}`);
});
EOF
```

ADIM 3 — PERFORMANS TAHMINI
```bash
# Satır sayısı ve karmaşıklık
echo "Dosya boyutu: $(wc -l < $ARGUMENTS) satır"
echo "Three.js çağrıları: $(grep -c 'new THREE\.' $ARGUMENTS 2>/dev/null || echo 0)"
echo "Event listener: $(grep -c 'addEventListener' $ARGUMENTS 2>/dev/null || echo 0)"
echo "dispose() çağrısı: $(grep -c 'dispose()' $ARGUMENTS 2>/dev/null || echo 0)"
```

ADIM 4 — RAPOR
playtest-ai agent ile tam rapor üret.

OYUN: $ARGUMENTS
