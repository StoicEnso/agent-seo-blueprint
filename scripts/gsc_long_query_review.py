#!/usr/bin/env python3
"""Review saved query+page GSC rows offline. No network, credentials or site writes."""
import argparse
from copy import deepcopy
from datetime import date, datetime, timezone
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit

PATTERN = r"^(?:\S+\s+){7,}\S+$"
# RE2 Perl whitespace excludes vertical tab and Unicode spaces; Python \s differs.
RE2_SPACE = r"[ \t\n\f\r]"
RE2_TOKEN = r"[^ \t\n\f\r]"
LONG_QUERY = re.compile(PATTERN.replace(r"\S", RE2_TOKEN).replace(r"\s", RE2_SPACE))
TOKENS = re.compile(RE2_TOKEN + "+")


def page_in_property(page, prop):
    """Validate absolute public-style URL membership without network access."""
    try:
        parsed = urlsplit(page)
        if parsed.scheme not in ("https", "http") or not parsed.hostname:
            return False
        if parsed.username or parsed.password or parsed.fragment or parsed.port == 0:
            return False
        if prop.startswith("sc-domain:"):
            domain = prop[len("sc-domain:"):].lower()
            if not domain or any(c in domain for c in "/:@?# "):
                return False
            return parsed.hostname == domain or parsed.hostname.endswith("." + domain)
        prefix = urlsplit(prop)
        return (prefix.scheme in ("http", "https") and bool(prefix.hostname)
                and not prefix.username and not prefix.password
                and not prefix.query and not prefix.fragment
                and parsed.scheme == prefix.scheme and parsed.hostname == prefix.hostname
                and (parsed.port or (443 if parsed.scheme == "https" else 80))
                == (prefix.port or (443 if prefix.scheme == "https" else 80))
                and parsed.path.startswith(prefix.path))
    except (ValueError, TypeError):
        return False


def number(value, name, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    if not math.isfinite(value) or value < 0 or (integer and int(value) != value):
        raise ValueError(f"invalid {name}")
    return int(value) if integer else float(value)


def review(payload, as_of=None, max_age_days=7):
    if not isinstance(payload, dict):
        raise ValueError("input must be an export object")
    meta = payload.get("metadata")
    rows = payload.get("rows")
    if not isinstance(meta, dict) or not isinstance(rows, list):
        raise ValueError("metadata object and rows list are required")
    for key in ("property", "start_date", "end_date", "captured_at", "search_type"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f"metadata.{key} is required")
    if meta.get("data_state") != "final" or not isinstance(meta.get("filters"), dict):
        raise ValueError("final data_state and explicit filters object required")
    dims = meta.get("dimensions")
    if (not isinstance(dims, list) or len(dims) != len(set(dims))
            or not {"query", "page"}.issubset(dims)
            or not set(dims).issubset({"query", "page", "country", "device"})):
        raise ValueError("dimensions must contain query,page and optional country,device")
    if not isinstance(meta.get("extraction_complete"), bool):
        raise ValueError("explicit extraction_complete boolean required")
    start, end = date.fromisoformat(meta["start_date"]), date.fromisoformat(meta["end_date"])
    captured = datetime.fromisoformat(meta["captured_at"].replace("Z", "+00:00"))
    today = as_of or datetime.now(timezone.utc).date()
    if not captured.tzinfo or start > end or end > captured.date() or captured.date() > today:
        raise ValueError("invalid window/capture dates or capture timezone missing")
    if isinstance(max_age_days, bool) or not isinstance(max_age_days, int) or max_age_days < 0:
        raise ValueError("max_age_days must be a nonnegative integer")
    # Validate the property even when there are no rows.
    prop = meta["property"]
    probe = ("https://" + prop[len("sc-domain:"):] + "/") if prop.startswith("sc-domain:") else prop
    if not page_in_property(probe, prop):
        raise ValueError("invalid property")
    stale = (today - end).days > max_age_days
    seen, candidates, nonmatches = set(), [], []
    for i, raw in enumerate(rows):
        if not isinstance(raw, dict):
            raise ValueError(f"row {i}: object required")
        row = deepcopy(raw)
        if "keys" in raw:
            if not isinstance(raw["keys"], list) or len(raw["keys"]) != len(dims):
                raise ValueError(f"row {i}: keys must match declared dimensions")
            for key, value in zip(dims, raw["keys"]):
                if key in row and row[key] != value:
                    raise ValueError(f"row {i}: conflicting {key}")
                row[key] = value
        if any(not isinstance(row.get(d), str) or not row[d] for d in dims):
            raise ValueError(f"row {i}: every declared dimension is required")
        if not page_in_property(row["page"], prop):
            raise ValueError(f"row {i}: page outside property or invalid URL")
        identity = tuple(row[d] for d in dims)
        if identity in seen:
            raise ValueError(f"row {i}: duplicate dimension scope; do not sum overlapping exports")
        seen.add(identity)
        clicks = number(row.get("clicks"), "clicks", integer=True)
        impressions = number(row.get("impressions"), "impressions", integer=True)
        position = number(row.get("position"), "position")
        if impressions == 0 or clicks > impressions or position < 1:
            raise ValueError(f"row {i}: invalid performance metrics")
        ctr = clicks / impressions
        if "ctr" in row:
            supplied = number(row["ctr"], "ctr")
            if supplied > 1 or abs(supplied - ctr) > 0.0001:
                raise ValueError(f"row {i}: CTR must be a 0..1 ratio consistent with clicks/impressions")
        row.update(clicks=clicks, impressions=impressions, ctr=ctr, position=position,
                   word_count=len(TOKENS.findall(row["query"])),
                   status="STALE_DATA" if stale else "NEEDS_PAGE_REVIEW")
        (candidates if LONG_QUERY.fullmatch(row["query"]) else nonmatches).append(row)
    candidates.sort(key=lambda r: (-r["impressions"], r["ctr"], r["query"], r["page"]))
    return {
        "metadata": deepcopy(meta), "regex": PATTERN, "as_of": today.isoformat(),
        "max_age_days": max_age_days, "window_days": (end - start).days + 1,
        "status": "STALE_DATA" if stale else ("PARTIAL_EXPORT" if not meta["extraction_complete"]
                  else ("CANDIDATES_NEED_REVIEW" if candidates else "NO_MATCHES")),
        "input_rows": len(rows), "matched_rows": len(candidates),
        "nonmatching_rows": len(nonmatches), "candidates": candidates, "nonmatches": nonmatches,
        "limitations": ["Top/anonymized rows may be omitted even when extraction_complete is true.",
                        "Length is not question intent, ChatGPT evidence or an approval to publish.",
                        "Review order is not a forecast or proof of a content gap."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    parser.add_argument("--as-of", type=date.fromisoformat, default=None)
    parser.add_argument("--max-age-days", type=int, default=7)
    args = parser.parse_args()
    try:
        result = review(json.loads(args.export.read_text(encoding="utf-8")), args.as_of, args.max_age_days)
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        parser.exit(2, f"Invalid saved export: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
