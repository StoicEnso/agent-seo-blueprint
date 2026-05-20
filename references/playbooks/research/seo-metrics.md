---
title: Key SEO Metrics & Thresholds — KD, Authority, Volume, CPC
area: research
source_lessons: ["02-07"]
tools: [ahrefs, serp]
---

# Key SEO Metrics & Thresholds — KD, Authority, Volume, CPC

**What it is.** The four metrics Danny actually filters and decides on in Ahrefs: Keyword Difficulty (KD), Domain/Page Authority, Search Volume, and Cost Per Click (CPC). Each has a concrete threshold that turns a keyword from "interesting" into "build it" or "skip it."

**When to use.**
- Every time you evaluate a candidate keyword.
- When setting filters in Ahrefs Keyword Explorer before browsing lists.
- When comparing yourself against the sites currently ranking.

**Method.**
1. **Keyword Difficulty (KD).** Estimates how hard it is to rank. Filter your keyword lists to KD < 20. At KD ≤ 20 you typically need only ~10 backlinks, so a new low-authority site can reach the top within ~1-2 months. Higher KD means stronger backlink competition you can't beat early on.
2. **Domain Authority (DA) & Page Authority (PA).** DA = whole-site authority (backlink strength); PA = a single page's authority (Ahrefs calls page-level "URL rating"). When you look up a keyword, check the DA *and especially the PA* of the pages ranking top 3. A high-DA site can still have a weak top-ranking page (few links to that specific URL) — that's beatable. Authority is logarithmic: each 10 points is ~10× the previous, so a DA-60 link is ~10× a DA-50 link, and a DA-90 link (e.g. CNN) is worth orders of magnitude more than a DA-10 link.
3. **Search Volume.** Estimated monthly searches for *that exact keyword* (LSI/related terms not included). Use US volume by default — usually the highest-paying market — but check global too. Apply the click-curve: position #1 ≈ 30% of clicks, #2 ≈ 15%, #3 ≈ 10%. Hard-skip anything under 100 volume; strongly discount under 500.
4. **CPC (cost per click).** What advertisers pay per click for the term in Google Ads. Use it as a monetization filter: high volume + meaningful CPC = people pay real money for this traffic → moneymaker. High volume + near-zero CPC (1-2 cents) = traffic nobody monetizes → usually not worth it.
5. **Combine into a verdict.** The ideal keyword: KD < 20, volume comfortably > 500, weak page authority among the top 3, and a healthy CPC. Run the live SERP to confirm content type and exceedability (see [[match-and-exceed]]).

**Decision criteria / heuristics.**
- KD < 20 → rankable as a new site (~10 backlinks, 1-2 months).
- Volume < 100 → skip. Volume < 500 → discount heavily.
- Sanity-check expected clicks: at #3 you get ~10% of volume; 150 volume → ~15 clicks/mo → at 1% conversion ≈ 1 sale/year (worthless).
- Top-3 pages with low PA / few referring domains → beatable even if DA is high.
- High volume + ~$0 CPC → traffic isn't monetizable, deprioritize.
- High volume + low KD + solid CPC → priority target.
- Prefer US-paying markets, but a healthy global split (e.g. half US, half other Western countries) means more money overall.

**Example.** A keyword with KD 9, 20k US searches, and a real CPC, where the #1 page has a URL rating of ~7 and only ~16 referring domains, is a green light — the difficulty is low and the incumbent's page is weakly linked despite a decent domain. Contrast `car insurance`: KD 83 and $20 CPC — lucrative but unwinnable without CNN-tier authority, so skip the head term and hunt sub-niches.

**Pitfalls.**
- Reading DA alone and missing that the *page* ranking has almost no links (the real bar).
- Falling for low KD on a near-zero-volume keyword — math leaves you with no traffic.
- Ignoring CPC and building for high-volume traffic that earns nothing.
- Forgetting volume is per-keyword only — sum LSI/long-tails to see the real opportunity (see [[keyword-fundamentals]]).

**Related.** [[keyword-fundamentals]], [[match-and-exceed]], [[competitor-research]], [[finding-and-validating-niches]]. Course refs: 02-07 (key SEO metrics).
