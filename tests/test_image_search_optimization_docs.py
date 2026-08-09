import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ImageSearchOptimizationDocsTest(unittest.TestCase):
    def test_playbook_covers_discovery_accessibility_performance_and_metadata(self):
        text = (
            ROOT / "references/playbooks/content/image-search-optimization.md"
        ).read_text()

        required = [
            "https://developers.google.com/search/docs/appearance/google-images",
            "https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata",
            "https://web.dev/learn/performance/image-performance",
            "<img>",
            "srcset",
            "alt=\"\"",
            "image sitemap",
            "ImageObject",
            "Search Console image-search impressions",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_playbook_rejects_common_image_seo_overclaims(self):
        text = (
            ROOT / "references/playbooks/content/image-search-optimization.md"
        ).read_text()

        self.assertIn("never stuff keywords", text)
        self.assertIn("not mandatory markup for every image", text)
        self.assertIn("does not prove", text)
        self.assertIn("Do not lazy-load the likely LCP/hero image", text)

    def test_content_workflow_and_brief_route_to_the_playbook(self):
        workflow = (ROOT / "workflows/content-production.md").read_text()
        audit = (ROOT / "workflows/site-audit.md").read_text()
        maintenance = (ROOT / "workflows/technical-seo-maintenance.md").read_text()
        brief = (ROOT / "assets/content-brief.md").read_text()
        skill = (ROOT / "SKILL.md").read_text()

        self.assertIn(
            "references/playbooks/content/image-search-optimization.md", workflow
        )
        self.assertIn("visual intent", workflow)
        self.assertIn("image-search-optimization.md", audit)
        self.assertIn("do not infer image indexation or traffic", audit)
        self.assertIn("image-search-optimization.md", maintenance)
        self.assertIn("LCP handling", maintenance)
        self.assertIn("decorative images use empty alt", brief)
        self.assertIn("image-search-optimization", skill)


if __name__ == "__main__":
    unittest.main()
