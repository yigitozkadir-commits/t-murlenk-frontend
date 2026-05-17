# Katman 3 — Agent / Skill Ayrım Düzeltmesi
# Bu değişikliği CLAUDE-KATMAN3-EKLENTI.md'deki agent tanımlarına uygula

---

## Sorun
Katman 3'te 6 agent ve 6 skill tamamen aynı isme sahip:
  - mcp-server-builder (hem agent hem skill)
  - rag-pipeline (hem agent hem skill)
  - multi-agent-coordinator (hem agent hem skill)
  - playtest-ai (hem agent hem skill)
  - monetization-optimizer (hem agent hem skill)
  - community-manager (hem agent hem skill)

"community-manager ile görev yap" yazıldığında Claude hangisini kullandığını bilemez.

---

## Çözüm: İsimlendirme Kuralı

### Agent → düşünen ve karar veren
Adlandırma: olduğu gibi bırak (mevcut .md dosyaları değişmez)

### Skill → referans ve şablon koleksiyonu
Adlandırma: sonuna `-kit` ekle

```
ÖNCE (çakışıyor)          SONRA (net ayrım)
──────────────────────    ──────────────────────────
skill: mcp-server-builder → mcp-server-kit
skill: rag-pipeline       → rag-pipeline-kit
skill: multi-agent-coord  → multi-agent-kit
skill: playtest-ai        → playtest-kit
skill: monetization-optim → monetization-kit
skill: community-manager  → community-kit
```

---

## Uygulama Scripti

```bash
#!/bin/bash
# katman3-yeniden-adlandir.sh
# ~/.claude/skills/ klasöründeki Katman 3 skill'lerini yeniden adlandır

SKILLS_DIR="$HOME/.claude/skills"
declare -A YENIDEN_ADLANDIR=(
  ["mcp-server-builder"]="mcp-server-kit"
  ["rag-pipeline"]="rag-pipeline-kit"
  ["multi-agent-coordinator"]="multi-agent-kit"
  ["playtest-ai"]="playtest-kit"
  ["monetization-optimizer"]="monetization-kit"
  ["community-manager"]="community-kit"
)

for ESKI in "${!YENIDEN_ADLANDIR[@]}"; do
  YENI="${YENIDEN_ADLANDIR[$ESKI]}"
  if [[ -d "$SKILLS_DIR/$ESKI" ]]; then
    mv "$SKILLS_DIR/$ESKI" "$SKILLS_DIR/$YENI"
    # SKILL.md içindeki isim satırını güncelle
    sed -i "s/^name: $ESKI/name: $YENI/" "$SKILLS_DIR/$YENI/SKILL.md" 2>/dev/null || true
    echo "✅ $ESKI → $YENI"
  else
    echo "⚠️  Bulunamadı: $ESKI"
  fi
done

echo ""
echo "Sonuç:"
find "$SKILLS_DIR" -name "SKILL.md" | sort | while read f; do
  isim=$(grep "^name:" "$f" 2>/dev/null | head -1 | cut -d: -f2 | tr -d ' ')
  echo "  skill: $isim"
done
```

---

## CLAUDE.md Güncelleme

Hızlı Referans — Skill bölümündeki Katman 3 satırlarını güncelle:

```
# ÖNCE
mcp-server-builder   → MCP araç şablonları
rag-pipeline         → Chunk + hibrit arama
multi-agent-coordinator → Zincir kalıpları
playtest-ai          → Denge testi + edge case
monetization-optimizer → Dönüşüm formülleri
community-manager    → discord.py + reddit bot

# SONRA
mcp-server-kit       → MCP araç şablonları
rag-pipeline-kit     → Chunk + hibrit arama
multi-agent-kit      → Zincir kalıpları
playtest-kit         → Denge testi + edge case
monetization-kit     → Dönüşüm formülleri
community-kit        → discord.py + reddit bot
```

---

## Kullanım Farkı (Örnekler)

```
# Agent  — düşünür, karar alır, çalıştırır
"playtest-ai ile timurlenk_v35.html'yi denge aç hataları için test et"

# Skill  — şablon verir, referans gösterir
"playtest-kit'ten denge test şablonu al ve bu oyuna uyarla"
```
