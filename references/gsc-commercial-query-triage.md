# Commercial-term query triage in Search Console

A small extension of the existing monitoring, search-intent, GSC 4–20 and content-opportunity workflows. A regex filter is discovery, **not a ranking intervention**. It changes a report view; it cannot force Google to send visitors.

## Source and correction

An owner-supplied screenshot attributed to **Hridoy Reh (@hridoyreh)** was reviewed on 21 October 2026. No post URL or publication date was visible, so neither is invented. The creator claimed 14,500+ visitors; the pictured report showed about 14.5k **clicks**, not unique visitors, over a selected 12-month window. It does not establish causality, a comparable baseline, or that the chart uses this filter.

The screenshot's regex uses phrases such as `buy shop order`, `schedule reserve nearme instock available sameday`, and `reviews alternative alternatives` where alternatives need `|`. Those spaces are literal. This causes false negatives for standalone `buy`, `schedule` and `alternatives`. A trailing space in `review ` also misses an end-of-query `review`.

Use this explicit, case-insensitive **English seed**, in Query → Custom (regex) → Matches regex:

```regex
(?i)\b(buy|shop|order|pricing|price|cost|hire|book|schedule|reserve|near\s*me|in\s*stock|available|same\s*day|best|vs|review|reviews|alternative|alternatives|deal|discount)\b
```

`|` means OR. `\b` is an ASCII word boundary in RE2. `\s*` handles common whitespace variants, including `near me` and `nearme`. The explicit `(?i)` makes case handling clear. Keep a versioned copy of any site-specific term additions. This is not language-universal: use native-language terms and test boundaries for other scripts. Do not use unsupported RE2 lookarounds or backreferences.

### Small pilot before expansion

Test **3–10** real queries manually before relying on a saved filter. Include expected hits, substring false positives and omitted action/tool queries. Examples below are synthetic, not performance evidence:

| Query | Candidate signal | Review still needed |
|---|---|---|
| `buy garden app` | transaction | Is this the site's actual product and current intent? |
| `garden app alternatives` | comparison | Which existing page owns this demand? |
| `garden design cost` | price | Is the user buying software or planning a contractor budget? |
| `best price near me` | overlapping groups | Is local availability relevant at all? |
| `garden book` | transaction-word hit | Could be a publication, not a booking. |
| `costume ideas` | no match | Boundary prevents substring `cost`. |
| `garden generator` | no match | An action query can matter without a listed modifier. |

The live Search Console API accepted the corrected regex during the bounded source check. Local Python tests validate the portable pattern subset and normalization contract; they are not a general RE2 conformance suite.

## Collect comparable evidence

1. Resolve the existing project workspace. Use the latest complete **final** 28 days, plus the preceding adjacent equal-length final window. Search Console dates use `America/Los_Angeles`, not the operator's local date. Confirm available dates with a date-only query. Keep recent partial data separate.
2. Record exact property, search type, country, device, windows and filters. Keep unfiltered property totals, named `query` rows and `query+page` rows **separate**. A query can reach multiple URLs, so page-grouped impressions are not interchangeable with property-grouped impressions.
3. Compare the literal source pattern and corrected pattern at identical scope. Preserve both expressions, input/response captures, grouping and collection times. Do not transfer a chart's click count to a different filter.
4. Preserve an unfiltered control. Query filters omit hidden/anonymized queries. API row pagination does not guarantee exhaustive coverage; the UI table is also limited. A missing query is unknown, not zero demand. The difference between property totals and named-query sums is not automatically a complete count of anonymized queries.
5. Read relevant surviving queries with their observed URLs. Separate transaction, price, comparison and availability **signals**, not proven intent classes. Groups can overlap; do not sum their metrics as mutually exclusive buckets.

## Offline analyzer

`scripts/gsc_commercial_queries.py` uses Python's standard library only. It reads already-authorized, normalized exports. It makes no network, credential, scheduler or website call, and it does not replace `gsc_pull.py` or implement a new collector.

```bash
python3 scripts/gsc_commercial_queries.py assets/gsc-commercial-query-example.json --as-of 2026-10-21
# Private project data stays in the project's private workspace:
python3 scripts/gsc_commercial_queries.py /private/current-queries.json \
  --previous /private/previous-queries.json --as-of YYYY-MM-DD > /private/commercial-triage.json
```

Input contract:

- `meta`: `site`, `start`, `end`, `dimensions`, `type: web`, `data_state: final`, `country`, `device`. Dates are inclusive ISO dates. Set country/device to `all` explicitly when unfiltered. `date_timezone`, if present, must be `America/Los_Angeles`.
- `dimensions`: exactly `["query"]` or `["query", "page"]`; `rows[].keys` follow that order.
- `rows`: unique dimension keys, nonnegative whole clicks, positive whole impressions, finite position ≥1; optional CTR must be a 0–1 fraction consistent with clicks/impressions. Unknown values do not become zero.
- Supply an **unfiltered** baseline. Nonempty `include_regex`, `exclude_regex` or `filters` is rejected so the pattern comparison cannot silently discard its control.
- Optional previous data must match property, dimensions, search type, country/device, and be adjacent/equal-length. Missing previous rows produce `null` deltas, not assumed zeroes.

Output preserves matched candidates, nonmatching controls, source-pattern false negatives, overlapping signal groups and current row sums. Position is impression-weighted only within that same row aggregation. Empty CTR/position are `null`. Status is always `REVIEW_ONLY` (or `STALE_REVIEW_ONLY` after seven days); no row is approved for write. Invalid input emits `INVALID_INPUT` and exits 2. Explicit empty rows are allowed but do not prove full coverage. Save outputs privately: **No live project query rows** belong in the public skill repository.

## Review, do not auto-optimize

For 3–10 relevant candidates:

- Check business fit and separate brand/navigation from generic demand. A contractor cost calculator may have little value for a software purchase.
- Inspect the live search results, existing page, canonical and current content. Check whether multiple URLs have distinct legitimate roles. Multiple ranking URLs are a review signal, not proof of harmful cannibalization.
- Check existing briefs, tickets and open PRs before creating work. Prefer the appropriate existing page; do not create a page per modifier.
- Keep low-position/low-volume evidence, page-one weak-CTR opportunities and actual comparable click loss distinct. Zero clicks alone do not identify a snippet defect.
- A protected page or product/trust claim stays protected. Route any justified exact change through `content-opportunity-audit-and-measurement.md` and the normal content workflow. Preserve exact-diff approval and measurement gates. No automatic publication follows from this analyzer.
- Measure approved changes at the existing +28/+56-day checkpoints. Search clicks, sessions, leads, paid outcomes and causal claims remain separate. Source screenshots do not establish growth promises.

Primary references, checked 21 October 2026:
- [Search Analytics query API: RE2 filters, final data, Pacific dates, aggregation and top-row limits](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [Search results performance: clicks, impressions, chart/table aggregation and preliminary data](https://support.google.com/webmasters/answer/7576553?hl=en)
