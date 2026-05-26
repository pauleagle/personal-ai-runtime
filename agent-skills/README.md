# Agent Skills

This directory contains Codex-loadable skills. Each skill provides concise, actionable instructions for a specific agent workflow or capability.

## Structure

Each skill lives in its own folder and must include a `SKILL.md`.

```text
agent-skills/
  preflight-protocol/
    SKILL.md
```

Optional supporting files may be added when a skill needs reusable scripts, references, templates, or assets.

```text
agent-skills/
  example-skill/
    SKILL.md
    scripts/
    references/
    assets/
```

## SKILL.md

`SKILL.md` is the agent-facing entry point. Keep it focused on what the agent needs at execution time:

- When the skill should be used
- What the agent must do
- What the agent must avoid
- Required output format or workflow
- Any files, tools, or constraints the agent should consider

Avoid placing long background notes, design history, or broad project documentation in `SKILL.md`.

## Relationship to Playbooks

Some skills are derived from or aligned with files in `agent-playbooks/`.

A playbook describes the intended behavior at the workflow or policy level. A skill translates that behavior into concise instructions an agent can load and execute.

When a skill is based on a playbook, keep the two aligned:

- Preserve the playbook's core intent and constraints.
- Make the skill concise and execution-oriented.
- Add implementation rules only when they help the agent apply the workflow reliably.
- Re-check the related playbook when changing the skill.
- For large playbooks, one playbook may map to a root/orchestrator skill plus child or shared skills; keep the root skill first in README mappings and mark the set `aligned` only after all mapped skills are reviewed together.

## Skill Inventory

Status follows the definitions in `agent-playbooks/README.md`.

| Skill | Playbook | Status | Description |
|---|---|---|---|
| `preflight-protocol/` | `preflight-protocol.md` | `aligned` | Check task understanding, assumptions, uncertainty, risks, next steps, and likely files before non-trivial work. |
| `changelog-normalization/` | `changelog-normalization.md` | `aligned` | Normalize changelog drafts or mixed notes into stable release history. |
| `playbook-to-skill/` | `playbook-to-skill.md` | `aligned` | Extract human-readable playbooks into one or more concise Codex skills, including orchestrator/child layouts and alignment checks. |
| `prompt-to-playbook/` | `prompt-to-playbook.md` | `aligned` | Generalize one-off prompts, successful examples, or repeated instructions into maintainable playbooks. |
| `spec-driven-change-verification/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Root/orchestrator skill for spec-first, mutation-aware, human-governed change verification workflows. |
| `spec-drill-down/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Clarify ambiguous requirements into testable spec candidates before implementation. |
| `spec-definition/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Create or revise formal correctness specs with scope, rules, acceptance criteria, and testing implications. |
| `devils-advocate-review/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Challenge draft plans or specs before implementation and produce numbered objections. |
| `devils-advocate-drill-down/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Resolve numbered objections and gate workflow atomic decomposition. |
| `workflow-atomic-decomposition/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Split revised specs into selected workflow slices, atomic items, dependencies, and verification loops. |
| `orchestrator-state-machine/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Maintain durable workflow state, live `workflow_step`, dependency graph, gates, and checkpoints. |
| `context-pack-builder/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Build bounded context packs for stateless subagent jobs. |
| `atomic-subagent-runner/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Run or evaluate one bounded subagent job and return structured results. |
| `spec-based-test-design/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Design spec-traced tests from accepted specs and atomic items. |
| `diff-analysis/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Analyze diffs for changed components, behavior candidates, and verification scope. |
| `intent-analysis/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Infer change intent, confidence, uncertainty, and spec alignment from context and diff. |
| `impact-analysis/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Identify impacted specs, tests, components, risks, and validation gaps. |
| `jit-test-generation/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Select or generate focused candidate tests with diff/intent/impact traceability. |
| `mutation-testing/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Validate test effectiveness with mutation tooling or scoped manual mutation checks. |
| `test-effectiveness-evaluation/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Interpret test and mutation results into effectiveness and gap classifications. |
| `decision-proposal/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Prepare human decision options for ambiguity, validation gaps, or behavior changes. |
| `test-promotion/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Promote, persist, refine, or discard generated and candidate tests based on evidence. |
| `spec-test-evolution/` | `spec-driven-change-verification-workflow-playbook.md` | `skill-extracted` | Update specs, tests, indexes, and traceability after accepted decisions or gap analysis. |
| `nested-module-git-initialization/` | `nested-module-git-initialization.md` | `skill-extracted` | Check and initialize Git boundaries for nested child projects under `modules/` or `poc-modules/`. |
| `utf8-traditional-chinese-defaults/` | `utf8-traditional-chinese-defaults.md` | `aligned` | Default text work to UTF-8, prefer Traditional Chinese for Chinese output, and use explicit UTF-8 encoding for PowerShell text I/O. |

## Naming

Use short, lowercase, hyphenated folder names.

Good examples:

- `preflight-protocol`
- `release-checklist`
- `doc-maintenance`

## Per-skill README files

A separate `README.md` inside an individual skill folder is optional. Add one only when the skill needs human-facing maintenance notes, examples, test instructions, or design rationale that would make `SKILL.md` too noisy.
