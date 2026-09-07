"""Documentation/template contract tests, not live ranking or runtime validation."""
import csv
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'references/local-profile-evidence-quality.md'
PLAYBOOK = ROOT / 'references/playbooks/maintenance/local-business-profile-audit.md'


class LocalProfileEvidenceDocsTest(unittest.TestCase):
    def test_context_is_blank_and_sourced(self):
        data = json.loads((ROOT / 'assets/local-business-context.json').read_text())
        self.assertEqual(data['schema_version'], 1)
        self.assertTrue(data['example_only'])
        self.assertTrue(data['private_project_data_only'])
        fields = set(data) - {'schema_version', 'example_only', 'private_project_data_only'}
        self.assertEqual(fields, {'business_name', 'website', 'profile_url', 'services',
                                'actual_service_areas', 'target_customers', 'goals',
                                'baseline_metrics', 'competitors', 'previous_tests'})
        for name in fields:
            field = data[name]
            self.assertEqual(set(field), {'value', 'source', 'verified_at', 'status'})
            for key in ('value', 'source', 'verified_at'):
                self.assertIsNone(field[key])
            self.assertIn(field['status'], ('NOT_VISIBLE', 'NEEDS_OWNER_DATA'))

    def test_observations_preserve_coverage_and_unknowns(self):
        with (ROOT / 'assets/local-profile-observations.csv').open(newline='') as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            self.assertEqual(list(reader), [])
        self.assertEqual(len(fields), len(set(fields)))
        self.assertTrue({'observation_status', 'source_method', 'observed_at', 'query',
                         'location_context', 'device', 'window_days', 'window_start',
                         'window_end', 'sample_size', 'oldest_review_at',
                         'observed_reviews_in_window', 'coverage', 'count_semantics',
                         'coverage_proof', 'truth_basis', 'approval_state'}.issubset(fields))
        text = REFERENCE.read_text()
        for state in ('OBSERVED', 'NOT_VISIBLE', 'NOT_APPLICABLE', 'NEEDS_OWNER_DATA'):
            self.assertIn(state, text)
        self.assertIn('not proof of absence', text)

    def test_partial_review_windows_are_not_exact_totals(self):
        text = REFERENCE.read_text()
        for phrase in ('coverage=FULL', 'coverage=PARTIAL', 'coverage=UNKNOWN',
                       'verified complete export', 'LOWER_BOUND', 'EXACT',
                       'cannot support an exact count', 'last-50-review sample',
                       'does not establish the 30-day total', 'no pagination',
                       'unknown response delay'):
            self.assertIn(phrase, text)

    def test_photos_require_rights_privacy_and_approval(self):
        with (ROOT / 'assets/local-photo-plan.csv').open(newline='') as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            self.assertEqual(list(reader), [])
        self.assertEqual(len(fields), len(set(fields)))
        self.assertTrue({'business_purpose', 'shot_description', 'actual_location',
                         'rights_evidence', 'customer_consent', 'privacy_review',
                         'owner', 'planned_date', 'approval_state', 'published_receipt'}.issubset(fields))
        text = REFERENCE.read_text()
        self.assertIn('Unknown rights or consent blocks upload', text)
        self.assertIn('Upload remains approval-gated', text)
        self.assertIn('Never commit private client data', text)

    def test_existing_owner_playbook_and_routes(self):
        text = PLAYBOOK.read_text()
        self.assertIn('../../local-profile-evidence-quality.md', text)
        resolved = (PLAYBOOK.parent / '../../local-profile-evidence-quality.md').resolve()
        self.assertEqual(resolved, REFERENCE.resolve())
        self.assertIn('local-business-profile-audit.md', (ROOT / 'workflows/site-audit.md').read_text())
        for phrase in ('**Read-only by default.**', '**No review manipulation.**',
                       '**No location spoofing.**', 'Do not claim causality',
                       'reject' ):
            self.assertIn(phrase.lower(), text.lower())
        self.assertTrue((ROOT / 'assets/local-business-profile-audit.csv').is_file())

    def test_rejected_source_claims_and_gsc_route(self):
        text = REFERENCE.read_text()
        for phrase in ('12 identifiable', 'six months', 'seven-day expiry',
                       'Never coach review keywords', 'Reject doorway multiplication',
                       'not proof that a title or description caused it',
                       'No Search Console rows is not proof of no rankings',
                       'current final 28-day evidence', 'effort, dependency, owner'):
            self.assertIn(phrase, text)
        self.assertTrue((ROOT / 'references/playbooks/maintenance/gsc-position-4-20-opportunity-mining.md').is_file())
        for source in ('209630505',):
            self.assertNotIn(source, text)  # no unrelated UGC-ad intake
        self.assertIn('2095896040155340809', text)
        self.assertIn('support.google.com/business/answer/7091', text)


if __name__ == '__main__':
    unittest.main()
