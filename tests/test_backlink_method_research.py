import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BacklinkMethodsResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "assets/backlink-method-research.csv").open(newline="") as f:
            cls.rows = list(csv.DictReader(f))
        cls.review = json.loads((ROOT / "assets/backlink-method-source-review-20261024.json").read_text())
        cls.doc = (ROOT / "references/playbooks/authority/other-link-building.md").read_text()

    def test_exact_26_unique_research_rows(self):
        self.assertEqual(len(self.rows), 26)
        self.assertEqual({r["method_id"] for r in self.rows}, {f"BM{i:02}" for i in range(1, 27)})
        self.assertTrue(all(r["action_status"] == "RESEARCH_ONLY_NOT_APPROVED" for r in self.rows))

    def test_all_rows_have_real_source_and_fit(self):
        for row in self.rows:
            for field in ["source_url", "source_observed_at", "reader_value", "prerequisites", "next_check"]:
                self.assertTrue(row[field], (row["method_id"], field))
            self.assertRegex(row["source_url"], r"https://x[.]com/[^/]+/status/[0-9]+$")

    def test_quote_chain_is_12_unique_posts_not_comments(self):
        ids = self.review["quote_chain_post_ids"]
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)
        self.assertEqual(ids[0], "2113979571884429494")
        self.assertTrue(self.review["quote_chain_complete"])
        self.assertEqual({r["source_url"].split("/")[-1] for r in self.rows[:12]}, set(ids))

    def test_comment_scope_is_honest(self):
        comments = self.review["comments"]
        self.assertEqual(len(comments), 7)
        self.assertEqual(sum(c["relationship"] == "direct reply" for c in comments), 3)
        self.assertIn("Not an exhaustive reply census", self.review["comment_coverage"])
        self.assertIn("No concrete extra backlink method", self.review["comment_coverage"])

    def test_fern_sample_does_not_overstate_follow_or_indexing(self):
        fern = self.rows[0]
        self.assertEqual(fern["research_status"], "PUBLIC_SAMPLE_LINK_OBSERVED")
        self.assertEqual(fern["observed_href"], "https://resend.com/docs")
        self.assertEqual(fern["observed_rel"], "noopener noreferrer")
        self.assertIn("actual indexing NOT_MEASURED", fern["index_observation"])
        self.assertIn("Request listing", fern["next_check"])
        self.assertIn("not Google indexing requirements or a ranking factor", self.doc)

    def test_postman_sample_distinguishes_link_slots(self):
        row = self.rows[1]
        self.assertEqual(row["research_status"], "PUBLIC_SAMPLE_LINK_OBSERVED")
        self.assertEqual(row["observed_example_url"], "https://www.postman.com/adaptlypost")
        self.assertEqual(row["observed_href"], "https://adaptlypost.com/")
        self.assertEqual(row["observed_rel"], "noreferrer noopener")
        self.assertIn("description links have nofollow", row["next_check"])
        self.assertIn("header and actual indexing NOT_MEASURED", row["index_observation"])
        observation = self.review["first_party_observations"][-1]
        self.assertEqual(observation["links"][0]["rel"], "noreferrer noopener")
        self.assertIn("nofollow", observation["links"][1]["rel"])

    def test_unknown_links_are_not_synthetic_success(self):
        self.assertTrue(all(not r["observed_href"] and not r["observed_rel"] for r in self.rows[2:]))
        self.assertTrue(all(r["index_observation"] == "NOT_MEASURED" for r in self.rows[2:]))

    def test_mirror_and_registry_counts_are_not_backlinks(self):
        self.assertIn("not four guaranteed backlinks", self.rows[3]["next_check"])
        self.assertIn("not HTML backlink evidence", self.rows[8]["next_check"])
        self.assertIn("noindex", self.rows[9]["next_check"])
        self.assertIn("not an indexable backlink result", self.doc)

    def test_paid_and_widget_routes_have_hard_guards(self):
        self.assertEqual(self.rows[24]["research_status"], "PAID_PUBLICITY_ONLY")
        self.assertIn("sponsored/nofollow", self.rows[24]["next_check"])
        self.assertIn("appropriately qualified", self.rows[23]["next_check"])
        self.assertIn("never buy ranking credit", self.doc)
        self.assertIn("host page separately from the iframe", self.doc)

    def test_existing_routes_are_reused_not_repromoted(self):
        self.assertIn("already occurs", self.rows[2]["reuse_route"])
        self.assertIn("201", self.rows[25]["next_check"])
        self.assertIn("not advertised 11464", self.rows[25]["next_check"])
        self.assertIn("do not bulk-endorse", self.rows[25]["next_check"])
        self.assertIn("do not create a second account", self.rows[1]["reuse_route"])

    def test_workflow_and_readme_route_to_existing_playbook(self):
        workflow = (ROOT / "workflows/authority-and-links.md").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertIn("Source-led product/resource methods", workflow)
        self.assertIn("backlink-method-research.csv", workflow)
        self.assertIn("not an approved submission queue", workflow)
        self.assertIn("backlink-method-source-review-20261024.json", readme)
        for link in re.findall(r"\]\(([^)]+)\)", self.doc.split("## Source-led product", 1)[1]):
            if not link.startswith(("https://", "http://", "#")):
                target = (ROOT / "references/playbooks/authority" / link.split("#")[0]).resolve()
                self.assertTrue(target.exists(), link)

    def test_no_executed_external_action_or_installed_skill_claim(self):
        excluded = self.review["actions_not_performed"]
        for phrase in ["Account creation", "DNS changes", "Purchase", "Installed-skill change"]:
            self.assertIn(phrase, excluded)
        self.assertIn("No package\nwas run", self.doc)
        self.assertIn("draft-and-hold", self.doc)


if __name__ == "__main__":
    unittest.main()
