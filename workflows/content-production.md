---
title: Content Production
goal: Take a validated keyword (or sitemap entry) and produce an intent-matched, on-page-optimized content brief ready to build.
playbooks:
  - references/playbooks/content/content-fundamentals.md
  - references/playbooks/content/content-types-overview.md
  - references/playbooks/content/programmatic-seo.md
  - references/playbooks/content/free-tools-strategy.md
  - references/playbooks/content/content-pages.md
  - references/playbooks/content/landing-pages.md
  - references/playbooks/content/articles.md
  - references/playbooks/content/content-rings.md
  - references/playbooks/content/on-page-optimization.md
  - references/playbooks/content/content-what-not-to-do.md
  - references/playbooks/research/match-and-exceed.md
  - references/playbooks/research/search-intent.md
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
---

# Content Production

**When to run this.** A keyword (or a row from a `research/<date>_sitemap-plan.json`) is validated and you need to decide *what kind of page* to build and produce a brief for it. Runs after `research-and-ideation.md`. **This workflow plans and briefs content — it never publishes.** Building/publishing is an irreversible action that requires explicit user confirmation outside this workflow.

**Prerequisites.**
- **Workspace** resolved (`python3 scripts/workspace.py status --path <DIR>`; ASK before creating if absent).
- **Inputs:** the target keyword(s) and intent from the keyword map / sitemap plan; the target country/locale; the operator's build strength (developer vs writer); the product/offer to upsell.
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

3. **(Optional) Summon ICP personas for content angles.** When you need fresh angles, FAQ questions, or objections to address on the page, dispatch persona subagents per `agents/icp-persona.md`: pick 3–6 distinct personas, launch **all in parallel, `model="opus"`**, then merge with `agents/synthesizer.md`. Use their literal queries as H2s/FAQ entries and their objections as copy to defeat. Save to `research/<date>_content-angles.json`.

4. **Load the format-specific method and draft the page plan.** Open the playbook for the chosen type and follow its method:
   - **Programmatic SEO:** confirm the scalability gate (hundreds of pages), lock head keyword + leaf pattern *before* generating, plan data acquisition → shaping → hub/leaf templates → offer injection. Heed crawl-budget batching.
   - **Free tool:** pick the angle (free counterpart / adjacent audience / link magnet); spec a tool that's *easier* than the top 3; plan killer title + meta variants; add How-it-works + FAQ so it isn't thin; plan the upsell.
   - **Content page:** choose the sub-pattern (comparison / success-story-review / niche hub / examples-how-to / integration); plan sections, screenshots, pricing/testimonial blocks; load niche/long-tail keywords here, off the homepage.
   - **Landing page:** one keyword per page, inform + link straight to checkout.
   - **Article:** confirm you'll invest in genuine human writing; if not, pick a different format.

5. **Apply on-page optimization to the brief.** Load `references/playbooks/content/on-page-optimization.md`. Specify: meta title (main keyword, intent-matched, natural) and description (synonyms/variants); internal links to/from related pages; a page-speed plan (prefer static generation); and canonicals for any parameterized/duplicate URLs.

6. **Run the what-not-to-do guardrail.** Load `references/playbooks/content/content-what-not-to-do.md` as a pre-brief checklist: no AI content spam, respect crawl budget (batch large publishes), no keyword stuffing, no duplicate/cannibalizing pages, no thin content. Flag any risk in the brief.

7. **Emit the content brief.** Assemble a brief object: `{keyword, intent, content_type, sub_pattern, serp_summary, outline (H1/H2s), meta_title, meta_description, target_keywords[], internal_links[], data_sources (pSEO), upsell/offer, on_page_checklist, guardrail_notes, persona_angles?}`. Write it with `python3 scripts/report.py note --workspace <DIR> --subdir briefs --name <keyword-slug>-brief --data <brief.json>` → `briefs/<date>_<keyword-slug>-brief.json`. Repeat steps 1–7 per page when briefing a whole sitemap.

**Decision points.**
- **Format selection** is driven by the live SERP + the intent→format map, NOT by preference. If the SERP shows articles, do not brief a landing page.
- **Programmatic vs hand-built:** hundreds of scalable long-tail variants → programmatic; only 3–5 pages of opportunity → write/build them individually.
- **Article go/no-go:** only if genuine quality writing is committed; otherwise pick a developer-friendly format.
- **Summon personas?** Only when angles/FAQ/objections are thin.
- **Build/publish?** Out of scope here. Producing the brief is the deliverable; any build or publish step requires explicit user confirmation.

**Outputs.**
- `briefs/<date>_<keyword-slug>-brief.json` — one intent-matched, on-page-optimized brief per page, ready to hand to a builder.
- `research/<date>_content-angles.json` — synthesized persona angles/FAQs (if run).

**Done when.** Every targeted keyword has a brief whose format matches the live SERP, includes an outline + metadata + internal-link + upsell plan, and passes the what-not-to-do checklist. Hand briefs to the user/builder for the (confirmation-gated) build; route "ranks but needs links" pages to `authority-and-links.md` and add new pages to `monitoring.md`.
