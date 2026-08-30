# PlanIt Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/planit.md`.**
> Unblocks the register adapter (`window-intelligence.md` Step 1 / `NEXT-VERSION.md` N6).
> Nothing was fetched. Values marked *verify* must be confirmed on first supervised run.

Document type: source-card

Source name: PlanIt

Publisher / owner: PlanIt (planit.org.uk), an independent aggregator of UK local-authority planning applications

Primary URL: `https://www.planit.org.uk/api/applics/json`

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: *verify.* PlanIt aggregates data published by local planning authorities; the aggregation and the
underlying records may carry different terms. **Under the licence rule in `EXTERNAL_SOURCE_RULES.md`, if the
licence is unclear the Spider may record the uncertainty but must not ingest the source as declared truth.**
Until verified, PlanIt output is **derived**, not declared.

Attribution requirement: *verify.* Expect attribution to PlanIt **and** to the originating planning authority.

Access method: public HTTPS JSON API

API key required: *verify* — believed not required for modest use

Rate limit or access limit: *verify.* Declare a hard ceiling regardless: **≤ 200 requests per run, concurrency 3,
5 s timeout, ≤ 1 MB per response, 0 redirects** — the limits pattern already used by
`pipelinenews/data/news-discovery/202608272130-sector-intelligence-contract.json`.

Data type: local planning applications — reference, authority, address, description, dates, decision, documents

Update frequency: continuous, following authority publication; individual authorities update on their own cadence

Field list: application reference, authority name, address, postcode, description, application type, received
date, validated date, decided date, decision, appeal status, source URL. *Confirm exact names on first run.*

Declared fields: what PlanIt explicitly returns for a queried application reference

Derived-only fields: every classification this system adds — `event_type` (`CONDITION_DISCHARGE_APPLIED`,
`RESERVED_MATTERS_APPROVED`, `COMMENCEMENT_NOTICE` …), the mapping to a window state, and any binding to a
`repd_ref`

Known gaps:
- coverage is not uniform across all UK authorities
- **the join key is fragile**: the REPD spine carries `planning_application_reference`, but it is *frequently
  empty*, and reference formats differ by authority (`CB/25/01098/FULL` is one held example)
- Scotland, Wales and Northern Ireland authority coverage: *verify*
- document-level detail (the actual condition being discharged) may require following a document link — **out of
  scope; retain no document text**

Known failure modes: HTTP 429, authority-side outage, reference not found, reference matched to the wrong
authority, schema drift, an empty result that means "not indexed" rather than "no application"

Allowed Spider use: **observe and derive** — look up an application by the official reference already held on the
spine; emit dated, sourced organisation-role claims and organisation events through the existing
`register-ingest.mjs` module, which already domain-pins `planit.org.uk`.

Not-allowed Spider use:
- treating an application description as an official decision
- inferring a role that the source record does not state explicitly — `role_must_be_explicit_in_source_record: true`
- **guessing a reference.** If `planning_application_reference` is empty, the fetcher must **ABSTAIN** and record
  the abstention. It must never search by name or address to find one.
- retaining raw HTML or document bodies

Screening boundary: a PlanIt record is evidence that an application exists and what the register says about it.
It is not planning advice, and an absent record is not evidence that no application exists.

Status: draft

---

## Already wired for this source

`pipelinenews/archive/202608261547-pipelinenews/attributionv1/modules/register-ingest.mjs` already contains:

```js
planit: ["planit.org.uk", "OFFICIAL_PLANNING_AGGREGATOR"]
```

with `sourceDetails()` rejecting any `evidence_url` whose hostname is not `planit.org.uk` or a subdomain, and
`check_batch6_registers.mjs` asserting that substituting another host throws
`source URL does not match planit policy`. **The adapter exists and is gated. Only the fetcher and this card are
missing.**

Note the credibility already assigned to this domain in
`discoveryv1/modules/credibility.mjs`: `"planit.org.uk": 1` — tier-one, authoritative. That is a strong claim for
an aggregator whose licence is unverified, and it should be reviewed when the licence is confirmed.
