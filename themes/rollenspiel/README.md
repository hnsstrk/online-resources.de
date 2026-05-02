# Rollenspiel — Hugo theme

Editorial Hugo theme for **[online-resources.de](https://www.online-resources.de/)**. Pergament/Grimoire palette, serif editorial typography (Cormorant Garamond / EB Garamond / Cinzel), Light+Dark via `data-theme`, Fuse.js search, Hugo resource pipeline for CSS.

## Installation

```bash
cd themes
git submodule add https://github.com/hnsstrk/theme-rollenspiel rollenspiel
```

In `config.yml`:

```yaml
theme: rollenspiel
```

## Compatibility with PaperMod

Consumes the same `config.yml` params:

- `params.label.text`, `params.description`, `params.author`
- `params.socialIcons` — list of `{ name, url }` with known handlers: twitter, reddit, twitch, instagram, github, youtube, discord, linkedin, rss.
- `params.DateFormat`, `params.ShowReadingTime`, `params.ShowWordCount`, `params.ShowBreadCrumbs`, `params.ShowPostNavLinks`, `params.ShowFullTextinRSS`.
- `params.assets.favicon*`
- `menu.main` — rendered in topbar.
- `params.fuseOpts` — currently ignored (search uses hardcoded compatible defaults; port if needed).

## Frontmatter

Theme works with the existing minimal schema — no required additions:

```yaml
---
title: "Verlassene Mine"
date: 2023-09-04T21:20:43+02:00
author: hnsstrk
categories:
 - Das schwarze Auge
 - Greifenfurter Adel
tags:
  - Rollenspiel
---
```

Optional per-post:

- `drop_cap: false` — disable the decorative drop-cap on the first paragraph (default: true).
- `showtoc: false` — disable the inline table of contents (handled by Hugo).

## Classification

The theme derives a `DSA`/`DSK`/`GURPS` system tag from `categories` at render time — no data migration needed:

| Category contains | Tag |
|---|---|
| "Das schwarze Auge" or "DSA" | DSA |
| "Die schwarze Katze" or "DSK" | DSK |
| "GURPS" | GURPS |

## Author

hnsstrk — https://hnsstrk.de

## License

MIT.
