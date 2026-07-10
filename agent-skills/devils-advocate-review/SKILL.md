---
name: devils-advocate-review
description: Use before finalizing a plan or spec to challenge hidden assumptions, edge cases, overdesign, architecture risk, compatibility gaps, migration cost, testing cost, and spec/implementation drift.
---

# Devil's Advocate Review

## Purpose

Challenge a draft plan or spec before implementation so unresolved risks are found early and routed into a numbered drill-down queue.

## Script-First Execution

Before semantic review, collect deterministic evidence that is available for the draft under review. Use file reads, targeted `rg`, diff/impact evidence helpers, existing test results, or context manifests to establish facts about changed files, spec sections, acceptance criteria, known tests, and referenced artifacts.

Use LLM judgement for the actual adversarial review: hidden assumptions, edge cases, compatibility risk, migration cost, overdesign, and whether an objection should block atomic decomposition.

## Prompt Contract

Stable prefix:

- Skill: `devils-advocate-review`
- Execution Profile: `heavy-llm`
- Reusable Rules: objections use IDs in the form `DA-[scope]-[number]` (e.g. `DA-P0-001`); objections are review findings, not final decisions; include at least one compatibility or replacement check for major behavior changes; distinguish risks from style preferences.
- Scope / Governance Defaults: no implementation here; no atomic decomposition while blocking objections remain unresolved; no broad speculative objections without an actionable consequence.
- Output Contract: see the `### Devil's Advocate Review Report` template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

## Workflow

1. Read the draft plan/spec, scope, non-goals, acceptance criteria, architecture constraints, and known risks.
2. Identify hidden assumptions, missing edge cases, overdesign, underspecified behavior, migration risk, testing gaps, and compatibility or replacement issues.
3. Create numbered objections with spec scope references.
4. Assign severity: `Low`, `Medium`, or `High`.
5. Sort findings from `Low` to `High` so drill-down can resolve them in order.
6. Mark which objections block atomic decomposition.
7. Hand off the numbered list to `devils-advocate-drill-down`.

## Mandatory Rules

- Use IDs in the form `DA-[scope]-[number]`, such as `DA-P0-001` or `DA-CR-001-001`.
- Do not rewrite the spec inside the review unless the user explicitly asks.
- Do not treat objections as final decisions; they are review findings for drill-down or human governance.
- Include at least one compatibility or replacement check for major behavior changes.
- Distinguish risks from style preferences.

## Boundaries

- Do not implement.
- Do not decompose atomic items while blocking objections remain unresolved.
- Do not create broad speculative objections with no actionable consequence.

## Validation

Check that each objection has:

1. ID.
2. Severity.
3. Affected spec scope.
4. Risk statement.
5. Why it matters.
6. Required clarification, spec change, or human decision.

## Output

Use this report template:

```md
### Devil's Advocate Review Report

| ID | Severity | Spec Scope | Risk | Why It Matters | Required Action | Blocks Decomposition? |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

- Hidden assumptions:
- Compatibility or replacement concerns:
- Testing or mutation concerns:
- Simplification proposals:
- Recommended drill-down order:
```
