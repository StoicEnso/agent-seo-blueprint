---
title: Internal-Linking Optimisations — Google Discovery and Programmable Review
area: content
operational_addition: true
sources:
  - https://x.com/VengeonsP/status/2110831074787963098
  - https://chromewebstore.google.com/detail/maillagebooster/okbkojlihlckehofpgkgbiidoghjaang
official_guidance:
  - https://developers.google.com/search/docs/crawling-indexing/links-crawlable
  - https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site
---

# Internal-linking optimisations

## What this solves

Find existing pages that already discuss a destination's topic but lack a useful contextual link to it. Keep this inside the existing topic architecture and internal-link ledger, rather than building a second content or backlink programme. An internal link joins two pages on the same site; it is not an acquired external backlink.

Use this for a homepage, product page, guide or calculator with a clear keyword/intent owner. Do not point every related phrase at the homepage. A specific calculator, comparison or guide is often the better destination.

## Source, coverage and limits

Paul Vengeons' 15 October 2026 post describes a manual Google method: search `site:domain "exact keyword"`, read the matching pages, turn a relevant existing phrase into a link to the target, and aim for five in-body links rather than footer links. The original image illustrates this with `site:paulvengeons.fr "consultant seo"`.

The complete main post and image were checked on 18 October. The post contains **no programmable code** and no separate X Article. A visible reply recommends **MaillageBooster**, a Chrome extension offered by EMPIRIK. Its public listing claims Google-result analysis; keyword, TF-IDF, Jaccard and multilingual stemming scores; existing-link/anchor/HTTP checks; URL filters; and Excel, HTML and print-to-PDF exports. It claims local processing, no data collection and free use. These are vendor claims, **not** a code audit, measured accuracy, permission review or independently verified privacy promise. No extension was installed. Installing one is a separate owner-approved action; do not grant browser-data permissions merely to use this method.

The scanner below is our original, offline implementation of the discovery step. It is not the poster's or extension vendor's code. It deliberately does not scrape Google, fetch URLs, score semantic relevance, modify HTML or publish changes.

**Five links is a pilot suggestion, not a Google requirement.** Google recommends crawlable links with descriptive, natural anchor text. It does not require five exact-match anchors. A Google `site:` result is incomplete discovery evidence, not a crawl inventory, indexed-page count, ordinary keyword rank or proof that a phrase occurs in the editorial body. Snippets can match shared footers or old content.

## Before either method: choose the owner page

1. Resolve the approved site/workspace, responsible owner, review scope and protected/revenue pages. A request for an audit alone does not authorise edits or PR creation. A request for a PR authorises that review artifact, not a merge or deployment.
2. Record the destination's canonical URL, successful live response, visible purpose, title/H1 and indexability. Respect robots rules and rate limits during approved collection. Do not treat a sitemap as indexation proof.
3. Read first-party query/page data where access is available. Use complete equal periods, the exact property, country/device/search-type scope and final-data setting. Keep query rows private where required. Separate branded, non-branded, `site:` checks and hidden queries. Missing query rows are unknown, not zero demand.
4. Compare alternative owner pages for the same job. A homepage can own broad product intent while a specialist generator, free-tools comparison and instructional guide keep their own intent. Two URLs with impressions for one term do not alone prove harmful cannibalisation.
5. Freeze one destination and a small set of natural phrases. Record why each source reader would want that destination next. Keyword matches and semantic scores order review; neither is approval.

## Method A — Google-assisted manual discovery

### 1. Build a few exact queries

For a fictitious product:

```text
site:example.com "AI landscape design"
site:example.com "AI landscape generator"
site:example.com/blog/ "AI landscape design"
```

`site:` has no space before the domain. Quote the phrase. A path-scoped query can narrow the sample but is still incomplete. Use ordinary research volume, not automated pagination. With the existing helper:

```bash
python3 scripts/serp_capture.py 'site:example.com "AI landscape design"' --country us --json
```

That command builds a capture plan. Open its URL in the approved browser and read the results yourself. Record the time, country/language parameters, actual location when visible, personalisation notice, query, result URLs and any access limits. Parameters do not guarantee a physical location or neutral results. Never bypass a CAPTCHA or automate a blocked search.

### 2. Read the actual donor pages

For each result:

- open the live page and check response, final URL, canonical and noindex/robots signals;
- locate the phrase in the article/main content, not navigation, footer, unrelated recommendations, hidden markup or a repeated conversion module;
- check the full surrounding sentence and destination intent;
- inspect current contextual links to the target; a logo/home link is not an editorial link;
- skip duplicate donors, redirects, noncanonical aliases, target self-links, already-useful links, protected pages and overlapping open PRs;
- do not replace a good specialist link or an existing conversion link with a homepage link just to meet a quota.

A hit with only footer matches is a rejection, not a link opportunity. Fewer than five useful donors is a valid result. Do not create thin support pages or add awkward text to make the count.

### 3. Draft the smallest useful change

Prefer linking an existing natural phrase. Use an ordinary crawlable `<a href="/canonical-path">descriptive phrase</a>` or the site's equivalent link component. Never nest an anchor. Keep words, claims, assets and existing calls to action unchanged for a link-only pilot. Do not blanket-link every occurrence, stuff exact anchors, add global footer links, or put analytics parameters on canonical internal URLs.

Write a row in `assets/internal-link-ledger.csv` with source, destination, exact anchor, reader reason, owner, state and check date. Keep proposed change details and capture evidence in `assets/internal-link-opportunity-review.csv`. One retained donor counts once, even if it has several links or aliases. Exact anchors are allowed when natural, but should not be imposed on every page.

## Method B — programmable saved-HTML discovery

### 1. Collect a bounded, approved sample

Use existing crawler exports, approved HTTP collection or saved rendered HTML. Begin with 3–10 real relevant pages, then expand only if the output proves useful. Honour the site's robots/terms/access rules and a low concurrency cap; on HTTP 429 honour `Retry-After` and stop or reduce collection. Do not fetch private/authenticated pages or install a package/extension for this pass. Record when and how the capture was made.

Save HTML beside a JSON manifest. Capture final URL, actual status, content type, relevant `X-Robots-Tag`, and an optional SHA-256 (a content fingerprint). Do not invent successful metadata for a failed fetch. All capture files must resolve **under the manifest directory**. Example shape (illustrative only; not live evidence):

```json
[
  {
    "url": "https://example.com/blog/yard-planning",
    "final_url": "https://example.com/blog/yard-planning",
    "status": 200,
    "content_type": "text/html",
    "html_path": "pages/yard-planning.html",
    "x_robots_tag": ""
  }
]
```

`keywords.json`:

```json
["AI landscape design", "AI landscape generator"]
```

`protected-urls.json` is a JSON array of fully qualified donor URLs which must not be proposed. The site's protected-path rules can be broader than this file; check them separately.

### 2. Run offline

```bash
python3 scripts/internal_link_opportunities.py \
  --manifest audits/captures/manifest.json \
  --target https://example.com/ \
  --keywords audits/captures/keywords.json \
  --exclude-urls audits/captures/protected-urls.json \
  --out audits/captures/opportunities.json
```

The script uses only Python's standard library. It makes **zero network requests** and **zero site edits**. It reads the captures, writes one report, and refuses to overwrite its input files.

The report includes every input's decision and a separate candidate list. It:

- requires a same-origin HTTP(S) source, HTTP 200 HTML, unchanged final URL and exactly one self-referencing canonical;
- rejects target self-links, duplicate source URLs, protected inputs, noindex/`none`, query URLs, external sources and conflicting/missing canonicals;
- rejects captures outside the manifest folder, files over 5 MB, mismatched supplied hashes, and `<base>` elements that need manual URL review;
- selects article paragraphs/list items first, then main, then labelled body fallback;
- excludes script/style/template, nav/header/footer/aside, forms/buttons/SVG and explicit hidden markup;
- finds case-insensitive, whitespace-normalised word-boundary phrases, including inline emphasis;
- never joins text across paragraphs or across an existing anchor;
- skips a donor when the chosen editorial scope already links to the target;
- emits at most one candidate per source with capture hash, matched phrase, excerpt and extraction scope;
- leaves `reader_reason` blank, `approval: not_granted` and `live_link_verified: false` for human/project-owner review.

**Limits:** this is an HTML parser, not a renderer or relevance model. CSS classes, JavaScript, malformed markup, custom recommendation components, breadcrumbs and repeated body modules can still produce false candidates. Body fallback always needs manual boilerplate review. Existing anchor/URL matching is conservative and does not prove that an existing link is useful or followed. A source can change after capture; its saved status is not a current live check. Absence of noindex is not proof of robots allowance or indexation. Do not use a missing candidate as proof no opportunity exists. It will not discover semantic variants that lack the supplied phrases. Verify all retained rows in the rendered live page and current source before editing.

### 3. Review and create the authorised PR

Add the reader reason, exact proposed anchor/paragraph, current source revision, guard decision and destination check to each retained row. Reject stale captures or changed source before applying the diff. Keep private analytics, credentials, customer data and full third-party archives out of public PRs.

Use the existing project owner and branch workflow. Scan open PRs first. Check the actual narrow diff, formatting, touched tests, link validity, no nested anchors and required build/type/guard gates. Do not rewrite homepage copy, pricing, claims or funnel behaviour as a side effect. The owner reviews the exact PR. **No automatic publication**, merge, deploy, indexing request or scheduled job follows from a candidate, score, passing test or completed draft.

## Measurement and completion

Before a later authorised release, retain source/target baselines and write the exact live date after verifying the released links. Count proposed, merged and live links separately. Use equal 28-day and 56-day before/after windows once sufficient settled data exists. Keep Google/Bing, branded/non-branded and source/target results separate. Compare named queries, impressions, clicks, organic landings and source→target journeys only where existing measurement supports them. Keep sign-ups and first-time payers separate from returning payments. No traffic or revenue gain is implied by a new link.

Record other releases, query mix, seasonality and result-page changes. Before/after movement alone is not causal proof. Do not schedule recurring work unless the owner separately asks for it and the manual pilot already works.

Done for an **audit**: every sampled page has a reason/evidence decision, intent ownership is resolved or explicitly flagged, and retained links have reader reasons. Done for a **PR request**: the scoped PR exists and is checked on GitHub, required tests are recorded, and protected/overlapping surfaces are untouched. This still does not mean the links are live. A live claim needs the separate approved release and production check.

## Related

- `topic-architecture-and-internal-link-ledger.md`: page ownership, journeys and the existing ledger.
- `on-page-optimization.md`: link, title and canonical checks.
- [Content opportunity audit](../maintenance/content-opportunity-audit-and-measurement.md): the owning measurement method.
- [Google link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable).
- [Google site operator limitations](https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site).
