#!/usr/bin/env python3
"""
Thin DataForSEO API v3 client (stdlib only). Starting point helper for the
agent-seo-blueprint skill when we want cheap, agent-friendly SEO data at scale.

Auth: set DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD (or DATAFORSEO_API_LOGIN +
DATAFORSEO_API_PASSWORD). Credentials come from https://app.dataforseo.com/api-access
and are never stored in project.json.

Subcommands (all print JSON):
    estimate          rough public-price estimate; no credentials required
    user-data         account/balance metadata
    locations         list locations for SERP or Google Ads keyword endpoints
    keyword-volume    Google Ads search-volume tasks (live or standard)
    keyword-volume-get / keyword-volume-ready
    keyword-ideas     DataForSEO Labs Google keyword ideas (live)
    serp              Google Organic SERP task (live or standard)
    serp-get / serp-ready
    backlinks         Backlinks API live rows
    raw               escape hatch: arbitrary GET/POST path

Examples:
    python3 scripts/dataforseo_client.py estimate keyword-volume --count 2500 --mode standard
    python3 scripts/dataforseo_client.py keyword-volume --keyword "ai headshot generator" --location-code 2840 --live
    python3 scripts/dataforseo_client.py keyword-ideas --keyword "ai headshot" --location-code 2840 --limit 50
    python3 scripts/dataforseo_client.py serp --keyword "ai headshot generator" --location-code 2840 --depth 10 --live
    python3 scripts/dataforseo_client.py backlinks --target competitor.com --dofollow --limit 25

Design notes:
- Defaults are conservative: US/en where a location is needed, small limits, and
  normalized output by default when a known response shape is returned.
- Use --dry-run on paid commands to inspect endpoint/payload/estimated cost
  without credentials or spend.
- Standard queued endpoints POST a task and return the task id; use the matching
  *_get or *_ready commands later. Do not busy-wait/poll in this helper.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

BASE = "https://api.dataforseo.com"
LOGIN_ENVS = ("DATAFORSEO_LOGIN", "DATAFORSEO_API_LOGIN")
PASSWORD_ENVS = ("DATAFORSEO_PASSWORD", "DATAFORSEO_API_PASSWORD")
USER_AGENT = "agent-seo-blueprint-dataforseo/0.1"


def load_private_env() -> None:
    """Load optional local SEO credentials without printing or committing secrets."""
    paths: List[Path] = []
    if os.environ.get("SEO_API_ENV"):
        paths.append(Path(os.environ["SEO_API_ENV"]).expanduser())
    paths.extend([
        Path.home() / ".secrets" / "seo-api.env",
        Path("/root/.secrets/seo-api.env"),
    ])
    seen = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        try:
            lines = path.read_text().splitlines()
        except OSError:
            continue
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("export ").strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
        return


load_private_env()

# Public pricing snapshot documented in references/integrations/dataforseo.md.
SERP_BASE = {"standard": 0.0006, "priority": 0.0012, "live": 0.002}
KEYWORD_VOLUME_TASK = {"standard": 0.05, "live": 0.075}
LABS_TASK = 0.01
LABS_ITEM = 0.0001
BACKLINKS_REQUEST = 0.02
BACKLINKS_ROW = 0.00003


def env_first(names: Iterable[str]) -> Optional[str]:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def have_auth() -> bool:
    return bool(env_first(LOGIN_ENVS) and env_first(PASSWORD_ENVS))


def auth_header() -> str:
    login = env_first(LOGIN_ENVS)
    password = env_first(PASSWORD_ENVS)
    if not login or not password:
        raise RuntimeError(
            "No DataForSEO credentials found. Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD "
            "(or DATAFORSEO_API_LOGIN / DATAFORSEO_API_PASSWORD). Use --dry-run or estimate "
            "to inspect paid calls without credentials."
        )
    token = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def request(method: str, path: str, payload: Any = None, timeout: int = 90) -> Dict[str, Any]:
    if not path.startswith("/"):
        path = "/" + path
    url = BASE + path
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    try:
        authorization = auth_header()
    except RuntimeError as e:
        return {"ok": False, "http_status": None, "detail": str(e)}
    req = urllib.request.Request(
        url,
        data=data,
        method=method.upper(),
        headers={
            "Authorization": authorization,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace")
            return {"ok": True, "http_status": resp.status, "data": json.loads(body)}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:2000]
        return {"ok": False, "http_status": e.code, "detail": detail}
    except urllib.error.URLError as e:
        return {"ok": False, "http_status": None, "detail": str(e.reason)}


def dataforseo_ok(resp: Dict[str, Any]) -> bool:
    if not resp.get("ok"):
        return False
    data = resp.get("data") or {}
    if data.get("status_code") and data.get("status_code") != 20000:
        return False
    if data.get("tasks_error", 0):
        return False
    return True


def emit(obj: Any, raw: bool = False) -> int:
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    if isinstance(obj, dict) and not obj.get("ok", True):
        return 1
    return 0


def parse_json_arg(value: Optional[str], default: Any = None) -> Any:
    if value is None or value == "":
        return default
    if value.startswith("@"):
        return json.loads(Path(value[1:]).expanduser().read_text(encoding="utf-8"))
    return json.loads(value)


def collect_keywords(args: argparse.Namespace) -> List[str]:
    out: List[str] = []
    for value in getattr(args, "keyword", []) or []:
        out.append(value)
    if getattr(args, "keywords", None):
        # Accept comma, newline, or pipe separated quick lists.
        text = args.keywords.replace("|", "\n").replace(",", "\n")
        out.extend(x.strip() for x in text.splitlines() if x.strip())
    if getattr(args, "file", None):
        text = Path(args.file).expanduser().read_text(encoding="utf-8")
        out.extend(x.strip() for x in text.splitlines() if x.strip() and not x.lstrip().startswith("#"))
    seen = set()
    unique = []
    for kw in out:
        k = " ".join(kw.split())
        if k and k.lower() not in seen:
            unique.append(k)
            seen.add(k.lower())
    return unique


def add_locale(task: Dict[str, Any], args: argparse.Namespace) -> None:
    for field in ("location_code", "location_name", "location_coordinate", "language_code", "language_name"):
        value = getattr(args, field, None)
        if value not in (None, ""):
            task[field] = value


def maybe_add(task: Dict[str, Any], key: str, value: Any) -> None:
    if value not in (None, ""):
        task[key] = value


def estimate_serp_cost(depth: int, mode: str) -> float:
    pages = max(1, math.ceil(max(depth, 1) / 10))
    base = SERP_BASE[mode]
    if pages == 1:
        return base
    return base + (pages - 1) * base * 0.75


def normalize_keyword_volume(api: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for task in api.get("tasks", []) or []:
        for item in task.get("result") or []:
            rows.append({
                "keyword": item.get("keyword"),
                "volume": item.get("search_volume"),
                "kd": None,
                "cpc": item.get("cpc"),
                "competition": item.get("competition"),
                "competition_index": item.get("competition_index"),
                "low_top_of_page_bid": item.get("low_top_of_page_bid"),
                "high_top_of_page_bid": item.get("high_top_of_page_bid"),
                "monthly_searches": item.get("monthly_searches"),
                "location_code": item.get("location_code"),
                "language_code": item.get("language_code"),
                "intent": None,
                "target_url": "",
                "priority": "",
                "cluster": "",
                "notes": "DataForSEO Google Ads search volume; KD requires Labs or Ahrefs.",
            })
    return {"ok": True, "source": "dataforseo", "kind": "keyword_volume", "cost": api.get("cost"), "rows": rows, "raw_status": api.get("status_message")}


def normalize_keyword_ideas(api: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for task in api.get("tasks", []) or []:
        for result in task.get("result") or []:
            for item in result.get("items") or []:
                info = item.get("keyword_info") or {}
                props = item.get("keyword_properties") or {}
                intent = item.get("search_intent_info") or {}
                serp = item.get("serp_info") or {}
                avg_links = item.get("avg_backlinks_info") or {}
                rows.append({
                    "keyword": item.get("keyword"),
                    "volume": info.get("search_volume"),
                    "kd": props.get("keyword_difficulty"),
                    "cpc": info.get("cpc"),
                    "competition": info.get("competition_level"),
                    "competition_index": info.get("competition"),
                    "intent": intent.get("main_intent"),
                    "serp_features": serp.get("serp_item_types"),
                    "avg_referring_domains_top_serp": avg_links.get("referring_domains"),
                    "avg_backlinks_top_serp": avg_links.get("backlinks"),
                    "monthly_searches": info.get("monthly_searches"),
                    "location_code": item.get("location_code"),
                    "language_code": item.get("language_code"),
                    "target_url": "",
                    "priority": "",
                    "cluster": "",
                    "notes": "DataForSEO Labs keyword ideas.",
                })
    return {"ok": True, "source": "dataforseo", "kind": "keyword_ideas", "cost": api.get("cost"), "rows": rows, "raw_status": api.get("status_message")}


def normalize_serp(api: Dict[str, Any], top: int = 10) -> Dict[str, Any]:
    packs = []
    for task in api.get("tasks", []) or []:
        for result in task.get("result") or []:
            items = result.get("items") or []
            organic = []
            for item in items:
                if item.get("type") == "organic":
                    organic.append({
                        "rank": item.get("rank_group") or item.get("rank_absolute"),
                        "rank_absolute": item.get("rank_absolute"),
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "domain": item.get("domain"),
                        "type": "organic",
                        "description": item.get("description"),
                        "is_featured_snippet": item.get("is_featured_snippet"),
                        "notes": "",
                    })
                    if len(organic) >= top:
                        break
            item_types = result.get("item_types") or []
            packs.append({
                "query": result.get("keyword") or (task.get("data") or {}).get("keyword"),
                "country": result.get("location_code"),
                "language": result.get("language_code"),
                "captured_at": result.get("datetime"),
                "dominant_content_type": "unknown",
                "results": organic,
                "serp_features": [x for x in item_types if x not in ("organic",)],
                "intent_read": "",
                "exceedable": "needs human/course review",
                "check_url": result.get("check_url"),
            })
    return {"ok": True, "source": "dataforseo", "kind": "serp", "cost": api.get("cost"), "serps": packs, "raw_status": api.get("status_message")}


def normalize_backlinks(api: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for task in api.get("tasks", []) or []:
        for result in task.get("result") or []:
            for item in result.get("items") or []:
                rows.append({
                    "source_domain": item.get("domain_from"),
                    "source_url": item.get("url_from"),
                    "source_rank": item.get("domain_from_rank"),
                    "source_page_rank": item.get("page_from_rank"),
                    "anchor": item.get("anchor") or item.get("alt"),
                    "target_url": item.get("url_to"),
                    "first_seen": item.get("first_seen"),
                    "last_seen": item.get("last_seen"),
                    "dofollow": item.get("dofollow"),
                    "external_links": item.get("page_from_external_links"),
                    "spam_score": item.get("backlink_spam_score"),
                    "source_dr": None,
                    "notes": "DataForSEO rank is not Ahrefs DR; treat source_rank as a separate 0-1000 authority signal.",
                })
    return {"ok": True, "source": "dataforseo", "kind": "backlinks", "cost": api.get("cost"), "rows": rows, "raw_status": api.get("status_message")}


def print_dry_run(kind: str, endpoint: str, payload: Any, estimate: Optional[float] = None, notes: Optional[List[str]] = None) -> int:
    return emit({
        "ok": True,
        "dry_run": True,
        "kind": kind,
        "endpoint": BASE + endpoint,
        "payload": payload,
        "estimated_cost_usd": estimate,
        "notes": notes or [],
    })


def cmd_estimate(args: argparse.Namespace) -> int:
    if args.estimate_kind == "keyword-volume":
        tasks = max(1, math.ceil(args.count / 1000))
        cost = tasks * KEYWORD_VOLUME_TASK[args.mode]
        notes = ["Google Ads search volume bills per task; each task can contain up to 1,000 keywords."]
    elif args.estimate_kind == "serp":
        cost = args.queries * estimate_serp_cost(args.depth, args.mode)
        notes = ["SERP price is per 10-result page; first page full base, subsequent pages 75% base."]
    elif args.estimate_kind == "keyword-ideas":
        cost = args.requests * (LABS_TASK + args.limit * LABS_ITEM)
        notes = ["Approximation for DataForSEO Labs all-other endpoint pricing: $0.01/task + $0.0001/item."]
    elif args.estimate_kind == "backlinks":
        requests = max(1, math.ceil(args.rows / 1000))
        cost = requests * BACKLINKS_REQUEST + args.rows * BACKLINKS_ROW
        notes = ["Backlinks API has a $100/month minimum commitment credited to account balance."]
    else:
        raise AssertionError(args.estimate_kind)
    return emit({"ok": True, "kind": args.estimate_kind, "estimated_cost_usd": round(cost, 8), "notes": notes})


def cmd_user_data(args: argparse.Namespace) -> int:
    if not have_auth():
        sys.exit(str(RuntimeError("No DataForSEO credentials found; set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD.")))
    return emit(request("GET", "/v3/appendix/user_data"))


def cmd_locations(args: argparse.Namespace) -> int:
    # DataForSEO documents location lists at /v3/serp/google/locations and
    # /v3/keywords_data/google/locations. Country filtering is an optional
    # JSON field on the GET request, not a path suffix.
    api = "keywords_data/google" if args.api == "google-ads" else "serp/google"
    path = f"/v3/{api}/locations"
    payload = [{"country": args.country.lower()}] if args.country else None
    if args.dry_run:
        return print_dry_run("locations", path, payload, 0, ["Country is sent as an optional GET JSON field; the path stays /locations."])
    resp = request("GET", path, payload)
    if args.country and dataforseo_ok(resp):
        country = args.country.upper()
        for task in (resp.get("data") or {}).get("tasks", []) or []:
            if isinstance(task.get("result"), list):
                task["result"] = [r for r in task["result"] if (r.get("country_iso_code") or "").upper() == country]
                task["result_count"] = len(task["result"])
    return emit(resp)


def cmd_keyword_volume(args: argparse.Namespace) -> int:
    keywords = collect_keywords(args)
    if not keywords:
        sys.exit("keyword-volume requires --keyword, --keywords, or --file")
    if len(keywords) > 1000:
        sys.exit("DataForSEO Google Ads search volume accepts max 1,000 keywords per task; split the file.")
    task: Dict[str, Any] = {"keywords": keywords}
    add_locale(task, args)
    maybe_add(task, "date_from", args.date_from)
    maybe_add(task, "date_to", args.date_to)
    maybe_add(task, "tag", args.tag)
    if args.search_partners:
        task["search_partners"] = True
    if args.include_adult_keywords:
        task["include_adult_keywords"] = True
    mode = "live" if args.live else "standard"
    path = f"/v3/keywords_data/google_ads/search_volume/{'live' if args.live else 'task_post'}"
    estimate = KEYWORD_VOLUME_TASK[mode]
    payload = [task]
    if args.dry_run:
        return print_dry_run("keyword_volume", path, payload, estimate, ["Bills once per task, not per keyword, up to 1,000 keywords."])
    if not have_auth():
        sys.exit("No DataForSEO credentials found; set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD, or use --dry-run.")
    resp = request("POST", path, payload)
    if args.raw or not dataforseo_ok(resp) or not args.live:
        return emit(resp)
    return emit(normalize_keyword_volume(resp["data"]))


def cmd_keyword_volume_get(args: argparse.Namespace) -> int:
    path = f"/v3/keywords_data/google_ads/search_volume/task_get/{args.id}"
    if args.dry_run:
        return print_dry_run("keyword_volume_get", path, None, 0)
    resp = request("GET", path)
    if args.raw or not dataforseo_ok(resp):
        return emit(resp)
    return emit(normalize_keyword_volume(resp["data"]))


def cmd_keyword_volume_ready(args: argparse.Namespace) -> int:
    path = "/v3/keywords_data/google_ads/search_volume/tasks_ready"
    if args.dry_run:
        return print_dry_run("keyword_volume_ready", path, None, 0)
    return emit(request("GET", path))


def cmd_keyword_ideas(args: argparse.Namespace) -> int:
    keywords = collect_keywords(args)
    if not keywords:
        sys.exit("keyword-ideas requires --keyword, --keywords, or --file")
    task: Dict[str, Any] = {"keywords": keywords, "limit": args.limit}
    add_locale(task, args)
    maybe_add(task, "offset", args.offset)
    if args.include_serp_info:
        task["include_serp_info"] = True
    filters = parse_json_arg(args.filters, None)
    if filters is not None:
        task["filters"] = filters
    order_by = parse_json_arg(args.order_by, None)
    if order_by is not None:
        task["order_by"] = order_by
    path = "/v3/dataforseo_labs/google/keyword_ideas/live"
    estimate = LABS_TASK + args.limit * LABS_ITEM
    payload = [task]
    if args.dry_run:
        return print_dry_run("keyword_ideas", path, payload, estimate)
    if not have_auth():
        sys.exit("No DataForSEO credentials found; set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD, or use --dry-run.")
    resp = request("POST", path, payload)
    if args.raw or not dataforseo_ok(resp):
        return emit(resp)
    return emit(normalize_keyword_ideas(resp["data"]))


def cmd_serp(args: argparse.Namespace) -> int:
    task: Dict[str, Any] = {"keyword": args.keyword, "depth": args.depth}
    add_locale(task, args)
    maybe_add(task, "device", args.device)
    maybe_add(task, "os", args.os)
    maybe_add(task, "tag", args.tag)
    maybe_add(task, "se_domain", args.se_domain)
    if args.max_crawl_pages:
        task["max_crawl_pages"] = args.max_crawl_pages
    if args.people_also_ask_click_depth:
        task["people_also_ask_click_depth"] = args.people_also_ask_click_depth
    if args.calculate_rectangles:
        task["calculate_rectangles"] = True
    if args.priority:
        task["priority"] = 2
        mode = "priority"
    elif args.live:
        mode = "live"
    else:
        mode = "standard"
    if args.live:
        path = "/v3/serp/google/organic/live/advanced"
    else:
        path = "/v3/serp/google/organic/task_post"
    payload = [task]
    estimate = estimate_serp_cost(args.depth, mode)
    if args.dry_run:
        return print_dry_run("serp", path, payload, estimate)
    if not have_auth():
        sys.exit("No DataForSEO credentials found; set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD, or use --dry-run.")
    resp = request("POST", path, payload)
    if args.raw or not dataforseo_ok(resp) or not args.live:
        return emit(resp)
    return emit(normalize_serp(resp["data"], top=args.top))


def cmd_serp_get(args: argparse.Namespace) -> int:
    path = f"/v3/serp/google/organic/task_get/{args.kind}/{args.id}"
    if args.dry_run:
        return print_dry_run("serp_get", path, None, 0)
    resp = request("GET", path)
    if args.raw or not dataforseo_ok(resp):
        return emit(resp)
    return emit(normalize_serp(resp["data"], top=args.top))


def cmd_serp_ready(args: argparse.Namespace) -> int:
    path = "/v3/serp/google/organic/tasks_ready"
    if args.dry_run:
        return print_dry_run("serp_ready", path, None, 0)
    return emit(request("GET", path))


def cmd_backlinks(args: argparse.Namespace) -> int:
    task: Dict[str, Any] = {"target": args.target, "mode": args.mode, "limit": args.limit}
    filters = parse_json_arg(args.filters, None)
    if args.dofollow and filters is None:
        filters = ["dofollow", "=", True]
    if filters is not None:
        task["filters"] = filters
    maybe_add(task, "offset", args.offset)
    maybe_add(task, "search_after_token", args.search_after_token)
    path = "/v3/backlinks/backlinks/live"
    estimate = BACKLINKS_REQUEST + args.limit * BACKLINKS_ROW
    payload = [task]
    if args.dry_run:
        return print_dry_run("backlinks", path, payload, estimate, ["Backlinks API has a $100/month minimum commitment."])
    if not have_auth():
        sys.exit("No DataForSEO credentials found; set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD, or use --dry-run.")
    resp = request("POST", path, payload)
    if args.raw or not dataforseo_ok(resp):
        return emit(resp)
    return emit(normalize_backlinks(resp["data"]))


def cmd_raw(args: argparse.Namespace) -> int:
    payload = parse_json_arg(args.data, None)
    if args.dry_run:
        return print_dry_run("raw", args.path, payload, None)
    if not have_auth():
        sys.exit("No DataForSEO credentials found; set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD, or use --dry-run.")
    return emit(request(args.method, args.path, payload))


def add_locale_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--location-code", type=int, default=2840, help="Default 2840 = United States.")
    parser.add_argument("--location-name", default="")
    parser.add_argument("--location-coordinate", default="")
    parser.add_argument("--language-code", default="en")
    parser.add_argument("--language-name", default="")


def add_keyword_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--keyword", action="append", default=[], help="Repeatable keyword/seed.")
    parser.add_argument("--keywords", default="", help="Comma/newline/pipe separated keywords.")
    parser.add_argument("--file", default="", help="One keyword per line.")


def main() -> int:
    ap = argparse.ArgumentParser(description="DataForSEO API v3 helper for agent-seo-blueprint.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    est = sub.add_parser("estimate", help="Estimate public prices without credentials.")
    est_sub = est.add_subparsers(dest="estimate_kind", required=True)
    e_kw = est_sub.add_parser("keyword-volume")
    e_kw.add_argument("--count", type=int, required=True)
    e_kw.add_argument("--mode", choices=["standard", "live"], default="standard")
    e_serp = est_sub.add_parser("serp")
    e_serp.add_argument("--queries", type=int, default=1)
    e_serp.add_argument("--depth", type=int, default=10)
    e_serp.add_argument("--mode", choices=["standard", "priority", "live"], default="standard")
    e_ideas = est_sub.add_parser("keyword-ideas")
    e_ideas.add_argument("--requests", type=int, default=1)
    e_ideas.add_argument("--limit", type=int, default=100)
    e_bl = est_sub.add_parser("backlinks")
    e_bl.add_argument("--rows", type=int, required=True)
    est.set_defaults(func=cmd_estimate)

    user = sub.add_parser("user-data", help="Show account metadata/balance.")
    user.set_defaults(func=cmd_user_data)

    loc = sub.add_parser("locations", help="List supported locations.")
    loc.add_argument("--api", choices=["serp", "google-ads"], default="serp")
    loc.add_argument("--country", default="", help="Optional ISO country code filter sent in the GET body, e.g. us.")
    loc.add_argument("--dry-run", action="store_true")
    loc.set_defaults(func=cmd_locations)

    kv = sub.add_parser("keyword-volume", help="Google Ads search volume: live or standard task_post.")
    add_keyword_args(kv); add_locale_args(kv)
    kv.add_argument("--live", action="store_true", help="Use live endpoint; default is cheaper standard queue.")
    kv.add_argument("--date-from", default="")
    kv.add_argument("--date-to", default="")
    kv.add_argument("--search-partners", action="store_true")
    kv.add_argument("--include-adult-keywords", action="store_true")
    kv.add_argument("--tag", default="")
    kv.add_argument("--dry-run", action="store_true")
    kv.add_argument("--raw", action="store_true")
    kv.set_defaults(func=cmd_keyword_volume)

    kvg = sub.add_parser("keyword-volume-get", help="Fetch a standard Google Ads search-volume task by id.")
    kvg.add_argument("--id", required=True); kvg.add_argument("--dry-run", action="store_true"); kvg.add_argument("--raw", action="store_true")
    kvg.set_defaults(func=cmd_keyword_volume_get)
    kvr = sub.add_parser("keyword-volume-ready", help="List completed standard Google Ads search-volume tasks.")
    kvr.add_argument("--dry-run", action="store_true")
    kvr.set_defaults(func=cmd_keyword_volume_ready)

    ideas = sub.add_parser("keyword-ideas", help="DataForSEO Labs Google keyword ideas live endpoint.")
    add_keyword_args(ideas); add_locale_args(ideas)
    ideas.add_argument("--limit", type=int, default=100)
    ideas.add_argument("--offset", type=int, default=None)
    ideas.add_argument("--include-serp-info", action="store_true")
    ideas.add_argument("--filters", default="", help="JSON filter array, or @file.json")
    ideas.add_argument("--order-by", default="", help="JSON order_by value, or @file.json")
    ideas.add_argument("--dry-run", action="store_true")
    ideas.add_argument("--raw", action="store_true")
    ideas.set_defaults(func=cmd_keyword_ideas)

    serp = sub.add_parser("serp", help="Google Organic SERP: live advanced or standard task_post.")
    serp.add_argument("--keyword", required=True); add_locale_args(serp)
    serp.add_argument("--depth", type=int, default=10)
    serp.add_argument("--top", type=int, default=10, help="Normalized organic rows to keep.")
    serp.add_argument("--live", action="store_true")
    serp.add_argument("--priority", action="store_true", help="Standard task_post with high priority=2.")
    serp.add_argument("--device", choices=["desktop", "mobile"], default="desktop")
    serp.add_argument("--os", default="")
    serp.add_argument("--se-domain", default="")
    serp.add_argument("--max-crawl-pages", type=int, default=0)
    serp.add_argument("--people-also-ask-click-depth", type=int, default=0)
    serp.add_argument("--calculate-rectangles", action="store_true")
    serp.add_argument("--tag", default="")
    serp.add_argument("--dry-run", action="store_true")
    serp.add_argument("--raw", action="store_true")
    serp.set_defaults(func=cmd_serp)

    sg = sub.add_parser("serp-get", help="Fetch a standard SERP task by id.")
    sg.add_argument("--id", required=True)
    sg.add_argument("--kind", choices=["advanced", "regular", "html"], default="advanced")
    sg.add_argument("--top", type=int, default=10)
    sg.add_argument("--dry-run", action="store_true")
    sg.add_argument("--raw", action="store_true")
    sg.set_defaults(func=cmd_serp_get)
    sr = sub.add_parser("serp-ready", help="List completed standard SERP tasks.")
    sr.add_argument("--dry-run", action="store_true")
    sr.set_defaults(func=cmd_serp_ready)

    bl = sub.add_parser("backlinks", help="Backlinks API live endpoint.")
    bl.add_argument("--target", required=True)
    bl.add_argument("--mode", default="as_is", help="Default as_is; see DataForSEO docs for alternatives.")
    bl.add_argument("--limit", type=int, default=100)
    bl.add_argument("--offset", type=int, default=None)
    bl.add_argument("--search-after-token", default="")
    bl.add_argument("--dofollow", action="store_true")
    bl.add_argument("--filters", default="", help="JSON filter array, or @file.json")
    bl.add_argument("--dry-run", action="store_true")
    bl.add_argument("--raw", action="store_true")
    bl.set_defaults(func=cmd_backlinks)

    raw = sub.add_parser("raw", help="Escape hatch for arbitrary DataForSEO API path.")
    raw.add_argument("--method", choices=["GET", "POST"], default="GET")
    raw.add_argument("--path", required=True, help="Path like /v3/appendix/user_data")
    raw.add_argument("--data", default="", help="JSON payload or @file.json for POST.")
    raw.add_argument("--dry-run", action="store_true")
    raw.set_defaults(func=cmd_raw)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
