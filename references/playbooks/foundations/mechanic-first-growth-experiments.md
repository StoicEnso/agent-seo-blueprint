---
title: Mechanic-First Growth Experiments
area: foundations
operational_addition: true
sources:
  - "https://x.com/hnshah/status/2088663964116983856"
  - "https://x.com/gregisenberg/status/2088272956203966970"
  - "https://x.com/connorshowler/status/2088653427387584570"
  - "https://x.com/jammer3k/status/2088618901902901633"
source_type: creator-authored product theses, unverified SEO-claim list, and prohibited platform-evasion recipe
---

# Mechanic-First Growth Experiments

## Purpose

Use this playbook when a creator, competitor, platform, or adjacent product exposes a tactic that looks worth copying. Extract the **behavioral mechanism** first, then test whether that mechanism can create a useful behavior for this project. Do not clone the visible feature or repeat the creator's conclusion by default.

One source argues that cheaper software increases the value of judgment: teams can build more ideas, so they need stronger selection, smaller tests, and better learning loops. Another proposes consumer agents that close small avoided tasks by gathering context and preparing the action while the user keeps final control. These are useful product theses, not causal proof that a specific tactic, market, or forecast will work.

## Hard rules

1. **Define the behavior before the build.** Name the user or business behavior that should change and why it matters.
2. **Separate observation from explanation.** A visible feature, creator claim, engagement count, competitor adoption, or temporal sequence does not prove the mechanism or result.
3. **Transfer mechanisms, not surfaces.** Preserve the job and causal hypothesis; adapt the implementation to the project's audience, trust constraints, and product truth.
4. **Run the smallest reversible test.** Cheap implementation is not a reason to ship broadly.
5. **Pre-register the decision.** Record the primary metric, guardrails, minimum sample or time window, success threshold, failure threshold, and kill condition before launch.
6. **Keep external actions approval-gated.** Account creation, publishing, outreach, submissions, paid placement, and production changes need the normal user confirmation.
7. **Keep the learning when the test fails.** A stopped experiment can still improve the mechanism library; do not hide negative or null results.
8. **Refuse manipulation.** Manufactured consensus, negative SEO, parasite pages built mainly to exploit another site's signals, three-way exchanges designed to conceal coordination, click or traffic manipulation, fake personas, device or location spoofing and residential-proxy account setups intended to misrepresent geography, and policy evasion are not experiments to run.
9. **Keep consequential action with the user.** An agent may gather context, compare options, populate a draft, and ask for approval. It must not silently send, file, sign, dispute, switch, buy, cancel, or submit sensitive data.

## Method

### 1. Name the target behavior

Write one sentence in this form:

`For <audience>, increase/decrease <observable behavior> because it supports <business or user outcome>.`

Examples include completing onboarding, returning to update a project, verifying an agent's work, following a relevant internal link, reading an evidence page before conversion, or referring a qualified visitor.

Do not start with “we need this feature” or “we need this SEO tactic.”

### 2. Capture the source observation

Record:

- source URL, author/platform, and observation date;
- the visible feature or tactic;
- the source-authored claim;
- direct evidence available to this project;
- unknowns and alternative explanations; and
- constraints that differ between the source and this project.

Views, likes, bookmarks, rankings, links, or a creator's audience-growth number are context. They are not proof of causality.

### 2A. Grade claims before they enter the backlog

Assign one evidence grade:

- `PRIMARY_SUPPORTED` — a current first-party policy, product surface, public dataset, or project-owned measurement supports the narrow claim;
- `DIRECTLY_OBSERVED` — the project saw the state at a dated URL or in its own data, without a causal conclusion;
- `THIRD_PARTY_STUDY` — method and data are available but are not project-owned or independently replicated;
- `HYPOTHESIS` — plausible but not yet supported well enough to recommend; or
- `REJECTED_OR_PROHIBITED` — contradicted, too vague to test, or dependent on manipulation or policy evasion.

A creator list that says backlinks matter, sandboxes exist, exact-match domains win, Google cannot read content, consensus can be manufactured, or exchanges are undetectable contains several different claims. Do not accept the list as a package. Split each claim, define its observable meaning, check primary evidence, and drop claims that cannot support an ethical bounded test. Allegations about a company or ranking system are not reusable operating guidance without reliable evidence.

A device-setup recipe designed to make a platform treat an operator as if they were in another country is a platform-evasion recipe, not an SEO experiment. Do not turn it into an app, automation, or operating playbook.

### 3. Decompose the mechanism

Describe the sequence without product names:

`trigger -> reduced friction or new incentive -> user action -> feedback/state change -> reason to repeat`

For an SEO example, a third-party press-release page is not interesting merely because it can contain links. The possible mechanism is: a real company event becomes a public, shareable source page; relevant readers or journalists can discover it; qualified referral or editorial pickup may follow. Whether that mechanism works must be measured. “Dofollow page” is a surface property, not the user behavior.

### 3A. Screen a tiny avoided loop as a product-and-search wedge

The Greg Isenberg source proposes a narrow consumer-agent wedge: choose one small task people avoid because it combines context retrieval, a decision, and an uncomfortable or clerical action; prepare most of the work; let the user approve the final step. Its “biggest opportunity,” “47 little things,” and 12-month app forecast are **source-authored framing**, not measured market size, demand, or timing.

A qualifying loop should have:

- a named audience and one repeatable trigger;
- direct evidence that the task recurs or remains unfinished;
- a clear user cost in time, money, stress, or missed opportunity;
- context that can be accessed with informed consent and data minimization;
- a prepared output the user can inspect and correct;
- an explicit approval boundary before any consequential action;
- an observable closure receipt; and
- a safe failure, expiry, and deletion path.

Map the mechanism as:

`trigger -> consented context -> options/evidence -> prepared action -> explicit approval -> external action -> closure receipt`

The default safe boundary is **prepare, do not commit**. The agent may collect allowed records, compare options, calculate, populate a form draft, draft a reply, and remind the user. It must not send a message, file a claim or dispute, sign a form, switch a provider, purchase or cancel a service, submit child or school data, or make a legal, financial, health, insurance, or eligibility decision without current user approval and the required authority.

For an SEO or product opportunity, the creator thesis is not keyword evidence. Validate the loop separately with current search demand, intent, a live SERP, first-party user evidence, existing alternatives, and willingness to pay. Start with one loop and one audience; do not manufacture a programmatic page set from a list of chores.

Copy `assets/tiny-loop-opportunity-map.csv` to `research/<date>_tiny-loop-opportunity-map.csv`. Record the evidence, access basis, approval boundary, primary metric, and guardrails before a build. Useful measures include eligible-loop frequency, prepared-action acceptance, verified closure rate, time to close, correction rate, false-trigger rate, approval rejection, and trust or privacy incidents.

### 4. Test transfer fit

Score `0–2` for:

- audience and problem match;
- behavior match;
- trust and policy fit;
- evidence strength;
- implementation reversibility;
- measurement quality;
- maintenance cost; and
- likely business relevance.

Reject the idea if it needs fake personas, fabricated engagement, copied content, platform-policy evasion, undisclosed incentives, link manipulation, or a result that cannot be observed.

### 5. Design the minimum viable test

Specify:

- one hypothesis;
- one primary change;
- one primary metric;
- no more than three guardrail metrics;
- baseline and comparison method;
- cohort, page, query, or audience scope;
- start/end dates or minimum sample;
- owner;
- rollback or stop method; and
- what will remain unchanged.

Avoid testing a new format, new audience, new offer, and new channel at the same time.

### 6. Run a bounded learning loop

Use:

`observe -> explain -> hypothesize -> test -> measure -> decide -> record`

The decision is `adopt | revise | reject | inconclusive`. “Shipped” is not a result. Do not expand until the original test reaches its decision gate.

### 7. Add the result to a mechanism ledger

Write `research/<date>_mechanic-experiment.json` with:

`source,observation,target_behavior,mechanism,hypothesis,transfer_assumptions,test_scope,primary_metric,guardrails,baseline,decision_thresholds,start_at,end_at,result,decision,limitations,next_test,owner`

Preserve failed and inconclusive rows. They prevent the same weak idea from being rediscovered and rebuilt.

## Decision rules

- **Adopt:** the primary metric passes its threshold, guardrails stay acceptable, and no policy or trust failure appears.
- **Revise:** the mechanism remains plausible, but evidence identifies one bounded implementation defect.
- **Reject:** the result misses the failure threshold, creates harmful guardrail movement, or requires manipulation.
- **Inconclusive:** the sample, attribution, or test integrity cannot support a decision. Do not call this a win.

## Done condition

The source claim and direct evidence are separated; the target behavior and mechanism are explicit; one reversible test has pre-registered success, failure, and kill conditions; external writes remain gated; and the final decision records limitations as well as results. For a tiny-loop wedge, the audience, trigger, consented context, approval boundary, closure receipt, safe failure path, and independent search or user-demand evidence are also recorded.
