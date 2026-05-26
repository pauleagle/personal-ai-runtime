---
name: atomic-subagent-runner
description: Use to launch, supervise, or evaluate one stateless bounded subagent job with a context pack, allowed scope, forbidden scope, validation requirements, structured output contract, and state patch proposal.
---

# Atomic Subagent Runner

## Purpose

Run one short-lived bounded job and return a structured result that can be validated and merged by the orchestrator.

## Workflow

1. Read the context pack, job ID, parent atomic item ID, allowed scope, forbidden scope, validation requirements, and output contract.
2. Confirm the job is small enough for one bounded worker.
3. Execute only the requested analysis, patch, test, review, or summary task.
4. Reject or stop when required context is missing, scope is unsafe, or the task would require hidden chat history.
5. Produce structured output with consumed artifacts, produced artifacts, validation result, gaps, and state patch proposal.
6. Do not advance durable state directly unless this job is explicitly the single writer for that state artifact.
7. Return retry, blocked, or human decision required when appropriate.

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

Report:

- job result
- consumed artifacts
- produced artifacts
- validation result
- state patch proposal
- unresolved gaps
- retry or blocked note
- human decision required
