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
