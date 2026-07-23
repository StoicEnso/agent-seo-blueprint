---
title: Monitoring
goal: Track rank/traffic snapshots, respond to Google updates, and prove whether the SEO work paid off — on-demand or scheduled.
playbooks:
  - references/playbooks/maintenance/measuring-seo-results.md
  - references/playbooks/maintenance/staying-ahead-with-backlinks.md
  - references/playbooks/maintenance/navigating-google-updates.md
  - references/playbooks/maintenance/keyword-intent-evolution.md
  - references/playbooks/maintenance/seo-operational-checklist.md
  - references/playbooks/foundations/seo-process-overview.md
scripts:
  - scripts/workspace.py
  - scripts/gsc_pull.py
  - scripts/ga4_pull.py
  - scripts/ahrefs_client.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [gsc, ga4, ahrefs, serp]
outputs:
  - monitoring/<date>_snapshot.md          # rank/traffic snapshot (via report.py monitoring)
  - monitoring/<date>_leading-indicators.json  # the 6 action-task checklist
  - monitoring/<date>_snapshot.json         # raw snapshot payload
---

# Monitoring

**When to run this.** A site has live, ranking (or settling) content and the user wants ongoing maintenance: periodic rank/traffic snapshots, a quick read after a Google update, or a "did our work pay off" review. Stage 4 of the loop — it never ends. Runs **on-demand** OR on a **schedule** the user chooses at setup.

**Prerequisites.**
- **Workspace** resolved (`python3 scripts/workspace.py status --path <DIR>`; ASK before creating if absent). Tracked keywords + cadence live under `monitoring` in `project.json`.
- **From the user (asked at setup):** the cadence (see step 1), the most important keywords/pages to track, and the top 3–5 competitors to benchmark against.
- **Data sources:** Google Search Console (`gsc_pull.py`) for impressions/clicks/avg-position/per-keyword movement; GA4 (`ga4_pull.py`) for organic sessions/engagement/conversions; Ahrefs (`ahrefs_client.py`) for competitor backlink pace; live SERP (`serp_capture.py`) for intent/format checks. Browser fallbacks in `references/integrations/<src>.md`. GSC/GA4 OAuth is done by the user; the skill guides, never auto-auths.

**Steps.**

1. **At setup, ASK the cadence and configure.** Load `references/playbooks/maintenance/measuring-seo-results.md` — it recommends: **inputs weekly, outputs reviewed monthly, full leading-vs-trailing analysis quarterly.** Recommend that rhythm, then ask the user to confirm a cadence. Record it in `project.json` (`monitoring.enabled`, `monitoring.cadence`, `monitoring.tracked_keywords`) via the workspace config.
   - **On-demand:** just run steps 3–7 now.
   - **Scheduled:** wire a recurring run. For an in-session recurring poll, use the **`loop`** skill (e.g. a weekly check). For a true cron-style remote agent, use the **`schedule`** skill to register a routine that re-invokes this workflow at the chosen cadence. Confirm the schedule with the user before creating it.

2. **(Scheduled only) Register the routine.** Hand the chosen cadence to the `schedule` skill (cron) or `loop` skill (interval). The routine's job each run = "execute workflows/monitoring.md steps 3–7 for <workspace>" and surface the snapshot. Creating/altering a schedule is a user-confirmed action.

3. **Capture the rank/traffic snapshot (trailing indicators).** Pull from GSC (`gsc_pull.py`): clicks, impressions, average position, and per-keyword movement for the tracked keywords/pages. Pull from GA4 (`ga4_pull.py`): organic sessions, engagement, conversions. This is the trailing data — informative but lagging.

4. **Track the six leading indicators (the work).** From `measuring-seo-results.md`, log the action-task checklist for the period: (1) content shipped, (2) new keywords/content targeted, (3) existing pages optimized, (4) link opportunities identified + contacted, (5) backlinks acquired, (6) competitor backlinks tracked. Save to `monitoring/<date>_leading-indicators.json`. These are checked weekly; the user fills them or the agent reads them from the workspace (briefs shipped, drafts sent in `outreach/`, etc.).

5. **Benchmark competitor backlink pace.** Load `references/playbooks/maintenance/staying-ahead-with-backlinks.md`. In Ahrefs (`ahrefs_client.py`), for you + the top 3–5 competitors run the filtered query: DR > ~25, one link per domain, "new" in the last 30 days. Count unique new referring domains (and high-DR wins separately). If you're below a competitor's pace, that's a leading indicator of future ranking loss → flag "increase outreach" and route to `authority-and-links.md`.

6. **Respond to movement (diagnose before acting).** Load `references/playbooks/maintenance/navigating-google-updates.md` and `references/playbooks/maintenance/keyword-intent-evolution.md`:
   - **New content bouncing wildly** → settling phase (~3–6 months for a new domain); don't over-react.
   - **Drop coinciding with a confirmed Google update** → content-quality/value reassessment; improve genuine helpfulness, not tricks. Annotate the update date.
   - **Drop with no update** → check intent/format shift first: capture the live SERP (`serp_capture.py`), see if the rewarded format changed; if so, the fix is reformatting the page (route to `content-production.md`). Confirm with GSC that impressions hold while clicks/position fall (losing to a better-fit format, not losing demand).
   - **Below competitors on links** → ramp outreach (`authority-and-links.md`).

7. **Emit the snapshot + run the review.** Assemble `{site, period, metrics:{clicks,impressions,avg_position,sessions,...}, keywords:[{keyword,position,change}], notes}` and run `python3 scripts/report.py monitoring --workspace <DIR> --data <snapshot.json>` → `monitoring/<date>_snapshot.md`. Save the raw payload too. On the configured cadence: **monthly** review the trend; **quarterly** tie the leading indicators (step 4) to the trailing results (step 3) — did the inputs translate into rankings/traffic? If inputs were done consistently and rankings still flat after a quarter, dig into the trailing data for a diagnosis.

8. **Re-test operational regressions and opportunities.** Load `references/playbooks/maintenance/seo-operational-checklist.md` and re-check the prior audit's failed/partial rows that can change over time: traffic/ranking declines, page-two opportunities, high-impression/low-CTR pages, sitemap processing, robots/noindex, truthful freshness signals, broken links, CWV, schema validation, and branded/site SERP anomalies. Use GSC for indexation; treat `site:` checks as directional only. Append status changes and evidence to the current snapshot rather than rerunning all 37 checks blindly.

**Decision points.**
- **Cadence** (asked at setup): weekly inputs / monthly outputs / quarterly analysis is the recommended default — but the user chooses.
- **On-demand vs scheduled** → run now (steps 3–7) vs register via `schedule`/`loop` (user-confirmed).
- **Movement diagnosis:** settling vs update vs intent shift vs competitor links → routes to different responses (above). Diagnose before acting; don't gut a page over a one-week wobble.
- **Judge inputs weekly, outcomes quarterly** — don't treat the weekly dashboard as the success verdict.

**Outputs.**
- `monitoring/<date>_snapshot.md` — rank/traffic snapshot table (from `report.py`).
- `monitoring/<date>_leading-indicators.json` — the six action-task checklist for the period.
- `monitoring/<date>_snapshot.json` — raw payload for trend diffing.

**Done when.** A snapshot + leading-indicator log are written for the period, operational regressions/opportunities have evidence-backed status changes, any ranking movement has been diagnosed (settling / update / intent / links) with the right follow-up routed, and — if scheduled — the recurring routine is registered at the user-confirmed cadence. The quarterly review explicitly answers "did the work pay off?" by connecting inputs to outcomes.
