# Integration: Bing Webmaster Tools (BWT)

## Purpose and boundary

Read observed Bing search performance for an already verified site: page/query impressions, clicks, CTR and average position when exposed. Use it to discover page-specific query gaps alongside Google Search Console; see the optional Google + Bing branch in `references/playbooks/maintenance/content-opportunity-audit-and-measurement.md`.

This is an **export/browser reference, not a new API client**. No Bing script, authentication setup, account import, verification, API parity or automatic collection is claimed. Prefer authorized saved exports; otherwise use approved normal browser controls on an already authenticated site. Follow the existing skill authentication gate if a login/consent screen appears. Do not import GSC sites, grant new scopes or change DNS during a read-only review.

## Bounded collection

1. Open `https://www.bing.com/webmasters/` and select the exact verified site.
2. Open Search Performance and record the selected search surface/report and complete date window. Verify current controls; navigation may change.
3. Select the exact page or Page details view if available. Confirm the selected URL/canonical and read its associated search keywords. Do not relabel a site-wide keyword list as that page's data.
4. Export the returned keywords and available metrics, preserving original headers and the selected filters. Record country/device/search type only where the live report exposes them; unsupported dimensions stay unavailable.
5. Save the export and minimal screenshot evidence with collection time, property, page filter, dates, report timezone (or unknown), scope, row cap/pagination, finality and omissions. Export capability does not prove that all query rows were returned.
6. If page-query mapping, export, metrics or access is missing, record a partial/unavailable state and continue a labeled single-engine review. Never fabricate an empty export to stand in for failure.

Rate-safe collection is one bounded sequence per source, not many parallel agents. Respect access controls and provider limits. Keep private query exports in the project workspace, not in public PRs; exclude personal data and credentials from examples.

## Metric interpretation

- Preserve the reported engine/surface. Record an unknown surface instead of assuming all dashboard traffic is ordinary Bing web search.
- Keep Bing metrics separate from Google; the same query may have different audiences, result layouts, positions and counting definitions.
- A missing Google query row does not disqualify a Bing observation, and does not prove Google has no demand or ranking.
- Preserve observed zero versus unavailable values. Retain provider notes and source UI placeholders rather than silently treating every exported zero as an observation.
- Do not label query impressions as market search volume, unique people, conversions, AI citations or profit. No Copilot/ChatGPT attribution follows from a Bing query table.
- URL submission and IndexNow are writes, require exact approval, and do not guarantee indexing or rankings. This collection does neither.

## Primary references and evidence limits

Reviewed 7 November 2026:
- [Bing: Start Using Bing Webmaster Tools to Improve Your Site Visibility](https://blogs.bing.com/webmaster/2025/6/Start-Using-Bing-Webmaster-Tools-to-Improve-Your-Site-Visibility/) (17 June 2025): describes impressions, clicks and average position across pages and keywords. Retention and features are mutable; inspect the current report rather than hard-code a promise.
- [Bing Search Performance help](https://www.bing.com/webmasters/help/search-performance-c680da36): official help entry; this review's direct fetch returned only the JavaScript shell. A search excerpt is not a full documentation capture or a live authenticated dashboard check.
- [Google Search performance overview](https://support.google.com/webmasters/answer/7576553?hl=en): supports keeping report dimensions/aggregation and export limitations explicit. The reviewed extraction was partial; no claim of exhaustive current documentation review.

No customer property was accessed for this source update. The creator screenshot is reference evidence only.
