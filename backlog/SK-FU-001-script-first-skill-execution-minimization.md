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
- Added a spec/test evolution plan validator under `spec-test-evolution` with regression tests and documented invocation.
- Added a prompt-to-playbook request inspection helper under `prompt-to-playbook` with regression tests and documented invocation.
- Added a root script-first evidence gate to `spec-driven-change-verification` that points to existing deterministic helpers.
- Added script-first evidence guidance to judgement-heavy `intent-analysis` without adding unnecessary automation.
- Added script-first evidence guidance to judgement-heavy `decision-proposal` without adding unnecessary automation.
- Added script-first evidence guidance to judgement-heavy `devils-advocate-review` without adding unnecessary automation.
- Added script-first evidence guidance to judgement-heavy `test-promotion` without adding unnecessary automation.
- Extended the playbook/skill inventory audit to warn when skills with `scripts/` lack Windows plus Linux/POSIX/macOS invocation coverage or a documented platform limitation.
- Added Windows plus Linux/macOS invocation coverage notes to existing script-bearing skills that did not explicitly document both sides.

Still open:

- Decide whether each `SKILL.md` should later receive machine-readable `metadata.execution_profile`.

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

#### `spec-test-evolution`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Validating local JSON spec/test evolution plan artifacts before editing specs, tests, indexes, or workflow notes.
- Checking required `decision_source`, `affected_artifacts`, `updates`, `traceability`, `rerun_point`, and `next_validation_step` fields.
- Checking affected artifacts and updates shape.
- Checking at least one non-empty update group is declared.
- Checking parent and child traceability refs are present and non-empty.
- Warning when decision source appears unresolved.
- Warning when root index traceability is absent or empty.
- Structured JSON output for downstream workflow and merge-gate checks.

Test / validation actions:

- Added `agent-skills/spec-test-evolution/scripts/validate_spec_test_evolution_plan.py`.
- Added `tests/agent_skills/test_validate_spec_test_evolution_plan.py`.
- Updated `agent-skills/spec-test-evolution/SKILL.md` with script-first invocation guidance.
- Covered valid evolution plans, missing required fields, empty update groups, missing traceability refs, ambiguous decision-source warnings, and missing root-index traceability warnings.
- Ran `python -m unittest tests.agent_skills.test_validate_spec_test_evolution_plan`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\spec-test-evolution --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `python agent-skills\spec-test-evolution\scripts\validate_spec_test_evolution_plan.py <temp-sample-evolution-plan.json> --json`.
- Ran `git diff --check`.

Direct smoke result:

- The helper reported the temporary sample evolution plan as `valid: true` with no findings.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `prompt-to-playbook`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Inspecting deterministic repository facts before creating or updating a local playbook.
- Checking optional source prompt/example file existence and kind.
- Checking target playbook path stays under `agent-playbooks/`.
- Checking target playbook uses a Markdown filename.
- Parsing `agent-playbooks/README.md` Playbook / Skill mapping rows.
- Detecting whether the target playbook already has a README row.
- Extracting mapped skills and playbook status.
- Warning when a new playbook needs a README row with Skill `-` and Status `draft`.
- Warning when updating a mapped `aligned` or `aligned-with-followups` playbook requires `skill-extracted` status until resync.
- Structured JSON output for downstream workflow consumption.

Test / validation actions:

- Added `agent-skills/prompt-to-playbook/scripts/inspect_playbook_request.py`.
- Added `tests/agent_skills/test_inspect_playbook_request.py`.
- Updated `agent-skills/prompt-to-playbook/SKILL.md` with script-first invocation guidance.
- Updated `agent-playbooks/prompt-to-playbook.md` with matching deterministic evidence guidance.
- Covered existing unmapped draft playbooks, missing README rows for new playbooks, mapped aligned playbooks requiring status changes, outside-playbook target rejection, and source prompt file evidence.
- Ran `python -m unittest tests.agent_skills.test_inspect_playbook_request`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\prompt-to-playbook --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `python agent-skills\prompt-to-playbook\scripts\inspect_playbook_request.py --repo-root . --target-playbook agent-playbooks\prompt-to-playbook.md --json`.
- Ran `git diff --check`.

Direct smoke result:

- The helper reported `valid: true` for `agent-playbooks/prompt-to-playbook.md`, detected the existing README mapping to `prompt-to-playbook/`, and warned that updating a mapped `aligned` playbook requires `skill-extracted` status until resync.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `spec-driven-change-verification`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Added a root skill script-first evidence gate before LLM judgement.
- Pointed routine entry checks to existing diff, impact, and mutation/test tooling evidence helpers.
- Pointed artifact-specific checks to existing orchestrator state, context manifest, subagent job contract, and spec/test evolution plan validators.
- Required the root workflow to run available deterministic checks for the current step or state why no local script-first check applies.
- Kept the full source playbook out of routine execution context and did not change trigger behavior or README status.

Test / validation actions:

- Updated `agent-skills/spec-driven-change-verification/SKILL.md` with script-first evidence gate guidance.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\spec-driven-change-verification --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `git diff --check`.

Direct smoke result:

- The UTF-8-safe validator reported the root skill as valid.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `intent-analysis`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Added script-first guidance before intent inference.
- Pointed local repo evidence collection to existing diff and impact evidence helpers.
- Required fallback evidence to be stated when local repo artifacts are unavailable.
- Kept LLM judgement scoped to inferred intent, confidence, contradictions, spec alignment, and behavior drift risk.
- Avoided adding a new helper because the skill is primarily semantic and can reuse existing deterministic evidence collectors.

Test / validation actions:

- Updated `agent-skills/intent-analysis/SKILL.md` with script-first evidence guidance.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\intent-analysis --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `git diff --check`.

Direct smoke result:

- The UTF-8-safe validator reported `intent-analysis` as valid.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `decision-proposal`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Added script-first guidance before framing human decision options.
- Pointed local repo evidence collection to existing impact, validation-result, mutation/tool availability, and orchestrator-state helpers.
- Required fallback evidence to be stated when local artifacts are unavailable.
- Kept LLM judgement scoped to why a decision is needed, option tradeoffs, recommendation labeling, and required updates.
- Avoided adding a new helper because the skill is primarily human-governance framing and can reuse existing deterministic evidence collectors.

Test / validation actions:

- Updated `agent-skills/decision-proposal/SKILL.md` with script-first evidence guidance.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\decision-proposal --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `git diff --check`.

Direct smoke result:

- The UTF-8-safe validator reported `decision-proposal` as valid.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `devils-advocate-review`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Added script-first guidance before adversarial semantic review.
- Required deterministic evidence collection from file reads, targeted `rg`, diff/impact evidence helpers, existing test results, or context manifests when available.
- Kept LLM judgement scoped to hidden assumptions, edge cases, compatibility risk, migration cost, overdesign, and decomposition-blocking objections.
- Avoided adding a new helper because the skill is primarily review judgement and can reuse existing deterministic evidence collectors.

Test / validation actions:

- Updated `agent-skills/devils-advocate-review/SKILL.md` with script-first evidence guidance.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\devils-advocate-review --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct smoke result:

- The UTF-8-safe validator reported `devils-advocate-review` as valid.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `test-promotion`

Status: completed for this follow-up pass.

Scriptable portion covered:

- Added script-first guidance before promotion judgement.
- Required deterministic evidence collection from validation artifacts, test runner output, mutation/effectiveness summaries, diff/impact evidence helpers, and targeted file reads when available.
- Kept LLM judgement scoped to promotion level classification, mutation strength, traceability gaps, and whether a test should be refined, persisted, or discarded.
- Avoided adding a new helper because the skill is primarily evidence-based judgement and can reuse existing deterministic validation and mutation evidence collectors.

Test / validation actions:

- Updated `agent-skills/test-promotion/SKILL.md` with script-first evidence guidance.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\test-promotion --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct smoke result:

- The UTF-8-safe validator reported `test-promotion` as valid.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.

#### `playbook-to-skill` script portability audit

Status: completed for this follow-up pass.

Scriptable portion covered:

- Extended `audit_skill_inventory.py` to inspect skills that contain `scripts/`.
- Added a `script-portability` warning when a script-bearing skill does not document Windows plus Linux/POSIX/macOS invocation coverage or a platform limitation / validation gap.
- Kept portability findings as warnings, not errors, so legacy or intentionally limited helpers can still be reviewed without breaking inventory validity.
- Added regression coverage for missing and present script portability guidance.
- Added explicit Windows PowerShell plus Linux/macOS invocation coverage notes to existing script-bearing skills that lacked both terms.
- Updated `playbook-to-skill` skill and playbook text so the audit coverage is discoverable.

Test / validation actions:

- Updated `agent-skills/playbook-to-skill/scripts/audit_skill_inventory.py`.
- Updated `tests/agent_skills/test_audit_skill_inventory.py`.
- Updated script-bearing `SKILL.md` files with explicit cross-platform invocation coverage notes.
- Updated `agent-playbooks/playbook-to-skill.md` with matching audit guidance.
- Ran `python -m unittest tests.agent_skills.test_audit_skill_inventory`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\playbook-to-skill --json`.
- Ran `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`.
- Ran `git diff --check`.

Direct smoke result:

- The focused audit test reported 5 tests OK.
- The full test suite reported 53 tests OK.
- The UTF-8-safe validator reported `playbook-to-skill` as valid.
- The inventory audit reported `valid: true`, 16 playbook rows, 25 skill rows, and no findings.
- The first sandboxed inventory audit rerun hit the known `windows sandbox: spawn setup refresh`; the same command succeeded when rerun with escalated execution.

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
- [x] High-priority aligned / aligned-with-followups skills explicitly prefer deterministic discovery before LLM judgement where applicable.
- [x] Future script additions include Windows and Linux invocation coverage or explicitly document why not.
- [x] The rule does not require scripts for purely semantic judgement tasks.
- [x] The update does not silently change current skill triggers, output contracts, or extraction maps.
- [x] `agent-skills/README.md` and `agent-playbooks/README.md` remain synchronized after any status or mapping changes.

---

## Review Notes

This backlog item is intentionally non-blocking.

The existing aligned and aligned-with-followups skills remain usable. The gap is execution efficiency and verification discipline, not a known correctness failure in the current skill contracts.

---

## Recommended Commit Message

```text
docs(backlog): add SK-FU-001 script-first skill follow-up
```
