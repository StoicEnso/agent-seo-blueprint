import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "workflows" / "geo-audit.md"
OFFICIAL = ROOT / "references" / "playbooks" / "foundations" / "google-generative-ai-search-official.md"
FOUNDATION = ROOT / "references" / "playbooks" / "foundations" / "seo-and-ai-future.md"
FIXTURE = ROOT / "tests" / "fixtures" / "geo-google-findings.json"


def load_report_module():
    spec = importlib.util.spec_from_file_location("agent_seo_report", ROOT / "scripts" / "report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GoogleGeoGuardrailsTest(unittest.TestCase):
    def test_official_reference_is_wired_into_workflow(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("google-generative-ai-search-official.md", workflow)
        self.assertIn("google_ai_overviews", workflow)
        self.assertIn("google_ai_mode", workflow)
        self.assertIn("Generative AI performance report", workflow)
        self.assertIn("Google myth-busting guardrails", workflow)
        self.assertIn("Do not generalize that source to other providers", workflow)
        self.assertIn("the report is impression-only", workflow)
        self.assertIn("Do not invent AI clicks, queries, CTR, conversions", workflow)

    def test_google_hacks_are_explicitly_rejected(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (WORKFLOW, OFFICIAL, FOUNDATION)
        ).lower()
        for phrase in (
            "absence of `llms.txt` is **not** a google defect",
            "tiny artificial “ai chunks” are not required",
            "there is no special ai schema",
            "manufactured or inauthentic mentions are never recommended",
        ):
            self.assertIn(phrase, combined)
        self.assertNotIn("optional `/llms.txt` guidance", combined)
        self.assertIn("scope: google ai overviews and ai mode only", combined)
        self.assertIn("do not generalize it to chatgpt, perplexity, claude", combined)

    def test_geo_context_renders_without_breaking_findings(self):
        report = load_report_module()
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            output = report.render_audit(tmp, "GEO audit: example.com", data)
            rendered = output.read_text(encoding="utf-8")
        self.assertIn("**Readiness verdict:** moderate", rendered)
        self.assertIn("## Google eligibility", rendered)
        self.assertIn("## Google myth checks", rendered)
        self.assertIn("## Google AI performance", rendered)
        self.assertIn("google_ai_overviews", rendered)
        self.assertIn("The page has useful claims", rendered)

    def test_generic_audit_shape_remains_supported(self):
        report = load_report_module()
        data = {
            "summary": "Generic audit fixture.",
            "findings": [
                {"severity": "high", "area": "technical", "issue": "A | B", "fix": "Fix | it"}
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = report.render_audit(tmp, "Site audit: example.com", data)
            rendered = output.read_text(encoding="utf-8")
        self.assertIn("Generic audit fixture.", rendered)
        self.assertIn("A / B", rendered)
        self.assertIn("Fix / it", rendered)
        self.assertNotIn("## Google eligibility", rendered)


if __name__ == "__main__":
    unittest.main()
