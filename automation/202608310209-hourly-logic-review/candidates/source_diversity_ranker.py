#!/usr/bin/env python3
"""UNREVIEWED quarantined candidate: relevance/diversity evidence reranker."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    domain: str
    relevance: float
    authority: float
    recency: float


def rank(
    rows: Iterable[Evidence],
    *,
    diversity_penalty: float = 0.18,
    limit: int = 20,
) -> list[Evidence]:
    remaining = list(rows)
    selected: list[Evidence] = []
    domain_counts: dict[str, int] = {}

    while remaining and len(selected) < limit:
        def score(item: Evidence) -> tuple[float, str]:
            base = (
                0.55 * item.relevance
                + 0.30 * item.authority
                + 0.15 * item.recency
            )
            penalty = diversity_penalty * domain_counts.get(item.domain.casefold(), 0)
            return (base - penalty, item.evidence_id)

        best = max(remaining, key=score)
        remaining.remove(best)
        selected.append(best)
        key = best.domain.casefold()
        domain_counts[key] = domain_counts.get(key, 0) + 1
    return selected
