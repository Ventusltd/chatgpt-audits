# 202608310122 audit failure auto-repair

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`

This workflow reacts when one of the overnight `chatgpt-audits` workflows completes unsuccessfully.

It retains the failed-job log, classifies common failure modes, writes a timestamped diagnosis to a new audit branch, and requests a GitHub-native re-run only while the failed source run is below attempt 3.

## Hard limits

- `Ventusltd/chatgpt-audits` is the only writable repository.
- Product workflow dispatches, re-runs and repository mutations are forbidden.
- Logs are redacted for common secret-shaped strings before retention.
- No source file is automatically rewritten from a log inference.
- Every diagnosis and repair branch remains `UNREVIEWED`.
