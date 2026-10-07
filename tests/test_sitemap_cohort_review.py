"""Parent offline contracts only; no live GSC collection or write enforcement."""
from pathlib import Path
import csv
import importlib.util
import io
import json
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


class SitemapCohortReviewTests(unittest.TestCase):
    def test_header_separates_metrics_collection_and_submission(self):
        rows = list(csv.reader(io.StringIO(read('assets/sitemap-cohort-evidence.csv'))))
        self.assertEqual(len(rows), 1, 'Repository asset must contain no site observations')
        headers = rows[0]
        self.assertEqual(len(headers), len(set(headers)))
        self.assertEqual(len(headers), 40)
        for field in ('cohort_id', 'sitemap_kind', 'index_parent_url', 'submission_route', 'submission_state',
                      'processing_state', 'filter_available', 'report_name', 'metric_name', 'metric_unit',
                      'collection_state', 'report_count', 'inspection_sample_n', 'owner', 'approval_scope',
                      'actual_receipt', 'follow_up_at'):
            self.assertIn(field, headers)

    def test_zero_unknown_and_comma_notes_roundtrip_through_asset_schema(self):
        fields = next(csv.reader(io.StringIO(read('assets/sitemap-cohort-evidence.csv'))))
        stream = io.StringIO()
        writer = csv.DictWriter(stream, fields)
        writer.writeheader()
        writer.writerow({'cohort_id': 'synthetic-zero', 'metric_name': 'indexed', 'metric_unit': 'URLs',
                         'report_count': 0, 'collection_state': 'OBSERVED',
                         'alternative_explanations': 'sample only, not a census'})
        writer.writerow({'cohort_id': 'synthetic-unknown', 'report_count': '', 'collection_state': 'MISSING_ACCESS'})
        values = list(csv.DictReader(io.StringIO(stream.getvalue())))
        self.assertEqual(values[0]['report_count'], '0')
        self.assertEqual(values[0]['alternative_explanations'], 'sample only, not a census')
        self.assertEqual(values[1]['report_count'], '')
        self.assertEqual(values[1]['collection_state'], 'MISSING_ACCESS')

    def test_routes_write_to_workspace_not_source_template(self):
        for name in ('site-audit', 'monitoring', 'technical-seo-maintenance'):
            body = read(f'workflows/{name}.md')
            self.assertIn('audits/<date>_sitemap-cohort-evidence.csv', body.split('---', 2)[1])
        body = read('workflows/technical-seo-maintenance.md')
        self.assertIn('Never put client observations into the repository template', body)
        steps = body.split('### Bounded operating pass', 1)[1]
        self.assertEqual(len(re.findall(r'^\d+\. ', steps, re.MULTILINE)), 7)
        self.assertIn('raw-source authoritative, not a new `report.py` renderer', body)
        self.assertIn('helper `gsc_pull.py` remains a stub', body)
        self.assertIn('No live write is required', body)

    def test_report_definitions_and_proposal_authority_remain_distinct(self):
        gsc = read('references/integrations/gsc.md')
        method = read('references/playbooks/maintenance/technical-seo-maintenance.md')
        workflow = read('workflows/technical-seo-maintenance.md')
        self.assertIn('top-level report', gsc)
        self.assertIn('auto-discovered children', gsc)
        self.assertIn('report/API submission', gsc)
        self.assertIn('robots.txt', gsc)
        self.assertIn('specific sitemap/index filter is not', gsc)
        self.assertIn('Proposal and inspection are read-only', gsc)
        self.assertIn('A proposal needs no new write grant', method)
        self.assertIn('Reuse a usable exact child/index filter', workflow)
        self.assertIn('fresh scope/target check', method)
        self.assertIn('does not remove its pages from the index', method)
        self.assertIn('Preserve existing scoped approvals and holds', workflow)

    def test_source_bounds_and_receipts_do_not_turn_into_indexation_guarantees(self):
        method = read('references/playbooks/maintenance/technical-seo-maintenance.md')
        for phrase in ('https://support.google.com/webmasters/answer/7451001',
                       'https://support.google.com/webmasters/answer/7440203',
                       'January 2025', 'incomplete examples are a diagnostic sample',
                       'leave the ratio unknown', 'successful live test cannot prove',
                       'not proof of a ranking, crawl or indexing improvement'):
            self.assertIn(phrase, method)
        self.assertIn('No live write is required', read('workflows/technical-seo-maintenance.md'))
        self.assertIn('Membership changes or a newly available filter require a new baseline', read('workflows/monitoring.md'))

    def test_raw_evidence_packet_retains_limits_using_existing_note_helper(self):
        spec = importlib.util.spec_from_file_location('sitemap_report_review', ROOT / 'scripts/report.py')
        report = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(report)
        data = {'source': 'synthetic-test-only', 'cohort_id': 'fixture', 'metric': 'indexed',
                'observed_count': 0, 'unknown_expected_count': None, 'collection_state': 'PARTIAL',
                'membership_revision': 'fixture-v1', 'limits': ['URL examples incomplete'],
                'actual_receipt': None}
        with tempfile.TemporaryDirectory() as workspace:
            path = report.render_note(workspace, 'audits', 'sitemap-evidence-packet', data)
            self.assertEqual(json.loads(path.read_text()), data)


if __name__ == '__main__':
    unittest.main()
