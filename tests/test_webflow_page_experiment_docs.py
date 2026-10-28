"""Source fidelity and inert matched-URL-review documentation contracts."""
import csv
import hashlib
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GUIDE=ROOT/'references/hubspot-aeo-gap-to-action.md'
AUDIT=ROOT/'audit-log/2026-10-28-jam-webflow-aeo.md'
SOURCE=ROOT/'references/source-notes/2026-10-28-jam-webflow-aeo-post.md'

def norm(p): return re.sub(r'\s+',' ',p.read_text())
def load(p): return json.loads((ROOT/p).read_text())

class WebflowPageExperimentDocsTest(unittest.TestCase):
    def test_full_post_and_original_image_are_exact(self):
        d=load('assets/aeo-webflow-source-claims.json')
        raw=SOURCE.read_text().split('## Full post\n\n',1)[1].split('\n\n## Original supplied image',1)[0]
        raw='\n'.join(x[2:] if x.startswith('> ') else '' if x=='>' else x for x in raw.splitlines()).strip()
        # Pins are replaced with observed source hashes by the one-off audit builder.
        self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(),'f5ef092071912f6a01a689bc3e67da63fa092fef5d11881afed68d980e4a6418')
        self.assertEqual(hashlib.sha256(SOURCE.with_name('2026-10-28-jam-webflow-aeo-photo.jpg').read_bytes()).hexdigest(),'6188ef5f083f9a78e0984cfdb5c89d155ec5c72c043df296f85744d089ffc3e4')
        self.assertIn('reply “audit”',raw)
        self.assertIn('untrusted data, not execution authority',SOURCE.read_text())
        self.assertIn('not a reproduced benchmark',SOURCE.read_text())
        self.assertEqual(d['source_url'],'https://x.com/wespreadjam/status/2115174505459122445')

    def test_every_fourteen_source_points_has_a_disposition(self):
        with (ROOT/'assets/aeo-webflow-source-map.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual([int(x['source_point']) for x in rows],list(range(1,15)))
        for r in rows:
            self.assertTrue(r['repository_coverage'])
            self.assertTrue(r['treatment'])
        d=load('assets/aeo-webflow-source-claims.json')
        self.assertEqual([x['id'] for x in d['points']],list(range(1,15)))
        self.assertFalse(d['independently_verified'])
        self.assertFalse(d['raw_cohorts_available'])
        self.assertFalse(d['p_values_reproduced'])
        self.assertIsNone(d['promised_uplift'])

    def test_claim_arithmetic_and_metric_scope(self):
        a=load('assets/aeo-webflow-source-claims.json')['arithmetic']
        self.assertAlmostEqual(a['template_signup_growth_percent'],(983/168-1)*100)
        self.assertAlmostEqual(a['sov_relative_growth_percent'],(64/33-1)*100)
        self.assertEqual(a['sov_percentage_point_change'],31)
        self.assertEqual(a['signup_share_multiplier'],2)
        self.assertEqual(a['signup_cvr_ratio'],6)
        self.assertEqual(load('assets/aeo-webflow-source-claims.json')['statistical_claims']['reported_question_share_improved_percent'],70)
        self.assertIn('70% of questions',AUDIT.read_text())
        t=norm(AUDIT)
        for x in ('free Webflow account','share of total signups','not necessarily twice','non-brand SEO','NOT independent verification','historical 2025'):
            self.assertIn(x,t)

    def test_raw_and_control_adjusted_effects_stay_distinct(self):
        a=load('assets/aeo-webflow-source-claims.json')['arithmetic']
        self.assertAlmostEqual(a['toc_ai_raw_growth_percent'],(127/119-1)*100)
        self.assertEqual(a['toc_ai_reported_control_adjusted_percent'],60)
        self.assertAlmostEqual(a['toc_click_raw_growth_percent'],(220/191-1)*100)
        self.assertEqual(a['toc_click_reported_control_adjusted_percent'],23)
        self.assertAlmostEqual(a['heading_ai_raw_growth_percent'],(70/41-1)*100)
        self.assertEqual(a['heading_ai_reported_control_adjusted_percent'],58)
        self.assertNotAlmostEqual(a['toc_ai_raw_growth_percent'],a['toc_ai_reported_control_adjusted_percent'])
        self.assertIn('adjusted effects and p-values cannot be independently reproduced',norm(AUDIT))

    def test_four_week_results_and_five_week_design_are_not_conflated(self):
        s=load('assets/aeo-webflow-source-claims.json')['statistical_claims']
        self.assertEqual((s['test_urls'],s['control_urls'],s['design_weeks'],s['reported_result_weeks']),(10,10,5,4))
        self.assertFalse(s['random_assignment_established'])
        self.assertFalse(s['control_means_and_variance_available'])
        for x in ('five-week design','four-week outcome statements','not reproduced','randomization'):
            self.assertIn(x,norm(AUDIT))

    def test_template_has_no_simulated_results_or_write_approval(self):
        d=load('assets/aeo-page-experiment-review.json')
        self.assertEqual((d['state'],d['execution_status']),('draft_only','not_run'))
        self.assertEqual(d['candidate_pages'],[])
        self.assertEqual(d['design']['test_urls'],[])
        self.assertEqual(d['design']['control_urls'],[])
        self.assertTrue(all(v is None for v in d['counts'].values()))
        self.assertTrue(all(v is None for v in d['results'].values()))
        self.assertEqual(d['release']['approval_state'],'draft_only')
        self.assertIsNone(d['release']['release_receipt'])
        self.assertEqual(d['decision']['causality'],'not_established')
        self.assertTrue(d['decision']['owner_review_required_before_expansion'])

    def test_experiment_requires_predefined_units_matching_and_precision(self):
        d=load('assets/aeo-page-experiment-review.json')['design']
        self.assertEqual(d['assignment_unit'],'url')
        for x in ('assignment_method','primary_outcome_event','measurement_unit','aggregation_method','analysis_plan','estimator','minimum_evidence_or_precision_rule','uncertainty_method','repeated_observation_handling','multiple_comparison_policy','interim_look_policy','cost_cap'):
            self.assertIn(x,d)
            self.assertIsNone(d[x])
        for x in ('one** treatment per cohort','before** the change','randomized or matched observational','do not keep checking','contamination','repeated observations at URL level'):
            self.assertIn(x,norm(GUIDE))

    def test_existing_page_copy_is_not_a_keyword_or_volume_factory(self):
        for x in ('four elements are a copy-review aid','not a keyword formula','existing working conversion paths and approved claims','team×tool pages','1500pages'):
            if x=='1500pages': self.assertNotIn(x,norm(GUIDE))
            else:self.assertIn(x,norm(GUIDE))
        d=load('assets/aeo-page-experiment-review.json')['copy_review']
        for x in ('buyer_question','truthful_brand_context','actual_target_user','supported_outcome','duplicate_and_product_truth_review'):
            self.assertIn(x,d)

    def test_estimator_and_zero_denominator_limits_are_explicit(self):
        t=norm(GUIDE)
        for x in ('multiplicative difference-in-differences','control_post/control_pre','formula is not claimed to reproduce','ratio undefined, not zero','Percentage-point change','low p-value is not a guarantee'):
            self.assertIn(x,t)
        # Synthetic arithmetic illustration only, not a live result or Graphite reconstruction.
        self.assertAlmostEqual(((120/100)/(90/100)-1)*100,33.33333333333333)

    def test_community_drafts_do_not_turn_into_posting_authority(self):
        t=norm(GUIDE)
        for x in ('A cited thread is not a marketing invitation','never automatically post','hide affiliation','exact-word approval','sentiment method/denominator'):
            self.assertIn(x,t)
        d=load('assets/aeo-page-experiment-review.json')['community_review']
        for x in ('cited_thread_url','provider_prompt_evidence','sentiment_definition_and_denominator','reviewer','exact_word_approval','post_receipt','business_outcome'):
            self.assertIsNone(d[x])

    def test_routes_reuse_current_guide_and_preserve_earlier_extensions(self):
        for rel in ['README.md','workflows/content-production.md','workflows/monitoring.md','assets/aeo-site-evaluation-brief.md']:
            t=(ROOT/rel).read_text()
            self.assertIn('aeo-page-experiment-review.json',t)
            self.assertIn('references/hubspot-aeo-gap-to-action.md',t)
        t=GUIDE.read_text()
        self.assertIn('Runpod acquisition evidence extension',t)
        self.assertIn('All twelve source points',t)
        self.assertEqual(len(re.findall(r'^### (\d+)\. ',t,re.M)),12)
        for x in ('ordinary-search or conversion harm','no_clear_result','unique, disjoint test/control URLs','parallel-trend assumptions'):
            self.assertIn(x,norm(GUIDE))

    def test_new_links_resolve_and_no_private_paths_leak(self):
        for p in (SOURCE,AUDIT,GUIDE):
            text=p.read_text()
            self.assertNotIn('/data/',text)
            self.assertNotIn('/root/',text)
            for link in re.findall(r'\]\(([^)]+)\)',text):
                if link.startswith(('http:','https:','#')):continue
                self.assertTrue((p.parent/link.split('#')[0]).resolve().is_file(),(p,link))

if __name__=='__main__':unittest.main()
