---
title: Monitoring
goal: Track ordinary search, bounded Google AI visibility, current GSC opportunities, and business outcomes — on-demand or scheduled.
playbooks:
  - references/playbooks/maintenance/measuring-seo-results.md
  - references/playbooks/maintenance/staying-ahead-with-backlinks.md
  - references/playbooks/maintenance/navigating-google-updates.md
  - references/playbooks/maintenance/keyword-intent-evolution.md
  - references/playbooks/maintenance/gsc-position-4-20-opportunity-mining.md
  - references/playbooks/maintenance/seo-operational-checklist.md
  - references/playbooks/maintenance/google-generative-ai-visibility.md
  - references/playbooks/maintenance/cloudflare-agent-readiness-and-aeo.md
  - references/playbooks/maintenance/cross-platform-ai-citation-loop.md
  - references/playbooks/foundations/seo-process-overview.md
scripts:
  - scripts/workspace.py
  - scripts/gsc_pull.py
  - scripts/ga4_pull.py
  - scripts/ahrefs_client.py
  - scripts/dataforseo_client.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [gsc, ga4, ahrefs, dataforseo, serp]
outputs:
  - monitoring/<date>_snapshot.md          # rank/traffic snapshot (via report.py monitoring)
  - monitoring/<date>_leading-indicators.json  # the 6 action-task checklist
  - monitoring/<date>_snapshot.json         # raw ordinary-search snapshot payload
  - monitoring/<date>_gsc-4-20-opportunities.json # current, verified quick-win/recovery rows
  - monitoring/<date>_google-ai-visibility.json # optional Google AI impression snapshot
  - monitoring/<date>_cloudflare-agent-aeo.json # optional Cloudflare readiness, synthetic panel, and operator snapshot
  - monitoring/<date>_ai-citation-observations.json # optional non-Google provider citation snapshot
  - monitoring/<date>_ai-discovery-self-report.json # optional signup/lead discovery survey snapshot
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

   **Optional Google AI visibility layer.** When the property exposes Search Console's Generative AI performance report, load `references/playbooks/maintenance/google-generative-ai-visibility.md`. Capture impression-only views by canonical page, country, date, and device into `monitoring/<date>_google-ai-visibility.json`; record the inclusion-control state without changing it. Keep this dataset separate from ordinary Search clicks/CTR/position. Report absence as rollout/access ambiguity, not zero visibility.

   **Optional Cloudflare agent/AEO layer.** When the site uses Cloudflare and the dashboard evidence is in scope, load `references/playbooks/maintenance/cloudflare-agent-readiness-and-aeo.md`. Save Agent Readiness checks, the precomputed synthetic AEO category/model panel, and first-party AI Operator Activity as separate sections in `monitoring/<date>_cloudflare-agent-aeo.json`. Preserve access state, snapshot/model/category metadata, and limitations. Do not blend its scores with GSC/GA4 or infer user-query impressions, clicks, revenue, or causality.

   **Optional cross-platform citation layer.** When the workspace tracks a fixed buyer-question set for ChatGPT, Microsoft Copilot, Perplexity, Claude, or another named provider, load `references/playbooks/maintenance/cross-platform-ai-citation-loop.md`. Re-run the same question versions modestly, save dated provider/surface/locale/account-state observations to `monitoring/<date>_ai-citation-observations.json`, and keep mentions/citations separate from ordinary Search metrics, Google AI impressions, and Cloudflare evidence.

   Preserve `first_seen_at`, `last_seen_at`, `consecutive_runs_seen`, `dropped_on`, the full observation history, and missed checks when citation persistence is in scope. Report observed duration only. Do not assume a fixed citation half-life, exact disappearance date between sparse checks, or provider-wide refresh cadence.

   **Optional self-reported discovery layer.** When the business already asks or approves testing “How did you hear about us?”, save the exact question/options, form location, dates, response denominator, non-response, normalized source, and raw answer to `monitoring/<date>_ai-discovery-self-report.json`. Compare it with referrals and conversions as a separate directional signal. Do not multiply the response share into hidden traffic, view-through conversions, or causal revenue.

4. **Mine current GSC positions 4–20.** Load `references/playbooks/maintenance/gsc-position-4-20-opportunity-mining.md`. Use the latest final 28-day query+page rows, reject stale/irrelevant/intent-mismatched candidates, and inspect the live page/SERP before recommending a narrow change. Keep 90-day-only rows as recovery context unless current data confirms them. Save valid, rejected, and recovery-only rows to `monitoring/<date>_gsc-4-20-opportunities.json` and route implementation briefs to `content-production.md`.

5. **Track the six leading indicators (the work).** From `measuring-seo-results.md`, log the action-task checklist for the period: (1) content shipped, (2) new keywords/content targeted, (3) existing pages optimized, (4) link opportunities identified + contacted, (5) backlinks acquired, (6) competitor backlinks tracked. Save to `monitoring/<date>_leading-indicators.json`. These are checked weekly; the user fills them or the agent reads them from the workspace (briefs shipped, drafts sent in `outreach/`, etc.).

6. **Benchmark competitor backlink pace.** Load `references/playbooks/maintenance/staying-ahead-with-backlinks.md`. In Ahrefs (`ahrefs_client.py`), for you + the top 3–5 competitors run the filtered query: DR > ~25, one link per domain, "new" in the last 30 days. Count unique new referring domains (and high-DR wins separately). If you're below a competitor's pace, that's a leading indicator of future ranking loss → flag "increase outreach" and route to `authority-and-links.md`.

7. **Respond to movement (diagnose before acting).** Load `references/playbooks/maintenance/navigating-google-updates.md` and `references/playbooks/maintenance/keyword-intent-evolution.md`:
   - **New content bouncing wildly** → settling phase (~3–6 months for a new domain); don't over-react.
   - **Drop coinciding with a confirmed Google update** → content-quality/value reassessment; improve genuine helpfulness, not tricks. Annotate the update date.
   - **Drop with no update** → check intent/format shift first: capture the live SERP (`serp_capture.py`), see if the rewarded format changed; if so, the fix is reformatting the page (route to `content-production.md`). Confirm with GSC that impressions hold while clicks/position fall (losing to a better-fit format, not losing demand).
   - **Below competitors on links** → ramp outreach (`authority-and-links.md`).

8. **Emit the snapshot + run the review.** Assemble `{site, period, metrics:{clicks,impressions,avg_position,sessions,...}, keywords:[{keyword,position,change}], notes}` and run `python3 scripts/report.py monitoring --workspace <DIR> --data <snapshot.json>` → `monitoring/<date>_snapshot.md`. Save the raw payload too. On the configured cadence: **monthly** review the trend; **quarterly** tie the leading indicators (step 5) to the trailing results (step 3) — did the inputs translate into rankings/traffic? If inputs were done consistently and rankings still flat after a quarter, dig into the trailing data for a diagnosis.

9. **Re-test operational regressions and opportunities.** Load `references/playbooks/maintenance/seo-operational-checklist.md` and re-check the prior audit's failed/partial rows that can change over time: traffic/ranking declines, page-two opportunities, high-impression/low-CTR pages, sitemap processing, robots/noindex, truthful freshness signals, broken links, CWV, schema validation, and branded/site SERP anomalies. Use GSC for indexation; treat `site:` checks as directional only. Append status changes and evidence to the current snapshot rather than rerunning all 37 checks blindly.

10. **Interpret Google AI visibility without overclaiming.** When step 3 produced an AI snapshot, map visible canonical pages to journey roles (problem, use case, product, pricing, comparison, trust, case study, implementation). Flag gaps only when demand, business value, non-duplication, and live evidence justify a useful page. Correlate impressions separately with ordinary GSC, analytics, leads, and revenue; never infer AI clicks, CTR, or causality from impression-only data.

11. **Interpret cross-platform citation observations without overclaiming.** When step 3 produced a provider citation snapshot, compare brand mention presence, owned versus third-party cited domains, newly cited or dropped URLs, and page-role coverage by provider. Correlate those observations separately with referrals, sessions, leads, assisted conversions, transactions, and revenue; never convert citation observations into impressions, clicks, CTR, conversions, or causal proof.

**Decision points.**
- **Cadence** (asked at setup): weekly inputs / monthly outputs / quarterly analysis is the recommended default — but the user chooses.
- **On-demand vs scheduled** → run now (steps 3–7) vs register via `schedule`/`loop` (user-confirmed).
- **Movement diagnosis:** settling vs update vs intent shift vs competitor links → routes to different responses (above). Diagnose before acting; don't gut a page over a one-week wobble.
- **Cloudflare evidence available?** Keep readiness checks, synthetic AEO panel metrics, and first-party operator traffic separate; unavailable early access is not zero visibility.
- **Cross-platform citation monitoring?** Only when the question set is fixed and the provider/surface is explicit; never blend it into Google or Cloudflare reporting.
- **Judge inputs weekly, outcomes quarterly** — don't treat the weekly dashboard as the success verdict.

**Outputs.**
- `monitoring/<date>_snapshot.md` — rank/traffic snapshot table (from `report.py`).
- `monitoring/<date>_leading-indicators.json` — the six action-task checklist for the period.
- `monitoring/<date>_snapshot.json` — raw ordinary-search payload for trend diffing.
- `monitoring/<date>_gsc-4-20-opportunities.json` — current valid opportunities plus rejected/recovery-only rows.
- `monitoring/<date>_google-ai-visibility.json` — optional impression-only Google AI snapshot with explicit limitations.
- `monitoring/<date>_cloudflare-agent-aeo.json` — optional Cloudflare snapshot with readiness, synthetic panel, and operator-activity lanes kept separate.
- `monitoring/<date>_ai-citation-observations.json` — optional provider-specific citation observation snapshot with explicit metric limitations.
- `monitoring/<date>_ai-discovery-self-report.json` — optional first-party discovery-survey snapshot with wording, denominator, non-response, and attribution limitations.

**Done when.** A snapshot + leading-indicator log are written for the period, operational regressions/opportunities have evidence-backed status changes, any ranking movement has been diagnosed (settling / update / intent / links) with the right follow-up routed, and — if scheduled — the recurring routine is registered at the user-confirmed cadence. If the Google AI report was available, its separate impression snapshot, inclusion-control state, limitations, and journey-role interpretation are also recorded. If Cloudflare evidence was in scope, its readiness, synthetic panel, and first-party operator lanes are preserved separately with access state and limitations. If cross-platform citation monitoring was in scope, its provider-specific observation snapshot, persistence history, and limitations are recorded separately. If self-reported discovery was in scope, wording, denominator, non-response, and limitations are preserved outside click attribution. The quarterly review explicitly answers "did the work pay off?" by connecting inputs to outcomes without treating AI impressions, vendor panel scores, citation observations, or survey answers as hidden clicks or causal revenue.
