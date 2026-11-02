# Eight-plus-word Search Console queries: export → page review → pull request

Use the existing monitoring and content-production workflows. This is a query-length discovery slice, not a second content programme or a reason to publish automatically.

## Source and limits

An @askOkara screenshot dated 2 November 2026 suggests filtering Google Search Console (GSC) for searches with eight or more words, finding high impressions with few clicks, and answering the query near the top of its ranking page. Treat this as a hypothesis to review, not a proven SEO hack. The screenshot's suggestion that these are the same questions people ask ChatGPT is unverified. Ordinary Google Search rows do not measure ChatGPT prompts, AI traffic, citations, or conversions. Do not connect Okara or another third-party account to perform this task.

## Collect an honest export

1. Inventory the actual site owner, property, repository and existing writer/PR route for every in-scope site. Domain and URL-prefix properties are not interchangeable. Deduplicate against current exports, opportunities, open branches and PRs. Preserve existing holds and single-writer ownership.
2. Open **Performance → Search results** for the exact property. Use the latest **final** 28-day window; record explicit dates, capture time, search type, country, device and every filter. GSC dates use Pacific Time. Do not call preliminary or older saved data current. An optional final 90-day export is historical context, not current demand.
3. Add **Query → Custom (regex) → Matches regex** and paste:

   ```text
   ^(?:\S+\s+){7,}\S+$
   ```

   This matches eight or more whitespace-delimited tokens. It does not require a question mark or interrogative intent. It excludes shorter useful questions and does not segment languages without spaces. Leading/trailing whitespace can prevent a match. Keep the raw query and describe any normalization; never silently substitute a broader regex.
4. Turn on clicks, impressions, CTR and average position. Save query rows AND observed **query+page pairs**. In the UI, select an exact query and export its Pages table, retaining that query filter. Through an already authorized API, request dimensions `query,page` and preserve their order. Never join unrelated top Queries and top Pages tables by row number or guess the ranking page. Capture all observed URLs for a query; multiple URLs alone do not prove cannibalization.
5. Keep raw exports private. Record pagination, returned row count, row limits and whether extraction stopped early. UI exports and Search Analytics API rows omit anonymized queries and can return only top rows; finishing pagination is not proof of all demand. A filtered empty result is not proof of zero questions or zero impressions. Preserve unfiltered or nonmatching control rows separately when available; do not add overlapping totals.

`scripts/gsc_pull.py` remains a credential-gated **stub**, not a working exporter. Use the existing authorized API/browser route in `integrations/gsc.md`; do not claim the stub performed a live pull. An API request through that route can use:

```json
{
  "startDate": "2026-10-04", "endDate": "2026-10-31",
  "type": "web", "dataState": "final", "dimensions": ["query", "page"],
  "dimensionFilterGroups": [{"filters": [{"dimension": "query", "operator": "includingRegex", "expression": "^(?:\\S+\\s+){7,}\\S+$"}]}],
  "rowLimit": 25000, "startRow": 0
}
```

Dates above are an example, not a permanent window. Retain country/device filters and page through `startRow` in a bounded rate-safe sequence. Google uses RE2; the expression uses no lookbehind or backreferences. The offline Python helper uses compatible syntax, not an embedded RE2 engine.

## Offline candidate review

Copy `assets/gsc-long-query-export.example.json`, replace every synthetic field with checked private export evidence, then run:

```bash
python3 scripts/gsc_long_query_review.py /private/site-export.json > /private/long-query-review.json
```

The helper reads saved JSON only. It accepts normalized rows or Search Analytics `keys` in the declared dimension order. It validates metadata, property/page membership, metrics and duplicate query+page scope. It preserves the manifest, raw queries and nonmatches. Sort order is impressions descending, CTR ascending, then query/page; this is a transparent **review order**, not forecast revenue or guaranteed uplift. It never fetches data, decides intent, creates a PR, writes to a website or publishes. Inputs older than seven days at the window end are labeled `STALE_DATA`; default freshness is a triage setting, not a Google guarantee. Incomplete extraction remains `PARTIAL_EXPORT`. Every otherwise eligible row remains `NEEDS_PAGE_REVIEW`.

## Decide whether a page change is justified

- Assess business relevance, geography, language, brand intent, sample size, current position, seasonality, SERP features and the actual search results. High impressions with low clicks may reflect low rank or zero-click results, not a weak answer. CTR is clicks divided by impressions, not an estimate of answer quality.
- Inspect the observed ranking page and verify a specific missing or unclear answer. Preserve a page revision/snapshot and live SERP evidence with time. A good existing answer is a valid `NO_CHANGE` result. Reject unsupported claims, wrong intent, stale-only signals and duplicated pending work.
- Group closely related queries onto the existing correct page. Do not make one thin page per query or force every answer into an FAQ. Where helpful, place a concise, accurate answer near the top, without displacing the main user task, product proof or conversion path. Source prices, numbers, comparisons and legal/technical claims. Preserve accessibility, canonical URLs and useful internal links; do not add misleading schema or keyword stuffing.
- Prefer a 3–10-pair pilot before expanding. The current 4–20 opportunity lane can supply context, but **do not apply its rank cutoff to this length-based export**. Keep outside-range candidates visible for separate review.

## Site-specific PR contract

For each supported change, use the owning site's authorized writer and review route. The brief/PR includes exact query+page evidence, final window and scope, source file locator, live page/SERP findings, relevant query cluster, existing PR deduplication, exact before/after diff, product/claim sources, test results and rollback. Keep private GSC rows out of public PRs; use approved redacted/aggregate evidence references. Run applicable lint, build, content, accessibility and link checks. A ticket to an exclusive build lead is a handoff, not a completed implementation PR.

Statuses: `NO_MATCHES`, `NO_CHANGE`, `REJECTED`, `STALE_DATA`, `PARTIAL_EXPORT`, `ACCESS_BLOCKED`, `BRIEF_READY`, `PR_OPEN`. Record exact site/property/access state and next action; never invent a PR when data supports no change. Agent handoff acceptance is not export completion. Report each site's result, PR/ticket URL and unresolved gate separately.

Opening a review PR does **not** authorize merge, deploy, publication, scheduling, new accounts, new paid connectors, scope upgrades or unrelated browser work. Preserve existing site-owner approval gates. After a separately approved release, record its date and compare like-for-like final query/page windows at +28 and +56 days using the existing measurement ledger. Keep rankings, ordinary search clicks, named AI-provider evidence and business outcomes separate. Before/after movement alone is not causal proof.
