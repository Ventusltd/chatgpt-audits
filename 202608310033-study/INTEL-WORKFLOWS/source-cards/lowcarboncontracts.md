# Low Carbon Contracts Company (LCCC) Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/lowcarboncontracts.md`.**
> Completes the register adapter's five-source set. Nothing was fetched.

Document type: source-card

Source name: Low Carbon Contracts Company — CfD register and contract data

Publisher / owner: Low Carbon Contracts Company Ltd (LCCC), the government-owned CfD counterparty

Primary URL: `https://www.lowcarboncontracts.uk/`

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: *verify.* LCCC publishes contract and settlement data as a public counterparty; re-use terms must be
read from the site.

Attribution requirement: attribution to LCCC. *Verify wording.*

Access method: public HTTPS — published registers, data downloads and dashboards

API key required: *verify* — believed not required for published registers

Rate limit or access limit: *verify.* Declare a ceiling: **≤ 50 requests per run, concurrency 2, 5 s timeout,
≤ 1 MB per response, 0 redirects.** Prefer a single register download over per-project queries.

Data type: Contracts for Difference register — CfD holder, technology, capacity, delivery year, strike price,
milestone dates and contract status

Update frequency: on allocation-round outcomes and contract events; register refreshed periodically

Field list: *verify.* Expect CfD unit name, counterparty name, technology, installed capacity, delivery year,
contract start, milestone delivery date, status.

Declared fields: what the register explicitly publishes

Derived-only fields: the binding of a CfD unit to a `repd_ref`, and any inference from a milestone date

Known gaps:
- **CfD covers a minority of this product's pipeline.** The live solar and BESS population studied in
  `PROJECT-STUDIES/_RANKING.md` is overwhelmingly merchant and route-to-market driven, not CfD-supported. BESS is
  not CfD-eligible at all. **Expect this source to bind to very few of the 2,859 studied projects.**
- CfD unit naming does not match REPD project naming
- no `repd_ref` in the register

Known failure modes: register restructured between allocation rounds, unit renamed on transfer, download URL
changes, name-only matching producing false candidates

Allowed Spider use: **observe and derive.** Where a CfD contract is explicitly held by an organisation for a named
unit, emit an `OWNER` role claim through the existing adapter, `CONFIRMED` at credibility 1. A CfD milestone
delivery date is genuine `PROCURING`-class evidence: it is a contractual commitment to deliver by a date.

Not-allowed Spider use: inferring a role the register does not state; treating a strike price or delivery year as
a construction programme; name-matching a CfD unit to a project without corroboration

Screening boundary: the CfD register states contractual facts between LCCC and a counterparty. It is not a
construction schedule.

Status: draft

---

## Already wired, and a note on where the value actually is

`register-ingest.mjs`: `lccc: ["lowcarboncontracts.uk", "OFFICIAL_CFD_REGISTER"]`, domain-pinned.
`credibility.mjs`: `"lowcarboncontracts.uk": 1`.

**Sequencing advice.** Of the five domain-pinned register sources, this one should be built **last**. The measured
population it can serve is small — CfD is largely irrelevant to a pipeline that is 130 BESS projects and 49 solar
projects in the inferred funding window — while PlanIt, planning.data.gov.uk and The Gazette serve the whole
population. Build breadth first.

Its value is not volume, it is **certainty**: a CfD contract is the least ambiguous evidence of commitment
available anywhere in this source set. For the handful of large solar projects it does cover, it is worth more
than any other single record.
