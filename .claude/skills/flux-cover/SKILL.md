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

- **Negationen im Prompt.** „ohne Menschen" macht Menschen wahrscheinlicher, weil das Modell auf das Substantiv anspringt. Frag stattdessen: Was sähe man, wenn das Ding nicht da wäre? → `deserted`, `empty`, `unmarked`. Ein separates Negativ-Feld hilft hier nicht — siehe unten.
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

**Settings** (ComfyUI, klein 9B distilled): euler · Flux2Scheduler [4, 1456, 816] · CFG 1 · Seed notieren
**LoRA-Kette:** `anatomy 2.0` → `chiaroscuro 2.5` → `detail −5.0`
**Zielmaß:** 1456×816 erzeugen, dann **Lanczos 2×** auf 2912×1632 — **kein Refine-Pass**
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

Workflow: **`hnsstrk - Blog-Cover (Flux2 Klein 9B)`** (`~/Projekte/comfyui/user/default/workflows/`). Am 26.07.2026 für genau diesen Zweck gebaut: 25 Knoten, die drei Slider vorbelegt, kein Refine-Pass, Lanczos fest am Ausgang. Öffnen, Prompt einsetzen, starten — die Werte unten sind bereits eingestellt.

Für freie Motive, alle 14 Regler oder ein Varianten-Gitter gibt es daneben den großen `hnsstrk - Flux2 Klein 9B - Text zu Bild`; dessen Bedienung steht in `Referenz Flux 2 Klein Text-to-Image Workflows` im Vault.

| | |
|---|---|
| Modell | `flux-2-klein-9b-Q8_0.gguf` (distilled) |
| Encoder | `qwen_3_8b_fp8mixed.safetensors` — **Paar-Regel:** 9B nur mit dem 8B-Encoder |
| Sampler | `euler` · `Flux2Scheduler [4, Breite, Höhe]` · `CFGGuider 1` |
| Basisgröße | 1456×816 |
| Vergrößerung | `ImageScaleBy` lanczos **2.0** → 2912×1632 |

Breite und Höhe im `Flux2Scheduler` müssen mit dem Latent übereinstimmen — sie fließen in die Sigma-Berechnung ein.

### Warum dieser Workflow keinen Refine-Pass hat

Der große Workflow kann einen zweiten Sampler-Durchgang; der Cover-Workflow hat ihn gar nicht erst. Am 25.07.2026 im direkten Vergleich entschieden: Der Refine ist gebaut, um Details *hinzuzuerfinden*, und arbeitet damit gegen einen Stil, der von Andeutung lebt. Konkret zeichnet er die Figuren wieder aus — aus schwarzen Silhouetten werden Gestalten mit Mänteln und Hüten, und das an Kleins schwächster Stelle. Auch mit `denoise 0.25` statt 0.35 blieb der Effekt.

`ImageScaleBy` mit Lanczos vergrößert dagegen nur, was schon da ist; der Pinselstrich wächst mit, statt übermalt zu werden. Nebeneffekt: ein Sampler-Durchgang statt zwei, kein `VAEEncode` auf 4,75 Megapixel, und Batch 2 läuft ohne Speichersorgen.

**Falls doch einmal der große Workflow benutzt wird:** Dort sitzt `Hochskalieren` *innerhalb* des Refine-Zweigs — der Schalter wählt zwischen dem Bild aus Durchgang 1 (unskaliert) und dem verfeinerten aus Durchgang 2. Refine aus heißt dort also **auch keine Vergrößerung**. Genau diese Falle war der Anlass, den Cover-Workflow als eigene Datei zu bauen.

**Warnung zum Speicher:** Mit aktivem Refine bei 2.0 und Batch 2 hat der OOM-Killer den Server abgeräumt — 32 GB System-RAM reichen dafür nicht. Die Messung „für Klein unkritisch" in der Setup-Notiz gilt für 1024², nicht für 4,75 Megapixel im zweiten Durchgang. Wer den Refine doch braucht: Server mit `--cache-none` starten und Batch auf 1.

### Zur Modellwahl

Der Blog fährt seit dem 25.07.2026 auf **9B**. Das ist eine bewusste Entscheidung gegen die frühere Empfehlung 4B base: Sämtliche vorhandenen LoRAs sind für 9B gebaut, und ohne die Slider trifft kein Prompt den Reihenstil. **Die Lizenzfrage bleibt davon unberührt** — 9B steht unter der FLUX Non-Commercial License, deren §2(d) und §4(a) einander bei der Nutzung der erzeugten Bilder widersprechen. Für einen nicht monetisierten Blog vertretbar; käme Werbung dazu, wäre das neu zu bewerten. 4B ist Apache 2.0 und hätte dieses Problem nicht.

**Iterieren:** Seed festhalten und nur den Prompt ändern. So siehst du, was die Formulierung bewirkt hat, statt Prompt- und Rauschänderung zu vermischen.

## Der Negativ-Prompt hängt am Modell, nicht am Prompt

Zu dieser Frage widersprechen sich die Anleitungen im Netz: Die einen schreiben „FLUX.2 unterstützt keine Negativ-Prompts", die anderen nennen Guidance-Werte, bei denen sie funktionieren. Beide haben recht — sie reden über verschiedene Varianten. **Am 26.07.2026 an der eigenen Installation nachgemessen:**

| Modell | Steps · CFG | Lauf | Negativ-Prompt |
|---|---|---|---|
| `flux-2-klein-9b-Q8_0` (distilled) | 4 · **1** | 21 s | **wird nicht gelesen** — Pixelunterschied mit und ohne Negativtext exakt `0.000` |
| `flux-2-klein-base-9b-Q8_0` (base) | 20 · **5** | 87 s | **wirkt** — Pixelunterschied `2.512`, also spürbar, aber kein Umbau des Bildes |

Der Grund ist nicht modellspezifische Zickigkeit, sondern die Rechnung dahinter: Bei `CFG 1` wird der negative Zweig gar nicht ausgewertet — das Feld kann stehenbleiben, es kostet nichts und bewirkt nichts. Erst ab `CFG > 1` fließt er ein, und distilled-Modelle sind auf `CFG 1` trainiert.

**Der Wechsel auf base ist aber kein reiner Zugewinn.** Im selben Vergleich, gleicher Prompt, gleiche Slider-Kette:

| | Anteil praktisch schwarzer Bildfläche |
|---|---|
| distilled, 4 Steps, CFG 1 | **35 %** — brauchbar, entspricht den gelungenen Covern |
| base, 20 Steps, CFG 5 | **84 %** — zu dunkel für ein Cover |
| base **ohne** Slider | **96 %** — noch dunkler, liegt also nicht an der Kette |

base nimmt die Lichtbeschreibung des Prompts erheblich wörtlicher. Die Slider greifen dort zwar (belegt: Pixelunterschied 31,5 mit gegen ohne Kette), aber ihre Werte wären für base neu zu kalibrieren — die hier dokumentierten gelten für distilled.

**Für die Cover heißt das: kein Negativ-Prompt.** Der Weg über base kostet das Vierfache an Rechenzeit (87 s statt 21 s), verlangt eine eigene Kalibrierung und liefert bei unveränderten Werten ein unbrauchbar dunkles Bild. Die eigentliche Steuerung liegt ohnehin woanders — positiv formulieren und die Slider dosieren. Wer den Negativ-Weg dennoch braucht, stellt Modell, Steps, CFG **und** Slider gemeinsam um, nicht nur eines davon.

## LoRAs — der Tonwert kommt nicht aus dem Prompt

Am 25.07.2026 im direkten Vergleich belegt (gleicher Prompt, gleicher Seed, nur die LoRA-Kette dazwischen): Der Prompt allein bringt die Bilder nicht dunkel genug. Klein 9B distilled leuchtet das ganze Gewölbe aus, wo der Reihenstil eine warme Quelle im Schwarzen verlangt. Zwei Slider schließen die Lücke:

| Slider | Wert | Wirkung |
|---|---|---|
| `klein_slider_anatomy` | **2.0** | fängt Kleins schwächste Stelle ab, wo doch eine Figur im Bild ist |
| `klein_slider_chiaroscuro` | **2.5** | Licht bleibt an der Quelle, der Rest fällt in Schatten |
| `klein_slider_detail` | **−5.0** | nimmt Schärfe heraus — aus der Ziegelstudie wird Malerei |

Kette: `UnetLoaderGGUF` → anatomy → chiaroscuro → detail → `CFGGuider`.

`detail` steht bewußt weit im Minus. Der Slot-Titel im großen Workflow nennt „3 … 8" — das ist die Civitai-Empfehlung für *mehr* Detail und damit die falsche Richtung für diesen Stil. Bei −3.0 war das Ergebnis noch zu sauber; −5.0 ist der belegte Wert der Öl-Läufe und im Cover-Workflow bereits eingestellt.

**Warum Slider und keine Stil-LoRA:** Die Fantasy-LoRAs (`80sFantasy`, `DarkGhibli`, `EtherialGothic`) brauchen ein Trigger-Wort **am Anfang des Prompts** — das verwässert die sorgfältig gebaute Bildbeschreibung. Slider wirken ohne Trigger, allein über die Stärke, und sind stufenlos dosierbar. Sie arbeiten dabei **nicht** im 0–1-Bereich: Wer bei 1.0 stehenbleibt, hält sie für wirkungslos.

### Der Slider ersetzt den Prompt nicht — er verstärkt, was der Prompt anlegt

Am 26.07.2026 gemessen, weil verbreitete LoRA-Anleitungen etwas anderes nahelegen. Vier Läufe, gleicher Seed, gleiches Modell, gleiche Kette — nur der Prompt unterschieden:

| | Anteil praktisch schwarzer Bildfläche |
|---|---|
| voller Prompt **mit** Stil-Baustein | 38 % — gemalt, warm, lesbar |
| gekürzter Prompt **ohne** Stil-Baustein | **82 %** — ein dunkles Rendering, Motiv kaum erkennbar |

`chiaroscuro 2.5` zieht den Kontrast auf, aber er erfindet keine Lichter. Nennt der Prompt keine — `visible canvas weave in the highlights`, `narrow highlights`, `a warm amber core` —, dann hat der Slider nichts zum Herausarbeiten und zieht das ganze Bild ins Schwarze. **Der Stil-Baustein ist deshalb nicht Kosmetik, sondern die Bedingung dafür, daß die Kette überhaupt brauchbar arbeitet.** Wer ihn beim Kürzen wegläßt, muß auch die Slider zurücknehmen.

**Was die Kette nicht tut:** Sie macht das Modell nicht prompt-taub. Zwei bewußt gegensätzliche Motive (nächtlicher Kanal, sonnenhelle Markthalle) blieben mit Kette klar getrennt — die helle Szene blieb hell. Die verbreitete Warnung „bei ausbleibender Prompt-Wirkung die Stärke auf 0.5–0.6 senken" stammt aus dem Umgang mit **Stil- und Konsistenz-LoRAs**; auf Slider, die auf genau eine Achse trainiert sind, läßt sie sich nicht übertragen.

**Prüfen, ob die LoRA wirklich gegriffen hat:** Eine LoRA für die falsche Modellgröße wird von ComfyUI stillschweigend übergangen — der Lauf meldet Erfolg und liefert das Bild ohne sie. Verlässlich ist nur der Vergleich zweier Läufe **bei identischem Seed**: Unterscheiden sie sich nicht, hat die LoRA nicht gewirkt. Der Shape-Fehler steht dann im Server-Log, nicht in der Oberfläche. Die vorhandenen Slider sind sämtlich für **9B** — an einem 4B-Modell tun sie nichts.

Bestand und Trigger-Wörter aller LoRAs: `Referenz LoRA-Kandidaten Flux 2 Klein` im Vault.

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
- Klein liegt qualitativ unter [pro]. Der lokale Weg ist nicht der einzige verfügbare.

## Wenn Klein nicht reicht — die anderen Wege

Für die Cover der laufenden Reihen bleibt Klein gesetzt, und das hat einen technischen Grund, keinen preislichen: **Der Reihenstil hängt an den LoRA-Slidern.** `chiaroscuro` und `detail` im Minus sind das, was aus dem Rendering eine Malerei macht — und LoRAs gibt es in keinem der Cloud-Dienste. Ein über Midjourney erzeugtes Cover träfe den Look der Serie nicht, und das sieht man auf der Übersichtsseite sofort nebeneinander.

Für alles außerhalb der Reihen — Einzelbilder, DSK, GURPS, Illustrationen im Fließtext — sind die anderen Wege oft die bessere Wahl:

| Weg | Wann |
|---|---|
| **ElevenLabs** (Seedream 5 Pro, Flux.2 Pro) | Wenn ein Bild einfach gut werden soll. Pay per use, Ergebnisse nach Einschätzung des Nutzers mindestens auf Midjourney-Niveau. Erster Griff für Einzelbilder. |
| **Midjourney** | Vorhandenes Abo, stärkste Bildsprache bei freien Motiven — aber am wenigsten steuerbar und ohne Seed-Treue über Serien hinweg. Siehe `Midjourney` im Vault. |
| **BFL-API direkt** ([pro]/[max]) | Wenn derselbe Prompt gebraucht wird, den Klein nicht hinbekommt. Dann `disable_pup: true` setzen, sonst schreibt das Upsampling ihn vor der Generierung um und der Seed nützt nichts. Abrechnung pro Megapixel. |
| **Klein lokal** | Reihen-Cover, Serien mit Stilbindung, Iteration bei festem Seed. Kostenlos und beliebig oft wiederholbar. |

Die Prompt-Regeln dieses Skills gelten **nur für Klein**. [pro], [max] und Seedream haben Prompt-Upsampling — dort funktionieren Stichwortketten, JSON-Prompting und HEX-Farbcodes, die hier ausdrücklich ausgeschlossen sind. Ein Klein-Prompt läuft dort zwar durch, nutzt aber deren Stärken nicht.
