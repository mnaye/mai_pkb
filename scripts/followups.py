#!/usr/bin/env python3
"""Read the follow-ups ledger for the weekly run, and show it in README.md.

``data/follow-ups.csv`` holds dated commitments the agent has met: comment
deadlines, expected filings, trial readouts. The agent adds rows and closes
them; this script does everything that is only arithmetic on dates, so the
agent never spends a turn reading the file to find out what is due.

Usage:
    python3 scripts/followups.py prompt [--today YYYY-MM-DD] [--horizon DAYS]
        Print the open items that are overdue or due within the horizon,
        plus undated (TBD) ones, as plain text for the workflow prompt.

    python3 scripts/followups.py render [--check]
        Rewrite the FOLLOWUPS:START / FOLLOWUPS:END block in README.md.
        --check exits 1 if README.md is out of date instead of rewriting it.
"""

import argparse
import csv
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "data" / "follow-ups.csv"
README = ROOT / "README.md"

START = "<!-- FOLLOWUPS:START -->"
END = "<!-- FOLLOWUPS:END -->"

HORIZON_DAYS = 21  # three weekly runs of warning before a deadline


def parse_due(value):
    """Return a date, or None for TBD / anything that isn't an ISO date."""
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


def load_open():
    with LEDGER.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["status"].strip() == "open"]
    # Dated items first, soonest first; TBD items after them.
    return sorted(rows, key=lambda r: (parse_due(r["due"]) is None, parse_due(r["due"]) or date.max))


def prompt(today, horizon):
    rows = load_open()
    cutoff = today + timedelta(days=horizon)
    due, undated = [], []
    for r in rows:
        d = parse_due(r["due"])
        if d is None:
            undated.append(r)
        elif d <= cutoff:
            days = (d - today).days
            when = "OVERDUE by %d days" % -days if days < 0 else "due in %d days" % days
            due.append("- %s (%s, %s): %s [%s]" % (r["due"], when, r["area"], r["item"], r["source"]))

    out = []
    if due:
        out.append("Due within %d days or overdue:" % horizon)
        out.extend(due)
    else:
        out.append("Nothing open is due within %d days." % horizon)
    if undated:
        out.append("Open with no date yet (update only if you meet them; do not spend budget chasing them):")
        out.extend("- %s: %s [%s]" % (r["area"], r["item"], r["source"]) for r in undated)
    return "\n".join(out)


def render():
    rows = load_open()
    out = [START, "", "### 📌 Coming up", ""]
    if not rows:
        out.append("_Nothing open._")
    else:
        out.append("| Due | Item | Area |")
        out.append("| --- | --- | --- |")
        for r in rows:
            item = r["item"].replace("|", "\\|")
            out.append("| %s | [%s](%s) | %s |" % (r["due"], item, r["source"], r["area"]))
    out += [
        "",
        "<sub>Open items from [`data/follow-ups.csv`](data/follow-ups.csv), where the weekly run "
        "records deadlines it finds and closes them once they're covered.</sub>",
        "",
        END,
    ]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prompt")
    p.add_argument("--today", type=date.fromisoformat, default=date.today())
    p.add_argument("--horizon", type=int, default=HORIZON_DAYS)
    r = sub.add_parser("render")
    r.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.cmd == "prompt":
        print(prompt(args.today, args.horizon))
        return 0

    text = README.read_text(encoding="utf-8")
    block = render()
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.S)
    if pattern.search(text):
        new = pattern.sub(lambda _: block, text)
    else:
        # First run: place the block straight after the trend table.
        anchor = "<!-- TRENDS:END -->"
        if anchor not in text:
            sys.exit("README.md has no %s marker to anchor the follow-ups block" % anchor)
        new = text.replace(anchor, anchor + "\n\n" + block, 1)

    if args.check:
        return 0 if new == text else 1
    if new != text:
        README.write_text(new, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
