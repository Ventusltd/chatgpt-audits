#!/usr/bin/env python3
"""UNREVIEWED quarantined candidate: deterministic search replay harness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence


@dataclass(frozen=True)
class Fixture:
    query: str
    required_ids: tuple[str, ...]
    forbidden_ids: tuple[str, ...] = ()


def replay(
    fixtures: Iterable[Fixture],
    search: Callable[[str], Sequence[str]],
) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for fixture in fixtures:
        returned = tuple(search(fixture.query))
        returned_set = set(returned)
        missing = sorted(set(fixture.required_ids) - returned_set)
        forbidden = sorted(set(fixture.forbidden_ids) & returned_set)
        findings.append(
            {
                "query": fixture.query,
                "returned": list(returned),
                "missing_required": missing,
                "returned_forbidden": forbidden,
                "pass": not missing and not forbidden,
            }
        )
    return findings
