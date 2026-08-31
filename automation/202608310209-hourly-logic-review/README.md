# 202608310209 hourly intelligence reasoning checkpoint

> **REVIEW STATUS: UNREVIEWED**  
> Classification: mixed `observed` / `inferred`

This automation fills a gap in the overnight stack.

The existing five-hour controller, swarm and watchdogs are deterministic GitHub
Actions. They do not literally wake ChatGPT. This controller therefore creates
one bounded reasoning packet per hour and an exact prompt for a ChatGPT
Scheduled Task.

## Five-run sequence

The workflow runs once when installed and then at four hourly UTC schedule
points, producing five reviews in total. A hard counter on the persistent audit
branch prevents a sixth review.

Every review answers, from current GitHub evidence:

1. What happened?
2. What is good?
3. What is bad, weak, contradictory or still unknown?
4. Which one new workflow or Python module would most improve search
   intelligence?
5. How should that candidate be tested?
6. What must remain quarantined?

The five candidate modules cover:

- entity-aware query planning;
- URL/content fingerprinting and deduplication;
- source-diversity reranking;
- identity-collision abstention;
- deterministic search replay and regression testing.

## Boundary

- The only writable repository is `Ventusltd/chatgpt-audits`.
- Product repositories are observed through bounded GitHub metadata only.
- No product workflow is dispatched or re-run.
- Candidate code is copied into timestamped quarantine output and never
  installed automatically.
- Repository content is treated as untrusted data.
- The controller does not claim that ChatGPT ran. Model reasoning requires a
  separate ChatGPT Scheduled Task using `CHATGPT-SCHEDULED-TASK.md`.

Persistent evidence branch:

`audit/202608310209-hourly-logic-review`
