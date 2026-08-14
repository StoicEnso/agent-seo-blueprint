---
title: Number Reconciliation — Every Load-Bearing Figure Must Be Reproducible
area: research
source_lessons: []  # process guardrail learned from multi-agent master-plan runs
tools: [ahrefs]
---

# Number Reconciliation — Every Load-Bearing Figure Must Be Reproducible

**What it is.** A guardrail for any data-driven SEO deliverable, especially multi-agent ones. LLM agents **fabricate and drift on aggregates** — a clustering agent will confidently write "53 terms / 12,060 volume" when the data shows 28 / 7,500. Left unchecked, these numbers propagate into the executive summary and the forecast, and the whole plan becomes untrustworthy. The rule: **every load-bearing number must be recomputed from the source file by a command, and reconciled once by a separate pass.**

**Why it matters.** A plan's credibility is its numbers. One fabricated total in the exec summary discredits the entire document. This is cheap to prevent and expensive to discover late.

**When to use.**
- Any deliverable that cites volumes, KD averages, keyword counts, summed/addressable totals, or forecasts.
- ALWAYS in a multi-agent workflow (each agent is a fresh context that can invent figures).
- Before writing the executive summary or KPI forecast.

**Method.**
1. **Single source of truth.** Designate the raw data file (e.g. `keywords.csv`, the JSON artifacts) as canonical. Every figure traces back to it.
2. **Recompute, don't quote.** Load-bearing numbers are produced by a command (Bash `awk`/`sort`/`node -e`/`python`), not recalled from another agent's prose. State the filter used: e.g. "KD 1–20, vol≥100, US = 1,612 kws / 1,922,950 vol".
3. **Cite the recipe.** Next to each headline figure, note how it was computed (filter + file) so a reviewer can re-run it. If you can't reproduce it, you can't ship it.
4. **Dedicated reconciliation pass.** After the analysis agents finish, run ONE agent whose only job is to recompute every load-bearing number from the source and flag mismatches, fabrications, and undocumented filters. (In the master-plan workflow this is the completeness-critic + the synthesis "Number reconciliations" block.)
5. **Tag measured vs projected.** A number pulled from data is *measured*; an extrapolation is *projected*. Label every figure as one or the other. **Never sum measured + projected into the same line.**
6. **One canonical value per metric.** When agents disagree (170 vs 277k vs 380k for the same pool), pick the reproducible one, write it once, and have all sections cite that — don't let three numbers for one thing survive.
7. **One committed recompute script (not scattered Bash).** In multi-pass/cascade runs, different agents use slightly different ad-hoc filters and the "universe" drifts (e.g. 7,748 vs 7,823 vs 2,676 for the same thing). The fix: have the synthesis write ONE script — `analysis/recompute.py` — that reads ONE source file, applies ONE explicit filter set, and prints every headline; ship a snapshot of its output. Every doc cites *that script's* numbers; the adversarial pass re-runs it. A figure not in `recompute.py`'s output doesn't ship.
8. **Strict niche scoping — prune off-niche IN the recompute script.** "AI X" is not "X". The adjacent vertical, the generic-tool term, the competitor BRAND term, and the service-HIRE term (when the product is DIY/self-serve) are off-niche and **inflate the money/forecast pools**. Encode the prune as an explicit regex in `recompute.py` and state what it removed (e.g. "−395 kws / −233k vol: CAD tools, art-`drawing`, competitor brands, plant-care"). A `/vs/{competitor}` page may be planned, but the competitor's branded volume is never "our" demand. (See [[winnability-and-serp-regimes]].)

**Decision criteria / heuristics.**
- Can't reproduce it from the source with a command? → don't print it.
- Two agents give different totals for the same thing? → recompute; the prose loser is wrong.
- A suspiciously round or convenient number (exactly what the thesis needs)? → recompute before trusting.
- Forecast/revenue figures → must cite their input assumptions and be regenerable (use `scripts/forecast.py`, not hand arithmetic).
- Projected figure in a revenue line? → separate it; mark it; never blend with measured.

**Example.** In a personalized-baby-books master-plan run, the clustering agent emitted a BOFU floor of "53 terms / 12,060 vol". The reconciliation pass recomputed from `keywords.csv` (KD<20, vol≥100): **28 terms / 7,500 vol** (the artifact itself only listed 23 / 8,100). It also found the "addressable low-KD pool" cited as 862/1.1M actually computed to 1,612/1.92M under the documented filter, and that one name pool double-counted a KD-24 term above the rankable bar. All three were corrected to single canonical values before the exec summary was written. Without the pass, three wrong numbers would have anchored the plan.

**Pitfalls.**
- Trusting another agent's aggregate because it "sounds right".
- Letting the executive summary cite a figure no section can reproduce.
- Summing projected and measured volumes (inflates the headline).
- Skipping the reconciliation pass "because the critic will catch it" — make it a required step, not luck.

**Related.** [[seo-metrics]], [[measuring-seo-results]], [[ai-overviews-and-serp-features]], [[research-for-existing-sites]]. Tooling: `scripts/forecast.py` (reproducible forecasts). Used by the `full-master-plan` workflow.
