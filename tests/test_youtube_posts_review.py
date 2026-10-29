import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'audit-log/evidence/2026-10-29-youtube-posts'

class YouTubePostsReviewTests(unittest.TestCase):
    def setUp(self):
        self.form = json.loads((ROOT / 'assets/youtube-post-review.json').read_text())
        self.claims = json.loads((EVIDENCE / 'claims.json').read_text())
        self.play = (ROOT / 'references/playbooks/authority/hosted-publishing-experiments.md').read_text()
        self.review = (ROOT / 'audit-log/2026-10-29-youtube-posts-review.md').read_text()

    def test_pinned_original_evidence(self):
        self.assertEqual(len(self.claims['sha256']), 4)
        for name, digest in self.claims['sha256'].items():
            self.assertEqual(hashlib.sha256((EVIDENCE / name).read_bytes()).hexdigest(), digest)

    def test_exact_source_and_date(self):
        self.assertEqual(self.claims['source_url'], 'https://x.com/jespernissenseo/status/2115426892459254182')
        self.assertEqual(self.claims['checked_on'], '2026-10-29')
        self.assertEqual(self.form['source_url'], self.claims['source_url'])

    def test_all_claim_dispositions(self):
        self.assertEqual({r['id'] for r in self.claims['claims']}, {'post-format','rank-13-minutes','query','indexing-tool','backlinks','entities','local','traffic','unlimited','policy'})
        for r in self.claims['claims']:
            self.assertTrue(r['reason'])
            self.assertTrue(r['disposition'])

    def test_no_independent_rank_claim(self):
        self.assertIs(self.claims['independent_google_rank_reproduced'], False)
        self.assertIn('not an independently reproduced search result', self.review)
        self.assertEqual(self.claims['image_query'], 'Youtube community posts exploded in visibility')

    def test_template_cannot_claim_execution(self):
        self.assertEqual(self.form['state'], 'DRAFT_RESEARCH_ONLY')
        self.assertEqual(self.form['execution'], 'manual_review_only')
        self.assertEqual(self.form['verdict'], 'NOT_RUN')
        self.assertFalse(self.form['expansion_authorized'])
        self.assertIn('not an approval validator', self.play)

    def test_approval_stays_empty(self):
        a = self.form['approval']
        self.assertEqual(a['state'], 'EXACT_PUBLICATION_NOT_APPROVED')
        self.assertTrue(all(v is None for k,v in a.items() if k != 'state'))
        for k in ['project','channel_url','channel_role','eligibility_evidence','availability_checked_at']:
            self.assertIsNone(self.form[k])
        self.assertTrue(all(v is None for v in self.form['draft'].values()))

    def test_no_fabricated_results(self):
        self.assertEqual(self.form['observations'], [])
        for section in ['publication','page_evidence','outcomes']:
            self.assertTrue(all(v is None for v in self.form[section].values()))

    def test_no_indexer_or_scheduler(self):
        self.assertFalse(self.form['indexing_service_used'])
        self.assertFalse(self.form['measurement_plan']['schedules_created'])
        self.assertIn('Do not submit to Primeindexer', self.play)
        self.assertIn('a plan, not scheduled jobs', self.play)

    def test_eligibility_and_feature_distinction(self):
        for term in ['Communities','supervised','Made-for-Kids','24-hour','Germany','channel-role']:
            self.assertIn(term, self.review)
        self.assertIn('not the same public Posts-tab surface', self.play)

    def test_project_evidence_required(self):
        for term in ['demand_evidence','original_evidence','owned_page_overlap_review','disclosure']:
            self.assertIn(term, self.form)
        for term in ['primary_goal','success_threshold','query_panel','baseline','cost_cap']:
            self.assertIn(term, self.form['measurement_plan'])

    def test_metrics_remain_separate(self):
        for term in ['ordinary_search_visibility','google_ai_overview_citation','other_provider_citations','youtube_engagement','qualified_referrals','leads','conversions','revenue']:
            self.assertIn(term, self.form['outcomes'])
        self.assertIn("not the project's own Search Console property", self.play)

    def test_no_followed_link_or_causal_claim(self):
        for term in ['rendered destination `href`/`rel`','correlation is not causation','exact-phrase retrieval is not competitive demand','Google still prohibits link spam']:
            self.assertIn(term, self.play)
        self.assertIn('no outbound project website URL', self.review)

    def test_current_workflows_route_existing_home(self):
        for rel in ['workflows/authority-and-links.md','workflows/content-production.md','workflows/monitoring.md','README.md']:
            text = (ROOT / rel).read_text()
            self.assertIn('assets/youtube-post-review.json', text)
            self.assertIn('references/playbooks/authority/hosted-publishing-experiments.md', text)
            self.assertIn('audit-log/2026-10-29-youtube-posts-review.md', text)

    def test_original_parasite_intake_preserved(self):
        self.assertTrue((ROOT / 'assets/parasite-seo-idea-pilots.csv').exists())
        self.assertIn('11-idea intake', self.play)
        self.assertIn('henry/parasite-source-20261026', self.review)
        self.assertGreaterEqual(len(self.form['measurement_plan']['stop_conditions']), 6)

if __name__ == '__main__':
    unittest.main()
