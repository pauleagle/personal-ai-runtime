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
4. When mutation cost is growing, use the impact set to choose tests that should kill specific meaningful mutants instead of defaulting to full-suite execution.
5. Record traceability metadata: diff source, intent, impacted component, spec ref, risk item, expected mutant or failure mode, and reproducibility note.
6. Keep generated tests ephemeral unless later promoted.
7. Hand off candidates to focused execution and scoped mutation validation.

## Mandatory Rules

- Generated tests are not trusted tests by default.
- Every JIT test needs a spec ref or risk item.
- Do not generate broad full-suite tests as a substitute for impact analysis.
- Do not use JIT tests to inflate test count; use them to close a named spec, impact, or mutation-effectiveness gap.
- A JIT test intended for mutation validation must name the impacted risk or mutant it is expected to kill.
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
5. Expected focused test command or scoped mutation handoff is explicit.
6. Full-suite fallback is justified only when impact cannot be narrowed or checkpoint confidence is required.

## Output

Report:

- selected existing tests
- generated JIT test candidates
- traceability metadata
- reproducibility notes
- expected behavior
- expected mutant or failure mode, when relevant
- candidate status
- validation handoff
