import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OrganizationEntityReconciliationDocsTest(unittest.TestCase):
    def test_playbook_preserves_identity_and_claim_guards(self):
        text = (ROOT / "references/playbooks/content/organization-entity-reconciliation.md").read_text(encoding="utf-8")
        required = [
            "unambiguously identify the same entity",
            "One subject per node",
            "Identity, not mention",
            "No bulk profile creation",
            "does not turn a profile into a followed backlink",
            "REPAIR_THEN_INCLUDE",
            "RELATION_ONLY",
            "A clean validator result proves syntax",
            "the only reason to include a URL is domain authority",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_audit_narrows_creator_claims(self):
        text = (ROOT / "references/audit-log/2026-08-26-organization-sameas-entity-reconciliation.md").read_text(encoding="utf-8")
        required = [
            "do not prove ranking impact",
            "Better than 300 directory listings",
            "All screenshot URLs belong on Organization `sameAs`",
            "Profile/account writes stay under their own approved platform workflow",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_identity_audit_asset_separates_decisions(self):
        with (ROOT / "assets/organization-entity-identity-audit.csv").open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle))
        required = {
            "entity_id",
            "entity_type",
            "candidate_url",
            "identity_match",
            "profile_control",
            "indexable",
            "include_in_sameas",
            "decision_reason",
            "last_verified_at",
            "review_status",
        }
        self.assertTrue(required.issubset(set(header)))

    def test_router_and_audit_workflows_are_wired(self):
        files = [
            ROOT / "SKILL.md",
            ROOT / "workflows/site-audit.md",
            ROOT / "workflows/technical-seo-maintenance.md",
            ROOT / "references/playbooks/content/schema-types-reference.md",
            ROOT / "references/playbooks/content/eeat-framework.md",
        ]
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertIn("organization-entity-reconciliation", text, path.as_posix())
        self.assertIn(
            "organization-entity-identity-audit.csv",
            (ROOT / "SKILL.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
