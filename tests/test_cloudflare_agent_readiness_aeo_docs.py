import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "references" / "playbooks" / "maintenance" / "cloudflare-agent-readiness-and-aeo.md"
GEO = ROOT / "workflows" / "geo-audit.md"
MONITORING = ROOT / "workflows" / "monitoring.md"


class CloudflareAgentAeoDocsTest(unittest.TestCase):
    def test_playbook_is_wired_into_both_workflows(self):
        for path in (GEO, MONITORING):
            text = path.read_text(encoding="utf-8")
            self.assertIn("cloudflare-agent-readiness-and-aeo.md", text)
            self.assertIn("cloudflare-agent-aeo.json", text)

    def test_three_evidence_lanes_are_kept_separate(self):
        text = PLAYBOOK.read_text(encoding="utf-8").lower()
        for phrase in (
            "agent readiness diagnostics",
            "aeo visibility synthetic category panel",
            "ai operator activity first-party network evidence",
            "not actual user-query logs",
            "not a ranking or citation formula",
        ):
            self.assertIn(phrase, text)

    def test_access_pricing_and_causality_are_guarded(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in (PLAYBOOK, GEO, MONITORING)
        )
        self.assertIn("requires requesting early access", combined)
        self.assertIn("does not establish a price", combined)
        self.assertIn("do not describe either product as free", combined)
        self.assertIn("not causality", combined)
        self.assertIn("unavailable beta access", combined)

    def test_source_and_announcement_scope_are_explicit(self):
        text = PLAYBOOK.read_text(encoding="utf-8")
        self.assertIn("https://blog.cloudflare.com/aeo/", text)
        self.assertIn("https://x.com/glenngabe/status/2085703866385928685", text)
        self.assertIn("2026-08-06", text)
        self.assertIn("Anthropic Claude and OpenAI GPT", text)


if __name__ == "__main__":
    unittest.main()
