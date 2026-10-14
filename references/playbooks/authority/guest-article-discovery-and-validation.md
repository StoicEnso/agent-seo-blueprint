---
title: Guest-article discovery and editorial validation
area: authority
source_lessons: []
source_type: external_observation_and_live_pilot
tools: [public-search, first-party-pages, offline-ledger-check]
---

# Guest-article discovery and editorial validation

## What it is

A bounded way to find relevant publications that accept outside expertise, inspect their current rules and real articles, and prepare a small human-reviewed pitch queue. The goal is useful editorial coverage for the right readers, not buying ranking credit.

A search result is a **discovery lead, not a verified opportunity**. An open contributor route is not acceptance, a free placement, an indexed page, a followed link, traffic or revenue. A publisher's backlink policy is not the actual `rel` on an eventual page. Domain-rating or traffic screenshots are source claims, not current independent measurements.

## When to use — and when not to

Use when a product has a truthful expert or evidence-led angle for a specific audience and the owner asks for guest articles, contributed columns or editorial opportunities. For existing resource gaps use `editorial-link-intent-and-assets.md`. For entity listings use `directory-submissions.md`; this is not a directory-submission workflow. For relevant interviews and existing mentions use `manual-outreach.md`.

Do not use to generate unrelated guest-post inventory, mass backlinks, link exchanges, SEO article packages, fake expert profiles, or a quota of dofollow placements. Existing approval and product-truth rules remain unchanged.

## Method

1. **Pin product and audience truth.** Read the correct current product domain. A same-name domain may be unrelated or for sale. Record who the buyer is, the useful owned page, actual capabilities, important limits and the human author/proof basis. Do not recycle unverified testimonials, marketing multipliers, compliance guarantees or unreleased features.
2. **Generate a small query set.** Start with the observed pattern `intitle:"write for us" "your niche"`. Extend to descriptive variants for `contributor guidelines`, `submit an article`, `editorial guidelines`, `pitch an article`, and named specialist publications. Useful adjacent terms can include the buyer's work, not only the product category. Record the actual provider, query, date and locale where available. A Brave or Bing result is not a captured Google result.
3. **Search modestly and serially.** `python3 scripts/guest_article_review.py queries --keyword "garden design" --keyword "freight forwarding"` generates queries only. It does not run searches. Use approved public search separately. Process a bounded batch before expanding. Respect 429/Retry-After, access restrictions and human-verification walls; do not fan workers against one search provider or bypass bot checks. If the exact operator returns weak results, vary the words or inspect the publication directly rather than repeat the same empty query.
4. **Inspect the destination itself.** Open publisher-owned contributor or editorial pages and a genuinely relevant published sample. Capture text/HTML evidence, exact URL, UTC date, excerpt and file checksum. Record the current intake route, editorial review, audience, topic limits, author/disclosure requirements, article constraints, fee/membership state and what the publisher says about links. An old `write for us` page with no usable route stays conditional. A general contact page alone does not prove an outside-contributor programme.
5. **Separate route proof from cost and acceptance.** A route can be current while its fee is unknown. **Unknown cost is not free.** `EXPLICITLY_FREE` requires a clear publisher statement, preserved in the evidence. Paid or membership routes stay conditional until their separate economic/eligibility requirements are reviewed. No payment, membership purchase or representation is authorised by this playbook.
6. **Check quality and reader benefit.** Prefer a coherent specialist audience, accountable authors/editors, specific editorial constraints and relevant real articles. State the reader problem and why the proposed contribution belongs there. Reject unrelated multi-niche link sellers, paid followed-link packages, required reciprocal links, closed intake and invented credentials. Do not rank by raw domain rating or promise SEO value. An ordinary contributor page may still be a poor destination.
7. **Keep an evidence ledger.** Copy `assets/guest-article-opportunity-ledger.json` into the existing project workspace. Preserve discovered, conditional and rejected rows rather than converting missing evidence to zero. One product/publisher pair has one row; a publisher may fit several products only for distinct, defensible audiences/angles. For `VERIFIED_EDITORIAL`, require current first-party guidelines, a first-party route, a relevant sample, evidence references, editorial review, author basis and claim limits. A fee-unknown verified row remains explicitly fee-unknown.
8. **Check the saved packet offline.** `python3 scripts/guest_article_review.py validate <ledger.json> --evidence-root <packet-dir>` checks required states, first-party URLs, saved file hashes and excerpts, duplicate destinations and freshness. Evidence paths must stay inside the specified packet; existing files are never overwritten. The default maximum evidence age is 30 days. A stale row needs a new live check, not an edited date. The tool does **not** fetch, interpret website truth, approve a target or send anything.
9. **Prepare a narrow DRAFT.** Name one article and a concrete reader benefit. Refer to the publisher's actual coverage. State the real author's basis and disclose the product connection. Offer an original example, method or rights-safe asset only if it exists. A useful neutral article can fit where promotional links do not. Never demand a followed link, prescribe an exact-match anchor, invent an expert identity or offer a quid pro quo.
10. **Review before any external action.** Never send without explicit per-batch approval for the actual destination, sender, content, disclosure, link and any spend. `DRAFT_REVIEW_READY` means only that the saved packet passed structural checks. It is not outreach authority. Recheck the rules and exact article/product facts before the approved send. Do not create accounts or submit forms merely because the route is public.
11. **Record real outcomes separately.** After authorised outreach, distinguish sent, replied, accepted, published and rejected. Publication needs a public URL and a real live check of the exact linked page, canonical, robots/indexability, rendered `href`/`rel` and disclosures. Keep publication, indexing, referrals, leads and conversions separate. Temporal sequence is not causation. A guest article is not a guaranteed ranking improvement.

## State and evidence contract

- `DISCOVERED`: a lead only. Missing route/sample/current rules are unresolved, not implicitly valid.
- `VERIFIED_EDITORIAL`: fresh saved first-party route, guidelines and sample inspected; useful angle and author basis recorded. **Neither accepted nor published.** Cost can still be `UNKNOWN`; say so.
- `CONDITIONAL`: fees, membership, author eligibility, editor-only approval, rights, a blocked page or incomplete evidence need resolution. State the one next question/action.
- `REJECTED`: off-topic, closed, false-author, link-selling or other hard failure; preserve the reason. A structural checker cannot independently detect an undisclosed network.

Cost is one of `UNKNOWN`, `EXPLICITLY_FREE`, `PAID`, `MEMBERSHIP_REQUIRED`. Public statements belong in the source packet; absence of a price is never evidence of zero cost. Link policy is one of `UNKNOWN`, `EDITORIAL_DISCRETION`, `BIO_ONLY`, `NO_PROMOTIONAL_LINKS`. Actual published link behaviour stays unobserved until a real page exists.

The discovery ledger always has `outreach_authorized:false`, `outreach_status:"DRAFT_NOT_SENT"` and `link_outcome:"NOT_PLACED"`. Do not repurpose it as a live outreach executor or use a valid result to bypass approval. Keep later send/publication receipts in a separate owner-approved outcome log.

## Example — illustrative, not real destinations or product claims

- A garden-concept tool finds a specialist gardening outlet. Pitch a worked explanation of what a generated visual can and cannot tell a homeowner before a contractor visit. Do not claim engineering, plant suitability or exact-cost guarantees.
- A customs-document tool finds a forwarding publication. Pitch a rights-safe example of missing-field/consistency checks and human review before declaration entry. Do not present automation as authorised customs filing or invent time savings.
- A carrier-information service finds a transport/procurement outlet. Pitch how to document a dated licence check and its limits. A licence record alone does not prove financial health, safety or compliance, and a forthcoming alert service is not an available feature.

## Pitfalls

- Mistaking search-result title, arrows, domain age or screenshot traffic for current destination validation.
- Treating “accepts guest posts” as “accepts us”, “costs nothing” or “promises a link”.
- Sending promotional software articles to specialist magazines whose audience needs practical, neutral advice.
- Copying an article across many publications, stuffing anchors or writing low-value pieces mainly for links.
- Fabricating authors, case studies, customers, regulated credentials or product results.
- Using a sample's visible link as proof of the rules for a different article.
- Hiding sponsorship or exchanging followed links. Paid or advertorial links require truthful disclosure and appropriate `rel="sponsored"` or `nofollow` qualification; never buy ranking credit.
- Skipping cost/membership checks because a search result came from a respected brand.
- Editing another agent's workspace, changing schedules or applying unrelated pending PRs to run this method.

## Source and validation lineage

The query pattern is observed in Hridoy Reh's post of 14 October 2026: https://x.com/hridoyreh/status/2110388370094633204, quoting https://x.com/hridoyreh/status/2110324990918922307. His SEO example is a discovery illustration, not evidence about these products. The destination-screening, cost-state and offline evidence requirements are our own bounded method. See `references/audit-log/2026-10-14-guest-article-discovery.md` for the live pilot and its limits.

## Related

`manual-outreach.md`, `editorial-link-intent-and-assets.md`, `linkbuilding-what-not-to-do.md`, `other-link-building.md`, `workflows/authority-and-links.md`, `workflows/content-production.md`, `workflows/monitoring.md`.
