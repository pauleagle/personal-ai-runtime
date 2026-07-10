---
name: spec-definition
description: Use to create, revise, or normalize a formal correctness spec from clarified requirements, including scope, non-goals, rules, invariants, acceptance criteria, testing implications, and README/spec file placement.
---

# Spec Definition

## Purpose

Create or update the formal correctness contract that implementation, tests, JIT tests, mutation evaluation, and human decisions must trace back to.

## Script-First Execution

Before drafting, establish deterministic facts with file reads and targeted `rg`: existing `SPEC.md` / `specs/` files, README entry points, index files, and open-question lists; verify every path the spec will reference actually exists.

Use LLM judgement only for the correctness contract content itself.

## Prompt Contract

Stable prefix:

- Skill: `spec-definition`
- Execution Profile: `heavy-llm`
- Reusable Rules: spec is the correctness source, not chat; when README and spec conflict, the spec is authoritative; backlog is not accepted correctness unless promoted and indexed; do not bury ambiguous behavior in prose — mark it as an open question or human decision.
- Scope / Governance Defaults: no implementation while drafting unless explicitly asked and scope is clear; no mutation or JIT test workflows here; do not mark the spec ready for atomic decomposition while blocking open questions remain.
- Output Contract: see the `### Spec Definition Report` template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

## Workflow

1. Read clarified requirements, existing README, existing spec files, open questions, and current project structure.
2. Decide where the spec belongs: existing `SPEC.md`, a split file under `specs/`, or a new formal spec file.
3. Define context, goal, scope, non-goals, inputs, outputs, business rules, invariants, error conditions, acceptance criteria, testing implications, and main workflow candidates.
4. Keep README as an entry point; move correctness contracts into spec files when they become detailed.
5. Separate accepted behavior from backlog, proposed, deferred, or rejected items.
6. Preserve traceability for follow-up items, parent IDs, root spec indexes, and local spec indexes when applicable.
7. Hand off to Devil's Advocate review or revised-spec integration.

## Mandatory Rules

- Spec is the correctness source; do not leave behavior contracts only in chat.
- If README and spec conflict, treat the spec as authoritative and update the stale summary when in scope.
- Backlog is not accepted correctness unless promoted and indexed.
- Follow-up items require parent traceability and root/local index updates when applicable.
- Do not bury ambiguous behavior in prose; mark it as an open question or human decision.

## Boundaries

- Do not implement code while drafting the spec unless explicitly asked and scope is clear.
- Do not run mutation or JIT test workflows here.
- Do not mark the spec ready for atomic decomposition while blocking open questions remain.

## Validation

Check that the spec includes:

1. Scope and non-goals.
2. Inputs and outputs.
3. Rules, invariants, and error conditions.
4. Acceptance criteria.
5. Testing implications.
6. Open questions and decision status.
7. Correct README/spec/index placement.

## Output

Use this report template:

```md
### Spec Definition Report

- Spec location:
- Sections created or updated:
- Accepted behavior:
- Open questions:
- Testing implications:
- Main workflow candidates:
- Index or README updates:
- Next gate:
```
