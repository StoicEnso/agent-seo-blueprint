import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERVIEW = ROOT / "references" / "playbooks" / "content" / "content-types-overview.md"
PAGES = ROOT / "references" / "playbooks" / "content" / "content-pages.md"
AVOID = ROOT / "references" / "playbooks" / "content" / "content-what-not-to-do.md"
SITEMAP = ROOT / "references" / "playbooks" / "research" / "keyword-to-sitemap.md"
CHECKLIST = ROOT / "references" / "playbooks" / "maintenance" / "seo-operational-checklist.md"
WORKFLOW = ROOT / "workflows" / "content-production.md"


class SaasPageSelectionDocsTest(unittest.TestCase):
    def test_nine_saas_families_are_candidate_prompts_not_a_formula(self):
        text = OVERVIEW.read_text(encoding="utf-8").lower()
        for family in (
            "**alternative**",
            "**comparison**",
            "**integration**",
            "**constraint**",
            "**pricing**",
            "**use case**",
            "**problem**",
            "**feature**",
            "**audience/company size**",
        ):
            self.assertIn(family, text)
        self.assertIn("practitioner article", text)
        self.assertIn("not as a universal priority order", text)
        self.assertIn("do not inherit the field article's claimed ordering", text)
        self.assertIn("https://x.com/nicholasdulait/status/2087537648747286874", text)

    def test_mutable_and_comparative_claims_require_product_truth(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in (OVERVIEW, PAGES, CHECKLIST)
        )
        for phrase in (
            "material areas where the owner's product loses",
            "working supported integration",
            "do not publish a near-match",
            "do not copy stale competitor prices",
            "source, and checked date",
            "literally true",
        ):
            self.assertIn(phrase, combined)

    def test_doorway_and_scaled_content_boundaries_use_current_google_policy(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in (OVERVIEW, AVOID, SITEMAP, CHECKLIST, WORKFLOW)
        )
        self.assertIn("https://developers.google.com/search/docs/essentials/spam-policies", combined)
        self.assertIn("https://developers.google.com/search/docs/fundamentals/ai-optimization-guide", combined)
        self.assertIn("doorway abuse", combined)
        self.assertIn("scaled content abuse", combined)
        self.assertIn("consolidate token-swapped variants", combined)
        self.assertIn("no doorway-like token variant survives", combined)

    def test_no_fixed_crawl_or_word_count_is_promoted(self):
        text = AVOID.read_text(encoding="utf-8").lower()
        self.assertIn("does not publish a universal pages-per-site-per-month", text)
        self.assertIn("there is no universal `100–200 words` minimum", text)
        self.assertNotIn("~30-40", text)
        self.assertNotIn("release ~10-30 per month", text)
        self.assertNotIn("aim for at least ~100-200 words", text)

    def test_workflow_records_build_reject_or_consolidate_evidence(self):
        text = WORKFLOW.read_text(encoding="utf-8").lower()
        for phrase in (
            "saas modifier branch",
            "saas_page_family?",
            "eligibility_evidence?",
            "product_truth_evidence?",
            "overlap_canonical_decision?",
            "reject_consolidate_reason?",
            "never use the field article's order or six-month claim as a forecast",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
