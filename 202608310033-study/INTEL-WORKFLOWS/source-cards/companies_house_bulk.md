# Companies House Bulk Data Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/companies_house_bulk.md`.**
> This source is **already in production use** in `companies` and has no card. Nothing was fetched here.

Document type: source-card

Source name: Companies House bulk data products — Basic Company Data and Accounts Bulk Data

Publisher / owner: Companies House

Primary URL: `https://download.companieshouse.gov.uk/`
- Basic company data index: `.../en_output.html`
- Daily accounts index: `.../en_accountsdata.html`
- Monthly accounts index: `.../en_monthlyaccountsdata.html`

Source-card status: draft

Last checked: **2026-08-07** *(held — the pinned Basic file carries `Last-Modified: Fri, 07 Aug 2026 08:10:19 GMT`)*

Licence: **Open Government Licence v3.0**, recorded in the held download plan with the two caveats quoted in
`companies_house_rest.md`

Attribution requirement: *"Contains public sector information licensed under the Open Government Licence v3.0.
Source: Companies House."* Already used.

Access method: HTTPS file download of ZIP archives

API key required: no

Rate limit or access limit: none published for file downloads. Self-imposed ceilings, already in code:
`MAXIMUM_ARCHIVE_BYTES = 4e9`, `MAXIMUM_TOTAL_BYTES = 12e9`, connect 15 s, read 45 s, and a **hard four-file
plan** re-probed by HTTP HEAD on every run.

Data type: whole-register company snapshot, and bulk electronic accounts in XBRL/iXBRL

Update frequency: Basic Company Data **monthly**; accounts **daily and monthly**

Field list — Basic Company Data, the columns actually read:
`CompanyNumber`, `CompanyName`, `CompanyStatus`, `SICCode.SicText_1..4`, `PreviousName_1..10`, incorporation and
accounts dates, registered address

Declared fields: every column published in the bulk CSV

Derived-only fields: `assets_gte_10m`, `energy_relevant_large_company`, `btm_tags`, `probable_project_spv`,
`repd_name_candidates` and every `evidence_type` — all deterministic derivations, all marked candidate

Known gaps — **and this is the whole reason the REST card exists**:
- **no registered charges** in the Basic product
- **no PSC** in the Basic product
- **no officers** in the Basic product
- **no filing history** in the Basic product
- accounts coverage is limited to electronically filed accounts
- the register records what was filed, not what is true

What the Basic product **does** carry that is directly useful, and is currently unexploited:
`PreviousName_1..10` → **`COMPANY_RENAME`**; `SICCode.SicText_*` diffed between two monthly snapshots →
**`SIC_CHANGE`**; `CompanyStatus` diffed → **`COMPANY_STATUS_CHANGE`** and the whole **distress** trio.
This is **Route A** in `companies-engine.md` §6.7: half the funding vocabulary and all of distress, with **no API
key, no new host and no new privacy surface**.

Known failure modes: monthly URL changes with the publication date; ETag or byte drift against the pinned plan
(**already fails closed** — `fixed_plan()` raises *"The source-pinned Companies House archive closure drifted"*);
zip-bomb risk (**already bounded** by `MAX_TOTAL_EXPANDED_BYTES`, `MAX_COMPRESSION_RATIO`, `MAX_MEMBERS`,
`MAX_NESTING`); a company number format outside `^[A-Z0-9]{8}$`

Allowed Spider use: **observe, derive and distil, in ephemeral runner storage only.** Scan the whole register,
retain only compact keyed tables.

Not-allowed Spider use:
- committing any raw archive or company master — enforced: `raw_archives: 0`, `company_master_files: 0`,
  `raw_company_json_files: 0`
- retaining descriptive columns in a bridge table — `descriptive_edge_columns: 0`
- **retaining a Route A snapshot for any company not bound to a project vehicle** — the minimal per-generation
  projection must be filtered to bound vehicles before it is landed
- publishing to `main`, `data/current/` or Pages — candidate branch only

Screening boundary: bulk company data describes companies, not projects. Every company-to-project edge derived
from it is `CANDIDATE`, role `UNKNOWN`, decision `ABSTAIN`.

Status: draft

---

## Held provenance

The four objects the current checkpoint pins, re-probed by HEAD every run and compared on URL, filename, bytes,
ETag and Last-Modified:

| kind | file | bytes |
|---|---|---:|
| accounts | `Accounts_Monthly_Data-May2026.zip` | 1,975,424,256 |
| accounts | `Accounts_Monthly_Data-June2026.zip` | 2,348,684,884 |
| accounts | `Accounts_Monthly_Data-July2026.zip` | 2,229,763,708 |
| basic | `BasicCompanyDataAsOneFile-2026-08-01.zip` | 493,049,031 |

`EXPECTED_TOTAL_BYTES = 7,046,921,879`. Scan result: **5,695,465 Basic rows scanned, 294,904 companies selected,
39,845 probable project SPVs, 316 tagged `BTM_DATA_CENTRE`.**

**Route A needs exactly one new thing: a second Basic snapshot to diff against.** The repository pins one. The
next monthly publication gives the second, and every rename, SIC change and status change between them becomes
visible with no API key at all.
