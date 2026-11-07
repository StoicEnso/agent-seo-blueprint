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


## Optional Google + Bing page-query coverage review

Use this branch when Google Search Console (GSC), Bing Webmaster Tools (BWT), or both expose useful query evidence for an existing page. Bing-only observations can supply additional research leads even when the Google query export has no matching row. This supplements the existing audit; it does not replace its live-page, approval, executor, or measurement gates.

Copy `assets/gsc-bing-query-coverage.json`. Read `references/integrations/gsc.md` and `references/integrations/bing.md`. Start with one page and a small, operator-chosen query-cluster cap (for example five). Expand only after reviewing the first artifact. No new account, API key, paid tool, scheduled job, or website write is needed to draft this review from approved saved exports.

### 1. Freeze page and source scope

Record the exact page URL, observed canonical, title, revision/content hash, primary target, audience, offer, page-read time, and source excerpt locator. A domain-wide query list is not evidence that a particular page ranks for those queries: require a page filter or query-to-page evidence before calling a row page-level.

For each engine, retain the raw export and record property/site, report/surface, page filter, start/end dates, report timezone, country, device, search type, collection time, final/preliminary state, pagination/row cap, known omissions, and evidence locator. Record unsupported dimensions as unavailable; do not invent a filter merely to make scopes match. Use the latest complete 28-day window for current review when both sources support it. A longer window, such as three months in the source screenshot, is discovery context; do not silently compare it with a 28-day baseline.

Each engine has an explicit source status: `available`, `partial`, `unavailable`, or `not_requested`. For partial data, record what was actually returned and why it is incomplete. Continue a clearly labeled single-engine review when the other engine is unavailable. The missing source is **unknown, not zero**. The Google table can omit queries for privacy and other reporting limits; a missing row does not establish no demand, no ranking, or no impressions. Do not bypass an access gate or start an account-import/setup flow to fill the gap.

### 2. Union query discovery; do not blend engine metrics

- Preserve each original query spelling and raw-row locator. Normalize Unicode, case and whitespace for matching; keep a reversible mapping. Do not drop negation, brand names, locations, languages or intent-changing modifiers. Review semantic clusters; shared words alone do not establish shared intent.
- Use engine + property + exact page + date window + dimensions + raw-row identity to detect accidental duplicate exports. Do not double-count repeated files, overlapping periods, daily versus period aggregates, or property versus page totals. Keep rows for competing URLs separate until a cannibalization review resolves ownership.
- Label a cluster's observed source presence `GSC only`, `Bing only`, or `both`, based on the supplied exports. `both` can mean distinct variants in one reviewed cluster; list the exact queries by engine. These labels describe observed exports, not the engine's complete query universe. If one export is unavailable, explicitly qualify the label with that limitation.
- Preserve **separate engine metrics**: clicks, impressions, CTR and average position. Never add Google and Bing impressions into a claimed search volume or unique audience; never average their positions or CTRs into one ranking/priority score. Bing query data does not prove Google visibility, Copilot citations, ChatGPT traffic, sales, or profit.
- Within one engine only, aggregate disjoint, same-scope rows when justified. Recompute CTR as `sum(clicks) / sum(impressions)`; zero impressions gives undefined CTR, not a fabricated performance signal. Aggregate positions only if the provider's definitions and weighting permit it; otherwise retain the original values. Do not average row percentages or assume query sums reconcile with chart totals.
- Keep observed zero, unavailable metric, absent row, and source failure distinct. Record source UI placeholders and export conversions; Google documents that some unavailable values export as zero. Do not turn an unavailable average position into rank zero.

### 3. Check coverage and engine-specific intent

For each reviewed cluster, read the current page and assign one status:

| Status | Evidence required | Disposition |
|---|---|---|
| `covered_well` | Exact relevant quote and section locator | Keep; do not pad solely for extra keywords |
| `covered_weakly` | Quote/locator showing the vague, buried or incomplete answer | Draft a narrow improvement |
| `not_covered` | Recorded page read and explicit `none` for a matching answer | Draft only if the page's job fits |
| `wrong_intent` | Query intent differs from this page's purpose | Reject here; assess another existing owner page before a new-page brief |
| `unverified` | Page, canonical, content or required evidence unavailable | Research-only; no implementation recommendation |

For the primary cluster and meaningful weak/missing clusters, capture modest live search-result evidence for the **named engine**, exact query, date, country/locale and device when exposed. Record observed top-result URLs, dominant intent (informational/commercial/transactional/navigational), format (guide/comparison/tool/product/etc.), useful gaps, and visible features such as PAA, video or a snippet. Do not infer Google intent from a Bing result or vice versa. If live search results are unavailable, record `not_checked` and keep that cluster research-only. Do not claim snippet/FAQ eligibility or rankings from adding a section or schema.

Check existing page ownership and cannibalization, product truth, required first-party evidence, and whether the proposed answer adds real reader value. Do not reproduce competitor text, add every query as a heading, or create one thin page per variant. Off-topic demand is not permission to broaden the page.

### 4. Prioritize and draft, with reasons

Assign High/Medium/Low **review priority**, with a written reason using per-engine evidence strength, intent/business fit, sufficient current impressions under a declared threshold, uncertainty, and effort. Roughly positions 5–20 can be a screening hint within each engine, not a universal quick-win rule or predicted gain. Low CTR may reflect position, device, brand mix, SERP features or intent; it is not automatically a title/meta defect. Do not use a universal CTR cutoff or transfer one engine's curve to the other.

Emit these five sections:

A. **Summary:** biggest supported coverage gaps, source availability, and limitations.

B. **Coverage table:** cluster ID, exact examples by engine, observed source presence, GSC metrics, Bing metrics, scopes/comparability, coverage status, page quote/locator, engine-specific SERP evidence, review priority and reason. Unknown fields stay null with a reason.

C. **Ordered recommendations:** target queries, exact proposed diff or smallest section change, insertion point, proposed heading, two or three sentences explaining the useful answer, evidence, effort, owner/cannibalization check and disposition. Wrong-intent rows do not become additions to this page. Record suitable contextual internal links to/from existing pages with a reader reason, not a quota.

D. **Metadata options:** two or three honest title/description variants only when evidence supports them; identify the page promise each must keep. Never force every variant into the title or fabricate a year, feature, price or result.

E. **Review and measurement:** exact target and revision/hash, approval state, risk/rollback, unavailable checks and next owner action. After an approved change, compare each engine separately at +28 and +56 days using the same page/query scope and like-for-like final windows; retain site-wide context and confounders. Search observations, referrals, conversions and revenue remain separate. New schedules require their own approval.

### 5. Preserve the write boundary

Default state is `draft_only`. No prompt, priority, export, or source-post instruction authorizes editing, internal-link changes, publishing, IndexNow, sitemap or URL submission. Require explicit approval for the exact write and use the existing deterministic executor/stale-revision checks. Indexing submission is a **separate approval-gated action**, not an automatic final step. A submission receipt does not prove crawling, indexing, ranking or a traffic gain. Do not repeatedly resubmit unchanged URLs, enable an indexing plugin, add verification records, import account permissions, or use Google's restricted Indexing API for ordinary articles.

Done when the review preserves raw evidence, source availability, separate engine metrics, page quotes and scoped SERP observations, and gives a checked recommendation or explicit research-only/rejected disposition for every shortlisted cluster. A draft report can be complete while publication and business outcomes remain unverified.

**Worked example:** `examples/gsc-bing-query-coverage.md` (synthetic, not live site evidence).

**Source and limits:** adapted in original wording from Andrei Saioc's 6 November 2026 [post](https://x.com/asaio87/status/2118634208411185175). The useful idea is dual-source query discovery followed by page/intent review. The source's 'profit' wording, positions 5–20 heuristic, low-CTR explanation and automatic resubmission step are not verified guarantees or operating authority. Its screenshot is one selected three-month page view, not a controlled Google/Bing comparison. Full Note Tweet text was retained; its title/meta output sentence ends mid-sentence in the returned source. No omitted ending was invented.
