# GSC Zero-Click Untargeted-Query Triage

Use this read-only triage inside monitoring after the normal GSC 4-20 and content-opportunity flows. It turns saved query/page rows into a review ledger. It does not prove that a page is missing, promise traffic, or publish anything.

## Inputs and scope
Save the exact property, finalized complete date range and timezone, search type, dimensions, filters, query/page grouping, and pagination/row-limit state. Keep domain and URL-prefix properties separate: they may overlap and cannot be summed into a unique-site total. Preserve anonymous/capped-row caveats. Keep current metrics separate from earlier-query history.

Provide an explicit inventory, owned-page, and intent coverage check per query. A GSC impression already has an observed result URL. No inventory match, missing coverage evidence, or anonymous/partial data is UNKNOWN, not evidence of zero coverage. Parameterize minimum impressions and position thresholds for the site; they are review filters, not universal laws.

## Procedure
1. Export saved query+page data from one comparable final window. Filter zero-click rows with the chosen minimum impressions.
2. Run python3 scripts/gsc_zero_click_triage.py input.json --output monitoring/date_gsc-zero-click-ledger.json --csv monitoring/date_gsc-zero-click-review.csv. This makes no network, GSC, CMS, URL, publishing, scheduling, outreach, or spend write.
3. Review each ledger row with the observed page, inventory, intent and cannibalization evidence. Classify only as: relevant untargeted topic needing a new dedicated page; existing page content/intent adjustment; relevant well-ranked snippet/CTR investigation; low-rank authority/technical issue; cannibalization; irrelevant/brand/navigational/no-click-answer intent; or unknown due to missing evidence.
4. Research intent and current SERP before a useful draft. Route an approved brief to content-production.md; any live change retains the existing explicit approval and measurement gates. Never blindly create a page or redirect a URL.

## Required ledger fields
Every candidate records property, finalized range/timezone, search type, dimensions, filters, page URL, clicks, impressions, CTR, position, query/page grouping, inventory/coverage evidence, category, recommendation, confidence, and limitations. The tool emits an inspectable JSON ledger and CSV review view; CSV formula-prefix values are escaped.

## Interpretation limits and sources
Zero clicks in the current period can follow earlier clicks. High ranking with zero clicks can be a SERP, snippet, or no-click-answer question; low rank can be authority, technical, or format work. Treat the creator post as a candidate-filter idea, not a guaranteed-growth claim.

Official references, captured 2026-10-08: Performance report https://support.google.com/webmasters/answer/7576553 ; Search Analytics API https://developers.google.com/webmaster-tools/v1/searchanalytics/query ; data anomalies https://support.google.com/webmasters/answer/6211453 . Recheck these sources before changing an implementation.
