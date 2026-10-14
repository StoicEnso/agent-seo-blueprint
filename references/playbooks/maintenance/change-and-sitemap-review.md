---
title: Change-Driven Product Copy and Competitor Sitemap Review
area: maintenance
operational_addition: true
source_status: Original bounded adaptation of two public workflow mechanisms, 14 October 2026.
---

# Change-driven product copy and competitor sitemap review

## What it is
Two cheap triggers for a useful review queue: a product source file changed, or a competitor's sitemap listing changed. Neither trigger is an instruction to publish. The job is to find specific, evidence-backed work without repeatedly auditing everything.

## When to use
Use after a product release, when prices/limits/features may have changed, or when watching a small set of relevant competitors. Do not use it to manufacture daily output, infer hidden rankings, copy competitors or sell sponsored links. Select a user-approved cadence; a quiet run can correctly finish with no new work.

## Method
1. Maintain a versioned, non-sensitive source-to-page map. Give each claim a stable ID, exact product source paths, owned page, current claim and evidence URLs where available. The helper fingerprints the map. No wildcard matching or model-inferred fact is treated as an exact mapping.
2. Compare two pinned commits from the actual repository root. Require the earlier commit to be an ancestor. Keep rename/delete evidence and unmapped changes. Do not treat uncommitted edits, a branch name alone or an unverified deployment as live product facts.
3. Inspect the source and actual product before flagging an owned statement as wrong. Draft the smallest correction. A release/content brief needs a verified shipped feature and an actual buyer benefit. Keep code maintenance distinct from a launch.
4. Preserve saved UTF-8 sitemap XML with acquisition evidence. The helper records a SHA-256 fingerprint, source URL, observation time and completeness. It does not resolve domains, fetch pages, crawl indexes or call rank APIs.
5. Compare only compatible, complete observations. Preserve URL spelling, trailing slashes and query strings; this deliberately avoids pretending different URLs are the same. Missing baseline or incomplete/index coverage suppresses the entire comparison. Source switches require a new baseline.
6. Verify any interesting competitor page, actual search demand, unique reader value and existing owned-page coverage. A new sitemap entry may be old, unindexed or commercially irrelevant. A missing entry does not prove deletion. `lastmod` is supplied metadata, not proof the content changed.
7. Route justified candidates through the current technical/content/monitoring workflows. Retain exact-diff approval, product truth, intent, provenance, cannibalization, rollback/live receipt and comparable 28/56-day outcome checks. Drafts do not authorize external publication, email or directory writes.

## Decision criteria
- **Product source changed, owned claim still true:** `NO_ACTION`.
- **Changed source has no mapping:** `NEEDS_MAPPING`, not an invented affected page.
- **Feature appears in a commit but shipment is unknown:** `NEEDS_LIVE_PROOF`.
- **Owned statement contradicts verified live product:** `COPY_CORRECTION_DRAFT`.
- **Verified user-facing release with useful evidence:** `RELEASE_BRIEF_DRAFT`.
- **New competitor listing with independent demand and no existing owned coverage:** a normal content brief candidate.
- **Partial/error/index observation or unverifiable competitor claim:** explicit unknown/coverage note, never false removals or a ranking claim.

## Example
A recorded commit changes `src/product/limits.ts`; claim `starter-export-limit` maps it to `/pricing`. That triggers a review of the real live plan limit and pricing text. The tool does not claim the limit changed or edit the page. Separately, a complete competitor URL-set snapshot lists `/guides/exporting` for the first time. Inspect that page and search intent before proposing anything; its age and rankings remain unknown.

## Limits and pitfalls
- The scripts accept saved input, use the Python standard library, and write only the nominated report. They make no network/model calls. Git reads are capped and timed, with no shell/hooks/external diff/text conversion. They emit no diff bodies or binary content.
- Secret/private path components, `_source`, dependency trees and credential files are excluded from product metadata. The cap counts all observed paths before exclusions. Mapping private paths is rejected. Do not put sensitive statements or credentials in a claim map.
- XML and JSON inputs are capped at 5 MB; sitemap entries at 50,000. UTF-16/32, DTD/entities, corrupt schema, duplicate URLs, local/IP-literal hosts, userinfo, fragments, nonstandard ports and unexpected host/source swaps are rejected. Supported source metadata does not itself prove a successful acquisition: verify the receipt.
- Large/index/cross-host/CDN sitemap coverage needs an explicit future collector design or an existing approved manual evidence route. Do not silently weaken checks or convert a partial view to a complete baseline.
- This is a candidate generator, not a semantic truth checker, deployment detector, keyword extractor or indexing test. Existing Google Search Console and analytics integrations supply independent outcome evidence.
- Failure leaves an existing output unchanged; callers must check the exit code and must not mistake an older output for a fresh run.

## Related
- [Operating runbook](../../../workflows/change-and-sitemap-review.md)
- [Content opportunity audit and measurement](content-opportunity-audit-and-measurement.md)
- [Technical SEO maintenance](technical-seo-maintenance.md)
- [Competitor research](../research/competitor-research.md)
- [Product-copy helper](../../../scripts/change_review.py)
- [Saved-sitemap helper](../../../scripts/sitemap_snapshot.py)

## Source lineage
- Public post: https://x.com/illyism/status/2110180038637408357
- Mechanism reference: https://github.com/Illyism/seo-skills/blob/af48ce5953e00ca75d1cd4d440e77d0c0d61a038/seo/seo-autopilot/SKILL.md
- Release-draft reference: https://github.com/Illyism/seo-skills/blob/af48ce5953e00ca75d1cd4d440e77d0c0d61a038/marketing/diff-marketing/SKILL.md

Only the code-change review and sitemap-observation mechanisms were adapted. No skill body, paid-course material, paid-service pitch, publishing quota, ranking promise, auto-merge rule or "do not write tests" instruction was adopted.
