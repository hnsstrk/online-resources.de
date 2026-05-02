# Änderungsprotokoll

Alle nennenswerten Änderungen an diesem Projekt werden in dieser Datei
festgehalten.

Das Format orientiert sich an [Keep a Changelog 1.1.0][kac], die Sprache ist
Deutsch. Da das Projekt eine persönliche Hugo-Website ohne Versionsnummern
ist, wird **datumsbasiert** gruppiert: Die obersten Sections markieren
zeitliche Cluster (Releases auf den Live-Server), nicht semantische Versionen.

Geschrieben werden vor allem strukturelle, gestalterische und technische
Änderungen am Theme, an der Konfiguration und am Build/Deploy. Einzelne
Blog-Posts und ihre Bildkorrekturen tauchen hier nicht auf — sie sind im
Git-Verlauf vollständig nachvollziehbar.

[kac]: https://keepachangelog.com/de/1.1.0/

---

## [Unreleased]

### Geändert
- Archiv-Struktur überarbeitet: `content/archive/` zu `content/blog/`
  umbenannt (inkl. der Sub-Sections `dsa/` und `dsk/`), die Übersichts-Seite
  `content/archives.md` heißt jetzt `content/archiv.md`.
- Theme-Layout entsprechend nachgezogen: `layouts/archives/single.html`
  verschoben nach `layouts/_default/archives.html`, plus Anpassungen in
  `list.html`, `archive-card.html` und den CSS-Dateien `list.css`,
  `main.css`.

### Hinzugefügt
- Eigenes Stylesheet `themes/rollenspiel/assets/css/archiv.css` für die
  neue Archiv-Seite.

---

## 2026-05-02 — Theme-Refactor und Page-Header-Vereinheitlichung

### Hinzugefügt
- **`post-summary`-Skill** als versionierter Bestandteil des Repos
  (`.claude/skills/post-summary/`): Python-Generator mit Briefing,
  kategorie-aware Erzählstimmen (DSA/Greifenfurter Adel, DSK/Benjamin
  Büchernase, Inigo-Tagebuch, Warhammer Fantasy, GURPS) und Schutznetz
  für das 400-Zeichen-Limit. `.gitignore` mit Negations-Trick angepasst,
  damit nur diese Skill getrackt wird.
- **Stimmungsvolle `summary:`-Frontmatter für 96 Bestands-Posts**, je
  Kategorie in passender Erzählperspektive (45–60 Wörter, Ø 363 Zeichen,
  generiert via Gemini CLI parallel).
- **Einheitlicher Page-Header für alle Inhaltsseiten** (Single-Posts,
  Sektionen, Taxonomien, About).
- `npm ci` als Vorstufe im Server-Build, damit das Theme-Bundle (PostCSS
  und Co.) reproduzierbar erzeugt wird.

### Geändert
- **Hugo-Theme komplett ausgetauscht**: PaperMod-Submodul entfernt, das
  zuvor neu eingeführte Eigen-Theme `aventurien` aus markenrechtlicher
  Vorsicht zu `rollenspiel` umbenannt. `localStorage`-Key
  `aventurien-theme` → `rollenspiel-theme`, PostCSS-Pfade und Partials
  nachgezogen.
- `partials/post-summary.html` nutzt jetzt direkt `.Summary` von Hugo
  statt einer eigenen Regex-H2-Logik — Voraussetzung für die neuen
  Frontmatter-Summaries.
- **`config.yml` aufgeräumt**: 71 Zeilen PaperMod-Erbschaft entfernt
  (–30 %, von 235 auf 164 Zeilen). Beibehalten wurden nur Parameter,
  die nachweislich vom `rollenspiel`-Theme genutzt werden.
- **Hero-Layout neu sortiert**: Meta-Zeile (Datum · Min. · Autor) wandert
  ins Hero-Main unter den Lead-Text; im Hero-Side steht jetzt der
  poetische Claim aus `params.home.claim.big` als großes Italic-Statement,
  inkl. Zierbalken (`border-left`).

### Entfernt
- PaperMod als Theme und als Git-Submodul.
- `home__claim`-Streifen unter dem Hero, `params.home.claim.info` und
  `params.home.heroCaptionFallback` (passten nicht zum neuen Claim-Ton).

---

## 2026-05-01 — Eigenes Theme „Aventurien"

### Hinzugefügt
- Komplett neues Hugo-Theme `themes/aventurien/` (später → `rollenspiel`)
  als Ersatz für PaperMod. Drei Layout-Varianten (Hero-Home,
  Article-Single, Filter-Archive), monumentale Cinzel-Wordmark,
  Pergament/Grimoire-Palette mit Light- und Dark-Modus, 1440-px-Page-
  Container mit Schatten.
- PostCSS-Pipeline (`postcss-import`, `autoprefixer`) für das CSS-Bundle.
- Footer- und Hero-Texte vollständig per `params.{footer,home,brand}` in
  `config.yml` konfigurierbar.
- Cover-Image-Partial liest `cover.image`/`cover.caption` aus dem
  Frontmatter (Frontmatter-First, kein Wild-`*.webp`-Fallback mehr).
- Filter-Archive-Pages unter `content/archive/`, `…/dsa/`, `…/dsk/` mit
  drei statischen Filter-Tabs.
- Pagination auf 12 Beiträge pro Seite (3 × 4-Grid).

---

## 2026-03-28 — CI/CD, Rechtsseiten und Aufräumarbeiten

### Hinzugefügt
- **GitHub-Actions-Workflow** für automatisches Deployment auf den
  Contabo-VPS via SSH-Trigger (Actions auf Commit-SHA gepinnt).
- **About-Seite** „Über diese Seite" inkl. Kampagnen-Übersicht und
  Betreiber-Info, Navigation um den `Über`-Link erweitert.
- **Datenschutzerklärung** (DSGVO-konform: Serverlogs, Contabo-AVV).
- `README.md` und initiale `.mailmap` erstellt, `CLAUDE.md` um
  Tech-Stack-Tabelle, CI/CD-Doku, Vault-Pfade (Linux + macOS),
  Deployment-Beschreibung und Projektstruktur erweitert.

### Geändert
- **Deploy-Strategie umgestellt**: Hugo baut direkt auf dem Contabo-VPS
  (`git pull` → `hugo --destination /var/www/…`). Kein Runner-Build,
  kein `rsync`, kein doppelter Speicher.
- Impressum modernisiert: § 5 TMG → § 5 DDG, rechtlich wirkungsloser
  Haftungsausschluss und nicht mehr existenter § 55 RStV entfernt.
- Footer-Copyright als statischer Wert statt nicht ausgewerteter
  Hugo-Template-Syntax.
- PaperMod-Theme-Submodul aktualisiert (behebt fehlende
  `get-page-images`-Partials).

### Behoben
- **Rechtschreibkorrekturen in 77 Blog-Posts**: Tippfehler, alte
  Rechtschreibung (`daß` → `dass`, `schloß` → `schloss`), falsche
  Zeitformen, inkonsistente Eigennamen (Stordian, Andaryn, Unelementare).
  DSA/DSK-Fachbegriffe wurden bewusst beibehalten.
- YAML-Fehler in `config.yml` (fehlender Listentrenner bei `discord`).
- Doppelte `categories`-Einträge in drei Blog-Posts.
- Execute-Bit für `deploy/build.sh` in Git gesetzt.

---

## 2026-03-18 — Projekt-Setup für Claude Code

### Hinzugefügt
- `CLAUDE.md` für den Claude-Code-Projektkontext.
- MIT-Lizenz.

### Geändert
- `notes.sqlite` aus dem Tracking entfernt und in `.gitignore`
  aufgenommen.

---

## 2025-04 bis 2025-05 — Inhaltsausbau, Murmel-Bogen

### Hinzugefügt
- Neue Beiträge der DSA-Kampagne (u. a. Zwergenschmiede, Alte Bekannte,
  Neuer Freund, Unelementare, Unwasser und Unluft).
- Mehrere DSK-Beiträge und Tagebucheinträge.

### Geändert
- Bestehende Beiträge der Murmel-/Aventurien-Bögen überarbeitet
  (Korrekturen an Zeitlinien, Bildreferenzen, Kleinigkeiten).
- PaperMod-Submodul auf den damals aktuellen Stand aktualisiert.

---

## 2024-08 bis 2025-02 — Streik, Khunchom, Basar-Bande

### Hinzugefügt
- DSK: „Streik der Hafenarbeiter", „Der verrückte Abt", „Aus der Tiefe",
  „Seltsame Gestalten", „Calamari", „Prüfung der Götter", „Das Ende
  des Kultes", „Keine besonderen Vorkommnisse", „Das Loch", „Unter
  Khunchom", „Basar-Bande", „Die Universität".
- DSA: Diverse Beiträge des Greifenfurter Bogens („Vermisste Freunde",
  „Postraub", neue Sitzungsnummern).
- Drittes Rätsel und navigatorische Anpassungen.

### Geändert
- Impressum aktualisiert.
- Konfiguration und Navigation mehrfach feinjustiert.

> **Hinweis**: In diesem Zeitraum häufen sich automatische
> `QOwnNotes commit`-Einträge (Auto-Sync der Editor-Datenbank). Diese
> sind nicht inhaltsrelevant und werden hier nicht einzeln aufgeführt.

---

## 2024-05 bis 2024-08 — Drachentempel, Perricum, Buttercup

### Hinzugefügt
- DSA: „Die Rettung von Aishulibeth", „Zurück nach Ragath", „Der
  Schlüssel zum Tempel", „Der Drachentempel", „Ein Abschied und eine
  Begrüßung", „Gastfreundschaft", „Reise nach Perricum", „Buttercup".
- DSK: „Geschäfte mit dem Don".

### Geändert
- Beitrag „Geschäfte mit dem Don" inhaltlich korrigiert (Inigo statt
  anderer Katze verletzt).
- „Die Vernichtung von Moloch" überarbeitet, Cover-Images für mehrere
  Beiträge ergänzt.

---

## 2024-01 bis 2024-05 — GURPS-Mitschriften, Sommerzeit-Sorgen

### Hinzugefügt
- Alte **GURPS-Mitschriften** als historischer Bestand.
- DSA-Sitzungen 38 bis 41, „An Tagen wie diesen", „Verstärkung",
  „Es wird gruselig!", „Die Reise beginnt", „Die Vernichtung von Moloch".
- DSK 8 bis 10, „Die zweite Murmel und ihre Folgen", Perlenglanz-
  Beiträge, „Die Schriftrollen".
- `Rollenspiel`-Tag eingeführt.

### Behoben
- Zahlreiche Tippfehler-Runden in Bestands-Beiträgen.
- Wiederkehrende Umlaut- und Sommerzeit-Probleme in Captions.

---

## 2023-11 bis 2023-12 — DSK-Premiere und Cover-Images

### Hinzugefügt
- DSK-Sitzungen 1 bis 3 („Glöckchen für den Don", „Die Rettung von
  Goldi's Taverne", „Die Erzählungen für DSK Session 3", „Hort des
  Mondlichtrudels").
- DSA: „Reise nach Wolldorf", „Tempeltor", „Die Suche nach den Murmeln
  beginnt".
- Cover-Image-Workflow eingeführt (PNG → WebP, Pfad-Konventionen).

### Geändert
- Beitragsformat für DSK überarbeitet, Content-Struktur neu sortiert.
- `baseURL` auf `https://` umgestellt.

### Behoben
- Diverse Cover-Image-Fehler, die nur im Live-System sichtbar wurden.

---

## 2023-04 bis 2023-10 — Projektstart

### Hinzugefügt
- **Erstes Hugo-Setup** mit PaperMod-Submodul, deutsche Lokalisierung,
  Favicons, Impressum vorbereitet.
- DSA-Sitzungen 29 bis 32, Kategorie „Kampagne", erste Avatare der
  Spieler.
- Beiträge „Aller Anfang ist schwer", „Familienzusammenführung",
  „Verlassene Mine".
- PayPal-Link auf der Startseite.

### Geändert
- Twitch- und GitHub-Links angepasst.
- PaperMod auf `master`-Branch fixiert.

### Entfernt
- `public/`-Verzeichnis aus dem Repository (gehört in den Build).
