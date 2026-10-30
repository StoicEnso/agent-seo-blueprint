import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('packet', ROOT/'scripts/journalist_data_packet.py')
packet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packet)


class JournalistPacketTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = ROOT/'examples/journalist-data-public.csv'

    def mutate(self, **changes):
        with self.source.open(newline='') as f:
            rows = list(csv.DictReader(f))[:1]
        rows[0].update(changes)
        p = self.root/'input.csv'
        with p.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=packet.FIELDS)
            w.writeheader()
            w.writerows(rows)
        return p

    def test_real_source_regional_totals_and_changes(self):
        rows = packet.load_rows(self.source)
        self.assertEqual(len(rows), 9)
        for field in ('previous', 'current'):
            self.assertEqual(sum(r[field] for r in rows[:-1]), rows[-1][field])
        self.assertEqual((rows[-1]['previous'], rows[-1]['current']), (682, 783))
        self.assertEqual(rows[-1]['change_percent'], 14.8)
        self.assertEqual(rows[1]['change_percent'], 124.3)
        self.assertEqual(rows[5]['change_percent'], -16.9)

    def test_zero_denominator_is_undefined(self):
        rows = packet.load_rows(self.mutate(previous='0', current='5'))
        self.assertIsNone(rows[0]['change_percent'])

    def test_all_zero_chart_is_valid(self):
        out = self.root/'out'
        packet.build(self.mutate(previous='0', current='0'), out)
        ET.parse(out/'chart.svg')
        self.assertNotIn('nan', (out/'chart.svg').read_text())

    def test_reject_negative_decimal_nan_and_huge_counts(self):
        for value in ('-1', '1.5', 'NaN', '1000000000000'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                packet.load_rows(self.mutate(current=value))

    def test_formula_injection_rejected(self):
        for value in ('=HYPERLINK("bad")', '\t=bad', '+bad', '@bad'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                packet.load_rows(self.mutate(geography=value))

    def test_invalid_source_urls_rejected(self):
        for value in ('file:///etc/passwd', 'javascript:alert(1)', 'https://user:secret@example.org/data', 'https:///missing'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                packet.load_rows(self.mutate(source_url=value))

    def test_missing_field_rejected(self):
        with self.assertRaises(ValueError):
            packet.load_rows(self.mutate(source_locator=''))

    def test_same_period_rejected(self):
        with self.assertRaises(ValueError):
            packet.load_rows(self.mutate(period_current='2024-25'))

    def test_duplicate_observation_rejected(self):
        p = self.root/'duplicates.csv'
        with self.source.open() as f:
            lines = f.readlines()
        p.write_text(''.join([lines[0], lines[1], lines[1]]))
        with self.assertRaises(ValueError):
            packet.load_rows(p)

    def test_mixed_metric_rejected(self):
        with self.source.open(newline='') as f:
            rows = list(csv.DictReader(f))[:2]
        rows[1]['unit'] = 'different unit'
        p = self.root/'mixed.csv'
        with p.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=packet.FIELDS)
            w.writeheader()
            w.writerows(rows)
        with self.assertRaises(ValueError):
            packet.load_rows(p)

    def test_svg_escapes_text_and_uses_zero_baseline(self):
        out = self.root/'out'
        packet.build(self.mutate(geography='<script> & test'), out, '<Brand &>')
        svg = (out/'chart.svg').read_text()
        ET.fromstring(svg)
        self.assertNotIn('<script>', svg)
        self.assertIn('&lt;Brand &amp;&gt;', svg)
        self.assertIn('x="400"', svg)
        self.assertIn('aria-labelledby="title desc"', svg)

    def test_existing_output_is_not_overwritten(self):
        out = self.root/'out'
        packet.build(self.source, out)
        original = (out/'figures.json').read_bytes()
        with self.assertRaises(FileExistsError):
            packet.build(self.source, out)
        self.assertEqual(original, (out/'figures.json').read_bytes())

    def test_draft_outputs_and_no_send_claim(self):
        out = self.root/'out'
        packet.build(self.source, out)
        data = json.loads((out/'figures.json').read_text())
        self.assertEqual(data['publication'], 'NOT_APPROVED')
        self.assertEqual(data['outreach'], 'NOT_APPROVED')
        self.assertIn('NOT SENT', (out/'pitch-DRAFT.md').read_text())
        self.assertIn('Counts', (out/'chart.svg').read_text())
        self.assertEqual({p.name for p in out.iterdir()}, {'figures.json', 'data.csv', 'chart.svg', 'statistics.md', 'pitch-DRAFT.md'})

    def test_routes_and_guards_are_present(self):
        playbook = (ROOT/'references/playbooks/authority/journalist-ready-data-packets.md').read_text()
        for text in ('unverified anecdotes', 'public-source reanalysis', 'deterministic', 'small-cell', 'NOT', 'spokesperson', 'separately', 'AI citations'):
            self.assertIn(text.lower(), playbook.lower())
        self.assertIn('journalist-ready-data-packets.md', (ROOT/'SKILL.md').read_text())
        self.assertIn('journalist-ready-data-packets.md', (ROOT/'workflows/authority-and-links.md').read_text())
        fields = next(csv.reader((ROOT/'assets/journalist-data-brief.csv').open()))
        for name in ('privacy_review', 'reuse_rights_review', 'followup_gap', 'spokesperson_approval', 'publication_approval', 'outreach_approval', 'rendered_href_rel'):
            self.assertIn(name, fields)


if __name__ == '__main__':
    unittest.main()
