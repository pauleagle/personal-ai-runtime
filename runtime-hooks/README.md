# Runtime Hooks

This directory contains explicit runtime governance helpers for Personal AI Runtime.

The current MVP is a deterministic gate contract validator. It validates local JSON artifacts and returns whether a declared gate is `pass` or `blocked`.

It does not intercept Codex tool calls, run a daemon, wrap the agent runtime, or make human-governance decisions automatically.

## Gate Contract Validator

Python baseline:

- Required: Python 3.10 or newer.
- Current local validated baseline: Python 3.10.11.
- No third-party Python packages are required for the current MVP validator.

Check the version after cloning this repo on a new machine:

```powershell
python --version
```

On Linux/macOS, use `python3 --version` if `python` does not point to Python 3.

## Fresh Clone Checklist

After cloning this repo on another machine:

1. Confirm `python --version` reports Python 3.10 or newer.
2. Run the environment smoke check.
3. Run the full MVP smoke check.
4. Run explicit gate contracts for the active atomic item when they exist.

Smoke commands return exit code `0` on `pass` and non-zero on `blocked`.

## Troubleshooting Blocked Smoke Checks

When a smoke command returns `blocked`, inspect:

- `blocking_reasons`: concrete missing version, file, or contract fields.
- `checked_items`: each deterministic check and whether it passed.
- `next_allowed_action`: the next safe action, such as `fix-environment` or `fix-contracts`.

Common first fixes:

- If `python-version` is blocked, install or select Python 3.10 or newer.
- If a `file:` check is blocked, confirm the repo clone is complete and run the command from the repo root with `--repo-root .`.
- If a gate contract is blocked, fix the JSON artifact before continuing implementation.

Run the environment smoke check:

```powershell
python runtime-hooks\scripts\check_runtime_hooks_environment.py --repo-root . --json
```

Run the full MVP smoke check:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --json
```

Run one or more explicit gate contracts:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --json
```

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
