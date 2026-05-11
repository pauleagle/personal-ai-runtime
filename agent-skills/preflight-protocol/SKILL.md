---
name: preflight-protocol
description: Run a brief preflight before complex, ambiguous, risky, multi-step, architecture, migration, refactor, or behavior-changing work; clarify understanding, assumptions, uncertainty, risks, and next steps before modifying files.
---

# Preflight Protocol

## Purpose

Before starting non-trivial work, perform a short preflight check.

Use this skill to reduce repeated mistakes, hidden assumptions, wrong implementation direction, and premature coding while still moving the task forward.

## When to use

Use this skill when the task involves any of the following:

- Architecture design
- Non-trivial code implementation
- Refactoring
- Migration
- Documentation restructuring
- Release preparation
- Cross-project changes
- Agent workflow design
- Tasks with unclear requirements
- Tasks with multiple possible interpretations
- Tasks that may affect existing behavior
- Changes touching multiple files, data formats, public APIs, or user-visible behavior

## When not to use

Do not use this skill for very small, low-risk tasks, such as:

- Simple translation
- Simple wording polish
- One-line explanation
- Small factual answer
- Trivial formatting change

## Discovery before preflight

Before outputting the preflight, read or search files when needed to understand the task. Keep this discovery read-only.

Do not modify files, run destructive commands, make architecture decisions, or start implementation before the preflight.

## Required preflight output

Before doing the actual task, output a concise preflight with the following sections.

### 1. Task understanding

Summarize what the agent believes the user is asking for.

### 2. Known inputs / constraints

List the known inputs, constraints, user-provided requirements, relevant files, and any limits on tools, formats, encoding, or scope.

### 3. Assumptions

List the assumptions the agent is making.

### 4. Uncertainties

List anything unclear, missing, or not yet confirmed. If none are identified, say so.

### 5. Alternative interpretations

List any possible alternative meanings of the request. If none are identified, say so.

### 6. Risks

List possible risks, such as breaking existing behavior, overwriting user changes, changing conventions, choosing the wrong abstraction, missing backward compatibility requirements, or relying on tests that may be unavailable or expensive.

### 7. Next steps

State the planned next steps before execution.

### 8. Files likely to be touched

List files or areas that are likely to be read or modified. If no files are expected to be modified, say so.

## Execution rules

- Keep the preflight brief. Use the full template for high-risk or highly ambiguous tasks.
- For medium-risk tasks, use a compact preflight with only the meaningful bullets.
- Do not ask for confirmation when a reasonable, low-risk assumption is available.
- Ask the user only when an uncertainty materially changes the outcome or makes execution unsafe.
- After the preflight, continue executing the task unless there is a blocking uncertainty.

## Output template

```md
## Preflight

### Task understanding

- ...

### Known inputs / constraints

- ...

### Assumptions

- ...

### Uncertainties

- ...

### Alternative interpretations

- ...

### Risks

- ...

### Next steps

- ...

### Files likely to be touched

- ...
```
