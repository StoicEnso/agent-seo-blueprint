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

## Sitemap cohort evidence (conditional)

When an indexation pattern needs investigation, record one metric/status observation row per logical cohort in a workspace copy of `assets/sitemap-cohort-evidence.csv`. Start with property/type, exact sitemap or index URL, membership source, current filter, capture date/source, report counts/states, and expected canonical-eligible set with exclusion limits. Record overlap/deduplication, representative URL Inspection evidence, alternative explanations and confidence before proposing a bounded fix.

The Sitemaps top-level report lists report/API submissions (an index detail can show auto-discovered children); Page Indexing sitemap membership may come from a report submission or `robots.txt`. A specific sitemap/index filter is not “All submitted pages.” A submitted or parsed sitemap is not proof of crawling or indexation, and Google fetch/processing success is not proof of indexation. Index and child counts may overlap; incomplete examples and the 1,000 displayed-submission limit are observations, not complete censuses. Keep a usable index in place; do not create nested indexes or prescribe routine child submissions for tiny or inapplicable sites.

A direct child submission may be proposed for a real filter/report gap after the exact URL, purpose, risks, planned rollback and follow-up are recorded. A proposal needs no new write grant. Execute only with valid exact owner write approval and a fresh scope/target check, then record the actual receipt; do not invent a receipt in advance. It is a reporting/discovery operation, not proof of a ranking, crawl or indexing improvement. Do not run validation or indexing-request loops.

### Evidence interpretation and record shape

One CSV row is one metric/status observation for an identified logical cohort and capture. Reuse `cohort_id` across its metric/reason rows. Keep `report_name`, `metric_name`, `metric_unit` and `collection_state` beside `report_count`; a blank count is unknown, whereas an observed zero is `0`. Allowed collection descriptions include `OBSERVED`, `MISSING_ACCESS`, `UNAVAILABLE`, `FAILED` and `PARTIAL`. Submission, processing and indexing states are separate fields, not synonyms for collection success. Link the source export, inventory version and inspection packet instead of copying a competing truth set.

Use the Page Indexing summary counts for the selected property/filter; the incomplete examples are a diagnostic sample, not their denominator. For an eligible-indexed ratio, require the same cohort, membership revision, reporting window and defined canonical-eligible denominator. If only a bound or mismatched/partial inventory exists, leave the ratio unknown. Keep intentional exclusions and not-yet-known URLs separate. Never add the parent index and overlapping child counts to make a site total.

`Crawled - currently not indexed` alone does not prove low quality, a crawl-budget problem or a template failure. Inspect representative affected and comparison URLs. Distinguish the indexed/cached state and selected canonical from a live fetch/render; a successful live test cannot prove that URL is indexed. Preserve alternate explanations, confidence reasons and the limits of the sample.

Removing a sitemap from the report does not remove its pages from the index. A rollback is a reviewed reporting/file-change plan, not promised deindexing or a guaranteed undo of discovery. `Validate fix`, request indexing, robots/file edits and submission/deletion are consequential actions, not inspection steps. Sitemap-scoped validation uses membership at request time; it is not an automatic whole-site test.

**Source basis, checked 7 October 2026:**
- Practitioner prompt: https://x.com/brodieseo/status/2107457558248358111; Nick's quoted endorsement: https://x.com/nickleroy/status/2107519993936048128. The screenshot shows a January 2025 property example, not a present-day universal rule.
- Sitemaps report/listing, index coverage, discovery and display limits: https://support.google.com/webmasters/answer/7451001?hl=en.
- Page Indexing filter membership, incomplete examples, canonical goals and validation scope: https://support.google.com/webmasters/answer/7440203?hl=en.
