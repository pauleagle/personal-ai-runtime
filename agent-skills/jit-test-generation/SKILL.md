---
name: jit-test-generation
description: Use to generate or select focused just-in-time tests from diff, intent, impact, spec refs, and risk items while preserving traceability and treating generated tests as candidates.
---

# JIT Test Generation

## Purpose

Generate or select focused tests for the current change, based on actual diff impact and spec-traced risk.

## Workflow

1. Read diff analysis, intent analysis, impact analysis, spec refs, existing test inventory, and validation gaps.
2. Prefer selecting existing focused tests when they cover the impacted behavior.
3. Generate new JIT test candidates only for uncovered spec or risk gaps.
4. Record traceability metadata: diff source, intent, impacted component, spec ref, risk item, and reproducibility note.
5. Keep generated tests ephemeral unless later promoted.
6. Hand off candidates to test execution and mutation validation.

## Mandatory Rules

- Generated tests are not trusted tests by default.
- Every JIT test needs a spec ref or risk item.
- Do not generate broad full-suite tests as a substitute for impact analysis.
- Do not persist generated tests unless promotion criteria are met.
- Include reproducibility instructions.

## Boundaries

- Do not mutate code.
- Do not mark tests trusted.
- Do not update long-term regression suites without explicit promotion.

## Validation

Check:

1. Existing tests were considered.
2. Generated tests have traceability metadata.
3. Reproducibility instructions exist.
4. Candidate status is clear.
5. Validation handoff is explicit.

## Output

Report:

- selected existing tests
- generated JIT test candidates
- traceability metadata
- reproducibility notes
- expected behavior
- candidate status
- validation handoff
