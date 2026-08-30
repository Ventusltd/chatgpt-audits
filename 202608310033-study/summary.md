# summary

Written last. Headline findings from an overnight read-only survey of all twelve repositories, and the single
recommended first move.

Nothing outside `gridatlas/_build-plan/` was created, edited or deleted. No git state changed anywhere.

---

## The frame

`globalgrid2050` is the **origin hub**, being deliberately big-banged out into specialised repos and apps — each
with its own repo and its own data. The Parquet + DuckDB layer exists precisely to carve the monolith into
queryable specialised pieces: electricity price and intelligence, the GIS/SLD financial sandbox, gridatlas, the
solar / electrical / cable-topology engineering apps, pipelinenews, and the data repos beneath them. Its 240
workflows are **intentionally paused, not abandoned** — live apps consume what they produce, and the runs are held
so nothing is lost during the split. An existing dashboard already records which app feeds from which data; that
dashboard is the topology source of truth.

So the debt in the hub is **transitional**: it shrinks as pieces move out. The risk in a federation mid-split is not
decay at the centre. **It is broken seams at the edges.** That is the lens for everything below.

---

## Headline findings

### 1. The live sales link is a 404. Today.

`pipelinenews/ui/atlas-v9-deep-links.js` and `companies/state/atlas-v9-link-contract.json` both emit

```
https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=…
```

GridAtlas scope 1 (`202608301321`) moved every release under `atlas/releases/`, and `tools/scope/loop.mjs` now
*asserts* zero root release directories. The path no longer exists. The last green browser proof of a working deep
link (`releases/current-v3.json`, Pages run `33259747002`) was against release `202608291430-atlas-v9`, **before**
the move. Nothing has re-proved the link since.

Every deep link the sales motion depends on currently returns 404. This is the seam disease in its purest form — a
consumer left pointing at a producer that reorganised — and it is exactly what a federation mid-split must be able
to catch automatically.

### 2. The window-intelligence layer at generation 202608300415 is not in the repositories.

That generation in `pipelinenews` is a single 78-line workflow (`ed03159`, *"advance PipelineNews successor gate"*).
Exhaustive search of all twelve repositories and the full git history of the four governance repos found no
eight-state lifecycle, no evidence-order state machine, no ranker, no alerts, no PSC or charge handling. The spine
carries **five** lifecycle values, not eight.

What *does* exist is better than nothing and worse than described — roughly **70 % of the parts**, built to exactly
the right discipline, archived and never wired:

| component | where | state |
|---|---|---|
| register adapter, 5 domain-pinned official sources, 3 outputs incl. abstentions | `attributionv1/modules/register-ingest.mjs` | candidate, fixture-gated, never run live |
| evidence ledger, deterministic ids, person-key guard, contradictions coexist | `attributionv1/modules/attribution-ledger.mjs` | candidate |
| charge → `LENDER`, with `financial_close_inferred_from_charge_alone: false` | same file | candidate |
| contradiction view carrying `project_state_at_claim` | `attributionv1/modules/discrepancy-view.mjs` | candidate |
| credibility tiers (1.0 / 0.7 / 0.6 / 0.3) + corroboration maths | `discoveryv1/modules/credibility.mjs` | candidate |
| Lincoln–Petersen coverage alarm over **search vs register** channels | `discoveryv1/modules/capture-recapture.mjs` | candidate |

The two-channel coverage estimator was written for precisely the two registers in the product thesis. The pieces
were designed for this. They were never connected.

### 3. DuckDB cannot be the drawing plane. This is arithmetic, not opinion.

From the repository's own budget model (`data-gridatlas/tools/202608301930-fidelity.py`):

```
35,700,000 bytes of DuckDB-WASM runtime × 8 ÷ 20,000,000 bit/s = 14.28 s
layer budget                                                   = 15.00 s
```

**The runtime consumes 95 % of the budget before it reads one byte of data.** Five layers are already over:
primary roads 26.0 s, trunk roads 23.5 s, mainline rail 20.7 s, global ports 16.6 s, motorways 15.6 s. Every other
layer passes only because a runner has a fast link.

The same cost sits on the critical sales path: **a deep link cannot resolve without booting DuckDB**. On a 1 GB
phone that is the difference between a working link and a blank map.

### 4. The governance registry is excellent and nobody calls it.

`cvaa` at `d2ebc01f` ships 24 vaccines, a hardened runner (per-antibody child process under the Node permission
model, network namespace, 5 s cap, empty env, banned-API scan, lockfile enforcement, SARIF, ratchet-only baselines
with expiry) and a one-block consumer workflow. **Exactly one `cvaa.json` exists in the workspace — cvaa's own.**
GridAtlas comes closest, running `inoculate.mjs` inline and requiring seven named vaccines to be immune; everything
else is a re-implementation in `tools/scope/loop.mjs`.

Two cvaa baselines expire **2026-09-30** — one month away. If they lapse, every future consumer inherits a registry
that fails its own gate.

### 5. Project vehicles are reachable, and the plumbing already exists.

The `companies` repo pulls balance-sheet fields for entities over £10m and excludes directors and PSCs — correct for
its demand view, and left alone. But it also already computes `probable_project_spv` for every selected company and
emits 475,596 `PROJECT_NAME_SPV_CANDIDATE` edges, all correctly `ABSTAIN`.

And the README's *"the Companies House REST API is not used"* is true of the **data**, not the **capability**: a
complete, reviewed REST client already exists — Basic auth, 1 MB response ceiling, `429` handling that reads
`x-ratelimit-reset` and refuses any reset beyond five minutes, and a retention rule that keeps headers and nothing
else. It is wired as a credential probe and retains no payload.

So a narrow, separate project-vehicle projection is an **extension of reviewed code**, not a new network surface.
And the count-only treatment of director and individual-PSC changes keeps it inside the existing privacy law rather
than beside it: *"three directors were appointed to the vehicle on 12 March"* is a corporate fact about a company,
and it does not require, or retain, any individual's identity.

### 6. One free slot, and one obligation attached to it.

The immutable shell has four replaceable script slots. Two are taken, one is the engine (forbidden), and
**one is free**: `202608292126-pre-snapped-config-adapter.js`. It is also the only moment `window.initVentusMap`
exists and has not yet been called — so it is the only place a new map layer can be installed.

Whatever takes it **must reproduce the pre-snap rewrite** (`snap: false` for 400/275/220/132/66 kV) or the browser
re-snaps 14,565 line features against 5,800 substations on the main thread, and the 15 s budget is gone. Further
capabilities are added by superseding that composite, never by claiming another slot.

---

## The single recommended first move

> **Fix the broken production deep-link seam, then make it arrive on any device: repoint the two consumers at
> `https://ventusltd.github.io/gridatlas/atlas/`, prove both golden sentinels in a real browser, ship the
> `exact-ref-index` cartridge, and then adopt cvaa on gridatlas.**

`NEXT-VERSION.md` **N1 → N2 → N3**.

Why this and nothing else first:

- **It is broken in production now.** Every link the sales motion depends on returns 404. No new capability is worth
  anything while the path to it is dead.
- **The fix is small and reversible.** One constant in `pipelinenews`, one successor contract in `companies`, one
  browser proof against `13599` and `17494`. The rollback block in `releases/current-v3.json` already names the
  last-known-green surface and is untouched.
- **`exact-ref-index` then makes the link *arrive*.** A ~340 KB gzipped static index resolves a deep link in about
  0.15 s with **no runtime at all**, on any device, replacing a 14.9 s best case that fails outright on a
  constrained phone. It is drafted in full, expressed as anchored replacement blocks over the pinned parent so every
  one of the eight literal markers `verify-compose.mjs` asserts survives untouched, and it keeps
  `deep_link.status === 'RESOLVED'` so the existing browser gate passes byte-for-byte.
- **Adopting cvaa on gridatlas closes the loop.** GridAtlas is ~90 % compliant already and is the repository the
  vaccines were written from. Adopting it converts a re-implementation into a real dependency — and the
  `consumer-pointer-current` vaccine drafted in `cvaa-integration-plan.md` §5 V1 makes finding 1 impossible to
  repeat silently. **That is the most important vaccine in the registry for a federation mid-split**, and this
  incident is its provenance.

Two things can start in parallel tonight, because neither depends on anything:

- **N4 — the design-freeze calibration.** Pure arithmetic over a frozen file already in the repository: for every
  project that reached construction, the median `under_construction − planning_permission_granted` per
  `(technology, capacity_band)`, with a cell of fewer than 30 samples recorded as NULL rather than guessed. It
  converts two of the three alerts from impossible to possible, needs no new source and raises no privacy question.
- **N5 — the source cards.** `postcodes.io` and `nominatim` are called by the **shipped product** with no card at
  all, and `repd.md` — the card for the dataset the entire product is built on — still reads
  `Licence: study required`. Two hours of writing closes live compliance debt and unblocks the register adapter.

---

## The shape of the whole plan

**Finish federating the hub. Prove every seam with cvaa. Let the intelligence triangle ride on top of a coherent
platform.**

```
        FINISH FEDERATING              PROVE THE SEAMS              THE INTELLIGENCE
        the hub splits out             cvaa holds the edges         rides on top
        ─────────────────              ────────────────────         ────────────────
        globalgrid2050  ──┐            N3  cvaa on gridatlas        N6  register adapter
          apps + data      │           N1  repoint consumers        N7  vehicle filing watch
          repos radiate    ├──────►    V1  consumer-pointer-        N8  state machine + ranker
          workflows        │               current vaccine          N9  the map layer
          paused on        │           N14 cvaa <-> dependency      N12 grid + contractor
          purpose        ──┘               dashboard                    exposure
```

The order matters and it is not the order of excitement. A window-intelligence layer painted on a map whose deep
links 404, whose seams are unverified and whose drawing plane is 95 % consumed by an analytical runtime is a demo,
not a product. The same layer on a platform where every seam is proved and every extraction has a fidelity report
is a timing engine a supplier will pay for.

The highest-value future work is **N14** — wiring cvaa to the dependency dashboard so it reads the intended topology
and proves reality still matches it: that no extraction from the monolith lost fidelity, and no seam broke, **before
a source in `globalgrid2050` is retired**. That is the transplant-parity discipline `data-gridatlas` already applies
to a single layer (origin GeoJSON vs Parquet partition, feature-by-feature hashes, dropped properties as a policy
surface, delivery budget kept separate from the fidelity verdict), applied at federation scale.

It needs one thing this survey could not find, and it is the first question in `questions.md`: **where the dashboard
lives.**

---

## What is in this folder

| file | what it is |
|---|---|
| `ECOSYSTEM-MAP.md` | Every repo, what it owns, full data flow, the triangle with real join keys, composition mechanics, the shared governance law |
| `window-intelligence.md` | **The core.** Part I: exhaustive account of what exists, including the honest finding on `202608300415`. Part II: the eight states, the transitions and their evidence, the corporate-events adapter, the state machine, the ranker and its weightings, the three alerts, the datasets — in build order |
| `companies-engine.md` | How `companies` fetches and serves; the Parquet/DuckDB schema and query surface; the exact project-vehicle projection kept separate from the balance-sheet view; every join key |
| `intelligence-chain.md` | All eight hops with their contracts; the 404 seam and its two repairs; contract repairs; five mobile/iPad fragilities with severities |
| `CARTRIDGE-CATALOG.md` | 14 cartridges — purpose, source, delivery type, measured budget — with the window layer as the centrepiece, and what is deliberately *not* proposed |
| `DATA-DELIVERY-PLAN.md` | The three delivery planes, the arithmetic that decides them, device tiering, the migration order, and how to extend the existing fidelity harness |
| `DRAFT-CARTRIDGES/` | `window-intelligence` and `exact-ref-index`, each `.js.txt` plus a one-page spec |
| `spiders-feeds.md` | What spiders actually scrapes, live vs stale, the missing source cards, and the six-step pipeline for turning a feed into an artefact |
| `cvaa-integration-plan.md` | The one-block workflow, per-repo predicted findings from measured counts, draft `cvaa.json` baselines, adoption order, and five new vaccines this workspace justifies |
| `NEXT-VERSION.md` | The build plan: N0–N14, dependencies, the exact files each step touches, what to test on the live product after each, and ten standing promotion gates |
| `questions.md` | Fourteen things I could not determine, each with what I assumed and what changes if the answer differs. **Q0 is the dashboard.** |
| `summary.md` | This file |

Everything here is a plan or a draft. Nothing is installed, nothing is wired, and no repository was changed.
