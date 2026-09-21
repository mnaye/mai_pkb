#!/usr/bin/env python3
"""Regenerate the rolling 13-week topic-trend table in README.md.

Deterministic and model-free: this reads ``data/trends.csv`` (one row per
published item, appended by the weekly agent) and rewrites the block between
the TRENDS:START / TRENDS:END markers in README.md.

The point of doing it here rather than in the agent: counting 13 weeks of
history by re-reading the archive would cost ~26 extra turns against a 35-turn
cap and tens of thousands of tokens every week. Counting rows in a CSV costs
nothing, and the numbers cannot be misremembered.

Usage:  python3 scripts/render_trends.py [--check]

    --check   exit 1 if README.md is out of date instead of rewriting it
"""

import csv
import html
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "data" / "trends.csv"
README = ROOT / "README.md"

WINDOW_WEEKS = 13
BAR_WIDTH = 12

START = "<!-- TRENDS:START -->"
END = "<!-- TRENDS:END -->"

# The closed vocabulary. Topics are listed here even when they have zero items
# in the window: a standing zero is a signal (it is how three empty weeks of
# `clinical-ml` became visible), not something to hide by omission.
AREAS = [
    (
        "ai-engineering",
        "🤖 AI Engineering",
        ["models", "agents", "skills-tooling", "context", "infra", "clinical-ml"],
    ),
    (
        "healthcare",
        "🏥 Healthcare",
        ["fda", "payment", "enforcement", "clinical-ai", "trials", "market"],
    ),
]

WEEK_RE = re.compile(r"^(\d{4})-W(\d{2})$")


def week_monday(week_str):
    """'2026-W38' -> the date of that ISO week's Monday."""
    m = WEEK_RE.match(week_str.strip())
    if not m:
        raise ValueError("bad week value: %r" % week_str)
    return date.fromisocalendar(int(m.group(1)), int(m.group(2)), 1)


def load_rows():
    if not LEDGER.exists():
        sys.exit("missing ledger: %s" % LEDGER)
    with LEDGER.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        row["_monday"] = week_monday(row["week"])
    return rows


def bar(n, maxn):
    """A fixed-width bar, so every row lines up however small the counts are."""
    if maxn <= 0:
        return "░" * BAR_WIDTH
    filled = int(round(n / float(maxn) * BAR_WIDTH))
    if n > 0:
        filled = max(1, filled)
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def render(rows):
    if not rows:
        return "%s\n\n_No items logged yet._\n\n%s" % (START, END)

    # Anchor on the newest week actually present, not on today: the table then
    # shows the most recent 13 weeks of real data and renders identically no
    # matter what day the workflow happens to run.
    anchor = max(r["_monday"] for r in rows)
    first = anchor - timedelta(weeks=WINDOW_WEEKS - 1)
    window = [r for r in rows if r["_monday"] >= first]

    weeks_published = sorted({r["week"] for r in window})
    span_start = "%d-W%02d" % first.isocalendar()[:2]
    span_end = "%d-W%02d" % anchor.isocalendar()[:2]

    out = [START, ""]
    out.append("### 📈 Topic trends — rolling %d weeks" % WINDOW_WEEKS)
    out.append("")
    out.append(
        "`%s` → `%s` · **%d weeks published** · **%d items** · ranked by volume, "
        "counted from [`data/trends.csv`](data/trends.csv)."
        % (span_start, span_end, len(weeks_published), len(window))
    )
    out.append("")

    known = set()
    for _, _, topics in AREAS:
        known.update(topics)

    for slug, label, topics in AREAS:
        area_rows = [r for r in window if r["area"] == slug]
        # Seed every vocabulary topic at zero so a dormant one still gets a row.
        counts = dict((t, 0) for t in topics)
        last_seen = {}
        for r in area_rows:
            t = r["topic"].strip()
            counts[t] = counts.get(t, 0) + 1
            if t not in last_seen or r["week"] > last_seen[t]:
                last_seen[t] = r["week"]

        # Off-vocabulary topics still get a row, so typos surface loudly
        # instead of being silently dropped from the totals.
        for t in sorted(counts):
            if t not in known:
                print(
                    "warning: off-vocabulary topic %r in %s" % (t, slug),
                    file=sys.stderr,
                )

        # Highest volume first. Stable sorts compose, so ties fall back to most
        # recently seen, then alphabetical — the output never reshuffles itself.
        ranked = sorted(counts.items(), key=lambda kv: kv[0])
        ranked.sort(key=lambda kv: last_seen.get(kv[0], ""), reverse=True)
        ranked.sort(key=lambda kv: kv[1], reverse=True)

        maxn = max([n for _, n in ranked] + [0])

        out.append("**%s** — %d items" % (label, len(area_rows)))
        out.append("")
        # Raw HTML: GitHub strips <style> and style= from READMEs, so alignment
        # attributes and a fixed-width bar are what "pretty" can mean here.
        # No blank lines inside the block — they break GitHub out of the table.
        out.append("<table>")
        out.append(
            '<tr>'
            '<th align="right">#</th>'
            '<th align="left">Topic</th>'
            '<th align="left">Trend</th>'
            '<th align="right">Items</th>'
            '<th align="left">Last seen</th>'
            '</tr>'
        )
        for rank, (topic, n) in enumerate(ranked, 1):
            flag = "" if topic in known else " ⚠️"
            name = "<code>%s</code>%s" % (html.escape(topic), flag)
            if n and n == maxn:
                name = "<b>%s</b>" % name
            seen = last_seen.get(topic)
            out.append(
                '<tr>'
                '<td align="right"><sub>%d</sub></td>'
                '<td>%s</td>'
                '<td><code>%s</code></td>'
                '<td align="right"><b>%d</b></td>'
                '<td><sub>%s</sub></td>'
                '</tr>' % (rank, name, bar(n, maxn), n, seen if seen else "—")
            )
        out.append("</table>")
        out.append("")

    out.append(END)
    return "\n".join(out)


def main():
    check = "--check" in sys.argv[1:]
    rows = load_rows()
    block = render(rows)

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit("README.md is missing the %s / %s markers" % (START, END))

    pattern = re.compile(
        re.escape(START) + r".*?" + re.escape(END), re.DOTALL
    )
    updated = pattern.sub(lambda _: block, text, count=1)

    if updated == text:
        print("trend table already up to date")
        return

    if check:
        sys.exit("README.md trend table is out of date; run scripts/render_trends.py")

    README.write_text(updated, encoding="utf-8")
    print("trend table updated (%d rows in ledger)" % len(rows))


if __name__ == "__main__":
    main()
