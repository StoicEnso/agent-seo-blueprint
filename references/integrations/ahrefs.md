# Integration: Ahrefs

## What it provides
Ahrefs is the backbone metric source for research and authority work:
- **Keyword data:** search volume, Keyword Difficulty (KD), CPC, global vs. country volume, parent topic, "also ranks for."
- **Authority data:** Domain Rating (DR), URL Rating (page-level authority), referring domains, total backlinks.
- **Backlink data:** referring domains and individual backlinks (anchor, DR of source, first-seen date) — the raw material for link stealing and outreach.
- **Site/competitor overview:** organic traffic estimate, organic keyword count, top pages.

**Consumed by:**
- `references/playbooks/research/seo-metrics.md` — KD/DR/URL-rating/volume/CPC thresholds.
- `references/playbooks/research/competitor-research.md`, `research/match-and-exceed.md` — page authority of top-3 results.
- `references/playbooks/research/keyword-fundamentals.md`, `research/keyword-to-sitemap.md`, `research/finding-and-validating-niches.md` — keyword lists + filters.
- `references/playbooks/authority/link-stealing.md`, `authority/understanding-authority.md`, `authority/manual-outreach.md`, `authority/acquiring-domain-authority.md`, `authority/other-link-building.md` — backlinks + DR.
- `references/playbooks/content/programmatic-seo.md`, `content/free-tools-strategy.md` — keyword discovery at scale.
- Workflows: `research-and-ideation.md`, `authority-and-links.md`, `site-audit.md`.

## Auth — API path
- **Script:** `scripts/ahrefs_client.py`
- **Env var:** `AHREFS_API_KEY` (Ahrefs API v3 token, Bearer auth). Requires a plan tier that includes API access — confirm the user's plan; many web subscriptions do NOT include API, in which case the browser fallback below is primary.
- **Base:** `https://api.ahrefs.com/v3` — header `Authorization: Bearer $AHREFS_API_KEY`.

What the agent runs:
```bash
python3 scripts/ahrefs_client.py overview  --target ahrefs.com
python3 scripts/ahrefs_client.py keywords  --keyword "ai headshot generator" --country us
python3 scripts/ahrefs_client.py backlinks --target competitor.com --limit 25
```
If `AHREFS_API_KEY` is not set, the script prints a clear message + a per-command pointer and exits 2 — branch to the browser fallback.

**Endpoint note:** v3 paths/params vary by subscription and evolve over time. The client targets the documented v3 REST shape (e.g. `/site-explorer/overview`, `/keywords-explorer/overview`, `/site-explorer/backlinks`). If a call returns 404/403, the endpoint/plan differs — fall back to the browser path, which always works with a normal web login.

## Auth — browser fallback path (primary if no API)
The user must already be logged into Ahrefs at `app.ahrefs.com`. The skill never enters credentials.

**A. Domain / page overview (DR, referring domains, backlinks, traffic):**
1. `mcp__claude-in-chrome__navigate` → `https://app.ahrefs.com/site-explorer` (or paste the target into Site Explorer).
2. Enter the target domain or exact URL; pick mode (Domain / *.domain / Prefix / Exact URL).
3. `mcp__claude-in-chrome__get_page_text` and read the Overview cards: **Domain Rating (DR)**, **URL Rating (UR)** for a specific page, **Referring domains**, **Backlinks**, **Organic traffic**, **Organic keywords**.

**B. Keyword metrics (volume, KD, CPC):**
1. `navigate` → `https://app.ahrefs.com/keywords-explorer`.
2. Enter the keyword(s); set the country (default US — usually highest CPC market; check Global too).
3. `get_page_text` and read **Volume**, **Keyword Difficulty (KD)**, **CPC**, **Global volume**, **Parent topic**.
4. For lists, open the "Matching terms" / "Related terms" report and read the table (use `javascript_tool` to extract rows if the table is large).

**C. Backlinks / referring domains (for link stealing + outreach):**
1. In Site Explorer for the target, open **Backlinks** or **Referring domains**.
2. Sort by DR or "first seen" (recency). `get_page_text` / `javascript_tool` to extract: linking domain, DR of source, anchor, target URL, first-seen date.

If a login wall or 2FA prompt appears, STOP and ask the user to log in — never enter credentials or complete auth for them.

## Rate limits / gotchas
- **API:** v3 spends "units" per row/endpoint against your plan quota; batch queries and request only needed columns. 401/403 = bad/expired token; 429 = rate limit.
- **Browser:** Ahrefs throttles rapid navigation; keep it to a human pace. Heavy report pages are JS-rendered — wait for load before reading. Some reports are paginated; capture the top rows you need, don't crawl everything.
- **Authority is logarithmic** (per `seo-metrics.md`): each ~10 DR points ≈ 10× link value — read DR/UR with that in mind.
- Prefer **URL Rating (page-level)** over DR when judging whether a specific top-3 result is beatable.

## Output shape
Whether via API or browser, normalize to these shapes so they feed `scripts/report.py` (keywords) and the playbooks:

**Keyword row** (one per keyword; many → `scripts/report.py keywords`):
```json
{ "keyword": "ai headshot generator", "volume": 18000, "kd": 12, "cpc": 2.40,
  "global_volume": 41000, "intent": "transactional", "current_rank": null,
  "target_url": "", "priority": "high", "cluster": "headshots", "notes": "weak top-3 PA" }
```

**Domain/URL overview:**
```json
{ "target": "competitor.com", "mode": "domain", "dr": 62, "ur": null,
  "referring_domains": 1840, "backlinks": 12500, "org_traffic": 220000, "org_keywords": 31000 }
```

**Backlink row:**
```json
{ "source_domain": "blog.example.org", "source_dr": 54, "anchor": "best headshot tool",
  "target_url": "https://competitor.com/", "first_seen": "2026-03-02", "dofollow": true }
```
