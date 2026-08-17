import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CreatorTacticIntakeDocsTests(unittest.TestCase):
    def test_mechanic_first_playbook_requires_a_bounded_learning_loop(self):
        text = (
            ROOT
            / "references"
            / "playbooks"
            / "foundations"
            / "mechanic-first-growth-experiments.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "Define the behavior before the build",
            "Transfer mechanisms, not surfaces",
            "Run the smallest reversible test",
            "Pre-register the decision",
            "Views, likes, bookmarks, rankings, links",
            "REJECTED_OR_PROHIBITED",
            "Manufactured consensus",
            "three-way exchanges designed to conceal coordination",
            "residential-proxy account setups intended to misrepresent geography",
            "https://x.com/gregisenberg/status/2088272956203966970",
            "https://x.com/jammer3k/status/2088618901902901633",
            "not an SEO experiment",
            "adopt | revise | reject | inconclusive",
        ):
            self.assertIn(phrase, text)

    def test_tiny_loop_wedge_is_evidence_gated_and_routed(self):
        playbook = (
            ROOT
            / "references"
            / "playbooks"
            / "foundations"
            / "mechanic-first-growth-experiments.md"
        ).read_text(encoding="utf-8")
        research = (ROOT / "workflows" / "research-and-ideation.md").read_text(
            encoding="utf-8"
        )
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for phrase in (
            "source-authored framing",
            "explicit approval",
            "prepare, do not commit",
            "consented context",
            "observable closure receipt",
            "independent search or user-demand evidence",
            "do not manufacture a programmatic page set",
        ):
            self.assertIn(phrase, playbook)

        self.assertIn("tiny-loop-opportunity-map.csv", research)
        self.assertIn("tiny-loop-opportunity-map.csv", skill)
        self.assertIn("tiny-loop-opportunity-map.csv", readme)
        self.assertIn("A creator's opportunity forecast is not demand validation", research)

        with (ROOT / "assets" / "tiny-loop-opportunity-map.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            fields = set(csv.DictReader(handle).fieldnames or [])
        self.assertTrue(
            {
                "audience",
                "trigger",
                "evidence_of_frequency",
                "search_demand_evidence",
                "consented_context_sources",
                "data_minimization_rule",
                "approval_boundary",
                "closure_receipt",
                "safe_failure_or_expiry",
                "primary_metric",
                "guardrails",
                "verdict",
            }.issubset(fields)
        )

    def test_topic_architecture_rejects_depth_inflation_and_has_templates(self):
        text = (
            ROOT
            / "references"
            / "playbooks"
            / "content"
            / "topic-architecture-and-internal-link-ledger.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "self-reported observational findings",
            "not independently replicated causal proof",
            "49,000 AI mentions over three months",
            "not evidence that topic architecture caused rankings, citations, traffic, or sales",
            "AI drafts need evidence review",
            "universal “topical authority score,”",
            "No thin support pages",
            "Navigation and footer links",
            "Every planned link gets one row",
        ):
            self.assertIn(phrase, text)

        with (ROOT / "assets" / "topic-architecture-map.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            topic_fields = set(csv.DictReader(handle).fieldnames or [])
        with (ROOT / "assets" / "internal-link-ledger.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            link_fields = set(csv.DictReader(handle).fieldnames or [])

        self.assertTrue(
            {"page_role", "distinct_value", "evidence_required", "money_page_url"}.issubset(
                topic_fields
            )
        )
        self.assertTrue(
            {"source_url", "destination_url", "anchor_text", "reader_reason"}.issubset(
                link_fields
            )
        )

    def test_openpr_claims_are_corrected_and_not_generalized(self):
        text = (
            ROOT
            / "references"
            / "playbooks"
            / "authority"
            / "press-release-distribution.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "**one free press release per 30 days**",
            "**no more than five in-text backlinks**",
            "own pages were inconsistent",
            "do **not** go live immediately",
            "15 fresh public releases",
            "does not prove that an allowed backlink becomes clickable",
            "No ranking or indexing promises",
            "optimized-anchor links in press releases",
            "External writes need approval",
            "Sequence is not causation",
        ):
            self.assertIn(phrase, text)

        with (ROOT / "assets" / "press-release-distribution-registry.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["platform"], "openPR")
        self.assertEqual(row["verification_status"], "VERIFIED_CANDIDATE")
        self.assertIn("up to five followed links", row["source_claims_unverified"])
        self.assertIn("no more than five in-text backlinks", row["official_observations"])
        self.assertIn("another destination-owned page said three links", row["official_observations"])
        self.assertEqual(
            row["sample_link_attribute_observed"],
            "no_publisher_destination_hyperlink_observed_in_15_fresh_samples",
        )
        self.assertIn("No claim of guaranteed indexation", row["notes"])

    def test_local_business_profile_intake_is_evidence_gated(self):
        text = (
            ROOT
            / "references"
            / "playbooks"
            / "maintenance"
            / "local-business-profile-audit.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "https://x.com/bloggersarvesh/status/2088983373859725755",
            "relevance, distance, and prominence",
            "`$100k/month` in `90 days` framing is unverified",
            "does **not** publish a review-velocity formula",
            "No ranking or revenue guarantees",
            "Do not incentivize reviews",
            "Do not script the reviewer's keywords",
            "Posting frequency is a hypothesis",
            "Reject the obsolete claim that all posts expire after seven days",
            "no public change occurred without approval",
            "visibility from leads, conversions, and revenue",
        ):
            self.assertIn(phrase, text)

        with (ROOT / "assets" / "local-business-profile-audit.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            fields = set(csv.DictReader(handle).fieldnames or [])
        self.assertTrue(
            {
                "location_context",
                "observed_at",
                "source_claim",
                "evidence_grade",
                "official_evidence_or_project_observation",
                "hypothesis_or_unknown",
                "truth_basis",
                "policy_risk",
                "approval_state",
                "visibility_metric",
                "business_outcome_metric",
            }.issubset(fields)
        )

    def test_local_business_profile_playbook_is_routed_and_read_only(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        audit = (ROOT / "workflows" / "site-audit.md").read_text(encoding="utf-8")
        monitoring = (ROOT / "workflows" / "monitoring.md").read_text(
            encoding="utf-8"
        )
        checklist = (
            ROOT
            / "references"
            / "playbooks"
            / "maintenance"
            / "seo-operational-checklist.md"
        ).read_text(encoding="utf-8")

        for text in (skill, readme, audit, monitoring, checklist):
            self.assertIn("local-business-profile-audit", text)
        self.assertIn("read-only by default", skill)
        self.assertIn("require explicit approval", audit)
        self.assertIn("One before/after movement is not causal proof", monitoring)

    def test_new_playbooks_are_routed_and_guarded(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        research = (ROOT / "workflows" / "research-and-ideation.md").read_text(
            encoding="utf-8"
        )
        content = (ROOT / "workflows" / "content-production.md").read_text(
            encoding="utf-8"
        )
        authority = (ROOT / "workflows" / "authority-and-links.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("mechanic-first-growth-experiments.md", research)
        self.assertIn("topic-architecture-and-internal-link-ledger.md", research)
        self.assertIn("topic-architecture-and-internal-link-ledger.md", content)
        self.assertIn("press-release-distribution.md", authority)
        self.assertIn("minute-level indexing", skill)
        self.assertIn("not a topical-authority score", skill)


if __name__ == "__main__":
    unittest.main()
