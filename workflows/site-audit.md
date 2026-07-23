---
title: Site Audit
goal: Audit a live site across technical, on-page, and content dimensions, then emit a prioritized, severity-ranked fix list.
playbooks:
  - references/playbooks/content/on-page-optimization.md
  - references/playbooks/content/content-what-not-to-do.md
  - references/playbooks/content/content-fundamentals.md
  - references/playbooks/content/content-types-overview.md
  - references/playbooks/research/match-and-exceed.md
  - references/playbooks/research/research-for-existing-sites.md
  - references/playbooks/maintenance/keyword-intent-evolution.md
  - references/playbooks/maintenance/seo-operational-checklist.md
  - references/playbooks/authority/understanding-authority.md
  - references/playbooks/authority/linkbuilding-what-not-to-do.md
scripts:
  - scripts/workspace.py
  - scripts/pagespeed_run.py
  - scripts/serp_capture.py
  - scripts/gsc_pull.py
  - scripts/ahrefs_client.py
  - scripts/report.py
integrations: [pagespeed, gsc, serp, ahrefs]
outputs:
  - audits/<date>_audit.md            # severity-ranked fix list (via report.py audit)
  - audits/<date>_audit-findings.json # raw findings payload
---

# Site Audit

**When to run this.** The user has a live site and asks "why isn't this ranking / converting", wants a health check before investing in content or links, or a page that used to rank has slipped. Read-only and safe — it inspects and reports; it changes nothing on the site.

**Prerequisites.**
- **Workspace** resolved (`python3 scripts/workspace.py status --path <DIR>`; ASK before creating if absent). The domain(s) should be in `project.json`.
- **From the user:** the domain + the key pages/keywords that matter most; ideally GSC property access.
- **Data sources:** PageSpeed/Lighthouse (`pagespeed_run.py`), live SERP + page scraping (`serp_capture.py`), Google Search Console (`gsc_pull.py`), Ahrefs (`ahrefs_client.py`). Each has a browser-MCP fallback in `references/integrations/<src>.md` when no API key/credentials are present. GSC/GA4 OAuth must be done by the user — the skill guides, never auto-auths.

**Steps.**

1. **Scope the audit.** List the URLs to inspect (priority pages from the user; or pull the top traffic pages via `ahrefs_client.py` Top Pages / `gsc_pull.py`). Decide how deep (single page, key templates, or whole site sample). Load `references/playbooks/maintenance/seo-operational-checklist.md`, create a 37-row coverage ledger, and record which URLs/templates represent each applicable check. Do not infer whole-site coverage from the homepage.

2. **Technical audit — speed & Core Web Vitals.** Load `references/playbooks/content/on-page-optimization.md` (page-speed section). Run `python3 scripts/pagespeed_run.py <url>` for each priority URL (browser-Lighthouse fallback in `references/integrations/pagespeed.md`). Flag slow loads (5–10s), poor CWV, and non-static pages that should be statically generated. Severity by impact on rankings/conversion.

3. **Technical audit — indexation & duplication.** From `on-page-optimization.md` (canonicals) and `references/playbooks/content/content-what-not-to-do.md` (duplicate content, crawl budget): check for parameterized/near-duplicate URLs without canonicals, duplicate meta titles/descriptions across templated pages, and mass-published pages straining crawl budget. Use `gsc_pull.py` coverage/indexation signals where available. A `site:` query via `serp_capture.py` is directional discovery evidence only, never an authoritative indexed-page count.

4. **On-page audit.** Per priority page, scrape it with `serp_capture.py` and check against `on-page-optimization.md`: meta title contains the main keyword AND matches search intent (no obscure titles that cause bounces); meta description uses variants; internal links present and pointing at related pages; H1/H2 structure sane. Record each gap as a finding.

5. **Content/intent audit.** Load `references/playbooks/content/content-fundamentals.md`, `content-types-overview.md`, and `references/playbooks/maintenance/keyword-intent-evolution.md`. For each key page, capture the live SERP for its target keyword (`serp_capture.py`) and check: does the page's **content type match the format Google now rewards**? An intent/format mismatch (e.g. a landing page where reviews now rank) is a high-severity finding with the fix "reformat to the now-preferred type." Also scan for thin content, keyword stuffing, AI-spam pages, and keyword cannibalization (two pages chasing one keyword) per `content-what-not-to-do.md`.

6. **Opportunity audit (gaps).** Load `references/playbooks/research/research-for-existing-sites.md`. Via `ahrefs_client.py`, surface low-effort wins: add-a-phrase Organic-Keyword wins, Content-Gap keywords, and competitor Top Pages worth building. These become positive "opportunity" findings (lower severity than breakage, but high ROI).

7. **Authority sanity check.** Load `references/playbooks/authority/understanding-authority.md` and `linkbuilding-what-not-to-do.md`. Via `ahrefs_client.py`, eyeball the backlink profile: is page-level authority too thin to rank the target keyword? Any toxic/spammy referring domains worth disavowing? Note as findings (deep link work routes to `authority-and-links.md`).

8. **Close the operational coverage ledger.** For every row in `seo-operational-checklist.md`, record `pass | partial | fail | blocked | not_applicable` plus evidence. Route research, content, authority, local, and monitoring opportunities to their owning workflows. Write `audits/<date>_operational-seo-coverage.csv`; `not_applicable` requires a reason.

9. **Score, rank, and emit the report.** Assign each finding a severity (`critical | high | medium | low`), an area (technical / on-page / content / intent / opportunity / authority), the issue, and the recommended fix (with evidence). Assemble `{summary, score?, findings:[...]}` and run `python3 scripts/report.py audit --workspace <DIR> --title "Site audit: <domain>" --data <findings.json>`. `report.py` sorts findings by severity into a prioritized table → `audits/<date>_audit.md`. Save the raw payload too (`report.py note ... --subdir audits --name audit-findings`).

**Decision points.**
- **Drop with a confirmed Google update** → treat as a content-quality/value finding (audit helpfulness) per `keyword-intent-evolution.md` / maintenance.
- **Drop with no update** → suspect intent/format shift (step 5) or competitor backlink momentum (step 7) before anything else.
- **Severity calls:** site-breaking/indexation issues = critical; intent mismatch on a money page = high; thin/missing metadata = medium; nice-to-have opportunities = low.
- **Found toxic links?** Flag for disavow but route the actual disavow workflow to `authority-and-links.md` (it touches Search Console).

**Outputs.**
- `audits/<date>_audit.md` — prioritized, severity-ranked fix list (Markdown table from `report.py`).
- `audits/<date>_audit-findings.json` — raw findings for re-rendering or diffing against the next audit.
- `audits/<date>_operational-seo-coverage.csv` — evidence/status for all 37 operational checks.

**Done when.** Every priority URL has been checked across technical, on-page, content/intent, opportunity, and authority dimensions; all 37 operational checks have evidence-backed statuses or explicit `not_applicable` reasons; all findings carry a severity + concrete fix; and the ranked report plus coverage ledger are written to the workspace. Hand high-ROI content fixes to `content-production.md`, link findings to `authority-and-links.md`, and set a re-audit cadence in `monitoring.md`.
