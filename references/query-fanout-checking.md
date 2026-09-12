# Query fan-out checking

## Purpose and limits

Query fan-out means the related searches an AI service issues while answering a question. Use this extension with the existing cross-platform citation loop. Do not use it for worker concurrency, ordinary keyword expansion, or a claim that every provider exposes its complete search history.

A social screenshot described collecting fan-outs from Gemini, ChatGPT, Perplexity, and Claude and writing articles for them. It also claimed citations for 5,000+ phrases. That is an anecdotal lead, not independently checked evidence, a benchmark, or a promise. The useful hypothesis is to map observable retrieval needs to useful content. Do not infer private reasoning or undisclosed searches from an answer.

This package supplies a manual capture procedure and an offline ledger validator. It does not include or claim a tested browser/API extractor for any provider. A structurally valid ledger is not proof that its evidence is true; a human or agent must inspect the referenced artifacts.

## 1. Freeze the pilot

Use 3–10 real buyer questions from the existing versioned prompt panel. Keep prompt_id, prompt_version, exact wording, intent, buyer stage and business value. Start with one approved project and its existing workspace. Research does not authorize new paid usage, account connections, scripts from external sources, publication, or schedulers.

List Gemini, ChatGPT, Perplexity and Claude as separate candidate providers. Record unavailable or out-of-scope providers rather than silently omitting them. Add Copilot or Google AI Search only when relevant and approved. Google Search AI features and the Gemini app are different surfaces. Consumer apps and developer APIs are different surfaces too. No result from one proves behavior on another.

For each question/provider run record model/version when exposed, mode, web-search setting, UTC timestamp, locale, language, account/personalization state, and exact surface. Do not collect personal identifiers or secrets. A changed prompt gets a new version. A changed provider mode gets a distinct observation.

## 2. Inspect what the exact surface exposes

Use an existing permitted read-only interface or official response/export. Inspect current behavior and provider documentation rather than assuming a permanent capability. No undocumented bypass, hidden reasoning extraction, intercepted private traffic, CAPTCHA bypass, or invented API fields.

Accepted evidence methods for actual query text:
- `visible_query_ui`: the interface explicitly displays search-query strings for this run;
- `official_api_query_metadata`: a documented API response explicitly contains issued search queries for this run;
- `approved_export`: a permitted export preserves actual issued query strings with a run locator.

For an observed query save the verbatim text, its evidence method, and an evidence locator to the relevant screenshot/export/response field. A source title, result URL, answer heading, URL parameter of unclear meaning, progress message, or model's retrospective explanation is not query evidence. Asking a model what it would search produces hypotheses, not observations.

If only citations are visible, record `citation_only`. If a completed run exposes neither query text nor usable citation evidence, record `not_exposed`. Use `no_search_observed` only with explicit evidence that this run did not call search, not merely an empty source list. Use `blocked` with the actual failure and `untested` for unrun cases. Unknown is not zero; never fabricate rows to fill a provider panel.

## 3. Capture a bounded ledger

Copy `assets/query-fanout-ledger.json` to the private project's `research/<date>_query-fanout.json`. Replace synthetic placeholders before recording real results. Each observation links to one exact versioned question and one provider/surface run. Preserve original query strings and citation URLs separately. Keep query-to-citation links unknown unless the source explicitly provides them; adjacent display is not proof of a causal link.

Each completed run needs a dated evidence locator. An `observed` run needs at least one actual query with its own locator and method. Non-observed states must have an empty queries array; this encodes missing observations, not a count of hidden searches. Generated ideas belong only in the separate hypotheses list with `kind: inferred`, their rationale, and validation status. Never merge them into observed query counts.

Run `python3 scripts/query_fanout_check.py <ledger.json>`. Fix rejected records before planning from them. Keep source artifacts in the private project; publish only the empty template and synthetic tests. The validator makes no network calls, spends no credits, writes no site files, and cannot certify source authenticity.

## 4. Map evidence to buyer needs and pages

Group observed queries by genuine intent while retaining observation/query IDs and verbatim strings. Deduplicate planning ideas, not source evidence. Build a coverage table with: intent cluster; observation IDs; observed queries or explicitly inferred candidate; existing URL/section; cited URLs; source/page role; gap; business relevance; first-party proof required; independent demand evidence; decision (`keep`, `update`, `new_brief`, `retest`, `reject`); draft brief locator.

Inspect the existing page and site architecture first. A useful section update is preferable to another page for the same intent. If query data is unavailable, continue normal buyer-question/citation research but label that basis. Never pretend a citation-derived content gap is an observed fan-out gap.

Use a clear priority order: real buyer value, repeatable observed need, existing-page coverage gap, available truthful evidence, and effort. Query recurrence is not search volume or market demand. Validate demand with customer/support research, ordinary search evidence, or relevant business data. Reject a new page whose only justification is a synthetic query or a target page count.

Route justified briefs to `workflows/content-production.md`. Include direct answers, factual sources, original evidence, useful comparisons and honest limitations where applicable. Preserve existing article QA, product-truth and publication gates. No thin page per fan-out phrase, keyword stuffing, fabricated evidence, scaled doorway pages, citation guarantees or automatic publishing.

## 5. Retest comparable runs

Use the same question/version, provider, surface, mode, locale and account state after a suitable discovery window, usually the existing 4–8 week review. Record changes and limitations if exact matching is impossible. A review date is not authorization to add a timer.

Report exposed query overlap/change and observation coverage per provider, citing the sample size and missing/blocked cases. Keep citation/mention changes separate from search impressions, referrals, conversions and revenue. No universal fan-out/GEO score, hidden-query completeness claim, or causal ranking claim. Temporal change after editing content is not proof the edit caused citation.

## Done condition

The provider coverage matrix includes unknown and blocked cases; exact questions are versioned; actual query evidence is separated from citations and hypotheses; the offline validator passes; proposed content decisions map to checked pages and independent buyer need; and publication, spend and scheduling remain approval-gated. Distinguish `procedure_ready`, `fixture_tested`, and `live_provider_verified` in reports. A fixture test never earns the last status.
