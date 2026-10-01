---
title: Local AI First-Party Evidence
area: maintenance
operational_addition: true
verified_at: 2026-10-01
sources:
  - https://x.com/alexgroberman/status/2105289457335427525
  - https://www.brightlocal.com/research/local-ai-visibility-study/
  - https://www.brightlocal.com/resources/ai-directory-sources/
---

# Local AI First-Party Evidence

## What it is and when to use it

A read-only supplement for a real local business: audit whether its owned website supplies truthful facts that match local customer tasks, then compare saved observations across named search surfaces. Use `workflows/site-audit.md` for site gaps, `workflows/content-production.md` for justified draft briefs, and `workflows/monitoring.md` for repeat measurement. Retain the existing cross-platform citation and local-profile safeguards. This is not a new universal GEO score or a replacement for local SEO.

First verify applicability. A global SaaS product, a publisher, or a marketplace is not automatically a local service business because it has a registered address. For a marketplace, separate the platform from eligible providers. Do not invent branches, offices, service areas, licensing, reviews, or customer-facing prices.

## Source screening and denominators

Alex Groberman's post mixes BrightLocal findings with promotion of SEO Stuff packages and RightCited. Those sales links, DR50+ placement claims, prices, and free-audit pitches are not independently validated integration recommendations.

BrightLocal's September 16 study reports roughly 93% of unique cited domains were business sites, while business sites supplied 42% of citation instances. Unique-domain share is not citation-volume share, business mention rate, impressions, clicks, leads, or revenue. A cited business-site domain may belong to a competitor; the 93% figure does not mean the queried business's website is always cited. Observational source use does not prove adding pages causes recommendations.

The detailed methodology states 200,875 non-branded prompts, 1,342 locations, about three reports per location, nine grid points, and 60 days. The introduction instead says 200,085 searches and about 1,300 locations. Preserve the discrepancy and section locator; do not silently choose a reconciled total. The examined surfaces are ChatGPT, Google AI Mode, and Google AI Overviews. Do not extend the evidence to Claude, Perplexity, Grok, SaaS, or every country.

The August 26 source-analysis page describes US, UK, and Australia and has separate counts: 60,970 checks, 1,355 methodology locations, and 1,967,762 citations. Its text also gives other location counts and Google/Yelp shares that differ from its table. Do not merge this panel with September's prompt denominator or resolve its internal conflicts without evidence. Label quoted percentages with URL, date, section, metric, denominator, and limitation. Use rounded ranges or attributed section-specific values when necessary.

## Procedure

1. **Establish truth.** Record actual business identity, services, area model, opening/availability facts, who it serves, contact path, and price/range only when appropriate and supported. For every fact retain its source URL or private owner-approved evidence locator, status (`verified`, `missing`, `conflicting`, `not_applicable`), and a draft-only action. Private evidence is not public-share permission.
2. **Inspect owned pages.** Check rendered/crawlable text, correct canonical/indexability where relevant, navigation, and useful service/problem/price/decision answers. Map each need to an existing URL before proposing another page. Check internal links and competing page intent. Prefer updating a real useful page to mass-producing city/service permutations. Reject doorway pages, duplicated location text, fake addresses, and unsupported schema. This study does not require special AI markup.
3. **Keep the ecosystem.** Audit accurate Business Profile facts, genuine reviews, relevant industry/general directories, and legitimate local sources. First-party and third-party evidence are complementary, not substitutes. Do not discard relevant listings based on the 93% figure or buy contextual followed links from the post's pitch.
4. **Build a small panel.** Choose 3–5 verified customer tasks, not a content quota. Keep exact prompt, panel version, provider, surface, declared location context, locale, account state, UTC timestamp, and evidence locator. Use real or explicitly supplied research geography; do not spoof location or bypass challenges. Unsupported surfaces remain explicitly outside this v1 validator.
5. **Repeat modestly.** When authorized access exists, save at least three attempts over more than one day before drawing a directional conclusion. Three is a pilot heuristic, not a study requirement or statistical power guarantee. Vary geography only in separately labelled groups. No paid tracker signup, external API batch, or scheduler change follows from this playbook alone.
6. **Record actual outcomes.** Distinguish `returned`, `no_answer`, and `unavailable`. A completed no-answer attempt belongs in the completed denominator; inaccessible or failed retrieval does not prove absence. Record named businesses separately from cited URLs. A mention is not a citation and neither is a click. Google Maps, AI Overviews, AI Mode, and ChatGPT require separate datasets.
7. **Draft only the useful gap.** Prioritize factual errors and existing-page clarity. Require distinct intent, real operations, source support, maintainability, and a user benefit before proposing a new local page. Website, profile, directory, review, outreach, purchase, and publication writes retain their approval gates.
8. **Recheck after approved changes.** Use the same declared panel and context with a fixed 4–8 week read when feasible. Track ordinary Search, Maps observations, named answer surfaces, referrals, leads, conversions, and revenue separately. Record other site changes, seasonality, availability, campaigns, competitors, and platform changes. Before/after association is not causal proof.

## Offline ledger

Copy `assets/local-ai-evidence-ledger.json`. It is an empty template, not real research. Run:

`python3 scripts/local_ai_evidence_check.py <ledger.json>`

The validator only reads local JSON. It never logs into a provider, collects searches, edits a website, or sends messages. It validates context and source-statistic denominators and counts saved attempts by provider/surface/exact-prompt/location/locale/account/panel. It reports counts and insufficient-repeat warnings, not a visibility score, lift forecast, or statistical significance. It cannot authenticate captured evidence or prove a fact is true; a human must inspect the source.

## Done and stop conditions

Done means a truthful owned-page gap ledger, separately labelled source metrics and observations, a small repeat panel with limitations, draft-only recommendations, and no unauthorized writes. Stop the affected claim when facts conflict, access is unavailable, location context is unclear, or no distinctive local value exists. Mark unknown, retain evidence, and continue unaffected read-only work. Reject global promises, domain-share-to-traffic calculations, Maps-rank-to-AI conversions, mass city pages, and paid-placement guarantees.
