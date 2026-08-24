---
name: flux-cover
description: |
  Erzeugt das Cover eines Hugo-Blogposts — als fertigen Bildprompt und, über
  OpenRouter, auch als fertige Bilddatei. Drei Wege: FLUX.2 [klein] lokal in
  ComfyUI (nur Ganymed), FLUX.2 [pro]/[max] über die OpenRouter-Bild-API
  (überall, kostet Geld), Midjourney oder Seedream 5 Pro von Hand.
  Hält den Reihenstil über den Stil-Baustein und ein Referenzbild zusammen.
  TRIGGER when: user wants a cover/title image prompt for a post, mentions "Cover",
  "Titelbild", "Bildprompt", "Prompt für das Bild", "Flux", "Klein", "ComfyUI",
  "OpenRouter", "Midjourney", "Seedream", "ElevenLabs" in the context of images,
  or asks what to feed into the image generator for a blog post.
  DO NOT TRIGGER when: user wants the post text itself (use edrics-notizen or
  helbrechts-chronik), only the summary field (use post-summary), or works on
  Hugo templates and theme code.
allowed-tools: Read, Glob, Grep, Bash
---

# flux-cover — Skill

Baut aus einem Post unter `content/posts/` einen Bildprompt fürs Cover — und erzeugt auf zwei Wegen auch das Bild selbst.

**Der Prompt hängt davon ab, wo gearbeitet wird.** FLUX.2 [klein] läuft lokal in ComfyUI, und ComfyUI gibt es nur auf **Ganymed**. Überall sonst führt der Weg über die Bild-API von OpenRouter zu FLUX.2 [pro] oder [max] — automatisiert, aber kostenpflichtig. Midjourney und Seedream 5 Pro bleiben Handarbeit in fremden Oberflächen. Der Motivteil bleibt in allen Fällen derselbe; was sich ändert, ist der Dialekt und der Weg, auf dem der Reihenstil gehalten wird.

**Drei Wege, zwei davon fertig bis zur Datei:**

| Weg | Ausgabe | Kosten |
|---|---|---|
| ComfyUI lokal (nur Ganymed) | Bilddatei | keine |
| OpenRouter, `scripts/cover.py` | Bilddatei | rund 0,03 USD ([pro]) bzw. 0,07 USD ([max]) je Bild |
| Midjourney · Seedream 5 Pro | nur Prompt, Nutzer rendert selbst | Abo bzw. ElevenLabs-Guthaben |

**Ein Lauf über OpenRouter kostet Geld. Nie ungefragt starten** — Prompt und geschätzte Kosten vorlegen, dann entscheidet der Nutzer. `--trocken` zeigt den Request, ohne zu senden.

## Warum Klein anders geprompted wird als Midjourney oder Flux [pro]

Klein hat **kein Prompt-Upsampling**. [pro] und [max] schicken deinen Prompt vorher durch ein Sprachmodell, das ihn ausformuliert — Klein nicht. Sein Textencoder (Qwen3) bekommt den Prompt sogar ohne System-Message: was dasteht, ist alles, was das Modell sieht. Ein Prompt, der bei Midjourney als Stichwortkette funktioniert, liefert hier ein dünnes Bild, weil niemand die Lücken füllt.

Deshalb gilt für jeden Prompt aus diesem Skill: **ausformulierte Prosa**. BFL selbst formuliert es als *„describe scenes like a novelist, not a search engine"*.

Zweitwichtigster Hebel ist das **Licht** — laut BFL der Einzelfaktor mit dem größten Einfluß auf die Bildqualität bei Klein. Beschreibe Quelle, Härte, Richtung, Farbtemperatur und was das Licht mit den Oberflächen macht. Bei den Covern dieses Blogs ist Licht ohnehin das tragende Motiv: eine warme Quelle im Dunkeln.

## Ablauf

0. **Ziel bestimmen.** Läuft ComfyUI?

   ```bash
   curl -s -m 2 -o /dev/null -w "%{http_code}" -H "comfy-user: default" \
     http://127.0.0.1:8188/system_stats
   ```

   `200` → Ganymed, der lokale Klein-Weg ist die Hauptfassung. Alles andere (`000`, Zeitüberschreitung) → OpenRouter ist der Weg zur fertigen Datei, die Midjourney- und Seedream-Fassungen kommen als Alternative dazu. Der Nutzer kann das überstimmen: Nennt er ein Ziel ausdrücklich („für Midjourney", „über OpenRouter"), gilt seine Angabe ohne Prüfung.

1. **Post lesen.** Titel, `summary`, `categories` und Fließtext. Ist kein Pfad genannt, den jüngsten Post nehmen (`ls -t content/posts/`).
2. **Reihe bestimmen** über `categories:` im Frontmatter, dann den passenden Stil-Baustein aus [stile.md](stile.md) holen. Steht die Reihe dort nicht, mit dem Nutzer einen Stil festlegen statt einen zu erfinden — ein geratener Stil bricht die Serie, und das sieht man auf der Übersichtsseite sofort.
3. **Motiv wählen:** ein **Ort oder eine Szene**, keine Handlung mit Gesichtern. Die Cover dieses Blogs erzählen durchgehend über Schauplätze; Figuren sind kleine dunkle Silhouetten, die den Maßstab setzen, nicht Porträts. Das gilt für jedes Ziel — bei Klein kommt hinzu, dass er Menschen unzuverlässig zeichnet, aber die Regel folgt der Reihe, nicht dem Modell.
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

Die ersten beiden Punkte gelten überall, die letzten drei sind Klein-Eigenheiten.

- **Negationen im Prompt.** „ohne Menschen" macht Menschen wahrscheinlicher, weil das Modell auf das Substantiv anspringt. Frag stattdessen: Was sähe man, wenn das Ding nicht da wäre? → `deserted`, `empty`, `unmarked`. Bei Midjourney gibt es dafür `--no`; Klein hat kein brauchbares Gegenstück (siehe unten).
- **Stimmungsworte statt Sichtbarem.** „düster" ist keine Bildinformation. Was macht es düster — welcher Anteil des Bildes liegt im Schatten, wo ist die einzige Lichtquelle, wie weit reicht sie?
- **Keyword-Ketten** mit Kommas — bei Klein. Siehe oben: es gibt niemanden, der sie ausformuliert. Midjourney und die [pro]-Modelle kommen damit zurecht; der Prosa-Prompt schadet dort aber auch nicht, deshalb wird er einmal gebaut und überall verwendet.
- **Text im Bild.** Die Model Card von klein 4B sagt selbst, gerenderter Text könne *„inaccurate or subject to distortion"* sein; in einem Test von wiro.ai kippte bei 6 von 10 Prompts die Schreibung. Die Cover dieses Blogs tragen ohnehin keinen Text — dabei bleiben.
- **Zahlen als Mengenangabe.** „acht tote Ratten" wird nicht acht. `a heap of dead rats` liefert verläßlich ein stimmiges Bild.

## Ausgabeformat

Immer zuerst die Fassung fürs erkannte Ziel, darunter die Alternativen in Kurzform. Dateiname und Frontmatter stehen nur einmal am Ende — sie gelten unabhängig vom Generator.

**Auf Ganymed (ComfyUI antwortet):**

````markdown
## Prompt — [Titel des Posts]

```
[der Prompt als Fließtext]
```

**Settings** (ComfyUI, klein 9B distilled): euler · Flux2Scheduler [4, 1456, 816] · CFG 1 · Seed notieren
**LoRA-Kette:** `anatomy 2.0` → `chiaroscuro 2.5` → `detail −5.0`
**Zielmaß:** 1456×816 erzeugen, dann **Lanczos 2×** auf 2912×1632 — **kein Refine-Pass**
**Workflow:** `hnsstrk - Blog-Cover (Flux2 Klein 9B)`
````

**Über OpenRouter** (der Weg zur fertigen Datei außerhalb von Ganymed):

````markdown
## Prompt — [Titel des Posts]

```
[Motivtext + Stil-Baustein + Hex-Palette der Reihe]
```

**Aufruf:**
```bash
.claude/skills/flux-cover/scripts/cover.py \
  --modell pro \
  --prompt "<der Prompt>" \
  --referenz "<URL aus stile.md>" \
  --ziel content/posts/<post-ordner>/<motiv>.webp
```
**Kosten:** rund 0,03 USD ([pro]) bzw. 0,07 USD ([max]) — vor dem Lauf bestätigen lassen.
````

**Auf jedem anderen Rechner** — derselbe Motivtext, dreimal anders verpackt:

````markdown
## Prompt — [Titel des Posts]

### Midjourney
```
[Motivtext + Stil-Baustein] --ar 16:9 --sref [URL aus stile.md] --sw 100 --style raw
```

### Seedream 5 Pro (ElevenLabs)
```
[Motivtext + Stil-Baustein]
```
Referenzbild: [URL aus stile.md] · Seitenverhältnis 16:9

### FLUX.2 [pro] (ElevenLabs)
```
[Motivtext + Stil-Baustein + Hex-Palette der Reihe]
```
Referenzbild: [URL aus stile.md] · Seitenverhältnis 16:9
````

**Immer am Ende, unabhängig vom Weg:**

````markdown
**Dateiname:** `<motiv>.webp`

**Frontmatter:**
```yaml
cover:
    image: "<motiv>.webp"
    caption: "<Bildunterschrift auf Deutsch>"
```
````

Maße und Dateinamenskonvention stehen in [stile.md](stile.md) — sie sind Vorgabe dieses Projekts, keine Empfehlung eines Anbieters. Das Zielmaß 2912×1632 gilt auch für die Cloud-Wege; liefert der Dienst kleiner, hinterher hochskalieren.

## Reihentreue ohne LoRAs — das Referenzbild

Auf Ganymed tragen die LoRA-Slider den Reihenstil. Kein Cloud-Dienst kennt LoRAs, und ein Cover, das den Look der Serie verfehlt, fällt auf der Übersichtsseite sofort auf. **Der Ersatz ist ein Referenzbild:** ein vorhandenes Cover derselben Reihe, das der Dienst als Stilvorlage bekommt.

Die Cover liegen öffentlich unter berechenbaren URLs, sind also direkt verlinkbar — geprüft am 26.07.2026 (`HTTP 200`, `image/webp`, rund 1 MB, 2912×1632). Midjourney akzeptiert `.webp` und empfiehlt Referenzen ab 1024 px; unsere liegen deutlich darüber.

Die URL je Reihe steht in [stile.md](stile.md). Nie ein Cover einer *anderen* Reihe als Referenz nehmen, und bei „Greifenfurter Adel" keins von 2023 oder früher — das holt den fotorealistischen Bruch zurück.

## Cover über OpenRouter — `scripts/cover.py`

Der einzige Weg außerhalb von Ganymed, der ohne Handarbeit in einer fremden Oberfläche zur fertigen Datei führt. Das Skript ruft die Bild-API von OpenRouter auf, holt das Bild, bringt es auf 2912×1632 und legt es als WebP ab.

```bash
.claude/skills/flux-cover/scripts/cover.py \
  --modell pro \
  --prompt "<Motivtext + Stil-Baustein + Hex-Palette>" \
  --referenz "https://www.online-resources.de/posts/.../kanalratten.webp" \
  --ziel content/posts/2026-08-…/hafenviertel.webp
```

Ausgabe ist der Pfad der fertigen Datei auf `stdout`; Modell, Laufzeit, Seed und die tatsächlichen Kosten stehen auf `stderr`.

Weitere Schalter: `--seed`, `--ar` (Vorgabe `16:9`), `--zielmass keine` (liefert das unskalierte PNG), `--steps`/`--guidance` (an Black Forest Labs durchgereicht), `--liste` (Modelle und Preise), `--guthaben` (Kontostand), `--trocken` (zeigt den Request und sendet nichts — kostet nichts).

**Der Schlüssel** liegt in `~/.config/openrouter/key` (Rechte 600) oder in `$OPENROUTER_API_KEY`. Das Skript liest ihn zur Laufzeit und gibt ihn nirgends aus. **Nie in eine Datei des Repositories schreiben, nie in eine Beispiel-Kommandozeile, nie in eine Fehlermeldung.**

### Welches Modell

| Modell | Preis je Megapixel Ausgabe | Wofür |
|---|---|---|
| `--modell pro` | 0,03 USD | **Standardwahl.** Reicht für Reihen-Cover. |
| `--modell max` | 0,07 USD | Wenn [pro] das Motiv zweimal verfehlt hat, oder bei besonders verwickelter Szene. |
| `--modell flex` | 0,06 USD aus **plus** 0,06 USD je Megapixel Referenzbild | Stark bei Text und Typografie — die Cover tragen keinen Text. **Kein Grund, ihn zu nehmen.** |
| `--modell klein4b` | 0,014 USD | Dasselbe Modell wie lokal, aber **ohne** die LoRA-Slider, die den Reihenstil erst herstellen. Nur als Notbehelf. |

Bei rund einem Megapixel Ausgabe kostet ein Bild also ungefähr 0,03 USD mit [pro] und 0,07 USD mit [max]. Ein Nachlauf mit anderem Seed kostet dasselbe noch einmal.

### Was der OpenRouter-Weg kann

- **Referenzbilder:** bis zu **acht** bei [pro], [max] und [flex], vier bei [klein-4b]. Damit ist der Reihenstil so gut gebunden wie über Midjourneys `--sref` — sogar besser, weil mehrere Cover derselben Reihe gleichzeitig als Vorlage dienen können.
- **Seitenverhältnis** über `aspect_ratio`; `16:9` ist dabei.
- **Seed** wird angenommen. Die Spezifikation sagt dazu ausdrücklich: *„Determinism is not guaranteed for all providers."*
- **Steps, Guidance und Safety Tolerance** gehen als Durchreichparameter an Black Forest Labs.

### Was er nicht kann

- **Keine Auflösungssteuerung.** Die API kennt zwar `resolution` (`512`/`1K`/`2K`/`4K`) und `size` (`"2048x1152"`), aber **die FLUX-Modelle melden beides nicht als unterstützt** — nur `aspect_ratio`, `output_format`, `n`, `seed` und `input_references`. Das Zielmaß 2912×1632 kommt deshalb nicht aus dem Modell, sondern aus dem Hochskalieren mit Lanczos, genau wie im lokalen Workflow.
- **Kein WebP als Ausgabeformat.** FLUX liefert nur `png` oder `jpeg`; das Skript fordert PNG an und wandelt selbst um.
- **Nur ein Bild je Aufruf** (`n` ist auf 1 begrenzt). Kein Varianten-Gitter wie in ComfyUI.
- **Kein Zugriff auf das Prompt-Upsampling.** [pro] und [max] schicken den Prompt durch ein Sprachmodell, bevor sie rendern. Der Schalter, der das abstellt, gehört **nicht** zu den drei durchgereichten Parametern — über OpenRouter ist er nicht erreichbar. Serientreue kommt hier also allein aus dem Referenzbild, nicht aus dem Seed.
- **Keine LoRAs.** Die drei Slider, die den Tonwert der Reihe herstellen, gibt es nur lokal.

### Fehler und Guthaben

| Code | Bedeutung |
|---|---|
| 400 | Parameter paßt nicht zum Modell — meist `resolution`, `size` oder `quality` bei FLUX |
| 402 | Guthaben erschöpft |
| 413 | Request zu groß — Referenzbild als URL statt als lokale Datei übergeben |
| 429 | Rate Limit |
| 502 · 524 · 529 | Anbieter ausgefallen, zu langsam oder überlastet |

Abgerechnet wird nach dem Alles-oder-nichts-Prinzip: Ein Lauf, der nicht fertig wird, kostet nichts. Kontostand mit `--guthaben` (der Abruf selbst ist kostenlos).

**Referenzbild als URL, nicht als Datei.** Die Cover liegen öffentlich; eine URL ist ein paar Dutzend Zeichen. Dieselbe Datei lokal eingebettet sind rund 1,5 Millionen Zeichen im Request — das läuft in ein 413. Das Skript kann beides, die URL ist der richtige Weg.

### Was hier geprüft ist und was nicht

Alles am **24.08.2026** an der laufenden API erhoben, ohne einen einzigen Bildlauf:

| Belegt | Quelle |
|---|---|
| Endpunkt `POST /api/v1/images`, vollständiges Anfrage- und Antwortschema | `https://openrouter.ai/openapi.json`, Pfad `/images` |
| Modell-IDs `black-forest-labs/flux.2-pro` und `…/flux.2-max` | `GET /api/v1/images/models` |
| Unterstützte Parameter je Modell, Höchstzahl Referenzbilder, Durchreichparameter | `GET /api/v1/images/models/black-forest-labs/flux.2-pro/endpoints` |
| Preise 0,03 / 0,07 / 0,06 / 0,014 USD je Megapixel | derselbe Endpunkt, Feld `pricing` |
| Rückgabe als base64 in `data[0].b64_json`, **keine URL, keine Ablauffrist** | Antwortschema `ImageGenerationResponse` |
| Guthabenabfrage `GET /api/v1/credits` | eigener Abruf, HTTP 200 |
| Der Skalierschritt liefert exakt 2912×1632 WebP | eigener Lauf gegen ein Testbild 1408×800 |

**Ungeprüfte Annahme bleibt:**

- **Welche Pixelmaße FLUX bei `aspect_ratio: "16:9"` tatsächlich liefert.** Black Forest Labs nennt 64×64 als Minimum, 4 Megapixel als Maximum, Vielfache von 16 und „recommended up to 2MP". Die Kostenrechnung oben unterstellt rund ein Megapixel. Steht die erste Datei, ist die Frage mit `magick identify` beantwortet — und die Kostenangabe hier entsprechend zu berichtigen.
- **Ob ein WebP als Referenzbild angenommen wird.** Die Modelle melden `image` als Eingabeformat, ohne die Codecs aufzuzählen. Wird die URL abgewiesen, hilft `--referenz <lokale PNG-Datei>`.
- **Ob der Seed bei [pro] und [max] trägt** — siehe Prompt-Upsampling oben.
- **Der Bildlauf selbst ist noch nie gelaufen.** Erprobt sind am 24.08.2026 nur die kostenlosen Wege: `--liste`, `--trocken` (baut den Request korrekt auf) und `--guthaben` (HTTP 200, Schlüssel wird angenommen). Damit stehen Authentifizierung, Endpunkt und Anfrageaufbau; offen bleibt alles, was erst die Antwort zeigt — Pixelmaße, Referenzbild-Annahme, Seed-Wirkung.

## Der gleiche Prompt in fünf Dialekten

Der Motivteil — Hauptmotiv, Raumschichtung, Licht — ist überall identisch. Was sich unterscheidet:

| | Klein (lokal) | OpenRouter [pro]/[max] | Midjourney | FLUX.2 [pro] (ElevenLabs) | Seedream 5 Pro |
|---|---|---|---|---|---|
| Prosa nötig | **ja**, kein Upsampling | nein, hat Upsampling | nein, verträgt Ketten | nein, hat Upsampling | nein |
| Stil-Baustein | unverändert anhängen | anhängen plus `--referenz` | anhängen **plus** `--sref` | anhängen plus Referenzbild | anhängen plus Referenzbild |
| Seitenverhältnis | über Breite/Höhe | `--ar 16:9` | `--ar 16:9` | Parameter der API | Parameter der Oberfläche |
| Auflösung | frei wählbar | **nicht steuerbar**, hinterher skalieren | fest je Modell | Parameter der API | Parameter der Oberfläche |
| Negativ-Prompt | nein (siehe unten) | nein | `--no <begriff>` | nein dokumentiert | nein dokumentiert |
| HEX-Farben | **nein** | ja | nein | ja, dokumentiert | ungeprüft |
| Wiederholbarkeit | Seed exakt | Seed, ohne Zusicherung | `--seed`, nur ungefähr | Seed, aber Upsampling stört | Referenzbild |
| Bild kommt fertig | ja | **ja** | nein, Handarbeit | nein, Handarbeit | nein, Handarbeit |

### Midjourney

Stil-Baustein in den Prompt, Referenzbild als `--sref`, Rest über Parameter:

```
<Motivteil als Fließtext, Stil-Baustein am Ende>
--ar 16:9 --sref <URL aus stile.md> --sw 100 --style raw
```

`--sw` steuert, wie stark die Vorlage durchschlägt (0–1000, Standard 100). Trifft der Look nicht, zuerst `--sw` erhöhen — nicht den Stil-Baustein aufblähen. `--style raw` nimmt Midjourneys eigene Verschönerung heraus, die sonst gegen den ruhigen Reihenlook arbeitet. Für Motive ohne Figuren zusätzlich `--no people`; das ist hier zulässig, anders als bei Klein.

### FLUX.2 [pro] über ElevenLabs

Prosa funktioniert, ist aber nicht nötig — [pro] schickt den Prompt durch ein Sprachmodell, das ihn ausformuliert. Zwei Folgen daraus:

- **HEX-Farben sind dokumentiert und wirken.** Die Palette je Reihe steht als Hex-Zeile in [stile.md](stile.md) — bei [pro] gehört sie in den Prompt, bei Klein nicht.
- **Wer Wiederholbarkeit braucht, schaltet das Upsampling ab** (`disable_pup: true` in der API von Black Forest Labs). Sonst wird der Prompt vor jeder Generierung neu umgeschrieben und der Seed nützt nichts. Über die Oberfläche von ElevenLabs ist der Schalter nicht erreichbar, **über OpenRouter ebensowenig** (durchgereicht werden nur `steps`, `guidance`, `safety_tolerance`) — auf beiden Wegen führt nur das Referenzbild zu Serientreue.

### Seedream 5 Pro über ElevenLabs

Nach Einschätzung des Nutzers mindestens auf Midjourney-Niveau, seit Anfang 2026 besonders stark bei Komposition und mehrfigurigen Szenen. Steuerung läuft über Referenzbilder, nicht über Parameter: klarer Prompt aus Motiv, Aufbau und Stil, dazu die Referenz aus [stile.md](stile.md).

**Nicht verwechseln:** *Seedream* erzeugt Bilder, *Seedance* Videos — beide gibt es bei ElevenLabs. Und Seedream 5 Pro ist in den USA gesperrt; von Deutschland aus nutzbar.

### Wann welcher Weg

| Weg | Wann |
|---|---|
| **Klein lokal** (nur Ganymed) | Reihen-Cover, wenn die Maschine erreichbar ist. Kostenlos, beliebig oft wiederholbar, Seed-treu. |
| **OpenRouter [pro]** | Erster Griff außerhalb von Ganymed. Der einzige Weg, der ohne fremde Oberfläche zur fertigen Datei führt, und mit bis zu acht Referenzbildern die stärkste Stilbindung. Kostet je Bild rund 0,03 USD. |
| **OpenRouter [max]** | Wenn [pro] das Motiv zweimal verfehlt hat. Gut das Doppelte an Kosten. |
| **Midjourney** | Wenn der Nutzer ohnehin dort arbeitet oder `--sref` mit abgestufter Stärke (`--sw`) braucht. |
| **Seedream 5 Pro** | Wenn das Motiv Komposition oder mehrere Figuren verlangt. |
| **FLUX.2 [pro] über ElevenLabs** | Nur, wenn kein OpenRouter-Guthaben da ist — es ist derselbe Modellzugang, nur von Hand. |


---

## Nur auf Ganymed: der lokale Klein-Weg

Alles ab hier setzt ComfyUI voraus und gilt für kein anderes Ziel.

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

> [!warning] Diese Werte gehören zum Baustein vom 25.07.2026
> Für den feineren Baustein, den „Edrics Notizen" seit 08/2026 verlangt, gilt **`detail +1.0` und 8 Steps** statt −5.0 und 4. Der Slider steht dann im Positiven, weil das Ziel ausmodellierte Formen sind und nicht mehr die Andeutung. Welcher Baustein für welche Reihe gilt, steht in [stile.md](stile.md) — dort auch die Begründung.

### Referenzbilder gehen auch lokal

`stile.md` führt Referenzbilder als Ersatz für die LoRAs *in der Cloud*. Das ist unvollständig: **ComfyUI kann sie ebenfalls**, und für wiederkehrende Schauplätze ist das der einzige verlässliche Weg, denselben Raum zweimal zu treffen. Am 24.08.2026 erprobt — die Schmiede aus `esse.webp` kam mit Ziegelwand, Rauchhaube und Steinboden wieder.

Der Cover-Workflow hat den Zweig nicht; er wird an den Graphen angehängt, je Bild vier Knoten:

```
LoadImage → ImageScaleToTotalPixels (megapixels 1.0, resolution_steps 16) → VAEEncode → ReferenceLatent
```

`ReferenceLatent` nimmt `conditioning` und `latent`; mehrere Bilder werden verkettet (jedes bekommt das Conditioning des vorherigen), das letzte geht als `positive` in den `CFGGuider`. Die Datei muss in `~/Projekte/comfyui/input/` liegen. Vorbild und Feinheiten: `~/.claude/skills/comfyui-bild/scripts/render.py`, Funktion `referenz_kette` — `resolution_steps` ist dort Pflicht, sonst weist ComfyUI den Auftrag ab.

**Eine Referenz, nicht zwei.** Mit zwei Vorlagen malte Klein am 24.08. Bildinhalte doppelt — aus einem Dolch wurden zwei gekreuzte Klingen. Mit einer war das Ergebnis sauber.

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

Für jedes Ziel:

- Der Prompt ist durchgehend Prosa, keine Kommakette.
- Alle drei Bildebenen sind benannt und gefüllt.
- Lichtquelle, Reichweite und Wirkung auf Oberflächen stehen ausformuliert da.
- Der Stil-Baustein der Reihe steckt unverändert drin.
- `Style:`/`Mood:`-Suffix schließt ab.
- Keine Mengenzahl, kein Text im Bild.
- 110–170 Wörter.
- Dateiname und Frontmatter-Block stehen dabei.

Zusätzlich außerhalb von Ganymed:

- Die Referenzbild-URL der Reihe ist genannt und stammt aus [stile.md](stile.md).
- Bei Midjourney hängen `--ar 16:9 --sref … --sw 100 --style raw` am Prompt.
- Beim OpenRouter-Weg stehen der vollständige Aufruf und die geschätzten Kosten da — und der Nutzer hat zugestimmt, bevor gerendert wurde.

## Grenzen

- **512 Token** Encoder-Limit bei Klein, hart abgeschnitten (`MAX_LENGTH=512, truncation=True` im flux2-Quellcode).
- **Keine Gewichtungssyntax** — `(wort:1.2)` und `[]` haben bei Klein keine Wirkung. Midjourney kennt `::` als Gewichtung, das ist ein anderer Mechanismus.
- **JSON-Prompting und HEX-Farbcodes** sind für [pro]/[max] dokumentiert, für Klein nicht. In der Klein-Fassung Farben deshalb ausschreiben: `deep teal-grey`, `warm amber`.
- **Für Midjourney und ElevenLabs prüft der Skill nicht, ob der Dienst erreichbar ist** — er liefert nur den Prompt. Ob das ElevenLabs-Guthaben reicht oder Midjourney gerade läuft, steht auf einem anderen Blatt. Beim OpenRouter-Weg beantwortet `cover.py --guthaben` wenigstens die Guthabenfrage.
- Klein liegt qualitativ unter [pro]; dafür ist er kostenlos, wiederholbar und der einzige Weg mit LoRA-Steuerung.
- **`cover.py` ist noch nie scharf gelaufen.** Gebaut und in Trockenläufen geprüft, aber ohne echten Bildlauf — der kostet Geld und ist die Entscheidung des Nutzers.
