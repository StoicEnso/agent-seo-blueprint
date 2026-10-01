"""Synthetic offline fixtures; no real-provider observations or network calls."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("local_check", ROOT / "scripts/local_ai_evidence_check.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def fixture():
    return {"version": 1, "applicability": "local_business", "limitations": ["Synthetic fixture; not live evidence."], "fact_checks": [], "source_statistics": [], "observations": [{"provider": "openai", "surface": "chatgpt_search", "exact_prompt": "Find a local plumber", "location_context": "Owner-supplied test area", "locale": "en-GB", "account_state": "test", "panel_version": "v1", "attempt_id": "one", "captured_at": "2026-10-01T01:00:00Z", "evidence_locator": "synthetic://one", "state": "returned", "target_mentioned": True, "owned_site_cited": False}]}


class LocalEvidenceTest(unittest.TestCase):
    def rejects(self, data):
        with self.assertRaises((ValueError, TypeError)):
            mod.validate(data)

    def test_empty_template(self):
        data = json.loads((ROOT / "assets/local-ai-evidence-ledger.json").read_text())
        self.assertEqual(mod.validate(data)["groups"], [])

    def test_single_run_is_not_proof(self):
        g = mod.validate(fixture())["groups"][0]
        self.assertTrue(g["insufficient_repeat_evidence"])
        self.assertEqual((g["business_mentions"], g["owned_site_citations"]), (1, 0))

    def test_no_answer_and_unavailable_denominators(self):
        data = fixture()
        base = data["observations"][0]
        data["observations"] += [{**base, "attempt_id": "two", "state": "no_answer", "target_mentioned": False, "owned_site_cited": False}, {**base, "attempt_id": "three", "state": "unavailable", "target_mentioned": None, "owned_site_cited": None}]
        g = mod.validate(data)["groups"][0]
        self.assertEqual((g["completed_attempts"], g["no_answer_attempts"], g["unavailable_attempts"]), (2, 1, 1))

    def test_three_runs_need_separate_days(self):
        data = fixture()
        base = data["observations"][0]
        data["observations"] += [{**base, "attempt_id": "two"}, {**base, "attempt_id": "three"}]
        self.assertTrue(mod.validate(data)["groups"][0]["insufficient_repeat_evidence"])
        data["observations"][-1]["captured_at"] = "2026-10-02T01:00:00Z"
        self.assertFalse(mod.validate(data)["groups"][0]["insufficient_repeat_evidence"])

    def test_context_changes_split_groups(self):
        for field, value in (("location_context", "Another area"), ("exact_prompt", "Different task"), ("locale", "en-US"), ("account_state", "signed_out"), ("panel_version", "v2")):
            with self.subTest(field=field):
                data = fixture(); data["observations"].append({**data["observations"][0], "attempt_id": "two", field: value})
                self.assertEqual(len(mod.validate(data)["groups"]), 2)

    def test_google_surfaces_split(self):
        data = fixture(); base = data["observations"][0]
        for i, surface in enumerate(("maps", "ai_mode", "ai_overviews")):
            data["observations"].append({**base, "attempt_id": str(i), "provider": "google", "surface": surface})
        self.assertEqual(len(mod.validate(data)["groups"]), 4)

    def test_duplicate_attempt_rejected(self):
        data = fixture(); data["observations"].append(copy.deepcopy(data["observations"][0])); self.rejects(data)

    def test_unavailable_is_not_absence(self):
        data = fixture(); data["observations"][0].update(state="unavailable", target_mentioned=False, owned_site_cited=False); self.rejects(data)

    def test_no_answer_cannot_claim_citation(self):
        data = fixture(); data["observations"][0].update(state="no_answer", owned_site_cited=True); self.rejects(data)

    def test_missing_context_rejected(self):
        for key in mod.CONTEXT:
            data = fixture(); del data["observations"][0][key]; self.rejects(data)

    def test_pair_mismatch_rejected(self):
        data = fixture(); data["observations"][0]["surface"] = "maps"; self.rejects(data)

    def test_timestamp_requires_utc(self):
        for stamp in ("2026-10-01T01:00:00", "2026-10-01T01:00:00+01:00", "not-a-date"):
            data = fixture(); data["observations"][0]["captured_at"] = stamp; self.rejects(data)

    def test_nonlocal_and_needs_review_do_not_count(self):
        for value in ("not_applicable", "needs_review"):
            data = fixture(); data["applicability"] = value; self.rejects(data)

    def test_source_share_denominator_not_interchangeable(self):
        data = fixture(); data["source_statistics"] = [{"source_url": "https://example.test/study", "source_date": "2026-09-16", "section": "Key findings", "metric": "unique_domain_share", "denominator": "unique_domains", "reported_percent": 93, "limitation": "Attributed observation, not causality."}]
        self.assertTrue(mod.validate(data)["valid"])
        data["source_statistics"][0]["denominator"] = "citation_instances"; self.rejects(data)

    def test_invalid_percent_rejected(self):
        for value in (-1, 101, True, "93", float("nan")):
            data = fixture(); data["source_statistics"] = [{"source_url": "https://example.test", "source_date": "2026-09-16", "section": "test", "metric": "citation_volume_share", "denominator": "citation_instances", "reported_percent": value, "limitation": "Test"}]; self.rejects(data)

    def test_facts_are_draft_only(self):
        data = fixture(); data["fact_checks"] = [{"field": "services", "evidence_locator": "synthetic://fact", "proposed_action": "Draft correction", "status": "verified", "action_state": "draft_only"}]
        self.assertTrue(mod.validate(data)["valid"])
        data["fact_checks"][0]["action_state"] = "publish"; self.rejects(data)

    def test_malformed_containers_rejected(self):
        for key in ("limitations", "fact_checks", "source_statistics", "observations"):
            data = fixture(); data[key] = None; self.rejects(data)

    def test_docs_keep_source_and_action_boundaries(self):
        doc = (ROOT / "references/playbooks/maintenance/local-ai-first-party-evidence.md").read_text()
        for phrase in ("93%", "42%", "200,875", "200,085", "1,342", "not causal proof", "doorway", "draft", "not automatically a local service business", "unavailable", "4–8 week", "DR50+"):
            self.assertIn(phrase, doc)
        self.assertIn("local-ai-first-party-evidence.md", (ROOT / "SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
