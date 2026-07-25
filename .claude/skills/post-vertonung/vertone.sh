#!/bin/bash
# Vertont Hugo-Posts über die ElevenLabs-API und legt die MP3 ins Page-Bundle.
# Siehe SKILL.md für Hintergrund, Stimme, Pausenwerte und Kosten.
set -u

# ── Einstellungen ────────────────────────────────────────────────────────────
VOICE="re2r5d74PqDzicySNW0I"        # Leon Stern — Fiction & Fantasy
MODEL="eleven_multilingual_v2"
SPEED="0.9"                          # leicht unter Normaltempo
STABILITY="0.5"
SIMILARITY="0.75"
FORMAT="mp3_44100_64"                # 64 kbps mono — für Sprache ausreichend
MAX_CHARS=10000                      # Request-Limit von multilingual_v2

PAUSE_TITEL="1.5"                    # nach dem Titel
PAUSE_VOR_H="1.0"                    # vor einer Überschrift
PAUSE_NACH_H="0.7"                   # nach einer Überschrift
PAUSE_ABSATZ="0.5"                   # nach jedem Absatz
# ─────────────────────────────────────────────────────────────────────────────

MODE=""; KATEGORIE=""; ZIELE=()
while [ $# -gt 0 ]; do
  case "$1" in
    --dry) MODE="dry"; shift ;;
    --run) MODE="run"; shift ;;
    --kategorie) KATEGORIE="$2"; shift 2 ;;
    -h|--help) sed -n '2,4p' "$0"; exit 0 ;;
    *) ZIELE+=("$1"); shift ;;
  esac
done

if [ -z "$MODE" ]; then
  echo "Modus fehlt: --dry (zeigt nur) oder --run (erzeugt Audio)" >&2
  exit 2
fi
if [ "$MODE" = "run" ] && [ -z "${ELEVENLABS_API_KEY:-}" ]; then
  echo "ELEVENLABS_API_KEY ist nicht gesetzt." >&2
  exit 2
fi

# Zielmenge bestimmen: explizite Pfade, sonst alle Posts der Kategorie ohne Vertonung.
if [ ${#ZIELE[@]} -eq 0 ]; then
  if [ -z "$KATEGORIE" ]; then
    echo "Weder Pfad noch --kategorie angegeben." >&2
    exit 2
  fi
  while IFS= read -r md; do
    bundle=$(dirname "$md")
    [ -f "$bundle/vertonung.mp3" ] || ZIELE+=("$bundle")
  done < <(grep -rl "$KATEGORIE" content/posts/*/index.md 2>/dev/null | sort)
  if [ ${#ZIELE[@]} -eq 0 ]; then
    echo "Keine Posts der Kategorie $KATEGORIE ohne vorhandene Vertonung gefunden."
    exit 0
  fi
fi

# Text für die Sprachausgabe aufbereiten.
# Markdown wird aufgelöst, Pausen werden als <break/>-Tags gesetzt: nach dem Titel,
# um Überschriften herum und am Absatzende. Bewusst KEINE Pausen innerhalb von
# Absätzen — Satzzeichen erledigt das Modell selbst, und zu viele Tags lassen die
# Stimme hetzen (dokumentierte Eigenart der API).
aufbereiten() {
  local md="$1" titel
  titel=$(awk -F'"' '/^title:/{print $2; exit}' "$md")
  [ -z "$titel" ] && titel=$(awk '/^title:/{sub(/^title:[[:space:]]*/,""); print; exit}' "$md")

  { printf '%s.<break time="%ss" />\n\n' "$titel" "$PAUSE_TITEL"
    awk 'BEGIN{n=0} /^---$/{n++; next} n>=2{print}' "$md"
  } | sed -E \
      -e 's/\*\*([^*]+)\*\*/\1/g' \
      -e 's/\*([^*]+)\*/\1/g' \
      -e 's/`([^`]+)`/\1/g' \
      -e 's/\[([^]]+)\]\([^)]+\)/\1/g' \
      -e 's/^!\[[^]]*\]\([^)]*\)[[:space:]]*$//' \
      -e 's/^>[[:space:]]?//' \
      -e "s|^#{1,6}[[:space:]]+(.*)\$|<break time=\"${PAUSE_VOR_H}s\" />\1.<break time=\"${PAUSE_NACH_H}s\" />|" \
      -e 's/[[:space:]]+$//' \
    | awk -v p="$PAUSE_ABSATZ" '
        # Absatzende = Leerzeile nach einer nichtleeren Zeile, die nicht schon
        # mit einem Break endet (Überschriften bringen ihre eigene Pause mit).
        /^$/ { if (prev != "" && prev !~ /\/>$/) printf "<break time=\"%ss\" />\n", p; print; prev=""; next }
        { print; prev=$0 }
      ' \
    | awk '
        # Zwei Pausen direkt hintereinander zu einer zusammenfassen: vor einer
        # Überschrift träfe sonst der Absatz-Break auf den Überschriften-Break.
        # Gehäufte Tags lassen die Stimme laut API-Doku hetzen — also die
        # schwächere verwerfen und nur die längere stehen lassen.
        # Leerzeilen dazwischen werden mitgepuffert, sonst greift der Vergleich nicht.
        /^<break time="[0-9.]+s" \/>$/ { if (held != "") print held; held=$0; blanks=""; next }
        /^$/ { if (held != "") { blanks = blanks "\n" } else print; next }
        {
          if (held != "") {
            if ($0 !~ /^<break/) { print held; printf "%s", blanks }
            held=""; blanks=""
          }
          print
        }
        END { if (held != "") print held }
      ' \
    | cat -s
}

gesamt=0
for bundle in "${ZIELE[@]}"; do
  bundle="${bundle%/}"
  md="$bundle/index.md"
  if [ ! -f "$md" ]; then
    echo "Übersprungen: $bundle (keine index.md)" >&2
    continue
  fi
  slug=$(basename "$bundle")
  text=$(aufbereiten "$md")
  laenge=${#text}
  gesamt=$((gesamt + laenge))

  if [ "$laenge" -gt "$MAX_CHARS" ]; then
    echo "ABBRUCH $slug: $laenge Zeichen über dem Limit von $MAX_CHARS." >&2
    echo "  Chunking ist nicht implementiert — Post teilen oder Skript erweitern." >&2
    continue
  fi

  if [ "$MODE" = "dry" ]; then
    echo "══════════════════════════════════════════════════════════════"
    echo "$slug — $laenge Zeichen, $(grep -o '<break' <<<"$text" | wc -l) Pausen"
    echo "──────────────────────────────────────────────────────────────"
    echo "$text"
  else
    printf "%-52s %6d Zeichen  " "$slug" "$laenge"
    payload=$(mktemp); trap 'rm -f "$payload"' EXIT
    jq -n --arg t "$text" --arg m "$MODEL" \
          --argjson st "$STABILITY" --argjson si "$SIMILARITY" --argjson sp "$SPEED" '{
      text: $t, model_id: $m,
      voice_settings: { stability: $st, similarity_boost: $si, style: 0.0,
                        use_speaker_boost: true, speed: $sp }
    }' > "$payload"

    code=$(curl -s -w "%{http_code}" -X POST \
      "https://api.elevenlabs.io/v1/text-to-speech/${VOICE}?output_format=${FORMAT}" \
      -H "xi-api-key: ${ELEVENLABS_API_KEY}" -H "Content-Type: application/json" \
      -d @"$payload" --output "$bundle/vertonung.mp3.neu")

    if [ "$code" = "200" ] && [ -s "$bundle/vertonung.mp3.neu" ]; then
      mv "$bundle/vertonung.mp3.neu" "$bundle/vertonung.mp3"
      echo "HTTP 200  $(du -h "$bundle/vertonung.mp3" | cut -f1)"
    else
      echo "HTTP $code  FEHLER: $(head -c 200 "$bundle/vertonung.mp3.neu" 2>/dev/null)"
      rm -f "$bundle/vertonung.mp3.neu"
    fi
    rm -f "$payload"
  fi
done

echo
printf "Gesamt: %d Zeichen  ≈  %d Credits\n" "$gesamt" "$gesamt"

# Kontostand dazu, damit die Zahl einen Bezug hat. Der Abruf ist kostenlos;
# schlägt er fehl (fehlender user_read-Scope, kein Netz), bleibt es beim Rohwert.
if [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  konto=$(curl -s --max-time 10 -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
            https://api.elevenlabs.io/v1/user/subscription 2>/dev/null)
  frei=$(jq -r 'if .character_limit then (.character_limit - .character_count) else empty end' <<<"$konto" 2>/dev/null)
  if [ -n "$frei" ]; then
    printf "Guthaben: %d Credits frei" "$frei"
    [ "$MODE" = "dry" ] && printf "  →  danach %d" "$((frei - gesamt))"
    printf "\n"
  fi
fi
