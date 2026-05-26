---
name: intent-analysis
description: Use to infer developer intent from diff, prompt, plan, commit, or PR context, including confidence, uncertainty, mismatch with spec, and risk notes.
---

# Intent Analysis

## Purpose

Infer what a change is trying to accomplish and where intent is uncertain, so impact analysis and JIT testing target the right behavior.

## Workflow

1. Read the user request, plan, spec refs, atomic item, commit message or PR context, and diff summary.
2. State the most likely intended change.
3. Identify evidence supporting that intent.
4. Identify uncertainty, contradictions, or missing context.
5. Compare inferred intent with spec and acceptance criteria.
6. Flag possible intent/spec mismatch or behavior drift.
7. Hand off impacted areas to `impact-analysis` or decision ambiguity to `decision-proposal`.

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

Report:

- inferred intent
- evidence
- confidence
- uncertainty
- spec alignment
- behavior drift risk
- next analysis step
