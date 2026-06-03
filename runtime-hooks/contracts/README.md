# Runtime Hook Contracts

This directory contains project-specific gate contracts for concrete atomic
items.

Use these files when an actual workflow item needs its own declared scope,
proposed changed files, acceptance criteria, expected artifacts, and validation
plan. Do not use this directory for stable smoke fixtures or illustrative
examples.

Current targets:

- `hook_mvp_001_a37_pre_edit_contract.json`: first project-specific `pre-edit`
  contract target for the mounted guard workflow.
- `hook_mvp_001_a39_pre_edit_contract.json`: documentation slice for the
  project-specific contract generation design boundary.
- `hook_mvp_001_a40_pre_edit_contract.json`: documentation and example slice
  for the gate-result state patch proposal boundary.
- `hook_mvp_001_a41_pre_edit_contract.json`: blocked gate-result state patch
  proposal example slice.
- `hook_mvp_001_a42_pre_edit_contract.json`: deterministic state patch
  proposal validator slice.
- `hook_mvp_001_a43_pre_edit_contract.json`: full smoke state patch proposal
  validation slice.
- `hook_mvp_001_a44_pre_edit_contract.json`: required state patch proposal
  smoke gate slice.
- `hook_mvp_001_a45_pre_edit_contract.json`: pre-edit guard and state patch
  proposal consistency smoke slice.
- `hook_mvp_001_a46_pre_edit_contract.json`: machine-readable consistency
  check output slice.
- `hook_mvp_001_a47_pre_edit_contract.json`: selected pre-edit contract source
  consistency slice for state patch proposal smoke.
- `hook_mvp_001_a48_pre_edit_contract.json`: matched proposal trace output
  slice for pre-edit guard/proposal consistency checks.
- `hook_mvp_001_a49_pre_edit_contract.json`: markdown matched proposal trace
  output slice for consistency checks.
- `hook_mvp_001_a50_pre_edit_contract.json`: markdown state patch proposal
  source metadata output slice.
- `hook_mvp_001_a51_pre_edit_contract.json`: markdown gate result contract path
  output slice.
- `hook_mvp_001_a52_pre_edit_contract.json`: markdown mounted pre-edit guard
  trace output slice.
- `hook_mvp_001_a53_pre_edit_contract.json`: markdown environment trace output
  slice.
- `hook_mvp_001_a54_pre_edit_contract.json`: markdown smoke notes output slice.
- `hook_mvp_001_a55_pre_edit_contract.json`: markdown selected smoke inputs
  output slice.

## Designing Contract Generation

Contract generation is still a design boundary, not an implemented helper.

Before drafting a project-specific contract, gather these source fields from the
active atomic item or backlog slice:

- atomic item ID;
- spec or backlog reference;
- allowed repo-relative scope;
- forbidden scope and explicit non-goals;
- acceptance criteria;
- expected artifacts;
- proposed changed files for `pre-edit`;
- validation plan and commit checkpoint expectation.

Draft the contract as a durable JSON artifact under this directory, then run the
mounted `pre-edit` guard before editing the proposed files. If the guard blocks,
fix the contract or request a scope decision; do not treat prose approval as a
gate override.

This design boundary still defers:

- automatic contract discovery or generation;
- automatic scope expansion or repair;
- durable orchestrator-state mutation;
- wrapper, daemon, Codex CLI integration, or broad runtime interception.

Validate a project-specific `pre-edit` contract with the mounted guard:

```powershell
python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a37_pre_edit_contract.json --repo-root . --json
```

Validate it through full smoke when the mounted guard must run:

```powershell
python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a37_pre_edit_contract.json --require-pre-edit-guard --json
```

Boundaries:

- These contracts are durable workflow targets, not generated handoff outputs.
- These contracts do not generate, repair, or discover scope automatically.
- Passing a contract allows the next workflow action; it does not mark the item
  complete.
- Blocked results require missing information, scope change, or human decision
  before continuing.
