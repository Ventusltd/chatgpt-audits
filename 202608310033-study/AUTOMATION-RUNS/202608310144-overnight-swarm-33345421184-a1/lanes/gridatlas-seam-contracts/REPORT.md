# Overnight swarm lane — gridatlas-seam-contracts

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Compare exact producer and consumer routes, pointer contracts and golden REPD sentinels.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| gridatlas | `cd4ef33430a3` | 111 | 805,194 |
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |
| globalgrid2050 | `6afd5dea7216` | 2,465 | 546,141,474 |

## Findings

### HIGH — Consumers and producer evidence contain different GridAtlas route generations

Classification: `observed`

Observed 12 stale-root-shaped URL occurrence(s) and 0 stable `/gridatlas/atlas/` occurrence(s). Runtime 404 is not asserted by this offline lane; the source-level route drift is proven.

- `companies@200e9b3a5c2f:state/atlas-v9-link-audit.json:9` — 
- `companies@200e9b3a5c2f:state/atlas-v9-link-contract.json:3` — 
- `companies@200e9b3a5c2f:state/atlas-v9-link-contract.json:14` — 
- `companies@200e9b3a5c2f:state/atlas-v9-link-contract.json:18` — 
- `companies@200e9b3a5c2f:state/atlas-v9-link-contract.json:40` — 
- `globalgrid2050@6afd5dea7216:homepage_versions/202608291526-globalgrid2050/manifest.json:5` — 

### MEDIUM — Producer and receiver contracts discuss repd_ref and technology differently

Classification: `observed`

The lane records exact references to both parameters so a human can decide whether technology is identity or corroborating metadata.

- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:104` — test "$(jq -c '[.relationship_schema[].name]' "$CONTRACT")" = '["company_number","repd_ref","evidence_type"]'
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:105` — test "$(jq -c '[.solar_relationship_schema[].name]' "$CONTRACT")" = '["company_number","repd_ref","evidence_type"]'
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:411` — test "$(jq -c '.datasets.company_repd_candidates.schema_readback | map(.name)' "$manifest")" = '["company_number","repd_ref","evidence_type"]'
- `companies@200e9b3a5c2f:.github/workflows/202608281337-compact-parquet-companies-candidate.yml:412` — test "$(jq -c '.datasets.solar_company_repd_relationships.schema_readback | map(.name)' "$manifest")" = '["company_number","repd_ref","evidence_type"]'
- `companies@200e9b3a5c2f:.github/workflows/202608300312-sync-gridatlas-v9-link-contract.yml:46` — test "$(jq -c '[.relationship_schema[].name]' "$COMPANIES_CONTRACT")" = '["company_number","repd_ref","evidence_type"]'
- `companies@200e9b3a5c2f:.github/workflows/202608300312-sync-gridatlas-v9-link-contract.yml:47` — test "$(jq -c '[.solar_relationship_schema[].name]' "$COMPANIES_CONTRACT")" = '["company_number","repd_ref","evidence_type"]'

### INFO — Beacon Fen and East Pye are available as federation sentinels

Classification: `observed`

The exact source evidence contains 13599/Beacon Fen and 17494/East Pye. A graduated fix should prove both through the real producer and stable receiver.

- `companies@200e9b3a5c2f:.github/workflows/202608300312-sync-gridatlas-v9-link-contract.yml:22` — GOLDEN_REPD_REF: '13599'
- `companies@200e9b3a5c2f:state/atlas-v9-link-audit.json:9` — "golden_url": "https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=13599",
- `companies@200e9b3a5c2f:state/atlas-v9-link-contract.json:13` — "golden_repd_ref": "13599",
- `companies@200e9b3a5c2f:state/atlas-v9-link-contract.json:14` — "golden_url": "https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=13599",
- `companies@200e9b3a5c2f:tests/test_202608271507_bounded_companies_house.py:321` — "repd_ref": "13599",
- `companies@200e9b3a5c2f:tests/test_202608271507_bounded_companies_house.py:322` — "gg_project_id": "GG2050-REPD-13599",

## Metrics

```json
{
  "route_counts": {
    "OTHER_GRIDATLAS_ROUTE": 15,
    "STALE_ROOT_RELEASE_SHAPE": 12
  },
  "gridatlas_url_occurrences": 27
}
```

Nothing in this lane authorises installation or publication.
