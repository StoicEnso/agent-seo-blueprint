#!/usr/bin/env python3
"""
Render workflow artifacts from data into a project workspace.

Thin, dependency-free helpers the workflows call to write dated, consistent artifacts
(audit reports, keyword maps, monitoring snapshots). Templates live in ../assets/.

Usage:
    python3 scripts/report.py audit      --workspace DIR --title "Site audit: example.com" --data findings.json
    python3 scripts/report.py keywords   --workspace DIR --data keywords.json   # -> CSV keyword map
    python3 scripts/report.py monitoring --workspace DIR --data snapshot.json
    python3 scripts/report.py note       --workspace DIR --subdir research --name angles --data x.json

`--data` is a JSON file; structure depends on the artifact (see each renderer).
Outputs are written dated into the workspace subdir and the path is printed.
"""
import argparse, csv, json, sys, datetime
from pathlib import Path

TODAY = datetime.date.today().isoformat()


def out_path(ws, subdir, stem, ext):
    d = Path(ws).expanduser().resolve() / subdir
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{TODAY}_{stem}.{ext}"


def load(data_path):
    return json.loads(Path(data_path).read_text(encoding="utf-8")) if data_path else {}


def render_audit(ws, title, data):
    """data: {summary, score?, findings:[{area,severity,issue,fix,evidence?}]}"""
    findings = data.get("findings", [])
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings.sort(key=lambda f: order.get(str(f.get("severity", "low")).lower(), 9))
    lines = [f"# {title}", "", f"_Generated {TODAY}_", ""]
    if data.get("summary"):
        lines += ["## Summary", data["summary"], ""]
    if data.get("score") is not None:
        lines += [f"**Overall score:** {data['score']}", ""]
    lines += ["## Findings (prioritized)", "", "| # | Severity | Area | Issue | Recommended fix |",
              "|---|---|---|---|---|"]
    for i, f in enumerate(findings, 1):
        lines.append(f"| {i} | {f.get('severity','')} | {f.get('area','')} | "
                     f"{f.get('issue','').replace('|','/')} | {f.get('fix','').replace('|','/')} |")
    p = out_path(ws, "audits", "audit", "md")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def render_keywords(ws, data):
    """data: {"rows":[{keyword,volume,kd,intent,cpc,current_rank,target_url,priority,cluster}]}
    Also accepts a bare list of row dicts."""
    rows = data.get("rows", []) if isinstance(data, dict) else (data or [])
    cols = ["keyword", "cluster", "intent", "volume", "kd", "cpc", "current_rank", "target_url", "priority", "notes"]
    p = out_path(ws, "keywords", "keyword-map", "csv")
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    return p


def render_monitoring(ws, data):
    """data: {site, period, metrics:{clicks,impressions,avg_position,...}, keywords:[{keyword,position,change}], notes}"""
    lines = [f"# Monitoring snapshot — {data.get('site','')}", "", f"_Generated {TODAY}_  period: {data.get('period','')}", ""]
    m = data.get("metrics", {})
    if m:
        lines += ["## Metrics", "", "| Metric | Value |", "|---|---|"]
        for k, v in m.items():
            lines.append(f"| {k} | {v} |")
        lines.append("")
    kws = data.get("keywords", [])
    if kws:
        lines += ["## Tracked keywords", "", "| Keyword | Position | Change |", "|---|---|---|"]
        for k in kws:
            lines.append(f"| {k.get('keyword','')} | {k.get('position','')} | {k.get('change','')} |")
        lines.append("")
    if data.get("notes"):
        lines += ["## Notes", data["notes"], ""]
    p = out_path(ws, "monitoring", "snapshot", "md")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def render_note(ws, subdir, name, data):
    p = out_path(ws, subdir, name, "json")
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return p


def main():
    ap = argparse.ArgumentParser(description="Render SEO workflow artifacts.")
    ap.add_argument("kind", choices=["audit", "keywords", "monitoring", "note"])
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--title", default="SEO report")
    ap.add_argument("--data", default="")
    ap.add_argument("--subdir", default="research")
    ap.add_argument("--name", default="note")
    args = ap.parse_args()
    data = load(args.data)
    if args.kind == "audit":
        p = render_audit(args.workspace, args.title, data)
    elif args.kind == "keywords":
        p = render_keywords(args.workspace, data)
    elif args.kind == "monitoring":
        p = render_monitoring(args.workspace, data)
    else:
        p = render_note(args.workspace, args.subdir, args.name, data)
    print(f"Wrote {p}")


if __name__ == "__main__":
    main()
