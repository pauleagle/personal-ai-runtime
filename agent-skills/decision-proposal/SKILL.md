---
name: decision-proposal
description: Use to turn ambiguity, validation gaps, breaking changes, survived mutations, or spec/test conflicts into human-readable decision options such as accept, update spec, reject, refine tests, or defer.
---

# Decision Proposal

## Purpose

Prepare human governance decisions without letting the agent silently redefine correctness.

## Script-First Execution

Before framing decision options, collect or reuse deterministic evidence when local artifacts are available:

```powershell
python agent-skills/impact-analysis/scripts/collect_impact_evidence.py --repo-root . --json
python agent-skills/test-effectiveness-evaluation/scripts/collect_validation_result_evidence.py --json path/to/test-or-mutation-output.txt
python agent-skills/orchestrator-state-machine/scripts/validate_orchestrator_state.py path/to/state.json --json
```

Use mutation/test/tool availability evidence when relevant:

```powershell
python agent-skills/mutation-testing/scripts/detect_mutation_test_tools.py --repo-root . --json
```

Use LLM judgement after evidence collection to explain why a decision is needed, compare options, and recommend only when the evidence supports it. Do not ask the LLM to infer changed paths, test outcomes, mutation availability, or workflow state when local command output can establish those facts.

## Workflow

1. Run or reuse deterministic evidence checks for impact, test/mutation results, tool availability, and workflow state when local artifacts exist; if not available, state the fallback evidence source.
2. Read spec refs, impact analysis, test effectiveness evaluation, mutation result, risks, open questions, and current workflow state.
3. Identify the decision needed and why it cannot be resolved mechanically.
4. Present clear options such as accept change, update spec, reject change, refine tests, fix implementation, defer, or accept risk.
5. For each option, list consequences, validation impact, spec/test updates, and risk.
6. Recommend one option only when evidence supports it.
7. Record required durable-state updates after the human decision.
8. Hand accepted decisions to `spec-test-evolution` or the root orchestrator.

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
