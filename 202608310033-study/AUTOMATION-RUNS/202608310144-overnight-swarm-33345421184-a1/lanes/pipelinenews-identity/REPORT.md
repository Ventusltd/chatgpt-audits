# Overnight swarm lane — pipelinenews-identity

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `mixed`  
> Quarantined audit output. It is not installed, trusted or published.


Purpose: Prove project identity, abstention, related-context and eligibility semantics.

## Exact source pins

| Repository | Commit | Files | Selected bytes |
|---|---:|---:|---:|
| pipelinenews | `83d9c430b283` | 734 | 98,692,242 |

## Findings

### INFO — Primary, related and abstaining roles already exist

Classification: `observed`

The current source distinguishes PRIMARY_MATCH, related context/development and abstention/rejection. vNext should retain these semantics as a standalone binder.

- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:81` — - Preserve Beacon Fen as PRIMARY_MATCH to REPD 13599 and never 13600.
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:693` — - PRIMARY_MATCH
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:805` — - Project-table news signals come only from canonical PRIMARY_MATCH items.
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:809` — - Canonical: RELEVANT confidence percentage, PRIMARY_MATCH and REPD reference.
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:839` — - PRIMARY_MATCH and eligible_for_news_signal true on every canonical item.
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:869` — - One article may have only one PRIMARY_MATCH.

### HIGH — News eligibility is explicitly separate from relationship context

Classification: `observed`

Several paths encode eligible_for_news_signal. A related mention must never become project identity or a register fact.

- `pipelinenews@83d9c430b283:.github/workflows/202608272130-sector-intelligence-candidate.yml:255` — assert.ok(ledger.datasets.sector_items.rows.every(({ eligible_for_news_signal }) => eligible_for_news_signal === false));
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:805` — - Project-table news signals come only from canonical PRIMARY_MATCH items.
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:839` — - PRIMARY_MATCH and eligible_for_news_signal true on every canonical item.
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/README.md:903` — - Eligible for news signal: true
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/202608260159-pipelinenews/contracts/release.v9.5.1.json:36` — "related_development_drives_news_signal": false,
- `pipelinenews@83d9c430b283:archive/202608261547-pipelinenews/consumer_v1/tests/verify_consumer.py:57` — forbidden = {"repd_ref", "gg_project_id", "project_id", "project_signal_eligible", "eligible_for_news_signal"}

### MEDIUM — Query context is discussed as a non-identity signal

Classification: `observed`

The current contract contains a query-context rule. The binder should enforce evidence returned by the source rather than trust the search query that found it.

## Metrics

```json
{
  "category_counts": {
    "abstention": 165,
    "news_signal": 50,
    "primary_match": 30,
    "project_identity": 953,
    "related_context": 2
  },
  "primary_match_lines": 30
}
```

Nothing in this lane authorises installation or publication.
