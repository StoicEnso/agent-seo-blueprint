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
  - references/playbooks/authority/linkbuilding-what-not-to-do.md
  - references/playbooks/research/match-and-exceed.md
scripts:
  - scripts/workspace.py
  - scripts/ahrefs_client.py
  - scripts/serp_capture.py
  - scripts/report.py
integrations: [ahrefs, serp]
outputs:
  - outreach/<date>_opportunities.json   # ranked backlink targets
  - outreach/<date>_drafts.json          # drafted (NOT sent) outreach messages
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
   - **Link stealing** (`link-stealing.md`) — find roundups/listicles linking a weaker competitor but not you; pitch "add me" or "swap the weak link." Needs you to be genuinely better.
   - **Affiliate program** (`affiliate-programs.md`) — if there's a paid product: clean `?via=` links, generous commissions, recruit competitor affiliates (Ahrefs Backlinks filtered to the affiliate param). Quote conversion rate.
   - **HARO / Help a B2B Writer Out** (`haro.md`) — if someone can speak as an expert: draft credible, specific quotes (add a Loom touch) for high-DR editorial links.
   - **Manual outreach** (`manual-outreach.md`) — revisit-the-topic pitches, missing-link asks, free-access offers, and the case-study trade (target smaller tools with few case studies).
   - **Content rings** (`content-rings-for-links.md`) — link the new page from your own aged, genuinely-useful properties for a launch head start. (Build new ring properties via `content-production.md`'s content-ring path.)
   - **Audience / acquisition / other** (`building-an-audience.md`, `acquiring-domain-authority.md`, `other-link-building.md`) — longer-horizon plays.

3. **Run the guardrail before building any list.** Load `references/playbooks/authority/linkbuilding-what-not-to-do.md`. Refuse: bought cheap link packages, uniform exact-match anchor spam, forum/Reddit/comment URL spam, PBNs/link farms, off-topic or niche-mismatched links. If a chosen tactic drifts into these, drop it — penalties here can be permanent.

4. **Build the ranked opportunity list.** For each tactic, gather concrete targets via `ahrefs_client.py` + `serp_capture.py`: the linking page URL, referring-domain DR, dofollow?, outbound-link count (dilution), topical relevance, the tactic that fits, the contact handle/source, and a priority score. Save with `python3 scripts/report.py note --workspace <DIR> --subdir outreach --name opportunities --data <json>` → `outreach/<date>_opportunities.json`.

5. **DRAFT outreach (do not send).** For each high-priority target, draft a short, personal, value-first message per the relevant playbook (e.g. link-stealing: "saw you link [competitor], here's a stronger tool"; affiliate: commission + conversion rate; HARO: credibility hook + concrete answer; case-study trade: offer to write it). Keep each message specific to the recipient. Save all drafts to `outreach/<date>_drafts.json` with `{target_url, contact, tactic, subject, body, status:"DRAFT"}`.

6. **Optional — disavow cleanup.** If `site-audit` or an affiliate-spam review surfaced toxic referring domains, build a disavow file per `linkbuilding-what-not-to-do.md` / `affiliate-programs.md` and write `outreach/<date>_disavow.txt`. Hand it to the user to upload in Search Console — do NOT submit it.

7. **Hand off for confirmation.** Present the opportunity list + drafts to the user. Sending, posting, submitting the affiliate recruitment, or uploading the disavow file happens ONLY after the user explicitly confirms — and the user (or a user-approved channel) does the actual send. Log replies/sends back into the workspace for `monitoring.md`'s leading-indicator tracking.

**Decision points.**
- **Paid product?** Yes → affiliate program is high-leverage. No → lean on link-stealing, HARO, manual outreach, content rings.
- **Expert available?** Yes → HARO. No → skip it.
- **Add-alongside vs swap** (link stealing): neutral roundup → add; clearly inferior/dead listed tool → swap.
- **VIP affiliate rate:** reserve for the few high-DR, exact-niche sites that actually move rankings.
- **Any tactic touching the what-not-to-do list** → drop it (asymmetric, possibly permanent downside).
- **Send/submit anything?** Only on explicit user confirmation. Default is draft-and-hold.

**Outputs.**
- `outreach/<date>_opportunities.json` — ranked backlink targets with DR/dilution/relevance/tactic.
- `outreach/<date>_drafts.json` — personalized outreach drafts, `status:"DRAFT"`, never sent by the agent.
- `outreach/<date>_disavow.txt` — optional disavow file for the user to submit.

**Done when.** A ranked opportunity list and matching personalized drafts exist in the workspace, every chosen tactic passed the guardrail, and nothing has been sent/submitted without explicit user confirmation. Feed sent-outreach + acquired-link counts into `monitoring.md` (leading indicators) and re-check competitor backlink pace there monthly.
