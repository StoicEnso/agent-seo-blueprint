import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'references/playbooks/content/agent-article-production-qa.md'
COMMERCE = ROOT / 'references/playbooks/maintenance/ai-search-commerce-readiness.md'
IDS = {'markdown_parity', 'agent_signup', 'answer_first', 'original_data', 'html_comparison', 'author_schema', 'buyer_faq', 'bing_discovery', 'provider_access', 'source_quotes'}

class AiSearchPageReviewDocsTest(unittest.TestCase):
    def setUp(self):
        self.text = QA.read_text()
        self.review = self.text.split('## Optional AI-search page-structure review', 1)[1]
        self.template = json.loads((ROOT / 'assets/ai-search-page-review.json').read_text())

    def test_all_ten_claims_have_a_unique_documented_template_id(self):
        checks = self.template['checks']
        self.assertEqual(len(checks), 10)
        self.assertEqual({c['claim_id'] for c in checks}, IDS)
        for key in IDS:
            self.assertEqual(self.review.count('| `' + key + '` |'), 1)

    def test_template_is_not_fabricated_evidence(self):
        for field in ('page_url', 'canonical_url', 'captured_at', 'page_type'):
            self.assertIsNone(self.template[field])
        self.assertEqual(self.template['platform_scope'], [])
        for check in self.template['checks']:
            self.assertEqual(check['state'], 'not_checked')
            self.assertEqual(check['evidence'], [])
            self.assertIsNone(check['finding'])
            self.assertIsNone(check['owner'])
        self.assertIn('not a passed audit', self.review)

    def test_template_preserves_evidence_scope_and_unknowns(self):
        for check in self.template['checks']:
            for field in ('claim_id', 'state', 'evidence', 'not_applicable_reason', 'finding', 'recommendation', 'owner'):
                self.assertIn(field, check)
        self.assertIn('pass`, `fail` and `mixed` require observed evidence', self.review)
        self.assertIn('not_applicable` requires a reason', self.review)

    def test_routes_resolve_without_a_new_playbook_or_workflow(self):
        for file in ('SKILL.md', 'README.md', 'workflows/geo-audit.md'):
            text = (ROOT / file).read_text()
            self.assertIn('references/playbooks/content/agent-article-production-qa.md', text)
            self.assertIn('assets/ai-search-page-review.json', text)
        self.assertIn('### Optional AI-search page-structure review', (ROOT / 'README.md').read_text())
        self.assertIn('## Optional AI-search page-structure review', self.text)
        self.assertEqual(len(list((ROOT / 'workflows').glob('*.md'))), 11)

    def test_vendor_claim_is_not_the_geo_query_benchmark(self):
        for phrase in ('10K websites ranked #1 in LLMs', 'unverified vendor claim', '10,000 **queries**', '25+ agents', 'was not tested'):
            self.assertIn(phrase, self.review)

    def test_markdown_does_not_create_a_google_requirement(self):
        for phrase in ('are not mandatory', 'same material facts, prices, limits', 'must not hide different offers', 'Missing `llms.txt` is not a Google defect'):
            self.assertIn(phrase, self.review)

    def test_word_counts_and_original_statistics_are_not_quotas(self):
        for phrase in ('Do not force a definition-plus-number formula', 'denominator', 'collection dates', 'illustrative 43%', 'never invent research'):
            self.assertIn(phrase.lower(), self.review.lower())

    def test_comparisons_and_authorship_require_real_evidence(self):
        for phrase in ('a real `table`', 'headers, caption/context', 'commercial relationship', 'Use only genuine identities', 'advance dates without a substantive change'):
            self.assertIn(phrase, self.review)

    def test_faq_does_not_invent_buyer_or_search_data(self):
        for phrase in ('model-generated questions are hypotheses', 'saved exact provider prompts', 'FAQ rich results are no longer shown', 'Do not auto-add FAQPage/HowTo'):
            self.assertIn(phrase, self.review)

    def test_bing_and_indexnow_receipts_are_not_indexing_proof(self):
        for phrase in ('not a proven sole or sufficient ChatGPT gateway', 'missing `site:` result is not proof', 'genuine added, changed or deleted owned URLs', 'do not ping unchanged pages', 'HTTP 202 means key validation pending', 'Neither proves a crawl, index entry, citation or traffic'):
            self.assertIn(phrase, self.review)

    def test_signup_stops_before_consequential_effects(self):
        text = COMMERCE.read_text()
        for phrase in ('owner-approved test environment', 'exact authorised stop boundary', 'without weakening them', 'not a successful signup', 'Actual account creation, outbound email, OAuth consent, subscription/payment', 'Redact credentials'):
            self.assertIn(phrase, text)
        self.assertEqual(self.template['agent_usability']['state'], 'not_checked')
        self.assertIsNone(self.template['agent_usability']['authorized_stop_boundary'])

    def test_search_training_and_user_fetches_remain_distinct(self):
        for phrase in ('Search, training and user-triggered fetches are different controls', 'OAI-SearchBot', 'PerplexityBot', 'Claude-SearchBot', 'GPTBot/ClaudeBot', 'No blanket allow rule'):
            self.assertIn(phrase, self.review)

    def test_geo_uplift_has_study_specific_limits(self):
        for phrase in ('up to 40%', 'benchmark visibility metrics', 'not a current cross-provider forecast', '40-point citation-rate rise', 'traffic/revenue lift'):
            self.assertIn(phrase, self.review)
        self.assertIn('https://arxiv.org/html/2311.09735v3', self.review)

    def test_image_structure_and_ctas_are_optional(self):
        for phrase in ('19 numbered elements', 'seven conversion placements', 'six technical cards', 'do not install all seven', 'not verified measurements', 'no 3–6-link quota', 'Do not require SSR'):
            self.assertIn(phrase, self.review)
        self.assertEqual(self.template['optional_components'], [])
        self.assertEqual(self.template['conversion_experiments'], [])

    def test_outcomes_and_authority_are_never_preclaimed(self):
        self.assertEqual(set(self.template['outcomes']), {'indexing', 'citations', 'referrals', 'conversions', 'revenue', 'causality'})
        for outcome in self.template['outcomes'].values():
            self.assertEqual(outcome['evidence'], [])
            self.assertIn(outcome['state'], ('not_checked', 'not_measured', 'not_established'))
        self.assertEqual(self.template['approval']['state'], 'not_requested')
        self.assertIn('No cadence or follow-up is activated', self.review)

    def test_readme_category_counts_match_actual_files(self):
        readme = (ROOT / 'README.md').read_text()
        for directory in (ROOT / 'references/playbooks').iterdir():
            if directory.is_dir():
                count = len(list(directory.rglob('*.md')))
                self.assertRegex(readme, re.escape(directory.name + '/') + r'\s+\(' + str(count) + r'\)')

    def test_primary_sources_and_source_attribution_present(self):
        for url in ('https://x.com/irabukht/status/2114031412991218048', 'https://developers.google.com/search/docs/appearance/ai-features', 'https://developers.openai.com/api/docs/bots', 'https://www.indexnow.org/documentation', 'https://llmstxt.org/', 'https://developers.google.com/search/updates#removing-faq-rich-result'):
            self.assertIn(url, self.review)

if __name__ == '__main__':
    unittest.main()
