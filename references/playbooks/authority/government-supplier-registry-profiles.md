---
title: Government supplier registry profiles
goal: Screen legitimate supplier registries without turning procurement declarations into a backlink hack.
source_status: Creator tactic fact-checked against registry-owner guidance on 2026-08-22.
---

# Government supplier registry profiles

Use this playbook when a source claims that SAM.gov, SBA Small Business Search, a state vendor portal, the UK Central Digital Platform, or another public procurement registry will provide a government-domain backlink.

The useful mechanism is narrow: a genuine supplier may gain a public entity record through normal procurement activity, and that record may contain its website. Registration is **not** an SEO entitlement. A government-domain page, a supplier identifier, or a creator screenshot does not prove that a public, indexable, followed website link exists.

## Claim split

Keep three evidence lanes separate:

1. **Creator claim** — what the post says the registry provides.
2. **Registry-owner fact** — official purpose, eligibility, declarations, privacy, and publication rules.
3. **Observed link outcome** — one current public profile, its indexability, rendered destination `href`, `rel`, and live status.

Do not promote a candidate from a creator claim directly to `APPROVED` or `LIVE`.

## Non-negotiable gates

### 1. Genuine procurement purpose

The entity must have a real reason to participate in the registry's procurement system. Do not register only to create a backlink, obtain a government-domain URL, or manufacture an entity signal.

Record:

- the goods or services the entity could truthfully supply;
- the target agency, buyer, framework, tender class, or supplier programme;
- the named business owner for the procurement route; and
- the expected procurement outcome independent of SEO.

No real procurement use case means `REJECT_NO_PROCUREMENT_INTENT`.

### 2. Jurisdiction and entity eligibility

Verify eligibility from the registry owner before preparing a registration. Check legal name, entity identifier, registered address, operating jurisdiction, business type, size rules, required classifications, and any foreign-entity requirements.

Never invent or infer:

- small-business status;
- US operating presence or economic contribution;
- ownership, control, affiliate, veteran, women-owned, disadvantaged, or location status;
- financial, tax, banking, exclusion, connected-person, insurance, trade-assurance, or qualification answers; or
- an intention to bid for awards.

An agent may organise owner-supplied facts and draft neutral descriptions. An authorised human must review every representation and declaration.

### 3. Public-link proof

Before treating a registry as a backlink candidate, inspect both official publication rules and one current public profile created through the same route.

Verify:

- the profile is publicly accessible without an account or share code;
- search engines may index the page;
- a website field is displayed publicly;
- the rendered link points to the intended canonical destination;
- the rendered `rel` value is recorded rather than assumed;
- the profile is durable enough to recheck; and
- the listing is available to this entity for a legitimate reason.

A supplier ID, private supplier-information record, downloadable bid pack, award-system account, or buyer-only search result is not a public backlink.

### 4. Human attestation and exact-write approval

Account creation, identity checks, two-factor authentication, tax or banking data, certifications, exclusions, connected-person data, declarations, and form submission stay with an authorised human.

The agent may prepare a field map and draft. It must not submit until the user approves the exact registry, entity, purpose, factual packet, and declarations. A broad request for “.gov backlinks” does not authorise false statements or a backlink-only procurement registration.

## Registry-specific fact checks

### United States: SAM.gov and SBA Small Business Search

- Official SAM.gov guidance says full entity registration is for organisations that want to bid on government contracts or apply for federal assistance.
- Requesting a Unique Entity ID without full registration is a different path. It does not by itself prove a public SBA profile or website backlink.
- SBA guidance says a qualifying small business generally must be physically located and operate in the US or its territories. A foreign business may qualify only when it has a US operation that makes a significant US economic contribution under the applicable rules.
- Small-business status depends on NAICS, receipts, employees, affiliates, and other facts. Misrepresentation can carry severe penalties.
- SBA Small Business Search has public profiles, but verify a current profile's website field and rendered link before counting an outcome.

Verdict rule: do not use SAM.gov or SBA Small Business Search as a generic backlink route for a foreign or ineligible entity. Do not complete full SAM registration without a real federal-award use case.

### United Kingdom: Central Digital Platform / Find a Tender

- The Central Digital Platform lets suppliers register, obtain an identifier, store core supplier information, and share it for procurements.
- Official publication guidance says stored supplier information is available only to contracting authorities chosen by the supplier; it **cannot be freely accessed**.
- A supplier identifier becomes public when a procurement notice containing that supplier is published. Registration alone does not create a public backlink.
- Supplier setup can require connected-person, qualification, trade-assurance, exclusion, and financial information plus a declaration.

Verdict rule: registration may have procurement value for a bid-ready supplier, but do not count it as a backlink unless a later public notice or profile displays and links the website.

### State, local, and other national portals

Do not generalise from SAM.gov. For each portal, verify:

1. official ownership and current registration route;
2. eligible supplier classes and geography;
3. whether the record is public or buyer-only;
4. whether the website field is public;
5. actual indexability and rendered link behaviour; and
6. the declarations and maintenance duties created by registration.

Many procurement systems are private workspaces. Others publish only tenders, awards, or notices after real procurement activity. Treat each as a separate route.

## Workflow

### Phase 0 — define the entity and destination

Resolve the exact legal entity, canonical website, target page, operating countries, supplied services, and real procurement purpose. If any are unknown, stop before account work.

Copy `assets/government-supplier-registry-opportunities.csv` into the project's `outreach/` folder. Keep one row per registry and entity pair.

### Phase 1 — preserve source lineage

Record the creator source, date observed, exact claim, and any promoted service. Mark the row `UNVERIFIED_SOURCE_LEAD`. A high domain rating, `.gov` suffix, “free,” “autopilot,” or AI-ranking claim is not outcome evidence.

### Phase 2 — verify the registry owner

Read the current official registration, eligibility, privacy/publication, and declaration pages. Record official URLs and dated excerpts. Classify the route:

- `PUBLIC_SUPPLIER_PROFILE_CANDIDATE`
- `PROCUREMENT_ONLY_PRIVATE_RECORD`
- `PUBLIC_ONLY_AFTER_NOTICE_OR_AWARD`
- `IDENTIFIER_ONLY`
- `INELIGIBLE`
- `UNKNOWN_NEEDS_REVIEW`

Reject SEO-only registrations and any route whose eligibility cannot be proven.

### Phase 3 — inspect a live public example

Find a current profile from the same route. Record HTTP status, login requirement, robots directive, canonical, website field, destination `href`, link `rel`, and observation date. Do not use search snippets as proof.

Only `PUBLIC_SUPPLIER_PROFILE_CANDIDATE` rows with verified eligibility and a real procurement purpose may move to `READY_FOR_OWNER_REVIEW`.

### Phase 4 — prepare, review, and submit

Prepare a field map from owner-supplied facts. Mark sensitive or declarative fields `HUMAN_ONLY`. Present:

- registry and purpose;
- entity and eligibility evidence;
- exact public-link evidence;
- required declarations;
- privacy and maintenance effects; and
- the expected procurement value even if no SEO value appears.

After exact approval, the authorised person completes authentication, attestations, and submission. Save a receipt without exposing confidential data.

### Phase 5 — verify the outcome

After approval or publication, inspect the actual public page. Record the live URL, rendered link, `rel`, indexability, referral tag or analytics path, and recheck date. Count a backlink only when the destination link exists on the public page.

Use these terminal verdicts:

- `LIVE_VERIFIED_LINK`
- `LIVE_NO_WEBSITE_LINK`
- `PRIVATE_OR_BUYER_ONLY`
- `PUBLIC_ONLY_AFTER_PROCUREMENT_EVENT`
- `REJECT_INELIGIBLE`
- `REJECT_NO_PROCUREMENT_INTENT`
- `EXPIRED_OR_REMOVED`

## Measurement

Track procurement and SEO outcomes separately.

**Procurement:** bid eligibility, notices, invitations, submitted bids, awards, and qualified buyer contacts.

**SEO:** public profile URL, rendered destination link, `rel`, index observations, referral sessions, assisted conversions, survival at 30/90 days, and brand/entity mentions.

Never report a government registration, supplier identifier, or private record as an acquired backlink.

## Stop conditions

Stop and mark the row with evidence when:

- there is no genuine procurement purpose;
- the entity does not meet geography or size rules;
- the route asks for facts the owner has not supplied;
- the supplier record is private, buyer-only, or share-code-only;
- no current public example shows a website link;
- the registration would create tax, banking, compliance, or renewal duties the owner has not accepted;
- a declaration would be misleading; or
- the only expected benefit is SEO.

## Source and official evidence

- Creator source: <https://x.com/floriandarroman/status/2090801830112759955>
- Quoted article: <https://x.com/borjafat/status/2090800950243958944>
- SAM.gov entity registration: <https://sam.gov/entity-registration>
- SBA contracting requirements: <https://www.sba.gov/counseling/get-started/#basic-requirements>
- SBA Small Business Search: <https://dsbs.sba.gov/>
- UK supplier registration guide: <https://www.gov.uk/government/publications/procurement-act-2023-short-guides/suppliers-how-to-register-your-organisation-and-first-administrator-on-find-a-tender-in-three-easy-steps-html>
- UK publication guidance: <https://www.gov.uk/government/publications/procurement-act-2023-guidance-documents-procure-phase/guidance-central-digital-platform-and-publication-of-information-html>

