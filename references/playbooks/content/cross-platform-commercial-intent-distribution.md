---
title: Cross-Platform Commercial-Intent Distribution
area: content
operational_addition: true
source_scope: Field hypothesis adapted from a vendor-authored affiliate-marketing video; validate every surface and metric independently
field_input: https://x.com/floriandarroman/status/2083886530737881548
---

# Cross-Platform Commercial-Intent Distribution

Use this when a validated commercial query may support more than an owned web page—for example a YouTube demonstration, a native social explanation, or an editorial contribution on a third-party surface that already appears in the live search journey. The goal is to earn useful visibility on the surfaces buyers actually use, not to mass-copy one asset, manufacture reviews, or exploit another domain’s authority.

This is an optional distribution branch after intent validation. It does not replace the canonical owned page, the live-SERP format decision, or the authority workflow.

## 1. Start with one validated buyer query

Record:

- exact query and locale;
- buyer stage and job-to-be-done;
- product/offer and claim boundary;
- current owned page, if any;
- measurable conversion action;
- whether monetization is first-party, affiliate, sponsorship, or none.

Do not start with a platform quota such as “publish everywhere.” If the query has no evidence of demand or commercial relevance, return it to research.

## 2. Map the actual search surfaces

Capture the live Google/Bing SERP and, only where relevant, the native search results on YouTube, Reddit, LinkedIn, X, TikTok, Medium, Quora, or another surface. Record dated evidence rather than assuming a platform ranks because it did in someone else’s example.

For each surface save:

- whether it appears in the ordinary SERP, video carousel, discussions/forums result, or answer-engine citations;
- native result format and apparent search intent;
- top useful results and their evidence/experience level;
- whether the brand can contribute legitimately under the platform’s rules;
- a distinct user value the new asset would add;
- the source URL or screenshot locator and capture date.

Keep answer-engine observations in the provider-specific citation ledger. A YouTube URL appearing in one answer or one SERP is not proof of stable ranking, traffic, or conversion.

## 3. Choose one primary and at most two supporting surfaces

Score each candidate from 0–2 on:

1. observed visibility for the exact query;
2. audience/intent fit;
3. ability to make a genuinely better native asset;
4. durable ownership or attribution;
5. measurable referral/conversion path;
6. production cost and repeatability.

Select the strongest surface, then at most two supporting surfaces. An owned page usually remains the evidence hub. A supporting video, post, or contribution must answer a platform-native need rather than repeat the page verbatim.

## 4. Build a proof-led native asset

### YouTube / searchable video

Use for demonstrations, comparisons, walkthroughs, tests, and questions where visual proof matters.

Require:

- an exact buyer-question title, not vague clickbait;
- the direct answer and fit boundary early;
- an on-screen product demonstration or first-hand evidence where possible;
- disclosed comparison criteria and material limitations;
- chapters and a reviewed transcript/captions;
- source links for material factual claims;
- a clear next step to the owned evidence or product page;
- disclosure of affiliate/sponsor relationships when applicable.

A video can complement the owned page and may become discoverable in YouTube, ordinary search, or answer engines. None of those outcomes is guaranteed.

### Native social post or short video

Adapt the same buyer problem into a genuinely native proof unit: one insight, demonstration, before/after, framework, or answer. Do not clone another creator’s script or duplicate the same file across every platform without adaptation. Social reach is a distribution hypothesis, not SEO proof.

### Independent editorial/community surface

Contribute only when the participation is authentic, useful, and permitted. Answer the user’s question first; link only when the destination materially helps. Disclose commercial relationships. Route legitimate editorial pitches to `workflows/authority-and-links.md`.

Do not create disposable accounts, evade moderation, seed fake reviews, impersonate customers, or post affiliate links into communities as if they were neutral recommendations.

## 5. Connect the journey without laundering claims

Create one map:

`query → surface/result → native asset → disclosed CTA/link → owned page or offer → measured outcome`

For each hop record the evidence source and metric contract. Keep these separate:

- search impressions, clicks, and positions;
- native-platform views, watch time, engagement, and profile/link clicks;
- answer-engine mentions/citations;
- referral sessions;
- leads, trials, transactions, and revenue;
- affiliate commission or sponsorship revenue.

Use real tracking parameters or platform attribution where available. `not_available` and `blocked` are valid values. Never estimate impressions, CTR, conversions, commission, or revenue from views or anecdotes.

## 6. Run a bounded test

For one query cluster:

1. capture the dated surface map;
2. produce the canonical owned brief or record the existing page;
3. brief one primary native asset and no more than two supporting adaptations;
4. define a 30/60/90-day measurement window appropriate to discovery and indexing;
5. record publishing as separately approval-gated;
6. compare actual visibility, engagement, referrals, and conversions by surface;
7. keep, revise, or stop the surface based on evidence.

Do not call the model “passive.” Content requires production, maintenance, disclosure, moderation, and attribution work.

## Output contract

Suggested artifact: `research/<date>_<query-slug>-distribution-map.json`.

```json
{
  "captured_at": "YYYY-MM-DD",
  "query": "...",
  "locale": "en-GB",
  "buyer_stage": "commercial_investigation",
  "owned_hub": {"url": "...", "status": "existing|briefed|not_available"},
  "surfaces": [
    {
      "name": "youtube",
      "observed_for_query": true,
      "evidence": "...",
      "native_intent": "comparison",
      "distinct_value": "first-hand product walkthrough",
      "score": 10,
      "role": "primary"
    }
  ],
  "journey": {
    "cta": "...",
    "destination": "...",
    "tracking": "..."
  },
  "metrics": {
    "search": "not_available",
    "native": "not_available",
    "referrals": "not_available",
    "conversions": "not_available",
    "revenue": "not_available"
  },
  "disclosures_required": [],
  "publication_status": "DRAFT",
  "limitations": ["surface observations are dated", "no ranking or revenue guarantee"]
}
```

## Source-quality and compliance note

A 2026 creator video claimed $328,000 from an affiliate website and recommended shifting commercial-intent distribution from blogging toward social/video/community platforms. The revenue, exit, passive-income, sponsorship, and third-party earnings claims were self-presented and were not independently verified for this playbook. The useful hypothesis is narrower: search demand can be served by multiple surfaces, and a searchable native asset can create an additional discovery path when live evidence supports it.

For UK-facing work, commercial intent and affiliate relationships must be made clear; ASA/CAP guidance is the current primary reference. Platform and search-engine rules must be checked at execution time.

## Rejected tactics

- copying another creator’s scripts, videos, or account wholesale;
- “parasite SEO” pages whose main purpose is to exploit host authority without independent reader value;
- fake first-person recommendations or undisclosed affiliate links;
- warmed disposable accounts, ban evasion, comment spam, or mass posting;
- automated comment-to-DM capture without consent and platform compliance;
- publishing the same shallow asset everywhere;
- treating social views, answer-engine mentions, or rankings as revenue;
- quoting the source’s revenue/ROI claims as expected performance.

## Done when

The query and locale are fixed; live surface evidence is dated; one primary and at most two supporting surfaces are selected; every asset has distinct native value, a claim boundary, and a disclosure plan; the owned evidence hub remains clear; the journey and metrics stay separated; publication remains approval-gated; and no copied, deceptive, spammy, or ban-evasion tactic survives the plan.
