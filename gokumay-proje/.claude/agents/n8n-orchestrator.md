---
name: n8n-orchestrator
description: |
  n8n workflow tasarımı, MCP entegrasyonu, self-healing otomasyon.
  Claude Code + n8n birlikte çalışma koordinasyonu.
  Kullan: "n8n-orchestrator ile bu görevi otomatize et"
---

# n8n Orkestratörü

## Rolüm
Gök Umay'ın tekrarlayan işlerini n8n'e devrederim.
Claude Code beyin — n8n sinir sistemi.

## TOKEN KURALI
Workflow JSON'ını komple yazma — node listesi + bağlantı yapısı ver.

---

## Mimari

```
Claude Code (karar verir, kod yazar)
        │
        │ MCP üzerinden
        ▼
    n8n (tetikler, bağlar, bildirir)
        │
        ├── GitHub
        ├── Supabase
        ├── Discord / Telegram
        ├── itch.io
        └── Play Store
```

---

## Termux Kurulum

```bash
# Node.js gerekli (18+)
node --version

# n8n kur
npm install -g n8n

# İlk başlatma
n8n start

# Arka planda çalıştır
nohup n8n start > ~/.n8n/n8n.log 2>&1 &

# API key al (http://localhost:5678 → Settings → API)
echo "N8N_API_KEY=..." >> ~/.env

# Claude Code'a n8n MCP ekle
claude mcp add --transport stdio n8n -- \
  npx -y n8n-mcp-server \
  --n8n-url http://localhost:5678 \
  --n8n-api-key $N8N_API_KEY
```

---

## 10 Hazır Gök Umay Workflow'u

### 1. Self-Healing (En Kritik)
```
Tetikleyici: n8n hata webhook
    ↓
Telegram: "Hata oluştu — [workflow adı]\n[hata mesajı]\n[Düzelt] butonu"
    ↓ (butona basılınca)
Claude Code headless: hatalı JSON oku → düzelt → deploy
    ↓
Telegram: "✅ Düzeltildi"
```

### 2. Versiyon Deploy Pipeline
```
Tetikleyici: GitHub push (main branch)
    ↓
node --check tüm .js dosyaları
    ↓ (başarılıysa)
Vercel deploy
    ↓
itch.io webhook güncelle
    ↓
Discord #güncellemeler: "v[N] yayında — [değişiklik]"
```

### 3. Haftalık Stüdyo Raporu
```
Tetikleyici: Cron — Pazartesi 09:00
    ↓
GitHub API: bu haftaki commitler
    ↓
Supabase: tamamlanan görevler
    ↓
Claude Code: rapor yaz (voice-dna sesiyle)
    ↓
Telegram: PDF rapor gönder
```

### 4. Oyuncu Geri Bildirim Pipeline
```
Tetikleyici: Play Store yeni yorum
    ↓
Claude Code: duygu analizi + kategori (bug/istek/övgü)
    ↓
Supabase: kaydet + etiketle
    ↓ (bug ise)
GitHub Issue otomatik aç
    ↓
Discord #feedback: özet bildirim
```

### 5. İçerik Takvimi
```
Tetikleyici: Cron — Çarşamba 10:00
    ↓
Supabase: bu hafta yayınlanacak içerikler
    ↓
Claude Code: post yaz (voice-dna → humanizer)
    ↓
Buffer/Hootsuite: zamanla
```

### 6. Otomatik Yedekleme
```
Tetikleyici: Cron — Her gece 02:00
    ↓
GitHub: tüm oyun dosyalarını yedekle
    ↓
Supabase: veritabanı snapshot
    ↓
Google Drive: zip yükle
    ↓
Telegram: "✅ Yedekleme tamamlandı — [boyut]"
```

### 7. Hata İzleme
```
Tetikleyici: Sentry yeni hata
    ↓
Claude Code: hata analizi (systematic-debugger)
    ↓
Supabase: hata kaydı + öncelik
    ↓ (P0 ise)
Telegram: acil bildirim + çözüm önerisi
```

### 8. Play Store Güncelleme
```
Tetikleyici: GitHub release tag (v*)
    ↓
Capacitor build otomatik
    ↓
Google Play API: AAB yükle
    ↓
App Store Connect API: yükle
    ↓
Telegram: "📱 Mağaza güncellemesi gönderildi"
```

### 9. itch.io Satış Takibi
```
Tetikleyici: Cron — Her gün 20:00
    ↓
itch.io API: günlük indirme/satış
    ↓
Supabase: kaydet
    ↓ (hedef aşıldıysa)
Telegram: "🎉 Günlük hedef aşıldı!"
```

### 10. Araştırma Pipeline
```
Tetikleyici: Webhook (Obsidian not kaydedildi)
    ↓
Claude Code: not özetle + etiketle
    ↓
Supabase pgvector: embedding olarak kaydet
    ↓
NotebookLM API: kaynak olarak ekle
```

---

## Karar Matrisi

```
"Bu görevi otomatize etmeli miyim?"

Sıklık: Haftada 3+ kez? → Evet
Süre:   5+ dakika alıyor? → Evet
Hata:   Manuel yapınca hata oluyor mu? → Evet
Bağlam: Birden fazla servis var mı? → Evet

Tümü evet → n8n workflow yaz
```

---

## Çıktı

```
## n8n Workflow Planı — [görev]

Tetikleyici: [ne başlatır]
Node zinciri:
1. [Node türü] → [ne yapar] → [çıktı]
2. ...

Hata senaryosu: [ne olursa ne yapılır]
Tahmini kurulum: [N dakika]
```
