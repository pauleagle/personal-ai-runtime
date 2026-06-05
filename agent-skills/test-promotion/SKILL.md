---
name: test-promotion
description: Use to decide whether generated, JIT, candidate, or mutation-validated tests should remain ephemeral, become trusted tests, be persisted as regression tests, be refined, or be discarded.
---

# Test Promotion

## Purpose

Move tests through the generated-to-trusted lifecycle only when evidence shows they are useful, stable, traceable, and worth keeping.

## Script-First Execution

Before promotion judgement, collect deterministic evidence for the candidate tests. Prefer existing validation artifacts, test runner output, mutation/effectiveness summaries, diff/impact evidence helpers, and targeted file reads over memory or inference.

Use LLM judgement only after evidence collection to classify promotion level, weigh mutation strength, identify traceability gaps, and decide whether a test should be refined, persisted, or discarded.

## Workflow

1. Read test origin, spec refs, baseline results, mutation results, impacted scope, stability notes, and test effectiveness evaluation.
2. Classify each test as `L0 Generated`, `L1 Candidate`, `L2 Trusted`, or `L3 Persisted`.
3. Promote tests only when criteria are met.
4. Discard or refine tests that lack traceability, are flaky, duplicate existing tests, or do not kill meaningful mutations.
5. Prefer promotion evidence from focused or scoped mutation tied to the impacted risk; full-suite pass alone is insufficient for trust.
6. If persisting tests, identify target suite, naming, spec refs, and maintenance notes.
7. Hand required edits to implementation or spec/test evolution.

## Mandatory Rules

- Generated tests start at `L0`.
- Baseline pass and reproducibility are required for `L1`.
- Meaningful impacted-scope mutation kill or equivalent strong evidence is required for `L2`.
- Long-term stability and regression value are required for `L3`.
- Do not keep tests only because they increase count or coverage.
- Do not promote a generated or JIT test just because it passes the full suite; it must explain what risk it protects.

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
5. Impacted risk or mutant protected by the test is named when relevant.
6. Promotion or discard reason is explicit.

## Output

Report:

- test promotion table
- promoted tests
- persisted test targets
- discarded tests
- refinement needs
- traceability notes
- impacted risk or mutation evidence
- maintenance risk
