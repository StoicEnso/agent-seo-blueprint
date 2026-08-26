# Skill improvement audit — Organization `sameAs` entity reconciliation

**Date:** 2026-08-26  
**Target:** `references/playbooks/content/organization-entity-reconciliation.md`  
**Source type:** Creator tactic shared as a social post and code screenshot; qualified against current first-party documentation.

## Source

- Taras post: <https://x.com/tarasshyn/status/2091954190067363888>
- Credited source in the post: <https://x.com/Charles_SEO>
- Google Organization structured data: <https://developers.google.com/search/docs/appearance/structured-data/organization>
- Google structured data introduction: <https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data>
- Schema.org `sameAs`: <https://schema.org/sameAs>

The post says that putting social, company, product, review, developer, knowledge-base, and directory profile URLs into Organization `sameAs` helps Google understand the entity better than “300 junk directory listings.” The screenshot includes social profiles, GitHub, Wikidata, Crunchbase, F6S, E27, npm, StackShare, Product Hunt, There's An AI For That, SaaSHub, G2, Capterra, GetApp, Software Advice, Trustpilot, AlternativeTo, and WebCatalog.

The source post is a discovery lead. Its engagement and screenshot do not prove ranking impact, Knowledge Panel eligibility, AI citations, backlink value, or that every listed URL identifies the same Organization node.

## First-party findings

1. Google says Organization markup on the home page can help it understand administrative details and disambiguate the organization.
2. Google's Organization example includes `sameAs` profile URLs.
3. Google says it may make general use of `sameAs` and recommends fewer complete and accurate properties over inaccurate data.
4. Schema.org defines `sameAs` as a reference page that unambiguously indicates the item's identity.
5. Neither source says that a long `sameAs` list is a ranking factor, that it replaces relevant directory/editorial work, or that any page mentioning a brand is eligible.

## Accepted mechanism

- Build one canonical identity node with a stable `@id` and consistent facts.
- Treat profile lists as candidates, not production markup.
- Verify each candidate against the exact schema subject and entity type.
- Separate identity match, public access, indexability, control, and authority/referral value.
- Route related products, founders, repositories, reviews, and mentions to separate nodes/properties or exclude them.
- Validate the rendered graph and keep external profile creation/repair behind separate approval.

## Rejected or narrowed

- **“Entity stacking” as a Google feature.** Rejected as terminology. The playbook uses entity reconciliation and identity graph.
- **A long list is better.** Rejected. Accuracy and unambiguous identity are the gate.
- **Better than 300 directory listings.** Kept only as creator framing. No comparative evidence was supplied.
- **All screenshot URLs belong on Organization `sameAs`.** Rejected. Product, repository, review, marketplace, and company pages can represent different subjects.
- **Ranking, Knowledge Panel, backlink, or AI-citation benefit.** Rejected as a guarantee. Any observed change must stay labelled and provider/outcome lanes remain separate.
- **Create profiles to fill the array.** Rejected. Profile/account writes stay under their own approved platform workflow.

## Repository additions

- Add `references/playbooks/content/organization-entity-reconciliation.md`.
- Add `assets/organization-entity-identity-audit.csv`.
- Route Organization/entity audits from the skill router, site audit, technical maintenance, schema reference, and E-E-A-T review.
- Add documentation tests for exact-subject matching, entity-type separation, external-write approval, and no ranking/Knowledge Panel claims.
- Mirror the same transcript-free files into both repositories; do not copy the source screenshot into either repository.
