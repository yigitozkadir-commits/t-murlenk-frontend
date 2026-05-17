# CLAUDE.md — Katman 2 Eklentisi
# Bu bölümü mevcut CLAUDE.md'nin sonuna ekle

---

## Katman 2 — Gelişmiş Sistemler

### Yeni Agent'lar (4)

```
n8n-orchestrator    → n8n workflow tasarımı ve MCP koordinasyonu
memory-manager      → Supabase pgvector kalıcı hafıza
publisher           → Çok kanallı yayın pipeline
analytics-reporter  → Metrik takibi ve oyuncu analizi
```

### Yeni Skill'ler (6)

```
n8n-workflows       → Workflow şablonları, Termux kurulum
prompt-caching      → %90 token tasarrufu — API caching
supabase-memory     → pgvector şema + Python istemcisi
gemini-hybrid       → Claude + Gemini iş bölümü
sentry-monitoring   → HTML5 oyun hata izleme
store-listing       → ASO + platform listing şablonları
```

### Yeni Slash Komutları (7)

```
/workflow [görev]   → n8n workflow oluştur
/remember [bilgi]   → Kalıcı hafızaya kaydet
/recall [sorgu]     → Geçmiş kararları getir
/publish [dosya]    → Tüm platformlara yayınla
/deploy [proje]     → Belirtilen platforma deploy et
/announce [oyun]    → Çok kanallı duyuru hazırla
/metrics [oyun]     → Analitik raporu getir
/cost-check         → API maliyet analizi
```

---

## Katman 2 Hızlı Referans

### Hafıza İş Akışı

```
Önemli karar alındı → /remember [karar]
Benzer sorunla karşılaşıldı → /recall [sorgu]
Geçmiş versiyon kararı → /recall [konu] mimari
```

### Maliyet Kontrolü

```
Haftalık → /cost-check
Araştırma görevi → Gemini CLI önce (ücretsiz)
Büyük belge → NotebookLM → özet → Claude
Tekrarlayan API → prompt-caching skill uygula
```

### Yayın Pipeline

```
/review → /security → /publish → /announce → /metrics
```

### n8n Durumu

```bash
# n8n çalışıyor mu?
curl -s http://localhost:5678/healthz && echo "✅" || echo "❌ Başlat: nohup n8n start &"
```

### Ortam Değişkenleri (Katman 2 için)

```bash
# ~/.env'e ekle
export SUPABASE_URL="https://[proje].supabase.co"
export SUPABASE_KEY="[anon-key]"
export N8N_API_KEY="[n8n-api-key]"
export TELEGRAM_BOT_TOKEN="[token]"
export TELEGRAM_CHAT_ID="[chat-id]"
export DISCORD_WEBHOOK_URL="[url]"
export SENTRY_DSN="https://[key]@sentry.io/[proje]"
export GEMINI_API_KEY="[key]"
export ITCH_API_KEY="[key]"
```
