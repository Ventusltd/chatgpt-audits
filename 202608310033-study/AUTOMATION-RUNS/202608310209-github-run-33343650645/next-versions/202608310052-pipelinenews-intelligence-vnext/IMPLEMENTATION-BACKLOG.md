# PipelineNews intelligence vNext — implementation backlog

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`  
> This is quarantined study output. It is not installed, trusted or published.

## P0 — graduate only after human review

1. Freeze the evidence-event, identity-relationship and timing-transition schemas.
2. Extract the current discovery runner into source-specific collectors with source cards and deterministic request receipts.
3. Add an append-only evidence ledger with idempotency keys, source revisions, retractions and contradictions.
4. Build a company/project/planning identity binder that defaults to `ABSTAIN` and records validity intervals.
5. Add a Companies funding-event adapter that consumes only a reviewed compact export; no raw company master is retained.
6. Add a planning/procurement event adapter with authority, application reference, status/effective date and source digest.
7. Enforce the dual-register gate: funding + procurement + reviewed identity, otherwise remain withheld.
8. Produce a reviewed project-intelligence summary for PipelineNews and GridAtlas; keep observed facts and inferred windows visually separate.
9. Replace the hard-coded GridAtlas release URL with a verified current pointer contract and two golden deep-link sentinels.
10. Add regression fixtures for one-signal silence, ambiguous identity, revised filing, retracted event, stale window and conflicting evidence.

## P1 — after P0 is proven

1. Add data-centre demand-side events using the same evidence and identity contracts.
2. Add source-card health, freshness and revision dashboards.
3. Add a human review queue for conflicts, stale windows and candidate relationships.
4. Add an operational scorecard measuring lead-time versus trade-press publication without treating later news as ground truth.
5. Add CVAA vaccines for consumer pointer drift, inference-as-fact, one-signal promotion and missing source revisions.

## Explicitly excluded

- Product-repository mutations from this audit branch.
- Live Companies House, planning, news or scraper network calls.
- Public credit/bankability scores or individual director/PSC output.
- Automatic publication from an inferred score.
