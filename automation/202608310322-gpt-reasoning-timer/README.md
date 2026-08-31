# 202608310322 real GPT hourly architecture reviewer

> **REVIEW STATUS: UNREVIEWED**  
> Classification: `inferred`

This is the model-backed counterpart to the deterministic hourly logic review.
It uses GitHub's official `actions/ai-inference` action, pinned to commit
`b81b2afb8390ee6839b494a404766bef6493c7d9`, with the GitHub Models permission
`models: read` and model `openai/gpt-4.1`.

## Five-run timer

The workflow runs immediately when installed and then four more times, hourly,
for a maximum of five committed model reviews. A persistent counter lives only
on:

`audit/202608310322-real-gpt-hourly-review`

Expected sequence on 31 August 2026, Europe/London:

1. Immediate activation run after approximately 03:25 BST.
2. 04:34 BST.
3. 05:34 BST.
4. 06:34 BST.
5. 07:34 BST.

The branch counter is authoritative. A delayed cron or rerun cannot create a
sixth review.

## What each model call must answer

- What materially happened?
- What is good, with exact evidence?
- What is bad, contradictory, stalled, weak or unknown?
- What single new workflow or Python module would best improve PipelineNews
  search intelligence?
- What deterministic tests must gate it?
- What must remain quarantined and must not be promoted?

## Safety and trust boundary

- Repository excerpts are marked as untrusted evidence and cannot alter the
  system prompt.
- The model has no GitHub MCP tools and cannot take repository actions.
- Product repositories are never written to or dispatched.
- Only timestamped evidence and model output are committed to the quarantine
  branch.
- Responses must satisfy a strict JSON schema before a review is retained.
- Any failed inference is handed to the bounded audit failure-repair workflow,
  with a maximum source-run attempt of 3.
- All outputs remain `UNREVIEWED` until human graduation.
