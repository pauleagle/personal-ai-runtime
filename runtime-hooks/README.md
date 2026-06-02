# Runtime Hooks

This directory contains explicit runtime governance helpers for Personal AI Runtime.

The current MVP is a deterministic gate contract validator. It validates local JSON artifacts and returns whether a declared gate is `pass` or `blocked`.

It does not intercept Codex tool calls, run a daemon, wrap the agent runtime, or make human-governance decisions automatically.

## When To Use This MVP

Use these helpers when you need a deterministic check for an explicit gate contract artifact, such as:

- verifying a `pre-run`, `pre-edit`, or `post-run` JSON contract before continuing an atomic item;
- checking that a fresh clone has the minimum Python version and required runtime hook files;
- running sample contracts to confirm the MVP helpers work on a new machine;
- validating one or more explicit gate contracts for the active atomic item.

## When Not To Use This MVP

Do not treat these helpers as:

- tool-call interception;
- an agent wrapper, daemon, or runtime server;
- a policy DSL or complete authorization system;
- automatic approval for expanded scope;
- a substitute for human decisions when a gate is blocked.

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

## Gate Contract Schema Reference

All gate contracts are JSON objects.

Common required fields:

- `gate`: `pre-run`, `pre-edit`, or `post-run`.
- `atomic_item_id`: the active atomic item identifier.
- `spec_ref`: backlog, spec, issue, or durable artifact reference.
- `allowed_scope`: list of allowed repo-relative paths or scope entries.
- `forbidden_scope`: list of forbidden repo-relative paths or scope entries.
- `acceptance_criteria`: non-empty list of completion criteria.
- `expected_artifacts`: list of expected artifacts, or an explicit statement that none are expected.
- `validation_plan`: list of planned validation actions or explicit skip reason.

Additional `pre-edit` field:

- `proposed_changed_files`: list of files the edit intends to change.

Additional `post-run` fields:

- `changed_files`: list of files actually changed.
- `validation_actions`: validations that were run.
- `acceptance_results`: acceptance criteria mapped to pass, blocked, or explanatory results.
- `remaining_risks`: list of known risks, or `none known`.
- `follow_up_items`: list of follow-ups, or `none`.
- `commit_checkpoint`: object with `status` set to `committed`, `skipped`, or `blocked`. `committed` requires `commit`; `skipped` or `blocked` requires `skip_reason` or `blocked_reason`.

Scope matching is intentionally simple in this MVP: exact paths, path prefixes, and entries ending in `/**` are supported. This is not a policy DSL.

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

## Interpreting Smoke Results

For a passing full MVP smoke result:

- `status` should be `pass`.
- `next_allowed_action` should be `ready`.
- `environment.status` should be `pass`.
- Every item in `gate_results` should have `status: pass`.

For a blocked result:

- Do not continue implementation.
- Use `next_allowed_action` to decide whether to fix the environment or the gate contract.
- Fix every item listed in `blocking_reasons`.
- Rerun the same smoke command after the fix.

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

## Active Atomic Item Example

A small active-item example lives at:

- `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json`

It shows how to map one atomic item to:

- `atomic_item_id`
- `spec_ref`
- `allowed_scope`
- `forbidden_scope`
- `acceptance_criteria`
- `expected_artifacts`
- `validation_plan`

Validate it directly before starting the corresponding edit:

```powershell
python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --json
```

## MVP Boundaries

- No runtime interception.
- No policy DSL.
- No automatic scope expansion.
- No automatic commit, revert, or approval decision.
- Gate failure can only be resolved by completing missing information, changing scope, or receiving a human decision.
