# 03 — Funding and procurement signal separation

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `observed`  
> This is quarantined study output. It is not installed, trusted or published.

The commercial timing engine needs two independent evidence lanes. The source scan below records only code and contract language; it does not assert that a real project is funded or procuring.

## Evidence-language inventory

- `inference_term`: 377 selected source-code line(s)
- `procurement_fact`: 18 selected source-code line(s)
- `identity_key`: 15 selected source-code line(s)
- `privacy_boundary`: 4 selected source-code line(s)
- `funding_fact`: 1 selected source-code line(s)

## Candidate event model

1. **Observed register event:** a source-stamped filing, charge, planning status, condition or procurement notice.
2. **Identity relationship:** a separately evidenced binding between company, planning application and canonical project.
3. **Inferred window:** a rule-versioned interpretation that cites observed evidence IDs and is always labelled `inferred`.
4. **Corroborated sales window:** permitted only when an observed funding lane and an observed procurement lane both exist for the same reviewed project identity.

## Hard boundary

- One lane alone must remain silent.
- Absence of a filing or planning event is not negative evidence.
- News may corroborate or explain evidence; it must not manufacture the funding or procurement fact.
- Company relationship Parquet can stay compact; event history belongs in a separate, append-only contract.
- Public outputs must preserve the Companies privacy boundary and exclude individual director/PSC details.
