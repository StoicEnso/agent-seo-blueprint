---
title: Full SEO Master Plan (end-to-end, multi-agent)
goal: Turn a niche + a logged-in Ahrefs session into a complete, evidence-grounded SEO master plan (clusters/funnel, competition/SERP-gap, PSEO, content, IA, technical, free-tools, authority, KPI forecast) with every number reconciled from live data.
playbooks:
  - references/playbooks/research/finding-and-validating-niches.md
  - references/playbooks/research/seo-metrics.md
  - references/playbooks/research/search-intent.md
  - references/playbooks/research/winnability-and-serp-regimes.md   # low KD != winnable; win_mechanism per cluster
  - references/playbooks/research/keyword-to-sitemap.md
  - references/playbooks/research/number-reconciliation.md
  - references/playbooks/research/research-for-existing-sites.md    # code/GSC ground-truth for live sites
  - references/playbooks/content/programmatic-seo.md
  - references/playbooks/content/free-tools-strategy.md
  - references/playbooks/authority/understanding-authority.md
  - references/playbooks/maintenance/ai-overviews-and-serp-features.md
  - references/playbooks/maintenance/measuring-seo-results.md
scripts:
  - scripts/master_plan_workflow.mjs   # the packaged Workflow-tool pipeline (standard depth)
  - scripts/master_plan_cascade.mjs    # EXHAUSTIVE/adversarial pipeline: N strategies -> judge -> review (deep mode)
  - scripts/forecast.py                # deterministic click-curve + AIO-haircut forecast
  - scripts/workspace.py
integrations: [ahrefs, serp]
outputs:
  - SEO-MASTER-PLAN.md + 00-EXECUTIVE-SUMMARY.md + 03..08 section files
  - data/keywords.csv + summary.json + overviews.json + serp_summary.json + clusters.json
  - analysis/clusters.json + competition.json + pseo.json
---

# Full SEO Master Plan (end-to-end, multi-agent)

**When to run this.** The user wants the whole thing — "build me an exhaustive SEO plan for X" — not just keyword research. Produces a board-ready master plan grounded in live Ahrefs data. Requires the **Workflow tool** (multi-agent orchestration) and a **logged-in app.ahrefs.com** Chrome session for the data pull.

**The shape: scout inline, then pipeline.** Pull all the data yourself FIRST in one sequential process (never fan parallel agents at Ahrefs — Cloudflare throttles), then run the multi-agent workflow over the SAVED files. The workflow does analysis + writing only; it does not call Ahrefs.

## Step 1 — Pick a date'd output dir + resolve scope

Create `docs/seo-research/<date>/{data,raw}` (or use a workspace via `scripts/workspace.py`). Confirm with the user: brand, product one-liner, the main/seed keyword, target geos (note spelling variants like personalized/personalised), and whether the site is pre-launch (technical = build spec) or live (technical = audit; add PageSpeed/GSC).

**Define the niche STRICTLY.** "AI X" is not "X" — write down what's in-niche vs off-niche (adjacent verticals, generic-tool terms, competitor brands, service-hire intent) before pulling data; you'll commit this as the off-niche prune in `recompute.py`. See [number-reconciliation](../references/playbooks/research/number-reconciliation.md) §7–8.

**Live site that is ALSO a code repo? Ground-truth it in code (read [research-for-existing-sites](../references/playbooks/research/research-for-existing-sites.md) §Step 5).** Before trusting curl/assumptions: read the actual routes + `robots`/`noindex`/sitemap source, **check unmerged branches** for in-progress pSEO, grep for an on-disk **GSC export** (`.seo/`, `Queries.csv`) and use it as the measured baseline, and get **DR from Site Explorer** (never infer it from rankings). Write findings to `analysis/live-site-state.md` + `analysis/authority-and-health.md` so the workflow agents inherit them.

## Step 2 — Pull the data (Ahrefs sweep, rate-safe)

Use the **ahrefs-keywords-explorer** skill. First `node scripts/extract-cookies.mjs`, then `node scripts/ke-headless.mjs selftest` (confirm 10/10 — fix any encoding drift before pulling). Then sweep a seed list spanning the niche (core/product, adjacent, informational, AI/tool, gift/occasion seeds):

```bash
node .../ahrefs-keywords-explorer/scripts/sweep.mjs --seeds seeds.txt \
  --out docs/seo-research/<date> --country us,gb --related --questions --suggestions --overviews
```

Then pull SERPs (with feature/AIO detection) for BOTH the money terms AND the top forecast-bearing TOFU terms — the AIO playbook makes TOFU SERP evidence MANDATORY before forecasting:

```bash
for kw in "<money1>" "<money2>" "<tofu1>" "<tofu2>"; do
  node .../ke-headless.mjs serp "$kw" > docs/seo-research/<date>/data/serp/"$kw".json; done
```

Verify: `data/keywords.csv` has thousands of rows; `serp_summary.json` carries real DR/UR + `features`; `overviews.json` has `byCountry`. If SERP fields are null, the parser/encoding drifted — run `selftest`.

## Step 3 — Run the master-plan workflow

```
Workflow({ scriptPath: ".../agent-seo-blueprint/scripts/master_plan_workflow.mjs", args: {
  dir: "docs/seo-research/<date>",
  dataDir: ".../<date>/data", analysisDir: ".../<date>/analysis", rawDir: ".../<date>/raw",
  playbooks: ".../agent-seo-blueprint/references/playbooks",
  brand, product, niche, seedKeyword, geos
}})
```

Pipeline (≈17 agents): **Analyze data** (cluster/funnel map ∥ competition/SERP-gap ∥ PSEO sizing ∥ persona design) → **ICP personas** (role-play ∥, then synthesize angles) → **Strategy modules** (content, IA, technical, free-tools, authority, KPI — each writes its section) → **Synthesize plan** (number-reconciliation critic → master synthesis writes the exec summary, master plan, README).

**Before assigning page types, grade WINNABILITY (read [winnability-and-serp-regimes](../references/playbooks/research/winnability-and-serp-regimes.md)).** Low KD ≠ winnable — KD is blind to SERP features. From the live SERPs, tag each cluster's `win_mechanism` (blue_link / image_pack / aio_citation / local_pack) and build the format that mechanism rewards (render/gallery for image_pack, NOT a thin text page). The standard `master_plan_workflow.mjs` does this in its competition agent; if you ran an older pass that assigned text pages to image-pack SERPs, fix it.

**EXHAUSTIVE / "fully explore this" mode → use `master_plan_cascade.mjs` instead.** When the user wants the niche fully exhausted ("come to the best plan", "explore every angle", "cascade ideas"), run the cascade pipeline: 4 foundation analysts (clean clusters ∥ winnability map ∥ exhaustive non-thin pSEO ∥ competitor teardown) → **5 divergent strategists** (pSEO-maximalist · tool/product-led · visual/image-pack engine · local domination · topical-authority/GEO) → **3-judge panel** → synthesis (writes `analysis/recompute.py`) → **4–5 adversarial reviewers** (numbers ∥ winnability ∥ thin-page/scaled-content ∥ niche discipline ∥ code ground-truth) → final plan + exec summary. Same args as the standard script. Same scout-then-pipeline rule — pull data first.

**One reproducible `recompute.py`.** The synthesis must write a single `analysis/recompute.py` (one source file, one off-niche prune, stated filters) that EVERY headline regenerates from; the adversarial pass re-runs it. No figure ships that isn't in its output. See [number-reconciliation](../references/playbooks/research/number-reconciliation.md) §7–8.

## Step 4 — Close the forecast loop deterministically

Don't let the KPI agent hand-arithmetic the headline number. Feed the prioritized clusters + PSEO families to `scripts/forecast.py` as pools (`volume,kd,intent,aio,capture_share`); it applies the AI-Overview haircut and emits base + downside at 3/6/12/18 months:

```bash
python3 scripts/forecast.py --in pools.json --aio-haircut 0.5
```

## Step 5 — Verify before delivering (REQUIRED)

- **Numbers:** spot-recompute 3–4 headline figures from `keywords.csv` (see `number-reconciliation.md`). If any can't be reproduced, fix it before shipping.
- **Links:** every TOC link in `SEO-MASTER-PLAN.md` resolves to an existing file in the same dir.
- **Forecast honesty:** informational pools carry the AIO haircut; measured and projected figures are labelled and never summed.
- **Coverage:** exec summary, content, IA, technical, free-tools, authority, KPI, and a risk/resilience + measurement section all present.

**Guardrails.** Irreversible actions (publishing, outreach) stay DRAFT-only. SERP/Ahrefs reads are modest-volume personal research. Every load-bearing number must be reproducible from the source data — no exceptions.

## Next — operational rollout

Once the plan exists and the user wants the operating sequence ("roll out BOFU, then mid, then top of funnel"), run **[full-funnel-rollout.md](./full-funnel-rollout.md)** (`scripts/funnel_rollout_cascade.mjs`): it extends this plan into a wave-by-wave BOFU→MOFU→TOFU rollout with entry/exit/KILL gates and the down-funnel handoff plumbing — TOFU as reach/citation only, built last, never a revenue line.
