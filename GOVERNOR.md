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
| `--max-turns` | `claude_args` | **Assertion, not a brake** — see below. |
| `timeout-minutes: 25` | job level | The runner kills the job on wall clock. **The only true hard stop.** |
| `concurrency: weekly-research` | workflow level | Two runs can never overlap and double-spend. |
| `--disallowedTools Task` | `claude_args` | No subagents. |
| Already-published guard | `Plan the run` step | Re-runs no-op if this week's files already exist. |

**`--max-turns` does not stop the run.** Measured, not assumed: run 32644519184 was
configured with `--max-turns 20`, ran to **27 turns**, reported `subtype: success`, and
committed all its work — and *then* the action failed the step with *"Claude reported a
successful result after 27 turns, exceeding the configured maximum of 20."* So the cap
behaves as a post-hoc assertion by the action wrapper, not a mid-run brake. Two consequences:

- Budget with **`timeout-minutes`**, which the runner genuinely enforces. `--max-turns` is a
  tripwire that tells you afterwards that a run misbehaved.
- Set it *above* what the search/fetch budget arithmetically implies, or every healthy run
  goes red. 2 areas x (5 searches + 4 fetches) = 18 research turns, plus reading the brief
  and skills, writing 2 files and the README, and 3 commits — about 27. A cap of 20 was
  internally contradictory with the budget on the very same page, which is exactly what
  happened.

**Why `--disallowedTools Task` is not redundant.** `--allowedTools` is *additive* — it adds
to Claude Code's built-in default tool set rather than replacing it
([claude-code#62608](https://github.com/anthropics/claude-code/issues/62608)), so listing
six tools does **not** deny the rest. Subagents are the worst case for this budget: each is
a fresh context that re-reads files, and `--max-turns` bounds the parent loop, not the turns
burned inside a child. Denying `Task` is the only thing that actually stops it.

### 2. Soft budget — what the agent is *told* to spend

The prompt hands the agent a per-area cap on `WebSearch` (5) and `WebFetch` (4) calls, plus
a "land the plane" instruction. Fetches are capped tighter than searches because a fetch
pulls a whole article into context — it is the token-heaviest thing the agent does, and the
first dial to turn.

Unlike layer 1, **these are advisory**. The agent reads them and generally complies, but
nothing enforces them; only the turn cap, the timeout, and the tool denials are hard. The skills in [`skills/`](skills/) say *where* to look; the
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

| `note` | Meaning |
| --- | --- |
| `ok` | Clean run. |
| `overran turn cap (N/M) — research OK` | Claude finished and committed; the action red-X'd on the assertion. Raise `GOV_MAX_TURNS`. |
| `stopped at turn cap (M)` | The SDK actually halted it mid-run. Work may be incomplete. |
| `hit Claude usage limit` | The Pro 5-hour window ran out. Tuesday's retry picks it up. |
| `claude OK; action failed` | Research succeeded, the wrapper failed for some other reason — read the step log. |
| `failed (…)` | Genuine failure. |

**Watch `cost_usd`, not `turns`.** The 27-turn run cost $1.35 — turns are a poor proxy for
spend, because a turn can be a one-line file write or a full article fetch.

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
  GOV_MAX_TURNS: '35'
  GOV_SEARCHES_PER_AREA: '5'
  GOV_FETCHES_PER_AREA: '4'
  GOV_AREAS: 'ai-engineering healthcare'
```

### Measured baseline

| Run | Scope | Turns | Cost | Duration | Outcome |
| --- | --- | --- | --- | --- | --- |
| First (pre-governor) | 4 areas | 20 | **$5.16** | ~10 min | Green, but committed nothing (5 permission denials) |
| 32623239367 | 4 areas | — | — | 4m37s | Failed — Pro session limit reached |
| 32644519184 | 2 areas | 27 | **$1.35** | 3m16s | Research committed; red X on the turn assertion |

Roughly a **74% cost reduction**, driven mostly by the scope cut. `modelUsage` also shows
Claude Code routing some internal work to Haiku 4.5 on its own — page-fetch summarization
already runs on a cheap model without being asked.

**If runs keep hitting the usage limit,** in order of leverage:

1. Switch `GOV_MODEL` to `claude-sonnet-5` — by far the largest reduction in quota draw,
   and this task (search → scrape → summarize) sits well within Sonnet's range.
2. Drop `GOV_FETCHES_PER_AREA` — page fetches are the most token-expensive calls, since
   each one pulls a whole article into context. Below 3 per area it gets hard to honor the
   "primary sources" accuracy rule.
3. Drop `timeout-minutes` — the only cap that actually interrupts a run mid-flight.
   Lowering `GOV_MAX_TURNS` does *not* reduce spend; it just red-X's the job afterwards.
4. Move the cron away from hours when Mai is likely to be using Claude Code herself —
   the two share one window, so an overlap is what makes a limit hit likely.
5. Cut `GOV_AREAS` to one area. Last resort — it halves the output, not just the cost.

**Manual runs** (Actions → Weekly Research → Run workflow) take two inputs:

- `areas` — comma-separated slugs, to override the focus areas for one run (e.g. `healthcare`).
- `force` — run even if this week already published.

## Considered, not built

Three ideas that resolve to a single change — **splitting the run into a cheap `gather`
phase and an expensive `publish` phase, handing off through a committed candidates file**:

- run candidate collection on a cheaper model, ranking and writing on a stronger one;
- save intermediate research so a failed run resumes instead of restarting;
- keep research from touching the weekly index, so an incomplete run cannot corrupt it.

Deferred deliberately until `.governor/run-log.csv` has rows in it. Tuning six dials before
seeing where the turns actually go is guesswork, and the split roughly doubles the
workflow's complexity. The resume behavior is the piece most likely to be worth it.

Its real cost, if built: the editorial call — *is this worth Mai's attention* — happens
during gathering, on the cheaper model. The stronger model would only rank what the cheaper
one chose to surface.

## What is *not* governed

- **Token spend inside a single turn.** A turn that fetches a huge page is expensive and
  no cap sees it; the fetch budget is the proxy control.
- **The Pro window itself.** There's no API to ask "how much budget is left" before
  starting, so the governor can't pre-flight the check — it can only bound the request and
  handle the failure gracefully.
