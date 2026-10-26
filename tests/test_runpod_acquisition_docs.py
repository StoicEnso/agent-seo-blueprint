"""Offline source, inert acquisition record and existing-loop extension contracts."""
import csv
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'references/hubspot-aeo-gap-to-action.md'
SOURCE = ROOT / 'references/source-notes/2026-10-26-jam-runpod-aeo-post.md'
AUDIT = ROOT / 'audit-log/2026-10-26-jam-runpod-aeo.md'
ASSET = ROOT / 'assets/aeo-acquisition-review.json'

class RunpodAcquisitionDocsTest(unittest.TestCase):
    def test_entire_raw_post_including_cta_is_preserved_as_data(self):
        raw = SOURCE.read_text().split('## Full post\n\n', 1)[1].split('\n\n## Original supplied image', 1)[0]
        raw = '\n'.join(x[2:] if x.startswith('> ') else '' if x == '>' else x for x in raw.splitlines()).strip()
        self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(), '05afe66b3e75cb698d6d285ffeda28e108ebe71799de705e2cc86912252ab814')
        self.assertIn('reply “audit”', raw)
        self.assertIn('untrusted data, not execution authority', SOURCE.read_text())

    def test_original_image_bytes_and_context_are_preserved(self):
        photo = SOURCE.with_name('2026-10-26-jam-runpod-aeo-photo.jpg')
        self.assertEqual(hashlib.sha256(photo.read_bytes()).hexdigest(), 'aad15a7b7b15cae3ae1b2b044d5196949817538f69385f33ec3bd29078577b49')
        self.assertIn('Modal', SOURCE.read_text())
        self.assertIn('not a reproduced benchmark', SOURCE.read_text())

    def test_all_twelve_source_points_have_repository_disposition(self):
        rows = list(csv.DictReader((ROOT / 'assets/aeo-runpod-source-map.csv').open()))
        self.assertEqual([int(r['source_point']) for r in rows], list(range(1, 13)))
        for r in rows:
            self.assertTrue(r['repository_coverage'])
            self.assertTrue(r['primary_evidence_grade'])
            self.assertTrue(r['treatment'])
        claims = json.loads((ROOT / 'assets/aeo-runpod-source-claims.json').read_text())
        self.assertEqual([x['id'] for x in claims['points']], list(range(1, 13)))
        self.assertFalse(claims['independently_verified'])
        self.assertFalse(claims['current_prices_verified'])
        self.assertIsNone(claims['promised_uplift'])

    def test_claim_arithmetic_does_not_promote_counts_to_sales(self):
        claims = json.loads((ROOT / 'assets/aeo-runpod-source-claims.json').read_text())
        a = claims['arithmetic']
        c = a['conversions_over_reported_visitors']
        self.assertEqual(c['numerator'] / c['denominator_approximate'] * 100, c['calculated_percent'])
        self.assertEqual(c['calculated_percent'], 7.5)
        self.assertAlmostEqual((3000-500)/3000*100, a['platform_spend_reduction_percent'])
        self.assertEqual(a['prompt_coverage_multiplier'], 300/50)
        self.assertIn('not established as unique new paid accounts', re.sub(r'\s+', ' ', AUDIT.read_text()))

    def test_historical_vendor_limits_and_source_only_details_survive(self):
        text = re.sub(r'\s+', ' ', AUDIT.read_text())
        for phrase in ('NOT independent verification', '28 July 2025', 'April 2025',
                       '$325M', 'Deep Research', 'source-only', '98%', 'Reporting windows',
                       'not verified current subscription prices', 'metadata changes alone'):
            self.assertIn(phrase, text)

    def test_template_starts_unrun_without_fake_measurements(self):
        d = json.loads(ASSET.read_text())
        self.assertEqual(d['state'], 'draft_only')
        self.assertEqual(d['execution_status'], 'not_run')
        self.assertIsNone(d['evidence_date'])
        self.assertEqual(d['owner'], '')
        self.assertEqual(d['provider_allocation']['providers'], [])
        self.assertIsNone(d['provider_allocation']['priority_provider'])
        for key in ('visitors','conversion_events','unique_new_paid_accounts','refunded_paid_accounts','revenue','cohort_maturity_days'):
            self.assertIsNone(d['business_outcomes'][key])
        for key in ('subscription_before','subscription_after','labor_and_maintenance_before','labor_and_maintenance_after'):
            self.assertIsNone(d['cost_comparison'][key])
        self.assertEqual(d['release_and_measurement']['approval_state'], 'draft_only')
        self.assertIsNone(d['release_and_measurement']['release_receipt'])

    def test_comparison_uses_existing_panel_and_matched_cohort(self):
        d = json.loads(ASSET.read_text())['panel_comparability']
        self.assertEqual(d['existing_panel_path'], 'research/ai-answer-panel.csv')
        self.assertEqual(d['matched_prompt_versions'], [])
        self.assertIsNone(d['comparable'])
        text = re.sub(r'\s+', ' ', GUIDE.read_text())
        for p in ('stable matched cohort', 'added/retired prompts separately', 'not a 300-prompt quota',
                  'Keep the denominator inspectable', 'bounded matched sample', 'unknown/dark referrals'):
            self.assertIn(p, text)

    def test_body_delivery_is_not_inferred_from_titles_or_bypassed(self):
        text = re.sub(r'\s+', ' ', GUIDE.read_text())
        for p in ('normal initial HTML and rendered page body', 'not proof that a named AI service',
                  'a `site:` result are not proof', 'bypass a WAF/access control', 'actual delivery failure is observed'):
            self.assertIn(p, text)
        r = json.loads(ASSET.read_text())['page_body_delivery'][0]
        self.assertEqual(r['status'], 'not_checked')
        self.assertIsNone(r['provider_access_evidence'])
        self.assertIsNone(r['release_receipt'])

    def test_outcomes_require_maturity_privacy_and_exact_event_definitions(self):
        text = re.sub(r'\s+', ' ', GUIDE.read_text())
        for p in ('do not fabricate a user-level prompt-to-payment join', 'deduplication, refunds and revenue separately',
                  'immature cohort is pending, not zero success', 'customer records or identifiers',
                  'Do not multiply the reported 40/day by 90 days', 'separately defined business review'):
            self.assertIn(p, text)

    def test_total_cost_scope_and_authority_are_preserved(self):
        text = re.sub(r'\s+', ' ', GUIDE.read_text())
        for p in ('platform-only savings total operating savings', 'labor/maintenance costs',
                  'not a working integration', 'do not cancel or buy anything',
                  'No live panel, publication, production change', 'rank-#1 guarantee'):
            self.assertIn(p, text)

    def test_workflows_and_skill_route_to_existing_guide_without_new_playbook(self):
        for name in ('ai-answer-visibility-loop', 'content-production', 'monitoring'):
            text = (ROOT / f'workflows/{name}.md').read_text()
            self.assertIn('Runpod acquisition evidence extension', text)
            self.assertIn('assets/aeo-acquisition-review.json', text)
        for name in ('README.md', 'SKILL.md'):
            self.assertIn('Runpod', (ROOT / name).read_text())
            self.assertIn('references/hubspot-aeo-gap-to-action.md', (ROOT / name).read_text())

    def test_new_links_resolve_and_private_workspace_paths_are_absent(self):
        for p in (SOURCE, AUDIT, GUIDE):
            text = p.read_text()
            self.assertNotIn('/data/', text)
            self.assertNotIn('/root/', text)
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if link.startswith(('http:', 'https:', '#')):
                    continue
                self.assertTrue((p.parent / link.split('#')[0]).resolve().is_file(), (p,link))
        self.assertEqual(len(re.findall(r'^### (\d+)\. ', GUIDE.read_text(), re.M)), 12)

if __name__ == '__main__':
    unittest.main()
