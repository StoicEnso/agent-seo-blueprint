#!/usr/bin/env python3
"""Create a research-only external-action approval queue.

This tool creates rows only. It never sends, posts, publishes, buys, approves,
or marks an action executed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
from pathlib import Path

FIELDS = [
    "candidate_id",
    "created_at",
    "source_url",
    "platform",
    "community",
    "opportunity_score",
    "hard_fail",
    "recommended_lane",
    "speaker_identity",
    "affiliation_disclosure",
    "community_rules_url",
    "rules_state",
    "product_truth_state",
    "draft_path",
    "claim_evidence_path",
    "approval_state",
    "approved_by",
    "approved_at",
    "execution_state",
    "executed_at",
    "verification_path",
    "notes",
]


def load(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def candidate_id(url: str) -> str:
    return "social-" + hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def lane(row: dict[str, str]) -> str:
    if row.get("hard_fail"):
        return "not_eligible"
    score = float(row.get("opportunity_score") or 0)
    if score >= 0.15:
        return "research_then_draft"
    if score >= 0.04:
        return "observe_or_owned_content"
    return "observe_only"


def build(rows: list[dict[str, str]], created_at: str) -> list[dict[str, str]]:
    queue: list[dict[str, str]] = []
    for row in rows:
        url = row.get("url", "")
        queue.append(
            {
                "candidate_id": candidate_id(url),
                "created_at": created_at,
                "source_url": url,
                "platform": "reddit" if "reddit.com" in url else "unknown",
                "community": row.get("subreddit", ""),
                "opportunity_score": row.get("opportunity_score", ""),
                "hard_fail": row.get("hard_fail", ""),
                "recommended_lane": lane(row),
                "speaker_identity": "",
                "affiliation_disclosure": "",
                "community_rules_url": "",
                "rules_state": "not_checked",
                "product_truth_state": "not_checked",
                "draft_path": "",
                "claim_evidence_path": "",
                "approval_state": "research_only",
                "approved_by": "",
                "approved_at": "",
                "execution_state": "not_executed",
                "executed_at": "",
                "verification_path": "",
                "notes": row.get("title", ""),
            }
        )
    return queue


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a research-only approval queue from ranked opportunities")
    parser.add_argument("opportunities", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--created-at", default=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat())
    args = parser.parse_args()
    rows = build(load(args.opportunities), args.created_at)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
