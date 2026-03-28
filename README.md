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
| Static Site Generator | [Hugo](https://gohugo.io/) |
| Theme | [PaperMod](https://github.com/adityatelange/hugo-PaperMod) (Git-Submodul) |
| Sprache | Deutsch (`de-de`) |
| Hosting | [online-resources.de](https://www.online-resources.de/) |

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
├── config.yml          # Hugo-Konfiguration (Theme, Parameter, Menü)
├── content/
│   ├── posts/          # Blogbeiträge (Markdown)
│   ├── archives.md     # Archivseite
│   ├── search.md       # Suchseite
│   └── impressum.md    # Impressum
├── themes/PaperMod/    # Theme (Git-Submodul)
└── archetypes/         # Hugo-Archetypen für neue Inhalte
```

## Lizenz

[MIT](LICENSE)
