# Stil-Briefing für Edrics Notizen

Verbindliche Regeln für die Erzählstimme. Ergebnis eines Interviews mit dem Nutzer (2026-07-04) — bei künftigen Anpassungswünschen hier ändern, nicht stillschweigend im Fließtext abweichen.

## Perspektive

**Ich-Form, durchgehend aus Edric Stonepaths Sicht.** Kein auktorialer Erzähler, kein Perspektivwechsel innerhalb eines Kapitels. Begründung: passt zu seinem Trait „spricht mehr mit sich selbst als mit anderen" und den bereits vorliegenden Mitschriften, die selbst schon Ich-Form sind.

## Künstlerische Freiheit

**Ausgeschmückt, aber faktentreu.** Erfundene Dialogzeilen, Sinneseindrücke, Szenenübergänge, innere Kommentare sind erlaubt und erwünscht — die in den Mitschriften belegten Ereignisse, Namen und deren Reihenfolge dürfen dabei nicht verändert oder erfunden werden. Wo eine Mitschrift lückenhaft ist (z. B. fehlende Namen in `Extern.md`), aus dem Kontext plausibel ergänzen, nicht frei erfinden.

## Running Gags / wiederkehrende Motive

**Dezent.** Motive wie das Bier, das Murmeln vor sich hin, oder Handwerks-Weisheiten dürfen anklingen, wenn die Mitschrift sie hergibt (z. B. das Bier-Motiv ist in beiden vorliegenden Mitschriften real belegt) — aber nicht als aufgesetzter Running Gag in jedem Kapitel wiederholen, wenn die Quelle dafür keinen Anlass gibt. Andeutung statt Wiederholungsschema.

## Umgang mit Fremdquellen (z. B. Extern.md)

Edric erzählt nur, was er selbst wahrgenommen hat. Szenen aus einer fremden Mitschrift, bei denen Edric nicht anwesend war:

- **Nur als Hörensagen einbauen**, dort wo die eigene Mitschrift ohnehin ein Gruppentreffen zeigt (z. B. abends in der Taverne, Austausch der Erkenntnisse — dieses Muster ist in beiden Mitschriften explizit vorhanden).
- Formulieren als "X erzählte mir…", "Aus dem, was Y berichtete…", nie als Edrics eigene Beobachtung darstellen.
- Fehlt in `Extern.md` ein Name (Format-/Exportfehler der Quelle), aus dem Kontext der eigenen Mitschrift plausibel zuordnen (z. B. "die Kleriker" → Gregor, "die Diebin" → Lysa). Bleibt die Zuordnung unklar, umschreiben statt zu raten ("einer aus der Truppe").

## Granularität

**Ein Blogpost pro Session/Datum.** Jede Mitschrift-Datei bzw. jedes Datum innerhalb einer Mitschrift wird ein eigenständiger Post unter `content/posts/<datum>-<slug>/index.md` — analog zur bestehenden Praxis im Blog (ein Post pro Sitzung).

## Sprachmuster

Siehe [persona-edric-stonepath.md](persona-edric-stonepath.md), Abschnitt „Sprachmuster".

## Format

- **Frontmatter:** `title`, `summary` (45–60 Wörter, gleiche Konvention wie `post-summary`-Skill), `author: hnsstrk`, `date`, `categories:` (Block-Style, analog zu allen Bestandsposts):
  ```yaml
  categories:
    - Edrics Notizen
  tags:
    - Rollenspiel
  ```
- **Body:** Zwischenüberschriften (`##`) für Szenenwechsel, analog zu bestehenden Posts (siehe `content/posts/2023-10-21-Aller_Anfang_ist_schwer/index.md` als Formatvorlage).
- **Keine Spoiler-Titel-Overkill**, keine Werbefloskeln — gleiche Anti-Beispiele wie im `post-summary`-Briefing gelten sinngemäß.

## Beispiel (Tonalität, keine Vorlage für Ereignisse)

> Old Jordan schuldete mir noch immer ein Bier. Ich hatte das nicht vergessen, auch wenn zwei Leichen auf seinem Boden lagen und mein wichtigstes Anliegen offensichtlich niemanden sonst interessierte. Metall lügt nicht — aber ein Wirt, der einem mitten in der Aufregung ein Bier verspricht, offenbar auch nicht immer die Wahrheit.
