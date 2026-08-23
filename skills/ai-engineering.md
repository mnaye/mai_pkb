# Research Skill — AI Engineering

A focused source guide for the `ai-engineering/` area. The weekly brief loads this when researching AI engineering.

## Goal

Surface the most notable **new** AI-engineering work from the past 7 days along two tracks:

1. **Agentic coding & harnessing** — new/updated GitHub repositories for coding agents, agent harnesses, orchestration frameworks, tool-use / MCP tooling, eval harnesses, and agent runtimes. **Prioritize repos with a lot of stars** (established, high-signal projects) and fast-rising new repos gaining stars quickly.
2. **Productionizing healthcare models** — AI-engineering techniques for taking healthcare/clinical ML models to production: deployment, monitoring, evaluation, guardrails, RAG over clinical data, fine-tuning, privacy/compliance (HIPAA/PHI), MLOps. **Prioritize major GitHub repos with a lot of stars _and_ published articles/papers.**

## How to research

### Track 1 — GitHub repos (agentic coding / harnessing)

1. Check **GitHub Trending** and **star-sorted search**:
   - Trending: https://github.com/trending (and `?since=weekly`), languages Python / TypeScript
   - Search sorted by stars, recently pushed, e.g.:
     - https://github.com/search?q=agent+coding&type=repositories&s=stars&o=desc
     - https://github.com/search?q=AI+agent+harness&type=repositories&s=stars&o=desc
     - https://github.com/search?q=MCP+server&type=repositories&s=stars&o=desc
   - Also queries for: `coding agent`, `autonomous agent`, `agent framework`, `agent orchestration`, `tool use`, `LLM eval harness`.
2. For each candidate, **fetch the repo page** to read the real name, description, star count, and last-updated date.
3. **Star threshold:** favor repos with **1k+ stars**, or clearly fast-rising newcomers (hundreds of stars gained this week). Note the star count in the write-up.

### Track 2 — Productionizing healthcare models (repos + articles)

1. **GitHub:** star-sorted search for healthcare/clinical ML infra, e.g.:
   - https://github.com/search?q=clinical+LLM&type=repositories&s=stars&o=desc
   - queries: `healthcare machine learning production`, `medical LLM`, `clinical NLP`, `MLOps healthcare`, `medical RAG`.
2. **Articles & papers:** fetch recent, citable pieces on productionizing healthcare ML:
   - **arXiv** — https://arxiv.org/list/cs.LG/recent and https://arxiv.org/list/cs.CL/recent (filter for clinical/medical + deployment/eval)
   - **Papers with Code** — https://paperswithcode.com
   - **Hugging Face blog** — https://huggingface.co/blog
   - Engineering blogs: **Google Research / Health**, **Microsoft Research**, **NVIDIA (Clara/MONAI)**, **Nature Digital Medicine**, **NEJM AI**
3. Prefer items that pair an **implementation (repo)** with a **write-up (article/paper)**.

## Priority sources

- **GitHub** — Trending, star-sorted repository search (the core of this skill)
- **arXiv** (cs.LG, cs.CL, cs.AI), **Papers with Code**
- **Hugging Face** blog & trending models
- **Nature Digital Medicine**, **NEJM AI**, **The Lancet Digital Health** (for healthcare-model production)
- Vendor/lab engineering blogs: Anthropic, OpenAI, Google, Microsoft, NVIDIA MONAI

## What to capture per item

- **Name / repo / title** (bold)
- One-line description — what it does and why it matters
- **Star count** (for repos) and **last updated / published date**
- **Link** to the fetched source

## Guardrails

- **Only include repos/articles you actually fetched** — real star counts, real links, no fabrication.
- For repos, verify recent activity (pushed within the last ~week) so the list stays current, not just perennially-popular projects with no news.
- Prefer primary sources (the repo, the paper, the official blog) over roundups.
- Attribute curation to **Mai with Claude**.
