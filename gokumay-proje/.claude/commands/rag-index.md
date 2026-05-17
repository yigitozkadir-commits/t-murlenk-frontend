---
description: Belgeyi RAG pipeline'a yükle ve indeksle.
tools: [bash]
---

RAG'a yükle: $ARGUMENTS

```bash
# Dosya/klasör tespiti
if [ -d "$ARGUMENTS" ]; then
  echo "📁 Klasör modu: $ARGUMENTS"
  bash ~/.claude/scripts/rag_yukle.sh "$ARGUMENTS"
else
  echo "📄 Tekil dosya: $ARGUMENTS"
  # Belge tipini tahmin et
  TIP="genel"
  echo "$ARGUMENTS" | grep -qi "gdd\|tasarim" && TIP="gdd"
  echo "$ARGUMENTS" | grep -qi "bug\|hata" && TIP="bug"
  echo "$ARGUMENTS" | grep -qi "tarihi\|kaynak" && TIP="tarihi"

  python3 ~/.claude/scripts/rag_client.py yukle \
    "$ARGUMENTS" \
    "$(basename $ARGUMENTS .md)" \
    "$TIP"
fi

# İstatistik
python3 -c "
from supabase import create_client
import os
db = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
r = db.table('belgeler').select('id', count='exact').execute()
print(f'✅ Toplam indekslenen chunk: {r.count}')
"
```
