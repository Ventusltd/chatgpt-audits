# intelligence-chain

The end-to-end journey and the exact contracts at each seam:

```
map feature in gridatlas
   -> deep link
      -> pipelinenews project
         -> company / window intelligence
            -> and back to the map
```

This seam drives contracts and sales, so every hop is stated as a contract with a named identifier, a named
producer, a named consumer and a named proof. Fragilities — including one that is **broken in production today** —
are called out with the repair.

Nothing here was installed. All contract drafts are for review.

---

## 1. The chain at a glance

| Hop | From | To | Identifier passed | Producer | Consumer | Proof of success |
|---|---|---|---|---|---|---|
| **H1** | map feature | deep link | `repd_ref` | gridatlas search cartridge `selectResult()` → `history.replaceState` | the URL bar | `location.search` contains `repd_ref` |
| **H2** | deep link | gridatlas receiver | `repd_ref` | any external surface | `receiveExactRepdDeepLink()` | `document.body.dataset.gridatlasRepdDeepLink === 'resolved'` |
| **H3** | pipelinenews project row | gridatlas | `repd_ref` (+`technology`) | `buildAtlasV9DeepLink(project)` | gridatlas receiver | golden sentinel opens the right project card |
| **H4** | project | canonical id | `gg_project_id = "GG2050-REPD-" + repd_ref` | pipelinenews spine | every governance artefact | `^GG2050-REPD-[0-9]+$` |
| **H5** | canonical id | company candidates | `repd_ref` | companies Parquet | DuckDB reader | FK closure: `unknown_repd_refs = 0` |
| **H6** | company | project vehicle | `company_number` | project-vehicle bindings (draft) | corporate-events adapter | `binding_status = PRIMARY_MATCH` |
| **H7** | window state | map | `repd_ref` + `state` + `window_score` | `project_window_state` Parquet (draft) | window-intelligence cartridge (draft) | feature painted by state, popup cites proof |
| **H8** | map | back out | `repd_ref` | window cartridge popup | pipelinenews / companies surfaces | round-trip returns to the same project |

---

## 2. Hop by hop, with the exact contract

### H1 — map feature → deep link (gridatlas internal)

**Producer.** `atlas/cartridges/202608301624-place-global-search-v9-5.js`, `setDeepLink(result)`:

```js
const url = new URL(window.location.href);
url.searchParams.set('repd_ref', result.repd_ref);
history.replaceState(history.state, '', url);
```

**Rules already enforced.**
- Only a REPD result sets it. `selectLocation()` — the gazetteer lane — **deletes** `repd_ref` before flying, so a
  postcode or a place can never leave a stale project identity in the URL. `result_class: LOCATION_ONLY`,
  `sets_deep_link: false` in `atlas/current.json`.
- `hasSafeMapPoint()` rejects `(0,0)` and the REPD false origin `(49.766807, -7.55716)` before any fly-to.
- `history.replaceState`, not `pushState` — no back-button history pollution.

**Fragility.** The parameter is set even when the fly-to is refused (`canMap === false`); `state.last_selection.mapped`
records the truth but the URL does not. A link copied from a project with no safe coordinate resolves on the
receiving side to a card with no map. That is arguably correct (identity is not geometry) but it should be an
explicit contract clause, not an accident. See §5.1.

### H2 — deep link → gridatlas receiver

**Consumer.** `receiveExactRepdDeepLink(input, resultsEl)` in the same cartridge:

1. read `repd_ref` from `location.search`; absent → `status: 'ABSENT'`, silent
2. `invariant(/^[A-Za-z0-9-]{1,40}$/.test(repdRef))`
3. put the ref in the search box, run `queryOfficialRepd(repdRef)` against the Parquet via DuckDB-WASM
4. `invariant(exact)` — an **exact string match** on `repd_ref`; a near match is a failure, never a substitute
5. `await waitForCapturedMap()` — polls `window.__GRIDATLAS_V9_MAP__` every 50 ms up to **60 s**
6. `selectResult(exact)`; then assert `last_selection.repd_ref === repdRef` **and** `last_selection.mapped === true`
7. success → `document.body.dataset.gridatlasRepdRef = repdRef`, `…RepdDeepLink = 'resolved'`
   failure → `…RepdDeepLink = 'failed'`, error pushed to `window.__GRIDATLAS_PLACE_SEARCH__.failures`, map still usable

**Contract of record.** `gridatlas/contracts/atlas-v9-deep-link-contract.v1.json`:

```
identity.required          ["repd_ref", "technology"]
repd_ref.pattern           ^[A-Za-z0-9-]{1,40}$
technology.allowed         solar | bess | wind_onshore | wind_offshore
optional_evidence          name, longitude, latitude
name_is_identity           false
coordinates_are_identity   false
consumer_base_pointer      https://ventusltd.github.io/gridatlas/state/live-set.json
only_promotion_eligible_release  true
preserve_query_on_root_redirect  true
sentinels                  Beacon Fen 13599 (solar), East Pye 17494 (solar)
```

**Contract mismatch (real).** The contract declares `technology` **required**; the receiver never reads it. Producers
send it, the receiver ignores it. Consequences: (a) a hand-built link with only `repd_ref` works, contrary to the
contract; (b) a producer that sends the *wrong* technology gets no error. Neither is dangerous — identity is the ref
— but the contract and the code disagree and one of them is wrong. Repair in §5.2.

**What works today.** `gridatlas/index.html` at the repo root redirects to `./atlas/` **preserving `search` and
`hash`**:

```js
window.location.replace('./atlas/' + window.location.search + window.location.hash);
```

so `https://ventusltd.github.io/gridatlas/?repd_ref=13599` resolves correctly. `loop.mjs` asserts both that the root
index redirects to `./atlas/` and that it no longer hard-codes a release id.

### H3 — pipelinenews project → gridatlas (the sales link)

**Producer.** `pipelinenews/ui/atlas-v9-deep-links.js`:

```js
const query = new URLSearchParams({ repd_ref: repdRef, technology });
for (const key of ['name', 'longitude', 'latitude']) { ... }
return `${BASE_URL}?${query.toString()}`;
```

**Producer contract.** `pipelinenews/ui/cartridges/202608291504-atlas-pointer-deep-link.mjs` — a *self-validating*
cartridge. At module load it throws unless the injected receipt has
`schema === 'pipelinenews.gridatlas-pointer-receipt.v1'`, `classification === 'VERIFIED_GRIDATLAS_LIVE_POINTER'`,
`query_parameter === 'repd_ref'`, HTTPS, hostname `ventusltd.github.io`, pathname equal to the receipt route, and an
empty query and fragment on the base. `buildAtlasV9DeepLink` returns `""` unless `geometry_status === 'valid'` and
`repd_ref` matches `^\d+$`; the row then presents as `NO MAP`.

Sentinels declared in the cartridge: contractual golden (`16135`), East Pye `17494`, Beacon Fen `13599`, and
invalid-geometry `12780` whose expected URL is `""`.

---

## 3. The break — deep-link base URL drift

**This is the most important finding in this document.**

| Surface | Base URL it emits or claims |
|---|---|
| `pipelinenews/ui/atlas-v9-deep-links.js` | `https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/` |
| `pipelinenews/state/atlas-v9-current.json` | `https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/` |
| `pipelinenews/releases/202608300309-pipelinenews/atlas-link-manifest.json` | `…/gridatlas/202608300453-atlas-v9/`, golden URL `…/?repd_ref=13599` |
| `companies/state/atlas-v9-link-contract.json` | `…/gridatlas/202608300453-atlas-v9/`, template `…/?repd_ref={repd_ref}` |
| **`gridatlas/state/live-set.json` (the pointer of record)** | **stable `/gridatlas/atlas/`, immutable `/gridatlas/atlas/releases/202608300453-atlas-v9/`** |

GridAtlas scope 1 (`scope-of-works/202608301321-01-move-atlas-into-atlas-folder.md`, generation `202608301321`)
moved every release under `atlas/releases/`. `tools/scope/loop.mjs` `validateAtlasLayout()` now **asserts**
`rootReleases.length === 0` and that the root index no longer contains `CURRENT_RELEASE`. Since GitHub Pages serves
the repository tree, `https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/` **no longer exists**.

Every deep link currently produced by pipelinenews and every link built from the companies template therefore
resolves to a 404. The one thing this whole federation was built to do — hand a salesperson a URL that opens the
right project on the map — is broken at the moment of the move.

The pipelinenews receipts were verified against the *older* release `202608291430-atlas-v9`
(`releases/current-v3.json`, `public_proof.receiver_url = …/gridatlas/202608291430-atlas-v9/?repd_ref=16135`,
`pages_run_id 33259747002`), so the last green proof predates the move. Nothing has re-proved the link since.

### Repair — two options, and the recommendation

**Option 1 (recommended): point every consumer at the stable route.**

```
BASE_URL = https://ventusltd.github.io/gridatlas/atlas/
```

Pros: survives every future release promotion without touching a consumer; matches
`consumer_base_pointer` and `only_promotion_eligible_release` intent; the composer already guarantees the stable
route serves the promoted composition. Cons: the consumer is no longer pinned to one immutable release, so a bad
promotion reaches consumers immediately — which is exactly what
`gridatlas/state/live-set.json.verification.promotion_eligible` and the local+public Chromium gates exist to prevent.

**Option 2: point at the immutable release route.**

```
BASE_URL = https://ventusltd.github.io/gridatlas/atlas/releases/202608300453-atlas-v9/
```

Pros: byte-pinned, matches the "never hard-code an unverified candidate" milestone language literally. Cons: the
immutable shell is the **un-cartridged** application. It contains the *original* `202608291818-place-postcode-search.js`,
not the current gazetteer cartridge — so a deep link to the release route gets the older receiver and none of the
v9.5 search behaviour. **This option silently downgrades the product.**

**Recommendation: Option 1**, with the consumer additionally reading
`https://ventusltd.github.io/gridatlas/state/live-set.json` and refusing to build links unless
`verification.promotion_eligible === true` and `verification.failed_gates === 0` — which is precisely what
`docs/milestones/202608300305-atlas-v9-federated-deep-links.md` already specifies as the governing invariant, and
what the self-validating cartridge in pipelinenews is already shaped to do.

### Draft repair contract (for pipelinenews; do not install)

```json
{
  "schema": "pipelinenews.gridatlas-pointer-receipt.v2",
  "generation": "<stamp>",
  "classification": "VERIFIED_GRIDATLAS_LIVE_POINTER",
  "repository": "Ventusltd/gridatlas",
  "resolved_commit": "<commit of the pointer read>",
  "pointer": { "path": "state/live-set.json", "bytes": 0, "sha256": "<hash>" },
  "receiver": {
    "base_url": "https://ventusltd.github.io/gridatlas/atlas/",
    "route": "/gridatlas/atlas/",
    "generation": "202608300453",
    "release_id": "202608300453-atlas-v9",
    "composition_generation": "<atlas/current.json generation>",
    "query_parameter": "repd_ref",
    "golden_repd_ref": "13599",
    "promotion_eligible": true,
    "failed_gates": 0
  },
  "immutable_route_is_uncartridged": true,
  "fallback": { "…": "unchanged last-known-green V8 candidate" }
}
```

Add `composition_generation` so a consumer can tell *which cartridge set* it linked into — today the receipt records
the shell release but not the composition, and the composition is what actually determines receiver behaviour.

---

## 4. H4–H8: the rest of the chain

### H4 — project → canonical id

`gg_project_id = "GG2050-REPD-" + repd_ref`, pattern `^GG2050-REPD-[0-9]+$`.
Enforced in code by `normaliseAttribution()`: `if (input.gg_project_id !== expectedProjectId) throw`.
Derived, never stored, in the companies candidate (`key_authorities.gg_project_id.stored_in_candidate: false`).

### H5 — canonical id → company candidates

`repd_ref` (VARCHAR) into `company-repd-relationships-v1.parquet`. Foreign-key closure is audited:
every relationship `repd_ref` must exist in the pinned 7,680-project universe (`unknown_repd_refs: 0`).

**Cardinality warning that reaches the UI.** A single `repd_ref` can return hundreds of candidate companies, all
`ABSTAIN`. A card that shows them uncritically manufactures the impression of ownership. The display label is
already mandated: **"Company-REPD candidate (name evidence; ownership unconfirmed)"**. Use it verbatim, and
show a **count** plus the evidence-type breakdown by default, never a list of company names.

### H6 — company → project vehicle

`company_number` (`^[A-Z0-9]{8}$`) into the draft `project-vehicle-bindings-v1.parquet`. Only
`binding_status = PRIMARY_MATCH` rows may carry events. Design in `companies-engine.md` §6.3.

### H7 — window state → map

The new hop. `project_window_state` keyed on `(gg_project_id, generation)` and carrying `repd_ref` for the map join.
The cartridge (draft in `DRAFT-CARTRIDGES/`) paints REPD points by `state` and adds a legend group
"Funding window". Popup content, drafted:

```
BEACON FEN ENERGY ENERGY PARK              [FUNDING WINDOW]
500.0 MW solar · South Kesteven · REPD 13599
Entered window 2026-07-14 · rank 3 of 218
Evidence: registered charge created 2026-07-14 (Companies House)
          corporate PSC change 2026-06-30 (Companies House)
Estimated design freeze 2026-11-02 (MEDIUM confidence — derived, not published)
[ Open project ]  [ Open evidence ]
```

Every line is either an official fact with its register named, or explicitly labelled derived. No company is
named as an owner. No score is shown without the terms behind it being reachable.

### H8 — map → back out

Two outbound links from the popup:

| Button | URL | Identifier |
|---|---|---|
| Open project | `https://ventusltd.github.io/pipelinenews/releases/{current}/?repd_ref={repd_ref}` | `repd_ref` |
| Open evidence | `https://ventusltd.github.io/pipelinenews/releases/{current}/window/?gg_project_id=GG2050-REPD-{repd_ref}` | `gg_project_id` |

**Neither exists yet.** PipelineNews has no `repd_ref` inbound receiver — the deep link is currently one-way,
pipelinenews → gridatlas. Making the loop close requires a pipelinenews receiver cartridge symmetrical to the
gridatlas one: read `repd_ref`, exact-match against the 7,680 spine, scroll and highlight the row, set
`document.body.dataset.pipelinenewsRepdRef`, fail closed. Logged as `questions.md` Q6 and as a step in
`NEXT-VERSION.md`.

Outbound link law:
- the map may link **out** with `repd_ref`; it must never post, and never send anything but the ref
- an outbound link must be built from the consumer's own live pointer, never hard-coded — the same rule that this
  document's §3 exists because of

---

## 5. Contract repairs, drafted

### 5.1 Deep link when the project has no safe map point

Add to `gridatlas/contracts/atlas-v9-deep-link-contract.v2.json`:

```json
"resolution_classes": {
  "RESOLVED_AND_MAPPED":   "exact repd_ref found and a safe map point exists; map flies to it",
  "RESOLVED_NOT_MAPPED":   "exact repd_ref found; no safe map point. The card is shown, the map does not move.",
  "NOT_FOUND":             "no exact repd_ref match in the pinned Parquet",
  "MALFORMED":             "repd_ref failed the identity pattern"
},
"body_dataset": {
  "gridatlasRepdRef":      "the ref, on any RESOLVED_* class",
  "gridatlasRepdDeepLink": "resolved | resolved-unmapped | not-found | malformed"
}
```

Today the receiver treats `RESOLVED_NOT_MAPPED` as a **failure** (`invariant(state.last_selection?.mapped === true)`),
so 28 of the 7,680 spine projects with missing geometry — and any of the 11,069 with a false origin — report
`failed` even though identity resolved perfectly. The producer already guards this with
`geometry_status === 'valid'`, but a hand-typed or historical URL does not. Splitting the class removes a false
failure and makes the proof honest.

### 5.2 Reconcile `technology`

Either (a) make the receiver read and validate it, and reject a mismatch against the Parquet row, or
(b) demote it in the contract from `identity.required` to `optional_evidence`.

Recommendation: **(b)**. `repd_ref` is already unique and authoritative; requiring a second field that the receiver
ignores adds a way for a producer to be wrong without being told. Move `technology` to `optional_evidence` alongside
`name`, `longitude`, `latitude`, and keep the producer sending it for readability of the URL.

### 5.3 Record the composition, not just the release

Every receipt should carry `atlas/current.json`'s `generation` and `cartridge_order` alongside the shell
`release_id`. Two links to the same `release_id` can behave differently if the composition changed between them.

---

## 6. Mobile and iPad — what is fragile

Test matrix already defined by `pipelinenews/atman/202608271638-mobile-ui-invariants.mjs`; reuse it:

| cell | viewport | dpr | represents |
|---|---|---|---|
| P1 | 390 × 844 | 3 | iPhone 14/15 portrait |
| P2 | 375 × 667 | 2 | iPhone SE portrait |
| L1 | 844 × 390 | 3 | iPhone 14/15 landscape |
| L2 | 932 × 430 | 3 | iPhone Pro Max landscape |
| L3 | 667 × 375 | 2 | iPhone SE landscape |
| L4 | 852 × 393 | 3 | iPhone 16 landscape |
| T1 | 768 × 1024 | 2 | the 768 px breakpoint boundary |
| R1 | rotate P1↔L1, 3 cycles, 250 ms settle | 3 | orientation churn |

### 6.1 The five real fragilities

**F1 — DuckDB-WASM on a 1 GB phone. Severity: high.**
The deep-link receiver **cannot resolve without DuckDB**: `receiveExactRepdDeepLink` → `queryOfficialRepd` →
`runtime()` → dynamic `import('https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm')` → bundle selection
→ a Worker → `database.instantiate()`. On a low-memory device this is tens of megabytes of WebAssembly plus a
1.45 MB Parquet before a single pixel of the project moves. The build request already sets a **400 MB heap budget**
(`state/streaming-road-fix.json`) — that budget is for the A-road layers, and a 1 GB phone has far less headroom
than that once Safari's per-tab limit applies.
*Consequence:* on a constrained phone the deep link times out at the 60 s `waitForCapturedMap` boundary, or the tab
is reclaimed, and the salesperson sees a map with no project.
*Mitigation (design, in `DATA-DELIVERY-PLAN.md`):* ship a **tiny exact-ref index** — `repd_ref → {name, lon, lat,
technology, capacity, status}` — as a static, hash-pinned JSON or a per-outcode shard, ~200–400 KB gzipped for all
11,069 rows, and resolve the deep link from that **first**, promoting to DuckDB only for free-text search. Deep-link
resolution then costs one small fetch and works on any device.

**F2 — `user-scalable=no`. Severity: medium (accessibility and iPad).**
The shell head carries `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0,
user-scalable=no">`. iOS Safari has ignored `user-scalable=no` since iOS 10 for accessibility reasons; Chrome on
Android honours it. So pinch-zoom on the page chrome differs between an iPad and an Android phone, and the setting
fails WCAG 1.4.4. The map itself handles its own gestures, so removing the restriction costs nothing functionally.
*Repair:* `content="width=device-width, initial-scale=1, viewport-fit=cover"` — but this is a **shell** change and
the shell is immutable. It therefore belongs in a future shell release, not a cartridge. Recorded in
`NEXT-VERSION.md` as a deferred shell item.

**F3 — Fullscreen on iPhone. Severity: low (already degrades well).**
`enterFullscreen()` adds `.fs-active` classes and `.is-fullscreen` (`position: fixed; width: 100vw; height: 100dvh`)
*before* attempting `requestFullscreen()`/`webkitRequestFullscreen()`. On iPhone Safari, element fullscreen is
unavailable, both calls no-op or reject (the promise rejection is caught), and the CSS fallback carries the UI. The
`fullscreenchange` / `webkitfullscreenchange` listeners never fire, so exit depends entirely on the `✕ Exit` button —
which is present. **This is good defensive code**; the only risk is a future cartridge assuming
`document.fullscreenElement` is meaningful. Note it, do not change it.

**F4 — The layer curtain at two columns. Severity: medium.**
`#fs-curtain-keys` and `.scada-keys` are `grid-template-columns: 1fr 1fr`, collapsing to one column only below
480 px. At **768 × 1024 (iPad portrait, cell T1)** they stay two-column, and `.scada-wrapper` is capped at `38vh`
(28vh under `max-height: 600px`). Adding a **new layer group** — which the window-intelligence cartridge does —
pushes the existing 11 groups and 60 layers further down a scrollable panel that is already only ~390 px tall on an
iPad. The new group must therefore be inserted **first** in the config array, not appended, or it will be
invisible without scrolling on the device most likely to be used in a meeting.
*This is a cartridge-level decision and costs nothing to get right; getting it wrong costs the demo.*

**F5 — Third-party geocoders from a browser. Severity: medium (policy, not code).**
The search cartridge calls `https://api.postcodes.io` on every keystroke (180 ms debounce) and
`https://nominatim.openstreetmap.org/search` on Enter or the GO button. Nominatim's usage policy expects an
identifying User-Agent or Referer and roughly one request per second; a browser cannot set User-Agent, and a busy
demo can exceed the rate. The code already restricts Nominatim to explicit activation (not keystrokes) and
de-duplicates against the UK lane, which is the right shape. Neither service has a source card in `spiders`.
*Repair:* add source cards for `postcodes.io` and `nominatim`, record the rate expectation and the attribution
requirement, and keep global search on explicit activation only. Recorded in `spiders-feeds.md`.

### 6.2 Things that are already right on mobile

- `height: 100vh; height: 100dvh` on `.dashboard` and `.is-fullscreen` — handles the iOS dynamic toolbar correctly
- `new ResizeObserver(() => map.resize()).observe(mapEl)` — orientation change is handled without a resize listener
- `max-width: calc(100vw - 40px)` on the measure and poly-zone readouts
- `@media (max-height: 600px)` shrinks the SCADA panel for landscape phones
- `:focus-visible` outlines on every control
- search input `keydown` handlers call `stopImmediatePropagation` so the map never steals typing
- the search results panel hides on map click, which is also the on-screen-keyboard dismissal path

### 6.3 Mobile gate to add for any new cartridge

Run the existing device matrix against a locally served composition and assert:

1. the composition loads and `document.documentElement.dataset.gridatlasGeneration` equals the expected generation
2. a golden deep link (`?repd_ref=13599`) reaches `gridatlasRepdDeepLink = 'resolved'` **within 15 s** on the P2 cell
   (375 × 667) — the tightest realistic device
3. the new legend group is visible **without scrolling** on T1 (768 × 1024)
4. `window.performance.memory.usedJSHeapSize` (Chromium) stays under the declared budget after the new layer
   hydrates
5. three rotate cycles (R1) leave the map sized correctly and the deep-link dataset attribute unchanged
6. zero uncaught exceptions and zero failed network requests to a non-allowlisted host

---

## 7. What the seam is worth commercially, and what protects it

The chain is the product surface a customer touches, so each contract clause maps to a sales promise:

| Promise | Clause that keeps it honest |
|---|---|
| "This link opens that exact project." | `EXACT_REPD_REF_ONLY`; `name_is_identity: false`; `coordinates_are_identity: false` |
| "We are not guessing who owns it." | `identity_posture: CANDIDATE_ONLY_NOT_CONFIRMED_OWNERSHIP`; display label mandated |
| "This is from the register, not the press." | `evidence_domain` pinned per source; `official_register_credibility: 1` |
| "We will tell you when it enters the window, not after." | window-state generation cadence + `WINDOW_ENTRY` alert |
| "We will tell you when we are wrong." | contradictions coexist; `CONFLICTS_WITH_CONFIRMED` is a visible state |
| "We do not hold data on individuals." | `assertNoPersonKeys`; count-only director and individual-PSC events |
| "If it breaks, the previous version is still there." | `rollback` blocks in every pointer; `last_known_green` |

The single largest commercial risk in this document is **§3**: every link the sales motion depends on is currently
a 404. Fixing that is one file in pipelinenews, one file in companies, and a re-proof — and it should happen before
any new capability is added on top.
