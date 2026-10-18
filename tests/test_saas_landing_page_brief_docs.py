import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = ROOT / "references/playbooks/content/landing-pages.md"
GUIDE = GUIDE_PATH.read_text(encoding="utf-8")
WORKFLOW = (ROOT / "workflows/content-production.md").read_text(encoding="utf-8")


class SaasLandingPageBriefDocsTests(unittest.TestCase):
    def test_existing_guide_is_the_workflow_owner(self):
        self.assertIn("## SaaS landing-page brief: section-to-evidence plan", GUIDE)
        self.assertIn("landing-pages.md#saas-landing-page-brief-section-to-evidence-plan", WORKFLOW)
        self.assertIn("Reuse `assets/content-brief.md`", WORKFLOW)
        self.assertIn("review-ready only", WORKFLOW)
        self.assertIn("synonyms alone do not justify competing urls", GUIDE.lower())

    def test_copyable_plan_preserves_evidence_and_unknowns(self):
        blocks = re.findall(r"```markdown\n(.*?)\n```", GUIDE, re.S)
        self.assertEqual(len(blocks), 1)
        plan = blocks[0]
        for field in ("Parent content brief / source packet", "Existing owner URL", "Planned canonical URL", "actual destination", "Evidence reference + checked date", "Primary conversion event, unit, denominator and source", "GSC and analytics baselines / review window", "no schedule created", "draft_not_approved"):
            with self.subTest(field=field):
                self.assertIn(field, plan)
        self.assertIn("unknown", plan)
        for block in ("Promise and next action", "Product demo or sample output", "Supported use cases", "Proof and limits", "Buyer questions and objections"):
            self.assertIn("| " + block + " |", plan)
        self.assertIn("keep / merge / reorder / omit", plan)

    def fixture(self):
        blocks = re.findall(r"```json\n(.*?)\n```", GUIDE, re.S)
        self.assertEqual(len(blocks), 1)
        return json.loads(blocks[0])

    def test_worked_example_is_fictional_unmeasured_and_unapproved(self):
        fixture = self.fixture()
        self.assertEqual(fixture["example_kind"], "fictional_fixture_not_live_evidence")
        self.assertEqual(fixture["serp_evidence"], "unknown")
        self.assertEqual(fixture["conversion_baseline"], "unknown")
        self.assertEqual(fixture["publication_state"], "draft_not_approved")
        self.assertIs(fixture["schedule_created"], False)
        self.assertIn("**ExampleBrief is an invented product.**", GUIDE)
        self.assertIn("No live search results, product test, conversion measurement or customer evidence has been supplied", GUIDE)

    def test_example_reuses_owner_and_rejects_unverified_capabilities(self):
        fixture = self.fixture()
        self.assertEqual(fixture["planned_canonical_url"], fixture["existing_owner_url"])
        self.assertEqual(fixture["planned_canonical_url"], "https://example.com/meeting-notes")
        self.assertEqual(fixture["disposition"], "review_existing_page_before_new_url")
        self.assertEqual(fixture["assumed_supported_input"], "pasted_text_notes_only")
        self.assertEqual(set(fixture["unverified_claims_to_omit"]), {"live_audio_recording", "accuracy_guarantee", "customer_time_savings"})
        self.assertIn("if_the_real_product_supports_it", fixture["primary_action"])
        self.assertIn("not a new-page approval", GUIDE)

    def test_template_does_not_create_ranking_freshness_or_scale_rules(self):
        for phrase in ("five optional authoring blocks, not a five-section ranking rule", "Merge, reorder or omit", "No bulk near-duplicate pages", "Do not force a rewrite every 30 days", "No traffic or revenue outcome is promised", "not five sections specified by the source"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, GUIDE)
        self.assertNotIn("only a landing page will rank", GUIDE)

    def test_review_keeps_metrics_and_authority_separate(self):
        for phrase in ("Keep GSC impressions/clicks separate from analytics sessions, eligible signups and paid outcomes", "before/after change causal proof", "quality pass does not grant those permissions", "publish, send outreach, create a schedule or install a vendor tool", "Every material product claim", "explicit unresolved hold"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, GUIDE)
        self.assertIn("https://x.com/codyschneider/status/2111517654749999271", GUIDE)

    def test_all_local_markdown_links_resolve_inside_the_repository(self):
        for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", GUIDE):
            if target.startswith(("https://", "http://", "#")):
                continue
            path = (GUIDE_PATH.parent / target.split("#", 1)[0]).resolve()
            with self.subTest(target=target):
                self.assertTrue(path.is_relative_to(ROOT.resolve()))
                self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
