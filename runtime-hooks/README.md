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
- When a `pre-edit` contract is selected, `pre_edit_guard.status` should be `pass`
  and `pre_edit_guard.allowed_to_edit` should be `true`.

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

The default full smoke also runs the mounted `pre-edit` guard against the sample
`pre-edit` contract, so fresh-clone checks cover the first mounted hook.

Run one or more explicit gate contracts:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --json
```

Run explicit gate contracts and state patch proposal artifacts together:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a43_pre_edit_contract.json --require-pre-edit-guard --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json
```

Smoke validates selected state patch proposal artifacts with
`validate_state_patch_proposal.py` and reports summarized results. It does not
apply proposals or mutate orchestrator state.
Markdown output includes each proposal path, atomic item ID, source gate
contract, and validation artifact for human traceability.

For workflows that must prove proposal validation ran, add
`--require-state-patch-proposal`. Smoke blocks if that option is set but no
state patch proposal artifact is selected.

When `--require-pre-edit-guard` and `--require-state-patch-proposal` are both
set, smoke also requires at least one selected `pre-edit` proposal whose
`gate_status` and source gate contract match the mounted guard status and the
selected pre-edit contract. This prevents a stale proposal for an older contract
from satisfying a new mounted guard. This is a consistency check only; smoke
still does not apply proposals or mutate orchestrator state. The
machine-readable result is reported in `consistency_checks`.
When a proposal matches, the check also reports the matched proposal path,
atomic item ID, source gate contract, and validation artifact so the
orchestrator can trace which proposal satisfied the guard. Markdown output
prints the same trace fields in the consistency checks section for human
review.

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

## Choosing Contract Types

Use sample fixtures, active examples, and project-specific contracts for
different jobs:

- Sample fixtures in `tests/fixtures/`: use these to confirm the helper works
  after a fresh clone or environment change. They are stable smoke inputs, not
  the current item's governance record.
- Active examples in `runtime-hooks/examples/`: use these to understand the
  expected shape of `pre-run`, `pre-edit`, `post-run`, and blocked gate
  contracts for a real atomic item.
- Project-specific contracts: create these when an actual workflow item needs
  its own scope, acceptance criteria, proposed files, validation plan, and
  checkpoint evidence.

Do not edit the sample fixtures merely to fit a project item. Keep samples
stable and create a new project-specific contract instead.

Project-specific contracts live in `runtime-hooks/contracts/`. These are
durable workflow targets for concrete atomic items, unlike sample fixtures and
examples. See `runtime-hooks/contracts/README.md` for naming, validation
commands, and boundaries.

Contract generation is not implemented. The current design boundary is to draft
a project-specific contract from an accepted atomic item, validate that explicit
artifact with the mounted `pre-edit` guard, and stop for missing scope or human
decisions when the guard blocks.

First project-specific target:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a37_pre_edit_contract.json --require-pre-edit-guard --json
```

## Active Atomic Item Example

A small active-item example lives at:

- `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json`
- `runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json`
- `runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json`

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

Validate the `pre-edit` example before making its proposed changes:

```powershell
python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --json
```

Validate the `post-run` example before marking the item complete:

```powershell
python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a18_post_run_contract.json --json
```

Or include it in the full smoke helper's explicit contract path:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --json
```

Run the active `pre-run`, `pre-edit`, and `post-run` examples together:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --contract runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --contract runtime-hooks\examples\hook_mvp_001_a18_post_run_contract.json --json
```

Current active example coverage:

- `pre-run`: active item contract shape and declared scope.
- `pre-edit`: proposed changed files checked against allowed and forbidden scope.
- `post-run`: changed files, validation actions, acceptance results, risks, follow-ups, and commit checkpoint shape.
- Combined smoke: all three active examples validated through repeated explicit `--contract`.

Blocked example:

- `runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json`

That fixture intentionally proposes a file outside `allowed_scope`. It should
return `status: blocked`, include concrete `blocking_reasons` entries, and set
`next_allowed_action` to `handoff`. When the same path also matches
`forbidden_scope`, both violations are reported.

## Orchestrator State Integration Boundary

The current MVP can feed an orchestrator state machine, but it does not write
state by itself.

An orchestrator may read a gate validation result and record a separate state
patch with:

- `atomic_item_id`: the item checked by the gate contract.
- `gate`: `pre-run`, `pre-edit`, or `post-run`.
- `gate_status`: `pass` or `blocked`.
- `next_allowed_action`: copied from the gate result.
- `blocking_reasons`: copied when the gate is blocked.
- `validation_artifact`: the path to the gate contract or captured gate result.
- `checkpoint_status`: commit or validation checkpoint state, when applicable.

Boundary rules:

- A passing gate result may allow the orchestrator to move a queued item into
  the next workflow step, but it does not complete that step by itself.
- A blocked gate result must keep or move the item into a blocked queue with the
  concrete blocking reasons.
- Human decisions, scope expansion, commit checkpoints, and workflow cursor
  advancement remain orchestrator responsibilities.
- This MVP does not persist gate results, mutate orchestrator JSON, discover
  active items, or intercept tool calls.

Example state artifact:

- `tests/fixtures/orchestrator_state_gate_result_sample.json`

That fixture shows a blocked `pre-edit` gate result represented in the
orchestrator state's `blocked` queue. It is an example of the boundary contract,
not a required schema for every project.

### State Patch Proposal Shape

When a workflow wants to hand a gate result to an orchestrator, write or pass a
separate state patch proposal artifact instead of mutating state directly.

A patch proposal should identify:

- the source gate contract and captured gate result;
- `atomic_item_id`, `gate`, `gate_status`, and `next_allowed_action`;
- proposed queue movement or blocked queue entry;
- proposed `workflow_step` movement, if any;
- copied `blocking_reasons` for blocked gates;
- `validation_artifact` and `checkpoint_status`;
- whether a human decision or scope decision is required;
- commit checkpoint status, or why it is not applicable.

Boundary rules:

- The runtime hook MVP may produce or validate inputs for a patch proposal, but
  it does not apply the patch.
- The orchestrator owns queue mutation, workflow cursor advancement, and merge
  policy.
- A passing `pre-edit` gate can propose moving an item toward edit work; it does
  not complete the atomic item.
- A blocked gate must propose a blocked state or handoff path with the original
  blocking reasons preserved.
- Commit checkpoints remain `post-run` or orchestrator responsibilities.

Example patch proposal artifacts:

- `runtime-hooks/examples/hook_mvp_001_a40_gate_result_state_patch_proposal.json`
- `runtime-hooks/examples/hook_mvp_001_a41_blocked_gate_result_state_patch_proposal.json`
- `runtime-hooks/examples/hook_mvp_001_a47_gate_result_state_patch_proposal.json`

The A40 example shows a passing `pre-edit` gate proposal. The A41 example shows
a blocked `pre-edit` gate proposal that keeps workflow advancement disabled,
preserves the original blocking reasons, and proposes a blocked queue entry. The
A47 example shows a passing proposal whose source gate contract and validation
artifact match the selected project-specific pre-edit contract. None of these
examples apply the patch.

Validate a patch proposal artifact:

```powershell
python runtime-hooks\scripts\validate_state_patch_proposal.py runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json
```

The validator checks proposal shape and basic pass/blocked semantics only. It
does not apply patches, mutate durable orchestrator state, expand scope, or make
human-governance decisions.

## Blocked Gate Handoff Note

When a gate returns `blocked` and the next safe action is `handoff`, write a
short handoff note before stopping or returning control to the orchestrator.

Minimal fields:

- `atomic_item_id`: the item blocked by the gate.
- `gate`: `pre-run`, `pre-edit`, or `post-run`.
- `gate_status`: usually `blocked`.
- `blocking_reasons`: copied from the gate result without rewriting meaning.
- `next_allowed_action`: copied from the gate result.
- `attempted_command`: the validator or smoke command that produced the result.
- `scope_decision_needed`: whether human or orchestrator scope adjustment is needed.
- `resume_from`: the exact artifact or command to rerun after the fix.

Boundary rules:

- A handoff note is not a gate override.
- Do not mark the item complete from the handoff note alone.
- Do not expand scope inside the note; record the decision needed instead.
- If the workflow has a durable orchestrator state artifact, the handoff note may
  be used as input to a later state patch, but this MVP does not write that patch.

## MVP Boundaries

- No runtime interception.
- No policy DSL.
- No automatic scope expansion.
- No automatic commit, revert, or approval decision.
- Gate failure can only be resolved by completing missing information, changing scope, or receiving a human decision.

## Closeout Status

The current MVP is ready to pause as a deterministic validation layer:

- Gate contracts are defined for `pre-run`, `pre-edit`, and `post-run`.
- The validator checks required fields, simple scope boundaries, blocked reasons,
  and post-run commit checkpoint shape.
- Environment and full smoke helpers support fresh-clone checks and repeated
  explicit contracts.
- Active passing examples cover all three gate types.
- A blocked active `pre-edit` example demonstrates scope violation reporting.
- Orchestrator integration remains a documented boundary, not implemented
  persistence.

Before moving beyond this MVP, make a separate decision on whether the next
phase is contract generation, orchestrator-state persistence, or real runtime
interception.

## Mounting Decision Spec

Before mounting these helpers into any runtime path, decide the mounting model
explicitly:

- Mount layer: manual command, PowerShell wrapper, Codex CLI wrapper,
  orchestrator step, or future daemon.
- First gate to mount: `pre-edit` is the safest first hard-block candidate;
  `post-run` is useful as a completion gate; `pre-run` is useful for planning
  discipline.
- Enforcement mode: advisory check, soft block with handoff, or hard block.
- Blocked output: console JSON, handoff note, orchestrator-state patch proposal,
  or persisted gate result artifact.
- Human decision boundary: blocked gates require missing information, scope
  changes, or human decision before continuing.

Recommended next mounting path:

1. Start with an orchestrator step or manual command that runs explicit
   project-specific contracts.
2. Use `pre-edit` as the first hard-block gate because it can prevent scoped
   file edits before they happen.
3. Emit blocked results as handoff notes first; defer durable state writes until
   the state patch schema is decided.
4. Keep Codex CLI wrapper, daemon, and broad tool-call interception as separate
   specs.

Do not mount this MVP as if it already intercepts every tool call. It currently
validates explicit artifacts only.

## Mounting Readiness Checklist

Before enabling any mounted workflow path, confirm:

- A project-specific gate contract exists for the active item.
- The mount layer is named and intentionally limited.
- The first mounted gate is selected, preferably `pre-edit`.
- Enforcement mode is selected: advisory, soft block, or hard block.
- Blocked output destination is selected: console JSON, handoff note,
  orchestrator-state patch proposal, or persisted artifact.
- Human decision boundary is written down for scope expansion and blocked gates.
- The exact command to rerun after a fix is recorded.
- The mount can be disabled without changing the validator helpers.

If any item is missing, keep using manual explicit contract validation.

## First Mounted Hook

The first mounted MVP hook is the hard-block `pre-edit` guard:

```powershell
python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --repo-root . --json
```

Use it as a manual or orchestrator-step guard before editing files for an
atomic item. It only accepts explicit `pre-edit` contracts. A passing result
sets `allowed_to_edit: true` and `next_allowed_action: edit`. A blocked result
sets `allowed_to_edit: false`, exits non-zero, and includes a `handoff_note`
with the blocked gate fields needed for a safe stop or orchestrator handoff.

Blocked example:

```powershell
python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --repo-root . --json
```

Write a blocked handoff note artifact:

```powershell
python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --repo-root . --handoff-note-out runtime-hooks\handoffs\blocked-pre-edit.json --json
```

This mounted hook still does not intercept tool calls, mutate orchestrator
state, expand scope, or make human-governance decisions. It is the first
concrete attachment point for the explicit artifact validator.

`--handoff-note-out` writes only when the guard blocks. Passing guard results do
not create a handoff artifact, because there is no blocked state to hand off.
Relative handoff output paths are resolved from `--repo-root`, which keeps
manual and orchestrator-step runs deterministic across different shell working
directories.

The full smoke helper includes this guard whenever the selected contract set
contains a `pre-edit` contract. If no `pre-edit` contract is selected, the guard
result is omitted instead of forcing an unrelated check.

Full smoke can also write the mounted guard's blocked handoff note:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --pre-edit-handoff-note-out runtime-hooks\handoffs\smoke-blocked-pre-edit.json --json
```

The smoke helper passes this path through to the mounted `pre-edit` guard. The
artifact is written only when that guard blocks.
If this option is provided without selecting any `pre-edit` contract, smoke
blocks instead of silently skipping the artifact.
Generated handoff artifacts under `runtime-hooks/handoffs/` are ignored by Git;
the directory exists as a conventional local output target, not as durable
source state.

For mounted workflows that require the `pre-edit` guard to run, add:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --require-pre-edit-guard --json
```

That command blocks because no `pre-edit` contract is selected. Use this option
when a manual or orchestrator-step workflow must prove the mounted guard was
actually selected instead of merely running unrelated contracts.

## Mounted Hook Closeout

The first mounted hook phase is ready to pause:

- Mounted gate: `pre-edit`.
- Mount layer: manual or orchestrator step.
- Enforcement mode: hard block.
- Passing result: `allowed_to_edit: true`.
- Blocked result: `allowed_to_edit: false`, `next_allowed_action: handoff`, and
  optional ignored handoff artifact output under `runtime-hooks/handoffs/`.
- Full smoke can require the mounted guard with `--require-pre-edit-guard`.

Still deferred:

- Automatic contract generation for project-specific items.
- Durable orchestrator-state mutation.
- A real wrapper, daemon, or broad tool-call interception layer.
- Automatic scope expansion, approval, commit, revert, or completion decisions.

Safe next options are to pause here, design project-specific contract
generation, design orchestrator-state persistence, or start a separate spec for
real runtime interception. Do not treat this mounted guard as full runtime
interception.
