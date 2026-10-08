---
title: GSC Zero-Click Untargeted-Query Triage
area: maintenance
operational_addition: true
---

# GSC Zero-Click Untargeted-Query Triage

Use this read-only triage inside monitoring after the normal GSC 4-20 and content-opportunity flows. It turns saved query/page rows into a review ledger. It does not prove that a page is missing, promise traffic, or publish anything.

## Inputs and scope
Save the exact property, finalized complete date range and timezone, search type, dimensions, filters, query/page grouping, and pagination/row-limit state. Keep domain and URL-prefix properties separate: they may overlap and cannot be summed into a unique-site total. Preserve anonymous/capped-row caveats. Keep current metrics separate from earlier-query history.

Provide an explicit inventory, owned-page, and intent coverage check per query. A GSC impression already has an observed result URL. No inventory match or missing coverage evidence is UNKNOWN, not evidence of zero coverage. Anonymous query omissions and row caps limit discovery; they do not erase observed rows. A capped export cannot prove a page gap. Nonfinal or incomplete windows stay unknown. Parameterize minimum impressions and position thresholds for the site; they are review filters, not universal laws.

## Procedure
1. Export separate query-only and query+page data from one comparable final window. Confirm zero clicks in the query-only snapshot: zero clicks on one page is not a zero-click query when another page was clicked. Keep query and query/page aggregation separate; do not sum page impressions into a query total. Filter with the chosen minimum impressions.
2. Run python3 scripts/gsc_zero_click_triage.py input.json --output monitoring/date_gsc-zero-click-ledger.json --csv monitoring/date_gsc-zero-click-review.csv. This makes no network, GSC, CMS, URL, publishing, scheduling, outreach, or spend write.
3. Review each ledger row with the observed page, inventory, intent and cannibalization evidence. Inspect the real page and related tools, not only its URL: a generic slug can already serve the query. Multiple ranking pages are a cannibalization candidate, not proof of harm. Classify only as: relevant untargeted topic needing a new dedicated page; existing page content/intent adjustment; relevant well-ranked snippet/CTR investigation; low-rank authority/technical issue; cannibalization; irrelevant/brand/navigational/no-click-answer intent; or unknown due to missing evidence.
4. Research intent and current SERP before a useful draft. Route an approved brief to content-production.md; any live change retains the existing explicit approval and measurement gates. Never blindly create a page or redirect a URL.

## Required ledger fields
Every candidate records property, finalized range/timezone, search type, dimensions, filters, page URL, clicks, impressions, CTR, position, query/page grouping, inventory/coverage evidence, category, recommendation, confidence, and limitations. The tool emits an inspectable JSON ledger and CSV review view; CSV formula-prefix values are escaped.

## Input template and example

Start from `templates/gsc-zero-click-input.json`. Metrics use numbers and CTR uses a fraction (`0.02`, not `2%`). `metadata.date_range` must include ISO start/end dates, timezone and a boolean `finalized`. Set `data_quality.complete_window` from the actual collection. Supply `rows` as query/page observations; an empty page is explicitly unknown. Optional `query_totals` holds the separate query-only clicks. If it is absent, the ledger flags the unverified query-wide filter. Optional `history` preserves earlier clicks without claiming that missing earlier rows had zero clicks.

`coverage` is a unique per-query list with status `covered`, `not_covered` or `unknown` and a non-empty evidence reference. `not_covered` means a documented inventory plus related-page/intent review found no suitable dedicated page; it does not mean an export lacked the URL. Store exact reviewed URLs and explanations in that reference. Page-level intent mismatch can justify improving an existing tool rather than adding a new URL. The output is a draft review, never an execution instruction.

Example: 60 zero-click impressions for “gazebo size calculator” lead to a pergola URL. Read its controls before proposing a gazebo page. If it already supports gazebos, improve sizing guidance or query targeting instead. If the query needs seating-layout advice the tool cannot give, draft that narrow feature brief and check adjacent assets before choosing a URL.

## Retargeting and measurement

Retargeting here means mapping a search intent to a suitable owned page or useful tool. It does not authorize paid remarketing, cookies, audiences, spend, publication or redirects. Record the proposed target, user benefit and relevant product action. Search impressions do not prove requests, leads or revenue. After a separately approved change, use the existing content-change ledger and comparable +28/+56-day checks; keep clicks, tool use, requests and paid conversions distinct. No routine is created by this playbook.

## Interpretation limits and sources
Zero clicks in the current period can follow earlier clicks. High ranking with zero clicks can be a SERP, snippet, or no-click-answer question; low rank can be authority, technical, or format work. Treat the creator post as a candidate-filter idea, not a guaranteed-growth claim.

Creator seed (not a guaranteed-growth claim): https://x.com/hridoyreh/status/2107689877684858898 . Official references checked 2026-10-08: Performance report https://support.google.com/webmasters/answer/7576553 ; Search Analytics API https://developers.google.com/webmaster-tools/v1/searchanalytics/query ; data anomalies https://support.google.com/webmasters/answer/6211453 . These are living documents, not pinned versions. The support-page captures were partial; the API reference explicitly says it returns top rows, not guaranteed all rows. Recheck the relevant source before changing an implementation.
