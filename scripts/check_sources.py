#!/usr/bin/env python3
"""Check that every published item links to its own source, not a front page.

Each item under ``## Items`` in a weekly brief, and each row it logged to
``data/trends.csv``, must point at the page that supports it: the article,
the agency document, the repo, the release post. A homepage, a search page,
or an index (a newsroom, a trending board, a changelog) changes daily, so
months later nobody can check what the brief said or why. Those get flagged.

Deterministic and model-free. The agent runs it before each area's commit,
chained with ``&&`` so a failure blocks the commit; the workflow runs it again
afterwards as a backstop.

Usage:
    python3 scripts/check_sources.py FILE [FILE ...]   check these briefs
    python3 scripts/check_sources.py --week 2026-W42   both areas for a week
    python3 scripts/check_sources.py --all             the whole archive

    --annotate   also print GitHub ::warning:: lines to stderr
    Exit status is 1 if anything is flagged.
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "data" / "trends.csv"
AREAS = ["ai-engineering", "healthcare"]
FILE_RE = re.compile(r"^(?P<area>[a-z-]+)/(?P<week>\d{4}-W\d{2})\.md$")

# A URL whose last path segment is one of these is a listing, not a source.
INDEX_SEGMENTS = {
    "news", "newsroom", "news-and-events", "press", "press-releases",
    "press-releases.html", "press-announcements", "media", "media-centre",
    "media-center", "blog", "updates", "trending", "articles", "insights",
    "publications", "releases", "headlines", "latest", "topics", "category",
    "tag", "index.html", "home",
}
SEARCH_KEYS = {"q", "query", "s", "search", "term", "keyword", "keywords"}
LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")


def problem(url):
    """Why this URL can't be an item's source, or None if it's a direct link."""
    u = urlparse(url.strip())
    if u.scheme not in ("http", "https") or not u.netloc:
        return "not a web link"
    segments = [s for s in u.path.split("/") if s]
    if not segments:
        return "homepage"
    if "search" in (s.lower() for s in segments) or SEARCH_KEYS & set(parse_qs(u.query)):
        return "search page"
    if segments[-1].lower() in INDEX_SEGMENTS:
        return "index page"
    host = u.netloc.lower()
    if host.endswith("github.com") and len(segments) < 2:
        return "index page"  # a user or org page, not a repo
    return None


def items(text):
    """(title, first link) for each top-level bullet under ## Items."""
    m = re.search(r"^## Items\s*$", text, re.M)
    if not m:
        return []
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    section = rest[:nxt.start()] if nxt else rest
    out = []
    for part in re.split(r"\n(?=- )", section.strip()):
        if not part.startswith("- "):
            continue
        title = re.match(r"- \*\*(.+?)\*\*", part, re.S)
        title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", title.group(1)) if title else part[2:60]
        link = LINK_RE.search(part)
        out.append((title.strip(), link.group(1) if link else None))
    return out


def check_file(path, ledger):
    rel = path.relative_to(ROOT).as_posix()
    m = FILE_RE.match(rel)
    found = []
    for title, link in items(path.read_text(encoding="utf-8")):
        why = "no source link" if link is None else problem(link)
        if why:
            found.append((rel, "item", title, link or "—", why))
    if m:
        for r in ledger:
            if r["week"] == m.group("week") and r["area"] == m.group("area"):
                why = problem(r["url"])
                if why:
                    found.append(("data/trends.csv", m.group("week"), r["headline"], r["url"], why))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--week")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--annotate", action="store_true")
    args = ap.parse_args()

    if args.all:
        paths = sorted(p for a in AREAS for p in (ROOT / a).glob("*-W*.md"))
    elif args.week:
        paths = [ROOT / a / ("%s.md" % args.week) for a in AREAS]
        paths = [p for p in paths if p.exists()]
    else:
        paths = [(ROOT / f).resolve() for f in args.files]
    if not paths:
        print("No briefs to check.")
        return 0

    with LEDGER.open(newline="", encoding="utf-8") as fh:
        ledger = list(csv.DictReader(fh))

    found = []
    for p in paths:
        found += check_file(p, ledger)

    if not found:
        print("✅ Every item links to its own source (%d brief(s) checked)." % len(paths))
        return 0

    print("⚠️ %d link(s) are a homepage, search page or index, not the item's own source:" % len(found))
    print("")
    print("| Where | Item | Link | Problem |")
    print("| --- | --- | --- | --- |")
    for where, kind, title, link, why in found:
        label = where if kind == "item" else "%s (%s row)" % (where, kind)
        print("| %s | %s | %s | %s |" % (label, title[:70].replace("|", "/"), link, why))
        if args.annotate:
            print("::warning title=Source link check::%s: '%s' — %s, not its own source (%s)"
                  % (label, title[:70], why, link), file=sys.stderr)
    print("")
    print("Fix: link the article, document, repo or release itself. If you can't reach a "
          "direct source within budget, move the item to Also noted, marked unconfirmed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
