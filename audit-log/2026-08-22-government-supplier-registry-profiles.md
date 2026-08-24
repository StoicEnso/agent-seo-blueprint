# Skill improvement audit — government supplier registry profiles

**Date:** 2026-08-22  
**Target:** `references/playbooks/authority/government-supplier-registry-profiles.md`  
**Pre-declared validation gate:** the complete repository test suite must pass; a new documentation test must prove the claim split, jurisdiction and procurement-intent gates, human attestation boundary, public-link verification fields, and source-specific corrections.

## Evidence batch

| Source | Observation | Evidence grade |
|---|---|---|
| Florian Darroman X post quoting Borja's article | Claims that an agent can obtain free `.gov` backlinks “on autopilot” through SAM.gov, SBA Small Business Search, state vendor portals, and equivalent non-US registries. | Creator tactic; discovery lead only |
| SAM.gov entity-registration guidance | Full registration is for entities that want to bid for federal awards or apply for federal assistance. A Unique Entity ID-only request is a separate path. | First-party registry-owner evidence |
| SBA contracting requirements | Small-business status depends on size, affiliates, NAICS, location/US economic contribution, and other facts. The page warns of severe penalties for knowing misrepresentation. | First-party eligibility evidence |
| UK Central Digital Platform publication guidance | Stored supplier information is not freely accessible. A supplier identifier becomes public when a procurement notice naming the supplier is published. | First-party publication evidence |
| Public SBA Small Business Search examples | Public supplier pages exist, but a current route-specific page must be inspected for its website field, rendered `href`, `rel`, and indexability before counting a link. | Direct public-profile evidence; outcome still entity-specific |

## Accepted edits

1. Added government supplier registries as a separately screened authority source class.
2. Preserved the useful mechanism: discover legitimate public supplier profiles and verify the actual public website link.
3. Added a jurisdiction, entity, procurement-purpose, declaration, privacy, and public-link proof gate.
4. Added a registry opportunity ledger that separates source claims, official rules, submission state, and live link evidence.
5. Kept agent work to research, field mapping, drafting, and post-publication verification. Authentication, attestations, sensitive data, and submission stay human-reviewed and exact-approval-gated.

## Rejected or narrowed

- **“.gov backlinks on autopilot.”** Rejected. Procurement registration creates legal and factual representations and may not create a public page.
- **“Anyone can register on SAM.gov for the listing.”** Narrowed. Official guidance ties full registration to federal awards or assistance; a UEI-only request is different.
- **“Tick small business and enter the public SBA search.”** Narrowed. Eligibility is fact-dependent and cannot be self-declared for SEO.
- **“The UK government supplier registry gives a backlink.”** Rejected for registration alone. Official guidance says stored supplier information cannot be freely accessed.
- **“A `.gov` domain is an AI-ranking signal.”** Retained only as a creator hypothesis. No ranking, citation, traffic, or conversion outcome is promised.

## Validation

Run the whole Python test suite, `git diff --check`, and the new government-registry documentation test in both repositories. The local installed skill update must use the Skill Workshop path and pass the skill-catalogue simulation.

## Execution decision

Do not create accounts from the creator article alone. First identify one legal entity with real procurement intent, verify jurisdictional eligibility, and prove that the exact route can produce a public website link. If official guidance says the supplier data is private or public only after a notice or award, classify the route as procurement-only and do not count a backlink.

