import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(name):
    return (ROOT / name).read_text(encoding='utf-8')


class RecurringWorkReviewTest(unittest.TestCase):
    def test_wrapper_has_full_runbook_and_manual_output_contract(self):
        body = text('workflows/recurring-work-delivery.md')
        frontmatter = body.split('---', 2)[1]
        for key in ('title:', 'goal:', 'playbooks:', 'scripts:', 'integrations:', 'outputs:'):
            self.assertIn(key, frontmatter)
        self.assertEqual(len(re.findall(r'^\d+\. \*\*', body, re.MULTILINE)), 6)
        for output in ('monitoring/recurring-work-ledger.md', 'weekly-work-review.md', 'monthly-outcome-review.md'):
            self.assertIn(output, body)
        self.assertIn('not an implemented executor or security control', body)
        self.assertIn('this pass creates no timer', body)

    def test_routing_and_readme_cover_all_actual_workflows(self):
        names = {p.stem for p in (ROOT / 'workflows').glob('*.md')}
        readme = text('README.md')
        rows = set(re.findall(r'^\| \*\*([a-z-]+)\*\* \|', readme, re.MULTILINE))
        self.assertTrue(names.issubset(rows), names - rows)
        self.assertIn(f'#the-workflows-{len(names)}-runbooks', readme)
        self.assertNotIn('#the-workflows-11-runbooks', readme)
        router = text('SKILL.md').split('## Route by intent', 1)[1].split('## Course knowledge', 1)[0]
        self.assertIn('workflows/recurring-work-delivery.md', router)

    def test_new_runbook_references_existing_paths(self):
        for name in ('workflows/recurring-work-delivery.md', 'assets/recurring-work-ledger.md'):
            body = text(name)
            refs = re.findall(r'(?:workflows|assets|references|scripts)/[A-Za-z0-9_./-]+\.(?:md|py)', body)
            for reference in refs:
                self.assertTrue((ROOT / reference).is_file(), reference)

    def test_ledger_keeps_decision_fields_and_aligned_template_row(self):
        body = text('assets/recurring-work-ledger.md')
        rows = [line for line in body.splitlines() if line.startswith('|')]
        cells = [[c.strip() for c in line.strip('|').split('|')] for line in rows]
        self.assertEqual(len(cells), 3)
        self.assertEqual(len(cells[0]), len(cells[1]))
        self.assertEqual(len(cells[0]), len(cells[2]))
        self.assertIn('Hypothesis / alternatives / confidence reason', cells[0])
        for required in ('Owner + approval', 'Risk + rollback', 'Receipt', 'Outcome/recheck + date'):
            self.assertIn(required, cells[0])
        self.assertIn('link existing detailed artifacts', body)
        self.assertIn('implementation separate from later outcome evidence', body)

    def test_old_numeric_promises_do_not_override_new_workflow(self):
        metrics = text('references/playbooks/research/seo-metrics.md')
        tools = text('references/playbooks/research/keyword-research-tools.md')
        for bad in ('~10 backlinks', '1-2 months', 'a DA-60 link is', 'Hard-skip anything under 100', 'Volume < 100 → skip'):
            self.assertNotIn(bad, metrics)
        for bad in ('All draw from the same data', 'the data matches', 'data is the same everywhere', 'around $29/mo'):
            self.assertNotIn(bad, tools)
        self.assertIn('low-volume, high-margin', metrics)
        self.assertIn('provider estimate saved in a CSV is still an estimate', text('references/playbooks/research/number-reconciliation.md'))

    def test_owner_handoffs_do_not_count_drafts_as_delivery_or_use_crawl_quotas(self):
        content = text('workflows/content-production.md')
        authority = text('workflows/authority-and-links.md')
        self.assertIn('recurring-work-delivery.md', content)
        self.assertIn('not a publication receipt', content)
        self.assertIn('never authorizes outreach', authority)
        self.assertIn('fresh destination evidence', authority)
        self.assertIn('Google does not publish a universal', text('references/playbooks/content/content-what-not-to-do.md'))
        self.assertNotIn('~30-40', text('references/playbooks/content/content-what-not-to-do.md'))
        self.assertNotIn('fixed multiplier', text('workflows/authority-and-links.md'))

    def test_missing_evidence_is_scoped_and_raw_manifest_roundtrips(self):
        workflow = text('workflows/recurring-work-delivery.md')
        self.assertIn('Pause only the affected action', workflow)
        self.assertIn('Keep independent safe work moving', workflow)
        self.assertIn('25,000', text('references/integrations/gsc.md'))
        spec = importlib.util.spec_from_file_location('report_review', ROOT / 'scripts/report.py')
        report = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(report)
        manifest = {'source': 'synthetic-test-only', 'collection_status': 'PARTIAL', 'observed_clicks': 0,
                    'unknown_conversion_value': None, 'limits': ['bounded rows'], 'data_state': 'final'}
        with tempfile.TemporaryDirectory() as workspace:
            saved = report.render_note(workspace, 'monitoring', 'collection-manifest', manifest)
            self.assertEqual(json.loads(saved.read_text()), manifest)
            snapshot = report.render_monitoring(workspace, {'site': 'example.test', 'period': 'test',
                                                         'metrics': {'clicks': 0}, 'notes': 'PARTIAL — see raw collection manifest.'})
            rendered = snapshot.read_text()
            self.assertIn('| clicks | 0 |', rendered)
            self.assertIn('PARTIAL', rendered)


if __name__ == '__main__':
    unittest.main()
