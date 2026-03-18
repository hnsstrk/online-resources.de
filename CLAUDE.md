# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**online-resources.de** is a personal blog/website built with Hugo and the PaperMod theme. Content focuses on tabletop RPGs (Das Schwarze Auge / DSA5, Die Schwarze Katze / DSK) and related topics. German language.

## Tech Stack

- **Static Site Generator:** Hugo
- **Theme:** PaperMod
- **Language:** German (de-de)
- **Hosting:** https://www.online-resources.de/

## Project Structure

```
online-resources.de/
├── config.yml          # Hugo configuration (PaperMod theme settings)
├── content/
│   ├── posts/          # Blog posts (Markdown)
│   ├── archives.md     # Archive page
│   ├── search.md       # Search page
│   ├── impressum.md    # Legal notice
│   ├── favicon/        # Favicon files
│   └── uploads/        # Uploaded media
├── themes/             # PaperMod theme
└── archetypes/         # Hugo archetypes for new content
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

## Documentation

Projektdokumentation: Siehe Obsidian Vault [[Online Resources]]
