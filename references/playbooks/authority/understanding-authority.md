---
title: understanding-authority
area: authority
source_lessons: ["04-01", "04-02", "04-03", "04-04"]
tools: [ahrefs]
---

# understanding-authority

**What it is.** The mental model for why backlinks matter and how their value is calculated, plus the precondition (a genuinely good product) that makes every later link tactic possible. This is the foundation you load before running any specific link-building playbook.

**When to use.**
- Before starting any link-building campaign, to set strategy and expectations.
- When deciding whether a given backlink opportunity is worth the effort.
- When explaining to a stakeholder why content + keywords alone aren't producing traffic.

**Method.**
1. Treat a backlink as a vote of confidence: one site linking to yours signals to Google that yours is worth visiting. Without enough of these votes, even great content and keywords won't earn rankings.
2. Weight links by the linking domain's authority, not just the count. Authority is logarithmic, so a domain rating (DR) 50 site passes roughly 10x the value of a DR 40 site. Prioritize a few high-DR links over many low-DR ones.
3. Account for link dilution: the value of a page is split across every outbound link on it. A page linking to 100+ sites passes almost nothing to each; a page linking to only one or two passes most of its value to you. This is why bought "listicle" links on link repositories are weak even when the domain is DR 70 — the value is shared across all the other listed sites.
4. Confirm your product/page is link-worthy before outreach (see step 6). Link tactics that involve displacing a competitor only work if you're objectively better.
5. Map the landscape in Ahrefs first: Site Explorer the top-ranking competitor for your target keyword, open its Backlinks report, and note which referring domains are high-DR and dofollow. These become your target list across the other playbooks.
6. Audit your own product/landing page as if you were a writer about to link to it. Remove anything that makes linking embarrassing: broken flows, intrusive cookie/marketing pop-ups, slow or ugly pages. A link is a public endorsement; nobody endorses a bad experience.

**Decision criteria / heuristics.**
- Prefer high-DR + few outbound links + dofollow + topically relevant. Any one of those missing lowers the link's value.
- A high-DR link buried in a 200-link page can be worth less than a mid-DR link that's one of two on the page.
- If the page/product isn't yet better than the incumbent, fix the product first; link-stealing and displacement tactics depend on "match and exceed."
- Backlinks also feed LLM answers (ChatGPT and similar surface the top-ranking pages and the brands mentioned in them), so authority compounds beyond classic Google rankings — treat it as a long-term asset, not a dying tactic.

**Example.** You want to rank an AI headshot tool. You Site Explorer the #1 competitor in Ahrefs and find 40 referring domains. Twelve are DR 60+ review/listicle sites, the rest are scattered low-DR blogs. You ignore the long tail and build a target list of the 12 high-DR pages — these are where displacing the competitor (link stealing) and affiliate placements will move the needle most. Before emailing anyone, you strip a pop-up off your landing page so writers who click through aren't put off.

**Pitfalls.**
- Buying backlinks on shared link repositories/listicles: the DR looks high but value is split across every link on the page, so it's effectively a low-quality link (and risky — see [[linkbuilding-what-not-to-do]]).
- Chasing link volume over link quality; ten DR 20 links rarely match one strong DR 60 link.
- Starting outreach before the product/page is genuinely good — every displacement tactic falls apart if you aren't actually better.

**Related.** [[link-stealing]], [[affiliate-programs]], [[manual-outreach]], [[linkbuilding-what-not-to-do]]. Course refs: 04-01, 04-02, 04-03, 04-04. Builds on Research "Match and exceed" (02-06).
