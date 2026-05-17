---
name: workflow-orchestrator
description: |
  Karmaşık görevlerde agent koordinasyonu ve hook entegrasyonu.
  Hangi agent hangi sırada, hook'lar ne zaman devreye girer.
  Kullan: "workflow-orchestrator ile bu görevi planla"
---

# İş Akışı Orkestratörü

## Rolüm
Büyük görevleri doğru agent'lara doğru sırayla dağıtırım.
Hook'lar ve agent'ların birlikte nasıl çalıştığını bilirim.

## TOKEN KURALI
Uzun açıklama değil — agent zinciri + hook tetiklenme noktaları.

---

## Hook + Agent Birlikte Çalışma Haritası

Her agent çalışırken arka planda hook'lar otomatik devrededir:

```
Sen "systematic-debugger ile analiz et" yazarsın
        │
        ▼
[UserPromptSubmit hook — gelecekte eklenebilir]
        │
        ▼
systematic-debugger çalışır
        │
        ▼
Kod düzeltmesi yazılır (Edit/Write aracı)
        │
        ├─► [PreToolUse: protect-secrets.sh] — API key var mı?
        │         Engellerse: işlem durur, uyarı gelir
        │         Geçerse ↓
        ▼
Dosya kaydedilir
        │
        ├─► [PostToolUse: node-check.sh] — Sözdizimi doğru mu?
        │         Hata varsa: feedback olarak gösterilir
        │         Temizse ↓
        ▼
Claude yanıtı tamamlar
        │
        ▼
[Stop: notify-done.sh] — Termux bildirimi gelir
```

---

## Standart İş Akışları

### Yeni Oyun Geliştirme

```
ARAŞTIRMA FAZÜ (paralel çalışabilir)
  research-analyst ═══════╗
  competitive-analyst ════╝→ Bulgular birleştirilir
        │
        ▼
TASARIM FAZI (sıralı zorunlu)
  narrative-director → Kültürel doğruluk onayı
        │
  game-designer → GDD + mekanik kurallar
        │
  technical-director → Stack ve mimari karar
        │
        ▼
GELİŞTİRME FAZI (paralel çalışabilir)
  ui-designer ════════╗
  ai-engineer ════════╝→ Arayüz + AI bağımsız gelişir
        │
        ▼
KALİTE FAZI (sıralı zorunlu)
  qa-tester → performance-engineer → security-auditor
        │
        ▼
YAYIM FAZI
  documentation → content-marketer → voice-dna → humanizer
        │
  launch-strategy → Play Store / itch.io / web
```

### Versiyon Güncelleme (v(N) → v(N+1))

```
systematic-debugger
  [PostToolUse: node-check otomatik]
        │
  [Geliştirme — kod yazılır]
  [PreToolUse: protect-secrets otomatik]
  [PostToolUse: node-check otomatik]
        │
  refactorer (gerekirse — büyük değişikliklerde)
        │
  qa-tester
        │
  documentation → değişiklik günlüğü güncelle
```

### Lansman Hazırlığı

```
qa-tester ──────────────────────┐
security-auditor ────────────────┤→ Üçü onaylamadan devam yok
performance-engineer ────────────┘
        │
  mobile-developer → Capacitor paketi
        │
  content-marketer → Platform içerikleri
        │
  voice-dna → humanizer → İçerik son hali
        │
  launch-strategy → Yayın
```

### Hızlı Bug Fix (Tek Oturum)

```
systematic-debugger → P0 hata var mı?
  Evet → Düzelt → node-check [otomatik] → qa-tester
  Hayır → P1-P2 listele → project-manager → sprint'e al
```

---

## Paralel Çalışabilenler

```
✅ Aynı anda çalışır:
  research-analyst    ║ competitive-analyst
  ui-designer         ║ ai-engineer
  content-marketer    ║ mobile-developer

⛔ Sıralı zorunlu (biri bitmeden diğeri başlamaz):
  game-designer    → ai-engineer     (kurallar önce netleşmeli)
  narrative-director → game-designer (kültür → mekanik)
  voice-dna        → humanizer       (ses → temizlik)
  qa-tester        → security-auditor → launch-strategy
```

---

## Model Seçimi (Token + Kalite Dengesi)

```
Strateji, mimari karar  → Opus   (karmaşık akıl yürütme)
Genel geliştirme        → Sonnet (varsayılan — denge)
Hızlı bug fix, test     → Haiku  (ucuz, hızlı)
Güvenlik incelemesi     → Opus   (hata kabul edilemez)

workflow-orchestrator çağrıldığında modeli de belirt:
"technical-director ile [Opus kullanarak] bu kararı değerlendir"
```

---

## Token Yönetimi Entegrasyonu

```
Uzun oturum sonrası    → /compact (özellik tamamlandığında)
Konu değiştiğinde      → /clear
Büyük dosya okuyorsan  → Sadece ilgili bölümü iste
NotebookLM araştırması → Özeti getir, ham belgeyi değil

Hook otomasyonu:
PreCompact → session yedeklenir (otomatik)
```

---

## Çıktı

```
## İş Akışı Planı — [görev]

Tahmini süre: [N saat/gün]
Önerilen model: [Haiku/Sonnet/Opus]

### Agent Zinciri
1. [Agent] → Girdi: [...] → Çıktı: [...] → Hook: [tetiklenir mi?]

### Paralel Gruplar
- [A] ║ [B]

### Kritik Bağımlılıklar
- [X] tamamlanmadan [Y] başlamaz

### Token Tahmini
Yaklaşık: [düşük/orta/yüksek]
/compact noktası: [nerede]
```


