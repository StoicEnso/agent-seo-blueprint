#!/usr/bin/env python3
"""Offline directory evidence/review reconciliation. No collectors or external actions."""
import argparse
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


IDENTITY = ("record_id", "listing_url", "target_url")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
DECISIONS = {"accurate", "review_needed", "not_applicable", "unverifiable"}


def instant(value):
    """Require a dated, timezone-aware timestamp; never assume the host timezone."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing timestamp")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return result.astimezone(timezone.utc)


def identity(row):
    if not isinstance(row, dict):
        raise ValueError("each record must be an object")
    key = tuple(row.get(field, "") for field in IDENTITY)
    if not all(isinstance(value, str) and value.strip() for value in key):
        raise ValueError("record_id, listing_url and target_url are required")
    for url in key[1:]:
        parsed = urlsplit(url)
        if (parsed.scheme not in {"http", "https"} or not parsed.hostname
                or parsed.username is not None or parsed.password is not None):
            raise ValueError("expected public HTTP(S) URL without credentials")
    return key


def snapshot_key(row):
    """A caller must hash the saved page BYTES, not the URL or capture date."""
    key = identity(row)
    page_hash = row.get("page_sha256", "")
    if not isinstance(page_hash, str) or not SHA256.fullmatch(page_hash):
        return None
    if not isinstance(row.get("final_url", ""), str):
        return None
    final = urlsplit(row.get("final_url") or "")
    status = str(row.get("http_status", ""))
    if (final.scheme not in {"http", "https"} or not final.hostname
            or final.username is not None or final.password is not None):
        return None
    if not status.isdigit() or not 100 <= int(status) <= 599:
        return None
    material = [*key, page_hash, row["final_url"], status]
    return hashlib.sha256(json.dumps(material, separators=(",", ":")).encode()).hexdigest()


def valid_review(review, row):
    if not isinstance(review, dict) or not snapshot_key(row):
        return False
    try:
        instant(review.get("reviewed_at"))
    except (TypeError, ValueError):
        return False
    return bool(
        review.get("snapshot_key") == snapshot_key(row)
        and review.get("reviewer")
        and review.get("decision") in DECISIONS
    )


def reconcile(current, previous=None):
    """Preserve reviews only for the same identity and exact page bytes/context."""
    result = copy.deepcopy(current)
    identity(result)
    prior = previous or {}
    for history_source in (result.get("review_history", []), prior.get("review_history", [])):
        if not isinstance(history_source, list) or not all(isinstance(item, dict) for item in history_source):
            raise ValueError("review_history must be an array of review objects")
    history = copy.deepcopy(result.get("review_history", []))
    for item in prior.get("review_history", []):
        if item not in history:
            history.append(copy.deepcopy(item))
    old = prior.get("review")
    if old and old not in history:
        history.append(copy.deepcopy(old))
    supplied = result.get("review")
    if supplied and not valid_review(supplied, result):
        raise ValueError("supplied review does not match the current evidence snapshot")
    if not supplied and old and all(result.get(k) == prior.get(k) for k in IDENTITY):
        if snapshot_key(result) == snapshot_key(prior) and valid_review(old, prior):
            result["review"] = copy.deepcopy(old)
    if valid_review(result.get("review"), result):
        result["review_state"] = "reviewed_same_snapshot"
    else:
        result.pop("review", None)
        result["review_state"] = "stale_review" if old or history else "pending_review"
    result["review_history"] = history
    result["snapshot_key"] = snapshot_key(result)
    return result


def follow_up(row, as_of):
    value = row.get("next_check") or row.get("follow_up_at")
    if not value:
        state = "missing_date"
    else:
        try:
            state = "overdue" if instant(value) < as_of else "due" if instant(value) == as_of else "planned"
        except (TypeError, ValueError):
            state = "invalid_date"
    action = {
        "missing_date": "propose one dated evidence check for owner review",
        "invalid_date": "correct the date in review; do not execute a check",
        "overdue": "review one bounded evidence check; never resubmit",
        "due": "review one bounded evidence check; never resubmit",
        "planned": "retain existing date; no action now",
    }[state]
    if row.get("hold"):
        action = "retain hold; internal review only until the named owner releases it"
    return {"state": state, "proposed_next_step": action, "executable": False}


def assess(row, as_of, max_age_days=30):
    result = reconcile(row)
    try:
        age = (as_of - instant(row.get("observed_at"))).total_seconds() / 86400
        freshness = "future_invalid" if age < 0 else "stale" if age > max_age_days else "current_dated_observation"
    except (TypeError, ValueError):
        age, freshness = None, "unknown"
    review = result.get("review")
    if review and instant(review["reviewed_at"]) > as_of:
        result["review_state"] = "future_review_invalid"
    indexing = row.get("indexing", {})
    indexed = "unknown"
    if isinstance(indexing, dict) and indexing.get("state") in {"indexed", "not_indexed"}:
        try:
            index_age = (as_of - instant(indexing.get("observed_at"))).total_seconds() / 86400
            if (indexing.get("method") == "authorized_url_inspection"
                    and indexing.get("evidence_ref") and indexing.get("url") == row["listing_url"]
                    and 0 <= index_age <= max_age_days):
                indexed = indexing["state"] + "_at_observation"
        except (TypeError, ValueError):
            pass
    return {
        "record_id": row["record_id"], "snapshot_key": snapshot_key(row),
        "review_state": result["review_state"], "freshness": freshness,
        "age_days": round(age, 2) if age is not None else None,
        "indexing": indexed, "follow_up": follow_up(row, as_of),
        "listing_state": row.get("listing_state", "unknown"),
        "link_attributes": row.get("link_attributes", []),
        "business_outcome": row.get("business_outcome", "unknown"),
    }


def reconcile_business(approved, observed):
    """Compare only source-backed approved BUSINESS fields. Missing stays unknown."""
    result = []
    for field in ("name", "website", "phone", "address", "category"):
        truth, public = approved.get(field, {}), observed.get(field, {})
        if not isinstance(truth, dict) or not isinstance(public, dict):
            raise ValueError("business facts must include value/source/verified_at/status")
        good = lambda fact: (fact.get("value") is not None and fact.get("source")
                             and fact.get("verified_at") and fact.get("status") == "verified")
        status = "unknown"
        if good(truth) and good(public):
            instant(truth["verified_at"])
            instant(public["verified_at"])
            normalize = lambda value: " ".join(str(value).casefold().split())
            status = "match" if normalize(truth["value"]) == normalize(public["value"]) else "conflict_review"
        result.append({"field": field, "state": status, "write_authorized": False})
    return result


def run(payload, as_of, limit=20):
    if not isinstance(payload, dict):
        raise ValueError("ledger must be an object")
    if payload.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if not 1 <= limit <= 100:
        raise ValueError("review queue limit must be between 1 and 100")
    max_age = payload.get("max_age_days", 30)
    if not isinstance(max_age, int) or isinstance(max_age, bool) or not 1 <= max_age <= 365:
        raise ValueError("max_age_days must be an integer between 1 and 365")
    records, previous = payload.get("records", []), payload.get("previous_records", [])
    if not isinstance(records, list) or not isinstance(previous, list):
        raise ValueError("records and previous_records must be arrays")
    for group in (records, previous):
        seen = set()
        for row in group:
            identity(row)
            if row["record_id"] in seen:
                raise ValueError("duplicate record_id")
            seen.add(row["record_id"])
    old = {row["record_id"]: row for row in previous}
    reconciled = [reconcile(row, old.get(row["record_id"])) for row in records]
    assessments = [assess(row, as_of, max_age) for row in reconciled]
    queue = [row for row in assessments if row["freshness"] != "current_dated_observation"
             or row["review_state"] != "reviewed_same_snapshot"
             or row["follow_up"]["state"] != "planned"]
    current_ids = {row["record_id"] for row in records}
    return {
        "schema_version": 1, "mode": "OFFLINE_REVIEW_ONLY", "as_of": as_of.isoformat(),
        "records": reconciled, "assessments": assessments, "review_queue": queue[:limit],
        "queue_total": len(queue), "deferred_count": max(0, len(queue) - limit),
        "not_collected_previous_records": [row for row in previous if row["record_id"] not in current_ids],
        "network_requests": 0, "external_writes": 0, "schedule_changes": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--as-of", required=True, help="timezone-aware timestamp")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    try:
        print(json.dumps(run(json.loads(args.ledger.read_text()), instant(args.as_of), args.limit), indent=2))
    except (ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"Invalid saved evidence: {exc}\n")


if __name__ == "__main__":
    main()
