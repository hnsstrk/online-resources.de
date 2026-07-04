---
name: edrics-notizen
description: |
  Verwandelt rohe D&D5e-Sitzungsmitschriften (Stichpunkte, oft unvollständige
  Notizen) in vollständige Hugo-Blog-Kapitel, erzählt in Ich-Form aus der Sicht
  von Edric Stonepath (Artificer/Waffenschmied, Waterdeep). Legt pro Session/
  Datum einen neuen Post unter content/posts/ an, inkl. Frontmatter und
  Kategorie "Edrics Notizen".
  TRIGGER when: user wants to turn D&D5e session notes/summaries into a blog
  post, mentions "Edric", "Mitschrift in eine Erzählung verwandeln", "Session
  als Kapitel schreiben", "Abenteuer-Post für D&D5e".
  DO NOT TRIGGER when: user only wants a short summary field for an existing
  post (use post-summary instead), or works on DSA5/DSK/GURPS content.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# edrics-notizen — Skill

Schreibt aus rohen Sitzungsmitschriften vollständige, atmosphärische Blog-Kapitel für die D&D5e-Kampagne — in der festen Ich-Form-Stimme von Edric Stonepath.

## Warum Skill statt Agent

Die Aufgabe ist eine wiederholbare, fest umrissene Prozedur (Quellen lesen → feste Stimme anwenden → Hugo-Post schreiben) ohne offene Exploration oder wechselnde Tool-Strategie — das ist die Domäne eines Skills, nicht eines Agents. Genau dieses Muster existiert im Repo bereits als `post-summary`-Skill für Kurz-Summaries; dieser Skill folgt derselben Architektur für vollständige Kapitel. Ein Agent wäre angemessen, wenn die Quellenlage unklar wäre oder autonome Recherche über mehrere Systeme nötig wäre — hier sind Quellen und Zielformat von Anfang an fix.

## Wann nutzen

- Nach einer Session, wenn eine eigene Mitschrift (z. B. `DnD5e_YYYYMMDD.txt`) und optional die Mitschrift eines Mitspielers vorliegen.
- Wenn mehrere Sessions/Daten auf einmal in Blog-Kapitel umgesetzt werden sollen.

## Quellen

| Quelle | Rolle |
|---|---|
| Edrics eigene Mitschrift | Primärquelle — Rückgrat der Erzählung, Ich-Form direkt verwendbar |
| `Extern.md` (Mitschrift eines anderen Spielers) | Sekundärquelle für Szenen ohne Edric — nur als Hörensagen einbauen (siehe briefing.md). Enthält oft fehlende Eigennamen (Exportfehler des anderen Tools) — beim Zuordnen im Kontext der eigenen Mitschrift plausibilisieren, nicht raten |
| FoundryVTT-Charakterbogen (`fvtt-Actor-*.json`, Feld `system.details.biography`) | Persönlichkeit/Hintergrund — keine Ereignisse. Destillat: [persona-edric-stonepath.md](persona-edric-stonepath.md) |
| [namen-und-figuren.md](namen-und-figuren.md) | Bestätigter Cast (Namen, Rollen, aufgelöste Namens-Lücken aus `Extern.md`) — vor dem Schreiben immer gegenprüfen, bevor ein Name aus einer Mitschrift übernommen wird |

## Arbeitsweise

1. Alle Mitschriften einlesen, nach Datum sortieren.
2. Pro Session/Datum einen Post planen (Granularität: siehe briefing.md).
3. Ereignisse aus Edrics eigener Mitschrift als Faktenbasis übernehmen — Reihenfolge und Inhalte nicht verändern. Namen gegen [namen-und-figuren.md](namen-und-figuren.md) prüfen (z. B. „Arik" in der Mitschrift → „Alric Dorn" im Post).
4. Szenen aus `Extern.md`, die Edric nicht selbst erlebt hat, nur dort einbauen, wo die eigene Mitschrift ein Gruppentreffen zeigt (z. B. abends in der Taverne) — als Hörensagen, nicht als eigene Wahrnehmung.
5. Nach [briefing.md](briefing.md) ausschmücken: erfundene Dialogzeilen, Sinneseindrücke, Übergänge erlaubt; Fakten bleiben unangetastet.
6. Hugo-Post anlegen unter `content/posts/<datum>-<slug>/index.md` — Frontmatter- und Body-Format siehe [briefing.md](briefing.md), Abschnitt „Format".
7. Falls `content/categories/edrics-notizen/_index.md` noch nicht existiert, anlegen (Vorlage: `content/categories/tagebuch-von-inigo/_index.md` — `title: "Edrics Notizen"`).

## Stil-Briefing

Siehe [briefing.md](briefing.md) — Perspektive, künstlerische Freiheit, Running Gags, Umgang mit Fremdquellen, Format. Ergebnis eines Interviews mit dem Nutzer; bei Wunsch nach Anpassung dort ändern.

## Fertig, wenn…

- Ereignisse, Namen und ihre Reihenfolge stimmen mit den Mitschriften überein — nichts erfunden, nur ausgeschmückt.
- Alle Eigennamen gegen [namen-und-figuren.md](namen-und-figuren.md) abgeglichen (Spitznamen aus einer Mitschrift durch den dort hinterlegten vollen Namen ersetzt).
- Hörensagen-Szenen aus `Extern.md` tauchen ausschließlich an Punkten auf, wo die eigene Mitschrift ein Gruppentreffen zeigt.
- `summary` ist 45–60 Wörter lang.
- `content/categories/edrics-notizen/_index.md` existiert.

## Bekannte Grenzen

- Nur für Edric Stonepath / diese Kampagne kalibriert. Für andere Charaktere/Kampagnen eigenes Persona-Briefing anlegen (Muster: `persona-edric-stonepath.md` kopieren, Steckbrief + Sprachmuster anpassen).
- Kein automatisiertes Voice-Modell (kein Gemini/Codex-Call wie bei `post-summary`) — Claude schreibt die Kapitel direkt anhand des Briefings.
- Cover-Bild/OG-Image pro Post ist nicht Teil dieses Skills — falls gewünscht, manuell ergänzen oder bestehende Theme-Automatik (Cover-Fallback) greifen lassen.

## Erweiterung

Für weitere Kampagnen/Charaktere: neues Persona-Briefing anlegen, in einer Tabelle „Erzählstimme nach Charakter" (analog zu `post-summary/briefing.md`) referenzieren, statt diesen Skill zu verzweigen.
