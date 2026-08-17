#!/usr/bin/env python3
"""Compute deterministic AI-answer visibility metrics from saved JSONL runs."""
from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

VALID_STATUSES = {"ok", "partial"}


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> list[float | None]:
    if total == 0:
        return [None, None]
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    margin = z * math.sqrt((p * (1 - p) / total) + (z * z / (4 * total * total))) / denominator
    return [max(0.0, center - margin), min(1.0, center + margin)]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"line {number}: expected object")
        rows.append(row)
    return rows


def validate_run(run: dict[str, Any], number: int) -> list[str]:
    errors: list[str] = []
    always_required = ("run_id", "prompt_id", "prompt_version", "prompt_text", "provider", "surface", "locale", "captured_at", "status")
    for field in always_required:
        if run.get(field) in (None, ""):
            errors.append(f"run {number}: {field} is required")
    if run.get("status") in VALID_STATUSES:
        for field in ("model", "account_state", "raw_answer", "parser_version", "parse_review_state"):
            if run.get(field) in (None, ""):
                errors.append(f"run {number}: {field} is required for a valid answer run")
        mentions = run.get("mentions")
        citations = run.get("citations")
        if not isinstance(mentions, list):
            errors.append(f"run {number}: mentions must be a list")
        else:
            for index, mention in enumerate(mentions, 1):
                if not isinstance(mention, dict) or not (mention.get("entity_id") or mention.get("entity_name")):
                    errors.append(f"run {number}: mention {index} needs entity_id or entity_name")
        if not isinstance(citations, list):
            errors.append(f"run {number}: citations must be a list")
        else:
            for index, citation in enumerate(citations, 1):
                if not isinstance(citation, dict) or not citation.get("url") or not citation.get("domain") or not citation.get("source_type"):
                    errors.append(f"run {number}: citation {index} needs url, domain, and source_type")
                if isinstance(citation, dict) and not isinstance(citation.get("owned"), bool):
                    errors.append(f"run {number}: citation {index} owned must be true or false")
    return errors


def aggregate(runs: Iterable[dict[str, Any]], brand: str) -> dict[str, Any]:
    all_runs = list(runs)
    valid = [run for run in all_runs if run.get("status") in VALID_STATUSES]
    errors = [run for run in all_runs if run.get("status") not in VALID_STATUSES]
    brand = brand.casefold()
    present = 0
    positions: list[int] = []
    sentiments: Counter[str] = Counter()
    brand_mentions = 0
    all_mentions = 0
    brand_weight = 0.0
    all_weight = 0.0
    citations = 0
    owned_citations = 0
    competitor_mentions: Counter[str] = Counter()

    for run in valid:
        mentions = run.get("mentions") or []
        seen_brand = False
        seen_entities: set[str] = set()
        for mention in mentions:
            entity = str(mention.get("entity_id") or mention.get("entity_name") or "").casefold()
            if not entity or entity in seen_entities:
                continue
            seen_entities.add(entity)
            all_mentions += 1
            try:
                position = int(mention.get("position") or 0)
            except (TypeError, ValueError):
                position = 0
            weight = (1.0 / position) if position > 0 else 0.0
            all_weight += weight
            if entity == brand:
                seen_brand = True
                brand_mentions += 1
                brand_weight += weight
                if position > 0:
                    positions.append(position)
                sentiment = str(mention.get("sentiment") or "unknown").lower()
                sentiments[sentiment] += 1
            else:
                competitor_mentions[entity] += 1
        present += int(seen_brand)
        for citation in run.get("citations") or []:
            citations += 1
            owned_citations += int(bool(citation.get("owned")))

    total = len(valid)
    visibility = present / total if total else None
    return {
        "runs": {"total": len(all_runs), "valid": total, "errors_or_refusals": len(errors)},
        "brand": brand,
        "visibility": {
            "mentions": present,
            "responses": total,
            "rate": visibility,
            "wilson_95": wilson(present, total),
        },
        "share_of_voice": {
            "raw": (brand_mentions / all_mentions) if all_mentions else None,
            "brand_mentions": brand_mentions,
            "all_tracked_brand_mentions": all_mentions,
            "position_weighted": (brand_weight / all_weight) if all_weight else None,
            "brand_weight": brand_weight,
            "all_tracked_brand_weight": all_weight,
        },
        "position": {
            "count": len(positions),
            "mean": statistics.mean(positions) if positions else None,
            "median": statistics.median(positions) if positions else None,
            "distribution": dict(sorted(Counter(positions).items())),
        },
        "sentiment": dict(sorted(sentiments.items())),
        "citations": {
            "total": citations,
            "owned": owned_citations,
            "owned_share": (owned_citations / citations) if citations else None,
        },
        "competitors": dict(competitor_mentions.most_common()),
        "limitations": [
            "answer_runs_are_observations_not_impressions",
            "provider_datasets_must_remain_separate",
            "visibility_change_does_not_establish_causality",
        ],
    }


def report(rows: list[dict[str, Any]], brand: str) -> dict[str, Any]:
    errors = [error for index, row in enumerate(rows, 1) for error in validate_run(row, index)]
    if errors:
        raise ValueError("; ".join(errors))
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("provider") or "unknown")].append(row)
    return {
        "schema_version": "geo-metrics-0.1",
        "brand": brand,
        "all_providers": aggregate(rows, brand),
        "providers": {name: aggregate(items, brand) for name, items in sorted(groups.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute deterministic metrics from AI answer-run JSONL")
    parser.add_argument("runs", type=Path)
    parser.add_argument("--brand", required=True, help="Canonical entity_id for the project brand")
    parser.add_argument("--out")
    args = parser.parse_args()
    try:
        payload = report(load_jsonl(args.runs), args.brand)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 2
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(path)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
