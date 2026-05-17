#!/usr/bin/env python3
# reddit_manager.py — Gök Umay Reddit Yönetimi (TAM İMPLEMENTASYON)
# ~/.claude/scripts/reddit_manager.py
#
# KURULUM:
#   pip install praw anthropic --break-system-packages
#   Reddit app: https://www.reddit.com/prefs/apps (script tipi)
#   export REDDIT_CLIENT_ID="..."
#   export REDDIT_SECRET="..."
#   export REDDIT_USERNAME="..."
#   export REDDIT_PASSWORD="..."
#
# BAŞLAT: python3 reddit_manager.py izle
# ARKA PLAN: nohup python3 reddit_manager.py izle > ~/.claude/logs/reddit.log 2>&1 &

import praw
import anthropic
import os
import time
import logging
import argparse
from datetime import datetime, timedelta

# ── Loglama ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
log = logging.getLogger("gokumay-reddit")

# ── İstemciler ────────────────────────────────────────────────────────────────
reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID", ""),
    client_secret=os.environ.get("REDDIT_SECRET", ""),
    user_agent="GokUmayBot/1.0 (by u/GokUmayStudio)",
    username=os.environ.get("REDDIT_USERNAME", ""),
    password=os.environ.get("REDDIT_PASSWORD", ""),
)
claude = anthropic.Anthropic()

# ── Sabitler ──────────────────────────────────────────────────────────────────
HEDEF_SUBREDDITLER = ["chess", "boardgames", "IndieGaming", "history", "Turkey"]

ILGILI_KELIMELER = [
    "tamerlane chess", "timurid chess", "turkish chess", "ottoman chess",
    "hiashatar", "togyzool", "shatar", "şatra", "satranç varyant",
    "central asian chess", "historical chess variant", "türk oyunları",
    "orta asya oyunları", "mangala", "mancala türkiye",
]

SPAM_SAATLERI = 24        # Aynı kullanıcıya max bu kadar saatte bir cevap ver
GUNLUK_CEVAP_LIMITI = 10  # Günlük maksimum cevap sayısı

# Cevapladığımız kullanıcıları ve zamanları takip et
cevaplananlar: dict[str, datetime] = {}
gunluk_cevap_sayaci = {"tarih": datetime.now().date(), "sayi": 0}


# ── Yardımcılar ───────────────────────────────────────────────────────────────

def spam_kontrolu(kullanici: str) -> bool:
    """True = cevap verebiliriz. False = çok yakın zamanda cevapladık."""
    # Günlük limit
    if gunluk_cevap_sayaci["tarih"] != datetime.now().date():
        gunluk_cevap_sayaci.update({"tarih": datetime.now().date(), "sayi": 0})

    if gunluk_cevap_sayaci["sayi"] >= GUNLUK_CEVAP_LIMITI:
        return False

    # Kullanıcı bazlı cooldown
    if kullanici in cevaplananlar:
        gecen = datetime.now() - cevaplananlar[kullanici]
        if gecen < timedelta(hours=SPAM_SAATLERI):
            return False

    return True


def cevap_uret(yorum_metni: str, subreddit: str) -> str | None:
    """Claude ile doğal bir cevap üret. Reklam gibi görünmesin."""
    try:
        yanit = claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            system=(
                "Sen tarihi satranç ve strateji oyunları meraklısı bir geliştiricisin. "
                "Reddit yorumuna doğal, samimi, kısa cevap ver (max 3 cümle, İngilizce). "
                "Reklam yapma. Bilgi paylaş — eğer Gök Umay oyunlarıyla bağlantısı varsa "
                "sadece bir kez ve doğal biçimde bahsedebilirsin. "
                f"Subreddit: r/{subreddit}"
            ),
            messages=[{"role": "user", "content": f"Yorum:\n{yorum_metni[:500]}\n\nDoğal cevap:"}],
        )
        return yanit.content[0].text.strip()
    except Exception as e:
        log.error(f"Cevap üretilemedi: {e}")
        return None


# ── Ana İşlevler ──────────────────────────────────────────────────────────────

def yorum_izle():
    """
    Hedef subredditlerde alakalı yorumları izle ve cevapla.
    Sürekli çalışır — ctrl+c ile durdur.
    """
    log.info(f"Reddit yorumları izleniyor: {', '.join(HEDEF_SUBREDDITLER)}")
    subredditler = "+".join(HEDEF_SUBREDDITLER)

    while True:
        try:
            for yorum in reddit.subreddit(subredditler).stream.comments(skip_existing=True):
                metin = yorum.body.lower()

                # İlgili mi?
                if not any(k in metin for k in ILGILI_KELIMELER):
                    continue

                # Kendi yorumlarımıza cevap verme
                if yorum.author and yorum.author.name == os.environ.get("REDDIT_USERNAME"):
                    continue

                kullanici = str(yorum.author) if yorum.author else "unknown"

                # Spam kontrolü
                if not spam_kontrolu(kullanici):
                    log.info(f"Spam koruması: {kullanici} atlandı")
                    continue

                # Cevap üret
                cevap = cevap_uret(yorum.body, yorum.subreddit.display_name)
                if not cevap:
                    continue

                # Gönder
                try:
                    yorum.reply(cevap)
                    cevaplananlar[kullanici] = datetime.now()
                    gunluk_cevap_sayaci["sayi"] += 1
                    log.info(
                        f"✅ r/{yorum.subreddit.display_name} | "
                        f"u/{kullanici} | "
                        f"Günlük: {gunluk_cevap_sayaci['sayi']}/{GUNLUK_CEVAP_LIMITI}"
                    )
                    time.sleep(30)  # Rate limit — her cevaptan sonra 30 sn bekle
                except Exception as e:
                    log.warning(f"Yorum gönderilemedi: {e}")

        except Exception as e:
            log.error(f"Stream hatası: {e}. 60 sn sonra tekrar denenecek.")
            time.sleep(60)


def post_paylas(subreddit: str, baslik: str, icerik: str):
    """Hedef subreddite içerik paylaş."""
    try:
        gonderi = reddit.subreddit(subreddit).submit(title=baslik, selftext=icerik)
        log.info(f"✅ Post paylaşıldı: r/{subreddit} | {baslik[:50]}")
        log.info(f"   URL: https://reddit.com{gonderi.permalink}")
        return gonderi
    except Exception as e:
        log.error(f"Post paylaşılamadı (r/{subreddit}): {e}")
        return None


def haftalik_icerik_olustur(konu: str) -> dict[str, str]:
    """
    İçerik takvimi için haftalık post metni üret.
    """
    yanit = claude.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        system=(
            "Gök Umay Stüdyo geliştirici perspektifinden bir Reddit postu yaz. "
            "İngilizce, 3-5 paragraf, bilgi odaklı, reklam tonu yok. "
            "Başlık ve içerik ayrı yaz. Format: BASLIK: [...] | ICERIK: [...]"
        ),
        messages=[{"role": "user", "content": f"Konu: {konu}"}],
    )
    ham = yanit.content[0].text
    if "BASLIK:" in ham and "ICERIK:" in ham:
        baslik = ham.split("BASLIK:")[1].split("ICERIK:")[0].strip().strip("|")
        icerik = ham.split("ICERIK:")[1].strip()
    else:
        baslik = konu
        icerik = ham
    return {"baslik": baslik, "icerik": icerik}


def istatistik_goster():
    """Bu hafta yapılan gönderileri ve karma listele."""
    ben = reddit.redditor(os.environ.get("REDDIT_USERNAME", ""))
    print(f"\n📊 u/{ben.name} İstatistikleri")
    print(f"   Yorum Karma: {ben.comment_karma}")
    print(f"   Post Karma:  {ben.link_karma}")
    print(f"\nSon 5 yorum:")
    for yorum in ben.comments.new(limit=5):
        print(f"   [{yorum.score:+d}] r/{yorum.subreddit} — {yorum.body[:80]}...")


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gök Umay Reddit Yöneticisi")
    parser.add_argument(
        "komut",
        choices=["izle", "post", "istatistik"],
        help="izle: yorum akışı | post: içerik paylaş | istatistik: karma göster",
    )
    parser.add_argument("--subreddit", default="IndieGaming")
    parser.add_argument("--konu", default="Tamerlane Chess tarihi ve dijital uyarlaması")

    args = parser.parse_args()

    # Credentials kontrolü
    if not all([
        os.environ.get("REDDIT_CLIENT_ID"),
        os.environ.get("REDDIT_SECRET"),
        os.environ.get("REDDIT_USERNAME"),
        os.environ.get("REDDIT_PASSWORD"),
    ]):
        print("❌ Reddit ortam değişkenleri eksik. ~/.env kontrol et.")
        raise SystemExit(1)

    if args.komut == "izle":
        yorum_izle()

    elif args.komut == "post":
        icerik = haftalik_icerik_olustur(args.konu)
        print(f"Başlık: {icerik['baslik']}")
        print(f"İçerik önizleme: {icerik['icerik'][:200]}...")
        onay = input(f"\nr/{args.subreddit} adresine paylaş? (e/h): ")
        if onay.lower() == "e":
            post_paylas(args.subreddit, icerik["baslik"], icerik["icerik"])

    elif args.komut == "istatistik":
        istatistik_goster()
