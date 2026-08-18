---
title: hosted-publishing-experiments
area: authority
source_lessons: []
tools: [serp, analytics, backlink-monitoring]
---

# Hosted publishing experiments

**What it is.** A controlled way to test a third-party publishing surface such as Telegra.ph without turning a creator claim, domain-level authority score, or easy API into a backlink promise. The output is one useful, original article for one suitable site, followed by rendered-link, index, referral, and business-outcome checks.

**When to use.**
- A platform offers public hosted pages and the user wants to know whether it can support discovery, referral traffic, citations, or links.
- A source claims “high-DA dofollow backlinks,” fast indexing, or unlimited automated pages and the claim needs live verification.
- A real guide, research note, launch explanation, or technical walkthrough would help readers even if the outbound link passes no ranking credit.

**Do not use it** to mass-produce thin pages, spin one article across many projects, create doorway pages, or manufacture links mainly to manipulate rankings.

## Evidence ledger: Telegra.ph, observed 2026-08-18

Keep creator claims separate from live facts.

| Evidence | Current observation | What it proves | What it does not prove |
|---|---|---|---|
| Source post | `https://x.com/jespernissenseo/status/2089076596531417229` claims unlimited “DA93 dofollow” links, API publishing, and indexing | A tactic worth screening | Link equity, indexing, traffic, ranking, safety, or suitability for every site |
| Official API | `https://telegra.ph/api` documents `createAccount`, `createPage`, `editPage`, `getPage`, and related methods | Submission can be automated through an official HTTP API | Permission to publish; that every submitted link remains intact or followed |
| Public rendering | The official API page returned HTTP 200, a canonical URL, and page-level `robots` content `index, follow` | That inspected page is crawl-eligible | That a new article will be crawled, indexed, retained, or ranked |
| Link qualification | Current external links on the inspected API page rendered with `rel="nofollow"` | The blanket “dofollow” claim is not supported by the inspected live page | A template-wide guarantee for every user article; verify the actual published pilot |
| Discovery files | `https://telegra.ph/robots.txt` and `/sitemap.xml` returned 404 during the check | No standard root robots/sitemap file was observed | A crawl block; page-level directives and crawler behavior still decide eligibility |

A third-party `DA` or `DR` score is a vendor metric at domain level. It does not prove that a page is indexed, that an outbound link is followed, or that ranking credit reaches the destination.

## Decision: can this be used for every site?

**No blanket rollout.** Screen every site separately. A site is eligible only when all of these are true:

1. There is a real reader job that fits a standalone hosted article.
2. The article has original evidence, examples, images, data, or a useful explanation that is not already duplicated elsewhere.
3. The destination page is the best natural next step for that reader.
4. The article can name the relationship and avoid false independence, fake endorsement, or hidden sponsorship.
5. The project can measure referral or business value even if the link is `nofollow`.

Reject a site when the only reason to publish is “get a high-DA link,” when the same copy would be reused across projects, or when no independent reader would value the page.

## Method

### 1. Define the job before the page

Choose one primary job:

- **Reader/referral test:** Can a genuinely useful article send qualified visitors?
- **Discovery test:** Can the article itself be found for a narrow query?
- **Citation test:** Will independent writers or answer systems discover and cite the evidence?
- **Link-observation test:** How does the platform render and qualify a natural outbound link?

Do not use ranking improvement as the sole primary metric. One third-party page cannot isolate ranking causality.

### 2. Complete the site-fit row

Copy `assets/hosted-publishing-experiment.csv` into the project workspace and add one row per site. Record:

- project and destination URL;
- unique reader job and article thesis;
- original evidence or asset;
- why the destination link helps the reader;
- duplicate/thin-content review;
- relationship disclosure;
- approval state;
- expected public URL and verification dates;
- actual canonical, robots directive, rendered `href`, rendered `rel`, and HTTP status;
- index observations, referral sessions, assisted conversions, and verdict.

`eligible` means “worth drafting,” not “safe to publish automatically.”

### 3. Draft one pilot, not an unlimited batch

Draft one article for the best-fit site first. Requirements:

- unique title, thesis, examples, and evidence;
- enough standalone value to remain useful if every outbound link is removed;
- one or a small number of natural destination links;
- brand or URL anchors by default, not repeated exact-match money keywords;
- no fake author identity, fake quote, fabricated result, or copied customer story;
- no spun variants, cross-site duplicate copy, or templated city/keyword doors;
- explicit disclosure when the author, product, or destination is connected to the article.

A successful pilot does not authorize cloning it for every site.

### 4. Prepare the API request but hold the write

Telegra.ph supports API-based account and page operations. A draft implementation may prepare:

1. `createAccount` with a truthful `short_name` and optional author data;
2. `createPage` with a unique title and Telegraph Node JSON content;
3. `editPage` for approved corrections;
4. `getPage` for read-only API verification.

Treat the access token as a secret. Never place it in source control, logs, screenshots, analytics URLs, or article content. Account creation, page creation, edits, and deletion are external writes. Obtain explicit approval for the exact account, article, links, disclosure, and destination before calling a write method.

### 5. Verify the rendered public page

After an approved publication, inspect the public result rather than trusting the request payload. Capture:

1. HTTP status and final URL;
2. canonical URL;
3. page-level robots directive;
4. rendered destination `href`;
5. rendered `rel` tokens such as `nofollow`, `ugc`, or `sponsored`;
6. whether the link is visible without login and works;
7. whether the article or link was edited, stripped, redirected, or removed;
8. a dated HTML or screenshot receipt.

If the actual destination link is `nofollow`, record it as `nofollow`. Do not rename it “dofollow” because the domain has a high third-party score.

### 6. Measure crawl, discovery, and business outcomes separately

Check on a pre-set schedule such as day 0, 7, 14, and 30:

- exact public URL discovery in more than one search surface when possible;
- cache/search snippets only as supplemental evidence;
- backlink discovery in available first-party or third-party tools;
- UTM-tagged referral sessions;
- engaged visits, sign-ups, assisted conversions, or other project outcome;
- article survival and unchanged link behavior.

A `site:` query is not a complete index ledger. An indexed article is not proof of transferred authority. A new backlink coinciding with a ranking change is not causal proof.

### 7. Decide before expanding

Use one of four verdicts:

- `ADOPT_FOR_REFERRAL_OR_CONTENT` — useful readers or business outcomes justify selective use.
- `REVISE_AND_RETEST` — the page is useful but the topic, destination, or distribution needs one bounded retry.
- `REJECT_FOR_LINK_EQUITY` — the rendered link is qualified/stripped, or there is no evidence supporting the dofollow premise.
- `INCONCLUSIVE` — the page is crawl-eligible but evidence is too weak or the observation window is incomplete.

Expansion means another unique, justified article after review. It never means an unlimited API loop.

## Decision criteria / heuristics

- **API availability is an execution fact, not an SEO result.**
- **`index, follow` is eligibility, not guaranteed indexation.**
- **A domain metric is not page-level link evidence.**
- **A `nofollow` link can still support referral or discovery goals, but not a dofollow claim.**
- **One good site-specific article beats a duplicated cross-site batch.**
- **Publishing for all sites requires a completed fit row and separate approval for every article.**

## Stop conditions

Stop or reject the rollout when any of these occurs:

- the content plan becomes spun, duplicated, thin, or doorway-like;
- exact-match anchors or page volume become the main strategy;
- the rendered link is stripped or qualified and the only goal was followed-link equity;
- the page is `noindex`, private, broken, or repeatedly removed;
- the platform terms or moderation state are unclear;
- there is no reader value beyond the backlink;
- the pilot produces no useful referral, citation, or business signal within the registered window;
- the user has not approved the exact external write.

## Example

A design software company has original before/after research and a public methodology page. It drafts one Telegra.ph article explaining the evaluation method, discloses the company connection, links once to the methodology for reproducibility, and adds UTM parameters. After approval it publishes, records the rendered `rel`, checks discovery on days 7/14/30, and measures engaged referrals. It does not clone the article for unrelated sites and does not call the link followed unless the live HTML proves it.

## Pitfalls

- Treating “unlimited pages” as a growth strategy rather than a spam warning.
- Reporting `DA93` as ranking value.
- Confusing crawl eligibility with indexation.
- Checking only the API response instead of rendered HTML.
- Creating an account or page before the content owner approves the exact write.
- Losing the edit token or exposing it in a repository.
- Publishing the same article for every owned site.
- Declaring success from one indexed URL without referral or business evidence.

**Related.** [[directory-submissions]] (destination verification), [[press-release-distribution]] (hosted distribution and link qualification), [[editorial-link-intent-and-assets]] (reader-first reasons to link), [[linkbuilding-what-not-to-do]] (scaled manipulation guardrails), [[measuring-seo-results]] (outcome separation). Official API: `https://telegra.ph/api`. Google spam policy: `https://developers.google.com/search/docs/essentials/spam-policies`.
