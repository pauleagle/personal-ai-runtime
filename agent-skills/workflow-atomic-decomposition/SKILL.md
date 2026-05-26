---
name: workflow-atomic-decomposition
description: Use when a revised spec is ready to split into selected workflow slices, atomic implementation items, bootstrap prerequisites, dependency edges, verification loops, and traceable work items.
---

# Workflow Atomic Decomposition

## Purpose

Split a revised spec into implementation-sized atomic items that can be independently executed, tested, reviewed, committed, and advanced through the spec-driven workflow.

## Workflow

1. Read the revised spec, accepted scope, non-goals, Devil's Advocate gate result, and open questions.
2. Confirm the gate is `pass`; if not, stop and report blockers.
3. Identify main workflow candidates and ask for or infer the selected workflow when safe.
4. Identify candidate workflow slices, then split the selected workflow into atomic items based on behavior, contract, validation boundary, and dependency edges.
5. Add bootstrap prerequisite items such as `P0-00` when scaffolding is required before behavior work.
6. Include replacement, compatibility, and migration items when the spec changes existing behavior.
7. For each item, define ID, title, status, spec refs, allowed scope, forbidden scope, dependencies, validation, mutation expectation, and completion criteria.
8. Classify decomposition gaps and state whether the workflow can continue or must return to spec clarification.
9. Keep backlog, deferred, proposed, and accepted items separate.
10. Hand off item metadata to `orchestrator-state-machine`.

## Mandatory Rules

- Atomic items describe verifiable behavior or contracts, not just file lists.
- One item should be small enough to implement, test, review, and commit alone.
- Dependency edges must be explicit.
- Every item needs spec refs and validation hooks.
- Replacement, migration, and compatibility work must become explicit items when behavior changes.
- Do not enter implementation while decomposition blockers remain.

## Boundaries

- Do not implement the items in this skill.
- Do not turn future ideas into accepted work without human approval.
- Do not rely on chat order as dependency metadata.

## Validation

Check:

1. Selected workflow is clear.
2. Every atomic item has spec refs.
3. Dependencies are explicit.
4. Validation is defined.
5. Open questions or gaps are listed.
6. Gap/no-gap continuation decision is explicit.
7. Items can support commit-then-advance.

## Output

Report:

- main workflow map
- candidate workflow slices
- selected workflow
- atomic items
- dependency graph
- bootstrap prerequisite items
- replacement, compatibility, or migration items
- deferred items
- gap classification
- gap/no-gap continuation decision
- next orchestrator state patch
