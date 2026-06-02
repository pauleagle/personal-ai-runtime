# Runtime Hooks

This directory contains explicit runtime governance helpers for Personal AI Runtime.

The current MVP is a deterministic gate contract validator. It validates local JSON artifacts and returns whether a declared gate is `pass` or `blocked`.

It does not intercept Codex tool calls, run a daemon, wrap the agent runtime, or make human-governance decisions automatically.

## Gate Contract Validator

Run:

```powershell
python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_run_sample.json --json
```

Expected output fields:

- `gate`: `pre-run`, `pre-edit`, or `post-run`
- `status`: `pass` or `blocked`
- `blocking_reasons`: concrete reasons when blocked
- `checked_items`: deterministic checks and results
- `next_allowed_action`: the next action allowed by the gate result
- `notes`: non-blocking caveats

## Fixtures

Representative sample contracts live in `tests/fixtures/`:

- `gate_contract_pre_run_sample.json`
- `gate_contract_pre_edit_sample.json`
- `gate_contract_post_run_sample.json`

Use these as smoke checks and as examples when creating a new explicit gate artifact for an atomic item.

## MVP Boundaries

- No runtime interception.
- No policy DSL.
- No automatic scope expansion.
- No automatic commit, revert, or approval decision.
- Gate failure can only be resolved by completing missing information, changing scope, or receiving a human decision.
