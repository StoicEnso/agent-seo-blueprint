"""Offline contract tests for sitemap cohort guidance; they do not access GSC or a live site."""
from pathlib import Path
import csv
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SitemapCohortDocsTests(unittest.TestCase):
    def test_template_is_empty_and_has_evidence_shape(self):
        path = ROOT / "assets/sitemap-cohort-evidence.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        self.assertEqual(len(rows), 1)
        headers = set(rows[0])
        self.assertTrue({"property", "property_type", "sitemap_or_index_url", "membership_source", "current_filter", "source_observed_at", "report_count", "report_state", "canonical_eligible_set_source", "overlap_handling", "representative_url_inspection_evidence", "alternative_explanations", "proposed_exact_change_or_write", "owner_approval", "rollback_plan", "actual_receipt", "follow_up"}.issubset(headers))

    def test_routing_and_scope_guardrails_are_real(self):
        technical = (ROOT / "references/playbooks/maintenance/technical-seo-maintenance.md").read_text(encoding="utf-8") + (ROOT / "workflows/technical-seo-maintenance.md").read_text(encoding="utf-8")
        gsc = (ROOT / "references/integrations/gsc.md").read_text(encoding="utf-8")
        routes = "\n".join((ROOT / p).read_text(encoding="utf-8") for p in ["workflows/technical-seo-maintenance.md", "workflows/site-audit.md", "workflows/monitoring.md", "references/playbooks/maintenance/seo-operational-checklist.md"])
        for phrase in ["usable index", "Index and child counts may overlap", "cached-versus-live", "not proof of indexation", "owner-approved GSC write authority"]:
            self.assertIn(phrase, technical)
        for phrase in ["report/API submission list", "robots.txt", "specific sitemap/index filter", "up to 1,000", "No submission, deletion, Validate fix, or Request indexing"]:
            self.assertIn(phrase, gsc)
        for phrase in ["sitemap-cohort-evidence.csv", "unknown/partial", "mismatched windows/memberships", "exact GSC write"]:
            self.assertIn(phrase, routes)

if __name__ == "__main__":
    unittest.main()
