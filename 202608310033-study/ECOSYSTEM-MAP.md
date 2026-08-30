# ECOSYSTEM-MAP

Draft artefact — not a build output. Written from a read-only survey of every repository under
`C:\Users\vikra\OneDrive\Documents\GitHub`. Nothing in any repository was changed.

Scope: every repo, what it owns, the full data flow, and the `companies ↔ pipelinenews ↔ gridatlas` triangle drawn
explicitly with the join keys **as they exist today**. Where the repositories contradict a stated assumption, the
contradiction is recorded here and repeated in `questions.md`.

---

## 0. One-paragraph statement of the product

The product is a **timing engine for grid-connection sales**. Studies, cable and LV design are bought *before* a
project design freeze; inverters are fought over *after*. The asset is being one supplier a month ahead of the trade
press by watching two registers — Companies House for the **funding signal** and local planning registers for the
**procurement signal** — and staying silent until both are on the record. `gridatlas` is the front door where a human
*sees* it. The intelligence is knowing which project entered the funding window this week. The frozen spine
underneath all of it is the DESNZ Renewable Energy Planning Database Q2 2026 extract.

---

## 1. Repository register

| Repo | Role | Owns | Publishes | Live? |
|---|---|---|---|---|
| `gridatlas` | **Application** — the map front door | Immutable shell releases, SHA-256 cartridges, composition pointer, REPD search Parquet, browser proofs | Pages `/gridatlas/atlas/` | **Yes** |
| `data-gridatlas` | **Data plane** for the map | Source contracts, V8→V9 transplant, per-source ZSTD Parquet partitions, browser layer registry, layer fidelity | Pages `/data-gridatlas/202608291237-data-gridatlas/` | Yes (candidate data) |
| `pipelinenews` | **Governance / discovery engine** | The 7,680-project spine, project partitions, news and sector-intelligence contracts, deep-link cartridges, identity policy, attribution ledger (archived) | Pages `/pipelinenews/releases/202608291447-pipelinenews/` | Yes |
| `companies` | **Funding signal** | Companies House bulk acquisition, accounts extraction, compact Company↔REPD candidate Parquet, Atlas link contract | Candidate branch only — `main` and Pages unchanged | **No — candidate only** |
| `globalgrid2050` | **Original V8 source / oracle + homepage** | The pinned V8 Atlas engine, `dist/repd_master.json`, v6–v9.7 dashboards, GIS/SLD sandbox, catalogue | `globalgrid2050.com` | Yes |
| `data-gb-electricity` | GB electricity time series | FUELINST / FUELHH / prices partitioned Parquet, Elexon fetchers | Repo files (no Pages product) | Data current to 2026-05/06 |
| `gb-electricity-ui` | UI shell for the above | Blank chart shells, migration scope | Pages | Shells only, **not wired** |
| `data-interconnectors` | Border-flow data | Cable reference table, Elexon INT-code pipelines | — | **No landed data** |
| `data-centres-gb` | GB data-centre facilities | OSM Overpass producer, facility Parquet, company relationship Parquet (all ABSTAIN), GeoJSON export, FastAPI reader | Candidate branch only | Candidate only |
| `data-federation-map-for-globalgrid2050-all-repos` | Federation metadata ledger | Repo nodes and edges, roles, dependency graph, weekly build reports, Parquet snapshots | Pages dashboard | Yes |
| `spiders` | Scanner species lab + **source-card doctrine** | Spider OS rules, external-source rules, ten source cards, `spider_maya` AREAS graph, `spider_printer` registry smoke | Pages | Doctrine live; scanners minimal (see §7) |
| `cvaa` | **Governance protocol** | 24 vaccines, `inoculate.mjs`, reusable workflow, `vaccines.lock`, fleet/replay/score tooling | Reusable GitHub workflow | Yes, but **adopted by nobody** (see §8) |

---

## 2. The spine — what "the project" actually is

Two REPD derivations exist and they are **not the same set**. Getting this wrong breaks every join.

### 2a. `pipelinenews` project spine (the governance spine)

- Contract: `pipelinenews/data/contracts/202608261927-release-v9-1.json`
- Build manifest: `pipelinenews/data/manifests/202608261927-build-manifest-v9-1.json`
- Source: DESNZ REPD **Q2 2026**, workbook sha256 `99ec4d0509a9fdfb999116e33c459084ce9ab59b44e3fafba5fc9b280ae2d5a6`,
  14,657 source records
- Filter: `capacity_mw >= 1.0`; technologies `solar | bess | wind_onshore | wind_offshore`; **all** official statuses;
  development deduplication forbidden; record identity preserved
- **project_count = 7,680**, capacity 356,474.09 MW, largest 4,100 MW
  (solar 3,563 · bess 1,609 · wind_onshore 2,399 · wind_offshore 109)
- Geometry: 7,652 present, 28 missing
- Canonical id: **`GG2050-REPD-{repd_ref}`** — the only canonical project key in the federation
- Development id: `GG2050-DEV-REPD-{repd_ref}`
- Per-project `lifecycle` values observed in the v9.1 partitions: `LIVE_PRE_CONSTRUCTION`, `UNDER_CONSTRUCTION`,
  `OPERATIONAL`, `INACTIVE`, `UNKNOWN` — **five values, not eight** (see `window-intelligence.md` §2)
- Per-project date fields that a lifecycle machine can actually key on:
  `planning_application_submitted`, `planning_permission_granted`, `planning_permission_refused`,
  `planning_application_withdrawn`, `planning_permission_expired`, `under_construction`, `operational`,
  `repd_record_updated`
- Other fields: `identity_status` (`REPD_BOUND`), `identity_confidence` (`authoritative`), `geometry_status`
  (`valid` / `missing`), `easting`, `northing`, `coordinate_source`, `planning_authority`,
  `planning_application_reference`, `operator`, `county`, `region`, `country`,
  `development_repd_refs`, `direct_related_repd_refs`, `planning_sibling_repd_refs`, `relationships`
- Physical layout: `data/projects/202608261927-project-partition-v9-1-01..16.json` (500 records each, last 180),
  map partitions in `data/atlas/202608261927-atlas-{tech}-partition-v9-1-*.geojson`

### 2b. `gridatlas` REPD search Parquet (the map and search spine)

- Manifest: `gridatlas/data/repd_v9_manifest_202608290716.json`
- Source: `REPD_Publication_Q2_2026.csv`, sha256 `84c1b5f958a934d8b4b86ec88f50bdcf43830ded7ff2efc27bffca0c98695035`,
  published 2026-08-03, 5,087,389 bytes
- **rows = 11,069** — *no capacity floor*, so it includes sub-1 MW records the governance spine excludes
- Statuses: awaiting construction 5,942 · operational 3,132 · application submitted 1,539 · under construction 456
- Addresses 11,059 · postcodes 9,505 (9,060 valid)
- Privacy: **1,729 possible individual applicants withheld** (`applicant_publication_state`)
- Parquet 1,454,200 bytes, 23 columns:
  `repd_ref, name, repd_address_raw, repd_address_display, repd_postcode_raw, repd_postcode, postcode_valid,
  county, region, country, planning_authority, planning_application_reference, repd_operator_or_applicant,
  applicant_publication_state, technology, repd_technology, status, capacity_mw, longitude, latitude,
  source_record_updated, source_row, source_row_sha256`
- Browser registry: `repd_browser_registry_202608290716.json`, **9,328,402 bytes** of the same records as JSON
- V8 oracle cross-check: 10,610 of 10,784 oracle features matched by name + rounded coordinate (98.3865 %)

**Consequence:** `repd_ref` is the shared key, but `11,069 ⊇ 7,680`. Anything the window-intelligence layer emits must
state which universe it is in. The gridatlas search cartridge asserts `closure.rows === 11069`,
`closure.postcodes === 9505` and `closure.addresses === 11059` as hard invariants, so it fails closed if the Parquet
is swapped for the 7,680 set without a new cartridge generation.

### 2c. What is **not** in the spine

The stated join keys are "site name, parish, postcode against the spine".

- **site name** — present, as `name`.
- **postcode** — present, as `repd_postcode` (raw and normalised, with `postcode_valid`), on 9,505 of 11,069 rows.
- **parish** — **absent**. No REPD derivation in the workspace carries a parish, ward or LSOA field. The V8 oracle
  (`globalgrid2050/dist/repd_master.json`) carries `local_planning_authority` (largely empty) but no parish. The word
  "parish" occurs in the corpus only inside project names.

The available administrative keys, in descending join strength, are:
`repd_postcode` → `planning_application_reference` → `planning_authority` (LPA) → `county` → `region` → `country`.
Any parish-level join must be **derived** — e.g. postcode → ONS postcode directory → parish — which is a new source
requiring a spiders source-card. Logged in `questions.md` Q3.

---

## 3. The triangle, drawn with real keys

```
                       +----------------------------------------------+
                       |  DESNZ REPD Q2 2026 (frozen, hash-pinned)    |
                       |  workbook 99ec4d05...  /  CSV 84c1b5f9...    |
                       +----------------+-----------------------------+
                    (>= 1 MW filter)    |    (no capacity floor)
                 +----------------------+------------------------+
                 v                                               v
   +==============================+            +===============================+
   |  pipelinenews                |            |  gridatlas                    |
   |  7,680 projects              |            |  11,069 REPD rows (Parquet)   |
   |  gg_project_id =             |            |  search + fly-to + deep link  |
   |    GG2050-REPD-{repd_ref}    |            |  identity: repd_ref ONLY      |
   +==============+===============+            +===============^===============+
                  |                                            |
                  |  EDGE A - deep link                        |  ?repd_ref={repd_ref}
                  |  buildAtlasV9DeepLink(project)             |  (+ technology required by producer;
                  |  gate: geometry_status === 'valid'         |   name/lon/lat optional evidence,
                  +--------------------------------------------+   never identity)
                              ^
                              |  EDGE B - company_number <-> repd_ref <-> evidence_type
                              |  482,030 candidate rows, role=UNKNOWN, decision=ABSTAIN
                              |
                 +============+====================================+
                 |  companies                                      |
                 |  294,904 selected companies                     |
                 |  company-repd-relationships-v1.parquet          |
                 |  key: (company_number, repd_ref, evidence_type) |
                 |  state/atlas-v9-link-contract.json -> URL tmpl  |
                 +=================================================+
```

### Edge A — pipelinenews → gridatlas (the deep link)

| Item | Value |
|---|---|
| Producer | `pipelinenews/ui/atlas-v9-deep-links.js`, contract `ui/cartridges/202608291504-atlas-pointer-deep-link.mjs` |
| Function | `buildAtlasV9DeepLink(project)` |
| Required identity | `repd_ref` matching `^[A-Za-z0-9-]{1,40}$` **and** `technology ∈ {solar, bess, wind_onshore, wind_offshore}` |
| Eligibility gate | `project.geometry_status === 'valid'`, else empty string and the row presents as `NO MAP` |
| Optional evidence | `name`, `longitude`, `latitude` — explicitly **not identity** |
| Consumer | `gridatlas` search cartridge, `receiveExactRepdDeepLink()` in `atlas/cartridges/202608301624-place-global-search-v9-5.js` |
| Consumer rule | `EXACT_REPD_REF_ONLY`; on success sets `document.body.dataset.gridatlasRepdRef` and `document.body.dataset.gridatlasRepdDeepLink = 'resolved'` |
| Consumer failure | sets `…RepdDeepLink = 'failed'`, pushes to `window.__GRIDATLAS_PLACE_SEARCH__.failures`, map stays usable |
| Contract file | `gridatlas/contracts/atlas-v9-deep-link-contract.v1.json` |
| Pointer of record | `https://ventusltd.github.io/gridatlas/state/live-set.json` |
| Sentinels | Beacon Fen `13599` (solar), East Pye `17494` (solar), Prologis DC4 `16135`, invalid-geometry `12780` |

**Defect, live today.** Both producers emit `https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=…`,
a **pre-migration path**. GridAtlas scope 1 (`202608301321-01-move-atlas-into-atlas-folder.md`) moved every release
under `atlas/releases/`, and `tools/scope/loop.mjs` now asserts `rootReleases.length === 0`. The stable route is
`/gridatlas/atlas/`; the immutable route is `/gridatlas/atlas/releases/202608300453-atlas-v9/`. Both
`pipelinenews/ui/atlas-v9-deep-links.js` and `companies/state/atlas-v9-link-contract.json` still carry the old base.
Detail and the two possible repairs are in `intelligence-chain.md` §3.

### Edge B — companies → pipelinenews and gridatlas (the funding key)

| Item | Value |
|---|---|
| Producer | `companies/build/python/202608281337-compact-parquet-companies.py` |
| Datasets | `company-repd-relationships-v1.parquet` (482,030 rows, 1,405,427 B), `solar-company-repd-relationships-v1.parquet` (346,233 rows, 1,118,626 B) |
| Declared key | `(company_number, repd_ref, evidence_type)` — 481,248 distinct pairs, 749 pairs with more than one evidence type, max 3 |
| Columns | exactly three VARCHARs. **No** names, URLs, descriptive fields or per-row provenance |
| Evidence vocabulary | `EXACT_OPERATOR_NAME` 5,669 · `EXACT_PROJECT_NAME` 765 · `PROJECT_NAME_SPV_CANDIDATE` 475,596 |
| Derivation of gg id | `GG2050-REPD-{repd_ref}` — derived downstream, **not stored** in the candidate |
| Role | `UNKNOWN` only |
| Consumer decision | `ABSTAIN` only, `eligible_for_join: false` |
| Pinned REPD universe | `pipelinenews@35f35ada161223fb3ee19e525664ee7f17df1ddd`, 7,680 projects, universe sha256 `d00dffe4659dbbb796cb1f32a6e446d3c429e800fc2c446b79b90189ee1db99c` |
| Downstream contract | `companies/contracts/202608281846-federated-company-repd-relationship-contract-v1.json` |
| Atlas URL template | `companies/state/atlas-v9-link-contract.json` — one dataset-level template, never a per-row URL |
| Storage rule | *"One dataset-level URL template; never duplicate URLs into relationship rows."* |

### Edge C — pipelinenews ← companies (the consumer projection)

`pipelinenews/data/federation/202608282041-relationship-intelligence-contract.json` is the only place the two meet.
It records **three rows** and all three are `ABSTAIN`:

| relationship_family | segment | candidate_rows | requested_role | decision |
|---|---|---|---|---|
| COMPANY_REPD | ALL_CANDIDATES | 482,030 | UNKNOWN | ABSTAIN |
| COMPANY_REPD | SOLAR_SUBSET | 346,233 | UNKNOWN | ABSTAIN |
| DATA_CENTRE_COMPANY | OWNER_OPERATOR_SLOTS | 612 | UNASSERTED_OWNER_OR_OPERATOR_SLOT | ABSTAIN |

Hard gates: `rows: 3`, `project_bindings: 0`, `confirmed_ownership_rows: 0`, `confirmed_operator_rows: 0`,
`all_decisions: ABSTAIN`, `all_eligible_for_join: false`, `landed_duckdb_readback_required: true`.
Acquisition posture: `PINNED_CONTRACTS_ONLY`, max 2 network requests, 0 parallel, 0 redirects, 10 s timeout,
16,384 bytes per contract, hash-and-byte verification before decode, 0 upstream Parquet files copied,
0 upstream person names copied.
Browser projection: max 3 rows, `dynamic-import-on-user-open`, 0 startup requests, must render after core ready,
must not mutate generic news or the project table, `FAIL_CLOSED_WITH_CORE_PRODUCT_UNCHANGED`.

**This is the seam the window-intelligence layer must cross**, and the only legitimate way to cross it is a successor
contract with an explicit evidence rule, per the `future_role_rule` in the companies contract:
*"A new role may be added only by a successor contract with an explicit evidence rule, source provenance and
deterministic validation."*

### Edge D — data-gridatlas → gridatlas (the drawing plane)

| Item | Value |
|---|---|
| Manifest | `https://ventusltd.github.io/data-gridatlas/202608291237-data-gridatlas/data/manifest.json`, sha256 `3246dbdaa042ae8352ec9b7128cb6c2fe65e4f1aba0534302510661828df2526` pinned inside the bridge cartridge |
| Closure asserted by the cartridge | `sources: 56`, `layers: 60`, `features: 541,282` |
| Transport | `streaming-parquet-bridge` monkey-patches `window.fetch`. Eleven `data/*.geojson` paths in the release go to `force-cache`; every other V8 legacy path resolves to `partitions/{stem}.parquet`, is queried in DuckDB-WASM and streamed back as `application/geo+json` |
| Response contract | `HEADERS_BEFORE_PARQUET_BODY` — headers return before the body is reconstructed, so the engine 15 s `fetchWithTimeout` protects establishment only |
| Derived topology | `derived/grid_{400,275,220,132,66}kv_snapped.parquet` — endpoint snapping moved out of the browser |
| Critical path | `grid_400kv.geojson` is served content-addressed from `atlas/releases/cartridges/5f5fbec8…/grid_400kv.geojson` straight to the MapLibre worker; DuckDB prewarm waits until `src-400` reports loaded |
| V8 oracle | `globalgrid2050@f2f343a92ee972cc74ed23b4b99d8a22896791ad`, untouched |

### Edge E — the missing edges

- **companies → gridatlas directly.** Exists only as a URL template. GridAtlas never reads a companies artefact.
- **planning registers → anything.** *No live adapter exists anywhere in the workspace.* PlanIt,
  planning.data.gov.uk, NESO, LCCC and the Gazette are named as allowed sources in
  `pipelinenews/archive/202608261547-pipelinenews/attributionv1/contracts/register-ingest.v1.json`, and a working
  ingest module exists, but nothing calls it against live data.
- **Companies House filing history, charges, PSC.** The acquisition path is the **bulk product only**
  (`download.companieshouse.gov.uk`): `BasicCompanyData*.zip` plus the accounts bulk. Charges, PSC, officers and
  filing history are **not in the bulk basic product** and are therefore not obtainable by the current acquisition
  code. This is the single largest gap between the stated product and the built system — see `companies-engine.md` §5.

---

## 4. Data flow, end to end, as built

```
DESNZ REPD CSV (Q2 2026)  --->  gridatlas/compiler/202608290716-compile-atlas-v9.py
       |                         +-> data/repd_projects_*.parquet (11,069) + browser registry (9.3 MB JSON)
       |
       +--------------------->  globalgrid2050 v9.1 spine build
                                +-> pipelinenews/data/projects/*.json (7,680, 16 partitions)
                                   +-> pipelinenews/data/atlas/*.geojson (per-technology map partitions)

Companies House bulk ZIPs --->  companies/build/python/202608262245-companies-house-source.py   [Actions temp only]
       |                         +-> 202608262245-extract-accounts.py  (XBRL/iXBRL -> 6 balance-sheet facts)
       |                         +-> 202608281337-compact-parquet-companies.py
       |                              |- select: (assets>=10m AND SIC-tagged) OR REPD name candidate OR probable SPV
       |                              |- 294,904 selected companies
       |                              +-> company-repd-relationships-v1.parquet   (3 cols, ZSTD, <=20 MB)
       |
       +--------------------->  companies/contracts/...-federated-company-repd-relationship-contract-v1.json
                                +-> pipelinenews/data/federation/...-relationship-intelligence-contract.json
                                    (3 rows, all ABSTAIN)

V8 GeoJSON corpus (oracle) ---> data-gridatlas/compiler/202608291015-build-v8-transplant.py
                                +-> 56 partitions + 5 snapped topologies + layers/membership Parquet
                                   +-> gridatlas streaming-parquet-bridge cartridge -> MapLibre sources

Elexon BMRS ----------------->  data-gb-electricity (FUELINST/FUELHH/prices Parquet) --> gb-electricity-ui [not wired]
OSM Overpass ---------------->  data-centres-gb (306 elements, 612 ABSTAIN relationships) --> candidate branch only
```

---

## 5. Governance and identity law (the shared constitution)

Every repository obeys the same five rules. Any new layer must too.

1. **Not authorised by default.** Contracts carry `"deployment": "not-authorised"` and `"promotion_eligible": false`
   until a browser-proved gate flips them.
2. **Hash-verified closure.** Nothing is decoded before its bytes are hashed. The gridatlas composer verifies each
   cartridge with `crypto.subtle.digest`; the bridge verifies the data manifest; the search cartridge verifies the
   REPD manifest and Parquet identity; `inoculate.mjs` refuses a vaccine whose sha256 is absent from `vaccines.lock`.
3. **Ledgered.** Timestamped, write-once files. `scope-of-works/*.md` in gridatlas; `manifests/`, `contracts/`,
   `releases/` in pipelinenews and companies. Every contract carries a `recovery_rule`: never overwrite, always
   succeed with a later Europe/London-timestamped file.
4. **Sourced or rejected.** `claim_status ∈ {CONFIRMED, REPORTED, ABSTAIN}`; missing organisation → ABSTAIN;
   contradictions coexist and never overwrite; a name match is a **candidate**, never ownership;
   `CONFIRMED` requires credibility ≥ 0.7.
5. **Organisations, not people.** `attribution-ledger.mjs` throws on any field matching
   `/(^|_)(person|individual|officer|name_of_person)($|_)/i`. Every contract sets
   `directors: false`, `individual_psc: false`, `residential_addresses: false`, `private_individual_names: false`.
   The REPD compile withholds 1,729 possible individual applicants.

**Rule 5 is the one the project-vehicle work must engage with precisely, not around.** See `companies-engine.md` §4.

---

## 6. Route and pointer map (what URL is what)

| Surface | URL | Pointer file of record |
|---|---|---|
| GridAtlas stable | `https://ventusltd.github.io/gridatlas/atlas/` | `gridatlas/atlas/current.json` |
| GridAtlas immutable | `…/gridatlas/atlas/releases/202608300453-atlas-v9/` | `gridatlas/state/live-set.json`, byte-identical to `gridatlas/releases/current-v5.json` (loop.mjs enforces identity) |
| GridAtlas root redirect | `…/gridatlas/` → `./atlas/` preserving `search` and `hash` | `gridatlas/index.html` |
| GridAtlas data plane | `…/data-gridatlas/202608291237-data-gridatlas/` | `data-gridatlas/releases/current.json`, `state/live-set.json` |
| PipelineNews | `…/pipelinenews/releases/202608291447-pipelinenews/` | `pipelinenews/releases/current-v3.json` |
| PipelineNews rollback | `…/pipelinenews/releases/202608271524-v8-fast-candidate.html` | same file, `rollback` block, `PRESERVE_ON_ANY_GRIDATLAS_POINTER_OR_RECEIVER_FAILURE` |
| Companies | none — candidate branch `candidate/202608272155-compact` only | `companies/contracts/202608281337-compact-parquet-companies.json` |
| GlobalGrid2050 | `https://globalgrid2050.com/` | homepage catalogue |

---

## 7. Composition mechanics of the front door (needed by every cartridge)

`gridatlas/atlas/index.html` is a **composer**, not an app:

1. fetch `./current.json` (schema `gridatlas.current.v2`, architecture `IMMUTABLE_SHELL_PLUS_HASHED_CARTRIDGES`)
2. fetch the immutable shell `atlas/releases/{release_id}/index.html`, inject `<base href>`
3. for each id in `cartridge_order`: fetch the cartridge, verify SHA-256, blob-URL it, and **replace the first
   `<script src>` whose basename equals `replace_script`**
4. inject `window.__GRIDATLAS_ATLAS__` state, set `documentElement.dataset.gridatlasGeneration`,
   then `document.write` the composed document
5. on any failure: `document.body.dataset.gridatlasRouter = 'failed'` and the shell is **not** modified

The shell (`202608300453-atlas-v9/index.html`) has exactly **four** replaceable script slots:

| Order in HTML | Slot file | Status |
|---|---|---|
| 1 | `202608292311-maplibre-worker-bridge.js` | **taken** by `streaming-parquet-bridge` |
| 2 | `202608291818-place-postcode-search.js` | **taken** by `uk-gazetteer-flyto` |
| 3 | `ventus-corev8engine.js` | **forbidden** — the engine itself |
| 4 | `202608292126-pre-snapped-config-adapter.js` | **FREE** — the only remaining slot |

Slot 4 runs *after* the engine defines `window.initVentusMap` and *before* the shell inline script calls it. It is
therefore the correct and only place to inject new map layers. Any cartridge taking it **must preserve the existing
pre-snap behaviour** (`snap: false` for layer ids `400, 275, 220, 132, 66`) or the topology will be snapped again in
the browser and the 15 s budget will blow.

Engine facts a layer cartridge depends on:
- `window.initVentusMap({ config, center, zoom })` where `config` is an array of `{ group, layers[] }`
- each layer: `{ id, label, color, type: 'line'|'point', width|radius, url, filter?, preload?, minzoom?, snap?, isSubs? }`
- the engine creates `src-{id}` and `l-{id}`, builds legend rows in `#scada-ui-container` and `#fs-curtain-keys`,
  and hydrates on first checkbox tick via `fetchAndParseGeoJSON(layer.url)` with a 15 s timeout and a 4-way queue
- label text is driven by `updateUIState(id, state, stats)` writing `#lbl-{id}` and `#fs-lbl-{id}`
- the live map instance is exposed by the search cartridge as `window.__GRIDATLAS_V9_MAP__` via a `maplibregl.Map` Proxy

Hard limits enforced by `tools/scope/loop.mjs`:

- cartridge file ≤ **400,000 bytes**
- `atlas/current.json` `live_route` must be `/gridatlas/atlas/`; `release_route` must match `CURRENT_RELEASE`
- `releases/current-v5.json` and `state/live-set.json` must be byte-identical
- exactly the 8 named immutable releases under `atlas/releases/`, zero at root
- exactly the 2 named workflows in `.github/workflows/` (`202608301321-scope-loop.yml`, `202608301321-verify-live.yml`)
- 21 archived workflows under `.github/workflow-archive/202608301321-hostile-amnesia/`
- scope numbers **1..6 only**; a closed master requires exactly 6 done scopes
- `sha256sums.txt` of the current release must verify, with ≥ 20 entries

The last two are blockers for any new build campaign. See `NEXT-VERSION.md` §0.

---

## 8. Governance protocol adoption — actual state

`cvaa` at `d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e` ships 24 vaccines, a hardened `inoculate.mjs` (per-antibody child
process under the Node permission model, `unshare -rn` network namespace where available, 5 s cap, empty env,
banned-API scan, `vaccines.lock` enforcement, SARIF output, per-repo `cvaa.json` ratchet-only baselines with expiry)
and a reusable workflow `.github/workflows/202608301446-inoculate.yml`.

**No repository in the workspace calls it.** There is exactly one `cvaa.json` in existence (cvaa's own). GridAtlas
comes closest: `.github/workflows/202608301321-verify-live.yml` checks cvaa out at the pinned SHA and runs
`inoculate.mjs . --json --no-write` inline, then requires seven named vaccines to be `immune`
(`full-history-checkout`, `no-app-copies`, `pointer-verifies`, `derived-state-not-authored`, `context-diet`,
`registry-integrity`, `no-dangerous-apis`) and asserts `shallow === false`. Everything else in GridAtlas is a
*re-implementation* of the antibodies in `tools/scope/loop.mjs`, and
`governance/202608301524-cvaa-gridatlas-application.md` documents that re-implementation, not an integration.
Full adoption plan in `cvaa-integration-plan.md`.

---

## 9. Where the window-intelligence layer actually sits

Nothing in the workspace is named "window intelligence". Generation `202608300415` in `pipelinenews` is a single
78-line workflow (`.github/workflows/202608300415-advance-successor-to-exact-atlas.yml`, commit `ed03159`,
2026-08-30 05:12 +0100) about advancing the Atlas successor gate. An exhaustive search across all twelve repositories
and their full git history for `window`, `lifecycle`, `ranker`, `corporate-event`, `register-adapter`, `distressed`,
`design freeze`, `freeze overdue`, `PSC` and `persons with significant control` returns nothing matching the
described layer.

The substrate the layer *would* be built on does exist, in three places:

1. **`pipelinenews/archive/202608261547-pipelinenews/attributionv1/`** — the register adapter
   (`modules/register-ingest.mjs`, 96 lines, five official sources with domain-pinned policy), the evidence ledger
   (`modules/attribution-ledger.mjs`, 90 lines, including `attributionsFromRegisteredCharge`), the contradiction view
   (`modules/discrepancy-view.mjs`, 38 lines), the role schema
   (`contracts/attribution-role.v1.schema.json`, 8 roles, 3 claim statuses), the source-law contract
   (`contracts/register-ingest.v1.json`) and three fixture gates
   (`tests/check_batch5_attribution.mjs`, `check_batch6_registers.mjs`, `check_batch7_product.mjs`).
   **Status: CANDIDATE, archived, never wired, no live browser projection, no person-keyed dataset.**
2. **`companies`** — the funding-side selection already tags `probable_project_spv` and emits
   `PROJECT_NAME_SPV_CANDIDATE` for 475,596 edges. **Status: candidate branch, ABSTAIN.**
3. **`gridatlas`** — the receiver, the search lane, the free config slot and the streaming data plane.
   **Status: live.**

`window-intelligence.md` documents each of those completely, states honestly what is present and what is not, and
drafts the wiring that is genuinely missing, in the build order the system implies.
