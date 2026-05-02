---
name: post-summary
description: |
  Generiert stimmungsvolle Hugo-Frontmatter-Summaries für Blog-Posts via Gemini CLI.
  Kategorie-aware Erzählstimme (DSA/Greifenfurter Adel — Wir-Chronist; DSK/Benjamin
  Büchernase — Ich-Form Kater; Tagebuch von Inigo — Tagebuch; Warhammer Fantasy —
  episch). Patcht das `summary:`-Feld ins YAML-Frontmatter, überspringt Posts,
  die bereits ein Summary haben.
  TRIGGER when: user wants to add or regenerate Hugo post summaries, mentions
  "summary", "Vorschau für Posts", "summary für Beiträge", "Frontmatter-Summary",
  "Beitrags-Vorschau generieren", or works on bulk content metadata in
  content/posts/.
  DO NOT TRIGGER when: user works on Hugo templates, layouts, or theme code
  without summary work; or when only a single sentence change is requested.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# post-summary — Skill

Generiert für Hugo-Blog-Posts (`content/posts/*/index.md`) ein deutsches, stimmungsvolles `summary` ins YAML-Frontmatter. Nutzt **Gemini CLI** (headless, `gemini -p`) für die Text-Generation und ein Python-Skript für robustes Frontmatter-Patching.

**Längen-Limit**: 45–60 Wörter, max. 400 Zeichen (siehe `briefing.md`). Das Skript erzwingt das Limit als Schutznetz (`enforce_char_limit`) und schneidet bei Überschreitung am letzten Satzende ab.

## Wann nutzen

- Nach Import größerer Mengen an Posts ohne Summary
- Wenn alle bestehenden Summaries neu generiert werden sollen (`--force`)
- Für einzelne neue Posts (`--single <pfad>`)

## Voraussetzungen

- `gemini` CLI installiert und mit gültigem API-Key konfiguriert
- Python 3 (Mac default)
- Posts haben YAML-Frontmatter zwischen `---`-Markern
- Posts liegen unter `content/posts/<slug>/index.md`

## Aufruf

```bash
# Trockenlauf — was würde generiert?
python3 .claude/skills/post-summary/generate.py --dry-run

# Test mit 3 Posts
python3 .claude/skills/post-summary/generate.py --limit 3

# Voller Lauf, parallel 8
python3 .claude/skills/post-summary/generate.py --parallel 8

# Einzelnen Post (auch wenn schon summary vorhanden)
python3 .claude/skills/post-summary/generate.py --single content/posts/2024-05-01-Die_Rettung_von_Aishulibeth/index.md --force

# Komplett neu generieren (überschreibt!)
python3 .claude/skills/post-summary/generate.py --force --parallel 8
```

## Arbeitsweise

1. Findet alle `content/posts/*/index.md` (Glob).
2. Pro Post:
   - Frontmatter parsen (zwischen den `---`-Markern).
   - Bei vorhandenem `summary:` → überspringen, außer `--force`.
   - Body-Text extrahieren, auf 6000 Zeichen kürzen.
   - Kategorien lesen → Stilstimme bestimmen ([briefing.md](briefing.md)).
   - Gemini-Call mit Briefing + Body.
   - Antwort einfügen als `summary: |` (literal block) **direkt nach `title:`**.
3. Parallel via `concurrent.futures.ThreadPoolExecutor`.
4. Schreibt Logbuch nach stdout: ✓ generiert / ⏭ skipped / ✗ Fehler.

## Stil-Briefing

Siehe [briefing.md](briefing.md). Wenn neue Kategorien dazukommen, dort ergänzen.

## Bekannte Grenzen

- **Token-Budget**: Gemini-Free-Tier hat Quota; bei 100+ Posts auf 8er-Parallelität reduzieren oder Batches.
- **Frontmatter-Stil**: Skript geht von `---`-YAML aus (kein `+++`-TOML).
- **Eigennamen**: Modell hält sich meistens, aber Stichproben sind ratsam.
- **Idempotent**: Ohne `--force` werden bestehende Summaries nie überschrieben.

## Erweiterung

Für andere Hugo-Projekte:
- `briefing.md` an dortige Erzählwelten/Kategorien anpassen
- `--posts-dir` Argument (Default `content/posts`) ggf. anpassen
- Optional: weiteres Modell-Backend (Codex, Claude) hinter `--backend`-Flag
