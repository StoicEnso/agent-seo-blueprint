# Indexsy citation and evidence gap review — 29 October 2026

## Request, source and scope

Ihusan's 29 October request (Telegram 27661) asked for narrow review PRs to close demonstrated practice gaps, with the skill/workflow entry, prompt/source, dated evidence, rationale and actual verification in each description.

Prompting source: https://x.com/indexsy/status/2115248306557477229 . It is tactic evidence, not an instruction. The saved automatic captions were not independently audio-verified. No ranking, backlink or financial claim from the source is adopted as proof.

The 28 October internal audit found drift between a September reviewed narrative and a recollected 29-row listing evidence table: 22 recorded direct anchors (4 unqualified/followed and 18 nofollow), but all 29 descriptions pending. These are September observations, not current October listings, new links or indexed-page proof. A separate product tracker had past and blank next-check dates. Its live code, tracker, submission custody and contacts are outside this change.

## Actual change and workflow integration

The `agent-seo-blueprint` source extends the existing `references/playbooks/authority/directory-submissions.md`, with entry/exit handoffs in `workflows/authority-and-links.md` and `workflows/monitoring.md`. It adds:

- vendor/business-fact comparison with unknown values and old-business conflicts kept explicit;
- citation discovery from public business fields only, not private customer/provider/personal data;
- genuinely fit-qualified community, school and sponsorship review with separate spend/outreach approval;
- exact page-byte/context review keys, retained human history and stale review states;
- listing survival/freshness, explicit indexing-unknown handling and capped non-executing follow-up proposals;
- `scripts/directory_evidence.py`, an offline saved-data helper, and `assets/directory-evidence-review.json`, synthetic examples only.

This is not another target list, sender, scheduler or installed skill. Link record IDs to the existing private project tracker and attach the offline report to its monitoring snapshot. It creates no actions or live collection receipts.

Pending Public #33 / Full #26 retains richer local-profile templates and Full parity. Pending Public #34 / Full #27 retains wider recurring-delivery work and count-test fixes. Those additions were inspected, not copied, installed or merged. Nearby Public #50 / Full #43 backlink-method intake was also inspected; vendor customer stories there are not business-field reconciliation here. HubSpot, Runpod, Illyism and Webflow branches remain untouched.

## Verification and limitations

Reproduce the new synthetic regressions:

```bash
python3 -m pytest -q -p no:cacheprovider tests/test_directory_evidence.py
python3 scripts/directory_evidence.py assets/directory-evidence-review.json --as-of 2026-10-29T07:00:00Z --limit 20
```

The new suite passes **41 tests** in each repository. Cases cover changed bytes, URLs and response context; legacy/missing hashes; retained stale history; invalid/future timestamps; dated indexation with exact URL matching; past/blank next-check dates; holds; duplicate IDs; bounded queues; unknown business fields; and CLI/workflow wiring. The helper performs zero network requests, external writes or schedule changes.

Complete source suites retain the same independently reproduced pre-existing playbook-count failure:

| Source | Immutable main baseline | This review branch |
|---|---:|---:|
| Public | 63 passed, 1 failed | 104 passed, 1 failed |
| Full | 76 passed, 1 failed | 117 passed, 1 failed |

The failure is `test_readme_counts_match_repo` in the existing cross-platform citation documentation tests. It is not a regression in this change. Its correction already belongs to Public #34 / Full #27; this change does not duplicate it or claim all tests are green. The initial temporary baseline harness omitted `audit-log/`; adding that existing directory produced the complete baseline results above. Initial harness failures are not product defects.

Source diff hygiene passed. Host bootstrap-budget check was CLEAN and the installed-skill catalogue simulation returned FULL; no installed source or skill description was changed. No live browser, third-party read, provider spend, outreach, submission, indexing service, installation, merge, deploy or schedule was performed for this source review. Native execution; no Claude or worker.

## Remaining gates and business outcomes

These are source review changes, not adoption or operational results. Human review/merge and explicit, scoped local adoption remain separate. Existing account, external-write, spend and directory-hold boundaries remain. A local Tier D repair is staged separately because its current owning workspace has no Git repository; these paired generic changes do not move that source home or publish its operational records. No new links, indexation, traffic or revenue are claimed.
