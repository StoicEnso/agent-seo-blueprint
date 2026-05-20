# Integration: Google Analytics 4 (GA4)

## What it provides
First-party behavior + conversion data for a property you own:
- **Organic traffic:** sessions and engaged sessions from the **Organic Search** channel.
- **Engagement:** engagement rate, average engagement time.
- **Conversions:** key events / conversions (overall and by landing page).
- **Landing-page detail:** which organic entry pages drive sessions and conversions.

GSC answers "did Google show/click us"; **GA4 answers "did that traffic do anything"** (engage, convert). The two together close the "did the work pay off" loop.

**Consumed by:**
- `references/playbooks/maintenance/measuring-seo-results.md` — GA4 organic sessions, engagement, conversions at quarterly review.
- `references/playbooks/maintenance/navigating-google-updates.md` — confirm a ranking drop actually cost sessions/conversions.
- Workflows: `monitoring.md`, `site-audit.md`.

## Auth — API path (documented; stub is dependency-free)
- **Script:** `scripts/ga4_pull.py` — checks for creds, prints the target output shape, and (when creds exist) reports what it *would* query. It intentionally does **not** import Google libraries (none are installed).
- **Env var:** `GA4_CREDS` = path to a service-account JSON (recommended) or OAuth token file.
- **Endpoint:** `POST https://analyticsdata.googleapis.com/v1beta/properties/{propertyId}:runReport`
- **Scope:** `https://www.googleapis.com/auth/analytics.readonly`
- **Setup the user does (skill guides, never auto-auths):** create a service account, enable the Google Analytics Data API, then **grant that service-account email at least Viewer on the GA4 property** (Admin → Property Access Management). Or run OAuth once and save the token to `GA4_CREDS`.
- **Optional libs (NOT installed; note only):** `google-analytics-data`, `google-auth`.
- Request body example (isolate organic):
  ```json
  { "dateRanges": [{ "startDate": "2026-04-22", "endDate": "2026-05-20" }],
    "dimensions": [{ "name": "sessionDefaultChannelGroup" }],
    "metrics": [{ "name": "sessions" }, { "name": "engagedSessions" },
                { "name": "conversions" }, { "name": "engagementRate" }],
    "dimensionFilter": { "filter": { "fieldName": "sessionDefaultChannelGroup",
      "stringFilter": { "value": "Organic Search" } } } }
  ```

What the agent runs:
```bash
python3 scripts/ga4_pull.py --property 123456789 --days 28
python3 scripts/ga4_pull.py --print-shape          # show the JSON shape to produce
```
With no `GA4_CREDS`, the script prints the browser-fallback steps + output shape and exits 2.

## Auth — browser fallback path (primary if no creds)
The user must already be logged into the Google account with GA4 access. The skill never logs in or completes OAuth.
1. `mcp__claude-in-chrome__navigate` → `https://analytics.google.com`.
2. Select the property (top-left). Open **Reports → Acquisition → Traffic acquisition**.
3. Set the date range. `mcp__claude-in-chrome__get_page_text` and find the **Organic Search** row: Sessions, Engaged sessions, Engagement rate, (Key events / Conversions).
4. For landing pages: **Reports → Engagement → Landing page** (or build an Explore with dimension *Landing page* + a *Session default channel group = Organic Search* filter); read sessions + conversions per page via `get_page_text` / `mcp__claude-in-chrome__javascript_tool`.
5. For update/period comparison, use GA4's date "Compare" toggle and read the deltas.

If a login/consent screen appears, STOP and ask the user to sign in. GA4 UI loads asynchronously — wait for tables to render before reading.

## Rate limits / gotchas
- **Property id is numeric** (e.g. `123456789`), not the "G-XXXX" measurement id — use the numeric one for the API.
- GA4 applies **thresholding/sampling** on some reports (especially with demographics or large ranges); large date spans may be sampled. Note when a report shows a sampling indicator.
- "Conversions" depends on which events the user marked as **key events** — confirm with the user what counts as a conversion.
- Channel grouping: "Organic Search" is the default channel group; custom groupings can shift attribution. Default channel group is the safe bet.
- API: Data API has per-property + per-project request quotas; batch metrics into one `runReport` call rather than many.

## Output shape
Produce this (API or browser); `--print-shape` prints it:
```json
{
  "property_id": "123456789",
  "period": "2026-04-22..2026-05-20",
  "channel": "Organic Search",
  "metrics": {
    "sessions": 8400, "engaged_sessions": 5900, "engagement_rate": 0.70,
    "conversions": 132, "avg_engagement_time_sec": 78.5
  },
  "top_landing_pages": [
    { "page": "/ai-headshots", "sessions": 2100, "conversions": 48 }
  ]
}
```
Feed `metrics` into the monitoring snapshot (`scripts/report.py monitoring`) alongside the GSC pull, and use it in the measuring-seo-results quarterly review.
