---
name: devils-advocate-drill-down
description: Use after Devil's Advocate Review to resolve numbered objections from Low to High before workflow atomic decomposition, producing spec patch requirements, human decisions, and pass or blocked gate status.
---

# Devil's Advocate Drill-down

## Purpose

Turn review objections into resolved spec changes, explicit deferred rationale, accepted human risk, or a blocked gate before atomic decomposition.

## Script-First Execution

Read the numbered objection list and the affected spec sections directly from their artifacts. When a durable orchestrator state artifact exists as JSON, validate it first:

```sh
python agent-skills/orchestrator-state-machine/scripts/validate_orchestrator_state.py path/to/state.json --json
```

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

Use LLM judgement only for resolution decisions and gate status.

## Prompt Contract

Stable prefix:

- Skill: `devils-advocate-drill-down`
- Execution Profile: `heavy-llm`
- Reusable Rules: every objection gets a status, processed `Low` to `High`; `open` or unresolved `confirmed` objections block `workflow-atomic-decomposition`; `deferred-with-rationale` needs a reason and non-blocking explanation; `accepted-risk-by-human` must name the human decision.
- Scope / Governance Defaults: no atomic item implementation here; do not silently drop objections; do not mark the gate `pass` if compatibility or replacement policy is missing for a major behavior change.
- Output Contract: see the `### Devil's Advocate Drill-down Report` template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

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

Use this report template:

```md
### Devil's Advocate Drill-down Report

| ID | Status | Resolution Or Rationale | Spec Patch Required | Human Decision |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

| Change | Compatibility Or Replacement Policy | Decision | Decided By |
| --- | --- | --- | --- |
|  |  |  |  |

- Spec patch requirements:
- Deferred items and rationale:
- Accepted risks and human decisions:
- Atomic decomposition gate status: pass | blocked
```
