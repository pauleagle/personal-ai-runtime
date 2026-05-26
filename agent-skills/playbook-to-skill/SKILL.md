---
name: playbook-to-skill
description: Convert an existing playbook into one or more executable agent skills, extract a single skill, split a large playbook into orchestrator and child skills, check alignment between playbook and skills, resync after playbook changes, and update Playbook / Skill README mappings.
---

# Playbook To Skill

## Purpose

Turn `agent-playbooks/` workflows into concise Codex skills while keeping playbooks human-readable. Support single-skill extraction, multi-skill extraction, orchestrator-plus-children layouts, alignment checks, and resync after playbook changes.

## Workflow

1. Read the target playbook, `agent-playbooks/README.md`, `agent-skills/README.md`, and any mapped skills.
2. Determine whether the user wants assessment only, a single skill, a root/orchestrator skill, child skills, an extraction map only, an alignment check, or resync after playbook changes.
3. Choose an extraction mode: `single-skill`, `multi-skill`, `orchestrator-plus-children`, `alignment-check`, or `resync-after-playbook-change`.
4. If the user did not clearly ask to modify files, report assessment and extraction strategy only.
5. If the playbook is large or contains independent workflows, create an extraction map before editing skills.
6. Create or update only the needed `agent-skills/<skill-name>/SKILL.md` files.
7. Keep each skill concise, imperative, executable, and scoped to its trigger.
8. Update `agent-playbooks/README.md` and `agent-skills/README.md` when mappings, descriptions, or statuses change.
9. Validate frontmatter, naming, scope, README status, and alignment with the source playbook.

## Extraction Modes

- `single-skill`: one stable playbook workflow becomes one `SKILL.md`.
- `multi-skill`: a large playbook with independent workflows is mapped before creating multiple skills.
- `orchestrator-plus-children`: a root skill handles phase detection, delegation, context control, and final output; child skills perform concrete actions.
- `alignment-check`: compare an existing playbook and skills without modifying files unless asked.
- `resync-after-playbook-change`: update mapped skills and README status after the playbook changed.

## Multi-skill Rules

- Do not compress a playbook into one large skill when it has multiple phases, different triggers, different output contracts, or different validation rules.
- Use a root/orchestrator skill when the workflow needs phase detection, child-skill delegation, context control, gating, or output integration.
- Extract a child skill only when it has its own trigger, responsibility, workflow, validation, output contract, and clear handoff.
- Use `shared` for a reusable skill that supports more than one workflow.
- Keep background context, design intent, standard prompts, and the extraction map in the playbook.
- Do not copy the full playbook into any skill.

## Extraction Map

Before multi-skill extraction, propose this table:

```md
### Extraction Map

| Playbook Section | Proposed Skill | Skill Type | Trigger | Responsibility | Keep In Playbook? |
| --- | --- | --- | --- | --- | --- |
| ... | ... | root / child / shared | ... | ... | yes / no / partial |
```

## Skill Rules

Each skill should keep:

- `name`
- `description`
- purpose
- trigger conditions
- workflow
- mandatory rules
- boundaries
- validation
- output format

Each skill should omit:

- long background stories
- design history
- one-off project context
- long examples
- unstable ideas
- full playbook text
- unnecessary README, references, assets, or scripts

## README Sync

- Use `draft` when only the playbook exists and it is not stable yet.
- Use `skill-extracted` when one or more skills exist but the full playbook/root/child set has not been reviewed as synchronized.
- Use `aligned` only after the playbook and all mapped root, child, and shared skills are reviewed and synchronized.
- Use `aligned-with-followups` when the playbook and mapped skills are reviewed and synchronized, remain usable, and the playbook only adds non-blocking proposed follow-up backlog that does not change current triggers, rules, output contracts, or the extraction map.
- Use `deprecated` when the playbook or skill is no longer recommended.
- For one-to-many mappings, list the root skill first and include child/shared skills in the README mapping or the playbook extraction map.
- If the playbook changed after extraction, downgrade `aligned` to `skill-extracted` until resync is complete.
- Do not downgrade to `skill-extracted` for a documented non-blocking follow-up backlog unless it requires unsynchronized skill behavior changes.

## Alignment Checks

Check that playbook and skills agree on:

- core intent
- trigger conditions
- workflow
- mandatory rules and boundaries
- output contract
- validation
- README mapping and status

## Validation

After edits:

1. Check that every `SKILL.md` has valid YAML frontmatter.
2. Check that each `name` matches its folder name.
3. Check that each `description` states concrete trigger scenarios.
4. Check that each skill is shorter and more command-oriented than the playbook.
5. Check one-to-many README mappings and status rules.
6. Run `quick_validate.py` when available.

## Output

When reporting results, include:

- Playbook Assessment
- Extraction Mode
- Extraction Strategy
- Extraction Map, when relevant
- Files changed
- README updates
- Validation result
- Open questions
