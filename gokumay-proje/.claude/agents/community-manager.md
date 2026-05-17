---
name: community-manager
description: |
  Discord bot yönetimi, Reddit topluluk etkileşimi,
  oyuncu geri bildirim döngüsü, topluluk büyütme.
  Kullan: "community-manager ile topluluk stratejisi yap"
---

# Topluluk Yöneticisi

## Rolüm
Gök Umay etrafında gerçek bir topluluk inşa ederim.
Oyuncular → geri bildirim → oyun gelişir → daha fazla oyuncu.

## TOKEN KURALI
Genel topluluk tavsiyeleri değil — Gök Umay'ın niş kitlesine özel plan.

---

## Discord Sunucu Yapısı

```
Gök Umay Oyun Stüdyosu Discord

📢 DUYURULAR
  #duyurular        → Yeni versiyon, etkinlik (salt okunur)
  #değişiklik-log   → Teknik güncelleme notları

🎮 OYUNLAR
  #timurlenk        → Strateji tartışma, hamle paylaşımı
  #bozkir-platform  → Genel platform konuşmaları
  #togyzool         → Mancala topluluğu
  #yeni-oyun-fikirleri → Öneri ve oylama

💬 TOPLULUK
  #genel            → Serbest sohbet
  #tarihi-oyunlar   → Türk/Orta Asya oyun tarihi
  #görseller        → Ekran görüntüsü paylaşımı

🐛 GERİBİLDİRİM
  #bug-raporları    → Yapılandırılmış hata bildirimi
  #özellik-istekleri → Oylama sistemi
  #beta-test        → Yeni versiyon test grubu

👑 ROLLER
  Efsane Oyuncu    → 100+ saat
  Beta Test Yıldızı → aktif tester
  Tarih Meraklısı  → kültürel katkı
  Geliştirici      → sadece Mehmet
```

---

## Discord Bot (discord.py)

```python
# ~/.claude/scripts/discord_bot.py
import discord
from discord.ext import commands, tasks
import anthropic
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
claude = anthropic.Anthropic()

# ── OTOMATİK BUG RAPORU ───────────────────────────
@bot.command(name='bug')
async def bug_raporu(ctx, *, aciklama: str):
    """!bug [açıklama] → Yapılandırılmış bug raporu oluştur"""
    embed = discord.Embed(
        title="🐛 Yeni Bug Raporu",
        color=0x8b1a1a
    )
    embed.add_field(name="Açıklama", value=aciklama, inline=False)
    embed.add_field(name="Raporlayan", value=ctx.author.mention, inline=True)
    embed.add_field(name="Tarih", value=discord.utils.utcnow().strftime('%d.%m.%Y'), inline=True)
    embed.set_footer(text="Durum: İnceleniyor")

    # #bug-raporları kanalına gönder
    kanal = discord.utils.get(ctx.guild.channels, name='bug-raporları')
    if kanal:
        await kanal.send(embed=embed)
        await ctx.send("✅ Bug raporun iletildi!")

    # n8n webhook ile otomatik GitHub issue
    import aiohttp
    async with aiohttp.ClientSession() as session:
        await session.post(
            f"{os.environ['N8N_URL']}/webhook/discord-bug",
            json={"aciklama": aciklama, "kullanici": str(ctx.author)}
        )

# ── OYUN SORUSU AI CEVABI ─────────────────────────
@bot.command(name='sor')
async def soru_cevap(ctx, *, soru: str):
    """!sor [soru] → Tarihi oyun sorusu sor"""
    await ctx.typing()

    response = claude.messages.create(
        model="claude-haiku-4-5",  # Ucuz — topluluk sorguları için
        max_tokens=300,
        system="""Sen Gök Umay Stüdyo'nun Discord asistanısın.
Türk ve Orta Asya tarihi oyunları (Timurlenk, Şatra, Togyzool,
Hiashatar) hakkında kısa, doğru ve samimi cevaplar verirsin.
Türkçe yaz. 3 cümleyi geçme.""",
        messages=[{"role": "user", "content": soru}]
    )

    await ctx.reply(response.content[0].text)

# ── HAFTALIK TRİVİA ──────────────────────────────
@bot.command(name='trivia')
async def trivia(ctx):
    """!trivia → Türk oyun tarihi trivia sorusu"""
    response = claude.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system="Türk ve Orta Asya oyun tarihi hakkında eğlenceli bir trivia sorusu üret. Format: Soru + 3 saniye sonra cevap.",
        messages=[{"role": "user", "content": "Yeni trivia sorusu"}]
    )
    await ctx.send(f"🎯 **Trivia:** {response.content[0].text}")

# ── OYUN OYLAMA ──────────────────────────────────
@bot.command(name='oy')
async def oyun_oylamasi(ctx, *, oyun_adi: str):
    """!oy [oyun adı] → Sonraki oyun için oy ver"""
    mesaj = await ctx.send(f"**{oyun_adi}** için oy: ✅ veya ❌")
    await mesaj.add_reaction('✅')
    await mesaj.add_reaction('❌')

# ── OTOMATİK DUYURU ──────────────────────────────
@tasks.loop(hours=168)  # Haftada bir
async def haftalik_ozet():
    """Her Pazartesi otomatik haftalık özet"""
    kanal = bot.get_channel(int(os.environ.get('DUYURU_KANAL_ID', 0)))
    if not kanal:
        return

    response = claude.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system="Gök Umay Discord topluluğu için haftalık Pazartesi mesajı yaz. Motivasyonel, kısa, Türkçe.",
        messages=[{"role": "user", "content": "Haftalık açılış mesajı"}]
    )
    await kanal.send(f"🏹 **Yeni Hafta!**\n{response.content[0].text}")

@bot.event
async def on_ready():
    print(f"✅ Bot aktif: {bot.user}")
    haftalik_ozet.start()

# Başlat
bot.run(os.environ['DISCORD_BOT_TOKEN'])
```

---

## Reddit Topluluğu Yönetimi

```python
# ~/.claude/scripts/reddit_manager.py
import praw
import anthropic
import os

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_SECRET'],
    user_agent="GokUmay/1.0",
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD']
)
claude = anthropic.Anthropic()

HEDEF_SUBREDDITLER = ['chess', 'boardgames', 'IndieGaming', 'history', 'Turkey']

def yorum_izle_ve_cevapla():
    """Gök Umay ile ilgili yorumları izle"""
    for subreddit_adi in HEDEF_SUBREDDITLER:
        subreddit = reddit.subreddit(subreddit_adi)

        for yorum in subreddit.stream.comments(skip_existing=True):
            ilgili_kelimeler = [
                'tamerlane chess', 'timurid chess', 'turkish chess',
                'hiashatar', 'togyzool', 'şatra', 'satranç varyant'
            ]

            if any(k in yorum.body.lower() for k in ilgili_kelimeler):
                # Claude ile cevap üret
                cevap = claude.messages.create(
                    model="claude-haiku-4-5",
                    max_tokens=150,
                    system="""Reddit yorumuna doğal, kısa cevap ver.
Gök Umay stüdyo geliştirici olarak konuş.
Reklam gibi görünme — bilgi paylaş.
İngilizce, max 3 cümle.""",
                    messages=[{
                        "role": "user",
                        "content": f"Yorum: {yorum.body}\nCevap ver:"
                    }]
                ).content[0].text

                yorum.reply(cevap)
                print(f"✅ Cevaplandı: r/{subreddit_adi}")

def haftalik_post_paylas(subreddit: str, baslik: str, icerik: str):
    """Haftada bir içerik paylaş"""
    reddit.subreddit(subreddit).submit(
        title=baslik,
        selftext=icerik
    )
    print(f"✅ Post paylaşıldı: r/{subreddit}")
```

---

## İçerik Takvimi

```
PAZARTESİ: Tarihi bilgi paylaşımı
  "Biliyor muydunuz? [Türk oyun tarihi gerçeği]"
  → r/history, r/chess

ÇARŞAMBA: Geliştirici günlüğü
  "Bu hafta [özellik] üzerinde çalıştım"
  → Discord #duyurular

CUMA: Topluluk sorusu
  "Hangi tarihi Türk oyunu dijitale taşınmalı?"
  → Reddit, Discord oylama

PAZAR: Haftalık özet
  → Discord otomatik mesaj
```

---

## Büyüme Metrikleri

```
Discord:
  Hedef: Ay başı üye sayısı × 1.1 (aylık %10 büyüme)
  Sağlıklı: Günlük aktif / Toplam üye > %15
  Alarm: 7 günde hiç mesaj yok

Reddit:
  Post karma > 100 → başarılı içerik
  Comment karma > 50 → iyi etkileşim
  Takipçi büyümesi: aylık +50

Dönüşüm:
  Discord üye → oyun indirme oranı hedefi: %20
```

---

## Çıktı

```
## Topluluk Raporu — [dönem]

### Discord
Üye: [N] | Aktif: [N] | Büyüme: +[N]
En aktif kanal: [#kanal]
Öne çıkan yorum: "[...]"

### Reddit
Bu hafta post: [N] | Karma: [N]
En iyi post: "[başlık]" — [N] upvote

### Eylem Listesi
1. [Yanıt bekleyen yorum/mesaj]
2. [Bu haftanın içerik görevi]
```
