import csv
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BorjaBacklinkReviewTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / 'assets/borja-backlink-tactic-review.csv').open(newline='') as f:
            self.rows = list(csv.DictReader(f))
        self.review = (ROOT / 'audit-log/2026-11-01-borja-backlink-tactics.md').read_text()
        self.workflow = (ROOT / 'workflows/authority-and-links.md').read_text()

    def test_exact_source_coverage_without_duplicates(self):
        entries = []
        for row in self.rows:
            self.assertRegex(row['source_entries'], r'^\d+-\d+$')
            first, last = map(int, row['source_entries'].split('-'))
            self.assertLessEqual(first, last)
            entries.extend(range(first, last + 1))
        self.assertEqual(entries, list(range(1, 70)))
        self.assertEqual(len(self.rows), 12)
        self.assertEqual(len({r['family'] for r in self.rows}), 12)

    def test_existing_routes_and_gates(self):
        for row in self.rows:
            route = Path(row['existing_route'])
            self.assertFalse(route.is_absolute())
            self.assertNotIn('..', route.parts)
            self.assertTrue((ROOT / route).is_file(), route)
            self.assertGreater(len(row['evidence_gate']), 50)
            self.assertIn(row['decision'], {'COVERED', 'REJECT_EXCHANGE_CONDITION'})
        exchange = self.rows[0]
        self.assertEqual(exchange['decision'], 'REJECT_EXCHANGE_CONDITION')
        self.assertIn('reciprocity', exchange['evidence_gate'])

    def test_claims_approvals_and_duplicate_check(self):
        for phrase in ['2116164330014007296', 'unverified author claim',
                       'DRAFT only', 'exact batch approval',
                       'not merged dependencies', 'not a business outcome']:
            self.assertIn(phrase, self.review)
        for number in [50, 31, 62, 22]:
            self.assertIn(f'/pull/{number}', self.review)
        self.assertIn('borja-backlink-tactic-review.csv', self.workflow)

    def test_canonical_workflow_routes(self):
        frontmatter = self.workflow.split('---')[1]
        for name in ['editorial-link-intent-and-assets', 'statistics-page-link-earning']:
            path = f'references/playbooks/authority/{name}.md'
            self.assertIn(f'  - {path}', frontmatter)
        self.assertIn('Source review: backlink tactics', (ROOT / 'README.md').read_text())

    def test_review_relative_links(self):
        parent = ROOT / 'audit-log'
        for link in re.findall(r'\]\(([^)]+)\)', self.review):
            if not link.startswith('https://'):
                self.assertTrue((parent / link).resolve().is_file(), link)


if __name__ == '__main__':
    unittest.main()
