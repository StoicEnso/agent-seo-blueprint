#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
playbook = (ROOT / "references" / "playbooks" / "authority" / "editorial-link-intent-and-assets.md").read_text(encoding="utf-8").lower()
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
asset = (ROOT / "assets" / "editorial-link-opportunity.json").read_text(encoding="utf-8")

for phrase in [
    "credit-based or networked",
    'rel="sponsored"',
    "provider citation observations are a targeting hint only",
    "decayed_resource",
    "statistics_or_research_need",
    "missing_visual",
    "article_video_asset",
    "unlinked_owned_asset",
    "never send without explicit per-batch approval",
    "temporal sequence is not causation",
]:
    assert phrase in playbook, phrase

for phrase in ["editorial-link-intent-and-assets", "credit-based reciprocal-link networks", "sponsored"]:
    assert phrase in skill, phrase

for field in [
    '"intent_class"', '"observed_gap"', '"evidence"', '"rights_and_attribution"',
    '"replacement_fit"', '"required_rel"', '"hard_fails"', '"status"'
]:
    assert field in asset, field

print("editorial-link-intent docs: PASS")
