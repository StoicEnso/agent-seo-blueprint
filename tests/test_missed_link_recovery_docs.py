"""Check that the recovered sources remain bounded to evidence-led advice."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MissedLinkRecoveryDocsTest(unittest.TestCase):
    def test_five_sources_and_decision_limits(self):
        memo = (ROOT / "audit-log/2026-09-24-missed-link-recovery.md").read_text()
        for source_id in (
            "2102058813444542763",
            "2102686470033084670",
            "2102384016661844445",
            "2102265246325047711",
            "2102459363051065722",
        ):
            self.assertIn(source_id, memo)
        for limit in ("self-reported", "Do not import the number as verified", "No SEO action", "No URL inventory was submitted"):
            self.assertIn(limit, memo)

    def test_existing_workflows_gain_bounded_checks(self):
        pseo = (ROOT / "references/playbooks/content/programmatic-seo.md").read_text()
        links = (ROOT / "references/playbooks/content/topic-architecture-and-internal-link-ledger.md").read_text()
        self.assertIn("reported six-day directory win is not a rollout target", pseo)
        self.assertIn("tool accepting 2,000 URLs does not imply a 2,000-page target", links)


if __name__ == "__main__":
    unittest.main()
