# Research Brief

This is the editable "brain" of the weekly research agent. Refine it over time without touching the CI workflow.

## Task

Each week, research the most notable new developments — GitHub repositories, papers, product/model releases, and industry news from the **past 7 days** — across these four focus areas:

1. **Southeast Asian Food & Culture** (`sea-food-culture/`) — food systems, nutrition, ingredients, culinary culture, and food-industry developments across Southeast Asia. **When researching this area, follow the source guide and scraping steps in [`skills/sea-food-culture.md`](skills/sea-food-culture.md)** — search the web, then fetch (scrape) articles from the major travel sites listed there.
2. **AI Engineering** (`ai-engineering/`) — models, tooling, frameworks, and practical engineering patterns for building with AI. **When researching this area, follow [`skills/ai-engineering.md`](skills/ai-engineering.md)** — scrape GitHub (Trending + star-sorted search) for agentic-coding/harnessing repos, and gather high-star repos plus published articles on productionizing healthcare models.
3. **Data Science** (`data-science/`) — methods, techniques, tooling, and applied work. **When researching this area, follow [`skills/data-science.md`](skills/data-science.md)** — high-star GitHub repos plus published articles and papers.
4. **Healthcare Trends** (`healthcare/`) — developments, research, and market movement in the healthcare sector. **When researching this area, follow [`skills/healthcare.md`](skills/healthcare.md)** — search, then fetch articles from the major health-industry, research, and regulatory sources listed there.

## What to publish

From everything you find across the four areas, select the **top 3 developments overall** for the week — the most notable items, regardless of which area they fall in.

For **each** of the 3 selected items, write (or append to) a dated file at:

```
{area}/{year}-W{week}.md
```

where `{area}` is the folder of the focus area the item belongs to, `{year}` is the four-digit year, and `{week}` is the ISO week number (e.g. `ai-engineering/2026-W33.md`). If two of the week's top-3 items share an area, put both in that one weekly file.

### File format

Each weekly file should contain:

- A **3–5 sentence summary** of the week's theme for that area.
- A **bulleted list** of items, each with:
  - **Name** — bold.
  - A **one-line description**.
  - A **link** to the source.

## Update the index

After writing the topic files, **replace** the contents of `README.md`'s **This Week** section (near the top of the README) so it reflects only the current week:

1. **This week's research brief** — replace the blockquote with a fresh **2–3 sentence overview** of the week's top findings across the areas covered (the through-line / why it matters).
2. **The table** — one row per focus area with three columns:
   - **Focus Area** — the area name (keep the emoji).
   - **Summary** — a one-line takeaway for that area this week, or `—` if it wasn't in the top 3.
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
