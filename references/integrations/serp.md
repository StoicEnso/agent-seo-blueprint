# Integration: Live SERP (Google search results)

## What it provides
A read of what Google actually ranks for a query, right now:
- **Top organic results:** rank, title, URL, domain, and the **content TYPE** of each (tool, article, comparison, gallery, product, forum).
- **Dominant content type in the top 3** — the "appetite" Google rewards for that query (match-and-exceed).
- **SERP features:** featured snippet, People Also Ask, image/video pack, shopping, ads — strong **intent** signals.
- **Exceedability read:** are the top results thin/weak (beatable) or strong/well-linked?

**Consumed by:**
- `references/playbooks/research/match-and-exceed.md` — read the SERP, identify the format, judge if you can beat it.
- `references/playbooks/research/search-intent.md` — infer informational/commercial/transactional/navigational intent from the result mix + features.
- `references/playbooks/content/content-types-overview.md`, `content/on-page-optimization.md`, `content/articles.md` — pick the format that matches the SERP.
- `references/playbooks/research/finding-and-validating-niches.md` — sanity-check a niche by eyeballing its SERPs.
- Workflows: `research-and-ideation.md`, `content-production.md`.

## This integration is BROWSER-ONLY (no API)
There is **no compliant programmatic endpoint**. Live Google results are personalized, JS-rendered, and bot-protected. The agent reads the SERP itself with Chrome MCP tools. `scripts/serp_capture.py` is **not** an API client — it validates the query, builds the exact Google URL to open, and prints the capture procedure + output shape:
```bash
python3 scripts/serp_capture.py "ai headshot generator" --country us --top 10
python3 scripts/serp_capture.py "best crm for startups" --json   # machine-readable plan
```
It performs **no network calls**.

## Auth — browser path (the only path)
No login is required for a plain Google search, but the user must be on a normal browser session. The skill never solves challenges or signs in.
1. Get the URL from `serp_capture.py` (it sets `gl` country, `hl` language, `num`, and `pws=0` to reduce personalization).
2. `mcp__claude-in-chrome__navigate` → that URL.
3. **If a CAPTCHA, "unusual traffic," or consent wall appears: STOP.** Do not solve or bypass it. Tell the user to clear it manually, then resume. (See ToS notes.)
4. `mcp__claude-in-chrome__get_page_text` (or `read_page`) to grab the rendered results.
5. Extract, for the top N **organic** results (skip ads, but note their presence): rank, title, url, domain, content type.
6. Record SERP features present and infer intent. Judge the top-3 dominant type (the "appetite") and whether you can exceed it.
7. Use `mcp__claude-in-chrome__javascript_tool` only to read/structure on-page text (e.g. collect result blocks) — never to defeat anti-bot measures.

For competitor **on-page** structure (headings, word count, sections of a top result), navigate to that result URL and read it the same way — feeds `content/on-page-optimization.md` and `research/match-and-exceed.md`.

## Rate limits / gotchas / ToS
- **Personal-research volume only.** A handful of queries per session to inform decisions — NOT bulk/automated scraping. `serp_capture.py` caps `--top` at 50 to keep it human-scale.
- **Respect bot detection. NEVER bypass a CAPTCHA** or "unusual traffic" interstitial — stop and hand it to the user. Bypassing is against Google's ToS and out of scope for this skill.
- Results are **personalized + geo-dependent**; set the right `--country`. Even with `pws=0`, location/IP still influence results — treat readings as directional.
- SERPs are volatile and JS-heavy: wait for full render before reading; re-running can show different results.
- Do not store or redistribute scraped Google content beyond the user's own research artifacts.

## Output shape
Produce this per query (the agent saves it as a research note via `scripts/report.py note --subdir research`):
```json
{
  "query": "ai headshot generator",
  "country": "us",
  "captured_at": "2026-05-20",
  "dominant_content_type": "free tool",
  "results": [
    { "rank": 1, "title": "...", "url": "https://...", "domain": "...",
      "type": "tool", "notes": "polished generator, heavy backlinks" }
  ],
  "serp_features": ["people_also_ask", "image_pack", "ads"],
  "intent_read": "transactional",
  "exceedable": "maybe — top tools are strong; need authority first"
}
```
This drives the match-and-exceed verdict and the content-type choice for the keyword.
