# WS-FU-001 Evaluate WSL2 Runtime Workspace Migration

## Metadata

- Type: Workspace Follow-up
- ID: WS-FU-001
- Status: Draft
- Source Observation: WSL is installed and current, but only Docker Desktop's WSL2 data distro is registered; the runtime workspace still lives at `C:\personal-ai-runtime`.
- Suggested Location: `backlog/WS-FU-001-evaluate-wsl2-runtime-workspace-migration.md`
- Scope:
  - WSL2 Linux development environment setup
  - `personal-ai-runtime` workspace placement
  - Windows-hosted assistant and private context path bridging
  - runtime hook smoke and sandbox stability checks
- Status Impact: No current repo workflow status change; this is a non-blocking workspace/tooling follow-up after `HOOK-MVP-001`.

---

## Summary

Evaluate whether `personal-ai-runtime` should move from the Windows filesystem to a WSL2 Linux filesystem for faster dependency-heavy development, test execution, and runtime hook experiments.

The current machine has WSL2 available, but `wsl -l -v` only shows `docker-desktop-data` as a stopped WSL2 distro. That means there is not yet a normal Ubuntu/Debian-style distro for daily development. This follow-up should therefore start as an isolated migration spike, not an immediate move of the primary workspace.

---

## Clone Strategy Decision

Because the existing Windows workspace has reached a checkpoint and has been pushed, the WSL2 workspace should be created as a clean clone from the pushed repository state.

The WSL2 experiment should not copy, move, rsync, or bind-mount the current `C:\personal-ai-runtime` working tree as its main repo. The expected starting point is a fresh Linux-filesystem clone, such as:

```text
/home/<wsl-user>/personal-ai-runtime
```

The Windows workspace remains the known-good checkpoint while the WSL2 clone gathers evidence.

---

## Background

Current workspace layout:

```text
C:\personal-ai-runtime
C:\personal-ai-assistant
C:\personal-ai-context-private
```

The proposed long-term architecture is:

```text
WSL2 Linux filesystem:
  /home/<user>/personal-ai-runtime

Windows filesystem:
  C:\personal-ai-assistant
  C:\personal-ai-context-private
```

Rationale:

- `personal-ai-runtime` contains code, tests, helper scripts, nested modules, dependencies, and future runtime tooling that may benefit from Linux filesystem performance when executed inside WSL2.
- `personal-ai-assistant` and `personal-ai-context-private` are mostly low-frequency Markdown / JSON / YAML style data and should remain convenient to back up, sync, and edit from Windows.
- Cross-filesystem access should be treated carefully: Linux tools should do heavy repo I/O on Linux filesystems, while Windows-hosted assistant/context data can be read through explicit path bridging when needed.

---

## Current Observations

- `wsl --version` reports a recent WSL application version, not an old Docker-era WSL install.
- `wsl -l -v` reports only:

```text
docker-desktop-data    Stopped    2
```

- `docker-desktop-data` is a Docker Desktop data distro, not a normal interactive Linux development environment.
- The runtime repo and current Codex / PowerShell workflow are already functioning from `C:\personal-ai-runtime`.
- `HOOK-MVP-001` is complete and records WSL2 sandbox stability testing as a separate environment experiment, not part of the hook MVP correctness contract.

---

## Problem

Directly moving `personal-ai-runtime` into WSL2 could improve Linux-side execution performance, but it may also break existing Windows-oriented assumptions:

- hardcoded `C:\personal-ai-assistant` references,
- `CORE_RULES.md` path references,
- Codex CLI / PowerShell command shapes,
- runtime hook script invocation paths,
- VS Code workspace assumptions,
- nested Git repository boundaries,
- assistant/context private data routing,
- and current validation / commit checkpoint habits.

The migration should be proven with an isolated clone before changing the main workspace.

---

## Objective

Create a bounded WSL2 workspace migration experiment that answers:

- whether a normal WSL2 distro can run the repo's current tests and runtime hook smoke checks,
- whether `personal-ai-runtime` performs more reliably or faster from a Linux filesystem,
- whether the known `windows sandbox: spawn setup refresh` noise changes under WSL2,
- how to bridge `personal-ai-assistant` and `personal-ai-context-private` without hardcoding Windows-only paths,
- and whether the WSL2 clone is safe to promote as the main runtime workspace.

---

## Non-goals

This follow-up should not:

- Move the current `C:\personal-ai-runtime` workspace immediately.
- Copy or synchronize the current Windows working tree into WSL2 as the experiment's main repo.
- Delete, reset, or rewrite the Windows workspace.
- Move `personal-ai-assistant` or `personal-ai-context-private` into WSL2.
- Treat Docker Desktop's `docker-desktop-data` distro as a development distro.
- Change runtime hook correctness criteria from `HOOK-MVP-001`.
- Rewrite all scripts for portability before collecting evidence.
- Add broad path abstraction or environment-variable machinery before a focused spike proves the need.

---

## Suggested Investigation Steps

1. Install or select a normal WSL2 development distro, such as Ubuntu.
2. Clone `personal-ai-runtime` into the Linux filesystem, for example `/home/<user>/personal-ai-runtime`.
3. Configure Git identity and line-ending behavior for the WSL clone.
4. Establish explicit environment variables or config values for external data paths:
   - `PERSONAL_AI_ASSISTANT_PATH`
   - `PERSONAL_AI_CONTEXT_PATH`
5. Map those paths to Windows-hosted locations through WSL mount paths only for low-frequency assistant/context reads.
6. Run focused environment validation:
   - Python version check.
   - runtime hook environment smoke.
   - runtime hook full smoke.
   - full test suite.
7. Run repeated smoke loops to compare stability against Windows sandbox behavior.
8. Open the WSL clone through VS Code Remote WSL and verify normal editing, testing, and Git status behavior.
9. Record any path, encoding, permission, or line-ending problems.
10. Decide whether to keep WSL as an experiment, promote it as the main runtime workspace, or defer migration.

---

## Candidate Evidence To Collect

For each WSL2 test pass, record:

- distro name and version,
- `wsl --version`,
- `wsl -l -v`,
- repo path,
- Python version,
- Node / npm versions if relevant,
- Git status before and after validation,
- runtime hook smoke command and result,
- full test command and result,
- whether `windows sandbox: spawn setup refresh` appears,
- assistant/context path mapping used,
- and any VS Code Remote WSL issues.

Suggested compact log shape:

```md
### Observation

- Distro:
- Repo path:
- Assistant path:
- Context path:
- Commands:
- Results:
- Sandbox behavior:
- Path / encoding issues:
- Notes:
```

---

## Acceptance Criteria

This follow-up is complete when:

- [ ] A normal WSL2 development distro exists, or the follow-up records why it was not installed.
- [ ] A WSL2 Linux-filesystem clone of the pushed `personal-ai-runtime` repo is created for testing without disturbing the Windows workspace.
- [ ] Assistant and private context path bridging is documented for the WSL clone.
- [ ] Runtime hook environment smoke passes in WSL2, or blockers are documented.
- [ ] Runtime hook full smoke passes in WSL2, or blockers are documented.
- [ ] The full test suite passes in WSL2, or blockers are documented.
- [ ] Repeated smoke results compare WSL2 behavior against the known Windows sandbox spawn setup refresh noise.
- [ ] A recommendation exists: keep Windows primary, promote WSL2 runtime primary, maintain both, or defer.
- [ ] No private context content is copied into the runtime repo during the experiment.

---

## Review Notes

This backlog item exists because WSL2 may be a better execution substrate for dependency-heavy runtime work, but the current machine only has Docker Desktop's WSL2 data distro registered.

The safe path is a migration spike: prove the WSL2 clone, path bridging, tests, runtime hook smokes, and editor workflow before changing the main workspace.

---

## Recommended Commit Message

```text
docs(backlog): add WS-FU-001 WSL2 workspace follow-up
```
