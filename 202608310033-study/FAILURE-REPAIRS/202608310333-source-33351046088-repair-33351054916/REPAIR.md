# Audit workflow failure diagnosis

> **REVIEW STATUS: UNREVIEWED**  
> Classification: mixed `observed` / `inferred`  
> This diagnosis belongs only to `Ventusltd/chatgpt-audits`.

Source workflow: **202608310322 real GPT hourly architecture reviewer**  
Run: `33351046088` attempt `1`  
Conclusion: **failure**  
Head SHA: `d1d121e336a8032ff12f4e847a16ccef07a65776`  
Inspected: `2026-08-31T03:33:48.680561+01:00` Europe/London

## Classified failure modes

### bytecode_boundary

Classification: `inferred`

> le "$BUILD_PROMPT" "$RENDER_RESPONSE"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6162624Z ^[[36;1mfind "$CONTROLLER_ROOT" -type d -name __pycache__ -prune -exec rm -rf {} +^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6163471Z ^[[36;1m^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6164080Z ^[[36;1mTEST_ROOT="$RUNNER_TEMP/202608310322-renderer-self-test"^[[0m reason Validate model c

### network_transient

Classification: `inferred`

> erer 2026-08-31T02:33:36.6192856Z ^[[36;1mtest -s "$TEST_ROOT/rendered/MODEL-REVIEW.json"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6215027Z shell: /usr/bin/bash --noprofile --norc -e -o pipefail {0} reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6215747Z env: reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6216339Z CONTROLLER_ROOT: automation/202608310322-gpt-reasoning-timer reason V

### contract_assertion

Classification: `inferred`

> 08-31T02:33:36.6158240Z ^[[36;1mtest -f "$RENDER_RESPONSE"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6158933Z ^[[36;1mtest -f "$PROMPT_SCHEMA"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6159812Z ^[[36;1mgrep -q '^model: openai/gpt-4.1$' "$PROMPT_SCHEMA"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:33:36.6160698Z ^[[36;1mgrep -q '^responseFormat: json_schema$' "$PROMPT_SCHEMA"^[[

## Bounded action

- Re-run requested: **True**
- Endpoint class: `/repos/Ventusltd/chatgpt-audits/actions/runs/33351046088/rerun-failed-jobs`
- Reason: GitHub-native bounded retry requested because the completed audit run is below attempt 3.

## Hard boundary

- Maximum source-run attempt: 3.
- No product workflow is dispatched or re-run.
- No source file is automatically rewritten from a log inference.
- The failed log is retained in redacted form for human review.
