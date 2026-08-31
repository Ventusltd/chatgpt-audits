# PipelineNews intelligence engine vNext — quarantined candidate

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`  
> This is quarantined study output. It is not installed, trusted or published.

This is a modular design candidate generated after four evidence checkpoints. It is not a product release and cannot write to PipelineNews, GridAtlas, Companies or GlobalGrid2050.

## Intended chain

```text
source-specific collectors
  -> append-only evidence ledger
    -> reviewed identity bindings
      -> dual-register timing state machine
        -> human-reviewed read model
          -> PipelineNews and GridAtlas consumers
```

## Why this is the next version

The present source surface contains large runners with collection, networking, evidence, identity, validation and publication concerns together. The candidate therefore extracts contracts first and leaves product implementation to a separate reviewed graduation.

## Files

- `architecture.vnext.json` — module and repository ownership.
- `schemas/evidence-event.schema.json` — observed, revised, retracted and contradicted evidence.
- `schemas/timing-transition.schema.json` — inferred state transitions with human-review status.
- `schemas/project-intelligence-summary.schema.json` — minimal reviewed consumer payload.
- `reference/state_machine.py` — non-publishing reference logic.
- `reference/test_state_machine.py` — one-signal silence, dual-register gate, retraction and review tests.
