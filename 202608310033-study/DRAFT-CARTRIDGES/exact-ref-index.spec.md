# Cartridge spec — `exact-ref-index`

One page. Draft. Not installed.

| | |
|---|---|
| **id** | `uk-gazetteer-flyto` (a superseding generation of the existing cartridge, not a new id) |
| **draft** | `./exact-ref-index.js.txt` — anchored replacement blocks, not a whole file |
| **slot** | `replace-script` → `202608291818-place-postcode-search.js` |
| **parent** | `atlas/cartridges/202608301624-place-global-search-v9-5.js`, sha256 `b6497b437de52f68151a1bb22ccd95133d15c243c58eb9df1912fb36f38bcfca` |
| **delivery type** | `map-ready-geojson` — a static hash-pinned JSON lookup (not drawn) |
| **new data artefact** | `gridatlas/data/repd_ref_index_<gen>.json`, schema `gridatlas.repd-ref-index.v1` |

---

## 1. Purpose

Make a deep link resolve on any device, including a 1 GB phone on a poor connection.

Today the path is:

```
?repd_ref=13599
  -> receiveExactRepdDeepLink
     -> queryOfficialRepd
        -> runtime()
           -> verifyManifest()                         fetch + sha256, ~5 KB
           -> import @duckdb/duckdb-wasm@1.29.0        ~35.7 MB
           -> selectBundle + Worker + instantiate
        -> read_parquet(repd_projects_...parquet)      1.45 MB
     -> selectResult -> map.flyTo
```

At the 20 Mbit reference used by `data-gridatlas/tools/202608301930-fidelity.py`, the DuckDB runtime alone is
**14.3 s**, against a 15 s budget, before a single project byte moves. On a constrained device it is worse and can
exceed the receiver's own 60 s `waitForCapturedMap` ceiling.

After this cartridge:

```
?repd_ref=13599
  -> receiveExactRepdDeepLink
     -> loadRefIndex()      fetch + sha256, ~340 KB gzipped   ~0.15 s
     -> lookupExactRef()    O(1) object lookup
     -> selectResult -> map.flyTo
```

DuckDB is never instantiated for a deep link. It remains the free-text search engine, booted lazily on the first
typed query, exactly as today.

---

## 2. Feeding data source

Built from the existing pinned Parquet, at build time, in the existing `gridatlas/compiler/` pattern:

```
source     data/repd_projects_202608290716.parquet
           sha256 174040c37f3d63742d6fdd7af722a8cfdf3fb53de3ff85ff1142d22fdac4866b
rows       11,069   (unique_repd_refs 11,069 — the key is unique)
output     data/repd_ref_index_<gen>.json
schema     gridatlas.repd-ref-index.v1
```

Payload shape:

```json
{
  "schema": "gridatlas.repd-ref-index.v1",
  "generation": "202608290716",
  "rows": 11069,
  "parquet_sha256": "174040c37f3d63742d6fdd7af722a8cfdf3fb53de3ff85ff1142d22fdac4866b",
  "records": {
    "13599": ["Beacon Fen Energy Park", "solar", "awaiting construction", 500.0, -0.31, 52.84]
  }
}
```

Row form is an **array of six values**, not an object, deliberately: repeating six keys 11,069 times roughly doubles
the payload. Order is `[name, technology, status, capacity_mw, longitude, latitude]` and is asserted by the builder
test, not by a comment.

The `parquet_sha256` field is the safety catch: the cartridge asserts it equals the `PARQUET_SHA256` the search lane
already verifies, so the two lanes can never silently describe different universes.

---

## 3. Size and budget

| item | figure |
|---|---|
| raw JSON | 11,069 × ~95 B ≈ **1.05 MB** |
| gzip over the wire | **≈ 300–380 KB** |
| transfer at 20 Mbit | **≈ 0.15 s** |
| transfer at 3 Mbit (poor mobile) | ≈ 1.0 s |
| heap | one object of 11,069 six-element arrays ≈ 3–5 MB — negligible against the 400 MB cap |
| cartridge JS delta | ~3 KB added to a 17 KB parent; the 400,000 B cap is untouched |

**Do not reuse `data/repd_browser_registry_202608290716.json` for this.** It is 9,328,402 bytes — the full record set
including both address forms, both postcode forms, region, country, LPA, planning reference, operator, publication
state, both technology fields, the source row and its sha256. It would cost **3.7 s at 20 Mbit** and a much larger
heap for information a deep link does not need. Build the minimal index.

---

## 4. Behaviour changes

| | parent | this generation |
|---|---|---|
| deep-link resolution | DuckDB + Parquet | ref index first, DuckDB only as fallback |
| free-text search | DuckDB + Parquet | unchanged |
| gazetteer lanes | postcodes.io + Nominatim | unchanged |
| no safe map point | `status: 'FAILED'`, `dataset='failed'` | `status: 'RESOLVED_NOT_MAPPED'`, `dataset='resolved-unmapped'` |
| malformed ref | throws → `FAILED` | `status: 'MALFORMED'`, `dataset='malformed'` |
| ref not in universe | throws → `FAILED` | `status: 'NOT_FOUND'`, `dataset='not-found'` |
| no ref in URL | `status: 'ABSENT'`, no dataset attribute | `status: 'ABSENT'`, `dataset='absent'` |
| mapped success | `status: 'RESOLVED'`, `dataset='resolved'` | **identical** — deliberately preserved |

The last row matters: `atman/202608301624-verify-v9-5-search.mjs` waits on the literal string `'RESOLVED'` and then
asserts `repd_ref === '13599' && mapped === true`. Keeping that value makes the existing gate pass unchanged while
still separating "identity resolved but no geometry" from "failure".

---

## 5. Open points

1. **Generation bump.** The verifier asserts
   `window.__GRIDATLAS_PLACE_SEARCH__.generation === EXPECTED_SEARCH_GENERATION`. Both the cartridge constant and the
   workflow env must move together.
2. **Index staleness.** If the REPD Parquet is regenerated and the index is not, the `parquet_sha256` assertion fails
   and the cartridge falls back to the DuckDB lane — degraded, not broken. That is the intended failure mode, but the
   build must regenerate both in the same generation.
3. **Sharding.** Not needed at 11,069 rows. If the universe grows past ~50,000, shard by
   `repd_ref % 16` and fetch one shard; the cartridge structure already isolates that behind `loadRefIndex()`.
4. **`cache: 'force-cache'`.** The index is content-addressed by its filename generation, so aggressive caching is
   safe. The manifest and cartridges keep `no-store` as they do today.

---

## 6. Acceptance gate

1. every existing test in `atman/202608301624-verify-v9-5-search.mjs` passes unchanged, with
   `EXPECTED_SEARCH_GENERATION` set to the new generation
2. on `?repd_ref=13599`, `window.__GRIDATLAS_PLACE_SEARCH__.ref_index.verified === true` and
   `duckdb_booted_for === null` — **DuckDB was never instantiated**
3. `ref_index.ms` recorded and under 3,000 ms on the 375 × 667 cell
4. `?repd_ref=12780` (the invalid-geometry sentinel from the pipelinenews cartridge) yields
   `status: 'RESOLVED_NOT_MAPPED'` and `dataset.gridatlasRepdDeepLink === 'resolved-unmapped'`, and the map does not
   move to a false origin
5. `?repd_ref=99999999` yields `NOT_FOUND`; `?repd_ref=<40+ chars>` yields `MALFORMED`; neither throws
6. free-text search for `Beacon Fen` still returns `13599` first and still boots DuckDB (`duckdb_booted_for` set)
7. **negative test:** serve an index whose `parquet_sha256` is altered; assert the cartridge falls back to the
   DuckDB lane and the deep link still resolves
8. zero uncaught exceptions

---

## 7. Rollback

Revert `atlas/current.json` to the previous cartridge generation. The index artefact can stay on disk unused; it is
content-addressed and harmless. One file, one commit.
