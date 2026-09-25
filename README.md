<div align="center">

# 🧠 mai_pkb

### My Personal Knowledge Base

*A living record of the latest research, ideas, and industry trends worth tracking.*

![Updated Weekly](https://img.shields.io/badge/updated-weekly-brightgreen)
![Curated by Mai with Claude](https://img.shields.io/badge/curated%20by-Mai%20with%20Claude-8A2BE2)
![Focus Areas](https://img.shields.io/badge/focus%20areas-2-blue)

</div>

---

## 🗓️ This Week

**📁 Previous weeks:** every brief is archived as a dated file (`{year}-W{week}.md`) inside its focus-area directory — browse either folder to read back through the weeks:

- [`ai-engineering/`](ai-engineering/) — all AI Engineering briefs
- [`healthcare/`](healthcare/) — all Healthcare briefs

> **This week's research brief (2026-W39):** No frontier model landed this week, and the through-line across the top three is **verification as the scarce resource** — who checks the machine's output, and who is allowed to stop checking. **FDA published a final order on 17 September denying** a petition (from Harrison.ai) that would have exempted radiology **computer-aided detection, diagnosis and triage software** from 510(k) review, holding that the case for skipping premarket notification was not made and that manufacturers of the largest, most commercially mature AI device category **must keep clearing every product**. On the engineering side the same instinct shows up voluntarily: **`cloudflare/security-audit-skill`** took the biggest weekly star gain on GitHub (**+14,864 to 18,717**) for a design that assumes the agent hallucinates and routes every finding to a *different* agent that tries to disprove it. And **`JustVugg/colibri`** (**36,739 ★, +7,441**) moves the frontier in the other direction — a dependency-free C engine streaming MoE experts off NVMe to run 744B–2.8T-parameter models on a desktop, trading throughput for access.

<!-- TRENDS:START -->

### 📈 Topic trends — rolling 13 weeks

`2026-W27` → `2026-W39` · **6 weeks published** · **31 items** · ranked by volume, counted from [`data/trends.csv`](data/trends.csv).

**🤖 AI Engineering** — 17 items

<table>
<tr><th align="right">#</th><th align="left">Topic</th><th align="left">Trend</th><th align="right">Items</th><th align="left">Last seen</th></tr>
<tr><td align="right"><sub>1</sub></td><td><b><code>skills-tooling</code></b></td><td><img src="https://placehold.co/96x12/9BD3F0/9BD3F0.png" alt="7" height="12"></td><td align="right"><b>7</b></td><td><a href="ai-engineering/2026-W39.md"><sub>2026-W39</sub></a></td></tr>
<tr><td align="right"><sub>2</sub></td><td><code>infra</code></td><td><img src="https://placehold.co/41x12/9BD3F0/9BD3F0.png" alt="3" height="12"><img src="https://placehold.co/55x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>3</b></td><td><a href="ai-engineering/2026-W39.md"><sub>2026-W39</sub></a></td></tr>
<tr><td align="right"><sub>3</sub></td><td><code>agents</code></td><td><img src="https://placehold.co/41x12/9BD3F0/9BD3F0.png" alt="3" height="12"><img src="https://placehold.co/55x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>3</b></td><td><a href="ai-engineering/2026-W36.md"><sub>2026-W36</sub></a></td></tr>
<tr><td align="right"><sub>4</sub></td><td><code>models</code></td><td><img src="https://placehold.co/27x12/9BD3F0/9BD3F0.png" alt="2" height="12"><img src="https://placehold.co/69x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>2</b></td><td><a href="ai-engineering/2026-W38.md"><sub>2026-W38</sub></a></td></tr>
<tr><td align="right"><sub>5</sub></td><td><code>context</code></td><td><img src="https://placehold.co/27x12/9BD3F0/9BD3F0.png" alt="2" height="12"><img src="https://placehold.co/69x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>2</b></td><td><a href="ai-engineering/2026-W34.md"><sub>2026-W34</sub></a></td></tr>
<tr><td align="right"><sub>6</sub></td><td><code>clinical-ml</code></td><td><img src="https://placehold.co/96x12/E7EDF3/E7EDF3.png" alt="0" height="12"></td><td align="right"><b>0</b></td><td><sub>—</sub></td></tr>
</table>

**🏥 Healthcare** — 14 items

<table>
<tr><th align="right">#</th><th align="left">Topic</th><th align="left">Trend</th><th align="right">Items</th><th align="left">Last seen</th></tr>
<tr><td align="right"><sub>1</sub></td><td><b><code>fda</code></b></td><td><img src="https://placehold.co/96x12/9BD3F0/9BD3F0.png" alt="4" height="12"></td><td align="right"><b>4</b></td><td><a href="healthcare/2026-W39.md"><sub>2026-W39</sub></a></td></tr>
<tr><td align="right"><sub>2</sub></td><td><code>trials</code></td><td><img src="https://placehold.co/72x12/9BD3F0/9BD3F0.png" alt="3" height="12"><img src="https://placehold.co/24x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>3</b></td><td><a href="healthcare/2026-W38.md"><sub>2026-W38</sub></a></td></tr>
<tr><td align="right"><sub>3</sub></td><td><code>clinical-ai</code></td><td><img src="https://placehold.co/48x12/9BD3F0/9BD3F0.png" alt="2" height="12"><img src="https://placehold.co/48x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>2</b></td><td><a href="healthcare/2026-W38.md"><sub>2026-W38</sub></a></td></tr>
<tr><td align="right"><sub>4</sub></td><td><code>market</code></td><td><img src="https://placehold.co/48x12/9BD3F0/9BD3F0.png" alt="2" height="12"><img src="https://placehold.co/48x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>2</b></td><td><a href="healthcare/2026-W37.md"><sub>2026-W37</sub></a></td></tr>
<tr><td align="right"><sub>5</sub></td><td><code>enforcement</code></td><td><img src="https://placehold.co/48x12/9BD3F0/9BD3F0.png" alt="2" height="12"><img src="https://placehold.co/48x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>2</b></td><td><a href="healthcare/2026-W36.md"><sub>2026-W36</sub></a></td></tr>
<tr><td align="right"><sub>6</sub></td><td><code>payment</code></td><td><img src="https://placehold.co/24x12/9BD3F0/9BD3F0.png" alt="1" height="12"><img src="https://placehold.co/72x12/E7EDF3/E7EDF3.png" alt="" height="12"></td><td align="right"><b>1</b></td><td><a href="healthcare/2026-W37.md"><sub>2026-W37</sub></a></td></tr>
</table>

<details open>
<summary><b>What each topic covers</b></summary>
<table>
<tr><th align="left">Area</th><th align="left">Topic</th><th align="left">Covers</th></tr>
<tr><td rowspan="6"><sub><b>🤖 AI Engineering</b></sub></td><td><code>models</code></td><td><sub>Frontier and open-weight releases, licensing, pricing, deprecations</sub></td></tr>
<tr><td><code>agents</code></td><td><sub>Coding agents, harnesses, runtimes, orchestration, eval harnesses</sub></td></tr>
<tr><td><code>skills-tooling</code></td><td><sub>Skills, plugins, MCP, manifests, registries, SDKs</sub></td></tr>
<tr><td><code>context</code></td><td><sub>Memory, retrieval/RAG, context-window engineering</sub></td></tr>
<tr><td><code>infra</code></td><td><sub>Serving, local inference, compilers, cost and performance plumbing</sub></td></tr>
<tr><td><code>clinical-ml</code></td><td><sub>Productionizing healthcare and clinical models</sub></td></tr>
<tr><td rowspan="6"><sub><b>🏥 Healthcare</b></sub></td><td><code>fda</code></td><td><sub>Device and drug authorization, guidance, clearances, recalls, agency leadership</sub></td></tr>
<tr><td><code>payment</code></td><td><sub>CMS rules, coverage, reimbursement, Medicare/Medicaid, prior authorization</sub></td></tr>
<tr><td><code>enforcement</code></td><td><sub>DOJ, state AG, OCR and FTC actions, settlements, litigation, HIPAA</sub></td></tr>
<tr><td><code>clinical-ai</code></td><td><sub>AI and digital-health products, deployments, consent and disclosure</sub></td></tr>
<tr><td><code>trials</code></td><td><sub>Clinical and translational readouts</sub></td></tr>
<tr><td><code>market</code></td><td><sub>Funding, M&amp;A, IPOs, layoffs, business moves</sub></td></tr>
<tr><td><sub><b>either</b></sub></td><td><code>other</code></td><td><sub>Nothing in the list fits — one primary topic per item, and never invent a new one</sub></td></tr>
</table>
</details>

<!-- TRENDS:END -->

| Focus Area | Summary | File |
| --- | --- | --- |
| 🤖 AI Engineering | **`cloudflare/security-audit-skill`** posts the week's largest star gain (**+14,864 → 18,717 ★**) on an adversarial design where the agent that checks a finding is never the one that found it; **`colibri`** (**36,739 ★, +7,441**) runs Kimi K3 and GLM-5.2 class MoE models off NVMe in pure C at 1–7 tok/s. | [2026-W39](ai-engineering/2026-W39.md) |
| 🏥 Healthcare | **FDA denied the 510(k) exemption petition** for radiology CAD/CADe/CADx and triage software (91 FR 58817, effective 17 Sep) — premarket review stays for the biggest AI device category; separately **all 50 states, DC and Puerto Rico applied** to CMS's most-favored-nation **GENEROUS** Medicaid drug-pricing model ($64.3B / 10 yrs). | [2026-W39](healthcare/2026-W39.md) |

*(Claude replaces the brief and table each week; the archive pointer under the heading stays.)*

---

## 🎯 Focus Areas

| Area | What I'm tracking |
| --- | --- |
| 🤖 **AI Engineering** | Models, tooling, frameworks, and practical patterns for building with AI |
| 🏥 **Healthcare Trends** | Regulatory change first (FDA, CMS, HHS, legislation) — then industry moves, market movement, and research |

---

## 📌 Purpose

This repo is where I collect and organize notes, papers, articles, and takeaways as I follow these topics over time. It's a growing reference for myself — not a polished publication.

---

## 🔄 Updates

> This knowledge base is **updated weekly by Claude** and published with summaries of the **top 3 developments** each week — the most notable research and industry moves worth knowing. Deliberately narrow: two focus areas, both covered every week, inside a bounded per-run budget (see [GOVERNOR.md](GOVERNOR.md)).

---

## 🗂️ Structure

Notes are organized by focus area. *(More structure to come as the knowledge base grows.)*

```
mai_pkb/
├── .github/workflows/
│   └── weekly-research.yml   # the weekly trigger + the governor's dials
├── research-brief.md         # what to research + output format (the "brain")
├── skills/                   # per-area source guides
├── GOVERNOR.md               # how each run's spend is bounded
├── .governor/run-log.csv     # turns / cost / outcome, one row per run
├── CLAUDE.md                 # standing conventions
├── 🤖 ai-engineering/        # AI models, tools, and engineering practices
└── 🏥 healthcare/            # Healthcare regulation, industry trends, and research
```

Each week, Claude drops a dated file (`{area}/{year}-W{week}.md`) for the top items and refreshes the **This Week** section above.

---

## ⚙️ How the automation works

A scheduled research agent — no laptop cron or server needed. GitHub hosts everything.

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'ui-sans-serif, system-ui, -apple-system, sans-serif','fontSize':'13px','lineColor':'#94a3b8'},'flowchart':{'curve':'basis','nodeSpacing':40,'rankSpacing':70,'padding':14}}}%%
flowchart LR
    subgraph S1[" ⏰ TRIGGER "]
        direction TB
        CRON["🗓️ Weekly cron<br/>Mondays 09:00 UTC"]
        RETRY["🔁 Retry cron<br/>Tuesdays · no-ops if Monday landed"]
        MANUAL["👆 Run workflow<br/>manual dispatch"]
    end

    subgraph S2[" 🎛️ GOVERNOR "]
        direction TB
        PLAN["📋 Plan the run<br/>ISO week · scope<br/>skip if already published"]
        CAPS["🚧 Hard caps<br/>max-turns · timeout<br/>concurrency · budget"]
    end

    subgraph S3[" 🤖 AGENT "]
        direction TB
        CLAUDE["Claude Code · headless<br/>claude-code-action<br/>WebSearch · WebFetch · Read · Write · git"]
    end

    subgraph S4[" 📚 OUTPUT "]
        direction TB
        FILES["📄 Dated briefs<br/>area/YYYY-Www.md"]
        RDME["📌 README<br/>This Week table"]
    end

    BRAIN[["🧠 THE BRAIN<br/>research-brief.md · CLAUDE.md · skills/*.md"]]
    WEB{{"🌐 WEB SOURCES<br/>GitHub · arXiv · FDA / CMS / HHS · health media"}}
    REPO[("✅ git repo<br/>commit after each area")]
    LOG[("📊 run-log.csv<br/>turns · cost · outcome")]

    CRON   --> PLAN
    RETRY  --> PLAN
    MANUAL --> PLAN
    PLAN   -->|"➊ scope + ISO week"| CAPS
    CAPS   -->|"➋ launch under caps"| CLAUDE
    BRAIN  -.->|"➌ loads instructions"| CLAUDE
    CLAUDE <-->|"➍ search · scrape"| WEB
    CLAUDE -->|"➎ writes"| FILES
    CLAUDE -->|"➏ refreshes"| RDME
    FILES  --> REPO
    RDME   --> REPO
    CLAUDE -.->|"➐ accounting"| LOG

    classDef trig  fill:#fef3c7,stroke:#f59e0b,stroke-width:1.5px,color:#78350f;
    classDef gov   fill:#e2e8f0,stroke:#64748b,stroke-width:1.5px,color:#1e293b;
    classDef agent fill:#ede9fe,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95;
    classDef brain fill:#e0f2fe,stroke:#0ea5e9,stroke-width:1.5px,color:#075985;
    classDef web   fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#14532d;
    classDef out   fill:#ffe4e6,stroke:#f43f5e,stroke-width:1.5px,color:#881337;
    classDef store fill:#f1f5f9,stroke:#475569,stroke-width:1.5px,color:#0f172a;

    class CRON,RETRY,MANUAL trig;
    class PLAN,CAPS gov;
    class CLAUDE agent;
    class BRAIN brain;
    class WEB web;
    class FILES,RDME out;
    class REPO,LOG store;

    style S1 fill:#fffbeb,stroke:#f59e0b,stroke-width:2px,color:#78350f;
    style S2 fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#1e293b;
    style S3 fill:#faf5ff,stroke:#8b5cf6,stroke-width:2px,color:#4c1d95;
    style S4 fill:#fff1f2,stroke:#f43f5e,stroke-width:2px,color:#881337;
```

**⏰ Trigger** — [`.github/workflows/weekly-research.yml`](.github/workflows/weekly-research.yml) fires on a cron (Mondays 09:00 UTC), with a Tuesday retry and a manual **Run workflow** button.

➊ **Plan the run** — resolves this week's ISO week, scope, and dated filenames, and skips the whole run if the week already published.<br/>
➋ **Launch under caps** — starts **`anthropics/claude-code-action`** headless with the areas, the ISO week, and a per-area search/fetch budget, bounded by a hard turn cap and job timeout.<br/>
➌ **Load the Brain** — Claude reads [`research-brief.md`](research-brief.md), [`CLAUDE.md`](CLAUDE.md), and the per-area guides in [`skills/`](skills/).<br/>
➍ **Research** — WebSearch and WebFetch against the sources each skill prioritizes, until the budget is spent.<br/>
➎➏ **Write** — the dated brief for each area, then this README's *This Week* table — **committing after each area**, so a run cut short still publishes what it finished.<br/>
➐ **Accounting** — records turns, cost, and why the run ended in [`.governor/run-log.csv`](.governor/run-log.csv) and the job summary.

See [GOVERNOR.md](GOVERNOR.md) for the dials and how to turn them.

### One-time setup

1. Push this repo to GitHub.
2. Generate a Claude Code token: run **`claude setup-token`** locally (uses your Claude Pro/Max subscription — no API billing).
3. Add it as a repo secret named **`CLAUDE_CODE_OAUTH_TOKEN`** (Settings → Secrets and variables → Actions).
4. Run **`/install-github-app`** from Claude Code (installs the GitHub App; needs repo admin).
5. Open the **Actions** tab → **Weekly Research** → **Run workflow** to test without waiting for Monday.

### Two decisions to make

- **Auto-commit vs. review:** the workflow commits straight to `main`. To sanity-check first, have the brief open a **pull request** instead — then your weekly ritual is merging one PR.
- **Topic scope:** two areas, both covered weekly. To add or drop one, change `GOV_AREAS` in the workflow and the area list in `research-brief.md` (and add a `skills/` guide for anything new).

---

## ✍️ Conventions

- 📄 One topic per note where practical
- 🔗 Link related notes to build connections over time
- 🏷️ Capture the source and date for anything worth citing later
- 🚫 Never invent links or facts — primary sources only

<div align="center">

---

*Curated by Mai with Claude.* 💜

</div>
