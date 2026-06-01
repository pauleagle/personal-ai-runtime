---
name: orchestrator-state-machine
description: Use to maintain durable workflow state for spec-driven execution, including workflow_step, atomic item status, dependency graph, ready/running/blocked/completed queues, merge gates, usage gates, and commit checkpoints.
---

# Orchestrator State Machine

## Purpose

Keep long-running spec-driven work in durable artifacts rather than chat context, and decide which bounded job can run next.

## Script-First Execution

Before semantic state decisions, validate durable state artifacts when they are JSON:

```powershell
python agent-skills\orchestrator-state-machine\scripts\validate_orchestrator_state.py <state-file> --json
```

The helper checks required cursor/status fields and queue shapes. It does not decide which job should run next; use LLM judgement after validation for dependency, usage, validation, human decision, and merge gates.

## Workflow

1. Read the root spec, atomic item index, current state artifact, dependency graph, git status, validation results, and human decision status.
2. Identify the current `workflow_step` as the next step to execute or currently executing.
3. Build or update ready, running, blocked, completed, and deferred queues.
4. Apply dependency, usage, validation, human decision, and merge gates.
5. Select the next job only when its prerequisites and allowed scope are clear.
6. After successful completion, write a state patch that advances `workflow_step`, atomic item status, validation status, and checkpoint metadata.
7. If a step blocks or fails, keep or rewind the cursor to the earliest rerun point.
8. Produce a handoff or resume note.

## Mandatory Rules

- `workflow_step` is a live progress cursor, not a static history label.
- Subagent output does not count as progress until merged into durable state.
- Writer jobs require single-writer scope or an explicit merge gate.
- Human decisions block state advancement until recorded.
- Commit checkpoints should align with completed atomic items when the workflow uses commit-then-advance.
- Do not mark partial or failed jobs completed.

## Boundaries

- Do not implement project changes here unless state artifacts themselves are the target.
- Do not infer completed work from chat memory alone.
- Do not run parallel jobs when dependency or merge policy is unclear.

## Validation

Check:

1. State artifact and spec refs exist or gaps are reported.
2. Cursor meaning is clear.
3. Ready and blocked reasons are explicit.
4. State patch is traceable to job ID and atomic item ID.
5. Validation and human decision status are included.

## Output

Report:

- current state
- workflow_step
- ready queue
- blocked queue and reasons
- selected next job
- state patch proposal or history
- checkpoint status
- resume note
