---
title: Cross-Platform Buyer-Question Citation Loop
area: maintenance
operational_addition: true
source_scope: Dated answer-engine observations plus ordinary SEO and first-party business evidence; no universal AI-ranking formula
field_inputs:
  - https://x.com/i/article/2083164906480656384
  - https://x.com/mal_shaik/status/2089120487481982981
  - https://x.com/charles_seo/status/2113655739772535200
---

# Cross-Platform Buyer-Question Citation Loop

Use this when a brand wants to understand or improve how a named answer engine—such as Microsoft Copilot, ChatGPT, Perplexity, or Claude—mentions the brand and cites sources for high-value buyer questions. It turns mutable answer-engine observations into a repeatable evidence loop. There is no public universal GEO score or formula for this work. It is not a promise that a content template, backlink, or query position will cause citation.

## 1. Freeze a small buyer-question set

Start with about 10 questions asked close to a buying decision, not thousands of generic keywords. Source them from sales calls, support conversations, Search Console, pricing objections, lost deals, competitor comparisons, and validated customer research.

For every question record:

- a stable question ID and the exact wording;
- buyer stage and business value;
- named engine and surface;
- country/locale and language;
- account/personalization state when it can affect the result;
- first-tested date and retest cadence.

Do not silently rewrite questions between runs. Add a new version when wording changes so the history remains comparable.

For buyer-question runs, also load `references/query-fanout-checking.md`. Save exposed query strings, citation-only evidence, and inferred ideas separately in `assets/query-fanout-ledger.json` copied to the private project. Validate with `python3 scripts/query_fanout_check.py <ledger.json>`. Unknown query visibility is not zero searches. No hidden-query extractor or cross-provider equivalence is implied.

## 2. Capture a platform-specific baseline

Run the fixed questions modestly and in accordance with the platform's terms. For each observation save:

- retrieval date and engine/surface;
- whether the brand was mentioned;
- exact cited/source URLs, when exposed;
- cited domain and source type (`owned`, `editorial/listicle`, `community`, `directory`, `other`);
- the visible answer excerpt needed to interpret the citation;
- the page or product role (`problem`, `use_case`, `comparison`, `pricing`, `trust`, `case_study`, `implementation`);
- an evidence locator such as an export or screenshot reference, without treating the screenshot as traffic proof.

Keep each provider in its own dataset. Microsoft Copilot observations are not Google Search Console Generative AI impressions, and neither dataset proves coverage on another platform. Keep ordinary Search clicks, impressions, positions, sessions, and conversions in their own measurement lane too.

Suggested artifact: `monitoring/<date>_ai-citation-observations.json`.

```json
{
  "captured_at": "YYYY-MM-DD",
  "platform": "microsoft_copilot",
  "surface": "...",
  "locale": "en-GB",
  "questions": [
    {
      "question_id": "q01",
      "exact_text": "...",
      "buyer_stage": "comparison",
      "brand_mentioned": false,
      "citations": [
        {"url": "https://example.com/page", "domain": "example.com", "source_type": "editorial/listicle"}
      ],
      "evidence": "..."
    }
  ],
  "limitations": ["mutable_answers", "no_impression_or_click_count", "no_causality"]
}
```

### Optional buyer-recommendation mini-panel

Use this only when the question is **who the answer recommends**, not merely whether a brand is mentioned or cited. Discovery: [Charles Floate, 23 October 2026](https://x.com/charles_seo/status/2113655739772535200). His three-runs-on-three-surfaces idea is a small diagnostic, not an industry benchmark, a complete ten-question panel or proof of a default entity.

Copy `assets/buyer-recommendation-panel.json` to the private project's `monitoring/` directory. The shipped file is an **unconfigured, not-run template**: no answers, zeroes, approvals or business results are supplied. Fill the canonical brand entity and one versioned, evidence-backed buyer question, locale and language. Avoid naming your brand in an otherwise unbranded question. The initial nine planned slots are three each for ChatGPT, the Gemini app and Google AI Mode. Gemini is not AI Mode, and AI Mode is not an AI Overview. If a surface is unavailable or requires login, record that fact; never silently substitute a provider, API or model to complete nine cells. Claude and Perplexity need separately scoped slots; this panel says nothing about them.

Before collection, freeze the planned slots and context policy. Use a fresh conversation for each run; do not let prior answers, memory, leading follow-ups or brand hints contaminate a supposedly unprimed run. Record actual model (or `not_exposed`), surface, account/personalization state, locale, language, timezone-aware capture time, exact prompt/version and durable evidence for each slot. Logged out and Incognito are different observations. Incognito does not hide location or make runs independent, anonymous or fully unpersonalized. Record unavoidable context limits. Do not evade access controls or buy calls to fill missing slots.

Manually review the full answer against the real entity and classify **the target brand**:

| Label | Meaning |
|---|---|
| `primary` | An explicit, sole first choice for the scoped buyer job, supported by the answer's wording. Being first in an unordered list is insufficient. |
| `tied_primary` | Explicitly shares the first choice; not a sole pick. |
| `option` | A recommended option, but no explicit sole first choice. |
| `mention_only` | Named without being recommended, including rejected or negative mentions. |
| `absent` | A complete, reviewed answer does not name the target brand. |
| `unclear` | Ambiguous, incomplete, unreviewed, failed or inaccessible evidence. |

Store citation presence separately as `cited`: whether the answer cites an owned URL for the target brand. A citation alone must not upgrade a label. Retain the raw answer and, for every positive/non-absent classification, a verbatim `classification_quote` that occurs in that answer. This supports review, but does not mechanically prove that the quote endorses the brand. Record ties, conditions, negation and the actual winner in the private review notes. A reviewer must resolve these meanings; do not ask this arithmetic tool to infer them.

Each observation uses this shape (illustrative only, not a real measurement):

```json
{
  "slot_id": "chatgpt-1", "provider": "chatgpt", "surface": "web_search",
  "model": "not_exposed", "account_state": "logged_out; fresh_chat; memory_not_available",
  "locale": "en-GB", "language": "en", "captured_at": "2026-10-25T10:00:00+00:00",
  "prompt_text": "EXACT FROZEN PROMPT", "prompt_version": 1,
  "status": "ok", "review_state": "verified", "recommendation": "option",
  "raw_answer": "Example is one option for this job.",
  "classification_quote": "Example is one option for this job.",
  "cited": false, "evidence_locator": "answers/chatgpt-1.txt"
}
```

For `partial | error | refusal | blocked | not_available`, set `recommendation: unclear` and add `reason`. An absent slot is **not run**, not a zero. Keep attempts/retries in the private collection log; select one observation per preplanned slot without cherry-picking. Do not replace a non-favourable answer with a retry. A different prompt, locale or language needs a new panel/version. Context changes remain separate result groups.

Summarize saved, manually labelled evidence offline:

```bash
python3 scripts/recommendation_panel.py monitoring/buyer-panel.json --out monitoring/buyer-panel-summary.json
```

The script makes no provider requests, parses no answer semantics, writes no website and creates no schedule. It rejects duplicate/unknown slots, prompt drift, malformed labels, timezone-free timestamps and malformed evidence fields. It preserves planned/observed/not-run coverage and separates provider, surface, model, account state, locale and language. Only complete `ok`, manually `verified`, non-`unclear` answers enter the denominator. It reports **strict primary picks / classifiable answers**, with ties/options/mentions/absences and citations separate. Zero classifiable answers gives `null`, never 0%. Report the denominator and exclusions beside every rate. Do not pool the three providers into a single 0/9 or 9/9 visibility score. With this sample, zero observed picks does not prove universal absence and nine picks do not establish market dominance. Repeated outputs can be correlated; no population estimate or causal inference is justified.

Keep `geo_metrics.py` unchanged for mention, position and citation metrics. Its first mention position and positive sentiment are not recommendation labels. Link the two artifacts by immutable run/slot IDs in the private workspace; do not silently reinterpret historic observations.

### Source claims and the buyer-page conversion loop

The source's $200k/month take-home claim, 8x ChatGPT lead-generation conversion claim and approximately 57% international AI Overview prevalence are **unverified source claims**, not targets or forecasts. The attached custom income dashboard shows approximately $199,392 USD equivalent for 24 September–23 October 2026, including community, PressWhizz pay, consulting, affiliate, training and partner income. It does not expose underlying transactions, costs, taxes, acquisition cohorts, conversion denominators or a causal AI-SEO contribution. Do not call it audited profit, client results, a conversion study, or proof that all income came from recommendations. No linked dataset supports 8x or 57%; no universal multiplier or prevalence rate is established.

Retain the useful sequence as a **bounded hypothesis**, using the existing workflows:

1. Validate one buyer job/question and inspect its live search/answer intent. Keep an existing-page and cannibalization check; update a suitable page before proposing another URL.
2. Save the provider baseline and the actual cited/recommended competitors. A recommendation gap is not automatically a content or access fault.
3. Route a justified page brief to `workflows/content-production.md`: truthful fit/limitations, offer, proof, price/terms where relevant, one clear next action and accessible mobile controls. Do not claim to be best or default without support.
4. Expand the question only with real customer/search evidence or exposed provider queries. Use `references/query-fanout-checking.md`; distinguish inferred ideas from observed searches. Do not create thin pages for every generated variant.
5. Separate **CRO (conversion-rate optimization)** from search eligibility. Identify one page/offer/friction hypothesis and a predeclared conversion event, denominator, cohort, date range, timezone, attribution scope and decision rule. Obtain applicable approval before any page or tracking change. A nine-answer panel is not a conversion sample.
6. Compare actual first-party cohorts only: report eligible sessions/users and completed, deduplicated qualified leads/signups using like-for-like definitions, windows and conversion lag. Exclude bots/internal tests and distinguish qualified leads from submitted forms, sales and net profit. If the comparator rate is zero or the data is absent, the ratio is undefined, not 8x. Missing referrers and attribution limits remain unknown; a referrer does not prove a particular prompt, citation or recommendation.
7. Retest identical question versions and observe search, referrals, leads and revenue in separate lanes. Choose a review window with the owner; do not activate a cadence. Heatmaps/session replay are optional page-behaviour evidence, not SEO ranking or causality proof. Use existing lawful, consented, masked evidence only; no installation or collection of credentials, sensitive fields or personal recordings follows from this source. A before/after change alone proves no causal lift.

As checked 25 October 2026, [Google's AI-features guide](https://developers.google.com/search/docs/appearance/ai-features) says ordinary Search foundations apply, with no additional technical requirements, and that AI Overviews do not always trigger. This does not validate 57% international prevalence. Check the live reporting surface before making attribution claims. [GA4 channel documentation](https://support.google.com/analytics/answer/9756891?hl=en) now describes **AI Assistant** separately from Organic Search, explicitly excluding Google AI Overviews and AI Mode from that assistant channel. Record the report's actual date, available channel/source dimensions and session/user/event scope; do not impose a historic referral classification or mix scopes. The [Chrome Incognito documentation](https://support.google.com/chrome/answer/95464?hl=en) explains its local privacy limits. Neither these sources nor the panel establish conversion uplift.

This is a research/briefing branch of the existing citation loop, not a new publishing system. Public submissions, outreach, new accounts, paid calls, analytics/heatmap installation, crawler/security changes and live edits still need their own applicable authority. Copying the template grants none.

## 3. Diagnose the gap before prescribing work

Classify each useful gap:

1. **Eligibility/access gap** — the relevant page is not indexable, crawlable, renderable, or available to the scoped provider under the owner's policy.
2. **Owned-page gap** — no useful page answers the buyer's question with distinct intent and evidence.
3. **Page-quality gap** — a page exists but lacks a direct, supportable answer, common comparison criteria, current facts, primary sources, first-hand proof, or honest limitations.
4. **Authority/source gap** — the engine repeatedly cites independent comparisons, listicles, communities, or directories where qualified competitors appear and the brand does not.
5. **Measurement-only gap** — evidence is too thin or volatile to justify changes; preserve the baseline and retest.

Use ordinary Search evidence too. A current, intent-matched page in GSC positions 4–20 may be a narrower improvement candidate, but its Search position does not prove or guarantee answer-engine citation.

### 3A. Map corroboration surfaces without turning them into quotas

When the baseline shows that a provider cites several source classes, copy `assets/ai-citation-source-coverage.csv` to `research/<date>_ai-citation-source-coverage.csv`. Use one row per observed or qualified source, not one row per desired placement.

Useful source classes include:

- `owned_comparison`, `owned_use_case`, `owned_pricing`, and other distinct buyer-help pages;
- independent editorial comparisons, directories, review sites, and partner resources;
- authentic community discussions that already exist because people used the product;
- public repositories, documentation, datasets, or tools that provide verifiable product proof; and
- other sources actually cited on the scoped provider/surface.

For every row record the exact question, provider/surface, date, URL, source role, whether the brand is present, whether the URL was actually cited, evidence grade, proof locator, limitations, and the proposed action. Distinguish **observed cited sources** from **candidate sources**. A candidate directory, Reddit thread, repository, or comparison page is not citation evidence until the scoped observation shows it.

Source breadth is a coverage hypothesis, not a citation formula. Do not set quotas for comparison pages, directories, repository stars, reviews, or community mentions. Do not create thin comparison permutations, submit to irrelevant directories, manufacture Reddit threads or votes, solicit fake reviews, or use open-source popularity as a substitute for product truth.

#### Dated Cal.com field example

A 2026-08-16 creator post attributed Cal.com's alleged answer-engine visibility to `47` comparison posts, `23` niche-directory listings, more than `45,000` GitHub stars, and `200+` Reddit mentions, then called Cal.com the “#1 ChatGPT recommended scheduling tool.” Treat this as a source-coverage hypothesis, not a verified causal explanation.

A bounded check on 2026-08-17 found:

- the public GitHub repository reported 47,731 stars, supporting only the narrow “45,000+” count;
- the English sitemap exposed 35 blog URLs matching a broad comparison/alternative URL pattern, which confirms a material owned comparison footprint but does not validate the claimed total of 47;
- the `23` directory placements and `200+` Reddit mentions were not reproduced from a complete, dated inventory; and
- the attached “Visibility Rank #1” screenshot lacked the provider, prompt set, locale, account state, methodology, and retrieval date needed to prove a universal ChatGPT rank.

Official OpenAI crawler documentation supports a narrower access check: `OAI-SearchBot` controls eligibility for ChatGPT search results, separately from `GPTBot` training controls. It does not publish a rule that a fixed mix of comparisons, directories, stars, or Reddit mentions produces recommendation. Google likewise says its AI Search features use ordinary Search eligibility and people-first SEO foundations, with no additional technical requirements. Keep those provider contracts separate.

## 4. Build pages for buyers, not an AI quota

When a justified page is missing, route it to `workflows/content-production.md`. Useful page roles may include use-case, comparison, alternatives, pricing, implementation, trust/case study, or a well-sourced statistics/original-research resource.

For applicable pages require:

- a direct answer near the top that remains accurate when quoted alone;
- clear “best for” or fit guidance rather than declaring one winner for everyone;
- comparisons using the same disclosed criteria and columns;
- current prices/features with source and checked date where relevant;
- original/primary sources for material claims;
- at least one honest limitation or tradeoff per option;
- accurate authorship, methodology, and material update date;
- first-party examples, screenshots, data, or experience when available.

Do not add synthetic “AI chunks,” fake FAQs, unsupported statistics, or repetitive answer blocks. Clear sections help people first; they are not a provider-specific ranking requirement.

A main guide plus five to seven supporting pages can be a useful cluster only when each page has distinct demand, intent, evidence, and buyer value. The numbers are a planning range, not a quota.

## 5. Strengthen authentic corroboration

Map the domains cited for the fixed questions. Prioritize independent pages that name several relevant competitors, cover a genuine missing use case, and are editorially appropriate.

Route outreach to `workflows/authority-and-links.md`. Draft a factual pitch that explains the omitted use case and offers checked facts, screenshots, criteria, and limitations. Never auto-send, buy manipulative placement, fabricate community discussion, hide sponsorship, or manufacture citations.

Partner links belong only when they help the reader and satisfy the authority workflow's quality, disclosure, and approval gates. Reciprocal-link volume is not a citation strategy.

## 6. Retest without inventing causality

After material changes have had time to be discovered, rerun the same question versions on the same platform/surface and locale. Monthly or a 4–8 week review window is usually more meaningful than daily checking; choose the cadence with the user.

Compare:

- brand mention presence;
- owned versus third-party cited domains;
- newly cited or dropped URLs;
- page-role coverage;
- ordinary Search visibility;
- measurable referrals/sessions;
- leads, assisted conversions, transactions, and revenue.

Keep those measures separate. A changed answer after publishing or outreach is temporal association, not proof that one action caused the change. Do not convert observation counts into estimated impressions, clicks, CTR, conversions, or revenue without an actual data source.

## Source-quality note

A July 2026 vendor-authored field article described a 90-day program and claimed 14.7K Microsoft Copilot citations. The operational ideas above—fixed buyer questions, useful comparison/use-case pages, coherent internal linking, authentic third-party source work, and repeat testing—are used as hypotheses and workflow inputs. The 14.7K claim is not independently verified here and must not be repeated as a benchmark, expected result, or causal proof.

A separate August 2026 creator post described Cal.com's comparison pages, directory listings, GitHub stars, and Reddit mentions as an engineered-visibility recipe. That source-mix explanation is also a hypothesis, not an independently established benchmark, expected result, ranking formula, or causal proof.

## Done when

The exact buyer-question set is versioned; each platform has a separate dated baseline; cited URLs and source types are recorded; any source-coverage map separates observed citations from candidates; every recommended page or authority action maps to a real observed gap; content and outreach remain approval-gated; the retest cadence is chosen; and the report clearly separates mentions/citations from traffic, conversions, and causality.
