---
name: skill-creator
description: |
  Gök Umay'a özel yeni skill dosyaları oluşturur ve günceller.
  Kullan: "skill-creator ile [konu] için skill yaz"
---

# Skill Yaratıcı

## Rolüm
Tekrarlayan görevler → skill dosyası → bir daha açıklamaya gerek yok.

## TOKEN KURALI
Şişirilmiş skill değil — sıkı, odaklı, 100-150 satır max.

---

## Skill Dosyası Şablonu

```markdown
---
name: skill-adı
description: |
  Ne yapar (1-2 cümle).
  Kullan: "skill-adı ile [görev]"
---

# Skill Başlığı

## TOKEN KURALI
[Bu skill için token tasarrufu taktikleri]

---

## [Ana İçerik]

[Kopyala-çalıştır hazır kod veya kontrol listesi]

---

## Çıktı

[Beklenen çıktı formatı]
```

---

## Skill vs Agent Ayrımı

```
Skill  = Claude'a bir konuyu öğretir (pasif bağlam)
         ~/.claude/skills/skill-adı/SKILL.md

Agent  = Belirli rolü üstlenir, görev alır (aktif eylem)
         ~/.claude/agents/agent-adı.md

Test: "Bunu bilen biri mi lazım, yapan biri mi?"
Bilen → skill / Yapan → agent
```

---

## Kalite Kriterleri

```
✓ "Kullan:" örneği var mı?
✓ TOKEN KURALI bölümü var mı?
✓ Çıktı formatı net mi?
✓ Gök Umay'a özel detay var mı?
✓ 200 satırı aşıyor mu? → Kırp
✓ Başka skill ile örtüşüyor mu? → Birleştir
```

---

## Mevcut Skill Kataloğu

```
Kod:       systematic-debugging, owasp-security, vibesec
Oyun:      three-js-patterns, game-ai-engine, minimax-ai
İçerik:    humanizer, voice-dna-skill, seo-geo
Entegrasyon: notebooklm, capacitor-mobile
```

Yeni skill yazmadan önce bu listede ara — zaten var mı?


