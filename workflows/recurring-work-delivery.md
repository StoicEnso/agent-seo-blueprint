---
title: Recurring SEO work delivery
goal: Turn fresh, evidence-bounded signals into reviewable work without promising output, scheduling work, or bypassing approval.
playbooks:
  - references/playbooks/maintenance/seo-operational-checklist.md
  - references/playbooks/maintenance/content-opportunity-audit-and-measurement.md
scripts:
  - scripts/workspace.py
  - scripts/report.py
integrations: []  # selected by the owning workflow, using existing authorised access
outputs:
  - monitoring/recurring-work-ledger.md  # links to existing detailed owner artifacts
  - monitoring/<date>_weekly-work-review.md
  - monitoring/<date>_monthly-outcome-review.md
---

# Recurring SEO work delivery

Use this wrapper to prepare and deliver recurring work through the existing research, content, audit, technical, authority, AI-answer, and monitoring workflows. It is manual by default. It does not start a scheduler, provider, website write, directory submission, outreach, or publication.

The service-offer screenshot that prompted this wrapper is a dated marketing observation. Its article/fix/pitch counts, price references, page-one and indexation claims are not capacity targets, guarantees, or proof of repository capability. The post attributes $1,500/month; the pictured offer says $1,000/month. Keep those claims attributed rather than reconciling them into a fact.

## Inputs and route selection

Record business context before prioritising: offer, customer and market, commercial value or margin when known, fulfilment capacity, buyer journey, approved product claims, current releases/migrations, conversion-path evidence, and unknowns. Never infer missing context.

| Signal / question | Existing route | Required guard |
|---|---|---|
| demand, buyer questions, comparisons, page maps | `workflows/research-and-ideation.md` | provider/date/window/country/unit/status provenance; GSC appearances are property observations, not market demand |
| draft, comparison, calculator, page revision or social adaptation | `workflows/content-production.md` | product truth, distinct value, factual review, approval before publishing |
| title, internal-link, speed, redirect, indexation, canonical, robots, JavaScript or schema concern | `workflows/site-audit.md` then `workflows/technical-seo-maintenance.md` | preserve reproduction evidence and alternative explanations; no blind write |
| link, directory or editorial opportunity | `workflows/authority-and-links.md` | qualify relevance and approval; no outreach/submission from this wrapper |
| AI answer/citation observation | `workflows/ai-answer-visibility-loop.md` | citation is not traffic, conversion, revenue, or causal proof |
| regression, page-two observation, competitor/release change, business outcome | `workflows/monitoring.md` | collection completeness and date-window limits before diagnosis |

Copy `assets/recurring-work-ledger.md` to `monitoring/recurring-work-ledger.md` in the existing project workspace as the single reviewed-work ledger. It is a raw source artifact, not a `report.py` template; do not claim renderer support for it. Link existing content-opportunity, citation, directory and technical artifacts by stable item ID instead of copying them into a competing truth system. Preserve raw manifests and data beside their owning artifacts.

## State and delivery contract

A row moves only through these states: `proposed`, `drafted`, `approved`, `applied`, `verified`, `deferred`, or `rejected`. `approved` is permission for the exact reviewed scope, not proof of application or success. `applied` requires a receipt; `verified` requires the defined post-change check. `deferred` and `rejected` retain the reason and evidence.

Before any write, recheck the input, business/release context, approval scope, target state, and duplicate/carry-forward rows. Pause only the affected action when its required evidence is stale or inadequate, access is missing, collection is partial/failed, capacity or budget is unapproved/exhausted, its route has an unresolved blocker, or the exact change differs from approval. A bounded sample can support a bounded observation, not a whole-site claim. Keep independent safe work moving. Preserve the reason and next check; do not rerun blindly.

A proposed change must retain: measured fact (or explicit `UNKNOWN`), source/artifact and capture time, collection status (`MEASURED_ZERO`, `MISSING_ACCESS`, `FAILED`, `PARTIAL`, `UNAVAILABLE`, or other stated limit), hypothesis and alternatives, priority reason, owner, authority/approval, exact diff or revision, risk/rollback, receipt, and outcome check. Use `OBSERVED`, `PROVIDER_ESTIMATE`, `MODELLED`, or `UNKNOWN` for numeric provenance. A missing or partial pull is not a measured zero.

## Cadence is a review trigger, not a quota

- **Daily, when fresh evidence exists:** inspect new regressions, release notices, broken conversion paths, indexation/technical alerts, and bounded AI-answer observations. Route only actionable, non-duplicate work.
- **Weekly:** reconcile carried rows, changed competitor/content observations, page-two candidates, approved draft/revision candidates, receipts, blockers, and conversion-path checks. Compare like-for-like windows only.
- **Monthly:** review business outcomes where first-party evidence exists (qualified leads, bookings, sales or contribution), capacity, budget, unresolved risks, stale assumptions, and whether recurring checks remain useful. Output counts alone are not success.
- **Release-triggered:** when an actual approved release, price, feature, claim, migration, redirect, or offer change is evidenced, verify product truth, affected comparison/pricing pages, structured data, feeds and related drafts, conversion path, release claim correctness, and rollback owner before proposing work.

Do not schedule cadence, set a fixed crawl/article/fix/pitch quota, or promise rankings, indexation, citations, traffic, leads, or revenue. A scheduler or paid provider needs separate explicit approval of cadence, cost, owner, and stop rule.

## Manual operating pass

1. **Resolve and scope.** Run `python3 scripts/workspace.py status --path <DIR>`. Ask before creating an absent workspace. Reuse the existing plan, ledgers, owner approvals and holds. Record target URLs/templates, applicable checks, available sources, freshness limits, inspection/drafting capacity and maximum permitted cost. This wrapper does not widen access or release an owner hold.
2. **Inspect a bounded change set.** Use new signals, changed releases and prior failed/partial rows instead of rerunning every audit. Keep source state and coverage explicit. Run the owning workflow's collection step with existing authorised access; a helper stub or successful exit is not evidence of collection. Missing inputs do not become zero. Mark inapplicable checks with a reason.
3. **Reconcile before adding.** Match existing work by target, change type and revision. Reuse the stable ID and link its detailed artifact. Carry unresolved rows with owner, reason and next trigger; never discard them merely because a new week starts. Record observed fact separately from hypothesis, alternative explanations and confidence reason.
4. **Prioritise useful work.** Rank real breakage and conversion risk, truthful product/release corrections, and evidenced buyer opportunities by business value, uncertainty, dependency and effort. Stop new work at the recorded capacity/cost limit. Do not fill a content, fix, crawl or outreach quota. Prepare social drafts through content production only when useful for the approved surface; no public post is sent by this wrapper.
5. **Prepare and review.** Route the item to its existing workflow. Preserve exact diff/revision, source packet, owner, approval scope, risks, rollback and post-change check. Revalidate changed inputs and target state before any separately authorised execution. `approved`, `applied` and `verified` are distinct. This document is a review procedure, not an implemented executor or security control.
6. **Report and close the pass.** Write a weekly change review and, when due, a monthly outcome review. List new/carried/rejected work, drafts, exact-approved work, actual applied receipts, verification results, blockers and next checks separately. Use existing monitoring snapshots for supported metrics; raw ledger/manifests remain authoritative for fields the renderer does not display. No causal outcome is implied by a count of completed tasks. Keep due measurement reads in the manual queue or an already authorised routine; this pass creates no timer.

## Closeout

Record an exact revision/diff and rollback path for every applied change. Record a receipt that identifies what actually happened, then run the route-specific regression/outcome check at the stated window. A check can verify implementation, not causal SEO or business effect. Keep evidence, missing-data limits, and carried work visible in the ledger.

**Done when.** The applicable inspection is recorded, every action has a truthful state and linked source evidence, duplicate/carried rows are reconciled, the appropriate weekly/monthly review exists, and the next checks have owners and triggers. Unavailable data or an unresolved hypothesis remains explicit; it does not prevent unrelated safe work.

## Source limits

Prompting reference: https://x.com/illyism/status/2107528090025107778, saved 7 October 2026. Its pictured service offer is not an implementation benchmark. The owning workflows and current primary-source evidence, not the screenshot, determine each action.
