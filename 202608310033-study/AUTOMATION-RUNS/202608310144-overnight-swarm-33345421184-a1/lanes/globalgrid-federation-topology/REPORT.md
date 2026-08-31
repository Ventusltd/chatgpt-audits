# Overnight swarm lane — globalgrid-federation-topology

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Measure app-to-data and repo-to-repo seams without treating the transitional monolith as a product failure.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| globalgrid2050 | `6afd5dea7216` | 2,465 | 546,141,474 |
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |
| gridatlas | `cd4ef33430a3` | 111 | 805,194 |
| companies | `200e9b3a5c2f` | 75 | 950,259 |

## Findings

### HIGH — Cross-repository seams are the highest transition risk

Classification: `inferred`

Observed 25 directed repository-reference edges in the selected source surface. These references should have executable producer/consumer contract tests.

- `audit@6afd5dea7216:Infinite GitHub Repositories_ Federated Architecture and Migration Plan for a Free Static Grid-Intelligence Platform.md:118` — "repoUrl": "https://github.com/ventusltd/app-solar-bess-topology-v8",
- `audit@6afd5dea7216:Infinite GitHub Repositories_ Federated Architecture and Migration Plan for a Free Static Grid-Intelligence Platform.md:141` — "repoUrl": "https://github.com/ventusltd/data-grid-networks",
- `audit@6afd5dea7216:Infinite GitHub Repositories_ Federated Architecture and Migration Plan for a Free Static Grid-Intelligence Platform.md:180` — Spin-up is one command: `gh repo create ventusltd/app-<slug>-v<n> --template ventusltd/template-app --public`, or the “Use this template” button. Because a template generates a fresh single-commit history (not a fork), each app is independent with no parent link. The vendored `vendor/` directory is what makes the repo “self-contained with all dependencies pre-installed.” Dependabot handles the one downside of vendor…
- `audit@6afd5dea7216:Infinite GitHub Repositories_ Federated Architecture and Migration Plan for a Free Static Grid-Intelligence Platform.md:180` — Spin-up is one command: `gh repo create ventusltd/app-<slug>-v<n> --template ventusltd/template-app --public`, or the “Use this template” button. Because a template generates a fresh single-commit history (not a fork), each app is independent with no parent link. The vendored `vendor/` directory is what makes the repo “self-contained with all dependencies pre-installed.” Dependabot handles the one downside of vendor…
- `audit@6afd5dea7216:.github/workflows/catalogue-gridatlas-v9.yml:28` — GRIDATLAS_REPOSITORY: Ventusltd/gridatlas
- `audit@6afd5dea7216:dc_cables_knowledge/index.md:7` — [Open Hardware Disclosure – Module Level DC Arc Suppression And Insulation Fault Disconnection Circuit](https://raw.githubusercontent.com/Ventusltd/pv-arc-protection-circuit/main/Open-Hardware-Disclosure.md)

## Metrics

```json
{
  "edge_count": 25,
  "top_edges": [
    {
      "source": "pipelinenews",
      "target": "data-centres-gb",
      "occurrences": 58
    },
    {
      "source": "pipelinenews",
      "target": "globalgrid2050",
      "occurrences": 56
    },
    {
      "source": "pipelinenews",
      "target": "companies",
      "occurrences": 39
    },
    {
      "source": "companies",
      "target": "pipelinenews",
      "occurrences": 35
    },
    {
      "source": "gridatlas",
      "target": "globalgrid2050",
      "occurrences": 16
    },
    {
      "source": "pipelinenews",
      "target": "gridatlas",
      "occurrences": 14
    },
    {
      "source": "gridatlas",
      "target": "pipelinenews",
      "occurrences": 12
    },
    {
      "source": "gridatlas",
      "target": "data-gridatlas",
      "occurrences": 10
    },
    {
      "source": "gridatlas",
      "target": "cvaa",
      "occurrences": 8
    },
    {
      "source": "globalgrid2050",
      "target": "gridatlas",
      "occurrences": 6
    },
    {
      "source": "companies",
      "target": "data-gb-electricity",
      "occurrences": 6
    },
    {
      "source": "pipelinenews",
      "target": "gridatlas.git",
      "occurrences": 3
    },
    {
      "source": "gridatlas",
      "target": "companies",
      "occurrences": 3
    },
    {
      "source": "pipelinenews",
      "target": "globalgrid2050.git",
      "occurrences": 2
    },
    {
      "source": "companies",
      "target": "globalgrid2050-hompage",
      "occurrences": 2
    },
    {
      "source": "globalgrid2050",
      "target": "app-solar-bess-topology-v8",
      "occurrences": 1
    },
    {
      "source": "globalgrid2050",
      "target": "data-grid-networks",
      "occurrences": 1
    },
    {
      "source": "globalgrid2050",
      "target": "app-",
      "occurrences": 1
    },
    {
      "source": "globalgrid2050",
      "target": "template-app",
      "occurrences": 1
    },
    {
      "source": "globalgrid2050",
      "target": "pv-arc-protection-circuit",
      "occurrences": 1
    }
  ],
  "category_counts": {
    "application_reference": 132,
    "parquet": 731,
    "pointer": 162,
    "repo_reference": 56,
    "workflow": 119
  }
}
```

Nothing in this lane authorises installation or publication.
