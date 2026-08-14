---
title: AI Overviews & SERP Features — Haircut the Click Curve, Win the Citation
area: maintenance
source_lessons: ["05-01","05-03"]  # extends "navigating updates" + "intent evolution" into the AIO era
tools: [ahrefs, serp]
---

# AI Overviews & SERP Features — Haircut the Click Curve, Win the Citation

**What it is.** The classic click curve (#1 ≈ 30%, #2 ≈ 15%, #3 ≈ 10%) assumes a plain ten-blue-links SERP. In 2025–26 that is rarely true: **AI Overviews (AIO), People-Also-Ask, image/video packs, shopping, discussions (Reddit/forums) and top-stories** push the first organic result far down the page and answer the query in-SERP. Forecasting with the raw click curve **over-states traffic** — sometimes 2×. This playbook adds the missing step: measure SERP-feature exposure, haircut the forecast, and shift the plan toward queries and formats the features can't eat.

**The course gap.** The course predates AIO; its CTR math is optimistic for informational queries. This is the correction.

**When to use.**
- Before forecasting any keyword pool's traffic (REQUIRED for forecast-bearing pools — see [[measuring-seo-results]]).
- When deciding which clusters to build first (commercial/entertainment vs informational).
- When a page ranks #1–3 but real GSC clicks are far below the click-curve estimate.

**Method.**
1. **Measure exposure with real SERPs.** For the top N forecast-bearing terms per pool, pull the SERP and read its **features**, not just the organic list. With the Ahrefs skill: `node scripts/ke-headless.mjs serp "<kw>"` → `features:{ai_overview, questions, image_pack, discussions, shopping, top_stories, paids}` (the `serpOverview()` parser surfaces these). Record an **AIO-exposure flag** per term/pool.
2. **Read the intent signal — AIO tracks intent.** Empirically, AIO saturates **informational "ideas / how / what" queries** and largely spares **commercial-buy** (gifts, "best X", product) and **entertainment "give me the thing"** (read-the-story, lyrics, watch) queries. Weight the build toward the AIO-safe intents; treat informational head terms as citation plays, not click plays.
3. **Apply the haircut in the forecast.** Don't use a flat ×0.8. For informational + AIO-exposed pools, multiply organic CTR by **(1 − haircut), haircut ≈ 0.4–0.6**. Keep ~full CTR on no-AIO commercial/entertainment pools and on long-tail PSEO leaves (lighter features). Run it deterministically: `scripts/forecast.py --aio-haircut 0.5` (set `"aio": true/false` and `"intent"` per pool in the input). This stops the headline number from being fiction.
4. **Win the citation (AIO/PAA optimization).** When the AIO eats the click, be the *source* it cites: put a concise, extractable direct answer in the first screen (40–60 words), use FAQPage/HowTo schema, clear H2 questions matching PAA, lists/tables/definitions, and strong entity/EEAT signals. Being cited drives brand + the residual click.
5. **Don't fight features you can't win — reformat.** If the SERP is a shopping pack, build the product/gift page, not an article. If it's an image pack (themes/ideas), invest in original imagery + Pinterest. If it's "discussions", seed/answer on Reddit/forums. If it's an entertainment library (nursery rhymes, bedtime stories), HOST the artifact (read-online / lyrics / video) instead of writing about it.
6. **Re-check quarterly.** Feature coverage shifts; a pool that's AIO-free today may not be in six months. Re-pull SERPs and re-haircut.

**Decision criteria / heuristics.**
- Forecast-bearing pool with no SERP-feature data → **do not forecast it yet.** Pull SERPs first.
- Informational + AIO present → citation play + 0.4–0.6 CTR haircut; never anchor revenue on it.
- Commercial-buy / entertainment-host intent + no AIO → safer; weight build here.
- Head terms with strong refdomains AND AIO → drop from the capture model; target the long-tail/idea variants and PSEO leaves instead.
- "Ranking #1" ≠ "30% CTR" anymore — verify against GSC, not the curve.

**Example (personalized-baby-books research, 2026-06).** Live SERPs for 20 TOFU head terms: **AI Overviews on 16/20 (80%)**, plus near-universal PAA + image packs. The 4 AIO-free terms were the *commercial* (`baby shower gifts`, `gender reveal cake`) and *entertainment* (`nursery rhymes`, `bedtime stories`) ones. Page authority was low everywhere (top-5 median URL-rating 4–6 — beatable), so the barrier was **features, not links**. The plan therefore: lean on commercial/keepsake/name-book pools + PSEO long-tail, host an entertainment story library, optimize for AIO citation on informational, and apply a 0.5 haircut — turning a fictional 218k/mo into an honest base/downside band.

**Image-pack & informational pools are FEEDERS, not click channels.** An image-pack/AIO-gated informational pool (e.g. an "ideas / inspiration" ocean owned by Pinterest/Houzz/DR90+) does not pay in classic organic clicks — its value is **image-pack impressions + Pinterest referral + AIO citations that drain to a session**. Model it at low CTR/capture, label it a reach/trial/citation feeder, and **anchor the revenue case on the `blue_link` money + commercial pools** (which carry no informational AIO haircut). Don't let the big informational volume dominate the headline — it's the least certain. (Pair with [[winnability-and-serp-regimes]].)

**The double-haircut trap (a real forecast bug).** `scripts/forecast.py` already folds the AIO haircut INTO the effective CTR for `intent:informational, aio:true` pools (`eff_ctr = base_ctr × (1−haircut) × capture`). If a downstream agent then multiplies the pool's output by `(1−haircut)` *again* — "to apply the haircut" — it is applied **twice**, halving the number a second time. Apply the haircut exactly **once**: either via the pool flags fed to `forecast.py`, or by hand — never both. When a "corrected" forecast suddenly drops ~50% on the informational pools, suspect a double-application and re-derive from `forecast.py`'s own output.

**Pitfalls.**
- Forecasting informational pools at full click-curve CTR (the single biggest over-statement).
- Treating AIO as a tailwind ("we'll get cited so it's fine") — model the *click loss* first, count citations as upside.
- Ignoring `discussions`/Reddit dominance — sometimes the only way in is the forum, not your page.
- Building articles for SERPs that show shopping/image/video packs.
- **Double-applying the haircut** (see above) — or, conversely, letting the image-pack ocean's clicks anchor the business case when they're the least certain line in the model.

**Related.** [[measuring-seo-results]], [[navigating-google-updates]], [[keyword-intent-evolution]], [[seo-metrics]], [[search-intent]], [[number-reconciliation]]. Tooling: Ahrefs `serp` (feature detection), `scripts/forecast.py` (deterministic haircut model). Course refs: extends 05-01 (updates) and 05-03 (intent evolution) into the AI-Overview era.
