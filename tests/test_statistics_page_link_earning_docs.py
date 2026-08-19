import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = (
    ROOT
    / "references"
    / "playbooks"
    / "authority"
    / "statistics-page-link-earning.md"
)
ASSET = ROOT / "assets" / "statistics-page-brief.csv"
SKILL = ROOT / "SKILL.md"


class StatisticsPageLinkEarningDocsTest(unittest.TestCase):
    def test_creator_claim_is_kept_as_a_hypothesis(self):
        text = PLAYBOOK.read_text(encoding="utf-8")
        for phrase in (
            "80-query dataset",
            "creator hypothesis",
            "not a “rank without backlinks” guarantee",
            "A weak domain ranking in one observed result is a lead",
            "Sequence is not causation",
        ):
            self.assertIn(phrase, text)

    def test_page_requires_real_evidence_and_stable_architecture(self):
        text = PLAYBOOK.read_text(encoding="utf-8")
        for phrase in (
            "stable yearless URL",
            "at least one auditable original or reproducible statistic",
            "Never invent data",
            "Preserve the original `datePublished`",
            "Use `Dataset` only when the page exposes a real dataset",
            "A footer link is optional, not a default",
            "Publishing and sending outreach are separate external actions",
        ):
            self.assertIn(phrase, text)

    def test_skill_routes_the_playbook_and_template(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("statistics-page-link-earning.md", text)
        self.assertIn("assets/statistics-page-brief.csv", text)
        self.assertIn("hold publication and outreach for explicit approval", text)

    def test_template_preserves_source_method_and_outcome_separation(self):
        with ASSET.open(newline="", encoding="utf-8") as handle:
            fields = set(csv.DictReader(handle).fieldnames or [])
        self.assertTrue(
            {
                "target_query",
                "serp_checked_at",
                "serp_fit_evidence",
                "source_url",
                "claim_text",
                "sample_size",
                "methodology",
                "calculation",
                "verification_state",
                "original_stat",
                "stable_url",
                "date_published",
                "date_modified",
                "contextual_link_reader_reason",
                "footer_link_justified",
                "publication_approval",
                "outreach_approval",
                "new_referring_domains",
                "assisted_conversions",
                "limitations",
                "verdict",
            }.issubset(fields)
        )


if __name__ == "__main__":
    unittest.main()
