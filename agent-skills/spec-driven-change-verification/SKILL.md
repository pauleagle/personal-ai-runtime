---
name: spec-driven-change-verification
description: Use for spec-driven implementation and verification workflows, including module or poc-module phase work, atomic item execution, spec/test evolution, diff-aware verification, JIT test selection, mutation-aware validation, human decision gates, and durable orchestrator-state handoffs.
---

# Spec-Driven Change Verification

## Purpose

Run a spec-first, mutation-aware, human-governed verification workflow without relying on one long chat as the source of state. Use this as the root/orchestrator skill; treat `agent-playbooks/spec-driven-change-verification-workflow-playbook.md` as design background, not as default execution context.

## Script-First Execution

Before LLM judgement, collect deterministic evidence that matches the current workflow step and available artifacts. Use only the relevant helpers; do not run scripts just to create noise.

Common entry checks:

```sh
python agent-skills/diff-analysis/scripts/collect_git_diff_evidence.py --repo-root . --json
python agent-skills/impact-analysis/scripts/collect_impact_evidence.py --repo-root . --json
python agent-skills/mutation-testing/scripts/detect_mutation_test_tools.py --repo-root . --json
```

When the corresponding artifacts exist, validate them before semantic interpretation:

```sh
python agent-skills/orchestrator-state-machine/scripts/validate_orchestrator_state.py path/to/state.json --json
python agent-skills/context-pack-builder/scripts/build_context_manifest.py --repo-root . --json <source> [<source> ...]
python agent-skills/atomic-subagent-runner/scripts/validate_subagent_job_contract.py path/to/job.json --json
python agent-skills/spec-test-evolution/scripts/validate_spec_test_evolution_plan.py path/to/evolution-plan.json --json
```

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

Use LLM reasoning after these checks to interpret impact, resolve ambiguity, classify gaps, frame human decisions, and decide which child skill should own the next step.

## Playbook Access Rule

Do not read the full source playbook during normal execution.

Start with this root skill, the relevant child skill, project instructions, the target spec or atomic item, current diff, tests, and durable state artifacts.

Read `agent-playbooks/spec-driven-change-verification-workflow-playbook.md` only when:

- the user asks for playbook/skill alignment, extraction, or workflow design;
- a child-skill boundary or extraction map must be checked;
- the skills conflict and the original design rationale is needed;
- the task explicitly requires updating the playbook itself.

When playbook context is needed, search for the specific section and read only the relevant excerpt. Do not pull the full playbook into context as a routine setup step.

## Prompt Contract

Stable prefix:

- Skill: `spec-driven-change-verification`
- Execution Profile: `hybrid`
- Reusable Rules: spec defines correctness with traceable refs; report mutation honestly; humans decide ambiguity and breaking behavior; durable state lives outside chat.
- Scope / Governance Defaults: not for trivial edits with no behavior, spec, or test impact; do not start implementation while spec refs or acceptance criteria are materially unclear; do not merge unrelated refactors into an atomic item or mark a workflow step complete while validation, state updates, or human decisions are missing.
- Output Contract: see the `### Spec-Driven Change Verification Report` template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

## Workflow

1. Run deterministic evidence checks available for the current workflow step, or state why no local script-first check applies.
2. Read the relevant project instructions, spec, active atomic item or phase, README/index files, current git status, and durable state artifacts. Do not read the full source playbook by default.
3. If the task is complex or ambiguous, run `preflight-protocol` before changing files.
4. Identify the current workflow step, selected workflow, atomic item ID, spec refs, durable state location, allowed scope, forbidden scope, and human decision status.
5. If requirements or acceptance criteria are unclear, stop implementation and produce spec drill-down questions or a spec gap report.
6. Before atomic decomposition, ensure Devil's Advocate objections are numbered, resolved, deferred with rationale, or accepted by the human; unresolved objections block implementation.
7. Work on one atomic item at a time. Design or select spec-traced tests before or alongside implementation.
8. After implementation, inspect the diff to infer intent, impacted components, impacted specs, impacted tests, risks, and validation gaps.
9. Run focused tests and add or select JIT tests when the diff exposes uncovered behavior.
10. Use impact/JIT evidence to choose a validation scope: run focused tests and scoped mutation inside the atomic-item loop; reserve full suites or full mutation runs for checkpoint gates, broad-impact changes, or release-level confidence.
11. Validate test effectiveness with mutation testing when available; prefer scoped manual mutation for one to three meaningful impacted risks when framework mutation would force irrelevant full-scope cost.
12. Classify results as code issue, test gap, spec gap, equivalent mutation, accepted risk, or human decision required.
13. Update specs, tests, README/index files, orchestrator state, atomic metadata, run notes, or handoff artifacts when the workflow step requires durable state.
14. Advance `workflow_step` only after the current step's validation and durable-state updates are complete.

## Child Skill Delegation

Use these child skills when the task matches their trigger:

- `spec-drill-down`: clarify ambiguous requirements into testable spec candidates.
- `spec-definition`: create or revise the formal correctness contract.
- `devils-advocate-review`: challenge a draft plan or spec before implementation.
- `devils-advocate-drill-down`: resolve numbered objections before atomic decomposition.
- `workflow-atomic-decomposition`: split a revised spec into selected workflow slices and atomic items.
- `orchestrator-state-machine`: maintain workflow state, `workflow_step`, dependency graph, gates, and checkpoint status.
- `context-pack-builder`: prepare bounded context packs for stateless subagents.
- `atomic-subagent-runner`: launch or supervise one bounded subagent job and validate its structured result.
- `spec-based-test-design`: design tests from accepted specs and atomic items with traceability.
- `diff-analysis`: inspect diffs for changed components, behavior candidates, and unrelated edits.
- `intent-analysis`: infer change intent and uncertainty from request, spec, and diff.
- `impact-analysis`: identify impacted specs, tests, components, risks, and validation gaps.
- `jit-test-generation`: select or generate focused candidate tests from diff, intent, impact, and spec refs.
- `mutation-testing`: validate test effectiveness with framework or scoped manual mutation.
- `test-effectiveness-evaluation`: classify effective tests, weak tests, survived mutations, and validation gaps.
- `decision-proposal`: prepare human decision options for ambiguity, gaps, and behavior changes.
- `test-promotion`: promote, persist, refine, or discard generated and candidate tests.
- `spec-test-evolution`: update specs, tests, indexes, and traceability after accepted decisions.

## Mandatory Rules

- Spec defines correctness; tests, JIT tests, mutation results, and implementation choices must trace back to spec refs or risk items.
- Do not write tests only for coverage. Every durable test needs a semantic source.
- Do not trust generated tests until they pass baseline execution and, when relevant, kill a meaningful mutation.
- Do not claim mutation tooling was run if it was not. State when mutation was manual, scoped, skipped, or blocked.
- Do not treat full-scope mutation as the default inner loop. If validation cost is growing, first narrow by diff, intent, impact set, spec refs, and JIT risk items.
- Use full unit or full mutation runs as explicit checkpoint evidence, not as a substitute for impact analysis.
- Humans decide ambiguity, breaking behavior, accepted risk, and spec evolution. The agent may propose options, not silently redefine correctness.
- Keep durable workflow state outside chat: atomic item metadata, `workflow_step`, dependency edges, validation results, remaining gaps, and decision status belong in project artifacts.
- Treat subagents as stateless bounded workers. Pass only the required context pack and require structured output.
- Prefer commit-then-advance for atomic items when the workflow uses commit checkpoints.
- Keep backlog, proposed, accepted, deferred, and rejected items clearly separated.
- Keep the full source playbook out of routine execution context unless the Playbook Access Rule allows it.

## Boundaries

- Do not use this skill for trivial edits that do not affect behavior, tests, specs, or workflow state.
- Do not start implementation while spec refs, allowed scope, or acceptance criteria are materially unclear.
- Do not merge unrelated refactors into an atomic item.
- Do not mark a workflow step complete when validation, state updates, or human decisions are still missing.
- Do not use the source playbook as a substitute for selecting the correct child skill.

## Validation

Before reporting completion, check:

1. The implemented change maps to spec refs and the current atomic item.
2. Focused tests or an explicit test-gap explanation are present.
3. Validation scope is justified as focused, JIT, scoped mutation, full-suite checkpoint, or skipped/blocked.
4. Mutation testing or scoped manual mutation reasoning is reported honestly.
5. Diff analysis found no unrelated changes.
6. Durable state, README/index files, spec files, or run notes were updated when required.
7. Remaining gaps and human decision points are explicit.
8. If the source playbook was read, the reason and section scope are reported.

## Output

Use this report template:

```md
### Spec-Driven Change Verification Report

- Current workflow step and atomic item:
- Spec refs and allowed scope:
- Playbook sections read, if any:
- Changes made:
- Tests and validation run:
- Mutation result or manual mutation note:
- Gap classification:
- Durable state updates:
- Human decisions needed:
- Next step:
```
