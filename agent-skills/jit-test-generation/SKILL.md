---
name: jit-test-generation
description: Use to generate or select focused just-in-time tests from diff, intent, impact, spec refs, and risk items while preserving traceability and treating generated tests as candidates.
---

# JIT Test Generation

## Purpose

Generate or select focused tests for the current change, based on actual diff impact and spec-traced risk.

## Script-First Execution

Before selecting or generating tests, collect deterministic evidence with the existing helpers:

```sh
python agent-skills/diff-analysis/scripts/collect_git_diff_evidence.py --repo-root . --json
python agent-skills/impact-analysis/scripts/collect_impact_evidence.py --repo-root . --json
python agent-skills/mutation-testing/scripts/detect_mutation_test_tools.py --repo-root . --json
```

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

Use these to ground diff scope, impacted paths, and available test commands; use LLM judgement only for selecting or designing the candidate tests and their traceability metadata.

## Prompt Contract

Stable prefix:

- Skill: `jit-test-generation`
- Execution Profile: `heavy-llm`
- Reusable Rules: generated tests are not trusted by default; every JIT test needs a spec ref or risk item; do not generate broad full-suite tests as a substitute for impact analysis; do not persist generated tests unless promotion criteria are met.
- Scope / Governance Defaults: do not mutate code; do not mark tests trusted; do not update long-term regression suites without explicit promotion.
- Output Contract: see the JIT Test Generation Report template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

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

Use this report template:

```md
### JIT Test Generation Report

- Selected Existing Tests:
- Generated JIT Test Candidates:
- Traceability Metadata:
- Reproducibility Notes:
- Expected Behavior:
- Expected Mutant Or Failure Mode, When Relevant:
- Candidate Status:
- Validation Handoff:
```
