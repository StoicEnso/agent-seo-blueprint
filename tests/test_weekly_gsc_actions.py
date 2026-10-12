import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("weekly_gsc_under_test", ROOT / "scripts/weekly_gsc_actions.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
AS_OF = "2026-10-02"


def queue(outcome="UPDATE_EXISTING"):
    scope = {"project": "demo", "property": "sc-domain:example.com", "search_type": "web", "dimensions": ["query", "page"], "filters": [], "aggregation": "byPage", "timezone": "America/Los_Angeles"}
    task = {"id": "query-page-1", "dedup_key": "example.com/page:example-intent", "outcome": outcome, "evidence_refs": ["exports/query-page.json"], "carried_forward": False, "expensive_check": False}
    if outcome in {"HOLD", "NEEDS_MORE_DATA"}:
        task["hold_reason"] = "Await an independently checked live canonical."
    elif outcome == "NO_ACTION":
        task["no_action_reason"] = "The current page already answers this intent."
    else:
        needed = validator.UPDATE_CHECKS if outcome == "UPDATE_EXISTING" else validator.NEW_CHECKS
        task.update({"lane": "content", "query_or_intent": "example intent", "target_url": "https://example.com/page", "problem_or_deliverable": "Add a sourced section missing from the live page.", "owner": "editor", "due": {"date": "2026-10-09", "timezone": "Europe/London", "policy": "Owner-selected next review; not a scheduled job."}, "approval_status": "PENDING", "acceptance_criteria": "Review the exact useful diff with supported claims.", "source_or_cms_revision": "cms:revision-17", "uncertainty": ["Observed changes are not causal proof."], "metrics": {"current": {"clicks": 10, "impressions": 100, "ctr": 0.1, "position": 8.0}, "previous": {"clicks": 5, "impressions": 80, "ctr": 0.0625, "position": 9.0}}, "checks": {name: {"status": "confirmed", "evidence_refs": ["research/" + name + ".json"], "observed_date": AS_OF} for name in needed}, "measurement_plan": {"checkpoints_days": [28, 56], "like_for_like": True, "baseline_refs": ["exports/baseline.json"], "site_control_refs": ["exports/site-control.json"], "metrics_separate": True, "causality_claimed": False, "schedule_created": False}})
        if outcome == "NEW_PAGE_REVIEW":
            task["existing_owner_url"] = None
    return {"schema_version": "1.0", "queue_id": "demo-2026-10-02", "scope": scope, "windows": {"current": {"start": "2026-09-01", "end": "2026-09-28", "final": True, "scope": copy.deepcopy(scope), "source_refs": ["exports/current.json"]}, "previous": {"start": "2026-08-04", "end": "2026-08-31", "final": True, "scope": copy.deepcopy(scope), "source_refs": ["exports/previous.json"]}, "collection_date": AS_OF, "final_through": "2026-09-28"}, "limitations": ["Top rows only; privacy-limited or missing query rows remain unknown."], "caps": {"candidate_cap": 20, "expensive_check_cap": 8}, "execution": {"mode": "review_only", "cms_write": False, "publish": False, "schedule": False}, "review_policy": {"max_data_age_days": 7, "max_evidence_age_days": 7, "due_timezone": "Europe/London"}, "prior_pending_tasks": [], "tasks": [task]}


class WeeklyGscActionsTests(unittest.TestCase):
    def reject(self, data, phrase=None):
        with self.assertRaises(ValueError) as caught:
            validator.validate(data, AS_OF)
        if phrase:
            self.assertIn(phrase, str(caught.exception))

    def cli(self, content, extra=None, binary=False):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "queue.json"
            if binary:
                path.write_bytes(content)
            else:
                path.write_text(content, encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/weekly_gsc_actions.py"), str(path), "--as-of", AS_OF] + (extra or []), text=True, capture_output=True)
        self.assertNotIn("Traceback", result.stderr)
        return result, json.loads(result.stdout)

    def test_valid_update_and_new_page(self):
        self.assertTrue(validator.validate(queue(), AS_OF))
        self.assertTrue(validator.validate(queue("NEW_PAGE_REVIEW"), AS_OF))

    def test_preserves_non_action_outcomes(self):
        for outcome in ("HOLD", "NEEDS_MORE_DATA", "NO_ACTION"):
            with self.subTest(outcome=outcome):
                self.assertTrue(validator.validate(queue(outcome), AS_OF))

    def test_partial_data_can_only_be_held(self):
        data = queue("HOLD")
        data["windows"]["current"]["final"] = False
        self.assertTrue(validator.validate(data, AS_OF))
        data = queue(); data["windows"]["current"]["final"] = False
        self.reject(data, "final windows")

    def test_missing_previous_rows_are_unknown_not_zero(self):
        data = queue()
        data["tasks"][0]["metrics"]["previous"] = dict.fromkeys(validator.METRICS, None)
        data["tasks"][0]["uncertainty"] = ["Prior query row was not returned; growth is unknown."]
        self.assertTrue(validator.validate(data, AS_OF))
        self.assertIsNone(data["tasks"][0]["metrics"]["previous"]["impressions"])

    def test_rejects_non_boolean_final(self):
        for value in ("false", 1, None, []):
            data = queue(); data["windows"]["current"]["final"] = value
            self.reject(data, "boolean")

    def test_rejects_dates_and_incomparable_windows(self):
        for field, value in (("start", "20260901"), ("start", "2026-02-30"), ("end", "2026-08-01"), ("start", "2026-08-31"), ("end", "2026-09-29")):
            data = queue(); data["windows"]["current"][field] = value
            self.reject(data)

    def test_rejects_future_collection_and_final_dates(self):
        data = queue(); data["windows"]["collection_date"] = "2026-08-01"
        self.reject(data)
        data = queue(); data["windows"]["final_through"] = "2026-10-03"
        self.reject(data, "collection_date")
        with self.assertRaisesRegex(ValueError, "as_of"):
            validator.validate(queue(), "2026-10-01")

    def test_rejects_stale_action_data_and_evidence(self):
        with self.assertRaisesRegex(ValueError, "stale"):
            validator.validate(queue(), "2026-10-20")
        data = queue(); data["tasks"][0]["checks"]["serp"]["observed_date"] = "2026-09-01"
        self.reject(data, "stale")
        data = queue(); data["tasks"][0]["checks"]["serp"]["observed_date"] = "2026-10-03"
        self.reject(data, "future-dated")

    def test_rejects_insufficient_final_through(self):
        data = queue(); data["windows"]["final_through"] = "2026-09-27"
        self.reject(data, "cover current")

    def test_rejects_changed_scope(self):
        for field, value in (("property", "sc-domain:other.example"), ("search_type", "image"), ("filters", [{"dimension": "country", "operator": "equals", "expression": "USA"}]), ("aggregation", "auto")):
            data = queue(); data["windows"]["previous"]["scope"][field] = value
            self.reject(data, "mismatch")

    def test_rejects_unsupported_dimensions_timezone_and_aggregation(self):
        for field, value in (("dimensions", ["query"]), ("timezone", "Europe/London"), ("aggregation", "byProperty"), ("filters", None)):
            data = queue(); data["scope"][field] = value
            self.reject(data)

    def test_rejects_duplicate_current_tasks(self):
        data = queue(); data["tasks"].append(copy.deepcopy(data["tasks"][0]))
        self.reject(data, "unique")
        data = queue(); other = copy.deepcopy(data["tasks"][0]); other["id"] = "new-id"; data["tasks"].append(other)
        self.reject(data, "unique")

    def test_pending_tasks_are_carried_not_cloned(self):
        data = queue(); task = data["tasks"][0]
        data["prior_pending_tasks"] = [{"id": task["id"], "dedup_key": task["dedup_key"]}]
        task["carried_forward"] = True
        self.assertTrue(validator.validate(data, AS_OF))
        task["id"] = "cloned-id"
        self.reject(data, "cloned")

    def test_rejects_dropped_or_retargeted_pending_work(self):
        data = queue(); task = data["tasks"][0]
        data["prior_pending_tasks"] = [{"id": task["id"], "dedup_key": "different-intent"}]
        task["carried_forward"] = True
        self.reject(data, "retargeted")
        data = queue(); data["prior_pending_tasks"] = [{"id": "old-task", "dedup_key": "old-intent"}]
        self.reject(data, "every prior")

    def test_rejects_candidate_and_expensive_cap_overruns(self):
        data = queue(); data["caps"]["candidate_cap"] = 0; data["caps"]["expensive_check_cap"] = 0
        self.reject(data, "candidate_cap")
        data = queue(); data["caps"]["expensive_check_cap"] = 0; data["tasks"][0]["expensive_check"] = True
        self.reject(data, "expensive")
        data = queue(); data["caps"]["candidate_cap"] = True
        self.reject(data, "integer")

    def test_execution_and_approval_cannot_be_authorized(self):
        for key in ("cms_write", "publish", "schedule"):
            data = queue(); data["execution"][key] = True
            self.reject(data, "false")
        for value in ("APPROVED", "AUTO_WRITE", True):
            data = queue(); data["tasks"][0]["approval_status"] = value
            self.reject(data, "PENDING")
        data = queue(); data["auto_publish"] = False
        self.reject(data, "unsupported")

    def test_rejects_unknown_or_executable_task_fields(self):
        for field in ("command", "publish", "auto_write", "growth"):
            data = queue(); data["tasks"][0][field] = "run"
            self.reject(data, "unsupported")

    def test_rejects_invalid_metrics_and_ctr(self):
        for value in (True, -1, float("nan"), float("inf"), "10", None):
            data = queue(); data["tasks"][0]["metrics"]["current"]["clicks"] = value
            self.reject(data, "finite")
        for value in (8, 0.5):
            data = queue(); data["tasks"][0]["metrics"]["current"]["ctr"] = value
            self.reject(data)
        data = queue(); data["tasks"][0]["metrics"]["current"]["position"] = 0
        self.reject(data, "at least 1")

    def test_rejects_clicks_exceeding_impressions_and_no_current_demand(self):
        data = queue(); data["tasks"][0]["metrics"]["current"]["clicks"] = 101
        self.reject(data, "cannot exceed")
        data = queue(); data["tasks"][0]["metrics"]["current"] = {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}
        self.reject(data, "current demand")

    def test_growth_must_match_known_nonzero_baseline(self):
        data = queue(); data["tasks"][0]["growth_pct"] = {"clicks": 100, "impressions": 25}
        self.assertTrue(validator.validate(data, AS_OF))
        data["tasks"][0]["growth_pct"]["clicks"] = 200
        self.reject(data, "match observed")
        for value in (None, 0):
            data = queue(); data["tasks"][0]["metrics"]["previous"] = {"clicks": value, "impressions": 80, "ctr": None, "position": 9}
            data["tasks"][0]["growth_pct"] = {"clicks": 100}
            self.reject(data, "known nonzero")

    def test_rejects_placeholders_and_missing_evidence(self):
        for field in ("owner", "source_or_cms_revision", "acceptance_criteria"):
            data = queue(); data["tasks"][0][field] = "REPLACE_ME"
            self.reject(data, "placeholder")
        data = queue(); data["tasks"][0]["evidence_refs"] = []
        self.reject(data, "evidence")
        data = queue(); data["tasks"][0]["checks"]["serp"]["evidence_refs"] = []
        self.reject(data, "evidence")

    def test_action_requires_every_review_field(self):
        for field in ("owner", "due", "checks", "metrics", "measurement_plan", "uncertainty", "source_or_cms_revision", "target_url", "problem_or_deliverable"):
            data = queue(); del data["tasks"][0][field]
            self.reject(data)

    def test_missing_new_page_checks_and_existing_owner_block_new_page(self):
        for field in validator.NEW_CHECKS:
            data = queue("NEW_PAGE_REVIEW"); del data["tasks"][0]["checks"][field]
            self.reject(data, "checks")
        data = queue("NEW_PAGE_REVIEW"); data["tasks"][0]["existing_owner_url"] = "https://example.com/current-owner"
        self.reject(data, "ownership")

    def test_checks_need_evidence_not_a_boolean_or_generic_string(self):
        for value in (True, "checked", None, {"status": "confirmed", "evidence_refs": [], "observed_date": AS_OF}):
            data = queue(); data["tasks"][0]["checks"]["serp"] = value
            self.reject(data)

    def test_due_policy_must_name_project_timezone(self):
        data = queue(); data["tasks"][0]["due"]["timezone"] = "UTC"
        self.reject(data, "timezone")
        data = queue(); data["tasks"][0]["due"]["policy"] = ""
        self.reject(data, "non-empty")
        data = queue(); data["tasks"][0]["due"]["date"] = "2026-09-01"
        self.reject(data, "past due")

    def test_carried_overdue_task_requires_explanation(self):
        data = queue(); task = data["tasks"][0]
        data["prior_pending_tasks"] = [{"id": task["id"], "dedup_key": task["dedup_key"]}]
        task["carried_forward"] = True; task["due"]["date"] = "2026-09-01"
        self.reject(data, "overdue_reason")
        task["overdue_reason"] = "Awaiting the owner's exact-diff review; keep original due date."
        self.assertTrue(validator.validate(data, AS_OF))

    def test_rejects_foreign_credentialed_and_executable_urls(self):
        for value in ("https://foreign.example/page", "javascript:publish()", "https://user:secret@example.com/page", "https://example.com/white space"):
            data = queue(); data["tasks"][0]["target_url"] = value
            self.reject(data)

    def test_measurement_stays_separate_and_unscheduled(self):
        for field, value in (("checkpoints_days", [7]), ("causality_claimed", True), ("schedule_created", True), ("metrics_separate", False), ("site_control_refs", [])):
            data = queue(); data["tasks"][0]["measurement_plan"][field] = value
            self.reject(data)

    def test_non_action_reasons_are_required(self):
        for outcome, field in (("HOLD", "hold_reason"), ("NEEDS_MORE_DATA", "hold_reason"), ("NO_ACTION", "no_action_reason")):
            data = queue(outcome); data["tasks"][0][field] = ""
            self.reject(data)

    def test_malformed_containers_fail_with_value_error(self):
        for field in ("scope", "windows", "caps", "execution", "review_policy"):
            for value in (None, [], "bad", True):
                data = queue(); data[field] = value
                self.reject(data)
        for field in ("metrics", "checks", "due", "measurement_plan"):
            data = queue(); data["tasks"][0][field] = None
            self.reject(data)
        for value in (None, [], 42, True):
            with self.assertRaises(ValueError):
                validator.validate(value, AS_OF)

    def test_cli_rejects_bad_json_utf8_and_container_shapes(self):
        for content in ("{", "null", "[]", json.dumps({**queue(), "scope": None})):
            result, output = self.cli(content)
            self.assertEqual(result.returncode, 2); self.assertFalse(output["valid"])
            self.assertFalse(output["execution_authority"])
        result, output = self.cli(b"\xff", binary=True)
        self.assertEqual(result.returncode, 2); self.assertFalse(output["valid"])

    def test_cli_valid_historical_artifact_never_grants_execution(self):
        result, output = self.cli(json.dumps(queue()))
        self.assertEqual(result.returncode, 0)
        self.assertTrue(output["valid"]); self.assertFalse(output["execution_authority"])
        result, output = self.cli(json.dumps(queue()), ["--as-of", "2026-10-20"])
        self.assertEqual(result.returncode, 2); self.assertIn("stale", output["error"])

    def test_malformed_task_outcomes_and_filters_are_clean_errors(self):
        for value in (None, [], {}, True):
            data = queue(); data['tasks'][0]['outcome'] = value
            self.reject(data, 'outcome')
            result, output = self.cli(json.dumps(data))
            self.assertEqual(result.returncode, 2); self.assertFalse(output['valid'])
        for field in ('dimension', 'operator'):
            data = queue(); data['scope']['filters'] = [{'dimension': 'country', 'operator': 'equals', 'expression': 'USA'}]
            data['scope']['filters'][0][field] = []
            self.reject(data, 'unsupported filter')

    def test_url_prefix_does_not_accept_lookalike_hostname(self):
        data = queue()
        for scope in (data['scope'], data['windows']['current']['scope'], data['windows']['previous']['scope']):
            scope['property'] = 'https://example.com'
        self.assertTrue(validator.validate(data, AS_OF))
        data['tasks'][0]['target_url'] = 'https://example.com.evil.example/page'
        self.reject(data, 'outside')

    def test_cli_rejects_duplicate_json_fields(self):
        result, output = self.cli('{"schema_version":"1.0","schema_version":"1.0"}')
        self.assertEqual(result.returncode, 2)
        self.assertIn('duplicate JSON field', output['error'])

    def test_template_is_not_a_valid_action_queue(self):
        asset = json.loads((ROOT / "assets/weekly-gsc-action-queue.json").read_text())
        self.assertEqual(asset["tasks"][0]["outcome"], "HOLD")
        with self.assertRaises(ValueError):
            validator.validate(asset, AS_OF)

    def test_docs_and_source_claims_are_bounded(self):
        text = (ROOT / "references/playbooks/maintenance/weekly-gsc-action-queue.md").read_text()
        for phrase in ("non-overlapping, equal-length", "Rising impressions alone", "No automatic CMS write", "Monday", "America/Los_Angeles", "PENDING", "gsc_pull.py", "unknown", "28", "56"):
            self.assertIn(phrase, text)
        audit = (ROOT / "references/audit-log/2026-10-12-weekly-gsc-action-queue.md").read_text()
        self.assertIn("2109259283523043469", audit)
        self.assertIn("not controlled, causal, or transferable proof", audit)

    def test_router_preserves_original_two_column_routes(self):
        lines = (ROOT / "SKILL.md").read_text().splitlines()
        rows = [line for line in lines if line.startswith("| Rank recurring content") or line.startswith("| Build a bounded offline weekly")]
        self.assertEqual(len(rows), 2)
        for line in rows:
            self.assertEqual(line.count("|"), 3)
        self.assertIn("content-opportunity-audit-and-measurement.md", rows[0])
        self.assertIn("weekly-gsc-action-queue.md", rows[1])

    def test_workflows_and_readme_expose_actual_validator_command(self):
        monitoring = (ROOT / "workflows/monitoring.md").read_text()
        self.assertIn("monitoring/<date>_weekly-gsc-action-queue.json", monitoring)
        self.assertIn("python3 scripts/weekly_gsc_actions.py", monitoring)
        self.assertIn("weekly-gsc-action-queue.md", (ROOT / "workflows/content-production.md").read_text())
        self.assertIn("scripts/weekly_gsc_actions.py", (ROOT / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
