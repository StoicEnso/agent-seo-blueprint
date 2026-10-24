import csv
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "references/playbooks/maintenance/seo-operational-checklist.md"


class BraveUrlSubmissionDocsTest(unittest.TestCase):
    def setUp(self):
        self.text = CHECKLIST.read_text(encoding="utf-8")

    def test_existing_37_check_matrix_is_preserved(self):
        matrix = self.text.split("## 37-check matrix", 1)[1].split("## Brave Search", 1)[0]
        rows = re.findall(r"^\| ([A-Z]+-\d+) \|", matrix, re.MULTILINE)
        self.assertEqual(len(rows), 37)
        self.assertEqual(len(set(rows)), 37)
        self.assertIn("does not add a 38th row", self.text)

    def test_official_route_and_creator_claim_are_attributed(self):
        for phrase in (
            "https://search.brave.com/submit-url",
            "https://search.brave.com/help/brave-search-crawler",
            "https://x.com/hridoyreh/status/2114004776061182246",
            "Insert the URL to be re-fetched",
            "unverified creator claim",
        ):
            self.assertIn(phrase, self.text)

    def test_default_is_read_only_and_named_approval_is_required(self):
        for phrase in ("read-only by default", "Require explicit user approval", "named public URLs", "Submit once", "No tight loops", "CAPTCHA bypass", "Retry-After"):
            self.assertIn(phrase, self.text)

    def test_preflight_keeps_exclusions_and_canonical_checks(self):
        for phrase in ("canonical tag", "X-Robots-Tag", "Googlebot", "robots.txt", "intentional block", "private, authenticated, staging", "homepage request is not a full-site"):
            self.assertIn(phrase, self.text)

    def test_provider_acceptance_is_not_a_business_outcome(self):
        for phrase in ("not proof of indexing", "not_found_in_sample", "not_checked", "referral_sessions", "conversions", "revenue", "never zero", "Google/Bing", "IndexNow"):
            self.assertIn(phrase, self.text)

    def test_receipt_ambiguity_does_not_authorize_a_repeat(self):
        for phrase in ("unknown_after_dispatch", "single dispatch before clicking", "do not automatically retry", "avoid duplicate submissions", "A missing local record is **unknown**", "screenshot or DOM receipt"):
            self.assertIn(phrase, self.text)

    def test_header_only_template_has_separate_evidence_lanes(self):
        with (ROOT / "assets/brave-url-submission-tracker.csv").open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(list(reader), [])
            fields = reader.fieldnames
        self.assertEqual(len(fields), len(set(fields)))
        self.assertTrue({"canonical_url", "preflight_evidence", "googlebot_crawl_allowed", "approval_evidence", "approval_scope", "prior_submission_evidence", "refresh_reason", "attempt_count", "submitted_at", "submission_state", "confirmation_text", "submission_evidence", "visibility_state", "visibility_provider", "visibility_query", "visibility_checked_at", "observed_result_urls", "visibility_evidence", "referral_sessions", "conversions", "revenue", "outcome_evidence"}.issubset(fields))

    def test_both_existing_workflows_route_to_the_supplement(self):
        for name in ("site-audit.md", "technical-seo-maintenance.md"):
            text = (ROOT / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn("seo-operational-checklist.md#brave-search-url-submission-and-re-fetch-supplemental", text)
            self.assertIn("assets/brave-url-submission-tracker.csv", text)
            self.assertIn("read-only", text)
            self.assertIn("approval", text)

    def test_skill_routes_brave_to_existing_workflows(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Check Brave Search coverage", text)
        self.assertIn("seo-operational-checklist.md#brave-search-url-submission-and-re-fetch-supplemental", text)
        self.assertIn("assets/brave-url-submission-tracker.csv", text)
        self.assertIn("named-URL submission approval", text)

    def test_readme_discovery_does_not_claim_rollout(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Brave Search", text)
        self.assertIn("submission acceptance is not indexing", text)


if __name__ == "__main__":
    unittest.main()
