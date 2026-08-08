---
title: Cloudflare Agent Readiness and AEO Evidence
area: maintenance
operational_addition: true
source_scope: Cloudflare product announcement dated 2026-08-06; product access, model coverage, metrics, and pricing may change
official_source: https://blog.cloudflare.com/aeo/
field_lead: https://x.com/glenngabe/status/2085703866385928685
---

# Cloudflare Agent Readiness and AEO Evidence

Use this when a site is on Cloudflare and the owner wants a dated view of whether agents can access the site, which AI operators crawl or refer traffic, and how Cloudflare's synthetic category panel observes brand mentions and citations. Treat the dashboard as three separate evidence lanes, not one universal “AEO score.”

As of the official 2026-08-06 announcement, **Agent Readiness** is available in the Cloudflare dashboard and **AEO Visibility** requires requesting early access. The announcement does not establish a price, so do not describe either product as free without a current first-party pricing or account entitlement check.

## What the three lanes measure

### 1. Agent Readiness diagnostics

Cloudflare scans a hostname and reports vendor-defined `pass | fail | neutral` checks with request/response evidence. The announcement groups checks into:

- quick wins such as readable `robots.txt`, XML sitemaps, scoped AI-crawler rules, and optional machine-readable Markdown;
- technical groundwork such as Content Signals, API catalogs, link headers, and agent-login instructions;
- advanced integrations such as OAuth discovery, MCP/A2A cards, skills indexes, Web Bot Auth, and WebMCP;
- informational commerce standards, which the announcement says are not counted in the score.

This is an **agent-usability diagnostic**, not evidence that Google or another answer engine requires every check, and not a ranking or citation formula. Validate each recommendation against the site's actual product, security posture, crawler policy, and the named provider's current official documentation before changing anything.

### 2. AEO Visibility synthetic category panel

Cloudflare infers an industry/category and tests category-level prompts without naming the brand. At announcement time it probed Anthropic Claude and OpenAI GPT, repeated prompts across models, and reused a precomputed category snapshot across accounts. Reported metrics include:

- **Citation Rate** — share of tested answers that cite the site;
- **Prominence** — where citations appear and how much answer substance is attributed to them;
- **Mention Rate** — share of tested answers that name the brand, cited or not;
- **Share of Voice** — the site's share of citations versus observed competitors;
- **Industry Fit** — a vendor-defined score based on which brands appear together in the panel corpus.

These are observations from Cloudflare's sampled prompt panel. They are not actual user-query logs, Search Console impressions, click counts, market share, conversions, or proof that one change caused a later score movement. Record the inferred category, model/provider coverage, snapshot date, locale if exposed, and product version/access state with every capture.

### 3. AI Operator Activity first-party network evidence

Cloudflare separately reports real crawl and referral activity that passes through its network, grouped by operator, including request errors such as `403` and `404`. Keep this first-party traffic/error lane separate from the synthetic AEO panel.

- Crawl volume does not prove citation, recommendation, training use, or human visibility.
- Referral traffic does not prove that a particular prompt or answer caused a visit.
- An operator name may aggregate multiple crawlers or surfaces; preserve Cloudflare's label and the capture date.
- Reconcile referrals with analytics and server-side conversion evidence before making revenue claims.

## Procedure

### 1. Confirm applicability and access

Record the hostname, Cloudflare zone/account, dashboard access state, date, and whether AEO Visibility is available, waitlisted, or absent. Do not infer zero visibility from unavailable beta access.

### 2. Capture each lane independently

For Agent Readiness, record every material check with status, exact evidence, owner policy, and proposed action. For AEO Visibility, record category/model/snapshot metadata plus the reported metrics and cited domains/URLs when exposed. For AI Operator Activity, record crawl counts, referrals, error classes, and date range by operator.

Suggested artifact: `monitoring/<date>_cloudflare-agent-aeo.json`.

```json
{
  "captured_at": "YYYY-MM-DD",
  "source": "cloudflare_dashboard",
  "hostname": "example.com",
  "access": {
    "agent_readiness": "available|unavailable|not_checked",
    "aeo_visibility": "available|early_access_requested|unavailable|not_checked"
  },
  "agent_readiness": {
    "vendor_verdict": "...",
    "checks": [
      {"name": "...", "status": "pass|fail|neutral", "evidence": "...", "action": "..."}
    ]
  },
  "aeo_panel": {
    "snapshot_date": "YYYY-MM-DD",
    "industry": "...",
    "category": "...",
    "providers_models": ["..."],
    "metrics": {
      "citation_rate": null,
      "prominence": null,
      "mention_rate": null,
      "share_of_voice": null,
      "industry_fit": null
    },
    "cited_sources": []
  },
  "operator_activity": {
    "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
    "operators": [
      {"name": "...", "crawls": null, "referrals": null, "errors_403": null, "errors_404": null}
    ]
  },
  "limitations": [
    "aeo_is_a_precomputed_synthetic_category_panel",
    "operator_activity_is_separate_first_party_network_evidence",
    "no_user_query_impressions_or_causal_attribution"
  ]
}
```

### 3. Diagnose before acting

Route evidence by failure class:

- access or response errors → `workflows/technical-seo-maintenance.md`;
- missing or weak buyer-answer content → `workflows/content-production.md`;
- entity or authentic corroboration gaps → `workflows/authority-and-links.md`;
- provider-specific mention/citation investigation → `workflows/geo-audit.md`;
- measurable referral/conversion analysis → `workflows/monitoring.md` with analytics.

Do not blindly enable crawler access, Markdown, authentication metadata, APIs, agent protocols, or payment standards. Crawler-policy, security, authentication, and production changes require the owner's explicit approval and their own verification plan.

### 4. Compare like with like

Retest only after recording the original panel snapshot, category, provider/model coverage, and product state. If those changed, label the run non-comparable. Report score movement as a dated association, not causality. Keep Cloudflare AEO, Cloudflare operator activity, ordinary GSC, Google AI reports, GA4, and other providers' direct citation observations in separate datasets.

## Done when

Access state is explicit; all available lanes are captured independently; vendor scores retain their names and limitations; the AEO panel is labelled synthetic and snapshot-based; operator activity is labelled first-party network evidence; pricing is not asserted without current proof; every proposed action maps to observed evidence and an owner; and no access or production setting is changed without approval.

## Sources

- Cloudflare, “From ranking to recommended: get your site ready to thrive in the age of AI agents,” published 2026-08-06: https://blog.cloudflare.com/aeo/
- Glenn Gabe discovery post, published 2026-08-07: https://x.com/glenngabe/status/2085703866385928685
