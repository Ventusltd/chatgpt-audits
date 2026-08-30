# Financial Disclosures Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/financial_disclosures.md`.**
> Nothing was fetched.

Document type: source-card

Source name: UK regulatory financial disclosures — RNS via the FCA National Storage Mechanism, and listed-fund /
developer investor announcements

Publisher / owner: FCA (National Storage Mechanism); London Stock Exchange (RNS); individual issuers

Primary URL: FCA NSM `https://data.fca.org.uk/`; issuer investor-relations feeds per company

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: **verify, and do not assume.** Regulatory announcements are published for market transparency; that
purpose does not automatically grant re-use or redistribution rights, and RNS content is commercially licensed by
its distributor. Treat as **derived evidence with a link**, never as redistributable content. Retain metadata and
a canonical URL; **retain no announcement body.**

Attribution requirement: issuer name, announcement date and a link to the source record

Access method: public HTTPS search and per-issuer feeds

API key required: *verify* — NSM search is public; some distributor feeds are licensed

Rate limit or access limit: *verify.* Declare a ceiling: **≤ 50 requests per run, concurrency 2, 5 s timeout,
≤ 1 MB per response, 0 redirects, 0 retained body bytes.**

Data type: regulatory announcements — acquisitions and disposals, financing and debt facilities, project
milestones, portfolio updates, results

Update frequency: continuous on business days

Field list: issuer name, issuer LEI or company number where present, announcement headline, category, timestamp,
canonical URL

Declared fields: the announcement metadata as published

Derived-only fields: any mapping to a project, any inferred funding event, any capacity or portfolio figure read
out of narrative text

Known gaps:
- **only listed and publicly reporting entities are covered.** The live pipeline studied in
  `PROJECT-STUDIES/_RANKING.md` is dominated by private developers and funds — Island Green Power, Innova
  Renewables, NatPower UK, Statera Energy, Alcemi, Green Switch Capital — most of which will not appear here at all
- announcements name **portfolios**, rarely individual REPD projects
- a financing announcement usually **follows** the charge filing, so this source lags the Companies House signal

Known failure modes: search interface change, announcement withdrawn or replaced, issuer identified by name only,
narrative text that cannot be parsed into a fact without inference

Allowed Spider use: **observe and derive.** Corroborate a funding event already evidenced by a registered charge
or a PSC change. Where an announcement explicitly names a project *and* a transaction, that is genuine `REPORTED`
evidence at tier 0.6.

Not-allowed Spider use:
- **inferring a project-level funding event from a portfolio-level announcement.** "Fund X closes £500m
  facility" says nothing about any specific `repd_ref`.
- treating a disclosure as confirmation of financial close for a project
- computing or publishing any **credit, bankability or investability score** — forbidden outright by the
  `companies` README
- retaining announcement bodies
- naming individuals

Screening boundary: a disclosure is evidence that an issuer announced something on a date. It is corroboration for
a register fact, never a substitute for one.

Status: draft

---

## Sequencing: this is the lowest-priority of the eight sources

Ranked by *evidence delivered per unit of build effort and licence risk*, against the population actually studied:

| source | population served | licence risk | leads or lags the register |
|---|---|---|---|
| Companies House REST (charges, PSC) | all bound vehicles | low — OGL | **leads by months** |
| Companies House bulk diff (Route A) | all bound vehicles | low — OGL | leads |
| The Gazette | all bound vehicles | low | concurrent, and it is the distress signal |
| PlanIt / planning.data.gov.uk | all with a planning reference | **unverified** | **leads the press** |
| NESO connection register | large projects | low | leads |
| LCCC | CfD projects only — very few here | low | leads, but tiny population |
| Local / national / trade news | uneven | **restrictive** | **lags** |
| **Financial disclosures** | **listed issuers only — a minority** | **restrictive** | **lags the charge filing** |

Financial disclosures sit at the bottom on all four axes. Build them last, or not at all until the register
sources are delivering.

The one exception worth stating: for the handful of **listed** counterparties in the pipeline — Centrica,
E.ON UK, RWE, EDF Energy Renewables, SSE, Ørsted, Gresham House, Statkraft — an RNS announcement is often the only
public evidence of a portfolio-level decision that will later show up as a dozen individual project charges. That
is a *pattern* signal rather than a *project* signal, and it should be presented as such or not at all.
