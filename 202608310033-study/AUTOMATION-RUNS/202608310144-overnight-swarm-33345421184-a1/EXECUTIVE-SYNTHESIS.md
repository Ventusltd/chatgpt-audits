# Overnight parallel audit swarm — executive synthesis

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Created: `2026-08-31T01:44:42.777660+01:00`

Completed lanes: **12 / 12**

Missing required lanes: **none**

## Evidence volume

| Lane | Evidence rows | Findings | Snapshot failures |
|---|---:|---:|---:|
| adversarial-invariants | 1,200 | 2 | 0 |
| companies-binding-forensics | 1,200 | 3 | 0 |
| pipelinenews-collectors | 897 | 3 | 0 |
| pipelinenews-identity | 1,200 | 3 | 0 |
| pipelinenews-timing-engine | 1,200 | 3 | 0 |
| claude-claim-crosscheck | 58 | 1 | 0 |
| federated-data-contracts | 1,200 | 2 | 0 |
| gridatlas-seam-contracts | 1,200 | 3 | 0 |
| cvaa-vaccine-coverage | 1,200 | 2 | 0 |
| datacentre-demand-intelligence | 1,200 | 2 | 0 |
| globalgrid-federation-topology | 1,200 | 1 | 0 |
| workflow-governance | 1,200 | 2 | 0 |

## Highest-priority findings

### HIGH — News-only events cannot create funding or procurement state

Lane: `adversarial-invariants` · Classification: `observed`

The property test applies 1,000 news events after identity review and remains IDENTITY_REVIEWED.

### HIGH — High-impact Claude claims now have explicit support states

Lane: `claude-claim-crosscheck` · Classification: `observed`

Route drift is source-supported; the 604 binding count remains handoff-only; the unknown-ref mismatch requires exact historical-spine reproduction; exact-ref performance is design-only until browser proof exists.

### HIGH — The provisional decode conflicts with the zero-unknown-REPD contract

Lane: `companies-binding-forensics` · Classification: `contradicted`

Claude reported 2,128 unknown REPD references against a contract asserting zero. This may be path/pin mismatch, but it is a failed closure until reproduced against the exact producer spine.

### HIGH — A nested relationship reference must never replace the top-level project identity

Lane: `companies-binding-forensics` · Classification: `inferred`

The generated regression fixture proves the safe rule: read only the top-level repd_ref and reject a nested-only record.

### HIGH — The reported 604 bindings remain an upper bound

Lane: `companies-binding-forensics` · Classification: `inferred`

The handoff reports 482,030 candidate edges reduced to 604, but incorporation dates are absent and historical-spine/FK closure is still being checked. The number must not enter a product read model yet.

### HIGH — Privacy exclusions are present and must remain hard gates

Lane: `datacentre-demand-intelligence` · Classification: `observed`

No individual director/PSC or residential data is needed to infer demand-side procurement timing.

### HIGH — Compact Parquet/DuckDB consumer boundaries are repeatedly stated

Lane: `federated-data-contracts` · Classification: `observed`

The repositories contain explicit compactness, hashing and ownership language. The vNext intelligence engine should consume only reviewed relationship/event tables, never a company-master dump.

### HIGH — Cross-repository seams are the highest transition risk

Lane: `globalgrid-federation-topology` · Classification: `inferred`

Observed 25 directed repository-reference edges in the selected source surface. These references should have executable producer/consumer contract tests.

### HIGH — Consumers and producer evidence contain different GridAtlas route generations

Lane: `gridatlas-seam-contracts` · Classification: `observed`

Observed 12 stale-root-shaped URL occurrence(s) and 0 stable `/gridatlas/atlas/` occurrence(s). Runtime 404 is not asserted by this offline lane; the source-level route drift is proven.

### HIGH — News eligibility is explicitly separate from relationship context

Lane: `pipelinenews-identity` · Classification: `observed`

Several paths encode eligible_for_news_signal. A related mention must never become project identity or a register fact.

### HIGH — News is corroboration, not a register fact

Lane: `pipelinenews-timing-engine` · Classification: `inferred`

Current news code is rich enough to explain events, but allowing headlines to create a lane would collapse the stated commercial discipline.

### HIGH — Funding and procurement must remain separate authoritative lanes

Lane: `pipelinenews-timing-engine` · Classification: `inferred`

The scanned repositories contain funding/account and planning/procurement language, but the commercial window must only emerge after reviewed identity and both observed lanes.

## What has been built

- Source-pinned, parallel specialist evidence rather than one serial narrative.
- A quarantined PipelineNews vNext schema and reference-test candidate.
- A 100,000-sequence adversarial state-machine proof when the lane completed.
- A nested-relationship REPD identity regression fixture.
- A route-drift matrix across PipelineNews, Companies, GridAtlas and GlobalGrid2050.
- A ranked human graduation queue.

No product repository was changed or dispatched.
