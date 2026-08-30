# IBM Horsham

**Verdict: BUILT / UNKNOWN STAGE**  |  demand score 52 / 100  |  OSM element `DCGB-OSM-WAY-128487593`

> Generated 2026-08-31 from data already held in the repositories. No Overpass, OSM, planning-register
> or operator fetch was performed. This is a **built-estate** record, not a project pipeline record.
> Everything marked **inferred** is a derived opinion of this model, never a published fact.

---

## 1. Identity - as published by the source

| field | value |
|---|---|
| source record id | `DCGB-OSM-WAY-128487593` |
| OSM element | https://www.openstreetmap.org/way/128487593 |
| coordinates (lat, lon) | 51.0215574, -0.350469 |
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
element: **IBM Horsham**.

At that separation the two records are almost certainly the same site - the V8 layer appears to derive from the
same OpenStreetMap source with names retained. **But proximity never establishes identity** under the federation
rule (`coordinates_are_identity: false`), so this name is offered as a **candidate label**, not as a fact about
this element. Confirming it requires re-reading the OSM tags, which needs a supervised Overpass fetch.

## 3. Grid exposure - computed from held topology, screening-grade only

| measure | value |
|---|---|
| nearest transmission circuit | 2.48 km at 400 kV |
| nearest substation | 0.72 km |
| that substation, voltage | 33000 / 11000 |
| that substation, name | Southwater Primary Substation |

Within 2.48 km of a 400 kV circuit - a workable connection distance for a load of this kind.

## 4. Generation adjacency - the pairing that matters

| measure | value |
|---|---|
| nearest live solar or BESS project | 1.46 km |
| that project | Great Oak Energy Hub |
| its capacity | 400 MW |
| its inferred window state | **PROCURING_INFERRED** |
| its REPD reference | `17245` |

**This is the high-value case.** A live generation project inside the inferred commercial window sits within
1.46 km of this load. Private-wire, co-location and behind-the-meter conversations are live *now*, and the
generation side is at the exact point where studies and cable design are being bought.

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

