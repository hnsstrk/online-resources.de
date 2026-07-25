---
name: flux-cover
description: |
  Erzeugt aus einem Hugo-Blogpost einen fertigen Bildprompt für FLUX.2 [klein] —
  ausformulierte Prosa statt Keyword-Liste, mit dem Stil-Baustein der jeweiligen
  Reihe, damit die Cover einer Serie zusammenpassen. Liefert dazu ComfyUI-Settings
  und einen Dateinamen-Vorschlag fürs Post-Bundle.
  TRIGGER when: user wants a cover/title image prompt for a post, mentions "Cover",
  "Titelbild", "Bildprompt", "Prompt für das Bild", "Flux", "Klein", "ComfyUI",
  or asks what to feed into the image generator for a blog post.
  DO NOT TRIGGER when: user wants the post text itself (use edrics-notizen or
  helbrechts-chronik), only the summary field (use post-summary), or works on
  Hugo templates and theme code.
allowed-tools: Read, Glob, Grep, Bash
---

# flux-cover — Skill

Baut aus einem Post unter `content/posts/` einen Bildprompt für **FLUX.2 [klein]**, lokal in ComfyUI. Ausgabe ist Text — der Skill generiert kein Bild und schreibt nichts ins Repo.

## Warum Klein anders geprompted wird als Midjourney oder Flux [pro]

Klein hat **kein Prompt-Upsampling**. [pro] und [max] schicken deinen Prompt vorher durch ein Sprachmodell, das ihn ausformuliert — Klein nicht. Sein Textencoder (Qwen3) bekommt den Prompt sogar ohne System-Message: was dasteht, ist alles, was das Modell sieht. Ein Prompt, der bei Midjourney als Stichwortkette funktioniert, liefert hier ein dünnes Bild, weil niemand die Lücken füllt.

Deshalb gilt für jeden Prompt aus diesem Skill: **ausformulierte Prosa**. BFL selbst formuliert es als *„describe scenes like a novelist, not a search engine"*.

Zweitwichtigster Hebel ist das **Licht** — laut BFL der Einzelfaktor mit dem größten Einfluß auf die Bildqualität bei Klein. Beschreibe Quelle, Härte, Richtung, Farbtemperatur und was das Licht mit den Oberflächen macht. Bei den Covern dieses Blogs ist Licht ohnehin das tragende Motiv: eine warme Quelle im Dunkeln.

## Ablauf

1. **Post lesen.** Titel, `summary`, `categories` und Fließtext. Ist kein Pfad genannt, den jüngsten Post nehmen (`ls -t content/posts/`).
2. **Reihe bestimmen** über `categories:` im Frontmatter, dann den passenden Stil-Baustein aus [stile.md](stile.md) holen. Steht die Reihe dort nicht, mit dem Nutzer einen Stil festlegen statt einen zu erfinden — ein geratener Stil bricht die Serie, und das sieht man auf der Übersichtsseite sofort.
3. **Motiv wählen:** ein **Ort oder eine Szene**, keine Handlung mit Gesichtern. Das ist keine Stilfrage, sondern folgt zwei Dingen: Die Cover dieses Blogs erzählen durchgehend über Schauplätze, und Klein zeichnet Menschen unzuverlässig — Anatomie ist seine bekannteste Schwäche. Figuren gehören als kleine dunkle Silhouetten ins Bild, die den Maßstab setzen, nicht als Porträts.
4. **Prompt bauen** nach dem Aufbau unten.
5. **Ausgeben** im Format unten — Prompt, Settings, Dateiname.

## Aufbau des Prompts

Reihenfolge zählt: Klein gewichtet, was zuerst kommt.

```
[Hauptmotiv in einem Satz] → [Raumschichtung] → [Licht] → [Stil-Baustein der Reihe] → Style:/Mood:-Suffix
```

**Raumschichtung** ist das belegt stärkste Muster für stimmungsvolle Szenen — benenne ausdrücklich `Foreground:`, `Midground:`, `Background:` und was in jeder Ebene liegt. Das gibt dem Modell die Tiefenstaffelung vor, statt sie zu erraten.

**Licht** in fünf Aspekten: Quelle (Fackel, Öllampe, Kaminfeuer), Härte, Richtung, Farbtemperatur, Wirkung auf Oberflächen (nasses Kopfsteinpflaster, feuchtes Mauerwerk, Rauch).

**Suffix** am Ende, so wie BFL es dokumentiert:
```
Style: [Medium und Machart]. Mood: [zwei bis drei Stimmungsworte].
```

**Länge: 110–170 Wörter** inklusive Stil-Baustein. BFL unterscheidet drei Bänder — 30–80 Wörter für die meiste Produktionsarbeit, 80–300+ für komplexe Editorial-Motive. Ein Cover mit drei Bildebenen und ausformuliertem Licht gehört ins obere Band; die Wahl ist bewußt, nicht BFLs Standardempfehlung. Dabei gilt BFLs Vorbehalt: jeder Satz muß Bildinformation tragen. Füllwerk verdünnt die Details, die zählen.

## Was den Prompt verdirbt

- **Negationen.** Klein kennt keine Negativ-Prompts, und „ohne Menschen" macht Menschen wahrscheinlicher, weil das Modell auf das Substantiv anspringt. Frag stattdessen: Was sähe man, wenn das Ding nicht da wäre? → `deserted`, `empty`, `unmarked`.
- **Stimmungsworte statt Sichtbarem.** „düster" ist keine Bildinformation. Was macht es düster — welcher Anteil des Bildes liegt im Schatten, wo ist die einzige Lichtquelle, wie weit reicht sie?
- **Keyword-Ketten** mit Kommas. Siehe oben: es gibt niemanden, der sie ausformuliert.
- **Text im Bild.** Die Model Card von klein 4B sagt selbst, gerenderter Text könne *„inaccurate or subject to distortion"* sein; in einem Test von wiro.ai kippte bei 6 von 10 Prompts die Schreibung. Die Cover dieses Blogs tragen ohnehin keinen Text — dabei bleiben.
- **Zahlen als Mengenangabe.** „acht tote Ratten" wird nicht acht. `a heap of dead rats` liefert verläßlich ein stimmiges Bild.

## Ausgabeformat

````markdown
## Prompt — [Titel des Posts]

```
[der Prompt als Fließtext]
```

**Settings** (ComfyUI, klein base 4B): euler · Flux2Scheduler [20, 1456, 816] · CFG 5 · Negativ-Node leer · Seed notieren
**Zielmaß:** 1456×816 generieren, dann 2× auf 2912×1632 skalieren
**Dateiname:** `<motiv>.webp`

**Frontmatter:**
```yaml
cover:
    image: "<motiv>.webp"
    caption: "<Bildunterschrift auf Deutsch>"
```
````

Maße und Dateinamenskonvention stehen in [stile.md](stile.md) — sie sind Vorgabe dieses Projekts, keine Empfehlung von BFL.

## ComfyUI-Settings

Für **klein base 4B**: Sampler `euler` · `Flux2Scheduler [20, Breite, Höhe]` · `CFGGuider 5` · Negativ-Node vorhanden, aber leer. (Werte aus den offiziellen Comfy-Org-Workflow-Templates.)

**Die base-Variante ist für diesen Blog die richtige.** Die distillierte hellt Bilder auf — bei Covern, die von einer warmen Quelle in tiefem Dunkel leben, arbeitet sie gegen den Stil. Base hat den größeren Tonwertumfang und erlaubt echtes CFG. Beide 4B-Varianten stehen unter Apache 2.0.

Breite und Höhe im `Flux2Scheduler` müssen mit dem Latent übereinstimmen — sie fließen in die Sigma-Berechnung ein.

**Iterieren:** Seed festhalten und nur den Prompt ändern. So siehst du, was die Formulierung bewirkt hat, statt Prompt- und Rauschänderung zu vermischen.

## Stilgedächtnis

Die Stil-Bausteine je Reihe stehen in [stile.md](stile.md). Kommt eine Reihe dazu oder ändert sich der Look, dort ergänzen — nicht im Prompt improvisieren.

## Fertig, wenn

- Der Prompt ist durchgehend Prosa, keine Kommakette.
- Alle drei Bildebenen sind benannt und gefüllt.
- Lichtquelle, Reichweite und Wirkung auf Oberflächen stehen ausformuliert da.
- Der Stil-Baustein der Reihe steckt unverändert drin.
- `Style:`/`Mood:`-Suffix schließt ab.
- Keine Negation, keine Mengenzahl, kein Text im Bild.
- 110–170 Wörter.

## Grenzen

- **512 Token** Encoder-Limit, hart abgeschnitten (`MAX_LENGTH=512, truncation=True` im flux2-Quellcode).
- **Keine Gewichtungssyntax** — `(wort:1.2)` und `[]` haben bei Klein keine Wirkung.
- **JSON-Prompting und HEX-Farbcodes** sind nur für [pro]/[max] dokumentiert, für Klein nicht. Farben deshalb ausschreiben: `deep teal-grey`, `warm amber`.
- Klein liegt qualitativ unter [pro]. Sitzt ein Cover partout nicht, ist derselbe Prompt über die BFL-API eine Option — dann aber mit `disable_pup: true`, sonst wird er vor der Generierung umgeschrieben und der Seed nützt nichts.
