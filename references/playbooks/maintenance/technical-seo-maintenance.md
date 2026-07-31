# Technical SEO Maintenance

Technical SEO is not a one-off audit. Treat it like weekly plumbing: small verified fixes compound, especially on content-heavy SaaS, marketplaces, and programmatic SEO sites.

## Core operating principle

Every week, pull the site evidence, ask "what's broken?", and fix the highest-leverage small issues before they grow into ranking, crawl, conversion, or AI-citation problems.

Useful inputs:
- Google Search Console exports: pages, queries, impressions, clicks, CTR, average position, indexing/coverage where available.
- PageSpeed / CrUX / Lighthouse: Core Web Vitals and performance regressions.
- Live crawl/sample checks: raw HTML, rendered DOM, canonicals, redirects, robots, sitemap, status codes.
- Structured-data validation: article/product/FAQ/breadcrumb/org/schema consistency.
- Recent publishing log: newly shipped pages, templates, programmatic batches, and content updates.

## Weekly technical audit checklist

1. **Indexation and crawlability**
   - Important pages are indexable, canonicalized to themselves or the intended canonical, included in sitemap when appropriate, and internally linked.
   - Flag accidental `noindex`, robots blocks, stale sitemap entries, orphaned pages, crawl traps, duplicate parameter pages, or canonical chains.

2. **Redirect hygiene**
   - Check common chains such as `http -> https -> www` or legacy slugs bouncing through multiple hops.
   - Flag redirect chains, loops, old internal links pointing at redirected URLs, and inconsistent preferred host/protocol.

3. **Structured data / schema**
   - Validate JSON-LD and avoid duplicate schema on templated pages.
   - Use appropriate schema for page type: Article, Product/SoftwareApplication, FAQPage where genuinely useful, BreadcrumbList, Organization, WebSite.
   - Prefer important schema in initial HTML where practical; JS-injected schema may be delayed or missed by some fetchers.
   - Do not overstate harmless legacy rich-result markup as critical; severity depends on page value and whether a feature/result is blocked.

4. **Rendering and hydration**
   - Compare raw HTML and rendered DOM for key answers, pricing, product details, author/trust info, and schema.
   - Flag JS-only critical content, hydration bugs that change or hide content, mobile/desktop content mismatch, and render-blocking bundles.

5. **Core Web Vitals and page speed**
   - Use CrUX field data when available; Lighthouse is a proxy.
   - Diagnose LCP by subpart: TTFB, resource load delay, resource load duration, element render delay.
   - Flag heavy JS, unoptimized hero images, layout shifts, blocking third-party scripts, and slow server response.

6. **Metadata and SERP snippets**
   - Titles and descriptions should be unique, intent-matched, and not obviously truncated or duplicated at scale.
   - Flag missing titles/descriptions, duplicate template titles, misleading snippets, and pages where GSC shows impressions but poor CTR.

7. **Internal links and crawl depth**
   - Important pages should be reachable from relevant hubs, nav, or related content.
   - Flag orphaned pages, broken links, generic anchors, missing hub→spoke links, and new pages with no incoming internal links.

8. **Duplicate/thin programmatic pages**
   - For marketplace or pSEO sites, every indexable item/template page needs a unique title, useful description, and structured data.
   - Flag thin near-duplicates, pages created before enough source data exists, cannibalized pages targeting the same query, and templated pages missing distinguishing value.

9. **Trust, security, and hygiene**
   - Check HTTPS consistency, mixed content, exposed debug pages/secrets, broken media, missing trust/commercial pages, and outdated screenshots/pricing on important pages.

## GSC patterns worth investigating

- **Impressions up, CTR down:** snippet/title mismatch, SERP feature change, weak meta, or intent shift.
- **Impressions stable, position/clicks down:** competing pages improved, intent format shifted, or page no longer matches query task.
- **Page coverage collapse:** indexation/canonical/sitemap/internal-linking issue or demand moving to a different page/query cluster.
- **New pages not gaining impressions:** crawl depth, sitemap, internal links, canonical/noindex, or insufficient uniqueness.
- **High bounce/low engagement on article pages:** performance/hydration issue, intent mismatch, intrusive layout, or answer buried too low.

## Recurring cadence recommendation

Default for active content-heavy sites:
- **Weekly:** light technical SEO audit + leading-indicator checklist.
- **Monthly:** traffic/rank trend review from GSC/GA4.
- **Quarterly:** leading-vs-trailing analysis — did shipped work create measurable ranking/traffic movement?

When a workspace has a live/indexable domain and no existing recurring SEO technical audit or monitoring schedule, proactively suggest creating one. Do **not** create or modify schedules without user confirmation.

The recurring job should:
- run the technical audit workflow against a bounded URL sample,
- write reports to the workspace,
- alert only on critical/high findings, material movement, or data/auth blockers,
- avoid noisy weekly pings when only low-priority cleanup is found,
- name the project/domain in the job so future runs can detect it and avoid duplicates.

## Output shape

Each finding should include:
- severity: `critical | high | medium | low`
- area: `technical | indexation | schema | performance | rendering | metadata | internal-links | trust`
- evidence: URL + metric/snippet/report path
- fix: concrete next action
- owner lane: `engineering | content | analytics | authority | manual-review`

Good weekly output is not "SEO looks fine." Good output is: "Here are the 3 fixes that matter, 7 small cleanup items logged, and no schedule gap / schedule proposed."
