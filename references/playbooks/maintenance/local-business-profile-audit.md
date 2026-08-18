---
title: Local Business Profile Audit
area: maintenance
operational_addition: true
sources:
  - "https://x.com/bloggersarvesh/status/2088983373859725755"
  - "https://support.google.com/business/answer/7091?hl=en"
  - "https://support.google.com/business/answer/7249669?hl=en"
  - "https://support.google.com/business/answer/3474122?hl=en"
  - "https://support.google.com/business/answer/7342169?hl=en"
  - "https://support.google.com/business/answer/9455399?hl=en"
source_type: creator-authored local SEO playbook screened against current Google Business Profile guidance
verified_at: 2026-08-17
---

# Local Business Profile Audit

## Purpose

Use this playbook for a read-only Google Business Profile (GBP) and local SEO audit. It turns a creator-authored sequence—categories, reviews, replies, posts, and services—into an evidence ledger. It does not copy the creator's ranking or revenue promises. The source's `$100k/month` in `90 days` framing is unverified and must not appear as a forecast, benchmark, or expected outcome.

Google's current guidance supports the narrow facts that complete and accurate profile information helps Google understand the business; categories affect local ranking; local results mainly use relevance, distance, and prominence; and more reviews plus positive ratings can help local ranking. Google says helpful replies can help a business stand out. It does **not** publish a review-velocity formula, confirm keyword-rich replies as a ranking lever, promise that service-description keywords improve rank, or say that frequent posts raise rank.

## Hard rules

1. **Read-only by default.** Capture evidence and draft recommendations. Category, service-area, hours, attribute, service, post, photo, or reply changes require explicit approval before editing the profile.
2. **Truth before competitor parity.** Add a category, service, location, attribute, or service area only when the real business supports it. Never copy a competitor field merely because it correlates with a ranking.
3. **No ranking or revenue guarantees.** Keep `PRIMARY_SUPPORTED`, `DIRECTLY_OBSERVED`, and `HYPOTHESIS` claims separate.
4. **No review manipulation.** Do not incentivize reviews, gate negative reviewers, ask customers to include target keywords or neighborhoods, write fake reviews, or suppress genuine criticism.
5. **Helpful replies, not keyword stuffing.** Replies should be brief, relevant, personal, privacy-safe, and non-promotional. Treat any direct ranking effect from reply wording as unproven.
6. **No location spoofing.** Use the searcher's real or explicitly supplied location context. Do not use residential proxies, fake addresses, device spoofing, or other methods that misrepresent geography.
7. **Separate local visibility from business outcomes.** A map-pack position is not a lead, booking, sale, or revenue result.

## Evidence grades

- `PRIMARY_SUPPORTED` — current Google policy/help text supports the narrow recommendation.
- `DIRECTLY_OBSERVED` — captured on a dated profile, result page, website, or first-party report; no causal claim.
- `HYPOTHESIS` — plausible tactic that needs a bounded test.
- `REJECTED_OR_PROHIBITED` — false, policy-unsafe, manipulative, or dependent on misrepresented location/business facts.

## Procedure

### 1. Confirm eligibility and scope

Record the real business name, website, profile URL, verified/owner-access state, public address or service-area model, locations, hours, service areas, target services, and target customer locations. If ownership or eligibility is unclear, stay read-only and mark the issue `blocked`.

### 2. Capture the baseline

Copy `assets/local-business-profile-audit.csv` to `audits/<date>_local-business-profile-audit.csv`. Record:

- profile completeness and accuracy;
- primary and additional categories;
- address/service area, hours, phone, website, attributes, services, products where applicable, photos/videos, posts, and Q&A;
- total reviews, rating, dated recent-review observations, reply coverage, and reply quality;
- website/entity consistency, including name/address/phone and truthful `LocalBusiness` structured data where applicable;
- Business Profile performance data available to the owner; and
- 3–5 high-value local queries with the real location context and capture time.

Use modest query volume. Personalized or location-sensitive observations must state the context and date.

### 3. Audit categories

Google says categories affect local ranking. Check that the primary category is the most specific accurate description of the core business. Use only a few additional categories that describe real departments or offerings; do not add one category per product or service.

Competitor categories are discovery evidence. A gap becomes a recommendation only after the business's website, operations, licensing, and customer offer verify the category. Note that category edits may trigger re-verification.

### 4. Audit reviews and replies

Record review count, rating, and dated recent-review observations for the business and a small relevant competitor set. Use competitor cadence as context—not a formula, quota, or causal ranking factor.

Review acquisition must request honest feedback from genuine customers without incentives or gating. Do not script the reviewer's keywords, service names, or locations.

Audit replies for coverage, timeliness, relevance, privacy, and helpfulness. Draft varied responses only when requested. Keep them short, conversational, non-promotional, and specific to the actual feedback. Do not repeat service/location keywords merely for SEO.

### 5. Audit services and profile completeness

Cross-check services against the real website and offer. Add only truthful services. Google can show services to local customers and allows descriptions/prices where supported; it does not promise a ranking lift from keyword-heavy descriptions. Draft clear customer-facing descriptions and reject stuffing, unsupported claims, phone numbers, prices in custom service names, or copied competitor text.

Check hours, special hours, attributes, contact details, address/service area, photos/videos, and products where applicable. Completeness and accuracy are the objective.

### 6. Audit posts

Treat posts as customer communication: announcements, offers, events, and updates. Google says posts can appear on Search and Maps and that posts older than six months are archived unless a date range is set. Reject the obsolete claim that all posts expire after seven days.

Draft a practical calendar only when the business has real updates and can maintain it. Posting frequency is a hypothesis, not a ranking guarantee. No publishing occurs without approval.

### 7. Check website and entity consistency

Verify that the website supports the profile's business facts, service areas, services, contact details, policies, and conversion path. Use truthful local landing pages only where distinct demand and real service coverage exist. Reject doorway pages, fake offices, duplicated city pages, and fabricated `LocalBusiness` ratings or locations.

### 8. Prioritize the recommendation ledger

For every row record the source, evidence grade, observed state, business impact, proposed change, truth basis, approval state, and verification method. Prioritize:

1. eligibility, ownership, and material factual errors;
2. primary category and core business information;
3. hours, service areas, contact/website consistency, and services;
4. review acquisition/reply process and customer trust;
5. useful photos, products, and posts; and
6. bounded tests for remaining hypotheses.

### 9. Draft, approve, verify

Present the exact proposed profile changes as a batch. The user must approve before any edit, post, upload, or public reply. After an approved change, capture the receipt and public state. If Google requests re-verification, stop and return the gate to the owner.

### 10. Measure over a fixed window

Pre-register a 4–8 week test where feasible. Keep profile edits small enough to interpret. Track:

- profile views or impressions where available;
- calls, messages, direction requests, bookings, and website clicks;
- dated local query observations with the same location/device context; and
- leads, conversions, and revenue separately.

Do not claim causality from one before/after observation. Record confounders such as seasonality, promotions, review campaigns, website changes, competitors, and Google updates.

## Done condition

The audit CSV contains dated evidence for every applicable field; categories and services have a truth basis; reviews/replies/posts are policy-safe; supported claims and hypotheses are separate; no public change occurred without approval; and the measurement plan distinguishes visibility from leads, conversions, and revenue.
