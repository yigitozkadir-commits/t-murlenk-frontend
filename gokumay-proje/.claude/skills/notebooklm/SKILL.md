---
name: notebooklm
description: |
  NotebookLM ile büyük belgeleri özetle, token kullanımını azalt.
  Araştırma → özet → Claude Code iş akışı.
  Kullan: "notebooklm ile bu belgeyi işle"
---

# NotebookLM Entegrasyonu

Büyük belgeler doğrudan Claude Code'a getirilmez.
NotebookLM önce damıtır, Claude Code özeti işler.
Token tasarrufu: %60-80.

## İş Akışı

```
1. Kaynağı NotebookLM'e yükle
   → PDF, URL, metin, YouTube linki

2. NotebookLM'de şu soruyu sor:
   "[Konu] hakkında en önemli 5 bulguyu çıkar.
    Her bulgu için kaynak paragrafını da belirt."

3. Ses notu oluştur (opsiyonel)
   → Podcast formatı → bilgiyi pasif dinle

4. Metin çıktısını kopyala → Claude Code'a getir

5. research-analyst ile yapılandır
```

## Ne Zaman NotebookLM Kullan

```
Büyük belgeler:   100+ sayfa PDF, akademik makale
Çok kaynak:       5+ URL'i aynı anda analiz et
Tarihi araştırma: Murray, Bell, Parlett gibi klasikler
Video içerik:     YouTube transkriptini analiz et
Teknik dokuman:   Capacitor, Three.js büyük changelog
```

## Ne Zaman Doğrudan Claude Code Kullan

```
Kısa belgeler:    < 20 sayfa
Kod dosyaları:    Doğrudan analiz et
Hata mesajları:   Kopyala-yapıştır
Hızlı soru:       Tek kaynak, net soru
```

## NotebookLM'e Yükleme Tipleri

```
PDF        → Sürükle bırak
URL        → Web sayfası (JS-heavy siteler kısmi çalışır)
Metin      → Kopyala yapıştır (max ~500K karakter)
YouTube    → Video URL yapıştır → transkript otomatik çekilir
Google Doc → Drive entegrasyonu ile
```

## Tarihi Oyun Araştırması İçin Örnek Prompt

```
NotebookLM'de:
"Bu kaynaktan Timurlenk Satranç varyantı hakkında şunları çıkar:
1. Oyunun tarihi belgesi (ne zaman, kim tarafından)
2. Orijinal kural seti (tam mı, kısmi mi belgelenmiş?)
3. Tahta boyutu ve taş sayısı
4. Modern uyarlamalar var mı?
5. Güvenilirlik notu (birincil kaynak mı, ikincil mi?)"
```

## Token Karşılaştırma

```
Yöntem                Token kullanımı
─────────────────────────────────────
Ham PDF → Claude      ~50.000 token
NotebookLM özeti      ~2.000 token
Tasarruf              ~96%
```

## Sınırlamalar

```
- NotebookLM Türkçe içerikte bazen İngilizce yanıt verir
  → Soruyu İngilizce sor, Türkçe çeviri iste
- Gerçek zamanlı web tarama yok
  → Güncel içerik için firecrawl skill kullan
- Max 50 kaynak / notebook
```


