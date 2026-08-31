#!/usr/bin/env python3
"""UNREVIEWED dual-register reference state machine."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Context:
    identity_reviewed: bool = False
    funding: bool = False
    procurement: bool = False
    human_reviewed: bool = False
    conflict: bool = False
    stale: bool = False
    news_count: int = 0

def state(ctx: Context) -> str:
    if ctx.conflict:
        return "CONFLICTED"
    if ctx.stale:
        return "STALE"
    if not ctx.identity_reviewed:
        return "IDENTITY_CANDIDATE"
    if ctx.funding and ctx.procurement:
        return "RELEASE_CANDIDATE" if ctx.human_reviewed else "CORROBORATED_WINDOW"
    if ctx.funding:
        return "FUNDING_OBSERVED"
    if ctx.procurement:
        return "PROCUREMENT_OBSERVED"
    return "IDENTITY_REVIEWED"

def apply(ctx: Context, event: str) -> None:
    if event == "IDENTITY_REVIEWED": ctx.identity_reviewed = True
    elif event == "FUNDING_OBSERVED": ctx.funding = True
    elif event == "PROCUREMENT_OBSERVED": ctx.procurement = True
    elif event == "NEWS_OBSERVED": ctx.news_count += 1
    elif event == "HUMAN_REVIEWED": ctx.human_reviewed = True
    elif event == "RETRACT_FUNDING": ctx.funding = False
    elif event == "RETRACT_PROCUREMENT": ctx.procurement = False
    elif event == "CONTRADICTION": ctx.conflict = True
    elif event == "RESOLVE_CONFLICT": ctx.conflict = False
    elif event == "MARK_STALE": ctx.stale = True
    elif event == "REFRESH": ctx.stale = False
    else: raise ValueError(event)
