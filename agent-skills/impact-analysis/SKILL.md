---
name: impact-analysis
description: Use to identify impacted components, specs, tests, contracts, risks, and validation gaps from diff, inferred intent, test results, or mutation results.
---

# Impact Analysis

## Purpose

Determine what a change can affect and classify verification gaps so testing, mutation, and human decisions stay focused.

## Workflow

1. Read diff analysis, intent analysis, spec refs, dependency notes, test map, and known risk items.
2. Identify impacted components, APIs, data contracts, workflows, specs, tests, and documentation.
3. Classify risks as code issue, test gap, spec gap, behavior drift, compatibility gap, migration gap, or human decision required.
4. Estimate impact confidence and blast radius.
5. Recommend focused tests, JIT tests, mutation targets, or spec updates.
6. Identify earliest workflow step to rerun when a gap requires rollback.
7. Hand off to JIT test generation, mutation testing, test effectiveness evaluation, or decision proposal.

## Mandatory Rules

- Impact must trace to diff, intent, spec, tests, or known dependency.
- Do not escalate every change to full-scope testing by default.
- Do not hide spec gaps as test gaps.
- Distinguish low-confidence impact from confirmed impact.
- If human governance is needed, say so directly.

## Boundaries

- Do not implement fixes.
- Do not run tests unless asked.
- Do not accept breaking changes without human decision.

## Validation

Check:

1. Impacted specs and tests are named when known.
2. Risk categories are explicit.
3. Confidence is stated.
4. Focused validation recommendations are present.
5. Human decision needs are flagged.

## Output

Report:

- impacted components
- impacted specs
- impacted tests
- risk classification
- impact confidence
- focused validation recommendation
- rerun point
- human decision needed
