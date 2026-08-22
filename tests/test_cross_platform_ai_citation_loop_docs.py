import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYBOOKS = sorted((ROOT / "references" / "playbooks").rglob("*.md"))
WORKFLOWS = sorted((ROOT / "workflows").glob("*.md"))


class CrossPlatformCitationLoopDocsTest(unittest.TestCase):
    def test_playbook_has_required_guardrails(self):
        playbook = (ROOT / "references" / "playbooks" / "maintenance" / "cross-platform-ai-citation-loop.md").read_text(encoding="utf-8")
        playbook_lower = playbook.lower()
        self.assertIn("Microsoft Copilot observations are not Google Search Console Generative AI impressions", playbook)
        self.assertIn("Do not convert observation counts into estimated impressions, clicks, CTR, conversions, or revenue", playbook)
        self.assertIn("There is no public universal GEO score", (ROOT / "workflows" / "geo-audit.md").read_text(encoding="utf-8"))
        self.assertIn("must not be repeated as a benchmark, expected result, or causal proof", playbook)
        for phrase in (
            "never auto-send, buy manipulative placement, fabricate community discussion, hide sponsorship, or manufacture citations",
            "it is not a promise that a content template, backlink, or query position will cause citation.",
            "source breadth is a coverage hypothesis, not a citation formula.",
            "does not validate the claimed total of 47",
            "lacked the provider, prompt set, locale, account state, methodology, and retrieval date",
        ):
            self.assertIn(phrase, playbook_lower)

    def test_source_coverage_template_is_bounded_and_wired(self):
        template = (ROOT / "assets" / "ai-citation-source-coverage.csv").read_text(encoding="utf-8")
        geo = (ROOT / "workflows" / "geo-audit.md").read_text(encoding="utf-8")
        category = (ROOT / "workflows" / "category-citation-loop.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for field in (
            "platform",
            "surface",
            "exact_question",
            "source_class",
            "cited_on_scoped_surface",
            "evidence_grade",
            "approval_state",
            "limitations",
        ):
            self.assertIn(field, template.splitlines()[0])
        for text in (geo, category, skill):
            self.assertIn("assets/ai-citation-source-coverage.csv", text)
        self.assertIn("Source counts are not quotas or causal weights", geo)
        self.assertIn("fixed counts of comparison pages, directories, repository stars, reviews, or community mentions", category)

    def test_relevant_workflows_reference_cross_platform_loop(self):
        expected = {
            "workflows/geo-audit.md",
            "workflows/category-citation-loop.md",
            "workflows/monitoring.md",
            "workflows/authority-and-links.md",
            "workflows/content-production.md",
        }
        for rel in expected:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("cross-platform-ai-citation-loop.md", text, rel)

    def test_commercial_distribution_playbook_is_bounded_and_wired(self):
        playbook = (
            ROOT
            / "references"
            / "playbooks"
            / "content"
            / "cross-platform-commercial-intent-distribution.md"
        ).read_text(encoding="utf-8")
        workflow = (ROOT / "workflows" / "content-production.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("cross-platform-commercial-intent-distribution.md", workflow)
        self.assertIn("cross-platform-commercial-intent-distribution", skill)
        for phrase in (
            "Do not create disposable accounts, evade moderation, seed fake reviews",
            "one primary and at most two supporting surfaces",
            "Never estimate impressions, CTR, conversions, commission, or revenue",
            "publication remains approval-gated",
        ):
            self.assertIn(phrase, playbook)

    def test_readme_counts_match_repo(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(len(PLAYBOOKS), 66)
        self.assertEqual(len(WORKFLOWS), 11)
        self.assertIn("## The knowledge layer (66 playbooks)", readme)
        self.assertIn("#the-knowledge-layer-66-playbooks", readme)
        self.assertIn("**66 playbooks**", readme)
        self.assertIn("36 original course distillations plus 30 operational additions", readme)
        self.assertIn("36 course distillations + 30 operational additions", readme)
        self.assertIn("content/         (18)", readme)
        self.assertIn("cross-platform-commercial-intent-distribution", readme)
        self.assertIn("authority/       (18)", readme)
        self.assertIn("government-supplier-registry-profiles", readme)
        self.assertIn("foundations/     (6)", readme)
        self.assertIn("maintenance/     (13)", readme)
        self.assertIn("## The workflows (11 runbooks)", readme)
        self.assertIn("**11 workflows**", readme)
        self.assertIn("ai-answer-visibility-loop", readme)


if __name__ == "__main__":
    unittest.main()
