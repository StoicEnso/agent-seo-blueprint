# Commercial-query filter source adaptation — 21 October 2026

Source: an owner-supplied screenshot attributed to Hridoy Reh (@hridoyreh). No original post URL or publication date was visible; none is invented. The original screenshot remains in the owner's private archive, not redistributed here.

Accepted: use current first-party query evidence to discover terms worth reviewing. Correct missing regex alternatives and retain an unfiltered control. Add a deterministic, offline review tool with synthetic examples and tests, not a second collector or website writer.

Rejected: “forced Google”, 14,500 visitors as a verified unique-user count, guaranteed growth, treating a regex hit as proven commercial intent, and automatically creating pages or rewriting snippets. The screenshot shows search clicks over 12 months, not causal proof. No live project query rows or credentials are included.

Novelty check: existing main already covers search intent, GSC 4–20 opportunities and content-opportunity measurement. Open weekly-action and zero-click PRs cover related queues but not missing-separator detection, source-versus-corrected modifier matching, explicit nonmatching controls or unknown-safe row comparisons. This addition extends those methods; it does not duplicate their execution paths or pull them in as dependencies.

Evidence: Google's current Search Analytics API documents RE2 filters, final data, inclusive Pacific dates, aggregation and internal top-row limits. The standard Search performance help documents clicks and chart/table aggregation. Both were checked on 21 October 2026. A bounded private application verified Google accepts the corrected expression; private project metrics are intentionally absent from this public source addition.

Implementation: references/gsc-commercial-query-triage.md, scripts/gsc_commercial_queries.py, assets/gsc-commercial-query-example.json, tests/test_gsc_commercial_queries.py; routed from SKILL, README, monitoring, GSC integration and the existing GSC opportunity playbook. The analyzer has no network, auth or website side effects. No installed skill, site, account, schedule or production state was changed.
