# SK-FU-002 Normalize Prompt and Context Templates for LLM Execution Profiles

## Metadata

- Type: Skill Follow-up
- ID: SK-FU-002
- Status: Draft
- Source Request: Backlog request to normalize and template prompts and context for `hybrid`, `low-llm`, and `heavy-llm` execution profiles.
- Suggested Location: `backlog/SK-FU-002-normalize-prompt-context-templates-for-llm-execution-profiles.md`
- Scope:
  - `agent-skills/README.md`
  - `agent-skills/*/SKILL.md`
  - `agent-playbooks/*`
  - future shared prompt and context template artifacts
- Principle: Normalize prompt and context contracts before expanding LLM reasoning.
- Integration Status: Not integrated
- Status Impact: No current README status change; this is a non-blocking cross-skill maintenance follow-up.

---

## Summary

Add shared prompt and context templates for skills whose execution profile is `hybrid`, `low-llm`, or `heavy-llm`.

The goal is to reduce ad hoc prompting, oversized context packs, and inconsistent output contracts. Deterministic evidence should still be collected first under SK-FU-001, but once LLM judgement is needed, the LLM-facing prompt and context should be as normalized, bounded, and reusable as practical.

---

## Background

`agent-skills/README.md` currently defines execution profiles:

- `script`: deterministic commands, parsers, validators, or status checks do most of the work.
- `hybrid`: deterministic discovery first, then LLM judgement for interpretation, synthesis, or scoped decisions.
- `low-llm`: mostly structured text transformation or cleanup with limited judgement after facts are collected.
- `heavy-llm`: semantic reasoning, design, review, decomposition, or decision framing is the core value.

SK-FU-001 focuses on minimizing avoidable LLM work through script-first execution. This follow-up focuses on the remaining LLM work: when LLM reasoning is required, prompts and context should follow stable templates rather than being rebuilt from scratch every time.

---

## Problem

Current skill execution can still vary too much after deterministic evidence is collected:

- Context packs may include different levels of detail for similar tasks.
- Prompts may omit scope boundaries, output contracts, or uncertainty handling.
- `hybrid` skills may mix raw evidence and interpretation in inconsistent ways.
- `low-llm` skills may overuse free-form judgement for structured cleanup work.
- `heavy-llm` skills may receive broad context without a clear reasoning frame or decision contract.
- Subagent handoffs may become harder to compare because each run uses a different prompt shape.

This makes execution harder to audit, repeat, test, and improve.

---

## Objective

Define shared prompt and context template guidance for `hybrid`, `low-llm`, and `heavy-llm` skills.

The templates should make each LLM step explicit about:

- task objective,
- execution profile,
- deterministic evidence already collected,
- relevant context sources,
- allowed scope,
- forbidden scope,
- assumptions,
- uncertainty handling,
- required output format,
- validation or closeout expectations,
- and traceability back to files, specs, tests, or prior decisions.

---

## Target Profiles

### `hybrid`

Use a prompt template that separates:

- deterministic facts,
- inferred risks or gaps,
- judgement requested from the LLM,
- decisions that must remain with the user,
- and validation evidence required before closeout.

The LLM should not rediscover file, diff, status, test, or validator facts that were already collected by command output.

### `low-llm`

Use a compact transformation template that includes:

- input text or artifact path,
- target style or schema,
- preservation rules,
- allowed edits,
- forbidden edits,
- output format,
- and verification checklist.

The LLM should focus on bounded normalization, cleanup, classification, or formatting rather than open-ended reasoning.

### `heavy-llm`

Use a reasoning template that includes:

- problem statement,
- accepted facts,
- relevant constraints,
- competing options,
- risk categories,
- decision gates,
- uncertainty budget,
- and required structured output.

The LLM should reason deeply, but still from a bounded context pack with explicit evidence and traceability.

---

## Proposed Template Layers

### 1. Context Contract

Each LLM-bound context pack should declare:

```md
## Context Contract

- Task:
- Execution Profile:
- Skill:
- Required Inputs:
- Deterministic Evidence:
- Relevant Files:
- Relevant Specs or Playbooks:
- Prior Decisions:
- Allowed Scope:
- Forbidden Scope:
- Known Gaps:
- Token / Context Priority:
```

### 2. Prompt Contract

Each LLM prompt should declare:

```md
## Prompt Contract

- Objective:
- Use Evidence As Facts:
- Do Not Re-derive:
- Reasoning Scope:
- Required Output:
- Uncertainty Handling:
- Human Decision Required When:
- Validation / Closeout:
```

### 3. Output Contract

Each LLM result should declare:

```md
## Output Contract

- Summary:
- Findings:
- Decisions:
- Assumptions:
- Risks:
- Validation Evidence:
- Follow-ups:
- Blockers:
```

The exact output shape can remain Markdown unless a specific workflow requires JSON.

---

## Candidate Template Artifacts

Possible implementation paths:

- Add a shared "Prompt and Context Templates" section to `agent-skills/README.md`.
- Add reusable template files under a shared skill-maintenance location, if the repo adopts one.
- Add profile-specific snippets to selected `SKILL.md` files only when they materially change execution behavior.
- Extend context-pack-builder guidance so it can produce profile-aware context contracts.
- Extend atomic-subagent-runner guidance so subagent jobs include profile-aware prompt contracts.

Suggested template names:

- `hybrid-context-contract.md`
- `hybrid-prompt-contract.md`
- `low-llm-transformation-contract.md`
- `heavy-llm-reasoning-contract.md`
- `llm-output-contract.md`

---

## Non-goals

This follow-up should not:

- Replace SK-FU-001 script-first minimization.
- Force every skill to use the same exact prompt.
- Add large prompt frameworks that make small tasks heavier.
- Require hidden chain-of-thought capture or expose private reasoning.
- Make `script` profile skills LLM-heavy.
- Change current skill triggers, README status values, or playbook mappings in the backlog step.
- Treat templates as mandatory when a tiny direct answer is sufficient.

---

## Suggested Implementation Steps

1. Review current `hybrid`, `low-llm`, and `heavy-llm` skills in `agent-skills/README.md`.
2. Identify repeated LLM input patterns across those skills.
3. Draft shared context, prompt, and output contract snippets.
4. Decide where shared templates should live.
5. Update only high-impact skills first:
   - `context-pack-builder`
   - `atomic-subagent-runner`
   - `spec-driven-change-verification`
   - `spec-drill-down`
   - `spec-definition`
   - `workflow-atomic-decomposition`
   - `decision-proposal`
   - `prompt-to-playbook`
   - `playbook-to-skill`
6. Add lightweight examples showing how a script-first evidence block becomes an LLM prompt contract.
7. Verify the templates do not increase context size for low-complexity tasks.

---

## Acceptance Criteria

This follow-up is complete when:

- [ ] Shared template guidance exists for `hybrid`, `low-llm`, and `heavy-llm` profiles.
- [ ] The guidance clearly separates deterministic evidence from LLM judgement.
- [ ] At least one context contract template exists.
- [ ] At least one prompt contract template exists.
- [ ] At least one output contract template exists.
- [ ] `low-llm` guidance stays compact and transformation-oriented.
- [ ] `heavy-llm` guidance supports deeper reasoning without unbounded context dumps.
- [ ] Subagent-oriented skills can reuse the same contract shape for handoffs.
- [ ] The update does not require current `script` profile skills to add LLM prompts.
- [ ] The update does not silently change skill triggers, README status values, or playbook mappings.

---

## Review Notes

This backlog item is intentionally paired with SK-FU-001.

SK-FU-001 asks:

> Can deterministic execution reduce the amount of LLM work?

SK-FU-002 asks:

> Once LLM work remains necessary, can its prompt, context, and output shape be made repeatable?

The desired outcome is not more prompting. The desired outcome is less improvisation around the prompting that is genuinely needed.

---

## Recommended Commit Message

```text
docs(backlog): add SK-FU-002 prompt context template follow-up
```
