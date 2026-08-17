#!/usr/bin/env python3
"""Validate and summarize a versioned AI buyer-question panel."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REQUIRED = [
    "prompt_id",
    "prompt_version",
    "prompt_text",
    "intent",
    "funnel_stage",
    "segment",
    "locale",
    "priority",
    "business_value",
    "evidence_source",
    "active",
    "created_at",
    "retired_at",
    "change_reason",
]
INTENTS = {"commercial", "competitor", "problem", "branded", "other"}
FUNNEL = {"bofu", "mofu", "tofu", "retention", "other"}
BOOLS = {"true", "false"}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in REQUIRED if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing columns: {', '.join(missing)}")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def validate(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    seen_versions: set[tuple[str, int]] = set()
    active_texts: dict[tuple[str, str], str] = {}
    versions: dict[str, list[int]] = defaultdict(list)

    for index, row in enumerate(rows, start=2):
        prefix = f"row {index}"
        for field in REQUIRED:
            if field not in {"retired_at", "change_reason"} and not row.get(field):
                errors.append(f"{prefix}: {field} is required")
        try:
            version = int(row.get("prompt_version", ""))
            if version < 1:
                raise ValueError
        except ValueError:
            errors.append(f"{prefix}: prompt_version must be a positive integer")
            continue
        key = (row["prompt_id"], version)
        if key in seen_versions:
            errors.append(f"{prefix}: duplicate prompt_id/version {key}")
        seen_versions.add(key)
        versions[row["prompt_id"]].append(version)

        intent = row.get("intent", "").lower()
        if intent not in INTENTS:
            errors.append(f"{prefix}: unsupported intent {intent!r}")
        funnel = row.get("funnel_stage", "").lower()
        if funnel not in FUNNEL:
            errors.append(f"{prefix}: unsupported funnel_stage {funnel!r}")
        active = row.get("active", "").lower()
        if active not in BOOLS:
            errors.append(f"{prefix}: active must be true or false")
        if active == "false" and not row.get("retired_at"):
            errors.append(f"{prefix}: retired_at is required when active=false")
        if version > 1 and not row.get("change_reason"):
            errors.append(f"{prefix}: change_reason is required for prompt_version > 1")
        text_key = (row.get("locale", "").lower(), " ".join(row.get("prompt_text", "").lower().split()))
        if active == "true":
            if text_key in active_texts:
                errors.append(f"{prefix}: duplicate active prompt text; first seen as {active_texts[text_key]}")
            active_texts[text_key] = row["prompt_id"]

    for prompt_id, values in versions.items():
        ordered = sorted(set(values))
        expected = list(range(1, max(ordered) + 1))
        if ordered != expected:
            errors.append(f"prompt {prompt_id}: versions must be contiguous from 1; found {ordered}")
    return errors


def summary(rows: list[dict[str, str]]) -> dict[str, object]:
    active = [row for row in rows if row.get("active", "").lower() == "true"]
    return {
        "rows": len(rows),
        "active_prompts": len(active),
        "prompt_ids": len({row["prompt_id"] for row in rows}),
        "intents": dict(sorted(Counter(row["intent"].lower() for row in active).items())),
        "funnel_stages": dict(sorted(Counter(row["funnel_stage"].lower() for row in active).items())),
        "locales": dict(sorted(Counter(row["locale"] for row in active).items())),
        "segments": dict(sorted(Counter(row["segment"] for row in active).items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a versioned AI buyer-question panel CSV")
    parser.add_argument("panel", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        rows = load_rows(args.panel)
        errors = validate(rows)
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}) if args.json else f"INVALID: {exc}")
        return 2
    payload = {"valid": not errors, "errors": errors, "summary": summary(rows)}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("VALID" if not errors else "INVALID")
        print(json.dumps(payload["summary"], indent=2))
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
