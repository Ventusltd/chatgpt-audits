# UNREVIEWED — Recent Git Push Review

**Generated:** 2026-09-04 22:42 BST  
**Write boundary:** this report is committed only to `Ventusltd/chatgpt-audits`. No product repository was changed.  
**Scope:** recent `gridatlas` pushes from the last independently catalogued working release, v9.106, through live v9.116; adjacent `pipelinenews` and `globalgrid2050` pushes where they affect release truth.  
**Status:** UNREVIEWED. Observations are separated from inferences. Absence of evidence is not treated as evidence of absence.

## Executive verdict

The recent product repairs are mostly well targeted and evidence-driven. The hidden-tab iPhone arrival fix, single DuckDB runtime, attribution clearance and restoration of the V8 layers panel all address real measured failures.

The release machinery is now the weakest part of the system.

**Observed:** v9.115 and v9.116 both deployed successfully while the repository's named cartridge `proof` check failed. On v9.116, Pages finished deployment before the proof finished failing. The failing test is also stale: it hard-codes generation `202609040337` and asserts that `atlas/current.json` still has that generation, while current is `202609042123`.

**Inferred:** the workflow called a gate is functioning as a post-deployment alarm. Therefore v9.116 should currently be described as:

> **LIVE · PRODUCT-SPECIFIC PROOF PASSED · CROSS-REPO PROOF RED · NOT RELEASE-VERIFIED**

This is not evidence that v9.116 itself is broken. It is evidence that the estate cannot presently prove that it is safe.

## Evidence boundary

Primary Grid Atlas range:

- Last catalogued working-verified base: `2d8cc7bacf80a3f20ecfb96ea24548fcea43a19d` — v9.106
- Latest live head: `703337bb927ef870ea03f3eef3a454ca1f9fdfb3` — v9.116
- Intermediate product repair: `b7a40d1f881af202a81f97f65e3d5a895e104391` — v9.115
- Technology/wordmark repair: `64268fd06a0da54ddffbcdaaaee382e314e829f7` — v9.111

Adjacent evidence:

- Pipeline ancestry repair: `7ecb405583919c0d78f532913c3c6c72cc2ed64c`
- Pipeline coordination-only note: `3335fe6f47ae4f7f3052a7dea28e20c9570d9230`
- GlobalGrid catalogue of v9.106: `ab8545145e0e14a0eff0862782517905cd431364`

## Findings

### F-01 — P0 — Public deployment is not gated by the mandatory proof

**Observed**

For Grid Atlas v9.116, commit `703337b` produced five checks:

- `build`: success
- `deploy`: success
- `report-build-status`: success
- `build-one-stage`: success
- `proof`: failure

The Pages deployment completed at approximately 21:26:33 UTC. The proof failed at approximately 21:28:36 UTC. The same split occurred for v9.115: deployment succeeded and proof failed.

The workflow file `.github/workflows/202608312212-cartridge-proof.yml` describes itself as the gate every cartridge cut passes through. Technically, however, it is an independent push workflow. Pages can publish the same pushed commit without waiting for it.

**Inferred**

The live pointer is promoted by the source push, not by proof success. The word “gate” overstates the current control. A red build can be public before the red result exists.

**Required repair**

1. A source push should create or update a **candidate composition**, not the live composition.
2. The complete proof suite should run against that exact candidate.
3. Only a green proof should create a small, auditable promotion commit or invoke a deployment workflow.
4. Pages should deploy from the promoted pointer, not directly from every `main` push.
5. Where repository settings permit, the proof should be a required check before the protected promotion branch can move.

A `workflow_run`-based promotion, or a dedicated `candidate` → `live` pointer transition, would make the control real. Merely rerunning proof after a public push does not.

### F-02 — P0 — The exact Pipeline corpus proof is deterministically stale

**Observed**

The failing step is:

`The exact Pipeline 0144 corpus has honest arrival states`

The test `tools/proofs/202609040229-arrival-identity-corpus.proof.mjs` contains:

- `const GENERATION = '202609040337'`
- a read of current `atlas/current.json`
- `assert.equal(current.generation, GENERATION)`

Current `atlas/current.json` says generation `202609042123`.

The CI job successfully checked out the pinned Pipeline repository and successfully completed the composition and composed-cartridge proof before reaching this assertion. Therefore the CI failure is not explained by the Pipeline repository being absent from the runner.

After this step failed, the following checks were skipped:

- mobile identity, absence, failure and retry browser proof
- docked mobile card/layer-control hit testing
- scope ledger and workflow budget
- deterministic `STATE.md` check
- CRLF and renormalisation checks

**Inferred**

Every generation after `202609040337` is structurally capable of failing this test even when the stable arrival contract has not regressed. The test currently binds a historical contract fixture to the mutable live generation.

This also makes the v9.115/v9.116 commit wording incomplete: the CI runner did have the Pipeline corpus; the red result is reproducible from the hard-coded generation assertion.

**Required repair**

Separate two questions:

1. **Historical corpus contract:** does the pinned Pipeline 0144 corpus still produce the required receiver states against the current receiver implementation?
2. **Current composition identity:** do the current manifest, parts and hashes agree with `atlas/current.json`?

The first should pin corpus bytes and stable source-contract identifiers, but derive the current composition dynamically. The second is already covered by the composition verifier and should not be reimplemented with an obsolete literal generation.

Independent governance checks should also be separate jobs, or use controlled `if: always()` execution, so one corpus assertion cannot silently skip line-ending, state and workflow-budget enforcement.

### F-03 — P1 — GlobalGrid's “v9.106 working verified” link opens v9.116

**Observed**

The current `globalgrid2050/index.html` prominently labels:

`UK Grid Atlas V9.106 — Current Release (Working Verified)`

Its link is the mutable route:

`https://ventusltd.github.io/gridatlas/atlas/`

That route now resolves its composition from generation `202609042123`, v9.116. The text and evidence beside the link still cite v9.106 generation `202609040337` and commit `2d8cc7b`.

**Inferred**

The catalogue transfers old verification evidence to newer bytes. A user selecting a specifically described working-verified v9.106 build is not receiving that build.

**Required repair**

Create a pinned composition route for generation `202609040337` and point the verified v9.106 record to it. Keep a separate dynamic row for `/atlas/`, labelled with its actual current version and proof state.

Suggested public distinction:

- `Grid Atlas v9.106 — working verified` → exact pinned composition
- `Grid Atlas current live — v9.116 — proof red/pending` → mutable live route

Pinned routes already exist for v9.68, v9.74, v9.75, v9.77 and v9.107. The important missing route is the one the catalogue actually calls verified: v9.106.

### F-04 — P1 — Small source repairs cause excessive generated release churn

**Observed**

Between v9.106 and v9.116:

- 6 Git commits advanced the head
- 10 new composition manifests were added
- 17 generated cartridge files were added
- those cartridge files contain approximately **101,094 added lines**

The latest v9.116 commit is the clearest example. Its substantive menu module change is 49 changed lines (`+41/-8`), and the related SLD part changes 21 lines (`+17/-4`). The same commit adds two rebuilt cartridges containing **13,727 lines** in total, plus another full composition manifest and parts manifests.

**Inferred**

The immutable history is valuable, but the current assembly boundary is too coarse. A menu/panel repair is embedded into both the large SLD and substation-intelligence products, forcing both to be restamped. This makes code review, bisecting, storage, change attribution and human verification harder than the actual product change warrants.

**Required repair**

Move the menu bar and shared visual controls into one small independently hashed cartridge loaded after the large functional cartridges. Unchanged content-addressed cartridges should be reused byte-for-byte across compositions.

The target property is:

> one small UI change → one small cartridge, one composition manifest and one proof delta

not:

> one small UI change → two 6–7k-line application restamps

### F-05 — P1 — “Last known green” does not identify a green composition

**Observed**

`atlas/current.json` records:

- `last_known_green.release_id = 202608300453-atlas-v9`
- `last_known_green.route = /gridatlas/atlas/releases/202608300453-atlas-v9/`

That identifies the immutable shell release. It does not identify the verified composition generation, composition version, source commit or proof run. v9.106 through v9.116 all continue to use that shell.

The manual rollback workflow performs `verify-compose`, `run-current` and scope lint before pushing. It does not run the separate exact Pipeline corpus proof or the browser arrival/hit-test checks before push. Its final note says the pushed proof is “the gate”, but the same push can trigger Pages publication before that proof completes.

**Inferred**

An operator cannot mechanically answer “which exact complete composition was last green?” from `last_known_green`. The rollback control also has weaker pre-push parity than the ordinary proof suite it claims to mirror.

**Required repair**

Record at least:

- exact composition generation
- composition version
- source commit SHA
- proof workflow run ID
- proof conclusion and completion time
- immutable pinned route
- predecessor generation

The rollback workflow should default to that exact generation and run the same complete acceptance suite before it pushes any pointer transition.

### F-06 — P2 — Durable state says “done” while mandatory release proof is red

**Observed**

`STATE.md` records `Master: done` and `Active scope: none` for composition `202609042123`. The push's mandatory proof is red. The v9.111 commit message also explicitly retained an open defect: Scope can arm invisibly and clear the reader's selection.

**Inferred**

“Done” currently describes the coding session, not the release state. Future agents may read it as product truth and stop investigating a composition that was never fully proven.

**Required repair**

Use separate state dimensions, for example:

- `BUILD: COMPLETE`
- `PRODUCT_PROOF: PASS`
- `CROSS_REPO_PROOF: PASS/FAIL`
- `PROMOTION: CANDIDATE/LIVE`
- `PUBLIC_VERIFICATION: PASS/PENDING`
- `OPEN_DEFECTS: count + identifiers`

A mandatory red proof should prevent the durable release state from becoming simply `done`.

### F-07 — P2 — One DuckDB runtime, but two copied broker implementations

**Observed**

v9.115 correctly introduces one page-level DuckDB runtime and correctly closes only the search lane's connection during retry, without terminating the database shared by the data plane.

The search cartridge source also states that the broker function is duplicated verbatim from the streaming bridge because no shared module loader exists.

**Inferred**

Runtime ownership is now correct, but source ownership is duplicated. The two implementations can drift while continuing to claim the same window-key contract.

**Required repair**

Extract a tiny, versioned, content-hashed DuckDB runtime-broker module loaded before both consumers. Both lanes should depend on one implementation and an explicit API version, while retaining separate connections.

## Positive findings worth retaining

### P-01 — Hidden-tab iPhone arrival repair is technically sound

The v9.115 design distinguishes wall time from visible time, refuses to spend the arrival budget while hidden, retries on first visibility and retains an absolute ceiling. That addresses the actual `target="_blank"`/iOS compositing failure rather than masking it with a longer arbitrary timeout.

### P-02 — Shared DuckDB lifecycle ownership is correct

The runtime is shared, but each consumer receives its own connection. Search retry closes only its connection and does not terminate the shared database. This is the correct ownership boundary.

### P-03 — V8 layers restoration preserves one behavioural source of truth

v9.116 restores the original V8 panel while keeping the six menus. The Grid menu proxies the original engine inputs rather than cloning layer state, so panel and menu cannot independently disagree about which layer is active.

### P-04 — Measurement-led UI proofs are improving

The attribution fix tests actual occlusion with `elementFromPoint`, not mere DOM presence. The V8 panel proof was written to fail against v9.115 before passing against v9.116. These are useful proof patterns.

### P-05 — Pipeline repair-only ancestry handling is strong

Pipeline commit `7ecb405` walks the immutable release ancestry, detects malformed, missing, cyclic and forward parent chains, and recognises repair-only cartridges through manifest history rather than only supplemental assets. Its routing-without-deployment-authority check passed. This is a good example of fail-closed release logic.

### P-06 — Pinned comparison routes are the right recovery primitive

The additive `/atlas/v/<generation>/` routes make earlier compositions independently testable without moving live. That should become the basis of catalogue truth, regression comparisons and rollback evidence.

## Immediate order of work

1. **Stop calling v9.116 verified.** Keep it live only as `proof red/pending` while the stale test is repaired. Do not infer a product rollback solely from the stale assertion; the product-specific composition proof passed.
2. **Repair the exact Pipeline corpus proof** so it tests current composition bytes against the pinned corpus without asserting that current is still v9.106.
3. **Rerun the complete v9.116 suite** and ensure every previously skipped browser, state, scope and line-ending check executes.
4. **Make publication depend on green proof**, using candidate and promoted pointers rather than deploying every source push.
5. **Correct GlobalGrid identity** by pinning v9.106 and separately labelling current v9.116.
6. **Record exact last-known-green composition identity** and bring rollback pre-push checks to full parity.
7. **Reduce cartridge amplification** by separating menu/UI and the DuckDB broker from the two large functional cartridges.

## Release classification at this audit snapshot

| Item | Classification | Basis |
|---|---|---|
| Grid Atlas v9.106 / `2d8cc7b` | WORKING VERIFIED, but catalogue link not pinned | GlobalGrid verification record exists; mutable link now lands elsewhere |
| Grid Atlas v9.115 / `b7a40d1` | LIVE · PROOF RED · NOT RELEASE-VERIFIED | Pages success and proof failure on same commit |
| Grid Atlas v9.116 / `703337b` | LIVE · PRODUCT-SPECIFIC PROOF PASS · CROSS-REPO PROOF RED | composition/cartridge step passed; stale corpus step failed; later checks skipped |
| Pipeline `7ecb405` | SOURCE CHANGE GREEN · NO DEPLOYMENT AUTHORITY | ancestry tests/check succeeded |
| Pipeline `3335fe6` | COORDINATION NOTE ONLY | only `docs/coordination/BOARD.md` changed; no check runs |

## Final assessment

**Inferred:** the engineering direction is improving, but version velocity has outrun release truth. The next high-value push is not v9.117. It is a release-control repair that makes “green”, “live”, “verified” and “pinned” mean four explicit, mechanically consistent things.
