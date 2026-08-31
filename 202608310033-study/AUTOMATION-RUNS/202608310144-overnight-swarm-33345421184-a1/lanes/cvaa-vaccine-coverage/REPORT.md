# Overnight swarm lane — cvaa-vaccine-coverage

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Run CVAA self-tests where possible and map vaccines to the observed federation failure modes.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| cvaa | `d2ebc01f6eab` | 47 | 205,030 |
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |
| gridatlas | `cd4ef33430a3` | 111 | 805,194 |

## Findings

### INFO — CVAA registry and consumer snapshots were executed read-only where possible

Classification: `observed`

A non-zero consumer result is retained as a finding, not silently baselined. The audit swarm does not mutate CVAA or consumer repositories.


### MEDIUM — Federation pointer drift and nested-identity ambiguity deserve executable vaccines

Classification: `inferred`

The strongest overnight candidates are a consumer-pointer-current vaccine and a top-level-identity-only vaccine.

- `companies@200e9b3a5c2f:README.md:5` — The repository retains reviewed acquisition and accounts-extraction code. The current recovery checkpoint, `202608281337`, builds a key-only relationship-and-report candidate; it does not publish or overwrite a stable dataset.
- `companies@200e9b3a5c2f:README.md:17` — Publication is restricted to an immutable candidate branch. `main`, `data/current/`, Pages and releases remain unchanged. Historical workflows live under `.github/workflow-history/` as inert audit evidence; checkpoint `202608281337` is the sole active publication path.
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:387` — test ! -e data/current
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:453` — if git diff --cached --name-only | grep -Eq '(^|/)current/|(^|/)pages/|(^|/)releases/'; then
- `companies@200e9b3a5c2f:.github/workflows/202608300312-sync-gridatlas-v9-link-contract.yml:81` — release_id="$(jq -r '.current.release_id // empty' /tmp/atlas-state.json)"
- `companies@200e9b3a5c2f:.github/workflows/202608300312-sync-gridatlas-v9-link-contract.yml:82` — live_url="$(jq -r '.current.live_url // empty' /tmp/atlas-state.json)"

## Metrics

```json
{
  "execution_count": 5,
  "nonzero": 4,
  "category_counts": {
    "amnesia": 44,
    "boundary": 389,
    "determinism": 482,
    "pointer": 104,
    "vaccine": 181
  }
}
```

Nothing in this lane authorises installation or publication.
