# Skill improvement audit — content opportunity audit and measurement

**Date:** 2026-08-24
**Target:** `references/playbooks/maintenance/content-opportunity-audit-and-measurement.md`
**Source type:** First-party implementation case study shared by a third party.

## Source

- Ian Nuttall share: <https://x.com/iannuttall/status/2091882414083596320>
- Quoted case study by harsehaj: <https://x.com/harsehaj/status/2091690736211112005>
- Saved full text: `vault/knowledge-base/articles/2026-08-24-how-i-built-an-seo-aeo-blog-engine.md`

The article reports 18 generated posts, 50+ edits, a 5.8× increase in impressions, a 9.8× increase in page-one queries, and average position movement from 10.9 to 6.6. These are creator-reported results from one implementation. They are not independently controlled or transferable benchmarks.

## Accepted mechanisms

1. Join current CMS, GSC, analytics, visibility, and prior-run data into one bounded audit.
2. Rank candidate pages by separate real-loss, CTR-headroom, and rank-headroom signals.
3. Run cheap checks across the inventory and expensive verification only on a capped priority set plus a rotating buffer.
4. Keep agent judgement read/draft-only. Put publication in a separate deterministic executor that revalidates the approved diff.
5. Gate new drafts on strategy, structure, provenance, and cannibalization, with no more than two revision attempts.
6. Capture exact before evidence plus same-period site evidence when a change goes live, then read final data at +28 and +56 days.
7. Keep AI crawl, citation, and referral lanes separate from ordinary Search and business outcomes.

## Rejected or narrowed

- **“10× page-one posts.”** Kept only as the source sharer's headline. Not adopted as an expected result.
- **Generic CTR curve as truth.** Narrowed to a property/scoped curve where possible. A generic curve is a labelled queue-ordering fallback only.
- **Estimated headroom as recoverable clicks.** Rejected. Headroom orders review and does not forecast rankings, traffic, conversions, or revenue.
- **Automatic publication of missing metadata or known dead-link replacements.** Rejected for this skill. Every website write remains explicitly approval-gated.
- **Creator-reported before/after metrics as causal proof.** Rejected. The playbook requires page-level and same-period site evidence and records confounders.

## Repository additions proposed

- Add `references/playbooks/maintenance/content-opportunity-audit-and-measurement.md`.
- Add `assets/content-opportunity-ledger.json`.
- Route recurring content-opportunity work from `SKILL.md` and the monitoring/content-production workflows.
- Add documentation tests for approval separation, estimate labels, stale-revision rejection, cannibalization, and 28/56-day measurement.
- Mirror the same transcript-free files into both `agent-seo-blueprint-full` and `agent-seo-blueprint`; do not include the saved X article in either repository.
