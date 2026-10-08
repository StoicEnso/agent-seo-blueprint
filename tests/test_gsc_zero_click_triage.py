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
 def test_nonfinal_window_unknown(self):
  d=base(); d['metadata']['date_range']['finalized']=False; p,o=run(d); self.assertEqual(o['records'][0]['category'],'unknown_due_to_missing_evidence')
 def test_bad_dates_rejected(self):
  for start,end in [('not-a-date','2026-09-28'),('2026-10-01','2026-09-28')]:
   d=base(); d['metadata']['date_range'].update(start=start,end=end); p,o=run(d); self.assertEqual(p.returncode,2)
 def test_nonfinite_metrics_rejected(self):
  for val in (float('nan'),float('inf'),True,-1):
   d=base(); d['rows'][0]['position']=val; p,o=run(d); self.assertEqual(p.returncode,2)
 def test_invalid_quality_and_history_rejected(self):
  for key,val in [('data_quality',{'complete_window':'false'}),('history',{'alpha':[]}),('query_totals',[])]:
   d=base(); d[key]=val; p,o=run(d); self.assertEqual(p.returncode,2)
 def test_invalid_thresholds_rejected(self):
  for flags in (['--min-impressions','nan'],['--min-impressions','-1'],['--high-rank-position','30','--low-rank-position','20']):
   p,o=run(base(),flags); self.assertEqual(p.returncode,2)
 def test_zero_impressions_with_zero_threshold_excluded(self):
  d=base(); d['rows'][0]['impressions']=0; p,o=run(d,['--min-impressions','0']); self.assertEqual(o['records'],[])
 def test_clicked_other_page_excludes_whole_query(self):
  d=base(); d['rows'].append(dict(d['rows'][0],page='https://example.com/b',clicks=1,ctr=0.2)); p,o=run(d); self.assertEqual(o['records'],[])
 def test_query_only_clicks_exclude_candidate(self):
  d=base(); d['query_totals']={'alpha':{'clicks':1}}; p,o=run(d); self.assertEqual(o['records'],[])
 def test_anonymous_caveat_preserves_verified_observation(self):
  d=base(); d['coverage'][0]['status']='covered'; d['data_quality']={'complete_window':True,'anonymous_rows':True}; p,o=run(d); self.assertEqual(o['records'][0]['category'],'existing_page_content_or_intent_adjustment'); self.assertEqual(o['records'][0]['confidence'],'low')
 def test_capped_rows_cannot_prove_missing_page(self):
  d=base(); d['data_quality']={'row_limit_reached':True}; p,o=run(d); self.assertEqual(o['records'][0]['category'],'unknown_due_to_missing_evidence')
 def test_empty_page_association_unknown(self):
  d=base(); d['rows'][0]['page']=''; p,o=run(d); self.assertEqual(o['records'][0]['category'],'unknown_due_to_missing_evidence')
 def test_empty_or_duplicate_coverage_rejected(self):
  for mode in ('empty','duplicate'):
   d=base()
   if mode=='empty': d['coverage'][0]['evidence']=''
   else: d['coverage']*=2
   p,o=run(d); self.assertEqual(p.returncode,2)
 def test_out_of_scope_page_rejected(self):
  d=base(); d['rows'][0]['page']='https://other.example/a'; p,o=run(d); self.assertEqual(p.returncode,2)
 def test_impossible_ctr_rejected(self):
  d=base(); d['rows'][0]['ctr']=50; p,o=run(d); self.assertEqual(p.returncode,2)
 def test_low_rank_and_cannibalization(self):
  d=base(); d['coverage'][0]['status']='covered'; d['rows'][0]['position']=50; p,o=run(d); self.assertEqual(o['records'][0]['category'],'low_rank_authority_or_technical_issue'); d['rows'][0]['cannibalization']=True; p,o=run(d); self.assertEqual(o['records'][0]['category'],'cannibalization')
 def test_irrelevant_navigational_intent(self):
  d=base(); d['rows'][0]['intent']='navigational'; p,o=run(d); self.assertEqual(o['records'][0]['category'],'irrelevant_brand_navigational_no_click_answer')
 def test_documented_intent_mismatch_before_low_rank(self):
  d=base(); d['coverage'][0]['status']='covered'; d['rows'][0].update(position=65,intent_mismatch=True); p,o=run(d); self.assertEqual(o['records'][0]['category'],'existing_page_content_or_intent_adjustment')
 def test_csv_whitespace_formula_and_full_evidence_fields(self):
  with tempfile.TemporaryDirectory() as x:
   d=base(); d['rows'][0]['query']='  =SUM(A1:A2)'; i=Path(x)/'i.json'; o=Path(x)/'o.json'; c=Path(x)/'o.csv'; i.write_text(json.dumps(d)); p=subprocess.run([sys.executable,str(SCRIPT),str(i),'--output',str(o),'--csv',str(c)],text=True,capture_output=True); self.assertEqual(p.returncode,0); row=list(csv.DictReader(c.open()))[0]; self.assertTrue(row['query'].startswith("'")); self.assertIn('property',row); self.assertIn('coverage_evidence',row); self.assertIn('limitations',row)
if __name__=='__main__': unittest.main()
