---
name: prompt-caching
description: |
  Anthropic API prompt caching — %90 token tasarrufu.
  Sistem promptu, tool tanımı, belge caching kalıpları.
  Kullan: "prompt-caching ile API maliyetini düşür"
---

# Prompt Caching

## TOKEN KURALI
Teori değil — çalışan kod bloğu ver.

---

## Tek Satır Değişiklik

```python
# ÖNCE — her istek tam fiyat
system = "Sen bir oyun geliştirici asistanısın..."

# SONRA — %90 tasarruf
system = [{
    "type": "text",
    "text": "Sen bir oyun geliştirici asistanısın...",
    "cache_control": {"type": "ephemeral"}  # ← Bu kadar!
}]
```

---

## Fiyat Mantığı (Mayıs 2026, Sonnet 4.6)

```
Cache yazma:  Standart fiyatın %125 (ilk istek)
Cache okuma:  Standart fiyatın %10  (sonraki istekler)
Cache ömrü:   5 dakika (her erişimde sıfırlanır)

Başa baş noktası: 3+ istek → karlı
```

---

## 5 Temel Kalıp

### 1. Sistem Promptu (En Basit)

```python
import anthropic
client = anthropic.Anthropic()

SISTEM = """
[Gök Umay stüdyo promptu — 5000+ token]
[20 agent tanımı]
[Altın kurallar]
[Stack bilgisi]
"""

def sor(kullanici_sorusu: str):
    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=[{
            "type": "text",
            "text": SISTEM,
            "cache_control": {"type": "ephemeral"}
        }],
        messages=[{"role": "user", "content": kullanici_sorusu}]
    )
```

### 2. Büyük Belge Caching (RAG için)

```python
def belge_ile_sor(belge: str, soru: str):
    """Aynı belgeye çok soru sorulacaksa cache'le"""
    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=[
            {
                "type": "text",
                "text": "Gök Umay geliştirici asistanısın.",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"Analiz edilecek dosya:\n\n{belge}",
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[{"role": "user", "content": soru}]
    )
# İlk istek: belge cache'e yazılır
# Sonraki istekler: %90 ucuz
```

### 3. Çok Turlu Konuşma

```python
def sohbet(gecmis: list, yeni_mesaj: str):
    """Uzun geliştirme oturumlarında maliyet kontrolü"""
    # Son mesaj hariç hepsini cache'le
    if gecmis:
        gecmis[-1]["content"][-1]["cache_control"] = {
            "type": "ephemeral"
        }

    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=[{"type": "text", "text": SISTEM,
                 "cache_control": {"type": "ephemeral"}}],
        messages=gecmis + [{"role": "user", "content": yeni_mesaj}]
    )
```

### 4. Tool Tanımı Caching

```python
ARACLAR = [
    {"name": "kod_yaz", "description": "...", "input_schema": {...}},
    {"name": "test_et", "description": "...", "input_schema": {...}},
    # ... 10+ araç
]

def araçlarla_sor(soru: str):
    # Son araçta cache_control ekle — hepsini kapsar
    araclar = ARACLAR.copy()
    araclar[-1] = {**araclar[-1],
                   "cache_control": {"type": "ephemeral"}}

    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        tools=araclar,
        messages=[{"role": "user", "content": soru}]
    )
```

### 5. Batch + Cache (Maksimum Tasarruf)

```python
def toplu_islem(istekler: list):
    """Batch %50 + Cache %90 = %95 toplam indirim"""
    return client.messages.batches.create(
        requests=[{
            "custom_id": f"istek-{i}",
            "params": {
                "model": "claude-haiku-4-5",
                "max_tokens": 500,
                "system": [{
                    "type": "text",
                    "text": SISTEM,
                    "cache_control": {"type": "ephemeral"}
                }],
                "messages": [{"role": "user", "content": istek}]
            }
        } for i, istek in enumerate(istekler)]
    )
```

---

## Maliyet Monitörü

```python
def maliyet_raporu(response):
    u = response.usage
    toplam = u.input_tokens + u.cache_creation_input_tokens + u.cache_read_input_tokens

    # Sonnet 4.6 fiyatları ($/M token)
    normal_maliyet = toplam * 3 / 1_000_000
    gercek = (
        u.input_tokens * 3 +
        u.cache_creation_input_tokens * 3.75 +
        u.cache_read_input_tokens * 0.30
    ) / 1_000_000

    hit = u.cache_read_input_tokens / toplam * 100 if toplam else 0
    tasarruf = (1 - gercek / normal_maliyet) * 100 if normal_maliyet else 0

    print(f"Cache hit: %{hit:.0f} | Tasarruf: %{tasarruf:.0f} | Maliyet: ${gercek:.5f}")
    return gercek
```

---

## 5 Ölümcül Hata

```
❌ Dinamik içerik cache prefix'te
   "Şu an: {datetime.now()}" → her seferinde miss!
   Çözüm: Tarih/saat mesaj kısmına taşı

❌ Kullanıcıya özel prefix
   "Sen {kullanici_adi} için..." → her kullanıcı farklı cache
   Çözüm: Kullanıcı bilgisi message'da olsun

❌ Whitespace tutarsızlığı
   Bazen strip(), bazen değil → miss!
   Çözüm: " ".join(prompt.split()) — normalize et

❌ Minimum token altı (1024 Sonnet, 2048 Haiku)
   Kısa prompt → cache oluşmaz, sadece write primi ödersin

❌ Model güncellemesinde unutmak
   claude-sonnet-4-6 → claude-sonnet-4-7 → tüm cache sıfır!
   Çözüm: Model değişince warmup planla
```

---

## Minimum Gereksinimler

```
Model          Minimum Token
─────────────────────────────
Haiku 4.5      2.048 token
Sonnet 4.6     1.024 token
Opus 4.6       1.024 token
```
