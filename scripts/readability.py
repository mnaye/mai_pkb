#!/usr/bin/env python3
"""Check each weekly file's So what section: present, and at reading grade 8.

The So what sections are written for an 8th-grade reading level. This
estimates the Flesch-Kincaid grade of each one, plus the one-line so-whats in
README.md, so the job summary shows whether the agent hit the target.

Deterministic and model-free. The syllable count is a heuristic, and product
names (pgvector, Opus 5.5) push the score up a little, so treat it as a guide
rather than a gate: it warns, it never fails the run.

Usage:  python3 scripts/readability.py [--week 2026-W40] [--target 8] [--annotate]

    --annotate   also print GitHub ::warning:: lines (to stderr) for a missing
                 section or a grade above target, so they show on the run page
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AREAS = ["ai-engineering", "healthcare"]


def syllables(word):
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    n = len(groups)
    if word.endswith("e") and not word.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(n, 1)


def plain(md):
    """Strip markdown down to the words a reader actually reads."""
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)  # links -> their text
    md = re.sub(r"`[^`]*`", "code", md)  # inline code counts as one word
    md = re.sub(r"<br>", ". ", md)
    md = re.sub(r"^#+ .*$", "", md, flags=re.M)  # headings aren't sentences
    md = re.sub(r"^\*[^*\n]+\*$", "", md, flags=re.M)  # the italic audience line
    # Labels like **Healthcare data scientists:** or *Problem:* are signposts,
    # not sentences; counted as one-word sentences they flatter the score.
    md = re.sub(r"\*{1,2}[^*\n]{1,40}:\*{1,2}", "", md)
    md = re.sub(r"[*_>|]", "", md)
    return md


def grade(md):
    text = plain(md)
    sentences = [s for s in re.split(r"[.!?]+(?:\s|$)", text) if re.search(r"[A-Za-z]", s)]
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if not sentences or not words:
        return None
    syl = sum(syllables(w) for w in words)
    return 0.39 * len(words) / len(sentences) + 11.8 * syl / len(words) - 15.59


def so_what(path):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^## So what\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def latest_week():
    weeks = sorted(p.stem for a in AREAS for p in (ROOT / a).glob("*-W*.md"))
    return weeks[-1] if weeks else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", default=None)
    ap.add_argument("--target", type=float, default=8.0)
    ap.add_argument("--annotate", action="store_true")
    args = ap.parse_args()
    week = args.week or latest_week()

    rows = []
    for area in AREAS:
        path = ROOT / area / ("%s.md" % week)
        if not path.exists():
            continue
        section = so_what(path)
        rows.append(("%s/%s.md" % (area, week), None if section is None else grade(section)))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    lines = re.findall(r"\*\*So what:\*\*(.*?)(?:\(\[more\]|\|)", readme)
    # Only expect README lines if this week is what the README shows.
    if "research brief (%s)" % week in readme:
        rows.append(("README so-what lines", grade(". ".join(lines)) if lines else None))

    print("| Text | Grade (target <= %g) |" % args.target)
    print("| --- | --- |")
    for name, g in rows:
        if g is None:
            print("| %s | ⚠️ missing |" % name)
            warn = "So what missing: %s" % name
        else:
            over = g > args.target
            print("| %s | %.1f%s |" % (name, g, " ⚠️ above target" if over else ""))
            warn = "So what reads at grade %.1f (target %g): %s" % (g, args.target, name) if over else None
        if warn and args.annotate:
            # stderr, so the annotation reaches the log, not the summary table.
            print("::warning title=So what check::%s" % warn, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
