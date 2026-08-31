# Overnight swarm lane — pipelinenews-collectors

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Map every current collector, source closure, acquisition bound and retention rule.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |

## Findings

### MEDIUM — Current discovery runners are large orchestration units

Classification: `observed`

Observed 2 discovery runners above 30 kB. Extraction should preserve behaviour while separating acquisition, evidence and identity.

- `audit@:discovery/javascript/202608270844-live-news-runner.mjs:` — 
- `audit@:discovery/javascript/202608272130-sector-intelligence-runner.mjs:` — 

### INFO — Network and retention limits are explicitly encoded

Classification: `observed`

Request counts, response-byte bounds, timeouts and zero/full-body retention rules appear in the current source evidence.

- `pipelinenews@83d9c430b283:.github/workflows/202608271600-mobile-ui-comparator.yml:173` — assert.equal(manifest.execution.cell_record_max_bytes, 262144);
- `pipelinenews@83d9c430b283:.github/workflows/202608271620-mobile-ui-comparator.yml:178` — assert.equal(manifest.execution.cell_record_max_bytes, 262144);
- `pipelinenews@83d9c430b283:.github/workflows/202608271631-mobile-ui-comparator.yml:178` — assert.equal(manifest.execution.cell_record_max_bytes, 262144);
- `pipelinenews@83d9c430b283:.github/workflows/202608271638-mobile-ui-comparator.yml:178` — assert.equal(manifest.execution.cell_record_max_bytes, 262144);
- `pipelinenews@83d9c430b283:.github/workflows/202608271656-mobile-ui-comparator.yml:178` — assert.equal(manifest.execution.cell_record_max_bytes, 262144);
- `pipelinenews@83d9c430b283:.github/workflows/202608282044-federated-relationship-candidate.yml:186` — maximum_contract_bytes: 16384,

### MEDIUM — Frozen and approved evidence is mixed with runner code

Classification: `observed`

Hard-coded articles, gazetteers or frozen generic feeds are present. They should become separately hashed fixtures or reviewed ledgers, not disappear.

- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/discoveryv1/data/discovery_mentions.json:52` — "reason": "CLOSED_GAZETTEER_GATES_PASSED",
- `pipelinenews@83d9c430b283:build/javascript/202608272130-verify-v8-fast-browser.mjs:384` — assert.equal(sha256(genericBytes), contract.frozen_generic_news.sha256);
- `pipelinenews@83d9c430b283:build/javascript/202608272130-verify-v8-fast-browser.mjs:387` — assert.equal(manifest.outputs.some(({ path: relative }) => relative === contract.frozen_generic_news.path), false);
- `pipelinenews@83d9c430b283:discovery/javascript/202608270844-bbc-enrichment.mjs:454` — return Object.freeze({ outcome: 'ABSTAIN', reason: matches.length ? 'AMBIGUOUS_IDENTITY' : 'NO_CLOSED_GAZETTEER_MATCH', repd_ref: null });
- `pipelinenews@83d9c430b283:discovery/javascript/202608270844-live-news-runner.mjs:40` — const APPROVED_ARTICLES = Object.freeze([
- `pipelinenews@83d9c430b283:discovery/javascript/202608270844-live-news-runner.mjs:292` — 'closed_gazetteer',

## Metrics

```json
{
  "large_runner_count": 2,
  "large_runners": [
    {
      "path": "discovery/javascript/202608270844-live-news-runner.mjs",
      "bytes": 54293
    },
    {
      "path": "discovery/javascript/202608272130-sector-intelligence-runner.mjs",
      "bytes": 45523
    }
  ],
  "category_counts": {
    "contract_schema": 156,
    "deployment_gate": 305,
    "hardcoded_evidence": 28,
    "network_call": 120,
    "request_bound": 101,
    "retention_rule": 128,
    "source_closure": 59
  }
}
```

Nothing in this lane authorises installation or publication.
