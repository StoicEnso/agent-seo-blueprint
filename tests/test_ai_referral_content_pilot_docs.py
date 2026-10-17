import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AiReferralContentPilotDocsTests(unittest.TestCase):
    def test_playbook_preserves_source_limits_and_separate_lanes(self):
        text = (ROOT / "references" / "playbooks" / "content" / "evidence-bound-ai-referral-content-pilot.md").read_text(encoding="utf-8")
        for phrase in (
            "https://x.com/hridoyreh/status/2111145144506352107",
            "131 **users** in 15 countries",
            "unverified author claims",
            "not restate it as 131 customers",
            "A provider citation is not a referral.",
            "Referrer host alone cannot identify a prompt, cited page, model, or cause.",
            "one to three pages in a pilot",
            "Reuse before creating.",
            "reporting window and time zone",
            "provider citations/mentions, referral sessions, eligible first-party signups, and paid customers/revenue",
            "zero ad spend” does not mean zero cost",
            "No personal data, raw event IDs, or private analytics captures",
        ):
            self.assertIn(phrase, text)

    def test_template_has_truth_and_measurement_fields(self):
        with (ROOT / "assets" / "ai-referral-content-pilot.csv").open(newline="", encoding="utf-8") as handle:
            fields = set(csv.DictReader(handle).fieldnames or [])
        self.assertTrue({
            "question_version", "evidence_source", "page_role", "reuse_disposition",
            "claim_evidence_url", "product_truth_owner", "reporting_window_start",
            "reporting_window_end", "time_zone", "referrer_scope", "cohort_definition",
            "deduplication_key_or_rule", "provider_citation_or_mention_unit",
            "referral_session_unit", "signup_unit", "paid_customer_or_revenue_unit",
            "limitations", "decision_state",
        }.issubset(fields))

    def test_workflows_route_the_pilot_without_execution_authority(self):
        content = (ROOT / "workflows" / "content-production.md").read_text(encoding="utf-8")
        answers = (ROOT / "workflows" / "ai-answer-visibility-loop.md").read_text(encoding="utf-8")
        for text in (content, answers):
            self.assertIn("evidence-bound-ai-referral-content-pilot.md", text)
            self.assertIn("ai-referral-content-pilot.csv", text)
        self.assertIn("does not authorize publishing, analytics changes, outreach, or a schedule", content)
