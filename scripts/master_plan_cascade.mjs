/**
 * master_plan_cascade.mjs — EXHAUSTIVE, ADVERSARIAL master-plan pipeline (Workflow-tool script).
 *
 * The deeper sibling of master_plan_workflow.mjs. Use when the user wants the niche "fully explored
 * and exhausted" — it diverges N strategies, scores them with a judge panel, synthesizes the best,
 * then adversarially reviews every load-bearing claim. Niche-AGNOSTIC: all specifics come from args
 * + the data on disk. Run AFTER pulling live data (Ahrefs sweep + SERP pulls; see full-master-plan.md).
 *
 * Invoke:  Workflow({ scriptPath: ".../scripts/master_plan_cascade.mjs", args: {
 *   dataDir, serpDir, analysisDir, playbooks,            // paths
 *   brand, product, niche, seedKeyword, geos             // niche context strings
 * }})
 * Pre-reqs on disk in dataDir: keywords.csv (required), summary.json, overviews.json, serp_summary.json
 *   (+ serpDir/*.json live SERP pulls with DR/UR + features). Optional: analysisDir/winnability-and-scoping.md,
 *   live-site-state.md, authority-and-health.md (a prior scout pass strengthens every agent).
 *
 * Pillars baked in (the learnings this script enforces):
 *  - STRICT NICHE SCOPING: "AI X" != "X"; off-niche/competitor/service-hire/adjacent terms are pruned from money/forecast pools.
 *  - WINNABILITY: low KD != winnable; classify win_mechanism (blue_link/image_pack/aio_citation/local_pack) from live SERPs and match the format.
 *  - ONE RECOMPUTE SCRIPT: every headline regenerates from a single committed recompute script; numbers reconciled, measured vs projected tagged.
 *  - CODE GROUND-TRUTH (live sites): verify routes/robots/sitemap + unmerged branches in the actual repo, not just curl.
 *  - NON-THIN pSEO: every leaf needs a real uniqueness mechanism; demand-gate expansion; ship-noindex-then-flip.
 */
export const meta = {
  name: 'master-plan-cascade',
  description: 'Exhaustive, adversarial SEO master plan: foundation analysis -> N divergent strategy cascades -> judge panel -> synthesis -> adversarial review -> best market-capture plan. Strict niche scoping, winnability-aware, non-thin pSEO, one reproducible recompute script.',
  phases: [
    { title: 'Foundation' },
    { title: 'Strategy cascade' },
    { title: 'Judge panel' },
    { title: 'Synthesis' },
    { title: 'Adversarial review' },
    { title: 'Final plan' },
  ],
}

const A = args || {}
const DATA = A.dataDir, SERP = A.serpDir || (A.dataDir + '/serp'), ANALYSIS = A.analysisDir, PB = A.playbooks
const BRAND = A.brand || 'the brand', PRODUCT = A.product || 'the product'
const NICHE = A.niche || A.seedKeyword || 'the niche', SEED = A.seedKeyword || NICHE
const GEOS = A.geos || 'US (primary), then other English markets'

const SCOPE = `STRICT NICHE SCOPING (read ${PB}/research/number-reconciliation.md): the niche is "${NICHE}" — NOT the broader category. "AI X design" is not "AI design"; an adjacent vertical, a generic-tool term, a competitor BRAND term, and a service-HIRE term ("[x] near me" when the product is DIY/self-serve) are OFF-NICHE and must be EXCLUDED from money/forecast pools. (A /vs/{competitor} page is allowed; the competitor's branded volume is never counted as our demand.) Commit the off-niche prune as an explicit regex in the recompute script.`

const WINNABILITY = `WINNABILITY (read ${PB}/research/winnability-and-serp-regimes.md): LOW KD != WINNABLE. KD is blind to SERP features. For every cluster, classify the win_mechanism from the LIVE SERPs in ${SERP}/*.json: blue_link (weakly-linked top pages, low UR — a low-DR site wins with ~10-15 page links) / image_pack (Pinterest/Houzz/DR90+ own the top; the blue link is unwinnable; win the image pack + below-the-fold slot with ORIGINAL imagery, never thin text) / aio_citation (be the cited source, not the click) / local_pack (win the sub-pack organic slot; separate service-hire from product intent) / shopping_pack (an organic_shopping/PLA block owns the top of a PRODUCT SERP — win the Shopping slot with a Google Merchant feed AND the still-contestable organic slot with an exact-match product page; usually AIO-light, so it's a stronger forecast pool than image/AIO oceans). Then build the FORMAT that mechanism rewards. A "missing organic position 1" in the SERP data is usually a Shopping/ads block — verify before assuming AIO. If ~40%+ of top-5 are DR90-100 UGC/brand, target only the 1-2 displaceable slots (lower capture, not a promise).`

const METHOD = `SEO METHOD (playbooks ${PB}): KD<20 rankable for a low-authority site, but the real bar is the top-3 pages' URL-rating, not domain DR. intent->format: transactional->tool/landing; commercial(best/vs/[city])->comparison/local; informational->the format the win_mechanism rewards (render/gallery for image_pack, NOT text). Long-tail clusters beat heads on odds. pSEO 6 steps: family->URL pattern->data->shape->hub+leaf(unique)->inject offer; EVERY leaf needs a real non-thin uniqueness mechanism or it won't rank; demand-gate expansion (don't template near-zero-vol grids); ship-noindex-then-flip <=20/wk; the gate should be enforceable in code/CI for live sites, not prose. AIO: image-pack/AIO informational pools are reach/citation feeders, not click channels; apply the haircut ONCE (~0.5) and never double-count; anchor the business case on the blue_link money pools. NUMBER DISCIPLINE: every load-bearing figure regenerates from ONE committed recompute script reading ONE source file with explicit filters; tag measured vs projected; never sum them; pick ONE canonical value per metric. POLICY-SAFETY (2024-26): every page family must survive scaled-content-abuse / doorway / site-reputation-abuse / fake-EEAT / helpful-content scrutiny — apply the "would this page exist if Google did not?" test; a templated set on a low-authority domain is the #1 demotion profile, so gate it on real per-leaf value + EEAT and noindex-until-proven. DEFENSIBILITY: prefer plays a DR-incumbent can't copy in a week (first-party data/UGC, brand/entity, operational lock-in, earned authority) over commodity generators/collection pages.`

const CONTEXT = `PRODUCT: ${BRAND} — ${PRODUCT}. NICHE / money seed: "${SEED}". GEOS: ${GEOS}.
GOAL: the BEST plan to capture maximum realistic market for THIS niche specifically — exhaustive (pSEO + content + tools + local + authority) yet SENSIBLE (no thin pages, no off-niche drift, no feature-locked blue-link bets).
${SCOPE}
${WINNABILITY}
DATA ON DISK (read first; aggregate with Bash; cite real numbers, never guess): ${DATA}/keywords.csv (columns keyword,volume,kd,cpc,clicks,parent,country,seed,category,funnel), ${DATA}/summary.json, ${DATA}/overviews.json, ${DATA}/serp_summary.json + ${SERP}/*.json (live SERP w/ DR/UR + features). Prior scout notes if present: ${ANALYSIS}/winnability-and-scoping.md, ${ANALYSIS}/live-site-state.md, ${ANALYSIS}/authority-and-health.md.`

// ---------- schemas ----------
const CLUSTERS_SCHEMA = { type:'object', additionalProperties:false, required:['clusters','clean_universe_note'], properties:{
  clean_universe_note:{type:'string'},
  clusters:{type:'array', items:{type:'object', additionalProperties:false, required:['name','intent','funnel','kd_band','summed_volume','win_mechanism','page_type','priority','top_keywords'], properties:{
    name:{type:'string'}, intent:{type:'string'}, funnel:{type:'string',enum:['TOFU','MOFU','BOFU']}, kd_band:{type:'string'},
    summed_volume:{type:'number'}, win_mechanism:{type:'string',enum:['blue_link','image_pack','aio_citation','local_pack','shopping_pack','mixed']},
    page_type:{type:'string'}, priority:{type:'string',enum:['P0','P1','P2','P3']},
    top_keywords:{type:'array', items:{type:'object', additionalProperties:false, required:['kw','vol','kd'], properties:{kw:{type:'string'},vol:{type:'number'},kd:{type:'number'}}}} }}}
}}
const WINMAP_SCHEMA = { type:'object', additionalProperties:false, required:['verdicts','summary'], properties:{
  summary:{type:'string'},
  verdicts:{type:'array', items:{type:'object', additionalProperties:false, required:['cluster','win_mechanism','beatable','evidence'], properties:{
    cluster:{type:'string'}, win_mechanism:{type:'string'}, beatable:{type:'string',enum:['yes','maybe','hard']}, evidence:{type:'string'} }}}
}}
const PSEO_SCHEMA = { type:'object', additionalProperties:false, required:['families','total_pages','total_volume_estimate','doctrine'], properties:{
  total_pages:{type:'number'}, total_volume_estimate:{type:'number'}, doctrine:{type:'string'},
  families:{type:'array', items:{type:'object', additionalProperties:false, required:['name','url_pattern','page_count','volume_estimate','uniqueness_mechanism','data_source','win_mechanism','priority','examples'], properties:{
    name:{type:'string'}, url_pattern:{type:'string'}, page_count:{type:'number'}, volume_estimate:{type:'number'},
    uniqueness_mechanism:{type:'string'}, data_source:{type:'string'}, win_mechanism:{type:'string'}, priority:{type:'string',enum:['P0','P1','P2','P3']},
    examples:{type:'array',items:{type:'string'}} }}}
}}
const COMPETITOR_SCHEMA = { type:'object', additionalProperties:false, required:['competitors','gaps'], properties:{
  gaps:{type:'array',items:{type:'string'}},
  competitors:{type:'array', items:{type:'object', additionalProperties:false, required:['domain','what_they_rank_for','page_structure','why_they_win','how_to_beat'], properties:{
    domain:{type:'string'}, what_they_rank_for:{type:'string'}, page_structure:{type:'string'}, why_they_win:{type:'string'}, how_to_beat:{type:'string'} }}}
}}
const STRATEGY_SCHEMA = { type:'object', additionalProperties:false, required:['thesis','pillars','page_architecture','moat','twelve_month_build','market_capture_estimate','biggest_risk'], properties:{
  thesis:{type:'string'}, moat:{type:'string'}, market_capture_estimate:{type:'string'}, biggest_risk:{type:'string'},
  pillars:{type:'array',items:{type:'string'}},
  page_architecture:{type:'array', items:{type:'object', additionalProperties:false, required:['layer','url_pattern','page_count','win_mechanism','funnel_role'], properties:{
    layer:{type:'string'}, url_pattern:{type:'string'}, page_count:{type:'string'}, win_mechanism:{type:'string'}, funnel_role:{type:'string'} }}},
  twelve_month_build:{type:'array',items:{type:'string'}}
}}
const JUDGE_SCHEMA = { type:'object', additionalProperties:false, required:['ranking','best_ideas_to_graft','verdict'], properties:{
  verdict:{type:'string'},
  ranking:{type:'array', items:{type:'object', additionalProperties:false, required:['strategy','market_capture','winnability_realism','non_thin_sensibility','conversion_fit','effort_roi','total','note'], properties:{
    strategy:{type:'string'}, market_capture:{type:'number'}, winnability_realism:{type:'number'}, non_thin_sensibility:{type:'number'}, conversion_fit:{type:'number'}, effort_roi:{type:'number'}, total:{type:'number'}, note:{type:'string'} }}},
  best_ideas_to_graft:{type:'array',items:{type:'string'}}
}}
const REVIEW_SCHEMA = { type:'object', additionalProperties:false, required:['fixes','fabrications','thin_page_risks','verdict'], properties:{
  verdict:{type:'string'}, fixes:{type:'array',items:{type:'string'}}, fabrications:{type:'array',items:{type:'string'}}, thin_page_risks:{type:'array',items:{type:'string'}} }}
const SECTION_SCHEMA = { type:'object', additionalProperties:false, required:['title','file','summary','takeaways'], properties:{
  title:{type:'string'}, file:{type:'string'}, summary:{type:'string'}, takeaways:{type:'array',items:{type:'string'}} }}

// ---------- PHASE 1: Foundation (4 parallel analysts) ----------
phase('Foundation')
const [clusters, winmap, pseo, competitors] = await parallel([
  () => agent(`${CONTEXT}\n\n${METHOD}\n\nTASK: Build the CLEAN niche-scoped cluster + funnel map. Aggregate ${DATA}/keywords.csv with Bash; PRUNE all off-niche per the scoping rule (adjacent verticals, generic-tool terms, competitor brands, service-hire intent). Group the clean universe into coherent clusters; per cluster set intent, funnel, KD band, summed volume (recomputed, state filter), the WIN MECHANISM grounded in ${SERP}/*.json, the right page_type for that mechanism, and priority (P0 = winnable + high-intent + product-aligned). Also emit the exact off-niche prune filter you used so it can be committed to a recompute script. Write ${ANALYSIS}/clusters-clean.json. Return it.`, {label:'clusters-clean', phase:'Foundation', schema:CLUSTERS_SCHEMA}),
  () => agent(`${CONTEXT}\n\n${METHOD}\n\nTASK: Build the WINNABILITY map (read ${PB}/research/winnability-and-serp-regimes.md). For each major cluster read the live SERPs in ${SERP}/*.json and state the win mechanism, a beatable verdict (yes/maybe/hard) with DR/UR/feature EVIDENCE, and whether a blue link is even available (vs image_pack/AIO/local-pack lock). Be ruthless: if DR90+ UGC/brand own it with image_pack, say a text page can't win and name the real play (image + sub-pack slot + citation). Return the structured map.`, {label:'winnability', phase:'Foundation', schema:WINMAP_SCHEMA}),
  () => agent(`${CONTEXT}\n\n${METHOD}\n\nTASK: Design the EXHAUSTIVE but NON-THIN pSEO architecture for "${NICHE}". Bash-mine ${DATA}/keywords.csv for scalable families (per-entity / per-attribute / per-location / per-occasion / per-problem / per-style as the niche affords). For EACH family give URL pattern, honest page_count, volume estimate (tag measured vs projected), the UNIQUENESS MECHANISM that makes each leaf non-thin (the specific real per-leaf data/asset, not "good content"), the DATA SOURCE, the win mechanism, priority, and 3 example slugs. Enforce the doctrine: no leaf ships without its uniqueness asset + offer CTA; demand-gate expansion (flag any family with near-zero vol/page as a doorway tripwire). Write ${ANALYSIS}/pseo-architecture.json. Return it.`, {label:'pseo-arch', phase:'Foundation', schema:PSEO_SCHEMA}),
  () => agent(`${CONTEXT}\n\n${METHOD}\n\nTASK: Competitor teardown. Use WebFetch/WebSearch to actually OPEN the pages of the incumbents that rank in ${SERP}/*.json (the top blue-link winners AND a representative image-pack/AIO winner). For each: what they rank for, page structure, why they win (links? unique asset? freshness?), and concretely how ${BRAND} beats them (name the product's structural wedge). List the biggest content/format GAPS ${BRAND} can own. Return structured.`, {label:'competitors', phase:'Foundation', schema:COMPETITOR_SCHEMA}),
])

const FOUND = `FOUNDATION FINDINGS (shared ground truth; numbers recomputed from data):
CLEAN CLUSTERS: ${JSON.stringify(clusters).slice(0,3500)}
WINNABILITY: ${JSON.stringify(winmap).slice(0,2500)}
pSEO ARCHITECTURE: ${JSON.stringify(pseo).slice(0,3000)}
COMPETITORS/GAPS: ${JSON.stringify(competitors).slice(0,2000)}`

// ---------- PHASE 2: Strategy cascade (5 divergent strategists) ----------
phase('Strategy cascade')
const THESES = [
  { key:'pseo-maximalist', angle:'Programmatic-at-scale: win maximum long-tail via the strongest pSEO families, each leaf non-thin (real per-leaf asset + data) and demand-gated. Maximize indexed surface sensibly.' },
  { key:'tool-or-product-led', angle:'Product/tool-led: capture all BOFU money demand with exact-match product/tool landing pages; the page that ranks IS the converting product; viral/PLG funnel.' },
  { key:'visual-serp-engine', angle:'Image-pack / visual-SERP engine: treat the image-pack-gated informational ocean as a visual distribution play — original imagery galleries engineered to own image_pack + Pinterest + AIO citations, all funnelling to the money pages.' },
  { key:'local-domination', angle:'Local SEO: own "[city/region] [niche]" and the sub-pack organic slot; per-location pages with real local data; optional GBP. (Only if the niche has genuine product-aligned local demand — exclude service-hire.)' },
  { key:'topical-authority-geo', angle:'Topical-authority / GEO: become THE cited entity for the niche in ChatGPT/Perplexity/AI-Overviews via a deep interlinked hub, original data studies, and content rings.' },
]
const strategies = await parallel(THESES.map(t => () =>
  agent(`${CONTEXT}\n\n${FOUND}\n\nYou are STRATEGIST "${t.key}". Design a COMPLETE 12-month market-capture plan for ${BRAND} from THIS thesis: ${t.angle}\nGround every choice in the foundation findings + the winnability reality (do NOT propose thin text for image-pack-locked SERPs; do NOT drift off the "${NICHE}" niche). Maximize realistic market capture for THIS niche specifically. Give the thesis, pillars, the full page architecture (layers, URL patterns, page counts, win mechanism, funnel role), the moat (why competitors can't copy), the 12-month build sequence, an honest market-capture estimate, and the biggest risk. Return structured.`,
    {label:`strat:${t.key}`, phase:'Strategy cascade', schema:STRATEGY_SCHEMA})
    .then(s => ({...s, key:t.key}))
)).then(r => r.filter(Boolean))

// ---------- PHASE 3: Judge panel (3 judges score the 5) ----------
phase('Judge panel')
const stratDigest = strategies.map(s => `### ${s.key}\nthesis: ${s.thesis}\ncapture: ${s.market_capture_estimate}\nmoat: ${s.moat}\narchitecture: ${(s.page_architecture||[]).map(p=>p.layer+":"+p.url_pattern+"("+p.page_count+","+p.win_mechanism+")").join(' | ')}\nrisk: ${s.biggest_risk}`).join('\n\n')
const judges = await parallel(['market-capture & winnability realism','non-thin sensibility & conversion fit','effort/ROI & AIO-GEO resilience'].map(lens => () =>
  agent(`${CONTEXT}\n\nYou are a JUDGE focusing on: ${lens}. Score each strategy 1-10 on market_capture, winnability_realism, non_thin_sensibility, conversion_fit, effort_roi (total = sum). Penalize HARD any plan that proposes thin pages for image-pack-locked SERPs, drifts off the "${NICHE}" niche, assumes blue-link wins where the SERP is feature-locked, or templates near-zero-vol grids. Reward realistic, product-aligned, compounding capture. List the single best idea to graft from EACH strategy. End with a one-line verdict on which thesis should be the spine.\n\nSTRATEGIES:\n${stratDigest}`,
    {label:`judge:${lens.split(' ')[0]}`, phase:'Judge panel', schema:JUDGE_SCHEMA})
)).then(r => r.filter(Boolean))

// ---------- PHASE 4: Synthesis (1 agent merges winner + grafts) ----------
phase('Synthesis')
const judgeDigest = judges.map((j,i)=>`Judge ${i+1} verdict: ${j.verdict}\nranking: ${(j.ranking||[]).map(r=>r.strategy+"="+r.total).join(', ')}\ngraft: ${(j.best_ideas_to_graft||[]).join('; ')}`).join('\n\n')
const masterDraft = await agent(`${CONTEXT}\n\n${FOUND}\n\n5 STRATEGIES:\n${stratDigest}\n\nJUDGE PANEL:\n${judgeDigest}\n\nTASK: Synthesize the SINGLE BEST exhaustive market-capture plan for ${BRAND}. Pick the winning thesis as the spine and graft the best ideas from the runners-up. Produce: (1) the strategy in one page, (2) the COMPLETE page/IA architecture every layer with URL patterns + page counts + win mechanism + funnel role, (3) the full pSEO family table with non-thin uniqueness mechanism per family, (4) the image-pack/visual engine spec (if applicable), (5) the money-page + tool plan, (6) internal-linking contract, (7) the 12-month build sequence with indexing waves, (8) how it captures MAXIMUM market while staying sensible (no thin pages, no off-niche, no feature-locked bets). ALSO write ${ANALYSIS}/recompute.py — ONE committed script that regenerates every headline number from ${DATA}/keywords.csv with one explicit off-niche prune and stated filters. Recompute the headline addressable numbers from it. Write the full plan to ${ANALYSIS}/MASTER-PLAN.md and return a structured section record.`,
  {label:'synthesis', phase:'Synthesis', schema:SECTION_SCHEMA})

// ---------- PHASE 5: Adversarial review (4-5 skeptics) ----------
phase('Adversarial review')
const REVIEW_SLICES = [
  'NUMBERS: write/verify analysis/recompute.py and re-derive every headline figure in MASTER-PLAN.md from keywords.csv; flag any not reproducible, any off-niche term counted in money/forecast pools, and any metric with >1 surviving value.',
  'WINNABILITY: cross-check every "winnable/blue-link" claim against serp/*.json; flag any page proposed for an image-pack/AIO/local-pack-locked SERP as a text blue-link play; verify capture shares reflect the displaceable-slot reality.',
  'THIN-PAGE & SCALED-CONTENT: audit every pSEO family; flag any leaf lacking a real uniqueness mechanism (would be a thin doorway) and any near-zero-vol/page grid; check ship-noindex-then-flip + demand-gating are enforced (ideally in code for live sites).',
  'NICHE DISCIPLINE: flag any drift into the broader category / generic-tool / competitor-brand / service-hire demand; confirm everything serves the specific "${NICHE}" intent.',
  'CODE GROUND-TRUTH (only if a live codebase/repo is in context): verify the plan\'s claims about existing routes, robots/noindex directives, sitemap inclusion, and UNMERGED branches against the actual code — correct any assumption that contradicts the repo.',
  'GOOGLE-POLICY ASSASSIN: beyond thin pages, audit the WHOLE plan against the 2024-26 spam/quality policies — scaled-content abuse (any large templated set on a low-authority domain), doorway pages (near-duplicate pages funneling to one destination), site-reputation/parasite abuse (renting third-party authority), fake/AI-author EEAT or manufactured expertise, expired-domain abuse. Apply the "would this page exist if Google did not?" test to every page family; flag anything that would draw a manual action or core-update demotion, and the kill-switch/EEAT gate that de-risks it.',
  'MOAT / DEFENSIBILITY ASSASSIN: for every pillar, ask could a DR-incumbent or fast-follower copy it in a week? Flag commodity plays (a free generator, a generic collection page, a listicle) that carry NO durable advantage, and verify the plan\'s stated moat is real — first-party data/UGC, brand/entity, operational lock-in, or earned authority that a competitor must rebuild from scratch. A plan that ranks but is trivially copyable is not a strategy.',
]
const reviews = await parallel(REVIEW_SLICES.map(slice => () =>
  agent(`${CONTEXT}\n\nYou are a ruthless ADVERSARIAL REVIEWER. Read ${ANALYSIS}/MASTER-PLAN.md and the JSON artifacts in ${ANALYSIS}/. Your slice: ${slice}\nRecompute from ${DATA}/keywords.csv with Bash where relevant. Return concrete fixes (with corrected numbers), fabrications, and thin-page risks. Be specific and harsh; default to skepticism.`,
    {label:`review:${slice.split(':')[0].slice(0,16)}`, phase:'Adversarial review', schema:REVIEW_SCHEMA})
)).then(r => r.filter(Boolean))

// ---------- PHASE 6: Final plan (apply fixes) ----------
phase('Final plan')
const reviewDigest = reviews.map((r,i)=>`Reviewer ${i+1} (${r.verdict}):\n  fixes: ${(r.fixes||[]).join(' | ')}\n  fabrications: ${(r.fabrications||[]).join(' | ')}\n  thin-page risks: ${(r.thin_page_risks||[]).join(' | ')}`).join('\n\n')
const final = await agent(`${CONTEXT}\n\nThe draft plan is at ${ANALYSIS}/MASTER-PLAN.md. Apply EVERY valid fix from the adversarial review below — correct numbers (regenerate via analysis/recompute.py), remove off-niche terms from pools, downgrade any text page proposed for an image-pack-locked SERP to the correct mechanism, ensure every pSEO leaf has a stated non-thin uniqueness mechanism, and reconcile any claim that contradicts the codebase. Add a "SUPERSEDED ARTIFACTS" section listing every corrected figure (old -> new + source). Rewrite ${ANALYSIS}/MASTER-PLAN.md as the FINAL plan, and ALSO write a tight ${ANALYSIS}/EXEC-SUMMARY.md (strategy on a page, addressable numbers niche-scoped, P0 quick wins, biggest risks honestly). Every load-bearing number reproducible from recompute.py with its filter, tagged measured/projected.\n\nADVERSARIAL REVIEW:\n${reviewDigest}`,
  {label:'final-synthesis', phase:'Final plan', schema:SECTION_SCHEMA})

return { clusters, winmap, pseo, competitors, strategies: strategies.map(s=>s.key), judges: judges.length, reviews: reviews.length, masterDraft, final }
