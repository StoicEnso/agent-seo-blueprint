---
title: Research for Existing Sites — Steal Competitors' Keywords & Pages
area: research
source_lessons: ["02-14","02-15","02-16","02-17"]
tools: [ahrefs, serp]
---

# Research for Existing Sites — Steal Competitors' Keywords & Pages

**What it is.** Keyword research for a site that already exists. The goal is to find low-hanging fruit you're not yet ranking for by reverse-engineering competitors: the keywords they rank for that you don't (Organic Keywords), the *pages* they built that you didn't think of (Top Pages), automated keyword gaps (Content Gap), and related-term rabbit holes off your own main keyword (Also Ranks For).

**When to use.**
- You have a live site/product and want more rankings and traffic.
- A site is stagnant or declining and you need new keyword/page ideas.
- You want quick wins: terms you can rank for by adding a phrase or building one page.

**Method — Step 1: Mine a competitor's Organic Keywords (the keyword-add quick wins).**
1. Identify your main keyword and find the top-ranking competitor for it (search it on google.com, US).
2. In Ahrefs → **Site Explorer**, enter the competitor's URL → **Organic Keywords** to list every term they rank for (position, KD, volume).
3. Scan for keywords you *don't* rank for or rank poorly on — especially LSI variants and near-zero-KD terms with real volume.
4. For terms you can win by simply adding the phrase to an existing page, do exactly that: add the keyword/phrase to your tool or page so Google associates you with it. Often Google doesn't equate two synonyms (e.g. `PFP` vs `DP`) automatically — adding the missing word unlocks the traffic.

**Method — Step 2: Mine a competitor's Top Pages (find pages you should build).**
1. In Site Explorer → **Top Pages** to see which of the competitor's *pages* pull the most traffic.
2. For an interesting page, use the URL dropdown → **overview** to see that page's specific keywords.
3. Look for pages built around an angle you don't cover at all (a side tool, a meme/variant page, a themed pack). These reveal whole new pages worth creating.
4. Watch for the competitor's mistakes: **keyword cannibalization** (multiple of their pages fighting for one keyword) is a weakness you can exploit by having one focused page.
5. Build the missing page (often a quick tool or themed variant), make it better (match-and-exceed), then upsell your main product from it. Export keyword lists to a spreadsheet when triaging at scale.

**Method — Step 3: Content Gap (automated gap finding).**
1. In Ahrefs → **Content Gap** (competitive analysis): enter your domain plus 2-3 competitor domains.
2. "Show keyword opportunities" returns keywords where competitors rank in the top but you don't.
3. Triage the list — drop terms that are too hard (high KD/authority); keep realistic gaps.
4. For promising gaps, drill deeper with Keyword Ideas / Also Ranks For to assess the surrounding cluster, exactly as in new-niche research.
5. Note: this is the automated counterpart to the manual Top Pages dig — faster, but the manual approach surfaces nuances the tool misses; do both.

**Method — Step 4: Also Ranks For off your own keyword (the related-term rabbit hole).**
1. Put your main keyword in **Keyword Explorer** → **Also Ranks For** to get topically related terms.
2. Filter: minimum volume ~500, and filter out branded terms and (usually) non-commercial intent unless relevant.
3. Because these terms are topically related to what you already rank for, your site is well-positioned to rank for them too.
4. Pick promising ones and go deeper (Also Ranks For on those, then again) — keep descending the rabbit hole to surface long-tail and regional variants (e.g. `DP for Instagram`, heavy in India/Asia, vs `PFP` in the West).
5. Decide whether each opportunity warrants adding a keyword to an existing page or building a new dedicated page.

**Decision criteria / heuristics.**
- Cheapest win first: if you can rank by *adding a phrase* to an existing page, do that before building anything.
- Google doesn't always merge synonyms — explicitly add the missing variant (PFP/DP, picture/photo, etc.).
- A competitor's high-traffic page on an angle you lack = build that page.
- Competitor keyword cannibalization = an opening for your single focused page.
- Keep one page per main keyword; spin up new pages for secondary keywords rather than overloading the main one.
- Also Ranks For: minimum ~500 volume, strip branded/non-commercial terms, then go deeper.
- Run both manual (Top Pages) and automated (Content Gap) gap-finding.

**Example.** For `profilepicture.ai` (main keyword `PFP maker`), inspecting the top competitor's Organic Keywords surfaced `DP pic` / `profile photo maker` with big volume and ~0 KD that the site didn't rank for — fixable by adding those phrases to existing pages. Their Top Pages revealed standalone pages (a crypto "laser eyes" page, a "funny PFP" page) pulling easy traffic on low-KD terms — each a new page to build and upsell from. Content Gap and Also Ranks For (e.g. `DP for Instagram`) added more. This same digging is literally how HeadshotPro was discovered inside Profile Picture AI.

**Pitfalls.**
- Building new pages before grabbing the free wins of adding missing phrases to existing pages.
- Assuming Google equates your synonyms automatically (it often doesn't).
- Relying only on the automated Content Gap and missing manual Top Pages insights (or vice versa).
- Chasing non-commercial / branded Also-Ranks-For terms when revenue is the goal.
- Cannibalizing your own keywords by targeting the same term with multiple pages.

**Related.** [[competitor-research]], [[keyword-fundamentals]], [[seo-metrics]], [[match-and-exceed]], [[finding-and-validating-niches]], [[keyword-to-sitemap]]. Course refs: 02-14 (research for existing businesses), 02-15 (finding keywords in top pages), 02-16 (content gaps), 02-17 (also ranks for).


## Process-first audit before acquisition or automation

Use this section when auditing an existing site's business workflow, not just its page markup. It adapts Vas's [19 October 2026 article](https://x.com/vasuman/status/2112287872615387215), “Where to Begin With AI Transformation.” His improvement percentages and client examples are attributed experience, not independently verified results or targets for another business.

1. **Start with the completed customer job.** Name the useful result and its owner. Prioritize a workflow by evidenced volume, human cost, risk, and cross-team handoffs. If these inputs are unavailable, provide an unranked shortlist; do not invent a financial score or assume finance is always first.
2. **Agree the baseline before building.** Record the measurement period, attempted and completed jobs, human touch time, waiting time, exception/rework rate, actual costs and evidence source. Keep processing speed, end-to-end time, released capacity, cash savings and extra revenue separate. A model is not a measured customer result. Never count the same released hours as both saved payroll and new sales without a justified allocation.
3. **Map the real work.** Combine permitted event logs with operator interviews and representative difficult cases. Include intake, informal email/manual work, queues, approvals, handoffs and downstream failures. A public-site journey is only a `public_proposal`; it cannot establish the actual internal bottleneck. Use `first_party_validated` only with evidence for each step. Missing private evidence is `not_measured`, not zero.
4. **Delete or simplify first.** For each step record `delete | simplify | deterministic_code | model_assist | human_decision`. Fixed rules normally belong in ordinary code; variable documents may justify model assistance. Do not automate an unnecessary handoff or remove a legal, consent, security or expert-review control.
5. **Keep existing systems and knowledge boundaries.** Define inputs, outputs, owner, source/version, permissions, data retention and exception route. Reuse existing systems where appropriate. A shared knowledge store is not permission to copy private material across accounts, customers or teams.
6. **Prove the pilot without live effects.** Use read-only analysis, drafts, or shadow mode. Shadow mode compares proposed decisions with the approved human process; it must not send, publish, file, charge or change production. Include non-happy-path cases, stop conditions, quality/risk checks and an explicit human promotion decision. Existing approvals and owner holds still apply; this method grants no new authority.
7. **Measure useful staff work.** Capture reusable staff procedures only after real cases show value. Measure completed-job time, quality, exceptions and cost, not seats, tokens, tasks launched or agents installed. Retain the baseline and limitations when reporting progress.

### Output and offline review

Use `assets/process-first-audit-input.json` for one or more sites. A public-only audit must identify which internal facts remain unknown and the one bounded pilot that could test the hypothesis. It must not call itself a completed process-discovery or return-on-investment audit.

```bash
python3 scripts/audit_evidence_review.py \
  --input assets/process-first-audit-input.json \
  --output /your/project/audits/process-evidence-summary.json
```

The helper reads local JSON only. It validates evidence states, calculates measured human minutes per completed job and exception rates only when the inputs support them, and keeps provider/surface/locale observation lanes separate. It never makes a network call, spends money, sends outreach, changes a site or promotes a pilot. Empty provider observations are not zero visibility. See the existing `cross-platform-ai-citation-loop.md` playbook for citation-source work; keep SEO acquisition and operational delivery evidence separate.
