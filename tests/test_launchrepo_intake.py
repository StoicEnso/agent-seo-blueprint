import csv,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
 with (ROOT/'assets'/name).open(newline='') as f:
  reader=csv.DictReader(f);data=list(reader)
  assert all(None not in r and None not in r.values() for r in data)
  return data
class LaunchRepoIntakeTests(unittest.TestCase):
 def test_reconciliation_balances(self):
  data=rows('launchrepo-source-reconciliation.csv')
  self.assertEqual(len(data),121);self.assertEqual(len({r['domain'] for r in data}),121)
  self.assertEqual(sum(r['decision']=='imported_unverified' for r in data),66)
  self.assertEqual(sum(r['decision']=='separate_community' for r in data),5)
  self.assertEqual(sum(r['decision']=='deferred' for r in data),4)
 def test_candidates_are_unverified_and_unique(self):
  allrows=rows('startup-backlink-candidates.csv');new=[r for r in allrows if r['source_url']=='https://launchrepo.dev/']
  self.assertEqual(len(new),66);self.assertEqual(len({r['canonical_domain'] for r in new}),66)
  names=[r['candidate_name'].lower() for r in allrows];self.assertEqual(len(names),len(set(names)))
  for r in new:
   self.assertEqual(r['verification_status'],'UNVERIFIED_SOURCE_LEAD')
   self.assertEqual(r['source_observed_at'],'2026-09-18')
   self.assertEqual(r['public_indexable'],'unknown');self.assertEqual(r['link_attribute'],'unknown')
   self.assertEqual(r['submission_url'],'');self.assertEqual(r['last_verified_at'],'')
   self.assertTrue(all(not v for k,v in r.items() if k.startswith('source_claimed_')))
  ledger=rows('launchrepo-source-reconciliation.csv');excluded={r['domain'] for r in ledger if r['decision']!='imported_unverified'}
  self.assertTrue(excluded.isdisjoint({r['canonical_domain'] for r in new}))
 def test_no_submission_or_bulk_catalog_claim(self):
  self.assertEqual(rows('directory-submission-tracker.csv'),[])
  entry=next(r for r in rows('directory-discovery-sources.csv') if r['source_url']=='https://launchrepo.dev/')
  self.assertEqual(entry['verification_status'],'DISCOVERY_SOURCE_ONLY');self.assertEqual(entry['observed_candidate_count'],'121')
  self.assertIn('not accessed',entry['notes'])
 def test_guidance_is_evidence_scoped(self):
  text=(ROOT/'references/playbooks/authority/launchrepo-public-intake.md').read_text()
  for term in ['Pending approval','earliest acceptable launch date','partner-distribution','production deploy','CAPTCHA','No listing, account, purchase']:
   self.assertIn(term,text)
if __name__=='__main__':unittest.main()
