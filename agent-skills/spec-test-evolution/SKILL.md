---
name: spec-test-evolution
description: Use after human decisions or validation gap analysis to update specs, tests, workflow notes, indexes, and traceability so code, tests, and correctness contracts evolve together.
---

# Spec/Test Evolution

## Purpose

Apply accepted governance decisions to specs, tests, and workflow artifacts so behavior changes do not become implicit spec drift.

## Workflow

1. Read the human decision, decision proposal, spec refs, test effectiveness evaluation, mutation results, and impacted artifacts.
2. Determine whether to update spec, tests, README/index files, atomic metadata, backlog, follow-up items, or workflow notes.
3. Preserve traceability between parent items, follow-ups, atomic items, tests, and specs.
4. Keep accepted behavior separate from proposed, deferred, rejected, or backlog work.
5. Update tests only when they remain traceable to accepted spec or risk.
6. Update durable workflow state and rerun point when changes require earlier workflow steps.
7. Report remaining gaps and next validation step.

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
- traceability updates
- rerun point
- remaining gaps
- next validation step
