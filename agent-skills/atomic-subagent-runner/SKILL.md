---
name: atomic-subagent-runner
description: Use to launch, supervise, or evaluate one stateless bounded subagent job with a context pack, allowed scope, forbidden scope, validation requirements, structured output contract, and state patch proposal.
---

# Atomic Subagent Runner

## Purpose

Run one short-lived bounded job and return a structured result that can be validated and merged by the orchestrator.

## Script-First Execution

When the subagent job is represented as a local JSON contract, validate the contract before launching or evaluating the worker:

```sh
python agent-skills/atomic-subagent-runner/scripts/validate_subagent_job_contract.py path/to/job.json --json
```

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

The helper checks required fields, non-empty context and validation fields, allowed/forbidden scope shape, likely hidden chat-history dependency, and whether state patch or merge gate governance is declared. Use LLM judgement after this deterministic check to decide whether the job is small enough, semantically safe, and ready to run.

## Prompt / Handoff Contract

When a context pack includes a stable prefix plus dynamic run packet, preserve that shape as the subagent handoff contract. Treat `prompt_contract` as recommended prose or artifact structure for this follow-up pass; do not require a new JSON field or validator rule.

Stable prefix:

- Skill:
- Execution Profile:
- Reusable Rules:
- Scope / Governance Defaults:
- Output Contract:
- Validation / Closeout Defaults:

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

Use the stable prefix as fixed execution instructions and the dynamic packet as run-specific evidence. Do not rely on hidden chat history to fill either section.

## Workflow

1. Run the script-first job contract validation when a local JSON job contract exists; if the helper is unavailable or the contract is not local JSON, state the fallback.
2. Read the context pack, job ID, parent atomic item ID, allowed scope, forbidden scope, validation requirements, and output contract.
3. Confirm the job is small enough for one bounded worker.
4. Execute only the requested analysis, patch, test, review, or summary task.
5. Reject or stop when required context is missing, scope is unsafe, or the task would require hidden chat history.
6. Produce structured output with consumed artifacts, produced artifacts, validation result, gaps, and state patch proposal.
7. Do not advance durable state directly unless this job is explicitly the single writer for that state artifact.
8. Return retry, blocked, or human decision required when appropriate.

## Mandatory Rules

- Subagents are stateless and bounded.
- Do not use previous chat context as an implicit input.
- Stay inside allowed scope.
- Respect forbidden scope.
- Output must be parseable and reviewable.
- Failed or partial jobs are not completed jobs.

## Boundaries

- Do not act as the root orchestrator.
- Do not dispatch additional subagents unless explicitly asked.
- Do not merge state without an explicit merge gate or writer permission.

## Validation

Check:

1. Job ID and parent atomic item ID are present.
2. Consumed and produced artifacts are listed.
3. Validation command or review result is included.
4. State patch proposal is explicit or intentionally absent.
5. Retry/block/human-decision status is clear.

## Output

Use this report template:

```md
### Subagent Job Report

- job result:
- consumed stable prefix / dynamic run packet, when provided:
- consumed artifacts:
- produced artifacts:
- validation result:
- state patch proposal:
- unresolved gaps:
- retry or blocked note:
- human decision required:
```
