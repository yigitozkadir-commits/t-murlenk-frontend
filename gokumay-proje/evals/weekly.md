---
description: |
  Haftalık sprint değerlendirmesi, sonraki hafta planı ve agent kalite testi.
tools: [bash, read, edit]
---

Haftalık değerlendirme yap.

MEVCUT DURUM:
```bash
# Bu haftaki değişiklikler
git log --oneline --since="7 days ago" 2>/dev/null || \
  ls -lt *.html 2>/dev/null | head -10

# Açık TODO'lar
grep -r "TODO\|FIXME" --include="*.html" --include="*.js" . 2>/dev/null | wc -l

# RAG veritabanı durumu
python3 ~/.claude/scripts/rag_seed.py sayi 2>/dev/null || echo "RAG: bağlanamadı"
```

BU HAFTA DEĞERLENDİRME:
### Tamamlanan
- [liste]

### Yarım Kalan
- [liste]

### Karşılaşılan Sorunlar
- [liste + nasıl çözüldü]

### Öğrenilenler
- [liste]

AGENT KALİTE TESTİ (hızlı — 5 kritik agent):
```bash
python3 ~/.claude/scripts/agent_evals.py --hizli 2>/dev/null | tail -20
```

Eğer herhangi bir agent ❌ aldıysa agent dosyasını gözden geçir.

RAG GÜNCELLEME:
```bash
# Değişen dosyaları yeniden indeksle (sadece hash değişmişleri)
python3 ~/.claude/scripts/rag_auto_index.py 2>/dev/null
```

SONRAKI HAFTA PLANI:
Odak: [tek özellik veya oyun]
Agent sırası: [workflow-orchestrator formatında]

Versiyon hedefleri:
- [Oyun 1] v[N] → v[N+1]: [ne değişecek]

CLAUDE.md güncelleme gerekiyor mu?
- Aktif proje versiyonları
- Yeni altın kural
- Arşive taşınacak proje
