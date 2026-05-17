---
description: Gök Umay MCP sunucusu için yeni araç tanımla ve ekle.
tools: [bash, edit]
---

Yeni MCP aracı ekle: $ARGUMENTS

ADIM 1 — ARAÇ TANIMI
```
Ad:          [snake_case — Claude bunu okur]
Açıklama:    [Ne yapar — 1 cümle, net]
Parametreler:
  - [ad]: [tip] — [açıklama] [zorunlu/opsiyonel]
Handler:     [Ne döndürür]
```

ADIM 2 — MEVCUT SUNUCUYA EKLE
```bash
SUNUCU=~/.claude/mcp-servers/gokumay-araclar/index.ts

# Araç listesine ekle (ListToolsRequestSchema handler)
# Switch case'e ekle (CallToolRequestSchema handler)
echo "Düzenlenecek dosya: $SUNUCU"
```

ADIM 3 — TEST ET
```bash
# Sunucuyu yeniden başlat
pkill -f "tsx.*gokumay-araclar" 2>/dev/null || true

# Claude Code'a tanıt
claude mcp list  # sunucu görünüyor mu?

# Test çağrısı
claude "gokumay-araclar araçlarını listele"
claude "[$ARGUMENTS] aracını test et"
```

ADIM 4 — HAFIZAYA KAYDET
```bash
python3 ~/.claude/scripts/memory_client.py kaydet \
  "MCP araç eklendi: $ARGUMENTS" \
  "Gökumay MCP sunucusuna $ARGUMENTS aracı eklendi." \
  "mimari" "genel"
```

ARAÇ: $ARGUMENTS
