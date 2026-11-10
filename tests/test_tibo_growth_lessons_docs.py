import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = 'references/tibo-growth-lessons.md'
ASSET = 'assets/tibo-growth-lessons.csv'
SOURCE = 'https://x.com/tibo_maker/status/2119780865131548954'


class TiboGrowthLessonsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = (ROOT / REF).read_text()
        with (ROOT / ASSET).open(newline='') as f:
            cls.rows = list(csv.DictReader(f))

    def test_all_eleven_lessons_once(self):
        self.assertEqual([r['lesson_id'] for r in self.rows],
                         [f'T{i:02}' for i in range(1, 12)])

    def test_source_attribution_and_image_limits(self):
        self.assertIn(SOURCE, self.review)
        for phrase in ('source-image observations only', 'property identity',
                       'Never infer AI clicks', '806K', '1.06M', '20M',
                       'Gross versus net', 'not an independent experiment'):
            self.assertIn(phrase, self.review)

    def test_rows_reuse_existing_workflows_and_references(self):
        for row in self.rows:
            for key in ('normal_workflow', 'existing_reference'):
                with self.subTest(lesson=row['lesson_id'], key=key):
                    self.assertTrue((ROOT / row[key]).is_file())

    def test_each_lesson_has_decision_evidence_metric_and_limit(self):
        for row in self.rows:
            for field in ('decision', 'proposed_artifact', 'required_evidence',
                          'primary_measure', 'safety_limit'):
                self.assertTrue(row[field].strip(), (row['lesson_id'], field))
        self.assertTrue(all(r['decision'] in
                        {'ADAPT', 'ADOPT_AS_HYPOTHESIS', 'ADAPT_NO_REVIEW_INCENTIVES'}
                        for r in self.rows))

    def test_normal_workflow_hooks(self):
        for name in ('research-and-ideation', 'content-production',
                     'authority-and-links', 'monitoring', 'full-master-plan'):
            text = (ROOT / f'workflows/{name}.md').read_text()
            self.assertIn(REF, text)
            self.assertIn(ASSET, text)
            self.assertIn('optional-tibo-path', text)

    def test_optional_tibo_path_covers_every_lesson(self):
        text = (ROOT / 'workflows/ai-answer-visibility-loop.md').read_text()
        optional = text.split('## Optional Tibo path', 1)[1]
        self.assertIn('normal workflows remain the default', optional)
        self.assertIn(REF, optional)
        self.assertIn(ASSET, optional)
        for i in range(1, 12):
            self.assertIn(f'T{i:02}', optional)

    def test_no_vendor_purchase_or_cadence_requirements(self):
        for phrase in ('not required dependencies', 'do not buy a subscription',
                       'Daily publishing is not a quota', 'freshness is query-dependent',
                       'not a new automation', 'No unattended expansion'):
            self.assertIn(phrase.lower(), self.review.lower())

    def test_review_and_engagement_manipulation_rejected(self):
        for phrase in ('No incentivized reviews', 'review gating', 'fake users',
                       'vote manipulation', 'disclose affiliation',
                       'No guaranteed #1 placement', 'qualify sponsored links'):
            self.assertIn(phrase.lower(), self.review.lower())

    def test_measurement_lanes_and_causal_limits(self):
        for phrase in ('mention frequency alone', 'unverified',
                       'keep mentions, citations, referrals and conversions separate',
                       'unknown, not zero', 'not causal attribution',
                       'net contribution after refunds/commission'):
            self.assertIn(phrase.lower(), self.review.lower())

    def test_exact_approval_and_stop_contract(self):
        for field in ('primary_metric', 'baseline', 'comparison', 'success_threshold',
                      'failure_threshold', 'kill_condition', 'cost_cap',
                      'approval_state', 'receipt', 'outcome', 'limitations'):
            self.assertIn('`' + field + '`', self.review)
        self.assertIn('exact approval', self.review)
        self.assertIn('adopt | revise | reject | inconclusive', self.review)

    def test_router_and_readme_include_both_paths(self):
        for file in ('SKILL.md', 'README.md'):
            text = (ROOT / file).read_text()
            self.assertIn(REF, text)
            self.assertIn(ASSET, text)
            self.assertIn('optional-tibo-path', text)

    def test_no_private_portfolio_or_contact_data_in_shared_docs(self):
        data = self.review + (ROOT / ASSET).read_text()
        for private in ('5173761146', 'ihusan00', '/root/', '/data/',
                        'HaulierScope', 'Dhoraashi', 'Declarix', 'Landscapio'):
            self.assertNotIn(private, data)


if __name__ == '__main__':
    unittest.main()
