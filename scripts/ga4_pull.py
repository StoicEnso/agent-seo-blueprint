#!/usr/bin/env python3
"""
Pull Google Analytics 4 (GA4) data — organic sessions, engagement, conversions —
for the "did the SEO work pay off" measurement and update-impact analysis.

CREDS GATE: this stub checks for GA4_CREDS (path to a service-account JSON or OAuth
token). If ABSENT, it tells the agent to use the BROWSER FALLBACK in
references/integrations/ga4.md (read the logged-in GA4 UI / Explore via Chrome MCP).
Dependency-free on purpose: the real GA4 Data API needs google-analytics-data /
google-auth, which are NOT installed and must NOT be imported here.

Usage (intent — fully wired only once creds + optional libs exist):
    python3 scripts/ga4_pull.py --property 123456789 --days 28
    python3 scripts/ga4_pull.py --property 123456789 --channel "Organic Search" --days 90

Consumed by playbooks: maintenance/measuring-seo-results, maintenance/navigating-google-updates;
and the monitoring + site-audit workflows.

== API PATH (documented, not implemented here — see references/integrations/ga4.md) ==
  Endpoint: POST https://analyticsdata.googleapis.com/v1beta/properties/{propertyId}:runReport
  Auth:     OAuth2 / service account with scope
            https://www.googleapis.com/auth/analytics.readonly
            (service account email must be GRANTED Viewer on the GA4 property).
  Body:     {"dateRanges":[{startDate,endDate}],
             "dimensions":[{"name":"sessionDefaultChannelGroup"}],
             "metrics":[{"name":"sessions"},{"name":"engagedSessions"},
                        {"name":"conversions"},{"name":"engagementRate"}],
             "dimensionFilter": <filter to Organic Search>}
  Optional libs (NOT installed): google-analytics-data, google-auth.
  Output shape: see OUTPUT_SHAPE below.

Stdlib only here (urllib, json, argparse, os, sys). No pip installs.
"""
import argparse
import datetime
import json
import os
import sys

ENV = "GA4_CREDS"

OUTPUT_SHAPE = {
    "property_id": "123456789",
    "period": "2026-04-22..2026-05-20",
    "channel": "Organic Search",
    "metrics": {
        "sessions": 0,
        "engaged_sessions": 0,
        "engagement_rate": 0.0,
        "conversions": 0,
        "avg_engagement_time_sec": 0.0,
    },
    "top_landing_pages": [
        {"page": "/example", "sessions": 0, "conversions": 0}
    ],
}

FALLBACK = """
No {env} found — GA4 Data API is not configured here.

USE THE BROWSER FALLBACK (works with a normal logged-in Google account):
  -> Follow references/integrations/ga4.md. In short, the agent (via Chrome MCP):
     1. Opens https://analytics.google.com (user already logged in) and selects the property.
     2. Reports > Acquisition > Traffic acquisition; set the date range.
     3. Filters / reads the "Organic Search" row: Sessions, Engaged sessions,
        Engagement rate, Conversions, via get_page_text / javascript_tool.
     4. For landing-page detail, use Engagement > Landing page (or an Explore report).

Produce this JSON shape so it feeds the measuring + monitoring playbooks:
{shape}
""".strip()


def main():
    ap = argparse.ArgumentParser(
        description="Pull GA4 organic metrics (browser fallback if no creds).")
    ap.add_argument("--property", help="GA4 numeric property id, e.g. 123456789")
    ap.add_argument("--days", type=int, default=28, help="Lookback window in days (default 28).")
    ap.add_argument("--channel", default="Organic Search",
                    help="Default channel group to isolate (default: Organic Search).")
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

    end = datetime.date.today()
    start = end - datetime.timedelta(days=args.days)
    print(json.dumps({
        "status": "creds_present_libs_missing",
        "message": (
            "GA4_CREDS is set, but this dependency-free stub does not import the Google "
            "client libraries. Either install google-analytics-data + google-auth and wire "
            "the runReport call (see the API PATH in this file's docstring and "
            "references/integrations/ga4.md), or use the browser fallback."),
        "would_query": {
            "property": args.property,
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "channel": args.channel,
        },
        "target_output_shape": OUTPUT_SHAPE,
    }, indent=2))
    sys.exit(3)


if __name__ == "__main__":
    main()
