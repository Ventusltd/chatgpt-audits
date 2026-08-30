# cvaa-integration-plan

How `cvaa` should police `gridatlas`, `pipelinenews`, `companies` and the data repositories: the exact small
workflow each needs, pinned to a cvaa commit SHA (and where that SHA comes from), plus each repository's
`cvaa.json` baseline.

**Drafts and instructions only.** No workflow was written into any repository and no `cvaa.json` was created.

---

## 1. Current state: the registry exists and nobody calls it

| fact | evidence |
|---|---|
| cvaa HEAD | `d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e` — *"202608301726: make full-history fleet audit permanent"* |
| vaccines | **24**, all locked in `vaccines.lock` by sha256 |
| reusable workflow | `Ventusltd/cvaa/.github/workflows/202608301446-inoculate.yml@<sha>` |
| consumer template | `cvaa/consumer-workflow-template.yml` — copy it, replace both SHAs, done |
| repositories with a `cvaa.json` | **1** — cvaa's own |
| repositories calling the reusable workflow | **0** |
| closest thing to adoption | `gridatlas/.github/workflows/202608301321-verify-live.yml`, which checks cvaa out at the pinned SHA and runs `inoculate.mjs . --json --no-write` inline, then requires **7 named vaccines** to be `immune` and `shallow === false` |

`gridatlas/governance/202608301524-cvaa-gridatlas-application.md` describes "active antibodies" — but those are
re-implemented in `tools/scope/loop.mjs`, not run from cvaa. The document is accurate about the *behaviour* and
misleading about the *mechanism*.

### Where the pinned SHA comes from

Three places already carry it, and they agree:

```
gridatlas/STATE.md                         CVAA pin: d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e
gridatlas/atlas/current.json               provenance.cvaa_commit
gridatlas/.github/workflows/…-verify-live.yml   env.CVAA_SHA
gridatlas/state/streaming-road-fix.json    cvaa_commit
```

**Rule for every consumer:** take the SHA from `gridatlas/atlas/current.json` `provenance.cvaa_commit`, or read it
directly with `git -C cvaa rev-parse HEAD` after reviewing the diff. **Never `@main`** — the consumer template says
so in its own comment, and vaccine `no-dangerous-apis` cites CVE-2025-30066 (tj-actions/changed-files, March 2025,
23,000+ repos) as the reason.

---

## 2. The workflow every repository needs

Identical in all twelve. Copy to `<repo>/.github/workflows/<12-digit-stamp>-inoculate.yml`:

```yaml
# Copied from Ventusltd/cvaa/consumer-workflow-template.yml
# Both SHAs are the reviewed Ventusltd/cvaa commit. Never @main.
name: Inoculate against hostile amnesia
on:
  push:
  pull_request:
  schedule:
    - cron: '17 */6 * * *'
  workflow_dispatch:
permissions:
  contents: read
  security-events: write
jobs:
  cvaa:
    uses: Ventusltd/cvaa/.github/workflows/202608301446-inoculate.yml@d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e
    with:
      cvaa_sha: d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e
```

Why this exact shape and nothing more:

- the reusable workflow already checks out **both** the consumer and cvaa with `fetch-depth: 0`, satisfying the
  `full-history-checkout` vaccine — a shallow checkout makes every history vaccine silently report immune
- it runs `node tools/selftest.mjs` in cvaa **before** running the antibodies, so a broken registry fails loudly
- it uploads SARIF under category `cvaa`, so findings appear as code-scanning annotations, not buried logs
- `contents: read` only — the checker never writes
- the cron is `17 */6 * * *`: every six hours, **not** pinned to a calendar day, which is what the
  `no-time-based-gates` vaccine requires
- `workflow_dispatch` is present, which `least-permissions` requires alongside any `schedule`
- `timeout-minutes: 10` lives inside the reusable workflow, satisfying `least-permissions` for the caller

**Two exceptions, both in gridatlas:**

1. `tools/scope/loop.mjs` `validateWorkflowBudget()` asserts the workflow directory contains **exactly**
   `['202608301321-scope-loop.yml', '202608301321-verify-live.yml']`. Adding a third file fails the lint. The
   `ACTIVE_WORKFLOWS` constant in `tools/scope/lib.mjs` must be extended **in the same commit** as the new workflow.
2. The `no-per-release-workflows` antibody exempts filenames matching `/scope-loop|verify-live|inoculate/`, so an
   `…-inoculate.yml` does not count against the timestamped-workflow baseline in any repository. Name it
   accordingly.

---

## 3. Per-repository predicted findings and `cvaa.json` baseline

`cvaa.json` shape (from cvaa's own):

```json
{ "legacy_workflows": <int>,
  "allow": [ { "vaccine": "<slug>", "max": <int>, "expires": "YYYY-MM-DD" } ] }
```

Semantics from `inoculate.mjs`: a `max` **downgrades error to warning** while `findings.length <= max`; an expired
`expires` adds a finding of its own. Baselines may only ratchet **down**. `legacy_workflows` is read only by
`no-per-release-workflows`.

Measured inputs, this workspace, at survey time:

| repo | workflows | timestamped | unpinned `uses:` | jobs w/o timeout | scope files | pointer file | root app copies |
|---|---:|---:|---:|---:|---:|---|---|
| gridatlas | 2 | 2 | **0** | 0 | 8 | `atlas/current.json` | 0 |
| pipelinenews | 44 | 36 | **123** | 1 | 0 | none | 0 |
| companies | 7 | 7 | **0** | 2 | 0 | none | 0 |
| data-gridatlas | 11 | 11 | **0** | 0 | 0 | `releases/current.json` | 0 |
| data-centres-gb | 5 | 4 | **0** | 0 | 0 | none | 0 |
| data-gb-electricity | 2 | 0 | 5 | 0 | 0 | none | 0 |
| data-interconnectors | 1 | 0 | 3 | 0 | 0 | none | 0 |
| gb-electricity-ui | 1 | 0 | 4 | 1 | 0 | none | 0 |
| spiders | 2 | 0 | 2 | 2 | 0 | none | 0 |
| data-federation-map | 8 | 0 | 15 | 5 | 0 | none | 0 |
| globalgrid2050 | **240** | 9 | **440** | **172** | 0 | none | **1** |
| cvaa | 2 | 2 | 4 | 0 | 0 | none | 0 |

Note: `pinned-actions` and `least-permissions` carry `level: warning` intrinsically, so they never fail a build —
but they still appear in SARIF and still need a baseline to stay legible.

### 3.1 `gridatlas` — adopt first, and it will be clean

Predicted findings:

| vaccine | predicted | note |
|---|---|---|
| `one-active-scope` | 0 | master `done`, no active numbered scope |
| `no-app-copies` | 0 | 0 root release dirs, `atlas/` present — the antibody's own worked example, now cured |
| `no-per-release-workflows` | 0 | both files match the `scope-loop\|verify-live` exemption |
| `self-terminating-loops` | 0 | neither workflow has a `schedule:` any more |
| `chaining-token` | **1** | `verify-live.yml` runs `git push` with `secrets.GRIDATLAS_SCOPE_TOKEN \|\| github.token`. The antibody looks for `secrets.\w*PAT\w*`, `app-token`, `create-github-app-token` or `GRIDATLAS_APP` — `GRIDATLAS_SCOPE_TOKEN` matches **none** of those patterns |
| `pointer-verifies` | 0 | `sha256sums.txt` verifies; both cartridges hash-match and are ~17 KB and ~10 KB |
| `derived-state-not-authored` | 0 | `STATE.md` is generated and `loop.mjs` exists |
| `context-diet` | 0 | no `prompt:` block in either workflow |
| `rollback-exists` | **1** | workflows write `atlas/current.json` but nothing matches `/rollback\|roll back\|git checkout .* -- .*current\.json/` |
| `pinned-actions` | 0 (warning) | every `uses:` is a 40-char SHA. Exemplary |
| `least-permissions` | 0 (warning) | both have `permissions:` and `timeout-minutes:` |
| `agent-quarantine` | 0 | no agent action in either workflow |
| `vocabulary` | 0 | statuses are `active`/`done`/`blocked` |
| `monotonic-utc-generations` | **≥ 1** | this is why cvaa's own baseline allows 2; gridatlas has BST/UTC drift in its history |
| `on-ledger-commits` | **likely several** | commits stamped ≥ the first scope generation that name no scope file |
| `executor-declared` | **8** | **no scope file has an `executor:` field.** Every one fails |
| `loop-exists` | **1** | `scope-loop.yml` has no `schedule:` — retired at scope 6 by design. The vaccine says the loop must be perpetual |
| `rollback-exercised` | **1** | no commit subject matches `/roll ?back\|rollback drill/i` |
| `attestation-freshness` | possible | depends on commit subject ordering |
| `full-history-checkout` | 0 | both cvaa-referencing checkouts use `fetch-depth: 0` |
| `no-time-based-gates` | 0 | `MISSION_EXPIRES_AT` was removed; no cron pinned to a day |

Draft `gridatlas/cvaa.json`:

```json
{
  "legacy_workflows": 0,
  "allow": [
    { "vaccine": "executor-declared",          "max": 8, "expires": "2026-10-31" },
    { "vaccine": "on-ledger-commits",          "max": 10, "expires": "2026-10-31" },
    { "vaccine": "monotonic-utc-generations",  "max": 2, "expires": "2026-10-31" },
    { "vaccine": "loop-exists",                "max": 1, "expires": "2026-09-30" },
    { "vaccine": "rollback-exercised",         "max": 1, "expires": "2026-09-30" },
    { "vaccine": "rollback-exists",            "max": 1, "expires": "2026-09-30" },
    { "vaccine": "chaining-token",             "max": 1, "expires": "2026-09-30" }
  ]
}
```

Every entry is a real, short-dated debt with an obvious cure:

- `executor-declared` — add `executor: script` to the eight scope files. `tools/scope/loop.mjs` does not validate
  unknown front-matter keys, so this is additive and safe. **Cure, do not baseline, if there is time.**
- `rollback-exercised` and `rollback-exists` — write one rollback workflow and dispatch it once as a drill. This is
  the single highest-value item in the whole file: a rollback that has never run is not a rollback.
- `chaining-token` — either rename the secret to contain `PAT`, or move to a GitHub App token. Renaming to satisfy a
  regex is the wrong fix; the App token is the right one, because the vaccine's actual point is that a default token
  does not chain workflow runs.
- `loop-exists` — a genuine disagreement between cvaa doctrine ("the loop must be perpetual") and the gridatlas
  closure record ("schedule retired at scope 6"). Baseline it and resolve deliberately; see `questions.md` Q9.

### 3.2 `pipelinenews` — the largest cleanup

Predicted: **123 `pinned-actions` warnings** and **36 timestamped workflows** against a default baseline of 0.
No scope ledger, so `one-active-scope`, `vocabulary`, `executor-declared`, `on-ledger-commits` and `loop-exists`
all return `[]` — they are scope-gated and pipelinenews has no `scope-of-works/`.

Draft `pipelinenews/cvaa.json`:

```json
{
  "legacy_workflows": 36,
  "allow": [
    { "vaccine": "pinned-actions",   "max": 123, "expires": "2026-10-31" },
    { "vaccine": "least-permissions", "max": 5,  "expires": "2026-10-31" }
  ]
}
```

Then ratchet: pin the actions in batches and lower `max` each time. It only goes down.
`legacy_workflows: 36` is an honest record of a graveyard, not permission to grow it — the antibody fires the moment
a 37th appears.

Note pipelinenews already archives aggressively (`.github/workflow-archive/`), so the fastest reduction is moving
inert workflows there rather than editing them.

### 3.3 `companies` — nearly clean, and it matters most

Predicted: `pinned-actions` **0** (all SHA-pinned — the acquisition workflows are exemplary),
`least-permissions` **2** (jobs without `timeout-minutes`), `no-per-release-workflows` **7**.

Draft `companies/cvaa.json`:

```json
{
  "legacy_workflows": 7,
  "allow": [
    { "vaccine": "least-permissions", "max": 2, "expires": "2026-09-30" }
  ]
}
```

This repository will produce the project-vehicle projection. It is the one where a governance regression is most
expensive, and it is already the closest to clean. **Adopt it second, right after gridatlas.**

### 3.4 `data-gridatlas` — clean

`pinned-actions` 0, `least-permissions` 0, 11 timestamped workflows.
It has a pointer (`releases/current.json`), so `pointer-verifies` will run. That antibody reads
`atlas/releases/${pointer.release_id}` and `atlas/${cartridge.path}` — paths that do not exist here — so it will
report `no sha256sums.txt` unless the pointer lacks `release_id`. **Check this before adopting**; it may need a
`pointer-verifies` baseline of 1, or the antibody may need to become gridatlas-shaped-only. Recorded as
`questions.md` Q10.

```json
{ "legacy_workflows": 11, "allow": [] }
```

### 3.5 The four small data repos and spiders

| repo | `legacy_workflows` | allow |
|---|---|---|
| `data-centres-gb` | 4 | `least-permissions` 0 |
| `data-gb-electricity` | 0 | `pinned-actions` 5, expires 2026-09-30 |
| `data-interconnectors` | 0 | `pinned-actions` 3, expires 2026-09-30 |
| `gb-electricity-ui` | 0 | `pinned-actions` 4, `least-permissions` 1, expires 2026-09-30 |
| `spiders` | 0 | `pinned-actions` 2, `least-permissions` 2, expires 2026-09-30 |
| `data-federation-map` | 0 | `pinned-actions` 15, `least-permissions` 5, expires 2026-10-31 |

All are small enough to cure rather than baseline within a day. Prefer curing.

### 3.6 `globalgrid2050` — adopt last, or not yet

240 workflows, 440 unpinned `uses:`, 172 jobs without a timeout, 6 with no `permissions:` block, and **one root
application copy** (`202608300453-atlas-v9`) which trips `no-app-copies` — the mirrored Atlas release. Commit
`ebe024e0 202608301300: use canonical GridAtlas app and remove mirror` suggests this is already being unwound.

Adopting cvaa here today produces hundreds of findings and teaches nothing. Two better options:

1. **Defer.** Adopt after the mirror removal lands and the workflow count is reduced.
2. **Adopt read-only in warning mode** with a large, dated baseline purely to make the size of the debt visible:

```json
{
  "legacy_workflows": 240,
  "allow": [
    { "vaccine": "pinned-actions",    "max": 440, "expires": "2026-12-31" },
    { "vaccine": "least-permissions", "max": 180, "expires": "2026-12-31" },
    { "vaccine": "no-app-copies",     "max": 1,   "expires": "2026-09-30" }
  ]
}
```

Recommendation: **option 2**, because a number that is visible and shrinking beats a number nobody has.

### 3.7 `cvaa` itself

Already immune against itself by contract — the README's recovery instruction is
`node inoculate.mjs .` and *"the registry must report immune against itself"*. Its existing `cvaa.json` allows
`pinned-actions` 6 and `monotonic-utc-generations` 2, both expiring **2026-09-30 — one month from now**. Renew or
cure before then, or every consumer inherits a registry that fails its own gate.

---

## 4. Adoption order and why

| order | repo | reason |
|---|---|---|
| 1 | **gridatlas** | It is the front door, it is already 90 % compliant, and it is the repository whose failures the vaccines were written from. Adopting it converts a re-implementation into a real dependency. Requires the `ACTIVE_WORKFLOWS` edit in the same commit. |
| 2 | **companies** | Nearly clean, and about to grow the project-vehicle projection — the most privacy-sensitive new code in the plan. |
| 3 | **data-gridatlas** | Clean, and it feeds the map. Resolve the `pointer-verifies` shape question first. |
| 4 | **pipelinenews** | Largest cleanup, highest value: it owns the spine, the identity policy and the deep-link contracts. |
| 5 | the four small data repos + spiders | Cure rather than baseline; a day's work in total. |
| 6 | data-federation-map | Moderate debt, no product risk. |
| 7 | globalgrid2050 | Defer or adopt warning-only. |

---

## 5. What cvaa should gain from this survey

Five vaccines this workspace justifies, drafted as candidates for the registry. Each follows the required form:
`vaccines/<12-digit>-<kebab-slug>.md` with front matter (`vaccine`, `generation`, `dose`, optional `level`,
optional `superseded_by`) and the five sections Disease / Symptom / Antibody / Dose / Provenance, then
`node inoculate.mjs --lock`.

### V1 — `consumer-pointer-current`

**Disease.** A consumer hard-codes a producer's release path. The producer reorganises. Every link 404s and nothing
notices, because the consumer's own tests pass.

**Symptom.** `pipelinenews/ui/atlas-v9-deep-links.js` and `companies/state/atlas-v9-link-contract.json` both emit
`https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/` after gridatlas scope 1 moved every release under
`atlas/releases/`. See `intelligence-chain.md` §3.

**Antibody sketch** (data-only, no network — antibodies may not fetch):

```js
export default ({ paths, files }) => {
  // any committed file that embeds a sibling repo's dated release directory
  // directly under the repo root is a hard-coded consumer pointer
  const bad = [];
  for (const p of paths) {
    if (!/\.(json|js|mjs|md|ya?ml)$/.test(p)) continue;
    // the runner would need file text; today ctx exposes only workflows + STATE.
    // This vaccine therefore requires a ctx extension: ctx.pointerRefs, a
    // precomputed list of /github\.io\/[\w-]+\/\d{12}-[\w-]+\// matches.
  }
  return bad;
};
```

**Note:** this needs a small `buildContext` extension in `inoculate.mjs` (a precomputed grep result), because
antibodies get a data-only snapshot and cannot read arbitrary files. That is the right way to add it — the context
is where IO belongs.

### V2 — `search-plane-not-drawing-plane`

**Disease.** A browser data plane that boots a 35.7 MB analytical runtime to draw a map layer. Every layer is then
within a rounding error of its own budget.

**Symptom.** `on_demand_budget_s_at_20mbit` ≥ 14.3 s for **every** partition in `data-gridatlas`, because the
runtime alone is 14.28 s at the declared 20 Mbit reference.

**Antibody.** Given a repo with a `data/manifest.json` and a declared runtime cost, fire when any layer's on-demand
budget exceeds the declared layer budget. This is arithmetic over committed manifests — no network needed.

### V3 — `absence-is-not-evidence`

**Disease.** A projection presents an empty result as a negative fact.

**Symptom.** Cured everywhere it appears in this workspace and worth locking:
`absence_rule` (companies), `empty_result_means_no_mentions: false` (discoveryv1),
`empty_dataset_policy` (sector intelligence), `Unknown is a real state` (spider printer).

**Antibody.** Any contract JSON declaring a dataset must carry an explicit absence rule.

### V4 — `person-key-forbidden`

**Disease.** A dataset about organisations acquires a person-level field, one column at a time.

**Symptom.** Not yet observed — `attribution-ledger.mjs` `assertNoPersonKeys` prevents it at runtime — but the
project-vehicle work in `companies-engine.md` deliberately approaches the line, and the guard currently lives in one
archived module rather than in the registry.

**Antibody.** Fire on any committed contract or schema declaring a column matching
`/(^|_)(person|persons|individual|officer|director|dob|date_of_birth|residential)($|_)/i` unless it appears in a
declared allowlist (today: `persons_entitled`, a Companies House charge field naming a secured party).

### V5 — `source-card-before-fetch`

**Disease.** Product code calls an external host that has never been studied for licence, attribution or rate limit.

**Symptom.** The live gridatlas search cartridge calls `api.postcodes.io` on every keystroke and
`nominatim.openstreetmap.org` on Enter. Neither has a source card in `spiders/docs/sources/`. `repd.md` exists but
records `Licence: study required` for the dataset the entire product is built on.

**Antibody.** Any external hostname appearing in a committed cartridge or fetcher must have a corresponding
source-card path in the declared registry, with `status` not `draft`.

---

## 6. What to do tonight, concretely

1. Read `cvaa/consumer-workflow-template.yml` and confirm `d2ebc01f6eab41f2a84b0c53c4cfae0d2625ec5e` is the commit
   you have reviewed (`git -C cvaa log -1`).
2. Draft `gridatlas/.github/workflows/<stamp>-inoculate.yml` from the template, **and in the same commit** add
   `'<stamp>-inoculate.yml'` to `ACTIVE_WORKFLOWS` in `tools/scope/lib.mjs`, or `loop.mjs lint` fails.
3. Draft `gridatlas/cvaa.json` from §3.1.
4. Run `node work/cvaa/inoculate.mjs . --json --no-write` locally against gridatlas to replace every "predicted"
   above with a measured number, then set each `max` to the measured value rather than my estimate.
5. Renew or cure the two cvaa baselines expiring **2026-09-30**.
6. Only then repeat for `companies`.
