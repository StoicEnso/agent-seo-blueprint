/**
 * master_plan_workflow.mjs — packaged end-to-end SEO master-plan pipeline (Workflow tool script).
 *
 * Reusable for ANY niche. Run AFTER pulling live data (Ahrefs sweep → keywords.csv + SERP +
 * overviews + clusters; see workflows/full-master-plan.md). It analyzes the SAVED data (never
 * hammers Ahrefs in parallel), ideates with ICP personas, writes strategy sections, reconciles
 * every number, and synthesizes the master plan.
 *
 * Invoke:  Workflow({ scriptPath: ".../scripts/master_plan_workflow.mjs", args: {
 *   dir, dataDir, analysisDir, rawDir, playbooks,        // paths (analysisDir = where sections are written)
 *   brand, product, niche, seedKeyword, geos             // niche context strings
 * }})
 * Pre-reqs on disk in dataDir: keywords.csv (required), summary.json, overviews.json,
 *   serp_summary.json (+ serp/*.json), clusters.json, traffic_by_domain.json.
 */
export const meta = {
  name: 'full-master-plan',
  description: 'End-to-end SEO master plan from live data: clusters/funnel, competition/SERP-gap, PSEO sizing, ICP personas, content/IA/technical/free-tools/authority/KPI sections, number reconciliation, synthesis',
  phases: [
    { title: 'Analyze data' },
    { title: 'ICP personas' },
    { title: 'Strategy modules' },
    { title: 'Synthesize plan' },
  ],
}

const A = args || {}
const DATA = A.dataDir, ANALYSIS = A.analysisDir, RAW = A.rawDir, PB = A.playbooks
const BRAND = A.brand || 'the brand', PRODUCT = A.product || 'the product'
const NICHE = A.niche || A.seedKeyword || 'the niche', SEED = A.seedKeyword || NICHE
const GEOS = A.geos || 'US (primary), then other English markets'

const METHOD = `SEO METHODOLOGY (apply strictly; playbooks at ${PB}):
- METRICS: KD<20 = rankable for a new/low-authority site (~10 backlinks, 1-2 months). Skip vol<100, discount <500. Click curve #1~30%/#2~15%/#3~10%. CPC = monetization filter. The REAL bar is the top-3 pages' URL-rating (page authority), NOT domain authority — a high-DR site with a weakly-linked ranking page is beatable.
- INTENT->FORMAT: informational->articles/explainers; commercial (best/vs/review/ideas)->comparison & curation; transactional (buy/custom/generator)->landing pages & the tool; navigational/branded->ignore. Confirm against the live SERP.
- LONG-TAIL: a cluster of low-volume long-tails can equal a head term with realistic odds. PSEO (6 steps): scalable family -> design URL/keyword pattern FIRST -> gather data -> shape -> template hub+leaf (unique meta) -> inject offer. Every leaf must add real value beyond its source or it won't rank. Stagger indexing.
- SITEMAP: home = one short-tail commercial keyword built as a richer-than-incumbents tool/page; category hubs per group; PSEO long-tail layer; every sub-page links UP to the converting tool.
- FREE TOOLS: build for generator/maker/calculator terms; make them EASIER than incumbents; exact-match title + variant-rich meta; How-it-works + FAQ; upsell on the result step.
- AUTHORITY: galleries/Product Hunt, link-stealing (sites linking to competitors), affiliate program, HARO/digital-PR, content rings, small influencer placements.
- AI OVERVIEWS (read ${PB}/maintenance/ai-overviews-and-serp-features.md): the click curve is OPTIMISTIC where SERP features sit. Measure feature exposure per pool; haircut informational+AIO CTR by ~0.4-0.6 (not flat); lean on AIO-safe commercial/entertainment intents; win the citation.
- NUMBER DISCIPLINE (read ${PB}/research/number-reconciliation.md): EVERY load-bearing number is recomputed from keywords.csv via a command, with the filter stated. Tag measured vs projected; never sum them. No figure ships unless it is reproducible.`

const CONTEXT = `PRODUCT: ${BRAND} — ${PRODUCT}. NICHE / main keyword: "${SEED}". GEOS: ${GEOS}.
GOAL: a credible path to large-scale organic traffic — prioritizing LOW-competition (KD<20), high-volume, high-intent lower-funnel keywords, plus top-funnel content engineered to funnel back to the money pages.
DATA ON DISK (read first; use Bash to aggregate — cite real numbers, never guess): ${DATA}/summary.json, ${DATA}/overviews.json (KD+global split+intent), ${DATA}/keywords.csv (full universe: keyword,volume,kd,cpc,clicks,parent,country,seed,category,funnel), ${DATA}/serp_summary.json + ${DATA}/serp/*.json (DR/UR + SERP features), ${DATA}/clusters.json, ${DATA}/traffic_by_domain.json. Raw dumps: ${RAW}.`

// ---------- schemas ----------
const CLUSTER_SCHEMA = { type:'object', additionalProperties:false, required:['clusters','total_addressable_volume','notes'], properties:{
  total_addressable_volume:{type:'number'}, notes:{type:'string'},
  clusters:{type:'array', items:{type:'object', additionalProperties:false, required:['name','intent','funnel','page_type','summed_volume','avg_kd','priority','top_keywords'], properties:{
    name:{type:'string'}, intent:{type:'string'}, funnel:{type:'string',enum:['TOFU','MOFU','BOFU']}, page_type:{type:'string'},
    summed_volume:{type:'number'}, avg_kd:{type:'number'}, priority:{type:'string',enum:['P0','P1','P2','P3']},
    top_keywords:{type:'array', items:{type:'object', additionalProperties:false, required:['kw','vol','kd'], properties:{kw:{type:'string'},vol:{type:'number'},kd:{type:'number'}}}} }}}
}}
const COMPETITION_SCHEMA = { type:'object', additionalProperties:false, required:['competitors','term_verdicts','format_insights'], properties:{
  format_insights:{type:'string'},
  competitors:{type:'array', items:{type:'object', additionalProperties:false, required:['domain','strength','note'], properties:{domain:{type:'string'},dr:{type:['number','null']},strength:{type:'string'},note:{type:'string'}}}},
  term_verdicts:{type:'array', items:{type:'object', additionalProperties:false, required:['term','ranking_format','beatable','rationale'], properties:{term:{type:'string'},ranking_format:{type:'string'},top_page_ur:{type:['number','null']},beatable:{type:'string',enum:['yes','maybe','hard']},rationale:{type:'string'}}}}
}}
const PSEO_SCHEMA = { type:'object', additionalProperties:false, required:['families','total_pages_estimate','total_volume_estimate','notes'], properties:{
  total_pages_estimate:{type:'number'}, total_volume_estimate:{type:'number'}, notes:{type:'string'},
  families:{type:'array', items:{type:'object', additionalProperties:false, required:['name','url_pattern','page_count_estimate','summed_volume_estimate','data_source','priority','examples'], properties:{
    name:{type:'string'}, url_pattern:{type:'string'}, page_count_estimate:{type:'number'}, summed_volume_estimate:{type:'number'}, data_source:{type:'string'}, priority:{type:'string',enum:['P0','P1','P2','P3']}, examples:{type:'array',items:{type:'string'}} }}}
}}
const PERSONA_DEF_SCHEMA = { type:'object', additionalProperties:false, required:['personas'], properties:{
  personas:{type:'array', minItems:4, maxItems:6, items:{type:'object', additionalProperties:false, required:['key','who'], properties:{key:{type:'string'},who:{type:'string'}}}} }}
const PERSONA_SYNTH_SCHEMA = { type:'object', additionalProperties:false, required:['angles','objections','keyword_seeds','verdict'], properties:{
  verdict:{type:'string'}, objections:{type:'array',items:{type:'string'}}, keyword_seeds:{type:'array',items:{type:'string'}},
  angles:{type:'array', items:{type:'object', additionalProperties:false, required:['angle','funnel','format','target_cluster'], properties:{angle:{type:'string'},funnel:{type:'string'},format:{type:'string'},target_cluster:{type:'string'}}}}
}}
const SECTION_SCHEMA = { type:'object', additionalProperties:false, required:['title','file','summary','takeaways'], properties:{
  title:{type:'string'}, file:{type:'string'}, summary:{type:'string'}, takeaways:{type:'array',items:{type:'string'}} }}

// ---------- PHASE 1: data analysis ∥ persona design ----------
phase('Analyze data')
const clusterThunk = () => agent(
`${CONTEXT}\n\n${METHOD}\n\nTASK: Build the COMPLETE keyword-cluster + funnel map from the live data. Read summary.json & overviews.json, then aggregate keywords.csv with Bash (dedupe, sum volume per topic, average KD). Group the whole universe into coherent clusters; per cluster classify intent, assign funnel (TOFU/MOFU/BOFU), recommend the page type per intent->format, sum volume, average KD, set priority (P0=low-KD+high-intent+volume). Surface the lowest-KD highest-intent BOFU opportunities explicitly. Recompute every figure from the CSV (state filters). WRITE the structured result to ${ANALYSIS}/clusters.json. Return it.`,
  {label:'kw-clusters', phase:'Analyze data', schema: CLUSTER_SCHEMA})
const competitionThunk = () => agent(
`${CONTEXT}\n\n${METHOD}\n\nTASK: Competitive SERP + traffic-gap analysis. Read serp_summary.json, ${DATA}/serp/*.json, traffic_by_domain.json. Identify incumbents + strength (DR, traffic share). Per money term: ranking FORMAT, top-3 URL-rating (page authority), SERP FEATURES present (ai_overview etc.), and a beatability verdict (yes/maybe/hard) grounded in real DR/UR. Note weak-page-authority openings and AIO exposure. WRITE to ${ANALYSIS}/competition.json. Return it.`,
  {label:'serp-gap', phase:'Analyze data', schema: COMPETITION_SCHEMA})
const pseoThunk = () => agent(
`${CONTEXT}\n\n${METHOD}\n\nTASK: Programmatic-SEO opportunity sizing. From keywords.csv (Bash-mine patterns) identify scalable long-tail FAMILIES (hundreds-thousands of low-KD pages): per-entity, per-attribute, per-occasion, per-location, per-relationship, and locale spelling variants as relevant to "${NICHE}". For each: URL pattern, honest page-count + summed/estimated volume (tag measured vs projected), the DATA SOURCE that makes each leaf non-thin, priority, 3 example titles+slugs. Design the hub->leaf tree. WRITE to ${ANALYSIS}/pseo.json. Return it.`,
  {label:'pseo-sizing', phase:'Analyze data', schema: PSEO_SCHEMA})
const designerThunk = agent(
`${CONTEXT}\n\nDesign 5 distinct ideal-customer personas for ${BRAND} (${PRODUCT}) in the "${NICHE}" niche — span buyer types, demographics, and gift-giver vs self-buyer. Each persona: a short \`key\` (kebab-case) and a vivid 1-2 sentence \`who\` (age, situation, mindset, device, price sensitivity). Return the structured object.`,
  {label:'persona-designer', phase:'Analyze data', schema: PERSONA_DEF_SCHEMA})

const [[clusters, competition, pseo], personaDefs] = await Promise.all([
  parallel([clusterThunk, competitionThunk, pseoThunk]),
  designerThunk,
])
log('Data analysis + persona design complete')

// ---------- PHASE 2: ICP personas + synthesis ----------
phase('ICP personas')
const PERSONAS = (personaDefs && personaDefs.personas) || []
const personaOut = await parallel(PERSONAS.map(p => () => agent(
`You are roleplaying a real ideal customer for ${BRAND} (${PRODUCT}). YOU ARE: ${p.who}\n\nStay in character. Give: (1) the exact phrases you'd type into Google at each stage — problem/top-funnel (don't know products exist), commercial (comparing), transactional (ready to buy); (2) your real hopes, doubts and objections about this product; (3) what content/page would make you trust and buy; (4) the occasions/triggers that send you searching. Quote real search phrasing. Prose + bulleted phrase lists.`,
  {label:'icp:'+(p.key||'persona'), phase:'ICP personas'})))
const personaSynth = await agent(
`${CONTEXT}\n\nSynthesize these ${PERSONAS.length} ICP persona transcripts into: ranked CONTENT ANGLES (funnel stage + best format + target cluster), top OBJECTIONS the site must overcome, and a deduped list of KEYWORD SEEDS they used. End with a one-line demand verdict.\n\nTRANSCRIPTS:\n${personaOut.filter(Boolean).map((t,i)=>`--- ${PERSONAS[i]?.key||i} ---\n${t}`).join('\n\n')}`,
  {label:'persona-synth', phase:'ICP personas', schema: PERSONA_SYNTH_SCHEMA})
log('Persona synthesis complete')

const DIGEST = `\n\n=== DATA DIGEST (cite/extend; full artifacts in ${ANALYSIS}) ===\nCLUSTERS: ${JSON.stringify(clusters).slice(0,6000)}\nCOMPETITION: ${JSON.stringify(competition).slice(0,4000)}\nPSEO: ${JSON.stringify(pseo).slice(0,4000)}\nPERSONA SYNTH: ${JSON.stringify(personaSynth).slice(0,3000)}`

// ---------- PHASE 3: strategy modules (parallel; each writes its section) ----------
phase('Strategy modules')
const mod = (key, file, brief) => () => agent(
`${CONTEXT}\n\n${METHOD}${DIGEST}\n\nYou are writing ONE section of an exhaustive SEO master plan. ${brief}\n\nGround every claim in the real data (read ${ANALYSIS}/*.json and ${DATA}/*.json; Bash for exact numbers; tag measured vs projected). Be concrete and prescriptive — tables, prioritized lists, exact keywords w/ vol+KD, URL patterns, examples. Write polished Markdown to ${file}. Return the structured summary.`,
  {label:key, phase:'Strategy modules', schema: SECTION_SCHEMA})
const modules = await parallel([
  mod('content-strategy', `${ANALYSIS}/03-content-strategy.md`, 'SECTION: Content Strategy & Editorial Plan. Pillars + hub-and-spoke clusters (TOFU that funnels to money pages, commercial comparison/gift-guide pages, BOFU landing pages). Map persona angles to pages. 12-month editorial calendar (month, title, target kw+vol+KD, intent, format, internal-link-to-money-page, funnel role). Show how high-volume TOFU funnels back. Include AI-Overview citation guidance per the AIO playbook.'),
  mod('information-architecture', `${ANALYSIS}/04-information-architecture.md`, 'SECTION: Information Architecture & Sitemap. Home (main short-tail commercial keyword + the converting tool), category hubs (one per cluster), PSEO long-tail layer, resource hub, conversion pages. URL scheme, breadcrumbs, internal-linking model (sub-pages link UP), locale mirror if multi-geo. ASCII sitemap tree + page-inventory table (URL pattern, type, target keyword, intent, priority).'),
  mod('technical-seo', `${ANALYSIS}/05-technical-seo.md`, 'SECTION: Technical SEO (build spec if pre-launch, audit-driven if live). Rendering (SSG/ISR for PSEO+hubs, staggered indexing for crawl budget), URL/canonical rules, international SEO + hreflang for the target geos (incl. spelling variants), structured data matrix (Product/Offer/Review/FAQPage/Article/BreadcrumbList/Organization), sitemaps/robots, Core Web Vitals budgets, image SEO, duplicate-meta avoidance across templated pages, CI guards, GSC/GA4 setup, indexing rollout. Concrete implementation notes + a checklist.'),
  mod('free-tools-funnel', `${ANALYSIS}/06-free-tools-and-funnel.md`, 'SECTION: Free-Tool TOFU & Conversion Funnel. Specific free tools that capture TOFU search and funnel to the paid product (target keywords w/ real vol+KD, why we win, the "make it easier" angle, upsell path, minimum How-it-works+FAQ). Then the full funnel TOFU->email->MOFU comparison->BOFU->purchase->repeat loop, with conversion assumptions.'),
  mod('authority-links', `${ANALYSIS}/07-authority-and-links.md`, 'SECTION: Authority & Link Building (12-month). Launch moves (Product Hunt, directories/gift-guides), link-stealing (name competitor backlink sources to pitch), affiliate program (commission model + who to recruit), HARO/digital-PR angles, content rings & free-tool magnets, influencer seeding. Prioritize by effort vs authority; target referring-domain counts to beat the KD<20 terms (cite incumbents\' refdomains).'),
  mod('kpi-forecast', `${ANALYSIS}/08-kpi-and-forecast.md`, 'SECTION: KPI Model, Traffic Forecast & Roadmap. Build the forecast with scripts/forecast.py (pass the prioritized clusters + PSEO families as pools with volume/kd/intent/aio/capture_share; apply the AI-Overview haircut). Show base + downside staged at 3/6/12/18 months and the arithmetic path to the traffic goal (and # of pages/content required). Conversion-to-revenue assumptions (separate measured vs projected), leading GSC/GA4 KPIs, and a phased 90-day + 12-month roadmap. Be honest about assumptions and AIO/forecast risk.'),
])
log('Strategy modules complete')

// ---------- PHASE 4: reconcile + synthesize ----------
phase('Synthesize plan')
const critic = await agent(
`${CONTEXT}\n\nYou are a ruthless completeness + NUMBER-RECONCILIATION critic (read ${PB}/research/number-reconciliation.md and ${PB}/maintenance/ai-overviews-and-serp-features.md). Read the sections at ${ANALYSIS}/03..08*.md and the JSON artifacts. RECOMPUTE every load-bearing number from ${DATA}/keywords.csv (state filters) and flag fabrications, conflicting figures, undocumented filters, measured-vs-projected blending, missed low-KD opportunities, and any forecast that ignores AIO. Also flag missing sections needed for completeness (measurement, Google-update/scaled-content resilience, internationalization, schema, repeat-purchase/LTV). Return a prioritized, specific list of fixes with the corrected numbers.`,
  {label:'reconcile-critic', phase:'Synthesize plan'})
log('Reconciliation critic done')
const sectionSummaries = modules.filter(Boolean).map(m=>`- ${m.title} (${m.file})\n  ${m.summary}\n  takeaways: ${(m.takeaways||[]).join('; ')}`).join('\n')
const synth = await agent(
`${CONTEXT}\n\n${METHOD}\n\nYou are the lead strategist assembling the FINAL master plan. Sections exist at ${ANALYSIS}/03..08*.md; artifacts at ${ANALYSIS}/*.json. Summaries:\n${sectionSummaries}\n\nReconciliation-critic findings to incorporate (use the CORRECTED numbers everywhere):\n${critic}\n\nDIGEST:\n${DIGEST}\n\nDO:\n1) WRITE ${ANALYSIS}/00-EXECUTIVE-SUMMARY.md — opportunity (addressable volume, low-KD money clusters w/ real vol+KD, the traffic path), strategy on a page, P0 quick wins, headline KPIs. Every number reproducible.\n2) WRITE ${A.dir}/SEO-MASTER-PLAN.md — master doc: exec summary, a TOC with WORKING relative links to each section file in this same directory, a consolidated P0/P1 backlog table, a 90-day roadmap, and a risk/resilience + measurement section addressing the critic (incl. the number reconciliations and AIO haircut).\n3) WRITE ${A.dir}/README.md — index of the deliverable (what each file is, how data was pulled, date, geos).\nKeep ALL files in the SAME directory and make links consistent. Return a confirmation listing files written + headline numbers.`,
  {label:'master-synthesis', phase:'Synthesize plan'})

return { clusters, competition, pseo, personaSynth, modules: modules.filter(Boolean), critic, synth }
