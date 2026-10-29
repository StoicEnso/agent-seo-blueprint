"""Synthetic offline regression cases. No real business/contact data or network."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("directory_evidence", ROOT / "scripts/directory_evidence.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
NOW = m.instant("2026-10-29T07:00:00Z")


def record(**changes):
    row = {"record_id": "synthetic-directory-1", "listing_url": "https://directory.example/product/example",
           "target_url": "https://business.example/", "final_url": "https://directory.example/product/example",
           "http_status": 200, "observed_at": "2026-10-28T12:00:00Z",
           "page_sha256": hashlib.sha256(b"saved page bytes v1").hexdigest(),
           "next_check": "2026-11-04T12:00:00Z", "listing_state": "public_reference_at_observation"}
    row.update(changes)
    return row


def reviewed():
    row = record()
    row["review"] = {"snapshot_key": m.snapshot_key(row), "reviewer": "synthetic-reviewer",
                     "reviewed_at": "2026-10-28T13:00:00Z", "decision": "accurate", "notes": "Synthetic only"}
    return row


def test_same_bytes_preserve_review_even_on_later_capture():
    old = reviewed()
    new = record(observed_at="2026-10-29T06:00:00Z")
    result = m.reconcile(new, old)
    assert result["review"] == old["review"]
    assert result["review_state"] == "reviewed_same_snapshot"
    assert old == reviewed()  # no mutation


@pytest.mark.parametrize("changes", [
    {"page_sha256": "b" * 64}, {"listing_url": "https://directory.example/different"},
    {"target_url": "https://different.example/"}, {"http_status": 403},
    {"final_url": "https://directory.example/login"}, {"page_sha256": ""},
])
def test_changed_context_or_bytes_invalidate_without_erasing_history(changes):
    old = reviewed()
    new = m.reconcile(record(**changes), old)
    assert new["review_state"] == "stale_review"
    assert "review" not in new
    assert old["review"] in new["review_history"]


def test_cannot_paste_old_review_onto_different_bytes():
    row = reviewed()
    row["page_sha256"] = "c" * 64
    with pytest.raises(ValueError, match="does not match"):
        m.reconcile(row)


def test_unhashed_legacy_evidence_is_not_retroactively_reviewed():
    row = record(page_sha256="", description_accuracy="pending_review")
    assert m.reconcile(row)["review_state"] == "pending_review"


@pytest.mark.parametrize("date,state", [("2026-09-26T00:00:00Z", "stale"),
    ("2026-10-30T00:00:00Z", "future_invalid"), ("", "unknown"),
    ("bad", "unknown"), ("2026-10-29", "unknown")])
def test_freshness_is_not_current_from_new_run_date(date, state):
    assert m.assess(record(observed_at=date), NOW)["freshness"] == state


@pytest.mark.parametrize("value,state", [("", "missing_date"), ("bad", "invalid_date"),
    ("2026-10-26T00:00:00Z", "overdue"), ("2026-10-29T07:00:00Z", "due"),
    ("2026-11-01T00:00:00Z", "planned")])
def test_past_and_blank_followup_dates_have_bounded_nonexecuting_steps(value, state):
    result = m.assess(record(next_check=value), NOW)["follow_up"]
    assert result["state"] == state
    assert result["executable"] is False


def test_hold_overrides_overdue_next_step_without_clearing_due_state():
    result = m.assess(record(next_check="2026-10-19T00:00:00Z", hold="owner hold"), NOW)
    assert result["follow_up"]["state"] == "overdue"
    assert "retain hold" in result["follow_up"]["proposed_next_step"]


def test_follow_up_at_alias():
    result = m.assess(record(next_check="", follow_up_at="2026-10-26T00:00:00Z"), NOW)
    assert result["follow_up"]["state"] == "overdue"


@pytest.mark.parametrize("indexing", [None, {"state": "indexed", "method": "site_search"},
    {"state": "indexed", "method": "robots_index_follow"},
    {"state": "indexed", "method": "authorized_url_inspection", "observed_at": "2026-09-01T00:00:00Z", "evidence_ref": "saved", "url": "https://directory.example/product/example"},
    {"state": "indexed", "method": "authorized_url_inspection", "observed_at": "2026-10-28T00:00:00Z", "evidence_ref": "saved", "url": "https://different.example/"},
])
def test_indexing_unknown_is_not_inferred_from_public_html(indexing):
    assert m.assess(record(indexing=indexing), NOW)["indexing"] == "unknown"


def test_exact_dated_inspection_is_observation_not_current_guarantee():
    row = record(indexing={"state": "indexed", "method": "authorized_url_inspection",
                          "url": record()["listing_url"], "observed_at": "2026-10-28T00:00:00Z", "evidence_ref": "synthetic.json"})
    assert m.assess(row, NOW)["indexing"] == "indexed_at_observation"


def test_future_review_is_invalid():
    row = reviewed()
    row["review"]["reviewed_at"] = "2026-10-30T13:00:00Z"
    assert m.assess(row, NOW)["review_state"] == "future_review_invalid"


def test_business_comparison_does_not_invent_missing_public_fields():
    fact = lambda value: {"value": value, "source": "https://business.example/", "verified_at": "2026-10-28T00:00:00Z", "status": "verified"}
    approved = {"name": fact("New Example Ltd"), "address": fact("Approved business address")}
    observed = {"name": fact("Old Example Ltd")}
    result = {row["field"]: row for row in m.reconcile_business(approved, observed)}
    assert result["name"]["state"] == "conflict_review"
    assert result["address"]["state"] == "unknown"
    assert not any(row["write_authorized"] for row in result.values())


def test_old_rows_not_collected_are_retained_not_reported_as_removed():
    result = m.run({"schema_version": 1, "records": [], "previous_records": [reviewed()]}, NOW)
    assert result["not_collected_previous_records"] == [reviewed()]
    assert result["assessments"] == []


def test_queue_cap_and_zero_side_effects():
    rows = [record(record_id=f"row-{i}", next_check="") for i in range(25)]
    result = m.run({"schema_version": 1, "records": rows}, NOW, limit=3)
    assert len(result["review_queue"]) == 3
    assert result["queue_total"] == 25 and result["deferred_count"] == 22
    assert result["network_requests"] == result["external_writes"] == result["schedule_changes"] == 0


def test_duplicate_ids_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        m.run({"schema_version": 1, "records": [record(), record()]}, NOW)


def test_cli_saved_synthetic_fixture():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/directory_evidence.py"),
        str(ROOT / "assets/directory-evidence-review.json"), "--as-of", NOW.isoformat()], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["mode"] == "OFFLINE_REVIEW_ONLY"
    assert {row["follow_up"]["state"] for row in output["assessments"]} >= {"missing_date", "overdue"}


def test_workflow_entry_exit_and_pending_dependency_are_explicit():
    authority = (ROOT / "workflows/authority-and-links.md").read_text()
    monitoring = (ROOT / "workflows/monitoring.md").read_text()
    playbook = (ROOT / "references/playbooks/authority/directory-submissions.md").read_text()
    for text in (authority, monitoring, playbook):
        assert "directory_evidence.py" in text
    for phrase in ("old-business", "public BUSINESS", "school", "sponsorship", "unknown", "same page bytes"):
        assert phrase in playbook
    assert "Public #33 / Full #26" in playbook
    assert "Public #34 / Full #27" in monitoring


@pytest.mark.parametrize("changes", [{"final_url": ""}, {"http_status": ""}, {"http_status": 999}])
def test_incomplete_capture_context_cannot_bind_review(changes):
    assert m.snapshot_key(record(**changes)) is None


def test_repeated_reconciliation_preserves_stale_history():
    changed = m.reconcile(record(page_sha256="d" * 64), reviewed())
    again = m.reconcile(changed)
    assert again["review_history"] == changed["review_history"]
    assert again["review_state"] == "stale_review"


@pytest.mark.parametrize("payload", [[], {"schema_version": 1, "records": ["not-an-object"]}])
def test_malformed_ledger_is_rejected(payload):
    with pytest.raises(ValueError):
        m.run(payload, NOW)


def test_malformed_history_is_rejected():
    with pytest.raises(ValueError, match="review_history"):
        m.reconcile(record(review_history="not-an-array"))
