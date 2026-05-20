#!/usr/bin/env python3
"""
Thin Ahrefs API v3 client (stdlib only). Used by research/authority workflows for
keyword metrics, backlink/referring-domain counts, and competitor data.

Auth: set AHREFS_API_KEY to a v3 API token (Bearer auth). If the key is ABSENT,
this script does NOT fail silently — it prints clear instructions telling the agent
to use the browser-fallback procedure documented in
references/integrations/ahrefs.md (drive the logged-in Ahrefs web app via Chrome MCP).

Subcommands (all print JSON to stdout):
    overview   --target DOMAIN_OR_URL [--mode domain|prefix|exact]
                 -> Domain Rating, referring domains, backlinks, org traffic/keywords
    keywords   --keyword "term" [--country us]
                 -> volume, keyword difficulty (KD), CPC, global volume
    backlinks  --target DOMAIN_OR_URL [--limit 50]
                 -> recent referring domains / backlinks (for link-stealing, outreach)

Examples:
    python3 scripts/ahrefs_client.py overview --target ahrefs.com
    python3 scripts/ahrefs_client.py keywords --keyword "ai headshot generator" --country us
    python3 scripts/ahrefs_client.py backlinks --target competitor.com --limit 25

Consumed by playbooks: research/seo-metrics, research/competitor-research,
research/match-and-exceed, research/keyword-to-sitemap, authority/link-stealing,
authority/understanding-authority, authority/manual-outreach.

NOTE ON ENDPOINTS: Ahrefs API v3 paths/params evolve and depend on your subscription.
The endpoint map below reflects the v3 REST shape (base https://api.ahrefs.com/v3).
If a call 404s, the browser fallback (references/integrations/ahrefs.md) is authoritative
and always works with a normal web subscription. Stdlib only; no pip installs.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

BASE = "https://api.ahrefs.com/v3"
ENV = "AHREFS_API_KEY"

FALLBACK_MSG = (
    "No {env} found in the environment.\n\n"
    "Ahrefs has no usable API key here. Use the BROWSER FALLBACK instead:\n"
    "  -> Follow references/integrations/ahrefs.md (the agent drives the logged-in\n"
    "     Ahrefs web app with Chrome MCP tools and reads the metrics off the UI).\n\n"
    "Quick pointer for '{cmd}':\n{hint}\n"
).strip()

FALLBACK_HINTS = {
    "overview": (
        "  Open https://app.ahrefs.com/site-explorer for the target, read the\n"
        "  Overview cards: Domain Rating (DR), Referring domains, Backlinks,\n"
        "  Organic traffic, Organic keywords."),
    "keywords": (
        "  Open https://app.ahrefs.com/keywords-explorer, enter the keyword + country,\n"
        "  read Volume, Keyword Difficulty (KD), CPC, Global volume."),
    "backlinks": (
        "  In Site Explorer -> Backlinks (or Referring domains), sort by recency/DR,\n"
        "  read the linking domains and target URLs."),
}


def have_key():
    return bool(os.environ.get(ENV))


def no_key_exit(cmd):
    print(FALLBACK_MSG.format(env=ENV, cmd=cmd, hint=FALLBACK_HINTS.get(cmd, "  See the reference doc.")))
    # Exit non-zero so a wrapper can branch to the browser path, but message is the point.
    return 2


def call(path, params):
    """GET a v3 endpoint with Bearer auth; return parsed JSON."""
    key = os.environ[ENV]
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "User-Agent": "agent-seo-blueprint/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return {"ok": True, "data": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")[:600]
        except Exception:
            pass
        return {"ok": False, "status": e.code, "detail": detail,
                "hint": "If 401/403 the token is invalid; if 404 the endpoint/plan differs "
                        "-> use the browser fallback in references/integrations/ahrefs.md."}
    except urllib.error.URLError as e:
        return {"ok": False, "status": None, "detail": str(e.reason)}


def cmd_overview(args):
    # v3 site-explorer domain-rating + metrics. Params reflect the documented v3 shape.
    return call("/site-explorer/overview", {
        "target": args.target,
        "mode": args.mode,
        "output": "json",
    })


def cmd_keywords(args):
    return call("/keywords-explorer/overview", {
        "keywords": args.keyword,
        "country": args.country,
        "output": "json",
    })


def cmd_backlinks(args):
    return call("/site-explorer/backlinks", {
        "target": args.target,
        "mode": args.mode,
        "limit": args.limit,
        "order_by": "first_seen:desc",
        "output": "json",
    })


def main():
    ap = argparse.ArgumentParser(description="Ahrefs API v3 client (browser fallback if no key).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    o = sub.add_parser("overview", help="Domain/URL authority + traffic overview.")
    o.add_argument("--target", required=True)
    o.add_argument("--mode", choices=["domain", "prefix", "exact", "subdomains"], default="domain")

    k = sub.add_parser("keywords", help="Keyword volume / KD / CPC.")
    k.add_argument("--keyword", required=True)
    k.add_argument("--country", default="us")

    b = sub.add_parser("backlinks", help="Referring domains / backlinks list.")
    b.add_argument("--target", required=True)
    b.add_argument("--mode", choices=["domain", "prefix", "exact", "subdomains"], default="domain")
    b.add_argument("--limit", type=int, default=50)

    args = ap.parse_args()

    if not have_key():
        sys.exit(no_key_exit(args.cmd))

    handler = {"overview": cmd_overview, "keywords": cmd_keywords, "backlinks": cmd_backlinks}[args.cmd]
    result = handler(args)
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
