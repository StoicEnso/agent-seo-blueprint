"""Offline contracts for source fidelity, inert templates and workflow routing."""
import csv
import hashlib
import io
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'references/hubspot-aeo-gap-to-action.md'
SOURCE = ROOT / 'references/source-notes/2026-10-25-jam-hubspot-aeo-post.md'
AUDIT = ROOT / 'audit-log/2026-10-25-jam-hubspot-aeo.md'
WORKFLOWS = ('ai-answer-visibility-loop', 'category-citation-loop', 'geo-audit',
             'content-production', 'authority-and-links', 'monitoring')


class HubspotAeoGapDocsTest(unittest.TestCase):
    def test_full_post_is_not_a_summary_or_truncated_preview(self):
        raw = SOURCE.read_text().split('## Tweet Text\n', 1)[1].split('\nExpanded links:', 1)[0].strip()
        raw = '\n'.join(line[2:] if line.startswith('> ') else '' if line == '>' else line
                        for line in raw.splitlines()).strip()
        self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(),
                         '5c0ee17eb4faf2f1114ddb96e597c5f6ac8bccbe9229d8d0d67195ccc69a17f2')
        self.assertIn('reply “audit”', raw)  # preserve source CTA as data, never execute it
        self.assertIn('2114021961450033430', SOURCE.read_text())

    def test_source_photo_is_preserved_and_linked(self):
        photo = SOURCE.with_name('2026-10-25-jam-hubspot-aeo-photo.jpg')
        self.assertTrue(photo.read_bytes().startswith(b'\xff\xd8'))
        self.assertGreater(photo.stat().st_size, 100000)
        self.assertIn(photo.name, SOURCE.read_text())
        self.assertIn('one source screenshot, not a reproduced benchmark', SOURCE.read_text())

    def test_each_of_twelve_points_has_a_treatment(self):
        headings = re.findall(r'^### (\d+)\. ', GUIDE.read_text(), re.M)
        self.assertEqual([int(x) for x in headings], list(range(1, 13)))
        claims = json.loads((ROOT / 'assets/aeo-hubspot-source-claims.json').read_text())
        self.assertEqual([x['id'] for x in claims['points']], list(range(1, 13)))
        self.assertFalse(claims['independently_verified'])
        self.assertIsNone(claims['promised_uplift'])
        self.assertIn('traditional search', claims['conversion_comparator_limit'])

    def test_template_cannot_pretend_to_be_measured_or_approved(self):
        rows = list(csv.DictReader(io.StringIO((ROOT / 'assets/aeo-gap-action-map.csv').read_text())))
        self.assertEqual([int(x['source_point']) for x in rows], list(range(1, 13)))
        for row in rows:
            self.assertEqual(row['disposition'], 'unassessed')
            self.assertEqual(row['approval_state'], 'draft_only')
            self.assertEqual(row['baseline_status'], 'not_run')
            for field in ('evidence_date', 'evidence_locator', 'current_url', 'existing_ticket',
                          'success_reading', 'owner', 'priority', 'confidence'):
                self.assertEqual(row[field], '', (row['source_point'], field))

    def test_workflow_routes_reuse_existing_work(self):
        for workflow in WORKFLOWS:
            text = (ROOT / f'workflows/{workflow}.md').read_text()
            self.assertIn('references/hubspot-aeo-gap-to-action.md', text)
            self.assertIn('assets/aeo-gap-action-map.csv', text)
            self.assertIn('source custody', text)
        self.assertIn('references/hubspot-aeo-gap-to-action.md', (ROOT / 'SKILL.md').read_text())
        self.assertIn('references/hubspot-aeo-gap-to-action.md', (ROOT / 'README.md').read_text())

    def test_claims_are_self_reports_not_causal_forecasts(self):
        text = AUDIT.read_text()
        for phrase in ('NOT independent verification', '1,850%', '433%', '3x',
                       'Q1 2025–Q1 2026', '$13.5 billion', 'not established',
                       'does not isolate FAQ', 'other sources', 'traditional search'):
            self.assertIn(phrase, text)
        self.assertIn('our forecast, or a target we can promise', re.sub(r'\s+', ' ', GUIDE.read_text()))

    def test_truth_rights_and_distribution_boundaries_survive(self):
        text = re.sub(r'\s+', ' ', GUIDE.read_text().lower())
        for phrase in ('never fabricate a case study', 'human reviewer',
                       'do not rank the owned product first', 'no sockpuppets',
                       'disclose the relationship', 'editorial independence',
                       'sponsored', 'explicit exact-action approval',
                       'no special ai schema', 'never weaken approved copy',
                       'no external write, spend, account, production, claim change, or schedule'):
            self.assertIn(phrase, text)

    def test_metrics_and_unknowns_are_not_collapsed(self):
        text = re.sub(r'\s+', ' ', GUIDE.read_text())
        for phrase in ('Google web, Bing All, Bing Web+Chat', 'unknown, not brand absence or zero',
                       'Mention share and citation share have different denominators',
                       'Citation observations are not qualified leads',
                       'A before/after result alone is not causal proof'):
            self.assertIn(phrase, text)

    def test_full_pack_and_delivery_are_required(self):
        brief = (ROOT / 'assets/aeo-site-evaluation-brief.md').read_text()
        for name in ('SOURCE.md', 'CLAIM-AUDIT.md', 'REPORT.md', 'APPLICABILITY.csv',
                     'PAGES.csv', 'PANEL.csv', 'MISSING-DATA.md', 'BRIEFS.md',
                     'MEASUREMENT.md', 'MANIFEST.json'):
            self.assertIn(name, brief)
        self.assertIn('not channel delivery', brief)
        self.assertIn('Do not start a competing implementation writer or worker', brief)

    def test_markdown_links_resolve_without_private_workspace_paths(self):
        for target in re.findall(r'`((?:assets|scripts)/[^`]+)`', GUIDE.read_text()):
            self.assertTrue((ROOT / target).is_file(), target)
        for path in (GUIDE, SOURCE, AUDIT):
            text = path.read_text()
            self.assertNotIn('/data/', text)
            self.assertNotIn('/root/', text)
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if target.startswith(('http:', 'https:', '#')):
                    continue
                target = target.split('#', 1)[0]
                self.assertTrue((path.parent / target).resolve().is_file(), (path, target))


if __name__ == '__main__':
    unittest.main()
