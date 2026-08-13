---
title: Agent-Readable Web Delivery and Bot-Log Evidence
area: maintenance
operational_addition: true
source_scope: Current provider crawler documentation, standard HTTP behavior, the informal llms.txt proposal, and dated single-site field observations
official_sources:
  - https://developers.openai.com/api/docs/bots
  - https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Content_negotiation
proposal_source: https://llmstxt.org/
field_inputs:
  - https://x.com/zenorocha/status/2087547759083901252
  - https://x.com/marclou/status/2087872366898827510
---

# Agent-Readable Web Delivery and Bot-Log Evidence

Use this playbook when a site owner wants agents, search fetchers, or developer tools to retrieve accurate public content with less rendering or URL-discovery friction. This is a technical accessibility and product-usability lane. It is not a Google ranking requirement, a universal answer-engine optimization formula, or proof that a crawler request caused a citation, answer, training event, signup, or sale.

## Evidence model

Keep these lanes separate:

1. **Configuration evidence** — `robots.txt`, sitemap, canonical, HTTP status/headers, HTML source, Markdown alternatives, `llms.txt`, and authentication/access policy.
2. **Request evidence** — sanitized origin/CDN logs showing a dated request, requested path, response status, bytes, latency, cache result, and a claimed user agent.
3. **Provider-role evidence** — current first-party documentation that describes a crawler as search, model training, or user-triggered retrieval.
4. **Answer/citation evidence** — a dated observation from the named product surface.
5. **Business evidence** — referral, session, conversion, retention, and revenue data.

A request in a server log proves that a request reached that logging layer. It does not by itself prove successful parsing, indexing, training, recommendation, citation, or a human outcome. Client-side analytics can miss non-browser requests, while CDN logs can omit origin detail. Record the source and its limits instead of calling either source complete.

## 1. Scope the user job and provider

Record the exact content set and job: documentation lookup, pricing/policy retrieval, product comparison, public support answer, or another real task. Name the provider/client in scope. Do not apply a generic “AI bot” rule to all systems.

Check current official documentation before classifying a bot. OpenAI and Anthropic document separate roles for automatic search, model-development crawling, and user-triggered retrieval. These roles and identifiers can change.

Respect the owner's licensing, privacy, and crawler choices. Never enable search or training access silently. Report the tradeoff and require approval before any production policy change.

## 2. Verify ordinary web access first

For each priority URL, capture:

- HTTP status, redirects, canonical, content type, cache behavior, and response time;
- whether the main facts, links, identifiers, and error guidance are available in raw HTML or another documented representation;
- whether a JS-only widget hides content or actions from the scoped client;
- robots directives and sitemap/discovery state where relevant;
- authentication, rate-limit, and error behavior without completing a consequential action.

Do not demand that every interactive product become no-JavaScript. Preserve progressive enhancement where the task justifies it: stable links/forms, accessible names, truthful errors, and a server/API route for the important public or authorized job.

## 3. Test Markdown as an optional alternative

A clean Markdown representation can reduce navigation and rendering noise for documentation or dense reference material. It is optional. HTML remains a first-class web representation and may still be fetched.

When Markdown is justified:

- choose a stable explicit URL such as a documented `.md` alternative;
- return an accurate `Content-Type` such as `text/markdown; charset=utf-8`;
- expose the relationship from HTML with `Link: <...>; rel="alternate"; type="text/markdown"` or an equivalent HTML link;
- keep title, canonical identity, facts, links, dates, policies, and access controls in parity with HTML;
- prevent stale shadow content, duplicate ownership confusion, private-data leakage, and different claims for bots versus people;
- test a bounded question set against both HTML and Markdown.

Do not generate a Markdown copy of every page by default. Prioritize stable public documentation, policies, pricing facts, API references, help content, and other pages where the alternative serves a real retrieval job.

## 4. Use HTTP content negotiation carefully

`Accept`-based content negotiation is standard HTTP behavior, but it adds cache and validation complexity. Prefer explicit alternate URLs unless one URL with multiple representations materially improves the user job.

If the site serves Markdown for `Accept: text/markdown`:

- use `Vary: Accept` so shared caches do not serve the wrong representation;
- keep the HTML default for ordinary browser requests;
- test `Accept: text/html`, `Accept: text/markdown`, mixed quality values, wildcards, absent headers, and unsupported types;
- avoid user-agent sniffing as the representation switch;
- preserve canonical identity and representation parity;
- verify CDN, edge cache, application, and monitoring behavior.

A successful negotiation test proves delivery behavior, not a ranking or citation gain.

## 5. Treat `llms.txt` as a voluntary map

`llms.txt` is an informal proposal for a concise Markdown map to useful resources. It can help a known client or agent discover curated documentation. It does not replace `robots.txt`, XML sitemaps, navigation, canonicals, or ordinary crawlability.

If a project adopts it:

- keep it concise, current, public, and human-readable;
- link only to canonical, useful, permission-safe resources;
- include descriptions that distinguish the resources;
- test every URL, redirect, status, and representation;
- record which real client or workflow consumes it;
- assign an owner and freshness check.

Absence of `llms.txt` is not a Google defect. Do not claim that OpenAI, Anthropic, or another provider requires it, uses it for a specific purpose, or rewards it without current first-party evidence for that claim. A single site's request volume is local field evidence only.

## 6. Build a privacy-safe request ledger

When server or CDN logs are available, sample a bounded date range and preserve aggregate evidence such as:

- provider label and claimed user-agent string;
- verification state: `verified_provider_range | user_agent_only | not_verified`;
- provider role from current official documentation: `search | training | user_triggered | other | unknown`;
- normalized path or route class;
- status class, bytes, latency, cache result, and date bucket;
- robots result and relevant representation (`html | markdown | other`);
- observation source and retention window.

Verify published source IP ranges when a provider supplies them. A user-agent string can be spoofed, so never label it verified from text alone. If verification is not possible, preserve `user_agent_only` or `not_verified`.

Before saving or sharing evidence, remove or irreversibly hash personal identifiers as allowed by policy and strip secrets, cookies, authorization headers, request bodies, fragments, and sensitive query-string values. Prefer normalized paths and aggregate counts. Follow the site's privacy notice, retention policy, contractual duties, and applicable law.

Never join a user-triggered fetch to a named person or private prompt unless the owner has a lawful, disclosed, necessary measurement design. Do not fingerprint users or reconstruct prompts from URLs.

Suggested artifact: `monitoring/<date>_agent-request-evidence.json`.

```json
{
  "captured_at": "YYYY-MM-DD",
  "source": "origin|cdn|other",
  "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "privacy_transform": "normalized_paths_and_sensitive_fields_removed",
  "requests": [
    {
      "provider": "openai",
      "claimed_user_agent": "OAI-SearchBot",
      "identity_verification": "verified_provider_range|user_agent_only|not_verified",
      "documented_role": "search|training|user_triggered|other|unknown",
      "path_class": "/docs/*",
      "representation": "html|markdown|other",
      "requests": 0,
      "status_2xx": 0,
      "status_4xx": 0,
      "status_5xx": 0
    }
  ],
  "limitations": [
    "request_does_not_prove_parsing_indexing_training_citation_or_business_outcome"
  ]
}
```

## 7. Diagnose before proposing work

Map an observed failure to the smallest fix:

- `403` or robots mismatch → verify owner policy and provider role; ask before access changes;
- `404` or redirect loop → repair discovery/canonical routes;
- `406` or wrong cached representation → correct negotiation and `Vary` behavior;
- `5xx`, timeout, or oversized response → engineering/performance fix;
- missing facts in raw HTML and failed scoped rendering → rendering/progressive-enhancement fix;
- stale Markdown or `llms.txt` → parity/ownership fix or remove the stale alternative;
- healthy delivery but weak citation → route to content/evidence/entity diagnosis, not more technical files;
- healthy citation but no business result → inspect referrals, task completion, and conversion separately.

## Field-input limits

August 2026 X posts proposed `llms.txt`, Markdown alternatives, content negotiation, server-log review, and reducing JS-only dependence. A separate TrustMRR post reported more than one million requests and local path/format patterns. The public post and screenshot do not expose request definitions, deduplication, verified bot identities, raw methodology, outcome joins, or causal controls. Treat all supplied percentages, path rankings, “used to answer/index/train” labels, and request counts as dated single-site observations. Do not transfer them as benchmarks or provider-wide behavior.

## Done when

The provider and user job are explicit; ordinary HTML/access behavior is tested; any Markdown, negotiation, or `llms.txt` proposal has a real consumer and parity plan; request logs are privacy-safe and identity-bounded; search/training/user-triggered roles remain separate; findings map to observed failures; and no crawl, citation, ranking, training, traffic, or revenue claim exceeds the evidence.
