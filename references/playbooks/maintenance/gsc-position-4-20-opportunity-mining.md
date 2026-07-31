---
title: GSC Position 4–20 Opportunity Mining
area: maintenance
operational_addition: true
---

# GSC Position 4–20 Opportunity Mining

Use this for ongoing optimization when a site already has live pages and Search Console data. The goal is to find queries Google is currently testing in positions 4–20 where a small, evidence-backed page improvement could help.

## Inputs

- Google Search Console property and search type, usually `web`.
- A current final-data window, normally the latest complete 28 days.
- Optional 90-day export for history and decay checks.
- Access to each ranking page and the current live SERP.

## Procedure

1. Pull current GSC query rows and filter average position to `>= 4` and `<= 20`.
2. Sort by impressions, then join query+page rows so every query has an observed ranking URL.
3. Reject wrong-geo, irrelevant, accidental, duplicate, or intent-mismatched rows.
4. Treat 90-day-only rows as context. They are recovery/decay leads unless the current final-data window confirms the signal.
5. Inspect the live SERP and page for the exact missing element: entity/term coverage, comparison or cost table, useful FAQ, internal links, schema, title/snippet fit, or content-format mismatch.
6. Prefer a narrow implementation brief. Do not broadly rewrite a page when a precise addition answers the observed gap.
7. Track the same query/page pair in later final-data windows after the change ships.

## Required opportunity record

```json
{
  "property": "sc-domain:example.com",
  "date_range": ["YYYY-MM-DD", "YYYY-MM-DD"],
  "query": "...",
  "page": "https://example.com/...",
  "clicks": 0,
  "impressions": 0,
  "ctr": 0.0,
  "position": 0.0,
  "current_signal": true,
  "intent_fit": "confirmed|rejected|uncertain",
  "page_gap": "...",
  "recommended_change": ["..."],
  "caveats": ["..."],
  "status": "VALID|REJECTED|RECOVERY_ONLY"
}
```

## Evidence rules

- Current final 28-day data wins. A historical 90-day spike never becomes a “quick win” without current confirmation.
- Average position is an aggregate, not a stable rank; preserve device/country/date scope.
- Search Console rows are evidence of observed performance, not proof that one edit will cause a ranking gain.
- Keep implementation and measurement separate: route page changes to `content-production.md`, then follow up in `monitoring.md`.

## Done condition

Produce an implementation-ready list of valid opportunities and explicit rejected/recovery-only rows. Every valid row includes current GSC evidence, a verified ranking page, live intent/SERP evidence, a precise change, and caveats.
