---
name: decision-proposal
description: Use to turn ambiguity, validation gaps, breaking changes, survived mutations, or spec/test conflicts into human-readable decision options such as accept, update spec, reject, refine tests, or defer.
---

# Decision Proposal

## Purpose

Prepare human governance decisions without letting the agent silently redefine correctness.

## Workflow

1. Read spec refs, impact analysis, test effectiveness evaluation, mutation result, risks, open questions, and current workflow state.
2. Identify the decision needed and why it cannot be resolved mechanically.
3. Present clear options such as accept change, update spec, reject change, refine tests, fix implementation, defer, or accept risk.
4. For each option, list consequences, validation impact, spec/test updates, and risk.
5. Recommend one option only when evidence supports it.
6. Record required durable-state updates after the human decision.
7. Hand accepted decisions to `spec-test-evolution` or the root orchestrator.

## Mandatory Rules

- Humans decide correctness ambiguity, breaking behavior, accepted risk, and spec evolution.
- Do not bury the decision in a long narrative.
- Do not present only one option when meaningful alternatives exist.
- Label recommendation separately from facts.
- Include the cost of doing nothing when relevant.

## Boundaries

- Do not implement the selected option before the human decides.
- Do not mark workflow complete while a decision is pending.
- Do not treat absent user response as approval.

## Validation

Check:

1. Decision question is explicit.
2. Options are mutually understandable.
3. Tradeoffs and risks are listed.
4. Recommendation is labeled.
5. Required follow-up state/spec/test updates are clear.

## Output

Report:

- decision needed
- evidence
- options
- recommendation
- risks
- required updates
- blocked workflow step
- human response needed
