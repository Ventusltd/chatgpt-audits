# National and Trade News Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/national_and_trade_news.md`.**
> Nothing was fetched. Governs a class of sources; each publisher needs its own allowlist row.

Document type: source-card

Source name: UK national press and renewable-energy trade press (a class, allowlisted per publisher)

Publisher / owner: many

Primary URL: per publisher; **RSS/Atom feeds only**

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: per publisher, generally restrictive. Headlines and short extracts with a link are commonly tolerated;
full-text retention is not. Where unclear: record the uncertainty, do not ingest as declared truth.

Attribution requirement: publisher name and canonical link wherever used

Access method: public RSS/Atom over HTTPS. Feeds only.

API key required: no

Rate limit or access limit: declare **≤ 11 network requests per run total, concurrency 3, ≤ 6 results per source,
≤ 96 total items, ≤ 48 feed entries scanned, 5 s timeout, ≤ 1 MB response, 0 redirects** — the exact ceilings
already fixed in the sector-intelligence contract, reused rather than reinvented.

Data type: news items — title, summary, canonical URL, publication timestamp

Update frequency: continuous

Field list: `title`, `link`, `description`/`summary`, `pubDate`, `guid`, `category`

Declared fields: the feed entry as published

Derived-only fields: topic assignment, any project binding, any inferred event, and every classification

Known gaps:
- **the trade press is the competitor this product is trying to beat.** If a project appears here, the timing
  advantage is already gone. Its value is *measuring* the lead, not creating it.
- national coverage skews to the largest projects and to policy
- corporate announcements are reported after the corporate decision

Known failure modes: paywalls, syndication duplicates, feed retirement, schema drift, a name collision between
projects

Allowed Spider use: **observe and derive only.** Context, corroboration, and — most valuably — as the
`search_index_events` channel in the capture-recapture coverage estimate that measures whether the register
channel is actually leading.

Not-allowed Spider use: identical to `local_news.md`. A news item may never change a project state; credibility
never gates identity; unbound items have their identity fields stripped; no article body; no raw HTML; summaries
capped at 300 characters; no private individuals named.

Screening boundary: evidence that a publisher reported something on a date. Nothing more.

Status: draft

---

## Credibility tiers already assigned

From `discoveryv1/modules/credibility.mjs`, longest-suffix match wins:

| tier | score | domains as coded |
|---|---:|---|
| trade press | **0.7** | `solarpowerportal.co.uk`, `energy-storage.news`, `current-news.co.uk`, `renews.biz`, `constructionenquirer.com`, `theconstructionindex.co.uk`, `pv-magazine.com`, `businessgreen.com` |
| national press | **0.6** | `bbc.co.uk`, `bbc.com`, `theguardian.com`, `ft.com`, `thetimes.co.uk` |
| default / social | **0.3** | everything unlisted, plus `x.com`, `medium.com` |

One apex domain is suppressed to 0.3 by sha256 digest without being named in the source. That mechanism should be
left exactly as it is.

`constructionenquirer.com` and `theconstructionindex.co.uk` are worth noting: at 0.7 they are the two feeds most
likely to name an **EPC or principal contractor appointment**, which is `DESIGN_FROZEN`-class evidence in the
eight-state model. They are the highest-value news feeds in the list for this product — and even so, a named
contractor in the trade press is `REPORTED`, never `CONFIRMED`, until a register agrees.

## Binding discipline, already built and tested

`discoveryv1/contracts/binding.v1.json` records the regression that must keep passing:

```
headline: "Huge solar farm set to cost £1bn"   ->  ABSTAIN
snippet_primary_repd_ref: "17494"
forbidden_primary_repd_ref: "20670"
```

A headline with no identity evidence **abstains**. Matching runs against a closed REPD gazetteer with an identity
gate, a technology gate, location corroboration and an ambiguity margin; a foreign-location conflict is
`REJECTED`; a wind result is `REJECTED`.

Note that the forbidden reference `20670` is the *same collision* documented in
`PROJECT-STUDIES/_RANKING.md` §5.2 — the governance spine carries East Pye under `20670`, while this contract
forbids it. **Resolve the reference space before wiring this source**, or the regression and the spine will
contradict each other.

## Publisher allowlist — to be populated

| publisher | feed URL | licence checked | terms URL | tier | status |
|---|---|---|---|---|---|
| *(none yet — populate before first run)* | | | | | |
