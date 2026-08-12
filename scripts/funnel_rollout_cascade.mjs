/**
 * funnel_rollout_cascade.mjs — ADVERSARIAL full-funnel (BOFU→MOFU→TOFU) ROLLOUT pipeline (Workflow-tool script).
 *
 * The sibling of master_plan_cascade.mjs. That one GENERATES the strategy; this one EXTENDS an existing,
 * canonical plan into the OPERATIONAL rollout: how the brand sequences and operates BOFU, then MOFU, then
 * TOFU over time, with every upper stage engineered to FUNNEL DOWN to the money page. Use after a master
 * plan exists and the user asks to "roll out the full funnel / sequence BOFU+MOFU+TOFU".
 *
 * Invoke:  Workflow({ scriptPath: ".../scripts/funnel_rollout_cascade.mjs", args: {
 *   dataDir, serpDir, analysisDir, playbooks,            // paths
 *   canonicalPlan, graveyard, outFile,                   // the existing plan + killed-ideas record + EXACT output path
 *   brand, product, niche, seedKeyword, geos             // niche context strings
 * }})
 * Pre-reqs on disk: the canonicalPlan markdown (the master/strategy doc), keywords.csv + SERP files in dataDir,
 *   and ideally the graveyard (killed ideas). The funnel map is written to analysisDir/funnel-map.json.
 *
 * Pillars baked in (the learnings this script enforces):
 *  - DEFENSIBLE STAGE DEFINITION: "roll out the full funnel" is reconciled with "TOFU-for-its-own-sake is dead".
 *    TOFU re-enters ONLY as (a) an AIO-safe HOSTED artifact/tool users want, (b) brand + LLM-citation / share-of-AI-voice
 *    measured as reach/assist, or (c) genuine link bait — always built LAST, capped, EEAT-gated, NEVER a revenue line,
 *    and every upper-funnel play must have a CONCRETE, measurable path DOWN to the money page or it does not ship.
 *  - NO RESURRECTION: read the graveyard; a killed idea (per-name pages, raw-TOFU pools, vanity occasion totals) never returns.
 *  - WINNABILITY + AIO: classify each cluster's win_mechanism from live SERPs; informational/image-pack pools are FEEDERS,
 *    not click channels; anchor revenue on blue_link/shopping money + commercial pools.
 *  - SINGLE-PASS FORECAST: sessions × CTR × conversion computed ONCE; the AIO haircut applied exactly once (no double-haircut,
 *    no 10× "sessions" slip). Convertible vs feeder/assist split; never sum measured + projected.
 *  - DOWN-FUNNEL PLUMBING: explicit handoff system (tool/photo wedge as universal converter, strictly-downward internal
 *    linking, email capture per rung, occasion-timed CTAs, repeat/retention loop) — not hand-wavy "builds awareness".
 *  - ADVERSARIAL: 5 divergent rollout strategies → 3-judge panel (score + steal) → synthesis → 5 red-teamers
 *    (numbers / AIO-double-haircut / policy+graveyard / funnel-coherence / sequencing) → finalize with a changelog.
 *
 * NOTE (operational): background workflows die silently if the sandbox is suspended mid-run — resume with
 *   Workflow({scriptPath, resumeFromRunId}) (cached prefix returns instantly). And ALWAYS verify outFile was
 *   actually written to the EXACT path after the run — synthesis agents sometimes rename it.
 */
export const meta = {
  name: 'full-funnel-rollout-cascade',
  description: 'Adversarial BOFU→MOFU→TOFU rollout for an existing SEO plan: funnel map → 5 divergent strategies → 3 judges → synthesis → 5 red-teamers → final rollout doc. Defensible per-stage definitions, down-funnel handoff plumbing, TOFU as reach/citation only, single-pass forecast, no resurrected ideas.',
  phases: [
    { title: 'Funnel map' },
    { title: 'Divergent strategies' },
    { title: 'Judge panel' },
    { title: 'Synthesize rollout' },
    { title: 'Red-team' },
    { title: 'Finalize' },
  ],
}

const A = args || {}
const DATA = A.dataDir, SERP = A.serpDir || (A.dataDir + '/serp'), ANALYSIS = A.analysisDir, PB = A.playbooks
const PLAN = A.canonicalPlan, GRAVE = A.graveyard, OUT = A.outFile
const BRAND = A.brand || 'the brand', PRODUCT = A.product || 'the product'
const NICHE = A.niche || A.seedKeyword || 'the niche', SEED = A.seedKeyword || NICHE
const GEOS = A.geos || 'US (primary), then other English markets'

const GROUND = `PRODUCT: ${BRAND} — ${PRODUCT}. NICHE / main keyword: "${SEED}". GEOs: ${GEOS}.

CANONICAL PLAN (read it fully first — it is the source of the verified demand pools, pillars, and constraints you must honor): ${PLAN}.
KILLED-IDEAS RECORD (DO NOT resurrect anything in here): ${GRAVE}.
LIVE DATA (read + Bash-aggregate; cite real numbers, never invent): ${DATA}/keywords.csv, summary.json, overviews.json, clusters.json, competition.json, ${DATA}/serp_summary.json + ${SERP}/*.json (DR/UR + SERP features), traffic_by_domain.json.
METHODOLOGY PLAYBOOKS: ${PB}/content/full-funnel-rollout.md (the rollout method — defensible stage defs, handoff plumbing, wave/kill-gates), ${PB}/foundations/adversarial-agent-orchestration.md (this pipeline's pattern), ${PB}/research/winnability-and-serp-regimes.md (low KD ≠ winnable; win_mechanism), ${PB}/maintenance/ai-overviews-and-serp-features.md (AIO haircut; feeders not click channels; the double-haircut trap), ${PB}/research/number-reconciliation.md (reproduce every figure; single forecast chain).

HARD CONSTRAINTS (any plan violating these is wrong):
- Use ONLY the canonical plan's verified demand numbers; recompute anything contested from keywords.csv with stated filters; tag measured vs projected and never sum them.
- TOFU may ONLY re-enter as AIO-safe hosted artifact / brand+LLM-citation (assist/reach) / link bait — built LAST, capped, EEAT-gated, never a revenue line, each with a concrete down-funnel path. Raw informational/volume TOFU pools the graveyard killed stay dead.
- Respect every cap, content-diff gate, no-per-name rule, and policy guardrail in the canonical plan.
- Forecast is single-pass (sessions × CTR × conversion once; AIO haircut once). Convertible vs feeder/assist split.

THE TASK: produce a COMPREHENSIVE, defensible FULL-FUNNEL ROLLOUT that EXTENDS the canonical plan — the wave-by-wave operating plan for BOFU→MOFU→TOFU with entry/exit/KILL gates per stage, the cross-funnel handoff plumbing, channel roles per stage, per-stage KPIs, and an honest reconciliation of "roll out the full funnel" with "TOFU-for-its-own-sake is dead".`

// ---------- schemas ----------
const FUNNELMAP_SCHEMA = { type:'object', additionalProperties:false, required:['stages','funnel_down_mechanics','tofu_defensibility_verdict','dependency_gates'], properties:{
  tofu_defensibility_verdict:{type:'string'}, funnel_down_mechanics:{type:'array', items:{type:'string'}}, dependency_gates:{type:'array', items:{type:'string'}},
  stages:{type:'array', items:{type:'object', additionalProperties:false, required:['stage','clusters'], properties:{
    stage:{type:'string',enum:['BOFU','MOFU','TOFU']},
    clusters:{type:'array', items:{type:'object', additionalProperties:false, required:['name','volume','intent','win_mechanism','aio_exposed','book_relevance','role'], properties:{
      name:{type:'string'}, volume:{type:'number'}, intent:{type:'string'},
      win_mechanism:{type:'string',enum:['blue_link','image_pack','aio_citation','local_pack','shopping','hosted_artifact']},
      aio_exposed:{type:'boolean'}, book_relevance:{type:'string',enum:['core','adjacent','assist','feeder','off-niche']}, role:{type:'string'} }}} }}}
}}
const STRATEGY_SCHEMA = { type:'object', additionalProperties:false, required:['name','thesis','tofu_stance','waves','funnel_handoffs','risks','why_best'], properties:{
  name:{type:'string'}, thesis:{type:'string'}, tofu_stance:{type:'string'}, why_best:{type:'string'},
  funnel_handoffs:{type:'array', items:{type:'string'}}, risks:{type:'array', items:{type:'string'}},
  waves:{type:'array', items:{type:'object', additionalProperties:false, required:['wave','window','stage_focus','plays','entry_gate','exit_gate','kpis'], properties:{
    wave:{type:'string'}, window:{type:'string'}, stage_focus:{type:'string'}, plays:{type:'array',items:{type:'string'}}, entry_gate:{type:'string'}, exit_gate:{type:'string'}, kpis:{type:'array',items:{type:'string'}} }}}
}}
const JUDGE_SCHEMA = { type:'object', additionalProperties:false, required:['ranking','best','steal','rationale'], properties:{
  best:{type:'string'}, rationale:{type:'string'}, steal:{type:'array',items:{type:'string'}},
  ranking:{type:'array', items:{type:'object', additionalProperties:false, required:['name','defensibility','policy_safety','data_grounding','funnel_coherence','feasibility','total'], properties:{
    name:{type:'string'}, defensibility:{type:'number'}, policy_safety:{type:'number'}, data_grounding:{type:'number'}, funnel_coherence:{type:'number'}, feasibility:{type:'number'}, total:{type:'number'} }}}
}}
const REVIEW_SCHEMA = { type:'object', additionalProperties:false, required:['issues','verdict'], properties:{
  verdict:{type:'string'},
  issues:{type:'array', items:{type:'object', additionalProperties:false, required:['severity','area','problem','fix'], properties:{
    severity:{type:'string',enum:['must-fix','should-fix','nit']}, area:{type:'string'}, problem:{type:'string'}, fix:{type:'string'} }}}
}}

// ---------- PHASE 1: funnel map ----------
phase('Funnel map')
const funnelMap = await agent(
`${GROUND}\n\nTASK: Build the FUNNEL MAP. Read the canonical plan + graveyard + data. Place every meaningful cluster into BOFU / MOFU / TOFU. For each: real volume (recompute from keywords.csv, state filter), intent, win_mechanism (blue_link/image_pack/aio_citation/local_pack/shopping/hosted_artifact — infer from the SERP files; low KD alone is NOT winnable), aio_exposed, book_relevance (core/adjacent/assist/feeder/off-niche), and its ROLE in the funnel. Then: (1) a one-paragraph TOFU-defensibility verdict — which TOFU (if any) is worth building given the graveyard kills + AIO saturation, and in what FORMAT; (2) the concrete funnel-DOWN mechanics that move an upper-funnel visitor toward the money page; (3) the dependency gates (what must be true before each stage opens). WRITE the structured map to ${ANALYSIS}/funnel-map.json and return it.`,
  {label:'funnel-map', phase:'Funnel map', schema: FUNNELMAP_SCHEMA})
log('Funnel map complete')
const MAP = `\n\n=== FUNNEL MAP (canonical; build on this) ===\n${JSON.stringify(funnelMap).slice(0,6000)}`

// ---------- PHASE 2: divergent strategists ----------
phase('Divergent strategies')
const LENSES = [
  {key:'bofu-cashflow-first', brief:'BOFU-first / cashflow-then-expand. Win the winnable money heads + occasion, bank conversion + reviews, open MOFU/TOFU only behind hard revenue/asset gates. TOFU stays tiny + citation-only.'},
  {key:'moat-led-compounding', brief:'Moat-led. BOFU + the first-party proof/review/UGC moat first; MOFU rides the moat; TOFU is brand + LLM-citation + EEAT content feeding recommendability, not clicks.'},
  {key:'demand-ladder', brief:'Demand-capture ladder. Climb intent BOFU → MOFU → adjacent TOFU, but ONLY where a hosted artifact/tool users want exists (AIO-safe formats), each rung internally linked DOWN to BOFU.'},
  {key:'brand-geo-aio', brief:'Brand/GEO-led. Treat TOFU primarily as a share-of-AI-voice + branded-search engine (the only durable upper-funnel play in an AIO world): hosted tools, original-data/PR, entity strength — assist/reach, funneling to BOFU via email + retargeting.'},
  {key:'portfolio-killgates', brief:'Portfolio with explicit kill-gates. Run all three stages as a managed portfolio with per-wave entry/exit + KILL criteria (stop scaling any stage that misses its gate), maximizing optionality while staying policy-safe and capped.'},
]
const strategies = await parallel(LENSES.map(L => () => agent(
`${GROUND}${MAP}\n\nYou are a senior SEO strategist proposing ONE full-funnel rollout strategy under this lens: ${L.brief}\n\nProduce a complete, sequenced BOFU→MOFU→TOFU rollout as waves (window, stage focus, specific plays tied to real clusters/pages from the canonical plan, entry gate, exit gate, KPIs). State your TOFU stance explicitly (what TOFU you build, what you refuse, why — reconcile with the graveyard kills + AIO). Give the funnel-handoff mechanics (how each upper stage converts down to the money page). Ground every play and number in the data + canonical plan; do not resurrect graveyard-killed ideas. Return the structured strategy.`,
  {label:'strat:'+L.key, phase:'Divergent strategies', schema: STRATEGY_SCHEMA})))
log('Divergent strategies complete: ' + strategies.filter(Boolean).map(s=>s&&s.name).join(' | '))

// ---------- PHASE 3: judge panel ----------
phase('Judge panel')
const STRAT_DIGEST = strategies.filter(Boolean).map((s,i)=>`### STRATEGY ${i+1}: ${s.name}\n${JSON.stringify(s).slice(0,2400)}`).join('\n\n')
const judges = await parallel(['defensibility-and-policy','funnel-coherence-and-conversion','feasibility-and-data'].map(lens => () => agent(
`${GROUND}\n\nYou are a judge with the lens: "${lens}". Score each strategy 0–5 on defensibility, policy_safety, data_grounding, funnel_coherence, feasibility (total /25). Pick the best and list the specific ideas to STEAL from the runners-up into the final. Be harsh on anything that resurrects killed TOFU spam, double-counts vanity volume, or claims clean-SERP CTR.\n\nSTRATEGIES:\n${STRAT_DIGEST}`,
  {label:'judge:'+lens, phase:'Judge panel', schema: JUDGE_SCHEMA})))
log('Judging complete')

// ---------- PHASE 4: synthesis ----------
phase('Synthesize rollout')
const JUDGE_DIGEST = judges.filter(Boolean).map((j,i)=>`JUDGE ${i+1}: best=${j.best}; steal=${(j.steal||[]).join('; ')}; ranking=${JSON.stringify(j.ranking)}`).join('\n')
const synth = await agent(
`${GROUND}${MAP}\n\nYou are the lead strategist. Synthesize the judged strategies into ONE comprehensive FULL-FUNNEL ROLLOUT and WRITE it to EXACTLY this path (do NOT rename it): ${OUT}\n\nSTRATEGIES:\n${STRAT_DIGEST}\n\nJUDGE PANEL:\n${JUDGE_DIGEST}\n\nThe document MUST contain: (1) a 1-page thesis reconciling "roll out the full funnel" with "TOFU-for-its-own-sake is dead" — the DEFENSIBLE definition of each stage; (2) an ASCII funnel architecture showing BOFU/MOFU/TOFU and the down-funnel flows; (3) a stage-by-stage plan — BOFU, MOFU, TOFU each: role, real target clusters (vol/KD/win_mechanism from data), page/asset types, format discipline (AIO/SERP-feature aware), and how it hands off DOWN to BOFU; (4) a WAVE-BY-WAVE rollout calendar (M0–3, 3–6, 6–12, 12–18) with entry/exit gates + KILL criteria per stage; (5) the cross-funnel handoff system (email capture, retargeting, strictly-downward internal-linking rules, content→product CTAs, repeat/retention loop); (6) channel roles (organic vs Shopping/PLA vs Pinterest vs PR/affiliate vs LLM/SOAV) per stage; (7) a per-stage KPI + gate table; (8) an honest forecast note — convertible vs feeder/assist, single forecast chain, AIO haircut once — consistent with the canonical plan; (9) a policy-resilience note per stage; (10) a "What this synthesis decided (provenance)" section noting the winning spine + panel-mandated steals. Every number recomputed from data and labelled measured/projected. Return a short confirmation + the headline sequencing.`,
  {label:'synthesis', phase:'Synthesize rollout'})
log('Synthesis written')

// ---------- PHASE 5: adversarial red-team ----------
phase('Red-team')
const REVIEW_LENSES = [
  {key:'numbers', brief:'Number reconciliation. Recompute every load-bearing figure from keywords.csv (state filters). Flag any number not reproducible, any measured+projected blending, any vanity-volume creep, and any forecast arithmetic slip (e.g. sessions × CTR × conversion that does not actually multiply out — the 10× trap).'},
  {key:'aio-serp', brief:'AIO / SERP-feature realism. Check win_mechanism per cluster matches the SERP files; check the AIO haircut is applied exactly ONCE (no double-haircut); flag any TOFU treated as a click/revenue line rather than feeder/citation; flag clean-SERP CTR claims.'},
  {key:'policy-graveyard', brief:'Policy + graveyard guard. Does the rollout resurrect any KILLED idea (raw-TOFU pools, per-name pages, vanity occasion totals, etc.)? Any scaled-content/doorway risk in the TOFU/MOFU expansion? Caps + content-diff gates respected?'},
  {key:'funnel-coherence', brief:'Funnel coherence. Does each upper-funnel play have a REAL, specific path DOWN to the money page (not hand-wavy "builds awareness")? Are the handoff mechanics concrete and measurable? Does TOFU traffic actually convert or is it vanity?'},
  {key:'sequencing-feasibility', brief:'Sequencing + feasibility. Are entry/exit gates realistic for this brand\'s authority/stage? Are upper stages correctly gated behind BOFU+moat+authority (not run too early)? Are kill-criteria concrete? Is resourcing sane?'},
]
const reviews = await parallel(REVIEW_LENSES.map(R => () => agent(
`${GROUND}\n\nYou are an adversarial red-teamer. Read the rollout doc at ${OUT} (and the data/canonical-plan/graveyard as needed). LENS: ${R.brief}\n\nReturn a prioritized issue list (severity must-fix/should-fix/nit, area, the problem, the concrete fix). Be specific and cite the offending line/number. End with a one-line verdict (ship / fix-then-ship / rework).`,
  {label:'redteam:'+R.key, phase:'Red-team', schema: REVIEW_SCHEMA})))
log('Red-team complete')

// ---------- PHASE 6: finalize ----------
phase('Finalize')
const ALL_ISSUES = reviews.filter(Boolean).flatMap((r,i)=>(r.issues||[]).map(x=>({reviewer:REVIEW_LENSES[i].key, ...x})))
const mustfix = ALL_ISSUES.filter(x=>x.severity==='must-fix')
const final = await agent(
`${GROUND}\n\nYou are the lead strategist finalizing ${OUT}. The adversarial red-team raised these issues (apply EVERY must-fix; apply should-fixes where correct; reject any that are wrong, with one-line reasoning):\n\n${JSON.stringify(ALL_ISSUES).slice(0,9000)}\n\nEDIT ${OUT} in place — recompute any contested number from keywords.csv, ensure the AIO haircut is applied once and the forecast chain actually multiplies out, ensure no killed idea resurfaces, and make every upper-funnel play have a concrete down-funnel path. Append a final "## What the red-team changed" section (fixed vs deliberately-rejected-with-reasoning). If a forecast error also exists in the canonical plan, FLAG it (do not silently edit the canonical plan). Then return: files written, count of must-fix issues resolved, and the final headline sequencing (BOFU→MOFU→TOFU waves in one line each).`,
  {label:'finalize', phase:'Finalize'})

return { funnelMap, strategies: strategies.filter(Boolean).length, judges: judges.filter(Boolean).length, mustfix: mustfix.length, reviews: reviews.filter(Boolean).length, final }
