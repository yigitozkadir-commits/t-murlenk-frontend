#!/usr/bin/env python3
# agent_evals_tam.py — Gök Umay Tüm 30 Agent Kalite Testi
# ~/.claude/scripts/agent_evals_tam.py
#
# Önceki agent_evals.py'nin yerine geçer — tüm 30 agent kapsanıyor.
#
# KULLANIM:
#   python3 agent_evals_tam.py              → tüm 30 agent
#   python3 agent_evals_tam.py qa-tester    → tek agent
#   python3 agent_evals_tam.py --hizli      → 5 kritik agent
#   python3 agent_evals_tam.py --katman 1   → sadece Katman 1 (20 agent)
#   python3 agent_evals_tam.py --katman 2   → sadece Katman 2 (4 agent)
#   python3 agent_evals_tam.py --katman 3   → sadece Katman 3 (6 agent)

import os, sys, json, time
from pathlib import Path
from dataclasses import dataclass, field
from anthropic import Anthropic

client = Anthropic()
EV = Path.home()
AGENT_DIR = EV / ".claude" / "agents"

@dataclass
class EvalCase:
    ad: str
    girdi: str
    beklenen_icerir: list[str]
    beklenen_icermez: list[str]
    max_token: int = 400

@dataclass
class AgentEval:
    agent_adi: str
    katman: int
    vakalar: list[EvalCase]

@dataclass
class EvalSonuc:
    vaka_adi: str
    gecti: bool
    puan: float
    sure_ms: int
    hatalar: list[str] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════════════
# KATMAN 1 — 20 AGENT
# ══════════════════════════════════════════════════════════════════════════════

KATMAN1: list[AgentEval] = [

    AgentEval("systematic-debugger", 1, [
        EvalCase("5-neden",
            "Three.js sahnesinde raycaster çalışmıyor, mesh'e tıklayamıyorum.",
            ["neden", "raycaster", "sahne"],
            ["harika", "tabii ki"]),
        EvalCase("token-kurali",
            "Bu 10.000 satırlık dosyayı tamamen oku.",
            ["ilgili bölüm", "sadece"],
            ["tamamını okuyorum"]),
    ]),

    AgentEval("technical-director", 1, [
        EvalCase("stack-karari",
            "Yeni çok oyunculu oyun için WebSocket mi WebRTC mi?",
            ["gecikme", "Supabase", "WebSocket"],
            ["kesinlikle", "harika soru"]),
        EvalCase("csp-uyumu",
            "Oyuna Web Worker eklemek istiyorum.",
            ["CSP", "blob", "new Function"],
            ["sorun yok", "doğrudan ekle"]),
    ]),

    AgentEval("game-designer", 1, [
        EvalCase("denge-analiz",
            "Timurlenk'te beyaz %65 kazanıyor. Ne yapmalıyım?",
            ["denge", "değerlendirme", "AI"],
            ["bilmiyorum"]),
        EvalCase("mekanik-karar",
            "Togyzool'a taş çalma mekaniği ekleyelim mi?",
            ["kural", "tarih", "test"],
            ["süper fikir"]),
    ]),

    AgentEval("qa-tester", 1, [
        EvalCase("test-plani",
            "Timurlenk v35 yayın öncesi test planı.",
            ["P0", "tarayıcı", "mobil"],
            ["harika", "muhteşem"]),
        EvalCase("edge-case",
            "Tahta doluyken hamle yapılmaya çalışılırsa?",
            ["sonsuz", "edge case", "test"],
            ["olası değil"]),
    ]),

    AgentEval("project-manager", 1, [
        EvalCase("sprint-plani",
            "Bu hafta hem Timurlenk v35 hem Togyzool AI'ı bitiremem, hangisini seçelim?",
            ["öncelik", "sprint", "risk"],
            ["ikisini de yap"]),
        EvalCase("tahmın",
            "Timurlenk'e 3D animasyon eklemek ne kadar sürer?",
            ["gün", "risk", "bağımlılık"],
            ["1 saat", "basit"]),
    ]),

    AgentEval("narrative-director", 1, [
        EvalCase("kulturel-dogruluk",
            "Timurlenk oyununda 'Kral' yerine ne demeliyim?",
            ["Şah", "tarihi", "kaynak"],
            ["king", "önemli değil"]),
        EvalCase("kaynak-kontrolu",
            "Deve taşının hareket kuralını nereden doğrulayabilirim?",
            ["Murray", "1913", "kaynak"],
            ["Wikipedia", "uydur"]),
    ]),

    AgentEval("refactorer", 1, [
        EvalCase("tekrar-kod",
            "3 farklı oyunda aynı minimax kodu var, ne yapmalıyım?",
            ["fonksiyon", "ortak", "modül"],
            ["kopyala-yapıştır", "sorun değil"]),
        EvalCase("buyuk-dosya",
            "timurlenk.html 8000 satır oldu.",
            ["bölüm", "modül", "okunabilirlik"],
            ["sorun yok", "normal"]),
    ]),

    AgentEval("performance-engineer", 1, [
        EvalCase("fps-dusus",
            "5 dakikada 60 FPS'ten 20 FPS'e düşüyor.",
            ["hafıza", "dispose", "sızıntı"],
            ["yeniden başlat"]),
        EvalCase("mobil-optimizasyon",
            "Android'de oyun çok yavaş.",
            ["üçgen", "pixelRatio", "gölge"],
            ["sorun değil", "zayıf cihaz"]),
    ]),

    AgentEval("security-auditor", 1, [
        EvalCase("xss",
            "innerHTML = userInput kullanıyorum.",
            ["XSS", "textContent", "sanitize"],
            ["sorun yok"]),
        EvalCase("api-key",
            "Supabase key'i HTML'e gömdüm.",
            ["env", "ortam değişkeni", "güvensiz"],
            ["sorun olmaz"]),
    ]),

    AgentEval("launch-strategy", 1, [
        EvalCase("lansman-zamanlama",
            "Timurlenk'i ne zaman yayınlamalıyım?",
            ["hedef", "kitle", "platform"],
            ["hemen", "bekle"]),
        EvalCase("platform-secimi",
            "itch.io mu Play Store mu önce?",
            ["itch", "HTML5", "mobil", "önce"],
            ["ikisi aynı"]),
    ]),

    AgentEval("content-marketer", 1, [
        EvalCase("itch-aciklama",
            "Timurlenk için itch.io açıklaması yaz.",
            ["tarihi", "11x10", "Murray"],
            ["muhteşem", "harika", "!"]),
        EvalCase("reddit-post",
            "r/chess için Timurlenk tanıtım postu.",
            ["variant", "historical", "browser"],
            ["amazing", "incredible"]),
    ]),

    AgentEval("research-analyst", 1, [
        EvalCase("kaynak-analiz",
            "Togyzool için hangi akademik kaynaklar var?",
            ["kaynak", "tarih", "araştır"],
            ["bilmiyorum", "yok"]),
        EvalCase("rekabet-analiz",
            "Browser'da çalışan diğer tarihi satranç oyunları neler?",
            ["rakip", "browser", "karşılaştır"],
            ["yok", "teksin"]),
    ]),

    AgentEval("ai-engineer", 1, [
        EvalCase("minimax-impl",
            "Togyzool için minimax AI nasıl yazarım?",
            ["minimax", "değerlendirme", "derinlik"],
            ["mümkün değil", "zor"]),
        EvalCase("csp-motor",
            "AI motoru CSP ihlali yapıyor.",
            ["new Function", "fakeSelf", "blob"],
            ["eval", "Worker"]),
    ]),

    AgentEval("ui-designer", 1, [
        EvalCase("tahta-tasarimi",
            "11x10 Timurlenk tahtası için renk şeması öner.",
            ["kontrast", "erişilebilirlik", "Three.js"],
            ["istediğin rengi"]),
        EvalCase("mobil-ui",
            "Dokunmatik ekran için taş seçim UI'ı.",
            ["dokunmatik", "hedef", "piksel"],
            ["mouse ile aynı"]),
    ]),

    AgentEval("voice-dna", 1, [
        EvalCase("reklam-tonu",
            "Düzelt: 'Muhteşem yeni oyunumuz harika bir deneyim sunuyor!'",
            ["somut", "düzeltilmiş"],
            ["muhteşem", "harika"]),
        EvalCase("humanizer-sira",
            "Metni hazırla.",
            ["humanizer"],
            ["direkt yayınla"]),
    ]),

    AgentEval("documentation", 1, [
        EvalCase("degisiklik-log",
            "v34'ten v35'e Deve taşı hareketi düzeltildi. Changelog yaz.",
            ["v35", "Deve", "düzeltildi"],
            ["harika güncelleme"]),
        EvalCase("api-doku",
            "AIBridge kayıt sistemi için dokümantasyon.",
            ["fonksiyon", "parametre", "örnek"],
            ["kendin anla"]),
    ]),

    AgentEval("competitive-analyst", 1, [
        EvalCase("rakip-analiz",
            "Lichess ve Chess.com'un olmadığı boşluk nerede?",
            ["tarihi", "varyant", "niş"],
            ["rakip yok", "aynısını yap"]),
        EvalCase("farklilasma",
            "Gök Umay'ı diğer indie oyun stüdyolarından ayıran ne?",
            ["Türk", "tarihi", "kültür"],
            ["hiçbir fark yok"]),
    ]),

    AgentEval("mobile-developer", 1, [
        EvalCase("capacitor-paket",
            "HTML5 oyunu Play Store'a nasıl yüklerim?",
            ["Capacitor", "AAB", "SDK"],
            ["doğrudan yükle"]),
        EvalCase("ios-ses",
            "iOS'ta ses çıkmıyor.",
            ["AudioContext", "resume", "dokunuş"],
            ["iOS sorunu değil"]),
    ]),

    AgentEval("workflow-orchestrator", 1, [
        EvalCase("agent-zinciri",
            "Timurlenk v35 yayın süreci.",
            ["qa-tester", "security", "voice-dna"],
            ["direkt yayınla"]),
        EvalCase("paralel-calisma",
            "Hangi agent'lar aynı anda çalışabilir?",
            ["paralel", "sıralı", "bağımlılık"],
            ["hepsi aynı anda"]),
    ]),

    AgentEval("skill-creator", 1, [
        EvalCase("skill-tasarim",
            "Togyzool için yeni bir skill tasarla.",
            ["SKILL.md", "TOKEN KURALI", "referans"],
            ["agent gibi yaz"]),
        EvalCase("skill-test",
            "Yazdığım skill doğru mu?",
            ["test", "girdi", "çıktı"],
            ["evet doğru", "mükemmel"]),
    ]),
]


# ══════════════════════════════════════════════════════════════════════════════
# KATMAN 2 — 4 AGENT
# ══════════════════════════════════════════════════════════════════════════════

KATMAN2: list[AgentEval] = [

    AgentEval("n8n-orchestrator", 2, [
        EvalCase("workflow-tasarim",
            "Discord'dan gelen bug raporunu GitHub'a otomatik aktaran workflow tasarla.",
            ["webhook", "node", "GitHub", "Discord"],
            ["manuel yap", "mümkün değil"]),
        EvalCase("maliyet-optimizasyon",
            "n8n workflow'um çok fazla API çağrısı yapıyor.",
            ["batch", "rate limit", "önbellek"],
            ["sorun değil"]),
    ]),

    AgentEval("memory-manager", 2, [
        EvalCase("kaydet-karari",
            "Raycaster bug'ını 5 Neden ile çözdüm. Kaydetmeli miyim?",
            ["kaydet", "kategori", "bug"],
            ["gerek yok", "unut"]),
        EvalCase("hatirla-sorgu",
            "Daha önce Three.js hafıza sızıntısı sorunuyla karşılaştık mı?",
            ["sorgula", "benzerlik", "semantik"],
            ["bilmiyorum", "hayır"]),
    ]),

    AgentEval("publisher", 2, [
        EvalCase("uclu-kapi",
            "Timurlenk v35'i yayınlamak istiyorum.",
            ["qa-tester", "security", "performance"],
            ["hemen yayınla", "direkt"]),
        EvalCase("platform-paralel",
            "itch.io ve Play Store için içerik üret.",
            ["paralel", "platform", "içerik"],
            ["sırayla yap"]),
    ]),

    AgentEval("analytics-reporter", 2, [
        EvalCase("metrik-rapor",
            "Timurlenk'in bu haftaki performans raporu.",
            ["indirme", "görüntülenme", "retention"],
            ["iyi gidiyor", "kötü gidiyor"]),
        EvalCase("kpi-belirleme",
            "Başarıyı nasıl ölçeceğiz?",
            ["KPI", "hedef", "ölçüm"],
            ["sezgiyle", "hissedersin"]),
    ]),
]


# ══════════════════════════════════════════════════════════════════════════════
# KATMAN 3 — 6 AGENT
# ══════════════════════════════════════════════════════════════════════════════

KATMAN3: list[AgentEval] = [

    AgentEval("mcp-server-builder", 3, [
        EvalCase("araç-tasarim",
            "itch.io istatistiklerini çeken MCP aracı tasarla.",
            ["tool", "inputSchema", "handler"],
            ["yapamam", "API yok"]),
        EvalCase("mcp-kurulum",
            "MCP aracını Claude Code'a nasıl eklerim?",
            ["claude mcp add", "stdio", "tsx"],
            ["manuel yaz"]),
    ]),

    AgentEval("rag-pipeline", 3, [
        EvalCase("chunk-strateji",
            "Timurlenk GDD'sini RAG'a yükleyeceğim, chunk boyutu ne olmalı?",
            ["token", "500", "800", "örtüşme"],
            ["farketmez", "1000"]),
        EvalCase("semantik-sorgu",
            "Raycaster sorunuyla ilgili geçmiş kayıtları nasıl sorgularım?",
            ["embedding", "benzerlik", "pgvector"],
            ["CTRL+F", "grep"]),
    ]),

    AgentEval("multi-agent-coordinator", 3, [
        EvalCase("zincir-calistir",
            "/chain lansman timurlenk komutu ne yapar?",
            ["agent", "zincir", "sıralı", "paralel"],
            ["tek agent", "basit"]),
        EvalCase("model-secim",
            "Bu zincirde hangi model kullanılmalı?",
            ["Haiku", "Sonnet", "Opus", "maliyet"],
            ["hep Opus", "fark etmez"]),
    ]),

    AgentEval("playtest-ai", 3, [
        EvalCase("denge-testi",
            "Timurlenk'te beyaz ve siyahın kazanma oranını test et.",
            ["simülasyon", "%50", "denge"],
            ["elle oyna", "tahmin et"]),
        EvalCase("sonsuz-dongu",
            "Oyunda sonsuz döngü var mı nasıl anlarım?",
            ["pozisyon", "hash", "tekrar"],
            ["süre ölç", "göz at"]),
    ]),

    AgentEval("monetization-optimizer", 3, [
        EvalCase("fiyat-strateji",
            "Timurlenk için fiyatlandırma stratejisi.",
            ["freemium", "pay what you want", "dönüşüm"],
            ["ücretsiz olmaz", "pahalı sat"]),
        EvalCase("aso-optimizasyon",
            "Play Store'da oyun bulunmuyor.",
            ["ASO", "anahtar kelime", "başlık"],
            ["reklam ver", "bekle"]),
    ]),

    AgentEval("community-manager", 3, [
        EvalCase("discord-strateji",
            "Discord sunucumuzu nasıl büyütelim?",
            ["içerik", "düzenli", "etkileşim"],
            ["reklam", "hemen büyür"]),
        EvalCase("reddit-etik",
            "Yorumlara otomatik cevap verecek bot.",
            ["spam", "limit", "doğal"],
            ["hepsine cevap ver", "sınırsız"]),
    ]),
]


# ══════════════════════════════════════════════════════════════════════════════
# ÇALIŞTIRICI
# ══════════════════════════════════════════════════════════════════════════════

TUM_EVALLER = KATMAN1 + KATMAN2 + KATMAN3

KRITIK_5 = {"systematic-debugger", "security-auditor", "qa-tester",
             "workflow-orchestrator", "technical-director"}


def agent_prompt_oku(adi: str) -> str:
    yol = AGENT_DIR / f"{adi}.md"
    return yol.read_text(encoding="utf-8") if yol.exists() else f"Sen {adi} rolündesin."


def vaka_calistir(adi: str, vaka: EvalCase, prompt: str) -> EvalSonuc:
    t0 = time.time()
    try:
        r = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=vaka.max_token,
            system=[{"type": "text", "text": prompt, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": vaka.girdi}],
        )
        yanit = r.content[0].text.lower()
    except Exception as e:
        return EvalSonuc(vaka.ad, False, 0.0, int((time.time()-t0)*1000), [str(e)])

    sure = int((time.time()-t0)*1000)
    hatalar = []
    puan = 0.0

    if vaka.beklenen_icerir:
        eslesme = sum(1 for k in vaka.beklenen_icerir if k.lower() in yanit)
        puan += (eslesme / len(vaka.beklenen_icerir)) * 0.7
        eksik = [k for k in vaka.beklenen_icerir if k.lower() not in yanit]
        if eksik:
            hatalar.append(f"Eksik: {eksik}")

    if vaka.beklenen_icermez:
        yasak = [k for k in vaka.beklenen_icermez if k.lower() in yanit]
        puan += 0.3 if not yasak else 0.0
        if yasak:
            hatalar.append(f"Yasak ifade: {yasak}")

    puan = round(max(0.0, min(1.0, puan)), 2)
    return EvalSonuc(vaka.ad, puan >= 0.6, puan, sure, hatalar)


def agent_test_et(ae: AgentEval) -> tuple[float, list[EvalSonuc]]:
    print(f"\n  🤖 [{ae.katman}] {ae.agent_adi}")
    prompt = agent_prompt_oku(ae.agent_adi)
    sonuclar = [vaka_calistir(ae.agent_adi, v, prompt) for v in ae.vakalar]
    for s in sonuclar:
        print(f"     {'✅' if s.gecti else '❌'} {s.vaka_adi} ({s.puan:.0%}, {s.sure_ms}ms)")
        for h in s.hatalar:
            print(f"        ⚠️  {h}")
    ort = sum(s.puan for s in sonuclar) / len(sonuclar)
    return ort, sonuclar


def rapor_yaz(genel: dict, tum_sonuclar: dict, katman_filter: int | None):
    gecenler = sum(1 for p in genel.values() if p >= 0.6)
    ort = sum(genel.values()) / len(genel) if genel else 0

    print("\n" + "═" * 55)
    print("📊 ÖZET")
    print("═" * 55)
    for adi, puan in sorted(genel.items(), key=lambda x: x[1], reverse=True):
        print(f"  {'✅' if puan>=0.6 else '❌'} {adi:<30} {puan:.0%}")
    print(f"\n  Genel: {ort:.0%} ({gecenler}/{len(genel)} geçti)")

    rapor_yolu = EV / ".claude" / "logs" / "eval_rapor.json"
    rapor_yolu.parent.mkdir(exist_ok=True)
    rapor_yolu.write_text(json.dumps({
        "tarih": time.strftime("%Y-%m-%d %H:%M"),
        "genel_ort": round(ort, 2),
        "gecen": gecenler,
        "toplam": len(genel),
        "sonuclar": tum_sonuclar,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  📄 Rapor: {rapor_yolu}")

    basarisiz = [a for a, p in genel.items() if p < 0.6]
    if basarisiz:
        print(f"\n  ⚠️  Düzelt: {basarisiz}")


def main():
    hedef = None
    hizli = "--hizli" in sys.argv
    katman_filter = None

    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--katman" and i+2 <= len(sys.argv)-1:
            katman_filter = int(sys.argv[i+2])
        elif not arg.startswith("--"):
            hedef = arg

    evaller = TUM_EVALLER
    if hedef:
        evaller = [ae for ae in TUM_EVALLER if ae.agent_adi == hedef]
        if not evaller:
            print(f"❌ Bulunamadı: {hedef}")
            print(f"   Mevcut: {[ae.agent_adi for ae in TUM_EVALLER]}")
            return
    elif katman_filter:
        evaller = [ae for ae in TUM_EVALLER if ae.katman == katman_filter]
    elif hizli:
        evaller = [ae for ae in TUM_EVALLER if ae.agent_adi in KRITIK_5]

    print(f"\n🧪 Gök Umay Agent Evals — {len(evaller)} agent")
    print("=" * 55)

    genel: dict[str, float] = {}
    tum_sonuclar: dict[str, list] = {}

    for ae in evaller:
        ort, sonuclar = agent_test_et(ae)
        genel[ae.agent_adi] = ort
        tum_sonuclar[ae.agent_adi] = [
            {"vaka": s.vaka_adi, "gecti": s.gecti, "puan": s.puan,
             "sure_ms": s.sure_ms, "hatalar": s.hatalar}
            for s in sonuclar
        ]

    rapor_yaz(genel, tum_sonuclar, katman_filter)


if __name__ == "__main__":
    main()
