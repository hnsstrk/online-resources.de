---
name: helbrechts-chronik
description: |
  Verwandelt neutrale DSA5-Sitzungszusammenfassungen (aus RPG Audio Studio) in
  Kapitel der Kampagnenchronik "Greifenfurter Adel" — erzählt in Wir-Form mit
  Helbrecht (adliger Weißmagier, Stratege) als eingebettetem Ich-Erzähler. Legt
  pro Sitzung einen Hugo-Post unter content/posts/ an, schreibt die fortlaufende
  Rundennummer der Reihe fort (Kategorien "Das schwarze Auge" + "Greifenfurter
  Adel").
  TRIGGER when: user wants to turn a DSA5 session summary into a blog post,
  mentions "Helbrecht", "Greifenfurter Adel", "DSA-Runde als Kapitel schreiben",
  or RPG Audio Studio invokes this skill via blog-draft for a DSA5 session.
  DO NOT TRIGGER when: the session is D&D5e/Waterdeep (use edrics-notizen), the
  user only wants a short summary field (use post-summary), or the content is a
  standalone in-game document/codex without a session.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# helbrechts-chronik — Skill

Schreibt aus einer neutralen Sitzungszusammenfassung das nächste Kapitel der DSA5-Kampagnenchronik „Greifenfurter Adel" — in der etablierten Stimme der Reihe: Wir-Form für die Gruppe, Helbrecht als wertende Ich-Instanz.

## Warum Skill statt Agent

Wie `edrics-notizen`: eine wiederholbare, fest umrissene Prozedur (Quelle lesen → feste Stimme anwenden → Hugo-Post schreiben) ohne offene Exploration. Quellen und Zielformat sind fix; die Reihe existiert mit 62 Kapiteln, an die stilistisch und inhaltlich angeschlossen wird.

## Wann nutzen

- Nach einer DSA5-Sitzung der Greifenfurter-Adel-Runde, wenn RPG Audio Studio eine neutrale Zusammenfassung erzeugt hat (`blog-draft` übergibt Sitzungsdatum und Quellen-Pfad).
- Manuell, wenn eine Sitzungsmitschrift/-zusammenfassung dieser Kampagne in ein Kapitel umgesetzt werden soll.

## Quellen

| Quelle | Rolle |
|---|---|
| Übergebene Sitzungszusammenfassung (Pfad im Aufruf) | Primärquelle — Faktenbasis: Ereignisse, Namen, Reihenfolge. Nichts davon verändern oder erfinden |
| Die bestehenden Chronik-Posts (`content/posts/`, Kategorie „Greifenfurter Adel") | Stil-Referenz, Anschluss an das letzte Kapitel und Quelle der fortlaufenden Rundennummer |
| [persona-helbrecht-von-greifenhorst.md](persona-helbrecht-von-greifenhorst.md) | Erzählstimme: Herkunft, Kernzüge, Sprachmuster mit Original-Zitaten |
| [namen-und-figuren.md](namen-und-figuren.md) | Bestätigter Cast (Gruppe, NSCs, Orte, Handlungsstand) — Namen aus der Zusammenfassung vor der Übernahme hier gegenprüfen |
| Kampagnen-Vault (Logseq), Unterordner `pages/Greifenfurter Adel%2F…` | Optionale Tiefen-Quelle: Charakterseiten und Sitzungsprotokolle mit mehr Detail als der Blog — nur lesend, bei Unklarheiten zu Figuren/Hintergrund. **Pfad nicht fest verdrahten** — der Vault liegt je nach Maschine anders (macOS: `~/Meine Ablage/Vault RPG/`, Linux: unter dem Insync-Ordner); dynamisch auflösen, z. B. `find "$HOME" -maxdepth 4 -type d -name "Vault RPG"` |

## Arbeitsweise

1. Die übergebene Zusammenfassung vollständig lesen — sie ist die Faktenbasis; Ereignisse und deren Reihenfolge bleiben unangetastet.
2. Die **nächste Rundennummer** bestimmen: per Grep über `content/posts/` nach `Runde der Kampagne: Greifenfurter Adel` die höchste Nummer finden (Stand 2026-07: 61) und um eins erhöhen. Den Post mit der höchsten Nummer kurz anlesen, um erzählerisch anzuschließen (die Kapitel beginnen dort, wo das letzte endete).
3. Namen und Figuren gegen [namen-und-figuren.md](namen-und-figuren.md) prüfen; unbekannte Namen aus der Zusammenfassung übernehmen, nicht raten. Unklare Sprecher-Zuordnungen umschreiben („einer aus unserer Runde") statt erfinden.
4. Das Kapitel nach [briefing.md](briefing.md) schreiben — Perspektive, Ton, Tempus, Wissensgrenze und Format sind dort verbindlich geregelt.
5. Hugo-Post anlegen unter `content/posts/<datum>-<Titel_Slug>/index.md` (Slug-Norm der neueren Posts: Großschreibung mit Unterstrichen, z. B. `2026-07-23-Ankunft_in_Selem`). Bestehende Posts NIE überschreiben.

## Stil-Briefing

Siehe [briefing.md](briefing.md) — abgeleitet aus der Analyse der Bestandskapitel (2026-07-23: 14 von 62 vollständig gelesen, Rest per Grep geprüft). Bei Anpassungswünschen dort ändern, nicht stillschweigend abweichen.

## Fertig, wenn…

- Ereignisse, Namen und Reihenfolge stimmen mit der Zusammenfassung überein — nichts erfunden, nur ausgeschmückt.
- Die Rundennummer schließt lückenlos an die höchste bestehende an; die H2-Kopfzeile hat exakt die Form `## Das schwarze Auge - NN. Runde der Kampagne: Greifenfurter Adel`.
- Frontmatter entspricht der aktuellen Norm der Reihe (siehe briefing.md): genau die zwei Kategorien, Tag `Rollenspiel`, kein `author`-Feld.
- `summary` ist 3–4 Sätze in präsentischer Wir-Form, gleicher Ton wie der Body.
- Die Wissensgrenze ist gewahrt: nichts aufgelöst, was die Gruppe nicht weiß.

## Bekannte Grenzen

- Nur für die Kampagne „Greifenfurter Adel" / Helbrechts Stimme kalibriert (Muster für weitere Reihen: `edrics-notizen`).
- Cover-Bild ist nicht Teil dieses Skills — der Nutzer ergänzt `cover:` mit eigenem Bild beim Gegenlesen (Konvention siehe briefing.md).
- Die seltenen In-Game-Dokument-Posts der Reihe („Codex"-Format: Schriftrollen, Patientenakten — ohne Rundennummer, 5000+ Wörter) sind ein eigenes Format und NICHT Teil dieser Prozedur; nur auf ausdrücklichen Wunsch des Nutzers.
