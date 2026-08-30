# DATA-DELIVERY-PLAN

Heavy layers as **PMTiles** or **map-ready GeoJSON**, not on-demand DuckDB. Device tiering: full data on desktop,
tiles on a 1 GB phone. **DuckDB is for SEARCH only** — companies, projects — never for drawing big layers.
Plus a fidelity-check approach against origin data.

All figures are measured from the repositories, not estimated from memory. Sources:
`data-gridatlas/202608291237-data-gridatlas/data/manifest.json` (rows and Parquet bytes),
`gridatlas/atlas/releases/202608300453-atlas-v9/data/*.geojson` (delivered GeoJSON bytes),
`data-gridatlas/tools/202608301930-fidelity.py` (the budget formulas already in use).

---

## 1. The arithmetic that decides everything

The repository already encodes the budget model. From `tools/202608301930-fidelity.py`:

```python
delivery_budget_s_at_20mbit  = original_bytes * 8 / (20 * 1_000_000)
on_demand_budget_s_at_20mbit = (duckdb_runtime_bytes + partition_bytes) * 8 / (20 * 1_000_000)
duckdb_runtime_bytes         = 35_700_000     # DuckDB-WASM module + worker
```

and the layer budget asserted by the browser job is **15 s** and **400 MB heap**.

**35,700,000 × 8 ÷ 20,000,000 = 14.28 s.**

The DuckDB runtime consumes **95 % of the layer budget before it reads a single byte of data.** Every on-demand
layer is therefore within 0.7 s of failure by construction, and any layer whose Parquet exceeds ~1.75 MB is over
budget no matter how well it is compressed.

This is not a tuning problem. It is the wrong plane for drawing, and the fix is architectural.

### Measured: every partition against the 15 s on-demand budget

| partition | rows | Parquet B | on-demand s @20Mbit | verdict |
|---|---:|---:|---:|---|
| uk_primary_roads | 163,790 | 29,292,883 | **26.0** | over |
| uk_trunk_roads | 130,228 | 23,058,196 | **23.5** | over |
| uk_mainline_railways | 89,933 | 16,109,232 | **20.7** | over |
| global_ports | 45,148 | 5,688,405 | **16.6** | over |
| uk_motorways | 17,713 | 3,243,863 | **15.6** | over |
| grid_11kv_ukpn | 15,126 | 1,738,387 | **15.0** | at the line |
| subsea_data_cables | 7,479 | 1,563,602 | 14.9 | at the line |
| repd_master_v8_oracle | 10,784 | 1,482,074 | 14.8 | at the line |
| uk_metros_trams_root | 7,829 | 1,411,687 | 14.8 | at the line |
| grid_132kv | 6,227 | 1,411,851 | 14.8 | at the line |
| grid_400kv | 4,106 | 869,466 | 14.6 | at the line |
| grid_substations | 5,800 | 748,993 | 14.6 | at the line |
| industrial_offtakers | 5,878 | 744,705 | 14.6 | at the line |
| everything else | — | < 700,000 | 14.3–14.6 | at the line |

**Nothing is comfortably inside the budget.** The five "over" rows are the ones users notice; the rest pass only
because a runner has a fast link.

### Measured: the same layers as static GeoJSON

Delivered GeoJSON is already in the release for eleven layers, so the ratio is measurable rather than guessed:

| layer | GeoJSON B | Parquet B | ratio | static s @20Mbit |
|---|---:|---:|---:|---:|
| grid_132kv | 2,835,650 | 1,411,851 | 2.01× | 1.13 |
| grid_400kv | 1,469,779 | 869,466 | 1.69× | 0.59 |
| industrial_offtakers | 1,295,616 | 744,705 | 1.74× | 0.52 |
| grid_substations | 1,192,749 | 748,993 | 1.59× | 0.48 |
| grid_275kv | 1,022,298 | 604,554 | 1.69× | 0.41 |
| grid_66kv | 597,395 | 319,120 | 1.87× | 0.24 |
| railways | 508,861 | 587,824 | 0.87× | 0.20 |
| airports | 119,566 | 120,680 | 0.99× | 0.05 |
| grid_220kv | 62,038 | 36,941 | 1.68× | 0.02 |
| datacentres | 42,850 | 40,405 | 1.06× | 0.02 |
| power_plants | 35,626 | 30,866 | 1.15× | 0.01 |

**Line layers expand ~1.6–2.0×; point layers are roughly 1:1.** Static delivery is **12–30× faster** than the
on-demand path for every one of these, because it skips a 35.7 MB runtime.

Projecting the ratio onto the layers not yet delivered as GeoJSON:

| layer | Parquet B | est. GeoJSON B | static s @20Mbit | verdict |
|---|---:|---:|---:|---|
| uk_primary_roads | 29,292,883 | ~52 MB | **20.8** | still over |
| uk_trunk_roads | 23,058,196 | ~41 MB | **16.4** | still over |
| uk_mainline_railways | 16,109,232 | ~29 MB | **11.5** | inside, but heap-hostile |
| uk_motorways | 3,243,863 | ~5.8 MB | 2.3 | fine |
| global_ports | 5,688,405 | ~5.7 MB | 2.3 | fine |
| grid_11kv_ukpn | 1,738,387 | ~1.8 MB | 0.7 | fine (but quarantined) |

So the split is clean and evidence-based:

- **three layers must be tiles** — `uk_primary_roads`, `uk_trunk_roads`, `uk_mainline_railways`
- **everything else should be static map-ready GeoJSON**
- **nothing should be drawn through DuckDB**

---

## 2. The three delivery planes

### 2.1 `map-ready-geojson` — the default drawing plane

**Use for:** any layer whose delivered GeoJSON is ≤ 2 MB raw, or ≤ 20,000 features.

**Rules.**
1. Built once, at build time, in `data-gridatlas`. Never derived in the browser.
2. Content-addressed filename or a hash-pinned manifest entry. The cartridge verifies the digest with
   `crypto.subtle.digest` before handing bytes to MapLibre — the pattern the search cartridge and the bridge already
   use.
3. Served with `cache: 'force-cache'`; the manifest keeps `no-store`.
4. Property set trimmed to what is drawn or shown in the popup. Everything else lives in the search Parquet.
   `industrial_offtakers` at 1.30 MB for 5,878 points is ~220 B per point — that is a rich payload for a dot.
5. `preload: false` unless the layer is on the critical path. Only `grid_400kv` is.

**Budget.** ≤ 2 MB raw per layer ⇒ ≤ 0.8 s at 20 Mbit. Gzip typically takes this to 0.2–0.3 s.

### 2.2 `pmtiles` — the heavy plane

**Use for:** anything above 2 MB raw or 20,000 line features. Today that is exactly four layers.

**Why it works.** A GeoJSON source transfers and parses the *whole national dataset* whatever the viewport. A
PMTiles archive is a single range-requested file; the client fetches only the tiles covering the current view at
the current zoom. Typical viewport cost is **50–500 KB**, independent of the national size.

**Rules.**
1. One archive per layer, built in `data-gridatlas` from the same Parquet partition that feeds the fidelity check.
2. `minzoom` gating is mandatory: `uk_primary_roads` must not load at national zoom. Suggested floors —
   motorways 5, trunk 7, primary 9, mainline rail 6.
3. Archive pinned by sha256 in the data manifest; the PMTiles header is verified before the protocol is registered.
4. The `pmtiles` library must be version-pinned exactly as `@duckdb/duckdb-wasm@1.29.0` is. New third-party
   dependency — see `questions.md` Q7.
5. Attribution travels with the tiles: OpenStreetMap contributors, as the shell footer already states.

**Budget.** ≤ 500 KB per viewport at any zoom; archive size unbounded (it is not transferred whole).

### 2.3 `search-parquet` — the search plane, and *only* the search plane

**Use for:** answering a question the user explicitly asked, over a keyed dataset, returning tens of rows.

**Current legitimate users.**
- REPD free-text search — `repd_projects_202608290716.parquet`, 1.45 MB, 11,069 rows
- companies candidate lookup — `company-repd-relationships-v1.parquet`, 1.41 MB, 482,030 rows
- contractor exposure — future, capped at 20 MB per the companies discipline

**Rules.**
1. **Never at load.** The runtime boots on the first explicit query, not on page open. The existing bridge already
   gets this right: `scheduleRuntimePrewarm()` waits until `map.isSourceLoaded('src-400')` and then defers to
   `requestIdleCallback`.
2. **Never for a deep link.** A deep link is a keyed lookup and belongs in the static ref index —
   `DRAFT-CARTRIDGES/exact-ref-index.spec.md`.
3. **One runtime, shared.** Adding a second searchable Parquet costs only its own bytes, because DuckDB is already
   instantiated. Adding a second *runtime* would be a defect.
4. DuckDB reads Parquet over HTTP range requests, so a keyed query touches only the needed row groups — the
   practical transfer for `WHERE company_number = ?` is far below the 1.41 MB file size. This is why Parquet is the
   right format for search and the wrong one for drawing.
5. Every result set must carry its provenance fields
   (`candidate_commit`, `manifest_sha256`, `dataset_sha256`, `evidence_type`, `relationship_status`) per the
   companies contract.

**What must move off this plane.** The `streaming-parquet-bridge` currently routes *every* legacy V8 data path
through DuckDB. That was the right move at the time — it removed 56 raw GeoJSON files from the release. But it
means the drawing plane is the search plane, and §1 shows the cost. The migration is §4.

---

## 3. Device tiering

Three tiers, decided from evidence available in the browser, and **degrading, never blocking**.

| tier | detection | drawing plane | search plane | preloaded layers |
|---|---|---|---|---|
| **desktop** | `navigator.deviceMemory >= 8` or no signal and viewport ≥ 1024 wide | full static GeoJSON; PMTiles for the heavy four | DuckDB on explicit query | 400 kV + substations |
| **tablet** | viewport 768–1023, or `deviceMemory` 4–7 | static GeoJSON ≤ 2 MB; PMTiles for anything heavier | DuckDB on explicit query | 400 kV only |
| **constrained** | `deviceMemory <= 4`, or `navigator.connection.saveData`, or `effectiveType` in `{slow-2g, 2g, 3g}` | **PMTiles only** for anything over 500 KB; static GeoJSON under that | **ref index only**; DuckDB refused unless the user opts in | none |

Rules.

1. **Detection is advisory, never gating.** `navigator.deviceMemory` is absent on Safari. When unknown, use viewport
   width and `connection.effectiveType`, and default to **tablet**, not desktop. Never block a layer a user asked
   for — surface a warning and let them proceed.
2. **The constrained tier must still deep-link.** That is the whole point of `exact-ref-index`: a sales link opens
   the right project on any device, with no runtime, in ~0.15 s of transfer.
3. **Report the tier.** `window.__GRIDATLAS_DEVICE_TIER__ = { tier, signals, decided_at }` so a browser gate can
   assert the tier it exercised.
4. **The 400 MB heap cap is a desktop cap.** For the constrained tier assume ~150 MB usable. A 50 MB GeoJSON parsed
   into JS objects can reach 300–500 MB of heap — which is why the heavy four are tiles on every tier, not just the
   small one.

Draft detection (10 lines, no dependency):

```js
function deviceTier() {
  const memory = Number(navigator.deviceMemory) || null;
  const connection = navigator.connection || {};
  const saveData = connection.saveData === true;
  const slow = ['slow-2g', '2g', '3g'].includes(connection.effectiveType);
  const width = Math.max(window.innerWidth || 0, window.innerHeight || 0);
  if (saveData || slow || (memory !== null && memory <= 4)) return 'constrained';
  if (memory !== null && memory >= 8 && width >= 1024) return 'desktop';
  if (width >= 1024) return 'desktop';
  return 'tablet';
}
```

---

## 4. Migration plan, in order

| step | change | risk | proof |
|---|---|---|---|
| **D1** | Publish the ref index; deep links stop needing DuckDB | low | `exact-ref-index.spec.md` §6 |
| **D2** | Move the eleven already-delivered GeoJSON layers off the on-demand path and onto their static release copies (they are already in the release; the bridge already `force-cache`s them) | none — already the behaviour | assert `map_ready_requests > 0` and `intercepted_on_demand` does not grow for those paths |
| **D3** | Build static GeoJSON for the remaining light partitions (`global_ports`, `uk_motorways`, `heavy_emitters_uk`, supermarkets, transit, stadiums, EV, hydrocarbons, subsea cables) and add them to the map-ready set | low | fidelity PASS + browser budget under 15 s and 400 MB |
| **D4** | Build PMTiles for `uk_primary_roads`, `uk_trunk_roads`, `uk_mainline_railways`, `uk_motorways`; register the protocol in the bridge cartridge | medium — new dependency | viewport transfer ≤ 500 KB at each zoom floor; feature count > 0; fidelity against origin |
| **D5** | Restrict DuckDB to the search plane; the bridge no longer intercepts drawing paths | medium | `duckdb_runtime_started === false` after a full desktop session with every layer toggled and no search typed |
| **D6** | Add device tiering and the tier report | low | gate asserts the tier on each device cell |

D5 is the point at which §1's arithmetic stops applying to the map at all.

---

## 5. Fidelity check against origin data

The approach already exists and is good. It should be extended, not replaced.

### 5.1 What exists

`data-gridatlas/.github/workflows/202608301931-layer-fidelity.yml` — daily at 03:23, on push to `*/data/**`, and on
dispatch. Two jobs:

**Job `offline`** — for every layer URL parsed out of the immutable shell:
1. resolve the layer's Parquet partition from the data manifest (with the two known aliases,
   `repd_master → repd_master_v8_oracle` and `uk_metros_trams → uk_metros_trams_root`)
2. fetch the V8 origin GeoJSON from `globalgrid2050` at the pinned commit
3. run `tools/202608301930-fidelity.py`, which compares **feature by feature**:
   - `sha256(canonical(original_feature))` vs the stored `original_feature_sha256`
   - `geometry != feature.geometry` → `coord_mismatch`
   - `sha256(canonical({geometry, properties}))` vs `projected_feature_sha256`
   - property keys dropped / added / changed, reported as a **policy surface**, not a geometry failure
   - `count_match`, `missing_partition_rows`, `extra_partition_rows`
4. emit SARIF with two rules: `layer-fidelity` (error) and `layer-delivery-budget` (warning at > 15 s on-demand)

**Job `browser`** — Playwright 1.62.1 + Chromium against the **public** composition:
toggle every layer in `#scada-ui-container`, wait for a terminal `[OK|EMPTY|FAIL]` label, wait for
`map.isSourceLoaded(sourceId)`, then measure `Runtime.getHeapUsage`, elapsed seconds and
`querySourceFeatures().length`. Fails if the label is not `[OK]`, the source is not loaded, seconds > 15,
heap > 400 MB, or features < 1.

This is a genuinely strong harness: it proves **identity** offline and **delivery** in a real browser.

### 5.2 What must be added for the new planes

| addition | why |
|---|---|
| **PMTiles fidelity** | The current comparator reads a Parquet partition. For a tiled layer it must instead decode the archive, count features per tile at each zoom floor, and compare the **union** of decoded features at max zoom against the origin feature count with a declared simplification tolerance. Tile simplification means byte-identical hashes are impossible; the check becomes count + geometry-within-tolerance, and the tolerance must be **declared in the contract**, not discovered. |
| **Static GeoJSON fidelity** | Trivial and strong: `sha256(delivered_bytes)` must equal the manifest digest, and `sha256(canonical(feature))` per feature must equal `original_feature_sha256`. Same function, no new logic. |
| **Ref-index fidelity** | Assert `rows === 11069`, `parquet_sha256` matches the pinned Parquet, and every `repd_ref` in the index exists in the Parquet with identical `longitude`/`latitude` to 6 dp. |
| **Window-layer fidelity** | Assert every `repd_ref` in every window artefact exists in the 7,680 spine, that states are drawn from the eight-value enum, that no feature carries a person-keyed property, and that the union of the five files has no duplicate `repd_ref`. |
| **Device-tier budgets** | The browser job runs one 1280 × 900 desktop context. Add the `pipelinenews` device cells (390 × 844, 375 × 667, 768 × 1024) with tier-specific budget thresholds. |
| **Origin availability** | `NO_ORIGIN` is currently recorded and skipped. It should be a **warning that ages into an error**: an origin that has been unfetchable for more than N runs means the layer can no longer be proved and must be marked unproved on the map. |

### 5.3 The rule the whole plan rests on

> Fidelity and delivery are separate verdicts and must never be traded against each other.

`fidelity.py` already does this — dropped properties are reported but do not fail geometry fidelity, and the
delivery budget is a *warning*, not a fidelity failure. Keep that separation. A layer may be
`FIDELITY PASS / DELIVERY OVER BUDGET`, and that is exactly the state the three road layers are in today. The
answer is a different delivery plane, not a weaker fidelity test.

---

## 6. Summary table — the target state

| layer group | plane | budget | tier availability |
|---|---|---|---|
| Topology 400/275/220/132/66 kV | map-ready-geojson (pre-snapped) | ≤ 1.2 s each | all tiers |
| 11 kV UKPN | map-ready-geojson | 0.7 s | desktop only (**quarantined identity**) |
| Substations | map-ready-geojson | 0.48 s | all tiers |
| Assets (nuclear, gas, industry, DC, airports, rail) | map-ready-geojson | ≤ 0.52 s each | all tiers |
| REPD official v9 | map-ready-geojson | ~0.5 s gzipped | all tiers |
| **Funding window (5 states)** | **map-ready-geojson** | **≤ 0.24 s gzipped** | **all tiers** |
| Pipeline projects (7,680) | map-ready-geojson | ~0.3 s gzipped | all tiers |
| Supermarkets, transit, stadiums, EV, ports, hydrocarbons, subsea | map-ready-geojson | ≤ 2.3 s each | desktop, tablet |
| **Motorways, trunk, primary, mainline rail** | **pmtiles** | **≤ 500 KB per viewport** | all tiers, zoom-gated |
| REPD search | search-parquet | on explicit query | desktop, tablet; opt-in on constrained |
| Companies candidates | search-parquet | on explicit query | desktop, tablet; opt-in on constrained |
| Deep-link resolution | static ref index | 0.15 s | **all tiers, no runtime** |
