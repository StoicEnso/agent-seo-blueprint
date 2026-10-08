import csv,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/'scripts/gsc_zero_click_triage.py'
def base(): return {"metadata":{"property":"sc-domain:example.com","search_type":"web","dimensions":["query","page"],"filters":{},"date_range":{"start":"2026-09-01","end":"2026-09-28","timezone":"UTC","finalized":True}},"properties":["sc-domain:example.com"],"rows":[{"query":"alpha","page":"https://example.com/a","clicks":0,"impressions":5,"ctr":0,"position":12}],"coverage":[{"query":"alpha","status":"not_covered","evidence":"inventory checked"}]}
def run(d,more=()):
 with tempfile.TemporaryDirectory() as x:
  i=Path(x)/'in.json'; o=Path(x)/'out.json'; i.write_text(json.dumps(d)); p=subprocess.run([sys.executable,str(SCRIPT),str(i),'--output',str(o),*more],text=True,capture_output=True); return p,json.loads(o.read_text()) if o.exists() else None
class TestTriage(unittest.TestCase):
 def test_new_page_and_raw_metrics(self):
  p,o=run(base()); self.assertEqual(p.returncode,0); self.assertEqual(o['records'][0]['category'],'relevant_untargeted_new_dedicated_page'); self.assertEqual(o['records'][0]['impressions'],5)
 def test_zero_impressions_excluded(self):
  d=base(); d['rows'][0]['impressions']=0; p,o=run(d); self.assertEqual(o['records'],[])
 def test_existing_coverage_adjustment(self):
  d=base(); d['coverage'][0]['status']='covered'; p,o=run(d); self.assertEqual(o['records'][0]['category'],'existing_page_content_or_intent_adjustment')
 def test_missing_coverage_unknown(self):
  d=base(); d['coverage']=[]; p,o=run(d); self.assertEqual(o['records'][0]['category'],'unknown_due_to_missing_evidence')
 def test_multiple_query_page_rows(self):
  d=base(); d['rows'].append({"query":"beta","page":"https://example.com/b","clicks":0,"impressions":8,"ctr":0,"position":5}); d['coverage'].append({"query":"beta","status":"covered","evidence":"inventory"}); p,o=run(d); self.assertEqual(len(o['records']),2); self.assertNotEqual(o['records'][0]['page_url'],o['records'][1]['page_url'])
 def test_partial_anonymous_unknown(self):
  d=base(); d['data_quality']={"complete_window":False,"anonymous_rows":True}; p,o=run(d); self.assertEqual(o['records'][0]['category'],'unknown_due_to_missing_evidence'); self.assertIn('anonymous',' '.join(o['records'][0]['limitations']))
 def test_duplicate_properties_rejected(self):
  d=base(); d['properties']*=2; p,o=run(d); self.assertEqual(p.returncode,2); self.assertIsNone(o)
 def test_invalid_input_rejected(self):
  d=base(); del d['rows'][0]['ctr']; p,o=run(d); self.assertEqual(p.returncode,2); self.assertIsNone(o)
 def test_csv_formula_prefix_escaped(self):
  d=base(); d['rows'][0]['query']='=SUM(A1:A2)'
  with tempfile.TemporaryDirectory() as x:
   i=Path(x)/'i.json'; o=Path(x)/'o.json'; c=Path(x)/'o.csv'; i.write_text(json.dumps(d)); p=subprocess.run([sys.executable,str(SCRIPT),str(i),'--output',str(o),'--csv',str(c)],text=True,capture_output=True); self.assertEqual(p.returncode,0); self.assertIn("'=SUM(A1:A2)", c.read_text(encoding='utf-8'))
 def test_read_only_and_history(self):
  d=base(); d['coverage'][0]['status']='covered'; d['rows'][0]['position']=4; d['history']={"alpha":{"clicks":3}}; p,o=run(d); self.assertEqual(o['mode'],'read_only_draft'); self.assertEqual(o['records'][0]['category'],'relevant_well_ranked_snippet_ctr_investigation'); self.assertIn('Earlier window',' '.join(o['records'][0]['limitations']))
if __name__=='__main__': unittest.main()
