# CARTRIDGE-CATALOG

Every cartridge the next GridAtlas should have. The window-intelligence / funded-project layer is the centrepiece:
the cartridge that shows, on the map, **which projects are in the funding window now**.

Each entry states purpose, feeding data source, delivery type
(`map-ready-geojson` | `pmtiles` | `search-parquet`) and a size/budget note grounded in the measured artefact sizes
in `data-gridatlas/202608291237-data-gridatlas/data/manifest.json` and the release GeoJSON payloads.

---

## 0. The constraints every entry must respect

| Constraint | Value | Source |
|---|---|---|
| Cartridge file size | **≤ 400,000 bytes** | `tools/scope/loop.mjs` `validateAtlasLayout` |
| Layer hydration budget | **≤ 15 s** wall clock per layer | `state/streaming-road-fix.json`, browser fidelity job |
| Heap budget | **≤ 400 MB** used JS heap | same |
| Features after hydration | **≥ 1** | browser fidelity job |
| Free shell slots | **exactly one** — `202608292126-pre-snapped-config-adapter.js` | shell `index.html` |
| Cartridge must not modify the shell | `immutable_shell_modified: false` | every composition manifest |
| DuckDB-WASM runtime cost | **35.7 MB ≈ 14.3 s at 20 Mbit** before any data | `tools/202608301930-fidelity.py` default |

**The last row governs the whole catalogue.** At 20 Mbit the DuckDB runtime alone consumes 14.3 of the 15 s budget.
Anything drawn through DuckDB-on-demand is over budget by construction. DuckDB is a **search** engine here, not a
drawing engine. See `DATA-DELIVERY-PLAN.md`.

### The one-free-slot problem

Only one shell script slot remains. Therefore the next cartridge must be a **composite**: a single file that both
(a) preserves the existing pre-snap config rewrite and (b) installs every new capability that needs to run before
`initVentusMap` is called. Subsequent capabilities are added by superseding that composite with a later generation,
not by claiming a new slot. Each entry below states whether it needs the slot or can live inside an already-taken one.

---

## 1. Priority table

| # | Cartridge | Slot need | Delivery | Priority |
|---|---|---|---|---|
| C1 | `exact-ref-index` | inside search slot | `map-ready-geojson` (static JSON) | **1 — unblocks mobile** |
| C2 | `window-intelligence` | **free config slot** | `map-ready-geojson` | **2 — the centrepiece** |
| C3 | `repd-official-v9` | free config slot (with C2) | `map-ready-geojson` | 3 |
| C4 | `pipeline-projects` | inside C2 | `map-ready-geojson` | 4 |
| C5 | `companies-search` | inside search slot | `search-parquet` | 5 |
| C6 | `grid-connection-status` | inside C2 | `map-ready-geojson` | 6 |
| C7 | `distress-overlay` | inside C2 | `map-ready-geojson` | 7 |
| C8 | `contractor-exposure` | inside C2 | `search-parquet` | 8 |
| C9 | `highways-pmtiles` | inside bridge slot | `pmtiles` | 9 |
| C10 | `data-centres-gb` | inside C2/C3 config | `map-ready-geojson` | 10 |
| C11 | `interconnectors` | inside C2/C3 config | `map-ready-geojson` | 11 |
| C12 | `gb-electricity-hud` | inside C2 | `search-parquet` | 12 |
| C13 | `heavy-industry-offtakers` | inside C2/C3 config | `map-ready-geojson` | 13 |
| C14 | `deep-link-out` | inside C2 | none | 14 |

---

## C1 — `exact-ref-index`

**Purpose.** Make deep-link resolution instant and device-independent. Today
`receiveExactRepdDeepLink` cannot resolve without booting DuckDB-WASM (35.7 MB) and querying a 1.45 MB Parquet — on a
1 GB phone that is the difference between a working sales link and a blank map. This cartridge resolves
`?repd_ref=` from a small static index first and only falls back to DuckDB for free-text search.

**Feeding data source.** `gridatlas/data/repd_projects_202608290716.parquet` (11,069 rows), projected at build time
to a minimal index. New build artefact, same generation lineage, hash-pinned like the existing manifest.

**Delivery type.** `map-ready-geojson` — specifically a static, hash-verified JSON object map (not drawn; used for
lookup). Optionally sharded by `repd_ref` modulo for very large future universes; not needed at 11,069.

**Fields per row (7).** `repd_ref, name, technology, status, capacity_mw, longitude, latitude`.
Deliberately excludes address, postcode, county, LPA, operator — those come from the Parquet when search runs.

**Size/budget.**
- Estimated raw JSON ≈ 11,069 × ~95 B ≈ **1.05 MB**, gzip ≈ **300–380 KB** over the wire.
- At 20 Mbit: **0.15 s** transferred. Against a 15 s budget, effectively free.
- Compare: today's path is 14.3 s (runtime) + 0.6 s (Parquet) ≈ **14.9 s** on a good connection, and unbounded on a
  constrained device.
- The 9.3 MB `repd_browser_registry_202608290716.json` already in `gridatlas/data/` is the *wrong* artefact for this —
  it is the full record set and would cost 3.7 s at 20 Mbit plus a large heap. Build a new minimal index; do not
  reuse the registry.

**Placement.** Inside the existing `uk-gazetteer-flyto` search slot, as a superseding generation of that cartridge.
No new slot consumed.

**Acceptance.** Golden deep link `?repd_ref=13599` reaches `gridatlasRepdDeepLink='resolved'` in **< 3 s** on the
375 × 667 cell with DuckDB never instantiated; free-text search still works and still boots DuckDB lazily.

---

## C2 — `window-intelligence` — **the centrepiece**

**Purpose.** Show, on the map, which projects are in the funding window **now**, ranked, with the register evidence
that put them there and an estimated design-freeze date labelled as derived. This is the product: a supplier opens
the map and sees the projects where studies, cable and LV design are being bought this month.

**Feeding data source.** `pipelinenews` `project_window_state` + `window_evidence` datasets drafted in
`window-intelligence.md` §12.6, published as a compact map-ready artefact:

```
https://ventusltd.github.io/pipelinenews/releases/data/window/{generation}/window-map-v1.geojson
```

with a hash-pinned sidecar manifest carrying `generation`, row counts per state, `spine_projects_sha256`, and the
ranker weights used.

**Delivery type.** `map-ready-geojson`. One point per project **that has a decided state**, never the whole spine.

**Layers installed (one new legend group, inserted FIRST — see `intelligence-chain.md` §6.1 F4).**

| layer id | label | colour | filter |
|---|---|---|---|
| `win_funding` | Funding window | `#00ff88` | `state == FUNDING_WINDOW` |
| `win_procuring` | Procuring | `#ffae00` | `state == PROCURING` |
| `win_consented` | Consented, no funding evidence | `#8888ff` | `state == CONSENTED` |
| `win_frozen` | Design frozen | `#888888` | `state == DESIGN_FROZEN` |
| `win_distressed` | Distressed | `#ff2222` | `state == DISTRESSED` |

Radius interpolated on `window_score` so the highest-ranked project is visibly the biggest dot, not the biggest
project. Capacity is already available on the REPD layers; the window layer's job is to rank by *timing*.

**Popup.** Exactly as drafted in `intelligence-chain.md` §4 H7 — name, state, capacity, LPA, REPD ref, date entered,
rank, the proof rows with their register named, the estimated freeze marked derived, and two outbound buttons.

**Size/budget.**
- Upper bound is the whole spine: 7,680 features. Realistic first cut is projects in states 2–5 and 8, which is a
  subset — assume worst case 7,680.
- At ~230 B per feature (7 properties + a point) ≈ **1.8 MB** raw, gzip ≈ **500–650 KB**.
- At 20 Mbit: **0.72 s** raw / ~0.26 s gzipped. Well inside 15 s.
- Heap: 7,680 point features in MapLibre is trivial (compare `grid_substations` at 5,800 and
  `industrial_offtakers` at 5,878, both live today).
- Cartridge JS: the config injector plus popup renderer, estimated **12–18 KB**, well under the 400 KB cap.

**Slot.** Takes the free `202608292126-pre-snapped-config-adapter.js` slot and **must reproduce the pre-snap
rewrite** (`snap: false` for `400, 275, 220, 132, 66`) or the topology snaps twice in the browser.

**Fail-closed behaviour.** If the window artefact or its manifest fails its hash check, the cartridge must add
**no** layers, log to `window.__GRIDATLAS_WINDOW__.failures`, still perform the pre-snap rewrite, and let the map
run exactly as it does today. `FAIL_CLOSED_WITH_CORE_PRODUCT_UNCHANGED`.

**Draft implementation:** `DRAFT-CARTRIDGES/window-intelligence.js.txt` + `window-intelligence.spec.md`.

---

## C3 — `repd-official-v9`

**Purpose.** Replace the V8 oracle REPD layers with the official DESNZ Q2 2026 extract. Today all 16 REPD layers in
the shell config point at `/dist/repd_master.json` — the 10,784-feature V8 oracle — and `data-gridatlas` marks all
16 `ORACLE_ONLY_REPLACED_BY_OFFICIAL_REPD_V9`. The map is drawing yesterday's data while the search lane already
uses the official extract. That inconsistency is visible to a customer the moment they search a project and then
look at the dots.

**Feeding data source.** `gridatlas/data/repd_projects_202608290716.parquet` (11,069) projected to GeoJSON, or the
`data-gridatlas` partition `repd_master_v8_oracle.parquet` superseded by a new official partition.

**Delivery type.** `map-ready-geojson`, one file, technology-filtered client-side exactly as the shell already does
(all 16 layers share `src-repd`).

**Size/budget.**
- V8 oracle GeoJSON today: `globalgrid2050/dist/repd_master.json`, 4,256,963 B for 10,784 features
  (`gridatlas/data/repd_v9_manifest_…json` `v8_oracle.bytes`). **2.0 s at 20 Mbit** raw.
- Official 11,069 features with the same 8 drawn properties ≈ **4.4 MB** raw, gzip ≈ **1.1–1.4 MB** ⇒ **0.5 s**.
- Keep the drawn property set to `{name, tech, raw_tech, status, capacity, repd_ref}` — six keys. Adding address,
  postcode and LPA to the drawn payload roughly doubles it for no map benefit; those belong in the search Parquet.
- Heap: 11,069 points, negligible.

**Identity note.** The V8 property names (`tech`, `raw_tech`, `capacity`, `status`) are baked into 16 shell layer
filters. The projection **must emit V8 property names** or every filter breaks. Add `repd_ref` as a new property —
it is absent from the V8 oracle, which is why the map cannot currently deep-link *out* of a clicked dot.

---

## C4 — `pipeline-projects`

**Purpose.** Draw the 7,680-project governance spine as its own layer group, so the map can distinguish
*"a REPD record"* (11,069) from *"a project we govern"* (7,680, ≥ 1 MW) — and so every dot in that group carries a
working outbound deep link into pipelinenews.

**Feeding data source.** `pipelinenews/data/atlas/202608261927-atlas-{tech}-partition-v9-1-*.geojson`, already
built: 8 solar parts, 4 bess, 5 wind_onshore, 1 wind_offshore, 18 files.

**Delivery type.** `map-ready-geojson`, concatenated at build time into one file per technology.

**Size/budget.** Measured directly from the repository:

| technology | parts | total bytes | at 20 Mbit |
|---|---|---|---|
| solar | 8 | 1,278,933 | 0.51 s |
| bess | 4 | 584,029 | 0.23 s |
| wind_onshore | 4+ | ~700,000 | 0.28 s |
| wind_offshore | 1 | 33,754 | 0.01 s |
| **all** | 18 | **≈ 2.6 MB** | **≈ 1.0 s** |

Comfortably inside budget as static GeoJSON. Gzipped, ~0.3 s.

**Placement.** Inside C2's config injection, as a second group. Adds `geometry_status` so the 28 projects with
missing geometry are excluded from drawing rather than plotted at a false origin.

---

## C5 — `companies-search`

**Purpose.** Let a user type a company name or number and see which REPD projects that company is a **candidate**
for — with the mandated caveat, never as ownership.

**Feeding data source.**
`companies` candidate branch `data/candidates/202608272155-compact/company-repd-relationships-v1.parquet`
(482,030 rows, 1,405,427 B) — plus, when it exists, the project-vehicle bindings table.

**Delivery type.** `search-parquet`. This is the correct and intended use of the DuckDB lane: a keyed lookup over a
small Parquet, run only on an explicit user query, never at load.

**Size/budget.**
- Parquet 1.41 MB ⇒ **0.56 s** transfer at 20 Mbit, on top of the DuckDB runtime the search lane already boots.
- Because the search lane already instantiates DuckDB for REPD free-text search, the marginal cost is only the
  1.41 MB. Adding it does **not** add a second runtime.
- Query: `SELECT repd_ref, evidence_type FROM read_parquet(...) WHERE company_number = ?` — DuckDB will read only
  the needed row groups over HTTP range requests, so the practical transfer is far below 1.41 MB.

**Presentation law (non-negotiable).**
- header must read **"Company-REPD candidate (name evidence; ownership unconfirmed)"**
- default view is a **count** and an evidence-type breakdown, not a list of company names
- the three evidence types must be labelled with their claim limits from the companies contract
- absence of a row is displayed as *"this bounded generator emitted no assertion"*, never *"no relationship"*

---

## C6 — `grid-connection-status`

**Purpose.** For each project in the funding window, show its grid exposure: nearest substation, nearest circuit
and its voltage, and whether a connection-register entry exists. This is the sentence a cable and connectivity
supplier opens a call with.

**Feeding data source.**
- `data-gridatlas` `partitions/grid_substations.parquet` (5,800 rows) and
  `derived/grid_{132,275,400}kv_snapped.parquet` (6,227 / 2,935 / 4,106 rows)
- NESO connection register via the Step 1 register adapter (`window-intelligence.md` §10)

**Delivery type.** `map-ready-geojson` — but as a **precomputed join**, not a client-side spatial query. Compute
nearest-substation and nearest-circuit distance **at build time** in DuckDB and ship them as properties on the
window layer. A browser does not need the topology loaded to display "2.1 km from a 132 kV circuit".

**Size/budget.** Three extra numeric properties and two short strings on the C2 payload: `nearest_substation_km`,
`nearest_circuit_kv`, `nearest_circuit_km`, `nearest_substation_name`, `connection_register_status`.
≈ 60 B per feature × 7,680 ≈ **460 KB** added raw, ~100 KB gzipped. **0.18 s.**

**Discipline.** Distance is straight-line and **screening-grade**. It never asserts a route, a cost or a connection
likelihood. `connection_register_status` is `ABSTAIN` unless a register row was actually found — absence is not
evidence. This is required by the `spiders` source-card doctrine and by the abstention law.

---

## C7 — `distress-overlay`

**Purpose.** Surface the highest-precedence state on its own, because "stop selling to this developer" is an alert
in its own right and must not be buried inside a ranked list a salesperson scrolls past.

**Feeding data source.** `project_window_state` rows with `state = DISTRESSED`, plus the proof rows.

**Delivery type.** `map-ready-geojson` — a small subset of the C2 payload, drawn on its own layer with its own
legend entry, always at the top of the paint order.

**Size/budget.** Small by nature; the 7,680-project spine has a minority in `INACTIVE`. Even at 10 % that is ~770
features ≈ **180 KB** raw. Negligible.

**Behaviour.** Selecting a distressed project shows the terminal filing or planning event and its date, and offers
the contractor-exposure view (C8) for the same developer — *"you have three other projects with this counterparty"*.

---

## C8 — `contractor-exposure`

**Purpose.** For a named organisation, how many projects it is confirmed on, by state and capacity — including how
many are distressed. A supplier's own exposure, and a competitor's footprint.

**Feeding data source.** `CONFIRMED` attribution roles from the register adapter (`DEVELOPER, OWNER, EPC,
PRINCIPAL_CONTRACTOR, ICP, OM_PROVIDER, LENDER, TECHNICAL_ADVISER`), published as a compact Parquet.

**Delivery type.** `search-parquet`. Explicit query only; no layer.

**Size/budget.** Bounded by the number of confirmed register roles, which starts near zero and grows slowly.
Even 100,000 rows of `(gg_project_id, role, organisation, company_number, effective_from, evidence_url)` is
< 5 MB Parquet. Cap the artefact at 20 MB, matching the companies discipline.

**Discipline.** `REPORTED` roles never appear in a count — only in the discrepancy view, labelled. No individual is
named. No score of any kind is computed.

---

## C9 — `highways-pmtiles`

**Purpose.** Restore motorways, trunk roads and primary roads to the map without blowing the budget. These are the
three layers the current architecture cannot serve within 15 s.

**Feeding data source.** `data-gridatlas` `partitions/uk_motorways.parquet`, `uk_trunk_roads.parquet`,
`uk_primary_roads.parquet`, plus `uk_mainline_railways.parquet`.

**Delivery type.** **`pmtiles`.** This is the only entry in the catalogue that must be tiles, and the numbers say why:

| layer | rows | Parquet bytes | est. GeoJSON | on-demand at 20 Mbit | static GeoJSON at 20 Mbit |
|---|---|---|---|---|---|
| `uk_motorways` | 17,713 | 3,243,863 | ~6 MB | **15.6 s** | 2.4 s |
| `uk_trunk_roads` | 130,228 | 23,058,196 | ~40 MB | **23.5 s** | 16.0 s |
| `uk_primary_roads` | 163,790 | 29,292,883 | ~50 MB | **26.0 s** | 20.0 s |
| `uk_mainline_railways` | 89,933 | 16,109,232 | ~28 MB | **20.7 s** | 11.2 s |

(on-demand = `(35,700,000 + partition_bytes) × 8 / 20e6`, the exact formula in `tools/202608301930-fidelity.py`)

Every one is over the 15 s on-demand budget; three of four are over even as static GeoJSON; and the heap cost of
50 MB of GeoJSON parsed into JS objects is several hundred megabytes — against a 400 MB cap and a 1 GB phone.

With PMTiles, only the tiles in the current viewport transfer: **typically 50–500 KB per view**, independent of the
national dataset size, with `minzoom` gating so primary roads never load at national zoom.

**Slot.** Lives inside the existing `streaming-parquet-bridge` slot as a superseding generation, because the bridge
already owns `window.fetch` interception and is the natural place to route a source to a `pmtiles://` protocol
handler instead of a GeoJSON URL.

**Dependency.** Requires a PMTiles protocol registration in the browser. MapLibre supports a custom protocol; the
`pmtiles` library must be loaded. That is a new third-party dependency and needs the same version-pinning and
integrity discipline as `@duckdb/duckdb-wasm@1.29.0`. Recorded in `questions.md` Q7.

---

## C10 — `data-centres-gb`

**Purpose.** Data centres as offtakers and as competitors for connection capacity. The shell already has a
`Data Ctrs` layer (`dc`), currently fed by the 240-row V8 partition.

**Feeding data source.** `data-centres-gb` `exports/202608281053-osm-data-centres.geojson` — 306 OSM elements from
one bounded Overpass request, with `DCGB-OSM-{TYPE}-{id}` source-record ids.

**Delivery type.** `map-ready-geojson`.

**Size/budget.** The whole candidate closure is 292,578 B across 4 files; the GeoJSON export is a fraction of that.
**< 0.1 s.** Trivial.

**Discipline.** `facility_identity_status: SOURCE_ELEMENT_ONLY` — an OSM element is **not** a facility. Buildings and
campuses are not merged. The 612 company relationship rows are all `ABSTAIN` with
`abstention_reason: VERIFIED_COMPANY_NUMBER_REQUIRED`; no operator or owner may be displayed as fact.
Data Center Map is excluded from ingestion by its terms and must stay excluded.

---

## C11 — `interconnectors`

**Purpose.** Border flows as context for the grid picture, and the future-cable list as a pipeline of its own.

**Feeding data source.** `data-interconnectors` — **which currently has no landed data**. It has
`reference/interconnector_cables.csv`, two pipelines and a research note. Ten operational cables are documented with
BMRS codes and capacities; six future cables are listed as `DATA NOT WIRED`.

**Delivery type.** `map-ready-geojson`, built from the reference table plus landing-point coordinates.

**Size/budget.** 16 features. **Bytes are irrelevant.** The constraint here is truth, not size.

**Discipline.** The repository's own law: a future cable carries no fake values, no BMRS code and no data wiring
until Elexon issues an operational code. The map must render future cables in a visually distinct, explicitly
labelled `DATA NOT WIRED` style, or not at all. Sign convention if flows are ever added: positive signed MW is
**import to GB**.

**Blocked on:** running `pipelines/build_interconnectors.py` to land data. Recorded in `questions.md` Q8.

---

## C12 — `gb-electricity-hud`

**Purpose.** Put a live-ish national context number in the HUD header — current renewable share, or the last
settled half-hour by technology — so the map has a pulse rather than only a countdown clock.

**Feeding data source.** `data-gb-electricity` `generation/dataset=fuelhh/year=*/month=*/data_*.parquet`
(settled, key `time + technology`) and `dataset=fuelinst` (provisional, key `periodStartUTC + fuelType`).

**Delivery type.** `search-parquet` — one small aggregate query, or better, a **precomputed daily summary JSON**
published by `data-gb-electricity` so the browser reads a 2 KB file rather than booting a query.

**Size/budget.** A precomputed summary is ~1–3 KB. **Effectively free.** Reading the partitioned Parquet directly
from the browser would mean a runtime boot for a header number — do not.

**Freshness caveat.** FUELHH is landed to **2026-05**, FUELINST to **2026-06**; today is 2026-08-30. The monthly
updater is documented as *unproven until a controlled dispatch is audited*. Any HUD number must therefore carry its
own `as of` date and must show `STALE` when older than one settlement month. Never present a two-month-old figure
as "now".

---

## C13 — `heavy-industry-offtakers`

**Purpose.** Behind-the-meter demand next to a consented generator is a commercial pairing. The shell already has
`ind` (Industry, `industrial_offtakers`) and `naei_co2` (Major Industrial Sites, `heavy_emitters_uk`).

**Feeding data source.** `data-gridatlas` `partitions/industrial_offtakers.parquet` (5,878 rows, 744,705 B) and
`partitions/heavy_emitters_uk.parquet` (2,458 rows, 419,289 B). Plus the `BTM_*` SIC tags already computed in
`companies` for behind-the-meter classification.

**Delivery type.** `map-ready-geojson` (both are already released as GeoJSON: `industrial_offtakers.geojson`
1,295,616 B, and `heavy_emitters_uk` is a legacy JSON route).

**Size/budget.** 1.30 MB ⇒ **0.52 s** at 20 Mbit static. Within budget as a preloaded layer, which is how it is
configured today.

**Blocker.** `industrial_offtakers` is marked
`QUARANTINED_OUTPUT_NOT_REPRODUCIBLE_FROM_ADJACENT_FETCHER` in the browser layer registry — the output cannot be
regenerated from its stated fetcher. It draws today because the release GeoJSON is pinned, but it is **not
promotable** and must not be presented as a maintained dataset until reacquired. Same for `grid_11kv_ukpn`
(`QUARANTINED_SYNTHETIC_UKPN_11KV_IDENTITY`) and the three metro/tram layers
(`QUARANTINED_GEOMETRY_MISMATCH`).

---

## C14 — `deep-link-out`

**Purpose.** Close the loop. Every project popup gains **Open project** and **Open evidence** buttons that carry
`repd_ref` / `gg_project_id` back to pipelinenews.

**Feeding data source.** None — it reads the consumer's live pointer
(`https://ventusltd.github.io/pipelinenews/releases/current-v3.json`) and builds URLs from it.

**Delivery type.** none (behaviour only).

**Size/budget.** ~3 KB of cartridge JS.

**Blocked on:** pipelinenews having an inbound `repd_ref` receiver, which it does not
(`intelligence-chain.md` §4 H8). Until then the buttons must be **absent**, not broken.

---

## 2. Cartridges deliberately NOT proposed

| Not proposed | Why |
|---|---|
| A cartridge that draws the 482,030-row company candidate table | It is a candidate edge list with `role: UNKNOWN` and `decision: ABSTAIN`. Drawing it would manufacture ownership. Search only (C5). |
| A cartridge that scores companies | `companies` README forbids a public credit or bankability score. |
| A cartridge that names directors or PSCs | Excluded by every contract in the federation. |
| A cartridge that geocodes a project from its address | `coordinates_are_identity: false`; proximity never establishes identity. |
| A cartridge that shows news headlines against a project | Only via `sector_project_bindings` with an evidence-backed binding; unbound items have their identity fields physically stripped. |
| A second full application | `new_full_application_folders: 0`, `no-app-copies` vaccine. |
| A cartridge replacing `ventus-corev8engine.js` | The engine slot is forbidden. |

---

## 3. Delivery-type summary

| Delivery type | Cartridges | Rule |
|---|---|---|
| `map-ready-geojson` | C1, C2, C3, C4, C6, C7, C10, C11, C13 | Static, hash-pinned, gzip-served, one fetch, no runtime. Budget: **≤ 2 MB raw per layer** at 20 Mbit ⇒ ≤ 0.8 s. |
| `pmtiles` | C9 | Anything over 2 MB raw or over 20,000 line features. Viewport-bounded transfer. |
| `search-parquet` | C5, C8, C12 | Explicit user query only. Never at load. Never for drawing. Shares one DuckDB runtime with the existing search lane. |

**Total added first-load cost if C1+C2+C3+C4 ship together:**
0.38 MB (C1 gz) + 0.6 MB (C2 gz) + 1.3 MB (C3 gz) + 0.35 MB (C4 gz) ≈ **2.6 MB gzipped ≈ 1.05 s at 20 Mbit** —
and C2/C3/C4 are user-toggled layers, so only C1 is truly first-load. First paint is unchanged.
