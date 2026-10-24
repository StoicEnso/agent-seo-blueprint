#!/usr/bin/env python3
"""Summarize manually reviewed buyer recommendations from saved evidence; no network."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path

LABELS = {"primary", "tied_primary", "option", "mention_only", "absent", "unclear"}
STATUSES = {"ok", "partial", "error", "refusal", "blocked", "not_available"}
CONTEXT = ("provider", "surface", "model", "account_state", "locale", "language")


def required_text(obj: dict, key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key}: non-empty text required")
    return value


def timestamp(value: str) -> None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("captured_at: ISO timestamp required") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("captured_at: timezone required")


def validate(panel: dict) -> tuple[dict[str, dict], list[dict]]:
    if not isinstance(panel, dict) or type(panel.get("schema_version")) is not int or panel["schema_version"] != 1:
        raise ValueError("schema_version: expected 1")
    for key in ("panel_id", "brand_entity_id"):
        required_text(panel, key)
    prompt = panel.get("prompt")
    if not isinstance(prompt, dict):
        raise ValueError("prompt: expected object")
    for key in ("id", "text", "locale", "language"):
        required_text(prompt, key)
    if type(prompt.get("version")) is not int or prompt["version"] < 1:
        raise ValueError("prompt version: positive integer required")
    plan = panel.get("planned_runs")
    rows = panel.get("observations")
    if not isinstance(plan, list) or not plan or not isinstance(rows, list):
        raise ValueError("planned_runs: non-empty list; observations: list required")
    slots = {}
    for row in plan:
        if not isinstance(row, dict):
            raise ValueError("planned run: expected object")
        for key in ("slot_id", "provider", "surface"):
            required_text(row, key)
        if row["slot_id"] in slots:
            raise ValueError("duplicate planned slot")
        slots[row["slot_id"]] = row
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("observation: expected object")
        slot = required_text(row, "slot_id")
        if slot not in slots or slot in seen:
            raise ValueError("unknown or duplicate observed slot")
        seen.add(slot)
        for key in CONTEXT + ("captured_at", "evidence_locator", "prompt_text"):
            required_text(row, key)
        timestamp(row["captured_at"])
        if any(row[key] != slots[slot][key] for key in ("provider", "surface")):
            raise ValueError("observed provider/surface differs from planned slot")
        if row["prompt_text"] != prompt["text"] or type(row.get("prompt_version")) is not int or row["prompt_version"] != prompt["version"]:
            raise ValueError("observed prompt differs from frozen version")
        if any(row[key] != prompt[key] for key in ("locale", "language")):
            raise ValueError("observed locale/language differs from frozen prompt")
        if row.get("status") not in STATUSES:
            raise ValueError("unknown status")
        if row.get("review_state") not in {"verified", "needs_review"}:
            raise ValueError("unknown review_state")
        if row.get("recommendation") not in LABELS:
            raise ValueError("unknown recommendation label")
        if not isinstance(row.get("cited"), bool):
            raise ValueError("cited: true or false required; not a recommendation label")
        if row["status"] == "ok":
            raw = required_text(row, "raw_answer")
            if row["recommendation"] not in {"absent", "unclear"}:
                quote = required_text(row, "classification_quote")
                if quote not in raw:
                    raise ValueError("classification_quote: must occur in raw_answer")
        else:
            required_text(row, "reason")
            if row["recommendation"] != "unclear":
                raise ValueError("incomplete or failed run must be labelled unclear")
    return slots, rows


def summarize(panel: dict) -> dict:
    slots, rows = validate(panel)
    by_surface = defaultdict(list)
    for slot in slots.values():
        by_surface[(slot["provider"], slot["surface"])].append(slot["slot_id"])
    output = []
    for (provider, surface), planned_ids in sorted(by_surface.items()):
        observed = [row for row in rows if row["slot_id"] in planned_ids]
        contexts = defaultdict(list)
        for row in observed:
            contexts[tuple(row[key] for key in CONTEXT)].append(row)
        context_results = []
        for context, items in sorted(contexts.items()):
            valid = [row for row in items if row["status"] == "ok" and row["review_state"] == "verified" and row["recommendation"] != "unclear"]
            labels = Counter(row["recommendation"] for row in valid)
            context_results.append({
                **dict(zip(CONTEXT, context)),
                "observed": len(items), "classifiable": len(valid),
                "excluded": len(items) - len(valid),
                "strict_primary_picks": labels["primary"],
                "strict_primary_rate": labels["primary"] / len(valid) if valid else None,
                "labels": {label: labels[label] for label in sorted(LABELS - {"unclear"})},
                "cited_classifiable_runs": sum(row["cited"] for row in valid),
            })
        output.append({
            "provider": provider, "surface": surface, "planned": len(planned_ids),
            "observed": len(observed), "not_run": len(planned_ids) - len(observed),
            "statuses": dict(sorted(Counter(row["status"] for row in observed).items())),
            "contexts": context_results,
        })
    return {
        "schema_version": 1, "panel_id": panel["panel_id"],
        "brand_entity_id": panel["brand_entity_id"], "prompt": panel["prompt"],
        "coverage": {"planned": len(slots), "observed": len(rows), "not_run": len(slots) - len(rows)},
        "provider_surfaces": output,
        "limitations": [
            "Manual labels and raw evidence require human semantic review; this script does not verify meaning.",
            "Tied primary, option, first list position, mention and citation are not a strict primary pick.",
            "Missing, partial, failed, unreviewed and unclear runs are not brand absences.",
            "Repeated runs need not be independent; no population inference or cross-provider score.",
            "No search impressions, traffic, conversions, revenue or causal effect is measured.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("panel", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = summarize(json.loads(args.panel.read_text(encoding="utf-8")))
        if args.out and args.out.resolve() == args.panel.resolve():
            raise ValueError("output must not overwrite the evidence input")
        text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
