import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ViralDemandTests(unittest.TestCase):
 def test_template_no_invented_metrics(self):
  d=json.loads((ROOT/'assets/content-to-demand-comparison.json').read_text())
  self.assertEqual(d['comparison_status'],'INCOMPARABLE');self.assertEqual(d['publication_status'],'NOT_APPROVED')
  self.assertTrue(all(v is None for v in d['funnel'].values()))
  self.assertIn('gross_or_net',d['required_revenue_fields']);self.assertIn('crosspost_overlap',d['required_social_fields'])
 def test_source_lineage_and_audio_limit(self):
  d=json.loads((ROOT/'assets/content-to-demand-comparison.json').read_text());s=(ROOT/d['source_review']).read_text()
  self.assertEqual(len(d['source_urls']),4)
  for u in d['source_urls']:self.assertIn(u,s)
  self.assertIn('no spoken text was invented',s);self.assertIn('assessment remains incomplete',s)
 def test_method_gate_and_non_causal_metrics(self):
  s=(ROOT/'references/playbooks/research/finding-and-validating-niches.md').read_text()
  for term in ['INCOMPARABLE','gross/net basis','unique posts/creators','A download is not','continue | revise | stop | inconclusive','not a unique audience','content-to-demand-comparison.json']:self.assertIn(term,s)
 def test_route_reuse_not_backlink_duplication(self):
  s=(ROOT/'references/playbooks/content/cross-platform-commercial-intent-distribution.md').read_text();self.assertIn('do not clone',s);self.assertIn('content-to-demand-comparison.json',s)
  s=(ROOT/'workflows/research-and-ideation.md').read_text();self.assertIn('INCOMPARABLE',s)
if __name__=='__main__':unittest.main()
