---
description: Multi-agent zinciri çalıştır — paralel + sıralı.
tools: [bash]
---

Agent zinciri: $ARGUMENTS

MEVCUT ZİNCİRLER:
  versiyon  → bug + perf + güvenlik → qa → belge
  icerik    → taslak → voice-dna → humanizer
  lansman   → qa → güvenlik → içerik × 3 → yayın
  arastirma → research + narrative → game-designer → technical

ZİNCİR SEÇ:
```bash
python3 << EOF
import asyncio, sys
sys.path.insert(0, '$HOME/.claude/scripts')

# Hangi zincir?
ZINCIR = "$ARGUMENTS".lower()

async def calistir():
    if 'versiyon' in ZINCIR or 'version' in ZINCIR:
        print("🔗 Versiyon geçiş zinciri başlatılıyor...")
        # multi_agent.versiyon_gec() çağrısı
    elif 'icerik' in ZINCIR or 'content' in ZINCIR:
        print("🔗 İçerik üretim zinciri başlatılıyor...")
    elif 'lansman' in ZINCIR or 'launch' in ZINCIR:
        print("🔗 Lansman pipeline başlatılıyor...")
    else:
        print(f"Bilinmeyen zincir: {ZINCIR}")
        print("Kullanım: /chain versiyon|icerik|lansman|arastirma [parametre]")

asyncio.run(calistir())
EOF
```

MALIYET TAHMİNİ:
```bash
python3 -c "
zincirir_maliyetler = {
    'versiyon': 0.003,
    'icerik': 0.001,
    'lansman': 0.008,
    'arastirma': 0.005,
}
z = '$ARGUMENTS'.split()[0].lower()
maliyet = zincirir_maliyetler.get(z, 0.005)
print(f'Tahmini maliyet: \${maliyet:.4f} (~{int(maliyet*1000)} token)')
"
```

ZİNCİR: $ARGUMENTS
