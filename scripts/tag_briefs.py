#!/usr/bin/env python3
"""Stamp each weekly brief item with the topic logged for it in the ledger.

The agent already writes one `data/trends.csv` row per published item. This
matches those rows back to the items in `{area}/{year}-Www.md` and stamps the
topic onto the item line, so someone reading a brief sees the same
classification the trend table counts.

Deterministic and model-free, which is the point: the agent does no tagging
work, spends no turns on it, and cannot invent a tag that the trend table
then disagrees with.

Matching is by URL first (a ledger row's URL almost always appears in its
item) with headline/title word overlap as the tiebreak — necessary because
several items in a week can cite the same front-page URL. Assignment is
brute-forced over permutations, which is optimal at these sizes (<= 6 items
per file) rather than greedy.

Usage:  python3 scripts/tag_briefs.py [--check]

    --check   exit 1 if any brief is untagged or mistagged, changing nothing
"""

import csv
import re
import sys
from collections import defaultdict
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "data" / "trends.csv"

# The stamp. The `topic:` prefix keeps it unambiguous to find again, so
# re-running replaces the tag instead of stacking a second one beside it.
TAG = "`topic:%s`"
TAG_RE = r"`topic:[a-z-]+`"

# Pre-vocabulary briefs carry ad-hoc markers like *(regulation / product /
# funding)* in the same position. Those are exactly the fragmentation the
# closed vocabulary replaced, so they are overwritten rather than left to sit
# next to the canonical tag.
LEGACY_RE = r"\*\([^)]*\)\*"

TITLE_RE = re.compile(r"^- \*\*(.+?)\*\*", re.S)
AFTER_TITLE_RE = re.compile(r"\s*(?:%s|%s)" % (TAG_RE, LEGACY_RE))

STOP = {
    "the", "a", "an", "of", "for", "and", "to", "in", "on", "with", "its",
    "it", "is", "as", "at", "by", "from", "that", "this", "new", "now",
}

MIN_SCORE = 20.0  # below this, refuse to guess


def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower())
            if len(w) > 2 and w not in STOP}


def split_items(section):
    """Every item is a top-level '- ' bullet; an item may wrap across lines.

    The trailing newlines matter: the split consumes only the one newline
    before the next bullet, so a blank-line-separated item keeps a '\\n' of its
    own. Rejoining those with '\\n\\n' would add one blank line per run and the
    briefs would drift a little wider every week, so strip them here and let
    the join own the separator.
    """
    parts = re.split(r"\n(?=- )", section.strip())
    return [p.rstrip("\n") for p in parts if p.startswith("- ")]


def title_of(item):
    m = TITLE_RE.search(item)
    return m.group(1) if m else item[:200]


def score(row, item):
    """How well one ledger row matches one brief item."""
    total = 0.0
    url = row["url"].strip()
    if url and url in item:
        total += 100.0
    a, b = words(row["headline"]), words(title_of(item))
    if a and b:
        total += 50.0 * len(a & b) / len(a | b)
    return total


def best_assignment(rows, items):
    """Optimal row->item assignment. Brute force is fine at this size."""
    if not rows or not items:
        return {}
    best_total, best_perm = None, None
    for perm in permutations(range(len(items)), len(rows)):
        total = sum(score(rows[i], items[perm[i]]) for i in range(len(rows)))
        if best_total is None or total > best_total:
            best_total, best_perm = total, perm
    return {i: best_perm[i] for i in range(len(rows))}


def stamp(item, topic):
    """Insert or replace the topic tag directly after the item's bold title."""
    m = TITLE_RE.search(item)
    if not m:
        return item
    head, rest = item[: m.end()], item[m.end():]
    existing = AFTER_TITLE_RE.match(rest)
    if existing:
        rest = rest[existing.end():]
    return "%s %s%s" % (head, TAG % topic, rest)


def process(path, rows, problems):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^## Items\s*$", text, re.M)
    if not m:
        problems.append("%s: no '## Items' section" % path)
        return text, text

    start = m.end()
    nxt = re.search(r"^## ", text[start:], re.M)
    end = start + (nxt.start() if nxt else len(text) - start)
    section = text[start:end]

    items = split_items(section)
    if not items:
        problems.append("%s: no items found under '## Items'" % path)
        return text, text
    if len(rows) != len(items):
        problems.append(
            "%s: %d ledger rows but %d items — tagging what matches"
            % (path.name, len(rows), len(items))
        )

    pairing = best_assignment(rows, items)
    tagged = dict()
    for ri, ii in pairing.items():
        s = score(rows[ri], items[ii])
        if s < MIN_SCORE:
            problems.append(
                "%s: no confident match for %r (best score %.1f) — left untagged"
                % (path.name, rows[ri]["headline"][:50], s)
            )
            continue
        tagged[ii] = rows[ri]["topic"]

    rebuilt = []
    for i, item in enumerate(items):
        rebuilt.append(stamp(item, tagged[i]) if i in tagged else item)

    # Preserve the section's original leading/trailing whitespace exactly.
    lead = section[: len(section) - len(section.lstrip("\n"))]
    trail = section[len(section.rstrip("\n")):]
    new_section = lead + "\n\n".join(rebuilt) + trail
    return text, text[:start] + new_section + text[end:]


def main():
    check = "--check" in sys.argv[1:]
    if not LEDGER.exists():
        sys.exit("missing ledger: %s" % LEDGER)

    by_file = defaultdict(list)
    with LEDGER.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            by_file[(row["area"], row["week"])].append(row)

    problems, changed = [], []
    for (area, week), rows in sorted(by_file.items()):
        path = ROOT / area / ("%s.md" % week)
        if not path.exists():
            problems.append("%s: brief missing for %d ledger rows" % (path, len(rows)))
            continue
        before, after = process(path, rows, problems)
        if before != after:
            changed.append(path)
            if not check:
                path.write_text(after, encoding="utf-8")

    for p in problems:
        print("warning: %s" % p, file=sys.stderr)

    if check:
        if changed:
            sys.exit(
                "%d brief(s) need tagging: %s"
                % (len(changed), ", ".join(str(p.relative_to(ROOT)) for p in changed))
            )
        print("all briefs tagged")
        return

    if changed:
        print("tagged %d brief(s): %s"
              % (len(changed), ", ".join(str(p.relative_to(ROOT)) for p in changed)))
    else:
        print("all briefs already tagged")


if __name__ == "__main__":
    main()
