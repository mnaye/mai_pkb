# Research Brief

This is the editable "brain" of the weekly research agent. Refine it over time without touching the CI workflow.

## Task

Each week, research the most notable new developments — GitHub repositories, papers, product/model releases, and industry news from the **past 7 days** — across these two focus areas:

1. **AI Engineering** (`ai-engineering/`) — models, tooling, frameworks, and practical engineering patterns for building with AI. **When researching this area, follow [`skills/ai-engineering.md`](skills/ai-engineering.md)** — scrape GitHub (Trending + star-sorted search) for agentic-coding/harnessing repos, and gather high-star repos plus published articles on productionizing healthcare models.
2. **Healthcare Trends** (`healthcare/`) — **changes in healthcare regulation first**, then industry moves, market movement, and research. **When researching this area, follow [`skills/healthcare.md`](skills/healthcare.md)** — lead with the regulatory sources listed there (FDA, CMS, HHS/OCR, ASTP-ONC, Federal Register), fetching the primary agency document before any secondary coverage, and spend what's left of the budget on industry and research.

## Who reads this

Write for three readers, all working in or around healthcare:

- **Healthcare data scientists**: analysis, cohorts, evaluation, and the evidence behind clinical and business decisions.
- **ML engineers in healthcare**: building, validating, deploying and monitoring models and agents under PHI, HIPAA and regulatory constraints.
- **Healthcare executives**: budget, risk, compliance and strategy, and deciding which problems their teams take on.

Every weekly file ends its items with a **So what** for these readers (format below). An AI Engineering
item still needs its healthcare angle spelled out: what the tool or model changes for someone handling
patient data, clinical workflows or regulated submissions.

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
- A **`## So what`** section, placed **directly after `## Items`** and before any `## Also noted` or
  `## Caveats`. It must be its own `## ` heading, because `scripts/tag_briefs.py` reads the items
  from `## Items` up to the next `## ` heading. Use this shape:

  ```markdown
  ## So what

  *For healthcare data scientists, ML engineers in healthcare, and healthcare executives.*

  - **Healthcare data scientists:** how this week's items change their work, and one concrete next step.
  - **ML engineers in healthcare:** what it means for building, validating, deploying or monitoring
    under PHI and regulatory constraints.
  - **Healthcare executives:** the decision, budget, risk or deadline it puts in front of them.

  ### Problems worth taking on

  **<Name of the use case>.** *Problem:* who has it and what it costs them today. *Why now:* which
  item above makes it newly possible or newly necessary. *First step:* the data, owner and success
  measure for a small pilot.
  ```

  **Write the So what in plain English, at an 8th-grade reading level or below.** The rest of the
  file keeps its normal register; this section is the part busy readers skim, including executives
  who don't live in the details. In practice:
  - **Short sentences**, around 15 words on average and rarely more than 20. One idea per sentence.
  - **Everyday words.** "Use" not "leverage", "check" not "validate", "cost" not "spend profile".
  - **Explain any term a smart non-specialist wouldn't know, in plain words, the first time it
    appears**: "private health data (the law calls it PHI)", "a drug filing sent to FDA". Drop the
    term if the sentence works without it. Names of products, agencies and rules stay as they are.
  - **Talk to the reader**, in the active voice: "Check this claim yourself", not "Verification of
    this claim is recommended".
  - Plain doesn't mean vague. Keep the dates, numbers and names that make it useful.

  `scripts/readability.py` scores each So what section after the run and reports the grade in the
  job summary. See `healthcare/2026-W40.md` for a section written this way.

  Rules for the So what:
  - **Ground every line in an item in this file**, and name it. It's analysis of what you published,
    so it needs no searches or fetches of its own and must not add new facts, figures or links.
  - **Be specific.** "Re-price the agent-assisted refactor you shelved last quarter" beats "could
    transform workflows". If an item changes nothing for one of the readers, write *Nothing
    actionable this week* for that reader instead of stretching.
  - **One or two problems worth taking on**, not more. Each is a problem a team could scope in a
    week, framed as an idea to test rather than a claim that it works.
  - **Don't overstate the item.** If the source says a rule changes wording and keeps the safety
    standard, the so-what can't say the standard dropped.

## Update the index

After writing the topic files, update `README.md`'s **This Week** section (near the top of the README) so it reflects only the current week. Replace **only these two things**:

1. **This week's research brief** — replace the blockquote with a fresh **2–3 sentence overview** of the week's top findings (the through-line / why it matters).
2. **The table** — one row per focus area with four columns:
   - **Focus Area** — the area name (keep the emoji).
   - **Topics** — the topic tags you logged for that area this week, as inline code joined by ` · `
     (e.g. `` `fda` · `trials` ``). Use **exactly** the tags you wrote to [`data/trends.csv`](data/trends.csv)
     for this week — no others, no invented ones — so this table and the trend counts below it can
     never disagree. `—` if the area published nothing.
   - **Summary** — a one-line takeaway for that area this week, then `<br>**So what:** ` and one
     or two short sentences with the most actionable implication for the readers above, in the same
     plain English as the So what section (8th-grade level or below), then
     ` ([more](area/{year}-W{week}.md#so-what))` linking to that file's So what section. `—` if
     nothing from the area made the top 3.
   - **File** — a markdown link to this week's dated file for that area (e.g. `[2026-W33](ai-engineering/2026-W33.md)`), or `—` if it wasn't in the top 3.

**Leave the "📁 Previous weeks" archive pointer in place** — it sits directly under the
`## 🗓️ This Week` heading, *above* the blockquote. It lists the focus-area directories so readers can
find earlier weeks, and it is not week-specific. Do not rewrite, move, or drop it.

Do not keep prior weeks in the blockquote or table — the dated files under each folder are the archive.

**Never touch the `<!-- TRENDS:START -->` / `<!-- TRENDS:END -->` block.** It sits directly *below*
the focus-area table, so both things you rewrite come before it — stop at the table and leave the
markers, and everything between them, exactly as they are. It is regenerated by
`scripts/render_trends.py` from the ledger below: editing it by hand will just be overwritten, and
re-deriving those counts by reading the archive would blow the run's turn cap.

The same goes for the **`<!-- FOLLOWUPS:START -->` / `<!-- FOLLOWUPS:END -->` block** below it:
`scripts/followups.py` regenerates it from [`data/follow-ups.csv`](data/follow-ups.csv). Change the
ledger, never the block.

## Log the week's items (the trend ledger)

For **every item you publish**, append one row to [`data/trends.csv`](data/trends.csv):

```
week,date,area,topic,headline,url
2026-W38,2026-09-10,ai-engineering,models,"DeepSeek-V4.1-Flash absorbs V4-Pro API traffic",https://...
```

- `week` — the ISO week given to you in the prompt. `date` — when the thing happened, not when you found it.
- `headline` — short, quoted. `url` — the same primary link used in the write-up.
- Append it in the **same step you commit that area's file**. Do this from your existing shell call —
  it should cost no extra research and no extra turns.

## Follow-ups (dated commitments)

[`data/follow-ups.csv`](data/follow-ups.csv) is how the knowledge base remembers dates between weeks:
comment deadlines, expected filings, trial readouts, effective dates. The workflow reads it for you and
lists in the prompt whatever is overdue or coming due soon, so you don't need to open it to find out.

```
due,item,area,source,status,added_week,closed_week
2026-10-19,"FDA comment period closes on ...",healthcare,https://...,open,2026-W34,
```

- **Add a row** for each new dated commitment you meet in this week's research, and only when a source
  states the date. `due` is an ISO date, or `TBD` when the event is announced but not scheduled.
  `status` is `open`. `added_week` is this week. Append it in the same shell call as the trends.csv row.
- **Close a row** by setting `status` to `done` (it happened) or `dropped` (withdrawn, cancelled,
  superseded) and `closed_week` to this week, and only when you have a source for that. A deadline
  simply passing is not a reason to close it: say what happened, or leave it open for next week.
- **Never delete a row.** The closed rows are the history.
- The ledger doesn't earn extra budget. Check on a follow-up only if it's a plausible top-3 item
  anyway, or if it turns up in research you were already doing.

### Topic vocabulary — closed list, exactly one per item

Pick the single **primary** topic. If nothing fits, use `other` — do **not** invent a new tag, and do
not combine tags (`regulation / product / funding` is what this list exists to prevent). Adding a
topic means editing this list first.

**`ai-engineering`**

| Topic | Covers |
| --- | --- |
| `models` | Frontier/open-weight releases, licensing, pricing, deprecations |
| `agents` | Coding agents, harnesses, runtimes, orchestration, eval harnesses |
| `skills-tooling` | Skills, plugins, MCP, manifests, registries, SDKs |
| `context` | Memory, retrieval/RAG, context-window engineering |
| `infra` | Serving, local inference, compilers, cost/performance plumbing |
| `clinical-ml` | Track 2 — productionizing healthcare/clinical models |

**`healthcare`**

| Topic | Covers |
| --- | --- |
| `fda` | Device/drug authorization, guidance, clearances, recalls, agency leadership |
| `payment` | CMS rules, coverage, reimbursement, Medicare/Medicaid, prior authorization |
| `enforcement` | DOJ/state AG/OCR/FTC actions, settlements, litigation, HIPAA |
| `clinical-ai` | AI and digital-health products, deployments, and consent/disclosure |
| `trials` | Clinical and translational readouts |
| `market` | Funding, M&A, IPOs, layoffs, business moves |

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
