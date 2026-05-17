#!/usr/bin/env python3
# rag_seed.py — Gök Umay Stüdyo RAG Başlangıç İçeriği
# ~/.claude/scripts/rag_seed.py
#
# Sistemi ilk kez doldurur. Bir kez çalıştır, sonra /rag-index ile güncel tut.
# ÇALIŞTIR: python3 rag_seed.py

import os
import sys
from supabase import create_client
from embedding import embed_toplu

db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# ── Seed Verisi ────────────────────────────────────────────────────────────────
# Her kayıt: (kaynak, tur, baslik, icerik)
SEED: list[tuple[str, str, str, str]] = [

    # ── MİMARİ KARARLAR ───────────────────────────────────────────────────────

    ("kararlar", "mimari", "CSP uyumlu AI motoru",
     "Gök Umay oyunlarında Web Worker yasak — CSP blob URL engelliyor. "
     "Çözüm: new Function + fakeSelf mesaj köprüsü. "
     "fakeSelf nesnesi postMessage/addEventListener simüle eder. "
     "Tüm AI kodları bu şablona sarılmalı. "
     "eval() kesinlikle kullanma — CSP bloğu tetikler."),

    ("kararlar", "mimari", "Three.js versiyon sabitleme r128",
     "Three.js r128 CDN'den inline yükle. "
     "r129+ sürümlerde OrbitControls import yolu değişti — eski oyunlar bozulur. "
     "CDN: https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js "
     "Versiyon asla otomatik güncelleme. Her yeni proje başında r128 onayla."),

    ("kararlar", "mimari", "Tek HTML dosya mimarisi",
     "Gök Umay oyunları tek .html dosyasına sığar. "
     "Avantaj: itch.io'ya doğrudan yükle, CDN gereksiz, zero-install. "
     "CSS ve JS inline. Dış bağımlılık sadece Three.js CDN. "
     "Çok dosyalı yapıya geçme — söylenmeden bölme yasak."),

    ("kararlar", "mimari", "Bozkır Platform plugin mimarisi",
     "Platform katmanı paylaşılan bileşenleri barındırır: "
     "nebula, toast, confetti, SFX, ELO, achievements, AIBridge. "
     "Her oyun bir plugin olarak AIBridge'e kayıt olur. "
     "AIBridge engine kayıt sistemi: oyun adı → AI fonksiyon referansı. "
     "Oyunlar birbirinin state'ini göremez."),

    ("kararlar", "mimari", "localStorage vs Supabase seçimi",
     "Tek kullanıcı, offline çalışma → localStorage yeterli. "
     "Çok kullanıcı, ELO, liderboard → Supabase. "
     "Bozkır Platform çok kullanıcılı olduğu için Supabase kullanır. "
     "Tek oyun prototipleri localStorage ile başlar."),

    # ── BUG ÇÖZÜM ARŞİVİ ─────────────────────────────────────────────────────

    ("bug-arsiv", "bug", "Raycaster hedef listesi sahne değişince güncellenmez",
     "Belirti: Yeni eklenen mesh'e tıklanmıyor, eski silinmiş mesh hâlâ tıklanıyor. "
     "Kök neden: Raycaster objeler listesi sahne değişiminde yenilenmez. "
     "Çözüm: Her sahne değişiminde raycaster.setFromCamera() öncesi "
     "objects dizisini scene.children'dan yeniden oluştur. "
     "Kod: const objects = scene.children.filter(m => m.isMesh);"),

    ("bug-arsiv", "bug", "Minimax alpha-beta budama hatalı hamle seçimi",
     "Belirti: AI basit kazan durumunu kaçırıyor. "
     "Kök neden: Alpha-beta değerleri düzgün başlatılmamış. "
     "Çözüm: alpha = -Infinity, beta = +Infinity ile başlat. "
     "Derinlik 0'da değerlendirme fonksiyonu skoru döndürmeli, tekrar çağırmamalı. "
     "Transposition table eklenirse zobrist hash kullan."),

    ("bug-arsiv", "bug", "Web Audio API mobilde sessiz kalıyor",
     "Belirti: iOS/Android'de ses çıkmıyor. "
     "Kök neden: Mobile tarayıcılar kullanıcı etkileşimi olmadan AudioContext başlatmıyor. "
     "Çözüm: AudioContext'i ilk dokunuş/tıklama eventinde oluştur veya resume() çağır. "
     "Kod: document.addEventListener('touchstart', () => ctx.resume(), {once: true});"),

    ("bug-arsiv", "bug", "Capacitor Android'de localStorage kaybolması",
     "Belirti: Uygulama güncellemesinden sonra kayıtlı veri gitti. "
     "Kök neden: Capacitor WebView update localStorage'ı sıfırlayabiliyor. "
     "Çözüm: Capacitor Preferences plugin kullan (localStorage değil). "
     "import { Preferences } from '@capacitor/preferences'; "
     "await Preferences.set({key: 'skor', value: JSON.stringify(data)});"),

    ("bug-arsiv", "bug", "Three.js hafıza sızıntısı sahne değişiminde",
     "Belirti: Uzun oturumda FPS düşüşü, tarayıcı yavaşlaması. "
     "Kök neden: Geometry ve material dispose edilmiyor. "
     "Çözüm: Sahne temizlerken her mesh için: "
     "mesh.geometry.dispose(); mesh.material.dispose(); "
     "renderer.dispose() sadece uygulama kapanışında. "
     "Texture'lar: texture.dispose() ayrıca çağrılmalı."),

    # ── OYUN TASARIM KARARLARI ────────────────────────────────────────────────

    ("gdd-kararlar", "oyun", "Timurlenk Satranç kuralları kaynağı",
     "Temel kaynak: Murray 1913 'A History of Chess' — Timur satranç kuralları bölümü. "
     "11x10 tahta. Ek taşlar: Deve (Camel) ve Zurafa (Giraffe). "
     "Deve: (1,3) L-şekli atlama. Zurafa: (1,4) atlama. "
     "Şah'ın bulunduğu kale yok — 'Citadel' kuralı uygulanmaz (tartışmalı). "
     "Her kural değişikliğinde kaynak notunu güncelle."),

    ("gdd-kararlar", "oyun", "Togyzool Tuzdık mekaniği",
     "Togyzool: Kazakistan'ın mancala oyunu. 9 çukur, 2 sıra. "
     "Tuzdık: Bir çukur kalıcı olarak kaptürlenır, rakip taşlar oraya düşmez. "
     "Hata: Her hamlede tüm tahla hesaplama = O(n^2). "
     "Düzeltme: Sadece değişen çukuru güncelle. "
     "AI yanıt süresi: 340ms → 80ms. "
     "Tuzdık sırası: Tek sayılı çukurlar seçilebilir."),

    ("gdd-kararlar", "oyun", "ELO sistemi parametreleri",
     "K faktörü: Yeni oyuncu (<30 oyun) K=40, normal K=20, üst (>2400) K=10. "
     "Başlangıç puanı: 1200. "
     "Beklenen skor formülü: E = 1 / (1 + 10^((Rb-Ra)/400)). "
     "Beraberlik: her oyuncuya +0.5 puan. "
     "Minimum puan: 100 (sıfıra düşme yok)."),

    ("gdd-kararlar", "oyun", "Zorluk seviyeleri minimax derinlikleri",
     "Kolay: derinlik 1-2, zaman limiti 200ms. "
     "Orta: derinlik 3-4, zaman limiti 1000ms. "
     "Zor: derinlik 5-6, zaman limiti 3000ms. "
     "Çok zor: iterative deepening, zaman limiti 5000ms. "
     "Mobile'da max derinlik 1 azalt (işlemci kısıtı)."),

    # ── KÜLTÜREL DOĞRULUK ─────────────────────────────────────────────────────

    ("kulturel", "kulturel", "Hiashatar — Moğolistan satranç varyantı",
     "Hiashatar: Moğolistan'ın geleneksel satranç varyantı. "
     "10x10 tahta. Bodyguard (Kheshig) taşı eklendi — at + fil kombinasyonu. "
     "Gece kuralı: Gece oynanan maçlarda bazı taşlar daha güçlü (tartışmalı). "
     "Kaynak: Parlett 'A History of Board Games' (doğrula). "
     "Moğolca terimler oyun içinde kullan: 'Nohoi' = köpek (rakip taşa verilen isim)."),

    ("kulturel", "kulturel", "Şatra — Tibet satranç varyantı",
     "Şatra: Tibet'in satranç varyantı. "
     "8x8 tahta. Filler köşegen değil düz hareket eder — Batı satrancından fark. "
     "Taşlar Tibetçe isimlerle anılır: Gyalpo (Şah), Langchen (Fil). "
     "Kaynak: Li (1998) 'Chess in the East'. "
     "Dikkat: 'Şatra' terimi bazı kaynaklarda Moğol satranç için de kullanılıyor."),

    # ── PERFORMANS OPTİMİZASYONLARI ──────────────────────────────────────────

    ("performans", "mimari", "FPS optimizasyon kontrol listesi",
     "1. requestAnimationFrame içinde obje oluşturma yasak. "
     "2. Geometry'leri önceden oluştur, döngüde clone() kullan. "
     "3. Sahne dışındaki mesh'leri visible=false yap, sil değil. "
     "4. Texture atlas kullan — çok sayıda küçük texture yerine tek büyük. "
     "5. renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)) — 2x yeter. "
     "6. Gölge: shadowMap sadece kritik objeler için."),

    ("performans", "mimari", "Mobil FPS hedefleri",
     "iOS Safari hedef: 60 FPS. "
     "Android Chrome hedef: 30 FPS (düşük uç cihaz). "
     "Test: renderer.info.render.triangles ile üçgen sayısını izle. "
     "Limit: 50.000 üçgen altında tut (mobil uyum). "
     "LOD: Uzak objeler için düşük poly model kullan."),

    # ── YAYIM BİLGİSİ ─────────────────────────────────────────────────────────

    ("yayin", "proje", "itch.io yayım kontrol listesi",
     "1. HTML5 zip paketi: oyun.html → oyun.zip. "
     "2. Başlık: tarihsel varyant adı + 'Chess Variant' (SEO). "
     "3. Etiket: historical, strategy, chess, browser-game, türkiye. "
     "4. Kapak görseli: 630x500px minimum. "
     "5. video: gameplay GIF > screenshot. "
     "6. Fiyat: Ücretsiz + 'Pay what you want'. "
     "7. Platform: HTML5 (browser). "
     "8. Dil: İngilizce açıklama zorunlu, Türkçe opsiyonel."),

    ("yayin", "proje", "Play Store hazırlık kontrol listesi",
     "Capacitor ile paket: npx cap add android → npx cap build android. "
     "AAB formatı zorunlu (APK değil). "
     "Hedef SDK: 34 (güncel gereksinim). "
     "İzinler: INTERNET yeterli — gereksiz izin ekleme. "
     "Gizlilik politikası: zorunlu, GitHub Pages'te yayınla. "
     "Uygulama ID: com.gokumay.[oyun_adi]. "
     "İlk yayın inceleme süresi: 3-7 gün."),

]


def seed_yukle():
    """Tüm seed verisini embedding ile Supabase'e yükle."""
    print(f"📚 {len(SEED)} kayıt yüklenecek...")

    metinler = [f"{baslik}\n{icerik}" for _, _, baslik, icerik in SEED]
    print("🔢 Embedding hesaplanıyor (toplu)...")
    embeddinglar = embed_toplu(metinler)

    kayitlar = [
        {
            "kaynak": kaynak,
            "tur": tur,
            "baslik": baslik,
            "icerik": icerik,
            "chunk_index": 0,
            "meta": {"kaynak": "seed-v1"},
            "embedding": emb,
        }
        for (kaynak, tur, baslik, icerik), emb in zip(SEED, embeddinglar)
    ]

    # 10'arlı batch ile yükle
    BATCH = 10
    for i in range(0, len(kayitlar), BATCH):
        grup = kayitlar[i:i + BATCH]
        db.table("belgeler").insert(grup).execute()
        print(f"   ✅ {i + len(grup)}/{len(kayitlar)} yüklendi")

    print(f"\n✅ Seed tamamlandı — {len(kayitlar)} kayıt Supabase'de")
    print("Sonraki adım: /rag-index ~/.claude/CLAUDE.md")


def seed_sil():
    """Seed verisini temizle (yeniden başlatmak için)."""
    db.table("belgeler").delete().eq("meta->>kaynak", "seed-v1").execute()
    print("🗑️  Seed verisi silindi")


if __name__ == "__main__":
    komut = sys.argv[1] if len(sys.argv) > 1 else "yukle"
    if komut == "yukle":
        seed_yukle()
    elif komut == "sil":
        seed_sil()
    elif komut == "sayi":
        r = db.table("belgeler").select("id", count="exact").execute()
        print(f"Toplam kayıt: {r.count}")
    else:
        print("Kullanım: rag_seed.py [yukle|sil|sayi]")
