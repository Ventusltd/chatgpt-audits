# The Gazette Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/thegazette.md`.**
> Unblocks the **distress** path, which is the highest-precedence branch of the eight-state model.
> Nothing was fetched.

Document type: source-card

Source name: The Gazette (London, Edinburgh and Belfast Gazettes) — the UK official public record

Publisher / owner: The National Archives, published by APS Group on behalf of HM Government

Primary URL: `https://www.thegazette.co.uk/`

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: Gazette content is Crown copyright; the site publishes data under terms that generally permit re-use
with attribution, and provides structured feeds. *Verify the exact re-use terms and whether the data-service terms
differ from the website terms.*

Attribution requirement: Crown copyright acknowledgement naming The Gazette. *Verify wording.*

Access method: public HTTPS — Atom/JSON feeds and a search API over statutory notices

API key required: *verify* — believed not required for public notice search

Rate limit or access limit: *verify.* Declare a ceiling regardless: **≤ 100 requests per run, concurrency 2, 5 s
timeout, ≤ 1 MB per response, 0 redirects.**

Data type: statutory notices — insolvency (administration, liquidation, receivership), company strike-off,
personal insolvency, wills and probate, and state notices

Update frequency: continuous, several times daily on business days

Field list: notice id, notice code and type, publication date, notice text, and where present the company name
and company number. *Confirm on first run.*

Declared fields: the notice as published, its type, its date, and the company it names

Derived-only fields: this system's mapping of a notice type to
`ADMINISTRATION` / `LIQUIDATION` / `STRIKE_OFF_PROPOSED` / `STRIKE_OFF_DISCONTINUED`, and any binding of the named
company to a project vehicle

Known gaps:
- a notice names a **company**, not a project. The link to a project runs through the vehicle binding, which is
  `ABSTAIN` by default
- personal insolvency notices name **individuals** and are entirely out of scope
- timing: a notice is published after the event, not before

Known failure modes: feed outage, notice text format variation, a company named without a company number, schema
drift, an ambiguous company name

Allowed Spider use: **observe and derive.** Detect a statutory insolvency or strike-off event against a company
number already bound to a project vehicle, and emit an **organisation event**.

Not-allowed Spider use:
- **inventing a delivery role from a notice.** This is already enforced in code:
  `gazette_notice_is_organisation_event_not_delivery_role: true`, and
  `check_batch6_registers.mjs` asserts that no emitted role carries `evidence_kind: OFFICIAL_STATUTORY_NOTICE`.
- ingesting **personal insolvency** notices, or any notice naming a natural person. The person-key guard in
  `attribution-ledger.mjs` would throw, and it must never be relaxed to accommodate this source.
- asserting that a project has failed because its named developer has. A parent's insolvency is evidence about the
  parent.

Screening boundary: a Gazette notice is authoritative evidence that a statutory event was published about a named
company on a date. Everything downstream of that — what it means for a project — is inference.

Status: draft

---

## Already wired for this source

`register-ingest.mjs` contains `gazette: ["thegazette.co.uk", "OFFICIAL_STATUTORY_NOTICE"]` and routes gazette
records down a **separate branch** that produces `organisation_events`, never `roles`:

```js
if (record.source_type === "gazette") {
  organisationEvents.push(normaliseOrganisationEvent(record, details));
  continue;
}
```

`credibility.mjs` assigns `"thegazette.co.uk": 1`.

**This is the single most valuable unbuilt fetcher in the plan.** Under the evidence-order state machine
(`window-intelligence.md` §12.1) `DISTRESSED` is checked first and overrides everything, and it is the one alert
that saves money rather than making it: *stop selling to this developer.* It also needs no design-freeze
calibration, no funding model and no capacity estimate — only a company number and a notice.
