---
name: mutation-testing
description: Use to validate test effectiveness with mutation tooling or scoped manual mutation checks, reporting killed, survived, equivalent, skipped, or blocked mutation results honestly.
---

# Mutation Testing

## Purpose

Check whether tests can detect meaningful broken behavior, not merely whether code is covered.

## Workflow

1. Read impacted scope, selected tests, spec refs, risk items, and available mutation tooling.
2. Decide whether to use framework mutation or scoped manual mutation.
3. If using a framework, restrict mutation to impacted scope when practical.
4. If using manual mutation, define one to three meaningful mutants tied to the diff risk.
5. Apply mutation safely, run focused tests, classify killed, survived, equivalent, skipped, or blocked.
6. Revert any manual mutation before finishing.
7. Report exact commands, scope, mutants, results, and limitations.
8. Hand survived or unclear results to `test-effectiveness-evaluation`.

## Mandatory Rules

- Do not claim mutation tooling was run if it was not.
- Manual mutation is valid only when mutants, tests, and results are explicit.
- Do not chase mutation score without impact analysis.
- Equivalent mutations must be marked as suspicious unless reasoning is clear.
- Survived mutations require gap classification.
- Leave the worktree free of intentional mutants.

## Boundaries

- Do not broaden to full-scope mutation when cost or relevance is unjustified.
- Do not add tests solely to improve mutation score.
- Do not decide spec evolution alone.

## Validation

Check:

1. Mutation scope is listed.
2. Framework or manual mode is stated.
3. Mutants are described.
4. Commands and tests are reported.
5. Results are classified.
6. Manual mutants were reverted.

## Output

Report:

- mutation mode
- impacted scope
- mutants
- commands run
- killed mutations
- survived mutations
- equivalent or suspicious mutations
- skipped or blocked reason
- limitations
