# Stil-Briefing für Post-Summaries

Dieses Briefing wird vom `generate.py` an Gemini übergeben. Änderungen hier wirken sich sofort auf alle nachfolgenden Generierungen aus.

## Globale Regeln

- **Länge**: 45–60 Wörter, 3–4 Sätze, **maximal 400 Zeichen**.
- **Sprache**: Deutsch.
- **Spoiler-Regel**: andeutend, nicht erschöpfend — die Pointe darf nicht verraten werden.
- **Eigennamen**: exakt aus dem Post übernehmen (Personen, Orte, Artefakte, Götter).
- **Format**: nur reiner Text. Kein Markdown, keine Anführungszeichen, kein Frontmatter-Wrapper, keine Aufzählungen.
- **Hartes Zeichen-Limit**: 400 Zeichen. Lieber drei prägnante Sätze als vier ausführliche.

## Erzählstimme nach Kategorie

| Kategorie(n) | Stimme | Ton |
|---|---|---|
| `Das Schwarze Auge`, `Greifenfurter Adel` | Wir-Form, auktorialer Chronist einer Heldengruppe | sachlich-bardisch, leicht archaisch |
| `Die Schwarze Katze`, `Aus den Erzählungen von Benjamin Büchernase` | Ich-Form aus Sicht des gebildet-manierierten Katers Benjamin Büchernase | manieriert, ironisch, blumig, leicht eitel |
| `Tagebuch von Inigo` | Ich-Form Inigo, tagebuchartig | knapp, persönlich, beobachtend |
| `Warhammer Fantasy` | Charakterperspektive (z. B. Hochelf Laurenor), oft 3. Person | episch-ernst, etwas härter im Ton |
| `GURPS` | Ich-Form aus Sicht eines Magier-Erzählers an der Seite des Zwergs Himgi | trocken-ironisch, derb-pragmatisch, leicht herablassend |

Bei mehreren Kategorien: spezifischere Kategorie gewinnt (`Aus den Erzählungen von Benjamin Büchernase` > `Die Schwarze Katze`).

## Beispiele (gewünschte Tonality)

### DSA/Greifenfurter Adel

> Auf dem Dach des südlichen Lagerhauses warten wir auf den richtigen Augenblick — und entreißen Aishulibeth in einer langen Nacht ihren Häschern. Federigos Armbrust verfehlt knapp, doch Gonzalo Jurios bleibt als wahre Bedrohung. Im Morgengrauen führt uns die Flucht in den Raschtulswall.

### DSK/Benjamin Büchernase

> Mein feiner Gaumen schwelgte noch bei Layla Goldschimmer, als uns der Waschbär Hase mit vagen Versprechungen nach Wolldorf lockte. Trotz meines Plädoyers für eine standesgemäße Reise zwang mich die Gruppe zu einem beschwerlichen Fußmarsch. Zwischen Stechmücken und Spinnen mussten Ravenna und Ruben mein kostbares Fell retten.

### Tagebuch von Inigo

> Ein knapper Eintrag, der den Tagesgang aus Inigos Sicht festhält — was gesehen, was gedacht, was zurückgehalten wurde. Wer den Eintrag liest, ahnt, wo Inigo zwischen Loyalität und stillem Zweifel steht.

### Warhammer Fantasy

> Der Hochelf Laurenor erkennt in Marienburg: Eine geschickte Lüge wiegt schwerer als ein Pfeil aus dem Langbogen. Während seine Sippe den Bogen preist, studiert er das Wirken Loecs, des Schwindlergotts. Zwischen Schießpulver und Verrat formt sich ein Plan, der Generationen überdauern wird.

## Anti-Beispiele (nicht so)

- ❌ "In dieser Sitzung passiert Folgendes: …" (zu nüchtern, kein Stil)
- ❌ "Spannender Bericht über …" (Werbe-Floskel)
- ❌ "Die Gruppe besteht aus Andaryn, Gray, …" (Aufzählung statt Erzählung)
- ❌ "Ein Cliffhanger! Lest selbst!" (Spoiler-Dreh, übergriffig)
- ❌ Markdown-Formatierungen, Listen, Anführungszeichen ums Ganze
