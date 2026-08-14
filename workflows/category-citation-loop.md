---
title: Category Citation Loop
goal: Choose a truthful category phrase, build a useful owned evidence cluster, and monitor category framing across search and answer engines.
playbooks:
  - references/playbooks/foundations/seo-and-ai-future.md
  - references/playbooks/content/content-fundamentals.md
  - references/playbooks/content/on-page-optimization.md
  - references/playbooks/content/agent-article-production-qa.md
  - references/playbooks/research/search-intent.md
  - references/playbooks/maintenance/cross-platform-ai-citation-loop.md
outputs:
  - research/<date>_category-citation-loop.md
---

# Category Citation Loop

Use when the user wants to own a defensible category phrase and become easier to discover, understand, or cite across search and answer engines. The operating idea is: make the product memorable in distribution, then make the owned evidence genuinely useful enough to cite.

## Procedure

1. **Choose scope from project evidence, then capture a platform-specific baseline.** Load `cross-platform-ai-citation-loop.md` and run `geo-audit.md` for a bounded prompt set. Select one primary provider and at most two supporting providers from the project's audience, referrals, optional self-report, buyer-question coverage, product fit, conversion value, cost, and policy risk—not another company's channel ranking. Freeze exact buyer-question versions per provider/surface, then record dates, platform/account/location where relevant, mentioned brands, cited domains, source types, retrieval observability, persistence fields, and owned-page citations. Keep Google AI impression data, provider observations, self-reported discovery, referrals, and conversions separate, and do not merge them into one universal score.
2. **Choose one primary phrase.** Score candidates on buyer intent, specificity, product-truth fit, live SERP/answer evidence, conversion relevance, and the ability to publish genuinely useful material. Add 2–4 supporting phrases and a do-not-use list for overbroad or untrue claims.
3. **Build an owned evidence cluster, not a quota.** Consider category definition, use-case, comparison, alternatives, pricing, implementation, trust/case-study, and a useful tool/resource. Match page roles to the observed buyer-question gaps. Create only pages with distinct demand, intent, evidence, and non-duplicative value.
4. **Make comparison claims defensible.** Include real alternatives and tradeoffs, explain evaluation criteria, state who each option is for, cite material claims, and preserve limitations. Never rank the product first for every use case by construction.
5. **Strengthen the positioning spine.** Use the truthful category phrase consistently across the homepage/product copy, relevant page titles/descriptions, schema descriptions, internal anchors, and launch/demo assets. Consistency is an entity/positioning aid, not permission to keyword-stuff.
6. **Create one memorable proof-led distribution asset.** Demonstrate the actual job-to-be-done and repeat the category phrase naturally. Any social publishing or launch is a separate approval-gated action.
7. **Monitor and compound.** Re-run the same question versions and ordinary GSC/analytics evidence over 4–8 weeks. Save dated provider observations into `monitoring/<date>_ai-citation-observations.json` when this loop continues in `monitoring.md`. Track platform-specific mentions/citations separately from clicks, leads, assisted conversions, revenue, and Google AI impressions.

## Evidence and spam guardrails

- Owned pages must help a buyer even if the brand were removed.
- Do not manufacture third-party mentions, citations, proof, or category demand.
- Do not seed fake community discussion, engineer a misleading comparison, or hide instructions/rewards in schema, metadata, package files, or an agent-facing interface.
- Do not turn answer-engine observations into a universal GEO score or formula.
- Do not fabricate community discussion, hidden sponsorship, or undisclosed influence to force citations.
- Do not create one page for every query-fan-out phrase or duplicate comparison permutation.
- AI/search outputs are mutable observations, not rankings guaranteed by a template.
- Visibility screenshots do not prove clicks, conversions, or revenue.
- Google-specific Generative AI impressions stay in the separate `google-generative-ai-visibility.md` contract.

## Done condition

The report contains the versioned evidence baseline, primary/supporting phrase decision, competitor/framing map, only the justified page briefs, distribution concept, exact monitoring prompt set, and separated citation-versus-business measurement plan.
