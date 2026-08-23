# CLAUDE.md — Standing Conventions

Conventions for the weekly research agent and for anyone (human or Claude) editing this knowledge base.

## Voice & format

- Write concise, skimmable summaries — a knowledgeable colleague catching Mai up, not marketing copy.
- One topic per note where practical.
- Every citable claim carries its **source link** and a **date**.
- Use markdown links, not bare URLs.

## Files & naming

- Weekly topic files live under their focus-area folder: `{area}/{year}-W{week}.md` (ISO week, e.g. `ai-engineering/2026-W33.md`).
- Focus-area folders: `ai-engineering/`, `healthcare/`.
- Keep the `README.md` **This Week** section current — it shows only the latest week; the dated files are the archive.

## Accuracy

- **Never fabricate** links, names, papers, or facts. If unsure, leave it out.
- Prefer primary sources over secondary coverage.

## Cadence

- Updated **weekly** (Mondays 09:00 UTC via GitHub Actions, with a Tuesday retry).
- Each run is budget-bounded — see [`GOVERNOR.md`](GOVERNOR.md).
- Publish the **top 3 developments overall** across the two focus areas each week.

## Attribution

- Curated by **Mai with Claude**.
