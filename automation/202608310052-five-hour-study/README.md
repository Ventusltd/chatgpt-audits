# 202608310052 five-hour quarantined study automation

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`  
> This automation belongs only to `Ventusltd/chatgpt-audits`.

## Mission

Run five source-pinned checkpoints over the Ventus grid-intelligence repositories, with the PipelineNews timing/intelligence engine first. Produce evidence ledgers, conflicts, schemas, a reference state machine and a graduation backlog without changing or dispatching any product repository.

## Five checkpoints

| Hour | Focus | Main output |
|---:|---|---|
| 1 | Exact source manifest, repository inventory and workflow topology | `01-REPOSITORY-INVENTORY.*` |
| 2 | PipelineNews collectors, evidence, identity, scoring and publication coupling | `02-PIPELINENEWS-ENGINE-AUDIT.*` |
| 3 | Companies funding facts versus planning/procurement facts | `03-*` event-contract and evidence files |
| 4 | Re-test the copied Claude study against pinned source commits | `04-CLAUDE-CROSSCHECK-LEDGER.json` |
| 5 | Generate the quarantined PipelineNews vNext candidate | schemas, migration map, backlog, reference state machine and tests |

The workflow holds the run open for the full five-hour window and commits one checkpoint per hour to a new branch:

```text
audit/<London timestamp>-five-hour-<GitHub run id>
```

It never merges that branch and never opens a product pull request.

## Network and write boundary

Allowed:

- shallow, sparse, read-only Git snapshots of the explicitly listed public `Ventusltd/*` repositories;
- push of checkpoint commits to the run-specific branch in `Ventusltd/chatgpt-audits`;
- upload of the same audit output as a GitHub Actions artifact.

Forbidden:

- live Companies House, planning, news, RSS, map or scraper calls;
- package installation or package-registry access;
- writes, commits, pushes, workflow dispatches, releases or Pages builds in any product repository;
- treating absence as evidence;
- representing a commercial window as an observed fact.

## Quarantine gates

`verify_quarantine.py` fails the run when:

- any changed path escapes the timestamped `AUTOMATION-RUNS` folder;
- a product snapshot changes after its initial content hash;
- a generated file lacks an `UNREVIEWED` label;
- binary output, bytecode, symlinks, secret-like strings or oversized files appear;
- a required checkpoint artefact is missing.

## PipelineNews vNext doctrine encoded by the candidate

```text
source collectors
  -> append-only evidence ledger
    -> reviewed identity binder
      -> funding lane + procurement lane
        -> dual-register timing state machine
          -> human-reviewed read model
```

One signal remains silent. News may corroborate and explain; it does not manufacture the register fact. Retractions and contradictions are first-class. `PUBLISHED` is deliberately forbidden in the audit reference implementation.

## Files

- `study-plan.json` — repositories, sparse source surfaces, phases, limits and hard gates.
- `run_study.py` — source snapshotter, deterministic scanners, cross-checker and vNext generator.
- `verify_quarantine.py` — write-boundary, source-integrity, labelling and output checks.
- `.github/workflows/202608310052-five-hour-quarantined-study.yml` — five-hour orchestration.

Nothing here is trusted until a human reviews and graduates a bounded artefact into its owning product repository.
