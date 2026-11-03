"""Offline checks for the dated 186-row source intake; no network or writes."""
import csv
import unittest
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = "https://www.dotstore.io/blog/186-launchpads-to-list-your-startup-and-get-backlinks"
POST = "https://x.com/voidyaps/status/2117211405430685874"


def read_csv(relative):
    with (ROOT / relative).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader), reader.fieldnames


class VoidyapsDirectoryIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit, cls.audit_fields = read_csv("assets/voidyaps-directory-intake-20261103.csv")
        cls.candidates, cls.candidate_fields = read_csv("assets/voidyaps-missing-candidates.csv")
        cls.by_row = {int(row["source_row"]): row for row in cls.audit}

    def test_full_source_order_is_preserved(self):
        self.assertEqual([int(r["source_row"]) for r in self.audit], list(range(1, 187)))
        self.assertEqual(self.by_row[1]["candidate_name"], "dotstore")
        self.assertEqual(self.by_row[186]["candidate_name"], "Pro Launch")

    def test_all_dispositions_reconcile(self):
        counts = Counter(r["decision"] for r in self.audit)
        self.assertEqual(counts["EXISTING_MAIN"], 31)
        self.assertEqual(counts["EXISTING_PENDING_PR"], 60)
        self.assertEqual(counts["NEW_UNVERIFIED_CANDIDATE"], 77)
        self.assertEqual(sum(counts.values()), 186)
        self.assertEqual(186 - 31 - 60 - 77, 18)

    def test_new_domains_are_unique_and_exactly_the_new_disposition(self):
        expected = {r["canonical_domain"] for r in self.audit if r["decision"] == "NEW_UNVERIFIED_CANDIDATE"}
        actual = {r["canonical_domain"] for r in self.candidates}
        self.assertEqual(len(self.candidates), 77)
        self.assertEqual(len(actual), 77)
        self.assertEqual(actual, expected)
        self.assertEqual(len({r["canonical_domain"] for r in self.audit}), 186)

    def test_new_queue_uses_the_existing_schema(self):
        legacy, fields = read_csv("assets/startup-backlink-candidates.csv")
        self.assertEqual(self.candidate_fields, fields)
        self.assertFalse(any(r["source_url"] == ARTICLE for r in legacy))
        self.assertTrue(all(None not in r for r in self.candidates))

    def test_claims_never_become_verified_candidate_outcomes(self):
        for row in self.candidates:
            with self.subTest(name=row["candidate_name"]):
                self.assertEqual(row["verification_status"], "UNVERIFIED_SOURCE_LEAD")
                self.assertEqual(row["public_indexable"], "unknown")
                self.assertEqual(row["link_attribute"], "unknown")
                self.assertEqual(row["submission_url"], "")
                self.assertEqual(row["last_verified_at"], "")
                self.assertEqual(row["source_claimed_traffic_unverified"], "")
                self.assertEqual(row["source_claimed_approval_time_unverified"], "")
                self.assertIn("not destination-verified", row["notes"])

    def test_source_provenance_and_dates_are_complete(self):
        for row in self.audit:
            self.assertEqual(row["source_url"], ARTICLE)
            self.assertEqual(row["source_post_url"], POST)
            self.assertEqual(row["source_observed_at"], "2026-11-03")
            self.assertTrue(row["source_entry_url"].startswith("https://www.dotstore.io/"))
            self.assertEqual(row["verification_status"], "UNVERIFIED_SOURCE_LEAD")
            self.assertTrue(row["fit_gate"])
        for row in self.candidates:
            self.assertEqual(row["source_url"], ARTICLE)
            self.assertEqual(row["source_observed_at"], "2026-11-03")
            self.assertEqual(row["source_mentions"], "1")
            source = self.by_row[int(row["source_row_numbers"])]
            self.assertEqual(source["source_entry_url"], row["source_entry_url"])

    def test_domain_identity_comes_from_source_url_not_aggregator_host(self):
        for row in self.audit:
            host = urlsplit(row["destination_url_source_claimed"]).hostname
            self.assertIsNotNone(host)
            self.assertEqual(row["canonical_domain"], host.lower().removeprefix("www.").rstrip("."))
            if int(row["source_row"]) != 1:
                self.assertNotEqual(row["canonical_domain"], "dotstore.io")

    def test_main_and_pending_coverage_are_not_conflated(self):
        for row in self.audit:
            if row["decision"] == "EXISTING_MAIN":
                self.assertTrue(row["existing_evidence"].startswith("origin/main:"))
            elif row["decision"] == "EXISTING_PENDING_PR":
                self.assertTrue(row["existing_evidence"].startswith("origin/henry/"))
            elif row["decision"] == "NEW_UNVERIFIED_CANDIDATE":
                self.assertEqual(row["existing_evidence"], "")

    def test_known_domain_conflicts_are_not_hidden_by_name_matching(self):
        for row in self.audit:
            if row["matched_domain"]:
                self.assertEqual(row["matched_domain"], row["canonical_domain"])

    def test_launch_names_do_not_collapse_different_entities(self):
        self.assertEqual(self.by_row[58]["canonical_domain"], "trylaunch.ai")
        self.assertEqual(self.by_row[184]["canonical_domain"], "launchsoar.com")
        self.assertEqual(self.by_row[58]["decision"], "EXISTING_PENDING_PR")
        self.assertEqual(self.by_row[184]["decision"], "NEW_UNVERIFIED_CANDIDATE")
        self.assertEqual(self.by_row[83]["canonical_domain"], "launchit.fast")
        self.assertEqual(self.by_row[163]["canonical_domain"], "launchit.site")
        self.assertEqual(len({r["candidate_name"].lower() for r in self.candidates}), 77)
        for number in [83, 163, 184]:
            row = next(r for r in self.candidates if r["source_row_numbers"] == str(number))
            self.assertIn(row["canonical_domain"], row["candidate_name"])

    def test_aliases_retain_original_source_labels(self):
        self.assertEqual(self.by_row[59]["candidate_name"], "G2 Crowd")
        self.assertEqual(self.by_row[59]["matched_name"], "G2")
        self.assertNotEqual(self.by_row[4]["decision"], "NEW_UNVERIFIED_CANDIDATE")
        self.assertNotEqual(self.by_row[50]["decision"], "NEW_UNVERIFIED_CANDIDATE")

    def test_free_claim_is_not_applied_to_priced_rows(self):
        priced = [r for r in self.audit if "$" in r["source_claimed_note_unverified"]]
        self.assertEqual(len(priced), 14)
        for row in priced:
            self.assertIn("$", row["source_claimed_cost_unverified"])
        self.assertEqual(self.by_row[13]["source_claimed_cost_unverified"], "$16")
        self.assertEqual(self.by_row[54]["source_claimed_cost_unverified"], "$249")

    def test_link_conditions_survive_and_do_not_become_observed_rel(self):
        self.assertIn("only if you rank", self.by_row[21]["source_claimed_link_attribute_unverified"])
        self.assertIn("unless you pay", self.by_row[49]["source_claimed_link_attribute_unverified"])
        self.assertIn("redirect", self.by_row[86]["source_claimed_link_attribute_unverified"])
        self.assertTrue(all(r["link_attribute"] == "unknown" for r in self.candidates))

    def test_unrelated_app_and_identity_mismatch_are_not_queued(self):
        self.assertEqual(self.by_row[136]["decision"], "NOT_A_DIRECTORY")
        self.assertIn("journal", self.by_row[136]["fit_gate"])
        self.assertEqual(self.by_row[131]["decision"], "IDENTITY_REVIEW_HOLD")
        self.assertIn("reviews.financesonline.com", self.by_row[131]["fit_gate"])
        self.assertEqual(self.by_row[182]["decision"], "NOT_A_DIRECTORY")

    def test_services_are_not_counted_as_directory_placements(self):
        for number in [81, 183]:
            self.assertEqual(self.by_row[number]["decision"], "SUBMISSION_SERVICE_OR_DISCOVERY")
        new = {int(r["source_row_numbers"]) for r in self.candidates}
        self.assertTrue(new.isdisjoint({81, 183, 185}))

    def test_specialty_routes_and_generic_web_lists_are_kept_visible(self):
        for number in [25, 35, 55, 63, 82, 89, 103, 141, 178]:
            self.assertEqual(self.by_row[number]["decision"], "CONDITIONAL_NON_DIRECTORY")
        for number in [78, 99, 148, 168]:
            self.assertEqual(self.by_row[number]["decision"], "OUT_OF_SCOPE_GENERIC_WEB")

    def test_low_dr_is_not_a_standalone_rejection(self):
        row = self.by_row[71]
        self.assertEqual(row["source_claimed_dr_unverified"], "16")
        self.assertEqual(row["decision"], "NEW_UNVERIFIED_CANDIDATE")
        self.assertIn("not a rejection", row["fit_gate"])

    def test_financial_profiles_require_truthful_approved_facts(self):
        for number in [20, 40, 96]:
            self.assertIn("truthful approved", self.by_row[number]["fit_gate"])
        self.assertIn("complete placement gate is not verified", self.by_row[100]["fit_gate"])

    def test_registry_is_discovery_only_not_a_free_or_verified_catalog(self):
        rows, _ = read_csv("assets/directory-discovery-sources.csv")
        found = [r for r in rows if r["source_url"] == ARTICLE]
        self.assertEqual(len(found), 1)
        row = found[0]
        self.assertEqual(row["observed_candidate_count"], "186")
        self.assertEqual(row["verification_status"], "DISCOVERY_SOURCE_ONLY")
        self.assertIn("Not all free", row["notes"])
        self.assertIn("No verified backlink", row["notes"])

    def test_existing_routing_reaches_the_new_assets(self):
        for rel in ["README.md", "workflows/authority-and-links.md", "references/playbooks/authority/startup-backlink-directory-submissions.md"]:
            text = (ROOT / rel).read_text()
            self.assertIn("voidyaps-missing-candidates.csv", text)
        guide = (ROOT / "references/playbooks/authority/startup-backlink-directory-submissions.md").read_text()
        self.assertIn("Pending PR coverage is not merged coverage", guide)
        self.assertIn("not an all-free list", guide)
        self.assertIn("186", guide)
        self.assertIn("77", guide)

    def test_urls_are_public_http_data_without_credentials(self):
        for row in self.audit:
            for field in ["source_url", "source_post_url", "source_entry_url", "destination_url_source_claimed"]:
                value = urlsplit(row[field])
                self.assertIn(value.scheme, {"http", "https"})
                self.assertIsNone(value.username)
                self.assertIsNone(value.password)
            self.assertTrue(row["source_claimed_dr_unverified"].isdigit())
            self.assertLessEqual(int(row["source_claimed_dr_unverified"]), 100)


if __name__ == "__main__":
    unittest.main()
