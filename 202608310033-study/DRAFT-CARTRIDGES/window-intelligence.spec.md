# Cartridge spec — `window-intelligence`

One page. Draft. Not installed.

| | |
|---|---|
| **id** | `window-intelligence` |
| **draft** | `./window-intelligence.js.txt` |
| **type** | `script` |
| **slot** | `replace-script` → `202608292126-pre-snapped-config-adapter.js` |
| **contract module** | `ui/cartridges/<gen>-window-intelligence.mjs` (to be written at build time) |
| **delivery type** | `map-ready-geojson` — five static, hash-pinned artefacts, one per state |
| **runtime dependencies** | none new. Uses MapLibre already loaded by the shell and the `window.__GRIDATLAS_V9_MAP__` handle the search cartridge exposes. **No DuckDB.** |

---

## 1. Purpose

Show on the map which projects are in the funding window **now**, ranked by timing rather than size, with the
register evidence that put them there and an estimated design-freeze date explicitly labelled as derived.

This is the visible surface of the product thesis: studies, cable and LV design are bought *before* design freeze;
this cartridge is where a supplier sees which sites reached that point this month.

---

## 2. Feeding data source

Published by `pipelinenews` from the `project_window_state` and `window_evidence` datasets drafted in
`window-intelligence.md` §12.6.

```
<WINDOW_BASE>/window-map-manifest.json     schema pipelinenews.window-map-manifest.v1
<WINDOW_BASE>/funding.geojson              state = FUNDING_WINDOW
<WINDOW_BASE>/procuring.geojson            state = PROCURING
<WINDOW_BASE>/consented.geojson            state = CONSENTED
<WINDOW_BASE>/frozen.geojson               state = DESIGN_FROZEN
<WINDOW_BASE>/distressed.geojson           state = DISTRESSED
```

**One file per state, deliberately.** The engine hydrates a layer only when its checkbox is ticked, so a user who
opens only "Funding window" downloads only the funding-window projects — the smallest and most valuable file.
A single combined file would force every state's bytes on every user and would duplicate all features across five
MapLibre sources, because the engine gives every non-REPD layer its own `src-{id}`.

### Feature properties (drawn payload)

| property | type | source |
|---|---|---|
| `repd_ref` | string | spine — the join key and the deep-link identity |
| `name` | string | spine |
| `technology` | string | spine |
| `capacity_mw` | number | spine |
| `planning_authority` | string | spine |
| `county` | string | spine |
| `state` | string | one of the eight |
| `entered_state_at` | date string | earliest proof row for this state |
| `window_score` | number 0–1 | ranker |
| `window_rank` | integer | ranker |
| `window_total` | integer | ranker — so the popup can say "3 of 218" |
| `freeze_estimate_at` | date string \| null | derived, null until calibrated |
| `freeze_estimate_confidence` | `LOW`/`MEDIUM`/`HIGH` \| null | derived |
| `nearest_circuit_kv` | number \| null | C6 precomputed |
| `nearest_circuit_km` | number \| null | C6 precomputed |
| `proof_json` | string | JSON array of `{kind, register, date}` — max 5 rows |

Nothing else. No company names, no ownership, no score components, no person data.
`proof_json` is a string because MapLibre feature properties are flat.

---

## 3. Why this slot, and the obligation it carries

The shell has four `<script src>` slots. Two are taken, one is the engine (forbidden), and one is free:
`202608292126-pre-snapped-config-adapter.js`. It is the **only** point at which `window.initVentusMap` exists and has
not yet been called, so it is the only point at which the layer config can be extended.

The script being replaced does one thing: it rewrites `snap: true → false` for layer ids `400, 275, 220, 132, 66`,
because `data-gridatlas` now ships `derived/grid_*_snapped.parquet` with the endpoint snapping already applied. If
this cartridge does not reproduce that rewrite, `hydrateLayer` calls `snapLines()` at runtime over
4,106 + 2,935 + 126 + 6,227 + 1,171 = **14,565** line features against 5,800 substations — an O(n·m) loop in the main
thread. That is the exact behaviour the v9.5 work removed.

The draft therefore performs the identical rewrite **first**, asserts the same closure
(`JSON.stringify(changed.sort()) === JSON.stringify(['132','220','275','400','66'])`), and **throws on mismatch**
rather than continuing. A pre-snap failure is not recoverable by disabling the window layer.

---

## 4. Behaviour

1. Capture `originalInit = window.initVentusMap`; if absent, record and return without patching anything.
2. Capture `upstreamFetch = window.fetch` — which at this point is the `streaming-parquet-bridge`'s fetch, not the
   platform's. Chaining onto it rather than the platform preserves both bridges.
3. On `initVentusMap(options)`:
   a. pre-snap rewrite (throws on failure)
   b. fetch and SHA-256-verify the window manifest; assert schema, generation format, spine `project_count === 7680`
      and spine `projects_sha256`, a declared digest for every state file, and the presence of the ranker contract
   c. install a narrow `window.fetch` interceptor scoped to exactly the five window URLs, which verifies each
      payload digest before returning it
   d. prepend the `Funding window` group to the config and call `originalInit`
   e. poll for `window.__GRIDATLAS_V9_MAP__` (50 ms, 60 s cap), then bind popups and legend-count upgrades
4. On any manifest failure: record it, call `originalInit` with the **pre-snapped but otherwise unmodified** config,
   and log. No layers, no popups, product identical to today.

### Legend counts

The engine's generic hydrate path calls `updateUIState(id, 'OK')` with no stats, so the label reads
`Funding window [OK]`. The cartridge listens for `sourcedata` with `isSourceLoaded`, counts distinct `repd_ref`,
sums `capacity_mw`, and rewrites `#lbl-{id}` / `#fs-lbl-{id}` to `Funding window [218 | 6.4GW]` using the same
`[count | unit]` format the engine uses elsewhere. Purely a DOM write; absent elements are ignored.

### Popup

Registered after the engine's, so `window._closePopupKeepShape?.()` closes the engine's popup before ours opens.
Content is specified in `intelligence-chain.md` §4 H7. Three phrasing rules are load-bearing:

- the freeze date always reads **"Estimated design freeze … (derived by GridAtlas, not published)"**
- the grid distance always reads **"straight line, screening only — not a route or a connection"**
- the footer always reads **"Official registers only. No ownership is asserted."**

---

## 5. Size and budget

| item | figure | at 20 Mbit |
|---|---|---|
| cartridge JS | ~14 KB (cap is 400,000 B) | negligible |
| manifest | ~4 KB | negligible |
| `funding.geojson` | expected low hundreds of features; worst case bounded by the spine | — |
| all five files combined | ≤ 7,680 features ≈ 1.8 MB raw / ~600 KB gzip | 0.72 s raw, 0.24 s gzip |
| first load cost | **0 bytes** — every layer is `preload: false` | 0 s |
| heap after all five hydrate | 7,680 point features, comparable to `grid_substations` (5,800) and `industrial_offtakers` (5,878), both live today | well under the 400 MB cap |

The cartridge adds **nothing** to first paint. The manifest fetch is the only load-time request and it is 4 KB.

---

## 6. Open points to resolve before installing

1. **`initVentusMap` becomes asynchronous.** The shell calls `window.initVentusMap({...})` and discards the return
   value, and the engine's own return value is unused, so returning a promise is safe against *this* shell. It is
   still a behaviour change and must be **proved in the browser gate**, not assumed. If it proves unsafe, the
   fallback is to install layers synchronously with a placeholder empty source and populate them after verification —
   at the cost of a brief empty legend entry.
2. **Two `window.fetch` patches now exist.** `streaming-parquet-bridge` (slot 1) and this cartridge (slot 4). The
   chain is bridge → window. The gate must assert both still work: an A-road layer must still hydrate from Parquet
   **and** a window layer must still hydrate from its verified GeoJSON, in the same session.
3. **Group ordering.** The group is prepended. Confirm on the 768 × 1024 cell that "Funding window" is visible
   without scrolling in both `#scada-ui-container` and `#fs-curtain-keys`.
4. **`window_score` radius.** Confirm the interpolation reads sensibly when most scores cluster; if the distribution
   is tight, switch to a rank-based radius (`window_rank <= 10` large, etc.) rather than a score-based one.
5. **`WINDOW_BASE` cross-origin.** The artefacts are served from the `pipelinenews` Pages origin, not `gridatlas`.
   GitHub Pages sets permissive CORS for static assets, but this must be verified in the browser gate, not assumed.
   If it fails, mirror the five artefacts into `gridatlas/data/window/` at build time and pin them there.

---

## 7. Acceptance gate (browser, local then public)

1. composition loads; `document.documentElement.dataset.gridatlasGeneration` equals the expected generation
2. `window.__GRIDATLAS_WINDOW__.pre_snap_applied === true` and
   `pre_snap_changed_layer_ids` sorted equals `['132','220','275','400','66']`
3. `window.__GRIDATLAS_WINDOW__.manifest_verified === true`, `failures.length === 0`
4. legend group `Funding window` exists and is the **first** group in `#scada-ui-container`
5. ticking `win_funding` reaches label `[n | …]` with `n >= 1` in **< 15 s**, heap under 400 MB
6. clicking a rendered funding-window point opens a popup containing the exact strings
   `Estimated design freeze`, `screening only`, and `No ownership is asserted.`
7. `?repd_ref=13599` still resolves — `document.body.dataset.gridatlasRepdDeepLink === 'resolved'`
8. an A-road layer (`trunk_roads`) still hydrates from Parquet in the same session — both fetch patches coexist
9. **negative test:** serve a manifest with one byte changed; assert `applied === false`, zero window layers, the
   400 kV layer still renders, and the deep link still resolves
10. zero uncaught exceptions, zero requests to a host outside
    `{ventusltd.github.io, cdn.jsdelivr.net, api.postcodes.io, nominatim.openstreetmap.org,
    basemaps.cartocdn.com, server.arcgisonline.com}`

---

## 8. Rollback

Revert `atlas/current.json` to the previous generation and the previous `cartridge_order`. The immutable shell is
untouched, the previous cartridges remain on disk, and `state/live-set.json` still names the same release. No data
artefact is deleted. Rollback is one file and one commit.
