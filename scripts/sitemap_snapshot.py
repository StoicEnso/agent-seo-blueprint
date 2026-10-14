#!/usr/bin/env python3
"""Make and compare bounded snapshots of saved UTF-8 sitemap XML. No network."""
import argparse
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from review_inputs import (MAX_ROWS, bounded_bytes, digest, fields, lastmod,
                           load_json, public_url, text, timestamp, write_json)

NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
LIMITATIONS = ["Saved XML and operator-supplied source metadata require provenance review.",
               "Listings and lastmod are not proof of publication date, page edits, indexation, rankings, traffic or queries."]


def local_tag(tag, namespace):
    prefix = "{" + namespace + "}" if namespace else ""
    if not isinstance(tag, str) or not tag.startswith(prefix):
        raise ValueError("unexpected XML namespace")
    name = tag[len(prefix):]
    if "{" in name or "}" in name:
        raise ValueError("unexpected XML namespace")
    return name


def xml_fields(node, namespace):
    result = {}
    for child in node:
        # Image/news extensions are not page URL or lastmod evidence.
        if child.tag.startswith("{") and not child.tag.startswith("{" + namespace + "}"):
            continue
        name = local_tag(child.tag, namespace)
        if name not in ("loc", "lastmod"):
            continue
        if name in result or len(child):
            raise ValueError("duplicate or nested sitemap field")
        result[name] = (child.text or "").strip()
    if not result.get("loc"):
        raise ValueError("sitemap entry has no loc")
    if result.get("lastmod"):
        lastmod(result["lastmod"])
    else:
        result.pop("lastmod", None)
    return result


def validate_snapshot(value):
    fields(value, ("schema_version", "source_sitemap", "observation_time", "xml_sha256",
                   "capture_status", "complete", "limitations", "urls"), ("index_children",))
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("unsupported snapshot version")
    host = public_url(value["source_sitemap"])
    timestamp(value["observation_time"])
    if not isinstance(value["xml_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", value["xml_sha256"]):
        raise ValueError("invalid XML fingerprint")
    if type(value["complete"]) is not bool:
        raise ValueError("complete must be boolean")
    status = value["capture_status"]
    if status not in ("complete_urlset", "partial_urlset", "unresolved_index"):
        raise ValueError("unsupported capture status")
    if value["complete"] != (status == "complete_urlset"):
        raise ValueError("complete flag disagrees with capture status")
    limitations = value["limitations"]
    if not isinstance(limitations, list) or not 1 <= len(limitations) <= 20:
        raise ValueError("limitations must be a nonempty bounded list")
    for limitation in limitations:
        text(limitation, "limitation")
    rows = value["urls"]
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise ValueError("urls must be a bounded list")
    seen = set()
    for row in rows:
        fields(row, ("url",), ("lastmod",))
        if public_url(row["url"]) != host:
            raise ValueError("URL host differs from source sitemap")
        if row["url"] in seen:
            raise ValueError("duplicate URL")
        seen.add(row["url"])
        if "lastmod" in row:
            lastmod(row["lastmod"])
    if status == "unresolved_index":
        if rows or "index_children" not in value:
            raise ValueError("unresolved index cannot assert page coverage")
        children = value["index_children"]
        if not isinstance(children, list) or len(children) > MAX_ROWS:
            raise ValueError("index_children must be a bounded list")
        seen_children = set()
        for child in children:
            if public_url(child) != host or child in seen_children:
                raise ValueError("unsafe or duplicate index child")
            seen_children.add(child)
    elif "index_children" in value:
        raise ValueError("urlset cannot contain index_children")
    return value


def snapshot(input_path, source, observed, incomplete=False):
    host = public_url(source)
    timestamp(observed)
    raw = bounded_bytes(input_path)
    # The supported format is UTF-8; this also closes UTF-16/32 DTD bypasses.
    decoded = raw.decode("utf-8-sig")
    if "\x00" in decoded or re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", decoded, re.I):
        raise ValueError("DTD/entities and non-UTF-8 XML are not supported")
    declaration = re.search(r"<\?xml[^>]*encoding\s*=\s*['\"]([^'\"]+)['\"]", decoded, re.I)
    if declaration and declaration.group(1).lower() not in ("utf-8", "utf8", "us-ascii"):
        raise ValueError("XML must use UTF-8")
    root = ET.fromstring(decoded)
    namespace = root.tag[1:].split("}", 1)[0] if root.tag.startswith("{") else ""
    if namespace not in ("", NAMESPACE):
        raise ValueError("unexpected sitemap namespace")
    kind = local_tag(root.tag, namespace)
    if kind not in ("urlset", "sitemapindex"):
        raise ValueError("expected urlset or sitemapindex")
    expected = "url" if kind == "urlset" else "sitemap"
    rows, children, seen = [], [], set()
    for entry in root:
        if local_tag(entry.tag, namespace) != expected:
            raise ValueError("unexpected sitemap entry")
        data = xml_fields(entry, namespace)
        if public_url(data["loc"]) != host:
            raise ValueError("unsafe or unexpected-host URL")
        if data["loc"] in seen:
            raise ValueError("duplicate URL")
        seen.add(data["loc"])
        if len(seen) > MAX_ROWS:
            raise ValueError("sitemap row cap exceeded")
        if kind == "urlset":
            rows.append({"url": data["loc"], **({"lastmod": data["lastmod"]} if "lastmod" in data else {})})
        else:
            children.append(data["loc"])
    status = "unresolved_index" if kind == "sitemapindex" else "partial_urlset" if incomplete else "complete_urlset"
    result = {"schema_version": 1, "source_sitemap": source, "observation_time": observed,
              "xml_sha256": digest(raw), "capture_status": status,
              "complete": status == "complete_urlset", "limitations": list(LIMITATIONS), "urls": rows}
    if kind == "sitemapindex":
        result["index_children"] = children
        result["limitations"].append("Index children were not combined; all comparison claims are suppressed.")
    if incomplete:
        result["limitations"].append("Operator marked the capture incomplete; all comparison claims are suppressed.")
    return validate_snapshot(result)


def comparison(baseline, current):
    validate_snapshot(current)
    common = {"schema_version": 1, "candidate_only": True,
              "source_sitemap": current["source_sitemap"], "current_observation_time": current["observation_time"],
              "current_xml_sha256": current["xml_sha256"], "limitations": list(LIMITATIONS)}
    if baseline is None:
        return {**common, "comparison": "suppressed", "reason": "baseline_unavailable"}
    validate_snapshot(baseline)
    if baseline["source_sitemap"] != current["source_sitemap"]:
        raise ValueError("source sitemap mismatch")
    if timestamp(baseline["observation_time"]) >= timestamp(current["observation_time"]):
        raise ValueError("snapshot times must be strictly increasing")
    common.update(baseline_observation_time=baseline["observation_time"], baseline_xml_sha256=baseline["xml_sha256"])
    if not baseline["complete"] or not current["complete"]:
        return {**common, "comparison": "suppressed", "reason": "incomplete_or_index_coverage"}
    before = {row["url"]: row for row in baseline["urls"]}
    after = {row["url"]: row for row in current["urls"]}
    changed = sorted(url for url in set(before) & set(after) if before[url].get("lastmod") != after[url].get("lastmod"))
    return {**common, "comparison": "conservative", "newly_listed": sorted(set(after) - set(before)),
            "no_longer_listed": sorted(set(before) - set(after)), "lastmod_changed": changed,
            "lastmod_changes": [{"url": url, "before": before[url].get("lastmod"), "after": after[url].get("lastmod"),
                                 "metadata_only": True} for url in changed]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("snapshot")
    make.add_argument("--input", required=True)
    make.add_argument("--source", required=True)
    make.add_argument("--observed", required=True)
    make.add_argument("--incomplete", action="store_true")
    make.add_argument("--output", required=True)
    diff = commands.add_parser("compare")
    diff.add_argument("--baseline", required=True)
    diff.add_argument("--current", required=True)
    diff.add_argument("--output", required=True)
    arguments = parser.parse_args()
    if arguments.command == "snapshot":
        result = snapshot(arguments.input, arguments.source, arguments.observed, arguments.incomplete)
        inputs = (arguments.input,)
    else:
        current, current_hash = load_json(arguments.current)
        baseline, baseline_hash = (load_json(arguments.baseline) if Path(arguments.baseline).exists() else (None, None))
        result = comparison(baseline, current)
        result.update(current_snapshot_sha256=current_hash, baseline_snapshot_sha256=baseline_hash)
        inputs = (arguments.baseline, arguments.current)
    write_json(arguments.output, result, inputs=inputs)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, ET.ParseError, OSError, UnicodeError) as error:
        raise SystemExit("sitemap-review: " + str(error))
