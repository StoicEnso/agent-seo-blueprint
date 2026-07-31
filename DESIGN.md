# Design Spec — `agent-seo-blueprint` Skill

**Date:** 2026-05-20
**Status:** Approved design, pre-implementation
**Author/owner:** ihusanadam (StoicEnso)

---

## Context

The user completed Danny Postma's "SEO Blueprint" course (62 lessons, fully archived + transcribed at
`~/Library/Mobile Documents/com~apple~CloudDocs/Courses/Danny Postma - SEO Blueprint/`). They want that knowledge
turned into **one comprehensive Claude skill** so that:

1. **Any agent** can access the course's content, ideas, and playbooks (knowledge available on demand, and *searchable* —
   "what does the course say about keyword finding?" should return the relevant lessons **and** the distilled playbook).
2. The skill can **actually do the work** — agentic pipelines that drive Ahrefs, Google Search Console, GA4, live SERP
   scraping, and PageSpeed/Lighthouse against real sites, writing artifacts into a per-project workspace.
3. **ICP persona subagents** (Opus) can be summoned to explore use cases, surface content angles, and pressure-test
   niche/keyword ideas.

Decisions locked during brainstorming:
- **Execution model:** both agentic *and* playbook/methodology.
- **Target:** general-purpose consultant tool (works on any site/niche; no hardcoded site).
- **Data access:** Ahrefs **API with browser fallback**; plus GSC, GA4, live SERP+page scraping, PageSpeed/Lighthouse.
- **Course material handling:** **hybrid** — full 1-for-1 distilled playbooks in original wording (shareable), PLUS a
  **gitignored `_source/`** holding the transcripts, linked to the iCloud archive. "All the course covers, in full."
- **Output:** **per-project workspace** — skill uses an existing one if provided, else asks/creates one.
- **Monitoring:** asks at setup, recommends cadence; provides runbooks + pipelines for both on-demand and scheduled.
- **Architecture:** two-layer (knowledge + pipelines) **plus** a searchable course mirror and ICP persona subagents.
  No size constraints — "as big as needed."

### Intended outcome
A self-contained skill at `~/.claude/skills/seo-blueprint/` that any Claude agent can invoke to (a) answer SEO questions
grounded in the course, (b) run end-to-end SEO workflows against live data, and (c) ideate via persona subagents — all
while keeping the paid source material private and the distilled methodology shareable.

---

## Non-goals (YAGNI)

- Not a hosted service, web app, or dashboard. It's a Claude skill (markdown + scripts).
- Not redistributing Danny's transcripts. `_source/` is gitignored and private; only original distillations ship.
- Not auto-publishing content or sending outreach without explicit user confirmation (respect irreversible-action gates).
- No paid API is *required* — every integration has a browser fallback so the skill works with web subscriptions alone.

---

## Architecture overview

```
~/.claude/skills/seo-blueprint/
├── SKILL.md                        # thin intent router + how-to-use + workspace bootstrap
├── DESIGN.md                       # this file
├── references/
│   ├── playbooks/                  # LAYER 1: distilled, original, 1-for-1 methodology
│   │   ├── research/               #   niches, keywords, intent, match-and-exceed, metrics, tools...
│   │   ├── content/                #   content types, programmatic SEO, free tools, pages, on-page...
│   │   ├── authority/              #   link stealing, HARO, verified directories, affiliate, outreach, content rings...
│   │   └── maintenance/            #   volatility, updates, intent, measurement, operational coverage...
│   ├── course-index/               # mirrored, searchable course
│   │   ├── course-index.json       #   62 lessons: title, summary, takeaways, →playbook, →transcript
│   │   └── course-index.md         #   human-readable mirror (chapter/lesson outline + links)
│   ├── integrations/               # LAYER 3 docs: what each source gives + how to auth
│   │   ├── ahrefs.md  gsc.md  ga4.md  serp.md  pagespeed.md
│   └── coverage-map.md             # all 62 lessons → playbook(s) that cover them (full-coverage proof)
├── workflows/                      # LAYER 2: job-oriented runbooks (compose playbooks + tools)
│   ├── research-and-ideation.md
│   ├── content-production.md
│   ├── site-audit.md
│   ├── authority-and-links.md
│   └── monitoring.md
├── agents/                         # ICP persona subagents (Opus)
│   ├── icp-persona.md              #   persona role-play template (launcher prompt)
│   ├── synthesizer.md              #   merges N persona outputs into ranked insights
│   └── personas/                   #   optional saved persona library
├── scripts/                        # executable helpers (Python, venv-based)
│   ├── search_course.py            #   query index + transcripts → lessons + playbooks
│   ├── ahrefs_client.py            #   API client + browser-fallback reader
│   ├── gsc_pull.py  ga4_pull.py  serp_capture.py  pagespeed_run.py
│   ├── workspace.py                #   find/create per-project workspace + project.json
│   └── report.py                   #   render audit/keyword/brief artifacts from data
├── assets/                         # templates + source-lead research assets
│   ├── audit-report.md  content-brief.md  keyword-map.csv  outreach-email.md  monitoring-snapshot.md
│   └── startup-backlink-candidates.csv # 127 source mentions → 122 unverified leads
└── _source/                        # GITIGNORED: transcripts + link to iCloud archive (private authority)
    └── .gitignore                  # ignores everything here
```

### Layer 1 — Knowledge base (mirrored + searchable)
- **Playbooks** (`references/playbooks/`): each course concept distilled into an original, agent-readable playbook —
  what it is, when to use it, step-by-step method, decision criteria, examples, pitfalls. Each playbook header carries
  `source_lessons:` tags. Written in *our own words* (facts/processes aren't copyrightable) so the skill is shareable.
- **Course index** (`references/course-index/`): one entry per lesson (all 62), mirroring the 6 chapters. Fields:
  `chapter, lesson, title, summary, key_takeaways[], playbook (path), transcript (path in _source/)`.
- **Search** (`scripts/search_course.py`): keyword + fuzzy/semantic search over the index and transcripts. Returns the
  matching lessons (with short quotes ≤15 words for grounding) **and** the linked playbook(s). This is the
  "what does the course say about X" entry point.
- **`_source/`** (gitignored): the txt/srt transcripts (copied or symlinked from the iCloud archive) plus a pointer file
  to the archive path. Private. Used by search and as the authority for distillation.
- **`coverage-map.md`**: matrix of all 62 lessons → playbook(s) covering them — the explicit "in full" guarantee.

### Layer 2 — Pipelines / workflows (`workflows/`)
Each runbook is a numbered procedure: prerequisites → which playbooks to load → which scripts/tools to run → decision
points → artifacts to emit (into the workspace). The five:
1. **research-and-ideation** — niche finding/validation, keyword research, competitor gap analysis, match-and-exceed,
   keyword→sitemap planning. Can summon ICP personas for divergent ideation.
2. **content-production** — content-type selection, programmatic SEO planning, free-tool page design, landing pages,
   articles, content rings, and on-page optimization; emits content briefs and, when explicitly requested, an
   evidence packet, review draft, and bounded content-QA report.
3. **site-audit** — technical + on-page + content audit of a live site → prioritized, severity-ranked fix list.
4. **authority-and-links** — link stealing, HARO, affiliate, manual outreach, content rings → opportunity lists +
   drafted outreach (never sent without confirmation).
5. **monitoring** — ordinary rank/traffic snapshots, optional impression-only Google AI visibility snapshots,
   Google-update detection/response, and "is it paying off" measurement; on-demand plus optional scheduled (via the
   `schedule`/`loop` skills) with a recommended cadence chosen at setup.

Operational additions compose around these five core pipelines: `technical-seo-maintenance.md`, `geo-audit.md`, and
`category-citation-loop.md` are bounded deep-dive runbooks that route findings back into the core workflows. The 37-check
SEO ledger routes evidence across audit/research/content/monitoring, the startup backlink asset feeds the directory/entity
verification path, and Google Generative AI impression evidence remains a separate monitoring layer with explicit
metric/rollout limitations. None of these artifacts turns heuristics, DR snapshots, `site:` counts, or AI impressions
into business facts; live verification and external-write approval gates still apply.

### Layer 3 — Tooling & data (`scripts/` + `references/integrations/`)
- **Ahrefs**: `ahrefs_client.py` uses the API when a key is in project config; otherwise drives the logged-in Ahrefs web
  app via Chrome MCP and reads the UI. Reference doc covers both auth paths.
- **Google Search Console / GA4**: API when credentials present, browser fallback otherwise. Ordinary GSC Search
  Analytics and the limited-rollout, browser/export-only Generative AI impression report use separate data contracts;
  neither is allowed to imply cross-platform AI visibility or causality.
- **Live SERP + page scraping**: `serp_capture.py` browser-reads Google results for match-and-exceed + intent analysis;
  on-page extractor pulls competitor page structure.
- **DataForSEO**: `dataforseo_client.py` provides credential-gated, structured keyword/SERP/backlink data for bulk work;
  secrets stay in environment variables and the helper never prints them.
- **PageSpeed/Lighthouse**: `pagespeed_run.py` (API or CLI) for Core Web Vitals in the audit; `cwv-thresholds.md` keeps
  current field/lab thresholds and interpretation boundaries centralized.
- Each integration ships a reference doc: what data it provides, how to authenticate, browser-fallback steps, rate
  limits, and which workflows/playbooks consume it.

### ICP persona subagents (`agents/`)
- `icp-persona.md`: a launcher/template that instantiates an **Opus subagent** role-playing a specific ideal-customer
  profile. Given a niche/product, the persona surfaces: jobs-to-be-done, pain points, the exact phrases they'd search,
  objections, and willingness-to-pay signals.
- The skill summons **N personas in parallel** (divergent), then `synthesizer.md` merges + ranks the insights into
  content angles, keyword seeds, and niche validation verdicts.
- Consumed by research-and-ideation and content-production workflows. `personas/` can store reusable persona definitions.

### Per-project workspace
- Every workflow first resolves a workspace via `scripts/workspace.py`:
  - If the user names/points to one, use it.
  - Else look for `./seo-workspace/<project>/`; if none, **ask** the user before creating.
- Contents: `project.json` (domain(s), niche, Ahrefs workspace/API key ref, GSC property, GA4 property id, locale),
  plus dated artifacts: audit reports, keyword maps (CSV), content briefs, source packets, review drafts, content-QA
  reports, monitoring history, outreach lists.
- `project.json` schema documented in a reference; secrets referenced by env-var name, never stored in plaintext.

### Routing (`SKILL.md`)
- Thin and fast: detects intent (research / content / audit / authority / monitoring / "what does the course say…") →
  routes to the right workflow or to course-search → loads only the playbooks + integration docs that step needs
  (progressive disclosure; never load everything at once).
- Documents workspace bootstrap, the course-search command, and the persona-summoning entry point.

---

## How the build itself will run (implementation approach)

1. **Scaffold** the directory tree above; add `_source/.gitignore` first so transcripts never get committed.
2. **Populate `_source/`** by copying the 62 `.txt` (and `.srt`) transcripts from the iCloud archive + a pointer file.
3. **Build the course index** programmatically from the existing `_manifest.json` + transcript summaries.
4. **Distill playbooks** via parallel subagents: each reads a cluster of related lesson transcripts and writes an
   original playbook; coverage tracked against the manifest so all 62 lessons map to ≥1 playbook.
5. **Write workflows** that reference the finished playbooks + integration scripts.
6. **Implement scripts** (search first — it's testable immediately; then workspace; then integrations with browser
   fallbacks; API paths gated on credentials).
7. **Author integration reference docs** + the persona templates.
8. **Validate** with `skill-creator`'s `quick_validate.py`; verify the coverage map; smoke-test `search_course.py` and
   one end-to-end workflow (e.g., research-and-ideation on a sample niche).

Built following `skill-creator` conventions (SKILL.md frontmatter, progressive disclosure, references/scripts layout).

---

## Verification / success criteria

- `search_course.py "keyword finding"` returns the correct lessons (e.g., Research 09–12) **and** the linked playbook.
- `coverage-map.md` shows all 62 lessons → ≥1 playbook (0 uncovered).
- Each of the 5 workflows runs end-to-end on a sample project and writes the expected artifacts to the workspace.
- Ahrefs/GSC/GA4/SERP/PageSpeed each work via browser fallback with no API key, and via API when a key is present.
- ICP persona summon produces N persona outputs + a synthesized, ranked insight set.
- `_source/` is gitignored; no transcript text appears in any shippable file.
- `skill-creator/scripts/quick_validate.py` passes on the finished skill.

---

## Open questions / risks

- **Ahrefs API availability** — confirm the user's plan tier supports API; if not, browser fallback is primary. (To
  resolve at implementation start.)
- **GSC/GA4 auth** — OAuth flows must be done by the user (per safety rules); skill guides, never auto-auths.
- **SERP scraping fragility + ToS** — browser reads of Google are for personal research; keep volume modest, respect
  bot-detection, never bypass CAPTCHAs.
- **Playbook fidelity** — distillations must capture the course's actual method, not generic SEO advice; coverage map +
  source_lesson tags + spot-checks against `_source/` mitigate drift.

> Note: spec saved with the skill artifact (not git-committed — `~/.claude` is not a git repo).
