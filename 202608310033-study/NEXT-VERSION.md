# NEXT-VERSION

The complete step-by-step build plan: which cartridges to install in what order, their dependencies, and what to
**test on the live product after each step**. Written so it can be executed without rediscovering anything.

Every step has: **why**, **exact files touched**, **the command**, **the live test**, **the promotion gate**, and
**the rollback**. Steps are numbered `N0…N14`. Nothing here has been executed.

---

## 0. Read this before touching anything

### 0.1 The frame

`globalgrid2050` is the **origin hub**, being deliberately big-banged out into specialised repos and apps, each with
its own repo and its own data. The Parquet + DuckDB layer exists precisely to carve the monolith into queryable
specialised pieces. The apps radiating from it include electricity price and intelligence, the GIS/SLD financial
sandbox, gridatlas, the solar / electrical / cable-topology engineering apps, pipelinenews, and the data repos
beneath them.

Consequences that shape this plan:

- **The 240 workflows in `globalgrid2050` are intentionally paused, not abandoned.** Live apps consume the data they
  produce, and the runs are held on purpose so nothing is lost during the split. Do not "clean them up".
- **Its debt is transitional.** It shrinks as pieces move out. Measuring it is useful; failing a build on it is not.
- **The real risk of a federation mid-split is not decay, it is broken seams** — a consumer left pointing at a
  producer that reorganised. That has already happened once, in production, and it is `N1`.
- **An existing dashboard already maps every workflow and every app-to-data dependency.** That dashboard is the
  topology source of truth. This plan does not duplicate it; `N14` proposes wiring cvaa to it. See
  `questions.md` Q0 — locating it is the first thing a future session should do.

### 0.2 Hard constraints in the gridatlas repo (measured, not assumed)

These will stop a build if you do not handle them. All are enforced by `tools/scope/loop.mjs`, which
`.github/workflows/202608301321-verify-live.yml` runs before **and** after every change.

| # | Constraint | Where | What to do |
|---|---|---|---|
| B1 | Scope numbers must be **1..6**; a closed master requires **exactly 6 done scopes** | `loop.mjs` `validateScopeLedger()` | See `N0` — this is the first blocker |
| B2 | `.github/workflows/` must contain **exactly** `202608301321-scope-loop.yml` and `202608301321-verify-live.yml` | `loop.mjs` `validateWorkflowBudget()` via `ACTIVE_WORKFLOWS` in `tools/scope/lib.mjs` | Any new workflow must be added to `ACTIVE_WORKFLOWS` **in the same commit** |
| B3 | Exactly **21** archived workflows under `.github/workflow-archive/202608301321-hostile-amnesia/` | same | Do not add or remove archived files |
| B4 | Cartridge file **≤ 400,000 bytes** | `loop.mjs` + `pointer-verifies` vaccine | Both draft cartridges are ~14–20 KB |
| B5 | `releases/current-v5.json` and `state/live-set.json` must be **byte-identical** | `loop.mjs` `validateAtlasLayout()` | Edit both or neither |
| B6 | Exactly the **8** named releases under `atlas/releases/`, **0** at root | `loop.mjs` + `verify-compose.mjs` | Never add a release directory |
| B7 | `atlas/current.json` `live_route` must be `/gridatlas/atlas/`, `release_route` must be `/gridatlas/atlas/releases/202608300453-atlas-v9/` | `loop.mjs` | Do not "improve" these strings |
| B8 | `STATE.md` must byte-match `node tools/scope/loop.mjs state --stdout` | `derived-state-not-authored` vaccine + `AGENTS.md` | Regenerate in the same commit, never hand-edit |
| B9 | `verify-compose.mjs` asserts **eight literal markers** inside the gazetteer cartridge and two inside its contract | `tools/scope/verify-compose.mjs` | See `N2` — a superseding search cartridge must keep every marker |
| B10 | **One free shell slot only:** `202608292126-pre-snapped-config-adapter.js` | shell `index.html` | Any cartridge taking it must reproduce the pre-snap rewrite |

### 0.3 The markers `verify-compose.mjs` requires (B9, quoted exactly)

In the cartridge named by `uk-gazetteer-flyto`:

```
GEOCODER_BASE = 'https://api.postcodes.io'
Promise.all([
kind: 'postcode'
kind: 'postcode_district'
kind: 'place'
url.searchParams.delete('repd_ref')
serial !== activeQuerySerial
geocoder_failures
```

In `ui/cartridges/202608301136-uk-gazetteer-flyto.mjs`:

```
resultClass: 'LOCATION_ONLY'
setsDeepLink: false
```

The `exact-ref-index` draft is expressed as **anchored replacement blocks over the pinned parent** precisely so that
every one of these survives untouched.

### 0.4 The standing promotion gate

`202608301321-verify-live.yml` is already the promotion machine. Do not write a second one. Its sequence:

```
1  checkout gridatlas  (fetch-depth 0)  + cvaa @ pinned SHA (fetch-depth 0)
2  node 22.18.0, npm ci, playwright chromium
3  build ONE cartridge from a request file in state/
4  node tools/scope/verify-compose.mjs
5  assert build report: full_application_copies_created == 0, immutable_shell_modified == false
6  assert atlas/current.json generation == this run's UTC minute; cartridge_order exact
7  node tools/scope/loop.mjs state          -> regenerates STATE.md
8  git add ONLY the allowed file set; assert nothing else is staged; commit locally
9  node work/cvaa/inoculate.mjs . --json --no-write
      require 7 vaccines immune, shallow == false
10 serve the exact committed tree on 127.0.0.1:4173
11 LOCAL Chromium proofs
12 push only if 9 and 11 passed and HEAD^ == origin/main
13 request Pages build; poll public atlas/current.json for the exact generation
14 PUBLIC Chromium proofs
15 upload every proof as a 90-day artifact
```

**Every step below plugs a new proof script into 11 and 14. Nothing else about the machine changes.**

---

## N0 — Unblock the scope ledger

**Why.** `loop.mjs` hard-codes `scope >= 1 && scope <= 6`, and with the master `done` it also asserts
`scopes.length === 6 && every status === 'done'`. Scope 7 cannot exist. Every step after this needs a ledger entry
(`on-ledger-commits` vaccine) and `AGENTS.md` requires the loop to pass before handover.

**Files touched (gridatlas):**

```
tools/scope/loop.mjs                    scope range and the closed-master assertion
scope-of-works/202608301321-scope-of-works.md   master reopened: status active, active_scope 7
scope-of-works/<stamp>-07-<slug>.md     new scope 7, status active, parent = scope 6 file
scope-of-works/202608301524-06-...md    add `next:` pointing at scope 7
scope-of-works/202608301525-closure.md  supersede, do not delete
STATE.md                                regenerated
```

**Two options, choose deliberately:**

| option | change | cost |
|---|---|---|
| **A (recommended)** | Replace the literal `6` with a `MAX_SCOPE` constant in `lib.mjs` and make the closed-master check `scopes.length === MAX_SCOPE` | one constant, one commit, the campaign continues in the same ledger |
| B | Leave the six-scope chain closed as a historical record and start a **second** ledger (`scope-of-works-v2/`) with its own master | more faithful to "write-once", but `loop.mjs`, `advance.mjs` and `bootstrap.mjs` all hard-code `SCOPE_DIR` |

Option A is smaller and keeps one ledger, which is what `one-active-scope` and `on-ledger-commits` are shaped for.

**Also required now (B2):** add `executor: script` to all existing scope files. The `executor-declared` vaccine
fires on every scope file without it, and `loop.mjs` ignores unknown front-matter keys, so this is additive.

**Command:**

```bash
node tools/scope/loop.mjs lint
node tools/scope/loop.mjs state --stdout | diff - STATE.md
```

**Live test:** none — no application change. The map must be untouched.
**Gate:** `lint` PASS, `state --stdout` byte-matches `STATE.md`, `git status` shows only the named files.
**Rollback:** revert the commit. No published artefact moved.

---

## N1 — Fix the broken production deep-link seam ★ DO THIS FIRST

**Why.** This is the live sales path and it is currently **404**. `pipelinenews/ui/atlas-v9-deep-links.js` and
`companies/state/atlas-v9-link-contract.json` both emit

```
https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=...
```

but gridatlas scope 1 moved every release under `atlas/releases/`, and `loop.mjs` now *asserts*
`rootReleases.length === 0`. The path no longer exists. Full analysis: `intelligence-chain.md` §3.

This is also the exact disease of a federation mid-split: a consumer left pointing at a producer that reorganised.
It is why the `consumer-pointer-current` vaccine (`cvaa-integration-plan.md` §5 V1) matters more than any other.

**Decision, already argued in `intelligence-chain.md` §3:** point consumers at the **stable route**
`https://ventusltd.github.io/gridatlas/atlas/`, not the immutable release route. The immutable release route serves
the **un-cartridged** shell — it contains the original `202608291818-place-postcode-search.js`, not the v9.5
gazetteer cartridge — so pinning there silently downgrades the product.

**Files touched — `pipelinenews`:**

```
ui/atlas-v9-deep-links.js                       BASE_URL -> https://ventusltd.github.io/gridatlas/atlas/
state/atlas-v9-current.json                     base_url, add composition_generation
ui/cartridges/<stamp>-atlas-pointer-deep-link.mjs   successor, schema ...gridatlas-pointer-receipt.v2
releases/<stamp>-pipelinenews/                  new timestamped release carrying the corrected receipt
releases/current-v3.json                        pointer moves only after the sentinel proof passes
```

**Files touched — `companies`:**

```
state/<stamp>-atlas-v9-link-contract.json       successor; never overwrite the 202608300415 file
scripts/<stamp>-build-atlas-v9-company-repd-links.py   emit the stable route
```

**Consumer rule to encode in the v2 receipt** (already the governing invariant in
`docs/milestones/202608300305-atlas-v9-federated-deep-links.md`): refuse to build links unless the fetched
`gridatlas/state/live-set.json` has `verification.promotion_eligible === true` **and**
`verification.failed_gates === 0`. Also record `composition_generation` from `atlas/current.json`, because two links
to the same `release_id` can behave differently if the cartridge set changed.

**Live test — run these four URLs in a real browser, desktop and iPad:**

| URL | expected |
|---|---|
| `https://ventusltd.github.io/gridatlas/atlas/?repd_ref=13599` | Beacon Fen card + fly-to; `document.body.dataset.gridatlasRepdDeepLink === 'resolved'` |
| `https://ventusltd.github.io/gridatlas/?repd_ref=13599` | root redirect preserves the query; same result |
| `https://ventusltd.github.io/gridatlas/atlas/?repd_ref=17494` | East Pye |
| the old `.../gridatlas/202608300453-atlas-v9/?repd_ref=13599` | **404 — confirm the disease before and after** |

Then, from the pipelinenews live release, click through to the map from a project row and confirm it lands.

**Gate.** Both golden sentinels (`13599`, `17494`) resolve from a link built by the corrected producer, in a real
browser, with `route_interceptions: 0` and `synthetic_receiver: false` — the same evidence shape
`releases/current-v3.json` already records. Only then move the pipelinenews pointer.

**Rollback.** `pipelinenews/releases/current-v3.json` `rollback` block already names
`202608271524-v8-fast-candidate.html` with `PRESERVE_ON_ANY_GRIDATLAS_POINTER_OR_RECEIVER_FAILURE`. Do not touch it.

---

## N2 — Install the `exact-ref-index` cartridge

**Why.** A deep link currently cannot resolve without booting DuckDB-WASM: 35.7 MB, **14.28 s of a 15 s budget at
20 Mbit** before any project data moves. On a 1 GB phone the link times out or the tab is reclaimed. `N1` makes the
URL correct; `N2` makes it *arrive*. Spec: `DRAFT-CARTRIDGES/exact-ref-index.spec.md`.

**Files touched (gridatlas):**

```
compiler/<stamp>-build-repd-ref-index.py          new; the sketch is in the draft, Block 5
data/repd_ref_index_<stamp>.json                  new artefact, ~1.05 MB raw / ~340 KB gzip
tools/v9_5/<stamp>-build-search-cartridge.py      applies the anchored blocks to the pinned parent
atlas/cartridges/<stamp>-place-global-search-v9-6.js
ui/cartridges/<stamp>-uk-gazetteer-flyto.mjs      must keep resultClass/setsDeepLink markers (B9)
atlas/current.json                                cartridge entry + sha256 + generation
atlas/manifests/<stamp>-composition.json
STATE.md                                          regenerated
state/<stamp>-exact-ref-index-request.json        the build request, modelled on state/streaming-road-fix.json
```

**Build the index first, and assert as you build:**

```
rows == 11069
unique repd_ref == 11069
parquet_sha256 == 174040c37f3d63742d6fdd7af722a8cfdf3fb53de3ff85ff1142d22fdac4866b
row form == [name, technology, status, capacity_mw, longitude, latitude]
```

**Do NOT reuse `data/repd_browser_registry_202608290716.json`** — 9,328,402 bytes, 3.7 s at 20 Mbit, for data a deep
link does not need.

**Two things that will bite (both already checked):**

1. `atman/202608301624-verify-v9-5-search.mjs` waits on the literal string `deep_link?.status === 'RESOLVED'`. The
   draft deliberately keeps that value for the mapped case and puts the new information in `resolution_class`.
   **Do not rename it.**
2. The same verifier asserts `window.__GRIDATLAS_PLACE_SEARCH__.generation === EXPECTED_SEARCH_GENERATION`. Bump the
   cartridge constant **and** pass the new value in the workflow env, together.

**Live test on the real product, after promotion:**

| # | test | expected |
|---|---|---|
| 1 | open `/gridatlas/atlas/` on desktop | map loads as before, 400 kV renders |
| 2 | `?repd_ref=13599` on desktop | Beacon Fen resolves in **under 3 s** |
| 3 | in the console: `__GRIDATLAS_PLACE_SEARCH__.duckdb_booted_for` | **`null`** — DuckDB never started |
| 4 | `__GRIDATLAS_PLACE_SEARCH__.ref_index` | `{loaded:true, verified:true, rows:11069, ms:<3000}` |
| 5 | **on a phone, on mobile data**, `?repd_ref=13599` | resolves; this is the whole point |
| 6 | type `Beacon Fen` in the search box | `13599` first; `duckdb_booted_for` now set — search still works |
| 7 | type `SW1A 1AA` | postcode lane still works, popup still says *"Location only · postcodes.io · no project identity claimed"* |
| 8 | type `Delhi` and press GO | global lane still works |
| 9 | `?repd_ref=12780` | `resolved-unmapped`; map does **not** fly to a false origin |
| 10 | `?repd_ref=99999999` | `not-found`, no exception |

**Gate.** All ten pass locally and publicly; `atman/202608301624-verify-v9-5-search.mjs` passes unchanged;
`verify-compose.mjs` PASS; `loop.mjs lint` PASS; cvaa's seven selected vaccines immune.

**Rollback.** Revert `atlas/current.json` to the previous generation and `cartridge_order`. The index artefact may
stay on disk unused — it is content-addressed and inert. One file, one commit.

---

## N3 — Adopt cvaa on gridatlas

**Why.** cvaa's real job in this federation is keeping the **seams** coherent while pieces move out of the hub.
`N1` proved the seam can break silently. gridatlas is ~90 % compliant already and is the repo the vaccines were
written from, so adopting it converts a re-implementation into a real dependency.

**Files touched (gridatlas), all in one commit:**

```
.github/workflows/<stamp>-inoculate.yml     copied from cvaa/consumer-workflow-template.yml
                                            both SHAs = d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e
tools/scope/lib.mjs                         ACTIVE_WORKFLOWS gains '<stamp>-inoculate.yml'   (B2)
cvaa.json                                   the baseline drafted in cvaa-integration-plan.md §3.1
STATE.md                                    regenerated (Active workflows becomes 3)
```

**Before setting the baselines, measure them:**

```bash
git clone --depth=0 https://github.com/Ventusltd/cvaa work/cvaa   # or reuse the checkout
git -C work/cvaa checkout d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e
node work/cvaa/tools/selftest.mjs
node work/cvaa/inoculate.mjs . --json --no-write
```

Set every `max` to the **measured** count, not the estimate in `cvaa-integration-plan.md`. Baselines only ratchet
down, so starting too low is a build failure and starting too high is permanent debt.

**Cure rather than baseline, if there is time:** `executor-declared` (8 findings, cured by one front-matter line per
scope file — already done in `N0`).

**Live test.** None on the map. This step must be provably inert to the product.
**Gate.** The inoculate workflow runs green (or warning-only within the baseline); `loop.mjs lint` still PASS with
three active workflows; `verify-live.yml` still passes end to end; the public map is byte-identical.
**Rollback.** Delete the workflow and revert `ACTIVE_WORKFLOWS`. Two lines.

---

## N4 — The design-freeze calibration

**Why.** It is the **only** item in the whole plan with no dependency, no new source, no new privacy question and no
network access. It is pure arithmetic over a frozen file already in the repository, and it converts two of the three
alerts from impossible to possible. It can be done tonight.

**Files touched (pipelinenews):**

```
build/python/<stamp>-calibrate-design-freeze.py
contracts/<stamp>-design-freeze-calibration.json      deployment: not-authorised
```

**Method.** Over the 7,680-project spine, for every project that reached `under construction`, compute
`under_construction - planning_permission_granted` in days. Take the median per `(technology, capacity_band)`, and
record the sample size per cell.

```
technology     solar | bess | wind_onshore | wind_offshore
capacity_band  1-5 | 5-20 | 20-50 | 50-100 | 100-250 | 250+ MW
```

**Rules.** A cell with **fewer than 30 samples is NULL**, not a guess. A NULL cell means
`freeze_estimate_at = null` for those projects, which means alerts 2 and 3 do not fire for them. Publish the sample
size beside every median so a reader can see the confidence.

**Live test.** None. It is a contract file.
**Gate.** Deterministic rebuild byte-identical; every cell either has ≥ 30 samples or is NULL; the output is
recomputable from `projects_sha256 = 24484ca8…5ad52` alone.
**Rollback.** Delete the generation.

---

## N5 — Source cards (unblocks everything downstream)

**Why.** `spiders/docs/os/EXTERNAL_SOURCE_RULES.md` requires a source card before a source is used. The register
adapter cannot legitimately start without PlanIt and planning.data.gov.uk cards, and **the shipped product already
calls two geocoders with no card at all**.

**Files touched (spiders):**

```
docs/sources/postcodes_io.md            COMPLIANCE DEBT on something already live
docs/sources/nominatim.md               same; record the rate policy and attribution requirement
docs/sources/repd.md                    complete it — licence is currently "study required" for the SPINE
docs/sources/planit.md                  unblocks N6
docs/sources/planning_data_gov_uk.md    unblocks N6
docs/sources/thegazette.md              unblocks the distress path
docs/sources/lowcarboncontracts.md      unblocks CfD evidence
docs/sources/companies_house_bulk.md    OGL v3 + the accuracy caveat already in the plan
docs/sources/companies_house_rest.md    unblocks N7 Route B
```

Move each from `draft` to `studied` and then `approved-for-derived-scan` explicitly.

**Live test.** None.
**Gate.** No card left at `Last checked: unknown` for any source the product actually calls.
**Rollback.** n/a — documentation only.

---

## N6 — Register adapter (the PROCUREMENT signal)

**Why.** It is the only window component whose engine already exists and passes a gate:
`pipelinenews/archive/.../attributionv1/modules/register-ingest.mjs` with `check_batch5` and `check_batch6`.
Design: `window-intelligence.md` §10.

**Reuse unchanged:** `register-ingest.mjs`, `attribution-ledger.mjs`, `register-ingest.v1.json`,
`attribution-role.v1.schema.json`, both fixture gates.

**Add:**

```
pipelinenews/discovery/javascript/<stamp>-register-fetch.mjs      bounded fetcher (draft skeleton in §10.4)
pipelinenews/contracts/<stamp>-register-fetch.json                limits + selection + source law
pipelinenews/discovery/tests/<stamp>-check-register-live.mjs      the gate in §10.5
```

Selection: `lifecycle == LIVE_PRE_CONSTRUCTION`, `capacity_mw >= 5`, requires both `planning_authority` and
`planning_application_reference`. Limits: ≤ 200 requests/run, concurrency 3, 5 s timeout, ≤ 1 MB response,
0 redirects, 0 raw HTML retained.

**Watch out:** `planning_application_reference` is **frequently empty** on the spine (Berwick Bank has `""`).
Abstain on an empty reference; never guess.

**Live test.** None on the map yet — this lands data only.
**Gate.** §10.5, verbatim: both fixture gates still pass byte-identically; zero roles carry
`OFFICIAL_STATUTORY_NOTICE`; zero person-keyed fields; at least one abstention on a deliberately reference-less
project; two conflicting official roles both retained; deterministic rebuild byte-identical.
**Rollback.** Discard the generation.

---

## N7 — Project-vehicle projection (the FUNDING signal)

**Why.** An SPV owning a consented park has no trade, so its filing history *is* the project's biography. Full
design: `companies-engine.md` §6.

**Do Route A first** (`companies-engine.md` §6.7): snapshot diff of the Basic Company Data file for **bound vehicles
only**. No API key, no new host, no new privacy question — and it delivers the entire **distress** path, which is
the highest-precedence branch of the state machine.

**Files touched (companies), following the `202608281337` source-boundary pattern exactly:**

```
contracts/<stamp>-project-vehicle-events.json
build/python/<stamp>-build-project-vehicle-events.py
tests/test_<stamp>_project_vehicle_events.py            hostile fixture, no network
.github/workflows/<stamp>-project-vehicle-candidate.yml
data/candidates/<stamp>-vehicle/                        candidate branch only
```

**The binding rule is the hard part** (§6.3). 475,596 `PROJECT_NAME_SPV_CANDIDATE` edges exist and all are correctly
`ABSTAIN`. The five-clause rule promotes a small subset to `PRIMARY_MATCH`. **The resulting count is unknown until
it is run** — report it as an output, never assume it.

**Gate (§11.3 + §6.6).** Zero person-keyed columns; twelve columns exactly; **`unbound_vehicle_rows == 0`** — the
load-bearing gate that stops this becoming general company surveillance; every event on the official register
domain; `financial_close_inferred_from_charge_alone` still `false`; deterministic rebuild.

**Do not touch** the £10m balance-sheet view, its selection rule, or the three-column relationship tables.
Route B (REST reads for charges and corporate PSC) is a **later generation with its own contract**, never an edit to
`202608281337`.

**Live test.** None on the map.
**Rollback.** Discard the candidate branch. `main`, `data/current/` and Pages were never touched.

---

## N8 — State machine, ranker, datasets

**Why.** Turns N6 + N7 into one ordered list. Design: `window-intelligence.md` §9 and §12.

**Files touched (pipelinenews):**

```
contracts/<stamp>-project-window-lifecycle-v1.json     the eight states + the legacy mapping
<stamp>/modules/window-state-machine.mjs               pure, no IO, no clock
<stamp>/modules/corporate-events.mjs
<stamp>/modules/window-ranker.mjs
releases/data/window/<stamp>/project-window-state/...parquet
releases/data/window/<stamp>/window-evidence/...parquet
releases/data/window/<stamp>/window-alerts/...parquet
tests/<stamp>-check-window-state.mjs
```

**Invariants the gate must assert (§12.1):** the resolver is **pure**; `DISTRESSED` returns before any other branch
can run; no state without either REPD-frozen fields or a `PRIMARY_MATCH` proof; `FUNDING_WINDOW` impossible without
`planning_permission_granted`; `ABSTAIN` projects keep their legacy `lifecycle` and are **not ranked at all**; state
regression other than to `DISTRESSED` fails the build.

**Alerts.** Only `WINDOW_ENTRY` is enabled now. `THIRTY_DAYS_TO_FREEZE` and `FREEZE_OVERDUE` stay disabled until
`N4`'s calibration is published, and the alerts dataset gets **no browser projection until it has run silently for
at least two generations and been eyeballed.** *"Stay silent until both are on the record"* applies to us first.

**Physical pattern:** copy the sector-intelligence contract exactly — ZSTD, DuckDB 1.3.2, declared keys, rows equal
distinct keys, zero null keys, `IMMUTABLE_FULL_GENERATION_WRITE_FROM_EMPTY_TARGET`,
`WRITE_STAGE → DUCKDB_AUDIT → PUBLISH → DUCKDB_LANDED_READBACK`.

**Live test.** None yet.
**Gate.** As above, plus two silent generations before N9.
**Rollback.** Discard the generation. Nothing published.

---

## N9 — Install the `window-intelligence` cartridge ★ the centrepiece

**Why.** This is where the product becomes visible: which projects are in the funding window **now**, ranked, with
the evidence. Spec: `DRAFT-CARTRIDGES/window-intelligence.spec.md`.

**Depends on:** N2 (slot discipline proven), N8 (data exists and has run silently twice).

**Files touched (gridatlas):**

```
tools/v9_5/<stamp>-build-window-cartridge.py
atlas/cartridges/<stamp>-window-intelligence.js       takes the LAST free slot (B10)
ui/cartridges/<stamp>-window-intelligence.mjs
atlas/current.json                                    cartridge_order gains window-intelligence
atlas/manifests/<stamp>-composition.json
state/<stamp>-window-intelligence-request.json
STATE.md
```

**The obligation that comes with the slot.** It replaces
`202608292126-pre-snapped-config-adapter.js`, so it **must** reproduce `snap: false` for `400, 275, 220, 132, 66`
and assert the closure. If it does not, the browser re-snaps 14,565 line features against 5,800 substations on the
main thread and the 15 s budget is gone.

**iPad detail that decides whether the demo works:** insert the group **first**, not last. `.scada-wrapper` is capped
at `38vh` (`28vh` under `max-height: 600px`) and the key grid is two-column above 480 px, so an appended twelfth
group is below the fold on a 768 × 1024 iPad.

**Live test on the real product:**

| # | test | expected |
|---|---|---|
| 1 | desktop, open the map | **"Funding window" is the first legend group** |
| 2 | console: `__GRIDATLAS_WINDOW__.pre_snap_applied` | `true`, ids sorted `['132','220','275','400','66']` |
| 3 | console: `__GRIDATLAS_WINDOW__.manifest_verified` | `true`, `failures.length === 0` |
| 4 | tick "Funding window" | label becomes `[n \| x GW]` within **15 s**, dots appear |
| 5 | click a dot | popup contains `Estimated design freeze`, `screening only`, `No ownership is asserted.` |
| 6 | tick "Major A-Roads (Trunk)" in the same session | still hydrates — **both fetch patches coexist** |
| 7 | `?repd_ref=13599` | still resolves (N2 unaffected) |
| 8 | **iPad portrait, 768 × 1024** | "Funding window" visible without scrolling, in the panel and the fullscreen curtain |
| 9 | **phone, mobile data** | map loads; window layer opens; heap stays sane |
| 10 | serve a corrupted manifest (negative test) | zero window layers, 400 kV still renders, deep link still resolves |

**Gate.** All ten, local and public. Plus the two behaviour risks named in the spec §6, **proved not assumed**:
`initVentusMap` returning a promise is harmless against this shell, and the `pipelinenews`-origin artefacts are
CORS-readable from the `gridatlas` origin. If CORS fails, mirror the five artefacts into `gridatlas/data/window/`
and pin them there.

**Rollback.** Revert `atlas/current.json`. The previous composition is on disk and the shell never changed.

---

## N10 — `repd-official-v9`

**Why.** All 16 REPD map layers still draw the **V8 oracle** (`/dist/repd_master.json`, 10,784 features) while the
search lane already uses the official Q2 2026 extract. A customer sees the inconsistency the moment they search a
project and then look at the dots. `data-gridatlas` already marks all 16
`ORACLE_ONLY_REPLACED_BY_OFFICIAL_REPD_V9`.

**The trap.** Sixteen shell layer filters are baked against V8 property names (`tech`, `raw_tech`, `capacity`,
`status`). The projection **must emit V8 property names** or every filter breaks. Add `repd_ref` as a new property —
it is absent from the oracle, which is why you currently cannot deep-link *out* of a clicked dot.

**Live test.** Toggle all 16 REPD layers; each reports `[count | MW]`; Beacon Fen appears where search says it is;
`Solar PV (Operational Only)` count matches a DuckDB count over the Parquet.
**Gate.** Fidelity PASS against the official extract; every layer under 15 s and 400 MB.
**Rollback.** Revert the composition generation.

---

## N11 — `highways-pmtiles`

**Why.** Three layers cannot be served within budget by any GeoJSON or DuckDB route.

| layer | rows | Parquet | on-demand @20Mbit | static GeoJSON @20Mbit |
|---|---:|---:|---:|---:|
| uk_primary_roads | 163,790 | 29.3 MB | **26.0 s** | **20.8 s** |
| uk_trunk_roads | 130,228 | 23.1 MB | **23.5 s** | **16.4 s** |
| uk_mainline_railways | 89,933 | 16.1 MB | **20.7 s** | 11.5 s (heap-hostile) |
| uk_motorways | 17,713 | 3.2 MB | **15.6 s** | 2.3 s |

**Slot.** Inside the existing `streaming-parquet-bridge` slot as a superseding generation — it already owns
`window.fetch` and is the natural place to route a source to a `pmtiles://` protocol handler.

**New third-party dependency.** The `pmtiles` library must be version-pinned exactly as
`@duckdb/duckdb-wasm@1.29.0` is. See `questions.md` Q7.

**Zoom floors (mandatory):** motorways 5, mainline rail 6, trunk 7, primary 9.

**Live test.** At national zoom, primary roads are **not** requested. At zoom 10 over a city, the viewport transfer
is ≤ 500 KB. Feature count > 0 at each floor. Heap stays under budget on the phone cell.
**Gate.** PMTiles fidelity per `DATA-DELIVERY-PLAN.md` §5.2 — count plus geometry-within-a-**declared** tolerance,
because tile simplification makes byte-identical hashes impossible.
**Rollback.** Revert the bridge cartridge generation.

---

## N12 — `companies-search`, `grid-connection-status`, `distress-overlay`

Three smaller cartridges, all inside slots already taken, in this order.

**C5 `companies-search`** — `search-parquet`, 1.41 MB, shares the existing DuckDB runtime so the marginal cost is
only the file. **Presentation law is non-negotiable:** header reads *"Company-REPD candidate (name evidence;
ownership unconfirmed)"*; default view is a **count** and evidence-type breakdown, never a list of company names;
absence displays as *"this bounded generator emitted no assertion"*.

**C6 `grid-connection-status`** — five extra properties on the window payload, computed at **build time** in DuckDB,
~460 KB raw added. The browser never loads topology to say "2.1 km from a 132 kV circuit". Always labelled
screening-grade; never a route, a cost or a likelihood.

**C7 `distress-overlay`** — the highest-precedence state on its own layer, always top of the paint order, because
"stop selling" is an alert in its own right.

**Live test.** Company search returns candidates with the caveat visible; a funding-window popup shows the grid
line; a distressed project shows its terminal filing and offers the same developer's other projects.
**Gate.** No company presented as an owner; no score anywhere; no individual named.

---

## N13 — `deep-link-out` (close the loop)

**Blocked on** pipelinenews gaining an inbound `repd_ref` receiver, which it does not have today — the deep link is
currently one-way. Build the symmetrical receiver first: read `repd_ref`, exact-match against the 7,680 spine,
scroll and highlight the row, set `document.body.dataset.pipelinenewsRepdRef`, fail closed.

Until that exists, the popup buttons must be **absent**, not broken.

**Live test.** Map dot → "Open project" → correct pipelinenews row → link back → same project on the map. Round
trip, on desktop and on iPad.

---

## N14 — Wire cvaa to the dependency dashboard ★ highest-value future work

**Why.** This is the point of the whole governance layer. An existing dashboard already maps every workflow and
every app-to-data dependency in the federation. cvaa should **read that intended topology and prove reality still
matches it** — that no extraction from the monolith lost fidelity, and no seam broke, **before a source in
`globalgrid2050` is retired.**

That is the transplant-parity discipline `data-gridatlas` already applies to a single layer
(`tools/202608301930-fidelity.py`: origin GeoJSON vs Parquet partition, feature-by-feature hashes, dropped-property
policy surface, delivery budget separated from fidelity verdict) — applied at **federation scale**.

**Prerequisite.** Locate the dashboard. `questions.md` **Q0**.

**Shape, once located:**

```
1. the dashboard exports a machine-readable topology:
     app -> data repo -> dataset -> producing workflow -> consuming surface
2. a cvaa antibody (or a precomputed ctx extension) reads it and asserts, per edge:
     - the producer still publishes the named dataset at the named path
     - the consumer still points at the producer's CURRENT route, not a stale one   <- the N1 disease
     - the extraction's fidelity report is PASS and not older than N generations
     - a paused workflow is marked paused ON PURPOSE, with the app that depends on it named
3. retiring a source in globalgrid2050 requires: every consuming edge re-pointed,
   every fidelity report PASS, and the dashboard updated in the same change
```

**The vaccine that carries it** is `consumer-pointer-current` (`cvaa-integration-plan.md` §5 V1) — elevated to the
most important vaccine in the registry, because a federation mid-split fails at its seams, not at its centre.
It needs a small `buildContext` extension in `inoculate.mjs` (a precomputed grep of committed files for
`github.io/<repo>/<12-digit>-...` patterns), because antibodies get a data-only snapshot and may not read arbitrary
files or reach the network. That is the correct place for the IO.

**On `globalgrid2050` itself:** adopt cvaa **warning-only** with a dated baseline, exactly as drafted in
`cvaa-integration-plan.md` §3.6 option 2. The 240 workflows are intentionally paused and their debt is
transitional — a number that is visible and shrinking beats a number nobody has. **Do not adopt it in error mode
there**, and do not let a red build there block the split.

---

## Dependency graph

```
N0 ledger unblock ─┬─> N2 exact-ref-index ─┬─> N9 window cartridge ──> N12 ──> N13
                   │                       │
                   ├─> N3 cvaa gridatlas ──┴──────────────────> N14 cvaa <-> dashboard
                   │
                   ├─> N10 repd-official-v9
                   └─> N11 highways-pmtiles

N1 deep-link seam  ──────────────────────> (independent, do FIRST)

N4 freeze calibration ─┐
N5 source cards ──> N6 register adapter ─┤
                   N7 vehicle projection ─┴─> N8 state machine + ranker ──> N9
```

**N1 is independent of everything and is the live 404. It goes first.**
**N4 has no dependencies at all and can be done in parallel, tonight.**

---

## Promotion gates — the standing rules

| gate | rule |
|---|---|
| **G1 Composition** | `verify-compose.mjs` PASS; `full_application_copies_created == 0`; `immutable_shell_modified == false` |
| **G2 Ledger** | `loop.mjs lint` PASS before and after; `STATE.md` byte-matches `state --stdout` |
| **G3 File boundary** | only the declared file set is staged — copy the `git diff --cached --name-only \| grep -Evc "$allowed"` assertion from `verify-live.yml` |
| **G4 Governance** | cvaa's seven selected vaccines immune, `shallow == false` |
| **G5 Local browser** | every proof script passes against `127.0.0.1:4173` on the exact committed tree |
| **G6 Public browser** | the same scripts pass against `https://ventusltd.github.io/gridatlas/atlas/` after Pages serves the exact generation |
| **G7 Budget** | every toggled layer under **15 s** and **400 MB**; features ≥ 1 |
| **G8 Device** | the golden deep link resolves on **375 × 667** and **768 × 1024**, not only 1280 × 900 |
| **G9 Fidelity** | for any new or changed data layer, the `data-gridatlas` fidelity job is PASS; a delivery-budget warning is a *warning*, never traded against fidelity |
| **G10 Seam** | for any change touching a cross-repo contract, both golden sentinels (`13599`, `17494`) resolve end to end from the producing surface, in a real browser |

**Any red gate leaves the previous pointers unchanged.** Recovery is always the last-known-green timestamped release.
That is already the law in `docs/milestones/202608300305-atlas-v9-federated-deep-links.md`; this plan adds nothing to
it, it just obeys it.

---

## What to do first, in order, on the day

1. **N1** — repoint the two consumers at `/gridatlas/atlas/`, prove both sentinels in a browser, move the pointer.
   *The sales link is a 404 today; nothing else matters more.*
2. **N0** — unblock the ledger so the campaign can be recorded.
3. **N2** — ship `exact-ref-index`; the link now arrives on any device.
4. **N3** — adopt cvaa on gridatlas; measure the baselines, do not guess them.
5. **N4** and **N5** in parallel — calibration and source cards; neither needs anything.
6. Then N6 → N7 → N8 → N9, the window layer, in that order.
