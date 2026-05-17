---
name: rag-pipeline
description: |
  Oyun dokümanları üzerinde RAG (Retrieval-Augmented Generation).
  GDD, bug raporları, tarihi kaynaklar — semantik arama ile anlık bağlam.
  Kullan: "rag-pipeline ile [konu] hakkında GDD'yi sorgula"
---

# RAG Pipeline Yöneticisi

## Rolüm
Gök Umay'ın tüm belgelerini aranabilir hale getiririm.
Soru sorarsın — ilgili belge parçası otomatik bulunur, Claude'a verilir.

## TOKEN KURALI
Tüm belgeyi yükleme — sadece ilgili chunk'ları getir (max 3-5).

---

## RAG Mimarisi

```
Belgeler (GDD, bug raporu, tarihi kaynak, CLAUDE.md)
        ↓
   Chunking (500-800 token parçalar)
        ↓
   Embedding (Supabase/OpenAI)
        ↓
   pgvector'e kaydet
        ↓
   Soru gelince → semantik arama → ilgili chunk'lar → Claude'a bağlam
```

---

## Supabase RAG Şeması

```sql
-- Belge deposu
create table belgeler (
  id          uuid primary key default gen_random_uuid(),
  kaynak      text not null,     -- 'gdd-timurlenk', 'bug-raporu', 'murray-1913'
  tur         text not null,     -- 'gdd', 'bug', 'tarihi', 'kod', 'karar'
  baslik      text not null,
  icerik      text not null,
  chunk_index int  default 0,    -- Büyük belge bölümü
  meta        jsonb default '{}', -- Proje, versiyon, tarih
  embedding   vector(1536),
  eklendi     timestamptz default now()
);

create index belgeler_embedding_idx
  on belgeler using hnsw (embedding vector_cosine_ops);

-- RAG arama fonksiyonu
create or replace function belge_ara(
  sorgu_embedding vector(1536),
  tur_filtre      text  default null,
  kaynak_filtre   text  default null,
  min_benzerlik   float default 0.6,
  maks_sonuc      int   default 5
)
returns table (
  kaynak text, baslik text, icerik text,
  tur text, meta jsonb, benzerlik float
)
language sql stable as $$
  select kaynak, baslik, icerik, tur, meta,
    1 - (embedding <=> sorgu_embedding) as benzerlik
  from belgeler
  where
    (tur_filtre    is null or tur    = tur_filtre)
    and (kaynak_filtre is null or kaynak = kaynak_filtre)
    and 1 - (embedding <=> sorgu_embedding) > min_benzerlik
  order by embedding <=> sorgu_embedding
  limit maks_sonuc;
$$;
```

---

## Python RAG İstemcisi

```python
# ~/.claude/scripts/rag_client.py
import os, sys, json
from pathlib import Path
from supabase import create_client

db = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_KEY']
)

def chunk_yap(metin: str, boyut: int = 600, bindirme: int = 100) -> list:
    """Metni örtüşen parçalara böl"""
    kelimeler = metin.split()
    parcalar = []
    i = 0
    while i < len(kelimeler):
        parca = ' '.join(kelimeler[i:i+boyut])
        parcalar.append(parca)
        i += boyut - bindirme
    return parcalar

def embed(metin: str) -> list:
    """Placeholder — gerçek embedding API'si bağla"""
    import hashlib
    h = hashlib.md5(metin.encode()).digest()
    return [float(b)/255.0 for b in h] * 96

def belge_yukle(
    dosya_yolu: str,
    kaynak: str,
    tur: str = 'gdd',
    meta: dict = None
):
    """Belgeyi chunk'la, embed et, Supabase'e yükle"""
    metin = Path(dosya_yolu).read_text(encoding='utf-8')
    baslik = Path(dosya_yolu).stem

    parcalar = chunk_yap(metin)
    print(f"📄 {baslik}: {len(parcalar)} parça")

    for i, parca in enumerate(parcalar):
        db.table('belgeler').insert({
            'kaynak': kaynak,
            'tur': tur,
            'baslik': f"{baslik} [Bölüm {i+1}/{len(parcalar)}]",
            'icerik': parca,
            'chunk_index': i,
            'meta': meta or {},
            'embedding': embed(parca)
        }).execute()

    print(f"✅ {len(parcalar)} chunk yüklendi: {kaynak}")

def rag_sorgula(
    soru: str,
    tur: str = None,
    kaynak: str = None,
    sayi: int = 4
) -> str:
    """Semantik arama → Claude bağlamı üret"""
    embedding = embed(soru)

    result = db.rpc('belge_ara', {
        'sorgu_embedding': embedding,
        'tur_filtre': tur,
        'kaynak_filtre': kaynak,
        'maks_sonuc': sayi
    }).execute()

    if not result.data:
        return "İlgili belge parçası bulunamadı."

    bagłam = f"## '{soru}' İçin İlgili Belgeler\n\n"
    for chunk in result.data:
        bagłam += f"### {chunk['baslik']} "
        bagłam += f"(Kaynak: {chunk['kaynak']}, "
        bagłam += f"Benzerlik: %{chunk['benzerlik']*100:.0f})\n"
        bagłam += f"{chunk['icerik']}\n\n---\n\n"

    return bagłam

# CLI
if __name__ == '__main__':
    komut = sys.argv[1] if len(sys.argv) > 1 else 'yardim'

    if komut == 'yukle' and len(sys.argv) >= 4:
        belge_yukle(sys.argv[2], sys.argv[3],
                    sys.argv[4] if len(sys.argv) > 4 else 'gdd')
    elif komut == 'ara' and len(sys.argv) >= 3:
        print(rag_sorgula(' '.join(sys.argv[2:])))
    else:
        print("Kullanım:")
        print("  rag.py yukle dosya.md kaynak-adi [tur]")
        print("  rag.py ara 'soru metni'")
```

---

## Gök Umay Belge Kataloğu

Yüklenecek belgeler ve öncelik sırası:

```bash
# 1. CLAUDE.md (en önemli)
python3 ~/.claude/scripts/rag_client.py yukle \
  ~/.claude/CLAUDE.md "claude-md" "karar"

# 2. GDD dosyaları
for f in ~/projeler/gdd/*.md; do
  python3 ~/.claude/scripts/rag_client.py yukle \
    "$f" "gdd-$(basename $f .md)" "gdd"
done

# 3. Bug raporları
python3 ~/.claude/scripts/rag_client.py yukle \
  ~/projeler/bug-raporlari.md "bug-gecmisi" "bug"

# 4. Tarihi kaynaklar (NotebookLM özeti)
python3 ~/.claude/scripts/rag_client.py yukle \
  ~/notlar/murray-ozet.md "murray-1913" "tarihi"
```

---

## Claude Bağlam Entegrasyonu

```python
# Herhangi bir Claude çağrısından önce RAG çalıştır
def rag_ile_sor(soru: str, claude_client) -> str:
    # 1. İlgili belge parçalarını getir
    bagłam = rag_sorgula(soru)

    # 2. Claude'a bağlamla birlikte sor
    response = claude_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=[
            {
                "type": "text",
                "text": "Sen Gök Umay stüdyo asistanısın.",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": bagłam,  # RAG bağlamı
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[{"role": "user", "content": soru}]
    )
    return response.content[0].text
```

---

## Çıktı

```
## RAG Sorgu Sonucu — [soru]

Bulunan: [N] chunk
Kaynaklar: [liste]

### Bağlam Özeti
[İlgili içerik özeti]

### Claude Yanıtı
[RAG bağlamlı yanıt]
```
