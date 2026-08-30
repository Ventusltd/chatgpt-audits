# planning.data.gov.uk Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/planning_data_gov_uk.md`.**
> Unblocks the register adapter alongside `planit.md`. Nothing was fetched.

Document type: source-card

Source name: Planning Data platform (planning.data.gov.uk)

Publisher / owner: UK Ministry of Housing, Communities and Local Government

Primary URL: `https://www.planning.data.gov.uk/`

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: **expected Open Government Licence v3.0** for a UK government open-data platform. *Verify on the
platform's own licence page before this card leaves draft.*

Attribution requirement: expected OGL v3.0 attribution naming MHCLG and the platform. *Verify.*

Access method: public HTTPS — entity pages, dataset downloads and a JSON API

API key required: no

Rate limit or access limit: *verify.* Declare a ceiling regardless: **≤ 200 requests per run, concurrency 3, 5 s
timeout, ≤ 1 MB per response, 0 redirects.**

Data type: national planning datasets assembled from local authority sources — entities with stable identifiers,
geographies, and dataset-specific attributes

Update frequency: continuous as authorities publish; dataset-dependent

Field list: `entity`, `reference`, `name`, `dataset`, `organisation-entity`, `start-date`, `end-date`,
`geometry`, plus dataset-specific fields. *Confirm on first run.*

Declared fields: what the platform explicitly publishes per entity

Derived-only fields: this system's `event_type` classification, window-state mapping, and any binding to a
`repd_ref`

Known gaps:
- dataset coverage varies; not every authority publishes every dataset
- the platform models *planning data* broadly (constraints, designations, boundaries) — the
  application-level detail needed for a condition-discharge signal may be thinner than PlanIt's
- **the same fragile join key**: the REPD `planning_application_reference`, frequently empty and
  authority-specific in format

Known failure modes: entity not found, dataset withdrawn or renamed, schema drift, an empty result meaning "not
published here" rather than "does not exist"

Allowed Spider use: **observe and derive.** Corroborate a PlanIt record against an official government platform.
Where the two agree, credibility is unchanged (both are already tier-one); where they disagree, **both claims are
retained and the disagreement is surfaced** — `contradictions_overwrite: false`.

Not-allowed Spider use: inferring a role not explicitly stated; treating absence as evidence; retaining raw HTML

Screening boundary: an entity record is evidence of what the platform publishes. It is not planning advice and
not a decision.

Status: draft

---

## Already wired for this source

`register-ingest.mjs` contains `planning_data: ["planning.data.gov.uk", "OFFICIAL_PLANNING_DATA"]`, domain-pinned
and fixture-gated. `credibility.mjs` assigns `"planning.data.gov.uk": 1`.

**Why two planning sources rather than one.** The register-ingest fixture deliberately includes the *same*
DEVELOPER claim from both `planit` and `planning_data` for the same project (`GG2050-REPD-17494`,
Fixture Project Development Limited, effective 2026-08-01), producing two `CONFIRMED` rows that coexist. That is
the corroboration model working as designed: two independent official sources agreeing is stronger evidence than
one, and the ledger keeps both rather than collapsing them.
