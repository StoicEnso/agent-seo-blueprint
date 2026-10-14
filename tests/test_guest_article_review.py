import ast
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("guest_article_review", ROOT / "scripts/guest_article_review.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
NOW = datetime(2026, 10, 14, 21, 0, tzinfo=timezone.utc)


class GuestArticleReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = json.loads((ROOT / "assets/guest-article-opportunity-ledger.json").read_text())
        self.row = self.data["opportunities"][0]

    def check(self):
        return MODULE.check_ledger(self.data, self.root, NOW)

    def verified(self):
        for eid, url, text in [
            ("guidelines", "https://example.org/contribute", "We accept original expert articles. Editors review all submissions. There is no submission or publication fee."),
            ("sample", "https://example.org/garden-planning", "An original guide to planning a garden and discussing its limits.")
        ]:
            file = self.root / (eid + ".txt")
            file.write_text(text)
            self.data["evidence"].append({"id": eid, "url": url, "captured_at": "2026-10-14T20:00:00Z", "path": file.name,
                                          "sha256": hashlib.sha256(file.read_bytes()).hexdigest(), "excerpt": text})
        self.row.update(status="VERIFIED_EDITORIAL", guidelines_url="https://example.org/contribute", route_url="https://example.org/contribute",
                        sample_url="https://example.org/garden-planning", checked_at="2026-10-14T20:30:00Z", evidence_ids=["guidelines", "sample"],
                        editorial_review_observed=True)
        return self.row

    def test_discovered_template_stays_unverified(self):
        result = self.check()
        self.assertEqual(result["rows"][0]["verdict"], "MORE_EVIDENCE_NEEDED")
        self.assertFalse(result["outreach_authorized"])

    def test_valid_packet_is_draft_only(self):
        self.verified()
        result = self.check()
        self.assertEqual(result["rows"][0]["verdict"], "DRAFT_REVIEW_READY")
        self.assertEqual(result["network_requests"], 0)
        self.assertFalse(result["rows"][0]["outreach_authorized"])

    def test_unknown_cost_is_not_free(self):
        self.verified()
        self.assertFalse(self.check()["rows"][0]["cost_confirmed_free"])

    def test_explicit_free_requires_a_saved_statement(self):
        self.verified().update(cost_state="EXPLICITLY_FREE", free_basis="There is no submission or publication fee.")
        self.assertTrue(self.check()["rows"][0]["cost_confirmed_free"])

    def test_missing_free_basis_fails(self):
        self.verified().update(cost_state="EXPLICITLY_FREE")
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_invented_free_basis_fails(self):
        self.verified().update(cost_state="EXPLICITLY_FREE", free_basis="We promise a free followed link.")
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_paid_and_membership_remain_conditional(self):
        self.verified()
        for state in ("PAID", "MEMBERSHIP_REQUIRED"):
            self.row["cost_state"] = state
            with self.assertRaises(MODULE.ReviewError): self.check()
            self.row.update(status="CONDITIONAL", reason="Needs owner cost/eligibility review.")
            self.assertEqual(self.check()["rows"][0]["verdict"], "MORE_EVIDENCE_NEEDED")
            self.row["status"] = "VERIFIED_EDITORIAL"

    def test_missing_sample_evidence_fails(self):
        self.verified()["evidence_ids"] = ["guidelines"]
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_missing_route_evidence_fails(self):
        self.verified()["route_url"] = "https://example.org/another-route"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_external_route_does_not_imply_first_party_proof(self):
        self.verified()["route_url"] = "https://other.example.org.evil.org/form"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_missing_editorial_review_fails(self):
        self.verified()["editorial_review_observed"] = False
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_missing_author_or_claim_limits_fails(self):
        self.verified()
        for field in ("author_basis", "claim_limits"):
            saved = self.row[field]; self.row[field] = ""
            with self.assertRaises(MODULE.ReviewError): self.check()
            self.row[field] = saved

    def test_stale_check_fails(self):
        self.verified()["checked_at"] = "2026-09-01T00:00:00Z"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_stale_evidence_fails_even_with_fresh_checked_date(self):
        self.verified(); self.data["evidence"][0]["captured_at"] = "2026-09-01T00:00:00Z"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_future_check_and_capture_fail(self):
        self.verified(); self.row["checked_at"] = "2026-10-15T00:00:00Z"
        with self.assertRaises(MODULE.ReviewError): self.check()
        self.row["checked_at"] = "2026-10-14T20:30:00Z"
        self.data["evidence"][0]["captured_at"] = "2026-10-15T00:00:00Z"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_naive_or_bad_timestamps_fail(self):
        for value in ("2026-10-14", "2026-10-14T20:00:00", "yesterday", None):
            with self.assertRaises(MODULE.ReviewError): MODULE.stamp(value)

    def test_hash_mismatch_fails(self):
        self.verified(); (self.root / "guidelines.txt").write_text("Changed rules")
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_excerpt_must_exist(self):
        self.verified(); self.data["evidence"][0]["excerpt"] = "Invented rule"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_whitespace_variation_in_excerpt_is_allowed(self):
        self.verified(); self.data["evidence"][0]["excerpt"] = "Editors  review\nall submissions."
        self.assertTrue(self.check()["valid"])

    def test_evidence_escape_and_absolute_paths_fail(self):
        self.verified()
        for value in ("../outside.txt", str(self.root / "guidelines.txt")):
            self.data["evidence"][0]["path"] = value
            with self.assertRaises(MODULE.ReviewError): self.check()

    def test_symlink_escape_fails(self):
        self.verified()
        with tempfile.TemporaryDirectory() as outside:
            file = Path(outside) / "outside.txt"; file.write_text("outside")
            link = self.root / "escape.txt"; link.symlink_to(file)
            self.data["evidence"][0]["path"] = link.name
            with self.assertRaises(MODULE.ReviewError): self.check()

    def test_duplicate_evidence_id_fails(self):
        self.verified(); self.data["evidence"].append(copy.deepcopy(self.data["evidence"][0]))
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_duplicate_row_or_destination_fails(self):
        extra = copy.deepcopy(self.row); self.data["opportunities"].append(extra)
        with self.assertRaises(MODULE.ReviewError): self.check()
        extra["id"] = "another"; extra["domain"] = "www.example.org"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_same_publisher_for_distinct_product_is_not_duplicate(self):
        extra = copy.deepcopy(self.row); extra.update(id="another", product="Another product with a distinct reader reason")
        self.data["opportunities"].append(extra)
        self.assertEqual(len(self.check()["rows"]), 2)

    def test_hard_failure_requires_rejected_state(self):
        self.row["risk_flags"] = ["required_link_exchange"]
        with self.assertRaises(MODULE.ReviewError): self.check()
        self.row.update(status="REJECTED", reason="Requires an exchange")
        self.assertEqual(self.check()["rows"][0]["verdict"], "DO_NOT_PITCH")

    def test_no_authority_send_or_placement_claims(self):
        for field, value in (("outreach_status", "SENT"), ("link_outcome", "FOLLOWED_LINK_PLACED")):
            saved = self.row[field]; self.row[field] = value
            with self.assertRaises(MODULE.ReviewError): self.check()
            self.row[field] = saved
        self.data["outreach_authorized"] = True
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_url_checks_reject_unsafe_destinations(self):
        for url in ("http://example.org/x", "https://user:pass@example.org/", "https://localhost/", "https://127.0.0.1/", "https://[::1]/",
                    "https://foo.internal/", "https://example.org:8443/", "https://example.org/x#part", "javascript:alert(1)", "https://example.org/with space", "https://-bad.org/"):
            with self.subTest(url=url), self.assertRaises(MODULE.ReviewError): MODULE.hostname(url)

    def test_public_subdomain_is_first_party(self):
        self.assertTrue(MODULE.first_party("https://mag.example.org/contribute", "example.org"))
        self.assertFalse(MODULE.first_party("https://notexample.org/contribute", "example.org"))

    def test_queries_are_deduplicated_and_never_run(self):
        result = MODULE.queries(["garden design", "garden design"])
        self.assertEqual(len(result["queries"]), 3)
        self.assertEqual(result["queries"][0]["query"], 'intitle:"write for us" "garden design"')
        self.assertEqual(result["network_requests"], 0)
        self.assertFalse(result["outreach_authorized"])

    def test_query_injection_or_overlong_batch_fails(self):
        for values in (["bad\nquery"], ['bad"quote'], ["bad\\slash"], ["\x00bad"], [], ["x"] * 11, ["x" * 101]):
            with self.assertRaises(MODULE.ReviewError): MODULE.queries(values)

    def test_duplicate_json_keys_and_nonfinite_values_fail(self):
        file = self.root / "bad.json"
        for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{broken'):
            file.write_text(text)
            with self.assertRaises(MODULE.ReviewError): MODULE.load_json(file)

    def test_invalid_schema_and_states_fail(self):
        for value in (True, "1", 2, None):
            self.data["schema_version"] = value
            with self.assertRaises(MODULE.ReviewError): self.check()
        self.data["schema_version"] = 1
        self.row["status"] = "APPROVED"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_malformed_objects_fail_closed(self):
        for payload in (None, [], True, "bad"):
            with self.assertRaises(MODULE.ReviewError): MODULE.check_ledger(payload, self.root, NOW)
        for field in ("status", "cost_state", "link_policy"):
            saved = self.row[field]
            for value in ([], {}, True, None):
                self.row[field] = value
                with self.assertRaises(MODULE.ReviewError): self.check()
            self.row[field] = saved
        for value in (True, "30", [], None, 0, 91):
            with self.assertRaises(MODULE.ReviewError): MODULE.check_ledger(self.data, self.root, NOW, value)
        for value in (None, "now", datetime(2026, 10, 14)):
            with self.assertRaises(MODULE.ReviewError): MODULE.check_ledger(self.data, self.root, value)
        for value in (None, 1, "garden"):
            with self.assertRaises(MODULE.ReviewError): MODULE.queries(value)

    def test_free_claim_on_unverified_row_also_needs_current_first_party_proof(self):
        self.row["cost_state"] = "EXPLICITLY_FREE"
        with self.assertRaises(MODULE.ReviewError): self.check()
        self.verified().update(status="CONDITIONAL", reason="Author review pending.", cost_state="EXPLICITLY_FREE",
                               free_basis="There is no submission or publication fee.")
        self.assertTrue(self.check()["rows"][0]["cost_confirmed_free"])
        self.data["evidence"][0]["url"] = "https://unrelated.example.net/contribute"
        with self.assertRaises(MODULE.ReviewError): self.check()

    def test_cli_smoke_and_structured_errors(self):
        import subprocess
        import sys
        script = str(ROOT / "scripts/guest_article_review.py")
        def run(*args):
            return subprocess.run([sys.executable, script, *args], capture_output=True, text=True)
        result = run("queries", "--keyword", "garden design")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(json.loads(result.stdout)["queries"]), 3)
        file = self.root / "ledger.json"
        file.write_text(json.dumps(self.data))
        result = run("validate", str(file), "--as-of", NOW.isoformat())
        self.assertEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)["outreach_authorized"])
        for text in ("[]", '{"schema_version":1,"outreach_authorized":true}', "{broken"):
            file.write_text(text)
            result = run("validate", str(file), "--as-of", NOW.isoformat())
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stderr)["valid"])
            self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(run("validate", str(self.root / "absent.json")).returncode, 2)
        self.assertEqual(run("validate", str(file), "--as-of", "yesterday").returncode, 2)

    def test_code_has_no_external_execution_or_network_client(self):
        tree = ast.parse((ROOT / "scripts/guest_article_review.py").read_text())
        imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        imported |= {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        self.assertFalse(imported & {"requests", "urllib.request", "subprocess", "smtplib", "socket", "http.client"})
        self.assertFalse(any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval"} for node in ast.walk(tree)))


class GuestArticleDocsTests(unittest.TestCase):
    def test_router_workflow_and_template_are_discoverable(self):
        for file in ("SKILL.md", "workflows/authority-and-links.md", "README.md"):
            text = (ROOT / file).read_text()
            self.assertIn("guest-article-discovery-and-validation", text)
            self.assertIn("guest_article_review.py", text)
        self.assertIn("guest-article-opportunity-ledger.json", (ROOT / "SKILL.md").read_text())

    def test_playbook_preserves_core_boundaries(self):
        text = (ROOT / "references/playbooks/authority/guest-article-discovery-and-validation.md").read_text()
        for phrase in ("Unknown cost is not free", "Never send without explicit per-batch approval", "DRAFT_REVIEW_READY", "not a verified opportunity", "Temporal sequence is not causation", 'rel="sponsored"', "not a directory-submission workflow"):
            self.assertIn(phrase, text)

    def test_audit_keeps_pilot_and_source_claims_separate(self):
        text = (ROOT / "references/audit-log/2026-10-14-guest-article-discovery.md").read_text()
        self.assertIn("2110388370094633204", text)
        self.assertIn("not acceptance", text)
        self.assertIn("unknown", text.lower())


if __name__ == "__main__":
    unittest.main()
