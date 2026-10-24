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


## Optional AI-search page-structure review

Use for a guide, definition, how-to, comparison or product page when the user asks about AI-search page anatomy. This is an evidence review inside the existing QA process, not another publishing workflow or a universal page template. Copy `assets/ai-search-page-review.json` into the project's `audits/` directory. Leave unrun checks `not_checked`; a populated template is not a passed audit.

### Source assessment and limits

Discovery: [Ira Bodnar, 24 October 2026](https://x.com/irabukht/status/2114031412991218048), including its page-anatomy infographic. It promotes Ryze AI and Firegoat. The claimed research of **10K websites ranked #1 in LLMs** has no linked dataset, sampling method, prompt panel, provider/version, locale or reproducible rank definition in the source. Treat it as an unverified vendor claim, not an established study. The separate GEO-bench paper uses 10,000 **queries**, not proof of that claimed website study. Firegoat's claimed 25+ agents is vendor-attributed and was not tested; no signup or tool purchase is needed to perform this review.

The infographic's 19 numbered elements, structured-data note, seven conversion placements and six technical cards are an idea menu. They are not a required count, sequence, word limit, citation recipe or conversion benchmark. The post itself says 50 words while the image says 40–60; neither is a provider rule.

### Ten source claims, ten bounded checks

| ID | Claim assessment | What to inspect and retain |
|---|---|---|
| `markdown_parity` | An AI-only second page and `llms.txt` are not mandatory. | Read the human-facing page first. Optional Markdown must preserve the same material facts, prices, limits, sources, disclosures and update date; it must not hide different offers or model instructions. Check discoverability and freshness only if a real retrieval task needs it. Missing `llms.txt` is not a Google defect. Detailed delivery/cache implementation belongs in the existing agent-delivery work, not this page review. |
| `agent_signup` | Task usability is separate from ranking. | Load `ai-search-commerce-readiness.md` for the bounded signup review. Record labels, validation, accessibility, authentication steps and the exact safe stop. No actual account creation, email, OAuth grant, subscription or paid-tool test follows from this checklist. |
| `answer_first` | An early self-contained answer helps readers; exact extraction is not guaranteed. | Check that the opening answers the real question and states the entity, scope and material limits. Include a number only if useful and evidenced. Do not force a definition-plus-number formula, 50 words, or 40–60 words. |
| `original_data` | Being first does not guarantee citation or exclude later sources. | Keep the sample size, denominator, collection dates, method, metric definition, limitations and reproducible source. Redact personal data. Never turn the illustrative 43% into a real statistic. Never invent research to fit the layout. A sourced external statistic is valid when accurately attributed. |
| `html_comparison` | HTML tables are useful; image understanding is not universally impossible. | Inspect raw and rendered content, a real `table`, headers, caption/context and meaningful cell values. State units, dates, criteria, limitations and any commercial relationship. Offer a text equivalent for image-only comparisons. Do not assume every row will appear in answers or invent prices or rankings. |
| `author_schema` | Truthful authorship and consistent metadata help accountability; LinkedIn is not compulsory. | Match the visible author/reviewer, actual credentials, profile links and published/modified dates to supported structured data. Use only genuine identities. Do not fabricate expertise, force an author onto an unsuitable page type, or advance dates without a substantive change. |
| `buyer_faq` | Buyer questions need evidence; model-generated questions are hypotheses. | Separate sales/support, search data and saved exact provider prompts from generated suggestions. Answer only relevant questions at the length needed. An FAQ section is not a promise of a rich result or citation. As checked 24 October 2026, Google's FAQ documentation redirects to its removal notice; FAQ rich results are no longer shown. Do not auto-add FAQPage/HowTo markup as a search-growth trick. |
| `bing_discovery` | Bing is relevant, but is not a proven sole or sufficient ChatGPT gateway. | Keep Bing URL Inspection evidence separate from Google eligibility and direct OpenAI crawler/citation checks. A missing `site:` result is not proof of absence from an index or from all ChatGPT answers. IndexNow notifies participating engines of genuine added, changed or deleted owned URLs; do not ping unchanged pages or equate a receipt with indexing. An IndexNow HTTP 200 means received; HTTP 202 means key validation pending. Neither proves a crawl, index entry, citation or traffic. |
| `provider_access` | Search, training and user-triggered fetches are different controls. | Follow `workflows/geo-audit.md` and current official provider docs. Inspect scoped OAI-SearchBot, PerplexityBot and Claude-SearchBot access separately from GPTBot/ClaudeBot and user-triggered agents. Check relevant response/CDN evidence as well as robots rules. No blanket allow rule, authentication weakening or crawler-policy change is authorised by an audit. |
| `source_quotes` | Real sources and expert quotes strengthen evidence; the uplift is study-specific. | Link support at the claim, verify quotations and disclose interests. The GEO paper reports **up to 40%** under its own benchmark visibility metrics, engines, domains and interventions. This is not a current cross-provider forecast, a 40-point citation-rate rise, a traffic/revenue lift, or proof that this layout caused a change. |

### Adapt the image to the reader's actual job

Retain useful ideas, but record `not_applicable` with a reason when a component does not fit:

- **Orientation:** intent-matched title/H1, real byline when relevant, honest dates, direct opening, decision summary and key facts. A year belongs in a title only when the content needs it; do not manufacture freshness.
- **Definition and execution:** explain the entity, use one stable name, give useful steps, inputs and verifiable completion criteria, and show real mistakes/tradeoffs. Do not force 200–300 words, exactly three mistakes or H3 steps onto every page.
- **Proof and comparison:** show real original data where available, a semantic comparison table, selection method and declared criteria. Explain who benefits, who should choose another option and why. Do not invent weighted scores, a price of failure or numerical case-study results.
- **Trust and continuation:** support claims inline, use real examples and relevant FAQs, show substantive changes if a changelog helps, and link to genuinely useful related pages/tools. There is no 3–6-link quota and no need to build a calculator merely to fill a slot.
- **Schema and media:** select supported types for the actual visible page. A schema vocabulary term is not a Google rich-result entitlement. Use a video, transcript or diagram only when it adds proof or explanation; no compulsory VideoObject, HowTo, FAQPage or special AI schema.
- **Conversion placements:** the image proposes a sticky bar/side tab, lead magnet, early image CTA, video, option verdict, in-text link and final image CTA. Treat these seven placements as optional conversion hypotheses. Check offer truth, accessible controls, mobile obstruction, consent and a sensible next action; do not install all seven. The 10%/15%/30% positions and claims that readers are warmest or will never reach the bottom are not verified measurements of this page.
- **Technical cards:** inspect access/rendering/canonicals, provider-specific discovery, authentic corroboration, cross-surface fact consistency, real freshness and measurement. Do not require SSR if the scoped renderer can access the content, claim unmentioned brands cannot be recommended, treat a `site:` query as an index verdict, or turn a weekly 20–50-prompt suggestion into an automatic job.

### Evidence record and handoff

For each applicable check retain the canonical page URL, capture date, platform/surface, page type, exact evidence locator, state (`pass | fail | mixed | unknown | not_checked | not_applicable`), recommendation and owner. `pass`, `fail` and `mixed` require observed evidence; `not_applicable` requires a reason. An unrun or inaccessible check is not zero visibility.

Use the template's `claim_id` to connect a source claim, page finding and proposed fix. Keep optional page components, agent usability and conversion experiments separate from search eligibility. Record the baseline, approved change, follow-up dates and possible confounders before any experiment. Keep indexing, citations, referrals, conversions, revenue and causality separate; a layout review establishes none of them. Never fill outcome fields from a source's marketing percentages.

This review produces proposed fixes only. Publishing, account creation, external sends, new paid calls, tool installs, crawler/security changes and scheduled monitoring need their own applicable approval. No cadence or follow-up is activated by copying the template.

### Checked sources (24 October 2026)

- [Google AI features and ordinary Search requirements](https://developers.google.com/search/docs/appearance/ai-features)
- [Google structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) and [Article guidance](https://developers.google.com/search/docs/appearance/structured-data/article)
- [Google FAQ rich-result removal notice](https://developers.google.com/search/updates#removing-faq-rich-result)
- [OpenAI crawler roles](https://developers.openai.com/api/docs/bots) and [ChatGPT search providers](https://help.openai.com/en/articles/9237897-chatgpt-search)
- [Anthropic crawler roles](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Perplexity crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers.md)
- [IndexNow protocol, ownership and receipt meanings](https://www.indexnow.org/documentation)
- [llms.txt proposal](https://llmstxt.org/) — optional agent-documentation format, not proof of a ranking requirement
- [GEO paper, version 3, 28 June 2024](https://arxiv.org/html/2311.09735v3) — experimental evidence, not the post's unverified 10K-website study
