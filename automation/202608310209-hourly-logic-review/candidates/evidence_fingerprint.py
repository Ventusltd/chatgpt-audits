#!/usr/bin/env python3
"""UNREVIEWED quarantined candidate: evidence canonicalisation and hashing."""

from __future__ import annotations

import hashlib
import re
import urllib.parse
from dataclasses import dataclass


TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
SPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class Fingerprint:
    canonical_url: str
    content_sha256: str


def canonical_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value.strip())
    host = parsed.netloc.casefold().removeprefix("www.")
    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    pairs = [
        (key, item)
        for key, item in pairs
        if not key.casefold().startswith("utm_")
        and key.casefold() not in TRACKING_KEYS
    ]
    query = urllib.parse.urlencode(sorted(pairs))
    path = re.sub(r"/+", "/", parsed.path or "/")
    return urllib.parse.urlunsplit(
        (parsed.scheme.casefold() or "https", host, path.rstrip("/") or "/", query, "")
    )


def normalise_text(value: str) -> str:
    return SPACE_RE.sub(" ", value.casefold()).strip()


def fingerprint(url: str, title: str, body: str = "") -> Fingerprint:
    canonical = canonical_url(url)
    payload = "\n".join([canonical, normalise_text(title), normalise_text(body)])
    return Fingerprint(
        canonical_url=canonical,
        content_sha256=hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    )
