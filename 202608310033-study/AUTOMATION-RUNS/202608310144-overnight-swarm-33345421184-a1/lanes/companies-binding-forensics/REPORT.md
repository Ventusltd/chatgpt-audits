# Overnight swarm lane — companies-binding-forensics

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Cross-check collision order, historical spine closure, top-level repd_ref extraction and upper-bound binding claims.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| companies | `200e9b3a5c2f` | 75 | 950,259 |
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| gridatlas | `cd4ef33430a3` | 111 | 805,194 |

## Findings

### HIGH — The reported 604 bindings remain an upper bound

Classification: `inferred`

The handoff reports 482,030 candidate edges reduced to 604, but incorporation dates are absent and historical-spine/FK closure is still being checked. The number must not enter a product read model yet.


### HIGH — The provisional decode conflicts with the zero-unknown-REPD contract

Classification: `contradicted`

Claude reported 2,128 unknown REPD references against a contract asserting zero. This may be path/pin mismatch, but it is a failed closure until reproduced against the exact producer spine.

### HIGH — A nested relationship reference must never replace the top-level project identity

Classification: `inferred`

The generated regression fixture proves the safe rule: read only the top-level repd_ref and reject a nested-only record.


## Metrics

```json
{
  "category_counts": {
    "binding": 378,
    "collision": 43,
    "company_number": 179,
    "historical_pin": 66,
    "parquet_duckdb": 435,
    "relationships": 43,
    "repd_ref": 56
  },
  "handoff_present": true,
  "extractor_tests": {
    "review_status": "UNREVIEWED",
    "tests": 3,
    "passed": 3,
    "classification": "observed"
  },
  "reported_candidate_edges": 482030,
  "reported_upper_bound": 604
}
```

Nothing in this lane authorises installation or publication.
