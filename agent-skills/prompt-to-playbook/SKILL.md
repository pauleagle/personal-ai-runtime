---
name: prompt-to-playbook
description: Convert one-off prompts, successful examples, repeated task instructions, or conversation-tested workflows into human-readable agent playbooks. Use when the user asks to turn a prompt into a playbook, generalize a successful prompt, create an agent-playbooks markdown file from repeated instructions, or update playbook README mappings without automatically extracting a normal task skill.
---

# Prompt To Playbook

## Purpose

Turn a one-off prompt, successful case, or repeated task instruction into a reusable `agent-playbooks/name.md` playbook while stopping at the playbook layer unless the user explicitly asks for a normal task skill.

## Script-First Execution

Before creating or updating a local playbook file, inspect deterministic repository facts for the request:

```powershell
python agent-skills/prompt-to-playbook/scripts/inspect_playbook_request.py --repo-root . --target-playbook agent-playbooks/name.md --json
```

If the source prompt or example is a local file, include it:

```powershell
python agent-skills/prompt-to-playbook/scripts/inspect_playbook_request.py --repo-root . --source path/to/prompt.md --target-playbook agent-playbooks/name.md --json
```

Use the same Python commands on Linux/macOS shells. The helper checks source file evidence, target playbook path safety, `agent-playbooks/README.md` mapping presence, mapped skills, status values, and whether updating a mapped aligned playbook requires `skill-extracted` status until resync. Use LLM judgement after this evidence to decide whether the prompt is reusable, how to generalize it, and what content belongs in the playbook.

## Workflow

1. Run the script-first request inspection when the target playbook is local; if the helper is unavailable or the request is not local-file based, state the fallback.
2. Read the source prompt, successful example, or repeated instruction.
3. Read `agent-playbooks/README.md` and `agent-skills/README.md` when updating repository files.
4. Determine whether the user wants analysis only, a new playbook, an existing playbook update, or a merge of several prompts.
5. Identify the recurring problem, reusable principles, trigger conditions, exclusions, agent rules, and useful output format.
6. Remove or generalize one-off names, dates, paths, environment details, and assumptions.
7. Create or update the target file under `agent-playbooks/` using the repository playbook structure.
8. Do not create a normal task skill unless the user explicitly asks for skill extraction.
9. If a new playbook is not listed in `agent-playbooks/README.md`, add a row with Skill `-` and Status `draft`.
10. If an existing playbook with a mapped skill is changed, set its Status to `skill-extracted` until the playbook and skill are reviewed again.
11. Update `agent-skills/README.md` only for this `prompt-to-playbook` skill or if the user explicitly asks for a skill inventory change.

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
