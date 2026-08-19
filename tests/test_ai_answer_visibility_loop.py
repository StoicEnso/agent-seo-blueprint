import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


prompt_panel = load_script("prompt_panel")
social_fetch = load_script("social_fetch")
geo_metrics = load_script("geo_metrics")
rank_social = load_script("rank_social_opportunities")
approval_queue = load_script("approval_queue")


ATOM = b'''<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example thread</title>
  <updated>2026-08-17T12:00:00+00:00</updated>
  <entry>
    <author><name>/u/original</name></author>
    <content type="html">&lt;div&gt;&lt;p&gt;Need an AI garden design app.&lt;/p&gt;&lt;p&gt;&lt;a href="https://example.com"&gt;Example&lt;/a&gt;&lt;/p&gt;&lt;/div&gt;</content>
    <link href="https://www.reddit.com/r/landscaping/comments/abc123/example/" />
    <published>2026-08-17T11:00:00+00:00</published>
    <updated>2026-08-17T11:00:00+00:00</updated>
    <title>Best AI garden design app?</title>
  </entry>
  <entry>
    <author><name>/u/replier</name></author>
    <content type="html">&lt;div&gt;&lt;p&gt;Try a photo-based tool.&lt;/p&gt;&lt;/div&gt;</content>
    <link href="https://www.reddit.com/r/landscaping/comments/abc123/example/comment1/" />
    <published>2026-08-17T11:30:00+00:00</published>
    <updated>2026-08-17T11:30:00+00:00</updated>
    <title>Re: Best AI garden design app?</title>
  </entry>
</feed>'''


class PromptPanelTest(unittest.TestCase):
    def test_asset_panel_is_valid(self):
        rows = prompt_panel.load_rows(ROOT / "assets" / "ai-answer-panel.csv")
        self.assertEqual(prompt_panel.validate(rows), [])
        self.assertEqual(prompt_panel.summary(rows)["active_prompts"], 10)

    def test_duplicate_active_text_fails(self):
        rows = prompt_panel.load_rows(ROOT / "assets" / "ai-answer-panel.csv")
        duplicate = dict(rows[0])
        duplicate["prompt_id"] = "q99"
        errors = prompt_panel.validate(rows + [duplicate])
        self.assertTrue(any("duplicate active prompt text" in error for error in errors))


class SocialFetchTest(unittest.TestCase):
    def test_reddit_rss_normalizes_thread(self):
        payload = social_fetch.parse_reddit_atom(
            ATOM,
            "https://www.reddit.com/r/landscaping/comments/abc123/example/",
            "thread",
        )
        self.assertEqual(payload["raw_source"], "reddit-rss")
        self.assertEqual(payload["post"]["engagement"]["replies"], 1)
        self.assertIn("AI garden design app", payload["post"]["text"])
        self.assertEqual(payload["post"]["links"][0]["url"], "https://example.com")
        self.assertEqual(len(payload["replies"]), 1)

    def test_non_reddit_host_fails_closed(self):
        with self.assertRaises(social_fetch.FetchError):
            social_fetch.canonical_reddit_url("https://example.com/r/test/comments/abc/post/")

    def test_private_route_fails_closed(self):
        with self.assertRaises(social_fetch.FetchError):
            social_fetch.canonical_reddit_url("https://www.reddit.com/message/inbox/")

    def test_fetch_requires_thread_url(self):
        with self.assertRaises(social_fetch.FetchError):
            social_fetch.fetch_reddit_thread("https://www.reddit.com/r/landscaping/", 5, None, 60)

    def test_rate_limit_stops_before_json_fallback(self):
        with mock.patch.object(social_fetch, "_request", return_value=(429, b"", {"retry-after": "60"})) as request:
            with self.assertRaisesRegex(social_fetch.FetchError, "no fallback attempted"):
                social_fetch.fetch_reddit_thread(
                    "https://www.reddit.com/r/landscaping/comments/abc123/example/", 5, None, 60
                )
        self.assertEqual(request.call_count, 1)


class GeoMetricsTest(unittest.TestCase):
    def test_metrics_keep_provider_blocks(self):
        rows = [
            {
                "run_id": "r1",
                "prompt_id": "q1",
                "prompt_version": 1,
                "prompt_text": "What is the best AI landscape tool?",
                "provider": "alpha",
                "model": "alpha-model",
                "surface": "api",
                "locale": "en-US",
                "account_state": "no_personalization",
                "captured_at": "2026-08-17T18:00:00Z",
                "status": "ok",
                "raw_answer": "Competitor, then Landscapio.",
                "parser_version": "fixture-1",
                "parse_review_state": "reviewed",
                "mentions": [
                    {"entity_id": "landscapio", "position": 2, "sentiment": "positive"},
                    {"entity_id": "competitor", "position": 1, "sentiment": "neutral"},
                ],
                "citations": [
                    {"url": "https://landscapio.example/", "domain": "landscapio.example", "source_type": "owned", "owned": True},
                    {"url": "https://editorial.example/", "domain": "editorial.example", "source_type": "editorial", "owned": False},
                ],
            },
            {
                "run_id": "r2",
                "prompt_id": "q1",
                "prompt_version": 1,
                "prompt_text": "What is the best AI landscape tool?",
                "provider": "beta",
                "model": "beta-model",
                "surface": "web",
                "locale": "en-US",
                "account_state": "logged_out",
                "captured_at": "2026-08-17T18:05:00Z",
                "status": "ok",
                "raw_answer": "Competitor.",
                "parser_version": "fixture-1",
                "parse_review_state": "reviewed",
                "mentions": [{"entity_id": "competitor", "position": 1, "sentiment": "positive"}],
                "citations": [
                    {"url": "https://community.example/", "domain": "community.example", "source_type": "community", "owned": False}
                ],
            },
        ]
        payload = geo_metrics.report(rows, "landscapio")
        self.assertEqual(set(payload["providers"]), {"alpha", "beta"})
        self.assertEqual(payload["providers"]["alpha"]["visibility"]["rate"], 1.0)
        self.assertEqual(payload["providers"]["beta"]["visibility"]["rate"], 0.0)
        self.assertAlmostEqual(payload["all_providers"]["citations"]["owned_share"], 1 / 3)
        self.assertIn("visibility_change_does_not_establish_causality", payload["all_providers"]["limitations"])


class OpportunityAndQueueTest(unittest.TestCase):
    def test_rank_never_allows_action_and_queue_stays_research_only(self):
        truth = {
            "keywords": ["ai landscape design", "garden design app", "yard photo"],
            "buyer_intent_terms": ["best", "recommend"],
            "exclude_terms": [],
            "do_not_engage_subreddits": [],
        }
        item = {
            "url": "https://www.reddit.com/r/landscaping/comments/abc123/example/",
            "title": "Best AI landscape design app?",
            "text": "Can anyone recommend a garden design app for a yard photo?",
            "updated_at": "2026-08-17T12:00:00Z",
        }
        now = rank_social.parse_time("2026-08-17T18:00:00Z")
        row = rank_social.score_item(item, truth, now)
        self.assertEqual(row["action_allowed"], "false")
        self.assertEqual(row["approval_state"], "research_only")
        queue = approval_queue.build([row], "2026-08-17T18:00:00+00:00")
        self.assertEqual(queue[0]["approval_state"], "research_only")
        self.assertEqual(queue[0]["execution_state"], "not_executed")
        self.assertEqual(queue[0]["rules_state"], "not_checked")
        self.assertEqual(queue[0]["reply_pattern"], "evidence_led_community_reply")
        for field in (
            "authority_basis",
            "mechanism_to_explain",
            "advice_correction",
            "follow_up_value_plan",
            "product_mention_justification",
        ):
            self.assertEqual(queue[0][field], "")

    def test_community_reply_review_asset_stays_non_executing(self):
        packet = json.loads((ROOT / "assets" / "community-reply-review.json").read_text(encoding="utf-8"))
        self.assertEqual(packet["rules_state"], "not_checked")
        self.assertEqual(packet["product_truth_state"], "not_checked")
        self.assertEqual(packet["approval_state"], "research_only")
        self.assertEqual(packet["execution_state"], "not_executed")
        self.assertEqual(packet["reply_pattern"], "evidence_led_community_reply")


class DocumentationContractTest(unittest.TestCase):
    def test_router_and_workflow_are_wired(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "workflows" / "ai-answer-visibility-loop.md").read_text(encoding="utf-8")
        reference = (ROOT / "references" / "integrations" / "social-fetch.md").read_text(encoding="utf-8")
        self.assertIn("workflows/ai-answer-visibility-loop.md", skill)
        self.assertIn("Reddit RSS/Atom", reference)
        normalized_workflow = " ".join(workflow.split())
        for phrase in (
            "Do not post, comment, submit, buy a placement, or publish without explicit human approval",
            "Keep providers separate",
            "Never convert answer counts or social observations into estimated impressions, clicks, CTR, conversions, or revenue",
            "A high score never grants action authority",
            "The reply must still help if the product name is removed",
            "Never split one answer into multiple comments, seed replies, or prolong a thread to influence ranking",
            "treat its account-history and causality claims as unverified",
        ):
            self.assertIn(phrase, normalized_workflow)


if __name__ == "__main__":
    unittest.main()
