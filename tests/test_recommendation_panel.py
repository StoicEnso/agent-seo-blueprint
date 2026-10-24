import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("recommendation_panel", ROOT / "scripts/recommendation_panel.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
TEMPLATE = ROOT / "assets/buyer-recommendation-panel.json"


def panel():
    result = json.loads(TEMPLATE.read_text())
    result.update(panel_id="synthetic-panel-v1", brand_entity_id="example")
    result["prompt"] = {"id": "q1", "version": 1, "text": "Who should I hire for this job?", "locale": "en-GB", "language": "en"}
    return result


def answer(p, slot="chatgpt-1", label="primary", **changes):
    planned = next(row for row in p["planned_runs"] if row["slot_id"] == slot)
    row = {
        **planned, "model": "not_exposed", "account_state": "logged_out; fresh_chat",
        "locale": "en-GB", "language": "en", "captured_at": "2026-10-25T10:00:00Z",
        "prompt_text": p["prompt"]["text"], "prompt_version": 1,
        "status": "ok", "review_state": "verified", "recommendation": label,
        "raw_answer": "For this job, Example is my sole first choice.",
        "classification_quote": "Example is my sole first choice.",
        "cited": False, "evidence_locator": f"synthetic/{slot}.txt",
    }
    row.update(changes)
    p["observations"].append(row)
    return row


def context(result, provider="chatgpt"):
    return next(r for r in result["provider_surfaces"] if r["provider"] == provider)["contexts"][0]


class RecommendationArithmeticTest(unittest.TestCase):
    def test_unconfigured_template_fails_closed(self):
        with self.assertRaises(ValueError):
            MOD.summarize(json.loads(TEMPLATE.read_text()))

    def test_empty_configured_panel_is_not_zero_visibility(self):
        r = MOD.summarize(panel())
        self.assertEqual(r["coverage"], {"planned": 9, "observed": 0, "not_run": 9})
        self.assertTrue(all(not x["contexts"] for x in r["provider_surfaces"]))

    def test_one_primary_has_one_denominator_not_nine(self):
        p = panel(); answer(p)
        r = MOD.summarize(p); c = context(r)
        self.assertEqual(c["classifiable"], 1)
        self.assertEqual(c["strict_primary_rate"], 1)
        self.assertEqual(r["coverage"]["not_run"], 8)
        self.assertNotIn("all_providers", r)

    def test_ties_and_options_do_not_become_sole_picks(self):
        p = panel()
        answer(p, label="primary"); answer(p, "chatgpt-2", "tied_primary"); answer(p, "chatgpt-3", "option")
        c = context(MOD.summarize(p))
        self.assertEqual(c["strict_primary_rate"], 1 / 3)
        self.assertEqual(c["labels"]["tied_primary"], 1)
        self.assertEqual(c["labels"]["option"], 1)

    def test_mention_and_citation_are_not_recommendations(self):
        p = panel(); answer(p, label="mention_only", cited=True)
        c = context(MOD.summarize(p))
        self.assertEqual(c["strict_primary_picks"], 0)
        self.assertEqual(c["cited_classifiable_runs"], 1)

    def test_only_observed_reviewed_absence_is_zero(self):
        p = panel(); answer(p, label="absent", raw_answer="Choose the other company.", classification_quote=None)
        c = context(MOD.summarize(p))
        self.assertEqual(c["strict_primary_rate"], 0)
        self.assertEqual(c["labels"]["absent"], 1)

    def test_all_unclear_rate_is_null(self):
        p = panel(); answer(p, label="unclear")
        c = context(MOD.summarize(p))
        self.assertIsNone(c["strict_primary_rate"])
        self.assertEqual(c["excluded"], 1)

    def test_unreviewed_positive_is_excluded(self):
        p = panel(); answer(p, review_state="needs_review")
        self.assertIsNone(context(MOD.summarize(p))["strict_primary_rate"])

    def test_failures_and_partials_are_not_absences(self):
        for status in MOD.STATUSES - {"ok"}:
            with self.subTest(status=status):
                p = panel(); answer(p, label="unclear", status=status, reason="synthetic unavailable evidence", raw_answer=None, classification_quote=None)
                c = context(MOD.summarize(p))
                self.assertIsNone(c["strict_primary_rate"])
                self.assertEqual(c["labels"]["absent"], 0)

    def test_failed_positive_label_rejected(self):
        p = panel(); answer(p, status="partial", reason="truncated")
        with self.assertRaises(ValueError): MOD.summarize(p)

    def test_missing_failure_reason_rejected(self):
        p = panel(); answer(p, label="unclear", status="blocked")
        with self.assertRaises(ValueError): MOD.summarize(p)

    def test_provider_surfaces_stay_separate(self):
        p = panel(); answer(p); answer(p, "gemini-1", "absent"); answer(p, "google-1", "option")
        r = MOD.summarize(p)
        self.assertEqual(context(r)["strict_primary_rate"], 1)
        self.assertEqual(context(r, "gemini")["strict_primary_rate"], 0)
        self.assertEqual(len(r["provider_surfaces"]), 3)

    def test_model_and_account_drift_split_contexts(self):
        for field, value in [("model", "changed_model"), ("account_state", "signed_in")]:
            with self.subTest(field=field):
                p = panel(); answer(p); answer(p, "chatgpt-2", **{field: value})
                results = next(x for x in MOD.summarize(p)["provider_surfaces"] if x["provider"] == "chatgpt")
                self.assertEqual(len(results["contexts"]), 2)
                self.assertTrue(all(c["classifiable"] == 1 for c in results["contexts"]))

    def test_duplicate_observation_rejected(self):
        p = panel(); answer(p); answer(p)
        with self.assertRaises(ValueError): MOD.summarize(p)

    def test_duplicate_plan_rejected(self):
        p = panel(); p["planned_runs"].append(copy.deepcopy(p["planned_runs"][0]))
        with self.assertRaises(ValueError): MOD.summarize(p)

    def test_unplanned_observation_rejected(self):
        p = panel(); row = answer(p); row["slot_id"] = "unplanned"
        with self.assertRaises(ValueError): MOD.summarize(p)

    def test_surface_substitution_rejected(self):
        p = panel(); answer(p, surface="api")
        with self.assertRaises(ValueError): MOD.summarize(p)

    def test_prompt_and_locale_drift_rejected(self):
        for changes in [{"prompt_text": "Who should I hire? Example?"}, {"prompt_version": 2}, {"locale": "en-US"}, {"language": "fr"}]:
            with self.subTest(changes=changes):
                p = panel(); answer(p, **changes)
                with self.assertRaises(ValueError): MOD.summarize(p)

    def test_timestamp_needs_timezone(self):
        for stamp in ["2026-10-25T10:00:00", "yesterday", "2026-10-25"]:
            with self.subTest(stamp=stamp):
                p = panel(); answer(p, captured_at=stamp)
                with self.assertRaises(ValueError): MOD.summarize(p)

    def test_raw_and_quoted_evidence_required(self):
        for changes in [{"raw_answer": ""}, {"evidence_locator": ""}, {"classification_quote": ""}, {"classification_quote": "Invented quote"}]:
            with self.subTest(changes=changes):
                p = panel(); answer(p, **changes)
                with self.assertRaises(ValueError): MOD.summarize(p)

    def test_unknown_status_review_and_label_rejected(self):
        for changes in [{"status": "success"}, {"review_state": "auto_pass"}, {"recommendation": "first_in_list"}, {"cited": "true"}]:
            with self.subTest(changes=changes):
                p = panel(); answer(p, **changes)
                with self.assertRaises(ValueError): MOD.summarize(p)

    def test_malformed_structures_rejected(self):
        for value in [None, [], {"schema_version": True}, {"schema_version": 2}]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError): MOD.summarize(value)
        for field, value in [("planned_runs", []), ("planned_runs", ["bad"]), ("observations", ["bad"]), ("observations", None)]:
            with self.subTest(field=field, value=value):
                p = panel(); p[field] = value
                with self.assertRaises(ValueError): MOD.summarize(p)

    def test_script_does_not_mutate_evidence(self):
        p = panel(); answer(p); before = copy.deepcopy(p)
        MOD.summarize(p)
        self.assertEqual(p, before)

    def test_no_statistical_or_business_result_is_invented(self):
        p = panel(); answer(p)
        r = MOD.summarize(p)
        self.assertNotIn("revenue", r)
        self.assertNotIn("conversion_rate", r)
        self.assertNotIn("wilson_95", context(r))
        self.assertIn("no population inference", " ".join(r["limitations"]))

    def test_cli_success_and_input_is_unchanged(self):
        p = panel(); answer(p)
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            src = Path(tmp) / "panel.json"; out = Path(tmp) / "out.json"
            src.write_text(json.dumps(p)); before = src.read_bytes()
            run = subprocess.run([sys.executable, str(ROOT / "scripts/recommendation_panel.py"), str(src), "--out", str(out)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertEqual(src.read_bytes(), before)
            self.assertEqual(context(json.loads(out.read_text()))["strict_primary_picks"], 1)

    def test_cli_rejects_same_output_and_malformed_json(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            src = Path(tmp) / "panel.json"; src.write_text(json.dumps(panel())); before = src.read_bytes()
            run = subprocess.run([sys.executable, str(ROOT / "scripts/recommendation_panel.py"), str(src), "--out", str(src)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(src.read_bytes(), before)
            src.write_text("invalid json")
            run = subprocess.run([sys.executable, str(ROOT / "scripts/recommendation_panel.py"), str(src)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(json.loads(run.stdout)["status"], "error")


class RecommendationDocsTest(unittest.TestCase):
    def test_routes_and_files_are_connected(self):
        for rel in ["SKILL.md", "README.md", "workflows/geo-audit.md", "workflows/ai-answer-visibility-loop.md"]:
            text = (ROOT / rel).read_text()
            self.assertIn("buyer-recommendation-panel.json", text)
            self.assertIn("recommendation_panel.py", text)
        p = (ROOT / "references/playbooks/maintenance/cross-platform-ai-citation-loop.md").read_text()
        for phrase in ["unverified source claims", "8x", "57%", "$199,392", "tied_primary", "Incognito", "consented", "masked", "AI Assistant", "before/after", "not run", "strict primary picks / classifiable answers", "Do not pool"]:
            self.assertIn(phrase, p)

    def test_template_is_inert_and_has_nine_unique_slots(self):
        t = json.loads(TEMPLATE.read_text())
        self.assertEqual(t["observations"], [])
        self.assertEqual(t["status"], "DRAFT_NOT_RUN")
        self.assertIsNone(t["brand_entity_id"])
        self.assertEqual(len({p["slot_id"] for p in t["planned_runs"]}), 9)
        for key in ["publication", "tracking_installation", "spend", "scheduling"]:
            self.assertEqual(t["approval"][key], "NOT_GRANTED")


if __name__ == "__main__":
    unittest.main()
