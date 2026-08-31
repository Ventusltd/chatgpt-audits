# Overnight swarm lane — adversarial-invariants

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Execute deterministic adversarial sequences proving one-signal silence, review gates and unambiguous binding extraction.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |

## Findings

### INFO — The dual-register reference engine survived 100,000 deterministic adversarial sequences

Classification: `observed`

Executed 1,551,382 transitions with zero invariant failures. This proves the reference logic only; it does not prove current PipelineNews implements it.


### HIGH — News-only events cannot create funding or procurement state

Classification: `observed`

The property test applies 1,000 news events after identity review and remains IDENTITY_REVIEWED.


## Metrics

```json
{
  "adversarial": {
    "review_status": "UNREVIEWED",
    "classification": "observed",
    "sequences": 100000,
    "transitions": 1551382,
    "failures": 0
  },
  "category_counts": {
    "conflict": 22,
    "news": 1150,
    "procurement": 21,
    "review": 7
  }
}
```

Nothing in this lane authorises installation or publication.
