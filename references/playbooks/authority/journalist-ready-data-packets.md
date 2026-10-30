---
title: Journalist-ready data packets
area: authority
source_posts: ["https://x.com/illyism/status/2116094451315855827"]
---

# Journalist-ready data packets

## Scope and source status

Use this branch when a recent, relevant article suggests a follow-up that your evidence can answer. This is **earned editorial research**, not paid press-release distribution. Extend [[statistics-page-link-earning]] rather than making another thin statistics page. The statistics playbook owns search fit, stable yearless URLs, dates, methodology and schema; this branch owns the reporter fit and finished evidence packet.

ILIAS ISM's 30 October 2026 post proposes: find a relevant journalist; use an article plus your site to suggest database questions; run a query; make a branded chart; publish the raw data; and send the chart, CSV and suggested quote in the first email. The screenshot gives a similar topic-ideation prompt. The claimed DR 4 national-news placement, DR 80+ links and AI Overview citations are **unverified anecdotes, not promised outcomes**. No named placement or causal test accompanies the saved source. A domain score does not prove editorial value, a followed link or an AI citation.

## Procedure

1. **Verify editorial fit.** Save the article URL, title, publication date, byline, desk, exact paragraph and the new question. Check the author's public professional contact route. An anonymous vendor blog is a topic lead, not a verified journalist target. Reject unrelated, stale or already-answered angles; do not scrape personal contact data or mass-email a list.
2. **Write a narrow data contract.** State population, period, geography, unit, inclusion/exclusion rules, owner and limitations before the query. An LLM may propose a question or read-only SQL, but cannot invent rows or establish permission. Review SQL for bounded SELECT-only effects, joins, duplicate counts and costs; use an approved read-only account and scoped export. Do not give a third-party model customer rows, credentials, private URLs or confidential schema. Obtain the data owner's consent where required.
3. **Minimise and review.** Use aggregate, rights-cleared data only. Check consent, contracts, retention, identifiers and small-cell/re-identification risk. Suppress or combine unsafe cells under the data owner's policy. Keep the raw private export outside the public packet. Public-source reanalysis is a valid fallback, but label it **public-source reanalysis**, never proprietary database research. Save source versions and exact table/cell locators.
4. **Verify before prose.** Independently reconcile raw totals, denominator, missing values and comparable definitions. Compute changes from unrounded values. Counts are not prevalence or individual risk. Repeated events are not unique businesses; overlapping actions must not be added as independent cases. Report zero-base percentage change as undefined. Explain any annual reporting discontinuity. A CSV parser passing does not verify the source or statistical fitness.
5. **Build the finished packet.** Supply an accessible, numerical chart, downloadable aggregate CSV, concise findings, full method/source ledger, suggested quote marked DRAFT and attribution, and correction contact. Do not use image generation to draw numerical marks: it can alter labels or values. Use deterministic SVG/plotting; branding must not hide source or imply publisher endorsement. The tool below creates an offline starter, not a send-approved package.
6. **Draft the statistics page and first email.** Use the existing canonical statistics page when appropriate. Put the new supported fact, why it follows the recipient's article, CSV/chart references, source/method URL, caveat and draft quote in the first message. Do not offer to prepare evidence later. Check the actual newsroom attachment rules: prefer small, safe attachments or public download links as the recipient requires. Never fabricate a spokesperson, quote approval, exclusive claim or publication URL. No tracking pixels or undisclosed sponsorship.
7. **Hold external actions separately.** Publication, third-party model upload and outreach each need their applicable approval. Repository PR approval is not production publishing or permission to email a journalist. Verify a live accessible evidence URL before a send-ready pitch. No new accounts, paid tools, subscriptions, schedules or autonomous follow-up sequence are implied.
8. **Measure separate outcomes.** Record packet review, publication, send receipt, reply, actual editorial mention, rendered destination href/rel, referral visits, qualified leads and assisted conversions separately. Check AI citations by named platform, query, surface and time; a news link is not an AI citation. Observe at 7 and 30 days only through an approved monitoring lane; do not create a schedule. Keep no response/inconclusive distinct from failure. Stop after the approved single-pilot batch; expand only on real editorial/business value.

## Offline starter

Copy `assets/journalist-data-brief.csv` for editorial and approval evidence. Prepare a CSV with the fields in `examples/journalist-data-public.csv`, then run:

```bash
python3 scripts/journalist_data_packet.py --input examples/journalist-data-public.csv --output /path/to/new-packet --brand 'Research draft'
```

The script uses only the Python standard library. It reads a local aggregate CSV, writes a new directory and makes no network calls, SQL calls, model calls, publication or sends. It refuses existing output directories and invalid/duplicate observations. It cannot detect undisclosed private data: the human/data-owner privacy and reuse reviews remain mandatory. Its SVG and page are explicitly DRAFT; its source URLs and denominators still need review.

The included real public example reproduces Traffic Commissioner Table 6 inquiry counts for 2024-25 and 2025-26, including the Great Britain total. It is not a customer database, a compliance-risk league table or proof of unique/newsworthy insight. Exclude the national total from regional summation. Read `examples/journalist-data-public.md` before interpreting it.

**Done when:** a reviewer can trace each fact to a permitted source and reproduce it; a relevant reporter and genuinely additive angle are verified; the chart, CSV, method, page and draft quote exist; publication/outreach are separately authorised or clearly held. A built packet alone is not an acquired backlink, completed outreach or business result.
