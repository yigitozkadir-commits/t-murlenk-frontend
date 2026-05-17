#!/usr/bin/env python3
# memory.py — Gök Umay Stüdyo (DÜZELTİLMİŞ)
# Değişiklik: embed() placeholder → embedding.py modülü
#
# KURULUM: pip install supabase voyageai --break-system-packages
# ÇALIŞTIR: python3 memory.py kaydet "Başlık" "İçerik" bug timurlenk

import os
import sys
from supabase import create_client
from embedding import embed  # ← GERÇEk EMBEDDING

db = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"]
)


def kaydet(baslik, icerik, kategori="genel", etiketler=None, proje=None, onem=3):
    embedding = embed(f"{baslik}\n{icerik}")
    db.table("studio_memory").insert({
        "kategori": kategori,
        "baslik": baslik,
        "icerik": icerik,
        "etiketler": etiketler or [],
        "proje": proje,
        "onem": onem,
        "embedding": embedding,
    }).execute()
    print(f"✅ Kaydedildi: {baslik}")


def hatirla(sorgu, kategori=None, sayi=5):
    embedding = embed(sorgu)
    sonuclar = db.rpc("hafiza_ara", {
        "sorgu_embedding": embedding,
        "kategori_filtre": kategori,
        "eslesme_sayisi": sayi,
    }).execute()
    for k in sonuclar.data:
        print(f"\n📌 {k['baslik']} ({k['benzerlik']:.0%})")
        print(f"   {k['icerik'][:200]}")
    return sonuclar.data


def unut(baslik_arama):
    db.table("studio_memory").delete().ilike("baslik", f"%{baslik_arama}%").execute()
    print(f"🗑️  Silindi: {baslik_arama}")


if __name__ == "__main__":
    komut = sys.argv[1] if len(sys.argv) > 1 else "yardim"
    if komut == "kaydet" and len(sys.argv) >= 4:
        kaydet(
            sys.argv[2], sys.argv[3],
            sys.argv[4] if len(sys.argv) > 4 else "genel",
            proje=sys.argv[5] if len(sys.argv) > 5 else None,
        )
    elif komut == "hatirla":
        hatirla(" ".join(sys.argv[2:]))
    elif komut == "unut":
        unut(" ".join(sys.argv[2:]))
    else:
        print("Kullanım: memory.py [kaydet|hatirla|unut] [args]")
