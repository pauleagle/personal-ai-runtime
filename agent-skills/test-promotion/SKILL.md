---
name: test-promotion
description: Use to decide whether generated, JIT, candidate, or mutation-validated tests should remain ephemeral, become trusted tests, be persisted as regression tests, be refined, or be discarded.
---

# Test Promotion

## Purpose

Move tests through the generated-to-trusted lifecycle only when evidence shows they are useful, stable, traceable, and worth keeping.

## Workflow

1. Read test origin, spec refs, baseline results, mutation results, stability notes, and test effectiveness evaluation.
2. Classify each test as `L0 Generated`, `L1 Candidate`, `L2 Trusted`, or `L3 Persisted`.
3. Promote tests only when criteria are met.
4. Discard or refine tests that lack traceability, are flaky, duplicate existing tests, or do not kill meaningful mutations.
5. If persisting tests, identify target suite, naming, spec refs, and maintenance notes.
6. Hand required edits to implementation or spec/test evolution.

## Mandatory Rules

- Generated tests start at `L0`.
- Baseline pass and reproducibility are required for `L1`.
- Meaningful mutation kill or equivalent strong evidence is required for `L2`.
- Long-term stability and regression value are required for `L3`.
- Do not keep tests only because they increase count or coverage.

## Boundaries

- Do not persist tests without clear promotion evidence.
- Do not change spec to justify a weak test.
- Do not hide discarded tests if they reveal a real gap.

## Validation

Check:

1. Test origin is known.
2. Spec trace exists.
3. Baseline result exists.
4. Mutation/effectiveness evidence is considered.
5. Promotion or discard reason is explicit.

## Output

Report:

- test promotion table
- promoted tests
- persisted test targets
- discarded tests
- refinement needs
- traceability notes
- maintenance risk
