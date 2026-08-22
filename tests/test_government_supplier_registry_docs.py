import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GovernmentSupplierRegistryDocsTests(unittest.TestCase):
    def test_playbook_separates_claims_rules_and_link_outcomes(self):
        playbook = (
            ROOT
            / "references"
            / "playbooks"
            / "authority"
            / "government-supplier-registry-profiles.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Claim split", playbook)
        self.assertIn("Creator claim", playbook)
        self.assertIn("Registry-owner fact", playbook)
        self.assertIn("Observed link outcome", playbook)
        self.assertIn("Genuine procurement purpose", playbook)
        self.assertIn("REJECT_NO_PROCUREMENT_INTENT", playbook)
        self.assertIn("rendered destination `href`", playbook)
        self.assertIn("human must review every representation and declaration", playbook)

    def test_playbook_corrects_us_and_uk_overclaims(self):
        playbook = (
            ROOT
            / "references"
            / "playbooks"
            / "authority"
            / "government-supplier-registry-profiles.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Unique Entity ID", playbook)
        self.assertIn("physically located and operate in the US", playbook)
        self.assertIn("UK Central Digital Platform", playbook)
        self.assertIn("cannot be freely accessed", playbook)
        self.assertIn("Registration alone does not create a public backlink", playbook)
        self.assertIn("do not use SAM.gov", playbook)

    def test_tracker_keeps_eligibility_approval_and_live_proof_separate(self):
        path = ROOT / "assets" / "government-supplier-registry-opportunities.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            self.assertEqual(list(reader), [])

        self.assertTrue(
            {
                "source_claim_url",
                "real_procurement_intent",
                "eligibility_status",
                "eligibility_evidence",
                "route_class",
                "required_attestations",
                "authorized_reviewer",
                "public_profile_example_url",
                "publicly_accessible",
                "indexable",
                "website_field_present",
                "destination_href",
                "link_rel",
                "approval_status",
                "submission_receipt",
                "live_profile_url",
                "verdict",
            }.issubset(fields)
        )

    def test_skill_and_workflow_route_the_tactic_with_guardrails(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "workflows" / "authority-and-links.md").read_text(
            encoding="utf-8"
        )
        audit = (
            ROOT / "audit-log" / "2026-08-22-government-supplier-registry-profiles.md"
        ).read_text(encoding="utf-8")

        self.assertIn("government-supplier-registry-profiles.md", skill)
        self.assertIn("Government supplier registries", skill)
        self.assertIn("government-supplier-registry-profiles.md", workflow)
        self.assertIn("government-supplier-registry-opportunities.csv", workflow)
        self.assertIn("procurement-purpose", workflow)
        self.assertIn("on autopilot", audit)
        self.assertIn("stored supplier information cannot be freely accessed", audit)


if __name__ == "__main__":
    unittest.main()

