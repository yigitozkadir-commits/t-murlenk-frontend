---
name: multi-agent-coordinator
description: |
  Agent zinciri kurma, paralel çalıştırma, model seçimi.
  Subagent API kullanım kalıpları ve maliyet optimizasyonu.
  Kullan: "multi-agent-coordinator ile zincir kur"
---

# Multi-Agent Koordinasyon

## TOKEN KURALI
Her agent için ayrı Claude çağrısı — cache kullan, Haiku tercih et.

---

## Temel Zincir Kalıbı

```python
import anthropic
import os
from pathlib import Path

client = anthropic.Anthropic()

def agent(rol: str, gorev: str, bagłam: str = "", model: str = None) -> str:
    """Tek agent çalıştır — cache uyumlu"""
    dosya = Path.home() / f".claude/agents/{rol}.md"
    sistem = dosya.read_text() if dosya.exists() else f"{rol} rolündesin."

    # Model seçimi — belirtilmezse role göre otomatik
    if not model:
        model = MODEL_HARITA.get(rol, "claude-sonnet-4-6")

    mesajlar = []
    if bagłam:
        mesajlar.append({"role": "user", "content": f"Bağlam:\n{bagłam}"})
        mesajlar.append({"role": "assistant", "content": "Anladım."})
    mesajlar.append({"role": "user", "content": gorev})

    r = client.messages.create(
        model=model,
        max_tokens=1500,
        system=[{"type": "text", "text": sistem,
                 "cache_control": {"type": "ephemeral"}}],
        messages=mesajlar
    )
    return r.content[0].text

MODEL_HARITA = {
    # Haiku — hızlı, ucuz, yeterli
    "systematic-debugger":  "claude-haiku-4-5",
    "qa-tester":            "claude-haiku-4-5",
    "performance-engineer": "claude-haiku-4-5",
    "voice-dna":            "claude-haiku-4-5",
    "content-marketer":     "claude-haiku-4-5",
    "humanizer":            "claude-haiku-4-5",

    # Sonnet — denge
    "game-designer":        "claude-sonnet-4-6",
    "narrative-director":   "claude-sonnet-4-6",
    "security-auditor":     "claude-sonnet-4-6",
    "research-analyst":     "claude-sonnet-4-6",
    "ai-engineer":          "claude-sonnet-4-6",

    # Opus — kritik kararlar
    "technical-director":   "claude-opus-4-6",
}
```

---

## Paralel Çalıştırma

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def paralel(gorevler: list[dict]) -> list[str]:
    """
    gorevler = [
        {"rol": "qa-tester", "gorev": "..."},
        {"rol": "security-auditor", "gorev": "..."},
    ]
    """
    loop = asyncio.get_event_loop()
    isler = [
        loop.run_in_executor(executor, lambda g=g: agent(g["rol"], g["gorev"], g.get("bagłam", "")))
        for g in gorevler
    ]
    return await asyncio.gather(*isler)
```

---

## Hazır Zincirler

### Versiyon Geçiş Zinciri
```python
async def versiyon_gec(dosya: str):
    # Paralel analiz
    bug, perf, guv = await paralel([
        {"rol": "systematic-debugger",  "gorev": f"{dosya} hatalarını P0-P3 listele"},
        {"rol": "performance-engineer", "gorev": f"{dosya} performans sorunları"},
        {"rol": "security-auditor",     "gorev": f"{dosya} güvenlik taraması"},
    ])

    # QA kararı — önceki sonuçlarla
    qa = agent("qa-tester", "Yayın kararı ver",
               bagłam=f"Bug:\n{bug}\n\nPerf:\n{perf}\n\nGüv:\n{guv}")

    # Belgeleme
    if "✅" in qa:
        doc = agent("documentation", f"{dosya} değişiklik günlüğü", bug)
        return {"durum": "ONAYLANDI", "qa": qa, "belge": doc}
    return {"durum": "REDDEDİLDİ", "qa": qa}
```

### İçerik Zinciri
```python
async def icerik_uret(konu: str, platform: str):
    # Taslak
    taslak = agent("content-marketer", f"{konu} için {platform} içeriği")

    # Ses uyarlama
    ses = agent("voice-dna", "Mehmet'in sesiyle yaz", taslak)

    # Temizlik
    temiz = agent("humanizer", "AI izlerini kaldır", ses)

    return temiz
```

---

## Maliyet Hesabı

```python
def maliyet_tahmin(zincir: list[dict]) -> float:
    """Agent zinciri maliyet tahmini (USD)"""
    fiyatlar = {
        "claude-haiku-4-5":   {"input": 0.80,  "output": 4.00},    # $/M token
        "claude-sonnet-4-6":  {"input": 3.00,  "output": 15.00},
        "claude-opus-4-6":    {"input": 15.00, "output": 75.00},
    }

    toplam = 0.0
    for gorev in zincir:
        model = MODEL_HARITA.get(gorev["rol"], "claude-sonnet-4-6")
        f = fiyatlar[model]
        # Ortalama tahmini: 500 input + 500 output token/agent
        toplam += (500 * f["input"] + 500 * f["output"]) / 1_000_000

    return toplam

# Örnek:
# versiyon_gec zinciri = 5 agent
# Haiku×3 + Sonnet×1 + Haiku×1 ≈ $0.003 per run
```
