# CLAUDE.md — Katman 3 Mod Eklentisi
# Bu bölümü CLAUDE-KATMAN3-EKLENTI.md'nin sonuna ekle

---

## Katman 3 — Geliştirme / Yayın Modu

Katman 3 bileşenleri her zaman aktif değil. İki mod:

```
GELİŞTİRME MODU (varsayılan)
  ✅ mcp-server-builder    — her zaman aktif
  ✅ rag-pipeline          — her zaman aktif
  ✅ multi-agent-coordinator — her zaman aktif
  ✅ playtest-ai           — her zaman aktif
  ❌ monetization-optimizer — yayın haftası
  ❌ community-manager     — yayın haftası

YAYIN MODU (oyun çıkmadan 3 gün önce aktifleştir)
  ✅ Tüm Geliştirme Modu bileşenleri
  ✅ monetization-optimizer
  ✅ community-manager (Discord + Reddit botları)
```

### Yayın Modunu Aç

```bash
bash ~/.claude/scripts/mod-gec.sh yayin
```

### Geliştirme Moduna Dön

```bash
bash ~/.claude/scripts/mod-gec.sh gelistirme
```
