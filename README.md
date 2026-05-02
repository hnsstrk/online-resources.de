# online-resources.de

Persönlicher Hugo-Blog mit Spielberichten aus Pen-&-Paper-RPG-Kampagnen.

**Live:** [https://www.online-resources.de/](https://www.online-resources.de/)

## Inhalt

Spielberichte und Notizen aus laufenden und abgeschlossenen Kampagnen:

- **DSA5** – Das Schwarze Auge 5. Edition (Greifenfurter Adel)
- **DSK** – Die Schwarze Katze

## Tech-Stack

| Komponente | Details |
|---|---|
| Static Site Generator | [Hugo](https://gohugo.io/) (extended) |
| Theme | `rollenspiel` (eigenes Theme unter `themes/rollenspiel/`) |
| CSS-Pipeline | PostCSS (`postcss-import`, `autoprefixer`) — installiert via `npm ci` im Build |
| Sprache | Deutsch (`de-de`) |
| Hosting | Contabo Ubuntu VPS + Nginx, GitHub-Actions-SSH-Trigger |
| Live | https://www.online-resources.de/ |

## Lokale Entwicklung

Voraussetzungen: Hugo installiert (`hugo version` zum Prüfen).

```bash
# Repository klonen (inkl. Theme-Submodul)
git clone --recurse-submodules https://github.com/hnsstrk/online-resources.de.git
cd online-resources.de

# Entwicklungsserver starten (inkl. Entwürfe)
hugo server -D
```

Der Server ist dann unter [http://localhost:1313](http://localhost:1313) erreichbar.

Falls das Submodul fehlt:

```bash
git submodule update --init --recursive
```

## Build

```bash
hugo
```

Die fertige Site wird im Verzeichnis `public/` erzeugt.

## Projektstruktur

```
online-resources.de/
├── config.yml             # Hugo-Konfiguration (Theme, Parameter, Menü)
├── content/
│   ├── posts/             # Blogbeiträge (Markdown)
│   ├── archiv.md          # Archivseite
│   ├── search.md          # Suchseite
│   ├── about.md           # Über
│   ├── impressum.md       # Impressum
│   ├── datenschutz.md     # Datenschutz
│   ├── blog/_index.md     # Blog-Section
│   └── categories/        # Term-Index-Pages mit deutschen Titeln
├── themes/rollenspiel/    # Eigenes Theme (kein Submodul)
├── deploy/build.sh        # Server-Build-Skript
├── package.json           # PostCSS-Pipeline-Dependencies
└── archetypes/            # Hugo-Archetypen für neue Inhalte
```

## Lizenz

Die Inhalte dieses Repositorys (Texte, Theme-Code, Konfiguration, Bilder)
stehen unter der **Creative Commons Attribution-NonCommercial 4.0
International** (CC BY-NC 4.0) — siehe [LICENSE](LICENSE).

Drittkomponenten (Hugo, Fuse.js, PostCSS, Schriften) stehen unter ihren
eigenen Lizenzen — siehe [THIRD-PARTY-LICENSES.md](THIRD-PARTY-LICENSES.md).
