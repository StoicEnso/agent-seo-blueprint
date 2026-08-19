---
title: Statistics-page link earning
area: authority
tags: [statistics, original-data, link-earning, digital-pr, evergreen-content]
outputs:
  - briefs/<date>_statistics-page-brief.csv
  - outreach/<date>_statistics-page-pitches.json
---

# Statistics-page link earning

## Use this when

A site needs a source-worthy research asset, the live search results show demand for a current-year `topic statistics <year>` page, and the business can publish auditable data or a reproducible calculation. The method can support a relevant commercial page through useful contextual links, but it is not a “rank without backlinks” guarantee.

Do not use it when the only plan is to copy other pages, fabricate a survey, swap a year into thin text, or add a site-wide footer link only to push PageRank.

## Source status

This playbook was prompted by Borja’s 18 August 2026 X post and 20-second video: `https://x.com/borjafat/status/2089742971679691089`.

The linked full article reports a one-day snapshot of **80 live US Google searches across ten niches** and **423 page-one sites**, scored by referring-domain counts. It reports that sites below 1,000 referring domains held 24.4% of page-one statistics results, 21.4% of trends results, 12.0% of news results, and 10.0% of report results; no small site reached the top three for report queries. The article does not publish the full 80-query dataset or site-level scoring table, and the snapshot shows who ranked that day—not how quickly they got there. Treat the figures as directional creator evidence, not a causal benchmark. The author also states that link earning was not measured: **“The link part is a bet, not a measurement.”** Validate the mechanism on the target SERP and measure the target site’s own results.

The reusable mechanism is stronger than the claim:

- current-year statistics queries can have explicit research and citation intent;
- a stable, well-sourced page can compound age, links, and refresh history;
- one original number can make a page more quotable than a copied list;
- clear methodology, definitions, and downloadable data reduce citation friction;
- relevant contextual links can connect the research asset to a commercial page without turning the page into a doorway.

## Success contract

Before drafting, record:

1. the exact target query and country/language;
2. the live result set and checked date;
3. evidence that the result set rewards statistics, data, research, or quotable facts;
4. the unique first-party statistic or reproducible calculation;
5. the stable yearless URL and current-year title;
6. the relevant commercial page and the reader reason for each direction of the link;
7. the publication, outreach, and maintenance owner;
8. the measurement window and stop condition.

Use `assets/statistics-page-brief.csv`. Keep unknown values blank or `UNVERIFIED`; never infer them from a creator claim.

## Procedure

### 1. Qualify the live SERP

Search the exact current-year query and close variants at modest volume. Capture the top results, result types, freshness, visible methodology, source quality, backlink patterns when available, and whether the intent is informational, editorial research, news, commercial comparison, or mixed.

Proceed only when a useful statistics or research page fits the dominant intent and the site can add distinct value. A weak domain ranking in one observed result is a lead, not proof that authority is irrelevant.

Reject the idea when:

- the result set is dominated by official datasets that the site cannot improve or interpret;
- the query is too broad for the business to supply credible expertise;
- the planned page would duplicate an existing page or cannibalize a better target;
- the only differentiation is a new year in the title;
- the facts cannot be checked or licensed for reuse.

### 2. Choose a stable information architecture

Use a yearless canonical URL such as `/statistics/seo-statistics/` or, for one flagship resource, `/statistics/`. Put the current year in the title and on-page heading, not in a new annual URL. Add a `/statistics/` index only when the site has several genuinely distinct research assets.

Keep one canonical page through annual refreshes. Preserve prior figures in a dated history section when they remain useful. Do not create `/2026/`, `/2027/`, and `/2028/` clones that reset authority or leave stale near-duplicates.

### 3. Build an evidence ledger before prose

The page must contain at least one of these:

- a first-party operational number with a defined population and time window;
- a customer or industry survey with consent, sample size, question wording, field dates, and limitations;
- a reproducible calculation from cited public data, with formula and source versions;
- a small original audit with inclusion criteria, checked date, and raw observations.

For every claim, record source URL, publisher, publication date, retrieval date, exact supported statement, unit, geography, time period, sample size when relevant, and verification state.

Never invent data, merge unlike denominators, quote a number outside its period or geography, or label a copied total as original research. If no original number survives review, either narrow the page to an honest sourced guide or stop the statistics-page experiment.

### 4. Make the page easy to quote and verify

Use this structure when it fits the intent:

1. concise answer and “key statistics” box;
2. the original number with one plain-language quotable sentence;
3. methodology, definitions, sample, calculation, and limitations near the claim;
4. scannable tables with units and periods;
5. charts with descriptive titles, accessible alt text, and linked source data;
6. a downloadable CSV or source table when rights and privacy allow it;
7. grouped supporting statistics with direct citations;
8. historical figures and change notes;
9. author/reviewer identity and relevant expertise;
10. visible `Published` and `Last updated` dates.

Use natural language. Do not pad the page to hit a word count or bury the method under generic AI prose.

### 5. Use accurate metadata and schema

The title can include the current year. The canonical URL stays stable. Update `dateModified` only when the page actually changes. Preserve the original `datePublished`.

Use `Article` schema when the page is an article. Use `Dataset` only when the page exposes a real dataset and all required properties are true. Do not add unsupported review, fact-check, or AI-specific schema. Schema does not make weak evidence authoritative and does not guarantee rankings or citations.

### 6. Link for readers, not for a footprint

Add a contextual link from the statistics page to one relevant service, product, or money page only when the reader has a clear next step. Link the commercial page back to the research asset where the data supports a claim or helps evaluation. Record both links in the internal-link ledger with a reader reason and natural anchor text.

A footer link is optional, not a default. Use it only when the statistics hub is a true site-wide research resource that users may reasonably seek from every page. Do not add many exact-match footer links, force a footer link to every statistics article, or treat site-wide placement as a substitute for useful navigation and contextual links.

### 7. Draft ethical citation outreach

After the page passes publication review, identify writers, journalists, analysts, listicle owners, and pages that already cite comparable facts. Draft a short pitch that leads with the original number, methodology, why it is relevant to the recipient’s current work, and a direct data URL. Offer the data or chart for citation; do not demand a followed link, hide sponsorship, fake urgency, or automate a large blast.

Publishing and sending outreach are separate external actions. Hold the exact page and exact recipient batch for explicit approval.

### 8. Refresh and measure

Review quarterly for broken sources, material source revisions, query-intent change, and new internal evidence. Run the major annual refresh before the new-year query season. Change the title year, figures, methodology version, visible update date, and `dateModified` together. Keep a change log.

Measure separately:

- indexation and canonical state;
- rankings and organic sessions for the fixed query set;
- new referring domains and the exact citing pages;
- referral sessions from citations;
- contextual-link clicks to the commercial page;
- assisted conversions with a declared attribution window;
- maintenance cost and data freshness.

Sequence is not causation. A ranking, link, or conversion after publication does not prove that the year, schema, footer, or one internal link caused it.

## Stop conditions

Stop or revise when:

- no auditable original number remains;
- the page drifts into copied-stat aggregation without distinct value;
- a source changes or can no longer support the claim;
- privacy, licensing, consent, or confidentiality is unclear;
- the live SERP no longer rewards this page type;
- the page cannibalizes a stronger asset;
- the annual refresh would create a thin duplicate;
- outreach requires misleading attribution, hidden payment, or a guaranteed-link claim;
- maintenance cost exceeds measured search, referral, or commercial value.

## Done when

A brief exists with a qualified live SERP, stable yearless URL, checked evidence ledger, at least one auditable original or reproducible statistic, draft page structure, honest schema plan, two-way contextual-link reasons, approval states, maintenance date, and a measurement plan. No fabricated data, page publication, outreach send, or ranking/backlink promise occurred.
