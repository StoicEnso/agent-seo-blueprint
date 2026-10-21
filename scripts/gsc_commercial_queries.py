#!/usr/bin/env python3
"""Offline, read-only commercial-term discovery from normalized GSC exports.

No credentials, network, site writes or automatic keyword-to-content decisions.
Input: {meta:{site,start,end,dimensions,type,data_state,country,device},rows:[...]}.
Only query or query+page dimensions are accepted. See the accompanying reference.
"""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
import re
import sys

# Screenshot transcription, line wraps collapsed only. Kept to expose false negatives.
SOURCE_REGEX = r"\b(buy shop order|pricing|price|cost|hire|book|schedule reserve nearme instock available sameday|best|vs|review |reviews alternative alternatives | deal discount)\b"
GROUPS = {
    "transaction": r"buy|shop|order|hire|book|schedule|reserve",
    "price": r"pricing|price|cost|deal|discount",
    "comparison": r"best|vs|review|reviews|alternative|alternatives",
    "availability": r"near\s*me|in\s*stock|available|same\s*day",
}
CORRECTED_REGEX = r"(?i)\b(buy|shop|order|pricing|price|cost|hire|book|schedule|reserve|near\s*me|in\s*stock|available|same\s*day|best|vs|review|reviews|alternative|alternatives|deal|discount)\b"
PATTERN = re.compile(CORRECTED_REGEX, re.ASCII)
SOURCE_PATTERN = re.compile(SOURCE_REGEX, re.IGNORECASE | re.ASCII)
GROUP_PATTERNS = {name: re.compile(r"\b(?:" + value + r")\b", re.IGNORECASE | re.ASCII)
                  for name, value in GROUPS.items()}
SCOPE = ("site", "dimensions", "type", "country", "device")


def classify(query):
    """Lexical candidate signals only, never a buying-intent or relevance verdict."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a nonempty string")
    return {
        "matched_terms": sorted({match.group().lower() for match in PATTERN.finditer(query)}),
        "signal_groups": [name for name, pattern in GROUP_PATTERNS.items() if pattern.search(query)],
        "source_pattern_match": bool(SOURCE_PATTERN.search(query)),
    }


def _date(value):
    if not isinstance(value, str):
        raise ValueError("dates must be ISO YYYY-MM-DD strings")
    try:
        parsed = dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("invalid date") from exc
    if parsed.isoformat() != value:
        raise ValueError("dates must use YYYY-MM-DD")
    return parsed


def _number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(label + " must be a finite number (unknown is not zero)")
    return value


def validate(payload, as_of):
    if not isinstance(payload, dict) or not isinstance(payload.get("meta"), dict):
        raise ValueError("input needs meta and rows")
    meta = payload["meta"]
    for key in SCOPE:
        if key not in meta or meta[key] is None:
            raise ValueError("missing scope: " + key)
    for key in ("site", "type", "country", "device"):
        if not isinstance(meta[key], str) or not meta[key].strip():
            raise ValueError("invalid scope: " + key)
    if meta["dimensions"] not in (["query"], ["query", "page"]):
        raise ValueError("dimensions must be query or query,page, in that order")
    if meta["type"] != "web" or meta.get("data_state") != "final":
        raise ValueError("only final ordinary web Search data is supported")
    # This analyzer expects an unfiltered baseline; otherwise source/corrected comparisons mislead.
    if meta.get("include_regex") or meta.get("exclude_regex") or meta.get("filters"):
        raise ValueError("use an unfiltered query baseline for discovery")
    start, end = _date(meta.get("start")), _date(meta.get("end"))
    if start > end or end >= as_of:
        raise ValueError("window must end before as-of and start no later than end")
    if meta.get("date_timezone", "America/Los_Angeles") != "America/Los_Angeles":
        raise ValueError("GSC dates use America/Los_Angeles")
    rows = payload.get("rows")
    if not isinstance(rows, list):
        raise ValueError("rows must be a list (an explicit empty list is allowed)")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid row")
        keys = row.get("keys")
        if not isinstance(keys, list) or len(keys) != len(meta["dimensions"]):
            raise ValueError("row keys must match dimensions")
        if any(not isinstance(key, str) or not key.strip() for key in keys):
            raise ValueError("row keys must be nonempty strings")
        if tuple(keys) in seen:
            raise ValueError("duplicate dimension keys; do not silently double-count")
        seen.add(tuple(keys))
        clicks = _number(row.get("clicks"), "clicks")
        impressions = _number(row.get("impressions"), "impressions")
        position = _number(row.get("position"), "position")
        if clicks < 0 or impressions <= 0 or clicks > impressions or position < 1:
            raise ValueError("invalid clicks/impressions/position range")
        if int(clicks) != clicks or int(impressions) != impressions:
            raise ValueError("clicks and impressions must be whole counts")
        if "ctr" in row:
            ctr = _number(row["ctr"], "ctr")
            if not 0 <= ctr <= 1 or abs(ctr - clicks / impressions) > 0.0001:
                raise ValueError("ctr must be a fraction consistent with clicks/impressions")
    return start, end


def metrics(rows):
    clicks = sum(row["clicks"] for row in rows)
    impressions = sum(row["impressions"] for row in rows)
    return {"rows": len(rows), "clicks": clicks, "impressions": impressions,
            "ctr": clicks / impressions if impressions else None,
            "impression_weighted_position": (
                sum(row["position"] * row["impressions"] for row in rows) / impressions
                if impressions else None)}


def analyze(current, previous=None, as_of=None):
    as_of = _date(as_of) if as_of else dt.datetime.now(dt.timezone.utc).date()
    start, end = validate(current, as_of)
    old = {}
    if previous is not None:
        pstart, pend = validate(previous, as_of)
        if any(current["meta"][key] != previous["meta"][key] for key in SCOPE):
            raise ValueError("comparison scope/dimensions must match")
        if pend + dt.timedelta(days=1) != start or (end - start) != (pend - pstart):
            raise ValueError("comparison needs adjacent equal-length non-overlapping windows")
        old = {tuple(row["keys"]): row for row in previous["rows"]}
    matched, controls, recovered = [], [], []
    for row in current["rows"]:
        signals = classify(row["keys"][0])
        before = old.get(tuple(row["keys"]))
        item = {"keys": row["keys"], "clicks": row["clicks"],
                "impressions": row["impressions"], "ctr": row["clicks"] / row["impressions"],
                "position": row["position"], **signals,
                "previous_observation": "observed" if before is not None else "not_observed_or_unavailable",
                "click_delta": row["clicks"] - before["clicks"] if before is not None else None,
                "intent_verified": False, "business_fit_verified": False,
                "existing_page_reviewed": False, "approved_for_write": False,
                "disposition": "REVIEW_ONLY" if signals["matched_terms"] else "CONTROL_NOT_MATCHED"}
        if signals["matched_terms"]:
            matched.append(item)
            if not signals["source_pattern_match"]:
                recovered.append(item)
        else:
            controls.append(item)
    order = lambda row: (-row["impressions"], tuple(row["keys"]))
    return {
        "status": "STALE_REVIEW_ONLY" if (as_of - end).days > 7 else "REVIEW_ONLY",
        "as_of": as_of.isoformat(), "meta": current["meta"],
        "filters": {"corrected": CORRECTED_REGEX, "source_transcription": SOURCE_REGEX},
        "aggregation": "query" if current["meta"]["dimensions"] == ["query"] else "query_page",
        "observed_rows": metrics(current["rows"]),
        "commercial_term_candidates": metrics(matched),
        "source_pattern_missed": metrics(recovered),
        "groups": {name: metrics([row for row in matched if name in row["signal_groups"]])
                   for name in GROUPS},
        "candidates": sorted(matched, key=order), "nonmatching_controls": sorted(controls, key=order),
        "limitations": [
            "Regex matches are not verified buying intent, relevance, rankings or conversions.",
            "English seed only; ASCII word boundaries and whitespace matching are not language-universal.",
            "Named query rows exclude hidden data; pagination does not guarantee exhaustive coverage.",
            "Row sums are not property totals; query and query+page aggregations are not interchangeable.",
            "Groups overlap. Do not sum group totals. Missing prior rows are unknown, not zero.",
            "No website writes or automatic content generation. Review the live SERP and existing page first.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("current", type=Path)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--as-of", help="ISO date; default today UTC; GSC windows themselves use Pacific dates")
    args = parser.parse_args()
    try:
        current = json.loads(args.current.read_text(encoding="utf-8"))
        previous = json.loads(args.previous.read_text(encoding="utf-8")) if args.previous else None
        report = analyze(current, previous, args.as_of)
    except (OSError, ValueError, TypeError, OverflowError, RecursionError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc)}))
        return 2
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
