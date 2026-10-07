---
title: Technical SEO Maintenance
goal: Turn technical SEO into a recurring operating habit: detect plumbing issues early, write prioritized fixes, and suggest a cron cadence when none exists.
playbooks:
  - references/playbooks/maintenance/technical-seo-maintenance.md
  - references/playbooks/maintenance/measuring-seo-results.md
  - references/playbooks/content/on-page-optimization.md
  - references/playbooks/content/image-search-optimization.md
  - references/playbooks/content/schema-types-reference.md
  - references/playbooks/content/content-what-not-to-do.md
references:
  - references/integrations/cwv-thresholds.md
  - references/integrations/pagespeed.md
  - references/integrations/gsc.md
scripts:
  - scripts/workspace.py
  - scripts/pagespeed_run.py
  - scripts/gsc_pull.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [pagespeed, gsc, serp]
outputs:
  - audits/<date>_sitemap-cohort-evidence.csv  # optional material sitemap question; same linked workspace evidence
  - audits/<date>_technical-seo-audit.md
  - audits/<date>_technical-seo-audit-findings.json
  - monitoring/<date>_technical-seo-cron-check.md
---

# Technical SEO Maintenance

**When to run this.** A site is live, has indexed or soon-to-index pages, ships content/templates regularly, or the user asks for technical SEO audits, schema, Core Web Vitals, GSC diagnostics, or recurring SEO hygiene. This is the "plumbing compounds" workflow: small verified fixes every week beat giant occasional audits.

**Prerequisites.**
- **Workspace** resolved (`python3 scripts/workspace.py status --path <DIR>`; ask before creating if absent). Domain(s) should be in `project.json`.
- **Access:** PageSpeed works without setup; GSC is ideal if creds/browser access exists; otherwise use public checks + `site:`/SERP sampling.
- **Safety:** This workflow is read-only by default. It may create reports and propose recurring scheduler jobs. It never edits the live site or creates/changes schedules without explicit user confirmation.

## Steps

1. **Load the maintenance playbook.** Read `references/playbooks/maintenance/technical-seo-maintenance.md`. Keep this focused: the output is a ranked fix list, not a sprawling SEO essay.

2. **Check whether a recurring cadence already exists.** Inspect both:
   - the workspace `project.json` for `monitoring.*` or `technical_seo.*`, and
   - recurring jobs available in the current agent harness/runtime for this project/domain/workspace name.

   If a suitable active recurring job exists, record its name/cadence in `monitoring/<date>_technical-seo-schedule-check.md` and do **not** suggest a duplicate. If the site is live/indexable and no suitable job exists, proactively recommend a recurring schedule before finishing. Suggested default:

   - **Weekly light technical SEO audit** — GSC/PageSpeed/schema/indexation/template checks; notify only on critical/high findings or auth/data blockers.
   - **Monthly trend review** — connect fixes to GSC/GA4 movement.
   - **Quarterly strategy review** — leading indicators vs trailing outcomes.

   Do not create the recurring job yet unless the user confirms.

3. **Select a bounded URL sample.** Include:
   - homepage and key money pages,
   - top GSC pages by impressions/clicks if available,
   - newly published pages/templates,
   - representative programmatic/marketplace item pages,
   - pages with recent ranking/CTR drops.

4. **Pull GSC and performance evidence.**
   - GSC: clicks, impressions, CTR, average position, top queries/pages, query coverage drops, pages where impressions hold but clicks/position fall.
   - PageSpeed/CWV: run `pagespeed_run.py` for the sample; use CrUX field data where present; classify LCP/INP/CLS by `cwv-thresholds.md`.

5. **Run the weekly technical checklist.** For each sampled URL/template, check:
   - indexability: robots, noindex, canonical, sitemap inclusion, crawl depth;
   - duplicates: duplicate titles/descriptions, duplicate/invalid schema, near-duplicate pages, faceted/parameter URLs;
   - redirects: http→https→www chains, loops, stale internal links;
   - rendering: key content/schema visible in initial HTML where practical, hydration/JS-only risks, content parity mobile vs desktop;
   - titles/meta: missing, duplicated, misleading, or truncated past sensible SERP length;
   - structured data: appropriate schema for articles/products/FAQ/breadcrumb/org, valid JSON-LD, no stale rich-result assumptions;
   - links/media: broken internal/outbound links, orphaned pages, oversized images, missing important alt text, layout-shift media; for image-led/visual-intent templates, apply `image-search-optimization.md` to discovery, stable URLs, responsive delivery, LCP handling, sitemap need, and conditional rights metadata;
   - trust/security basics: HTTPS/mixed content, exposed secrets/debug dumps, missing commercial trust pages where expected.

6. **Turn findings into a small weekly fix backlog.** Prefer "fix 10 small things" over vague advice. Each finding needs:
   - severity (`critical | high | medium | low`),
   - area (`technical | indexation | schema | performance | rendering | metadata | internal-links | trust`),
   - evidence (URL, metric, snippet, screenshot/report path),
   - recommended fix,
   - owner lane (`engineering`, `content`, `analytics`, `authority`, `manual-review`).

7. **Emit artifacts.** Save raw findings JSON, then run:
   `python3 scripts/report.py audit --workspace <DIR> --title "Technical SEO audit: <domain>" --data <findings.json>`
   Rename/copy the resulting report if needed to `audits/<date>_technical-seo-audit.md`; save raw payload as `audits/<date>_technical-seo-audit-findings.json`.

8. **Recommend scheduling when missing.** If step 2 found no recurring job and the site is suitable, end with a concrete setup ask:
   - recommended cadence,
   - what data sources will be used,
   - what will be reported vs silently logged,
   - stop/disable condition,
   - owner of fixes.

   Only after the user says yes, create the recurring job using the host harness's scheduler. The job instructions should tell the agent to run this workflow for the exact workspace/domain, write artifacts, avoid noisy notifications, and surface only critical/high findings or blockers.

## Decision points

- **No GSC/GA4 access:** continue with public/PageSpeed/schema/indexation checks and mark GSC/GA4 as a data-access blocker, not a workflow failure.
- **Tiny/new site:** use a monthly audit until content volume justifies weekly; still recommend weekly only if pages ship frequently.
- **Programmatic/marketplace site:** weekly is the default because template, canonical, schema, and duplicate-content mistakes compound quickly.
- **Critical indexing/security issue:** notify immediately and route to the owner lane; do not bury it in a monthly report.
- **Low-only findings:** write to workspace and summarize briefly; don't spam the user.

**Done when.** A bounded technical audit artifact exists, high/critical fixes are clearly ranked, and the recurring cadence posture is explicit: existing cron reused, new cron proposed, or scheduling intentionally skipped with reason.

## Sitemap cohort evidence pass

For a material indexation question, use the existing technical-maintenance pass to create a bounded cohort record in a workspace copy of `assets/sitemap-cohort-evidence.csv`; this is an offline evidence contract, not a collector, GSC write, or indexing guarantee. Inventory the served sitemap index and leaf sitemaps, logical page/template/content/date cohorts, chosen GSC property, canonical eligibility, deliberate exclusions, last read/processing state, and the route used to inspect them. A valid sitemap index remains a supported submission mechanism.

Keep states separate: served sitemap, submitted sitemap, parsed/discovered URL, crawled URL, and indexed canonical URL are not interchangeable. Preserve `unknown`, `missing`, and `partial` states. Do not sum overlapping index and child rows, use incomplete up-to-1,000 URL examples as a census, or compute ratios across different windows or memberships. Inspect representative URLs with cached-versus-live source/render/canonical/robots/noindex evidence; one coverage status alone does not diagnose quality, traffic, crawl budget, or a template fault.

If a child sitemap might improve reporting, inspect the actual current property/filter first. Reuse a usable exact child/index filter; its availability is not a reason for another submission. For an evidenced gap, prepare a conditional proposal with purpose, exact URL, risks, rollback and follow-up. Execute only under owner-approved GSC write authority after a fresh scope/target check, then record the actual receipt. Never submit all children by default, repeat validation, or promise crawling/indexing.


### Bounded operating pass

1. Resolve the existing workspace with `python3 scripts/workspace.py status --path <DIR>`; ask before creating one. Preserve existing scoped approvals and holds; this flow widens no access and releases no hold. Copy the empty template to `audits/<date>_sitemap-cohort-evidence.csv`. Never put client observations into the repository template. Link it from the ordinary audit findings and coverage row; it is raw-source authoritative, not a new `report.py` renderer.
2. Inventory only the relevant existing indexes/leaf sitemaps and logical template/content/date cohorts. Preserve exact property type/host/protocol/path, parent/leaf relation, served/processing states, submission or index/robots discovery route, last read and membership source/version. Do not create nested indexes or split every shard without a useful reporting question.
3. Inspect the actual Sitemaps detail and Page Indexing selector with existing authorised read access. Distinguish `All known pages`, `All submitted pages`, `Unsubmitted pages` and the specific sitemap/index filter. Record availability; missing access or a missing dropdown is not zero indexation. Sitemaps top-level listing and Page Indexing membership have different rules.
4. Capture counts by explicit metric/reason/unit plus source timestamp and reporting window. Retain limits: 1,000 displayed submitted requests need not be all submissions; up-to-1,000 URL examples may be incomplete even below that limit. Do not sum overlapping parent/child observations or derive ratios from mismatched windows/memberships.
5. Inspect bounded affected and comparison URLs, retaining cached-versus-live source/render/canonical/robots/noindex evidence, legitimate exclusions, sample size, alternatives and confidence. Pause only the action needing inadequate evidence; independent safe inspection can continue. The helper `gsc_pull.py` remains a stub, not a new cohort collector.
6. Reuse a working filter/index or prepare the exact bounded fix/reporting proposal. Record owner, current approval scope and planned rollback separately from the later execution receipt. Do not turn a proposed action into an approved, applied or verified one. Submission, deletion, Validate fix, request indexing, file/robots changes and new recurring jobs require their own authority; this pass grants none.
7. Save the evidence CSV and linked packets; route actual site fixes to the owning workflow. If separately authorised execution later occurs, verify its receipt, subsequent processing/filter availability and comparable cohort observations at the stated follow-up. A submission acknowledgment or successful processing is not crawling/indexation. Keep absent data and unresolved hypotheses explicit.

**Done when this branch is applicable:** the workspace evidence is saved, source/metric/state and current filter are inspectable, overlap and canonical exclusions are handled, inspection/alternatives are bounded, and the next action is reuse, a reviewable proposal or an explicit data gap. No live write is required to complete the read-only pass. If inapplicable, record the reason in the existing coverage ledger.
