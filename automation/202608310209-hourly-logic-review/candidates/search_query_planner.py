#!/usr/bin/env python3
"""UNREVIEWED quarantined candidate: entity-aware search query planner.

No network I/O. Consumer code supplies aliases, exclusions and source lanes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class Query:
    text: str
    lane: str
    reason: str


def normalise_terms(values: Iterable[str]) -> tuple[str, ...]:
    cleaned = {" ".join(value.split()).strip() for value in values if value.strip()}
    return tuple(sorted(cleaned, key=lambda value: (value.casefold(), value)))


def plan_queries(
    canonical_name: str,
    *,
    aliases: Sequence[str] = (),
    identifiers: Sequence[str] = (),
    event_terms: Sequence[str] = (),
    excluded_terms: Sequence[str] = (),
    source_lanes: Mapping[str, Sequence[str]] | None = None,
) -> list[Query]:
    names = normalise_terms([canonical_name, *aliases, *identifiers])
    events = normalise_terms(event_terms)
    exclusions = normalise_terms(excluded_terms)
    lanes = source_lanes or {"open_web": ()}
    output: list[Query] = []
    seen: set[tuple[str, str]] = set()

    for lane, lane_terms in sorted(lanes.items()):
        lane_suffix = " ".join(normalise_terms(lane_terms))
        for name in names:
            for event in events or ("",):
                positive = " ".join(
                    part for part in [f'"{name}"', event, lane_suffix] if part
                )
                negative = " ".join(f'-"{term}"' for term in exclusions)
                text = " ".join(part for part in [positive, negative] if part)
                key = (lane, text.casefold())
                if key in seen:
                    continue
                seen.add(key)
                output.append(
                    Query(
                        text=text,
                        lane=lane,
                        reason="canonical/alias x event x source-lane expansion",
                    )
                )
    return output
