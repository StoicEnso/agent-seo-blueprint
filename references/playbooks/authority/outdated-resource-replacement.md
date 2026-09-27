---
title: outdated-resource-replacement
area: authority
source: https://x.com/hridoyreh/status/2102694375390347463
---

# Outdated-resource replacement (on-demand subskill)

Use this **inside** `workflows/authority-and-links.md` when a user asks to find stale, broken or misleading editorial resource links. Do not use it for directories, Wikipedia edits, generic link swaps, or paid placements; those have separate owners. This is a bounded *research and draft* method, not a backlink-acquisition guarantee.

The source post reports 13+ high-quality backlinks and displays a redacted Search Console card with 14 external links from 13 sites. The hidden domains, baseline and attribution cannot be checked. Do not treat that claim as proof of the tactic or expected results.

## Inputs and destination gate

- Identify the exact page to offer, its current live URL, locale, reader job and first-party feature evidence. Verify the page opens to the intended content. Record what it *does not* do. A photo-to-yard visualizer is not automatically a plant-ID app, 2D CAD planner, seasonal planting calendar or generic AI-art generator.
- If no relevant, working and genuinely useful destination exists, stop. Do not pitch a weak near-match just to earn a link. Never invent a testimonial, conversion, accuracy, price or ranking claim.
- Sources may be live SERP/manual editorial search or an authenticated backlink index. No DataForSEO or Ahrefs login means no proprietary referring-domain, traffic, DR or dofollow assertion. Preflight any paid bulk pull.

## Five-candidate pilot

1. Choose at most five **link instances** from current editorial pages, not a screenshot or a search snippet. Capture the source URL, exact anchor/context, old target URL, existing outbound-link `href`/`rel`, and retrieval date. One page can have multiple candidates, but report distinct domains and the resulting concentration.
2. Recheck the old target's HTTP status, redirect chain, final URL, and actual reader job. A 200 parking page, 404, unrelated destination, or reproducible DNS failure can justify a correction. A 403/402, CAPTCHA, bot block, timeout, transient maintenance notice or old publication date alone does **not** prove the link is obsolete. For DNS, test both `www` and bare domain; for redirects, read the final content. Mark uncertain items `HOLD_RECHECK`.
3. Grade each candidate as `REPLACEMENT_REVIEW` (unusable/off-topic source link **and** our resource meets the same reader job), `ADDITIONAL_RESOURCE_REVIEW` (active source link, but a distinct missing option serves the audience), `HOLD_RECHECK` (uncertain or temporary fault), or `REJECT_NO_FIT` (our page cannot support the original link's reader job/claim). Editorial quality and source independence matter more than volume. Do not describe an additional-resource suggestion as broken-link building.
4. For each candidate, record `{referring_url, anchor, old_target_url, old_status, final_url, observed_at_utc, reader_job, replacement_url, fit_evidence, limitation, disposition, confidence, next_check}` in the existing `outreach/<date>_opportunities.json`. A five-row intake does not mean five qualified pitches. Keep a `REJECT_NO_FIT` row as a negative control when found.
5. At most two high-fit candidates may receive brief, individualized `DRAFT` messages. Offer the editor a factual correction and show why the proposed page helps their readers. Do not send email, post a comment, submit a form, pay for placement, request exact-match anchor text, or imply an editor agreed. An external send needs owner approval for the exact batch. Follow existing `linkbuilding-what-not-to-do.md` and `manual-outreach.md`.
6. Recheck immediately before any approved outreach. If an editor voluntarily changes the page, verify the live `href`, `rel`, indexability and context, then measure referral sessions/business outcomes separately. Neither a live link nor a provider rank score proves traffic or ranking lift.

## Landscapio pilot notes (27 Sep 2026)

The public page `https://www.landscapioai.com/` returned 200 and offers photo-to-yard ideas. Its pricing, cost-accuracy and testimonial claims were not independently verified. Public spot checks, not DataForSEO or Search Console, produced five **potential** link instances: WPS→Sketch Garden (www DNS failure; bare domain redirects to drawing-art site), Country Living→GardenManager (parking/for-sale redirect), MorningDough→Gemoo landscape page (404 with maintenance notice, `HOLD_RECHECK`), MorningDough→Fotor generic image generator (active, possible distinct photo-to-yard addition), MorningDough→Live3D landscape-art generator (active, possible distinct addition). The first two still require exact job fit and editorial review; none are earned backlinks. Country Living→Dr. A’s app is a rejected negative control: the app link is 404, but plant advice is not a yard-photo design job.

For source URLs and observed targets, see `examples/landscapio-outdated-resource-prospects.md`. Repeat the live checks before claiming the five are current.
