# Integration: DataForSEO

## What it provides
DataForSEO is the low-cost, API-first data backbone for this skill when we need structured data at more than browser/manual scale:

- **Keyword volume/CPC/competition:** Google Ads Keyword Data API, up to 1,000 keywords per task.
- **Keyword ideas and cluster sizing:** DataForSEO Labs Google keyword ideas, including volume, CPC, KD-like `keyword_difficulty`, intent, SERP features, and average backlink/referring-domain signals for ranking pages.
- **SERP snapshots:** Google Organic SERP API, including top organic results, SERP feature types, domains, titles, descriptions, and check URLs.
- **Backlink rows:** Backlinks API for competitor link-stealing, outreach target discovery, and backlink pace monitoring.
- **Account/budget control:** user-data endpoint, dry-runs, and public-price estimates before spending.

**Consumed by:**
- `workflows/research-and-ideation.md` — bulk keyword volume, keyword ideas, SERP validation, cluster sizing.
- `workflows/content-production.md` — structured SERP rows and pSEO long-tail sizing.
- `workflows/site-audit.md` — keyword opportunity enrichment, SERP/intent checks, backlink sanity checks.
- `workflows/authority-and-links.md` — backlink opportunity rows.
- `workflows/monitoring.md` — competitor backlink pace and periodic SERP refreshes.

Use **DataForSEO** when the job is bulk, structured, repeatable, or cost-sensitive. Use **Ahrefs** when you need the UI-specific reports, DR/UR, Content Gap, Top Pages, or a logged-in browser fallback.

## Auth — API path
- **Script:** `scripts/dataforseo_client.py`
- **Env vars:** `DATAFORSEO_LOGIN` + `DATAFORSEO_PASSWORD`.
  - Also accepts `DATAFORSEO_API_LOGIN` + `DATAFORSEO_API_PASSWORD`.
- **Private env autoload:** if the shell env is missing, the helper checks `SEO_API_ENV`, then `~/.secrets/seo-api.env`, then `/root/.secrets/seo-api.env` without printing secrets.
- **Base:** `https://api.dataforseo.com`
- **Auth:** HTTP Basic auth using credentials from `https://app.dataforseo.com/api-access`.
- **Secrets rule:** never write the login/password into `project.json`; the workspace only records env-var names.

Credential check:
```bash
python3 scripts/dataforseo_client.py user-data
```

No credentials? You can still estimate cost and inspect payloads:
```bash
python3 scripts/dataforseo_client.py estimate keyword-volume --count 2500 --mode standard
python3 scripts/dataforseo_client.py keyword-volume --keyword "ai headshot generator" --dry-run
python3 scripts/dataforseo_client.py serp --keyword "ai headshot generator" --depth 20 --live --dry-run
```

Location-code lookup is free. Country filtering uses an optional GET JSON field; the path remains `/locations`:
```bash
python3 scripts/dataforseo_client.py locations --api serp --country us --dry-run
python3 scripts/dataforseo_client.py locations --api google-ads --country us --dry-run
```
- SERP locations path: `/v3/serp/google/locations`
- Google keyword-data locations path: `/v3/keywords_data/google/locations`

## Common commands

### 1) Keyword volume / CPC / competition
Cheapest default is standard queue. It returns a task id; retrieve later with `keyword-volume-get`.
```bash
python3 scripts/dataforseo_client.py keyword-volume \
  --keywords "ai headshot generator,professional headshot ai" \
  --location-code 2840 --language-code en

python3 scripts/dataforseo_client.py keyword-volume-ready
python3 scripts/dataforseo_client.py keyword-volume-get --id <task-id>
```

Live mode for immediate but slightly pricier results:
```bash
python3 scripts/dataforseo_client.py keyword-volume \
  --keyword "ai headshot generator" \
  --location-code 2840 --language-code en --live
```

### 2) Keyword ideas / cluster sizing / KD-like difficulty
```bash
python3 scripts/dataforseo_client.py keyword-ideas \
  --keyword "ai headshot" \
  --location-code 2840 --language-code en \
  --include-serp-info --limit 100
```

Optional filters are JSON arrays. Example: search volume > 100 and keyword difficulty <= 20:
```bash
python3 scripts/dataforseo_client.py keyword-ideas \
  --keyword "ai headshot" --limit 100 \
  --filters '[["keyword_info.search_volume",">",100],"and",["keyword_properties.keyword_difficulty","<=",20]]'
```

### 3) Google Organic SERP
Live structured SERP:
```bash
python3 scripts/dataforseo_client.py serp \
  --keyword "ai headshot generator" \
  --location-code 2840 --language-code en \
  --depth 10 --top 10 --live
```

Standard queue:
```bash
python3 scripts/dataforseo_client.py serp --keyword "ai headshot generator" --depth 10
python3 scripts/dataforseo_client.py serp-ready
python3 scripts/dataforseo_client.py serp-get --id <task-id> --kind advanced
```

### 4) Backlinks
```bash
python3 scripts/dataforseo_client.py backlinks \
  --target competitor.com \
  --mode as_is --dofollow --limit 100
```

With a custom filter:
```bash
python3 scripts/dataforseo_client.py backlinks \
  --target competitor.com \
  --filters '["domain_from_rank",">",250]' \
  --limit 100
```

### 5) Raw escape hatch
Use only when the helper does not yet expose a needed endpoint:
```bash
python3 scripts/dataforseo_client.py raw --method GET --path /v3/appendix/user_data
python3 scripts/dataforseo_client.py raw --method POST --path /v3/dataforseo_labs/google/keyword_ideas/live --data @payload.json
```

## Pricing snapshot / cost rules
Always run `estimate` or `--dry-run` before a large pull.

- **Minimum payment/top-up:** $50.
- **Google Ads keyword volume:**
  - Standard queue: $0.05 per task; up to 1,000 keywords/task; about $50 per 1M keywords.
  - Live: $0.075 per task; about $75 per 1M keywords.
- **Google Organic SERP:**
  - Standard queue: $0.0006 per SERP page (10 results); subsequent result pages cost 75% of base.
  - Priority queue: $0.0012 per first SERP page.
  - Live: $0.002 per first SERP page.
  - Top 100 standard is about $0.00465; top 100 live is about $0.0155.
- **DataForSEO Labs Google:**
  - Search intent: about $0.001/task + $0.0001/keyword.
  - Most other endpoints: about $0.01/task + $0.0001/item.
  - `include_clickstream_data=true` can multiply cost by 2.
- **Backlinks API:**
  - $100/month minimum commitment, redeemed to account balance.
  - $0.02/request + $0.00003/row.
  - Up to 1,000 rows/request; 1,000 backlink rows ≈ $0.05.

Estimator examples:
```bash
python3 scripts/dataforseo_client.py estimate keyword-volume --count 2500
python3 scripts/dataforseo_client.py estimate serp --queries 100 --depth 10 --mode standard
python3 scripts/dataforseo_client.py estimate keyword-ideas --requests 5 --limit 100
python3 scripts/dataforseo_client.py estimate backlinks --rows 5000
```

## Limits / gotchas
- General rate limit: **2,000 requests/minute**.
- Live Google Ads keyword endpoints: **12 requests/minute**; for bulk, use standard queue.
- Tasks-ready endpoints: **20 requests/minute**; prefer callbacks/postbacks for production systems.
- Database APIs including Labs, Backlinks, OnPage: max **30 simultaneous requests**.
- Recommended `task_post` batch: up to **100 tasks/request**; Google Ads keyword volume task supports up to **1,000 keywords** in the task's `keywords` array.
- Google Ads may combine or suppress similar keywords; submit close variants separately when exact separation matters.
- DataForSEO backlink `domain_from_rank` / `page_from_rank` are **not Ahrefs DR/UR**. Label them as DataForSEO rank signals, not DR.
- DataForSEO SERP snapshots are structured and scalable, but for final match-and-exceed judgment the browser SERP can still be useful for visual format/context.
- 402xx errors usually mean payment, cost limit, rate limit, duplicate-task limit, IP whitelist, too many simultaneous queries, or insufficient funds. Check `scripts/dataforseo_client.py user-data` and the DataForSEO dashboard.

## Output shapes
The helper normalizes common live/get responses to shapes that plug into `scripts/report.py`.

**Keyword row** (`keyword-volume`, `keyword-ideas`; write with `report.py keywords`):
```json
{
  "keyword": "ai headshot generator",
  "volume": 18000,
  "kd": 12,
  "cpc": 2.4,
  "competition": "HIGH",
  "intent": "transactional",
  "serp_features": ["organic", "people_also_ask"],
  "avg_referring_domains_top_serp": 24.5,
  "current_rank": null,
  "target_url": "",
  "priority": "high",
  "cluster": "headshots",
  "notes": "DataForSEO Labs keyword ideas"
}
```

**SERP snapshot** (`serp`):
```json
{
  "query": "ai headshot generator",
  "country": 2840,
  "language": "en",
  "captured_at": "2026-05-25 19:00:00 +00:00",
  "dominant_content_type": "unknown",
  "results": [
    {"rank": 1, "title": "...", "url": "https://...", "domain": "...", "type": "organic", "description": "..."}
  ],
  "serp_features": ["people_also_ask", "images"],
  "intent_read": "",
  "exceedable": "needs human/course review",
  "check_url": "https://www.google.com/search?..."
}
```

**Backlink row** (`backlinks`):
```json
{
  "source_domain": "blog.example.org",
  "source_url": "https://blog.example.org/post",
  "source_rank": 716,
  "source_page_rank": 897,
  "anchor": "best headshot tool",
  "target_url": "https://competitor.com/",
  "first_seen": "2026-03-02 00:00:00 +00:00",
  "last_seen": "2026-05-01 00:00:00 +00:00",
  "dofollow": true,
  "external_links": 22,
  "spam_score": 0,
  "source_dr": null,
  "notes": "DataForSEO rank is not Ahrefs DR"
}
```

## Browser fallback
None. DataForSEO is API-only. If credentials/funds are absent, use:
- `ahrefs_client.py` + `references/integrations/ahrefs.md` for Ahrefs browser fallback.
- `serp_capture.py` + `references/integrations/serp.md` for personal/manual live SERP reads.
