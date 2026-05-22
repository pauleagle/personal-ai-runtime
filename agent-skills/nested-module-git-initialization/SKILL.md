---
name: nested-module-git-initialization
description: Check and initialize Git boundaries for nested child projects under modules/ or poc-modules/. Use when editing, documenting, scaffolding, testing, or organizing a child project that is expected to be its own repository.
---

# Nested Module Git Initialization

## Purpose

Ensure child projects under `modules/` or `poc-modules/` have their own Git repository when they are being actively organized or edited.

## Workflow

1. Identify each target child project root from task paths:
   - `modules/<project>/`
   - `poc-modules/<project>/`
2. Check whether the child project root has `.git`:
   - Use `Test-Path <project-root>/.git` on PowerShell.
   - Treat either a `.git` directory or `.git` file as already initialized.
3. Do not rely only on `git -C <project-root> rev-parse --show-toplevel`; it may report the parent workspace repository.
4. If `.git` is missing and the task is actively editing or organizing that child project, run:

```powershell
git -C <project-root> init
```

5. After checking or initializing, run:

```powershell
git -C <project-root> status --short
```

6. Continue the requested work only after the Git boundary is clear.

## Rules

- Apply this only to clear `modules/<project>/` or `poc-modules/<project>/` roots.
- Do not initialize Git for `external-source/`, vendor folders, caches, build output, or temporary directories.
- Do not initialize Git when the user is only asking conceptual questions.
- Do not initialize Git if the user explicitly asked not to.
- Do not initialize Git when the project root is ambiguous; ask first.
- Do not run `git init` in the parent repo root to solve a child project boundary issue.
- Do not delete, overwrite, or recreate an existing `.git`.
- Do not run `git add`, `git commit`, `git remote add`, or `git tag` unless the user explicitly asks.
- If `git init` fails, report the error and the next suggested action.

## Output

When reporting the boundary check, use this concise format:

````md
### Git Boundary Check

- Project root:
- `.git` exists:
- Action:

### Initialization Result

- `git init` executed:
- Result:
- Notes:

### Current Status

```text
<git status --short summary>
```

### Next Decisions

- Initial commit needed:
- Remote needed:
- Branch naming needed:
````
