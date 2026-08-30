# window-intelligence

**The core artefact.** Two halves:

- **Part I — What exists.** An exhaustive account of the layer as it is actually present in the repositories today,
  including an honest finding about generation `202608300415`.
- **Part II — The wiring that remains.** Drafts and instructions, in the build order the system implies:
  register adapter first, then the project-vehicle filing watch, then the ranked output, then grid and contractor
  exposure.

Nothing here is installed. Every code block is a **draft to review**, written to the conventions the repositories
already use.

---
---

# PART I — WHAT EXISTS

## 1. Finding on generation 202608300415

The brief describes a window-intelligence layer *already existing* at generation `202608300415` in `pipelinenews`,
with an eight-state project lifecycle, a register adapter, a corporate-events adapter, an evidence-order state
machine (distressed always wins) and a ranker — tested, disciplined, not-authorised by default, hash-verified,
ledgered, sourced-or-rejected.

**That layer is not in the repository.** The evidence:

| Check | Result |
|---|---|
| Files matching `*202608300415*` in `pipelinenews` | exactly one: `.github/workflows/202608300415-advance-successor-to-exact-atlas.yml` |
| Commit `202608300415` | `ed03159286b0868cb3895fb570a9ab65c0c2aa48`, 2026-08-30 05:12 +0100, *"advance PipelineNews successor gate"*, **1 file changed, 78 insertions** — a workflow that advances the Atlas successor gate |
| Successor `202608300416` (`1fb5ac9`) | edits the same workflow, 61 insertions / 48 deletions |
| Text search across all 12 repos for `window-intelligence`, `window_intelligence`, `funding_window`, `evidence-order`, `evidence_order` | 0 hits |
| Text search for `design freeze`, `freeze overdue`, `days to freeze`, `window entry` | 1 hit, in an unrelated GlobalGrid2050 employer's-requirements fragment |
| Text search for `persons with significant control`, `psc_` | 0 hits |
| Filename search across the **full git history** of `pipelinenews`, `companies`, `cvaa`, `spiders` for `window`, `lifecycle`, `ranker`, `corporate`, `register` | only `attributionv1/*register*`, `releases/javascript/202608262115-projects-v8-windowed.js` (a table-paging file), and `cvaa/vaccines/202608301324-no-expiry-windows.md` |
| Remote branches on `pipelinenews` | 9, all `atman/*mobile-css*` or `ci/*atlas-pointer*` / `ci/*pages*` — none carrying such a layer |

**What *does* exist is better than nothing and worse than described:** roughly 70 % of the components, built to the
right discipline, sitting in an archived candidate that was never wired, plus a lifecycle field with five values
rather than eight. Sections 2–7 document all of it precisely. Section 8 onward drafts the rest.

This is recorded again in `questions.md` Q1. If a `202608300415` layer exists somewhere outside this workspace
(another clone, an unpushed branch, another machine), Part II should be read as a **specification to diff against it**
rather than as new work.

---

## 2. The project lifecycle as it exists — five states, not eight

Source: `pipelinenews/archive/202608261547-pipelinenews/202608260159-pipelinenews/data/v9.1/projects/part-*.json`,
field `lifecycle`. Distinct values across all 7,680 records:

| Value | Meaning as used |
|---|---|
| `LIVE_PRE_CONSTRUCTION` | consented or applied, not yet building — **the entire commercial window is compressed into this one state** |
| `UNDER_CONSTRUCTION` | REPD status `under construction` |
| `OPERATIONAL` | REPD status `operational` |
| `INACTIVE` | refused, withdrawn, expired, abandoned |
| `UNKNOWN` | insufficient evidence |

A second, orthogonal five-value enum exists in the V7 UI (`globalgrid2050/uk_renewables_pipeline/v7/scripts/core/project-state.js`),
`lifecycle_view ∈ {ALL, CURRENT, DISPUTED, HISTORICAL, REVIEW}`. That is a **display filter**, not a project state,
and must not be confused with `lifecycle`.

The commercially load-bearing distinction — *is this project inside the funding window, approaching design freeze, or
past it* — does not exist as data anywhere. `LIVE_PRE_CONSTRUCTION` covers a project that got consent yesterday and
one that freezes design next month, identically. **Splitting that state is the whole job.**

The raw date fields needed to split it are already carried on every project record:

```
planning_application_submitted   planning_permission_granted    planning_permission_refused
planning_application_withdrawn   planning_permission_expired    under_construction
operational                      repd_record_updated
```

plus `planning_authority`, `planning_application_reference`, `operator`, `capacity_mw`, `technology`,
`geometry_status`, `county`, `region`, `country`, `development_repd_refs`, `planning_sibling_repd_refs`.

---

## 3. The register adapter — exists, complete, archived

**File:** `pipelinenews/archive/202608261547-pipelinenews/attributionv1/modules/register-ingest.mjs` (96 lines)
**Contract:** `attributionv1/contracts/register-ingest.v1.json`
**Gate:** `attributionv1/tests/check_batch6_registers.mjs` — passes on its fixture
**Status:** `CANDIDATE`, archived, never run against a live register.

### 3.1 Source policy (domain-pinned, hardcoded)

```js
const sourcePolicy = Object.freeze({
  planit:        ["planit.org.uk",            "OFFICIAL_PLANNING_AGGREGATOR"],
  planning_data: ["planning.data.gov.uk",     "OFFICIAL_PLANNING_DATA"],
  neso:          ["neso.energy",              "OFFICIAL_CONNECTION_REGISTER"],
  lccc:          ["lowcarboncontracts.uk",    "OFFICIAL_CFD_REGISTER"],
  gazette:       ["thegazette.co.uk",         "OFFICIAL_STATUTORY_NOTICE"]
});
```

`sourceDetails()` rejects any record whose `evidence_url` is not `https:` and whose hostname is not the policy host
or a subdomain of it. `check_batch6` asserts this: substituting `https://publisher.example/item` throws
`source URL does not match planit policy`.

### 3.2 Source law (`register-ingest.v1.json`)

| Rule | Value |
|---|---|
| `official_register_credibility` | `1` |
| `role_must_be_explicit_in_source_record` | `true` |
| `missing_organisation` | `ABSTAIN` |
| `gazette_notice_is_organisation_event_not_delivery_role` | `true` |
| `contradictions_overwrite` | `false` |

### 3.3 Three outputs

`ingestRegisterRecords(records)` returns `{ roles, organisation_events, abstentions }`:

- **roles** — one organisation-role claim per *explicit* source assertion, normalised through
  `normaliseAttribution()`, always `claim_status: "CONFIRMED"`, `credibility: 1`
- **organisation_events** — gazette records only. `organisation_event_id = PN-ORG-EVENT-<sha256(gg_project_id \n organisation \n event_type \n source_ref \n observed_at)[0:20].toUpperCase()>`.
  A statutory notice is an **organisation event, never a delivery role** — `check_batch6` asserts no role carries
  `evidence_kind: "OFFICIAL_STATUTORY_NOTICE"`.
- **abstentions** — retained rows with `decision: "ABSTAIN"`, `reason: "NO_EXPLICIT_ORGANISATION"`

Fixture proof (`data/register-fixture-proof.json`): 4 roles, 4 confirmed, 1 organisation event, 1 abstention;
two *officially conflicting* `OWNER` records coexist (NESO says one company, LCCC says another) and neither wins.

**This is already the corporate-events adapter in embryo.** `organisation_events` is exactly the shape a
project-vehicle filing watch needs — it just currently accepts one `event_type` from one source.

---

## 4. The evidence ledger — exists, complete, archived

**File:** `attributionv1/modules/attribution-ledger.mjs` (90 lines)
**Schema:** `attributionv1/contracts/attribution-role.v1.schema.json`
**Release contract:** `attributionv1/contracts/release.attributionv1.json`
**Gate:** `attributionv1/tests/check_batch5_attribution.mjs`

### 4.1 Grain and key

One dated, sourced organisation-role claim per canonical project.
`attribution_id = PN-ATTR-<sha256(gg_project_id \n role \n organisation \n url \n observed_at)[0:20].toUpperCase()>`
Deterministic; identical evidence yields an identical id, so `appendAttributions` deduplicates by construction.

### 4.2 Roles and statuses

```
DEVELOPER  OWNER  EPC  PRINCIPAL_CONTRACTOR  ICP  OM_PROVIDER  LENDER  TECHNICAL_ADVISER
CONFIRMED  REPORTED  ABSTAIN
```

### 4.3 Invariants enforced in code

- `repd_ref` must match `^\d+$`; `gg_project_id` must equal `GG2050-REPD-{repd_ref}` exactly
- `evidence_url` must be `https:`
- `credibility ∈ (0, 1]`; **`CONFIRMED` requires credibility ≥ 0.7**
- `assertNoPersonKeys()` walks the whole object recursively and throws on any key matching
  `/(^|_)(person|individual|officer|name_of_person)($|_)/iu`
- rows are sorted by `gg_project_id` (numeric collation) → `role` → `observed_at` → `attribution_id`
- **no row overwrites another**; contradictory claims coexist (`check_batch5` asserts 2 rows, 2 organisations)

### 4.4 The charge path — the funding signal that already works

```js
export function attributionsFromRegisteredCharge(project, charge) {
  if (charge.source_domain !== "find-and-update.company-information.service.gov.uk")
    throw new Error("registered-charge source must be the official company register");
  if (!Array.isArray(charge.persons_entitled) || !charge.persons_entitled.length) return [];
  return charge.persons_entitled.map((organisation) => normaliseAttribution({
    ..., role: "LENDER", effective_from: charge.created_on,
    evidence_kind: "REGISTERED_CHARGE_NAMED_SECURED_PARTY",
    credibility: 1, claim_status: "CONFIRMED"
  }));
}
```

Interpretation contract, asserted by the gate:

```
named_secured_party_confirmed:              true
registered_charge_date_confirmed:           true
financial_close_inferred_from_charge_alone: false
```

**A charge proves a named lender arrived on a date. It does not prove financial close.** That distinction is the
discipline the whole funding-window state must inherit.

Note `persons_entitled` — a Companies House field name — passes `assertNoPersonKeys` because the forbidden pattern
requires `person` as a whole underscore-delimited token; `persons_entitled` is not matched. In practice
`persons_entitled` on a charge is a security trustee or a bank, i.e. an organisation. That is fine but **fragile**:
a draft hardening is in §12.4.

---

## 5. The contradiction view — exists

**File:** `attributionv1/modules/discrepancy-view.mjs` (38 lines) + `sql/attribution-discrepancy.sql`

Joins each `REPORTED` claim to the `CONFIRMED` claims for the same project and role and labels it:

| status | meaning |
|---|---|
| `CONSISTENT` | a confirmed record names the same organisation |
| `CONFLICTS_WITH_CONFIRMED` | a confirmed record names a different organisation |
| `NO_CONFIRMED_RECORD` | nothing official yet |

It carries `project_state_at_claim: project?.lifecycle ?? "UNKNOWN"` — **the only place in the codebase where a
project state is attached to an evidence claim.** That single field is the seed of the state machine.
`publication_law`: `descriptive_status_only: true`, `allegation_or_person_assessment: false`.

---

## 6. The ranker — exists as a credibility engine

**File:** `pipelinenews/archive/202608261547-pipelinenews/discoveryv1/modules/credibility.mjs` (58 lines)
**Contract:** `discoveryv1/contracts/credibility.v1.json`

### 6.1 Tiers

| Tier | Score | Domains (as coded) |
|---|---|---|
| authoritative | **1.0** | `gov.uk`, `planninginspectorate.gov.uk`, `planning.data.gov.uk`, `planit.org.uk`, `neso.energy`, `nationalgrideso.com`, `find-and-update.company-information.service.gov.uk`, `thegazette.co.uk`, `lowcarboncontracts.uk`, `ofgem.gov.uk` |
| trade_press | **0.7** | `solarpowerportal.co.uk`, `energy-storage.news`, `current-news.co.uk`, `renews.biz`, `constructionenquirer.com`, `theconstructionindex.co.uk`, `pv-magazine.com`, `businessgreen.com` |
| national_or_regional_press | **0.6** | `bbc.co.uk`, `bbc.com`, `theguardian.com`, `ft.com`, `thetimes.co.uk` |
| corporate_social_or_unknown | **0.3** (default) | `x.com`, `medium.com`, everything unlisted |

Longest-suffix match wins. One apex domain is suppressed to 0.3 by sha256 digest without naming it.
`zero_credibility_allowed: false`.

### 6.2 Corroboration

```js
eventConfidence(mentions) = min(1, max(credibility) + min(0.2, 0.05 * (distinctDomains - 1)))
```

Rounded to 2 dp. Distinct-domain increment `0.05`, cap `0.2`, ceiling `1`.

### 6.3 Identity is never ranked

`credibility_may_gate_identity: false` (`release.discoveryv1.json`) and `identity_gate: false`
(`credibility.v1.json`). A high score never makes a binding true. Binding is decided by
`matcher-bridge.mjs` against a closed REPD gazetteer with an ambiguity margin, and any ambiguity is `ABSTAIN`,
any foreign-location conflict is `REJECTED`.

### 6.4 Coverage and freshness — the alert precedent

`discoveryv1/modules/capture-recapture.mjs`:

- `lincolnPetersen(nA, nB, overlap)` → `{estimated_total, recall_a, recall_b, note}`; zero overlap returns null
  with `"no overlap — channels not comparable"`
- `weeklyCoverageReport({week_ending, search_index_events, register_events, overlap})` →
  `pipelinenews.discovery-coverage.v1` with **`alert_threshold: 0.8`**
- `publicationReadiness({evaluated_at, latest_discovered_at, maximum_age_hours = 24, provider_statuses})` →
  `CURRENT` or `CANDIDATE_NOT_CURRENT`, with `empty_result_means_no_mentions: false`

**The two channels the Lincoln–Petersen estimator was designed for are exactly the two registers in the product
thesis:** `search_index_events` and `register_events`. It is already the coverage alarm for "are we actually a month
ahead, or just not looking?"

---

## 7. What the sector-intelligence layer contributes

`pipelinenews/data/news-discovery/202608272130-sector-intelligence-contract.json` (schema v3) is the live-ish
projection pattern the window layer should copy verbatim:

- three datasets — `sector_items`, `sector_item_topics`, `sector_project_bindings` — each with a declared key
- `sector_project_bindings` grain: *one evidence-backed project-binding decision for one item and REPD reference*,
  key `(intelligence_item_id, repd_ref, binding_role)`, `default_binding_decision: NONE`
- `forbidden_sector_item_fields`: `repd_ref, gg_project_id, project, technology, capacity_mw, operator, county,
  related_context_repd_ref` — **identity fields are physically removed from the un-bound projection**, so a sector
  item cannot leak an unproved project claim
- physical layout `releases/data/intelligence/{generation}/{dataset-dir}/{generation}-part-000.parquet`, ZSTD,
  `IMMUTABLE_FULL_GENERATION_WRITE_FROM_EMPTY_TARGET`, stage order
  `WRITE_STAGE → DUCKDB_AUDIT → PUBLISH → DUCKDB_LANDED_READBACK`
- time provenance separates `collection_anchor_at` (Actions wall clock) from `observed_at` and `source_published_at`
- `deployment: "not-authorised"`

---

## 8. Summary of Part I

| Component described in the brief | Present? | Where | State |
|---|---|---|---|
| Eight-state project lifecycle | **No** | — | Five values exist on the spine (`lifecycle`) |
| Register adapter | **Yes** | `attributionv1/modules/register-ingest.mjs` | Candidate, archived, fixture-gated, never run live |
| Corporate-events adapter | **Partly** | `organisation_events` in the same module (Gazette only) + `attributionsFromRegisteredCharge` | Candidate; no Companies House filing feed exists |
| Evidence-order state machine | **No** | — | `discrepancy-view.mjs` carries `project_state_at_claim`; nothing computes a state |
| "Distressed always wins" | **No** | — | No precedence rule anywhere |
| Ranker + weightings | **Yes, for evidence** | `discoveryv1/modules/credibility.mjs` + `credibility.v1.json` | Candidate; ranks *sources*, not *projects* |
| Three alerts | **No** | — | `weeklyCoverageReport` has one threshold (0.8) for coverage, not for windows |
| Not-authorised by default | **Yes** | every contract | Live discipline |
| Hash-verified closure | **Yes** | composer, bridge, search cartridge, inoculate | Live discipline |
| Ledgered | **Yes** | scope-of-works, manifests, contracts | Live discipline |
| Sourced-or-rejected | **Yes** | `claim_status`, `ABSTAIN`, `binding_status` | Live discipline |

---
---

# PART II — THE WIRING THAT REMAINS

Build order, as the system implies it:

```
STEP 1  register adapter            -> the PROCUREMENT signal becomes real data
STEP 2  project-vehicle filing watch -> the FUNDING signal becomes real data
STEP 3  ranked output                -> the two signals become one ordered list
STEP 4  grid and contractor exposure -> the list becomes a sales conversation
```

Each step is a separate timestamped generation, each `deployment: not-authorised` until its gate passes, each
rolled back by discarding the generation.

---

## 9. STEP 0 (prerequisite) — the eight-state lifecycle contract

Draft file: `pipelinenews/contracts/<generation>-project-window-lifecycle-v1.json`

### 9.1 The eight states

| # | State | Plain meaning | The money |
|---|---|---|---|
| 1 | `SUBMITTED` | Application in, not determined | Nothing yet. Watch only. |
| 2 | `CONSENTED` | Permission granted, no funding evidence yet | The clock starts. Nobody is buying. |
| 3 | `FUNDING_WINDOW` | **Consent + funding evidence on the record, before design freeze** | **Studies, cable and LV design are bought here.** This is the product. |
| 4 | `PROCURING` | Procurement evidence on the record (condition discharge, connection offer accepted, contractor named) | Design decisions are being made now; last call for spec influence. |
| 5 | `DESIGN_FROZEN` | Freeze evidenced (commencement notice, construction-stage approval, EPC named) | Cable and LV are decided. Inverter fight begins. |
| 6 | `UNDER_CONSTRUCTION` | REPD status `under construction` | Delivery and O&M only. |
| 7 | `OPERATIONAL` | REPD status `operational` | Aftermarket. |
| 8 | `DISTRESSED` | Administration, liquidation, strike-off, refusal, withdrawal, expiry | **Always wins.** Stop selling. Tell the team. |

Plus one non-state: **`ABSTAIN`** — insufficient evidence to place the project. `ABSTAIN` is not state 9; it is the
absence of a state, and it is the default. A project with no window evidence stays at its REPD-derived state.

### 9.2 Mapping from the existing five

| existing `lifecycle` | maps to |
|---|---|
| `LIVE_PRE_CONSTRUCTION` | `SUBMITTED` \| `CONSENTED` \| `FUNDING_WINDOW` \| `PROCURING` \| `DESIGN_FROZEN` — resolved by evidence; **`CONSENTED` if `planning_permission_granted` is set, else `SUBMITTED`** |
| `UNDER_CONSTRUCTION` | `UNDER_CONSTRUCTION` |
| `OPERATIONAL` | `OPERATIONAL` |
| `INACTIVE` | `DISTRESSED` |
| `UNKNOWN` | `ABSTAIN` |

The existing five are therefore fully preserved: the new contract is a **refinement**, never a contradiction, of the
frozen spine. Nothing about the 7,680-record spine changes.

### 9.3 Evidence required for each transition

Each transition names the evidence classes that can cause it. **No transition may be caused by inference, news,
proximity or a name match.** `credibility_may_gate_identity: false` continues to hold.

| From → To | Required evidence | Source class | Minimum credibility |
|---|---|---|---|
| — → `SUBMITTED` | `planning_application_submitted` present on the spine | REPD (frozen) | 1.0 |
| `SUBMITTED` → `CONSENTED` | `planning_permission_granted` present on the spine, **or** an `OFFICIAL_PLANNING_DATA` / `OFFICIAL_PLANNING_AGGREGATOR` record with an explicit decision of grant | REPD or register | 1.0 |
| `CONSENTED` → `FUNDING_WINDOW` | **any one** funding event: `REGISTERED_CHARGE_CREATED`, `PSC_CORPORATE_CHANGE`, `COMPANY_RENAME`, `DIRECTOR_APPOINTMENT_COUNT_CHANGE`, `SIC_CHANGE_TO_ENERGY`, bound to a project vehicle bound to this project | Companies House filing (`find-and-update.company-information.service.gov.uk`) | 1.0 |
| `FUNDING_WINDOW` → `PROCURING` | **any one**: condition-discharge or reserved-matters application registered against `planning_application_reference`; NESO connection-register entry moving to an accepted/energised state; LCCC CfD contract; an `ICP` or `PRINCIPAL_CONTRACTOR` role confirmed by a register | `OFFICIAL_PLANNING_*`, `OFFICIAL_CONNECTION_REGISTER`, `OFFICIAL_CFD_REGISTER` | 1.0 |
| `PROCURING` → `DESIGN_FROZEN` | **any one**: notice of commencement / construction-stage approval registered; an `EPC` role confirmed by a register; a construction-phase charge (a second charge post-consent naming a construction lender) | register or Companies House | 1.0 |
| `DESIGN_FROZEN` → `UNDER_CONSTRUCTION` | REPD status `under construction` **or** an official commencement record | REPD or register | 1.0 |
| `UNDER_CONSTRUCTION` → `OPERATIONAL` | REPD status `operational` | REPD | 1.0 |
| **any → `DISTRESSED`** | **any one**: Gazette insolvency notice (`GAZETTE_INSOLVENCY`), Companies House `administration`/`liquidation`/`gazette strike-off` filing, `planning_permission_refused`, `planning_application_withdrawn`, `planning_permission_expired` | Gazette, Companies House, REPD | 1.0 |
| `DISTRESSED` → anything | **only** an explicit official record of discharge/restoration/new consent, and only forward to `CONSENTED` | register | 1.0 |

Skipping is permitted where evidence justifies it (a project can go `CONSENTED → PROCURING` if procurement evidence
lands before any funding evidence). Regression other than to `DISTRESSED` is **forbidden**; a state never goes
backwards on the same evidence generation.

### 9.4 Draft contract file

```json
{
  "schema": "pipelinenews.project-window-lifecycle.v1",
  "generation": "<12-digit Europe/London stamp>",
  "deployment": "not-authorised",
  "promotion_eligible": false,
  "owner": "Ventusltd/pipelinenews",
  "purpose": "Refine the frozen five-value project lifecycle into eight evidence-gated commercial states without mutating the REPD spine.",
  "spine": {
    "repository": "Ventusltd/pipelinenews",
    "release": "9.1",
    "project_count": 7680,
    "capacity_mw": 356474.09,
    "build_manifest": "data/manifests/202608261927-build-manifest-v9-1.json",
    "projects_sha256": "24484ca837ac56520ba971fb2c2c1d29620e16a3c71bbaa5764e94c9b515ad52",
    "spine_mutation_allowed": false
  },
  "states": ["SUBMITTED","CONSENTED","FUNDING_WINDOW","PROCURING","DESIGN_FROZEN","UNDER_CONSTRUCTION","OPERATIONAL","DISTRESSED"],
  "non_state": "ABSTAIN",
  "default_state_rule": "REPD_DERIVED_ONLY",
  "legacy_mapping": {
    "LIVE_PRE_CONSTRUCTION": ["SUBMITTED","CONSENTED","FUNDING_WINDOW","PROCURING","DESIGN_FROZEN"],
    "UNDER_CONSTRUCTION": ["UNDER_CONSTRUCTION"],
    "OPERATIONAL": ["OPERATIONAL"],
    "INACTIVE": ["DISTRESSED"],
    "UNKNOWN": ["ABSTAIN"]
  },
  "evidence_classes": {
    "REPD_FROZEN": 1.0,
    "OFFICIAL_PLANNING_DATA": 1.0,
    "OFFICIAL_PLANNING_AGGREGATOR": 1.0,
    "OFFICIAL_CONNECTION_REGISTER": 1.0,
    "OFFICIAL_CFD_REGISTER": 1.0,
    "OFFICIAL_STATUTORY_NOTICE": 1.0,
    "OFFICIAL_COMPANY_FILING": 1.0
  },
  "law": {
    "state_change_requires_official_evidence": true,
    "news_may_change_state": false,
    "name_match_may_change_state": false,
    "proximity_may_change_state": false,
    "llm_may_change_state": false,
    "regression_forbidden_except_distressed": true,
    "distressed_precedence": "ABSOLUTE",
    "insufficient_evidence": "ABSTAIN",
    "contradictions_coexist": true,
    "no_row_overwrites_another": true
  }
}
```

---

## 10. STEP 1 — the register adapter (procurement signal)

**Why first:** it is the only step whose engine already exists and passes a gate. It turns the *procurement* signal
into data with no new privacy surface and no new acquisition risk beyond a rate-limited public API.

### 10.1 What to reuse unchanged

- `attributionv1/modules/register-ingest.mjs` — domain policy, three-output shape, abstention rule
- `attributionv1/modules/attribution-ledger.mjs` — normalisation, id derivation, person-key guard, coexistence
- `attributionv1/contracts/register-ingest.v1.json` and `attribution-role.v1.schema.json`
- `attributionv1/tests/check_batch5_attribution.mjs`, `check_batch6_registers.mjs`

### 10.2 What must be added

1. **A live fetcher.** The module ingests *records*; nothing produces them. A fetcher must:
   - take the spine's `planning_authority` + `planning_application_reference` + `repd_postcode` as the query keys
   - call PlanIt (`https://www.planit.org.uk/api/applics/json`) and/or planning.data.gov.uk
   - obey the sector-intelligence limits pattern: bounded request count, 5 s timeout, ≤1 MB response, 0 redirects,
     no raw HTML retained
   - emit records in the exact fixture shape (`source_type, repd_ref, gg_project_id, role?, organisation?,
     company_number?, effective_from?, event_type?, event_date?, evidence_url, observed_at, source_ref`)
2. **A source card** in `spiders/docs/sources/planit.md` and `planning_data_gov_uk.md` before either is used —
   `EXTERNAL_SOURCE_RULES.md` requires it, and neither card exists today.
3. **A second event vocabulary** for procurement events (see 10.3), because today only `gazette` produces
   `organisation_events`.
4. **A window-state writer** that consumes roles + events and emits the state (see §12).

### 10.3 Draft: procurement event vocabulary

Add to a successor of `register-ingest.v1.json`. Every value is a *thing an official register publishes*, never an
interpretation.

```
PLANNING_DECISION_GRANTED         PLANNING_DECISION_REFUSED
PLANNING_APPLICATION_WITHDRAWN    PLANNING_PERMISSION_EXPIRED
CONDITION_DISCHARGE_APPLIED       CONDITION_DISCHARGE_APPROVED
RESERVED_MATTERS_APPLIED          RESERVED_MATTERS_APPROVED
NON_MATERIAL_AMENDMENT            SECTION_106_COMPLETED
COMMENCEMENT_NOTICE               CONNECTION_OFFER_ACCEPTED
CONNECTION_REGISTER_STATUS_CHANGE CFD_CONTRACT_SIGNED
```

`CONDITION_DISCHARGE_*` and `RESERVED_MATTERS_*` are the highest-value procurement tells: a discharge application
against a drainage, cabling, access or grid-connection condition is a developer buying design work **right now**.

### 10.4 Draft: fetcher skeleton (review only, do not install)

```js
// DRAFT — pipelinenews/discovery/javascript/<generation>-register-fetch.mjs
// Fetches only. Never decides a state. Never writes a role. Emits records for register-ingest.mjs.

export const REGISTER_FETCH_CONTRACT = Object.freeze({
  schema: "pipelinenews.register-fetch.v1",
  generation: "<stamp>",
  deployment: "not-authorised",
  limits: {
    maximum_network_requests: 200,      // one page per selected project per run
    maximum_concurrency: 3,
    request_timeout_ms: 5000,
    maximum_response_bytes: 1048576,
    redirects: 0,
    retained_raw_html_bytes: 0,
    maximum_selected_projects: 200
  },
  selection: {
    // only projects where the procurement signal can exist at all
    lifecycle_in: ["LIVE_PRE_CONSTRUCTION"],
    minimum_capacity_mw: 5,
    requires: ["planning_authority", "planning_application_reference"]
  },
  sources: ["planit", "planning_data"],
  empty_result_means_no_activity: false   // absence is never evidence
});

export async function fetchRegisterRecords(project, { now, fetchImpl }) {
  // 1. build the query from OFFICIAL keys only
  const ref = String(project.planning_application_reference || "").trim();
  const lpa = String(project.planning_authority || "").trim();
  if (!ref || !lpa) return { records: [], abstained: [{ gg_project_id: project.gg_project_id,
    reason: "NO_OFFICIAL_PLANNING_REFERENCE" }] };

  // 2. one bounded request; caller enforces concurrency and timeout
  // 3. map ONLY explicit fields; anything absent -> omit, never guess
  // 4. every emitted record carries evidence_url on the policy domain and observed_at = now
  // 5. return { records, abstained }
}
```

### 10.5 Acceptance gate for Step 1

```
node <generation>-check-register-live.mjs
```

- fixture gates `check_batch5` and `check_batch6` still pass byte-identically
- every emitted record survives `ingestRegisterRecords` without throwing
- 0 roles carry `evidence_kind: OFFICIAL_STATUTORY_NOTICE`
- 0 rows contain a person-keyed field (re-assert `assertNoPersonKeys`)
- abstentions ≥ 1 on a project deliberately missing `planning_application_reference`
- a project with two conflicting official roles retains both
- `deployment: not-authorised` in the emitted manifest
- deterministic rebuild: run twice, byte-identical output

---

## 11. STEP 2 — the project-vehicle filing watch (funding signal)

**This is the step the brief is really about, and it is blocked on acquisition.** See `companies-engine.md` §5 for
the full design; this section states only what the window layer needs from it.

### 11.1 The distinction that governs the design

The `companies` repository pulls balance-sheet fields for entities over £10m and excludes directors and PSCs on
privacy grounds. **That is correct for its demand view and must not change.**

A **project vehicle** is different. An SPV owning a consented park has no trade, so its filing history *is* the
project's biography:

| Filing | What it means for the project | Lead time vs trade press |
|---|---|---|
| **Charge registered** (MR01) | A lender arrived | months before a compound application, ~a year before a press release |
| **Corporate PSC change** | Developer sold, or a fund took control | months |
| **Company rename** | Rebadging on acquisition or at financial close | weeks to months |
| **Director appointment count change** | Integration — the buyer putting its people in | weeks |
| **SIC change into an energy code** | Vehicle activated | variable |
| **Administration / liquidation / strike-off** | The end | immediate, and it always wins |

These are **public corporate filings about a company**, not personal data. The narrow, separate projection designed
in `companies-engine.md` §4 keeps them entirely apart from the private balance-sheet view and keeps every
person-level field excluded — including **individual** PSCs, whose *existence and change count* may be recorded but
whose identity may not.

### 11.2 The corporate-events adapter (draft)

Extends the existing `organisation_events` shape. Same id derivation, same coexistence law, same abstention rule.

```js
// DRAFT — pipelinenews/<generation>/modules/corporate-events.mjs
// Consumes rows from the companies project-vehicle projection.
// Emits organisation_events. NEVER emits a role. NEVER emits a person field.

const COMPANY_REGISTER = "find-and-update.company-information.service.gov.uk";

export const CORPORATE_EVENT_TYPES = Object.freeze([
  "REGISTERED_CHARGE_CREATED",
  "REGISTERED_CHARGE_SATISFIED",
  "PSC_CORPORATE_CHANGE",          // corporate PSC only; individual PSC -> count delta, no identity
  "PSC_STATEMENT_CHANGE",
  "COMPANY_RENAME",
  "DIRECTOR_APPOINTMENT_COUNT_CHANGE",
  "SIC_CHANGE",
  "ACCOUNTS_TYPE_CHANGE",
  "COMPANY_STATUS_CHANGE",
  "ADMINISTRATION",
  "LIQUIDATION",
  "STRIKE_OFF_PROPOSED",
  "STRIKE_OFF_DISCONTINUED"
]);

// Which events may move a project into FUNDING_WINDOW.
export const FUNDING_EVIDENCE = new Set([
  "REGISTERED_CHARGE_CREATED",
  "PSC_CORPORATE_CHANGE",
  "COMPANY_RENAME",
  "DIRECTOR_APPOINTMENT_COUNT_CHANGE",
  "SIC_CHANGE"
]);

// Which events are terminal. These always win.
export const DISTRESS_EVIDENCE = new Set([
  "ADMINISTRATION", "LIQUIDATION", "STRIKE_OFF_PROPOSED"
]);

export function normaliseCorporateEvent(record) {
  assertNoPersonKeys(record);                                    // reuse attribution-ledger guard
  if (record.source_domain !== COMPANY_REGISTER)
    throw new Error("corporate event source must be the official company register");
  if (!CORPORATE_EVENT_TYPES.includes(record.event_type))
    throw new Error(`unsupported corporate event: ${record.event_type}`);
  if (!String(record.organisation ?? "").trim())
    throw new Error("corporate event requires an organisation");
  if (!/^[A-Z0-9]{8}$/.test(String(record.company_number ?? "")))
    throw new Error("corporate event requires a Companies House company number");

  // Identity of the project is NOT established here. It is carried as a candidate binding
  // and resolved by the vehicle-binding step, which may ABSTAIN.
  const identity = [record.company_number, record.event_type, record.event_date,
                    record.source_ref, record.observed_at].join("\n");
  return {
    organisation_event_id: `PN-ORG-EVENT-${sha256(identity).slice(0, 20).toUpperCase()}`,
    company_number: String(record.company_number),
    organisation: String(record.organisation).trim(),
    event_type: record.event_type,
    event_date: record.event_date ?? null,
    // binding is a separate, abstainable decision:
    candidate_gg_project_ids: [...new Set(record.candidate_gg_project_ids || [])].sort(),
    gg_project_id: record.binding_status === "PRIMARY_MATCH" ? record.gg_project_id : null,
    binding_status: record.binding_status,        // PRIMARY_MATCH | ABSTAIN | REJECTED
    binding_evidence: record.binding_evidence,    // what proved it; required for PRIMARY_MATCH
    evidence_url: record.evidence_url,
    evidence_domain: COMPANY_REGISTER,
    evidence_kind: "OFFICIAL_COMPANY_FILING",
    credibility: 1,
    observed_at: record.observed_at
  };
}
```

Note the deliberate reuse of `binding_status ∈ {PRIMARY_MATCH, ABSTAIN, REJECTED}` from
`discoveryv1/contracts/discovery-mention.v1.schema.json`. **A name match is not a binding.** The 475,596
`PROJECT_NAME_SPV_CANDIDATE` edges in the companies candidate are all, correctly, `ABSTAIN` today; the vehicle
binding rule that can promote a subset of them to `PRIMARY_MATCH` is designed in `companies-engine.md` §6.

### 11.3 Acceptance gate for Step 2

- 0 rows with a director name, date of birth, residential address or individual PSC identity
- every event carries `evidence_domain === "find-and-update.company-information.service.gov.uk"`
- an event whose binding is `ABSTAIN` carries `gg_project_id: null` and is still retained
- a charge event produces a `LENDER` role **only** through `attributionsFromRegisteredCharge`, and
  `financial_close_inferred_from_charge_alone` remains `false`
- an `ADMINISTRATION` event on a bound vehicle drives the project to `DISTRESSED` in the same generation
- deterministic rebuild, byte-identical

---

## 12. STEP 3 — the state machine and the ranked output

### 12.1 The evidence-order state machine

Precedence, highest first. Evaluated per project, per generation, over all evidence with
`observed_at <= generation_anchor`.

```
 0. DISTRESS          -> DISTRESSED            (absolute; nothing overrides it)
 1. REPD_TERMINAL     -> OPERATIONAL | UNDER_CONSTRUCTION
 2. FREEZE            -> DESIGN_FROZEN
 3. PROCUREMENT       -> PROCURING
 4. FUNDING           -> FUNDING_WINDOW
 5. CONSENT           -> CONSENTED
 6. SUBMISSION        -> SUBMITTED
 7. (nothing)         -> ABSTAIN
```

Draft implementation:

```js
// DRAFT — pipelinenews/<generation>/modules/window-state-machine.mjs
// Pure. No IO. No network. Deterministic. Given evidence, returns a state and its proof.

const ORDER = ["DISTRESSED","OPERATIONAL","UNDER_CONSTRUCTION","DESIGN_FROZEN",
               "PROCURING","FUNDING_WINDOW","CONSENTED","SUBMITTED"];

export function resolveWindowState(project, evidence, { anchor }) {
  const at = (e) => e.event_date || e.effective_from || e.observed_at;
  const seen = evidence.filter(e => at(e) <= anchor);

  // 0. distressed always wins — checked first, returned immediately
  const distress = seen.filter(e => DISTRESS_EVIDENCE.has(e.event_type)
                                 || REPD_TERMINAL_NEGATIVE.has(e.event_type));
  if (distress.length || project.planning_permission_refused
                      || project.planning_application_withdrawn
                      || project.planning_permission_expired) {
    return decided("DISTRESSED", distress, "DISTRESS_PRECEDENCE_ABSOLUTE");
  }

  if (project.operational)          return decided("OPERATIONAL",        [], "REPD_FROZEN");
  if (project.under_construction)   return decided("UNDER_CONSTRUCTION", [], "REPD_FROZEN");

  const freeze      = seen.filter(e => FREEZE_EVIDENCE.has(e.event_type));
  if (freeze.length)      return decided("DESIGN_FROZEN",  freeze,      "FREEZE_EVIDENCE");

  const procurement = seen.filter(e => PROCUREMENT_EVIDENCE.has(e.event_type));
  if (procurement.length) return decided("PROCURING",      procurement, "PROCUREMENT_EVIDENCE");

  const funding     = seen.filter(e => FUNDING_EVIDENCE.has(e.event_type)
                                    && e.binding_status === "PRIMARY_MATCH");
  if (funding.length && project.planning_permission_granted)
                          return decided("FUNDING_WINDOW", funding,     "FUNDING_EVIDENCE_AFTER_CONSENT");

  if (project.planning_permission_granted)   return decided("CONSENTED", [], "REPD_FROZEN");
  if (project.planning_application_submitted) return decided("SUBMITTED", [], "REPD_FROZEN");
  return { state: null, decision: "ABSTAIN", reason: "NO_SUFFICIENT_EVIDENCE", proof: [] };
}

function decided(state, proof, reason) {
  return {
    state,
    decision: "DECIDED",
    reason,
    proof: proof.map(e => ({
      evidence_id: e.organisation_event_id || e.attribution_id,
      evidence_kind: e.evidence_kind,
      evidence_url: e.evidence_url,
      event_type: e.event_type || null,
      observed_at: e.observed_at
    })).sort((a, b) => a.evidence_id.localeCompare(b.evidence_id))
  };
}
```

Invariants the gate must assert:

- the function is **pure** — same inputs, same output, no clock read, no network
- `DISTRESSED` is returned before any other branch can run
- a state is never returned without either REPD-frozen fields or at least one `PRIMARY_MATCH` proof row
- `FUNDING_WINDOW` is impossible without `planning_permission_granted`
- an `ABSTAIN` project keeps its REPD-derived legacy `lifecycle` and is **not** shown as a window project
- state regression between two generations, other than to `DISTRESSED`, is an error and fails the build

### 12.2 The estimated design-freeze date (clearly derived, never declared)

Freeze is the thing being sold against, and it is not published by anyone. It must therefore be an **estimate,
labelled as one, with its inputs visible**.

```
freeze_estimate_at = consent_date + technology_lead_days(technology, capacity_band)
freeze_estimate_confidence = LOW | MEDIUM | HIGH
```

`HIGH` only when a procurement event has landed (state ≥ `PROCURING`); `MEDIUM` when funding evidence has landed;
`LOW` otherwise. The lead-day table must be **calibrated from the spine itself** — for every project that reached
`under construction`, measure `under_construction - planning_permission_granted` and take the median per
`(technology, capacity_band)`. That calibration is computable today from the 7,680-record spine with no new source.
It is a build task, not a guess, and its output belongs in the contract as a pinned table with the calibration
sample size per cell.

**Until that calibration is run, `freeze_estimate_at` must be null and alerts 2 and 3 must be disabled.** Recorded
in `questions.md` Q5.

### 12.3 The ranker

Ranks **projects**, not sources. Reuses `credibilityForDomain` and `eventConfidence` unchanged for the evidence
term. Draft weightings, all explicit and all tunable in the contract, never in code:

```
window_score =  w1 * state_weight
             +  w2 * evidence_confidence
             +  w3 * freshness
             +  w4 * capacity_weight
             +  w5 * proximity_to_freeze
             -  w6 * distress_penalty
```

| Term | Definition | Draft weight |
|---|---|---|
| `state_weight` | `FUNDING_WINDOW` 1.00 · `PROCURING` 0.85 · `CONSENTED` 0.45 · `DESIGN_FROZEN` 0.20 · `SUBMITTED` 0.10 · `UNDER_CONSTRUCTION` 0.05 · `OPERATIONAL` 0.00 · `DISTRESSED` 0.00 | **w1 = 0.40** |
| `evidence_confidence` | `eventConfidence(proof)` — max source credibility + 0.05 per extra distinct domain, capped 0.2, ceiling 1 | **w2 = 0.20** |
| `freshness` | `max(0, 1 - age_days / 90)` on the newest proof row | **w3 = 0.15** |
| `capacity_weight` | `min(1, log10(1 + capacity_mw) / log10(501))` — 1 MW ≈ 0.11, 50 MW ≈ 0.63, 500 MW ≈ 1.00 | **w4 = 0.15** |
| `proximity_to_freeze` | `0` if `freeze_estimate_at` is null; else `clamp(0, 1, 1 - days_to_freeze / 180)` | **w5 = 0.10** |
| `distress_penalty` | `1` if state is `DISTRESSED`, else `0` | **w6 = 1.00** |

Weights sum to 1.00 before the penalty. `DISTRESSED` therefore scores ≤ 0 and sorts last **and** is surfaced
separately, because "stop selling" is itself an alert.

Rules:
- the ranker **never** changes a state, a binding or an identity
- a project with `decision: "ABSTAIN"` is not ranked at all — it does not appear with score 0, it does not appear
- ties break on `capacity_mw` desc, then `repd_ref` ascending numeric — deterministic
- the score and every term are emitted alongside the rank, so a salesperson can see *why*

Draft contract fragment:

```json
"ranker": {
  "schema": "pipelinenews.window-ranker.v1",
  "weights": { "state": 0.40, "evidence": 0.20, "freshness": 0.15,
               "capacity": 0.15, "freeze_proximity": 0.10, "distress_penalty": 1.00 },
  "state_weight": { "FUNDING_WINDOW": 1.00, "PROCURING": 0.85, "CONSENTED": 0.45,
                    "DESIGN_FROZEN": 0.20, "SUBMITTED": 0.10, "UNDER_CONSTRUCTION": 0.05,
                    "OPERATIONAL": 0.00, "DISTRESSED": 0.00 },
  "freshness_horizon_days": 90,
  "capacity_reference_mw": 500,
  "freeze_horizon_days": 180,
  "abstain_is_not_ranked": true,
  "ranker_may_change_state": false,
  "ranker_may_establish_identity": false,
  "tie_break": ["capacity_mw DESC", "repd_ref ASC"]
}
```

### 12.4 Draft hardening of the person-key guard

`assertNoPersonKeys` currently allows `persons_entitled` (charges) because the regex requires `person` as a whole
token. That is correct behaviour but accidental. Draft: add an explicit allowlist so the intent is legible and a
future field cannot slip through.

```js
const PERSON_KEY = /(^|_)(person|persons|individual|officer|officers|director|directors|
                          dob|date_of_birth|residential|name_of_person)($|_)/iu;
const ORGANISATION_ALLOWLIST = new Set(["persons_entitled"]);  // CH charge field; always an org in practice
```

with a gate asserting that every value under `persons_entitled` is a non-empty string and that the key appears only
on records whose `evidence_kind === "REGISTERED_CHARGE_NAMED_SECURED_PARTY"`.

### 12.5 The three alerts

All three are **derived rows in an alerts dataset**, never emails, never pushes, in this generation. Delivery is a
later decision.

| # | Alert | Fires when | Payload | Precondition |
|---|---|---|---|---|
| 1 | **WINDOW_ENTRY** | a project transitions into `FUNDING_WINDOW` in this generation | `gg_project_id`, `repd_ref`, `name`, `capacity_mw`, `technology`, `planning_authority`, the **proof rows** that caused it, `window_score`, `rank` | none — available as soon as Steps 1+2 land |
| 2 | **THIRTY_DAYS_TO_FREEZE** | `freeze_estimate_at - generation_anchor ∈ [0, 30] days` **and** state ∈ {`FUNDING_WINDOW`, `PROCURING`} **and** no freeze alert already fired for this project | as above plus `freeze_estimate_at`, `freeze_estimate_confidence`, `days_to_freeze` | **blocked on the freeze calibration (§12.2)** |
| 3 | **FREEZE_OVERDUE** | `generation_anchor > freeze_estimate_at` **and** state still ∈ {`FUNDING_WINDOW`, `PROCURING`} | as above plus `days_overdue` and the reason the estimate may be wrong (`no_procurement_evidence` / `no_commencement_record`) | **blocked on the freeze calibration** |

Alert law:

- an alert is a **claim about our own model**, not about the project. Alert text must say
  *"estimated design freeze"*, never *"design freeze"*
- an alert never fires from an `ABSTAIN` project
- an alert never fires twice for the same `(gg_project_id, alert_type, state)` — dedupe key
- `DISTRESSED` cancels every open alert for that project and emits one `WINDOW_CLOSED` row instead
- the alerts dataset is `deployment: not-authorised` and has **no** browser projection until it has run silently for
  at least two generations and been eyeballed. *"Stay silent until both are on the record"* is a product rule and it
  applies to us first.

### 12.6 Output datasets (draft, three tables, sector-intelligence physical pattern)

```
releases/data/window/{generation}/project-window-state/{generation}-part-000.parquet
releases/data/window/{generation}/window-evidence/{generation}-part-000.parquet
releases/data/window/{generation}/window-alerts/{generation}-part-000.parquet
```

**project_window_state** — grain: one resolved state per project per generation. Key `(gg_project_id, generation)`.

| column | type | note |
|---|---|---|
| gg_project_id | VARCHAR | `GG2050-REPD-{repd_ref}` |
| repd_ref | VARCHAR | join key to gridatlas |
| generation | VARCHAR | 12-digit stamp |
| state | VARCHAR | one of the eight, or NULL when ABSTAIN |
| decision | VARCHAR | `DECIDED` \| `ABSTAIN` |
| reason | VARCHAR | precedence branch taken |
| previous_state | VARCHAR | from the previous generation, NULL on first run |
| entered_state_at | DATE | date of the earliest proof row for this state |
| legacy_lifecycle | VARCHAR | the frozen spine value, unchanged |
| freeze_estimate_at | DATE | NULL until calibrated |
| freeze_estimate_confidence | VARCHAR | `LOW`\|`MEDIUM`\|`HIGH`\|NULL |
| window_score | DOUBLE | NULL when ABSTAIN |
| window_rank | BIGINT | NULL when ABSTAIN |
| proof_count | BIGINT | |

**window_evidence** — grain: one proof row backing one state decision.
Key `(gg_project_id, generation, evidence_id)`. Columns: `evidence_id, evidence_kind, evidence_domain, evidence_url,
event_type, event_date, observed_at, credibility, binding_status, company_number`.
`company_number` is nullable and present only for `OFFICIAL_COMPANY_FILING` rows.

**window_alerts** — grain: one alert. Key `(gg_project_id, alert_type, generation)`.
Columns: `alert_type, fired_at, state, previous_state, freeze_estimate_at, days_to_freeze, window_score,
window_rank, dedupe_key`.

Hard gates (copy the sector-intelligence pattern exactly): rows equal distinct declared keys; zero null declared
keys; ZSTD; DuckDB 1.3.2; landed readback required; `IMMUTABLE_FULL_GENERATION_WRITE_FROM_EMPTY_TARGET`;
`WRITE_STAGE → DUCKDB_AUDIT → PUBLISH → DUCKDB_LANDED_READBACK`.

---

## 13. STEP 4 — grid and contractor exposure

Only after Steps 1–3 are green. This is where the ranked list becomes a sales conversation, and it is the first
step that touches the map's *other* data.

### 13.1 Grid exposure

For each project in `FUNDING_WINDOW` or `PROCURING`, compute against the pinned `data-gridatlas` topology:

| Metric | Source | Note |
|---|---|---|
| nearest substation and distance | `partitions/grid_substations.parquet` (5,800 rows) | straight-line; explicitly **not** a route |
| nearest 132 kV / 275 kV / 400 kV line and distance | `derived/grid_{132,275,400}kv_snapped.parquet` | pre-snapped topology |
| voltage of the nearest circuit | same | |
| whether a connection-register entry exists | NESO via the register adapter | `ABSTAIN` if not found — absence is not evidence |

Discipline: distance is **screening-grade** (`spiders/docs/os/SPIDER_SENSES.md` and the source-card doctrine both
require this framing). It never certifies a connection, a route or a cost. It is a conversation opener: *"this 49 MW
site sits 2.1 km from a 132 kV circuit and entered the funding window three weeks ago."*

### 13.2 Contractor exposure

From the attribution roles already produced in Step 1:

- which `ICP`, `PRINCIPAL_CONTRACTOR`, `EPC`, `OM_PROVIDER` organisations are named on projects in each state
- how many projects each organisation is named on, by state and by capacity
- which organisations appear on `DISTRESSED` projects (a supplier's exposure to a failing developer)

All from `CONFIRMED` register roles only. `REPORTED` roles appear in the discrepancy view, never in the exposure
count. No person is named anywhere.

### 13.3 What Step 4 must not do

- must not join a company to a project by name similarity to produce a contractor claim
- must not compute a credit, bankability or risk score for any organisation
  (`companies` README: *"no public credit or bankability score is produced"*)
- must not present distance as a connection cost or a connection likelihood

---

## 14. Build sequence with gates

| Step | Deliverable | Gate | Blocks |
|---|---|---|---|
| **0** | `project-window-lifecycle-v1.json` contract + legacy mapping proof | mapping covers all five legacy values; spine sha256 unchanged | nothing |
| **1** | register fetcher + source cards + procurement event vocabulary + live-run manifest | §10.5 | needs source cards first |
| **2** | companies project-vehicle projection (`companies-engine.md` §4) + corporate-events adapter | §11.3 | **blocked on acquisition — see `companies-engine.md` §5** |
| **3a** | `window-state-machine.mjs` + purity/precedence gate | §12.1 invariants | needs 1 or 2 (either alone yields a partial but valid state) |
| **3b** | freeze calibration from the spine | median lead per (technology, capacity band) with sample sizes ≥ 30 per cell, else cell is NULL | needs only the spine — **can be done immediately** |
| **3c** | ranker + three datasets + alerts 1 (2 and 3 gated on 3b) | §12.6 hard gates; two silent generations before any projection | needs 3a, 3b |
| **4** | grid + contractor exposure | screening-grade labelling asserted; no score, no route, no person | needs 3c |
| **5** | gridatlas cartridge (`DRAFT-CARTRIDGES/window-intelligence`) | browser gate per `NEXT-VERSION.md` | needs 3c published |

**The single item that can start tonight with no dependency, no new source and no privacy question is 3b — the
freeze calibration.** It is pure arithmetic over a frozen file already in the repository, and it converts two of the
three alerts from impossible to possible.

---

## 15. What this layer must never do

Carried forward verbatim from the existing contracts, because these are the reasons the system is trustworthy:

- a state change requires an official record; news, a name match, proximity or an LLM never changes a state
- credibility ranks evidence, never identity (`credibility_may_gate_identity: false`)
- contradictions coexist; no row overwrites another
- absence of a row means the bounded generator emitted no assertion — **never** that nothing happened
- a registered charge confirms a named secured party on a date; it does not confirm financial close
- a statutory notice is an organisation event, not a delivery role
- organisations, never people; no director names, no dates of birth, no residential addresses, no individual PSC
  identities, no credit or bankability scores
- not authorised by default; nothing is promoted without a browser-proved or DuckDB-readback gate
- every generation is write-once and rolled back by discarding it
