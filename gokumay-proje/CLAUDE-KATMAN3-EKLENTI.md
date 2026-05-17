# CLAUDE.md — Katman 3 Eklentisi
# Bu bölümü mevcut CLAUDE.md'nin sonuna ekle

---

## Katman 3 — Zeka Katmanı

### Yeni Agent'lar (6)

```
mcp-server-builder      → Özel MCP araçları — yeni yetenekler ekle
rag-pipeline            → Belge semantik arama — GDD, bug, tarihi kaynak
multi-agent-coordinator → Agent zincirleri — otomatik koordinasyon
playtest-ai             → Oyun simülasyonu — denge ve edge case testi
monetization-optimizer  → Gelir optimizasyonu — fiyat, freemium, ASO
community-manager       → Discord bot + Reddit otomasyon
```

### Yeni Skill'ler (6)

```
mcp-server-builder   → TypeScript MCP şablonu + araç blokları
rag-pipeline         → Chunk stratejisi + hibrit arama + prompt entegrasyonu
multi-agent-coordinator → Zincir kalıpları + model seçimi + maliyet
playtest-ai          → Denge testi CLI + edge case + hafıza testi
monetization-optimizer → Dönüşüm formülü + freemium tasarım + KPI
community-manager    → discord.py bot + praw Reddit + içerik bankası
```

### Yeni Slash Komutları (5)

```
/mcp-add [araç]     → MCP sunucusuna yeni araç ekle
/rag-index [dosya]  → Belgeyi RAG pipeline'a yükle
/playtest [oyun]    → Denge + edge case + performans testi
/chain [zincir]     → Multi-agent zinciri çalıştır
/community [görev]  → Discord/Reddit topluluk yönetimi
```

---

## Katman 3 Hızlı Referans

### MCP Araçları
```bash
claude mcp list                    # Aktif araçlar
claude "gokumay araçlarını listele" # Test
```

### RAG Sorgulama
```bash
python3 ~/.claude/scripts/rag_client.py ara "Timurlenk Deve kuralı"
/rag-index ~/.claude/CLAUDE.md     # Anayasayı indeksle
```

### Multi-Agent Zincirler
```
/chain versiyon timurlenk_v34.html → 5 agent paralel çalışır
/chain icerik "Timurlenk güncelleme" → 4 agent sıralı çalışır
/chain lansman timurlenk → tam pipeline
```

### Topluluk
```bash
# Discord bot başlat (arka planda)
nohup python3 ~/.claude/scripts/discord_bot.py > ~/.claude/logs/discord.log &

# Reddit bot başlat
nohup python3 ~/.claude/scripts/reddit_manager.py > ~/.claude/logs/reddit.log &
```

### Yeni Ortam Değişkenleri (Katman 3 için)
```bash
export DISCORD_BOT_TOKEN="..."
export DUYURU_KANAL_ID="..."
export REDDIT_CLIENT_ID="..."
export REDDIT_SECRET="..."
export REDDIT_USERNAME="..."
export REDDIT_PASSWORD="..."
export N8N_URL="http://localhost:5678"
```
