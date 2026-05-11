---
name: prompt-to-playbook
description: Convert one-off prompts, successful examples, repeated task instructions, or conversation-tested workflows into human-readable agent playbooks. Use when the user asks to turn a prompt into a playbook, generalize a successful prompt, create an agent-playbooks markdown file from repeated instructions, or update playbook README mappings without automatically extracting a normal task skill.
---

# Prompt To Playbook

## Purpose

Turn a one-off prompt, successful case, or repeated task instruction into a reusable `agent-playbooks/name.md` playbook while stopping at the playbook layer unless the user explicitly asks for a normal task skill.

## Workflow

1. Read the source prompt, successful example, or repeated instruction.
2. Read `agent-playbooks/README.md` and `agent-skills/README.md` when updating repository files.
3. Determine whether the user wants analysis only, a new playbook, an existing playbook update, or a merge of several prompts.
4. Identify the recurring problem, reusable principles, trigger conditions, exclusions, agent rules, and useful output format.
5. Remove or generalize one-off names, dates, paths, environment details, and assumptions.
6. Create or update the target file under `agent-playbooks/` using the repository playbook structure.
7. Do not create a normal task skill unless the user explicitly asks for skill extraction.
8. If a new playbook is not listed in `agent-playbooks/README.md`, add a row with Skill `-` and Status `draft`.
9. If an existing playbook with a mapped skill is changed, set its Status to `skill-extracted` until the playbook and skill are reviewed again.
10. Update `agent-skills/README.md` only for this `prompt-to-playbook` skill or if the user explicitly asks for a skill inventory change.

## Playbook Rules

- Preserve the prompt's reusable intent, not its single-use wording.
- Keep human-facing purpose, principles, applicability, standard prompt, and output format in the playbook.
- Add `適用時機` and `不適用時機` to prevent overuse.
- Add `Agent 行為規則` for required checks, guardrails, and confirmation points.
- Keep the standard prompt copyable and practical.
- Avoid project-specific or date-specific wording unless it is explicitly part of the reusable workflow.
- Mark unclear or immature playbooks as `draft` in `agent-playbooks/README.md`.
- Downgrade an existing mapped playbook from `aligned` to `skill-extracted` after changing the playbook without reviewing and syncing the skill.

## Boundaries

- Do not automatically extract the resulting playbook into a general task skill.
- Do not create per-skill README files, scripts, references, assets, or `agents/openai.yaml` unless separately requested.
- Do not invent stable process rules from a prompt that is too vague; report gaps instead.
- Do not preserve sensitive or one-off context as reusable guidance.

## Validation

After creating or updating files:

1. Check that the playbook follows `agent-playbooks/README.md`.
2. Check that the playbook is generalized beyond the source prompt.
3. Check that README tables are consistent when changed.
4. Run `quick_validate.py` for this skill when the skill itself is created or edited.

## Output

When reporting results, include:

- Files changed
- New or updated playbook
- New or updated skill, if any
- README updates
- Validation result
