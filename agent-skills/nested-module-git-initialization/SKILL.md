---
name: nested-module-git-initialization
description: Check and initialize Git boundaries for nested child projects under modules/ or poc-modules/. Use when editing, documenting, scaffolding, testing, or organizing a child project that is expected to be its own repository.
---

# Nested Module Git Initialization

## Purpose

Ensure child projects under `modules/` or `poc-modules/` have their own Git repository when they are being actively organized or edited.

## Script-First Execution

Use the bundled helper for routine boundary checks before falling back to manual commands. The canonical implementation is cross-platform Python, with PowerShell and POSIX shell wrappers.

Windows / PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File agent-skills\nested-module-git-initialization\scripts\check_nested_module_git.ps1 -ProjectRoot modules\<project>
```

Linux / POSIX shell:

```sh
sh agent-skills/nested-module-git-initialization/scripts/check_nested_module_git.sh --project-root modules/<project>
```

Direct Python fallback:

```sh
python3 agent-skills/nested-module-git-initialization/scripts/check_nested_module_git.py --project-root modules/<project>
```

If the helper reports that `.git` is missing and the task is actively editing or organizing that child project, rerun it with initialization enabled:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File agent-skills\nested-module-git-initialization\scripts\check_nested_module_git.ps1 -ProjectRoot modules\<project> -Initialize
```

```sh
sh agent-skills/nested-module-git-initialization/scripts/check_nested_module_git.sh --project-root modules/<project> --initialize
```

The helper is the deterministic evidence collector for this skill. Use LLM judgment for identifying the intended child project root, resolving ambiguity, and summarizing the result in the user-facing handoff.

## Workflow

1. Identify each target child project root from task paths:
   - `modules/<project>/`
   - `poc-modules/<project>/`
2. Run the script-first boundary check when available:
   - On Windows, use `scripts/check_nested_module_git.ps1 -ProjectRoot <project-root>`.
   - On Linux, use `scripts/check_nested_module_git.sh --project-root <project-root>`.
   - Use the Python script directly when a wrapper is unavailable.
   - Use `-Json` / `--json` when another workflow step needs structured evidence.
3. If the script is unavailable, manually check whether the child project root has `.git`:
   - Use `Test-Path <project-root>/.git` on PowerShell.
   - Use `test -e <project-root>/.git` on Linux / POSIX shell.
   - Treat either a `.git` directory or `.git` file as already initialized.
4. Do not rely only on `git -C <project-root> rev-parse --show-toplevel`; it may report the parent workspace repository.
5. If `.git` is missing and the task is actively editing or organizing that child project, run the helper with `-Initialize` or run:

```sh
git -C <project-root> init
```

6. After checking or initializing, ensure the resulting status was captured by the helper or run:

```sh
git -C <project-root> status --short
```

7. Continue the requested work only after the Git boundary is clear.

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

## Validation

Check:

1. The child project root was identified as `modules/<project>/` or `poc-modules/<project>/`.
2. The script-first boundary check was used when available, or the manual fallback reason is clear.
3. `.git` was checked directly at the child project root.
4. `git init` was run only when `.git` was missing and the task was actively editing or organizing that child project.
5. `git -C <project-root> status --short` was run after the check or initialization.
6. Windows and Linux invocation paths are documented when the helper script is changed.
7. No commit, remote, tag, or parent-repo initialization was performed unless explicitly requested.

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
