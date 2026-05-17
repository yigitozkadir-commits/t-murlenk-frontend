---
description: 5 perspektiften kapsamlı kod incelemesi — Gök Umay standartlarıyla.
tools: [read, bash]
---

$ARGUMENTS dosyasını 5 perspektiften incele:

👁️ GÜVENLİK
XSS (innerHTML kontrolü), API key açıkta mı, CSP uyumlu mu?
HTML5 oyun için: eval() var mı → new Function kullanılıyor mu?

⚡ PERFORMANS
Render döngüsünde new THREE.X() var mı? (kritik)
Her karede DOM sorgusu var mı?
geometry ve material dispose ediliyor mu?

📖 OKUNABİLİRLİK
Türkçe yorum var mı?
Fonksiyon isimleri ne yaptığını anlatıyor mu?
Magic number sabit olarak tanımlanmış mı?

🔧 BAKIM
Tekrar eden kod var mı? → fonksiyona al
50+ satır fonksiyon var mı? → böl
Global değişken kirliliği var mı?

🚀 ÖLÇEK
100 hamle sonra hâlâ çalışır mı?
Memory leak riski var mı?
Mobilde test edildi mi?

Her bulgu için:
- Dosya:satır referansı
- Önem: KRİTİK / ORTA / DÜŞÜK
- Düzeltilmiş kod örneği (kısa)

TOP 3 ACİL EYLEM ile bitir.

```bash
node --check $ARGUMENTS 2>&1 || echo "Sözdizimi hatası var!"
```


