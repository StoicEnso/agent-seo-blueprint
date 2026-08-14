---
title: Content Types Overview (Picking the Right Format)
area: content
source_lessons: ["03-02","03-11","03-17"]
tools: [serp]
field_inputs:
  - https://x.com/NicholasDulait/status/2087537648747286874
official_sources:
  - https://developers.google.com/search/docs/essentials/spam-policies
  - https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
---

# Content Types Overview (Picking the Right Format)

**What it is.** A map of the content formats available for SEO and how to choose between them. The three formats worth building deliberately are programmatic SEO, free tools, and content pages; landing pages, articles, and content rings are supporting formats used situationally.

**When to use.**
- After keyword research, when deciding which *kind* of page to build for a target keyword or cluster.
- When planning a site's content mix across transactional, commercial-investigation, and informational intents.

**Method.**
1. Read the SERP for the target keyword and identify intent (see content-fundamentals / match-and-exceed).
2. Map intent → format:
   - **Transactional** (ready to buy) → **landing page** focused on the exact keyword.
   - **Informational, scalable** (hundreds of long-tail variants from data) → **programmatic SEO**.
   - **Action/tool keywords** (generator, calculator, maker) → **free tool**.
   - **Informational, structured** (the searcher wants rich content, not a pure article) → **content page** (a hybrid of landing page + blog post: blog-level depth, landing-page structure with components).
   - **Pure informational** the searcher wants written prose → **article** (only if you'll invest in real writing).
   - **Off-site backlink/traffic engine** → **content ring** of separate sites.
3. Default to the operator's strengths: as a developer, prioritize landing pages, free tools, and programmatic/content pages over written articles.

## SaaS demand-page matrix

An August 2026 practitioner article proposed nine SaaS page families. Use them as research prompts, not as a universal priority order, indexing recipe, traffic forecast, or proof of purchase intent. Validate every candidate against live query demand, the current SERP, product truth, distinct user value, overlap with existing pages, and the evidence needed to keep claims current.

| Family | Search job | Publish only when |
|---|---|---|
| **Alternative** | Find a replacement for a named product | The product is a real alternative for the named use case. Any `free`, `open-source`, `cheaper`, or audience modifier is literally true. The page uses fair criteria, current evidence, and explicit limitations. |
| **Comparison** | Choose between named products | The compared products serve an overlapping job. Features, prices, and limitations have cited sources and checked dates. Include material areas where the owner's product loses. |
| **Integration** | Use the product with another platform | A working supported integration or a reproducible workflow exists. Include setup steps, supported actions, limitations, and proof; a partner name in the heading is not enough. |
| **Constraint** | Filter options by a binary requirement | The product verifiably meets the constraint, such as no credit card, no subscription, no installation, no-code, or open source. Do not publish a near-match. |
| **Pricing** | Understand cost or compare price models | Price, currency, billing period, unit, plan limits, taxes/fees where material, source, and checked date are clear. Do not copy stale competitor prices. |
| **Use case** | Complete a specific job | The page has a distinct workflow, audience context, examples, product capability, proof, and next step—not a synonym-swapped feature page. |
| **Problem** | Understand or solve a pain before category selection | The page teaches a useful diagnostic or method and connects the product only where it genuinely helps. Do not mint one page per wording variation. |
| **Feature** | Find a product with a required capability | The feature exists, is materially relevant to the query, and can be demonstrated. Table-stakes features alone rarely justify a separate page. |
| **Audience/company size** | Find a fit for a specific operating context | The workflow, permissions, onboarding, economics, compliance, support, or proof materially differs for that audience. If only the H1 and nouns change, consolidate instead of creating doorway-like variants. |

Before briefing a page, record: `page_family`, exact query/locale, live SERP format, distinct user job, product-truth evidence, comparison/pricing checked dates where relevant, overlap/canonical decision, unique sections or functionality, conversion role, and a reject/consolidate reason when the gate fails.

**Decision criteria / heuristics.**
- A "content page" is the middle ground: more content than a landing page, more structure and components than a blog post. Use it when Google rewards rich-but-structured content for the keyword.
- Don't force a format the SERP doesn't reward — the SERP decides, not your preference.
- Content pages are a family with many sub-patterns (comparison, success stories, niche hubs, examples, integrations) — pick the sub-pattern that matches the keyword modifier.
- Do not inherit the field article's claimed ordering, competition level, intent level, or traffic timing. Rank the local queue with observed demand, business value, winnability, proof strength, implementation cost, and risk.
- Multiple modifiers do not automatically deserve multiple URLs. One useful page can answer several closely related variants when the user job and SERP format are the same.

**Example.** For "AI headshots" (transactional) build a landing page; for "tattoo ideas" (scalable informational) build programmatic SEO; for "LinkedIn profile generator" (action keyword) build a free tool; for "Ahrefs vs SEMrush" (commercial comparison) build a content page (comparison sub-pattern). Same business, four formats, chosen by intent.

**Pitfalls.**
- Treating "blog post" as the default answer to every keyword.
- Mixing formats that fight the SERP's demonstrated preference.
- Publishing `free`, `open-source`, `cheaper`, integration, feature, pricing, or audience claims that product evidence cannot support.
- Swapping a product, audience, or company-size token across substantially similar pages. Google's current spam policies identify substantially similar pages for similar queries that funnel users onward as doorway abuse, and its generative-AI guidance rejects mass pages for query variations when the primary purpose is ranking manipulation.

**Related.** [[content-fundamentals]], [[programmatic-seo]], [[free-tools-strategy]], [[content-pages]], [[landing-pages]], [[articles]], [[content-rings]] · course refs 03-02, 03-11, 03-17.
