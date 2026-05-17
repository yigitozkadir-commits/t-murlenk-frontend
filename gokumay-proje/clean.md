---
description: Proje klasörünü temizle — gereksiz dosyaları kaldır.
tools: [bash]
---

$ARGUMENTS projesini temizle.

```bash
# Node.js artıkları
rm -rf node_modules .next dist build coverage
npm cache clean --force 2>/dev/null || true

# Capacitor build artıkları (kaynak koduna dokunma!)
# android/ ve ios/ klasörleri yeniden üretilebilir
# Silmeden önce sor

# Genel temizlik
find . -name ".DS_Store" -delete
find . -name "Thumbs.db" -delete
find . -name "*.log" -delete 2>/dev/null
find . -name "*.tmp" -delete 2>/dev/null

# Python artıkları
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Boyut kontrolü
echo "Temizlik sonrası:"
du -sh . 2>/dev/null
df -h . 2>/dev/null
```

DOĞRULAMA:
```bash
# Oyun hâlâ açılıyor mu?
ls *.html 2>/dev/null

# Git durumu temiz mi?
git status --short 2>/dev/null || echo "Git repo değil"
```

.gitignore güncel mi? Kontrol et:
```bash
cat .gitignore 2>/dev/null || echo ".gitignore yok — oluştur?"
```


