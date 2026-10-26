import csv
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ParasiteIntakeTests(unittest.TestCase):
    def test_exact_eleven_source_bound_rows(self):
        with (ROOT/'assets/parasite-seo-idea-pilots.csv').open(newline='') as handle:
            rows=list(csv.DictReader(handle))
        self.assertEqual([int(x['id']) for x in rows],list(range(1,12)))
        for row in rows:
            self.assertIn('2114390277737890085',row['source_url'])
            self.assertEqual(row['pilot_state'],'DRAFT_RESEARCH_ONLY')
            self.assertEqual(row['approval_state'],'EXACT_PUBLICATION_NOT_APPROVED')
            for key in ['public_url','rendered_destination_href','rendered_rel','index_observation','referrals','business_outcome']:
                self.assertFalse(row[key])
    def test_truth_and_outcome_guards(self):
        text=(ROOT/'audit-log/2026-10-26-parasite-seo-11-idea-intake.md').read_text()
        for term in ['fake vacancies','disguised promotional paper','title bait-and-switch','expired-domain abuse','Pages limits','one-time fee','No live experiment has run','exact publication approval','qualified referrals']:
            self.assertIn(term,text)
    def test_existing_workflow_routes_intake(self):
        for rel in ['references/playbooks/authority/hosted-publishing-experiments.md','workflows/authority-and-links.md']:
            text=(ROOT/rel).read_text()
            self.assertIn('parasite-seo-idea-pilots.csv',text)
            self.assertIn('2026-10-26-parasite-seo-11-idea-intake.md',text)
if __name__=='__main__':unittest.main()
