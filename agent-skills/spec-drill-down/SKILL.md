---
name: spec-drill-down
description: Use when requirements, plans, acceptance criteria, inputs, outputs, edge cases, or behavior-change policy are unclear and must be clarified into testable spec candidates before implementation.
---

# Spec Drill-down

## Purpose

Turn ambiguous requirements into testable spec candidates without prematurely implementing or inventing correctness.

## Script-First Execution

Before asking clarification questions, establish deterministic facts with file reads and targeted `rg`: which README, spec, and open-question files already exist for the area in question, and which sections and acceptance criteria they already contain.

When the ambiguity concerns an in-flight change, optionally collect diff evidence:

```sh
python agent-skills/diff-analysis/scripts/collect_git_diff_evidence.py --repo-root . --json
```

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

Use LLM judgement only for the clarification questions and testable spec candidates themselves.

## Prompt Contract

Stable prefix:

- Skill: `spec-drill-down`
- Execution Profile: `heavy-llm`
- Reusable Rules: do not implement while correctness is materially unclear; do not convert guesses into spec; keep questions tied to behavior, validation, scope, or risk; treat human answers as governance inputs that must be reflected in the spec.
- Scope / Governance Defaults: no Devil's Advocate review here (hand off to `devils-advocate-review` after a draft spec exists); no atomic decomposition until the revised spec is clear; no tests beyond illustrative acceptance examples.
- Output Contract: see the `### Spec Drill-down Report` template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

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

Use this report template:

```md
### Spec Drill-down Report

- Clarified requirements:
- Assumptions removed or confirmed:
- Open questions:
- Acceptance criteria candidates:
- Non-goals:
- Compatibility or replacement policy:
- Recommended next step:
```
