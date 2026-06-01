# SK-FU-001 Script-First Skill Execution Minimization

## Metadata

- Type: Skill Follow-up
- ID: SK-FU-001
- Status: Draft
- Source Review: `agent-skills/README.md` aligned / aligned-with-followups inventory review
- Suggested Location: `backlog/SK-FU-001-script-first-skill-execution-minimization.md`
- Scope:
  - `agent-skills/README.md`
  - `agent-playbooks/README.md`
  - aligned skills
  - aligned-with-followups skills
- Principle: 能用 script 就不用 LLM
- Integration Status: Partially integrated
- Status Impact: No current README status change; this is a non-blocking cross-skill maintenance follow-up.
- Script Portability: Future reusable skill scripts should support Windows and Linux by default, preferably through one portable implementation plus thin shell wrappers.

---

## Summary

Review the `aligned` and `aligned-with-followups` skills under the minimization principle:

> If a deterministic script, parser, validator, grep, status command, or test command can answer a question reliably, run that first and reserve LLM reasoning for interpretation, judgement, synthesis, and unresolved ambiguity.

The current skill inventory is usable, but many skills still describe human/LLM review steps without explicitly requiring deterministic discovery or validation before semantic reasoning. This follow-up should add a shared script-first execution rule and supporting validation scripts where they reduce repeated LLM work.

---

## Current Integration Progress

Completed:

- Added an `Execution Profile` section to `agent-skills/README.md`.
- Added a `Profile` column to the skill inventory.
- Classified each current aligned / aligned-with-followups skill as `script`, `hybrid`, `low-llm`, or `heavy-llm`.
- Kept the classification at the README index layer only, so existing `SKILL.md` frontmatter and trigger behavior remain unchanged.
- Added cross-platform script guidance for future reusable skill scripts.
- Added Windows / Linux wrapper guidance to `nested-module-git-initialization`.
- Completed the first low-complexity per-skill script-first pass for `nested-module-git-initialization` by adding regression tests for its existing Python helper and wrappers contract.
- Added a UTF-8-safe skill validation wrapper under `utf8-traditional-chinese-defaults` with regression tests and documented invocation.
- Added a repeatable playbook/skill inventory audit script under `playbook-to-skill` with regression tests and documented invocation.
- Added a changelog structure evidence helper under `changelog-normalization` with regression tests and documented script-first invocation.
- Added an atomic subagent job contract validator under `atomic-subagent-runner` with regression tests and documented invocation.

Still open:

- Decide whether each `SKILL.md` should later receive machine-readable `metadata.execution_profile`.
- Review remaining high-priority skills one by one before adding per-skill script-first rules beyond the README profile hint.
- Audit future script additions for Windows and Linux invocation coverage.

---

## Review Method

The review intentionally used scriptable checks first:

- Parsed `agent-skills/README.md` for rows with status `aligned` or `aligned-with-followups`.
- Counted matching skills and grouped by status.
- Checked each mapped `agent-skills/<skill>/SKILL.md` for:
  - frontmatter `name`,
  - line count,
  - presence of `scripts/`,
  - whether the skill text mentions scriptable tools or commands.
- Ran the existing `quick_validate.py` validator against the target skills where possible.
- Used `rg` / `Select-String` style searches for command/tool references.

No semantic alignment was accepted purely from memory or impression.

---

## Scripted Review Findings

| Status | Skills Reviewed | Mention Scriptable Tooling | Has `scripts/` Directory |
|---|---:|---:|---:|
| `aligned` | 6 | 5 | 0 |
| `aligned-with-followups` | 19 | 4 | 0 |
| Total | 25 | 9 | 0 |

Validator result:

- 23 / 25 skills were mechanically valid with `quick_validate.py`.
- `changelog-normalization` and `prompt-to-playbook` triggered `UnicodeDecodeError` under Windows `cp950` default decoding.
- The two failures appear to be validator UTF-8 handling issues, not confirmed skill frontmatter defects, because both files read correctly with `Get-Content -Encoding UTF8`.

Important caveat:

- The existing validator script uses Python `Path.read_text()` without explicit `encoding="utf-8"`.
- For Traditional Chinese or mixed-language skills, validation itself should be UTF-8-safe before its result is treated as authoritative.

---

## Problem

Several aligned skills can benefit from deterministic pre-checks, but the current skill set does not define a shared rule for when scripts or command output must precede LLM judgement.

This causes avoidable issues:

- LLM review may re-derive facts that `rg`, `git`, tests, or validators could answer directly.
- Alignment checks may depend on prose reading instead of inventory parsing.
- Skill frontmatter validation may be skipped or run inconsistently.
- Windows UTF-8 pitfalls can make a validator fail before the skill content is actually inspected.
- Spec-driven skills may ask an LLM to classify state before basic artifacts, diffs, statuses, and test outputs are collected.
- Script helpers may accidentally become Windows-only or Linux-only if path separators, shells, or command names are hard-coded without wrappers.

---

## Objective

Add a shared script-first minimization rule for aligned and aligned-with-followups skills.

The rule should make deterministic checks the first step whenever the question is about:

- file existence,
- README inventory rows,
- frontmatter validity,
- status values,
- changed files and diffs,
- path routing,
- Git boundaries,
- available tests,
- command availability,
- generated artifacts,
- changelog headings,
- encoding/readability,
- or validation outputs.

LLM reasoning should then summarize, interpret, compare, or decide only after those facts are collected.

---

## Non-goals

This follow-up should not:

- Replace semantic review, risk analysis, design judgement, or human decisions with scripts.
- Force every skill to have a `scripts/` directory.
- Add heavyweight automation for one-off judgement tasks.
- Change all `aligned` statuses to `aligned-with-followups` immediately.
- Edit all skill files in one large sweep without a focused implementation plan.
- Treat script output as authoritative when the script is known to be encoding-unsafe or scope-blind.

---

## Proposed Shared Rule

Suggested concise rule for `agent-skills/README.md` or a shared skill maintenance section:

```md
### Script-First Minimization

For aligned skills, prefer deterministic checks before LLM reasoning. If a script, parser, `rg`, `git`, test command, validator, or file read can establish a fact, run it first and use the LLM only to interpret the result, resolve ambiguity, or make a judgement that cannot be scripted safely.

Do not ask the LLM to infer file existence, status rows, frontmatter validity, changed files, command availability, or test outcomes when a local command can verify them.
```

Suggested script portability rule:

```md
When adding reusable skill scripts, support Windows and Linux by default. Prefer one portable implementation, such as Python, with thin PowerShell and POSIX shell wrappers when wrapper ergonomics help. If a script cannot be cross-platform, document the limitation and validation gap in the skill.
```

Suggested compact rule for individual skills:

```md
Before semantic judgement, run deterministic discovery and validation available for this task. Use LLM reasoning only for synthesis, gap classification, and decisions that cannot be answered safely by command output.
```

---

## Candidate Scriptable Checks

| Area | Candidate Check |
|---|---|
| Skill inventory | Parse `agent-skills/README.md` and `agent-playbooks/README.md` tables; detect missing mapped files and status mismatches. |
| Skill frontmatter | Validate `SKILL.md` YAML with explicit UTF-8 decoding; confirm `name` matches folder name. |
| Skill size / shape | Count lines, detect unexpectedly long skills, and flag missing required sections. |
| Playbook mapping | Confirm mapped playbooks exist and that one-to-many mappings list the root skill first. |
| Git boundaries | Use `Test-Path <module>/.git` and `git -C <module> status --short` before child-module edits. |
| Diff analysis | Use `git status`, `git diff --name-only`, `git diff --stat`, and targeted `rg` before LLM impact analysis. |
| Encoding | Read Markdown with explicit UTF-8 and fail clearly on mojibake or validator encoding errors. |
| Script portability | Prefer portable runtimes, avoid hard-coded path separators, and document Windows plus Linux invocation. |
| Mutation/test availability | Detect installed mutation/test tools before claiming they ran. |

---

## Priority Candidates

### High

- `playbook-to-skill`
- `prompt-to-playbook`
- `spec-driven-change-verification`
- `diff-analysis`
- `impact-analysis`
- `mutation-testing`
- `nested-module-git-initialization`
- `utf8-traditional-chinese-defaults`

Reason:

These skills already depend on inventory, filesystem, Git, test, mutation, or encoding facts that scripts can verify cheaply.

### Per-Skill Implementation Log

#### `nested-module-git-initialization`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Deterministic child project root validation for `modules/<project>` and `poc-modules/<project>`.
- Direct `.git` boundary detection before LLM judgement.
- Optional `git init` execution only when explicitly requested by the helper flag.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Made `scripts/check_nested_module_git.py` testable with injected `argv` and `repo_root`, without changing CLI behavior.
- Added `tests/agent_skills/test_nested_module_git_initialization.py`.
- Covered missing boundary, requested initialization, existing boundary, and invalid nested path rejection.
- Ran `python -m unittest tests.agent_skills.test_nested_module_git_initialization`.
- Ran `python -m unittest discover -s tests`.
- Ran `python C:/Users/pauleagle/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-skills/nested-module-git-initialization`.
- Ran `python agent-skills\nested-module-git-initialization\scripts\check_nested_module_git.py --project-root modules/style-fit-profiler --json`.
- Ran `git diff --check`.

Direct smoke result:

- The helper reported `action: existing-boundary` for `modules/style-fit-profiler`; no initialization was needed.

#### `utf8-traditional-chinese-defaults`

Status: completed for this follow-up pass.

Scriptable portion covered:

- UTF-8-safe `SKILL.md` validation using explicit `encoding="utf-8"`.
- Clean decode-error reporting for non-UTF-8 skill files.
- Structured JSON output for downstream workflow consumption.
- Deterministic frontmatter validation before LLM interpretation of encoding or validator failures.

Test / validation actions:

- Added `agent-skills/utf8-traditional-chinese-defaults/scripts/validate_skill_utf8.py`.
- Added `tests/agent_skills/test_validate_skill_utf8.py`.
- Covered valid UTF-8 Traditional Chinese frontmatter, non-UTF-8 rejection, and invalid frontmatter shape.
- Ran `python -m unittest tests.agent_skills.test_validate_skill_utf8`.
- Ran `python -m unittest discover -s tests`.
- Ran `python C:/Users/pauleagle/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-skills/utf8-traditional-chinese-defaults`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\utf8-traditional-chinese-defaults --json`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\changelog-normalization --json`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\prompt-to-playbook --json`.

#### `diff-analysis`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Deterministic collection of `git status --short`.
- Deterministic collection of `git diff --name-only`.
- Deterministic collection of `git diff --name-status`.
- Deterministic collection of `git diff --stat`.
- Optional staged-only evidence collection.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/diff-analysis/scripts/collect_git_diff_evidence.py`.
- Added `tests/agent_skills/test_collect_git_diff_evidence.py`.
- Covered working tree diff evidence, staged diff evidence, and non-repository rejection.
- Ran `python -m unittest tests.agent_skills.test_collect_git_diff_evidence`.
- Ran `python -m unittest discover -s tests`.
- Ran `python C:/Users/pauleagle/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-skills/diff-analysis`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\diff-analysis --json`.
- Ran `python agent-skills\diff-analysis\scripts\collect_git_diff_evidence.py --repo-root . --json`.

Direct smoke result:

- The helper reported the current root repo status and confirmed no unstaged diff entries at smoke-check time; the only reported status entries were this follow-up's then-untracked script and test files.

#### `playbook-to-skill`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Parsing `agent-playbooks/README.md` Playbook / Skill mapping rows.
- Parsing `agent-skills/README.md` skill inventory rows.
- Checking allowed playbook status values and skill execution profiles.
- Checking mapped playbook and skill paths exist.
- Checking `SKILL.md` frontmatter `name` matches the skill folder.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/playbook-to-skill/scripts/audit_skill_inventory.py`.
- Added `tests/agent_skills/test_audit_skill_inventory.py`.
- Covered synchronized inventory, invalid status/profile values, and frontmatter/folder name mismatch.
- Ran `python -m unittest tests.agent_skills.test_audit_skill_inventory`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\playbook-to-skill --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Legacy `quick_validate.py` still hit `UnicodeDecodeError` on this UTF-8 skill under Windows cp950 defaults; this was treated as a validator encoding limitation because the UTF-8-safe validator passed.

Direct smoke result:

- The helper reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings for the current repository.

#### `mutation-testing`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Detecting available mutation binaries without running them.
- Detecting available test runners without running tests.
- Parsing `package.json` test and mutation scripts.
- Detecting Python project markers and test directories.
- Producing candidate test/mutation commands as availability evidence.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/mutation-testing/scripts/detect_mutation_test_tools.py`.
- Added `tests/agent_skills/test_detect_mutation_test_tools.py`.
- Covered `package.json` test/mutation scripts, Python test directory detection, invalid package JSON reporting, missing repo rejection, and `npx` not counting as mutation tooling by itself.
- Ran `python -m unittest tests.agent_skills.test_detect_mutation_test_tools`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\mutation-testing\scripts\detect_mutation_test_tools.py --repo-root . --json`.

Direct smoke result:

- The helper reported `mutationToolingAvailable: false` for the current repository and suggested `python -m unittest discover -s tests` as test tooling evidence. No mutation tooling or tests were executed by the helper.

#### `impact-analysis`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Collecting `git status --short`, `git diff --name-only`, and `git diff --name-status` as changed-path evidence.
- Mechanically classifying changed paths as `source`, `tests`, `specs`, `docs`, `config`, `generated`, or `other`.
- Expanding untracked directories while excluding Python cache noise.
- Optional staged-only evidence collection.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/impact-analysis/scripts/collect_impact_evidence.py`.
- Added `tests/agent_skills/test_collect_impact_evidence.py`.
- Covered changed/untracked path classification, staged evidence collection, non-repository rejection, and untracked directory expansion.
- Ran `python -m unittest tests.agent_skills.test_collect_impact_evidence`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\impact-analysis\scripts\collect_impact_evidence.py --repo-root . --json`.

Direct smoke result:

- The helper reported the current root repo status and classified this follow-up's then-untracked script as `other` and test file as `tests`; cache files were excluded.

#### `context-pack-builder`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Building deterministic metadata for selected context source paths.
- Checking source existence, kind, repo-relative path, byte size, line count, and SHA-256.
- Reporting missing sources, directory inputs, outside-repo paths, and per-file size warnings.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/context-pack-builder/scripts/build_context_manifest.py`.
- Added `tests/agent_skills/test_build_context_manifest.py`.
- Covered UTF-8 file metadata, missing source invalidation, directory and large-file warnings, and outside-repo warnings.
- Ran `python -m unittest tests.agent_skills.test_build_context_manifest`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\context-pack-builder\scripts\build_context_manifest.py --repo-root . --json agent-skills\context-pack-builder\SKILL.md backlog\SK-FU-001-script-first-skill-execution-minimization.md`.

Direct smoke result:

- The helper reported two existing file sources, total bytes, line counts, SHA-256 hashes, and no warnings for the sampled context-pack inputs.

#### `test-effectiveness-evaluation`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Extracting deterministic evidence from text test or mutation result artifacts.
- Detecting unittest run count, runtime, and pass/fail status.
- Extracting mutation term counts for `killed`, `survived`, `equivalent`, `skipped`, and `blocked`.
- Reporting missing result files without crashing.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/test-effectiveness-evaluation/scripts/collect_validation_result_evidence.py`.
- Added `tests/agent_skills/test_collect_validation_result_evidence.py`.
- Added `tests/fixtures/validation_result_sample.txt` for smoke-check evidence.
- Covered unittest pass evidence, unittest failure evidence, mutation term count extraction, and missing result files.
- Ran `python -m unittest tests.agent_skills.test_collect_validation_result_evidence`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\test-effectiveness-evaluation\scripts\collect_validation_result_evidence.py --json tests\fixtures\validation_result_sample.txt`.

Direct smoke result:

- The helper reported `testsRun: 5`, `status: passed`, `killed: 2`, and `survived: 0` from the sample validation result fixture. No gap classification was performed by the helper.

#### `orchestrator-state-machine`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Validating durable orchestrator state JSON artifacts.
- Checking required `workflow_step`, `implementation_status`, and queue fields.
- Checking queue fields are lists.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/orchestrator-state-machine/scripts/validate_orchestrator_state.py`.
- Added `tests/agent_skills/test_validate_orchestrator_state.py`.
- Added `tests/fixtures/orchestrator_state_sample.json`.
- Covered valid state, missing required fields, and invalid queue type.
- Ran `python -m unittest tests.agent_skills.test_validate_orchestrator_state`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\orchestrator-state-machine\scripts\validate_orchestrator_state.py tests\fixtures\orchestrator_state_sample.json --json`.

Direct smoke result:

- The helper reported the sample orchestrator state as valid with `workflow_step: Step 11 - Test Execution` and empty ready/running/blocked/completed/deferred queues.

#### `changelog-normalization`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Checking target changelog file existence.
- Reading changelog text with explicit UTF-8 decoding.
- Extracting Markdown headings and H2 version / `Unreleased` sections.
- Detecting released sections missing ISO dates.
- Detecting `Unreleased` sections that are not first.
- Detecting dated version sections that are not newest-first.
- Detecting category headings and list entries before a category heading.
- Flagging likely TODO, commit-log, merge-log, or AI-residue lines as deterministic review evidence.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/changelog-normalization/scripts/analyze_changelog_structure.py`.
- Added `tests/agent_skills/test_analyze_changelog_structure.py`.
- Updated `agent-skills/changelog-normalization/SKILL.md` with script-first invocation guidance.
- Updated `agent-playbooks/changelog-normalization.md` with matching deterministic evidence guidance.
- Covered valid version/category/date extraction, missing dates, uncategorized entries, noise detection, missing changelog rejection, and outside-repo path rejection.
- Ran `python -m unittest tests.agent_skills.test_analyze_changelog_structure`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\changelog-normalization --json`.
- Ran `python C:/Users/pauleagle/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-skills/changelog-normalization`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `python agent-skills\changelog-normalization\scripts\analyze_changelog_structure.py --repo-root . --json`.
- Ran `git diff --check`.

Direct smoke result:

- The helper reported `valid: false` for the current repository because no root `CHANGELOG.md` exists; this is the expected deterministic missing-file evidence for this repo state.
- The UTF-8-safe validator reported the skill as valid. Legacy `quick_validate.py` still raised `UnicodeDecodeError` under Windows `cp950`, matching the known validator encoding limitation already recorded in this follow-up.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `atomic-subagent-runner`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Validating local JSON subagent job contract artifacts before launch or evaluation.
- Checking required `job_id`, `parent_atomic_item_id`, `subagent_role`, `context_pack`, `allowed_scope`, `forbidden_scope`, `validation_requirements`, and `output_contract` fields.
- Checking non-empty context, scope, validation, and output contract fields.
- Checking allowed / forbidden scope field shape.
- Warning when `forbidden_scope` is empty.
- Warning when `state_patch_policy` or `merge_gate` governance is absent.
- Warning when `context_pack` appears to rely on hidden chat history instead of durable artifacts.
- Structured JSON output for downstream orchestration or merge-gate checks.

Test / validation actions:

- Added `agent-skills/atomic-subagent-runner/scripts/validate_subagent_job_contract.py`.
- Added `tests/agent_skills/test_validate_subagent_job_contract.py`.
- Updated `agent-skills/atomic-subagent-runner/SKILL.md` with script-first invocation guidance.
- Covered valid contracts, missing required fields, empty required values, missing governance warnings, empty forbidden-scope warnings, and hidden chat-history context warnings.
- Ran `python -m unittest tests.agent_skills.test_validate_subagent_job_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\atomic-subagent-runner --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `python agent-skills\atomic-subagent-runner\scripts\validate_subagent_job_contract.py <temp-sample-job.json> --json`.
- Ran `git diff --check`.

Direct smoke result:

- The helper reported the temporary sample job contract as `valid: true` with no findings.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

### Medium

- `changelog-normalization`
- `context-pack-builder`
- `orchestrator-state-machine`
- `spec-test-evolution`
- `test-effectiveness-evaluation`

Reason:

These skills still need judgement, but deterministic pre-checks can reduce context load and prevent missed files, stale state, or weak validation claims.

### Lower

- `devils-advocate-review`
- `intent-analysis`
- `decision-proposal`
- `test-promotion`

Reason:

These are more judgement-heavy. Scripts should collect evidence first, but should not replace the actual reasoning output.

---

## Suggested Implementation Steps

1. Add the shared script-first minimization rule to `agent-skills/README.md`. Completed partially via the `Execution Profile` section and `Profile` inventory column.
2. Add a UTF-8-safe skill validator wrapper or update validation guidance so `quick_validate.py` failures caused by Windows default encoding are not misclassified as skill defects.
3. Add or document a small skill inventory audit script that checks:
   - README rows,
   - mapped skill/playbook existence,
   - frontmatter `name`,
   - status values,
   - missing `SKILL.md`,
   - and one-to-many mapping shape.
4. Update high-priority skills with a short "run deterministic checks first" line only where it changes execution behavior.
5. Re-run validation and confirm statuses remain correct.

---

## Acceptance Criteria

This follow-up is complete when:

- [x] A shared script-first minimization rule exists in the skill maintenance docs.
- [x] Cross-platform script guidance exists for future reusable skill scripts.
- [x] Skill validation is UTF-8-safe on Windows.
- [x] A repeatable inventory audit exists or is documented.
- [ ] High-priority aligned / aligned-with-followups skills explicitly prefer deterministic discovery before LLM judgement where applicable.
- [ ] Future script additions include Windows and Linux invocation coverage or explicitly document why not.
- [ ] The rule does not require scripts for purely semantic judgement tasks.
- [ ] The update does not silently change current skill triggers, output contracts, or extraction maps.
- [ ] `agent-skills/README.md` and `agent-playbooks/README.md` remain synchronized after any status or mapping changes.

---

## Review Notes

This backlog item is intentionally non-blocking.

The existing aligned and aligned-with-followups skills remain usable. The gap is execution efficiency and verification discipline, not a known correctness failure in the current skill contracts.

---

## Recommended Commit Message

```text
docs(backlog): add SK-FU-001 script-first skill follow-up
```
