#!/usr/bin/env python3
# embedding.py — Gök Umay Stüdyo
# Gerçek embedding API — memory.py ve rag_client.py bu modülü kullanır
#
# KURULUM:
#   pip install voyageai --break-system-packages
#   echo 'export VOYAGE_API_KEY="pa-..."' >> ~/.env
#
# ALTERNATIF (OpenAI):
#   pip install openai --break-system-packages
#   echo 'export OPENAI_API_KEY="sk-..."' >> ~/.env
#   EMBED_PROVIDER=openai python3 embedding.py test

import os
import sys
import json
from typing import Union

PROVIDER = os.environ.get("EMBED_PROVIDER", "voyage")  # voyage | openai


def embed(metin: str) -> list[float]:
    """
    Metni 1024 veya 1536 boyutlu vektöre çevir.
    Voyage AI varsayılan — daha ucuz, Türkçe desteği iyi.
    """
    metin = metin[:8000]  # Max token güvenliği

    if PROVIDER == "voyage":
        return _voyage_embed(metin)
    elif PROVIDER == "openai":
        return _openai_embed(metin)
    else:
        raise ValueError(f"Bilinmeyen provider: {PROVIDER}")


def embed_toplu(metinler: list[str], batch: int = 32) -> list[list[float]]:
    """
    Çok sayıda metni toplu embed et — API çağrı sayısını azaltır.
    Büyük RAG indekslemesi için kullan.
    """
    sonuclar = []
    for i in range(0, len(metinler), batch):
        grup = metinler[i:i + batch]
        if PROVIDER == "voyage":
            sonuclar.extend(_voyage_embed_toplu(grup))
        else:
            sonuclar.extend([_openai_embed(m) for m in grup])
    return sonuclar


# ── Voyage AI ─────────────────────────────────────────────────────────────────

def _voyage_embed(metin: str) -> list[float]:
    """
    voyage-3-lite — en ucuz, 1024 boyut, Türkçe + İngilizce iyi.
    Fiyat: $0.02 / 1M token (OpenAI'nin 1/3'ü)
    """
    import voyageai
    client = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
    sonuc = client.embed([metin], model="voyage-3-lite", input_type="document")
    return sonuc.embeddings[0]


def _voyage_embed_toplu(metinler: list[str]) -> list[list[float]]:
    import voyageai
    client = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
    sonuc = client.embed(metinler, model="voyage-3-lite", input_type="document")
    return sonuc.embeddings


# ── OpenAI ────────────────────────────────────────────────────────────────────

def _openai_embed(metin: str) -> list[float]:
    """
    text-embedding-3-small — 1536 boyut.
    Fiyat: $0.02 / 1M token
    NOT: Supabase şemasında vector(1536) kullanılmalı.
    """
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    sonuc = client.embeddings.create(
        input=metin,
        model="text-embedding-3-small"
    )
    return sonuc.data[0].embedding


# ── Supabase Boyut Uyumu ───────────────────────────────────────────────────────

BOYUT = {
    "voyage": 1024,
    "openai": 1536,
}

def boyut_al() -> int:
    """Aktif provider'ın vektör boyutunu döndür."""
    return BOYUT.get(PROVIDER, 1024)


# ── CLI Test ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    komut = sys.argv[1] if len(sys.argv) > 1 else "test"

    if komut == "test":
        print(f"Provider: {PROVIDER}")
        v = embed("Timurlenk satranç oyununda Deve taşı nasıl hareket eder?")
        print(f"Boyut: {len(v)}")
        print(f"İlk 5 değer: {v[:5]}")
        print("✅ Embedding çalışıyor")

    elif komut == "boyut":
        print(boyut_al())
