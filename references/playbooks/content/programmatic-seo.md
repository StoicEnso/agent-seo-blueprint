---
title: Programmatic SEO (pSEO)
area: content
source_lessons: ["03-03","03-04","03-05","03-06"]
tools: [ahrefs, serp, dataforseo, openai, mongodb, screenshot-api, google-maps-api]
---

# Programmatic SEO (pSEO)

**What it is.** Using code to generate many SEO pages from a structured dataset: identify a repeatable demand pattern, acquire and shape trustworthy data, then template pages that each satisfy a specific search intent. It is not permission to clone a page and swap one token.

**When to use.**
- A keyword family has a repeatable shape and enough validated long-tail demand to justify a page system.
- The product can supply useful data, utility, examples, comparisons, or other page-level value at scale.
- The page family has a credible conversion path and a sustainable update owner.
- Skip pSEO when there are only a handful of valuable pages, the source data is weak, or every page would say essentially the same thing.

## Method

1. **Identify the opportunity.** Validate the head term and long-tail family with live SERPs plus DataForSEO/Ahrefs. Count plausible pages after deduplication; do not confuse every combinatorial variation with real demand.
2. **Choose a demand pattern.** Load `programmatic-pattern-library.md`. Classify the opportunity as one primary pattern: curation, comparison, use case, integration, template, converter, examples, directory, glossary, localization, location, or profile. Select from observed search behavior, not trend lists.
3. **Design the page structure first.** Lock hub, category, and leaf URL/keyword rules before generation. Define canonical and cannibalization rules. Estimate crawl/indexation load and generation cost.
4. **Create a unique-data ledger.** For every page family define the fields that make each leaf genuinely different: source, provenance, freshness, first-party element, user utility, and update cadence. At least one page-specific field is mandatory; high-risk families need several.
5. **Gather raw data.** Acquire source data from first-party product usage, user contributions, APIs, vetted datasets, or controlled scraping. Keep source URLs/timestamps and respect rights/terms.
6. **Shape the data into content.** Normalize, deduplicate, classify, summarize, and calculate. AI may transform records but must not invent missing facts. Add quality thresholds that prevent empty/thin leaves from publishing.
7. **Build hub and leaf templates.** Inject data into titles, H1/H2s, body, visuals, answer blocks, internal links, schema, and conversion modules. Every page must resolve its query independently and offer value beyond the raw source.
8. **Layer only after one pattern works.** Combining dimensions can create useful narrow queries, but it also creates combinatorial spam. Require live demand, distinct intent, enough unique data, and a hard page-count cap for each layered family.
9. **Launch in cohorts.** Publish a small validation cohort first, inspect crawl/indexation/rank/engagement/conversion and quality failures, then expand. Do not dump thousands of unproven URLs into the index.
10. **Inject the offer without breaking intent.** Place contextual CTAs, product modules, or tool actions where they help the searcher. Do not turn an informational page into a disguised checkout page.
11. **Monitor and prune.** Track indexation, impressions, ranking, conversions, stale data, near-duplicates, and orphan pages. Refresh useful pages; consolidate, noindex, or retire pages that cannot earn their place.

## Required pSEO brief fields

Add these to every pSEO plan:

- `primary_pattern`
- `query_formula`
- `dimensions[]`
- `validated_keyword_examples[]`
- `estimated_unique_pages_after_dedupe`
- `hub_category_leaf_model`
- `data_sources[]` with provenance/freshness
- `unique_data_ledger[]`
- `minimum_publish_threshold`
- `canonical_and_cannibalization_plan`
- `internal_link_graph`
- `conversion_path`
- `indexation_cohorts[]`
- `update_cadence_and_owner`
- `kill_or_consolidate_rules`

## Decision gates

- **Demand gate:** repeated query shape is visible in live keyword/SERP data.
- **Value gate:** each leaf does something the raw data source or generic search results do not.
- **Data gate:** unique data is trustworthy, attributable, maintainable, and present before publish.
- **Intent gate:** the template format matches the exact SERP intent.
- **Scale gate:** the useful page count is large enough to justify code, but capped below combinatorial nonsense.
- **Quality gate:** leaves below the data/content threshold do not publish.
- **Operations gate:** there is an owner and cadence for refresh, monitoring, and pruning.

## Evidence-safe AI-search guidance

Structured, answerable pages can improve extractability for answer engines, but search/citation performance must be measured rather than promised. Include:

- a direct answer near the top when the query warrants it
- explicit “who this is for” or selection guidance on decision pages
- clean entity names, attributes, comparisons, and cited facts
- first-party screenshots/data/examples where lawful
- section-level standalone clarity
- visible freshness and source provenance

Do not repeat vendor traffic, revenue, or citation percentages as guarantees. Treat them as case-study leads to verify independently.

## Worked lessons

- **TattoosAI:** first-party/user-generated visual data can sustain many category leaves when taxonomy and page-depth thresholds are real.
- **Landingfolio:** a curated screenshot dataset plus useful filters/counts can outperform raw listings and open adjacent page families.
- **HeadshotPro near-me failure:** reformatting Google Maps data without enough new value produced shallow pages that did not rank. This remains the most important negative example.

## Pitfalls

- token-swapped pages with no unique data
- combinatorial layering before validating one primary pattern
- keyword/URL structure chosen after expensive generation
- fabricated or stale facts
- duplicate metadata, canonicals, or overlapping intent
- mass publishing without crawl/indexation cohorts
- no owner for refresh/pruning
- projecting vendor case-study results onto a new site

**Related.** [[programmatic-pattern-library]], [[content-fundamentals]], [[free-tools-strategy]], [[content-pages]], [[content-what-not-to-do]], [[on-page-optimization]] · course refs 03-03 through 03-06.
