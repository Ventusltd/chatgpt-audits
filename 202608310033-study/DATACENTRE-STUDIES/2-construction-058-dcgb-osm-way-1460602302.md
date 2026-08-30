# DCGB-OSM-WAY-1460602302

**Verdict: WATCH - BUILDING**  |  demand score 58 / 100  |  OSM element `DCGB-OSM-WAY-1460602302`

> Generated 2026-08-31 from data already held in the repositories. No Overpass, OSM, planning-register
> or operator fetch was performed. This is a **built-estate** record, not a project pipeline record.
> Everything marked **inferred** is a derived opinion of this model, never a published fact.

---

## 1. Identity - as published by the source

| field | value |
|---|---|
| source record id | `DCGB-OSM-WAY-1460602302` |
| OSM element | https://www.openstreetmap.org/way/1460602302 |
| coordinates (lat, lon) | 51.6788299, -0.8324093 |
| lifecycle as tagged | **CONSTRUCTION** |
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

The nearest named point in the pinned V8 `datacentres` layer is 7.52 km away, recorded as "Unknown Data Centre".
That is too far, or too generic, to offer even as a candidate label. **This element remains unnamed.**

## 3. Grid exposure - computed from held topology, screening-grade only

| measure | value |
|---|---|
| nearest transmission circuit | 0.66 km at 132 kV |
| nearest substation | 5.47 km |
| that substation, voltage | 33000 / 11000 |
| that substation, name | _unnamed in source_ |

Sitting within 2 km of a 132 kV circuit. For a data centre that is the difference between a
viable large load and a decade in a connection queue. It is the single most commercially relevant fact held about this site.

## 4. Generation adjacency - the pairing that matters

| measure | value |
|---|---|
| nearest live solar or BESS project | 8.89 km |
| that project | Bumpers Farm Phase 2 |
| its capacity | 12 MW |
| its inferred window state | **PAST_EXPECTED_START** |
| its REPD reference | `6282` |

No live generation project close enough for a direct pairing conversation.

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
5. **The planning application behind it** - this element is tagged CONSTRUCTION, so a planning record almost certainly exists. Nothing in the repositories links to it. This is the acquisition gap described in `DATACENTRES-NEXT/`.
6. **The company that owns it** - Companies House number required before any binding, by contract.

## 7. Verdict

**WATCH - BUILDING.** One of only **4** elements tagged `CONSTRUCTION`. Load is arriving here; the connection is already agreed and the generation-pairing conversation is late but not closed.

