---
title: On-Page Optimization (Four High-Impact Basics)
area: content
source_lessons: ["03-22"]
tools: [serp]
---

# On-Page Optimization (Four High-Impact Basics)

**What it is.** Four on-page fundamentals that are easy to get right and meaningfully affect rankings: internal linking, meta titles/descriptions, page speed, and canonicals. (General on-page SEO is well-documented elsewhere; this is the high-leverage shortlist.)

**When to use.**
- On every page you publish — apply these as a checklist for all content types.
- When auditing why content with good keywords and links still underperforms.

**Method.**
1. **Internal linking & site authority.** Treat the site as a whole. From each content page, link to other related pages so page authority spreads across the site and search engines understand its structure and which pages relate. Link related content together deliberately.
2. **Meta titles & descriptions.** Put the main target keyword in the meta title. Use synonyms/variants in the meta description (e.g. "profile picture" + "DP"). Critically, the title must match the user's search intent and read naturally — if there's no visible match between the query and the title, searchers bounce thinking they landed in the wrong place.
3. **Page loading speed.** Make pages fast — slow pages (5-10s loads) hurt both rankings and conversion, and Google penalizes slow sites. Prefer statically generated pages (e.g. pre-built HTML with Nuxt) that serve instantly with no server-side loading; ensure all content/images are present and fast.
4. **Canonicals.** Use canonical tags to tell Google which is the main page, so duplicate or parameterized URLs don't dilute SEO. Point variant URLs (e.g. shared affiliate links with URL parameters) at the canonical main page so Google ignores the duplicates and consolidates authority on one page.

**Decision criteria / heuristics.**
- Title must satisfy the searcher's intent, not just contain the keyword — match-and-exceed applies to metadata too.
- Static generation is the default for speed where the framework allows it.
- Any time URL parameters create many near-identical pages, reach for canonicals.
- Internal links are free authority distribution — use them on every content page.

**Example.** Google began ranking many of an operator's affiliate URLs because a shared URL parameter created hundreds of near-duplicate pages. Adding a canonical (on every page, or at least the homepage) pointing those parameterized URLs at the single main page told Google to ignore the duplicates and consolidate all that SEO value onto one page instead of scattering it.

**Pitfalls.**
- Obscure titles that don't mention what the page is (e.g. omitting "profile generator" for "profile picture maker") → bounces.
- Slow pages — great content won't rank if it loads slowly.
- Letting parameterized/duplicate URLs accumulate without canonicals (splits authority; see content-what-not-to-do on duplicate content).

**Related.** [[content-what-not-to-do]], [[content-fundamentals]], [[free-tools-strategy]], [[content-pages]] · course ref 03-22.
