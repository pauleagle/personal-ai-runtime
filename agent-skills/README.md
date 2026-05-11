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

## Skill Inventory

Status follows the definitions in `agent-playbooks/README.md`.

| Skill | Playbook | Status | Description |
|---|---|---|---|
| `preflight-protocol/` | `preflight-protocol.md` | `skill-extracted` | Check task understanding, assumptions, uncertainty, risks, next steps, and likely files before non-trivial work. |
| `changelog-normalization/` | `changelog-normalization.md` | `aligned` | Normalize changelog drafts or mixed notes into stable release history. |
| `playbook-to-skill/` | `playbook-to-skill.md` | `aligned` | Extract human-readable playbooks into concise, command-oriented Codex skills. |
| `prompt-to-playbook/` | `prompt-to-playbook.md` | `aligned` | Generalize one-off prompts, successful examples, or repeated instructions into maintainable playbooks. |

## Naming

Use short, lowercase, hyphenated folder names.

Good examples:

- `preflight-protocol`
- `release-checklist`
- `doc-maintenance`

## Per-skill README files

A separate `README.md` inside an individual skill folder is optional. Add one only when the skill needs human-facing maintenance notes, examples, test instructions, or design rationale that would make `SKILL.md` too noisy.
