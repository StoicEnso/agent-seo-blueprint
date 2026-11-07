"""Offline documentation/asset contract checks; not live collector or ranking tests."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = "references/playbooks/maintenance/content-opportunity-audit-and-measurement.md"


class GscBingCoverageDocsTest(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / PLAYBOOK).read_text(encoding="utf-8")
        self.template = json.loads((ROOT / "assets/gsc-bing-query-coverage.json").read_text(encoding="utf-8"))

    def test_template_is_empty_nonexecuting_review(self):
        self.assertEqual(self.template["mode"], "draft_only")
        self.assertEqual(self.template["clusters"], [])
        self.assertFalse(self.template["decision"]["website_write_allowed"])
        self.assertFalse(self.template["decision"]["indexing_submission_allowed"])
        self.assertEqual(self.template["decision"]["approval"], "not_requested")

    def test_missing_sources_and_metrics_default_to_unknown(self):
        for engine in ("gsc", "bing"):
            self.assertEqual(self.template["sources"][engine]["status"], "not_requested")
            observation = self.template["cluster_template"]["observations"][engine]
            for field in ("clicks", "impressions", "ctr", "avg_position"):
                self.assertIsNone(observation[field])
            self.assertEqual(observation["metric_status"], "unavailable")
        self.assertIn("unknown, not zero", self.text)

    def test_scope_retains_page_and_provider_boundaries(self):
        for source in self.template["sources"].values():
            for field in ("property", "report_surface", "page_filter", "date_start", "date_end", "timezone", "country", "device", "search_type", "data_finality", "row_limit", "pagination_complete", "raw_export", "failure_reason"):
                self.assertIn(field, source)
        self.assertIn("A domain-wide query list is not evidence", self.text)
        self.assertIn("unsupported dimensions as unavailable", self.text)

    def test_discovery_union_is_not_metric_blending(self):
        for phrase in ("separate engine metrics", "never average their positions or CTRs", "not the engine's complete query universe", "privacy", "zero impressions gives undefined CTR", "overlapping periods"):
            self.assertIn(phrase, self.text)
        self.assertNotIn("combined_ctr", self.template["cluster_template"])

    def test_coverage_requires_quotes_and_research_only_states(self):
        for status in ("covered_well", "covered_weakly", "not_covered", "wrong_intent", "unverified"):
            self.assertIn("`" + status + "`", self.text)
        cluster = self.template["cluster_template"]
        self.assertEqual(cluster["coverage"]["status"], "unverified")
        self.assertEqual(cluster["disposition"], "research_only")
        self.assertIn("page_quote", cluster["coverage"])

    def test_serp_evidence_is_engine_specific_and_not_assumed(self):
        for phrase in ("named engine", "exact query", "observation", "not_checked", "Do not infer Google intent from a Bing result"):
            self.assertIn(phrase, self.text)
        self.assertEqual(self.template["cluster_template"]["serp_status_by_engine"], {"gsc": "not_checked", "bing": "not_checked"})

    def test_priority_does_not_predict_gains_or_diagnose_ctr_alone(self):
        for phrase in ("review priority", "not a universal quick-win rule", "not automatically a title/meta defect", "Do not use a universal CTR cutoff"):
            self.assertIn(phrase, self.text)

    def test_write_submission_and_measurement_gates_remain(self):
        for phrase in ("exact write", "separate approval-gated action", "stale-revision", "submission receipt does not prove", "Google's restricted Indexing API", "+28 and +56 days"):
            self.assertIn(phrase, self.text)
        self.assertEqual(self.template["measurement"]["days_after_approved_change"], [28, 56])
        self.assertFalse(self.template["measurement"]["causality_claimed"])
        self.assertFalse(self.template["measurement"]["schedule_created"])

    def test_router_workflows_and_gsc_reference_connect_the_extension(self):
        for file in ("SKILL.md", "workflows/monitoring.md", "workflows/content-production.md", "references/integrations/gsc.md"):
            text = (ROOT / file).read_text(encoding="utf-8")
            self.assertIn("content-opportunity-audit-and-measurement.md", text)
            self.assertIn("Bing", text)
        self.assertIn("gsc-bing-query-coverage.json", (ROOT / "SKILL.md").read_text())
        self.assertIn("gsc-bing-query-coverage.json", (ROOT / "workflows/monitoring.md").read_text())

    def test_bing_reference_does_not_claim_a_collector_or_api(self):
        text = (ROOT / "references/integrations/bing.md").read_text()
        for phrase in ("not a new API client", "page-query mapping", "JavaScript shell", "not in public PRs", "approval", "partial/unavailable"):
            self.assertIn(phrase, text)
        self.assertFalse((ROOT / "scripts/bing_pull.py").exists())

    def test_source_audit_narrows_claims(self):
        text = (ROOT / "references/audit-log/2026-11-07-bing-gsc-query-coverage.md").read_text()
        for phrase in ("2118634208411185175", "not a forecast", "ends mid-sentence", "No customer account", "not rankings or live integration behavior"):
            self.assertIn(phrase, text)

    def test_example_discloses_synthetic_data_and_rejected_rows(self):
        text = (ROOT / "examples/gsc-bing-query-coverage.md").read_text()
        for phrase in ("Synthetic example only", "wrong_intent", "unverified", "covered_well", "Bing authentication fails", "research-only", "16/800 = 2%", "3/120 = 2.5%"):
            self.assertIn(phrase, text)
        self.assertEqual(16 / 800, .02)
        self.assertEqual(3 / 120, .025)

    def test_readme_integration_inventory_matches_disk(self):
        count = len(list((ROOT / "references/integrations").glob("*.md")))
        self.assertEqual(count, 9)
        self.assertIn(f"**{count} integration references**", (ROOT / "README.md").read_text())

    def test_extension_file_references_resolve(self):
        paths = ["assets/gsc-bing-query-coverage.json", "examples/gsc-bing-query-coverage.md", "references/integrations/bing.md"]
        for path in paths:
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertTrue(any(path in (ROOT / owner).read_text() for owner in (PLAYBOOK, "SKILL.md", "README.md")), path)


if __name__ == "__main__":
    unittest.main()
