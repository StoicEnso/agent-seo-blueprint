#!/usr/bin/env python3
"""
Pull Google Search Console (GSC) performance data — clicks, impressions, CTR,
average position, and per-query / per-page breakdowns.

CREDS GATE: this stub checks for GSC_CREDS (path to a service-account JSON or an
OAuth token file). If it is ABSENT, the script does NOT attempt anything — it tells
the agent to use the BROWSER FALLBACK in references/integrations/gsc.md (read the
logged-in Search Console UI via Chrome MCP). We keep this script dependency-free on
purpose: the real API needs google-api-python-client / google-auth, which are NOT
installed and must NOT be imported here.

Usage (intent — fully wired only once creds + optional libs exist):
    python3 scripts/gsc_pull.py --site https://example.com/ --days 28
    python3 scripts/gsc_pull.py --site sc-domain:example.com --dimension query --rows 100

Consumed by playbooks: maintenance/measuring-seo-results, maintenance/navigating-google-updates,
maintenance/keyword-intent-evolution; and the monitoring + site-audit workflows.

== API PATH (documented, not implemented here — see references/integrations/gsc.md) ==
  Endpoint: POST https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
  Auth:     OAuth2 / service account with scope
            https://www.googleapis.com/auth/webmasters.readonly
            (service account must be ADDED as a user on the GSC property).
  Body:     {"startDate","endDate","dimensions":["query"|"page"|"date"],"rowLimit":...}
  Optional libs (NOT installed): google-api-python-client, google-auth.
  Output shape: see OUTPUT_SHAPE below — designed to feed scripts/report.py monitoring.

Stdlib only here (urllib, json, argparse, os, sys). No pip installs.
"""
import argparse
import datetime
import json
import os
import sys

ENV = "GSC_CREDS"

# The JSON the agent should ultimately produce (whether via API or browser fallback),
# so it plugs straight into scripts/report.py monitoring + the measuring playbook.
OUTPUT_SHAPE = {
    "site": "https://example.com/",
    "period": "2026-04-22..2026-05-20",
    "metrics": {"clicks": 0, "impressions": 0, "ctr": 0.0, "avg_position": 0.0},
    "rows": [
        {"key": "example query or /page", "clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
    ],
    "dimension": "query",
}

FALLBACK = """
No {env} found — Search Console API is not configured here.

USE THE BROWSER FALLBACK (works with a normal logged-in Google account):
  -> Follow references/integrations/gsc.md. In short, the agent (via Chrome MCP):
     1. Opens https://search.google.com/search-console (user already logged in).
     2. Selects the property, opens Performance > Search results.
     3. Sets the date range (e.g. last 28 days) and toggles all 4 metrics.
     4. Reads the Total clicks / impressions / CTR / avg position cards, then the
        Queries (or Pages) table, via get_page_text / javascript_tool.

Produce this JSON shape so it feeds scripts/report.py and the measuring playbook:
{shape}
""".strip()


def main():
    ap = argparse.ArgumentParser(
        description="Pull GSC performance data (browser fallback if no creds).")
    ap.add_argument("--site", help="Property: https URL or sc-domain:example.com")
    ap.add_argument("--days", type=int, default=28, help="Lookback window in days (default 28).")
    ap.add_argument("--dimension", choices=["query", "page", "date"], default="query")
    ap.add_argument("--rows", type=int, default=100, help="Max rows for the breakdown table.")
    ap.add_argument("--print-shape", action="store_true",
                    help="Print the target JSON output shape and exit.")
    args = ap.parse_args()

    if args.print_shape:
        print(json.dumps(OUTPUT_SHAPE, indent=2))
        return

    creds = os.environ.get(ENV)
    if not creds:
        print(FALLBACK.format(env=ENV, shape=json.dumps(OUTPUT_SHAPE, indent=2)))
        sys.exit(2)

    # Creds are present, but the Google client libs are intentionally NOT vendored here.
    end = datetime.date.today()
    start = end - datetime.timedelta(days=args.days)
    print(json.dumps({
        "status": "creds_present_libs_missing",
        "message": (
            "GSC_CREDS is set, but this dependency-free stub does not import the Google "
            "client libraries. Either install google-api-python-client + google-auth and "
            "wire the searchAnalytics.query call (see the API PATH in this file's docstring "
            "and references/integrations/gsc.md), or use the browser fallback."),
        "would_query": {
            "site": args.site,
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": [args.dimension],
            "rowLimit": args.rows,
        },
        "target_output_shape": OUTPUT_SHAPE,
    }, indent=2))
    sys.exit(3)


if __name__ == "__main__":
    main()
