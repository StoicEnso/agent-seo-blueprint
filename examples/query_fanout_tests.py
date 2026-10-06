"""Synthetic tests only; no live provider queries. Run with python3 examples/query_fanout_tests.py."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fanout', ROOT / 'scripts/query_fanout_check.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FanoutTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'assets/query-fanout-ledger.json').read_text())
        self.row = self.data['observations'][0]
    def observed(self):
        self.row.update(state='observed', captured_at='2026-09-12T04:00:00Z', evidence='synthetic/run.json', queries=[{'query_id':'s01', 'text':'synthetic buyer query', 'method':'official_api_query_metadata', 'evidence':'synthetic/run.json#/queries/0'}])
    def test_template(self):
        self.assertEqual(module.validate(self.data), [])
    def test_observed(self):
        self.observed(); self.assertEqual(module.validate(self.data), [])
    def test_inferred_is_not_observed(self):
        self.observed(); self.row['queries'][0]['method'] = 'model_guess'
        self.assertTrue(module.validate(self.data))
    def test_missing_query_evidence(self):
        self.observed(); self.row['queries'][0]['evidence'] = ''
        self.assertTrue(module.validate(self.data))
    def test_hidden_is_not_observed(self):
        self.observed(); self.row['state'] = 'not_exposed'
        self.assertTrue(module.validate(self.data))
    def test_empty_observed(self):
        self.observed(); self.row['queries'] = []
        self.assertTrue(module.validate(self.data))
    def test_citation_only(self):
        self.row.update(state='citation_only', captured_at='2026-09-12T04:00:00Z', evidence='synthetic/sources.png', reason='Only sources exposed', citations=[{'url':'https://example.com/source', 'evidence':'synthetic/sources.png'}])
        self.assertEqual(module.validate(self.data), [])
    def test_citation_only_needs_citation(self):
        self.row.update(state='citation_only', captured_at='2026-09-12T04:00:00Z', evidence='synthetic/sources.png', reason='Only sources exposed')
        self.assertTrue(module.validate(self.data))
    def test_unknown_question_version(self):
        self.row['prompt_version'] = 9
        self.assertTrue(module.validate(self.data))
    def test_duplicate_run(self):
        self.data['observations'].append(copy.deepcopy(self.row))
        self.assertTrue(module.validate(self.data))
    def test_timezone_required(self):
        self.observed(); self.row['captured_at'] = '2026-09-12T04:00:00'
        self.assertTrue(module.validate(self.data))
    def test_hypothesis_separate(self):
        self.data['hypotheses'] = [{'kind':'inferred', 'text':'synthetic topic idea', 'rationale':'customer hypothesis', 'validation_status':'unvalidated'}]
        self.assertEqual(module.validate(self.data), [])
    def test_bad_hypothesis(self):
        self.data['hypotheses'] = [{'kind':'observed', 'text':'guessed query'}]
        self.assertTrue(module.validate(self.data))
    def test_malformed_types(self):
        for field, value in [('state', []), ('prompt_version', []), ('queries', {}), ('observation_id', [])]:
            d = copy.deepcopy(self.data); d['observations'][0][field] = value
            self.assertTrue(module.validate(d))
    def test_provider_states_kept_separate(self):
        self.assertEqual(len(module.summarize(self.data)), 4)
    def test_no_search_needs_evidence(self):
        self.row.update(state='no_search_observed', captured_at='2026-09-12T04:00:00Z', reason='Explicit search-tool status')
        self.assertTrue(module.validate(self.data))
    def test_untested_cannot_claim_capture(self):
        self.row['captured_at'] = '2026-09-12T04:00:00Z'
        self.assertTrue(module.validate(self.data))
    def test_duplicate_query(self):
        self.observed(); self.row['queries'].append(copy.deepcopy(self.row['queries'][0]))
        self.assertTrue(module.validate(self.data))

if __name__ == '__main__':
    unittest.main()
