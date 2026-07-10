---
name: spec-test-evolution
description: Use after human decisions or validation gap analysis to update specs, tests, workflow notes, indexes, and traceability so code, tests, and correctness contracts evolve together.
---

# Spec/Test Evolution

## Purpose

Apply accepted governance decisions to specs, tests, and workflow artifacts so behavior changes do not become implicit spec drift.

## Script-First Execution

When the spec/test evolution work is represented as a local JSON plan, validate the plan before editing specs, tests, indexes, or workflow notes:

```sh
python agent-skills/spec-test-evolution/scripts/validate_spec_test_evolution_plan.py path/to/evolution-plan.json --json
```

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

The helper checks that decision source, affected artifacts, update groups, traceability refs, rerun point, and next validation step are present. It warns when the decision source looks unresolved or root index traceability is absent. Use LLM judgement after this deterministic check to decide whether the evolution is semantically correct and whether human approval is still required.

## Prompt Contract

Stable prefix:

- Skill: `spec-test-evolution`
- Execution Profile: `hybrid`
- Reusable Rules: do not evolve spec without a human decision when correctness is ambiguous; do not leave behavior changes only in implementation or tests; follow-up items require parent backlink and root/local index visibility; set the rerun point to the earliest affected workflow step when a gap requires rework.
- Scope / Governance Defaults: do not implement unrelated changes; do not promote backlog items into accepted spec without approval; do not mark the workflow complete while traceability gaps remain.
- Output Contract: see the `### Spec/Test Evolution Report` template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

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

Use this report template:

```md
### Spec/Test Evolution Report

- Decision Applied:
- Spec Updates:
- Test Updates:
- Index Or README Updates:
- Workflow Note Updates:
- Traceability Updates:
- Rerun Point:
- Remaining Gaps:
- Next Validation Step:
```
