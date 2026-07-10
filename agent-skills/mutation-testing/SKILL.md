---
name: mutation-testing
description: Use to validate test effectiveness with mutation tooling or scoped manual mutation checks, reporting killed, survived, equivalent, skipped, or blocked mutation results honestly.
---

# Mutation Testing

## Purpose

Check whether tests can detect meaningful broken behavior, not merely whether code is covered.

## Script-First Execution

Before choosing framework mutation, manual mutation, or a blocked/skipped result, collect deterministic tooling evidence:

```sh
python agent-skills/mutation-testing/scripts/detect_mutation_test_tools.py --repo-root . --json
```

The helper detects available mutation/test binaries, `package.json` test or mutation scripts, Python project markers, test directories, and candidate commands. It does not run tests or mutation tooling. Treat its output as availability evidence only; do not report killed, survived, equivalent, or mutation score unless a separate mutation or manual mutation check was actually executed.

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

## Prompt Contract

Stable prefix:

- Skill: `mutation-testing`
- Execution Profile: `hybrid`
- Reusable Rules: never claim mutation tooling ran when it did not; mutation scope follows the impact set; survived mutations require gap classification.
- Scope / Governance Defaults: do not broaden to full-scope mutation when cost or relevance is unjustified; do not add tests solely to improve mutation score; do not decide spec evolution alone.
- Output Contract: see the Mutation Testing Report template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

## Workflow

1. Read impacted scope, selected tests, spec refs, risk items, and deterministic tooling evidence.
2. Decide whether to use framework mutation, scoped manual mutation, or a skipped/blocked result based on impact, relevance, and cost.
3. Treat manual mutation as the atomic-item probe: define one to three meaningful mutants tied to the diff risk and run the smallest focused tests that should kill them.
4. Treat framework mutation as the repeatable/reportable path for CI or regression confidence; restrict it to impacted scope when practical.
5. If the available framework can only run broad full-scope mutation and the cost is not justified, prefer scoped manual mutation or report the validation gap instead of broadening blindly.
6. Apply mutation safely, run focused tests, classify killed, survived, equivalent, skipped, or blocked.
7. Revert any manual mutation before finishing.
8. Report exact commands, scope, mutants, results, and limitations.
9. Hand survived or unclear results to `test-effectiveness-evaluation`.

## Mandatory Rules

- Do not claim mutation tooling was run if it was not.
- Manual mutation is valid only when mutants, tests, and results are explicit.
- Do not chase mutation score without impact analysis.
- Mutation scope must follow the impact set; full-scope mutation without impact analysis is an anti-pattern unless explicitly used as a checkpoint gate.
- Equivalent mutations must be marked as suspicious unless reasoning is clear.
- Survived mutations require gap classification.
- Leave the worktree free of intentional mutants.

## Boundaries

- Do not broaden to full-scope mutation when cost or relevance is unjustified.
- Do not add tests solely to improve mutation score.
- Do not decide spec evolution alone.
- Do not use framework mutation cost as a reason to skip test-effectiveness validation when a small manual mutant can target the impacted risk.

## Validation

Check:

1. Mutation scope is listed.
2. Framework or manual mode is stated.
3. Mutants are described.
4. Commands and tests are reported.
5. Results are classified.
6. Scope choice explains why focused, scoped manual, framework, full checkpoint, skipped, or blocked was appropriate.
7. Framework mutation score is included when the tool produces one.
8. Manual mutants were reverted.
9. Tooling availability is based on command evidence, not assumption.

## Output

Use this report template:

```md
### Mutation Testing Report

- Mutation Mode:
- Impacted Scope:
- Mutants:
- Commands Run:
- Framework Mutation Score, When Produced:
- Killed Mutations:
- Survived Mutations:
- Equivalent Or Suspicious Mutations:
- Skipped Or Blocked Reason:
- Limitations:
```
