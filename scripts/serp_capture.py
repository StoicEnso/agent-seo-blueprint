#!/usr/bin/env python3
"""
SERP capture helper — NOT an API client.

A live Google SERP must be read by the AGENT itself with Chrome MCP tools
(navigate -> get_page_text / javascript_tool), because results are personalized,
JS-rendered, and bot-protected. There is no compliant programmatic endpoint, so this
script does NOT fetch anything. It validates the query, builds the exact Google URL to
open, and prints the step-by-step browser-capture procedure plus the JSON output shape.

Usage:
    python3 scripts/serp_capture.py "ai headshot generator"
    python3 scripts/serp_capture.py "best crm for startups" --country uk --top 5
    python3 scripts/serp_capture.py "vpn for gaming" --json   # machine-readable plan

Consumed by playbooks: research/match-and-exceed, research/search-intent,
content/content-types-overview, content/on-page-optimization, research/finding-and-validating-niches.

ToS / ethics (enforced by procedure, see references/integrations/serp.md):
  - Personal-research volume only. A handful of queries per session, not bulk scraping.
  - Respect bot detection. NEVER solve or bypass a CAPTCHA — stop and tell the user.
  - Read what's on screen; do not hammer pagination or automate at scale.

Stdlib only (urllib, json, argparse, os, sys). No pip installs. No network calls.
"""
import argparse
import json
import sys
import urllib.parse

# gl = country (geo), hl = interface language. Personal research, single country at a time.
COUNTRY_DEFAULTS = {
    "us": ("us", "en"), "uk": ("uk", "en"), "gb": ("gb", "en"),
    "ca": ("ca", "en"), "au": ("au", "en"), "de": ("de", "de"),
    "fr": ("fr", "fr"), "es": ("es", "es"), "nl": ("nl", "nl"),
    "in": ("in", "en"), "br": ("br", "pt"),
}

OUTPUT_SHAPE = {
    "query": "ai headshot generator",
    "country": "us",
    "captured_at": "2026-05-20",
    "dominant_content_type": "free tool | comparison | listicle | gallery | article | product",
    "results": [
        {
            "rank": 1,
            "title": "",
            "url": "",
            "domain": "",
            "type": "tool|article|comparison|gallery|product|forum",
            "notes": "what makes it rank; thin/strong; format cues",
        }
    ],
    "serp_features": ["featured_snippet", "people_also_ask", "image_pack", "video", "ads", "shopping"],
    "intent_read": "informational | commercial | transactional | navigational",
    "exceedable": "yes|no|maybe — why",
}


def build_serp_url(query, country, top):
    gl, hl = COUNTRY_DEFAULTS.get(country.lower(), (country.lower(), "en"))
    params = {"q": query, "gl": gl, "hl": hl, "num": max(10, top), "pws": 0}
    return "https://www.google.com/search?" + urllib.parse.urlencode(params)


def procedure(url, query, country, top):
    return f"""
SERP CAPTURE PLAN (agent runs this with Chrome MCP — do NOT use Python to fetch)

Query    : {query!r}
Country  : {country}
Capture  : top {top} organic results
Open URL : {url}

Steps:
  1. mcp__claude-in-chrome__navigate -> {url}
     (User must already be signed in / on a normal Google session. Do NOT log in for them.)
  2. If a CAPTCHA / "unusual traffic" / consent wall appears: STOP. Do not solve it.
     Tell the user to complete it manually, then resume. Never bypass bot detection.
  3. mcp__claude-in-chrome__get_page_text  (or read_page) to grab the rendered results.
  4. Extract, for the top {top} ORGANIC results (skip ads, label them separately):
       rank, title, url, domain, and your read of the content TYPE.
  5. Note SERP features present: featured snippet, People Also Ask, image/video pack,
     shopping, ads. These signal intent and the format Google rewards.
  6. Judge the dominant content type in the top 3 (the "appetite") and whether you can
     exceed it -> feeds research/match-and-exceed and research/search-intent.

Keep it to a few queries per session (personal research). See references/integrations/serp.md.

Emit this JSON (feeds the playbooks + scripts/report.py keyword/research notes):
{json.dumps(OUTPUT_SHAPE, indent=2)}
""".strip()


def main():
    ap = argparse.ArgumentParser(
        description="Plan a live SERP capture (browser-only via Chrome MCP; prints the procedure).")
    ap.add_argument("query", help="The search query to inspect, e.g. 'ai headshot generator'")
    ap.add_argument("--country", default="us", help="2-letter country for geo (default us).")
    ap.add_argument("--top", type=int, default=10, help="How many organic results to capture (default 10).")
    ap.add_argument("--json", action="store_true", help="Print the plan as JSON instead of text.")
    args = ap.parse_args()

    q = args.query.strip()
    if not q:
        sys.exit("Query is empty. Provide a search term, e.g. serp_capture.py \"best crm\"")
    if len(q) > 300:
        sys.exit("Query is unreasonably long (>300 chars). SERP capture is for real search terms.")
    if args.top < 1 or args.top > 50:
        sys.exit("--top must be between 1 and 50 (personal-research volume).")

    url = build_serp_url(q, args.country, args.top)

    if args.json:
        print(json.dumps({
            "mode": "browser-only",
            "engine": "google",
            "query": q,
            "country": args.country,
            "top": args.top,
            "open_url": url,
            "tool_chain": ["mcp__claude-in-chrome__navigate",
                           "mcp__claude-in-chrome__get_page_text"],
            "tos_notes": [
                "personal-research volume only",
                "respect bot detection; never bypass CAPTCHAs",
                "user must already be logged in; skill never enters passwords",
            ],
            "output_shape": OUTPUT_SHAPE,
            "reference": "references/integrations/serp.md",
        }, indent=2))
        return

    print(procedure(url, q, args.country, args.top))


if __name__ == "__main__":
    main()
