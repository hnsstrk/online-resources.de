# Stil-Briefing für Helbrechts Chronik („Greifenfurter Adel")

Verbindliche Regeln für die Erzählstimme. Abgeleitet aus der Analyse der Bestandskapitel (2026-07-23: 14 der 62 Kapitel quer über die Reihe vollständig gelesen, die übrigen per Grep auf Rundenköpfe, Frontmatter und Namen geprüft; Runden 01–61) — bei künftigen Anpassungswünschen hier ändern, nicht stillschweigend im Fließtext abweichen.

## Perspektive

**Wir-Form für die Gruppe, mit Helbrecht als eingebettetem Ich-Erzähler.** „Wir" handelt; das „ich" wertet, plant, ordnet ein und sorgt sich. Kein auktorialer Erzähler, kein Perspektivwechsel. Die Abschnitte-je-Charakter-Form (`### Link`, `### Andaryn`) gehört zur Frühphase der Reihe (Runden 01–09) und wird NICHT mehr verwendet.

**Helbrechts Name fällt im Text nicht** — er ist die Ich-Instanz. Sein Familienname („von Greifenhorst"/„Greifenhorst-Schwarzberg") ist in keinem der 62 Bestandskapitel etabliert und wird ohne ausdrücklichen Nutzerwunsch nicht eingeführt.

## Tempus

**Erzählte Handlung im Präteritum** — Helbrecht chronographiert rückblickend. **Ausnahme: seine bis heute gültigen Kommentare und Sorgen stehen im Präsens**, wie in den Bestandskapiteln belegt („Doch dieser alte Schwarzpelz … macht mir Sorgen. Ich fürchte, dass wir ihn nicht zum letzten Mal gesehen haben."). Erkennungszeichen: Die Aussage gilt noch, während er schreibt — dann Präsens erlaubt; die Szene selbst bleibt Vergangenheit.

## Ton und Stimme

- **Förmlich-adlig, leicht pathetisch, mit trockener Ironie und Standesbewusstsein.** Untertreibung statt Effekthascherei; Spott gern auf Kosten der eigenen Gruppe, nie hämisch.
- **Götteranrufungen als Sprachfärbung**, sparsam und formelhaft: „Der Gnade der Zwölfe sei Dank", „in Borons Reich eingehen". Keine Predigten.
- **Satzbau:** eher lang und hypotaktisch mit Einschüben; in Kampfszenen kürzer getaktet.
- **Kämpfe als taktische Choreografie** — wer tat was, in welcher Reihenfolge, mit welchem Plan. Helbrecht bewertet als Stratege nach („Meiner Meinung nach wäre es sinnvoller gewesen …").
- **Soziale Szenen als genaue Beobachtung** von Rang, Blicken, Andeutungen und Intrige.
- **Kapitelschluss:** oft mit Vorausdeutung oder offener Sorge — nie mit auflösendem Wissen.

## Schreibweisen (konsistent halten — belegte Formen der Reihe)

- **Helbrecht:** im Fließtext nie namentlich, nie mit Familiennamen (er ist das „ich").
- **Götterformeln:** wie belegt „Der Gnade der **Zwölfen** sei Dank" (Genitiv mit -n, so steht es in der Chronik), „in Borons Reich eingehen", „Praios' Licht".
- **Magie:** aventurisch umschreiben — „**Madas Gabe**" statt „Magie", Zaubernamen wie „Ignifaxius" unübersetzt.
- **Namen exakt wie in [namen-und-figuren.md](namen-und-figuren.md):** „Andaryn" (voll: Andaryn von Arestehr), „Gray der Eisige" (kurz: Gray), „Link", „Nga'Churr A'Sar" (mit Apostrophen), „Boronep" (voll: Boronep Hairan). Kein Neu-Eindeutschen, keine Spitznamen erfinden.
- **Datierung:** aventurisch in BF, wenn die Quelle ein Ingame-Jahr nennt; sonst keine Jahreszahlen erfinden.

## Wissensgrenze (nicht verletzen)

Strikt Helbrechts Kenntnisstand. Was die Gruppe nicht weiß, bleibt Rätsel, Vermutung oder Sorge („Was deutete dieser Wahnsinnige da nur an?") — niemals auktorial auflösen, keine Spielleiter-Informationen, keine Spoiler. Die Reihe mischt klassisches DSA mit kosmischem Horror (Mythos-Anklänge): Das Unheimliche wirkt durch Andeutung.

## Session-Datum vs. Ingame-Zeit

Das Sitzungsdatum ist ein realer Termin, keine Ingame-Zeitspanne. Nie aus realen Datumsabständen erzählte Zeit ableiten; ohne explizite Angabe in der Quelle vage bleiben („kurz darauf", „am folgenden Morgen" nur, wenn belegt). Das `date:`-Frontmatter-Feld nutzt den realen Termin (Blog-Konvention).

## Künstlerische Freiheit

**Ausgeschmückt, aber faktentreu.** Erfundene Dialogzeilen, Sinneseindrücke, Übergänge und Helbrechts innere Kommentare sind erwünscht — die in der Zusammenfassung belegten Ereignisse, Namen und deren Reihenfolge sind unantastbar. DSA-Terminologie (Götter, Orte, BF-Datierung) korrekt verwenden; bei Unsicherheit lieber vage bleiben als falsch präzisieren.

## Format

- **Pfad:** `content/posts/<datum>-<Titel_Slug>/index.md` — Slug in der Norm der neueren Posts (Großschreibung, Unterstriche: `Unter_Khunchom`).
- **Frontmatter** (Norm der Posts ab 2024 — kein `author`-Feld):
  ```yaml
  title: "Kurzer nominaler Titel"
  summary: "3–4 Sätze, präsentische Wir-Form, gleicher pathetischer Ton wie der Body — atmosphärischer Teaser, keine nüchterne Inhaltsangabe (~250–400 Zeichen)."
  date: <realer Termin, ISO-8601 mit Zeitzonen-Offset>
  categories:
   - Das schwarze Auge
   - Greifenfurter Adel
  tags:
    - Rollenspiel
  ```
  Einrückung exakt so (categories 1 Leerzeichen, tags 2). Kein `cover:` — das ergänzt der Nutzer mit eigenem Bild beim Gegenlesen (Konvention der Reihe: `image`/`caption` mit `.webp`; ältere Posts führen zusätzlich `alt`, die neueren ab 2025 nicht mehr).
- **Body:** erste Zeile immer `## Das schwarze Auge - NN. Runde der Kampagne: Greifenfurter Adel` (NN = nächste fortlaufende Nummer; bündelt ein Post ausnahmsweise zwei Sitzungen: `NN. und MM. Runde`). Danach Fließtext, bei Szenen-/Ortswechseln `###`-Zwischenüberschriften nach Ort („### In der Kanalisation"). Zielumfang 800–1400 Wörter. Der Einstieg schließt an das Ende des letzten Kapitels an.

## Beispiel (Tonalität — konstruiertes Beispiel im Stil der Reihe, KEIN Zitat und keine Vorlage für Ereignisse)

> Der Gnade der Zwölfen und einigen Heiltränken sei Dank, dass ich an jenen Tagen nicht in Borons Reich einging. Meiner Meinung nach wäre es freilich sinnvoller gewesen, den Rückzug zu ordnen, statt sich wie ein Ochse in die vorderste Reihe zu drängen — doch wer hört in solchen Stunden schon auf seinen Chronisten. Was dieser Wahnsinnige uns damit sagen wollte, weiß ich bis heute nicht. Es macht mir Sorgen.

Wörtlich belegte Sätze der Reihe: siehe [persona-helbrecht-von-greifenhorst.md](persona-helbrecht-von-greifenhorst.md), „Sprachmuster".
