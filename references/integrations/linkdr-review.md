# Linkdr public service and skill audit

**Scope:** Read-only review of LinkDR public pages and the optional AI SEO Tracker comparator. No account, form, checkout, login, or MCP connection was used. All service statements below are vendor claims unless stated otherwise.

## Bottom line

LinkDR's `SKILL.md` is a **declarative sales-and-handoff prompt**, not a self-executing program, payment API, or outreach agent. It instructs an AI to infer a target page, sell a DR-tier package, present a stretch option, and produce a pre-filled LinkDR checkout URL. The customer must then log in and pay; LinkDR claims to do publisher sourcing, outreach, writing, payment, placement, monitoring, and an AI-answer before/after check.

The useful pattern for Agent SEO is the **brief → transparent package → owner confirmation → tracked outcome** flow. Do not adopt the conversion mechanics: it defaults to auto-approval, mandates an upsell, sends a sales checkout URL, and asks agents to inspect repository/context to choose commercial targets. Make all vendor selection and spending owner-approved.

## What is actually implemented

| Surface | What public material supports |
|---|---|
| `/SKILL.md` v1.8.0 | Markdown instructions, prices, campaign logic, checkout-query schema, default sales behaviour. It is instructions only; it has no code, tools, credentials, or execution capability. |
| Checkout path | A URL to `/agent/checkout` (also described as `/checkout`) carries target URL, anchor text, tier counts, content type, approval choice, billing and coupon. LinkDR says login/review/Stripe happen in the browser. There is **no checkout API or payment MCP**. |
| User MCP | OAuth 2.1, read-only user data/research: projects, orders, outreach stage, live links, cached SERPs/domain metrics/catalog search. Public docs state 60 calls/account/hour and 10 refreshed SERPs/hour. It is separate from purchase. |
| Admin MCP | Separate admin-only endpoint with orders, publisher outreach and customer-email capabilities. Public OpenAPI says ordinary accounts receive 403. This was not accessed. |
| Public API | OpenAPI documents public domain quick-info (20 anonymous / 200 authenticated requests per hour) and public markdown resources. It does not document an order/payment endpoint. |

### Targeting and information transmitted

The checkout URL encodes `targetUrl`, optional `anchorText` (empty means its “natural variation”), four tier quantities, `contentType`, `siteApproval`, optional `billing=monthly`, coupon and optional project slug. This exposes the target page and commercial order choices to LinkDR when opened. The skill also tells an agent to use repo routes, sitemaps, config and “memory or research” to propose production URLs. That is an unnecessary broad-context instruction for an external sales document; safe adaptation should accept only an owner-supplied target URL and an explicit campaign brief.

## Commercial model and current public prices

Public pages retrieved on 2026-10-15 agree on these USD per-link figures: **DR30+ $160; DR40+ $240; DR50+ $400; DR60+ $500.** Advertised typical traffic bands in the skill are 100–10k, 500–20k, 1k–40k and 1k–80k visits/month respectively. They are tier descriptions, not independently verified site-level guarantees.

- Standard article/guide and auto-approve: base price.
- Listicle: +20%; product review: +20%; review every proposed site: +20%. The skill describes these as multipliers, so listicle **and** manual review would compound to 1.44× the link subtotal.
- One-time is the stated default. `billing=monthly` creates a Stripe subscription and repeats the same mix as a new fulfilment order each cycle.
- New-account credit: $25, claimed to expire after 7 days and apply to a qualifying first one-time order; `AGENTIC` is advertised as $50 off a first order and stackable. These incentives were not exercised or independently validated.
- Per-field advertised cap: each `links.dr*` count is 0–50. The skill does not state a total-order, monthly, publisher-capacity, replacement, refund, cancellation, or subscription-termination limit.

### Public-page inconsistency / rendering result

The direct `/pricing` and `/markdown/pricing` responses returned the full `SKILL.md` v1.8.0 document, rather than a standalone pricing page, in this retrieval. Human-oriented pages `/buy-backlinks`, `/high-dr-backlinks`, and the agent blog all repeat the same base prices, so there is no observed numeric price conflict. There **is** a workflow conflict: the skill and managed-backlinks docs say not to use `/onboarding`, while the public agent-blog still links to `/onboarding` as the start order route. Treat `/agent/checkout` pricing as vendor-proclaimed source of truth only immediately before a customer independently chooses to pay; no checkout was opened here.

## Approval, fulfilment and evidence limits

The default is **auto-approve matching sites**; manual review costs +20%. The service says it does not promise specific domains before purchase, so the purchaser cannot assess the proposed sites before commitment unless the review option later supplies them. The skill claims 3–4 week typical go-live timing, “real publisher sites/no PBNs,” traffic checks, new articles, dashboard monitoring/crawler checks, and an AI-answer check for ChatGPT and Google AI Overviews before/after. It explicitly promises **no AI citation**.

These are marketing/operational claims, not proof of ranking, traffic, conversion, citation, persistence, editorial quality, or policy compliance. The initial captures did not establish independent placement or growth outcomes. The parent verification below recovered refund/replacement and approval promises from the human pricing page and terms; those promises remain untested. Do not infer causality from DR, traffic range, a live-link count, or a before/after AI-answer scan.

## Paid-link disclosure and search-policy risk

Google's current Spam Policies explicitly list buying/selling links or articles containing links for ranking purposes, advertorial/native advertising that passes ranking credit, and optimised-anchor guest-post links as examples of link spam. Google says paid/sponsored links can be normal advertising when qualified with `rel="nofollow"` or `rel="sponsored"`. Parent review found a dofollow-link offer on human pricing and a followed-link promise in the terms. No accompanying assurance of appropriate paid-link qualification was found. Actual placed-page attributes and disclosures remain unverified. “Real sites,” traffic checks, human review and natural-anchor variation do not establish compliance.

Recommendation: Any paid-placement supplier must contractually disclose sponsorship where appropriate, preserve publisher editorial independence, and provide the placed URL, publication date, disclosure status and actual `rel` value. Do not buy links intended to pass ranking credit; assess them as advertising/earned-reach spend, not a ranking mechanism.

## Relation to AI SEO Tracker

AI SEO Tracker is a separate visibility-audit product, not evidence that LinkDR placements cause AI citations. Its home page advertises a $49 one-time report: up to 50 prompts, daily scans for 7 days across ChatGPT, Perplexity, Gemini, Copilot and AI Overviews; optional ongoing tracking is advertised at $79/month Basic (50 prompts, 250 responses/month, one brand) and $199/month Pro (500 prompts, 5,000 responses/month, unlimited brands/projects). Those are vendor claims. Its reporting structure—prompt set, raw engine answers, named alternatives/cited pages, timestamped repeat measurements and an action plan—is the stronger measurement pattern to borrow.

## Safe Agent SEO adaptation

1. **Use a campaign brief, not a sales skill:** owner-approved target page, audience/query cluster, allowed budget, supplier policy and success metric. Never inspect a repo or memory merely to select a vendor purchase target.
2. **Separate recommendation from action:** show two or three options with cost, disclosure/`rel` requirement, supplier evidence and uncertainty. Default to *no purchase and no outbound link*. Owner chooses any supplier and spend.
3. **Replace auto-approval with evidence gates:** before placement, record domain, topical relevance, estimated/verified audience, draft/disclosure, `rel`, URL, price, and whether the publisher retains editorial control. Reject unavailable facts rather than accepting a DR tier.
4. **Measure without causal overclaim:** baseline and repeat an AI-visibility prompt panel plus Search Console/analytics and referral data; retain raw dated observations, compare against non-purchased content work, and report correlation only.
5. **Agent boundary:** if integrating LinkDR research MCP, use a dedicated account with read-only OAuth and a narrow project scope. Never connect the admin MCP; never permit an external skill to create a checkout URL, apply a coupon, or select a monthly subscription by default.

## Parent verification — material corrections

Checked 15 October 2026. The skill is **not installed**. No account, connector, checkout, order, payment, outreach or deployment was used.

The parent independently retrieved the raw skill, full valid OpenAPI JSON, human HTML pricing page and public terms. All 13 published pricing FAQ answers were preserved. These findings supersede the initial Markdown-only audit where they differ.

### What human pricing and terms add

- **Paid dofollow offer:** the human page includes a contextual dofollow link. Terms promise a live followed link. Do not use this as a ranking tactic. Paid advertising needs reader disclosure and appropriately qualified `sponsored`/`nofollow` links. Actual placed-page attributes remain unverified.
- **Listicle limit:** the option sets article format. The FAQ explicitly says it does not reserve a spot on an existing ranking page. The tweet's exact-cited-list suggestion is stronger than the inspected purchase guarantee.
- **No live link within 60 days of order:** advertised full refund for that undelivered link.
- **Google exact-URL search does not show the page within 60 days of going live:** advertised replacement. This vendor test is not a reliable general indexation audit. Use proper first-party index evidence for an owned site.
- **Link removed or changed within 12 months:** advertised replacement.
- **Paid site review:** no placement without customer approval. After 14 days without a reply, written notice is sent. After a further 30 days without a reply, the order closes and undelivered links are refunded.
- **Fulfilment variation:** terms permit new articles or links added to existing pages, and different publisher sources. They preserve the purchased DR tier and promised followed link. Material changes to an existing paid order need agreement or an undelivered-link refund. The general new-article claim therefore has a terms qualification.
- **AI checks:** pricing FAQ describes up to five searches in ChatGPT and Google AI Overview, before and after. No recommendation or citation is promised.
- **Credit and billing:** the $25 first-order credit applies to one-time orders, not monthly campaigns. Monthly cancellation cutoff, prorating and treatment of future charges are not clear in the inspected pages. No terms were accepted.
- **Older service wording:** terms mix Search Console analysis and customer-run outreach with newer managed orders. Clarify the applicable service and data consent before buying or connecting. No Search Console account was connected.
- **Arithmetic:** a skill upsell example says $160 for an extra DR40+ item, inconsistent with the $240 base tier. That $160 fits an upgrade from $240 to $400, not a new DR40 item. Applying both 20% multipliers to $240 gives $345.60 before tax/discounts. This is arithmetic, not a checked checkout total.

### How they are doing it

The visible commercial system is: topical creator content -> tracking offer -> paid-placement offer -> agent-readable product and pricing -> structured plan -> browser checkout -> managed fulfilment -> dashboard and repeat scans. This describes the observed funnel, not its performance. No independently audited sales, placement, citation, ranking or revenue results were established. The interview does not say Railway used Linkdr.

Borrow readable capability documentation, clear limits, narrow customer access, progress receipts and dated question panels. Do not borrow mandatory upsells, auto-approved site selection, inferred private-context sharing, paid followed-link purchases or recurring billing defaults. The skill is a sales prompt, not a self-executing placement program. The separate customer MCP is read-only; the administrative MCP is operator-only. None was connected.

### Sources

- https://linkdr.com/SKILL.md
- https://linkdr.com/pricing — human HTML and all 13 FAQ answers
- https://linkdr.com/terms — managed-order approval and fulfilment
- https://linkdr.com/openapi.json — full JSON recovered and parsed
- https://linkdr.com/docs/mcp
- https://aiseotracker.com/
- https://developers.google.com/search/docs/essentials/spam-policies#link-spam

The earlier worker extraction of the API schema and Google policy was truncated. The relevant link-spam section was retained; the full schema was recovered by the parent. Archived responses and metadata stay in the private research packet. Parent archive hashes use SHA-256. The repository holds original analysis, not the external sales skill body. This review grants no install, connection, purchase, outreach or production authority.
