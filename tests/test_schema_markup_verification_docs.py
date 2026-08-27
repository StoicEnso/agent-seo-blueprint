import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SchemaMarkupVerificationDocsTest(unittest.TestCase):
    def test_reference_preserves_validation_and_claim_boundaries(self):
        text = (ROOT / "references/playbooks/content/schema-types-reference.md").read_text(encoding="utf-8")
        required = [
            "Evidence-Gated Verification Loop",
            "Schema.org validity is not Google rich-result eligibility",
            "no extra technical requirements or special Schema.org markup",
            "Generated markup is a draft, not production evidence",
            "validator success does not prove rankings",
            "Search appearance, ordinary Search performance, named AI-provider observations, referrals, conversions, and revenue",
            "bounded pilot",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_evidence_review_narrows_source_claims(self):
        text = (ROOT / "references/audit-log/2026-08-27-schema-markup-verification-loop.md").read_text(encoding="utf-8")
        required = [
            "practitioner and vendor evidence",
            "Entity optimized schema",
            "Generated schema is production-ready by default",
            "A clean validator result proves rankings, rich-result display, or AI citation",
            "Do not create a tool-specific dependency on Schemawriter.ai",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_ledger_keeps_evidence_lanes_separate(self):
        with (ROOT / "assets/structured-data-verification-ledger.csv").open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle))
        required = {
            "page_url",
            "template",
            "schema_type",
            "source_or_rendered",
            "visible_content_match",
            "google_feature_supported",
            "rich_results_test_status",
            "schemaorg_validator_status",
            "search_appearance_baseline",
            "ai_observation_baseline",
            "deployment_state",
            "review_status",
        }
        self.assertTrue(required.issubset(set(header)))

    def test_router_and_workflows_are_wired(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        site_audit = (ROOT / "workflows/site-audit.md").read_text(encoding="utf-8")
        technical = (ROOT / "workflows/technical-seo-maintenance.md").read_text(encoding="utf-8")
        for text in [skill, site_audit, technical]:
            self.assertIn("structured-data-verification-ledger.csv", text)
            self.assertIn("schema-types-reference.md", text)
        self.assertIn("read-only until the user approves the exact deployment", technical)


if __name__ == "__main__":
    unittest.main()
