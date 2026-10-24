---
title: other-link-building
area: authority
source_lessons: ["04-13"]
tools: [ahrefs, hunter]
---

# other-link-building

**What it is.** A toolkit of additional, well-known link-building tactics worth keeping in rotation — linkable assets, broken-link building, the skyscraper technique, guest posting, podcasts, link swapping, forum participation, and (with heavy caveats) ABC link boosting.

**When to use.**
- Your core tactics (link stealing, affiliates, HARO, outreach) are running and you want more surface area.
- A specific situation fits one of these (you have a dataset for an infographic, you found dead links to replace, you got invited to a podcast, etc.).
- You want cheap, on-topic links that competitors overlook.

**Method (pick what fits the situation).**
1. **Linkable assets:** commission a designer to turn research/data into an infographic, then offer it to writers who cover that topic. They get easy content; you get a backlink for the embed/credit.
2. **Broken-link building:** find articles linking to dead/offline resources (Ahrefs has a tool for this), confirm you have content that could replace them, and email the writer: their link is broken, here's a working, valuable replacement (yours). Effectively link-stealing for links that no longer resolve.
3. **Skyscraper technique:** find content with many backlinks, build something substantially better, then tell each site linking to the weaker/empty resource that you've made a far stronger version worth linking to instead. (Also covered on the research side.)
4. **Guest posting:** offer a company with a blog a free article on a relevant topic in exchange for including your link in the content. They get free content; you inject a backlink on a higher-DR site.
5. **Podcasts:** appear on podcasts — show notes typically link to your site, and the host's own website usually lists the episode with another backlink, plus visibility on Apple Podcasts/Spotify. When a link is missing from the notes, just ask (see [[manual-outreach]]).
6. **Link swapping:** arrange a reciprocal link with a relevant site ("I'll link you, you link me"). Do this only with a few good, on-topic sites — overdoing reciprocal links is detectable and devalued by Google.
7. **Forum participation (Quora/Reddit/etc.):** answer questions thoroughly and genuinely, linking back only where it truly adds value. Largely devalued now and easy to overdo — treat as minor profile-building, never as spam.
8. **ABC link boosting (gray/black hat — caution):** strengthen a site that links to you by buying links to *that* site, indirectly boosting you. The course flags this as gray/black-hat link buying; understand it exists but treat it as out of bounds unless you fully accept the risk — cross-reference [[linkbuilding-what-not-to-do]].

**Decision criteria / heuristics.**
- Favor tactics that produce genuinely useful content (infographics, skyscraper, broken-link replacements) — they're durable and low-risk.
- Use link swaps and forums sparingly and authentically; volume here triggers Google's penalties.
- Podcasts and guest posts are high-value when topical and on decent-DR sites.
- ABC boosting is gray/black hat; the safe default is to skip it.

**Example.** The course mix: producing an infographic for writers to feature; using Ahrefs to spot articles pointing to a dead resource and offering a live free tool as the replacement; a skyscraper upgrade of a weak, well-linked resource pitched to its linkers; a guest post placing a backlink on a high-DR blog; a podcast appearance (Andreessen Horowitz / a16z) yielding a high-DR show-notes link; and a reciprocal swap with a peer founder's site — kept to just a few quality partners so it doesn't look manipulative.

**Pitfalls.**
- Over-swapping reciprocal links or spamming forums — Google detects patterns and devalues/penalizes.
- Posting low-effort forum answers just to drop a link.
- Treating ABC boosting as safe — it's link buying with real banning risk (see [[linkbuilding-what-not-to-do]]).
- Auto-sending the outreach legs (infographic, broken-link, skyscraper, guest-post pitches) — draft for user review.

## Directory and entity profiles

Treat directory submissions as a separate verification-led lane, not a bulk backlink tactic. Use [[directory-submissions]] for candidate qualification, submission packaging, approval gates, and live-listing evidence.

Do not cite directory DR screenshots as proof of value; verify relevance, public indexability, eligibility, and the actual listing first.

**Related.** [[link-stealing]] (broken-link & skyscraper are variants), [[manual-outreach]] (podcast missing-link asks), [[directory-submissions]], [[linkbuilding-what-not-to-do]] (ABC boosting / swap-overuse risk), [[understanding-authority]]. Course ref: 04-13.


## Source-led product and resource methods — 24 October 2026

The research inventory is [backlink-method-research.csv](../../../assets/backlink-method-research.csv).
It has **26 research rows, not 26 verified backlinks**. Every row is
`RESEARCH_ONLY_NOT_APPROVED`. Evidence, source claims, audience value and authorisation are
separate. [The source review](../../../assets/backlink-method-source-review-20261024.json)
records the 12-post quoted chain and the 7 comments actually observed. The quoted posts,
not the comments, supplied the additional concrete platform methods. Public reply access was
partial; never claim every reply was checked.

### 1. Documentation benchmark report: Fern Agent Score

Use only for a genuine public documentation site. A report can help find broken agent access,
missing content, unreadable responses and parse errors. Prepare useful, accurate docs first.
The source proposes `llms.txt`, Markdown page representations and `npx afdocs`. Treat these as
agent-readability options, **not Google indexing requirements or a ranking factor**. Preserve
HTML/Markdown content parity, stable URLs, access controls and useful page structure.

The local `npx afdocs` suggestion can download and execute third-party code. It is not a safe
read-only command by default: inspect the package and version, obtain required installation
approval, use an isolated environment, and never expose private docs or credentials. No package
was run in this source review.

First-party sample checked on 24 October:
- Page: <https://buildwithfern.com/agent-score/company/resend>, HTTP 200.
- Docs anchor: `https://resend.com/docs`, `rel="noopener noreferrer"`.
- No `nofollow`, `ugc` or `sponsored` token appeared on that sampled anchor. `noopener` and
  `noreferrer` are not `nofollow`; there is no HTML `dofollow` attribute to require.
- No robots `noindex` or `X-Robots-Tag` appeared on that response. This is **not proof of actual
  indexing**, Google ranking credit, clicks, or durable retention.

Score submission can disclose a URL and create a public result. It is an external action,
not a harmless lookup. Draft-and-hold the exact target and consent first. A result page and
**Request listing** on the leaderboard are separate steps. Do not guess a result slug: the
plausible `/company/adaptlypost` URL returned a noindex not-found shell, not a verified listing.
After an approved run, inspect the exact public URL, rendered docs anchor, redirects, canonical,
robots and dated index observations. DR 77 is the creator's unverified domain metric, not an
observed benefit for your docs.

### 2. Useful product distribution, not empty profiles

The author's quoted chain adds these routes. Each needs current destination-owned eligibility,
terms, privacy and rendered-link evidence; creator speed and acceptance claims are anecdotes.

| Route | Reader/customer job | Exact caution before a pilot |
| --- | --- | --- |
| Postman public team/profile + workspace | Browse and test a real API using a useful collection | Sanitise OpenAPI, examples, environments and exports; never publish stored API keys. Official public-workspace docs support the route. On the rendered `postman.com/adaptlypost` profile, the Website social link to `https://adaptlypost.com/` had `rel="noreferrer noopener"`, but the description links had `nofollow`. Verify each link slot; one sample is not a blanket followed-link or indexing claim. |
| Chrome Web Store | One useful browser task connected to the product | Real extension, minimal permissions, privacy and maintenance. Recheck developer fees; no registration or store submission from this research task. Already a candidate in the directory inventory: enrich rather than duplicate. |
| npm CLI | A maintained command-line alternative to a public API | Package security, licence, ownership and current publication controls. npm.io, Libraries.io, jsDelivr and deps.dev pickups are separate, unverified pages, not four guaranteed links. |
| RapidAPI | A useful API marketplace entry and playground | Verify proxying, authorisation, ownership, billing and current publication terms. Do not copy a source's free-plan or auth recipe into production. |
| ClawHub | A real reviewed agent skill | Review the skill and exact publisher commands first. Do not assume no moderation, a passed security audit, or automatic aggregator links. |
| Official MCP Registry | An accurate discoverable server record | A registry/API record is not automatically an indexable HTML backlink. Reuse existing releases and receipts; verify each downstream page separately. |
| Glama | Claim and maintain an imported connector or a server page | Check for an existing imported record first. Connector claims and repository submissions are different routes; no duplicate publication. |
| Smithery | A working remote MCP integration | Verify current auth/header mapping and ownership steps. Never leak a key in a URL query or upload private credentials to obtain a link. |
| Claude connector directory | Let customers connect a real integration | The source says its community page is noindex and cites a plan price. Both need current verification. A private/noindex page can have product value, but is not an indexable backlink result. |
| Vercel connector directory | Platform-native integration discovery | Verify that the current programme accepts the exact integration. Approval timing and DR are not guarantees. |
| Zapier integration directory | Working customer automations | A personal MCP connection is not necessarily a public integration listing. Test the actual supported publishing route and current review requirements. |

All package releases, registry writes, connector publication, account creation, DNS verification,
security scopes and store fees need their own approved scope. This playbook authorises none.
A checked integration can still yield zero links, nofollow links, a noindex page or no traffic.

### 3. Other saved methods: create the useful thing first

- **Original resource boards:** Padlet and Milanote for a genuinely useful niche collection.
- **Original photography:** Flickr only with image rights and truthful relevant context.
- **Charts and maps:** Flourish and Datawrapper with properly licensed data and clear methodology.
- **Code and designs:** CodePen for a working original demo; Thingiverse for an original useful design.
- **Educational resources:** OER Commons, MERLOT and TES only with real educational fit, correct
  licences and current platform requirements. Source platform names are research leads, not
  submission approvals or proven followed links.
- **Vendor customer stories:** use a tool you genuinely use, show a truthful workflow with
  screenshots and ask whether its team wants the story. The vendor controls publication and
  linking. No fabricated testimonial, compulsory positive review or promised ranking lift.
  Use [[manual-outreach]] and [[editorial-link-intent-and-assets]]; draft outreach only.
- **Embeddable tools:** build for genuine utility. Provider credit must be optional/removable or
  appropriately qualified. Inspect the host page separately from the iframe. Never distribute
  compulsory exact-match, hidden or sitewide followed links.
- **Paid syndicated publicity:** the saved MSN-partner pitch supplied no three client placement
  URLs. Its domain-level incoming backlink count is not delivered client links. Require the
  exact publisher, live sample, audience, rights, disclosure, price and terms. Mark paid links
  appropriately (`sponsored` or `nofollow`); never buy ranking credit. Route to
  [[press-release-distribution]], not a cheap-backlink queue.
- **Directories:** reuse [[directory-submissions]] and the existing discovery records. The
  earlier paired source-intake PRs retained 201 publicly delivered records, not 11,464 verified
  sites. Do not copy those leads into a second submission queue or rerun completed submissions.

### 4. One research row to one measured outcome

Before a recommendation, record topical fit, real audience job, eligibility, current route and
cost, rights/privacy, an exact public sample, canonical/robots, redirects, and observed `href`
and `rel`. Unknown stays unknown. Keep directory, benchmark, package, integration and editorial
routes distinct; do not count a package mirror, registry JSON object or private profile as a
new referring domain without a verified public link.

Prepare one best-fit pilot and **draft-and-hold** it for exact approval. After any separately
approved action, record submitted versus live, then count actual unique linking domains,
actual index observations, referral visits, qualified signups and business outcomes separately.
A link observed is not indexing proved; indexing is not a conversion. Stop when the asset is
irrelevant, fails a platform rule, requires unsafe disclosure, becomes spam, or cannot justify
its cost without a ranking promise.

Sources: [Taras's quoted chain](https://x.com/tarasshyn/status/2113979571884429494),
[Grant O's 10 public resource ideas](https://x.com/2whazzuup/status/2112994557755523507),
[customer-story method](https://x.com/borjafat/status/2099860622955397212),
[widget claim](https://x.com/illyism/status/2097453174734963024),
[paid MSN claim](https://x.com/samigrows/status/2112151188963762644),
[Postman public workspaces](https://learning.postman.com/docs/collaborating-in-postman/using-workspaces/public-workspaces),
[Google link-spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam),
[Google outbound link qualification](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links).
