# Stilgedächtnis — Cover je Reihe

Erhoben am 25.07.2026 aus den vorhandenen Covern. Die Bausteine sind für **FLUX.2 [klein]** formuliert: Farben ausgeschrieben statt als HEX-Code, weil HEX-Prompting nur für [pro]/[max] dokumentiert ist. Die Hex-Werte stehen als präzise Fassung derselben Farbworte dabei — jeweils eine repräsentative Palette aus zwei bis drei Covern der Reihe, nicht aus einem Einzelbild gemessen.

Der Baustein wird **unverändert** ans Ende der Szenenbeschreibung gehängt, vor das `Style:/Mood:`-Suffix.

Geführt werden nur die beiden laufenden Reihen. Die DSK-Reihen (Benjamin Büchernase, Tagebuch von Inigo) und GURPS **bekommen keinen Stil** — entschieden am 25.07.2026. Ihre Cover folgen ohnehin keinem gemeinsamen Look. Wird für einen Post dieser Reihen doch einmal ein Bild gebraucht, entsteht der Prompt ohne Reihen-Baustein; nachfragen ist dann unnötig.

---

## Edrics Notizen

**Kategorien:** `Dungeons & Dragons 5e` + `Edrics Notizen`
**Grundlage:** die 8 Cover der Reihe (04/2026–08/2026). **Achtung: Die Reihe hat einen Stilwandel** — die Cover ab 07/2026 sind deutlich feiner gemalt als der Baustein von Juli beschreibt. Maßgeblich ist das jüngste Cover, nicht der Text unten.

**Referenzbild** — nach Schauplatz wählen, nicht pauschal:

| Motiv | Referenz |
|---|---|
| Schmiede, Werkstatt | `https://online-resources.de/posts/2026-07-30-gefunden_und_vergessen/esse.webp` |
| Kanal, Gewölbe (wiederkehrender Ort) | `https://online-resources.de/posts/2026-07-23-acht_ratten_und_kein_zeichen/kanalratten.webp` |
| **Neuer Schauplatz, Innenraum, Figur im Bild** | `https://online-resources.de/posts/2026-08-13-eine_uniform_und_eine_fehlende_seite/uniform.webp` |

**Die ersten beiden Zeilen dienen der Ortstreue, die dritte der Stilbindung.** Bei einem
Schauplatz, den es im Bestand schon gibt, ist die Ortstreue wichtiger — dann das Cover dieses
Ortes nehmen, auch wenn es älter ist. Bei einem **neuen** Ort gibt es nichts wiederzutreffen;
dann zählt allein der aktuelle Stil, und der steht in `uniform.webp` (13.08.) und
`messer.webp` (20.08.), nicht in `kanalratten.webp` (23.07.).

Am 29.08.2026 am Bild geprüft: `kanalratten.webp` zeigt den **alten** pastosen Stand —
sichtbare Pinselspur, Formen aufgelöst, Figuren als reine schwarze Silhouetten. Wer es für ein
neues Motiv als Referenz gibt, holt genau den Look zurück, den der Stilwandel abgelöst hat.
`uniform.webp` ist für Innenräume mit Figur die beste Vorlage: aktueller Stil, ruhiger Raum
ohne aufdringliches Inventar, eine ausgearbeitete Gestalt von hinten, eine warme Laterne gegen
kaltes Blaugrün. `messer.webp` hat denselben Stil, schleppt aber Esse, Rauchhaube und
Werkzeugwand mit — nur für Schmiedemotive.

> `Finely rendered oil painting on canvas, smooth paint surface with delicate blending, tight controlled brushwork, crisp precise edges on metal and brickwork, soft even gradations through the shadows, a single warm amber light source against cold slate green darkness, muted earthy palette of near-black brown, burnt sienna and deep teal, most of the frame held in shadow, cinematic perspective receding into depth.`

**Betriebspunkt für diesen Baustein** (Klein 9B, die schnelle Variante mit 4 bis 8 Rechenschritten): drei Regler-LoRAs — `anatomy 2.0` (Körperbau, fängt Kleins schwächste Stelle ab) · `chiaroscuro 2.5` (Hell-Dunkel: Licht bleibt an der Quelle, der Rest fällt in den Schatten) · **`detail +1.0`** (Ausarbeitungsgrad, positiv = feiner) — dazu **8 Rechenschritte**. Nicht die Werte aus dem Cover-Workflow vom 25.07. — die gehören zum alten Baustein.

**Der Stilwandel — belegt am 24.08.2026 an vier Anläufen:** Der Baustein unten stammt vom 25.07. und verlangt einen **pastosen Farbauftrag** — die Farbe so dick aufgetragen, dass die Pinselspur als Relief stehen bleibt (im Prompt heißt das `impasto`) — dazu angedeutete statt ausgearbeitete Formen. Die beiden jüngsten Cover erfüllen das nicht: `esse.webp` (30.07.) und `uniform.webp` (13.08.) sind fein ausmodelliert, glatt, mit sauberen Kanten — `uniform.webp` zeigt sogar eine ausgearbeitete Figur mit Gesicht. Wer sich an den Juli-Baustein hält, produziert ein Bild, das neben dem jüngsten Cover grob wirkt; genau das ist am 24.08. dreimal passiert und wurde dreimal zurückgewiesen. Die wirksamen Hebel in dieser Reihenfolge: **`detail` von −5.0 auf +1.0** (der größte), **Steps von 4 auf 8**, und die Formulierung für den dicken Farbauftrag ersetzt durch „smooth paint surface, delicate blending, tight controlled brushwork, crisp precise edges" — also glatte Oberfläche, weiche Übergänge, kein sichtbarer Strich.

*Die Bausteine selbst sind englischer Prompt-Text und bleiben es — sie gehen wörtlich an das Modell. Erklärt wird im deutschen Text drumherum.*

<details>
<summary>Der alte Baustein vom 25.07.2026 (nicht mehr verwenden)</summary>

> `Traditional oil painting on coarse canvas, thick visible impasto brushstrokes, paint dragged and scumbled, edges dissolving into brushwork rather than drawn, forms suggested instead of rendered, visible canvas weave in the highlights, a single warm amber light source glowing at the vanishing point against deep teal-grey shadows, cinematic one-point perspective receding into depth, muted earthy palette of near-black bark brown, burnt sienna and cold slate green, figures as solid black shapes against the glow.`

Erarbeitet gegen einen ersten Versuch („painterly digital matte painting with soft oil-like brushwork"), der ein *digitales Bild, das nach Öl aussieht* beschrieb und genau das lieferte: glatte Flächen, gerenderte Rohre, jeder Ziegel einzeln. Die Umstellung auf die **Machart statt die Wirkung** war damals richtig und bleibt der Merksatz für neue Reihen: nicht sagen, wonach es aussehen soll, sondern was der Pinsel tut. Nur ist das Ziel inzwischen ein anderer Pinsel.

</details>

**Figuren:** Der alte Baustein schrieb `figures as solid black shapes against the glow` fest. Das gilt nicht mehr pauschal — `uniform.webp` zeigt Edric von hinten mit ausgearbeitetem Profil. Für Motive **ohne** Hauptfigur bleibt die Silhouetten-Formel richtig und gehört dann in den Motivteil; für ein Figurenbild wird sie weggelassen.

**Motivkreis:** Kanalisation und Gewölbe unter Waterdeep, Hafenviertel mit Fachwerk und Schiffsmasten, verwohnte Schankräume, Schmiede und Werkstatt mit Amboß, verrostete Rohre mit Dampf, nasses Kopfsteinpflaster mit Lichtreflex.

**Eigenheiten:** Der Blick zieht fast immer in die Tiefe — Tunnel, Gasse, Schankraum. Vordergrundelemente (Planken, Fässer, Tischkante) rahmen das Bild. Kamera auf Augenhöhe; erzählt wird über den Ort.

### Wiederkehrende Schauplätze

Dieselben Orte kommen mehrfach vor. Wer sie neu erfindet, bricht die Erzählung — im August 2026 landeten dabei Holzdielen in einer Schmiede. **Vor jedem Prompt zu einem bekannten Ort das vorhandene Cover ansehen** und die Merkmale übernehmen; zusätzlich das Bild als Referenz in den Lauf geben.

**Edrics Schmiede** (`esse.webp` 30.07. · `journal.webp` 23.04. · `messer.webp` 20.08.): Wände aus rußgeschwärztem **Ziegel**, kein Putz. **Boden aus Steinplatten**, mit Kohlegrus und Zunder — niemals Holz, dafür fliegen zu viele Funken. Große gemauerte **Esse mit breiter schwarzer Rauchhaube**, das Feuerbett auf einem Sockel in Hüfthöhe, nicht als offener Kamin am Boden. Werkzeug an Eisenhaken in Reihe an der Wand, **Amboß auf einem Holzklotz**, schwere Werkbank aus Eiche.

**Der Kanal unter dem Hafenviertel** (`kanal.webp` 09.07. · `kanalratten.webp` 23.07.): Tonnengewölbe aus Ziegel, Wasserlauf in der Mittelachse, schmale Simse an den Wänden, quer gelegte Planken als Übergang, verrostete Rohre mit Dampf.

**Hex (für [pro]):** `#1B140B` · `#A15526` · `#48504C` · `#F5B736`

---

## Greifenfurter Adel

**Kategorien:** `Das schwarze Auge` + `Greifenfurter Adel`
**Grundlage:** die 4 neuesten Cover (2025). **Achtung:** Die Reihe hat einen Stilbruch — die Cover bis 2023 sind fotorealistische Nebellandschaften. Maßgeblich ist der gemalte Stil ab 2024.
**Referenzbild** (für `--sref` und Cloud-Modelle):
`https://online-resources.de/posts/2025-05-03-unwasser_und_unluft/unwasser.webp`
Niemals ein Cover von 2023 oder früher als Referenz nehmen — das holt den fotorealistischen Bruch zurück.

> `Dramatic oil painting on canvas, loaded brush and visible impasto, edges dissolving into brushwork rather than drawn, one warm amber light source glowing against cool desaturated blue-grey gloom, symmetrical central vanishing point framed by weathered stone architecture, drifting haze and a wet reflective floor, tiny figures as solid black shapes for scale, palette of deep olive black, cold sage grey and burnt copper.`

*Analog zum Edric-Baustein auf Machart umgestellt (25.07.2026) — die Öl-Formulierung ist dort am Bild belegt, für diese Reihe noch nicht gegengeprüft. Der frühere Zusatz „high architectural detail" ist bewusst entfallen: Er zog das Ergebnis ins Gerenderte, während `klein_slider_detail` im negativen Bereich gerade dagegen arbeitet.*

**Motivkreis:** Gewölbe und Kanäle mit Wasserlauf in der Mittelachse, Fackelreihen an Quadermauern, Elementarwesen aus Feuer, Wasser und Nebel, Lagerhäuser und Kellergänge, tulamidisch-orientalische Basar- und Wüstenarchitektur, Zwergenschmiede.

**Eigenheiten:** Stärker symmetrisch als Edrics Notizen — Fluchtpunkt mittig, links und rechts spiegelnde Architektur, das Motiv frontal in der Mitte. Kamera gelegentlich leicht untersichtig, damit die Bedrohung größer wirkt. Ausnahme im Bestand: ein helles Tageslicht-Porträt einer Echsen-Figur — gleicher Malstil, invertiertes Lichtkonzept. Für Tagszenen taugt es als Vorbild.

**Hex (für [pro]):** `#1F241F` · `#556153` · `#976138` · `#3F3843`

---

## Prompt-Fallen — am 29.08.2026 teuer gelernt

Drei Formulierungen haben beim Cover zum Post vom 27.08. je eine ganze Runde
gekostet (vier Bilder, rund 0,30 USD). Alle drei sind vermeidbar, wenn man vor dem
Lauf danach sucht.

**1. Ortsangaben am Motiv wörtlich lesen.** `on its rim a dwarf woman with a lute`
heißt „auf dem Beckenrand" — und genau da stand sie dann, im Brunnen statt davor.
Wer eine Figur **vor** etwas haben will, schreibt, worauf sie steht:
`stands on the flagstones, behind her the basin`. Präpositionen wie *on*, *at*,
*by* setzt das Modell wörtlich um; sie sind keine vage Ortsangabe.

**2. Kein Wort zweimal für verschiedene Dinge.** Im selben Prompt standen
`iron fire bowls` für die Feuerstellen und `stone offering basin` für den
Spendenbrunnen. Ergebnis: In drei von vier Bildern war der Brunnen eine weitere
Feuerschale, das Wasserbecken fehlte ganz. Mit `braziers` für das Feuer war das
`basin` sofort eindeutig Wasser. **Vor jedem Lauf prüfen, ob zwei Dinge im Prompt
dasselbe Gattungswort tragen** — *bowl/basin*, *stand/pillar*, *cloth/cloak*.

**3. Ein Geschlecht setzt sich nur über ein Referenzbild durch.** `a stocky female
dwarf bard`, `her braided hair` — achtmal formuliert, achtmal kam ein männlicher
Zwerg heraus. Erst das Charakterporträt als **zweites Referenzbild** hat es
gedreht, und zwar auf Anhieb. Bei einer wiederkehrenden Figur gehört ihr Porträt
in den Lauf, nicht ihre Beschreibung in den Prompt.

**Und ein Nebenbefund:** Je mehr Einzelheiten der Prompt aufzählt, desto eher fällt
eine davon weg. Als Brunnen, Münzen, Amboss, Kohlebecken und lachende Gesichter
alle zugleich verlangt waren, hatte die Bardin in drei von vier Bildern keine Laute
mehr in der Hand. Was das Motiv trägt, gehört nach vorn — das Modell gewichtet nach
Reihenfolge.

### Referenzbilder von Figuren

**Charakterporträts gehören nicht ins Repository** (Nutzerentscheidung 29.08.2026) —
es ist öffentlich, und die Bilder der Spielfiguren sind es nicht. Sie liegen auf
Ganymed unter `~/Bilder/Rollenspiel/portraets/`. Wer den Skill auf einer anderen
Maschine benutzt, hat sie nicht; dann bleibt nur der Weg über den Prompt, und der
trifft das Geschlecht nicht (siehe Falle 3 oben).

Vor dem Ablegen auf 768 px verkleinern und als JPEG speichern: Das Original mit
1,2 MB bläht den Request auf (Gefahr eines HTTP 413), die verkleinerte Fassung mit
139 kB reicht für Aussehen und Farbe vollkommen.

```bash
magick <original> -resize 768x768 -quality 88 ~/Bilder/Rollenspiel/portraets/<figur>.jpg
```

| Figur | Datei |
|---|---|
| Thyra Hammerhall (Zwergin, Bardin) | `~/Bilder/Rollenspiel/portraets/thyra-hammerhall.jpg` |

Aufruf mit zwei Vorlagen — erst der Reihenstil, dann die Figur:

```bash
--referenz "https://online-resources.de/posts/.../uniform.webp" \
--referenz ~/Bilder/Rollenspiel/portraets/thyra-hammerhall.jpg
```

## Technische Konventionen für alle Reihen

- **Zielmaß:** 2912×1632 WebP (16:9). In Klein 1456×816 generieren, dann 2× skalieren. Über OpenRouter ist die Auflösung nicht steuerbar — `scripts/cover.py` skaliert selbst auf das Zielmaß.
- **Dateiname:** kurzes deutsches Substantiv, klein geschrieben — `kanalratten.webp`, `unwasser.webp`, `hafenviertel.webp`.
- **Nachbearbeitung immer mit `-quality 92`.** ImageMagick schreibt WebP sonst mit Qualität 75 neu: Beim Retuschieren am 29.08.2026 schrumpfte ein Cover dabei von 602 auf 213 kB. Sichtbar war es nicht, aber vermeidbar. **Und das unbearbeitete Original erst löschen, wenn die bearbeitete Fassung geprüft ist** — am 29.08. war es umgekehrt, damit gab es keinen Weg zurück.
- **Cover immer über `cover.image` im Frontmatter bestimmen**, nie per Verzeichnis-Scan: in den Post-Bundles liegen 34 Dateien, die nirgends referenziert sind (33 Bilder und eine Audiodatei), und zwei verschiedene Cover heißen beide `loch.webp`.
- **Kein Text im Bild** — keines der bestehenden Cover trägt welchen. **Ausnahme: Schrift als Textur.** Ein beschriebenes Blatt darf beschrieben aussehen; Klein malt dann Handschriftzeilen, die keine Wörter ergeben (`a few lines of dark scrawled handwriting`). Das ist gewollt und funktioniert. Lesbare Wörter kann Klein nicht — wer sie braucht, setzt sie hinterher mit einem Schrift-Font ein.
