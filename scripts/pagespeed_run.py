#!/usr/bin/env python3
"""
Run Google PageSpeed Insights (Lighthouse) against a URL and print a compact JSON
summary of Core Web Vitals + category scores.

This is the ONE integration script that fully works with no setup: the PageSpeed
Insights API is public. An API key (env PAGESPEED_API_KEY) is OPTIONAL and only
raises your quota — without it you still get results, just at a lower rate limit.

Usage:
    python3 scripts/pagespeed_run.py https://example.com
    python3 scripts/pagespeed_run.py https://example.com --strategy desktop
    python3 scripts/pagespeed_run.py https://example.com --strategy mobile --pretty

Output (stdout, JSON) plugs into the site-audit workflow and scripts/report.py
(audit findings). Field shape is documented in references/integrations/pagespeed.md.

Stdlib only (urllib, json, argparse, os, sys). No pip installs.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# Lighthouse audit ids -> our short metric keys (the Core Web Vitals + a few extras).
METRIC_AUDITS = {
    "largest-contentful-paint": "LCP",
    "cumulative-layout-shift": "CLS",
    "first-contentful-paint": "FCP",
    "total-blocking-time": "TBT",
    "interaction-to-next-paint": "INP",
    "speed-index": "SpeedIndex",
    "server-response-time": "TTFB",
}


def build_url(target, strategy, key):
    params = {"url": target, "strategy": strategy}
    # Ask only for the categories we summarize (keeps the response smaller).
    items = list(params.items()) + [
        ("category", "performance"),
        ("category", "accessibility"),
        ("category", "best-practices"),
        ("category", "seo"),
    ]
    if key:
        items.append(("key", key))
    return API + "?" + urllib.parse.urlencode(items)


def fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": "agent-seo-blueprint/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def summarize(raw, target, strategy):
    lh = raw.get("lighthouseResult", {})
    cats = lh.get("categories", {})
    audits = lh.get("audits", {})

    scores = {}
    for cat_id, cat in cats.items():
        s = cat.get("score")
        scores[cat_id] = round(s * 100) if isinstance(s, (int, float)) else None

    metrics = {}
    for audit_id, short in METRIC_AUDITS.items():
        a = audits.get(audit_id)
        if not a:
            continue
        metrics[short] = {
            "value": a.get("numericValue"),
            "display": a.get("displayValue"),
            "score": a.get("score"),
        }

    # Field data (CrUX) when Google has real-user measurements for this origin/page.
    field = {}
    le = raw.get("loadingExperience", {}).get("metrics", {})
    for k, v in le.items():
        field[k] = {
            "percentile": v.get("percentile"),
            "category": v.get("category"),  # FAST / AVERAGE / SLOW
        }

    return {
        "url": target,
        "strategy": strategy,
        "fetched_url": raw.get("id", target),
        "lighthouse_version": lh.get("lighthouseVersion"),
        "scores": scores,                      # performance/accessibility/best-practices/seo, 0-100
        "core_web_vitals_lab": metrics,        # Lighthouse lab metrics (LCP, CLS, INP, ...)
        "field_data_crux": field or None,      # real-user CrUX data if available, else null
    }


def main():
    ap = argparse.ArgumentParser(
        description="Run PageSpeed Insights (Lighthouse) on a URL; print CWV + scores as JSON.")
    ap.add_argument("url", help="Full URL to test, e.g. https://example.com")
    ap.add_argument("--strategy", choices=["mobile", "desktop"], default="mobile",
                    help="Lighthouse environment (default: mobile).")
    ap.add_argument("--timeout", type=int, default=90, help="HTTP timeout seconds (default 90).")
    ap.add_argument("--pretty", action="store_true", help="Indent the JSON output.")
    ap.add_argument("--raw", action="store_true", help="Dump the full raw API response instead of the summary.")
    args = ap.parse_args()

    if not args.url.lower().startswith(("http://", "https://")):
        sys.exit("URL must start with http:// or https://")

    key = os.environ.get("PAGESPEED_API_KEY")  # optional
    url = build_url(args.url, args.strategy, key)

    try:
        raw = fetch(url, args.timeout)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:500]
        except Exception:
            pass
        err = {"error": "http_error", "status": e.code, "url": args.url, "detail": body}
        print(json.dumps(err, indent=2))
        # Graceful: tell the agent how to recover, then exit cleanly (0) so pipelines continue.
        sys.stderr.write(
            "\nPageSpeed API returned an error. If this is a quota/429, set PAGESPEED_API_KEY "
            "or retry later. See references/integrations/pagespeed.md.\n")
        return
    except urllib.error.URLError as e:
        print(json.dumps({"error": "network_error", "url": args.url, "detail": str(e.reason)}, indent=2))
        sys.stderr.write("\nNetwork unreachable. Check connectivity; see references/integrations/pagespeed.md.\n")
        return
    except Exception as e:  # noqa: BLE001 - never crash a pipeline on a bad response
        print(json.dumps({"error": "unexpected", "url": args.url, "detail": str(e)}, indent=2))
        return

    out = raw if args.raw else summarize(raw, args.url, args.strategy)
    print(json.dumps(out, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
