---
name: test-effectiveness-evaluation
description: Use to interpret test, JIT test, or mutation results and classify weak tests, effective tests, validation gaps, spec gaps, implementation issues, and recommended improvements.
---

# Test Effectiveness Evaluation

## Purpose

Interpret validation results to decide whether tests are effective, weak, incomplete, unstable, or blocked by spec ambiguity.

## Script-First Execution

Before classifying effectiveness, extract deterministic evidence from available test or mutation result artifacts:

```powershell
python agent-skills\test-effectiveness-evaluation\scripts\collect_validation_result_evidence.py --json <result-file> [<result-file> ...]
```

The helper reads text result files, detects unittest run counts and pass/fail status, and extracts mutation term counts such as `killed`, `survived`, `equivalent`, `skipped`, and `blocked`. It does not decide whether a survived mutation is a test gap, spec gap, implementation issue, or equivalent mutation; use LLM judgement for that classification after evidence is collected.

Run the helper from Windows PowerShell or Linux/macOS shells with the same Python command shape.

## Workflow

1. Read deterministic validation-result evidence, baseline test results, JIT test results, mutation results, spec refs, risk items, and impact analysis.
2. Identify which tests passed baseline and which killed meaningful mutations.
3. Classify survived mutations as test gap, spec gap, implementation issue, equivalent mutation, accepted risk, or unclear.
4. Identify flaky, brittle, redundant, or coverage-only tests.
5. Recommend refine tests, update spec, fix implementation, discard candidate tests, or request human decision.
6. Provide promotion recommendation for generated tests when appropriate.
7. Hand decisions to `decision-proposal`, `test-promotion`, or `spec-test-evolution`.

## Mandatory Rules

- Passing tests alone do not prove effectiveness.
- Survived mutation is a gap until classified.
- Do not promote generated tests without evidence.
- Distinguish test weakness from spec ambiguity.
- Report tooling limitations clearly.

## Boundaries

- Do not edit tests or code in this skill unless explicitly asked.
- Do not decide human governance questions.
- Do not hide flaky or inconclusive results.

## Validation

Check:

1. Baseline result is considered.
2. Mutation or manual mutation result is considered.
3. Gap classification is explicit.
4. Recommended next action is clear.
5. Human decision needs are identified.
6. If the helper script changed, run its unit tests and a CLI smoke check.

## Output

Report:

- effective tests
- weak tests
- candidate tests
- survived mutation classification
- validation gaps
- recommended improvements
- promotion recommendation
- human decision needed
