---
title: Weekly GSC Action Queue
area: maintenance
operational_addition: true
source_status: Single creator anecdote adapted into review-only work records; qualified against Google primary documentation on 2026-10-12.
---

# Weekly GSC action queue

A compact **offline review artifact** for an existing resolved project and explicitly authorized Search Console property. It turns saved, read-only ordinary Search evidence into specific, bounded tasks rather than another metric-only report. It does not decide SEO strategy automatically, connect accounts, run on a schedule, change a CMS, or publish. Monday is an optional owner-selected review cadence, never an invented global task time.

This extends [content opportunity audits](content-opportunity-audit-and-measurement.md), not a second ranking engine or CMS executor. Keep its existing approval, exact-diff, stale-revision, source/quality, and +28/+56 measurement gates.

## Inputs and scope contract

Use the latest two **finalized**, non-overlapping, equal-length windows (normally 28 days). Record each window's property, search type, query+page dimensions, filters, response aggregation, start/end dates, source references and final state. The two explicit window scopes must match the queue scope. Do not infer equivalence from one shared label.

Record collection date, final-through date, source freshness, and export/top-row/privacy limits. GSC date boundaries use **America/Los_Angeles** (Pacific time), not the operator's local date. API responses return top rows and are not a complete query inventory. Missing query rows mean **unknown**, not zero. Do not compare changed filters, properties, dimensions, aggregation, incomplete, or stale windows as like-for-like. Preserve unknown previous metrics as `null`; never replace missing rows with synthetic zeros or calculate percentage growth from unknown/zero baselines.

`gsc_pull.py` remains a credential-gated **stub**, not a working automatic GSC connection. Use the existing [GSC integration](../../integrations/gsc.md) for an authorized collector. A browser, API, Codex, or another permitted route may save an export; none grants account, installation, scheduler or website-write authority. Do not upload credentials or private exports into a public repository or prompt.

## Decide the work before drafting

Use current useful demand and diagnosed real loss to order review, not a universal CTR/rank formula or uplift promise. Keep absolute changes, proportional changes, assumptions, site-wide changes, seasonality, update dates, tracking changes and other confounders distinct. A weekly swing or average position alone is not an instruction to rewrite a page.

- `UPDATE_EXISTING`: inspect the live page, canonical, exact SERP and intent first. Identify the smallest useful correction or addition and record its baseline CMS/source revision. Inspect product truth and material sources before a draft; use the established content QA gates. Route technical or authority problems to their owning workflow, not a content rewrite.
- `NEW_PAGE_REVIEW`: verify current demand, audience/business relevance, live SERP, existing inventory/cannibalization, distinct page role, useful original contribution and source packet. Rising impressions alone never selects a new article. If an existing page owns the intent, improve/consolidate/retarget it or hold; do not create a competing page.
- `HOLD` / `NEEDS_MORE_DATA`: keep the observation and name the missing fact, evidence or decision. Partial/stale records can be held but cannot become action-ready merely by changing a label.
- `NO_ACTION`: retain the reviewed reason not to act; do not manufacture a new task to fill a weekly quota.

Apply project-selected candidate and expensive-check caps. The example cap of 20 candidates and 8 checks is an editable policy seed, not a Google rule. The validator checks the *declared* counts; it cannot audit external tool calls. Record every live/expensive check truthfully.

Use a stable dedup key for project + canonical/target page + normalized intent. Preserve the task ID across runs. Carry pending work forward instead of cloning it; record each prior pending ID/key in `prior_pending_tasks`. Every pending item needs a current carried, held, or resolved disposition. Do not silently drop work, invent that there is no prior queue, reset deadlines, or open a duplicate task when the prior ledger is unavailable. Group overlapping proposals for review.

## Artifact contract

Copy `assets/weekly-gsc-action-queue.json`. Its placeholders intentionally fail validation. Example dates are illustrative, not a current data pull. Record these fields:

- `schema_version: "1.0"`, stable `queue_id`, explicit `scope`, and matching `windows.current.scope` / `windows.previous.scope` with saved `source_refs`.
- `limitations`: non-empty declarations of coverage, unknowns and relevant access/measurement limits.
- `execution`: `mode: "review_only"`, `cms_write: false`, `publish: false`, `schedule: false`. There is no execution authority in this artifact.
- `caps`: integer `candidate_cap` and `expensive_check_cap`; no silent overflow.
- `review_policy`: owner-selected `max_data_age_days`, `max_evidence_age_days` and `due_timezone`. Example7-day ages are workflow policy, not a freshness ranking rule. The timezone is a named project declaration; the validator checks its IANA-style shape, not local scheduler configuration.
- `prior_pending_tasks`: saved stable `{id, dedup_key}` identities, or an explicitly checked empty set. The validator can check declared identity consistency, not independently discover prior work.
- Every task: `id`, `dedup_key`, `outcome`, non-placeholder `evidence_refs`, `carried_forward` and `expensive_check` booleans. Holds need `hold_reason`; no-action records need `no_action_reason`.

For `UPDATE_EXISTING` and `NEW_PAGE_REVIEW`, also require:

- `lane`, `query_or_intent`, authorized-property `target_url`, precise `problem_or_deliverable`, named `owner`, and `acceptance_criteria`.
- `due: {date: "YYYY-MM-DD", timezone: "<project timezone>", policy: "<owner-selected review rule>"}`. This is a review due date, not a newly created Monday automation. Carried overdue work retains its original date and `overdue_reason`.
- `approval_status: "PENDING"` and inspectable `source_or_cms_revision`. No validated/approved/auto-write state is permitted.
- `metrics.current` and `metrics.previous`, each with `clicks`, `impressions`, fractional `ctr` and `position`; unknown previous values remain `null`. Record `uncertainty`; optional `growth_pct` is limited to clicks/impressions with known nonzero baselines and must agree with observed values. It is not a forecast.
- Evidence-bearing `checks`, each shaped `{status: "confirmed", evidence_refs: ["saved reference"], observed_date: "YYYY-MM-DD"}`. Generic strings or booleans are insufficient. Update checks: `page`, `canonical`, `serp`, `intent`, `cannibalization`. New-page checks: `serp`, `intent`, `cannibalization`, `demand`, `business_relevance`, `inventory`, `distinct_page_role`, `original_contribution`, `source_packet`. New-page review must have `existing_owner_url: null` *after* the inventory/intent check rules out an existing owner.
- `measurement_plan`: `checkpoints_days: [28,56]`, `like_for_like: true`, saved `baseline_refs` and separate `site_control_refs`, `metrics_separate: true`, `causality_claimed: false`, `schedule_created: false`. These are a follow-up plan, not fabricated measurement or a registered job.

The validator rejects unsupported fields, malformed or duplicate JSON keys, bad dates/types/metrics, scope drift, stale or non-final action data, duplicate/cloned pending work, cap overflow, missing evidence declarations, unsupported growth claims and executable states. Partial hold records may pass the schema without being actionable. Passing validation proves **schema/invariants only**: it does not open source files, verify evidence content, infer intent, evaluate the proposed text, assess product truth or approve a task. Human/agent evidence review is still required.

## Validate and route

```bash
python3 scripts/weekly_gsc_actions.py <saved-queue.json>
# Historical artifact review only; this does not make old data current:
python3 scripts/weekly_gsc_actions.py <saved-queue.json> --as-of 2026-10-02
```

The CLI defaults freshness to today's UTC date, rejects invalid files with structured JSON and exit code 2, and never makes network/credential/scheduler/CMS calls. Library validation defaults to the recorded collection date for deterministic historical checks; supply the current `as_of` date for a live review. A 4 MiB input limit bounds the offline file parser.

Save the queue at `monitoring/<date>_weekly-gsc-action-queue.json`. Route selected tasks through the existing monitoring/content-production handoff. Prepare the exact proposed diff with evidence, risk, rollback and baseline revision. No automatic CMS write. Revalidate the revision and exact approval before any permitted executor applies a change. Reject stale approvals.

Measure approved work with like-for-like **+28/+56-day** reads and a separate same-period site control. Keep ordinary Search, analytics/revenue and AI observations separate. No observation or source screenshot proves causality. Scheduling these reads still requires the project's explicit cadence and authority; merely recording a plan creates no routine.

## Codex or agent review prompt

> For the existing resolved project and explicitly authorized GSC property, produce a saved weekly action queue from supplied read-only exports only. Do not connect GSC, install tools, schedule work, write a CMS or publish. Compare latest finalized, non-overlapping equal-length query+page windows in America/Los_Angeles; record each source scope, limits, unknowns and current final-through date. Inspect prior pending work and preserve stable identities. Produce specific UPDATE_EXISTING, NEW_PAGE_REVIEW, HOLD/NEEDS_MORE_DATA or NO_ACTION records, not a metric-only report or content quota. Require live page/SERP/intent/canonical diagnosis and the smallest useful diff for updates. For new-page reviews, verify demand, relevance, existing inventory/ownership, distinct role, original contribution and sources; rising impressions alone are insufficient. Include named owner, project due-date policy/timezone, evidence-bearing checks, revision, acceptance criteria, PENDING approval, and a separate +28/+56 measurement plan. Keep missing rows unknown and creator uplift claims separate from project evidence. Apply declared caps and validate the artifact, then present it for evidence and exact-diff review. Passing validation grants no execution authority.

## Source and limits

[Mila's post](https://x.com/milachervenkova/status/2109259283523043469) suggests a Monday task list and reports one exact-match-domain traffic increase. It is not causal or transferable proof. Reject monthly EMD updates as a guaranteed ranking rule and do not attribute results to a Google update without separate evidence. Changing dates or adding/removing content merely to seem fresh is not a useful update.

- [Search Analytics query](https://developers.google.com/webmaster-tools/v1/searchanalytics/query): final data, Pacific date boundaries, response aggregation, filters and top-row limits.
- [Google people-first content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content): helpful original work, not date-only freshness or automated ranking manipulation.
- [Source audit](../../audit-log/2026-10-12-weekly-gsc-action-queue.md).

## Done when

Specific capped review work or explicit hold/no-action reasons are saved with evidence, identity and source limits. Validation and independent review are recorded separately. No task is approved by its score/schema, and no website or schedule changed from this artifact. Any later permitted publication follows the existing exact-diff, QA, live-receipt and measurement gates.
