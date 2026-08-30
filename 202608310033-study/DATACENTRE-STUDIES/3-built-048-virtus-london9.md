# VIRTUS LONDON9

**Verdict: BUILT / UNKNOWN STAGE**  |  demand score 48 / 100  |  OSM element `DCGB-OSM-WAY-787209399`

> Generated 2026-08-31 from data already held in the repositories. No Overpass, OSM, planning-register
> or operator fetch was performed. This is a **built-estate** record, not a project pipeline record.
> Everything marked **inferred** is a derived opinion of this model, never a published fact.

---

## 1. Identity - as published by the source

| field | value |
|---|---|
| source record id | `DCGB-OSM-WAY-787209399` |
| OSM element | https://www.openstreetmap.org/way/787209399 |
| coordinates (lat, lon) | 51.5188766, -0.6189915 |
| lifecycle as tagged | **OPERATIONAL_OR_UNSPECIFIED** |
| facility identity status | `SOURCE_ELEMENT_ONLY` |
| name in the OSM candidate export | **null** - the export carries no name |
| operator in the OSM candidate export | **null** |
| owner in the OSM candidate export | **null** |
| eligible for company binding | **false** |
| licence | ODbL-1.0 |
| attribution | (c) OpenStreetMap contributors |

**`SOURCE_ELEMENT_ONLY` means what it says.** One OSM element is not one facility. Buildings and campuses are
not merged by the producer, deliberately, so two rows may describe one site and one row may describe part of a
site. Nothing here asserts a facility identity.

## 2. Name recovery - cross-source proximity, NOT identity

The pinned V8 `datacentres` layer in `data-gridatlas` carries a named point **0 m** from this
element: **VIRTUS LONDON9**.

At that separation the two records are almost certainly the same site - the V8 layer appears to derive from the
same OpenStreetMap source with names retained. **But proximity never establishes identity** under the federation
rule (`coordinates_are_identity: false`), so this name is offered as a **candidate label**, not as a fact about
this element. Confirming it requires re-reading the OSM tags, which needs a supervised Overpass fetch.

## 3. Grid exposure - computed from held topology, screening-grade only

| measure | value |
|---|---|
| nearest transmission circuit | 0.10 km at 132 kV |
| nearest substation | 0.14 km |
| that substation, voltage | 33000 |
| that substation, name | _unnamed in source_ |

Sitting within 2 km of a 132 kV circuit. For a data centre that is the difference between a
viable large load and a decade in a connection queue. It is the single most commercially relevant fact held about this site.

## 4. Generation adjacency - the pairing that matters

| measure | value |
|---|---|
| nearest live solar or BESS project | 3.44 km |
| that project | Wexham Park Hospital, Wexham Street - Solar PV Panels |
| its capacity | 1.59 MW |
| its inferred window state | **PAST_EXPECTED_START** |
| its REPD reference | `19938` |

A live generation project is close, but it is not in the commercial window (PAST_EXPECTED_START). Note the adjacency and
re-check when that project moves state.

## 5. Corporate evidence already held

**None, by design.** The producer emits `eligible_for_company_binding: false` and
`abstention_reason: VERIFIED_COMPANY_NUMBER_REQUIRED` for every one of the 612 relationship rows in the
`data-centres-gb` candidate. No operator, owner or company number is asserted anywhere.

The only company-side evidence held that touches this sector is aggregate: the `companies` candidate report
records **316 companies tagged `BTM_DATA_CENTRE`** (SIC 63110) out of 294,904 selected. That is a population,
not a link to this site.

## 6. What cannot be determined without a live fetch

1. **Name, operator and owner** - stripped from the candidate export. One bounded Overpass re-read recovers the tags.
2. **IT load in MW** - not in OSM, not in the repositories, and the single most important missing number. Only operator disclosure or a planning application carries it.
3. **Whether this element is one facility** - `SOURCE_ELEMENT_ONLY`. Merging buildings into campuses needs a deliberate, evidenced rule.
4. **Grid connection status and contracted capacity** - nothing held answers this; it needs the NESO connection register.
5. **Any expansion or new-build application at this site** - a built site is also a pipeline site if it is expanding. Nothing held would show that.
6. **The company that owns it** - Companies House number required before any binding, by contract.

## 7. Verdict

**BUILT / UNKNOWN STAGE.** Tagged `OPERATIONAL_OR_UNSPECIFIED`, which in OSM conflates "running" with "untagged". Demand-side value is retrofit, expansion and co-location, not new connection.

