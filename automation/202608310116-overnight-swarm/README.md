# 202608310116 overnight audit swarm

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`

This is the parallel successor to the five-hour serial audit. It exists only in `Ventusltd/chatgpt-audits` and cannot mutate or dispatch a product repository.

## Execution model

1. Resolve one exact commit manifest for all nine source repositories.
2. Fan out twelve source-pinned specialist lanes, with a maximum of twelve parallel runners.
3. Preserve every lane as a 90-day Actions artefact, including incomplete evidence.
4. Aggregate once into a run-specific `audit/<timestamp>-overnight-swarm-<run>-a<attempt>` branch.
5. Execute schema, quarantine, top-level identity and 100,000-sequence timing-engine gates.
6. Run hourly during the bounded 31 August 2026 overnight window.

## Highest-priority lanes

- PipelineNews collectors and source closure.
- PipelineNews identity and abstention.
- Dual-register funding plus procurement timing engine.
- Company↔REPD collision, historical-spine and nested-reference forensics.
- GridAtlas producer/consumer route contracts and golden sentinels.
- Claude claim cross-check.
- 100,000 deterministic adversarial state transitions.

## Controller integrity

The five Python modules are stored as a compressed, split payload because the controller is generated and verified as one unit. `assemble_controller.py` requires:

- all eight named parts;
- the base64 stream SHA-256;
- the compressed archive SHA-256;
- the exact five-file closure;
- the SHA-256 of every extracted source file;
- no links or path traversal.

The readable hashes are in `controller-manifest.json`. Every run assembles into ephemeral runner storage and recompiles all modules before use.

## Boundaries

Allowed: read-only Git transport to explicitly whitelisted public Ventus repositories, audit artefacts, and run-specific audit branches.

Forbidden: product writes, product workflow dispatches, live Companies House/planning/news/map/scraper calls, package installation, raw company dumps, publication, and treating absence as evidence.
