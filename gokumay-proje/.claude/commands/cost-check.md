---
description: API maliyet analizi ve optimizasyon önerileri.
tools: [bash]
---

API maliyet analizi yap.

ADIM 1 — MEVCUT KULLANIM
```bash
# Claude Code kullanım istatistikleri
claude --usage 2>/dev/null || \
  echo "Kullanım: Anthropic Console → Usage bölümünden kontrol et"

# Günlük harcama tahmini
echo "Hedef: Günde <\$2 maliyet"
```

ADIM 2 — OPTİMİZASYON TARAMASI

Aşağıdaki soruları kontrol et:

PROMPT CACHING:
```bash
# Python scriptlerde cache_control var mı?
grep -r "cache_control" ~/.claude/scripts/ 2>/dev/null && \
  echo "✅ Caching aktif" || \
  echo "❌ Caching yok — prompt-caching skill'ini uygula"
```

GEMİNİ KULLANIMI:
```bash
# Bu ay kaç Gemini isteği yapıldı?
ls ~/.gemini/logs/ 2>/dev/null | wc -l || \
  echo "Gemini: Log bulunamadı"
```

CLAUDE CODE EFFort SEVİYESİ:
```bash
grep "CLAUDE_CODE_EFFORT_LEVEL" ~/.claude/settings.json
# medium olmalı — high çok token yer
```

ADIM 3 — MALİYET HESAPLAMA

```python
# Tahmini aylık maliyet (Sonnet 4.6)
# Gerçek değerleri gir:
gunluk_istek = 50        # ortalama
istek_basi_token = 2000  # input + output
cache_hit_orani = 0.7    # %70 cache hit

normal = gunluk_istek * istek_basi_token * 3 / 1_000_000
caching_ile = normal * (1 - cache_hit_orani * 0.9)
gemini_tasarruf = gunluk_istek * 0.3 * istek_basi_token * 3 / 1_000_000

print(f"Normal: ${normal*30:.2f}/ay")
print(f"Caching ile: ${caching_ile*30:.2f}/ay")
print(f"Gemini hibrit: ${(caching_ile - gemini_tasarruf)*30:.2f}/ay")
```

ADIM 4 — KRİTİK OPTİMİZASYONLAR

Sırayla uygula — sıra önemli:

1. CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 ← settings.json'da var mı?
2. Sistem promptu cache_control var mı?
3. Büyük dosyalar .claudeignore'da mı?
4. Araştırma görevleri Gemini'ye taşındı mı?
5. Batch API kullanılıyor mu? (toplu işlemler için)

ÇIKTI:
```
Tahmini aylık maliyet: $[X]
Potansiyel tasarruf:   $[Y] (%[Z])
Öncelikli eylem:       [ne yapılmalı]
```
