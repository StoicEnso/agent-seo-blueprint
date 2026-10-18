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
4. If a missing variant truthfully describes the existing product and serves the same observed search task, draft a natural clarification on the existing owner page. Check current results and inventory first; a synonym gap alone does not prove a new page or traffic gain.

**Method — Step 2: Mine a competitor's Top Pages (find pages you should build).**
1. In Site Explorer → **Top Pages** to see which of the competitor's *pages* pull the most traffic.
2. For an interesting page, use the URL dropdown → **overview** to see that page's specific keywords.
3. Look for pages built around an angle you don't cover at all (a side tool, a meme/variant page, a themed pack). These reveal whole new pages worth creating.
4. Watch for the competitor's mistakes: **keyword cannibalization** (multiple of their pages fighting for one keyword) is a weakness you can exploit by having one focused page.
5. Review the current inventory and search task before proposing a missing page. Improve an existing owner where it already fits; consider a new tool or page only for distinct demand and useful supported value. Export keyword lists to a spreadsheet when triaging at scale.

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
- A competitor's high-traffic page is a research lead, not a build instruction. Confirm demand, intent, existing ownership and useful product fit first.
- Competitor keyword cannibalization = an opening for your single focused page.
- Keep one owner page per evidenced intent cluster, not one page per keyword or synonym. Split only for a distinct supported task after inventory and current-result review; otherwise improve the existing owner or hold.
- Also Ranks For: minimum ~500 volume, strip branded/non-commercial terms, then go deeper.
- Run both manual (Top Pages) and automated (Content Gap) gap-finding.

**Example.** For `profilepicture.ai` (main keyword `PFP maker`), inspecting the top competitor's Organic Keywords surfaced `DP pic` / `profile photo maker` with big volume and ~0 KD that the site didn't rank for — fixable by adding those phrases to existing pages. Their Top Pages revealed standalone pages (a crypto "laser eyes" page, a "funny PFP" page) pulling easy traffic on low-KD terms — each a new page to build and upsell from. Content Gap and Also Ranks For (e.g. `DP for Instagram`) added more. This same digging is literally how HeadshotPro was discovered inside Profile Picture AI.

**Pitfalls.**
- Building new pages before grabbing the free wins of adding missing phrases to existing pages.
- Assuming Google equates your synonyms automatically (it often doesn't).
- Relying only on the automated Content Gap and missing manual Top Pages insights (or vice versa).
- Chasing non-commercial / branded Also-Ranks-For terms when revenue is the goal.
- Cannibalizing your own keywords by targeting the same term with multiple pages.

## Existing category-page recovery review

Use this branch for an established site whose existing commercial page may already own the buyer's task. Improve that page before treating every missing keyword as a new URL. This is a **read-only audit and draft**, not a second content, linking or publishing system.

**Source boundary.** [Keval Shah's case](https://x.com/SEOKeval/status/2111090683423387886), shared in [this post](https://x.com/seokeval/status/2111208227115295222), reports a number-one result for a CBD category in less than four months. The author says the brand already had substantial authority and a mostly clean site. Client URL, query market/device, dated comparable analytics and revenue evidence are not supplied here. Several interventions changed together: the case does not isolate causality or establish a four-month timetable for another site. Its screenshots and third-party traffic estimates are not verified clicks, orders or revenue. Do not recreate its backlink pattern to simulate an established site's history.

### Five review lanes — reuse the existing methods

1. **Establish the owner and technical baseline.** Record the current URL, source/CMS revision, rendered page, HTTP status, robots/indexability, intended and observed canonical, relevant product facts and existing query/page coverage. Keep country, language, device, search type, date range, filters and collection limits with every comparison. Existing referring pages and internal paths provide context, not a guaranteed authority score. If exports or observations are missing, record unknown rather than zero.
   - For a broken inbound destination, inspect the actual referring page, old URL, response/redirect chain and old content before proposing a repair. Restore the original useful content when appropriate; propose a permanent 301/308 only for a confirmed relevant successor. If no equivalent exists, retain an appropriate 404/410 rather than redirecting everything to the homepage. A duplicate label alone does not justify deletion, merging or canonical changes. Route the exact mapping and rollback plan through the [technical audit](../../../workflows/site-audit.md); no repair executes during this review.
2. **Check one intent cluster, not one URL per phrase.** Capture the current results and actual ranking page types for the main query and proposed modifiers in the same market/language/device. Use [search intent](search-intent.md) and [match and exceed](match-and-exceed.md). Similar wording is not proof of shared intent; different wording is not proof of different intent. Keep same-task variants on the existing owner. A separate page needs a distinct user task, current result-format evidence, inventory/cannibalization review and supported original value. If these checks are missing or mixed, HOLD the split. Write one concise accurate title, not a list of every synonym; Google may show a different title link.
3. **Improve the category's buying help, not its word count.** Inspect representative top results for useful questions, selection criteria and page format, then add original product facts, supported differentiation, limitations, availability and relevant FAQs where the reader needs them. Do not copy competitor text, invent reviews or treat the top three results as an exhaustive specification. Put the exact useful draft in the [existing content brief](../../../assets/content-brief.md) and run [content production](../../../workflows/content-production.md). Visible FAQs do not promise FAQ rich results. Health or other high-impact claims require the sourcing and qualified review in the [trust framework](../content/eeat-framework.md); an SEO case study is not medical evidence.
4. **Find useful existing internal paths.** Inspect relevant established categories, guides and hubs for a passage where the target genuinely helps the reader. Capture source URL, existing paragraph, destination canonical, proposed natural anchor and reader benefit in the [existing topic/link ledger](../content/topic-architecture-and-internal-link-ledger.md). Verify that the destination works and the rendered link is crawlable. Prior backlinks alone do not justify an unrelated internal link; do not inject sitewide keyword anchors or promise transferred ranking gains.
5. **Keep external links and outcomes separate.** Route a real editorial opportunity to [authority and links](../../../workflows/authority-and-links.md), not an automatic link order. Do not adopt the case's 40-link quota, 50% keyword-rich-anchor target, DR30+ or 1,000-estimated-monthly-visit cutoffs as safety or ranking rules. Third-party metrics can help research; they do not establish audience fit, editorial merit or policy compliance. Reject paid/exchanged ranking-credit links and automated link schemes. Advertising/sponsorship links need appropriate qualification and their own approval. Log each approved change/revision and rollback separately; if several changes ship together, attribution remains uncertain. Use [measurement](../maintenance/content-opportunity-audit-and-measurement.md) and [monitoring](../../../workflows/monitoring.md) for comparable post-change reads, with search metrics, orders and revenue kept separate. A follow-up plan does not create a schedule.

### Worked ownership decision — illustrative, not a live finding

A retailer already has a patio-paver category. `patio pavers`, `buy patio pavers` and `patio pavers online` are **candidates** to share it, not three pages to build. `how to lay patio pavers` is a candidate for an instructional task, not an automatic new article. Current results and existing guide inventory still decide. The following record deliberately has no collected evidence, no verified product claims and no observed gains. Attach the reviewed evidence to the existing audit findings/brief rather than opening a parallel ledger.

```json
{
  "example_only": true,
  "page_url": "https://shop.example/collections/patio-pavers",
  "existing_owner_url": "https://shop.example/collections/patio-pavers",
  "search_scope": {"country": null, "language": null, "device": null, "observed_at": null},
  "same_intent_candidates": ["patio pavers", "buy patio pavers", "patio pavers online"],
  "separate_intent_candidate": "how to lay patio pavers",
  "ownership_decision": "retain_existing_pending_evidence",
  "new_page_decision": "HOLD",
  "proposed_title": "Patio Pavers | Example Shop",
  "source_revision": null,
  "evidence_refs": [],
  "product_claims_verified": false,
  "approval_status": "DRAFT_NOT_APPROVED",
  "execution": {"publish": false, "delete": false, "redirect": false, "outreach": false, "schedule": false},
  "baseline_metrics": {"search_clicks": null, "orders": null, "revenue": null},
  "causality_claimed": false
}
```

**Review handoff.** Give the approver the existing owner/inventory decision, scoped baseline, captured results and product sources, exact title/content/link or old-to-new URL proposal, source revision, named reviewer, acceptance checks and rollback. Keep separate `KEEP | UPDATE_EXISTING | SPLIT_REVIEW | HOLD` decisions in the existing findings. `SPLIT_REVIEW` is not page-creation approval; missing evidence remains HOLD. Research does not authorize publication, deletion, redirects, canonical edits, external outreach, spend or schedules.

**First-party guardrails checked 18 October 2026:** [Google title guidance](https://developers.google.com/search/docs/appearance/title-link), [redirect guidance](https://developers.google.com/search/docs/crawling-indexing/301-redirects), and [link-spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam). These explain implementation and policy limits; they do not verify the creator's case or promise rankings. Recheck living guidance before shipping.

**Related.** [[competitor-research]], [[keyword-fundamentals]], [[seo-metrics]], [[match-and-exceed]], [[finding-and-validating-niches]], [[keyword-to-sitemap]]. Course refs: 02-14 (research for existing businesses), 02-15 (finding keywords in top pages), 02-16 (content gaps), 02-17 (also ranks for).
