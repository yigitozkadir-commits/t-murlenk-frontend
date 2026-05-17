---
name: rag-pipeline
description: |
  RAG (Retrieval-Augmented Generation) kurulumu ve kullanımı.
  Belge yükleme, chunk stratejisi, semantik arama, Claude entegrasyonu.
  Kullan: "rag-pipeline ile belgeleri indeksle"
---

# RAG Pipeline

## TOKEN KURALI
Tüm belgeyi yükleme — ilgili chunk'ları getir (max 3-5).

---

## Chunk Stratejisi

```python
def akilli_chunk(metin: str, tip: str = 'genel') -> list:
    """
    Belge tipine göre optimal chunk stratejisi

    tip='gdd'      → Başlık bazlı bölme (## ile)
    tip='kod'      → Fonksiyon bazlı bölme
    tip='bug'      → Satır bazlı, 300 token
    tip='tarihi'   → Paragraf bazlı, 500 token
    tip='genel'    → Kayan pencere, 600 token, %15 bindirme
    """
    if tip == 'gdd':
        # Markdown başlıklarında böl
        import re
        bölümler = re.split(r'\n(?=#{1,3} )', metin)
        return [b.strip() for b in bölümler if len(b.strip()) > 50]

    elif tip == 'kod':
        # Fonksiyon tanımlarında böl
        import re
        fonksiyonlar = re.split(r'\n(?=function |const |class |def )', metin)
        return [f.strip() for f in fonksiyonlar if len(f.strip()) > 30]

    else:
        # Kayan pencere
        kelimeler = metin.split()
        boyut = {'bug': 200, 'tarihi': 400, 'genel': 500}.get(tip, 500)
        bindirme = boyut // 6
        parcalar = []
        i = 0
        while i < len(kelimeler):
            parca = ' '.join(kelimeler[i:i+boyut])
            if len(parca) > 50:
                parcalar.append(parca)
            i += boyut - bindirme
        return parcalar
```

---

## Toplu Belge Yükleme

```bash
#!/bin/bash
# ~/.claude/scripts/rag_yukle.sh
# Kullanım: bash rag_yukle.sh [klasör]

KLASOR="${1:-.}"
echo "📚 RAG indeksleme: $KLASOR"

# GDD dosyaları
for f in "$KLASOR"/gdd/*.md; do
  [ -f "$f" ] && python3 ~/.claude/scripts/rag_client.py yukle \
    "$f" "gdd-$(basename $f .md)" "gdd"
done

# Bug raporları
for f in "$KLASOR"/bugs/*.md; do
  [ -f "$f" ] && python3 ~/.claude/scripts/rag_client.py yukle \
    "$f" "bug-$(basename $f .md)" "bug"
done

# Claude konfigürasyonu
python3 ~/.claude/scripts/rag_client.py yukle \
  ~/.claude/CLAUDE.md "claude-config" "karar"

echo "✅ İndeksleme tamamlandı"
python3 -c "
from supabase import create_client
import os
db = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
r = db.table('belgeler').select('id', count='exact').execute()
print(f'Toplam chunk: {r.count}')
"
```

---

## Sorgu Optimizasyonu

```python
def hibrit_ara(sorgu: str, db, sayi: int = 5) -> list:
    """
    Hibrit arama: Semantik + Tam metin
    Semantik tek başına bazen kaçırır — kombinasyon daha iyi
    """
    embedding = embed(sorgu)

    # 1. Semantik arama
    semantik = db.rpc('belge_ara', {
        'sorgu_embedding': embedding,
        'maks_sonuc': sayi
    }).execute().data

    # 2. Tam metin araması
    tam_metin = db.table('belgeler')\
        .select('kaynak,baslik,icerik,tur')\
        .text_search('icerik', sorgu.replace(' ', ' & '))\
        .limit(sayi).execute().data

    # 3. Birleştir, tekrarları kaldır
    gorulen = set()
    birlesik = []
    for k in semantik + tam_metin:
        anahtar = k['baslik']
        if anahtar not in gorulen:
            gorulen.add(anahtar)
            birlesik.append(k)

    return birlesik[:sayi]
```

---

## Claude Prompt Entegrasyonu

```python
def rag_sistem_prompt(sorgu: str) -> list:
    """
    Cache uyumlu RAG bağlamı üret
    Sistem promptuna ekle → prompt caching ile ucuzlaşır
    """
    bagłam = rag_sorgula(sorgu)

    return [
        {
            "type": "text",
            "text": "Sen Gök Umay stüdyo asistanısın.",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": f"İlgili belgeler:\n\n{bagłam}",
            "cache_control": {"type": "ephemeral"}  # Bağlam da cache'le
        }
    ]
```

---

## Bakım

```bash
# Eski chunk'ları temizle (belge güncellenince)
python3 -c "
from supabase import create_client
import os
db = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
# Kaynak adına göre sil
db.table('belgeler').delete().eq('kaynak', 'gdd-timurlenk').execute()
print('Temizlendi — yeniden yükle')
"

# İstatistik
python3 -c "
from supabase import create_client
import os
db = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
r = db.table('belgeler').select('tur').execute()
from collections import Counter
print(Counter(k['tur'] for k in r.data))
"
```
