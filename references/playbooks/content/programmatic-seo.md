---
title: Programmatic SEO (pSEO)
area: content
source_lessons: ["03-03","03-04","03-05","03-06"]
tools: [ahrefs, serp, openai, mongodb, screenshot-api, google-maps-api]
---

# Programmatic SEO (pSEO)

**What it is.** Using code to generate hundreds or thousands of SEO pages from a structured dataset: acquire raw data, shape it into consumable content, and template it into a page tree that ranks for one head keyword plus a large family of long-tail keywords. Best for informational/curation content (idea galleries, directories, curated collections), not for handfuls of pages.

**When to use.**
- A keyword family is genuinely scalable — hundreds of long-tail variants (cities, categories, names, types) all with search volume and low difficulty.
- The content can be produced from data (user-generated content, an API, a scraper) rather than hand-written.
- Skip pSEO when you only have 3-5 pages' worth of opportunity — just write those by hand.

**Method (the six steps).**
1. **Identify the opportunity.** In Ahrefs, find a head keyword whose long-tail variants number in the hundreds/thousands with low keyword difficulty (Ahrefs will show the volume of matching keyword ideas). If it doesn't scale to hundreds of pages, it isn't a pSEO opportunity.
2. **Design the page structure first.** Lock the head keyword for the hub page and the long-tail pattern for the leaf pages BEFORE generating anything — getting this wrong wastes real money in AI generation credits. Plan the tree: hub → category → (optional) sub-category/leaf.
3. **Gather raw data.** Collect ugly source data at scale: user-generated content, a queryable API, or a scraper. This step is just acquisition; the data is not yet presentable.
4. **Shape the data into content.** Transform ugly data into consumable content: have AI summarize/rewrite descriptions, auto-tag and categorize items, group items, count them. Run this on a schedule (cron) so new data flows in continuously.
5. **Display / template it.** Build one hub template and one leaf template. Programmatically inject the keyword and dynamic numbers into title, H1/H2 and body; auto-generate meta titles (e.g. "{count} Best {keyword} Designs and Inspiration"); decide on screenshots/images. Pages get built from the database on deploy.
6. **Inject your offer.** Because this is informational content, monetize by promoting your own product inside the pages — CTA buttons between items, a featured "position" that is actually your product, pop-ups. This turns free traffic into customers.

**Decision criteria / heuristics.**
- Scalability gate: hundreds of pages possible → pSEO; only a few → write manually.
- Build the page-structure/keyword plan before spending generation credits.
- Depth beats breadth: every leaf page must give the user a reason to choose you over the raw source (e.g. over Google Maps itself). Shallow templated pages do not rank.
- Stagger indexing — don't dump 1000 pages on Google at once (see content-what-not-to-do: crawl budget).

**Worked examples.**

*TattoosAI (successful, ~$4k/mo, fully autonomous).* Opportunity: huge low-difficulty volume for "tattoo ideas" variants (rose, flower, finger, name tattoos), ~2000 page options in Ahrefs. Structure: hub "tattoo ideas" → leaf "{keyword} tattoo ideas" (e.g. dragon, family, Greek). Data: a free/paid AI tattoo generator made USERS generate the raw content (hundreds of thousands of tattoos from their prompts). Shape: a daily cron pulls new generations, saves the prompt, AI extracts and tags categories (e.g. "black cat" → cat tattoo); a second cron groups and counts items; any new category passing ~100 items gets its own page with an AI-written description and headers. Display: auto-built category pages of generated tattoos. Offer: "design your own tattoo" CTAs between items linking to the paid generator. The whole machine ran on autopilot with no manual upkeep.

*Landingfolio (successful, 1-2k visitors/day, runs untouched for years).* Opportunity: lots of search for landing-page inspiration by type (SaaS, product, mobile-app, marketing). Structure: hub "landing page inspiration" → leaf categories by industry, URL like /inspiration/landing-page/product. Data: a screenshot API capturing desktop + mobile of homepages (later also pricing pages, by appending /pricing); a Product Hunt scraper pulling the day's top 10 to review and add. Shape: tag each screenshot with keywords found in Ahrefs (manual pre-AI; would be AI now). Display: ONE template that swaps only the keyword + a live count; auto SEO title like "{count} Best Marketing Landing Page Designs and Inspiration"; categories pulled from MongoDB and pages built on deploy. Offer: a paid Figma/Webflow/Tailwind component library added later as upsell. This is curation — bundle the best of what's already out there. Bonus: scraping pricing pages opened a whole new ranking surface ("pricing page design") for free.

*HeadshotPro "near me" (FAILED — instructive).* Opportunity: "headshots near me" + per-city variants (New York, Dallas, SF) across thousands of cities. Structure: hub "headshot photographers near me" listing countries → country page listing cities → city leaf "professional headshots in {city}". Data: Google Maps API returns photographers per city; scrape their sites + reviews (52 US cities, ~240 studios). Shape: AI-write a Yelp/TripAdvisor-style breakdown of the top 5 per city (reviews, address, summary). Offer: at position 2, pitch "get AI headshots now instead of waiting for an appointment." It never ranked and was taken down. Why: shallow content — it added nothing a user couldn't get by filtering Google Maps directly. The lesson: pSEO only works when each page adds real value beyond its data source.

**Pitfalls.**
- Shallow content: re-listing API/Maps data with no added value gives users (and Google) no reason to pick you — it won't rank.
- Locking keywords/structure too late and burning generation credits on the wrong target.
- Duplicate meta tags across hundreds of templated pages (penalized as duplicate content — vary titles/descriptions).
- Mass-publishing all pages at once and blowing the crawl budget.

**Related.** [[content-fundamentals]], [[free-tools-strategy]], [[content-pages]], [[content-what-not-to-do]], [[on-page-optimization]] · course refs 03-03 (method), 03-04 (TattoosAI), 03-05 (Landingfolio), 03-06 (HeadshotPro failure).
