---
title: Content Production
goal: Take a validated keyword (or sitemap entry) and produce an intent-matched brief, plus an optional review-ready draft and QA report.
playbooks:
  - references/playbooks/content/content-fundamentals.md
  - references/playbooks/content/content-types-overview.md
  - references/playbooks/content/cross-platform-commercial-intent-distribution.md
  - references/playbooks/content/programmatic-seo.md
  - references/playbooks/content/programmatic-pattern-library.md
  - references/playbooks/content/free-tools-strategy.md
  - references/playbooks/content/content-pages.md
  - references/playbooks/content/landing-pages.md
  - references/playbooks/content/articles.md
  - references/playbooks/content/content-rings.md
  - references/playbooks/content/on-page-optimization.md
  - references/playbooks/content/image-search-optimization.md
  - references/playbooks/content/content-what-not-to-do.md
  - references/playbooks/content/agent-article-production-qa.md
  - references/playbooks/research/match-and-exceed.md
  - references/playbooks/research/search-intent.md
  - references/playbooks/maintenance/seo-operational-checklist.md
scripts:
  - scripts/workspace.py
  - scripts/search_course.py
  - scripts/serp_capture.py
  - scripts/ahrefs_client.py
  - scripts/report.py
integrations: [serp, ahrefs]
outputs:
  - briefs/<date>_<keyword-slug>-brief.json   # one content brief per page
  - research/<date>_content-angles.json        # if personas summoned
  - research/<date>_<keyword-slug>-distribution-map.json # if a cross-platform search-surface test is justified
  - research/<date>_<keyword-slug>-source-packet.json  # if drafting an article
  - drafts/<date>_<keyword-slug>.md                    # if drafting an article
  - audits/<date>_<keyword-slug>-content-qa.json       # if drafting an article
---

# Content Production

**When to run this.** A keyword (or a row from a `research/<date>_sitemap-plan.json`) is validated and you need to decide *what kind of page* to build and produce a brief for it. When the user also asks for an article draft, continue through the evidence-grounded production and QA branch in step 8. Runs after `research-and-ideation.md`. **This workflow never publishes.** Building/publishing is an irreversible action that requires explicit user confirmation outside this workflow.

**Prerequisites.**
- **Workspace** resolved (`python3 scripts/workspace.py status --path <DIR>`; ASK before creating if absent).
- **Inputs:** the target keyword(s) and intent from the keyword map / sitemap plan (or an explicit user-selected topic); the target country/locale; the operator's build strength (developer vs writer); the product/offer to upsell; and, when product claims appear, a product-truth contract or a conservative claim boundary.
- **Data sources:** live SERP (`serp_capture.py`, browser fallback in `references/integrations/serp.md`) and Ahrefs for cluster sizing (`ahrefs_client.py`).

**Steps.**

1. **Re-read the live SERP for the exact keyword.** Load `references/playbooks/content/content-fundamentals.md` and `references/playbooks/research/match-and-exceed.md`. Run `scripts/serp_capture.py` on the keyword (target country). Classify the format Google rewards in the top 3 and confirm intent with `references/playbooks/research/search-intent.md`. The SERP is the source of truth — `"X generator"` and `"best X generator"` resolve to opposite formats, so test the exact phrasing.

2. **Select the content type.** Load `references/playbooks/content/content-types-overview.md` and map intent → format:
   - Transactional → **landing page** (`landing-pages.md`).
   - Scalable informational, hundreds of long-tail variants from data → **programmatic SEO** (`programmatic-seo.md`).
   - Action/tool keyword (generator, maker, calculator) → **free tool** (`free-tools-strategy.md`).
   - Informational-but-structured, with a modifier (vs/review/niche/examples/integration) → **content page** (`content-pages.md`, pick the sub-pattern by modifier).
   - Pure prose informational, and you'll invest in real writing → **article** (`articles.md`).
   - Off-site backlink/traffic engine → **content ring** (`content-rings.md`; the link-building side lives in `authority-and-links.md`).
   Default to the operator's strengths; don't force a format the SERP doesn't reward.

   **SaaS modifier branch.** For alternative, comparison, integration, constraint, pricing, use-case, problem, feature, or audience/company-size queries, apply the SaaS demand-page matrix in `content-types-overview.md`. The supplied practitioner ordering is candidate-generation input only. Do not inherit its intent, competition, indexing, or traffic-timing claims. Reject or consolidate a page when product truth is weak, the user job overlaps an existing URL, the live SERP does not support the format, or the only change is a token in the heading.

   **Optional cross-platform commercial-intent branch.** When the user wants a distribution test—or the live search journey repeatedly exposes a native video, discussion, or editorial surface for a valuable query—load `references/playbooks/content/cross-platform-commercial-intent-distribution.md`. Capture dated evidence, keep the owned page as the evidence hub, and select one primary plus at most two supporting surfaces. Save `research/<date>_<keyword-slug>-distribution-map.json`. This is not permission to mass-copy content, seed affiliate links, evade moderation, or publish: every native asset must add distinct value and all external writes remain approval-gated.

3. **(Optional) Summon ICP personas for content angles.** When you need fresh angles, FAQ questions, or objections to address on the page, dispatch persona subagents per `agents/icp-persona.md`: pick 3–6 distinct personas, launch **all in parallel, `model="opus"`**, then merge with `agents/synthesizer.md`. Use their literal queries as H2s/FAQ entries and their objections as copy to defeat. Save to `research/<date>_content-angles.json`.

4. **Load the format-specific method and draft the page plan.** Open the playbook for the chosen type and follow its method:
   - **Programmatic SEO:** load `programmatic-pattern-library.md`; choose one of the 12 observed-demand patterns, score the opportunity, build the unique-data ledger, lock hub/leaf/canonical rules, and launch a bounded cohort. Layer dimensions only when combined demand, distinct intent, page-level data, deduplication, and a hard page cap are all proven.
   - **Free tool:** pick the angle (free counterpart / adjacent audience / link magnet); spec a tool that's *easier* than the top 3; plan killer title + meta variants; add How-it-works + FAQ so it isn't thin; plan the upsell.
   - **Content page:** choose the sub-pattern (alternative/comparison / success-story-review / niche hub / examples-how-to / integration); apply the SaaS family gate when relevant; plan sections, screenshots or demonstrations, current pricing/product evidence, limitations, and proof; load justified niche/long-tail keywords here, off the homepage.
   - **Landing page:** one keyword per page, inform + link straight to checkout.
   - **Article:** confirm you'll invest in genuine human writing; if not, pick a different format.

   If the brief is being routed from `geo-audit.md` or `category-citation-loop.md`, also load `references/playbooks/maintenance/cross-platform-ai-citation-loop.md`. Carry forward the exact buyer-question version, scoped provider, observed source/page-role gap (`problem`, `use_case`, `comparison`, `pricing`, `trust`, `case_study`, `implementation`), and required first-party evidence. Build pages for buyers, not an AI quota: do not mint one page per synthetic fan-out or create unsupported comparison claims just to chase citations.

   Apply the relevant content checks from `references/playbooks/maintenance/seo-operational-checklist.md`: titles are intent-first (50–60 characters is guidance, not a hard pass/fail), authorship/E-E-A-T signals must be real, schema must match visible content, `dateModified` changes only after material edits, and FAQ/PAA sections belong on the most appropriate page unless a standalone page has distinct demand and enough value.

5. **Apply on-page optimization to the brief.** Load `references/playbooks/content/on-page-optimization.md`. Specify: meta title (main keyword, intent-matched, natural) and description (synonyms/variants); internal links to/from related pages; a page-speed plan (prefer static generation); and canonicals for any parameterized/duplicate URLs. When the live SERP has meaningful visual intent or the page relies on original/product/diagram imagery, also load `references/playbooks/content/image-search-optimization.md` and add an evidence-backed image plan: image purpose, landing-page context, stable descriptive filename, accessible alt behavior, responsive delivery/performance, discovery route, and only the structured metadata that fits the real page and rights use case.

6. **Run the what-not-to-do guardrail.** Load `references/playbooks/content/content-what-not-to-do.md` as a pre-brief checklist: no AI content spam, respect crawl budget (batch large publishes), no keyword stuffing, no duplicate/cannibalizing pages, no thin content. Flag any risk in the brief.

7. **Emit the content brief.** Assemble a brief object: `{keyword, intent, content_type, sub_pattern, serp_summary, outline (H1/H2s), meta_title, meta_description, target_keywords[], internal_links[], data_sources (pSEO), upsell/offer, on_page_checklist, guardrail_notes, persona_angles?, saas_page_family?, eligibility_evidence?, product_truth_evidence?, overlap_canonical_decision?, claim_checked_dates?, reject_consolidate_reason?}`. Write it with `python3 scripts/report.py note --workspace <DIR> --subdir briefs --name <keyword-slug>-brief --data <brief.json>` → `briefs/<date>_<keyword-slug>-brief.json`. Repeat steps 1–7 per page when briefing a whole sitemap.

8. **(Article drafts only) Produce and QA the draft.** Load `references/playbooks/content/agent-article-production-qa.md`. Do not run this branch merely because a brief exists; the user must have asked for an article draft.
   1. Resolve the approved backlog/topic row and record the product-truth contract: approved facts and evidence, required product URLs, approved CTA language, comparison boundaries, forbidden claims, and open reviewer questions. If no contract exists, keep product claims conservative and flag them.
   2. Build `research/<date>_<keyword-slug>-source-packet.json`, mapping every material claim or outline section to a source URL, extracted fact/quote, publication date where relevant, reliability note, freshness requirement, and intended section. Research by claim, not by an arbitrary page count.
   3. Draft from the brief and source packet. Preserve the live-SERP format, answer the core query early, cite material claims where appropriate, and add original value rather than padding to a universal word count.
   4. Run a separate anti-slop rewrite that removes generic introductions, repeated conclusions, canned transitions, filler, fake authority, unsupported certainty, choppy fragments, and duplicated facts while preserving evidence, links, code, and product truth.
   5. Run mechanical lint for heading hierarchy, keyword/title/meta placement, link validity, required product links, citations, forbidden phrases/claims, TODOs/placeholders, alt text, and schema consistency.
   6. Run weighted semantic QA: intent/coverage 25, evidence/E-E-A-T 25, human value 15, writing quality 15, product truth 10, on-page/internal linking 10. Unsupported material claims, fabricated quotes/sources/testimonials, false product claims, intent/format mismatch, cannibalization, broken required links, or missing critical evidence are hard fails regardless of score.
   7. Revise against named defects no more than twice. Pass only at 85/100 or higher with no hard fails. Otherwise stop and emit the remaining defects; never loop indefinitely or publish.
   8. Write the review draft to `drafts/<date>_<keyword-slug>.md` and the inspectable QA result to `audits/<date>_<keyword-slug>-content-qa.json` with category scores, hard-fail results, revision count, and unresolved defects.

**Decision points.**
- **Format selection** is driven by the live SERP + the intent→format map, NOT by preference. If the SERP shows articles, do not brief a landing page.
- **Programmatic vs hand-built:** hundreds of scalable long-tail variants → programmatic; only 3–5 pages of opportunity → write/build them individually.
- **SaaS family page?** Build only when the exact query has evidence, the SERP format fits, the product claim is true, and the page has a distinct job and value. Otherwise reject or consolidate it. Never use the field article's order or six-month claim as a forecast.
- **Article go/no-go:** only if genuine quality writing is committed; otherwise pick a developer-friendly format.
- **Citation-loop brief?** Only create it when a fixed buyer question, observed provider gap, and distinct page value justify the page.
- **Cross-platform distribution map?** Only when live surface evidence and a measurable buyer journey justify it; never from a platform quota or a creator revenue anecdote.
- **Summon personas?** Only when angles/FAQ/objections are thin.
- **Build/publish?** Out of scope here. Producing the brief is the deliverable; any build or publish step requires explicit user confirmation.
- **Draft requested?** Briefing alone stops at step 7. Article drafting uses step 8 and still stops at a review-ready artifact.
- **QA pass?** A weighted score below 85, any hard fail, or more than two failed automated revisions stops the run with a defect report.

**Outputs.**
- `briefs/<date>_<keyword-slug>-brief.json` — one intent-matched, on-page-optimized brief per page, ready to hand to a builder.
- `research/<date>_content-angles.json` — synthesized persona angles/FAQs (if run).
- `research/<date>_<keyword-slug>-distribution-map.json` — dated search-surface evidence, selected native roles, journey, disclosure, and separated metrics (if justified).
- `research/<date>_<keyword-slug>-source-packet.json` — claim-to-source evidence packet (if an article draft is requested).
- `drafts/<date>_<keyword-slug>.md` — evidence-grounded review draft (if requested).
- `audits/<date>_<keyword-slug>-content-qa.json` — weighted QA, hard-fail results, revisions, and remaining defects (if requested).

**Done when.** Every targeted keyword has a brief whose format matches the live SERP, includes an outline + metadata + internal-link + upsell plan, and passes the what-not-to-do checklist. Each SaaS-family candidate also records eligibility and product-truth evidence, overlap/canonical disposition, checked dates for mutable claims, and a build/reject/consolidate decision; no doorway-like token variant survives. Citation-loop-driven briefs also preserve the triggering question version, provider scope, and evidence plan. Any cross-platform distribution branch also has dated surface evidence, no more than three selected surfaces, distinct native value, a disclosure plan, an owned evidence hub, and separate search/native/referral/conversion/revenue metrics. If an article draft was requested, the source packet, draft, and QA report are inspectable; the draft scores at least 85/100; no hard fail remains; and no more than two automated revisions were used. Hand review-ready artifacts to the user/builder for the confirmation-gated build; route "ranks but needs links" pages to `authority-and-links.md` and add new pages to `monitoring.md`.
