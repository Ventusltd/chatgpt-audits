# REVIEW STATUS: UNREVIEWED
"""Quarantined reference state machine for PipelineNews vNext.

This module is a design artefact only. It deliberately cannot publish.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class State(str, Enum):
    DISCOVERED = "DISCOVERED"
    IDENTITY_CANDIDATE = "IDENTITY_CANDIDATE"
    FUNDING_OBSERVED = "FUNDING_OBSERVED"
    PROCUREMENT_OBSERVED = "PROCUREMENT_OBSERVED"
    CORROBORATED_WINDOW = "CORROBORATED_WINDOW"
    HUMAN_REVIEWED = "HUMAN_REVIEWED"
    RELEASE_CANDIDATE = "RELEASE_CANDIDATE"
    WITHHELD = "WITHHELD"
    CONFLICTED = "CONFLICTED"
    STALE = "STALE"


class Lane(str, Enum):
    FUNDING = "FUNDING"
    PROCUREMENT = "PROCUREMENT"
    CORROBORATION = "CORROBORATION"


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    lane: Lane
    fact_status: str = "OBSERVED"
    retracted: bool = False

    @property
    def usable(self) -> bool:
        return self.fact_status == "OBSERVED" and not self.retracted


def observed_lanes(evidence: Iterable[Evidence]) -> set[Lane]:
    return {item.lane for item in evidence if item.usable}


def has_dual_register_corroboration(evidence: Iterable[Evidence]) -> bool:
    lanes = observed_lanes(evidence)
    return Lane.FUNDING in lanes and Lane.PROCUREMENT in lanes


def propose_transition(
    current: State,
    requested: State,
    evidence: Iterable[Evidence],
    *,
    identity_reviewed: bool = False,
    human_reviewed: bool = False,
    contradiction: bool = False,
) -> State:
    evidence = tuple(evidence)
    lanes = observed_lanes(evidence)

    if contradiction:
        return State.CONFLICTED

    if requested == State.IDENTITY_CANDIDATE:
        return State.IDENTITY_CANDIDATE

    if requested == State.FUNDING_OBSERVED:
        if Lane.FUNDING not in lanes:
            raise ValueError("observed funding evidence is required")
        return State.FUNDING_OBSERVED

    if requested == State.PROCUREMENT_OBSERVED:
        if Lane.PROCUREMENT not in lanes:
            raise ValueError("observed procurement evidence is required")
        return State.PROCUREMENT_OBSERVED

    if requested == State.CORROBORATED_WINDOW:
        if not identity_reviewed:
            raise ValueError("reviewed project identity is required")
        if not has_dual_register_corroboration(evidence):
            raise ValueError("both funding and procurement evidence are required")
        return State.CORROBORATED_WINDOW

    if requested == State.HUMAN_REVIEWED:
        if current != State.CORROBORATED_WINDOW or not human_reviewed:
            raise ValueError("human review follows a corroborated window")
        return State.HUMAN_REVIEWED

    if requested == State.RELEASE_CANDIDATE:
        if current != State.HUMAN_REVIEWED or not human_reviewed:
            raise ValueError("release candidate requires recorded human review")
        return State.RELEASE_CANDIDATE

    raise ValueError(f"unsupported or forbidden transition: {requested.value}")


def publish(*_args: object, **_kwargs: object) -> None:
    raise RuntimeError("PUBLISHED transitions are forbidden in chatgpt-audits")
