# DCGB-OSM-WAY-37867853

**Verdict: WATCH - PROPOSED**  |  demand score 77 / 100  |  OSM element `DCGB-OSM-WAY-37867853`

> Generated 2026-08-31 from data already held in the repositories. No Overpass, OSM, planning-register
> or operator fetch was performed. This is a **built-estate** record, not a project pipeline record.
> Everything marked **inferred** is a derived opinion of this model, never a published fact.

---

## 1. Identity - as published by the source

| field | value |
|---|---|
| source record id | `DCGB-OSM-WAY-37867853` |
| OSM element | https://www.openstreetmap.org/way/37867853 |
| coordinates (lat, lon) | 51.5033505, -0.4124311 |
| lifecycle as tagged | **PROPOSED** |
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

The nearest named point in the pinned V8 `datacentres` layer is 0.95 km away, recorded as "VIRTUS LONDON2".
That is too far, or too generic, to offer even as a candidate label. **This element remains unnamed.**

## 3. Grid exposure - computed from held topology, screening-grade only

| measure | value |
|---|---|
| nearest transmission circuit | 0.40 km at 275 kV |
| nearest substation | 0.40 km |
| that substation, voltage | 275000 / 66000 |
| that substation, name | North Hyde Substation |

Sitting within 2 km of a 275 kV circuit. For a data centre that is the difference between a
viable large load and a decade in a connection queue. It is the single most commercially relevant fact held about this site.

## 4. Generation adjacency - the pairing that matters

| measure | value |
|---|---|
| nearest live solar or BESS project | 6.95 km |
| that project | Long Lane, Stanwell - Battery Energy Storage |
| its capacity | 49.9 MW |
| its inferred window state | **FUNDING_WINDOW_INFERRED** |
| its REPD reference | `13133` |

A live generation project inside the inferred commercial window sits 6.95 km away. Too far for a private wire
without a substantial route, but close enough to matter for grid-capacity competition at the same nodes.

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
5. **The planning application behind it** - this element is tagged PROPOSED, so a planning record almost certainly exists. Nothing in the repositories links to it. This is the acquisition gap described in `DATACENTRES-NEXT/`.
6. **The company that owns it** - Companies House number required before any binding, by contract.

## 7. Verdict

**WATCH - PROPOSED.** One of only **8** elements in the whole held estate tagged `PROPOSED`. This is as close as the repositories currently get to a data-centre pipeline, and it is almost nothing. Acquiring the real proposed-and-consented pipeline is the priority described in `DATACENTRES-NEXT/NEXT-VERSION-DATACENTRES.md`.

