# SK-FU-002 Normalize Prompt and Context Templates for LLM Execution Profiles

## Metadata

- Type: Skill Follow-up
- ID: SK-FU-002
- Status: Draft
- Source Request: Backlog request to normalize and template prompts and context for `hybrid`, `low-llm`, and `heavy-llm` execution profiles.
- Suggested Location: `backlog/SK-FU-002-normalize-prompt-context-templates-for-llm-execution-profiles.md`
- Scope:
  - `agent-skills/README.md`
  - `agent-skills/*/SKILL.md`
  - `agent-playbooks/*`
  - future shared prompt and context template artifacts
- Principle: Normalize prompt and context contracts before expanding LLM reasoning.
- Primary Goal: Make recurring LLM prompt/context prefixes cache-friendly without over-designing small tasks.
- Integration Status: Not integrated
- Status Impact: No current README status change; this is a non-blocking cross-skill maintenance follow-up.

---

## Summary

Add shared prompt and context templates for skills whose execution profile is `hybrid`, `low-llm`, or `heavy-llm`.

The goal is to reduce ad hoc prompting, oversized context packs, and inconsistent output contracts while making recurring prompt/context prefixes more cache-friendly. Deterministic evidence should still be collected first under SK-FU-001, but once LLM judgement is needed, the stable parts of the LLM-facing prompt and context should be normalized, bounded, and reusable as practical.

This should not become a heavy prompt framework. The design should keep stable instructions and contract shapes cacheable, while isolating variable run-specific evidence, file snippets, user requests, and validation results into small dynamic packets.

---

## Background

`agent-skills/README.md` currently defines execution profiles:

- `script`: deterministic commands, parsers, validators, or status checks do most of the work.
- `hybrid`: deterministic discovery first, then LLM judgement for interpretation, synthesis, or scoped decisions.
- `low-llm`: mostly structured text transformation or cleanup with limited judgement after facts are collected.
- `heavy-llm`: semantic reasoning, design, review, decomposition, or decision framing is the core value.

SK-FU-001 focuses on minimizing avoidable LLM work through script-first execution. This follow-up focuses on the remaining LLM work: when LLM reasoning is required, prompts and context should follow stable templates rather than being rebuilt from scratch every time.

---

## Problem

Current skill execution can still vary too much after deterministic evidence is collected:

- Context packs may include different levels of detail for similar tasks.
- Prompts may omit scope boundaries, output contracts, or uncertainty handling.
- `hybrid` skills may mix raw evidence and interpretation in inconsistent ways.
- `low-llm` skills may overuse free-form judgement for structured cleanup work.
- `heavy-llm` skills may receive broad context without a clear reasoning frame or decision contract.
- Subagent handoffs may become harder to compare because each run uses a different prompt shape.
- Prompt caching opportunities are reduced when stable instructions, output contracts, and profile-specific reasoning frames are rewritten differently for every run.
- Overly elaborate templates may cost more context than they save for small tasks.

This makes execution harder to audit, repeat, test, and improve.

---

## Objective

Define shared prompt and context template guidance for `hybrid`, `low-llm`, and `heavy-llm` skills.

The templates should make each LLM step explicit about:

- task objective,
- execution profile,
- deterministic evidence already collected,
- relevant context sources,
- allowed scope,
- forbidden scope,
- assumptions,
- uncertainty handling,
- required output format,
- validation or closeout expectations,
- and traceability back to files, specs, tests, or prior decisions.

The templates should also separate cacheable and dynamic content:

- Cacheable: profile pattern, role/task frame, stable rules, output contract, forbidden behaviors, and human-governance boundaries.
- Dynamic: current user request, command output, file snippets, changed paths, test results, validation artifacts, open questions, and run-specific assumptions.

For tiny tasks, a compact inline contract is enough; do not force a full multi-section template when a short direct answer or transformation is safer and cheaper.

---

## Target Profiles

### `hybrid`

Use a prompt template that separates:

- deterministic facts,
- inferred risks or gaps,
- judgement requested from the LLM,
- decisions that must remain with the user,
- and validation evidence required before closeout.

The LLM should not rediscover file, diff, status, test, or validator facts that were already collected by command output.

### `low-llm`

Use a compact transformation template that includes:

- input text or artifact path,
- target style or schema,
- preservation rules,
- allowed edits,
- forbidden edits,
- output format,
- and verification checklist.

The LLM should focus on bounded normalization, cleanup, classification, or formatting rather than open-ended reasoning.

### `heavy-llm`

Use a reasoning template that includes:

- problem statement,
- accepted facts,
- relevant constraints,
- competing options,
- risk categories,
- decision gates,
- uncertainty budget,
- and required structured output.

The LLM should reason deeply, but still from a bounded context pack with explicit evidence and traceability.

---

## Drill-down: Profile Pattern Analysis

### Inventory Snapshot

Current `agent-skills/README.md` profile distribution:

| Profile | Count | Skills |
|---|---:|---|
| `hybrid` | 12 | `preflight-protocol`, `playbook-to-skill`, `spec-driven-change-verification`, `orchestrator-state-machine`, `context-pack-builder`, `atomic-subagent-runner`, `diff-analysis`, `impact-analysis`, `mutation-testing`, `test-effectiveness-evaluation`, `spec-test-evolution`, `utf8-traditional-chinese-defaults` |
| `low-llm` | 1 | `changelog-normalization` |
| `heavy-llm` | 11 | `prompt-to-playbook`, `spec-drill-down`, `spec-definition`, `devils-advocate-review`, `devils-advocate-drill-down`, `workflow-atomic-decomposition`, `spec-based-test-design`, `intent-analysis`, `jit-test-generation`, `decision-proposal`, `test-promotion` |
| `script` | 1 | `nested-module-git-initialization` |

The template design should focus on the 24 non-`script` skills while preserving SK-FU-001's rule that deterministic evidence is collected first.

### Profile-Level Design Patterns

### Prompt Cache Design Constraint

The profile patterns below should be designed around a stable prefix plus a small dynamic suffix:

```md
## Stable Cacheable Prefix

- Skill / profile pattern
- Reusable rules
- Scope and governance defaults
- Output contract
- Validation / closeout defaults

## Dynamic Run Packet

- User request
- Deterministic evidence
- Relevant file snippets or artifact paths
- Current assumptions / gaps
- Required decision or transformation
```

Design guidance:

- Keep stable template text identical across similar runs when possible.
- Put volatile command output, diffs, test logs, and source snippets after the stable prefix.
- Prefer one profile pattern plus a short dynamic packet over bespoke prompts for every skill execution.
- Avoid giant universal prompts; cacheability should come from stable, profile-specific contracts, not from one all-purpose mega-template.
- Allow a "minimal contract" path for small low-risk tasks.

#### Pattern H1: Evidence Interpretation (`hybrid`)

Applies to:

- `diff-analysis`
- `impact-analysis`
- `mutation-testing`
- `test-effectiveness-evaluation`
- `utf8-traditional-chinese-defaults`

Context architecture:

- Deterministic Evidence: command output, validator output, file status, test/mutation availability, or decoding evidence.
- Evidence Scope: repository boundary, staged/unstaged mode, target file, result artifact, or selected path set.
- Interpretation Request: classify risk, confidence, validation scope, gap type, or likely cause.
- Human Decision Boundary: identify ambiguity or accepted-risk decisions that cannot be resolved mechanically.

Prompt contract:

```md
## Prompt Contract: Evidence Interpretation

- Objective:
- Evidence To Treat As Fact:
- Evidence Scope:
- Interpretation Needed:
- Do Not Re-run Or Re-infer:
- Risk / Gap Taxonomy:
- Human Decision Required When:
- Required Output:
```

Output contract:

```md
## Output Contract: Evidence Interpretation

- Evidence Summary:
- Interpretation:
- Risk Or Gap Classification:
- Confidence:
- Recommended Validation:
- Human Decision Needed:
- Follow-ups:
```

#### Pattern H2: State And Contract Gate (`hybrid`)

Applies to:

- `spec-driven-change-verification`
- `orchestrator-state-machine`
- `context-pack-builder`
- `atomic-subagent-runner`
- `spec-test-evolution`

Context architecture:

- Durable State Or Contract: orchestrator state, context manifest, subagent job contract, evolution plan, or current workflow step.
- Deterministic Validation: state/contract/helper output and missing-field warnings.
- Gate Inputs: allowed scope, forbidden scope, validation requirements, dependency state, merge policy, and human decision status.
- State Patch Target: artifact or note that would receive durable updates.

Prompt contract:

```md
## Prompt Contract: State And Contract Gate

- Objective:
- Current Durable State Or Contract:
- Deterministic Validation:
- Allowed Scope:
- Forbidden Scope:
- Gate Rules:
- State Patch Policy:
- Stop Conditions:
- Required Output:
```

Output contract:

```md
## Output Contract: State And Contract Gate

- Gate Status:
- Ready Items:
- Blocked Items:
- Required State Patch:
- Validation Evidence:
- Human Decision Needed:
- Resume Note:
```

#### Pattern H3: Maintenance Routing (`hybrid`)

Applies to:

- `preflight-protocol`
- `playbook-to-skill`

Context architecture:

- User Request: exact requested change or review mode.
- Repository Rules: AGENTS / README / inventory constraints.
- Deterministic Discovery: target files, mappings, git status, validators, and existing conventions.
- Routing Decision: whether to assess, edit, extract, resync, ask, or stop.

Prompt contract:

```md
## Prompt Contract: Maintenance Routing

- Objective:
- User Request:
- Deterministic Discovery:
- Applicable Rules:
- Routing Options:
- Blocking Ambiguity:
- Planned Edits Or No-Edit Mode:
- Required Output:
```

Output contract:

```md
## Output Contract: Maintenance Routing

- Task Understanding:
- Route Selected:
- Assumptions:
- Risks:
- Files Likely Touched:
- Validation Plan:
- Open Questions:
```

#### Pattern L1: Bounded Transformation (`low-llm`)

Applies to:

- `changelog-normalization`

Context architecture:

- Source Artifact: exact file or text to normalize.
- Structure Evidence: headings, dates, categories, ordering, noise flags, and missing-file status.
- Preservation Rules: facts, version ownership, dates, entries, and wording that must not be invented.
- Transformation Target: schema, category set, ordering rule, or cleanup style.

Prompt contract:

```md
## Prompt Contract: Bounded Transformation

- Objective:
- Source Artifact:
- Deterministic Structure Evidence:
- Target Shape:
- Preserve:
- Allowed Edits:
- Forbidden Edits:
- Verification Checklist:
- Required Output:
```

Output contract:

```md
## Output Contract: Bounded Transformation

- Normalized Structure:
- Entries Kept:
- Entries Moved Or Merged:
- Entries Rewritten Or Removed:
- Open Questions:
- Verification Notes:
```

Design constraint:

- `low-llm` prompts should stay short. The template should reduce judgement, not introduce a large reasoning scaffold.

#### Pattern G1: Requirements And Spec Synthesis (`heavy-llm`)

Applies to:

- `prompt-to-playbook`
- `spec-drill-down`
- `spec-definition`

Context architecture:

- Source Intent: user request, source prompt, existing playbook, clarified requirements, or candidate spec.
- Known Facts: deterministic repository facts and accepted decisions.
- Unknowns: ambiguity, open questions, unstated assumptions, and governance decisions.
- Target Contract: playbook section, spec section, acceptance criteria, or non-goal list.

Prompt contract:

```md
## Prompt Contract: Requirements And Spec Synthesis

- Objective:
- Source Intent:
- Accepted Facts:
- Constraints:
- Open Questions:
- Non-goals:
- Target Contract:
- Human Decision Required When:
- Required Output:
```

Output contract:

```md
## Output Contract: Requirements And Spec Synthesis

- Clarified Requirements:
- Candidate Contract:
- Acceptance Criteria:
- Non-goals:
- Open Questions:
- Assumptions Removed Or Confirmed:
- Recommended Next Gate:
```

#### Pattern G2: Adversarial Review And Governance (`heavy-llm`)

Applies to:

- `devils-advocate-review`
- `devils-advocate-drill-down`
- `decision-proposal`
- `test-promotion`

Context architecture:

- Review Target: plan, spec, objection list, decision point, generated test, or candidate promotion.
- Evidence Base: deterministic evidence, spec refs, test results, mutation results, risk notes, or prior decisions.
- Governance Boundary: what the agent may recommend versus what the human must decide.
- Option Space: objections, options, defer/accept/reject choices, or promotion levels.

Prompt contract:

```md
## Prompt Contract: Adversarial Review And Governance

- Objective:
- Review Target:
- Evidence Base:
- Governance Boundary:
- Option Or Objection Space:
- Severity Or Promotion Scale:
- Blocking Criteria:
- Required Output:
```

Output contract:

```md
## Output Contract: Adversarial Review And Governance

- Findings Or Options:
- Severity / Recommendation:
- Why It Matters:
- Required Clarification Or Decision:
- Validation Impact:
- Blocked Step:
- Next Gate:
```

#### Pattern G3: Traceable Design Generation (`heavy-llm`)

Applies to:

- `workflow-atomic-decomposition`
- `spec-based-test-design`
- `jit-test-generation`
- `intent-analysis`

Context architecture:

- Accepted Source: spec refs, selected workflow, diff evidence, impact evidence, or intent evidence.
- Design Target: atomic items, test cases, JIT candidates, or intent/risk model.
- Traceability Requirement: every generated item maps back to spec refs, diff evidence, risk items, or validation gaps.
- Quality Gate: dependency edges, validation hooks, mutation expectation, confidence, and promotion status.

Prompt contract:

```md
## Prompt Contract: Traceable Design Generation

- Objective:
- Accepted Source:
- Deterministic Evidence:
- Generation Target:
- Traceability Rules:
- Quality Gate:
- Forbidden Inventions:
- Required Output:
```

Output contract:

```md
## Output Contract: Traceable Design Generation

- Generated Items:
- Traceability Map:
- Dependencies Or Preconditions:
- Validation Hooks:
- Confidence:
- Gaps:
- Next Gate:
```

### Shared Context Architecture

All non-`script` profile templates should share the same high-level context stack:

1. Evidence Packet: deterministic command, parser, validator, git, test, or artifact evidence from SK-FU-001.
2. Source Context: only the files, specs, playbooks, snippets, or artifacts needed for this LLM judgement.
3. Scope Contract: allowed scope, forbidden scope, non-goals, and human-governed decisions.
4. Reasoning Contract: the profile pattern and the exact judgement requested from the LLM.
5. Output Contract: structured result shape, validation/closeout notes, and next gate.

The shared stack should be implemented as guidance first. Reusable files or snippets can be introduced after the pattern matrix is accepted.

### Design Decisions From This Drill-down

- Use profile-specific patterns, not one universal mega-prompt.
- Keep `low-llm` templates compact and artifact-oriented.
- Let `hybrid` templates start from evidence packets and ask only for interpretation, routing, or gate decisions.
- Let `heavy-llm` templates carry explicit reasoning frames, but bound them with source context, traceability, and human decision gates.
- Treat prompt-cache friendliness as a primary design goal: stable prefix, dynamic run packet, repeatable output contract.
- Avoid over-design by allowing compact inline contracts for small tasks and by deferring reusable template files until the pattern matrix proves useful.
- Keep output Markdown by default; JSON should be required only for machine-ingested job contracts or validators.
- Do not add prompt templates to `script` profile skills unless a future human explicitly requests an LLM-facing closeout pattern.

### Open Design Questions

- Should shared templates live as Markdown snippets under a new `agent-skills/_shared/` location, under `agent-playbooks/`, or only in README guidance?
- Should `context-pack-builder` own the context contract templates, or should SK-FU-002 introduce a separate shared maintenance artifact?
- Should `atomic-subagent-runner` require a `prompt_contract` field in future JSON job contracts, or only recommend it?
- Should profile-specific templates become machine-readable metadata later, or remain human-readable guidance?

---

## Proposed Template Layers

### 1. Context Contract

Each LLM-bound context pack should declare:

```md
## Context Contract

- Task:
- Execution Profile:
- Skill:
- Required Inputs:
- Deterministic Evidence:
- Relevant Files:
- Relevant Specs or Playbooks:
- Prior Decisions:
- Allowed Scope:
- Forbidden Scope:
- Known Gaps:
- Token / Context Priority:
```

### 2. Prompt Contract

Each LLM prompt should declare:

```md
## Prompt Contract

- Objective:
- Use Evidence As Facts:
- Do Not Re-derive:
- Reasoning Scope:
- Required Output:
- Uncertainty Handling:
- Human Decision Required When:
- Validation / Closeout:
```

### 3. Output Contract

Each LLM result should declare:

```md
## Output Contract

- Summary:
- Findings:
- Decisions:
- Assumptions:
- Risks:
- Validation Evidence:
- Follow-ups:
- Blockers:
```

The exact output shape can remain Markdown unless a specific workflow requires JSON.

---

## Candidate Template Artifacts

Possible implementation paths:

- Add a shared "Prompt and Context Templates" section to `agent-skills/README.md`.
- Add reusable template files under a shared skill-maintenance location, if the repo adopts one.
- Add profile-specific snippets to selected `SKILL.md` files only when they materially change execution behavior.
- Extend context-pack-builder guidance so it can produce profile-aware context contracts.
- Extend atomic-subagent-runner guidance so subagent jobs include profile-aware prompt contracts.

Suggested template names:

- `hybrid-context-contract.md`
- `hybrid-prompt-contract.md`
- `low-llm-transformation-contract.md`
- `heavy-llm-reasoning-contract.md`
- `llm-output-contract.md`

---

## Non-goals

This follow-up should not:

- Replace SK-FU-001 script-first minimization.
- Force every skill to use the same exact prompt.
- Add large prompt frameworks that make small tasks heavier.
- Require hidden chain-of-thought capture or expose private reasoning.
- Make `script` profile skills LLM-heavy.
- Change current skill triggers, README status values, or playbook mappings in the backlog step.
- Treat templates as mandatory when a tiny direct answer is sufficient.

---

## Suggested Implementation Steps

1. Review current `hybrid`, `low-llm`, and `heavy-llm` skills in `agent-skills/README.md`.
2. Identify repeated LLM input patterns across those skills.
3. Draft shared context, prompt, and output contract snippets.
4. Decide where shared templates should live.
5. Update only high-impact skills first:
   - `context-pack-builder`
   - `atomic-subagent-runner`
   - `spec-driven-change-verification`
   - `spec-drill-down`
   - `spec-definition`
   - `workflow-atomic-decomposition`
   - `decision-proposal`
   - `prompt-to-playbook`
   - `playbook-to-skill`
6. Add lightweight examples showing how a script-first evidence block becomes an LLM prompt contract.
7. Verify the templates do not increase context size for low-complexity tasks.

---

## Acceptance Criteria

This follow-up is complete when:

- [ ] Shared template guidance exists for `hybrid`, `low-llm`, and `heavy-llm` profiles.
- [ ] The guidance separates stable cacheable prompt/context prefix from dynamic run-specific evidence packets.
- [ ] The guidance clearly separates deterministic evidence from LLM judgement.
- [ ] At least one context contract template exists.
- [ ] At least one prompt contract template exists.
- [ ] At least one output contract template exists.
- [ ] `low-llm` guidance stays compact and transformation-oriented.
- [ ] `heavy-llm` guidance supports deeper reasoning without unbounded context dumps.
- [ ] The design includes a minimal-contract path so small tasks are not forced into oversized templates.
- [ ] Subagent-oriented skills can reuse the same contract shape for handoffs.
- [ ] The update does not require current `script` profile skills to add LLM prompts.
- [ ] The update does not silently change skill triggers, README status values, or playbook mappings.

---

## Review Notes

This backlog item is intentionally paired with SK-FU-001.

SK-FU-001 asks:

> Can deterministic execution reduce the amount of LLM work?

SK-FU-002 asks:

> Once LLM work remains necessary, can its prompt, context, and output shape be made repeatable?

The desired outcome is not more prompting. The desired outcome is less improvisation around the prompting that is genuinely needed.

---

## Recommended Commit Message

```text
docs(backlog): add SK-FU-002 prompt context template follow-up
```
