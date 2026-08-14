---
title: Contextual Internal-Link Architecture Audit
area: maintenance
operational_addition: true
source_scope: Dated observational study of 534,888 internal links across 38 B2B SaaS sites; useful for audit hypotheses, not causal thresholds
field_input: https://x.com/borjafat/status/2087509184585646163
---

# Contextual Internal-Link Architecture Audit

Use this when a site has many pages, priority commercial pages receive weak internal support, orphan risk is unclear, or total internal-link counts are dominated by navigation, footer, documentation, or template links. The aim is to improve discovery and user journeys with relevant editorial links. It is not a fixed link quota or ranking guarantee.

## Evidence boundary

The source study reported associations between contextual inbound links and whether sampled B2B SaaS pages ranked for any US organic query. It also disclosed confounding and crawl-cap limits. Pages that already matter may attract more editorial links, so the observed association does not prove that adding a fourth link caused ranking.

Treat all supplied numbers—including four links, 24.7%, 12.2%, 67.8%, and anchor-text differences—as dated field observations. Do not use them as a universal audit pass/fail rule, forecast, or client benchmark.

## 1. Define the priority set

Start with pages selected from business and search evidence:

- product, service, category, comparison, pricing, signup, or other conversion pages;
- valid GSC opportunities and pages with declining internal support;
- new or recently updated pages that serve a distinct intent;
- useful documentation or resources that should help a visitor complete a task.

Record the page's job, canonical URL, indexability, target audience, supporting topic cluster, current performance evidence, and desired user next step. Do not send links toward a page only because it is not ranking. Fix intent, quality, canonical, and indexation failures first.

## 2. Build an edge-level crawl record

Export internal links as individual source→destination edges where possible. Preserve:

- source URL and destination URL after canonical normalization;
- discovery location such as body/main content, navigation, footer, sidebar, related-content module, breadcrumbs, or unknown;
- anchor text and accessible name;
- followability, status, redirect, nofollow state, and canonical result;
- source and destination template/page type;
- DOM or extractor evidence for the placement;
- crawl date and crawl coverage limits.

Do not classify a link as contextual from destination frequency alone. A frequency rule can create a **template-link candidate set**, but inspect representative templates and DOM positions before final classification. Repeated related-content modules may still help users, while a manually inserted link can appear across templated pages.

## 3. Separate link classes before counting

Report at least:

- contextual body/main-content links;
- navigation/footer/breadcrumb/sitewide links;
- templated related-content/sidebar links;
- unknown/unclassified links.

Show both total inbound links and unique linking pages. Deduplicate repeated components where the audit question requires it. Preserve each class instead of deleting template links from the source evidence.

## 4. Find and verify orphan candidates

A crawl-observed orphan is not automatically a true orphan. Reconcile the crawl against:

- XML sitemap and canonical inventory;
- content management system or route inventory when available;
- GSC indexed/performance pages;
- analytics landing pages;
- known feeds, pagination, faceted routes, and pages outside the crawl scope.

Classify each candidate:

- `true_orphan_priority` — valid indexable page with no useful discovered inbound path;
- `weakly_linked_priority` — has links, but they are irrelevant, hidden in low-use templates, broken, or too deep;
- `intentional_orphan` — login, campaign, legal, utility, duplicate, or other intentionally isolated page;
- `crawl_scope_unknown` — evidence is incomplete.

Do not add links to pages that should be redirected, merged, noindexed, removed, or kept isolated.

## 5. Audit destination concentration

Measure how contextual links are distributed by destination and page type. Review the highest-share pages manually. A concentration is not automatically bad: hubs, documentation roots, and core tools may deserve broad support.

Flag concentration only when it exposes a mismatch, such as:

- low-value or obsolete destinations absorbing many editorial links;
- redirects or non-canonical pages receiving links;
- generic pages receiving support while higher-value, intent-matched pages are isolated;
- a template module creating apparent editorial support;
- priority pages buried at excessive click depth.

## 6. Map relevant source opportunities

For each priority destination, find source pages that:

- serve a related intent or answer a prerequisite question;
- contain a passage where the link helps the reader continue;
- are live, canonical, indexable when appropriate, and not themselves thin or obsolete;
- do not already provide an equivalent useful link;
- can use an accurate descriptive anchor without forcing a keyword.

Rank opportunities by reader usefulness, topical relationship, source visibility/traffic when available, destination need, and implementation cost. Do not prioritize solely by link count.

## 7. Write useful anchors

Use concise anchors that describe the destination in the source sentence. Natural variation should follow context and page meaning, not a mechanical synonym or exact-match quota.

Reject:

- repeated generic labels such as “learn more” when a clearer label is possible;
- forced exact-match anchors that make prose unnatural;
- fabricated variants created only to imitate a field-study correlation;
- links inserted where they interrupt or mislead the reader;
- anchors that promise content the destination does not provide.

Accessibility comes first: the anchor or accessible name should make sense out of context.

## 8. Recommend a bounded change set

Use `four contextual links` only as a review trigger if the project chooses it, never as an automatic fix or success threshold. A page may need zero, one, or many links depending on its role and cluster.

Each recommendation should include:

- source and destination URL;
- link class and proposed placement;
- exact reader benefit;
- proposed anchor or sentence context;
- current evidence and checked date;
- risk or dependency;
- owner and status (`proposed | approved | implemented | rejected | not_applicable`).

Draft the changes. Do not edit a content management system or publish links without approval.

Suggested artifact: `audits/<date>_internal-link-architecture.json`.

## 9. Measure without claiming causality

Before and after an approved release, track separately:

- crawl discovery, true-orphan count, click depth, broken/redirected edges, and representation parity;
- GSC impressions, clicks, average position, and query count for the same page set;
- user navigation or conversion data when available;
- release date, concurrent content/technical/link changes, and observation window.

Improvement after the release is temporal association unless the design supports stronger causal inference. Do not promise a ranking-position gain. The source study itself reported near-zero association with position among pages that already ranked.

## Done when

Priority pages are business- and intent-led; edge-level evidence separates contextual, template, and unknown links; orphan candidates are reconciled against inventories; concentration is interpreted by page role; proposed links help real users; anchors remain natural and accessible; any numeric threshold is local and optional; and implementation plus outcome claims remain approval- and evidence-bounded.
