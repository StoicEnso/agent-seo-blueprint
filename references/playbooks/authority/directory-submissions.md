---
title: Directory & Entity Submissions
area: authority
source_lessons: []
operational_addition: true
source: "https://x.com/hridoyreh/status/2079831605863178416"
additional_discovery_source: "https://directoryfinder.com/"
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

## Discovery-source intake

Directory aggregators and crowd-sourced lists are useful queue builders, not evidence that a destination is suitable or that their metrics are current. Record the source in `assets/directory-discovery-sources.csv`, then preserve candidate-level provenance in `assets/startup-backlink-candidates.csv` or the project tracker.

For every imported claim:

- record the source name, source entry URL, and `source_observed_at` date;
- store DR, traffic, price, approval time, and link-type claims only in fields ending `_unverified`;
- deduplicate on the destination's canonical domain while retaining every source that mentioned it;
- filter by the project's niche, geography, business type, and eligibility before spending time on verification;
- never rank the queue by source-claimed DR alone; and
- re-open the destination's own submission/claim route rather than trusting an aggregator's direct link.

As observed on 2026-08-07, Directory Finder exposed 68 listing pages through its public sitemap and offered filters/claims for niche, DR, estimated traffic, price, approval time, link type, and submission route. Those fields are useful discovery metadata, but they remain third-party, mutable claims until checked against destination-owned pages and live public listings. The dated source record lives in `assets/directory-discovery-sources.csv`. Only 19 relevant, non-duplicate candidates were added to the research queue; local, travel, health, awards, jobs, crypto, generic-web, and other poor-fit entries were excluded at intake. This is not an endorsement of all 68 destinations.

## Conditional local-entity baseline

A 2026-08-09 social checklist named 35 business profiles, general directories, maps, and content/community platforms as a universal “backlink starter pack.” The list is retained as a discovery source, not imported wholesale. A physical or service-area business may have a legitimate local-entity lane, but an online-only startup should not manufacture a location or create irrelevant profiles for links.

| Surface | Dated first-party observation | Decision before use |
|---|---|---|
| Google Business Profile | Google's eligibility guidance says the business must have a customer-facing physical location or travel to customers: `https://support.google.com/business/answer/3038177` | Use only for a truthful eligible local/service-area business; one accurate profile, real-world name, precise address/service area, and minimal accurate categories. |
| Bing Places / Bing for Business | `https://www.bingplaces.com/` redirected to `https://www.bing.com/forbusiness/` on 2026-08-09 | Treat the renamed/redirected surface as mutable. Re-open the live claim flow, confirm country and business eligibility, and inspect a public result before recommendation. |
| Apple Business | Apple's current business product exposes Maps, Brands, actions, and discovery/insight features at `https://business.apple.com/` | Confirm current country, organization, verification, and place/brand requirements. Record the actual public Apple Maps/brand output rather than assuming a backlink. |
| Yelp for Business | `https://business.yelp.com/` offered a free page claim/add route and described local-business discovery on 2026-08-09 | Confirm category/geographic fit, an existing-page conflict, public indexability, and current link behavior. Never solicit or fabricate reviews. |
| OpenStreetMap | `https://www.openstreetmap.org/fixthemap` documents factual map repair/community editing | Not a marketing directory or backlink tactic. Add or correct only verifiable real-world map data under OpenStreetMap's norms; never insert promotional text or fictitious locations. |

Other names from the checklist—such as BBB, Nextdoor, Foursquare, Yellow Pages, Manta, Hotfrog, Chamber of Commerce, MapQuest, Alignable, MerchantCircle, Brownbook, Cylex, EZlocal, ShowMeLocal, CitySquares, Superpages, and Yellowbook—remain research leads until destination-owned eligibility, claim route, geography, moderation/cost, public output, and link behavior are live-verified. Their presence in a social list is not enough to add them to a project plan.

Crunchbase, About.me, Medium, Substack, Pinterest, YouTube, Vimeo, GitHub, Product Hunt, Reddit, and Quora are not interchangeable directory submissions. Route them to the appropriate company-profile, launch, audience, community, developer, or native-content workflow only when the project has a genuine use case. Do not create thin repositories, empty profiles, duplicate posts, or self-promotional community contributions for a backlink.

## First-party verification gate

Promotion from `UNVERIFIED_SOURCE_LEAD` to `VERIFIED` requires destination-first evidence:

1. **Identity and eligibility:** the destination's own site states that this business/product type may apply or claim a listing.
2. **Submission route:** the current submit/claim URL is destination-owned or an explicitly documented provider route. Save the URL and verification date.
3. **Cost and moderation:** use current destination pricing/terms and submission guidance, not an aggregator badge or old screenshot.
4. **Public output:** inspect at least one public listing on the destination for indexability, canonical behavior, login walls, and listing quality.
5. **Link behavior:** observe the actual rendered link on a comparable live listing. Do not infer `follow`/`nofollow` from a discovery source.
6. **Evidence split:** keep third-party claims in `source_claimed_*_unverified`; store current observations in `cost`, `link_attribute`, `indexable`, `submission_url_verified_at`, `last_verified_at`, and `evidence`.

If the destination's evidence conflicts with the discovery source, the destination wins and the discrepancy is recorded. If no destination-owned route or public listing can be verified, keep the row unverified or reject it.

## Verification checklist

For every candidate, capture:

- canonical domain and submission/claim URL
- destination-owned evidence for the submission/claim route
- route type: directory, product index, launch platform, review profile, public entity profile, or editorial suggestion
- topical and geographic fit
- public listing example from another company
- indexability (`noindex`, robots, canonical, login wall)
- outbound-link behavior (`follow`, `nofollow`, `ugc`, redirect, JavaScript-only, or unknown)
- moderation/approval model and cost
- source-claim versus first-party-evidence discrepancies
- required assets and fields
- duplicate/listing-conflict check
- `last_verified_at` and evidence source

Reject the candidate when the only link is inside a private account, the listing is not indexable, the platform is unrelated to the project, or the route requires misrepresentation.

## Sourced candidate set — July 2026

These are discovery leads from a public X checklist. **No DR values are preserved in this curated table because they are unverified and mutable.** Five were already present in the maintained directory catalog; twelve are newly recorded candidates.

The broader source intake is stored in `assets/startup-backlink-candidates.csv`: 146 source mentions normalized to 141 unique candidate names after the 19-row Directory Finder fit screen, with source lineage and mention counts preserved. The asset is deliberately a research queue, not an approved directory list. Its `source_claimed_dr_unverified` values are source-reported snapshots only; never sort or recommend on them without current verification. Promote a row into the submission tracker only after completing the verification checklist below.

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

For a paid directory, make a placement decision rather than a backlink decision. Require evidence of a relevant audience, plausible referral or assisted-conversion value, transparent pricing, durable public exposure, and owner approval. A `dofollow` claim does not justify payment; a `nofollow` link does not automatically make a genuinely useful listing worthless.

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

Use `assets/directory-submission-tracker.csv` or equivalent fields. Keep discovery lineage and destination-verified observations separate:

`destination,domain,route_type,fit,status,discovery_source,source_entry_url,source_observed_at,source_claimed_dr_unverified,source_claimed_traffic_unverified,source_claimed_cost_unverified,source_claimed_approval_time_unverified,source_claimed_link_attribute_unverified,submission_url,submission_url_verified_at,public_listing_url,cost,link_attribute,indexable,last_verified_at,submitted_at,approved_at,follow_up_at,evidence,notes`

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
