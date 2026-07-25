# Stilgedächtnis — Cover je Reihe

Erhoben am 25.07.2026 aus den vorhandenen Covern. Die Bausteine sind für **FLUX.2 [klein]** formuliert: Farben ausgeschrieben statt als HEX-Code, weil HEX-Prompting nur für [pro]/[max] dokumentiert ist. Die Hex-Werte stehen als präzise Fassung derselben Farbworte dabei — jeweils eine repräsentative Palette aus zwei bis drei Covern der Reihe, nicht aus einem Einzelbild gemessen.

Der Baustein wird **unverändert** ans Ende der Szenenbeschreibung gehängt, vor das `Style:/Mood:`-Suffix.

Geführt werden nur die beiden laufenden Reihen. Die DSK-Reihen (Benjamin Büchernase, Tagebuch von Inigo) und GURPS **bekommen keinen Stil** — entschieden am 25.07.2026. Ihre Cover folgen ohnehin keinem gemeinsamen Look. Wird für einen Post dieser Reihen doch einmal ein Bild gebraucht, entsteht der Prompt ohne Reihen-Baustein; nachfragen ist dann unnötig.

---

## Edrics Notizen

**Kategorien:** `Dungeons & Dragons 5e` + `Edrics Notizen`
**Grundlage:** alle 5 Cover der Reihe (04/2026–07/2026), streng einheitlich
**Referenzbild** (für `--sref` und Cloud-Modelle):
`https://www.online-resources.de/posts/2026-07-23-acht_ratten_und_kein_zeichen/kanalratten.webp`

> `Traditional oil painting on coarse canvas, thick visible impasto brushstrokes, paint dragged and scumbled, edges dissolving into brushwork rather than drawn, forms suggested instead of rendered, visible canvas weave in the highlights, a single warm amber light source glowing at the vanishing point against deep teal-grey shadows, cinematic one-point perspective receding into depth, muted earthy palette of near-black bark brown, burnt sienna and cold slate green, figures as solid black shapes against the glow.`

**Warum diese Formulierung — am 25.07.2026 im Vergleich erarbeitet:** Der erste Baustein lautete „painterly digital matte painting with soft oil-like brushwork". Das beschreibt ein *digitales Bild, das nach Öl aussieht* — und genau das lieferte Klein: glatte Flächen, gerenderte Rohre, jeder Ziegel einzeln. Erst die Beschreibung der **Machart statt der Wirkung** kippte das Ergebnis: Farbe geschleppt und geschrubbt, Kanten die sich in Pinselstrich auflösen, „forms suggested instead of rendered". Merksatz für neue Reihen: nicht sagen, wonach es aussehen soll, sondern was der Pinsel tut.

Ebenso `figures as solid black shapes against the glow` statt „small dark silhouettes" — der Refine-Pass modelliert Figuren sonst wieder aus, und Menschen sind Kleins schwächste Stelle.

**Motivkreis:** Kanalisation und Gewölbe unter Waterdeep, Hafenviertel mit Fachwerk und Schiffsmasten, verwohnte Schankräume, Schmiede und Werkstatt mit Amboß, verrostete Rohre mit Dampf, nasses Kopfsteinpflaster mit Lichtreflex.

**Eigenheiten:** Der Blick zieht fast immer in die Tiefe — Tunnel, Gasse, Schankraum. Vordergrundelemente (Planken, Fässer, Tischkante) rahmen das Bild. Kamera auf Augenhöhe. Figuren sind entweder gar nicht da oder reine Silhouetten ohne Gesichtsdetails; erzählt wird über den Ort.

**Hex (für [pro]):** `#1B140B` · `#A15526` · `#48504C` · `#F5B736`

---

## Greifenfurter Adel

**Kategorien:** `Das schwarze Auge` + `Greifenfurter Adel`
**Grundlage:** die 4 neuesten Cover (2025). **Achtung:** Die Reihe hat einen Stilbruch — die Cover bis 2023 sind fotorealistische Nebellandschaften. Maßgeblich ist der gemalte Stil ab 2024.
**Referenzbild** (für `--sref` und Cloud-Modelle):
`https://www.online-resources.de/posts/2025-05-03-unwasser_und_unluft/unwasser.webp`
Niemals ein Cover von 2023 oder früher als Referenz nehmen — das holt den fotorealistischen Bruch zurück.

> `Dramatic oil painting on canvas, loaded brush and visible impasto, edges dissolving into brushwork rather than drawn, one warm amber light source glowing against cool desaturated blue-grey gloom, symmetrical central vanishing point framed by weathered stone architecture, drifting haze and a wet reflective floor, tiny figures as solid black shapes for scale, palette of deep olive black, cold sage grey and burnt copper.`

*Analog zum Edric-Baustein auf Machart umgestellt (25.07.2026) — die Öl-Formulierung ist dort am Bild belegt, für diese Reihe noch nicht gegengeprüft. Der frühere Zusatz „high architectural detail" ist bewusst entfallen: Er zog das Ergebnis ins Gerenderte, während `klein_slider_detail` im negativen Bereich gerade dagegen arbeitet.*

**Motivkreis:** Gewölbe und Kanäle mit Wasserlauf in der Mittelachse, Fackelreihen an Quadermauern, Elementarwesen aus Feuer, Wasser und Nebel, Lagerhäuser und Kellergänge, tulamidisch-orientalische Basar- und Wüstenarchitektur, Zwergenschmiede.

**Eigenheiten:** Stärker symmetrisch als Edrics Notizen — Fluchtpunkt mittig, links und rechts spiegelnde Architektur, das Motiv frontal in der Mitte. Kamera gelegentlich leicht untersichtig, damit die Bedrohung größer wirkt. Ausnahme im Bestand: ein helles Tageslicht-Porträt einer Echsen-Figur — gleicher Malstil, invertiertes Lichtkonzept. Für Tagszenen taugt es als Vorbild.

**Hex (für [pro]):** `#1F241F` · `#556153` · `#976138` · `#3F3843`

---

## Technische Konventionen für alle Reihen

- **Zielmaß:** 2912×1632 WebP (16:9). In Klein 1456×816 generieren, dann 2× skalieren.
- **Dateiname:** kurzes deutsches Substantiv, klein geschrieben — `kanalratten.webp`, `unwasser.webp`, `hafenviertel.webp`.
- **Cover immer über `cover.image` im Frontmatter bestimmen**, nie per Verzeichnis-Scan: in den Post-Bundles liegen 34 Dateien, die nirgends referenziert sind (33 Bilder und eine Audiodatei), und zwei verschiedene Cover heißen beide `loch.webp`.
- **Kein Text im Bild** — keines der bestehenden Cover trägt welchen.
