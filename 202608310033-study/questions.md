# questions

Everything I could not determine from the repositories. Ordered by how much it blocks.

Each question states **what I found**, **why it matters**, **what I assumed so the work could continue**, and
**what changes if the answer is different**.

---

## Q0 — Where is the dependency dashboard? ★ blocks the highest-value work

**Point me at the dashboard (repo, app, or data file) that maps every workflow and app-to-data dependency, so a
future session can use it as the topology source of truth and cvaa can verify reality against it.**

**What I found.** Nothing conclusive in this workspace. `data-federation-map-for-globalgrid2050-all-repos` is the
closest candidate — it describes itself as *"the backend metadata database that records which repositories exist,
what role each repo has, and how repositories depend on each other"*, with repo nodes, dependency edges, role
classification, weekly build reports, Parquet snapshots and DuckDB verification, plus a named internal dashboard
(`jean-luc/README.md`, "Jean Luc Federation Dashboard"). `spiders/spider_printer_v1/data/topology.json` is a second
candidate — a screening-grade topological map of the federation with layers for data repos, engines, apps,
libraries, schemas, infrastructure, external authorities and future cartridges. `spiders/spider_maya/v1` holds a
51-node / 92-edge graph of the GlobalGrid2050 AREAS menu, last run 2026-07-04.

**What I could not determine.** Which of these is *the* dashboard you mean; whether it records the **workflow →
dataset → app** edges specifically (as opposed to repo → repo edges); whether the 240 paused workflows in
`globalgrid2050` are enumerated there with the app that depends on each; and whether it is machine-readable.

**Why it matters.** `NEXT-VERSION.md` N14 — wiring cvaa to that dashboard so it proves reality still matches the
intended topology before a source in `globalgrid2050` is retired — is the highest-value future work in the whole
plan, and it cannot start without it. It is also what turns the `consumer-pointer-current` vaccine from a good idea
into an enforceable federation-wide gate.

**What I assumed.** That the dashboard exists, is authoritative, and can export a machine-readable topology. N14 is
written to that assumption and names its prerequisite explicitly.

**What changes if the answer is different.** If the dashboard is presentation-only, N14 gains a first step: export a
machine-readable edge list from it. If the workflow→app edges live somewhere else entirely, N14 points there
instead. Nothing else in the plan moves.

---

## Q1 — Does a window-intelligence layer exist outside this workspace?

**What I found.** Generation `202608300415` in `pipelinenews` is **one file**:
`.github/workflows/202608300415-advance-successor-to-exact-atlas.yml`, commit `ed03159`, 2026-08-30 05:12 +0100,
*"advance PipelineNews successor gate"*, 78 insertions. Its successor `202608300416` (`1fb5ac9`) edits the same
workflow.

I searched every one of the twelve repositories, and the **full git history** of `pipelinenews`, `companies`,
`cvaa` and `spiders`, for: `window-intelligence`, `window_intelligence`, `funding_window`, `evidence-order`,
`evidence_order`, `design freeze`, `freeze overdue`, `days to freeze`, `window entry`, `persons with significant
control`, `psc_`, `ranker`, `corporate-event`, `register-adapter`, `distressed`, `state machine`. The only
filename-level hits in history were `attributionv1/*register*`,
`releases/javascript/202608262115-projects-v8-windowed.js` (table paging) and
`cvaa/vaccines/202608301324-no-expiry-windows.md`. The nine remote branches on `pipelinenews` are all
`atman/*mobile-css*` or `ci/*atlas-pointer*` / `ci/*pages*`.

The project spine carries **five** `lifecycle` values (`LIVE_PRE_CONSTRUCTION`, `UNDER_CONSTRUCTION`,
`OPERATIONAL`, `INACTIVE`, `UNKNOWN`), not eight.

**Why it matters.** The brief describes the layer as already built, tested and disciplined. If it exists on another
machine, in an unpushed branch, or in a clone outside this workspace, then `window-intelligence.md` Part II should
be read as **a specification to diff against it**, not as new work — and several days of effort would be wasted
rebuilding it.

**What I assumed.** That what is in this workspace is what exists. `window-intelligence.md` Part I documents the
real substrate exhaustively (the register adapter, the evidence ledger, the charge→LENDER path, the contradiction
view, the credibility tiers, the capture-recapture coverage alarm — roughly 70 % of the parts, built to the right
discipline, archived and never wired) and Part II drafts only what is genuinely missing.

**What changes if the answer is different.** Part II becomes a review checklist. Part I is correct either way.

---

## Q2 — Route A or Route B for the project-vehicle filing watch?

**What I found.** The `companies` acquisition path is the **bulk product only**:
`BasicCompanyDataAsOneFile-2026-08-01.zip` (493,049,031 B) plus three monthly accounts archives, all HEAD-probed and
pinned by URL, bytes, ETag and Last-Modified. The Basic file carries current name, **previous names**, company
status, incorporation date, SIC 1–4 and address. It does **not** carry charges, PSC, officers or filing history.

But a complete, reviewed **REST client already exists** in
`build/python/202608271507-freeze-companies-house-plan.py`: `api.company-information.service.gov.uk`, HTTP Basic
auth from `COMPANIES_HOUSE_API_KEY`, a 1 MB response ceiling, `429` handling that reads `x-ratelimit-reset` and
refuses any reset beyond a five-minute boundary, and a retention rule that keeps the status and rate-limit headers
and **nothing else**. It is wired as a *credential probe* against `/company/00000006` and retains no payload.

So the README statement *"the Companies House REST API is not used"* is true of the **data**, not the **capability**.

**Why it matters.**
- **Route A (snapshot diff, no key):** renames, SIC changes, status changes and the entire **distress** path
  (administration, liquidation, strike-off) — obtainable today with no new host, no new secret and no new privacy
  question. Distress is the highest-precedence branch of the state machine.
- **Route B (bounded REST reads, needs the key):** charges, corporate PSC changes and director-count changes — the
  earliest and highest-value funding evidence, months before a compound application.

**What I assumed.** Route A first (`companies-engine.md` §6.7, `NEXT-VERSION.md` N7). The §6.4 schema is defined in
terms of *events*, not of where the bytes came from, so Route B drops in later without a schema change.

**What changes if the answer is different.** If a Companies House API key already exists and is authorised for this
use, Route B can run in parallel with Route A and the funding signal arrives roughly one generation sooner. The
request budget cannot be sized until Q4 is answered.

---

## Q3 — Is "parish" in scope, and where would it come from?

**What I found.** The brief names the spine join keys as *"site name, parish, postcode"*. Site name and postcode
exist. **Parish does not exist anywhere.** No REPD derivation in the workspace carries a parish, ward or LSOA field.
The V8 oracle (`globalgrid2050/dist/repd_master.json`) carries `local_planning_authority`, largely empty. The word
"parish" appears in the corpus only inside project names.

The administrative keys that do exist, strongest first:
`repd_postcode` (present on 9,505 of 11,069 rows, valid on 9,060) → `planning_application_reference` →
`planning_authority` (LPA) → `county` → `region` → `country`.

**Why it matters.** A parish-level join is the natural grain for a **local planning register** query, which is the
procurement signal. Without it, the register adapter keys on `planning_authority` + `planning_application_reference`,
which is coarser and fails on the many rows where the reference is empty.

**What I assumed.** Parish is out of scope for now. `NEXT-VERSION.md` N6 keys the register fetcher on LPA plus
planning reference and **abstains** on an empty reference rather than guessing.

**What changes if the answer is different.** Deriving parish means postcode → ONS Postcode Directory → parish, which
is a **new external source** and therefore needs a source card
(`spiders-feeds.md` §2.2, `docs/sources/ons_postcode_directory.md`) before it can be used. It would add roughly one
step to N5 and one to N6.

---

## Q4 — How many project vehicles does the binding rule actually promote?

**What I found.** 482,030 candidate edges over 481,248 distinct `(company_number, repd_ref)` pairs, of which
**475,596 are `PROJECT_NAME_SPV_CANDIDATE`** — a deterministic rule that fires when every distinctive token of a
project name is a subset of the company's tokens. All are correctly `ABSTAIN`, role `UNKNOWN`.

**Why it matters.** A projection watching all 475,596 would be noise, would blow any REST request budget, and would
be a general company-surveillance dataset rather than a project-vehicle biography. The five-clause binding rule in
`companies-engine.md` §6.3 (exact-name or ≥ 2 distinctive tokens plus an SPV term; **unique in both directions**;
energy SIC or SPV term; incorporation date inside a plausible window relative to the planning dates; no competing
candidate) is designed to cut it to a workable number — but **I cannot compute the result without running it**, and
I am not permitted to run anything.

**What I assumed.** Nothing. `NEXT-VERSION.md` N7 requires the count to be **reported as an output**, never assumed,
and the contract gate `unbound_vehicle_rows == 0` means an event row cannot exist for an unbound company regardless
of the number.

**What changes if the answer is different.** If the rule promotes only a handful, clauses 2 and 5 (bidirectional
uniqueness) are too strict and need a corroboration path instead. If it promotes tens of thousands, clause 4 (the
incorporation-date window) needs tightening and Route B's request budget needs rethinking.

---

## Q5 — Is the design-freeze estimate acceptable as a derived number?

**What I found.** Nobody publishes a design-freeze date. It is the thing the entire product sells against and it
does not exist as a fact. The spine does carry every input needed to calibrate an estimate:
`planning_permission_granted`, `under_construction`, `operational`, `technology`, `capacity_mw`, over 7,680
projects.

**Why it matters.** Two of the three alerts — `THIRTY_DAYS_TO_FREEZE` and `FREEZE_OVERDUE` — are impossible without
it. It is also the only number in the whole design that is **ours** rather than a register's, which makes it the
one place the system could mislead a customer.

**What I assumed.** That a labelled estimate is acceptable if and only if it is unmistakably labelled. Every popup
line reads *"Estimated design freeze … (derived by GridAtlas, not published)"*; the confidence is `LOW` unless
funding evidence has landed (`MEDIUM`) or procurement evidence has landed (`HIGH`); a `(technology, capacity_band)`
cell with **fewer than 30 samples is NULL**, not a guess; and **until the calibration is published,
`freeze_estimate_at` is null and both alerts are disabled**.

**What changes if the answer is different.** If a derived date is unacceptable at any confidence, the product keeps
alert 1 (`WINDOW_ENTRY`) — which needs no estimate — and drops alerts 2 and 3. The window layer still works; it just
tells you when a project *entered* the window rather than how long is left.

---

## Q6 — Should pipelinenews gain an inbound `repd_ref` receiver?

**What I found.** The deep link is **one-way**. `pipelinenews` builds links into `gridatlas`
(`buildAtlasV9DeepLink`), and `gridatlas` has a rigorous inbound receiver. `pipelinenews` has **no** inbound
receiver — nothing reads `?repd_ref=` on its side.

**Why it matters.** The chain in the brief is *"map feature → deep link → pipelinenews project → company/window
intelligence → **and back**"*. The "and back" hop does not exist. Without it, cartridge C14 `deep-link-out` has
nowhere to send the user, and the round trip a salesperson needs cannot be demonstrated.

**What I assumed.** That it should be built, symmetrically: read `repd_ref`, exact-match against the 7,680 spine,
scroll and highlight the row, set `document.body.dataset.pipelinenewsRepdRef`, fail closed. `NEXT-VERSION.md` N13
carries it, and states that until it exists the popup buttons must be **absent**, not broken.

**What changes if the answer is different.** If pipelinenews is not the intended destination, name the surface that
is (the GIS/SLD sandbox? an engineering app?) and N13 points there instead. The identifier passed is `repd_ref`
either way.

---

## Q7 — Is a new third-party browser dependency (PMTiles) acceptable?

**What I found.** The composition currently loads exactly two pinned third-party runtime dependencies:
`maplibre-gl@3.6.2` (in the immutable shell) and `@duckdb/duckdb-wasm@1.29.0` (dynamically imported by two
cartridges). Both are version-pinned. The three heavy road layers cannot be served within the 15 s / 400 MB budget
by any GeoJSON or DuckDB route — `uk_primary_roads` is 26.0 s on-demand and 20.8 s as static GeoJSON.

**Why it matters.** PMTiles is the only delivery model that decouples transfer cost from national dataset size
(≈ 50–500 KB per viewport regardless). But it is a new library in the browser, and `no-dangerous-apis` exists
because of exactly this class of risk (CVE-2025-30066, tj-actions/changed-files, 23,000+ repos).

**What I assumed.** That it is acceptable if pinned to an exact version with integrity discipline equal to
`duckdb-wasm@1.29.0`, and if the archive is sha256-pinned in the data manifest with its header verified before the
protocol is registered.

**What changes if the answer is different.** Without PMTiles the three road layers must be **dropped from the map**
rather than shipped over budget. That is a real product decision, not a technical one — the alternative is a layer
that takes 26 s and blows the heap on a phone.

---

## Q8 — Should `data-interconnectors` be built, or left as reference?

**What I found.** The repository has pipelines (`build_interconnectors.py`,
`monthly_update_interconnectors.py`), a reference CSV, a research note and a workflow — and **no landed data at
all**. Ten operational cables are documented with BMRS codes and capacities; six future cables are listed
`DATA NOT WIRED`. Its own law is explicit: a future cable carries no fake values, no BMRS code and no data wiring
until Elexon issues an operational code.

**Why it matters.** Cartridge C11 is 16 features — bytes are irrelevant. The constraint is truth, not size.

**What I assumed.** That the reference table alone is enough for a map layer, with future cables rendered in a
visually distinct, explicitly labelled `DATA NOT WIRED` style. `CARTRIDGE-CATALOG.md` C11 says so.

**What changes if the answer is different.** If flows should be live, the build workflow needs a dispatch and an
audit first, and the sign convention (positive signed MW = **import to GB**) must be carried onto the map.

---

## Q9 — Is the gridatlas scope loop retired on purpose, or should it be perpetual?

**What I found.** A direct contradiction between two governed records.

- `gridatlas/scope-of-works/202608301525-closure.md`: *"All six bounded scopes are complete. The loop schedule is
  retired."* `loop.mjs` `validateWorkflowBudget()` **enforces** it: when the master is `done` it asserts
  `scope-loop-mode: retired` and that no `schedule:` remains.
- `cvaa/vaccines/202608301704-loop-exists.md`: *"The perpetual loop is quietly retired, so the repo has a ledger but
  nothing that advances it"* — and cites gridatlas scope 6 as the symptom.

Each is correct in its own frame and they cannot both be satisfied.

**Why it matters.** Adopting cvaa on gridatlas (`NEXT-VERSION.md` N3) makes this a live finding on the first run.

**What I assumed.** Baseline `loop-exists` at 1 with a short expiry
(`cvaa-integration-plan.md` §3.1) so the disagreement is **visible and dated** rather than silently resolved either
way.

**What changes if the answer is different.** If the loop should be perpetual, restore a bounded schedule with a
genuine exit-0 path (`self-terminating-loops` requires one) and relax the `loop.mjs` closure assertion. If retirement
is correct, `loop-exists` needs a `superseded_by` or a documented per-repo exemption in cvaa.

---

## Q10 — Does `pointer-verifies` apply to non-gridatlas repos?

**What I found.** `inoculate.mjs` `buildContext()` picks the first existing of
`atlas/current.json`, `current.json`, `releases/current.json` as the pointer. In `data-gridatlas` that resolves to
`releases/current.json`. But the `pointer-verifies` antibody then looks for
`atlas/releases/${pointer.release_id}/sha256sums.txt` and `atlas/${cartridge.path}` — **gridatlas-shaped paths that
do not exist in `data-gridatlas`.**

**Why it matters.** Adopting cvaa on `data-gridatlas` (`NEXT-VERSION.md`, adoption order 3) would likely produce a
spurious *"names X which has no sha256sums.txt"* finding on an otherwise clean repository — teaching people to
ignore findings, which is the worst possible outcome for a governance registry.

**What I assumed.** That it should be checked before adoption, and either baselined at 1 or fixed upstream. I did
**not** assume it fails; the antibody may return `[]` if the pointer lacks `release_id`.

**What changes if the answer is different.** If it does fire, the better fix is upstream in cvaa: make
`pointer-verifies` shape-aware (only assert cartridge hashes when `pointer.cartridges` exists) rather than adding a
baseline in every data repo.

---

## Q11 — Which REPD universe is authoritative for the window layer: 11,069 or 7,680?

**What I found.** Two derivations of the same Q2 2026 source, and they are **not the same set**.

| | rows | filter | key artefact |
|---|---:|---|---|
| `gridatlas` search Parquet | **11,069** | no capacity floor | `data/repd_projects_202608290716.parquet` |
| `pipelinenews` governance spine | **7,680** | `capacity_mw >= 1.0`, four technologies | `data/manifests/202608261927-build-manifest-v9-1.json` |

`repd_ref` is the shared key and `11,069 ⊇ 7,680`. The `companies` candidate is pinned to the **7,680** universe
(`unknown_repd_refs: 0` against it). The gridatlas search cartridge asserts `closure.rows === 11069` as a hard
invariant and will fail closed if the Parquet is swapped.

**Why it matters.** A user can search a 0.35 MW rooftop project (present in 11,069, absent from 7,680) and then find
it has no window state — which reads as a bug rather than a scope decision.

**What I assumed.** The window layer is scoped to the **7,680** governance spine, and the cartridge verifies
`spine.project_count === 7680` and `projects_sha256` before installing any layer. The search lane keeps 11,069.

**What changes if the answer is different.** If the window layer should cover all 11,069, the companies candidate
must be regenerated against the wider universe and the "no window state" case needs an explicit UI treatment
(*"below the 1 MW governance threshold"*) rather than silence.

---

## Q12 — What is the intended release cadence for the window generation?

**What I found.** Nothing. Every existing generation in the federation is event-driven — a scope advance, a repair,
a promotion — not scheduled. `no-time-based-gates` forbids a cron pinned to a calendar day, and
`self-terminating-loops` requires an exit-0 path when nothing is pending.

**Why it matters.** *"One month ahead of the trade press"* is a cadence claim. If the window state is recomputed
monthly, the worst-case latency between a charge being registered and the alert firing is a month — which could eat
the entire advantage. Weekly is probably right; daily may exceed a REST request budget under Route B.

**What I assumed.** Weekly, with `WINDOW_ENTRY` deduplicated on `(gg_project_id, alert_type, state)` so a
re-run cannot re-alert. The `publicationReadiness` helper already in `discoveryv1` uses a 24-hour default freshness
window and returns `CANDIDATE_NOT_CURRENT` beyond it — that shape should be reused to make staleness visible.

**What changes if the answer is different.** Cadence sets the Route B request budget and the alert dedupe window.
Nothing structural changes.

---

## Q13 — Two smaller ones, recorded so they are not rediscovered

**Q13a — `technology` in the deep-link contract.** `contracts/atlas-v9-deep-link-contract.v1.json` declares
`identity.required: ["repd_ref", "technology"]`, but the gridatlas receiver **never reads `technology`**. Producers
send it; the receiver ignores it. A hand-built link with only `repd_ref` works, contrary to the contract, and a
producer sending the wrong technology is never told. I assumed the **contract** is wrong and recommended demoting
`technology` to `optional_evidence` (`intelligence-chain.md` §5.2), because `repd_ref` is already unique and
authoritative.

**Q13b — the three quarantined layers.** `industrial_offtakers`
(`QUARANTINED_OUTPUT_NOT_REPRODUCIBLE_FROM_ADJACENT_FETCHER`), `grid_11kv_ukpn`
(`QUARANTINED_SYNTHETIC_UKPN_11KV_IDENTITY`) and the three metro/tram sources (`QUARANTINED_GEOMETRY_MISMATCH`) draw
on the live map today because the release GeoJSON is pinned, but they are **not promotable** and cannot be
regenerated from their stated fetchers. I assumed they stay drawn and unpromoted, and flagged in
`CARTRIDGE-CATALOG.md` C13 that they must not be presented as maintained datasets. If a customer would be misled by
a layer that cannot be rebuilt, they should be removed rather than labelled.
