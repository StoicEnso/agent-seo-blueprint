---
title: Content — What Not To Do
area: content
source_lessons: ["03-21"]
tools: []
official_sources:
  - https://developers.google.com/search/docs/essentials/spam-policies
  - https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
---

# Content — What Not To Do

**What it is.** The content-creation mistakes that get a site penalized, deranked, or blacklisted. Avoiding these protects all the legitimate work you've done; a blacklisted domain may never recover.

**When to use.**
- As a pre-publish checklist for any content, especially anything generated or templated at scale.
- When diagnosing a ranking drop that isn't explained by competition or a Google update.

**Method (avoid each of these).**
1. **No scaled AI content spam.** Don't mass-publish shallow AI-written pages. Google defines scaled content abuse by purpose and lack of user value, regardless of whether pages are made by AI, automation, or people. Human review is useful only when it produces accurate, original, task-completing content; it is not a compliance stamp.
2. **Plan large releases, but do not invent a crawl quota.** Google does not publish a universal pages-per-site-per-month indexing allowance. Crawl-budget work matters most for very large or rapidly changing sites. For a large launch, use canonical URLs, valid sitemaps, reliable internal links, server capacity, cohort QA, and Search Console evidence. Staged releases can reduce operational risk, but `10–30 pages per month` is not a ranking or indexing rule.
3. **No keyword stuffing.** Don't repeat the target keyword (or variants) unnaturally many times. Write naturally; use a content-analysis tool (e.g. Surfer SEO) to check keyword frequency against top-ranking pages rather than overstuffing — over-optimization is flagged as spam and downgrades you.
4. **No duplicate content.** Never steal/copy content from other sites (Google knows who published first). And don't duplicate within your own site — reusing the same meta title/description across hundreds of programmatic pages is read as duplicate content and penalized. Write unique titles, descriptions, and body content per page.
5. **No keyword cannibalization.** Don't have two+ pages targeting the same keyword — Google won't know which to rank, so they bounce around and eventually drop. One main keyword per page (e.g. one page for "AI headshot generator", a different page for "professional headshot").
6. **No thin or commodity content.** Don't ship a page that fails its user job or adds no distinct value. There is no universal `100–200 words` minimum. A concise working tool may be useful; a long synonym-swapped page may still be thin. Add instructions, examples, evidence, limitations, FAQs, or original functionality only when they help the visitor.
7. **No doorway or query-variation factories.** Do not create substantially similar alternative, integration, location, audience, company-size, feature, problem, or fan-out pages that funnel users to the same destination. Google defines doorway abuse around similar query-targeted pages that are less useful than the final destination, and warns against creating separate pages for every query variation primarily to manipulate rankings or generative-AI responses. Consolidate variants that share the same job and content.

**Decision criteria / heuristics.**
- If a tactic is designed to trick Google rather than help the user, assume it will eventually be caught and penalized.
- Scale (programmatic SEO, tools) is fine; scale of *shallow* or *duplicated* content is not.
- Use staged releases when they improve QA, infrastructure safety, and measurement—not because of a made-up monthly crawl allowance.
- A new modifier deserves a new URL only when demand, intent, product truth, and page value are distinct.

**Example.** A SaaS plan finds demand for `tool for freelancers`, `tool for small businesses`, and `tool for teams of five`. If the product, workflow, proof, and offer are the same, build one strong audience-fit page or improve the core page instead of cloning three headings. If permissions, onboarding, pricing, compliance, workflows, and proof differ materially, separate pages may be justified after live SERP and cannibalization checks.

**Pitfalls.** (this playbook is the pitfall list) — the meta-pitfall is assuming Google won't notice; it does, eventually, and recovery is slow or impossible.

**Related.** [[programmatic-seo]] (crawl budget, duplicate meta), [[free-tools-strategy]] (thin content), [[articles]] (AI spam), [[on-page-optimization]] (canonicals for duplicates), [[content-rings]] (PBN risk) · course ref 03-21.
