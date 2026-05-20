# Integration: Google PageSpeed Insights (Lighthouse)

## What it provides
Lab + field performance data for a single URL:
- **Category scores (0-100):** Performance, Accessibility, Best Practices, SEO.
- **Core Web Vitals (lab, from Lighthouse):** LCP, CLS, INP, FCP, TBT, Speed Index, TTFB (server response time).
- **Field data (CrUX):** real-user percentiles + FAST/AVERAGE/SLOW buckets, when Google has enough traffic for the origin/page.

**Consumed by:**
- `workflows/site-audit.md` — page-speed + technical findings feed the severity-ranked fix list.
- Playbook `references/playbooks/maintenance/keyword-intent-evolution.md` — "optimize existing pages (page speed)" is a tracked maintenance action.
- Playbook `references/playbooks/maintenance/measuring-seo-results.md` — "existing pages optimized" leading indicator.

This is the **only integration that works with zero setup** — the API is public.

## Auth — API path (primary, fully implemented)
- **Script:** `scripts/pagespeed_run.py`
- **Env var (optional):** `PAGESPEED_API_KEY` — only raises the quota. Without it you still get results at the lower anonymous rate.
- **Endpoint:** `GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
- **Key params:** `url`, `strategy` (`mobile`|`desktop`), repeated `category` (performance/accessibility/best-practices/seo), optional `key`.

What the agent runs:
```bash
python3 scripts/pagespeed_run.py https://example.com --strategy mobile --pretty
python3 scripts/pagespeed_run.py https://example.com --strategy desktop   # second pass
```
Run **both** mobile and desktop for an audit; Google indexes mobile-first, so mobile is the priority score.

Example raw request (what the script issues):
```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile&category=performance&category=seo&key=$PAGESPEED_API_KEY
```

## Auth — browser fallback path
Rarely needed (the API is public), but if the API is blocked or quota-exhausted and you want a quick read:
1. `mcp__claude-in-chrome__navigate` → `https://pagespeed.web.dev/analysis?url=<URL-encoded target>` (no login required).
2. Wait for the run to finish (it can take 20-40s). `mcp__claude-in-chrome__get_page_text` to read the page.
3. Pull the two big numbers (Mobile / Desktop performance scores), the four category scores, and the Core Web Vitals values shown under "Diagnose performance issues."
4. The user does not need to be logged in for PageSpeed; if any Google sign-in/consent wall appears, direct the user to clear it — the skill never logs in.

## Rate limits / gotchas
- **Anonymous (no key):** a shared daily quota; you can hit HTTP 429 ("Quota exceeded ... Queries per day") quickly when the shared pool is busy. The script handles this gracefully (prints structured JSON error, hints to set a key, exits 0).
- **With key:** ~25,000 queries/day, ~240/min (default GCP quota). Set `PAGESPEED_API_KEY` for audit batches.
- A single run is one URL. For a site audit, run the handful of key templates/pages, not every URL.
- Lab metrics (Lighthouse) are a controlled-environment estimate; **field data (CrUX) is the source of truth** for real-user CWV — prefer it when present (`field_data_crux` is non-null).
- Timeouts: slow pages can take >60s; the script default is 90s (`--timeout`).

## Output shape
`scripts/pagespeed_run.py` prints this JSON (the agent stores it and/or maps it into `scripts/report.py` audit findings):
```json
{
  "url": "https://example.com",
  "strategy": "mobile",
  "fetched_url": "https://example.com/",
  "lighthouse_version": "11.0.0",
  "scores": { "performance": 98, "accessibility": 91, "best-practices": 100, "seo": 92 },
  "core_web_vitals_lab": {
    "LCP": { "value": 612.0, "display": "0.6 s", "score": 1.0 },
    "CLS": { "value": 0.0, "display": "0", "score": 1.0 },
    "INP": { "value": null, "display": null, "score": null },
    "FCP": { "value": 510.0, "display": "0.5 s", "score": 1.0 },
    "TBT": { "value": 0.0, "display": "0 ms", "score": 1.0 },
    "SpeedIndex": { "value": 510.0, "display": "0.5 s", "score": 1.0 },
    "TTFB": { "value": 40.0, "display": "Root document took 40 ms", "score": 1.0 }
  },
  "field_data_crux": {
    "LARGEST_CONTENTFUL_PAINT_MS": { "percentile": 800, "category": "FAST" }
  }
}
```
For an **audit**, turn weak scores into findings (e.g. `{ "area": "performance", "severity": "high", "issue": "Mobile LCP 4.1s (poor)", "fix": "...", "evidence": "PSI mobile" }`) and pass to `scripts/report.py audit`.

On error the script prints `{"error": ..., "status": ..., "detail": ...}` and exits 0 so pipelines continue.
