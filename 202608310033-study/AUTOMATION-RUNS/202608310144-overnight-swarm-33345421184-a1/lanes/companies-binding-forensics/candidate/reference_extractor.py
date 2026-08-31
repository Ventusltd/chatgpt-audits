#!/usr/bin/env python3
"""UNREVIEWED reference extractor: top-level REPD identity only."""
from __future__ import annotations


def extract_top_level_repd_ref(record: dict) -> str:
    if not isinstance(record, dict):
        raise TypeError("record must be a dict")
    value = record.get("repd_ref")
    if value is None:
        raise KeyError("top-level repd_ref is absent")
    text = str(value).strip()
    if not text or not text.isdigit():
        raise ValueError("top-level repd_ref must be numeric")
    return text
