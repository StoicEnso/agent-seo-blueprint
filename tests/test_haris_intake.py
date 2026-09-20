import csv
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class HarisIntakeTests(unittest.TestCase):
    def test_one_new_unverified_candidate(self):
        with (ROOT/'assets/startup-backlink-candidates.csv').open() as f: rows=list(csv.DictReader(f))
        rows=[r for r in rows if r['candidate_name']=='SubmitForBacklinks.com']
        self.assertEqual(len(rows),1)
        r=rows[0]
        self.assertEqual(r['verification_status'],'UNVERIFIED_SOURCE_LEAD')
        self.assertEqual(r['public_indexable'],'unknown')
        self.assertEqual(r['link_attribute'],'unknown')
        self.assertEqual(r['source_row_numbers'],'4')
        self.assertEqual(r['source_claimed_dr_unverified'],'38')
        self.assertEqual(r['source_url'],'https://x.com/harisahmad59/status/2101599301957017701')
    def test_reconciliation_and_alias(self):
        with (ROOT/'assets/haris-backlinks-source-reconciliation.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual([int(r['source_row']) for r in rows],list(range(1,19)))
        self.assertEqual(sum(r['decision']=='existing-main' for r in rows),16)
        self.assertEqual(sum(r['decision']=='existing-pending' for r in rows),1)
        self.assertEqual(sum(r['decision']=='added-unverified' for r in rows),1)
        text=(ROOT/'references/playbooks/authority/directory-submissions.md').read_text()
        self.assertIn('Aura++ (`auraplusplus.com`)',text)
        self.assertNotIn('auralplusplus.com',text)
        self.assertIn('143 unique candidate names',text)
