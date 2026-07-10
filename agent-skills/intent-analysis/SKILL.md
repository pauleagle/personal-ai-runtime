---
name: intent-analysis
description: Use to infer developer intent from diff, prompt, plan, commit, or PR context, including confidence, uncertainty, mismatch with spec, and risk notes.
---

# Intent Analysis

## Purpose

Infer what a change is trying to accomplish and where intent is uncertain, so impact analysis and JIT testing target the right behavior.

## Script-First Execution

Before inferring intent, collect deterministic evidence when local repo artifacts are available:

```sh
python agent-skills/diff-analysis/scripts/collect_git_diff_evidence.py --repo-root . --json
python agent-skills/impact-analysis/scripts/collect_impact_evidence.py --repo-root . --json
```

Use commit messages, PR text, user prompts, specs, and atomic item metadata as stated evidence when available. Use LLM judgement only to infer the likely intent, confidence, contradictions, spec alignment, and behavior drift risk. Do not ask the LLM to rediscover changed files, path categories, or git status when the local helpers can collect them.

Run the helper from Windows PowerShell or a POSIX shell (Linux/macOS) with the same command shape; use `python3` when `python` is unavailable.

## Prompt Contract

Stable prefix:

- Skill: `intent-analysis`
- Execution Profile: `heavy-llm`
- Reusable Rules: treat intent as inference, not fact, unless explicitly stated by the user or spec; always state confidence and uncertainty; do not expand scope based on guessed intent; report spec conflicts instead of silently accepting them.
- Scope / Governance Defaults: read-only (no file edits); do not decide correctness alone; do not generate tests without impact context.
- Output Contract: see the Intent Analysis Report template under `## Output`.

Dynamic run packet:

- User Request:
- Deterministic Evidence:
- Relevant Files Or Artifacts:
- Current Assumptions Or Gaps:
- Requested Judgement Or Transformation:

## Workflow

1. Run deterministic diff and impact evidence checks when local repo artifacts are available; if not, state the fallback evidence source.
2. Read the user request, plan, spec refs, atomic item, commit message or PR context, and diff summary.
3. State the most likely intended change.
4. Identify evidence supporting that intent.
5. Identify uncertainty, contradictions, or missing context.
6. Compare inferred intent with spec and acceptance criteria.
7. Flag possible intent/spec mismatch or behavior drift.
8. Hand off impacted areas to `impact-analysis` or decision ambiguity to `decision-proposal`.

## Mandatory Rules

- Treat intent as an inference, not a fact, unless explicitly stated by the user or spec.
- Include confidence level and uncertainty.
- Do not expand scope based on guessed intent.
- If intent conflicts with spec, report the conflict instead of accepting it silently.

## Boundaries

- Do not modify files.
- Do not decide correctness alone.
- Do not generate tests without impact context.

## Validation

Check:

1. Intent statement is explicit.
2. Evidence is listed.
3. Confidence is stated.
4. Uncertainty is stated.
5. Spec mismatch is reported when present.

## Output

Use this report template:

```md
### Intent Analysis Report

- Inferred Intent:
- Evidence:
- Confidence: high | medium | low
- Uncertainty:
- Spec Alignment:
- Behavior Drift Risk:
- Next Analysis Step:
```
