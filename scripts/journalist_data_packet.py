#!/usr/bin/env python3
"""Offline, draft-only evidence packet builder. Python standard library only."""
import argparse
import csv
import html
import io
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

FIELDS = ("metric", "geography", "period_previous", "period_current", "previous", "current", "unit", "source_url", "source_locator")

def load_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(FIELDS):
            raise ValueError("CSV must have the exact documented fields in order")
        raw = list(reader)
    if not 1 <= len(raw) <= 100:
        raise ValueError("Use 1 to 100 reviewed aggregate observations")
    rows, seen = [], set()
    for row in raw:
        if None in row or any(v is None or not v.strip() for v in row.values()):
            raise ValueError("Missing or extra values")
        row = {k: v.strip() for k, v in row.items()}
        if any(len(v) > 500 or any(ord(c) < 32 for c in v) or v.startswith(("=", "+", "-", "@")) for v in row.values()):
            raise ValueError("Unsafe or oversized CSV value")
        for k in ("previous", "current"):
            if not re.fullmatch(r"[0-9]{1,12}", row[k]):
                raise ValueError("Counts must be bounded non-negative integers")
            row[k] = int(row[k])
        u = urlsplit(row["source_url"])
        if u.scheme not in ("https", "http") or not u.hostname or u.username or u.password:
            raise ValueError("Use an ordinary public HTTP(S) source URL")
        if row["period_previous"] == row["period_current"]:
            raise ValueError("Periods must differ")
        key = (row["metric"], row["geography"], row["period_previous"], row["period_current"])
        if key in seen:
            raise ValueError("Duplicate observation")
        seen.add(key)
        row["change"] = row["current"] - row["previous"]
        row["change_percent"] = round(row["change"] / row["previous"] * 100, 1) if row["previous"] else None
        rows.append(row)
    if len({(r["metric"], r["unit"], r["period_previous"], r["period_current"]) for r in rows}) != 1:
        raise ValueError("One packet must use one metric, unit and period pair")
    return rows


def build(source, output, brand="Research draft"):
    if not brand.strip() or len(brand) > 80 or any(ord(c) < 32 for c in brand):
        raise ValueError("Use a short brand label")
    rows = load_rows(source)
    out = Path(output)
    out.mkdir(parents=True, exist_ok=False)
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=FIELDS)
    w.writeheader()
    w.writerows({k: r[k] for k in FIELDS} for r in rows)
    (out / "data.csv").write_text(buf.getvalue(), encoding="utf-8")
    (out / "figures.json").write_text(json.dumps({"status": "DRAFT_REVIEW_REQUIRED", "publication": "NOT_APPROVED", "outreach": "NOT_APPROVED", "rows": rows}, indent=2)+"\n", encoding="utf-8")
    esc = lambda s: html.escape(str(s), quote=True)
    height = 150 + 72 * len(rows)
    maxval = max(max(r["previous"], r["current"]) for r in rows) or 1
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">', '<title id="title">Draft aggregate counts by geography</title>', '<desc id="desc">Zero-based paired horizontal bars. Full values and sources are in data.csv. Counts are not individual risk. Review required.</desc>', '<rect width="100%" height="100%" fill="white"/>', f'<text x="20" y="30" font-size="20">{esc(brand)} — DRAFT, NOT FOR PUBLICATION</text>', f'<text x="20" y="60" font-size="16">{esc(rows[0]["metric"])}: {esc(rows[0]["period_previous"])} (grey), {esc(rows[0]["period_current"])} (blue)</text>']
    lines = ['# DRAFT statistics page — review required', '', 'Data basis, reuse rights, privacy review, definitions, novelty, author, spokesperson consent, canonical URL and correction contact: REVIEW REQUIRED.', '', 'These are counts, not individual risk or unique people/businesses. Do not sum a national total with its regional components.', '', '| Geography | Previous | Current | Change | Change % |', '|---|---:|---:|---:|---:|']
    for i, r in enumerate(rows):
        y = 105 + 72*i
        svg.append(f'<text x="20" y="{y+12}" font-size="15">{esc(r["geography"])}</text>')
        for j, k in enumerate(("previous", "current")):
            svg.append(f'<rect x="400" y="{y+j*22}" width="{r[k]/maxval*650:.2f}" height="16" fill="{["#666666", "#075985"][j]}"/><text x="{410+r[k]/maxval*650:.2f}" y="{y+13+j*22}" font-size="14">{r[k]}</text>')
        pct = 'undefined (zero base)' if r['change_percent'] is None else str(r['change_percent'])+'%'
        safe_geo = r['geography'].replace('|', r'\|')
        lines.append(f'| {safe_geo} | {r["previous"]} | {r["current"]} | {r["change"]:+d} | {pct} |')
    svg += [f'<text x="20" y="{height-15}" font-size="14">Source and exact locators: data.csv. Method: statistics.md. NOT a risk ranking.</text>', '</svg>']
    (out/'chart.svg').write_text('\n'.join(svg)+'\n', encoding='utf-8')
    lines += ['', '## Method', '', 'Absolute change = current − previous. Percentage change = (current − previous) / previous × 100, rounded once to one decimal. Zero-base percentage change is undefined. Bar axes begin at zero. Definitions and periods must be independently checked before use.', '', '## Sources', '']
    for r in rows:
        lines += [f'- {r["geography"]}: {r["source_url"]} — {r["source_locator"]}']
    lines += ['', '## Suggested quote — DRAFT, no approved spokesperson', '', 'Use only a source-checked finding, with its population, periods and caveat. Never attribute this draft to a real person without consent.', '', '## Publication and outreach', '', 'NOT APPROVED. Validate an accessible evidence URL, recipient/byline/desk, method, rights and privacy before seeking the exact applicable approval. A local packet is not a live page or a sent pitch.']
    (out/'statistics.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    (out/'pitch-DRAFT.md').write_text("""DRAFT — NOT SENT — NOT SEND-READY

Recipient/byline and professional contact: VERIFY
Recent article, date and exact follow-up gap: VERIFY
Subject: [new supported finding tied to the verified article]

[Explain why this is a new, useful follow-up to that article.]
The prepared chart (chart.svg), aggregate figures (data.csv) and method
(statistics.md) are available for review. They are not yet public.
[Add one independently checked finding and its key caveat.]
Suggested quote: DRAFT — spokesperson approval required.
Public evidence/download URL and correction contact: NOT YET VERIFIED.

Check attachment rules, public URL, data rights and privacy. Obtain the
separate publication and exact recipient/batch outreach approvals before use.
""", encoding='utf-8')
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--brand', default='Research draft')
    args = p.parse_args()
    try:
        rows = build(args.input, args.output, args.brand)
    except (ValueError, OSError) as e:
        p.exit(2, f'error: {e}\n')
    print(json.dumps({'status': 'DRAFT_REVIEW_REQUIRED', 'observations': len(rows), 'output': args.output}))


if __name__ == '__main__':
    main()
