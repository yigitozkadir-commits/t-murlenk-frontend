---
name: n8n-workflows
description: |
  n8n node yapıları, webhook kurulumu, Gök Umay workflow şablonları.
  Termux'ta kurulum ve MCP bağlantısı.
  Kullan: "n8n-workflows ile bu workflow'u kur"
---

# n8n Workflow Şablonları

## TOKEN KURALI
Tam JSON verme — node listesi + bağlantı yapısı + webhook URL.

---

## Termux Kurulum

```bash
# Kurulum (tek seferlik)
npm install -g n8n

# Başlatma
n8n start --port 5678

# Arka plan (Termux'ta)
nohup n8n start > ~/.n8n/n8n.log 2>&1 &
echo $! > ~/.n8n/n8n.pid

# Durdurma
kill $(cat ~/.n8n/n8n.pid)

# Erişim
# Telefon tarayıcısı: http://localhost:5678
# Bilgisayardan (aynı wifi): http://[telefon-ip]:5678
```

---

## MCP Bağlantısı

```bash
# n8n API key al
# http://localhost:5678 → Settings → API → Create API Key

# Claude Code'a ekle
claude mcp add n8n-mcp \
  --transport stdio \
  -- npx -y n8n-mcp-server \
  --n8n-url http://localhost:5678 \
  --n8n-api-key YOUR_KEY_HERE

# Test
claude "n8n'deki workflow'ları listele"
```

---

## Kritik Node Tipleri

```
Tetikleyiciler:
  Webhook          → HTTP POST aldığında başla
  Cron             → Zamanlanmış çalıştır
  GitHub Trigger   → Push/PR/Release'de başla
  File Trigger     → Dosya değiştiğinde başla

İşlem:
  HTTP Request     → Herhangi bir API çağrısı
  Code             → JavaScript/Python çalıştır
  Set              → Değişken ata
  IF               → Koşul dallandırma
  Switch           → Çoklu dal

Bildirim:
  Telegram         → Bot mesajı gönder
  Discord          → Webhook ile mesaj
  Email (Gmail)    → E-posta gönder

Veri:
  Supabase         → Tablo okuma/yazma
  GitHub           → API işlemleri
  HTTP Request     → REST API
```

---

## Self-Healing Workflow Kurulumu

```
1. n8n'de yeni workflow oluştur: "Gök Umay Self-Healing"

2. Node 1: Webhook (tetikleyici)
   → URL: http://localhost:5678/webhook/hata-bildirimi
   → Method: POST
   → Authentication: Header Auth

3. Node 2: Code (hata mesajını formatla)
   const hata = $input.first().json;
   return [{
     json: {
       mesaj: `⚠️ Workflow Hatası\n📌 ${hata.workflowName}\n❌ ${hata.error}\n⏰ ${new Date().toLocaleString('tr-TR')}`
     }
   }];

4. Node 3: Telegram (bildirim gönder)
   → Bot Token: BotFather'dan al
   → Chat ID: kendi chat ID'n
   → Message: {{ $json.mesaj }}
   → Reply Markup: Inline Keyboard
     [{ text: "🔧 Claude ile Düzelt", callback_data: "fix" }]

5. Node 4: IF (buton tıklandıysa)
   → Condition: callback_data == "fix"

6. Node 5: Code (Claude Code'u tetikle)
   const { execSync } = require('child_process');
   execSync(`claude --headless "$(cat ~/.claude/commands/fix.md)" \
     --file ${$json.workflowFile}`, {stdio: 'inherit'});

7. Node 6: Telegram (tamamlandı bildirimi)
   → "✅ Düzeltildi!"
```

---

## Cron Zamanlamaları

```
Dakika Saat  Gün  Ay   Haftanın_Günü
─────────────────────────────────────
0      9    *    *    1           → Pazartesi 09:00 (haftalık rapor)
0      20   *    *    *           → Her gece 20:00 (itch.io takip)
0      2    *    *    *           → Her gece 02:00 (yedekleme)
0      10   *    *    3           → Çarşamba 10:00 (içerik takvimi)
*/30   *    *    *    *           → Her 30 dakika (Sentry kontrol)
```

---

## Ortam Değişkenleri

```bash
# ~/.env — n8n başlarken yükle
export N8N_API_KEY="..."
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
export DISCORD_WEBHOOK_URL="..."
export GITHUB_TOKEN="..."
export SUPABASE_URL="..."
export SUPABASE_KEY="..."
export ITCH_API_KEY="..."
export SENTRY_DSN="..."

# n8n başlatma scripti
source ~/.env && n8n start
```

---

## Hata Ayıklama

```bash
# n8n logları
tail -f ~/.n8n/n8n.log

# Belirli workflow'u manuel tetikle
curl -X POST http://localhost:5678/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# n8n durumu
curl http://localhost:5678/healthz
```
