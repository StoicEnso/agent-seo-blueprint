import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RecurringWorkDeliveryDocsTest(unittest.TestCase):
    def test_wrapper_routes_to_existing_workflows_with_guards(self):
        text = (ROOT / "workflows/recurring-work-delivery.md").read_text(encoding="utf-8")
        required = [
            "workflows/research-and-ideation.md",
            "workflows/content-production.md",
            "workflows/site-audit.md",
            "workflows/technical-seo-maintenance.md",
            "workflows/authority-and-links.md",
            "workflows/ai-answer-visibility-loop.md",
            "workflows/monitoring.md",
            "manual by default",
            "not capacity targets, guarantees",
            "It does not start a scheduler",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_states_and_write_controls_are_explicit(self):
        text = (ROOT / "workflows/recurring-work-delivery.md").read_text(encoding="utf-8")
        for state in ("proposed", "drafted", "approved", "applied", "verified", "deferred", "rejected"):
            self.assertIn(f"`{state}`", text)
        for phrase in ("duplicate/carry-forward rows", "exact change differs from approval", "risk/rollback", "receipt", "outcome check"):
            self.assertIn(phrase, text)

    def test_ledger_and_routing_contracts_are_discoverable(self):
        ledger = (ROOT / "assets/recurring-work-ledger.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        monitoring = (ROOT / "workflows/monitoring.md").read_text(encoding="utf-8")
        self.assertIn("raw, human-reviewable source artifact", ledger)
        self.assertIn("Do not report it as renderer-supported", ledger)
        self.assertIn("recurring-work-delivery.md", skill)
        self.assertIn("recurring-work-ledger.md", monitoring)

    def test_monitoring_schedule_and_diagnosis_do_not_overclaim(self):
        monitoring = (ROOT / "workflows/monitoring.md").read_text(encoding="utf-8")
        for phrase in (
            "step 8 report emission",
            "duplicate timer",
            "review hypothesis, not evidence of future ranking loss",
            "not a content-quality verdict",
            "do not start outreach automatically",
        ):
            self.assertIn(phrase, monitoring)

    def test_provenance_and_collection_limits_remain_visible(self):
        wrapper = (ROOT / "workflows/recurring-work-delivery.md").read_text(encoding="utf-8")
        gsc = (ROOT / "references/integrations/gsc.md").read_text(encoding="utf-8")
        metrics = (ROOT / "references/playbooks/research/seo-metrics.md").read_text(encoding="utf-8")
        for phrase in ("MEASURED_ZERO", "MISSING_ACCESS", "PARTIAL", "PROVIDER_ESTIMATE", "GSC appearances are property observations"):
            self.assertIn(phrase, wrapper)
        self.assertIn("Pacific-time date boundary", gsc)
        self.assertIn("helper remains a stub", gsc)
        self.assertIn("Do not relabel GSC impressions as market demand", metrics)


if __name__ == "__main__":
    unittest.main()
