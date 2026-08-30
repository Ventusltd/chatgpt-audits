# REPD Source Card — COMPLETED DRAFT

> **DRAFT — for review, then it replaces `spiders/docs/sources/repd.md`.**
> **PRIORITY 1: REPD is the spine of the entire product and its existing card records
> `Licence: study required` with `Last checked: unknown`.** That is the largest unstudied dependency in the
> federation.
> Nothing was fetched in this session. Every field below is either **evidenced from a repository artefact**
> (marked *held*) or flagged *verify on first supervised run*.

Document type: source-card

Source name: Renewable Energy Planning Database (REPD)

Publisher / owner: UK Department for Energy Security and Net Zero (DESNZ)

Primary URL *(held — recorded in `gridatlas/data/repd_v9_manifest_202608290716.json`)*:
`https://assets.publishing.service.gov.uk/media/6a6cbdc00c36759b5ccaa305/REPD_Publication_Q2_2026.csv`
Landing page and quarterly index: *verify — the manifest records only the asset URL, not the publication page.*

Source-card status: **draft → should become `approved-for-declared-reference`**

Last checked: **2026-08-03** *(held — the manifest records `source.published: "2026-08-03"`)*

Licence: **Open Government Licence v3.0 is the expected licence** for a DESNZ statistical publication of this
kind. *Verify against the publication page before this card leaves draft — the current card says "study required"
and this must not be replaced by an assumption.*

Attribution requirement: expected OGL v3.0 form —
*"Contains public sector information licensed under the Open Government Licence v3.0. Source: DESNZ Renewable
Energy Planning Database."* The `companies` repository already carries the exactly equivalent Companies House
wording in its download plan, including a `rights_caveat` and an `accuracy_caveat`; **mirror that pattern.**
*Verify wording.*

Access method: quarterly CSV download over HTTPS from `assets.publishing.service.gov.uk`

API key required: no

Rate limit or access limit: none known for a single quarterly file download. Ceiling to declare: **one file per
quarter**, ~5 MB.

Data type: planning and development records for UK renewable electricity projects — one row per REPD record,
carrying reference, name, technology, capacity, planning status, dates, operator/applicant, address, postcode and
administrative geography

Update frequency: **quarterly**. The held extract is **Q2 2026**, published 2026-08-03.

Field list *(held — the 23 typed columns compiled into `repd_projects_202608290716.parquet`)*:
`repd_ref, name, repd_address_raw, repd_address_display, repd_postcode_raw, repd_postcode, postcode_valid,
county, region, country, planning_authority, planning_application_reference, repd_operator_or_applicant,
applicant_publication_state, technology, repd_technology, status, capacity_mw, longitude, latitude,
source_record_updated, source_row, source_row_sha256`

Plus, in the governance spine derivation: `planning_application_submitted`, `planning_permission_granted`,
`planning_permission_refused`, `planning_application_withdrawn`, `planning_permission_expired`,
`under_construction`, `operational`, `easting`, `northing`, `coordinate_source`, `geometry_status`.

Declared fields: every column published in the REPD CSV and its metadata

Derived-only fields: **everything this system adds** — `lifecycle`, `gg_project_id`, `technology` normalisation,
the eight-state window model, `freeze_estimate_at`, `window_score`, grid proximity, SPV name-binding strength.
All are derived and must be labelled as such wherever displayed.

Known gaps *(all held, all measured)*:
- **1,729 records have their applicant withheld** as possible individuals (`possible_individual_applicants_withheld`)
- **28 of the 7,680 spine projects have no geometry** (`geometry_status: missing`)
- **1,564 of 11,069 records have no postcode**; a further 445 have an invalid one
- `planning_application_reference` is **frequently empty**, which blocks any register lookup
- **no parish, ward or LSOA field exists** — see `questions.md` Q3
- the register **lags reality**: `under_construction` is often unrecorded for projects that have started

Known failure modes:
- the quarterly URL changes each publication; the asset path is opaque and must be rediscovered
- **reference-space instability, measured in this workspace and serious:** the two derivations in this federation
  do not agree what a `repd_ref` is. The GridAtlas Parquet holds 11,069 unique, all-numeric references; the
  PipelineNews spine holds 7,515 unique references over 7,680 rows, of which **2,516 are alphanumeric legacy
  references** (`01006W5`) and **154 references appear more than once, on genuinely different projects**. Only
  3,670 references exist in both. Full detail: `PROJECT-STUDIES/_RANKING.md` section 5.
- capacity can differ between derivations for the same named project (East Pye Solar Farm: 500.0 MW under one
  reference, 0.0 MW under another, in the same GridAtlas registry)
- status vocabulary is broad (14 values observed) and mixes decision outcomes with lifecycle stages

Allowed Spider use: as the **frozen, hash-pinned spine** of the product. Declared reference for project identity,
capacity, technology, status, dates and location. Geospatial joins and derived mapping, marked derived.

Not-allowed Spider use:
- treating a derived status inference as an official planning decision
- publishing a withheld applicant name
- treating `repd_ref` as a unique project key **until the reference-space defect above is reconciled**
- presenting the quarterly extract as real-time

Screening boundary: REPD records what was submitted to and decided by planning authorities, as collated
quarterly. It is not a live register, it is not a connection register, and it is not evidence of construction
activity.

Status: draft

---

## Held provenance — everything already pinned in the repositories

| artefact | value |
|---|---|
| source CSV sha256 | `84c1b5f958a934d8b4b86ec88f50bdcf43830ded7ff2efc27bffca0c98695035` |
| source CSV bytes | 5,087,389 |
| published | 2026-08-03 |
| source workbook sha256 (spine build) | `99ec4d0509a9fdfb999116e33c459084ce9ab59b44e3fafba5fc9b280ae2d5a6` |
| source record count (spine build) | 14,657 |
| GridAtlas Parquet | 11,069 rows, sha256 `174040c37f3d63742d6fdd7af722a8cfdf3fb53de3ff85ff1142d22fdac4866b` |
| governance spine | 7,680 rows at ≥ 1 MW, `projects_sha256 24484ca837ac56520ba971fb2c2c1d29620e16a3c71bbaa5764e94c9b515ad52` |
| V8 oracle cross-check | 10,610 of 10,784 features matched by name and rounded coordinate — 98.39 % |

**The provenance discipline is already excellent. Only the licence field is missing, and it is the one field that
determines whether any of it may be published.**
