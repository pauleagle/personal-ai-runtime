---
name: context-pack-builder
description: Use to prepare bounded context packs for stateless subagents, selecting only required specs, diffs, artifacts, constraints, allowed scope, forbidden scope, validation requirements, and output contracts.
---

# Context Pack Builder

## Purpose

Create minimal but sufficient context packs so subagents can run one bounded job without inheriting long chat history or stale artifacts.

## Script-First Execution

After selecting candidate sources, build deterministic source metadata before handing the pack to a subagent:

```sh
python agent-skills/context-pack-builder/scripts/build_context_manifest.py --repo-root . --json <source> [<source> ...]
```

The helper checks file existence, source kind, relative path, byte size, line count, SHA-256, missing sources, directories, outside-repo paths, and per-file size warnings. Use this as the manifest evidence layer; use LLM judgement to decide inclusion rationale, exclusions, compact prior findings, allowed scope, forbidden scope, validation requirements, and output contract.

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

## Prompt / Handoff Contract

When building a context pack for a subagent, use the shared stable-prefix / dynamic-run-packet shape from `agent-skills/README.md`. Treat this as a handoff recommendation, not a new file format or schema requirement.

Stable prefix:

- Skill: `context-pack-builder`
- Execution Profile: `hybrid`
- Reusable Rules: subagents are stateless, scope must be bounded, and missing or stale artifacts must be explicit.
- Scope / Governance Defaults: allowed scope, forbidden scope, validation requirements, output contract, and human-decision boundaries.
- Output Contract: included sources, excluded sources, compact prior findings, stale or missing artifact warnings, and next recipient.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

Keep source snippets and command output in the dynamic run packet after the stable prefix so repeated handoff instructions remain cache-friendly.

## Workflow

1. Read the selected job, atomic item metadata, spec refs, dependency notes, allowed scope, forbidden scope, and output contract.
2. Identify required source files, artifacts, tests, diffs, prior findings, and human decisions.
3. Run deterministic manifest building for selected source paths when available.
4. Exclude unrelated history, obsolete drafts, closed objections, and out-of-scope files.
5. Summarize prior findings only as durable references or compact handoff notes.
6. Record included and excluded sources.
7. Note token budget, stale artifacts, missing sources, and assumptions.
8. Hand the context pack to `atomic-subagent-runner` or the root orchestrator.

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
7. If the manifest helper changed, run its unit tests and a CLI smoke check.

## Output

Use this report template:

```md
### Context Pack Report

- context pack manifest:
- stable prefix / dynamic run packet, when handing off to a subagent:
- included sources:
- excluded sources:
- compact prior findings:
- allowed scope:
- forbidden scope:
- validation requirements:
- output contract:
- stale or missing artifact warnings:
```
