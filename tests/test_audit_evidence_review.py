import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_evidence_review', ROOT / 'scripts/audit_evidence_review.py')
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def fixture():
    return json.loads((ROOT / 'assets/process-first-audit-input.json').read_text())


def observation(provider='example_engine', status='observed', mentioned=True):
    return {'provider': provider, 'surface': 'search', 'locale': 'en-GB', 'question_id': 'q1', 'question_version': 'v1', 'exact_question': 'Which tool fits this task?', 'captured_at': '2026-10-20T10:00:00Z' if status == 'observed' else None, 'status': status, 'brand_mentioned': mentioned if status == 'observed' else None, 'citations': [], 'evidence': ['answer-export.json'] if status == 'observed' else []}


class AuditEvidenceReviewTests(unittest.TestCase):
    def test_template_preserves_unknown_baseline(self):
        result = MOD.summarize(fixture())['sites'][0]
        self.assertIsNone(result['baseline']['human_minutes_per_completed_job'])
        self.assertEqual(result['provider_lanes'], [])
        self.assertEqual(result['workflow_evidence_scope'], 'public_proposal')

    def test_measured_baseline_arithmetic(self):
        data = fixture(); site = data['sites'][0]
        site['workflow']['evidence_scope'] = 'first_party_validated'
        site['workflow']['steps'][0]['evidence'] = ['event-log.csv plus operator interview']
        site['baseline'] = {'status': 'measured', 'period': '2026-10-01/2026-10-07', 'completed_jobs': 10, 'total_human_minutes': 250, 'exception_jobs': 2, 'evidence': ['checked-job-log.csv']}
        result = MOD.summarize(data)['sites'][0]['baseline']
        self.assertEqual(result['human_minutes_per_completed_job'], 25)
        self.assertEqual(result['exception_rate'], .2)

    def test_zero_jobs_has_no_derived_rate(self):
        data = fixture(); site = data['sites'][0]
        site['workflow']['evidence_scope'] = 'first_party_validated'
        site['workflow']['steps'][0]['evidence'] = ['checked log']
        site['baseline'] = {'status': 'measured', 'period': '2026-10-01/2026-10-07', 'completed_jobs': 0, 'total_human_minutes': 0, 'exception_jobs': 0, 'evidence': ['checked empty log']}
        self.assertIsNone(MOD.summarize(data)['sites'][0]['baseline']['exception_rate'])

    def test_public_workflow_cannot_claim_measured_baseline(self):
        data = fixture(); data['sites'][0]['baseline']['status'] = 'measured'
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_missing_first_party_step_evidence_rejected(self):
        data = fixture(); data['sites'][0]['workflow']['evidence_scope'] = 'first_party_validated'
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_unknown_baseline_cannot_contain_zero(self):
        data = fixture(); data['sites'][0]['baseline']['completed_jobs'] = 0
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_no_live_pilot_mode(self):
        data = fixture(); data['sites'][0]['pilot']['mode'] = 'automatic_send'
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_stop_condition_required(self):
        data = fixture(); data['sites'][0]['pilot']['stop_condition'] = ''
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_provider_surface_locale_lanes_do_not_merge(self):
        data = fixture(); rows = [observation(), observation('other_engine'), observation()]
        rows[2]['locale'] = 'en-US'
        data['sites'][0]['provider_observations'] = rows
        self.assertEqual(len(MOD.summarize(data)['sites'][0]['provider_lanes']), 3)

    def test_unavailable_not_in_observed_denominator(self):
        data = fixture(); rows = [observation(), observation(status='unavailable')]
        rows[1]['question_id'] = 'q2'
        data['sites'][0]['provider_observations'] = rows
        lane = MOD.summarize(data)['sites'][0]['provider_lanes'][0]
        self.assertEqual((lane['observed'],lane['unavailable'],lane['brand_mentioned']), (1,1,1))

    def test_unchecked_provider_not_zero_visibility(self):
        data = fixture();data['sites'][0]['provider_observations'] = [observation(status='not_checked')]
        self.assertIsNone(MOD.summarize(data)['sites'][0]['provider_lanes'][0]['brand_mentioned'])

    def test_unavailable_cannot_claim_brand_absent(self):
        data = fixture();row = observation(status='unavailable');row['brand_mentioned'] = False
        data['sites'][0]['provider_observations'] = [row]
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_observed_answer_needs_evidence_and_boolean(self):
        for field, value in [('evidence', []), ('brand_mentioned', None), ('brand_mentioned', 1)]:
            with self.subTest(field=field, value=value):
                data = fixture();row = observation();row[field] = value;data['sites'][0]['provider_observations'] = [row]
                with self.assertRaises(ValueError): MOD.summarize(data)

    def test_timestamp_needs_timezone(self):
        data = fixture();row = observation();row['captured_at'] = '2026-10-20T10:00:00';data['sites'][0]['provider_observations'] = [row]
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_duplicate_capture_rejected(self):
        data = fixture();row = observation();data['sites'][0]['provider_observations'] = [row,copy.deepcopy(row)]
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_citation_url_and_source_type_validated(self):
        for url in ['javascript:alert(1)', 'https://user:secret@example.com/path', '/relative']:
            data = fixture();row = observation();row['citations'] = [{'url':url,'source_type':'editorial'}];data['sites'][0]['provider_observations'] = [row]
            with self.assertRaises(ValueError): MOD.summarize(data)

    def test_citation_query_preserved(self):
        data = fixture();row = observation();url = 'https://example.com/article?id=2';row['citations'] = [{'url':url,'source_type':'editorial'}];data['sites'][0]['provider_observations'] = [row]
        MOD.summarize(data);self.assertEqual(row['citations'][0]['url'], url)

    def test_duplicate_site_rejected(self):
        data = fixture();data['sites'].append(copy.deepcopy(data['sites'][0]))
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_cli_writes_valid_summary_and_rejects_bad_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'input.json';out = Path(tmp)/'summary.json';source.write_text(json.dumps(fixture()))
            result = subprocess.run([sys.executable,str(ROOT/'scripts/audit_evidence_review.py'),'--input',str(source),'--output',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(out.read_text())['mode'],'offline_review_only')
            source.write_text('{}');out.unlink()
            result = subprocess.run([sys.executable,str(ROOT/'scripts/audit_evidence_review.py'),'--input',str(source),'--output',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,2);self.assertFalse(out.exists())

    def test_boolean_schema_version_rejected(self):
        data = fixture();data['schema_version'] = True
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_changed_question_text_needs_new_version(self):
        data = fixture();rows = [observation(),observation('other_engine')];rows[1]['exact_question'] = 'A different buying question'
        data['sites'][0]['provider_observations'] = rows
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_invalid_numeric_baselines_rejected(self):
        for value in [-1, float('nan'), float('inf'), True, 10 ** 400]:
            with self.subTest(value=value):
                data = fixture();site = data['sites'][0];site['workflow']['evidence_scope'] = 'first_party_validated'
                site['workflow']['steps'][0]['evidence'] = ['checked log']
                site['baseline'] = {'status':'measured','period':'one checked week','completed_jobs':10,'total_human_minutes':value,'exception_jobs':1,'evidence':['checked log']}
                with self.assertRaises(ValueError): MOD.summarize(data)

    def test_exception_count_cannot_exceed_completed_jobs(self):
        data = fixture();site = data['sites'][0];site['workflow']['evidence_scope'] = 'first_party_validated';site['workflow']['steps'][0]['evidence'] = ['checked log']
        site['baseline'] = {'status':'measured','period':'one checked week','completed_jobs':1,'total_human_minutes':2,'exception_jobs':2,'evidence':['checked log']}
        with self.assertRaises(ValueError): MOD.summarize(data)

    def test_methods_wired_to_existing_owners(self):
        research = (ROOT/'references/playbooks/research/research-for-existing-sites.md').read_text()
        citation = (ROOT/'references/playbooks/maintenance/cross-platform-ai-citation-loop.md').read_text()
        site = (ROOT/'workflows/site-audit.md').read_text();geo = (ROOT/'workflows/geo-audit.md').read_text()
        self.assertIn('Process-first audit before acquisition or automation',research)
        self.assertIn('public_proposal',research);self.assertIn('not_measured',research);self.assertIn('shadow mode',research.lower())
        self.assertIn('Citation-source and author review',citation)
        self.assertIn('readiness-only; provider visibility not measured',citation)
        self.assertIn('functional query parameters',citation)
        self.assertIn('process-first',site.lower());self.assertIn('citation-source',geo.lower())
        self.assertIn('audit_evidence_review.py',(ROOT/'SKILL.md').read_text())


if __name__ == '__main__':
    unittest.main()
