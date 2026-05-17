---
description: Yeni oyun projesi başlat — araştırmadan iskelet koda.
tools: [read, edit, bash]
---

Yeni oyun projesi başlat: $ARGUMENTS

ADIM 1 — ARAŞTIRMA (research-analyst + narrative-director)
- Oyunun tarihi kökeni belgelenmiş mi?
- Kurallar tam mı yoksa rekonstrüksiyon mu gerekiyor?
- NotebookLM'e eklenecek kaynak listesi

ADIM 2 — TASARIM (game-designer)
- Temel kurallar (5 madde)
- Kazanma koşulu
- Taş/parça listesi ve değerleri
- Edge case'ler

ADIM 3 — MİMARİ (technical-director)
- Tahta boyutu ve yapısı
- AI motoru derinliği (derinlik 2/3/4)
- Bozkır Platform'a entegre mi, standalone mi?

ADIM 4 — ISKELET DOSYA OLUŞTUR
```bash
# Dosya adı: [oyun_adi]_v1.html
cp ~/.claude/templates/oyun-iskelet.html [oyun_adi]_v1.html
```

İskelet içeriği:
- Three.js inline CDN
- Tahta oluşturma kalıbı (three-js-patterns skill)
- AI motor şablonu (game-ai-engine skill)
- HUD yapısı (frontend-design skill)
- Gök Umay renk sistemi

ADIM 5 — CLAUDE.md GÜNCELLE
Aktif Projeler bölümüne ekle.

OYUN: $ARGUMENTS


