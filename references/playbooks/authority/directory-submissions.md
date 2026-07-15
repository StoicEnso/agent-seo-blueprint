---
title: Directory & Entity Submissions
area: authority
source_lessons: []
operational_addition: true
---

# Directory & Entity Submissions

## Purpose

Use legitimate directories, product indexes, launch platforms, review profiles, and public entity profiles to improve discoverability and earn a small base of relevant links. Treat these as **entity-discovery and citation work**, not a shortcut to authority.

A directory link is worth pursuing only when the destination is relevant, public, indexable, accurate, and useful to a real visitor. Domain Rating screenshots are leads, not evidence.

## Hard rules

1. **Verify live before recommending or submitting.** Confirm the site resolves, accepts the business/product category, exposes a public listing, and has a working submission or claim route.
2. **Never promise a backlink, dofollow status, DR increase, or ranking lift.** Record observed link attributes after the listing is live.
3. **No fake identities, fake reviews, duplicate businesses, spun descriptions, or paid placement without approval.**
4. **Keep entity facts consistent.** Business name, URL, category, location, social handles, and product positioning must match the project truth source.
5. **Prefer relevance over headline DR.** A niche launch directory with real users can beat an unrelated high-DR account profile.
6. **Separate candidates from approved destinations.** Unknown or questionable routes stay in research until verified.
7. **Treat submission as an external write.** Prepare the package first; obtain explicit approval before publishing a listing or creating an account.
8. **Verify after submission.** Save the public URL, status, date, evidence, link attribute if observable, and follow-up date.

## Verification checklist

For every candidate, capture:

- canonical domain and submission/claim URL
- route type: directory, product index, launch platform, review profile, public entity profile, or editorial suggestion
- topical and geographic fit
- public listing example from another company
- indexability (`noindex`, robots, canonical, login wall)
- outbound-link behavior (`follow`, `nofollow`, `ugc`, redirect, JavaScript-only, or unknown)
- moderation/approval model and cost
- required assets and fields
- duplicate/listing-conflict check
- `last_verified_at` and evidence source

Reject the candidate when the only link is inside a private account, the listing is not indexable, the platform is unrelated to the project, or the route requires misrepresentation.

## Sourced candidate set — July 2026

These are discovery leads from a public X checklist. **No DR values are preserved because they are unverified and mutable.** Five were already present in the maintained directory catalog; twelve are newly recorded candidates.

| Destination | Route type | Catalog status | What to verify before use |
|---|---|---|---|
| Buy Me a Coffee | Public creator/business profile | Existing | Public profile, category fit, outbound-link behavior |
| GitHub | Repository / GitHub Pages | Existing | A real open-source or docs use case; do not create thin repos for links |
| G2 | Software review profile | Existing | Product eligibility, claim route, review-policy compliance |
| Uneed | Product directory / launch | Existing | Current submission route, moderation, public listing |
| What Launched Today | Launch directory | Existing | Current submission route, category fit, public listing |
| ProvenExpert | Review/profile platform | New candidate | Business eligibility, public indexability, no review manipulation |
| Aural++ (`auralplusplus.com`) | AI-tool claim/listing | New candidate | Domain identity, ownership claim flow, moderation, public link |
| Reclaim.ai | Account/profile candidate | New candidate — likely reject unless public | Confirm a public indexable profile exists; private account links do not count |
| Grokipedia | Editorial/topic suggestion | New candidate — editorial only | Editorial policy, notability, conflict-of-interest disclosure, no self-authored promotion |
| Modal | Account/profile candidate | New candidate — likely reject unless public | Confirm a public indexable profile exists and the project genuinely uses Modal |
| Dodo Payments Index (`index.dodopayments.com`) | Product index | New candidate | Eligibility, submission route, public listing, category fit |
| BetterLaunch (`betterlaunch.co`) | Launch directory | New candidate | Current submission flow, badge terms, public listing |
| CtrlAlt (`ctrlalt.cc`) | Startup/product showcase | New candidate | Current submission flow, moderation, public listing |
| DomainAIo (`domainaio.com`) | Backlink/launch platform | New candidate | Platform legitimacy, public listing, fees, link behavior |
| Needle (`useneedle.net`) | Directory | New candidate | Live domain, free-listing claim, public indexability |
| ABackLaunch (`abacklaunch.com`) | Startup launch directory | New candidate | Live submission route, moderation, public listing |
| Nick Launches (`nicklaunches.com`) | Product launch directory | New candidate | Live submission route, moderation, public listing |

## Priority model

Score verified destinations from 0–3 on each factor:

- topical fit
- audience usefulness
- entity/citation value
- public indexability
- likelihood of acceptance
- maintenance burden (reverse score)

Do not use third-party DR as the primary sort. Prioritize destinations with a real audience and clean entity fit.

## Submission package

Prepare once, then adapt per platform:

- canonical business/product name
- one-line description (50–80 characters)
- short description (150–300 characters)
- long description (500–1,000 characters)
- canonical URL with sensible UTM only when allowed
- category and tags
- logo, square icon, screenshots, and social proof
- founder/company details that are already public and approved
- consistent social/profile links
- approved CTA and product claims

Never paste identical long descriptions everywhere. Preserve the same facts while adapting wording to each audience.

## Tracker schema

Use `assets/directory-submission-tracker.csv` or equivalent fields:

`destination,domain,route_type,fit,status,submission_url,public_listing_url,cost,link_attribute,indexable,last_verified_at,submitted_at,approved_at,follow_up_at,evidence,notes`

Recommended statuses:

`candidate -> verified -> approved -> submitted -> live | rejected | expired`

## Reporting

Report verified outcomes, not submission volume:

- approved live listings and their public URLs
- rejected candidates with reason
- pending moderation/follow-up dates
- entity consistency issues fixed
- referral traffic or assisted conversions when available

A batch of 20 unverified submissions is not success. Three accurate, relevant, public listings can be.
