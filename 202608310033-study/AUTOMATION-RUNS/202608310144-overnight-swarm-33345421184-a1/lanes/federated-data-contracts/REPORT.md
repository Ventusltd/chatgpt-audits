# Overnight swarm lane — federated-data-contracts

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Inventory Parquet, DuckDB, manifest, schema, ownership and compact-consumer boundaries.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| data-gridatlas | `b335aca6c9c6` | 32 | 485,659 |
| data-centres-gb | `c5dfdee3ba5d` | 32 | 228,929 |
| data-gb-electricity | `7c492745c974` | 472 | 98,041,589 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |

## Findings

### HIGH — Compact Parquet/DuckDB consumer boundaries are repeatedly stated

Classification: `observed`

The repositories contain explicit compactness, hashing and ownership language. The vNext intelligence engine should consume only reviewed relationship/event tables, never a company-master dump.

- `companies@200e9b3a5c2f:README.md:7` — ## Compact relationship candidate
- `companies@200e9b3a5c2f:README.md:13` — - a compact aggregate report, bounded manifest, DuckDB audit and source evidence.
- `companies@200e9b3a5c2f:README.md:15` — Parquet is written with DuckDB 1.3.2 and ZSTD compression, then independently read back against an exact three-column schema, composite keys, a dataset-level semantic digest and whole-file SHA receipts. Each file is hard-capped at 20 MB and the durable closure at 30 MB total. Descriptive fields, technology, row-level repository provenance and per-row digests are forbidden from the bridges; exact source commits and p…
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:7` — - .github/workflows/202608281337-compact-parquet-companies-candidate.yml
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:9` — - build/python/202608281337-compact-parquet-companies.py
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:10` — - contracts/202608281337-compact-parquet-companies.json

### MEDIUM — Manifests and hashes are common but seam-level closure still matters

Classification: `observed`

A file hash proves bytes, not that producer and consumer agree on identifiers, schema and validity windows.

- `companies@200e9b3a5c2f:README.md:13` — - a compact aggregate report, bounded manifest, DuckDB audit and source evidence.
- `companies@200e9b3a5c2f:README.md:15` — Parquet is written with DuckDB 1.3.2 and ZSTD compression, then independently read back against an exact three-column schema, composite keys, a dataset-level semantic digest and whole-file SHA receipts. Each file is hard-capped at 20 MB and the durable closure at 30 MB total. Descriptive fields, technology, row-level repository provenance and per-row digests are forbidden from the bridges; exact source commits and p…
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:74` — test "$(sha256sum .github/workflow-history/202608281112-compact-parquet-companies-candidate.yml | cut -d' ' -f1)" = 0cf0be7d09137a71e77be455966d2f1b342a3540c147867edeee9eab2013aafa
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:103` — test "$(jq -r '.outputs.manifest' "$CONTRACT")" = manifest-compact-v1.json
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:111` — test "$(jq '[.relationship_schema[].name] | map(select(. == "technology" or . == "relationship_json" or . == "relationship_sha256" or contains("repository") or contains("commit") or contains("name") or contains("url"))) | length' "$CONTRACT")" -eq 0
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:131` — {"name":"companies-plan-202608272155-33123064395","digest":"sha256:5458cb47d45107be3468472da15d02f18e0b5c0992f10c594af6897f2aea8aaa"},

## Metrics

```json
{
  "category_counts": {
    "compact_boundary": 43,
    "duckdb": 77,
    "manifest": 577,
    "ownership": 41,
    "parquet": 273,
    "schema": 189
  }
}
```

Nothing in this lane authorises installation or publication.
