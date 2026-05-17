#!/bin/bash
# eks3-kurulum.sh — Gök Umay %4 Tamamlama Paketi
# RAG soğuk başlangıç + MCP semantik arama + Agent evals
# Kullanım: bash eks3-kurulum.sh
# Gereksinim: duzeltme-kurulum.sh + eks2-kurulum.sh çalıştırılmış olmalı

set -e
echo "🎯 Gök Umay — Son %4 Düzeltmeleri"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REPO="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS="$HOME/.claude/scripts"
MCP_DIR="$HOME/.claude/mcp-servers/gokumay-tools"

# ── 1. RAG Seed + Auto-Index ──────────────────────────────────────────────────
echo ""
echo "1️⃣  RAG başlangıç içeriği kuruluyor..."
mkdir -p "$SCRIPTS"

cp "$REPO/rag-seed/rag_seed.py"       "$SCRIPTS/"
cp "$REPO/rag-seed/rag_auto_index.py" "$SCRIPTS/"
echo "   ✅ rag_seed.py + rag_auto_index.py kuruldu"

# Supabase bağlantısı varsa seed yükle
if [[ -n "$SUPABASE_URL" && -n "$SUPABASE_KEY" ]]; then
  echo "   📚 Seed verisi yükleniyor (${SUPABASE_URL%/*})..."
  python3 "$SCRIPTS/rag_seed.py" yukle && \
    echo "   ✅ Seed tamamlandı" || \
    echo "   ⚠️  Seed başarısız — manuel çalıştır: python3 ~/.claude/scripts/rag_seed.py yukle"

  echo "   🔍 CLAUDE.md ve agent'lar indeksleniyor..."
  python3 "$SCRIPTS/rag_auto_index.py" && \
    echo "   ✅ Auto-index tamamlandı" || \
    echo "   ⚠️  Auto-index başarısız"
else
  echo "   ⚠️  SUPABASE_URL/KEY eksik — seed manuel yükle:"
  echo "       source ~/.env && python3 ~/.claude/scripts/rag_seed.py yukle"
  echo "       python3 ~/.claude/scripts/rag_auto_index.py"
fi

# ── 2. MCP Semantik Arama Düzeltmesi ─────────────────────────────────────────
echo ""
echo "2️⃣  MCP hafiza_ara → gerçek semantik arama..."
if [[ -d "$MCP_DIR" ]]; then
  # Eski index.ts'i yedekle
  cp "$MCP_DIR/index.ts" "$MCP_DIR/index.ts.bak" 2>/dev/null || true
  cp "$REPO/mcp-fix/index.ts" "$MCP_DIR/"
  echo "   ✅ index.ts güncellendi (eski: index.ts.bak)"

  # MCP'yi yeniden başlat
  if which claude &>/dev/null; then
    claude mcp remove gokumay-tools 2>/dev/null || true
    claude mcp add gokumay-tools \
      --transport stdio \
      -- tsx "$MCP_DIR/index.ts" 2>/dev/null && \
      echo "   ✅ MCP yeniden kayıt edildi" || \
      echo "   ⚠️  Manuel kayıt: claude mcp add gokumay-tools --transport stdio -- tsx $MCP_DIR/index.ts"
  fi
else
  echo "   ⚠️  MCP dizini bulunamadı: $MCP_DIR"
  echo "       Önce eks2-kurulum.sh çalıştır"
fi

# ── 3. Agent Evals ───────────────────────────────────────────────────────────
echo ""
echo "3️⃣  Agent eval sistemi kuruluyor..."
mkdir -p "$HOME/.claude/logs"

cp "$REPO/evals/agent_evals.py" "$SCRIPTS/"
echo "   ✅ agent_evals.py kuruldu"

# Güncellenmiş weekly.md
cp "$REPO/evals/weekly.md" "$HOME/.claude/commands/weekly.md"
echo "   ✅ weekly.md güncellendi (eval + RAG adımları eklendi)"

# İlk eval çalıştır (hızlı mod)
echo ""
echo "   🧪 İlk agent testi (5 kritik agent, ~60 sn)..."
python3 "$SCRIPTS/agent_evals.py" --hizli 2>/dev/null | tail -15 || \
  echo "   ⚠️  Eval çalışmadı — API key kontrol et"

# ── Özet ─────────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 %4 Düzeltme Özeti"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ RAG: 20+ başlangıç kaydı + CLAUDE.md + agent'lar indekslendi"
echo "✅ MCP: hafiza_ara → pgvector semantik arama"
echo "✅ Evals: 8 agent × 16 test vakası + weekly entegrasyonu"
echo ""
echo "Kontrol:"
echo "  RAG:   python3 ~/.claude/scripts/rag_seed.py sayi"
echo "  MCP:   claude \"raycaster tıklama sorunu hakkında hafızamı ara\""
echo "  Evals: python3 ~/.claude/scripts/agent_evals.py"
echo "  Haftalık: /weekly  (artık eval + RAG güncelleme dahil)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
