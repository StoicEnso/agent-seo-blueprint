# Recurring work ledger

One row per reviewed work item. This is a raw, human-reviewable source artifact. Do not report it as renderer-supported by `scripts/report.py`.

| ID | Trigger/cadence | Route | State | Fact + provenance | Collection/data limit | Business/release/conversion context | Hypothesis / alternatives / confidence reason | Priority reason | Owner + approval | Proposed exact diff/revision | Risk + rollback | Receipt | Outcome/recheck + date | Carry/defer/reject reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| example-keep-as-template | weekly/manual | `workflows/monitoring.md` | proposed | `UNKNOWN`; no measured input yet | `MISSING_ACCESS`; do not treat as zero | offer, release and conversion path unknown | no diagnosis; alternatives and confidence not yet established | no priority until evidence exists | owner: unassigned; approval: none | none | no write; no rollback needed | none | obtain bounded source and recheck | template only |

Allowed states: `proposed`, `drafted`, `approved`, `applied`, `verified`, `deferred`, `rejected`. Record `OBSERVED`, `PROVIDER_ESTIMATE`, `MODELLED`, or `UNKNOWN` for numbers. Approval does not imply application; application does not imply verification or success.

Use stable IDs and link existing detailed artifacts. Keep evidence of implementation separate from later outcome evidence. A blank or unknown field must not be replaced by a guessed value.
