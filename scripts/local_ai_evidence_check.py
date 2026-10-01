"""Offline validation/counting of saved local AI evidence; no network or writes."""
import json
import sys
from collections import defaultdict
from datetime import datetime

SURFACES = {("google", "maps"), ("google", "ai_overviews"), ("google", "ai_mode"), ("openai", "chatgpt_search")}
DENOMINATORS = {"unique_domain_share": "unique_domains", "citation_volume_share": "citation_instances", "business_mention_rate": "completed_attempts", "result_set_overlap": "compared_result_sets"}
CONTEXT = ("provider", "surface", "exact_prompt", "location_context", "locale", "account_state", "panel_version")

def required_text(row, key):
    if not isinstance(row.get(key), str) or not row[key].strip():
        raise ValueError("Missing non-empty text: " + key)


def validate(data):
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("Expected object with version 1")
    if data.get("applicability") not in {"local_business", "not_applicable", "needs_review"}:
        raise ValueError("Invalid applicability")
    for key in ("limitations", "fact_checks", "source_statistics", "observations"):
        if not isinstance(data.get(key), list):
            raise ValueError("Expected list: " + key)
    if not data["limitations"] or any(not isinstance(x, str) or not x.strip() for x in data["limitations"]):
        raise ValueError("Declare limitations")
    for row in data["fact_checks"]:
        if not isinstance(row, dict):
            raise ValueError("Fact must be an object")
        for key in ("field", "evidence_locator", "proposed_action"):
            required_text(row, key)
        if row.get("status") not in {"verified", "missing", "conflicting", "not_applicable"} or row.get("action_state") != "draft_only":
            raise ValueError("Facts need valid status and draft_only action")
    for row in data["source_statistics"]:
        if not isinstance(row, dict):
            raise ValueError("Statistic must be an object")
        for key in ("source_url", "source_date", "section", "metric", "denominator", "limitation"):
            required_text(row, key)
        if DENOMINATORS.get(row["metric"]) != row["denominator"]:
            raise ValueError("Source statistic denominator mismatch")
        v = row.get("reported_percent")
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 100:
            raise ValueError("reported_percent must be between 0 and 100")
    groups = defaultdict(lambda: {"completed_attempts": 0, "unavailable_attempts": 0, "no_answer_attempts": 0, "business_mentions": 0, "owned_site_citations": 0, "days": set()})
    seen = set()
    for row in data["observations"]:
        if not isinstance(row, dict):
            raise ValueError("Observation must be an object")
        if data["applicability"] != "local_business":
            raise ValueError("Observations require local_business applicability")
        for key in CONTEXT + ("attempt_id", "captured_at", "evidence_locator"):
            required_text(row, key)
        if row["attempt_id"] in seen:
            raise ValueError("Duplicate attempt_id")
        seen.add(row["attempt_id"])
        if (row["provider"], row["surface"]) not in SURFACES:
            raise ValueError("Unsupported provider/surface pair")
        dt = datetime.fromisoformat(row["captured_at"].replace("Z", "+00:00"))
        if dt.tzinfo is None or dt.utcoffset().total_seconds() != 0:
            raise ValueError("captured_at must be UTC")
        state = row.get("state")
        if state not in {"returned", "no_answer", "unavailable"}:
            raise ValueError("Invalid observation state")
        for key in ("target_mentioned", "owned_site_cited"):
            value = row.get(key)
            if state == "unavailable":
                if value is not None:
                    raise ValueError("Unavailable outcome must be null, not absence")
            elif type(value) is not bool:
                raise ValueError("Completed outcomes must be booleans")
            elif state == "no_answer" and value:
                raise ValueError("No-answer attempt cannot contain mentions/citations")
        group = groups[tuple(row[k] for k in CONTEXT)]
        if state == "unavailable":
            group["unavailable_attempts"] += 1
        else:
            group["completed_attempts"] += 1
            group["no_answer_attempts"] += int(state == "no_answer")
            group["business_mentions"] += int(row["target_mentioned"])
            group["owned_site_citations"] += int(row["owned_site_cited"])
            group["days"].add(dt.date().isoformat())
    result = []
    for context, counts in sorted(groups.items()):
        days = len(counts.pop("days"))
        result.append({**dict(zip(CONTEXT, context)), **counts, "completed_days": days, "insufficient_repeat_evidence": counts["completed_attempts"] < 3 or days < 2})
    return {"valid": True, "applicability": data["applicability"], "groups": result, "limitations": data["limitations"], "note": "Counts only; not traffic, causality, significance, or a universal score."}


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/local_ai_evidence_check.py <ledger.json>", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)
        print(json.dumps(validate(data), indent=2, allow_nan=False))
        return 0
    except (ValueError, TypeError, OSError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
