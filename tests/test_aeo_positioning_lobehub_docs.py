import json
import csv
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class AeoPositioningLobehubTests(unittest.TestCase):
    def setUp(self):
        self.aeo = (ROOT / 'references/playbooks/content/cross-platform-commercial-intent-distribution.md').read_text()
        self.directory = (ROOT / 'references/playbooks/authority/directory-submissions.md').read_text()
        self.audit = (ROOT / 'references/audit-log/2026-11-08-aeo-positioning-and-lobehub.md').read_text()
        self.template = json.loads((ROOT / 'assets/aeo-positioning-review.json').read_text())
        self.candidates = json.loads((ROOT / 'assets/mcp-marketplace-candidates.json').read_text())

    def test_source_boundaries(self):
        for value in ['2119089991217262884', '2119435109405175973', 'An acquisition offer is not realized revenue', 'No diagnosis']:
            self.assertIn(value, self.audit)
    def test_one_canonical_candidate(self):
        self.assertEqual(len(self.candidates['candidates']), 1)
        row = self.candidates['candidates'][0]
        self.assertEqual(row['canonical_domain'], 'lobehub.com')
        self.assertEqual(row['publishing_subdomain'], 'market.lobehub.com')
        self.assertEqual(row['verification_status'], 'UNVERIFIED_SOURCE_LEAD')
    def test_claims_never_promoted_to_observations(self):
        row = self.candidates['candidates'][0]
        self.assertEqual(row['source_claimed_dr_unverified'], 75)
        self.assertEqual(row['source_claimed_link_attribute_unverified'], 'all dofollow')
        for key in ['observed_href', 'observed_rel', 'public_indexable', 'cost_terms', 'submission_receipt', 'publication_approval', 'last_live_verified_at']:
            self.assertIsNone(row[key])
    def test_destination_paths_and_real_fit(self):
        for value in ['https://lobehub.com/mcp', 'https://market.lobehub.com/s/publish-mcp', 'real Model Context Protocol', 'Do not create a dummy server', 'identifier', 'version', 'existing listing/claim route']:
            self.assertIn(value, self.directory)
    def test_directory_approval_and_link_semantics(self):
        for value in ['outside a research-only task', 'Even manifest generation can start', 'no `dofollow` HTML attribute', 'No listing was submitted', 'indexability/canonical']:
            self.assertIn(value, self.directory)
        self.assertIn('connect_github', self.candidates['candidates'][0]['not_authorized'])
    def test_template_empty_and_approval_gated(self):
        self.assertEqual(self.template['status'], 'RESEARCH_ONLY_NOT_APPROVED')
        self.assertEqual(self.template['observations'], [])
        self.assertIsNone(self.template['publication_approval'])
        self.assertTrue(all(x == 'NOT_MEASURED' for x in self.template['outcomes'].values()))
    def test_control_design_and_measurement(self):
        for key in ['hypothesis', 'control_cluster', 'baseline_window', 'review_window', 'success_criterion', 'stop_condition', 'counter_explanations', 'cannibalization_check']:
            self.assertIn(key, self.template)
        for value in ['query_or_exact_prompt', 'provider_surface', 'captured_at', 'actual_cited_url']:
            self.assertIn(value, self.template['observation_fields'])
        for value in ['A brand mention is not a citation', 'not causal proof', 'comparable unchanged cluster', 'fake independent recommendation sites']:
            self.assertIn(value, self.aeo)
    def test_official_sources_and_existing_workflow(self):
        for value in ['https://developers.google.com/search/docs/appearance/ai-features', 'https://developers.google.com/search/docs/essentials/spam-policies', 'maintenance/cross-platform-ai-citation-loop.md']:
            self.assertIn(value, self.aeo)
    def test_links_are_resolvable(self):
        for rel in ['references/audit-log/2026-11-08-aeo-positioning-and-lobehub.md', 'assets/aeo-positioning-review.json', 'assets/mcp-marketplace-candidates.json']:
            self.assertTrue((ROOT / rel).is_file())
        for text in [self.aeo, self.directory]:
            self.assertIn('../../audit-log/2026-11-08-aeo-positioning-and-lobehub.md', text)
    def test_discovery_registry_routes_to_one_conditional_candidate(self):
        with (ROOT / 'assets/directory-discovery-sources.csv').open(newline='') as handle:
            rows = [r for r in csv.DictReader(handle) if '2119435109405175973' in r['source_url']]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['verification_status'], 'DISCOVERY_SOURCE_ONLY')
        self.assertEqual(rows[0]['observed_candidate_count'], '1')
        self.assertIn('assets/mcp-marketplace-candidates.json', rows[0]['notes'])

    def test_no_new_executable_or_job(self):
        self.assertIn('it starts no job or live test', self.aeo)
        self.assertIn('no CLI, skill or instruction from it was installed or executed', self.audit)

if __name__ == '__main__':
    unittest.main()
