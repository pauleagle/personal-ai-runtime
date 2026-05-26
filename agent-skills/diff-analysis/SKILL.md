---
name: diff-analysis
description: Use to analyze git diffs, commits, or file changes for changed components, behavior-change candidates, affected modules, unrelated edits, and verification scope.
---

# Diff Analysis

## Purpose

Inspect changes after implementation or before review so verification is driven by actual diff impact, not assumptions.

## Workflow

1. Read git status and the relevant diff or commit.
2. Identify changed files, changed components, data contracts, public APIs, tests, docs, and generated artifacts.
3. Separate intended changes from unrelated edits or workspace noise.
4. Identify possible behavior-change candidates and compatibility risks.
5. Map changed areas to specs, atomic items, and tests when possible.
6. Recommend focused validation scope.
7. Hand off intent questions to `intent-analysis` and impact scope to `impact-analysis`.

## Mandatory Rules

- Do not treat all changed files as intended changes.
- Call out unrelated edits and untracked noise.
- Do not infer correctness from a clean diff alone.
- Preserve file-level and behavior-level observations separately.
- Use the current repository boundary; for nested modules, inspect the child repo when applicable.

## Boundaries

- Do not modify files.
- Do not decide whether behavior is acceptable; route ambiguity to human decision or decision proposal.
- Do not run tests unless explicitly asked.

## Validation

Check:

1. Changed files are listed.
2. Behavior-change candidates are identified.
3. Unrelated or suspicious changes are flagged.
4. Affected specs/tests are named when known.
5. Recommended validation scope is included.

## Output

Report:

- changed files
- changed components
- behavior-change candidates
- unrelated edits or workspace noise
- impacted specs
- impacted tests
- recommended validation scope
