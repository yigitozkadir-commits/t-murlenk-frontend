# Gök Umay Stüdyo — Claude Code Altyapısı

Solo oyun geliştirici stüdyo için Claude Code konfigürasyonu.
20 agent, 11 skill, 15 slash komutu, 6 hook.

## Kurulum (Termux)

```bash
# 1. Repo'yu clone et
git clone https://github.com/[kullanici]/gokumay-claude ~/.claude-config
cd ~/.claude-config

# 2. .claude klasörünü ana Claude dizinine bağla
cp -r .claude/* ~/.claude/

# 3. Hook'ları kur
bash kurulum-hooks.sh

# 4. Doğrula
ls ~/.claude/agents/ | wc -l    # 20
ls ~/.claude/skills/ | wc -l    # 11
ls ~/.claude/commands/ | wc -l  # 15

# 5. Oyun projesinde Claude Code başlat
cd ~/oyun-projesi
claude
```

## Yapı

```
.claude/
├── CLAUDE.md          — Master anayasa (buradan başla)
├── settings.json      — Token + hook ayarları
├── agents/            — 20 uzman agent
├── skills/            — 11 araç seti
└── commands/          — 15 slash komutu

kurulum-hooks.sh       — Hook kurulum scripti (bir kez çalıştır)
.claudeignore          — Token koruması (proje köküne koy)
```

## Slash Komutları

| Komut | Ne Yapar |
|-------|----------|
| `/fix [dosya]` | Hata bul ve düzelt |
| `/review [dosya]` | 5 perspektif kod incelemesi |
| `/refactor [dosya]` | Kodu temizle |
| `/version [dosya]` | Versiyon geçişi |
| `/perf [dosya]` | FPS / performans analizi |
| `/security [dosya]` | Güvenlik taraması |
| `/launch [proje]` | Lansman hazırlığı |
| `/post [konu]` | Platform içeriği yaz |
| `/new-game [ad]` | Yeni oyun başlat |
| `/myth [varlık]` | Türk mitolojisi araştır |
| `/notebook-prep [konu]` | NotebookLM pipeline |
| `/weekly` | Haftalık plan |
| `/explain [konu]` | 3 seviyeli açıklama |
| `/automate [görev]` | Bash script otomasyonu |
| `/clean [klasör]` | Proje temizliği |

## Teknoloji

Three.js · Web Audio API · Vanilla JS · Capacitor · HTML5


