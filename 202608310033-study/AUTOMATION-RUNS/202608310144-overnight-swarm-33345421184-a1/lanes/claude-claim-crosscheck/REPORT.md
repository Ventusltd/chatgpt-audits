# Overnight swarm lane — claude-claim-crosscheck

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Score high-impact Claude claims as supported, partial, contradicted or still unverified against pinned source.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| gridatlas | `cd4ef33430a3` | 111 | 805,194 |
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |

## Findings

### HIGH — High-impact Claude claims now have explicit support states

Classification: `observed`

Route drift is source-supported; the 604 binding count remains handoff-only; the unknown-ref mismatch requires exact historical-spine reproduction; exact-ref performance is design-only until browser proof exists.


## Metrics

```json
{
  "claim_status_counts": {
    "SUPPORTED_BY_PINNED_SOURCE": 1,
    "HANDOFF_ONLY_PROVISIONAL": 1,
    "CONTRACT_SIDE_SUPPORTED_MEASUREMENT_UNREPRODUCED": 1,
    "NOT_OBSERVED": 1
  },
  "claims": [
    {
      "claim_id": "CLAUDE-DEEP-LINK-DRIFT",
      "claim": "PipelineNews/Companies retained an old root release route while GridAtlas moved to the stable atlas route.",
      "status": "SUPPORTED_BY_PINNED_SOURCE",
      "classification": "observed",
      "evidence": [
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "companies",
          "commit": "200e9b3a5c2f687a12109aee7a5cf7635016b0fb",
          "path": "state/atlas-v9-link-audit.json",
          "line": 9,
          "excerpt": "\"golden_url\": \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=13599\","
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "companies",
          "commit": "200e9b3a5c2f687a12109aee7a5cf7635016b0fb",
          "path": "state/atlas-v9-link-contract.json",
          "line": 3,
          "excerpt": "\"base_url\": \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/\","
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "companies",
          "commit": "200e9b3a5c2f687a12109aee7a5cf7635016b0fb",
          "path": "state/atlas-v9-link-contract.json",
          "line": 14,
          "excerpt": "\"golden_url\": \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=13599\","
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "companies",
          "commit": "200e9b3a5c2f687a12109aee7a5cf7635016b0fb",
          "path": "state/atlas-v9-link-contract.json",
          "line": 18,
          "excerpt": "\"url_template\": \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref={repd_ref}\""
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": "scope-of-works/202608301321-scope-of-works.md",
          "line": 38,
          "excerpt": "- Last known green route before migration: `/gridatlas/202608300453-atlas-v9/`"
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": "state/cross-repo-atlas-v9-milestones.json",
          "line": 79,
          "excerpt": "\"base_url\": \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/\","
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "pipelinenews",
          "commit": "83d9c430b283f8beaa8c0a05e42b14d4a4784623",
          "path": ".github/workflows/202608300522-resume-exact-atlas-pages-promotion.yml",
          "line": 109,
          "excerpt": "test \"$atlas_url\" = https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/"
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "pipelinenews",
          "commit": "83d9c430b283f8beaa8c0a05e42b14d4a4784623",
          "path": "automation/202608301200-extend-pages-atlas-link-v2.py",
          "line": 78,
          "excerpt": "== \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/\","
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "pipelinenews",
          "commit": "83d9c430b283f8beaa8c0a05e42b14d4a4784623",
          "path": "automation/202608301200-extend-pages-atlas-link-v2.py",
          "line": 116,
          "excerpt": "== \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/?repd_ref=13599\","
        },
        {
          "classification": "observed",
          "category": "old_root_route",
          "repository": "pipelinenews",
          "commit": "83d9c430b283f8beaa8c0a05e42b14d4a4784623",
          "path": "automation/202608301200-extend-pages-atlas-link-v2.py",
          "line": 233,
          "excerpt": "and receiver.get(\"base_url\") == \"https://ventusltd.github.io/gridatlas/202608300453-atlas-v9/\""
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": ".github/workflows/202608301321-verify-live.yml",
          "line": 138,
          "excerpt": "curl --fail --silent http://127.0.0.1:4173/gridatlas/atlas/current.json >/dev/null && exit 0"
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": ".github/workflows/202608301321-verify-live.yml",
          "line": 145,
          "excerpt": "GRIDATLAS_URL: http://127.0.0.1:4173/gridatlas/atlas/"
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": ".github/workflows/202608301321-verify-live.yml",
          "line": 152,
          "excerpt": "GRIDATLAS_URL: http://127.0.0.1:4173/gridatlas/atlas/"
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": ".github/workflows/202608301321-verify-live.yml",
          "line": 198,
          "excerpt": "GRIDATLAS_URL: https://ventusltd.github.io/gridatlas/atlas/"
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": ".github/workflows/202608301321-verify-live.yml",
          "line": 205,
          "excerpt": "GRIDATLAS_URL: https://ventusltd.github.io/gridatlas/atlas/"
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": "atlas/state/live-set.json",
          "line": 4,
          "excerpt": "\"live_route\": \"/gridatlas/atlas/\","
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": "atlas/state/live-set.json",
          "line": 17,
          "excerpt": "\"route\": \"/gridatlas/atlas/releases/202608300453-atlas-v9/\""
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": "scope-of-works/202608301321-01-move-atlas-into-atlas-folder.md",
          "line": 32,
          "excerpt": "- Root resolves through `/gridatlas/atlas/` to the same last-known-green application."
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": "state/live-set.json",
          "line": 16,
          "excerpt": "\"live_url\": \"https://ventusltd.github.io/gridatlas/atlas/\","
        },
        {
          "classification": "observed",
          "category": "stable_atlas_route",
          "repository": "gridatlas",
          "commit": "cd4ef33430a3e989d9cd53f87498c40112b95504",
          "path": "state/live-set.json",
          "line": 28,
          "excerpt": "\"route\": \"/gridatlas/atlas/\","
        }
      ]
    },
    {
      "claim_id": "CLAUDE-604-UPPER-BOUND",
      "claim": "482,030 edges reduce to 604 upper-bound bindings.",
      "status": "HANDOFF_ONLY_PROVISIONAL",
      "classification": "inferred",
      "evidence": [
        {
          "source": "202608310033-study/HANDOFFS/202608310116-claude-company-repd-progress.md"
        }
      ]
    },
    {
      "claim_id": "CLAUDE-UNKNOWN-REF-MISMATCH",
      "claim": "A contract asserting zero unknown REPD refs conflicts with a first measurement of 2,128.",
      "status": "CONTRACT_SIDE_SUPPORTED_MEASUREMENT_UNREPRODUCED",
      "classification": "contradicted",
      "evidence": [
        {
          "classification": "observed",
          "category": "unknown_repd_refs",
          "repository": "companies",
          "commit": "200e9b3a5c2f687a12109aee7a5cf7635016b0fb",
          "path": "build/python/202608281337-compact-parquet-companies.py",
          "line": 707,
          "excerpt": "\"unknown_repd_refs\": unknown_refs,"
        },
        {
          "classification": "observed",
          "category": "unknown_repd_refs",
          "repository": "companies",
          "commit": "200e9b3a5c2f687a12109aee7a5cf7635016b0fb",
          "path": "contracts/202608281846-federated-company-repd-relationship-contract-v1.json",
          "line": 91,
          "excerpt": "\"unknown_repd_refs\": 0,"
        },
        {
          "classification": "observed",
          "category": "unknown_repd_refs",
          "repository": "companies",
          "commit": "200e9b3a5c2f687a12109aee7a5cf7635016b0fb",
          "path": "tests/test_202608281337_compact_parquet_companies.py",
          "line": 238,
          "excerpt": "\"unknown_repd_refs\": 0,"
        },
        {
          "source": "202608310033-study/HANDOFFS/202608310116-claude-company-repd-progress.md"
        }
      ]
    },
    {
      "claim_id": "CLAUDE-EXACT-REF-PERFORMANCE",
      "claim": "An exact-ref index can avoid DuckDB boot for deep links and resolve under three seconds.",
      "status": "NOT_OBSERVED",
      "classification": "inferred",
      "evidence": []
    }
  ]
}
```

Nothing in this lane authorises installation or publication.
