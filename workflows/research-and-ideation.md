---
title: Research & Ideation
goal: Turn a blank slate (or a vague idea) into a validated niche, a triaged keyword cluster, and a planned sitemap.
playbooks:
  - references/playbooks/foundations/seo-process-overview.md
  - references/playbooks/research/keyword-fundamentals.md
  - references/playbooks/research/search-intent.md
  - references/playbooks/research/keyword-research-tools.md
  - references/playbooks/research/seo-metrics.md
  - references/playbooks/research/finding-and-validating-niches.md
  - references/playbooks/research/competitor-research.md
  - references/playbooks/research/match-and-exceed.md
  - references/playbooks/research/research-for-existing-sites.md
  - references/playbooks/research/keyword-to-sitemap.md
  - references/playbooks/maintenance/seo-operational-checklist.md
scripts:
  - scripts/workspace.py
  - scripts/search_course.py
  - scripts/ahrefs_client.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [ahrefs, serp]
outputs:
  - research/<date>_niche-candidates.json
  - research/<date>_persona-insights.json   # if personas summoned
  - keywords/<date>_keyword-map.csv
  - research/<date>_sitemap-plan.json
---

# Research & Ideation

**When to run this.** The user wants to find a niche to build, has a half-formed product idea and needs proof of demand, or owns a live site and wants new keyword/page opportunities. This is the first stage of the four-stage loop (see `references/playbooks/foundations/seo-process-overview.md`); nothing downstream (content, links) should start until research is done.

**Prerequisites.**
- **Workspace.** Resolve it first: `python3 scripts/workspace.py status --path <DIR>`. If none exists, ASK the user where to put it and whether to create one, then `python3 scripts/workspace.py init --path <DIR> --name <NAME> [--domain d] [--niche n]`. Never create a workspace silently.
- **Data sources.** Ahrefs (Keyword Explorer, Site Explorer) and the live SERP. Both have a browser-MCP fallback documented in `references/integrations/ahrefs.md` and `references/integrations/serp.md` if no API key is in `project.json`.
- **From the user.** Their build skill (developer? writer?), target country/locale, monetization intent (free tool, paid product, affiliate), and — for an existing site — the domain plus 1–3 competitor domains.

**Steps.**

1. **Orient and route.** Load `seo-process-overview.md`. Decide the entry: *new niche* (no product) → step 2; *existing site* → skip to step 6. Optionally run `python3 scripts/search_course.py "<topic>"` to surface the exact lessons + playbooks for the user's question.

2. **Find candidate niches (new build).** Load `references/playbooks/research/finding-and-validating-niches.md` for the data-dump hunt method. Run the filtered Ahrefs Keyword Explorer dump via `scripts/ahrefs_client.py` (or the browser fallback): KD ≤ 20, volume > 100, target country, plus a buildable include-word (`generator`/`maker`/`free`/`tool`, optionally `AI`). Skim for buildable gems; write candidates to `research/<date>_niche-candidates.json` via `python3 scripts/report.py note --workspace <DIR> --subdir research --name niche-candidates --data <json>`.

3. **(Optional) Summon ICP personas for divergent ideation.** When the niche is fuzzy or you want non-obvious angles/keyword seeds, dispatch persona subagents per `agents/icp-persona.md`:
   - Pick **3–6 DISTINCT** personas (different segments/budgets/sophistication). Fill every `{{PLACEHOLDER}}`, or load a saved profile from `agents/personas/*.md`.
   - Launch them **all in parallel in one message** — one Task/Agent call per persona, `model="opus"`. Do not run sequentially; you want independent voices.
   - Each returns the structured block (jobs-to-be-done, literal queries, buying triggers, objections, where they hang out, willingness-to-pay).
   - Merge the raw outputs with `agents/synthesizer.md` into ranked content angles, keyword seeds, and a niche-validation read. Save to `research/<date>_persona-insights.json`. Feed the literal queries back into steps 4–6 as additional seed keywords.

4. **Validate each candidate (the gauntlet).** Using `finding-and-validating-niches.md`, check in order: low KD; what searchers want and whether you can build it; willingness to pay (CPC, paying competitors); volume + geo split; live SERP via `scripts/serp_capture.py`; top-3 page authority; and the **size of the whole cluster** (Keyword Ideas + Also Ranks For), not just the head term. Apply `seo-metrics.md` for what KD/DR/URL-rating/CPC mean. **Walk away** on an empty surrounding cluster or a wall-of-difficulty SERP.

5. **Read and grade the SERP.** Load `references/playbooks/research/match-and-exceed.md`. For each surviving keyword, capture the live top-3 with `serp_capture.py`, identify the dominant content *type* (the format you must match), and judge whether you can *exceed* the incumbents' depth/authority. This call decides format selection later in content-production.

6. **(Existing site) Mine competitors for gaps.** Load `references/playbooks/research/research-for-existing-sites.md`. Via `ahrefs_client.py`: (a) competitor **Organic Keywords** for add-a-phrase quick wins; (b) **Top Pages** for pages you should build; (c) **Content Gap** across your domain + 2–3 competitors; (d) **Also Ranks For** off your own main keyword. Triage out high-KD/branded/non-commercial terms.

7. **Confirm winnability.** Load `references/playbooks/research/competitor-research.md`. Inspect the top results' **page authority (URL rating / referring domains to the exact URL)** — not domain authority. Low page authority among leaders = winnable. Mine each competitor's Organic Keywords for LSI variants and fold them in.

8. **Build the triaged keyword map.** Consolidate all keywords (seeds, persona queries, competitor mines, gaps) into rows with `keyword, cluster, intent, volume, kd, cpc, current_rank, target_url, priority, notes`. The data file must be JSON shaped `{"rows": [ {…}, {…} ]}` (a bare list of row objects also works). Write the CSV: `python3 scripts/report.py keywords --workspace <DIR> --data <keywords.json>` → `keywords/<date>_keyword-map.csv`.

   Use `references/playbooks/maintenance/seo-operational-checklist.md` to harden opportunity selection: KD/volume are filters, not verdicts; inspect page-level competition and SERP format. People Also Ask questions are research inputs, not an instruction to create one thin page per question.

9. **Plan the sitemap.** Load `references/playbooks/research/keyword-to-sitemap.md`. Assign the short-tail commercial head term to the home page; group keyword directions into category/hub pages; route high-supply long-tail to a programmatic layer; wire internal links upward to the converting asset. Save the tree to `research/<date>_sitemap-plan.json` (note each page's target keyword(s), intent, and chosen format from step 5).

**Decision points.**
- **New niche vs existing site** → step 2 vs step 6.
- **Green light** (low KD + buildable + paying demand + beatable SERP + large cluster) → proceed to sitemap. **Red flags** (empty cluster, or KD 50–80 with high-DA incumbents) → drop the candidate or mine sub-niches.
- **Summon personas?** Only when angles/seeds are thin or you want divergent ideas — skip for a well-understood niche to save time.
- **Exceed call** (match-and-exceed): weak incumbents → proceed; strong well-linked incumbents → deprioritize until authority is built (hand off to `authority-and-links.md`).

**Outputs.**
- `research/<date>_niche-candidates.json` — candidates + validation verdicts.
- `research/<date>_persona-insights.json` — synthesized persona angles/seeds (if run).
- `keywords/<date>_keyword-map.csv` — the triaged keyword cluster with intent, KD, volume, priority.
- `research/<date>_sitemap-plan.json` — page tree mapping every validated keyword to a page + format.

**Done when.** At least one niche/keyword cluster has passed the full gauntlet (or all are correctly rejected), the keyword map CSV exists, and every validated keyword has a home in the sitemap plan with an intent-matched format chosen. Hand the sitemap plan + keyword map to `content-production.md`; hand any "needs authority first" keywords to `authority-and-links.md`.
