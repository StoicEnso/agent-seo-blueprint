---
title: Content Opportunity Audit and Measurement
area: maintenance
operational_addition: true
source_status: Single first-party case study adapted into bounded, evidence-gated operating rules on 2026-08-24.
---

# Content Opportunity Audit and Measurement

Use this playbook when a site has published content plus current Search Console data and the operator wants a recurring system that ranks content opportunities, drafts narrow fixes or missing-page briefs, and measures approved changes.

The source case study joined a CMS, Google Search Console, SEMrush, product analytics, and prior-run data. It reported strong results from one company. Preserve the mechanism, not the multiplier: its 5.8× impressions and 9.8× page-one-query claims are one observed outcome, not a benchmark, forecast, or promise.

## Operating boundary

Keep four components separate:

1. **Collectors** read the CMS, GSC, analytics, backlink/visibility tools, live pages, and the prior run.
2. **The agent** scores, verifies, drafts, and explains. It has no website write permission.
3. **The approval surface** presents an exact diff with evidence and `Approve`, `Edit`, or `Skip` states.
4. **A deterministic executor** re-reads the live page, validates the approved change, applies it once, records the receipt, and enrolls the change for measurement.

The agent's judgement belongs in the skill and is easy to revise. The write path belongs in tested code and must not trust the agent's claims without revalidation. No score, schedule, or previous approval authorizes publication.

## Inputs

- Current final GSC query+page data, normally the latest complete 28 days.
- The matching previous final window for real click-loss checks.
- Current CMS inventory with canonical URL, title, description, publication/update dates, and revision identifier or content hash.
- Live page and live SERP evidence for candidates that survive cheap screening.
- Optional analytics conversions, provider-specific citation observations, and prior audit/measurement ledgers.
- A user-approved cadence, candidate cap, expensive-verification cap, minimum evidence thresholds, and publication policy.

## Phase 1 — collect once and preserve scope

Pull each source in one bounded sequence. Record property, locale, device, search type, date windows, timezone, source freshness, and access limitations. Join GSC query rows to their observed page. Do not fan agents out against rate-limited sources.

Run cheap checks across the full inventory:

- missing or weak title/description;
- broken links, dead media, or invalid embeds;
- current click loss against the previous comparable window;
- current positions 4–20 with meaningful impressions;
- high-impression, low-CTR rows after position and SERP-feature context;
- stale product positioning or direct contradiction with current first-party documentation;
- cannibalization candidates where multiple URLs serve the same query intent; and
- query demand with no dedicated owner page.

Cheap checks produce candidates, not edit instructions.

## Phase 2 — rank by headroom

Compute three separate, inspectable signals. Keep their assumptions in the ledger.

### 1. Recoverable click loss

Use a real current-versus-previous decline. Require both a material absolute loss and a material proportional loss so tiny pages and noise do not dominate.

`recover_headroom = max(0, previous_clicks - current_clicks)`

A verified real loss outranks modelled estimates, but it still needs live diagnosis. Demand, seasonality, intent, indexing, SERP layout, competitors, or measurement drift may explain the decline.

### 2. CTR headroom

For current page-one rows, compare observed clicks with a property- and scope-specific expected CTR curve when one exists:

`ctr_headroom = max(0, expected_ctr(position, scope) × impressions - clicks)`

Average position blends queries, devices, countries, and dates. SERP features change organic CTR. Treat this as a queue-ordering estimate, not recoverable-click or revenue forecast. A borrowed generic curve must be labelled `HEURISTIC_FALLBACK`, and low-impression rows must not rank highly from percentage gaps alone.

### 3. Rank headroom

For relevant page-two or lower-page-one rows, estimate the click difference between current observed CTR and a modest target position supported by the live SERP:

`rank_headroom = max(0, target_ctr(scope) × impressions - clicks)`

Do not assume that a content edit will reach the target. Links, site authority, format, demand, and SERP regime may be the real constraint.

### Queue rule

Store all three signals. Let the strongest valid signal name the candidate's primary lever, but preserve the other values and assumptions. Prioritize verified click loss before soft estimates. Apply a candidate cap. Expensive verification runs only on the highest-value candidates plus a small rotating buffer so low-volume pages are not permanently ignored.

## Phase 3 — verify before drafting

For every shortlisted candidate:

1. Open the live page. Do not diagnose from memory or stale CMS text.
2. Inspect the exact live SERP and current intent/format.
3. Confirm the observed ranking page and canonical.
4. Identify the smallest evidence-backed change.
5. Check product truth and source every direct contradiction.
6. Check cannibalization and existing page ownership.
7. Route authority-constrained rows to `authority-and-links.md` instead of rewriting them.

Use one of these dispositions:

- `METADATA_TEST` — current impressions and ranking exist, but the title/description does not match intent.
- `SURGICAL_CORRECTION` — one exact phrase, fact, link, media reference, or product detail is wrong or stale.
- `CONTENT_ADDITION` — the page lacks a narrow section needed by the observed intent.
- `REFORMAT_OR_REBUILD` — the live SERP rewards a different format; require a normal content brief and human review.
- `CONSOLIDATE_OR_RETARGET` — multiple owned pages overlap materially.
- `NEW_PAGE_BRIEF` — current demand has no appropriate owner page and passes the normal content-production gates.
- `AUTHORITY_ROUTE`, `TECHNICAL_ROUTE`, `NO_ACTION`, or `NEEDS_MORE_DATA`.

Do not auto-publish any class. The source case study auto-applied two narrow classes, but this blueprint keeps all website writes explicitly approval-gated.

## Phase 4 — generate only from observed demand

A new-page candidate needs:

- current query demand and an observed URL/coverage gap;
- live SERP and intent confirmation;
- a real cluster, persona, and business purpose;
- a source packet for material claims;
- a product-truth contract when product claims appear; and
- a cannibalization check against every existing owner page.

Before any draft is saved, run four gates:

1. **Strategy** — approved cluster/persona, no forbidden claim or term.
2. **Structure** — intent-matched format and required sections.
3. **Provenance** — every material claim and code snippet has a source; code includes its first-party documentation URL and version where available.
4. **Cannibalization** — no existing page already owns the target query and intent.

Allow no more than two evidence-led revision attempts. If a hard fail remains, stop without a draft and emit the defect report. Never rephrase a cannibalizing topic until it slips through the gate; route it to the existing owner page.

## Phase 5 — approval and deterministic execution

Each review item must show:

- candidate and primary lever;
- source windows and assumptions;
- current live text and proposed exact diff;
- evidence URLs and quoted contradictions where relevant;
- expected outcome stated as a hypothesis;
- risk, rollback method, and measurement dates; and
- `Approve`, `Edit`, or `Skip` state.

The executor must:

1. acquire an idempotency lock for the change identifier;
2. re-fetch the page and current CMS revision;
3. reject stale approvals when the content hash/revision no longer matches;
4. reject if another unsaved or newer draft would overwrite the approved change;
5. re-run schema, link, product-truth, provenance, and cannibalization checks relevant to the change;
6. apply exactly the approved diff once;
7. verify the live result and canonical URL;
8. write a receipt with the live revision and timestamp; and
9. enroll the change in the measurement ledger.

A failed receipt or enrollment does not justify a blind retry. Reconcile the live state first.

## Phase 6 — measure approved changes

At the live-change timestamp, save:

- page/query GSC metrics for the preceding final 28-day window;
- the same site's aggregate search metrics for the identical dates as a directional control;
- analytics sessions, conversions, and revenue when available;
- current indexation, canonical, title/description, and relevant live-SERP state;
- provider-specific AI crawl, citation, and referral observations in separate lanes; and
- the exact old/new change with approval and deployment receipts.

Schedule final-data reads at **+28 days** and **+56 days**. Compare like-for-like scope. Preserve absolute and proportional changes for the page and the same-period site control. Do not call a lift causal when the whole site, demand, SERP, product, links, or tracking changed.

For a new page with no baseline, record a growth curve from zero at the same checkpoints. Do not compare it to a fabricated pre-period.

Keep these outcomes separate:

- ordinary Search impressions, clicks, CTR, and position;
- analytics sessions, leads, conversions, and revenue;
- AI crawler access;
- answer-provider citations or mentions; and
- referral clicks from named providers.

Citation observations are not impressions, clicks, conversions, or attribution.

## Cadence

A safe default is:

- weekly cheap inventory scan and bounded candidate queue;
- weekly owner review of proposed edits and at most one new-page draft;
- monthly operational outcome review; and
- quarterly strategy review against leading and trailing indicators.

The user chooses the schedule. Do not create a recurring job until the workflow has passed a manual pilot, the artifact shape is reviewed, the inputs are non-interactive, and failure/stop paths are observable.

## Required artifacts

- `monitoring/<date>_content-opportunity-audit.json`
- `monitoring/<date>_content-opportunity-summary.md`
- `drafts/<date>_<candidate>-proposed-change.md` or a normal content brief
- `monitoring/content-change-ledger.jsonl`
- `monitoring/<change-id>_28d.json`
- `monitoring/<change-id>_56d.json`

Copy `assets/content-opportunity-ledger.json` as the schema seed.

## Stop conditions

Stop or downgrade a candidate when:

- GSC data is stale, partial, or scoped differently across windows;
- the live ranking URL, intent, or canonical cannot be confirmed;
- impressions are too low for the proposed estimate;
- the candidate is authority- or technical-constrained rather than content-constrained;
- a source claim or product fact cannot be verified;
- another page already owns the intent;
- the approved diff is stale;
- a write or verification receipt is missing;
- the site-wide control moved materially enough to prevent a useful interpretation; or
- the only reason to act is a creator's claimed multiplier.

## Done condition

The run is complete when every candidate has an evidence-backed disposition, soft headroom estimates remain labelled as estimates, expensive checks stayed within the cap, no agent received website write access, every live change has an exact approval and receipt, and every live change has scheduled 28-day and 56-day readings with page and same-period site evidence.

## Source lineage

- Ian Nuttall share: <https://x.com/iannuttall/status/2091882414083596320>
- Quoted first-party case study: <https://x.com/harsehaj/status/2091690736211112005>
- Saved research note: `vault/knowledge-base/articles/2026-08-24-how-i-built-an-seo-aeo-blog-engine.md`
