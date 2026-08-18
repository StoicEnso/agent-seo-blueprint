# Skill improvement audit — press-release value path

**Date:** 2026-08-17  
**Target:** `references/playbooks/authority/press-release-distribution.md`  
**Pre-declared validation gate:** the existing documentation test suite must pass, plus the new test must prove that the source claim, cost/value routes, map-specific route, registry states, and approval boundary are present.

## Evidence batch

| Source | Observation | Evidence grade |
|---|---|---|
| Chris — Local SEO X post and silent 26.5-second video | Claims around 300 placements/backlinks/referring domains, map pickup links, and beating 90% of competitors. Vendor, package, live examples, and measurement were absent. | Unverified creator claim |
| PR Underground pricing | Basic: $74.99 for one release. Page claims 300+ sites, one-business-day publication, and a PDF placement report. | First-party offer; live delivery/value not yet verified |
| EIN Presswire pricing | Basic: $149. Page lists an embedded Google My Business listing and three keyword-anchor links. | First-party offer; live pickup/map preservation not yet verified |
| PRLog comparison | Free hosted option; paid $29/$49/$99 options with vendor syndication-count claims. | First-party offer; live delivery/value not yet verified |
| IssueWire pricing | $21 single-release/first-free wording, but inconsistent comparison cards and no jointly observable selected checkout terms. | First-party evidence conflict; checkout verification required |
| eReleases pricing | $399 Buzz Builder and PR Newswire/journalist-distribution positioning. | First-party offer |
| Press Advantage pricing | $349/month, two releases, vendor placement/backlink/map claims. | First-party offer; marketing claims unverified |

## Accepted edits

1. Added Chris's source as a supporting source and decomposed its 300-site argument into testable claims.
2. Added a goal-based price path: free rehearsal, low-cost broad-syndication test, map-specific test, editorial reach, and deferred recurring service.
3. Added seven explicit registry rows and states. Vendor price/outlet claims remain observations, not SEO outcome claims.
4. Updated the skill router and guardrail text so a request for a cheap/value press-release route loads the price path before any checkout or submission.
5. Added a documentation test that guards the claim split, price recommendations, registry states, and map requirement.

## Rejected or deferred

- **“300 placements means 300 referring domains/backlinks”** — rejected. It needs live-domain, canonical, robots, and link-attribute evidence.
- **“A map embed means every pickup links to the Google Business Profile”** — deferred pending exact checkout confirmation and a comparable live-pickup sample.
- **IssueWire as the cheapest recommendation** — deferred because its page rendered contradictory comparison-card values; checkout verification is required.
- **Subscription/bulk purchase** — deferred. One measured release must prove value before scaling.

## Validation

- New unit assertion added before validation.
- Run the whole repository test suite, standard repository verifier scripts when available, `git diff --check`, and OpenClaw skill simulation after the candidate edits.

## Next batch

Before any paid test: choose a specific real news event, create the owned evidence page, re-check the exact package and refund/correction terms, inspect a fresh comparable pickup, then seek approval for the exact draft, destination, cost, assets, and links.
