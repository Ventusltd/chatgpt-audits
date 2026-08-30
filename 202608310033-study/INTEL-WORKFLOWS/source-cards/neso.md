# NESO Connection Register Source Card

> **DRAFT — for review, then it replaces the stub at `spiders/docs/sources/neso.md`.**
> The existing stub records `Primary URL: study required` and `Licence: study required`. Nothing was fetched.

Document type: source-card

Source name: NESO (National Energy System Operator) data portal — connection register and related datasets

Publisher / owner: National Energy System Operator

Primary URL: `https://api.neso.energy/api/3/action/datastore_search` *(the CKAN datastore API — the endpoint form
already domain-pinned in the register adapter fixture)*

Source-card status: draft — the existing stub must be replaced, not amended

Last checked: not checked — no network access permitted in this session

Licence: NESO publishes open data under terms that generally follow OGL-style re-use. *Verify per dataset — CKAN
portals commonly carry a per-resource licence field, and it must be read per dataset rather than assumed for the
portal.*

Attribution requirement: attribution to NESO. *Verify wording.*

Access method: public HTTPS CKAN datastore API returning JSON; also bulk CSV resources

API key required: *verify* — believed not required for public datasets

Rate limit or access limit: *verify.* Declare a ceiling regardless: **≤ 100 requests per run, concurrency 2, 5 s
timeout, ≤ 1 MB per response, 0 redirects.** Prefer a **single bulk resource fetch** over per-project queries where
the dataset supports it — one request for the whole register is both cheaper and kinder than 400 lookups.

Data type: transmission and distribution connection register entries — project name, connection site, contracted
capacity, agreed connection date, connection status; plus TEC register, embedded register and related datasets

Update frequency: periodic, dataset-dependent — commonly monthly or quarterly. *Verify.*

Field list: *verify per dataset.* Expect at minimum: project name, customer name, connection site / substation,
MW contracted, agreed connection date, status, and a project or agreement reference.

Declared fields: what the dataset explicitly publishes

Derived-only fields: **the join to a REPD project.** The connection register keys on the operator's own project
name and connection site, **not** on `repd_ref`. Every binding is derived, and by default `ABSTAIN`.

Known gaps:
- **there is no `repd_ref` in the connection register.** The join must be made on name plus connection site plus
  capacity, which is exactly the kind of name-similarity binding the federation forbids as identity. Expect a low
  bind rate and a high abstention rate, and treat that as correct.
- queue reform has repeatedly changed register structure and status vocabulary
- capacity in the connection register is *contracted* capacity, which need not equal REPD `capacity_mw`

Known failure modes: CKAN resource id changes between publications, schema drift, dataset withdrawn or superseded,
a project present under a name that matches nothing in the spine

Allowed Spider use: **observe and derive.** Establish whether a connection-register entry exists for a project,
and at what stage — a `PROCURING` evidence class in the eight-state model. Also, as a standalone product surface,
show where queue capacity sits relative to the data-centre estate.

Not-allowed Spider use:
- treating a name match as a confirmed project binding
- treating a contracted connection date as a construction date
- presenting register status as an operational fact
- **treating absence of an entry as evidence that no connection exists** — `absence_rule` applies

Screening boundary: the connection register states what has been contracted with the system operator. It is not a
build programme and not a guarantee.

Status: draft

---

## Already wired for this source

`register-ingest.mjs`: `neso: ["neso.energy", "OFFICIAL_CONNECTION_REGISTER"]`, domain-pinned.
`credibility.mjs`: `"neso.energy": 1` and `"nationalgrideso.com": 1`.

The register-ingest fixture already exercises the hard case: two official sources, NESO and LCCC, naming
**different** OWNER organisations for the same project — and `check_batch6_registers.mjs` asserts both survive:

```js
const owners = proof.roles.filter((row) => row.role === "OWNER");
assert.equal(owners.length, 2);
assert.equal(new Set(owners.map((row) => row.organisation)).size, 2,
  "officially conflicting owner records must coexist");
```

**That is the behaviour to preserve.** Two official registers disagreeing is normal, and the product's job is to
show the disagreement, not to pick a winner.
