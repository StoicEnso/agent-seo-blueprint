---
title: Affiliate Programs and Competitor-Affiliate Mining
area: authority
source_lessons: ["04-06"]
tools: [ahrefs, dataforseo, browser]
---

# Affiliate Programs and Competitor-Affiliate Mining

## What it is

A legitimate affiliate program can align incentives for publishers to evaluate, recommend, and link to a paid product. A competitor's public referral backlinks can also reveal publishers already willing to cover the category. Neither is permission to buy editorial claims, conceal sponsorships, or spam a public list.

## Eligibility and economics gate

Use this only when the product is paid, conversion and retention are measurable, the product is strong enough to recommend honestly, and commission can be funded from real unit economics.

```text
max_affiliate_payout = gross_profit_after_fulfilment - support_cost - desired_contribution_margin
```

Model one-time versus recurring payout, churn, refund risk, cookie window, minimum payout, and VIP tiers. A higher rate is useful only when sustainable. Never blindly outbid a competitor or promise earnings/conversion data that current evidence does not support.

## Program design

1. Prefer reliable first-party tracking or a reputable platform whose links and redirects are understood.
2. Publish current terms, attribution window, payout timing, disclosure requirements, prohibited traffic, and quality rules.
3. Provide accurate product facts, demo access, assets, and a dependable evaluation path.
4. Track referral traffic, trials/sales, retention, refunds, and payout-to-gross-profit—not links alone.
5. Review suspicious referral spikes, coupon abuse, fake reviews, and thin templated promotion.

A direct URL parameter such as `?via=partner` can be easy to read and track, but link equity depends on implementation and search-engine treatment. Never guarantee that a referral URL passes ranking authority.

## Competitor-affiliate backlink mining

A competitor's public referral links form a high-intent research pool, not a send list.

1. **Choose a real affiliate-active competitor.** Verify a current public program or sample referral link. Do not infer a program from one unusual parameter.
2. **Fingerprint public referral routes.** Record verified patterns such as `via`, `ref`, `refer`, `affiliate`, `aff`, `partner`, `/ref/`, partner subdomains, or platform redirects and retain the evidence URL.
3. **Pull backlink rows.** Use Ahrefs or DataForSEO. Filter competitor target URLs, redirects, anchor/copy, and referring pages for verified patterns.
4. **Deduplicate and qualify.** Keep one best page per referring domain. Retain relevant, public, indexable editorial reviews, comparisons, tutorials, roundups, and resources with a real audience. Reject coupon spam, scraped pages, PBNs, link farms, fake reviews, and irrelevant sites.
5. **Verify incumbent terms.** Capture the public commission, payout model, cookie window, recurring/one-time structure, and verification date. Never invent private conversion rates or earnings.
6. **Rank by expected value.** Use topical/audience fit, page traffic and ranking keywords, editorial quality, placement prominence, contactability, current competitor prominence, commercial intent, and link quality. DR or a provider rank is only one signal.
7. **Design a sustainable offer.** Base standard/VIP terms on margin, LTV, conversion evidence, and product advantage—not a reflexive promise to pay more.
8. **Draft one honest ask.** `test/add`, `comparison`, or `switch`. Reference the exact page and explain the defensible product advantage. Offer access or evidence so the publisher can evaluate independently.
9. **Measure.** Track approvals/sends, replies, accepted tests, placements, referral traffic, trials/sales, conversion, retention, payout ratio, and acquired links.

## Required prospect record

```json
{
  "competitor": "example.com",
  "competitor_referral_pattern": "via",
  "evidence_url": "https://example.com/affiliate",
  "competitor_program_terms": "...",
  "competitor_program_terms_verified_at": "YYYY-MM-DD",
  "referring_domain": "publisher.com",
  "referring_page": "https://publisher.com/best-tools",
  "competitor_target_url": "https://example.com/?via=partner",
  "page_type": "comparison|review|tutorial|roundup|other",
  "current_placement": "...",
  "topical_fit": "high|medium|low",
  "estimated_traffic": null,
  "authority_metric": null,
  "ask_type": "test/add|comparison|switch",
  "suggested_offer": "...",
  "offer_basis": "margin/LTV and verified public terms",
  "vip_candidate": false,
  "quality_flags": [],
  "status": "DRAFT"
}
```

## Outreach and external-action gate

Draft only. Never auto-send or contact at unsafe volume. Any batch needs explicit user review/confirmation, truthful claims, proper affiliate disclosure, and per-prospect personalization. Do not disparage competitors or demand replacement as a condition of payment.

## Link-quality and disavow guardrail

Low authority alone is not evidence of harm. Review spammy/manipulative links, request removal where practical, and prepare a disavow file only for a credible manual-action or severe link-scheme risk. The user reviews and submits it; this workflow never uploads it automatically.

## Done condition

A qualified, deduplicated prospect list and personalized DRAFT asks exist; every program claim has dated public evidence; proposed economics are sustainable; spam/disclosure rules are explicit; and no outreach or program change occurred without confirmation.
