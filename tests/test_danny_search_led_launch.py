import csv
import hashlib
import json
import re
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DannySearchLedTests(unittest.TestCase):
    def load(self, path):
        return (ROOT / path).read_text(encoding='utf-8')

    def test_all_twenty_posts_are_unique_and_routed(self):
        self.assertNotIn(b'\r', (ROOT / 'assets/danny-search-led-claim-map.csv').read_bytes())
        with (ROOT / 'assets/danny-search-led-claim-map.csv').open(newline='') as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(list(range(1, 21)), [int(x['sequence']) for x in rows])
        self.assertEqual(20, len({x['post_id'] for x in rows}))
        self.assertEqual('1646368426246680579', rows[0]['post_id'])
        self.assertEqual('1646368527853711360', rows[-1]['post_id'])
        for row in rows:
            self.assertIn(row['post_id'], row['source_url'])
            self.assertRegex(row['source_text_sha256'], r'^[0-9a-f]{64}$')
            self.assertTrue((ROOT / row['existing_home']).is_file(), row)
            self.assertIn(row['decision'], {'already_covered', 'guardrail_added', 'source_claim_only', 'not_adopted'})
            self.assertTrue(row['safe_adaptation'])
        self.assertGreater(sum(x['decision'] == 'already_covered' for x in rows), 5)

    def test_orders_have_a_click_denominator(self):
        data = json.loads(self.load('assets/danny-search-led-scenarios.json'))
        self.assertEqual('illustrative_not_measured', data['status'])
        for row in data['corrected_examples']:
            calc = Decimal(str(row['eligible_searches'])) * Decimal(str(row['organic_click_share'])) * Decimal(str(row['visit_to_paid_rate']))
            self.assertEqual(Decimal(str(row['expected_orders'])), calc)
            self.assertLess(calc, Decimal('30'))
        self.assertEqual(Decimal('3.000'), Decimal('1500') * Decimal('0.10') * Decimal('0.02'))

    def test_existing_forecast_is_reused_and_not_paid_sales(self):
        data = json.loads(self.load('assets/danny-search-led-scenarios.json'))
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/forecast.py'), '--json'], input=json.dumps(data['forecast_pools']), text=True, capture_output=True, check=True)
        result = json.loads(run.stdout)
        self.assertEqual(0.1, result['base']['rows'][0]['eff_ctr'])
        self.assertEqual(round(1500 * 0.75 * 0.10), result['base']['totals']['m18'])
        self.assertNotIn('revenue', result)
        self.assertNotIn('sales', result)
        self.assertIn('not verified global demand', data['forecast_pools'][0]['name'])

    def test_no_country_or_order_guarantee(self):
        text = self.load('references/playbooks/research/number-reconciliation.md')
        for phrase in ['Do not triple a country volume', '3 expected orders, not 30', 'organic click share', 'already observed organic visits', 'Fractional expectations', 'labour, hosting', 'not measured customer counts']:
            self.assertIn(phrase, text)

    def test_metrics_do_not_prescribe_backlinks_or_rank_deadlines(self):
        text = self.load('references/playbooks/research/seo-metrics.md')
        self.assertIn('does not prescribe ten backlinks', text)
        self.assertIn('not Google ranking scores', text)
        self.assertNotIn('KD < 20 → rankable as a new site (~10 backlinks, 1-2 months)', text)
        self.assertNotIn('each 10 points is ~10× the previous', text)

    def test_product_hunt_uses_actual_link_evidence(self):
        text = self.load('references/playbooks/authority/startup-backlink-directory-submissions.md')
        for phrase in ['10–50 copies are not 10–50 independent endorsements', 'actual destination `href`', 'rendered `rel`', 'publication approval', 'not Google PageRank', 'No Product Hunt page or link attribute was live-verified']:
            self.assertIn(phrase, text)

    def test_free_assets_and_pricing_are_not_permission_or_rank_proof(self):
        text = self.load('references/playbooks/content/free-tools-strategy.md')
        self.assertIn('does not prove a ranking gain', text)
        self.assertIn('redistribution/commercial-use rights', text)
        self.assertIn('pricing hypothesis', text)
        self.assertIn('Paid conversion', self.load('workflows/research-and-ideation.md'))

    def test_existing_workflow_routes_and_no_set_forget(self):
        self.assertIn('zero followers', self.load('SKILL.md'))
        self.assertIn('danny-search-led-claim-map.csv', self.load('README.md'))
        self.assertIn('Product Hunt launch claims', self.load('workflows/authority-and-links.md'))
        self.assertIn('not set-and-forget', self.load('workflows/monitoring.md'))
        self.assertIn('No new collector', self.load('audit-log/2026-10-27-danny-search-led-launch.md'))

    def test_added_markdown_links_resolve(self):
        for path in ['references/playbooks/research/number-reconciliation.md', 'references/playbooks/research/seo-metrics.md', 'references/playbooks/content/free-tools-strategy.md', 'references/playbooks/authority/startup-backlink-directory-submissions.md']:
            text = self.load(path)
            for target in re.findall(r'\[[^]]*\]\(([^)]+)\)', text):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                self.assertTrue((ROOT / path).parent.joinpath(target.split('#')[0]).is_file(), (path, target))


if __name__ == '__main__':
    unittest.main()
