# 02 — PipelineNews intelligence-engine audit

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `observed`  
> This is quarantined study output. It is not installed, trusted or published.

Pinned source: `Ventusltd/pipelinenews@83d9c430b283f8beaa8c0a05e42b14d4a4784623`.

| Candidate file | Bytes | Lines | Responsibilities observed | Monolith candidate |
|---|---:|---:|---|---:|
| `discovery/javascript/202608270844-live-news-runner.mjs` | 54,293 | 1,312 | collection, evidence, identity, network, presentation, publication, scoring, validation | YES |
| `discovery/javascript/202608272130-sector-intelligence-runner.mjs` | 45,523 | 949 | collection, evidence, identity, network, presentation, publication, scoring, validation | YES |
| `ui/javascript/202608270844-v8-live-news-runtime.js` | 43,021 | 901 | collection, evidence, identity, network, presentation, publication, scoring, validation | YES |
| `ui/javascript/202608270055-v8-fast-runtime.js` | 40,948 | 863 | collection, evidence, identity, network, presentation, publication, scoring, validation | YES |
| `index/202608270055-compile-v8-fast.mjs` | 29,797 | 620 | collection, evidence, identity, network, presentation, publication, scoring, validation | YES |
| `atman/reports/202608271656/metrics.json` | 139,278 | 5,523 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `atman/202608262014-build-pages.py` | 82,413 | 1,541 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `.github/workflows/202608272048-mobile-orientation-candidate.yml` | 66,117 | 1,253 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `.github/workflows/202608272015-mobile-orientation-candidate.yml` | 65,962 | 1,252 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `.github/workflow-archive/20260830-email-storm/202608291447-atlas-pointer-deep-link-successor.yml` | 40,673 | 872 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `.github/workflow-archive/20260830-email-storm/202608291504-atlas-pointer-deep-link-successor.yml` | 38,948 | 846 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `.github/workflows/202608272130-sector-intelligence-candidate.yml` | 34,924 | 642 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `build/javascript/202608272130-verify-v8-fast-browser.mjs` | 33,307 | 549 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `build/javascript/202608270055-verify-v8-fast-contract.mjs` | 32,535 | 621 | collection, evidence, identity, presentation, publication, scoring, validation | YES |
| `index/202608291447-compile-atlas-pointer-deep-link.mjs` | 30,542 | 529 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `index/202608291504-compile-atlas-pointer-deep-link.mjs` | 28,415 | 506 | collection, evidence, identity, network, presentation, publication, validation | YES |
| `build/python/202608272130-build-sector-intelligence-parquet.py` | 27,641 | 580 | collection, evidence, identity, presentation, publication, scoring, validation | YES |
| `index/202608270844-compile-v8-live-news.mjs` | 26,361 | 611 | collection, evidence, identity, presentation, publication, scoring, validation | YES |
| `manifests/202608290146-adaptive-build-controller-prompt.md` | 25,886 | 279 | collection, evidence, identity, presentation, publication, scoring, validation | YES |
| `manifests/202608290202-adaptive-build-controller-prompt.md` | 25,886 | 279 | collection, evidence, identity, presentation, publication, scoring, validation | YES |

## Module-boundary observations

- **Not observed in selected snapshot:** dedicated `collector` filename/interface.
- **Not observed in selected snapshot:** dedicated `evidence_ledger` filename/interface.
- **Not observed in selected snapshot:** dedicated `identity_binder` filename/interface.
- **Not observed in selected snapshot:** dedicated `timing_state_machine` filename/interface.
- **Observed `publisher` names:** `.github/workflows/202608300522-resume-exact-atlas-pages-promotion.yml`

## Current deep-link producer

- **Observed:** `https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/` in `ui/atlas-v9-deep-links.js`.

## Architectural conclusion

- **Observed:** collection, network access, evidence handling, identity terms, validation and release/promotion terms coexist in large runner files.
- **Inferred:** adding another runner would increase coupling and make abstention, retraction and source revision harder to prove.
- **Inferred:** the vNext boundary should be `collectors → evidence ledger → identity binder → timing state machine → reviewed read model`.
- **Not checked:** this automated scan does not execute live feeds or prove current public Pages behaviour.
