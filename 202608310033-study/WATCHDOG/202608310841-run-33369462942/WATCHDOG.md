# Hourly audit watchdog

> **REVIEW STATUS: UNREVIEWED**  
> Classification: mixed `observed` / `inferred`  
> Product repositories were inspected read-only. Automatic re-runs are restricted to the latest failed `Ventusltd/chatgpt-audits` workflow.

Checked: `2026-08-31T08:41:15.061797+01:00` Europe/London  
Five-hour controller: **NOT_SEEN_IN_LOOKBACK**  
Overnight swarm: **COMPLETED_SUCCESS**  
Actionable audit failures: **0**  
Automatic audit re-runs requested: **0**  
Product failures observed read-only: **3**  
Pages/platform observations separated from actionable failures: **29**  
Potentially stalled runs: **0**

## Repository status

| Repository | Active | Audit-actionable | Product observations | Pages noise | Stalled | Re-runs | API |
|---|---:|---:|---:|---:|---:|---:|---|
| `Ventusltd/chatgpt-audits` | 1 | 0 | 0 | 23 | 0 | 0 | OK |
| `Ventusltd/pipelinenews` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/companies` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/gridatlas` | 0 | 0 | 0 | 6 | 0 | 0 | OK |
| `Ventusltd/data-gridatlas` | 0 | 0 | 3 | 0 | 0 | 0 | OK |
| `Ventusltd/globalgrid2050` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/spiders` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/cvaa` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/data-centres-gb` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/data-gb-electricity` | 0 | 0 | 0 | 0 | 0 | 0 | OK |

## Actionable audit failures

No latest audit workflow is presently in a repair-eligible failed state.

## Product-repository observations

Observed `3` non-Pages product failures/cancellations. They are evidence only; this audit controller has no mutation or dispatch authority there.
- `Ventusltd/data-gridatlas` run `33360755252` — failure: Hourly watchdog b335aca6c9c6b028b358c419410e4cf5b2035c2e.
- `Ventusltd/data-gridatlas` run `33341883582` — failure: Hourly watchdog b335aca6c9c6b028b358c419410e4cf5b2035c2e.
- `Ventusltd/data-gridatlas` run `33335301216` — failure: Hourly watchdog b335aca6c9c6b028b358c419410e4cf5b2035c2e.

## Repair boundary

- Only the latest failed audit workflow may be re-run, up to attempt 3.
- A newer active or successful run suppresses repair of an older failed run with the same workflow name.
- Product-repository runs are evidence only: no dispatch, re-run, commit, release or Pages mutation is allowed.
- Pages build/deployment noise is counted separately and is not labelled an unresolved audit failure.
- Deterministic source defects are sent to the separate repair diagnosis workflow; this watchdog does not rewrite source from logs.
- Absence from this bounded lookback is not evidence that no older failure exists.
