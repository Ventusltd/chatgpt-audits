# _RANKING — live-pipeline solar and BESS, ranked by funding-window likelihood

**This is the product's first real output.** Every live-pipeline solar and BESS project in the frozen REPD spine,
ranked by how likely it is to be inside the commercial window *now* — the window in which studies, cable and LV
design are bought, before design freeze.

Generated **2026-08-31** from data already held in the repositories. **No live register, Companies House, news or
network fetch of any kind was performed.** Every judgement labelled *inferred* is a derived opinion of this model,
never a published fact.

---

## 1. What was studied

**Live pipeline** is defined strictly as: not operational, not refused, not abandoned, not withdrawn.

| official REPD status | in scope | projects |
|---|---|---:|
| Awaiting Construction | yes | 1,683 |
| Application Submitted | yes | 649 |
| Revised | yes | 306 |
| Under Construction | yes | 238 |
| Planning Permission Expired | yes — retained, verdict DISTRESSED | 172 |
| Appeal Lodged | yes | 5 |
| No Application Required | yes | 1 |
| Operational | **excluded** | 1,400 |
| Application Refused | **excluded** | 297 |
| Abandoned | **excluded** | 165 |
| Application Withdrawn | **excluded** | 152 |
| Appeal Refused | **excluded** | 95 |
| Appeal Withdrawn | **excluded** | 8 |
| Decommissioned | **excluded** | 1 |

**2,859 projects studied**, one markdown file each in this directory, named
`<capacity>-<repd_ref>-<slug>.md` so the directory sorts largest-first.

Source of truth: `pipelinenews/data/projects/202608261927-project-partition-v9-1-01..16.json` — DESNZ REPD Q2 2026,
spine release 9.1, `projects_sha256 24484ca837ac56520ba971fb2c2c1d29620e16a3c71bbaa5764e94c9b515ad52`,
7,680 records at 1 MW and above. Extraction verified: 7,680 rows out, exactly matching the build manifest.

---

## 2. Headline result

| inferred state | projects | capacity | what it means commercially |
|---|---:|---:|---|
| **FUNDING_WINDOW** | **179** | **14,752 MW** | **Consented and early in the lead. The money is being committed now.** |
| **PROCURING** | **275** | **30,328 MW** | Consented and late in the lead. Last call for specification influence. |
| PAST_EXPECTED_START | 1,186 | 50,902 MW | Consented longer ago than comparable projects took to start building. Stalled, or the register has not caught up. Indistinguishable in held data. |
| PRE_CONSENT | 795 | 63,868 MW | No consent. Nothing is being bought. Watch only. |
| DESIGN_FROZEN_OR_LATER | 234 | 12,942 MW | Already building. Cable and LV decided. |
| DISTRESSED | 171 | 2,063 MW | Permission expired. Stop selling. |
| CONSENTED_NO_DATE | 18 | 1,215 MW | Awaiting construction with no granted date. Abstain. |
| UNKNOWN | 1 | 1 MW | Abstain. |

**The addressable near-term market is 454 projects and 45,080 MW** — the FUNDING_WINDOW and PROCURING populations
combined. Of those, **415 projects / 43,126 MW sit within 5 km of a mapped transmission circuit.**

The funding window is overwhelmingly **BESS**, not solar:

| technology | projects in window | capacity in window |
|---|---:|---:|
| bess | 130 | 12,082 MW |
| solar | 49 | 2,671 MW |

That is a direct consequence of the calibration in section 4: BESS takes about 2.4 times longer from consent to
construction than solar, so at any moment far more consented BESS sits inside the early part of the lead.

---

## 3. Method and scoring — declared in full

Six components. Nothing is hidden and nothing is learned; every weight is a stated choice.

| component | maximum | rule |
|---|---:|---|
| **inferred state** | 40 | FUNDING_WINDOW 40 · PROCURING 34 · PAST_EXPECTED_START 14 · CONSENTED_NO_DATE 12 · PRE_CONSENT 6 · UNKNOWN 4 · DESIGN_FROZEN_OR_LATER 2 · DISTRESSED 0 |
| **capacity** | 25 | `25 × log(1+MW) / log(501)` — 1 MW ≈ 4.3, 50 MW ≈ 15.8, 500 MW ≈ 25.0 |
| **grid proximity** | 20 | nearest circuit ≤2 km 15 · ≤5 km 12 · ≤10 km 8 · ≤20 km 4 · else 1; **plus 5** if a substation is within 2 km |
| **record freshness** | 10 | REPD record updated ≤180 d 10 · ≤365 d 7 · ≤730 d 4 · else 1 |
| **name-binding strength** | 5 | HIGH 5 · LOW 2 · NONE 0 (see section 6) |
| **demand adjacency** | 5 | data centre ≤10 km 5 · ≤25 km 3; **plus 2** if an industrial offtaker is within 5 km; capped at 5 |

Theoretical maximum **105**. Ties break on capacity, then REPD reference ascending.

**What the score is not.** It is not a probability, not a credit or bankability score, and not a claim about any
company. It ranks *timing likelihood on held evidence*. A high score means "look here first", nothing more.

---

## 4. The calibration — measured, not assumed

The funding-window judgement rests on one measurement taken from the spine itself, with no external input.

For every solar and BESS project in the 7,680-record spine that carries **both** `planning_permission_granted` and
`under_construction`, the lead was computed as `under_construction − planning_permission_granted`. Leads below zero
or above 3,650 days were discarded.

| technology | capacity band | samples | median lead | p25 | p75 |
|---|---|---:|---:|---:|---:|
| solar | all bands | **1,003** | **234 d** | 99 | 412 |
| solar | 1–5 MW | 288 | 213 d | 98 | 363 |
| solar | 5–20 MW | 584 | 218 d | 97 | 384 |
| solar | 20–50 MW | 121 | 457 d | 173 | 822 |
| solar | 50–100 MW | 9 | *(n<30 — not used)* | | |
| solar | 250+ MW | 1 | *(n<30 — not used)* | | |
| bess | all bands | **143** | **570 d** | 343 | 878 |
| bess | 20–50 MW | 72 | 707 d | 374 | 956 |
| bess | 1–5 MW | 6 | *(n<30 — not used)* | | |
| bess | 5–20 MW | 16 | *(n<30 — not used)* | | |
| bess | 50–100 MW | 24 | *(n<30 — not used)* | | |
| bess | 100–250 MW | 13 | *(n<30 — not used)* | | |
| bess | 250+ MW | 12 | *(n<30 — not used)* | | |

**A cell with fewer than 30 samples is not used.** Those classes fall back to the technology-level median rather
than publish a number derived from a dozen projects. This is the rule set out in `NEXT-VERSION.md` N4 and it is
applied here without exception.

Two findings worth stating on their own:

1. **BESS is a much longer game than solar.** 570 days versus 234. A supplier who calibrates BESS timing on solar
   experience will arrive roughly eleven months too early, twice.
2. **Large solar behaves like BESS, not like small solar.** Solar 20–50 MW takes 457 days against 213–218 days for
   everything below 20 MW. The step change is at 20 MW, not at 50.

### From lead to window

`position = days_since_consent / calibrated_lead`

| position | inferred state | reading |
|---|---|---|
| ≤ 60 % | FUNDING_WINDOW | studies, cable and LV design are bought here |
| 60–100 % | PROCURING | design decisions being made; specification influence closing |
| > 100 % | PAST_EXPECTED_START | past the point a comparable project started building |

**The 60 % boundary is a declared modelling assumption, not a measurement.** Design freeze is not published by
anyone. The lead is measured; where inside it the freeze falls is a choice, and it is stated here so it can be
argued with and changed.

---

## 5. Two data-integrity findings that materially affect this output

Both were discovered while building this ranking. Both are new, and both are more serious than the 404 recorded in
`summary.md`.

### 5.1 `repd_ref` is not unique in the governance spine

The spine holds **7,680 rows over 7,515 unique `repd_ref` values**. **154 references appear more than once**, some
three times. They are not duplicate rows — they are *different projects sharing a reference*:

| repd_ref | project A | project B |
|---|---|---|
| `10058` | Indian Queens National Grid Substation, Domelick Hill — BESS, 50 MW, Cornwall, granted 2024-04-23 | Indian Queens Sub station, Carne Hill — BESS, 50 MW, Cornwall, granted 2023-12-22 |
| `10236` | Elland Storage Project, 49.9 MW, Calderdale, Revised | Lowfields Energy Storage Project, 49.9 MW, Calderdale, Awaiting Construction |

Consequences across the federation:

- `gg_project_id = GG2050-REPD-{repd_ref}` is presented everywhere as **the canonical project key**. It is not
  unique, so it does not identify a project.
- `attribution-ledger.mjs` enforces `gg_project_id === "GG2050-REPD-" + repd_ref`, and `appendAttributions`
  deduplicates on a hash of it. Two different projects would silently share one evidence ledger.
- The GridAtlas deep-link rule is `EXACT_REPD_REF_ONLY`, and the receiver takes the **first** match. `?repd_ref=10058`
  is ambiguous and resolves to whichever of two battery projects the Parquet happens to return first.
- The companies foreign-key gate `unknown_repd_refs: 0` still passes — the references exist — but a company edge to
  `10058` cannot say which project it means.

### 5.2 The two REPD derivations do not share a reference namespace

| | unique refs | non-numeric refs |
|---|---:|---:|
| GridAtlas search Parquet (11,069 rows) | 11,069 | **0** |
| PipelineNews governance spine (7,680 rows) | 7,515 | **2,516** |
| **intersection** | **3,670** | |

- **Only 3,670 references exist in both.** 3,845 spine refs are absent from GridAtlas; 7,399 GridAtlas refs are
  absent from the spine.
- **2,516 spine references are alphanumeric** in the legacy REPD style (`01006W5`, `01007W5`). GridAtlas has none.
  The deep-link contract pattern `^[A-Za-z0-9-]{1,40}$` accepts them, so they validate and then find nothing.
- `attribution-ledger.mjs` requires `repd_ref` to match `^\d+$`. **Those 2,516 projects can never receive an
  attribution claim** — the register adapter and the whole window layer would silently exclude a third of the spine.

**The flagship sentinel is itself affected.** East Pye Solar Farm, 500 MW, appears in the GridAtlas registry
**twice** — as `17494` at 500.0 MW and as `20670` at **0.0 MW**. The governance spine carries East Pye as `20670`
at 500.0 MW. And `discoveryv1/contracts/binding.v1.json` explicitly records
`"snippet_primary_repd_ref": "17494"` with `"forbidden_primary_repd_ref": "20670"` — so the discovery contract
already flagged this collision and chose 17494, while the spine uses 20670. The deep-link contract lists 17494 as a
sentinel; the spine cannot produce it.

Likewise `12780`, the invalid-geometry "NO MAP" sentinel in the pipelinenews cartridge, **does not exist in the
GridAtlas Parquet at all** — a deep link for it returns not-found, not resolved-unmapped.

### 5.3 What this costs this ranking

**339 of the 2,859 studied projects (11.9 %) cannot be opened on the map today** by `?repd_ref=`, independent of the
404 in `summary.md`. Broken down by state:

| inferred state | not addressable |
|---|---:|
| DISTRESSED | 167 |
| PRE_CONSENT | 72 |
| PAST_EXPECTED_START | 55 |
| PROCURING | 19 |
| DESIGN_FROZEN_OR_LATER | 14 |
| **FUNDING_WINDOW** | **10** |
| CONSENTED_NO_DATE | 1 |
| UNKNOWN | 1 |

Ten projects in the funding window — the highest-value rows in this document — have no working map link. Every
affected study file carries a **Deep-link warning** in section 8.

**Recommendation.** Add a reference-reconciliation step to `NEXT-VERSION.md` before N2. Both derivations must agree
what a `repd_ref` identifies, and one of them must be authoritative, before any deep link or window layer is built
on top of it. This is now logged as the first thing to resolve after the 404.

---

## 6. Corporate evidence — what could and could not be used

The 482,030-row Company-REPD candidate table exists in this workspace **only as a ZSTD Parquet blob** on the
`candidate/202608272155-compact` branch of `Ventusltd/companies` (`git ls-tree` confirms the object is present,
1,405,427 bytes). It cannot be decoded without DuckDB, which this session is not permitted to run. **No per-project
company edge is quoted anywhere in these studies.**

What *was* readable, from the same branch, is the aggregate report:

| measure | value |
|---|---:|
| Basic Company Data rows scanned | 5,695,465 |
| companies selected | 294,904 |
| **probable project SPVs** | **39,845** |
| companies with REPD candidates | 259,582 |
| candidate relationship rows | 482,030 |
| companies with assets ≥ £10m | 505 |
| energy-relevant large companies | 385 |
| **companies tagged BTM_DATA_CENTRE** | **316** |

And what *was* computable per project is the deterministic name rule itself, taken from
`companies/build/python/202608262245-compile-companies-house.py` and applied to each project name:

| binding strength | projects | meaning |
|---|---:|---|
| HIGH | 1,929 | two or more distinctive tokens — a high-precision vehicle binding under the rule drafted in `companies-engine.md` §6.3 |
| LOW | 828 | one distinctive token — too weak to bind alone |
| **NONE** | **102** | **no distinctive token of five or more characters — the SPV rule can never generate an edge for these projects at all** |

Those 102 projects are structurally invisible to the funding signal as currently designed. They would need
operator-name or planning-reference binding instead. That is a real gap in the drafted rule, found by applying it.

Operator-name SPV shape (legal suffix plus energy token) is present on only **278 of 2,859** published operator
names — most projects publish a developer, not a vehicle. That is expected and is exactly why the vehicle must be
found in the register rather than in the REPD operator field.

---

## 7. Grid exposure — computed, screening-grade

Straight-line distance from each project point to the nearest feature in the pinned V8 transplant
(`data-gridatlas` generation 202608291015). 5,800 substations with voltage; 47,897 circuit vertices sampled every
third vertex from the 400 kV, 275 kV and 132 kV layers; 240 mapped data centres; 5,878 industrial offtakers.

**A straight line is not a route, a connection, a cost or a likelihood.** This is screening evidence for a
conversation opener, and every study file says so.

Result: **415 of the 454 funding-window and procuring projects (43,126 MW) sit within 5 km of a mapped
transmission circuit.** Grid proximity is therefore *not* a differentiator in this population — nearly all of them
are close. It earns its place in the score by demoting the minority that are not.

---

## 8. Where the money is, geographically

Top counties by capacity in the inferred funding window:

| county | projects | capacity |
|---|---:|---:|
| Nottinghamshire | 4 | 1,375 MW |
| East Riding of Yorkshire | 6 | 1,135 MW |
| Bedfordshire | 3 | 727 MW |
| Highland | 6 | 680 MW |
| Lincolnshire | 9 | 659 MW |
| Kent | 5 | 648 MW |
| Derbyshire | 4 | 624 MW |
| Cambridgeshire | 5 | 552 MW |
| West Glamorgan | 2 | 500 MW |
| East Sussex | 2 | 430 MW |

Top developers by capacity in the inferred funding window:

| operator as published | projects | capacity |
|---|---:|---:|
| Innova Renewables | 2 | 800 MW |
| Orsted UK Limited / PS Renewables | 1 | 740 MW |
| Greenfield Energy Developments Limited | 5 | 680 MW |
| Statera Energy | 2 | 550 MW |
| Island Green Power | 3 | 537 MW |
| Green Switch Capital Limited | 2 | 520 MW |
| Tribus Clean Energy Limited | 1 | 500 MW |
| Balance Power Projects Limited | 2 | 500 MW |
| Penso Power (BW ESS) | 2 | 420 MW |
| Noriker Power Limited | 1 | 349 MW |

For context, the **whole** live solar and BESS pipeline by developer is led by Island Green Power (16 projects,
5,071 MW), Innova Renewables (16, 3,831 MW), NatPower UK (4, 3,500 MW), Statera Energy (10, 2,830 MW) and
Alcemi Storage Development Limited (4, 2,300 MW). The concentration is real: **the top 20 operators hold a
substantial share of live capacity**, which means the funding-window signal is also a small-account-list problem.

---

## 9. How to use this

1. **Start with the FUNDING_WINDOW block below** — 179 projects, 14,752 MW, ranked. These are the ones where, on
   held evidence, the studies and cable/LV money is being committed now.
2. **For each, open its study file** and read section 7 — the gaps. Nothing here is confirmed. The score says
   "look", not "act".
3. **Before acting, run the two checks held data cannot answer:** is there a registered charge over the project
   vehicle, and has a condition-discharge or reserved-matters application been lodged against the planning
   reference. Those two turn an inference into evidence. `INTEL-WORKFLOWS/PLAN.md` designs the supervised fetches.
4. **Treat PAST_EXPECTED_START as the research queue, not the reject pile.** 1,186 projects and 50,902 MW sit
   there, and held data cannot distinguish "stalled" from "building, register lagging". One register check
   separates them, and whichever way it falls the answer is commercially useful.

---

## 10. The full ranking

All 2,859 studied projects, most likely and largest first. Columns:

`#` rank · `score` /105 · `MW` · `tech` · `inferred state` · `project` · `operator as published` ·
`planning authority` · `granted` · `days` since consent · `circuit` nearest km/kV · `ref` REPD reference ·
`map` addressable by `?repd_ref=` today.

| # | score | MW | tech | inferred state | project | operator | planning authority | granted | days | circuit | ref | map |
|---:|---:|---:|---|---|---|---|---|---|---:|---|---|---|
| 1 | 105.0 | 500 | bess | FUNDING_WINDOW | Sundon, Chalton - Battery Energy Storage System | Statera Energy | Central Bedfordshire | 2026-04-16 | 137 | 0.1km/132kV | `18777` | y |
| 2 | 104.1 | 400 | bess | FUNDING_WINDOW | Lletty Scilp Farm, Swansea North - Energy Storage Sy... | Innova Renewables | Swansea | 2026-05-19 | 104 | 0.1km/400kV | `17035` | y |
| 3 | 102.2 | 250 | bess | FUNDING_WINDOW | Layhams Road - Battery Storage Facility | Penso Power (BW ESS) | Bromley | 2026-03-09 | 175 | 1.3km/400kV | `15195` | y |
| 4 | 102.0 | 500 | bess | FUNDING_WINDOW | Torksey Ferry Road, Rampton - Battery Energy Storage | Tribus Clean Energy Limited | Bassetlaw | 2026-06-02 | 90 | 1.0km/400kV | `16723` | y |
| 5 | 101.1 | 400 | bess | FUNDING_WINDOW | Wicken Bridleway, Church Road - Battery Energy Stora... | Green Switch Capital Limited | East Cambridgeshire | 2026-04-08 | 145 | 3.9km/400kV | `16410` | y |
| 6 | 100.8 | 375 | bess | FUNDING_WINDOW | Stallingboroughe, Stallingborough Road - BESS | Island Green Power | North East Lincolnshire | 2026-04-24 | 129 | 1.6km/400kV | `17458` | y |
| 7 | 99.2 | 249 | bess | FUNDING_WINDOW | Power Station Road, Isle Of Grain - Battery Energy S... | Ecostor Grain West Limited | Medway | 2025-12-12 | 262 | 0.2km/400kV | `18348` | y |
| 8 | 99.1 | 240 | bess | FUNDING_WINDOW | Mollington - Battery Energy Storage | Qair Renewables UK Limited | Cheshire West and Chester | 2026-05-07 | 116 | 0.3km/132kV | `18182` | y |
| 9 | 99.0 | 740 | solar | FUNDING_WINDOW | One Earth Solar Farm | Orsted UK Limited / PS Renewables | The Planning Inspectorate - ... | 2026-07-08 | 54 | 0.3km/400kV | `14807` | y |
| 10 | 98.6 | 100 | bess | FUNDING_WINDOW | Peat Dykes Farm, Harrop Lane - Battery Energy Storag... | Brockwell Storage & Solar Limited | Bradford | 2026-06-03 | 89 | 0.1km/132kV | `19412` | y |
| 11 | 98.6 | 100 | bess | FUNDING_WINDOW | Grendon Road, Earls Barton - Battery Energy Storage ... | Greenfield Energy Developments Lim... | North Northamptonshire | 2026-03-16 | 168 | 0.9km/132kV | `19050` | y |
| 12 | 98.3 | 200 | bess | FUNDING_WINDOW | Knocknagael, Essich - Battery Energy Storage System | Field Energy | Scottish Government (S36) | 2026-02-04 | 208 | 0.2km/132kV | `16201` | y |
| 13 | 98.1 | 400 | bess | FUNDING_WINDOW | Moor Hall Farm, Moor Hall Drive - Battery Energy Sto... | Balance Power Projects Limited | Wealden | 2025-09-23 | 342 | 0.9km/132kV | `16245` | y |
| 14 | 98.1 | 400 | bess | FUNDING_WINDOW | Thornton Battery Storage | Greenfield Energy Developments Lim... | East Riding of Yorkshire | 2026-02-27 | 185 | 0.9km/400kV | `19288` | y |
| 15 | 97.7 | 170 | bess | FUNDING_WINDOW | Hilfield Lane, Aldenham - Battery Energy Storage | Penso Power (BW ESS) | Hertsmere | 2026-01-16 | 227 | 0.2km/275kV | `17387` | y |
| 16 | 96.8 | 228 | bess | FUNDING_WINDOW | Woodlands Farm, Calcott Hill - Battery Energy Storag... | Sky UK Development Limited | Canterbury | 2026-05-26 | 97 | 1.6km/400kV | `18025` | y |
| 17 | 96.7 | 62 | bess | FUNDING_WINDOW | Station Road, Crescent Industrial Estate - Battery S... | PJS One Limited | Test Valley | 2026-01-29 | 214 | 0.1km/400kV | `19012` | y |
| 18 | 96.4 | 125 | bess | FUNDING_WINDOW | Exeter Substation, Broadclyst - Battery Energy Stora... | Island Green Power | East Devon | 2026-05-20 | 103 | 0.3km/400kV | `17747` | y |
| 19 | 96.0 | 800 | solar | PROCURING | Springwell, Lincoln - Springwell Solar Farm & Batter... | EDF Energy Renewables | The Planning Inspectorate - ... | 2026-04-08 | 145 | 1.8km/132kV | `13044` | y |
| 20 | 96.0 | 750 | bess | PROCURING | Neilston Greener Grid Park - Phase 2 | Statkraft UK LTD | Scottish Government (S36) | 2025-08-13 | 383 | 0.1km/132kV | `15528` | y |
| 21 | 95.8 | 480 | bess | PROCURING | Fairlawns Farm, Chelmsford Road - Battery Energy Sto... | Gresham House Devco Pipeline | Rochford | 2025-07-17 | 410 | 1.2km/132kV | `16887` | y |
| 22 | 95.8 | 50 | bess | FUNDING_WINDOW | Orrell Street Battery Energy Storage Facility | Enzygo Limited Environmental Consu... | Wigan | 2026-02-26 | 186 | 0.6km/132kV | `7724` | **n** |
| 23 | 95.8 | 50 | bess | FUNDING_WINDOW | Sully Moors Road - Battery Energy Storage Facility | Centrica Plc Head Office | Vale of Glamorgan | 2026-02-13 | 199 | 0.1km/132kV | `19656` | y |
| 24 | 95.8 | 50 | bess | FUNDING_WINDOW | Grendon Lakes, Grendon - Battery Storage Facility | Statera Energy | North Northamptonshire | 2025-07-29 | 398 | 0.2km/132kV | `14321` | y |
| 25 | 95.8 | 50 | solar | FUNDING_WINDOW | Burwell Anchor Lane Farm, Newnham Drove - Solar Pane... | Burwell AL Limited | East Cambridgeshire | 2026-03-20 | 164 | 0.6km/400kV | `17757` | y |
| 26 | 95.8 | 50 | bess | FUNDING_WINDOW | Ebbsfleet Lane - Battery Storage System | Grenergy Renewables UK Limited | Thanet | 2026-01-16 | 227 | 0.5km/132kV | `19402` | y |
| 27 | 95.8 | 50 | solar | FUNDING_WINDOW | Cobham Road, Bookham - Solar Farm | Public Power Solution Limited | Mole Valley | 2026-05-21 | 102 | 1.4km/132kV | `15940` | y |
| 28 | 95.6 | 100 | bess | FUNDING_WINDOW | Moat Lane, Wickersley - Battery Storage Facility | Newton Energi Limited | Rotherham | 2025-11-19 | 285 | 0.1km/275kV | `15746` | y |
| 29 | 95.6 | 100 | bess | FUNDING_WINDOW | Moat Lane, Wickersley - Battery Storage Facility | Harmony Energy Storage | Rotherham | 2025-11-19 | 285 | 0.1km/275kV | `16065` | y |
| 30 | 95.6 | 100 | bess | FUNDING_WINDOW | Rhydypandy Road, Morriston - Battery Energy Storage ... | Statkraft UK | Swansea | 2025-12-18 | 256 | 0.5km/132kV | `18120` | y |
| 31 | 95.6 | 349 | bess | FUNDING_WINDOW | Gibson Farm, Blackhillock - Battery Energy Storage S... | Noriker Power Limited | Scottish Government (S36) | 2025-12-03 | 271 | 0.7km/132kV | `14283` | y |
| 32 | 95.6 | 100 | bess | FUNDING_WINDOW | Darenth Road - Battery Energy Storage System | Net Zero Marine Services Limited | Dartford | 2025-10-06 | 329 | 2.0km/132kV | `18483` | y |
| 33 | 95.6 | 100 | bess | FUNDING_WINDOW | Ebstree Road, Trysull, Seisdon - Battery Energy Stor... | NZED Projectco 3 limited | South Staffordshire | 2025-11-21 | 283 | 0.3km/400kV | `19116` | y |
| 34 | 95.3 | 200 | bess | PROCURING | Spennymoor Greener Grid Park | Statkraft UK Limited | County Durham | 2025-07-14 | 413 | 0.2km/400kV | `13576` | y |
| 35 | 95.3 | 200 | bess | FUNDING_WINDOW | Sunbury Battery Energy Storage System - Battery Ener... | EcoDev Group Limited | Spelthorne | 2026-01-16 | 227 | 2.6km/275kV | `15814` | **n** |
| 36 | 95.3 | 200 | bess | FUNDING_WINDOW | East Road, Marchwood - Battery Energy Storage | BW ESS Development UK Limited | New Forest | 2025-11-13 | 291 | 0.1km/132kV | `19403` | y |
| 37 | 95.2 | 150 | bess | FUNDING_WINDOW | Carncome, Lislunnan Road - Battery Energy Storage | Valor Power Limited | Antrim and Newtownabbey | 2026-04-10 | 143 | 0.9km/275kV | `20558` | y |
| 38 | 95.0 | 300 | bess | FUNDING_WINDOW | Rednal Airfield, West Felton - Battery Energy Storag... | Private Developer | Shropshire | 2026-04-16 | 137 | 0.2km/400kV | `18028` | y |
| 39 | 94.7 | 360 | bess | PROCURING | Harker Moss - Battery Energy Storage System | ESB (Harker) Limited | Cumberland | 2025-07-09 | 418 | 0.0km/275kV | `17649` | y |
| 40 | 94.2 | 320 | bess | PROCURING | Burton Wood Farm, Spring Lane - Battery Energy Stora... | Grenergy Renewables | Gedling | 2025-03-27 | 522 | 2.3km/132kV | `16085` | y |
| 41 | 94.2 | 55 | bess | FUNDING_WINDOW | East Rogerton Cottage, Markethill Road - Battery Sto... | Apatura - GPC 680 Limited | Scottish Government (S36) | 2026-02-04 | 208 | 0.7km/275kV | `13449` | **n** |
| 42 | 94.1 | 70 | bess | FUNDING_WINDOW | High Brockland Farm, Brock Lane - Battery Energy Sto... | Bluefield Renewable Developments L... | Northumberland | 2026-01-07 | 236 | 0.9km/400kV | `18250` | y |
| 43 | 94.0 | 500 | bess | PROCURING | Kilmarnock Battery Energy Storage System | Matrix Renewables | Scottish Government (S36) | 2025-04-07 | 511 | 1.0km/400kV | `15176` | y |
| 44 | 93.1 | 400 | bess | FUNDING_WINDOW | Stenson Lane - Battery Energy Storage System | Innova Renewables | South Derbyshire | 2025-10-27 | 308 | 0.3km/132kV | `16675` | y |
| 45 | 93.1 | 25 | bess | FUNDING_WINDOW | Newton Lane, Ledston - Battery Storage Facility | Harmony LS Limited | Leeds | 2026-05-22 | 101 | 0.2km/132kV | `14523` | **n** |
| 46 | 93.1 | 25 | bess | FUNDING_WINDOW | Heol Aur, Dafen Industrial Estate - Battery Storage ... | Westfa Limited | Carmarthenshire | 2026-02-26 | 186 | 0.5km/132kV | `18991` | y |
| 47 | 93.1 | 25 | solar | FUNDING_WINDOW | Lentons Lane - Solar Panels | Eon UK Plc | Coventry | 2026-01-09 | 234 | 0.3km/132kV | `19794` | y |
| 48 | 93.1 | 240 | bess | PROCURING | Cockenzie Battery Storage System - Site A | Gresham House | Scottish Government (S36) | 2025-07-23 | 404 | 0.2km/400kV | `14539` | y |
| 49 | 93.0 | 1025 | bess | PROCURING | Fairfields Energy Storage System | Novus Renewable Services | South Derbyshire | 2025-03-17 | 532 | 0.4km/400kV | `14018` | y |
| 50 | 93.0 | 1000 | bess | PROCURING | Rover Way, Splott - Energy Park & Data Centre | Latos Cardiff Limited | Cardiff | 2025-04-15 | 503 | 0.4km/275kV | `16190` | y |
| 51 | 93.0 | 600 | bess | PROCURING | Daines Battery Energy Storage System | SSE Daines BESS Limited | Trafford | 2025-05-15 | 473 | 0.3km/400kV | `17495` | y |
| 52 | 93.0 | 500 | bess | PROCURING | Culham Science Centre, Clifton Hampden - Battery Sto... | Statera Energy | South Oxfordshire | 2025-07-22 | 405 | 0.2km/400kV | `12968` | y |
| 53 | 92.8 | 177 | bess | FUNDING_WINDOW | Dunton Lane - Battery Energy Storage System | Central Bedfordshire Council | Central Bedfordshire | 2025-10-24 | 311 | 0.3km/400kV | `17482` | y |
| 54 | 92.8 | 50 | bess | FUNDING_WINDOW | Cooksland Farm, Old Snydale -Battery Energy Storage | Ylem Energy Limited / Root Power | Wakefield | 2025-11-26 | 278 | 0.2km/400kV | `16557` | y |
| 55 | 92.8 | 50 | solar | FUNDING_WINDOW | Mareham Lane, Solar PV Panels | Lighthouse Development Consulting | North Kesteven | 2026-02-16 | 196 | 0.2km/132kV | `15180` | y |
| 56 | 92.8 | 50 | bess | FUNDING_WINDOW | Sudmeadow Road, Hempsted - Battery Energy Storage Sy... | Greenfield Energy Developments Lim... | Gloucester | 2025-11-21 | 283 | 0.5km/132kV | `17343` | y |
| 57 | 92.8 | 50 | solar | FUNDING_WINDOW | Edge Lane, Maiden Law - Solar Farm & Battery Storage | Lightsource BP | County Durham | 2026-04-22 | 131 | 0.3km/400kV | `11619` | y |
| 58 | 92.8 | 50 | bess | FUNDING_WINDOW | Grigorhill Cottage, Grigorhill - Battery Energy Stor... | OPDE UK Limted | Highland | 2026-01-13 | 230 | 1.5km/132kV | `16752` | y |
| 59 | 92.8 | 50 | solar | FUNDING_WINDOW | Twinwood Road Oakley And Clapham, Thurleigh Road - S... | PACE Elevate Energy Limited | Bedford | 2026-02-19 | 193 | 0.4km/132kV | `19369` | y |
| 60 | 92.8 | 50 | solar | FUNDING_WINDOW | Neat Marsh North, Neat Marsh Road - Solar Farm | Neat Marsh Solar Limited | East Riding of Yorkshire | 2026-02-27 | 185 | 0.4km/275kV | `19431` | y |
| 61 | 92.6 | 100 | bess | FUNDING_WINDOW | Tyddyn Forgan, Llanddeiniolen - Energy Storage Syste... | Firstway Energy / Net Zero Twenty ... | Gwynedd | 2026-01-23 | 220 | 0.4km/400kV | `18370` | y |
| 62 | 92.6 | 100 | bess | FUNDING_WINDOW | Buildwas - Battery Energy Storage | Greenfield Energy Developments Lim... | Shropshire | 2026-04-22 | 131 | 0.2km/400kV | `18395` | y |
| 63 | 92.6 | 100 | bess | FUNDING_WINDOW | Hurst Farm, Mansfield Road - Battery Energy Storage ... | Lightsource BP | Bolsover | 2025-12-19 | 255 | 0.6km/132kV | `17844` | y |
| 64 | 92.5 | 98 | bess | FUNDING_WINDOW | Barnett Wood Lane - Battery Storage | Bluestone Energy | Mole Valley | 2025-09-24 | 341 | 1.1km/132kV | `12919` | y |
| 65 | 92.4 | 45 | bess | FUNDING_WINDOW | Edge Lane, Maiden Law - Solar Farm & Battery Storage | Lightsource BP | County Durham | 2026-04-22 | 131 | 0.3km/400kV | `11618` | y |
| 66 | 92.3 | 200 | bess | PROCURING | Rawfield Lane - Battery Energy Storage System | Harmony Energy Limited | North Yorkshire | 2025-08-21 | 375 | 0.8km/275kV | `17502` | y |
| 67 | 92.3 | 200 | bess | PROCURING | Cowley Substation, Blackberry Lane - Battery Storage... | Penso Power (BW ESS) | South Oxfordshire | 2025-07-17 | 410 | 0.6km/132kV | `17503` | y |
| 68 | 92.2 | 20 | bess | FUNDING_WINDOW | Kings Weston Lane - Battery Energy Storage System | Fig Power | Bristol, City of | 2026-03-16 | 168 | 0.7km/400kV | `17691` | y |
| 69 | 92.2 | 20 | solar | FUNDING_WINDOW | Owlers Farm, Wakefield Road - Solar Farm | IBE Flushdyke Limited | Wakefield | 2026-05-14 | 109 | 1.7km/275kV | `19094` | y |
| 70 | 92.2 | 320 | solar | FUNDING_WINDOW | Peartree Hill Solar Farm | JBM Solar / RWE | The Planning Inspectorate - ... | 2026-07-02 | 60 | 1.1km/132kV | `15001` | y |
| 71 | 92.2 | 150 | bess | FUNDING_WINDOW | Battery Storage System Development in Lisburn | Lisburn Energy Limited | Stockton-on-Tees | 2026-01-30 | 213 | 0.5km/275kV | `16478` | y |
| 72 | 92.1 | 400 | bess | PROCURING | Ginns Road, Stocking Pelham - Battery Energy Storage | FRV TH Powertek Limited | East Hertfordshire | 2025-04-29 | 489 | 0.2km/400kV | `16769` | y |
| 73 | 92.0 | 300 | bess | FUNDING_WINDOW | Ryedale Farm, Seaton Common Lane - Battery Energy St... | RPC Elmya Carnation Foxdale Limite... | East Riding of Yorkshire | 2025-12-12 | 262 | 0.3km/400kV | `19251` | y |
| 74 | 91.7 | 37 | solar | FUNDING_WINDOW | Stallingboroughe, Stallingborough Road - Solar PV En... | Island Green Power | North East Lincolnshire | 2026-04-24 | 129 | 1.6km/400kV | `17459` | y |
| 75 | 91.6 | 37 | bess | FUNDING_WINDOW | STOR Field 9 | Capbal | Fife | 2026-06-05 | 87 | 0.5km/132kV | `7018` | y |
| 76 | 91.3 | 120 | bess | FUNDING_WINDOW | Hill Farm, Wacton Road - Battery Energy Storage Syst... | Green Switch Capital Limited | South Norfolk | 2026-03-25 | 159 | 0.3km/400kV | `16537` | y |
| 77 | 91.2 | 320 | bess | PROCURING | Avondale Nurseries, Spa Lane - Battery Energy Storag... | Sandbrook Capital Bes Limited | West Lancashire | 2025-07-23 | 404 | 0.5km/275kV | `14673` | y |
| 78 | 91.2 | 150 | bess | PROCURING | Downiebrae Road, Rutherglen - Battery Energy Storage... | Battery Box Limited | Scottish Government (S36) | 2025-09-03 | 362 | 0.1km/132kV | `16197` | y |
| 79 | 91.1 | 70 | bess | FUNDING_WINDOW | Illey Lane - Battery Energy Storage | Grenergy Renewables UK Limited | Bromsgrove | 2025-10-14 | 321 | 0.6km/132kV | `17338` | y |
| 80 | 91.1 | 25 | bess | FUNDING_WINDOW | Houston Solar PV Farm & Energy Storage Facility | The Old Rectory | Scottish Government (S36) | 2026-03-20 | 164 | 1.7km/400kV | `14293` | y |
| 81 | 91.0 | 600 | bess | PROCURING | Stable Green, Sand Hill Lane - Battery Energy Storag... | Lightrock Power | Wealden | 2025-07-31 | 396 | 0.1km/400kV | `18138` | y |
| 82 | 91.0 | 300 | bess | PROCURING | Appleford - Battery Energy Storage | TBC 001 Limited | Vale of White Horse | 2025-08-08 | 388 | 1.1km/400kV | `17837` | y |
| 83 | 90.8 | 30 | bess | FUNDING_WINDOW | Mcdonnell Drive, Exhall - Battery Energy Storage Sys... | Greenfield Energy Developments Lim... | Nuneaton and Bedworth | 2025-10-10 | 325 | 0.1km/275kV | `19161` | y |
| 84 | 90.8 | 50 | solar | FUNDING_WINDOW | Moat Farm - Solar Farm | Elgin Energy EsCo Limited | Forest of Dean | 2026-05-19 | 104 | 1.2km/400kV | `10624` | y |
| 85 | 90.8 | 50 | bess | FUNDING_WINDOW | Bulls Copse Road, Marchwood Bypass - Battery Energy ... | Sky UK Development Limited | New Forest | 2026-02-20 | 192 | 0.4km/132kV | `19388` | y |
| 86 | 90.8 | 50 | bess | FUNDING_WINDOW | Malice Farm, French Drove - BESS | FRV TH Powertek Limited | Peterborough | 2026-05-13 | 110 | 0.3km/132kV | `19562` | y |
| 87 | 90.8 | 50 | solar | FUNDING_WINDOW | Malice Farm, French Drove - Solar Farm | FRV TH Powertek Limited | Peterborough | 2026-05-13 | 110 | 0.3km/132kV | `19563` | y |
| 88 | 90.8 | 50 | bess | FUNDING_WINDOW | Keepers House, Byrecleugh - Battery Energy Storage | Sunlaws Development Company Limite... | Scottish Borders | 2025-12-08 | 266 | 0.1km/400kV | `16783` | y |
| 89 | 90.5 | 28 | bess | FUNDING_WINDOW | A171, Guisborough Woods - Battery Energy Storage Sys... | Harmony MS Limited | Redcar and Cleveland | 2026-04-20 | 133 | 4.7km/400kV | `17983` | y |
| 90 | 90.5 | 99 | bess | FUNDING_WINDOW | Remembrance Way - Battery Energy Storage System | Root Power South Limited | North West Leicestershire | 2026-01-08 | 235 | 0.4km/400kV | `17573` | y |
| 91 | 90.1 | 240 | bess | PROCURING | Springfield Farm, Weeland Road - Battery Energy Stor... | Newton Energi Limited | North Yorkshire | 2025-05-07 | 481 | 1.4km/400kV | `16644` | y |
| 92 | 90.1 | 240 | bess | PROCURING | Eastlands Farm, Catsfield - Catsfield Battery Energy... | Masdar Arlington Energy | Rother | 2025-08-04 | 392 | 1.1km/400kV | `17826` | y |
| 93 | 90.1 | 240 | bess | PROCURING | Staithes Road, Saltend -Battery Energy Storage Syste... | SFEL One Limited | East Riding of Yorkshire | 2025-07-21 | 406 | 0.7km/132kV | `17842` | y |
| 94 | 90.0 | 650 | bess | PROCURING | Braxbess Battery Storage | Braxbess Limited | Scottish Government (S36) | 2025-07-23 | 404 | 0.3km/132kV | `15169` | y |
| 95 | 90.0 | 560 | bess | PROCURING | Whitehall Battery Storage | Apatura | Scottish Government (S36) | 2025-07-22 | 405 | 0.2km/275kV | `15797` | y |
| 96 | 90.0 | 500 | bess | PROCURING | Holmfield Battery Storage | Masdar Arlington Energy | Calderdale | 2025-05-29 | 459 | 0.2km/132kV | `17964` | y |
| 97 | 89.9 | 180 | bess | FUNDING_WINDOW | Salamander Offshore Wind Farm - Battery Storage and ... | Orsted / Simply Blue Group | Scottish Government (S36) | 2025-10-28 | 307 | 1.7km/132kV | `11035` | y |
| 98 | 89.8 | 50 | bess | FUNDING_WINDOW | Stirling Battery and Solar Energy Park | EcoDev Group Limited | Scottish Government (S36) | 2026-02-11 | 201 | 1.5km/132kV | `14994` | y |
| 99 | 89.8 | 50 | solar | FUNDING_WINDOW | Potterne Park Farm, Potterne - Solar Farm | Potterne Solar Project Limited | Wiltshire | 2026-04-20 | 133 | 0.3km/132kV | `15715` | y |
| 100 | 89.8 | 50 | bess | FUNDING_WINDOW | Buslingthorpe Green - Battery Energy Storage | Living Power Plc | Leeds | 2025-07-09 | 418 | 0.2km/132kV | `16437` | y |
| 101 | 89.8 | 50 | bess | FUNDING_WINDOW | Stoneworthy - Battery Energy Storage System | RES Limited | Torridge | 2025-07-03 | 424 | 0.7km/132kV | `16561` | y |
| 102 | 89.8 | 50 | bess | FUNDING_WINDOW | Weddington Road - Battery Energy Storage | Fig Power | Nuneaton and Bedworth | 2026-02-02 | 210 | 2.8km/132kV | `17365` | y |
| 103 | 89.7 | 48 | bess | FUNDING_WINDOW | Meadowville, Hull Road - Battery Energy Storage Syst... | UK Battery Storage Limited | York | 2025-10-23 | 312 | 0.2km/400kV | `18831` | **n** |
| 104 | 89.6 | 10 | solar | FUNDING_WINDOW | Quarry, Ditchford Lane - Solar Farm | Novus Renewable Services | North Northamptonshire | 2026-06-03 | 89 | 0.5km/132kV | `15138` | y |
| 105 | 89.6 | 102 | bess | PROCURING | Cockenzie Battery Storage System - Site B | Gresham House | Scottish Government (S36) | 2025-07-23 | 404 | 0.2km/400kV | `17556` | y |
| 106 | 89.6 | 456 | bess | PROCURING | Gretna Green Battery Storage | Gresham House Devco Pipeline | Scottish Government (S36) | 2025-03-17 | 532 | 0.3km/400kV | `15427` | y |
| 107 | 89.6 | 37 | solar | FUNDING_WINDOW | Oaks Farm - Solar Farm | Novus Renewable Services Limited | Buckinghamshire | 2026-05-29 | 94 | 1.0km/132kV | `13331` | y |
| 108 | 89.6 | 79 | bess | FUNDING_WINDOW | Battery Energy Storage System Development in Ballyme... | Green Frog Power | South Antrim | 2025-10-20 | 315 | 0.3km/275kV | `16744` | y |
| 109 | 89.6 | 100 | bess | PROCURING | Gammaton Barton Farm, Alverdiscott - Battery Energy ... | Torridge District Council | Torridge | 2025-07-17 | 410 | 1.2km/132kV | `18361` | y |
| 110 | 89.6 | 100 | bess | PROCURING | Crondall Road, Crondall - Fleet Bramley Battery Ener... | Cragside Energy Limited | Hart | 2025-08-22 | 374 | 0.2km/132kV | `16472` | y |
| 111 | 89.5 | 98 | bess | FUNDING_WINDOW | Hams Hall, Hams Lane - Battery Energy Storage System | Eon UK Plc | North Warwickshire | 2025-10-17 | 318 | 0.3km/132kV | `19010` | y |
| 112 | 89.4 | 75 | solar | PROCURING | Houston Solar PV Farm & Energy Storage Facility | The Old Rectory | Scottish Government (S36) | 2026-03-20 | 164 | 1.7km/400kV | `14294` | y |
| 113 | 89.3 | 200 | bess | PROCURING | Pond Industrial Park, Whitburn Road - Pond Battery S... | Banks Renewables | Scottish Government (S36) | 2025-03-24 | 525 | 0.3km/132kV | `13404` | y |
| 114 | 89.3 | 200 | bess | PROCURING | Walsoken, Burrettgate Road - Battery Storage Facilit... | Walsoken Limited | King's Lynn and West Norfolk | 2025-07-25 | 402 | 0.5km/132kV | `14290` | **n** |
| 115 | 89.3 | 200 | bess | PROCURING | Salters Battery Energy Storage System | Buccleuch Group | Scottish Government (S36) | 2025-05-12 | 476 | 1.3km/132kV | `15173` | y |
| 116 | 89.3 | 200 | bess | PROCURING | North Lanrigg Energy Storage | North Lanrigg Battery Storage Limi... | Scottish Government (S36) | 2025-07-24 | 403 | 1.4km/275kV | `17014` | y |
| 117 | 89.3 | 200 | bess | PROCURING | Rectory Lane - Energy Storage System | Net Zero Eighteen Limited | Cheshire West and Chester | 2025-05-19 | 469 | 0.3km/132kV | `17037` | y |
| 118 | 89.3 | 200 | bess | PROCURING | Tara Melbourne Road, Thornton - Battery Energy Stora... | Rewe 9 Limited | East Riding of Yorkshire | 2025-08-28 | 368 | 0.3km/400kV | `18852` | y |
| 119 | 89.2 | 43 | solar | PROCURING | Wormald Green Solar Farm | Harmony Energy Limited | North Yorkshire | 2025-07-31 | 396 | 1.1km/132kV | `8541` | y |
| 120 | 89.2 | 43 | bess | FUNDING_WINDOW | Killin Switching Station, Boreland - Boreland Energy... | Boreland Energy Limited | Stirling | 2025-09-08 | 357 | 0.1km/132kV | `12598` | y |
| 121 | 89.1 | 400 | bess | PROCURING | Glenside Farm - Battery Storage | Apatura | Scottish Government (S36) | 2025-02-25 | 552 | 0.4km/275kV | `14988` | y |
| 122 | 89.1 | 400 | bess | PROCURING | Great Oak Energy Hub | Clearstone Energy Limited | Horsham | 2025-03-28 | 521 | 1.1km/400kV | `17245` | y |
| 123 | 89.1 | 400 | bess | PROCURING | Bullen Lane, Bramford - Battery Energy Storage | Clearstone Energy Limited | Mid Suffolk | 2025-03-27 | 522 | 0.3km/400kV | `17754` | y |
| 124 | 88.8 | 50 | solar | FUNDING_WINDOW | Trevarthian Farmhouse - Solar PV Farm & Battery Ener... | Trevarthian Renewables Limited | Cornwall | 2026-06-01 | 91 | 6.3km/132kV | `9092` | y |
| 125 | 88.7 | 38 | bess | FUNDING_WINDOW | Hastings Hill Farm, Foxcover Road - Battery Energy S... | Root Power (North) Limited | Sunderland | 2025-07-24 | 403 | 0.7km/275kV | `17469` | y |
| 126 | 88.5 | 28 | solar | FUNDING_WINDOW | Bonnyton, Kirkton Moor Road - Solar PV Panels | Advance Construction(Scotland) Lim... | East Renfrewshire | 2026-02-11 | 201 | 0.8km/275kV | `18664` | y |
| 127 | 88.4 | 35 | bess | FUNDING_WINDOW | Warren Lane, Bramham - Battery Energy Storage | Harmony Energy Limited | Leeds | 2025-07-15 | 412 | 0.3km/275kV | `14954` | y |
| 128 | 88.4 | 35 | solar | FUNDING_WINDOW | Elstronwick, Burstwick - Daisy Hill Solar Photovolta... | Enviromena Project Management UK L... | East Riding of Yorkshire | 2026-01-30 | 213 | 4.4km/132kV | `16816` | y |
| 129 | 88.0 | 238 | solar | PROCURING | Fenwick Solar Farm & Battery Storage | Boom Developments Limited | The Planning Inspectorate - ... | 2026-02-18 | 194 | 0.0km/275kV | `14099` | y |
| 130 | 88.0 | 1200 | bess | PROCURING | West Leake Lane, Ratcliffe - Battery Storage | Sandbrook Capital BES Limited | Rushcliffe | 2025-02-10 | 567 | 3.0km/132kV | `12464` | y |
| 131 | 88.0 | 550 | bess | PROCURING | Eggborough Battery Energy Storage System | SSE Renewables Ireland Limited | North Yorkshire | 2025-05-30 | 458 | 1.0km/400kV | `17000` | y |
| 132 | 87.9 | 85 | bess | FUNDING_WINDOW | Old Wood Energy Park - Battery Energy Storage | Exagen | Rushcliffe | 2026-06-05 | 87 | 1.4km/132kV | `16013` | y |
| 133 | 87.9 | 66 | bess | PROCURING | Queenslaine Farm, Highworth Road - Battery Energy St... | Elgin Energy | Swindon | 2025-09-12 | 353 | 1.8km/132kV | `18424` | y |
| 134 | 87.8 | 50 | solar | FUNDING_WINDOW | Lumiere Solar Farm | RWE Renewables UK Limited | Melton | 2026-05-14 | 109 | 1.7km/132kV | `16541` | y |
| 135 | 87.8 | 30 | bess | PROCURING | Marsh Lane, Gowhole - Energy Storage System | Novus Renewable Services Limited | High Peak | 2025-01-17 | 591 | 0.3km/132kV | `13982` | y |
| 136 | 87.8 | 30 | bess | FUNDING_WINDOW | Wallerscote Limebeds - Battery Energy Storage | Infinis Solar Developments Limited... | Cheshire West and Chester | 2025-07-21 | 406 | 1.6km/132kV | `14887` | y |
| 137 | 87.8 | 30 | solar | FUNDING_WINDOW | Alleston Solar Farm | Stantec UK Limited | Welsh Government (NSIP) | 2026-03-10 | 174 | 0.2km/400kV | `15560` | y |
| 138 | 87.8 | 30 | bess | PROCURING | Greenfield Road, Westoning - Battery Energy Storage ... | Cragside Energy Limited | Central Bedfordshire | 2025-07-02 | 425 | 1.4km/132kV | `17411` | y |
| 139 | 87.8 | 30 | bess | FUNDING_WINDOW | Humberfield Recycling Centre - Battery Energy Storag... | FCC Environment | East Riding of Yorkshire | 2025-07-28 | 399 | 0.1km/132kV | `19009` | y |
| 140 | 87.8 | 50 | solar | FUNDING_WINDOW | Soars Lodge Farm, Foston Lane - Solar Farm | Soars Solar Limited | Blaby | 2026-03-20 | 164 | 2.0km/132kV | `12395` | y |
| 141 | 87.8 | 50 | solar | FUNDING_WINDOW | Hillam Grange, Austfield Lane - Solar Farm | Noventum Power Limited | North Yorkshire | 2025-12-19 | 255 | 0.7km/132kV | `14040` | y |
| 142 | 87.8 | 50 | bess | FUNDING_WINDOW | SSE Taynuilt Substation - Battery Energy Storage | Downing Energy Development Company... | Argyll and Bute | 2025-11-14 | 290 | 0.9km/132kV | `15648` | y |
| 143 | 87.8 | 50 | solar | FUNDING_WINDOW | Old Wood Energy Park - Solar Pv Panel | Exagen | Rushcliffe | 2026-06-05 | 87 | 1.4km/132kV | `16012` | y |
| 144 | 87.8 | 50 | bess | FUNDING_WINDOW | Tir Artair - Battery Energy Storage Facility | Opdenergy | Perth and Kinross | 2026-05-13 | 110 | 0.2km/132kV | `16292` | y |
| 145 | 87.8 | 50 | bess | FUNDING_WINDOW | Bindwells Battery Storage Facility | OPDE UK Limted | Angus | 2026-02-04 | 208 | 1.9km/132kV | `18013` | y |
| 146 | 87.7 | 49 | bess | FUNDING_WINDOW | Dougliehill Water Treatment Works, Dougliehill Road ... | Bluestone Energy | Inverclyde | 2025-08-06 | 390 | 0.8km/132kV | `16240` | **n** |
| 147 | 87.7 | 63 | bess | PROCURING | Dolphingstone Farm - Battery Energy Storage System | RNA Energy Limited | Scottish Government (S36) | 2025-07-04 | 423 | 1.2km/275kV | `13618` | y |
| 148 | 87.6 | 48 | solar | FUNDING_WINDOW | Park House Farm, Meriden Road - Solar Farm | Enviromena Asset Management UK Lim... | North Warwickshire | 2025-12-11 | 263 | 1.9km/275kV | `13440` | y |
| 149 | 87.6 | 28 | bess | FUNDING_WINDOW | Sunny Oaks Renewable Energy Park | Ridge Clean Energy Limited | Isle of Wight | 2025-07-15 | 412 | 0.7km/132kV | `12054` | y |
| 150 | 87.3 | 200 | bess | PROCURING | Corner Of Weeland Road, Lunn Lane - Battery Storage ... | Newton Energi Limited | North Yorkshire | 2025-07-31 | 396 | 0.5km/400kV | `15375` | y |
| 151 | 87.3 | 200 | bess | PROCURING | Kingston International Business Park - Battery Energ... | Story Contracting Limited | East Riding of Yorkshire | 2025-07-02 | 425 | 0.2km/132kV | `17424` | y |
| 152 | 87.2 | 150 | solar | FUNDING_WINDOW | Dean Moor Solar Farm & Battery Storage | Firma Energy / IB Vogt | The Planning Inspectorate - ... | 2026-07-02 | 60 | 0.2km/132kV | `14551` | y |
| 153 | 87.2 | 42 | solar | PROCURING | Higher Witheven Solar | Downing Renewables | Cornwall | 2025-08-19 | 377 | 0.3km/400kV | `10483` | y |
| 154 | 87.1 | 42 | solar | FUNDING_WINDOW | Valley Farm, Hessett - Solar Panels | Opdenergy UK Limted | Mid Suffolk | 2026-03-23 | 161 | 1.1km/132kV | `18471` | y |
| 155 | 87.1 | 25 | bess | FUNDING_WINDOW | Lodge Farm, Calow - Battery Energy Storage System | Enray Power | North East Derbyshire | 2025-07-16 | 411 | 0.4km/132kV | `17666` | y |
| 156 | 87.0 | 500 | bess | PROCURING | Braston New Energy | New Energy Partnership | Scottish Government (S36) | 2025-04-23 | 495 | 1.6km/275kV | `15530` | y |
| 157 | 87.0 | 11 | bess | FUNDING_WINDOW | Shore Top Farm, Kearsley Road - Battery Energy Stora... | Taiyo Power & Storage Limited | Bury | 2025-11-20 | 284 | 0.2km/132kV | `19074` | y |
| 158 | 86.9 | 40 | solar | FUNDING_WINDOW | The Coach House, Gwinear Lane - Speedwell Solar Farm | StatKraft | Cornwall | 2026-03-19 | 165 | 0.5km/132kV | `12910` | y |
| 159 | 86.9 | 40 | bess | FUNDING_WINDOW | Chillington Estate, Chillington Park - Battery Stora... | Elgin Energy Esco Limited | South Staffordshire | 2025-07-25 | 402 | 1.4km/275kV | `14087` | y |
| 160 | 86.8 | 50 | bess | FUNDING_WINDOW | Little Hale Fen - Solar Farm | AGR Solar 2 Limited | North Kesteven | 2025-08-13 | 383 | 0.8km/132kV | `9586` | y |
| 161 | 86.8 | 50 | solar | FUNDING_WINDOW | Hatton Solar Farm | Push Energy | East Lindsey | 2025-12-12 | 262 | 1.6km/132kV | `9798` | **n** |
| 162 | 86.8 | 50 | bess | PROCURING | Rigifa Cove Road - Battery Storage | Trina Solar | Aberdeen City | 2024-11-13 | 656 | 1.9km/132kV | `12970` | y |
| 163 | 86.8 | 50 | bess | FUNDING_WINDOW | Geiselittle Farm - Battery Energy Storage | Whirlwind Renewables | Highland | 2025-08-20 | 376 | 0.7km/275kV | `15387` | y |
| 164 | 86.8 | 50 | bess | FUNDING_WINDOW | Middlerigg - Battery Energy Storage | Galileo Green Energy Scotland Limi... | West Lothian | 2025-07-22 | 405 | 0.3km/275kV | `16642` | y |
| 165 | 86.8 | 50 | solar | PROCURING | Scalm Park, Wistow - Solar Farm & Battery Energy Sto... | Grenergy | North Yorkshire | 2025-09-11 | 354 | 0.7km/132kV | `16648` | y |
| 166 | 86.8 | 50 | solar | PROCURING | Titchfield Lane, Wickham - Solar Panels | Conrad Energy (Developments) II Li... | Winchester | 2025-09-25 | 340 | 1.3km/400kV | `18186` | y |
| 167 | 86.8 | 50 | solar | PROCURING | The Strawberry Line, Brinsea Road - Solar Farm | RWE Renewables UK | North Somerset | 2025-08-26 | 370 | 1.5km/132kV | `18838` | y |
| 168 | 86.6 | 100 | bess | PROCURING | Edwin Richards Quarry, Portway Road - Battery Storag... | Downing Energy Development Company... | Sandwell | 2025-02-12 | 565 | 1.4km/275kV | `13917` | y |
| 169 | 86.6 | 100 | bess | PROCURING | Pool Hall Farm, Lower Penn - Battery Storage | Elgin Energy Esco Limited | South Staffordshire | 2025-07-21 | 406 | 0.7km/132kV | `14062` | y |
| 170 | 86.6 | 100 | bess | PROCURING | Burton Green Farm - Battery Energy Storage | Conrad Energy (Developments) Limit... | Solihull | 2025-07-09 | 418 | 0.6km/132kV | `17274` | y |
| 171 | 86.6 | 100 | bess | PROCURING | National Grid Substation - Battery Energy Storage Sy... | Penso Power (BW ESS) | East Devon | 2025-08-22 | 374 | 0.2km/400kV | `17484` | y |
| 172 | 86.6 | 100 | bess | PROCURING | Upton Lane, Nursling - Battery Energy Storage | Masdar Arlington Energy | Test Valley | 2025-05-15 | 473 | 0.1km/132kV | `16191` | y |
| 173 | 86.5 | 98 | bess | PROCURING | Henwood Lane, Catherine De Barnes - Battery Storage ... | ARL016 | Solihull | 2025-07-30 | 397 | 0.4km/132kV | `16425` | y |
| 174 | 86.4 | 21 | bess | FUNDING_WINDOW | Leeway House, Leeway Industrial Estate - Battery Ene... | Aldustria Limited | Newport | 2025-07-25 | 402 | 0.4km/132kV | `18327` | y |
| 175 | 86.3 | 200 | bess | PROCURING | Earthcott Green Farm, Earthcott Green - Battery Ener... | Immersa Limited | South Gloucestershire | 2025-07-30 | 397 | 0.5km/132kV | `13643` | y |
| 176 | 86.3 | 200 | bess | PROCURING | Bay Gateway - Battery Storage Facility | Energi Generation | Lancaster | 2025-03-21 | 528 | 0.7km/132kV | `17028` | y |
| 177 | 86.3 | 200 | bess | PROCURING | Yaxley, Eye Airfield Industrial Estate - Battery Sto... | Field Yaxley Limited | Mid Suffolk | 2025-07-04 | 423 | 0.9km/400kV | `17833` | y |
| 178 | 86.3 | 200 | bess | PROCURING | Barn Farm - Batter Energy Storage Facility | Harmony Energy Storage | South Derbyshire | 2025-07-04 | 423 | 0.4km/400kV | `17982` | y |
| 179 | 86.1 | 90 | bess | PROCURING | Summerway Drove, East Bower - Battery Storage | Renewable Connections Developments... | Somerset | 2025-02-10 | 567 | 0.4km/400kV | `15716` | y |
| 180 | 86.0 | 300 | bess | PROCURING | Kintore Battery Energy Storage Project | Alcemi Storage Development Limited | Scottish Government (S36) | 2025-05-07 | 481 | 0.4km/132kV | `10467` | y |
| 181 | 86.0 | 300 | bess | PROCURING | Mossmorran Battery Storage | Gresham House Devco Pipeline | Scottish Government (S36) | 2025-05-06 | 482 | 0.9km/132kV | `15426` | y |
| 182 | 85.9 | 40 | solar | PROCURING | Middleton Farm Cottage, Middleton Road - Solar Photo... | Bluestone Energy Limited | Renfrewshire | 2025-09-03 | 362 | 1.7km/132kV | `15760` | y |
| 183 | 85.8 | 30 | bess | FUNDING_WINDOW | Ditcher Law Wind Farm | E Power Ltd | Scottish Government (S36) | 2026-02-13 | 199 | 1.5km/132kV | `8376` | y |
| 184 | 85.8 | 30 | bess | FUNDING_WINDOW | Medlock Road, Failsworth - Battery Energy Storage | Root Power (North) Limited | Oldham | 2025-10-21 | 314 | 0.3km/132kV | `17657` | y |
| 185 | 85.8 | 30 | bess | FUNDING_WINDOW | Woodend And Moor Row, Egremont - Battery Energy Stor... | JT Energy Storage (Windel Energy) | Cumberland | 2025-12-15 | 259 | 0.6km/132kV | `19121` | y |
| 186 | 85.5 | 60 | bess | FUNDING_WINDOW | Knuzden Moss Farm, Oswaldtwistle - Battery Energy St... | Root Power (North) Limited | Hyndburn Borough | 2025-10-28 | 307 | 0.2km/132kV | `16758` | y |
| 187 | 85.5 | 342 | bess | PROCURING | Kincardine Battery Storage | Gresham House Devco Pipeline Limit... | Scottish Government (S36) | 2025-07-22 | 405 | 0.5km/275kV | `15527` | y |
| 188 | 85.4 | 21 | solar | FUNDING_WINDOW | Lower Wyke Farm, St Mary Bourne - Solar Farm | British Solar Renewables | Basingstoke and Deane | 2026-06-11 | 81 | 0.4km/132kV | `10973` | y |
| 189 | 85.4 | 75 | bess | PROCURING | Ashton Road, Bredbury - Battery Energy Storage | Cragside Energy Limited | Stockport | 2025-07-24 | 403 | 1.2km/275kV | `16667` | y |
| 190 | 85.4 | 35 | solar | PROCURING | Water Hall Farm, Waterhall Road - Solar Farm | Bluefield Renewable Developments L... | West Suffolk | 2025-07-04 | 423 | 0.4km/400kV | `13120` | y |
| 191 | 85.2 | 250 | bess | PROCURING | East York Energy Hub | York Energy Park Limited | York | 2025-09-15 | 350 | 0.3km/132kV | `10583` | y |
| 192 | 85.2 | 249 | bess | PROCURING | Stracathro - Battery Energy Storage System | Opdenergy UK 8 Limited | Scottish Government (S36) | 2025-08-13 | 383 | 0.5km/132kV | `14042` | y |
| 193 | 85.2 | 150 | bess | PROCURING | Belston Battery Storage | KX Alpha Ltd | Scottish Government (S36) | 2025-07-22 | 405 | 0.3km/275kV | `14545` | y |
| 194 | 85.1 | 25 | bess | FUNDING_WINDOW | Fernishaw Solar Farm & Battery Energy Storage Facili... | Elgin Energy (EEB67) | Scottish Government (S36) | 2025-07-23 | 404 | 0.7km/275kV | `14540` | y |
| 195 | 84.8 | 50 | bess | FUNDING_WINDOW | Shereford Road, West Raynham Estate - Battery Energy... | Bluefield Renewable Developments L... | North Norfolk | 2025-11-04 | 300 | 1.6km/132kV | `19006` | y |
| 196 | 84.8 | 50 | bess | FUNDING_WINDOW | Milton Farm - Energy Storage System | Renewco Power | Dumfries and Galloway | 2025-07-30 | 397 | 0.3km/400kV | `13846` | y |
| 197 | 84.8 | 50 | bess | PROCURING | Peterstow Gas Compressor Station, Hentland - Energy ... | Novus Renewable Services Limited | Herefordshire, County of | 2025-03-19 | 530 | 0.1km/132kV | `13976` | y |
| 198 | 84.8 | 50 | solar | FUNDING_WINDOW | Caudwell Farm, Hollbeach - Solar Array | Green Energy International | South Holland | 2026-02-03 | 209 | 2.4km/132kV | `14653` | y |
| 199 | 84.8 | 50 | bess | PROCURING | Hobble Lane, Great Wyrley - Battery Energy Storage | Anglo ES Great Wyrley Limited | South Staffordshire | 2025-02-20 | 557 | 0.1km/132kV | `15802` | y |
| 200 | 84.8 | 50 | bess | FUNDING_WINDOW | Milton Farm - Energy Storage System | Renewco Power | Dumfries and Galloway | 2025-07-30 | 397 | 0.3km/400kV | `16895` | y |
| 201 | 84.8 | 50 | bess | FUNDING_WINDOW | Middleton Of Potterton Farm - Battery Energy Storage... | Green Switch Capital (Qair) | Aberdeenshire | 2025-07-09 | 418 | 1.7km/275kV | `17259` | y |
| 202 | 84.6 | 22 | bess | FUNDING_WINDOW | Sacketts Hill Farm - Battery Energy Storage System | Greenfield Limited | Thanet | 2025-08-06 | 390 | 1.2km/132kV | `16556` | y |
| 203 | 84.6 | 22 | solar | FUNDING_WINDOW | Pudds Cross Farm, Pudds Cross - Solar Panels & Batte... | BSR Energy | Dacorum | 2025-12-23 | 251 | 0.8km/132kV | `17108` | y |
| 204 | 84.6 | 100 | bess | PROCURING | The Old Vicarage, Reedley - Battery Storage | European Energy A/S | Pendle | 2025-06-26 | 431 | 1.0km/132kV | `12767` | y |
| 205 | 84.6 | 100 | bess | FUNDING_WINDOW | Hallyburton - Battery Storage | Balance Power Projects Limited | Scottish Government (S36) | 2025-10-02 | 333 | 1.3km/132kV | `14990` | y |
| 206 | 84.5 | 60 | solar | PROCURING | Stirling Battery and Solar Energy Park | EcoDev Group Limited | Scottish Government (S36) | 2026-02-11 | 201 | 1.5km/132kV | `14995` | y |
| 207 | 84.5 | 60 | bess | PROCURING | Canalside - Battery Storage System | Greenfield Energy Developments Lim... | South Staffordshire | 2025-07-14 | 413 | 0.6km/132kV | `17623` | y |
| 208 | 84.4 | 45 | bess | FUNDING_WINDOW | EV Charging Station Development in Toomebridge | Heron Storage Limited | Mid Ulster | 2025-10-15 | 320 | 0.3km/275kV | `17038` | y |
| 209 | 84.3 | 200 | bess | PROCURING | Eskrigg End Road, Old Hutton - Battery Energy Storag... | Harmony MS Limited | Westmorland and Furness | 2025-07-10 | 417 | 0.2km/400kV | `17376` | y |
| 210 | 84.3 | 200 | bess | PROCURING | Dunton Lane - Battery Energy Storage System | Harmony BW Limited | Central Bedfordshire | 2025-07-21 | 406 | 0.7km/400kV | `17651` | y |
| 211 | 84.0 | 52 | bess | PROCURING | Woodstock Road, Yarnton - Battery Energy Storage Sys... | Renewable Connections Developments... | Cherwell | 2025-06-13 | 444 | 0.1km/132kV | `17593` | y |
| 212 | 83.9 | 24 | bess | FUNDING_WINDOW | Parkhouse Road - Battery Energy Storage | GPC 1184 Limited | Glasgow City | 2025-08-08 | 388 | 0.1km/132kV | `16086` | y |
| 213 | 83.9 | 40 | solar | PROCURING | Fibden Farm, Hampton Lovett - Solar Array | Grenergy Renewables | Wychavon | 2025-07-29 | 398 | 0.8km/132kV | `16721` | y |
| 214 | 83.8 | 50 | bess | PROCURING | Westfield Road, Carlton - Battery Storage | Firma Vogt Solar Limited | Leeds | 2025-07-14 | 413 | 0.1km/132kV | `13264` | **n** |
| 215 | 83.8 | 50 | bess | PROCURING | Withy Place, Bramley Road - Battery Energy Storage | Root Power South Limited | Basingstoke and Deane | 2025-07-02 | 425 | 0.3km/400kV | `17240` | y |
| 216 | 83.8 | 50 | bess | PROCURING | Park Road, Overseal - Battery Storage Facility | Care Power Overseal | South Derbyshire | 2025-07-25 | 402 | 1.9km/132kV | `17586` | y |
| 217 | 83.8 | 50 | bess | PROCURING | Glassenbury - Battery Storage System | Gresham House | Tunbridge Wells | 2025-04-23 | 495 | 0.6km/132kV | `18392` | y |
| 218 | 83.8 | 50 | bess | PROCURING | Hinksford Substation, Hinksford Lane - Battery Energ... | Balance Power Projects Limited | South Staffordshire | 2025-03-06 | 543 | 0.1km/132kV | `16101` | y |
| 219 | 83.8 | 50 | bess | PROCURING | Anchor Lane, Burwell - Battery Energy Storage | Burwell AL Limited | East Cambridgeshire | 2025-05-20 | 468 | 1.0km/132kV | `16094` | y |
| 220 | 83.8 | 50 | bess | PROCURING | Cornhills Farm, Muttonhole Road - Battery Storage | Big Battery (Sheriff Faulds Farm 1... | South Lanarkshire | 2025-02-07 | 570 | 0.2km/400kV | `11647` | y |
| 221 | 83.8 | 50 | bess | FUNDING_WINDOW | Long Lane, Stanwell - Battery Energy Storage | Harwood Project One Limited | Spelthorne | 2025-07-18 | 409 | 2.4km/132kV | `13133` | **n** |
| 222 | 83.8 | 50 | bess | PROCURING | Ebstree Road, Trysull - Battery Energy Storage | Bengrove Bess Limited | South Staffordshire | 2024-11-21 | 648 | 0.3km/400kV | `14497` | y |
| 223 | 83.8 | 23 | solar | FUNDING_WINDOW | Swallett Energy Park | Exagen | Wiltshire | 2026-01-21 | 222 | 2.7km/400kV | `14171` | y |
| 224 | 83.7 | 2 | solar | FUNDING_WINDOW | Exolum, Silver Lane - Solar PV Array | Exolum Limited | West Berkshire | 2026-06-05 | 87 | 1.3km/400kV | `19943` | y |
| 225 | 83.6 | 100 | bess | PROCURING | Learielaw Farm, Learielaw - Battery Energy Storage | Intelligent Land Investments Group | Scottish Government (S36) | 2025-05-19 | 469 | 0.7km/132kV | `7970` | **n** |
| 226 | 83.6 | 100 | bess | PROCURING | Newfields Farm, Rownall Road - Battery Energy Storag... | REPD Limited | Staffordshire Moorlands | 2025-07-10 | 417 | 0.2km/132kV | `14342` | **n** |
| 227 | 83.5 | 36 | solar | PROCURING | Woodlands Farm, Clapton - Ground Mounted Solar Park | Ecotricity Generation Limited | Stroud | 2025-08-05 | 391 | 0.8km/132kV | `12586` | y |
| 228 | 83.3 | 1 | solar | FUNDING_WINDOW | Wipac Group, London Road - Solar Panels | Wipac Group | Buckinghamshire | 2026-06-10 | 82 | 1.9km/400kV | `20788` | y |
| 229 | 83.2 | 20 | bess | PROCURING | Reeds Solar Farm, Alders Road - Solar Farm & Battery... | Low Carbon | Tunbridge Wells | 2025-03-06 | 543 | 0.2km/132kV | `12940` | y |
| 230 | 82.9 | 40 | bess | PROCURING | Heanor Road - Battery Energy Storage System | Downing Energy Development Company... | Amber Valley | 2025-02-14 | 563 | 1.1km/132kV | `13472` | y |
| 231 | 82.9 | 40 | bess | PROCURING | Newton Of Pitfodels - Battery Storage | Flexion Energy Uk Storage | Aberdeen City | 2025-03-28 | 521 | 0.3km/132kV | `13606` | y |
| 232 | 82.9 | 40 | bess | PROCURING | Electricity Substation, Bellevue Lane - Battery Stor... | Coriolis Energy | Cheshire West and Chester | 2025-05-07 | 481 | 0.2km/132kV | `16357` | y |
| 233 | 82.8 | 30 | solar | FUNDING_WINDOW | Hook Lane, Malshanger | Nextpower SPV 18 Limited | Basingstoke and Deane | 2026-02-13 | 199 | 4.0km/400kV | `7962` | y |
| 234 | 82.8 | 30 | bess | FUNDING_WINDOW | Colbrans Farm Estate, Laughton - Battery Storage | Innova | Wealden | 2025-07-21 | 406 | 1.8km/132kV | `11681` | y |
| 235 | 82.8 | 30 | bess | FUNDING_WINDOW | Blackpark House - Battery Storage | Anesco | Highland | 2025-10-14 | 321 | 1.9km/132kV | `12383` | y |
| 236 | 82.8 | 50 | bess | FUNDING_WINDOW | Bridgend Farm, Arbuthnott - Battery Energy Storage S... | OPDE UK Limted | Aberdeenshire | 2025-09-16 | 349 | 0.2km/132kV | `16522` | y |
| 237 | 82.8 | 1 | solar | FUNDING_WINDOW | Dewsbury Sewage, Clough Lane - Solar Panels | Downing Renewables | Wakefield | 2026-05-12 | 111 | 1.7km/132kV | `14404` | **n** |
| 238 | 82.8 | 1 | bess | FUNDING_WINDOW | Docks Way Disposal Site, Docks Way - Battery Energy ... | Newport City Council | Newport | 2026-02-12 | 200 | 0.4km/132kV | `20120` | y |
| 239 | 82.7 | 80 | bess | PROCURING | West Kingsmill, Landulph - Battery Storage | Boultbee Brooks Real Estate Herefo... | Cornwall | 2025-07-18 | 409 | 0.3km/132kV | `13687` | y |
| 240 | 82.7 | 80 | bess | PROCURING | Europa Way - Battery Storage Facility | Newton Energi Limited | North East Lincolnshire | 2025-05-20 | 468 | 0.4km/132kV | `17763` | y |
| 241 | 82.6 | 13 | solar | FUNDING_WINDOW | Ewanrigg Farmhouse, Ewanrigg - Solar Farm | Anesco Limited | Cumberland | 2026-06-03 | 89 | 1.7km/132kV | `18952` | y |
| 242 | 82.1 | 70 | bess | PROCURING | Persley BESS - Battery Storage | Anesco | Scottish Government (S36) | 2025-06-04 | 453 | 1.1km/275kV | `14537` | y |
| 243 | 82.1 | 70 | bess | PROCURING | Severn Road, Hallen - Battery Storage Facility | EL Avonmouth Limited | South Gloucestershire | 2025-02-24 | 553 | 0.4km/400kV | `15027` | y |
| 244 | 82.1 | 70 | bess | PROCURING | Boxgrove Common, Tinwood Lane - Battery Energy Stora... | Net Zero Fifteen Limited | Chichester | 2025-07-23 | 404 | 0.2km/132kV | `17294` | y |
| 245 | 82.1 | 42 | bess | FUNDING_WINDOW | Glentaggart - Battery Energy Storage | South Lanarkshire Council / Brockw... | South Lanarkshire | 2026-01-29 | 214 | 1.1km/400kV | `18360` | y |
| 246 | 82.1 | 25 | bess | FUNDING_WINDOW | Ash Tree Solar Farm & Battery Storage | Low Carbon Limited | South Kesteven | 2025-07-18 | 409 | 1.5km/132kV | `15396` | y |
| 247 | 82.1 | 32 | bess | PROCURING | Post Farm, Lytchett Minster - Battery Energy Storage | S4N Lytchett Limited | Dorset | 2024-11-28 | 641 | 1.0km/132kV | `10291` | y |
| 248 | 82.0 | 300 | bess | FUNDING_WINDOW | Philips Mains, Mey - Battery Energy Storage | Ampeak Energy | Scottish Government (S36) | 2026-01-19 | 224 | 18.1km/275kV | `14987` | y |
| 249 | 81.9 | 40 | bess | FUNDING_WINDOW | Tar Solar Farm | Bluefield Renewable Developments L... | West Oxfordshire | 2025-09-05 | 360 | 0.7km/132kV | `17629` | y |
| 250 | 81.8 | 65 | bess | PROCURING | Ashday Hall Farm, Ashday Lane - Battery Energy Stora... | Sandbrook Capital Bes Limited | Calderdale | 2025-03-12 | 537 | 0.1km/132kV | `16909` | y |
| 251 | 81.8 | 50 | bess | PROCURING | Weald Farm, Cambridge Road - Solar Farm & Battery St... | Ashfield District Council / Voltal... | Huntingdonshire | 2025-05-08 | 480 | 0.5km/132kV | `14873` | y |
| 252 | 81.8 | 50 | bess | PROCURING | Owls Hatch Road, Thanet Way - Battery Energy Storage... | Root Power South Limited | Canterbury | 2025-07-03 | 424 | 0.1km/132kV | `18017` | y |
| 253 | 81.8 | 30 | solar | PROCURING | Manor Farm, South Hiendley - Solar Photovoltaic Farm | Enzygo Limited | Wakefield | 2025-07-25 | 402 | 0.1km/132kV | `12659` | y |
| 254 | 81.8 | 30 | bess | PROCURING | Tanners Lane - Battery Energy Storage System | Tag Energy Development UK Limited | Solihull | 2025-06-23 | 434 | 0.1km/132kV | `15128` | **n** |
| 255 | 81.8 | 30 | bess | PROCURING | West Moss Lane, Higher Ballam - Battery Energy Stora... | Lower 48 Energy BESS Limited | Fylde | 2025-04-30 | 488 | 0.6km/132kV | `16767` | y |
| 256 | 81.8 | 30 | bess | PROCURING | Biggar Road, Cleland - Battery Energy Storage System | Starlight Energy SPV 1 Limited | North Lanarkshire | 2025-03-12 | 537 | 0.4km/275kV | `17064` | y |
| 257 | 81.8 | 30 | bess | PROCURING | Chosen Park, Baglan Energy Park - Unit 3 - Battery S... | Aldustria Energy Storage | Neath Port Talbot | 2025-06-19 | 438 | 0.1km/275kV | `18342` | y |
| 258 | 81.8 | 50 | bess | PROCURING | Silkstead Farm, Poles Lane - Battery Energy Storage ... | Winchester Energy Reserve Limited | Winchester | 2025-03-13 | 536 | 0.5km/132kV | `15674` | y |
| 259 | 81.7 | 22 | solar | PROCURING | New Hall Farm, New Hall Lane - Solar Farm | Downing Energy Development Company... | Wakefield | 2025-06-11 | 446 | 1.8km/400kV | `12776` | y |
| 260 | 81.6 | 10 | solar | FUNDING_WINDOW | Duckinfield Farm, Hurst Lane - Solar Farm | Noventum Power Limited | Warrington | 2026-05-22 | 101 | 4.3km/132kV | `16992` | y |
| 261 | 81.6 | 10 | bess | FUNDING_WINDOW | Pudds Cross Farm, Pudds Cross - Solar Panels & Batte... | BSR Energy | Dacorum | 2025-12-23 | 251 | 0.8km/132kV | `17107` | y |
| 262 | 81.6 | 100 | bess | PROCURING | High Boydstone Farm - Battery Energy Storage Facilit... | New Energy Partnership | Scottish Government (S36) | 2025-06-02 | 455 | 1.8km/132kV | `16174` | y |
| 263 | 81.6 | 100 | bess | PROCURING | Lane Side - Energy Storage | Net Zero Twenty Three Limited | Bradford | 2025-07-16 | 411 | 0.1km/132kV | `17416` | y |
| 264 | 81.6 | 60 | bess | PROCURING | Holmquarry Road - Battery Storage | Big Battery (Holmquarry Road) Limi... | Scottish Government (S36) | 2025-07-22 | 405 | 0.4km/275kV | `11581` | y |
| 265 | 81.5 | 2 | solar | FUNDING_WINDOW | Princess Royal Hospital, Grainger Drive - Solar PV P... | Shresbury and Telford Hospital NHS... | Telford and Wrekin | 2026-06-01 | 91 | 1.2km/132kV | `20763` | y |
| 266 | 81.5 | 99 | bess | PROCURING | Station Road, Carlton - Battery Energy Storage Syste... | Root Power (North) Limited | North Yorkshire | 2025-05-14 | 474 | 0.5km/400kV | `17577` | y |
| 267 | 81.4 | 45 | bess | PROCURING | Lower Bodachra - Energy Storage System | Novus Renewables Services Limited | Scottish Government (S36) | 2025-06-24 | 433 | 0.6km/275kV | `14301` | y |
| 268 | 81.3 | 57 | bess | PROCURING | Saundercroft Road, Broadclyst - Battery Energy Stora... | Pivoted Power Llp | East Devon | 2025-07-18 | 409 | 0.3km/132kV | `18044` | y |
| 269 | 81.3 | 26 | solar | PROCURING | Lowfield Farm - Solar Farm | Renewable Connections Developments... | Central Bedfordshire | 2025-11-03 | 301 | 0.6km/400kV | `16062` | y |
| 270 | 81.2 | 20 | solar | PROCURING | Leighton Road & Hawthorn - Solar Panels | Econergy International Limited | Central Bedfordshire | 2025-07-29 | 398 | 1.1km/132kV | `12613` | y |
| 271 | 81.2 | 5 | bess | FUNDING_WINDOW | Menear Road - Solar & Battery storage | Anesco Limited | Cornwall | 2026-02-13 | 199 | 2.0km/132kV | `11078` | y |
| 272 | 81.1 | 25 | bess | PROCURING | West Thorpe Church Farm, Willoughby On The Wolds - B... | Integrum Renewable Energy Limited | Rushcliffe | 2024-09-24 | 706 | 0.2km/132kV | `15938` | y |
| 273 | 80.9 | 40 | solar | FUNDING_WINDOW | Kimblewick Road Solar Farm | Kimblewick Solar Limited | Buckinghamshire | 2026-01-14 | 229 | 2.9km/400kV | `13227` | y |
| 274 | 80.9 | 40 | solar | PROCURING | Chillington Estate, Chillington Park - Solar Panels | Elgin Energy Esco Limited | South Staffordshire | 2025-07-25 | 402 | 1.4km/275kV | `14088` | y |
| 275 | 80.8 | 50 | bess | PROCURING | Greens Farm - Battery energy storage | Cambridge Power | East Hertfordshire | 2025-07-18 | 409 | 0.0km/132kV | `9012` | y |
| 276 | 80.8 | 50 | bess | PROCURING | Monets Garden Battery, Osbaldwick - Energy Storage F... | Monets Garden Battery Limited | York | 2025-03-28 | 521 | 0.3km/132kV | `17496` | y |
| 277 | 80.8 | 50 | solar | PROCURING | Little Hale Fen - Solar Farm | AGR Solar 2 Limited | North Kesteven | 2025-08-13 | 383 | 0.8km/132kV | `14955` | y |
| 278 | 80.8 | 30 | bess | FUNDING_WINDOW | Kellas Wind Farm | E Power Limited | Scottish Government (S36) | 2026-01-22 | 221 | 0.7km/275kV | `16138` | y |
| 279 | 80.8 | 50 | bess | PROCURING | Hewitts Avenue, New Waltham - Battery Storage | Harmony HS (JB) Limited | North East Lincolnshire | 2025-03-28 | 521 | 0.3km/132kV | `11832` | y |
| 280 | 80.8 | 50 | bess | PROCURING | Dunbar Grid Substation - Battery Storage | FRV TH Powertek Limited | East Lothian | 2024-10-01 | 699 | 0.2km/132kV | `13864` | y |
| 281 | 80.8 | 50 | bess | PROCURING | Balblair Quarry, Balblair - Battery Energy Storeage ... | Lovat Estates Limited (LG-B-50a Li... | Highland | 2025-05-30 | 458 | 0.3km/275kV | `14635` | y |
| 282 | 80.8 | 50 | bess | PROCURING | Carseview Road - Battery Energy Storage System | Unknown | Angus | 2025-06-11 | 446 | 1.1km/132kV | `15494` | y |
| 283 | 80.8 | 50 | bess | PROCURING | Duniface Gas Peaking Plant - Battery Energy Storage ... | Forsa Energy Gas Holdings Limited | Fife | 2024-09-26 | 704 | 0.1km/132kV | `15749` | y |
| 284 | 80.8 | 50 | bess | PROCURING | The Greenlink Converter Station - Lambeeth Battery E... | Sirius EcoDev Limited | Pembrokeshire | 2024-10-16 | 684 | 0.1km/400kV | `15803` | y |
| 285 | 80.8 | 50 | bess | PROCURING | Newburgh Road, Abernethy - Battery Energy Storage Fa... | Opdenergy | Perth and Kinross | 2025-05-15 | 473 | 0.2km/275kV | `16286` | y |
| 286 | 80.8 | 50 | bess | PROCURING | Eweleaze Spinney - Battery Energy Storage Facility | Weymouth Battery Limited | Dorset | 2025-04-04 | 514 | 0.1km/400kV | `17121` | y |
| 287 | 80.8 | 50 | bess | PROCURING | Broomloan Road - Battery Energy Storage | Lifetime Property Limited | Glasgow City | 2024-10-04 | 696 | 0.1km/132kV | `17129` | y |
| 288 | 80.8 | 23 | solar | PROCURING | Turners Lane, Barnacre - Solar Farm | Noventum Power Limited | Wyre | 2025-08-05 | 391 | 0.7km/400kV | `14397` | y |
| 289 | 80.8 | 50 | bess | PROCURING | Brown Edge - Battery Storage | Anesco | Staffordshire Moorlands | 2025-05-07 | 481 | 0.4km/132kV | `11418` | y |
| 290 | 80.6 | 22 | solar | PROCURING | Wallerscote Limebeds - Solar Pv Park | Infinis Solar Developments Limited... | Cheshire West and Chester | 2025-07-21 | 406 | 1.6km/132kV | `14888` | y |
| 291 | 80.4 | 35 | bess | FUNDING_WINDOW | Quarry Solar Farm & Battery Storage Facility | JBM Solar Projects 34 Limited | West Oxfordshire | 2025-07-28 | 399 | 3.6km/132kV | `13492` | **n** |
| 292 | 80.4 | 45 | bess | PROCURING | Slack Lane, Westhoughton - Battery Energy Storage Sy... | Foundation Property & Capital Grou... | Bolton | 2024-12-24 | 615 | 2.3km/132kV | `17105` | y |
| 293 | 80.2 | 20 | bess | PROCURING | Former EON Power Station, Booth Lane - Battery Energ... | Bluefield Sandbach Limited | Cheshire East | 2025-04-11 | 507 | 0.8km/132kV | `10436` | **n** |
| 294 | 80.2 | 20 | solar | PROCURING | Sunny Oaks Renewable Energy Park | Ridge Clean Energy Limited | Isle of Wight | 2025-07-15 | 412 | 0.7km/132kV | `12055` | **n** |
| 295 | 80.2 | 20 | bess | PROCURING | Craigshaw Drive - Battery Storage Facility & Electri... | Craigshaw Drive Ev Limited | Aberdeen City | 2024-10-01 | 699 | 0.7km/132kV | `15435` | y |
| 296 | 80.2 | 20 | solar | PROCURING | Station Road, Tivetshall St Margaret - Solar PV Pane... | Pathfinder Clean Energy UK Dev Lim... | South Norfolk | 2025-06-30 | 427 | 1.0km/400kV | `16035` | y |
| 297 | 80.2 | 20 | bess | PROCURING | Clayhill Farm, Greenfield Road - Battery Energy Stor... | Conrad Energy (Developments) Limit... | Central Bedfordshire | 2024-12-18 | 621 | 0.3km/132kV | `16782` | y |
| 298 | 80.2 | 1 | solar | FUNDING_WINDOW | Co-Op Nisa, Waldo Way - Solar Panels | Co-Operative | North Lincolnshire | 2026-05-13 | 110 | 0.6km/132kV | `20715` | y |
| 299 | 80.0 | 4 | solar | PROCURING | Knauf UK Sittingbourne, Barge Way - Solar Panels | Knauf (UK) GMBH | Swale | 2026-02-24 | 188 | 0.4km/132kV | `20305` | y |
| 300 | 79.9 | 40 | bess | PROCURING | Tredington House Farm, Tredington - Battery Energy S... | Greenfield Energy Developments Ltd | Tewkesbury | 2024-12-10 | 629 | 0.2km/132kV | `16562` | y |
| 301 | 79.8 | 30 | bess | FUNDING_WINDOW | Thrift Solar Farm and BESS | IB Vogt UK Limited | Epping Forest | 2025-12-24 | 250 | 2.1km/275kV | `18681` | y |
| 302 | 79.8 | 30 | solar | FUNDING_WINDOW | Thrift Solar Farm and BESS | IB Vogt UK Limited | Epping Forest | 2025-12-24 | 250 | 2.1km/275kV | `18682` | y |
| 303 | 79.8 | 30 | solar | FUNDING_WINDOW | Parsonage Farm - Solar PV Farm & Battery Storage | Trilogy Logistics REIT Limited | Essex | 2026-01-29 | 214 | 4.2km/132kV | `19354` | y |
| 304 | 79.8 | 50 | bess | FUNDING_WINDOW | Lythmore House, Technology Park Forss - Battery Ener... | Forss Energy Storage Limited | Highland | 2025-08-13 | 383 | 4.8km/275kV | `17703` | y |
| 305 | 79.7 | 18 | solar | PROCURING | Menear Road - Solar & Battery storage | Anesco Limited | Cornwall | 2026-02-13 | 199 | 2.0km/132kV | `11077` | y |
| 306 | 79.5 | 60 | bess | PROCURING | Inchbean Farm, Treeswoodhead Road - Battery Energy S... | RNA Energy Limited | Scottish Government (S36) | 2025-06-19 | 438 | 1.1km/275kV | `13323` | y |
| 307 | 79.4 | 45 | bess | FUNDING_WINDOW | Sclenteuch Wind Farm | RES Limited | Scottish Government (S36) | 2025-12-16 | 258 | 0.7km/275kV | `9930` | y |
| 308 | 79.2 | 20 | bess | FUNDING_WINDOW | Battery Energy Storage System Development in Moneymo... | J D Excavations Tyrone Limited | Mid Ulster | 2025-12-11 | 263 | 5.3km/275kV | `18059` | y |
| 309 | 79.2 | 5 | bess | FUNDING_WINDOW | Trekenning Farm - Battery Storage Facility & Co-Op | Wessex Strategic | Cornwall | 2025-12-23 | 251 | 4.1km/132kV | `12912` | y |
| 310 | 79.1 | 15 | solar | PROCURING | Buttercombe Lane - Solar Farm | Exagen Development Limited | North Devon | 2026-03-26 | 158 | 2.0km/132kV | `19125` | y |
| 311 | 78.9 | 24 | solar | PROCURING | Flordon Road, Bracon Ash - Solar Panels & Battery St... | Ralos Projects Limited | South Norfolk | 2025-07-04 | 423 | 1.9km/400kV | `14308` | y |
| 312 | 78.8 | 50 | bess | PROCURING | Admiralty Road - Battery Energy Storage Facility | Abbey Power Solution Limited | Great Yarmouth | 2025-07-10 | 417 | 4.1km/132kV | `9470` | **n** |
| 313 | 78.8 | 50 | bess | PROCURING | Stonehill Energy Storage | Penso Power (BW ESS) | Wiltshire | 2025-05-02 | 486 | 0.2km/132kV | `11812` | y |
| 314 | 78.8 | 50 | bess | PROCURING | Shindour, Feddal Hill Wood - Battery Energy Storage ... | Whirlwind Energy Storage Limited | Perth and Kinross | 2024-10-24 | 676 | 0.3km/400kV | `13236` | y |
| 315 | 78.8 | 30 | solar | PROCURING | Marsh Lane Solar Farm, Lion Road - Solar Farm | Aura Power Storage Solutions | South Norfolk | 2025-08-13 | 383 | 1.0km/400kV | `13987` | y |
| 316 | 78.8 | 30 | bess | PROCURING | Fox Cover Road - Battery Energy Storage | Newton Energi Limited | Sunderland | 2024-09-26 | 704 | 0.5km/275kV | `14968` | y |
| 317 | 78.8 | 30 | bess | PROCURING | Immingham Solar Farm - Battery Storage Facility | One Planet Developments Limited | North East Lincolnshire | 2025-05-06 | 482 | 0.9km/132kV | `16092` | y |
| 318 | 78.8 | 30 | solar | FUNDING_WINDOW | Mundham, Runcton Lane - Solar Farm | BNRG Renewables Limited | Chichester | 2026-03-11 | 173 | 7.4km/132kV | `17029` | y |
| 319 | 78.8 | 30 | bess | PROCURING | Ellenroad Farm, Bentgate Street - Battery Energy Sto... | Root Power (North) Limited | Rochdale | 2025-03-14 | 535 | 2.8km/132kV | `17293` | y |
| 320 | 78.8 | 30 | solar | FUNDING_WINDOW | Heydon Road, Heydon - Solar PV Panels | Grupotec | North Norfolk | 2026-04-01 | 152 | 5.2km/132kV | `18268` | y |
| 321 | 78.8 | 50 | solar | PROCURING | Ash Tree Solar Farm & Battery Storage | Low Carbon Limited | South Kesteven | 2025-07-18 | 409 | 1.5km/132kV | `15397` | y |
| 322 | 78.8 | 50 | solar | PROCURING | Moreton Brook Farm, Lea Lane - Solar Farm | Aura Power Developments Limited | East Staffordshire | 2025-07-25 | 402 | 1.3km/132kV | `17591` | y |
| 323 | 78.8 | 30 | bess | PROCURING | Electricity Substation, Bardarroch - Battery Energy ... | Balance Power Projects Limited | East Ayrshire | 2025-03-04 | 545 | 0.1km/275kV | `15569` | y |
| 324 | 78.8 | 50 | bess | PROCURING | Wombourne Road, Wombourne - Battery Energy Storage S... | Pathfinder Clean Energy UK Dev Lim... | South Staffordshire | 2025-05-29 | 459 | 0.5km/132kV | `15934` | y |
| 325 | 78.8 | 49 | bess | PROCURING | Chapel Lane - Battery Energy Storage System | Anesco Limited | Walsall | 2025-01-13 | 595 | 0.1km/400kV | `9721` | **n** |
| 326 | 78.7 | 2 | solar | PROCURING | Cranswick Convenience Foods, Valley Park Industrial ... | Cranswick Convenience Foods | Barnsley | 2026-02-12 | 200 | 0.2km/132kV | `20280` | y |
| 327 | 78.7 | 80 | solar | PROCURING | Nettly Burn Renewable Energy Park | Grupotec Solar UK 4 Ltd | Scottish Government (S36) | 2026-03-06 | 178 | 3.3km/132kV | `15539` | y |
| 328 | 78.6 | 17 | bess | FUNDING_WINDOW | Battery Energy Storage Facility Development in Derry | Heron Property Limited | Derry City and Strabane | 2025-12-19 | 255 | 5.2km/275kV | `18441` | y |
| 329 | 78.6 | 100 | bess | PROCURING | Lions Den, Hammerwich - Battery Storage Facility | Elgin Energy Services Limited | Lichfield | 2025-07-24 | 403 | 3.5km/275kV | `14418` | y |
| 330 | 78.6 | 100 | bess | PROCURING | Kilwinning Battery Storage | Apatura | Scottish Government (S36) | 2025-05-21 | 467 | 0.3km/132kV | `15783` | y |
| 331 | 78.6 | 100 | bess | PROCURING | Woodford Road - Battery Energy Storage System | Pegasus Group | Stockport | 2025-05-30 | 458 | 3.9km/275kV | `15902` | y |
| 332 | 78.6 | 100 | bess | PROCURING | Derby Road, Egginton - Battery Storage Facility | First Way Solar Limited | South Derbyshire | 2025-06-24 | 433 | 1.7km/132kV | `16378` | y |
| 333 | 78.6 | 100 | bess | PROCURING | West Leake Lane, Ratcliffe - Battery Storage | Renewable Energy Systems RES ltd (... | Rushcliffe | 2025-07-10 | 417 | 3.0km/132kV | `17002` | y |
| 334 | 78.5 | 99 | bess | PROCURING | Little Hale Drove, Little Hale Fen - Battery Storage | Root-Power (South) Limited | North Kesteven | 2025-03-14 | 535 | 0.9km/400kV | `17585` | y |
| 335 | 78.5 | 13 | bess | PROCURING | Windmill Farm Solar Farm (Old Malton) | Harmony Energy | North Yorkshire | 2025-02-25 | 552 | 1.6km/132kV | `8347` | y |
| 336 | 78.3 | 73 | bess | FUNDING_WINDOW | Classic Marble Showers, Omagh Road - Battery Energy ... | Green Frog Power (Gort BESS) Limit... | Mid Ulster | 2026-06-19 | 73 | 39.3km/275kV | `16899` | y |
| 337 | 78.2 | 20 | bess | FUNDING_WINDOW | Dunside Wind Farm | EDF Energy | Scottish Government (S36) | 2026-03-24 | 160 | 4.9km/400kV | `10865` | y |
| 338 | 78.1 | 15 | bess | FUNDING_WINDOW | Nettly Burn Renewable Energy Park | Grupotec Solar UK 4 Ltd | Scottish Government (S36) | 2026-03-06 | 178 | 3.3km/132kV | `15538` | y |
| 339 | 78.1 | 70 | bess | PROCURING | Sandyforth Farm, Ashton Road - Battery Energy Storag... | UKGEA | Wigan | 2025-02-25 | 552 | 0.4km/132kV | `15930` | y |
| 340 | 78.1 | 25 | solar | PROCURING | St Ippolyts - Solar Farm & Battery Storage | Brockwell Storage & Solar Limited | North Hertfordshire | 2025-07-28 | 399 | 0.4km/400kV | `9694` | **n** |
| 341 | 78.0 | 41 | solar | PROCURING | Pitstock Farm - Solar Photovoltaic Panels | Voltalia UK Limited | Swale | 2025-10-03 | 332 | 3.8km/132kV | `15085` | y |
| 342 | 77.9 | 40 | solar | PROCURING | Vigo Lane, Borden - Solar Farm | Industria Solar Vigo (Industria Br... | Swale | 2025-09-01 | 364 | 0.4km/132kV | `10695` | y |
| 343 | 77.9 | 40 | solar | PROCURING | Colbrans Farm Estate, Laughton - Solar Panels | Innova | Wealden | 2025-07-21 | 406 | 1.8km/132kV | `11682` | y |
| 344 | 77.9 | 40 | solar | PROCURING | Craigluscar, Craigluscar Road - Solar Array & Batter... | Locogen Consulting Limited | Fife | 2025-07-03 | 424 | 1.2km/275kV | `13322` | y |
| 345 | 77.9 | 40 | bess | PROCURING | Glasgow Road, Eaglesham - Battery Storage Facility | GPC 1137 Limited (Apatura) | East Renfrewshire | 2025-04-15 | 503 | 0.1km/275kV | `15278` | **n** |
| 346 | 77.8 | 2 | solar | PROCURING | Roydsdale Way, Unit 6 - Solar Panel | BorgWarner | Bradford | 2026-03-02 | 182 | 0.3km/132kV | `20278` | y |
| 347 | 77.8 | 18 | bess | FUNDING_WINDOW | Earlsburn Avenue - Earlsburn Wind Farm Extension | Naturalis Energy / REG Wind Power ... | Scottish Government (S36) | 2025-12-16 | 258 | 3.6km/400kV | `11481` | y |
| 348 | 77.8 | 50 | solar | PROCURING | Carr Lane, Tickton - Solar Farm | Albanwise Synergy Limited | East Riding of Yorkshire | 2025-07-18 | 409 | 1.5km/132kV | `11743` | y |
| 349 | 77.7 | 38 | solar | PROCURING | Britton Court Farm, Hackington Road - Solar Farm | Renewable Connections Developments... | Canterbury | 2025-07-04 | 423 | 0.3km/400kV | `17454` | y |
| 350 | 77.6 | 10 | bess | PROCURING | Wissett Solar Farm, Wissett - Battery Storage (Apple... | Pathfinder Clean Energy UK Dev Lim... | East Suffolk | 2025-02-17 | 560 | 1.7km/132kV | `9912` | y |
| 351 | 77.6 | 10 | bess | PROCURING | Kings Dyke, Whittlesey - Battery Energy Storage | Power Initiatives Limited | Fenland | 2025-05-02 | 486 | 1.4km/132kV | `17656` | y |
| 352 | 77.4 | 35 | bess | PROCURING | Hill Court Solar farm & Battery storage | Longlands Solar Farm Limited | South Gloucestershire | 2025-05-29 | 459 | 0.2km/132kV | `8889` | y |
| 353 | 77.4 | 35 | solar | PROCURING | Quarry Solar Farm & Battery Storage Facility | RWE | West Oxfordshire | 2025-07-28 | 399 | 3.6km/132kV | `13491` | **n** |
| 354 | 77.2 | 20 | bess | PROCURING | Froghall Farm, Wyton Road - Solar Farm & Battery Ene... | GAM Capital Limited | East Riding of Yorkshire | 2024-11-11 | 658 | 0.7km/275kV | `13655` | y |
| 355 | 77.1 | 15 | solar | PROCURING | Little Rose Lane, Blunsdon - Solar Panels | Quintas Cleantech | Swindon | 2026-02-11 | 201 | 3.0km/132kV | `17362` | y |
| 356 | 76.9 | 24 | bess | FUNDING_WINDOW | Battery Energy Storage System in Newmills | Exergy Solutions Limited | Mid Ulster | 2025-07-09 | 418 | 5.5km/275kV | `16456` | y |
| 357 | 76.9 | 40 | bess | PROCURING | Kellwood Road - Battery Storage | Geocore Limited | Dumfries and Galloway | 2025-04-15 | 503 | 0.1km/132kV | `11545` | **n** |
| 358 | 76.9 | 40 | bess | PROCURING | Hull Road, Lund - Battery Energy Storage System | Ylem Energy Limited | North Yorkshire | 2025-01-21 | 587 | 1.3km/132kV | `16921` | y |
| 359 | 76.9 | 1 | solar | PROCURING | Tesco, Cygnet View - Solar PV Arrays | Tesco Plc | Thurrock | 2026-03-09 | 175 | 0.2km/400kV | `20282` | y |
| 360 | 76.9 | 1 | solar | PROCURING | Euroclad Group, Wentloog Road - Solar Panels | Euroclad Group Limited | Cardiff | 2026-03-06 | 178 | 0.4km/132kV | `20365` | y |
| 361 | 76.8 | 50 | bess | FUNDING_WINDOW | Omagh Road, Garvaghy - Battery Energy Storage | Heron Storage Limited | Mid Ulster | 2026-04-14 | 139 | 39.5km/275kV | `17663` | y |
| 362 | 76.8 | 50 | solar | PROCURING | Yew Tree Farm, Yew Tree Lane - Solar Farm | Yew Tree Farm Solar Limited | North Somerset | 2025-10-08 | 327 | 1.3km/400kV | `19452` | y |
| 363 | 76.8 | 30 | solar | PROCURING | Blacksmiths Lane, Middlewood Green - Solar Farm | Low Carbon Limited | Mid Suffolk | 2025-08-08 | 388 | 1.6km/400kV | `13530` | y |
| 364 | 76.8 | 30 | bess | PROCURING | Lower Farm, Drointon Lane - Solar farm & Battery Ene... | Innova Renewables | Stafford | 2025-01-14 | 594 | 0.7km/132kV | `13549` | y |
| 365 | 76.8 | 1 | solar | PROCURING | Dalmacoulter Landfill, Dalmacoulter Road - Solar Far... | North Lanarkshire Council | North Lanarkshire | 2026-04-22 | 131 | 0.2km/275kV | `19546` | y |
| 366 | 76.7 | 48 | bess | FUNDING_WINDOW | Battery Energy Storage System Facility Development i... | Green Frog Power (Tremoge) Limited | Mid Ulster | 2026-06-17 | 75 | 19.7km/275kV | `18550` | y |
| 367 | 76.5 | 342 | bess | PROCURING | Red Moss - Battery Storage | Green Switch Capital Limited | Scottish Government (S36) | 2025-06-19 | 438 | 1.1km/400kV | `15980` | y |
| 368 | 76.3 | 200 | bess | PROCURING | Carlisle Road - Battery Energy Storage System | Zenobe Energy | Scottish Government (S36) | 2025-04-28 | 490 | 2.8km/400kV | `9684` | y |
| 369 | 76.1 | 15 | bess | PROCURING | Ash Farm, Titchfield Lane - Battery Storage | Botley Energy Reserve 2 Limited | Winchester | 2025-02-19 | 558 | 0.2km/400kV | `14145` | y |
| 370 | 76.1 | 25 | bess | PROCURING | High Barnes Farm, Coal Lane - Battery Storage | Enviromena Project Management UK L... | Hartlepool | 2025-05-28 | 460 | 2.1km/275kV | `16081` | y |
| 371 | 76.0 | 500 | bess | PAST_EXPECTED_START | Eggborough Power Station, Selby Road - Battery Stora... | Eggborough Power Limited | North Yorkshire | 2023-01-17 | 1322 | 0.0km/400kV | `12483` | y |
| 372 | 75.9 | 40 | bess | PROCURING | Red Barn - Solar Farm & Battery Storage | Eden Renewables | Wiltshire | 2025-01-27 | 581 | 1.9km/400kV | `15145` | y |
| 373 | 75.8 | 6 | bess | PROCURING | Lister Battery Limited - Battery Energy Storage Syst... | Lister Battery Limited | Liverpool | 2025-04-23 | 495 | 0.2km/275kV | `17750` | y |
| 374 | 75.8 | 30 | solar | PROCURING | Beech Tree Solar Farm | Low Carbon UK Solar Investment Co ... | Wiltshire | 2025-07-30 | 397 | 0.7km/132kV | `13851` | y |
| 375 | 75.8 | 50 | bess | PROCURING | Templeton Farm, Templeton - Battery Storage | Fig Power | Angus | 2024-11-21 | 648 | 0.3km/132kV | `13605` | y |
| 376 | 75.6 | 28 | bess | FUNDING_WINDOW | Sandy Knowe Wind Farm Extension | Executive Resource Group | Scottish Government (S36) | 2025-08-26 | 370 | 6.0km/132kV | `12079` | y |
| 377 | 75.5 | 12 | bess | PROCURING | St Ippolyts - Solar Farm & Battery Storage | Brockwell Storage & Solar Limited | North Hertfordshire | 2025-07-28 | 399 | 0.4km/400kV | `9695` | **n** |
| 378 | 75.4 | 45 | solar | PROCURING | Manor Farm, Noke - Solar Farm | Green Nation | Cherwell | 2025-09-16 | 349 | 4.4km/132kV | `11556` | y |
| 379 | 75.4 | 45 | bess | PROCURING | The Smithy - Battery Storage | Renewable Energy Systems | Highland | 2025-01-29 | 579 | 0.1km/132kV | `14676` | y |
| 380 | 75.4 | 21 | solar | PROCURING | Frome Valley - Solar Farm | Anesco | Herefordshire, County of | 2025-07-07 | 420 | 1.8km/132kV | `16355` | y |
| 381 | 75.3 | 12 | bess | PROCURING | Stor Generation Plant - Battery Storage | Green Frog Power 214 Limited | Bradford | 2025-04-07 | 511 | 0.0km/132kV | `8998` | **n** |
| 382 | 75.2 | 20 | bess | PROCURING | Green Frog Power, Great Field Lane - Battery Energy ... | Pulse Clean Energy | Kingston upon Hull, City of | 2025-05-02 | 486 | 0.2km/132kV | `18684` | y |
| 383 | 75.1 | 90 | bess | PROCURING | North Side Bay Gateway, Heysham - Battery Energy Sto... | Cragside Energy Limited | Lancaster | 2025-07-24 | 403 | 2.1km/132kV | `16579` | y |
| 384 | 75.1 | 25 | bess | PROCURING | Battery Point, Newton Street - Battery Energy Storag... | Point & Sandwick Trust | Na h-Eileanan Siar | 2024-12-06 | 633 | 2.8km/132kV | `12460` | y |
| 385 | 74.9 | 40 | bess | PROCURING | Landown Farm, Bakeacre Lane - Battery Energy Storage... | Integrum Renewable Energy Limited | South Derbyshire | 2025-05-30 | 458 | 0.4km/132kV | `16308` | y |
| 386 | 74.8 | 1 | bess | FUNDING_WINDOW | Roxane UK, Armathwaite - Solar Array & Battery Stora... | Roxane UK Limited | Westmorland and Furness | 2026-03-17 | 167 | 0.8km/400kV | `16774` | y |
| 387 | 74.6 | 10 | bess | PROCURING | Marston Fields Farm, Kingsbury Road - Battery Energy... | PACE Wedge Energy Limited | North Warwickshire | 2025-06-17 | 440 | 0.4km/132kV | `17950` | y |
| 388 | 74.2 | 20 | bess | PROCURING | Plymouth Stor Generation - Battery storage | Pulse Clean Energy | Plymouth | 2025-03-26 | 523 | 0.0km/132kV | `10432` | **n** |
| 389 | 74.2 | 20 | bess | FUNDING_WINDOW | Fair Park Solar Farm | Downing Renewable Developments Llp | Cornwall | 2025-10-16 | 319 | 0.7km/132kV | `13760` | y |
| 390 | 74.2 | 26 | solar | PROCURING | Marshes Farm | One Planet | Maldon | 2025-09-10 | 355 | 5.3km/132kV | `17716` | y |
| 391 | 74.1 | 1 | solar | PROCURING | SNOP UK, Washington Road - Solar Panels | SNOP UK Limited | Sunderland | 2026-03-09 | 175 | 0.3km/275kV | `20296` | y |
| 392 | 74.0 | 1450 | bess | PAST_EXPECTED_START | Thorpe Marsh Power Station - Battery Energy Storage | West Burton Energy | Doncaster | 2025-01-28 | 580 | 0.2km/275kV | `12453` | **n** |
| 393 | 74.0 | 500 | bess | PROCURING | Redshaw Battery Energy Storage | BayWa r.e. UK Limited | Scottish Government (S36) | 2025-08-20 | 376 | 17.5km/132kV | `16473` | y |
| 394 | 74.0 | 300 | bess | PAST_EXPECTED_START | Carrog Ganol, Rhosgoch - Battery Energy Storage Syst... | Boom Developments Limited | Isle of Anglesey | 2024-09-26 | 704 | 0.2km/132kV | `13217` | y |
| 395 | 73.8 | 50 | bess | PROCURING | Tomchrasky Estate Wind farm | E Power Limited | Scottish Government (S36) | 2025-05-06 | 482 | 0.7km/132kV | `8364` | y |
| 396 | 73.8 | 50 | bess | PROCURING | Drumore Cottage, Swordale - Battery Storage | Fig Power | Highland | 2024-12-10 | 629 | 0.6km/275kV | `12983` | y |
| 397 | 73.8 | 50 | bess | PROCURING | Spittal Mains Quarry - Battery storage | Fig Power Limited | Highland | 2025-03-28 | 521 | 0.9km/132kV | `16163` | y |
| 398 | 73.8 | 30 | solar | PROCURING | Haigh Lane, Woolley Edge Lane - Solar Farm | Boom Developments Limited | Wakefield | 2025-08-07 | 389 | 3.4km/132kV | `14647` | y |
| 399 | 73.8 | 105 | bess | PROCURING | Kinmuck Battery Energy Storage | Kinmuck Energy Storage Limited / I... | Scottish Government (S36) | 2025-05-08 | 480 | 0.4km/275kV | `13001` | y |
| 400 | 73.4 | 7 | bess | PROCURING | Denfield - Battery Storage Facility | Peter J Stirling Limited | Angus | 2025-02-14 | 563 | 0.9km/132kV | `15198` | **n** |
| 401 | 73.3 | 20 | solar | FUNDING_WINDOW | Ferry Lane, Skellingthorpe - Solar Panels | PS Renewables Limited | North Kesteven | 2026-05-14 | 109 | 4.4km/400kV | `18918` | y |
| 402 | 73.2 | 5 | solar | PROCURING | Roxane UK, Armathwaite - Solar Array & Battery Stora... | Roxane UK Limited | Westmorland and Furness | 2026-03-17 | 167 | 0.8km/400kV | `16773` | y |
| 403 | 73.0 | 11 | bess | PROCURING | Enoch Hill, Dalmellington - Battery Storage | RWE Renewables Uk Limited | East Ayrshire | 2025-07-17 | 410 | 0.9km/132kV | `7769` | y |
| 404 | 72.9 | 24 | solar | PROCURING | Carr House Farm, East Heslerton - Solar Farm | Renewable Connections Developments... | North Yorkshire | 2025-06-05 | 452 | 0.7km/132kV | `16155` | y |
| 405 | 72.8 | 50 | bess | FUNDING_WINDOW | Clashindarroch Wind Farm Extension | Infinergy | Scottish Government (S36) | 2025-12-18 | 256 | 8.3km/275kV | `8004` | y |
| 406 | 72.8 | 50 | bess | PROCURING | Rookery Farm, Kimbolton Road - Battery Storage Facil... | Bluefield Renewable Developments L... | Huntingdonshire | 2025-07-25 | 402 | 1.8km/132kV | `15073` | y |
| 407 | 72.8 | 50 | bess | PROCURING | Camp Farm, Knowle Hill - Battery Storage | Ampyr Solar Europe | North Warwickshire | 2025-08-18 | 378 | 2.7km/132kV | `17961` | y |
| 408 | 72.8 | 50 | solar | PROCURING | Rookery Farm, Kimbolton Road - Solar Farm | Bluefield Renewable Developments L... | Huntingdonshire | 2025-07-25 | 402 | 1.8km/132kV | `15072` | y |
| 409 | 72.8 | 50 | solar | PROCURING | Stowey Road, Stowey - Solar Farm | Regener8 Power | Bath and North East Somerset | 2025-07-24 | 403 | 3.3km/132kV | `8323` | y |
| 410 | 72.8 | 50 | solar | PROCURING | Wandon End - Solar Farm & Battery Storage | EPL 002 Limited | North Hertfordshire | 2025-07-15 | 412 | 4.1km/132kV | `13056` | y |
| 411 | 72.8 | 50 | solar | PROCURING | Camp Farm, Knowle Hill - Solar Farm | Ampyr Solar Europe | North Warwickshire | 2025-08-18 | 378 | 2.7km/132kV | `17962` | y |
| 412 | 72.7 | 4 | solar | PROCURING | Sunbank Lane - Solar Panels | Igen Energy Limited | Manchester | 2026-04-17 | 136 | 3.3km/400kV | `20533` | y |
| 413 | 72.6 | 10 | solar | PROCURING | Snapewood Solar Farm | ABEI Energy | Wyre | 2026-03-05 | 179 | 1.6km/400kV | `15697` | y |
| 414 | 72.6 | 10 | bess | PROCURING | Craigluscar, Craigluscar Road - Solar Array & Batter... | Locogen Consulting Limited | Fife | 2025-07-03 | 424 | 1.1km/275kV | `13321` | y |
| 415 | 72.6 | 10 | bess | PROCURING | Elvanfoot, Leadhills Road - Battery Storage | Muirhall Energy Limited | South Lanarkshire | 2025-02-10 | 567 | 0.5km/400kV | `12900` | y |
| 416 | 72.6 | 100 | bess | PAST_EXPECTED_START | Walpole Sub Station, Walpole Bank - Battery Storage | Henry Energy Limited | King's Lynn and West Norfolk | 2023-07-04 | 1154 | 0.2km/132kV | `13045` | y |
| 417 | 72.4 | 2 | bess | PROCURING | Glyngwernen Farm, Uchaf Fawr - Battery Storage | Bartypower Limited | Carmarthenshire | 2025-02-17 | 560 | 1.1km/132kV | `16838` | y |
| 418 | 72.3 | 200 | bess | PAST_EXPECTED_START | Bolney - Battery Storage | Elements Green | Horsham | 2024-09-05 | 725 | 0.2km/132kV | `13880` | y |
| 419 | 72.2 | 20 | bess | PROCURING | Ardoch Farm | Capbal | North Ayrshire | 2025-03-19 | 530 | 0.2km/132kV | `7575` | **n** |
| 420 | 72.2 | 20 | bess | PROCURING | West Burton Solar Project | Island Green Power | The Planning Inspectorate - ... | 2025-01-24 | 584 | 1.4km/132kV | `10916` | y |
| 421 | 72.2 | 20 | solar | PROCURING | Lower House Farm, Lewth Lane - Solar Farm | Greentech | Wyre | 2025-11-12 | 292 | 2.2km/132kV | `17004` | y |
| 422 | 72.2 | 5 | bess | PROCURING | Suncoast Battery Storage | Low Carbon Solar Park 20 Limited | Eastbourne | 2025-02-19 | 558 | 0.8km/132kV | `14402` | y |
| 423 | 72.2 | 5 | bess | FUNDING_WINDOW | Ware Solar Park - Solar Farm & Battery Energy Storag... | The Farm Energy Company | East Hertfordshire | 2025-10-17 | 318 | 5.9km/132kV | `16729` | y |
| 424 | 72.1 | 400 | bess | PAST_EXPECTED_START | Low Harker Farm, Low Harker - Battery Storage Facili... | Zenobe Energy Limited | Cumberland | 2024-07-18 | 774 | 0.3km/275kV | `15956` | y |
| 425 | 72.0 | 2 | solar | PROCURING | Bayram Timber Limited, Gibson Lane South - Solar Pan... | Footprint Zero | East Riding of Yorkshire | 2026-04-08 | 145 | 4.9km/400kV | `20479` | y |
| 426 | 71.9 | 24 | solar | PROCURING | Ware Solar Park - Solar Farm & Battery Energy Storag... | The Farm Energy Company | East Hertfordshire | 2025-10-17 | 318 | 5.9km/132kV | `16728` | y |
| 427 | 71.9 | 39 | solar | PROCURING | Brompton Solar Farm - Solar Farm | Energyline Limited | North Yorkshire | 2025-08-21 | 375 | 3.2km/132kV | `16548` | y |
| 428 | 71.8 | 50 | solar | PROCURING | Fair Park Solar Farm | Downing Renewable Developments Llp | Cornwall | 2025-10-16 | 319 | 0.7km/132kV | `13761` | y |
| 429 | 71.7 | 38 | bess | PROCURING | Oaklands Solar Farm Project - Solar Farm & Battery S... | BayWa r.e. UK Limited | The Planning Inspectorate - ... | 2025-06-19 | 438 | 0.3km/400kV | `9546` | y |
| 430 | 71.6 | 350 | bess | PAST_EXPECTED_START | Pembroke Power Station, Pwllcrochan - Battery Storag... | RWE Generation UK Plc | Pembrokeshire | 2025-01-31 | 577 | 0.1km/132kV | `14913` | y |
| 431 | 71.6 | 350 | bess | PAST_EXPECTED_START | Goldborough Road, Hundleton - Battery Energy Storage | Pembroke Green Limited (Enso Energ... | Pembrokeshire | 2025-01-06 | 602 | 1.1km/132kV | `15277` | y |
| 432 | 71.5 | 2 | solar | FUNDING_WINDOW | Bartlett Business Park - Solar Panels | Indurent Management Limited | Fenland | 2026-05-05 | 118 | 10.9km/132kV | `20596` | y |
| 433 | 71.5 | 28 | solar | PROCURING | Crystal Rig Solar Farm | Fred Olsen Renewables | Scottish Government (S36) | 2025-07-30 | 397 | 0.4km/400kV | `4631` | y |
| 434 | 71.2 | 150 | bess | PAST_EXPECTED_START | Cholmondeley Road - Battery Storage | P3P Partners LLP | Halton | 2022-08-10 | 1482 | 0.2km/132kV | `9763` | y |
| 435 | 71.0 | 1400 | bess | PAST_EXPECTED_START | Thorpe Marsh Power Station, Marsh Lane - Battery Ene... | West Burton Energy / Banks Group | Doncaster | 2025-01-28 | 580 | 0.2km/275kV | `13644` | y |
| 436 | 71.0 | 1025 | bess | PAST_EXPECTED_START | The Balk, Almholme - Energy Storage System | Innova Renewables | Doncaster | 2024-10-14 | 686 | 0.9km/275kV | `14060` | y |
| 437 | 71.0 | 1000 | bess | PRE_CONSENT | Tesside GigaPark - Battery Energy Storage System | NatPower UK (NP SPV 27 Limited) | Redcar and Cleveland | - | - | 0.9km/400kV | `19634` | y |
| 438 | 71.0 | 500 | bess | CONSENTED_NO_DATE | East Claydon Battery Energy Storage | Statera Energy | Buckinghamshire | - | - | 0.2km/400kV | `15501` | y |
| 439 | 70.8 | 50 | bess | PROCURING | Loch Toftingall, Halsary Wind Farm - Battery Energy ... | Infinergy Limited / Boralex | Highland | 2024-11-12 | 657 | 3.8km/132kV | `13949` | y |
| 440 | 70.5 | 60 | bess | PAST_EXPECTED_START | Redcote Lane, Armley - Battery Storage Facility | Cambridge Power Limited | Leeds | 2023-05-18 | 1201 | 0.2km/132kV | `12224` | y |
| 441 | 70.4 | 264 | bess | PAST_EXPECTED_START | Bolney Substation - Battery Storage | One Planet Developments Limited | Mid Sussex | 2024-10-18 | 682 | 0.1km/132kV | `8986` | **n** |
| 442 | 70.2 | 250 | bess | PAST_EXPECTED_START | Toddington Services, Hipsey Spinney - Battery Storag... | Kona Energy Limited | Central Bedfordshire | 2025-01-06 | 602 | 0.3km/132kV | `15573` | **n** |
| 443 | 70.2 | 249 | bess | PAST_EXPECTED_START | Ridham Avenue, Swale Way - Kemsley Battery Energy St... | Ouse Energy Limited | Swale | 2024-09-17 | 713 | 0.3km/400kV | `15779` | y |
| 444 | 70.1 | 41 | bess | PROCURING | Ladyfield Renewable Energy Park | Ridge Clean Energy Limited | Scottish Government (S36) | 2025-05-02 | 486 | 0.1km/132kV | `15785` | y |
| 445 | 70.0 | 500 | bess | PAST_EXPECTED_START | West Burton Power Station, North Road - Battery Stor... | Fidra Energy / Drax | Bassetlaw | 2024-09-05 | 725 | 0.3km/400kV | `11928` | y |
| 446 | 69.9 | 228 | bess | PAST_EXPECTED_START | Smeaton Battery Energy Storage System | Kona Energy | Scottish Government (S36) | 2024-08-29 | 732 | 0.3km/275kV | `13627` | y |
| 447 | 69.8 | 50 | bess | PROCURING | Battery Energy Storage System Facility in Antrim | Heron Storage Limited | Antrim and Newtownabbey | 2025-03-21 | 528 | 10.1km/275kV | `16592` | y |
| 448 | 69.8 | 30 | bess | PROCURING | Rushett Lane - Battery Storage System | Enso Energy | Epsom and Ewell | 2025-04-03 | 515 | 6.0km/275kV | `15398` | y |
| 449 | 69.8 | 50 | solar | PAST_EXPECTED_START | Yanel Farm, Churchill Green - Solar Farm | Capital Dynamics Limited | North Somerset | 2024-04-18 | 865 | 0.6km/132kV | `11783` | y |
| 450 | 69.6 | 450 | bess | PAST_EXPECTED_START | Gateway Energy Centre - Battery Energy Storage | Intergen Limited | Thurrock | 2023-01-13 | 1326 | 0.8km/400kV | `10309` | y |
| 451 | 69.6 | 100 | bess | PAST_EXPECTED_START | Walpole Sub Station, Walpole Bank - Battery Storage | Henry Energy Limited | King's Lynn and West Norfolk | 2023-07-04 | 1154 | 0.3km/132kV | `12683` | y |
| 452 | 69.5 | 36 | solar | PROCURING | Little Drum Solar Farm - Solar Park & Battery Storag... | Grupotec Solar UK 5 Limited | Dumfries and Galloway | 2025-07-28 | 399 | 3.5km/132kV | `16847` | y |
| 453 | 69.4 | 2 | solar | FUNDING_WINDOW | Solar PV Energy Development in Newry | HHT Management Limited | Newry, Mourne and Down | 2026-05-14 | 109 | 9.2km/275kV | `16583` | y |
| 454 | 69.3 | 200 | bess | PAST_EXPECTED_START | Bryntywod, Llangyfelach - Battery Energy Storage Sys... | FRV TH Powertek Limited | Swansea | 2025-02-06 | 571 | 0.2km/132kV | `16050` | y |
| 455 | 69.1 | 42 | bess | PAST_EXPECTED_START | South Pargillis - Battery Storage | Infinis Energy Services Limited | Fife | 2023-06-09 | 1179 | 0.3km/132kV | `9564` | y |
| 456 | 69.1 | 400 | bess | PAST_EXPECTED_START | Cellarhead Substation, Rownall Road - Battery Energy... | C&S Energy Limited | Staffordshire Moorlands | 2022-12-22 | 1348 | 0.2km/400kV | `10013` | **n** |
| 457 | 69.1 | 400 | bess | PAST_EXPECTED_START | East Chickerell Court Farm - Battery Energy Storage ... | Statera Energy | Dorset | 2025-01-27 | 581 | 0.3km/400kV | `12651` | y |
| 458 | 69.1 | 400 | bess | PAST_EXPECTED_START | Bicker Fen Bess, Vicarage Drove - Battery Storage | FRV TH Powertek Limited | Boston | 2025-02-05 | 572 | 0.8km/400kV | `16628` | y |
| 459 | 68.6 | 22 | bess | PROCURING | Surmer Hall, Church Walk - Solar Farm & Battery Stor... | Boultbee Brooks (Renewables Rowley... | Braintree | 2024-12-04 | 635 | 5.6km/400kV | `15400` | y |
| 460 | 68.6 | 350 | solar | PAST_EXPECTED_START | Mallard Pass Solar Farm | Canadian Solar UK (Recurrent Energ... | The Planning Inspectorate - ... | 2024-07-12 | 780 | 0.4km/400kV | `9904` | y |
| 461 | 68.6 | 100 | bess | PROCURING | Murton Way - Battery Energy Storage | First Way Solar Limited | York | 2025-07-17 | 410 | 5.8km/400kV | `14759` | **n** |
| 462 | 68.4 | 35 | solar | PROCURING | Brownside Farm - Electricity Production Facility & B... | Aberdeenshire Council | Aberdeenshire | 2025-06-18 | 439 | 8.1km/132kV | `17758` | y |
| 463 | 68.3 | 72 | solar | PAST_EXPECTED_START | Lower Bodachra - Solar Panels | Novus Renewables Services Limited | Scottish Government (S36) | 2025-06-24 | 433 | 0.1km/132kV | `14302` | y |
| 464 | 68.2 | 20 | solar | PROCURING | Moreton Morrell - Solar PV | Innova Renewables Limited | Stratford-on-Avon | 2025-07-17 | 410 | 6.1km/132kV | `16517` | y |
| 465 | 68.2 | 249 | bess | PRE_CONSENT | Aberthaw Battery Energy Storage System | Aberthaw Energy Limited | Vale of Glamorgan | - | - | 0.8km/275kV | `20451` | y |
| 466 | 68.2 | 150 | bess | PAST_EXPECTED_START | Neilston - Battery Storage | Apatura (GPC 1119 Ltd) | Scottish Government (S36) | 2025-02-04 | 573 | 0.3km/400kV | `14538` | y |
| 467 | 68.0 | 1000 | bess | PRE_CONSENT | Swinford Energy Park - Energy Park Facility & Batter... | NatPower UK | Harborough | - | - | 0.4km/400kV | `19534` | y |
| 468 | 68.0 | 900 | bess | PAST_EXPECTED_START | Haughend Farm - Alyth Battery Energy Storage System | EcoDev Group Limited | Scottish Government (S36) | 2024-11-26 | 643 | 0.2km/275kV | `11858` | y |
| 469 | 68.0 | 750 | solar | PRE_CONSENT | Whitestone Solar Farm | Net Zero One Ltd | The Planning Inspectorate - ... | - | - | 0.6km/132kV | `17700` | y |
| 470 | 68.0 | 700 | bess | PAST_EXPECTED_START | Auchentiber Road - Battery Energy Storage System | Apatura GPC 700 Limited | Scottish Government (S36) | 2024-09-11 | 719 | 0.6km/400kV | `15425` | y |
| 471 | 68.0 | 502 | bess | PRE_CONSENT | High Netherfauld House Farm 1, Tower Road - Battery ... | ESB (Harker) Limited | Scottish Government (S36) | - | - | 1.8km/400kV | `18157` | y |
| 472 | 68.0 | 500 | bess | PAST_EXPECTED_START | Normanton Energy Reserve - Battery Storage | Exagen SPVO2 Limited | Blaby | 2024-01-16 | 958 | 1.5km/400kV | `11988` | y |
| 473 | 68.0 | 500 | bess | PRE_CONSENT | Braybrooke Battery Energy Storage System | Aura Power Developments Limited | North Northamptonshire | - | - | 0.3km/400kV | `19671` | y |
| 474 | 68.0 | 300 | bess | PAST_EXPECTED_START | Newarthill Energy Park | Geocore Limited | Scottish Government (S36) | 2025-02-04 | 573 | 0.2km/275kV | `14763` | y |
| 475 | 67.8 | 30 | bess | PAST_EXPECTED_START | Upper Newton Farm (Blythe House) - Solar Farm & Batt... | Innova Renewables | Staffordshire Moorlands | 2023-02-01 | 1307 | 0.2km/132kV | `10978` | y |
| 476 | 67.6 | 130 | bess | PAST_EXPECTED_START | Southfields Farm, Common Lane - Battery Storage | Toton Battery Storage Limited | Broxtowe | 2024-08-21 | 740 | 1.5km/132kV | `12698` | y |
| 477 | 67.5 | 60 | bess | PAST_EXPECTED_START | Misslebrook Farm, Botley Road - Battery Storage | Boom Developments Limited | Test Valley | 2024-04-05 | 878 | 0.7km/400kV | `12691` | y |
| 478 | 67.5 | 28 | solar | PAST_EXPECTED_START | Upper Newton Farm (Blythe House) - Solar Farm & Batt... | Innova Renewables | Staffordshire Moorlands | 2023-02-01 | 1307 | 0.2km/132kV | `10977` | y |
| 479 | 67.3 | 200 | bess | PRE_CONSENT | Low Moor Lane, Scotton - Battery Energy Storage Syst... | Harmony Energy Limited | North Yorkshire | - | - | 0.9km/132kV | `18049` | y |
| 480 | 67.3 | 120 | bess | PAST_EXPECTED_START | Kemsley Energy Park Battery Storage | FPC Electric Land limited | Swale | 2024-09-30 | 700 | 0.2km/400kV | `13489` | y |
| 481 | 67.3 | 56 | solar | PAST_EXPECTED_START | Berden Hall Solar Farm | British Solar Renewables | Uttlesford | 2024-07-18 | 774 | 0.2km/400kV | `20388` | y |
| 482 | 67.1 | 400 | bess | PRE_CONSENT | East Fulwood Energy Storage | Lightsourcebp | Scottish Government (S36) | - | - | 0.3km/400kV | `19578` | y |
| 483 | 67.1 | 25 | solar | PAST_EXPECTED_START | Manor Farm, Beachampton - Solar Farm | Anesco Limited | Buckinghamshire | 2024-01-12 | 962 | 0.9km/132kV | `11778` | y |
| 484 | 67.1 | 25 | solar | PROCURING | Home Farm | Canadian Solar / Novergy | Tewkesbury | 2025-06-16 | 441 | 6.2km/132kV | `14336` | y |
| 485 | 67.1 | 240 | bess | PAST_EXPECTED_START | Springfield Farm, Hensall - Battery Energy Storage F... | Newton Energi Limited | North Yorkshire | 2024-05-08 | 845 | 1.5km/400kV | `11680` | y |
| 486 | 67.0 | 940 | bess | PAST_EXPECTED_START | Fanny House Farm, Bay Gateway - Battery Storage | Innova Renewables | Lancaster | 2023-11-28 | 1007 | 0.9km/132kV | `14386` | y |
| 487 | 67.0 | 680 | bess | DESIGN_FROZEN_OR_LATER | Carrington Power Station, Manchester Road - Battery ... | Statera Energy | Trafford | 2023-07-20 | - | 0.1km/275kV | `13362` | y |
| 488 | 66.8 | 50 | bess | PAST_EXPECTED_START | Third Drove, Fengate - Battery Storage | Flag Fen Power Limited | Peterborough | 2023-01-05 | 1334 | 0.1km/132kV | `11558` | y |
| 489 | 66.8 | 50 | solar | PAST_EXPECTED_START | Broadway House Farm Solar Farm | Bluefield Renewable Developments L... | Northumberland | 2023-11-08 | 1027 | 1.3km/275kV | `8351` | y |
| 490 | 66.8 | 50 | solar | PAST_EXPECTED_START | Osgodby Grange, Osgodby - Solar Energy | Enray Power Limited | North Yorkshire | 2022-07-15 | 1508 | 1.6km/132kV | `9075` | y |
| 491 | 66.8 | 50 | bess | PROCURING | Lochluichart - Energy Storage Facility | Intelligent Land Investments Group | Highland | 2024-11-07 | 662 | 6.8km/132kV | `9220` | y |
| 492 | 66.8 | 50 | solar | PAST_EXPECTED_START | Church Farm, Kingston On Soar - Solar Photovoltaic F... | Renewable Connections Developments... | Rushcliffe | 2022-12-21 | 1349 | 0.7km/132kV | `9324` | y |
| 493 | 66.8 | 50 | bess | PAST_EXPECTED_START | Persley Croft - Battery Storage | RE Projects Development | Aberdeen City | 2024-08-29 | 732 | 0.9km/275kV | `13684` | y |
| 494 | 66.8 | 50 | solar | PAST_EXPECTED_START | Foxwalks Farm, Grafton Lane - Solar Farm | Spring Dev 10 Limited | Bromsgrove | 2024-07-18 | 774 | 0.4km/400kV | `14914` | y |
| 495 | 66.8 | 30 | solar | PROCURING | Solar Farm Development in Magheralin | Renewable Energy Systems RES ltd (... | Armagh City, Banbridge and C... | 2025-07-21 | 406 | 5.2km/275kV | `16337` | y |
| 496 | 66.7 | 4 | bess | FUNDING_WINDOW | Scottow Solar Farm - Battery Storage | Connected Energy Limited | North Norfolk | 2025-11-06 | 298 | 13.0km/132kV | `19344` | y |
| 497 | 66.6 | 100 | bess | PAST_EXPECTED_START | Libra Energy Stability Project - Battery Energy Stor... | Lightrock Power | Mid Sussex | 2025-01-31 | 577 | 0.2km/132kV | `12443` | y |
| 498 | 66.6 | 100 | bess | PAST_EXPECTED_START | Newburn Bridge Road - Battery Storage Facility | The Renewables Infrastructure Grou... | Gateshead | 2022-03-31 | 1614 | 0.2km/275kV | `12729` | y |
| 499 | 66.6 | 100 | solar | PAST_EXPECTED_START | Stonestreet Green - Solar Farm & Battery Storage | Evolution Power | The Planning Inspectorate - ... | 2025-10-23 | 312 | 1.4km/400kV | `10086` | y |
| 500 | 66.5 | 99 | bess | PAST_EXPECTED_START | Butts Field, Mill Lane - Battery Storage | Ecotricity Generation Limited | Southampton | 2024-10-03 | 697 | 1.6km/132kV | `7399` | **n** |
| 501 | 66.5 | 99 | bess | PAST_EXPECTED_START | Iron Acton Substation, Latteridge Lane - Battery Ene... | Balance Power Projects Limited | South Gloucestershire | 2024-08-16 | 745 | 0.2km/132kV | `14722` | y |
| 502 | 66.4 | 35 | bess | FUNDING_WINDOW | Mynydd Maen Solar Farm (Cil-Lonydd) | Cenin Renewables Limited | Welsh Government (NSIP) | 2025-11-12 | 292 | n/a | `17724` | y |
| 503 | 66.4 | 16 | bess | PROCURING | Knockkippen Wind, Solar & Battery Farm | Falck Renewables / REG Windpower | Scottish Government (S36) | 2025-04-30 | 488 | 1.9km/132kV | `10468` | y |
| 504 | 66.3 | 200 | bess | PAST_EXPECTED_START | Whitehill Energy Storage | Intelligent Land Investments Group | Scottish Government (S36) | 2024-10-28 | 672 | 1.0km/275kV | `10466` | y |
| 505 | 66.1 | 400 | bess | PAST_EXPECTED_START | Hunterston Grid Services Complex - Energy Storage Fa... | Amp Energy | Scottish Government (S36) | 2022-01-05 | 1699 | 0.5km/400kV | `10535` | y |
| 506 | 66.1 | 400 | bess | PAST_EXPECTED_START | Kincardine Grid Services Complex - Energy Storage Fa... | Amp Energy | Scottish Government (S36) | 2022-01-05 | 1699 | 0.1km/275kV | `10536` | y |
| 507 | 66.1 | 400 | bess | PAST_EXPECTED_START | Junction 27, Westleigh - Battery Storage | Clearstone Energy | Mid Devon | 2024-04-12 | 871 | 1.1km/400kV | `14935` | y |
| 508 | 66.0 | 500 | solar | PAST_EXPECTED_START | Tillbridge Solar Farm, Hemswell - Solar Panels | Tillbridge Solar Limited | The Planning Inspectorate - ... | 2025-10-14 | 321 | 7.8km/132kV | `12282` | y |
| 509 | 66.0 | 500 | solar | PRE_CONSENT | Light Valley Solar, Selby Road - Solar Farm | Light Valley Solar Limited ( Islan... | The Planning Inspectorate - ... | - | - | 0.8km/132kV | `17702` | y |
| 510 | 65.9 | 40 | solar | PAST_EXPECTED_START | Brogborough Landfill, Lidlington - Solar PV park | Infinis Solar Developments Limited | Central Bedfordshire | 2024-04-23 | 860 | 1.6km/132kV | `11005` | y |
| 511 | 65.9 | 40 | bess | PROCURING | Doogary Road, Omagh - Battery Storage | Omagh BES Limited | Fermanagh and Omagh | 2024-12-13 | 626 | 38.2km/275kV | `14125` | y |
| 512 | 65.8 | 39 | solar | PAST_EXPECTED_START | Sweet Briar Farm - Solar Farm | Lightrock Power | North Lincolnshire | 2024-02-09 | 934 | 0.3km/400kV | `9832` | y |
| 513 | 65.7 | 80 | bess | PAST_EXPECTED_START | Midland Road - Battery Energy Storage | Unknown | Bradford | 2024-12-20 | 619 | 0.3km/132kV | `15911` | y |
| 514 | 65.6 | 37 | solar | PAST_EXPECTED_START | Hill Farm Solar Park & Battery Storage (Hanningfield... | Gulermak Renewables Ltd | Chelmsford | 2022-07-07 | 1516 | 0.9km/400kV | `8911` | y |
| 515 | 65.6 | 349 | bess | PAST_EXPECTED_START | Penrhos Works - Battery Energy Storage System | Anglesey Land Holdings Limited | Isle of Anglesey | 2024-01-24 | 950 | 0.1km/132kV | `15472` | y |
| 516 | 65.5 | 16 | solar | PAST_EXPECTED_START | Gwenlais Farm, Carmel Road - Gwenlais Solar Farm | Solar Securities Group Limited | Swansea | 2025-06-11 | 446 | 1.5km/132kV | `18488` | y |
| 517 | 65.4 | 75 | bess | PAST_EXPECTED_START | Belasis Avenue - Battery Storage | Story Construction Limited | Stockton-on-Tees | 2024-04-19 | 864 | 1.3km/132kV | `13850` | y |
| 518 | 65.4 | 35 | solar | PAST_EXPECTED_START | Parley Court - Solar Farm | Enviromena Asset Management UK Lim... | Bournemouth, Christchurch an... | 2024-06-18 | 804 | 0.4km/132kV | `10041` | y |
| 519 | 65.3 | 12 | bess | PROCURING | Little Drum Solar Farm - Solar Park & Battery Storag... | Grupotec Solar UK 5 Limited | Dumfries and Galloway | 2025-07-28 | 399 | 4.3km/132kV | `16846` | y |
| 520 | 65.3 | 252 | bess | PRE_CONSENT | Braybrooke Village North, Harborough Road - Battery ... | Elmya Energy Limited | North Northamptonshire | - | - | 0.6km/400kV | `18956` | y |
| 521 | 65.2 | 20 | solar | PROCURING | Clay Lane, St Osyth - Solar Farm | Lighthouse Development Consulting ... | Tendring | 2025-11-27 | 277 | 6.4km/132kV | `18976` | y |
| 522 | 65.2 | 150 | bess | PAST_EXPECTED_START | Printworks Road - Stalybridge Battery Storage | Zenobe Energy | Tameside | 2023-12-15 | 990 | 0.1km/132kV | `10808` | y |
| 523 | 65.2 | 150 | bess | PAST_EXPECTED_START | Norrington Gate Farm, Broughton Gifford - Battery En... | ADV 003 Limited | Wiltshire | 2023-01-06 | 1333 | 0.5km/400kV | `11612` | y |
| 524 | 65.2 | 150 | bess | PAST_EXPECTED_START | Wilton International, Greystones Road - Phase 1 | Sembcorp Utilities (UK) Limited | Redcar and Cleveland | 2023-10-04 | 1062 | 0.1km/275kV | `14729` | y |
| 525 | 65.1 | 15 | bess | PROCURING | Brownside Farm - Electricity Production Facility & B... | Aberdeenshire Council | Aberdeenshire | 2025-06-18 | 439 | 8.1km/132kV | `17759` | y |
| 526 | 65.0 | 500 | bess | PRE_CONSENT | East Claydon Substation, East Claydon Road - Energy ... | Statkraft UK Limited | Buckinghamshire | - | - | 0.1km/132kV | `18957` | y |
| 527 | 64.9 | 2 | bess | PROCURING | Uphouse Farm - Sandpits Solar Farm & Battery Energy ... | Uphouse Farms Limited | North Norfolk | 2025-06-16 | 441 | 1.6km/132kV | `18192` | y |
| 528 | 64.8 | 480 | solar | PAST_EXPECTED_START | West Burton Solar Project | Island Green Power | The Planning Inspectorate - ... | 2025-01-24 | 584 | 1.4km/132kV | `10917` | y |
| 529 | 64.8 | 290 | bess | PAST_EXPECTED_START | Saundercroft Farm - Battery Energy Storage System | Exeter Storage Limited (Statera En... | East Devon | 2024-01-12 | 962 | 0.3km/132kV | `13980` | y |
| 530 | 64.8 | 30 | solar | PAST_EXPECTED_START | Brinsea Green Farm, Brinsea Lane - Solar Photovoltai... | RWE Renewables UK | North Somerset | 2025-02-28 | 549 | 0.2km/132kV | `14330` | y |
| 531 | 64.8 | 50 | bess | PAST_EXPECTED_START | Fair Oaks Renewable Energy Park - Solar farm & Batte... | Ridge Clean Energy Limited / L&G N... | Rushcliffe | 2023-10-02 | 1064 | 0.7km/400kV | `9795` | y |
| 532 | 64.8 | 50 | solar | PAST_EXPECTED_START | Fair Oaks Renewable Energy Park - Solar farm & Batte... | Ridge Clean Energy Limited / L&G N... | Rushcliffe | 2023-10-02 | 1064 | 0.7km/400kV | `9796` | y |
| 533 | 64.8 | 50 | solar | PAST_EXPECTED_START | Preston Hill Farm, Penkridge - Solar Farm | Engena Limited | South Staffordshire | 2024-02-02 | 941 | 0.7km/132kV | `10779` | y |
| 534 | 64.7 | 49 | bess | PAST_EXPECTED_START | Broomhill BESS - Battery Energy Storage | Gigabox Energy Storage Limited | Aberdeenshire | 2022-07-01 | 1522 | 0.5km/132kV | `10701` | y |
| 535 | 64.6 | 61 | bess | PAST_EXPECTED_START | Saturland Farm, Salterland Road - Battery Energy Sto... | Resources Unlimited LLP | Scottish Government (S36) | 2024-12-19 | 620 | 0.4km/132kV | `12024` | y |
| 536 | 64.6 | 450 | solar | PRE_CONSENT | Steeple Renewables Project | Renewable Energy Systems RES Limit... | The Planning Inspectorate - ... | - | - | 0.3km/400kV | `15253` | y |
| 537 | 64.6 | 450 | bess | PRE_CONSENT | Brockleaze, Neston Park Estate - Battery Energy Stor... | Grenergy Renewables UK Limited | Wiltshire | - | - | 0.4km/275kV | `18670` | y |
| 538 | 64.5 | 60 | bess | PAST_EXPECTED_START | West Boldon Substation - Battery Energy Storage | Whirlwind Energy Storage Limited | South Tyneside | 2024-12-10 | 629 | 0.2km/275kV | `14408` | y |
| 539 | 64.5 | 98 | solar | PRE_CONSENT | Hedgehog Grove Solar Farm - Solar Panels | Totalenergies Renewables Uk Limite... | The Planning Inspectorate - ... | - | - | 1.5km/132kV | `18870` | y |
| 540 | 64.4 | 46 | solar | PAST_EXPECTED_START | Snakes Meadow - Solar Farm | Renewable Connections Developments... | Bedford | 2024-05-08 | 845 | 0.2km/400kV | `9820` | y |
| 541 | 64.3 | 57 | bess | PAST_EXPECTED_START | Beechwood Farm, Hodgetts Lane - Battery Storage | Enso Energy Limited | Solihull | 2025-01-09 | 599 | 0.4km/275kV | `13297` | y |
| 542 | 64.3 | 200 | bess | PRE_CONSENT | Clay Tye Farm - Energy Storage Facility | London & Essex Energy Limited | Havering | - | - | 0.2km/132kV | `15607` | y |
| 543 | 64.3 | 200 | bess | PAST_EXPECTED_START | T Main Road, Ansty - Battery Energy Storage System | FRV Tyler Hill BESS 1 Ltd | Rugby | 2024-09-12 | 718 | 0.7km/132kV | `16212` | y |
| 544 | 64.3 | 26 | bess | PAST_EXPECTED_START | West Melton Electricity Substation - Energy Storage ... | Brampton Energy Storage Limited | Rotherham | 2022-09-13 | 1448 | 0.1km/132kV | `11436` | y |
| 545 | 64.1 | 190 | solar | PAST_EXPECTED_START | Helios Renewable Energy Project | Enso Green Holdings D Limited | The Planning Inspectorate - ... | 2025-12-03 | 271 | 1.7km/400kV | `11477` | y |
| 546 | 64.1 | 400 | bess | PAST_EXPECTED_START | Blackdyke Farm, Blackford - Battery Storage | Innova Renewables | Cumberland | 2023-10-05 | 1061 | 0.5km/132kV | `15005` | y |
| 547 | 64.1 | 400 | bess | PRE_CONSENT | Mulbarton Road, Keswick - Battery Energy Storage Sys... | Greenfield Energy Developments Lim... | South Norfolk | - | - | 1.2km/132kV | `19491` | y |
| 548 | 64.1 | 400 | bess | PRE_CONSENT | Wheaten Hill Farm - BESS | Boom Power Limited | Redditch | - | - | 0.6km/275kV | `19649` | y |
| 549 | 64.0 | 550 | bess | PAST_EXPECTED_START | Spalding Energy Park - Battery Storage | Intergen Limited | South Holland | 2023-06-14 | 1174 | 0.2km/400kV | `10173` | y |
| 550 | 64.0 | 500 | bess | DESIGN_FROZEN_OR_LATER | Eccles II Substation - Battery Energy Storage System | Matrix Renewables | Scottish Government (S36) | 2024-12-16 | - | 0.2km/400kV | `14058` | y |
| 551 | 63.9 | 180 | bess | PAST_EXPECTED_START | Fordtead Lane, Thorpe Marsh - Battery Energy Facilit... | Newton Energi Limited | Doncaster | 2024-04-30 | 853 | 0.7km/275kV | `14932` | y |
| 552 | 63.8 | 50 | bess | PROCURING | Ourack | Vattenfall | Scottish Government (S36) | 2025-03-25 | 524 | 7.2km/275kV | `5949` | y |
| 553 | 63.8 | 50 | bess | PAST_EXPECTED_START | Upton Lane, Nursling - Battery Storage Facility | Unknown | Test Valley | 2022-01-28 | 1676 | 0.1km/132kV | `9673` | y |
| 554 | 63.8 | 50 | bess | PAST_EXPECTED_START | Upper Latherford Farm, Latherford Lane - Battery Ene... | Net Zero Twelve Limited | South Staffordshire | 2024-10-16 | 684 | 0.2km/275kV | `15446` | y |
| 555 | 63.8 | 50 | solar | PAST_EXPECTED_START | California Farm - Solar Farm & Battery Storage | Infinis Solar Developments Limited | Stockton-on-Tees | 2023-03-15 | 1265 | 0.2km/132kV | `9117` | y |
| 556 | 63.8 | 50 | solar | PAST_EXPECTED_START | Lady Ings Farm, Middlestown - Solar Photovoltaic Far... | Boom Developments Limited | Wakefield | 2022-11-14 | 1386 | 0.1km/132kV | `10199` | y |
| 557 | 63.8 | 50 | bess | PAST_EXPECTED_START | Lowfields Energy Storage Project | UK Battery Storage | Calderdale | 2023-03-03 | 1277 | 0.1km/275kV | `10236` | **n** |
| 558 | 63.8 | 50 | solar | PAST_EXPECTED_START | Woodlands Farm - Solar Array | Elgin Energy EsCo Limited | Breckland | 2025-01-07 | 601 | 3.2km/132kV | `10969` | y |
| 559 | 63.8 | 50 | solar | PAST_EXPECTED_START | North Cote Farm & Park Farm, Dunsdale - Solar Arrays | Elgin Energy | Redcar and Cleveland | 2022-12-23 | 1347 | 4.7km/400kV | `11983` | y |
| 560 | 63.8 | 50 | bess | PAST_EXPECTED_START | Dunmill, Substation Dun - Battery Energy Storage | Renewable Energy Systems Limited | Angus | 2024-08-14 | 747 | 0.0km/132kV | `15233` | y |
| 561 | 63.8 | 368 | bess | PRE_CONSENT | Lower Dunton Road - Battery Energy Storage System | LJ Construction UK Limited | Basildon | - | - | 0.2km/132kV | `12458` | y |
| 562 | 63.7 | 49 | solar | PAST_EXPECTED_START | Common Farm - Solar Farm & Battery Storage | Banks Renewable | Rotherham | 2023-06-13 | 1175 | 0.6km/132kV | `9788` | y |
| 563 | 63.6 | 100 | bess | PAST_EXPECTED_START | North Walpole, St Peter - Battery Energy Storage | Roc Noir Limited | King's Lynn and West Norfolk | 2022-06-10 | 1543 | 0.1km/132kV | `9762` | y |
| 564 | 63.6 | 100 | bess | PAST_EXPECTED_START | Penn Croft Farm, Crondall - Battery Energy Storage F... | Fleet BESS Limited & SSE Energy So... | Hart | 2023-01-30 | 1309 | 0.7km/132kV | `10163` | y |
| 565 | 63.6 | 100 | bess | PAST_EXPECTED_START | Walpole St Andrew - Battery storage | Alfred Energy Limited | King's Lynn and West Norfolk | 2022-09-20 | 1441 | 0.1km/132kV | `10876` | y |
| 566 | 63.6 | 100 | bess | PAST_EXPECTED_START | Bradford West, Harrop Lane, Wilsden - Battery Storag... | 24 Power Limited | Bradford | 2023-05-15 | 1204 | 0.1km/400kV | `12909` | y |
| 567 | 63.6 | 100 | bess | PAST_EXPECTED_START | Bicker Drove - Battery Energy Storage System | Net Zero Twenty Two Limited | Boston | 2025-02-05 | 572 | 0.5km/132kV | `17344` | y |
| 568 | 63.6 | 165 | bess | PRE_CONSENT | Perimeter Road, Kirkby - Battery Energy Storage | Unknown | Knowsley | - | - | 0.3km/132kV | `15191` | y |
| 569 | 63.6 | 100 | bess | PAST_EXPECTED_START | South Thinford Lane, Thinford - Energy Storage | Renewable Energy Systems Limited | County Durham | 2022-10-21 | 1410 | 0.1km/400kV | `10489` | y |
| 570 | 63.6 | 100 | bess | PAST_EXPECTED_START | Linton Court Farm, Highnam - Battery storage | STOR 136 Limited | Tewkesbury | 2023-08-21 | 1106 | 0.9km/132kV | `13145` | y |
| 571 | 63.6 | 100 | bess | PAST_EXPECTED_START | Lower Larks Farm - Battery storage | IPP Cero Generation | South Gloucestershire | 2023-04-14 | 1235 | 0.0km/275kV | `14076` | y |
| 572 | 63.6 | 100 | bess | PAST_EXPECTED_START | Illeybrook Farm - Battery Energy Storage | Net Zero Eleven Limited | Dudley | 2025-02-04 | 573 | 1.1km/132kV | `14064` | y |
| 573 | 63.5 | 99 | bess | PAST_EXPECTED_START | Skelton Grange Battery Storage Facility | Catalyst Capital LLP | Leeds | 2021-08-04 | 1853 | 0.1km/132kV | `8914` | y |
| 574 | 63.4 | 75 | solar | PAST_EXPECTED_START | Fernishaw Solar Farm & Battery Energy Storage Facili... | Elgin Energy (EEB67) | Scottish Government (S36) | 2025-07-23 | 404 | 0.7km/275kV | `14541` | y |
| 575 | 63.3 | 200 | bess | PAST_EXPECTED_START | Heysham Energy Storage Project | Kona Energy Limited | Lancaster | 2022-05-23 | 1561 | 0.1km/400kV | `9545` | y |
| 576 | 63.3 | 200 | bess | DESIGN_FROZEN_OR_LATER | Windyhill Battery Storage Facility | Energy GridPower Ltd / Revera Ener... | Scottish Government (S36) | 2022-06-16 | - | 0.1km/132kV | `10596` | y |
| 577 | 63.3 | 200 | bess | PAST_EXPECTED_START | Worset Lane - Battery Energy Storage System | Clearstone Energy | Hartlepool | 2023-01-18 | 1321 | 4.8km/275kV | `11406` | y |
| 578 | 63.3 | 200 | bess | DESIGN_FROZEN_OR_LATER | Little Beanit Farm, Balsall Common - Battery Storage | Penso Power (BW ESS) | Solihull | 2023-08-31 | - | 0.4km/275kV | `11656` | y |
| 579 | 63.3 | 200 | bess | PAST_EXPECTED_START | Todhills and Westlinton - Harker Battery Energy Stor... | Windel Energy | Cumberland | 2024-03-14 | 900 | 0.8km/132kV | `15599` | y |
| 580 | 63.3 | 93 | bess | PAST_EXPECTED_START | Ipswich Road, Cardiff - Battery Storage | Green Frog Power 214 Limited | Cardiff | 2024-04-08 | 875 | 0.1km/132kV | `9910` | **n** |
| 581 | 63.2 | 20 | solar | PAST_EXPECTED_START | Craig Y Perchych, Glais - Solar farm | Windel Energy | Welsh Government (NSIP) | 2024-12-16 | 623 | 0.6km/400kV | `9777` | y |
| 582 | 63.2 | 20 | solar | PAST_EXPECTED_START | Totmonslow Farm, Upper Tean - Solar Farm | RE Projects Development Limited | Staffordshire Moorlands | 2023-08-17 | 1110 | 0.4km/400kV | `9232` | **n** |
| 583 | 63.2 | 9 | solar | PAST_EXPECTED_START | Merry Hill Shopping Centre - Solar Panels | Unknown | Dudley | 2025-06-11 | 446 | 0.3km/132kV | `18746` | y |
| 584 | 63.2 | 150 | bess | PRE_CONSENT | Riccarton Mains Road - Battery Energy Storage | Miller Developments | Scottish Government (S36) | - | - | 0.1km/275kV | `16656` | y |
| 585 | 63.2 | 150 | bess | PRE_CONSENT | Witney Bypass, Stanton Harcourt Road - Battery Stora... | Voltwise Power Holdings Limited | West Oxfordshire | - | - | 0.3km/132kV | `18593` | y |
| 586 | 63.1 | 42 | solar | PAST_EXPECTED_START | Parc Worlton Solar Farm | Lightrock Power | Welsh Government (NSIP) | 2025-01-21 | 587 | 0.9km/132kV | `12020` | y |
| 587 | 63.1 | 400 | solar | PAST_EXPECTED_START | East Yorkshire Solar Farm | Boom Power | The Planning Inspectorate - ... | 2025-05-09 | 479 | 3.7km/400kV | `15566` | y |
| 588 | 63.0 | 800 | solar | PRE_CONSENT | The Tween Bridge Solar Farm | RWE | The Planning Inspectorate - ... | - | - | 0.5km/400kV | `19574` | y |
| 589 | 63.0 | 500 | bess | PRE_CONSENT | Eckland Lodge Farm, Braybrooke - Battery Energy Stor... | Regener8 Power Limited | North Northamptonshire | - | - | 1.7km/400kV | `17405` | y |
| 590 | 63.0 | 500 | bess | PRE_CONSENT | Mop End Farm, Mop End Lane - Battery Energy Storage | Sandbrook Capital Bes Limited | Buckinghamshire | - | - | 0.5km/132kV | `19561` | y |
| 591 | 62.9 | 40 | solar | PAST_EXPECTED_START | Chalgrave Manor, Luton Road - Solar Farm | Aton Energy | Central Bedfordshire | 2023-05-19 | 1200 | 0.4km/132kV | `12490` | y |
| 592 | 62.9 | 40 | bess | PAST_EXPECTED_START | Goyt Hall Farm, Goyt Valley Footpath - Battery Energ... | Queequeg Renewables Limited | Stockport | 2024-08-23 | 738 | 0.5km/275kV | `13985` | y |
| 593 | 62.9 | 40 | solar | PAST_EXPECTED_START | Kitland Solar Farm | Statkraft UK Limited | North Somerset | 2024-12-19 | 620 | 0.5km/132kV | `14693` | y |
| 594 | 62.9 | 85 | bess | PAST_EXPECTED_START | Green Lane, Thurcroft - Battery Energy Storage Facil... | Newton Energi Limited | Rotherham | 2023-05-12 | 1207 | 0.2km/275kV | `12789` | y |
| 595 | 62.8 | 65 | solar | PAST_EXPECTED_START | Vianshill Farm, Parc Dyffryn - Solar Farm & Battery ... | Cenin Renewables Limited | Welsh Government (NSIP) | 2024-05-23 | 830 | 1.0km/132kV | `8460` | y |
| 596 | 62.8 | 30 | solar | PAST_EXPECTED_START | North Dairy Farm Solar Farm | British Solar Renewables | Dorset | 2024-01-15 | 959 | 0.7km/132kV | `14508` | y |
| 597 | 62.7 | 38 | solar | PAST_EXPECTED_START | Jockstown Farm Solar Farm | Green Energy International | Dumfries and Galloway | 2022-11-22 | 1378 | 0.7km/132kV | `8488` | y |
| 598 | 62.5 | 17 | solar | PAST_EXPECTED_START | Blythe House Farm Extension - Solar Array | Innova Renewables | Staffordshire Moorlands | 2024-07-22 | 770 | 0.4km/132kV | `15586` | y |
| 599 | 62.4 | 35 | solar | PAST_EXPECTED_START | East Aberthaw - Solar farm | Low Carbon UK Solar Investment Co ... | Welsh Government (NSIP) | 2024-12-20 | 619 | 1.2km/132kV | `10810` | y |
| 600 | 62.4 | 35 | solar | PAST_EXPECTED_START | Mount Farm, Mount Pleasant - Solar Farm | Mount Farm Solar Limited | Wychavon | 2024-06-07 | 815 | 3.6km/400kV | `15060` | y |
| 601 | 62.3 | 200 | bess | PRE_CONSENT | Womblehill Farm, Kintore - Battery Energy Storage Sy... | RE Projects Development (REPD) / F... | Scottish Government (S36) | - | - | 0.2km/132kV | `17325` | y |
| 602 | 62.3 | 120 | bess | PRE_CONSENT | Fort Widley, Portsdown Hill Road - Battery Energy St... | Voltwise Power Holdings Limited | Portsmouth | - | - | 0.8km/132kV | `19510` | y |
| 603 | 62.2 | 250 | bess | PRE_CONSENT | Abergelli Farm, Felindre - Battery Storage | EDF Energy Renewables | Swansea | - | - | 0.5km/400kV | `12661` | y |
| 604 | 62.2 | 5 | bess | PROCURING | St Columb Major - Battery Energy Storage Facility | Aldustria Energy Storage | Cornwall | 2025-05-19 | 469 | 4.3km/132kV | `18708` | y |
| 605 | 62.2 | 1 | solar | PROCURING | Suffolk Yacht Harbour, Levington - Solar Array | Suffolk Yacht Harbour Limited | East Suffolk | 2026-01-30 | 213 | 8.3km/132kV | `20011` | y |
| 606 | 62.1 | 70 | bess | PAST_EXPECTED_START | Oaklands Farm, New Road - Battery Energy Storage | Conrad Energy (Developments) II Li... | South Staffordshire | 2024-08-22 | 739 | 0.2km/132kV | `15735` | y |
| 607 | 62.1 | 244 | bess | PRE_CONSENT | Old Hall Farm, Lackenby - BESS | Lackenby Energy Limited | Redcar and Cleveland | - | - | 0.2km/400kV | `19565` | y |
| 608 | 62.1 | 400 | bess | PRE_CONSENT | The Tween Bridge Solar Farm | RWE | The Planning Inspectorate - ... | - | - | 0.5km/400kV | `12926` | y |
| 609 | 62.1 | 400 | solar | PRE_CONSENT | East Park Energy | Brockwell Energy | The Planning Inspectorate - ... | - | - | 1.0km/400kV | `15348` | y |
| 610 | 62.0 | 1000 | bess | PRE_CONSENT | Drakelow - Battery Energy Storage System | Tagenergy Development UK Limited | South Derbyshire | - | - | 0.4km/275kV | `17978` | y |
| 611 | 62.0 | 800 | bess | PRE_CONSENT | Sweetbriar Farm - Battery Energy Storage System | Lightrock Power Limited | North Lincolnshire | - | - | 0.8km/400kV | `18069` | y |
| 612 | 62.0 | 600 | bess | PRE_CONSENT | Beacon Fen Energy Park | Low Carbon Limited | The Planning Inspectorate - ... | - | - | 0.9km/132kV | `13599` | y |
| 613 | 62.0 | 600 | bess | PRE_CONSENT | Green Hill Solar Farm & Battery Storage | Island Green Power | The Planning Inspectorate - ... | - | - | 1.6km/132kV | `15793` | y |
| 614 | 62.0 | 600 | solar | PRE_CONSENT | Green Hill Solar Farm & Battery Storage | Island Green Power | The Planning Inspectorate - ... | - | - | 1.6km/132kV | `15794` | y |
| 615 | 62.0 | 531 | solar | PAST_EXPECTED_START | Gate Burton - Solar & Energy Storage Park | Low Carbon | The Planning Inspectorate - ... | 2024-07-12 | 780 | 1.2km/132kV | `9810` | y |
| 616 | 62.0 | 520 | bess | PRE_CONSENT | Red House Farm, Old Norwich Road - Battery Energy St... | The Surrey Research Park | Mid Suffolk | - | - | 0.8km/400kV | `18291` | y |
| 617 | 62.0 | 500 | solar | PAST_EXPECTED_START | Longfield | Longfield Solar Energy Farm Limite... | The Planning Inspectorate - ... | 2023-06-26 | 1162 | 0.2km/132kV | `8163` | y |
| 618 | 62.0 | 300 | bess | DESIGN_FROZEN_OR_LATER | Hornsea Project Three - Battery Storage | Orsted Power (UK) Limited | South Norfolk | 2023-01-23 | - | 0.4km/132kV | `9754` | y |
| 619 | 61.9 | 110 | bess | PRE_CONSENT | Bodelwyddan, Abergele Road - Solar Farm & Battery St... | Stantec | Welsh Government (NSIP) | - | - | 0.9km/132kV | `17948` | y |
| 620 | 61.9 | 110 | solar | PRE_CONSENT | Bodelwyddan, Abergele Road - Solar Farm & Battery St... | Stantec | Welsh Government (NSIP) | - | - | 0.9km/132kV | `17949` | y |
| 621 | 61.8 | 50 | bess | PAST_EXPECTED_START | Newmarket Road, Bottisham - Battery Energy Storage | Ridge Clean Energy Limited | East Cambridgeshire | 2023-12-21 | 984 | 0.8km/400kV | `10485` | y |
| 622 | 61.8 | 50 | bess | PROCURING | Battery Energy Storage System Development in Tyrone | Heron Storage Limited | Fermanagh and Omagh | 2025-03-20 | 529 | 77.2km/275kV | `16446` | y |
| 623 | 61.8 | 50 | solar | PAST_EXPECTED_START | Coldharbour Farm, Ashreigney - Solar Photovoltaic Ar... | Coldharbour Solar Park Limited | Torridge | 2023-09-19 | 1077 | 0.5km/132kV | `9456` | y |
| 624 | 61.8 | 30 | bess | PROCURING | Clachaig Glen | RWE UK | Scottish Government (S36) | 2024-11-05 | 664 | 7.2km/132kV | `8000` | y |
| 625 | 61.8 | 50 | solar | PAST_EXPECTED_START | Grange Of Berryhill - Solar Farm | Uniper UK Limited | Dundee City | 2022-09-21 | 1440 | 0.2km/132kV | `8480` | y |
| 626 | 61.8 | 50 | solar | PAST_EXPECTED_START | Hill Court, Tranton Lane Hill - Solar Farm | Longlands Solar Farm Limited | South Gloucestershire | 2023-06-30 | 1158 | 0.2km/132kV | `8890` | y |
| 627 | 61.8 | 50 | solar | PAST_EXPECTED_START | Low Farm, Flockton - Solar Photovoltaic Farm | Downing LLP | Kirklees | 2022-08-24 | 1468 | 1.2km/400kV | `9771` | y |
| 628 | 61.8 | 50 | solar | PAST_EXPECTED_START | Raspberry - Solar PV | RWE | Swale | 2024-06-28 | 794 | 0.7km/400kV | `10102` | **n** |
| 629 | 61.8 | 50 | solar | PAST_EXPECTED_START | Newmarket Road, Bottisham - Solar Array | Ridge Clean Energy Limited | East Cambridgeshire | 2023-12-21 | 984 | 0.8km/400kV | `10486` | y |
| 630 | 61.8 | 50 | solar | CONSENTED_NO_DATE | Longhedge Solar Farm | Renewable Energy Systems | Rushcliffe | - | - | 0.8km/132kV | `11063` | y |
| 631 | 61.8 | 50 | solar | PAST_EXPECTED_START | Straws Hadley Solar Farm | Qair UK | Buckinghamshire | 2024-12-06 | 633 | 0.5km/132kV | `12770` | y |
| 632 | 61.8 | 50 | solar | PAST_EXPECTED_START | East End Solar Farm | Low Carbon Solar Park 18 | Epping Forest | 2024-05-03 | 850 | 1.3km/132kV | `12925` | y |
| 633 | 61.8 | 50 | bess | PROCURING | Corshellach Battery Energy Storage | RES Limited | Northumberland | 2024-12-19 | 620 | 11.4km/132kV | `13290` | y |
| 634 | 61.8 | 50 | bess | PAST_EXPECTED_START | Kintore Substation, Leylodge - Battery Energy Storag... | XRE Gamma Limited / EDF | Aberdeenshire | 2024-09-13 | 717 | 0.1km/132kV | `14374` | **n** |
| 635 | 61.8 | 50 | solar | PAST_EXPECTED_START | Cobwood Solar Farm, Burnthouse Lane - Solar Farm & B... | Low Carbon UK Solar | Horsham | 2024-05-24 | 829 | 1.3km/400kV | `14833` | y |
| 636 | 61.8 | 50 | solar | PAST_EXPECTED_START | Weald Farm, Cambridge Road - Solar Farm & Battery St... | Ashfield District Council / Voltal... | Huntingdonshire | 2025-05-08 | 480 | 0.5km/132kV | `14874` | y |
| 637 | 61.8 | 50 | solar | PAST_EXPECTED_START | Abbotsley Country Homes, Drewels Lane - Solar Farm | Low Carbon Limited | Huntingdonshire | 2025-01-31 | 577 | 2.0km/132kV | `15490` | y |
| 638 | 61.6 | 130 | bess | PAST_EXPECTED_START | Stoke Lane - Battery Energy Storage | FPC Electric Land Limited | South Norfolk | 2022-09-09 | 1452 | 0.7km/400kV | `10390` | y |
| 639 | 61.6 | 212 | bess | PRE_CONSENT | Manor Farm, Dartford Road - Energy Storage System | Net Zero Thirty Three Limited | Bexley | - | - | 0.1km/400kV | `18107` | y |
| 640 | 61.6 | 100 | bess | PAST_EXPECTED_START | Balnuith Farm, Tealing - Battery Storage | Apatura | Scottish Government (S36) | 2024-10-22 | 678 | 0.1km/275kV | `13835` | y |
| 641 | 61.6 | 100 | bess | PRE_CONSENT | Hawkesyard Estate, Rugeley Road - Battery Energy Sto... | GSC Hawkesyard Limited | Lichfield | - | - | 0.6km/132kV | `14925` | y |
| 642 | 61.6 | 100 | bess | PRE_CONSENT | Church Bank - Battery Storage System | AMG Energy | South Tyneside | - | - | 0.3km/275kV | `18066` | y |
| 643 | 61.6 | 100 | bess | PRE_CONSENT | Thames Way, Northfleet - Battery Energy Storage | Speedgreen Limited | Gravesham | - | - | 0.8km/400kV | `18128` | y |
| 644 | 61.6 | 100 | bess | PRE_CONSENT | Old Allen Road, Wilsden - Battery Energy Storage Sys... | Renewable Connections Developments... | Bradford | - | - | 0.3km/132kV | `18266` | y |
| 645 | 61.5 | 60 | bess | PAST_EXPECTED_START | Greystones Road, Grangetown - Battery Energy Storage... | Sembcorp Utilities UK Limited | Redcar and Cleveland | 2021-12-17 | 1718 | 0.1km/275kV | `10081` | y |
| 646 | 61.5 | 440 | bess | PRE_CONSENT | Castle Road, Burton - Battery Energy Storage System | Rewe 7 Limited | Vale of Glamorgan | - | - | 2.1km/132kV | `19157` | y |
| 647 | 61.5 | 98 | bess | PRE_CONSENT | Coventry National Grid Substation, Hawkesbury Hall -... | Bluestone Energy | Coventry | - | - | 0.2km/275kV | `19945` | y |
| 648 | 61.4 | 27 | solar | PAST_EXPECTED_START | Wissett Solar Farm, Wissett - Solar Photovoltaic (PV... | Pathfinder Clean Energy UK Dev Lim... | East Suffolk | 2025-02-17 | 560 | 1.7km/132kV | `9913` | y |
| 649 | 61.4 | 27 | solar | PAST_EXPECTED_START | Washdyke Farm, Billingborough Road - Solar farm | GS Ignis Limited | South Kesteven | 2024-04-23 | 860 | 1.8km/132kV | `12419` | y |
| 650 | 61.3 | 57 | bess | PAST_EXPECTED_START | The Carrs - Meadow Farm Energy storage facility | BayWa r.e. | Stockton-on-Tees | 2023-09-21 | 1075 | 0.2km/132kV | `9207` | y |
| 651 | 61.3 | 57 | bess | PAST_EXPECTED_START | Ash Lane, Little London - Battery Storage | Bramley BESS Limited | Basingstoke and Deane | 2023-02-09 | 1299 | 0.3km/132kV | `11090` | y |
| 652 | 61.3 | 57 | bess | PAST_EXPECTED_START | Sutton Manor - Battery Storage Facility | Sizing John Limited | St. Helens | 2022-09-16 | 1445 | 0.1km/132kV | `11559` | y |
| 653 | 61.3 | 57 | bess | PAST_EXPECTED_START | The Rake, Lower Jowkin Lane - Battery Energy Storage | Shaw-Energi Limited | Rochdale | 2024-04-30 | 853 | 0.1km/132kV | `12187` | **n** |
| 654 | 61.3 | 57 | bess | PAST_EXPECTED_START | Southlands Solar Farm & Battery Storage | Enso Green Holdings Limited / Cero... | Chelmsford | 2024-11-26 | 643 | 0.4km/400kV | `13677` | y |
| 655 | 61.3 | 57 | bess | PAST_EXPECTED_START | Coxmoor Wood, Crondall Road - Battery Storage | Fleet Green Limited | Hart | 2024-04-22 | 861 | 0.6km/132kV | `13728` | y |
| 656 | 61.3 | 57 | bess | PAST_EXPECTED_START | Pentir Substation, Pentir - Battery Energy Storage | Lightsource BP | Gwynedd | 2024-09-09 | 721 | 0.1km/400kV | `15748` | y |
| 657 | 61.3 | 200 | bess | PRE_CONSENT | Pound Farm Lane - Battery Storage | Pulse Clean Energy | Rhondda Cynon Taf | - | - | 0.1km/275kV | `9969` | **n** |
| 658 | 61.3 | 200 | bess | PAST_EXPECTED_START | Westerleigh Hill, Westerleigh - Battery Energy Stora... | Immersa Limited | South Gloucestershire | 2024-07-19 | 773 | 1.1km/132kV | `13607` | y |
| 659 | 61.3 | 200 | bess | PRE_CONSENT | Cowpen Bewley, Seal Sands Link Road - Battery Energy... | Harmony Energy Limited | Stockton-on-Tees | - | - | 1.8km/400kV | `17005` | y |
| 660 | 61.3 | 200 | bess | PRE_CONSENT | Carrs Farm, South Hetton - Battery Energy Storage Sy... | Stephenson Halliday | County Durham | - | - | 0.3km/275kV | `18249` | y |
| 661 | 61.3 | 200 | bess | PRE_CONSENT | National Road, Cilfynydd - Battery Energy Storage Sy... | Rewe 2 Limited | Rhondda Cynon Taf | - | - | 0.3km/132kV | `19201` | y |
| 662 | 61.1 | 90 | bess | PAST_EXPECTED_START | Golf Road - Battery Energy Storage | Cragside Energy Limited | Trafford | 2024-10-18 | 682 | 0.2km/275kV | `13459` | y |
| 663 | 61.1 | 90 | bess | PRE_CONSENT | Dellows, Ginns Road - Battery Storage | Grenergy Renewables UK Limited | East Hertfordshire | - | - | 0.6km/132kV | `18668` | y |
| 664 | 61.1 | 400 | solar | PRE_CONSENT | Beacon Fen Energy Park | Low Carbon Limited | The Planning Inspectorate - ... | - | - | 0.9km/132kV | `13600` | y |
| 665 | 61.1 | 400 | bess | PRE_CONSENT | Cellarhead Substation, Rownall Road - Battery Storag... | S & C Energy Limited | Staffordshire Moorlands | - | - | 0.2km/400kV | `16111` | y |
| 666 | 61.1 | 25 | bess | PAST_EXPECTED_START | Stainland Road, Salterhebble - Battery Storage Facil... | Whirlwind Energy Storage Limited | Calderdale | 2021-09-28 | 1798 | 0.0km/132kV | `9397` | y |
| 667 | 61.1 | 25 | solar | PAST_EXPECTED_START | The Transmitting Station, Williton - Solar Farm (Wyn... | Elgin Energy ES Co Limited | Somerset | 2024-05-28 | 825 | 1.9km/132kV | `10106` | **n** |
| 668 | 61.1 | 25 | bess | PAST_EXPECTED_START | Pinkworthy Farm, Pyworthy - Battery Storage | Private Developer | Torridge | 2024-09-05 | 725 | 0.5km/132kV | `16068` | y |
| 669 | 61.1 | 114 | bess | PAST_EXPECTED_START | Hickling Lane, Swainsthorpe -Battery Storage | EDF Energy Renewables | South Norfolk | 2023-09-13 | 1083 | 0.1km/132kV | `13560` | y |
| 670 | 61.0 | 1000 | bess | PRE_CONSENT | Hawthorn Pit Green Energy Park - Battery Energy Stor... | NatPower UK | County Durham | - | - | 0.3km/275kV | `19676` | y |
| 671 | 61.0 | 500 | bess | DESIGN_FROZEN_OR_LATER | Devilla Energy Storage Facility | Alcemi Storage Development Limited | Scottish Government (S36) | 2023-12-13 | - | 0.6km/132kV | `9248` | y |
| 672 | 60.9 | 40 | solar | PAST_EXPECTED_START | Hinckley Road - Solar Farm | Capital Dynamics Limited | Blaby | 2023-05-10 | 1209 | 0.8km/400kV | `7715` | y |
| 673 | 60.9 | 40 | solar | PRE_CONSENT | Oldbridge, Congresbury - Solar Farm | Belltown Power Limited | North Somerset | - | - | 1.9km/400kV | `18440` | y |
| 674 | 60.9 | 180 | solar | PAST_EXPECTED_START | Byers Gill Solar Farm | JBM Solar Projects Limited | The Planning Inspectorate - ... | 2025-07-23 | 404 | 1.8km/132kV | `13156` | y |
| 675 | 60.8 | 39 | solar | PAST_EXPECTED_START | Glenniston Farm, Auchtertool - Solar Farm | Locogen Consulting Limited | Fife | 2024-04-05 | 878 | 0.2km/132kV | `10434` | y |
| 676 | 60.8 | 50 | bess | PAST_EXPECTED_START | Sundon Sub Station Battery Storage Facility | Clearstone Energy Limited | Central Bedfordshire | 2021-11-10 | 1755 | 0.1km/132kV | `9998` | y |
| 677 | 60.8 | 50 | bess | PAST_EXPECTED_START | Penstone Lane, Penn 1 - Battery Storage Facility | Anglo Renewables Limited | South Staffordshire | 2022-09-28 | 1433 | 0.3km/132kV | `10705` | y |
| 678 | 60.8 | 50 | bess | PAST_EXPECTED_START | Penstone Lane, Lower Penn 2 - Battery Storage | Anglo Renewables Limited | South Staffordshire | 2022-09-29 | 1432 | 0.3km/132kV | `10733` | y |
| 679 | 60.8 | 50 | bess | PAST_EXPECTED_START | South Staffordshire Railway Walk, Castlecroft - Batt... | Balance Power Projects Limited | South Staffordshire | 2022-08-16 | 1476 | 0.3km/132kV | `11414` | y |
| 680 | 60.8 | 50 | bess | PAST_EXPECTED_START | Swangate Project - Energy Storage System | Econergy International Limited | Rotherham | 2017-09-22 | 3265 | 0.1km/132kV | `11437` | y |
| 681 | 60.8 | 50 | bess | PAST_EXPECTED_START | Lancaster Power Extension, Middleton Road - Energy S... | Infra Balance New Energy | Lancaster | 2023-05-17 | 1202 | 0.3km/132kV | `12125` | y |
| 682 | 60.8 | 50 | bess | PAST_EXPECTED_START | Whelley Hill Farm, Worset Lane - Battery Energy Stor... | Reliance Energy Limited | Hartlepool | 2023-12-07 | 998 | 0.5km/275kV | `13246` | y |
| 683 | 60.8 | 50 | bess | PAST_EXPECTED_START | West Farm, Aspatria - Battery Storage Facility | Net Zero Seventeen Limited | Cumberland | 2024-09-04 | 726 | 0.8km/132kV | `15673` | y |
| 684 | 60.8 | 50 | solar | PAST_EXPECTED_START | Carlton Solar Farm | Island Green Power | North Yorkshire | 2024-04-17 | 866 | 0.9km/400kV | `12018` | y |
| 685 | 60.8 | 50 | bess | PAST_EXPECTED_START | Lapwing Fen II, Crown Farm | Private Developer | King's Lynn and West Norfolk | 2020-03-05 | 2370 | 0.8km/132kV | `7606` | y |
| 686 | 60.8 | 50 | solar | PAST_EXPECTED_START | Hasland Photovoltaic Solar Park | Kronos Solar | North East Derbyshire | 2021-12-08 | 1727 | 0.2km/132kV | `7887` | y |
| 687 | 60.8 | 50 | solar | PAST_EXPECTED_START | Nuneham Courtenay Solar Farm & Battery Storage Facil... | Enso Energy (Cowley Baldon Green L... | South Oxfordshire | 2022-01-11 | 1693 | 0.5km/132kV | `7937` | y |
| 688 | 60.8 | 50 | bess | PAST_EXPECTED_START | Mill Hill National Grid Substation | Harbour Energy | Barnet | 2023-03-13 | 1267 | 0.2km/275kV | `8009` | y |
| 689 | 60.8 | 50 | solar | PAST_EXPECTED_START | Bramley Frith Solar Farm | Bramley Solar Limited | Basingstoke and Deane | 2023-02-13 | 1295 | 0.4km/400kV | `8090` | y |
| 690 | 60.8 | 50 | bess | PAST_EXPECTED_START | Brentwood nergy Storage System | Anesco Limited | Brentwood | 2021-05-21 | 1928 | 0.2km/132kV | `8249` | y |
| 691 | 60.8 | 50 | solar | PAST_EXPECTED_START | Bloy’s Grove Solar Farm | EDF Energy Renewables | South Norfolk | 2022-08-04 | 1488 | 0.6km/400kV | `8308` | y |
| 692 | 60.8 | 50 | solar | PAST_EXPECTED_START | Horton Wood - Solar park | NextPower Horton Wood Limited | Sevenoaks | 2023-02-17 | 1291 | 1.0km/400kV | `8501` | y |
| 693 | 60.8 | 50 | solar | PAST_EXPECTED_START | Vicarage Drove - Solar farm & Battery storage | Renewable Connections Developments... | Boston | 2024-01-23 | 951 | 0.0km/132kV | `8518` | y |
| 694 | 60.8 | 50 | solar | PAST_EXPECTED_START | Canon Barns Road - Solar Photovoltaic Arrays & Batte... | Low Carbon Solar Park 5 Limited | Chelmsford | 2023-02-06 | 1302 | 0.5km/400kV | `8836` | **n** |
| 695 | 60.8 | 50 | bess | PAST_EXPECTED_START | Drumshoreland Road Battery Storage Facility | Sirius Renewables | West Lothian | 2022-07-07 | 1516 | 0.8km/132kV | `8920` | y |
| 696 | 60.8 | 50 | solar | PAST_EXPECTED_START | Gunthorpe Road, Marsh - Solar Farm | Walpole Green Limited | South Holland | 2023-09-29 | 1067 | 0.3km/400kV | `9319` | y |
| 697 | 60.8 | 50 | solar | PAST_EXPECTED_START | Whirlbush Farm, Kingsey - Solar Farm & Battery Stora... | Stark Energy | Buckinghamshire | 2022-03-03 | 1642 | 1.4km/132kV | `9348` | y |
| 698 | 60.8 | 50 | solar | PAST_EXPECTED_START | Jafa, Great Dunham - Solar Photovoltaic Farm & Batte... | Low Carbon UK Solar Investment Co ... | Breckland | 2023-03-30 | 1250 | 1.5km/132kV | `10307` | y |
| 699 | 60.8 | 50 | bess | PAST_EXPECTED_START | Newburgh Road, Abernethy - Battery Storage | CBS Solar Assets UK Limited | Perth and Kinross | 2022-09-26 | 1435 | 0.4km/132kV | `10607` | y |
| 700 | 60.8 | 50 | solar | PAST_EXPECTED_START | Callie's Solar Farm | Low Carbon UK Solar Investment Com... | Buckinghamshire | 2022-11-24 | 1376 | 1.8km/132kV | `10965` | y |
| 701 | 60.8 | 50 | bess | PAST_EXPECTED_START | South Leylodge Farmhouse, Kintore - Battery Energy S... | Conrad Energy (Developments) Limit... | Aberdeenshire | 2023-04-20 | 1229 | 0.1km/132kV | `11092` | y |
| 702 | 60.8 | 50 | solar | PAST_EXPECTED_START | Eckley Farms, Marden - Solar Energy Farm | Statkraft Wind UK Limited | Maidstone | 2024-02-05 | 938 | 0.4km/132kV | `11535` | y |
| 703 | 60.8 | 50 | bess | PAST_EXPECTED_START | Househill House, Househill - Battery Storage | Whirlwind Energy Storage Limited | Highland | 2023-02-15 | 1293 | 0.2km/132kV | `12056` | y |
| 704 | 60.8 | 50 | solar | PAST_EXPECTED_START | Cobholden Solar Farm | AGR Renewables | Bedford | 2025-01-30 | 578 | 0.5km/132kV | `12076` | y |
| 705 | 60.8 | 50 | bess | PAST_EXPECTED_START | Lichfield Road, Watton Lane - Battery Storage | Anglo ES Water Orton Limited | North Warwickshire | 2024-03-05 | 909 | 0.3km/132kV | `13369` | y |
| 706 | 60.8 | 50 | solar | PAST_EXPECTED_START | Froghall Farm, Wyton Road - Solar Farm & Battery Ene... | GAM Capital Limited | East Riding of Yorkshire | 2024-11-11 | 658 | 0.7km/275kV | `13655` | y |
| 707 | 60.8 | 50 | solar | PAST_EXPECTED_START | Church Farm, The Channel - Bramford Solar Farm and B... | Bramford Green Limited | Mid Suffolk | 2023-09-14 | 1082 | 0.6km/132kV | `13891` | y |
| 708 | 60.8 | 50 | bess | PAST_EXPECTED_START | Larks Lane & Latteridge Lane, Latteridge - Battery S... | Anglo Renewables | South Gloucestershire | 2024-01-04 | 970 | 0.1km/132kV | `14691` | y |
| 709 | 60.8 | 50 | bess | PAST_EXPECTED_START | Bankhead, Arbirlot - Battery Energy Storage | Ecocel Energy Storage Limited | Angus | 2024-09-19 | 711 | 0.8km/132kV | `14985` | y |
| 710 | 60.8 | 50 | solar | PAST_EXPECTED_START | Cattybrook Solar Farm | Luminous Energy Limited | South Gloucestershire | 2025-04-17 | 501 | 1.2km/132kV | `15626` | y |
| 711 | 60.8 | 50 | bess | PAST_EXPECTED_START | Coupar Angus, Pleasance Road - Battery Energy Facili... | Gresham House Asset Management Lim... | Perth and Kinross | 2024-09-11 | 719 | 0.3km/132kV | `16137` | y |
| 712 | 60.8 | 50 | bess | PAST_EXPECTED_START | Blue Bell Lodge, Rye Common Lane - Battery Storage | Pulse Clean Energy | Hart | 2023-05-22 | 1197 | 0.2km/132kV | `12496` | y |
| 713 | 60.8 | 50 | bess | PAST_EXPECTED_START | Coopers Lane, Kirkby - Battery Storage Facility | Pelagic Energy | Knowsley | 2024-04-30 | 853 | 0.1km/132kV | `14670` | y |
| 714 | 60.7 | 49 | bess | PAST_EXPECTED_START | Common Farm - Solar Farm & Battery Storage | Banks Renewable | Rotherham | 2023-06-13 | 1175 | 3.6km/400kV | `9787` | **n** |
| 715 | 60.6 | 10 | solar | PAST_EXPECTED_START | Reeds Solar Farm, Alders Road - Solar Farm & Battery... | Low Carbon | Tunbridge Wells | 2025-03-06 | 543 | 0.2km/132kV | `12941` | y |
| 716 | 60.6 | 10 | solar | PAST_EXPECTED_START | North Allington Solar Farm - Solar Farm | Noventum Power Limited | Wiltshire | 2025-09-26 | 339 | 0.9km/400kV | `17531` | y |
| 717 | 60.6 | 10 | solar | PAST_EXPECTED_START | Talbot Green, Llantrisant - Solar Farm | Windel Energy | Rhondda Cynon Taf | 2024-04-25 | 858 | 0.5km/132kV | `9772` | y |
| 718 | 60.6 | 100 | bess | PAST_EXPECTED_START | Hales Lane - Battery Storage Facility | Aura Power | North Yorkshire | 2022-05-16 | 1568 | 0.7km/400kV | `9635` | y |
| 719 | 60.6 | 100 | bess | PAST_EXPECTED_START | Shaftesbury Energy Park - Battery Storage System | TagEnergy | Dorset | 2023-03-29 | 1251 | 0.3km/132kV | `10626` | y |
| 720 | 60.6 | 100 | bess | PAST_EXPECTED_START | Capenhurst Lane, Capenhurst - Battery Storage | Aura Power BESS Limited | Cheshire West and Chester | 2023-12-08 | 997 | 0.1km/132kV | `12503` | y |
| 721 | 60.6 | 100 | bess | PAST_EXPECTED_START | Hillside Farm, Lancaster Road - Battery Storage | Hamilton March | Lancaster | 2023-09-19 | 1077 | 1.1km/400kV | `12964` | y |
| 722 | 60.6 | 100 | bess | PAST_EXPECTED_START | Walshaw House, Regent Street - Battery Energy Storag... | R B Business Park Limited | Pendle | 2023-12-14 | 991 | 0.2km/132kV | `14625` | y |
| 723 | 60.6 | 100 | bess | PAST_EXPECTED_START | Lakeside Energy Storage Facility | Tag Energy UK | North Yorkshire | 2021-05-06 | 1943 | 0.1km/132kV | `8268` | y |
| 724 | 60.5 | 99 | bess | PAST_EXPECTED_START | Scawby Brook, Brigg - Battery Storage | Centrica Plc | North Lincolnshire | 2021-09-09 | 1817 | 0.1km/132kV | `9848` | y |
| 725 | 60.4 | 45 | solar | PAST_EXPECTED_START | Brecks Solar Farm | Green Switch Capital Limited | Mansfield | 2023-09-18 | 1078 | 2.0km/275kV | `10087` | y |
| 726 | 60.4 | 21 | solar | PAST_EXPECTED_START | Brynwell Farm | Brynwell Farm Solar Limited | Welsh Government (NSIP) | 2022-11-10 | 1390 | 0.5km/132kV | `9067` | y |
| 727 | 60.4 | 75 | bess | PAST_EXPECTED_START | Holly Lane Energy Park - Solar Farm & Battery Storag... | Exagen | Warwick | 2025-01-30 | 578 | 0.2km/132kV | `13694` | y |
| 728 | 60.4 | 35 | solar | PAST_EXPECTED_START | Wickham Hall Estate Solar Photovoltaic Farm | Endurance Energy Wickham Hall Limi... | East Hertfordshire | 2023-12-19 | 986 | 0.5km/400kV | `10265` | y |
| 729 | 60.4 | 35 | bess | CONSENTED_NO_DATE | Wild Fowl Farm, Carrington Lane - Battery Storage Fa... | O&G Solar (SPV 56) Ltd | Trafford | - | - | 0.2km/132kV | `16383` | y |
| 730 | 60.4 | 45 | bess | PAST_EXPECTED_START | Cheshire Power Station - Battery Storage Facility | RWE Generation UK Plc | Cheshire West and Chester | 2023-05-24 | 1195 | 0.7km/132kV | `10295` | y |
| 731 | 60.3 | 20 | solar | PAST_EXPECTED_START | Mains Of Keithick Farm, Keithick - Battery Storage &... | EcoDev Group Limited | Scottish Government (S36) | 2025-03-13 | 536 | 1.5km/132kV | `11623` | y |
| 732 | 60.2 | 20 | solar | PAST_EXPECTED_START | Cwm Ivor Penyrheol Solar Farm | Caerphilly County Borough Council | Welsh Government (NSIP) | 2024-05-23 | 830 | 0.6km/132kV | `9398` | y |
| 733 | 60.2 | 20 | bess | PAST_EXPECTED_START | The Transmitting Station, Williton - Battery Storage... | Elgin Energy ES Co Limited | Somerset | 2024-05-28 | 825 | 1.9km/132kV | `10105` | **n** |
| 734 | 60.2 | 20 | bess | PAST_EXPECTED_START | Denfield Farm | Seahills Properties Limited | Angus | 2024-01-05 | 969 | 0.2km/132kV | `14341` | y |
| 735 | 60.2 | 150 | bess | PRE_CONSENT | Steeple Renewables Project | Renewable Energy Systems RES Limit... | The Planning Inspectorate - ... | - | - | 0.3km/400kV | `15252` | y |
| 736 | 60.2 | 150 | bess | PRE_CONSENT | Rayleigh Spur Roundabout, Benfleet - Battery Energy ... | Renewable Energy Systems RES ltd (... | Basildon | - | - | 0.9km/132kV | `18649` | y |
| 737 | 60.2 | 150 | bess | PRE_CONSENT | Bedhampton Pumping Station, Meyrick Road - Battery E... | E101 Hub 4 Limited | Havant | - | - | 1.5km/132kV | `18986` | y |
| 738 | 60.1 | 90 | bess | PAST_EXPECTED_START | Little Crow Solar Park | INRG Solar | The Planning Inspectorate - ... | 2022-04-05 | 1609 | 0.1km/132kV | `6557` | y |
| 739 | 60.1 | 90 | bess | PAST_EXPECTED_START | Caldwell Road - Battery Storage | Aludra Bess Limited / Renewable En... | South Derbyshire | 2024-07-02 | 790 | 0.4km/400kV | `9507` | **n** |
| 740 | 60.1 | 312 | bess | PAST_EXPECTED_START | Stargoose Farm - Battery Storage | Solarcentury Limited / Statkraft U... | South Cambridgeshire | 2022-04-14 | 1600 | 0.4km/132kV | `9240` | y |
| 741 | 60.1 | 400 | bess | DESIGN_FROZEN_OR_LATER | Hams Hall - Battery Energy Storage System | Welbar Energy Storage Limited / Pe... | North Warwickshire | 2022-03-04 | - | 0.1km/275kV | `9427` | y |
| 742 | 60.1 | 147 | solar | PRE_CONSENT | Frodsham Solar Project & Battery Storage | Cubico Renewables | The Planning Inspectorate - ... | - | - | 0.3km/400kV | `14097` | y |
| 743 | 60.0 | 4 | solar | PAST_EXPECTED_START | Hedco, Desoto Road - Solar panels | PSD Construct Limtied | Halton | 2024-06-14 | 808 | 1.0km/132kV | `11448` | y |
| 744 | 60.0 | 1000 | bess | PRE_CONSENT | Mowbray Battery Energy Storage Station | Mowbray Energy Park Limited | North Yorkshire | - | - | 0.4km/400kV | `18123` | y |
| 745 | 60.0 | 800 | solar | PRE_CONSENT | Great North Road Solar Park | Elements Green | The Planning Inspectorate - ... | - | - | 1.1km/400kV | `15150` | y |
| 746 | 60.0 | 500 | bess | PRE_CONSENT | Titan Battery Storage | Green Switch Capital Limited | Scottish Government (S36) | - | - | 0.5km/132kV | `17143` | y |
| 747 | 60.0 | 500 | solar | PRE_CONSENT | The Droves Solar Farm | Island Green Power | The Planning Inspectorate - ... | - | - | 1.4km/400kV | `17560` | y |
| 748 | 60.0 | 500 | bess | PRE_CONSENT | Greystone, Blackhills - Battery Energy Storage Syste... | Peterhead Flexpower | Scottish Government (S36) | - | - | 0.1km/275kV | `19212` | y |
| 749 | 59.9 | 40 | solar | PAST_EXPECTED_START | Desford Road, Thurlaston | Elgin Energy EsCo | Blaby | 2018-09-17 | 2905 | 1.0km/132kV | `6515` | y |
| 750 | 59.9 | 40 | bess | PAST_EXPECTED_START | Rubber and Allied Products | Volta Energy Storage | Newcastle-under-Lyme | 2017-12-15 | 3181 | 0.7km/132kV | `7096` | y |
| 751 | 59.9 | 40 | bess | PAST_EXPECTED_START | Tanners Lane - Battery Energy Storage Facility (Phas... | British Solar Renewables | Fareham | 2019-11-26 | 2470 | 0.3km/132kV | `9708` | y |
| 752 | 59.9 | 40 | bess | PAST_EXPECTED_START | Tofts Lane, Hunshelf - Battery Storage | Harmony HS (JV) Limited | Barnsley | 2023-11-13 | 1022 | 0.4km/132kV | `13733` | y |
| 753 | 59.9 | 40 | bess | PAST_EXPECTED_START | Claire Court, Rawmarsh Road - Battery Energy Storage... | Conrad Energy (Developments) Ii Li... | Rotherham | 2023-06-20 | 1168 | 0.1km/132kV | `13774` | y |
| 754 | 59.9 | 40 | bess | PAST_EXPECTED_START | Draycott Cross Road - Battery Storage System | Balance Power Projects Limited | Staffordshire Moorlands | 2024-01-05 | 969 | 1.7km/400kV | `14284` | y |
| 755 | 59.9 | 30 | solar | CONSENTED_NO_DATE | Windmill Farm Solar Farm (Old Malton) | Harmony Energy | North Yorkshire | - | - | 1.6km/132kV | `8348` | y |
| 756 | 59.8 | 18 | solar | PAST_EXPECTED_START | New Farm House Locks Farm | Nextpower Spv 12 Limited | Winchester | 2023-06-09 | 1179 | 0.3km/400kV | `7924` | y |
| 757 | 59.8 | 50 | bess | CONSENTED_NO_DATE | Armshead Farm, Armshead Road - Battery Energy Storag... | Conrad Energy (Developments) Limit... | Staffordshire Moorlands | - | - | 0.6km/132kV | `12804` | y |
| 758 | 59.8 | 30 | solar | PAST_EXPECTED_START | Hengrove Farm, Shottendane Road - Solar Farm | Industria Solar Bedworth Limited | Thanet | 2024-08-28 | 733 | 1.0km/132kV | `15013` | y |
| 759 | 59.8 | 50 | solar | CONSENTED_NO_DATE | Ledburn, Mentmore - Solar Farm | Vattenfall Wind Power Limited (Vat... | Buckinghamshire | - | - | 0.6km/132kV | `11814` | y |
| 760 | 59.7 | 38 | bess | PAST_EXPECTED_START | Maiden, Annfield Plain - Energy Storage | Stephenson Mohl Development | County Durham | 2021-08-18 | 1839 | 0.1km/132kV | `9036` | y |
| 761 | 59.7 | 80 | bess | PAST_EXPECTED_START | Netherlands Way - Battery Energy Facility | Volta Energy Group | North East Lincolnshire | 2022-01-06 | 1698 | 0.1km/132kV | `10429` | y |
| 762 | 59.6 | 130 | bess | PAST_EXPECTED_START | Clough Road - Battery Energy System | GAM Capital Limited | Kingston upon Hull, City of | 2023-09-12 | 1084 | 0.3km/132kV | `14225` | y |
| 763 | 59.6 | 100 | bess | PRE_CONSENT | Butterfly Lane, Elstree BESS - Battery Energy Storag... | Greenfield Energy Developments Lim... | Hertsmere | - | - | 1.3km/132kV | `19441` | **n** |
| 764 | 59.5 | 60 | bess | PRE_CONSENT | Pinstone Farm, Oxford Road - Battery Energy Storage ... | Voltwise Power Holdings Limited | Buckinghamshire | - | - | 0.8km/132kV | `18701` | y |
| 765 | 59.5 | 36 | solar | PAST_EXPECTED_START | Brynrhyd Solar Farm | Capital Dynamics Limited | Welsh Government (NSIP) | 2023-06-20 | 1168 | 1.9km/400kV | `9977` | y |
| 766 | 59.5 | 36 | bess | PAST_EXPECTED_START | Kingston Road, Slimbridge - Battery Storage | Relay Slimbridge Limited | Stroud | 2024-07-17 | 775 | 0.3km/132kV | `11516` | **n** |
| 767 | 59.4 | 75 | bess | PAST_EXPECTED_START | Quarterland Road, Islandmagee - Battery Storage | Solo Renewables Ltd | Mid and East Antrim | 2024-01-19 | 955 | 0.3km/275kV | `14117` | y |
| 768 | 59.4 | 35 | bess | PAST_EXPECTED_START | Northington Lane - Battery Storage Facility | Green Frog Ventures Limited | Forest of Dean | 2023-05-09 | 1210 | 0.1km/132kV | `9992` | y |
| 769 | 59.4 | 16 | solar | PAST_EXPECTED_START | County Lane - Solar farm | Boultbee Brooks Renewable Energy L... | Shropshire | 2023-03-21 | 1259 | 1.6km/400kV | `11166` | y |
| 770 | 59.4 | 16 | bess | PAST_EXPECTED_START | Mains Of Keithick Farm, Keithick - Battery Storage &... | EcoDev Group Limited | Scottish Government (S36) | 2023-03-21 | 1259 | 1.5km/132kV | `11622` | y |
| 771 | 59.3 | 56 | solar | PAST_EXPECTED_START | Mere Flats Solar Farm | NextPower UK | Doncaster | 2023-05-03 | 1216 | 0.3km/275kV | `12081` | y |
| 772 | 59.2 | 56 | bess | PAST_EXPECTED_START | High Constellation Wind Farm | BayWa r.e. UK Limited | Scottish Government (S36) | 2020-06-26 | 2257 | 1.8km/132kV | `7345` | y |
| 773 | 59.2 | 250 | bess | PRE_CONSENT | Toddington Services, Hipsey Spinney - Battery Storag... | Kona Energy Limited | Central Bedfordshire | - | - | 0.3km/132kV | `15883` | y |
| 774 | 59.2 | 320 | bess | DESIGN_FROZEN_OR_LATER | Monk Fryston Battery Storage | SSE Renewables | North Yorkshire | 2022-12-01 | - | 0.1km/275kV | `15164` | y |
| 775 | 59.2 | 33 | solar | PAST_EXPECTED_START | Barkham Farms - Solar Farm | Wokingham Borough Council | Wokingham | 2022-01-21 | 1683 | 0.2km/132kV | `8491` | y |
| 776 | 59.2 | 150 | solar | PAST_EXPECTED_START | Little Crow Solar Park | INRG Solar | The Planning Inspectorate - ... | 2022-04-05 | 1609 | 0.2km/132kV | `7175` | y |
| 777 | 59.1 | 15 | solar | PAST_EXPECTED_START | Walkford Moor Solar Farm, Walkford Lane - Solar Farm | Boultbee Brooks (Renewables Costoc... | New Forest | 2024-08-14 | 747 | 0.6km/132kV | `14066` | y |
| 778 | 59.1 | 15 | solar | PAST_EXPECTED_START | Northorpe Fen Farm, Fen Road - Solar Farm | Aardvark EM Limited | South Kesteven | 2025-12-19 | 255 | 1.4km/132kV | `15984` | y |
| 779 | 59.1 | 400 | bess | PRE_CONSENT | Bronwylfa Road, Rhostyllen - Energy Storage System | Innova Renewables | Wrexham | - | - | 0.4km/132kV | `16114` | y |
| 780 | 59.1 | 400 | bess | PRE_CONSENT | Flushing, Longside - Battery Energy Storage System | Harmony Energy Storage | Scottish Government (S36) | - | - | 1.7km/132kV | `18195` | y |
| 781 | 59.1 | 400 | bess | PRE_CONSENT | Netherton, Langside Road - Battery Energy Storage Sy... | Field Energy | Scottish Government (S36) | - | - | 1.0km/400kV | `19029` | y |
| 782 | 59.1 | 25 | solar | PAST_EXPECTED_START | Holly Lane Energy Park - Solar Farm & Battery Storag... | Exagen | Solihull | 2025-01-30 | 578 | 1.6km/132kV | `13695` | y |
| 783 | 59.0 | 1000 | bess | DESIGN_FROZEN_OR_LATER | Coalburn II Energy Storage Facility - Battery Storag... | Alcemi Storage Development Limited | Scottish Government (S36) | 2024-01-24 | - | 0.8km/400kV | `12206` | y |
| 784 | 59.0 | 500 | solar | PAST_EXPECTED_START | Heckington Fen Solar Park | Ecotricity Limited | The Planning Inspectorate - ... | 2025-01-24 | 584 | 3.8km/400kV | `9807` | y |
| 785 | 59.0 | 500 | bess | PRE_CONSENT | Lime Down - Battery Storage | Island Green Power | The Planning Inspectorate - ... | - | - | 6.1km/400kV | `16063` | y |
| 786 | 59.0 | 500 | solar | PRE_CONSENT | Lime Down - Solar Project | Island Green Power | The Planning Inspectorate - ... | - | - | 6.1km/400kV | `16064` | y |
| 787 | 59.0 | 14 | solar | PAST_EXPECTED_START | East Fulwood Greenock Road - Solar Farm | Springfield Limited / Aggreko | Renfrewshire | 2023-01-24 | 1315 | 0.3km/400kV | `9946` | y |
| 788 | 58.9 | 40 | solar | CONSENTED_NO_DATE | Littywood Farm, Toft Lane - Solar Array | Elgin Energy Services | South Staffordshire | - | - | 0.6km/132kV | `12981` | y |
| 789 | 58.9 | 140 | bess | PAST_EXPECTED_START | Coolkeeragh - Battery Storage | Coolkeeragh BES Ltd | Derry City and Strabane | 2024-06-30 | 792 | 0.2km/275kV | `15151` | y |
| 790 | 58.9 | 14 | solar | PAST_EXPECTED_START | Tiddiecross Lane, Charlton - Tiddiecross Solar Farm ... | Boultbee Brooks Renewables Walkfor... | Telford and Wrekin | 2025-06-06 | 451 | 1.4km/132kV | `17854` | y |
| 791 | 58.9 | 228 | bess | PRE_CONSENT | Wymondham Road, Bracon Ash - Battery Energy Storage ... | Green Switch Capital | South Norfolk | - | - | 1.9km/400kV | `18621` | y |
| 792 | 58.8 | 50 | bess | PAST_EXPECTED_START | Says Court Farm, Coalpit Heath - Battery Energy Stor... | Anglo Renewables Limited | South Gloucestershire | 2022-11-02 | 1398 | 0.4km/132kV | `11793` | y |
| 793 | 58.8 | 50 | bess | PAST_EXPECTED_START | Fairholme, Minety - Battery Storage | Pelagic Energy | Wiltshire | 2024-05-31 | 822 | 0.8km/132kV | `11810` | y |
| 794 | 58.8 | 50 | bess | CONSENTED_NO_DATE | Lowlands Farm - Battery Storage | Anglo Renewables | Dudley | - | - | 0.6km/132kV | `12959` | y |
| 795 | 58.8 | 50 | bess | PAST_EXPECTED_START | Bluebell Wood Solar Farm & Battery Storage | Low Carbon UK Solar Investment Co ... | Somerset | 2024-07-16 | 776 | 0.5km/132kV | `13988` | y |
| 796 | 58.8 | 50 | bess | PAST_EXPECTED_START | Cutts Bros, Wharf Road - Battery Storage Facility | Newton Energi Limited | Doncaster | 2024-10-29 | 671 | 1.0km/132kV | `15235` | **n** |
| 797 | 58.8 | 50 | solar | PAST_EXPECTED_START | Pilmoor Solar Farm | Stark Energy | North Yorkshire | 2024-09-11 | 719 | 0.6km/400kV | `15452` | y |
| 798 | 58.8 | 50 | solar | PAST_EXPECTED_START | Burnt House Farm - Solar Farm | Bluefield Renewable Developments L... | Northumberland | 2022-11-04 | 1396 | 0.6km/400kV | `17272` | y |
| 799 | 58.8 | 30 | bess | PAST_EXPECTED_START | Torrington Avenue Battery Storage Facility | Power Initiatives Limited | Coventry | 2024-04-15 | 868 | 0.1km/132kV | `9109` | **n** |
| 800 | 58.8 | 30 | solar | PAST_EXPECTED_START | Park Lane, Astley - Solar PV Farm | Tor Energy Solar Limited | North Warwickshire | 2022-07-28 | 1495 | 1.2km/400kV | `10104` | **n** |
| 801 | 58.8 | 30 | bess | PAST_EXPECTED_START | West Sleekburn - Battery Storage Compound | Enviromena Asset Management UK Lim... | Northumberland | 2022-10-19 | 1412 | 0.5km/132kV | `10957` | y |
| 802 | 58.8 | 30 | bess | PAST_EXPECTED_START | Rectory Farm, Rectory Lane - Battery Storage | Tag Energy | Wychavon | 2023-02-20 | 1288 | 0.3km/132kV | `11905` | y |
| 803 | 58.8 | 50 | bess | PAST_EXPECTED_START | National Grid Minety Substation | Harbour Energy | Wiltshire | 2021-01-25 | 2044 | 0.1km/132kV | `8021` | y |
| 804 | 58.8 | 50 | solar | PAST_EXPECTED_START | Sheraton Hall Solar Farm | Lightsource BP | County Durham | 2023-12-06 | 999 | 0.5km/275kV | `8254` | y |
| 805 | 58.8 | 50 | solar | PAST_EXPECTED_START | Chosley Farm, North Warnborough Solar Farm and Batte... | Shell Renewables (CSE23 Limited) | Hart | 2021-11-11 | 1754 | 2.7km/132kV | `8427` | y |
| 806 | 58.8 | 50 | bess | PAST_EXPECTED_START | Shindour - Energy Storage Facility | Gigabox Developments Limited | Stirling | 2021-12-16 | 1719 | 0.3km/400kV | `8464` | y |
| 807 | 58.8 | 50 | solar | PAST_EXPECTED_START | Brick House Farm - Solar Farm | Bluefield Renewwable Developments ... | Shropshire | 2022-10-21 | 1410 | 0.5km/132kV | `10513` | y |
| 808 | 58.8 | 50 | solar | PAST_EXPECTED_START | Rutton Farm, Whimple - Horton Solar Farm | Aura Power Developments Limited | East Devon | 2023-06-16 | 1172 | 0.6km/400kV | `11274` | y |
| 809 | 58.8 | 50 | solar | PAST_EXPECTED_START | Pilton Village, Luffenham Lane - Staveley Solar Arra... | Bluestone Energy Limited | Rutland | 2025-03-27 | 522 | 3.8km/132kV | `12827` | y |
| 810 | 58.8 | 50 | solar | PAST_EXPECTED_START | Long Whatton - Solar Farm | Endurance Energy Oakley Limited | Charnwood | 2024-02-26 | 917 | 0.4km/132kV | `13392` | y |
| 811 | 58.8 | 50 | solar | PAST_EXPECTED_START | Lower Farm, Drointon Lane - Solar farm & Battery Ene... | Innova Renewables | Stafford | 2025-01-14 | 594 | 0.7km/132kV | `13550` | y |
| 812 | 58.8 | 50 | solar | PAST_EXPECTED_START | Bluebell Wood Solar Farm & Battery Storage | Low Carbon UK Solar Investment Co ... | Somerset | 2024-07-16 | 776 | 0.5km/132kV | `13989` | y |
| 813 | 58.8 | 50 | solar | PAST_EXPECTED_START | The Balk, Almholme - Solar Farm | Innova Renewables | Doncaster | 2024-10-14 | 686 | 0.9km/275kV | `14061` | y |
| 814 | 58.8 | 50 | solar | PAST_EXPECTED_START | Croxdale Farms, Hett Moor Farm - Solar Farm | Lightsource SPV 189 Limited | County Durham | 2024-11-14 | 655 | 0.5km/400kV | `14327` | y |
| 815 | 58.8 | 50 | solar | PAST_EXPECTED_START | High Barnes Farm, Coal Lane - Solar Farm | Enviromena Project Management UK L... | Hartlepool | 2025-05-28 | 460 | 2.1km/275kV | `16082` | y |
| 816 | 58.8 | 50 | solar | PRE_CONSENT | Newlands Farm, Turnham Lane - Solar PV Panels | Stark Energy | North Yorkshire | - | - | 0.6km/132kV | `18955` | y |
| 817 | 58.8 | 50 | bess | PAST_EXPECTED_START | Gleniston, Auchtertool - Battery Storage Facility | Harmony Energy Limited | Fife | 2022-11-01 | 1399 | 0.1km/132kV | `11808` | y |
| 818 | 58.8 | 50 | solar | PAST_EXPECTED_START | Hanyards Lane, Tixall - Solar Energy Park | Private Developer | Stafford | 2024-06-19 | 803 | 1.0km/132kV | `13140` | y |
| 819 | 58.7 | 48 | solar | PAST_EXPECTED_START | Lawn Lane, Coven - Solar Farm | Anesco Limited | South Staffordshire | 2024-08-22 | 739 | 1.4km/275kV | `14574` | y |
| 820 | 58.7 | 48 | solar | PAST_EXPECTED_START | The Grange Solar Farm & Battery Storage | Pathfinder Clean Energy UK Dev Lim... | Mid Suffolk | 2023-11-09 | 1026 | 0.2km/132kV | `20390` | y |
| 821 | 58.6 | 354 | bess | PRE_CONSENT | Beane Solar Farm - Solar Panels | Renewable Energy Systems RES ltd (... | East Hertfordshire | - | - | 0.8km/132kV | `15672` | y |
| 822 | 58.6 | 13 | solar | PAST_EXPECTED_START | Chelson Meadow - Solar Farm | PEC Renewables Limited & Plymouth ... | Plymouth | 2022-06-24 | 1529 | 0.6km/132kV | `9571` | y |
| 823 | 58.6 | 350 | bess | PAST_EXPECTED_START | Camsiscan Farm, Craigie - Battery Energy Storage Sys... | Noriker Power Limited | Scottish Government (S36) | 2024-01-26 | 948 | 0.7km/275kV | `12820` | y |
| 824 | 58.6 | 100 | bess | PRE_CONSENT | Braidfield Road, Hardgate - Battery Storage Facility | Intelligent Land Investments Group... | Scottish Government (S36) | - | - | 0.1km/132kV | `11853` | y |
| 825 | 58.6 | 100 | bess | PAST_EXPECTED_START | Flemyland Battery Storage | Flemyland Battery Storage Limited | Scottish Government (S36) | 2024-12-06 | 633 | 0.8km/132kV | `13770` | y |
| 826 | 58.6 | 100 | bess | PRE_CONSENT | Frodsham Solar Project & Battery Storage | Cubico Renewables | The Planning Inspectorate - ... | - | - | 0.3km/400kV | `14096` | y |
| 827 | 58.6 | 100 | bess | PRE_CONSENT | Lowland Farm, Peel Road - Battery Energy Storage Fac... | Max Design Consultancy | Fylde | - | - | 0.5km/132kV | `18474` | y |
| 828 | 58.6 | 100 | bess | PRE_CONSENT | Station Road & Nye Road, Sandford - Battery Energy S... | Aura Power Developments Limited | North Somerset | - | - | 0.3km/132kV | `19207` | y |
| 829 | 58.6 | 100 | bess | PRE_CONSENT | Catsfield Christmas Tree Farm, The Stream - Battery ... | Elgin Energy Esco Limited | Rother | - | - | 1.1km/400kV | `19474` | y |
| 830 | 58.5 | 99 | bess | PRE_CONSENT | West Webbery Farm, The Water - Battery Energy Storag... | Enray SPV 241491 Limited | Torridge | - | - | 0.9km/132kV | `20307` | y |
| 831 | 58.5 | 162 | bess | PRE_CONSENT | Achies - Battery Energy Storage System | Sun4net Limited | Scottish Government (S36) | - | - | 1.8km/275kV | `18500` | y |
| 832 | 58.5 | 46 | solar | PAST_EXPECTED_START | Winchester Road, Wherwell - Solar Farm | RE Projects Development / Solarig | Test Valley | 2025-02-05 | 572 | 0.4km/132kV | `11883` | y |
| 833 | 58.4 | 160 | solar | PAST_EXPECTED_START | Alaw Môn Solar Farm - Solar Farm & Energy Storage F... | Enso Energy Limited | Welsh Government (NSIP) | 2025-08-26 | 370 | 8.2km/400kV | `18490` | y |
| 834 | 58.4 | 2 | solar | PAST_EXPECTED_START | Wester Moffat Farm, Towers Road - Solar Photovoltaic... | NHS Lanarkshire | North Lanarkshire | 2026-01-16 | 227 | 0.5km/275kV | `19151` | y |
| 835 | 58.4 | 45 | bess | PRE_CONSENT | Locks Street, Coatdyke - Battery Energy Storage Syst... | Bluestone Energy | North Lanarkshire | - | - | 1.5km/275kV | `18919` | y |
| 836 | 58.3 | 57 | bess | PAST_EXPECTED_START | Penwortham - Battery storage | Shaw-Energi Limited | South Ribble | 2022-04-29 | 1585 | 0.1km/132kV | `11217` | y |
| 837 | 58.3 | 200 | bess | PAST_EXPECTED_START | Drax Re-Power | Drax Group | The Planning Inspectorate - ... | 2018-05-24 | 3021 | 0.1km/132kV | `7017` | y |
| 838 | 58.3 | 200 | bess | PRE_CONSENT | Stocking Lane - Battery Energy Facility | Nel Tiger | North Yorkshire | - | - | 0.7km/400kV | `15082` | y |
| 839 | 58.3 | 200 | bess | PRE_CONSENT | Sunbury Battery Energy Storage System - Battery Ener... | EcoDev Group Limited | Spelthorne | - | - | 2.6km/275kV | `17161` | y |
| 840 | 58.3 | 200 | bess | PRE_CONSENT | Cefn Farm, Mount Road - Battery Energy Storage Syste... | Tec Marina | Rhondda Cynon Taf | - | - | 0.2km/132kV | `17655` | y |
| 841 | 58.3 | 120 | bess | DESIGN_FROZEN_OR_LATER | Uskmouth Power Station, West Nash Road - Battery Sto... | AW1 Energy Storage Limited | Newport | 2024-01-11 | - | 0.3km/132kV | `15263` | y |
| 842 | 58.2 | 20 | bess | PAST_EXPECTED_START | Fordhouse Lane - Battery Energy Storage System | FPC (Electric Land) Limited | Birmingham | 2023-08-18 | 1109 | 0.6km/132kV | `13108` | y |
| 843 | 58.2 | 249 | bess | DESIGN_FROZEN_OR_LATER | Richborough Energy Park - Phase 3 (Sheaf) | Pacific Green | Thanet | 2022-09-22 | - | 0.1km/400kV | `11201` | y |
| 844 | 58.2 | 20 | solar | PAST_EXPECTED_START | Watling Street, Caddington - Solar Farm | Chiltern Renewables Hockliffe Limi... | Central Bedfordshire | 2025-08-14 | 382 | 0.2km/400kV | `12630` | **n** |
| 845 | 58.1 | 90 | bess | PRE_CONSENT | Woodlands, Windermere Road - Battery Energy Storage | Build Studios | County Durham | - | - | 0.3km/275kV | `17574` | y |
| 846 | 58.1 | 42 | solar | PRE_CONSENT | Derril Water Solar Farm - Solar Farm | Renewable Energy System Limited | Torridge | - | - | 0.4km/400kV | `8802` | y |
| 847 | 58.1 | 400 | bess | PRE_CONSENT | Hall Farm, Hickling Lane - Battery Energy Storage | Innova Renewables Developments Lim... | South Norfolk | - | - | 0.0km/132kV | `17940` | y |
| 848 | 58.1 | 25 | solar | PAST_EXPECTED_START | Tuckey Farm | Unknown | Buckinghamshire | 2021-04-29 | 1950 | 0.2km/132kV | `5739` | **n** |
| 849 | 58.1 | 25 | bess | PAST_EXPECTED_START | Middlewich Road - Solar Photovoltaics & Battery Stor... | Cheshire East Council | Cheshire East | 2022-03-11 | 1634 | 0.3km/132kV | `8522` | y |
| 850 | 58.1 | 25 | bess | PAST_EXPECTED_START | Bristol Avenue - Battery Energy Storage Facility | Henco International Limited | Blackpool | 2021-05-11 | 1938 | 0.1km/132kV | `8809` | y |
| 851 | 58.1 | 25 | solar | PAST_EXPECTED_START | Whaddon Lane, Hilperton | British Solar Renewables | Wiltshire | 2022-04-06 | 1608 | 1.7km/400kV | `9057` | y |
| 852 | 58.1 | 25 | solar | PAST_EXPECTED_START | Varley , Talbot End Farm, Cromhall - Solar Farm | RES Limited | South Gloucestershire | 2024-01-24 | 950 | 2.3km/132kV | `11500` | y |
| 853 | 58.0 | 25 | solar | PAST_EXPECTED_START | Southlands Solar Farm & Battery Storage | Enso Green Holdings Limited / Cero... | Chelmsford | 2024-11-26 | 643 | 0.4km/400kV | `13678` | y |
| 854 | 58.0 | 300 | bess | PRE_CONSENT | Leek Road, Werrington - Battery Energy Storage | Masdar Arlington Energy | Staffordshire | - | - | 0.6km/400kV | `19553` | y |
| 855 | 57.9 | 40 | solar | PAST_EXPECTED_START | Minety Substation | JBM Solar Project | Wiltshire | 2022-04-07 | 1607 | 0.2km/400kV | `7942` | y |
| 856 | 57.9 | 40 | bess | PAST_EXPECTED_START | Bicester Road, Launton - Battery Energy Storage | Powersun Limited | Cherwell | 2024-09-05 | 725 | 0.2km/132kV | `16281` | y |
| 857 | 57.9 | 230 | bess | DESIGN_FROZEN_OR_LATER | Uskmouth Power Station - Battery Storage | Simec Atlantic Energy Uskmouth Pow... | Newport | 2022-12-07 | - | 0.3km/132kV | `10936` | y |
| 858 | 57.9 | 24 | solar | PAST_EXPECTED_START | Kirkby Road | Next Power SPV 7 / Intelligent Alt... | Hinckley and Bosworth | 2022-10-22 | 1409 | 1.9km/132kV | `6644` | y |
| 859 | 57.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Neilston Greener Grid Park | Statkraft UK LTD | Renfrewshire | 2022-04-28 | - | 1.9km/132kV | `8830` | y |
| 860 | 57.8 | 50 | bess | PAST_EXPECTED_START | Indian Queens National Grid Substation, Domelick Hil... | EDF Energy Renewables (merged with... | Cornwall | 2024-04-23 | 860 | 0.1km/400kV | `10058` | **n** |
| 861 | 57.8 | 50 | bess | PAST_EXPECTED_START | Indian Queens Sub station, Carne Hill - Battery Ener... | Renewable Connections Development ... | Cornwall | 2023-12-22 | 983 | 0.1km/400kV | `10058` | **n** |
| 862 | 57.8 | 50 | bess | PAST_EXPECTED_START | Ardleigh Road, Little Bromley - Battery Energy Stora... | Lawford Power Limited | Tendring | 2022-09-28 | 1433 | 0.2km/132kV | `10302` | y |
| 863 | 57.8 | 50 | solar | PAST_EXPECTED_START | Fraserburgh Road - Kirkton Solar PV Farm & Energy St... | Elgin Energy Es Co Limited | Scottish Government (S36) | 2022-12-22 | 1348 | 1.4km/132kV | `12823` | y |
| 864 | 57.8 | 50 | bess | PAST_EXPECTED_START | Balwyllo Farm, Dun - Energy Storage Facility | Whirlwind Energy Storage Limited | Angus | 2024-03-13 | 901 | 0.1km/132kV | `13058` | y |
| 865 | 57.8 | 50 | solar | PAST_EXPECTED_START | Worset Lane - Solar Farm | Canadian Solar UK | Hartlepool | 2021-08-26 | 1831 | 1.4km/275kV | `15247` | y |
| 866 | 57.8 | 50 | bess | PAST_EXPECTED_START | New Craigie Retail Park - Battery Energy Storage | Whirlwind Renewables | Dundee City | 2024-05-22 | 831 | 0.5km/132kV | `16018` | y |
| 867 | 57.8 | 50 | bess | PAST_EXPECTED_START | Norwich Substation Storage Facility | Pivot Power | South Norfolk | 2018-11-15 | 2846 | 0.1km/132kV | `7021` | y |
| 868 | 57.8 | 50 | bess | PAST_EXPECTED_START | Middleton Clean Energy Plant | Infra Balance New Energy | Lancaster | 2020-01-17 | 2418 | 0.7km/132kV | `7029` | y |
| 869 | 57.8 | 50 | solar | PAST_EXPECTED_START | South Lowfields Farm | Lightsource BP | North Yorkshire | 2019-12-09 | 2457 | 0.6km/132kV | `7486` | y |
| 870 | 57.8 | 50 | bess | PAST_EXPECTED_START | Newton Wood Farm | Anesco | Bolsover | 2020-10-28 | 2133 | 0.0km/132kV | `7780` | y |
| 871 | 57.8 | 50 | bess | PAST_EXPECTED_START | Reach Road | UK Power Networks | East Cambridgeshire | 2020-07-15 | 2238 | 0.6km/400kV | `7906` | y |
| 872 | 57.8 | 50 | solar | PAST_EXPECTED_START | Camblesforth Solar Farm | Island Green Power UK | North Yorkshire | 2022-07-08 | 1515 | 0.6km/400kV | `8100` | y |
| 873 | 57.8 | 50 | solar | PAST_EXPECTED_START | Elms Farm - Hinckley Solar Farm & Battery Storage | Low Carbon UK Solar Investment Co ... | Rugby | 2022-11-22 | 1378 | 0.3km/132kV | `8508` | y |
| 874 | 57.8 | 50 | solar | PAST_EXPECTED_START | Colton Mill Farm & Cawarden Springs Farm - Solar Pan... | Spring Dev 07 Limited | Lichfield | 2021-11-01 | 1764 | 0.6km/132kV | `8813` | y |
| 875 | 57.8 | 50 | bess | PAST_EXPECTED_START | Moreton Lane - Solar Farm & Battery Storage | JBM Solar Projects 7 Limited | Stroud | 2022-04-05 | 1609 | 0.8km/132kV | `8843` | y |
| 876 | 57.8 | 50 | solar | PAST_EXPECTED_START | Moreton Lane - Solar Farm & Battery Storage | JBM Solar Projects 7 Limited | Stroud | 2022-04-05 | 1609 | 0.8km/132kV | `8844` | y |
| 877 | 57.8 | 50 | bess | PAST_EXPECTED_START | Newhouse Farm - Energy Storage Facility | Intelligent Land Investments Group | Perth and Kinross | 2023-01-27 | 1312 | 0.7km/132kV | `9047` | y |
| 878 | 57.8 | 50 | solar | PAST_EXPECTED_START | Os Field 6800 Fence Dike Lane - Solar Farm | Lightrock Power Limited | North Yorkshire | 2023-06-27 | 1161 | 1.8km/132kV | `9212` | y |
| 879 | 57.8 | 50 | solar | PAST_EXPECTED_START | Estuary Farm, Edward Benefer Way - Solar Farm & Batt... | Namene Solar | King's Lynn and West Norfolk | 2021-12-08 | 1727 | 0.6km/132kV | `9346` | y |
| 880 | 57.8 | 50 | solar | PAST_EXPECTED_START | Yearby Village - Tees Solar Farm | EDF Energy Renewables | Redcar and Cleveland | 2024-04-30 | 853 | 3.0km/400kV | `9353` | y |
| 881 | 57.8 | 50 | solar | PAST_EXPECTED_START | The Old Airfield Solar Photovoltaic Farm | Grey Street Solar Limited | West Lindsey | 2021-05-27 | 1922 | 2.1km/132kV | `9575` | y |
| 882 | 57.8 | 50 | solar | PAST_EXPECTED_START | Black Flatts Solar Farm | Opdenergy UK 2 Limited | Lichfield | 2022-05-10 | 1574 | 1.6km/132kV | `9776` | y |
| 883 | 57.8 | 50 | solar | PAST_EXPECTED_START | Hawthorn Pit -Solar Farm | Aura Power Developments Limited | County Durham | 2023-05-25 | 1194 | 0.4km/275kV | `9799` | y |
| 884 | 57.8 | 50 | bess | PAST_EXPECTED_START | Stainland Energy Storage Project | Whirlwind Energy Storage Limited | Highland | 2022-11-04 | 1396 | 1.1km/275kV | `10225` | y |
| 885 | 57.8 | 50 | bess | PAST_EXPECTED_START | Model Farm | Tribus Clean Energy | King's Lynn and West Norfolk | 2022-01-27 | 1677 | 0.1km/132kV | `10687` | y |
| 886 | 57.8 | 50 | solar | PAST_EXPECTED_START | Studley Farm - Solar Farm & Battery Storage | Melksham Calne Green Limited | Wiltshire | 2022-06-09 | 1544 | 0.2km/132kV | `12864` | y |
| 887 | 57.8 | 50 | bess | PAST_EXPECTED_START | Landulph Substation, Ellbridge Lane - Battery Energy... | Conrad Energy | Cornwall | 2023-09-05 | 1091 | 0.2km/400kV | `13461` | y |
| 888 | 57.8 | 50 | solar | PAST_EXPECTED_START | Immingham Solar Farm - Solar Farm | One Planet Developments Limited | North East Lincolnshire | 2025-05-06 | 482 | 0.9km/132kV | `16091` | y |
| 889 | 57.8 | 50 | solar | PAST_EXPECTED_START | Creyke Beck Substation - Solar Farm & Battery Storag... | Albanwise Synergy Limited | East Riding of Yorkshire | 2022-01-06 | 1698 | 0.6km/132kV | `17072` | y |
| 890 | 57.8 | 50 | bess | PAST_EXPECTED_START | Rye Common | Pulse Clean Energy | Hart | 2021-09-28 | 1798 | 0.3km/132kV | `7028` | **n** |
| 891 | 57.8 | 50 | bess | PAST_EXPECTED_START | Well Street - Battery Storage | Larkfleet Group | Renfrewshire | 2023-05-23 | 1196 | 1.9km/132kV | `11473` | y |
| 892 | 57.7 | 49 | bess | PAST_EXPECTED_START | Cottam Power Station | EDF Energy | Bassetlaw | 2020-11-16 | 2114 | 0.0km/400kV | `7066` | y |
| 893 | 57.7 | 49 | bess | PAST_EXPECTED_START | Wester Balbeggie Farm, Balbeggie Avenue - Battery St... | Relay Balbeggie Limited | Fife | 2023-08-17 | 1110 | 0.4km/132kV | `12350` | y |
| 894 | 57.7 | 22 | solar | PAST_EXPECTED_START | Four Ashes, Deepmore Lane - Solar Farm | Renewable Connections | South Staffordshire | 2024-07-17 | 775 | 0.8km/400kV | `15224` | y |
| 895 | 57.6 | 10 | bess | PAST_EXPECTED_START | Midland Quarry Products, Smith Road - Battery Storag... | Gresham House Devco Pipeline Limit... | Sandwell | 2025-01-31 | 577 | 0.2km/275kV | `14747` | y |
| 896 | 57.6 | 10 | solar | PAST_EXPECTED_START | Stanborough, Hatfield - Solar Array | J Reddington Limited | Welwyn Hatfield | 2024-09-16 | 714 | 0.9km/132kV | `14877` | y |
| 897 | 57.6 | 10 | bess | PAST_EXPECTED_START | Wharf Road, Discovery Park - Battery Energy Storage | Kent Renewable Energy Limited | Dover | 2024-11-11 | 658 | 1.9km/132kV | `15093` | y |
| 898 | 57.6 | 10 | solar | PAST_EXPECTED_START | Kirkgate Lane, Felkirk - Solar Array | Kirkgate Lane Solar Farm Limited | Wakefield | 2025-04-10 | 508 | 0.9km/400kV | `15166` | y |
| 899 | 57.6 | 10 | solar | PAST_EXPECTED_START | Great Cowbridge Grange Farm, London Road - Solar Far... | Conrad Energy (Developments) Limit... | Basildon | 2025-05-01 | 487 | 1.3km/132kV | `17349` | y |
| 900 | 57.6 | 48 | bess | PAST_EXPECTED_START | Indian Queens Sub-Station - Battery Storage | Prime Energy Development Limited /... | Cornwall | 2022-10-17 | 1414 | 0.4km/400kV | `11725` | y |
| 901 | 57.6 | 100 | bess | PAST_EXPECTED_START | Third Energy UK Gas Limited - Battery Energy Storage | Third Energy | North Yorkshire | 2021-10-14 | 1782 | 0.0km/132kV | `9691` | y |
| 902 | 57.6 | 349 | bess | PRE_CONSENT | Cellarhead - Battery Site | C&S Energy Limited | Staffordshire Moorlands | - | - | 0.2km/400kV | `12179` | y |
| 903 | 57.6 | 100 | bess | DESIGN_FROZEN_OR_LATER | Freshfields, Fairy Lane - Battery Storage | STOR Power Utilities Limited | Trafford | 2023-03-20 | - | 0.1km/275kV | `12694` | y |
| 904 | 57.5 | 4 | bess | PROCURING | Barnard Castle - Solar Farm & Battery Storage System | Farm Energy Company | County Durham | 2025-06-10 | 447 | 16.7km/132kV | `14839` | y |
| 905 | 57.5 | 4 | solar | PAST_EXPECTED_START | Ditton Road - Solar Microgrid | Halton Borough Council | Halton | 2025-01-23 | 585 | 0.2km/132kV | `16673` | y |
| 906 | 57.4 | 16 | solar | PAST_EXPECTED_START | Kerswell Barton Farm, Broadclyst - Solar Panels | MJ Quinn Integrated Services Limit... | East Devon | 2025-08-07 | 389 | 1.0km/132kV | `18518` | y |
| 907 | 57.4 | 21 | solar | PAST_EXPECTED_START | Wicken Farm, Leckhampstead - Solar Farm | Opdenergy UK 2 Limited | Buckinghamshire | 2023-12-14 | 991 | 1.9km/400kV | `10435` | y |
| 908 | 57.4 | 35 | solar | PRE_CONSENT | Pencoed Ganol Farm, Pendderi Road - Solar Panels | Windel Solar 11 Limited | Welsh Government (NSIP) | - | - | 0.5km/132kV | `18181` | y |
| 909 | 57.4 | 16 | solar | PAST_EXPECTED_START | Martin Farm, St. Marys Road - Solar Panels | Enviromena Project Management UK L... | Folkestone and Hythe | 2026-01-23 | 220 | 1.9km/400kV | `18718` | y |
| 910 | 57.4 | 9 | solar | PAST_EXPECTED_START | Jaguar Land Rover Jaguar Plant, North Road - Solar P... | Jaguar Land Rover | Knowsley | 2025-02-25 | 552 | 0.5km/132kV | `17836` | y |
| 911 | 57.4 | 95 | bess | PAST_EXPECTED_START | Winterton Road - Battery Energy Storage | Newton Energi Limited | North Lincolnshire | 2022-12-16 | 1354 | 0.3km/132kV | `9608` | y |
| 912 | 57.3 | 9 | solar | PAST_EXPECTED_START | Parcel 2882, Water Lane - Solar Farm | Pathfinder Clean Energy UK Dev Lim... | Bath and North East Somerset | 2025-06-05 | 452 | 1.3km/132kV | `17422` | y |
| 913 | 57.3 | 20 | bess | PAST_EXPECTED_START | Vicarage Drove - Solar farm & Battery storage | Renewable Connections Developments... | Boston | 2024-01-23 | 951 | 0.0km/132kV | `8517` | y |
| 914 | 57.3 | 200 | bess | DESIGN_FROZEN_OR_LATER | Soay Solar Farm and Greener Grid Park | Statkraft Uk Limited | East Riding of Yorkshire | 2022-11-28 | - | 1.1km/400kV | `9014` | y |
| 915 | 57.3 | 9 | solar | PAST_EXPECTED_START | North Moss Lane - Solar Photovoltaic Farm | Taiyo Power & Storage Limited | Sefton | 2025-08-07 | 389 | 1.6km/132kV | `15491` | **n** |
| 916 | 57.2 | 20 | bess | PAST_EXPECTED_START | John Green Frog Power Compound, John North Road - Ba... | Green Frog Power Limited | Swansea | 2023-01-20 | 1319 | 0.0km/132kV | `12455` | y |
| 917 | 57.2 | 20 | solar | PAST_EXPECTED_START | Suncoast Solar Farm | Low Carbon Solar Park 20 Limited | Eastbourne | 2025-02-19 | 558 | 0.8km/132kV | `14403` | y |
| 918 | 57.2 | 20 | bess | PAST_EXPECTED_START | Heron Solar Farm & Battery Storage | JBM Solar Projects 38 Limited | Rushcliffe | 2024-08-27 | 734 | 0.1km/400kV | `15083` | y |
| 919 | 57.2 | 20 | solar | PAST_EXPECTED_START | Heron Solar Farm & Battery Storage | JBM Solar Projects 38 Limited | Rushcliffe | 2024-08-27 | 734 | 0.1km/400kV | `15084` | y |
| 920 | 57.2 | 43 | bess | PAST_EXPECTED_START | Ballingall Farm, Leslie - Battery Energy Storage Sys... | EcoDev Group Limited | Fife | 2023-09-14 | 1082 | 0.5km/275kV | `10825` | y |
| 921 | 57.2 | 43 | solar | PAST_EXPECTED_START | High Marnham - Solar Photovoltaic Farm | J G Pears Property Limited | Bassetlaw | 2023-01-05 | 1334 | 0.3km/275kV | `11392` | y |
| 922 | 57.2 | 9 | solar | PAST_EXPECTED_START | St Marys C Of E Va High School, Lieutenant Ellis Way... | eEnergy | Broxbourne | 2025-07-01 | 426 | 0.5km/132kV | `18739` | y |
| 923 | 57.2 | 150 | bess | PRE_CONSENT | Bishops Dal - Battery Energy Storage System | Renewable Energy Systems RES Limit... | Scottish Government (S36) | - | - | 0.4km/400kV | `16787` | y |
| 924 | 57.2 | 1 | solar | PAST_EXPECTED_START | Kinneil Kerse Wastewater Treatment Works - Solar PV ... | Scottish Water | West Lothian | 2026-01-23 | 220 | 1.7km/275kV | `18818` | **n** |
| 925 | 57.1 | 70 | bess | PAST_EXPECTED_START | Sale Golf Club, Golf Road - Battery Storage | 247 Power Limited | Trafford | 2023-11-17 | 1018 | 0.2km/275kV | `13731` | y |
| 926 | 57.1 | 70 | bess | PRE_CONSENT | Benton Green Lane - Battery Energy Storage System | Tamara Ettenfield | Solihull | - | - | 0.7km/275kV | `18680` | y |
| 927 | 57.1 | 400 | bess | DESIGN_FROZEN_OR_LATER | Eccles Battery Energy Storage System | Zenobe Energy Limited | Scottish Government (S36) | 2023-08-11 | - | 0.1km/400kV | `11867` | y |
| 928 | 57.1 | 25 | solar | PAST_EXPECTED_START | Denhead - Solar Array | Muirden Energy | Aberdeenshire | 2024-04-18 | 865 | 1.2km/132kV | `12161` | y |
| 929 | 57.0 | 14 | solar | PAST_EXPECTED_START | Lodge Hill, Berkley - Solar Park | Wessex Solar Energy Limited | Somerset | 2022-10-21 | 1410 | 1.5km/400kV | `6797` | y |
| 930 | 57.0 | 1000 | bess | PRE_CONSENT | Canners Lane Energy Park, High Dike - Battery Energy... | NatPower UK | North Kesteven | - | - | 0.7km/132kV | `18652` | y |
| 931 | 57.0 | 500 | bess | PRE_CONSENT | Abbotshaugh Battery Storage | Island Green Power (IGP Solar 25 L... | Scottish Government (S36) | - | - | 0.3km/400kV | `17552` | y |
| 932 | 57.0 | 500 | bess | PRE_CONSENT | Tyn Y Coed - Battery Energy Storage System | NatPower UK | Flintshire | - | - | 1.4km/132kV | `19130` | y |
| 933 | 57.0 | 19 | solar | PAST_EXPECTED_START | Codrington Road - Solar Photovoltaic Panels | Renewable Connections Limited | South Gloucestershire | 2023-08-11 | 1116 | 0.3km/400kV | `11693` | y |
| 934 | 57.0 | 8 | solar | PAST_EXPECTED_START | Glyngwernen Farm, Uchaf Fawr - Solar Farm | Bartypower Limited | Carmarthenshire | 2025-02-17 | 560 | 1.1km/132kV | `16839` | y |
| 935 | 57.0 | 300 | bess | PRE_CONSENT | Staythorpe Road, Averham - Battery Storage | SSE Battery Storage Limited | Newark and Sherwood | - | - | 0.4km/132kV | `12893` | y |
| 936 | 56.9 | 40 | bess | PAST_EXPECTED_START | Maldon Hall | Green Investment Group | Maldon | 2019-05-13 | 2667 | 1.0km/132kV | `7095` | y |
| 937 | 56.9 | 40 | solar | PAST_EXPECTED_START | Tycroes Solar Farm | Spring Dev 2 | Welsh Government (NSIP) | 2021-08-12 | 1845 | 1.3km/132kV | `7469` | y |
| 938 | 56.9 | 40 | bess | PAST_EXPECTED_START | Dalmarnock Road - Battery Storage | EcoDev Group Limited | South Lanarkshire | 2022-02-16 | 1657 | 0.1km/275kV | `8507` | y |
| 939 | 56.9 | 40 | solar | PAST_EXPECTED_START | North Fossil Farm - Solar Panels | Spring Dev 03 Ltd | Dorset | 2022-01-12 | 1692 | 1.4km/132kV | `8828` | y |
| 940 | 56.9 | 40 | bess | PAST_EXPECTED_START | Field House Solar Farm | Albanwise Synergy Limited | East Riding of Yorkshire | 2022-07-08 | 1515 | 0.9km/132kV | `8995` | y |
| 941 | 56.9 | 40 | solar | PAST_EXPECTED_START | Field House Solar Farm | Albanwise Synergy Limited | East Riding of Yorkshire | 2022-07-08 | 1515 | 0.9km/132kV | `8995` | y |
| 942 | 56.9 | 40 | bess | PAST_EXPECTED_START | Hollydale, Buildwas Road - Battery Storage | Telford Four Limited | Shropshire | 2024-01-12 | 962 | 0.2km/400kV | `13410` | y |
| 943 | 56.9 | 40 | bess | PAST_EXPECTED_START | Locarno Works, Brown Street - Battery Storage | Torridon Developments Limited | Dundee City | 2024-06-19 | 803 | 0.1km/132kV | `14232` | y |
| 944 | 56.9 | 140 | bess | PRE_CONSENT | Maydown Road - Battery Energy Storage System | Electric Land | Derry City and Strabane | - | - | 0.2km/275kV | `17882` | y |
| 945 | 56.8 | 65 | bess | PRE_CONSENT | Ceislein Wind Farm | RWE Renewables UK Limited | Scottish Government (S36) | - | - | 1.4km/132kV | `17100` | y |
| 946 | 56.8 | 138 | solar | PAST_EXPECTED_START | Oaklands Solar Farm Project - Solar Farm & Battery S... | BayWa r.e. UK Limited | The Planning Inspectorate - ... | 2025-06-19 | 438 | 0.4km/132kV | `9547` | y |
| 947 | 56.8 | 18 | bess | PAST_EXPECTED_START | Whaddon Lane, Hilperton | British Solar Renewables | Wiltshire | 2022-04-06 | 1608 | 1.7km/400kV | `9056` | y |
| 948 | 56.8 | 18 | solar | PAST_EXPECTED_START | Parkhill Farm, Letham Grange - Solar Farm | AlphaReal | Angus | 2023-12-19 | 986 | 4.4km/132kV | `12495` | y |
| 949 | 56.8 | 480 | bess | PRE_CONSENT | Elkesley Southbound, Elkesley - Battery Energy Stora... | Mespil Solar Energy | Bassetlaw | - | - | 1.4km/275kV | `18343` | y |
| 950 | 56.8 | 30 | solar | PAST_EXPECTED_START | Copper Bottom Solar Farm Ground-Mounted Solar PV Arr... | Aura Power Storage Solutions | Cornwall | 2024-07-18 | 774 | 0.1km/132kV | `8349` | y |
| 951 | 56.8 | 30 | bess | PAST_EXPECTED_START | Burnbank Street, Greenhill - Battery Storage Facilit... | Renewable Connections Developments... | North Lanarkshire | 2024-08-20 | 741 | 2.0km/275kV | `9368` | y |
| 952 | 56.8 | 30 | solar | PRE_CONSENT | Moorhouse Grange, Moorhouse Lane - Solar Farm | Zetland Group | Doncaster | - | - | 0.3km/275kV | `16233` | y |
| 953 | 56.8 | 30 | solar | PAST_EXPECTED_START | Westfield Solar Farm & Battery | Brockwell Energy Limited | Fife | 2021-02-12 | 2026 | 0.3km/275kV | `20392` | y |
| 954 | 56.8 | 50 | bess | CONSENTED_NO_DATE | Ravensroost Farm, Minety - Battery Energy Storage | Conrad Energy Developments II Limi... | Wiltshire | - | - | 0.3km/132kV | `7014` | y |
| 955 | 56.8 | 50 | solar | PAST_EXPECTED_START | Upper Leigh Solar Farm | Lightrock Power | Staffordshire Moorlands | 2024-04-02 | 881 | 0.7km/400kV | `19366` | y |
| 956 | 56.8 | 50 | bess | PRE_CONSENT | Leadhills Road, Elvanfoot Phase 2 - BESS | Elvanfoot Energy Storage 2 Limited | South Lanarkshire | - | - | 0.3km/400kV | `20588` | y |
| 957 | 56.7 | 360 | bess | DESIGN_FROZEN_OR_LATER | Staythorpe Road - Battery energy storage | Ecap Renewables (Elements Green) | Newark and Sherwood | 2024-05-03 | - | 0.4km/132kV | `11553` | **n** |
| 958 | 56.6 | 3 | solar | PAST_EXPECTED_START | IGC, Lydia Becker Way - Solar Panels | Ashcroft Electrical Services Limit... | Oldham | 2025-09-11 | 354 | 0.7km/132kV | `19482` | y |
| 959 | 56.6 | 48 | bess | PAST_EXPECTED_START | Holt Road - Battery Energy Storage | EDF Energy Renewables | Dorset | 2024-07-29 | 763 | 0.4km/400kV | `15470` | y |
| 960 | 56.6 | 130 | bess | PRE_CONSENT | Pashley Farm, Ninfield Road - Battery Energy Storage... | Elgin Energy Esco Limited | Wealden | - | - | 0.3km/132kV | `19142` | y |
| 961 | 56.6 | 100 | bess | PRE_CONSENT | East Park Energy | Brockwell Energy | The Planning Inspectorate - ... | - | - | 1.0km/400kV | `15347` | y |
| 962 | 56.6 | 100 | bess | PRE_CONSENT | Former Fife Power Station - Battery Energy Storage S... | Fife Power 1 Ltd | Scottish Government (S36) | - | - | 0.0km/275kV | `17018` | y |
| 963 | 56.6 | 100 | bess | PRE_CONSENT | Neil Fox Way - Battery Storage | Harmony Energy Limited | Wakefield | - | - | 0.1km/132kV | `11519` | y |
| 964 | 56.5 | 28 | solar | PAST_EXPECTED_START | Pyotdykes Farm, Stoneygroves, Liff - Solar Farm | Sonnedix Weston Limited | Angus | 2024-03-13 | 901 | 0.2km/132kV | `11847` | y |
| 965 | 56.5 | 28 | solar | PAST_EXPECTED_START | Spencers Wood Solar Farm, Basingstoke Road - Solar A... | Greentech | Wokingham | 2025-03-26 | 523 | 3.1km/132kV | `15460` | y |
| 966 | 56.5 | 28 | bess | PRE_CONSENT | Upper Pant-Ysgawen Farm, Maes-Yr-Haf Lane - Battery ... | Voltwise Power Holdings Limited | Caerphilly | - | - | 0.4km/132kV | `19387` | y |
| 967 | 56.5 | 60 | bess | PRE_CONSENT | Roaring Hill, Whinnyknowe - Battery Energy Storage S... | ELM Power Limited | Scottish Government (S36) | - | - | 0.4km/275kV | `16676` | y |
| 968 | 56.5 | 36 | bess | PAST_EXPECTED_START | Lisnabreeny Road | Energia Group | Lisburn and Castlereagh | 2019-06-21 | 2628 | 1.1km/275kV | `7556` | y |
| 969 | 56.5 | 99 | bess | PRE_CONSENT | Westfield Conservation Park - Battery Energy Storage... | Lightrock Power Limited | North Hertfordshire | - | - | 1.8km/400kV | `19668` | y |
| 970 | 56.5 | 12 | solar | PAST_EXPECTED_START | Hatherton Lodge Farm, Hunsterson Road - Solar Farm | Noventum Power Limited | Cheshire East | 2025-06-19 | 438 | 1.9km/132kV | `14524` | y |
| 971 | 56.4 | 35 | bess | PAST_EXPECTED_START | Patch Elm Lane - Battery Storage | Green Frog Ventures Limited | South Gloucestershire | 2022-03-18 | 1627 | 0.5km/132kV | `11415` | y |
| 972 | 56.4 | 35 | bess | PAST_EXPECTED_START | New Barn Road - Battery Energy Storage Facility | Aton Energy Development (Northflee... | Dartford | 2024-02-15 | 928 | 0.1km/400kV | `14650` | y |
| 973 | 56.4 | 45 | solar | PAST_EXPECTED_START | Land at Pen Onn - Solar Farm | Iolo Energy | Welsh Government (NSIP) | 2025-05-29 | 459 | 0.7km/132kV | `10909` | y |
| 974 | 56.4 | 16 | bess | PAST_EXPECTED_START | Little Llwyn Onn - Solar Farm & Battery Storage | Novus Renewable Services Limited | Wrexham | 2023-03-08 | 1272 | 1.0km/132kV | `11543` | y |
| 975 | 56.4 | 16 | solar | PAST_EXPECTED_START | Bretton Hall Solar Farm (Wales) | YnNi Newydd (New Energy Co-op) | Welsh Government (NSIP) | 2023-12-19 | 986 | 1.5km/132kV | `11633` | y |
| 976 | 56.4 | 16 | solar | PAST_EXPECTED_START | Vauls Farm, Astley Lane - Solar Farm | Industria Solar Bedworth Limited | North Warwickshire | 2023-07-19 | 1139 | 0.8km/400kV | `12647` | y |
| 977 | 56.3 | 57 | bess | PAST_EXPECTED_START | Sellindge Substation, Church Lane - Battery Storage | Pivoted Power Llp | Ashford | 2023-08-04 | 1123 | 0.0km/400kV | `12351` | y |
| 978 | 56.3 | 57 | bess | PRE_CONSENT | Beechwood Farm, Hodgetts Lane - Battery Storage | Enso Energy Limited | Solihull | - | - | 0.4km/275kV | `16855` | y |
| 979 | 56.3 | 57 | bess | PRE_CONSENT | Stevenage Road, Titmore Green - Battery Energy Stora... | Pivoted Power Llp | North Hertfordshire | - | - | 0.3km/400kV | `19189` | y |
| 980 | 56.3 | 34 | solar | PAST_EXPECTED_START | Nottingham Road - Solar Farm | NextPower SPV 9 Limited | Charnwood | 2023-03-30 | 1250 | 0.2km/400kV | `10097` | **n** |
| 981 | 56.2 | 20 | solar | PAST_EXPECTED_START | Sherbourne Warwick Solar (Hampton Lodge) | Pelagic Energy Development | Warwick | 2023-09-25 | 1071 | 5.2km/132kV | `11447` | y |
| 982 | 56.2 | 26 | solar | PAST_EXPECTED_START | Bloomfield Hatch Farm - Solar Farm & Battery | Horizon Power & Energy Limited | West Berkshire | 2022-09-02 | 1459 | 0.4km/132kV | `10814` | y |
| 983 | 56.2 | 33 | solar | PAST_EXPECTED_START | Whinfield Solar Farm | Alpha Real Capital LLP | Darlington | 2022-10-04 | 1427 | 3.8km/132kV | `12339` | y |
| 984 | 56.1 | 15 | bess | PAST_EXPECTED_START | Newburgh Road, Abernethy - Energy Storage | Centrica Business Solutions | Perth and Kinross | 2023-03-29 | 1251 | 0.3km/132kV | `13111` | y |
| 985 | 56.1 | 400 | bess | PRE_CONSENT | Green Man Road, Navenby - Battery Storage | Windel Energy / Canadian Solar | North Kesteven | - | - | 1.1km/400kV | `13977` | y |
| 986 | 56.1 | 400 | bess | PRE_CONSENT | Market Lane And Carr Lane, Great Moulton - Battery E... | Field Long Stratton Limited | South Norfolk | - | - | 1.0km/400kV | `18554` | y |
| 987 | 56.1 | 400 | bess | PRE_CONSENT | Polly Taylors Road, High Marnham - Battery Energy St... | Field Energy | Bassetlaw | - | - | 0.4km/275kV | `18638` | y |
| 988 | 56.1 | 25 | solar | PAST_EXPECTED_START | Strathruddie, Kinglassie - Solar farm | Renewable Connection Developments ... | Fife | 2022-03-16 | 1629 | 0.2km/132kV | `10828` | y |
| 989 | 56.1 | 25 | solar | PRE_CONSENT | Claymills Sewage Treatment Works, Meadow Lane - Sola... | Wetmore Solar Limited | East Staffordshire | - | - | 0.6km/132kV | `15698` | y |
| 990 | 56.0 | 24 | solar | PAST_EXPECTED_START | Sandbay, Elmsley Lane, Kewstoke - Solar Farm | Solar Southwest | North Somerset | 2024-10-03 | 697 | 2.9km/132kV | `13293` | y |
| 991 | 56.0 | 1000 | bess | PRE_CONSENT | Old Rides Farm, Leysdown Road - Battery Energy Stora... | Nat Power | Swale | - | - | 6.7km/400kV | `18601` | y |
| 992 | 56.0 | 600 | solar | PAST_EXPECTED_START | Cottam Solar Project | Island Green Power | The Planning Inspectorate - ... | 2024-09-05 | 725 | 5.4km/132kV | `10915` | y |
| 993 | 55.9 | 31 | solar | PAST_EXPECTED_START | Storridge Road - Solar Farm | NextPower SPV 15 Limited | Wiltshire | 2023-10-12 | 1054 | 0.6km/400kV | `10515` | y |
| 994 | 55.9 | 31 | solar | PAST_EXPECTED_START | Suttieside Farm, Suttieside Road - Solar Farm & Batt... | Relay Suttieside Limited | Angus | 2023-12-13 | 992 | 0.6km/132kV | `12214` | y |
| 995 | 55.9 | 40 | solar | PAST_EXPECTED_START | Red Barn - Solar Farm & Battery Storage | Eden Renewables | Wiltshire | 2025-01-27 | 581 | 1.9km/400kV | `15146` | y |
| 996 | 55.9 | 6 | solar | PAST_EXPECTED_START | Etex Building Performance, Redland Avenue - Solar Pa... | PROMAT UK/Etex Building Performanc... | North Somerset | 2024-12-30 | 609 | 0.6km/132kV | `17616` | y |
| 997 | 55.9 | 14 | solar | PAST_EXPECTED_START | Bretton Hall Solar Farm (England) | YnNi Newydd (New Energy Co-op) | Flintshire | 2023-10-12 | 1054 | 1.6km/132kV | `11634` | y |
| 998 | 55.9 | 14 | bess | PAST_EXPECTED_START | St Michaels Road, Ditton Road - Battery Storage | Shell Green Limited | Halton | 2023-10-27 | 1039 | 0.1km/132kV | `12904` | y |
| 999 | 55.9 | 14 | solar | PAST_EXPECTED_START | Dogsthorpe, Welland Road - Solar Farm & Battery Stor... | Infinis Solar Developments Limited | Peterborough | 2024-06-21 | 801 | 1.5km/132kV | `13027` | y |
| 1000 | 55.8 | 6 | bess | PAST_EXPECTED_START | Lime Kilns Energy Centre - Battery Energy Storage | Flexitricity | Thurrock | 2024-12-19 | 620 | 0.6km/132kV | `17397` | y |
| 1001 | 55.8 | 50 | bess | PAST_EXPECTED_START | Dersalloch Battery Storage Facility | Scottish Power Renewables (UK) Lim... | Scottish Government (S36) | 2021-11-29 | 1736 | 0.6km/132kV | `8927` | y |
| 1002 | 55.8 | 50 | solar | PAST_EXPECTED_START | Little Staughton Solar Farm | Nextpower SPV 12 Limited | Huntingdonshire | 2024-12-04 | 635 | 12.9km/132kV | `8991` | y |
| 1003 | 55.8 | 50 | bess | PAST_EXPECTED_START | Nutsgrove Farm, Thorney - Battery Energy Storage | Cambridge Power Limited | Peterborough | 2024-06-28 | 794 | 1.8km/132kV | `9975` | y |
| 1004 | 55.8 | 50 | bess | PAST_EXPECTED_START | Electricity Sub Station, Strichen - Battery Storage ... | Intelligent Land Investments Group... | Aberdeenshire | 2022-03-01 | 1644 | 0.3km/132kV | `10039` | y |
| 1005 | 55.8 | 50 | bess | PAST_EXPECTED_START | Greenbank Caravan & Trailers, Hillhead Of Phingask -... | Flexion Energy UK Storage | Aberdeenshire | 2023-01-30 | 1309 | 1.2km/132kV | `12303` | y |
| 1006 | 55.8 | 50 | bess | PAST_EXPECTED_START | Levedale Road, Levedale - Battery Energy Storage | Anglo Renewables Limited | South Staffordshire | 2024-12-06 | 633 | 0.5km/132kV | `13615` | y |
| 1007 | 55.8 | 50 | bess | PAST_EXPECTED_START | Low Horton - Battery Energy Storage System | Bluefield Renewable Developments L... | Northumberland | 2025-01-10 | 598 | 0.7km/275kV | `15753` | y |
| 1008 | 55.8 | 50 | bess | PRE_CONSENT | Thurcroft Interchange Energy Park - Battery Energy S... | Exagen | Rotherham | - | - | 0.2km/275kV | `18532` | y |
| 1009 | 55.8 | 50 | bess | PRE_CONSENT | Higher Bagmore Farm, Ebford Lane -Battery Energy Sto... | Enviromena | East Devon | - | - | 0.3km/132kV | `19391` | y |
| 1010 | 55.8 | 50 | bess | PRE_CONSENT | Roosecote Power Station, Rampside Road - Battery Ene... | Centrica Plc | Westmorland and Furness | - | - | 0.1km/132kV | `19570` | y |
| 1011 | 55.8 | 50 | solar | PAST_EXPECTED_START | Gately Moor Reservoir, Redmarshall - Solar Farm & Ba... | Canadian Solar & Novergy | Stockton-on-Tees | 2022-11-23 | 1377 | 0.0km/132kV | `11692` | y |
| 1012 | 55.8 | 50 | bess | PRE_CONSENT | Bulworthy Farm, Stoney Cross - Solar Photovoltaic Ar... | Noventum Power Limited | Torridge | - | - | 0.3km/400kV | `17883` | y |
| 1013 | 55.8 | 30 | bess | PAST_EXPECTED_START | North Tawton Primary Substation - Battery Storage | Balance Power Projects Limited | West Devon | 2021-11-03 | 1762 | 0.1km/132kV | `9275` | y |
| 1014 | 55.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Great Wheatley Road - Solar Farm | Aura Power Solar UK Limited | Rochford | 2024-03-11 | - | 0.8km/132kV | `9802` | y |
| 1015 | 55.8 | 30 | bess | PAST_EXPECTED_START | Catsbrain Farm - Battery Storage | Conrad Energy (Developments) II Li... | Swindon | 2023-10-03 | 1063 | 0.6km/132kV | `11787` | y |
| 1016 | 55.8 | 50 | solar | PAST_EXPECTED_START | Jericho Covert Solar Farm | Green Farm Solar Limited | Melton | 2022-08-19 | 1473 | 1.4km/132kV | `8227` | y |
| 1017 | 55.8 | 50 | solar | PAST_EXPECTED_START | Leaps Rigg - Solar Farm | Opdenergy UK 7 Limited | Cumberland | 2023-09-28 | 1068 | 0.3km/132kV | `8526` | y |
| 1018 | 55.8 | 50 | solar | PAST_EXPECTED_START | Canewdon Road, Canewdon - Solar Photovoltaic Farm | Low Carbon UK Solar Investment Com... | Rochford | 2024-01-11 | 963 | 0.3km/132kV | `9808` | y |
| 1019 | 55.8 | 50 | bess | PAST_EXPECTED_START | Drum Farm - Battery Energy Storage System | Field Energy | Moray | 2022-10-27 | 1404 | 0.4km/132kV | `9940` | y |
| 1020 | 55.8 | 50 | solar | PAST_EXPECTED_START | Nutsgrove Farm, Thorney - Solar Array | Cambridge Power Limited | Peterborough | 2024-06-28 | 794 | 1.8km/132kV | `9976` | y |
| 1021 | 55.8 | 50 | bess | PAST_EXPECTED_START | Fordtown Energy Storage | Private Developer | Aberdeenshire | 2021-02-24 | 2014 | 0.3km/132kV | `10239` | y |
| 1022 | 55.8 | 50 | bess | PAST_EXPECTED_START | Law Of Doune Road, Macduff - Battery Storage | Intelligent Land Investments Group... | Aberdeenshire | 2023-12-05 | 1000 | 0.3km/132kV | `10894` | y |
| 1023 | 55.8 | 50 | solar | PAST_EXPECTED_START | Copse Close Solar Farm | Copse Close Solar Farm Limited | East Hampshire | 2023-02-06 | 1302 | 0.3km/132kV | `10952` | y |
| 1024 | 55.8 | 50 | solar | PAST_EXPECTED_START | Dean Hill Road - Solar Farm | Low Carbon Storage Ireland | Mid Devon | 2023-11-30 | 1005 | 0.3km/400kV | `11753` | y |
| 1025 | 55.8 | 50 | solar | PAST_EXPECTED_START | Sunderlandwick Solar Farm | Elgin Energy EsCo Limited | East Riding of Yorkshire | 2023-04-21 | 1228 | 1.1km/132kV | `12008` | y |
| 1026 | 55.8 | 50 | bess | PAST_EXPECTED_START | Meetlaw Farm, Fordoun - Battery Energy Storage Syste... | One Planet Developments Limited | Aberdeenshire | 2023-09-19 | 1077 | 0.3km/275kV | `12361` | y |
| 1027 | 55.8 | 50 | bess | PAST_EXPECTED_START | Electricity Substation, Westerton Road - Battery Sto... | Keith Renewables Limited | Moray | 2023-03-15 | 1265 | 0.1km/132kV | `12467` | y |
| 1028 | 55.8 | 50 | solar | PAST_EXPECTED_START | Meerdyke Solar Panels & Battery Storage | Downing Renewable Developments Llp | King's Lynn and West Norfolk | 2024-03-06 | 908 | 0.3km/400kV | `12718` | y |
| 1029 | 55.8 | 50 | solar | PAST_EXPECTED_START | Long Pasture Farm, Little Stainton - Solar Farm | Electric Works | Darlington | 2023-08-10 | 1117 | 0.5km/132kV | `12952` | y |
| 1030 | 55.8 | 50 | bess | PRE_CONSENT | Hodgetts Lane, Berkswell - Electricity Storage Facil... | Coventry Energy Storage Limited | Solihull | - | - | 0.2km/132kV | `15230` | y |
| 1031 | 55.8 | 50 | bess | PRE_CONSENT | Govan Battery Energy Storage System | Vital Energi Utilities Limited | Glasgow City | - | - | 0.1km/132kV | `18260` | y |
| 1032 | 55.8 | 50 | solar | PRE_CONSENT | Thurcroft Interchange Energy Park - Solar Farm | Exagen | Rotherham | - | - | 0.2km/275kV | `18533` | y |
| 1033 | 55.8 | 50 | solar | PRE_CONSENT | Bulworthy Farm, Stoney Cross - Solar Photovoltaic Ar... | Noventum Power Limited | Torridge | - | - | 0.3km/400kV | `19426` | y |
| 1034 | 55.8 | 50 | solar | PRE_CONSENT | North Moor Farm, Keadby - Solar Panels | Lidsey Renewables Limited | North Lincolnshire | - | - | 0.2km/400kV | `19648` | y |
| 1035 | 55.8 | 50 | bess | PRE_CONSENT | Jamesfield Garden Centre, Newburgh - Battery Energy ... | Harmony Energy Limited | Perth and Kinross | - | - | 0.1km/132kV | `19734` | y |
| 1036 | 55.8 | 50 | bess | PRE_CONSENT | Laigh Park Water Treatment Works - Battery Energy St... | Bluestone Energy | Renfrewshire | - | - | 2.4km/132kV | `12030` | y |
| 1037 | 55.8 | 6 | solar | PAST_EXPECTED_START | Etex Building Performance, Redland Avenue - Solar PV... | PROMAT UK/Etex Building Performanc... | North Somerset | 2024-12-30 | 609 | 0.6km/132kV | `17613` | y |
| 1038 | 55.7 | 22 | solar | PAST_EXPECTED_START | Old Hall Solar farm | Renewable Connections | Melton | 2024-09-13 | 717 | 3.9km/400kV | `11153` | y |
| 1039 | 55.6 | 10 | bess | PAST_EXPECTED_START | Glenniston Farm, Auchtertool - Solar Farm | Locogen Consulting Limited | Fife | 2024-04-05 | 878 | 0.3km/132kV | `10433` | y |
| 1040 | 55.6 | 10 | solar | PAST_EXPECTED_START | Howgrove Farm, Green Lane - Solar Panels | Greenvolt Power UK Limited | North Somerset | 2025-11-03 | 301 | 1.1km/132kV | `19109` | y |
| 1041 | 55.6 | 17 | solar | PAST_EXPECTED_START | Leamington Road, Princethorpe - Ash Tree Solar Photo... | British Solar Renewables | Rugby | 2025-08-06 | 390 | 5.9km/132kV | `16614` | y |
| 1042 | 55.6 | 350 | solar | PRE_CONSENT | Fosse Green Energy | Windel Energy / Canadian Solar | The Planning Inspectorate - ... | - | - | 3.1km/400kV | `14101` | y |
| 1043 | 55.6 | 100 | bess | PAST_EXPECTED_START | Cobholden Battery Storage | AGR Renewables | Bedford | 2023-05-04 | 1215 | 3.5km/132kV | `9479` | y |
| 1044 | 55.6 | 100 | bess | PRE_CONSENT | Walpole Bank - Battery Energy Storage Facility | Field Devco Limited | King's Lynn and West Norfolk | - | - | 0.1km/132kV | `13639` | y |
| 1045 | 55.6 | 100 | bess | PRE_CONSENT | Atcost Road - Battery Storage Facility | O&G Group Limited | Barking and Dagenham | - | - | 0.4km/400kV | `16419` | y |
| 1046 | 55.6 | 100 | bess | PRE_CONSENT | Battery Shrewsbury Substation, Uffington - Battery E... | Lower 48 Energy BESS Limited | Shropshire | - | - | 0.1km/400kV | `18366` | y |
| 1047 | 55.6 | 47 | solar | PAST_EXPECTED_START | Firsfield Solar Farm | Enray Power Limited | West Suffolk | 2024-04-30 | 853 | 1.0km/132kV | `9780` | y |
| 1048 | 55.5 | 28 | solar | PAST_EXPECTED_START | Moorside Farm - Solar Farm | Opdenergy UK Limited | Lancaster | 2022-11-14 | 1386 | 1.1km/400kV | `8497` | y |
| 1049 | 55.5 | 60 | bess | PAST_EXPECTED_START | Blackhill Quarry, Woodbury - Battery Energy Storage ... | Clinton Devon Estates | East Devon | 2023-07-13 | 1145 | 2.3km/132kV | `12815` | y |
| 1050 | 55.5 | 22 | solar | PRE_CONSENT | Heath Road, Bagworth - Solar Farm | Renewable Connections Developments... | Hinckley and Bosworth | - | - | 1.0km/132kV | `19187` | y |
| 1051 | 55.5 | 99 | bess | PRE_CONSENT | Hood Barton, Staverton - Battery Energy Storage Syst... | Energy Planning | South Hams | - | - | 0.5km/400kV | `17261` | y |
| 1052 | 55.4 | 21 | solar | PAST_EXPECTED_START | Prentice’s Farm- Solar Farm | Anglo Renewables | Maldon | 2024-09-06 | 724 | 1.0km/132kV | `12990` | **n** |
| 1053 | 55.4 | 16 | solar | PAST_EXPECTED_START | Cox's Brook Solar Farm - Solar Array | PS Renewables Limited | Tewkesbury | 2024-04-24 | 859 | 0.5km/132kV | `13966` | y |
| 1054 | 55.3 | 57 | bess | DESIGN_FROZEN_OR_LATER | Braintree Road, Cressing - Battery Storage | Pivot Power (EDF Renewables) | Braintree | 2023-09-01 | - | 0.1km/400kV | `11995` | y |
| 1055 | 55.3 | 12 | bess | PAST_EXPECTED_START | Dragons Lane - Battery Storage Facility | Hydrock | Cheshire East | 2022-12-01 | 1369 | 1.1km/132kV | `11701` | y |
| 1056 | 55.3 | 9 | solar | PRE_CONSENT | Lings Farm, Birkin Lane - Solar Panels | Fuse Renewables Limited | North East Derbyshire | - | - | 0.5km/132kV | `19646` | y |
| 1057 | 55.2 | 20 | bess | PAST_EXPECTED_START | Strathruddie, Kinglassie - Solar farm | Renewable Connection Developments ... | Fife | 2022-03-16 | 1629 | 0.2km/132kV | `9403` | y |
| 1058 | 55.2 | 20 | solar | PAST_EXPECTED_START | South Lynch Farm - Solar Farm | Novus Renewable Services Limited | Winchester | 2024-10-17 | 683 | 3.9km/132kV | `13790` | y |
| 1059 | 55.2 | 20 | bess | PAST_EXPECTED_START | Westfield Solar Farm & Battery | Brockwell Energy Limited | Fife | 2021-02-12 | 2026 | 0.3km/275kV | `20391` | y |
| 1060 | 55.2 | 250 | bess | DESIGN_FROZEN_OR_LATER | Lapwing Fen 2 - Battery Storage Plant | Tribus Clean Energy | King's Lynn and West Norfolk | 2020-04-27 | - | 0.3km/132kV | `7614` | y |
| 1061 | 55.2 | 43 | solar | PAST_EXPECTED_START | Highfields Farm - Solar Farm & Battery Storage | Boultbee Brooks Renewable Energy L... | Rushcliffe | 2023-02-16 | 1292 | 1.1km/132kV | `10761` | y |
| 1062 | 55.1 | 70 | bess | PRE_CONSENT | Limekiln, Borlum House - Battery Energy Storage Syst... | Boralex | Scottish Government (S36) | - | - | 0.4km/275kV | `18731` | y |
| 1063 | 55.1 | 90 | bess | PRE_CONSENT | Newburn BESS - Battery Energy Storage System | Fig Power | Newcastle upon Tyne | - | - | 0.5km/275kV | `16588` | y |
| 1064 | 55.1 | 25 | bess | PAST_EXPECTED_START | Davies Road - Whitebirk Battery Storage | Field | Blackburn with Darwen | 2022-03-02 | 1643 | 0.3km/400kV | `9563` | y |
| 1065 | 55.1 | 25 | solar | PAST_EXPECTED_START | Lawns Solar Farm | Lightsource Limited | Fylde | 2023-02-01 | 1307 | 0.6km/132kV | `9878` | y |
| 1066 | 55.1 | 25 | bess | PAST_EXPECTED_START | Caton Road, Lancaster - Battery Storage Facility | Energi Generation 12 Limited | Lancaster | 2022-12-07 | 1363 | 0.1km/132kV | `10047` | y |
| 1067 | 55.1 | 25 | bess | PAST_EXPECTED_START | A981 Fraserburgh - Battery Energy Storage | Fraserburgh Energy Limited | Aberdeenshire | 2022-02-21 | 1652 | 1.3km/132kV | `10222` | y |
| 1068 | 55.1 | 25 | solar | PAST_EXPECTED_START | The Village Of Halse - Solar Array | Novus Renewable Services Limited | Somerset | 2024-01-26 | 948 | 2.0km/132kV | `10272` | y |
| 1069 | 55.1 | 25 | bess | PAST_EXPECTED_START | Bankhead Farm - Energy Storage System | Low Carbon Storage | Clackmannanshire | 2024-05-02 | 851 | 0.4km/132kV | `14450` | y |
| 1070 | 55.1 | 41 | solar | PAST_EXPECTED_START | West House Farm, Fishburn - Solar Farm | Voltis Renewables | County Durham | 2024-04-16 | 867 | 1.4km/400kV | `13079` | y |
| 1071 | 55.0 | 19 | solar | PAST_EXPECTED_START | Woodford Lane West - Solar Farm (Hebden Green) | Anglo Renewables | Cheshire West and Chester | 2024-07-25 | 767 | 4.7km/132kV | `14643` | y |
| 1072 | 55.0 | 500 | bess | DESIGN_FROZEN_OR_LATER | Coalburn Energy - Battery Storage | Alcemi Storage Development Limited | Scottish Government (S36) | 2023-06-07 | - | 0.5km/400kV | `11034` | y |
| 1073 | 55.0 | 500 | solar | PRE_CONSENT | East Pye Solar Farm | Island Green Power | The Planning Inspectorate - ... | - | - | 2.9km/400kV | `20670` | y |
| 1074 | 55.0 | 2 | solar | PAST_EXPECTED_START | Brewster Brothers, Drumshoreland Road - Solar Panels | Brewster Brothers Limited | West Lothian | 2025-09-19 | 346 | 1.4km/132kV | `14041` | y |
| 1075 | 54.9 | 40 | solar | PAST_EXPECTED_START | Ty’n y Waun - Solar Farm (Bridgend Energy Hub) | Cenin Renewables Limited | Welsh Government (NSIP) | 2024-10-11 | 689 | 0.8km/400kV | `10299` | y |
| 1076 | 54.9 | 40 | solar | PAST_EXPECTED_START | Tophams Solar Farm | Pathfinder Clean Energy UK Dev Lim... | North Hertfordshire | 2024-06-17 | 805 | 2.3km/400kV | `11089` | y |
| 1077 | 54.9 | 40 | bess | PAST_EXPECTED_START | Long Pasture Farm, Little Stainton - Solar Farm | Electric Works | Darlington | 2023-08-10 | 1117 | 0.5km/132kV | `12951` | y |
| 1078 | 54.9 | 40 | solar | PRE_CONSENT | Penllergaer Solar Farm - Solar Farm | Ecap Renewables | Welsh Government (NSIP) | - | - | 0.1km/400kV | `16010` | y |
| 1079 | 54.9 | 40 | bess | PRE_CONSENT | Newton Farm, Westburn Road - Battery Storage Facilit... | Apatura – GPC 676 Limited | South Lanarkshire | - | - | 0.0km/275kV | `18476` | **n** |
| 1080 | 54.9 | 40 | solar | PRE_CONSENT | Lightwood Solar Farm - Solar Panels | Eden AW Solar Ltd | Forest of Dean | - | - | 0.8km/132kV | `18917` | y |
| 1081 | 54.8 | 2 | solar | PAST_EXPECTED_START | Central Boulevard, Prologis Park - Solar Panels | Power Zero Limited | Coventry | 2025-12-17 | 257 | 1.2km/275kV | `20044` | y |
| 1082 | 54.8 | 18 | solar | PAST_EXPECTED_START | Highfield Farm, Royston Road - Solar Farm & Battery ... | Grupotec Solar 3 UK Limited | South Cambridgeshire | 2023-08-03 | 1124 | 3.4km/132kV | `13005` | y |
| 1083 | 54.8 | 18 | solar | PAST_EXPECTED_START | Whisby Quarry, Eagle Road - Solar Array | Conrad Energy | North Kesteven | 2025-09-17 | 348 | 0.6km/400kV | `16797` | y |
| 1084 | 54.8 | 8 | solar | PRE_CONSENT | Benton Lane, Quorum Business Park - Solar Panels | Shelborn Asset Management | North Tyneside | - | - | 1.4km/132kV | `20778` | y |
| 1085 | 54.8 | 50 | bess | PAST_EXPECTED_START | High Road, Saddlebow - Battery Storage | Lynn Power Limited | King's Lynn and West Norfolk | 2024-07-29 | 763 | 0.2km/132kV | `11648` | y |
| 1086 | 54.8 | 50 | solar | CONSENTED_NO_DATE | Wymondley Solar Farm, Great Wymondley | AGR Power Limited | North Hertfordshire | - | - | 0.6km/275kV | `9066` | y |
| 1087 | 54.8 | 30 | solar | PRE_CONSENT | North Newton Solar Farm | North Newton Solar Farm Limited | Somerset | - | - | 1.6km/132kV | `20544` | y |
| 1088 | 54.8 | 50 | bess | PAST_EXPECTED_START | Old Gallows Road - Battery storage | Foresight Group | Perth and Kinross | 2021-08-03 | 1854 | 0.1km/132kV | `8368` | y |
| 1089 | 54.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Burtree Lane - Solar farm | Darlington Borough Council / Aura ... | Darlington | 2023-01-11 | - | 1.2km/132kV | `8529` | y |
| 1090 | 54.8 | 50 | solar | PAST_EXPECTED_START | Scurf Dyke - Solar Farm | BayWa r.e. UK Limited | East Riding of Yorkshire | 2020-03-18 | 2357 | 0.5km/132kV | `12299` | y |
| 1091 | 54.8 | 50 | bess | PAST_EXPECTED_START | Landulph, Ellbridge Lane - Battery Storage Facility | Pivoted Power Llp | Cornwall | 2023-02-06 | 1302 | 0.3km/400kV | `12697` | y |
| 1092 | 54.7 | 38 | solar | PAST_EXPECTED_START | Grafton Underwood | ScottishPower Renewables UK | North Northamptonshire | 2020-09-23 | 2168 | 1.0km/132kV | `7349` | y |
| 1093 | 54.7 | 37 | bess | PAST_EXPECTED_START | Creag Riabhach Wind Farm Extension & Battery Storage | Creag Riabhach Wind Farm Limited | Scottish Government (S36) | 2024-07-05 | 787 | 1.0km/132kV | `11376` | y |
| 1094 | 54.6 | 10 | solar | PAST_EXPECTED_START | Fontley House Farm | Jardin Smith International | Winchester | 2017-05-03 | 3407 | 0.5km/132kV | `6392` | y |
| 1095 | 54.6 | 10 | solar | PAST_EXPECTED_START | Station Lane, South Stainley | Boultbee Brooks Renewable Energy | North Yorkshire | 2024-04-17 | 866 | 0.6km/132kV | `9103` | y |
| 1096 | 54.6 | 10 | bess | PAST_EXPECTED_START | Portmanmoor Road Industrial Estate, Splott - Battery... | Infinis Energy Services Limited | Cheshire West and Chester | 2024-07-22 | 770 | 0.2km/132kV | `16356` | y |
| 1097 | 54.6 | 10 | bess | PAST_EXPECTED_START | Mount Stamper Road, Treverbyn - Battery Energy Stora... | Aldustria Energy Storage | Cornwall | 2024-06-17 | 805 | 0.2km/132kV | `16379` | y |
| 1098 | 54.6 | 37 | solar | PAST_EXPECTED_START | Maisemore - Solar Farm | Renewable Connections Developments... | Tewkesbury | 2023-03-06 | 1274 | 0.4km/400kV | `11170` | y |
| 1099 | 54.6 | 10 | solar | PAST_EXPECTED_START | Little Llwyn Onn - Solar Farm & Battery Storage | Novus Renewable Services Limited | Wrexham | 2023-03-08 | 1272 | 1.0km/132kV | `11544` | y |
| 1100 | 54.6 | 165 | solar | PRE_CONSENT | Springfield - Solar Farm & Battery Energy Storage | Voltalia UK Limited | Scottish Government (S36) | - | - | 2.2km/132kV | `19017` | y |
| 1101 | 54.5 | 28 | solar | CONSENTED_NO_DATE | Deptford Farm, Ebberley Hill - Solar Farm | Elgin Energy ES Co Limited | Torridge | - | - | 0.2km/132kV | `15719` | y |
| 1102 | 54.5 | 46 | bess | DESIGN_FROZEN_OR_LATER | Parc Solar Caenewydd | Infinis Solar Developments | Welsh Government (NSIP) | 2024-12-02 | - | 0.3km/132kV | `11302` | y |
| 1103 | 54.5 | 98 | solar | PRE_CONSENT | Dupplin Solar - Solar Array | BLC Energy | Scottish Government (S36) | - | - | 0.4km/132kV | `20768` | y |
| 1104 | 54.4 | 1 | solar | PAST_EXPECTED_START | Novolex, Brue Avenue - Solar Panels | eEnergy Group PLC | Somerset | 2025-08-29 | 367 | 1.7km/400kV | `19456` | y |
| 1105 | 54.4 | 45 | solar | PAST_EXPECTED_START | Back Lane, Skerne - Solar Farm & Battery Storage | BayWa r.e. UK Limited | East Riding of Yorkshire | 2020-10-23 | 2138 | 0.9km/132kV | `12297` | y |
| 1106 | 54.4 | 16 | solar | PAST_EXPECTED_START | Aveley Landfill, Sandy Lane - PV Solar Array & Batte... | Infinis Energy Services Limited | Thurrock | 2024-07-24 | 768 | 0.4km/132kV | `15828` | y |
| 1107 | 54.4 | 16 | solar | PRE_CONSENT | Tollgate Farm, Welham Green - Solar Farm | Brockwell Energy Limited | Welwyn Hatfield | - | - | 0.3km/132kV | `19478` | y |
| 1108 | 54.3 | 57 | bess | CONSENTED_NO_DATE | Honiley Road - Solar Farm & Battery Storage | Enso Green Holdings Limited | Warwick | - | - | 1.8km/275kV | `12390` | y |
| 1109 | 54.3 | 1 | solar | PAST_EXPECTED_START | Moorcroft Drive, Moorcroft Park - Solar Panels | Noble Green Energy | Sandwell | 2025-11-14 | 290 | 0.1km/275kV | `19706` | y |
| 1110 | 54.3 | 44 | solar | PAST_EXPECTED_START | Bradley Road - Solar Farm | Renewable Connections Developments... | North East Lincolnshire | 2024-04-26 | 857 | 1.2km/132kV | `13863` | y |
| 1111 | 54.3 | 9 | solar | PAST_EXPECTED_START | Ratcliffe On Soar Power Station - Solar Farm | Rushcliffe Borough Council | Rushcliffe | 2023-07-19 | 1139 | 0.0km/132kV | `14507` | y |
| 1112 | 54.2 | 20 | bess | PAST_EXPECTED_START | Riverside Energy Park | Cory Riverside Energy | The Planning Inspectorate - ... | 2020-04-09 | 2335 | 1.9km/400kV | `6535` | y |
| 1113 | 54.2 | 20 | solar | PAST_EXPECTED_START | Sparrow Lodge Farm | Elgin Energy | West Northamptonshire | 2021-03-08 | 2002 | 3.0km/400kV | `7626` | y |
| 1114 | 54.2 | 20 | solar | PAST_EXPECTED_START | Washington Road - Solar Farm | Engerera Renewables Limited | Sunderland | 2021-12-01 | 1734 | 1.1km/275kV | `9841` | y |
| 1115 | 54.2 | 20 | bess | PAST_EXPECTED_START | Mount Road, Castle Gresley - Battery Storage Facilit... | Flexion Energy UK Storage Limited | South Derbyshire | 2022-07-17 | 1506 | 0.2km/132kV | `10012` | y |
| 1116 | 54.2 | 20 | bess | PAST_EXPECTED_START | Vause Farm - Battery Storage | Sirius Renewable Energy Limited | Chorley | 2024-02-09 | 934 | 0.2km/132kV | `10989` | y |
| 1117 | 54.2 | 20 | bess | PAST_EXPECTED_START | Hele Manor Farm, Bradford On Tone - Battery Storage ... | STOR 107 Limited | Somerset | 2023-04-13 | 1236 | 0.3km/400kV | `12174` | y |
| 1118 | 54.2 | 20 | bess | PAST_EXPECTED_START | Yarra Industrial Estate, Loicher Lane - Battery Stor... | Ecclesfield Power Limited | Sheffield | 2024-05-30 | 823 | 3.1km/132kV | `12524` | y |
| 1119 | 54.2 | 20 | bess | PAST_EXPECTED_START | Fraserburgh Road - Kirkton Solar PV Farm & Energy St... | Elgin Energy Es Co Limited | Scottish Government (S36) | 2022-12-22 | 1348 | 1.4km/132kV | `12822` | y |
| 1120 | 54.2 | 20 | bess | PAST_EXPECTED_START | Brockworth Road - Battery Storage System | Exagen | Tewkesbury | 2024-04-25 | 858 | 1.9km/400kV | `15518` | y |
| 1121 | 54.2 | 20 | bess | PAST_EXPECTED_START | Land North of Thornton Road | South Redhouse | Fife | 2016-02-10 | 3855 | 0.1km/132kV | `5797` | y |
| 1122 | 54.2 | 43 | bess | DESIGN_FROZEN_OR_LATER | Merchiston Industrial Estate, Smith Street - Battery... | Falkirk Power Limited | Falkirk | 2023-06-23 | - | 0.9km/132kV | `13225` | y |
| 1123 | 54.2 | 55 | solar | PRE_CONSENT | Brailsford Solar Park, Main Road - Solar Panels | British Solar Renewables | Derbyshire Dales | - | - | 1.1km/132kV | `20021` | y |
| 1124 | 54.2 | 9 | solar | PAST_EXPECTED_START | Norchard Farm | Norchard Solar Farm Limited | Wychavon | 2024-10-11 | 689 | 0.4km/132kV | `6550` | y |
| 1125 | 54.1 | 15 | solar | PRE_CONSENT | Newcastle Road, Cotes Heath - Solar Panels | Ampyr Solar Europe | Stafford | - | - | 0.5km/132kV | `17617` | y |
| 1126 | 54.1 | 15 | solar | PRE_CONSENT | Coed Bach Park, Gwynfryn Road - Solar Panels | Stellar Energy | Swansea | - | - | 1.4km/400kV | `19567` | y |
| 1127 | 54.1 | 42 | solar | DESIGN_FROZEN_OR_LATER | Parc Solar Caenewydd | Infinis Solar Developments | Welsh Government (NSIP) | 2024-12-02 | - | 0.3km/132kV | `11303` | y |
| 1128 | 54.1 | 15 | bess | PROCURING | Luggies Knowe, Hill Of Gremista - Wind Turbines & Ba... | Shetland Aerogenerators Ltd | Shetland Islands | 2025-04-18 | 500 | n/a | `15823` | y |
| 1129 | 54.1 | 25 | bess | PRE_CONSENT | Elvanfoot, Leadhills Road - Phase 3 - BESS | Elvanfoot Energy Storage 3 Limited... | South Lanarkshire | - | - | 0.3km/400kV | `19839` | y |
| 1130 | 54.1 | 69 | bess | PAST_EXPECTED_START | Thurleigh Road - Battery Energy Storage | Pathfinder Clean Energy UK Dev Lim... | Bedford | 2024-01-30 | 944 | 0.1km/132kV | `9651` | y |
| 1131 | 54.0 | 1000 | bess | PRE_CONSENT | Hill Rise, Coleby - Battery Energy Storage | Navenby Energy Limited | North Kesteven | - | - | 0.7km/400kV | `18790` | y |
| 1132 | 54.0 | 840 | solar | PRE_CONSENT | Botley West, Botley - Botley West Solar Project | Photovolt Development Partners / S... | The Planning Inspectorate - ... | - | - | 3.0km/132kV | `12588` | y |
| 1133 | 54.0 | 800 | bess | PRE_CONSENT | The Park Farm, Birds Corner - Battery Energy Storage | Regener8 Power Limited | Breckland | - | - | 2.8km/400kV | `19172` | y |
| 1134 | 54.0 | 522 | bess | PRE_CONSENT | Chads Farm - Photovoltaic Arrays & Battery Storage | Renewable Connections Developments... | Cheshire West and Chester | - | - | 0.5km/132kV | `10728` | y |
| 1135 | 54.0 | 500 | solar | PAST_EXPECTED_START | Sunnica Energy Farm (East and West) | Sunnica | The Planning Inspectorate - ... | 2024-07-12 | 780 | 11.1km/400kV | `7189` | y |
| 1136 | 54.0 | 1 | solar | PAST_EXPECTED_START | Navigator Tissue UK, Badger Road - Solar PV Panels | Navigator Tissue UK Limited | South Ribble | 2025-03-05 | 544 | 0.7km/132kV | `18073` | y |
| 1137 | 54.0 | 67 | bess | PAST_EXPECTED_START | Welford Solar Farm - Solar Farm & Battery Storage | Welford Solar Farm Limited | West Northamptonshire | 2024-10-11 | 689 | 3.9km/400kV | `19218` | y |
| 1138 | 53.9 | 18 | solar | PAST_EXPECTED_START | Arrats Mill, Arrat - Solar Photovoltaic Array | Southesk Estate | Angus | 2023-06-26 | 1162 | 1.1km/132kV | `12644` | y |
| 1139 | 53.9 | 40 | bess | PAST_EXPECTED_START | Breach Farm - Energy Barn | Bluefield Solar Income Fund | South Derbyshire | 2017-08-15 | 3303 | 0.4km/132kV | `6962` | **n** |
| 1140 | 53.9 | 18 | solar | PAST_EXPECTED_START | Caledonian Solar Park | Derwent London Green Energy Limite... | Glasgow City | 2023-06-22 | 1166 | 0.3km/275kV | `9883` | y |
| 1141 | 53.9 | 3 | solar | PAST_EXPECTED_START | Jutes Lane, Weatherlees Hill - Solar Panels | Southern Water Services Limited He... | Thanet | 2024-11-15 | 654 | 0.7km/400kV | `16244` | y |
| 1142 | 53.8 | 1 | solar | PAST_EXPECTED_START | Sytner BMW Sheffield, Brightside Way - Solar Panels | Sytner Group Limited | Sheffield | 2025-12-15 | 259 | 0.2km/275kV | `19937` | y |
| 1143 | 53.8 | 8 | solar | PAST_EXPECTED_START | Canon Barns Road Solar Park | Bluestone Energy | Chelmsford | 2022-01-31 | 1673 | 0.3km/400kV | `8925` | y |
| 1144 | 53.8 | 8 | solar | PAST_EXPECTED_START | Bicton Industrial Park, Stow Road - Solar Farm | Bluefield Renewable Developments L... | Huntingdonshire | 2023-12-01 | 1004 | 2.9km/132kV | `12195` | y |
| 1145 | 53.8 | 8 | solar | PAST_EXPECTED_START | Brookthorpe Solar Farm | PS Renewables | Stroud | 2024-12-18 | 621 | 3.5km/132kV | `13057` | y |
| 1146 | 53.8 | 8 | bess | PAST_EXPECTED_START | Rassau Industrial Estate, Rassau - Battery Energy St... | Private Developer | Blaenau Gwent | 2023-07-24 | 1134 | 0.1km/132kV | `13709` | y |
| 1147 | 53.8 | 8 | solar | PAST_EXPECTED_START | Fox Cover Solar Farm - Ground Mounted Photovoltaic P... | Enviromena Project Management UK L... | County Durham | 2025-03-12 | 537 | 3.9km/400kV | `16237` | y |
| 1148 | 53.8 | 50 | bess | CONSENTED_NO_DATE | Main Street, Kelham - Solar Farm & Battery Energy St... | Assured Asset Solar 2 Limited (Per... | Newark and Sherwood | - | - | 0.8km/400kV | `11998` | y |
| 1149 | 53.8 | 50 | bess | PRE_CONSENT | East Rogerton Cottage, Markethill Road - Battery Sto... | Apatura – GPC 612 Limited | South Lanarkshire | - | - | 0.7km/275kV | `19571` | y |
| 1150 | 53.8 | 50 | solar | PRE_CONSENT | Thornton Estate - Solar PV Panels | Stark Energy | Buckinghamshire | - | - | 0.4km/132kV | `19007` | y |
| 1151 | 53.8 | 30 | solar | PAST_EXPECTED_START | Wauntysswg Farm, near Tredagar | Elgin Energy | Welsh Government (NSIP) | 2019-08-01 | 2587 | 3.8km/132kV | `6477` | y |
| 1152 | 53.8 | 30 | bess | PRE_CONSENT | Cordon Farm, Abernethy - Battery Storage | Elgin Energy EsCo Limited | Perth and Kinross | - | - | 0.6km/132kV | `12903` | y |
| 1153 | 53.8 | 30 | solar | PRE_CONSENT | Manor Farm, Whitfield - Solar Panels | Elgin Energy Esco Ltd | West Northamptonshire | - | - | 1.6km/132kV | `14795` | y |
| 1154 | 53.8 | 30 | solar | PRE_CONSENT | White House Farm | Qair UK | Welsh Government (NSIP) | - | - | 0.9km/132kV | `15562` | y |
| 1155 | 53.8 | 50 | solar | CONSENTED_NO_DATE | Belvoir Estate - Solar farm | JBM Solar Projects Limited | Melton | - | - | 2.6km/132kV | `8483` | y |
| 1156 | 53.8 | 50 | solar | PAST_EXPECTED_START | Knapthorpe Grange, Caunton - Solar Farm | Knapthorpe Solar Limited | Newark and Sherwood | 2025-03-31 | 518 | 1.4km/400kV | `9894` | y |
| 1157 | 53.8 | 50 | solar | PAST_EXPECTED_START | Hockerton Road, Caunton - Solar Farm | Muskham Solar Limited | Newark and Sherwood | 2025-03-31 | 518 | 1.2km/132kV | `10080` | y |
| 1158 | 53.8 | 50 | solar | PRE_CONSENT | Glassthorpe Hill, Flore - Solar Farm | EDF Renewables | West Northamptonshire | - | - | 0.4km/400kV | `11380` | y |
| 1159 | 53.8 | 50 | solar | PRE_CONSENT | Postcombe - Solar Array | Solar 2 Limited | South Oxfordshire | - | - | 1.5km/132kV | `11653` | y |
| 1160 | 53.8 | 50 | solar | CONSENTED_NO_DATE | Main Street, Kelham - Solar Farm & Battery Energy St... | Assured Asset Solar 2 Limited (Per... | Newark and Sherwood | - | - | 0.8km/400kV | `11999` | y |
| 1161 | 53.8 | 50 | solar | PRE_CONSENT | Hett Moor Farm, Hett - Solar Farm | Lightsource SPV 189 Limited | County Durham | - | - | 0.5km/400kV | `14327` | y |
| 1162 | 53.8 | 50 | bess | PRE_CONSENT | Buckies Farm - Battery Energy Storage | OPDE UK Limted | Highland | - | - | 0.7km/275kV | `17093` | y |
| 1163 | 53.8 | 50 | solar | PRE_CONSENT | Broad Lane, Cawood - Solar Farm & Battery Storage | Quintas Cleantech | North Yorkshire | - | - | 1.8km/132kV | `17886` | y |
| 1164 | 53.8 | 50 | solar | PRE_CONSENT | Castle Hills Solar Farm - Solar Panels | Castle Hills Solar Farm Limited | Solihull | - | - | 1.4km/132kV | `19476` | y |
| 1165 | 53.8 | 50 | solar | PRE_CONSENT | America Farm, Woodcoates Road - Solar Farm | High Marnham Renewables Limited | Bassetlaw | - | - | 1.4km/275kV | `20755` | y |
| 1166 | 53.8 | 1 | solar | PAST_EXPECTED_START | Pembrey Road - Ground Mounted Solar Panels | Gravells Limited | Carmarthenshire | 2025-11-25 | 279 | 2.6km/132kV | `14022` | y |
| 1167 | 53.8 | 1 | solar | PAST_EXPECTED_START | PD Teesport Warehouse A, Bulk Tees - Solar Panels | PD Ports | Redcar and Cleveland | 2025-07-17 | 410 | 0.8km/275kV | `19065` | y |
| 1168 | 53.8 | 1 | solar | PAST_EXPECTED_START | Selhurst Traincare Depot, Selhurst Road - Solar Pane... | Energy Gardens Limited | Croydon | 2025-11-03 | 301 | 2.5km/400kV | `19709` | y |
| 1169 | 53.8 | 50 | bess | PRE_CONSENT | Malcolmwood Farm, Loanend Road - Battery Energy Stor... | Bluestone Energy | South Lanarkshire | - | - | 0.2km/275kV | `18736` | y |
| 1170 | 53.8 | 14 | solar | PAST_EXPECTED_START | Byde Mill Solar Farm, Poulshot - Solar Farm | Ampyr | Wiltshire | 2025-12-22 | 252 | 1.1km/132kV | `18110` | y |
| 1171 | 53.6 | 8 | bess | PAST_EXPECTED_START | Wouldham Road, Wouldham - Battery Storage Facility | AMP Energy Services Limited | Tonbridge and Malling | 2022-01-06 | 1698 | 0.1km/132kV | `10364` | y |
| 1172 | 53.6 | 8 | solar | PAST_EXPECTED_START | Langer Lane Solar Farm | Ethical Power Development Limited | North East Derbyshire | 2025-04-17 | 501 | 2.4km/132kV | `16745` | y |
| 1173 | 53.6 | 100 | bess | PRE_CONSENT | Power Generation Development in Islandmagee | Heron Storage Limited | Mid and East Antrim | - | - | 2.0km/275kV | `20022` | y |
| 1174 | 53.6 | 100 | bess | PRE_CONSENT | Arleston Solar & Battery Energy Storage System | Noventum Power Limited | South Derbyshire | - | - | 0.3km/132kV | `18141` | y |
| 1175 | 53.5 | 28 | solar | PAST_EXPECTED_START | Backworth Lane, Backworth - Solar Farm | Northumberland Estates | North Tyneside | 2023-05-09 | 1210 | 1.7km/275kV | `10979` | y |
| 1176 | 53.5 | 3 | solar | PAST_EXPECTED_START | Siniat, Kirkhaw Lane - Solar PV Panels | Siniat Limited | Wakefield | 2024-12-23 | 616 | 0.3km/132kV | `17648` | y |
| 1177 | 53.5 | 7 | bess | PAST_EXPECTED_START | Philip Street Car Breakers | Conrad Energy | Bristol, City of | 2020-06-29 | 2254 | 0.2km/132kV | `7938` | y |
| 1178 | 53.4 | 160 | bess | PRE_CONSENT | Beinneun II Windfarm | Beinneun 2 Ltd | Scottish Government (S36) | - | - | 1.6km/132kV | `15422` | y |
| 1179 | 53.4 | 75 | solar | DESIGN_FROZEN_OR_LATER | Cowbridge Road, Bicker Fen - Solar Array | AGR Solar 2 Limited | South Holland | 2023-07-21 | - | 0.6km/400kV | `12118` | y |
| 1180 | 53.4 | 35 | bess | DESIGN_FROZEN_OR_LATER | Darlington Road, Skeeby - Battery Energy Storage | Atrato Onsite Energy / Harmony Ene... | North Yorkshire | 2023-08-18 | - | 0.7km/132kV | `8131` | y |
| 1181 | 53.4 | 27 | solar | PAST_EXPECTED_START | Allington Lane - Solar & Battery Farm | Eastleigh Borough Council | Eastleigh | 2024-07-26 | 766 | 2.0km/400kV | `14585` | y |
| 1182 | 53.4 | 27 | solar | PRE_CONSENT | Toronto Green Energy Park, Addison Road - Solar Farm | Toronto Green Energy Park Limited | County Durham | - | - | 0.2km/132kV | `19733` | y |
| 1183 | 53.4 | 45 | solar | PRE_CONSENT | Woodfold Lane, Brentingby - Solar Farm | Windel Solar 12 Limited | Melton | - | - | 0.8km/132kV | `18693` | y |
| 1184 | 53.4 | 7 | bess | PAST_EXPECTED_START | Albrighton Substation, Beamish Lane - Battery Storag... | Fig Power (part of Hydrock) | Shropshire | 2024-02-26 | 917 | 1.7km/400kV | `12807` | **n** |
| 1185 | 53.4 | 7 | solar | PAST_EXPECTED_START | Moto Wetherby Motorway Service Area, Deighton Gates ... | Moto Hospitality Limited | North Yorkshire | 2024-08-09 | 752 | 0.8km/275kV | `15520` | y |
| 1186 | 53.3 | 57 | bess | PRE_CONSENT | National Grids Rainhill Substation Battery storage f... | Sizing John Limited | St. Helens | - | - | 0.1km/132kV | `11559` | y |
| 1187 | 53.3 | 57 | bess | PRE_CONSENT | Waterloo Farm, Furbarn Road - Battery Storage | Shaw-Energi Limited | Rochdale | - | - | 0.4km/275kV | `14597` | y |
| 1188 | 53.3 | 16 | solar | PAST_EXPECTED_START | Locquiers Farm, Plump Hill - Solar Farm | Opdenergy UK 3 Limited | Forest of Dean | 2021-12-15 | 1720 | 4.4km/132kV | `9114` | y |
| 1189 | 53.3 | 12 | solar | PAST_EXPECTED_START | Bentham House Farm, Mopes Lane - Solar Farm | Spring Dev 08 Limited | Wiltshire | 2025-06-06 | 451 | 2.3km/132kV | `17256` | y |
| 1190 | 53.3 | 34 | solar | PAST_EXPECTED_START | Rayton Farm Lane - Solar Farm | Harmony Energy Limited | Bassetlaw | 2024-03-07 | 907 | 0.1km/132kV | `11181` | y |
| 1191 | 53.3 | 34 | bess | PAST_EXPECTED_START | Battery Energy Storage Facility in Londonderry | Heron Storage Ltd | Derry City and Strabane | 2024-04-16 | 867 | 2.4km/275kV | `15303` | y |
| 1192 | 53.3 | 120 | bess | DESIGN_FROZEN_OR_LATER | Gainsborough Road, Saundby - Battery Storage Facilit... | Enso Energy / Cero Generation | Bassetlaw | 2022-07-14 | - | 0.6km/400kV | `9816` | y |
| 1193 | 53.3 | 3 | solar | PAST_EXPECTED_START | Waste Processing Plant, Manston Road North - Solar F... | Speciality Breads Limited | Thanet | 2025-07-30 | 397 | 1.9km/132kV | `18715` | y |
| 1194 | 53.2 | 26 | solar | PRE_CONSENT | Hollyhurst Farm, Mile Tree Lane - Solar Panels | Greenfield Energy Developments Lim... | Rugby | - | - | 0.3km/400kV | `18318` | y |
| 1195 | 53.2 | 150 | bess | DESIGN_FROZEN_OR_LATER | Fiddlers Ferry Power Station - Battery storage | SSE Enterprise (SSE PLC) | Warrington | 2023-06-20 | - | 0.1km/275kV | `9404` | y |
| 1196 | 53.1 | 15 | bess | PAST_EXPECTED_START | Estuary Farm, Edward Benefer Way - Solar Farm & Batt... | Namene Solar | King's Lynn and West Norfolk | 2021-12-08 | 1727 | 0.6km/132kV | `9345` | y |
| 1197 | 53.1 | 15 | solar | PAST_EXPECTED_START | Skye Green Solar Farm | PS Renewables Limited | Braintree | 2025-04-03 | 515 | 4.3km/400kV | `16905` | y |
| 1198 | 53.1 | 25 | solar | PAST_EXPECTED_START | St Cleres Hall Pit Solar Array | St Cleres Solar Farm Limited | Chelmsford | 2021-10-27 | 1769 | 1.6km/132kV | `8406` | y |
| 1199 | 53.1 | 25 | solar | PAST_EXPECTED_START | Wellbank - Solar Farm | Greentech | Angus | 2024-02-15 | 928 | 0.8km/132kV | `11365` | y |
| 1200 | 53.1 | 25 | solar | PAST_EXPECTED_START | Nickerlands Solar Farm - Solar Farm | AR Toot Hill Limited | Epping Forest | 2025-02-20 | 557 | 2.0km/275kV | `16550` | y |
| 1201 | 53.1 | 25 | bess | PRE_CONSENT | Newton Lane, Ledston - Battery Storage Facility | Harmony LS Limited | Leeds | - | - | 0.2km/132kV | `17443` | y |
| 1202 | 53.1 | 25 | bess | PRE_CONSENT | River Mel Solar Farm & Battery Storage System | Quintas Cleantech | South Cambridgeshire | - | - | 0.9km/132kV | `17887` | y |
| 1203 | 53.1 | 25 | solar | PRE_CONSENT | River Mel Solar Farm & Battery Storage System | Quintas Cleantech | South Cambridgeshire | - | - | 0.9km/132kV | `17888` | y |
| 1204 | 53.1 | 25 | solar | PRE_CONSENT | Spratsgate Lane, Siddington - Solar Farm and Battery... | Aura Power Developments Limited | Cotswold | - | - | 0.2km/132kV | `19221` | y |
| 1205 | 53.1 | 25 | solar | PAST_EXPECTED_START | Cressing East - Solar Farm | EDF Energy Renewables | Braintree | 2025-03-05 | 544 | 0.4km/400kV | `11235` | y |
| 1206 | 53.1 | 240 | bess | PRE_CONSENT | Kellingley Farm, Stocking Lane - Battery Energy Stor... | Newton Energi Limited | North Yorkshire | - | - | 6.6km/132kV | `19467` | y |
| 1207 | 53.0 | 6 | solar | PAST_EXPECTED_START | Boots Campus - Roof Top Solar Farm | Boots Company Plc | Nottingham | 2022-12-05 | 1365 | 0.5km/132kV | `11617` | y |
| 1208 | 53.0 | 24 | solar | PAST_EXPECTED_START | Moat Farm - Solar Farm | Anesco Limited | Buckinghamshire | 2022-02-22 | 1651 | 0.5km/400kV | `9478` | y |
| 1209 | 53.0 | 300 | bess | PRE_CONSENT | Spittal Mains, Spittal - Battery Energy Storage Syst... | Field Spittal Limited | Scottish Government (S36) | - | - | 0.9km/132kV | `16381` | y |
| 1210 | 52.9 | 6 | solar | PAST_EXPECTED_START | Gander Down Solar Farm, Stevens Drove - Solar Farm | PS Renewables Limited | Test Valley | 2023-06-01 | 1187 | 1.2km/132kV | `12142` | y |
| 1211 | 52.9 | 40 | solar | PRE_CONSENT | New Buildings Solar Farm, Sandon Road - Solar Farm | New Buildings Solar Farm Limited | Staffordshire Moorlands | - | - | 0.3km/132kV | `12252` | y |
| 1212 | 52.9 | 40 | solar | PRE_CONSENT | Nythe Road, Pedwell - Solar Photovoltaic Park | Elgin Energy Services Limited | Somerset | - | - | 0.4km/132kV | `16100` | **n** |
| 1213 | 52.9 | 40 | solar | PRE_CONSENT | Leyden Road - Solar Array | Trio Power Limited | West Lothian | - | - | 0.3km/275kV | `19086` | y |
| 1214 | 52.9 | 40 | solar | PRE_CONSENT | Lassington Lane, Highnam - Solar Farm | Pathfinder Clean Energy UK Dev Lim... | Tewkesbury | - | - | 0.6km/132kV | `19390` | y |
| 1215 | 52.9 | 40 | solar | PRE_CONSENT | Glyntaff Solar Farm, Bryntail Road - Solar Array | Renantis Falck Renewables Limited | Welsh Government (NSIP) | - | - | 0.6km/132kV | `15563` | y |
| 1216 | 52.9 | 5 | solar | PRE_CONSENT | Curver Way - Solar Panels | Harvest Green Developments | North Northamptonshire | - | - | 0.9km/132kV | `20661` | y |
| 1217 | 52.8 | 18 | solar | PAST_EXPECTED_START | Glebe Horsford - Solar Farm | Pathfinder Clean Energy UKDev Limi... | Broadland | 2025-07-01 | 426 | 5.2km/132kV | `12646` | y |
| 1218 | 52.8 | 6 | solar | PAST_EXPECTED_START | Crockwell Hill - Solar Farm | PS Renewables Limited | West Northamptonshire | 2025-05-27 | 461 | 0.4km/132kV | `17309` | y |
| 1219 | 52.8 | 50 | solar | PAST_EXPECTED_START | Wemyss Estate - Randolph Solar Farm & Battery Energy... | Elgin Energy | Scottish Government (S36) | 2022-05-24 | 1560 | 0.2km/132kV | `11482` | y |
| 1220 | 52.8 | 50 | bess | PRE_CONSENT | Westfield Road, Carlton - Battery Storage | Firma Vogt Solar Limited | Leeds | - | - | 0.1km/132kV | `15338` | y |
| 1221 | 52.8 | 50 | bess | PRE_CONSENT | Ipswich Road, Cardiff - Battery Storage | Green Frog Power 214 Limited | Cardiff | - | - | 0.1km/132kV | `15610` | y |
| 1222 | 52.8 | 50 | bess | PRE_CONSENT | Rush Green Motors - Battery storage | RNA Energy limited | North Hertfordshire | 2021-10-06 | - | 1.4km/132kV | `16045` | **n** |
| 1223 | 52.8 | 50 | bess | PRE_CONSENT | Pinkworthy Farm, Pyworthy - Battery Storage | Private Developer | Torridge | 2024-08-09 | - | 0.5km/132kV | `16068` | y |
| 1224 | 52.8 | 50 | bess | PRE_CONSENT | Maltby Solar Farm | Infinis Energy Services Limited | Rotherham | - | - | 0.6km/132kV | `17103` | y |
| 1225 | 52.8 | 50 | solar | PAST_EXPECTED_START | Stargoose Farm - Solar Farm | Solarcentury Limited / Statkraft U... | South Cambridgeshire | 2022-04-14 | 1600 | 0.4km/132kV | `11719` | y |
| 1226 | 52.8 | 50 | solar | PAST_EXPECTED_START | Middle Road Farm - Solar Farm & Battery Storage | Leicestershire Solar 1 Limited /No... | Stratford-on-Avon | 2023-08-18 | 1109 | 0.3km/132kV | `13970` | y |
| 1227 | 52.8 | 50 | bess | PRE_CONSENT | Grendon Lakes, Grendon - Battery Storage Facility | Statera Energy | North Northamptonshire | - | - | 0.2km/132kV | `14321` | y |
| 1228 | 52.8 | 50 | solar | PAST_EXPECTED_START | Low Horton Farm - Solar Farm | Bluefield Renewable Developments L... | Northumberland | 2022-11-04 | 1396 | 0.7km/275kV | `15753` | y |
| 1229 | 52.8 | 50 | solar | PRE_CONSENT | Low Fen, Drove Way - Solar Farm | South Cambridgeshire District Coun... | South Cambridgeshire | - | - | 1.3km/132kV | `17360` | y |
| 1230 | 52.8 | 30 | bess | PAST_EXPECTED_START | Blackpark Energy Storage | Shires Hamilton | Highland | 2020-12-15 | 2085 | 0.5km/132kV | `7226` | **n** |
| 1231 | 52.8 | 30 | bess | PAST_EXPECTED_START | Drumcross Battery Storage | Muirhall Energy | West Lothian | 2018-06-12 | 3002 | 2.2km/132kV | `8155` | y |
| 1232 | 52.8 | 30 | bess | DESIGN_FROZEN_OR_LATER | Farburn Place - Battery Energy Storage Facility | Peak Reserve Power Limited / Centr... | Aberdeen City | 2021-09-30 | - | 1.3km/132kV | `8385` | y |
| 1233 | 52.8 | 30 | bess | PAST_EXPECTED_START | Back Lane, Skerne - Solar Farm & Battery Storage | BayWa r.e. UK Limited | East Riding of Yorkshire | 2020-10-23 | 2138 | 0.9km/132kV | `12296` | y |
| 1234 | 52.8 | 30 | solar | PAST_EXPECTED_START | Manor Farm, Denchworth - Solar Photovoltaic Panels | Renewable Connections Limited | Vale of White Horse | 2025-04-03 | 515 | 7.3km/132kV | `12601` | y |
| 1235 | 52.8 | 30 | bess | PAST_EXPECTED_START | Bishopmill - Battery Energy Storage | Green Power Consultants | Moray | 2023-12-21 | 984 | 0.6km/132kV | `14191` | y |
| 1236 | 52.8 | 50 | solar | PAST_EXPECTED_START | Cayton Solar farm | Elgin Energy | North Yorkshire | 2022-01-13 | 1691 | 0.8km/132kV | `6561` | y |
| 1237 | 52.8 | 50 | solar | PAST_EXPECTED_START | Down Barn Farm | Scottish Power Renewables | Wiltshire | 2020-04-23 | 2321 | 0.3km/132kV | `7616` | y |
| 1238 | 52.8 | 50 | solar | PAST_EXPECTED_START | Cornwell Solar Farm | Low Carbon / EDF Energy Renewables | South Oxfordshire | 2021-10-26 | 1770 | 0.3km/132kV | `7945` | y |
| 1239 | 52.8 | 50 | solar | PAST_EXPECTED_START | Harlesford Solar Farm | Harlesford Solar Farm Limited | South Oxfordshire | 2021-12-16 | 1719 | 0.4km/132kV | `7956` | y |
| 1240 | 52.8 | 50 | solar | PAST_EXPECTED_START | Cotmoor Lane | JBM Solar | Newark and Sherwood | 2022-02-18 | 1655 | 0.2km/132kV | `8118` | y |
| 1241 | 52.8 | 50 | solar | PAST_EXPECTED_START | Haunton Solar Farm | Stark Energy | Lichfield | 2022-04-07 | 1607 | 1.1km/132kV | `8181` | y |
| 1242 | 52.8 | 50 | solar | PAST_EXPECTED_START | Dodwells Solar Farm | Opdenergy UK Limited | South Oxfordshire | 2023-08-23 | 1104 | 0.7km/132kV | `8539` | y |
| 1243 | 52.8 | 50 | bess | PRE_CONSENT | Howick Hall Farm - Battery Storage Facility | Penwortham Storage Limited | South Ribble | - | - | 0.2km/400kV | `8829` | y |
| 1244 | 52.8 | 50 | solar | PRE_CONSENT | Long Barrow Solar Farm Project | Low Carbon Solar Park 42 Limited | East Cambridgeshire | - | - | 0.8km/132kV | `9129` | y |
| 1245 | 52.8 | 50 | solar | PAST_EXPECTED_START | Perham Down - Meadow Solar Farm & Battery Storage | Low Carbon UK Solar Investment Co ... | Test Valley | 2022-11-18 | 1382 | 0.6km/132kV | `9176` | y |
| 1246 | 52.8 | 50 | solar | PAST_EXPECTED_START | Forest Gate - Solar Farm & Battery Storage | Eden Renewables | Wiltshire | 2023-03-10 | 1270 | 0.9km/132kV | `9230` | y |
| 1247 | 52.8 | 50 | bess | PRE_CONSENT | Burwell Main Sub-Station | Aura Power / Pivot Power | East Cambridgeshire | - | - | 0.1km/400kV | `9292` | y |
| 1248 | 52.8 | 50 | bess | PRE_CONSENT | Sundon Substation | Pivot Power | Central Bedfordshire | - | - | 0.2km/132kV | `9315` | y |
| 1249 | 52.8 | 50 | solar | PAST_EXPECTED_START | Impens Farm - Solar Farm & Battery Storage | Enso Energy Holdings H Limited | Somerset | 2022-12-06 | 1364 | 0.8km/132kV | `10812` | y |
| 1250 | 52.8 | 50 | bess | PRE_CONSENT | Grendon Lakes - Battery Storage | Statera Energy | North Northamptonshire | - | - | 0.1km/132kV | `10955` | **n** |
| 1251 | 52.8 | 50 | solar | PRE_CONSENT | Lower Waldridge Farm, Ford - Solar Farm | Low Carbon UK Solar Investment Co ... | Buckinghamshire | 2021-12-21 | - | 1.8km/132kV | `10965` | y |
| 1252 | 52.8 | 50 | solar | PAST_EXPECTED_START | Kenley Solar Farm | Boom Power Limited | East Riding of Yorkshire | 2022-11-18 | 1382 | 0.3km/132kV | `11367` | y |
| 1253 | 52.8 | 50 | solar | PAST_EXPECTED_START | Brigstock Solar Farm | Scottish Power Renewables | North Northamptonshire | 2022-01-14 | 1690 | 0.7km/132kV | `11724` | y |
| 1254 | 52.8 | 50 | solar | PAST_EXPECTED_START | Stoneshollow Solar Farm | JBM Solar Projects Limited | Hinckley and Bosworth | 2022-08-16 | 1476 | 1.1km/275kV | `12135` | y |
| 1255 | 52.8 | 50 | bess | PRE_CONSENT | Land Adjacent to 4 Redcote Lane (Armley) | Enstor (formerly CJ Energy) | Leeds | - | - | 0.2km/132kV | `12224` | y |
| 1256 | 52.8 | 50 | solar | PRE_CONSENT | Nuneham Courtenay - Solar Farm | RES Limited | South Oxfordshire | - | - | 0.6km/132kV | `12387` | y |
| 1257 | 52.8 | 50 | solar | PRE_CONSENT | Scawby Road - Solar Array | Brockwell Storage & Solar Limited | North Lincolnshire | - | - | 0.5km/132kV | `12608` | y |
| 1258 | 52.8 | 50 | bess | PRE_CONSENT | Middleton Of Blackhills, Rothienorman - Battery Ener... | Scot Stability Limited | Aberdeenshire | - | - | 0.6km/400kV | `13087` | **n** |
| 1259 | 52.8 | 50 | solar | PAST_EXPECTED_START | Crick Solar Farm | Voltalia UK | West Northamptonshire | 2024-06-26 | 796 | 0.5km/132kV | `13470` | y |
| 1260 | 52.8 | 50 | bess | PRE_CONSENT | Existing Kaimes Substation, Old Burdiehouse Road - B... | Kaimes Renewable Energy Park | City of Edinburgh | - | - | 0.1km/275kV | `13809` | y |
| 1261 | 52.8 | 50 | solar | PAST_EXPECTED_START | Carr House Farm, Drove Lane - Solar Panels | Private Developer | East Riding of Yorkshire | 2023-09-01 | 1095 | 0.2km/132kV | `14471` | y |
| 1262 | 52.8 | 50 | bess | PRE_CONSENT | Hodgetts Lane, Berkswell - Electricity Storage Facil... | Anglo ES Berkswell Limited | Solihull | - | - | 0.3km/275kV | `14510` | y |
| 1263 | 52.8 | 50 | bess | PAST_EXPECTED_START | Flatterton Farm, Flatterton Road - Battery Storage | Big Battery (Flatterton Farm) Limi... | Inverclyde | 2024-06-05 | 817 | 1.6km/132kV | `15154` | y |
| 1264 | 52.8 | 50 | bess | PRE_CONSENT | Hodgetts Lane, Berkswell - Electricity Storage Facil... | Coventry Energy Storage Limited | Solihull | - | - | 0.2km/132kV | `15230` | y |
| 1265 | 52.8 | 50 | bess | PRE_CONSENT | Broomloan Road - Battery Energy Storage | Lifetime Property Limited | Glasgow City | 2022-06-28 | - | 0.1km/132kV | `17129` | y |
| 1266 | 52.8 | 50 | solar | PAST_EXPECTED_START | Barnstaples Farm | Nextpower SPV 14 Limited | Vale of White Horse | 2024-02-28 | 915 | 3.1km/132kV | `17131` | y |
| 1267 | 52.8 | 50 | solar | PAST_EXPECTED_START | Welford Solar Farm - Solar Farm & Battery Storage | Welford Solar Farm Limited | West Northamptonshire | 2024-10-11 | 689 | 3.9km/400kV | `19219` | y |
| 1268 | 52.8 | 50 | solar | PRE_CONSENT | Pilfrey Solar Farm - Solar Farm | Culham Renewables Limited | North Lincolnshire | - | - | 0.6km/400kV | `19542` | y |
| 1269 | 52.8 | 2 | solar | PAST_EXPECTED_START | Panattoni Park, Luton Road - Solar Panels | Saber Renewable Energy Limited | Central Bedfordshire | 2025-04-15 | 503 | 1.1km/400kV | `18364` | y |
| 1270 | 52.8 | 50 | solar | PRE_CONSENT | West Fen Farm, Whitemoor Road - Solar Farm | Pathfinder Clean Energy UK Dev Lim... | Fenland | - | - | 0.6km/132kV | `15272` | y |
| 1271 | 52.8 | 4 | solar | PAST_EXPECTED_START | Mansfield Road, Temple Normanton - Solar Farm | Derbyshire County Council Property... | North East Derbyshire | 2024-05-20 | 833 | 0.3km/132kV | `16287` | y |
| 1272 | 52.8 | 23 | solar | PAST_EXPECTED_START | Green Lane & Cliff Lane, Gonerby Moor - Solar Farm | Lightsource BP | South Kesteven | 2024-01-22 | 952 | 1.0km/132kV | `12470` | **n** |
| 1273 | 52.8 | 50 | bess | PRE_CONSENT | Tollgate Battery Storage Facility | RNA Energy | Welwyn Hatfield | - | - | 0.1km/132kV | `7335` | y |
| 1274 | 52.7 | 22 | solar | PAST_EXPECTED_START | Cholderton Road, Quarley - Solar Farm | Innova Renewables | Test Valley | 2025-05-14 | 474 | 2.6km/132kV | `10146` | **n** |
| 1275 | 52.7 | 2 | solar | PAST_EXPECTED_START | Charlie Bighams Quarry Kitchen, Dulcote Hill Lane - ... | Charlie Bighams Quarry Kitchen | Somerset | 2025-09-23 | 342 | 3.5km/400kV | `17706` | y |
| 1276 | 52.7 | 48 | bess | PRE_CONSENT | Meadowville, Hull Road - Battery Energy Storage Syst... | UK Battery Storage Limited | York | - | - | 0.2km/400kV | `19424` | y |
| 1277 | 52.6 | 6 | solar | PAST_EXPECTED_START | Maelor Gasworks - Solar Farm & Battery Storage | Novus Renewable Services Limited | Wrexham | 2022-11-09 | 1391 | 0.9km/132kV | `9343` | y |
| 1278 | 52.6 | 10 | bess | PAST_EXPECTED_START | Minety Substation | JBM Solar Project | Wiltshire | 2022-04-07 | 1607 | 0.2km/400kV | `7941` | y |
| 1279 | 52.6 | 10 | solar | PAST_EXPECTED_START | Twyford, Melton - Solar Farm | Noventum Power Limited | Melton | 2024-11-27 | 642 | 0.4km/400kV | `15188` | y |
| 1280 | 52.6 | 13 | bess | PAST_EXPECTED_START | Maybrook Road - Battery facility | Conrad Energy (Develeopments) Limi... | Birmingham | 2022-08-08 | 1484 | 0.5km/132kV | `11008` | y |
| 1281 | 52.6 | 22 | solar | PRE_CONSENT | Mousewell Farm, Besom Lane - Solar Farm | RWE Renewables UK Limited | South Gloucestershire | - | - | 0.4km/400kV | `17083` | y |
| 1282 | 52.6 | 10 | solar | PRE_CONSENT | Dyffryn Farm, Ynysmaerdy - Solar Panels | Windel Solar 8 Limited | Rhondda Cynon Taf | - | - | 0.8km/132kV | `18881` | y |
| 1283 | 52.6 | 100 | bess | PRE_CONSENT | Kirkhaw Lane - Battery Storage Energy | SSE Enterprise | Wakefield | - | - | 0.0km/132kV | `10022` | y |
| 1284 | 52.6 | 100 | bess | PRE_CONSENT | Hillside Farm, Lancaster Road - Battery Storage | Hamilton March | Lancaster | - | - | 1.1km/400kV | `12964` | y |
| 1285 | 52.6 | 100 | bess | PRE_CONSENT | Dunballoch Farm, Dunballoch - Battery Energy Storage | Field Energy | Scottish Government (S36) | - | - | 0.5km/275kV | `16724` | y |
| 1286 | 52.6 | 100 | bess | PRE_CONSENT | Newfields Farm - Battery Energy Storage | REPD Limited | Staffordshire Moorlands | - | - | 0.2km/132kV | `14342` | **n** |
| 1287 | 52.6 | 100 | bess | PRE_CONSENT | Bay Gateway - Battery Storage Facility | Energi Generation | Lancaster | 2022-04-26 | - | 0.7km/132kV | `17028` | y |
| 1288 | 52.5 | 2 | solar | PAST_EXPECTED_START | East Surrey Hospital, Canada Avenue -Solar Panels | Carbon3 | Reigate and Banstead | 2025-11-11 | 293 | 3.5km/132kV | `19745` | y |
| 1289 | 52.5 | 6 | solar | PAST_EXPECTED_START | Uckfield Solar Electric Forecourt | Gridserve Sustainable Energy | Wealden | 2021-03-16 | 1994 | 1.7km/400kV | `7447` | y |
| 1290 | 52.5 | 6 | solar | PAST_EXPECTED_START | Clapham Plateau - Solar Farm | Sirius Renewable Energy | Bedford | 2023-01-25 | 1314 | 1.2km/132kV | `11699` | y |
| 1291 | 52.5 | 22 | solar | PAST_EXPECTED_START | Billingbear Solar Farm | WT Energy Limited | Windsor and Maidenhead | 2024-07-26 | 766 | 0.6km/132kV | `12584` | y |
| 1292 | 52.5 | 36 | bess | PRE_CONSENT | Lochluichart East, Ardachy - Battery Energy Storage ... | Boralex | Highland | - | - | 0.3km/132kV | `18520` | y |
| 1293 | 52.5 | 36 | solar | PRE_CONSENT | Two Mile Lane, Highnam - Solar Farm | O&G Solar SPV 52 Limited | Tewkesbury | - | - | 1.8km/400kV | `20772` | y |
| 1294 | 52.5 | 46 | solar | PAST_EXPECTED_START | Welby Solar Farm, Welby - Solar Farm | Island Green Power | South Kesteven | 2025-02-10 | 567 | 0.7km/132kV | `15194` | y |
| 1295 | 52.5 | 12 | solar | PAST_EXPECTED_START | Denfield - Solar Farm | Peter J Stirling Limited | Angus | 2025-02-14 | 563 | 1.2km/132kV | `15197` | **n** |
| 1296 | 52.5 | 340 | bess | PRE_CONSENT | Pittlesheugh Farm Bess, Springwells Farmhouse - Batt... | The Energy Workshop | Scottish Government (S36) | - | - | 0.8km/400kV | `14542` | y |
| 1297 | 52.4 | 35 | solar | PRE_CONSENT | Boyah Grange Solar Farm, Potato Pit Lane - Solar Far... | ABEI Energy Group | Erewash | - | - | 1.3km/132kV | `18689` | y |
| 1298 | 52.3 | 57 | bess | DESIGN_FROZEN_OR_LATER | Whitegate Battery Storage | Pelagic Energy (Constantine Energy... | Oldham | 2022-05-19 | - | 0.2km/275kV | `10690` | y |
| 1299 | 52.3 | 57 | bess | DESIGN_FROZEN_OR_LATER | Monk Fryston Battery Storage | Pelagic Energy / Constantine | North Yorkshire | 2022-08-01 | - | 0.1km/400kV | `19593` | y |
| 1300 | 52.3 | 12 | solar | PAST_EXPECTED_START | Land North of Balbeggie Avenue | North Gisborne | Fife | 2016-03-29 | 3807 | 0.7km/132kV | `5800` | y |
| 1301 | 52.3 | 12 | solar | PAST_EXPECTED_START | Bumpers Farm Phase 2 | Anesco | Buckinghamshire | 2015-10-26 | 3962 | 1.0km/132kV | `6282` | y |
| 1302 | 52.3 | 12 | solar | PAST_EXPECTED_START | Manor Farm | Iqony SENS UK Limited / Wessex Sol... | Buckinghamshire | 2022-06-07 | 1546 | 0.4km/400kV | `8079` | y |
| 1303 | 52.3 | 44 | solar | PAST_EXPECTED_START | Pool Farm, Mill Lane, Stratton - Solar Farm | JBM Solar Projects Limited | Cherwell | 2025-05-21 | 467 | 2.3km/132kV | `13032` | y |
| 1304 | 52.3 | 9 | solar | PAST_EXPECTED_START | Green Lane, Nempnett Thrubwell - Solar Farm | Green Switch Capital Limited | North Somerset | 2022-10-04 | 1427 | 1.1km/132kV | `10611` | y |
| 1305 | 52.3 | 2 | solar | PAST_EXPECTED_START | VPK Desborough, Stoke Albany Road, Desborough - Sola... | SNRG | North Northamptonshire | 2025-09-25 | 340 | 3.5km/400kV | `19672` | y |
| 1306 | 52.2 | 20 | solar | PAST_EXPECTED_START | Mopes Lane, Purton - Solar Farm | Spring Dev 08 Limited | Wiltshire | 2023-04-15 | 1234 | 1.8km/132kV | `9849` | y |
| 1307 | 52.2 | 20 | solar | PRE_CONSENT | Potters~ Hill Solar Photovoltaic Arrays | JBM Solar Projects 39 Limited | Melton | - | - | 0.7km/132kV | `16371` | y |
| 1308 | 52.2 | 20 | bess | PAST_EXPECTED_START | Peel Road - Battery Storage | Energi Generation | Fylde | 2023-09-06 | 1090 | 0.2km/132kV | `17226` | y |
| 1309 | 52.2 | 20 | solar | PRE_CONSENT | Aston Grange, Aston - Solar Panels & Battery Energy ... | Innova Renewables | Cheshire West and Chester | - | - | 0.4km/132kV | `18375` | y |
| 1310 | 52.2 | 20 | bess | PRE_CONSENT | Hill House Farm, Coventry Road - Battery Energy Stor... | Root Power South Limited | Solihull | - | - | 0.5km/275kV | `18866` | y |
| 1311 | 52.2 | 20 | bess | PAST_EXPECTED_START | Aikengall, Innerwick - Battery Energy Storage | Redstone Rig Storage Limited | East Lothian | 2024-08-16 | 745 | 0.4km/400kV | `4526` | y |
| 1312 | 52.2 | 5 | solar | PAST_EXPECTED_START | Sulhamstead Solar Field - Stud Farm | Mulbrick Clean Energy | West Berkshire | 2017-04-12 | 3428 | 1.1km/400kV | `5416` | **n** |
| 1313 | 52.2 | 5 | solar | PAST_EXPECTED_START | Lower Tregeen Farm | Powerquinn | Cornwall | 2016-04-15 | 3790 | 1.6km/132kV | `5954` | y |
| 1314 | 52.2 | 5 | bess | PAST_EXPECTED_START | Jenny Field Drive | Enstor Power | North Yorkshire | 2018-01-19 | 3146 | 0.4km/132kV | `7075` | y |
| 1315 | 52.2 | 5 | bess | PAST_EXPECTED_START | Dellsome Power Hatfield Grid Station - Energy storag... | AMP Energy Services Limited | Welwyn Hatfield | 2021-07-09 | 1879 | 0.0km/132kV | `9019` | y |
| 1316 | 52.2 | 5 | solar | PAST_EXPECTED_START | Middlewich Road - Solar Photovoltaics & Battery Stor... | Cheshire East Council | Cheshire East | 2022-03-11 | 1634 | 0.3km/132kV | `9565` | y |
| 1317 | 52.2 | 5 | bess | PAST_EXPECTED_START | Welwyn Power - Energy Storage Facility | AMP Energy Services Limited | Welwyn Hatfield | 2022-08-05 | 1487 | 1.9km/132kV | `11536` | y |
| 1318 | 52.2 | 5 | solar | PAST_EXPECTED_START | Copes Rough Wood, Lower House Lane - Solar Farm | Fields Form Solar Limited | North Warwickshire | 2023-09-08 | 1088 | 2.7km/132kV | `12178` | y |
| 1319 | 52.2 | 5 | solar | PAST_EXPECTED_START | Silver Lane, Risley - Solar Farm | Biffa Waste Services Limited | Warrington | 2023-08-04 | 1123 | 1.6km/132kV | `12643` | y |
| 1320 | 52.2 | 5 | bess | PAST_EXPECTED_START | Letchworth Garden City - Urban Reserve Energy Storag... | AMP Energy Services Limited | North Hertfordshire | 2024-04-10 | 873 | 0.9km/400kV | `15927` | y |
| 1321 | 52.1 | 15 | solar | PAST_EXPECTED_START | Marksbury Plain - Solar Park | Renewable Connections Developments... | Bath and North East Somerset | 2022-07-01 | 1522 | 5.8km/132kV | `10525` | y |
| 1322 | 52.1 | 15 | solar | PAST_EXPECTED_START | Bengrove Farm, Base Lane - Solar Farm | Sonnedix Bengrove Limited | Tewkesbury | 2024-10-21 | 679 | 1.0km/132kV | `15882` | y |
| 1323 | 52.1 | 42 | solar | PRE_CONSENT | Burton Gorse Plantation, Whitecross Lane - Solar Pan... | Starlight Energy | North Kesteven | - | - | 0.2km/132kV | `17363` | y |
| 1324 | 52.1 | 42 | solar | PRE_CONSENT | Redisham Hall Farm, School Road - Solar Panels | Opdenergy | East Suffolk | - | - | 1.2km/132kV | `18465` | **n** |
| 1325 | 52.1 | 400 | bess | PRE_CONSENT | Lagrae Battery Energy Storage System | Buccleuch Estates Limited | Scottish Government (S36) | - | - | 7.5km/132kV | `15529` | y |
| 1326 | 52.1 | 25 | solar | DESIGN_FROZEN_OR_LATER | Tolldish Hall Farm, Parrotts Grove - Solar Photovolt... | Novus Renewable Services Limited | Rugby | 2023-08-31 | - | 0.6km/400kV | `12597` | y |
| 1327 | 52.1 | 25 | solar | PAST_EXPECTED_START | Home Farm | Canadian Solar / Novergy | Wychavon | 2025-05-16 | 472 | 7.0km/132kV | `14306` | y |
| 1328 | 52.1 | 2 | solar | PAST_EXPECTED_START | Komatsu UK, Durham Road - Solar Panels | Komatsu UK Limited | Gateshead | 2024-12-19 | 620 | 1.5km/132kV | `17788` | y |
| 1329 | 52.1 | 5 | bess | PAST_EXPECTED_START | Union Court Storage Facility | Infinis Solar Developments Limited | Bolton | 2021-10-12 | 1784 | 0.1km/132kV | `14862` | **n** |
| 1330 | 52.1 | 4 | solar | PRE_CONSENT | Wervin Road, Wervin - Solar PV Panels | North England Zoological Departmen... | Cheshire West and Chester | - | - | 0.5km/400kV | `20800` | y |
| 1331 | 52.0 | 4 | solar | PRE_CONSENT | Newhouse, Biggar Road -Solar Array | Ampyr Distribution Energy | North Lanarkshire | - | - | 0.2km/275kV | `20641` | y |
| 1332 | 52.0 | 11 | solar | PAST_EXPECTED_START | Wittering Ford Road, Barnack - Solar Photovoltaic Fa... | Larkfleet limited | Peterborough | 2023-11-15 | 1020 | 3.7km/132kV | `13389` | y |
| 1333 | 51.9 | 40 | bess | PAST_EXPECTED_START | Whitehouse Farm Energy Barn | Bluefield Solar Income Fund | Malvern Hills | 2017-11-29 | 3197 | 0.4km/132kV | `7987` | y |
| 1334 | 51.9 | 40 | solar | PAST_EXPECTED_START | Thaxted - Solar farm | Low Carbon Limited | Uttlesford | 2022-09-29 | 1432 | 0.4km/132kV | `8476` | y |
| 1335 | 51.9 | 40 | bess | PAST_EXPECTED_START | Forest Gate - Solar Farm & Battery Storage | Eden Renewables | Wiltshire | 2023-03-10 | 1270 | 0.9km/132kV | `9229` | y |
| 1336 | 51.9 | 40 | bess | PRE_CONSENT | Brinsworth Road, Brinsworth - Battery Energy storage | Root Power South Limited | Rotherham | - | - | 0.4km/275kV | `17119` | y |
| 1337 | 51.9 | 40 | solar | PRE_CONSENT | Caswell Farm, Common Lane - Solar Farm | GridSource Limited | Dorset | - | - | 2.5km/132kV | `19147` | y |
| 1338 | 51.9 | 40 | bess | PRE_CONSENT | Hardybarn Lane, Green Fairfield - Battery Energy Sto... | S & L Energy Limited | High Peak | 2025-06-23 | - | 1.2km/132kV | `21092` | y |
| 1339 | 51.9 | 11 | solar | PAST_EXPECTED_START | Letch Lane - Solar Farm | Anesco Limited | Stockton-on-Tees | 2021-12-15 | 1720 | 0.2km/132kV | `9683` | y |
| 1340 | 51.9 | 2 | solar | PAST_EXPECTED_START | Middleton Road, Linwood - Solar Photovoltaic Panels | Scottish Water Horizons | Renfrewshire | 2025-01-23 | 585 | 1.4km/132kV | `16294` | y |
| 1341 | 51.8 | 2 | solar | PAST_EXPECTED_START | Coal Road, Whinmoor - Solar Panels | Unilever UK (Leeds) | Leeds | 2025-08-08 | 388 | 1.0km/132kV | `19055` | y |
| 1342 | 51.8 | 2 | solar | PAST_EXPECTED_START | VPK Wellington, Chelston Business Park - Solar Panel | SNRG | Somerset | 2025-08-15 | 381 | 1.0km/400kV | `19181` | y |
| 1343 | 51.8 | 39 | solar | PAST_EXPECTED_START | Old Chalk Pit, West Back Side - Three Oaks Renewable... | Ridge Clean Energy Limited | East Riding of Yorkshire | 2024-03-21 | 893 | 11.6km/132kV | `12526` | y |
| 1344 | 51.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Cowbridge Road, Bicker Fen - Battery Storage | AGR Solar 2 Limited | South Holland | 2023-07-21 | - | 0.6km/400kV | `12117` | y |
| 1345 | 51.8 | 50 | solar | PRE_CONSENT | Kintore - Solar Photovoltaic Array | Mespil Solar Energy | Scottish Government (S36) | - | - | 0.4km/132kV | `17471` | y |
| 1346 | 51.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Soay Solar Farm and Greener Grid Park | Statkraft Uk Limited | East Riding of Yorkshire | 2022-11-28 | - | 1.1km/400kV | `10586` | y |
| 1347 | 51.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Cutbush Farm, Belchamp St Paul - Solar Array | British Solar Renewables | Braintree | 2024-12-09 | - | 0.3km/132kV | `11329` | y |
| 1348 | 51.8 | 50 | solar | PAST_EXPECTED_START | Bluestone Farm, Low Lands - Solar Farm | Bluefield Renewable Developments L... | County Durham | 2024-05-28 | 825 | 8.1km/132kV | `13339` | y |
| 1349 | 51.8 | 30 | solar | PAST_EXPECTED_START | Berrington Farm - Solar Array | Econergy International Limited | Shropshire | 2025-05-02 | 486 | 5.7km/400kV | `12266` | y |
| 1350 | 51.8 | 30 | solar | PAST_EXPECTED_START | Woodlands Manor Farm, Horton - Solar Farm | BayWa r.e. UKLimited / Grüne Ener... | Dorset | 2025-05-07 | 481 | 2.3km/132kV | `14287` | y |
| 1351 | 51.8 | 30 | solar | PRE_CONSENT | Ashby Dell, Border Lane - Solar Farm | Sky UK Development Limited | East Suffolk | - | - | 1.1km/132kV | `19885` | y |
| 1352 | 51.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Wick Farm Melksham Substation | JBM Solar Projects | Wiltshire | 2021-12-17 | - | 0.2km/132kV | `8063` | y |
| 1353 | 51.8 | 50 | solar | PAST_EXPECTED_START | Crudwell Road Solar Farm & Battery Storage | Five Lanes Solar Limited | Wiltshire | 2023-08-23 | 1104 | 5.9km/400kV | `8919` | y |
| 1354 | 51.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Harrington Franklin, Richborough Energy Park - Batte... | EDP Renewables | Dover | 2022-12-06 | - | 0.3km/132kV | `11449` | y |
| 1355 | 51.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Overhill Farm, Rothienorman - Battery Energy Storage | One Planet Developments Limited | Aberdeenshire | 2023-03-01 | - | 0.6km/400kV | `11590` | y |
| 1356 | 51.8 | 2 | solar | PAST_EXPECTED_START | Rolls Royce Plc, Radial Park Road - Solar Panels | Rolls Royce | Sunderland | 2024-12-09 | 630 | 0.3km/132kV | `17380` | y |
| 1357 | 51.8 | 14 | solar | PRE_CONSENT | Firsby Lane, Hooton Roberts - Solar Panels | ILOS | Rotherham | - | - | 1.0km/275kV | `18281` | y |
| 1358 | 51.7 | 49 | solar | PAST_EXPECTED_START | The Old Airfield - Solar Farm | Peridot Solar Limited | Shropshire | 2023-03-09 | 1271 | 9.1km/132kV | `8525` | y |
| 1359 | 51.7 | 4 | solar | PAST_EXPECTED_START | Brassington Works, Manystones Lane - Solar Farm | Hoben International Limited | Derbyshire Dales | 2024-10-17 | 683 | 0.2km/132kV | `15448` | y |
| 1360 | 51.7 | 4 | solar | PAST_EXPECTED_START | Shepcote Lane - Solar Photovoltaic Panels | Peel Logistics Property | Sheffield | 2023-08-04 | 1123 | 0.2km/132kV | `14027` | y |
| 1361 | 51.7 | 2 | bess | PAST_EXPECTED_START | Stanborough, Hatfield - Battery Energy Storage Syste... | J Reddington Limited | Welwyn Hatfield | 2024-09-16 | 714 | 0.9km/132kV | `14878` | y |
| 1362 | 51.7 | 80 | bess | PRE_CONSENT | Springfield - Solar Farm & Battery Energy Storage | Voltalia UK Limited | Scottish Government (S36) | - | - | 2.2km/132kV | `19016` | y |
| 1363 | 51.6 | 10 | bess | PAST_EXPECTED_START | Old Green Farm, Alveston Battery Storage | Ecotricity | South Gloucestershire | 2019-11-17 | 2479 | 0.0km/132kV | `7182` | y |
| 1364 | 51.6 | 10 | bess | PAST_EXPECTED_START | Bradley Road - Battery Energy Storage System | Renewable Connections Developments... | North East Lincolnshire | 2024-04-26 | 857 | 1.2km/132kV | `13862` | y |
| 1365 | 51.6 | 17 | solar | PAST_EXPECTED_START | Ringmer - Solar array/Battery storage | Ouse Valley Energy Services Compan... | Lewes | 2023-01-19 | 1320 | 2.1km/132kV | `11163` | y |
| 1366 | 51.6 | 1 | solar | PAST_EXPECTED_START | J S Davidson Limited, Shrewsbury Avenue - Solar PV p... | Chiltern Cold Storage Group Limite... | Peterborough | 2024-09-27 | 703 | 1.0km/132kV | `16890` | y |
| 1367 | 51.6 | 1 | solar | PAST_EXPECTED_START | Rothley Lodge, Loughborough Road - Solar Panels | Sofidel UK Limited | Charnwood | 2025-03-28 | 521 | 1.9km/400kV | `18226` | y |
| 1368 | 51.6 | 78 | solar | DESIGN_FROZEN_OR_LATER | Gainsborough Road, Saundby - Solar Farm | Enso Energy / Cero Generation | Bassetlaw | 2022-07-14 | - | 0.6km/400kV | `9815` | y |
| 1369 | 51.5 | 60 | solar | PAST_EXPECTED_START | Frodo Solar and Battery Energy Development | Green Energy International | Scottish Government (S36) | 2023-05-16 | 1203 | 1.3km/132kV | `10994` | y |
| 1370 | 51.5 | 60 | bess | PRE_CONSENT | Bungalow Farm, Smeaton Lane - Battery Energy Storage | Integrum Renewable Energy Limited | Rugby | - | - | 0.4km/132kV | `16585` | y |
| 1371 | 51.5 | 60 | bess | PRE_CONSENT | Bungalow Farm, Smeaton Lane - Battery Energy Storage... | Integrum Renewable Energy Limited | Rugby | - | - | 0.5km/132kV | `18124` | y |
| 1372 | 51.5 | 36 | solar | PAST_EXPECTED_START | Wood End, Mursley Road | Elgin Energy | Buckinghamshire | 2022-12-02 | 1368 | 0.6km/132kV | `7605` | y |
| 1373 | 51.5 | 36 | bess | PRE_CONSENT | Kingston Road, Slimbridge - Battery Storage | Relay Slimbridge Limited | Stroud | - | - | 0.3km/132kV | `14882` | y |
| 1374 | 51.5 | 1 | solar | PAST_EXPECTED_START | Pen Y Dre High School, Goitre Lane - Solar Panels | Merthyr Tydfil County Borough Coun... | Merthyr Tydfil | 2025-05-08 | 480 | 0.5km/132kV | `18337` | y |
| 1375 | 51.5 | 16 | solar | PAST_EXPECTED_START | Corley Smorral Lane - Photovoltaic Solar Arrays | Barrs Family Enterprises Limited | North Warwickshire | 2022-07-27 | 1496 | 0.6km/275kV | `10067` | **n** |
| 1376 | 51.5 | 10 | bess | PAST_EXPECTED_START | Oil Sites Road | UK Power Reserve | Cheshire West and Chester | 2017-10-30 | 3227 | 0.5km/132kV | `6936` | y |
| 1377 | 51.5 | 4 | solar | PAST_EXPECTED_START | Leyland Trucks Limited, Croston Road - Solar Panels | Leyland Trucks Limited | South Ribble | 2024-05-21 | 832 | 0.8km/400kV | `16262` | y |
| 1378 | 51.4 | 4 | solar | PAST_EXPECTED_START | Wynyard Business Park, North Chapell Lane - Solar Pa... | Northumberland Estates Limited | Stockton-on-Tees | 2022-10-06 | 1425 | 0.7km/400kV | `11993` | y |
| 1379 | 51.4 | 35 | solar | PAST_EXPECTED_START | Higher Stockbridge Farm | Voltalia UK | Dorset | 2021-12-08 | 1727 | 0.3km/132kV | `7817` | y |
| 1380 | 51.4 | 35 | solar | PRE_CONSENT | Appledore Road, Kenardington - Solar Farm | Quintas Cleantech | Ashford | - | - | 1.8km/132kV | `17906` | y |
| 1381 | 51.4 | 1 | solar | PAST_EXPECTED_START | Lundwood, Sewage Works - Solar Array | Downing Energy Development Company... | Barnsley | 2024-01-12 | 962 | 0.6km/132kV | `14052` | y |
| 1382 | 51.4 | 16 | bess | PAST_EXPECTED_START | J3 Business Park - Battery Storage Facility | Forepower Limited | Doncaster | 2023-07-11 | 1147 | 0.6km/132kV | `14054` | y |
| 1383 | 51.4 | 16 | bess | PAST_EXPECTED_START | Allington Lane - Solar & Battery Farm | Eastleigh Borough Council | Eastleigh | 2024-07-26 | 766 | 2.0km/400kV | `14584` | y |
| 1384 | 51.4 | 1 | solar | PAST_EXPECTED_START | Intu Lakeside, West Thurrock Way - Solar Panels | Global Mutual | Thurrock | 2024-09-12 | 718 | 0.4km/400kV | `16778` | y |
| 1385 | 51.3 | 1 | solar | PAST_EXPECTED_START | Sun Fields, Gelli Bwch Farm -Solar Array | Hale Construction Limited | Neath Port Talbot | 2025-04-22 | 496 | 1.0km/275kV | `12911` | y |
| 1386 | 51.3 | 1 | solar | PAST_EXPECTED_START | Jaguar Landrover Phoenix Building, Eric Foundation R... | Jaguar | Cheshire West and Chester | 2025-04-17 | 501 | 1.1km/132kV | `18362` | y |
| 1387 | 51.3 | 1 | solar | PAST_EXPECTED_START | British Aerospace Airbus, Chester Road - Solar Panel... | British Aerospace Airbus Limited | Flintshire | 2025-09-15 | 350 | 2.8km/132kV | `19231` | y |
| 1388 | 51.3 | 57 | bess | PRE_CONSENT | Plas Power Estate Solar Farm | Lightsource BP | Welsh Government (NSIP) | - | - | 1.3km/132kV | `7858` | y |
| 1389 | 51.3 | 57 | bess | PRE_CONSENT | Cut Lane - Battery Energy Storage System | Pivoted Power Llp | Knowsley | - | - | 0.2km/275kV | `16131` | y |
| 1390 | 51.3 | 57 | solar | PRE_CONSENT | Plas Power Estate Solar Farm | Lightsource BP | Welsh Government (NSIP) | - | - | 1.3km/132kV | `18491` | y |
| 1391 | 51.3 | 57 | bess | PRE_CONSENT | Hallfield Farm, Easington - Battery Storage | Eden Renewables | County Durham | - | - | 1.2km/400kV | `18987` | y |
| 1392 | 51.3 | 12 | solar | PAST_EXPECTED_START | Bath Road, Grange Lane - Solar Photovoltaic Array | Grundon Waste Management Limited | West Berkshire | 2025-03-28 | 521 | 5.1km/400kV | `14924` | y |
| 1393 | 51.3 | 7 | solar | PAST_EXPECTED_START | The Hut Group, Skyline Drive - Solar Array | Olympus Power | Warrington | 2025-07-02 | 425 | 0.3km/132kV | `18815` | y |
| 1394 | 51.3 | 9 | solar | PAST_EXPECTED_START | White Horse Lane (Trowse) - Phase 2 | Wirsol | South Norfolk | 2021-09-17 | 1809 | 0.0km/132kV | `6360` | y |
| 1395 | 51.3 | 9 | solar | PAST_EXPECTED_START | Broken Scar Water Treatment Works Solar Farm | Northumbrian Water Limited | North Yorkshire | 2022-06-13 | 1540 | 0.3km/132kV | `9437` | y |
| 1396 | 51.2 | 15 | solar | PRE_CONSENT | Hackworth Road, North West Industrial Estate - Solar... | ABEI Energy Green IX Limited | County Durham | - | - | 2.4km/400kV | `19425` | y |
| 1397 | 51.2 | 20 | bess | PAST_EXPECTED_START | The Brickmakers Arms Battery | FPC Industry & Enterprise 2 Limite... | Bedford | 2021-12-22 | 1713 | 2.6km/132kV | `9668` | y |
| 1398 | 51.2 | 4 | solar | PAST_EXPECTED_START | Farlington Water Treatment Works, Gillman Road - Sol... | Portsmouth Water Limited | Portsmouth | 2022-11-25 | 1375 | 1.3km/132kV | `12107` | y |
| 1399 | 51.2 | 7 | bess | PAST_EXPECTED_START | Somerford Farm, Brinkworth - Battery Storage | Pelagic Energy | Wiltshire | 2024-10-17 | 683 | 2.0km/132kV | `11073` | y |
| 1400 | 51.2 | 1 | solar | PAST_EXPECTED_START | Westerleigh Solar, Oakleigh Green Farm Lane - Solar ... | EDF Energy Renewables Limited | South Gloucestershire | 2025-06-13 | 444 | 0.5km/132kV | `18278` | y |
| 1401 | 51.1 | 15 | solar | PAST_EXPECTED_START | Billericay Solar Farm - Solar Farm | Conrad Energy | Brentwood | 2025-04-30 | 488 | 2.4km/132kV | `17500` | y |
| 1402 | 51.1 | 15 | solar | PAST_EXPECTED_START | Green Lane Solar Park - Solar PV Panels | Sky UK Development Limited | King's Lynn and West Norfolk | 2025-10-14 | 321 | 15.8km/132kV | `19378` | y |
| 1403 | 51.1 | 25 | solar | PRE_CONSENT | Low Raisby Farm, Kelloe - Solar Panels | ABEI Energy Green II | County Durham | - | - | 0.4km/275kV | `19724` | y |
| 1404 | 51.1 | 33 | solar | PAST_EXPECTED_START | Poppleton Solar Farm | Ampyr Solar Europe UK Holdings Lim... | York | 2024-10-08 | 692 | 0.4km/275kV | `12159` | y |
| 1405 | 51.1 | 25 | solar | PRE_CONSENT | Knockair, Dougliehill Road - Solar Farm | Renewco Power | Inverclyde | - | - | 1.5km/132kV | `19964` | y |
| 1406 | 51.1 | 1 | solar | PAST_EXPECTED_START | Deritend Precision Casting, Vines Lane - Solar Panel... | Green Nation Solar Energy | Wychavon | 2025-05-23 | 465 | 2.6km/132kV | `18558` | y |
| 1407 | 51.1 | 1 | solar | PAST_EXPECTED_START | Data Centre, Dennison House, Stanhope Road - Solar P... | Electron Green | Surrey Heath | 2025-01-13 | 595 | 0.8km/132kV | `17227` | **n** |
| 1408 | 51.1 | 32 | solar | PRE_CONSENT | Fourstones Substation, Fourstones - Solar Farm & Bat... | ER New Projects 2 Limited | Northumberland | - | - | 0.7km/275kV | `18960` | y |
| 1409 | 51.0 | 2 | solar | PAST_EXPECTED_START | Wildersmoor Hall Farm, Higher Lane - Solar Farm | Lymm Community Energy Limited | Warrington | 2025-11-21 | 283 | 0.5km/132kV | `16031` | y |
| 1410 | 51.0 | 1 | solar | PAST_EXPECTED_START | Brookfields Park, Brookfields Drive - Solar PV Panel... | Next Distribution Limited | Rotherham | 2024-06-10 | 812 | 0.5km/132kV | `16302` | y |
| 1411 | 51.0 | 1 | solar | PAST_EXPECTED_START | City Football Academy - Solar Panels | Manchester City Football Club | Manchester | 2024-12-17 | 622 | 1.0km/132kV | `17465` | y |
| 1412 | 51.0 | 1 | solar | PAST_EXPECTED_START | Bentley Motors Limited, Pyms Lane - Solar Panels | 3ti Energy Hubs Limited | Cheshire East | 2025-05-16 | 472 | 0.6km/132kV | `18673` | y |
| 1413 | 51.0 | 1 | solar | PAST_EXPECTED_START | Wienerberger, Castle Road - Solar Panels | Olympus Power | Swale | 2024-08-12 | 749 | 0.5km/400kV | `16615` | y |
| 1414 | 51.0 | 1 | solar | PAST_EXPECTED_START | Brookfields Park, Brookfields Drive - Solar PV Panel... | Next Distribution Limited | Rotherham | 2024-06-10 | 812 | 0.5km/132kV | `17076` | y |
| 1415 | 51.0 | 500 | bess | PRE_CONSENT | Rothienorman, Middleton of Blackhills - BESS | Blackford Renewables Limited | Scottish Government (S36) | - | - | 5.9km/400kV | `18504` | y |
| 1416 | 51.0 | 300 | bess | DESIGN_FROZEN_OR_LATER | Blackhillock Electricity Substation - Battery Energy... | Zenobe Energy Limited | Scottish Government (S36) | 2022-02-28 | - | 0.2km/132kV | `9723` | y |
| 1417 | 50.9 | 24 | bess | PRE_CONSENT | Knockair, Dougliehill Road - Battery Storage Facilit... | Renewco Power | Inverclyde | - | - | 1.5km/132kV | `19963` | y |
| 1418 | 50.9 | 14 | bess | PAST_EXPECTED_START | Pershore Lane, Tibberton - Battery Energy Storage Sy... | Sirius Renewable Energy | Wychavon | 2023-10-27 | 1039 | 0.3km/132kV | `13096` | y |
| 1419 | 50.8 | 14 | solar | PAST_EXPECTED_START | Cressing Farm, Witham Road - Solar Farm | Eden Renewables | Braintree | 2025-06-06 | 451 | 2.6km/400kV | `12123` | y |
| 1420 | 50.8 | 8 | bess | PAST_EXPECTED_START | Bowesfield Flexible Energy Park | Banks Group | Stockton-on-Tees | 2021-10-15 | 1781 | 3.4km/400kV | `8399` | y |
| 1421 | 50.8 | 8 | bess | PAST_EXPECTED_START | Bridge Farm, Uffington - Battery Energy Storage | Hydrock | Shropshire | 2023-04-19 | 1230 | 0.4km/400kV | `13161` | y |
| 1422 | 50.8 | 6 | bess | PAST_EXPECTED_START | Abbotsley Country Homes, Drewels Lane - Solar Farm | Low Carbon Limited | Huntingdonshire | 2025-01-31 | 577 | 2.0km/132kV | `13629` | y |
| 1423 | 50.8 | 6 | solar | PAST_EXPECTED_START | Strichen Solar Project, Clayfords Farm - Solar Panel... | Solar Farm Number 2 | Aberdeenshire | 2024-11-19 | 650 | 1.2km/132kV | `17030` | y |
| 1424 | 50.8 | 6 | solar | PRE_CONSENT | Emergency Air Operation Base, Gloucester Road - Sola... | Bristol Energy | South Gloucestershire | - | - | 0.4km/132kV | `19780` | y |
| 1425 | 50.8 | 50 | bess | PRE_CONSENT | Burnt House Farm, Nedderton Village - Battery Energy... | Bluefield Renewable Developments L... | Northumberland | - | - | 0.6km/400kV | `9739` | y |
| 1426 | 50.8 | 50 | bess | PAST_EXPECTED_START | Frodo Solar and Battery Energy Development | Green Energy International | Scottish Government (S36) | 2023-05-16 | 1203 | 1.3km/132kV | `10993` | y |
| 1427 | 50.8 | 30 | bess | PRE_CONSENT | Weirs Drove, Burwell - Battery Storage Facility | Fen Power 1 Limited | East Cambridgeshire | - | - | 0.1km/400kV | `7272` | **n** |
| 1428 | 50.8 | 30 | solar | PAST_EXPECTED_START | Welsh Lane | Low Carbon | West Northamptonshire | 2021-11-25 | 1740 | 2.0km/132kV | `8056` | y |
| 1429 | 50.8 | 30 | solar | PRE_CONSENT | Green Lane, Stewartby - Solar PV Array | Infinis Solar Developments Limited | Bedford | - | - | 1.6km/132kV | `9077` | y |
| 1430 | 50.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Maes Mawr Solar | Elgin Energy EsCo Ltd | Welsh Government (NSIP) | 2023-12-21 | - | 0.4km/275kV | `9981` | y |
| 1431 | 50.8 | 30 | bess | PAST_EXPECTED_START | West Bendings - Battery Storage | Fiddes Battery Limited | Aberdeenshire | 2023-06-29 | 1159 | 0.1km/132kV | `10985` | y |
| 1432 | 50.8 | 30 | solar | PAST_EXPECTED_START | Parkend Crossgates - Solar Panels & Battery Storage | Greentech Projects Holding UK Limi... | Fife | 2024-03-07 | 907 | 2.7km/132kV | `11862` | y |
| 1433 | 50.8 | 30 | solar | PRE_CONSENT | Chalgrave Manor Solar Farm | R Upchurch & Partners | Central Bedfordshire | - | - | 0.4km/132kV | `12490` | y |
| 1434 | 50.8 | 30 | bess | PRE_CONSENT | Scawby Road - Solar Array | Brockwell Storage & Solar Limited | North Lincolnshire | - | - | 0.5km/132kV | `12607` | y |
| 1435 | 50.8 | 30 | solar | PAST_EXPECTED_START | Amington Hall Farm - Solar Farm | Tamworth Solar Limited | Tamworth | 2025-02-26 | 551 | 0.5km/132kV | `13371` | y |
| 1436 | 50.8 | 30 | bess | PRE_CONSENT | Frome Power, Styles Close - Energy Storage Facility | Trina Solar UK Hold Co Limited | Somerset | - | - | 0.1km/132kV | `14227` | y |
| 1437 | 50.8 | 30 | bess | PRE_CONSENT | West Fen Farm, Whitemoor Road - Battery Storage | Pathfinder Clean Energy UK Dev Lim... | Fenland | - | - | 0.6km/132kV | `15271` | y |
| 1438 | 50.8 | 30 | bess | PRE_CONSENT | Tanners Lane - Battery Energy Storage System | Tag Energy Development UK Limited | Solihull | - | - | 0.1km/132kV | `17526` | y |
| 1439 | 50.8 | 30 | bess | PRE_CONSENT | Stirches Renewable Energy Park - Solar Panels & Batt... | IB Vogt UK Limited | Scottish Government (S36) | - | - | 0.7km/132kV | `18030` | y |
| 1440 | 50.8 | 30 | solar | PRE_CONSENT | Stirches Renewable Energy Park - Solar Panels & Batt... | IB Vogt UK Limited | Scottish Government (S36) | - | - | 0.7km/132kV | `18031` | y |
| 1441 | 50.8 | 30 | solar | PRE_CONSENT | Hob Lane, Dunham On The Hill - Solar Farm | Belltown Power Limited | Cheshire West and Chester | - | - | 0.9km/400kV | `19082` | y |
| 1442 | 50.8 | 30 | bess | PRE_CONSENT | Gunnerby Road - 30MW Battery Energy Storage | Grenergy Renewables UK Limited | North East Lincolnshire | - | - | 0.6km/132kV | `19506` | y |
| 1443 | 50.8 | 50 | solar | PRE_CONSENT | Bolt Hall Farm, Lark Hill Road - Solar Photovoltaic ... | Green Switch Capital Limited | Rochford | - | - | 1.9km/132kV | `11927` | y |
| 1444 | 50.8 | 1 | solar | PAST_EXPECTED_START | ENVA England, Road Number 4 - Solar Panels | ENVA England Limited | Gedling | 2025-07-08 | 419 | 0.7km/400kV | `18794` | y |
| 1445 | 50.8 | 50 | solar | PAST_EXPECTED_START | Wood Lane Solar Farm | Scottish Power Limited | Bassetlaw | 2020-08-27 | 2195 | 0.4km/132kV | `7786` | y |
| 1446 | 50.8 | 50 | bess | PRE_CONSENT | Lovedean Energy Storage System | Anesco | East Hampshire | - | - | 0.1km/132kV | `9257` | y |
| 1447 | 50.8 | 50 | solar | PAST_EXPECTED_START | Tar Solar Farm | Bluefield Renewable Developments L... | West Oxfordshire | 2023-06-27 | 1161 | 0.7km/132kV | `9414` | y |
| 1448 | 50.8 | 50 | solar | PRE_CONSENT | Airfield Farm - Solar Array | Engena Limited | West Lindsey | - | - | 2.2km/132kV | `9891` | y |
| 1449 | 50.8 | 50 | solar | PAST_EXPECTED_START | Bury Farm - Solar Farm | Interguide Group Limited | Buckinghamshire | 2022-07-01 | 1522 | 1.5km/132kV | `10457` | y |
| 1450 | 50.8 | 50 | solar | PRE_CONSENT | Waterditch Farm - Solar Farm & Battery Storage | Meyrick Estate Management Limited | Bournemouth, Christchurch an... | - | - | 2.0km/132kV | `11515` | y |
| 1451 | 50.8 | 50 | bess | PAST_EXPECTED_START | Dormitories Star Inn Farm, Mains Of Fowlis - Battery... | Epsilon Generation | Perth and Kinross | 2023-12-20 | 985 | 0.4km/132kV | `13595` | y |
| 1452 | 50.8 | 50 | solar | PRE_CONSENT | Kenley House Farm, Ferry Road - Solar Farm | Lighthouse Development Consulting | East Riding of Yorkshire | - | - | 0.3km/132kV | `13832` | y |
| 1453 | 50.8 | 50 | solar | PRE_CONSENT | Manor Farm, Wick Lane - Solar Farm & Battery Storage | Qair UK | North Somerset | - | - | 1.4km/132kV | `14332` | y |
| 1454 | 50.8 | 50 | bess | PRE_CONSENT | Old Schoolhouse, Barras - Battery Energy Storage Sys... | Green Switch Capital Limited | Aberdeenshire | - | - | 1.7km/132kV | `15239` | y |
| 1455 | 50.8 | 50 | bess | PRE_CONSENT | Kintore Substation, Leylodge - Battery Energy Storag... | XRE Gamma Limited | Aberdeenshire | - | - | 0.1km/132kV | `15627` | y |
| 1456 | 50.8 | 50 | bess | PRE_CONSENT | Smiddyhill, Strichen - Battery Energy Storage | Muirden Energy | Aberdeenshire | - | - | 0.2km/132kV | `16884` | y |
| 1457 | 50.8 | 50 | solar | PRE_CONSENT | Idleigh Court Road, New Ash Green - Solar Array | Evolution Power | Sevenoaks | - | - | 2.0km/132kV | `17222` | y |
| 1458 | 50.8 | 50 | solar | PRE_CONSENT | Beane Solar Farm - Solar Panels | Renewable Energy Systems RES ltd (... | East Hertfordshire | - | - | 0.8km/132kV | `17726` | y |
| 1459 | 50.8 | 50 | solar | PRE_CONSENT | Engine Lane, Grimethorpe - Solar Farm | Enviromena | Barnsley | - | - | 0.1km/132kV | `18118` | y |
| 1460 | 50.8 | 50 | solar | PRE_CONSENT | Beechtree Junction, Potters Crouch - Solar PV Panels | Exagen Development Limited | St Albans | - | - | 0.2km/400kV | `18698` | y |
| 1461 | 50.8 | 50 | solar | PRE_CONSENT | Hayton House Farm - Solar Farm | Econergy International Limited | Leeds | - | - | 0.3km/132kV | `18950` | y |
| 1462 | 50.8 | 50 | solar | PRE_CONSENT | Hallfield Farm, Easington - Solar Farm | Eden Renewables | County Durham | - | - | 1.2km/400kV | `18988` | y |
| 1463 | 50.8 | 50 | solar | PRE_CONSENT | Butt Lane, Hooton Pagnell - Solar Farm | British Solar Renewables | Doncaster | - | - | 2.1km/275kV | `19249` | y |
| 1464 | 50.8 | 50 | solar | PRE_CONSENT | Green Lane, Moor Monkton - Solar Panels & Battery En... | Eden Renewables | North Yorkshire | - | - | 1.2km/275kV | `19333` | y |
| 1465 | 50.8 | 50 | solar | PRE_CONSENT | Sutton-on-the-Forest, Brownmoor Lane - Solar Park | Ampyr Energy UK Development Limite... | York | - | - | 0.3km/400kV | `19659` | y |
| 1466 | 50.8 | 50 | bess | PRE_CONSENT | Boothby Road - Battery Storage | Opdenergy UK Limted | Aberdeenshire | - | - | 0.6km/132kV | `19944` | y |
| 1467 | 50.8 | 23 | solar | CONSENTED_NO_DATE | Honiley Road - Solar Farm & Battery Storage | Enso Green Holdings Limited | Warwick | - | - | 1.8km/275kV | `12391` | y |
| 1468 | 50.8 | 1 | solar | PAST_EXPECTED_START | Curver Way - Solar Panels | Harvest Green Developments | North Northamptonshire | 2024-11-01 | 668 | 0.9km/132kV | `17241` | y |
| 1469 | 50.8 | 1 | solar | PAST_EXPECTED_START | Responsive Engineering, Scotswood Road - Solar Panel... | Responsive Engineering | Newcastle upon Tyne | 2025-04-25 | 493 | 1.0km/132kV | `18378` | y |
| 1470 | 50.8 | 1 | solar | PAST_EXPECTED_START | Lochhead Farmouse, Lochhead - Solar Photovoltaic Arr... | Laird Aggregates Limited | Angus | 2025-09-02 | 363 | 0.8km/132kV | `19246` | y |
| 1471 | 50.8 | 23 | bess | PRE_CONSENT | Giants Burn Wind Farm -Batter Energy Storage | Statkraft UK Limited | Scottish Government (S36) | - | - | 0.8km/132kV | `16078` | y |
| 1472 | 50.8 | 3 | solar | PAST_EXPECTED_START | Torbay Hospital, Nightingale Park - Solar Panel Arra... | TDA | Torbay | 2022-06-16 | 1537 | 0.3km/132kV | `10367` | y |
| 1473 | 50.7 | 49 | bess | PRE_CONSENT | Dougliehill Water Treatment Works, Dougliehill Road ... | Bluestone Energy | Inverclyde | - | - | 0.8km/132kV | `18293` | y |
| 1474 | 50.7 | 22 | solar | PAST_EXPECTED_START | Park Road - Solar Farm | Novus Renewable Services Limited | Braintree | 2023-12-15 | 990 | 3.3km/400kV | `10530` | y |
| 1475 | 50.7 | 29 | solar | PRE_CONSENT | South Carlton - Solar Panels | Enviromena | West Lindsey | - | - | 1.0km/132kV | `19099` | y |
| 1476 | 50.7 | 62 | solar | DESIGN_FROZEN_OR_LATER | Highfields Farm, Clifton Lane - Solar Panels | Elgin Energy ESCO Limited | Lichfield | 2023-07-11 | - | 0.4km/132kV | `10477` | y |
| 1477 | 50.7 | 48 | solar | PRE_CONSENT | Benridge Farm, Fillpoke Lane - Solar Panels | Development at Benridge Farm | County Durham | - | - | 3.5km/275kV | `18248` | y |
| 1478 | 50.6 | 13 | bess | PAST_EXPECTED_START | Dolly Lane, Buxworth - Battery Storage Facility & Su... | W Rigby & Sons | High Peak | 2024-02-21 | 922 | 0.4km/132kV | `15127` | y |
| 1479 | 50.6 | 48 | bess | PRE_CONSENT | Dog Trap Lane, Minety - Battery Energy Storage Syste... | Pelagic Energy | Wiltshire | - | - | 0.8km/132kV | `11810` | y |
| 1480 | 50.6 | 100 | bess | DESIGN_FROZEN_OR_LATER | Derrymeen Battery Energy Storage System | SSE Renewables | Mid Ulster | 2025-06-30 | - | 5.5km/275kV | `16444` | y |
| 1481 | 50.6 | 100 | bess | PRE_CONSENT | Pelham Road, Upton Magna - Battery Energy Storage Sy... | Elgin Energy Esco Limited | Shropshire | - | - | 0.2km/400kV | `18958` | y |
| 1482 | 50.6 | 100 | bess | PRE_CONSENT | Neil Fox Way - Battery Storage | Harmony Energy Limited | Wakefield | - | - | 0.1km/132kV | `19469` | y |
| 1483 | 50.5 | 28 | solar | PAST_EXPECTED_START | Ranksborough Farm | Elgin Energy | Rutland | 2022-01-13 | 1691 | 0.1km/132kV | `7617` | y |
| 1484 | 50.5 | 28 | solar | PAST_EXPECTED_START | Harewood Whin, Tinker Lane - Solar Farm | Yorwaste Limited | York | 2025-04-28 | 490 | 3.6km/275kV | `15267` | y |
| 1485 | 50.5 | 6 | solar | PRE_CONSENT | Twynersh Meadows, Thorpe Road - Solar Park & Battery... | Runnymede Borough Council | Runnymede | - | - | 0.9km/400kV | `12205` | y |
| 1486 | 50.5 | 36 | solar | PAST_EXPECTED_START | Surmer Hall, Church Walk - Solar Farm & Battery Stor... | Boultbee Brooks (Renewables Rowley... | Braintree | 2024-12-04 | 635 | 5.6km/400kV | `15401` | y |
| 1487 | 50.5 | 46 | solar | PRE_CONSENT | Milton Road, Gayton - Solar Farm | Anesco Limited | West Northamptonshire | - | - | 4.1km/400kV | `9130` | **n** |
| 1488 | 50.4 | 75 | bess | PRE_CONSENT | Power Generation in Development in Claudy | Ballyarton Energy Limited | Derry City and Strabane | - | - | 5.7km/275kV | `19970` | y |
| 1489 | 50.4 | 7 | bess | PAST_EXPECTED_START | Stoneclough - Battery Energy Storage | GAM Capital Limited / Infinis Ener... | Bolton | 2022-10-24 | 1407 | 0.2km/132kV | `11161` | y |
| 1490 | 50.3 | 12 | bess | PRE_CONSENT | White House Farm | Qair UK | Welsh Government (NSIP) | - | - | 0.9km/132kV | `15561` | y |
| 1491 | 50.3 | 12 | solar | PRE_CONSENT | Motcombe Road, Motcombe - Solar Pv Arrays | Enviromena | Dorset | - | - | 0.6km/132kV | `16914` | y |
| 1492 | 50.3 | 44 | solar | PRE_CONSENT | Gaston Lane, Farringdon - Solar Farm & Battery Stora... | Quintas Energy UK Limited | East Hampshire | - | - | 0.7km/132kV | `11951` | y |
| 1493 | 50.3 | 5 | solar | PRE_CONSENT | Stone Lane Quarry, Woburn Road - Solar Array Area | Arnold White Estates Limited | Central Bedfordshire | - | - | 0.6km/400kV | `13146` | y |
| 1494 | 50.3 | 43 | solar | PRE_CONSENT | Greenfield Road - Samphill Solar Farm | Anesco Limited | Central Bedfordshire | - | - | 1.6km/132kV | `19175` | **n** |
| 1495 | 50.3 | 26 | solar | PRE_CONSENT | Falcon Park, Wilsons Road - Solar Farm & Battery Ene... | Regener8 Power Limited | South Cambridgeshire | - | - | 4.0km/132kV | `17859` | y |
| 1496 | 50.2 | 20 | solar | PAST_EXPECTED_START | Ham Farm, Creech St Michael - Solar Array | Novus Renewable Services Limited | Somerset | 2024-06-28 | 794 | 5.9km/132kV | `10496` | y |
| 1497 | 50.2 | 43 | solar | PRE_CONSENT | Arleston Solar & Battery Energy Storage System | Noventum Power Limited | South Derbyshire | - | - | 0.3km/132kV | `18142` | y |
| 1498 | 50.2 | 5 | bess | PRE_CONSENT | Twynersh Meadows, Thorpe Road - Solar Park & Battery... | Runnymede Borough Council | Runnymede | - | - | 0.9km/400kV | `12204` | y |
| 1499 | 50.2 | 3 | solar | PAST_EXPECTED_START | Iceland, Solar Way - Solar Photovoltaic Array | Ortus Energy | Enfield | 2024-01-29 | 945 | 0.5km/132kV | `15182` | y |
| 1500 | 50.2 | 55 | bess | PRE_CONSENT | Greybarn Solar Energy Farm | Statkraft UK | Mid Suffolk | - | - | 1.2km/132kV | `9104` | y |
| 1501 | 50.2 | 33 | solar | PAST_EXPECTED_START | Partridge Hill Solar Farm | Green Switch Solutions/Belvedere E... | Doncaster | 2016-07-29 | 3685 | 3.9km/400kV | `5460` | y |
| 1502 | 50.1 | 15 | solar | PAST_EXPECTED_START | Rockbeare Hill | Spring Che | East Devon | 2020-07-30 | 2223 | 1.7km/132kV | `7815` | y |
| 1503 | 50.1 | 15 | bess | PAST_EXPECTED_START | Smithyard Lane - Battery Storage | Conrad Energy Limited | Somerset | 2023-02-15 | 1293 | 1.1km/132kV | `10766` | y |
| 1504 | 50.1 | 70 | bess | DESIGN_FROZEN_OR_LATER | Widow Hill, Balderstone Lane - Battery Energy Storag... | P3P Partners LLP | Burnley | 2023-07-20 | - | 0.1km/132kV | `9340` | y |
| 1505 | 50.1 | 5 | solar | PRE_CONSENT | Tymaen Farm, Rhos - Solar Panels | Carmarthenshire County Council | Carmarthenshire | - | - | 0.4km/132kV | `19763` | y |
| 1506 | 50.1 | 42 | solar | PAST_EXPECTED_START | Montreathmont Moor Forest - Solar Farm & Battery Sto... | Renewable Connections Developments... | Angus | 2022-12-16 | 1354 | 0.7km/132kV | `10964` | y |
| 1507 | 50.1 | 6 | solar | PAST_EXPECTED_START | Craignathro Farm - Solar Array | Craignathro Farms Limited | Angus | 2023-08-17 | 1110 | 0.8km/132kV | `13280` | y |
| 1508 | 50.1 | 25 | bess | PAST_EXPECTED_START | Wemyss Estate - Randolph Solar Farm & Battery Energy... | Elgin Energy | Scottish Government (S36) | 2022-05-24 | 1560 | 1.2km/132kV | `6383` | y |
| 1509 | 50.1 | 25 | solar | PAST_EXPECTED_START | Church Farm, Withington - Solar Farm | Elgin Energy | Shropshire | 2023-04-13 | 1236 | 0.9km/132kV | `12005` | y |
| 1510 | 50.1 | 25 | bess | PRE_CONSENT | Torrington Avenue Battery Storage Facility | Power Initiatives Limited | Coventry | - | - | 0.1km/132kV | `16279` | y |
| 1511 | 50.0 | 19 | solar | PAST_EXPECTED_START | North Farm, Horton - Solar Farm | North Farm Mannington Solar Limite... | Dorset | 2025-05-07 | 481 | 3.8km/132kV | `7912` | **n** |
| 1512 | 50.0 | 53 | bess | PRE_CONSENT | Barfield Lane, Reepham - Battery Energy Storage Syst... | Fiskerton Bess Limited | West Lindsey | - | - | 1.0km/132kV | `12600` | y |
| 1513 | 49.9 | 24 | solar | PRE_CONSENT | Appleford Sidings, Sutton Courtenay - Solar Photovol... | Infinis Solar Developments Limited | Vale of White Horse | - | - | 1.0km/132kV | `9084` | y |
| 1514 | 49.9 | 24 | solar | PAST_EXPECTED_START | Side Barn, Church Lane - Solar Farm | PS Renewables Limited | South Kesteven | 2025-01-15 | 593 | 0.6km/132kV | `13592` | y |
| 1515 | 49.9 | 40 | bess | PRE_CONSENT | Glasgow Road, Eaglesham - Battery Storage Facility | GPC 1137 Limited | East Renfrewshire | - | - | 0.1km/275kV | `18055` | y |
| 1516 | 49.9 | 40 | bess | PRE_CONSENT | Aston Road, Aston - Solar Panels & Battery Energy St... | Ampyr Solar Europe | West Oxfordshire | - | - | 3.8km/400kV | `18920` | y |
| 1517 | 49.9 | 40 | solar | PRE_CONSENT | Aston Road, Aston - Solar Panels & Battery Energy St... | Ampyr Solar Europe | West Oxfordshire | - | - | 3.8km/400kV | `18921` | y |
| 1518 | 49.9 | 40 | solar | PRE_CONSENT | Nythe Road, Pedwell - Solar Photovoltaic Park | Elgin Energy Services Limited | Somerset | - | - | 0.4km/132kV | `19367` | y |
| 1519 | 49.9 | 2 | solar | PAST_EXPECTED_START | The Range Distribution Centre, Severn Beach - Solar ... | InRange Limited | South Gloucestershire | 2025-07-28 | 399 | 0.5km/132kV | `19056` | y |
| 1520 | 49.9 | 39 | solar | PRE_CONSENT | The Grafton Solar Project - Solar Photovoltaic Panel... | Stantec | North Northamptonshire | - | - | 1.0km/132kV | `19128` | y |
| 1521 | 49.9 | 4 | bess | PAST_EXPECTED_START | Highfield Farm, Royston Road - Solar Farm & Battery ... | Grupotec Solar 3 UK Limited | South Cambridgeshire | 2023-08-03 | 1124 | 3.4km/132kV | `13004` | y |
| 1522 | 49.9 | 4 | solar | PAST_EXPECTED_START | Woodland Barton Farm -Solar Farm | KPS SPV 4 Limited | Cornwall | 2024-11-01 | 668 | 0.9km/132kV | `17357` | y |
| 1523 | 49.8 | 39 | solar | PRE_CONSENT | Oakley Bush Solar Farm - Solar PV Panels | Buccleuch Estates Limited | North Northamptonshire | - | - | 0.5km/132kV | `15270` | y |
| 1524 | 49.8 | 2 | solar | PAST_EXPECTED_START | Wexham Park Hospital, Wexham Street - Solar PV Panel... | Frimley Health NHS Foundation Trus... | Slough | 2025-12-12 | 262 | 1.9km/132kV | `19938` | y |
| 1525 | 49.8 | 10 | solar | PRE_CONSENT | Funtley Solar Photovoltaic PV Farm | Private Developer | Winchester | - | - | 0.7km/400kV | `17202` | y |
| 1526 | 49.8 | 10 | solar | PRE_CONSENT | Funtley Solar Photovoltaic PV Farm | Private Developer | Winchester | - | - | 0.7km/400kV | `17202` | y |
| 1527 | 49.8 | 50 | solar | PAST_EXPECTED_START | Milltown Airfield (Speyslaw) | Elgin Energy | Scottish Government (S36) | 2018-05-25 | 3020 | 3.9km/132kV | `6341` | y |
| 1528 | 49.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Pancross & Oaklands Solar Farm | Infinis | Welsh Government (NSIP) | 2024-05-23 | - | 0.6km/275kV | `7701` | y |
| 1529 | 49.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Pancross & Oaklands Solar Farm | Infinis | Welsh Government (NSIP) | 2024-05-23 | - | 0.6km/275kV | `7702` | y |
| 1530 | 49.8 | 50 | bess | PRE_CONSENT | Cottom Power Station | EDF Energy Thermal Generation Limi... | Bassetlaw | - | - | 0.2km/400kV | `8278` | y |
| 1531 | 49.8 | 50 | bess | PRE_CONSENT | Lowlands Farm - Battery Storage | Anglo Renewables | Dudley | - | - | 0.6km/132kV | `12959` | y |
| 1532 | 49.8 | 50 | bess | PRE_CONSENT | Huncoat Power Station - Battery Storage | 24 Power Limited | Burnley | 2022-01-18 | - | 0.2km/132kV | `13080` | **n** |
| 1533 | 49.8 | 50 | bess | PRE_CONSENT | Wareham Road, Scouse Farm - Battery Storage | Ylem Energy Limited | East Devon | - | - | 0.2km/400kV | `15962` | **n** |
| 1534 | 49.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Ford Oaks Solar & Green Infrastructure Facility | Low Carbon Alliance / Taiyo Power ... | East Devon | 2023-11-30 | - | 0.4km/132kV | `11366` | y |
| 1535 | 49.8 | 50 | bess | PRE_CONSENT | Lackenby | EDF Energy Renewables | Redcar and Cleveland | - | - | 0.2km/400kV | `7518` | **n** |
| 1536 | 49.8 | 50 | bess | PRE_CONSENT | Model Farm | Tribus Clean Energy | King's Lynn and West Norfolk | - | - | 0.1km/132kV | `7609` | **n** |
| 1537 | 49.8 | 50 | bess | PRE_CONSENT | Welkin Mill | Noriker Power | Stockport | - | - | 0.2km/275kV | `7832` | **n** |
| 1538 | 49.8 | 50 | bess | PRE_CONSENT | Colinglen Road Battery | Hannahstown BESS | Belfast | - | - | 0.9km/275kV | `8033` | y |
| 1539 | 49.8 | 50 | bess | PRE_CONSENT | National Grid Axminster Substation | Harbour Energy | East Devon | - | - | 0.1km/400kV | `8036` | y |
| 1540 | 49.8 | 50 | bess | PRE_CONSENT | Welkin Mill | Noriker Power | Stockport | - | - | 0.2km/275kV | `8055` | **n** |
| 1541 | 49.8 | 50 | bess | PRE_CONSENT | Hilfield Farm Tech | Capbal | Hertsmere | - | - | 0.1km/275kV | `8065` | **n** |
| 1542 | 49.8 | 50 | solar | PAST_EXPECTED_START | Warren Farm Solar Farm & Battery Storage | Enso Green Holdings I Limited | Doncaster | 2022-03-15 | 1630 | 1.9km/400kV | `8495` | y |
| 1543 | 49.8 | 50 | solar | PAST_EXPECTED_START | Tuxford Road Solar Farm | Enso Energy Limited | Newark and Sherwood | 2021-12-16 | 1719 | 1.2km/400kV | `8515` | **n** |
| 1544 | 49.8 | 50 | solar | PAST_EXPECTED_START | Felsted School Road - Solar Photovoltaic Farm & Batt... | Clearstone Energy | Uttlesford | 2023-09-05 | 1091 | 2.2km/132kV | `9070` | y |
| 1545 | 49.8 | 50 | bess | PRE_CONSENT | Elland Storage Project | UK Battery Storage | Calderdale | - | - | 0.1km/275kV | `10236` | **n** |
| 1546 | 49.8 | 50 | solar | PAST_EXPECTED_START | High Nunton Farm - Solar Farm & Battery Storage | High Nunton Solar Limited | Dumfries and Galloway | 2025-01-22 | 586 | 6.2km/132kV | `10533` | y |
| 1547 | 49.8 | 50 | bess | PAST_EXPECTED_START | Rothienorman - Battery Storage | Anesco Limited | Aberdeenshire | 2022-11-14 | 1386 | 1.1km/400kV | `10638` | y |
| 1548 | 49.8 | 50 | solar | PRE_CONSENT | Horsham Road - Solar Farm & Battery Storage | Bolney Green Limited | Horsham | - | - | 1.6km/132kV | `10658` | y |
| 1549 | 49.8 | 50 | bess | PRE_CONSENT | Braintree Road Substation | Pivot Power | Braintree | - | - | 0.1km/400kV | `11995` | y |
| 1550 | 49.8 | 50 | bess | PAST_EXPECTED_START | Killoch Depot, Killoch Colliery - Battery Storage | Brockwell Energy Limited | East Ayrshire | 2023-03-30 | 1250 | 2.1km/275kV | `12349` | y |
| 1551 | 49.8 | 50 | solar | PRE_CONSENT | Burthy Row Farm, Trefullock Moor - Solar Farm & Batt... | JBM Solar Projects Limited | Cornwall | - | - | 0.1km/132kV | `12853` | y |
| 1552 | 49.8 | 50 | bess | PRE_CONSENT | Platchaig House, Kilmorack - Battery Storage Facilit... | Whirlwind Renewables | Highland | 2022-08-30 | - | 0.2km/132kV | `14373` | **n** |
| 1553 | 49.8 | 50 | solar | PRE_CONSENT | Pleasance Road, Coupar - Solar Array | Couper Two Limited | Perth and Kinross | - | - | 0.5km/132kV | `14792` | **n** |
| 1554 | 49.8 | 50 | bess | PRE_CONSENT | Elland Storage Project | UK Battery Storage | Calderdale | - | - | 0.1km/275kV | `15304` | y |
| 1555 | 49.8 | 50 | solar | PRE_CONSENT | Green Acres Farm, Scarcewater - Solar Farm | EDF Renewables | Cornwall | - | - | 4.5km/132kV | `15619` | y |
| 1556 | 49.8 | 50 | bess | PRE_CONSENT | Kellwood Road - Battery Storage | Geocore Limited | Dumfries and Galloway | 2024-05-20 | - | 0.1km/132kV | `16540` | y |
| 1557 | 49.8 | 50 | bess | PRE_CONSENT | Middleton Of Blackhills, Rothienorman - Battery Ener... | Scot Stability Limited | Aberdeenshire | 2023-09-07 | - | 0.6km/400kV | `18572` | y |
| 1558 | 49.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Tye Lane - Solar Farm | EDF Energy Renewables | Mid Suffolk | 2023-12-18 | - | 0.3km/400kV | `20402` | y |
| 1559 | 49.8 | 2 | solar | PAST_EXPECTED_START | Pegasus House, Sackville Street - Roof Mounted Solar... | Unknown | Westminster | 2021-12-13 | 1722 | 0.1km/132kV | `9924` | y |
| 1560 | 49.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Dunfermline North - Solar Photovoltaic Array/Battery... | Dunfermline Solar Limited (AMPYR S... | Fife | 2023-06-23 | - | 1.0km/275kV | `11264` | y |
| 1561 | 49.8 | 30 | solar | PAST_EXPECTED_START | Trinlaymire Farm - Solar farm, Battery storage | Trinlaymire Net Zero Solar Limited | West Lothian | 2024-12-20 | 619 | 6.0km/132kV | `11426` | y |
| 1562 | 49.8 | 23 | solar | PRE_CONSENT | Strattons Farm, Newbury Road - Solar PV Farm | Anglo Renewables (AR Kingsclere Li... | Basingstoke and Deane | - | - | 1.6km/132kV | `15524` | y |
| 1563 | 49.8 | 23 | bess | PAST_EXPECTED_START | Steventon Road - Battery Energy Storage | Greenfield Company | Shropshire | 2024-08-30 | 731 | 1.9km/132kV | `16590` | y |
| 1564 | 49.8 | 2 | solar | PAST_EXPECTED_START | Premier Farnell, Unit 3 - Solar Panels | ABRDN (Investments Trust/Standard ... | Leeds | 2024-05-13 | 840 | 0.7km/132kV | `16143` | y |
| 1565 | 49.8 | 50 | bess | PRE_CONSENT | Rye Common Lane | Harmony Energy | Hart | - | - | 0.2km/132kV | `7737` | y |
| 1566 | 49.7 | 4 | solar | PAST_EXPECTED_START | Piramal Healthcare, Whalton Road - Solar Farm | Centrica Plc | Northumberland | 2024-06-25 | 797 | 3.1km/400kV | `14135` | y |
| 1567 | 49.7 | 2 | solar | PAST_EXPECTED_START | The Hut Group, Skyline Drive - Solar Photovoltaic Pa... | London Metric Property Plc | Warrington | 2025-11-13 | 291 | 0.3km/132kV | `19416` | **n** |
| 1568 | 49.7 | 2 | solar | PAST_EXPECTED_START | Schoeller Allibert Limited, Road One - Solar Panels ... | Schoeller Allibert Limited | Cheshire West and Chester | 2023-01-24 | 1315 | 0.2km/132kV | `12416` | y |
| 1569 | 49.7 | 8 | solar | PAST_EXPECTED_START | East Rightadown Farm, Brandis Corner - Solar Farm | Black Torrington Solar Limited | Torridge | 2023-09-01 | 1095 | 6.6km/132kV | `13220` | y |
| 1570 | 49.6 | 10 | solar | PAST_EXPECTED_START | Poole Farm, Quorn - Solar Farm | Leicestershire County Council | Charnwood | 2022-06-21 | 1532 | 0.6km/400kV | `10721` | y |
| 1571 | 49.6 | 10 | solar | PRE_CONSENT | Weeland Road, Kellingley - Solar Farm | Ivegate Limited | North Yorkshire | - | - | 0.8km/400kV | `13777` | y |
| 1572 | 49.6 | 10 | bess | PAST_EXPECTED_START | Ash Farm, Charlton Road - Battery Storage System | Ash Farm Solar Limited | Somerset | 2024-12-13 | 626 | 4.7km/132kV | `14025` | y |
| 1573 | 49.6 | 10 | solar | PRE_CONSENT | Glebe Farm, Curdridge Lane - Solar Farm | Glebe Farm Energy Limited | Winchester | - | - | 0.8km/400kV | `17266` | y |
| 1574 | 49.6 | 10 | bess | PRE_CONSENT | Hackworth Road, North West Industrial Estate - Solar... | ABEI Energy Green IX Limited | County Durham | - | - | 2.4km/400kV | `18298` | y |
| 1575 | 49.6 | 10 | solar | PRE_CONSENT | Bleabeck Solar Farm, Lots Road - Solar Farm | Noventum Power Limited | Westmorland and Furness | - | - | 1.2km/132kV | `20607` | y |
| 1576 | 49.6 | 10 | solar | PAST_EXPECTED_START | Blackberry Lane - Solar Farm | Wessex Solar Energy | Pembrokeshire | 2025-05-15 | 473 | 0.4km/400kV | `7703` | **n** |
| 1577 | 49.6 | 13 | solar | PAST_EXPECTED_START | Welsh Way - Solar PV Farm | Innova Renewables | Cotswold | 2024-09-23 | 707 | 7.5km/400kV | `13557` | y |
| 1578 | 49.6 | 48 | solar | DESIGN_FROZEN_OR_LATER | Fleet Hill Solar Farm | Capital Dynamics | Hart | 2025-04-10 | - | 1.9km/132kV | `15379` | y |
| 1579 | 49.6 | 10 | solar | PAST_EXPECTED_START | Over Farm | Over Farm Solar | Tewkesbury | 2016-06-06 | 3738 | 0.2km/132kV | `5432` | y |
| 1580 | 49.6 | 10 | solar | PRE_CONSENT | Longman Landfill, Stadium Road - Solar Array | The Highland Council | Highland | - | - | 4.7km/132kV | `19282` | y |
| 1581 | 49.5 | 2 | solar | PAST_EXPECTED_START | Calsonic Kansei - Solar Array | SNRG Limited | Sunderland | 2024-06-12 | 810 | 1.0km/275kV | `16278` | y |
| 1582 | 49.5 | 2 | solar | PAST_EXPECTED_START | Royal Seaforth Dock, New Jenkins Sheds - Solar Panel... | EON UK Heat Limited | Sefton | 2024-02-27 | 916 | 1.6km/132kV | `15926` | y |
| 1583 | 49.4 | 2 | solar | PAST_EXPECTED_START | Swaledale House, Weaverthorpe Road - Solar Panels | Princes Soft Drinks | Bradford | 2023-08-07 | 1120 | 1.1km/132kV | `14185` | y |
| 1584 | 49.4 | 21 | solar | PAST_EXPECTED_START | Court Barton Farm, Coffinswell - Solar Farm | Coubar Energy Limited (Windel) | Teignbridge | 2023-08-15 | 1112 | 1.4km/132kV | `9530` | y |
| 1585 | 49.4 | 2 | solar | PAST_EXPECTED_START | Hempsted Lane - Solar Array | Enovert South Limited | Gloucester | 2023-08-18 | 1109 | 0.2km/132kV | `11156` | y |
| 1586 | 49.4 | 2 | bess | PAST_EXPECTED_START | Biffa Waste Services, Fochriw Road - Battery Storage | Biffa Waste Services | Caerphilly | 2023-01-11 | 1328 | 0.4km/400kV | `12749` | y |
| 1587 | 49.4 | 2 | solar | PAST_EXPECTED_START | Radley College, Kennington Gate - Solar Array & Batt... | Radley College | Vale of White Horse | 2023-08-10 | 1117 | 0.9km/132kV | `13692` | y |
| 1588 | 49.4 | 2 | solar | PAST_EXPECTED_START | Whites Pit, Arena Way - Solar PV Array | Canford Renewable Energy Limited | Bournemouth, Christchurch an... | 2023-12-19 | 986 | 1.2km/132kV | `14974` | y |
| 1589 | 49.4 | 2 | solar | PAST_EXPECTED_START | Orbital Shopping Park, North Swindon District Centre... | Orbital Retail Park Swindon Limite... | Swindon | 2024-03-18 | 896 | 0.5km/132kV | `15782` | y |
| 1590 | 49.4 | 35 | solar | PRE_CONSENT | The A361, Ashby St Ledgers - Solar Farm | Elgin Energy Esco Limited | West Northamptonshire | - | - | 3.2km/132kV | `19652` | y |
| 1591 | 49.4 | 45 | bess | DESIGN_FROZEN_OR_LATER | Mount Pleasant Farm, Green Lane - Battery Storage | Barton Battery Storage | Wyre | 2023-10-03 | - | 0.7km/132kV | `13011` | y |
| 1592 | 49.4 | 45 | bess | PRE_CONSENT | Huncoat Power Station - Battery Storage Facility | 24 Power Limited | Burnley | - | - | 0.2km/132kV | `15712` | **n** |
| 1593 | 49.4 | 2 | solar | PAST_EXPECTED_START | Unit O, Penzance Drive - Solar Panels | Ortus Energy | Swindon | 2024-05-23 | 830 | 0.3km/132kV | `15022` | y |
| 1594 | 49.3 | 12 | solar | PAST_EXPECTED_START | Central Eco Park - Solar Farm | HY2Go Limited | South Lanarkshire | 2023-02-14 | 1294 | 0.8km/400kV | `10409` | y |
| 1595 | 49.3 | 34 | solar | PRE_CONSENT | Land North of Horsley Cross - Solar Farm & Battery E... | Mespil Solar Energy | Tendring | - | - | 1.8km/132kV | `18410` | y |
| 1596 | 49.3 | 5 | solar | PAST_EXPECTED_START | Hoon Hay Manor, Hatton - Solar Farm | Hoon Hay Solar Limited | South Derbyshire | 2023-01-13 | 1326 | 0.6km/132kV | `8111` | y |
| 1597 | 49.2 | 20 | bess | PAST_EXPECTED_START | Hagshaw Hill | Scottish Power Renewables | Scottish Government (S36) | 2020-02-26 | 2378 | 4.4km/400kV | `7456` | y |
| 1598 | 49.2 | 20 | bess | PRE_CONSENT | Gerrards Cross Sewage Treatment Works | Peak Gen Power | Buckinghamshire | - | - | 0.4km/132kV | `8271` | y |
| 1599 | 49.2 | 20 | solar | PAST_EXPECTED_START | Grounds Farm - Solar farm | Encavis | Central Bedfordshire | 2021-10-19 | 1777 | 1.6km/132kV | `8472` | y |
| 1600 | 49.2 | 20 | bess | PAST_EXPECTED_START | Hull East Stor Generation Compound - Battery energy ... | Green Frog Power 214 Limited | Kingston upon Hull, City of | 2021-07-29 | 1859 | 0.2km/132kV | `9006` | y |
| 1601 | 49.2 | 20 | solar | PAST_EXPECTED_START | Limes Farm Solar Farm & Battery Energy Storage | Downing Limited Liability Partners... | South Kesteven | 2025-05-12 | 476 | 2.5km/132kV | `11797` | y |
| 1602 | 49.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Lychgate Lane, Aston Flamville - Solar Farm | Elgin Energy ES Co Limited | Blaby | 2024-04-11 | - | 0.5km/275kV | `11885` | y |
| 1603 | 49.2 | 20 | bess | PRE_CONSENT | Larks Lane, Iron Acton - Battery Storage Facility | HD000ACT Limited | South Gloucestershire | - | - | 0.1km/132kV | `14091` | y |
| 1604 | 49.2 | 20 | solar | PRE_CONSENT | Maltby Solar Farm | Infinis Energy Services Limited | Rotherham | - | - | 0.6km/132kV | `17104` | y |
| 1605 | 49.2 | 20 | bess | PRE_CONSENT | Former EON Power Station, Booth Lane - Battery Energ... | Bluefield Sandbach Limited | Cheshire East | - | - | 0.8km/132kV | `17725` | y |
| 1606 | 49.2 | 20 | bess | PRE_CONSENT | Falcon Park, Wilsons Road - Solar Farm & Battery Ene... | Regener8 Power Limited | South Cambridgeshire | - | - | 4.0km/132kV | `17858` | y |
| 1607 | 49.2 | 20 | solar | PRE_CONSENT | Glevering Park House, Glevering Estate - Solar Panel... | Grupotec | East Suffolk | - | - | 2.2km/400kV | `18304` | y |
| 1608 | 49.2 | 20 | solar | PRE_CONSENT | Pentre Bach Solar Farm | Elgin Energy EsCo Ltd | Welsh Government (NSIP) | - | - | 1.0km/132kV | `18492` | y |
| 1609 | 49.2 | 20 | bess | PRE_CONSENT | Caswell Farm, Common Lane - Battery Energy Storage | GridSource Limited | Dorset | - | - | 2.5km/132kV | `19146` | y |
| 1610 | 49.2 | 20 | solar | PAST_EXPECTED_START | Wardlaw Wood - Solar Farm | Community Windpower Limited | North Ayrshire | 2024-11-07 | 662 | 0.3km/400kV | `17225` | y |
| 1611 | 49.2 | 15 | solar | PAST_EXPECTED_START | Camp Road, West Coker - Solar PV Panels | Conrad Energy | Somerset | 2024-01-31 | 943 | 5.3km/132kV | `12521` | y |
| 1612 | 49.2 | 5 | solar | PAST_EXPECTED_START | Apple Tree Close | Sun Farming | Teignbridge | 2016-05-31 | 3744 | 0.5km/400kV | `4962` | y |
| 1613 | 49.2 | 5 | solar | PAST_EXPECTED_START | Wold Cottage Solar Farm | First Renewable Developments | North Northamptonshire | 2015-07-31 | 4049 | 0.9km/132kV | `5269` | y |
| 1614 | 49.2 | 5 | solar | PAST_EXPECTED_START | Latimer Solar Park | First Renewable Developments | North Northamptonshire | 2015-08-03 | 4046 | 1.1km/132kV | `5274` | y |
| 1615 | 49.2 | 5 | solar | PAST_EXPECTED_START | Bulkworthy Solar Park | Ecotricity | Torridge | 2016-05-19 | 3756 | 0.6km/400kV | `5757` | y |
| 1616 | 49.2 | 5 | solar | PAST_EXPECTED_START | Stockton Court farm | Renewable Power Exchange | Malvern Hills | 2017-04-05 | 3435 | 0.6km/132kV | `6183` | **n** |
| 1617 | 49.2 | 5 | solar | PAST_EXPECTED_START | Stratford Road Solar Farm | Rowlandson Organisation Group | Buckinghamshire | 2022-01-28 | 1676 | 0.3km/132kV | `8267` | y |
| 1618 | 49.2 | 5 | solar | PAST_EXPECTED_START | Goose Hall Solar Farm | Lightsource BP | East Cambridgeshire | 2021-03-19 | 1991 | 0.2km/400kV | `9528` | y |
| 1619 | 49.2 | 5 | bess | PAST_EXPECTED_START | Trondheim Way - Battery Storage Facility | Vox Energy Limited | North East Lincolnshire | 2022-04-05 | 1609 | 0.0km/132kV | `10872` | y |
| 1620 | 49.2 | 5 | solar | PAST_EXPECTED_START | Newcastle International Airport Phase 3- Solar Farm | Newcastle International Airport | Newcastle upon Tyne | 2022-02-28 | 1645 | 2.2km/275kV | `11346` | y |
| 1621 | 49.2 | 5 | bess | PAST_EXPECTED_START | Coxhall Road, Tattingstone - Battery Storage | AMP Energy Services Limited | Babergh | 2023-01-17 | 1322 | 1.3km/132kV | `12693` | y |
| 1622 | 49.2 | 2 | solar | PAST_EXPECTED_START | Phinia, Courteney Road - Solar Panels | Phinia Delphi UK Limited | Medway | 2024-03-01 | 913 | 3.0km/400kV | `15469` | y |
| 1623 | 49.1 | 90 | bess | PRE_CONSENT | Caldwell Road - Battery Storage | Infrared Capital Partners Limited | South Derbyshire | 2022-03-03 | - | 0.4km/400kV | `16318` | y |
| 1624 | 49.1 | 2 | solar | PAST_EXPECTED_START | New Venture Buildings, Caswell Way - Solar Array | Bisley Office Equipment Limited | Newport | 2023-03-16 | 1264 | 0.2km/400kV | `13089` | y |
| 1625 | 49.1 | 2 | solar | PAST_EXPECTED_START | Dorsey Way, Enderby - Solar Panels | Goodman Logistics Developments UK ... | Blaby | 2024-04-23 | 860 | 0.6km/132kV | `15988` | y |
| 1626 | 49.1 | 42 | solar | PRE_CONSENT | Bardwell Fields, Knox Lane - Solar Farm | Opdenergy UK 23 Limited | West Suffolk | - | - | 2.6km/132kV | `19254` | **n** |
| 1627 | 49.1 | 42 | solar | PRE_CONSENT | Greybarn Solar Energy Farm | Statkraft UK | Mid Suffolk | - | - | 1.2km/132kV | `9105` | y |
| 1628 | 49.0 | 19 | solar | PRE_CONSENT | Cross Rein Bank Solar Farm - Solar Farm | PS Renewables Limited | North Yorkshire | - | - | 0.3km/132kV | `17281` | y |
| 1629 | 49.0 | 19 | solar | PRE_CONSENT | Pattenden Lane - Solar PV Energy | ILOS Energy UK Limited | Maidstone | - | - | 1.5km/132kV | `17499` | y |
| 1630 | 49.0 | 19 | solar | PAST_EXPECTED_START | Brains Solar Farm | NextPower SPV 13 Limited | Somerset | 2022-01-10 | 1694 | 1.0km/400kV | `9372` | y |
| 1631 | 49.0 | 2 | solar | PAST_EXPECTED_START | Thorn Lighting, Butchers Race - Solar Panels | Colliers Building Consultancy Limi... | County Durham | 2024-08-02 | 759 | 1.1km/132kV | `16576` | y |
| 1632 | 49.0 | 2 | solar | PAST_EXPECTED_START | Amazon Uk, Skelton Moor Road - Solar Panels | Zestec Group | Leeds | 2022-11-22 | 1378 | 0.7km/132kV | `12269` | y |
| 1633 | 48.9 | 40 | solar | DESIGN_FROZEN_OR_LATER | Rock Farm - Solar Farm | Anglo Renewables | Shropshire | 2023-09-25 | - | 1.4km/132kV | `10635` | y |
| 1634 | 48.9 | 40 | bess | PRE_CONSENT | Norwich Road Industrial Estate | RNA Energy | East Suffolk | - | - | 0.2km/132kV | `12529` | y |
| 1635 | 48.9 | 40 | solar | PAST_EXPECTED_START | Thorpe Park Solar Farm, Thorpe Le Soken - Solar Farm | Low Carbon UK Solar Investment Co ... | Tendring | 2023-02-17 | 1291 | 1.7km/132kV | `13028` | y |
| 1636 | 48.9 | 40 | bess | PRE_CONSENT | Derby Road - Battery Energy Storage System | Starlight Energy | Amber Valley | - | - | 3.3km/132kV | `15273` | y |
| 1637 | 48.9 | 40 | bess | PRE_CONSENT | Hardybarn Lane, Green Fairfield - Battery Energy Sto... | S & L Energy Limited | High Peak | - | - | 0.9km/132kV | `18393` | **n** |
| 1638 | 48.9 | 2 | solar | PAST_EXPECTED_START | Pilgrims Pride - Solar Array | EDF Energy Renewables | South Holland | 2025-07-08 | 419 | 1.1km/400kV | `17474` | y |
| 1639 | 48.8 | 2 | solar | PAST_EXPECTED_START | Rutherford Appleton Laboratory | The Science and Technology Facilit... | Vale of White Horse | 2021-07-13 | 1875 | 0.8km/132kV | `9016` | y |
| 1640 | 48.8 | 2 | solar | PAST_EXPECTED_START | Parsonage Way - Solar Panels | Wavin Plastic Limited | Wiltshire | 2022-10-11 | 1420 | 0.4km/132kV | `11837` | y |
| 1641 | 48.8 | 2 | solar | PAST_EXPECTED_START | Harrods Distribution Centre, Mill Lane - Solar Array | Private Developer | West Berkshire | 2023-02-24 | 1284 | 0.4km/132kV | `12897` | y |
| 1642 | 48.8 | 2 | solar | PAST_EXPECTED_START | Fort Shopping Park, Fort Parkway - Solar PV Panels | Ire Evaf Ii The Fort Propco Limite... | Birmingham | 2023-09-21 | 1075 | 0.2km/132kV | `14723` | y |
| 1643 | 48.8 | 18 | solar | PAST_EXPECTED_START | Selms Muir - Solar Farm | Renewable Connections | West Lothian | 2022-09-27 | 1434 | 0.8km/275kV | `11430` | y |
| 1644 | 48.8 | 18 | solar | PAST_EXPECTED_START | Higher Hawkerland Farm, Sidmouth Road - Solar Farm | Spring Dev 09 Limited | East Devon | 2023-04-28 | 1221 | 2.0km/132kV | `12578` | y |
| 1645 | 48.8 | 18 | solar | PRE_CONSENT | Crossway Green, Ombersley - Solar Panels | Tyler Hill Solar Limited | Wychavon | - | - | 0.7km/132kV | `14001` | y |
| 1646 | 48.8 | 8 | bess | PAST_EXPECTED_START | Tophams Solar Farm | Pathfinder Clean Energy UK Dev Lim... | North Hertfordshire | 2024-06-17 | 805 | 2.3km/400kV | `9037` | y |
| 1647 | 48.8 | 8 | bess | PAST_EXPECTED_START | Highfields Farm - Solar Farm & Battery Storage | Boultbee Brooks Renewable Energy L... | Rushcliffe | 2023-02-16 | 1292 | 1.1km/132kV | `9457` | y |
| 1648 | 48.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Coylton Substation, Coylton - Battery Energy Storage | Statkraft UK Limited | East Ayrshire | 2024-02-29 | - | 0.2km/275kV | `10162` | **n** |
| 1649 | 48.8 | 50 | bess | PRE_CONSENT | New Oaks, Station Road - Battery Energy Storage Syst... | Brockwell Energy Limited | _none_ | - | - | 5.4km/132kV | `19255` | y |
| 1650 | 48.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Halewick Lane, Sompting - Battery-based Energy Stora... | Public Power Solutions (PPS) / Wes... | Adur | - | - | 1.0km/132kV | `7168` | y |
| 1651 | 48.8 | 30 | solar | PRE_CONSENT | Hoopers Pool, Southwick - Solar Panels | Hoopers Pool Solar Farm Limited | Wiltshire | - | - | 0.5km/132kV | `18977` | y |
| 1652 | 48.8 | 30 | bess | PRE_CONSENT | Butt Lane, Hooton Pagnell Battery Energy Storage | British Solar Renewables | Doncaster | - | - | 2.1km/275kV | `19248` | y |
| 1653 | 48.8 | 30 | solar | PRE_CONSENT | Torkington Road, Hazel Grove - Solar PV Panels | Conrad Energy (Developments) Limit... | Stockport | - | - | 0.6km/400kV | `19250` | y |
| 1654 | 48.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Bradford West Substation (Harrop Edge Farm) | UK Battery Storage | Bradford | 2020-07-24 | - | 0.1km/132kV | `7045` | **n** |
| 1655 | 48.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Corner Copse Solar Farm | BayWa r.e. UK Limited | Swindon | 2020-06-25 | - | 2.2km/132kV | `7519` | y |
| 1656 | 48.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Grimsby Solar Farm | Aura Power | North East Lincolnshire | 2022-11-25 | - | 0.7km/400kV | `7889` | y |
| 1657 | 48.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Bredbury Substation - Battery Storage Facility | Private Developer | Stockport | 2021-12-02 | - | 0.2km/275kV | `9653` | y |
| 1658 | 48.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Holmston Road - Battery Storage Facility | Field Energy | South Ayrshire | 2023-06-30 | - | 0.2km/275kV | `11679` | y |
| 1659 | 48.8 | 2 | solar | PAST_EXPECTED_START | Sunningdale Road - Solar Panels | Harvest Green Developments | Leicester | 2025-08-14 | 382 | 2.2km/400kV | `19153` | y |
| 1660 | 48.8 | 2 | solar | PAST_EXPECTED_START | Sharps Bedrooms, Springvale Avenue - Solar Panels | Watt Energy Saver Limited | Wolverhampton | 2022-08-30 | 1462 | 0.9km/132kV | `12042` | y |
| 1661 | 48.8 | 2 | solar | PAST_EXPECTED_START | Delico, Steinbeck Crescent - Solar Panels | Cranswick Plc | Milton Keynes | 2023-04-27 | 1222 | 0.2km/132kV | `13166` | y |
| 1662 | 48.7 | 38 | solar | PRE_CONSENT | Derby Road - Solar Panels | Starlight Energy | Amber Valley | - | - | 3.3km/132kV | `15274` | y |
| 1663 | 48.7 | 2 | solar | PAST_EXPECTED_START | Poundland Distribution Centre - Solar Photovoltaic S... | Standard Life Assurance Limited | Harlow | 2022-07-12 | 1511 | 0.6km/132kV | `11459` | y |
| 1664 | 48.7 | 2 | solar | PAST_EXPECTED_START | Gorton Street & Murray Street, Grimsby Docks - Solar... | GY 1900 Limited | North East Lincolnshire | 2025-07-14 | 413 | 1.6km/132kV | `18607` | y |
| 1665 | 48.7 | 3 | solar | PAST_EXPECTED_START | Park Springs, Long Royd - Solar Panels | Leggett & Platt Barnsley | Barnsley | 2024-03-26 | 888 | 1.1km/132kV | `15851` | y |
| 1666 | 48.7 | 80 | bess | PAST_EXPECTED_START | Tealing Battery Energy Storage Farm | Sirius EcoDev Limited | Scottish Government (S36) | 2023-12-13 | 992 | 2.6km/132kV | `14543` | y |
| 1667 | 48.7 | 80 | bess | PRE_CONSENT | Barlow Road, Barlow Road - Battery Storage | Vox Energy Limited | North Yorkshire | - | - | 2.4km/132kV | `14715` | **n** |
| 1668 | 48.6 | 10 | bess | PAST_EXPECTED_START | Trevol Business Park | Londonwide Properties | Cornwall | 2019-09-02 | 2555 | 4.4km/132kV | `7404` | y |
| 1669 | 48.6 | 10 | solar | PAST_EXPECTED_START | New Rides Farm - Photovoltaic Panels | EnergieKontor UK Limited | Swale | 2021-09-30 | 1796 | 6.4km/400kV | `9270` | y |
| 1670 | 48.6 | 4 | solar | PAST_EXPECTED_START | Sharpley Hill Solar Farm | Opdenergy UK 2 Limited | Rushcliffe | 2021-12-02 | 1733 | 0.5km/132kV | `8851` | y |
| 1671 | 48.6 | 4 | solar | PAST_EXPECTED_START | Radcliffe Road, Holme Pierrepont - Solar Farm | Bassingfield REP Limited | Rushcliffe | 2022-12-21 | 1349 | 0.7km/400kV | `12241` | y |
| 1672 | 48.6 | 17 | solar | PAST_EXPECTED_START | Shire-End Farm | Qair Scotland Limited | Perth and Kinross | 2016-02-18 | 3847 | 1.8km/275kV | `4950` | y |
| 1673 | 48.6 | 17 | solar | PAST_EXPECTED_START | Drury Lane | Moss Lane Farm Solar Limited | Cheshire East | 2021-02-01 | 2037 | 0.4km/132kV | `7553` | y |
| 1674 | 48.6 | 13 | solar | PRE_CONSENT | Foxwalks Solar Farm - Extension | Spring Dev 10 Limited | Bromsgrove | - | - | 1.8km/400kV | `19977` | y |
| 1675 | 48.6 | 22 | solar | PAST_EXPECTED_START | Kemberton - Solar Farm | Vattenfall | Shropshire | 2024-02-22 | 921 | 3.4km/400kV | `11202` | y |
| 1676 | 48.6 | 8 | bess | PAST_EXPECTED_START | Newby Road, Hazel Grove - Battery Storage | AMP Energy Services Limited | Stockport | 2022-11-08 | 1392 | 1.9km/400kV | `11172` | y |
| 1677 | 48.6 | 1 | solar | PAST_EXPECTED_START | Premier Park Road - Photovoltaic System | SEGRO UK | Brent | 2022-05-17 | 1567 | 1.0km/132kV | `10898` | y |
| 1678 | 48.6 | 100 | bess | PRE_CONSENT | Rogerhill Solar and Battery Energy Storage System | Green Switch Capital Limited | Scottish Government (S36) | - | - | 3.5km/400kV | `14193` | y |
| 1679 | 48.6 | 100 | solar | PRE_CONSENT | Rogerhill Solar and Battery Energy Storage System | Green Switch Capital Limited | Scottish Government (S36) | - | - | 3.5km/400kV | `14194` | y |
| 1680 | 48.6 | 100 | bess | PRE_CONSENT | Mullaghmeash Road & Feeny - Battery Energy Storage | Private Developer | Derry City and Strabane | - | - | 5.4km/275kV | `18508` | y |
| 1681 | 48.5 | 28 | solar | PAST_EXPECTED_START | Home Farm - Solar PV Farm | Renewable Energy Systems (RES) | South Kesteven | 2025-03-13 | 536 | 2.5km/132kV | `16683` | y |
| 1682 | 48.5 | 60 | bess | PRE_CONSENT | The Waddings, Knighton-On-Teme - Battery Energy Stor... | Integrum SPV 22298 Limited | Malvern Hills | - | - | 0.3km/132kV | `17849` | y |
| 1683 | 48.5 | 60 | bess | PRE_CONSENT | Fourstones -Battery Energy Storage | Mespil Solar Energy | Northumberland | - | - | 0.3km/275kV | `18691` | y |
| 1684 | 48.5 | 4 | solar | PAST_EXPECTED_START | Newcastle International Airport Phase 2 - Solar Farm | Newcastle International Airport | Newcastle upon Tyne | 2022-02-28 | 1645 | 2.2km/275kV | `11344` | y |
| 1685 | 48.5 | 4 | solar | PAST_EXPECTED_START | Newcastle International Airport Phase 4 - Solar Farm | Newcastle International Airport | Newcastle upon Tyne | 2022-02-28 | 1645 | 2.2km/275kV | `11348` | y |
| 1686 | 48.4 | 125 | solar | PRE_CONSENT | Wentlooge Renewable Energy Hub | Wentlooge Farmers' Solar Scheme | Welsh Government (NSIP) | - | - | 0.4km/132kV | `11279` | **n** |
| 1687 | 48.4 | 125 | bess | PRE_CONSENT | Stallingborough Road - Battery Storage | Island Green Power | West Lindsey | - | - | 0.7km/400kV | `17508` | y |
| 1688 | 48.4 | 1 | solar | PAST_EXPECTED_START | Brakes, Edinburgh Road - Solar Panels | Brake Bros Limited | North Lanarkshire | 2023-06-06 | 1182 | 0.6km/275kV | `13916` | y |
| 1689 | 48.4 | 35 | solar | PRE_CONSENT | Vicarage Lane, Diddington - Solar Arrays | Cell Energy Limited | Huntingdonshire | - | - | 4.7km/400kV | `10073` | y |
| 1690 | 48.4 | 35 | bess | PRE_CONSENT | Windburn Wind Farm | Octopus Energy / Wind 2 Limited | Scottish Government (S36) | - | - | 1.5km/132kV | `13625` | y |
| 1691 | 48.4 | 27 | bess | PRE_CONSENT | Lowerfields Farm, Warren Lane - Battery Energy Stora... | Renewable Connections Developments... | Oldham | - | - | 2.1km/132kV | `19458` | y |
| 1692 | 48.4 | 16 | solar | PRE_CONSENT | Toyota Solar Farm - Solar Farm | Toyota Motor Manufacturing UK Limi... | South Derbyshire | - | - | 0.4km/132kV | `19657` | y |
| 1693 | 48.4 | 1 | solar | PAST_EXPECTED_START | Unit F, 6, Premier Park Road - Solar Panels | Segro Plc | Brent | 2023-09-06 | 1090 | 1.0km/132kV | `14520` | y |
| 1694 | 48.4 | 3 | solar | PAST_EXPECTED_START | Ocado Operating Limited, New Purfleet Road - Solar P... | Saber Renewable Energy Limited | Thurrock | 2025-05-06 | 482 | 0.4km/400kV | `18413` | y |
| 1695 | 48.4 | 1 | solar | PAST_EXPECTED_START | Suttons Park Avenue, Suttons Business Park - Solar P... | Brakes Group | Wokingham | 2023-08-11 | 1116 | 1.0km/132kV | `14323` | y |
| 1696 | 48.3 | 1 | solar | PAST_EXPECTED_START | Floplast, Castle Road - Solar Panels | Olympus Power | Swale | 2024-03-05 | 909 | 0.7km/400kV | `15656` | y |
| 1697 | 48.3 | 1 | solar | PAST_EXPECTED_START | London Medway Commercial Park | Pegasus Planning Group | Medway | 2021-05-13 | 1936 | 0.3km/400kV | `8435` | y |
| 1698 | 48.3 | 1 | solar | PAST_EXPECTED_START | Momentive Speciality Chemicals, Sully Moors Road - S... | Bakelite Synthetics Uk Limited | Vale of Glamorgan | 2023-07-31 | 1127 | 0.2km/132kV | `13689` | y |
| 1699 | 48.3 | 1 | solar | PAST_EXPECTED_START | Brew Dog Brewery, Condor Glen - Solar Panels | Scottish Power Pension Fund | North Lanarkshire | 2023-05-18 | 1201 | 0.7km/275kV | `13788` | y |
| 1700 | 48.3 | 1 | solar | PAST_EXPECTED_START | Gkn & Whippingham Technology Park, Beatrice Avenue -... | GKN Aerospace Services Limited | Isle of Wight | 2023-10-19 | 1047 | 0.6km/132kV | `13816` | y |
| 1701 | 48.3 | 1 | solar | PAST_EXPECTED_START | Coningsby Business Park, Stirling Way - Solar Panels | Industrials Propco 1 Limited | Peterborough | 2024-04-30 | 853 | 0.1km/132kV | `16049` | y |
| 1702 | 48.3 | 1 | solar | PAST_EXPECTED_START | Triumph Motorcycles, Normandy Way - Solar PV Array | Triumph Motorcycles Limited | Hinckley and Bosworth | 2023-11-01 | 1034 | 0.4km/132kV | `14626` | y |
| 1703 | 48.3 | 1 | solar | PAST_EXPECTED_START | Bluewater Shopping Centre, Upper Thames Walk - Solar... | Land Securities Property Limited | Dartford | 2023-04-06 | 1243 | 0.6km/400kV | `13138` | y |
| 1704 | 48.3 | 1 | solar | PAST_EXPECTED_START | Ford Halewood Transmissions Spekere, Boulevard - Sol... | On Site Energy Limited | Knowsley | 2023-12-06 | 999 | 0.2km/132kV | `14596` | y |
| 1705 | 48.3 | 1 | solar | PAST_EXPECTED_START | Dunsbury Park, Fitzwygram Way - Solar Panels | Watson Marlow Fluid Technology Sol... | Havant | 2024-06-14 | 808 | 0.1km/132kV | `16296` | y |
| 1706 | 48.3 | 1 | solar | PAST_EXPECTED_START | G Park Maxted Road - Solar Panels | BBUKPF | Dacorum | 2022-07-18 | 1505 | 1.3km/400kV | `11472` | y |
| 1707 | 48.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Dunfermline North - Solar Photovoltaic Array/Battery... | Dunfermline Solar Limited (AMPYR S... | Fife | 2023-06-23 | - | 1.0km/275kV | `11263` | y |
| 1708 | 48.2 | 1 | solar | PAST_EXPECTED_START | Snop, Rainhill Road - Solar Panels | SLIPIT | Sunderland | 2023-01-11 | 1328 | 1.2km/275kV | `12849` | y |
| 1709 | 48.2 | 1 | solar | PAST_EXPECTED_START | DHL Supply Chain, Pendeen Crescent -Solar Panels | GLP Capital | Milton Keynes | 2024-07-22 | 770 | 0.4km/132kV | `16519` | y |
| 1710 | 48.2 | 5 | solar | PAST_EXPECTED_START | Swancote Farm -Solar Panels | Swancote Energy Limited | Shropshire | 2025-01-21 | 587 | 7.0km/400kV | `17453` | y |
| 1711 | 48.2 | 7 | solar | PAST_EXPECTED_START | Newfordpark House, Glamis Road - Solar Panels | Don & Low Limited | Angus | 2023-02-14 | 1294 | 1.6km/275kV | `12845` | y |
| 1712 | 48.2 | 9 | bess | PAST_EXPECTED_START | Lower Mays Farm Solar Farm | Unknown | Wealden | 2021-07-15 | 1873 | 0.3km/132kV | `8371` | y |
| 1713 | 48.2 | 1 | solar | PAST_EXPECTED_START | Ellington South Site, Lynemouth Solar Array | The Coal Authority | Northumberland | 2023-03-20 | 1260 | 1.0km/132kV | `9030` | y |
| 1714 | 48.2 | 1 | solar | PAST_EXPECTED_START | Valiant Way, Pendeford | NESPF | South Staffordshire | 2021-11-12 | 1753 | 1.6km/275kV | `9597` | y |
| 1715 | 48.2 | 1 | solar | PAST_EXPECTED_START | College Street - Solar Panels | Pilkington | St. Helens | 2024-06-17 | 805 | 1.0km/132kV | `16362` | y |
| 1716 | 48.1 | 15 | solar | PAST_EXPECTED_START | South Park Solar Farm | Renewable Connections Developments... | Test Valley | 2022-11-03 | 1397 | 0.4km/132kV | `9126` | y |
| 1717 | 48.1 | 15 | solar | PRE_CONSENT | Totmonslow Farm - Solar Photovoltaic Farm | RE Projects Development | Staffordshire Moorlands | - | - | 0.4km/400kV | `13120` | y |
| 1718 | 48.1 | 1 | solar | PAST_EXPECTED_START | Perkins Engines, Fengate - Solar Farm | Perkins Engines | Peterborough | 2022-03-18 | 1627 | 0.4km/132kV | `10305` | y |
| 1719 | 48.1 | 3 | solar | PAST_EXPECTED_START | Mclaren Technology Centre, Chertsey Road - Solar Pan... | McLaren Group Limited | Woking | 2025-11-18 | 286 | 2.6km/132kV | `19536` | y |
| 1720 | 48.1 | 32 | solar | PAST_EXPECTED_START | Pipplepen Farm Solar Park - Solar Farm | Elgin Energy ES Co Limited | Somerset | 2023-01-24 | 1315 | 0.3km/132kV | `9481` | y |
| 1721 | 48.1 | 32 | solar | DESIGN_FROZEN_OR_LATER | Penpergwm Solar Farm (Great House Farm) | Renewable Connections Developments... | Welsh Government (NSIP) | 2023-01-17 | - | 0.2km/132kV | `10035` | y |
| 1722 | 48.1 | 32 | solar | PAST_EXPECTED_START | Drayton Manor Farm, Alcester Road - Solar Farm Phase... | Drayton Stratford | Stratford-on-Avon | 2023-11-07 | 1028 | 10.5km/400kV | `13508` | y |
| 1723 | 48.1 | 8 | bess | PAST_EXPECTED_START | Mill Farm, Teffont - Battery Energy Storage | Private Energy Partners Pty Limite... | Wiltshire | 2024-03-12 | 902 | 1.8km/132kV | `15320` | y |
| 1724 | 48.0 | 1 | solar | PAST_EXPECTED_START | Nigg Waste Water Plant, Coast Road - Solar PV Arrays | Scottish Water Horizons | Aberdeen City | 2023-09-15 | 1081 | 2.0km/132kV | `14657` | y |
| 1725 | 48.0 | 2 | solar | PAST_EXPECTED_START | Loggans Roundabout, Loggans Road - Solar Farm | Bauer Group | Cornwall | 2025-02-17 | 560 | 0.7km/132kV | `13701` | y |
| 1726 | 48.0 | 2 | solar | PRE_CONSENT | Drumforskie - Solar Array | Forster Group Ltd | Aberdeen City | - | - | 0.4km/132kV | `20237` | y |
| 1727 | 48.0 | 1 | solar | PAST_EXPECTED_START | Church Lane - Solar Canopy | Scunthorpe General Hospital | North Lincolnshire | 2025-05-19 | 469 | 1.7km/132kV | `18650` | y |
| 1728 | 48.0 | 1 | solar | PAST_EXPECTED_START | Sofina Distribution Centre, Normanby Enterprise Park... | Sofina Distribution Centre | North Lincolnshire | 2025-04-28 | 490 | 0.7km/132kV | `18196` | **n** |
| 1729 | 47.9 | 1 | solar | PAST_EXPECTED_START | Clipper Logistics, Shepcote Lane - Solar Panels | Logicor | Sheffield | 2023-01-05 | 1334 | 0.5km/275kV | `12743` | y |
| 1730 | 47.9 | 24 | bess | PRE_CONSENT | Manor Farm, Wick Lane - Solar Farm & Battery Storage | Qair UK | North Somerset | - | - | 1.4km/132kV | `14331` | y |
| 1731 | 47.9 | 1 | solar | PAST_EXPECTED_START | Parker Hannifin Manufacturing - Solar Panels | Parker Hannifin Manufacturing | Gateshead | 2023-08-10 | 1117 | 1.7km/132kV | `14249` | y |
| 1732 | 47.9 | 40 | solar | PRE_CONSENT | Hale Solar Farm | Elgin Energy | Buckinghamshire | - | - | 0.5km/132kV | `7969` | y |
| 1733 | 47.9 | 40 | solar | DESIGN_FROZEN_OR_LATER | Walpole Bank | DIF Capital Partners / Green Inves... | King's Lynn and West Norfolk | 2021-01-15 | - | 0.3km/400kV | `9524` | y |
| 1734 | 47.9 | 40 | bess | DESIGN_FROZEN_OR_LATER | Astra Centre, Royal Barn Road - Energy Storage | Arlington Energy Limited | Rochdale | 2021-11-01 | - | 0.1km/132kV | `9584` | y |
| 1735 | 47.9 | 40 | solar | DESIGN_FROZEN_OR_LATER | Barnsdale Road Solar Park | OnPath Energy | Leeds | 2021-10-21 | - | 0.6km/132kV | `14095` | **n** |
| 1736 | 47.9 | 40 | solar | PAST_EXPECTED_START | Nowhere Lane, Norwich - Solar Photovoltaic Panels | Albanwise Synergy Limited | South Norfolk | 2025-04-28 | 490 | 5.0km/132kV | `16707` | y |
| 1737 | 47.9 | 40 | bess | PRE_CONSENT | Kintore - Battery Energy Storage | Mespil Solar Energy | Scottish Government (S36) | - | - | 0.4km/132kV | `17470` | y |
| 1738 | 47.9 | 1 | solar | PAST_EXPECTED_START | East Golds Works, Kingsteignton Road - Solar Panels | Sibelco UK East Golds Works | Teignbridge | 2025-02-28 | 549 | 0.9km/132kV | `18000` | y |
| 1739 | 47.9 | 1 | solar | PAST_EXPECTED_START | Airyhall Distribution Service Reservoir, St Johns Te... | Scottish Water | Aberdeen City | 2023-09-01 | 1095 | 0.8km/132kV | `12839` | y |
| 1740 | 47.9 | 14 | bess | PAST_EXPECTED_START | Hare Craig Windfarm | EnergieKontor UK | East Ayrshire | 2022-07-12 | 1511 | 9.1km/400kV | `7261` | y |
| 1741 | 47.8 | 3 | solar | PAST_EXPECTED_START | ATS, Sopwith Way - Ground Mounted Solar Photovoltaic... | NATS | Fareham | 2024-06-11 | 811 | 2.7km/400kV | `15032` | y |
| 1742 | 47.8 | 6 | bess | PRE_CONSENT | Aston Grange, Aston - Solar Panels & Battery Energy ... | Innova Renewables | Cheshire West and Chester | - | - | 0.4km/132kV | `18374` | y |
| 1743 | 47.8 | 3 | solar | DESIGN_FROZEN_OR_LATER | Pepsico International Limited, Leycroft Road - Solar... | Walkers Snacks (Distribution) Limi... | Leicester | 2024-03-06 | - | 1.7km/400kV | `15743` | y |
| 1744 | 47.8 | 1 | solar | PAST_EXPECTED_START | Docks Way - Solar Panels | Newport City Council | Newport | 2024-08-07 | 754 | 0.1km/132kV | `15723` | y |
| 1745 | 47.8 | 50 | bess | PRE_CONSENT | Aultmore Forest - Buckie - Windfarm | Vattenfall | Scottish Government (S36) | - | - | 0.1km/400kV | `15995` | y |
| 1746 | 47.8 | 50 | bess | PRE_CONSENT | Cutts Bros, Wharf Road - Battery Storage Facility | Newton Energi Limited | Doncaster | - | - | 1.0km/132kV | `16514` | y |
| 1747 | 47.8 | 50 | bess | PRE_CONSENT | Wishaw Lane, Sutton Coldfield - Battery Energy Stora... | Wiggins Hill BESS Limited | Birmingham | - | - | 0.3km/132kV | `17996` | y |
| 1748 | 47.8 | 50 | bess | PRE_CONSENT | Kettleburgh Road Easton - Solar Panels & Battery Sto... | Quintas Cleantech | East Suffolk | - | - | 3.2km/400kV | `18299` | y |
| 1749 | 47.8 | 50 | bess | PRE_CONSENT | Marston Sewerage Pumping Station, Bodymoor Heath Lan... | Anesco Limited | North Warwickshire | - | - | 0.2km/132kV | `19075` | y |
| 1750 | 47.8 | 50 | solar | PAST_EXPECTED_START | Bypass Solar Farm | By-Pass Farm Solar Limited | South Kesteven | 2021-03-01 | 2009 | 1.5km/400kV | `9050` | y |
| 1751 | 47.8 | 50 | solar | PRE_CONSENT | Wood Lodge Farm, Huntingdon Road - Solar Farm | Unknown | North Northamptonshire | - | - | 0.6km/132kV | `14908` | **n** |
| 1752 | 47.8 | 50 | solar | PRE_CONSENT | Botley - Solar Photovoltaic Array | Red House Solar Limited | Vale of White Horse | - | - | 0.2km/400kV | `18174` | **n** |
| 1753 | 47.8 | 30 | bess | PRE_CONSENT | Catsbrain Farm | Green Hedge | Swindon | 2017-11-03 | - | 0.6km/132kV | `7988` | **n** |
| 1754 | 47.8 | 30 | bess | PRE_CONSENT | Roaring Hill (Resubmission) | Renewable Energy Systems (RES) | Fife | 2017-12-22 | - | 0.1km/275kV | `9224` | y |
| 1755 | 47.8 | 30 | bess | PRE_CONSENT | Jamesfield Organic Centre, Phase 1 | Harmony Energy Storage | Perth and Kinross | - | - | 0.3km/132kV | `10863` | y |
| 1756 | 47.8 | 30 | solar | PAST_EXPECTED_START | Galton Manor Farm - Solar Farm | Spring Dev 05 Limited | Dorset | 2023-03-30 | 1250 | 3.3km/132kV | `11197` | y |
| 1757 | 47.8 | 30 | solar | PRE_CONSENT | Leaford Solar Farm, Fulford Lane - Solar Farm | Renewable Energy Systems | Stafford | - | - | 2.3km/132kV | `14358` | y |
| 1758 | 47.8 | 30 | bess | PRE_CONSENT | Pound Farm Lane - Battery Storage | Pulse Clean Energy | Rhondda Cynon Taf | - | - | 0.1km/275kV | `20012` | y |
| 1759 | 47.8 | 1 | solar | PAST_EXPECTED_START | Merry Hill Centre - Solar Panels | Olympus Power | Dudley | 2023-08-07 | 1120 | 0.3km/132kV | `14431` | y |
| 1760 | 47.8 | 50 | solar | PAST_EXPECTED_START | Rag Lane Solar Farm | BayWa r.e. UK Limited | South Gloucestershire | 2021-12-02 | 1733 | 2.4km/275kV | `8393` | y |
| 1761 | 47.8 | 50 | solar | PRE_CONSENT | Clay Tye Road - Solar Farm | REG Windpower Limited | Havering | - | - | 0.4km/275kV | `9035` | y |
| 1762 | 47.8 | 50 | solar | PAST_EXPECTED_START | Turf Carr Solar Farm | Anesco Limited | East Riding of Yorkshire | 2024-05-29 | 824 | 0.9km/132kV | `11214` | y |
| 1763 | 47.8 | 50 | solar | PRE_CONSENT | Exton Lane, Burley - Solar Farm & Battery Storage | Econergy International Limited | Rutland | - | - | 3.9km/132kV | `11794` | y |
| 1764 | 47.8 | 50 | solar | PRE_CONSENT | Foxholes Farm, Roman Road - Solar Panels | Elgin Energy Esco Limited | North Northamptonshire | - | - | 1.2km/132kV | `12754` | y |
| 1765 | 47.8 | 50 | solar | PRE_CONSENT | Clifton Marsh Farm, Preston New Road - Solar Farm | Vattenfall | Fylde | - | - | 0.4km/132kV | `13763` | y |
| 1766 | 47.8 | 50 | bess | PAST_EXPECTED_START | Forest Avenue Cottage, Drumlithie - Battery Energy S... | Drumlithie Battery Limited | Aberdeenshire | 2023-11-14 | 1021 | 2.5km/275kV | `13986` | y |
| 1767 | 47.8 | 50 | solar | PRE_CONSENT | Longbreach Solar Farm | Noventum Power Limited | Buckinghamshire | - | - | 0.9km/400kV | `14279` | y |
| 1768 | 47.8 | 50 | solar | PRE_CONSENT | Cowley House Solar Farm | Unknown | County Durham | 2021-01-25 | - | 0.3km/400kV | `16393` | y |
| 1769 | 47.8 | 50 | bess | PRE_CONSENT | Admiralty Road - Battery Energy Storage Facility | BAT-NR30 Limited | Great Yarmouth | 2021-08-19 | - | 4.1km/132kV | `16394` | y |
| 1770 | 47.8 | 50 | bess | PRE_CONSENT | Loanhead Farm - Battery Energy Storage System | OPDE UK Limted | Moray | - | - | 0.2km/132kV | `16619` | y |
| 1771 | 47.8 | 50 | solar | PRE_CONSENT | Willowfields Energy Park, Marcham - Solar Panels | Exagen Development Limited | Vale of White Horse | - | - | 2.6km/132kV | `16902` | y |
| 1772 | 47.8 | 50 | solar | PRE_CONSENT | Mantle Solar Farm, Wymeswold - Solar Farm | Exagen | Charnwood | - | - | 2.6km/132kV | `18150` | y |
| 1773 | 47.8 | 50 | solar | PRE_CONSENT | West Pitnacree Farm, Alyth - Solar Panels | Greentech | Perth and Kinross | - | - | 3.3km/275kV | `18187` | y |
| 1774 | 47.8 | 50 | solar | PRE_CONSENT | Overton Grange, Overton Road - Solar Farm Battery En... | Anesco Limited | North Yorkshire | - | - | 0.5km/275kV | `18188` | y |
| 1775 | 47.8 | 50 | solar | PRE_CONSENT | Kettleburgh Road Easton - Solar Panels & Battery Sto... | Quintas Cleantech | East Suffolk | - | - | 3.2km/400kV | `18300` | y |
| 1776 | 47.8 | 50 | solar | PRE_CONSENT | Fourstones - Solar Park | Mespil Solar Energy | Northumberland | - | - | 0.3km/275kV | `18692` | y |
| 1777 | 47.8 | 50 | solar | PRE_CONSENT | Leys Lane - Solar Panels | Farm Energy Company | North Yorkshire | - | - | 2.1km/400kV | `19160` | y |
| 1778 | 47.8 | 30 | solar | PAST_EXPECTED_START | Llangennech Solar | Voltalia UK | Welsh Government (NSIP) | 2021-07-23 | 1865 | 3.0km/132kV | `6795` | y |
| 1779 | 47.8 | 30 | bess | PRE_CONSENT | Learielaw Farm | Intelligent Land Investments | West Lothian | 2020-10-29 | - | 0.7km/132kV | `13368` | y |
| 1780 | 47.8 | 30 | solar | PRE_CONSENT | Over Rankeilour Farm - Solar Farm | Balance Power Projects Limited | Fife | - | - | 1.7km/132kV | `16630` | y |
| 1781 | 47.8 | 50 | solar | PRE_CONSENT | Freeby Lane, Green Energy Park - Solar Panels & Batt... | Downing Renewable Developments | Melton | - | - | 3.2km/132kV | `18302` | y |
| 1782 | 47.8 | 1 | bess | PAST_EXPECTED_START | Brynwhilach Solar Farm, Morriston - Battery Storage | Swansea Bay University Health Boar... | Swansea | 2023-03-29 | 1251 | 0.1km/132kV | `1975` | y |
| 1783 | 47.8 | 1 | solar | PAST_EXPECTED_START | St Bedes Inter-Church School | Solar Options for Schools | Cambridge | 2019-03-29 | 2712 | 0.6km/132kV | `7275` | y |
| 1784 | 47.8 | 1 | solar | PAST_EXPECTED_START | Tesco Burnage Store | Tesco Stores | Manchester | 2020-01-15 | 2420 | 1.7km/275kV | `7619` | y |
| 1785 | 47.8 | 1 | solar | PAST_EXPECTED_START | Tesco Superstore Wisemore | Push Energy | Walsall | 2020-07-01 | 2252 | 1.0km/132kV | `7731` | y |
| 1786 | 47.8 | 1 | solar | PAST_EXPECTED_START | Crossens Pumping Station - Solar Array | Environment Agency | Sefton | 2022-02-25 | 1648 | 0.8km/132kV | `9513` | y |
| 1787 | 47.8 | 1 | solar | PAST_EXPECTED_START | Worcester Road, Wychbold - Solar Photovoltaic Panels | Webbs Garden Centre | Wychavon | 2022-10-28 | 1403 | 0.9km/132kV | `10885` | y |
| 1788 | 47.8 | 1 | bess | PAST_EXPECTED_START | Nelson and colne college, Scotland Road | Nelson & Colne College | Pendle | 2024-05-09 | 844 | 0.4km/132kV | `14414` | **n** |
| 1789 | 47.8 | 1 | bess | PAST_EXPECTED_START | Mid Kent College Medway Campus, Medway Road - Batter... | Mid Kent College | Medway | 2023-11-23 | 1012 | 1.5km/132kV | `15833` | y |
| 1790 | 47.8 | 1 | solar | PAST_EXPECTED_START | Y Tyddyn Teg, Heol Y Nant - Solar Farm | Power on Demand Limited | Carmarthenshire | 2025-01-29 | 579 | 0.3km/400kV | `16617` | y |
| 1791 | 47.8 | 50 | bess | PRE_CONSENT | Bronwylfa Road, Talwrn - Battery Storage Facility | Pelagic Energy | Wrexham | - | - | 0.1km/400kV | `13768` | y |
| 1792 | 47.8 | 50 | bess | PRE_CONSENT | Elvington Battery Energy Storage | Pathfinder Clean Energy UK Limited | Dover | - | - | 0.1km/132kV | `17462` | y |
| 1793 | 47.8 | 50 | solar | PRE_CONSENT | Elvington Solar Farm | Pathfinder Clean Energy UK Limited | Dover | - | - | 0.1km/132kV | `17463` | y |
| 1794 | 47.8 | 3 | solar | PAST_EXPECTED_START | Featherstone House Farm | C A Strawson Ltd | Newark and Sherwood | 2016-04-19 | 3786 | 0.7km/132kV | `C1764` | **n** |
| 1795 | 47.8 | 49 | bess | PRE_CONSENT | Chapel Lane - Battery Energy Storage System | Anesco Limited | Walsall | - | - | 0.1km/400kV | `15308` | y |
| 1796 | 47.7 | 3 | solar | PAST_EXPECTED_START | Airbus UK Industrial Complex - Solar panels | Custom Solar Limited | South Gloucestershire | 2024-04-25 | 858 | 1.6km/132kV | `16014` | y |
| 1797 | 47.7 | 48 | solar | PRE_CONSENT | Seaham Solar Park, Stockton Road - Solar Farm | Elements Green | County Durham | - | - | 4.4km/275kV | `17386` | y |
| 1798 | 47.6 | 10 | bess | PRE_CONSENT | Broad Lane, Cawood - Solar Farm & Battery Storage | Quintas Cleantech | North Yorkshire | - | - | 1.8km/132kV | `17885` | y |
| 1799 | 47.6 | 10 | bess | PRE_CONSENT | Lassington Lane, Highnam - Battery Storage | Pathfinder Clean Energy UK Dev Lim... | Tewkesbury | - | - | 0.6km/132kV | `19389` | y |
| 1800 | 47.6 | 10 | bess | PRE_CONSENT | Marton Sewage Works, High Street - Battery Energy St... | Loire Capital Holdings Limited | West Lindsey | - | - | 0.3km/132kV | `20514` | y |
| 1801 | 47.6 | 13 | solar | PAST_EXPECTED_START | Cullerlie Solar Farm | Elgin Energy ES Co Limited | Aberdeenshire | 2021-11-12 | 1753 | 1.1km/132kV | `8842` | y |
| 1802 | 47.6 | 13 | solar | PAST_EXPECTED_START | Rugby Road, Kilsby - Rainsbrook Solar Farm | Voltalia Limited | West Northamptonshire | 2023-04-12 | 1237 | 3.7km/132kV | `11896` | y |
| 1803 | 47.6 | 22 | bess | PRE_CONSENT | Kyllachy Wind Farm - BESS | Wind Estate (UK) Limited | Scottish Government (S36) | - | - | 0.1km/275kV | `16784` | y |
| 1804 | 47.6 | 3 | solar | PAST_EXPECTED_START | Ty Coch Hollybush Way | Torfaen CBC | Torfaen | 2019-10-21 | 2506 | 0.5km/132kV | `7240` | y |
| 1805 | 47.6 | 3 | solar | PAST_EXPECTED_START | Coton Road - Solar Photovoltaic Panels | Food and Rural Affairs | North Warwickshire | 2022-03-09 | 1636 | 0.6km/132kV | `9788` | y |
| 1806 | 47.6 | 3 | solar | PAST_EXPECTED_START | Euro Car Parts - Solar Panels & Battery Storage | Ivegate Limited | North Warwickshire | 2023-10-19 | 1047 | 1.9km/132kV | `14895` | y |
| 1807 | 47.6 | 3 | solar | PAST_EXPECTED_START | Elvington Water Treatment Works - Solar Photovoltaic... | Downing Renewable Developments | York | 2025-04-29 | 489 | 2.4km/400kV | `16967` | y |
| 1808 | 47.6 | 100 | bess | PRE_CONSENT | Gotham - Battery Energy storage | Net Zero Energy Development Limite... | Rushcliffe | - | - | 0.1km/400kV | `10986` | **n** |
| 1809 | 47.6 | 100 | bess | PRE_CONSENT | Clune Wind Farm - Battery Energy Storage | Renewable Energy Systems | Scottish Government (S36) | - | - | 3.5km/132kV | `15964` | y |
| 1810 | 47.6 | 100 | bess | PRE_CONSENT | Gotham - Battery Energy storage | Net Zero Energy Development Limite... | Rushcliffe | - | - | 0.1km/400kV | `16458` | y |
| 1811 | 47.6 | 165 | solar | PRE_CONSENT | Bowshiel Farm - Solar Farm | Voltalia UK | Scottish Government (S36) | - | - | 2.2km/400kV | `17780` | y |
| 1812 | 47.5 | 36 | solar | DESIGN_FROZEN_OR_LATER | Ducklington Solar Farm | Novus Renewable Services / Innova ... | West Oxfordshire | 2022-03-01 | - | 1.5km/132kV | `9090` | y |
| 1813 | 47.5 | 98 | solar | PRE_CONSENT | North Ray Solar Farm, Lincoln Gate - Solar Panels | TotalEnergies (North Ray Solar Far... | East Lindsey | - | - | 9.0km/132kV | `19975` | y |
| 1814 | 47.5 | 12 | solar | PRE_CONSENT | Horton Landfill Site, Henfield Road - Solar Panels | Valencia Energy Limited | Horsham | - | - | 1.0km/132kV | `16236` | y |
| 1815 | 47.4 | 2 | bess | PAST_EXPECTED_START | Former Howden Clough, Howden Clough Road - Battery U... | Biffa Waste Services Limited | Leeds | 2023-04-27 | 1222 | 0.7km/275kV | `12596` | y |
| 1816 | 47.4 | 2 | solar | PAST_EXPECTED_START | Coach Road Meadow - Solar Farm | Prospects Community Energy Limited | Hyndburn | 2024-06-14 | 808 | 1.6km/132kV | `13958` | y |
| 1817 | 47.4 | 3 | solar | PAST_EXPECTED_START | Nettlehill Road - Solar Panels | Zestec Renewable Energy | West Lothian | 2024-02-29 | 914 | 3.8km/132kV | `15820` | y |
| 1818 | 47.4 | 7 | solar | PAST_EXPECTED_START | Outwood Farm (Phase 2) | Wirsol | Basildon | 2014-12-11 | 4281 | 3.2km/132kV | `6170` | y |
| 1819 | 47.3 | 12 | solar | PAST_EXPECTED_START | University of Surrey, Blackwell Farm - Solar Farm | SSE Enterprise Contracting | Guildford | 2025-04-18 | 500 | 3.9km/132kV | `16170` | y |
| 1820 | 47.3 | 4 | solar | PAST_EXPECTED_START | Lyreco, Donnington Wood - Solar Panels | Private Developer | Telford and Wrekin | 2025-12-03 | 271 | 4.4km/132kV | `19957` | y |
| 1821 | 47.3 | 34 | solar | PRE_CONSENT | Bull Street, Creech St Michael - Solar Farm | Spring Dev 11 Limited | Somerset | - | - | 5.3km/132kV | `19222` | y |
| 1822 | 47.2 | 20 | solar | PAST_EXPECTED_START | Red House Farm - Solar Farm | Anesco Limited | Huntingdonshire | 2021-12-07 | 1728 | 5.1km/400kV | `9518` | y |
| 1823 | 47.2 | 20 | solar | PAST_EXPECTED_START | Knockkippen Wind, Solar & Battery Farm | Falck Renewables / REG Windpower | Scottish Government (S36) | 2025-04-30 | 488 | 1.9km/132kV | `10468` | y |
| 1824 | 47.2 | 20 | solar | PRE_CONSENT | Wisborough Green - Solar Photovoltaic Panels | Renewable Connections Developments... | Chichester | - | - | 1.5km/400kV | `16113` | y |
| 1825 | 47.2 | 20 | bess | PAST_EXPECTED_START | Hillcrest Cottage, Shebster - Battery Energy Storage... | Statkraft UK Limited | Highland | 2022-08-22 | 1470 | 0.3km/275kV | `10226` | y |
| 1826 | 47.2 | 5 | solar | PAST_EXPECTED_START | Home Farm, Hursley Park Road - Solar Panels | Clean Energy Capital (CEC) Limited | Winchester | 2025-06-26 | 431 | 2.3km/132kV | `17529` | y |
| 1827 | 47.2 | 5 | solar | PAST_EXPECTED_START | Ash Farm, Charlton Road - Solar Panels | Ash Farm Solar Limited | Somerset | 2024-12-13 | 626 | 4.7km/132kV | `14026` | y |
| 1828 | 47.2 | 9 | bess | PAST_EXPECTED_START | MOD Pendine, Llanmiloe - Solar Panels | QinetiQ | Carmarthenshire | 2024-10-09 | 691 | 5.0km/400kV | `14019` | y |
| 1829 | 47.1 | 15 | bess | PAST_EXPECTED_START | Three Bridges Solar Farm | Pathfinder Clean Energy UK Dev Lim... | Breckland | 2021-03-10 | 2000 | 5.7km/132kV | `8219` | y |
| 1830 | 47.1 | 15 | solar | PAST_EXPECTED_START | Three Bridges Solar Farm | Pathfinder Clean Energy UK Dev Lim... | Breckland | 2021-03-10 | 2000 | 5.7km/132kV | `8220` | y |
| 1831 | 47.1 | 70 | bess | PRE_CONSENT | Tontine Road - Battery Energy Storage System | Coriolis Energy | West Lancashire | - | - | 0.3km/132kV | `9819` | y |
| 1832 | 47.1 | 70 | bess | PRE_CONSENT | Tean Leys Farm, Tean Leys - Battery Storage | Tean Leys Energy Storage Limited | Staffordshire Moorlands | - | - | 0.3km/400kV | `17803` | y |
| 1833 | 47.1 | 3 | solar | PAST_EXPECTED_START | Premier Grocery Products Limited, Claylands Avenue -... | Premier Foods | Bassetlaw | 2024-12-11 | 628 | 3.0km/132kV | `17366` | y |
| 1834 | 47.1 | 42 | solar | PRE_CONSENT | Salters Lane - Solar Panels | Grupotec Solar Uk 9 Limited | Durham | - | - | 4.8km/400kV | `18564` | y |
| 1835 | 47.1 | 25 | solar | PRE_CONSENT | Pencaerlan Solar Farm | Greentech Projects Holding UK Limi... | Welsh Government (NSIP) | - | - | 0.5km/400kV | `9984` | y |
| 1836 | 47.1 | 25 | solar | PAST_EXPECTED_START | Frithwood Farm, Frithwood Lane - Solar Farm | Elgin Energy EsCo Limited | Bolsover | 2023-12-01 | 1004 | 2.8km/132kV | `13013` | y |
| 1837 | 47.0 | 2 | solar | PAST_EXPECTED_START | Omega Proteins - Solar Farm & Battery Storage | Leo Group Limited | Westmorland and Furness | 2023-05-19 | 1200 | 0.8km/132kV | `9544` | y |
| 1838 | 46.9 | 40 | solar | PRE_CONSENT | E/o the Academy Of Light, Sunderland Road - Solar Fa... | Sunderland AFC | South Tyneside | - | - | 4.4km/275kV | `13438` | y |
| 1839 | 46.9 | 40 | solar | PRE_CONSENT | Fibden Farm - Solar Array | Grenergy Renewables | Wychavon | - | - | 1.2km/132kV | `15976` | y |
| 1840 | 46.9 | 40 | solar | PRE_CONSENT | Cavendish Dock Road - Solar Array | Associated British Ports | Westmorland and Furness | - | - | 2.1km/132kV | `17087` | y |
| 1841 | 46.9 | 40 | solar | PRE_CONSENT | Hanwell Estate, Main Street - Solar Farm | Elgin Energy | Cherwell | - | - | 3.1km/132kV | `18446` | y |
| 1842 | 46.9 | 40 | bess | PRE_CONSENT | Smithy Lane, Staining - Solar PV Panels & BESS | Boom Power Limited | Fylde | - | - | 0.3km/132kV | `20961` | y |
| 1843 | 46.9 | 40 | solar | PRE_CONSENT | Smithy Lane, Staining - Solar PV Panels & BESS | Boom Power Limited | Fylde | - | - | 0.3km/132kV | `20962` | y |
| 1844 | 46.9 | 2 | solar | PAST_EXPECTED_START | Docks Way Solar Farm | Newport City Council | Newport | 2021-12-01 | 1734 | 0.3km/400kV | `8923` | y |
| 1845 | 46.9 | 6 | solar | PAST_EXPECTED_START | Masons Landfill, Bramford Road, Great Blakenham - So... | Valencia Waster Management Limited | Mid Suffolk | 2024-03-19 | 895 | 2.0km/132kV | `11683` | y |
| 1846 | 46.8 | 6 | bess | PAST_EXPECTED_START | Hamble Lane Battery Energy Storage | Balanced Grid Solutions | Eastleigh | 2019-11-22 | 2474 | 3.1km/132kV | `7420` | y |
| 1847 | 46.8 | 50 | bess | DISTRESSED | Wolverhampton West Sub Station | Statera Energy | South Staffordshire | 2016-10-21 | - | 0.1km/132kV | `6977` | **n** |
| 1848 | 46.8 | 50 | bess | DISTRESSED | Penwortham Sub Station | Statera Energy | South Ribble | 2021-05-14 | - | 0.0km/132kV | `7119` | **n** |
| 1849 | 46.8 | 50 | bess | PRE_CONSENT | Barlow Road, Barlow - Battery Storage | Vox Energy Limited | North Yorkshire | - | - | 2.4km/132kV | `12734` | **n** |
| 1850 | 46.8 | 50 | bess | PRE_CONSENT | Brunt Hill Wind Farm & Battery Storage | E Power Limited | Scottish Government (S36) | - | - | 0.1km/132kV | `12824` | y |
| 1851 | 46.8 | 50 | solar | PRE_CONSENT | Haxted Mead, Lingfield - Solar Farm | Haxted Mead Solar Farm Limited | Tandridge | - | - | 5.1km/132kV | `19401` | y |
| 1852 | 46.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | South Fambridge Hall - Solar farm & Battery storage | British Solar Renewables / BayWa r... | Rochford | 2021-12-15 | - | 0.7km/132kV | `9274` | y |
| 1853 | 46.8 | 50 | solar | PAST_EXPECTED_START | Ashorne Hill - Solar Farm | JBM Solar Projects Limited | Stratford-on-Avon | 2022-08-03 | 1489 | 2.3km/132kV | `9493` | y |
| 1854 | 46.8 | 50 | solar | PRE_CONSENT | Winterton Road, Roxby - Solar Farm | Solar 2 Limited | North Lincolnshire | - | - | 2.4km/132kV | `12162` | y |
| 1855 | 46.8 | 30 | solar | PRE_CONSENT | Wrotham Park - Solar Panels | Enviromena | Hertsmere | - | - | 1.1km/275kV | `19077` | y |
| 1856 | 46.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Winkburn Estate Solar Farm | Lightsource SPV 154 Limited | Newark and Sherwood | 2021-05-20 | - | 2.1km/132kV | `7388` | y |
| 1857 | 46.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Perrinpit Farm | Grune Energien | South Gloucestershire | 2022-09-21 | - | 0.5km/132kV | `7944` | y |
| 1858 | 46.8 | 50 | solar | PRE_CONSENT | Bramford Solar Farm | Bramford Green | Mid Suffolk | 2023-02-17 | - | 0.1km/132kV | `8008` | **n** |
| 1859 | 46.8 | 50 | bess | PAST_EXPECTED_START | Claydon Farm - Solar Farm & Battery Storage | JBM Solar Projects 17 Limited | Tewkesbury | 2021-12-17 | 1718 | 2.0km/132kV | `8038` | y |
| 1860 | 46.8 | 50 | solar | PAST_EXPECTED_START | Claydon Farm - Solar Farm & Battery Storage | JBM Solar Projects 17 Limited | Tewkesbury | 2021-12-17 | 1718 | 2.0km/132kV | `8039` | y |
| 1861 | 46.8 | 50 | solar | PAST_EXPECTED_START | Myttons Solar Farm | JBM Solar Projects Limited | Telford and Wrekin | 2021-03-15 | 1995 | 4.0km/400kV | `8226` | y |
| 1862 | 46.8 | 50 | solar | PAST_EXPECTED_START | Fernbrook - Solar farm & Battery storage | Low Carbon UK Solar Investment Com... | Dorset | 2023-02-13 | 1295 | 3.5km/132kV | `8506` | y |
| 1863 | 46.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Mannington Battery Energy Storage System | EDF Energy Renewables | Dorset | 2021-07-02 | - | 0.2km/400kV | `8833` | y |
| 1864 | 46.8 | 50 | solar | PAST_EXPECTED_START | Feldon Vale Solar Farm | Low Carbon Limited | Stratford-on-Avon | 2021-08-13 | 1844 | 3.4km/132kV | `12137` | y |
| 1865 | 46.8 | 50 | bess | PRE_CONSENT | Ellbridge Lane | Pivot Power | Cornwall | - | - | 0.3km/400kV | `12697` | y |
| 1866 | 46.8 | 2 | solar | PAST_EXPECTED_START | Bassingbourn Barracks, Old North Road - Solar PV Arr... | Defence Infrastructure Organisatio... | South Cambridgeshire | 2024-07-17 | 775 | 3.4km/132kV | `14347` | y |
| 1867 | 46.8 | 4 | solar | PAST_EXPECTED_START | Skelton Grange Landfill Site, Pontefract Lane - Sola... | Biffa Waste Services Limited | Leeds | 2023-09-29 | 1067 | 0.6km/275kV | `12937` | y |
| 1868 | 46.8 | 6 | solar | PAST_EXPECTED_START | Perrigo, Exeter Road - Solar Panels | Wrafton Laboratories (Trading as P... | North Devon | 2023-06-20 | 1168 | 2.9km/132kV | `13053` | y |
| 1869 | 46.7 | 29 | solar | DESIGN_FROZEN_OR_LATER | North Angle Farm | Cambridgeshire County Council / Bo... | East Cambridgeshire | 2020-11-25 | - | 0.4km/400kV | `7482` | y |
| 1870 | 46.7 | 22 | solar | PAST_EXPECTED_START | Hartley Wood Farm - Solar Farm | Bluefield Renewable Developments L... | Tendring | 2022-08-25 | 1467 | 3.0km/132kV | `9440` | y |
| 1871 | 46.7 | 2 | solar | PAST_EXPECTED_START | BAC Jaguar Land Rover Battery Assembly Centre, Canto... | Columbia Threadneedle Investments ... | North Warwickshire | 2024-03-04 | 910 | 0.3km/400kV | `15768` | y |
| 1872 | 46.7 | 2 | bess | PAST_EXPECTED_START | Cheltenham General Hospital - Battery Energy Storage... | Gloucestershire Hospitals NHS Foun... | Cheltenham | 2021-09-28 | 1798 | 0.9km/132kV | `9515` | y |
| 1873 | 46.6 | 10 | bess | PAST_EXPECTED_START | Aspley House Farm, Aspley Lane - Battery Storage Fac... | Hydrock | Stafford | 2023-01-27 | 1312 | 2.8km/132kV | `12571` | y |
| 1874 | 46.6 | 4 | solar | PAST_EXPECTED_START | Unit 3, Wilders Way - Solar Photovoltaic Panels | The Very Group | North West Leicestershire | 2022-09-20 | 1441 | 1.9km/400kV | `8862` | y |
| 1875 | 46.6 | 10 | bess | PAST_EXPECTED_START | Acharn Forest - Battery Storage | Biomass Energy Renewables Llp | Stirling | 2024-01-10 | 964 | 0.3km/132kV | `15321` | y |
| 1876 | 46.6 | 3 | solar | PAST_EXPECTED_START | Locher Works, Kilbarchan Road - Solar Photovoltaic A... | Bluestone Energy | Renfrewshire | 2024-09-05 | 725 | 0.8km/400kV | `15132` | y |
| 1877 | 46.6 | 100 | bess | PAST_EXPECTED_START | Kilgallioch - Battery energy storage | Scottish Power Renewables | Scottish Government (S36) | 2024-07-16 | 776 | 9.7km/132kV | `4386` | y |
| 1878 | 46.5 | 1 | solar | PRE_CONSENT | Horizon Centre, Gretton Road - Solar Array | Custom Solar Limited | North Northamptonshire | - | - | 2.1km/132kV | `19841` | y |
| 1879 | 46.5 | 126 | bess | PRE_CONSENT | Derehams Farm, Derehams Lane - Battery Storage | Newton Energi Limited | Buckinghamshire | - | - | 5.2km/400kV | `12649` | **n** |
| 1880 | 46.4 | 21 | solar | PAST_EXPECTED_START | Park Farm - Solar Panels | British Solar Renewables | East Suffolk | 2024-06-17 | 805 | 0.7km/400kV | `9087` | y |
| 1881 | 46.4 | 2 | solar | PAST_EXPECTED_START | Mercedes Benz UK - Solar array car port | Mercedes Benz Retail Group Limited | Milton Keynes | 2021-09-27 | 1799 | 4.7km/132kV | `9277` | y |
| 1882 | 46.4 | 2 | solar | PAST_EXPECTED_START | Albany Road - Solar Array | Solar Advanced Systems Limited T A... | Gateshead | 2021-12-10 | 1725 | 2.4km/132kV | `9830` | y |
| 1883 | 46.4 | 2 | solar | PAST_EXPECTED_START | The Wyman Gordon Facility, Nettlehill Road- Solar Fa... | Wyman-Gordon Limited | West Lothian | 2023-01-10 | 1329 | 3.3km/132kV | `11955` | y |
| 1884 | 46.4 | 2 | solar | PAST_EXPECTED_START | Dova Way, Barrow Island - Solar Array | Cumbria County Council | Westmorland and Furness | 2023-03-03 | 1277 | 1.8km/132kV | `12603` | y |
| 1885 | 46.4 | 35 | solar | PRE_CONSENT | Bognop Road, Essington - Solar Farm & Battery Energy... | Intelligent Alternatives Limited | South Staffordshire | - | - | 2.0km/275kV | `10678` | y |
| 1886 | 46.4 | 35 | solar | PRE_CONSENT | Escot Park Estate, Talaton - Solar Farm | Elgin Energy Esco Limited | East Devon | - | - | 2.6km/400kV | `19716` | y |
| 1887 | 46.4 | 45 | bess | PRE_CONSENT | Pleasance Road | Coronation Power | Perth and Kinross | - | - | 0.3km/132kV | `9997` | y |
| 1888 | 46.4 | 16 | bess | PRE_CONSENT | Mere Flats Solar Farm | NextPower UK | Doncaster | - | - | 0.3km/275kV | `11022` | y |
| 1889 | 46.4 | 16 | solar | PRE_CONSENT | Coal Pit Lane, Willey - Solar Farm | Enviromena | Rugby | - | - | 1.1km/132kV | `18978` | y |
| 1890 | 46.3 | 57 | bess | DESIGN_FROZEN_OR_LATER | Capenhurst Lane, Capenhurst - Battery storage | HD888CAP Limited | Cheshire West and Chester | 2022-03-11 | - | 0.1km/132kV | `9377` | y |
| 1891 | 46.3 | 12 | bess | PAST_EXPECTED_START | Caterham Bypass - Battery Energy Storage | Ylem Energy Limited | Tandridge | 2024-09-05 | 725 | 6.5km/132kV | `15574` | y |
| 1892 | 46.3 | 26 | solar | PRE_CONSENT | Ramsclough Farm, Haslingden Old Road - Solar Farm | Abei Energy Limited | Hyndburn | - | - | 2.9km/132kV | `19457` | y |
| 1893 | 46.3 | 44 | solar | PRE_CONSENT | Lullington Solar Park | Lullington Solar Park Limited | South Derbyshire | - | - | 2.8km/132kV | `9396` | **n** |
| 1894 | 46.3 | 4 | solar | PAST_EXPECTED_START | Two Oaks Quarry, Coxmoor Road - Solar Array | The Mansfield Sand Company Limited | Ashfield | 2024-01-31 | 943 | 1.6km/132kV | `12715` | y |
| 1895 | 46.3 | 34 | solar | PRE_CONSENT | Hundred Acre Lane, Carlton In Lindrick - Solar Panel... | Elawan Energy | Bassetlaw | - | - | 3.9km/132kV | `18905` | y |
| 1896 | 46.3 | 2 | solar | PAST_EXPECTED_START | Iport Avenue, New Rossington Solar Panels | Sonne Solar Limited | Doncaster | 2021-03-29 | 1981 | 0.3km/400kV | `8446` | y |
| 1897 | 46.3 | 9 | solar | PAST_EXPECTED_START | Main Terminal 1 Edinburgh Airport - Solar Farm | City of Edinburgh Council / Edinbu... | City of Edinburgh | 2021-10-25 | 1771 | 4.2km/275kV | `11672` | y |
| 1898 | 46.3 | 9 | bess | PAST_EXPECTED_START | Parkend Crossgates - Solar Panels & Battery Storage | Greentech Projects Holding UK Limi... | Fife | 2024-03-07 | 907 | 3.1km/132kV | `11861` | y |
| 1899 | 46.3 | 9 | solar | PRE_CONSENT | North Moss Lane - Solar Photovoltaic Farm | Taiyo Power & Storage Limited | Sefton | - | - | 1.6km/132kV | `18292` | y |
| 1900 | 46.2 | 20 | bess | PRE_CONSENT | Basing Road | Eco-Economix | Basingstoke and Deane | - | - | 0.4km/132kV | `7746` | y |
| 1901 | 46.2 | 20 | bess | PRE_CONSENT | Kirkhaw Lane | Walker & Son (Hauliers) Limited | Wakefield | - | - | 0.2km/132kV | `8430` | **n** |
| 1902 | 46.2 | 20 | bess | PRE_CONSENT | Moggerhanger Road, Sandy - Solar Farm | Kach Capital Estates Limited | Central Bedfordshire | - | - | 2.4km/400kV | `9349` | y |
| 1903 | 46.2 | 20 | bess | PRE_CONSENT | Plymouth Stor Generation - Battery storage | Green Frog Power 214 Limited | Plymouth | 2021-06-15 | - | 0.0km/132kV | `17928` | y |
| 1904 | 46.2 | 20 | solar | PRE_CONSENT | Somerton Door Farm, Somerton Door Drove - Solar farm | Sky UK Development Limited | Somerset | - | - | 6.5km/132kV | `19464` | y |
| 1905 | 46.2 | 9 | solar | PRE_CONSENT | Saltlands Avenue - Solar Parks | Somerset County Council | Somerset | - | - | 1.2km/400kV | `10136` | y |
| 1906 | 46.2 | 5 | bess | PAST_EXPECTED_START | Showfield Lane | Enstor Energy | North Yorkshire | 2019-02-06 | 2763 | 0.5km/132kV | `7171` | y |
| 1907 | 46.2 | 5 | solar | PAST_EXPECTED_START | Lower Mays Farm Solar Farm | Unknown | Wealden | 2021-07-15 | 1873 | 0.3km/132kV | `8372` | y |
| 1908 | 46.2 | 5 | solar | PAST_EXPECTED_START | Haberfield Park Farm - Solar Farm | PS Renewables Limited | North Somerset | 2023-11-17 | 1018 | 2.8km/132kV | `14017` | y |
| 1909 | 46.2 | 1 | solar | PAST_EXPECTED_START | Baker Perkins, Manor Drive - Solar Panels | Power Zero Limited | Peterborough | 2025-09-16 | 349 | 2.3km/132kV | `19342` | y |
| 1910 | 46.2 | 1 | solar | PAST_EXPECTED_START | Wilton Engineering Services, Port Clarence Offshore ... | Port Clarence Logistics Limited | Stockton-on-Tees | 2025-09-24 | 341 | 2.1km/400kV | `20085` | y |
| 1911 | 46.2 | 1 | solar | PRE_CONSENT | West Lodge Farm Solar Array | Highview Consultants Limited | North Northamptonshire | - | - | 4.0km/132kV | `20471` | y |
| 1912 | 46.1 | 15 | bess | PRE_CONSENT | Idleigh Court Road, New Ash Green - Solar Array | Evolution Power | Sevenoaks | - | - | 2.0km/132kV | `16695` | y |
| 1913 | 46.1 | 2 | solar | PAST_EXPECTED_START | Manor Farm, Crickheath - Solar Array | Manor Farm | Shropshire | 2023-10-25 | 1041 | 0.4km/132kV | `14573` | y |
| 1914 | 46.1 | 4 | solar | PAST_EXPECTED_START | Cannington - Solar Panels | Yeo Valley Properties Limited | Somerset | 2022-05-31 | 1553 | 0.8km/400kV | `10493` | y |
| 1915 | 46.1 | 25 | solar | PAST_EXPECTED_START | Bucklesham Solar Farm | Novus Renewable Services Limited | East Suffolk | 2023-11-28 | 1007 | 8.0km/132kV | `9399` | y |
| 1916 | 46.1 | 32 | bess | PRE_CONSENT | Gloucestershire Science and Technology Park (small) | Ecotricity | Stroud | - | - | 0.6km/132kV | `10796` | y |
| 1917 | 46.0 | 19 | bess | PRE_CONSENT | Jamesfield Organic Centre, Phase 2 | Harmony Energy Storage | Perth and Kinross | - | - | 0.3km/132kV | `10863` | y |
| 1918 | 46.0 | 19 | solar | PAST_EXPECTED_START | Wee Minnemoer, Millport - Solar Farm & Battery Stora... | Comsol Energy | North Ayrshire | 2024-02-09 | 934 | 4.0km/132kV | `13091` | y |
| 1919 | 46.0 | 2 | solar | PAST_EXPECTED_START | Xtratherm UK | Aniron Renewables | North East Derbyshire | 2020-05-01 | 2313 | 0.8km/132kV | `7951` | y |
| 1920 | 46.0 | 31 | solar | PRE_CONSENT | New South Farm, Piper Lane - Solar Farm | Abei Energy Group | Rotherham | - | - | 2.2km/275kV | `17927` | y |
| 1921 | 46.0 | 3 | bess | PAST_EXPECTED_START | Phoenix Healthcare Distribution Centre - Battery Sto... | Phoenix Medical Supplies | Wakefield | 2024-02-29 | 914 | 0.1km/400kV | `15807` | y |
| 1922 | 45.9 | 1 | solar | PAST_EXPECTED_START | WHS Plastics, Water Orton Lane - Solar Panels | WHS Plastics Limited | North Warwickshire | 2024-12-19 | 620 | 0.3km/275kV | `17536` | y |
| 1923 | 45.9 | 24 | solar | PRE_CONSENT | Primrose Hill Farm, Oxford Road - Solar Farm | Mespil Solar Energy | West Northamptonshire | - | - | 5.8km/132kV | `17832` | y |
| 1924 | 45.9 | 40 | bess | PRE_CONSENT | Breach Farm | Green Hedge Energy Barn | South Derbyshire | - | - | 0.4km/132kV | `6914` | y |
| 1925 | 45.9 | 40 | solar | PAST_EXPECTED_START | Hessay Solar Farm | Solar2 Limited | York | 2024-03-11 | 903 | 2.3km/275kV | `11974` | y |
| 1926 | 45.9 | 2 | solar | PRE_CONSENT | Howden Clough Landfill, Howden Clough Road - Solar F... | Biffa Waste Services Limited | Leeds | - | - | 0.7km/275kV | `20355` | y |
| 1927 | 45.9 | 40 | solar | PRE_CONSENT | Snowswick Lane, Coleshill - Solar Farm | Abei Energy Limited | Vale of White Horse | - | - | 6.6km/400kV | `19568` | y |
| 1928 | 45.9 | 14 | solar | PAST_EXPECTED_START | Standingfauld Farm, Muthill - Solar Panels | Relay Standingfauld Limited | Perth and Kinross | 2022-11-08 | 1392 | 1.7km/400kV | `11900` | y |
| 1929 | 45.9 | 40 | solar | PAST_EXPECTED_START | South Antrim Solar Park - Phase 2 | Hadstone Energy | Antrim and Newtownabbey | 2016-04-25 | 3780 | 11.0km/275kV | `6829` | y |
| 1930 | 45.8 | 8 | solar | PRE_CONSENT | Cooles Farm, Minety - Solar Park/Battery Storage | Ecotricity Generation Limited | Wiltshire | - | - | 1.6km/400kV | `12218` | y |
| 1931 | 45.8 | 6 | solar | PAST_EXPECTED_START | Rawcliffe Estate, Bridge Lane - Solar Farm | East Riding of Yorkshire Council (... | East Riding of Yorkshire | 2024-12-06 | 633 | 5.6km/400kV | `17031` | y |
| 1932 | 45.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Dungannon Energy Storage System | Low Carbon Storage Ireland | Mid Ulster | - | - | 0.3km/275kV | `7050` | y |
| 1933 | 45.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Norwich Road Industrial Estate | Eelpower Limited | East Suffolk | 2021-03-26 | - | 0.2km/132kV | `12529` | y |
| 1934 | 45.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Eccles Substation, Eccles - Battery Energy Storage S... | Eccles Grid Stability Limited | Scottish Borders | 2023-06-15 | - | 0.4km/400kV | `13003` | y |
| 1935 | 45.8 | 50 | bess | PRE_CONSENT | Far Moor - Battery Energy Storage System | Greenfield Energy Developments Lim... | West Lancashire | - | - | 0.1km/132kV | `18717` | y |
| 1936 | 45.8 | 30 | bess | PRE_CONSENT | Gloucestershire Science and Technology Park | Ecotricity | Stroud | - | - | 0.6km/132kV | `10796` | y |
| 1937 | 45.8 | 30 | bess | PAST_EXPECTED_START | Meiklelaught Farm - Battery Storage | Green Power Consultants | North Ayrshire | 2023-12-13 | 992 | 1.2km/132kV | `14525` | y |
| 1938 | 45.8 | 30 | bess | PRE_CONSENT | Caswell Lane, Brize Norton - Solar Farm & Battery St... | Ampyr Solar Europe | West Oxfordshire | - | - | 3.8km/132kV | `16350` | y |
| 1939 | 45.8 | 30 | solar | PRE_CONSENT | Caswell Lane, Brize Norton - Solar Farm & Battery St... | Ampyr Solar Europe | West Oxfordshire | - | - | 3.8km/132kV | `16351` | y |
| 1940 | 45.8 | 30 | solar | PRE_CONSENT | Boscar Layby, Raskelf - Solar Panels | Sky UK Development Limited | North Yorkshire | - | - | 1.6km/132kV | `17595` | y |
| 1941 | 45.8 | 30 | solar | PRE_CONSENT | Market Weighton Road, Barlby - Solar Farm & Battery ... | Quintas Cleantech | North Yorkshire | - | - | 4.5km/400kV | `17894` | y |
| 1942 | 45.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Burwell Solar Farm | EDF Energy Renewables | East Cambridgeshire | 2020-11-19 | - | 0.6km/132kV | `7630` | y |
| 1943 | 45.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Crick Road | Lightrock Power / Bluefield Solar ... | West Northamptonshire | 2020-11-19 | - | 0.8km/132kV | `7954` | y |
| 1944 | 45.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Unit 5 XL Business Park | Amber Infrastructure Group | West Lancashire | 2017-12-18 | - | 0.4km/132kV | `7985` | y |
| 1945 | 45.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Fen Lane, Bulphan Solar Farm | DIF Capital Partners | Havering | 2021-07-30 | - | 0.4km/275kV | `8411` | y |
| 1946 | 45.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Whitehills Energy Storage Facility | Gigabox Developments Limited / Whi... | Angus | 2021-12-15 | - | 0.3km/132kV | `8916` | y |
| 1947 | 45.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Welkin Mill, Welkin Road - Battery Storage | Noriker Power Limited | Stockport | 2023-08-01 | - | 0.2km/275kV | `12982` | y |
| 1948 | 45.8 | 50 | solar | PRE_CONSENT | Bedford Solar, Northill Road - Solar Farm & Battery ... | QC Ubertino Limited | Bedford | - | - | 4.3km/132kV | `18336` | y |
| 1949 | 45.8 | 1 | solar | PAST_EXPECTED_START | Hall And Pickles, Wombourne - Solar Panels | Advanced Renewable Power Limited | South Staffordshire | 2025-06-09 | 448 | 0.5km/400kV | `18690` | y |
| 1950 | 45.8 | 30 | bess | PRE_CONSENT | Fordtown Energy Storage | Intelligent Land Investments (ILI) | Aberdeenshire | - | - | 0.3km/132kV | `7234` | **n** |
| 1951 | 45.8 | 1 | solar | PAST_EXPECTED_START | Folly Brook Road, Emersons Green - Solar Panels | JJ Foodservice Limited | South Gloucestershire | 2022-10-13 | 1418 | 1.6km/132kV | `12034` | y |
| 1952 | 45.8 | 1 | solar | PAST_EXPECTED_START | Paragon Works, Rising Bridge Road - Solar Farm | Locogen Limited | Rossendale | 2025-04-02 | 516 | 1.1km/132kV | `16024` | y |
| 1953 | 45.8 | 1 | solar | PAST_EXPECTED_START | Headways, Unit 3 - Solar Panels | Harvest Green Developments | Wakefield | 2024-10-21 | 679 | 0.5km/275kV | `17203` | y |
| 1954 | 45.8 | 1 | solar | PAST_EXPECTED_START | Martells Quarry, Slough Lane - Solar Array | Sewells Reservoir Construction Ltd | Tendring | 2025-12-17 | 257 | 1.4km/132kV | `19726` | y |
| 1955 | 45.8 | 2 | solar | PAST_EXPECTED_START | Meadowhead Sewage Treatment Plant, Meadowhead Road -... | Scottish Water | North Ayrshire | 2024-06-07 | 815 | 0.5km/132kV | `16385` | y |
| 1956 | 45.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Tollgate Farm Battery Storage | RNA Energy / Harmony Energy Storag... | Welwyn Hatfield | 2019-01-22 | - | 0.1km/132kV | `6949` | **n** |
| 1957 | 45.8 | 3 | solar | PAST_EXPECTED_START | Phoenix Healthcare Distribution Centre - Solar Panel... | Phoenix Medical Supplies | Wakefield | 2024-02-29 | 914 | 0.1km/400kV | `15806` | y |
| 1958 | 45.7 | 49 | bess | DESIGN_FROZEN_OR_LATER | Titchfield Lane | Balanced Grid Solutions | Winchester | 2020-08-20 | - | 0.6km/400kV | `7828` | y |
| 1959 | 45.7 | 63 | solar | PAST_EXPECTED_START | Benthead Farm - Solar Farm & Battery Storage | Locogen Limited | Scottish Government (S36) | 2023-08-11 | 1116 | 2.6km/132kV | `10542` | y |
| 1960 | 45.7 | 6 | solar | PRE_CONSENT | Seghill Household Waste Recovery Centre -Solar Panel... | Suez Recycling and Recovery UK Lim... | Northumberland | - | - | 0.3km/275kV | `19296` | y |
| 1961 | 45.7 | 6 | solar | PRE_CONSENT | Seghill Household Waste Recovery Centre - Solar Pane... | Suez Recycling and Recovery UK Lim... | Northumberland | - | - | 0.3km/275kV | `20273` | y |
| 1962 | 45.7 | 2 | solar | PAST_EXPECTED_START | Cranswick Country Foods | Cranswick Plc | Mid Suffolk | 2021-04-29 | 1950 | 1.1km/400kV | `8436` | y |
| 1963 | 45.7 | 2 | solar | PAST_EXPECTED_START | Central Avenue, Severn Beach - Solar Photovoltaic Pa... | Zestec Asset Management | South Gloucestershire | 2021-08-20 | 1837 | 0.7km/400kV | `9267` | y |
| 1964 | 45.7 | 2 | solar | PRE_CONSENT | Studley Grange Farm, Studley - Solar Farm | Studley Grange Garden & Leisure Pa... | Wiltshire | - | - | 0.7km/132kV | `19854` | y |
| 1965 | 45.6 | 10 | bess | PAST_EXPECTED_START | Manor Farm Energy Storage | Innova Renewables Limited | East Lindsey | 2017-11-30 | 3196 | 2.9km/132kV | `1694` | y |
| 1966 | 45.6 | 1 | solar | PAST_EXPECTED_START | Kestrel Way - Solar Panels | Digital Realty | Woking | 2024-03-06 | 908 | 4.5km/400kV | `15780` | y |
| 1967 | 45.6 | 1 | solar | PAST_EXPECTED_START | Huskisson Dock Building, Huskisson Dock - Solar PV A... | Eon UK Plc | Liverpool | 2024-03-08 | 906 | 2.8km/275kV | `15721` | y |
| 1968 | 45.6 | 13 | solar | PAST_EXPECTED_START | Malmesbury Road Solar Farm | Wessex Solar Energy Limited | Wiltshire | 2023-10-26 | 1040 | 6.3km/132kV | `10764` | y |
| 1969 | 45.6 | 13 | solar | PRE_CONSENT | Peel Road Phase 2 - Solar Farm | Energi Generation | Fylde | - | - | 0.2km/132kV | `13300` | y |
| 1970 | 45.6 | 8 | bess | PAST_EXPECTED_START | Cocker Avenue - Energy storage facility | AMP Energy Services Limited | Wyre | 2021-06-25 | 1893 | 2.2km/132kV | `9009` | y |
| 1971 | 45.6 | 3 | solar | PAST_EXPECTED_START | Tir John Solar Farm | Swansea City and County Council | Swansea | 2023-06-13 | 1175 | 0.4km/132kV | `10018` | y |
| 1972 | 45.5 | 28 | solar | PRE_CONSENT | Manor Farm, Sherborne - Solar Farm | Solar 2 Limited | Basingstoke and Deane | - | - | 2.3km/400kV | `10046` | y |
| 1973 | 45.5 | 1 | solar | PAST_EXPECTED_START | Dominos Pizza Uk & Ireland, Central Park - Solar PV ... | Dominos Pizza Group Limited (Head ... | South Gloucestershire | 2024-07-30 | 762 | 0.4km/132kV | `16589` | y |
| 1974 | 45.5 | 1 | solar | PAST_EXPECTED_START | The Hollies Solar Park - Skegness - extension | Spencer Farm Produce (Juwi Renewab... | East Lindsey | 2013-12-04 | 4653 | 1.0km/132kV | `C2106` | **n** |
| 1975 | 45.5 | 7 | solar | PAST_EXPECTED_START | Suggenhall Farm - Photovoltaic Solar Array & Battery... | RNA Energy Limited | Mid Suffolk | 2024-04-17 | 866 | 1.7km/132kV | `10165` | y |
| 1976 | 45.5 | 1 | solar | PAST_EXPECTED_START | Shed 10, Alexandra Road South, Immingham Docks - Sol... | Associated British Ports (Head Off... | North East Lincolnshire | 2023-09-11 | 1085 | 1.5km/132kV | `14563` | y |
| 1977 | 45.5 | 4 | solar | PAST_EXPECTED_START | Cuckmere Solar Farm | Susenco Management | Wealden | 2017-02-06 | 3493 | 0.6km/132kV | `5663` | y |
| 1978 | 45.5 | 27 | bess | PRE_CONSENT | Craig Watch - Wind Farm & Battery Storage | Craig Watch Wind Farm Limited | Scottish Government (S36) | - | - | 0.7km/132kV | `11608` | y |
| 1979 | 45.4 | 35 | solar | PAST_EXPECTED_START | Parc Solar Traffwll | Low Carbon | Welsh Government (NSIP) | 2023-03-17 | 1263 | 3.8km/132kV | `7471` | y |
| 1980 | 45.4 | 35 | solar | PRE_CONSENT | Stow Park Farm, Stow Park - Solar Panels | Luminous Energy Group | West Lindsey | - | - | 0.4km/132kV | `16594` | **n** |
| 1981 | 45.4 | 45 | bess | PRE_CONSENT | Bloch Wind Farm & Battery Storage (Solway Bank Exten... | Renewable Energy Systems (RES) | Scottish Government (S36) | - | - | 4.2km/132kV | `10999` | y |
| 1982 | 45.4 | 16 | solar | PRE_CONSENT | Calvert Landfill Site Solar Array | Infinis Solar Developments Limited | Buckinghamshire | - | - | 3.3km/132kV | `9642` | y |
| 1983 | 45.4 | 3 | solar | PAST_EXPECTED_START | Chesterford Park - Green Energy Hub | Chesterford Park (General Partner)... | Uttlesford | 2022-12-23 | 1347 | 0.6km/400kV | `8983` | y |
| 1984 | 45.4 | 7 | bess | PRE_CONSENT | Albrighton Substation, Beamish Lane - Battery Storag... | Fig Power | Shropshire | - | - | 1.7km/400kV | `15306` | y |
| 1985 | 45.4 | 7 | solar | PRE_CONSENT | Central Park - Solar Farm & Battery Storage | Severnside Distribution Lane Limit... | South Gloucestershire | - | - | 0.5km/400kV | `20362` | y |
| 1986 | 45.3 | 1 | solar | PAST_EXPECTED_START | Global Ardour Recycling Limited - Solar Panels | SNRG | Preston | 2025-03-18 | 531 | 4.1km/132kV | `18034` | y |
| 1987 | 45.3 | 5 | solar | PAST_EXPECTED_START | Aston Martin Lagonda, Banbury Road - Solar panels | Aston Martin Head Office | Stratford-on-Avon | 2024-10-10 | 690 | 5.0km/132kV | `16633` | **n** |
| 1988 | 45.3 | 1 | solar | PAST_EXPECTED_START | Pirelli Limited, Derby Road - Solar Panels | Pirelli Limited | East Staffordshire | 2024-04-05 | 878 | 1.1km/132kV | `16022` | y |
| 1989 | 45.3 | 12 | bess | PRE_CONSENT | Benridge Farm, Fillpoke Lane - Battery Energy Storag... | Development at Benridge Farm | County Durham | - | - | 3.5km/275kV | `18247` | y |
| 1990 | 45.3 | 12 | solar | PRE_CONSENT | Woodfold Lane, Brentingby - Solar Farm | Noventum Power Limited | Melton | - | - | 0.8km/132kV | `18338` | y |
| 1991 | 45.3 | 34 | bess | DESIGN_FROZEN_OR_LATER | Dounreay, Thurso - Battery Energy Storage | Ylem Energy Limited (Reay Power) | Highland | 2025-01-31 | - | 0.3km/275kV | `14233` | y |
| 1992 | 45.3 | 16 | bess | PAST_EXPECTED_START | Grassing Rome Street - Battery Storage | STOR 141 Limited | Cumberland | 2024-03-07 | 907 | 2.2km/132kV | `11611` | y |
| 1993 | 45.3 | 1 | solar | PAST_EXPECTED_START | Victory Park Way - Solar Panels | Gardner Aerospace | Derby | 2022-03-31 | 1614 | 0.9km/132kV | `10697` | y |
| 1994 | 45.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Mill Lane, Nursling - Battery Storage Facility | Gerard Hall Energy | Test Valley | 2020-05-13 | - | 0.2km/132kV | `8099` | y |
| 1995 | 45.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Standby Embedded Stor Power Plant - Battery storage | Green Frog Power 214 Limited | North Tyneside | 2021-06-16 | - | 0.0km/132kV | `9010` | y |
| 1996 | 45.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Chadderton - Battery energy storage facility | Field | Oldham | 2022-12-09 | - | 0.2km/132kV | `11160` | y |
| 1997 | 45.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Glasgow Airport Solar Farm | AGS Airports Limited | Renfrewshire | 2023-04-06 | - | 1.7km/132kV | `11096` | y |
| 1998 | 45.2 | 5 | bess | PRE_CONSENT | Cleator Energy Storage Facility Extension | Cleator Battery Storage Limited | Cumberland | - | - | 0.1km/132kV | `11945` | **n** |
| 1999 | 45.2 | 5 | solar | PRE_CONSENT | Castle Hills Solar Farm - BESS | Castle Hills Solar Farm Limited | Solihull | - | - | 1.4km/132kV | `19475` | y |
| 2000 | 45.2 | 1 | solar | PAST_EXPECTED_START | Exeter City Council - Solar Panel Array | Exeter City Council | Exeter | 2019-10-29 | 2498 | 0.1km/132kV | `7484` | y |
| 2001 | 45.2 | 1 | solar | PAST_EXPECTED_START | Gypsy Moth Avenue - Solar Array | Aberdeen Standard Investment | Welwyn Hatfield | 2022-08-25 | 1467 | 2.9km/132kV | `10943` | y |
| 2002 | 45.2 | 1 | bess | PAST_EXPECTED_START | Woodlands - Battery Energy Storage | Infinis Battery Storage Limited | Doncaster | 2022-07-11 | 1512 | 1.7km/275kV | `11585` | y |
| 2003 | 45.2 | 1 | solar | PAST_EXPECTED_START | Climax Molybdenum UK Limited, Needham Road - Solar P... | Climax Molybdenum UK Ltd | Mid Suffolk | 2024-05-01 | 852 | 0.8km/132kV | `15324` | y |
| 2004 | 45.1 | 15 | solar | PRE_CONSENT | Avenue Farm - Back Road Solar Farm | South Norfolk & Broadland | South Norfolk | - | - | 0.8km/132kV | `19124` | y |
| 2005 | 45.1 | 2 | solar | PRE_CONSENT | Grove Farm, Daventry Road - Solar Farm | Biffa Waste Services Limited | West Northamptonshire | - | - | 1.7km/132kV | `20446` | y |
| 2006 | 45.1 | 5 | solar | PRE_CONSENT | Manor Farm, Laddingford - Solar PV Panels | Aardvark EM Limited | Maidstone | - | - | 4.0km/132kV | `20083` | y |
| 2007 | 45.1 | 5 | solar | PRE_CONSENT | Manor Farm, Laddingford - Solar Farm | BOOM Developments Limited | Maidstone | - | - | 4.0km/132kV | `20808` | y |
| 2008 | 45.1 | 42 | solar | PRE_CONSENT | Harbour Farm - Solar Farm | Grupotec | East Riding of Yorkshire | - | - | 0.6km/132kV | `11386` | y |
| 2009 | 45.1 | 25 | solar | PRE_CONSENT | Little Heath Lane - Solar PV Array | Energi Generation | Dacorum | - | - | 0.5km/132kV | `11085` | y |
| 2010 | 45.0 | 2 | bess | PAST_EXPECTED_START | Chadderton - Battery Storage System | Zetex Plc | Oldham | 2022-05-05 | 1579 | 1.3km/132kV | `10849` | y |
| 2011 | 45.0 | 2 | solar | PAST_EXPECTED_START | Crossways Farm, Thurlton - Solar Farm | M Gaze & Co Limited | South Norfolk | 2022-10-28 | 1403 | 0.1km/132kV | `11285` | y |
| 2012 | 45.0 | 2 | bess | PAST_EXPECTED_START | Halfway House, Lincoln Hill - Energy Storage | Humshaugh Net Zero | Northumberland | 2023-07-14 | 1144 | 2.8km/275kV | `12840` | y |
| 2013 | 45.0 | 2 | solar | PAST_EXPECTED_START | Marston House, Otley Road - Solar Panels | Eden Sustainable Limited | Bradford | 2023-05-05 | 1214 | 0.3km/275kV | `13634` | y |
| 2014 | 45.0 | 68 | solar | DESIGN_FROZEN_OR_LATER | Tregonning Farm - Solar Farm & Battery Storage | European Energy | Cornwall | 2023-12-05 | - | 3.8km/132kV | `10801` | y |
| 2015 | 45.0 | 1 | solar | PAST_EXPECTED_START | Pilgrims Pride Limited, Newtons Margate Industrial E... | EDF Energy Renewables Limited | Cornwall | 2025-04-15 | 503 | 2.4km/132kV | `18001` | y |
| 2016 | 45.0 | 1 | solar | PAST_EXPECTED_START | Westexe, Greendale Business Park - Solar Panels | Olympus Power | East Devon | 2024-02-14 | 929 | 0.7km/132kV | `15592` | y |
| 2017 | 44.9 | 40 | bess | DESIGN_FROZEN_OR_LATER | Land off Queenborough Road | UK Power Reserve | Swale | 2017-10-12 | - | 0.8km/132kV | `7003` | y |
| 2018 | 44.9 | 40 | bess | PRE_CONSENT | Breezy Hill, North Kyle Forest Estate - BESS | Brockwell Energy Limited | East Ayrshire | - | - | 1.3km/132kV | `16796` | y |
| 2019 | 44.9 | 1 | solar | PAST_EXPECTED_START | Shed 27, Alexandra Road, South Immingham - Solar Pho... | Associated British Ports (Head Off... | North East Lincolnshire | 2023-09-11 | 1085 | 1.5km/132kV | `14562` | y |
| 2020 | 44.9 | 1 | solar | PAST_EXPECTED_START | Belle Vue Road - Solar Array | University of Exeter | Exeter | 2023-08-01 | 1126 | 0.9km/400kV | `13468` | y |
| 2021 | 44.9 | 2 | solar | PAST_EXPECTED_START | Uphouse Farm - Sandpits Solar Farm & Battery Energy ... | Uphouse Farms Limited | North Norfolk | 2025-06-16 | 441 | 1.6km/132kV | `18193` | y |
| 2022 | 44.9 | 1 | solar | PAST_EXPECTED_START | Leek Road - Solar PV array | Goodwin Plc | Stoke-on-Trent | 2022-01-27 | 1677 | 0.5km/132kV | `10059` | y |
| 2023 | 44.9 | 11 | solar | PAST_EXPECTED_START | Gaywood Solar Farm | KYBO Solar Limited | Tandridge | 2024-01-18 | 956 | 8.3km/132kV | `13645` | y |
| 2024 | 44.9 | 109 | bess | PRE_CONSENT | Cnoc Buidhe Windfarm | Belltown Power Limited | Scottish Government (S36) | - | - | 19.6km/132kV | `13569` | y |
| 2025 | 44.9 | 1 | solar | PAST_EXPECTED_START | The Bungalow, Kus Industrial Estate - Solar Photovol... | Boardlink Limited | Flintshire | 2022-12-02 | 1368 | 2.5km/132kV | `12362` | y |
| 2026 | 44.9 | 1 | solar | PAST_EXPECTED_START | Safran Nacelles, Bancroft Road - Solar Panels | EDF Energy Renewables Limited | Burnley | 2024-04-30 | 853 | 0.6km/132kV | `14339` | y |
| 2027 | 44.8 | 18 | bess | PRE_CONSENT | Salters Lane - Solar Panels | Grupotec Solar Uk 9 Limited | Durham | - | - | 0.5km/275kV | `18563` | y |
| 2028 | 44.8 | 6 | bess | PAST_EXPECTED_START | Craignathro Farm - Solar Array | Craignathro Farms Limited | Angus | 2023-08-17 | 1110 | 0.6km/132kV | `10962` | y |
| 2029 | 44.8 | 6 | solar | PAST_EXPECTED_START | Aston Martin Lagonda, Llanmaes - Solar Pv Panels | Aston Martin Lagonda | Vale of Glamorgan | 2024-02-06 | 937 | 2.3km/275kV | `14735` | y |
| 2030 | 44.8 | 6 | solar | PRE_CONSENT | Crockwell Hill - Solar Farm | PS Renewables Limited | West Northamptonshire | - | - | 0.4km/132kV | `17286` | y |
| 2031 | 44.8 | 10 | solar | PAST_EXPECTED_START | Goosey Lodge - Solar Farm | Wykes Engineering Limited Goosey L... | Bedford | 2023-05-25 | 1194 | 6.1km/132kV | `11923` | y |
| 2032 | 44.8 | 50 | solar | PRE_CONSENT | Kells Solar Farm | Elgin Energy EsCo | Antrim and Newtownabbey | - | - | 1.0km/275kV | `5967` | **n** |
| 2033 | 44.8 | 50 | bess | PAST_EXPECTED_START | Clash Gour | EDF Energy Renewables/ Force 9 | Scottish Government (S36) | 2022-10-21 | 1410 | 4.4km/275kV | `6372` | y |
| 2034 | 44.8 | 50 | bess | PRE_CONSENT | Longcroft Wind Farm | Renewable Energy Systems | Scottish Government (S36) | - | - | 1.3km/400kV | `13538` | y |
| 2035 | 44.8 | 50 | bess | PRE_CONSENT | Lynemore Wind Farm | Galileo Empower UK Limited | Scottish Government (S36) | - | - | 3.6km/132kV | `16397` | y |
| 2036 | 44.8 | 30 | solar | PRE_CONSENT | New Works Lane - Solar Farm | Greentech | Telford and Wrekin | - | - | 0.7km/132kV | `9381` | y |
| 2037 | 44.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Colton - Solar photovoltaic farm, Battery storage | Pathfinder Clean Energy UK Dev Lim... | South Norfolk | 2022-06-30 | - | 1.5km/400kV | `10944` | y |
| 2038 | 44.8 | 30 | bess | DESIGN_FROZEN_OR_LATER | Colton - Solar photovoltaic farm, Battery storage | Pathfinder Clean Energy UK Dev Lim... | South Norfolk | 2022-06-30 | - | 1.5km/400kV | `10945` | y |
| 2039 | 44.8 | 30 | bess | PRE_CONSENT | Highland Wind Farm - Battery Storage | Highland Wind Farm Limited | Scottish Government (S36) | - | - | 3.4km/132kV | `16176` | y |
| 2040 | 44.8 | 50 | solar | PRE_CONSENT | Worlds End Solar Farm | British Solar Renewables | Stroud | - | - | 0.1km/132kV | `9053` | y |
| 2041 | 44.8 | 50 | solar | PRE_CONSENT | East Stour Solar Farm | EDF Energy Renewables | Ashford | - | - | 0.2km/132kV | `9402` | y |
| 2042 | 44.8 | 50 | solar | PAST_EXPECTED_START | New Road Solar Farm | Low Carbon UK Solar Investment Co ... | East Suffolk | 2021-10-13 | 1783 | 3.1km/132kV | `9625` | y |
| 2043 | 44.8 | 50 | solar | PRE_CONSENT | Charley Road - Solar Farm | Namene Solar | North West Leicestershire | - | - | 0.8km/132kV | `11736` | y |
| 2044 | 44.8 | 50 | solar | PRE_CONSENT | Bonnyknox Solar Farm | Renewable Energy Systems (RES) | Angus | - | - | 0.7km/132kV | `16666` | y |
| 2045 | 44.8 | 50 | solar | PRE_CONSENT | The Park Farm, Birds Corner - Battery Energy Storage | Regener8 Power Limited | Breckland | - | - | 2.8km/400kV | `17792` | y |
| 2046 | 44.8 | 50 | solar | PRE_CONSENT | Dykewood Farm, Water End Lane - Solar Panels | Regener8 Power Limited | Breckland | - | - | 2.1km/132kV | `18422` | y |
| 2047 | 44.8 | 50 | solar | PRE_CONSENT | Semere Lane, Dickleburgh - Solar Farm | Regener8 Power Limited | South Norfolk | - | - | 2.5km/400kV | `18423` | y |
| 2048 | 44.8 | 50 | solar | PRE_CONSENT | West Springfield Solar Farm - Solar Panels & BESS | BLC Energy | Scottish Government (S36) | - | - | 3.1km/132kV | `18945` | y |
| 2049 | 44.8 | 2 | solar | PAST_EXPECTED_START | Toronto Way, New Rossington Solar Panels | Sonne Solar Limited | Doncaster | 2021-04-08 | 1971 | 0.6km/400kV | `8444` | y |
| 2050 | 44.8 | 50 | solar | PRE_CONSENT | Milton Road, Gayton - Solar Farm | Anesco Limited | West Northamptonshire | - | - | 4.1km/400kV | `19423` | y |
| 2051 | 44.8 | 1 | bess | PAST_EXPECTED_START | Hazlehead Wind Farm Battery | Banks Renewables | Barnsley | 2020-06-10 | 2273 | 1.4km/400kV | `3937` | y |
| 2052 | 44.8 | 1 | solar | PAST_EXPECTED_START | Riverside Energy Park (REP) | Cory Riverside Energy | The Planning Inspectorate - ... | 2020-04-09 | 2335 | 1.9km/400kV | `7036` | y |
| 2053 | 44.8 | 1 | bess | PAST_EXPECTED_START | Council Green Waste Facility | Exeter City Council | Exeter | 2019-10-29 | 2498 | 0.1km/132kV | `7484` | y |
| 2054 | 44.8 | 1 | solar | PAST_EXPECTED_START | Bowman Stores Marsh Road | Bowman Stores | South Holland | 2020-09-01 | 2190 | 0.6km/400kV | `8054` | y |
| 2055 | 44.8 | 1 | solar | PAST_EXPECTED_START | Ford Motor Company Limited - Solar Farm | Onsite Energy Projects Limited | West Northamptonshire | 2021-11-18 | 1747 | 2.4km/132kV | `9566` | y |
| 2056 | 44.8 | 1 | solar | PAST_EXPECTED_START | Downs Road, Curbridge Business Park - Solar Panels | Stewart Milne Timber Systems Limit... | West Oxfordshire | 2021-12-01 | 1734 | 3.5km/132kV | `9822` | y |
| 2057 | 44.8 | 1 | solar | PAST_EXPECTED_START | Tamerton Road, Roborough - Solar Panels | Plessey Semi Conductors Limited | South Hams | 2022-04-06 | 1608 | 0.5km/400kV | `10782` | y |
| 2058 | 44.8 | 1 | solar | PAST_EXPECTED_START | City Road - Solar panel | Belong Construction Limited | Cheshire West and Chester | 2022-07-20 | 1503 | 1.6km/132kV | `11566` | y |
| 2059 | 44.8 | 1 | bess | PAST_EXPECTED_START | Biffa Electricity Generating Compound, Burtonhead Ro... | Biffa Waste Services Limited | St. Helens | 2022-10-18 | 1413 | 2.4km/132kV | `11906` | y |
| 2060 | 44.8 | 1 | solar | PAST_EXPECTED_START | Daisy Cottage, Ty-Canol Road - Solar Panels | Private Developer | Monmouthshire | 2022-10-27 | 1404 | 1.0km/400kV | `12110` | y |
| 2061 | 44.8 | 1 | solar | PAST_EXPECTED_START | Tecan Way, Granby Industrial Estate - Solar Photo Vo... | P L Cane Investments Limited | Dorset | 2023-06-09 | 1179 | 1.3km/400kV | `13800` | y |
| 2062 | 44.8 | 1 | solar | PAST_EXPECTED_START | Rehau Plastics, Pencefn Road - Solar Panels | Blaenau Plastics Ltd | Gwynedd | 2024-03-21 | 893 | 1.3km/275kV | `15854` | y |
| 2063 | 44.8 | 10 | solar | PAST_EXPECTED_START | Gooseys Lodge, Wymington Lane - Solar Farm | Wykes Engineering Limited Goosey L... | Bedford | 2024-05-02 | 851 | 6.0km/132kV | `15707` | y |
| 2064 | 44.7 | 49 | solar | PRE_CONSENT | Yew Tree Farm, Drointon Lane | Push Energy | Stafford | - | - | 0.6km/132kV | `14168` | y |
| 2065 | 44.7 | 2 | solar | PAST_EXPECTED_START | Poundland Distribution Centre,Three Sisters Road - S... | Standard Life Assurance Limited | Wigan | 2022-09-26 | 1435 | 1.3km/132kV | `11888` | y |
| 2066 | 44.7 | 80 | bess | DESIGN_FROZEN_OR_LATER | Trondheim Way Battery energy storage | Vox Burns Limited | North East Lincolnshire | 2023-01-23 | - | 0.0km/132kV | `8455` | y |
| 2067 | 44.7 | 80 | bess | PRE_CONSENT | Bowshiel Farm - Battery Energy Storage | Voltalia UK | Scottish Government (S36) | - | - | 2.2km/400kV | `17779` | y |
| 2068 | 44.6 | 10 | bess | PAST_EXPECTED_START | Stockbridge Road | Winchester Power | Winchester | 2017-12-14 | 3182 | 5.4km/132kV | `7097` | y |
| 2069 | 44.6 | 10 | bess | PRE_CONSENT | Sutton-on-the-Forest, Brownmoor Lane -BESS | Ampyr Energy UK Development Limite... | York | - | - | 0.3km/400kV | `19658` | y |
| 2070 | 44.6 | 6 | solar | PAST_EXPECTED_START | Babcock Marine Bldg, Wood Road - Solar Photovoltaic ... | Babcock Marine | Fife | 2023-12-08 | 997 | 3.5km/132kV | `13382` | y |
| 2071 | 44.6 | 3 | bess | PAST_EXPECTED_START | Wittering Ford Road | Solar Charging (Lark Energy) | Peterborough | 2019-11-13 | 2483 | 4.2km/132kV | `4956` | **n** |
| 2072 | 44.6 | 3 | bess | PAST_EXPECTED_START | Capon Tree Road - Battery Energy Storage | Prime Energy Limited | Cumberland | 2024-06-19 | 803 | 0.8km/275kV | `16377` | y |
| 2073 | 44.5 | 3 | solar | PAST_EXPECTED_START | Howdens Joinery, Thorpe Road - Solar Panels | Howden Joinery Properties Limited | East Riding of Yorkshire | 2024-03-06 | 908 | 4.4km/400kV | `15817` | y |
| 2074 | 44.5 | 5 | solar | PRE_CONSENT | Western Court, Bishops Sutton Road - Solar Farm | ILOS Energy UK Limited | Winchester | - | - | 2.0km/132kV | `20875` | y |
| 2075 | 44.4 | 2 | solar | PAST_EXPECTED_START | Dykes Of Gray Road - Solar PV Array | Dundee Renewable Energy Society | Dundee City | 2022-03-16 | 1629 | 0.8km/132kV | `9650` | y |
| 2076 | 44.4 | 75 | solar | PRE_CONSENT | Rush Wall Solar Park | Rush Wall Solar Park | Welsh Government (NSIP) | - | - | 1.2km/275kV | `7194` | **n** |
| 2077 | 44.4 | 27 | solar | DISTRESSED | Harborough Fields Farm | Warwickshire Solar 1 | Rugby | 2021-03-29 | - | 0.8km/132kV | `7897` | **n** |
| 2078 | 44.4 | 45 | bess | PAST_EXPECTED_START | A981 Fraserburgh - Battery Energy Storage | Fraserburgh Energy Limited | Aberdeenshire | 2023-04-13 | 1236 | 3.3km/132kV | `12711` | y |
| 2079 | 44.4 | 35 | solar | DESIGN_FROZEN_OR_LATER | Eastfields Farm, Deppers Bridge - Solar Farm | Vantage RE | Stratford-on-Avon | 2021-08-26 | - | 0.5km/132kV | `9701` | y |
| 2080 | 44.3 | 9 | solar | PAST_EXPECTED_START | Coast Viners Animal Nutrition, Drumlithie - Solar Ar... | East Coast Viners Renewables Limit... | Aberdeenshire | 2023-02-10 | 1298 | 1.5km/275kV | `11977` | y |
| 2081 | 44.3 | 12 | bess | DESIGN_FROZEN_OR_LATER | Rock Farm - Solar Farm | Enviromena | Shropshire | 2023-09-25 | - | 1.4km/132kV | `15248` | y |
| 2082 | 44.3 | 12 | bess | PRE_CONSENT | Stor Generation Plant - Battery Storage | Green Frog Power 214 Limited | Bradford | 2021-06-11 | - | 0.0km/132kV | `18096` | y |
| 2083 | 44.3 | 3 | solar | PAST_EXPECTED_START | Sherwood Way South | Zestec Asset Management | Ashfield | 2021-09-14 | 1812 | 3.5km/132kV | `9657` | y |
| 2084 | 44.3 | 3 | solar | PAST_EXPECTED_START | Brokenbury Farm, Galmpton - Solar Farm | Torbay Development Agency | Torbay | 2022-11-18 | 1382 | 3.7km/132kV | `9181` | y |
| 2085 | 44.3 | 9 | bess | PRE_CONSENT | Leyden Road - Battery Energy Storage | Trio Power Limited | West Lothian | - | - | 0.3km/275kV | `19085` | y |
| 2086 | 44.2 | 20 | bess | PAST_EXPECTED_START | Perserverance Road | Noriker Power | Herefordshire, County of | 2020-11-13 | 2117 | 6.2km/132kV | `7061` | **n** |
| 2087 | 44.2 | 20 | bess | PRE_CONSENT | Fordtown Energy Storage | Shires Hamilton | Aberdeenshire | - | - | 0.3km/132kV | `7764` | **n** |
| 2088 | 44.2 | 20 | solar | PAST_EXPECTED_START | Primrose Hall Solar Farm | Low Carbon Limited | Tendring | 2021-03-19 | 1991 | 5.4km/132kV | `8020` | y |
| 2089 | 44.2 | 20 | solar | PRE_CONSENT | Little Flanchford Farm, Flanchford Road - Solar Ener... | Ilos Little Flanchford Limited | Mole Valley | - | - | 2.1km/132kV | `16004` | y |
| 2090 | 44.2 | 20 | bess | PRE_CONSENT | Willowfields Energy Park, Marcham - Battery Energy S... | Exagen Development Limited | Vale of White Horse | - | - | 2.6km/132kV | `16903` | y |
| 2091 | 44.2 | 20 | bess | PAST_EXPECTED_START | North West Of Jameston Farm | Private Developer | North Ayrshire | 2021-09-21 | 1805 | 2.7km/132kV | `7133` | y |
| 2092 | 44.2 | 20 | bess | PAST_EXPECTED_START | Tofts - Battery Storage | Telford Three Limited | North Ayrshire | 2023-09-14 | 1082 | 1.9km/400kV | `14706` | y |
| 2093 | 44.2 | 3 | solar | PAST_EXPECTED_START | Roborough Solar Farm | Regener8 Power (Plymouth) | Plymouth | 2023-03-03 | 1277 | 0.6km/400kV | `12848` | y |
| 2094 | 44.2 | 3 | solar | PAST_EXPECTED_START | Roborough Solar Farm | Regener8 Power (South Hampshire) | Plymouth | 2023-03-09 | 1271 | 0.7km/400kV | `12924` | y |
| 2095 | 44.2 | 5 | solar | PAST_EXPECTED_START | Field 730M West Of Queen Street | Howmuir Solar | Angus | 2015-12-03 | 3924 | 0.4km/275kV | `5655` | y |
| 2096 | 44.2 | 5 | solar | PRE_CONSENT | South of Johnson's Lane | SBC Renewables | Knowsley | - | - | 0.9km/132kV | `5932` | **n** |
| 2097 | 44.2 | 5 | bess | PRE_CONSENT | Letchworth Power Energy Storage Facility | AMP Energy Services Limited | North Hertfordshire | - | - | 0.9km/400kV | `15927` | y |
| 2098 | 44.2 | 5 | bess | PRE_CONSENT | Coille Linne Wind Farm - Battery Energy Storage | Energiekontor (UK) Limited | Scottish Government (S36) | - | - | 0.8km/132kV | `16937` | y |
| 2099 | 44.2 | 5 | bess | PRE_CONSENT | Ballach Wind Farm | Energiekontor (UK) Limited | Scottish Government (S36) | - | - | 0.3km/132kV | `17147` | y |
| 2100 | 44.2 | 12 | solar | PRE_CONSENT | Barvills Solar Farm | Barvills Solar Limited (BE Renewab... | Thurrock | - | - | 1.2km/132kV | `5942` | y |
| 2101 | 44.2 | 9 | solar | PRE_CONSENT | Aggreko, Stirling Road - Solar Panels | Aggreko | West Dunbartonshire | - | - | 0.2km/132kV | `12009` | y |
| 2102 | 44.1 | 15 | solar | PRE_CONSENT | Eagland Hill - Solar Array | European Energy Photovoltaics Limi... | Wyre | - | - | 1.2km/400kV | `13983` | y |
| 2103 | 44.1 | 15 | solar | PRE_CONSENT | Bengrove Farm, Base Lane - Solar Farm | Sonnedix Bengrove Limited | Tewkesbury | - | - | 1.0km/132kV | `15882` | y |
| 2104 | 44.1 | 25 | bess | PRE_CONSENT | Snowswick Lane, Coleshill - Solar Farm | Abei Energy Limited | Vale of White Horse | - | - | 6.6km/400kV | `10757` | y |
| 2105 | 44.1 | 2 | solar | PAST_EXPECTED_START | Lockheed Road, Burtonwood & Westbrook - Solar panels | Brakes Group | Warrington | 2023-08-17 | 1110 | 0.3km/132kV | `14119` | y |
| 2106 | 44.1 | 32 | solar | DESIGN_FROZEN_OR_LATER | Aurora Solar Farm | Low Carbon UK Solar Investment Com... | West Oxfordshire | 2020-02-10 | - | 1.5km/132kV | `7385` | y |
| 2107 | 44.1 | 32 | solar | DESIGN_FROZEN_OR_LATER | Eastgate House Farm, Seamer - Solar Farm | Voltalia UK | North Yorkshire | 2022-10-07 | - | 0.6km/132kV | `9542` | y |
| 2108 | 44.1 | 53 | bess | PRE_CONSENT | Mid Hill Wind Farm | Invenergy Services UK | Scottish Government (S36) | - | - | 3.5km/132kV | `17153` | y |
| 2109 | 44.0 | 4 | solar | PAST_EXPECTED_START | Unilever UK, Corinium Avenue - Solar Panels | Unilever UK | Gloucester | 2024-05-22 | 831 | 0.6km/400kV | `16178` | y |
| 2110 | 44.0 | 4 | solar | PAST_EXPECTED_START | Solar Farm Development in Ballymena | Brooklands Altnagelvin No2 Limited | Mid and East Antrim | 2025-04-14 | 504 | 8.1km/275kV | `18060` | y |
| 2111 | 44.0 | 19 | solar | PRE_CONSENT | Fitcher Brook Solar Farm | Tyler Hill Renewables Limited | Malvern Hills | - | - | 0.9km/132kV | `14037` | y |
| 2112 | 44.0 | 5 | bess | PRE_CONSENT | Woodcock Solar Farm, Sweeming Lane - Battery Energy ... | AEUK Solar Project IX | North Yorkshire | - | - | 4.7km/132kV | `16639` | **n** |
| 2113 | 44.0 | 11 | solar | PAST_EXPECTED_START | Ferry Farm - Solar array | BNRG & Lanlink Estates Limited | Chichester | 2021-11-05 | 1760 | 16.4km/132kV | `8498` | y |
| 2114 | 43.9 | 40 | solar | PRE_CONSENT | Yardley Road Solar Farm | Solar 2 Limited | West Northamptonshire | - | - | 4.1km/400kV | `10009` | y |
| 2115 | 43.9 | 40 | solar | PRE_CONSENT | Chediston Hall - 40MW Solar Panels | Sky UK Development Limited | East Suffolk | - | - | 2.4km/132kV | `19230` | y |
| 2116 | 43.9 | 2 | solar | PAST_EXPECTED_START | Finlay Beverages, Elmsall Way - Solar Panels | Olympus Power | Wakefield | 2024-08-09 | 752 | 1.1km/400kV | `16564` | y |
| 2117 | 43.9 | 2 | solar | PAST_EXPECTED_START | Guilford Europe, Cotes Park Lane - Solar Panels | Alight AB | Amber Valley | 2023-04-04 | 1245 | 2.7km/132kV | `13070` | y |
| 2118 | 43.8 | 2 | solar | PAST_EXPECTED_START | Oakley Primary Academy, Station Road - Solar Panels ... | Cambridge Meridian Academies Trust | Bedford | 2023-02-22 | 1286 | 0.8km/132kV | `12231` | y |
| 2119 | 43.8 | 2 | solar | PAST_EXPECTED_START | Delphi Diesel Systems, Brunel Way - Solar Panels | Phinia Delphi UK Limited | Stroud | 2024-05-24 | 829 | 1.9km/132kV | `16257` | y |
| 2120 | 43.8 | 50 | bess | PRE_CONSENT | Watchman Energy Park | Renewco Power | Scottish Government (S36) | - | - | 8.2km/275kV | `17558` | y |
| 2121 | 43.8 | 30 | solar | PRE_CONSENT | Stell Solar Farm | Enviromena | North Yorkshire | - | - | 6.0km/132kV | `18911` | y |
| 2122 | 43.8 | 50 | bess | DISTRESSED | Lackenby | EDF Energy Renewables | Redcar and Cleveland | 2019-10-24 | - | 0.2km/400kV | `7040` | **n** |
| 2123 | 43.8 | 50 | bess | DISTRESSED | Grendon Storage | Statera Energy / Grendon Storage | North Northamptonshire | 2017-11-20 | - | 0.4km/132kV | `7089` | **n** |
| 2124 | 43.8 | 50 | bess | DISTRESSED | Taunton Substation | Pivot Power | Somerset | 2018-09-18 | - | 0.1km/400kV | `7153` | **n** |
| 2125 | 43.8 | 50 | bess | DISTRESSED | Harker Grid Sub Station | Pivot Power | Cumberland | 2019-07-10 | - | 0.0km/275kV | `7462` | **n** |
| 2126 | 43.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Bulphan Fen Solar Farm & Battery Storage | Warley Green Limited | Thurrock | 2021-10-21 | - | 1.2km/275kV | `8027` | y |
| 2127 | 43.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Bunkers Hill Farm - Solar farm & Battery stations | Vantage RE | Hart | 2021-11-11 | - | 0.5km/400kV | `8150` | y |
| 2128 | 43.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Leigh Delamere - Solar farm & Battery storage | Eden Renewables | Wiltshire | 2022-08-11 | - | 2.4km/400kV | `9238` | y |
| 2129 | 43.8 | 50 | solar | PRE_CONSENT | Lullington Solar Park | Lullington Solar Park Limited | South Derbyshire | - | - | 2.8km/132kV | `18812` | y |
| 2130 | 43.8 | 30 | solar | PAST_EXPECTED_START | Duddingston Solar Farm and Battery Storage | Aithrie Net Zero Solar Limited | West Lothian | 2024-04-03 | 880 | 7.1km/132kV | `11383` | y |
| 2131 | 43.8 | 1 | solar | PAST_EXPECTED_START | Tuesley Farm, Tuesley Lane - Solar Array | Hall Hunter Partnership | Waverley | 2023-11-29 | 1006 | 9.7km/132kV | `14628` | y |
| 2132 | 43.8 | 136 | bess | PRE_CONSENT | Newlands Hill Wind Energy Hub | Belltown Power Limited | Scottish Government (S36) | - | - | 2.1km/400kV | `12289` | y |
| 2133 | 43.8 | 3 | solar | PAST_EXPECTED_START | Bibsworth Lane, Willersey - Solar Farm | Farncombe Estates Holding Limited | Wychavon | 2025-05-19 | 469 | 9.4km/400kV | `15917` | y |
| 2134 | 43.7 | 4 | solar | PRE_CONSENT | Broad Path - Solar Panels | Valencia Energy Limited | Mid Devon | - | - | 1.9km/400kV | `18068` | y |
| 2135 | 43.6 | 10 | solar | PRE_CONSENT | Brook Hall Farm | South West Solar Parks (Brook Hall... | Wiltshire | - | - | 0.4km/400kV | `5926` | y |
| 2136 | 43.6 | 10 | solar | PRE_CONSENT | Littleton Green - Energy Park | Arnold White Estates Limited | Buckinghamshire | - | - | 3.6km/400kV | `14258` | y |
| 2137 | 43.6 | 10 | bess | PAST_EXPECTED_START | Bath Mews, Minsterley - Battery Storage Facility | Fig Power | Shropshire | 2024-07-26 | 766 | 12.7km/132kV | `16074` | y |
| 2138 | 43.6 | 48 | bess | DESIGN_FROZEN_OR_LATER | Tregonning Farm - Solar Farm & Battery Storage | European Energy | Cornwall | 2023-12-05 | - | 3.8km/132kV | `10800` | y |
| 2139 | 43.6 | 10 | solar | PAST_EXPECTED_START | Whitestones, Cuminestown - Solar Farm | Locogen Limited | Aberdeenshire | 2025-07-22 | 405 | 5.9km/400kV | `17707` | y |
| 2140 | 43.6 | 3 | bess | PAST_EXPECTED_START | Holiday Moss Landfill Site, Reeds Brow - Battery Sto... | Biffa Waste Services Limited | St. Helens | 2022-11-17 | 1383 | 0.5km/132kV | `12114` | y |
| 2141 | 43.5 | 2 | solar | PAST_EXPECTED_START | Fairy Hill, Compton Dando - Solar Farm | Environmental Gain Limited / Bath ... | Bath and North East Somerset | 2025-07-29 | 398 | 5.0km/132kV | `11606` | y |
| 2142 | 43.5 | 3 | solar | PRE_CONSENT | Kingsbury Pallets, Rush Lane - Solar Panels | Kingsbury Pallets Limited | North Warwickshire | - | - | 0.7km/132kV | `20804` | y |
| 2143 | 43.5 | 1 | solar | PAST_EXPECTED_START | Mylord Crescent, Camperdown Industrial Estate, Unit ... | Entek International Limited | North Tyneside | 2025-04-16 | 502 | 2.8km/275kV | `18316` | y |
| 2144 | 43.5 | 1 | solar | PAST_EXPECTED_START | CooperVision, Ensign Way - Solar Panels | Ylem Energy Limited | Eastleigh | 2024-09-17 | 713 | 2.9km/132kV | `16911` | y |
| 2145 | 43.5 | 4 | solar | PRE_CONSENT | Gwenlais Uchaf Farm | Renewable Developments | Swansea | - | - | 0.8km/400kV | `12809` | **n** |
| 2146 | 43.5 | 4 | solar | PAST_EXPECTED_START | Burrow Beck - Solar farm | Lancaster City Council | Lancaster | 2025-01-09 | 599 | 0.2km/400kV | `13806` | y |
| 2147 | 43.5 | 4 | solar | PAST_EXPECTED_START | Pirnhall Services, Bannockburn Interchange - Solar P... | Moto Hospitality Limited (Head Off... | Stirling | 2025-05-20 | 468 | 3.6km/400kV | `15251` | y |
| 2148 | 43.4 | 21 | solar | PAST_EXPECTED_START | Sedgeford Hall Estate - Solar Panels & Battery Stora... | Regener8 Power | King's Lynn and West Norfolk | 2023-08-23 | 1104 | 15.5km/132kV | `11206` | y |
| 2149 | 43.4 | 16 | solar | PRE_CONSENT | Moto Hospitality, Trowell Services Area North - Sola... | Moto Hospitality Limited | Broxtowe | - | - | 3.4km/132kV | `18604` | y |
| 2150 | 43.4 | 35 | bess | PRE_CONSENT | Rusholme Grange | Green Hedge Energy | North Yorkshire | - | - | 1.6km/400kV | `9121` | y |
| 2151 | 43.4 | 35 | bess | PRE_CONSENT | West Springfield Solar Farm - Solar Panels & BESS | BLC Energy | Scottish Government (S36) | - | - | 3.1km/132kV | `18944` | y |
| 2152 | 43.4 | 1 | solar | PAST_EXPECTED_START | Apetito, Canal Road - Solar Panels | Apetito UK Limited | Wiltshire | 2024-09-12 | 718 | 2.2km/132kV | `16818` | y |
| 2153 | 43.4 | 16 | solar | PRE_CONSENT | St Mary in the Marsh - Solar Panels | Enviromena | Folkestone and Hythe | - | - | 1.8km/400kV | `17767` | y |
| 2154 | 43.4 | 4 | solar | PAST_EXPECTED_START | NCL1, Follingsby Lane - Solar Panels | Zestec Asset Management | Gateshead | 2023-04-20 | 1229 | 2.0km/275kV | `13317` | y |
| 2155 | 43.3 | 1 | solar | PAST_EXPECTED_START | Lindrick Way, Barlborough - Solar Panels | Coster Special Technology | Bolsover | 2024-02-28 | 915 | 1.6km/132kV | `15776` | y |
| 2156 | 43.3 | 1 | solar | PAST_EXPECTED_START | Huntapac Produce Limited, Blackgate Lane - Solar Pho... | Huntapac Produce Limited | West Lancashire | 2023-02-10 | 1298 | 1.8km/132kV | `12989` | y |
| 2157 | 43.3 | 12 | solar | PAST_EXPECTED_START | Fawsley Estate, Fawsley - Solar Arrays | Elgin Energy EsCo | West Northamptonshire | 2024-01-24 | 950 | 6.3km/132kV | `12700` | y |
| 2158 | 43.3 | 1 | solar | PAST_EXPECTED_START | Berllandeg Farm, Rhoswiel - Solar Panels | Igreen Energy | Shropshire | 2025-06-18 | 439 | 0.9km/132kV | `16552` | **n** |
| 2159 | 43.3 | 1 | solar | PAST_EXPECTED_START | Bericap, Oslo Road - Solar Panels | Bericap UK Limited | Kingston upon Hull, City of | 2022-10-07 | 1424 | 0.4km/132kV | `11959` | y |
| 2160 | 43.2 | 20 | solar | PAST_EXPECTED_START | Bryn Henllys | Lightsource BP | Powys | 2018-06-11 | 3003 | 3.9km/132kV | `4775` | y |
| 2161 | 43.2 | 20 | bess | DISTRESSED | Petre Street | Renewable Energy Systems (RES) | Sheffield | 2017-11-24 | - | 0.1km/275kV | `6887` | **n** |
| 2162 | 43.2 | 20 | bess | DISTRESSED | Land To The East Of Wholeflats Road (Grangemouth) | Enstor (formerly CJ Energy) | Falkirk | - | - | 0.3km/275kV | `7043` | **n** |
| 2163 | 43.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | South Fambridge Hall - Solar farm & Battery storage | British Solar Renewables / BayWa r... | Rochford | 2021-12-15 | - | 0.7km/132kV | `9273` | y |
| 2164 | 43.2 | 2 | solar | PAST_EXPECTED_START | The Gaer - Solar Array | D & S Gethin | Powys | 2024-03-08 | 906 | 1.0km/132kV | `14605` | y |
| 2165 | 43.2 | 5 | solar | PRE_CONSENT | RAF Lossiemouth - Solar Panels | Cogeo Planning & Environmental Ser... | Moray | - | - | 5.0km/132kV | `20096` | y |
| 2166 | 43.2 | 1 | solar | PRE_CONSENT | Data Centre, Dennison House, Stanhope Road - Solar P... | Electron Green | Surrey Heath | - | - | 0.8km/132kV | `17628` | y |
| 2167 | 43.2 | 2 | solar | PAST_EXPECTED_START | Telford Shopping Centre - Solar Photovoltaic PV Arra... | Telford Trustee No.1 Limited | Telford and Wrekin | 2022-01-21 | 1683 | 3.2km/132kV | `10072` | y |
| 2168 | 43.1 | 15 | solar | PAST_EXPECTED_START | Blandford Hill - EV Charging Station & Solar Farm | Naturalis Energy Developments Limi... | Dorset | 2022-01-26 | 1678 | 3.3km/132kV | `8462` | y |
| 2169 | 43.1 | 15 | bess | PRE_CONSENT | Newnham Grange Farm - Battery Energy Storage | Neo Environmental (Belfast) | West Northamptonshire | - | - | 2.0km/132kV | `18605` | y |
| 2170 | 43.1 | 6 | bess | PAST_EXPECTED_START | Dunkeswell Airfield | Conrad (Tiddlywink) Limited | East Devon | 2021-11-23 | 1742 | 7.0km/400kV | `7022` | y |
| 2171 | 43.1 | 25 | solar | DESIGN_FROZEN_OR_LATER | White Cross Lane | Nextpower SPV 5 Limited | North Kesteven | 2019-12-31 | - | 0.1km/132kV | `6530` | y |
| 2172 | 43.1 | 25 | solar | PAST_EXPECTED_START | Sherbourne - Solar Farm | Namene Solar | Stratford-on-Avon | 2023-08-16 | 1111 | 6.5km/132kV | `13257` | y |
| 2173 | 43.1 | 1 | solar | PAST_EXPECTED_START | Aflex Hose, Dyson Wood Way - olar Panels | Watson Marlow Fluid Technology Sol... | Kirklees | 2024-06-06 | 816 | 0.9km/275kV | `16252` | y |
| 2174 | 43.0 | 4 | solar | PAST_EXPECTED_START | Uthrogle Mills - Solar Farm | BayWa R.e Operation Services Limit... | Fife | 2023-08-15 | 1112 | 1.9km/132kV | `13536` | y |
| 2175 | 43.0 | 2 | solar | PAST_EXPECTED_START | Solar PV Development in Ballymena | HHT Management Limited | Mid and East Antrim | 2024-08-16 | 745 | 8.3km/275kV | `16454` | y |
| 2176 | 43.0 | 3 | solar | PAST_EXPECTED_START | Amazon UK Services - Photovoltaic System | Zestec Asset Management | County Durham | 2022-04-06 | 1608 | 2.0km/400kV | `10579` | y |
| 2177 | 43.0 | 19 | solar | PRE_CONSENT | Steeley Lane, Steetley - Solar Photovoltaic Farm | Renewable Connections Developments... | Bassetlaw | - | - | 4.6km/132kV | `13679` | y |
| 2178 | 43.0 | 2 | solar | PAST_EXPECTED_START | Schutz UK Limited, Claylands Avenue - Solar Panels | Schutz (UK) Limited | Bassetlaw | 2023-07-26 | 1132 | 3.0km/132kV | `13892` | y |
| 2179 | 43.0 | 31 | bess | PAST_EXPECTED_START | Benthead Farm - Solar Farm & Battery Storage | Locogen Limited | Scottish Government (S36) | 2023-08-11 | 1116 | 2.6km/132kV | `10541` | y |
| 2180 | 42.9 | 40 | bess | DISTRESSED | Tofts Lane | Enstor Power UK | Barnsley | 2017-07-21 | - | 0.4km/400kV | `6942` | **n** |
| 2181 | 42.9 | 40 | bess | DISTRESSED | Carnegie Road (Phase 2) | Shawton Engineering | Liverpool | 2019-12-01 | - | 0.2km/275kV | `7403` | **n** |
| 2182 | 42.9 | 40 | bess | DESIGN_FROZEN_OR_LATER | Leigh Delamere - Solar farm & Battery storage | Eden Renewables | Wiltshire | 2022-08-11 | - | 2.4km/400kV | `9237` | y |
| 2183 | 42.9 | 31 | solar | PRE_CONSENT | East Cowton Solar Farm | Green Nation Solar Energy | North Yorkshire | - | - | 2.4km/132kV | `14793` | y |
| 2184 | 42.8 | 1 | solar | PAST_EXPECTED_START | Doncaster Road, Doncaster Road - Solar Array | M&T Haylage | Doncaster | 2023-06-28 | 1160 | 0.5km/132kV | `12831` | y |
| 2185 | 42.8 | 3 | solar | PAST_EXPECTED_START | Amazon, Symmetry Park - Solar Panels | Push Energy | Swindon | 2022-11-23 | 1377 | 3.2km/132kV | `12267` | y |
| 2186 | 42.8 | 6 | solar | PRE_CONSENT | Stangate West Landfill Site, Quarry Hill Road - Sola... | Infinis Solar Development Limited | Tonbridge and Malling | - | - | 0.7km/132kV | `21068` | y |
| 2187 | 42.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Portadown Road | Low Carbon Storage Ireland | Armagh City, Banbridge and C... | - | - | 0.2km/275kV | `7047` | y |
| 2188 | 42.8 | 50 | bess | PRE_CONSENT | South Kyle Wind Farm 2 | Vattenfall | Scottish Government (S36) | - | - | 1.1km/132kV | `10708` | y |
| 2189 | 42.8 | 50 | bess | PRE_CONSENT | Derehams Farm, Derehams Lane - Battery Storage | Newton Energi Limited | Buckinghamshire | - | - | 5.2km/400kV | `15544` | y |
| 2190 | 42.8 | 30 | bess | PRE_CONSENT | Yew Tree Farm, Drointon Lane | Push Energy | Stafford | - | - | 0.6km/132kV | `14167` | y |
| 2191 | 42.8 | 30 | solar | PRE_CONSENT | Green Lane & Cliff Lane, Gonerby Moor - Solar Farm | Lightsource BP | South Kesteven | - | - | 1.0km/132kV | `19165` | y |
| 2192 | 42.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Ferrymuir | Gore Street Energy Storage Fund | Fife | 2020-01-10 | - | 0.7km/132kV | `7371` | y |
| 2193 | 42.8 | 50 | bess | PRE_CONSENT | Bengrove Farm, Base Lane - Battery Storage | Bengrove Bess Limited | Tewkesbury | - | - | 1.0km/132kV | `12830` | y |
| 2194 | 42.8 | 50 | solar | PAST_EXPECTED_START | High Ercall Solar Farm | Assured Asset Solar 1 Limited | Telford and Wrekin | 2023-08-22 | 1105 | 5.3km/132kV | `13183` | y |
| 2195 | 42.8 | 82 | solar | PRE_CONSENT | M74 West Renewable Energy Park | Renewco Power | Scottish Government (S36) | - | - | 0.4km/400kV | `16026` | y |
| 2196 | 42.8 | 106 | bess | PRE_CONSENT | Bodinglee Wind Farm | Banks Group | Scottish Government (S36) | - | - | 1.8km/400kV | `13638` | y |
| 2197 | 42.8 | 1 | solar | PAST_EXPECTED_START | Tesco Distribution Centre, Stakehill Industrial Esta... | Tritax Management Llp | Rochdale | 2024-04-12 | 871 | 0.4km/275kV | `16093` | y |
| 2198 | 42.8 | 1 | solar | PAST_EXPECTED_START | Fairchild Road, Burtonwood & Westbrook - Solar Panel... | Mountpark Logistics | Warrington | 2023-10-23 | 1043 | 0.4km/132kV | `14452` | y |
| 2199 | 42.8 | 1 | solar | PAST_EXPECTED_START | Smart Systems | D2Smart Projects | North Somerset | 2015-09-28 | 3990 | 0.7km/400kV | `5210` | y |
| 2200 | 42.8 | 1 | solar | PAST_EXPECTED_START | Tesco Store East Didsbury | Tesco Stores | Manchester | 2020-01-15 | 2420 | 1.1km/275kV | `7625` | y |
| 2201 | 42.8 | 1 | solar | PAST_EXPECTED_START | Unit Q1, Quadrant Distribution Centre, Hardwick - So... | MG Markey Group Limited | Stroud | 2022-05-31 | 1553 | 1.7km/132kV | `11171` | y |
| 2202 | 42.8 | 1 | bess | PAST_EXPECTED_START | Studley Grange Landfill Site, Garden Centre Road - B... | Biffa Waste Services | Wiltshire | 2023-01-10 | 1329 | 0.7km/132kV | `12193` | y |
| 2203 | 42.8 | 1 | solar | PAST_EXPECTED_START | Halfway House, Lincoln Hill - Solar Array | Humshaugh Net Zero | Northumberland | 2023-07-14 | 1144 | 2.8km/275kV | `12841` | y |
| 2204 | 42.8 | 1 | solar | PAST_EXPECTED_START | Renolit Cramlington Limited, Station Road - Solar Pa... | Renolit Cramlington Limited | Northumberland | 2024-06-14 | 808 | 0.6km/275kV | `16370` | y |
| 2205 | 42.8 | 1 | solar | PAST_EXPECTED_START | Colton Road, Barnham Broom - Solar Array | Barnham Broom Golf and Country Clu... | South Norfolk | 2025-04-25 | 493 | 0.9km/400kV | `17679` | y |
| 2206 | 42.8 | 105 | bess | PRE_CONSENT | Shinness Wind Farm | Shinness Wind Farm Limited | Scottish Government (S36) | - | - | 0.3km/132kV | `12027` | y |
| 2207 | 42.7 | 18 | solar | PAST_EXPECTED_START | High Street - Solar Farm | Anesco Limited | Cheshire West and Chester | 2022-10-11 | 1420 | 11.2km/132kV | `10000` | y |
| 2208 | 42.7 | 2 | solar | PAST_EXPECTED_START | Business Park, Meridian Drive - Solar Panels | Maersk | North Warwickshire | 2023-09-11 | 1085 | 2.2km/132kV | `14589` | y |
| 2209 | 42.7 | 2 | solar | PAST_EXPECTED_START | Yorkshire Grown Produce, Main Road - Solar Panels | Yorkshire Grown Produce Limited | East Riding of Yorkshire | 2024-02-22 | 921 | 3.6km/400kV | `15593` | y |
| 2210 | 42.6 | 10 | solar | DESIGN_FROZEN_OR_LATER | Hawthorn Farm - Solar photovoltaic panels | Unknown | South Derbyshire | 2022-02-22 | - | 0.4km/132kV | `8856` | y |
| 2211 | 42.6 | 10 | bess | PAST_EXPECTED_START | Park Road Battery Storage | Arlington Energy Limited Avery Ene... | Rossendale | 2021-11-19 | 1746 | 1.8km/132kV | `10076` | y |
| 2212 | 42.6 | 22 | solar | PRE_CONSENT | Holt Lane Solar Park | Wessex Solar Energy | Hart | - | - | 0.1km/132kV | `18642` | y |
| 2213 | 42.6 | 10 | solar | DESIGN_FROZEN_OR_LATER | Rhigos Road - Solar Farm | Regener8 Power / Environmena | Rhondda Cynon Taf | 2024-06-13 | - | 0.3km/132kV | `11384` | y |
| 2214 | 42.6 | 3 | solar | PAST_EXPECTED_START | Salt Ayre Leisure Centre - Solar Farm | Lancaster City Council | Lancaster | 2021-04-28 | 1951 | 0.6km/132kV | `8071` | y |
| 2215 | 42.6 | 3 | solar | PRE_CONSENT | John Lennon Airport Scheme | Peel Energy | Halton | - | - | 1.9km/132kV | `9089` | **n** |
| 2216 | 42.5 | 28 | solar | PAST_EXPECTED_START | Preston Farm, Preston Candover - Solar PV Array | BSR Energy | Basingstoke and Deane | 2022-09-16 | 1445 | 12.1km/132kV | `10045` | y |
| 2217 | 42.5 | 28 | solar | PAST_EXPECTED_START | Docking Farm Solar | Metka EGN Projects Limited | Broadland | 2022-02-11 | 1662 | 2.9km/132kV | `10640` | y |
| 2218 | 42.5 | 28 | solar | PRE_CONSENT | Brandon Fields Estate, Brandon Fields - Solar Panels | OPDE Energy | West Suffolk | - | - | 12.1km/132kV | `18537` | y |
| 2219 | 42.5 | 28 | solar | PRE_CONSENT | Preston, Deanery - Solar Farm | Grange Farm Partnership | West Northamptonshire | - | - | 2.9km/132kV | `11728` | y |
| 2220 | 42.4 | 12 | solar | PRE_CONSENT | Stallingborough Road - Solar PV Panels | Island Green Power | West Lindsey | - | - | 0.7km/400kV | `17509` | y |
| 2221 | 42.4 | 2 | solar | PAST_EXPECTED_START | Solar PV Energy Development in Ballymena | HHT Management Limited | Mid and East Antrim | 2024-08-14 | 747 | 8.3km/275kV | `16451` | y |
| 2222 | 42.4 | 2 | solar | PRE_CONSENT | Auchinlea Landfill Site, Carlisle Road - Solar Array | North Lanarkshire Council | North Lanarkshire | - | - | 1.0km/275kV | `19880` | y |
| 2223 | 42.4 | 35 | solar | PRE_CONSENT | Mount Pleasant Farm - Solar Farm | Belltown Power Limited | Swindon | - | - | 6.0km/132kV | `19159` | y |
| 2224 | 42.4 | 16 | solar | PAST_EXPECTED_START | Barnard Castle - Solar Farm & Battery Storage System | Farm Energy Company | County Durham | 2025-06-10 | 447 | 16.7km/132kV | `14840` | y |
| 2225 | 42.4 | 7 | solar | PRE_CONSENT | Moggerhanger Road, Sandy - Solar Farm | Kach Capital Estates Limited | Central Bedfordshire | - | - | 2.4km/400kV | `10981` | y |
| 2226 | 42.3 | 4 | solar | DESIGN_FROZEN_OR_LATER | Moorhouse Farm, Moorhouse Lane - Solar Park | Cabot Park Solar Limited | Bristol, City of | 2024-04-30 | - | 0.3km/132kV | `13054` | y |
| 2227 | 42.3 | 12 | bess | PRE_CONSENT | New South Farm, Piper Lane - Solar Farm | Abei Energy Group | Rotherham | - | - | 2.2km/275kV | `15653` | y |
| 2228 | 42.3 | 9 | solar | DESIGN_FROZEN_OR_LATER | West Farm, Cosheston - Solar Farm | One Planet Developments Limited | Pembrokeshire | 2024-03-28 | - | 0.4km/132kV | `15617` | y |
| 2229 | 42.3 | 2 | solar | CONSENTED_NO_DATE | Winslade Park - Solar Array | Burrington Estates (New Homes Thri... | East Devon | - | - | 1.2km/132kV | `15800` | y |
| 2230 | 42.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Plot 2B EurolinkV | Trenport Investments | Swale | 2019-07-25 | - | 0.9km/400kV | `7383` | y |
| 2231 | 42.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Gipsy Lane | Arlington Energy | Rochdale | 2020-03-16 | - | 0.1km/132kV | `7632` | y |
| 2232 | 42.2 | 20 | bess | PAST_EXPECTED_START | Duddingston Solar Farm and Battery Storage | Aithrie Net Zero Solar Limited | West Lothian | 2024-04-03 | 880 | 7.1km/132kV | `11382` | y |
| 2233 | 42.2 | 20 | bess | PRE_CONSENT | Upper Leigh - Battery Energy Storage System | Lightrock Power | East Staffordshire | - | - | 0.3km/132kV | `13184` | y |
| 2234 | 42.2 | 20 | bess | PRE_CONSENT | Blackhills Wind Farm | Koehler Renewable Energy | Scottish Government (S36) | - | - | 0.6km/275kV | `16878` | y |
| 2235 | 42.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Siddington Solar Farm | Gresham House / Anesco Limited | Cotswold | 2021-05-21 | - | 1.3km/400kV | `8257` | y |
| 2236 | 42.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Glaxosmithkline Shewalton Road | Glaxosmithkline | North Ayrshire | 2019-06-19 | - | 0.9km/132kV | `7232` | y |
| 2237 | 42.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Balsillie Avenue - Roaring Hill Energy Storage Facil... | Tag Energy UK | Fife | 2021-09-03 | - | 0.1km/275kV | `7989` | **n** |
| 2238 | 42.2 | 3 | solar | PAST_EXPECTED_START | Roddas, The Creamery - Solar Photovoltaic Array | Roddas | Cornwall | 2023-11-08 | 1027 | 0.9km/132kV | `13463` | y |
| 2239 | 42.2 | 5 | bess | PRE_CONSENT | Hill Of Lynchrobbie, Dunbeath - Battery Storage Faci... | E Power Limited | Highland | - | - | 1.1km/132kV | `14399` | y |
| 2240 | 42.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Bowerhouse Farm (extension) | Ethical Power | North Somerset | 2022-03-25 | - | 0.6km/132kV | `7539` | y |
| 2241 | 42.2 | 33 | solar | DESIGN_FROZEN_OR_LATER | Minster Abbey, Bedlam Court Lane - Solar PV panels | The Benedictine Nuns of St Mildred... | Thanet | - | - | 1.5km/400kV | `9681` | y |
| 2242 | 42.2 | 1 | solar | PAST_EXPECTED_START | Pilgrim Factory Car Park And Fields, Cooksland Road ... | Envams Limited | Cornwall | 2024-07-19 | 773 | 2.5km/132kV | `15393` | y |
| 2243 | 42.2 | 3 | bess | PRE_CONSENT | Cellarhead Substation, Rownall Road - Battery Storag... | Sirius Renewable Energy Limited | Staffordshire Moorlands | - | - | 0.6km/400kV | `12448` | y |
| 2244 | 42.2 | 3 | bess | PRE_CONSENT | Rownall Road, Wetley Rocks - Battery Storage | Sirius Renewable Energy Limited | Staffordshire Moorlands | - | - | 0.6km/400kV | `12448` | y |
| 2245 | 42.1 | 15 | solar | DESIGN_FROZEN_OR_LATER | Trinity Hall Solar Farm | European Energy Photovoltaics Limi... | Central Bedfordshire | 2021-05-05 | - | 0.5km/132kV | `12623` | y |
| 2246 | 42.1 | 15 | solar | PRE_CONSENT | East Dundry Lane, Norton Hawkfield - Solar Farm | Enviromena | North Somerset | - | - | 6.8km/132kV | `19279` | y |
| 2247 | 42.1 | 25 | solar | PRE_CONSENT | Prentice’s Farm- Solar Farm | Anglo Renewables | Maldon | - | - | 1.0km/132kV | `16390` | y |
| 2248 | 42.1 | 2 | solar | PAST_EXPECTED_START | Chippenham Drive, Kingston - Solar Panels | Syzygy Renewables | Milton Keynes | 2024-07-02 | 790 | 5.4km/132kV | `16358` | y |
| 2249 | 42.0 | 2 | solar | PAST_EXPECTED_START | Knockout Print Services, Petteridge Lane - Solar Pan... | Knockout Print Services Limited | Tunbridge Wells | 2023-10-16 | 1050 | 3.2km/132kV | `14854` | y |
| 2250 | 42.0 | 19 | solar | DESIGN_FROZEN_OR_LATER | Beavor - Photovoltaic Solar Arrays | Anesco Limited / Gresham House | East Devon | 2022-02-10 | - | 1.5km/400kV | `10040` | y |
| 2251 | 42.0 | 1 | solar | PAST_EXPECTED_START | Fairbrook House, Clover Nook Road - Solar Panels | Eurocell Group | Bolsover | 2024-05-14 | 839 | 3.3km/132kV | `15778` | y |
| 2252 | 42.0 | 11 | solar | PAST_EXPECTED_START | Highgate Lane, Normanby-By-Spital - Solar Photovolta... | Boultbee Brooks Renewables Walkfor... | West Lindsey | 2025-07-24 | 403 | 11.6km/132kV | `15113` | y |
| 2253 | 41.9 | 14 | solar | DESIGN_FROZEN_OR_LATER | Hillhead Of Gask, Longhaven - Solar Array | The Greenspan Agency | Aberdeenshire | 2022-04-08 | - | 1.4km/275kV | `10470` | y |
| 2254 | 41.9 | 40 | solar | DESIGN_FROZEN_OR_LATER | Branston Solar Park (extension) | Ethical Power | North Kesteven | 2017-12-19 | - | 0.7km/132kV | `6456` | y |
| 2255 | 41.9 | 40 | bess | PRE_CONSENT | Loudwater Battery Storage Site | Capbal | Buckinghamshire | 2019-05-24 | - | 5.1km/400kV | `12803` | y |
| 2256 | 41.9 | 1 | solar | DESIGN_FROZEN_OR_LATER | Epic Long Ashton, Phase 1 - 3 Office Buildings | Epic Systems | North Somerset | 2025-03-06 | - | 4.9km/132kV | `15340` | y |
| 2257 | 41.8 | 18 | bess | DESIGN_FROZEN_OR_LATER | Aurora Solar Farm | Low Carbon UK Solar Investment Com... | West Oxfordshire | 2021-04-22 | - | 1.5km/132kV | `7384` | y |
| 2258 | 41.8 | 39 | solar | PRE_CONSENT | Binn Farm Solar Farm | Trio Power Limited | Perth and Kinross | - | - | 3.5km/132kV | `19596` | y |
| 2259 | 41.8 | 1 | solar | PAST_EXPECTED_START | Number One Industrial Estate - Solar Panels | Gardner Aerospace | County Durham | 2022-04-04 | 1610 | 3.1km/400kV | `10738` | y |
| 2260 | 41.8 | 6 | bess | PAST_EXPECTED_START | Holden Way | STOR Power | Tameside | 2018-06-25 | 2989 | 2.3km/132kV | `7145` | y |
| 2261 | 41.8 | 6 | bess | PAST_EXPECTED_START | Stephenson Road - Urban Reserve Flexible Energy Faci... | AMP Energy Services LImited | Colchester | 2022-10-28 | 1403 | 3.7km/132kV | `11362` | y |
| 2262 | 41.8 | 50 | bess | PRE_CONSENT | Crosbie Wind Farm | Galileo Green Energy Scotland Limi... | Scottish Government (S36) | - | - | 2.3km/400kV | `15796` | y |
| 2263 | 41.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Steeraway Farm - Solar Farm | Enviromena | Telford and Wrekin | 2023-05-09 | - | 1.2km/132kV | `10089` | y |
| 2264 | 41.8 | 50 | solar | PRE_CONSENT | Greenhead Energy Park | Exagen | Gateshead | - | - | 1.8km/400kV | `14960` | y |
| 2265 | 41.8 | 50 | solar | PRE_CONSENT | Long Ridding Lane, East Drayton - Solar Farm | High Marnham Renewables Limited | Bassetlaw | - | - | 3.1km/400kV | `20981` | y |
| 2266 | 41.8 | 2 | solar | PAST_EXPECTED_START | Mynydd y Gwryhd Solar Farm | Awel Aman Tawe | Neath Port Talbot | 2020-11-27 | 2103 | 2.3km/132kV | `7894` | y |
| 2267 | 41.8 | 1 | solar | PAST_EXPECTED_START | Shore Road - Distillery and Visitor Centre | Dornoch Distillery | Highland | 2023-10-31 | 1035 | 9.8km/132kV | `13234` | y |
| 2268 | 41.8 | 1 | bess | PAST_EXPECTED_START | Cold Move, Maes-Y-Clawdd | Cold Move Limited | Shropshire | 2023-04-05 | 1244 | 0.4km/132kV | `13304` | y |
| 2269 | 41.8 | 1 | bess | PAST_EXPECTED_START | HHT Battery Energy Storage System in Randalstown | HHT Renewables Ltd | Antrim and Newtownabbey | 2024-08-01 | 760 | 3.6km/275kV | `15515` | y |
| 2270 | 41.8 | 1 | solar | PAST_EXPECTED_START | Romo, Oddicroft Lane - Solar Panels | Romo limited | Ashfield | 2024-05-13 | 840 | 3.0km/132kV | `16180` | y |
| 2271 | 41.7 | 2 | solar | PAST_EXPECTED_START | Stublach Project Solar Farm | Storengy UK Limited | Cheshire West and Chester | 2021-05-04 | 1945 | 1.4km/132kV | `8274` | y |
| 2272 | 41.7 | 2 | solar | PRE_CONSENT | Hendir Uchaf Farm, Minffrwd Road - Solar Array | Shillibier Limited | Bridgend | - | - | 0.2km/400kV | `20312` | y |
| 2273 | 41.6 | 10 | bess | PAST_EXPECTED_START | Greenburn Wind Park | REG Windpower Limited | Scottish Government (S36) | 2023-04-21 | 1228 | 4.9km/132kV | `7865` | **n** |
| 2274 | 41.6 | 10 | solar | PRE_CONSENT | Pool Farm | Leicestershire County Council | Charnwood | - | - | 0.6km/400kV | `10721` | y |
| 2275 | 41.6 | 10 | bess | PRE_CONSENT | Oakley Bush Solar Farm - Battery Storage | Buccleuch Estates Limited | North Northamptonshire | - | - | 0.5km/132kV | `15269` | y |
| 2276 | 41.6 | 10 | solar | PRE_CONSENT | Whitehead Landfill Site, Lower Green Lane - Solar Fa... | Whitehead Restoration Limited | Wigan | - | - | 2.8km/400kV | `16363` | **n** |
| 2277 | 41.6 | 10 | solar | PRE_CONSENT | Whitehead Landfill Site, Lower Green Lane - Solar Fa... | Whitehead Restoration Limited | Wigan | - | - | 2.8km/400kV | `17060` | y |
| 2278 | 41.6 | 10 | bess | PRE_CONSENT | Market Weighton Road, Barlby - Solar Farm & Battery ... | Quintas Cleantech | North Yorkshire | - | - | 4.5km/400kV | `17893` | y |
| 2279 | 41.6 | 2 | solar | PAST_EXPECTED_START | Premier Grocery Products, Kennington Road - Solar Pa... | Premier Foods | Ashford | 2025-03-06 | 543 | 2.5km/132kV | `18082` | y |
| 2280 | 41.6 | 13 | bess | DISTRESSED | Leechpool Farm, Norrington Battery Storage | Ecotricity | Wiltshire | - | - | 0.4km/132kV | `7183` | **n** |
| 2281 | 41.6 | 2 | solar | PRE_CONSENT | Meadows Road, Manvers - Solar Array | Hyperion Zero Limited | Rotherham | - | - | 0.2km/132kV | `10665` | y |
| 2282 | 41.5 | 1 | solar | PRE_CONSENT | Bakkavor, Sluice Road - Solar Array | Bakkavor Group plc | South Holland | - | - | 0.3km/132kV | `20775` | y |
| 2283 | 41.4 | 2 | solar | PRE_CONSENT | Hempsted Lane - Solar Array | Enovert South Limited | Gloucester | - | - | 0.2km/132kV | `11156` | y |
| 2284 | 41.4 | 2 | solar | PAST_EXPECTED_START | Sandscale Park - Solar Array | Cumbria County Council | Westmorland and Furness | 2023-03-03 | 1277 | 0.2km/132kV | `11277` | y |
| 2285 | 41.4 | 2 | solar | PAST_EXPECTED_START | Nantycaws Waste Management Facility, Llanddarog - So... | CWM Environmental Limited (head of... | Carmarthenshire | 2024-12-17 | 622 | 3.0km/132kV | `17264` | y |
| 2286 | 41.4 | 2 | solar | PRE_CONSENT | Trewyn Bach, Clawdd Poncen - Solar Panels | Mark & Nadine Budgen | Denbighshire | - | - | 1.3km/400kV | `18371` | y |
| 2287 | 41.4 | 45 | bess | DESIGN_FROZEN_OR_LATER | Loch Fergus Farm - Energy Storage System | Locogen | Scottish Government (S36) | 2024-10-22 | - | 2.2km/275kV | `12273` | y |
| 2288 | 41.3 | 1 | solar | PRE_CONSENT | Holloway Farm, Great Milton - Solar Arrays | Holloway Farm Industrial Park Limi... | South Oxfordshire | - | - | 2.4km/400kV | `18033` | **n** |
| 2289 | 41.3 | 12 | solar | DESIGN_FROZEN_OR_LATER | Biggin Hill Airport, Main Road - Solar PV Array | LXi REIT | Bromley | - | - | 1.6km/400kV | `15451` | y |
| 2290 | 41.3 | 7 | solar | DESIGN_FROZEN_OR_LATER | Bowmans Harbour Solar Farm | Wolverhampton City Council | Wolverhampton | 2022-04-08 | - | 1.5km/132kV | `9527` | y |
| 2291 | 41.3 | 1 | solar | PRE_CONSENT | The Hut Group, Skyline Drive - Solar Photovoltaic Pa... | London Metric Property Plc | Warrington | 2025-09-30 | - | 0.3km/132kV | `19750` | y |
| 2292 | 41.3 | 9 | solar | PAST_EXPECTED_START | Carr Lane - Solar Farm | Anesco Limited | North Lincolnshire | 2023-08-07 | 1120 | 1.5km/400kV | `9004` | y |
| 2293 | 41.2 | 20 | bess | PAST_EXPECTED_START | Troston Loch Wind Farm | EDF Energy Renewables | Scottish Government (S36) | 2020-12-18 | 2082 | 4.0km/132kV | `6432` | y |
| 2294 | 41.2 | 20 | solar | DISTRESSED | Thanet Way, Herne Bay Solar Farm | Vattenfall | Canterbury | 2021-03-05 | - | 0.5km/132kV | `7411` | **n** |
| 2295 | 41.2 | 20 | bess | PAST_EXPECTED_START | Chleansaid Onshore Wind Farm | ESB | Scottish Government (S36) | 2023-12-15 | 990 | 3.1km/132kV | `7711` | y |
| 2296 | 41.2 | 20 | bess | PRE_CONSENT | Vale of Leven Wind Farm | Coriolis Energy Limited | Scottish Government (S36) | - | - | 0.8km/275kV | `11110` | y |
| 2297 | 41.2 | 20 | solar | PRE_CONSENT | Challoch, Barnkirk Road - Solar Array & Battery Ener... | Shropshire Council | Dumfries and Galloway | - | - | 2.0km/132kV | `17600` | y |
| 2298 | 41.2 | 20 | bess | PRE_CONSENT | Ardoch Farm | Capbal | North Ayrshire | 2021-07-30 | - | 0.6km/132kV | `17926` | y |
| 2299 | 41.2 | 20 | bess | PRE_CONSENT | Ochiltree - Battery Sorage | Statkraft UK Limited | East Ayrshire | - | - | 1.2km/275kV | `8527` | y |
| 2300 | 41.2 | 5 | solar | PRE_CONSENT | Land At Elton Farm | SEP Elton | Cheshire West and Chester | - | - | 0.2km/132kV | `5300` | y |
| 2301 | 41.2 | 5 | bess | PAST_EXPECTED_START | Eden Project | Good Energy | Cornwall | 2019-04-10 | 2700 | 2.9km/132kV | `7373` | y |
| 2302 | 41.2 | 5 | bess | PRE_CONSENT | Tiddlywink Barn | Conrad (Calne) | Wiltshire | - | - | 0.9km/400kV | `7527` | **n** |
| 2303 | 41.2 | 5 | bess | PRE_CONSENT | Coxhall Road, Tattingstone - Battery Storage | AMP Energy Services Limited | Babergh | - | - | 1.3km/132kV | `12693` | y |
| 2304 | 41.2 | 5 | solar | PRE_CONSENT | Welford Road - Solar Farm | Brampton Valley Way Trust | West Northamptonshire | - | - | 4.1km/132kV | `17896` | y |
| 2305 | 41.2 | 9 | solar | PRE_CONSENT | Holmer Green Senior School - Solar Panels | eEnergy | Buckinghamshire | - | - | 0.9km/132kV | `16711` | y |
| 2306 | 41.2 | 1 | solar | PAST_EXPECTED_START | Foxfield Nurseries, School Lane - Solar Panels | Medlar Fruit Farms Limited | Wyre | 2025-07-02 | 425 | 4.8km/400kV | `17795` | y |
| 2307 | 41.2 | 2 | solar | PAST_EXPECTED_START | Coombe Farm, Bean Field - Solar Arrays | A H Warren Trust Limited | Somerset | 2024-09-20 | 710 | 4.1km/132kV | `16653` | y |
| 2308 | 41.1 | 15 | bess | PRE_CONSENT | Cnoc Farasd Wind Farm | E Power Limited | Highland | - | - | 1.8km/400kV | `17575` | y |
| 2309 | 41.1 | 15 | bess | PRE_CONSENT | Bedford Solar, Northill Road - Solar Farm & Battery ... | QC Ubertino Limited | Bedford | - | - | 4.3km/132kV | `18335` | y |
| 2310 | 41.1 | 70 | bess | DESIGN_FROZEN_OR_LATER | Shetland Battery Energy Storage System | Zenobe Energy | Scottish Government (S36) | 2024-02-21 | - | n/a | `12856` | y |
| 2311 | 41.1 | 25 | solar | DISTRESSED | Raventhorpe Lodge (Sweeting Thorns) | Wirsol / Elgar Middleton | North Lincolnshire | 2016-12-05 | - | 1.3km/132kV | `5013` | **n** |
| 2312 | 41.1 | 5 | solar | PRE_CONSENT | Sunnydale Solar Farm | British Solar Renewables | Harborough | - | - | 0.8km/132kV | `7110` | **n** |
| 2313 | 41.1 | 5 | solar | PAST_EXPECTED_START | New Earth Solutions West, High Dike - Solar Panels &... | New Earth Solutions (West) Limited | North Kesteven | 2023-01-31 | 1308 | 4.0km/132kV | `12733` | y |
| 2314 | 41.0 | 88 | bess | PRE_CONSENT | Battery Energy Storage System Development in Drumqui... | Lightsource Renewable Energy Irela... | Fermanagh and Omagh | - | - | 45.5km/275kV | `17824` | y |
| 2315 | 41.0 | 2 | solar | PAST_EXPECTED_START | Hungerford Park - Solar Array | Hungerford Park | West Berkshire | 2025-07-24 | 403 | 8.0km/400kV | `18315` | y |
| 2316 | 41.0 | 2 | solar | PAST_EXPECTED_START | Edbro, Lever Street - Solar Panels | Edbro Plc | Bolton | 2023-06-02 | 1186 | 2.6km/132kV | `13680` | y |
| 2317 | 41.0 | 1 | solar | PRE_CONSENT | Tesco Superstore, Mansell Way - Solar Panels | Tesco Stores Limited | Bolton | - | - | 5.0km/132kV | `20819` | y |
| 2318 | 41.0 | 2 | solar | PRE_CONSENT | Dewsbury Sewage, Clough Lane - Solar Panels | Downing Renewables | Wakefield | - | - | 1.7km/132kV | `16738` | y |
| 2319 | 40.9 | 40 | solar | PRE_CONSENT | Blackthorn Solar Farm | Eden BD Solar Limited | Wiltshire | - | - | 4.5km/132kV | `18216` | y |
| 2320 | 40.9 | 11 | bess | DISTRESSED | Rayleigh Transforming Station | Aura Power / South East Grid Stora... | Rochford | 2017-08-31 | - | 0.2km/132kV | `6984` | **n** |
| 2321 | 40.9 | 14 | solar | DESIGN_FROZEN_OR_LATER | Aborfield Solar Park | Wessex Solar Energy | Wokingham | 2021-03-12 | - | 1.0km/132kV | `5371` | y |
| 2322 | 40.9 | 24 | solar | PRE_CONSENT | Tunstall & East Appleton Solar Farm - Solar Farm | Enviromena | North Yorkshire | - | - | 5.6km/132kV | `19653` | y |
| 2323 | 40.9 | 4 | solar | PRE_CONSENT | Sainsburys, Style Way - Solar Panels | Sainsburys Supermarkets Limited | West Northamptonshire | - | - | 4.4km/400kV | `21019` | y |
| 2324 | 40.8 | 30 | solar | PRE_CONSENT | Wincote Farm, Wincote Lane - Solar Farm | Green Switch Capital | Stafford | - | - | 7.6km/132kV | `11978` | y |
| 2325 | 40.8 | 18 | solar | PAST_EXPECTED_START | Codford Solar Farm Phase 4 | JM Stratton & Company | Wiltshire | 2024-07-17 | 775 | 11.0km/132kV | `14046` | y |
| 2326 | 40.8 | 18 | solar | PRE_CONSENT | Mathurst Solar Farm, Goudhust Road - Solar PV Farm | Renewable Connections Developments... | Maidstone | - | - | 3.6km/132kV | `16858` | y |
| 2327 | 40.8 | 8 | solar | PAST_EXPECTED_START | Shilton Road - Solar Park | Ecotricity Generation Limited | West Oxfordshire | 2023-06-27 | 1161 | 6.0km/400kV | `12168` | y |
| 2328 | 40.8 | 6 | bess | DESIGN_FROZEN_OR_LATER | Rassau Industrial Estate | Private Developer | Blaenau Gwent | 2020-01-22 | - | 0.0km/132kV | `7841` | y |
| 2329 | 40.8 | 6 | bess | DESIGN_FROZEN_OR_LATER | Brindley Close (Extension) | Public Power Solutions | Swindon | 2020-09-04 | - | 0.6km/132kV | `8045` | y |
| 2330 | 40.8 | 50 | bess | PRE_CONSENT | M74 West Renewable Energy Park | Renewco Power | Scottish Government (S36) | - | - | 0.4km/400kV | `16027` | y |
| 2331 | 40.8 | 50 | bess | PRE_CONSENT | Trench Road, Killymallaght Substation - Battery Ener... | Renewable Energy Systems Limited | Derry City and Strabane | - | - | 10.0km/275kV | `17535` | y |
| 2332 | 40.8 | 30 | bess | PRE_CONSENT | Balblair Wind Farm | Wind Power North Two Limited | Scottish Government (S36) | - | - | 0.8km/275kV | `16347` | y |
| 2333 | 40.8 | 50 | bess | DISTRESSED | Riverford Farm | Abham Storage / Statera Energy | South Hams | 2017-12-04 | - | 0.5km/400kV | `7078` | **n** |
| 2334 | 40.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Tiln Farm Solar Farm | Lightsource SPV 154 Limited | Bassetlaw | 2023-09-26 | - | 0.3km/132kV | `7561` | y |
| 2335 | 40.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | East Kilbride - Battery storage | Engie Regeneration Limited | South Lanarkshire | 2022-08-22 | - | 1.8km/400kV | `9013` | y |
| 2336 | 40.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Maidstone Road, Horsmonden - Paddock Solar Farm | Voltalia UK | Tunbridge Wells | 2023-09-05 | - | 2.2km/132kV | `10577` | y |
| 2337 | 40.8 | 1 | bess | PAST_EXPECTED_START | Blenheim Net Zero Estate | Vanburgh Unit Trust | West Oxfordshire | 2021-01-08 | 2061 | 6.2km/132kV | `8069` | y |
| 2338 | 40.8 | 2 | solar | PAST_EXPECTED_START | Mayflower Water Treatment Works, Roborough Down - So... | South West Water | South Hams | 2024-02-28 | 915 | 0.8km/400kV | `12083` | y |
| 2339 | 40.8 | 50 | bess | DESIGN_FROZEN_OR_LATER | Sundridge Hill | RNA Energy | Medway | 2018-08-17 | - | 0.7km/132kV | `7081` | y |
| 2340 | 40.7 | 49 | solar | DESIGN_FROZEN_OR_LATER | Paytherden Solar Farm (Peradon) | Lightrock Power Limited | East Devon | 2022-12-07 | - | 1.3km/400kV | `11756` | y |
| 2341 | 40.7 | 2 | solar | PAST_EXPECTED_START | Sunbank Lane Solar Panels | Zestec Asset Management | Manchester | 2021-07-06 | 1882 | 3.5km/400kV | `9149` | y |
| 2342 | 40.7 | 2 | solar | PAST_EXPECTED_START | Aerospace Business Park | Cenin Renewables | Vale of Glamorgan | 2020-03-26 | 2349 | 2.0km/275kV | `7830` | y |
| 2343 | 40.7 | 2 | solar | PAST_EXPECTED_START | Fordoun Sawmill Solar Array | Green Power (International) Limite... | Aberdeenshire | 2021-05-13 | 1936 | 2.6km/275kV | `9576` | y |
| 2344 | 40.7 | 2 | bess | PAST_EXPECTED_START | IBM Hursley - Battery Storage | IBM UK Limited | Winchester | 2024-06-19 | 803 | 1.6km/132kV | `16242` | y |
| 2345 | 40.7 | 2 | solar | PAST_EXPECTED_START | Newton Farm, Tongue Lane - Solar Farm & Battery Stor... | Newstead Farm | East Riding of Yorkshire | 2025-06-11 | 446 | 2.4km/400kV | `17947` | y |
| 2346 | 40.7 | 3 | bess | PRE_CONSENT | Glenhove Pumping Station, Glenhove Road - BESS | Scottish Water | North Lanarkshire | - | - | 2.0km/132kV | `21002` | y |
| 2347 | 40.6 | 10 | solar | DISTRESSED | Funtley Refuse Tip | Cassidy & Ashton Group Ltd | Winchester | 2013-08-28 | - | 0.9km/400kV | `C1479` | **n** |
| 2348 | 40.6 | 10 | solar | DISTRESSED | Land south of Francis Land | TGC Renewables/NESF | Wrexham | 2016-09-13 | - | 1.7km/132kV | `5281` | **n** |
| 2349 | 40.6 | 10 | bess | DISTRESSED | South Kirkby Business Park | Morris & co Handling | Wakefield | 2018-01-08 | - | 1.0km/400kV | `7109` | **n** |
| 2350 | 40.6 | 10 | bess | DISTRESSED | Britannia House | Peel Energy | Wirral | 2017-12-04 | - | 1.0km/132kV | `7986` | **n** |
| 2351 | 40.6 | 10 | solar | PAST_EXPECTED_START | Kinnell Farm, Kinnell - Solar Farm & Battery Energy ... | One Planet Developments Limited | Angus | 2023-11-20 | 1015 | 4.7km/132kV | `12633` | y |
| 2352 | 40.6 | 4 | solar | PRE_CONSENT | Holme Farm Solar Park | JBM Solutions | Rushcliffe | 2016-01-04 | - | 0.7km/400kV | `12241` | y |
| 2353 | 40.6 | 100 | bess | DESIGN_FROZEN_OR_LATER | Bullen Lane - Battery Storage | Cambridge Power Limited / Pivot Po... | Mid Suffolk | 2022-01-05 | - | 0.9km/400kV | `10311` | y |
| 2354 | 40.6 | 100 | bess | PRE_CONSENT | Murton Way - Battery Energy Storage | First Way Solar Limited | York | - | - | 5.8km/400kV | `18767` | y |
| 2355 | 40.6 | 4 | solar | PAST_EXPECTED_START | Hl Plastics Extrusions, Flamstead House Hall Road - ... | Custom Solar Limited | Amber Valley | 2024-04-23 | 860 | 2.1km/132kV | `15872` | y |
| 2356 | 40.5 | 6 | solar | DESIGN_FROZEN_OR_LATER | Elstow Landfill Site | Bedford Borough Council | Bedford | 2020-11-30 | - | 1.1km/132kV | `8013` | y |
| 2357 | 40.5 | 1 | solar | PAST_EXPECTED_START | Icknield Road, Ipsden - Solar Array & Battery Storag... | Icknield Gas Limited | South Oxfordshire | 2022-12-15 | 1355 | 3.7km/400kV | `10724` | y |
| 2358 | 40.5 | 46 | solar | DESIGN_FROZEN_OR_LATER | Woodington Solar Farm | Woodington Solar Limited | Test Valley | 2017-07-04 | - | 0.4km/132kV | `5883` | y |
| 2359 | 40.4 | 2 | solar | PRE_CONSENT | Camisky Wellfield Water, Blackcairn House - Solar Ar... | Scottish Water National Operations... | Highland | - | - | 0.5km/132kV | `20782` | y |
| 2360 | 40.3 | 1 | solar | PAST_EXPECTED_START | Three Nooks Wood, Weeton Road - Solar Panels | RG & JM Towers | Fylde | 2023-03-15 | 1265 | 2.6km/132kV | `13186` | y |
| 2361 | 40.3 | 120 | bess | PRE_CONSENT | Glen Ullinish II - Wind Farm | Muirhall Energy Limited | Scottish Government (S36) | - | - | 4.9km/132kV | `11000` | y |
| 2362 | 40.2 | 20 | bess | DISTRESSED | Bristol Road | UK Power Reserve | Gloucester | - | - | 1.5km/132kV | `6930` | **n** |
| 2363 | 40.2 | 20 | bess | DISTRESSED | Aven Industrial Estate | Max Design Consultancy | Rotherham | 2018-06-19 | - | 0.4km/400kV | `7007` | **n** |
| 2364 | 40.2 | 20 | bess | DISTRESSED | Leighton Hall Farm | Energy Demand and Response | Cheshire East | 2018-01-12 | - | 0.4km/132kV | `7032` | **n** |
| 2365 | 40.2 | 20 | bess | DISTRESSED | Beaufort Road | UK Power Reserve | Wirral | - | - | 1.4km/132kV | `7128` | **n** |
| 2366 | 40.2 | 1 | solar | PRE_CONSENT | Pendeen Crescent, Snelshall East - Solar panels | GLP Capital | Milton Keynes | - | - | 0.5km/132kV | `16188` | y |
| 2367 | 40.2 | 9 | solar | PAST_EXPECTED_START | Land North of Hill Farm | Greenheath Farming | Cherwell | 2020-10-05 | 2156 | 11.5km/132kV | `7760` | y |
| 2368 | 40.2 | 1 | solar | PAST_EXPECTED_START | Chariot Drive, Newbridge Road - Solar Panels | Nuveen Real Estate | City of Edinburgh | 2022-11-09 | 1391 | 3.7km/132kV | `12254` | y |
| 2369 | 40.2 | 1 | solar | PRE_CONSENT | Perkins Engines | Perkins Engines Company | Peterborough | - | - | 0.5km/132kV | `7771` | **n** |
| 2370 | 40.2 | 1 | solar | PAST_EXPECTED_START | Swinderby Quarry - Solar PV Array | CEMEX UK Properties | North Kesteven | 2023-11-13 | 1022 | 3.9km/400kV | `14667` | y |
| 2371 | 40.2 | 1 | solar | PRE_CONSENT | Sherwin Williams Diversified Brands, Thorncliffe Roa... | Sherwin Williams | Sheffield | - | - | 2.0km/132kV | `20867` | y |
| 2372 | 40.2 | 1 | solar | PRE_CONSENT | Leyland Trucks, Croston Road - Solar Array | Leyland Trucks Limited | South Ribble | - | - | 0.3km/400kV | `21072` | y |
| 2373 | 40.2 | 1 | solar | PAST_EXPECTED_START | Farmers Industrial Estate,Mill Road - Solar PV Syste... | Zestec Renewable Energy | South Norfolk | 2024-04-03 | 880 | 1.2km/400kV | `13817` | y |
| 2374 | 40.1 | 15 | solar | PRE_CONSENT | Chads Farm - Photovoltaic Arrays & Battery Storage | Renewable Connections Developments... | Cheshire West and Chester | - | - | 0.5km/132kV | `10729` | y |
| 2375 | 40.1 | 20 | solar | DISTRESSED | Burton Wold Solar Farm - Site A | First Renewable Developments | North Northamptonshire | 2014-10-27 | - | 0.5km/132kV | `C3245` | **n** |
| 2376 | 40.1 | 6 | solar | DESIGN_FROZEN_OR_LATER | Limebury Farm, Horns Cross - Solar Farm | Green Switch Capital Limited | Torridge | 2023-05-10 | - | 7.1km/400kV | `12972` | y |
| 2377 | 40.1 | 25 | solar | PAST_EXPECTED_START | Steeple Road | Elgin Energy Esco | Antrim and Newtownabbey | 2018-05-24 | 3021 | 5.2km/275kV | `6024` | y |
| 2378 | 40.1 | 1 | solar | PAST_EXPECTED_START | Essentra Components, Langford Lane - Solar Panels | Essentra Security | Cherwell | 2022-10-28 | 1403 | 2.8km/132kV | `12122` | y |
| 2379 | 40.0 | 2 | solar | DESIGN_FROZEN_OR_LATER | Croft Farm, Askern Road - Solar Array & Hydrogen Pla... | CF Estates (Yorkshire) Limited | Doncaster | 2023-05-11 | - | 0.4km/275kV | `12508` | y |
| 2380 | 40.0 | 19 | solar | PRE_CONSENT | Juniper Farm, Main Street - Solar Farm | ABEI Energy Group | North Yorkshire | - | - | 9.2km/132kV | `16763` | y |
| 2381 | 40.0 | 1 | solar | PRE_CONSENT | Sofina Distribution Centre, Normanby Enterprise Park... | Sofina Distribution Centre | North Lincolnshire | - | - | 0.7km/132kV | `18473` | y |
| 2382 | 40.0 | 1 | solar | PAST_EXPECTED_START | Keypoint, South Marston - Solar panels | Logicor | Swindon | 2024-01-17 | 957 | 2.3km/132kV | `14884` | y |
| 2383 | 39.9 | 31 | solar | DISTRESSED | Tealing Airfield PV | Green Cat Renewables | Angus | 2014-12-11 | - | 0.1km/132kV | `B1247` | **n** |
| 2384 | 39.9 | 40 | solar | PRE_CONSENT | Highfield Energy Park | Exagen | Northumberland | - | - | 7.1km/400kV | `12312` | **n** |
| 2385 | 39.9 | 4 | solar | DESIGN_FROZEN_OR_LATER | Lakeside Business Park | Custom Solar Limited | Portsmouth | 2022-11-01 | - | 0.7km/132kV | `15004` | y |
| 2386 | 39.8 | 1 | solar | PRE_CONSENT | Unit 8, Hudson Road - Solar Panels | INFARM | Bedford | - | - | 0.3km/132kV | `12790` | y |
| 2387 | 39.8 | 1 | solar | PAST_EXPECTED_START | Newbridge - Ground mounted solar Pv panels | Scottish Water | City of Edinburgh | 2022-08-04 | 1488 | 4.7km/132kV | `10938` | y |
| 2388 | 39.8 | 50 | bess | PRE_CONSENT | Glentarken Wind Farm | SSE Renewables Wind Farms UK Ltd | Scottish Government (S36) | - | - | 4.5km/132kV | `13002` | y |
| 2389 | 39.8 | 50 | bess | PRE_CONSENT | Quantans Hill Wind Farm | Vattenfall Wind Power Limited | Scottish Government (S36) | - | - | 0.5km/132kV | `13237` | y |
| 2390 | 39.8 | 30 | solar | PAST_EXPECTED_START | Barnfield Solar Farm, Wilmingham Lane - Solar PV Pan... | Low Carbon UK Solar | Isle of Wight | 2023-09-08 | 1088 | 10.8km/132kV | `12894` | y |
| 2391 | 39.8 | 30 | solar | PRE_CONSENT | Thorpe Park Solar Farm | Low Carbon UK Solar Investment Co ... | Tendring | - | - | 1.7km/132kV | `13028` | y |
| 2392 | 39.8 | 50 | bess | CONSENTED_NO_DATE | Glengolly Farmhouse- Battery Energy Storage | Ecocel Energy Storage Limited | Highland | - | - | n/a | `15088` | **n** |
| 2393 | 39.8 | 50 | solar | PRE_CONSENT | Cossans Solar Farm - Solar Farm | BLC Energy | Scottish Government (S36) | - | - | 2.3km/275kV | `18983` | y |
| 2394 | 39.8 | 1 | bess | PAST_EXPECTED_START | Tormywheel Wind Farm Extension | Muirhall Energy | West Lothian | 2020-03-06 | 2369 | 1.8km/400kV | `6208` | y |
| 2395 | 39.8 | 1 | solar | PAST_EXPECTED_START | Sheehan Recycled Aggregates Plant | Sheehan Haulage & Plant Hire Limit... | West Oxfordshire | 2021-10-01 | 1795 | 2.7km/132kV | `9512` | y |
| 2396 | 39.8 | 1 | bess | PAST_EXPECTED_START | Forthside Way - Battery Storage Unit | Stirling Council | Stirling | 2021-12-22 | 1713 | 1.7km/400kV | `10014` | y |
| 2397 | 39.8 | 1 | solar | PAST_EXPECTED_START | Wykey Farm, Ruyton Xi Towns - Solar Array | W H Gittins & Sons | Shropshire | 2022-05-13 | 1571 | 0.6km/400kV | `10882` | y |
| 2398 | 39.8 | 1 | solar | PAST_EXPECTED_START | Buckley Dairy, Fox View, Dry Hill Lane - Solar Array | Buckley Dairy | Kirklees | 2023-01-16 | 1323 | 4.5km/132kV | `12000` | y |
| 2399 | 39.8 | 1 | solar | PRE_CONSENT | D H L Exel Supply Chain Burton Foods, Portal Way - S... | Columbia Threadneedle | Liverpool | - | - | 0.6km/132kV | `14261` | y |
| 2400 | 39.8 | 1 | solar | PAST_EXPECTED_START | Essentra Components, Langford Locks - Solar Panels | Essentra Security | Cherwell | 2024-06-07 | 815 | 2.7km/132kV | `16261` | y |
| 2401 | 39.8 | 1 | bess | PRE_CONSENT | Petroc, Sticklepath - Battery Storage | Petroc College Of Further Educatio... | North Devon | - | - | 0.3km/132kV | `17166` | y |
| 2402 | 39.7 | 3 | solar | PAST_EXPECTED_START | Cherwell Valley Business Park - Solar Park | Cherwell Valley Silos Limited | West Northamptonshire | 2022-05-25 | 1559 | 4.0km/132kV | `10010` | y |
| 2403 | 39.7 | 29 | bess | DISTRESSED | Land at Derwenthaugh Eco Park | Derwenthaugh | Gateshead | 2018-11-23 | - | 0.5km/132kV | `7054` | **n** |
| 2404 | 39.6 | 10 | solar | PRE_CONSENT | Coal Clough Wind Farm (Co-located) | ScottishPower Renewables | Burnley | - | - | 1.1km/132kV | `7669` | y |
| 2405 | 39.6 | 8 | solar | DISTRESSED | Mynydd Bwllfa solar farm | Walters Group | Rhondda Cynon Taf | 2019-04-30 | - | 0.6km/132kV | `C3208` | **n** |
| 2406 | 39.6 | 3 | solar | PRE_CONSENT | London Southend Airport | London Southend Airport Ltd | Rochford | - | - | 2.0km/132kV | `5946` | y |
| 2407 | 39.6 | 3 | solar | PAST_EXPECTED_START | North James Cropper, Garnett Bridge Road - Solar Arr... | Ellergreen Hydro | Westmorland and Furness | 2024-01-17 | 957 | 2.6km/132kV | `13024` | y |
| 2408 | 39.6 | 100 | bess | PRE_CONSENT | Daer Wind Farm | E.ON Climate & Renewables UK Devel... | Scottish Government (S36) | - | - | 4.5km/400kV | `2908` | y |
| 2409 | 39.6 | 100 | bess | DESIGN_FROZEN_OR_LATER | Harestanes Windfarm | ScottishPower Renewables | Scottish Government (S36) | 2019-12-20 | - | 8.7km/400kV | `4119` | y |
| 2410 | 39.6 | 100 | bess | PRE_CONSENT | Energy Storage System Installation in Rasharkin | Renewable Energy Systems (RES) | Causeway Coast and Glens | - | - | 22.6km/275kV | `18463` | y |
| 2411 | 39.5 | 3 | solar | PAST_EXPECTED_START | The Wave - Solar & Battery Development | The Wave Group Limited | South Gloucestershire | 2021-10-22 | 1774 | 0.6km/132kV | `13099` | y |
| 2412 | 39.5 | 10 | solar | DESIGN_FROZEN_OR_LATER | Boston Landfill, Wyberton - Solar PV Array | Infinis Solar Developments Limited | Boston | 2022-01-21 | - | 0.4km/132kV | `9193` | y |
| 2413 | 39.5 | 16 | solar | DESIGN_FROZEN_OR_LATER | Hazelrigg Lane, Scotforth - Solar Farm | BeBa Energy UK Limited / Universit... | Lancaster | 2022-03-09 | - | 1.0km/400kV | `9372` | y |
| 2414 | 39.5 | 12 | solar | PRE_CONSENT | Wales End Road, Cavendish - Solar Farm | Noventum Power Limited | West Suffolk | - | - | 4.9km/132kV | `15752` | y |
| 2415 | 39.4 | 21 | solar | PAST_EXPECTED_START | Town Farm - Solar panels | British Solar Renewables | East Suffolk | 2024-01-05 | 969 | 6.0km/400kV | `9296` | y |
| 2416 | 39.4 | 2 | solar | PAST_EXPECTED_START | The James Hutton Institute - Solar PV Array | Dundee Renewable Energy Society | Perth and Kinross | 2022-01-19 | 1685 | 1.4km/132kV | `9817` | y |
| 2417 | 39.4 | 2 | bess | PRE_CONSENT | Gaston Lane, Farringdon - Solar Farm & Battery Stora... | Quintas Energy UK Limited | East Hampshire | - | - | 0.7km/132kV | `11950` | y |
| 2418 | 39.3 | 12 | solar | PRE_CONSENT | Merks Hill Farm, Braintree Road - Solar Farm | Sky UK Development Limited | Uttlesford | - | - | 10.1km/132kV | `19076` | y |
| 2419 | 39.3 | 2 | solar | PRE_CONSENT | Glenhove Pumping Station, Glenhove Road - Solar Arra... | Scottish Water | North Lanarkshire | - | - | 2.0km/132kV | `21003` | y |
| 2420 | 39.3 | 20 | solar | PRE_CONSENT | Sand Lane Solar Farm | PS Renewables Limited | North Lincolnshire | - | - | 1.8km/132kV | `17395` | y |
| 2421 | 39.3 | 7 | solar | PRE_CONSENT | Land to the south of Hill Farm | TGC Renewables | West Northamptonshire | - | - | 3.0km/400kV | `5880` | y |
| 2422 | 39.3 | 26 | solar | PAST_EXPECTED_START | Atherstone Hill Solar Farm | Elgin Energy Services | Stratford-on-Avon | 2023-04-11 | 1238 | 14.6km/400kV | `13020` | y |
| 2423 | 39.2 | 20 | solar | PAST_EXPECTED_START | Speyslaw Solar Farm | Elgin Energy | Moray | 2017-08-21 | 3297 | 5.8km/132kV | `6416` | y |
| 2424 | 39.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Hawthorne Road | Bluefield Renewable Developments | Sefton | 2022-03-29 | - | 2.6km/132kV | `7800` | y |
| 2425 | 39.2 | 20 | solar | PRE_CONSENT | Hill Farm - Solar Park | Hill Farm Solar Ltd | Blaby | - | - | 1.6km/400kV | `10161` | y |
| 2426 | 39.2 | 15 | solar | DISTRESSED | Coombe Solar Farm | British Solar Renewables | Mid Sussex | 2015-08-10 | - | 0.3km/400kV | `5095` | **n** |
| 2427 | 39.2 | 20 | bess | PAST_EXPECTED_START | Speyslaw Farm - Battery Storage | Elgin Energy EsCo | Moray | 2023-02-09 | 1299 | 5.8km/132kV | `10394` | y |
| 2428 | 39.2 | 5 | solar | PRE_CONSENT | Stud Farm | Mulbrick Cleans Energy | West Berkshire | - | - | 1.1km/400kV | `5574` | y |
| 2429 | 39.2 | 5 | solar | PAST_EXPECTED_START | Land at Martin Farm | Murex Energy | West Devon | 2015-11-16 | 3941 | 9.0km/132kV | `5584` | y |
| 2430 | 39.2 | 5 | solar | PRE_CONSENT | Chamber House | Rochdale Metropolitan Borough Coun... | Rochdale | 2015-07-28 | - | 1.0km/275kV | `9578` | y |
| 2431 | 39.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Meadow Lane Solar Farm | Gresham House / Anesco Limited | Amber Valley | 2021-10-21 | - | 0.7km/132kV | `8897` | y |
| 2432 | 39.1 | 15 | solar | PRE_CONSENT | East Dundry Lane, Norton Hawkfield - Solar Panels | Enviromena | Bath and North East Somerset | - | - | 7.0km/132kV | `19368` | y |
| 2433 | 39.1 | 25 | bess | DISTRESSED | Fraserburgh Development | Immersa | Aberdeenshire | 2018-05-30 | - | 0.2km/132kV | `7041` | **n** |
| 2434 | 39.1 | 25 | solar | DISTRESSED | High Green Longney Estate - Solar Farm | Elgin Energy | Stroud | 2019-09-26 | - | 0.7km/132kV | `7458` | **n** |
| 2435 | 39.1 | 4 | solar | PAST_EXPECTED_START | Gressingham Foods, Hinderclay Road - Solar Array | Centrica Business Solutions UK Ltd | Mid Suffolk | 2024-11-11 | 658 | 5.5km/132kV | `16535` | y |
| 2436 | 39.0 | 19 | solar | DESIGN_FROZEN_OR_LATER | Ray Valley Solar Farm | Low Carbon | Cherwell | 2020-12-04 | - | 2.2km/400kV | `7791` | **n** |
| 2437 | 39.0 | 2 | solar | PRE_CONSENT | Tuckey Farm | Solar Securities | Buckinghamshire | 2015-12-11 | - | 0.1km/132kV | `7311` | y |
| 2438 | 38.9 | 1 | bess | DESIGN_FROZEN_OR_LATER | Panasonic Manufacturing, Pentwyn - BESS | Panasonic Manufacturing UK | Cardiff | 2024-06-27 | - | 0.6km/275kV | `16366` | y |
| 2439 | 38.9 | 40 | solar | PRE_CONSENT | Adj To The A614 - Solar | One Planet Developments Limited | Bassetlaw | - | - | 0.3km/132kV | `16227` | y |
| 2440 | 38.8 | 2 | solar | PAST_EXPECTED_START | Dechra Pharmaceuticals Manufacturing, Building 3 - S... | Dechra Pharmaceuticals Manufacturi... | North Yorkshire | 2022-09-06 | 1455 | 7.7km/132kV | `11726` | y |
| 2441 | 38.8 | 6 | solar | PRE_CONSENT | Wiseburrow Farm | Primrose Solar/Camborne Energy | Mid Devon | - | - | 0.4km/400kV | `5940` | **n** |
| 2442 | 38.8 | 6 | solar | DESIGN_FROZEN_OR_LATER | Coed Ely - Solar Farm | Rhondda Cynon Taff County Borough ... | Rhondda Cynon Taf | 2023-12-05 | - | 0.2km/400kV | `13791` | y |
| 2443 | 38.8 | 50 | bess | PRE_CONSENT | Penicuik, Moorfoot Hills - Torfichen Wind Farm | RES Limited | Scottish Government (S36) | - | - | 9.6km/132kV | `13176` | y |
| 2444 | 38.8 | 30 | bess | DISTRESSED | Drumfad Wood | Capbal | Argyll and Bute | 2021-03-24 | - | 0.1km/132kV | `7165` | **n** |
| 2445 | 38.8 | 1 | solar | PAST_EXPECTED_START | Haw Wood, Thorington - Solar PV Panels | East Green Energy Limited | East Suffolk | 2024-12-13 | 626 | 8.0km/132kV | `16896` | y |
| 2446 | 38.7 | 22 | bess | PRE_CONSENT | Kentish Farm 2 - Battery Energy Storage | Push Energy | Braintree | - | - | 3.8km/400kV | `15318` | y |
| 2447 | 38.7 | 22 | solar | PRE_CONSENT | Cholderton Road, Quarley - Solar Farm | Novus Renewable Services Limited | Test Valley | - | - | 2.6km/132kV | `16538` | y |
| 2448 | 38.6 | 10 | solar | PRE_CONSENT | Bleabeck - Solar Farm | Noventum Power Limited | Westmorland and Furness | - | - | 1.1km/132kV | `14271` | y |
| 2449 | 38.6 | 10 | bess | PRE_CONSENT | Wales End Road, Cavendish - Battery Energy Storage S... | Noventum Power Limited | West Suffolk | - | - | 4.9km/132kV | `15751` | y |
| 2450 | 38.6 | 2 | solar | PRE_CONSENT | Units D E & F, Beaumont Road - Solar Panels | Aberla Energy | Cherwell | - | - | 0.8km/132kV | `21006` | y |
| 2451 | 38.6 | 22 | solar | PRE_CONSENT | Blackberry Lane | Wessex Solar Energy | Welsh Government (NSIP) | - | - | 0.4km/132kV | `16165` | y |
| 2452 | 38.6 | 6 | solar | PRE_CONSENT | Brixworth Landfill, Scaldwell Road - Solar Array & B... | SUEZ Recycling and Recovery UK Lim... | West Northamptonshire | - | - | 7.6km/400kV | `19119` | y |
| 2453 | 38.6 | 3 | solar | PAST_EXPECTED_START | Spring Gardens - Solar Farm | Calleva Community Energy Limited | West Berkshire | 2024-05-29 | 824 | 7.7km/132kV | `14241` | y |
| 2454 | 38.5 | 4 | solar | PRE_CONSENT | Droitwich Road, Martin Hussingtree - Solar Park | Ecotricity Limited | Wychavon | - | - | 0.3km/132kV | `13979` | y |
| 2455 | 38.4 | 2 | solar | PRE_CONSENT | Solar PV Energy Alterations in Belfast | HHT Management Limited | Belfast | - | - | 4.0km/275kV | `16445` | y |
| 2456 | 38.4 | 2 | solar | PRE_CONSENT | Glovers Meadow - Ground Mounted Solar Array | Shropshire Council | Shropshire | - | - | 0.9km/132kV | `16582` | y |
| 2457 | 38.4 | 35 | bess | PRE_CONSENT | Cossans Solar Farm -ESS | BLC Energy | Scottish Government (S36) | - | - | 2.3km/275kV | `18982` | y |
| 2458 | 38.4 | 1 | solar | PAST_EXPECTED_START | Chichester Food Park, Runcton Unit - Solar Panels | Landlink Estates Limited | Chichester | 2024-07-08 | 784 | 6.0km/132kV | `16474` | y |
| 2459 | 38.4 | 7 | solar | PAST_EXPECTED_START | Aldeby Landfill Site Solar Park | Infinis Solar Developments Limited | South Norfolk | 2022-04-08 | 1606 | 5.7km/132kV | `12863` | y |
| 2460 | 38.3 | 1 | solar | UNKNOWN | St Johns Terrace - Solar PV Array | Scottish Water | Aberdeen City | - | - | 0.8km/132kV | `9551` | **n** |
| 2461 | 38.3 | 1 | solar | PAST_EXPECTED_START | Cavenham Quarry, Cavenham Heath - Solar Array | Allen Newport Limited | West Suffolk | 2026-01-19 | 224 | 14.2km/132kV | `18879` | y |
| 2462 | 38.3 | 12 | bess | DISTRESSED | Mucklow Hill | Volta Energy Storage | Dudley | 2017-12-21 | - | 0.5km/132kV | `7984` | **n** |
| 2463 | 38.3 | 1 | solar | PRE_CONSENT | Middleton Lodge, Kneeton Lane - Solar Array | Middleton Lodge Estates Limited | North Yorkshire | - | - | 2.2km/132kV | `20631` | y |
| 2464 | 38.3 | 2 | solar | PAST_EXPECTED_START | ITP Aero, Harrier Park - Solar Panels | ITP Aero UK | Ashfield | 2024-12-04 | 635 | 5.3km/132kV | `17597` | y |
| 2465 | 38.3 | 26 | bess | DISTRESSED | Manor Farm | Coriolis Energy | South Kesteven | 2019-05-14 | - | 0.1km/132kV | `7820` | **n** |
| 2466 | 38.3 | 26 | solar | DESIGN_FROZEN_OR_LATER | Syston Road - Solar Farm | Barber Farm Partnership | Charnwood | 2022-08-12 | - | 4.4km/400kV | `8336` | y |
| 2467 | 38.2 | 20 | solar | DISTRESSED | High Green Longney Estate - Solar Farm | Elgin Energy | Stroud | 2019-07-26 | - | 0.7km/132kV | `6580` | **n** |
| 2468 | 38.2 | 2 | solar | PAST_EXPECTED_START | Silver Howe, Flusco - Solar Array, Wind Turbines Bat... | Leisure Resorts | Westmorland and Furness | 2023-05-19 | 1200 | 4.2km/132kV | `12144` | y |
| 2469 | 38.2 | 26 | solar | DESIGN_FROZEN_OR_LATER | Hull Solar Farm | Gridserve | East Riding of Yorkshire | 2015-10-15 | - | 1.5km/275kV | `5420` | y |
| 2470 | 38.2 | 5 | solar | PRE_CONSENT | Fromby Lane Solar Farm | Formby Lane Solar | West Lancashire | - | - | 2.1km/132kV | `5927` | **n** |
| 2471 | 38.2 | 5 | solar | DISTRESSED | Bryant Field Solar Park | First Renewable Developments | North Northamptonshire | 2015-07-30 | - | 0.6km/132kV | `5944` | **n** |
| 2472 | 38.2 | 5 | solar | PRE_CONSENT | Arla Lockerbie Creamery - Solar Farm | Scottish Southern Energy Renewable... | Dumfries and Galloway | - | - | 8.3km/400kV | `20606` | y |
| 2473 | 38.2 | 9 | bess | PAST_EXPECTED_START | Sunnica Energy Farm (East and West) | Sunnica | The Planning Inspectorate - ... | 2024-07-12 | 780 | 11.1km/400kV | `7188` | y |
| 2474 | 38.1 | 15 | bess | PAST_EXPECTED_START | Hollandmey Renewable Energy Development | Scottishpower Renewables | Scottish Government (S36) | 2024-09-16 | 714 | 17.8km/275kV | `8061` | y |
| 2475 | 38.1 | 15 | solar | PAST_EXPECTED_START | Hollandmey Renewable Energy Development | Scottishpower Renewables | Scottish Government (S36) | 2024-09-16 | 714 | 17.8km/275kV | `8061` | y |
| 2476 | 38.1 | 5 | solar | PRE_CONSENT | Tamerton Road | Roborough Solar | Plymouth | 2016-03-10 | - | 0.7km/400kV | `12924` | y |
| 2477 | 38.0 | 2 | bess | DESIGN_FROZEN_OR_LATER | Riverside Resource Recovery Facility Battery Storage | Riverside Resource Recovery Limite... | Bexley | - | - | 1.8km/400kV | `8261` | y |
| 2478 | 37.9 | 24 | bess | DISTRESSED | The Hollies | Spencer Farm Produce | East Lindsey | - | - | 1.0km/132kV | `1622` | y |
| 2479 | 37.9 | 24 | bess | DISTRESSED | Mauxhall Farm | ENGIE Renewables | North East Lincolnshire | 2021-05-21 | - | 0.8km/400kV | `7826` | **n** |
| 2480 | 37.9 | 24 | solar | DESIGN_FROZEN_OR_LATER | Chalk Pit Solar Farm | Greentech Services | Dover | 2022-11-25 | - | 7.2km/132kV | `11409` | y |
| 2481 | 37.9 | 40 | bess | DESIGN_FROZEN_OR_LATER | Bilbo Solar Farm Energy Storage | Green Energy International | Aberdeenshire | 2019-10-18 | - | 0.7km/132kV | `6736` | y |
| 2482 | 37.9 | 40 | solar | DESIGN_FROZEN_OR_LATER | Loch Fergus Farm - Solar Farm | Locogen | Scottish Government (S36) | 2024-10-22 | - | 2.2km/275kV | `12274` | y |
| 2483 | 37.8 | 6 | bess | DESIGN_FROZEN_OR_LATER | Midsomer Norton - Battery Energy Storage System | Conrad Energy (Developments) II Li... | Bath and North East Somerset | 2022-12-21 | - | 2.6km/132kV | `11866` | y |
| 2484 | 37.8 | 6 | solar | PRE_CONSENT | Sands Farm Quarry, Low Lane - Solar Panels | Valencia Waster Management Limited | Wiltshire | - | - | 7.6km/132kV | `16057` | y |
| 2485 | 37.8 | 50 | bess | PAST_EXPECTED_START | Garn Fach Wind Farm | EDF Renewables | Welsh Government (NSIP) | 2024-10-22 | 678 | 13.4km/132kV | `7704` | y |
| 2486 | 37.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Porth Wen | EDF Energy Renewables | Isle of Anglesey | 2018-03-09 | - | 0.6km/132kV | `6071` | y |
| 2487 | 37.8 | 50 | solar | PRE_CONSENT | Drayton Road, Upton - Solar Farm | High Marham Renewables Limited | Bassetlaw | - | - | 5.8km/400kV | `20872` | y |
| 2488 | 37.8 | 1 | solar | PAST_EXPECTED_START | Modus Furniture, Manor Farm - Solar Panels | MODUS Furniture Limited | Somerset | 2023-01-23 | 1316 | 6.1km/132kV | `12843` | y |
| 2489 | 37.8 | 1 | bess | PAST_EXPECTED_START | Accrington and Rossendale College, Sandy Lane - Batt... | Nelson & Colne College | Hyndburn | 2024-02-02 | 941 | 1.5km/132kV | `15255` | y |
| 2490 | 37.8 | 1 | bess | PAST_EXPECTED_START | Petroc, Bolham Road - Battery Storage & Air Source H... | Petroc | Mid Devon | 2024-01-29 | 945 | 7.6km/132kV | `15884` | y |
| 2491 | 37.8 | 1 | solar | PRE_CONSENT | Severn & Wye, Claxhill - Solar Panels & Battery Ener... | Olsa Futures Limited | Forest of Dean | - | - | 1.9km/132kV | `18283` | y |
| 2492 | 37.8 | 1 | solar | PRE_CONSENT | PFF Packaging, Salters Lane Industrial Estate, Sedge... | SSE Enterprise Contracting | County Durham | - | - | 1.8km/400kV | `18635` | y |
| 2493 | 37.8 | 1 | solar | PRE_CONSENT | Harmer Hill, Webscott - Solar Array | Unknown | Shropshire | - | - | 2.9km/400kV | `20822` | y |
| 2494 | 37.8 | 4 | solar | DISTRESSED | Goddard's Green | Dacorar Southern | Mid Sussex | 2019-07-04 | - | 0.5km/132kV | `6722` | **n** |
| 2495 | 37.8 | 23 | solar | DESIGN_FROZEN_OR_LATER | Hamer Warren Solar Farm | Somerley Estate | New Forest | 2021-02-03 | - | 2.4km/400kV | `8094` | y |
| 2496 | 37.7 | 10 | solar | DESIGN_FROZEN_OR_LATER | Offham Landfill Site - Solar PV Array | Infinis Limited | Tonbridge and Malling | 2023-10-13 | - | 4.9km/132kV | `9002` | y |
| 2497 | 37.6 | 10 | bess | DISTRESSED | Hadham Road | Private Developer | East Hertfordshire | - | - | 0.6km/132kV | `7068` | **n** |
| 2498 | 37.6 | 10 | bess | PRE_CONSENT | Juniper Farm, Main Street - BESS | ABEI Energy Group | North Yorkshire | - | - | 9.2km/132kV | `16762` | y |
| 2499 | 37.6 | 1 | solar | PAST_EXPECTED_START | Flexcon, Whitworth Road - Solar Panels | Flexcon Europe | Fife | 2023-10-13 | 1053 | 2.3km/132kV | `14782` | y |
| 2500 | 37.6 | 17 | solar | DESIGN_FROZEN_OR_LATER | Long Lane Solar Farm / Nottingham Brick Works | Earthworm/ EW Capital | Broxtowe | 2015-11-11 | - | 5.8km/132kV | `5144` | **n** |
| 2501 | 37.6 | 10 | bess | DISTRESSED | Huggin's Hall (Extension) | Glassenbury Battery Storage | Tunbridge Wells | - | - | 0.1km/132kV | `7742` | **n** |
| 2502 | 37.6 | 37 | solar | DESIGN_FROZEN_OR_LATER | Bilbo Solar Farm | Green Energy International | Aberdeenshire | 2019-11-15 | - | 0.7km/132kV | `6736` | y |
| 2503 | 37.6 | 3 | bess | PAST_EXPECTED_START | Blandford Hill - EV Charging Station & Solar Farm | Naturalis Energy Developments Limi... | Dorset | 2022-01-26 | 1678 | 3.3km/132kV | `8461` | y |
| 2504 | 37.5 | 2 | solar | PAST_EXPECTED_START | Whalesborough Farm, Marhamchurch - Solar Array | Country Parks Limited | Cornwall | 2024-02-23 | 920 | 8.4km/132kV | `14570` | y |
| 2505 | 37.5 | 1 | solar | PRE_CONSENT | Horizon Centre, Gretton Road - Solar Array | Custom Solar Limited | North Northamptonshire | - | - | 2.1km/132kV | `21050` | y |
| 2506 | 37.5 | 16 | solar | PRE_CONSENT | Kentish Farm 2 - Solar Farm | Push Energy | Braintree | - | - | 3.8km/400kV | `15319` | y |
| 2507 | 37.5 | 10 | solar | PAST_EXPECTED_START | Chittering Solar Farm - extension 2 | Abbey Renewables (North Fen Solar ... | South Cambridgeshire | 2015-06-16 | 4094 | 6.0km/132kV | `C3212` | **n** |
| 2508 | 37.4 | 1 | solar | PRE_CONSENT | Warburtons Bakery, Western Approach Distribution Par... | Warburtons Limited | South Gloucestershire | - | - | 0.5km/400kV | `20967` | y |
| 2509 | 37.4 | 2 | bess | DESIGN_FROZEN_OR_LATER | Lakeside Business Park | Custom Solar Limited | Portsmouth | 2022-11-01 | - | 0.7km/132kV | `15003` | y |
| 2510 | 37.3 | 5 | solar | PRE_CONSENT | Aston Martin Lagonda, Banbury Road - Solar panels | Aston Martin Head Office | Stratford-on-Avon | - | - | 5.0km/132kV | `16945` | y |
| 2511 | 37.3 | 200 | bess | PRE_CONSENT | Corriemoillie Substation Garve - Battery Energy Stor... | Isenau Energy Storage Five Limited | Scottish Government (S36) | - | - | 56.4km/132kV | `14677` | y |
| 2512 | 37.2 | 20 | solar | PAST_EXPECTED_START | High Parkfoot Farm | Elgin Energy | Cumberland | 2022-07-21 | 1502 | 6.1km/132kV | `6588` | y |
| 2513 | 37.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Swinford Wind Farm | Vattenfall | Harborough | 2021-12-22 | - | 1.0km/400kV | `6720` | y |
| 2514 | 37.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Carn Nicholas Farm | Suncredit UK | Swansea | 2015-12-14 | - | 0.6km/132kV | `5593` | y |
| 2515 | 37.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Jemmys Carr | Beacons Cross Solar (formerly Jemm... | Sefton | 2016-09-23 | - | 1.4km/132kV | `5938` | y |
| 2516 | 37.2 | 5 | bess | DESIGN_FROZEN_OR_LATER | Silver Spinney Farm | Thrive Renewables | West Northamptonshire | - | - | 2.9km/400kV | `7307` | y |
| 2517 | 37.2 | 5 | bess | DESIGN_FROZEN_OR_LATER | The Glowhouse | AMP Clean Energy | South Ribble | 2020-10-21 | - | 0.3km/132kV | `8031` | y |
| 2518 | 37.2 | 5 | solar | PAST_EXPECTED_START | Barton Road, Barton - Solar Farm | Cambridge University Director Of E... | South Cambridgeshire | 2023-08-09 | 1118 | 7.0km/132kV | `10578` | y |
| 2519 | 37.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Shewalton Landfill Solar Farm | North Ayrshire Council | North Ayrshire | 2023-06-15 | - | 1.7km/132kV | `13250` | y |
| 2520 | 37.2 | 5 | solar | PRE_CONSENT | Salcey Green Farm - Solar Panels | Salcey Green Farm | Milton Keynes | - | - | 7.7km/400kV | `15458` | **n** |
| 2521 | 37.1 | 15 | bess | PRE_CONSENT | High Mark Wind Farm - Wind Turbines | Wind Estate (UK) Ltd | Scottish Government (S36) | - | - | 5.1km/132kV | `16807` | y |
| 2522 | 37.1 | 90 | bess | PRE_CONSENT | Rivox Wind Farm - Wind farm | Belltown Power Limited | Scottish Government (S36) | - | - | 6.8km/275kV | `9317` | y |
| 2523 | 37.1 | 1 | solar | PAST_EXPECTED_START | Coppice Farm, Pen-Rhos - Solar Array | Coppice Farm | Powys | 2023-01-26 | 1313 | 2.0km/132kV | `12582` | y |
| 2524 | 37.1 | 1 | solar | PAST_EXPECTED_START | Water Treatment Works, Howden Wells - Solar Photovol... | Scottish Water | Scottish Borders | 2023-09-29 | 1067 | 4.8km/132kV | `14059` | y |
| 2525 | 37.0 | 8 | solar | DISTRESSED | Burton Wold Solar Farm | First Renewable Developments | North Northamptonshire | 2015-04-10 | - | 1.1km/132kV | `5024` | **n** |
| 2526 | 37.0 | 1 | solar | PRE_CONSENT | Tramway Farm, Crickheath - Solar Array | R & E J Bowker | Shropshire | - | - | 0.2km/132kV | `12905` | **n** |
| 2527 | 37.0 | 1 | solar | PRE_CONSENT | Tramway Farm, Crickheath - Solar Array | R & E J Bowker | Shropshire | - | - | 0.2km/132kV | `14425` | y |
| 2528 | 37.0 | 1 | solar | PAST_EXPECTED_START | Winston Farm, Ellesmere Road - Solar Array | S F Jones Limited | Shropshire | 2023-08-10 | 1117 | 2.4km/132kV | `13997` | y |
| 2529 | 37.0 | 14 | solar | DESIGN_FROZEN_OR_LATER | Stanstead Solar Project | Manchester Airport Group Plc | Uttlesford | 2022-08-24 | - | 6.5km/132kV | `9503` | y |
| 2530 | 36.9 | 14 | bess | PRE_CONSENT | Guildford Road Battery Storage Facility | Conrad Energy (Developments) Limit... | Waverley | - | - | 11.8km/132kV | `8269` | y |
| 2531 | 36.8 | 18 | solar | DISTRESSED | Mauxhall Farm | ENGIE Renewables | North East Lincolnshire | 2020-05-28 | - | 0.8km/400kV | `7221` | **n** |
| 2532 | 36.8 | 18 | bess | DISTRESSED | Churchtown Solar Farm Battery Storage | Renewable Energy Systems (RES) | Cornwall | 2021-03-08 | - | 0.1km/132kV | `7726` | **n** |
| 2533 | 36.8 | 6 | bess | PAST_EXPECTED_START | Shepherd's Rig Wind Farm | Boralex/Infinergy | Scottish Government (S36) | 2023-08-21 | 1106 | 4.7km/132kV | `3417` | y |
| 2534 | 36.8 | 6 | bess | PRE_CONSENT | Challoch, Barnkirk Road - Solar Array & Battery Ener... | Shropshire Council | Dumfries and Galloway | - | - | 2.0km/132kV | `17601` | y |
| 2535 | 36.8 | 18 | solar | DESIGN_FROZEN_OR_LATER | Kiln Fields Solar Farm | Enviromena Asset Management UK Lim... | Hart | 2021-12-20 | - | 0.5km/400kV | `9941` | y |
| 2536 | 36.8 | 50 | solar | PRE_CONSENT | Flashbrook Road, Knighton - Solar Farm | Scottish Power Renewables | Stafford | - | - | 10.7km/132kV | `16066` | y |
| 2537 | 36.8 | 1 | solar | PAST_EXPECTED_START | Ardagh Glass Limited - Solar Panels | Ardagh Glass Limited | North Ayrshire | 2021-08-17 | 1840 | 4.0km/132kV | `9352` | y |
| 2538 | 36.8 | 1 | solar | PRE_CONSENT | Princess Yachts Ltd (5) | Eden Sustainable | Plymouth | - | - | 1.8km/132kV | `9412` | y |
| 2539 | 36.8 | 1 | solar | PAST_EXPECTED_START | Sansaw Business Park, Hadnall - Solar Panels | Sansaw Properties Limited | Shropshire | 2022-05-30 | 1554 | 4.9km/400kV | `11028` | y |
| 2540 | 36.8 | 3 | solar | PRE_CONSENT | Chapel Banks, Curwen Road - Solar Panels | Murphy Technologies Limited | Cumberland | - | - | 2.6km/132kV | `21016` | y |
| 2541 | 36.7 | 49 | bess | DISTRESSED | Salt End Lane | AMPY Energy Services | East Riding of Yorkshire | 2018-02-28 | - | 0.3km/132kV | `7039` | **n** |
| 2542 | 36.7 | 2 | solar | PAST_EXPECTED_START | Baker Barracks Solar Development | Defence Estates Infrastructure Org... | Chichester | 2021-02-22 | 2016 | 6.0km/132kV | `8180` | y |
| 2543 | 36.6 | 10 | bess | DESIGN_FROZEN_OR_LATER | Moston Vale | Novus Renewable Services | Manchester | 2020-11-24 | - | 2.2km/132kV | `8085` | y |
| 2544 | 36.6 | 17 | solar | PRE_CONSENT | Long Lane Solar Farm | Earthworm | Broxtowe | - | - | 5.8km/132kV | `5603` | y |
| 2545 | 36.6 | 4 | solar | DESIGN_FROZEN_OR_LATER | Banbeath Industrial Estate Solar Array | RWE Renewables UK Limited | Fife | 2022-09-30 | - | 1.1km/132kV | `9500` | y |
| 2546 | 36.6 | 13 | bess | PAST_EXPECTED_START | Hollins Lane - Battery Energy Storage | Hydrock Consultants Limited | Shropshire | 2023-05-17 | 1202 | 13.1km/132kV | `13144` | y |
| 2547 | 36.6 | 13 | bess | PRE_CONSENT | Greenhead Energy Park | Exagen | Gateshead | - | - | 1.8km/400kV | `14959` | y |
| 2548 | 36.6 | 3 | solar | DISTRESSED | Morfa Ynys Farmlands | Energi Generation (formerly Solar ... | Carmarthenshire | 2016-05-03 | - | 0.2km/132kV | `5897` | **n** |
| 2549 | 36.6 | 3 | bess | PAST_EXPECTED_START | Dunore Point Treatment Works | NI Water | Antrim and Newtownabbey | 2022-05-18 | 1566 | 11.0km/275kV | `8171` | y |
| 2550 | 36.6 | 3 | solar | PRE_CONSENT | Chicklade EV Service Station - Solar Farm | Enviromena | Wiltshire | - | - | 5.6km/132kV | `20503` | y |
| 2551 | 36.6 | 1 | solar | PAST_EXPECTED_START | Thorlux Lighting Moons, Merse Road - Solar PV system | FW Thorpe PLC | Redditch | 2022-02-25 | 1648 | 5.3km/275kV | `10528` | y |
| 2552 | 36.6 | 100 | bess | PRE_CONSENT | Skreen Road - Battery Energy Storage System | Renewable Energy Systems Ltd | Fermanagh and Omagh | - | - | 45.2km/275kV | `18111` | y |
| 2553 | 36.5 | 4 | bess | PRE_CONSENT | Sands Farm Quarry, Low Lane - Battery Storage | Valencia Waster Management Limited | Wiltshire | - | - | 7.6km/132kV | `16058` | y |
| 2554 | 36.4 | 2 | solar | PRE_CONSENT | Compass House, Columbus Avenue - Solar Panels | Speciality Breads Limited | Thanet | - | - | 0.7km/132kV | `21030` | y |
| 2555 | 36.4 | 21 | solar | DESIGN_FROZEN_OR_LATER | Kincraig - Solar Farm and battery storage system | Renewable Connections Developments... | Aberdeenshire | 2022-10-18 | - | 5.3km/275kV | `11177` | y |
| 2556 | 36.4 | 7 | bess | DISTRESSED | The Brick Bank | Levington Developments | Stockton-on-Tees | 2019-01-08 | - | 1.6km/132kV | `7980` | **n** |
| 2557 | 36.4 | 7 | solar | PAST_EXPECTED_START | Rowan Gate - Solar Farm | Blackford Farms | Perth and Kinross | 2022-07-12 | 1511 | 8.2km/400kV | `11208` | y |
| 2558 | 36.4 | 7 | solar | PRE_CONSENT | Hamilton Road - Solar Farm | Hamilton Solar Limited | Ashfield | - | - | 3.9km/132kV | `20136` | **n** |
| 2559 | 36.3 | 1 | bess | PAST_EXPECTED_START | Arreton Valley Nursery, Hale Common - Battery Storag... | Iow Squirrel Limited | Isle of Wight | 2023-07-31 | 1127 | 6.5km/132kV | `14047` | y |
| 2560 | 36.3 | 2 | solar | PAST_EXPECTED_START | Marsh Farm, Sea Lane - Solar Array | Staples Brothers Limited | Boston | 2023-05-10 | 1209 | 4.8km/132kV | `13224` | y |
| 2561 | 36.3 | 7 | solar | DISTRESSED | Allsetts Farm | Gamma Solar Limited | Malvern Hills | 2015-08-14 | - | 0.4km/132kV | `5130` | **n** |
| 2562 | 36.2 | 20 | bess | DISTRESSED | Kilshaw Street | Capbal | Wigan | 2019-03-04 | - | 1.6km/132kV | `7072` | **n** |
| 2563 | 36.2 | 20 | bess | PRE_CONSENT | Perseverance Road | Noriker Power | Herefordshire, County of | - | - | 6.1km/132kV | `7966` | y |
| 2564 | 36.2 | 20 | bess | PRE_CONSENT | West Torrisdale Wind Farm | ESB Asset Development UK | Scottish Government (S36) | - | - | 2.4km/132kV | `8490` | y |
| 2565 | 36.2 | 5 | solar | PRE_CONSENT | Land West Of Vicarage Lane | SEP Puddington | Cheshire West and Chester | - | - | 0.4km/400kV | `5317` | y |
| 2566 | 36.2 | 5 | solar | PRE_CONSENT | Back Lane Solar Farm | BE Renewables | Sefton | - | - | 3.1km/132kV | `5936` | **n** |
| 2567 | 36.2 | 5 | bess | PAST_EXPECTED_START | Bunloinn Wind Farm | Energiekontor (UK) Limited | Scottish Government (S36) | 2024-04-02 | 881 | 4.8km/132kV | `9417` | y |
| 2568 | 36.2 | 1 | solar | PAST_EXPECTED_START | Car Park Legoland Windsor Resort, Winkfield Road - P... | Legoland Windsor Park Limited | Windsor and Maidenhead | 2024-06-06 | 816 | 5.7km/132kV | `15661` | y |
| 2569 | 36.1 | 15 | solar | PAST_EXPECTED_START | Howpark Solar Farm | Eurowind (UK) Limited | Scottish Borders | 2024-07-17 | 775 | 5.9km/400kV | `6214` | y |
| 2570 | 36.1 | 25 | solar | DISTRESSED | Stud Solar Farm | Martifer Solar (Voltalia) | Newark and Sherwood | 2015-06-15 | - | 0.4km/400kV | `4809` | **n** |
| 2571 | 36.1 | 5 | solar | PRE_CONSENT | Ty Du Uchaf, Pentreuchaf - Solar Panels | Hari Parry | Gwynedd | - | - | 3.6km/132kV | `16922` | y |
| 2572 | 36.0 | 6 | solar | DISTRESSED | Land north of Bryn Lane | TGC Renewables | Wrexham | 2016-09-13 | - | 1.4km/132kV | `5270` | **n** |
| 2573 | 36.0 | 2 | solar | PAST_EXPECTED_START | Felixstowe Mega Distibution Centre - Photovoltaic Ar... | Uniserve Group | East Suffolk | 2022-12-02 | 1368 | 12.9km/132kV | `11997` | y |
| 2574 | 35.9 | 1 | solar | DESIGN_FROZEN_OR_LATER | Concorde Way, Segensworth - Solar Panels | Solar Advanced Systems T/A SAS Ene... | Winchester | 2022-11-30 | - | 0.2km/400kV | `11755` | y |
| 2575 | 35.9 | 4 | solar | PRE_CONSENT | Preston Deanery | Rochester 003 /Elgar Middleton | West Northamptonshire | - | - | 3.1km/132kV | `6067` | **n** |
| 2576 | 35.8 | 50 | bess | PAST_EXPECTED_START | Alness Grid Sub Station, Mid Balnacraig - Battery St... | Balnacraig Battery Storage Limited | Highland | 2023-12-11 | 994 | n/a | `12780` | **n** |
| 2577 | 35.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Attleborough Road Solar Farm | Pace Carnival Energy | Breckland | 2021-10-11 | - | 11.7km/400kV | `8010` | y |
| 2578 | 35.8 | 30 | solar | DESIGN_FROZEN_OR_LATER | Bishampton Solar Farm | Infinis | Wychavon | 2021-11-05 | - | 4.1km/400kV | `11624` | **n** |
| 2579 | 35.8 | 50 | solar | DISTRESSED | RAF Desborough | RAF Desb | North Northamptonshire | 2015-08-26 | - | 2.5km/132kV | `4968` | **n** |
| 2580 | 35.8 | 1 | solar | DESIGN_FROZEN_OR_LATER | A J Lowther and Son Premise | Private Developer | Herefordshire, County of | 2020-10-16 | - | 1.4km/400kV | `7508` | y |
| 2581 | 35.8 | 23 | bess | PRE_CONSENT | Tweed Valley, Southern Uplands - Oliver Forest Wind ... | Statkraft UK Limited | Scottish Government (S36) | - | - | 7.4km/275kV | `17135` | y |
| 2582 | 35.7 | 2 | solar | PRE_CONSENT | Holloway Farm, Great Milton - Solar Arrays | Holloway Farm Industrial Park Limi... | South Oxfordshire | - | - | 2.4km/400kV | `20671` | y |
| 2583 | 35.7 | 48 | solar | DISTRESSED | Scopwick (Blankney Farm) | Hazel Capital LLP | North Kesteven | 2014-09-25 | - | 2.1km/132kV | `C3242` | **n** |
| 2584 | 35.6 | 6 | solar | DISTRESSED | Former Langton Colliery Site | Van Elle | Ashfield | 2016-06-30 | - | 1.0km/132kV | `6076` | **n** |
| 2585 | 35.6 | 10 | bess | DISTRESSED | Orchardbank Industrial Estate | Capbal | Angus | 2018-01-05 | - | 1.4km/275kV | `7574` | **n** |
| 2586 | 35.6 | 17 | solar | PRE_CONSENT | Oulton Street | Docking Farm Solar Limited | Broadland | - | - | 2.9km/132kV | `7918` | **n** |
| 2587 | 35.6 | 3 | solar | DESIGN_FROZEN_OR_LATER | Newcastle International Airport Phase 1 -Solar Farm | Newcastle International Airport | Newcastle upon Tyne | 2022-03-02 | - | 2.2km/275kV | `9755` | y |
| 2588 | 35.5 | 4 | solar | PRE_CONSENT | Bluestone National Park Resort, Canaston Wood - Sola... | Bluestone Resorts Limited | Pembrokeshire | - | - | 2.0km/132kV | `12976` | y |
| 2589 | 35.5 | 12 | bess | PRE_CONSENT | Highfield Energy Park | Exagen | Northumberland | - | - | 7.1km/400kV | `12311` | **n** |
| 2590 | 35.4 | 2 | solar | DISTRESSED | Amazon Boundary Way | Amazon UK Services / Push Energy | Dacorum | 2019-07-18 | - | 1.1km/400kV | `7250` | **n** |
| 2591 | 35.4 | 2 | solar | PRE_CONSENT | Hersey Gardens - Solar Panels | Bristol City Leap | Bristol, City of | - | - | 6.5km/132kV | `19520` | y |
| 2592 | 35.3 | 1 | solar | PRE_CONSENT | Berllandeg Farm, Rhoswiel - Solar Panels | Private Developer | Shropshire | - | - | 0.9km/132kV | `18884` | y |
| 2593 | 35.3 | 1 | solar | PRE_CONSENT | Westmorland Motorway Services, Tebay - Solar Array | Westmorland Family Limited | Westmorland and Furness | - | - | 4.6km/400kV | `17283` | y |
| 2594 | 35.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Douglas West Wind Farm (extension) | ScottishPower Renewables (UK) Limi... | Scottish Government (S36) | 2021-11-18 | - | 3.4km/132kV | `6826` | y |
| 2595 | 35.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Chelveston Renewable Energy Park | Federal Estates | North Northamptonshire | 2018-05-10 | - | 5.7km/132kV | `6941` | y |
| 2596 | 35.2 | 20 | bess | DESIGN_FROZEN_OR_LATER | Arecleoch Wind Farm (extension) | ScottishPower Renewables | Scottish Government (S36) | 2021-11-16 | - | 0.3km/132kV | `7881` | **n** |
| 2597 | 35.2 | 20 | bess | PRE_CONSENT | Dorenell Extension Wind Farm | Galileo | Scottish Government (S36) | - | - | 9.7km/132kV | `14535` | y |
| 2598 | 35.2 | 20 | bess | PRE_CONSENT | Cruach Clenamacrie Wind Farm | Voltalia | Scottish Government (S36) | - | - | 8.8km/132kV | `14548` | y |
| 2599 | 35.2 | 5 | bess | DISTRESSED | Dolgarrog Hydro Power Station | Innogy | Conwy | 2020-01-08 | - | 0.2km/132kV | `4881` | y |
| 2600 | 35.2 | 5 | solar | DISTRESSED | Welby Road Solar Farm | First Renewable Developments | Melton | 2015-09-10 | - | 0.5km/132kV | `5272` | **n** |
| 2601 | 35.2 | 5 | solar | DISTRESSED | Windmill Solar Farm | First Renewable Developments | North Northamptonshire | 2015-07-30 | - | 1.1km/132kV | `5280` | **n** |
| 2602 | 35.2 | 5 | solar | DISTRESSED | Top Lodge Solar Farm | First Renewable Developments | North Northamptonshire | 2015-07-29 | - | 1.1km/132kV | `5388` | **n** |
| 2603 | 35.2 | 5 | solar | DISTRESSED | Land North of Saddler Nook Lane | Delta Solar | Lancaster | 2015-10-22 | - | 1.9km/400kV | `5509` | **n** |
| 2604 | 35.2 | 5 | solar | DISTRESSED | Snowdown Colliery | BNRG Renewables UK | Dover | 2016-01-28 | - | 3.1km/132kV | `5567` | **n** |
| 2605 | 35.2 | 5 | solar | DISTRESSED | Old Dalby Lodge Farm | Ecotricity | Melton | 2016-05-12 | - | 3.4km/132kV | `5759` | **n** |
| 2606 | 35.2 | 5 | solar | PAST_EXPECTED_START | Wayside Farm | Yge Warren House | North Norfolk | 2016-02-17 | 3848 | 14.7km/132kV | `5878` | y |
| 2607 | 35.2 | 5 | solar | DISTRESSED | Royston Solar Farm (Phase 1) | Canadian Solar | South Cambridgeshire | 2014-10-29 | - | 0.6km/132kV | `5988` | **n** |
| 2608 | 35.2 | 5 | solar | DISTRESSED | Minnis Farm | Generale Du Solaire | Cherwell | - | - | 0.4km/132kV | `7350` | **n** |
| 2609 | 35.2 | 5 | bess | DISTRESSED | Swales Moor Farm | Bouygues Energies | Calderdale | 2020-08-13 | - | 0.6km/275kV | `7725` | **n** |
| 2610 | 35.2 | 2 | solar | PAST_EXPECTED_START | Natures Way Food, Chichester Road - Solar Panels | Landlink Estates Limited | Chichester | 2024-07-08 | 784 | 14.7km/132kV | `16462` | y |
| 2611 | 35.2 | 1 | solar | PRE_CONSENT | Birmingham And Solihull Rugby Club, Forshaw Heath La... | Birmingham & Solihull Rugby Footba... | Stratford-on-Avon | - | - | 3.0km/132kV | `18191` | y |
| 2612 | 35.2 | 2 | solar | PAST_EXPECTED_START | Little Cressingham, Cranswick Country Foods - Solar ... | Cranswick Country Foods Plc | Breckland | 2023-03-27 | 1253 | 10.1km/132kV | `12943` | y |
| 2613 | 35.2 | 7 | solar | DESIGN_FROZEN_OR_LATER | Wren Kitchens & Bedrooms, Parrott Street - Solar Arr... | Wren Kitchens Limited | North Lincolnshire | - | - | 3.2km/400kV | `20992` | y |
| 2614 | 35.1 | 4 | solar | PRE_CONSENT | Ditcheat - Solar Panels | Communities for Renewables | Somerset | - | - | 4.2km/400kV | `16978` | y |
| 2615 | 34.9 | 14 | solar | PAST_EXPECTED_START | Fen Farm - Solar Park | Ecotricity Limited | East Lindsey | 2024-08-02 | 759 | 15.5km/132kV | `16253` | y |
| 2616 | 34.8 | 6 | solar | PAST_EXPECTED_START | Glenkiln Farm, Lamlash Brodick - Solar Farm | Arran Community Renewables | North Ayrshire | 2025-03-20 | 529 | 26.1km/132kV | `15923` | y |
| 2617 | 34.8 | 10 | solar | PRE_CONSENT | Station Road, Ardley - Solar Farm & Battery Energy S... | Valencia Waster Management Limited | Cherwell | - | - | 6.4km/132kV | `16000` | y |
| 2618 | 34.8 | 50 | solar | DISTRESSED | Defford Aerodrome | Solar Planning | Wychavon | 2015-01-08 | - | 7.0km/132kV | `C3224` | **n** |
| 2619 | 34.8 | 1 | solar | PAST_EXPECTED_START | Leviton, Viewfield Industrial Estate - Solar Panels | Leviton Network Solutions europe | Fife | 2022-11-25 | 1375 | 2.9km/275kV | `12324` | y |
| 2620 | 34.7 | 2 | solar | PRE_CONSENT | Pyewipe Farm, Redbourne Road - Solar Arrays | Lincolnshire Pork Company Limited | North Lincolnshire | - | - | 5.3km/132kV | `20484` | y |
| 2621 | 34.7 | 3 | solar | PRE_CONSENT | Droop Hill, Glenbervie - Solar Park | The Greenspan Agency | Aberdeenshire | - | - | 2.7km/275kV | `18482` | y |
| 2622 | 34.7 | 2 | solar | DESIGN_FROZEN_OR_LATER | Belton Farm, Belton - Solar Pv System | Conrad Energy (Developments) Limit... | Shropshire | 2024-04-03 | - | 2.5km/132kV | `15591` | y |
| 2623 | 34.6 | 10 | solar | DISTRESSED | Cordon Farm | Elgin Energy | Perth and Kinross | 2017-07-19 | - | 0.8km/132kV | `6594` | **n** |
| 2624 | 34.6 | 10 | bess | DISTRESSED | Manton Wood | Lark Gas Assets | Bassetlaw | 2017-12-12 | - | 0.4km/132kV | `7035` | **n** |
| 2625 | 34.6 | 10 | bess | DESIGN_FROZEN_OR_LATER | Land Adj Harmer Warren Quarry | New Forest Energy (formerly Somerl... | New Forest | - | - | 2.5km/400kV | `7143` | y |
| 2626 | 34.6 | 10 | bess | DESIGN_FROZEN_OR_LATER | J3 Business Park - Battery Energy Storage Facility | Forepower Limited | Doncaster | 2023-01-24 | - | 0.4km/132kV | `12920` | y |
| 2627 | 34.6 | 10 | solar | DESIGN_FROZEN_OR_LATER | Dunmow Solar Farm, Chelmsford Road - Solar Farm | Dunmow Solar Limited | Uttlesford | 2024-07-04 | - | 11.0km/132kV | `5733` | **n** |
| 2628 | 34.6 | 3 | bess | PRE_CONSENT | Welton Gathering Centre, Sudbrooke - Battery Storage | Island Gas Limited | West Lindsey | - | - | 0.6km/132kV | `11792` | y |
| 2629 | 34.6 | 3 | bess | PAST_EXPECTED_START | Link Road - Battery Storage | Aldustria Energy Storage | Cornwall | 2022-11-01 | 1399 | 13.2km/400kV | `12112` | y |
| 2630 | 34.6 | 3 | solar | PRE_CONSENT | Hillhouse Quarry, Railway Bridge - Solar Array | Hillhouse Quarry Company Limited | South Ayrshire | - | - | 0.5km/132kV | `15596` | y |
| 2631 | 34.5 | 6 | solar | DESIGN_FROZEN_OR_LATER | West Holcombe | Wessex Solar Energy | Mid Devon | 2015-06-24 | - | 0.8km/400kV | `5255` | y |
| 2632 | 34.5 | 4 | bess | PAST_EXPECTED_START | Whitelaw Brae Wind farm | Thrive Renewables | Scottish Government (S36) | 2017-12-07 | 3189 | 7.4km/275kV | `3317` | y |
| 2633 | 34.5 | 4 | solar | DISTRESSED | Land to the North of Cursey Lane | Good Energy | Tewkesbury | 2016-11-22 | - | 0.5km/132kV | `5510` | **n** |
| 2634 | 34.5 | 4 | solar | DISTRESSED | Royston Solar Farm (Phase 2) | Canadian Solar | South Cambridgeshire | 2014-10-29 | - | 0.6km/132kV | `5989` | **n** |
| 2635 | 34.5 | 4 | solar | PAST_EXPECTED_START | Craigellachie Biomass CHP Plant, Craigellachie- Sola... | EDF Renewables | Moray | 2024-01-04 | 970 | 6.5km/132kV | `13086` | y |
| 2636 | 34.5 | 4 | solar | DESIGN_FROZEN_OR_LATER | Chamber House | Rochdale Metropolitan Borough Coun... | Rochdale | 2020-08-10 | - | 1.0km/275kV | `5284` | **n** |
| 2637 | 34.4 | 2 | solar | DESIGN_FROZEN_OR_LATER | Computacenter Warehouse | Computacenter UK | Welwyn Hatfield | 2019-03-08 | - | 2.8km/132kV | `7290` | y |
| 2638 | 34.4 | 2 | solar | PAST_EXPECTED_START | Sefter Farm, Pagham Road - Solar Panels | Barfoots Of Botley Limited | Arun | 2023-09-04 | 1092 | 8.7km/132kV | `14148` | y |
| 2639 | 34.4 | 7 | solar | DISTRESSED | Land at Mill Farm | TGC Renewables | Charnwood | 2017-08-15 | - | 1.6km/400kV | `5434` | **n** |
| 2640 | 34.3 | 1 | solar | DISTRESSED | Robert McBride Ltd | PerPetum Sun | Rochdale | 2015-04-29 | - | 1.1km/275kV | `5054` | **n** |
| 2641 | 34.3 | 1 | solar | PRE_CONSENT | Swanwick Colliery | Derbyshire County Council | Amber Valley | - | - | 3.4km/132kV | `5539` | y |
| 2642 | 34.3 | 1 | solar | DESIGN_FROZEN_OR_LATER | Whitehall Farm, Llanharry Road - Solar PV Panels | Mccarthy Contractors (Bridgend) Li... | Rhondda Cynon Taf | 2024-09-17 | - | 1.0km/132kV | `14356` | y |
| 2643 | 34.3 | 2 | solar | DESIGN_FROZEN_OR_LATER | Kenyon Way | Private Developer | Salford | 2020-07-24 | - | 1.3km/132kV | `7738` | y |
| 2644 | 34.2 | 20 | solar | DESIGN_FROZEN_OR_LATER | Gorse Lane | Elgin Energy Esco | North Kesteven | 2019-03-29 | - | 0.6km/132kV | `6701` | y |
| 2645 | 34.2 | 20 | solar | PRE_CONSENT | Boxted - Solar Panels | RES Limited | Colchester | - | - | 5.8km/132kV | `12993` | y |
| 2646 | 34.2 | 4 | solar | DISTRESSED | Land at Mansfield Road | Derbyshire County Council | North East Derbyshire | 2016-01-11 | - | 0.2km/132kV | `5378` | **n** |
| 2647 | 34.2 | 4 | solar | DISTRESSED | Amazon - BHX2 | Amazon UK Services / Push Energy | North West Leicestershire | - | - | 1.2km/400kV | `6715` | **n** |
| 2648 | 34.2 | 5 | bess | PAST_EXPECTED_START | Strath Oykel Wind Farm | Energiekontor (UK) Limited | Scottish Government (S36) | 2025-01-08 | 600 | 12.2km/132kV | `12290` | y |
| 2649 | 34.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Little Toms - Solar Farm | PS Renewables | Mid Devon | 2024-06-20 | - | 2.7km/132kV | `13014` | y |
| 2650 | 34.1 | 15 | solar | DISTRESSED | Hendra Barns Solar Farm | Caledon Partners (Smarter Energy S... | Cornwall | 2013-07-08 | - | 0.6km/132kV | `C0435` | **n** |
| 2651 | 34.1 | 15 | solar | DISTRESSED | Lockington Solar Park | Lark Energy | North West Leicestershire | 2015-01-14 | - | 1.4km/400kV | `C3200` | **n** |
| 2652 | 34.1 | 15 | solar | PAST_EXPECTED_START | Burgate Solar Farm | Pathfinder Clean Energy UK Dev Lim... | Broadland | 2021-08-13 | 1844 | 10.0km/132kV | `8221` | y |
| 2653 | 34.1 | 25 | bess | PRE_CONSENT | Corr Chnoc Wind Farm | Galileo Green Energy Scotland Limi... | Scottish Government (S36) | - | - | 16.0km/132kV | `14299` | y |
| 2654 | 34.0 | 2 | solar | DESIGN_FROZEN_OR_LATER | Hoods Close - Solar Panels | Trelleborg Industrial AVS | Leicester | - | - | 2.2km/400kV | `13697` | y |
| 2655 | 33.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Low Farm Solar Farm | Gresham House / Anesco Limited | East Lindsey | 2021-03-29 | - | 0.7km/132kV | `8053` | y |
| 2656 | 33.8 | 1 | solar | DISTRESSED | Court Colman | Solar Energy Farm | Bridgend | 2017-08-31 | - | 1.4km/132kV | `6420` | **n** |
| 2657 | 33.7 | 2 | solar | PAST_EXPECTED_START | Merryfield Lane, Ilton - Solar Farm | Solar South West Limited | Somerset | 2023-12-06 | 999 | 14.2km/132kV | `13545` | y |
| 2658 | 33.7 | 48 | bess | PRE_CONSENT | Classic Marble Showers Site | Engie Developments Ireland | Fermanagh and Omagh | - | - | 39.3km/275kV | `7979` | y |
| 2659 | 33.6 | 10 | bess | DISTRESSED | Pikelaw Place | Green Hedge Energy UK | West Lancashire | 2017-07-25 | - | 1.0km/132kV | `6944` | **n** |
| 2660 | 33.6 | 37 | solar | DISTRESSED | Woolfox Quarry | Renewable Energy Systems (RES) | Rutland | 2016-03-18 | - | 5.6km/400kV | `5016` | **n** |
| 2661 | 33.6 | 3 | solar | DESIGN_FROZEN_OR_LATER | Elmsall Way, South Elmsall - Solar Panels | Next Holdings | Wakefield | 2022-09-15 | - | 1.1km/400kV | `11359` | y |
| 2662 | 33.5 | 28 | solar | DISTRESSED | Friths Farm | Friths Solar Limited | Boston | 2014-10-09 | - | 1.0km/132kV | `C3380` | **n** |
| 2663 | 33.5 | 7 | solar | PRE_CONSENT | Westmill Quarry, Westmill Road - Solar Farm | Biffa Waste Services Limited | East Hertfordshire | - | - | 7.2km/400kV | `13928` | y |
| 2664 | 33.5 | 3 | solar | DESIGN_FROZEN_OR_LATER | Smart Systems Limited, Arnolds Way - Solar Panels | Smart Systems Limited | North Somerset | 2023-10-02 | - | 0.7km/400kV | `14415` | y |
| 2665 | 33.4 | 1 | solar | DESIGN_FROZEN_OR_LATER | B H K UK Davy Drive - Solar Panels | BHK (UK) Limited | County Durham | 2022-07-04 | - | 2.7km/275kV | `10988` | y |
| 2666 | 33.3 | 2 | solar | PRE_CONSENT | Old Wells Road, Stoke St Michael - Solar Panels | John Wainwright & Co Limited | Somerset | - | - | 4.1km/400kV | `17258` | y |
| 2667 | 33.3 | 12 | solar | PRE_CONSENT | Cruxton Farm - Solar Farm | Environmental Asset Management | Dorset | - | - | 3.9km/400kV | `17163` | **n** |
| 2668 | 33.2 | 20 | bess | PRE_CONSENT | Douglas West Wind Farm (extension) | Douglas West Extension / 3R Energy... | Scottish Government (S36) | - | - | 3.4km/132kV | `6826` | y |
| 2669 | 33.2 | 20 | bess | PRE_CONSENT | Knockodhar Wind Farm | REG Knockodhar Limited | Scottish Government (S36) | - | - | 3.4km/275kV | `14295` | y |
| 2670 | 33.2 | 5 | solar | DISTRESSED | Red Brae | Power Capital | Mid and East Antrim | 2015-10-13 | - | 0.6km/275kV | `5205` | **n** |
| 2671 | 33.2 | 5 | solar | DISTRESSED | Broxbournebury Solar Field | Mulbrick Clean Energy | Broxbourne | 2016-02-15 | - | 0.6km/132kV | `5647` | **n** |
| 2672 | 33.2 | 5 | solar | DISTRESSED | Glenhead Farm (Upper) | Environmental Energy Investments | North Lanarkshire | 2016-07-06 | - | 0.5km/275kV | `5909` | **n** |
| 2673 | 33.2 | 5 | solar | DISTRESSED | Fambridge Road/Canewdon Road | UK Solar Assets (Pobail LS-SPV) | Rochford | 2015-04-02 | - | 0.2km/132kV | `6017` | **n** |
| 2674 | 33.2 | 5 | solar | PRE_CONSENT | Land Off Penniment Lane | Global Renewable Construction | Mansfield | - | - | 1.8km/132kV | `6023` | **n** |
| 2675 | 33.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Blenheim Net Zero Estate | Vanburgh Unit Trust | West Oxfordshire | 2021-01-08 | - | 6.2km/132kV | `8070` | y |
| 2676 | 33.2 | 5 | solar | PRE_CONSENT | Castor Bay Water Treatment Works, Castor Bay Road - ... | NI Water | Armagh City, Banbridge and C... | - | - | 14.3km/275kV | `18205` | y |
| 2677 | 33.2 | 12 | solar | DISTRESSED | White Gorse Farm | Green Switch Solutions - Liquidate... | North Kesteven | 2014-11-25 | - | 0.2km/132kV | `C3325` | **n** |
| 2678 | 33.2 | 1 | solar | DESIGN_FROZEN_OR_LATER | Portsmouth International Port - Solar Panels | Portsmouth City Council | Portsmouth | 2023-06-20 | - | 3.6km/132kV | `9236` | y |
| 2679 | 33.2 | 1 | solar | PAST_EXPECTED_START | Park Pale House, Mountfield Lane - Solar Panel Array | Southern Water Services Limited | Rother | 2024-04-04 | 879 | 8.2km/132kV | `15894` | y |
| 2680 | 33.1 | 1 | solar | DESIGN_FROZEN_OR_LATER | Farnborough International Exhibition Centre, Etps Ro... | Farnborough International Limited | Rushmoor | 2024-02-15 | - | 4.2km/132kV | `15581` | y |
| 2681 | 32.8 | 2 | solar | PRE_CONSENT | Morfa Pingett | Richard Thomas Associates | Carmarthenshire | - | - | 2.5km/132kV | `9517` | **n** |
| 2682 | 32.8 | 1 | solar | PAST_EXPECTED_START | Lodge Farm, Boxted Road - Solar Panels | P.G Rix Farms Limited | Colchester | 2024-06-20 | 802 | 7.2km/132kV | `16346` | y |
| 2683 | 32.8 | 6 | bess | DISTRESSED | Land at Calthwaite | Balance Power | Westmorland and Furness | 2018-01-08 | - | 0.3km/132kV | `7094` | **n** |
| 2684 | 32.8 | 6 | bess | PRE_CONSENT | Binn Farm Solar Farm | Trio Power Limited | Perth and Kinross | - | - | 4.9km/132kV | `19595` | y |
| 2685 | 32.8 | 1 | bess | DESIGN_FROZEN_OR_LATER | Carland Cross Wind Farm - Storage | Scottish Power | Cornwall | - | - | 1.7km/132kV | `3976` | y |
| 2686 | 32.6 | 10 | solar | DISTRESSED | Coldham Estate Solar Farm | ScottishPower Renewables | Fenland | 2019-12-17 | - | 2.8km/132kV | `7677` | **n** |
| 2687 | 32.6 | 10 | bess | DESIGN_FROZEN_OR_LATER | Dragonhall Farm, Padanaram - Battery Storage | Ecosse Solar Parks Limited | Angus | - | - | 0.6km/275kV | `9065` | y |
| 2688 | 32.6 | 10 | bess | PRE_CONSENT | Bath Mews, Minsterley - Battery Storage Facility | Hydrock Consultants Limited | Shropshire | - | - | 12.8km/132kV | `13480` | **n** |
| 2689 | 32.6 | 10 | bess | PRE_CONSENT | Larbrax Wind Farm | Orsted Onshore UK Limited | Dumfries and Galloway | - | - | 13.2km/132kV | `15046` | **n** |
| 2690 | 32.6 | 28 | solar | DESIGN_FROZEN_OR_LATER | Bracon Ash Solar | Luminous Energy Ltd | South Norfolk | 2021-12-21 | - | 3.2km/132kV | `8838` | y |
| 2691 | 32.6 | 3 | solar | DESIGN_FROZEN_OR_LATER | Easter Bush | University of Edinburgh (Estates D... | Midlothian | 2021-10-22 | - | 2.8km/400kV | `7222` | y |
| 2692 | 32.5 | 2 | solar | DISTRESSED | Maydwell Avenue | Neame Sutton Ltd | Horsham | 2013-05-31 | - | 4.5km/400kV | `IF1004` | **n** |
| 2693 | 32.5 | 4 | solar | PAST_EXPECTED_START | Quotient Sciences, Taylor Drive - Solar PV Panel Arr... | The Duke of Northumberland Estate | Northumberland | 2023-11-09 | 1026 | 10.5km/400kV | `12457` | y |
| 2694 | 32.4 | 2 | solar | DISTRESSED | Delabole | Good Energy | Cornwall | 2016-02-26 | - | 0.2km/400kV | `5858` | **n** |
| 2695 | 32.4 | 2 | solar | DISTRESSED | Amazon LBA2 (Principal Place) | Amazon UK Services / Push Energy | Doncaster | 2019-03-28 | - | 0.3km/400kV | `6696` | **n** |
| 2696 | 32.4 | 2 | solar | DESIGN_FROZEN_OR_LATER | East Haddon - Solar Photovoltaic System | HW Brown | West Northamptonshire | 2022-09-30 | - | 1.8km/400kV | `11491` | y |
| 2697 | 32.4 | 2 | solar | PAST_EXPECTED_START | Findony Farm, Dunning - Solar Array | Simon Howie Butchers Limited | Perth and Kinross | 2023-01-18 | 1321 | 8.5km/275kV | `12755` | y |
| 2698 | 32.4 | 2 | solar | PRE_CONSENT | Bays Lane, Gurney Slade - Solar Panels | Morris & Perry Limited | Somerset | - | - | 6.0km/132kV | `19769` | y |
| 2699 | 32.2 | 5 | solar | DISTRESSED | Jamesfield Solar Farm | Green Power Consultants | Perth and Kinross | 2015-08-14 | - | 0.5km/132kV | `5471` | **n** |
| 2700 | 32.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Land at Tip Field | BE Renewables | Sefton | 2016-09-23 | - | 1.7km/132kV | `5534` | y |
| 2701 | 32.2 | 5 | solar | DISTRESSED | Llwyndyrys Farm | Luminous Energy | Gwynedd | 2015-11-09 | - | 1.1km/132kV | `5575` | **n** |
| 2702 | 32.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Winterton Landfill Site - Ground Mounted Solar PV Ar... | Infinis Solar Developments Limited | North Lincolnshire | 2021-07-09 | - | 0.4km/400kV | `8857` | y |
| 2703 | 32.2 | 26 | solar | PRE_CONSENT | Redmoor Farm | TGC Renewables | North Yorkshire | 2016-07-25 | - | 6.9km/132kV | `5929` | **n** |
| 2704 | 32.1 | 15 | bess | PRE_CONSENT | Flashbrook Road, Knighton - Solar Farm | Scottish Power Renewables | Stafford | - | - | 10.7km/132kV | `16066` | y |
| 2705 | 32.1 | 2 | solar | DESIGN_FROZEN_OR_LATER | Burges Lane, Stoke St Michael - Solar Array Panels | Hiscox Solar Partnership | Somerset | 2024-01-10 | - | 4.5km/400kV | `14798` | y |
| 2706 | 32.0 | 2 | bess | DISTRESSED | Dc1 Boscombe Road | Amazon UK Services / Push Energy | Central Bedfordshire | - | - | 0.3km/400kV | `6711` | **n** |
| 2707 | 32.0 | 8 | solar | DISTRESSED | Hatherton Lodge | Green Switch Solutions - Liquidate... | Cheshire East | 2016-02-12 | - | 2.5km/132kV | `C3406` | **n** |
| 2708 | 31.9 | 1 | solar | PAST_EXPECTED_START | R And Jm Pace, Church Road - Solar Array | R & J M Place Limited | North Norfolk | 2023-04-28 | 1221 | 17.4km/132kV | `13010` | y |
| 2709 | 31.9 | 40 | bess | DESIGN_FROZEN_OR_LATER | Cumberhead West Wind Farm | 3R Energy Solutions Limited | Scottish Government (S36) | 2021-11-18 | - | 2.1km/400kV | `3328` | y |
| 2710 | 31.9 | 11 | solar | PRE_CONSENT | Shilton Downs Solar Park | Ecotricity / Next Generation | West Oxfordshire | - | - | 5.0km/400kV | `5882` | **n** |
| 2711 | 31.8 | 1 | solar | PRE_CONSENT | Barnham Broom Hotel and Golf Club | Daveney | South Norfolk | - | - | 0.9km/400kV | `8092` | y |
| 2712 | 31.8 | 1 | bess | PRE_CONSENT | J3 Business Park | Car Hill Power | Doncaster | - | - | 0.4km/132kV | `12920` | y |
| 2713 | 31.7 | 13 | solar | DISTRESSED | Tylerfedwen Farm Solar Park | Private Developer | Neath Port Talbot | 2014-07-22 | - | 0.6km/132kV | `B1067` | **n** |
| 2714 | 31.6 | 10 | solar | DESIGN_FROZEN_OR_LATER | Carland Cross - Solar Farm | Scottish Power Limited Payments an... | Cornwall | 2020-05-26 | - | 2.7km/132kV | `1565` | **n** |
| 2715 | 31.6 | 10 | bess | DESIGN_FROZEN_OR_LATER | Slamseys Energy Storage | Gridserve Energy Storage | Braintree | 2017-09-15 | - | 1.1km/132kV | `7000` | y |
| 2716 | 31.6 | 3 | solar | PRE_CONSENT | Langleybury Film Hub | Ralph Trustees Limited | Three Rivers | - | - | 2.8km/132kV | `12762` | y |
| 2717 | 31.5 | 4 | bess | PRE_CONSENT | Station Road, Ardley - Solar Farm & Battery Energy S... | Valencia Waster Management Limited | Cherwell | - | - | 6.4km/132kV | `16001` | y |
| 2718 | 31.4 | 4 | solar | DISTRESSED | Land at Wittering Ford Road | Lark Energy | Peterborough | 2016-01-29 | - | 3.8km/132kV | `7631` | y |
| 2719 | 31.3 | 1 | solar | DISTRESSED | Boscombe Road (Unit DC1) | Amazon UK Services / Push Energy | Central Bedfordshire | - | - | 0.3km/400kV | `6711` | **n** |
| 2720 | 31.2 | 20 | bess | PRE_CONSENT | Grayside Wind Farm | Grayside WF | Scottish Government (S36) | - | - | 8.2km/275kV | `8003` | y |
| 2721 | 31.2 | 20 | bess | PRE_CONSENT | Blackpark Farm | Shires Hamilton | Highland | - | - | 5.1km/132kV | `8105` | y |
| 2722 | 31.2 | 5 | solar | PRE_CONSENT | West Grange Solar Farm | West Grange Solar | Fife | - | - | 2.7km/275kV | `6216` | **n** |
| 2723 | 31.2 | 1 | bess | DISTRESSED | Smithybrook View | Together Housing | North East Derbyshire | 2018-05-24 | - | 1.9km/132kV | `7982` | **n** |
| 2724 | 31.2 | 1 | solar | PAST_EXPECTED_START | Eyemouth Freezers, Toll Bridge Road - Solar Panels | Eyemouth Freezers Limited | Scottish Borders | 2024-04-04 | 879 | 9.7km/132kV | `16051` | y |
| 2725 | 31.1 | 25 | solar | DESIGN_FROZEN_OR_LATER | Twitch Hill, Cheswell Grange Farm - Solar Farm & Bat... | Ethical Power | Telford and Wrekin | 2022-06-29 | - | 5.0km/132kV | `10418` | y |
| 2726 | 31.1 | 5 | solar | DISTRESSED | Berryhill Farm Solar Array | Environmental Energy Investments | North Lanarkshire | 2016-07-13 | - | 0.5km/275kV | `5902` | **n** |
| 2727 | 30.8 | 1 | solar | DESIGN_FROZEN_OR_LATER | Wastewater Treatment Works, Fraserburgh | Scottish Water | Aberdeenshire | 2020-12-15 | - | 1.6km/132kV | `9523` | y |
| 2728 | 30.8 | 6 | solar | DISTRESSED | Land at Moss Farm (North) | TGC Renewables/NESF | Cheshire East | 2016-05-20 | - | 0.4km/132kV | `5939` | **n** |
| 2729 | 30.8 | 6 | bess | DISTRESSED | Coldham Estate Solar Farm | ScottishPower Renewables | Fenland | 2021-12-08 | - | 2.8km/132kV | `7676` | **n** |
| 2730 | 30.8 | 1 | solar | DISTRESSED | Lower Russells Field | Eastleigh Borough Council | Eastleigh | 2014-05-04 | - | 2.8km/132kV | `C2523` | **n** |
| 2731 | 30.8 | 1 | solar | DESIGN_FROZEN_OR_LATER | Former St Michaels Golf Course | Halton Borough Council | Warrington | 2018-04-27 | - | 1.0km/132kV | `6560` | y |
| 2732 | 30.8 | 1 | bess | PAST_EXPECTED_START | Battery Energy Storage System in Ballycastle | HHT Renewables Ltd | Causeway Coast and Glens | 2024-03-20 | 894 | 42.7km/275kV | `15516` | y |
| 2733 | 30.6 | 6 | solar | PRE_CONSENT | Bowhay Farm | Lightsource Renewable Energy | Teignbridge | - | - | 2.9km/400kV | `C1787` | **n** |
| 2734 | 30.6 | 10 | bess | DISTRESSED | Litchlake Farm | Hall Farm Energy | Buckinghamshire | - | - | 5.7km/400kV | `7011` | **n** |
| 2735 | 30.6 | 10 | bess | DISTRESSED | Park Farm | Eco-Economix | Wiltshire | 2018-05-03 | - | 0.5km/132kV | `7983` | **n** |
| 2736 | 30.6 | 8 | bess | DISTRESSED | Coombe Farm | KWTN Solar | Somerset | 2017-10-27 | - | 4.9km/400kV | `4752` | y |
| 2737 | 30.6 | 4 | solar | DISTRESSED | Glenhead Farm Lower Solar Array | Environmental Energy Investments | North Lanarkshire | 2016-07-06 | - | 0.7km/275kV | `5903` | **n** |
| 2738 | 30.5 | 2 | solar | PAST_EXPECTED_START | Sandringham Estate - Solar Array | Royal Sandringham Estate | King's Lynn and West Norfolk | 2024-07-12 | 780 | 10.0km/132kV | `16249` | y |
| 2739 | 30.4 | 21 | solar | DISTRESSED | Chelveston Renewable Energy Park | Wykes Engineering | North Northamptonshire | 2015-06-30 | - | 5.8km/132kV | `5055` | **n** |
| 2740 | 30.3 | 12 | bess | PRE_CONSENT | Castletown - Wind Farm | Wind 2 Limited | Highland | - | - | 6.9km/275kV | `10846` | y |
| 2741 | 30.3 | 2 | solar | DISTRESSED | Land Off Mill Lane | Private Developer | Rushcliffe | 2015-09-18 | - | 0.7km/400kV | `5298` | **n** |
| 2742 | 30.2 | 1 | solar | PAST_EXPECTED_START | Cefn-Y-Maes Farm, Rhydycroesau - Solar Park | Positech Energy Limited | Shropshire | 2022-10-14 | 1417 | 6.0km/132kV | `11860` | y |
| 2743 | 30.2 | 5 | solar | DISTRESSED | Pastures Farm solar park (Gonerby Lane) | Countryside Renewables | South Kesteven | 2015-06-10 | - | 1.7km/400kV | `C1306` | **n** |
| 2744 | 30.2 | 5 | solar | DISTRESSED | Land at New Orchard Farm | Solar Power South | North Somerset | 2015-06-30 | - | 1.0km/400kV | `4741` | **n** |
| 2745 | 30.2 | 5 | solar | DISTRESSED | Land at Moss Farm (South) | TGC Renewables/NESF | Cheshire East | 2016-05-31 | - | 0.3km/132kV | `5329` | **n** |
| 2746 | 30.2 | 5 | solar | DISTRESSED | Castell Ddu Solar Farm | Caledon Partners (Solar Power Park... | Swansea | 2016-01-14 | - | 1.7km/132kV | `5675` | **n** |
| 2747 | 30.2 | 5 | solar | DISTRESSED | Broadfield Farmhouse | British Solar Renewables | Cotswold | 2016-02-24 | - | 0.5km/400kV | `5822` | **n** |
| 2748 | 30.2 | 5 | solar | DISTRESSED | Farm at Lower Polmaise | Stirling Council | Stirling | 2015-10-08 | - | 0.7km/400kV | `5911` | **n** |
| 2749 | 30.2 | 5 | solar | DISTRESSED | Warren Park Solar Farm | Good Energy | Dorset | 2015-12-17 | - | 0.7km/400kV | `5987` | **n** |
| 2750 | 30.2 | 5 | bess | DISTRESSED | Shaws Farm | Capbal | South Lanarkshire | - | - | 4.3km/400kV | `7576` | **n** |
| 2751 | 30.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Dragonhall Farm, Padanaram - Solar Photovoltaic Arra... | Ecosse Solar Parks Limited | Angus | 2021-09-22 | - | 0.6km/275kV | `9066` | y |
| 2752 | 30.2 | 5 | solar | PRE_CONSENT | Bumpstead Hill | Lightsource Renewable Energy | Uttlesford | 2015-11-19 | - | 10.5km/132kV | `14930` | y |
| 2753 | 30.0 | 2 | solar | DESIGN_FROZEN_OR_LATER | Barclays Bank Plc, Radbroke Solar Carport - Solar Pa... | Barclays Plc | Cheshire East | 2022-10-04 | - | 3.3km/132kV | `10809` | y |
| 2754 | 30.0 | 2 | solar | PRE_CONSENT | Spring Gardens - Solar Farm | Calleva Community Energy Limited | West Berkshire | - | - | 7.7km/132kV | `14241` | y |
| 2755 | 30.0 | 11 | solar | DISTRESSED | Hall Farm (Hannington) | Archiception | West Northamptonshire | 2015-07-09 | - | 3.5km/400kV | `C3327` | **n** |
| 2756 | 29.8 | 2 | solar | PAST_EXPECTED_START | Paston Road, Bacton - Solar Photovoltaic Array | Shell UK (Head Office) | North Norfolk | 2022-09-29 | 1432 | 24.9km/132kV | `9350` | y |
| 2757 | 29.6 | 6 | solar | DISTRESSED | Blaen Bowi | Novus Solar Developments | Carmarthenshire | 2012-02-24 | - | 4.9km/132kV | `IF1095` | **n** |
| 2758 | 29.6 | 10 | solar | DISTRESSED | Carey Solar Farm | Elgin Energy EsCo | Perth and Kinross | 2015-11-11 | - | 0.4km/132kV | `5569` | **n** |
| 2759 | 29.6 | 10 | bess | PRE_CONSENT | Balnespick Wind Farm | Fred Olsen Renewables Limited | Scottish Government (S36) | - | - | 6.2km/132kV | `14768` | y |
| 2760 | 29.6 | 4 | solar | DISTRESSED | Sowerby Lodge | Sowerby Solar Solar Ltd | Westmorland and Furness | 2016-02-08 | - | 0.3km/132kV | `5651` | **n** |
| 2761 | 29.6 | 8 | bess | DISTRESSED | Gaywood Farm | AMDC Energy / Balanced Grid Soluti... | Sevenoaks | 2018-03-12 | - | 8.0km/132kV | `7113` | **n** |
| 2762 | 29.6 | 6 | solar | DESIGN_FROZEN_OR_LATER | Wooperton Station, Wooperton - Solar Farm | A&J Scott | Northumberland | 2023-10-05 | - | 2.4km/400kV | `11589` | y |
| 2763 | 29.5 | 2 | solar | DESIGN_FROZEN_OR_LATER | Pattemores Transport (Crewkern) | Pattemores Transport (Crewkerne) | Somerset | - | - | 0.4km/132kV | `7766` | y |
| 2764 | 29.4 | 2 | solar | DISTRESSED | Newnham Farm | Low Carbon Solar (Liquidated) | Isle of Wight | 2011-05-20 | - | 4.0km/132kV | `IF1076` | **n** |
| 2765 | 29.4 | 35 | solar | PRE_CONSENT | Mynydd Maen Solar Farm (Cil-Lonydd) | Cenin Renewables Limited | Welsh Government (NSIP) | - | - | n/a | `17724` | y |
| 2766 | 29.3 | 2 | solar | DISTRESSED | Belle Eau Park | Solar Choice | Newark and Sherwood | 2015-01-13 | - | 2.0km/132kV | `C3454` | **n** |
| 2767 | 29.3 | 4 | solar | PRE_CONSENT | Dunore Road, Aldergrove Solar Farm | NI Water | Antrim and Newtownabbey | - | - | 11.0km/275kV | `8870` | y |
| 2768 | 29.2 | 5 | solar | DISTRESSED | Ashland Solar Farm | Ashland Solar Farm Ltd | Mansfield | 2015-11-18 | - | 2.5km/132kV | `5595` | **n** |
| 2769 | 29.2 | 5 | solar | DISTRESSED | Alton Mead Lane | Brilliant Harvest Installations | Dorset | 2016-01-18 | - | 2.2km/132kV | `5662` | **n** |
| 2770 | 29.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Hownsgill Industrial Park | Project Genesis | County Durham | 2016-03-01 | - | 5.0km/400kV | `5844` | y |
| 2771 | 29.2 | 1 | solar | DISTRESSED | Rhas Fach Farm | Power for Wales Inc | Carmarthenshire | 2015-09-30 | - | 1.9km/400kV | `5517` | **n** |
| 2772 | 29.2 | 1 | solar | PAST_EXPECTED_START | HMP Hollesley - Solar Array | Ministry of Justice | East Suffolk | 2022-02-17 | 1656 | 11.5km/400kV | `10416` | y |
| 2773 | 29.2 | 1 | solar | PAST_EXPECTED_START | Heartsease Farm - Solar Array | Radnor Hills Limited | Powys | 2023-03-13 | 1267 | 18.8km/132kV | `13255` | y |
| 2774 | 29.1 | 2 | solar | DISTRESSED | Kingston Park | Amazon UK Services / Push Energy | Peterborough | - | - | 2.5km/132kV | `6712` | **n** |
| 2775 | 29.0 | 1 | solar | PRE_CONSENT | Winston Farm, Ellesmere Road - Solar Array | S F Jones Limited | Shropshire | - | - | 2.4km/132kV | `13997` | y |
| 2776 | 28.8 | 50 | bess | PRE_CONSENT | Bolfornought Farm Battery Storage Facility | Intelligent Land Investments Group | Stirling | - | - | 42.9km/132kV | `8912` | y |
| 2777 | 28.8 | 1 | solar | DESIGN_FROZEN_OR_LATER | Pinnacle Storage Park, Dale Abbey - Solar PV Panels | Hansteen Property Investments | Erewash | 2022-07-07 | - | 1.2km/132kV | `11017` | y |
| 2778 | 28.7 | 13 | solar | DISTRESSED | Bindwell Lane | NextPower SPV 8 Limited | Somerset | 2021-01-21 | - | 7.5km/132kV | `6563` | **n** |
| 2779 | 28.4 | 2 | bess | PAST_EXPECTED_START | Knocknain Farm, Leswalt - Battery Storage Unit | Knocknain Developments Limited | Dumfries and Galloway | 2023-09-21 | 1075 | 14.0km/132kV | `14032` | y |
| 2780 | 28.4 | 1 | solar | PRE_CONSENT | Horizon, Hurley - Solar Panels | Federated Hermes | Windsor and Maidenhead | - | - | 7.4km/132kV | `12039` | y |
| 2781 | 28.3 | 5 | solar | DISTRESSED | Foel Fawr | Marcol Afan Energy | Bridgend | 2016-04-22 | - | 4.3km/400kV | `C3341` | **n** |
| 2782 | 28.2 | 20 | bess | PRE_CONSENT | Chesters - Millmoor Rig Wind Farm & Battery Energy S... | ESB Asset Development UK Ltd | Scottish Government (S36) | - | - | 18.1km/132kV | `10715` | y |
| 2783 | 28.2 | 3 | solar | DISTRESSED | Knotwood Fields Farm | Global Renewable Construction | West Northamptonshire | 2015-12-17 | - | 4.5km/132kV | `5677` | **n** |
| 2784 | 28.1 | 25 | solar | PRE_CONSENT | Kells Solar Farm | Elgin Energy EsCo | Causeway Coast and Glens | 2016-05-31 | - | 29.8km/275kV | `6012` | y |
| 2785 | 28.0 | 2 | solar | PRE_CONSENT | Clickett Hill Road, Trimley St Mary - Photo Voltaic ... | Uniserve Holdings Limited | East Suffolk | - | - | 12.9km/132kV | `11997` | y |
| 2786 | 27.9 | 14 | bess | PRE_CONSENT | Hopsrig Wind Farm | Muirhall Energy Limited | Scottish Government (S36) | - | - | 5.8km/132kV | `11065` | y |
| 2787 | 27.8 | 6 | bess | DISTRESSED | Aldon Road | STOR Power | Wyre | 2017-12-08 | - | 2.1km/132kV | `7070` | **n** |
| 2788 | 27.8 | 2 | solar | PRE_CONSENT | Smoke Jacks Brickworks, Horsham Road - Ground Mounte... | Wienerberger Limited Head Office | Mole Valley | - | - | 10.3km/132kV | `17873` | y |
| 2789 | 27.8 | 1 | solar | PRE_CONSENT | Higher West Town, Woolsery - Solar Panels | Steve Davey & Partners | Torridge | - | - | 10.0km/400kV | `11782` | y |
| 2790 | 27.8 | 1 | solar | DESIGN_FROZEN_OR_LATER | Lilford Hall, Lilford - Solar Panels | Lilford Hall Estate | North Northamptonshire | - | - | 4.4km/132kV | `12947` | y |
| 2791 | 27.6 | 8 | solar | DESIGN_FROZEN_OR_LATER | Nethermains - Solar Farm | North Ayrshire Council | North Ayrshire | - | - | 4.0km/132kV | `13030` | y |
| 2792 | 27.6 | 3 | bess | DISTRESSED | Brendon Road - Battery Storage | Huntley Wood Investments Limited | Somerset | 2023-03-10 | - | 2.5km/132kV | `9496` | **n** |
| 2793 | 27.5 | 4 | solar | DISTRESSED | Williamthorpe Colliery | Derbyshire County Council | Derbyshire Dales | 2015-12-07 | - | 6.2km/132kV | `5533` | **n** |
| 2794 | 27.4 | 21 | solar | DISTRESSED | Land at Radbrook Pastures | TGC Renewables/NESF | Stratford-on-Avon | 2017-08-10 | - | 15.7km/400kV | `5421` | **n** |
| 2795 | 27.3 | 12 | solar | DISTRESSED | Stour Row Solar Farm | Allied Renewables | Dorset | 2011-08-24 | - | 2.7km/132kV | `6233` | **n** |
| 2796 | 27.2 | 20 | solar | PRE_CONSENT | Solar Farm Development in Antrim | Elgin Energy Esco Limited | Antrim and Newtownabbey | - | - | n/a | `17260` | y |
| 2797 | 27.2 | 5 | solar | DISTRESSED | Knights End Road Solar Farm | Caledon Partners (Solar Power Park... | Fenland | 2015-12-15 | - | 2.6km/132kV | `5374` | **n** |
| 2798 | 27.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | New Road Solar Farm | Solar Century/ Bluefield Solar | South Norfolk | 2015-11-02 | - | 0.2km/132kV | `5543` | y |
| 2799 | 27.2 | 5 | solar | DISTRESSED | Yeorton Hall Farm | Green Energy UK Direct | Cumberland | 2016-05-24 | - | 1.0km/132kV | `5676` | **n** |
| 2800 | 27.2 | 5 | solar | DISTRESSED | Bowscar | Psi Solar | Westmorland and Furness | 2016-06-07 | - | 0.8km/400kV | `5696` | **n** |
| 2801 | 27.2 | 5 | solar | DISTRESSED | Land At Penny Hill Lane | Banks Renewables | Rotherham | 2015-11-20 | - | 2.7km/400kV | `5710` | **n** |
| 2802 | 27.2 | 5 | solar | DISTRESSED | Bowburn | Citrus Durham | County Durham | 2017-02-15 | - | 2.8km/400kV | `6104` | **n** |
| 2803 | 26.8 | 50 | solar | DESIGN_FROZEN_OR_LATER | Crimscote Solar Farm and Storage Project | Regener8 SPV1 Limited | Stratford-on-Avon | 2022-11-29 | - | 18.2km/132kV | `9395` | y |
| 2804 | 26.8 | 2 | solar | DESIGN_FROZEN_OR_LATER | Normandy Barracks | Ministry of Defence | East Riding of Yorkshire | - | - | 4.7km/132kV | `7818` | y |
| 2805 | 26.8 | 1 | bess | PRE_CONSENT | Kip Water Hydro Scheme | Greenock Hydro Power | Inverclyde | - | - | 3.5km/132kV | `7162` | y |
| 2806 | 26.8 | 1 | bess | PAST_EXPECTED_START | Battery Energy Storage System in Broughshane | Heron Energy Limited | Mid and East Antrim | 2024-02-09 | 934 | 15.4km/275kV | `15281` | y |
| 2807 | 26.6 | 10 | bess | PRE_CONSENT | Leithenwater Wind Energy Hub - Wind Farm | Belltown Power Limited | Scottish Government (S36) | - | - | 24.9km/400kV | `16496` | y |
| 2808 | 26.4 | 2 | solar | DISTRESSED | Dunbar Energy Park | Hallhill Developments | East Lothian | 2012-03-07 | - | 3.9km/132kV | `AA526` | **n** |
| 2809 | 26.4 | 2 | solar | DESIGN_FROZEN_OR_LATER | Bruxiehall Farm | Bruxiehill Wind Energy | Aberdeenshire | 2015-11-25 | - | 0.1km/132kV | `5845` | y |
| 2810 | 26.3 | 1 | solar | DISTRESSED | Highwood Farm | Highwood Farm | Rugby | 2016-06-07 | - | 1.4km/132kV | `6097` | **n** |
| 2811 | 26.3 | 4 | bess | PRE_CONSENT | Craig Nab Wind Energy Hub - Wind Farm | Belltown Power Limited | Dumfries and Galloway | - | - | 6.2km/132kV | `12766` | y |
| 2812 | 26.2 | 4 | solar | DISTRESSED | Cleeve Road | Kanes Foods | Wychavon | 2021-03-01 | - | 4.4km/400kV | `6357` | **n** |
| 2813 | 26.2 | 5 | solar | DESIGN_FROZEN_OR_LATER | Lodge Farm Solar Farm | Ecotricity | Somerset | 2011-12-06 | - | 3.7km/400kV | `B0023` | **n** |
| 2814 | 26.2 | 5 | solar | PRE_CONSENT | Ballochmartin | Ramboll Environ UK/Comsol Energy | North Ayrshire | 2017-03-29 | - | 5.7km/400kV | `10437` | **n** |
| 2815 | 26.2 | 26 | solar | DISTRESSED | Redmoor Farm | TGC Renewables | North Yorkshire | 2017-01-27 | - | 6.9km/132kV | `4796` | **n** |
| 2816 | 25.8 | 8 | solar | DISTRESSED | Icklingham Solar Farm | Elveden Farms Ltd | West Suffolk | 2013-08-07 | - | 12.0km/132kV | `C1497` | **n** |
| 2817 | 25.8 | 1 | solar | PAST_EXPECTED_START | Land North of the A11 - Solar Park | Private Developer | Breckland | 2022-10-26 | 1405 | 13.6km/400kV | `10007` | y |
| 2818 | 25.6 | 10 | bess | PRE_CONSENT | Lochend Holding, Barrock - Wind Farm | Constantine Group Limited | Highland | - | - | 14.3km/275kV | `16917` | y |
| 2819 | 25.6 | 10 | bess | PRE_CONSENT | Greentoft, Neven Point, Eday - Wind Turbines & BESS | Green Power (International) Limite... | Orkney Islands | - | - | 85.2km/275kV | `19258` | y |
| 2820 | 25.3 | 12 | bess | PRE_CONSENT | Scawd Law Wind Farm | Fred Olsen Renewables | Scottish Government (S36) | - | - | 16.1km/132kV | `8002` | y |
| 2821 | 25.3 | 1 | solar | PRE_CONSENT | Pennington Wastewater Treatment Works, Milford Road ... | Southern Water | New Forest | - | - | 6.7km/132kV | `13485` | y |
| 2822 | 25.2 | 5 | bess | PAST_EXPECTED_START | Rowan Wind Farm | Energiekontor UK Limited | Scottish Government (S36) | 2024-04-26 | 857 | 51.8km/132kV | `16737` | y |
| 2823 | 25.2 | 1 | solar | DESIGN_FROZEN_OR_LATER | Building ONE | Science Museum Group | Swindon | 2019-06-04 | - | 4.4km/132kV | `7252` | y |
| 2824 | 24.9 | 40 | bess | PRE_CONSENT | Back Fell Wind Farm | E Power Limited | Scottish Government (S36) | - | - | n/a | `14546` | y |
| 2825 | 24.9 | 5 | solar | DISTRESSED | Bascote Road Solar Farm | TGC Renewables | Stratford-on-Avon | 2016-09-05 | - | 5.1km/132kV | `5441` | **n** |
| 2826 | 24.2 | 5 | solar | DISTRESSED | Two Oaks Quarry | Mansfield Sand | Ashfield | 2015-10-15 | - | 3.0km/132kV | `5840` | **n** |
| 2827 | 24.0 | 2 | solar | DISTRESSED | Land Hill Farm | Tealing Solar Parks | Wyre | 2015-11-27 | - | 0.3km/400kV | `5580` | **n** |
| 2828 | 23.9 | 40 | solar | DISTRESSED | RAF Faldingworth | Lunar Energy Power | West Lindsey | 2014-03-31 | - | 10.4km/132kV | `C2228` | **n** |
| 2829 | 23.8 | 30 | bess | PRE_CONSENT | Abhainn Dubh Wind Farm | E Power Limited | Scottish Government (S36) | - | - | 30.9km/132kV | `11357` | y |
| 2830 | 23.7 | 2 | solar | DISTRESSED | Hill of Blairfowl Solar Farm | Green Cat Renewables | Aberdeenshire | 2015-08-07 | - | 4.2km/400kV | `5479` | **n** |
| 2831 | 23.7 | 2 | solar | DISTRESSED | Pistyllgwyn Farm | Power for Wales Inc | Carmarthenshire | 2015-12-21 | - | 1.5km/132kV | `5571` | **n** |
| 2832 | 23.5 | 3 | solar | DISTRESSED | Pant Cefn Farm | Belvedere Energy Developments | Ceredigion | 2016-07-01 | - | 2.0km/132kV | `6053` | **n** |
| 2833 | 23.4 | 2 | bess | DISTRESSED | Sparsholt college | Sparsholt College (formerly Ecotri... | Winchester | 2017-12-20 | - | 6.7km/132kV | `7180` | **n** |
| 2834 | 23.4 | 27 | solar | PRE_CONSENT | Billown Solar Farm | Peel Cubico Renewables Limited | Isle of Man | - | - | 76.5km/400kV | `13930` | y |
| 2835 | 23.2 | 5 | bess | DISTRESSED | Berfern Farm | Capbal | Inverclyde | - | - | 5.5km/132kV | `7033` | **n** |
| 2836 | 23.2 | 1 | solar | DISTRESSED | Prospect Farm | Raw Energy | Buckinghamshire | 2015-06-08 | - | 3.3km/132kV | `5066` | **n** |
| 2837 | 22.6 | 3 | solar | DISTRESSED | Curryfree Wind Farm (co-location) | ESB Solar NI | Derry City and Strabane | 2018-11-21 | - | 11.0km/275kV | `6292` | **n** |
| 2838 | 22.5 | 5 | solar | PRE_CONSENT | La Rue De La Hougue Mauger - Solar Farm | Jersey Electricity Building Servic... | _none_ | - | - | n/a | `17120` | y |
| 2839 | 22.4 | 7 | solar | DISTRESSED | Blaenporth Solar Farm | Juwi Renewable Energies | Ceredigion | 2014-09-03 | - | 12.9km/132kV | `B1296` | **n** |
| 2840 | 22.3 | 1 | solar | PRE_CONSENT | Cefn-Y-Maes Farm, Rhydycroesau - Solar Park | Positech Energy Limited | Shropshire | - | - | 6.0km/132kV | `11859` | y |
| 2841 | 22.2 | 5 | solar | DISTRESSED | Land East of Sandyford | Selettra Holding | Angus | 2015-09-30 | - | 2.6km/275kV | `5464` | **n** |
| 2842 | 20.8 | 1 | solar | DISTRESSED | Drumcairn Road | Private Developer | Armagh City, Banbridge and C... | 2017-02-01 | - | 8.4km/275kV | `6105` | **n** |
| 2843 | 20.8 | 1 | solar | PRE_CONSENT | Stretton Sugwas Solar Farm | Herefordshire New Leaf Cooperative | Herefordshire, County of | - | - | 10.1km/132kV | `6221` | **n** |
| 2844 | 20.8 | 1 | solar | PRE_CONSENT | Shinny Road Macosquin | Northern Farm Partnership | Causeway Coast and Glens | - | - | 25.4km/275kV | `7744` | y |
| 2845 | 20.8 | 1 | solar | PRE_CONSENT | Drum Road, Cookstown - Solar & Battery Development | Numalls Energy Ltd | Mid Ulster | - | - | 15.6km/275kV | `14124` | y |
| 2846 | 20.6 | 4 | solar | DISTRESSED | Carrickatane | ESB Solar NI | Derry City and Strabane | 2018-11-21 | - | 13.4km/275kV | `6325` | **n** |
| 2847 | 20.2 | 5 | solar | DISTRESSED | Town End Farm | RALOS New Energy | Westmorland and Furness | 2016-10-11 | - | 3.4km/132kV | `5699` | **n** |
| 2848 | 20.2 | 5 | bess | PRE_CONSENT | Acheilidh Wind Farm (Previously known as Lairg III) | Energiekontor (UK) Limited | Scottish Government (S36) | - | - | 66.4km/132kV | `11936` | y |
| 2849 | 19.2 | 5 | solar | DISTRESSED | East Culkae Farm | Neo Environmental | Dumfries and Galloway | 2014-12-04 | - | 18.8km/132kV | `C3194` | **n** |
| 2850 | 19.0 | 2 | solar | DISTRESSED | Hill Top Farm | RG and RJ Allen Ltd | Rutland | 2013-11-11 | - | 6.6km/132kV | `C1815` | **n** |
| 2851 | 18.7 | 2 | solar | DESIGN_FROZEN_OR_LATER | Rock Barracks Solar Farm | Public Power Solutions (PPS) | East Suffolk | 2020-12-17 | - | 6.2km/400kV | `7714` | y |
| 2852 | 18.2 | 9 | solar | DISTRESSED | Trecoed Farm | Transition Bro Gwaun | Pembrokeshire | 2022-03-18 | - | 17.0km/132kV | `7187` | **n** |
| 2853 | 18.2 | 5 | solar | DISTRESSED | Cefn Cae For | Vortex (formerly SunEdison) | Isle of Anglesey | 2016-02-11 | - | 8.8km/400kV | `5802` | **n** |
| 2854 | 18.1 | 15 | solar | DISTRESSED | Patrickston Farm | Green Energy International | Stirling | 2020-05-05 | - | 12.3km/400kV | `7785` | **n** |
| 2855 | 16.5 | 2 | solar | DESIGN_FROZEN_OR_LATER | Cnocbreac Inver Estate - Solar Generation | Inver Hydro Limited | Argyll and Bute | 2024-10-28 | - | 30.9km/132kV | `15481` | y |
| 2856 | 14.2 | 5 | solar | DISTRESSED | Jack's Lane Solar | Renewable Energy Systems (RES) | King's Lynn and West Norfolk | 2016-02-11 | - | 11.2km/132kV | `5173` | **n** |
| 2857 | 14.2 | 5 | solar | DISTRESSED | Fen Farm Solar Park (extension) | Ecotricity | East Lindsey | 2016-03-02 | - | 15.7km/132kV | `5758` | **n** |
| 2858 | 13.8 | 1 | solar | DISTRESSED | Skelmonae Farm | Cloffrickford Renewable Energy | Aberdeenshire | 2021-12-01 | - | 5.5km/400kV | `6585` | **n** |
| 2859 | 13.7 | 2 | solar | DISTRESSED | Bluestone Heath Road | Marriages Specialist Foods | East Lindsey | 2015-03-31 | - | 15.9km/132kV | `5023` | **n** |
