---
name: post-vertonung
description: |
  Vertont Hugo-Blogposts als Audiofassung über die ElevenLabs-API und legt die
  MP3 ins Page-Bundle, wo das Theme sie automatisch als Player einbindet.
  Bereitet den Text vorher auf: Markdown auflösen, Sprechpausen nach Titel,
  Überschriften und Absätzen setzen, leicht verlangsamte Sprechgeschwindigkeit.
  TRIGGER when: user wants a post read aloud, mentions "vertonen", "Vertonung",
  "Audiofassung", "vorlesen lassen", "Hörfassung", "Audio für den Post",
  or wants an existing Vertonung regenerated.
  DO NOT TRIGGER when: user wants a cover image (use flux-cover), the post text
  itself (use edrics-notizen or helbrechts-chronik), or the summary field
  (use post-summary).
allowed-tools: Read, Bash, Glob, Grep
---

# post-vertonung — Skill

Erzeugt aus einem Post unter `content/posts/` eine gesprochene Fassung und legt sie als `vertonung.mp3` ins selbe Bundle. Das Theme-Partial `article-audio.html` findet sie dort ohne weitere Konfiguration — kein Frontmatter nötig.

## Aufruf

```bash
# Trockenlauf: zeigt den aufbereiteten Text samt Pausen, kostet nichts
.claude/skills/post-vertonung/vertone.sh --dry

# Einzelnen Post vertonen
.claude/skills/post-vertonung/vertone.sh --run content/posts/2026-07-23-Acht_Ratten_und_kein_Zeichen

# Alle Posts einer Kategorie, die noch keine Vertonung haben
.claude/skills/post-vertonung/vertone.sh --run --kategorie "Edrics Notizen"
```

**Immer erst `--dry`.** Der Trockenlauf zeigt, was tatsächlich gesendet würde — Fehler in der Aufbereitung fallen dort auf, bevor sie Geld kosten.

## Stimme und Einstellungen

| | |
|---|---|
| Stimme | **Leon Stern — Fiction & Fantasy** (`re2r5d74PqDzicySNW0I`) |
| Modell | `eleven_multilingual_v2` |
| Geschwindigkeit | **0.9** — etwas unter Normaltempo, gibt der Erzählung Ruhe |
| Stabilität | 0.5 · Similarity 0.75 · Speaker Boost an |
| Ausgabe | `mp3_44100_64`, mono |

**`language_code` bleibt bewußt ungesetzt.** Sonst liest die Stimme englische Eigennamen wie „Waterdeep" nach deutschen Regeln. Ohne den Parameter erkennt das Modell die Sprache selbst und kommt mit gemischtem Text besser zurecht.

**64 kbps statt 128:** Für gesprochenen Text ist das nicht unterscheidbar, halbiert aber die Dateigröße im Repo. Die API liefert direkt in dieser Bitrate — kein Umkodieren nötig.

## Pausen

Ohne Pausen läuft die Stimme durch Überschriften hindurch, als wären sie Teil des Satzes. Der offizielle Weg dagegen ist `<break time="…s" />`; die Modelle verstehen das Tag, es ist keine eingefügte Stille.

| Stelle | Pause |
|---|---|
| nach dem Titel | 1.5 s |
| vor einer Überschrift | 1.0 s |
| nach einer Überschrift | 0.7 s |
| nach jedem Absatz | 0.5 s |

**Sparsam bleiben.** ElevenLabs warnt ausdrücklich: zu viele Break-Tags im selben Text können dazu führen, daß die Stimme zu hetzen beginnt oder Rauschen und Artefakte auftreten. Deshalb gibt es keine Pausen innerhalb von Absätzen — Kommas und Punkte erledigt das Modell selbst. Maximal 3 Sekunden pro Tag sind zulässig.

Wer die Werte ändert: in `vertone.sh` stehen sie oben als Variablen, nicht im Code verstreut.

## Verbrauch — in Credits rechnen, nicht in Dollar

Der Plan ist eine Pauschale, kein Pay-per-use. Die Frage ist also nie „was kostet das", sondern **wieviel vom Monatskontingent geht drauf**.

| | |
|---|---|
| Monatskontingent (Starter) | **30.000 Credits** |
| Ansparung | unbenutzte laufen bis zu zwei Monate mit, Deckel bei 90.000 |
| Umrechnung bei `eleven_multilingual_v2` | **1 Zeichen ≈ 1 Credit** |
| Ein Post mittlerer Länge | rund 4.000–6.000 Credits |

Am 25.07.2026 gemessen: 4.245 gesendete Zeichen ergaben **4.121 Credits** Zuwachs. Die Break-Tags zählen also **nicht voll mit** — Pausen sind günstiger, als ihre Zeichenzahl vermuten ließe.

Trocken- wie Echtlauf geben am Ende die Credit-Zahl aus und dazu das verbleibende Guthaben; im Trockenlauf zusätzlich den Stand, der nach dem Lauf übrig bliebe. Der Abruf ist kostenlos.

## Grenzen

- **10.000 Zeichen pro Request** bei `eleven_multilingual_v2`. Längere Posts bräuchten Chunking an Satzgrenzen mit `previous_text`/`next_text` — das kann das Skript derzeit **nicht** und bricht mit einer Meldung ab, statt einen abgeschnittenen Text zu vertonen.
- Kein Vorlesen von Bildunterschriften, Tabellen oder Codeblöcken — die Aufbereitung entfernt Markdown, aber eine Tabelle ergibt gesprochen ohnehin wenig Sinn.
- `ELEVENLABS_API_KEY` muß in der Umgebung stehen.

## Nach der Vertonung

Die Datei liegt im Bundle und ist damit automatisch live, sobald deployt wird. Prüfen lohnt trotzdem — vor allem die Eigennamen der Kampagne. Sitzt eine Aussprache dauerhaft nicht, ist ein Pronunciation Dictionary mit Alias-Regeln der Weg (Phonem-Regeln werden von `multilingual_v2` stillschweigend ignoriert).
