---
title: AI Search Readiness Audit (GEO filename for compatibility)
goal: Assess whether a site is accessible, understandable, quotable, and corroborated enough to be a plausible source for AI-powered search experiences, then emit evidence-backed findings.
playbooks:
  - references/playbooks/foundations/seo-and-ai-future.md
  - references/playbooks/content/eeat-framework.md
  - references/playbooks/content/on-page-optimization.md
  - references/playbooks/content/content-fundamentals.md
  - references/playbooks/authority/understanding-authority.md
  - references/playbooks/maintenance/ai-search-commerce-readiness.md
references:
  - references/playbooks/content/schema-types-reference.md
scripts:
  - scripts/workspace.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [serp]
outputs:
  - audits/<date>_geo-audit.md           # AI-search readiness verdict + findings (via report.py audit)
  - audits/<date>_geo-findings.json      # raw findings payload
---

# AI Search Readiness Audit

**When to run this.** The user asks “do we show up in ChatGPT / Perplexity / AI Overviews?”, wants to know why a brand is not being cited by AI/search tools, asks whether current product/entity data and conversion paths are agent-ready, or the standard `site-audit.md` AI-search checklist flagged meaningful issues. This workflow checks whether the site is easy to access, understand, quote, corroborate, and—when applicable—act on without pretending to predict proprietary AI rankings.

All checks are inspection-based. A basic pass needs no SEO API keys — use `serp_capture.py` or browser fallback where the workflow needs SERP/page-source evidence. Direct platform checks may require a browser/account and should be reported as observed evidence, not universal truth. The workflow is read-only and does not change robots.txt, publish `/llms.txt`, or edit the site.

**Prerequisites.**
- **Workspace** resolved (`python3 scripts/workspace.py status --path <DIR>`; ASK before creating if absent). The domain should be in `project.json`.
- **From the user:** the domain + a short list of key topics, product lines, or prompts they care about in AI/search experiences.
- **Data sources:** `serp_capture.py` / browser for page-source checks, robots.txt, `/llms.txt`, and brand/source searches. Load `references/playbooks/foundations/seo-and-ai-future.md` for strategic context.

---

## Background: Why This Is a Distinct Audit

This is not a replacement for SEO. It is a focused evidence review of the pieces that make content easier for AI-search/retrieval systems to access, parse, quote, and corroborate:

- **Access:** relevant crawlers/fetchers can reach the important pages and content is visible in initial HTML where practical.
- **Extraction:** pages contain clear, self-contained answers, tables, definitions, and evidence that can be quoted.
- **Corroboration:** the brand/entity is mentioned consistently across trusted third-party sources, not just on owned pages.
- **Trust:** authorship, citations, schema, reputation, and policies make the content credible.

Avoid unsupported magic-number claims. Treat platform-specific citation studies as useful directional research, not permanent laws. Always inspect the current SERP/source set for the topic being audited.

## Readiness Dimensions

Do **not** present this as a platform formula. There is no public universal numeric metric from Google/OpenAI/Perplexity for this. Use these dimensions as an internal rubric and keep the output qualitative by default.

| Dimension | What it asks |
|---|---|
| Citability | Can the page provide concise, self-contained, well-supported passages that are easy to quote? |
| Structure | Is the content easy to parse: headings, lists, tables, definitions, FAQs where useful? |
| Authority/entity | Is the brand/person/product corroborated by credible on-site and third-party evidence? |
| Technical access | Can relevant crawlers/fetchers reach the content, and is key content visible in initial HTML where possible? |
| Evidence formats | Are screenshots, demos, tables, charts, data, or video used where they improve trust/usefulness? |

Report a qualitative verdict (`strong`, `moderate`, `weak`, `blocked`) plus evidence-backed findings. Avoid numeric ratings; if a user insists on an internal benchmark, label it as a local heuristic, not a search-engine metric.

---

## Steps

1. **Scope and baseline.** Identify the priority pages: homepage, product/service pages, and high-value informational pages. Record the target prompts/topics and whether the site is static/SSR, hybrid, or client-rendered SPA.

2. **Citability audit.** For each priority page, assess whether the page can be quoted cleanly:
   - Does the opening section directly answer the primary query?
   - Are there concise, self-contained answer blocks that make sense without the rest of the page?
   - Are definitions written clearly (`X is…`, `X refers to…`) where definitions matter?
   - Does the content include specific examples, sourced statistics, screenshots, methodology, or named-source citations?
   - Are conclusions placed near the start of sections rather than buried at the end?
   - Flag findings where important pages bury the answer, lack evidence, or cannot stand alone when quoted.

3. **Structure audit.** Inspect heading hierarchy and content format:
   - H1→H2→H3 hierarchy is clean.
   - H2/H3 headings match real user questions or topic entities.
   - Paragraphs are readable and scannable.
   - Tables/lists are used for comparisons, specs, pricing, steps, and pros/cons.
   - FAQ/Q&A sections are used only when they genuinely help users.
   - Flag findings where weak structure makes extraction or human scanning harder.

4. **Authority and brand signal audit.** Search for corroborating third-party evidence:
   - Brand/product mentions on reputable review/comparison pages, directories, partner pages, industry blogs, news, podcasts, YouTube, Reddit, Wikipedia/Wikidata where legitimately applicable.
   - Consistent entity details across site, schema, social profiles, directories, docs, and third-party pages.
   - On-page authority signals: named author/reviewer, publication/update date, credentials, external sources, case studies, testimonials.
   - Backlink/mention quality per `authority-and-links.md` if link data is available.
   - Flag findings where the brand has little corroboration, inconsistent entity signals, or missing on-page authorship/trust evidence. Do not require Wikipedia for brands that are not legitimately notable.

5. **Technical access audit.** Check whether AI/search crawlers and lightweight fetchers can access the important content.

   **Crawler policy (robots.txt):**
   Fetch `<domain>/robots.txt`. Check directives for relevant AI/search crawlers, for example:

   | User agent | Owner / use |
   |---|---|
   | OAI-SearchBot | OpenAI search features / ChatGPT search visibility |
   | GPTBot | OpenAI model-training crawl control, separate from search visibility |
   | ChatGPT-User | OpenAI user-triggered fetches; not the Search opt-out control |
   | Claude-SearchBot | Anthropic search-result quality / search visibility |
   | ClaudeBot | Anthropic model-training crawl control |
   | Claude-User | Anthropic user-triggered fetches |
   | PerplexityBot | Perplexity search-result visibility |
   | Perplexity-User | Perplexity user-triggered fetches |

   If a crawler/search bot is blocked, document the affected platform and tradeoff. User-triggered fetchers may follow different rules from automated crawlers, so use current provider docs and logs before making a platform-specific claim. Do not override the owner's licensing/privacy choice without approval.

   **`/llms.txt` presence:**
   Fetch `<domain>/llms.txt`. If absent, do not treat it as a defect by itself; optionally note it as a machine-readable guidance opportunity when the project cares about AI/retrieval documentation. It is emerging guidance, not a confirmed ranking factor. If present, verify: site title, short description, key page links with descriptions, and no stale/false claims.

   **Licensing / usage signals:**
   If content licensing matters, check whether the site publishes machine-readable AI usage/licensing terms. Treat this as policy clarity, not an SEO ranking lever.

   **Initial HTML / SSR check:**
   Compare rendered page to raw HTML source. Are primary content, key answers, pricing, product descriptions, author info, and schema present without relying entirely on client-side JavaScript? If important pages are JS-only and key content is absent from raw HTML, flag severity based on verified crawler/fetcher impact and business importance.

   Flag findings for unwanted crawler blockers, unclear crawler/licensing posture, JS-only key content, or inaccurate/stale `/llms.txt` guidance.

6. **Multi-modal evidence audit.** Inspect whether content includes evidence formats that improve user trust and quotability:
   - Informational images/screenshots/diagrams where they add proof.
   - Video, demos, or walkthroughs where useful.
   - Tables, charts, or original data when claims are quantitative.
   - Flag findings when important claims lack supporting evidence formats or when richer media would materially improve trust/usefulness.

7. **Commerce and agentic-readiness audit (when applicable).** Load `references/playbooks/maintenance/ai-search-commerce-readiness.md` for retailers, marketplaces, paid products, bookings, or services whose facts change. Compare crawled pages, feeds/APIs actually used by the business, and live-site state for identifiers, variants, price, currency, availability, language, freshness, shipping/promotions, and policy consistency. Test the real checkout, booking, lead, or support path without completing a consequential action. Keep platform visibility, landing sessions, assisted conversions, transactions, revenue, and controlled causal evidence as separate evidence grades. Skip this dimension explicitly when the site has no transactional/current-data surface.

8. **Prioritize and emit the report.** Assign a qualitative readiness verdict (`strong | moderate | weak | blocked`) and rank findings by severity (`critical | high | medium | low`) and business impact.

   Assemble `{readiness_verdict, dimension_notes:{citability, structure, authority, technical_access, evidence_formats, commerce_agentic_readiness}, findings:[...]}` and run:
   ```bash
   python3 scripts/report.py audit \
     --workspace <DIR> \
     --title "GEO audit: <domain> <date>" \
     --data <geo-findings.json>
   ```
   `report.py` sorts findings by severity into a prioritized table → `audits/<date>_geo-audit.md`.

---

## Decision Points

- **Crawler/search bot blocked for a desired platform** → potential high/critical issue only if the owner wants that platform to access the content; confirm policy before recommending changes.
- **SPA with JS-only key content** → high/critical only when important content is inaccessible to relevant fetchers or users; recommend SSR/static rendering for key content and schema where appropriate.
- **Good rankings but weak observed AI citation** → inspect whether cited/top-ranking third-party sources mention the brand and whether owned pages contain quotable, sourced answer blocks.
- **Blocked / very weak readiness** → prioritize technical access and citability.
- **Weak readiness** → improve structure/content and build credible third-party corroboration where evidence shows a gap.
- **Moderate readiness** → improve entity consistency, appropriate schema, optional `/llms.txt` guidance, and richer evidence where useful.
- **Strong readiness** → monitor observed platform/source changes; maintain authority and freshness.

**Relationship to standard site-audit.** The AI-search block in `workflows/site-audit.md` is a rapid signal pass. This workflow is the deep-dive: it reviews each readiness dimension and produces a standalone deliverable.

**Routing findings:**
- Authority/mention findings → `authority-and-links.md`.
- Content structure fixes → `content-production.md`.
- Technical access and SSR issues → engineering-fix bucket in `site-audit.md`.
- Schema/entity gaps → `references/playbooks/content/schema-types-reference.md` + engineering/content brief.
- Feed/live-state/conversion contradictions → `references/playbooks/maintenance/ai-search-commerce-readiness.md` + the owning product/engineering backlog.

**Outputs.**
- `audits/<date>_geo-audit.md` — AI-search readiness verdict, dimension notes, findings ranked by severity and impact.
- `audits/<date>_geo-findings.json` — raw findings for future comparison.

**Done when.** All five core readiness dimensions—and the commerce/agentic dimension when applicable—have been reviewed for priority pages; every finding has severity, affected page(s), evidence, and concrete fix; visibility and business-outcome evidence remain separated; the readiness verdict is assigned; and the report is written to the workspace.
