# 01 — Repository inventory and topology

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `observed`  
> This is quarantined study output. It is not installed, trusted or published.

This checkpoint records exact commits and scans the selected source-code surface. It does not infer that an unselected path is absent.

| Repository | Commit | Files scanned | Text files | Selected bytes |
|---|---:|---:|---:|---:|
| pipelinenews | `83d9c430b283` | 226 | 226 | 3.34 MiB |
| companies | `200e9b3a5c2f` | 75 | 75 | 0.91 MiB |
| gridatlas | `cd4ef33430a3` | 153 | 136 | 1.17 MiB |
| cvaa | `d2ebc01f6eab` | 47 | 46 | 0.20 MiB |
| spiders | `5575e70a2820` | 51 | 51 | 0.20 MiB |
| data-gridatlas | `b335aca6c9c6` | 30 | 29 | 0.35 MiB |
| globalgrid2050 | `6afd5dea7216` | 626 | 565 | 259.18 MiB |
| data-centres-gb | `c5dfdee3ba5d` | 27 | 27 | 0.21 MiB |
| data-gb-electricity | `7c492745c974` | 10 | 10 | 0.06 MiB |

## Workflow evidence categories

- `workflow_dispatch`: 155 observed line(s)
- `live_network_command`: 131 observed line(s)
- `git_push`: 121 observed line(s)
- `contents_write`: 117 observed line(s)
- `scheduled`: 14 observed line(s)
- `actions_write`: 11 observed line(s)
- `pages_write`: 10 observed line(s)

## Interpretation

- **Observed:** the manifest pins each analysed repository commit and content digest.
- **Observed:** product repositories contain several workflows with write-capable permissions or push commands; each exact line is in the JSON evidence ledger.
- **Inferred:** cross-repository seam verification should be treated as a first-class test surface because the repositories reference each other frequently.
- **Not checked:** raw datasets and excluded release/data directories were not downloaded.
