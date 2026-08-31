# PipelineNews intelligence engine vNext — seed architecture

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`  
> This is a quarantined design seed, not a PipelineNews release.

## Commercial purpose

The product is a timing engine for grid-connection sales. The high-value state is not “a headline exists”; it is a reviewed project identity for which both of these are on the record:

1. an organisation-level **funding signal** from Companies House evidence; and
2. a **procurement signal** from a local planning or procurement register.

The engine stays silent when only one lane is present. News is corroboration and explanation, not the authority that creates either register fact.

## Proposed module boundary

```text
collectors
  -> evidence ledger
    -> identity binder
      -> timing state machine
        -> reviewed read model
          -> PipelineNews + GridAtlas
```

| Module | Owns | Must not own |
|---|---|---|
| Collectors | source-specific retrieval, source card, raw receipt | identity decision, score, publication |
| Evidence ledger | observed events, revisions, retractions, contradictions, hashes | UI and promotion |
| Identity binder | project/company/planning relationships, abstention, validity | source collection and timing inference |
| Timing state machine | funding lane, procurement lane, staleness, withheld/conflicted states | rewriting evidence or publishing |
| Reviewed read model | minimum human-reviewed consumer payload | raw Companies data or unreviewed inference |

## Candidate state path

```text
DISCOVERED
  -> IDENTITY_CANDIDATE
  -> FUNDING_OBSERVED / PROCUREMENT_OBSERVED
  -> CORROBORATED_WINDOW
  -> HUMAN_REVIEWED
  -> RELEASE_CANDIDATE
```

Parallel safety states: `WITHHELD`, `CONFLICTED`, `STALE`.

`PUBLISHED` is outside this audit design. It remains the responsibility of an existing reviewed product-repository promotion workflow.

## Cross-repository ownership

- **Companies:** compact factual company/project relationships and organisation-level register events; no public individual PII or company-master dump.
- **PipelineNews:** evidence ledger, identity bindings, inferred timing states, withholding/conflict logic and reviewed read model.
- **GridAtlas:** exact project receiver and visual consumer; it does not own the evidence.
- **GlobalGrid2050:** catalogue/origin hub and federation topology.
- **Data-centres-gb:** demand-side evidence using the same evidence/identity contracts.
- **ChatGPT Audits:** unreviewed study and draft artefacts only.

## First graduation sequence

1. Human-review the evidence and transition contracts.
2. Freeze one-signal-silence and dual-register tests.
3. Extract interfaces from current PipelineNews runners without changing behaviour.
4. Add Companies and planning adapters against fixtures or reviewed compact exports only.
5. Produce a reviewed consumer summary and repair the GridAtlas pointer seam with golden sentinels.
6. Graduate one bounded artefact at a time; never copy this folder wholesale into a product repository.

The five-hour workflow re-tests this architecture against exact repository commits and generates a fuller timestamped candidate on its own quarantine branch.
