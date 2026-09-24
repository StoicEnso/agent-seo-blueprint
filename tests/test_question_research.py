import ast
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('questions', ROOT / 'scripts/question_research.py')
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)


def normalize():
    # Isolate pure function: no API calls, env files or credentials loaded.
    tree = ast.parse((ROOT / 'scripts/dataforseo_client.py').read_text())
    fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'normalize_serp')
    scope = {}
    exec('from typing import Dict, Any', scope)
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<normalizer>', 'exec'), scope)
    return scope['normalize_serp']


def raw():
    return {'tasks': [{'id': 'synthetic-task', 'data': {'keyword': 'export data'}, 'result': [
        {'keyword': 'export data', 'location_code': 2840, 'language_code': 'en',
         'datetime': '2026-09-15 12:00:00 +00:00', 'check_url': 'https://www.google.com/search?q=export',
         'item_types': ['organic', 'people_also_ask', 'video'],
         'items': [{'type': 'organic', 'rank_group': 1, 'title': 'Guide', 'url': 'https://example.org/guide'},
                   {'type': 'organic', 'rank_group': 2, 'title': 'Guide two', 'url': 'https://example.org/guide2'},
                   {'type': 'people_also_ask', 'items': [{'type': 'people_also_ask_element', 'title': 'Can I export my data?',
                    'items': [{'type': 'people_also_ask_expanded_element', 'url': 'https://example.org/export', 'description': 'Sample evidence'}]}]},
                   {'type': 'video', 'items': [{'url': 'https://www.youtube.com/watch?v=fixture', 'title': 'Demo'}]}]}]}]}


def row(**kwargs):
    r = {'kind': 'observed', 'source_type': 'review', 'source_record_id': 'fixture-review-v1',
         'exact_text': 'Can I export my data?', 'source_url': 'https://example.org/review/1',
         'source_evidence': 'research/fixture.json#/reviews/0', 'captured_at': '2026-09-15T12:00:00Z',
         'locale': 'en-US', 'expansion_depth': None, 'parent_question': None}
    r.update(kwargs)
    return r


def plan(b):
    return {'observation_ids': [b['observations'][0]['id']], 'owned_page_url': 'https://example.org/help/export',
            'coverage_decision': 'update_section', 'page_check_evidence': 'research/page.json',
            'video_fit_evidence': 'research/video-results.json', 'proof_plan': 'Demonstrate the verified export button.'}


def filled():
    b = q.bank([{'observations': [row()]}])
    p = q.brief(b, plan(b))
    p.update(title='How to export your data', direct_answer='Use Export in Settings.', original_script='Original fixture script.',
             chapter_outline=['Find settings', 'Export'], description='A short demonstration.', tracking_plan='Use a unique campaign tag.',
             claim_sources=['research/product-docs.json'], limitations=['Fixture only, not a live product claim.'])
    return p


class FeatureRetentionTests(unittest.TestCase):
    def test_paa_and_video_survive_organic_top_limit(self):
        out = normalize()(raw(), top=1)['serps'][0]
        self.assertEqual(len(out['results']), 1)
        self.assertEqual(out['results'][0]['url'], 'https://example.org/guide')
        self.assertEqual(out['people_also_ask'][0]['items'][0]['title'], 'Can I export my data?')
        self.assertIn('youtube.com', out['video_results'][0]['items'][0]['url'])
        self.assertEqual(out['task_id'], 'synthetic-task')

    def test_no_features_is_empty_not_invented(self):
        r = raw(); r['tasks'][0]['result'][0]['items'] = []
        out = normalize()(r)['serps'][0]
        self.assertEqual(out['people_also_ask'], []); self.assertEqual(out['video_results'], [])

    def test_nested_answers_preserved_and_input_unchanged(self):
        r = raw(); before = copy.deepcopy(r); out = normalize()(r)
        self.assertEqual(r, before)
        self.assertEqual(out['serps'][0]['people_also_ask'][0], r['tasks'][0]['result'][0]['items'][2])

    def test_short_video_group_retained(self):
        r = raw(); r['tasks'][0]['result'][0]['items'][-1]['type'] = 'short_videos'
        self.assertEqual(normalize()(r)['serps'][0]['video_results'][0]['type'], 'short_videos')

    def test_empty_tasks(self):
        self.assertEqual(normalize()({'tasks': []})['serps'], [])


class BankTests(unittest.TestCase):
    def test_import_retains_exact_question_raw_answer_and_unknown_tree(self):
        b = q.import_serp(normalize()(raw()), 'research/fixture.json', 'en-US')
        r = b['observations'][0]
        self.assertEqual(r['exact_text'], 'Can I export my data?')
        self.assertEqual(r['raw_question']['items'][0]['url'], 'https://example.org/export')
        self.assertIsNone(r['parent_question']); self.assertIsNone(r['expansion_depth'])
        self.assertIn('#/serps/0/people_also_ask/0/items/0', r['source_evidence'])

    def test_duplicate_capture_collapses(self):
        self.assertEqual(q.bank([{'observations': [row(), row()]}])['counts']['captured_records'], 1)

    def test_distinct_source_same_words_retained(self):
        b = q.bank([{'observations': [row(), row(source_url='https://other.example/review/1')]}])
        self.assertEqual(b['counts'], {'captured_records': 2, 'exact_text_clusters': 1})

    def test_conflicting_identity_rejected(self):
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            q.bank([{'observations': [row(), row(exact_text='Changed review')]}])

    def test_inferred_rejected(self):
        with self.assertRaisesRegex(ValueError, 'observed'):
            q.bank([{'observations': [row(kind='inferred')]}])

    def test_hypothesis_side_channel_rejected(self):
        with self.assertRaisesRegex(ValueError, 'hypotheses'):
            q.bank([{'observations': [], 'hypotheses': ['invented']}])

    def test_invalid_observations(self):
        for changes in ({'captured_at': '2026-09-15'}, {'source_url': 'javascript:bad'},
                        {'source_url': 'https://user:pass@example.org'}, {'exact_text': ''},
                        {'source_evidence': 'REPLACE_WITH_EVIDENCE'}, {'locale': 'en'},
                        {'expansion_depth': True}, {'expansion_depth': 3}, {'id': 'wrong'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                q.observation(row(**changes))

    def test_cap_rejected(self):
        with self.assertRaisesRegex(ValueError, 'cap'):
            q.bank([{'observations': [row(), row(source_record_id='second')]}], 1)

    def test_bad_caps(self):
        for cap in (0, 501, True, '50'):
            with self.subTest(cap=cap), self.assertRaises(ValueError):
                q.bank([{'observations': []}], cap)

    def test_locale_separates_clusters(self):
        b = q.bank([{'observations': [row(), row(locale='en-GB')]}])
        self.assertEqual(b['counts']['exact_text_clusters'], 2)

    def test_partial_shapes_rejected(self):
        for p in ({'ok': False, 'serps': []}, {'ok': True, 'serps': [{}]}, {'ok': True, 'serps': None}):
            with self.subTest(p=p), self.assertRaises(ValueError):
                q.import_serp(p, 'fixture.json', 'en-US')

    def test_bank_roundtrip_and_input_unchanged(self):
        original = {'observations': [row()]}; before = copy.deepcopy(original)
        b = q.bank([original]); self.assertEqual(q.bank([b]), b); self.assertEqual(original, before)

    def test_all_manual_sources_supported(self):
        for source in ('youtube_comment', 'youtube_transcript', 'review', 'gsc', 'support'):
            with self.subTest(source=source):
                self.assertEqual(q.observation(row(source_type=source))['source_type'], source)


class BriefTests(unittest.TestCase):
    def test_scaffold_stays_incomplete_and_unapproved(self):
        b = q.bank([{'observations': [row()]}]); p = q.brief(b, plan(b))
        self.assertEqual(p['status'], 'draft_incomplete'); self.assertEqual(p['publication_status'], 'not_approved')
        self.assertIsNone(p['original_script']); self.assertEqual(p['transcript']['status'], 'pending_recording')
        self.assertTrue(all(v is None for v in p['metrics'].values()))
        with self.assertRaises(ValueError): q.check_brief(p)

    def test_finished_draft_is_not_publication_approval(self):
        out = q.check_brief(filled())
        self.assertEqual(out['status'], 'draft_ready_for_review'); self.assertEqual(out['publication_status'], 'not_approved')

    def test_missing_ownership_or_source_rejected(self):
        b = q.bank([{'observations': [row()]}])
        for change in ({'observation_ids': ['wrong']}, {'page_check_evidence': ''},
                       {'coverage_decision': 'reject'}, {'video_fit_evidence': ''}, {'proof_plan': 'REPLACE_WITH_PROOF'}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                q.brief(b, dict(plan(b), **change))

    def test_mixed_locale_rejected(self):
        b = q.bank([{'observations': [row(), row(locale='en-GB')]}]); p = plan(b)
        p['observation_ids'] = [r['id'] for r in b['observations']]
        with self.assertRaisesRegex(ValueError, 'locales'): q.brief(b, p)

    def test_publication_and_transcript_claims_rejected(self):
        for change in ({'publication_status': 'approved'}, {'original_script': None},
                       {'cta_url': 'https://other.example/'}, {'claim_sources': []},
                       {'transcript': {'status': 'reviewed', 'locator': None}},
                       {'transcript': {'status': 'pending_recording', 'locator': 'fake.txt'}}):
            with self.subTest(change=change), self.assertRaises(ValueError): q.check_brief(dict(filled(), **change))

    def test_referenced_source_cannot_be_replaced(self):
        p = filled(); p['sources'][0]['source_record_id'] = 'different'
        with self.assertRaises(ValueError): q.check_brief(p)


class CliAndDocsTests(unittest.TestCase):
    def test_cli_success_and_invalid_json(self):
        cmd = [sys.executable, str(ROOT/'scripts/question_research.py'), 'check-bank']
        out = subprocess.run(cmd+[str(ROOT/'assets/question-observations.example.json')], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr); self.assertEqual(json.loads(out.stdout)['counts']['captured_records'], 1)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'bad.json'; p.write_text('{')
            out = subprocess.run(cmd+[str(p)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 1); self.assertFalse(json.loads(out.stderr)['ok'])

    def test_routes_and_boundaries(self):
        for name in ('SKILL.md', 'workflows/research-and-ideation.md', 'workflows/content-production.md',
                     'references/playbooks/content/cross-platform-commercial-intent-distribution.md'):
            self.assertIn('references/question-research-and-youtube.md', (ROOT/name).read_text())
        doc = (ROOT/'references/question-research-and-youtube.md').read_text()
        for phrase in ('--locale en-US', 'no network calls', 'not unique people', 'fixture_tested', 'live_source_verified', 'not_approved', 'Retry-After'):
            self.assertIn(phrase, doc)


if __name__ == '__main__': unittest.main()
