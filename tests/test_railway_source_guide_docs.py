import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'references/sources/railway-interview-source-guide.md'
PLAY = ROOT / 'references/playbooks/foundations/agent-discoverable-product-growth.md'
MAP = ROOT / 'references/railway-marketing-source-map.json'
PUB = 'https://www.knuckleup.co/episodes/jake-cooper'
VIDEO = 'https://www.youtube.com/watch?v=LQNqM1mA2e8'


class RailwaySourceGuideDocsTest(unittest.TestCase):
    def test_official_complete_source_is_linked_not_reproduced(self):
        text = GUIDE.read_text()
        for phrase in [PUB, VIDEO, 'not the full transcript', 'not republished',
                       'No permission to redistribute', 'Only the three explicitly labelled']:
            self.assertIn(phrase, text)
        data = json.loads(MAP.read_text())
        self.assertFalse(data['transcript']['raw_transcript_committed'])
        self.assertFalse(data['source_guide']['full_transcript_redistributed'])
        self.assertFalse(data['source_guide']['redistribution_permission_established'])
        self.assertLess(len(text.split()), 2200)

    def test_all_24_lessons_have_source_cards(self):
        guide = GUIDE.read_text()
        self.assertEqual(re.findall(r'^### Source (M\d\d)', guide, re.M),
                         [f'M{i:02}' for i in range(1, 25)])
        data = json.loads(MAP.read_text())
        for mechanism in data['mechanisms']:
            ident = mechanism['id']
            self.assertIn(f'<a id="source-{ident.lower()}"></a>', guide)
            self.assertEqual(mechanism['source_card'],
                             f'references/sources/railway-interview-source-guide.md#source-{ident.lower()}')
            self.assertEqual(mechanism['publisher_full_transcript_url'], PUB)
            section = guide.split(f'### Source {ident} —', 1)[1].split('\n### Source ', 1)[0]
            for number in mechanism['paragraphs']:
                self.assertIn(f'P{number:03}', section)
            self.assertIn('Source summary — our words', section)

    def test_each_playbook_lesson_links_to_its_evidence(self):
        play = PLAY.read_text()
        guide = GUIDE.read_text()
        for i in range(1, 25):
            ident = f'M{i:02}'
            section = play.split(f'### {ident} —', 1)[1].split('\n### M', 1)[0]
            self.assertIn(f'../../sources/railway-interview-source-guide.md#source-{ident.lower()}', section)
            self.assertIn(f'../playbooks/foundations/agent-discoverable-product-growth.md#lesson-{ident.lower()}', guide)
            self.assertIn(f'<a id="lesson-{ident.lower()}"></a>', play)

    def test_short_quotes_are_explicit_and_bounded(self):
        data = json.loads(MAP.read_text())
        quotes = data['short_quotations']
        self.assertEqual(len(quotes), 3)
        self.assertEqual(sum(len(q['text']) for q in quotes), 40)
        self.assertLessEqual(sum(len(q['text']) for q in quotes), 90)
        self.assertEqual(data['source_guide']['quotation_character_count'], 40)
        self.assertEqual(data['source_guide']['quote_verification'],
                         'exact_match_to_saved_publisher_text_not_full_audio_verification')
        guide = GUIDE.read_text()
        for quote in quotes:
            self.assertEqual(quote['speaker'], 'Jake Cooper')
            self.assertIn(f'“{quote["text"]}”', guide)
            self.assertIn(f'P{quote["paragraph"]:03}', guide)

    def test_timing_and_audio_limits_are_visible(self):
        guide = GUIDE.read_text()
        for phrase in ['full audio has not been independently checked',
                       'not publisher-provided anchors', 'broad navigation only',
                       'not a new timed transcript', 'not causal evidence of growth']:
            self.assertIn(phrase, guide)
        data = json.loads(MAP.read_text())
        self.assertFalse(data['transcript']['audio_verified'])
        self.assertFalse(data['transcript']['utterance_timestamps_available'])

    def test_publisher_chapters_keep_their_precision(self):
        chapters = json.loads(MAP.read_text())['source_guide']['publisher_chapters']
        self.assertEqual(len(chapters), 17)
        self.assertEqual(chapters[0]['seconds'], 0)
        self.assertEqual(chapters[-1]['seconds'], 4347)
        self.assertEqual([c['seconds'] for c in chapters], sorted(c['seconds'] for c in chapters))
        for chapter in chapters:
            self.assertEqual(chapter['precision'], 'publisher_chapter_start_not_utterance_timestamp')
            self.assertEqual(chapter['url'], VIDEO + f'&t={chapter["seconds"]}s')
            self.assertIn(chapter['url'], GUIDE.read_text())

    def test_readme_and_pdf_keep_the_new_evidence_discoverable(self):
        readme = (ROOT / 'README.md').read_text()
        self.assertIn('references/sources/railway-interview-source-guide.md', readme)
        self.assertIn('updated PDF includes this guide', readme)
        self.assertIn('../../sources/railway-interview-source-guide.md', PLAY.read_text())
        pdf = ROOT / 'docs/field-guides/railway-marketing-playbook.pdf'
        self.assertTrue(pdf.read_bytes().startswith(b'%PDF-'))
        self.assertGreater(pdf.stat().st_size, 150000)

    def test_no_absolute_archive_paths_in_the_guide(self):
        for text in [GUIDE.read_text(), PLAY.read_text(), MAP.read_text()]:
            self.assertNotRegex(text, r'/(?:data|root)/')
            self.assertNotRegex(text, r'telegram:\d{5,}')


if __name__ == '__main__':
    unittest.main()
