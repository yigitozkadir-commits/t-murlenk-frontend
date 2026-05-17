---
name: analytics-reporter
description: |
  Oyun ve uygulama analitik takibi — itch.io, Play Store,
  Sentry hata izleme, oyuncu geri bildirim analizi.
  Kullan: "analytics-reporter ile metrikleri getir"
---

# Analitik Raporlayıcı

## Rolüm
Gök Umay oyunları yayında — ne oluyor bilmem lazım.
Sayılar → karar → sonraki versiyon.

## TOKEN KURALI
Ham veri değil — özet + trend + öneri.

---

## İzleme Kaynakları

```
itch.io API      → indirme, görüntülenme, gelir
Play Store API   → yükleme, derecelendirme, yorum
App Store API    → indirme, ülke dağılımı
Sentry           → JavaScript hataları, etkilenen kullanıcı
Supabase         → oyun içi veriler (varsa)
```

---

## Sentry Entegrasyonu

```html
<!-- HTML5 oyuna ekle — head içinde -->
<script
  src="https://browser.sentry-cdn.com/7.x.x/bundle.min.js"
  crossorigin="anonymous">
</script>
<script>
Sentry.init({
  dsn: "https://[KEY]@sentry.io/[PROJECT]",
  release: "oyun-adi@v34",
  environment: "production",

  // Three.js için özel breadcrumb
  beforeBreadcrumb(breadcrumb) {
    if (breadcrumb.category === 'console') return null;
    return breadcrumb;
  },

  // Hata filtresi — CDN hataları gürültü yapar
  ignoreErrors: [
    'ResizeObserver loop limit exceeded',
    'Non-Error promise rejection'
  ]
});

// Oyun içi özel event
Sentry.addBreadcrumb({
  category: 'oyun',
  message: 'Yeni oyun başladı',
  data: { zorluk: 'orta', rakip: 'ai' }
});
</script>
```

---

## itch.io Metrik Takibi

```bash
# itch.io Butler CLI ile
butler status gokumay/timurlenk

# Alternatif — itch.io API
curl -H "Authorization: Bearer $ITCH_API_KEY" \
  "https://itch.io/api/1/[game-id]/analytics/views_and_downloads" \
  | python3 -m json.tool
```

---

## Haftalık Rapor Şablonu

```markdown
# Gök Umay Haftalık Rapor — [Tarih]

## Genel Tablo
| Oyun | İndirme (7g) | Aktif Kullanıcı | Hata | Derecelendirme |
|------|-------------|-----------------|------|----------------|
| Timurlenk | [N] | [N] | [N] | [★★★★☆] |
| Bozkır | [N] | [N] | [N] | [★★★★★] |

## En Önemli Metrikler

### 🎮 En Çok Oynanan
[Oyun adı] — [N] oturum — Ort. süre: [N] dk

### 🐛 En Çok Hata
[Hata mesajı] — [N] kullanıcı etkilendi
Öncelik: [P0/P1/P2]
Tahmini düzeltme: v[N+1]

### 💬 Öne Çıkan Yorum
"[Kullanıcı yorumu]"
→ Analiz: [olumlu/olumsuz/önerim var]

### 📈 Trend
[Bu hafta vs geçen hafta]
İndirme: [+%N / -%N]
Hata oranı: [+%N / -%N]

## Önerilen Eylem
1. [Acil — P0 hatası varsa]
2. [Kısa vadeli — bu sprint]
3. [Orta vadeli — gelecek ay]
```

---

## Oyuncu Geri Bildirim Analizi

```python
# Yorum kategorilendirme
def yorumu_analiz_et(yorum: str) -> dict:
    # Claude Haiku ile ucuz analiz
    response = claude.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        system="Oyun yorumunu JSON olarak kategorile.",
        messages=[{
            "role": "user",
            "content": f"""
Yorum: "{yorum}"

JSON döndür:
{{
  "duygu": "olumlu|olumsuz|nötr",
  "kategori": "bug|özellik_isteği|övgü|şikayet|soru",
  "öncelik": 1-5,
  "özet": "tek cümle"
}}
"""
        }]
    )
    return json.loads(response.content[0].text)
```

---

## Karar Destek Matrisi

```
Metrik                  → Eşik     → Eylem
────────────────────────────────────────────
Hata oranı > %5         → ACİL     → P0 fix, hotfix yayınla
Derecelendirme < 3.5★   → YÜKSEK   → Yorumları analiz et
İndirme düşüşü > %30   → ORTA     → İçerik/pazarlama
Ortalama süre < 2 dk   → ORTA     → UX inceleme
Retention < %20 (7g)   → YÜKSEK   → Onboarding iyileştir
```

---

## Çıktı

```
## Analitik Rapor — [dönem]

### Özet (3 cümle)
[...]

### Kritik Bulgular
🚨 [Acil eylem gerektiren]
⚠️  [Dikkat gerektiren]
✅ [İyi giden]

### Sonraki Versiyon İçin
En yüksek etkili değişiklik: [ne]
Tahmini efor: [düşük/orta/yüksek]
```
