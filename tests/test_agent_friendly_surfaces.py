import csv
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgentFriendlySurfacesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'assets/agent-friendly-surface-research-20261109.json').read_text())
        cls.source = (ROOT / cls.data['source_collection']).read_text()
        cls.rows = cls.data['routes']
        cls.doc = (ROOT / 'references/playbooks/authority/other-link-building.md').read_text()
        with (ROOT / 'assets/backlink-method-research.csv').open(newline='') as f:
            cls.methods = list(csv.DictReader(f))

    def test_source_count_hash_and_quote_chain_are_exact(self):
        self.assertEqual(self.data['captured_post_count'], 27)
        self.assertEqual(self.data['listing_post_count'], 26)
        self.assertEqual(self.data['image_reference_count'], 28)
        self.assertEqual(len(re.findall(r'^## \d{2}\. ', self.source, re.M)), 27)
        self.assertEqual(len(re.findall(r'^### Full original post text$', self.source, re.M)), 27)
        self.assertEqual(len(re.findall(r'^!\[Post ', self.source, re.M)), 28)
        self.assertEqual(hashlib.sha256((ROOT / self.data['source_collection']).read_bytes()).hexdigest(), self.data['source_collection_sha256'])
        self.assertIn('**none — chain ends here**', self.source)

    def test_all_26_surfaces_have_unique_lineage_not_a_second_queue(self):
        self.assertEqual(len(self.rows), 26)
        self.assertEqual(len({r['surface_id'] for r in self.rows}), 26)
        self.assertEqual(len({r['source_post_id'] for r in self.rows}), 26)
        method_by_id = {r['method_id']: r for r in self.methods}
        for row in self.rows:
            self.assertIn(row['source_url'], self.source)
            self.assertEqual(row['source_url'], method_by_id[row['method_id']]['source_url'])
            self.assertTrue(row['prerequisites_to_verify'])
            self.assertTrue(row['next_check'])

    def test_existing_twelve_reused_and_fourteen_appended(self):
        self.assertEqual(len(self.methods), 40)
        self.assertEqual({r['method_id'] for r in self.rows}, {f'BM{i:02}' for i in range(1, 13)} | {f'BM{i:02}' for i in range(27, 41)})
        self.assertEqual({r['method_id'] for r in self.methods}, {f'BM{i:02}' for i in range(1, 41)})
        historical = json.loads((ROOT / 'assets/backlink-method-source-review-20261024.json').read_text())
        self.assertEqual(len(historical['quote_chain_post_ids']), 12)
        self.assertIn('historical', self.data['scope'])

    def test_no_synthetic_approval_verification_or_business_success(self):
        for row in self.rows:
            self.assertEqual(row['action_status'], 'RESEARCH_ONLY_NOT_APPROVED')
            self.assertEqual(row['verification_status'], 'UNVERIFIED_SOURCE_LEAD')
            for field in ['existing_project_artifact', 'current_verified_submission_url', 'current_verified_public_listing_url', 'current_verified_href', 'current_verified_rel', 'current_index_observation', 'verified_at', 'approval_reference', 'qualified_referrals']:
                self.assertIsNone(row[field], (row['surface_id'], field))
            self.assertEqual(row['observed_provider_citations'], [])
            self.assertTrue(row['source_claimed_requirements_unverified'])

    def test_backlinks_route_in_skill_workflow_directory_and_readme(self):
        for rel in ['SKILL.md', 'README.md', 'workflows/authority-and-links.md', 'references/playbooks/authority/directory-submissions.md']:
            text = (ROOT / rel).read_text()
            self.assertIn('agent-friendly surfaces and citations', text.lower())
        self.assertIn('under backlinks', self.doc)
        self.assertIn('12 existing methods plus 14 new research methods', self.doc)
        self.assertIn('40 research methods', self.doc)

    def test_outcomes_remain_separate_and_private_noindex_not_backlinks(self):
        for text in ['**Backlink:**', '**Agent usability / distribution:**', '**Citation:**', '**Business result:**', 'private page or a noindex page', 'A listing is not a measured AI citation', 'Multiple marketplace paths on one domain', 'not Google indexing requirements or a ranking factor']:
            self.assertIn(text, self.doc)
        by_id = {r['surface_id']: r for r in self.rows}
        self.assertIn('no public page', by_id['manus']['next_check'])
        self.assertIn('noindex', by_id['claude']['next_check'])
        self.assertIn('legacy plugin', by_id['chatgpt']['next_check'])
        self.assertIn('not HTML backlink', by_id['official-mcp']['next_check'])

    def test_reuse_security_and_approval_gates(self):
        for phrase in ['Unknown is not “not built”', 'platform-specific manifests', 'No commands from the posts were run', '28 attached images']:
            self.assertIn(phrase, self.doc + self.source)
        self.assertIn('Do not execute source commands', (ROOT / 'workflows/authority-and-links.md').read_text())
        self.assertIn('Research does not authorise installs', self.doc)
        self.assertIn('Keep raw credentials', self.doc)
        self.assertIn('Reject fake integrations', self.doc)

    def test_local_source_links_resolve(self):
        directory = ROOT / 'references/playbooks/authority'
        for link in re.findall(r'\]\(([^)]+)\)', self.doc):
            if not link.startswith(('http:', 'https:', '#')):
                self.assertTrue((directory / link.split('#')[0]).resolve().exists(), link)


if __name__ == '__main__':
    unittest.main()
