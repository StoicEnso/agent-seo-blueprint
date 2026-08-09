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
