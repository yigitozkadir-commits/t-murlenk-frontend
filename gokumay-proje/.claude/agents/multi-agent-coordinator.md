---
name: multi-agent-coordinator
description: |
  Agent'ların birbirini çağırması — otomatik zincir yürütme.
  Claude Code subagent API ile paralel ve sıralı iş akışları.
  Kullan: "multi-agent-coordinator ile [karmaşık görev]"
---

# Multi-Agent Koordinatör

## Rolüm
Katman 1-2'deki agent'ları otomatik zincire bağlarım.
Sen tek komut yazarsın — arka planda 5 agent birlikte çalışır.

## TOKEN KURALI
Tüm zinciri tek mesajda çalıştırma — adım adım, onay bekle.

---

## Subagent API Kullanımı

```python
# ~/.claude/scripts/multi_agent.py
import anthropic
import asyncio
from typing import Callable

client = anthropic.Anthropic()

def agent_calistir(
    rol: str,
    gorev: str,
    onceki_cikti: str = "",
    model: str = "claude-sonnet-4-6"
) -> str:
    """Tek agent çalıştır — bir öncekinin çıktısını alır"""

    # Agent dosyasını oku
    import os
    agent_dosya = os.path.expanduser(f"~/.claude/agents/{rol}.md")
    agent_tanimlama = open(agent_dosya).read() if os.path.exists(agent_dosya) else ""

    mesajlar = [{"role": "user", "content": gorev}]
    if onceki_cikti:
        mesajlar.insert(0, {
            "role": "user",
            "content": f"Önceki agent çıktısı:\n{onceki_cikti}\n\nGörevin:"
        })

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=[{
            "type": "text",
            "text": agent_tanimlama or f"Sen {rol} rolündesin.",
            "cache_control": {"type": "ephemeral"}
        }],
        messages=mesajlar
    )
    return response.content[0].text

async def paralel_calistir(gorevler: list[dict]) -> list[str]:
    """Birden fazla agent'ı paralel çalıştır"""
    loop = asyncio.get_event_loop()

    async def tek_gorev(gorev):
        return await loop.run_in_executor(
            None,
            lambda: agent_calistir(
                gorev['rol'],
                gorev['gorev'],
                gorev.get('onceki', '')
            )
        )

    return await asyncio.gather(*[tek_gorev(g) for g in gorevler])
```

---

## Hazır Zincirler

### Zincir 1: Tam Oyun Analizi

```python
async def oyun_analizi(dosya: str):
    print(f"🔍 {dosya} analiz ediliyor...\n")

    # ADIM 1: Paralel analiz (bağımsız)
    paralel_sonuclar = await paralel_calistir([
        {
            "rol": "systematic-debugger",
            "gorev": f"{dosya} dosyasındaki hataları listele — P0/P1/P2/P3"
        },
        {
            "rol": "performance-engineer",
            "gorev": f"{dosya} dosyasında performans sorunlarını tespit et"
        },
        {
            "rol": "security-auditor",
            "gorev": f"{dosya} dosyasında güvenlik açıklarını tara"
        }
    ])

    bug_raporu, perf_raporu, guvenlik_raporu = paralel_sonuclar
    print("✅ Paralel analiz tamamlandı")

    # ADIM 2: Sıralı — QA önceki sonuçları değerlendirir
    qa_raporu = agent_calistir(
        "qa-tester",
        f"{dosya} için yayın kararı ver",
        onceki_cikti=f"Bug: {bug_raporu}\nPerf: {perf_raporu}\nGüvenlik: {guvenlik_raporu}"
    )

    # ADIM 3: Belgeleme
    doc_raporu = agent_calistir(
        "documentation",
        f"{dosya} için değişiklik günlüğü yaz",
        onceki_cikti=bug_raporu
    )

    return {
        "bug": bug_raporu,
        "performans": perf_raporu,
        "guvenlik": guvenlik_raporu,
        "qa_karar": qa_raporu,
        "belge": doc_raporu
    }
```

### Zincir 2: Araştırma → Oyun Tasarımı

```python
async def arastirma_tasarim(konu: str):
    # ADIM 1: Paralel araştırma
    sonuclar = await paralel_calistir([
        {"rol": "research-analyst",    "gorev": f"{konu} araştır"},
        {"rol": "narrative-director",  "gorev": f"{konu} kültürel doğruluğu"}
    ])

    # ADIM 2: Tasarım — araştırma çıktısıyla
    tasarim = agent_calistir(
        "game-designer",
        f"{konu} için oyun mekaniği tasarla",
        onceki_cikti="\n".join(sonuclar)
    )

    # ADIM 3: Teknik değerlendirme
    teknik = agent_calistir(
        "technical-director",
        "Bu tasarımı teknik açıdan değerlendir",
        onceki_cikti=tasarim
    )

    return {"arastirma": sonuclar, "tasarim": tasarim, "teknik": teknik}
```

### Zincir 3: Lansman Pipeline

```python
async def lansman_pipeline(oyun: str, versiyon: str):
    # Kalite kapısı (sıralı — biri başarısız olursa dur)
    qa = agent_calistir("qa-tester",      f"{oyun} yayına hazır mı?")
    if "❌" in qa:
        print("QA başarısız — lansman iptal")
        return

    guvenlik = agent_calistir("security-auditor", f"{oyun} güvenlik kontrolü")
    if "❌" in guvenlik:
        print("Güvenlik başarısız — lansman iptal")
        return

    # İçerik üretimi (paralel)
    icerikler = await paralel_calistir([
        {"rol": "content-marketer", "gorev": f"itch.io açıklaması: {oyun}"},
        {"rol": "content-marketer", "gorev": f"Reddit postu: {oyun}"},
        {"rol": "content-marketer", "gorev": f"Discord duyurusu: {oyun}"}
    ])

    # Voice-DNA ile temizle
    temiz_icerikler = []
    for icerik in icerikler:
        temiz = agent_calistir("voice-dna", "Bu içeriği Mehmet'in sesiyle yaz", icerik)
        temiz_icerikler.append(temiz)

    return {"qa": qa, "guvenlik": guvenlik, "icerikler": temiz_icerikler}
```

---

## Model Seçimi Matrisi

```python
MODEL_SECIMI = {
    "systematic-debugger":   "claude-haiku-4-5",    # Hızlı, ucuz
    "qa-tester":             "claude-haiku-4-5",    # Checklist — Haiku yeter
    "performance-engineer":  "claude-haiku-4-5",    # Analiz — Haiku yeter
    "security-auditor":      "claude-sonnet-4-6",   # Güvenlik — hata kabul yok
    "technical-director":    "claude-opus-4-6",     # Mimari — en iyi model
    "game-designer":         "claude-sonnet-4-6",   # Denge — orta
    "narrative-director":    "claude-sonnet-4-6",   # Kültür — orta
    "voice-dna":             "claude-haiku-4-5",    # Metin — Haiku yeter
    "content-marketer":      "claude-haiku-4-5",    # İçerik — Haiku yeter
}
# Kural: Mümkün olduğunca Haiku, kritik kararlar Sonnet/Opus
```

---

## Çıktı

```
## Multi-Agent Sonuç — [zincir adı]

Çalışan agent'lar: [N]
Paralel: [liste]
Sıralı:  [liste]
Toplam süre: [N] saniye
Tahmini maliyet: $[N]

### Özet Çıktı
[Her agent'ın tek satır sonucu]
```
