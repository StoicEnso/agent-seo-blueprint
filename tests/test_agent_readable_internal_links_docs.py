import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "references" / "playbooks" / "maintenance" / "agent-readable-web-delivery.md"
INTERNAL = ROOT / "references" / "playbooks" / "maintenance" / "contextual-internal-link-architecture.md"
LINKS = ROOT / "references" / "playbooks" / "authority" / "link-stealing.md"
GEO = ROOT / "workflows" / "geo-audit.md"
TECH = ROOT / "workflows" / "technical-seo-maintenance.md"
SITE = ROOT / "workflows" / "site-audit.md"
MONITORING = ROOT / "workflows" / "monitoring.md"
AUTHORITY = ROOT / "workflows" / "authority-and-links.md"
SKILL = ROOT / "SKILL.md"


class AgentReadableInternalLinksDocsTest(unittest.TestCase):
    def test_agent_delivery_keeps_evidence_lanes_and_roles_separate(self):
        text = AGENT.read_text(encoding="utf-8").lower()
        for phrase in (
            "configuration evidence",
            "request evidence",
            "provider-role evidence",
            "answer/citation evidence",
            "business evidence",
            "search | training | user_triggered",
            "does not by itself prove successful parsing, indexing, training",
        ):
            self.assertIn(phrase, text)

    def test_llms_markdown_and_negotiation_are_optional_and_safe(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in (AGENT, GEO, TECH, SKILL)
        )
        for phrase in (
            "informal proposal",
            "absence of `llms.txt` is not a google defect",
            "html remains a first-class web representation",
            "vary: accept",
            "avoid user-agent sniffing",
            "not a ranking or citation gain",
        ):
            self.assertIn(phrase, combined)

    def test_log_evidence_rejects_spoofed_identity_and_sensitive_data(self):
        text = AGENT.read_text(encoding="utf-8").lower()
        for phrase in (
            "a user-agent string can be spoofed",
            "verified_provider_range | user_agent_only | not_verified",
            "strip secrets, cookies, authorization headers, request bodies",
            "sensitive query-string values",
            "do not fingerprint users or reconstruct prompts",
        ):
            self.assertIn(phrase, text)

    def test_internal_link_audit_does_not_turn_four_links_into_formula(self):
        text = INTERNAL.read_text(encoding="utf-8").lower()
        for phrase in (
            "does not prove that adding a fourth link caused ranking",
            "do not classify a link as contextual from destination frequency alone",
            "crawl-observed orphan is not automatically a true orphan",
            "natural variation should follow context",
            "`four contextual links` only as a review trigger",
            "do not promise a ranking-position gain",
        ):
            self.assertIn(phrase, text)

    def test_internal_link_playbook_is_wired_into_audits(self):
        for path in (TECH, SITE):
            text = path.read_text(encoding="utf-8")
            self.assertIn("contextual-internal-link-architecture.md", text, str(path))
            self.assertIn("internal-link-architecture.json", text, str(path))

    def test_listicle_outreach_is_selective_and_approval_gated(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in (LINKS, AUTHORITY)
        )
        for phrase in (
            "real editorial omission",
            "follow up once",
            "do not repeat the source's “12 backlinks”",
            "add-alongside",
            "never auto-send",
            "appropriately qualified",
        ):
            self.assertIn(phrase, combined)

    def test_monitoring_preserves_request_and_internal_link_limits(self):
        text = MONITORING.read_text(encoding="utf-8").lower()
        self.assertIn("agent-request-evidence.json", text)
        self.assertIn("internal-link-architecture.json", text)
        self.assertIn("does not prove parsing, indexing, training, citation", text)
        self.assertIn("do not treat a field-study threshold as a ranking formula", text)


if __name__ == "__main__":
    unittest.main()
