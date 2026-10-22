import csv
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    with (ROOT / 'assets' / name).open() as f:
        return list(csv.DictReader(f))

class Launch94IntakeTests(unittest.TestCase):
    def test_all_source_rows_accounted_for(self):
        rows = load('launch94-source-reconciliation.csv')
        self.assertEqual([int(r['source_row']) for r in rows], list(range(1, 95)))
        for decision, count in [('existing-main',47),('existing-pending',11),('missing',35),('deferred',1)]:
            self.assertEqual(sum(r['decision'] == decision for r in rows), count)
        deferred = [r for r in rows if r['decision'] == 'deferred']
        self.assertEqual(deferred[0]['candidate_name'], 'Neeed Directory')

    def test_missing_leads_are_safe_and_nonduplicate(self):
        new = load('launch94-missing-candidates.csv')
        audit = load('launch94-source-reconciliation.csv')
        main = load('startup-backlink-candidates.csv')
        normalize = lambda x: ''.join(c for c in x.lower() if c.isalnum())
        self.assertEqual(len(new),35)
        self.assertEqual({r['candidate_name'] for r in new}, {r['candidate_name'] for r in audit if r['decision']=='missing'})
        self.assertFalse({normalize(r['candidate_name']) for r in new} & {normalize(r['candidate_name']) for r in main})
        for r in new:
            self.assertEqual(r['verification_status'],'UNVERIFIED_SOURCE_LEAD')
            self.assertEqual(r['public_indexable'],'unknown')
            self.assertEqual(r['link_attribute'],'unknown')
            self.assertEqual(r['canonical_domain'],'')
            self.assertEqual(r['submission_url'],'')
            self.assertEqual(r['source_url'],'https://x.com/hridoyreh/status/2101574360385360122')
            self.assertEqual(r['source_observed_at'],'2026-09-20')
