---
title: AI Search Readiness Audit (GEO filename for compatibility)
goal: Assess platform-specific AI-search eligibility, usefulness, accessibility, corroboration, and measurement without presenting GEO heuristics as ranking formulas.
playbooks:
  - references/playbooks/foundations/seo-and-ai-future.md
  - references/playbooks/foundations/google-generative-ai-search-official.md
  - references/playbooks/content/eeat-framework.md
  - references/playbooks/content/on-page-optimization.md
  - references/playbooks/content/content-fundamentals.md
  - references/playbooks/authority/understanding-authority.md
  - references/playbooks/maintenance/ai-search-commerce-readiness.md
  - references/playbooks/maintenance/cloudflare-agent-readiness-and-aeo.md
  - references/playbooks/maintenance/cross-platform-ai-citation-loop.md
references:
  - references/playbooks/content/schema-types-reference.md
  - references/playbooks/maintenance/google-generative-ai-visibility.md
scripts:
  - scripts/workspace.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [serp, gsc]
outputs:
  - audits/<date>_geo-audit.md
  - audits/<date>_geo-findings.json
  - audits/<date>_cloudflare-agent-aeo.json # optional Cloudflare evidence, when available and in scope
  - audits/<date>_provider-citation-observations.json # optional non-Google citation baseline
---

# AI Search Readiness Audit

**When to run this.** Use when the user asks whether a site appears in ChatGPT, Perplexity, Claude, Google AI Overviews/AI Mode, or another named AI-search experience; asks why a brand is not cited; or wants current product/entity data and conversion paths assessed for agent use.

This is a read-only, evidence-led audit. It does not change robots controls, publish `llms.txt`, alter Search Console inclusion, submit feeds, or edit the site. Direct platform checks may require an account/browser. Report observations with retrieval dates; never turn them into universal ranking laws.

## Prerequisites

- Resolve the project workspace with `python3 scripts/workspace.py status --path <DIR>`. Ask before creating one if absent.
- Record the domain, priority pages, business goal, target topics/prompts, and market/country.
- Record **platform scope** before auditing. Allowed labels:
  - `google_ai_overviews`
  - `google_ai_mode`
  - `chatgpt`
  - `perplexity`
  - `claude`
  - `other:<name>`
- Load `google-generative-ai-search-official.md` whenever either Google label is in scope. Do not generalize that source to other providers.

## Evidence contract

For every finding capture the URL/surface, retrieval date, observed evidence, affected platform, severity, business impact, and concrete fix. Distinguish:

- official provider documentation;
- Search Console or analytics data;
- live page/SERP/source observations;
- third-party studies;
- local audit heuristics.

There is no public universal GEO score. Use a qualitative verdict (`strong | moderate | weak | blocked`). A numeric benchmark is allowed only when the user explicitly asks for a local heuristic and it is labelled as such.

## Readiness dimensions

| Dimension | Question |
|---|---|
| Search eligibility | For Google, are priority pages indexed, snippet-eligible, crawlable, and included by the Search generative-AI control? |
| Human usefulness | Does the page offer non-commodity, satisfying, first-hand/expert value? |
| Clarity/citability | Can a human or retrieval system understand and quote well-supported passages without artificial chunking? |
| Authority/entity | Is the entity represented consistently and corroborated by authentic evidence? |
| Technical access | Can the scoped provider's search crawler/fetcher reach key content under the owner's policy? |
| Evidence formats | Do images, video, tables, demos, or original data materially improve proof and usefulness? |
| Measurement | What does the scoped platform actually expose, with what limitations? |
| Commerce/agent usability | Where relevant, are current facts and high-value flows accurate and operable? |

---

## Procedure

### 1. Scope and baseline

Identify the homepage, product/service pages, pricing/proof pages, and high-value informational pages. Record whether each is static/SSR, hybrid, or client-rendered. Capture the exact platform scope; do not run one blended “AI visibility” formula.

### 2. Run the Google lane when Google AI Overviews or AI Mode is in scope

Load `google-generative-ai-search-official.md` and verify:

1. **Indexed and snippet-eligible.** Priority URLs satisfy ordinary Google Search technical requirements and may show a snippet. If they fail, set the Google AI lane to `blocked` before prescribing GEO work.
2. **Search generative-AI inclusion.** Record the Search Console control state as `included | excluded | inherited | blocked | not_checked`. Do not confuse this with `Google-Extended`, which is a model-training control.
3. **Crawlability and rendering.** Googlebot can access the content; JavaScript follows normal JavaScript SEO; key content is not blocked.
4. **Page experience and duplication.** Check mobile usability, latency, main-content clarity, canonicalization, and duplicate URLs as ordinary SEO foundations.
5. **Local/ecommerce surfaces.** When relevant, inspect Merchant Center/feed accuracy and Google Business Profile completeness.
6. **Content quality.** Look for unique point of view, first-hand experience, expert insight, original evidence, useful media, clear organization, and people-first satisfaction. AI-assisted content must still meet Search Essentials and spam policies.
7. **RAG and fan-out response.** Cover genuinely useful subtopics in one strong page or coherent cluster, supported by user/SERP/business evidence. Do not create one thin page for every synthetic fan-out or exact long-tail variation.

### 3. Enforce Google myth-busting guardrails

The Google audit must explicitly confirm:

- absence of `llms.txt` is **not** a Google defect, eligibility issue, or ranking recommendation;
- tiny artificial “AI chunks” are not required;
- AI-only rewriting and exhaustive exact-query variants are not required;
- manufactured or inauthentic mentions are never recommended;
- there is no special AI schema for Google Search; valid structured data remains tied to supported Search/rich-result purposes;
- useful headings, concise passages, FAQs, tables, and media are recommended only when they help people and accurately express the content—not as extraction hacks.

### 4. Measure Google with the official report

Load `references/playbooks/maintenance/google-generative-ai-visibility.md`. Check the Search Console **Generative AI performance report** and record:

- property and retrieval date;
- report date range;
- availability/access state;
- impressions by the dimensions the live report exposes;
- newest-data/aggregation/row-limit caveats.

At the 2026-07-10 source version the report is impression-only. Do not invent AI clicks, queries, CTR, conversions, or AI Overview-versus-AI Mode attribution. If the report is absent, record `not_available` or `blocked`; absence is not proof of zero visibility.

### 5. Add optional Cloudflare and provider citation lanes when they are in scope

**Cloudflare evidence.** When the site uses Cloudflare and its dashboard evidence is in scope, load `references/playbooks/maintenance/cloudflare-agent-readiness-and-aeo.md`. Record the dashboard access state before interpreting absence: the 2026-08-06 announcement made Agent Readiness available while AEO Visibility required early-access registration.

Capture Agent Readiness diagnostics, AEO Visibility panel metrics, and AI Operator Activity as three separate evidence lanes. Label AEO metrics as a precomputed synthetic category/model snapshot—not user-query impressions, clicks, market share, or causal attribution. Label operator crawls/referrals/errors as first-party network evidence and reconcile referrals with analytics before making business claims. Save the raw capture to `audits/<date>_cloudflare-agent-aeo.json`.

Do not call the product free without a current first-party pricing or entitlement check. Do not treat Cloudflare's readiness checks, Markdown support, crawler controls, or agent-protocol suggestions as Google ranking requirements. Any crawler-policy, authentication, security, or production change remains approval-gated.

**Provider-specific citations.** When the user wants mention/citation evidence for ChatGPT, Perplexity, Claude, Microsoft Copilot, or another named provider, load `references/playbooks/maintenance/cross-platform-ai-citation-loop.md`. Route repeatable panel validation, deterministic metrics, public social discovery, or a human approval queue to `workflows/ai-answer-visibility-loop.md`, then:

- freeze a small, versioned buyer-question set instead of ad hoc prompts;
- save the exact provider, surface, locale, language, account state, and retrieval date for each run;
- record mention presence, cited URLs/domains, source types, page-role gaps, and the minimum answer excerpt needed to interpret the citation;
- write the raw observation set to `audits/<date>_provider-citation-observations.json`, or state why no provider citation baseline was collected.

Keep each provider in its own dataset. These observations are not interchangeable with ordinary Search data, the Google Search Console Generative AI performance report, or Cloudflare's synthetic AEO panel. Do not invent clicks, queries, CTR, conversions, attribution, or a universal GEO score/formula from citation observations.

### 6. Audit human usefulness, clarity, and evidence

For each priority page:

- Does the opening orient the reader and answer the real question?
- Are claims specific, supported, and attributable?
- Does the page provide original examples, methodology, screenshots, data, or first-hand evidence?
- Are headings, paragraphs, lists, and tables arranged for human comprehension?
- Are author/entity details and update dates accurate where relevant?
- Would a visitor leave satisfied rather than needing a generic summary rewritten elsewhere?

Treat “citability” as a local clarity/evidence heuristic, not a Google requirement. Do not prescribe a fixed word count, fixed answer-block size, or artificial chunking pattern.

### 7. Audit entity consistency and authentic corroboration

Compare the canonical entity name, product/service description, authorship, organization/person schema, social profiles, directories, reviews, and earned coverage. Search the priority topics and inspect which sources are actually cited or ranked.

Flag contradictory names, claims, pricing, or identity details. Recommend only legitimate third-party coverage, reviews, partnerships, references, and links. Never recommend fabricated mentions, paid spam placements, fake discussion, or undisclosed influence.

### 8. Run provider-specific access checks for non-Google platforms

Fetch `robots.txt` and check only providers in scope, using current official documentation:

| Agent | Purpose to verify |
|---|---|
| `OAI-SearchBot` | OpenAI search discovery |
| `GPTBot` | OpenAI model-training control, distinct from search |
| `ChatGPT-User` | User-triggered fetches |
| `Claude-SearchBot` | Anthropic search discovery |
| `ClaudeBot` | Anthropic model-training control |
| `Claude-User` | Anthropic user-triggered fetches |
| `PerplexityBot` | Perplexity search discovery |
| `Perplexity-User` | Perplexity user-triggered fetches |

Provider behavior and names may change; verify before asserting. Respect the owner's licensing/privacy choice. If a desired platform crawler is blocked, report the tradeoff rather than changing policy.

`llms.txt` may be inspected only as voluntary, provider-specific documentation. Its absence is not a generic defect and must never be scored against Google. If present, verify that it contains no stale or false claims.

Compare raw HTML with the rendered page where relevant. Flag JS-only key content only when evidence shows a user or scoped fetcher cannot access it.

### 9. Audit evidence formats and agent usability

Inspect whether useful images, screenshots, video, demos, tables, charts, or original data strengthen understanding and proof.

When browser-agent task completion matters, separately assess:

- visual rendering/screenshots;
- DOM structure and stable controls;
- accessibility tree, names, labels, and errors;
- completion of high-value flows without submitting a consequential action;
- relevant emerging protocols such as UCP.

Label this **agent usability**, not a proven Google AI ranking factor.

### 10. Audit commerce/current-data consistency when applicable

Load `ai-search-commerce-readiness.md` for retailers, marketplaces, paid products, bookings, or services whose facts change. Compare crawled pages, feeds/APIs actually used by the business, and live state for identifiers, variants, price, currency, availability, language, freshness, shipping/promotions, and policies. Keep visibility, sessions, assisted conversions, transactions, revenue, and causal evidence separate.

### 11. Emit the report

Use this optional-rich input shape. `report.py audit` remains backward compatible with ordinary site-audit findings:

```json
{
  "summary": "...",
  "readiness_verdict": "strong|moderate|weak|blocked",
  "platform_scope": ["google_ai_overviews", "google_ai_mode"],
  "source_versions": {"google_ai_optimization_guide": "2026-07-10"},
  "google_eligibility": {
    "indexed_and_snippet_eligible": "pass|fail|blocked|not_checked",
    "search_console_ai_inclusion": "included|excluded|inherited|blocked|not_checked",
    "crawlable": "pass|fail|blocked|not_checked",
    "javascript_seo": "pass|fail|not_applicable|not_checked",
    "merchant_or_local_surfaces": "pass|fail|not_applicable|not_checked"
  },
  "google_myth_checks": {
    "llms_txt_not_treated_as_signal": "pass|fail",
    "no_chunking_requirement_claim": "pass|fail",
    "no_special_ai_schema_claim": "pass|fail",
    "no_inauthentic_mentions": "pass|fail"
  },
  "google_ai_performance": {
    "status": "available|not_available|blocked|not_checked",
    "date_range": null,
    "evidence": null,
    "limitations": ["impressions_only", "no_query_dimension"]
  },
  "agentic_readiness": "assessed|not_applicable|not_checked",
  "dimension_notes": {},
  "findings": []
}
```

Run:

```bash
python3 scripts/report.py audit \
  --workspace <DIR> \
  --title "GEO audit: <domain> <date>" \
  --data <geo-findings.json>
```

Save the exact JSON separately as `audits/<date>_geo-findings.json` for comparison.

---

## Decision points

- **Google page not indexed/snippet-eligible** → Google AI lane is `blocked`; fix ordinary Search eligibility first.
- **Google report unavailable** → record rollout/access ambiguity; do not call it zero visibility.
- **Cloudflare AEO unavailable** → record early-access/account state; do not call it zero visibility or assume a price.
- **Cloudflare panel moves** → compare category, models, and snapshot metadata before interpreting; never claim causality from the score alone.
- **Desired non-Google search crawler blocked** → report the platform-specific tradeoff and ask before any policy change.
- **JS-only key content** → raise severity only when accessibility or scoped fetch evidence supports it.
- **Good rankings but weak observed citation** → inspect content usefulness/evidence and authentic source coverage; do not prescribe hacks.
- **Weak readiness** → prioritize foundations, non-commodity content, authentic corroboration, and measurable gaps.
- **Moderate readiness** → improve entity consistency, valid structured data for normal Search purposes, richer evidence, and platform measurement. Do not prescribe `llms.txt` for Google.
- **Strong readiness** → maintain freshness and monitor dated platform/source changes.

## Routing

- Authority/entity findings → `authority-and-links.md`.
- Provider-specific citation/framing gaps → `category-citation-loop.md` when the issue is coverage/positioning rather than access alone.
- Repeatable answer panels, separated metrics, public social evidence, and approval queues → `ai-answer-visibility-loop.md`.
- Content fixes → `content-production.md`.
- Indexing/rendering/technical issues → `site-audit.md` or `technical-seo-maintenance.md`.
- Valid schema gaps → `schema-types-reference.md`.
- Google AI reporting → `google-generative-ai-visibility.md`.
- Cloudflare readiness/AEO/operator evidence → `cloudflare-agent-readiness-and-aeo.md`.
- Feed/live-state contradictions → `ai-search-commerce-readiness.md` and the owning backlog.

## Done when

Platform scope is explicit; Google and non-Google claims are separated; Google eligibility, myth checks, and report availability are recorded when applicable; any Cloudflare readiness, synthetic AEO-panel, and first-party operator evidence is captured in separate lanes with access state and limitations; provider-specific citation baselines are captured when citation diagnosis is in scope; priority pages have evidence-backed findings; agent usability is separately labelled; every recommendation has a concrete fix and owner; the qualitative verdict is assigned; and both Markdown and raw JSON artifacts exist.
