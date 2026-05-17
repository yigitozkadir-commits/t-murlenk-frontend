#!/usr/bin/env python3
# agent_evals.py — Gök Umay Agent Kalite Test Sistemi
# ~/.claude/scripts/agent_evals.py
#
# KULLANIM:
#   python3 agent_evals.py              → tüm agent'ları test et
#   python3 agent_evals.py systematic-debugger  → tek agent test
#   python3 agent_evals.py --hizli      → sadece kritik 5 agent
#
# Her agent için beklenen girdi/çıktı çifti → geçer/kalır puanı.

import os
import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from anthropic import Anthropic

client = Anthropic()
EV = Path.home()
AGENT_DIR = EV / ".claude" / "agents"

# ── Veri yapıları ──────────────────────────────────────────────────────────────

@dataclass
class EvalCase:
    """Tek bir test vakası."""
    ad: str
    girdi: str
    beklenen_icerir: list[str]   # Çıktıda bu ifadelerden EN AZ BİRİ olmalı
    beklenen_icermez: list[str]  # Çıktıda bunlar OLMAMALI
    max_token: int = 400


@dataclass
class AgentEval:
    """Bir agent'ın tüm test vakaları."""
    agent_adi: str
    vakalar: list[EvalCase]
    model: str = "claude-haiku-4-5"  # Evals için ucuz model yeterli


@dataclass
class EvalSonuc:
    """Tek vaka sonucu."""
    vaka_adi: str
    gecti: bool
    puan: float          # 0.0 – 1.0
    yanit_ozeti: str
    sure_ms: int
    hatalar: list[str] = field(default_factory=list)


# ── Test Vakaları ─────────────────────────────────────────────────────────────

AGENT_EVALLARI: list[AgentEval] = [

    AgentEval("systematic-debugger", [
        EvalCase(
            "5-neden-teknik",
            "Three.js sahnesinde mesh'e tıklayamıyorum, raycaster çalışmıyor.",
            beklenen_icerir=["neden", "raycaster", "sahne", "mesh"],
            beklenen_icermez=["harika", "tabii ki", "mükemmel"],
        ),
        EvalCase(
            "token-kurali",
            "Bu dosyayı tamamen oku ve düzelt: [10000 satırlık dosya]",
            beklenen_icerir=["ilgili bölüm", "±20", "sadece"],
            beklenen_icermez=["tamamını okuyorum", "tüm dosyayı"],
        ),
    ]),

    AgentEval("technical-director", [
        EvalCase(
            "stack-karari",
            "Yeni çok oyunculu oyun için teknoloji seç: WebSocket mi, WebRTC mi?",
            beklenen_icerir=["WebSocket", "gecikme", "Supabase"],
            beklenen_icermez=["harika soru", "kesinlikle"],
        ),
        EvalCase(
            "csp-uyumu",
            "Oyuna Web Worker eklemek istiyorum.",
            beklenen_icerir=["CSP", "blob", "new Function", "fakeSelf"],
            beklenen_icermez=["sorun yok", "doğrudan ekle"],
        ),
    ]),

    AgentEval("game-designer", [
        EvalCase(
            "mekanik-tasarim",
            "Togyzool'a yeni bir mekanik eklemek istiyorum: taş çalma.",
            beklenen_icerir=["kural", "denge", "test", "tarih"],
            beklenen_icermez=["muhteşem", "süper fikir"],
        ),
        EvalCase(
            "denge-analiz",
            "Timurlenk'te beyaz çok sık kazanıyor (%65). Ne yapmalıyım?",
            beklened_icerir=["değerlendirme", "hamle", "AI", "denge"],
            beklenen_icermez=["bilmiyorum", "deneyebilirsin"],
        ),
    ]),

    AgentEval("security-auditor", [
        EvalCase(
            "xss-tespiti",
            "innerHTML = userInput kullanıyorum, sorun var mı?",
            beklenen_icerir=["XSS", "textContent", "sanitize", "güvenlik"],
            beklenen_icermez=["sorun yok", "gayet iyi"],
        ),
        EvalCase(
            "api-key-koruma",
            "Oyun kodunda Supabase key'i hard-code ettim.",
            beklenen_icerir=["env", "ortam değişkeni", "güvensiz", "sızdır"],
            beklenen_icermez=["sorun olmaz", "kabul edilebilir"],
        ),
    ]),

    AgentEval("qa-tester", [
        EvalCase(
            "test-plani",
            "Timurlenk v35 yayın öncesi test planı hazırla.",
            beklenen_icerir=["P0", "tarayıcı", "mobil", "performans"],
            beklenen_icermez=["harika", "muhteşem"],
        ),
        EvalCase(
            "edge-case",
            "Oyunda tahta doluyken hamle yapılmaya çalışılırsa ne olur?",
            beklenen_icerir=["sonsuz", "döngü", "edge case", "test"],
            beklenen_icermez=["önemli değil", "olası değil"],
        ),
    ]),

    AgentEval("voice-dna", [
        EvalCase(
            "reklam-tonu-reddet",
            "Şu metni düzelt: 'Muhteşem yeni oyunumuz çıktı! Harika bir deneyim!'",
            beklenen_icerir=["somut", "gerçek", "düzeltilmiş"],
            beklenen_icermez=["harika", "muhteşem", "!"],
        ),
        EvalCase(
            "humanizer-siralama",
            "Bu metni yayın için hazırla.",
            beklenen_icerir=["humanizer", "sıra"],
            beklenen_icermez=["direkt yayınla"],
        ),
    ]),

    AgentEval("performance-engineer", [
        EvalCase(
            "fps-analiz",
            "Oyunum 60 FPS'te başlayıp 5 dakikada 20 FPS'e düşüyor.",
            beklenen_icerir=["hafıza", "dispose", "sızıntı", "garbage"],
            beklenen_icermez=["yeniden başlat", "bilmiyorum"],
        ),
    ]),

    AgentEval("workflow-orchestrator", [
        EvalCase(
            "agent-zinciri",
            "Timurlenk v35'i yayınlamak istiyorum.",
            beklenen_icerir=["qa-tester", "security", "voice-dna", "humanizer"],
            beklenen_icermez=["direkt yayınla", "hemen yap"],
        ),
        EvalCase(
            "paralel-eslesme",
            "Hangi agent'lar aynı anda çalışabilir?",
            beklenen_icerir=["paralel", "sıralı", "bağımlılık"],
            beklenen_icermez=["hepsi aynı anda"],
        ),
    ]),
]

# game-designer'daki yazım hatasını düzelt
for ae in AGENT_EVALLARI:
    for v in ae.vakalar:
        if hasattr(v, "beklened_icerir"):
            v.beklenen_icerir = v.beklened_icerir  # type: ignore


# ── Değerlendirici ────────────────────────────────────────────────────────────

def agent_prompt_oku(agent_adi: str) -> str:
    yol = AGENT_DIR / f"{agent_adi}.md"
    if yol.exists():
        return yol.read_text(encoding="utf-8")
    return f"Sen {agent_adi} rolündesin. Gök Umay oyun stüdyosunda çalışıyorsun."


def tek_vaka_calistir(
    agent_adi: str, vaka: EvalCase, agent_prompt: str
) -> EvalSonuc:
    baslangic = time.time()

    yanit_metni = ""
    try:
        r = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=vaka.max_token,
            system=[{
                "type": "text",
                "text": agent_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": vaka.girdi}],
        )
        yanit_metni = r.content[0].text.lower()
    except Exception as e:
        sure = int((time.time() - baslangic) * 1000)
        return EvalSonuc(
            vaka_adi=vaka.ad,
            gecti=False,
            puan=0.0,
            yanit_ozeti=f"API hatası: {e}",
            sure_ms=sure,
            hatalar=[str(e)],
        )

    sure = int((time.time() - baslangic) * 1000)

    # ── Puanlama ──────────────────────────────────────────────────────────────
    hatalar: list[str] = []
    puan = 0.0

    # Beklenen içerikler (her biri eşit ağırlık)
    if vaka.beklenen_icerir:
        eslesme = sum(1 for k in vaka.beklenen_icerir if k.lower() in yanit_metni)
        icerik_puani = eslesme / len(vaka.beklenen_icerir)
        puan += icerik_puani * 0.7

        eksik = [k for k in vaka.beklenen_icerir if k.lower() not in yanit_metni]
        if eksik:
            hatalar.append(f"Eksik ifadeler: {eksik}")

    # Beklenmeyenler (herhangi biri varsa -0.3)
    if vaka.beklenen_icermez:
        yasak = [k for k in vaka.beklenen_icermez if k.lower() in yanit_metni]
        if yasak:
            puan -= 0.3
            hatalar.append(f"Yasak ifadeler bulundu: {yasak}")
        else:
            puan += 0.3

    puan = max(0.0, min(1.0, puan))
    gecti = puan >= 0.6

    return EvalSonuc(
        vaka_adi=vaka.ad,
        gecti=gecti,
        puan=puan,
        yanit_ozeti=yanit_metni[:150] + "...",
        sure_ms=sure,
        hatalar=hatalar,
    )


# ── Rapor ─────────────────────────────────────────────────────────────────────

def agent_test_et(ae: AgentEval) -> tuple[float, list[EvalSonuc]]:
    """Bir agent'ı tüm vakalarıyla test et. Ortalama puan döndür."""
    print(f"\n🤖 {ae.agent_adi}")
    print("   " + "─" * 40)

    prompt = agent_prompt_oku(ae.agent_adi)
    sonuclar: list[EvalSonuc] = []

    for vaka in ae.vakalar:
        sonuc = tek_vaka_calistir(ae.agent_adi, vaka, prompt)
        sonuclar.append(sonuc)

        durum = "✅" if sonuc.gecti else "❌"
        print(f"   {durum} [{vaka.ad}] puan={sonuc.puan:.2f} ({sonuc.sure_ms}ms)")
        for h in sonuc.hatalar:
            print(f"      ⚠️  {h}")

    ort = sum(s.puan for s in sonuclar) / len(sonuclar) if sonuclar else 0.0
    return ort, sonuclar


def tam_rapor(hedef: str | None = None, hizli: bool = False):
    """Tüm veya seçili agent'ları test et, JSON raporu kaydet."""
    evaller = AGENT_EVALLARI
    if hedef:
        evaller = [ae for ae in AGENT_EVALLARI if ae.agent_adi == hedef]
        if not evaller:
            print(f"❌ Agent bulunamadı: {hedef}")
            print(f"   Mevcut: {[ae.agent_adi for ae in AGENT_EVALLARI]}")
            return
    if hizli:
        kritikler = {"systematic-debugger", "security-auditor", "qa-tester",
                     "workflow-orchestrator", "technical-director"}
        evaller = [ae for ae in evaller if ae.agent_adi in kritikler]

    print("\n🧪 Gök Umay Agent Evals")
    print("=" * 50)

    genel: dict[str, float] = {}
    tum_sonuclar: dict[str, list[dict]] = {}

    for ae in evaller:
        ort, sonuclar = agent_test_et(ae)
        genel[ae.agent_adi] = ort
        tum_sonuclar[ae.agent_adi] = [
            {
                "vaka": s.vaka_adi,
                "gecti": s.gecti,
                "puan": round(s.puan, 2),
                "sure_ms": s.sure_ms,
                "hatalar": s.hatalar,
            }
            for s in sonuclar
        ]

    # Özet
    print("\n" + "=" * 50)
    print("📊 ÖZET")
    print("=" * 50)
    gecenler = 0
    for adi, puan in sorted(genel.items(), key=lambda x: x[1], reverse=True):
        durum = "✅" if puan >= 0.6 else "❌"
        print(f"   {durum} {adi:<30} {puan:.0%}")
        if puan >= 0.6:
            gecenler += 1

    genel_ort = sum(genel.values()) / len(genel) if genel else 0
    print(f"\n   Genel: {genel_ort:.0%} ({gecenler}/{len(genel)} agent geçti)")

    # JSON raporu kaydet
    rapor_yolu = EV / ".claude" / "logs" / "eval_rapor.json"
    rapor_yolu.parent.mkdir(exist_ok=True)
    rapor_yolu.write_text(json.dumps({
        "tarih": time.strftime("%Y-%m-%d %H:%M"),
        "genel_ort": round(genel_ort, 2),
        "agent_sayisi": len(genel),
        "gecen_sayisi": gecenler,
        "sonuclar": tum_sonuclar,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n   Rapor: {rapor_yolu}")

    # Başarısız agent'lar için önerir
    basarisizlar = [a for a, p in genel.items() if p < 0.6]
    if basarisizlar:
        print(f"\n   ⚠️  Düzeltilmesi gerekenler: {basarisizlar}")

    return genel_ort


# ── Sürekli İzleme ─────────────────────────────────────────────────────────────

def gecmiş_karsilastir():
    """Son 2 raporu karşılaştır — regresyon var mı?"""
    rapor_yolu = EV / ".claude" / "logs" / "eval_rapor.json"
    eski_yol = EV / ".claude" / "logs" / "eval_rapor_onceki.json"

    if not rapor_yolu.exists():
        print("❌ Rapor bulunamadı — önce test çalıştır")
        return

    # Mevcut raporu "onceki" olarak kopyala
    if rapor_yolu.exists():
        import shutil
        shutil.copy(rapor_yolu, eski_yol)
        print(f"📋 Referans kaydedildi: {eski_yol}")


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    hedef = None
    hizli = "--hizli" in sys.argv

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            hedef = arg
            break

    tam_rapor(hedef=hedef, hizli=hizli)
