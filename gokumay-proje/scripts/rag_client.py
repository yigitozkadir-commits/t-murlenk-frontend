#!/usr/bin/env python3
# rag_client.py — Gök Umay Stüdyo (DÜZELTİLMİŞ)
# Değişiklik: embed() placeholder → embedding.py modülü
# Chunk boyutunu Voyage AI boyutuna (1024) göre ayarla

import os
import sys
from pathlib import Path
from supabase import create_client
from embedding import embed, embed_toplu  # ← GERÇEK EMBEDDING

db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

CHUNK_BOYUT = 600   # token tahmini: karakter / 4
CHUNK_CAKISMA = 50  # ardışık chunklar arasında bağlam sürekliliği


def chunk_olustur(metin: str) -> list[str]:
    """Metni örtüşen chunk'lara böl."""
    kelimeler = metin.split()
    chunklar = []
    i = 0
    while i < len(kelimeler):
        chunk = " ".join(kelimeler[i:i + CHUNK_BOYUT])
        chunklar.append(chunk)
        i += CHUNK_BOYUT - CHUNK_CAKISMA
    return chunklar


def indeksle(dosya_yolu: str, kaynak: str = None, tur: str = "belge"):
    """Dosyayı okuyup chunk'lara böl, tümünü pgvector'e yükle."""
    yol = Path(dosya_yolu)
    metin = yol.read_text(encoding="utf-8")
    kaynak = kaynak or yol.stem
    chunklar = chunk_olustur(metin)

    print(f"📄 {kaynak}: {len(chunklar)} chunk oluşturuldu")

    # Toplu embedding — tek API çağrısı (maliyet optimizasyonu)
    embeddinglar = embed_toplu(chunklar)

    kayitlar = [
        {
            "kaynak": kaynak,
            "tur": tur,
            "baslik": f"{kaynak} — bölüm {i+1}/{len(chunklar)}",
            "icerik": chunk,
            "chunk_index": i,
            "meta": {"dosya": str(yol), "toplam_chunk": len(chunklar)},
            "embedding": emb,
        }
        for i, (chunk, emb) in enumerate(zip(chunklar, embeddinglar))
    ]

    db.table("belgeler").insert(kayitlar).execute()
    print(f"✅ {len(kayitlar)} chunk yüklendi → {kaynak}")


def ara(sorgu: str, tur: str = None, kaynak: str = None, sayi: int = 5):
    """Semantik arama — ilgili chunk'ları getir."""
    emb = embed(sorgu)
    sonuclar = db.rpc("belge_ara", {
        "sorgu_embedding": emb,
        "tur_filtre": tur,
        "kaynak_filtre": kaynak,
        "maks_sonuc": sayi,
    }).execute()

    for s in sonuclar.data:
        print(f"\n📚 [{s['kaynak']}] {s['baslik']} ({s['benzerlik']:.0%})")
        print(f"   {s['icerik'][:300]}")
    return sonuclar.data


if __name__ == "__main__":
    komut = sys.argv[1] if len(sys.argv) > 1 else "yardim"
    if komut == "indeksle" and len(sys.argv) >= 3:
        indeksle(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif komut == "ara":
        ara(" ".join(sys.argv[2:]))
    else:
        print("Kullanım: rag_client.py [indeksle <dosya> [kaynak] | ara <sorgu>]")
