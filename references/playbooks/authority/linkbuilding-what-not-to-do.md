---
title: linkbuilding-what-not-to-do
area: authority
source_lessons: ["04-14"]
tools: [ahrefs, search-console]
---

# linkbuilding-what-not-to-do

**What it is.** The guardrails for link building: the manipulative tactics that get a site flagged, demoted, or permanently de-ranked by Google — and the cleanup tool (disavow) for when bad links land on you anyway.

**When to use.**
- Before approving any aggressive or paid link tactic, to confirm it won't trigger a penalty.
- When auditing your own backlink profile or a competitor's spike that looks too good to be true.
- When affiliate or third-party spam dumps low-quality links on your domain and you need to neutralize them.

**Method — what NOT to do.**
1. **Don't buy cheap, low-quality link packages** (e.g. $10 Fiverr "thousands of backlinks"). They may spike traffic briefly, but Google identifies the obviously fake profile and demotes/de-ranks the site — often permanently, with no recovery.
2. **Don't over-optimize anchor text.** Sellers ask for your target keyword and stuff hundreds of links with that exact anchor (e.g. "professional headshots"). Real backlinks don't all use your keyword as anchor — natural anchors are often the bare title, the URL, brand name, or something random. Uniform keyword anchors are a clear manipulation signal.
3. **Don't spam your URL across forums/Quora/Reddit and comment sections.** Mass self-linking is detected and gets the domain demoted. Only contribute where you add genuine value, and link sparingly.
4. **Avoid link farms and private blog networks (PBNs)** — operators who own hundreds of interlinked blogs and inject your link across all of them for an instant backlink dump. Google increasingly identifies these; they're a reliable way to get banned. (This is the line your own [[content-rings-for-links]] must never cross.)
5. **Don't build links on irrelevant, off-topic sites.** A backlink from a site with nothing to do with your niche is an obvious mismatch. Relatedly, don't repurpose a domain into a different niche than its history: the course example of an ex-travel-agency domain (14 years as travel) rebuilt as a fitness blog got de-ranked because Google still expected travel content — see also [[acquiring-domain-authority]].
6. **Don't turn easy hosted-publishing APIs into a page farm.** “Unlimited,” high-authority, or automated page creation does not justify spun copies, doorway pages, fake authors, exact-match-anchor batches, or one near-identical article per owned site. Inspect the actual public page and rendered `rel`; a domain metric, `index, follow`, or successful API response does not prove a followed link or indexation. See [[hosted-publishing-experiments]].

**Method — cleanup (disavow).**
7. Periodically review new referring domains in Ahrefs and Google Search Console.
8. For links you didn't earn and don't endorse (affiliate spam, junk farms), build a disavow file and submit it via Google's disavow tool in Search Console. This tells Google to ignore those links — you're declaring you don't vouch for them — protecting your profile from third-party spam.

**Decision criteria / heuristics.**
- If a tactic is bought, automated at scale, or uses uniform keyword anchors, treat it as high-risk and default to not doing it.
- Relevance is mandatory: a link only helps if the source site is topically related to yours.
- A penalty here can be permanent — the asymmetry (small upside, catastrophic downside) means err heavily toward caution.
- Disavow is for links you genuinely don't endorse; don't disavow legitimate links.

**Example.** The course cases: one competitor bought bad backlinks, saw a temporary traffic surge, then was de-ranked permanently once Google flagged the fake profile. Another (instaheadshots) bought hundreds of links all anchored "professional headshots," a pattern Google penalizes. And the fit.nl domain — 14 years a travel agency — was rebuilt as a fitness blog and stopped ranking because the niche didn't match Google's expectation for that domain.

**Pitfalls (meta).**
- Assuming a brief traffic spike from bought links means it worked — the demotion comes later and is often unrecoverable.
- Letting affiliate or PBN spam accumulate without disavowing it.
- Confusing your own legitimate content ring with a PBN — the difference is real, useful, individually-earned properties vs. bought interlinked junk.

**Related.** [[content-rings-for-links]] (the PBN line), [[acquiring-domain-authority]] (niche-mismatch de-ranking), [[affiliate-programs]] (disavow workflow for affiliate spam), [[other-link-building]] (ABC boosting / swap-overuse risk), [[understanding-authority]]. Course ref: 04-14.
