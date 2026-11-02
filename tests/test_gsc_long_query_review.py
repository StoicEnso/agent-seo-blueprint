import copy
from datetime import date
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("long_query", ROOT / "scripts/gsc_long_query_review.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
TODAY = date(2026, 11, 2)


class LongQueryTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "assets/gsc-long-query-export.example.json").read_text())

    def run_review(self):
        return MOD.review(self.data, TODAY)

    def test_boundary_seven_eight_nine(self):
        for n, expected in [(7, False), (8, True), (9, True), (30, True)]:
            with self.subTest(n=n):
                self.assertEqual(bool(MOD.LONG_QUERY.fullmatch(" ".join(["word"] * n))), expected)

    def test_multiple_spaces_tabs_and_punctuation(self):
        self.assertTrue(MOD.LONG_QUERY.fullmatch("one  two\tthree four five six seven eight?"))

    def test_whitespace_not_silently_trimmed(self):
        q = "one two three four five six seven eight"
        for q2 in [" " + q, q + " ", q + "\n"]:
            self.assertIsNone(MOD.LONG_QUERY.fullmatch(q2))
        self.assertIsNone(MOD.LONG_QUERY.fullmatch("花园设计需要多少钱应该如何规划"))

    def test_re2_whitespace_semantics_not_python_unicode_split(self):
        for separator in ["\u00a0", "\v", "\u2003"]:
            q = "one" + separator + "two three four five six seven eight"
            self.assertIsNone(MOD.LONG_QUERY.fullmatch(q))
            self.assertEqual(len(MOD.TOKENS.findall(q)), 7)
        self.assertTrue(MOD.LONG_QUERY.fullmatch("one\ftwo three four five six seven eight"))

    def test_raw_rows_manifest_and_input_preserved(self):
        original = copy.deepcopy(self.data)
        result = self.run_review()
        self.assertEqual(self.data, original)
        self.assertEqual(result["metadata"], original["metadata"])
        self.assertEqual(result["matched_rows"], 2)
        self.assertEqual(result["nonmatching_rows"], 1)
        self.assertEqual(result["window_days"], 28)
        self.assertEqual(result["candidates"][0]["query"], self.data["rows"][0]["query"])
        self.assertTrue(all(r["status"] == "NEEDS_PAGE_REVIEW" for r in result["candidates"]))

    def test_low_ctr_is_tie_break_not_forecast(self):
        self.data["rows"][1]["impressions"] = 200
        self.assertEqual(self.run_review()["candidates"][0]["clicks"], 0)
        self.assertIn("not a forecast", " ".join(self.run_review()["limitations"]))

    def test_no_rank_4_20_cutoff(self):
        self.assertIn(23.0, [r["position"] for r in self.run_review()["candidates"]])

    def test_native_api_dimension_order(self):
        self.data["metadata"]["dimensions"] = ["page", "query"]
        for row in self.data["rows"]:
            row["keys"] = [row.pop("page"), row.pop("query")]
        self.assertEqual(self.run_review()["matched_rows"], 2)

    def test_conflicting_keys_rejected(self):
        self.data["rows"][0]["keys"] = ["another query", "https://example.com/"]
        with self.assertRaises(ValueError): self.run_review()

    def test_query_only_and_disconnected_tables_rejected(self):
        for dims in [["query"], ["query", "page", "date"], ["query", "page", "query"]]:
            with self.subTest(dims=dims):
                self.data["metadata"]["dimensions"] = dims
                with self.assertRaises(ValueError): self.run_review()

    def test_missing_page_rejected(self):
        del self.data["rows"][0]["page"]
        with self.assertRaises(ValueError): self.run_review()

    def test_duplicates_rejected_not_summed(self):
        self.data["rows"].append(copy.deepcopy(self.data["rows"][0]))
        with self.assertRaises(ValueError): self.run_review()

    def test_multiple_pages_preserved(self):
        row = copy.deepcopy(self.data["rows"][0])
        row["page"] = "https://example.com/another"
        self.data["rows"].append(row)
        self.assertEqual(self.run_review()["matched_rows"], 3)

    def test_segment_dimensions_preserved(self):
        self.data["metadata"]["dimensions"] += ["country", "device"]
        for row in self.data["rows"]: row.update(country="gbr", device="mobile")
        row = copy.deepcopy(self.data["rows"][0])
        row["device"] = "desktop"
        self.data["rows"].append(row)
        self.assertEqual(self.run_review()["matched_rows"], 3)

    def test_property_membership(self):
        for prop, page, expected in [
            ("sc-domain:example.com", "https://sub.example.com/path", True),
            ("sc-domain:example.com", "https://notexample.com/", False),
            ("sc-domain:example.com", "https://example.com.evil.test/", False),
            ("https://example.com/blog/", "https://example.com/blog/post", True),
            ("https://example.com/blog/", "https://example.com/blogger/post", False),
            ("https://example.com/", "http://example.com/", False),
            ("https://example.com/", "https://example.com:8443/", False),
            ("sc-domain:example.com", "https://secret@example.com/", False),
            ("sc-domain:example.com", "https://example.com/#fragment", False),
            ("sc-domain:", "https://example.com/", False),
        ]:
            with self.subTest(prop=prop, page=page):
                self.assertEqual(MOD.page_in_property(page, prop), expected)

    def test_out_of_property_rejected(self):
        self.data["rows"][0]["page"] = "https://other.test/"
        with self.assertRaises(ValueError): self.run_review()

    def test_numeric_validation(self):
        for key, value in [("clicks", -1), ("clicks", True), ("clicks", 1.5),
                           ("clicks", 201), ("impressions", 0), ("position", float("nan")),
                           ("position", float("inf")), ("position", 0), ("ctr", 2), ("ctr", 0.5)]:
            with self.subTest(key=key, value=value):
                bad = copy.deepcopy(self.data)
                bad["rows"][0][key] = value
                with self.assertRaises(ValueError): MOD.review(bad, TODAY)

    def test_ctr_derived_when_absent(self):
        del self.data["rows"][0]["ctr"]
        self.assertEqual(self.run_review()["candidates"][0]["ctr"], 0.01)

    def test_empty_and_no_matches_not_zero_demand(self):
        self.data["rows"] = []
        result = self.run_review()
        self.assertEqual(result["status"], "NO_MATCHES")
        self.assertIn("omitted", " ".join(result["limitations"]))

    def test_partial_and_stale_exports(self):
        self.data["metadata"]["extraction_complete"] = False
        self.assertEqual(self.run_review()["status"], "PARTIAL_EXPORT")
        result = MOD.review(self.data, date(2026, 11, 15))
        self.assertEqual(result["status"], "STALE_DATA")
        self.assertEqual(result["candidates"][0]["status"], "STALE_DATA")

    def test_metadata_required_and_final(self):
        for key in ["property", "start_date", "end_date", "captured_at", "dimensions", "filters",
                    "search_type", "data_state", "extraction_complete"]:
            with self.subTest(key=key):
                bad = copy.deepcopy(self.data)
                del bad["metadata"][key]
                with self.assertRaises(ValueError): MOD.review(bad, TODAY)
        self.data["metadata"]["data_state"] = "all"
        with self.assertRaises(ValueError): self.run_review()

    def test_date_validation(self):
        for key, value in [("start_date", "2026-11-01"), ("end_date", "2026-11-03"),
                           ("captured_at", "2026-11-02T12:00:00"),
                           ("captured_at", "2026-11-03T12:00:00Z")]:
            with self.subTest(key=key):
                bad = copy.deepcopy(self.data)
                bad["metadata"][key] = value
                with self.assertRaises(ValueError): MOD.review(bad, TODAY)

    def test_invalid_age_and_invalid_empty_property(self):
        with self.assertRaises(ValueError): MOD.review(self.data, TODAY, -1)
        self.data["rows"] = []
        self.data["metadata"]["property"] = "not-a-property"
        with self.assertRaises(ValueError): self.run_review()

    def test_cli_synthetic_fixture(self):
        run = subprocess.run([sys.executable, str(ROOT / "scripts/gsc_long_query_review.py"),
                              str(ROOT / "assets/gsc-long-query-export.example.json"),
                              "--as-of", "2026-11-02"], text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["matched_rows"], 2)

    def test_docs_are_wired_and_do_not_authorize_publication(self):
        for path in ["SKILL.md", "workflows/monitoring.md", "workflows/content-production.md",
                     "references/integrations/gsc.md",
                     "references/playbooks/maintenance/gsc-position-4-20-opportunity-mining.md"]:
            self.assertIn("gsc-long-query-review.md", (ROOT / path).read_text())
        text = (ROOT / "references/gsc-long-query-review.md").read_text()
        for phrase in [MOD.PATTERN, "query+page", "unverified", "anonymized", "NEEDS_PAGE_REVIEW",
                       "does **not** authorize merge", "stub", "single-writer", "+28", "+56"]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
