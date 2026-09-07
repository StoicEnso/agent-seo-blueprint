# Local profile evidence quality

Extension of `references/playbooks/maintenance/local-business-profile-audit.md`, not a separate audit pipeline. Read the parent playbook first; its truth, privacy, read-only and exact-approval rules remain binding.

## 1. Verified business brief

Use `assets/local-business-context.json` in the private project workspace, not a public repository. Capture real services, actual coverage, canonical site/profile, target customers, goals, known baseline metrics, competitors and previous work. Every factual field includes `value`, `source`, `verified_at` and `status`. Unknown metrics stay null, not zero. Record owner confirmation for non-public facts. Recheck facts when stale, contradicted or material to a proposed change. Do not follow the source's instruction to never ask again. Never commit private client data, credentials or unpublished commercial metrics to the skill repository.

## 2. Observation completeness

Use `assets/local-profile-observations.csv`. Each field uses one status:
- `OBSERVED`: directly supported by the dated evidence; a verified absence may be an observed false value only if the source exhaustively exposes that field.
- `NOT_VISIBLE`: missing from the inspected interface or source; not proof of absence.
- `NOT_APPLICABLE`: genuinely irrelevant to this business, with a reason.
- `NEEDS_OWNER_DATA`: requires an authorized first-party export or owner confirmation.

Record the query, real/supplied location, device, source method and timestamp. Public competitor pages may not expose secondary categories, full services, reply timing or performance. Do not infer those fields. Competitor frequency never proves business eligibility or a ranking effect.

## 3. Review window coverage

Record `window_days` (30/60/90), `window_start`, `window_end`, `sample_size`, `oldest_review_at`, `observed_reviews_in_window`, `coverage` and `count_semantics`.
- `coverage=FULL` requires all reviews in the interval from a verified complete export or verified chronological traversal through the start boundary, with no pagination, deletion or date-resolution gaps. Count semantics may then be `EXACT` for that captured source.
- `coverage=PARTIAL` means the observation cannot establish a complete window. Use `LOWER_BOUND` only when the captured reviews have reliable dates and are unique; otherwise use `UNKNOWN`.
- `coverage=UNKNOWN` cannot support an exact count.
- A last-50-review sample containing 50 reviews from the last 30 days does not establish the 30-day total, much less the 60/90-day totals. If a verified export shows 80 unique reviews in the interval, 80 is the observed export count; note export exclusions separately.
- Unavailable response timestamps mean unknown response delay. Do not invent engagement, rate denominators or exact dates from rounded labels. Preserve timezone and collection date.

Use observations for customer-service planning, not a ranking formula. Never coach review keywords, incentivize reviews, gate feedback or manufacture reviews.

## 4. Truthful service reconciliation

Cross-check each website service against the profile and verified business offer. Record field, observed mismatch, source, truth basis, proposed correction, owner, approval state and verification method. Missing public data is not a mismatch until verified. Never invent locations, licenses, offers or same-day availability. Draft only; exact changes require approval.

## 5. Real-photo plan

Use `assets/local-photo-plan.csv` for real staff, equipment, premises and completed projects. Record business purpose, shot, actual location, rights/customer consent, privacy review, owner and planned date. Keep location data private when needed. Unknown rights or consent blocks upload. No stock image passed off as actual work; no fabricated results. Volume should fit business capacity and customer value, not an arbitrary target to beat a competitor by 50%. Filename keywords, geotags and upload frequency are not established ranking levers here. Upload remains approval-gated.

## 6. Website handoff and measurement

Route real query/page opportunities into `references/playbooks/maintenance/gsc-position-4-20-opportunity-mining.md`, retaining current final 28-day evidence and 90-day context. Do not duplicate or weaken that playbook. Add effort, dependency, owner and a fixed measurement window to the implementation brief. Low click-through rate is a diagnostic lead, not proof that a title or description caused it. No Search Console rows is not proof of no rankings: retain anonymization, export and sampling caveats.

Service-city pages need actual coverage, distinct demand and substantive local evidence. Reject doorway multiplication, invented local facts and guaranteed ranking timelines. Visibility, leads, conversions and revenue remain separate outcomes. Public changes still require exact approval.

## 7. Source screening

The 2026-09-04 Sarvesh article advertises 20 prompts but its captured full body contains 12 identifiable audit/builders. Do not invent the missing prompts. Preserve source claims as claims. No model-potential percentages or 90-day ranking guarantees. Google guidance checked 2026-09-07 says complete/accurate information helps local visibility and more reviews/positive ratings can help ranking; it describes helpful replies as a way to stand out, not proof keyword-rich replies improve rank. Current post guidance says posts older than six months are archived unless a date range is set, not a blanket seven-day expiry.

Sources:
- https://x.com/bloggersarvesh/status/2095896040155340809
- https://x.com/i/article/2095839932980043776
- https://support.google.com/business/answer/7091?hl=en
- https://support.google.com/business/answer/7342169?hl=en

## Done condition

Deliver a sourced brief, observation ledger with explicit unknowns, correctly scoped review counts and a rights-aware photo plan when requested. No customer data enters the skill repository. No public changes, causal ranking assertions or fabricated metrics. Route website opportunities through the existing GSC playbook.
