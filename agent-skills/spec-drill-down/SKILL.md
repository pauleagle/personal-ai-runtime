---
name: spec-drill-down
description: Use when requirements, plans, acceptance criteria, inputs, outputs, edge cases, or behavior-change policy are unclear and must be clarified into testable spec candidates before implementation.
---

# Spec Drill-down

## Purpose

Turn ambiguous requirements into testable spec candidates without prematurely implementing or inventing correctness.

## Workflow

1. Read the initial request, relevant README, existing spec, open questions, and prior preflight.
2. Identify what is unclear: inputs, outputs, rules, invariants, error conditions, edge cases, compatibility, replacement policy, non-goals, or acceptance criteria.
3. Separate known facts from assumptions.
4. Ask focused questions only for decisions that materially affect correctness, scope, or validation.
5. When enough information exists, draft testable spec candidates instead of continuing to ask broad questions.
6. Mark unresolved items as open questions or human decision points.
7. Hand off clarified requirements to `spec-definition` or back to the root orchestrator.

## Mandatory Rules

- Do not implement while correctness is materially unclear.
- Do not convert guesses into spec.
- Keep questions tied to behavior, validation, scope, or risk.
- Preserve non-goals and compatibility decisions.
- Treat human answers as governance inputs that must be reflected in the spec.

## Boundaries

- Do not perform Devil's Advocate review; use `devils-advocate-review` after a draft spec exists.
- Do not decompose work into atomic items until the revised spec is clear enough.
- Do not create tests except as illustrative acceptance examples.

## Validation

Check that the output includes:

1. Clarified requirements.
2. Remaining open questions.
3. Candidate acceptance criteria.
4. Non-goals or excluded scope.
5. Items requiring human decision.

## Output

Report:

- clarified requirements
- assumptions removed or confirmed
- open questions
- acceptance criteria candidates
- non-goals
- compatibility or replacement policy
- recommended next step
