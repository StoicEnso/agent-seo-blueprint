# Integration: Google Search Console (GSC)

## What it provides
First-party Google search performance for a property you own/verify:
- **Totals:** clicks, impressions, CTR, average position (over a date range).
- **Breakdowns:** per **query**, per **page**, per **date** (and country/device).
- Used to spot per-keyword position switches, intent shifts, and Google-update impact.

**Consumed by:**
- `references/playbooks/maintenance/measuring-seo-results.md` — clicks/impressions/avg position + per-keyword movement at review time.
- `references/playbooks/maintenance/navigating-google-updates.md` — detect drops aligned with update dates.
- `references/playbooks/maintenance/keyword-intent-evolution.md` — watch a keyword's clicks/position change as intent shifts.
- Workflows: `monitoring.md`, `site-audit.md`.

## Auth — API path (documented; stub is dependency-free)
- **Script:** `scripts/gsc_pull.py` — checks for creds, prints the target output shape, and (when creds exist) reports what it *would* query. It intentionally does **not** import Google libraries (none are installed).
- **Env var:** `GSC_CREDS` = path to a service-account JSON (recommended) or an OAuth token file.
- **Endpoint:** `POST https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query`
- **Scope:** `https://www.googleapis.com/auth/webmasters.readonly`
- **Setup the user does (skill guides, never auto-auths):** create a service account in Google Cloud, enable the Search Console API, then **add the service-account email as a user on the GSC property** (Settings → Users and permissions). Or run an OAuth flow once and save the token to `GSC_CREDS`.
- **Optional libs (NOT installed; note only):** `google-api-python-client`, `google-auth`.
- Request body example:
  ```json
  { "startDate": "2026-04-22", "endDate": "2026-05-20",
    "dimensions": ["query"], "rowLimit": 100 }
  ```

What the agent runs:
```bash
python3 scripts/gsc_pull.py --site https://example.com/ --days 28 --dimension query
python3 scripts/gsc_pull.py --print-shape          # show the JSON shape to produce
```
With no `GSC_CREDS`, the script prints the browser-fallback steps + output shape and exits 2.

## Auth — browser fallback path (primary if no creds)
The user must already be logged into the Google account that owns the property. The skill never logs in or completes OAuth.
1. `mcp__claude-in-chrome__navigate` → `https://search.google.com/search-console`.
2. Select the property (top-left switcher). Open **Performance → Search results**.
3. Set the date range (e.g. **Last 28 days**) and toggle on all four metrics (Total clicks, Total impressions, Average CTR, Average position).
4. `mcp__claude-in-chrome__get_page_text` to read the four summary cards.
5. Switch the table tab to **Queries** (and/or **Pages**); `get_page_text` / `mcp__claude-in-chrome__javascript_tool` to extract rows (query/page, clicks, impressions, CTR, position). The table is paginated/JS-rendered — wait for load; pull the top N you need.
6. For update analysis, compare two date ranges (use the "Compare" date option) and read the deltas.

If a login or consent screen appears, STOP and ask the user to sign in.

## Rate limits / gotchas
- **Property type matters:** URL-prefix (`https://example.com/`) vs Domain (`sc-domain:example.com`) report differently — match what the user verified.
- GSC data lags ~2-3 days and the per-query table is **sampled/limited** to ~1,000 rows in the UI (more via API). Average position is an average — a small move can hide big per-query swings.
- API: standard Search Console API quotas (per-property + per-project QPS); page through `rowLimit`/`startRow` for large pulls.
- Position is 1-indexed; "0" CTR rows with high impressions = ranking but not clicked (snippet/title problem).

## Output shape
Produce this (API or browser) so it feeds `scripts/report.py monitoring` and the measuring playbook (`--print-shape` prints it):
```json
{
  "site": "https://example.com/",
  "period": "2026-04-22..2026-05-20",
  "metrics": { "clicks": 5230, "impressions": 142000, "ctr": 0.037, "avg_position": 14.2 },
  "rows": [
    { "key": "ai headshot generator", "clicks": 410, "impressions": 9800, "ctr": 0.042, "position": 6.3 }
  ],
  "dimension": "query"
}
```
For `scripts/report.py monitoring`, map `metrics` → its `metrics` block and the top `rows` → its `keywords` list (`{keyword, position, change}` after diffing against the previous snapshot).
