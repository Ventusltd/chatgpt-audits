# 202608310121 hourly audit watchdog

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`

This controller checks the overnight audit programme immediately when installed and then hourly at minute 43 UTC (01:43–08:43 Europe/London on 31 August 2026).

It observes recent GitHub Actions runs across the selected Ventus repositories, records failed jobs and failed steps, detects likely stalls, and confirms whether the five-hour controller and the twelve-lane overnight swarm remain active.

## Repair authority

Automatic repair is deliberately bounded:

- recent failed jobs in `Ventusltd/chatgpt-audits` may be re-run, with a hard maximum of attempt 3;
- product repositories are read-only evidence sources and are never dispatched, re-run, committed to or published by this controller;
- deterministic source defects are handed to the separate failure-diagnosis workflow rather than patched from an inferred log match;
- absence from the bounded lookback is never represented as evidence that no failure exists.

Each check is committed to `audit/hourly-watchdog-20260831` under a unique timestamped `202608310033-study/WATCHDOG/` folder. Nothing is merged automatically.
