"""Offline correctness and rejection tests; no credentials, models or network."""
import copy
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import change_review as change
import review_inputs as inputs
import sitemap_snapshot as sitemap


class InputTests(unittest.TestCase):
    def test_public_url_accepts_domain_and_standard_port(self):
        self.assertEqual(inputs.public_url("https://example.test:443/a?x=1"), "example.test")

    def test_public_url_rejects_local_ip_credentials_ports_and_controls(self):
        values = ["file:///etc/passwd", "ftp://example.test/a", "http://localhost/a",
                  "http://127.0.0.1/a", "http://127.1/a", "http://[::1]/a",
                  "https://x.internal/a", "https://x.local/a", "https://x.localhost/a",
                  "https://user:pass@example.test/a", "https://example.test:8443/a",
                  "https://example.test/a#fragment", "https://example.test/\na",
                  "https://example.test/a b", "https://example.test\\a", "https://example.test./a"]
        for value in values:
            with self.subTest(value=value), self.assertRaises(ValueError):
                inputs.public_url(value)

    def test_timestamps_require_valid_timezone_aware_iso(self):
        self.assertIsNotNone(inputs.timestamp("2026-10-14T09:00:00+01:00").utcoffset())
        for value in ["2026-10-14", "2026-10-14T09:00:00", "2026-19-99T09:00:00Z", True]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                inputs.timestamp(value)

    def test_lastmod_accepts_date_or_aware_timestamp(self):
        self.assertEqual(inputs.lastmod("2026-10-14"), "2026-10-14")
        self.assertEqual(inputs.lastmod("2026-10-14T09:00:00Z"), "2026-10-14T09:00:00Z")
        for value in ["2026-02-30", "2026-10-14T09:00:00", None, 3]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                inputs.lastmod(value)

    def test_bounded_read_rejects_excess_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input"
            path.write_bytes(b"1234")
            with self.assertRaises(ValueError):
                inputs.bounded_bytes(path, 3)

    def test_json_rejects_duplicates_nonfinite_and_corrupt_input(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            for raw in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{']:
                path.write_text(raw)
                with self.subTest(raw=raw), self.assertRaises(ValueError):
                    inputs.load_json(path)

    def test_writer_does_not_overwrite_input_or_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            path.write_text("preserve")
            with self.assertRaises(ValueError):
                inputs.write_json(path, {}, inputs=(path,))
            link = Path(folder) / "link.json"
            link.symlink_to(path)
            with self.assertRaises(ValueError):
                inputs.write_json(link, {})
            self.assertEqual(path.read_text(), "preserve")

    def test_writer_replaces_only_nominated_output(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "out.json"
            path.write_text("old")
            inputs.write_json(path, {"candidate_only": True})
            self.assertEqual(json.loads(path.read_text()), {"candidate_only": True})
            self.assertEqual([p.name for p in Path(folder).iterdir()], ["out.json"])


class GitReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.repo = self.folder / "repo"
        self.repo.mkdir()
        self.git("init", "--quiet")
        self.git("config", "user.name", "Offline test")
        self.git("config", "user.email", "offline@example.invalid")
        for name, raw in {"src/limits.py": b"limit = 1\n", "docs/delete.md": b"existing\n",
                          "docs/old.md": b"rename this document\n", "image.bin": b"\x00old",
                          "nested/_source/course.txt": b"private fixture",
                          "nested/private/secret.txt": b"secret fixture"}.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "baseline")
        self.base = self.git("rev-parse", "HEAD").strip()
        (self.repo / "src/limits.py").write_text("limit = 2\n")
        (self.repo / "docs/delete.md").unlink()
        self.git("mv", "docs/old.md", "docs/new.md")
        (self.repo / "image.bin").write_bytes(b"\x00new")
        (self.repo / "nested/_source/course.txt").write_text("hidden fixture updated")
        (self.repo / "nested/private/secret.txt").write_text("do not expose this fixture")
        self.git("add", "-A")
        self.git("commit", "--quiet", "-m", "change")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.map_path = self.folder / "map.json"
        self.ledger = {"schema_version": 1, "site_url": "https://product.test", "mappings": [
            {"claim_id": "plan-limit", "source_paths": ["src/limits.py"], "owned_page": "/pricing", "claim": "Verify live plan limit."},
            {"claim_id": "help-page", "source_paths": ["docs/old.md", "docs/new.md", "docs/delete.md"], "owned_page": "/help", "claim": "Review documentation references."}]}
        self.write_map()

    def git(self, *arguments):
        return subprocess.check_output(["git", "-C", str(self.repo), *arguments], stderr=subprocess.DEVNULL, text=True)

    def write_map(self):
        self.map_path.write_text(json.dumps(self.ledger))

    def review(self, **changes):
        arguments = dict(repository=self.repo, base_ref=self.base, head_ref=self.head, map_path=self.map_path)
        arguments.update(changes)
        return change.review(**arguments)

    def test_pins_commits_and_map_fingerprint(self):
        result = self.review(head_ref="HEAD")
        self.assertEqual(result["base_commit"], self.base)
        self.assertEqual(result["head_commit"], self.head)
        self.assertEqual(result["mapping_sha256"], inputs.digest(self.map_path.read_bytes()))
        self.assertTrue(result["candidate_only"])

    def test_maps_exact_source_to_owned_claim(self):
        row = next(r for r in self.review()["changed"] if r["source_paths"] == ["src/limits.py"])
        self.assertEqual(row["disposition"], "review_product_copy")
        self.assertEqual(row["mapped_claims"][0]["claim_id"], "plan-limit")

    def test_retains_both_rename_paths(self):
        row = next(r for r in self.review()["changed"] if r["status"].startswith("R"))
        self.assertEqual(row["source_paths"], ["docs/old.md", "docs/new.md"])

    def test_retains_real_baseline_deletion(self):
        row = next(r for r in self.review()["changed"] if r["source_paths"] == ["docs/delete.md"])
        self.assertEqual(row["status"], "D")

    def test_binary_changes_are_metadata_only_and_unmapped(self):
        row = next(r for r in self.review()["changed"] if r["source_paths"] == ["image.bin"])
        self.assertTrue(row["binary_metadata_only"])
        self.assertEqual(row["disposition"], "needs_mapping")

    def test_nested_private_paths_and_contents_are_not_exposed(self):
        result = self.review()
        self.assertEqual(result["excluded_path_count"], 2)
        encoded = json.dumps(result)
        self.assertNotIn("nested/_source", encoded)
        self.assertNotIn("do not expose", encoded)
        self.assertNotIn("limit = 2", encoded)

    def test_unchanged_commit_is_empty_and_worktree_edits_are_ignored(self):
        (self.repo / "src/limits.py").write_text("uncommitted change")
        self.assertEqual(self.review(base_ref=self.head)["changed"], [])
        self.assertNotIn("uncommitted", json.dumps(self.review()))

    def test_bad_and_option_like_revisions_are_rejected(self):
        for revision in ["missing-ref", "--help", "HEAD;echo", "HEAD\n", "HEAD:src/limits.py"]:
            with self.subTest(revision=revision), self.assertRaises(ValueError):
                self.review(base_ref=revision)

    def test_reversed_nonancestor_comparison_is_rejected(self):
        with self.assertRaises(ValueError):
            self.review(base_ref=self.head, head_ref=self.base)

    def test_wrong_repository_or_subdirectory_is_rejected(self):
        for path in [self.folder, self.repo / "src"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.review(repository=path)

    def test_changed_path_cap_counts_even_excluded_paths(self):
        with self.assertRaisesRegex(ValueError, "path cap"):
            self.review(cap=1)
        for cap in [0, 1001]:
            with self.subTest(cap=cap), self.assertRaises(ValueError):
                self.review(cap=cap)

    def test_invalid_mapping_version_rows_claims_and_hosts_are_rejected(self):
        variants = [[], {"schema_version": True, "site_url": "https://product.test", "mappings": []},
                    {**self.ledger, "mappings": "not a list"}]
        for key, value in [("source_paths", ["../secret"]), ("source_paths", ["nested/_source/course.txt"]),
                           ("source_paths", "src/limits.py"), ("source_paths", ["src/limits.py", "src/limits.py"]),
                           ("owned_page", "https://other.test/page"), ("claim", 3), ("claim_id", "bad id")]:
            variant = copy.deepcopy(self.ledger)
            variant["mappings"][0][key] = value
            variants.append(variant)
        for variant in variants:
            self.map_path.write_text(json.dumps(variant))
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                self.review()

    def test_duplicate_claim_id_is_rejected(self):
        self.ledger["mappings"].append(copy.deepcopy(self.ledger["mappings"][0]))
        self.write_map()
        with self.assertRaises(ValueError):
            self.review()

    def test_external_diff_is_disabled(self):
        self.git("config", "diff.external", "false")
        self.assertTrue(self.review()["candidate_only"])

    def test_git_reads_are_timed_and_output_capped(self):
        with mock.patch.object(change, "GIT_TIMEOUT", 0), self.assertRaisesRegex(ValueError, "timed out"):
            self.review()
        with mock.patch.object(change, "GIT_OUTPUT_LIMIT", 1), self.assertRaisesRegex(ValueError, "output limit"):
            self.review()

    def test_cli_error_preserves_previous_report(self):
        output = self.folder / "out.json"
        output.write_text("previous report")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/change_review.py"), "--repo", str(self.repo),
                                 "--base", "bad-ref", "--head", self.head, "--map", str(self.map_path),
                                 "--output", str(output)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(output.read_text(), "previous report")

    def test_cli_success_writes_candidate_report(self):
        output = self.folder / "out.json"
        result = subprocess.run([sys.executable, str(ROOT / "scripts/change_review.py"), "--repo", str(self.repo),
                                 "--base", self.base, "--head", self.head, "--map", str(self.map_path),
                                 "--output", str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(output.read_text())["candidate_only"])


class SitemapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.path = self.folder / "source.xml"
        self.source = "https://competitor.test/sitemap.xml"
        self.first = "2026-10-13T09:00:00+01:00"
        self.second = "2026-10-14T09:00:00+01:00"

    def make(self, body='<url><loc>https://competitor.test/a</loc></url>', observed=None, **kwargs):
        self.path.write_text('<urlset xmlns="' + sitemap.NAMESPACE + '">' + body + '</urlset>')
        return sitemap.snapshot(self.path, self.source, observed or self.first, **kwargs)

    def test_snapshot_records_hash_namespace_and_complete_state(self):
        result = self.make()
        self.assertEqual(result["xml_sha256"], inputs.digest(self.path.read_bytes()))
        self.assertEqual(result["capture_status"], "complete_urlset")
        self.assertTrue(result["complete"])

    def test_empty_urlset_is_valid_but_not_a_missing_capture(self):
        self.assertEqual(self.make("")["urls"], [])
        with self.assertRaises(OSError):
            sitemap.snapshot(self.folder / "missing.xml", self.source, self.first)

    def test_unsafe_source_rejected_even_for_index(self):
        self.path.write_text("<sitemapindex/>")
        for source in ["ftp://competitor.test/sitemap.xml", "https://localhost/sitemap.xml", "https://u:p@competitor.test/sitemap.xml"]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                sitemap.snapshot(self.path, source, self.first)

    def test_xml_rejects_malformed_html_wrong_namespace_and_missing_loc(self):
        for raw in ["<urlset>", "<html/>", '<urlset xmlns="urn:wrong"/>', "<urlset><error/></urlset>", "<urlset><url/></urlset>"]:
            self.path.write_text(raw)
            with self.subTest(raw=raw), self.assertRaises((ValueError, sitemap.ET.ParseError)):
                sitemap.snapshot(self.path, self.source, self.first)

    def test_xml_rejects_dtd_entities_and_utf16_utf32(self):
        raw = '<!DOCTYPE urlset [<!ENTITY x "expanded">]><urlset/>'
        for encoding in ["utf-8", "utf-16", "utf-32"]:
            self.path.write_bytes(raw.encode(encoding))
            with self.subTest(encoding=encoding), self.assertRaises((ValueError, UnicodeError)):
                sitemap.snapshot(self.path, self.source, self.first)

    def test_xml_rejects_unsupported_declared_encoding(self):
        self.path.write_text('<?xml version="1.0" encoding="ISO-8859-1"?><urlset/>')
        with self.assertRaises(ValueError):
            sitemap.snapshot(self.path, self.source, self.first)

    def test_xml_rejects_cross_host_duplicate_and_nested_fields(self):
        bodies = ['<url><loc>https://other.test/a</loc></url>',
                  '<url><loc>https://competitor.test/a</loc><loc>https://competitor.test/b</loc></url>',
                  '<url><loc><nested>https://competitor.test/a</nested></loc></url>',
                  '<url><loc>https://competitor.test/a</loc></url>' * 2]
        for body in bodies:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.make(body)

    def test_missing_lastmod_is_allowed_invalid_lastmod_is_rejected(self):
        self.assertNotIn("lastmod", self.make()["urls"][0])
        with self.assertRaises(ValueError):
            self.make('<url><loc>https://competitor.test/a</loc><lastmod>yesterday</lastmod></url>')

    def test_image_extension_is_not_mistaken_for_page_url(self):
        result = self.make('<url xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><loc>https://competitor.test/a</loc><image:image><image:loc>https://cdn.other.test/image.jpg</image:loc></image:image></url>')
        self.assertEqual(result["urls"], [{"url": "https://competitor.test/a"}])

    def test_xml_byte_and_row_caps(self):
        self.path.write_bytes(b"x" * (inputs.MAX_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "byte limit"):
            sitemap.snapshot(self.path, self.source, self.first)
        with mock.patch.object(sitemap, "MAX_ROWS", 1), self.assertRaisesRegex(ValueError, "row cap"):
            self.make('<url><loc>https://competitor.test/a</loc></url><url><loc>https://competitor.test/b</loc></url>')

    def test_index_records_children_and_suppresses_coverage(self):
        baseline = self.make()
        self.path.write_text('<sitemapindex><sitemap><loc>https://competitor.test/child.xml</loc></sitemap></sitemapindex>')
        current = sitemap.snapshot(self.path, self.source, self.second)
        self.assertEqual(current["index_children"], ["https://competitor.test/child.xml"])
        result = sitemap.comparison(baseline, current)
        self.assertEqual(result["comparison"], "suppressed")
        self.assertNotIn("no_longer_listed", result)

    def test_partial_current_or_baseline_suppresses_all_diffs(self):
        baseline = self.make(incomplete=True)
        current = self.make("", observed=self.second)
        self.assertEqual(sitemap.comparison(baseline, current)["comparison"], "suppressed")
        baseline = self.make()
        current = self.make("", observed=self.second, incomplete=True)
        self.assertNotIn("no_longer_listed", sitemap.comparison(baseline, current))

    def test_missing_baseline_is_not_all_new_pages(self):
        result = sitemap.comparison(None, self.make())
        self.assertEqual(result["reason"], "baseline_unavailable")
        self.assertNotIn("newly_listed", result)

    def test_comparison_preserves_query_and_trailing_slash_distinctions(self):
        baseline = self.make()
        body = ''.join('<url><loc>' + url + '</loc></url>' for url in
                       ['https://competitor.test/a', 'https://competitor.test/a/', 'https://competitor.test/a?x=1'])
        current = self.make(body, observed=self.second)
        result = sitemap.comparison(baseline, current)
        self.assertEqual(result["newly_listed"], ['https://competitor.test/a/', 'https://competitor.test/a?x=1'])
        self.assertEqual(result["no_longer_listed"], [])

    def test_lastmod_only_change_and_missing_metadata_are_explicit(self):
        baseline = self.make('<url><loc>https://competitor.test/a</loc><lastmod>2026-10-13</lastmod></url>')
        current = self.make(observed=self.second)
        result = sitemap.comparison(baseline, current)
        self.assertEqual(result["lastmod_changed"], ['https://competitor.test/a'])
        self.assertTrue(result["lastmod_changes"][0]["metadata_only"])
        self.assertIsNone(result["lastmod_changes"][0]["after"])

    def test_removal_is_listing_only(self):
        result = sitemap.comparison(self.make(), self.make("", observed=self.second))
        self.assertEqual(result["no_longer_listed"], ['https://competitor.test/a'])
        self.assertIn("not proof", " ".join(result["limitations"]))

    def test_unchanged_snapshots_have_empty_diffs(self):
        result = sitemap.comparison(self.make(), self.make(observed=self.second))
        self.assertEqual(result["newly_listed"], [])
        self.assertEqual(result["no_longer_listed"], [])
        self.assertEqual(result["lastmod_changed"], [])

    def test_source_swap_reversed_equal_and_naive_times_rejected(self):
        baseline = self.make()
        for source, observed in [("https://competitor.test/other.xml", self.second),
                                 (self.source, self.first), (self.source, "2026-10-12T09:00:00+01:00"),
                                 (self.source, "2026-10-14T09:00:00")]:
            current = copy.deepcopy(baseline)
            current.update(source_sitemap=source, observation_time=observed)
            with self.subTest(source=source, observed=observed), self.assertRaises(ValueError):
                sitemap.comparison(baseline, current)

    def test_corrupt_snapshot_schema_is_rejected_not_trusted(self):
        baseline = self.make()
        mutations = [("schema_version", True), ("complete", "false"), ("urls", {}),
                     ("xml_sha256", "bad"), ("capture_status", "invented"), ("limitations", []),
                     ("urls", [{"url": "https://other.test/a"}]),
                     ("urls", [{"url": "https://competitor.test/a"}] * 2),
                     ("urls", [{"url": "https://competitor.test/a", "lastmod": 3}])]
        for key, value in mutations:
            current = copy.deepcopy(baseline)
            current.update(observation_time=self.second)
            current[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                sitemap.comparison(baseline, current)

    def test_network_is_never_used(self):
        with mock.patch.object(socket, "create_connection", side_effect=AssertionError("network used")):
            sitemap.comparison(self.make(), self.make(observed=self.second))

    def test_cli_snapshots_and_missing_baseline_report(self):
        self.make()
        current = self.folder / "current.json"
        output = self.folder / "comparison.json"
        result = subprocess.run([sys.executable, str(ROOT / "scripts/sitemap_snapshot.py"), "snapshot", "--input", str(self.path),
                                 "--source", self.source, "--observed", self.first, "--output", str(current)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/sitemap_snapshot.py"), "compare", "--baseline", str(self.folder / "missing.json"),
                                 "--current", str(current), "--output", str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(output.read_text())["reason"], "baseline_unavailable")

    def test_cli_corrupt_input_preserves_existing_output(self):
        baseline = self.folder / "baseline.json"
        current = self.folder / "current.json"
        output = self.folder / "output.json"
        baseline.write_text(json.dumps(self.make()))
        current.write_text('{"complete":"false"}')
        output.write_text("previous report")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/sitemap_snapshot.py"), "compare", "--baseline", str(baseline),
                                 "--current", str(current), "--output", str(output)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(output.read_text(), "previous report")


class DocumentationTests(unittest.TestCase):
    def test_router_and_existing_workflows_discover_new_runbook(self):
        self.assertIn("workflows/change-and-sitemap-review.md", (ROOT / "SKILL.md").read_text())
        for name in ["monitoring", "technical-seo-maintenance", "content-production"]:
            self.assertIn("change-and-sitemap-review.md", (ROOT / "workflows" / (name + ".md")).read_text())
        self.assertIn("**change-and-sitemap-review**", (ROOT / "README.md").read_text())

    def test_all_new_markdown_links_exist(self):
        paths = [ROOT / "workflows/change-and-sitemap-review.md", ROOT / "references/playbooks/maintenance/change-and-sitemap-review.md"]
        for path in paths:
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if target.startswith(("https://", "http://", "#")):
                    continue
                with self.subTest(path=path, target=target):
                    self.assertTrue((path.parent / target).resolve().is_file())

    def test_schema_is_real_and_template_map_is_valid(self):
        schema = json.loads((ROOT / "assets/competitor-sitemap-snapshot.schema.json").read_text())
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("xml_sha256", schema["required"])
        self.assertEqual(schema["properties"]["complete"]["type"], "boolean")
        value, _ = change.mapping(ROOT / "assets/source-to-page-map.json")
        self.assertEqual(value["site_url"], "https://example.invalid")

    def test_runbook_has_commands_completion_and_existing_gates(self):
        value = (ROOT / "workflows/change-and-sitemap-review.md").read_text()
        for phrase in ["scripts/change_review.py", "scripts/sitemap_snapshot.py snapshot", "scripts/sitemap_snapshot.py compare",
                       "## Done when", "28/56-day", "approval", "cannibalization", "rollback/live receipt", "--incomplete"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, value)


if __name__ == "__main__":
    unittest.main()
