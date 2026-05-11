---
name: playbook-to-skill
description: Convert, extract, or align agent-playbooks into Codex skills. Use when the user asks to turn a playbook into a skill, extract SKILL.md from a playbook, align an existing skill with its playbook, update playbook/skill README tables, or keep agent-playbooks and agent-skills synchronized.
---

# Playbook To Skill

## Purpose

Turn a human-readable playbook in `agent-playbooks/` into a concise, command-oriented `agent-skills/<skill-name>/SKILL.md`, while keeping the playbook as the source for purpose, principles, context, and standard prompts.

## Workflow

1. Read the target playbook, `agent-playbooks/README.md`, and `agent-skills/README.md`.
2. Determine whether the user wants to update only the playbook, only the skill, both, or just check alignment.
3. Keep human-facing background, design intent, and standard prompts in the playbook.
4. Extract only execution-critical instructions into `SKILL.md`.
5. Create or update `agent-skills/<skill-name>/SKILL.md` using the same hyphen-case name as the playbook when possible.
6. Write frontmatter with only `name` and `description`.
7. Make the skill body concise, imperative, and execution-oriented.
8. Avoid adding per-skill README files, scripts, references, assets, or `agents/openai.yaml` unless they are clearly needed.
9. Update `agent-playbooks/README.md` and `agent-skills/README.md` when mappings or skill inventories change.
10. Run the skill validator when available.

## Extraction Rules

- Do not copy the playbook verbatim into the skill.
- Preserve the playbook's core intent, constraints, and safety rules.
- Put trigger scenarios in the skill `description`, not only in the body.
- Convert long explanations into short workflow steps or rules.
- Keep output templates only when they help the agent execute the workflow reliably.
- Keep background rationale, maintenance notes, and longer examples in the playbook.
- Do not invent behavior that is not supported by the playbook unless the user asks to extend it.

## README Sync

When a skill is created or updated from a playbook:

- Add or update the row in `agent-playbooks/README.md`.
- Use `draft` when only the playbook exists and it is not stable yet.
- Use `skill-extracted` when a skill has been extracted from the playbook.
- Use `aligned` only after the playbook and skill have been reviewed and confirmed synchronized.
- Use `deprecated` when the playbook or skill is no longer recommended.
- Add the skill to `agent-skills/README.md` if that README includes an inventory table or list.

## Validation

After creating or updating a skill:

1. Check that `SKILL.md` has valid YAML frontmatter.
2. Check that `name` matches the folder name.
3. Check that `description` clearly states when to use the skill.
4. Check that the body is shorter and more command-oriented than the playbook.
5. Run `quick_validate.py` if available.

## Output

When reporting results, include:

- Files changed
- Skill name and location
- README updates
- Validation result
