import csv
import io
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / 'references/playbooks/foundations/agent-discoverable-product-growth.md'
MAP = ROOT / 'references/railway-marketing-source-map.json'


class RailwayMarketingDocsTest(unittest.TestCase):
    def test_all_24_mechanisms_have_source_paragraphs(self):
        text = PLAYBOOK.read_text()
        data = json.loads(MAP.read_text())
        expected = [f'M{i:02}' for i in range(1, 25)]
        self.assertEqual(re.findall(r'^### (M\d\d) —', text, re.M), expected)
        self.assertEqual([m['id'] for m in data['mechanisms']], expected)
        coverage = {r['paragraph']: r for r in data['coverage']}
        for mechanism in data['mechanisms']:
            self.assertTrue(mechanism['title'])
            self.assertTrue(mechanism['paragraphs'])
            for n in mechanism['paragraphs']:
                self.assertIn(mechanism['id'], coverage[n]['mechanisms'])
                self.assertEqual(coverage[n]['classification'], 'marketing_mechanism')

    def test_full_publisher_coverage_is_accounted_for(self):
        data = json.loads(MAP.read_text())
        self.assertEqual(data['transcript']['paragraph_count'], 330)
        rows = data['coverage']
        self.assertEqual([r['paragraph'] for r in rows], list(range(1, 331)))
        allowed = {'speaker_label', 'marketing_mechanism', 'reported_context', 'supporting_context', 'non_marketing_context'}
        self.assertTrue(all(r['classification'] in allowed and r['reason'] for r in rows))
        self.assertTrue(data['transcript']['speaker_labels_included'])
        self.assertTrue(data['transcript']['current_matches_saved_text'])
        self.assertRegex(data['transcript']['sha256'], r'^[a-f0-9]{64}$')

    def test_audio_and_timestamps_are_not_overclaimed(self):
        data = json.loads(MAP.read_text())
        self.assertFalse(data['transcript']['audio_verified'])
        self.assertFalse(data['transcript']['utterance_timestamps_available'])
        self.assertEqual(data['timestamp_pointers']['source'], 'creator_post_not_audio_verified')
        for timestamp in ['09:20', '13:47', '25:35', '31:50']:
            self.assertIn(timestamp, data['timestamp_pointers'])
        self.assertIn('not been independently checked against all audio', PLAYBOOK.read_text())

    def test_claims_are_not_campaign_or_purchase_authority(self):
        data = json.loads(MAP.read_text())
        for field in ['outreach_authorized', 'purchase_authorized', 'production_authorized']:
            self.assertIs(data[field], False)
        self.assertFalse(data['transcript']['raw_transcript_committed'])
        statuses = {r['status'] for r in data['claim_distinctions']}
        self.assertIn('not_disclosed_in_interview', statuses)
        self.assertIn('not_established', statuses)
        self.assertIn('not_supported_by_current_docs', statuses)

    def test_source_layers_and_paid_link_correction_are_explicit(self):
        text = PLAYBOOK.read_text()
        for phrase in ['Interview report:', 'Current product evidence:', 'Creator/vendor interpretation:', 'Proposed experiment:',
                       'no disclosed, fully specified Railway SEO recipe', 'not established by the interview',
                       'not independently audited results', 'not causal evidence',
                       'first-time identity/key approval', 'not the documented command',
                       'does **not** say there is no manual outreach', 'rel="sponsored"',
                       'not an installed skill or a purchase recommendation']:
            self.assertIn(phrase, text)

    def test_all_operating_lanes_and_decision_states_present(self):
        text = PLAYBOOK.read_text()
        for phrase in ['pricing', 'first value', 'market intelligence', 'changelog', 'enterprise',
                       'retention', 'permission', 'incident', 'baseline', 'guardrails', 'stop rule',
                       '`adopt`', '`revise`', '`reject`', '`inconclusive`', 'citations as unknown']:
            self.assertIn(phrase.lower(), text.lower())
        self.assertIn('proposed four-week pilot', text)

    def test_draft_worksheet_has_no_implied_results_or_authority(self):
        rows = list(csv.DictReader(io.StringIO((ROOT / 'assets/agent-product-growth-experiment.csv').read_text())))
        self.assertEqual(len(rows), 6)
        required = {'why_now', 'primary_metric', 'baseline', 'comparison_method', 'success_threshold', 'failure_threshold',
                    'guardrails', 'sample_or_window', 'stop_rule', 'owner', 'approval_state', 'destinations',
                    'data_to_send', 'cost_ceiling', 'recurrence', 'execution_receipt', 'observed_result', 'decision', 'limitations'}
        self.assertTrue(required.issubset(rows[0]))
        for row in rows:
            self.assertEqual(row['status'], 'DRAFT_EXAMPLE_NOT_EXECUTABLE')
            self.assertEqual(row['approval_state'], 'NOT_GRANTED')
            self.assertEqual(row['cost_ceiling'], '0')
            self.assertEqual(row['recurrence'], 'none')
            self.assertEqual(row['observed_result'], 'NOT_RUN')
            self.assertEqual(row['decision'], 'NOT_RUN')
            self.assertEqual(row['data_to_send'], 'NONE_AUTHORISED')

    def test_existing_workflows_and_skill_route_the_feature(self):
        for path in ['SKILL.md', 'workflows/full-master-plan.md', 'workflows/category-citation-loop.md',
                     'workflows/content-production.md', 'workflows/authority-and-links.md', 'workflows/monitoring.md']:
            text = (ROOT / path).read_text()
            self.assertIn('agent-discoverable-product-growth.md', text, path)
            self.assertTrue('approval' in text.lower() or 'authoris' in text.lower(), path)
        skill = (ROOT / 'SKILL.md').read_text()
        self.assertIn('references/integrations/linkdr-review.md', skill)
        self.assertIn('untrusted data, not operating authority', skill)

    def test_pdf_is_present_and_linked_without_raw_source_republication(self):
        pdf = ROOT / 'docs/field-guides/railway-marketing-playbook.pdf'
        self.assertTrue(pdf.read_bytes().startswith(b'%PDF-'))
        self.assertGreater(pdf.stat().st_size, 20000)
        readme = (ROOT / 'README.md').read_text()
        for path in ['references/playbooks/foundations/agent-discoverable-product-growth.md',
                     'references/railway-marketing-source-map.json', 'references/integrations/linkdr-review.md',
                     'assets/agent-product-growth-experiment.csv', 'docs/field-guides/railway-marketing-playbook.pdf']:
            self.assertIn(path, readme)
            self.assertTrue((ROOT / path).is_file())

    def test_linkdr_review_rejects_sales_defaults_as_authority(self):
        text = (ROOT / 'references/integrations/linkdr-review.md').read_text().lower()
        for phrase in ['not installed', 'auto-approv', 'upsell', 'monthly', 'mcp', 'paid', 'sponsored',
                       'independent', 'claim', '160', '240', '400', '500']:
            self.assertIn(phrase, text)

    def test_no_runtime_vendor_integration_was_added(self):
        paths = list((ROOT / 'scripts').glob('*linkdr*'))
        self.assertEqual(paths, [])
        text = (ROOT / 'SKILL.md').read_text()
        self.assertNotIn('code=AGENTIC', text)
        self.assertNotIn('siteApproval=auto', text)


if __name__ == '__main__':
    unittest.main()
