---
name: community-manager
description: |
  Discord bot kurulumu, Reddit otomasyon, topluluk büyütme.
  discord.py ve praw şablonları, içerik takvimi.
  Kullan: "community-manager ile topluluğu büyüt"
---

# Topluluk Yönetimi

## TOKEN KURALI
Genel topluluk taktikleri değil — Gök Umay niş kitlesi için özel.

---

## Discord Bot Kurulum (Termux)

```bash
# discord.py kur
pip install discord.py aiohttp --break-system-packages

# Bot token al:
# discord.com/developers/applications → New Application
# Bot → Token → Copy

echo 'export DISCORD_BOT_TOKEN="..."' >> ~/.env
echo 'export DUYURU_KANAL_ID="..."' >> ~/.env  # Kanal ID'si (sağ tık → ID kopyala)
source ~/.env

# Test
python3 ~/.claude/scripts/discord_bot.py
```

---

## Reddit Bot Kurulum

```bash
pip install praw --break-system-packages

# Reddit App oluştur:
# reddit.com/prefs/apps → Create App → Script
# client_id ve secret al

echo 'export REDDIT_CLIENT_ID="..."' >> ~/.env
echo 'export REDDIT_SECRET="..."' >> ~/.env
echo 'export REDDIT_USERNAME="GokUmay"' >> ~/.env
echo 'export REDDIT_PASSWORD="..."' >> ~/.env
source ~/.env
```

---

## İçerik Bankası

```python
# ~/.claude/scripts/icerik_banka.py
# Hazır içerik şablonları — voice-dna sesiyle yazılmış

TARIHI_BILGILER = [
    "Timurlenk satranç varyantı 14. yüzyılda Semerkand sarayında oynandı. Teve (Deve) taşı standart satrançta yoktur — bu varyanta özgü.",
    "Hiashatar, Moğolistan'da hâlâ oynanıyor. 'Hia' kelimesi Moğolcada kalkan anlamına gelir.",
    "Togyzool'da 'Togyz' sayısı Türkçede dokuz demek. Tuva bölgesine özgü mancala varyantı.",
    "Murray 1913'te yayımladığı 'A History of Chess' kitabında Timurlenk'i belgeledi. Bu kitap hâlâ referans kaynak.",
]

GELISTIRICI_NOTLARI = [
    "Three.js raycaster'ı her karede çalıştırmak yerine sadece tıklama/dokunmada tetiklemek FPS'i %40 artırdı.",
    "Blob URL CSP tarafından bloklanıyor. Çözüm: new Function() + fakeSelf mesaj yolu.",
    "Minimax derinlik 3 masaüstünde <200ms, mobilde ~800ms. Mobil için derinlik 2 daha güvenli.",
]

SORU_BANKASI = [
    "Hangi Türk tarihi oyununun dijital versiyonunu görmek isterdiniz?",
    "11×10 Timurlenk tahtasını mı tercih edersiniz, standart 8×8'i mi?",
    "Türk satranç tarihi hakkında ne kadar biliyorsunuz?",
]
```

---

## Otomatik Yanıt Kalıpları

```python
# Sık sorulan sorular — otomatik cevap
SSS = {
    "nasıl oynuyorum": "Tarayıcında doğrudan açarsın — kurulum yok. {link}",
    "ücretli mi": "Web versiyonu tamamen ücretsiz. Mobil uygulama küçük bir ücretle gelecek.",
    "android var mı": "Yakında! Şu an tarayıcıda çalışıyor.",
    "kayıt gerekiyor mu": "Hayır — aç, oyna.",
    "kurallar nerede": "Oyun içinde '?' butonuna bas.",
    "source code": "Açık kaynak değil, ama satranç varyantının kuralları belgelenmiş.",
}

def otomatik_yanit(mesaj: str) -> str | None:
    mesaj_kucuk = mesaj.lower()
    for anahtar, cevap in SSS.items():
        if anahtar in mesaj_kucuk:
            return cevap
    return None  # Bilmiyorsa Claude'a sor
```

---

## Büyüme Taktikleri (Niş Kitle)

```
BoardGameGeek:
  ✓ Her oyun için sayfa aç (ücretsiz)
  ✓ Kuralları tam yaz — BGG wiki formatında
  ✓ "Dijital implementasyon" linkini ekle
  ✓ Tarihi kaynakları referansla (Murray, Bell)

Reddit r/chess:
  ✓ "I digitized X" formatı — viral potansiyel yüksek
  ✓ Kaynaklara referans ver — güvenilirlik
  ✓ Ekran görüntüsü + link — kısa açıklama
  ✗ Reklam gibi görünme — organik konuş

r/history + r/Turkey:
  ✓ Tarihi bağlamı öne çıkar, oyunu geri bırak
  ✓ "Bugün bu oyunu dijitale taşıdım" değil
  ✓ "14. yüzyıl Timurlu sarayında oynanan oyunu araştırırken..."

YouTube (uzun vadeli):
  ✓ "Tarihi Türk oyunları" playlist
  ✓ Her oyun için 3-5 dakika tanıtım
  ✓ SEO: "tamerlane chess", "türk strateji oyunu"
```

---

## Haftalık Görev Takvimi

```
PAZARTESİ:
  [ ] Discord haftalık mesaj (otomatik)
  [ ] Reddit tarihi bilgi paylaşımı

ÇARŞAMBA:
  [ ] Geliştirici günlüğü (Discord + Reddit)
  [ ] BoardGameGeek güncelleme (varsa)

CUMA:
  [ ] Topluluk sorusu / oylama
  [ ] Reddit r/IndieGaming (haftada bir)

PAZAR:
  [ ] Yorum + mesaj yanıtları gözden geçir
  [ ] Bir sonraki haftanın içeriğini hazırla
```
