# Overnight swarm lane — pipelinenews-timing-engine

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Build and adversarially test the dual-register funding plus procurement timing state machine.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |
| spiders | `5575e70a2820` | 51 | 213,357 |

## Findings

### HIGH — Funding and procurement must remain separate authoritative lanes

Classification: `inferred`

The scanned repositories contain funding/account and planning/procurement language, but the commercial window must only emerge after reviewed identity and both observed lanes.

- `companies@200e9b3a5c2f:README.md:3` — Companies House public-data processing for Deploy Net Zero.
- `companies@200e9b3a5c2f:README.md:5` — The repository retains reviewed acquisition and accounts-extraction code. The current recovery checkpoint, `202608281337`, builds a key-only relationship-and-report candidate; it does not publish or overwrite a stable dataset.
- `companies@200e9b3a5c2f:README.md:9` — GitHub Actions provides the transient compute, while the GitHub REST API verifies run and retained-artifact provenance. The planned Companies House bulk archive is downloaded once into temporary runner storage; the Companies House REST API is not used. The expected 294,904-company selected-union closure is a validation measure, not a durable company dataset; the aggregate report separately records the full number of…
- `companies@200e9b3a5c2f:README.md:21` — The retained annual workflow documents the earlier rolling electronic-accounts process. It is audit history only and must not be dispatched as a publication route. Checkpoint `202608281112` is the sole authorised Companies recovery path.
- `companies@200e9b3a5c2f:README.md:25` — - Companies House is credited as the public-register source.
- `companies@200e9b3a5c2f:README.md:31` — - Raw Companies House archives are processed in temporary Actions storage and are not committed.

### HIGH — News is corroboration, not a register fact

Classification: `inferred`

Current news code is rich enough to explain events, but allowing headlines to create a lane would collapse the stated commercial discipline.

- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:25` — PIPELINENEWS_COMMIT: "35f35ada161223fb3ee19e525664ee7f17df1ddd"
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:89` — test "$(jq -r '.inputs.pipelinenews_commit' "$CONTRACT")" = "$PIPELINENEWS_COMMIT"
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:168` — repository: Ventusltd/pipelinenews
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:169` — ref: ${{ env.PIPELINENEWS_COMMIT }}
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:188` — test "$(git -C work/repd-source rev-parse HEAD)" = "$PIPELINENEWS_COMMIT"
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:307` — repository: Ventusltd/pipelinenews

### MEDIUM — Retractions, contradictions and staleness require explicit transitions

Classification: `inferred`

The vNext state machine must preserve negative changes rather than overwrite the latest state.

- `companies@200e9b3a5c2f:.github/workflows/202608300327-bound-hourly-gridatlas-link-mission.yml:74` — 'mission window guard',
- `companies@200e9b3a5c2f:.github/workflows/202608300435-five-hour-key-only-atlas-watchdog.yml:36` — - name: Enforce bounded five-hour mission window
- `companies@200e9b3a5c2f:.github/workflows/202608300435-five-hour-key-only-atlas-watchdog.yml:37` — id: window
- `companies@200e9b3a5c2f:.github/workflows/202608300435-five-hour-key-only-atlas-watchdog.yml:51` — if: steps.window.outputs.active == 'true'
- `companies@200e9b3a5c2f:.github/workflows/202608300435-five-hour-key-only-atlas-watchdog.yml:59` — if: steps.window.outputs.active == 'true'
- `companies@200e9b3a5c2f:.github/workflows/202608300435-five-hour-key-only-atlas-watchdog.yml:86` — if: steps.window.outputs.active == 'true'

## Metrics

```json
{
  "category_counts": {
    "funding": 302,
    "news": 753,
    "procurement": 7,
    "review": 97,
    "timing": 41
  },
  "funding_evidence_lines": 302,
  "procurement_evidence_lines": 7
}
```

Nothing in this lane authorises installation or publication.
