# Site audit: {{DOMAIN}}

_Generated {{DATE}}_

> Fill-in template for a manual or workflow-assisted audit. The site-audit workflow can
> auto-render the **Findings table** via `scripts/report.py audit` from a findings JSON
> (columns: severity, area, issue, fix; severity ordered critical -> high -> medium -> low).
> The Scorecard, Quick wins, and Next steps sections are manual-only (not auto-rendered).
> Edit freely when writing by hand.

## Summary

{{2-4 sentence plain-language verdict: overall health of the site, the single biggest
problem holding rankings back, and what fixing the top items would unlock.}}

## Scorecard

| Area | Score (0-100) | Notes |
|---|---|---|
| Technical / crawlability | {{}} | indexing, robots, sitemap, redirects, status codes |
| Core Web Vitals / speed | {{}} | LCP, INP, CLS (from PageSpeed/Lighthouse) |
| On-page optimization | {{}} | titles, H1s, meta, headings, internal links, keyword targeting |
| Content quality & intent match | {{}} | match-and-exceed vs. SERP, thin/duplicate pages, intent fit |
| Authority / backlinks | {{}} | referring domains, link quality, gaps vs. competitors |

**Overall score:** {{}}

## Findings (prioritized)

Sorted by severity. One row per issue. Keep `severity` to: critical, high, medium, low.

| # | Severity | Area | Issue | Recommended fix |
|---|---|---|---|---|
| 1 | critical | {{area}} | {{what's wrong + evidence}} | {{specific action to fix it}} |
| 2 | high | {{}} | {{}} | {{}} |
| 3 | medium | {{}} | {{}} | {{}} |
| 4 | low | {{}} | {{}} | {{}} |

## Quick wins

Low-effort, high-impact fixes to ship first (most are pulled from the high/critical rows
above where the fix is cheap):

- [ ] {{quick win 1 — e.g. add missing title tags on the 12 service pages}}
- [ ] {{quick win 2 — e.g. fix the 5 internal links pointing to 404s}}
- [ ] {{quick win 3}}

## Next steps

Ordered plan after the quick wins — the bigger fixes and the follow-up:

1. {{step 1 — e.g. rewrite the 3 pages where intent mismatches the SERP (see match-and-exceed)}}
2. {{step 2 — e.g. build the missing comparison page for the commercial cluster}}
3. {{step 3 — e.g. re-run this audit + a monitoring snapshot in 30 days to confirm impact}}
