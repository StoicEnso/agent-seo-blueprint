import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GUIDE='references/playbooks/content/evidence-led-buyer-shortlists.md'
MAP='references/commercial-shortlist-source-map.json'
BRIEF='assets/commercial-shortlist-brief.json'
class BuyerShortlistDocsTest(unittest.TestCase):
 def test_all_source_steps_and_conversion_ideas_are_mapped(self):
  d=json.loads((ROOT/MAP).read_text())
  self.assertEqual([r['n'] for r in d['steps']],list(range(1,15)))
  self.assertEqual([r['n'] for r in d['conversion_ideas']],list(range(1,7)))
  self.assertTrue(all(r['source'] and r['adaptation'] for r in d['steps']+d['conversion_ideas']))
 def test_source_numbers_are_illustrations_not_rules(self):
  d=json.loads((ROOT/MAP).read_text());n=d['source_numeric_illustrations']
  self.assertEqual(n['conversion_positions_percent'],[10,15,30])
  self.assertEqual(n['introduction_max_words'],95)
  self.assertIn('not requirements',n['status'])
  text=(ROOT/GUIDE).read_text().lower()
  for word in ['six-week','unverified','not evidence of causality','not rules','not a quota']:
   self.assertIn(word,text)
 def test_honesty_and_fairness_gates(self):
  text=(ROOT/GUIDE).read_text().lower()
  for word in ['ownership','commercial interest','trade-offs','same criteria','current','missing fact is not a zero']:
   self.assertIn(word,text)
  for word in ['do not fabricate','no cloaking','dates are real','bots-only','not independently verified']:
   self.assertIn(word,text)
 def test_accessible_structure_and_truthful_offers(self):
  text=(ROOT/GUIDE).read_text().lower()
  for word in ['html table','caption','keyboard','mobile','captions/transcript','genuinely free','data use','consent']:
   self.assertIn(word,text)
 def test_research_is_not_falsely_approval_gated(self):
  text=(ROOT/GUIDE).read_text()
  self.assertIn('authorises this reusable guide and bounded research/drafting',text)
  self.assertNotIn('All research, writing, outreach, payment, and publication remain',text)
 def test_no_external_authority_or_fictional_results(self):
  d=json.loads((ROOT/BRIEF).read_text())
  self.assertEqual(d['status'],'DRAFT_NOT_EXECUTABLE')
  self.assertEqual(d['products'],[])
  self.assertEqual(d['claim_ledger'],[])
  self.assertEqual(d['observed_outcomes'],'NOT_RUN')
  self.assertIsNone(d['execution_receipt'])
  for field in ['publication','outreach','purchase']:
   self.assertEqual(d['approval'][field],'NOT_GRANTED')
  m=json.loads((ROOT/MAP).read_text())
  for field in ['publication_authorized','outreach_authorized','purchase_authorized']:
   self.assertFalse(m[field])
 def test_existing_workflows_own_execution(self):
  text=(ROOT/GUIDE).read_text()
  for rel in ['workflows/category-citation-loop.md','workflows/geo-audit.md','workflows/content-production.md','workflows/authority-and-links.md','workflows/monitoring.md']:
   self.assertIn(rel,text);self.assertTrue((ROOT/rel).is_file())
  for rel in ['README.md','SKILL.md','workflows/content-production.md']:
   self.assertIn('evidence-led-buyer-shortlists.md',(ROOT/rel).read_text())
 def test_no_workspace_or_customer_data_in_shared_files(self):
  for rel in [GUIDE,MAP,BRIEF]:
   text=(ROOT/rel).read_text()
   for private in ['/data/','/root/','5173761146','landscapioai.com','getdeclarix.com','dhoraashi.com','haulierscope.co.uk']:
    self.assertNotIn(private,text)
 def test_measurement_lanes_remain_separate(self):
  d=json.loads((ROOT/BRIEF).read_text())
  self.assertEqual(len(d['measurement']['separate_lanes']),5)
  text=(ROOT/GUIDE).read_text().lower()
  for term in ['not a lead','not revenue','association','not proof','provider','locale']:
   self.assertIn(term,text)
if __name__=='__main__':unittest.main()
