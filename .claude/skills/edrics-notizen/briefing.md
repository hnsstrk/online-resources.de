# Stil-Briefing für Edrics Notizen

Verbindliche Regeln für die Erzählstimme. Ergebnis eines Interviews mit dem Nutzer (2026-07-04) — bei künftigen Anpassungswünschen hier ändern, nicht stillschweigend im Fließtext abweichen.

## Perspektive

**Ich-Form, durchgehend aus Edric Stonepaths Sicht.** Kein auktorialer Erzähler, kein Perspektivwechsel innerhalb eines Kapitels. Begründung: passt zu seinem Trait „spricht mehr mit sich selbst als mit anderen" und den bereits vorliegenden Mitschriften, die selbst schon Ich-Form sind.

## Tempus

**Erzählte Handlung steht in der Vergangenheitsform (Präteritum/Perfekt/Plusquamperfekt).** Edric berichtet rückblickend, nicht live. Das gilt für:

- **Ereignisse und Handlungen** — was passierte, was gesagt/getan wurde.
- **Reported Speech / indirekte Rede.** Konjunktiv-I-Formen wie „sei", „habe", „gebe", „tue" sehen wie Präsens aus und sind zu vermeiden — stattdessen Indikativ Präteritum/Plusquamperfekt verwenden ("er sagte, sie sei krank gewesen" → "er sagte, sie war krank gewesen").
- **Generische/zeitlose Aussagen** über Orte oder Personen innerhalb der erzählten Szene ("hier leben Leute, die..." → "hier lebten Leute, die...").

**Ausnahme: Edrics eigene Überlegungen/Kommentare beim Schreiben bleiben im Präsens.** Wenn Edric mitten in der Erzählung eine Randbemerkung, Vermutung oder ein trockenes Urteil einwirft — nicht über das, was damals geschah, sondern über seine eigene, bis heute gültige Haltung dazu —, ist Präsens richtig, genau wie in einem echten Tagebuch. Erkennungszeichen: die Aussage bleibt wahr, während er schreibt, nicht nur während der Szene.

- ✅ "ich vermute, es gibt ein Gesetz dagegen, aber das ist nicht mein Fachgebiet" (Edrics andauernde Haltung, kein Teil der erzählten Handlung)
- ✅ "Kapellen sind nicht mein Fachgebiet." / "Muss nichts bedeuten." (trockener Kommentar im Jetzt des Schreibens)
- ❌ nicht die erzählte Handlung selbst ins Präsens ziehen ("die Truppe fleddert die Toten" statt "fledderte")

Im Zweifel: Passiert es in der Szene → Vergangenheit. Ist es Edrics Kommentar über die Szene → Präsens erlaubt.

Modale Konjunktiv-II-Formen (könnte, müsste, wäre) sind unproblematisch, da sie Möglichkeit/Vermutung ausdrücken, nicht Präsens.

## Session-Datum vs. Ingame-Zeit

**Die Datumsangaben der Mitschriften (z. B. 09.04.2026, 23.04.2026) sind reale Sessiontermine — keine Ingame-Zeitspanne.** Im Spiel hängen die Tage zusammen. Zwischen zwei Sessions vergehen in der Fiktion meist nur ein bis zwei Ingame-Tage, selbst wenn real-weltlich Wochen oder Monate dazwischenliegen (z. B. weil eine Session ausgefallen ist oder der Spieler nicht dabei war — der Charakter selbst hat dann höchstens ein, zwei Ingame-Tage "verpasst", nicht die reale Lücke).

- **Nie** aus der realen Datumsdifferenz auf eine erzählte Zeitspanne schließen ("ein paar Wochen später", "in den Wochen danach").
- Wenn eine Mitschrift explizit einen Zeitsprung nennt (z. B. "am nächsten Morgen"), diesen wörtlich übernehmen.
- Ist die tatsächliche Ingame-Zeitspanne unklar, vage bleiben ("kurz danach", "in der Zwischenzeit") statt eine konkrete Dauer zu erfinden.
- Das `date:`-Frontmatter-Feld darf trotzdem den realen Sessiontermin verwenden (Blog-Konvention, keine Ingame-Aussage) — nur der Fließtext darf keine falsche Ingame-Dauer suggerieren.

**Es gibt (Stand 2026-07-04) noch kein Ingame-Kalendersystem.** Der Spielleiter hat keine Zeitrechnung für die Spielwelt festgelegt — welcher Wochentag oder welches Datum in der Fiktion herrscht, lässt sich nicht bestimmen. Wochentags-Label in Edrics eigener Mitschrift ("Dienstag", "Mittwoch", "Donnerstag") sind rein private Zählhilfen des Spielers, um für sich selbst den Ablauf zu ordnen — sie entsprechen **nicht** echten Wochentagen der realen Sessiontermine und sind kein Hinweis auf einen Ingame-Kalender. Nicht versuchen, diese Label per Wochentagsrechnung (z. B. `datetime.strftime`) auf ein reales Datum zurückzuführen — das führt zu falschen Schlüssen. Als Reihenfolge-Information innerhalb einer Mitschrift sind sie trotzdem brauchbar (Tag 1, Tag 2, Tag 3 einer Session), nur eben nicht als Kalenderdatum.

## Künstlerische Freiheit

**Ausgeschmückt, aber faktentreu.** Erfundene Dialogzeilen, Sinneseindrücke, Szenenübergänge, innere Kommentare sind erlaubt und erwünscht — die in den Mitschriften belegten Ereignisse, Namen und deren Reihenfolge dürfen dabei nicht verändert oder erfunden werden. Wo eine Mitschrift lückenhaft ist (z. B. fehlende Namen in `Extern.md`), aus dem Kontext plausibel ergänzen, nicht frei erfinden.

## Running Gags / wiederkehrende Motive

**Dezent.** Motive wie das Bier, das Murmeln vor sich hin, oder Handwerks-Weisheiten dürfen anklingen, wenn die Mitschrift sie hergibt (z. B. das Bier-Motiv ist in beiden vorliegenden Mitschriften real belegt) — aber nicht als aufgesetzter Running Gag in jedem Kapitel wiederholen, wenn die Quelle dafür keinen Anlass gibt. Andeutung statt Wiederholungsschema.

## Umgang mit Fremdquellen (z. B. Extern.md)

Edric erzählt nur, was er selbst wahrgenommen hat. Szenen aus einer fremden Mitschrift, bei denen Edric nicht anwesend war:

- **Nur als Hörensagen einbauen**, dort wo die eigene Mitschrift ohnehin ein Gruppentreffen zeigt (z. B. abends in der Taverne, Austausch der Erkenntnisse — dieses Muster ist in beiden Mitschriften explizit vorhanden).
- Formulieren als "X erzählte mir…", "Aus dem, was Y berichtete…", nie als Edrics eigene Beobachtung darstellen.
- Fehlt in `Extern.md` ein Name (Format-/Exportfehler der Quelle), zuerst gegen [namen-und-figuren.md](namen-und-figuren.md) prüfen — der bestätigte Cast ist dort aufgelöst. Bleibt die Zuordnung auch dort unklar, umschreiben statt zu raten ("einer aus der Truppe"), und nach Bestätigung durch den Nutzer in `namen-und-figuren.md` ergänzen.

## Granularität

**Ein Blogpost pro Session/Datum.** Jede Mitschrift-Datei bzw. jedes Datum innerhalb einer Mitschrift wird ein eigenständiger Post unter `content/posts/<datum>-<slug>/index.md` — analog zur bestehenden Praxis im Blog (ein Post pro Sitzung).

## Sprachmuster

Siehe [persona-edric-stonepath.md](persona-edric-stonepath.md), Abschnitt „Sprachmuster".

## Format

- **Frontmatter:** `title`, `summary` (45–60 Wörter, gleiche Konvention wie `post-summary`-Skill), `date`, `categories:`/`tags:` (Block-Style, exakt die Einrückung aktueller Bestandsposts — `categories` mit 1 Leerzeichen, `tags` mit 2):
  ```yaml
  categories:
   - Edrics Notizen
  tags:
    - Rollenspiel
  ```
  Kein `author`-Feld — `params.author: hnsstrk` ist bereits Site-Default in `config.yml`, aktuelle Posts (2024/2025) lassen das Feld konsequent weg.
- **Body:** Zwischenüberschriften (`##`) für Szenenwechsel, analog zu bestehenden Posts (siehe `content/posts/2023-10-21-Aller_Anfang_ist_schwer/index.md` als Formatvorlage).
- **Keine Spoiler-Titel-Overkill**, keine Werbefloskeln — gleiche Anti-Beispiele wie im `post-summary`-Briefing gelten sinngemäß.

## Beispiel (Tonalität, keine Vorlage für Ereignisse)

> Old Jordan schuldete mir noch immer ein Bier. Ich hatte das nicht vergessen, auch wenn zwei Leichen auf seinem Boden lagen und mein wichtigstes Anliegen offensichtlich niemanden sonst interessierte. Metall lügt nicht — aber ein Wirt, der einem mitten in der Aufregung ein Bier verspricht, offenbar auch nicht immer die Wahrheit.
