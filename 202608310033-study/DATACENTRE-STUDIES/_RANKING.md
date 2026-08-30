# _RANKING — GB data centres held in the repositories, ranked

The demand side, ranked alongside the generation pipeline. **306 studies, one per OSM element** in the
`data-centres-gb` candidate, each in this directory.

Generated **2026-08-31** from data already held. **No Overpass, OSM, planning-register or operator fetch was
performed.**

---

## 1. READ THIS FIRST — what this is *not*

> **This is the BUILT ESTATE. It is not a data-centre project pipeline.**
>
> Of the 306 elements held, **294 are tagged `OPERATIONAL_OR_UNSPECIFIED`** — and in OpenStreetMap that value
> conflates "running" with "nobody tagged it". Only **8 are `PROPOSED`** and **4 are `CONSTRUCTION`**.
>
> **Twelve records is not a pipeline.** The proposed and consented large UK data-centre projects — the ones worth
> tens of billions of pounds of load, the ones fighting for the same grid capacity as every project in
> `PROJECT-STUDIES/_RANKING.md` — **are not in these repositories at all.**
>
> Acquiring them is designed in `_build-plan/DATACENTRES-NEXT/NEXT-VERSION-DATACENTRES.md`. It is the single
> largest data gap found across both overnight sessions.

And a second limit, equally important:

> **Every one of the 306 elements has `name_raw: null`, `operator_raw: null` and `owner_raw: null`.** The candidate
> export carries geometry, a source record id, a lifecycle bucket and licence metadata. Nothing else. Names in this
> ranking were recovered by *proximity* to the pinned V8 `datacentres` layer, which is a different source, and
> **proximity is never identity** under the federation rule. Every recovered name is a candidate label.

---

## 2. What was studied

| source | value |
|---|---|
| producer | `Ventusltd/data-centres-gb`, generation `202608281053` |
| branch | `candidate/202608281053-osm-data-centres` (read via `git show`; not on `main`) |
| artefact | `exports/202608281053-osm-data-centres.geojson`, 214,672 bytes |
| elements | **306** |
| source | OpenStreetMap via **one bounded Overpass request** |
| licence | **ODbL-1.0** |
| attribution | © OpenStreetMap contributors |
| identity rule | `DCGB-OSM-{NODE\|WAY\|RELATION}-{osm_id}` is a **source-record id, not a facility id** |
| company binding | `eligible_for_company_binding: false` on every row; all 612 relationship rows `ABSTAIN` with `VERIFIED_COMPANY_NUMBER_REQUIRED` |

Element composition: **274 ways, 29 nodes, 3 relations.** All are delivered as Points in the export.

Data Center Map is excluded from ingestion because its terms prohibit programmatic retrieval; OpenInfraMap is an
OSM visualisation, not a second source. Both exclusions are the producer's own stated law and are preserved here.

---

## 3. Headline result

| lifecycle as tagged | elements | verdict assigned |
|---|---:|---|
| `OPERATIONAL_OR_UNSPECIFIED` | 294 | BUILT / UNKNOWN STAGE |
| `PROPOSED` | **8** | WATCH — PROPOSED |
| `CONSTRUCTION` | **4** | WATCH — BUILDING |

**Data centres are sited on the grid, and the held data proves it:**

| distance to nearest mapped transmission circuit | elements |
|---|---:|
| ≤ 1 km | **160** |
| 1–2 km | 66 |
| 2–5 km | 71 |
| 5–10 km | 6 |
| > 10 km | 3 |

**226 of 306 (74 %) are within 2 km of a 400 / 275 / 132 kV circuit.** For the generation pipeline that is the
competition for the same nodes; for a cable and connectivity supplier it is the map of where large load already
lives.

**Name recovery** against the pinned V8 `datacentres` layer:

| separation | elements |
|---|---:|
| < 5 m — coincident, almost certainly the same site | **222** |
| 5–50 m | 4 |
| 50–500 m | 24 |
| 0.5–2 km | 20 |
| > 2 km — no usable label | 36 |

**179 elements recovered a usable name.** 62 matched only to a V8 point literally recorded as "Unknown Data
Centre". The remainder stay unnamed. The near-perfect coincidence strongly suggests the V8 layer derives from the
same OpenStreetMap source with tags retained — which means **one supervised Overpass re-read would restore names,
operators and owners to all 306**, at zero identity risk, because it is the same source the producer already used.

---

## 4. Scoring — declared in full

| component | maximum | rule |
|---|---:|---|
| lifecycle | 40 | `PROPOSED` 40 · `CONSTRUCTION` 34 · `OPERATIONAL_OR_UNSPECIFIED` 10 |
| grid exposure | 25 | circuit ≤2 km 20 · ≤5 km 12 · ≤10 km 8 · else 2; **plus 5** if a 275/400 kV substation is within 2 km |
| generation adjacency | 20 | project in FUNDING_WINDOW or PROCURING ≤5 km 20 · ≤15 km 12; any live project ≤5 km 8 · ≤15 km 4 |
| identity recoverable | 10 | a usable candidate name was recovered |

Theoretical maximum **95**. **Capacity is absent from the score because IT load in MW is absent from the data.**
That is the biggest single reason this ranking is weaker than the generation one, and no amount of modelling fixes
it — only operator disclosure or a planning application carries the number.

---

## 5. The pairing shortlist — 18 sites worth a call now

Data centres within 5 km of a generation project inside the inferred funding window or procurement band. This is
where the demand side and the supply side are commercially live **at the same time**.

| score | data centre (candidate label) | km | nearest live project | MW | project state |
|---:|---|---:|---|---:|---|
| 60 | RBS Melville Gate Data Centre | 2.11 | Salters Battery Energy Storage | 200 | PROCURING |
| 60 | AWS Didcot Data Centre | 2.10 | Appleford — Battery Energy Storage | 300 | PROCURING |
| 60 | AWS Didcot Data Centre *(second element)* | 2.09 | Appleford — Battery Energy Storage | 300 | PROCURING |
| 60 | iomart Glasgow Data Centre | 1.93 | Broomloan Road — Battery Energy Storage | 49.9 | PROCURING |
| 60 | British Telecom Computer Centre | 4.08 | Long Lane, Stanwell — Battery Storage | 49.9 | **FUNDING WINDOW** |
| 60 | Fujitsu Data Centre | 0.95 | Tesco, Cygnet View — Solar PV | 1.05 | PROCURING |
| 52 | CityFibre Cabinets | 3.21 | Fairlawns Farm, Chelmsford Road — BESS | 480 | PROCURING |
| 52 | IBM Horsham | 1.46 | Great Oak Energy Hub | 400 | PROCURING |
| 52 | Serverfarm LON1 — London | 0.93 | Long Lane, Stanwell — Battery Storage | 49.9 | **FUNDING WINDOW** |
| 52 | Skyways | 4.02 | Long Lane, Stanwell — Battery Storage | 49.9 | **FUNDING WINDOW** |
| 52 | RBS Data Centre | 4.53 | Cockenzie Battery Storage System | 240 | PROCURING |
| 52 | Digital Realty LHR17 | 3.48 | Long Lane, Stanwell — Battery Storage | 49.9 | **FUNDING WINDOW** |
| 50 | *(unnamed)* `DCGB-OSM-WAY-314914896` | 1.84 | Cooksland Farm, Old Snydale — BESS | 50 | **FUNDING WINDOW** |
| 50 | *(unnamed)* `DCGB-OSM-WAY-558958575` | 0.38 | Queenslaine Farm, Highworth Road | 66 | PROCURING |
| 50 | *(unnamed)* `DCGB-OSM-WAY-57977045` | 0.87 | Cooksland Farm, Old Snydale — BESS | 50 | **FUNDING WINDOW** |
| 50 | *(unnamed)* `DCGB-OSM-WAY-711646220` | 3.19 | Oaks Farm — Solar Farm | 37 | **FUNDING WINDOW** |
| 42 | *(unnamed)* `DCGB-OSM-WAY-194508831` | 3.76 | Long Lane, Stanwell — Battery Storage | 49.9 | **FUNDING WINDOW** |
| 42 | *(unnamed)* `DCGB-OSM-WAY-68167898` | 1.72 | Pitstock Farm — Solar Photovoltaics | 41 | PROCURING |

**The Stanwell / Heathrow cluster stands out.** Five separate data-centre elements — BT, Serverfarm LON1, Skyways,
Digital Realty LHR17 and one unnamed way — all sit within 4.1 km of the same 49.9 MW battery project at Long Lane,
Stanwell, which is in the inferred funding window. One battery, one connection conversation, five potential
counterparties. That is a single account, not five.

**Didcot is the second cluster:** two AWS elements, 2.1 km from a 300 MW battery in the procurement band, with a
400 kV circuit 0.8 km away.

---

## 6. Top-scoring named sites

| score | site (candidate label) | circuit | substation | nearest live project |
|---:|---|---|---|---|
| 60 | RBS Melville Gate Data Centre | 1.22 km / 400 kV | 3.52 km | 2.11 km, PROCURING |
| 60 | AWS Didcot Data Centre | 0.83 km / 400 kV | 0.83 km | 2.10 km, PROCURING |
| 60 | iomart Glasgow Data Centre | 1.38 km / 132 kV | 1.38 km | 1.93 km, PROCURING |
| 60 | British Telecom Computer Centre | 1.04 km / 132 kV | 0.70 km | 4.08 km, FUNDING WINDOW |
| 60 | Fujitsu Data Centre | 0.82 km / 400 kV | 0.10 km | 0.95 km, PROCURING |
| 53 | Hive IT | **0.03 km / 275 kV** | 0.13 km | 3.65 km, DISTRESSED |
| 53 | Hutchison 3G | **0.04 km / 275 kV** | 0.49 km | 0.44 km, PAST_EXPECTED_START |
| 53 | Redcentric Elland Data Centre | **0.07 km / 132 kV** | 0.10 km | 0.24 km, PAST_EXPECTED_START |
| 53 | Stellanor London North | 0.09 km / 132 kV | 0.33 km | 3.44 km, PAST_EXPECTED_START |
| 53 | Netwise | 0.15 km / 400 kV | 0.18 km | 2.35 km, PRE_CONSENT |
| 53 | DataVita DV2 | 0.23 km / 275 kV | 0.21 km | 1.78 km, PAST_EXPECTED_START |
| 53 | Microsoft Newport data centre | 0.43 km / 400 kV | 0.74 km | 2.19 km, PRE_CONSENT |
| 53 | Next Generation Data | 0.73 km / 400 kV | 0.94 km | 2.58 km, PAST_EXPECTED_START |
| 53 | Centerprise International Newport | 0.76 km / 400 kV | 0.98 km | 2.52 km, PAST_EXPECTED_START |
| 53 | IP House London Datacentre | 0.27 km / 132 kV | 0.47 km | 2.01 km, PRE_CONSENT |
| 53 | Vantage Data Centers — CWL1 | 0.79 km / 400 kV | 0.95 km | 2.51 km, PAST_EXPECTED_START |
| 53 | Vantage Data Centers — CWL13 | 0.78 km / 400 kV | 0.78 km | 2.22 km, PAST_EXPECTED_START |
| 53 | Pulsant Edinburgh South Gyle SC-1 | 0.72 km / 275 kV | 0.72 km | 3.36 km, PRE_CONSENT |
| 53 | Equinix LD3 | 1.52 km / 132 kV | 1.48 km | 0.96 km, PAST_EXPECTED_START |

**Newport, South Wales is a third cluster**: Next Generation Data, Vantage CWL1, Vantage CWL13, Microsoft Newport
and Centerprise International all within 1 km of 400 kV, all with live projects 2–3 km away.

---

## 7. The twelve pipeline elements — everything the repositories know

| lifecycle | element | score |
|---|---|---:|
| PROPOSED | `DCGB-OSM-WAY-10708918` | see study |
| PROPOSED | `DCGB-OSM-WAY-37867853` | see study |
| PROPOSED | `DCGB-OSM-WAY-324811964` | 56 |
| PROPOSED | `DCGB-OSM-WAY-326884636` | see study |
| PROPOSED | `DCGB-OSM-WAY-713367718` | 68 |
| PROPOSED | `DCGB-OSM-WAY-1302345665` | see study |
| PROPOSED | `DCGB-OSM-WAY-1542072469` | see study |
| PROPOSED | `DCGB-OSM-WAY-1545372119` | 68 |
| CONSTRUCTION | `DCGB-OSM-WAY-712277377` | see study |
| CONSTRUCTION | `DCGB-OSM-WAY-1460602301` | 62 |
| CONSTRUCTION | `DCGB-OSM-WAY-1460602302` | see study |
| CONSTRUCTION | `DCGB-OSM-WAY-1482180008` | 62 |

**All twelve are unnamed.** The elements the business most needs to know about are precisely the ones carrying the
least information — because a proposed site has no operator tag until someone adds one, and the candidate export
strips tags anyway.

Two of the PROPOSED elements score 77 (top of the whole ranking) on grid exposure plus proximity to a
funding-window project. Neither can be identified from held data. **That is the gap, in one sentence.**

---

## 8. What must be acquired, and why it is worth doing

| missing | why it matters | source that carries it |
|---|---|---|
| **Proposed and consented DC projects** | The entire pipeline. Twelve OSM tags is not it. | LPA planning registers; PlanIt; planning.data.gov.uk; NSIP for the largest |
| **IT load in MW** | Without it a data centre cannot be ranked against a 300 MW battery on any common axis | planning applications; operator disclosures |
| **Names, operators, owners** | 306 elements currently anonymous | one bounded Overpass re-read of the same query already used |
| **Grid connection status** | Who has capacity and who is queuing — the real competition | NESO connection register |
| **Company identity** | Required before any ownership claim, by contract | Companies House, gated on a verified number |

Design for all of these: `_build-plan/DATACENTRES-NEXT/`. Source cards and bounded workflows: `_build-plan/INTEL-WORKFLOWS/`.

---

## 9. How to read the study files

Filenames sort by pipeline stage first, then score:

```
1-proposed-<score>-<slug>.md        the 8 PROPOSED elements
2-construction-<score>-<slug>.md    the 4 CONSTRUCTION elements
3-built-<score>-<slug>.md           the 294 built or untagged elements
```

Each carries: identity as published, name recovery with its separation distance, grid exposure, generation
adjacency, the corporate abstention, the fetch gaps, and a verdict.

---

## 10. Honest summary

The held data-centre estate is **good geometry, no identity, and almost no pipeline**. It is genuinely useful for
three things — showing where large load already sits, showing that 74 % of it is within 2 km of transmission, and
finding the 18 places where a live generation project and an existing data centre are close enough to talk about
together.

It is useless for the thing the business actually wants: *which large data centre projects are coming, where, how
big, and when do they buy.* That answer is not in these repositories and cannot be inferred from what is. It has to
be acquired, deliberately and under the source-card doctrine, and that is what `DATACENTRES-NEXT` designs.
