# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**online-resources.de** is a personal blog/website built with Hugo and a custom theme called `rollenspiel`. Content focuses on tabletop RPGs — Das Schwarze Auge (DSA5), Die Schwarze Katze (DSK), Dungeons & Dragons 5e and Hexxen 1733. German language.

## Tech Stack

| Komponente | Technologie |
|------------|-------------|
| SSG | Hugo 0.159.1 extended |
| Theme | `rollenspiel` (eigenes Theme unter `themes/rollenspiel/`) |
| CSS-Pipeline | PostCSS (`postcss-import`, `autoprefixer`) — installiert via `npm ci` im Build |
| Suche | Fuse.js (clientseitig, via CDN) |
| Sprache | Deutsch (de-de) |
| Hosting | Contabo Ubuntu VPS + Nginx (Node.js LTS systemweit installiert) |
| CI/CD | GitHub Actions SSH-Trigger → Server baut mit Hugo + npm ci |
| SSL | Let's Encrypt / Certbot (Auto-Renewal) |
| URL | https://www.online-resources.de/ |
| Lizenz | Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0) |

## Project Structure

```
online-resources.de/
├── .github/workflows/        # GitHub Actions (SSH-Trigger für Deploy)
├── config.yml                # Hugo-Konfiguration
├── package.json              # PostCSS-Pipeline-Dependencies (Build-time)
├── postcss.config.js         # PostCSS-Config (postcss-import, autoprefixer)
├── content/
│   ├── posts/                # Blog-Posts (Markdown, mit Cover-Image im Bundle)
│   ├── archiv.md             # Archiv-Übersicht (Layout: archives.html)
│   ├── about.md              # Über-Seite
│   ├── search.md             # Suchseite (Layout: search/single.html)
│   ├── lizenz.md             # Lizenz und Credits (CC BY-NC 4.0 + Drittlizenzen)
│   ├── impressum.md          # Impressum
│   ├── datenschutz.md        # Datenschutzerklärung
│   ├── blog/_index.md        # Blog-Section
│   ├── categories/           # Term-Index-Pages (Custom Titles für Kategorien)
│   └── favicon/              # Favicon-Dateien
├── deploy/build.sh           # Server-Build-Skript (npm ci + hugo)
├── themes/rollenspiel/       # Eigenes Theme
└── archetypes/               # Hugo Archetypes
```

## Theme `rollenspiel` — Kernkonzepte

- **Editorial-Stil**: Cormorant Garamond + EB Garamond + Cinzel + JetBrains Mono.
- **Hero auf Home**: vollflächiges Cover des jüngsten Posts mit Kicker (System · Datum · Lesezeit · Autor), Title, Dek (Summary) und einem konfigurierbaren Italic-Claim im rechten Side-Block.
- **Page-Header auf Inhaltsseiten**: Title links, konfigurierbarer Side-Text rechts. Cascade in `layouts/partials/page-header.html`:
  1. Front-Matter `headerSide:` (höchste Priorität, pro-Seite-Override)
  2. `params.pageHeaders[<slug>]` aus `config.yml` (zentrale Map)
  3. `params.claim` (globaler Default mit `<em>`-Hervorhebungen)
- **Single-Variante --simple** für `about`, `impressum`, `datenschutz`, `search`: kein Hero, ruhige Lese-Spalte, page-header oben.
- **Filter-Bar entfällt**: System-Filterung läuft über die Term-Pages `/categories/das-schwarze-auge/` etc.

## Development

```bash
hugo server -D          # Dev server with drafts
hugo                    # Build static site
npm install             # Einmalig: PostCSS-Dependencies (für lokale Entwicklung)
```

## Key Configuration

- **Date format:** DD.MM.YYYY (German)
- **Default theme:** auto (dark/light based on system)
- **Features enabled:** RSS, reading time, word count, breadcrumbs, TOC, search (Fuse.js)
- **External links:** FoundryVTT instances (fvtt1/fvtt2.online-resources.de)
- **Navigation order**: Blog · Kategorien · Archiv · Tags · Über · Suche

## Deployment

Push auf `main` triggert automatisches Deployment:

1. GitHub Actions verbindet per SSH zum Contabo Server (User: `deploy`, forced command).
2. Server-Skript `deploy/build.sh`:
   - `git pull` + `git submodule update`
   - **Re-exec via `exec "$0"`** falls `build.sh` selbst durch den Pull aktualisiert wurde (geschützt gegen Endlos-Loop via `BUILD_REEXECED`).
   - `npm ci --no-audit --prefer-offline` — installiert PostCSS-Pipeline.
   - `rm -rf "$DEPLOY_DIR"/*` — räumt Geistereinträge aus früheren Builds.
   - `hugo --minify --gc --destination /var/www/online-resources.de/`.
3. Nginx serviert die statischen Dateien.

Permissions auf dem Server: `/home/hans/Repositories/online-resources.de/` ist `hans:websitebuilder` mit setgid (`drwxrwsr-x`); `deploy`-User ist Mitglied der Gruppe `websitebuilder` und hat damit Schreibrechte.

Kein Build auf dem GitHub Runner — der Server baut selbst.

## Lizenz

- Eigene Inhalte: **CC BY-NC 4.0** (siehe `LICENSE`).
- Drittkomponenten: siehe `THIRD-PARTY-LICENSES.md` (Repo) und `/lizenz/` (Live-Site).

## Projektdokumentation

Alle Konzepte, Entscheidungen und ADRs im Obsidian Vault:

**Vault-Pfad (plattformabhängig):**

| System | Vault-Basispfad |
|--------|----------------|
| Linux (Ganymed) | `/home/hnsstrk/Insync/hans.juergen.stark@gmail.com/Google Drive/Vault Obsidian/` |
| macOS (MacBook) | `/Users/hnsstrk/Meine Ablage/Vault Obsidian/` |

**Projektordner im Vault:** `Projekte/online-resources.de/`

Vollständige Pfade:

- Linux: `/home/hnsstrk/Insync/hans.juergen.stark@gmail.com/Google Drive/Vault Obsidian/Projekte/online-resources.de/`
- macOS: `/Users/hnsstrk/Meine Ablage/Vault Obsidian/Projekte/online-resources.de/`

Dieser Ordner ist bei jeder Arbeit am Projekt zu konsultieren.
