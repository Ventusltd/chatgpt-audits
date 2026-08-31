# Claude Company↔REPD progress handoff — 202608310116

> **REVIEW STATUS: UNREVIEWED**  
> Classification: mixed `observed` / `inferred`  
> Source: user-supplied Claude progress report. This is audit evidence, not a product finding.

## Reported execution boundary

Claude reports a read-only DuckDB 1.3.2 decode of the frozen Company↔REPD candidate Parquet. The stated task order is:

1. verify the contract;
2. run the collision check first;
3. apply the binding rule clause by clause and count survivors;
4. state clause 4 as an upper bound because incorporation dates are absent.

No product-repository write or live network request is claimed.

## Reported provisional result

- Candidate edges: **482,030**.
- Upper-bound bindings after the current clauses: **604**.
- Reduction: **99.87%**.

The value `604` remains provisional and must not be represented as a verified relationship count.

## Reported anomalies under investigation

1. The contract asserts `unknown_repd_refs: 0`, while the first decode measured **2,128**.
2. Claude then determined that the pinned commit was an ancestor but the project data occupied a different path at that historical point, so FK closure must be re-tested against the pinned spine rather than today's spine.
3. A possible extractor defect was identified: alphabetical matching may encounter `relationships` before `repd_ref`, potentially selecting a related project's reference instead of the intended top-level REPD reference.

## Required cross-checks for the ChatGPT audit swarm

- Treat 604 as an upper bound until exact historical-spine closure, collision and extraction tests pass.
- Reproduce collision testing before binding.
- Report counts surviving every clause.
- Distinguish observed register facts from inferred project-vehicle identity.
- Add a regression fixture containing both a top-level `repd_ref` and nested `relationships[*].repd_ref`.
- Require deterministic selection of the top-level field.
- Test the contract's `unknown_repd_refs: 0` assertion against the exact candidate producer commit and exact spine path.
- Feed a surviving Company event into PipelineNews only as a funding-lane fact after identity review. Funding alone must remain silent.
