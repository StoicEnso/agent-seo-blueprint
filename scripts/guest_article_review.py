#!/usr/bin/env python3
"""Generate research queries and check saved guest-article evidence offline.

No network, email, browser, submission, credential access or publication API.
A valid ledger is a review aid, never proof of acceptance or permission to act.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

MAX_JSON_BYTES = 2_000_000
MAX_EVIDENCE_BYTES = 1_000_000
STATUSES = {"DISCOVERED", "VERIFIED_EDITORIAL", "CONDITIONAL", "REJECTED"}
COSTS = {"UNKNOWN", "EXPLICITLY_FREE", "PAID", "MEMBERSHIP_REQUIRED"}
HARD_FLAGS = {"paid_followed_link", "required_link_exchange", "unrelated_niche", "closed_intake", "link_selling_network", "false_author_credentials"}


class ReviewError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def stamp(value):
    require(nonempty(value), "timestamp must be a non-empty ISO datetime")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReviewError("invalid ISO datetime") from exc
    require(parsed.tzinfo is not None, "timestamp must have a timezone")
    return parsed.astimezone(timezone.utc)


def hostname(url):
    require(nonempty(url) and not any(c.isspace() or ord(c) < 32 or c == "\\" for c in url), "URL must be non-empty without whitespace, controls or backslashes")
    try:
        parsed = urlsplit(url)
        host = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise ReviewError("invalid URL") from exc
    require(parsed.scheme == "https" and host and not parsed.username and not parsed.password,
            "evidence URLs must use HTTPS without credentials")
    require(port in (None, 443) and not parsed.fragment, "URL must use a public HTTPS port and have no fragment")
    host = host.lower().rstrip(".")
    require(host != "localhost" and "." in host and not host.endswith((".local", ".internal")), "public hostname required")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    require(address is None, "literal IP addresses are not publisher domains")
    require(re.fullmatch(r"[a-z0-9.-]+", host) is not None and all(
        re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", part) for part in host.split(".")),
        "invalid public hostname; use its ASCII/punycode form")
    return host


def first_party(url, domain):
    host = hostname(url)
    return host == domain or host.endswith("." + domain)


def queries(keywords):
    require(isinstance(keywords, list) and 1 <= len(keywords) <= 10, "provide 1–10 niche keywords")
    results = []
    seen = set()
    for keyword in keywords:
        require(nonempty(keyword) and len(keyword) <= 100 and not any(c in keyword for c in '\r\n"\\'),
                "keywords must be 1–100 characters without quotes, backslashes or newlines")
        require(all(ord(c) >= 32 for c in keyword), "keyword contains control characters")
        keyword = " ".join(keyword.split())
        for query in (
            f'intitle:"write for us" "{keyword}"',
            f'"{keyword}" ("contributor guidelines" OR "submit an article")',
            f'"{keyword}" ("editorial guidelines" OR "pitch an article")',
        ):
            if query not in seen:
                results.append({"keyword": keyword, "query": query, "status": "RESEARCH_QUERY_ONLY"})
                seen.add(query)
    return {"schema_version": 1, "queries": results, "network_requests": 0, "outreach_authorized": False}


def load_json(path):
    require(path.stat().st_size <= MAX_JSON_BYTES, "ledger exceeds size limit")
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(ReviewError("non-finite JSON number")))
    except (json.JSONDecodeError, UnicodeError, RecursionError) as exc:
        raise ReviewError("invalid UTF-8 JSON ledger") from exc


def check_ledger(payload, evidence_root, as_of, max_age_days=30):
    require(isinstance(payload, dict) and type(payload.get("schema_version")) is int and payload["schema_version"] == 1,
            "schema_version must be integer 1")
    require(payload.get("outreach_authorized") is False, "ledger must not grant outreach authority")
    require(type(max_age_days) is int and 1 <= max_age_days <= 90, "max evidence age must be 1–90 days")
    require(isinstance(payload.get("opportunities"), list) and len(payload["opportunities"]) <= 200,
            "opportunities must be a list of at most 200 rows")
    require(isinstance(payload.get("evidence"), list) and len(payload["evidence"]) <= 600,
            "evidence must be a list of at most 600 records")
    require(isinstance(as_of, datetime) and as_of.tzinfo is not None, "as_of must be a timezone-aware datetime")
    as_of = as_of.astimezone(timezone.utc)
    evidence_root = evidence_root.resolve()
    evidence = {}
    for item in payload["evidence"]:
        require(isinstance(item, dict), "evidence record must be an object")
        eid = item.get("id")
        require(nonempty(eid) and eid not in evidence, "evidence IDs must be non-empty and unique")
        hostname(item.get("url"))
        captured = stamp(item.get("captured_at"))
        require(captured <= as_of, f"future evidence: {eid}")
        path = item.get("path")
        require(nonempty(path) and not Path(path).is_absolute(), f"relative evidence path required: {eid}")
        file = (evidence_root / path).resolve()
        require(file.is_relative_to(evidence_root) and file.is_file(), f"evidence must exist inside root: {eid}")
        require(file.stat().st_size <= MAX_EVIDENCE_BYTES, f"evidence exceeds size limit: {eid}")
        content = file.read_bytes()
        require(item.get("sha256") == hashlib.sha256(content).hexdigest(), f"evidence hash mismatch: {eid}")
        require(nonempty(item.get("excerpt")), f"evidence excerpt required: {eid}")
        try:
            text = content.decode("utf-8")
        except UnicodeError as exc:
            raise ReviewError(f"evidence must be UTF-8 text: {eid}") from exc
        require(" ".join(item["excerpt"].split()) in " ".join(text.split()), f"excerpt not found in evidence: {eid}")
        evidence[eid] = (item, captured)

    results = []
    row_ids = set()
    destinations = set()
    for row in payload["opportunities"]:
        require(isinstance(row, dict), "opportunity must be an object")
        rid = row.get("id")
        require(nonempty(rid) and rid not in row_ids, "opportunity IDs must be non-empty and unique")
        row_ids.add(rid)
        for field in ("product", "publisher", "domain", "discovery_query", "pitch_title", "reader_value", "fit_reason"):
            require(nonempty(row.get(field)), f"{rid}: {field} required")
        domain = row["domain"]
        require(hostname("https://" + domain) == domain, f"{rid}: domain must be canonical lowercase hostname")
        key = (row["product"].strip().casefold(), domain.removeprefix("www."))
        require(key not in destinations, f"duplicate product/publisher destination: {rid}")
        destinations.add(key)
        require(isinstance(row.get("status"), str) and row["status"] in STATUSES, f"{rid}: invalid status")
        require(isinstance(row.get("cost_state"), str) and row["cost_state"] in COSTS, f"{rid}: invalid cost_state")
        require(isinstance(row.get("risk_flags"), list) and all(nonempty(x) for x in row["risk_flags"]), f"{rid}: risk_flags must be a string list")
        require(row.get("outreach_status") == "DRAFT_NOT_SENT", f"{rid}: research cannot claim an approved or sent pitch")
        require(row.get("link_outcome") == "NOT_PLACED", f"{rid}: discovery cannot claim a placed link")
        require(isinstance(row.get("link_policy"), str) and row["link_policy"] in {"UNKNOWN", "EDITORIAL_DISCRETION", "BIO_ONLY", "NO_PROMOTIONAL_LINKS"}, f"{rid}: invalid link policy")
        checked = stamp(row.get("checked_at")) if row.get("checked_at") is not None else None
        require(checked is None or checked <= as_of, f"{rid}: future checked_at")
        refs = row.get("evidence_ids")
        require(isinstance(refs, list) and all(nonempty(x) and x in evidence for x in refs), f"{rid}: evidence IDs must reference saved evidence")
        hard = sorted(set(row["risk_flags"]) & HARD_FLAGS)
        require(not hard or row["status"] == "REJECTED", f"{rid}: hard failure must be REJECTED")
        if row["cost_state"] == "EXPLICITLY_FREE":
            require(nonempty(row.get("free_basis")), f"{rid}: absent fee is not proof of free admission")
            require(any(first_party(evidence[x][0]["url"], domain)
                        and (as_of - evidence[x][1]).total_seconds() <= max_age_days * 86400
                        and " ".join(row["free_basis"].split()) in " ".join(evidence[x][0]["excerpt"].split()) for x in refs),
                    f"{rid}: free basis must quote current publisher-owned saved evidence")
        if row["status"] == "VERIFIED_EDITORIAL":
            require(checked is not None and (as_of - checked).total_seconds() <= max_age_days * 86400,
                    f"{rid}: missing or stale route check")
            require(row["cost_state"] in {"UNKNOWN", "EXPLICITLY_FREE"}, f"{rid}: paid or membership routes remain CONDITIONAL")
            require(row.get("editorial_review_observed") is True, f"{rid}: explicit editorial review evidence required")
            require(nonempty(row.get("author_basis")) and nonempty(row.get("claim_limits")), f"{rid}: author basis and claim limits required")
            for field in ("guidelines_url", "route_url", "sample_url"):
                url = row.get(field)
                require(first_party(url, domain), f"{rid}: {field} must be publisher-owned")
                matching = [evidence[x] for x in refs if evidence[x][0]["url"] == url]
                require(matching, f"{rid}: saved evidence missing for {field}")
                require(any((as_of - captured).total_seconds() <= max_age_days * 86400 for _, captured in matching),
                        f"{rid}: stale evidence for {field}")
            verdict = "DRAFT_REVIEW_READY"
        elif row["status"] == "REJECTED":
            require(nonempty(row.get("reason")), f"{rid}: rejection reason required")
            verdict = "DO_NOT_PITCH"
        else:
            require(nonempty(row.get("reason")), f"{rid}: unresolved condition required")
            verdict = "MORE_EVIDENCE_NEEDED"
        results.append({"id": rid, "product": row["product"], "publisher": row["publisher"], "verdict": verdict,
                        "cost_state": row["cost_state"], "cost_confirmed_free": row["cost_state"] == "EXPLICITLY_FREE",
                        "outreach_authorized": False})
    return {"schema_version": 1, "valid": True, "as_of": as_of.isoformat(), "rows": results,
            "network_requests": 0, "outreach_authorized": False,
            "limitations": "Checks saved evidence structure, hashes, excerpts and dates, not publisher quality, factual truth, acceptance, indexing, link rel or ranking value. Recheck rules before approved outreach."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    query = sub.add_parser("queries", help="Generate queries only; never runs searches")
    query.add_argument("--keyword", action="append", required=True)
    validate = sub.add_parser("validate", help="Check a saved ledger offline")
    validate.add_argument("ledger", type=Path)
    validate.add_argument("--evidence-root", type=Path)
    validate.add_argument("--as-of", help="Timezone-aware ISO timestamp; default is current UTC")
    validate.add_argument("--max-age-days", type=int, default=30)
    args = parser.parse_args(argv)
    try:
        if args.command == "queries":
            result = queries(args.keyword)
        else:
            now = stamp(args.as_of) if args.as_of else datetime.now(timezone.utc)
            result = check_ledger(load_json(args.ledger), args.evidence_root or args.ledger.parent, now, args.max_age_days)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ReviewError, OSError) as exc:
        print(json.dumps({"valid": False, "error": str(exc), "outreach_authorized": False}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
