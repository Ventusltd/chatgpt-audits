# companies-engine

How `Ventusltd/companies` fetches and serves today, its exact schema and query surface, and the design of a
**narrow, separate project-vehicle projection** kept distinct from the private balance-sheet view — with the join
keys to `pipelinenews` and `gridatlas` named precisely.

Drafts and instructions only. Nothing here was installed and nothing in the repository was changed.

---

## 1. What the repository is, in one line

Ephemeral GitHub Actions compute scans pinned Companies House **bulk** files inside a runner and retains only compact
cross-repository relationship tables plus an aggregate report. No raw archive, no company master, no personal data,
and nothing on `main` or Pages.

Current recovery checkpoint: **`202608281337`**, resuming acquisition generation **`202608272155`**.
Publication target: candidate branch `candidate/202608272155-compact`, path `data/candidates/202608272155-compact/`.
`promotion_eligible: false`. `stable_path_must_change: false`. `pages_must_change: false`.

---

## 2. How it fetches

### 2.1 Two acquisition paths, both bulk

`build/python/202608262245-companies-house-source.py` is the general acquirer:

| Page | URL | Used for |
|---|---|---|
| Basic company data | `https://download.companieshouse.gov.uk/en_output.html` | `BasicCompanyData*.zip` — company number, name, status, SIC 1–4, addresses |
| Daily accounts | `https://download.companieshouse.gov.uk/en_accountsdata.html` | `Accounts_Bulk_Data-*.zip` |
| Monthly accounts | `https://download.companieshouse.gov.uk/en_monthlyaccountsdata.html` | `Accounts_Monthly_Data-<Month><Year>.zip` |

Rules enforced in code:

- `download()` rejects any URL whose scheme is not `https` or whose hostname is not `download.companieshouse.gov.uk`
- streams in 1 MB chunks, hashing as it goes; refuses anything under 1,024 bytes
- writes `source-manifest.json` (`companies-house-source-manifest-v1`) with url, filename, bytes, sha256 per file
- `latest_basic()` prefers the `asonefile` variant of the newest date
- User-Agent `Ventus-PipelineNews/1.0 (+https://github.com/Ventusltd/pipelinenews)`

### 2.2 The frozen plan — what the current checkpoint actually pins

`build/python/202608272035-freeze-companies-house-plan.py` (wrapped unchanged by `…272120` and `…272155`) hard-pins
four objects and **re-probes them with HTTP HEAD every run**, failing closed on any drift of URL, filename, bytes,
ETag or Last-Modified:

| kind | file | bytes | ETag |
|---|---|---|---|
| accounts | `Accounts_Monthly_Data-May2026.zip` | 1,975,424,256 | `"5c27d3b8…-236"` |
| accounts | `Accounts_Monthly_Data-June2026.zip` | 2,348,684,884 | `"b86d234b…-280"` |
| accounts | `Accounts_Monthly_Data-July2026.zip` | 2,229,763,708 | `"2dcaa897…-266"` |
| basic | `BasicCompanyDataAsOneFile-2026-08-01.zip` | 493,049,031 | `"b6840201…-59"` |

`EXPECTED_TOTAL_BYTES = 7,046,921,879`. Ceilings: `MAXIMUM_ARCHIVE_BYTES = 4e9`, `MAXIMUM_TOTAL_BYTES = 12e9`,
`MAXIMUM_PAGE_BYTES = 2e6`, connect 15 s, read 45 s, redirects enumerated and bounded.
`require_official()` rejects credentials in the URL, a port, a query, a fragment, percent-encoded paths,
backslashes and `..` segments, and requires the `.zip` suffix.

Licence carried in the plan: **Open Government Licence v3.0**, with an explicit
`rights_caveat` ("OGL applies to Crown copyright material; third-party rights and data-protection duties may still
apply") and `accuracy_caveat` ("Companies House records what was filed; it does not verify every filed statement").

### 2.3 The REST API — present, but deliberately a credential probe only

This is important and easy to miss. `optional_rest_evidence()` in
`build/python/202608271507-freeze-companies-house-plan.py` already implements a **complete, reviewed REST client**:

```
host         api.company-information.service.gov.uk
probe path   /company/00000006
auth         HTTP Basic, key as username, empty password, from env COMPANIES_HOUSE_API_KEY
headers      Accept: application/json, Accept-Encoding: identity, Connection: close
ceilings     MAXIMUM_REST_RESPONSE_BYTES = 1_000_000, connect 15 s, read 45 s
429 handling reads x-ratelimit-reset, waits the server-derived delay, retries once
             refuses any reset beyond a five-minute boundary
retention    status + rate-limit headers only; no response body, no company payload, no secret
output       evidence/rest-api.json, schema companies-house-optional-rest-evidence-v1
             {enabled: false, status: "SKIPPED", reason: "optional-secret-not-configured"} when no key
```

The verifier (`202608271507-verify-companies-house-candidate.py`) records it in the manifest as
`inputs.optional_rest = {enabled, status, evidence_sha256}` and, in later generations, pins the evidence file by
sha256 (`EXPECTED_REST_EVIDENCE_SHA256`).

**So the statement in the README — "the Companies House REST API is not used" — is true of the *data*, not of the
*capability*.** The transport, auth, rate-limit discipline and retention rules for a REST call already exist and
have been through the same review as everything else. The project-vehicle watch in §5 is an extension of this
existing, bounded client — not a new network surface invented from nothing.

### 2.4 Where the bytes live

Nowhere durable. The archives are downloaded into runner temporary storage, expanded under strict ceilings
(`MAX_DOCUMENT_BYTES`, `MAX_OTHER_MEMBER_BYTES`, `MAX_TOTAL_EXPANDED_BYTES`, `MAX_COMPRESSION_RATIO`, `MAX_MEMBERS`,
`MAX_NESTING` — a zip-bomb guard), and discarded. Only four retained Actions artifacts are referenced by digest:

```
companies-plan-202608272155-33123064395   sha256:5458cb47…
accounts-202608272155-33123064395-0       sha256:73cfb688…
accounts-202608272155-33123064395-1       sha256:3da269b2…
accounts-202608272155-33123064395-2       sha256:4f37aa9e…
```

Hard gates: `raw_archives: 0`, `raw_company_json_files: 0`, `company_master_files: 0`, `company_master_rows: 0`,
`duplicate_corpus_builds: 0`.

---

## 3. What it extracts, and the selection rule

### 3.1 Accounts extraction (the private balance-sheet view)

`build/python/202608262245-extract-accounts.py` parses XBRL/iXBRL with lxml in recover mode and keeps **six facts**:

| XBRL local name (normalised) | field |
|---|---|
| `totalassets` | `total_assets` |
| `totalassetslesscurrentliabilities` | `total_assets_less_current_liabilities` |
| `netassetsliabilities` | `net_assets` |
| `turnoverrevenue`, `turnover` | `turnover` |
| `cashbankinhand`, `cashandcashequivalents` | `cash` |

plus `company_number` (regex `(?:^|_)([A-Z]{2}\d{6}|\d{8})(?:_|\.)` from the filename), `source_file`, and
`accounts_date` = the latest context date across the kept facts. Scale and sign attributes are applied. One row per
company, newest accounts date wins. Output is NDJSON.

### 3.2 Selection (`select_relationship_records`)

Streams the Basic archive CSV row by row with a 250,000-row heartbeat. Per row:

```python
large        = max(total_assets or 0, net_assets or 0) >= LIMIT            # LIMIT = 10_000_000
matches      = repd_candidates(name, repd_index)                          # see 3.3
probable_spv = has_legal_suffix(name) and has_energy_token(name)
                 legal  = {limited, ltd, plc, llp}
                 energy = {project, farm, solar, wind, battery, storage, bess, generation}
tags                  = sic_tags(sic_1..4)
energy_relevant_large = large and bool(tags)

keep if (energy_relevant_large or matches or probable_spv)
```

SIC tagging (`sic_tags`): division 05–39 → `INDUSTRIAL_SIC_B_TO_E`; plus prefix families
`BTM_MINING (05–09)`, `BTM_FOOD_PROCESSING (10,11)`, `BTM_PAPER (17)`, `BTM_CHEMICAL_PHARMA (20,21)`,
`BTM_RUBBER_PLASTICS (22)`, `BTM_GLASS_CEMENT_MINERALS (23)`, `BTM_METALS_ENGINEERING (24,25,28,29,30)`,
`BTM_WATER_WASTE (36–39)`; plus exact codes `52103 → BTM_COLD_STORAGE`, `63110 → BTM_DATA_CENTRE`,
`52230 → BTM_AIRPORT_INFRASTRUCTURE`, `49100/49200 → BTM_RAIL_INFRASTRUCTURE`, `47110 → BTM_SUPERMARKET`.

Result: **294,904 selected companies**, of which those with at least one REPD edge become relationship records.
Summary counters carried: `assets_gte_10m_companies`, `energy_relevant_large_companies`, `probable_project_spvs`,
`companies_with_repd_candidates`, `candidate_relationship_rows`, `btm_tag_counts`.

**Note for §4:** `probable_project_spv` is already computed for every selected company. The project-vehicle
projection does not need to invent an SPV detector; it needs to *narrow* this one and bind it.

### 3.3 The REPD matching rule (`repd_candidates`)

Normalisation `norm()`: lowercase, strip `limited|ltd|plc|holdings?|group|uk` as whole words, collapse
non-alphanumerics to single spaces.

Three deterministic rules produce three evidence types:

| Rule | Evidence type | Verified rows |
|---|---|---|
| `norm(company_name)` equals `norm(project.operator)` | `EXACT_OPERATOR_NAME` | 5,669 |
| `norm(company_name)` equals `norm(project.name)` | `EXACT_PROJECT_NAME` | 765 |
| every distinctive token of a project name (length ≥ 5, not in `GENERIC_PROJECT_TERMS`) is a subset of the company's tokens | `PROJECT_NAME_SPV_CANDIDATE` | 475,596 |

`GENERIC_PROJECT_TERMS` = `SPV_TERMS ∪ {the, and, park, site, phase, extension, offshore, onshore, limited, ltd}`
where `SPV_TERMS = {solar, wind, battery, bess, storage, renewable, energy, power, generation, farm, project,
developments}`.

Every one of these is explicitly **candidate generation only**. The contract states, per type,
*"it does not prove operator identity, ownership or control"*, *"a shared name does not prove company-to-project
identity"*, *"this is neither confirmed SPV status nor ownership"*.

---

## 4. Parquet, DuckDB and the query surface

### 4.1 Engine

DuckDB **1.3.2**, `SET threads = 1`, ZSTD compression, deterministic sort on the declared key.
Write → audit → landed readback. Files hard-capped at 20 MB each, 30 MB durable closure total.

### 4.2 The two landed tables

```
data/candidates/202608272155-compact/company-repd-relationships-v1.parquet
  rows 482,030   bytes 1,405,427   sha256 f278851979df8abd5dd66d3975176fdf159463538ed1a1b4a506d2568e300754
  record_universe_sha256 915b52a90c6876510e757a3839e2eef0018929e8937c9d8ec454d8466b45ef06

data/candidates/202608272155-compact/solar-company-repd-relationships-v1.parquet
  rows 346,233   bytes 1,118,626   sha256 b02e61639e159258d968afecc9bf2b2412f53c4347fcda8510196abf76066aed
  materialized_subset_of company_repd_candidates, predicate pinned_repd.technology = 'solar'
```

Schema, both tables, exactly three columns:

| column | DuckDB type | nullable | meaning |
|---|---|---|---|
| `company_number` | VARCHAR | false | Companies House company number; a stable company key, **not** evidence of a project role |
| `repd_ref` | VARCHAR | false | Authoritative REPD source identifier; downstream canonical key is `GG2050-REPD-{repd_ref}` |
| `evidence_type` | VARCHAR | false | Deterministic candidate-generation method from the closed vocabulary |

Declared key `(company_number, repd_ref, evidence_type)`. 481,248 distinct `(company_number, repd_ref)` pairs;
749 pairs carry more than one evidence type; maximum 3 per pair.

### 4.3 What is forbidden in the tables

`descriptive_edge_columns: 0`, `row_level_provenance_columns: 0`, `per_row_digest_columns: 0`,
`embedded_relationship_json_fields: 0`, `logical_json_cartridges: 0`, `row_url_columns: 0`.
Provenance lives once, artifact-level, in `manifest.inputs`. URLs live once, dataset-level, in
`state/atlas-v9-link-contract.json`.

### 4.4 Audit queries actually executed (`audit_relational_integrity`)

```sql
CREATE TABLE pinned_repd (repd_ref VARCHAR PRIMARY KEY, technology VARCHAR);
-- foreign-key closure: every relationship repd_ref exists in the pinned REPD universe
SELECT m.* FROM read_parquet('<main>') m ANTI JOIN pinned_repd USING (repd_ref);
SELECT count(*) FROM read_parquet('<main>') m ...;
-- solar is an exact subset, both directions
SELECT count(*) FROM (SELECT * FROM read_parquet('<solar>') EXCEPT SELECT * FROM read_parquet('<main>'));
SELECT count(*) FROM (... EXCEPT SELECT * FROM read_parquet('<solar>'));
```

Hard gates: `rows_equal_distinct_declared_keys`, `duplicate_key_groups = 0`, `null_declared_keys = 0`,
`unknown_repd_refs = 0`, `solar_is_exact_parent_subset = true`, `typed_column_mismatches = 0`,
`landed_duckdb_readback = true`.

### 4.5 The query surface a consumer actually has

There is no service. A consumer reads Parquet over HTTPS with DuckDB (in a runner, or DuckDB-WASM in a browser):

```sql
-- every candidate company for one project
SELECT company_number, evidence_type
FROM read_parquet('…/company-repd-relationships-v1.parquet')
WHERE repd_ref = '13599';

-- how many candidate projects one company touches
SELECT repd_ref, evidence_type
FROM read_parquet('…/company-repd-relationships-v1.parquet')
WHERE company_number = 'SC123456';

-- solar-only, pre-materialised so the technology join is not re-derived downstream
SELECT * FROM read_parquet('…/solar-company-repd-relationships-v1.parquet') WHERE repd_ref = '17494';
```

Every such read must carry, per `provenance.required_downstream_fields`:
`candidate_commit`, `manifest_sha256`, `dataset_sha256`, `observation_or_generation_time`, `evidence_type`,
`relationship_status` — and must present rows as candidates, never as confirmed facts.

**Sizing note:** at 1.4 MB the main table is small enough for a browser DuckDB-WASM search lane; at 482,030 rows it
is far too large to draw. It belongs in the SEARCH plane, never the drawing plane. See `DATA-DELIVERY-PLAN.md`.

---

## 5. The gap: what the bulk product does not contain

The stated funding signal is charges, PSC changes, renames, director appointments and administration. Of those,
the Basic Company Data bulk file carries:

| Signal | In `BasicCompanyDataAsOneFile`? | Notes |
|---|---|---|
| Company name | **yes** | current name only |
| Previous names | **yes** | `PreviousName_1..10` columns — a **rename is detectable from the bulk file** |
| Company status | **yes** | `Active`, `Liquidation`, `In Administration`, `Dissolved` — **distress is partly detectable** |
| Incorporation date | yes | |
| SIC 1–4 | **yes** | **SIC change detectable by diffing two monthly snapshots** |
| Registered address | yes | not used |
| Accounts / returns dates | yes | next-due and last-made-up dates |
| **Registered charges** | **no** | charge count is not in the basic file; charge detail is in the REST `/company/{n}/charges` or the "Mortgage" bulk product |
| **PSC** | **no** | separate PSC snapshot product / REST `/company/{n}/persons-with-significant-control` |
| **Officers / directors** | **no** | REST `/company/{n}/officers` |
| **Filing history** | **no** | REST `/company/{n}/filing-history` |

So:

- **Renames, SIC changes, status changes and distress are obtainable today by diffing two Basic snapshots.**
  This needs no new source, no API key and no new privacy surface. It is the cheapest half of the funding signal.
- **Charges, corporate PSC changes and director-count changes require the REST API** (or the separate PSC and
  Mortgage bulk products). The REST client already exists as a probe (§2.3) and would need to be extended.

`questions.md` Q2 asks which of the two routes to take. The design in §6 works for either, because the projection is
defined in terms of *events*, not in terms of *where the bytes came from*.

---

## 6. The project-vehicle projection — exact design

### 6.1 The principle

> An SPV owning a consented park has no trade, so its filing history **is** the project's biography.

The existing `companies` view answers *"which large trading entities exist and what is on their balance sheet"*.
The project-vehicle view answers a different question — *"what has happened to the company that owns this park"* —
and it must be **a separate projection with a separate contract, a separate output path, a separate grain and a
separate acceptance gate.** It shares only the company number.

### 6.2 What is different, stated as a table

| | Private balance-sheet view (existing) | Project-vehicle view (new) |
|---|---|---|
| Question | how big is this company | what happened to this vehicle |
| Population | assets ≥ £10m ∧ energy-relevant SIC | vehicles **bound** to a REPD project |
| Grain | one company, one accounts date | one dated corporate event for one vehicle |
| Fields | total assets, net assets, turnover, cash | event type, event date, counterparty *organisation* |
| Retained? | **transient selection only** — never in the relationship tables | landed, but only as events |
| Person data | excluded | **excluded, identically** |
| Output path | `data/candidates/{gen}-compact/` | `data/candidates/{gen}-vehicle/` |
| Contract | `202608281337-compact-parquet-companies.json` | new `…-project-vehicle-events.json` |
| Consumer decision | ABSTAIN | ABSTAIN until vehicle binding is `PRIMARY_MATCH` |

**The two must never be joined in a landed table.** A vehicle event row must not carry a balance-sheet number, and
a balance-sheet row must not carry an event. A downstream consumer may look at both, keyed on `company_number`, and
that is the only place they meet.

### 6.3 The vehicle binding rule (the hard part)

Today 475,596 `PROJECT_NAME_SPV_CANDIDATE` edges exist and all are `ABSTAIN`. A projection that watched all of them
would be noise. The binding rule must promote a small, defensible subset to `PRIMARY_MATCH`.

Draft rule — a candidate edge is promoted to `PRIMARY_MATCH` only if **all** of:

1. `evidence_type ∈ {EXACT_OPERATOR_NAME, EXACT_PROJECT_NAME}`, **or** `PROJECT_NAME_SPV_CANDIDATE` **and** the
   company's normalised name contains **every** distinctive token of the project name **and** at least one
   `SPV_TERM`, **and** the project-name token set has ≥ 2 distinctive tokens (a one-token name like "Ossian" is
   not distinctive enough to bind);
2. the edge is **unique in both directions** for that evidence type — this `company_number` binds to exactly one
   `repd_ref`, and this `repd_ref` binds to exactly one `company_number` under rule 1;
3. the company's SIC includes an energy code, **or** the company name contains an `SPV_TERM`;
4. the company was incorporated **no later than** `planning_permission_granted + 24 months` and **no earlier than**
   `planning_application_submitted - 60 months` (a vehicle for a park is not 20 years older than the application);
5. no other company satisfying 1–4 exists for the same `repd_ref`.

Anything failing any clause is `ABSTAIN` and is **retained** with its failure reason. `REJECTED` is reserved for a
positive contradiction — e.g. two companies satisfy 1–4 for the same project.

Rules 2 and 5 are what turn 475,596 into a workable number. **The actual count is unknown until the rule is run**
and is recorded as `questions.md` Q4 — the plan must state the expected count as an output, not an assumption.

Binding law, copied from the existing contracts:
`llm_may_establish_binding: false`, `name_equality_may_establish_binding: false`,
`capacity_may_establish_identity: false`, `absence_rule` unchanged.

### 6.4 Landed schema — `project-vehicle-events-v1.parquet`

Grain: **one dated corporate event for one bound project vehicle.**
Declared key: `(company_number, event_type, event_date, source_ref)`.

| column | DuckDB type | nullable | meaning |
|---|---|---|---|
| `company_number` | VARCHAR | false | Companies House number, `^[A-Z0-9]{8}$` |
| `repd_ref` | VARCHAR | false | bound project; rows only exist for `PRIMARY_MATCH` bindings |
| `event_type` | VARCHAR | false | closed vocabulary, §6.5 |
| `event_date` | DATE | false | the date **the register records**, never the date we noticed |
| `source_ref` | VARCHAR | false | the register's own reference (charge code, filing transaction id, snapshot pair id) |
| `counterparty_organisation` | VARCHAR | true | e.g. named secured party on a charge, corporate PSC name. **Organisation only.** NULL where the event has no counterparty |
| `counterparty_company_number` | VARCHAR | true | where the counterparty is itself a registered company |
| `magnitude` | BIGINT | true | integer delta where the event is a count change (director count, PSC count). NULL otherwise |
| `previous_value` | VARCHAR | true | for renames and SIC/status changes: the prior value. NULL otherwise |
| `new_value` | VARCHAR | true | for renames and SIC/status changes: the new value. NULL otherwise |
| `observed_at` | TIMESTAMP | false | generation anchor |

**Twelve columns and not one more.** No addresses, no dates of birth, no nationality, no names of natural persons,
no scores. A companion `project-vehicle-bindings-v1.parquet` carries
`(company_number, repd_ref, evidence_type, binding_status, binding_reason)` including every `ABSTAIN`.

### 6.5 The closed event vocabulary

| `event_type` | Source | Meaning | Window role |
|---|---|---|---|
| `REGISTERED_CHARGE_CREATED` | charges | a lender arrived | **funding** |
| `REGISTERED_CHARGE_SATISFIED` | charges | debt discharged | context |
| `PSC_CORPORATE_CHANGE` | PSC | a corporate PSC was added, ceased or changed | **funding** |
| `PSC_INDIVIDUAL_COUNT_CHANGE` | PSC | the *number* of individual PSCs changed. **No identity, ever.** | **funding** |
| `COMPANY_RENAME` | basic bulk (`PreviousName_*`) | rebadging | **funding** |
| `DIRECTOR_APPOINTMENT_COUNT_CHANGE` | officers | integration — buyer putting its people in. **Count only, no names.** | **funding** |
| `SIC_CHANGE` | basic bulk diff | vehicle activated or repurposed | **funding** |
| `COMPANY_STATUS_CHANGE` | basic bulk diff | Active → Liquidation etc. | context or distress |
| `ACCOUNTS_TYPE_CHANGE` | basic bulk / accounts | dormant → non-dormant is a strong activation tell | **funding** |
| `ADMINISTRATION` | status + Gazette | the end | **distress** |
| `LIQUIDATION` | status + Gazette | the end | **distress** |
| `STRIKE_OFF_PROPOSED` | status + Gazette | the end | **distress** |
| `STRIKE_OFF_DISCONTINUED` | status + Gazette | reprieve | context |

Note `PSC_INDIVIDUAL_COUNT_CHANGE` and `DIRECTOR_APPOINTMENT_COUNT_CHANGE`. These carry **a number, never a person**.
"Three directors were appointed to the vehicle on 12 March" is a corporate fact about a company. It is the signal
the product wants and it does not require, and must not retain, a single individual's identity. This is how the
project-vehicle view stays inside the existing privacy law rather than beside it.

### 6.6 Privacy block for the new contract (draft, verbatim-compatible with the existing ones)

```json
"privacy_and_storage": {
  "private_individual_names": false,
  "directors": false,
  "director_names": false,
  "individual_psc": false,
  "individual_psc_identity": false,
  "individual_psc_count_only": true,
  "dates_of_birth": false,
  "nationalities": false,
  "residential_addresses": false,
  "correspondence_addresses": false,
  "raw_archives": false,
  "company_master_files": false,
  "balance_sheet_fields_in_vehicle_tables": false,
  "credit_or_bankability_score": false,
  "pipeline_news_may_copy_bulk_company_data": false
}
```

and the corresponding hard gates:

```json
"hard_gates": {
  "vehicle_columns_per_table": 12,
  "person_keyed_columns": 0,
  "balance_sheet_columns": 0,
  "rows_equal_distinct_declared_keys": true,
  "null_declared_keys": 0,
  "unbound_vehicle_rows": 0,
  "events_without_official_source_ref": 0,
  "landed_duckdb_readback": true,
  "promotion_eligible": false
}
```

`unbound_vehicle_rows: 0` is the load-bearing gate: **an event row cannot exist for a company that is not bound to a
project.** That single constraint keeps this from becoming a general company-surveillance dataset. Everything
unbound stays in the bindings table as an `ABSTAIN` with no events attached.

### 6.7 Two acquisition routes for the same schema

**Route A — snapshot diff (no API key, available now).**
Retain, per generation, a *minimal* projection of the Basic file for bound vehicles only:
`(company_number, company_name, company_status, sic_1..4, previous_names)`. Diff against the previous generation's
projection. Emit `COMPANY_RENAME`, `SIC_CHANGE`, `COMPANY_STATUS_CHANGE` and the distress trio.
Cost: one extra ~50–200 KB Parquet per generation (bound vehicles only). No new host. No new secret.
Covers roughly half the funding vocabulary, and **all** of distress. `source_ref` = `SNAPSHOT_DIFF:{prev_gen}:{gen}`.

**Route B — bounded REST reads (needs `COMPANIES_HOUSE_API_KEY`).**
Extend the existing probe client to read, for bound vehicles only:
`/company/{n}/charges`, `/company/{n}/persons-with-significant-control`,
`/company/{n}/officers?items_per_page=1` (for the **count** in `total_results` only),
`/company/{n}/filing-history?category=…`.
Retain only the fields in §6.4. Reuse the existing 429/`x-ratelimit-reset` handling, the 1 MB response ceiling and
the "no body retained" rule. Bound by `maximum_rest_requests_per_run` and by the bound-vehicle count.
Covers the remaining vocabulary, including charges — the highest-value signal.

Recommendation: **do Route A first.** It is buildable tonight with no key, no new host and no new privacy question,
and it delivers the entire distress path — which, under "distressed always wins", is the highest-precedence branch
of the state machine. Route B follows once the vehicle-binding count from §6.3 is known and a request budget can be
sized against it.

---

## 7. Join keys, end to end

The complete chain, stated once, with the exact field names.

```
Companies House company number
        |  companies: company_number  (VARCHAR, ^[A-Z0-9]{8}$)
        v
project vehicle
        |  project-vehicle-bindings-v1.parquet
        |    (company_number, repd_ref, evidence_type, binding_status)
        |    binding_status must be PRIMARY_MATCH to carry events
        v
REPD reference
        |  companies: repd_ref (VARCHAR)  ==  pipelinenews: repd_ref (string, ^\d+$)
        |                                ==  gridatlas:     repd_ref (VARCHAR)
        v
canonical project
        |  pipelinenews: gg_project_id = "GG2050-REPD-" || repd_ref
        |    derived downstream; NOT stored in the companies candidate
        v
map feature
        |  gridatlas deep link: ?repd_ref={repd_ref}
        |    identity_rule EXACT_REPD_REF_ONLY
        |    receiver: atlas/cartridges/…-place-global-search-v9-5.js
        |    proof: document.body.dataset.gridatlasRepdRef === repd_ref
        v
map point
           gridatlas parquet: (longitude, latitude) — evidence, never identity
           false-origin guard rejects (49.766807, -7.55716) and (0,0)
```

Secondary join keys, for the register side (procurement signal):

| Key | Where it lives | Used for |
|---|---|---|
| `planning_application_reference` | both spines | the primary key into a local planning register |
| `planning_authority` | both spines | which register to query |
| `repd_postcode` / `repd_postcode_raw` / `postcode_valid` | gridatlas parquet (9,505 rows) | fallback lookup, and the only route to a parish (via a postcode directory, not yet a source) |
| `county`, `region`, `country` | both spines | coarse filtering only |
| `repd_operator_or_applicant` | gridatlas parquet | the name that `EXACT_OPERATOR_NAME` matches; **1,729 rows withheld as possible individuals** |
| `operator` | pipelinenews spine | same field, different derivation |

Cardinality warnings the plan must respect:

- `company_number → repd_ref` is **many-to-many** in the candidate table (481,248 distinct pairs over 482,030 rows).
  It is one-to-one only after the §6.3 binding rule.
- `repd_ref` is unique in both spines (`unique_repd_refs: 11069` in gridatlas; `record_identity_preserved` in
  pipelinenews) but the **sets differ**: 11,069 vs 7,680.
- `planning_application_reference` is **not unique and frequently empty** — the gridatlas registry shows empty
  strings and nulls; `Berwick Bank` has `""`. Any register fetcher must abstain on an empty reference, never guess.
- `repd_postcode` is null on 1,564 of 11,069 rows and invalid on a further 445.

---

## 8. What must not change in `companies`

- the £10m balance-sheet view, its selection rule, its exclusions and its transient-only retention
- `descriptive_edge_columns: 0` and the three-column relationship tables
- the OGL attribution and both caveats
- `promotion_eligible: false` and the candidate-branch-only publication
- the bulk-only acquisition boundary for the *existing* generation — Route B is a **new generation with a new
  contract**, never an edit to `202608281337`
- `recovery_rule`: never overwrite a contract or a pinned candidate; always add a later timestamped successor

---

## 9. Draft file plan for the new generation

```
companies/
  contracts/<gen>-project-vehicle-events.json          # new contract, deployment: not-authorised
  build/python/<gen>-build-project-vehicle-events.py   # binding rule + Route A snapshot diff
  tests/test_<gen>_project_vehicle_events.py           # hostile fixture; no network
  .github/workflows/<gen>-project-vehicle-candidate.yml
  data/candidates/<gen>-vehicle/
      project-vehicle-bindings-v1.parquet
      project-vehicle-events-v1.parquet
      vehicle-report-v1.json
      vehicle-parquet-audit-v1.json
      manifest-vehicle-v1.json
```

Source-boundary discipline: the workflow must assert the exact changed-file set the way
`202608281337-compact-parquet-companies-candidate.yml` does (`git diff --name-status` against a pinned parent,
compared to a literal expected list, with a hard count). That pattern is why this repository has never leaked a file
it did not intend to, and it should be copied verbatim.
