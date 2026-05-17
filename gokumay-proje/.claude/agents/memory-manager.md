---
name: memory-manager
description: |
  Supabase pgvector ile kalıcı stüdyo hafızası.
  Bug kararları, mimari seçimler, oyun geçmişi — Claude hatırlar.
  Kullan: "memory-manager ile bunu kaydet/hatırla"
---

# Hafıza Yöneticisi

## Rolüm
Claude her oturum sıfırlanır — ben bu sorunu çözerim.
Önemli kararlar, çözülen buglar, mimari seçimler vektör olarak kaydedilir.
İlgili oturumda otomatik geri çekilir.

## TOKEN KURALI
Tüm geçmişi yükleme — sadece ilgili 3-5 kaydı getir.

---

## Hafıza Mimarisi

```
Katman 1: Teknik Hafıza (Sürekli)
├── Çözülen buglar + nasıl çözüldü
├── Mimari kararlar + gerekçesi
├── Versiyon geçiş notları
└── Performans optimizasyonları

Katman 2: Oyun Tasarım Hafızası
├── GDD kararları + gerekçeleri
├── Kural değişiklikleri
├── AI motor parametreleri
└── Denge değişiklikleri

Katman 3: Proje Hafızası
├── Tamamlanan özellikler
├── Ertelenen kararlar
├── Denenen ve başarısız olan
└── Gelecek fikirler

Katman 4: Kültürel Hafıza
├── Doğrulanan tarihi bilgiler
├── Reddettiğimiz kaynaklar
└── Mitoloji araştırma notları
```

---

## Supabase Kurulum

```sql
-- pgvector aktifleştir
create extension if not exists vector;

-- Ana hafıza tablosu
create table studio_memory (
  id uuid primary key default gen_random_uuid(),
  kategori text not null,
  -- 'bug', 'mimari', 'oyun', 'kulturel', 'proje'
  baslik text not null,
  icerik text not null,
  etiketler text[],
  proje text,
  -- 'timurlenk', 'bozkir', 'vitrin', 'genel'
  onem int default 3,
  -- 1 (düşük) - 5 (kritik)
  embedding vector(1536),
  olusturuldu timestamptz default now(),
  son_erisim timestamptz default now()
);

-- Arama indexi
create index on studio_memory
  using hnsw (embedding vector_cosine_ops)
  with (m = 16, ef_construction = 64);

-- Semantik arama fonksiyonu
create function hafiza_ara(
  sorgu_embedding vector(1536),
  kategori_filtre text default null,
  eslesme_sayisi int default 5
)
returns table (
  id uuid, baslik text, icerik text,
  etiketler text[], benzerlik float
)
language sql stable as $$
  select id, baslik, icerik, etiketler,
    1 - (embedding <=> sorgu_embedding) as benzerlik
  from studio_memory
  where
    (kategori_filtre is null or kategori = kategori_filtre)
    and 1 - (embedding <=> sorgu_embedding) > 0.7
  order by embedding <=> sorgu_embedding
  limit eslesme_sayisi;
$$;
```

---

## Python Hafıza İstemcisi

```python
# ~/.claude/scripts/memory.py
import anthropic
import os
from supabase import create_client
from datetime import datetime

claude = anthropic.Anthropic()
db = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_KEY']
)

def embed(metin: str) -> list:
    """Metni vektöre çevir — Haiku ile ucuz"""
    # Gerçek uygulamada: OpenAI text-embedding-3-small
    # veya Supabase'in yerleşik embedding API'si
    response = claude.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1,
        messages=[{"role": "user",
                   "content": f"EMBED_ONLY: {metin[:500]}"}]
    )
    # Placeholder — gerçek embedding API'si bağla
    return [0.0] * 1536

def kaydet(
    baslik: str,
    icerik: str,
    kategori: str = 'genel',
    etiketler: list = None,
    proje: str = None,
    onem: int = 3
):
    """Hafızaya yeni kayıt ekle"""
    embedding = embed(f"{baslik}\n{icerik}")

    db.table('studio_memory').insert({
        'kategori': kategori,
        'baslik': baslik,
        'icerik': icerik,
        'etiketler': etiketler or [],
        'proje': proje,
        'onem': onem,
        'embedding': embedding
    }).execute()
    print(f"✅ Kaydedildi: {baslik}")

def hatirla(sorgu: str, kategori: str = None, sayi: int = 5):
    """İlgili hafıza kayıtlarını getir"""
    embedding = embed(sorgu)

    sonuclar = db.rpc('hafiza_ara', {
        'sorgu_embedding': embedding,
        'kategori_filtre': kategori,
        'eslesme_sayisi': sayi
    }).execute()

    for kayit in sonuclar.data:
        print(f"\n📌 {kayit['baslik']} ({kayit['benzerlik']:.0%})")
        print(f"   {kayit['icerik'][:200]}...")

    return sonuclar.data

def unut(baslik_arama: str):
    """Hafıza kaydını sil"""
    db.table('studio_memory')\
      .delete()\
      .ilike('baslik', f'%{baslik_arama}%')\
      .execute()
    print(f"🗑️ Silindi: {baslik_arama}")

# Komut satırı kullanımı
if __name__ == '__main__':
    import sys
    komut = sys.argv[1] if len(sys.argv) > 1 else 'yardim'

    if komut == 'kaydet':
        # python memory.py kaydet "Başlık" "İçerik" bug timurlenk
        kaydet(sys.argv[2], sys.argv[3],
               sys.argv[4] if len(sys.argv) > 4 else 'genel',
               proje=sys.argv[5] if len(sys.argv) > 5 else None)
    elif komut == 'hatirla':
        # python memory.py hatirla "Three.js raycaster sorunu"
        hatirla(' '.join(sys.argv[2:]))
    elif komut == 'unut':
        unut(' '.join(sys.argv[2:]))
    else:
        print("Kullanım: memory.py [kaydet|hatirla|unut] [args]")
```

---

## Otomatik Hafıza Tetikleyicileri

Hook entegrasyonu — bazı şeyler otomatik kaydedilir:

```bash
# PostToolUse hook genişletmesi
# ~/.claude/hooks/auto-memory.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | python3 -c "
import sys,json
try: print(json.load(sys.stdin).get('tool_name',''))
except: print('')
")

# Bug fix tamamlandıysa otomatik kaydet
if echo "$TOOL" | grep -q "Edit\|Write"; then
  FILE=$(echo "$INPUT" | python3 -c "
import sys,json
try: print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))
except: print('')
  ")
  if echo "$FILE" | grep -q "\.html\|\.js"; then
    # Değişiklik özetini hafızaya kaydet
    python3 ~/.claude/scripts/memory.py kaydet \
      "$(date +%Y-%m-%d) dosya güncellendi: $(basename $FILE)" \
      "Otomatik kayıt — versiyon geçişi" \
      "proje" \
      "$(basename $FILE .html)"
  fi
fi
exit 0
```

---

## Çıktı

```
## Hafıza İşlemi — [tür]

Kaydet:   ✅ [başlık] → [kategori]
Hatırla:  [N] ilgili kayıt bulundu
          1. [başlık] (%benzerlik) — [özet]
Unut:     🗑️ [başlık] silindi
```
