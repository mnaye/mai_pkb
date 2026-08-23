# GOVERNOR.md — bounding what the weekly agent spends

The weekly research agent runs on Mai's **Claude Pro** subscription via
`CLAUDE_CODE_OAUTH_TOKEN`. That means it draws from the *same* 5-hour usage window as
interactive Claude Code sessions on her laptop. An unbounded agentic run can quietly
eat the whole window — which is exactly what happened on
[run 32623239367](https://github.com/mnaye/mai_pkb/actions/runs/32623239367): the session
limit was reached mid-run, the job failed, and **nothing was committed**.

The governor is the set of controls that keeps one run inside a predictable envelope, and
makes a run that *does* get cut short still leave something behind.

> **Coming from Azure DevOps?** A workflow ≈ a pipeline, `uses:` ≈ a task, `concurrency:`
> ≈ a pipeline-level "batch / only one run at a time" setting, and `timeout-minutes:` is
> the same idea as the ADO job timeout. There's no ADO equivalent for the model-budget
> layers — those are specific to running an LLM agent in CI.

## The four layers

### 1. Hard caps — the workflow can't exceed these

| Control | Where | Effect |
| --- | --- | --- |
| `--max-turns` | `claude_args` | The agent is stopped after N turns, full stop. |
| `timeout-minutes: 25` | job level | The runner kills the job on wall clock. |
| `concurrency: weekly-research` | workflow level | Two runs can never overlap and double-spend. |
| Already-published guard | `Plan the run` step | Re-runs no-op if this week's files already exist. |

### 2. Soft budget — what the agent is *told* to spend

The prompt hands the agent a per-area cap on `WebSearch` and `WebFetch` calls, plus a
"land the plane" instruction. The skills in [`skills/`](skills/) say *where* to look; the
governor says *how much*. Where they conflict, the governor wins — that precedence is
written into [`research-brief.md`](research-brief.md#run-budget-the-governor) too, so the
agent sees it from both directions.

### 3. Narrow scope — the biggest lever

The knowledge base tracks **two** focus areas, `ai-engineering` and `healthcare`, and every
run covers both. Scope is the cheapest thing to control and the most expensive thing to get
wrong: each additional area is another full round of searching, scraping, and writing.

`sea-food-culture` and `data-science` were dropped on 2026-08-23 — they had never published
anything, so nothing was lost. To bring an area back, add its slug to `GOV_AREAS`, restore
its `skills/` guide, and list it in `research-brief.md`.

### 4. Accounting — so the dials can be tuned on evidence

Every run appends a row to [`.governor/run-log.csv`](.governor/run-log.csv) and writes the
same numbers to the GitHub Actions job summary:

```
date,run_id,week,areas,model,conclusion,turns,cost_usd,duration_s,denials,note
```

The `note` column is the useful one — it says *why* the run ended:
`ok`, `hit turn cap (20)`, `hit Claude usage limit`, or `failed (…)`. That maps directly
onto which dial to turn.

## Durability: the run must survive being killed

The agent is instructed to **commit after each area** rather than saving all writing for
the end. A run that dies at turn 18 of 20 then still publishes one area's research instead
of nothing. This is the single most important instruction in the prompt.

Backing it up: a **Tuesday 09:00 UTC retry cron**. The already-published guard makes it a
no-op if Monday's run landed. If Monday died on a usage limit, Tuesday picks the week up.

## Turning the dials

Everything tunable is in the `env:` block at the top of
[`.github/workflows/weekly-research.yml`](.github/workflows/weekly-research.yml):

```yaml
env:
  GOV_MODEL: claude-opus-5
  GOV_MAX_TURNS: '20'
  GOV_SEARCHES_PER_AREA: '4'
  GOV_FETCHES_PER_AREA: '6'
  GOV_AREAS: 'ai-engineering healthcare'
```

**If runs keep hitting the usage limit,** in order of leverage:

1. Switch `GOV_MODEL` to `claude-sonnet-5` — by far the largest reduction in quota draw,
   and this task (search → scrape → summarize) sits well within Sonnet's range.
2. Drop `GOV_FETCHES_PER_AREA` — page fetches are the most token-expensive calls, since
   each one pulls a whole article into context.
3. Drop `GOV_MAX_TURNS`.
4. Move the cron away from hours when Mai is likely to be using Claude Code herself —
   the two share one window, so an overlap is what makes a limit hit likely.
5. Cut `GOV_AREAS` to one area. Last resort — it halves the output, not just the cost.

**Manual runs** (Actions → Weekly Research → Run workflow) take two inputs:

- `areas` — comma-separated slugs, to override the focus areas for one run (e.g. `healthcare`).
- `force` — run even if this week already published.

## What is *not* governed

- **Token spend inside a single turn.** A turn that fetches a huge page is expensive and
  no cap sees it; the fetch budget is the proxy control.
- **The Pro window itself.** There's no API to ask "how much budget is left" before
  starting, so the governor can't pre-flight the check — it can only bound the request and
  handle the failure gracefully.
