import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EditorialLinkIntentDocsTest(unittest.TestCase):
    def test_playbook_has_safety_and_evidence_gates(self):
        text = (ROOT / "references" / "playbooks" / "authority" / "editorial-link-intent-and-assets.md").read_text(encoding="utf-8").lower()
        required = [
            "credit-based or networked",
            'rel="sponsored"',
            "provider citation observations are a targeting hint only",
            "decayed_resource",
            "statistics_or_research_need",
            "missing_visual",
            "article_video_asset",
            "unlinked_owned_asset",
            "never send without explicit per-batch approval",
            "temporal sequence is not causation",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_skill_routes_and_guards_the_playbook(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("editorial-link-intent-and-assets", skill)
        self.assertIn("credit-based reciprocal-link networks", skill)
        self.assertIn("sponsored", skill)

    def test_opportunity_asset_has_required_fields(self):
        asset = (ROOT / "assets" / "editorial-link-opportunity.json").read_text(encoding="utf-8")
        for field in [
            '"intent_class"',
            '"observed_gap"',
            '"evidence"',
            '"rights_and_attribution"',
            '"replacement_fit"',
            '"required_rel"',
            '"hard_fails"',
            '"status"',
        ]:
            self.assertIn(field, asset)


if __name__ == "__main__":
    unittest.main()
