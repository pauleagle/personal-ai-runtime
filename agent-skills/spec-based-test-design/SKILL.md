---
name: spec-based-test-design
description: Use to design tests from accepted specs or atomic items, preserving spec-to-test traceability, edge cases, error cases, invariants, and validation hooks before or alongside implementation.
---

# Spec-Based Test Design

## Purpose

Design tests from the correctness spec so validation checks behavior, boundaries, invariants, and regression risk rather than only increasing coverage.

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

Report:

- test matrix
- spec-to-test mapping
- atomic-item-to-test mapping
- selected existing tests
- proposed new tests
- edge and error cases
- test gaps
