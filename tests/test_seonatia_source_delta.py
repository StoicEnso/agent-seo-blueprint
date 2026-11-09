import csv,hashlib,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SeonatiaSourceDeltaTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((ROOT/'assets/seonatia-backlink-crosswalk-20261109.json').read_text());cls.entries=cls.data['entries']
  cls.candidates=list(csv.DictReader((ROOT/'assets/startup-backlink-candidates.csv').open()))
  cls.source=(ROOT/'references/sources/2026-11-09-seonatia-startup-backlinks.md').read_text()
 def test_complete_source_and_original_image(self):
  self.assertEqual(len(self.entries),21);self.assertEqual(len(re.findall(r'^- .* DR \d+',self.source,re.M)),21)
  self.assertEqual(self.data['image_entry_count'],18)
  image=ROOT/'references/sources/media/2026-11-09-seonatia-startup-backlinks.jpg'
  self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(),self.data['source_image_sha256'])
 def test_exact_delta_and_existing_reuse(self):
  counts={decision:sum(x['decision']==decision for x in self.entries) for decision in ['ADD_MISSING_RESEARCH_LEAD','REUSE_EXISTING','REUSE_CAPTERRA_HOLD_GT_IDENTITY']}
  self.assertEqual(list(counts.values()),[8,12,1]);self.assertEqual(len(self.candidates),150)
  for x in self.entries:
   if x['decision']=='ADD_MISSING_RESEARCH_LEAD':self.assertEqual(sum(r['candidate_name']==x['candidate_name'] for r in self.candidates),1)
  self.assertEqual(len(self.data['existing_evidence']),13)
 def test_no_invented_gt_alias_or_backlink_success(self):
  x=next(x for x in self.entries if 'GT /' in x['source_label'])
  self.assertEqual(x['normalised_source_domain'],'gt/capterra.com');self.assertIn('no G2 alias',x['first_party_check_note'])
  for x in self.entries:
   self.assertEqual(x['action_status'],'RESEARCH_ONLY_NOT_APPROVED')
   for field in ['verified_public_listing_url','verified_href','verified_rel']:self.assertIsNone(x[field])
   self.assertEqual(x['index_observation'],'NOT_MEASURED')
 def test_paid_signals_and_non_directory_routes(self):
  byname={x['candidate_name']:x for x in self.entries}
  self.assertIn('purchases',byname['Stripe Climate']['first_party_check_note'])
  self.assertIn('paid passes',byname['Indie Page']['first_party_check_note'])
  self.assertIn('checkout',byname['Viral Marketing Lab']['first_party_check_note'])
  self.assertEqual(byname['Carrd']['route_type'],'hosted_microsite')
  self.assertEqual(byname['Behance']['route_type'],'creative_portfolio')
 def test_existing_method_register_unchanged(self):
  methods=list(csv.DictReader((ROOT/'assets/backlink-method-research.csv').open()))
  self.assertEqual(len(methods),40)
 def test_crosswalk_links_and_approval_gate(self):
  doc=(ROOT/'references/playbooks/authority/directory-submissions.md').read_text()
  self.assertIn('8 missing research leads',doc);self.assertIn('No rendered listing href/rel',doc)
  self.assertIn('does not approve accounts',doc)
  for x in self.data['existing_evidence'].values():self.assertTrue((ROOT/x['path']).exists())
if __name__=='__main__':unittest.main()
