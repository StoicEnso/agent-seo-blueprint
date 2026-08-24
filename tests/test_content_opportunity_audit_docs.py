import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContentOpportunityAuditDocsTest(unittest.TestCase):
    def test_playbook_preserves_write_and_measurement_guards(self):
        text = (ROOT / "references/playbooks/maintenance/content-opportunity-audit-and-measurement.md").read_text(encoding="utf-8")
        required = [
            "has no website write permission",
            "HEURISTIC_FALLBACK",
            "Do not auto-publish any class",
            "reject stale approvals",
            "**+28 days**",
            "**+56 days**",
            "Citation observations are not impressions, clicks, conversions, or attribution.",
            "the only reason to act is a creator's claimed multiplier",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_ledger_defaults_reject_forecast_and_causality_claims(self):
        payload = json.loads((ROOT / "assets/content-opportunity-ledger.json").read_text(encoding="utf-8"))
        candidate = payload["candidate"]
        self.assertFalse(candidate["headroom"]["is_forecast"])
        self.assertFalse(candidate["measurement"]["causality_claimed"])
        self.assertIn("STALE", candidate["decision"]["candidate_status"])
        self.assertIn("HEURISTIC_FALLBACK", candidate["headroom"]["expected_ctr_source"])

    def test_router_and_workflows_are_wired(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        monitoring = (ROOT / "workflows/monitoring.md").read_text(encoding="utf-8")
        content = (ROOT / "workflows/content-production.md").read_text(encoding="utf-8")
        for text in (skill, monitoring, content):
            self.assertIn("content-opportunity-audit-and-measurement.md", text)
        self.assertIn("content-opportunity-ledger.json", skill)
        self.assertIn("content-change-ledger.jsonl", monitoring)
        self.assertIn("exact proposed diff", content)

    def test_source_claims_are_narrowed(self):
        audit = (ROOT / "references/audit-log/2026-08-24-content-opportunity-audit-and-measurement.md").read_text(encoding="utf-8")
        self.assertIn("not independently controlled or transferable benchmarks", audit)
        self.assertIn("Automatic publication", audit)
        self.assertIn("Rejected for this skill", audit)


if __name__ == "__main__":
    unittest.main()
