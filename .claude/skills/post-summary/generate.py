#!/usr/bin/env python3
"""
post-summary — generiert stimmungsvolle Hugo-Frontmatter-Summaries via Gemini CLI.

Aufruf-Beispiele siehe SKILL.md.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILL_DIR.parent.parent.parent
DEFAULT_POSTS_DIR = REPO_ROOT / "content" / "posts"
BRIEFING_PATH = SKILL_DIR / "briefing.md"

# Trunkierungs-Limit für den Body, der ans Modell geht
BODY_CHAR_LIMIT = 6000

# Hartes Maximum für das generierte Summary (Schutznetz, falls Modell überschießt)
SUMMARY_CHAR_LIMIT = 400

# Stimme nach Kategorie (spezifischer schlägt allgemeiner)
CATEGORY_VOICE = [
    ("Aus den Erzählungen von Benjamin Büchernase", "benjamin"),
    ("Tagebuch von Inigo", "inigo"),
    ("Greifenfurter Adel", "dsa"),
    ("Die schwarze Katze", "benjamin"),
    ("Das schwarze Auge", "dsa"),
    ("Warhammer Fantasy", "warhammer"),
    ("GURPS", "gurps"),
]

VOICE_INSTRUCTIONS = {
    "dsa":       "Wir-Form, auktorialer Chronist einer Heldengruppe, sachlich-bardisch, leicht archaisch.",
    "benjamin":  "Ich-Form aus Sicht des gebildet-manierierten Katers Benjamin Buechernase, ironisch, blumig, leicht eitel.",
    "inigo":     "Ich-Form Inigo, tagebuchartig knapp, persoenlich, beobachtend.",
    "warhammer": "Charakterperspektive, episch-ernst, etwas haerterer Ton.",
    "gurps":     "Ich-Form aus Sicht eines Magier-Erzaehlers an der Seite des Zwergs Himgi, trocken-ironisch, leicht herablassend, derb-pragmatisch.",
    "default":   "Stimmungsvoll-erzaehlend, neutrale Wir-/Es-Perspektive.",
}


@dataclass
class Post:
    path: Path
    title: str
    categories: list[str]
    has_summary: bool
    fm_start: int   # Zeilenindex der ersten ---
    fm_end: int     # Zeilenindex der zweiten ---
    title_line: int | None
    body: str
    raw_lines: list[str]


# ---------- Frontmatter-Parsing (lightweight, kein PyYAML) ----------

FM_DELIM = re.compile(r"^---\s*$")
TITLE_RE = re.compile(r'^title\s*:\s*(.*?)\s*$')
SUMMARY_RE = re.compile(r'^summary\s*:')
CATEGORY_LINE_RE = re.compile(r'^categories\s*:')
LIST_ITEM_RE = re.compile(r'^\s*-\s*(.+?)\s*$')


def parse_post(path: Path) -> Post | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=False)

    # Frontmatter-Grenzen finden
    delim_indices = [i for i, l in enumerate(lines) if FM_DELIM.match(l)]
    if len(delim_indices) < 2:
        return None
    fm_start, fm_end = delim_indices[0], delim_indices[1]

    fm_lines = lines[fm_start + 1:fm_end]

    title = ""
    title_line = None
    has_summary = False
    categories: list[str] = []

    in_categories = False
    for idx, line in enumerate(fm_lines):
        absolute_idx = fm_start + 1 + idx

        if SUMMARY_RE.match(line):
            has_summary = True

        m_title = TITLE_RE.match(line)
        if m_title:
            raw = m_title.group(1).strip()
            # Strip wrapping quotes
            if raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]
            elif raw.startswith("'") and raw.endswith("'"):
                raw = raw[1:-1]
            title = raw
            title_line = absolute_idx

        if CATEGORY_LINE_RE.match(line):
            in_categories = True
            continue
        if in_categories:
            m_item = LIST_ITEM_RE.match(line)
            if m_item:
                cat = m_item.group(1).strip()
                if cat.startswith('"') and cat.endswith('"'):
                    cat = cat[1:-1]
                elif cat.startswith("'") and cat.endswith("'"):
                    cat = cat[1:-1]
                categories.append(cat)
                continue
            # nicht-Listen-Zeile: Block beendet
            if line.strip() and not line.startswith(" "):
                in_categories = False

    body = "\n".join(lines[fm_end + 1:]).strip()

    return Post(
        path=path,
        title=title,
        categories=categories,
        has_summary=has_summary,
        fm_start=fm_start,
        fm_end=fm_end,
        title_line=title_line,
        body=body,
        raw_lines=lines,
    )


# ---------- Voice-Mapping ----------

def pick_voice(categories: list[str]) -> str:
    for needle, voice in CATEGORY_VOICE:
        if any(needle.lower() in c.lower() for c in categories):
            return voice
    return "default"


# ---------- Gemini-Call ----------

def build_prompt(briefing: str, title: str, categories: list[str], voice_hint: str, body: str) -> str:
    cat_str = ", ".join(categories) if categories else "(keine Kategorie)"
    body_trunc = body[:BODY_CHAR_LIMIT]
    return (
        f"{briefing}\n\n"
        f"---\n"
        f"KATEGORIEN: {cat_str}\n"
        f"GEWAEHLTE STIMME: {voice_hint}\n"
        f"TITEL: {title}\n\n"
        f"POST-INHALT (gekuerzt):\n"
        f"---\n{body_trunc}\n---\n\n"
        f"Schreibe JETZT das Summary, sonst nichts. Keine Anfuehrungszeichen, kein Markdown."
    )


def call_gemini(prompt: str, timeout: int = 90) -> str:
    """Ruft `gemini -p` auf, gibt Antwort als String zurück."""
    proc = subprocess.run(
        ["gemini", "-p", "Lies Stdin und befolge die Anweisungen.", "-o", "text"],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gemini exit {proc.returncode}: {proc.stderr.strip()[:300]}")
    out = proc.stdout.strip()
    # Filter Hilfszeilen ("Ripgrep is not available", etc.)
    cleaned_lines = [
        l for l in out.splitlines()
        if l.strip() and not l.startswith("Ripgrep")
    ]
    return " ".join(cleaned_lines).strip()


def enforce_char_limit(summary: str, limit: int = SUMMARY_CHAR_LIMIT) -> str:
    """
    Schutznetz: schneidet das Summary auf das harte Zeichen-Limit zurück.
    Bevorzugt einen Schnitt am Satzende (. ! ?), fällt sonst auf Wortgrenze zurück.
    """
    s = summary.strip()
    if len(s) <= limit:
        return s
    window = s[:limit]
    # letzter Satzschluss innerhalb des Limits
    last_sentence = max(window.rfind(". "), window.rfind("! "), window.rfind("? "),
                        window.rfind("."), window.rfind("!"), window.rfind("?"))
    if last_sentence >= int(limit * 0.6):
        return window[:last_sentence + 1].strip()
    # Fallback: letzte Wortgrenze
    last_space = window.rfind(" ")
    if last_space > 0:
        return window[:last_space].rstrip(",;:") + "…"
    return window


# ---------- Frontmatter-Patch ----------

def yaml_escape(s: str) -> str:
    """Escapt einen Single-Line-String für YAML (double-quoted)."""
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    s = re.sub(r"\s+", " ", s).strip()
    return s


def patch_frontmatter(post: Post, summary: str) -> str:
    new_line = f'summary: "{yaml_escape(summary)}"'
    lines = list(post.raw_lines)
    insert_at = (post.title_line + 1) if post.title_line is not None else (post.fm_start + 1)
    lines.insert(insert_at, new_line)
    return "\n".join(lines) + "\n"


# ---------- Worker ----------

def process_post(path: Path, briefing: str, force: bool, dry_run: bool) -> tuple[str, str]:
    """Returns (status, message). status in {ok, skip, error}."""
    label = path.parent.name if path.name == "index.md" else path.name
    try:
        post = parse_post(path)
        if post is None:
            return ("error", f"{label}: kein gültiges Frontmatter")
        if post.has_summary and not force:
            return ("skip", f"{label}: summary bereits vorhanden")
        if not post.body.strip():
            return ("error", f"{label}: Body leer")

        voice = pick_voice(post.categories)
        voice_hint = VOICE_INSTRUCTIONS.get(voice, VOICE_INSTRUCTIONS["default"])
        prompt = build_prompt(briefing, post.title, post.categories, voice_hint, post.body)

        if dry_run:
            return ("ok", f"{label} [{voice}]: würde generieren")

        summary = call_gemini(prompt)
        if not summary:
            return ("error", f"{label}: leere Gemini-Antwort")

        original_len = len(summary)
        summary = enforce_char_limit(summary)
        was_clipped = len(summary) < original_len

        # Wenn force + bereits vorhanden: vorher entfernen
        if force and post.has_summary:
            post = remove_summary_lines(post)

        new_text = patch_frontmatter(post, summary)
        path.write_text(new_text, encoding="utf-8")

        words = len(summary.split())
        chars = len(summary)
        clip_marker = " ✂" if was_clipped else ""
        preview = summary[:80].replace("\n", " ") + ("…" if len(summary) > 80 else "")
        return ("ok", f"{label} [{voice}, {words}w/{chars}c{clip_marker}]: {preview}")
    except Exception as e:
        return ("error", f"{label}: {e}")


def remove_summary_lines(post: Post) -> Post:
    """Entfernt bestehende summary-Zeile(n) aus dem Frontmatter (single-line + literal-block)."""
    new_lines: list[str] = []
    skip_block = False
    fm_start, fm_end = post.fm_start, post.fm_end
    removed = 0
    for idx, line in enumerate(post.raw_lines):
        if fm_start < idx < fm_end:
            if skip_block:
                # ein Literal-/Folded-Block endet bei einer nicht-eingerückten Zeile
                if line.startswith(" ") or line.startswith("\t"):
                    removed += 1
                    continue
                skip_block = False
            if SUMMARY_RE.match(line):
                removed += 1
                # Multi-line Block?
                if re.match(r'^summary\s*:\s*[|>][-+]?\s*$', line):
                    skip_block = True
                continue
        new_lines.append(line)
    # fm_end verschiebt sich
    return Post(
        path=post.path,
        title=post.title,
        categories=post.categories,
        has_summary=False,
        fm_start=post.fm_start,
        fm_end=post.fm_end - removed,
        title_line=post.title_line,
        body=post.body,
        raw_lines=new_lines,
    )


# ---------- CLI ----------

def main() -> int:
    parser = argparse.ArgumentParser(description="Hugo-Post-Summary-Generator (Gemini-backed).")
    parser.add_argument("--posts-dir", default=str(DEFAULT_POSTS_DIR),
                        help="Posts-Verzeichnis (Default: content/posts)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Maximalzahl der zu verarbeitenden Posts (0 = alle)")
    parser.add_argument("--parallel", type=int, default=4,
                        help="Anzahl paralleler Gemini-Calls (Default: 4)")
    parser.add_argument("--single", type=str, default=None,
                        help="Nur diesen einen Post verarbeiten")
    parser.add_argument("--force", action="store_true",
                        help="Bestehende summary-Felder überschreiben")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nur anzeigen, was generiert würde — kein Gemini-Call")
    args = parser.parse_args()

    if not BRIEFING_PATH.exists():
        print(f"FEHLER: Briefing nicht gefunden: {BRIEFING_PATH}", file=sys.stderr)
        return 2
    briefing = BRIEFING_PATH.read_text(encoding="utf-8")

    posts_dir = Path(args.posts_dir)
    if args.single:
        targets = [Path(args.single).resolve()]
    else:
        targets = sorted(posts_dir.glob("*/index.md"))

    if args.limit:
        targets = targets[:args.limit]

    if not targets:
        print("Keine Posts gefunden.", file=sys.stderr)
        return 1

    print(f"→ {len(targets)} Post(s), parallel={args.parallel}, force={args.force}, dry_run={args.dry_run}", flush=True)

    counts = {"ok": 0, "skip": 0, "error": 0}
    with cf.ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futures = {
            ex.submit(process_post, p, briefing, args.force, args.dry_run): p
            for p in targets
        }
        for fut in cf.as_completed(futures):
            status, msg = fut.result()
            counts[status] += 1
            symbol = {"ok": "✓", "skip": "⏭", "error": "✗"}[status]
            print(f"{symbol} {msg}", flush=True)

    print(f"\nFertig — ok={counts['ok']} skip={counts['skip']} error={counts['error']}")
    return 0 if counts["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
