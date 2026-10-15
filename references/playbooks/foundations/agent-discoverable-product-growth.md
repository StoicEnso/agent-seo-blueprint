---
title: Agent-Discoverable Product Growth — Railway Marketing Playbook
area: foundations
operational_addition: true
source_lessons: []
sources:
  - https://www.knuckleup.co/episodes/jake-cooper
  - https://www.youtube.com/watch?v=LQNqM1mA2e8
  - https://x.com/illyism/status/2110205324586270827
  - https://railway.com/changelog/2026-06-26-railway-over-ssh
source_type: full publisher transcript, creator commentary, and current first-party product documentation
---

# Agent-Discoverable Product Growth

## What this is

This is the complete **marketing-relevant playbook extracted from the whole Railway interview**, not just the four points in the linked post. It includes acquisition, positioning, product access, pricing, feedback, launches, team leverage, planning, trust, measurement and the operating conditions that support them. It is an original synthesis, not a reproduction of the interview.

The source is Knuckle Up episode 15 with Railway founder Jake Cooper and host Nakul Mandan, published 13 October 2026. All 330 publisher transcript paragraphs were reviewed. The saved transcript was fetched again on 15 October and matched the earlier saved text exactly. The speech has not been independently checked against all audio. Paragraph references below identify the publisher text, including speaker-label paragraphs. They are not line numbers or exact speech timestamps.

**There is no disclosed, fully specified Railway SEO recipe in this interview.** Cooper describes trying to make models recommend Railway. He does not disclose the prompts, source-placement mix, training method, citation data, attribution study or conversion results. The claim that paid listicle placements are the way to reproduce Railway's growth comes from the linked creator's commentary and sales links. It is not established by the interview.

The interview's near-$100 million annual recurring revenue (ARR), roughly 40-person company and lean team figures are source statements, not independently audited results. The post's growth attribution is not causal evidence. A later goal of roughly $500 million and 80–100 people is an ambition, not an achieved result. No tactic here guarantees adoption, recommendations, rankings, links, traffic or revenue.

## When to use it

Use this when a useful product must become easier for both people and their agents to discover, evaluate, try and trust. Use it to turn an interview into a testable operating plan, or to review a vendor's agent-facing sales skill. Do not start by buying links or building an interface no user needs.

Load the existing `mechanic-first-growth-experiments.md` playbook first for experiment design. Use `workflows/category-citation-loop.md` and `workflows/ai-answer-visibility-loop.md` for observed recommendations and citations. Use `workflows/content-production.md` for evidence assets, `workflows/authority-and-links.md` for independent editorial opportunities, and `workflows/monitoring.md` for measurement. This is a cross-workflow method, not a new automatic publisher or purchasing agent.

## Read the four layers separately

1. **Interview report:** what Cooper or Mandan actually says. A reported company practice is not an independently proven growth cause.
2. **Current product evidence:** what an official page documents at the check date. Access, eligibility and limits can change.
3. **Creator/vendor interpretation:** the linked post's explanation and commercial offer. This is not Railway's endorsement or procurement policy.
4. **Proposed experiment:** our bounded adaptation. It is not something Railway was proven to have done.

The tweet's 09:20, 13:47, 25:35 and 31:50 are its approximate navigation pointers. The publisher supplies broad chapter links, not utterance-level timestamps. Do not turn those pointers into precise audio-verified citations.

## The complete mechanism library

### M01 — Start with a real, narrow job

**Interview report, P010 and P062:** Railway started with a practical database-provisioning problem, then expanded into backends, frontends and other workloads. Its initial prototype attracted interest before a formal company strategy emerged.

**Mechanism:** a concrete job is easier to explain, demonstrate, recommend and evaluate than a broad claim to be everything for everyone. Adjacent expansion can follow real usage.

**Adaptation:** name one audience, trigger, input and useful output. Show one working example. Measure completion of that job before adding new category claims. Reject a vague agent interface that has no observable customer outcome.

### M02 — Make pricing and delivery economics work before scaling acquisition

**Interview report, P014–P030:** Railway removed an uneconomic free tier, accepted lower signups, invested in its underlying infrastructure and later restored a free offering it believed it could support. Growth had multiple inflection points and a long trough.

**Mechanism:** free usage is not healthy growth when servicing it loses money without a credible conversion path. The trial offer depends on actual delivery costs and customer progression.

**Adaptation:** model cost per completed job, abuse, support effort, conversion, paid retention and contribution margin. Test a capped sample or sandbox if it is useful and affordable. Do not copy Railway's pricing change without the same economics. Lower signup volume can be the right result if paid value and sustainability improve.

### M03 — Match the changing user workflow, not the fashionable label

**Interview report, P030 and P038:** Cooper connects demand with better models and more background agent workloads. He describes dashboard, command-line and Model Context Protocol (MCP) access alongside long-running jobs.

**Mechanism:** a product gains a new entry point when it meets work where the user or their software already operates. An MCP is a standard way for an AI application to use external tools; it is not itself a demand channel.

**Adaptation:** observe an actual workflow. Compare a normal web path with a small agent-friendly path. Track qualified task starts, successful outputs, retries, permission failures, paid activation and retention. An installed integration or tool call is not a customer win.

### M04 — Reduce time to first value, but preserve identity and permission boundaries

**Interview report, P038:** Cooper describes immediate virtual-machine access without prior signup. The tweet calls this zero-signup access.

**Current product correction:** Railway's inspected SSH changelog documents `ssh railway.new`, `ssh agent@railway.new` and `ssh sandbox@railway.new`. Secure Shell (SSH) is an existing terminal connection method. The page says a new machine receives a signup/sign-in and SSH-key approval link. It describes Priority Boarding access. Therefore **no separate installation is not the same as no account, no authentication or universal anonymous access**. The post's `ssh railway new` wording is not the documented command. These commands are source examples, not instructions to run during this audit.

**Adaptation:** let a user inspect a rights-safe sample or prepare a draft before demanding unnecessary setup. Keep authentication, tenant isolation, quotas, data rights and consequential approvals. Measure time to first valid result and abuse rate together. Never expose customer systems or remove legal review merely to improve activation.

### M05 — Treat recommendation and execution as two different problems

**Interview report, P134:** Cooper describes working both on models recommending Railway and on models using Railway infrastructure. He does not disclose the implementation of the recommendation work.

**Mechanism hypothesis:** the product must be understandable at selection time and usable after selection. Visibility without successful use is weak; excellent tooling without discovery can remain invisible.

**Adaptation:** keep separate work queues for (a) observed buyer questions, recommendations and citations, and (b) the ability to complete an authorised product task. Improve truthful docs, limits, examples and evidence where a real gap exists. Never claim to retrain, incept, poison or control an answer model through paid mentions. Keep provider recommendations separate from tool-execution success.

### M06 — Use first-party user evidence as the main product check

**Interview report, P050:** Cooper describes collecting sentiment, feedback and launch context in an internal system called Central Station, with a content-management system for launches. This report does not establish that the public community site and every internal system are the same implementation.

**Mechanism:** a joined feedback record can connect the problem, decision, shipped change and response. It reduces lost context between product, support and marketing.

**Adaptation:** begin with a small evidence inbox. Give each consented feedback item a source, date, audience/job, issue, owner and linked decision. Remove personal data not needed for the task. Separate repeated demand from one loud request. Measure closed loops and changed behaviour, not ticket volume alone.

### M07 — Dogfood the same customer path

**Interview report, P050:** Cooper says the team should use its own product more and make its own workflows run on the product's primitives.

**Mechanism:** repeated use exposes setup gaps, confusing concepts and unreliable paths that a landing-page review misses.

**Adaptation:** run a permitted internal or synthetic task through the same documented path a customer uses. Record every manual rescue and permission failure. Turn the largest repeated failure into a narrow fix and verify it again. Internal satisfaction is useful feedback, not proof of market demand or a testimonial.

### M08 — Collect market intelligence, then change the mechanism for your audience

**Interview report, P042–P054:** Cooper discourages copying engineering answers without understanding them, but explicitly describes marketing inspiration from other firms. He names a market-intelligence channel, Ramp and a turbopuffer ad. He asks how Railway can make an idea distinctive.

**Mechanism:** study why an asset wins attention or communicates value. Transfer the useful pattern, not the design, brand or unsupported outcome.

**Adaptation:** keep a small swipe file with the observed audience, hook, proof, offer, distribution, response and unknowns. Write the proposed mechanism in one sentence. Make one distinct, evidence-backed draft. Do not treat an inspiring advertisement as a measured result, or copy another firm's creative work.

### M09 — Spend limited innovation effort where it differentiates

**Interview report, P046:** Cooper discusses choosing build-versus-buy battles and the concept of innovation tokens.

**Mechanism:** custom work has an opportunity cost. Building every marketing system consumes the attention needed for the few parts that matter.

**Adaptation:** compare a manual workflow, an existing tool and a small custom solution. Record total cost, maintenance, data exposure, lock-in and reversibility. Build only when a documented gap justifies it. Buying access does not establish quality; a sales skill does not replace a strategy.

### M10 — Advance the biggest business constraint each week

**Interview report, P034 and P254:** Cooper rejects a single trick for a vertical growth chart. He describes one meaningful company problem moved forward each week across product, messaging, positioning, sales and operations.

**Mechanism:** focused, repeated improvements can compound. This is an operating principle, not a promised growth rate.

**Adaptation:** choose one main constraint with evidence. Define a shipped artefact and an observable business or user result. Keep a weekly record of the baseline, action, result, uncertainty and next decision. Do not count posts, pages or agent runs as progress when the bottleneck is conversion, delivery or retention.

### M11 — Require a short proposal and a clear reason to act now

**Interview report, P086–P090:** Railway reportedly declines most initiatives. Proposals include background, problem or opportunity, and why the work matters now. The team plans and challenges its choices quarterly.

**Mechanism:** prioritisation prevents cheap production from creating an unlimited backlog. Recurring demand can change the timing decision.

**Adaptation:** use a one-page brief: audience, evidence, opportunity, alternatives, reason to act now, expected result, owner, effort, limits and stop rule. Keep a reason to defer. A source's 90% rejection figure is not a target quota for another business.

### M12 — Learn the work manually before automating it

**Interview report, P102:** Cooper describes doing a job manually to understand its real steps before system design or hiring.

**Mechanism:** manual examples expose exceptions and the actual job to be done. Automating an assumed process can scale the wrong task.

**Adaptation:** examine 3–10 representative, permitted examples. Record inputs, decisions, error cases, outputs, corrections and completion receipts. Automate only the stable preparation steps. Keep judgement and consequential action behind review until evidence supports a safer boundary. No batch sends are authorised by this method.

### M13 — Let go-to-market staff build systems, not only add activity

**Interview report, P092–P106:** The stated team is one sales representative, one product marketer, two solutions engineers, one growth marketer and two developer-relations staff. That is seven stated roles; the host loosely calls it seven or eight. Cooper says recruiting and sales write code and automations. He does **not** say there is no manual outreach or no human sales work.

**Mechanism:** a small team can gain leverage from reusable preparation, routing and measurement. It still needs real human expertise and customer contact.

**Adaptation:** make one role own a complete loop, with a reusable tool, maintained evidence and a clear output. Measure valid work per hour, correction rate, customer value and maintenance burden. Do not claim one growth marketer caused all revenue, prescribe a universal headcount, or remove review because an automation exists.

### M14 — Use player-coaches and explicit ownership

**Interview report, P058, P110–P126 and P150:** Cooper favours hands-on leaders, autonomy and people who can improve systems. He separates broad idea exploration from focused execution.

**Mechanism:** someone must be able to do the work, judge quality, remove constraints and own the decision. A large number of agents does not replace that role.

**Adaptation:** name one responsible owner per experiment. Give them a bounded scope and review rights. Test a small work sample for evidence quality and correction skill. Keep the approval owner separate from the vendor. Avoid turning personal founder or recruitment preferences into universal employment rules.

### M15 — Onboard marketers and agents through trust, clarity and judgement

**Interview report, P158–P178:** Railway's described onboarding moves from small tasks to problems with trade-offs and then a proposal for what the business needs. Cooper describes roughly two weeks for each stage, with a scratchpad and visible progress.

**Mechanism:** context and feedback build reliable autonomy. New people or agents should not start with broad, unsupervised authority.

**Adaptation:** first complete a few safe evidence tasks. Then write and defend a small experiment brief. Only after that propose an independent priority. Use the existing permission controls throughout. The six-week sequence is a reported practice, not a mandatory duration or permission grant.

### M16 — Balance attractive work with essential maintenance

**Interview report, P182:** Cooper explicitly rejects everybody choosing only exciting projects. Teams take named commitments and include necessary reliability or abuse work.

**Mechanism:** acquisition can create problems that defeat the product promise. Marketing capacity must allow for delivery and trust work.

**Adaptation:** protect a named owner for support, data quality, security, documentation and broken conversion paths. Do not spend the entire cycle on visible campaigns while core evidence or delivery fails. The interview's rough work mix is descriptive, not a staffing formula.

### M17 — Attach context to the work item

**Interview report, P186–P190 and P214:** Remote work needs deliberate systems. Railway reportedly links meeting transcripts and decisions to planning items. Cooper describes using richer conversation when it is useful, then compressing the context. He also says internal memos should not be carelessly generated and passed to colleagues.

**Mechanism:** an inspectable brief and source context reduce handoff loss. The goal is clarity, not maximal document length or meetings at all costs.

**Adaptation:** record consented decisions, owners, evidence and next actions on the relevant item. Keep a short human-reviewed summary. Do not record private calls without consent, dump whole inboxes into agents, or treat generated prose as a checked decision.

### M18 — Build distribution around real shipped progress

**Interview report, P194:** Cooper reports a Friday changelog every week since 2021. This is a source claim; this review did not audit every historical release.

**Mechanism:** real product improvements create a repeatable reason to communicate. A changelog can connect a user problem, working change and next action.

**Adaptation:** prepare a proof-led release note with the affected audience, change, evidence, limits and usable next step. Publish only after the actual change and exact approval. Update the relevant docs and support context. A weekly release cadence is not a requirement to invent news or publish low-value pages.

### M19 — Make truthful claims and incident communication part of marketing

**Interview report, P194–P202:** Cooper discusses honour, acceleration, reliability and directness. He argues against dark patterns and overselling, and describes public incident reports and fast follow-up during reliability problems.

**Mechanism:** trust depends on whether the delivered product and failure handling match the promise. Hiding material limits can harm both adoption and retention.

**Adaptation:** keep a claim ledger for features, pricing, dates, evidence and limits. Distinguish live, beta and planned features. Prepare honest incident updates with scope, current state and confirmed facts. Do not promise an incident-response time or service level merely because Railway described one.

### M20 — Treat enterprise sales as a relationship problem when it is one

**Interview report, P210:** Cooper says enterprise penetration can require personal relationships and is hard to solve entirely through systems. Earlier revenue targets did not remove that need.

**Mechanism:** procurement, trust and stakeholder needs may outgrow a pure self-serve path. Automation can prepare evidence without replacing accountable conversation.

**Adaptation:** distinguish small self-serve users from organisations that need due diligence, contracts and expert review. Build a truthful evidence pack and a consented handoff. Measure qualified progression and retained value. Do not infer that an agent-facing skill eliminates salespeople or legal review.

### M21 — Revisit priorities when capabilities change

**Interview report, P138–P150 and P250:** Cooper describes changing a roadmap after model improvements and raising the bar for useful work. He also acknowledges being wrong.

**Mechanism:** cheaper implementation changes what can be tested. It does not prove that every new capability has demand.

**Adaptation:** revisit one blocked experiment when a genuine capability changes. Retain its old baseline and failed assumptions. Require fresh product and user evidence. Do not let a new model silently expand permissions, launch budgets or add dozens of initiatives.

### M22 — Close the whole delivery loop

**Interview report, P230–P234:** Cooper discusses scoped permissions and a lifecycle from development through staging, feature flags, monitoring and support feedback. These are reported engineering practices, not an authorisation to deploy or give an agent a wallet.

**Mechanism:** faster production increases the importance of safe rollout and observing real outcomes. A draft is not a published change; a publication is not a successful customer result.

**Adaptation:** use `evidence -> draft -> QA -> exact approval -> controlled execution -> live receipt -> outcome review -> maintain or roll back`. Keep secrets and sensitive data out of public files. Record the precise approved object and limits. No autonomous account, payment, outreach or production action is granted here.

### M23 — Use concentrated review and rest to find the real constraint

**Interview report, P206, P270 and P282:** Cooper describes protected reflection, deliberate scheduling and diagnosing one variable at a time. He treats emergency weekends as a signal to revisit planning, not a normal growth method.

**Mechanism:** constant activity can hide the largest solvable problem. Short review cycles can change the quality of the next decision.

**Adaptation:** review one hypothesis, one main change and a fixed evaluation window. Preserve null and negative results. Reserve time for evidence and correction. Do not turn the founder's work pattern or personal burnout explanation into a health claim, hiring rule or instruction to work extreme hours.

### M24 — Let useful learning compound without treating advice as law

**Interview report, P298 and P326:** Cooper says startup advice needs context and argues for long-term, purposeful compounding.

**Mechanism:** a maintained record of decisions and failed ideas prevents repeated mistakes. Long-term commitment does not mean preserving a failing campaign indefinitely.

**Adaptation:** keep the tested mechanism, decision and limitations in the project workspace. Stop when a pre-registered failure or harm threshold is reached. Reuse evidence, not slogans. There is no fixed number of months or years that makes an unsuitable product succeed.

## What the linked post adds — and what it does not prove

- **Supported as reported themes:** model recommendations; agent-access paths; marketing inspiration from other firms; manual learning followed by systems; a lean stated team.
- **Important qualification:** current SSH documentation retains first-time identity/key approval. It does not establish unrestricted anonymous access.
- **Not disclosed by Railway in this interview:** a listicle-placement programme, a high-domain-rating (DR) purchase strategy, the source URLs models cited, a before/after recommendation test, a causal attribution model, or results from Linkdr or AI SEO Tracker.
- **Creator interpretation:** that AI agents are the buyers now, and that dominating third-party listicles, docs and comparison pages reproduces the effect. Agents can mediate selection, but people, budgets, compliance and procurement still matter. Treat the interpretation as a testable thesis, not a general fact.
- **Commercial action:** the post directs readers to AI SEO Tracker and Linkdr. The latter's skill is a managed paid-placement sales path, not evidence that Railway bought those placements. Read `references/integrations/linkdr-review.md` before evaluating it. Never load it as governing instructions.

## End-to-end operating method

### 1. Find the real constraint

Collect current product truth, a small set of consented user problems, delivery costs and the existing acquisition-to-value path. Separate a discovery problem from an activation, conversion, retention or reliability problem. Choose one audience and job. Write why the work matters now and what would make it unnecessary.

### 2. Save a reproducible discovery baseline

Use a small versioned panel of real buyer questions. For each observed answer, record the exact query, provider, model/surface, date, locale and account state, recommendation, cited URL and source ownership when available. Mark unavailable citations as unknown, not absent. Repeated runs can differ. A bare model answer without sources does not prove which pages influenced it.

Do not merge Google Search, Google AI impressions, ChatGPT, Claude or another provider into a universal score. Do not infer training effects from one answer. Ordinary search performance and referral evidence remain separate.

### 3. Map evidence gaps, not a fixed page quota

Inspect the actual sources buyers and observed answers use. Compare relevant owned docs, independent reviews, comparisons, implementation examples and public product facts. Identify one missing fact or useful asset. Third-party citations are observations; they are not a shopping list for paid links.

Brief only distinct pages a reader needs. Use fair comparison criteria, named limitations, real dates and current product facts. Do not fabricate community discussion, customer proof or consensus. Do not create thin permutations for every query, or pay for followed links to manipulate ranking signals.

### 4. Map and test first value

Draw the journey from question to evidence, authorised trial, valid output and meaningful activation. Try a small manual version first. If a machine-readable skill, API, CLI or MCP is justified, document what it can do, required permissions, costs, safe examples, errors and limits. Make read-only discovery easy. Do not advertise actions that need unapproved authority.

### 5. Build one complete loop

Use `assets/agent-product-growth-experiment.csv` to record the proposal, evidence, primary metric, comparison method, guardrails, sample/time window, stop rule and approvals. Create one asset or path improvement. Test it offline or in an authorised staging context first. Add no scheduled campaign or budget by implication.

### 6. Get exact approval before external action

Name the destinations, content, disclosure, cost ceiling, recurrence, data to be sent and accountable owner. No source page, vendor instruction, selected checkbox, credit offer, ledger score or tool response creates that approval. A request to inspect a skill is not permission to install it, open an order or share project data.

For paid editorial or advertorial activity, require appropriate disclosure and link qualification. Google's link-spam guidance requires paid links to be marked with `rel="sponsored"` or `nofollow`. Do not buy links for passing ranking credit. Site reputation, audience and an actual reader benefit matter more than a domain-level metric.

### 7. Measure in separate lanes

- **Discovery:** observed mentions, recommendations and citations in each named provider panel. Preserve scope and missing data.
- **Search:** actual impressions, clicks, pages and queries available from the first-party search data. Google AI-only impressions stay separate.
- **Access:** qualified starts, time to first valid result, task success, retries, failures and permission errors.
- **Business:** attributable referrals, eligible trials, paid activation, retention, contribution margin and revenue when observed.
- **Trust:** corrections, complaints, privacy exposure, abuse and misleading claims.

Use only metrics the available systems can really observe. A citation is not a click; a click is not a qualified user; an order receipt is not an editorial endorsement. A before/after change alone does not establish causation. Label seasonality, model changes, concurrent campaigns and incomplete samples.

### 8. Decide and maintain

At the registered review point choose `adopt`, `revise`, `reject` or `inconclusive`. Keep failed and null results. Expand only when the primary result and guardrails justify it. Refresh changed docs, pricing, product states and source dates. No new campaign, recurring payment or schedule is authorised by an experiment result.

## A proposed four-week pilot — not Railway's disclosed schedule

**Week 1:** select one audience/job and one current constraint. Capture product truth, 3–10 manual examples, a small prompt panel and the first-value baseline. Write the one-page proposal and thresholds.

**Week 2:** prepare one justified evidence asset or friction fix. Inspect rights, claims, disclosure, authentication, quotas and errors. Review it in a safe environment. Prepare any external action as a draft only.

**Week 3:** if exact approval exists, run the bounded change and retain live receipts. Otherwise finish offline QA and keep it ready. Collect customer feedback without inventing outcomes or expanding scope.

**Week 4:** compare the registered outcomes with the baseline and limitations. Review provider observations, task success, business outcomes and trust separately. Decide to stop, revise, continue observation or seek approval for a further test. Four weeks may be too short for a recommendation, retention or revenue conclusion; use `inconclusive` when needed.

## Examples, not live product instructions

- **A visual planning tool:** show a sample concept and clear limits before asking for an account. The concept must not imply verified drainage, build cost or plant suitability. Measure valid concept-to-brief completion, not image generation count.
- **A customs-document tool:** prepare a sample pack with a visible human exception queue. Do not advertise autonomous filing or remove the authorised declarant's responsibilities. Measure corrected field completeness and review effort on rights-safe inputs.
- **A carrier-data tool:** show a dated, sourced licence record and its limits. Do not imply live monitoring, safety or solvency from a snapshot. Measure whether users can complete the narrow evidence task correctly.

These examples transfer the mechanism without copying Railway's interface or weakening the product's legal and trust constraints.

## Pitfalls

- Mistaking a founder interview for audited attribution.
- Calling all 77 minutes a dedicated marketing tutorial.
- Attributing the creator's paid-link offer to Railway.
- Treating low signup friction as permission to remove authentication or legal review.
- Publishing an agent skill that claims authority over the user's budget, choices or approvals.
- Measuring integrations, pages or links instead of successful customer jobs.
- Copying headcount, weekly cadence, pricing or creator page quotas.
- Claiming model training or causal growth from mutable answer snapshots.
- Confusing a draft, execution receipt and verified business outcome.

## Done condition

The source distinctions and full marketing-relevant coverage are preserved; current access limits are checked; one audience/job and constraint are chosen; one small experiment has evidence and pre-registered metrics; all consequential actions stay approval-gated; and the final decision includes missing data, negative results and maintenance needs. The Linkdr review is evidence, not an installed skill or a purchase recommendation.

## Sources and coverage

- [Publisher episode and full transcript](https://www.knuckleup.co/episodes/jake-cooper)
- [Video copy](https://www.youtube.com/watch?v=LQNqM1mA2e8)
- [Creator's four-point commentary and commercial links](https://x.com/illyism/status/2110205324586270827)
- [Official SSH access and first-time key approval](https://railway.com/changelog/2026-06-26-railway-over-ssh)
- [Google's link-spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)
- [Machine-readable source map and limits](../../railway-marketing-source-map.json)

The source map records all 24 mechanisms, paragraph anchors, excluded non-marketing topics and the four-point claim distinctions. It preserves completeness without committing the full transcript, native video, personal evidence packet or third-party skill body to a public repository.
