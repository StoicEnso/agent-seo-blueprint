---
title: Topic Architecture and Internal-Link Ledger
area: content
operational_addition: true
sources:
  - "https://x.com/borjafat/status/2088321150887620739"
  - "https://x.com/borjafat/status/2088271101604295096"
official_guidance:
  - "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"
  - "https://developers.google.com/search/docs/appearance/sitelinks"
  - "https://developers.google.com/search/docs/appearance/structured-data/article"
  - "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
---

# Topic Architecture and Internal-Link Ledger

## Purpose

Turn a validated topic into a small, useful page system with one clear conversion destination and inspectable contextual links. Use it after keyword/intent research and before drafting a cluster.

The source author reports a field study of 510 websites across 41 commercial searches, 40.4 million ranked keywords, and a 25,538-page crawl. It reports an association between deeper topic coverage and better positions, plus weak article-to-product linking on sampled sites. These are **self-reported observational findings**, not independently replicated causal proof. Do not turn them into a universal “topical authority score,” a guaranteed ranking lift, or a claim that backlinks no longer matter.

## Hard rules

1. **Start with a real user journey and money page.** A cluster without a useful destination is content inventory, not architecture.
2. **One page per distinct answer or format.** Merge query variants when a reader expects the same answer. Split only when intent, evidence, or page format differs.
3. **Every page must add distinct value.** No thin support pages, synthetic FAQ fan-out, or pages created only to increase a topic count.
4. **Contextual links need a reader reason.** Navigation and footer links help discovery but do not replace links placed where the next page is useful.
5. **Use descriptive, natural anchor text.** Do not mechanically repeat exact-match anchors.
6. **Authorship and research must be real.** Create an author page only when it helps readers verify a real creator. Create a statistics page only from original, transparent, reproducible work.
7. **No authority dilution fiction.** A second topic is not automatically harmful or free. Validate demand, fit, quality capacity, and maintenance cost for each topic.
8. **Measure the project, not the source anecdote.** Track crawlability, journeys, page/query outcomes, qualified traffic, and conversion evidence.

## Procedure

### 1. Define the topic contract

Record:

- topic and intended audience;
- business reason for coverage;
- primary user job or buyer question;
- target money/service page and approved offer;
- topic owner and reviewer;
- evidence available now; and
- exclusions or claims the project cannot support.

If the money page does not solve the problem discussed in the topic, choose another topic or destination.

### 2. Create the page map

Use `assets/topic-architecture-map.csv`. Add one row per planned or existing URL with:

`topic,page_role,query_or_question,intent,working_title,target_url,parent_pillar,money_page_url,distinct_value,evidence_required,author_or_reviewer,status,publish_date,last_reviewed_at,notes`

Allowed page roles:

- `money_page`
- `pillar`
- `supporting`
- `comparison`
- `use_case`
- `study_or_statistics`
- `author`
- `trust_or_policy`

The role does not create permission to publish. Every row still passes live SERP, intent, evidence, duplication, and product-truth checks.

### 3. Resolve overlap before writing

For every proposed URL:

1. Compare the expected answer, audience, intent, format, and conversion path with existing rows.
2. Merge terms when the same page can satisfy them completely.
3. Split only when a separate page gives a materially different answer or format.
4. Reject a row when it exists only to manufacture depth.
5. Record the winning canonical URL before drafting.

### 4. Draw the reader paths

Plan links only when they answer the reader's next question:

- pillar -> supporting page for useful depth;
- supporting page -> pillar for broader context;
- pillar/supporting page -> money page when the offer solves the discussed problem;
- supporting page -> another supporting page when it is the logical next step;
- page using a finding -> study/statistics page for method and source context;
- article byline -> real author page where readers would expect accountability.

Google's link guidance says every important page should have at least one link from another page and recommends descriptive, contextual anchors. That guidance does not prescribe a fixed link count or a ranking formula.

### 5. Write the link ledger

Use `assets/internal-link-ledger.csv`. Every planned link gets one row:

`topic,source_url,destination_url,anchor_text,reader_reason,source_page_role,destination_page_role,status,last_checked_at,http_result,final_url,notes`

Required checks:

- source and destination are canonical URLs;
- the anchor describes the destination naturally;
- surrounding text explains why the link is useful;
- the destination is live or the link is held until publication;
- the final URL does not rely on an unintended redirect; and
- status is `planned | live | broken | redirected | removed`.

Do not count menu/footer links as contextual ledger rows unless the audit explicitly needs a separate navigation inventory.

### 6. Add trust and evidence surfaces conditionally

**Author page:** include real first-hand work, relevant credentials where required, studies/datasets, topic-grouped articles, and consistent external profiles. Match visible bylines to accurate `Article` author markup when that schema is used. Google recommends author names and identifying author URLs to help it understand articles; this is not a ranking guarantee. A bio is not a ranking button.

**Study/statistics page:** pre-register what will be counted, inclusion/exclusion rules, dates, method, full or appropriately shareable data, limitations, corrections, and update history. Track citations/links and qualified usage separately from rankings.

### 7. Validate before publishing

Check:

- every page serves the intended audience if visited directly;
- each row has distinct evidence and value;
- no unsupported comparison, statistic, testimonial, credential, or product claim appears;
- money-page links are relevant and proportionate;
- schema matches visible content;
- canonicals and indexability are intentional; and
- the owner can maintain the cluster.

### 8. Audit and measure

After publishing, monitor:

- important pages with no contextual inbound link;
- ledger rows that are broken, redirected, or stale;
- crawl/indexation evidence by URL;
- query/page overlap in Search Console;
- page-to-page and page-to-money-page journeys;
- qualified organic traffic and conversions;
- external citations/referring domains for research assets; and
- content maintenance cost.

A ranking change after cluster publication is not proof that the map caused it. Preserve the timeline and competing changes.

## Done condition

Every retained page has a distinct user job, evidence plan, canonical URL, owner, and useful place in the journey; every planned contextual link has a ledger row and reader reason; thin depth-manufacturing pages are absent; and the map is measured with project evidence rather than a fabricated topical-authority score.
