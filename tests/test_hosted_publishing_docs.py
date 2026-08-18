import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HostedPublishingDocsTests(unittest.TestCase):
    def test_telegraph_claim_is_corrected_with_live_evidence(self):
        text = (
            ROOT
            / "references"
            / "playbooks"
            / "authority"
            / "hosted-publishing-experiments.md"
        ).read_text(encoding="utf-8")

        for phrase in (
            "https://x.com/jespernissenseo/status/2089076596531417229",
            "https://telegra.ph/api",
            "external links on the inspected API page rendered with `rel=\"nofollow\"`",
            "`index, follow` is eligibility, not guaranteed indexation",
            "A third-party `DA` or `DR` score is a vendor metric",
            "No blanket rollout",
            "Draft one pilot, not an unlimited batch",
            "API availability is an execution fact, not an SEO result",
            "REJECT_FOR_LINK_EQUITY",
            "Publishing the same article for every owned site",
        ):
            self.assertIn(phrase, text)

    def test_hosted_publishing_template_separates_fit_write_and_outcome(self):
        path = ROOT / "assets" / "hosted-publishing-experiment.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fields = set(reader.fieldnames or [])

        self.assertTrue(
            {
                "project",
                "destination_url",
                "fit_status",
                "reader_job",
                "article_thesis",
                "original_evidence_or_asset",
                "duplicate_or_thin_review",
                "relationship_disclosure",
                "approval_state",
                "public_url",
                "http_status",
                "canonical_url",
                "robots_directive",
                "rendered_destination_href",
                "rendered_rel",
                "index_check_day_0",
                "index_check_day_7",
                "index_check_day_14",
                "index_check_day_30",
                "referral_sessions",
                "engaged_referrals",
                "assisted_conversions",
                "article_survival_check",
                "verdict",
            }.issubset(fields)
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["approval_state"], "DRAFT_NOT_APPROVED")
        self.assertEqual(rows[0]["verdict"], "INCONCLUSIVE")
        self.assertIn("No publication has occurred", rows[0]["notes"])

    def test_candidate_registry_does_not_label_telegraph_dofollow(self):
        with (ROOT / "assets" / "startup-backlink-candidates.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = {row["candidate_name"]: row for row in csv.DictReader(handle)}

        row = rows["Telegra.ph"]
        self.assertEqual(
            row["verification_status"],
            "VERIFIED_CANDIDATE_DOFOLLOW_UNSUPPORTED",
        )
        self.assertEqual(row["source_claimed_link_attribute_unverified"], "DA93 dofollow")
        self.assertIn("indexation unverified", row["public_indexable"])
        self.assertIn("nofollow observed", row["link_attribute"])
        self.assertIn("No page was published", row["notes"])

    def test_playbook_is_fully_routed_and_guarded(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "workflows" / "authority-and-links.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        design = (ROOT / "DESIGN.md").read_text(encoding="utf-8")
        guardrail = (
            ROOT
            / "references"
            / "playbooks"
            / "authority"
            / "linkbuilding-what-not-to-do.md"
        ).read_text(encoding="utf-8")

        for text in (skill, workflow, readme, design):
            self.assertIn("hosted-publishing", text.lower())

        self.assertIn("hosted-publishing-experiments.md", skill)
        self.assertIn("hosted-publishing-experiment.csv", skill)
        self.assertIn("one-site hosted-publishing pilots", readme)
        self.assertIn("one separately approved pilot at most", workflow)
        self.assertIn("successful API response does not prove a followed link", guardrail)
        for phrase in (
            "spun/duplicated cross-site articles",
            "doorway pages",
            "volume-first API loops",
            "fake authorship",
            "one pilot never authorizes an all-site batch",
        ):
            self.assertIn(phrase, workflow)

    def test_audit_log_records_no_external_write(self):
        text = (ROOT / "audit-log" / "2026-08-18-telegraph-hosted-publishing.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "**API submission:** possible",
            "**Dofollow claim:** not supported",
            "No account or article was created",
            "one approved, original article for the strongest-fit site",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
