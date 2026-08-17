# agent-seo-blueprint

A comprehensive, **agentic SEO skill** for Claude Code (and compatible agents). It pairs a distilled SEO
**methodology** — mirrored from a full SEO course and made searchable — with **runnable pipelines** that execute that
methodology against live data (Ahrefs, Google Search Console, GA4, live SERP, PageSpeed/Lighthouse) and write artifacts
into a per-project workspace.

Think of it as two planes that reference each other:

1. **Knowledge layer** — 36 distilled, original-wording playbooks covering the entire course (62 lessons, proven
   coverage), operational article-production QA, directory/entity-submission, and 37-check SEO coverage playbooks,
   plus a searchable course index so any agent can answer
   *"what does the course say about X?"* and pull the right playbook.
2. **Pipeline layer** — 11 workflows total: 5 core pipelines, 4 operational deep dives, and 2 end-to-end planning
   workflows that compose those
   playbooks, drive the data integrations, summon customer-persona subagents for ideation, and produce concrete
   deliverables.

> **Self-contained:** clones and runs with **no API keys and no `pip install`** — data access and full-text search are
> optional add-ons. Independent reimplementation; not affiliated with, sponsored by, or endorsed by any course author.

---

## Table of contents

- [Highlights](#highlights)
- [How it works](#how-it-works)
- [Repository layout](#repository-layout)
- [The knowledge layer](#the-knowledge-layer-59-playbooks)
- [The workflows](#the-workflows-11-runbooks)
- [Data integrations](#data-integrations)
- [ICP persona subagents](#icp-persona-subagents)
- [Scripts reference](#scripts-reference)
- [Per-project workspace](#per-project-workspace)
- [Install](#install)
- [Quick start](#quick-start)
- [Self-contained design & the private `_source/`](#self-contained-design--the-private-_source)
- [Guardrails](#guardrails)
- [Extending the skill](#extending-the-skill)
- [Methodology, attribution & license](#methodology-attribution--license)

---

## Highlights

- **Searchable course brain** — `search_course.py "<topic>"` ranks all 62 lessons (titles, intent aliases, takeaways,
  summaries) and returns the matching **distilled playbooks** to read. Natural phrasing works: *"niche to build a
  startup"*, *"latent semantic keywords"*, *"keyword gap analysis"*.
- **59 playbooks**: 36 original course distillations plus 23 operational additions for article QA, schema/E-E-A-T,
  programmatic patterns, authority acquisition, technical maintenance, GSC opportunity mining, Google-only AI visibility,
  cross-platform citation evidence, deterministic planning, SERP-regime grading, and adversarial rollout design;
  `coverage-map.md` proves all 62 lessons map to at least one course-derived playbook.
- **11 workflows**: five core pipelines, four operational deep dives, and two end-to-end planning workflows for a full
  SEO master plan and a BOFU→MOFU→TOFU rollout.
- **8 integration references** covering Ahrefs, GSC, GA4, live SERP, PageSpeed/Lighthouse, DataForSEO, CWV thresholds, and public social research.
- **ICP persona subagents** — summon Opus subagents that role-play ideal customers to ideate content angles, surface the
  exact phrases people search, and pressure-test niches.
- **Per-project workspace** — config + dated artifacts (audits, keyword maps, briefs, source packets, drafts,
  content-QA reports, monitoring history, outreach).
- **Zero dependencies** — every script is Python 3 standard library only. **No `pip install`, no API key required** to
  start.

---

## How it works

```
User intent ─▶ SKILL.md (router)
                  │
                  ├─▶ "what does the course say about X?" ─▶ scripts/search_course.py ─▶ lessons + playbooks
                  │
                  └─▶ a job (research / content / audit / authority / monitoring)
                          │
                          ├─ resolve/create the per-project workspace (scripts/workspace.py)
                          ├─ load the relevant playbooks for the *method*  (references/playbooks/…)
                          ├─ pull live data (scripts/*  ⇄  references/integrations/*)
                          ├─ (optional) summon ICP persona subagents (agents/…)
                          └─ write artifacts to the workspace (scripts/report.py ⇄ assets/ templates)
```

Workflows **orchestrate**; playbooks hold the **method**. This keeps concepts in one place and lets pipelines stay thin.

---

## Repository layout

```
SKILL.md                       # intent router + how-to-use (the entry point)
DESIGN.md                      # architecture & design spec
README.md                      # this file
references/
  playbooks/                   # 36 course distillations + 23 operational additions
    research/        (11)       # keyword research, intent, metrics, winnability, number reconciliation…
    content/         (17)       # programmatic SEO, schema/E-E-A-T, image search, funnel rollout, articles…
    authority/       (14)       # editorial intent, directories, Wikipedia research, affiliate, outreach…
    foundations/     (5)        # SEO philosophy/process + official AI guidance + adversarial orchestration
    maintenance/     (12)       # updates, ROI, technical SEO, SERP features, and platform-scoped AI evidence
  course-index/
    course-index.json          # searchable index: 62 lessons → summary, takeaways, aliases, playbooks
    course-index.md            # human-readable mirror (6 chapters, 62 lessons)
  integrations/                # 8 source/threshold references, including DataForSEO, CWV, and public social research
  coverage-map.md              # proof: every lesson → its playbook(s)
workflows/                     # 5 core pipelines + 4 operational deep dives + 2 planning workflows
  research-and-ideation.md  content-production.md  site-audit.md
  authority-and-links.md    monitoring.md         technical-seo-maintenance.md
  geo-audit.md              category-citation-loop.md
  ai-answer-visibility-loop.md
  full-master-plan.md       full-funnel-rollout.md
agents/
  icp-persona.md               # launcher template for ONE persona subagent
  synthesizer.md               # merges N persona outputs into ranked insights
  personas/                    # reusable persona library + 2 examples
scripts/                       # Python 3 stdlib only — no pip deps
  search_course.py  workspace.py  report.py            # core
  ahrefs_client.py  gsc_pull.py  ga4_pull.py           # data (API or browser fallback)
  dataforseo_client.py  serp_capture.py  pagespeed_run.py
  forecast.py  master_plan_workflow.mjs  master_plan_cascade.mjs  funnel_rollout_cascade.mjs
  prompt_panel.py  social_fetch.py  geo_metrics.py  rank_social_opportunities.py  approval_queue.py
assets/                        # fill-in templates emitted into the workspace
  audit-report.md  content-brief.md  keyword-map.csv
  directory-discovery-sources.csv  directory-submission-tracker.csv
  startup-backlink-candidates.csv  # 146 source mentions → 141 unverified research leads
  outreach-email.md  monitoring-snapshot.md
_source/                       # PRIVATE, gitignored — paid-course transcripts (NOT in this repo)
```

---

## The knowledge layer (59 playbooks)

Each playbook is original wording with a consistent shape: **What it is · When to use · Method · Decision criteria /
heuristics · Example · Pitfalls · Related**. Frontmatter tags the `source_lessons` and any `tools` it uses.

**research/** — `keyword-fundamentals` · `search-intent` · `match-and-exceed` · `seo-metrics` ·
`keyword-research-tools` · `finding-and-validating-niches` · `competitor-research` · `keyword-to-sitemap` ·
`research-for-existing-sites` · `number-reconciliation` · `winnability-and-serp-regimes`

**content/** — `content-fundamentals` · `content-types-overview` · `cross-platform-commercial-intent-distribution` ·
`programmatic-seo` · `free-tools-strategy` · `content-pages` · `landing-pages` · `articles` · `content-rings` ·
`on-page-optimization` · `content-what-not-to-do` · `image-search-optimization` · `agent-article-production-qa` ·
`programmatic-pattern-library` · `full-funnel-rollout` · `eeat-framework` · `schema-types-reference`

**authority/** — `understanding-authority` · `link-stealing` · `editorial-link-intent-and-assets` · `affiliate-programs` ·
`acquiring-domain-authority` · `haro` · `manual-outreach` · `building-an-audience` · `content-rings-for-links` ·
`directory-submissions` · `startup-backlink-directory-submissions` · `wikipedia-dead-link-building` ·
`other-link-building` · `linkbuilding-what-not-to-do`

**foundations/** — `seo-philosophy` · `seo-and-ai-future` · `google-generative-ai-search-official` ·
`seo-process-overview` · `adversarial-agent-orchestration`

**maintenance/** — `navigating-google-updates` · `keyword-intent-evolution` · `staying-ahead-with-backlinks` ·
`measuring-seo-results` · `seo-operational-checklist` · `technical-seo-maintenance` ·
`gsc-position-4-20-opportunity-mining` · `google-generative-ai-visibility` · `ai-search-commerce-readiness` ·
`cloudflare-agent-readiness-and-aeo` · `cross-platform-ai-citation-loop` · `ai-overviews-and-serp-features`

> **Flagship play:** proactive niche discovery — mining search data for a low-KD, buildable gap with a real LSI cluster
> behind it, to build a product/startup around. See `research/finding-and-validating-niches.md` (the Ahrefs data-dump
> hunt + validation gauntlet + cluster sizing + walk-away rules).

---

## The workflows (11 runbooks)

Each runbook has frontmatter (`goal`, `playbooks`, `scripts`, `integrations`, `outputs`) and concrete numbered steps.

| Workflow | What it does | Key outputs |
|---|---|---|
| **research-and-ideation** | niche find/validate → keyword research → competitor gaps → match-and-exceed → keyword→sitemap; can summon ICP personas | keyword map CSV, sitemap plan |
| **content-production** | content-type selection → brief → optional cross-platform commercial-intent map → optional evidence packet, article draft, anti-slop rewrite, lint, bounded QA | content brief; optional distribution map, source packet, review draft, QA report |
| **site-audit** | technical + on-page + content + opportunity + authority audit | prioritized, severity-ranked fix list |
| **authority-and-links** | pick tactics → ranked opportunity list → **drafted** outreach (never auto-sent) | opportunity list, outreach drafts |
| **monitoring** | rank/traffic snapshots + GSC 4–20 opportunities + optional Google AI, Cloudflare agent/AEO, and provider citation evidence + update response + ROI measurement | ordinary-search, opportunity, and separated AI-evidence snapshots |
| **technical-seo-maintenance** | recurring indexation, crawlability, schema, CWV, rendering, and hygiene review | evidence ledger and prioritized maintenance report |
| **geo-audit** | Platform-scoped AI-search audit with official Google eligibility/reporting plus optional Cloudflare and provider-specific citation lanes | readiness report and raw findings |
| **category-citation-loop** | choose a truthful category phrase, build evidence, and monitor platform-specific buyer-question citations | category/citation baseline and loop plan |
| **ai-answer-visibility-loop** | freeze buyer questions, measure provider-separated answer visibility, collect public social evidence, and build a human approval queue | answer metrics, social candidates, non-executing approval queue |
| **full-master-plan** | build an evidence-grounded end-to-end SEO plan; use the adversarial cascade for exhaustive work | master plan, executive summary, source data, reconciled forecast |
| **full-funnel-rollout** | extend an existing plan into gated BOFU→MOFU→TOFU delivery waves | rollout plan, funnel map, entry/exit/kill gates |

---

## Data integrations

Each source has a reference doc (`references/integrations/<src>.md`) covering **what it provides**, the **API path**
(env-var auth + endpoints), the **browser-fallback procedure** (driven by Claude's Chrome integration when no key is
present), rate limits/ToS notes, and the **JSON output shape** that plugs into `report.py`.

| Source | Script | API? | Notes |
|---|---|---|---|
| Ahrefs | `scripts/ahrefs_client.py` | API if `AHREFS_API_KEY`, else browser | site explorer, keywords, backlinks, content gap |
| Google Search Console | `scripts/gsc_pull.py` + browser export | API/browser for ordinary Search; browser/export for limited-rollout AI report | clicks/impressions/positions plus separate Google AI impression snapshots |
| GA4 | `scripts/ga4_pull.py` | API if creds, else browser | traffic & conversions for ROI |
| Live SERP | `scripts/serp_capture.py` | browser only (Chrome) | match-and-exceed, intent, content-type research |
| PageSpeed / Lighthouse | `scripts/pagespeed_run.py` | public API (key optional) | Core Web Vitals for audits |
| DataForSEO | `scripts/dataforseo_client.py` | API if `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD` | bulk keywords, SERPs, backlinks, and structured research |
| Public social research | `scripts/social_fetch.py` | Reddit RSS/Atom in v0.1 | public thread/search evidence; read-only, cached, no authentication |

The skill **never** enters passwords or completes OAuth itself — it directs you to log in / authorize, then reads the
session. Secrets are referenced by env-var name in the workspace `project.json`, never stored in plaintext.

---

## ICP persona subagents

- `agents/icp-persona.md` — launcher template for one persona; fill the `{{PLACEHOLDERS}}` (persona, context, the
  product/niche). Dispatch **3–6 in parallel** via the Agent tool with `model=opus` for divergent ideation.
- `agents/synthesizer.md` — merges the persona outputs into ranked content angles, intent-clustered keyword seeds, and
  a niche-validation verdict. Feeds the research-and-ideation workflow.
- `agents/personas/` — reusable persona library (README + two distinct examples).

Each persona surfaces jobs-to-be-done, pains, the literal queries they'd type (short- and long-tail), buying triggers,
objections, where they hang out, and willingness-to-pay signals.

---

## Scripts reference

All Python 3 standard library only. Every script supports `--help`.

```bash
# Course search — "what does the course say about X"
python3 scripts/search_course.py "programmatic seo"            # lessons + playbooks
python3 scripts/search_course.py "haro" --json                 # machine-readable
python3 scripts/search_course.py "user intent" --full          # also search transcripts (needs local _source/)

# Per-project workspace
python3 scripts/workspace.py status --path ./seo-workspace/mysite
python3 scripts/workspace.py init  --path ./seo-workspace/mysite --name mysite --domain mysite.com --niche "ai tools"
python3 scripts/workspace.py show  --path ./seo-workspace/mysite

# Render artifacts (templates in assets/)
python3 scripts/report.py keywords   --workspace ./seo-workspace/mysite --data keywords.json   # → CSV
python3 scripts/report.py audit      --workspace ./seo-workspace/mysite --title "Audit" --data findings.json
python3 scripts/report.py monitoring --workspace ./seo-workspace/mysite --data snapshot.json

# Data sources (API where available, else they print the browser-fallback procedure)
python3 scripts/pagespeed_run.py https://example.com           # public API, no key needed
python3 scripts/ahrefs_client.py overview --domain example.com # needs AHREFS_API_KEY, else browser fallback
python3 scripts/serp_capture.py "ai headshot generator"        # prints the Chrome capture procedure
python3 scripts/dataforseo_client.py --help                     # bulk structured SEO data when credentials exist
python3 scripts/forecast.py --help                              # deterministic click-curve + AIO-haircut forecast
python3 scripts/prompt_panel.py panel.csv --json                # validate a versioned buyer-question panel
python3 scripts/social_fetch.py fetch <reddit-thread-url>       # normalized public Reddit evidence
python3 scripts/geo_metrics.py answer-runs.jsonl --brand acme   # provider-separated answer metrics
```

---

## Per-project workspace

One folder per site holds `project.json` (domains, niche, competitors, data-source config, monitoring settings) plus
dated artifacts in `audits/ keywords/ briefs/ monitoring/ outreach/ research/`. Workflows always resolve the workspace
first and **ask before creating one** if none exists.

---

## Install

```bash
git clone https://github.com/StoicEnso/agent-seo-blueprint.git ~/.claude/skills/agent-seo-blueprint
```

The skill is then available to Claude Code immediately. Verify:

```bash
cd ~/.claude/skills/agent-seo-blueprint
python3 scripts/search_course.py "find a niche to build a startup"
python3 scripts/workspace.py status --path ./seo-workspace
```

No `pip install`. No API key required to start.

---

## Quick start

Ask the agent things like:

- *"What does the course say about programmatic SEO?"* → search returns the lessons + `content/programmatic-seo.md`.
- *"Find me a buildable niche to start a product around."* → runs `research-and-ideation` (the data-dump hunt + validation).
- *"Do a keyword-gap analysis for mysite.com vs competitorA.com, competitorB.com."* → Ahrefs Content Gap → triaged keyword map.
- *"Audit mysite.com's SEO."* → `site-audit` → prioritized, severity-ranked fix list.
- *"Find link opportunities for mysite.com."* → `authority-and-links` → opportunity list + drafted outreach (you approve before sending).
- *"Set up weekly rank/traffic monitoring."* → `monitoring` → snapshots + optional schedule.
- *"Which pages appear in Google AI Overviews or AI Mode?"* → `monitoring` + `google-generative-ai-visibility` → impression-only page/country/date/device evidence with limitations.
- *"What does Cloudflare show about agent access, AI citations, and operator traffic?"* → `geo-audit` or `monitoring` + `cloudflare-agent-readiness-and-aeo` → three separate evidence lanes with access state and limitations.
- *"Show me how ChatGPT/Copilot/Perplexity/Claude cite us for buyer questions."* → `geo-audit` or `category-citation-loop` + `cross-platform-ai-citation-loop` → provider-specific observation sets with separated metrics.
- *"Track AI answers and find relevant Reddit discussions without posting."* → `ai-answer-visibility-loop` → a versioned question panel, public social evidence, separated metrics, ranked research candidates, and a non-executing approval queue.
- *"Which queries rank in positions 4–20 and are worth improving?"* → `monitoring` + `gsc-position-4-20-opportunity-mining`.
- *"Audit whether my product data and checkout are ready for AI agents."* → `geo-audit` + `ai-search-commerce-readiness`.
- *"Set up a recurring technical SEO maintenance pass."* → `technical-seo-maintenance`.

---

## Self-contained design & the private `_source/`

This repo is **self-contained**: a fresh clone validates and runs (search, workspace, report, all data scripts) with no
extra setup. What's *not* shipped is the paid-course **transcripts** — they are private and never redistributed.

- The included `references/course-index/` provides summaries, key takeaways, and playbook links, so search and routing
  work fully **without** transcripts.
- Only `search_course.py --full` (transcript full-text search) needs a local `_source/transcripts/`, and it degrades
  gracefully when absent.
- If you own the course, drop your own `.txt` per lesson (named `<chapter>-<lesson>_<slug>.txt`) into
  `_source/transcripts/` to enable `--full`. See `_source/SOURCE.md`.

---

## Guardrails

- **Irreversible actions** (publishing content, sending outreach/email, submitting forms, disavow uploads) are **drafted
  only** and require explicit user confirmation. Nothing is auto-sent or auto-published.
- **AI-search evidence** stays provider-specific: Google AI impressions remain separate from cross-platform citation observations, and neither dataset implies clicks, CTR, conversions, revenue, or a universal GEO score.
- **Cross-platform citation tactics** must stay truthful: no fabricated mentions, spam, fake discussion, or undisclosed influence. The vendor-authored 14.7K Copilot-citation field claim is treated only as unverified input, never as a benchmark or causal proof.
- **SERP/Google reads** are for personal research — modest volume, respect bot detection, never bypass CAPTCHAs.
- **Auth** is always performed by you (login/OAuth); the skill reads the authorized session and never handles passwords.

---

## Extending the skill

1. Add a playbook under `references/playbooks/<area>/` using the standard frontmatter + section shape.
2. Map it to its lesson(s) in `references/course-index/course-index.json` (and add `aliases` for searchability).
3. Reference it from the relevant `workflows/*.md`.
4. Validate: `python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py .`

---

## Methodology, attribution & license

The methodology is **distilled in original wording** from a paid SEO course. Methods, processes, and facts are not
copyrightable; the course **transcripts themselves are not included** and are never redistributed. Everything shipped
here (playbooks, index summaries, workflows, scripts) is original synthesis. Not affiliated with, sponsored by, or
endorsed by the course author.

**License:** MIT — see [`LICENSE`](LICENSE). Covers the original work in this repo (playbooks, course index, workflows,
scripts, templates). Course transcripts are not included and are not covered.
