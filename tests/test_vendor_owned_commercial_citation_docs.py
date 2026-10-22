import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VendorOwnedCommercialCitationDocsTest(unittest.TestCase):
    def test_asset_has_source_ownership_and_scope_fields(self):
        header = (ROOT / "assets" / "vendor-owned-commercial-citation-audit.csv").read_text(encoding="utf-8").splitlines()[0]
        for field in (
            "exact_query", "provider", "surface", "locale", "account_state", "captured_at",
            "result_type", "cited_url", "source_owner", "page_role", "ownership_disclosed",
            "observed_or_candidate", "product_truth_status", "evidence_grade", "approval_state", "limitations",
        ):
            self.assertIn(field, header)

    def test_playbook_is_wired(self):
        playbook_name = "vendor-owned-commercial-query-citations.md"
        asset_name = "assets/vendor-owned-commercial-citation-audit.csv"
        for rel in ("SKILL.md", "workflows/category-citation-loop.md", "workflows/content-production.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(playbook_name, text, rel)
            self.assertIn(asset_name, text, rel)
        self.assertIn("vendor-owned-commercial-query-citations", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_playbook_rejects_the_sales_formula(self):
        text = (ROOT / "references" / "playbooks" / "maintenance" / "vendor-owned-commercial-query-citations.md").read_text(encoding="utf-8")
        for phrase in (
            "Do not turn a vendor's `10 articles`, `60 articles`, or backlink bundle into a quota.",
            "The panel size bounds observation; it does not prescribe page count.",
            "Do not call a page independent when the vendor owns it.",
            "human-readable structure chosen for the buyer, not synthetic `AI chunks`.",
            "A `DR50+` backlink package is a vendor offer, not proof",
            "temporal association, not proof that the page caused it",
            "category ownership will occur in six to twelve months",
        ):
            self.assertIn(phrase, text)

    def test_measurement_and_writes_stay_separate(self):
        text = (ROOT / "references" / "playbooks" / "maintenance" / "vendor-owned-commercial-query-citations.md").read_text(encoding="utf-8")
        for phrase in (
            "ordinary Search impressions, clicks, CTR, and position",
            "Google-specific Generative AI impressions",
            "named-provider brand mentions and cited URLs",
            "referral sessions from named sources",
            "leads, assisted conversions, transactions, and revenue",
            "publication and outreach remain approval-gated",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
