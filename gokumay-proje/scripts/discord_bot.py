#!/usr/bin/env python3
# discord_bot.py — Gök Umay Discord Botu (TAM İMPLEMENTASYON)
# ~/.claude/scripts/discord_bot.py
#
# KURULUM:
#   pip install discord.py aiohttp anthropic --break-system-packages
#   export DISCORD_BOT_TOKEN="..."
#   export DUYURU_KANAL_ID="..."
#   export N8N_URL="http://localhost:5678"
#
# BAŞLAT: python3 discord_bot.py
# ARKA PLAN: nohup python3 discord_bot.py > ~/.claude/logs/discord.log 2>&1 &

import discord
from discord.ext import commands, tasks
import anthropic
import aiohttp
import os
import logging
from datetime import datetime, time, timezone

# ── Loglama ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
log = logging.getLogger("gokumay-bot")

# ── İstemciler ────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
claude = anthropic.Anthropic()

# ── Sabitler ─────────────────────────────────────────────────────────────────
CLAUDE_MODEL = "claude-haiku-4-5"  # Topluluk sorguları için Haiku — ucuz
N8N_URL = os.environ.get("N8N_URL", "http://localhost:5678")
DUYURU_KANAL_ID = int(os.environ.get("DUYURU_KANAL_ID", "0"))


# ── Yardımcılar ───────────────────────────────────────────────────────────────

def kanal_bul(guild: discord.Guild, isim: str) -> discord.TextChannel | None:
    return discord.utils.get(guild.text_channels, name=isim)


async def n8n_tetikle(webhook: str, veri: dict) -> bool:
    """n8n webhook'u çağır. Başarılıysa True döner."""
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.post(
                f"{N8N_URL}/webhook/{webhook}",
                json=veri,
                timeout=aiohttp.ClientTimeout(total=8),
            )
            return r.status < 400
    except Exception as e:
        log.warning(f"n8n webhook hatası ({webhook}): {e}")
        return False


# ── Etkinlikler ───────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    log.info(f"✅ Bot aktif: {bot.user} | {len(bot.guilds)} sunucu")
    haftalik_mesaj.start()
    log.info("⏰ Haftalık mesaj döngüsü başladı")


@bot.event
async def on_member_join(member: discord.Member):
    """Yeni üyeye hoş geldin mesajı."""
    kanal = kanal_bul(member.guild, "genel")
    if not kanal:
        return
    await kanal.send(
        f"Hoş geldin {member.mention}! 🏹\n"
        "Gök Umay Stüdyo'ya katıldın — Türk ve Orta Asya oyunlarını dijitale taşıyoruz.\n"
        "`!yardim` ile başlayabilirsin."
    )
    log.info(f"Yeni üye: {member.name}")


# ── Komutlar ──────────────────────────────────────────────────────────────────

@bot.command(name="yardim")
async def yardim(ctx: commands.Context):
    """!yardim → Komut listesi."""
    embed = discord.Embed(
        title="🏹 Gök Umay Bot Komutları",
        color=0x5B4A8A,
    )
    embed.add_field(name="!bug [açıklama]", value="Bug raporu gönder", inline=False)
    embed.add_field(name="!sor [soru]", value="Tarihi oyun sorusu sor", inline=False)
    embed.add_field(name="!trivia", value="Tarihi trivia sorusu", inline=False)
    embed.add_field(name="!oy [oyun adı]", value="Sonraki oyun için oy ver", inline=False)
    embed.add_field(name="!durum", value="Bot durum kontrolü", inline=False)
    embed.set_footer(text="Gök Umay Oyun Stüdyosu")
    await ctx.send(embed=embed)


@bot.command(name="bug")
async def bug_raporu(ctx: commands.Context, *, aciklama: str):
    """!bug [açıklama] → Yapılandırılmış bug raporu oluştur."""
    embed = discord.Embed(title="🐛 Yeni Bug Raporu", color=0x8B1A1A)
    embed.add_field(name="Açıklama", value=aciklama[:1000], inline=False)
    embed.add_field(name="Raporlayan", value=ctx.author.mention, inline=True)
    embed.add_field(name="Tarih", value=discord.utils.utcnow().strftime("%d.%m.%Y %H:%M"), inline=True)
    embed.add_field(name="Kanal", value=ctx.channel.name, inline=True)
    embed.set_footer(text="Durum: İnceleniyor")

    # #bug-raporları kanalına ilet
    bug_kanal = kanal_bul(ctx.guild, "bug-raporları")
    if bug_kanal and bug_kanal != ctx.channel:
        await bug_kanal.send(embed=embed)
        await ctx.reply("✅ Bug raporu #bug-raporları kanalına iletildi.", mention_author=False)
    else:
        await ctx.send(embed=embed)

    # n8n üzerinden GitHub issue aç (varsa)
    basari = await n8n_tetikle("discord-bug", {
        "aciklama": aciklama,
        "kullanici": str(ctx.author),
        "kullanici_id": ctx.author.id,
        "tarih": discord.utils.utcnow().isoformat(),
    })
    if basari:
        log.info(f"Bug n8n'e iletildi: {ctx.author} — {aciklama[:60]}")


@bot.command(name="sor")
async def soru_cevap(ctx: commands.Context, *, soru: str):
    """!sor [soru] → Tarihi oyun sorusu sor."""
    async with ctx.typing():
        try:
            yanit = claude.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=300,
                system=(
                    "Sen Gök Umay Stüdyo'nun Discord asistanısın. "
                    "Türk ve Orta Asya tarihi oyunları (Timurlenk Satranç, Şatra, "
                    "Togyzool, Hiashatar) hakkında kısa, doğru, samimi cevaplar verirsin. "
                    "Türkçe yaz. 3 cümleyi geçme. Emin olmadığın bilgiyi uydurma."
                ),
                messages=[{"role": "user", "content": soru}],
            )
            await ctx.reply(yanit.content[0].text, mention_author=False)
        except Exception as e:
            await ctx.reply("Şu an cevap veremiyorum, daha sonra tekrar dene.", mention_author=False)
            log.error(f"!sor hatası: {e}")


@bot.command(name="trivia")
async def trivia(ctx: commands.Context):
    """!trivia → Türk oyun tarihi trivia sorusu."""
    async with ctx.typing():
        try:
            yanit = claude.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=200,
                system=(
                    "Türk ve Orta Asya oyun tarihi hakkında tek bir trivia sorusu üret. "
                    "Format: 'Soru: [...] || Cevap: [...]' "
                    "Kısa, eğlenceli, doğrulanabilir bir gerçek olsun."
                ),
                messages=[{"role": "user", "content": "Yeni trivia sorusu üret."}],
            )
            ham = yanit.content[0].text
            if "||" in ham:
                soru_kismi, cevap_kismi = ham.split("||", 1)
                embed = discord.Embed(title="🎯 Tarihi Trivia", color=0x5B4A8A)
                embed.add_field(name="Soru", value=soru_kismi.replace("Soru:", "").strip(), inline=False)
                embed.add_field(name="Cevap", value=f"|| {cevap_kismi.replace('Cevap:', '').strip()} ||", inline=False)
                embed.set_footer(text="|| ile gösterilen cevabı görmek için tıkla")
                await ctx.send(embed=embed)
            else:
                await ctx.send(ham)
        except Exception as e:
            await ctx.send("Trivia üretilemedi, daha sonra dene.")
            log.error(f"!trivia hatası: {e}")


@bot.command(name="oy")
async def oylama(ctx: commands.Context, *, oyun_adi: str):
    """!oy [oyun adı] → Sonraki oyun için oy ver."""
    embed = discord.Embed(
        title=f"🗳️ Sonraki oyun: {oyun_adi}?",
        description="Oy vermek için reaksiyon ekle!",
        color=0x5B4A8A,
    )
    embed.set_footer(text=f"Öneren: {ctx.author.display_name}")
    mesaj = await ctx.send(embed=embed)
    await mesaj.add_reaction("✅")
    await mesaj.add_reaction("❌")


@bot.command(name="durum")
async def durum(ctx: commands.Context):
    """!durum → Bot sağlık kontrolü."""
    embed = discord.Embed(title="📊 Bot Durumu", color=0x00AA00)
    embed.add_field(name="Bot", value="✅ Çalışıyor", inline=True)
    embed.add_field(name="Gecikme", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Sunucu", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="n8n", value=N8N_URL, inline=False)
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)


# ── Zamanlanmış Görevler ──────────────────────────────────────────────────────

@tasks.loop(hours=168)  # Haftada bir — Pazartesi sabahı
async def haftalik_mesaj():
    """Her Pazartesi otomatik motivasyon mesajı."""
    if not DUYURU_KANAL_ID:
        return

    kanal = bot.get_channel(DUYURU_KANAL_ID)
    if not kanal:
        log.warning("Duyuru kanalı bulunamadı (DUYURU_KANAL_ID kontrol et)")
        return

    try:
        yanit = claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=150,
            system=(
                "Gök Umay Discord topluluğu için Pazartesi sabahı açılış mesajı yaz. "
                "Kısa (2-3 cümle), samimi, Türkçe. "
                "Türk oyun tarihi veya geliştirme süreciyle bağlantılı bir not ekle."
            ),
            messages=[{"role": "user", "content": "Pazartesi mesajı"}],
        )
        await kanal.send(f"🏹 **Yeni Hafta!**\n{yanit.content[0].text}")
        log.info("Haftalık mesaj gönderildi")
    except Exception as e:
        log.error(f"Haftalık mesaj hatası: {e}")


@haftalik_mesaj.before_loop
async def haftalik_mesaj_bekle():
    await bot.wait_until_ready()


# ── Başlat ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN ortam değişkeni eksik")
        print("   export DISCORD_BOT_TOKEN='...' >> ~/.env")
        raise SystemExit(1)
    log.info("Gök Umay Discord Botu başlatılıyor...")
    bot.run(token, log_handler=None)
