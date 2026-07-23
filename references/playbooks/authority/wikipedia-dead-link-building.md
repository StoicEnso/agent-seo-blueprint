---
title: Wikipedia Dead-Link Replacement
area: authority
operational_addition: true
tools: [serp, browser, wayback]
---

# Wikipedia Dead-Link Replacement

A quality-first broken-link workflow for finding dead citations on niche-relevant Wikipedia pages, reconstructing what the missing source supported, and planning a materially better replacement resource. The default deliverable is research and a replacement-content brief—not a live Wikipedia edit.

## Discovery loop

1. Build 5–20 tight terms from the site's genuine expertise.
2. Search `site:wikipedia.org <keyword> "dead link"` and browse relevant dead-link maintenance categories.
3. Capture the article, section, surrounding claim, cited URL, and the dead-link marker.
4. Confirm the URL is genuinely dead rather than temporarily unavailable; record dated checks.
5. Recover the strongest archived version with the Wayback Machine or another reputable archive.
6. Determine the exact claim the citation supported and whether the target site can publish an original, neutral, current resource that supports it better.
7. Rank candidates. Default to ten verified opportunities or a documented exhausted search space.

## Required record

```json
{
  "wikipedia_url": "https://en.wikipedia.org/wiki/...",
  "article_title": "...",
  "section": "...",
  "citation_context": "...",
  "dead_url": "https://...",
  "dead_status": "confirmed_dead|intermittent|not_dead",
  "dead_status_evidence": [],
  "archive_url": "https://web.archive.org/web/...",
  "archive_summary": "...",
  "replacement_content_type": "guide|dataset|study|calculator|reference|other",
  "replacement_concept": "...",
  "required_primary_sources": [],
  "target_site_fit": "...",
  "commerciality_risk": "low|medium|high",
  "coi_status": "owner|client|none|unknown",
  "edit_eligibility": "research_only|talk_page_request|independent_editor_review|direct_edit_possible",
  "priority": 0,
  "next_action": "...",
  "status": "VERIFIED|REJECTED|NEEDS_REVIEW"
}
```

## Quality and conflict-of-interest gate

A replacement must be original and materially better: current facts, clear authorship, cited primary sources, stable URL, neutral presentation, and no aggressive conversion layer. Reject copied text, fabricated research, thin commercial pages, unrelated sources, or claims the source cannot support.

Do not publish the resource, edit Wikipedia, post on a talk page, contact editors, or submit any external change without explicit confirmation. Record owner/client conflicts and prefer transparent edit requests or independent-editor review. Never coordinate deceptive accounts or edit wars, and never promise that a citation will remain, pass ranking authority, or create referral traffic.

## Output

Write `outreach/<date>_wikipedia_dead_links.json`. A research run is complete at ten verified niche-relevant opportunities or an evidence-backed exhausted-search report.
