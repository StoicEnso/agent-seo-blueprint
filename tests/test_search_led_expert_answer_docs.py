import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SearchLedExpertAnswerDocsTest(unittest.TestCase):
    def setUp(self):
        self.playbook = (ROOT / "references/playbooks/content/cross-platform-commercial-intent-distribution.md").read_text(encoding="utf-8")
        self.workflow = (ROOT / "workflows/content-production.md").read_text(encoding="utf-8")
        self.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.audit = (ROOT / "audit-log/2026-08-19-search-led-expert-answer-series.md").read_text(encoding="utf-8")

    def test_source_claim_is_bounded(self):
        for phrase in (
            "https://x.com/robhoffman_/status/2089832083233423615",
            "no query set, comparison cohort, account history",
            "Do not attribute the claim to a Google update without direct update evidence.",
            "creator hypotheses",
        ):
            self.assertIn(phrase, self.playbook + self.audit)

    def test_method_is_bounded_and_approval_gated(self):
        for phrase in (
            "Pilot **3–10 questions**",
            "one primary surface and at most two supporting adaptations",
            "Search volume alone does not prove social resonance.",
            "Do not post one unchanged asset everywhere.",
            "Publication on every external surface remains separately approval-gated.",
            "Keep ordinary-search visibility, native reach, referrals, named-provider answer mentions/citations, leads, and conversions separate.",
        ):
            self.assertIn(phrase, self.playbook)

    def test_template_preserves_evidence_and_outcomes(self):
        path = ROOT / "assets/search-led-expert-answer-map.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            header = next(csv.reader(handle))
        for field in (
            "exact_question",
            "question_source",
            "source_evidence",
            "owned_answer_url",
            "cannibalization_check",
            "claim_boundary",
            "proof_asset",
            "surface",
            "provider",
            "prompt_version",
            "publication_approval",
            "search_impressions",
            "native_views",
            "referral_sessions",
            "ai_mentions",
            "ai_citations",
            "conversions",
            "limitations",
            "verdict",
        ):
            self.assertIn(field, header)

    def test_skill_and_workflow_route_the_asset(self):
        for text in (self.skill, self.workflow, self.playbook):
            self.assertIn("assets/search-led-expert-answer-map.csv", text)
        self.assertIn("search-led founder or expert answer series", self.skill.lower())


if __name__ == "__main__":
    unittest.main()
