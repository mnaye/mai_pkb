# Research Brief

This is the editable "brain" of the weekly research agent. Refine it over time without touching the CI workflow.

## Task

Each week, research the most notable new developments — GitHub repositories, papers, product/model releases, and industry news from the **past 7 days** — across these two focus areas:

1. **AI Engineering** (`ai-engineering/`) — models, tooling, frameworks, and practical engineering patterns for building with AI. **When researching this area, follow [`skills/ai-engineering.md`](skills/ai-engineering.md)** — scrape GitHub (Trending + star-sorted search) for agentic-coding/harnessing repos, and gather high-star repos plus published articles on productionizing healthcare models.
2. **Healthcare Trends** (`healthcare/`) — developments, research, and market movement in the healthcare sector. **When researching this area, follow [`skills/healthcare.md`](skills/healthcare.md)** — search, then fetch articles from the major health-industry, research, and regulatory sources listed there.

## Run budget (the governor)

The workflow hands this run a **budget** in the prompt. Those numbers win over anything
below or in the skill files — the skills describe *where* to look, not *how much* to look.
Full detail: [`GOVERNOR.md`](GOVERNOR.md).

- **Scope.** This knowledge base tracks **two** areas, and every run covers both. The workflow
  names them in the prompt. Pick the week's **top 3 items across those two areas** — they may
  split 2/1, 3/0, or 1/2; take the genuinely most notable items, not one per area for balance.
- **Search/fetch budget.** The prompt states a per-area cap on `WebSearch` and `WebFetch`
  calls. Spend it on breadth first, then stop. Do **not** re-search to marginally improve an
  item you already have — a good item you found on search 2 is worth more than a slightly
  better one on search 6.
- **Land the plane.** The run has a hard turn cap and a wall-clock timeout. Leave room to
  write the files, update the README, and commit. Running out mid-sentence is the one
  genuinely bad outcome.
- **Commit after each area.** Finish an area's file → commit it → move to the next. Do not
  save all writing for the end. If the session is cut short (Claude usage limit, timeout),
  whatever is committed still publishes; whatever is only in memory is lost.
- **The ISO week is given to you.** Use the `{year}-W{week}` from the prompt. Don't shell out
  to `date` to recompute it.
- **An area with nothing worth publishing** gets `—` in the README table. Publishing fewer
  than 3 items is better than padding — see the accuracy rules.

## What to publish

From everything you find across the two areas, select the **top 3 developments overall** for the week — the most notable items, regardless of which of the two they fall in.

For **each** of the 3 selected items, write (or append to) a dated file at:

```
{area}/{year}-W{week}.md
```

where `{area}` is the folder of the focus area the item belongs to, and `{year}-W{week}` is the ISO week **given to you in the prompt** (e.g. `ai-engineering/2026-W33.md`). If two of the week's top-3 items share an area, put both in that one weekly file.

### File format

Each weekly file should contain:

- A **3–5 sentence summary** of the week's theme for that area.
- A **bulleted list** of items, each with:
  - **Name** — bold.
  - A **one-line description**.
  - A **link** to the source.

## Update the index

After writing the topic files, **replace** the contents of `README.md`'s **This Week** section (near the top of the README) so it reflects only the current week:

1. **This week's research brief** — replace the blockquote with a fresh **2–3 sentence overview** of the week's top findings (the through-line / why it matters).
2. **The table** — one row per focus area with three columns:
   - **Focus Area** — the area name (keep the emoji).
   - **Summary** — a one-line takeaway for that area this week, or `—` if nothing from it made the top 3.
   - **File** — a markdown link to this week's dated file for that area (e.g. `[2026-W33](ai-engineering/2026-W33.md)`), or `—` if it wasn't in the top 3.

Do not keep prior weeks in this section — the dated files under each folder are the archive.

## Commit

Commit everything with the message:

```
Weekly research: {YYYY-MM-DD}
```

## Accuracy rules

- **Never invent links, names, or facts.** Only include items you actually found and can link to a real source.
- If you cannot find 3 genuinely notable developments in a given week, publish fewer rather than padding.
- Prefer primary sources (the repo, the paper, the official release/announcement) over secondary coverage.
- Attribute curation to **"Mai with Claude"** where relevant.
