---
name: gemini-hybrid
description: |
  Claude + Gemini CLI hibrit stratejisi.
  Günde 1000 ücretsiz istek — araştırma ve ön işlem için.
  Kullan: "gemini-hybrid ile bu araştırmayı yap"
---

# Claude + Gemini Hibrit Strateji

## TOKEN KURALI
Gemini'yi araştırma/ön işlem için kullan — karar ve kod Claude'da.

---

## Termux Kurulum

```bash
# Gemini CLI kur
npm install -g @google/gemini-cli

# veya pip
pip install google-generativeai --break-system-packages

# API key al (ücretsiz)
# aistudio.google.com → Get API Key

# Ortam değişkeni
echo 'export GEMINI_API_KEY="..."' >> ~/.env
source ~/.env

# Test
gemini "Merhaba, çalışıyor musun?"
```

---

## İş Bölümü Matrisi

```
GEMINI (Ücretsiz — 1000/gün):
✓ Web araştırması — Türkçe kaynaklar dahil
✓ Mitoloji ham bilgi toplama
✓ Rakip oyun analizi
✓ Hızlı prototip fikirleri
✓ Veri dönüştürme / format değiştirme
✓ Basit Türkçe çeviri
✓ Google Workspace (Drive, Docs, Sheets)

CLAUDE CODE (Ücretli — verimli kullan):
✓ Gerçek kod yazma ve düzenleme
✓ Mimari kararlar
✓ Kapsamlı analiz
✓ Agent koordinasyonu
✓ Oyun mekanik tasarımı
✓ Kalite kontrol
```

---

## YK Sugi "Minyon Model" Stratejisi

```bash
# Türkçe mitoloji araştırması → Gemini → Claude
gemini "Türk mitolojisinde Umay Ana sembolik anlamları" > /tmp/umay.txt
cat /tmp/umay.txt | claude "Bunu tarot kart formatına dönüştür"

# Rakip oyun analizi → Gemini → Claude
gemini "itch.io chess variant en popüler 10 oyun 2026" > /tmp/rakipler.txt
cat /tmp/rakipler.txt | claude "competitive-analyst olarak analiz et"

# BoardGameGeek araştırması
gemini "BoardGameGeek Tamerlane chess reviews 2024 2025" > /tmp/bgg.txt
cat /tmp/bgg.txt | claude "narrative-director olarak doğruluk değerlendir"
```

---

## Pipeline Entegrasyonu

```bash
#!/bin/bash
# ~/.claude/scripts/arastir.sh
# Kullanım: bash arastir.sh "Moğol satranç kuralları" oyun

KONU="$1"
KATEGORI="${2:-genel}"

echo "🔍 Gemini ile araştırılıyor: $KONU"

# Gemini araştırır
gemini "Şu konuda kapsamlı bilgi ver: $KONU
  Kaynakları belirt.
  Belirsiz bilgileri işaretle." > /tmp/arastirma.txt

echo "📊 Sonuç: $(wc -w < /tmp/arastirma.txt) kelime"

# Claude işler
echo "🧠 Claude ile işleniyor..."
cat /tmp/arastirma.txt | claude "
research-analyst olarak bu araştırmayı işle:
1. Güvenilir bilgileri listele
2. Belirsiz olanları işaretle
3. Gök Umay projesine nasıl uygulanır?
4. Hafızaya kaydet: kategori=$KATEGORI
"

# Temizlik
rm /tmp/arastirma.txt
echo "✅ Tamamlandı"
```

---

## Google Workspace Entegrasyonu

```bash
# Google Drive'dan içerik al
gemini "Google Drive'ımdaki 'Türk Mitolojisi Notları' dokümanını özetle"

# Google Sheets'e veri yaz
gemini "Bu veriyi Google Sheets formatında hazırla:
$(cat oyun_istatistikleri.json)"

# Gmail'den bildirim gönder (n8n olmadan basit yol)
gemini "Bu metni e-posta formatına dönüştür: ..."
```

---

## Maliyet Optimizasyonu

```
Günlük 1000 ücretsiz istek planlaması:

Sabah (100 istek):   Araştırma toparlama
Öğle  (200 istek):   Ön işlem ve filtreleme
Akşam (400 istek):   İçerik üretimi desteği
Yedek (300 istek):   Beklenmedik görevler

Toplam günlük Claude tasarrufu:
  Ortalama 200 token/istek × 1000 istek = 200.000 token
  Sonnet 4.6 fiyatıyla = ~$0.60/gün tasarruf
  Aylık = ~$18 tasarruf
```

---

## Dikkat Edilecekler

```
❌ Gemini ile YAPMA:
- Gerçek kod yazma (hata oranı yüksek)
- Mimari kararlar
- Güvenlik incelemeleri
- Gök Umay'a özel iş mantığı

✓ Claude'a geç:
- Gemini çıktısını ham bırakma
- "Gemini bunu söyledi, sen ne düşünürsün?" formatı
- Çelişen bilgilerde Claude'a doğrulat
```
