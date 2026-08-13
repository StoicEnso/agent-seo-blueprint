---
title: AI Search Commerce and Agentic Readiness
area: maintenance
operational_addition: true
source_scope: Microsoft AEO/GEO guidance used as directional evidence, not a universal platform formula
---

# AI Search Commerce and Agentic Readiness

Use with `workflows/geo-audit.md` when a product, retailer, marketplace, or service depends on current structured facts and an actionable conversion path. This extends citability checks into freshness and transaction readiness without implying that every answer engine consumes the same inputs.

## Three data planes

Audit each separately and compare them for contradictions:

1. **Crawled pages** — canonical pages, initial HTML/rendered state, visible copy, internal links, policies, and schema.
2. **Feeds/APIs** — Merchant Center, product/catalog feeds, public APIs, partner feeds, inventory endpoints, or other structured sources actually used by the business/platform.
3. **Live site state** — current product detail, variant selection, stock, price, currency, promotion, shipping, locale, and checkout/contact path.

Absence of a feed/API is not automatically a defect. It is a gap only when the business or target platform needs that surface.

## Cross-surface consistency fields

For applicable products/entities, compare identifiers/SKUs, names, variants, price, currency, availability, language/locale, images, canonical URL, seller/brand, shipping, promotions, update timestamps, and policy terms. Record the source of truth and freshness owner. Never let schema or feeds advertise facts users cannot see or buy on the live site.

## Agentic conversion checks

- Can a user or agent reach the correct product/service from the observed answer or landing page?
- Are variants, stock, price, promotion, shipping, cancellation/returns, and geographic eligibility current and understandable?
- Does the final checkout, booking, lead, or support path work without hidden contradictions?
- Are consequential actions protected by normal user confirmation, authentication, payment, and policy controls?

## Agent-native product surface

Assess an API, app connector, Model Context Protocol (MCP) server, feed, or other agent-facing interface only when it lets a real user complete a useful product job. It is a product and retention surface, not a citation hack.

For an applicable interface verify:

- the supported user job and target agent/client;
- truthful capability descriptions, current schemas, stable identifiers, and useful error messages;
- least-privilege authentication and explicit user consent;
- a preview or confirmation boundary before purchase, publishing, account creation, data deletion, or another consequential action;
- observability for successful and failed task completion without exposing private user data;
- current documentation, ownership, support path, and deprecation behavior;
- product analytics that separate connector usage, retained users, acquisition, and revenue.

Run a controlled task-completion test. Record whether the client discovered the interface through an official catalogue, an explicit user connection, or another known path. Merely publishing an MCP server or connector does not prove that a provider will recommend it or acquire users for it. Existing-user task completion and new-user acquisition are separate outcomes.

Reject any hidden text or machine-readable instruction that offers a model a reward, pressures immediate signup, disguises advertising, overrides the user's intent, or tries to bias tool selection. Do not place prompt injection or model-directed “bribes” in schema, metadata, package files, documentation, or responses.

## Intent and trust content

Priority pages should provide extractable comparisons, real use cases, buyer questions, tradeoffs, current specs/pricing where applicable, primary-source support, clear authorship/methodology, and first-party evidence. Do not create artificial “AI chunks”; make sections understandable because that helps users.

## Measurement and claim quality

Keep evidence layers separate:

- platform visibility/mention/citation observation;
- landing-page sessions and referrals where measurable;
- leads, assisted conversions, transactions, and revenue;
- controlled causal evidence, if any.

A visibility screenshot cannot substantiate a revenue claim. Correlation, temporal sequence, attribution-model output, and controlled causality are different evidence grades and must be labelled honestly.
