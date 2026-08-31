# Claude live handoff — 202608310116

> **REVIEW STATUS: UNREVIEWED**
> Classification: mixed `observed` / `inferred`
> User-supplied progress report. This is supporting evidence for the timed audit only; it is not installed in any product repository.

## Observed progress supplied by Claude

Claude reports a read-only decoder over the frozen Company↔REPD candidate Parquet, with DuckDB 1.3.2, explicitly running a collision check before any binding rule and reporting clause-by-clause survival counts.

Reported headline result: **482,030 candidate edges → 604 upper-bound bindings**, a **99.87% reduction**.

Claude also reports an anomaly requiring resolution before reliance: the contract asserts `unknown_repd_refs: 0`, while the first measurement returned **2,128**. Claude then identified that the pin is an ancestor but the project data existed at a different path at that historical point, and began re-testing FK closure against the pinned spine rather than today's spine.

A possible extractor defect was also identified: `relationships` sorts before `repd_ref` alphabetically, so a generic matcher may have selected a related project's reference rather than the intended REPD reference. Claude was checking records containing relationships when this handoff was supplied.

## How the timed audit should use this

1. Treat **604 as an upper bound**, not a verified binding count, until the historical-spine FK closure and extractor ambiguity are resolved.
2. Reproduce the collision check before applying identity/binding rules.
3. Record clause-by-clause survivor counts rather than only the final number.
4. Keep observed Company-register evidence separate from inferred project-vehicle identity.
5. Do not interpret absence from the candidate table as evidence of no relationship.
6. Cross-check the claimed `unknown_repd_refs` contract against the exact source commit/path used to create the candidate.
7. Add a regression fixture where a row contains both `relationships` and `repd_ref`, proving the extractor chooses the intended field deterministically.
8. Feed verified organisation-level funding evidence into the PipelineNews funding lane only after identity review; it must not by itself create a commercial window.

## Priority impact

This materially strengthens checkpoints 2–4 of the five-hour programme. The most valuable immediate question is not whether 604 is small; it is whether those 604 survive exact identity, collision, historical-spine and provenance gates. Only the surviving reviewed set should be eligible to meet an independently observed planning/procurement signal in the PipelineNews dual-register timing engine.
