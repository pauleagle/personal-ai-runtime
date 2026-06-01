---
name: spec-test-evolution
description: Use after human decisions or validation gap analysis to update specs, tests, workflow notes, indexes, and traceability so code, tests, and correctness contracts evolve together.
---

# Spec/Test Evolution

## Purpose

Apply accepted governance decisions to specs, tests, and workflow artifacts so behavior changes do not become implicit spec drift.

## Script-First Execution

When the spec/test evolution work is represented as a local JSON plan, validate the plan before editing specs, tests, indexes, or workflow notes:

```powershell
python agent-skills/spec-test-evolution/scripts/validate_spec_test_evolution_plan.py path/to/evolution-plan.json --json
```

Run the helper from Windows PowerShell or Linux/macOS shells with the same Python command shape. The helper checks that decision source, affected artifacts, update groups, traceability refs, rerun point, and next validation step are present. It warns when the decision source looks unresolved or root index traceability is absent. Use LLM judgement after this deterministic check to decide whether the evolution is semantically correct and whether human approval is still required.

## Workflow

1. Run the script-first evolution plan validation when a local JSON evolution plan exists; if the helper is unavailable or the work is not represented as local JSON, state the fallback.
2. Read the human decision, decision proposal, spec refs, test effectiveness evaluation, mutation results, and impacted artifacts.
3. Determine whether to update spec, tests, README/index files, atomic metadata, backlog, follow-up items, or workflow notes.
4. Preserve traceability between parent items, follow-ups, atomic items, tests, and specs.
5. Keep accepted behavior separate from proposed, deferred, rejected, or backlog work.
6. Update tests only when they remain traceable to accepted spec or risk.
7. Update durable workflow state and rerun point when changes require earlier workflow steps.
8. Report remaining gaps and next validation step.

## Mandatory Rules

- Do not evolve spec without a human decision when correctness is ambiguous.
- Do not leave behavior changes only in implementation or tests.
- Follow-up items require parent backlink and root/local index visibility when applicable.
- Tests generated from follow-ups should trace to both follow-up ID and parent ID.
- If a gap requires rework, set the rerun point to the earliest affected workflow step.

## Boundaries

- Do not implement unrelated changes.
- Do not promote backlog items into accepted spec without approval.
- Do not mark the workflow complete while traceability gaps remain.

## Validation

Check:

1. Human decision or non-ambiguous gap source is present.
2. Updated artifacts are listed.
3. Traceability is preserved.
4. Tests and spec agree.
5. Rerun point or next workflow step is explicit.

## Output

Report:

- decision applied
- spec updates
- test updates
- index or README updates
- workflow note updates
- traceability updates
- rerun point
- remaining gaps
- next validation step
