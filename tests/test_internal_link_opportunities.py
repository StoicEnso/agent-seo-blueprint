import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('links', ROOT / 'scripts/internal_link_opportunities.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class InternalLinksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.target = 'https://example.com/'
        self.row = {'url': 'https://example.com/blog/a', 'final_url': 'https://example.com/blog/a',
                    'status': 200, 'content_type': 'text/html', 'html_path': 'a.html'}

    def run_page(self, body='<article><p>Use AI landscape design to plan a yard.</p></article>', head=None, **overrides):
        head = '<link rel="canonical" href="https://example.com/blog/a">' if head is None else head
        (self.base/'a.html').write_text('<html><head>'+head+'</head><body>'+body+'</body></html>')
        row = dict(self.row, **overrides)
        return M.discover([row], self.target, ['AI landscape design'], self.base)['pages'][0]

    def test_proposes_only_review_with_hash(self):
        r = self.run_page()
        self.assertEqual(r['status'], 'candidate_review_only')
        self.assertEqual(r['approval'], 'not_granted')
        self.assertFalse(r['live_link_verified'])
        self.assertEqual(len(r['source_sha256']), 64)

    def test_skips_navigation_footer_and_script(self):
        for tag in ['nav', 'footer', 'header', 'aside', 'script', 'template', 'form', 'button']:
            with self.subTest(tag=tag):
                self.assertEqual(self.run_page(f'<{tag}><p>AI landscape design</p></{tag}>')['reason'], 'no_unlinked_phrase')

    def test_prefers_article_to_main_boilerplate(self):
        self.assertEqual(self.run_page('<main><p>AI landscape design</p><article><p>Different topic.</p></article></main>')['reason'], 'no_unlinked_phrase')

    def test_existing_home_navigation_is_not_contextual(self):
        self.assertEqual(self.run_page('<nav><a href="/">Home</a></nav><article><p>AI landscape design</p></article>')['status'], 'candidate_review_only')

    def test_existing_article_target_is_not_duplicated(self):
        r = self.run_page('<article><p>Use AI landscape design or <a href="/#start">our tool</a>.</p></article>')
        self.assertEqual(r['reason'], 'already_links_to_target_in_selected_scope')

    def test_no_nested_anchor(self):
        self.assertEqual(self.run_page('<article><p><a href="/other">AI landscape design</a></p></article>')['reason'], 'no_unlinked_phrase')

    def test_does_not_stitch_across_anchor(self):
        self.assertEqual(self.run_page('<article><p>AI <a href="/other">landscape</a> design</p></article>')['reason'], 'no_unlinked_phrase')

    def test_does_not_stitch_across_paragraphs(self):
        self.assertEqual(self.run_page('<article><p>AI landscape</p><p>design</p></article>')['reason'], 'no_unlinked_phrase')

    def test_inline_emphasis_case_and_whitespace(self):
        r = self.run_page('<article><p>Use ai <strong>LANDSCAPE</strong>\n design for this.</p></article>')
        self.assertEqual(r['status'], 'candidate_review_only')

    def test_word_boundary(self):
        self.assertEqual(self.run_page('<article><p>AI landscape designer</p></article>')['reason'], 'no_unlinked_phrase')

    def test_hidden_content(self):
        for attr in ['hidden', 'aria-hidden="true"', 'style="display: none"']:
            self.assertEqual(self.run_page(f'<article><p {attr}>AI landscape design</p></article>')['reason'], 'no_unlinked_phrase')

    def test_noindex_meta(self):
        self.assertEqual(self.run_page(head='<meta name="robots" content="noindex,follow">')['reason'], 'noindex')

    def test_xrobots_none(self):
        self.assertEqual(self.run_page(x_robots_tag='none')['reason'], 'noindex')

    def test_noncanonical_alias(self):
        self.assertEqual(self.run_page(head='<link rel="canonical" href="/">')['reason'], 'noncanonical_source')

    def test_missing_canonical(self):
        self.assertEqual(self.run_page(head='')['reason'], 'missing_or_multiple_canonicals')

    def test_multiple_canonicals(self):
        self.assertEqual(self.run_page(head='<link rel="canonical" href="/blog/a"><link rel="canonical" href="/blog/a">')['reason'], 'missing_or_multiple_canonicals')

    def test_base_needs_review(self):
        self.assertEqual(self.run_page(head='<base href="https://other.test/"><link rel="canonical" href="/blog/a">')['reason'], 'base_element_needs_manual_review')

    def test_redirect_status_and_hash(self):
        for changes, reason in [({'final_url':'https://example.com/blog/b'},'redirected_source'),
                                ({'status':404},'not_200_html'),
                                ({'content_type':'application/json'},'not_200_html'),
                                ({'sha256':'wrong'},'capture_hash_mismatch')]:
            self.assertEqual(self.run_page(**changes)['reason'], reason)

    def test_path_outside_manifest(self):
        self.assertEqual(self.run_page(html_path='../secret.html')['reason'], 'capture_outside_manifest_directory')

    def test_same_origin_and_self_link(self):
        self.assertEqual(self.run_page(url='https://other.test/a')['reason'], 'different_origin')
        self.assertEqual(self.run_page(url=self.target)['reason'], 'self_link')

    def test_protected_and_duplicate(self):
        self.run_page()
        result=M.discover([self.row,self.row],self.target,['AI landscape design'],self.base,[self.row['url']])
        self.assertEqual([r['reason'] for r in result['pages']],['protected_or_excluded','duplicate_source'])

    def test_body_fallback_is_labelled(self):
        self.assertEqual(self.run_page('<div><p>AI landscape design</p></div>')['extraction_scope'],'body_fallback')

    def test_invalid_url_and_missing_capture_are_errors(self):
        result=M.discover([{'url':'file:///etc/passwd'},self.row],self.target,['AI landscape design'],self.base)
        self.assertTrue(all(r['status']=='error' for r in result['pages']))

    def test_cli_and_input_preservation(self):
        self.run_page()
        (self.base/'manifest.json').write_text(json.dumps([self.row]))
        (self.base/'keywords.json').write_text(json.dumps(['AI landscape design']))
        before=(self.base/'a.html').read_bytes()
        command=[sys.executable,str(ROOT/'scripts/internal_link_opportunities.py'),'--manifest',str(self.base/'manifest.json'),'--keywords',str(self.base/'keywords.json'),'--target',self.target,'--out',str(self.base/'result.json')]
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads((self.base/'result.json').read_text())
        self.assertEqual((data['network_requests'],data['site_edits'],len(data['candidates'])),(0,0,1))
        self.assertEqual((self.base/'a.html').read_bytes(),before)
        command[-1]=str(self.base/'a.html')
        self.assertNotEqual(subprocess.run(command,capture_output=True).returncode,0)
        self.assertEqual((self.base/'a.html').read_bytes(),before)

    def test_docs_and_routes_exist(self):
        ref='references/playbooks/content/internal-linking-optimisations.md'
        for file in ['SKILL.md','README.md','workflows/site-audit.md','workflows/content-production.md']:
            self.assertIn('internal-linking-optimisations', (ROOT/file).read_text())
        text=(ROOT/ref).read_text()
        for phrase in ['not a Google requirement','No extension was installed','No automatic publication','first-party','28-day','56-day','MaillageBooster']:
            self.assertIn(phrase,text)


if __name__=='__main__':
    unittest.main()
