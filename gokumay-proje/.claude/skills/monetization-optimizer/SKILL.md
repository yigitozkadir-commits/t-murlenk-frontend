---
name: monetization-optimizer
description: |
  Play Store/App Store gelir analizi, fiyatlandırma optimizasyonu,
  freemium model tasarımı, ASO gelir etkisi.
  Kullan: "monetization-optimizer ile gelir modelini analiz et"
---

# Gelir Optimizasyonu

## TOKEN KURALI
Genel pazarlama değil — Gök Umay'ın niş kitlesine özgü sayılar.

---

## Freemium Dönüşüm Formülü

```python
def donusum_hedefi_hesapla(
    aylik_indirme: int,
    hedef_gelir_usd: float,
    fiyat: float
) -> dict:
    """Hedef gelir için gereken dönüşüm oranı"""
    gereken_satin_alma = hedef_gelir_usd / (fiyat * 0.70)  # Mağaza %30 alır
    gereken_oran = gereken_satin_alma / aylik_indirme * 100

    return {
        "gereken_donusum": f"%{gereken_oran:.1f}",
        "satin_alma_hedefi": int(gereken_satin_alma),
        "gercekci": gereken_oran < 5,  # Sektör ortalaması %2-5
        "yorum": (
            "✅ Gerçekçi hedef" if gereken_oran < 3 else
            "⚠️ Zorlu ama mümkün" if gereken_oran < 5 else
            "❌ İndirme artırılmalı"
        )
    }

# Örnek:
# 1000 indirme/ay, $100 hedef, $1.99 fiyat
# → %7.1 dönüşüm gerekli → zor → fiyat artır veya indirme artır
```

---

## Play Store Gelir Tahmini

```python
MAAS_KESINTISI = {
    "play_store": 0.30,   # %30 (ilk $1M'dan sonra %15)
    "app_store":  0.30,   # %30 (küçük geliştirici %15)
    "itch_io":    0.10,   # %10 varsayılan (ayarlanabilir)
}

def net_gelir(brut: float, platform: str) -> float:
    return brut * (1 - MAAS_KESINTISI.get(platform, 0.30))

# $100 brut → Play Store: $70 net
# $100 brut → itch.io: $90 net
```

---

## Fiyat Testi (A/B)

```
Test Grubu A: $0.99  → Dönüşüm: yüksek, gelir: düşük
Test Grubu B: $1.99  → Dönüşüm: orta, gelir: orta
Test Grubu C: $2.99  → Dönüşüm: düşük, gelir: yüksek?

Formül: Gelir = İndirme × Dönüşüm × (Fiyat × 0.70)

2 hafta her fiyatı test et → en yüksek geliri seç
Play Store "Abone ol" dışındaki fiyat denemeleri için
Google Play Console → Gelir raporları → Ülkeye göre filtrele
```

---

## Ülke Bazlı Fiyatlandırma

```python
# Play Store yerel fiyatlandırma önerileri
ULKE_FAKTOR = {
    "TR":  0.30,  # Türkiye: $1.99 → ₺~18 (satın alma gücü)
    "US":  1.00,  # Baz
    "DE":  0.90,  # Almanya
    "GB":  0.95,  # İngiltere
    "IN":  0.20,  # Hindistan
    "BR":  0.40,  # Brezilya
}

def yerel_fiyat(baz_usd: float, ulke: str) -> str:
    faktor = ULKE_FAKTOR.get(ulke, 1.0)
    return f"${baz_usd * faktor:.2f}"

# Play Store bunu otomatik yapar —
# ama manuel override için kullanılabilir
```

---

## Ko-fi / Patreon Stratejisi

```
Tier 1 — $2/ay "Destekçi"
  ✓ İsim "Destekçiler" listesinde
  ✓ Beta erişimi
  ✓ Özel Discord rolü

Tier 2 — $5/ay "Bozkır Yoldaşı"
  ✓ Tier 1 + tümü
  ✓ Aylık geliştirici notu
  ✓ Oyun öneri oylaması

Tier 3 — $15/ay "Gök Umay Hamisi"
  ✓ Tier 2 + tümü
  ✓ İsim oyun içi credits'e
  ✓ Doğrudan Discord DM erişimi

Hedef: 50 × $5 = $250/ay pasif gelir
```

---

## Çıktı

```
## Gelir Analizi — [oyun/dönem]

Mevcut durum:
  İndirme: [N]/ay | Dönüşüm: %[N] | Gelir: $[N]/ay

Optimizasyon önerisi:
  Fiyat: $[N] → $[N]
  Freemium değişiklik: [ne açılsın/kapansın]
  Tahmini etki: +$[N]/ay

Break-even: [N] ay
```
