---
title: Adversarial Multi-Agent Orchestration — Diverge, Judge, Synthesize, Red-Team
area: foundations
source_lessons: []  # process method distilled from running master-plan + funnel-rollout cascades
tools: []
---

# Adversarial Multi-Agent Orchestration — Diverge, Judge, Synthesize, Red-Team

**What it is.** The pipeline shape behind every "exhaustive / best-possible" SEO deliverable in this skill (`master_plan_cascade.mjs`, `funnel_rollout_cascade.mjs`). A single agent iterating on its own draft converges on a *local* answer and never catches its own number errors. An adversarial cascade — **diverge → judge → synthesize → red-team → finalize** — explores the solution space, then attacks the survivor until only reproducible, policy-safe claims remain. This playbook is the reusable method (and the failure modes that make it necessary).

**When to use.**
- The user wants the niche/plan "fully explored", "the best plan", "every angle", or an exhaustive deliverable.
- The output has load-bearing numbers a stakeholder will fund against (forecasts, addressable pools).
- Any time one-shot generation would produce a plausible-but-unverified plan.
- NOT for a quick keyword pull or a single-section answer — the cascade is ~16 agents / ~1M tokens; scale to the ask.

**The pipeline (six phases).**
1. **Foundation (parallel analysts).** 3–4 agents establish ground truth from the saved data BEFORE any strategy: clean clusters, a winnability/SERP-regime map, opportunity sizing, a competitor teardown (and, for a follow-on rollout, a *funnel map*). Each writes a structured artifact. Strategy built on un-grounded foundation inherits its errors.
2. **Diverge (N strategists, distinct LENSES).** Spawn ~5 strategists, each forced into a *different* philosophy (e.g. for a master plan: pSEO-maximalist · tool/product-led · visual/image-pack · local-domination · topical-authority/GEO; for a rollout: cashflow-first · moat-led · demand-ladder · brand/GEO-AIO · portfolio-kill-gates). Distinct lenses are the whole point — five agents with the *same* prompt give five near-identical drafts. Force structured output (a schema) so they're comparable.
3. **Judge (odd-sized panel, distinct lenses).** 3 judges, each a different scoring lens (defensibility/policy · funnel-coherence/conversion · feasibility/data). Each scores every strategy on fixed axes AND names the specific ideas to **STEAL** from the runners-up. The winner is rarely wholesale best — the value is the winning *spine* plus grafted best-ideas.
4. **Synthesize (one canonical doc).** One agent fuses the winning spine + the panel-mandated steals into a single document, written to an EXACT output path. Pass the strategies + judge verdicts inline (digested) so it has the material without re-deriving.
5. **Red-team (N adversaries, distinct lenses).** ~5 reviewers attack the synthesized doc, each a different failure mode: **numbers reconciliation · AIO/double-haircut · policy+graveyard(no-resurrection) · funnel/thesis coherence · sequencing/feasibility**. Each returns severity-tagged issues (must-fix/should-fix/nit) with the concrete fix and the offending line. This phase is where the real defects die.
6. **Finalize.** One agent applies every must-fix (rejecting wrong critiques with a one-line reason), and appends a transparent **"What the red-team changed"** changelog. Ship that.

**Why this beats one-shot or single-agent-iterated.**
- Divergence covers solution space a single chain skips; judging extracts the best of all attempts; red-team lenses catch errors the author is blind to. In a real run the red-team caught a **10× forecast slip** (`6,000 × 0.275 × 0.08 = 132`, not the published 1,320 → orders off by 10×) the synthesis agent had confidently shipped — a single iterating agent never finds its own arithmetic error.

**Failure modes this method exists to catch (each became a red-team lens).**
- **Fabricated/drifted aggregates** → numbers lens recomputes from source (see [[number-reconciliation]]).
- **Forecast arithmetic slips** → the "sessions × CTR × conversion" chain must actually multiply out; verify it.
- **Double-applied AIO haircut** → applied in `forecast.py`'s effective CTR AND again by hand halves the number twice (see [[ai-overviews-and-serp-features]]).
- **Resurrected killed ideas** → a fresh agent re-proposes something an earlier red-team killed; the graveyard guard blocks it.
- **Vanity volume / win-mechanism mismatch** → big informational pools booked as click revenue; thin text pages aimed at image-pack/AIO SERPs (see [[winnability-and-serp-regimes]]).
- **Hand-wavy funnel coherence** → upper-funnel plays with no concrete down-funnel path; the coherence lens forces a measurable handoff or cuts the play.

**Operational nuances (learned the hard way).**
- **Scout-then-pipeline.** Pull all external data (Ahrefs/SERP) yourself in ONE sequential process first; never fan parallel agents at a rate-limited API (Cloudflare throttles). The cascade reads SAVED files only.
- **Ground every agent.** Pass the canonical artifacts inline as a digest AND give file paths; tell agents to Bash-aggregate the CSV and cite real numbers — never recall another agent's prose figure.
- **Structured schemas for comparability.** Strategists/judges/reviewers return JSON schemas so synthesis and finalize can mechanically compare and merge.
- **Resilience: background workflows die silently on sandbox suspend.** A long cascade (~25–30 min) can be killed mid-run by a host suspend — the task vanishes and no completion notification arrives (tell-tale: a large clock jump in file mtimes + a dangling "started" with no "result" in the journal). Recover with `Workflow({scriptPath, resumeFromRunId})` — the unchanged agent() prefix returns cached results instantly and it continues from the first incomplete agent. Stop the dead task first if it's still tracked.
- **Verify the output FILE, not just the return value.** Synthesis/finalize agents sometimes write to a *renamed* path or return the markdown as text without writing. After the run, confirm the exact `outFile` exists and contains the red-team changelog; if not, locate the renamed file or re-run finalize.
- **Cost-scale to the ask.** 3 strategists + 1 judge for "good enough"; 5 + 3 + 5 for "exhaustive". State the agent count before launching a big one.

**Decision criteria / heuristics.**
- Distinct lenses per phase, always — same prompt × N = wasted tokens.
- Odd-sized judge panel; require "steal from runners-up", not just "pick one".
- Every red-team issue carries a concrete fix + the offending line; finalize applies or rejects-with-reason.
- A figure not reproducible from source does not survive the numbers lens.
- Keep a transparent changelog — provenance is what makes the deliverable trustworthy.

**Pitfalls.**
- Five identical strategists (no lens divergence) → no real exploration.
- Skipping the red-team "because the synthesis looks polished" — polish hides arithmetic errors.
- Letting the synthesis agent invent the output filename (pin it; verify after).
- Treating a suspended/killed run as "still working" — check journal liveness, then resume.

**Related.** [[number-reconciliation]], [[ai-overviews-and-serp-features]], [[winnability-and-serp-regimes]], [[full-funnel-rollout]], [[seo-process-overview]]. Tooling: `scripts/master_plan_cascade.mjs`, `scripts/funnel_rollout_cascade.mjs`, `scripts/forecast.py`. Runbooks: `workflows/full-master-plan.md`, `workflows/full-funnel-rollout.md`.
