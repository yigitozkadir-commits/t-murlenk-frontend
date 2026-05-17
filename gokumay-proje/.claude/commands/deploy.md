---
description: Projeyi belirtilen platforma deploy et.
tools: [bash]
---

Deploy: $ARGUMENTS

PLATFORM TESPİT:
```bash
# Hangi platform? (belirtilmediyse otomatik tespit)
ls capacitor.config.json 2>/dev/null && PLATFORM="mobile" || PLATFORM="web"
ls vercel.json 2>/dev/null && PLATFORM="vercel"
echo "Tespit edilen platform: $PLATFORM"
```

WEB DEPLOY (GitHub Pages / Vercel):
```bash
# Git ile deploy
git add .
git commit -m "Deploy: $(date +%Y-%m-%d) — $ARGUMENTS"
git push origin main
echo "✅ GitHub Pages: https://[kullanici].github.io/[repo]"

# Vercel (kuruluysa)
vercel --prod 2>/dev/null && echo "✅ Vercel deploy" || true
```

ITCH.IO DEPLOY (Butler CLI):
```bash
# Butler kur (bir kez)
# https://itchio.itch.io/butler

OYUN_DOSYASI=$(ls *.html 2>/dev/null | tail -1)
VERSIYON=$(grep -o "v[0-9]*" $OYUN_DOSYASI | head -1)

butler push $OYUN_DOSYASI \
  gokumay/$ARGUMENTS:html5 \
  --userversion ${VERSIYON:-1.0.0}
echo "✅ itch.io: itchio.io/gokumay/$ARGUMENTS"
```

MOBİL DEPLOY (Capacitor):
```bash
# Android AAB oluştur
npx cap copy android
cd android && ./gradlew bundleRelease
echo "✅ AAB: android/app/build/outputs/bundle/release/"
echo "➡️  Play Store Console'a yükle"
```

DEPLOY SONRASI:
```bash
# Sentry release güncelle
sentry-cli releases new $ARGUMENTS 2>/dev/null || true

# Hafızaya kaydet
python3 ~/.claude/scripts/memory_client.py kaydet \
  "Deploy: $ARGUMENTS — $(date +%Y-%m-%d)" \
  "Platform: $PLATFORM. Başarılı." \
  "proje"

echo "📊 /metrics $ARGUMENTS — 24 saat sonra kontrol et"
```
