# Overnight swarm lane — workflow-governance

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Record workflow permissions, schedules, write paths and network commands as evidence, not assumptions.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |
| gridatlas | `cd4ef33430a3` | 111 | 805,194 |
| cvaa | `d2ebc01f6eab` | 47 | 205,030 |
| spiders | `5575e70a2820` | 51 | 213,357 |
| data-gridatlas | `b335aca6c9c6` | 32 | 485,659 |
| globalgrid2050 | `6afd5dea7216` | 2,465 | 546,141,474 |
| data-centres-gb | `c5dfdee3ba5d` | 32 | 228,929 |
| data-gb-electricity | `7c492745c974` | 472 | 98,041,589 |

## Findings

### MEDIUM — Write-capable and network-capable workflow lines are widespread

Classification: `observed`

These are evidence-line counts, not a claim that every workflow is active or unsafe. Every product workflow still needs bounded output and promotion gates.

- `companies@200e9b3a5c2f:.github/workflow-history/202608271507-bounded-companies-house-candidate.yml:14` — workflow_dispatch:
- `companies@200e9b3a5c2f:.github/workflow-history/202608271507-bounded-companies-house-candidate.yml:16` — concurrency:
- `companies@200e9b3a5c2f:.github/workflow-history/202608271507-bounded-companies-house-candidate.yml:29` — timeout-minutes: 5
- `companies@200e9b3a5c2f:.github/workflow-history/202608271507-bounded-companies-house-candidate.yml:64` — timeout-minutes: 10
- `companies@200e9b3a5c2f:.github/workflow-history/202608271507-bounded-companies-house-candidate.yml:83` — timeout-minutes: 10
- `companies@200e9b3a5c2f:.github/workflow-history/202608271507-bounded-companies-house-candidate.yml:130` — timeout-minutes: 180

### MEDIUM — Long-running automation needs explicit overlap control and recovery

Classification: `inferred`

The overnight audit uses source pinning, lane artifacts, a single aggregator and a same-repository watchdog to avoid competing pushes.

- `companies@200e9b3a5c2f:.github/workflow-history/202608271507-bounded-companies-house-candidate.yml:16` — concurrency:
- `companies@200e9b3a5c2f:.github/workflow-history/202608271547-bounded-companies-house-candidate.yml:16` — concurrency:
- `companies@200e9b3a5c2f:.github/workflow-history/202608271634-normalise-companies-candidate.yml:6` — concurrency:
- `companies@200e9b3a5c2f:.github/workflow-history/202608272016-bounded-companies-house-candidate.yml:16` — concurrency:
- `companies@200e9b3a5c2f:.github/workflow-history/202608272035-bounded-companies-house-candidate.yml:15` — concurrency:
- `companies@200e9b3a5c2f:.github/workflow-history/202608272120-bounded-companies-house-candidate.yml:15` — concurrency:

## Metrics

```json
{
  "category_counts": {
    "actions_write": 8,
    "concurrency": 134,
    "contents_write": 244,
    "git_push": 264,
    "network_command": 77,
    "pages_write": 5,
    "schedule": 16,
    "timeout": 172,
    "workflow_dispatch": 280
  },
  "repository_matrix": {
    "companies": {
      "actions_write": 1,
      "concurrency": 17,
      "contents_write": 15,
      "git_push": 15,
      "network_command": 26,
      "schedule": 2,
      "timeout": 67,
      "workflow_dispatch": 11
    },
    "cvaa": {
      "timeout": 3,
      "workflow_dispatch": 1
    },
    "data-centres-gb": {
      "concurrency": 5,
      "contents_write": 4,
      "git_push": 4,
      "network_command": 4,
      "timeout": 5,
      "workflow_dispatch": 2
    },
    "data-gb-electricity": {
      "concurrency": 1,
      "contents_write": 2,
      "git_push": 4,
      "network_command": 1,
      "schedule": 1,
      "timeout": 2,
      "workflow_dispatch": 2
    },
    "data-gridatlas": {
      "actions_write": 3,
      "concurrency": 11,
      "contents_write": 4,
      "git_push": 4,
      "network_command": 8,
      "schedule": 2,
      "timeout": 23,
      "workflow_dispatch": 9
    },
    "globalgrid2050": {
      "actions_write": 4,
      "concurrency": 100,
      "contents_write": 219,
      "git_push": 237,
      "network_command": 38,
      "pages_write": 5,
      "schedule": 11,
      "timeout": 72,
      "workflow_dispatch": 255
    }
  }
}
```

Nothing in this lane authorises installation or publication.
