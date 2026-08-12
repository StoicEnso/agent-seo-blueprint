#!/usr/bin/env python3
"""
forecast.py — deterministic organic-traffic forecast for an SEO plan.

Why this exists: LLM agents drift when they do click-curve arithmetic by hand (and
inflate the headline number). This makes the forecast reproducible: same input -> same
numbers, with the AI-Overview / SERP-feature haircut applied explicitly.

MODEL (per pool, per milestone month):
    captured_clicks = summed_volume * ramp[month] * effective_ctr
    effective_ctr   = base_ctr(kd_tier) * aio_factor * capture_share

  - base_ctr(kd_tier): the CTR of the realistic ranking position for that difficulty.
      KD<=10 -> behaves like avg position ~3; KD 11-20 -> ~5; KD>20 -> ~8 (or excluded
      with --max-kd). Position->CTR uses the course click curve (#1 .30, #2 .15, #3 .10...).
  - aio_factor: pools flagged informational AND aio_exposed get CTR * (1 - aio_haircut).
      AI Overviews + PAA/image packs depress organic CTR most on informational SERPs.
  - ramp[month]: share of the pool's pages indexed + matured by that month (authority ramp).
  - capture_share: optional per-pool fraction of the pool we realistically target (e.g.
      net out apparel/news noise) — default 1.0.

USAGE
  python3 scripts/forecast.py --in pools.json [--aio-haircut 0.5] [--scenario base|downside]
  python3 scripts/forecast.py            # runs the built-in baby-books sample

pools.json: [ { "name","volume","kd"|"position","intent":"informational|commercial|...",
               "aio": true|false, "capture_share": 0.8 }, ... ]
Outputs a Markdown table (base + downside) to stdout; add --json for machine output.
"""
import argparse, json, sys

# Course click curve: organic CTR by SERP position (no features).
POS_CTR = {1: 0.30, 2: 0.15, 3: 0.10, 4: 0.07, 5: 0.05, 6: 0.04, 7: 0.03, 8: 0.025, 9: 0.02, 10: 0.018}
# Default authority ramp: fraction of a pool's addressable captured by milestone month.
RAMP = {"base": {3: 0.02, 6: 0.10, 12: 0.45, 18: 0.75},
        "downside": {3: 0.01, 6: 0.06, 12: 0.28, 18: 0.45}}
MONTHS = [3, 6, 12, 18]

def kd_to_position(kd):
    if kd is None: return 5
    if kd <= 10: return 3
    if kd <= 20: return 5
    return 8

def base_ctr(pool, max_kd):
    pos = pool.get("position") or kd_to_position(pool.get("kd"))
    if pool.get("kd") is not None and max_kd is not None and pool["kd"] > max_kd:
        return 0.0  # excluded: above the rankable bar
    # interpolate beyond 10
    return POS_CTR.get(int(pos), 0.012)

def forecast(pools, scenario, aio_haircut, max_kd):
    ramp = RAMP[scenario]
    rows, totals = [], {m: 0.0 for m in MONTHS}
    for p in pools:
        ctr = base_ctr(p, max_kd)
        informational = str(p.get("intent", "")).lower().startswith("info")
        aio_factor = (1 - aio_haircut) if (informational and p.get("aio")) else 1.0
        share = p.get("capture_share", 1.0)
        eff = ctr * aio_factor * share
        cells = {}
        for m in MONTHS:
            clicks = p["volume"] * ramp[m] * eff
            cells[m] = clicks
            totals[m] += clicks
        rows.append({"name": p["name"], "volume": p["volume"], "kd": p.get("kd"),
                     "eff_ctr": round(eff, 4), "aio": bool(informational and p.get("aio")), **{f"m{m}": round(cells[m]) for m in MONTHS}})
    return rows, {f"m{m}": round(totals[m]) for m in MONTHS}

SAMPLE = [
    {"name": "Baby shower (ideas/games/themes)", "volume": 612350, "kd": 2, "intent": "informational", "aio": True, "capture_share": 0.79},
    {"name": "Baby names — lists", "volume": 411250, "kd": 4, "intent": "informational", "aio": True, "capture_share": 0.9},
    {"name": "Gender reveal", "volume": 294700, "kd": 2, "intent": "informational", "aio": True, "capture_share": 0.85},
    {"name": "Pregnancy announcement", "volume": 139100, "kd": 1, "intent": "informational", "aio": True, "capture_share": 0.9},
    {"name": "Keepsake / memory book (commercial)", "volume": 64000, "kd": 3, "intent": "commercial", "aio": False, "capture_share": 1.0},
    {"name": "Gift hubs (commercial)", "volume": 86000, "kd": 3, "intent": "commercial", "aio": False, "capture_share": 1.0},
    {"name": "BOFU money floor", "volume": 7500, "kd": 7, "intent": "transactional", "aio": False, "capture_share": 1.0},
]

def fmt_table(rows, totals, title):
    out = [f"### {title}", "", "| Pool | Volume | KD | eff CTR | AIO | mo3 | mo6 | mo12 | mo18 |",
           "|---|--:|--:|--:|:--:|--:|--:|--:|--:|"]
    for r in rows:
        out.append(f"| {r['name']} | {r['volume']:,} | {r['kd']} | {r['eff_ctr']:.3f} | {'yes' if r['aio'] else '—'} | "
                   f"{r['m3']:,} | {r['m6']:,} | {r['m12']:,} | {r['m18']:,} |")
    out.append(f"| **TOTAL** |  |  |  |  | **{totals['m3']:,}** | **{totals['m6']:,}** | **{totals['m12']:,}** | **{totals['m18']:,}** |")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile")
    ap.add_argument("--aio-haircut", type=float, default=0.5)
    ap.add_argument("--max-kd", type=float, default=None, help="exclude pools above this KD")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    pools = SAMPLE
    if args.infile:
        with open(args.infile) as fh: pools = json.load(fh)
    elif not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data: pools = json.loads(data)

    base_rows, base_tot = forecast(pools, "base", args.aio_haircut, args.max_kd)
    down_rows, down_tot = forecast(pools, "downside", min(args.aio_haircut + 0.15, 0.85), args.max_kd)

    if args.json:
        print(json.dumps({"assumptions": {"click_curve": POS_CTR, "ramp": RAMP, "aio_haircut": args.aio_haircut},
                          "base": {"rows": base_rows, "totals": base_tot},
                          "downside": {"rows": down_rows, "totals": down_tot}}, indent=2)); return

    print(f"# Organic-traffic forecast (deterministic)\n\nAssumptions: click curve #1={POS_CTR[1]:.0%}/#2={POS_CTR[2]:.0%}/#3={POS_CTR[3]:.0%}; "
          f"AIO haircut on informational pools = {args.aio_haircut:.0%}; ramp(base)={RAMP['base']}.\n")
    print(fmt_table(base_rows, base_tot, "Base case (clicks / month)")); print()
    print(fmt_table(down_rows, down_tot, "Downside (bigger AIO haircut + slower ramp)")); print()
    print("> Numbers are reproducible from the input pools. Edit pools.json (volume/kd/intent/aio/capture_share) "
          "or --aio-haircut to re-run. This is a model, not a promise — gate it against real GSC indexed-rate + CTR.")

if __name__ == "__main__":
    main()
