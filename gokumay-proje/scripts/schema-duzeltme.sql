-- schema-duzeltme.sql
-- Embedding boyut düzeltmesi
-- Voyage AI → 1024 boyut / OpenAI → 1536 boyut
--
-- KURULUM ÖNCE: embedding.py'de PROVIDER değişkenini kontrol et
-- Sonra bu dosyayı Supabase SQL Editor'de çalıştır

-- ── Voyage AI kullanıyorsan (varsayılan) ─────────────────────────────────────

-- Mevcut tabloları sil ve yeniden oluştur (ilk kurulumda)
-- UYARI: Veri varsa önce yedekle!

ALTER TABLE studio_memory
  ALTER COLUMN embedding TYPE vector(1024);

ALTER TABLE belgeler
  ALTER COLUMN embedding TYPE vector(1024);

-- Index'leri yeniden oluştur
DROP INDEX IF EXISTS studio_memory_embedding_idx;
CREATE INDEX studio_memory_embedding_idx
  ON studio_memory
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

DROP INDEX IF EXISTS belgeler_embedding_idx;
CREATE INDEX belgeler_embedding_idx
  ON belgeler
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- Arama fonksiyonlarını güncelle
CREATE OR REPLACE FUNCTION hafiza_ara(
  sorgu_embedding vector(1024),   -- ← 1024
  kategori_filtre text DEFAULT NULL,
  eslesme_sayisi  int  DEFAULT 5
)
RETURNS TABLE (
  id uuid, baslik text, icerik text,
  etiketler text[], benzerlik float
)
LANGUAGE sql STABLE AS $$
  SELECT id, baslik, icerik, etiketler,
    1 - (embedding <=> sorgu_embedding) AS benzerlik
  FROM studio_memory
  WHERE
    (kategori_filtre IS NULL OR kategori = kategori_filtre)
    AND 1 - (embedding <=> sorgu_embedding) > 0.7
  ORDER BY embedding <=> sorgu_embedding
  LIMIT eslesme_sayisi;
$$;

CREATE OR REPLACE FUNCTION belge_ara(
  sorgu_embedding vector(1024),   -- ← 1024
  tur_filtre      text  DEFAULT NULL,
  kaynak_filtre   text  DEFAULT NULL,
  min_benzerlik   float DEFAULT 0.6,
  maks_sonuc      int   DEFAULT 5
)
RETURNS TABLE (
  kaynak text, baslik text, icerik text,
  tur text, meta jsonb, benzerlik float
)
LANGUAGE sql STABLE AS $$
  SELECT kaynak, baslik, icerik, tur, meta,
    1 - (embedding <=> sorgu_embedding) AS benzerlik
  FROM belgeler
  WHERE
    (tur_filtre    IS NULL OR tur    = tur_filtre)
    AND (kaynak_filtre IS NULL OR kaynak = kaynak_filtre)
    AND 1 - (embedding <=> sorgu_embedding) > min_benzerlik
  ORDER BY embedding <=> sorgu_embedding
  LIMIT maks_sonuc;
$$;

-- ── OpenAI kullanıyorsan aşağıdaki komutu çalıştır ───────────────────────────
-- ALTER TABLE studio_memory ALTER COLUMN embedding TYPE vector(1536);
-- ALTER TABLE belgeler ALTER COLUMN embedding TYPE vector(1536);
-- (fonksiyonlarda da 1536 yaz)
