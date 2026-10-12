#!/usr/bin/env python3
"""Validate saved weekly GSC review queues offline; never collect or execute work.

Evidence references are declarations, not proof that their contents were checked.
A valid queue cannot grant publication, CMS-write, or scheduler authority.
"""
import argparse
import datetime as dt
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ACTIONS = {"UPDATE_EXISTING", "NEW_PAGE_REVIEW"}
OUTCOMES = ACTIONS | {"HOLD", "NEEDS_MORE_DATA", "NO_ACTION"}
SCOPE_KEYS = {"project", "property", "search_type", "dimensions", "filters", "aggregation", "timezone"}
TOP_KEYS = {"schema_version", "queue_id", "scope", "windows", "limitations", "caps", "execution", "review_policy", "prior_pending_tasks", "tasks"}
TASK_KEYS = {"id", "dedup_key", "outcome", "evidence_refs", "hold_reason", "no_action_reason", "carried_forward", "expensive_check", "lane", "query_or_intent", "target_url", "problem_or_deliverable", "owner", "due", "overdue_reason", "approval_status", "acceptance_criteria", "source_or_cms_revision", "metrics", "uncertainty", "growth_pct", "checks", "existing_owner_url", "measurement_plan"}
METRICS = {"clicks", "impressions", "ctr", "position"}
COMMON_CHECKS = {"serp", "intent", "cannibalization"}
UPDATE_CHECKS = COMMON_CHECKS | {"page", "canonical"}
NEW_CHECKS = COMMON_CHECKS | {"demand", "business_relevance", "inventory", "distinct_page_role", "original_contribution", "source_packet"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def obj(value, field, allowed=None):
    require(isinstance(value, dict), f"{field} must be an object")
    if allowed is not None:
        require(not (set(value) - allowed), f"{field} contains unsupported fields: {sorted(set(value) - allowed)}")
    return value


def text(value, field):
    require(isinstance(value, str) and bool(value.strip()), f"{field} must be non-empty text")
    require(not value.strip().upper().startswith(("REPLACE", "TODO", "TBD")), f"{field} cannot be a placeholder")
    return value


def day(value, field):
    require(isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), f"{field} must be YYYY-MM-DD")
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{field} must be a valid YYYY-MM-DD date") from None


def refs(value, field):
    require(isinstance(value, list) and bool(value), f"{field} needs evidence references")
    for item in value:
        text(item, field)
    return value


def integer(value, field):
    require(type(value) is int and value >= 0, f"{field} must be a non-negative integer")
    return value


def finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def metric(value, field, unknown=False):
    if value is None and unknown:
        return
    require(finite_number(value) and value >= 0, f"{field} must be a finite non-negative number")


def safe_url(value, field):
    text(value, field)
    try:
        parsed = urlsplit(value)
        require(parsed.scheme in {"http", "https"} and bool(parsed.hostname), f"{field} must be an HTTP(S) URL")
        require(not parsed.username and not parsed.password and not re.search(r"[\s\x00-\x1f]", value), f"{field} must not contain credentials or whitespace")
        parsed.port  # Reject malformed ports without connecting.
    except (ValueError, TypeError):
        raise ValueError(f"{field} must be an uncredentialed HTTP(S) URL") from None
    return parsed


def validate_scope(scope, field):
    obj(scope, field, SCOPE_KEYS)
    require(set(scope) == SCOPE_KEYS, f"{field} must record every scope field")
    for key in ("project", "property", "search_type", "aggregation"):
        text(scope[key], f"{field}.{key}")
    prop = scope["property"]
    if prop.startswith("sc-domain:"):
        label = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
        require(bool(re.fullmatch(rf"(?:{label}\.)+{label}", prop[10:])), f"{field}.property needs a valid domain")
    else:
        safe_url(prop, f"{field}.property")
    require(scope["search_type"] in {"web", "image", "video", "news"}, f"{field}.search_type must be ordinary Search")
    require(scope["aggregation"] in {"auto", "byPage"}, f"{field}.aggregation must match query+page data")
    require(scope["dimensions"] == ["query", "page"], f"{field}.dimensions must be [query,page]")
    require(scope["timezone"] == "America/Los_Angeles", f"{field}.timezone must be America/Los_Angeles")
    require(isinstance(scope["filters"], list), f"{field}.filters must be a list")
    for item in scope["filters"]:
        obj(item, f"{field}.filter", {"dimension", "operator", "expression"})
        require(set(item) == {"dimension", "operator", "expression"}, "filter must record dimension, operator and expression")
        require(isinstance(item["dimension"], str) and item["dimension"] in {"country", "device", "page", "query", "searchAppearance"}, "unsupported filter dimension")
        require(isinstance(item["operator"], str) and item["operator"] in {"contains", "equals", "notContains", "notEquals", "includingRegex", "excludingRegex"}, "unsupported filter operator")
        text(item["expression"], "filter.expression")


def validate_metrics(period, name, allow_unknown):
    obj(period, name, METRICS)
    require(set(period) == METRICS, f"{name} must record all four metrics")
    for key, value in period.items():
        metric(value, f"{name}.{key}", allow_unknown)
    clicks, impressions, ctr, position = (period[key] for key in ("clicks", "impressions", "ctr", "position"))
    if clicks is not None and impressions is not None:
        require(clicks <= impressions, f"{name}: clicks cannot exceed impressions")
    if ctr is not None:
        require(ctr <= 1, f"{name}.ctr must be a fraction between 0 and 1")
    if impressions is not None and impressions > 0 and position is not None:
        require(position >= 1, f"{name}.position must be at least 1 for observed impressions")
    if impressions is not None and impressions > 0 and clicks is not None and ctr is not None:
        require(math.isclose(ctr, clicks / impressions, abs_tol=0.001), f"{name}.ctr does not match clicks/impressions within display rounding")


def validate(queue, as_of=None):
    """Return True for schema/invariants only; raises ValueError on bad input.

    Default freshness is evaluated on the recorded collection date for deterministic
    historical validation. The CLI defaults to today's UTC date; supply --as-of
    explicitly to check a historical artifact.
    """
    obj(queue, "queue", TOP_KEYS)
    require(set(queue) == TOP_KEYS, "queue must record every top-level contract field")
    require(queue["schema_version"] == "1.0", "unsupported schema_version")
    text(queue["queue_id"], "queue_id")
    scope = queue["scope"]
    validate_scope(scope, "scope")
    refs(queue["limitations"], "limitations")
    execution = obj(queue["execution"], "execution", {"mode", "cms_write", "publish", "schedule"})
    require(execution.get("mode") == "review_only", "execution.mode must be review_only")
    for key in ("cms_write", "publish", "schedule"):
        require(execution.get(key) is False, f"execution.{key} must be false")
    policy = obj(queue["review_policy"], "review_policy", {"max_data_age_days", "max_evidence_age_days", "due_timezone"})
    max_age = integer(policy.get("max_data_age_days"), "max_data_age_days")
    max_evidence_age = integer(policy.get("max_evidence_age_days"), "max_evidence_age_days")
    due_timezone = text(policy.get("due_timezone"), "due_timezone")
    require(due_timezone == "UTC" or bool(re.fullmatch(r"[A-Za-z_+-]+(?:/[A-Za-z0-9_+-]+)+", due_timezone)), "due_timezone must be UTC or an explicit IANA-style name")
    caps = obj(queue["caps"], "caps", {"candidate_cap", "expensive_check_cap"})
    cap = integer(caps.get("candidate_cap"), "candidate_cap")
    expensive_cap = integer(caps.get("expensive_check_cap"), "expensive_check_cap")
    require(expensive_cap <= cap, "expensive_check_cap cannot exceed candidate_cap")
    windows = obj(queue["windows"], "windows", {"current", "previous", "collection_date", "final_through"})
    collected = day(windows.get("collection_date"), "collection_date")
    reference = collected if as_of is None else day(as_of, "as_of")
    require(reference >= collected, "collection_date cannot be after as_of")
    parsed = []
    for name in ("current", "previous"):
        window = obj(windows.get(name), f"windows.{name}", {"start", "end", "final", "scope", "source_refs"})
        start, end = day(window.get("start"), f"{name}.start"), day(window.get("end"), f"{name}.end")
        require(start <= end <= collected, f"{name} dates must be ordered and no later than collection_date")
        require(type(window.get("final")) is bool, f"{name}.final must be a boolean")
        validate_scope(window.get("scope"), f"{name}.scope")
        require(window["scope"] == scope, f"{name}.scope mismatch; not like-for-like")
        refs(window.get("source_refs"), f"{name}.source_refs")
        parsed.append((start, end, window["final"]))
    (cs, ce, current_final), (ps, pe, previous_final) = parsed
    require(cs > pe and ce - cs == pe - ps, "windows must be non-overlapping equal-length chronological ranges")
    final_through = day(windows.get("final_through"), "final_through")
    require(final_through <= collected, "final_through cannot be after collection_date")
    tasks = queue["tasks"]
    require(isinstance(tasks, list) and len(tasks) <= cap, "tasks must be a list within candidate_cap")
    actionable = any(isinstance(t, dict) and isinstance(t.get("outcome"), str) and t["outcome"] in ACTIONS for t in tasks)
    if actionable:
        require(current_final and previous_final, "action data must use final windows")
        require(final_through >= ce, "final_through must cover current window")
        require((reference - ce).days <= max_age, "current window is stale under review_policy")
    prior = queue["prior_pending_tasks"]
    require(isinstance(prior, list), "prior_pending_tasks must be a list")
    old_ids, old_keys = {}, {}
    for item in prior:
        obj(item, "prior_pending_task", {"id", "dedup_key"})
        ident, key = text(item.get("id"), "prior.id"), text(item.get("dedup_key"), "prior.dedup_key")
        require(ident not in old_ids and key not in old_keys, "duplicate prior pending identity")
        old_ids[ident], old_keys[key] = key, ident
    ids, dedup_keys, expensive = set(), set(), 0
    for task in tasks:
        obj(task, "task", TASK_KEYS)
        ident, key = text(task.get("id"), "task.id"), text(task.get("dedup_key"), "task.dedup_key")
        require(ident not in ids and key not in dedup_keys, "task IDs and dedup keys must be unique")
        ids.add(ident); dedup_keys.add(key)
        require(key not in old_keys or old_keys[key] == ident, "pending work cannot be cloned under a new ID")
        require(ident not in old_ids or old_ids[ident] == key, "pending task identity cannot be retargeted")
        require(type(task.get("carried_forward")) is bool and task["carried_forward"] == (ident in old_ids), "carried_forward must match prior pending evidence")
        require(type(task.get("expensive_check")) is bool, "expensive_check must be a boolean")
        expensive += int(task["expensive_check"])
        outcome = task.get("outcome")
        require(isinstance(outcome, str) and outcome in OUTCOMES, "invalid task outcome")
        refs(task.get("evidence_refs"), "task.evidence_refs")
        if "approval_status" in task:
            require(task["approval_status"] == "PENDING", "approval_status must be PENDING")
        if "metrics" in task:
            metrics = obj(task["metrics"], "metrics", {"current", "previous"})
            require(set(metrics) == {"current", "previous"}, "metrics must record current and previous")
            for period in ("current", "previous"):
                validate_metrics(metrics[period], f"metrics.{period}", period == "previous" or outcome not in ACTIONS)
        if outcome in {"HOLD", "NEEDS_MORE_DATA"}:
            text(task.get("hold_reason"), "hold_reason")
        if outcome == "NO_ACTION":
            text(task.get("no_action_reason"), "no_action_reason")
        if outcome not in ACTIONS:
            require("growth_pct" not in task, "non-action observations must not claim growth percentages")
            continue
        for field in ("lane", "query_or_intent", "target_url", "problem_or_deliverable", "owner", "acceptance_criteria", "source_or_cms_revision"):
            text(task.get(field), field)
        target = safe_url(task["target_url"], "target_url")
        if scope["property"].startswith("sc-domain:"):
            domain = scope["property"][10:].lower()
            require(target.hostname.lower() == domain or target.hostname.lower().endswith("." + domain), "target_url is outside the authorized property")
        else:
            prefix = safe_url(scope["property"], "scope.property")
            require((target.scheme, target.hostname, target.port) == (prefix.scheme, prefix.hostname, prefix.port) and task["target_url"].startswith(scope["property"]), "target_url is outside the authorized URL-prefix property")
        require(task.get("approval_status") == "PENDING", "actionable task approval_status must be PENDING")
        due = obj(task.get("due"), "due", {"date", "timezone", "policy"})
        due_day = day(due.get("date"), "due.date")
        require(due.get("timezone") == due_timezone, "due timezone must match explicit project policy")
        text(due.get("policy"), "due.policy")
        if due_day < collected:
            require(task["carried_forward"], "new tasks cannot have a past due date")
            text(task.get("overdue_reason"), "overdue_reason")
        require("metrics" in task, "actionable tasks require observed metrics")
        require(task["metrics"]["current"]["impressions"] > 0, "actionable tasks need observed current demand")
        refs(task.get("uncertainty"), "uncertainty")
        if "growth_pct" in task:
            growth = obj(task["growth_pct"], "growth_pct", {"clicks", "impressions"})
            require(bool(growth), "growth_pct must name a metric")
            for name, claimed in growth.items():
                previous, current = task["metrics"]["previous"][name], task["metrics"]["current"][name]
                require(previous is not None and previous > 0, "growth percentage needs known nonzero previous data")
                require(finite_number(claimed), "growth_pct must be finite")
                require(math.isclose(claimed, (current - previous) / previous * 100, abs_tol=0.001), "growth_pct must match observed metrics")
        checks = obj(task.get("checks"), "checks", UPDATE_CHECKS | NEW_CHECKS)
        needed = UPDATE_CHECKS if outcome == "UPDATE_EXISTING" else NEW_CHECKS
        require(needed <= set(checks), "actionable task lacks required live/intent/source checks")
        for name, check in checks.items():
            obj(check, f"checks.{name}", {"status", "evidence_refs", "observed_date"})
            require(check.get("status") == "confirmed", f"checks.{name} must be confirmed with evidence")
            refs(check.get("evidence_refs"), f"checks.{name}.evidence_refs")
            observed = day(check.get("observed_date"), f"checks.{name}.observed_date")
            require(observed <= collected and (reference - observed).days <= max_evidence_age, f"checks.{name} evidence is future-dated or stale")
        if outcome == "NEW_PAGE_REVIEW":
            require("existing_owner_url" in task and task["existing_owner_url"] is None, "existing page ownership must be ruled out before NEW_PAGE_REVIEW")
        measurement = obj(task.get("measurement_plan"), "measurement_plan", {"checkpoints_days", "like_for_like", "baseline_refs", "site_control_refs", "metrics_separate", "causality_claimed", "schedule_created"})
        require(measurement.get("checkpoints_days") == [28, 56], "measurement plan must retain +28/+56 checkpoints")
        for field in ("like_for_like", "metrics_separate"):
            require(measurement.get(field) is True, f"measurement_plan.{field} must be true")
        for field in ("causality_claimed", "schedule_created"):
            require(measurement.get(field) is False, f"measurement_plan.{field} must be false")
        refs(measurement.get("baseline_refs"), "measurement baseline_refs")
        refs(measurement.get("site_control_refs"), "measurement site_control_refs")
    require(expensive <= expensive_cap, "expensive checks exceed declared cap")
    require(set(old_ids) <= ids, "every prior pending task needs a carried or resolved disposition")
    return True


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON field: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", help="Saved JSON review artifact, not an API input")
    parser.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).date().isoformat(), help="Freshness date; defaults to today's UTC date. Set explicitly for historical checks.")
    args = parser.parse_args(argv)
    try:
        path = Path(args.queue)
        require(path.stat().st_size <= 4 * 1024 * 1024, "queue input exceeds 4 MiB offline limit")
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle, object_pairs_hook=unique_object)
        validate(payload, args.as_of)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RecursionError) as error:
        print(json.dumps({"valid": False, "error": str(error), "execution_authority": False}))
        return 2
    print(json.dumps({"valid": True, "note": "schema/invariants only; evidence is not independently verified", "execution_authority": False}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
