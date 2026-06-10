# WS-FU-002 Investigate Cross-Environment Git Line Ending Policy

## Metadata

- Type: Workspace Follow-up
- ID: WS-FU-002
- Status: Draft
- Source Observation: A Windows-hosted Markdown file edited from WSL briefly showed mixed CRLF/LF line endings, and Git reported that CRLF would be replaced by LF when the file is touched.
- Suggested Location: `backlog/WS-FU-002-investigate-cross-environment-line-ending-policy.md`
- Scope:
  - Windows Git and WSL Git global line-ending configuration
  - repo-local `.gitattributes` and `.editorconfig` policy
  - cross-mounted `/mnt/c` edits from WSL
  - Markdown / script line-ending expectations across `personal-ai-runtime` and `personal-ai-assistant`
  - detection and normalization commands for mixed CRLF/LF files
- Status Impact: No current implementation status change; this is a non-blocking workspace/tooling follow-up after the WSL2 workflow became active.

---

## Routing Decision

Track this as `WS-FU`, not `RT-FU`.

`RT-FU-001` should stay focused on Codex Windows sandbox process-spawn/setup failures. This item is about workspace policy across Windows, WSL2, Git, editors, and mounted paths. It belongs beside the WSL2 workspace migration follow-ups because the problem appears at the cross-environment boundary rather than inside the Codex runtime spawn layer.

---

## Summary

Investigate and define a stable line-ending policy for the mixed Windows / WSL2 workspace.

The current setup uses WSL2 for runtime validation while some durable assistant data and possibly controller workflows remain on the Windows filesystem. When Linux tools edit files under `/mnt/c`, and Windows tools or editors also touch the same files, line endings can drift or become mixed unless repo-local policy is explicit.

The follow-up should decide whether each repo should prefer LF everywhere, CRLF for selected Windows-facing files, or a documented mixed policy enforced by `.gitattributes` and editor settings.

---

## Current Observations

- WSL Git currently reports `core.autocrlf=input`.
- The runtime backlog Markdown files are tracked as `i/lf w/lf`.
- The Windows-hosted assistant `CORE_RULES.md` was observed as UTF-8 with CRLF before editing, then briefly became mixed CRLF/LF after a WSL-side patch, and was normalized back to CRLF.
- `git diff --check` caught no whitespace errors, but Git still warned that CRLF would be replaced by LF the next time Git touches the file.
- No repo-local `.gitattributes` was found in the checked runtime and assistant repo roots during the observation.

---

## Problem

Global Git settings reduce risk, but they do not fully define cross-environment behavior because:

- Windows Git and WSL Git have separate global config files.
- VS Code, PowerShell, shell tools, patch tools, and Git may each preserve or rewrite line endings differently.
- Files under `/mnt/c` can be edited by both Linux and Windows tools.
- Without `.gitattributes`, each clone may depend on local defaults such as `core.autocrlf`.
- Without `.editorconfig`, editors may preserve the first line ending they see or apply per-user defaults.

This makes it easy to create noisy diffs, confusing Git warnings, or mixed CRLF/LF files in assistant/backlog handoff documents.

---

## Objective

Create a deliberate cross-environment text-file policy that answers:

- what `core.autocrlf`, `core.eol`, and `core.safecrlf` should be on Windows Git and WSL Git,
- whether `personal-ai-runtime` and `personal-ai-assistant` should use the same `.gitattributes` policy,
- whether Markdown should be LF everywhere or CRLF in Windows-hosted assistant docs,
- which file types should be forced to LF or CRLF,
- whether `.editorconfig` should be added to match the Git policy,
- and which validation commands should be used before commit checkpoints.

---

## Non-goals

This follow-up should not:

- Reformat every existing file without an explicit normalization decision.
- Change runtime behavior, test logic, or module implementation code.
- Treat line-ending warnings as proof of a Codex sandbox defect.
- Move the assistant or private context repos into WSL2.
- Override user/editor preferences without recording the chosen repo policy.
- Mix this investigation into audio-topology-runtime MVP work.

---

## Candidate Investigation Steps

1. Record Windows Git global line-ending config:
   - `git config --global --get core.autocrlf`
   - `git config --global --get core.eol`
   - `git config --global --get core.safecrlf`
2. Record WSL Git global line-ending config with the same keys.
3. For each affected repo, record:
   - `git ls-files --eol`
   - existing `.gitattributes`
   - existing `.editorconfig`
   - representative Markdown, shell, PowerShell, JSON, and YAML file eol states.
4. Decide repo-local `.gitattributes` rules, such as:

```gitattributes
* text=auto

*.md text eol=lf
*.json text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.sh text eol=lf
*.ps1 text eol=crlf
*.bat text eol=crlf
*.cmd text eol=crlf
```

5. Decide whether `personal-ai-assistant` needs a different Markdown policy, such as `*.md text eol=crlf`.
6. Decide whether `.editorconfig` should enforce matching line endings for common editors.
7. Test one safe sample edit from WSL and one safe sample edit from Windows, then compare `git ls-files --eol` and `git diff --check`.
8. Record normalization steps only if an explicit repo policy is accepted.

---

## Candidate Evidence To Collect

For each repo under review, record:

- repo path,
- operating side used for the check: Windows or WSL,
- Git version,
- global Git line-ending settings,
- repo-local Git line-ending settings,
- `.gitattributes` and `.editorconfig` presence,
- `git ls-files --eol` summary for representative files,
- whether any file reports mixed or unexpected working-tree eol,
- editor used for the sample edit,
- validation command results,
- and recommended policy.

Suggested compact log shape:

```md
### Observation

- Repo:
- Side:
- Git config:
- Attributes:
- Editor config:
- Representative eol:
- Sample edit:
- Validation:
- Recommendation:
```

---

## Acceptance Criteria

This follow-up is complete when:

- [ ] Windows Git and WSL Git line-ending configs are recorded.
- [ ] `personal-ai-runtime` and `personal-ai-assistant` current eol states are sampled with `git ls-files --eol`.
- [ ] A repo-local `.gitattributes` recommendation exists for each repo.
- [ ] A matching `.editorconfig` recommendation exists, or a reason to skip it is recorded.
- [ ] The recommendation clearly states whether Markdown should be LF or CRLF in each repo.
- [ ] At least one WSL-side and one Windows-side sample edit are validated without mixed CRLF/LF.
- [ ] Any normalization plan is separated from the investigation and can be reviewed before broad file churn.

---

## Review Notes

This follow-up was split from `RT-FU-001` because the observed issue is a cross-workspace policy question, not a Codex Windows sandbox spawn failure.

It is also separate from `WS-FU-001` because the WSL2 migration spike is already completed; this item tracks one remaining operational gap before the mixed Windows / WSL2 workflow feels boring in the good way.

---

## Recommended Commit Message

```text
docs(backlog): add WS-FU-002 line ending policy follow-up
```
