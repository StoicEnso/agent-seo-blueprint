"""Offline documentation and illustrative-example checks; not SEO or live-evidence validation."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "references/playbooks/research/research-for-existing-sites.md"
WORKFLOW = ROOT / "workflows/site-audit.md"
HEADING = "## Existing category-page recovery review"


def section():
    return GUIDE.read_text().split(HEADING, 1)[1].split("**Related.**", 1)[0]


def example():
    return json.loads(re.search(r"```json\n(.*?)\n```", section(), re.S).group(1))


class CategoryPageRecoveryDocsTest(unittest.TestCase):
    def test_route_extends_existing_owner_without_another_playbook(self):
        text = WORKFLOW.read_text()
        self.assertIn("research-for-existing-sites.md#existing-category-page-recovery-review", text)
        self.assertIn("this read-only audit grants no", text)
        self.assertEqual(GUIDE.read_text().count(HEADING), 1)
        self.assertIn("not a second content, linking or publishing system", section())
        self.assertFalse(list((ROOT / "references/playbooks").rglob("*category-page-recovery*.md")))

    def test_established_site_source_and_limits_stay_explicit(self):
        text = section()
        for value in ("2111090683423387886", "2111208227115295222", "already had substantial authority",
                      "does not isolate causality", "not verified clicks, orders or revenue",
                      "does not", "four-month timetable"):
            self.assertIn(value, text)
        self.assertNotIn("calendly.com", text)

    def test_intent_cluster_ownership_does_not_generate_modifier_pages(self):
        whole, text = GUIDE.read_text(), section()
        self.assertNotIn("spin up new pages for secondary keywords", whole)
        self.assertIn("one owner page per evidenced intent cluster", whole)
        for value in ("Similar wording is not proof", "different wording is not proof",
                      "inventory/cannibalization review", "HOLD the split", "Google may show a different title"):
            self.assertIn(value, text)
        data = example()
        self.assertEqual(data["page_url"], data["existing_owner_url"])
        self.assertEqual(data["new_page_decision"], "HOLD")
        self.assertEqual(data["ownership_decision"], "retain_existing_pending_evidence")
        self.assertEqual(len(data["same_intent_candidates"]), 3)
        self.assertEqual(urlsplit(data["page_url"]).hostname, "shop.example")

    def test_missing_example_evidence_is_unknown_not_a_live_result(self):
        data = example()
        self.assertTrue(data["example_only"])
        self.assertEqual(data["evidence_refs"], [])
        self.assertIsNone(data["source_revision"])
        self.assertTrue(all(value is None for value in data["search_scope"].values()))
        self.assertEqual(set(data["baseline_metrics"]), {"search_clicks", "orders", "revenue"})
        self.assertTrue(all(value is None for value in data["baseline_metrics"].values()))
        self.assertFalse(data["product_claims_verified"])
        self.assertFalse(data["causality_claimed"])

    def test_example_cannot_authorize_actions(self):
        data = example()
        self.assertEqual(data["approval_status"], "DRAFT_NOT_APPROVED")
        self.assertEqual(set(data["execution"]), {"publish", "delete", "redirect", "outreach", "schedule"})
        self.assertTrue(all(value is False for value in data["execution"].values()))
        self.assertIn("SPLIT_REVIEW` is not page-creation approval", section())
        self.assertIn("rollback", section())

    def test_technical_recovery_is_exact_not_blanket_redirect_or_delete(self):
        text = section()
        for value in ("actual referring page, old URL", "confirmed relevant successor", "404/410",
                      "rather than redirecting everything to the homepage", "does not justify deletion",
                      "no repair executes during this review"):
            self.assertIn(value, text)
        for field in ("source/CMS revision", "country, language, device", "date range, filters", "unknown rather than zero"):
            self.assertIn(field, text)

    def test_content_linking_and_measurement_reuse_existing_gates(self):
        text = section()
        for value in ("Do not copy competitor text", "qualified review", "not medical evidence",
                      "do not promise FAQ rich results", "existing topic/link ledger", "reader benefit",
                      "Do not adopt the case's 40-link quota", "50% keyword-rich-anchor target", "DR30+",
                      "Reject paid/exchanged ranking-credit links", "orders and revenue kept separate",
                      "A follow-up plan does not create a schedule"):
            self.assertIn(value, text)
        for url in ("https://developers.google.com/search/docs/appearance/title-link",
                    "https://developers.google.com/search/docs/crawling-indexing/301-redirects",
                    "https://developers.google.com/search/docs/essentials/spam-policies#link-spam"):
            self.assertIn(url, text)

    def test_local_markdown_links_and_route_anchor_resolve(self):
        for source, text in ((GUIDE, section()), (WORKFLOW, WORKFLOW.read_text())):
            for target in re.findall(r"\]\(([^)]+)\)", text):
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc:
                    continue
                path = source.parent / unquote(parsed.path) if parsed.path else source
                self.assertTrue(path.is_file(), (source, target))
                if parsed.fragment:
                    anchors = set()
                    for heading in re.findall(r"^#+ (.+)$", path.read_text(), re.M):
                        anchors.add(re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-"))
                    self.assertIn(parsed.fragment, anchors, (source, target))


if __name__ == "__main__":
    unittest.main()
