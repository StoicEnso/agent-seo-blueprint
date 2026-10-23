import collections
import csv
import hashlib
import json
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ASSET = 'assets/rankinpublic-directory-source-20261023.csv'
PAGE = 'https://rankinpublic.xyz/directory-submission-service'
RAW_SOURCE_DIGEST = '8a7d09fb7a31eac73710dee05e32d40e5085b4650472163e36274c3654682997'


def read_rows(rel):
    with (ROOT / rel).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


class RankInPublicDirectoryIntakeTests(unittest.TestCase):
    def setUp(self):
        self.rows = read_rows(ASSET)

    def test_exact_complete_observed_source_not_advertised_catalog(self):
        self.assertEqual(len(self.rows), 201)
        self.assertEqual([int(r['source_row']) for r in self.rows], list(range(1, 202)))
        original = [dict(name=r['candidate_name'], dr=float(r['source_claimed_dr_unverified']),
                         site_url=r['source_entry_url'], type=r['source_claimed_type_unverified'])
                    for r in self.rows]
        digest = hashlib.sha256(json.dumps(original, ensure_ascii=False,
                    separators=(',', ':'), sort_keys=True).encode()).hexdigest()
        self.assertEqual(digest, RAW_SOURCE_DIGEST)

    def test_unique_normalized_source_hostnames_not_destination_verification(self):
        hosts = [urlsplit(r['source_entry_url']).hostname.lower().removeprefix('www.') for r in self.rows]
        self.assertEqual(len(set(hosts)), 201)
        self.assertEqual(hosts, [r['canonical_domain'] for r in self.rows])
        for row in self.rows:
            self.assertEqual(row['verification_status'], 'UNVERIFIED_SOURCE_LEAD')
            self.assertIn('no destination visit', row['notes'])
            self.assertTrue(0 <= float(row['source_claimed_dr_unverified']) <= 100)
            self.assertTrue(row['fit_gate'])

    def test_lineage_is_complete_and_claims_are_qualified(self):
        for row in self.rows:
            self.assertEqual(row['source_url'], PAGE)
            self.assertEqual(row['source_observed_at'], '2026-10-23')
            self.assertEqual(row['source_post_url'], 'https://x.com/antonioescudero/status/2113691684739674556')
            self.assertEqual(row['source_comment_url'], 'https://x.com/antonioescudero/status/2113691938767699998')
            self.assertIn('Unknown cost, link behavior and indexability', row['notes'])
            self.assertIn('no account, payment or submission authorized', row['notes'])

    def test_baseline_states_keep_main_documents_pending_and_gaps_separate(self):
        self.assertEqual(collections.Counter(r['baseline_coverage'] for r in self.rows), {
            'MAIN_CANDIDATE_NAME_ONLY': 8, 'MAIN_DOC_DOMAIN_ONLY': 1,
            'MAIN_DOC_NAME_ONLY': 2, 'OPEN_PR_CANDIDATE': 12,
            'NAME_COLLISION_REVIEW': 2, 'NEW_SOURCE_LEAD': 176,
        })
        for row in self.rows:
            if row['baseline_coverage'] == 'OPEN_PR_CANDIDATE':
                self.assertIn('origin/henry/', row['existing_evidence'])
            elif row['baseline_coverage'] == 'NEW_SOURCE_LEAD':
                self.assertFalse(row['existing_evidence'])
            else:
                self.assertIn('origin/main:', row['existing_evidence'])

    def test_six_post_recommendations_have_explicit_prior_coverage(self):
        rows = {r['canonical_domain']: r for r in self.rows}
        for domain in ['crunchbase.com', 'stackshare.io', 'saashub.com']:
            self.assertEqual(rows[domain]['baseline_coverage'], 'MAIN_CANDIDATE_NAME_ONLY')
        self.assertEqual(rows['brownbook.net']['baseline_coverage'], 'MAIN_DOC_NAME_ONLY')
        for domain in ['callupcontact.com', 'viesearch.com']:
            self.assertEqual(rows[domain]['baseline_coverage'], 'NEW_SOURCE_LEAD')
        self.assertEqual(rows['ctrlalt.cc']['baseline_coverage'], 'MAIN_DOC_DOMAIN_ONLY')

    def test_name_collision_does_not_merge_distinct_source_domains(self):
        collision = [r for r in self.rows if r['baseline_coverage'] == 'NAME_COLLISION_REVIEW']
        self.assertEqual({r['canonical_domain'] for r in collision}, {'nxgntools.com', 'nextgentools.me'})
        self.assertEqual(len(collision), 2)
        self.assertTrue(all('do not merge by normalized name' in r['notes'] for r in collision))

    def test_category_fit_does_not_promote_community_or_local_spam(self):
        gates = {
            'General Directory': 'BUSINESS_CATEGORY_AND_GEOGRAPHY',
            'Community': 'NATIVE_COMMUNITY_CONTRIBUTION_NOT_DIRECTORY_SPAM',
            'Media': 'EDITORIAL_RELEVANCE_NOT_AUTOMATIC_LISTING',
            'Others': 'SOURCE_TYPE_AND_REAL_READER_VALUE_UNCLEAR',
        }
        for row in self.rows:
            if row['source_claimed_type_unverified'] in gates:
                self.assertEqual(row['fit_gate'], gates[row['source_claimed_type_unverified']])

    def test_inventory_is_discoverable_but_not_bulk_added_to_project_queue(self):
        source = [r for r in read_rows('assets/directory-discovery-sources.csv') if r['source_url'] == PAGE]
        self.assertEqual(len(source), 1)
        self.assertEqual(source[0]['observed_candidate_count'], '201')
        self.assertEqual(source[0]['verification_status'], 'DISCOVERY_SOURCE_ONLY')
        self.assertIn(ASSET, source[0]['notes'])
        self.assertEqual(len(read_rows('assets/startup-backlink-candidates.csv')), 142)
        self.assertEqual(read_rows('assets/directory-submission-tracker.csv'), [])
        playbook = (ROOT / 'references/playbooks/authority/directory-submissions.md').read_text()
        self.assertIn(ASSET, (ROOT / 'README.md').read_text())
        for phrase in [ASSET, 'not an approved submission queue', 'not the number extracted or verified',
                       'unmerged', 'First-party verification gate', 'Do not bulk-import all 201',
                       'no followed link, DR increase, ranking, traffic or AI citation is promised',
                       'nxgntools.com', 'nextgentools.me']:
            self.assertIn(phrase, playbook)


if __name__ == '__main__':
    unittest.main()
