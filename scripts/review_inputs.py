"""Shared, dependency-free input checks for offline SEO review tools."""
from datetime import datetime
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit

MAX_BYTES = 5_000_000
MAX_ROWS = 50_000


def bounded_bytes(path, limit=MAX_BYTES):
    with Path(path).open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError("input exceeds byte limit")
    return raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("non-finite JSON number is not allowed")


def load_json(path):
    raw = bounded_bytes(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                       parse_constant=_invalid_constant)
    return value, digest(raw)


def fields(value, required, optional=()):
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    if not set(required) <= set(value) or set(value) - set(required) - set(optional):
        raise ValueError("missing or unsupported object fields")


def text(value, label, limit=4096):
    if not isinstance(value, str) or not value or len(value) > limit:
        raise ValueError(label + " must be a nonempty bounded string")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(label + " contains control characters")
    return value


def timestamp(value):
    text(value, "observation time", 80)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value):
        raise ValueError("observation time must be an ISO timestamp with timezone")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() is None:
        raise ValueError("observation time must include timezone")
    return parsed


def public_url(value):
    """Validate syntax only. Never resolve DNS or fetch a URL."""
    text(value, "URL")
    if any(char.isspace() for char in value) or "\\" in value:
        raise ValueError("URL contains whitespace or backslash")
    parsed = urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("URL must use HTTP(S) and a domain")
    if parsed.username is not None or parsed.password is not None or parsed.fragment:
        raise ValueError("URL userinfo and fragments are not allowed")
    host = parsed.hostname.encode("idna").decode("ascii").lower()
    if host.endswith(".") or "." not in host or host.endswith((".local", ".localhost", ".internal")):
        raise ValueError("local or ambiguous hosts are not allowed")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if re.fullmatch(r"[0-9.]+", host):
            raise ValueError("numeric hosts are not allowed")
    else:
        raise ValueError("IP-literal hosts are not supported")
    if any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
           for label in host.split(".")):
        raise ValueError("invalid domain")
    expected_port = 443 if parsed.scheme == "https" else 80
    if parsed.port not in (None, expected_port):
        raise ValueError("nonstandard ports are not supported")
    return host


def lastmod(value):
    text(value, "lastmod", 80)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        datetime.strptime(value, "%Y-%m-%d")
    else:
        timestamp(value)
    return value


def write_json(path, payload, inputs=()):
    """Validate before this call; replace only the explicitly nominated report."""
    output = Path(path)
    if output.is_symlink() or output.resolve() in {Path(p).resolve() for p in inputs}:
        raise ValueError("output must not overwrite an input or symlink")
    encoded = (json.dumps(payload, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode()
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".seo-review-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(encoded)
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
