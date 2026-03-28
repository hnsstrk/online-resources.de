# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**online-resources.de** is a personal blog/website built with Hugo and the PaperMod theme. Content focuses on tabletop RPGs (Das Schwarze Auge / DSA5, Die Schwarze Katze / DSK) and related topics. German language.

## Tech Stack

| Komponente | Technologie |
|------------|-------------|
| SSG | Hugo 0.159.1 extended |
| Theme | PaperMod (Git-Submodul) |
| Sprache | Deutsch (de-de) |
| Hosting | Contabo Ubuntu VPS + Nginx |
| CI/CD | GitHub Actions SSH-Trigger → Server baut mit Hugo |
| SSL | Let's Encrypt / Certbot (Auto-Renewal) |
| URL | https://www.online-resources.de/ |

## Project Structure

```
online-resources.de/
├── .github/workflows/  # GitHub Actions (SSH-Trigger für Deploy)
├── config.yml          # Hugo-Konfiguration (PaperMod Theme Settings)
├── content/
│   ├── posts/          # Blog-Posts (Markdown)
│   ├── archives.md     # Archiv-Seite
│   ├── search.md       # Suchseite
│   ├── impressum.md    # Impressum
│   ├── datenschutz.md  # Datenschutzerklärung
│   ├── favicon/        # Favicon-Dateien
│   └── uploads/        # Medien
├── deploy/             # Build-Script für Contabo Server
├── themes/             # PaperMod Theme (Git-Submodul)
└── archetypes/         # Hugo Archetypes
```

## Development

```bash
hugo server -D          # Dev server with drafts
hugo                    # Build static site
```

## Key Configuration

- **Date format:** DD.MM.YYYY (German)
- **Default theme:** auto (dark/light based on system)
- **Features enabled:** RSS, reading time, word count, breadcrumbs, TOC, search (Fuse.js)
- **External links:** FoundryVTT instances (fvtt1/fvtt2.online-resources.de)

## Deployment

Push auf `main` triggert automatisches Deployment:
1. GitHub Actions verbindet per SSH zum Contabo Server
2. Server: `git pull` → `hugo --minify --destination /var/www/online-resources.de/`
3. Nginx serviert die statischen Dateien

Kein Build auf dem GitHub Runner — der Server baut selbst.

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
