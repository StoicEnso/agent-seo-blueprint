---
title: Full-Funnel Rollout — Sequencing BOFU → MOFU → TOFU So Each Stage Funnels Down
area: content
source_lessons: []  # method distilled from the Aurelet full-funnel rollout cascade
tools: [ahrefs, serp]
---

# Full-Funnel Rollout — Sequencing BOFU → MOFU → TOFU So Each Stage Funnels Down

**What it is.** Once a master plan exists, the operational question is *in what order do we build the funnel, and how does each upper stage pay back into the money page?* This playbook is the method for the **BOFU → MOFU → TOFU rollout**: the defensible definition of each stage, the wave/kill-gate sequencing, the down-funnel handoff "plumbing", and — critically — how to "roll out the full funnel" WITHOUT reverting to the scaled-content TOFU gamble a good master plan already killed.

**The core reconciliation: "roll out TOFU" vs "TOFU-for-its-own-sake is dead".** Both are true. Raw informational/volume TOFU (name lists, "ideas" oceans, how-to heads) is ~80% AI-Overview-saturated, has no buyer intent, and is scaled-content/doorway risk — it stays dead as a *click/revenue* play. But TOFU re-enters legitimately in exactly three forms, **built last, capped, EEAT-gated, never a revenue line, each with a concrete path DOWN to the money page**:
1. **AIO-safe HOSTED artifacts/tools** the user actually wants (a generator, a calculator, a real library) — not a thin article about the topic.
2. **Brand + LLM-citation / share-of-AI-voice** building — measured as *reach/assist*, the durable upper-funnel play in an AIO world.
3. **Genuine link bait** — original data, a tool, a teardown that earns the refdomains the BOFU pages need.
If an upper-funnel idea fits none of these, or has no measurable down-funnel handoff, it does not ship. "Builds awareness" is not a plan.

**The defensible definition of each stage.**
- **BOFU — the cash engine (PRIMARY REVENUE).** The money pages on transactional/commercial buyer terms, won on page authority + the format the SERP rewards (blue link AND Shopping pack where present). Everything upstream exists to pour traffic here.
- **MOFU — capture & consideration (SECONDARY REVENUE → BOFU).** Occasion/gift, comparison/brand-evaluation, keepsake-adjacent — capped, merchandised, first-party-proof-backed pages that intercept in-market shoppers and route them to BOFU. Broad heads owned by DTC/Reddit/AIO are *assist/PR targets*, not capture.
- **TOFU — reach & recommendability (NEVER a revenue line, built LAST).** The three defensible forms above, gated behind a proven BOFU funnel + the proof moat + earned authority.

**Method.**
1. **Map every cluster to a stage** with its `win_mechanism` (blue_link/shopping/image_pack/aio_citation/local_pack/hosted_artifact), AIO exposure, and `role`. Low KD ≠ winnable (see [[winnability-and-serp-regimes]]).
2. **Sequence in waves with entry/exit/KILL gates.** A higher rung is built only AFTER the rung below proves the page→preview/tool→purchase model. Typical shape: Wave 0 (M0–3) build winnable BOFU + the moat pipeline (not a revenue phase); Wave 1 (M3–6) localize + compound proof + start MOFU; Wave 2 (M6–12) open the link push + ship the EEAT/hosted TOFU layer; Wave 3 (M12–18) close the authority gap, contest link-gated heads, new-geo optionality. Each stage carries a numeric entry gate, exit gate, and a KILL trigger (stop scaling what misses its gate).
3. **Wire the down-funnel plumbing** (the actual mechanism each upper stage uses to convert down): a universal converter wedge (tool/preview embedded everywhere), **strictly-downward internal linking** (every MOFU/TOFU page links to its BOFU money page, never sideways into more TOFU), email capture at each rung, occasion-timed CTAs, and a repeat/retention loop. Make each handoff measurable (assisted-conversion path, not vibes).
4. **Assign channel roles per stage** — organic vs Shopping/PLA vs Pinterest vs PR/affiliate vs LLM/SOAV. Informational/image-pack pools are *feeders* (impressions + referral + AIO citation), not organic-click channels (see [[ai-overviews-and-serp-features]]).
5. **Forecast convertible vs feeder/assist separately, single-pass.** Only BOFU + genuinely-buyer-intent MOFU is convertible; TOFU and broad gift heads are reach/assist. Compute sessions × CTR × conversion ONCE with the AIO haircut applied once (see [[number-reconciliation]] + the double-haircut trap).
6. **Per-stage KPI + gate table + policy-resilience note.** North-star = convertible + assisted *contribution*, plus branded search and share-of-AI-voice (immune to AIO click-theft). Each stage maps to the policy it must respect (scaled-content, doorway, parasite-SEO, COPPA/AADC/GDPR for any minor's-data tool).

**Decision criteria / heuristics.**
- TOFU is built LAST, never anchors revenue, and every TOFU asset has a named down-funnel path or it's cut.
- A higher funnel rung opens only when the rung below has proven conversion (build-gate rule).
- Strictly-downward internal links — upper pages feed PageRank + users to BOFU, never to each other.
- Broad, DTC/Reddit/AIO-owned heads = link/PR/citation targets, not ranking/traffic lines.
- Branded search + SOAV are primary KPIs once upper-funnel reach lands; raw TOFU clicks are vanity.

**Example (Aurelet, 2026-06).** A personalized-baby-book brand asked to "roll out BOFU + MOFU + TOFU too". The funnel map confirmed the big TOFU oceans (baby names 989k, baby shower 158k, gender reveal 115k) are ~80% AIO-saturated and were already killed (KILL-3) — so the rollout kept them dead as click plays and admitted TOFU only as: a photo→storybook preview tool (hosted artifact, also the universal CRO wedge), an AI-illustration craft hub + honest competitor teardown (EEAT + LLM-citation), and gift-guide PR (link bait). Sequencing: Wave 0 winnable BOFU + moat pipeline → Wave 1 UK localize + MOFU occasion → Wave 2 link push + EEAT TOFU → Wave 3 contest the rd259 link-gated heads. TOFU was booked as reach/assist, never revenue. The red-team caught (and the doc fixed) a 10× forecast slip and a capture-pool that exceeded its own ceiling.

**Pitfalls.**
- Reintroducing killed TOFU pools as "we'll just touch them lightly" — they come back as scaled content.
- Upper-funnel pages that link sideways into more content instead of down to BOFU.
- Booking feeder/citation reach as convertible organic revenue.
- Building TOFU before BOFU conversion + authority are proven (wrong order, wasted spend).
- Double-applying the AIO haircut or shipping a forecast whose chain doesn't multiply out.

**Related.** [[keyword-to-sitemap]], [[search-intent]], [[ai-overviews-and-serp-features]], [[winnability-and-serp-regimes]], [[number-reconciliation]], [[free-tools-strategy]], [[content-rings]], [[adversarial-agent-orchestration]]. Tooling: `scripts/funnel_rollout_cascade.mjs` (the adversarial rollout pipeline), `scripts/forecast.py`. Runbook: `workflows/full-funnel-rollout.md`.
