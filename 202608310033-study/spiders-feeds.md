# spiders-feeds

What `Ventusltd/spiders` actually scrapes, which feeds are live and which are stale, and how each could become an
artifact for a cartridge or for the `companies` / `pipelinenews` data.

Read-only survey. Nothing changed.

---

## 1. The honest headline

`spiders` is **not a scraper fleet.** It is a **doctrine repository** with two small working species and ten
source cards, most of them drafts.

| What the brief expects | What is there |
|---|---|
| A set of scrapers feeding the system | Two species: one reads a hand-authored menu, one probes a registry file |
| Live register scraping | **None.** No planning register, no Companies House, no Elexon scraper exists here |
| Feeds that can become cartridge artefacts | Two, and neither is about projects |

That is not a criticism of the repository. Its actual value is the part the rest of the federation is missing: a
**source-card protocol** that says a source may not be used until it has been studied, and a **scanner-mode
protocol** that says a scanner must declare what it is allowed to do before it runs. Those two documents are the
governance that a live register adapter needs, and they exist, and nothing else in the workspace has them.

---

## 2. Inventory

### 2.1 Species

| species | what it does | trigger | state |
|---|---|---|---|
| `spider_maya/v1` | Parses `const AREAS = [` out of the pinned GlobalGrid2050 homepage and emits a declared node/edge graph | `workflow_dispatch` only, with a required `globalgrid_ref` input | **STALE** — last run `20260704T233148Z`, i.e. 2026-07-04, ~8 weeks before this survey |
| `spider_printer_v1` | Weekly smoke check that `registry_of_all_content_in_repos_and_dependencies` still serves `registry/latest.json` and a graph, asserting `repo_count >= 1` and `file_count >= 1` | `schedule: '30 10 * * 1'` (Mondays 10:30) + dispatch | **LIVE**, but it is a *health probe*, not a data feed. It asserts nothing about content and prints totals |
| `species/federation-spider` | Static page ported from the federation repo | none | static |
| `species/seer-spider` | Reserved placeholder | none | placeholder |

`spider_maya` output, last run: **8 areas, 51 nodes, 92 edges, 143 declared rows, 0 derived rows**, with
`nodeHash`/`edgeHash` and the exact source commit `88894bebe6cc42a7bf766a2b104d609fd3a1f514` recorded in the audit
receipt. The scanner is deliberately conservative — its own docstring says it performs *"no git-tree discovery, URL
probing, dependency inference or promotion of derived facts."*

### 2.2 Source cards

Ten cards in `docs/sources/`. **Every single one has `Source-card status: draft` and `Last checked: unknown`.**

| card | publisher | licence | relevance to the window product |
|---|---|---|---|
| `repd.md` | DESNZ | *study required* | **the spine** — and its licence is unstudied |
| `neso.md` | NESO | *study required* | connection register — a `PROCURING` evidence source |
| `ofgem.md` | Ofgem | *study required* | regulatory decisions, interconnector approvals |
| `elexon_bmrs.md` | Elexon | *study required* | feeds `data-gb-electricity` and `data-interconnectors` |
| `pvlive.md` | *study required* | *study required* | solar generation estimates |
| `desnz_dukes_ecuk.md` | DESNZ | *study required* | national statistics context |
| `github_api.md` | GitHub | *study required* | repo metadata; used by the federation map |
| `github_pages.md` | GitHub | *study required* | surface-health probing |
| `data_gb_electricity.md` | Ventusltd | *study required* | internal |
| `data_interconnectors.md` | Ventusltd | *study required* | internal |

**Not present, and needed by the plan:**

| missing card | needed by | why |
|---|---|---|
| `planit.md` | window Step 1 register adapter | `planit.org.uk` is already domain-pinned in `register-ingest.mjs` |
| `planning_data_gov_uk.md` | window Step 1 | ditto |
| `thegazette.md` | window Step 1 (distress) | ditto |
| `lowcarboncontracts.md` | window Step 1 | ditto |
| `companies_house_bulk.md` | `companies` acquisition | already fetched daily-scale bulk files under OGL v3 |
| `companies_house_rest.md` | window Step 2 Route B | the REST probe already exists in code |
| `postcodes_io.md` | gridatlas search lane | called on **every keystroke** today, with no card |
| `nominatim.md` | gridatlas search lane | called on Enter today, with no card, and it has a rate policy |
| `ons_postcode_directory.md` | the "parish" join | the only route from postcode to parish |

The last three are the sharpest finding: **the live product already calls two external geocoders on user input, and
neither has a source card.** `docs/os/EXTERNAL_SOURCE_RULES.md` says
*"Every external source needs a source-card before it becomes part of the Spider OS"* — and by extension, before it
becomes part of a shipped product.

---

## 3. The doctrine that should govern every new feed

Two documents in `docs/os/` are the reusable asset. They should be adopted verbatim by the register adapter work.

### 3.1 `SCANNER_RULES.md` — five modes and a permission ladder

```
observe   read only
derive    infer findings from observed material
distil    create compact graph or data payloads from larger observations
render    create view payloads or static pages
apply     write accepted outputs to declared paths
```

- scheduled scanners may **observe and derive** only
- manual workflows may observe, derive, distil and render
- **apply requires explicit declared output paths**
- promotion from derived to declared requires **human dispatch**

Prohibited: silently overwriting declared truth; certifying engineering truth; hiding degraded or failed
observations; promoting its own inference; rewriting a loved working page.

Required receipt fields — these should be the manifest schema of every register run:

```
run id · timestamp · source list · method state · schema version
declared row count · derived row count · unknown count · degraded count · orphan count
output paths · logical hash · receipt path
```

Note `unknown count`, `degraded count`, `orphan count`. Those three make absence visible, which is exactly the
`absence_rule` the companies contract states in different words.

### 3.2 `EXTERNAL_SOURCE_RULES.md` — the source card

Twenty required fields per source, including `licence`, `attribution requirement`, `access method`,
`API key requirement`, `rate limit`, `update frequency`, `declared fields`, `derived-only fields`, `known gaps`,
`known failure modes`, `allowed Spider use`, `not-allowed Spider use`, `screening boundary`, `last checked date`,
`status ∈ {draft, studied, approved-for-derived-scan, approved-for-declared-reference, deprecated, blocked}`.

Three rules that map exactly onto the window layer's evidence law:

| Spider rule | window-layer equivalent |
|---|---|
| "If the source explicitly states a fact, the Spider may reference it as declared once the source-card permits" | `role_must_be_explicit_in_source_record: true` |
| "If the Spider calculates, joins, probes, classifies or infers, that output is derived" | the `freeze_estimate_at` label — *derived, not published* |
| "A broken source must be shown as degraded, failed or unknown, not hidden" | `ABSTAIN` retained with a reason, never dropped |
| "If licence or usage rights are unclear, the Spider may record the uncertainty but must not ingest the source as declared truth" | **`repd.md` licence is unstudied — and REPD is the spine** |

---

## 4. Feed-by-feed: what could become an artefact

### 4.1 Live today

| feed | current output | could become | delivery type | effort |
|---|---|---|---|---|
| `spider_printer_v1` registry smoke | console totals, weekly | A **federation health tile** in the GridAtlas HUD, or a status row in the build plan | none (status only) | low |
| `spider_maya/v1` AREAS graph | `nodes.json` (51), `edges.json` (92), audit receipt | Nothing for the map. It describes GlobalGrid2050 navigation, not projects | n/a | n/a |

Neither produces project, company or register data. **Neither should be wired into the window product.**

### 4.2 Named but not built — the ones that matter

| feed | source card | status | would feed | notes |
|---|---|---|---|---|
| **PlanIt planning applications** | **missing** | not built | window Step 1 `PROCURING` evidence | `planit.org.uk` already domain-pinned in `register-ingest.mjs`; query keys `planning_authority` + `planning_application_reference` exist on both spines |
| **planning.data.gov.uk** | **missing** | not built | same | official planning data platform; complements PlanIt |
| **The Gazette** | **missing** | not built | window **distress** evidence | already the only `organisation_events` producer in the archived adapter |
| **LCCC CfD register** | **missing** | not built | `PROCURING` evidence | `lowcarboncontracts.uk` domain-pinned |
| **NESO connection register** | `neso.md`, draft | not built | `PROCURING` evidence + C6 grid exposure | `neso.energy` domain-pinned; credibility 1.0 in `credibility.mjs` |
| **Companies House bulk** | **missing** | **built, in `companies`** | funding signal Route A | fetched under OGL v3 with attribution and caveats already recorded in the plan |
| **Companies House REST** | **missing** | **probe only, in `companies`** | funding signal Route B (charges, PSC) | full client with rate-limit handling exists; retains nothing |
| **Elexon BMRS** | `elexon_bmrs.md`, draft | **built, in `data-gb-electricity`** | C12 HUD context | FUELHH to 2026-05, FUELINST to 2026-06 — **2–3 months stale** |
| **Overpass / OSM** | **missing** | **built, in `data-centres-gb`** | C10 data centres | one bounded query, 306 elements, contributor identity discarded immediately |
| **postcodes.io** | **missing** | **live in the product** | gridatlas search | called on every keystroke, 180 ms debounce |
| **Nominatim / OSM** | **missing** | **live in the product** | gridatlas global search | called on Enter/GO only — correct shape, no card |
| **ONS postcode directory** | **missing** | not built | the parish join | the only route from `repd_postcode` to a parish; see `questions.md` Q3 |

### 4.3 Freshness verdict

| feed | last evidence of a run | verdict |
|---|---|---|
| `spider_printer` smoke | weekly cron, active | **live** |
| `spider_maya` graph | 2026-07-04 | **stale ~8 weeks** |
| `data-gb-electricity` FUELHH | 2026-05 | **stale 3 months**; monthly updater documented as *unproven until a controlled dispatch is audited* |
| `data-gb-electricity` FUELINST | 2026-06 | **stale 2 months** |
| `data-gb-electricity` prices | 2026 partitions present | stale, same pipeline |
| `data-interconnectors` | **no landed data at all** | **not built** — pipelines and a reference CSV only |
| `data-centres-gb` OSM | generation 202608281053 | **fresh**, candidate branch |
| `companies` bulk | acquisition run 33123064395, files dated to 2026-08-01 | **fresh**, candidate branch |
| REPD spine | Q2 2026, published 2026-08-03 | **fresh**, frozen by design |
| `data-gridatlas` V8 transplant | 202608291015 | fresh, candidate |

---

## 5. How a feed becomes an artefact — the pipeline to standardise

Every new feed should follow the same six steps, which combine the Spider doctrine with the federation's existing
contract discipline:

```
1. SOURCE CARD        spiders/docs/sources/<source>.md
                      20 fields, status moves draft -> studied -> approved-for-derived-scan
                      licence and attribution recorded; unclear licence => do not ingest as declared

2. SCANNER DECLARATION declare the mode (observe/derive/distil/render/apply) and the output paths
                      scheduled => observe+derive only; apply requires declared paths and human dispatch

3. BOUNDED FETCHER    in the owning data repo, never in spiders and never in gridatlas
                      domain-pinned, https only, request count capped, timeout, response ceiling,
                      0 redirects, no raw HTML retained  (pattern: sector-intelligence limits block)

4. NORMALISE          into an existing typed contract: attribution roles, organisation events, or a
                      declared-key Parquet. Missing required field => ABSTAIN and retain the abstention

5. LAND + AUDIT       ZSTD Parquet, DuckDB 1.3.2, declared key, rows == distinct keys, 0 null keys,
                      landed readback. Receipt carries every SCANNER_RULES field including unknown /
                      degraded / orphan counts

6. PROJECT            only then, a compact map-ready or search artefact for a cartridge, hash-pinned in
                      a manifest the cartridge verifies before decoding
```

**Steps 1 and 2 are where `spiders` earns its place.** Steps 3–6 belong to the data repositories, which already do
them well. The failure mode to avoid is a fetcher landing in `gridatlas` or in `spiders` itself — neither owns data.

---

## 6. Recommended actions, smallest first

| # | action | effort | unblocks |
|---|---|---|---|
| S1 | Write source cards for `postcodes.io` and `nominatim` and set them `approved-for-declared-reference` with the rate and attribution constraints the product already relies on | 1 hour | closes a live compliance gap in the shipped product |
| S2 | Complete `repd.md` — licence, attribution, update frequency. It is the spine and its licence is `study required` | 1 hour | removes the largest unstudied dependency in the federation |
| S3 | Write `planit.md` and `planning_data_gov_uk.md` | 2 hours | **unblocks window Step 1**, which cannot legitimately start without them |
| S4 | Write `thegazette.md` and `lowcarboncontracts.md` | 1 hour | completes the register adapter's source set |
| S5 | Write `companies_house_bulk.md` and `companies_house_rest.md`, recording OGL v3, the accuracy caveat, and the REST rate-limit headers already handled in code | 1 hour | **unblocks window Step 2 Route B** |
| S6 | Re-run `spider_maya` at a current `globalgrid_ref`, or mark the graph explicitly stale on its page | 15 min | removes a silently 8-week-old artefact |
| S7 | Write `ons_postcode_directory.md` and decide whether the parish join is in scope at all | 1 hour | resolves `questions.md` Q3 |
| S8 | Add a `spider_printer`-style smoke probe for each **live** feed (`data-gb-electricity` freshness, `data-centres-gb` candidate, the gridatlas live pointer) so staleness is visible rather than discovered | half a day | makes §4.3 self-reporting instead of a manual survey |

S3 and S5 are on the critical path for the window layer. S1 and S2 are compliance debt on something already shipped.
