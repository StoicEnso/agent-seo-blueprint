# Google Generative AI Visibility: Measurement and Response

## Purpose

Use Google Search Console's **Generative AI performance report** to measure whether canonical pages receive impressions in Google AI Overviews and AI Mode, then route evidence-backed follow-up work. This is a Google-only visibility workflow; it does not measure ChatGPT, Claude, Perplexity, Grok, clicks, conversions, or revenue.

Official references (verify again at execution time because rollout and fields can change):

- Google AI optimization guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Generative AI performance report: https://support.google.com/webmasters/answer/16984139
- Search generative AI inclusion control: https://support.google.com/webmasters/answer/16908024
- Direct report: https://search.google.com/search-console/performance/search-analytics/ai

## Evidence contract

Record the property, retrieval date, report date range, dimension, filters, and whether the newest data is preliminary. Treat every export as a snapshot, not proof of causality.

The report currently provides **impressions only** for AI Overviews and AI Mode. Available dimensions are:

- canonical/final page URL;
- country;
- date (Pacific Time; day/week/month granularity);
- device (desktop/tablet/mobile).

Do not invent unavailable fields. In particular:

- do not calculate AI CTR without an AI-click denominator;
- do not report AI queries unless Google adds and documents that dimension;
- do not claim a row identifies AI Overview versus AI Mode separately unless the live report exposes a documented feature filter;
- do not combine this report with ordinary GSC clicks and call the ratio "AI CTR";
- do not infer leads, revenue, or platform causality from impressions.

Normal Search Console limitations apply: limited rollout, access only for eligible properties with sufficient impressions, a 1,000-row table limit, preliminary newest data, and chart/table discrepancies caused by property-versus-page aggregation.

## Collection workflow

1. Confirm the exact GSC property (Domain vs URL-prefix) and date range.
2. Open the direct report. If absent, record `not available` and distinguish rollout/access from `zero visibility`; do not score the site as failed.
3. Export or capture four views: pages, countries, dates, and devices.
4. Preserve chart total separately from table rows because aggregation can differ.
5. Save a raw snapshot with this minimum shape:

```json
{
  "site": "sc-domain:example.com",
  "retrieved_at": "2026-07-23T18:00:00Z",
  "period": "2026-06-25..2026-07-22",
  "surface": "google_search_generative_ai",
  "included_features": ["AI Overviews", "AI Mode"],
  "metrics": {"impressions": 1234},
  "dimensions": {
    "pages": [{"key": "https://example.com/page", "impressions": 200}],
    "countries": [{"key": "GBR", "impressions": 500}],
    "devices": [{"key": "MOBILE", "impressions": 800}],
    "dates": [{"key": "2026-07-22", "impressions": 80}]
  },
  "limitations": ["impressions_only", "no_query_dimension", "limited_rollout"]
}
```

6. Compare like-for-like periods and the same property/dimension. Annotate control changes, migrations, indexation incidents, or major content launches.

## Inclusion-control check

Search Console has a separate **Search generative AI control**. Record whether the property is included, excluded, or inheriting from a parent. The default is inclusion, but verify the live property.

Keep these controls distinct:

- Search generative AI control: eligibility for links/content in Google's Search generative AI features.
- `Google-Extended`: model-training control; it is not the Search inclusion control.
- `noindex`: removes a page from Google Search entirely.

Changing inclusion is a consequential owner decision. Audit and recommend; do not toggle it without explicit approval.

## Buying-journey coverage matrix

Classify each AI-visible canonical page by its actual role:

| Journey role | Examples |
|---|---|
| Problem/education | definitions, diagnosis, guides |
| Use case/industry | audience- or workflow-specific pages |
| Product/service | capability and product-detail pages |
| Pricing | transparent pricing and plan explanations |
| Comparison/alternative | evidence-grounded comparison pages |
| Objection/trust | methodology, security, limitations, policies |
| Case study/proof | first-party evidence and documented outcomes |
| Implementation | setup, integration, process, support |

Report coverage as observed—not as a quota. A missing role becomes a content opportunity only when user demand, business value, non-duplication, and SERP evidence justify a useful page.

## Diagnostic matrix

- **Report unavailable** → record rollout/access ambiguity; continue with normal SEO and observed SERP/source checks.
- **Impressions rising** → identify which canonical pages/countries/devices gained; correlate separately with ordinary GSC, analytics referrals, leads, and revenue.
- **Impressions concentrated on a few informational pages** → inspect whether valuable product/pricing/proof pages are indexable, useful, internally linked, and supported by genuine evidence.
- **Impressions low across the site** → check index/snippet eligibility, crawlability, content quality, entity clarity, authority, and whether priority pages satisfy real questions.
- **Impressions high but site traffic weak** → do not call this an AI CTR problem. Assess whether pages offer a compelling reason to visit and use ordinary click/referral/conversion evidence separately.
- **Country/device gap** → verify localization, canonical/hreflang, mobile experience, and actual market demand before creating content.

## Official Google doctrine to preserve

Google says generative AI features are rooted in core Search ranking and quality systems and use retrieval/grounding plus query fan-out. Prioritize:

- indexed, snippet-eligible, crawlable pages;
- non-commodity, first-hand or expert content with inspectable evidence;
- clear technical structure and good page experience;
- useful images/video when they improve the page;
- accurate Merchant Center feeds and Google Business Profile data when applicable;
- authentic third-party corroboration.

Do **not** turn query fan-out into one thin page per phrase. Scaled pages made mainly to manipulate rankings or generative responses can violate spam policies.

## Myth-busting guardrails

For Google Search visibility, do not present any of these as requirements:

- `llms.txt` or other special AI text files;
- artificial content "chunking";
- rewriting solely for AI systems;
- special AI schema markup;
- manufactured mentions or paid authority placements.

`llms.txt` may still be a voluntary cross-platform documentation surface, and normal structured data may still support rich results. Label those separate purposes accurately; Google says neither is required for its generative AI Search features.

## Done when

A dated raw snapshot and short interpretation exist; report availability and limitations are explicit; inclusion-control state is recorded without changing it; page visibility is mapped to journey roles; every recommendation is tied to evidence; and Google-only data is not misrepresented as cross-platform AI visibility or business impact.
