---
description: Önemli kararı veya bilgiyi kalıcı hafızaya kaydet.
tools: [bash]
---

Şunu hafızaya kaydet: $ARGUMENTS

ADIM 1 — NE KAYDEDİLECEK?
Otomatik kategori tespiti:
- "hata/bug/fix/düzelt" geçiyorsa → kategori: bug
- "mimari/karar/seçim/neden" geçiyorsa → kategori: mimari
- "kural/mekanik/denge/oyun" geçiyorsa → kategori: oyun
- "tarihi/mitoloji/kültür/kaynak" geçiyorsa → kategori: kulturel
- Diğer → kategori: proje

ADIM 2 — KAYDET
```bash
python3 ~/.claude/scripts/memory_client.py kaydet \
  "$ARGUMENTS" \
  "$(date +%Y-%m-%d) tarihinde kaydedildi. Detay: $ARGUMENTS" \
  "[otomatik kategori]" \
  "[aktif proje — CLAUDE.md'den]"
```

ADIM 3 — DOĞRULA
```bash
python3 ~/.claude/scripts/memory_client.py hatirla "$ARGUMENTS"
```

Kaydedilen: ✅ [başlık]
Kategori: [kategori]
Proje: [proje]

SONRAKİ ARAŞTIRMADA OTOMATİK ÇEKILIR.
