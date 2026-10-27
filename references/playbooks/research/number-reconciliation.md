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

## Search-led launch claims: the 2023 Figcomponents example

The [20-post Danny Postma thread](https://x.com/dannypostma/status/1646368426246680579)
is a historical founder account, not a current benchmark. Its four-stage pattern
(keyword → useful product → distribution → observation) already belongs to the existing
research, content, authority and monitoring workflows. Do not create a second pipeline.
See `audit-log/2026-10-27-danny-search-led-launch.md` and
`assets/danny-search-led-claim-map.csv` for all 20 source records and their existing homes.

**Searches are not visits or sales.** The source's `500 × 3 × 2% = 30` omits
organic click-through and assumes an unverified country multiplier. Use:

`expected_orders = eligible_non_overlapping_searches × organic_click_share × visit_to_paid_rate`

Define each denominator. A visit-to-trial rate followed by a trial-to-paid rate
requires both factors; neither is a visit-to-paid rate. Do not apply an extra CTR
if the input is already observed organic visits. Search volume, Search Console
impressions, clicks, analytics sessions, trials and paid orders are distinct metrics.

- Use country-specific or directly reported global volumes with provider, date,
  locale, device where available, and deduplication rules. **Do not triple a country volume.**
- Do not add related-keyword volumes blindly: overlapping intents, close variants,
  country/global pools and multiple URLs can count the same opportunity twice.
- Even accepting 1,500 monthly searches only for illustration, a hypothetical 10%
  organic click share and 2% visit-to-paid rate produce **3 expected orders, not 30**.
  At 5% click share it is 1.5. At 1% it is 0.3. These are scenario expectations,
  not measured customer counts. Fractional expectations are not observed orders.
- `assets/danny-search-led-scenarios.json` preserves these explicit assumptions and
  a compatible input for the **existing** `scripts/forecast.py`. Its KD-to-position,
  CTR and maturity defaults are modelling assumptions, not validated forecasts.
  Override with site/locale/SERP evidence before any business decision.
- Revenue needs price, refunds and time basis. Profit also needs labour, hosting,
  tooling, payment fees and fulfilment costs. A `$0 marketing budget` is not zero total cost.

Run the existing forecast offline with the `forecast_pools` list copied into a
project-local input file; do not point it at the whole scenario object:

```sh
python3 - <<'PY'
import json
import subprocess
from pathlib import Path
example = json.loads(Path('assets/danny-search-led-scenarios.json').read_text())
subprocess.run(['python3', 'scripts/forecast.py', '--json'],
               input=json.dumps(example['forecast_pools']), text=True, check=True)
PY
```

No live keyword, search console, customer or revenue data is included. This command
reads local example data and prints a model; it neither validates a niche nor launches a product.
