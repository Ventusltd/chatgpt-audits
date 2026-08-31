#!/usr/bin/env python3
"""UNREVIEWED quarantined candidate: identity collision gate."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Binding:
    evidence_id: str
    subject_key: str
    candidate_key: str
    confidence: float


def conflicts(
    rows: Iterable[Binding],
    *,
    minimum_confidence: float = 0.70,
) -> list[dict[str, object]]:
    grouped: dict[str, list[Binding]] = defaultdict(list)
    for row in rows:
        if row.confidence >= minimum_confidence:
            grouped[row.subject_key].append(row)

    findings: list[dict[str, object]] = []
    for subject, candidates in sorted(grouped.items()):
        keys = sorted({row.candidate_key for row in candidates})
        if len(keys) <= 1:
            continue
        findings.append(
            {
                "subject_key": subject,
                "candidate_keys": keys,
                "evidence_ids": sorted({row.evidence_id for row in candidates}),
                "decision": "ABSTAIN_IDENTITY_COLLISION",
            }
        )
    return findings
