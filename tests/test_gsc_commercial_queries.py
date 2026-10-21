import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('gsc_commercial_queries', ROOT / 'scripts/gsc_commercial_queries.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def payload():
    return {'meta': {'site': 'sc-domain:example.com', 'start': '2026-09-21', 'end': '2026-10-18',
                     'dimensions': ['query'], 'type': 'web', 'data_state': 'final',
                     'country': 'all', 'device': 'all'},
            'rows': [{'keys': ['best garden app'], 'clicks': 1, 'impressions': 20, 'ctr': .05, 'position': 8},
                     {'keys': ['garden generator'], 'clicks': 2, 'impressions': 10, 'ctr': .2, 'position': 4},
                     {'keys': ['app alternatives'], 'clicks': 0, 'impressions': 5, 'ctr': 0, 'position': 10}]}


class ClassifierTests(unittest.TestCase):
    def test_all_intended_seed_terms_match(self):
        for term in ['buy', 'shop', 'order', 'pricing', 'price', 'cost', 'hire', 'book', 'schedule',
                     'reserve', 'near me', 'nearme', 'in stock', 'instock', 'available', 'same day',
                     'sameday', 'best', 'vs', 'review', 'reviews', 'alternative', 'alternatives',
                     'deal', 'discount']:
            with self.subTest(term=term):
                self.assertTrue(m.classify('garden ' + term)['matched_terms'])

    def test_case_insensitive(self):
        self.assertEqual(m.classify('BEST garden APP')['signal_groups'], ['comparison'])

    def test_whitespace_and_punctuation(self):
        self.assertTrue(m.classify('hire: near\tme!')['matched_terms'])
        self.assertTrue(m.classify('in   stock')['matched_terms'])

    def test_word_boundaries_prevent_substrings(self):
        for query in ['costume', 'bestow', 'bookcase', 'reviewer', 'yesterday', 'priceless', 'shopper']:
            with self.subTest(query=query):
                self.assertFalse(m.classify(query)['matched_terms'])

    def test_missing_pipes_in_source_are_demonstrated(self):
        for query in ['buy garden app', 'garden app alternatives', 'schedule a design', 'garden discount']:
            with self.subTest(query=query):
                hit = m.classify(query)
                self.assertTrue(hit['matched_terms'])
                self.assertFalse(hit['source_pattern_match'])

    def test_existing_valid_source_branches_preserved(self):
        self.assertTrue(m.classify('garden cost')['source_pattern_match'])
        self.assertTrue(m.classify('best app')['source_pattern_match'])

    def test_overlapping_groups_are_not_exclusive(self):
        self.assertEqual(m.classify('best price near me')['signal_groups'],
                         ['price', 'comparison', 'availability'])

    def test_empty_or_nonstring_query_rejected(self):
        for query in ['', ' ', None, 3]:
            with self.subTest(query=query), self.assertRaises(ValueError):
                m.classify(query)


class AnalyzerTests(unittest.TestCase):
    def analyze(self, value=None, previous=None):
        return m.analyze(payload() if value is None else value, previous, '2026-10-21')

    def test_metrics_and_recovered_candidates(self):
        out = self.analyze()
        self.assertEqual(out['commercial_term_candidates']['impressions'], 25)
        self.assertEqual(out['commercial_term_candidates']['ctr'], 1 / 25)
        self.assertEqual(out['source_pattern_missed']['rows'], 1)
        self.assertEqual(out['commercial_term_candidates']['impression_weighted_position'], 8.4)

    def test_controls_are_retained_and_no_action_is_approved(self):
        out = self.analyze()
        self.assertEqual(out['nonmatching_controls'][0]['keys'], ['garden generator'])
        for row in out['candidates'] + out['nonmatching_controls']:
            self.assertFalse(row['intent_verified'])
            self.assertFalse(row['business_fit_verified'])
            self.assertFalse(row['approved_for_write'])

    def test_missing_prior_is_unknown_not_zero(self):
        before = payload()
        before['meta'].update(start='2026-08-24', end='2026-09-20')
        before['rows'] = before['rows'][:1]
        before['rows'][0].update(clicks=2, ctr=.1)
        out = self.analyze(previous=before)
        known, missing = out['candidates']
        self.assertEqual(known['click_delta'], -1)
        self.assertIsNone(missing['click_delta'])
        self.assertEqual(missing['previous_observation'], 'not_observed_or_unavailable')

    def test_query_page_is_distinct_from_query_aggregation(self):
        p = payload()
        p['meta']['dimensions'] = ['query', 'page']
        for row in p['rows']:
            row['keys'].append('https://example.com/garden')
        self.assertEqual(self.analyze(p)['aggregation'], 'query_page')

    def test_empty_rows_is_observed_empty_not_coverage_proof(self):
        p = payload(); p['rows'] = []
        out = self.analyze(p)
        self.assertIsNone(out['observed_rows']['ctr'])
        self.assertIsNone(out['observed_rows']['impression_weighted_position'])
        self.assertTrue(out['limitations'])

    def test_stale_data_remains_review_only(self):
        self.assertEqual(m.analyze(payload(), as_of='2026-11-01')['status'], 'STALE_REVIEW_ONLY')

    def test_unknown_negative_or_nonfinite_metrics_rejected(self):
        for field, value in [('clicks', None), ('clicks', True), ('clicks', -1), ('clicks', .5),
                             ('clicks', 21), ('impressions', 0), ('impressions', float('inf')),
                             ('position', float('nan')), ('position', 0), ('ctr', .8)]:
            p = payload(); p['rows'][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.analyze(p)

    def test_missing_scope_rejected(self):
        for field in m.SCOPE:
            p = payload(); del p['meta'][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.analyze(p)

    def test_nonfinal_or_wrong_search_type_rejected(self):
        for field, value in [('data_state', 'all'), ('type', 'image')]:
            p = payload(); p['meta'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.analyze(p)

    def test_unknown_scope_type_rejected(self):
        p = payload(); p['meta']['country'] = []
        with self.assertRaises(ValueError): self.analyze(p)

    def test_pre_filtered_input_rejected(self):
        for field in ['include_regex', 'exclude_regex', 'filters']:
            p = payload(); p['meta'][field] = 'price'
            with self.subTest(field=field), self.assertRaises(ValueError): self.analyze(p)

    def test_duplicate_rows_rejected(self):
        p = payload(); p['rows'].append(copy.deepcopy(p['rows'][0]))
        with self.assertRaises(ValueError): self.analyze(p)

    def test_wrong_dimensions_and_keys_rejected(self):
        for dims in [['page'], ['page', 'query'], ['query', 'device']]:
            p = payload(); p['meta']['dimensions'] = dims
            with self.subTest(dims=dims), self.assertRaises(ValueError): self.analyze(p)
        p = payload(); p['rows'][0]['keys'].append('extra')
        with self.assertRaises(ValueError): self.analyze(p)

    def test_invalid_dates_or_timezone_rejected(self):
        for field, value in [('start', '20261001'), ('end', '2026-10-21'), ('end', '2026-10-22'),
                             ('start', '2026-10-19'), ('date_timezone', 'Europe/London')]:
            p = payload(); p['meta'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.analyze(p)

    def test_comparison_scope_mismatch_rejected(self):
        for field, value in [('site', 'sc-domain:other.com'), ('country', 'usa'), ('device', 'MOBILE')]:
            before = payload(); before['meta'].update(start='2026-08-24', end='2026-09-20')
            before['meta'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): self.analyze(previous=before)

    def test_comparison_overlap_gap_or_unequal_window_rejected(self):
        for start, end in [('2026-08-25', '2026-09-21'), ('2026-08-23', '2026-09-19'),
                           ('2026-08-23', '2026-09-20')]:
            before = payload(); before['meta'].update(start=start, end=end)
            with self.subTest(start=start, end=end), self.assertRaises(ValueError): self.analyze(previous=before)

    def test_input_not_mutated(self):
        p = payload(); saved = copy.deepcopy(p)
        self.analyze(p)
        self.assertEqual(p, saved)

    def test_cli_success_and_fail_closed_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'; path.write_text(json.dumps(payload()))
            cmd = [sys.executable, str(ROOT / 'scripts/gsc_commercial_queries.py'), str(path),
                   '--as-of', '2026-10-21']
            good = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertEqual(json.loads(good.stdout)['status'], 'REVIEW_ONLY')
            path.write_text('{broken')
            bad = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertEqual(json.loads(bad.stdout)['status'], 'INVALID_INPUT')
            self.assertNotIn('Traceback', bad.stderr)


class DocumentationTests(unittest.TestCase):
    def test_method_and_routes_exist(self):
        name = 'gsc-commercial-query-triage.md'
        for relative in ['SKILL.md', 'README.md', 'workflows/monitoring.md', 'references/integrations/gsc.md',
                         'references/playbooks/maintenance/gsc-position-4-20-opportunity-mining.md']:
            self.assertIn(name, (ROOT / relative).read_text())
        text = (ROOT / 'references' / name).read_text()
        for phrase in ['not unique visitors', 'not a ranking intervention', 'hidden', 'query+page',
                       'existing page', 'English', '3–10', 'No live project query rows', 'REVIEW_ONLY']:
            self.assertIn(phrase, text)


if __name__ == '__main__':
    unittest.main()
