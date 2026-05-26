---
name: devils-advocate-drill-down
description: Use after Devil's Advocate Review to resolve numbered objections from Low to High before workflow atomic decomposition, producing spec patch requirements, human decisions, and pass or blocked gate status.
---

# Devil's Advocate Drill-down

## Purpose

Turn review objections into resolved spec changes, explicit deferred rationale, accepted human risk, or a blocked gate before atomic decomposition.

## Workflow

1. Read the numbered Devil's Advocate objections, current spec, scope, non-goals, and human decisions already made.
2. Process objections from `Low` to `High`.
3. For each objection, decide whether it is resolved, deferred with rationale, accepted risk by human, duplicate, not applicable, or still open.
4. Record required spec patch requirements or decision table entries.
5. Block atomic decomposition when any objection remains `open` or `confirmed` without resolution.
6. For CR or major behavior change, require explicit compatibility or replacement decision.
7. Hand off pass/blocked status to the root orchestrator.

## Mandatory Rules

- Do not skip lower-severity objections without a status.
- `open` and unresolved `confirmed` objections block `workflow-atomic-decomposition`.
- `deferred-with-rationale` must include a reason and non-blocking explanation.
- `accepted-risk-by-human` must identify the human decision.
- Spec patch requirements must point to affected sections.

## Boundaries

- Do not implement atomic items.
- Do not silently drop objections.
- Do not mark the gate `pass` if compatibility or replacement policy is missing for a major behavior change.

## Validation

Check:

1. Every objection has a status.
2. Blocking objections are explicit.
3. Spec patch requirements are listed.
4. Human decisions are identified.
5. Gate status is `pass` or `blocked`.

## Output

Report:

- objection resolution table
- spec patch requirements
- compatibility or replacement decision table
- deferred items and rationale
- accepted risks and human decisions
- atomic decomposition gate status
