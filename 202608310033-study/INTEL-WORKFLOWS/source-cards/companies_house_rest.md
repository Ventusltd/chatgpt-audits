# Companies House REST API Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/companies_house_rest.md`.**
> Unblocks the **funding signal** — charges and corporate PSC changes. Nothing was fetched.
> **A complete, reviewed client for this source already exists in `companies` and is currently used only as a
> credential probe.** This card governs turning it into a bounded reader.

Document type: source-card

Source name: Companies House Public Data API

Publisher / owner: Companies House, an executive agency of the UK Department for Business and Trade

Primary URL: `https://api.company-information.service.gov.uk`

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: **Open Government Licence v3.0**, as recorded verbatim in the held download plan
(`companies/build/python/202608271507-freeze-companies-house-plan.py`), together with two caveats already written
by this federation and worth quoting because they are exactly right:
- *"OGL applies to Crown copyright material; third-party rights and data-protection duties may still apply."*
- *"Companies House records what was filed; it does not verify every filed statement."*

Attribution requirement: *"Contains public sector information licensed under the Open Government Licence v3.0.
Source: Companies House."* Already used in the repository.

Access method: HTTPS REST, HTTP Basic authentication with the API key as the username and an empty password

API key required: **yes** — `COMPANIES_HOUSE_API_KEY`, held as a repository secret, never retained in output

Rate limit or access limit: **600 requests per five-minute window** is the documented public limit; the held
client reads `x-ratelimit-limit`, `x-ratelimit-remain`, `x-ratelimit-reset` and `x-ratelimit-window` from every
response, sleeps for the server-derived delay on HTTP 429, retries once, and **refuses any reset beyond a
five-minute boundary**. *Verify the current published limit; do not hard-code it — the held client already reads
it from the response, which is the correct design.*

Data type: company profile, filing history, registered charges, persons with significant control, officers,
insolvency

Update frequency: continuous, as filings are accepted

Field list (only the endpoints this plan would call):
- `/company/{n}/charges` → `charge_code`, `created_on`, `delivered_on`, `satisfied_on`, `status`,
  `persons_entitled[]`, `classification`
- `/company/{n}/persons-with-significant-control` → `kind` (corporate vs individual), `name` (**corporate only**),
  `notified_on`, `ceased_on`, `natures_of_control`
- `/company/{n}/officers?items_per_page=1` → **`total_results` only** (a count)
- `/company/{n}/filing-history?category=…` → `category`, `date`, `description`, `transaction_id`

Declared fields: what the API returns for a queried company number

Derived-only fields: every mapping into the closed `event_type` vocabulary, the binding of a company to a project,
and any funding-window inference

Known gaps:
- charges are filed by the company; a lender's involvement can predate the filing
- PSC statements can be incomplete or under exemption
- a company number is required to query — **no search-by-project is possible**

Known failure modes: HTTP 429, HTTP 404 on a dissolved or invalid number, key revoked, schema drift, a charge with
an empty `persons_entitled`

Allowed Spider use: **observe and derive, for bound project vehicles only.** Retain only the twelve columns
defined in `companies-engine.md` §6.4.

Not-allowed Spider use — **the load-bearing section of this card**:
- **no director names, ever.** `/officers` may be read for `total_results` only, and the emitted event is
  `DIRECTOR_APPOINTMENT_COUNT_CHANGE` carrying a number.
- **no individual PSC identity, ever.** Corporate PSCs may be named as organisations
  (`PSC_CORPORATE_CHANGE`); individual PSCs may contribute only a count delta
  (`PSC_INDIVIDUAL_COUNT_CHANGE`). No name, no date of birth, no nationality, no address.
- no residential or correspondence addresses
- no credit, bankability or risk score — forbidden by the `companies` README
- **no querying a company that is not bound to a project.** The gate is `unbound_vehicle_rows: 0`; this is what
  stops the projection becoming general company surveillance.
- no retention of any response body beyond the declared columns
- **no inference of financial close from a charge alone** —
  `financial_close_inferred_from_charge_alone: false`, already asserted by `check_batch5_attribution.mjs`

Screening boundary: a Companies House record is evidence of **what was filed, and when**. It is not evidence that
the filed statement is true, and it is never evidence about a person.

Status: draft

---

## What already exists, and what this card would change

`optional_rest_evidence()` in `companies/build/python/202608271507-freeze-companies-house-plan.py` is a complete
client: TLS, Basic auth from the environment, `Accept-Encoding: identity`, `Connection: close`, a 1 MB response
ceiling, 429 handling with a server-derived delay and a five-minute refusal boundary, and a retention rule that
keeps only the status and the rate-limit headers. It writes
`evidence/rest-api.json` with `{enabled, status, reason}` and nothing else, and the verifier pins that file by
sha256.

**The transport, the auth, the backoff and the retention discipline are already built and reviewed.** What this
card authorises is narrow: reading four endpoints, for bound vehicles only, into twelve columns.

That is a change of *scope*, not of *capability* — and it must land as a **new timestamped generation with its own
contract**, never as an edit to `202608281337`.
