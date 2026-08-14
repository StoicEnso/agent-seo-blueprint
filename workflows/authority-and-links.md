---
title: Authority & Links
goal: Pick link-building tactics, build a ranked backlink opportunity list, and DRAFT outreach — never auto-sent.
playbooks:
  - references/playbooks/authority/understanding-authority.md
  - references/playbooks/authority/link-stealing.md
  - references/playbooks/authority/affiliate-programs.md
  - references/playbooks/authority/haro.md
  - references/playbooks/authority/manual-outreach.md
  - references/playbooks/authority/content-rings-for-links.md
  - references/playbooks/authority/building-an-audience.md
  - references/playbooks/authority/acquiring-domain-authority.md
  - references/playbooks/authority/other-link-building.md
  - references/playbooks/authority/directory-submissions.md
  - references/playbooks/authority/startup-backlink-directory-submissions.md
  - references/playbooks/authority/wikipedia-dead-link-building.md
  - references/playbooks/authority/linkbuilding-what-not-to-do.md
  - references/playbooks/research/match-and-exceed.md
  - references/playbooks/maintenance/cross-platform-ai-citation-loop.md
scripts:
  - scripts/workspace.py
  - scripts/ahrefs_client.py
  - scripts/dataforseo_client.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [ahrefs, dataforseo, serp]
outputs:
  - outreach/<date>_opportunities.json   # ranked backlink targets
  - outreach/<date>_drafts.json          # drafted (NOT sent) outreach messages
  - outreach/<date>_directory-submissions.csv  # verified directory/entity pipeline
  - outreach/<date>_wikipedia_dead_links.json  # verified research candidates; no live edit
  - outreach/<date>_disavow.txt          # optional disavow file (user submits)
---

# Authority & Links

**When to run this.** Content is live but won't climb (great content with no links rarely ranks), `match-and-exceed`/`site-audit` flagged "needs authority first," or the user wants an ongoing link-acquisition motion. This is stage 3 of the loop.

> **IRREVERSIBLE-ACTION GATE.** This workflow **drafts** outreach and assembles target lists. It NEVER sends email, posts, submits forms, or runs an affiliate/disavow action. Every message is written for the user to review and send; every disavow file is handed to the user to submit. Do not send anything without explicit, per-batch user confirmation.

**Prerequisites.**
- **Workspace** resolved (`python3 scripts/workspace.py status --path <DIR>`; ASK before creating if absent).
- **From the user:** the target money keyword(s) + the page being promoted; whether there's a paid product (enables affiliate); how much manual effort they'll sustain; who can speak as an expert (enables HARO).
- **Product-quality precheck:** load `references/playbooks/authority/understanding-authority.md` and audit the page as a writer about to link to it — fix embarrassing flows / pop-ups / slow loads FIRST. Displacement tactics depend on `match-and-exceed` (you must be objectively better).
- **Data sources:** Ahrefs (Site Explorer → Backlinks) via `ahrefs_client.py`; live SERP via `serp_capture.py`; contact-finding (e.g. Hunter.io) is a manual/user step the drafts reference. Browser fallbacks in `references/integrations/ahrefs.md` / `serp.md`.

**Steps.**

1. **Set strategy & map the landscape.** Load `understanding-authority.md`. Identify the top-ranking competitor for the money keyword (`serp_capture.py`), then Site-Explorer it in Ahrefs (`ahrefs_client.py`) → Backlinks. Note high-DR, dofollow, low-dilution, topically-relevant referring domains — this is the raw target pool. Weight by quality (DR is logarithmic; few outbound links = more value passed), not count.

2. **Pick tactics for this project.** Choose from the menu based on fit (you can run several):
   - **Link stealing / listicle-gap outreach** (`link-stealing.md`) — find live category roundups with a real editorial omission; prefer an add-alongside ask when the product adds distinct reader value, and reserve replacement for broken, discontinued, obsolete, or criterion-mismatched listings. Record criteria, disclosure/affiliate state, current link attributes, contact evidence, and checked date. Never auto-send or repeat a source's backlink count as an expected result.
   - **Affiliate program / competitor-affiliate mining** (`affiliate-programs.md`) — for a paid product with sustainable unit economics: fingerprint verified public referral routes, qualify the competitor's editorial affiliates, model a defensible offer, and draft `test/add`, `comparison`, or `switch` asks. Never invent terms or blindly outbid.
   - **HARO / Help a B2B Writer Out** (`haro.md`) — if someone can speak as an expert: draft credible, specific quotes (add a Loom touch) for high-DR editorial links.
   - **Manual outreach** (`manual-outreach.md`) — revisit-the-topic pitches, missing-link asks, free-access offers, and the case-study trade (target smaller tools with few case studies).
   - **Content rings** (`content-rings-for-links.md`) — link the new page from your own aged, genuinely-useful properties for a launch head start. (Build new ring properties via `content-production.md`'s content-ring path.)
   - **Directories / entity profiles** (`directory-submissions.md`) — relevant public directories, product indexes, launch platforms, review profiles, and entity profiles. Start with niche-filtered discovery sources, preserve source claims as unverified lineage, then verify the destination-owned submit route and a live public listing. Never sort solely by screenshot DR. Use `startup-backlink-directory-submissions.md` to turn sourced startup lists into a classified verification queue.
   - **Wikipedia dead citations** (`wikipedia-dead-link-building.md`) — verify the dead URL and archive, map the exact supported claim, and brief a materially better neutral resource. Research only by default; publishing, talk-page requests, editor contact, and edits are separately approval-gated.
   - **Audience / acquisition / other** (`building-an-audience.md`, `acquiring-domain-authority.md`, `other-link-building.md`) — longer-horizon plays.

   When authority work is routed from `geo-audit.md`, `category-citation-loop.md`, or `cross-platform-ai-citation-loop.md`, map which independent domains are actually cited for the fixed buyer-question set and prioritize editorially appropriate omissions over raw DR volume. Keep provider observations separated by platform/surface; a Copilot or ChatGPT citation gap does not prove a Google deficiency.

   For directory/entity discovery, register aggregators/checklists in `assets/directory-discovery-sources.csv`, then preserve candidate-level lineage in `assets/startup-backlink-candidates.csv`. Its original intake supplies 122 deduplicated research leads reconstructed from 127 source mentions. Every row starts `UNVERIFIED_SOURCE_LEAD`; source-reported DR, traffic, price, approval time, link type, and submission routes must never be presented as current fact. Live-verify identity, eligibility, relevance, a destination-owned submission route, public indexability, current cost/moderation, and actual link behavior before a candidate reaches the opportunity list.

3. **Run the guardrail before building any list.** Load `references/playbooks/authority/linkbuilding-what-not-to-do.md`. Refuse: bought cheap link packages, uniform exact-match anchor spam, forum/Reddit/comment URL spam, PBNs/link farms, off-topic or niche-mismatched links. If a chosen tactic drifts into these, drop it — penalties here can be permanent.

4. **Build the ranked opportunity list.** For each tactic, gather concrete targets via `ahrefs_client.py` + `serp_capture.py`: the linking page URL, referring-domain DR, dofollow?, outbound-link count (dilution), topical relevance, the tactic that fits, the contact handle/source, and a priority score. Affiliate prospects also require `competitor`, `competitor_referral_pattern`, `evidence_url`, `competitor_program_terms_verified_at`, `page_type`, `current_placement`, `ask_type`, `suggested_offer`, `offer_basis`, `vip_candidate`, and `quality_flags`. Directory/entity candidates also require source lineage, `route_type`, a destination-owned `submission_url` with `submission_url_verified_at`, `public_indexable`, `link_attribute` observed from a live listing, and `last_verified_at`; reject private-account-only or unrelated profiles. Save with `python3 scripts/report.py note --workspace <DIR> --subdir outreach --name opportunities --data <json>` → `outreach/<date>_opportunities.json`.

5. **DRAFT outreach (do not send).** For each high-priority target, draft a short, personal, value-first message per the relevant playbook (e.g. link-stealing: "saw you link [competitor], here's a stronger tool"; affiliate: reference the exact competing placement, verified commission structure, defensible product advantage, and only real conversion evidence; HARO: credibility hook + concrete answer; case-study trade: offer to write it). When the goal is citation coverage, offer checked facts, screenshots, criteria, methodology, and honest limitations — never fake discussion, hide sponsorship, or promise ranking/citation outcomes. Keep each message specific to the recipient. Save all drafts to `outreach/<date>_drafts.json` with `{target_url, contact, tactic, subject, body, status:"DRAFT"}`.

6. **Optional — disavow cleanup.** If `site-audit` or an affiliate-spam review surfaced toxic referring domains, build a disavow file per `linkbuilding-what-not-to-do.md` / `affiliate-programs.md` and write `outreach/<date>_disavow.txt`. Hand it to the user to upload in Search Console — do NOT submit it.

7. **Hand off for confirmation.** Present the opportunity list + drafts to the user. Sending, posting, creating a directory/profile account, submitting a listing, submitting affiliate recruitment, or uploading the disavow file happens ONLY after the user explicitly confirms — and the user (or a user-approved channel) does the actual send. For approved directory work, track `candidate -> verified -> approved -> submitted -> live | rejected | expired` in `assets/directory-submission-tracker.csv` and save the public URL/evidence. Log replies/sends back into the workspace for `monitoring.md`'s leading-indicator tracking.

**Decision points.**
- **Paid product?** Yes → affiliate program is high-leverage. No → lean on link-stealing, HARO, manual outreach, content rings.
- **Expert available?** Yes → HARO. No → skip it.
- **Add-alongside vs swap** (link stealing): neutral roundup → add; clearly inferior/dead listed tool → swap.
- **Listicle follow-up:** one unanswered reminder is the default maximum unless the owner approves a different recipient-appropriate cadence. Any paid/affiliate inclusion must be disclosed and appropriately qualified; do not buy undisclosed followed placement.
- **VIP affiliate rate:** reserve for the few high-DR, exact-niche sites that actually move rankings.
- **Citation-gap outreach?** Only pitch genuine omissions with verifiable evidence; never use fabricated mentions, spam, or undisclosed influence.
- **Any tactic touching the what-not-to-do list** → drop it (asymmetric, possibly permanent downside).
- **Directory/profile route?** Treat aggregators as discovery only. Verify relevance, a destination-owned submission route, a public indexable listing, current moderation/cost, and actual link behavior; reject private profile links and directory spam.
- **Paid directory?** Require audience/economic fit and explicit owner approval. Do not buy a placement merely because a source claims high DR or a followed link.
- **Send/submit anything?** Only on explicit user confirmation. Default is draft-and-hold.

**Outputs.**
- `outreach/<date>_opportunities.json` — ranked backlink targets with DR/dilution/relevance/tactic; affiliate rows also carry referral-pattern evidence, verified program terms, placement/ask type, offer basis, and quality flags.
- `outreach/<date>_drafts.json` — personalized outreach drafts, `status:"DRAFT"`, never sent by the agent.
- `outreach/<date>_directory-submissions.csv` — verified candidate/listing states and live evidence.
- `outreach/<date>_disavow.txt` — optional disavow file for the user to submit.

**Done when.** A ranked opportunity list and matching personalized drafts exist in the workspace, every chosen tactic passed the guardrail, and nothing has been sent/submitted without explicit user confirmation. Directory work also has verified route evidence and a tracked public listing URL or rejection reason. Wikipedia research either has ten verified candidates with dead/archive/COI evidence or an exhausted-search report; it never implies that an edit occurred. Feed approved sends + acquired-link counts into `monitoring.md` and re-check competitor backlink pace there monthly.
