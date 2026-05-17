---
description: NotebookLM araştırma pipeline hazırla — token verimli araştırma.
tools: [bash, read, edit]
---

"$ARGUMENTS" için NotebookLM araştırma paketi hazırla.

ADIM 1 — KAYNAK TOPLAMA
Web'den 5-8 güvenilir kaynak bul:
- Akademik/birincil kaynak (en az 1)
- Teknik belge (varsa)
- Topluluk kaynağı
- Görsel/video (YouTube transkript)

Her kaynak için:
[URL] — [Neden değerli — tek cümle]

ADIM 2 — NOTEBOOKLM YÜKLEME LİSTESİ
NotebookLM'e bu sırayla yükle:
1. [En kapsamlı kaynak]
2. [Çelişen görüş kaynağı]
3. [Güncel kaynak]

ADIM 3 — SORU LİSTESİ
NotebookLM'e sorulacak 8 kritik soru:
1. [Temel tanım sorusu]
2. [Gök Umay'a özgü soru]
3. [Tarihi doğruluk sorusu]
4. [Belirsizlik sorusu]
5. [Rakip görüş sorusu]
6. [Pratik uygulama sorusu]
7. [Kaynak güvenilirlik sorusu]
8. [Gelecek araştırma sorusu]

ADIM 4 — ÖZET GETIRME ŞABLONU
NotebookLM özeti aldıktan sonra bu formatta getir:

```
NotebookLM Özeti — $ARGUMENTS
---
[Özeti buraya yapıştır]
---
Görev: [Ne yapmamı istiyorsun]
Agent: [narrative-director / game-designer / research-analyst]
```

TOKEN TASARRUFU: Ham kaynak değil sadece özet → %60-80 token azalması.

KONU: $ARGUMENTS


