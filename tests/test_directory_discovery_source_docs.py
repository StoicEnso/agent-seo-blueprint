import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DirectoryDiscoverySourceDocsTests(unittest.TestCase):
    def test_source_registry_marks_directory_finder_discovery_only(self):
        path = ROOT / "assets" / "directory-discovery-sources.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        self.assertGreaterEqual(len(rows), 2)
        row = next(item for item in rows if item["source_name"] == "Directory Finder")
        self.assertEqual(row["verification_status"], "DISCOVERY_SOURCE_ONLY")
        self.assertEqual(row["last_observed_at"], "2026-08-07")
        self.assertEqual(row["observed_candidate_count"], "68")
        self.assertIn("submission_route", row["source_claimed_fields"])
        self.assertIn("third-party claims", row["notes"])
        self.assertIn("do not bulk-endorse", row["notes"])

    def test_social_starter_pack_is_registered_but_not_bulk_endorsed(self):
        path = ROOT / "assets" / "directory-discovery-sources.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        row = next(
            item
            for item in rows
            if item["source_url"]
            == "https://x.com/2whazzuup/status/2086169566108069962"
        )
        self.assertEqual(row["verification_status"], "DISCOVERY_SOURCE_ONLY")
        self.assertEqual(row["last_observed_at"], "2026-08-09")
        self.assertEqual(row["observed_candidate_count"], "35")
        self.assertIn("not bulk-imported", row["notes"])

    def test_candidate_queue_preserves_unverified_source_lineage(self):
        path = ROOT / "assets" / "startup-backlink-candidates.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fields = set(reader.fieldnames or [])

        self.assertEqual(len(rows), 190)
        self.assertTrue(
            {
                "source_url",
                "source_entry_url",
                "source_observed_at",
                "source_claimed_dr_unverified",
                "source_claimed_traffic_unverified",
                "source_claimed_cost_unverified",
                "source_claimed_approval_time_unverified",
                "source_claimed_link_attribute_unverified",
            }.issubset(fields)
        )
        directory_rows = [row for row in rows if row["route_type"] != "hosted_publishing_experiment"]
        self.assertEqual(len(directory_rows), 189)
        self.assertTrue(
            all(row["verification_status"] == "UNVERIFIED_SOURCE_LEAD" for row in directory_rows)
        )

        directory_finder_rows = [
            row for row in rows if row["source_url"] == "https://directoryfinder.com/"
        ]
        self.assertEqual(len(directory_finder_rows), 19)
        names = {row["candidate_name"] for row in directory_finder_rows}
        self.assertTrue(
            {
                "G2",
                "Capterra",
                "Crunchbase",
                "TopAI.tools",
                "DevTool.io",
                "API Finder",
                "QuestionDB Hub",
                "OpenClaw Directory",
                "Trustpilot",
                "Wellfound",
            }.issubset(names)
        )
        self.assertTrue(
            all(row["source_observed_at"] == "2026-08-07" for row in directory_finder_rows)
        )
        self.assertTrue(
            all(row["source_entry_url"].startswith("https://directoryfinder.com/dir/") for row in directory_finder_rows)
        )
        self.assertTrue(
            all("Relevance scope:" in row["notes"] for row in directory_finder_rows)
        )
        excluded = {
            "Yelp",
            "Tripadvisor",
            "Philly Home Pros",
            "Psychology Today",
            "Zocdoc",
            "CoinMarketCap",
            "Awwwards",
            "Best of the Web",
            "Jasmine Directory",
            "Blogarama",
        }
        self.assertTrue(names.isdisjoint(excluded))

    def test_publicly_linked_directory_reference_stays_an_unverified_queue(self):
        path = ROOT / "assets" / "startup-backlink-candidates.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        source_url = "https://gist.github.com/sosidudku1/311f704aed8fec04770b37c02a29e904"
        added = [row for row in rows if row["source_url"] == source_url]
        self.assertEqual(len(added), 48)
        self.assertEqual(len({row["canonical_domain"] for row in added}), 48)
        self.assertTrue(all(row["verification_status"] == "UNVERIFIED_SOURCE_LEAD" for row in added))
        self.assertTrue(all(row["submission_url"] == "" for row in added))
        self.assertTrue(all(row["public_indexable"] == "unknown" for row in added))
        self.assertTrue(all("not first-party verified" in row["notes"] for row in added))

        registry = ROOT / "assets" / "directory-discovery-sources.csv"
        with registry.open(newline="", encoding="utf-8") as handle:
            source_rows = list(csv.DictReader(handle))
        source = next(row for row in source_rows if row["source_url"] == source_url)
        self.assertEqual(source["verification_status"], "DISCOVERY_SOURCE_ONLY")
        self.assertEqual(source["observed_candidate_count"], "130")
        self.assertIn("first-party verification", source["notes"])

    def test_reference_intake_rejects_aliases_unavailable_and_unrelated_destinations(self):
        with (ROOT / "assets/startup-backlink-candidates.csv").open(newline="", encoding="utf-8") as handle:
            added = [row for row in csv.DictReader(handle) if row["source_url"].startswith("https://gist.github.com/sosidudku1/")]
        expected_source_ids = {2, 4, 7, 9, 10, 12, 13, 14, 16, 17, 19, 20, 25, 28, 29, 31, 33, 34, 35, 38, 39, 43, 44, 45, 50, 51, 54, 55, 56, 57, 63, 67, 69, 70, 73, 74, 75, 77, 78, 79, 80, 83, 85, 86, 98, 99, 100, 124}
        self.assertEqual({int(row["source_row_numbers"]) for row in added}, expected_source_ids)
        excluded_domains = {"startupstash.com", "toolpilot.ai", "aitoolhunt.com", "aitoolz.net", "ai-finder.net", "aeotools.space", "aiscoop.com", "remote.tools", "creativeaitools.com", "aipediahub.com", "copytools.ai", "aidesigntools.io"}
        self.assertTrue({row["canonical_domain"] for row in added}.isdisjoint(excluded_domains))
        for row in added:
            for key in ("source_claimed_dr_unverified", "source_claimed_cost_unverified", "source_claimed_link_attribute_unverified", "last_verified_at"):
                self.assertEqual(row[key], "")

    def test_specialist_surfaces_and_discovery_lists_keep_their_eligibility_gates(self):
        with (ROOT / "assets/startup-backlink-candidates.csv").open(newline="", encoding="utf-8") as handle:
            rows = {row["candidate_name"]: row for row in csv.DictReader(handle)}
        for name in ("Zapier App Directory", "Slack App Directory", "Notion Integrations Gallery"):
            self.assertEqual(rows[name]["route_type"], "marketplace")
            self.assertIn("not a general SaaS listing", rows[name]["notes"])
        self.assertEqual(rows["Awesome AI Tools (GitHub)"]["route_type"], "asset_contribution")
        self.assertIn("mahseema/awesome-ai-tools", rows["Awesome AI Tools (GitHub)"]["source_entry_url"])
        self.assertNotIn("Top AI Directories", rows)
        with (ROOT / "assets/directory-discovery-sources.csv").open(newline="", encoding="utf-8") as handle:
            discovery = {row["source_name"]: row for row in csv.DictReader(handle)}
        self.assertEqual(discovery["Top AI Directories"]["verification_status"], "DISCOVERY_SOURCE_ONLY")
        self.assertIn("Login/payment", discovery["Top AI Directories"]["notes"])

    def test_submission_tracker_separates_claims_from_direct_observations(self):
        path = ROOT / "assets" / "directory-submission-tracker.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            self.assertEqual(list(reader), [])

        self.assertTrue(
            {
                "discovery_source",
                "source_entry_url",
                "source_observed_at",
                "source_claimed_dr_unverified",
                "source_claimed_traffic_unverified",
                "source_claimed_cost_unverified",
                "source_claimed_approval_time_unverified",
                "source_claimed_link_attribute_unverified",
                "submission_url",
                "submission_url_verified_at",
                "cost",
                "link_attribute",
                "indexable",
                "last_verified_at",
                "evidence",
            }.issubset(fields)
        )

    def test_playbooks_require_first_party_destination_evidence(self):
        directory = (
            ROOT
            / "references"
            / "playbooks"
            / "authority"
            / "directory-submissions.md"
        ).read_text(encoding="utf-8")
        startup = (
            ROOT
            / "references"
            / "playbooks"
            / "authority"
            / "startup-backlink-directory-submissions.md"
        ).read_text(encoding="utf-8")
        workflow = (ROOT / "workflows" / "authority-and-links.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("## First-party verification gate", directory)
        self.assertIn("destination-owned", directory)
        self.assertIn("This is not an endorsement of all 68 destinations", directory)
        self.assertIn("## Conditional local-entity baseline", directory)
        self.assertIn("online-only startup should not manufacture a location", directory)
        self.assertIn("Not a marketing directory or backlink tactic", directory)
        self.assertIn("not interchangeable directory submissions", directory)
        self.assertIn("A `dofollow` claim does not justify payment", directory)
        self.assertIn("## Source audit before candidate verification", startup)
        self.assertIn("do not bulk-promote", startup.lower())
        self.assertIn("Treat aggregators as discovery only", workflow)
        self.assertIn("Do not buy a placement merely because a source claims high DR", workflow)


if __name__ == "__main__":
    unittest.main()
