import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CITATION = ROOT / "references" / "playbooks" / "maintenance" / "cross-platform-ai-citation-loop.md"
COMMERCE = ROOT / "references" / "playbooks" / "maintenance" / "ai-search-commerce-readiness.md"
FOUNDATIONS = ROOT / "references" / "playbooks" / "foundations" / "seo-and-ai-future.md"
GEO = ROOT / "workflows" / "geo-audit.md"
MONITORING = ROOT / "workflows" / "monitoring.md"
SKILL = ROOT / "SKILL.md"


class GammaAeoEvidenceDocsTest(unittest.TestCase):
    def test_self_report_is_not_laundered_into_attribution(self):
        combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in (CITATION, GEO, MONITORING, SKILL))
        for phrase in (
            "how did you hear about us?",
            "response denominator",
            "non-response",
            "hidden traffic",
            "causal",
        ):
            self.assertIn(phrase, combined)
        self.assertIn("view-through conversions", combined)

    def test_provider_scope_and_black_box_claims_are_bounded(self):
        text = CITATION.read_text(encoding="utf-8").lower()
        for phrase in (
            "do not copy another company's provider order",
            "one primary provider and at most two supporting providers",
            "uncited answer does not prove",
            "field_hypothesis",
            "consecutive_runs_seen",
            "dropped_on",
            "do not assume a three-month citation half-life",
        ):
            self.assertIn(phrase, text)

    def test_retrieval_and_memory_are_hypotheses_not_provider_facts(self):
        text = FOUNDATIONS.read_text(encoding="utf-8").lower()
        for phrase in (
            "retrieval, memory, and personalization are separate hypotheses",
            "field_hypothesis",
            "fixed live-web versus memory split",
            "traffic/revenue forecast input",
        ):
            self.assertIn(phrase, text)

    def test_agent_native_surface_is_user_safe_not_manipulative(self):
        combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in (COMMERCE, GEO, SKILL))
        for phrase in (
            "real user job",
            "least-privilege authentication",
            "explicit user consent",
            "before consequential actions",
            "prompt injection",
            "schema bribes",
        ):
            self.assertIn(phrase, combined)
        self.assertIn("merely publishing an mcp server or connector does not prove", combined)

    def test_deceptive_gamma_tactics_are_explicitly_rejected(self):
        citation = CITATION.read_text(encoding="utf-8").lower()
        agent_surface = COMMERCE.read_text(encoding="utf-8").lower()
        for phrase in (
            "fake community posts",
            "engineered to mislead",
            "hidden instructions",
            "provider-wide claims",
        ):
            self.assertIn(phrase, citation)
        self.assertIn('model-directed “bribes”', agent_surface)


if __name__ == "__main__":
    unittest.main()
