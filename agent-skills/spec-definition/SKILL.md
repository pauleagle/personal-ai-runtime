---
name: spec-definition
description: Use to create, revise, or normalize a formal correctness spec from clarified requirements, including scope, non-goals, rules, invariants, acceptance criteria, testing implications, and README/spec file placement.
---

# Spec Definition

## Purpose

Create or update the formal correctness contract that implementation, tests, JIT tests, mutation evaluation, and human decisions must trace back to.

## Workflow

1. Read clarified requirements, existing README, existing spec files, open questions, and current project structure.
2. Decide where the spec belongs: existing `SPEC.md`, a split file under `specs/`, or a new formal spec file.
3. Define context, goal, scope, non-goals, inputs, outputs, business rules, invariants, error conditions, acceptance criteria, testing implications, and main workflow candidates.
4. Keep README as an entry point; move correctness contracts into spec files when they become detailed.
5. Separate accepted behavior from backlog, proposed, deferred, or rejected items.
6. Preserve traceability for follow-up items, parent IDs, root spec indexes, and local spec indexes when applicable.
7. Hand off to Devil's Advocate review or revised-spec integration.

## Mandatory Rules

- Spec is the correctness source; do not leave behavior contracts only in chat.
- If README and spec conflict, treat the spec as authoritative and update the stale summary when in scope.
- Backlog is not accepted correctness unless promoted and indexed.
- Follow-up items require parent traceability and root/local index updates when applicable.
- Do not bury ambiguous behavior in prose; mark it as an open question or human decision.

## Boundaries

- Do not implement code while drafting the spec unless explicitly asked and scope is clear.
- Do not run mutation or JIT test workflows here.
- Do not mark the spec ready for atomic decomposition while blocking open questions remain.

## Validation

Check that the spec includes:

1. Scope and non-goals.
2. Inputs and outputs.
3. Rules, invariants, and error conditions.
4. Acceptance criteria.
5. Testing implications.
6. Open questions and decision status.
7. Correct README/spec/index placement.

## Output

Report:

- spec location
- sections created or updated
- accepted behavior
- open questions
- testing implications
- main workflow candidates
- index or README updates
- next gate
