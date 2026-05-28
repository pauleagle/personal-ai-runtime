# PB-FU-002 Integrate mdl_kernel into Spec-Driven Change Verification Workflow Playbook

## Metadata

- Type: Playbook Follow-up
- ID: PB-FU-002
- Status: Draft
- Parent Playbook: `agent-playbooks/spec-driven-change-verification-workflow-playbook.md`
- Suggested Location: `backlog/PB-FU-002-integrate-mdl-kernel-into-spec-driven-change-verification-workflow-playbook.md`
- Related Concepts:
  - Spec-Driven Change Verification Workflow
  - Preflight Protocol
  - Scope Control
  - Completion Check
  - Devil's Advocate Review
  - Atomic Subagent Orchestration
  - Minimal Faithful Execution Kernel
- External Source:
  - Working name: `mdl_kernel | minimal faithful execution kernel`
  - Shared by: https://github.com/scyprodigy
  - Attribution status: Confirmed
  - Attribution note: Credit the source by GitHub profile link only.

---

## Summary

Integrate the `mdl_kernel` concept into the Spec-Driven Change Verification Workflow Playbook as a compact execution kernel.

The core idea is:

> Validity is handled by binary gates. Compression is handled only after validity passes.

In other words:

- Faithfulness, scope, authority, correction cost, and usability are not scoring preferences.
- Any failed gate invalidates the plan or output.
- Only after all gates pass may the agent minimize plan length, merge steps, delete redundant work, or compress the final response.

This follow-up should add a reusable micro-kernel layer beneath the existing workflow, so every phase can avoid two common failure modes:

1. Producing a short but invalid answer.
2. Producing a complete but over-expanded, scope-creeping answer.

---

## Background

The current Spec-Driven Change Verification Workflow Playbook already defines a large correctness workflow involving:

- Preflight Protocol
- Spec Drill-down / Clarification Loop
- Draft Plan / Draft Spec
- Devil's Advocate Review
- Atomic Work Item Decomposition
- Spec-Based Test Design
- Implementation
- Diff Analysis
- Intent / Impact Analysis
- Risk / Gap Identification
- JIT Test Generation
- Test Execution
- Mutation Testing
- Human Decision
- Spec / Test Evolution

The `mdl_kernel` is not a replacement for this workflow.

It is better understood as a minimal execution kernel that can be applied inside each step, especially when an agent needs to decide:

- What is the smallest complete answer?
- Whether a plan is valid before optimization.
- Whether a step is too vague and needs splitting.
- Whether a result is over-scoped or under-specified.
- Whether the agent should ask the user, proceed with a low-risk assumption, or stop.

---

## Problem

The current workflow is strong on correctness governance, but some execution-level decisions may still be ambiguous:

- When should the agent stop refining?
- When is a plan short enough?
- When is compression safe?
- Which checks are non-negotiable gates versus soft scoring preferences?
- How should an agent avoid trading away correctness for brevity?
- How should a subagent decide whether a vague step needs splitting?

Without a compact execution kernel, different agents may interpret the same playbook differently.

This can cause:

- hidden assumptions,
- scope creep,
- overlong plans,
- premature implementation,
- incomplete DONE checks,
- or excessive user-facing reasoning.

---

## Objective

Add an `mdl_kernel`-inspired section to the parent playbook that defines a minimal faithful execution loop.

The section should clarify that:

1. Completion starts from a smallest required checklist.
2. Validity is binary and gate-based.
3. Compression is allowed only after all gates pass.
4. Refinement repairs invalidity before optimizing length.
5. Verification includes both positive checklist confirmation and negative review.
6. Reply should expose only the verified minimum result, key assumptions, limits, and at most one useful next step.
7. The agent should stop once no shorter valid result is available.

---

## Non-goals

This follow-up should not:

- Replace the existing Spec-Driven Change Verification Workflow.
- Rewrite the whole parent playbook.
- Turn every small task into the full 16-step workflow.
- Add unnecessary bureaucracy to simple answers.
- Require all internal reasoning traces to be exposed to the user.
- Treat gate results as weighted scores.
- Use compression as an excuse to omit required DONE items.
- Publish source attribution before the author confirms the preferred credit format.

---

## Proposed Playbook Addition

Add a new section near the core principles or execution overlay area:

```md
### Minimal Faithful Execution Kernel

Use this kernel inside each workflow step, especially when producing a plan, decomposing work, reviewing a result, or preparing a user-facing reply.

#### 1. Target

Derive the smallest checklist that makes the request complete.

- Make only low-risk assumptions.
- Mark assumptions that may affect the outcome.
- Ask the user only when required information is missing and cannot be safely assumed.

#### 2. Validity Gates

A plan or result is valid only if all gates pass:

| Gate | Required Check |
|---|---|
| Faithfulness | Every DONE item is covered. |
| Scope | No work is outside the request or allowed boundary. |
| Authority | No action exceeds granted permission, available evidence, repository policy, or safety boundary. |
| Correction Cost | No shortcut is likely to cause a larger future fix. |
| Usability | The result is understandable to this recipient, not only to an ideal reader. |

Any failed gate makes the plan invalid.

Do not trade a failed gate against brevity, elegance, speed, or apparent usefulness.

#### 3. Objective

After all gates pass, minimize plan length or response length.

Compression is allowed only after validity is secured.

#### 4. Refine

When refining a plan or result:

- Repair failed gates before shortening.
- Split vague steps only when needed for a gate.
- Merge redundant steps only when meaning and checks remain intact.
- Delete anything that does not change the result.
- Accept only when all gates pass and no shorter valid form is available.

#### 5. Verify

Before finalizing:

- Confirm every DONE item and boundary.
- Run a negative review for overreach, hidden assumptions, stale facts, missing checks, and scope creep.
- If verification fails, state the gap briefly, correct it, then re-verify.

#### 6. Reply

The final reply should contain:

- the verified minimum result,
- key assumptions,
- known limits,
- and at most one concrete next step when continuation helps.

Do not expose internal scoring, search traces, or chain-of-thought unless the user explicitly asks for a safe summary.

#### 7. Stop

Stop when verification passes and no shorter valid result is available.
```

---

## Integration Map

| `mdl_kernel` Concept | Existing Workflow Area | Integration Purpose |
|---|---|---|
| `1_target` | Preflight Protocol / Spec Drill-down | Convert vague request into smallest DONE checklist. |
| `2_gates` | Scope Control / Devil's Advocate / Completion Check | Make validity binary and non-negotiable. |
| `3_score` | Atomic Planning / Context Budget Control | Optimize for shortest valid plan only after gates pass. |
| `4_refine` | Drill-down / DA / Atomic Decomposition | Repair, split, merge, and delete with explicit validity protection. |
| `5_verify` | Completion Check / Mutation Result Review | Add final negative review before accepting. |
| `6_reply` | User-facing Completion Report | Keep response useful, bounded, and not overloaded. |
| `7_stop` | Orchestrator Stop Condition | Prevent endless refinement and overengineering. |

---

## Suggested Implementation Steps

1. Add the `Minimal Faithful Execution Kernel` section to the parent playbook.
2. Add a short reference from the existing `Preflight Protocol` section.
3. Add a short reference from the existing `Workflow Decomposition / Atomic Work Items` section.
4. Add a short reference from the existing `Completion Check` or final verification section.
5. If a root skill exists for `spec-driven-change-verification`, consider whether the skill should receive a compressed version of this kernel.
6. Keep attribution as pending until the shadowMAS author confirms whether and how they want to be credited.

---

## Suggested Skill Extraction Rule

If this follow-up is later extracted into a skill or shared rule, keep the skill version shorter than the playbook version.

Suggested compact rule:

```md
Before optimizing a plan or response, derive the smallest DONE checklist and apply binary gates: faithfulness, scope, authority, correction cost, and usability. Any failed gate invalidates the plan. Repair failed gates before compression. Compress only after all gates pass. Final output should expose the verified minimum result, key assumptions, limits, and at most one useful next step.
```

---

## Acceptance Criteria

This follow-up is complete when:

- [ ] The parent playbook includes a `Minimal Faithful Execution Kernel` section.
- [ ] The section clearly states that gates are binary and non-negotiable.
- [ ] The section clearly separates validity gates from compression objective.
- [ ] The section explains when to split, merge, delete, repair, and stop.
- [ ] The section maps naturally to existing Preflight, DA, Atomic Decomposition, and Completion Check stages.
- [ ] Attribution is marked as pending until the shadowMAS author confirms preferred credit.
- [ ] No personal attribution is published without explicit confirmation.
- [ ] The update does not require rewriting the full parent playbook.

---

## Devil's Advocate Review

### DA-PB-FU-002-001 — Risk: This becomes another abstract layer

Severity: Medium

If the kernel is added as a philosophical section only, agents may ignore it.

Mitigation:

- Add concrete gate names.
- Add explicit pass/fail behavior.
- Reference it from actual execution stages.

### DA-PB-FU-002-002 — Risk: Compression may be misunderstood as under-answering

Severity: Medium

Agents may minimize too aggressively and omit useful context.

Mitigation:

- Emphasize that compression happens only after every DONE item and gate passes.
- Keep `usability` as a gate.

### DA-PB-FU-002-003 — Risk: Attribution ambiguity

Severity: Medium

The idea came from a shared external note, but the preferred attribution is not yet confirmed.

Mitigation:

- Keep attribution as pending.
- Use neutral wording such as `inspired by an externally shared mdl_kernel note`.
- Add explicit TODO to update attribution after confirmation.

### DA-PB-FU-002-004 — Risk: Full workflow becomes too heavy for small tasks

Severity: Low

If the kernel is interpreted as requiring the full Spec-Driven Workflow every time, it may slow down simple work.

Mitigation:

- State that the kernel is a lightweight per-step execution rule.
- It does not imply running the full 16-step workflow for every task.

---

## Attribution TODO

Before publishing this in a public-facing or explicitly credited form, confirm with the shadowMAS author:

1. Should the source be credited?
2. Which name, handle, or project name should be used?
3. Is the exact `mdl_kernel` text allowed to be quoted?
4. Should the repo include a source URL, private note reference, or no link?
5. Is this considered an idea contribution, inspiration, or reusable external material?

Until confirmed, use:

```md
External inspiration: `mdl_kernel | minimal faithful execution kernel`, shared by the shadowMAS author. Attribution format pending confirmation.
```

---

## Recommended Commit Message

```text
docs(backlog): add PB-FU-002 for mdl kernel integration
```

