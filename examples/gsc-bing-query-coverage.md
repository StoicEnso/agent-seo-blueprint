# Google + Bing query coverage — worked review

**Synthetic example only.** URLs, exports, quotes, figures and SERP records below are invented fixtures for explaining the contract, not observations of a real site or traffic/ranking promises. Do not publish them as an audit.

## A. Summary and scope

Page: `https://example.com/guides/route-planning/`, canonical confirmed in the fixture. Audience: small delivery firms. Offer: route-planning software. Both fixture exports cover final 1–28 October 2026 web-search rows, GB/desktop; report timezone is recorded independently and cross-engine time boundaries remain a limitation. Page filter and raw-row locators are retained. Five clusters were reviewed, not every query in the universe.

## B. Coverage table (separate engine metrics)

| Cluster | Exact queries by engine / observed presence | GSC impressions / clicks / position | Bing impressions / clicks / position | Coverage and page evidence | Intent evidence / priority |
|---|---|---|---|---|---|
| C1 | GSC: route planning for vans; Bing: van route planner / both | 800 / 16 / 9 | 120 / 3 / 6 | covered_weakly; fixture H2 Planning: 'Choose your stops.' | Separate fixture Google and Bing results reward a worked multi-stop example; High review priority |
| C2 | Bing: route planning with delivery time windows / Bing only | not observed; unknown, not zero | 200 / 2 / 11 | not_covered; page read complete, quote none | Bing fixture result E2 shows informational how-to; Medium, but product capability must be verified before claiming it |
| C3 | GSC: careers at route planning ltd / GSC only | 90 / 0 / 14 | not observed; unknown, not zero | wrong_intent; careers navigation is not this guide's job | Reject addition; existing owner/cannibalization review before another-page suggestion |
| C4 | GSC: what is route planning / GSC only | 300 / 12 / 4 | not observed; unknown, not zero | covered_well; fixture intro: 'Route planning puts delivery stops in a useful order.' | Keep; no extra section needed |
| C5 | Bing: route planning for bicycles / Bing only | not observed; unknown, not zero | 12 / 0 / 18 | unverified; fixture page read lacks relevant scope evidence | SERP not_checked; research-only, not a new-page brief |

These source labels describe supplied exports. C1 has different exact variants in one reviewed cluster; it is not one shared exact query. No total across engines or blended CTR/position is calculated. Within the GSC C1 row CTR is 16/800 = 2%; within the Bing C1 row it is 3/120 = 2.5%. Neither rate is a universal target or a causal diagnosis.

## C. Recommendations

- **C1:** draft a worked example after H2 Planning, with two or three sentences explaining the stop order and its assumptions. Quote/source real product behavior before making a product claim. Evidence locators: fixture page P1 and distinct SERP records G1/B1 (named engine, exact query, observation date, locale/device and top URLs). Add a contextual link from an existing delivery guide only if the reader needs the next step; do not add a link quota.
- **C2:** propose H2 'Planning around delivery time windows' only after confirming the audience need and whether the page can answer truthfully. Explain constraints without claiming an unavailable product feature. Keep Medium priority rather than inferring Google demand from Bing.
- **C3:** reject for this page; do not add a careers FAQ to chase impressions. C4 stays unchanged. C5 remains research-only until page/intent evidence is available.

## D. Honest metadata options

1. 'Van route planning: a worked delivery example' — use only after the page contains that example.
2. 'Plan delivery stops for a small van fleet' — use only if scope and instructions match.

Description draft: 'See a worked delivery-stop plan, the assumptions behind it, and the checks to make before using it.' No unsupported number, year, feature or promised saving.

## E. Review and measurement

State: `draft_only`, approval `not_requested`; no executor or submission runs. Freeze the exact diff and source revision/hash before any approved write. Plan separate Google and Bing +28/+56-day same-scope final-window reads after an approved change, preserving baseline and confounders. This example creates no schedule and claims no measured result.

## Missing-source variant

If Bing authentication fails, set `bing.status=unavailable`, retain the reason and evidence, and leave its unavailable metrics null. Do not copy the Bing fixture rows into a real audit. Run a labeled Google-only review; `GSC only` means observed in the available export, not absent in Bing. If neither engine has usable page-query evidence, emit a research-only limitation instead of an implementation recommendation.
