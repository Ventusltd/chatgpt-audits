# Local News Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/local_news.md`.**
> Nothing was fetched. This card governs a **class** of sources, and each publisher added to the allowlist needs
> its own row in the register at the end of this file.

Document type: source-card

Source name: UK local and regional news publishers (a class, allowlisted per publisher)

Publisher / owner: many, each with its own terms

Primary URL: per publisher; **RSS/Atom feed URLs only**

Source-card status: draft

Last checked: not checked — no network access permitted in this session

Licence: **per publisher, and generally restrictive.** Headlines and short extracts are commonly tolerated with a
link; full-text retention is not. **Under the licence rule, where terms are unclear the Spider records the
uncertainty and does not ingest the source as declared truth.** Local news is therefore **derived evidence only**,
never a declared fact.

Attribution requirement: publisher name and a link to the canonical article, displayed wherever used

Access method: public RSS/Atom feeds over HTTPS. **Feeds only — no page scraping, no article-body retrieval.**

API key required: no

Rate limit or access limit: per publisher; usually unstated. Declare a ceiling: **≤ 3 feeds per run per
publisher, ≤ 48 entries scanned per feed, 5 s timeout, ≤ 1 MB per response, 0 redirects**, matching the limits
already fixed in `pipelinenews/data/news-discovery/202608272130-sector-intelligence-contract.json`.

Data type: news items — title, summary, canonical URL, publication timestamp

Update frequency: continuous

Field list: `title`, `link`, `description`/`summary`, `pubDate`, `guid`, `category`

Declared fields: the feed entry as published

Derived-only fields: **everything else** — topic assignment, any binding to a `repd_ref`, any inferred project
event, sentiment, and every classification

Known gaps:
- coverage is uneven and commercially driven
- a planning decision is usually reported **after** the register records it, so this source **lags** the
  procurement signal rather than leading it
- project names in local reporting rarely match REPD names

Known failure modes: feed removed or moved behind a paywall, truncated summaries, syndicated duplicates across
titles, schema drift, an item about a different project of the same name

Allowed Spider use: **observe and derive only.** Corroboration and context. A local news item may raise the
*confidence* attached to an event that a register has already evidenced.

Not-allowed Spider use — the load-bearing constraints, all already enforced elsewhere in this federation:
- **a news item may never change a project state.** `state_change_requires_official_evidence: true`,
  `news_may_change_state: false`
- **credibility may never gate identity.** `credibility_may_gate_identity: false`
- an item with no evidenced binding is `ABSTAIN`, and the identity fields are **physically stripped** from the
  projection — `forbidden_sector_item_fields` in the sector-intelligence contract lists
  `repd_ref, gg_project_id, project, technology, capacity_mw, operator, county, related_context_repd_ref`
- no full article body, no raw HTML: `retained_raw_html_bytes: 0`, `retained_article_body_bytes: 0`
- summaries capped at **300 characters**
- no naming of private individuals

Screening boundary: a news item is evidence that a publisher reported something on a date. It is not evidence that
the thing happened, and it is never evidence of project identity.

Status: draft

---

## Credibility tier

`discoveryv1/contracts/credibility.v1.json` places this class at **0.6** (`national_or_regional_press`) or
**0.3** (`corporate_social_or_unknown`) where the publisher is unlisted — against **1.0** for an official
register. Corroboration adds **0.05 per distinct domain**, capped at **0.2**.

**A local news story can therefore never outrank a register entry**, which is the correct design and must not be
softened to make the feed look more useful.

## Publisher allowlist — to be populated

Each publisher needs a row before its feed may be read. `licence` and `terms URL` are mandatory; an unverified
publisher stays out.

| publisher | feed URL | licence checked | terms URL | credibility tier | status |
|---|---|---|---|---|---|
| *(none yet — populate before first run)* | | | | | |

## Where the real value is

Not in the headline. In the **capture-recapture coverage estimator** already written and tested at
`discoveryv1/modules/capture-recapture.mjs`:

```js
weeklyCoverageReport({ week_ending, search_index_events, register_events, overlap })
// -> lincolnPetersen(nA, nB, overlap), alert_threshold: 0.8
```

Two channels — **search index** and **register** — with their overlap, giving an estimate of total events and a
recall figure per channel. That answers the question that actually matters: *are we a month ahead, or are we just
not looking?* It is the reason to wire a news channel at all, and it needs no article body to work.
