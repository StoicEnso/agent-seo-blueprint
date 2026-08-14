---
title: Full-Funnel Rollout (BOFU → MOFU → TOFU, adversarial)
goal: Take an existing master/strategy plan + its live data and produce the operational full-funnel rollout — wave-by-wave BOFU→MOFU→TOFU sequencing with entry/exit/KILL gates, the down-funnel handoff plumbing, channel roles, KPIs, and an honest forecast — via an adversarial multi-agent cascade.
playbooks:
  - references/playbooks/content/full-funnel-rollout.md
  - references/playbooks/foundations/adversarial-agent-orchestration.md
  - references/playbooks/research/winnability-and-serp-regimes.md
  - references/playbooks/maintenance/ai-overviews-and-serp-features.md
  - references/playbooks/research/number-reconciliation.md
  - references/playbooks/research/search-intent.md
scripts:
  - scripts/funnel_rollout_cascade.mjs   # the adversarial rollout pipeline (Workflow-tool script)
  - scripts/forecast.py                  # single-pass click-curve + AIO-haircut forecast
integrations: [ahrefs, serp]
outputs:
  - <plan-dir>/SEO-FULL-FUNNEL-ROLLOUT.md   # the operational rollout (extends the master plan)
  - analysis/funnel-map.json                # every cluster → stage + win_mechanism + down-funnel role
---

# Full-Funnel Rollout (BOFU → MOFU → TOFU, adversarial)

**When to run this.** A master/strategy plan already exists (e.g. from `full-master-plan.md`), and the user wants the operational rollout — "plan how we roll out BOFU, then mid, then top of funnel", "sequence the whole funnel", "add a full-funnel rollout". This EXTENDS the plan; it does not regenerate it. Uses the **Workflow tool** (multi-agent) and reads the SAVED data + the canonical plan from disk.

**The non-negotiable framing (read [full-funnel-rollout](../references/playbooks/content/full-funnel-rollout.md) first).** "Roll out TOFU" ≠ "resurrect the TOFU spam the plan already killed". TOFU re-enters ONLY as (a) an AIO-safe hosted artifact/tool, (b) brand + LLM-citation/SOAV measured as reach/assist, or (c) genuine link bait — built LAST, capped, EEAT-gated, **never a revenue line**, each with a concrete path DOWN to the money page. If the user says "not TOFU for the sake of TOFU", this is already the rule.

## Step 1 — Confirm inputs exist

You need, on disk: the canonical plan markdown (the master/strategy doc), the killed-ideas record (graveyard) if one exists, and the live data the plan was built on (`keywords.csv`, `serp_summary.json` + `serp/*.json` with DR/UR + features, `overviews.json`, `clusters.json`, `competition.json`). If SERP-feature data is missing for forecast-bearing terms, pull it first (`ahrefs-keywords-explorer` → `node scripts/ke-headless.mjs serp "<kw>"`) — the AIO playbook makes it mandatory before forecasting.

## Step 2 — Run the rollout cascade

```
Workflow({ scriptPath: ".../agent-seo-blueprint/scripts/funnel_rollout_cascade.mjs", args: {
  dataDir: "<plan-dir>/data", serpDir: "<plan-dir>/data/serp", analysisDir: "<plan-dir>/analysis",
  playbooks: ".../agent-seo-blueprint/references/playbooks",
  canonicalPlan: "<plan-dir>/SEO-STRATEGY-V2.md",   // the existing plan to extend
  graveyard:     "<plan-dir>/IDEAS-GRAVEYARD.md",    // killed ideas (no-resurrection guard)
  outFile:       "<plan-dir>/SEO-FULL-FUNNEL-ROLLOUT.md",
  brand, product, niche, seedKeyword, geos
}})
```

Pipeline (≈16 agents): **Funnel map** (every cluster → stage + win_mechanism + AIO + down-funnel role; writes `analysis/funnel-map.json`) → **5 divergent strategists** (cashflow-first · moat-led · demand-ladder · brand/GEO-AIO · portfolio-kill-gates) → **3-judge panel** (score + steal) → **synthesis** (writes the rollout doc) → **5 red-teamers** (numbers · AIO/double-haircut · policy+graveyard · funnel-coherence · sequencing) → **finalize** (applies must-fixes + appends a "what the red-team changed" log). See [adversarial-agent-orchestration](../references/playbooks/foundations/adversarial-agent-orchestration.md).

## Step 3 — If the run goes quiet, RESUME (don't assume it hung)

A ~25–30-min background cascade can be silently killed by a host/sandbox suspend (tell-tale: a big clock jump in the workflow file mtimes + a dangling "started" with no "result" in the journal, and the task no longer tracked). Recover:

```
Workflow({ scriptPath: ".../scripts/funnel_rollout_cascade.mjs", resumeFromRunId: "<runId>" })
```

The unchanged agent prefix (funnel map + strategies) returns cached results instantly; it continues from the first incomplete agent.

## Step 4 — Verify the OUTPUT FILE + the numbers (REQUIRED)

- **The file:** synthesis agents sometimes rename the output. Confirm `outFile` actually exists at the exact path and contains the "What the red-team changed" section; if not, find the renamed file (`find . -iname '*funnel*'`) and rename/re-run finalize.
- **The numbers:** spot-recompute 2–3 headline figures from `keywords.csv`; confirm the forecast chain actually multiplies out (the 10× trap) and the AIO haircut is applied once. If the red-team flagged the same error in the *canonical plan*, surface it to the user — do not silently edit the canonical plan.
- **The discipline:** TOFU carries no revenue line and every upper-funnel play has a named down-funnel path; no graveyard-killed idea reappears; caps + content-diff gates respected.

## Step 5 — Wire it in + commit

Link the new rollout doc from the plan's README and from the master/strategy doc's roadmap section. Commit to the project repo. (Irreversible actions — publishing, outreach — stay DRAFT-only.)
