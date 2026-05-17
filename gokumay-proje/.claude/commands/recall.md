---
description: Geçmiş kararları ve çözümleri hafızadan getir.
tools: [bash]
---

Hafızadan ara: $ARGUMENTS

ADIM 1 — SEMANTİK ARAMA
```bash
python3 ~/.claude/scripts/memory_client.py hatirla "$ARGUMENTS"
```

ADIM 2 — KATEGORİYE GÖRE DARALT (gerekirse)
```bash
# Sadece bug çözümleri
python3 ~/.claude/scripts/memory_client.py hatirla "$ARGUMENTS" bug

# Sadece mimari kararlar
python3 ~/.claude/scripts/memory_client.py hatirla "$ARGUMENTS" mimari

# Belirli proje
python3 ~/.claude/scripts/memory_client.py hatirla "$ARGUMENTS" genel timurlenk
```

ADIM 3 — SONUÇLARI CLAUDE BAĞLAMINA EKLE
Bulunan kayıtları şu anda yaptığın görevle ilişkilendir:
"Geçmişte [X sorunu] [Y şekilde] çözülmüştü.
 Şu anki [Z sorunu] için aynı yaklaşım uygulanabilir mi?"

ADIM 4 — GÜNCELLE (bilgi değiştiyse)
```bash
# Eski kaydı sil → yenisini ekle
python3 ~/.claude/scripts/memory_client.py unut "[eski başlık]"
python3 ~/.claude/scripts/memory_client.py kaydet "[yeni başlık]" "[yeni içerik]"
```

ARANAN: $ARGUMENTS
