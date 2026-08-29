#!/usr/bin/env python
"""Erzeugt ein Blog-Cover über die Bild-API von OpenRouter.

Nimmt dem Cloud-Weg die drei Handgriffe ab, die ihn bisher zur Handarbeit
gemacht haben:
  1. den Aufruf von POST /api/v1/images mit dem je Modell zulässigen Parametersatz
  2. das Referenzbild — Stilbindung der Reihe, ohne die kein Cover zur Serie paßt
  3. Skalierung auf das Projekt-Zielmaß 2912x1632 und Ablage als WebP

Der Schlüssel wird zur Laufzeit gelesen ($OPENROUTER_API_KEY oder
~/.config/openrouter/key) und niemals ausgegeben.

Aufruf:
    cover.py --prompt "..." --ziel content/posts/<post>/<motiv>.webp \\
             --referenz https://online-resources.de/.../kanalratten.webp
    cover.py --trocken --prompt "..." --ziel /tmp/x.webp   # zeigt nur den Request
    cover.py --guthaben
    cover.py --liste

ACHTUNG: Jeder Lauf ohne --trocken kostet Geld. Den Satz je Megapixel zeigt
--liste; er wird dafür bei OpenRouter abgefragt, nicht aus dieser Datei gelesen.
"""
import argparse
import base64
import datetime
import json
import mimetypes
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

API = "https://openrouter.ai/api/v1"
SCHLUESSEL_DATEI = os.path.expanduser("~/.config/openrouter/key")

# Zielmaß und Dateiformat sind Projektvorgabe (stile.md), keine Anbieter-Empfehlung.
ZIELMASS = "2912x1632"

# Grenzen am 24.08.2026 aus
# GET /api/v1/images/models/black-forest-labs/<modell>/endpoints erhoben; 'refs' ist
# die dort gemeldete Höchstzahl an Referenzbildern.
#
# 'usd_pro_mp' ist der Satz je Megapixel Ausgabe und seit dem 29.08.2026 nur noch der
# NOTWERT: Gezeigt wird, was satz_je_mp() zur Laufzeit von OpenRouter holt. Eine
# abgeschriebene Zahl veraltet unbemerkt — genau daran wurden 0,03 USD als Preis je Bild
# geführt, während für ein Bild 0,105 USD abgerechnet wurden.
MODELLE = {
    "pro": {
        "id": "black-forest-labs/flux.2-pro", "usd_pro_mp": 0.03, "refs": 8,
        "beschreibung": "Standardwahl. Gute Prompttreue, stabiles Licht, Mehrfach-Referenz.",
    },
    "max": {
        "id": "black-forest-labs/flux.2-max", "usd_pro_mp": 0.07, "refs": 8,
        "beschreibung": "Höchste Qualität und Editier-Konsistenz. Gut das Doppelte von [pro].",
    },
    "flex": {
        "id": "black-forest-labs/flux.2-flex", "usd_pro_mp": 0.06, "refs": 8,
        "beschreibung": "Stark bei Text und Typografie — für diese Cover ohne Nutzen. "
                        "Berechnet das Referenzbild zusätzlich (eigener Posten "
                        "'input_image' in der Preisauskunft).",
    },
    "klein4b": {
        "id": "black-forest-labs/flux.2-klein-4b", "usd_pro_mp": 0.014, "refs": 4,
        "beschreibung": "Dasselbe Modell wie lokal in ComfyUI, nur ohne LoRA-Slider. "
                        "Nur sinnvoll, wenn Ganymed nicht erreichbar ist.",
    },
}

# FLUX meldet nur diese Parameter als unterstützt (siehe SKILL.md, Abschnitt
# 'Was der OpenRouter-Weg nicht kann'). 'size' und 'resolution' stehen nicht
# darunter — deshalb kommt die Zielauflösung hier über das Hochskalieren.
STANDARD_AR = "16:9"


def satz_je_mp(modell, timeout=3.0):
    """(Satz je Megapixel Ausgabe, Herkunft) — Herkunft ist 'api' oder 'notwert'.

    GET auf /images/models/<id>/endpoints, **ohne Schlüssel**: eine öffentliche
    Preisauskunft, die keinen Lauf auslöst und nichts kostet. Genommen wird der Posten
    mit billable == 'output_image' — ein Anbieter darf mehrere führen (Ausgabebild,
    Referenzbild), und der Ausgabeposten ist der, den jeder Lauf auslöst.

    Jeder Fehlschlag heißt dasselbe: der eingebaute Notwert gilt, und die Ausgabe sagt
    das dazu (satz_text). Lieber ein gekennzeichneter alter Wert als eine Zahl, der man
    nicht ansieht, woher sie stammt.
    """
    m = MODELLE[modell]
    req = urllib.request.Request(API + "/images/models/" + m["id"] + "/endpoints",
                                 headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as antwort:
            daten = json.loads(antwort.read())
        for endpunkt in daten.get("endpoints") or []:
            for eintrag in endpunkt.get("pricing") or []:
                if (eintrag.get("billable") == "output_image"
                        and eintrag.get("cost_usd") is not None):
                    return float(eintrag["cost_usd"]), "api"
    except (urllib.error.URLError, OSError, ValueError, TypeError, AttributeError) as e:
        print("Satz nicht abrufbar (" + str(e) + ") — Notwert gilt", file=sys.stderr)
        return m["usd_pro_mp"], "notwert"
    print("Kein Ausgabeposten in der Preisauskunft — Notwert gilt", file=sys.stderr)
    return m["usd_pro_mp"], "notwert"


def satz_text(modell, timeout=3.0):
    """Den Satz als Text, mit ausdrücklicher Kennzeichnung eines Notwerts."""
    satz, herkunft = satz_je_mp(modell, timeout)
    text = ("%g" % satz).replace(".", ",") + " USD/MP"
    if herkunft == "api":
        return text
    return text + " (eingebauter Notwert, nicht abgerufen)"


def schluessel():
    k = os.environ.get("OPENROUTER_API_KEY")
    if k:
        return k.strip()
    try:
        with open(SCHLUESSEL_DATEI, encoding="utf8") as f:
            k = f.read().strip()
    except OSError:
        k = ""
    if not k:
        print("Kein Schlüssel gefunden. Erwartet in $OPENROUTER_API_KEY oder "
              + SCHLUESSEL_DATEI, file=sys.stderr)
        return None
    return k


def api(pfad, daten=None, timeout=300):
    k = schluessel()
    if k is None:
        raise SystemExit(2)
    kopf = {"Authorization": "Bearer " + k,
            # OpenRouter führt beides in der Nutzungsübersicht — hilft beim
            # Zuordnen der Kosten, hat sonst keine Wirkung.
            "HTTP-Referer": "https://www.online-resources.de/",
            "X-Title": "online-resources.de Cover"}
    if daten is not None:
        kopf["Content-Type"] = "application/json"
    req = urllib.request.Request(
        API + pfad,
        data=json.dumps(daten).encode("utf8") if daten is not None else None,
        headers=kopf)
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def referenz_teil(quelle):
    """Baut einen input_references-Eintrag. HTTP(S) geht direkt durch.

    Ein lokaler Pfad wird als data-URL eingebettet — das bläht den Request auf
    rund das 1,4-fache der Dateigröße auf und kann in ein 413 laufen. Die Cover
    dieses Blogs liegen öffentlich; die URL ist deshalb der bessere Weg.
    """
    if quelle.startswith(("http://", "https://")):
        return {"type": "image_url", "image_url": {"url": quelle}}
    if not os.path.isfile(quelle):
        print("Referenzbild nicht gefunden: " + quelle, file=sys.stderr)
        return None
    typ = mimetypes.guess_type(quelle)[0] or "image/png"
    with open(quelle, "rb") as f:
        roh = base64.b64encode(f.read()).decode("ascii")
    return {"type": "image_url",
            "image_url": {"url": f"data:{typ};base64,{roh}"}}


def skalieren(quelle, ziel, zielmass):
    """Bringt das Bild auf das Zielmaß und schreibt WebP.

    '^' füllt das Zielrechteck und schneidet mittig zu — nötig, weil die
    Anbieter das Seitenverhältnis auf ihr Raster runden und 16:9 nicht immer
    exakt trifft. Lanczos wie im lokalen Workflow: vergrößert, was da ist,
    statt Details hinzuzuerfinden.
    """
    befehl = ["magick", quelle, "-filter", "Lanczos",
              "-resize", zielmass + "^", "-gravity", "center",
              "-extent", zielmass, "-quality", "92", ziel]
    lauf = subprocess.run(befehl, capture_output=True, text=True)
    if lauf.returncode != 0:
        print("magick ist gescheitert:\n" + lauf.stderr[:800], file=sys.stderr)
        return False
    return True


def fehler_melden(e):
    try:
        koerper = json.loads(e.read().decode("utf8"))
        text = koerper.get("error", {}).get("message", "")
    except Exception:
        text = ""
    hinweise = {
        400: "Ein Parameter paßt nicht zum Modell. FLUX kennt nur aspect_ratio, "
             "output_format, n, seed und input_references.",
        401: "Der Schlüssel wird nicht angenommen.",
        402: "Guthaben erschöpft — Stand prüfen mit --guthaben.",
        413: "Der Request ist zu groß. Referenzbild als URL statt als lokale "
             "Datei übergeben.",
        429: "Rate Limit. Später erneut versuchen.",
        502: "Der Anbieter hinter dem Modell ist ausgefallen.",
        524: "Zeitüberschreitung beim Anbieter.",
        529: "Der Anbieter ist überlastet.",
    }
    print(f"OpenRouter hat mit HTTP {e.code} geantwortet.", file=sys.stderr)
    if text:
        print(text[:500], file=sys.stderr)
    if e.code in hinweise:
        print(hinweise[e.code], file=sys.stderr)
    # Abgerechnet wird nur, was fertig geworden ist: abgebrochene und
    # fehlgeschlagene Läufe kosten laut OpenRouter nichts.


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prompt")
    p.add_argument("--ziel", help="Zieldatei (.webp)")
    p.add_argument("--modell", default="pro", choices=list(MODELLE))
    p.add_argument("--referenz", action="append", default=[], metavar="URL|PFAD",
                   help="Stilvorlage der Reihe, URL aus stile.md. Mehrfach möglich.")
    p.add_argument("--seed", type=int,
                   help="Ohne Angabe wählt der Anbieter. Determinismus ist "
                        "nicht zugesichert.")
    p.add_argument("--ar", default=STANDARD_AR, help="Seitenverhältnis (Vorgabe 16:9)")
    p.add_argument("--zielmass", default=ZIELMASS,
                   help="Endmaß nach dem Hochskalieren, 'keine' läßt das Bild "
                        "wie geliefert (dann als PNG abgelegt)")
    p.add_argument("--steps", type=int,
                   help="Durchgereicht an Black Forest Labs (provider.options)")
    p.add_argument("--guidance", type=float, help="dito")
    p.add_argument("--trocken", action="store_true",
                   help="Request nur anzeigen, nichts senden — kostet nichts")
    p.add_argument("--guthaben", action="store_true", help="Kontostand abfragen")
    p.add_argument("--liste", action="store_true",
                   help="Modelle und Sätze je Megapixel (bei OpenRouter abgefragt)")
    a = p.parse_args()

    if a.liste:
        for k, m in MODELLE.items():
            print(f"{k:8s} {m['id']:34s} {satz_text(k)} · "
                  f"max {m['refs']} Referenzen\n         {m['beschreibung']}")
        return 0

    if a.guthaben:
        d = api("/credits", timeout=30)["data"]
        rest = d["total_credits"] - d["total_usage"]
        print(f"{rest:.2f} USD frei ({d['total_credits']:.2f} gekauft, "
              f"{d['total_usage']:.2f} verbraucht)")
        return 0

    if not a.prompt or not a.ziel:
        p.error("--prompt und --ziel werden gebraucht (oder --liste/--guthaben)")

    m = MODELLE[a.modell]
    if len(a.referenz) > m["refs"]:
        p.error(f"{a.modell} nimmt höchstens {m['refs']} Referenzbilder")
    if not a.referenz:
        print("Hinweis: ohne --referenz trifft das Bild den Reihenstil nicht. "
              "Die URL der Reihe steht in stile.md.", file=sys.stderr)

    anfrage = {"model": m["id"], "prompt": a.prompt,
               "aspect_ratio": a.ar, "output_format": "png", "n": 1}
    if a.seed is not None:
        anfrage["seed"] = a.seed
    if a.referenz:
        teile = [referenz_teil(q) for q in a.referenz]
        if None in teile:
            return 2
        anfrage["input_references"] = teile
    if a.steps is not None or a.guidance is not None:
        opt = {}
        if a.steps is not None:
            opt["steps"] = a.steps
        if a.guidance is not None:
            opt["guidance"] = a.guidance
        anfrage["provider"] = {"options": {"black-forest-labs": opt}}

    if a.trocken:
        # data-URLs kürzen, sonst ist die Ausgabe unlesbar
        zeigbar = json.loads(json.dumps(anfrage))
        for t in zeigbar.get("input_references", []):
            u = t["image_url"]["url"]
            if u.startswith("data:"):
                t["image_url"]["url"] = u[:60] + f"... ({len(u)} Zeichen)"
        print(json.dumps(zeigbar, indent=2, ensure_ascii=False))
        print(f"# POST {API}/images · Satz {satz_text(a.modell)} Ausgabe · "
              f"nichts gesendet", file=sys.stderr)
        return 0

    start = time.time()
    try:
        antwort = api("/images", anfrage)
    except urllib.error.HTTPError as e:
        fehler_melden(e)
        return 1
    except urllib.error.URLError as e:
        print("OpenRouter ist nicht erreichbar: " + str(e.reason), file=sys.stderr)
        return 1

    bilder = antwort.get("data") or []
    if not bilder or not bilder[0].get("b64_json"):
        print("Antwort ohne Bild:\n" + json.dumps(antwort)[:600], file=sys.stderr)
        return 1

    roh = base64.b64decode(bilder[0]["b64_json"])
    kosten = (antwort.get("usage") or {}).get("cost")
    dauer = time.time() - start

    ziel = os.path.abspath(a.ziel)
    os.makedirs(os.path.dirname(ziel) or ".", exist_ok=True)

    if a.zielmass == "keine":
        ziel = os.path.splitext(ziel)[0] + ".png"
        with open(ziel, "wb") as f:
            f.write(roh)
    else:
        zwischen = ziel + ".roh.png"
        with open(zwischen, "wb") as f:
            f.write(roh)
        ok = skalieren(zwischen, ziel, a.zielmass)
        os.remove(zwischen)
        if not ok:
            return 1

    # Der abgerechnete Betrag geht als Datei neben das Bild, nicht nur auf stderr —
    # sonst ist er nach dem headless-Lauf verloren. Die cover-Stufe von RPG Audio
    # Studio liest sie neben dem erzeugten Bild und löscht sie danach wieder, sodass
    # im Post-Ordner nichts liegen bleibt (dort docs/INTERFACE.md, Abschnitt cover).
    kosten_datei = {
        "kosten_usd": kosten,
        "modell_id": m["id"],
        "modell": a.modell,
        "sekunden": round(dauer, 1),
        "seed": a.seed,
        "usage": antwort.get("usage") or {},
        "zeitpunkt": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    with open(ziel + ".kosten.json", "w", encoding="utf-8") as f:
        json.dump(kosten_datei, f, ensure_ascii=False, indent=2)

    print(ziel)
    teile = [a.modell, f"{dauer:.1f} s"]
    if a.seed is not None:
        teile.append(f"Seed {a.seed}")
    if kosten is not None:
        teile.append(f"{kosten:.4f} USD")
    print("# " + " · ".join(teile), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
