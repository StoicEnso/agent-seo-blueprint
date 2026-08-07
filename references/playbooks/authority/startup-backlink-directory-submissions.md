---
title: Startup Backlink Directory/Profile Candidate Intake
area: authority
operational_addition: true
---

# Startup Backlink Directory/Profile Candidate Intake

Use this as the startup-specific discovery layer in front of `directory-submissions.md`. It turns crowd-sourced lists into a verification queue; it does not endorse every row or authorize submission.

## Source asset

`assets/directory-discovery-sources.csv` records the discovery sources and dated source-level observations. `assets/startup-backlink-candidates.csv` preserves candidate-level provenance and mutable source claims. Its original intake contains 127 source mentions normalized to 122 candidate names; source-reported DR is historical, explicitly unverified input—not current fact.

Directory Finder is registered as a structured discovery source because it exposes niche filters and third-party claims for DR, traffic, pricing, approval time, link type, and direct submission routes. As observed on 2026-08-07, its public sitemap exposed 68 listing pages. Do not bulk-promote those rows: filter by project fit first, then verify each selected destination on its own site.

## Source audit before candidate verification

1. Record `source_name`, `source_url`, source type, coverage, claimed fields, and observation date in the source registry.
2. For each selected source entry, preserve `source_entry_url` and only map mutable claims into `source_claimed_*_unverified` fields.
3. Normalize the destination name/domain and deduplicate across sources without discarding provenance.
4. Reject obvious category mismatches before live verification; broad directories-of-directories are not project shortlists.
5. Check that the source exposes enough provenance to revisit the entry. A screenshot, copied DR table, or anonymous list with no destination route is a weaker lead.
6. Do not crawl or import an entire changing source merely to inflate the queue. Start with the niche/region/product filters that match the project.

## Verification pipeline

1. Resolve the current domain and confirm it is the same entity named by the source.
2. Open the destination's own submit/claim page and record `submission_url_verified_at`; never treat an aggregator's direct link as current by default.
3. Classify the route: directory, product index, launch platform, review profile, public entity profile, community, marketplace, editorial/PR, or asset contribution.
4. Verify eligibility, topical fit, moderation/cost, truthful account requirements, a public listing example, indexability, and observed outbound-link behavior using destination-owned pages and live listings.
5. Compare direct evidence with each `source_claimed_*_unverified` value and log discrepancies.
6. Reject private-only profiles, fake-persona routes, irrelevant listings, thin repositories, review manipulation, pay-to-link packages, and surfaces whose only value is a claimed authority metric.
7. Score relevance, real audience usefulness, evidence quality, effort, risk, and likely durable visibility—not DR alone.
8. Draft platform-specific copy and hold it for explicit approval under `directory-submissions.md`.

Community/editorial surfaces such as Hacker News, Indie Hackers, YourStory, Medium, or Wikipedia are not ordinary directory submissions. They require genuine contribution, editorial merit, or the owning authority workflow.

## State model

`UNVERIFIED_SOURCE_LEAD -> VERIFIED -> APPROVED -> SUBMITTED -> LIVE | REJECTED | EXPIRED`

Every state change needs dated evidence. Creating accounts, posting, submitting, commenting, or editing an external site requires explicit user confirmation.

## Done condition

The selected candidate batch is source-audited, deduplicated, classified, and live-verified with first-party route evidence, discrepancy notes, and rejection reasons. No row is called a backlink win until a public listing URL and observed link/indexability evidence exist.
