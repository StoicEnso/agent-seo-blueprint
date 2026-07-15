#!/usr/bin/env python3
"""
Per-project workspace manager for the agent-seo-blueprint skill.

A workspace holds everything for ONE site/project: config, audits, keyword maps,
content briefs, review drafts, monitoring history, outreach lists.

Usage:
    python3 scripts/workspace.py status [--path DIR]      # show/resolve workspace
    python3 scripts/workspace.py init  --path DIR --name NAME [--domain d] [--niche n]
    python3 scripts/workspace.py show  --path DIR         # print project.json

Resolution rule for agents: if the user names a workspace, use it. Otherwise look for
./seo-workspace/<project>/. If none exists, ASK the user before creating one
(this script's `init` only runs on explicit instruction).

Secrets (API keys) are NEVER stored here — project.json references them by env-var name.
"""
import argparse, json, sys, datetime
from pathlib import Path

SUBDIRS = ["audits", "keywords", "briefs", "drafts", "monitoring", "outreach", "research"]

PROJECT_TEMPLATE = {
    "name": "",
    "created": "",
    "domains": [],
    "niche": "",
    "locale": "en-US",
    "competitors": [],
    "data_sources": {
        "ahrefs": {"mode": "browser", "api_key_env": "AHREFS_API_KEY", "workspace": ""},
        "gsc": {"mode": "browser", "property": "", "api_creds_env": "GSC_CREDS"},
        "ga4": {"mode": "browser", "property_id": "", "api_creds_env": "GA4_CREDS"},
        "serp": {"mode": "browser", "locale": "en-US"},
        "pagespeed": {"mode": "api", "api_key_env": "PAGESPEED_API_KEY"}
    },
    "monitoring": {"enabled": False, "cadence": "weekly", "tracked_keywords": []}
}


def ws_path(path):
    return Path(path).expanduser().resolve()


def status(path):
    p = ws_path(path)
    cfg = p / "project.json"
    if cfg.exists():
        data = json.loads(cfg.read_text(encoding="utf-8"))
        print(f"Workspace EXISTS: {p}")
        print(f"  name: {data.get('name')}  domains: {data.get('domains')}  niche: {data.get('niche')}")
        present = [d for d in SUBDIRS if (p / d).is_dir()]
        print(f"  subdirs: {', '.join(present) or '(none)'}")
        return 0
    print(f"NO workspace at: {p}")
    print("  -> Ask the user whether to create one here, then run: workspace.py init --path <DIR> --name <NAME>")
    return 1


def init(path, name, domain, niche):
    p = ws_path(path)
    p.mkdir(parents=True, exist_ok=True)
    for d in SUBDIRS:
        (p / d).mkdir(exist_ok=True)
    cfg = p / "project.json"
    if cfg.exists():
        print(f"project.json already exists at {cfg} — leaving it untouched.")
        return 0
    data = json.loads(json.dumps(PROJECT_TEMPLATE))
    data["name"] = name
    data["created"] = datetime.date.today().isoformat()
    if domain:
        data["domains"] = [domain]
    if niche:
        data["niche"] = niche
    cfg.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Initialized workspace at {p}")
    print(f"  created project.json + subdirs: {', '.join(SUBDIRS)}")
    print("  Next: fill in domains/competitors/data_sources in project.json (secrets by env-var name only).")
    return 0


def show(path):
    cfg = ws_path(path) / "project.json"
    if not cfg.exists():
        sys.exit(f"No project.json at {cfg}")
    print(cfg.read_text(encoding="utf-8"))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Per-project workspace manager.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status"); s.add_argument("--path", default="./seo-workspace")
    i = sub.add_parser("init")
    i.add_argument("--path", required=True); i.add_argument("--name", required=True)
    i.add_argument("--domain", default=""); i.add_argument("--niche", default="")
    sh = sub.add_parser("show"); sh.add_argument("--path", required=True)
    args = ap.parse_args()
    if args.cmd == "status":
        sys.exit(status(args.path))
    elif args.cmd == "init":
        sys.exit(init(args.path, args.name, args.domain, args.niche))
    elif args.cmd == "show":
        sys.exit(show(args.path))


if __name__ == "__main__":
    main()
