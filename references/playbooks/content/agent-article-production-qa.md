---
title: Evidence-Grounded Agent Article Production and QA
area: content
---

# Evidence-Grounded Agent Article Production and QA

## When to use

Use after `workflows/content-production.md` has produced a validated article brief and the user has asked for an actual draft. Do not use this to bypass the article go/no-go gate, live-SERP format check, or publication approval boundary.

## Inputs

- approved keyword/sitemap row or explicit user-selected topic;
- content brief and live-SERP summary;
- project/product truth contract if product claims or CTAs appear;
- internal-link candidates;
- target locale and audience.

## 1. Resolve the topic and truth contract

The run must point to an approved backlog item or explicit user request. Record:

- primary keyword and search intent;
- target URL and format;
- approved product facts with evidence;
- required product links and approved CTA language;
- forbidden or unverified claims and comparison boundaries;
- reviewer questions.

Never invent product capabilities, prices, guarantees, testimonials, comparisons, or customer outcomes.

## 2. Build a source-to-claim packet

Research by claim, not by quota. For every material claim or outline section, capture:

- source URL and title;
- source type and publication/update date when relevant;
- extracted fact, quote, or data point;
- intended section/claim;
- reliability note and freshness requirement;
- contradiction or uncertainty, if any.

Use primary/official sources for product, legal, medical, financial, pricing, or current technical claims whenever available. Search-result snippets alone are not evidence. Never fabricate quotations.

## 3. Draft from the brief and evidence

- Answer the core question early.
- Preserve the intent-matched structure and standalone H2 sections.
- Cite or link material claims where appropriate.
- Add original examples, screenshots, data, templates, calculations, or product-specific workflows where available.
- Include internal links and CTA only where useful and truthful.
- Do not force a universal word count; cover the job completely and stop.

## 4. Anti-slop rewrite

Run a distinct rewrite pass that removes:

- generic introductions and throat-clearing;
- repeated conclusions or section recaps;
- canned transitions and symmetrical filler;
- unsupported certainty and fake authority;
- fragmented prose and monotonous sentence rhythm;
- empty adjectives, hype, and marketing clichés;
- duplicated facts or examples;
- headings that promise more than the section delivers.

Keep facts, citations, structure, links, code, and product truth intact.

## 5. Mechanical lint

Check:

- one H1 and logical H2/H3 hierarchy;
- primary keyword in title, H1, URL, and first 100 words where natural;
- title at most 60 characters and meta description at most 155 unless the project overrides;
- valid internal/external links and descriptive anchors;
- image filenames/alt text where images exist;
- required product links and approved CTA language;
- forbidden claims/phrases absent;
- citations or source links for material claims;
- no fake quotes, TODOs, placeholder text, or accidental instruction leakage;
- schema plan consistent with the visible page.

## 6. Weighted QA

Score 0–100:

- Search intent and coverage — 25
- Evidence, accuracy, and E-E-A-T — 25
- Human value beyond an AI summary — 15
- Writing quality and coherence — 15
- Product truth and CTA integrity — 10
- On-page optimization and internal linking — 10

### Hard fails

Any of the following fails the draft regardless of score:

- unsupported material factual claim;
- fabricated quote/source/testimonial;
- false or unapproved product claim;
- search-intent or page-format mismatch;
- obvious cannibalization/duplicate-page risk;
- broken required link or missing required evidence;
- legal/safety-critical advice without appropriate sourcing and review.

## 7. Bounded revision

- Pass at 85+ with no hard fails.
- Below 85 or any hard fail: revise against named defects.
- Maximum two automated revision passes.
- After two failed passes, stop and emit a defect report; do not loop or publish.

## Outputs

1. Source-to-claim packet (`research/<date>_<slug>-source-packet.json`)
2. Review draft (`drafts/<date>_<slug>.md`)
3. QA report (`audits/<date>_<slug>-content-qa.json`) containing category scores, hard-fail results, revision count, and exact remaining defects.

## Publication boundary

This playbook never publishes. Publishing, CMS writes, notifications, or external sends require explicit user confirmation and the owning workflow's approval path.
