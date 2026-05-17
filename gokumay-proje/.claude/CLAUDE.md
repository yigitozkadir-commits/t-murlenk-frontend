# Gök Umay Stüdyo — Master Anayasa

## Bu Repo Nedir?
Gök Umay Stüdyo'nun Claude Code altyapısı.
Solo geliştirici. Oyunlar, uygulamalar, web siteleri — her şey yapılır.
Dil: Türkçe (yorumlar, belgeler, tüm iletişim).

## Repo Yapısı (49 Dosya)

```
.claude/
├── CLAUDE.md                    ← Bu dosya — her şeyin başlangıcı
├── settings.json                ← Token limitleri + hook ayarları
│
├── agents/                      ← 20 uzman — kim çalışıyor?
│   ├── systematic-debugger.md
│   ├── technical-director.md
│   ├── game-designer.md
│   ├── qa-tester.md
│   ├── project-manager.md
│   ├── narrative-director.md
│   ├── refactorer.md
│   ├── performance-engineer.md
│   ├── security-auditor.md
│   ├── launch-strategy.md
│   ├── content-marketer.md
│   ├── research-analyst.md
│   ├── ai-engineer.md
│   ├── ui-designer.md
│   ├── voice-dna.md
│   ├── documentation.md
│   ├── competitive-analyst.md
│   ├── mobile-developer.md
│   ├── workflow-orchestrator.md
│   └── skill-creator.md
│
├── skills/                      ← 11 araç seti — ne biliyor?
│   ├── systematic-debugging/SKILL.md
│   ├── owasp-security/SKILL.md
│   ├── vibesec/SKILL.md
│   ├── three-js-patterns/SKILL.md
│   ├── game-ai-engine/SKILL.md
│   ├── minimax-ai/SKILL.md
│   ├── frontend-design/SKILL.md
│   ├── notebooklm/SKILL.md
│   ├── humanizer/SKILL.md
│   ├── seo-geo/SKILL.md
│   └── capacitor-mobile/SKILL.md
│
└── commands/                    ← 15 slash komutu — nasıl tetikliyor?
    ├── fix.md          → /fix [dosya]
    ├── review.md       → /review [dosya]
    ├── refactor.md     → /refactor [dosya]
    ├── version.md      → /version [dosya]
    ├── launch.md       → /launch [proje]
    ├── security.md     → /security [dosya]
    ├── perf.md         → /perf [dosya]
    ├── post.md         → /post [konu]
    ├── new-game.md     → /new-game [oyun adı]
    ├── myth.md         → /myth [varlık adı]
    ├── notebook-prep.md→ /notebook-prep [konu]
    ├── automate.md     → /automate [görev]
    ├── weekly.md       → /weekly
    ├── explain.md      → /explain [konu]
    └── clean.md        → /clean [klasör]
```

---

## Token Verimliliği — EN YÜKSEK ÖNCELİK

Her görevde önce şunu sor: **"En az token ile en çok değeri nasıl üretirim?"**

```
✓ Mevcut kodu önce oku, sadece değişen kısmı yaz
✓ Büyük dosyada sadece ilgili bölümü oku (±20 satır)
✓ Sonuç önce, gerekçe sonra
✓ Tekrar eden blok → fonksiyona al
✓ NotebookLM özeti getir, ham kaynak değil (%60-80 tasarruf)
✗ Dosyanın tamamını okuma
✗ Gereksiz açıklama yapma
✗ Aynı kodu iki kez yazma
```

---

## Üç Katman Nasıl Birlikte Çalışır?

```
Sen yazarsın: /fix timurlenk_v34.html
                    ↓
         commands/fix.md okunur
         "5 Neden tekniği — adım adım talimat"
                    ↓
         agents/systematic-debugger.md devreye girer
         "hata ayıklayıcı rolü — düşünce yapısı"
                    ↓
         skills/systematic-debugging/SKILL.md referans alınır
         "Three.js hata kalıpları — hazır çözümler"
                    ↓
         hooks/node-check.sh otomatik tetiklenir
         "Sözdizimi hatası var mı?"
```

---

## Hangi İşte Ne Kullanılır?

### Hızlı Referans — Agent

```
Bug / hata        → /fix + systematic-debugger
Mimari karar      → technical-director
Mekanik tasarım   → game-designer
Kültürel doğruluk → narrative-director
Yayın kontrolü    → /review + qa-tester → /security + security-auditor
İçerik yazma      → voice-dna → humanizer (bu sırayla zorunlu)
Yeni oyun         → /new-game + workflow-orchestrator
Haftalık plan     → /weekly + project-manager
Araştırma         → /notebook-prep + research-analyst
Lansman           → /launch + launch-strategy
Mobil paket       → mobile-developer + capacitor-mobile skill
FPS sorunu        → /perf + performance-engineer
```

### Hızlı Referans — Skill

```
Three.js sahne      → three-js-patterns
AI motor            → game-ai-engine (CSP uyumlu inline motor)
Minimax denge       → minimax-ai (değerlendirme fonksiyonu)
Güvenlik tarama     → owasp-security + vibesec
UI bileşen          → frontend-design
NotebookLM pipeline → notebooklm
İçerik temizleme    → humanizer
SEO / GEO           → seo-geo
Mobil paketleme     → capacitor-mobile
```

---

## Kod Standartları

```
Sözdizimi kontrolü:  node --check dosya.js  (JS — zorunlu)
Versiyon numarası:   her değişiklikte +1 (v34→v35, atla değil)
Yorum dili:          Türkçe  // Bu fonksiyon X yapar
Hata yönetimi:       try/catch + konsola Türkçe mesaj
CSP uyumu:           blob URL yasak → new Function + fakeSelf
```

---

## Çıktı Formatları

| Senaryo | Format |
|---------|--------|
| Hızlı prototip | Tek HTML, sıfır dış bağımlılık |
| Oyun | HTML5, Three.js inline CDN, Web Audio API |
| Mobil | HTML5 → Capacitor → Play Store / App Store |
| Web sitesi | Çok dosyalı, normal proje düzeni |
| Uygulama | Projeye göre — önce teknik-director'a sor |

---

## Teknoloji Yığını

```
Oyun motoru:   Three.js r128 (inline CDN)
Ses:           Web Audio API (native)
AI motoru:     new Function + fakeSelf mesaj yolu (CSP uyumlu)
UI:            Vanilla JS + CSS3 (React sadece web app için)
Mobil:         Capacitor (HTML5 → native)
Veritabanı:    localStorage (basit) / Supabase (çok kullanıcılı)
Araştırma:     NotebookLM → Claude Code pipeline
```

---

## Bozkır Platform Mimarisi

```
Platform Katmanı
  → Paylaşılan: nebula, toast, confetti, SFX, ELO, achievements
      → AIBridge (engine kayıt sistemi)
            → Oyun Plugin'leri:
               Hiashatar | Togyzool | Şatra | Satrancı Rumi
               Timurlenk | Kurt & Koyun
```

---

## Aktif Projeler

- **Timurlenk Satranç v34+** — 11×10, 3D, minimax AI
- **Bozkır Platform v2** — 6 oyunlu platform
- **Vitrin v5** — Oyun showcase

### Arşiv
*(tamamlanan projeler buraya)*

---

## Hook Sistemi (Otomatik)

```
settings.json tanımlı — her araç çağrısında arka planda çalışır:

PreToolUse  → block-dangerous.sh   (tehlikeli komut engeli)
PreToolUse  → protect-secrets.sh   (API key koruması)
PostToolUse → node-check.sh        (sözdizimi doğrulama)
Stop        → notify-done.sh       (Termux bildirimi)
PreCompact  → pre-compact-backup.sh(oturum yedekleme)
```

Kurulum: `bash kurulum-hooks.sh` (repo kökünde)

---

## NotebookLM Entegrasyonu

```
Büyük belge / araştırma
        ↓
   NotebookLM (özetle, damıt)
        ↓
   /notebook-prep ile yapılandır
        ↓
   research-analyst → narrative-director / game-designer
```

Token tasarrufu: Ham kaynak değil özet kullan → %60-80 azalma.

---

## Yasaklar

```
❌ Görev başlamadan çok soru sorma — varsayım yap, sonra sor
❌ "Tabii ki!", "Harika soru!" dolgu ifadeler
❌ Aynı kodu iki kez yazma — referans ver
❌ Dış bağımlılık önermeden vanilla alternatifi denemeden
❌ Tek dosya projesini söylenmeden çok dosyaya bölme
❌ Büyük dosyanın tamamını okuma — sadece ilgili bölüm
❌ agent/skill/komut olmadan büyük görev başlatma
```

---

## İlk Açılışta Yap

```bash
# 1. Yapıyı doğrula
ls .claude/agents/ | wc -l    # 20 olmalı
ls .claude/skills/ | wc -l    # 11 olmalı
ls .claude/commands/ | wc -l  # 15 olmalı

# 2. Hook'ları kur (bir kez)
bash kurulum-hooks.sh

# 3. Çalışmaya başla
/weekly   # Haftalık plan
```

---

## Altın Kural

> **Oku. Düşün. Üret. Doğrula. Belgele.**
> Sırayla, verimli, Türkçe.


