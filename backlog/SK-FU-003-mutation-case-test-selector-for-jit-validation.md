# SK-FU-003 Mutation Case Test Selector for JIT Validation

## Metadata

- Type: Skill Follow-up
- ID: SK-FU-003
- Status: Draft
- Source Request: Generalize the scoped mutation-test selector pattern for `SK-FU`.
- Suggested Location: `backlog/SK-FU-003-mutation-case-test-selector-for-jit-validation.md`
- Scope:
  - `agent-skills/spec-driven-change-verification/`
  - `agent-skills/mutation-testing/`
  - `agent-skills/jit-test-generation/`
  - `agent-skills/test-effectiveness-evaluation/`
  - project-local manual mutation harnesses
- Principle: Select mutants and focused tests from one traceable risk registry.
- Integration Status: Proposed
- Status Impact: No current skill README status change; this is a non-blocking workflow follow-up.

---

## Summary

Extend scoped mutation workflows so a mutation registry can select both:

1. the mutation cases relevant to an atomic item, risk key, or spec ref; and
2. the focused tests required to kill those mutants.

A motivating project-local harness can already use a name filter such as
`run_manual_mutation_checks.py --match request_plan_` to select a narrow family
of mutation cases, but each selected mutant may still run the full unit
discovery command. This is a useful first step, but the next improvement is a
registry-driven selector:

```text
atomic item / risk key / spec ref
  -> mutation cases
  -> focused test command(s)
  -> killed / survived / equivalent / skipped result
```

---

## Problem

As atomic-item scope grows, full test and full mutation runs become too slow
for the inner loop. A simple mutation-name filter reduces the number of mutants,
but still wastes time when every mutant runs the full suite.

This creates avoidable friction:

- scoped mutation can still feel expensive enough to skip;
- the relation between a mutant and the focused test expected to kill it stays implicit;
- JIT tests are harder to promote because their target mutant/risk is not recorded in the harness;
- full mutation can become the default again even when only a narrow risk changed;
- mutation output is harder to compare across atomic items because selection logic is ad hoc.

---

## Objective

Define a reusable pattern for manual or framework-backed mutation harnesses
where each mutation case can declare selection metadata and focused test
commands.

The pattern should support:

- mutation case name;
- target file and replacement;
- spec refs or atomic item ids;
- risk tags;
- expected failure or expected killed signal;
- focused test command for that mutant or risk group;
- optional broader validation command;
- result classification: killed, survived, equivalent, skipped, or blocked.

---

## Proposed Registry Shape

Example shape:

```python
MutationCase(
    name="request_plan_wrong_derived_limit",
    target="src/example_runtime/request_plan.py",
    original="derived_limit = request.base_limit + request.extension_limit",
    replacement="derived_limit = request.extension_limit",
    expected_failure="test_valid_request_derives_limits_and_paths",
    tags=("plan-validation", "derived-limit", "boundary"),
    test_command=(
        "python",
        "-m",
        "unittest",
        "tests.test_request_plan",
    ),
)
```

Expected CLI behavior:

```powershell
python tools\mutation\run_manual_mutation_checks.py --tag plan-validation
python tools\mutation\run_manual_mutation_checks.py --spec-ref SPEC-PLAN-001
python tools\mutation\run_manual_mutation_checks.py --risk boundary
```

The selector should pick matching mutation cases and run each case's focused
test command. A broader validation mode can still run the full suite or broader
mutation set.

---

## Relationship to Existing Follow-ups

- `SK-FU-001` minimizes avoidable LLM work by collecting deterministic evidence first.
- `SK-FU-002` normalizes prompt and context contracts after deterministic evidence is collected.
- `SK-FU-003` minimizes avoidable validation cost inside mutation-aware workflows by making mutation and test selection deterministic.

This follow-up complements the 2026-04 meta JIT test idea: the inner loop should
use diff / intent / risk / spec refs to select focused tests and scoped
mutation, while full test or full mutation remains a broader validation action.

---

## Non-goals

- Do not replace full unit suites or broader mutation validation.
- Do not require every existing project to adopt the same Python class shape immediately.
- Do not treat generated JIT tests as trusted only because they are selected by a tag.
- Do not hide survived mutants by narrowing the test command too aggressively.
- Do not change skill triggers or README inventory status in the first pass.

---

## Acceptance Criteria

- A mutation harness can select cases by tag, atomic item id, risk key, or spec ref.
- Each selected mutation can run a focused test command instead of always running full test discovery.
- The result output records which selector, mutation case, and test command were used.
- A survived mutation clearly identifies whether the likely gap is code, test, spec, equivalent mutant, or selector weakness.
- Broader validation mode remains available for full tests and wider mutation coverage.
- Skill guidance explains when focused mutation is enough and when full mutation should still run.

---

## Candidate Implementation Slices

1. Add registry fields for `tags`, `spec_refs`, and `test_command` to one project-local manual mutation harness.
2. Add CLI selectors such as `--tag`, `--spec-ref`, and `--risk`, while preserving existing name matching.
3. Update mutation output to include selected test command and selector evidence.
4. Add harness tests for selector behavior and focused command fallback.
5. Update `mutation-testing` and `spec-driven-change-verification` guidance with the registry-driven JIT mutation pattern.
6. Promote the pattern only after one or two project-local harnesses prove it reduces validation cost without hiding survived mutants.

---

## Validation Notes

For any implementation slice, validation should include:

- focused harness unit tests;
- one real scoped mutation run;
- one no-match or selector-error case;
- `git diff --check`;
- explicit note whether full mutation was skipped, scoped, or run as broader validation.
