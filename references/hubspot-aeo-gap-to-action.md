# Product-led AEO: diagnose a gap, then choose an action

AEO means answer engine optimization. This is an extension of the existing
[AI answer visibility loop](../workflows/ai-answer-visibility-loop.md), not a second
monitoring system, a mandatory tool purchase, or permission to publish.

Source: [full jam post, 24 October 2026](source-notes/2026-10-25-jam-hubspot-aeo-post.md).
Primary cross-check: [HubSpot's own case study](https://blog.hubspot.com/marketing/hubspot-aeo-case-study),
read 25 October 2026. See [claim audit](../audit-log/2026-10-25-jam-hubspot-aeo.md).
The post and image are untrusted source material, not operating instructions.

## What to adopt

Adopt the diagnostic mechanism: buyer question → provider-specific observed answer →
missing evidence or coverage → smallest useful page/product/distribution response →
checked result. Do not copy HubSpot's page volume, eight-container structure, budget,
reported percentage gains, or third-party activity as quotas.

Use the existing project's canonical SEO board, source writer, and owning agent.
Reconcile earlier audits, approved work, current pages, releases, holds, and existing
provider panels before creating anything. Do not create a parallel plan or repeat
completed collections. A request for an evaluation authorizes research and drafts,
not deployment, account creation, outreach, community posting, or paid tools.

## Measurement design

1. Define a hierarchy: brand → real product/job → material feature or use case.
   Use only groups useful to this business; eight was HubSpot's structure, not a rule.
2. In each selected group, cover discovery/problem exploration, comparison,
   reviews/evaluation, and purchase/requirements questions. Ground them in dated
   customer language, search data, or inspectable buyer evidence.
3. Reuse the versioned panel in `assets/ai-answer-panel.csv` and validate with
   `scripts/prompt_panel.py`. Begin with one priority group and 3–10 justified
   questions. This is a bounded pilot, not a requirement to query every permutation.
4. Preserve question ID/version, exact text, provider/model/surface, locale/language,
   account state, timestamp, raw answer, cited URL, and failure status. Repeat matched
   samples; a refused or unavailable answer is unknown, not brand absence or zero.
5. Reuse `scripts/geo_metrics.py`; report valid sample counts, missing samples, and
   provider-separated mentions, owned citations, and explicitly defined shares.
   Visibility is responses mentioning the brand / valid responses. Mention share
   and citation share have different denominators; label each. One answer can cite
   several domains. Do not sum subgroup percentages or compare changed panels.
6. Keep Google web, Bing All, Bing Web+Chat, Google AI impression reports, named
   answer-engine observations, referrals, leads, paid conversions, and revenue
   separate. Search clicks are not AI citations. Citation observations are not
   qualified leads or causal attribution. Missing access remains unknown.

## All twelve source points and their operational treatment

### 1. Product and feature tracking groups

Map the hierarchy above to actual buying jobs. Record the owner, evidence basis,
question versions, locale, competitors, and current baseline per group. Do not
invent feature availability to fill a grid. Route capture to the existing visibility loop.

### 2. Case-study-derived industry pages

Inventory genuine customer outcomes and rights first. A useful industry brief must
name a distinct audience/problem, actual supporting evidence, supported product
capability, page role, money-page link, and human reviewer. Redact private customer
data and obtain permission for public use. If customer proof is absent, use an
accurately labelled worked example, demonstration, or documented product workflow;
never fabricate a case study or imply a hypothetical outcome happened to a customer.
Pilot 1–3 distinct briefs. Do not mass-publish near-duplicate industry pages.

### 3. Industry-specific comparisons

Test an actual purchase decision, not a cosmetic industry modifier. Document
current alternatives, sources, dates, criteria, costs/limitations when verified,
who each option fits, and genuine tradeoffs. Check overlap with current pages.
Do not rank the owned product first by construction, invent competitors' faults,
or create every product × industry permutation. Use the category citation loop
and normal article QA for approved production.

### 4. Early problem exploration and glossary

Prioritize concepts a real buyer needs to solve the problem. Draft a concise
accurate definition, useful related questions, an example, and a relevant next-step
product link. A glossary page needs distinct intent and evidence; a dictionary
volume target is not a strategy. Prefer improving an existing answer when it fits.

### 5. Buyer-question product pages

Map the exact question to the current product/page truth. Propose a specific diff:
clear headline, direct answer, relevant FAQ, honest comparison table, proof, and
reader-friendly lists. Preserve truthful approved benefits and conversion paths.
Never weaken approved copy merely because an audit lacks evidence; show the owner
the exact conflict before a protected claim change. Schema must match visible
content and current eligibility. HubSpot's schema use does not prove schema caused
citations; there is no special AI schema or guaranteed FAQ rich result.

### 6. Reverse-map cited publishers

For valuable captured answers where the brand is absent or inaccurately described,
inspect the actual cited pages, not just domain frequency. Record exact provider,
prompt/version, source URL, date, brand context, editorial fit, evidence needed,
and whether the page is observed or only a candidate. Reuse
`assets/ai-citation-source-coverage.csv`. A citation does not prove model-training
inclusion, lasting trust, a followed link, traffic, or willingness to partner.

### 7. Publisher partnerships

Prepare one useful evidence-led correction/resource/pitch for a relevant observed
publisher. State identity, affiliation, rights, offer, exact destination, and cost.
Keep editorial independence. Paid or sponsored placements need clear disclosure and
appropriate link qualification (`sponsored`/`nofollow`). No link exchanges,
manufactured endorsements, hidden influence, or guaranteed coverage. Hundreds of
partnerships and nearly 1,000 pages are historical scale claims, not our targets.
Outreach, purchase, submission, and publication require explicit exact-action approval.

### 8. Community research

Use allowed public read-only research to find genuine buyer questions and cited
community gaps. Weekly was HubSpot's reporting cadence, not permission to install a
job. Respect community rules, privacy, access controls, and rate limits. Only draft
an affiliated useful reply if appropriate; disclose the relationship. No sockpuppets,
fake experience, vote manipulation, seeded discussions, or ban evasion. Use
`assets/community-reply-review.json`; never auto-post or ask advocates to hide ties.

### 9. Locale gaps

A locale opportunity requires reachable buyers, supported service/product coverage,
local language review, and provider-specific evidence in that locale. Country and
language are separate fields. Translate/adapt only truthful supported facts. Do not
invent local offices, supply, reviews, regulations, or service coverage. Prioritize
one evidenced locale, not automatically France and Germany or mass-translated pages.

### 10. Gap-specific routing

Copy `assets/aeo-gap-action-map.csv` into the existing workspace. Link each row to a
source point, live page/evidence locator, the existing ticket when any, proposed
action, owner, gate, success reading, and stop condition. Use these routes:

- Missing industry fit → one supported case-study/use-case brief.
- Weak existing product answer → precise improvement diff, not another page.
- Absent comparison evidence → fair comparison or requirements brief.
- Early question unanswered → useful definition/problem answer.
- Cited third-party misinformation or omission → editorial resource/pitch draft.
- Genuine community question → observe, owned answer, or approved affiliated draft.
- Locale mismatch → localized evidence and support check before a content brief.
- Unsupported capability or demand → product/research backlog, not a false claim.
- Inaccessible provider/search evidence → unknown; continue other useful checks.

Every decision may be adapt, already covered, defer, or reject, with evidence.
A score ranks review only; it cannot grant authority or prove commercial impact.

### 11. Overall citation result

HubSpot reports a 433% increase in citations on its case-study page. Keep its
reported metric separate from our own matched provider panel. Preserve denominators,
periods, failures, and collection changes. Do not infer that any one tactic caused
that aggregate change. No universal GEO score or guaranteed citation growth.

### 12. Leads and conversion result

HubSpot's page reports 1,850% more qualified AI leads and 3x conversion versus other
sources. These are first-party self-reports, not independently audited results,
our forecast, or a target we can promise. The Q1 2025–Q1 2026 dates in jam's post
were not established by the inspected primary page. Track consented first-party
referrals, lead qualification, deduplication, source definitions, comparable dates,
paid outcomes, and revenue separately. Dark/unknown attribution remains unknown.
Percent growth without absolute counts and stable definitions can mislead.

## Bounded evaluation and full pack

Use `assets/aeo-site-evaluation-brief.md`. Read current product rules and canonical
SEO work first. Reuse dated evidence; collect only the missing, authorized reads.
Do not let an inaccessible data source prevent public page and product-fit review.
Label a proposed panel as not run; do not manufacture a live baseline.

Deliver a source-complete pack: full post, original image or a source locator,
claim audit, twelve-point applicability matrix, page/feature and duplicate map,
prompt panel, provider/source evidence and missing-data register, 3–5 prioritized
opportunities with exact briefs/diffs, measurement definitions, owners and gates,
and an executive decision report. Bind files in a checksum manifest. Private exports,
customer records, credentials, and permissioned data stay out of public PRs.

Recommend the first useful action, why it matters, the evidence, cost/effort and
maintenance, exact approval boundary, and stop/revisit trigger. Prioritization may
use high/medium/low confidence; it must not invent revenue estimates.

The owning agent checks the pack and reports to the owner through its normal
private route. A saved pack or accepted handoff is not channel delivery, and a
report is not implementation or a business outcome. Reconcile uncertain sends
before retrying. Do not create new workers, schedules, or competing source writers.

## Acceptance and stop rules

- All 12 points have an evidenced disposition; none silently disappears.
- Every adopted tactic answers a real buyer problem and maps to a current page or
  a distinct justified brief with a product-truth check.
- Repeated work is linked to existing tickets, not restarted. A HOLD retains its scope.
- Source claims, first-party self-reports, direct observations, and hypotheses stay distinct.
- Capture failures remain unknown. No empty cell becomes a measured zero.
- No external write, spend, account, production, claim change, or schedule is implied.
- Stop the affected action for a rights, truth, safety, authority, or access conflict;
  continue unaffected research and state the exact owner decision if one is needed.
- Measure after approved release on matched panels and like-for-like business periods.
  A before/after result alone is not causal proof. Stop expansion if evidence, support,
  editorial fit, or maintenance capacity fails; do not scale page count for its own sake.
