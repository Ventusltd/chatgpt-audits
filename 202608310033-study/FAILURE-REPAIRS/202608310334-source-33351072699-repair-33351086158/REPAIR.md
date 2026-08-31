# Audit workflow failure diagnosis

> **REVIEW STATUS: UNREVIEWED**  
> Classification: mixed `observed` / `inferred`  
> This diagnosis belongs only to `Ventusltd/chatgpt-audits`.

Source workflow: **202608310322 real GPT hourly architecture reviewer**  
Run: `33351072699` attempt `1`  
Conclusion: **failure**  
Head SHA: `5a709efc3bbd5fe90a061ccee7d597f109917791`  
Inspected: `2026-08-31T03:34:25.821499+01:00` Europe/London

## Classified failure modes

### bytecode_boundary

Classification: `inferred`

> le "$BUILD_PROMPT" "$RENDER_RESPONSE"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0532849Z ^[[36;1mfind "$CONTROLLER_ROOT" -type d -name __pycache__ -prune -exec rm -rf {} +^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0534653Z ^[[36;1m^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0535869Z ^[[36;1mTEST_ROOT="$RUNNER_TEMP/202608310322-renderer-self-test"^[[0m reason Validate model c

### network_transient

Classification: `inferred`

> 2026-08-31T02:34:13.0526692Z ^[[36;1mgrep -q '^model: openai/gpt-4.1$' "$PROMPT_SCHEMA"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0528504Z ^[[36;1mgrep -q '^responseFormat: json_schema$' "$PROMPT_SCHEMA"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0530416Z ^[[36;1mpython3 -m py_compile "$BUILD_PROMPT" "$RENDER_RESPONSE"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.05328

### contract_assertion

Classification: `inferred`

> 08-31T02:34:13.0523980Z ^[[36;1mtest -f "$RENDER_RESPONSE"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0525249Z ^[[36;1mtest -f "$PROMPT_SCHEMA"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0526692Z ^[[36;1mgrep -q '^model: openai/gpt-4.1$' "$PROMPT_SCHEMA"^[[0m reason Validate model controller and strict response renderer 2026-08-31T02:34:13.0528504Z ^[[36;1mgrep -q '^responseFormat: json_schema$' "$PROMPT_SCHEMA"^[[

## Bounded action

- Re-run requested: **True**
- Endpoint class: `/repos/Ventusltd/chatgpt-audits/actions/runs/33351072699/rerun-failed-jobs`
- Reason: GitHub-native bounded retry requested because the completed audit run is below attempt 3.

## Hard boundary

- Maximum source-run attempt: 3.
- No product workflow is dispatched or re-run.
- No source file is automatically rewritten from a log inference.
- The failed log is retained in redacted form for human review.
