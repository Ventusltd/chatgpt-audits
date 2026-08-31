# Hourly audit watchdog

> **REVIEW STATUS: UNREVIEWED**  
> Classification: mixed `observed` / `inferred`  
> Product repositories were inspected read-only. Automatic re-runs are restricted to the latest failed `Ventusltd/chatgpt-audits` workflow.

Checked: `2026-08-31T01:56:15.865607+01:00` Europe/London  
Five-hour controller: **RUNNING**  
Overnight swarm: **COMPLETED_SUCCESS**  
Actionable audit failures: **0**  
Automatic audit re-runs requested: **0**  
Product failures observed read-only: **22**  
Pages/platform observations separated from actionable failures: **48**  
Potentially stalled runs: **0**

## Repository status

| Repository | Active | Audit-actionable | Product observations | Pages noise | Stalled | Re-runs | API |
|---|---:|---:|---:|---:|---:|---:|---|
| `Ventusltd/chatgpt-audits` | 3 | 0 | 0 | 25 | 0 | 0 | OK |
| `Ventusltd/pipelinenews` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/companies` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/gridatlas` | 0 | 0 | 6 | 17 | 0 | 0 | OK |
| `Ventusltd/data-gridatlas` | 0 | 0 | 8 | 0 | 0 | 0 | OK |
| `Ventusltd/globalgrid2050` | 0 | 0 | 4 | 0 | 0 | 0 | OK |
| `Ventusltd/spiders` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/cvaa` | 0 | 0 | 4 | 6 | 0 | 0 | OK |
| `Ventusltd/data-centres-gb` | 0 | 0 | 0 | 0 | 0 | 0 | OK |
| `Ventusltd/data-gb-electricity` | 0 | 0 | 0 | 0 | 0 | 0 | OK |

## Actionable audit failures

No latest audit workflow is presently in a repair-eligible failed state.

## Product-repository observations

Observed `22` non-Pages product failures/cancellations. They are evidence only; this audit controller has no mutation or dispatch authority there.
- `Ventusltd/gridatlas` run `33327666102` — failure: 202608301321 Build, deploy and verify modular GridAtlas v9.5.
- `Ventusltd/gridatlas` run `33327606684` — failure: 202608301321 Build, deploy and verify modular GridAtlas v9.5.
- `Ventusltd/gridatlas` run `33327360790` — failure: 202608301321 Build, deploy and verify modular GridAtlas v9.5.
- `Ventusltd/gridatlas` run `33320567458` — failure: 202608301321 Build, deploy and verify live Atlas composition.
- `Ventusltd/gridatlas` run `33317013772` — failure: 202608301321 Verify live Atlas composition.
- `Ventusltd/gridatlas` run `33316814805` — failure: 202608301321 GridAtlas bounded scope loop.
- `Ventusltd/data-gridatlas` run `33341883582` — failure: Hourly watchdog b335aca6c9c6b028b358c419410e4cf5b2035c2e.
- `Ventusltd/data-gridatlas` run `33335301216` — failure: Hourly watchdog b335aca6c9c6b028b358c419410e4cf5b2035c2e.
- `Ventusltd/data-gridatlas` run `33326921334` — failure: 202608301931 Layer fidelity, V8 origin vs V9 delivery.
- `Ventusltd/data-gridatlas` run `33326870409` — failure: Current integrity cfb0dbc3212b6da2906788289808d205ea21b83f.
- `Ventusltd/data-gridatlas` run `33326870235` — failure: Hourly watchdog cfb0dbc3212b6da2906788289808d205ea21b83f.
- `Ventusltd/data-gridatlas` run `33326661920` — failure: Automation contract guard cd14104231c39acba3f5bbbb57e842ad34f925fd.

## Repair boundary

- Only the latest failed audit workflow may be re-run, up to attempt 3.
- A newer active or successful run suppresses repair of an older failed run with the same workflow name.
- Product-repository runs are evidence only: no dispatch, re-run, commit, release or Pages mutation is allowed.
- Pages build/deployment noise is counted separately and is not labelled an unresolved audit failure.
- Deterministic source defects are sent to the separate repair diagnosis workflow; this watchdog does not rewrite source from logs.
- Absence from this bounded lookback is not evidence that no older failure exists.
