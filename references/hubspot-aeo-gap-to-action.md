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

## Runpod acquisition evidence extension

Use this extension for a Runpod-style acquisition or tooling-cost claim. It
extends this guide and the current visibility/content/monitoring workflows; do
not start a second panel or tracking system. Read the
[complete Runpod post](source-notes/2026-10-26-jam-runpod-aeo-post.md),
[claim audit](../audit-log/2026-10-26-jam-runpod-aeo.md),
[twelve-point coverage map](../assets/aeo-runpod-source-map.csv) and
[claim registry](../assets/aeo-runpod-source-claims.json). Historical vendor
self-reports are not independent verification or expected gains.

Copy `assets/aeo-acquisition-review.json` into the existing project only when the
review is requested. Its draft_only/not_run state and null measurements are
intentional. Empty or inaccessible evidence is unknown, never a measured zero.
Keep the canonical backlog, owner, approved writers, source custody and holds.

#### R1. Check the body before prescribing more content

For a valuable existing URL, compare normal initial HTML and rendered page body;
retain a short content excerpt or permissioned evidence locator. Check HTTP
status, canonical, robots/noindex and relevant authorized index/provider evidence
separately. Record title-only, partial, full, blocked or unknown observations with
date and method. A body absent from initial HTML may render normally; a browser
render is not proof that a named AI service retrieved or indexed it. Search
snippets and a `site:` result are not proof of complete indexation.

Draft the smallest supported metadata, rendering or formatting repair only after
the actual delivery failure is observed. Do not invent a universal 'AI crawl'
agent, bypass a WAF/access control, or prescribe removing scripts or protections
on the strength of a vendor story. A proposed diff needs existing release
approval and a receipt; only then recheck actual page delivery. More articles
are not a remedy for a broken shared page template.

#### R2. Allocate provider attention from our evidence

Use consented first-party referral/analytics data for the same declared window,
timezone, source taxonomy and unit. Record absolute provider counts, the
qualified-lead/paid-account evidence when available, and unknown/dark referrals.
A missing referrer does not establish no AI influence. Do not apply Runpod's 98%
to this site, confuse sessions with users, or choose a provider because it is
convenient or appears in one screenshot. Keep the denominator inspectable.

Give the evidenced useful provider more of the approved collection budget, while
retaining a bounded matched sample for other relevant providers. State why,
confidence, limitations and a revisit trigger. A proposed allocation is not
approval to buy a vendor, add an account or increase query volume.

#### R3. Expand discovery without moving the goalposts

The existing panel records persona/segment, intent and funnel stage. Add justified
technical use cases there, with question IDs, versions and evidence. Start with
3–10 useful questions, not a 300-prompt quota. Keep a stable matched cohort for
baseline/follow-up comparison and report added/retired prompts separately. Match
provider, surface, locale, account state, sampling and dates; if those change,
label results non-comparable or show the matched subset with sample counts.

Review both useful wins and relevant losses. Do not keep only winning answers,
pick favorable screenshots, silently rewrite questions, or generate a title for
every prompt. Use research to check the gap, existing page overlap, product truth
and buyer value before one normal brief or narrow diff. ChatGPT Deep Research is
an optional named source suggestion, not a verified case requirement, mandatory
tool purchase or substitute for source checking.

#### R4. Connect questions to outcomes without pretending to join users

Join a prompt/version to the proposed page, canonical existing ticket, approved
diff and actual release receipt. A prompt observation is not a visit or a person;
do not fabricate a user-level prompt-to-payment join. In consented first-party
analytics, define visitors/sessions, the exact conversion event, unique new paid
accounts, attribution model/window, deduplication, refunds and revenue separately.
Use private minimal evidence locators; never put customer records or identifiers
in a public PR or send private analytics to an external model.

Report an as-of date and sufficiently mature acquisition cohort for the observed
close cycle; two weeks is this case's claim, not our fixed lag. An immature cohort
is pending, not zero success. Compare compatible periods, units and denominators.
2,100 / ~28,000 = 7.5%, approximately 8%, but those figures do not prove 2,100
unique paid accounts. Do not multiply the reported 40/day by 90 days or invent
paid revenue. Report changed spend, seasonality, releases and other confounders.
A before/after change remains observational, not causal proof.

#### R5. Compare costs on the same basis

Before recommending a stack change, record current authorized cost evidence,
currency, billing periods, prompt/provider/surface coverage, export/retention
requirements and quality/maintenance tradeoffs. Compare subscription, usage and
collection, model/research, and labor/maintenance costs; unknown components remain
unknown. Do not call platform-only savings total operating savings. $3,000 to
$500 is about 83.3% platform-spend reduction in a historical vendor case, not a
current quote, verified ROI or required product purchase. The 6x prompt count is
coverage, not a visibility score. Keep the existing stack when added cost or
maintenance exceeds evidenced value; do not cancel or buy anything from this review.

#### R6. Reuse the existing feedback and approval loop

One evidenced question → delivery/source diagnosis → existing ticket or distinct
brief → exact approved diff → release receipt → matched visibility and separately
defined business review. Preserve raw data, dates, missing evidence and failure
states; reuse existing exports rather than a second collector. Provider/API/data
availability must be live-checked; a repository stub is not a working integration.

No live panel, publication, production change, outreach, external audit reply,
purchase, account, staffing decision, installed-skill update or schedule is implied.
Stop expansion for non-comparable panels, inaccessible bodies, immature cohorts,
missing outcome definitions, unapproved spend, unsupported claims or rights issues.
Keep unaffected read/draft work moving and name the one exact owner decision if
needed. No causal revenue forecast or rank-#1 guarantee belongs in the result.


## Webflow existing-page and matched-experiment extension

For a Webflow-style template/category-page or answer-structure review, read the
[full source](source-notes/2026-10-28-jam-webflow-aeo-post.md),
[fourteen-point map](../assets/aeo-webflow-source-map.csv),
[case audit](../audit-log/2026-10-28-jam-webflow-aeo.md) and
[claim registry](../assets/aeo-webflow-source-claims.json). This extends the same
HubSpot/Runpod feedback loop; it is not a separate workflow or a provider tool.
Use `assets/aeo-page-experiment-review.json` only as a requested draft review.
Keep its draft_only/not_run state and null measurements until actual evidence exists.

#### W1. Prefer a useful existing conversion page over another article

Inventory current template/category/use-case URLs, canonical/robots state, body
availability and the exact real conversion event. Verify demand, audience, product
fit, rights and overlap with the current CMS/sitemap. Reuse R1 page-delivery checks.
Where first-party analytics exists, use comparable page-family sessions, signups,
qualified leads or paid accounts and denominators separately; missing data is
unknown, not a zero or automatic rejection. Choose one small justified pilot.
The case's 1,500 pages are not a target or permission for mass rewriting.

Review the existing above-the-fold copy for a clear buyer question, truthful
branded/product context, the actual intended user and a supported useful outcome.
Those four elements are a copy-review aid, not a keyword formula or a demand to
repeat the brand in every heading. Keep natural readable text, unique page value,
existing working conversion paths and approved claims. Do not replace useful
content with an AI-only introduction, force an answer format, create near-duplicate
team×tool pages, or invent product integrations, local coverage or customer proof.
Draft the exact smallest diff and link the canonical ticket; protected claim/CTA
changes retain their owner gate. No CMS write or release follows from this review.

#### W2. Review cited communities without an auto-comment loop

Reuse the existing source map and `assets/community-reply-review.json`. Retain the
provider, exact prompt/version, cited thread URL, date, observed need, affiliation,
community rules and useful original contribution. A cited thread is not a marketing
invitation. Track response suggestion, sentiment method/denominator, reviewer,
exact-word approval, actual post receipt and post outcome as distinct states.
Draft only where the contribution helps the reader; never automatically post,
coordinate votes, hide affiliation, seed praise or manufacture endorsements.
The case's 100 queries and 98% sentiment are not quotas or proof of lead quality.

#### W3. Freeze the proposed URL experiment before any approved change

Choose **one** treatment per cohort: a useful table of contents, question headings,
or an existing-page audience/outcome copy improvement. Do not mix all three and
attribute the result to one. A table of contents needs real working anchors and
helpful section labels; headings must preserve meaning and accurately introduce
answers. Inspect rendered keyboard/mobile navigation and ordinary Search effects.
These are user-focused hypotheses, not special AI markup, mandatory chunking or
proof that a model retrieved a section.

Record the hypothesis, primary outcome/event/unit, assignment unit (normally URL),
unique, disjoint test/control URLs, matching factors, baseline, post window, timezone,
provider/referrer taxonomy, minimum evidence/precision rule, approval state, exact
diff, release receipt, cost cap, guardrails, analysis plan and stop rules **before**
the change. State whether assignment is randomized or matched observational.
Match page type, relevant traffic/impressions and comparable product intent; avoid
cross-group templates, shared edits, redirects or canonical overlap. Record
contamination, tracking changes, campaigns, seasonality and other releases. Ten
URLs per group and five weeks were this case's design, not a powered universal
sample size. Choose duration/sample needs from real baseline volume; do not keep
checking and stop at the first favorable week. Missing or immature data is pending.

#### W4. Keep raw change, control adjustment and uncertainty separate

Retain test/control pre/post absolute counts, units and source locators. Define
whether aggregation uses URL means, totals, sessions, users, events or rates;
account for repeated observations at URL level. A raw relative change is
(test_post/test_pre−1)×100. If a multiplicative difference-in-differences is the
pre-registered estimator, adjusted relative uplift is
((test_post/test_pre)/(control_post/control_pre)−1)×100. Other estimators must
state their own definition; this formula is not claimed to reproduce Graphite's
analysis. Missing/zero baseline or control denominators make that ratio undefined,
not zero. Percentage-point change for rates is not relative growth.

Keep the raw data, control trend, chosen estimator, effect size, uncertainty or
confidence interval and statistical assumptions reviewable. Do not treat weekly
rows as independent URL experiments or infer adequate power from 10+10 URLs.
Disclose multiple outcomes/comparisons and any changes to the analysis plan.
A vendor p-value without data is source-only; a low p-value is not a guarantee,
a probability that a hypothesis is true, or proof of causality. The source's
119→127 raw AI visits is about 6.7%, not its reported 60% adjusted effect. Its four-week
outcomes and five-week design must stay distinct. Do not reproduce that effect or
p-value without inspectable controls, variance and a valid analysis. Check pre-trends and the estimator's
parallel-trend assumptions; matching alone does not remove confounding.

#### W5. Separate signup scope and decide whether expansion is justified

A free signup, new paid account, qualified lead and revenue are different events.
Record exact event definition, attribution window, deduplication, denominator,
page-family scope, consented evidence and as-of date; never join provider prompt
observations to imaginary users. Preserve the matched question panel separately
from referral/acquisition cohorts. 4%→8% signup share is not necessarily 2x absolute
signups; 24% vs 4% is a reported free-signup CVR comparison, not a 6x paid-sales forecast.

Return draft_only, needs_evidence, stop, no_clear_result or bounded_expand_review
with reasons. Stop affected expansion for low counts, insufficient precision,
non-comparable controls, contamination, tracking changes, ordinary-search or
conversion harm, unsupported claims, rights issues, missing approval or excess cost.
A promising effect is an owner-reviewed next decision, never permission to scale
1,500 pages, buy a vendor, publish, post, add a schedule or change the installed skill.
