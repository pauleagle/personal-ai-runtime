---
name: spec-based-test-design
description: Use to design tests from accepted specs or atomic items, preserving spec-to-test traceability, edge cases, error cases, invariants, and validation hooks before or alongside implementation.
---

# Spec-Based Test Design

## Purpose

Design tests from the correctness spec so validation checks behavior, boundaries, invariants, and regression risk rather than only increasing coverage.

## Script-First Execution

Before designing tests, collect deterministic evidence about changed paths and existing tests:

```sh
python agent-skills/impact-analysis/scripts/collect_impact_evidence.py --repo-root . --json
```

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

Use targeted file reads and `rg` to enumerate existing test files and the spec sections or acceptance criteria under design. Use LLM judgement only for scenario selection and the test matrix itself.

## Prompt Contract

Stable prefix:

- Skill: `spec-based-test-design`
- Execution Profile: `heavy-llm`
- Reusable Rules: every durable test must trace to a spec ref, risk item, or atomic item; do not write tests only for coverage metrics; include negative and boundary cases when the spec defines them; distinguish existing tests, proposed tests, and generated candidate tests.
- Scope / Governance Defaults: do not implement product code; do not run mutation testing (use `mutation-testing`); do not invent behavior not present in spec.
- Output Contract: see the `### Spec-Based Test Design Report` template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

## Workflow

1. Read the accepted spec, atomic item metadata, acceptance criteria, invariants, error conditions, existing tests, and allowed scope.
2. Identify the behavior, boundary, invariant, error, and regression scenarios that need validation.
3. Build a test matrix with spec refs for every proposed test.
4. Select existing tests when they already cover the requirement.
5. Propose new focused tests only where a real spec or risk gap exists.
6. Mark generated tests as candidate tests until baseline execution and mutation validation prove usefulness.
7. Hand off selected or proposed tests to implementation, test execution, or JIT test generation.

## Mandatory Rules

- Every durable test must trace to a spec ref, risk item, or atomic item.
- Do not write tests only for coverage metrics.
- Include negative and boundary cases when the spec defines them.
- Distinguish existing tests, proposed tests, and generated candidate tests.
- Do not promote generated tests to trusted tests here.

## Boundaries

- Do not implement product code.
- Do not run mutation testing; use `mutation-testing`.
- Do not invent behavior not present in spec.

## Validation

Check:

1. Test matrix has spec refs.
2. Atomic item refs are present when applicable.
3. Edge cases and error cases are considered.
4. Existing tests are reused where possible.
5. Test gaps are explicit.

## Output

Use this report template:

```md
### Spec-Based Test Design Report

| Test | Kind (existing / proposed / candidate) | Spec Ref | Atomic Item | Scenario |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

- Spec-To-Test Mapping:
- Atomic-Item-To-Test Mapping:
- Selected Existing Tests:
- Proposed New Tests:
- Edge And Error Cases:
- Test Gaps:
```
