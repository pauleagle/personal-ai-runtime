---
name: diff-analysis
description: Use to analyze git diffs, commits, or file changes for changed components, behavior-change candidates, affected modules, unrelated edits, and verification scope.
---

# Diff Analysis

## Purpose

Inspect changes after implementation or before review so verification is driven by actual diff impact, not assumptions.

## Script-First Execution

Collect deterministic Git evidence before semantic diff judgement.

```sh
python agent-skills/diff-analysis/scripts/collect_git_diff_evidence.py --repo-root . --json
```

For staged-only review:

```sh
python agent-skills/diff-analysis/scripts/collect_git_diff_evidence.py --repo-root . --staged --json
```

The helper records `git status --short`, `git diff --name-only`, `git diff --name-status`, and `git diff --stat`. Use this output as the file-level evidence layer; use LLM judgement only after that to classify changed components, behavior-change candidates, unrelated edits, impacted specs/tests, and validation scope.

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

## Prompt Contract

Stable prefix:

- Skill: `diff-analysis`
- Execution Profile: `hybrid`
- Reusable Rules: do not treat all changed files as intended; call out unrelated edits and untracked noise; do not infer correctness from a clean diff alone; keep file-level and behavior-level observations separate.
- Scope / Governance Defaults: read-only (no file edits); route acceptability ambiguity to human decision or decision proposal; do not run tests unless explicitly asked.
- Output Contract: see the Diff Analysis Report template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

## Workflow

1. Run deterministic Git evidence collection for the current repository boundary, or manually read git status and the relevant diff or commit when the helper is unavailable.
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
6. If the helper script changed, run its unit tests and a CLI smoke check.

## Output

Use this report template:

```md
### Diff Analysis Report

- Changed Files:
- Changed Components:
- Behavior-Change Candidates:
- Unrelated Edits Or Workspace Noise:
- Impacted Specs:
- Impacted Tests:
- Recommended Validation Scope:
```
