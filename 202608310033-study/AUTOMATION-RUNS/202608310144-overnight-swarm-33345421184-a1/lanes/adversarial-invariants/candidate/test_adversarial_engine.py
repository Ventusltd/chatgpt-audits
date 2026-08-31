#!/usr/bin/env python3
"""UNREVIEWED deterministic adversarial properties."""
import json
import random
from reference_engine import Context, apply, state

EVENTS = ["IDENTITY_REVIEWED","FUNDING_OBSERVED","PROCUREMENT_OBSERVED","NEWS_OBSERVED","HUMAN_REVIEWED","RETRACT_FUNDING","RETRACT_PROCUREMENT","CONTRADICTION","RESOLVE_CONFLICT","MARK_STALE","REFRESH"]
rng = random.Random(202608310116)
sequences = 100000
transitions = 0
for _ in range(sequences):
    ctx = Context()
    for _ in range(rng.randint(1, 30)):
        before_funding, before_procurement = ctx.funding, ctx.procurement
        event = rng.choice(EVENTS)
        apply(ctx, event)
        current = state(ctx)
        transitions += 1
        if event == "NEWS_OBSERVED":
            assert (ctx.funding, ctx.procurement) == (before_funding, before_procurement)
        if current == "CORROBORATED_WINDOW":
            assert ctx.identity_reviewed and ctx.funding and ctx.procurement and not ctx.conflict and not ctx.stale and not ctx.human_reviewed
        if current == "RELEASE_CANDIDATE":
            assert ctx.identity_reviewed and ctx.funding and ctx.procurement and ctx.human_reviewed and not ctx.conflict and not ctx.stale
        if ctx.conflict:
            assert current == "CONFLICTED"
        if ctx.stale and not ctx.conflict:
            assert current == "STALE"

news = Context(identity_reviewed=True)
for _ in range(1000): apply(news, "NEWS_OBSERVED")
assert state(news) == "IDENTITY_REVIEWED"
print(json.dumps({"review_status":"UNREVIEWED","classification":"observed","sequences":sequences,"transitions":transitions,"failures":0}))
