"""Guard the on-demand outdated-resource authority subskill and its example."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OutdatedResourceDocsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playbook = (ROOT / "references/playbooks/authority/outdated-resource-replacement.md").read_text()
        cls.example = (ROOT / "examples/landscapio-outdated-resource-prospects.md").read_text()
        cls.authority = (ROOT / "workflows/authority-and-links.md").read_text()

    def test_source_claim_is_not_a_result(self):
        self.assertIn("hidden domains, baseline and attribution cannot be checked", self.playbook)
        self.assertIn("none are earned backlinks", self.playbook)

    def test_false_broken_links_do_not_become_pitches(self):
        for gate in ("403/402", "transient maintenance notice", "HOLD_RECHECK", "REJECT_NO_FIT"):
            self.assertIn(gate, self.playbook)
        self.assertIn("not broken", self.example)
        self.assertIn("not replaced by Landscapio", self.example)

    def test_five_link_instances_and_rejected_control(self):
        self.assertEqual(self.example.count("| [WPS"), 1)
        self.assertEqual(self.example.count("| [Country Living"), 1)
        self.assertEqual(self.example.count("| [MorningDough"), 1)
        self.assertEqual(self.example.count("| Same MorningDough"), 2)
        self.assertIn("Rejected control:", self.example)

    def test_no_autosend_or_site_write(self):
        self.assertIn("Do not send email", self.playbook)
        self.assertIn("NEVER sends email", self.authority)
        self.assertIn("external send needs owner approval", self.playbook)


if __name__ == "__main__":
    unittest.main()
