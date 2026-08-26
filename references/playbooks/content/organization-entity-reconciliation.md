---
title: Organization Entity Reconciliation — Safe `sameAs` and Canonical Identity
area: content
source_lessons: []
operational_addition: true
source: "https://x.com/tarasshyn/status/2091954190067363888"
verified_against:
  - "https://developers.google.com/search/docs/appearance/structured-data/organization"
  - "https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data"
  - "https://schema.org/sameAs"
verification_date: 2026-08-26
---

# Organization Entity Reconciliation — Safe `sameAs` and Canonical Identity

## What it is

A read-first method for giving crawlers one consistent identity record for an organization, local business, person, product, or other entity. It uses a stable canonical entity node, truthful structured data, and a small verified set of `sameAs` URLs that **unambiguously identify the same entity**.

The social label **“entity stacking”** is not a Google feature or a ranking guarantee. Google states that Organization structured data on a home or organization page can help it understand and disambiguate an organization. Google also states that it may make general use of `sameAs`. Schema.org defines `sameAs` as a reference page that unambiguously indicates the item's identity. These facts support identity reconciliation. They do not prove ranking lift, a Knowledge Panel, AI citations, or that a long list beats other SEO work.

## When to use

- Organization, LocalBusiness, Person, ProfilePage, Product, SoftwareApplication, or WebSite markup has missing, stale, conflicting, or duplicated identity data.
- A brand has real public profiles but its site does not connect them to one canonical entity node.
- A directory/profile campaign produced URLs that now need a truth and identity audit.
- A site migration, rename, acquisition, or social-handle change created inconsistent names, URLs, logos, addresses, or descriptions.
- A creator claims that adding many profile links to `sameAs` will replace backlinks or directory work; use this method to test the underlying identity mechanism without adopting the claim.

## Governing rules

1. **One subject per node.** Every `sameAs` URL must identify the exact entity represented by that schema node. A Product Hunt product page is not automatically the same thing as its publisher Organization. A GitHub repository is not automatically the same thing as a company profile.
2. **Identity, not mention.** A news article, review, affiliate page, listicle mention, customer page, or unrelated high-authority profile is not `sameAs` merely because it mentions the entity.
3. **Truth before volume.** Prefer fewer complete and accurate properties over a long, weak, stale, or contradictory list. Google explicitly recommends fewer complete and accurate properties over badly formed or inaccurate data.
4. **No bulk profile creation.** Existing verified profiles may become candidates. Creating or claiming profiles remains a separate external write under the directory/platform workflow and requires exact approval.
5. **No authority claim.** `sameAs` does not turn a profile into a followed backlink, transfer a domain metric, prove indexation, guarantee a Knowledge Panel, or replace relevant editorial links and useful listings.
6. **Use the right entity type.** Put organization profiles on the Organization/LocalBusiness node, personal profiles on the Person node, and true product identity pages on the Product/SoftwareApplication node.
7. **Keep visible facts aligned.** Names, URLs, logos, addresses, contact details, founder relationships, and product descriptions must agree with the site's visible content and project truth source.

## Evidence ledger

Copy `assets/organization-entity-identity-audit.csv` into the project workspace. Record every candidate before editing markup.

Required checks:

- `candidate_url` returns a public page and resolves to its canonical URL;
- the page identifies the exact subject, not merely a mention or associated asset;
- entity type is compatible with the schema node;
- name, URL, logo, location, and description do not materially conflict;
- the profile is current, not abandoned, merged, impersonated, or superseded;
- public access, indexability, ownership/claim status, and evidence date are recorded separately;
- `include_in_sameas` is an explicit review decision with a reason.

A page can identify the entity without being controlled by it; Wikidata and Wikipedia are common examples. Record control separately from identity. A page can also be public yet unsuitable because it identifies a product, repository, review object, or category rather than the Organization node.

## Method

### 1. Freeze the canonical identity

For each schema node, record:

- canonical name and alternate name, if real;
- canonical URL;
- stable `@id` using a URL fragment such as `https://example.com/#organization`;
- most specific truthful type;
- logo/image, description, contact and address facts where applicable;
- parent, founder, brand, product, or person relationships as separate nodes instead of collapsing them into `sameAs`.

Reuse the same `@id` wherever the entity is referenced. Do not create competing Organization nodes with different facts on every template.

### 2. Build the candidate set

Collect existing URLs from:

- official social/company profiles;
- authoritative identity records such as Wikidata or Wikipedia, when they truly identify the entity;
- verified company, product, review, marketplace, launch, developer, or directory profiles;
- prior markup, footers, contact/about pages, knowledge panels, and project truth files.

Treat creator screenshots and bulk lists as discovery sources only. Do not copy their URLs into production markup without row-level verification.

### 3. Classify each URL

Use one decision:

- `INCLUDE` — exact subject, compatible entity type, current and fact-consistent;
- `REPAIR_THEN_INCLUDE` — exact subject but stale or conflicting; the external repair needs separate approval;
- `RELATION_ONLY` — related page, product, founder, repository, review object, or mention that needs another property/node or no markup;
- `REJECT` — ambiguous, unrelated, private, impersonated, spammy, obsolete, or misleading;
- `BLOCKED` — identity cannot be established from current evidence.

Do not let public indexability or a high domain metric override a subject mismatch.

### 4. Implement one coherent graph

Place Organization markup on the home page or one page that describes the organization, such as the About page, following current Google guidance. Use JSON-LD unless the stack has a sound reason not to.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Example Company",
  "url": "https://example.com/",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/example-company",
    "https://github.com/example-company"
  ]
}
```

The example shows shape, not mandatory platforms. Include only evidence-approved URLs. Model products, founders, brands, and local locations as their own nodes when needed, connected with the appropriate Schema.org properties.

### 5. Validate before release

- Parse the JSON-LD and validate expected value types.
- Run Google's Rich Results Test where applicable.
- Inspect rendered HTML and confirm the canonical node appears once with stable facts.
- Confirm each `sameAs` URL still resolves to the reviewed identity page.
- Use URL Inspection after deployment to confirm Google can access the page.
- Save the exact before/after markup, approval, deploy receipt, and verification date.

A clean validator result proves syntax and supported-property shape. It does not prove ranking impact, identity acceptance, a Knowledge Panel, or rich-result display.

## Measurement

Measure the implementation as an identity-data quality change:

- duplicate/conflicting entity nodes removed;
- approved candidate coverage and rejected mismatches;
- structured-data validity and crawl/render availability;
- branded-result/profile consistency over time;
- observed Knowledge Panel or Search appearance changes, labelled as observations;
- ordinary Search, referral, conversion, and named answer-provider outcomes kept separate.

Use a dated baseline and follow-up. Do not claim causality from a branded-result change without controlled evidence. Do not use engagement on the source post as proof that the tactic works.

## Stop conditions

Stop and escalate instead of shipping when:

- the same URL appears to identify a different entity type;
- a profile has conflicting legal name, location, ownership, or product facts;
- the candidate is private, login-only, removed, impersonated, or no longer canonical;
- inclusion would require creating, editing, or claiming an external profile without approval;
- the only reason to include a URL is domain authority, backlink hope, or a creator's list;
- multiple templates emit competing canonical entity nodes.

## Related

- `references/playbooks/content/schema-types-reference.md`
- `references/playbooks/content/eeat-framework.md`
- `references/playbooks/authority/directory-submissions.md`
- `workflows/site-audit.md`
- `workflows/technical-seo-maintenance.md`
