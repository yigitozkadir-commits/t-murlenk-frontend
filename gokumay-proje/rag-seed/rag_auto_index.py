#!/usr/bin/env python3
# rag_auto_index.py — Gök Umay kritik dosyaları otomatik indeksle
# ~/.claude/scripts/rag_auto_index.py
#
# KULLANIM:
#   python3 rag_auto_index.py          → tüm kritik dosyaları indeksle
#   python3 rag_auto_index.py --force  → var olanları sil, yeniden yükle
#
# CLAUDE.md, tüm agent.md ve skill SKILL.md dosyalarını RAG'a ekler.
# Haftalık /weekly komutuyla çağrılabilir.

import os
import sys
import hashlib
from pathlib import Path
from supabase import create_client
from rag_client import indeksle  # mevcut chunk + embed mantığı

db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
EV = Path.home()

# İndekslenecek kritik dosyalar
KRITIK_DOSYALAR: list[tuple[Path, str, str]] = [
    (EV / ".claude" / "CLAUDE.md",        "claude-anayasa",  "karar"),
]

# Tüm agent'lar
AGENT_DIR = EV / ".claude" / "agents"
if AGENT_DIR.exists():
    for md in AGENT_DIR.glob("*.md"):
        KRITIK_DOSYALAR.append((md, f"agent-{md.stem}", "karar"))

# Tüm skill'ler
SKILL_DIR = EV / ".claude" / "skills"
if SKILL_DIR.exists():
    for skill_md in SKILL_DIR.glob("*/SKILL.md"):
        isim = skill_md.parent.name
        KRITIK_DOSYALAR.append((skill_md, f"skill-{isim}", "karar"))


def dosya_hash(yol: Path) -> str:
    return hashlib.md5(yol.read_bytes()).hexdigest()


def zaten_indekslendi(kaynak: str, dosya_hash_degeri: str) -> bool:
    """Bu dosyanın bu hash'i daha önce yüklendi mi?"""
    r = db.table("belgeler") \
        .select("id") \
        .eq("kaynak", kaynak) \
        .eq("meta->>dosya_hash", dosya_hash_degeri) \
        .limit(1) \
        .execute()
    return bool(r.data)


def eski_kayitlari_sil(kaynak: str):
    db.table("belgeler").delete().eq("kaynak", kaynak).execute()


def auto_index(force: bool = False):
    """Kritik dosyaları kontrol et, değişmişse yeniden indeksle."""
    toplam = 0
    atlanan = 0

    print(f"🔍 {len(KRITIK_DOSYALAR)} dosya kontrol ediliyor...\n")

    for yol, kaynak, tur in KRITIK_DOSYALAR:
        if not yol.exists():
            print(f"   ⚠️  Bulunamadı: {yol}")
            continue

        h = dosya_hash(yol)

        if not force and zaten_indekslendi(kaynak, h):
            atlanan += 1
            continue

        # Eski kayıtları temizle
        eski_kayitlari_sil(kaynak)

        # İndeksle (rag_client.indeksle hash'i meta'ya ekleyecek şekilde genişletildi)
        print(f"   📄 {kaynak} ({yol.name})")
        _indeksle_hashli(yol, kaynak, tur, h)
        toplam += 1

    print(f"\n✅ {toplam} dosya güncellendi, {atlanan} dosya atlandı (değişmemiş)")


def _indeksle_hashli(yol: Path, kaynak: str, tur: str, h: str):
    """Dosyayı chunk'lara böl, embed et, hash ile birlikte yükle."""
    from rag_client import chunk_olustur
    from embedding import embed_toplu

    metin = yol.read_text(encoding="utf-8", errors="ignore")
    chunklar = chunk_olustur(metin)
    embeddinglar = embed_toplu(chunklar)

    kayitlar = [
        {
            "kaynak": kaynak,
            "tur": tur,
            "baslik": f"{kaynak} — bölüm {i+1}/{len(chunklar)}",
            "icerik": chunk,
            "chunk_index": i,
            "meta": {
                "dosya": str(yol),
                "toplam_chunk": len(chunklar),
                "dosya_hash": h,
            },
            "embedding": emb,
        }
        for i, (chunk, emb) in enumerate(zip(chunklar, embeddinglar))
    ]

    BATCH = 10
    for i in range(0, len(kayitlar), BATCH):
        db.table("belgeler").insert(kayitlar[i:i+BATCH]).execute()


if __name__ == "__main__":
    force = "--force" in sys.argv
    if force:
        print("⚠️  Force modu — tüm kayıtlar yeniden yükleniyor\n")
    auto_index(force=force)
