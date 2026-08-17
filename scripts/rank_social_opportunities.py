#!/usr/bin/env python3
"""Rank read-only social listening results with transparent components.

A score never authorizes engagement. Every candidate remains blocked until the
community rules, product truth, affiliation wording, and final draft are reviewed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

QUESTION_MARKERS = {
    "best", "recommend", "recommendation", "looking for", "what should", "which", "any good",
    "worth using", "tool", "app", "software", "how do", "help", "ideas", "alternatives",
}


def text_terms(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9][a-z0-9+-]{1,}", value.casefold()))


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def collect_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload.get("items"), list):
        return payload["items"]
    if isinstance(payload.get("post"), dict):
        return [payload["post"]]
    return []


def load_payloads(paths: list[Path]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        items.extend(collect_items(payload))
    deduped: dict[str, dict[str, Any]] = {}
    for item in items:
        if item.get("url"):
            deduped[item["url"]] = item
    return list(deduped.values())


def score_item(item: dict[str, Any], truth: dict[str, Any], now: dt.datetime) -> dict[str, Any]:
    title = str(item.get("title") or "")
    body = str(item.get("text") or "")
    joined = f"{title} {body}".casefold()
    tokens = text_terms(joined)
    keywords = [str(term).casefold() for term in truth.get("keywords", [])]
    intent_terms = [str(term).casefold() for term in truth.get("buyer_intent_terms", [])]
    exclude_terms = [str(term).casefold() for term in truth.get("exclude_terms", [])]
    do_not_engage = {str(term).casefold() for term in truth.get("do_not_engage_subreddits", [])}

    matched_keywords = [term for term in keywords if term in joined or text_terms(term) <= tokens]
    matched_intent = [term for term in intent_terms if term in joined]
    marker_hits = [term for term in QUESTION_MARKERS if term in joined]
    exclusion_hits = [term for term in exclude_terms if term in joined]

    url = str(item.get("url") or "")
    match = re.search(r"reddit\.com/r/([^/]+)", url, re.I)
    subreddit = match.group(1) if match else "unknown"
    timestamp = parse_time(item.get("updated_at") or item.get("posted_at"))
    age_days = (now - timestamp).total_seconds() / 86400 if timestamp else None

    if age_days is None:
        freshness = 0.1
    elif age_days <= 7:
        freshness = 1.0
    elif age_days <= 30:
        freshness = 0.8
    elif age_days <= 90:
        freshness = 0.5
    elif age_days <= 365:
        freshness = 0.2
    else:
        freshness = 0.05

    relevance = min(1.0, len(matched_keywords) / max(2, min(5, len(keywords) or 2)))
    buyer_intent = min(1.0, (len(matched_intent) + len(marker_hits)) / 3)
    answer_fit = 1.0 if "?" in title or marker_hits else 0.4
    source_influence = 0.5  # Unknown until an answer-engine citation is observed.
    evidence_quality = 0.7 if body else 0.45

    hard_fails: list[str] = []
    if not matched_keywords:
        hard_fails.append("no_product_relevance")
    if subreddit.casefold() in do_not_engage:
        hard_fails.append("do_not_engage_community")
    if exclusion_hits:
        hard_fails.append("excluded_topic")
    if age_days is not None and age_days > 365:
        hard_fails.append("stale_thread")

    score = relevance * buyer_intent * answer_fit * source_influence * freshness * evidence_quality
    return {
        "url": url,
        "subreddit": subreddit,
        "title": title,
        "updated_at": item.get("updated_at") or item.get("posted_at"),
        "age_days": round(age_days, 1) if age_days is not None else None,
        "matched_keywords": " | ".join(matched_keywords),
        "matched_intent": " | ".join(sorted(set(matched_intent + marker_hits))),
        "relevance": round(relevance, 4),
        "buyer_intent": round(buyer_intent, 4),
        "answer_fit": round(answer_fit, 4),
        "source_influence": round(source_influence, 4),
        "freshness": round(freshness, 4),
        "evidence_quality": round(evidence_quality, 4),
        "opportunity_score": round(score, 6),
        "hard_fail": " | ".join(hard_fails),
        "rules_state": "not_checked",
        "approval_state": "research_only",
        "action_allowed": "false",
    }


def write_csv(rows: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else [
        "url", "subreddit", "title", "updated_at", "age_days", "matched_keywords",
        "matched_intent", "relevance", "buyer_intent", "answer_fit", "source_influence",
        "freshness", "evidence_quality", "opportunity_score", "hard_fail", "rules_state",
        "approval_state", "action_allowed",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank read-only social opportunities")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--truth", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--now", help="ISO-8601 test clock; defaults to current UTC")
    args = parser.parse_args()

    truth = json.loads(args.truth.read_text(encoding="utf-8"))
    now = parse_time(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    if now is None:
        raise SystemExit("invalid --now")
    rows = [score_item(item, truth, now) for item in load_payloads(args.inputs)]
    rows.sort(key=lambda row: (bool(row["hard_fail"]), -float(row["opportunity_score"]), row["url"]))
    write_csv(rows, args.out)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
