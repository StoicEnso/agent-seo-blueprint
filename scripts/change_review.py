#!/usr/bin/env python3
"""Read pinned Git metadata; emit product-copy review candidates, never edits."""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import subprocess
import time
from urllib.parse import urlsplit

from review_inputs import fields, load_json, public_url, text, write_json

GIT_TIMEOUT = 30
GIT_OUTPUT_LIMIT = 1_000_000


def git(repo, *arguments):
    """No shell, hooks, external diff, text conversion, network or repo code."""
    environment = os.environ.copy()
    for key in list(environment):
        if key.startswith("GIT_"):
            environment.pop(key)
    environment.update(GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0", LC_ALL="C")
    command = ["git", "--no-pager", "-C", str(repo), "-c", "core.hooksPath=/dev/null",
               "-c", "core.fsmonitor=false", *arguments]
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment)
    buffers = {process.stdout: bytearray(), process.stderr: bytearray()}
    deadline = time.monotonic() + GIT_TIMEOUT
    try:
        with selectors.DefaultSelector() as selector:
            for stream in buffers:
                selector.register(stream, selectors.EVENT_READ)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ValueError("Git read timed out")
                for key, _ in selector.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 8192)
                    if not chunk:
                        selector.unregister(key.fileobj)
                    else:
                        buffers[key.fileobj].extend(chunk)
                        if sum(map(len, buffers.values())) > GIT_OUTPUT_LIMIT:
                            raise ValueError("Git metadata exceeds output limit")
        process.wait(timeout=max(0.01, deadline - time.monotonic()))
        if process.returncode:
            raise ValueError("Git read failed; check repository, revisions or ancestry")
        return bytes(buffers[process.stdout])
    except subprocess.TimeoutExpired as error:
        raise ValueError("Git read timed out") from error
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        process.stdout.close()
        process.stderr.close()


def commit(repo, revision):
    text(revision, "revision", 200)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_./~^+-]*", revision):
        raise ValueError("unsupported revision syntax")
    value = git(repo, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value):
        raise ValueError("revision did not resolve to one commit")
    return value


def safe_path(value):
    if not isinstance(value, str) or not value or len(value) > 4096:
        return False
    if any(ord(char) < 32 or ord(char) == 127 for char in value) or "\\" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        return False
    for part in path.parts:
        lowered = part.lower()
        if (lowered in (".git", "_source", "node_modules", "vendor", "id_rsa", "id_ed25519")
                or lowered.startswith((".env", "private", "_private", "secret", "credential"))
                or "secret" in lowered or "credential" in lowered
                or lowered.endswith((".pem", ".key", ".p12", ".pfx"))):
            return False
    return True


def mapping(path):
    value, fingerprint = load_json(path)
    fields(value, ("schema_version", "site_url", "mappings"), ("notes",))
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("unsupported mapping version")
    host = public_url(value["site_url"])
    parsed_site = urlsplit(value["site_url"])
    if parsed_site.path not in ("", "/") or parsed_site.query:
        raise ValueError("site_url must be an origin")
    if "notes" in value:
        text(value["notes"], "mapping notes")
    rows = value["mappings"]
    if not isinstance(rows, list) or len(rows) > 1000:
        raise ValueError("mappings must be a bounded list")
    identifiers = set()
    for row in rows:
        fields(row, ("claim_id", "source_paths", "owned_page", "claim"), ("evidence_urls",))
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", text(row["claim_id"], "claim_id", 80)):
            raise ValueError("invalid claim_id")
        if row["claim_id"] in identifiers:
            raise ValueError("duplicate claim_id")
        identifiers.add(row["claim_id"])
        paths = row["source_paths"]
        if not isinstance(paths, list) or not 1 <= len(paths) <= 200:
            raise ValueError("source_paths must be a nonempty bounded list")
        if any(not safe_path(path) for path in paths) or len(set(paths)) != len(paths):
            raise ValueError("unsafe or duplicate mapping path")
        page = text(row["owned_page"], "owned_page")
        if page.startswith("/") and not page.startswith("//"):
            page = value["site_url"].rstrip("/") + page
        if public_url(page) != host:
            raise ValueError("owned_page must belong to site_url")
        text(row["claim"], "claim")
        evidence = row.get("evidence_urls", [])
        if not isinstance(evidence, list) or len(evidence) > 20:
            raise ValueError("evidence_urls must be a bounded list")
        for url in evidence:
            public_url(url)
    return value, fingerprint


def changes(repo, base, head, cap):
    raw = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-status", "-z",
              "--find-renames", base, head, "--")
    tokens = raw.decode("utf-8").split("\0")
    if tokens[-1] != "":
        raise ValueError("truncated Git path metadata")
    tokens.pop()
    result, index, path_count = [], 0, 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        if not re.fullmatch(r"(?:[AMDT]|R\d{1,3})", status):
            raise ValueError("unsupported Git change status")
        count = 2 if status.startswith("R") else 1
        if index + count > len(tokens):
            raise ValueError("truncated Git change record")
        paths = tokens[index:index + count]
        index += count
        path_count += count
        if path_count > cap:
            raise ValueError("changed path cap exceeded")
        result.append({"status": status, "paths": paths})
    stat = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--numstat", "-z",
               "--no-renames", base, head, "--")
    binary = set()
    for record in stat.decode("utf-8").split("\0"):
        if not record:
            continue
        columns = record.split("\t", 2)
        if len(columns) != 3:
            raise ValueError("invalid Git binary metadata")
        if columns[:2] == ["-", "-"]:
            binary.add(columns[2])
    return result, binary


def review(repository, base_ref, head_ref, map_path, cap=200):
    if not 1 <= cap <= 1000:
        raise ValueError("max-paths must be 1..1000")
    repo = Path(repository).resolve()
    root = Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if root != repo:
        raise ValueError("repo must name the repository root, not a subdirectory")
    base, head = commit(repo, base_ref), commit(repo, head_ref)
    git(repo, "merge-base", "--is-ancestor", base, head)
    ledger, fingerprint = mapping(map_path)
    records, binary = changes(repo, base, head, cap)
    candidates, excluded = [], 0
    for record in records:
        paths = [path for path in record["paths"] if safe_path(path)]
        excluded += len(record["paths"]) - len(paths)
        if not paths:
            continue
        matches = [row for row in ledger["mappings"] if set(paths) & set(row["source_paths"])]
        candidates.append({"status": record["status"], "source_paths": paths,
                           "binary_metadata_only": bool(set(paths) & binary),
                           "disposition": "review_product_copy" if matches else "needs_mapping",
                           "mapped_claims": matches})
    return {"schema_version": 1, "kind": "candidate_product_copy_review", "candidate_only": True,
            "observation_time": datetime.now(timezone.utc).isoformat(), "repo": str(repo),
            "base_commit": base, "head_commit": head, "site_url": ledger["site_url"],
            "mapping_sha256": fingerprint, "excluded_path_count": excluded,
            "changed": candidates,
            "limitations": ["Git metadata does not prove shipment or stale published facts.",
                            "No diff bodies or binary content are emitted; working-tree edits are excluded.",
                            "Verify product truth, live pages and approved exact diff before a site write."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--map", required=True)
    parser.add_argument("--max-paths", type=int, default=200)
    parser.add_argument("--output", required=True)
    arguments = parser.parse_args()
    payload = review(arguments.repo, arguments.base, arguments.head, arguments.map, arguments.max_paths)
    write_json(arguments.output, payload, inputs=(arguments.map,))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, UnicodeError) as error:
        raise SystemExit("change-review: " + str(error))
