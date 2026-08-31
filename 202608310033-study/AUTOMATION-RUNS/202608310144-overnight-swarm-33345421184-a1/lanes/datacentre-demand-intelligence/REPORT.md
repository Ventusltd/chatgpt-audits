# Overnight swarm lane — datacentre-demand-intelligence

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Map the demand-side intelligence chain using the same evidence and identity discipline.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| data-centres-gb | `c5dfdee3ba5d` | 32 | 228,929 |
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| globalgrid2050 | `6afd5dea7216` | 2,465 | 546,141,474 |

## Findings

### MEDIUM — Demand-side intelligence can reuse evidence and identity contracts

Classification: `inferred`

Data-centre evidence should use source receipts, site identity, company bindings, abstention and compact Parquet outputs just like generation-side intelligence.

- `data-centres-gb@c5dfdee3ba5d:README.md:1` — # Data Centres GB
- `data-centres-gb@c5dfdee3ba5d:README.md:3` — Open-source, provenance-first tooling for compiling United Kingdom data-centre source records into compact Parquet, DuckDB-readable relationship tables and a small map export.
- `data-centres-gb@c5dfdee3ba5d:README.md:21` — data/facilities/generation=202608281053/source=OPENSTREETMAP/osm-data-centre-elements-v1.parquet
- `data-centres-gb@c5dfdee3ba5d:README.md:22` — data/relationships/generation=202608281053/data-centre-company-relationships-v1.parquet
- `data-centres-gb@c5dfdee3ba5d:README.md:23` — exports/202608281053-osm-data-centres.geojson
- `data-centres-gb@c5dfdee3ba5d:README.md:24` — reports/202608281053-osm-data-centres-audit.json

### HIGH — Privacy exclusions are present and must remain hard gates

Classification: `observed`

No individual director/PSC or residential data is needed to infer demand-side procurement timing.

- `data-centres-gb@c5dfdee3ba5d:.github/workflows/202608281626-osm-data-centres-candidate.yml:9` — - "contracts/202608281626-osm-overpass-retry-privacy.json"
- `data-centres-gb@c5dfdee3ba5d:.github/workflows/202608281626-osm-data-centres-candidate.yml:62` — $'A\tcontracts/202608281626-osm-overpass-retry-privacy.json' \
- `data-centres-gb@c5dfdee3ba5d:.github/workflows/202608281702-osm-data-centres-candidate.yml:68` — test "$(git rev-parse HEAD:contracts/202608281626-osm-overpass-retry-privacy.json)" = "d1952c80aed8e3407731bfe859c74f3ee15c9812"
- `data-centres-gb@c5dfdee3ba5d:.github/workflows/202608281702-osm-data-centres-candidate.yml:107` — - name: Run offline hostile fixture, privacy and indexed-query suites
- `data-centres-gb@c5dfdee3ba5d:build/python/202608271727-build-data-centres-intelligence.py:479` — with tempfile.TemporaryDirectory(prefix=f"dcgb-{GENERATION}-", dir=output_root) as temporary_name:
- `data-centres-gb@c5dfdee3ba5d:build/python/202608281626-osm-overpass-retry.py:18` — REPAIR_CONTRACT_REL = Path("contracts/202608281626-osm-overpass-retry-privacy.json")

## Metrics

```json
{
  "category_counts": {
    "datacentre": 187,
    "demand": 155,
    "identity": 98,
    "parquet": 261,
    "privacy": 18,
    "source": 481
  }
}
```

Nothing in this lane authorises installation or publication.
