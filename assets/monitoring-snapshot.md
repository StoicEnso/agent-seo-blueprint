# Monitoring snapshot — {{SITE}}

_Generated {{DATE}}  period: {{PERIOD}}_

> Point-in-time read on whether the SEO work is paying off. The monitoring workflow can
> auto-render this via `scripts/report.py monitoring` from a snapshot JSON — the Metrics
> and Tracked-keywords tables below mirror that output exactly. Compare against the prior
> snapshot in the workspace to see the trend, not just the level.

## Metrics

Top-line numbers for the period (from Google Search Console / GA4).

| Metric | Value |
|---|---|
| clicks | {{}} |
| impressions | {{}} |
| avg_position | {{}} |
| ctr | {{}} |
| {{add rows as needed — sessions, conversions, etc.}} | {{}} |

## Tracked keywords

Movement on the keywords we're targeting. `Change` = position delta vs. last snapshot
(use `+N` for improvement / climbing, `-N` for a drop; "new" if first seen).

| Keyword | Position | Change |
|---|---|---|
| {{keyword}} | {{}} | {{+N / -N / new}} |
| {{keyword}} | {{}} | {{}} |
| {{keyword}} | {{}} | {{}} |

## Notes

{{Interpretation: what moved and why. Flag any Google-update timing, sudden volatility,
intent shifts, or wins/losses worth acting on. Note what to do before the next snapshot —
e.g. "intent on X is shifting commercial; refresh the page format." Recommend the next
check-in cadence.}}
