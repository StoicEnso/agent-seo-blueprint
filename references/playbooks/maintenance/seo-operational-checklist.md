---
title: SEO Operational Completeness Checklist
area: maintenance
source_lessons: []
operational_addition: true
source: "https://x.com/askokara/status/2079927487648383270"
---

# SEO Operational Completeness Checklist

## Purpose

Use this as a coverage ledger during a site audit and as a routing map for follow-up work. It preserves a 37-item public checklist while replacing slogan-level advice with evidence rules, conditionality, and clear workflow ownership.

This is **not** a universal ranking formula. A check passes only when there is inspectable evidence for the site, template, page, or data source being reviewed. Mark every row `pass`, `partial`, `fail`, `blocked`, or `not_applicable`; never infer success from a homepage spot-check.

## Evidence contract

For each applicable check, record:

- `check_id` and status
- affected URL(s), template(s), or property
- observed evidence and timestamp
- tool/source used (crawl, page source/render, GSC, Bing Webmaster Tools, PageSpeed/Lighthouse, Rich Results Test, live SERP, repository inspection)
- severity and business impact when failed
- owning workflow and next action

Sample representative URLs from every important template. Use GSC/indexing reports as the primary indexation evidence where available. A `site:` query is directional discovery evidence only; it is not an authoritative count of indexed URLs.

## 37-check matrix

| ID | Operational check | Pass evidence / hardening | Owner workflow |
|---|---|---|---|
| IDX-01 | Resolve indexing issues | Important URLs are eligible/indexed or have documented reasons; coverage evidence names affected URLs. | `site-audit.md` |
| ARC-01 | Add useful breadcrumbs | Breadcrumbs reflect real hierarchy, are visible, linked, and use matching `BreadcrumbList` only when valid. | `site-audit.md` → content/engineering |
| IDX-02 | Use correct canonical tags | Self-canonicals and cross-canonicals select the intended URL; no conflicting redirects/noindex/sitemaps. | `site-audit.md` |
| PERF-01 | Fix Core Web Vitals | Field data where available, lab data otherwise; inspect LCP, INP, CLS by template/device. | `site-audit.md` |
| ARC-02 | Fix orphan pages | Important indexable pages have contextual internal links; crawl plus sitemap/GSC comparison finds no unexplained orphans. | `site-audit.md` |
| SERP-01 | Add appropriate schema | Markup matches visible content, uses supported current types, and contains no fabricated ratings/entities. | `site-audit.md` |
| ONP-01 | Fix heading structure | One clear page topic, logical H1/H2/H3 hierarchy, no styling-only or keyword-stuffed headings. | `site-audit.md` / `content-production.md` |
| CON-01 | Write original content | Page provides first-hand value, useful synthesis, data, examples, media, or expertise beyond a rewrite. | `content-production.md` |
| CON-02 | Avoid duplicate content | Exact/near duplicates have a deliberate merge, canonical, redirect, or distinct-intent justification. | `site-audit.md` |
| AUT-01 | Earn high-quality backlinks | Acquired links are relevant, editorial/useful, and verified; authority is not reduced to DR alone. | `authority-and-links.md` |
| ARC-03 | Use clean descriptive URLs | URLs are stable, readable, concise, and migration-safe; do not churn URLs merely for keywords. | `site-audit.md` |
| ARC-04 | Fix broken links and 404s | Internal broken links are corrected; removed URLs return the right status or redirect to a true equivalent. | `site-audit.md` |
| IDX-03 | Confirm JavaScript content is crawlable | Key content/links are present in initial HTML where practical or reliably render for relevant crawlers; compare source and rendered DOM. | `site-audit.md` |
| CON-03 | Resolve keyword cannibalization | GSC/SERP evidence shows whether multiple URLs conflict; merge, retarget, or differentiate only when intent overlaps. | `site-audit.md` / `content-production.md` |
| PERF-02 | Make the site mobile friendly | Mobile layout, navigation, tap targets, forms, media, and checkout/conversion paths are usable; not just responsive at one width. | `site-audit.md` |
| TRUST-01 | Add authorship and E-E-A-T evidence | Authorship, review process, sources, policies, credentials, and entity facts are visible when relevant; bios alone are not proof. | `site-audit.md` / `content-production.md` |
| ONP-02 | Write strong titles | Unique, intent-matched titles communicate the page clearly. `50–60 characters` is drafting guidance, not a universal rule; inspect pixel truncation and live SERPs. | `content-production.md` / `site-audit.md` |
| ONP-03 | Write unique meta descriptions | Important pages have useful, non-duplicated descriptions; snippets may be rewritten by search engines and are not guaranteed. | `content-production.md` / `site-audit.md` |
| CON-04 | Merge thin or overlapping pages | Consolidation preserves useful material, redirects true replacements, updates internal links, and avoids merging distinct intents. | `site-audit.md` / `content-production.md` |
| ONP-04 | Optimize images and alt text | Images are correctly sized/compressed/lazy-loaded where appropriate; alt text describes functional/meaningful images and decorative images use empty alt. | `site-audit.md` / `content-production.md` |
| INT-01 | Match every page to search intent | Live SERP format and user job align with page type, promise, depth, and conversion path. | `research-and-ideation.md` / `content-production.md` |
| RES-01 | Find attractive keyword opportunities | Volume and KD are starting filters only; require intent, business value, cluster depth, page-level competition, and SERP winnability. | `research-and-ideation.md` |
| ARC-05 | Add internal links to important pages | Contextual links support user journeys and distribute authority; anchors are descriptive and not mechanically exact-match. | `content-production.md` / `site-audit.md` |
| CON-05 | Publish comparison/alternative pages when justified | Live demand and SERP format support them; comparisons are accurate, current, fair, and evidence-backed. | `content-production.md` |
| CON-06 | Produce best-of/list content only where the SERP rewards it | Methodology, inclusion criteria, hands-on evidence, freshness, and disclosures make the list defensible. | `content-production.md` |
| ARC-06 | Build topic clusters around useful hubs | Cluster pages have distinct intent, complete coverage, and bidirectional internal links; avoid thin page multiplication. | `research-and-ideation.md` / `content-production.md` |
| LOCAL-01 | Create/maintain Google Business Profile when eligible | Only for eligible real-world/local businesses; facts, categories, hours, location/service area, and policies are accurate. | `local-business-profile-audit.md` from `site-audit.md` |
| MON-01 | Monitor pages losing traffic or rankings | Compare periods in GSC/GA4, segment by query/page/device/country, annotate updates/releases, and diagnose before changing content. | `monitoring.md` |
| SERP-02 | Validate schema | Current Rich Results Test/schema validation passes where applicable; warnings are interpreted, and no rich-result appearance is promised. | `site-audit.md` |
| CON-07 | Create feature/use-case pages where demand exists | Each page has distinct audience/problem/intent, real product truth, proof, and a conversion path; avoid doorway pages. | `content-production.md` |
| FRESH-01 | Maintain truthful `dateModified` | Update only when the visible main content changes materially; retain update notes/evidence where useful. | `content-production.md` / `monitoring.md` |
| MON-02 | Improve page-two opportunities | Use GSC query/page evidence (roughly positions 11–20), inspect intent and competitors, then improve substance/internal links rather than blindly refreshing. | `monitoring.md` → content/authority |
| IDX-04 | Submit and monitor sitemaps | Submit valid canonical-only sitemaps to GSC and Bing Webmaster Tools when properties exist; monitor processing/errors. | `site-audit.md` / maintenance |
| IDX-05 | Audit robots.txt and noindex | Important URLs are not unintentionally blocked; blocked/noindexed pages match an explicit policy. | `site-audit.md` |
| MON-03 | Improve high-impression, low-CTR pages | Use GSC by query/page, control for position and SERP features, then test title/description/intent changes; CTR alone is not proof of a snippet problem. | `monitoring.md` |
| SERP-03 | Inspect branded/site SERP snippets | Use `site:domain` and normal queries to spot title/snippet anomalies, but confirm indexation in GSC and avoid rewriting solely to force an exact keyword. | `site-audit.md` / `monitoring.md` |
| RES-02 | Mine People Also Ask questions carefully | Use live PAA/related questions as research inputs; answer on the most appropriate page unless a standalone page has distinct demand and enough value. Do not promise FAQ rich results. | `research-and-ideation.md` / `content-production.md` |

## Brave Search URL submission and re-fetch (supplemental)

This optional engine-specific check supplements **IDX-01 / IDX-04 / IDX-05**. It does not add a 38th row to the original 37-check matrix. Route it through `workflows/site-audit.md` or `workflows/technical-seo-maintenance.md`, not the backlink/directory acquisition queue.

### Meaning and sources

The official form at [Brave URL submission](https://search.brave.com/submit-url) says **Insert the URL to be re-fetched**. [Brave's crawler documentation](https://search.brave.com/help/brave-search-crawler) links it for re-fetching pages, including applying a changed `noindex` directive or removing an unavailable result. The [Hridoy Reh post, 24 October 2026](https://x.com/hridoyreh/status/2114004776061182246) proposes submitting a website here. Its guaranteed-appearance claim is an unverified creator claim, not a provider guarantee.

A submitted re-fetch request is **not proof of indexing**, a backlink, ranking, referrals, leads, conversions, or revenue. Google/Bing sitemap submissions and IndexNow are different provider actions; do not use their receipts as Brave evidence.

### Read-only preflight

1. Define a bounded set of public URLs. A homepage request is not a full-site or sitemap submission. Exclude private, authenticated, staging, parameter-only, duplicate and deliberately excluded URLs.
2. Fetch the intended URL; record its final HTTP status, redirect destination, canonical tag, robots meta and `X-Robots-Tag`. Check current robots.txt access, including Googlebot: Brave documents that a page Googlebot cannot crawl will not be crawled by its crawler either. Crawl access is not indexing proof. Do not remove an intentional block or `noindex` setting without separate site-change approval.
3. Check Brave directly using dated `site:domain` and/or exact-URL or brand queries. Save the provider, actual query, locale where known, result URLs and evidence. `not_found_in_sample` is not proof of complete index absence; `visible` does not prove a prior submission. Record `not_checked` or `blocked` when appropriate rather than inventing a zero. Do not re-fetch merely because a `site:` count differs from a sitemap.
4. Inspect the existing per-URL ledger and prior provider receipts. A missing local record is **unknown**, not proof that submission never occurred. Keep previously accepted requests and avoid duplicate submissions. A new exact user request may authorize a single refresh of an already submitted URL; record that scope and reason.

### Explicitly approved execution only

The audit remains read-only by default. **Require explicit user approval** for the named public URLs before any Submit action. Copy `assets/brave-url-submission-tracker.csv` to `audits/<date>_brave-url-submissions.csv`. Do not create accounts, change crawler rules, spend, install anything, schedule retries, or call an undocumented submission endpoint under this approval.

For each approved URL:

1. Record approval evidence and check the prior receipt/attempt ledger. Record `submitted_at` and the single dispatch before clicking so an interrupted run cannot silently resubmit.
2. Open the official form, enter the verified canonical URL, and press **Submit once**. Use ordinary approved browser controls; respect rate limits and provider Retry-After instructions. No tight loops, bulk URL spray, CAPTCHA bypass or alternate-profile evasion.
3. Wait for the provider's real result. Save the submitted input, confirmation text, timestamp and screenshot or DOM receipt. Observed success can read **Submitted / Success / Thank you for your submission.** A disabled button, click success or screenshot filename alone is insufficient.
4. If the result is interrupted or ambiguous, set `submission_state=unknown_after_dispatch`, inspect the existing page/provider state and do not automatically retry. Set `blocked` or `rejected` with the actual reason when that is the observed result. A later write needs the original still-valid scoped authority or a new decision if scope changes.
5. Record subsequent read-only Brave checks separately. Keep `submission_state`, `visibility_state` and measured `referral_sessions`, `conversions` and `revenue` independent. Leave unmeasured fields blank or explicitly `not_measured`, never zero. A recheck date is a recommendation, not permission to create a scheduler job or re-submit.

### Evidence fields and completion

The CSV is a header-only template, not a live submission list. Keep one row per exact canonical URL and approved attempt. Required fields include approval evidence, preflight evidence, attempt count, submission state, provider receipt, query/result URLs, dated visibility state, and independent outcome measurements. Valid submission states: `not_submitted`, `submitted_accepted`, `rejected`, `blocked`, `unknown_after_dispatch`. Visibility states: `not_checked`, `visible`, `not_found_in_sample`, `blocked`. An audit `pass` cannot replace either state.

Done means every in-scope URL has an inspectable provider receipt or a precise unresolved result; a later indexing outcome remains separately measured. Existing positive search results do not erase a missing submission receipt, and a successful receipt does not turn an unconfirmed result into indexed. Preserve dates and update observations rather than rewriting historical evidence.

## Audit procedure

1. Define scope: whole site, key templates, or priority URLs. Record what is explicitly out of scope.
2. Build a coverage row for all 37 checks; use `not_applicable` only with a reason.
3. Run the owning workflow's evidence step instead of duplicating shallow checks here.
4. Convert every `fail`/`partial` into a finding with severity, affected URLs/templates, evidence, fix, owner, and verification method.
5. Group implementation work by dependency: crawl/indexation first, then architecture/performance, then content/intent, then authority/opportunity work.
6. Save the coverage matrix beside the normal audit findings so the next audit can diff status changes.

## Output schema

Write `audits/<date>_operational-seo-coverage.csv` with:

`check_id,status,scope,evidence_source,evidence,affected_urls,severity,owner_workflow,next_action,verified_at,notes`

## Done condition

All 37 checks have a status and evidence or an explicit `not_applicable` reason; failures are represented in the main severity-ranked audit; opportunity rows are routed to research/content/authority/monitoring; and no heuristic is reported as a guaranteed ranking factor.
