---
name: context-pack-builder
description: Use to prepare bounded context packs for stateless subagents, selecting only required specs, diffs, artifacts, constraints, allowed scope, forbidden scope, validation requirements, and output contracts.
---

# Context Pack Builder

## Purpose

Create minimal but sufficient context packs so subagents can run one bounded job without inheriting long chat history or stale artifacts.

## Workflow

1. Read the selected job, atomic item metadata, spec refs, dependency notes, allowed scope, forbidden scope, and output contract.
2. Identify required source files, artifacts, tests, diffs, prior findings, and human decisions.
3. Exclude unrelated history, obsolete drafts, closed objections, and out-of-scope files.
4. Summarize prior findings only as durable references or compact handoff notes.
5. Record included and excluded sources.
6. Note token budget, stale artifacts, missing sources, and assumptions.
7. Hand the context pack to `atomic-subagent-runner` or the root orchestrator.

## Mandatory Rules

- Include enough context to execute the job, but not the whole long conversation.
- Do not include private or unrelated context unless explicitly required and allowed.
- Stale or missing artifacts must be called out.
- The context pack must state allowed scope and forbidden scope.
- The output contract must be explicit.

## Boundaries

- Do not execute the job.
- Do not modify project files except a requested context-pack artifact.
- Do not resolve ambiguity by padding the pack with everything.

## Validation

Check:

1. Job ID and atomic item ID are present.
2. Spec refs are present.
3. Included/excluded source list is present.
4. Allowed and forbidden scopes are explicit.
5. Validation requirements are explicit.
6. Missing or stale context is reported.

## Output

Report:

- context pack manifest
- included sources
- excluded sources
- compact prior findings
- allowed scope
- forbidden scope
- validation requirements
- output contract
- stale or missing artifact warnings
