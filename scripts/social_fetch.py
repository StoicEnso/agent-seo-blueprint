#!/usr/bin/env python3
"""Fetch public social-post data into a normalized JSON contract.

Version 1 deliberately supports Reddit only. The verified path on this host is
Reddit's Atom/RSS surface. Reddit ``.json`` is a bounded fallback because it
can return HTTP 403 even for public posts.

No login, posting, voting, paid API, CAPTCHA bypass, or private/deleted-content
recovery is implemented.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

VERSION = "0.1.0"
ATOM = {"a": "http://www.w3.org/2005/Atom"}
ALLOWED_REDDIT_HOSTS = {"reddit.com", "www.reddit.com", "old.reddit.com"}
DEFAULT_UA = os.environ.get(
    "SOCIAL_FETCH_USER_AGENT",
    "AgentSEOBlueprint-SocialFetch/0.1 (public research; no posting)",
)


class FetchError(RuntimeError):
    """A public fetch failed after the bounded strategy chain."""


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.links: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data.strip())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def html_to_text(value: str) -> tuple[str, list[str]]:
    parser = _TextExtractor()
    parser.feed(value or "")
    text = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
    return html.unescape(text), list(dict.fromkeys(parser.links))


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_reddit_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_REDDIT_HOSTS:
        raise FetchError(f"unsupported host: {host or '(missing)'}")
    if not parsed.path.startswith("/r/") and parsed.path not in {"/search", "/search/"}:
        raise FetchError("only public Reddit subreddit, thread, and search URLs are supported")
    path = re.sub(r"/+", "/", parsed.path)
    return urllib.parse.urlunparse(("https", "www.reddit.com", path, "", parsed.query, ""))


def _request(url: str, timeout: int, accept: str) -> tuple[int, bytes, dict[str, str]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": DEFAULT_UA,
            "Accept": accept,
            "Accept-Language": "en-GB,en;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            headers = {k.lower(): v for k, v in response.headers.items()}
            return response.status, response.read(), headers
    except urllib.error.HTTPError as exc:
        headers = {k.lower(): v for k, v in exc.headers.items()}
        return exc.code, exc.read(), headers
    except (urllib.error.URLError, TimeoutError) as exc:
        raise FetchError(f"network error for {url}: {exc}") from exc


def _cache_path(cache_dir: Path, url: str) -> Path:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return cache_dir / f"{digest}.json"


def _read_cache(cache_dir: Path | None, url: str, ttl_seconds: int) -> dict[str, Any] | None:
    if not cache_dir:
        return None
    path = _cache_path(cache_dir, url)
    if not path.exists() or time.time() - path.stat().st_mtime > ttl_seconds:
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["cache"] = {"hit": True, "path": str(path), "ttl_seconds": ttl_seconds}
    return payload


def _write_cache(cache_dir: Path | None, url: str, payload: dict[str, Any]) -> None:
    if not cache_dir:
        return
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = _cache_path(cache_dir, url)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _entry(entry: ET.Element) -> dict[str, Any]:
    link_el = entry.find("a:link", ATOM)
    author = entry.findtext("a:author/a:name", default="", namespaces=ATOM) or None
    content_html = entry.findtext("a:content", default="", namespaces=ATOM) or ""
    text, links = html_to_text(content_html)
    title = (entry.findtext("a:title", default="", namespaces=ATOM) or "").strip()
    url = link_el.attrib.get("href") if link_el is not None else None
    return {
        "url": url,
        "title": title,
        "author": {
            "handle": author,
            "name": None,
            "verified": None,
            "follower_count": None,
            "profile_url": f"https://www.reddit.com{author}" if author and author.startswith("/u/") else None,
            "avatar_url": None,
        },
        "posted_at": entry.findtext("a:published", default=None, namespaces=ATOM),
        "updated_at": entry.findtext("a:updated", default=None, namespaces=ATOM),
        "text": text,
        "html": content_html or None,
        "links": [{"url": item, "expanded_url": item, "title": None} for item in links],
        "media": [],
        "engagement": {
            "likes": None,
            "reposts": None,
            "replies": None,
            "bookmarks": None,
            "views": None,
            "quotes": None,
        },
    }


def parse_reddit_atom(body: bytes, requested_url: str, mode: str) -> dict[str, Any]:
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        raise FetchError(f"Reddit RSS parse failed: {exc}") from exc
    entries = [_entry(node) for node in root.findall("a:entry", ATOM)]
    feed_title = root.findtext("a:title", default="", namespaces=ATOM)
    feed_updated = root.findtext("a:updated", default=None, namespaces=ATOM)

    if mode == "thread":
        if not entries:
            raise FetchError("Reddit thread RSS returned no entries")
        post, replies = entries[0], entries[1:]
        post["engagement"]["replies"] = len(replies)
        return {
            "schema_version": "social-fetch-0.1",
            "platform": "reddit",
            "url": canonical_reddit_url(post.get("url") or requested_url),
            "requested_url": requested_url,
            "fetched_at": utc_now(),
            "raw_source": "reddit-rss",
            "status": "ok",
            "post": post,
            "replies": replies,
            "limitations": [
                "rss_has_no_vote_counts",
                "rss_reply_order_may_not_match_reddit_ui",
                "public_data_only",
            ],
        }

    items = [item for item in entries if item.get("url") and "/comments/" in item["url"]]
    return {
        "schema_version": "social-fetch-0.1",
        "platform": "reddit",
        "url": requested_url,
        "requested_url": requested_url,
        "fetched_at": utc_now(),
        "raw_source": "reddit-rss-search",
        "status": "ok",
        "feed": {"title": feed_title, "updated_at": feed_updated},
        "items": items,
        "limitations": [
            "rss_has_no_vote_counts",
            "reddit_search_relevance_is_platform_defined",
            "public_data_only",
        ],
    }


def _json_thread(body: bytes, requested_url: str) -> dict[str, Any]:
    try:
        raw = json.loads(body)
        post_data = raw[0]["data"]["children"][0]["data"]
        comment_nodes = raw[1]["data"]["children"]
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise FetchError(f"Reddit JSON parse failed: {exc}") from exc

    def comment(node: dict[str, Any]) -> dict[str, Any] | None:
        data = node.get("data", {})
        if node.get("kind") != "t1":
            return None
        permalink = data.get("permalink")
        return {
            "url": f"https://www.reddit.com{permalink}" if permalink else None,
            "title": None,
            "author": {"handle": f"/u/{data.get('author')}" if data.get("author") else None, "name": None},
            "posted_at": dt.datetime.fromtimestamp(data["created_utc"], dt.timezone.utc).isoformat() if data.get("created_utc") else None,
            "updated_at": None,
            "text": data.get("body", ""),
            "html": data.get("body_html"),
            "links": [],
            "media": [],
            "engagement": {"likes": data.get("score"), "reposts": None, "replies": None, "bookmarks": None, "views": None, "quotes": None},
        }

    permalink = post_data.get("permalink")
    post = {
        "url": f"https://www.reddit.com{permalink}" if permalink else requested_url,
        "title": post_data.get("title"),
        "author": {"handle": f"/u/{post_data.get('author')}" if post_data.get("author") else None, "name": None},
        "posted_at": dt.datetime.fromtimestamp(post_data["created_utc"], dt.timezone.utc).isoformat() if post_data.get("created_utc") else None,
        "updated_at": None,
        "text": post_data.get("selftext", ""),
        "html": post_data.get("selftext_html"),
        "links": [],
        "media": [],
        "engagement": {"likes": post_data.get("score"), "reposts": None, "replies": post_data.get("num_comments"), "bookmarks": None, "views": post_data.get("view_count"), "quotes": None},
    }
    replies = [parsed for node in comment_nodes if (parsed := comment(node))]
    return {
        "schema_version": "social-fetch-0.1",
        "platform": "reddit",
        "url": canonical_reddit_url(post["url"]),
        "requested_url": requested_url,
        "fetched_at": utc_now(),
        "raw_source": "reddit-json",
        "status": "ok",
        "post": post,
        "replies": replies,
        "limitations": ["top_level_replies_only", "public_data_only"],
    }


def fetch_reddit_thread(url: str, timeout: int, cache_dir: Path | None, ttl_seconds: int) -> dict[str, Any]:
    canonical = canonical_reddit_url(url).split("?", 1)[0].rstrip("/") + "/"
    if not re.match(r"^https://www\.reddit\.com/r/[^/]+/comments/[^/]+(?:/[^/]+)?/$", canonical, re.I):
        raise FetchError("fetch requires a public Reddit thread URL under /r/<subreddit>/comments/<id>/")
    cache_key = canonical + "thread"
    cached = _read_cache(cache_dir, cache_key, ttl_seconds)
    if cached:
        return cached

    attempts: list[dict[str, Any]] = []
    rss_url = canonical + ".rss"
    status, body, headers = _request(rss_url, timeout, "application/atom+xml, application/xml;q=0.9")
    attempts.append({"strategy": "reddit-rss", "status": status, "url": rss_url})
    if status == 200 and body:
        payload = parse_reddit_atom(body, canonical, "thread")
        payload["attempts"] = attempts
        _write_cache(cache_dir, cache_key, payload)
        return payload
    if status == 429:
        raise FetchError(f"Reddit RSS rate limited the request; retry_after={headers.get('retry-after')}; no fallback attempted")

    json_url = canonical + ".json?raw_json=1"
    status, body, headers = _request(json_url, timeout, "application/json")
    attempts.append({"strategy": "reddit-json", "status": status, "url": json_url})
    if status == 200 and body:
        payload = _json_thread(body, canonical)
        payload["attempts"] = attempts
        _write_cache(cache_dir, cache_key, payload)
        return payload

    retry_after = headers.get("retry-after")
    raise FetchError(f"Reddit public fetch failed; attempts={attempts}; retry_after={retry_after}")


def reddit_search_url(query: str, subreddit: str | None, sort: str, period: str) -> str:
    params = {"q": query, "sort": sort, "t": period}
    if subreddit:
        params["restrict_sr"] = "on"
        base = f"https://www.reddit.com/r/{urllib.parse.quote(subreddit)}/search.rss"
    else:
        base = "https://www.reddit.com/search.rss"
    return f"{base}?{urllib.parse.urlencode(params)}"


def search_reddit(query: str, subreddit: str | None, sort: str, period: str, timeout: int, limit: int, cache_dir: Path | None, ttl_seconds: int) -> dict[str, Any]:
    url = reddit_search_url(query, subreddit, sort, period)
    cached = _read_cache(cache_dir, url, ttl_seconds)
    if cached:
        cached["items"] = cached.get("items", [])[:limit]
        return cached
    status, body, headers = _request(url, timeout, "application/atom+xml, application/xml;q=0.9")
    if status != 200:
        raise FetchError(f"Reddit search RSS failed: status={status}; retry_after={headers.get('retry-after')}")
    payload = parse_reddit_atom(body, url, "search")
    payload["items"] = payload["items"][:limit]
    payload["attempts"] = [{"strategy": "reddit-rss-search", "status": status, "url": url}]
    _write_cache(cache_dir, url, payload)
    return payload


def write_payload(payload: dict[str, Any], output: str | None) -> None:
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if output:
        path = Path(output).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(path)
    else:
        print(text, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch normalized public social data. Reddit is supported in v0.1.")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--cache-dir", default=None)
    parser.add_argument("--cache-ttl", type=int, default=86400)
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="Fetch one public Reddit thread")
    fetch.add_argument("url")
    fetch.add_argument("--out")

    search = sub.add_parser("reddit-search", help="Search public Reddit RSS")
    search.add_argument("query")
    search.add_argument("--subreddit")
    search.add_argument("--sort", choices=["relevance", "hot", "top", "new", "comments"], default="relevance")
    search.add_argument("--period", choices=["hour", "day", "week", "month", "year", "all"], default="year")
    search.add_argument("--limit", type=int, default=25)
    search.add_argument("--out")

    args = parser.parse_args()
    cache_dir = Path(args.cache_dir).expanduser() if args.cache_dir else None
    try:
        if args.command == "fetch":
            payload = fetch_reddit_thread(args.url, args.timeout, cache_dir, args.cache_ttl)
            write_payload(payload, args.out)
        else:
            payload = search_reddit(args.query, args.subreddit, args.sort, args.period, args.timeout, args.limit, cache_dir, args.cache_ttl)
            write_payload(payload, args.out)
        return 0
    except FetchError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
