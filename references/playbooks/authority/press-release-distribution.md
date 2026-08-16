---
title: Evidence-Led Press Release Distribution
area: authority
operational_addition: true
source: "https://x.com/jespernissenseo/status/2088631252937048489"
official_guardrails:
  - "https://developers.google.com/search/docs/essentials/spam-policies#link-spam"
  - "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
---

# Evidence-Led Press Release Distribution

## Purpose

Use a press-release platform to publish **real, newsworthy company information** in a public format that journalists, partners, customers, and searchers can verify. Treat distribution as a PR/referral/citation experiment. Do not treat it as a parasite-SEO page factory or a guaranteed backlink tactic.

Google explicitly lists optimized-anchor links in press releases distributed on other sites as a link-spam example when they pass ranking credit, and it treats low-value content made mainly to manipulate ranking or linking signals as spam. Paid or advertorial links should be appropriately qualified, such as `rel="sponsored"` or `nofollow`.

## Source-claim assessment: openPR

The creator post claimed one free release, up to five followed links, and indexing “in minutes.” Live checks on 2026-08-16 found a real free route, but the link and indexing claims are more conditional:

- openPR's current submission page states **one free press release per 30 days**;
- that page also states **no more than five in-text backlinks**, so the five-link limit is supported as a submission rule;
- another destination-owned page observed in the same review stated a three-link limit, so openPR's own pages were inconsistent and the effective limit must be checked in the live form before use;
- it says releases do **not** go live immediately and are published on working days;
- paid credits are available for extra releases, and the service page listed paid correction/deletion;
- the service page prohibits duplicate/spam releases and content or images without rights;
- browser inspection of 15 fresh public releases found public `index,follow,noarchive` pages but no publisher-destination hyperlink in those samples; raw URLs were sometimes visible as text; and
- openPR's own SEO and Google News statements are platform marketing claims. They do not guarantee indexation, Google News inclusion, referral traffic, rankings, or link value.

The sample proves only the state of those pages at that time. It does not prove that an allowed backlink becomes clickable, followed, permanent, indexed, or valuable. Link rendering, attributes, robots directives, costs, terms, moderation, and templates are mutable and must be rechecked for each planned release.

## Hard rules

1. **Require real news.** Suitable triggers include a material product launch, original study, major verified milestone, event, partnership, award, funding update, or public-interest change. An evergreen sales page rewritten as “news” fails.
2. **Use an owned evidence hub.** Link to the canonical product, study, newsroom, or announcement page that contains full facts and remains under the project's control.
3. **No ranking or indexing promises.** Never promise a followed link, fast indexing, Google News inclusion, authority gain, traffic, citations, or sales.
4. **No optimized-anchor link stuffing.** Use the minimum links readers need, with branded, URL, or natural descriptive anchors.
5. **Paid distribution is not an SEO-link purchase.** Record the commercial relationship and verify link qualification. If a paid placement passes ranking credit and the operator cannot correct or qualify it, do not use it as a link-building tactic.
6. **No duplicates or mass syndication.** Do not spray the same release across platforms or automate cross-posting merely to create links. Adapt only when each destination and audience has a real use.
7. **Truth and rights are mandatory.** Verify every material claim, date, name, quote, logo, image, trademark, and contact detail. No fake quotes, awards, partnerships, journalists, or customers.
8. **External writes need approval.** Account creation, payment, submission, publication, corrections, and deletion are approval-gated actions.
9. **Stage carefully.** Some platforms charge for correction/deletion. Complete fact, legal, rights, link, and contact checks before submission.

## Candidate verification

Register candidates in `assets/press-release-distribution-registry.csv`. Before recommendation, verify from destination-owned pages:

- legal entity and contact information;
- current submit URL and account requirements;
- free allowance, price, correction/deletion terms, and refund state;
- accepted topics, prohibited content, rights requirements, and moderation;
- publication timing and whether approval is guaranteed;
- one comparable public release;
- public HTTP state, canonical, robots/indexability, and page permanence;
- actual outbound-link form and `rel` on a comparable live page;
- disclosure, author/source attribution, and contact presentation; and
- last verified date.

Keep creator/aggregator claims in `source_claims_unverified`. Store direct observations separately. A conflict is resolved in favor of current destination-owned evidence.

## Release procedure

### 1. Write the news contract

Record:

- event and exact date;
- why it matters now;
- affected audience;
- accountable company/contact;
- approved claims and direct evidence;
- approved quote and named speaker;
- canonical owned evidence URL;
- required disclosures; and
- facts that must not be claimed.

Stop if the event cannot support a plain, factual headline.

### 2. Draft for people, not link count

Use:

- descriptive factual headline;
- direct summary in the opening paragraph;
- evidence, context, and limitations;
- one accountable company/source section;
- working media with recorded rights; and
- only the links needed to verify facts or take the next relevant action.

Do not manufacture length, repeat keywords, hide commercial intent, or convert the release into a generic “ultimate guide.”

### 3. Run pre-submission QA

Check:

- every name, date, quote, number, product claim, and URL;
- duplicate/republication risk;
- image and trademark rights;
- destination terms and current costs;
- link count, anchors, destinations, and requested `rel` treatment;
- disclosure and contact details;
- canonical owned announcement state; and
- exact correction/deletion path if an error is found.

Save the draft with `status: "DRAFT"`. Ask for explicit approval of the exact destination, copy, links, assets, and any price.

### 4. Verify after an approved publication

Capture:

- submitted, approved, and first-live timestamps;
- public URL and final HTTP status;
- visible title/body/source/contact state;
- canonical and robots state;
- each outbound URL, anchor, redirect, and `rel` value;
- disclosure and platform attribution;
- correction needs and cost; and
- evidence screenshot or page capture.

Do not report “indexed” from publication alone. A `site:` result is directional evidence, not an authoritative index count. The project does not control the third-party property's Search Console.

### 5. Measure separate outcomes

Track independently:

- submission accepted/rejected;
- public release live;
- observable index presence with check date and method;
- qualified referral sessions and engagement;
- journalist/editorial pickups;
- new mentions or citations;
- acquired links and their actual `rel`;
- assisted conversions, leads, and revenue; and
- production, placement, correction, and maintenance cost.

Publication, index presence, a followed link, ranking change, media pickup, and conversion are different outcomes. Sequence is not causation.

## openPR decision as of 2026-08-16

`VERIFIED_CANDIDATE`, not approved for submission. It has a destination-owned free route and a current submission page that allows no more than five in-text backlinks. The claim that those links are reliably followed, plus the minute-level indexing claim, remains unproven. Recheck the live form, current first-party terms, a fresh public sample, actual link rendering and `rel`, correction cost, and topic eligibility before each use. Use only for genuine news with an owned evidence page and approved copy.

## Done condition

A candidate has current first-party route and terms evidence; the release is tied to real news and an owned evidence hub; claims, rights, links, disclosures, and correction risk pass QA; nothing is submitted without explicit approval; and outcomes are measured separately without ranking, indexing, or citation promises.
