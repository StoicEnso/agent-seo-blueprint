# Telegra.ph hosted-publishing intake — 2026-08-18

## Intake

- Source: `https://x.com/jespernissenseo/status/2089076596531417229`
- Source claim: Telegra.ph provides unlimited high-authority dofollow backlinks, has an API, and indexes pages.
- Requested use: assess suitability across owned sites and add the verified tactic to Agent SEO Blueprint.

## Live evidence checked

| Check | Result |
|---|---|
| Official API | `https://telegra.ph/api` documents account creation plus page create/edit/read methods. API submission is technically possible. |
| Public page response | The inspected official API page returned HTTP 200. |
| Canonical | A canonical URL was present on the inspected page. |
| Page robots | The inspected page exposed `index, follow`. This is crawl eligibility, not proof of indexation. |
| External-link attribute | Current external links on the inspected API page rendered with `rel="nofollow"`. |
| Root robots file | `https://telegra.ph/robots.txt` returned 404 during this check. |
| Root sitemap file | `https://telegra.ph/sitemap.xml` returned 404 during this check. |
| Search check | Public search results were inconsistent and did not provide a reliable index census. |
| Publication test | Not run. No account or article was created because that is an external write. |

## Verdict

- **API submission:** possible.
- **Dofollow claim:** not supported by the inspected current live evidence.
- **Indexing claim:** unverified for a new page. `index, follow` allows crawling but does not guarantee inclusion.
- **All-site rollout:** rejected as a blanket tactic. Each site needs a unique reader job, original evidence, a natural destination, disclosure, and a measurable goal that survives a `nofollow` outcome.
- **Safe next test:** one approved, original article for the strongest-fit site. Verify the actual rendered page and link before considering another site.

## Safeguards added

- New hosted-publishing playbook separates API capability, crawl eligibility, rendered link attributes, index observations, and business outcomes.
- New experiment ledger records one row per site and requires separate fit and approval states.
- Telegra.ph is recorded as a candidate with the source's `DA93`/dofollow wording preserved only as an unverified claim.
- Regression tests prevent the repository from relabelling it as a verified dofollow source or promising indexation, ranking value, or an unlimited rollout.

## Policy basis

- Google Search spam policies: `https://developers.google.com/search/docs/essentials/spam-policies`
- Easy API access does not authorize scaled thin content, doorway pages, duplicate articles, or link manipulation.
