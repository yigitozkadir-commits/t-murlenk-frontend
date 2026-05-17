---
name: supabase-memory
description: |
  Supabase pgvector ile kalıcı stüdyo hafızası kurulumu.
  SQL şemaları, Python istemcisi, semantik arama.
  Kullan: "supabase-memory ile hafızayı kur/sorgula"
---

# Supabase Kalıcı Hafıza

## TOKEN KURALI
Şema + fonksiyon + istemci kodu — üçü birlikte ver.

---

## Termux Kurulum

```bash
# Supabase CLI
npm install -g supabase

# Python bağımlılıkları
pip install supabase anthropic numpy --break-system-packages

# Ortam değişkenleri
echo 'export SUPABASE_URL="https://[proje].supabase.co"' >> ~/.env
echo 'export SUPABASE_KEY="[anon-key]"' >> ~/.env
source ~/.env

# Bağlantı testi
python3 -c "
from supabase import create_client
import os
db = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
print('✅ Bağlantı başarılı')
"
```

---

## Veritabanı Şeması

```sql
-- pgvector aktifleştir (Supabase'de zaten var)
create extension if not exists vector;

-- Ana hafıza tablosu
create table studio_memory (
  id          uuid primary key default gen_random_uuid(),
  kategori    text not null check (kategori in (
                'bug', 'mimari', 'oyun', 'kulturel', 'proje', 'genel'
              )),
  baslik      text not null,
  icerik      text not null,
  etiketler   text[] default '{}',
  proje       text, -- 'timurlenk' | 'bozkir' | 'vitrin' | null
  onem        int default 3 check (onem between 1 and 5),
  embedding   vector(1536),
  olusturuldu timestamptz default now(),
  guncellendi timestamptz default now()
);

-- Arama indexi (HNSW — hızlı, iyi kalite)
create index studio_memory_embedding_idx
  on studio_memory
  using hnsw (embedding vector_cosine_ops)
  with (m = 16, ef_construction = 64);

-- Kategoriye göre index
create index studio_memory_kategori_idx
  on studio_memory (kategori);

-- Projeye göre index
create index studio_memory_proje_idx
  on studio_memory (proje);

-- Semantik arama fonksiyonu
create or replace function hafiza_ara(
  sorgu_embedding vector(1536),
  kategori_filtre text    default null,
  proje_filtre    text    default null,
  min_benzerlik   float   default 0.65,
  maks_sonuc      int     default 5
)
returns table (
  id          uuid,
  kategori    text,
  baslik      text,
  icerik      text,
  etiketler   text[],
  proje       text,
  onem        int,
  benzerlik   float,
  olusturuldu timestamptz
)
language sql stable as $$
  select
    id, kategori, baslik, icerik,
    etiketler, proje, onem,
    1 - (embedding <=> sorgu_embedding) as benzerlik,
    olusturuldu
  from studio_memory
  where
    (kategori_filtre is null or kategori = kategori_filtre)
    and (proje_filtre is null or proje = proje_filtre)
    and 1 - (embedding <=> sorgu_embedding) > min_benzerlik
  order by embedding <=> sorgu_embedding
  limit maks_sonuc;
$$;

-- Son güncelleme trigger
create or replace function guncellendi_guncelle()
returns trigger language plpgsql as $$
begin
  new.guncellendi = now();
  return new;
end;
$$;

create trigger studio_memory_guncellendi
  before update on studio_memory
  for each row execute function guncellendi_guncelle();
```

---

## Python İstemcisi (Tam)

```python
# ~/.claude/scripts/memory_client.py
import anthropic
import os
import json
from supabase import create_client
from datetime import datetime

class GokUmayMemory:
    def __init__(self):
        self.claude = anthropic.Anthropic()
        self.db = create_client(
            os.environ['SUPABASE_URL'],
            os.environ['SUPABASE_KEY']
        )

    def embed(self, metin: str) -> list:
        """
        Metni vektöre çevir.
        Üretimde: Supabase'in yerleşik embedding API'si veya
                  OpenAI text-embedding-3-small (1536 boyut, ucuz)
        """
        # Supabase Edge Function ile embedding (önerilen)
        # response = self.db.functions.invoke('embed', {'input': metin})
        # return response.data['embedding']

        # Geçici placeholder — gerçek API bağla
        import hashlib
        h = hashlib.md5(metin.encode()).digest()
        return [float(b) / 255.0 for b in h] * 96  # 1536 boyut

    def kaydet(
        self,
        baslik: str,
        icerik: str,
        kategori: str = 'genel',
        etiketler: list = None,
        proje: str = None,
        onem: int = 3
    ) -> str:
        """Hafızaya yeni kayıt ekle — ID döndürür"""
        embedding = self.embed(f"{baslik}\n{icerik}")

        result = self.db.table('studio_memory').insert({
            'kategori': kategori,
            'baslik': baslik,
            'icerik': icerik,
            'etiketler': etiketler or [],
            'proje': proje,
            'onem': onem,
            'embedding': embedding
        }).execute()

        kayit_id = result.data[0]['id']
        print(f"✅ Kaydedildi [{kategori}]: {baslik}")
        return kayit_id

    def hatirla(
        self,
        sorgu: str,
        kategori: str = None,
        proje: str = None,
        sayi: int = 5
    ) -> list:
        """Semantik arama ile ilgili kayıtları getir"""
        embedding = self.embed(sorgu)

        result = self.db.rpc('hafiza_ara', {
            'sorgu_embedding': embedding,
            'kategori_filtre': kategori,
            'proje_filtre': proje,
            'maks_sonuc': sayi
        }).execute()

        kayitlar = result.data
        if not kayitlar:
            print(f"⚠️  '{sorgu}' için ilgili hafıza bulunamadı")
            return []

        print(f"\n📚 {len(kayitlar)} ilgili kayıt bulundu:")
        for k in kayitlar:
            print(f"\n  📌 {k['baslik']}")
            print(f"     Kategori: {k['kategori']} | "
                  f"Benzerlik: %{k['benzerlik']*100:.0f} | "
                  f"Önem: {'⭐' * k['onem']}")
            print(f"     {k['icerik'][:200]}{'...' if len(k['icerik']) > 200 else ''}")

        return kayitlar

    def claude_icin_bagłam(
        self,
        sorgu: str,
        kategori: str = None,
        proje: str = None
    ) -> str:
        """
        Claude'a gönderilecek hafıza bağlamı üretir.
        Token verimli — sadece ilgili kayıtlar.
        """
        kayitlar = self.hatirla(sorgu, kategori, proje, sayi=3)
        if not kayitlar:
            return ""

        bagłam = "## İlgili Geçmiş Kararlar\n\n"
        for k in kayitlar:
            bagłam += f"### {k['baslik']}\n"
            bagłam += f"{k['icerik']}\n\n"

        return bagłam

    def unut(self, id_veya_baslik: str) -> bool:
        """Kayıt sil — UUID veya başlık araması"""
        try:
            # UUID mi?
            import uuid
            uuid.UUID(id_veya_baslik)
            self.db.table('studio_memory')\
                .delete().eq('id', id_veya_baslik).execute()
        except ValueError:
            # Başlık araması
            self.db.table('studio_memory')\
                .delete()\
                .ilike('baslik', f'%{id_veya_baslik}%')\
                .execute()

        print(f"🗑️ Silindi: {id_veya_baslik}")
        return True

    def istatistik(self):
        """Hafıza durumu özeti"""
        result = self.db.table('studio_memory')\
            .select('kategori, count', count='exact')\
            .execute()

        toplam = result.count
        print(f"\n📊 Gök Umay Hafıza İstatistikleri")
        print(f"   Toplam kayıt: {toplam}")

        # Kategoriye göre dağılım
        for kategori in ['bug', 'mimari', 'oyun', 'kulturel', 'proje']:
            r = self.db.table('studio_memory')\
                .select('id', count='exact')\
                .eq('kategori', kategori)\
                .execute()
            if r.count > 0:
                print(f"   {kategori}: {r.count}")

# CLI kullanımı
if __name__ == '__main__':
    import sys
    mem = GokUmayMemory()
    komut = sys.argv[1] if len(sys.argv) > 1 else 'istatistik'

    if komut == 'kaydet' and len(sys.argv) >= 4:
        mem.kaydet(
            baslik=sys.argv[2],
            icerik=sys.argv[3],
            kategori=sys.argv[4] if len(sys.argv) > 4 else 'genel',
            proje=sys.argv[5] if len(sys.argv) > 5 else None
        )
    elif komut == 'hatirla' and len(sys.argv) >= 3:
        mem.hatirla(' '.join(sys.argv[2:]))
    elif komut == 'unut' and len(sys.argv) >= 3:
        mem.unut(' '.join(sys.argv[2:]))
    elif komut == 'istatistik':
        mem.istatistik()
    else:
        print("Kullanım:")
        print("  memory.py kaydet 'Başlık' 'İçerik' [kategori] [proje]")
        print("  memory.py hatirla 'Arama sorgusu'")
        print("  memory.py unut 'Başlık veya UUID'")
        print("  memory.py istatistik")
```

---

## Hazır Kayıt Şablonları

```bash
# Bug fix kaydı
python3 ~/.claude/scripts/memory_client.py kaydet \
  "Three.js raycaster mobilde çalışmıyor" \
  "Sorun: touch-action:none eklenmemişti. Çözüm: CSS'e touch-action:none; ekle, addEventListener'a passive:false ver." \
  "bug" "timurlenk"

# Mimari karar
python3 ~/.claude/scripts/memory_client.py kaydet \
  "CSP blob URL yasağı — inline AI motoru kararı" \
  "blob URL CSP tarafından engelleniyor. Çözüm: new Function() + fakeSelf mesaj yolu. Bu pattern tüm oyunlarda kullanılacak." \
  "mimari" "genel"

# Oyun tasarım kararı
python3 ~/.claude/scripts/memory_client.py kaydet \
  "Timurlenk Deve taşı değeri" \
  "Tarihi kaynaklara göre Deve (Camel) At'tan güçlü. Değer: 7 puan (At: 3, Fil: 3). Murray 1913 referansı." \
  "oyun" "timurlenk"
```
