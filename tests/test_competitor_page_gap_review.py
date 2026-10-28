import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PB = ROOT / "references/playbooks/research/research-for-existing-sites.md"
FIELDS = ['candidate_id', 'export_source', 'captured_at_utc', 'country', 'device', 'scope', 'coverage', 'competitor_url', 'serp_title', 'query_cluster', 'estimated_traffic', 'page_referring_domains', 'existing_url', 'coverage_evidence', 'decision', 'product_fit', 'live_serp_evidence', 'owned_status_evidence', 'unique_value', 'conversion_path', 'priority', 'owner', 'target_date', 'approval_state', 'notes']


class CompetitorPageGapReviewTest(unittest.TestCase):
    def text(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def rows(self):
        with (ROOT / "assets/competitor-page-gap-examples.csv").open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_blank_template_has_exact_schema_and_no_autoapproval(self):
        with (ROOT / "assets/competitor-page-gap-map.csv").open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.assertEqual(reader.fieldnames, FIELDS)
            self.assertEqual(list(reader), [])

    def test_export_metadata_and_unknowns_are_explicit(self):
        text = PB.read_text(encoding="utf-8")
        for phrase in ("SERP titles", "country/database", "device", "PARTIAL", "pagination/export limits", "Unknown stays unknown, not zero"):
            self.assertIn(phrase, text)

    def test_existing_answers_and_aliases_are_checked_before_new_urls(self):
        text = PB.read_text(encoding="utf-8")
        for phrase in ("not slugs", "rendered/CMS", "missing sitemap entry is not proof", "canonical", "trailing-slash", "Multiple competitor pages can map to one owned answer"):
            self.assertIn(phrase, text)

    def test_screenshots_do_not_become_zero_backlink_claim(self):
        text = PB.read_text(encoding="utf-8")
        for phrase in ("9 referring domains for React.js, 9 for Next.js and 6 for Vue.js", "5,401 groups of links", "One link per domain", "not independently recomputed", "42% or 114-page"):
            self.assertIn(phrase, text)

    def test_calendar_and_side_effects_stay_gated(self):
        text = PB.read_text(encoding="utf-8")
        for phrase in ("original value", "conversion/internal-link path", "proposed owner/date", "outside the calendar", "not_requested", "do not redirect, delete", "never instructions", "do not execute spreadsheet formulas"):
            self.assertIn(phrase, text)

    def test_workflow_and_integration_route_the_existing_playbook(self):
        research = self.text("workflows/research-and-ideation.md")
        for phrase in ("competitor-page-gap-map.csv", "competitor-page-gap-examples.csv", "read-only review", "research-for-existing-sites.md"):
            self.assertIn(phrase, research)
        ahrefs = self.text("references/integrations/ahrefs.md")
        self.assertIn("This change adds no Top Pages API command", ahrefs)
        self.assertIn("SERP titles", ahrefs)

    def test_authority_research_separates_asset_delivery_from_editorial_links(self):
        text = self.text("workflows/authority-and-links.md")
        for phrase in ("CDN asset", "editorial", "href", "rel", "not zero", "no disavow"):
            self.assertIn(phrase, text)

    def test_eight_examples_are_synthetic_and_cover_all_dispositions(self):
        rows = self.rows()
        self.assertEqual(len(rows), 8)
        self.assertEqual(len({r["candidate_id"] for r in rows}), 8)
        self.assertEqual({r["decision"] for r in rows}, {"reuse_existing", "update_existing", "new_candidate", "consolidation_review", "review", "reject"})
        for row in rows:
            self.assertIn(".test/", row["competitor_url"])
            self.assertEqual(row["export_source"], "SYNTHETIC_NOT_A_LIVE_EXPORT")
            self.assertEqual(row["approval_state"], "not_requested")
            self.assertFalse(row["page_referring_domains"])
            self.assertFalse(row["estimated_traffic"])

    def test_qualified_calendar_example_requires_a_complete_brief(self):
        for row in self.rows():
            if row["target_date"]:
                self.assertEqual(row["decision"], "new_candidate")
                self.assertEqual(row["product_fit"], "relevant")
                for key in ("live_serp_evidence", "owned_status_evidence", "unique_value", "conversion_path", "priority", "owner"):
                    self.assertTrue(row[key], key)
            if row["decision"] in ("review", "reject", "consolidation_review"):
                self.assertFalse(row["target_date"])
        rows = {r["candidate_id"]: r for r in self.rows()}
        self.assertEqual(rows["not-in-sitemap"]["decision"], "reuse_existing")
        self.assertEqual(rows["incomplete-inventory"]["coverage"], "PARTIAL")

    def test_review_scope_and_lf_only_csvs(self):
        audit = self.text("audit-log/2026-10-28-illyism-competitor-page-gap.md")
        self.assertIn("No new workflow, playbook, collector", audit)
        self.assertIn("not an implemented automatic semantic matcher", audit)
        for name in ("competitor-page-gap-map.csv", "competitor-page-gap-examples.csv"):
            self.assertNotIn(b"\r", (ROOT / "assets" / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
