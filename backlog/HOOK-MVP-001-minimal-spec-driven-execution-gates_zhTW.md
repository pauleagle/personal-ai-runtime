# HOOK-MVP-001 Minimal Spec-Driven Execution Gates

Version: v0.1-draft  
Status: MVP / Experimental  
Category: Runtime Governance  
Related:
- spec-driven-change-verification-workflow-playbook
- preflight-protocol
- devils-advocate-review
- devils-advocate-drill-down
- playbook-to-skill

---

# 1. 目的

本文件定義 Personal AI Runtime 的最小可行 Runtime Hook / Execution Gate 機制。

目標不是增加更多 prompt 規則，而是：

- 降低 agent 對長 context 的依賴
- 降低 instruction dilution
- 降低 scope drift
- 降低 hallucinated execution
- 將「請遵守規則」轉變為「執行前檢查」

本文件屬於 Runtime Governance Layer，而非一般 Playbook。

---

# 2. 核心理念

傳統 Prompt Engineering：

```text
請 AI 記得遵守規則
```

Hook / Gate 模式：

```text
如果不符合規則，就不允許進入下一步
```

核心差異：

| 模式 | 本質 |
|---|---|
| Prompt | 建議 |
| Playbook | 操作方法 |
| Skill | 可重用執行單元 |
| Hook / Gate | Runtime Enforcement |

---

# 3. MVP Gate 設計

MVP 階段先定義三種核心 Gate：

1. Pre-Run Gate
2. Pre-Edit Gate
3. Post-Run Gate

---

# 4. Pre-Run Gate

## 4.1 目的

防止 agent 尚未理解 spec / scope 就直接開始實作。

---

## 4.2 必須檢查項目

- 是否存在明確 atomic item
- 是否存在對應 spec / backlog / issue
- 是否列出 scope
- 是否列出 forbidden scope
- 是否列出 acceptance criteria
- 是否列出預期 artifact

---

## 4.3 Gate Failure 行為

若未通過：

- 禁止 implementation
- 禁止 file modification
- 只能要求補充資訊
- 只能回報缺失項目

---

# 5. Pre-Edit Gate

## 5.1 目的

防止 subagent 超出 scope 修改檔案。

此 Gate 為 MVP 階段最重要 Gate。

---

## 5.2 必須檢查項目

- 修改檔案是否位於 allowed paths
- 是否碰觸 forbidden paths
- 是否屬於 atomic item scope
- 是否出現大規模 unrelated rewrite
- 是否修改未宣告 dependency

---

## 5.3 Gate Failure 行為

若未通過：

- 阻止 edit
- 回報 scope violation
- 回到 orchestrator 重新決策
- 禁止自動擴大 scope

---

# 6. Post-Run Gate

## 6.1 目的

防止 agent 完成修改後未驗證即標記完成。

---

## 6.2 必須檢查項目

- 是否列出 changed files
- 是否列出驗證方式
- 是否執行 tests / lint / validation
- 是否對照 acceptance criteria
- 是否列出 remaining risks
- 是否產生 follow-up items

---

## 6.3 Gate Failure 行為

若未通過：

- 禁止標記完成
- 要求補充 verification
- 要求補充 risk analysis

---

# 7. 與 Subagent Architecture 的關係

Hook / Gate 的目的之一：

是讓 Subagent 可以安全化。

沒有 Hook 時：

```text
Subagent = 高風險自由執行
```

加入 Hook 後：

```text
Orchestrator
  ↓
Runtime Gates
  ↓
Scoped Subagent Execution
```

---

# 8. 未來可能演化方向

未來可能擴充：

- Usage Gate
- Cost Gate
- Context Budget Gate
- Spec Completeness Gate
- Diff Size Gate
- Risk Tier Gate
- Human Approval Gate
- Parallel Agent Conflict Gate

---

# 9. 與 Workflow 的關係

目前 workflow：

```text
PLAN
→ SPEC
→ IMPLEMENT
→ VERIFY
→ REVIEW
```

未來可能演化為：

```text
PLAN
→ Pre-Run Gate
→ IMPLEMENT
→ Pre-Edit Gate
→ VERIFY
→ Post-Run Gate
→ REVIEW
```

---

# 10. 核心原則

## 10.1 減少 Context Dependency

原則：

```text
能 Runtime Enforcement 的規則，
不要只依賴 Context 記憶。
```

---

## 10.2 降低自由度

目標不是讓 Agent 更自由。

而是：

```text
讓 Agent 在可控邊界內穩定執行。
```

---

## 10.3 將治理前移

避免：

```text
事後 review 才發現問題
```

改為：

```text
在執行前阻止問題
```

---

# 11. 當前狀態

目前屬於：

- 概念驗證（PoC）
- Runtime Governance MVP
- Hook Architecture 初始版

尚未綁定特定 runtime framework。

---

# 12. MVP Gate Contract

本節把前三個 Gate 轉成可驗收的最小契約。

MVP 不要求真正攔截所有工具呼叫；第一版只要求能以 deterministic input 判斷 gate 是否 `pass` / `blocked`，並輸出可讀的 blocking reasons。

---

## 12.1 共用輸入欄位

三種 Gate 應共用下列概念欄位：

| 欄位 | 說明 |
|---|---|
| `atomic_item_id` | 目前要執行的 atomic item；若沒有，Pre-Run Gate 應 blocked。 |
| `spec_ref` | 對應 spec、backlog、issue 或 durable artifact。 |
| `allowed_scope` | 允許讀寫或執行的路徑、artifact、workflow step。 |
| `forbidden_scope` | 禁止碰觸的路徑、artifact、行為或決策。 |
| `acceptance_criteria` | 完成此 item 前必須滿足的驗收條件。 |
| `expected_artifacts` | 預期會產生或修改的 artifact。 |
| `validation_plan` | 預期驗證方式，例如 tests、lint、validator、manual review 或 skip reason。 |

---

## 12.2 共用輸出欄位

三種 Gate 應回傳下列最小輸出：

| 欄位 | 說明 |
|---|---|
| `gate` | `pre-run`、`pre-edit` 或 `post-run`。 |
| `status` | `pass` 或 `blocked`。 |
| `blocking_reasons` | 若 blocked，列出具體缺失。 |
| `checked_items` | 已檢查項目與結果。 |
| `next_allowed_action` | 下一步允許做什麼，例如 ask-user、edit、validate、handoff。 |
| `notes` | 非阻塞風險或補充資訊。 |

---

## 12.3 Gate 判斷規則

### Pre-Run Gate

`pass` 條件：

- `atomic_item_id` 存在。
- `spec_ref` 存在。
- `allowed_scope` 與 `forbidden_scope` 已列出。
- `acceptance_criteria` 不為空。
- `expected_artifacts` 已列出，或明確說明此 item 不產生 artifact。

`blocked` 時只允許：

- 回報缺失欄位。
- 要求使用者或 orchestrator 補齊資訊。
- 建立或更新 backlog/spec drill-down。

### Pre-Edit Gate

`pass` 條件：

- 每個 proposed changed file 都落在 `allowed_scope`。
- 沒有 proposed changed file 落在 `forbidden_scope`。
- proposed change 能對應到 `atomic_item_id` 或 declared dependency。
- 沒有大規模 unrelated rewrite。

`blocked` 時只允許：

- 回報 scope violation。
- 回到 orchestrator 重切 scope。
- 要求人類批准擴大 scope。

### Post-Run Gate

`pass` 條件：

- changed files 已列出。
- validation actions 已列出。
- acceptance criteria 已逐項對照。
- remaining risks 已列出，或明確標示 none known。
- follow-up items 已列出，或明確標示 none。
- 若 workflow 使用 commit checkpoint，必須已完成 commit 或明確 blocked reason。

`blocked` 時只允許：

- 補跑驗證。
- 補齊 acceptance / risk / follow-up 對照。
- 回報未完成項，不得宣稱 item complete。

---

# 13. MVP Acceptance Criteria

- [x] Pre-Run Gate 有明確 input contract、pass / blocked 條件與 blocked 行為。
- [x] Pre-Edit Gate 有明確 input contract、pass / blocked 條件與 blocked 行為。
- [x] Post-Run Gate 有明確 input contract、pass / blocked 條件與 blocked 行為。
- [x] 三種 Gate 使用一致的 `pass` / `blocked` 狀態語義。
- [x] Gate output 能列出 `blocking_reasons` 與 `next_allowed_action`。
- [x] MVP 不要求綁定特定 runtime framework。
- [x] MVP 不要求攔截所有工具呼叫；可以先用 explicit gate check artifact 或 helper 實作。
- [x] Gate failure 不得被 prompt judgement 覆蓋；必須由補齊資訊、人類決策或 scope 調整解除。
- [x] 若後續進入 implementation，第一個 atomic item 應只做 deterministic contract validator，不做 full runtime hook framework。

---

# 14. Devil's Advocate Drill-down

本節在進入 `HOOK-MVP-001-A1` 前，先把主要 objections 轉成處置狀態與 spec patch requirements。

注意：本文件先前尚未有獨立 Devil's Advocate Review 輸出，因此本節同時列出 review objections 並完成 drill-down。後續若流程要求更嚴格，可先另產生完整 DA Review，再進入本節格式。

## 14.1 Objection Resolution Table

| ID | Severity | Objection | Status | Resolution |
|---|---|---|---|---|
| `DA-HOOK-MVP-001-001` | Low | `pass` / `blocked` 可能太粗，無法表達非阻塞 warning。 | resolved | MVP 維持 binary gate；非阻塞資訊放入 `notes`，不得影響 `status` 語義。 |
| `DA-HOOK-MVP-001-002` | Low | Pre-Run Gate 可能讓探索型分析工作也被要求提供完整 atomic item。 | resolved | Gate 只套用於宣告要進入 implementation / edit / completion 的工作；純分析、drill-down、handoff 可使用 `next_allowed_action: ask-user` 或 `handoff`。 |
| `DA-HOOK-MVP-001-003` | Medium | `allowed_scope` / `forbidden_scope` 若語義不清，validator 會變成形式檢查。 | resolved | `HOOK-MVP-001-A1` 先支援 repo-relative paths、artifact IDs、workflow step names 的簡單清單；不做複雜 policy language。 |
| `DA-HOOK-MVP-001-004` | Medium | Pre-Edit Gate 要求 proposed changed files，但實作前未必能完全預知最後 diff。 | resolved | Pre-Edit Gate 檢查「宣告的 proposed changed files」；實際 diff drift 交給 Post-Run Gate 檢查。若實作中發現需新增路徑，必須回到 gate 擴 scope。 |
| `DA-HOOK-MVP-001-005` | Medium | Post-Run Gate 要求 commit checkpoint 可能和使用者要求「不要 commit」衝突。 | resolved | commit 僅在 workflow 使用 commit checkpoint 時是 pass 條件；否則必須提供 explicit skip reason。 |
| `DA-HOOK-MVP-001-006` | High | deterministic helper 可能被誤認為真正 runtime hook enforcement，造成 false confidence。 | resolved | A1 明確命名為 contract validator，不宣稱攔截 tool calls；文件保留「MVP 不要求攔截所有工具呼叫」。 |
| `DA-HOOK-MVP-001-007` | High | Gate failure 如果可以被 agent prose override，Runtime Governance 會退化回 prompt 建議。 | resolved | Gate failure 只能由補齊資訊、人類決策或 scope 調整解除；LLM judgement 不得直接覆蓋 blocked status。 |

## 14.2 Spec Patch Requirements

- A1 validator 的 input contract 必須包含 gate type 與 gate-specific payload，而不是只檢查文件中是否有文字描述。
- A1 先採用簡單資料結構：清單、字串、布林與 object；不引入 policy DSL。
- Pre-Edit Gate 必須支援 `proposed_changed_files`，並檢查它們是否落在 `allowed_scope` 且避開 `forbidden_scope`。
- Post-Run Gate 必須允許 `commit_checkpoint` 搭配 `skip_reason`，以支援使用者明確要求不 commit 的情境。
- Output 必須保留 binary `status`，warning / caveat 只能放在 `notes`。
- 文件與 helper 不得宣稱已提供完整 runtime interception。

## 14.3 Compatibility / Replacement Decision Table

| Topic | Decision |
|---|---|
| 現有 Codex tool execution | 不替換、不攔截；A1 只做 explicit gate contract validation。 |
| 現有 spec-driven workflow playbook | 不在 A1 修改；先以 backlog contract validator 驗證概念。 |
| 現有人工 usage gate | 不替換；commit + 流量確認仍由互動流程執行。 |
| 未來 runtime hook framework | deferred；需要 A1 驗證有用後再設計。 |
| Human governance decisions | 不自動化；blocked status 需要補資訊、人類決策或 scope 調整才能解除。 |

## 14.4 Deferred Items

- 真正攔截 tool calls / edit calls 的 runtime hook framework。
- 支援複雜 path glob、rule priority、policy inheritance 或 multi-repo scope policy。
- 與 Codex CLI / wrapper / daemon 的整合方式。
- 將 gate result 寫入 durable orchestrator state 的 schema。

## 14.5 Gate Status

`pass` for `HOOK-MVP-001-A1`，條件是 A1 僅實作 deterministic contract validator，不實作 full runtime hook framework。

---

# 15. 下一個 Atomic Slice 建議

建議下一個 implementation item：

```text
HOOK-MVP-001-A1: deterministic gate contract validator
```

Scope:

- 新增一個最小 helper，讀取 local JSON gate contract artifact。
- 驗證 `pre-run`、`pre-edit`、`post-run` 的 required fields。
- 驗證 Pre-Edit Gate 的 `proposed_changed_files` 是否落在 `allowed_scope` 並避開 `forbidden_scope`。
- 允許 Post-Run Gate 的 `commit_checkpoint` 使用 explicit `skip_reason`。
- 輸出 structured JSON：`status`、`blocking_reasons`、`checked_items`、`next_allowed_action`。
- 新增 focused unit tests。

Non-goals:

- 不攔截 Codex tool calls。
- 不建立 daemon、agent wrapper 或 runtime server。
- 不修改現有 spec-driven workflow playbook。
- 不自動 commit、revert、擴大 scope 或作出 human-governance decision。
- 不宣稱已完成 runtime interception。

Validation:

- focused unit tests。
- CLI smoke check。
- `git diff --check`。

## 15.1 Implementation Log

Status: completed.

Implemented:

- Added `runtime-hooks/scripts/validate_gate_contract.py`.
- Added focused tests under `tests/runtime_hooks/test_validate_gate_contract.py`.
- Added smoke fixture `tests/fixtures/gate_contract_pre_run_sample.json`.
- Implemented `pre-run`, `pre-edit`, and `post-run` validation.
- Implemented binary `status`: `pass` or `blocked`.
- Implemented `blocking_reasons`, `checked_items`, `next_allowed_action`, and `notes` output fields.
- Implemented simple repo-relative exact / prefix / `/**` scope matching for `proposed_changed_files`.
- Supported `commit_checkpoint.status` values `committed`, `skipped`, and `blocked`; `skipped` / `blocked` require explicit `skip_reason` or `blocked_reason`.

Out of scope by design:

- No tool-call interception.
- No daemon, wrapper, or runtime server.
- No policy DSL.
- No automatic commit, revert, scope expansion, or human-governance decision.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_run_sample.json --json`.
- Ran `git diff --check`.

Direct smoke result:

- Focused tests reported 6 tests OK.
- Full test suite reported 59 tests OK.
- CLI smoke returned `gate: pre-run`, `status: pass`, and `next_allowed_action: edit`.
- The first sandboxed CLI smoke hit the known `windows sandbox: spawn setup refresh`; the same command succeeded when rerun with escalated execution.

---

## 15.2 Atomic Slice: `HOOK-MVP-001-A2`

```text
HOOK-MVP-001-A2: validator usage guidance and representative fixtures
```

Scope:

- Add a minimal `runtime-hooks/README.md` explaining what the MVP validator does and does not do.
- Add representative `pre-edit` and `post-run` sample gate contract fixtures.
- Keep A2 limited to documentation and fixtures; do not implement runtime interception, wrappers, daemons, policy DSL, or automatic governance decisions.

Acceptance criteria:

- `runtime-hooks/README.md` documents the validator command, expected output fields, fixtures, and MVP boundaries.
- Sample fixtures exist for `pre-run`, `pre-edit`, and `post-run`.
- Each sample fixture passes `validate_gate_contract.py --json`.
- Focused unit tests still pass.
- `git diff --check` passes.

Non-goals:

- No tool-call interception.
- No daemon, runtime wrapper, or Codex CLI integration.
- No policy DSL.
- No automatic commit, revert, scope expansion, or approval decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/README.md` with validator purpose, command usage, output fields, fixtures, and MVP boundaries.
- Added `tests/fixtures/gate_contract_pre_edit_sample.json`.
- Added `tests/fixtures/gate_contract_post_run_sample.json`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_run_sample.json --json`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_edit_sample.json --json`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_post_run_sample.json --json`.
- Ran `git diff --check`.

Direct smoke result:

- Focused tests reported 6 tests OK.
- All three fixture smoke checks returned `status: pass`.
- The sandboxed fixture smoke checks hit the known `windows sandbox: spawn setup refresh`; escalated reruns succeeded.

---

## 15.3 Atomic Slice: `HOOK-MVP-001-A3`

```text
HOOK-MVP-001-A3: document Python baseline for portable hook usage
```

Scope:

- Document the runtime hook Python version baseline for cloning this repo onto another machine.
- Keep the baseline as a minimum supported version rather than an exact pin.
- Do not add dependency management, virtual environment setup, packaging metadata, or CI.

Acceptance criteria:

- `runtime-hooks/README.md` states the required Python version.
- The documentation distinguishes required minimum version from current local validated baseline.
- The documentation states whether third-party packages are needed.
- Focused validator tests still pass.
- `git diff --check` passes.

Decision:

- Required baseline: Python 3.10 or newer.
- Current local validated baseline: Python 3.10.11.
- No `.python-version` is added for A3 because the hook MVP only needs a minimum version, and an exact pin could over-constrain company-machine setup.

Implementation log:

Status: completed.

Implemented:

- Added Python baseline guidance to `runtime-hooks/README.md`.

Validation actions:

- Ran `python --version`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `git diff --check`.

Direct result:

- Local Python reported `Python 3.10.11`.
- Focused tests reported 6 tests OK.

---

## 15.4 Atomic Slice: `HOOK-MVP-001-A4`

```text
HOOK-MVP-001-A4: runtime hook environment smoke check
```

Scope:

- Add a minimal environment check helper for validating a fresh clone on another machine.
- Check the Python minimum version and required runtime hook MVP files.
- Keep the helper dependency-free and compatible with older Python syntax where practical, so an outdated interpreter can return a clear blocked result.
- Document the environment smoke command in `runtime-hooks/README.md`.

Acceptance criteria:

- The helper reports `pass` when Python meets the baseline and required hook files exist.
- The helper reports `blocked` when Python is older than 3.10.
- The helper reports `blocked` when required hook MVP files are missing.
- The helper emits structured JSON with `status`, `blocking_reasons`, `checked_items`, and `next_allowed_action`.
- Focused runtime hook tests pass.
- `git diff --check` passes.

Non-goals:

- No dependency manager, virtual environment setup, packaging metadata, or CI.
- No runtime interception.
- No automatic installation or machine configuration.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/scripts/check_runtime_hooks_environment.py`.
- Added `tests/runtime_hooks/test_check_runtime_hooks_environment.py`.
- Added the environment smoke command to `runtime-hooks/README.md`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\check_runtime_hooks_environment.py --repo-root . --json`.
- Ran `git diff --check`.

Direct result:

- Environment smoke returned `status: pass`.
- Focused runtime hook tests reported OK.
- Full test suite reported 63 tests OK.

---

## 15.5 Atomic Slice: `HOOK-MVP-001-A5`

```text
HOOK-MVP-001-A5: one-command runtime hook MVP smoke
```

Scope:

- Add a single smoke helper that runs the environment check and all representative sample gate contracts.
- Keep the smoke helper dependency-free.
- Ensure the smoke helper blocks on environment failure before loading the gate validator.
- Document the full MVP smoke command in `runtime-hooks/README.md`.

Acceptance criteria:

- The smoke helper returns `pass` when the environment check passes and all sample gate contracts pass.
- The smoke helper returns `blocked` when the environment check is blocked.
- The smoke helper returns structured JSON with `status`, `environment`, `gate_results`, `blocking_reasons`, and `next_allowed_action`.
- The environment helper includes the smoke helper itself in required file checks.
- Focused runtime hook tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No dependency manager, virtual environment setup, packaging metadata, CI, or automatic installation.
- No runtime interception.
- No policy DSL.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Added `tests/runtime_hooks/test_run_runtime_hooks_smoke.py`.
- Added the full MVP smoke command to `runtime-hooks/README.md`.
- Updated `check_runtime_hooks_environment.py` required file checks to include the smoke helper.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --json`.
- Ran `git diff --check`.

Direct result:

- Full MVP smoke returned `status: pass`.
- Focused runtime hook tests reported OK.
- Full test suite reported 67 tests OK.
- The sandboxed full MVP smoke check hit the known `windows sandbox: spawn setup refresh`; escalated rerun succeeded.

---

## 15.6 Atomic Slice: `HOOK-MVP-001-A6`

```text
HOOK-MVP-001-A6: explicit contract support for runtime hook MVP smoke
```

Scope:

- Allow the full MVP smoke helper to validate explicit gate contract paths.
- Preserve the existing default behavior of validating the representative sample fixtures when no explicit contract is provided.
- Include selected contract paths in structured JSON output.
- Document the explicit contract command in `runtime-hooks/README.md`.

Acceptance criteria:

- `run_runtime_hooks_smoke.py` accepts repeated `--contract` arguments.
- No `--contract` still validates the three representative sample fixtures.
- Explicit valid contracts return `pass`.
- Explicit invalid contracts return `blocked` and aggregate blocking reasons.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No contract discovery or glob expansion.
- No policy DSL.
- No runtime interception.
- No automatic creation or repair of contract artifacts.

Implementation log:

Status: completed.

Implemented:

- Added repeated `--contract` support to `run_runtime_hooks_smoke.py`.
- Added `contract_paths` to smoke helper JSON output.
- Added focused tests for default samples, explicit valid contracts, explicit invalid contracts, and CLI explicit contract usage.
- Added explicit contract command guidance to `runtime-hooks/README.md`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --json`.
- Ran `git diff --check`.

Direct result:

- Explicit contract smoke returned `status: pass`.
- Focused runtime hook smoke tests reported OK.
- Full test suite reported 70 tests OK.
- The sandboxed explicit contract smoke check hit the known `windows sandbox: spawn setup refresh`; escalated rerun succeeded.

---

## 15.7 Atomic Slice: `HOOK-MVP-001-A7`

```text
HOOK-MVP-001-A7: fresh clone checklist and smoke output assertions
```

Scope:

- Add a concise fresh clone checklist for runtime hook MVP validation.
- Document smoke command exit code semantics.
- Add focused tests for CLI markdown output and invalid-contract non-zero exit behavior.
- Keep helper behavior unchanged.

Acceptance criteria:

- `runtime-hooks/README.md` includes a fresh clone checklist.
- README documents that smoke commands return `0` on `pass` and non-zero on `blocked`.
- CLI markdown output includes status and next allowed action.
- CLI invalid contract smoke returns non-zero and structured blocked JSON.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No dependency manager, packaging metadata, CI, or install automation.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Fresh Clone Checklist` guidance to `runtime-hooks/README.md`.
- Added CLI markdown output and invalid-contract exit code tests to `tests/runtime_hooks/test_run_runtime_hooks_smoke.py`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported 9 tests OK.
- Full test suite reported 72 tests OK.

---

## 15.8 Atomic Slice: `HOOK-MVP-001-A8`

```text
HOOK-MVP-001-A8: smoke troubleshooting guidance and environment CLI assertions
```

Scope:

- Add troubleshooting guidance for blocked runtime hook smoke checks.
- Add focused tests for environment helper CLI markdown output and non-zero blocked exit behavior.
- Keep helper behavior unchanged.

Acceptance criteria:

- `runtime-hooks/README.md` explains how to inspect `blocking_reasons`, `checked_items`, and `next_allowed_action`.
- README lists common first fixes for Python version, missing files, and blocked gate contracts.
- Environment helper CLI markdown output includes status and next allowed action.
- Environment helper CLI returns non-zero structured JSON when required files are missing.
- Focused environment helper tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No dependency manager, packaging metadata, CI, or install automation.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Troubleshooting Blocked Smoke Checks` guidance to `runtime-hooks/README.md`.
- Added environment helper CLI markdown and blocked exit tests.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Focused environment helper tests reported 6 tests OK.
- Full test suite reported 74 tests OK.

---

## 15.9 Atomic Slice: `HOOK-MVP-001-A9`

```text
HOOK-MVP-001-A9: smoke result interpretation guidance
```

Scope:

- Add concise README guidance for interpreting passing and blocked smoke results.
- Keep this slice documentation-only.

Acceptance criteria:

- README states the expected key fields for a passing full MVP smoke result.
- README states that blocked smoke results must stop implementation.
- README instructs rerunning the same smoke command after fixing blocking reasons.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Interpreting Smoke Results` guidance to `runtime-hooks/README.md`.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.10 Atomic Slice: `HOOK-MVP-001-A10`

```text
HOOK-MVP-001-A10: MVP usage and non-usage boundaries
```

Scope:

- Add README guidance for when to use the runtime hook MVP helpers.
- Add README guidance for when not to use them.
- Keep this slice documentation-only.

Acceptance criteria:

- README states that helpers are for deterministic checks of explicit gate contract artifacts.
- README lists fresh clone and active atomic item validation as valid uses.
- README states that helpers are not tool-call interception, runtime wrappers, daemons, policy DSLs, or human-approval substitutes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `When To Use This MVP` and `When Not To Use This MVP` sections to `runtime-hooks/README.md`.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.11 Atomic Slice: `HOOK-MVP-001-A11`

```text
HOOK-MVP-001-A11: MVP current status and deferred next options
```

Scope:

- Summarize the current HOOK-MVP-001 implementation status after A1 through A10.
- Separate completed MVP helper capabilities from deferred runtime governance work.
- Keep this slice documentation-only and suitable as a low-traffic handoff point.

Current MVP status:

- Gate contract spec exists for `pre-run`, `pre-edit`, and `post-run`.
- Deterministic gate contract validator exists at `runtime-hooks/scripts/validate_gate_contract.py`.
- Runtime hook environment check exists at `runtime-hooks/scripts/check_runtime_hooks_environment.py`.
- Full MVP smoke helper exists at `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Representative fixtures exist for all three gate types.
- Runtime hook README documents Python baseline, fresh clone checklist, smoke checks, troubleshooting, result interpretation, and MVP usage boundaries.
- Focused runtime hook tests and full test suite have passed across the A1-A8 implementation/test slices.
- A9-A11 are documentation-only closeout / handoff slices.

What this MVP can currently do:

- Validate explicit local JSON gate contracts.
- Validate proposed `pre-edit` changed files against simple allowed / forbidden scope entries.
- Validate `post-run` commit checkpoint shape including explicit skip / blocked reasons.
- Check whether a fresh clone has the required hook MVP files and Python 3.10+.
- Run one command to validate the runtime hook environment and sample or explicit gate contracts.

What remains deferred:

- Real tool-call or edit-call interception.
- Agent wrapper, daemon, runtime server, or Codex CLI integration.
- Policy DSL, rule inheritance, rule priority, or glob-rich scope language.
- Durable orchestrator-state persistence for gate results.
- Automatic installation, dependency management, or CI.
- Any automatic human-governance decision, approval, scope expansion, commit, revert, or completion claim.

Candidate next slices:

- `HOOK-MVP-001-A12`: add a concise contract schema reference section to `runtime-hooks/README.md`.
- `HOOK-MVP-001-A13`: add a small generated example for an active atomic item contract artifact.
- `HOOK-MVP-001-A14`: design, but do not implement, the first possible integration boundary with orchestrator state.
- `RT-FU-001`: continue collecting exact `windows sandbox: spawn setup refresh` observations separately from HOOK-MVP feature work.

Acceptance criteria:

- Backlog contains a clear current status summary.
- Backlog separates completed MVP helper capabilities from deferred work.
- Backlog lists safe next slices without starting them.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No README changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added the current MVP status, deferred work, and candidate next slices to this backlog.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.12 Atomic Slice: `HOOK-MVP-001-A12`

```text
HOOK-MVP-001-A12: README contract schema reference
```

Scope:

- Add a concise gate contract schema reference to `runtime-hooks/README.md`.
- Cover common required fields and gate-specific fields.
- Document the intentionally simple scope matching semantics.
- Keep this slice documentation-only.

Acceptance criteria:

- README lists the common required gate contract fields.
- README lists the additional `pre-edit` field.
- README lists the additional `post-run` fields and `commit_checkpoint` expectations.
- README states that scope matching is simple and not a policy DSL.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Gate Contract Schema Reference` to `runtime-hooks/README.md`.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.13 Atomic Slice: `HOOK-MVP-001-A13`

```text
HOOK-MVP-001-A13: active atomic item contract example
```

Scope:

- Add a small durable pre-run contract example for one active atomic item.
- Document how to validate that example before starting the corresponding edit.
- Add a focused test proving the example remains valid.
- Keep this slice limited to example artifact, README guidance, tests, and backlog state.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json` exists.
- The example maps `HOOK-MVP-001-A13` to spec reference, allowed scope, forbidden scope, acceptance criteria, expected artifacts, and validation plan.
- `runtime-hooks/README.md` points to the active atomic item example and its validator command.
- Focused validator tests pass.
- The example validates with `validate_gate_contract.py --json`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No runtime interception.
- No policy DSL.
- No automatic contract generation.
- No orchestrator-state persistence.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json`.
- Added `Active Atomic Item Example` guidance to `runtime-hooks/README.md`.
- Added a focused test that validates the durable active-item example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Active atomic item example returned `status: pass`.
- `git diff --check` passed.

---

## 15.14 Atomic Slice: `HOOK-MVP-001-A14`

```text
HOOK-MVP-001-A14: orchestrator state integration boundary
```

Scope:

- Design the first possible boundary between runtime hook gate results and durable orchestrator state.
- Document what an orchestrator may copy from gate validation output into a separate state patch.
- Document what remains outside the runtime hook MVP.
- Keep this slice design-only: no state persistence, no validator behavior change, no interception.

Acceptance criteria:

- `runtime-hooks/README.md` describes the orchestrator state integration boundary.
- The boundary identifies minimal fields an orchestrator could persist from a gate result.
- The boundary states that blocked gates must preserve concrete blocking reasons in orchestrator state.
- The boundary states that workflow cursor advancement, human decisions, scope expansion, and commit checkpoints remain orchestrator responsibilities.
- Existing orchestrator state sample validation still passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No orchestrator state schema implementation.
- No state mutation or persistence helper.
- No automatic active-item discovery.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Orchestrator State Integration Boundary` guidance to `runtime-hooks/README.md`.
- Documented candidate persisted fields: `atomic_item_id`, `gate`, `gate_status`, `next_allowed_action`, `blocking_reasons`, `validation_artifact`, and `checkpoint_status`.
- Documented that blocked gate results should remain blocked in orchestrator state until fixed or decided by a human.

Validation actions:

- Ran `python agent-skills\orchestrator-state-machine\scripts\validate_orchestrator_state.py tests\fixtures\orchestrator_state_sample.json --json`.
- Ran `git diff --check`.

Direct result:

- Orchestrator state sample validation returned `valid: true`.
- `git diff --check` passed.

---

## 15.15 Atomic Slice: `HOOK-MVP-001-A15`

```text
HOOK-MVP-001-A15: orchestrator state gate result example
```

Scope:

- Add a durable orchestrator state fixture showing how a blocked gate result can appear in the `blocked` queue.
- Add a focused test proving the fixture is accepted by the existing orchestrator state validator.
- Point README readers to the example state artifact.
- Keep this slice example-only: no state persistence helper, no schema enforcement change, no interception.

Acceptance criteria:

- `tests/fixtures/orchestrator_state_gate_result_sample.json` exists.
- The fixture includes a blocked queue item with `atomic_item_id`, `gate`, `gate_status`, `next_allowed_action`, `blocking_reasons`, `validation_artifact`, and `checkpoint_status`.
- The existing orchestrator state validator accepts the fixture.
- `runtime-hooks/README.md` points to the fixture as an example boundary contract.
- Focused orchestrator state tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No durable state mutation or persistence helper.
- No stricter orchestrator state schema.
- No automatic active-item discovery.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `tests/fixtures/orchestrator_state_gate_result_sample.json`.
- Added a focused orchestrator state validator test for the gate-result fixture.
- Added README guidance that the fixture is an example boundary contract.

Validation actions:

- Ran `python -m unittest tests.agent_skills.test_validate_orchestrator_state`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\orchestrator-state-machine\scripts\validate_orchestrator_state.py tests\fixtures\orchestrator_state_gate_result_sample.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused orchestrator state tests reported OK.
- Full test suite reported OK.
- Gate-result state fixture validation returned `valid: true`.
- `git diff --check` passed.

---

## 15.16 Atomic Slice: `HOOK-MVP-001-A16`

```text
HOOK-MVP-001-A16: active item explicit smoke coverage
```

Scope:

- Prove the full runtime hook smoke helper can validate the active atomic item contract example via explicit `--contract`.
- Document the explicit full-smoke command for the active item example.
- Keep this slice to smoke coverage and docs; do not change helper behavior.

Acceptance criteria:

- `tests/runtime_hooks/test_run_runtime_hooks_smoke.py` covers `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json` through explicit contract smoke.
- `runtime-hooks/README.md` documents the full smoke helper command for the active item example.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- The explicit active item smoke CLI returns `status: pass`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added focused smoke coverage for the A13 active item contract example.
- Added README guidance for running the active item example through `run_runtime_hooks_smoke.py --contract`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported OK.
- Full test suite reported OK.
- Explicit active item smoke returned `status: pass`.
- `git diff --check` passed.

---

## 15.17 Atomic Slice: `HOOK-MVP-001-A17`

```text
HOOK-MVP-001-A17: active pre-edit contract example
```

Scope:

- Add a durable `pre-edit` contract example for one active atomic item.
- Show proposed changed files that remain inside allowed scope and outside forbidden scope.
- Document how to validate the active `pre-edit` example.
- Add focused validator coverage for the durable example.
- Keep this slice example-only: no helper behavior change, no contract generation, no interception.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json` exists.
- The example maps `HOOK-MVP-001-A17` to spec reference, allowed scope, forbidden scope, proposed changed files, acceptance criteria, expected artifacts, and validation plan.
- The example's proposed changed files validate against the declared allowed and forbidden scope.
- `runtime-hooks/README.md` points to the active `pre-edit` example and its validator command.
- Focused validator tests pass.
- Full test suite passes.
- The example validates with `validate_gate_contract.py --json`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery or generation.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json`.
- Added focused validator coverage for the active `pre-edit` example.
- Added README guidance for validating the active `pre-edit` example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Full test suite reported OK.
- Active `pre-edit` example returned `status: pass`.
- `git diff --check` passed.

---

## 15.18 Atomic Slice: `HOOK-MVP-001-A18`

```text
HOOK-MVP-001-A18: active post-run contract example
```

Scope:

- Add a durable `post-run` contract example for one active atomic item.
- Show changed files, validation actions, acceptance results, remaining risks, follow-up items, and commit checkpoint state.
- Document how to validate the active `post-run` example.
- Add focused validator coverage for the durable example.
- Keep this slice example-only: no helper behavior change, no contract generation, no interception.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json` exists.
- The example maps `HOOK-MVP-001-A18` to spec reference, allowed scope, forbidden scope, changed files, validation actions, acceptance results, remaining risks, follow-up items, and commit checkpoint state.
- The example validates the `post-run` commit checkpoint shape with an explicit skip reason.
- `runtime-hooks/README.md` points to the active `post-run` example and its validator command.
- Focused validator tests pass.
- Full test suite passes.
- The example validates with `validate_gate_contract.py --json`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery or generation.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json`.
- Added focused validator coverage for the active `post-run` example.
- Added README guidance for validating the active `post-run` example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a18_post_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Full test suite reported OK.
- Active `post-run` example returned `status: pass`.
- `git diff --check` passed.

---

## 15.19 Atomic Slice: `HOOK-MVP-001-A19`

```text
HOOK-MVP-001-A19: active examples combined smoke coverage
```

Scope:

- Prove the full runtime hook smoke helper can validate the active `pre-run`, `pre-edit`, and `post-run` examples together through explicit repeated `--contract`.
- Document the combined active example smoke command.
- Keep this slice to smoke coverage and docs; do not change helper behavior.

Acceptance criteria:

- `tests/runtime_hooks/test_run_runtime_hooks_smoke.py` covers the active `pre-run`, `pre-edit`, and `post-run` examples together.
- The combined smoke result preserves contract order and reports all three gate types.
- `runtime-hooks/README.md` documents the combined active example smoke command.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- The combined active example smoke CLI returns `status: pass`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added focused smoke coverage for the active `pre-run`, `pre-edit`, and `post-run` examples together.
- Added README guidance for running all active examples through repeated `run_runtime_hooks_smoke.py --contract`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --contract runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --contract runtime-hooks\examples\hook_mvp_001_a18_post_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported OK.
- Full test suite reported OK.
- Combined active example smoke returned `status: pass`.
- `git diff --check` passed.

---

## 15.20 Atomic Slice: `HOOK-MVP-001-A20`

```text
HOOK-MVP-001-A20: active example coverage closeout
```

Scope:

- Summarize the current active example coverage after A13 through A19.
- Update safe candidate next slices so future continuation does not restart completed example work.
- Keep this slice documentation-only and suitable as a commit checkpoint.

Current active example coverage:

- `pre-run`: `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json`.
- `pre-edit`: `runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json`.
- `post-run`: `runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json`.
- Combined active smoke: repeated `--contract` validation covers all three examples in order.

What this closes:

- Active examples now cover the three MVP gate types.
- Focused validator tests keep all three durable examples valid.
- Focused smoke tests keep the combined active example workflow valid.
- README contains copyable commands for single-example and combined-example validation.

What remains deferred:

- Runtime interception of tool calls or edit calls.
- Automatic active-item discovery.
- Contract generation or repair.
- Durable orchestrator-state mutation or persistence helpers.
- Policy DSL, complex glob semantics, rule priority, or inheritance.
- Any automatic human-governance decision, scope expansion, commit, revert, or completion claim.

Candidate next slices:

- `HOOK-MVP-001-A21`: design a minimal handoff note format for blocked gate results without writing state.
- `HOOK-MVP-001-A22`: add a blocked active `pre-edit` example to demonstrate scope violation reporting.
- `HOOK-MVP-001-A23`: add README guidance for choosing between sample fixtures, active examples, and future project-specific contracts.
- `RT-FU-001`: continue collecting exact `windows sandbox: spawn setup refresh` observations separately from HOOK-MVP feature work.

Acceptance criteria:

- Backlog summarizes active example coverage after A13 through A19.
- Backlog separates closed coverage from deferred runtime governance work.
- Backlog lists safe next slices without starting them.
- `runtime-hooks/README.md` summarizes active example coverage.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added current active example coverage summary to `runtime-hooks/README.md`.
- Added A20 closeout, deferred work, and candidate next slices to this backlog.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.21 Atomic Slice: `HOOK-MVP-001-A21`

```text
HOOK-MVP-001-A21: blocked gate handoff note format
```

Scope:

- Design a minimal handoff note format for blocked gate results.
- Document when to use the note and what fields it should carry.
- Clarify that a handoff note cannot override a blocked gate, mark completion, or expand scope.
- Keep this slice documentation-only: no state writing, no helper behavior change, no interception.

Acceptance criteria:

- `runtime-hooks/README.md` documents a blocked gate handoff note format.
- The format includes `atomic_item_id`, `gate`, `gate_status`, `blocking_reasons`, `next_allowed_action`, `attempted_command`, `scope_decision_needed`, and `resume_from`.
- README states that the handoff note is not a gate override.
- README states that durable orchestrator state patching remains outside this MVP.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No durable state mutation or persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Blocked Gate Handoff Note` guidance to `runtime-hooks/README.md`.
- Documented minimal handoff fields and boundary rules.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.22 Atomic Slice: `HOOK-MVP-001-A22`

```text
HOOK-MVP-001-A22: blocked active pre-edit example
```

Scope:

- Add a durable blocked `pre-edit` contract example for one active atomic item.
- Demonstrate proposed changed file reporting when a path is outside `allowed_scope`.
- Add focused validator coverage for the blocked example.
- Document how to interpret the blocked example.
- Keep this slice example-only: no helper behavior change, no contract generation, no interception.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json` exists.
- The example returns `status: blocked`.
- The example includes concrete `blocking_reasons` entries for scope violations.
- The example returns `next_allowed_action: handoff`.
- `runtime-hooks/README.md` points to the blocked example and explains expected interpretation.
- Focused validator tests pass.
- Full test suite passes.
- The blocked example CLI returns non-zero structured JSON.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery or generation.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json`.
- Added focused validator coverage for the blocked active `pre-edit` example.
- Added README guidance for interpreting the blocked example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Full test suite reported OK.
- Blocked active `pre-edit` example returned `status: blocked`, `next_allowed_action: handoff`, and concrete allowed / forbidden scope reasons.
- `git diff --check` passed.

---

## 15.23 Atomic Slice: `HOOK-MVP-001-A23`

```text
HOOK-MVP-001-A23: contract type selection guidance
```

Scope:

- Add README guidance for choosing between sample fixtures, active examples, and future project-specific contracts.
- Clarify that sample fixtures are stable smoke inputs and should not be edited to fit project items.
- Keep this slice documentation-only.

Acceptance criteria:

- `runtime-hooks/README.md` describes when to use sample fixtures.
- `runtime-hooks/README.md` describes when to use active examples.
- `runtime-hooks/README.md` describes when to create project-specific contracts.
- README warns not to mutate sample fixtures merely to fit an active project item.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No contract discovery or generation.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Choosing Contract Types` guidance to `runtime-hooks/README.md`.
- Documented the distinction between stable sample fixtures, active examples, and project-specific contracts.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.24 Atomic Slice: `HOOK-MVP-001-A24`

```text
HOOK-MVP-001-A24: runtime hook MVP closeout status
```

Scope:

- Add a concise MVP closeout status to README and backlog.
- Mark the current MVP as ready to pause as a deterministic validation layer.
- Separate the next phase decisions from the completed MVP work.
- Keep this slice documentation-only.

Current MVP closeout status:

- Gate contracts are defined for `pre-run`, `pre-edit`, and `post-run`.
- Deterministic validator checks required fields, simple scope boundaries, blocked reasons, and post-run commit checkpoint shape.
- Environment and full smoke helpers support fresh-clone checks and repeated explicit contracts.
- Active passing examples cover all three gate types.
- Blocked active `pre-edit` example demonstrates scope violation reporting.
- Blocked gate handoff note format exists.
- Orchestrator integration remains documented boundary only; no persistence helper is implemented.

Next decision gate:

- Option A: pause HOOK-MVP-001 here and switch to RT-FU-001 observations or another backlog item.
- Option B: design contract generation, without implementing runtime interception.
- Option C: design orchestrator-state persistence, without implementing tool-call interception.
- Option D: begin a separate spec for real runtime interception / wrapper / daemon.

Acceptance criteria:

- `runtime-hooks/README.md` includes MVP closeout status.
- Backlog includes current MVP closeout status.
- Backlog separates next phase decisions from completed MVP work.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No contract generation.
- No orchestrator-state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Closeout Status` guidance to `runtime-hooks/README.md`.
- Added A24 closeout status and next decision gate to this backlog.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.25 Atomic Slice: `HOOK-MVP-001-A25`

```text
HOOK-MVP-001-A25: runtime hook mounting decision spec
```

Scope:

- Add a mounting decision spec before any runtime hook attachment work.
- Decide the candidate mounting layers and enforcement modes.
- Recommend a conservative first mounting path.
- Keep this slice documentation-only: no wrapper, daemon, CLI integration, state persistence, or interception.

Mounting decision points:

- Mount layer: manual command, PowerShell wrapper, Codex CLI wrapper, orchestrator step, or future daemon.
- First gate to mount: `pre-edit` for hard-block candidate, `post-run` for completion gate, `pre-run` for planning discipline.
- Enforcement mode: advisory check, soft block with handoff, or hard block.
- Blocked output: console JSON, handoff note, orchestrator-state patch proposal, or persisted gate result artifact.
- Human decision boundary: blocked gates require missing information, scope changes, or human decision before continuing.

Recommended first mounting path:

- Start with an orchestrator step or manual command using explicit project-specific contracts.
- Mount `pre-edit` first as a hard-block gate because it can prevent scoped file edits before they happen.
- Emit blocked results as handoff notes first.
- Defer durable state writes until a state patch schema is separately decided.
- Treat Codex CLI wrapper, daemon, and broad tool-call interception as separate specs.

Acceptance criteria:

- `runtime-hooks/README.md` documents the mounting decision spec.
- README states the candidate mount layers.
- README states recommended first gate and enforcement mode.
- README states blocked output options and human decision boundary.
- README preserves the boundary that this MVP validates explicit artifacts only.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No durable state persistence helper.
- No broad tool-call interception.

Implementation log:

Status: completed.

Implemented:

- Added `Mounting Decision Spec` guidance to `runtime-hooks/README.md`.
- Added A25 mounting decision spec and recommended first mounting path to this backlog.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.26 Atomic Slice: `HOOK-MVP-001-A26`

```text
HOOK-MVP-001-A26: mounting readiness checklist
```

Scope:

- Add a checklist for deciding whether a hook mounting path is ready.
- Keep the checklist focused on pre-implementation readiness.
- Keep this slice documentation-only.

Readiness checklist:

- A project-specific gate contract exists for the active item.
- The mount layer is named and intentionally limited.
- The first mounted gate is selected, preferably `pre-edit`.
- Enforcement mode is selected: advisory, soft block, or hard block.
- Blocked output destination is selected.
- Human decision boundary is written down for scope expansion and blocked gates.
- The exact command to rerun after a fix is recorded.
- The mount can be disabled without changing validator helpers.

Acceptance criteria:

- `runtime-hooks/README.md` includes a mounting readiness checklist.
- README says to keep using manual explicit contract validation if readiness is incomplete.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No durable state persistence helper.
- No broad tool-call interception.

Implementation log:

Status: completed.

Implemented:

- Added `Mounting Readiness Checklist` guidance to `runtime-hooks/README.md`.
- Added A26 readiness checklist to this backlog.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.27 Atomic Slice: `HOOK-MVP-001-A27`

```text
HOOK-MVP-001-A27: low-traffic handoff checkpoint
```

Scope:

- Record a low-traffic handoff checkpoint after A13 through A26.
- Preserve the current completed state, verification status, and safe resume options.
- Keep this slice documentation-only and suitable as a stop point.

Current completed state:

- Runtime hook MVP remains a deterministic validation layer, not interception.
- Active examples cover `pre-run`, `pre-edit`, and `post-run`.
- A blocked active `pre-edit` example demonstrates scope violation reporting.
- Full smoke supports repeated explicit `--contract` paths.
- Blocked gate handoff note format is documented.
- Mounting decision spec is documented.
- Mounting readiness checklist is documented.

Recent checkpoint commits:

- `e1019d5 test(runtime-hooks): add blocked pre-edit example`
- `81abf08 docs(runtime-hooks): explain contract type choices`
- `57afe6c docs(runtime-hooks): add mvp closeout status`
- `580cd99 docs(runtime-hooks): define mounting decision spec`
- `1f5dd9f docs(runtime-hooks): add mounting readiness checklist`

Safe resume options:

- Pause HOOK-MVP-001 here and switch to RT-FU-001 observations.
- Create a separate spec for project-specific contract generation.
- Create a separate spec for orchestrator-state persistence.
- Create a separate spec for a real runtime wrapper / daemon / interception layer.
- If continuing mounting work, start with an explicit project-specific `pre-edit` contract and manual/orchestrator-step validation.

Do not resume by directly implementing a broad hook wrapper. The next phase needs a fresh decision gate and a project-specific contract target.

Acceptance criteria:

- Backlog records current completed state after A13 through A26.
- Backlog records safe resume options.
- Backlog warns against directly implementing a broad hook wrapper.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No README changes.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added this low-traffic handoff checkpoint to the backlog.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.28 Atomic Slice: `HOOK-MVP-001-A28`

```text
HOOK-MVP-001-A28: first mounted pre-edit guard
```

Scope:

- Add the first mounted MVP hook as a manual/orchestrator-step `pre-edit` guard.
- Use `pre-edit` as the first mounted hook because it can block scoped file edits before they happen.
- Enforce hard-block semantics from an explicit `pre-edit` gate contract.
- Emit `allowed_to_edit`, `next_allowed_action`, blocking reasons, and a blocked handoff note.
- Keep this slice narrow: no broad wrapper, daemon, Codex CLI integration, durable state writes, or tool-call interception.

Acceptance criteria:

- `runtime-hooks/scripts/enforce_pre_edit_gate.py` exists.
- The guard returns pass for a valid explicit `pre-edit` contract.
- The guard blocks non-`pre-edit` contracts.
- The guard blocks failed `pre-edit` contracts and emits a handoff note.
- The environment smoke check includes the mounted guard helper as a required file.
- `runtime-hooks/README.md` documents the first mounted hook command and boundaries.
- Focused runtime hook tests pass.
- Full test suite passes.
- The guard CLI returns `allowed_to_edit: true` for the active passing `pre-edit` example.
- The guard CLI returns non-zero and `allowed_to_edit: false` for the blocked `pre-edit` example.
- `git diff --check` passes.

Non-goals:

- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Selected first hook:

- `pre-edit`, mounted as a manual/orchestrator-step hard-block guard.

Implemented:

- Added `runtime-hooks/scripts/enforce_pre_edit_gate.py`.
- Added focused tests under `tests/runtime_hooks/test_enforce_pre_edit_gate.py`.
- Updated environment smoke required files to include the mounted guard helper.
- Added README guidance for the first mounted hook command, pass/blocked behavior, handoff note output, and boundaries.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_enforce_pre_edit_gate`.
- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --repo-root . --json`.
- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --repo-root . --json`.
- Ran `git diff --check`.

Direct result:

- Focused mounted guard tests reported 5 tests OK.
- Focused environment tests reported 6 tests OK.
- Full test suite reported 86 tests OK.
- Passing active `pre-edit` guard CLI returned `status: pass`, `allowed_to_edit: true`, and `next_allowed_action: edit`.
- Blocked active `pre-edit` guard CLI returned exit code 1, `status: blocked`, `allowed_to_edit: false`, `next_allowed_action: handoff`, and a handoff note.
- `git diff --check` passed.

---

## 15.29 Atomic Slice: `HOOK-MVP-001-A29`

```text
HOOK-MVP-001-A29: full smoke coverage for mounted pre-edit guard
```

Scope:

- Update the full runtime hook smoke helper so it exercises the first mounted `pre-edit` guard.
- Run the guard when the selected contract set contains a `pre-edit` contract.
- Keep explicit contract smoke flexible: if no `pre-edit` contract is selected, skip the guard instead of blocking.
- Preserve the MVP boundary: no wrapper, daemon, tool-call interception, state mutation, or automatic scope expansion.

Acceptance criteria:

- `run_runtime_hooks_smoke.py` reports a `pre_edit_guard` result when a `pre-edit` contract is selected.
- Default full smoke runs the mounted guard against the sample `pre-edit` contract.
- Explicit smoke with only a `pre-run` contract omits the guard result.
- Explicit smoke with a blocked `pre-edit` contract returns blocked and includes guard blocking reasons.
- README explains that full smoke covers the first mounted hook.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- Full smoke CLI returns `status: pass` and `pre_edit_guard.status: pass`.
- `git diff --check` passes.

Non-goals:

- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Updated `runtime-hooks/scripts/run_runtime_hooks_smoke.py` to load and run the mounted `pre-edit` guard when a selected contract set includes a `pre-edit` contract.
- Added `pre_edit_guard` to smoke output.
- Kept explicit contract smoke flexible by omitting `pre_edit_guard` when no `pre-edit` contract is selected.
- Added focused smoke tests for default guard coverage, explicit skip behavior, and blocked guard behavior.
- Updated README guidance for interpreting `pre_edit_guard` and full smoke coverage.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported 12 tests OK.
- Full test suite reported 87 tests OK.
- Default full smoke returned `status: pass`, `next_allowed_action: ready`, `pre_edit_guard.status: pass`, and `pre_edit_guard.allowed_to_edit: true`.
- Blocked explicit `pre-edit` smoke returned exit code 1, `status: blocked`, `pre_edit_guard.status: blocked`, and `pre_edit_guard.allowed_to_edit: false`.
- `git diff --check` passed.

---

## 15.30 Atomic Slice: `HOOK-MVP-001-A30`

```text
HOOK-MVP-001-A30: blocked pre-edit handoff artifact output
```

Scope:

- Add optional handoff note artifact output to the mounted `pre-edit` guard.
- Write the handoff note only when the guard blocks.
- Keep the handoff artifact separate from durable orchestrator state.
- Keep this as manual/orchestrator-step support only: no wrapper, daemon, tool-call interception, or state mutation.

Acceptance criteria:

- `enforce_pre_edit_gate.py` accepts `--handoff-note-out`.
- A blocked guard writes a JSON handoff note artifact to the requested path.
- A passing guard does not write a handoff note artifact.
- The result includes `handoff_note_path` only when an artifact is written.
- README documents the handoff artifact command and boundary.
- Focused mounted guard tests pass.
- Full test suite passes.
- Blocked guard CLI writes the handoff artifact and returns non-zero.
- `git diff --check` passes.

Non-goals:

- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `--handoff-note-out` to `runtime-hooks/scripts/enforce_pre_edit_gate.py`.
- Added `handoff_note_path` to guard output.
- Wrote blocked handoff notes as UTF-8 JSON artifacts when requested.
- Kept passing guard results from writing handoff artifacts.
- Added focused tests for blocked artifact writing, passing no-write behavior, and CLI artifact output.
- Updated README guidance for blocked handoff artifact output.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_enforce_pre_edit_gate`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --repo-root . --handoff-note-out C:\tmp\hook-mvp-a30-blocked-handoff.json --json`.
- Ran `Test-Path C:\tmp\hook-mvp-a30-blocked-handoff.json`.
- Ran `Get-Content -Raw C:\tmp\hook-mvp-a30-blocked-handoff.json`.
- Ran `git diff --check`.

Direct result:

- Focused mounted guard tests reported 8 tests OK.
- Full test suite reported 90 tests OK.
- Blocked guard CLI returned exit code 1, `status: blocked`, and `handoff_note_path: C:\tmp\hook-mvp-a30-blocked-handoff.json`.
- The handoff artifact existed and contained `atomic_item_id: HOOK-MVP-001-A22`, `gate: pre-edit`, `gate_status: blocked`, and concrete scope blocking reasons.
- `git diff --check` passed.

---

## 15.31 Atomic Slice: `HOOK-MVP-001-A31`

```text
HOOK-MVP-001-A31: repo-root-relative handoff artifact paths
```

Scope:

- Resolve relative `--handoff-note-out` paths from `--repo-root`.
- Preserve absolute handoff output paths.
- Keep passing guard results from writing handoff artifacts.
- Keep this as mounted guard path hygiene only: no wrapper, daemon, tool-call interception, or state mutation.

Acceptance criteria:

- Relative handoff output paths are written under `--repo-root`.
- Absolute handoff output paths still work.
- Focused mounted guard tests pass.
- Full test suite passes.
- README documents repo-root-relative handoff output behavior.
- `git diff --check` passes.

Non-goals:

- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `resolve_handoff_note_path()` to resolve relative handoff output paths from `--repo-root`.
- Preserved absolute handoff output path behavior.
- Added focused test coverage for repo-root-relative handoff artifact output.
- Updated README guidance for deterministic handoff output path behavior.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_enforce_pre_edit_gate`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --repo-root . --handoff-note-out C:\tmp\hook-mvp-a31-absolute-handoff.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused mounted guard tests reported 9 tests OK.
- Full test suite reported 91 tests OK.
- Absolute handoff CLI returned exit code 1, `status: blocked`, and `handoff_note_path: C:\tmp\hook-mvp-a31-absolute-handoff.json`.
- Relative handoff output test wrote under the provided repo root.
- `git diff --check` passed.

---

## 15.32 Atomic Slice: `HOOK-MVP-001-A32`

```text
HOOK-MVP-001-A32: full smoke handoff artifact passthrough
```

Scope:

- Allow the full runtime hook smoke helper to pass a blocked handoff note output path to the mounted `pre-edit` guard.
- Include `pre_edit_guard.handoff_note_path` in smoke output.
- Write the handoff artifact only when the mounted `pre-edit` guard blocks.
- Keep this as smoke-to-guard passthrough only: no wrapper, daemon, tool-call interception, state mutation, or automatic scope expansion.

Acceptance criteria:

- `run_runtime_hooks_smoke.py` accepts `--pre-edit-handoff-note-out`.
- Blocked explicit `pre-edit` smoke writes the handoff artifact through the mounted guard.
- Passing `pre-edit` smoke does not write a handoff artifact.
- Smoke output includes `pre_edit_guard.handoff_note_path`.
- README documents the smoke handoff artifact command and boundary.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- Blocked smoke CLI writes the handoff artifact and returns non-zero.
- `git diff --check` passes.

Non-goals:

- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `--pre-edit-handoff-note-out` to `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Passed the handoff output path through to the mounted `pre-edit` guard.
- Added `pre_edit_guard.handoff_note_path` to smoke output.
- Preserved no-write behavior when the selected `pre-edit` guard passes.
- Recorded the full smoke command in blocked handoff artifacts created through the smoke helper.
- Added focused tests for blocked smoke artifact output, passing no-write behavior, and CLI artifact output.
- Updated README guidance for full smoke handoff artifact output.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --pre-edit-handoff-note-out C:\tmp\hook-mvp-a32-smoke-handoff.json --json`.
- Ran `Get-Content -Raw C:\tmp\hook-mvp-a32-smoke-handoff.json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported 15 tests OK.
- Full test suite reported 94 tests OK.
- Blocked full smoke CLI returned exit code 1, `status: blocked`, and `pre_edit_guard.handoff_note_path: C:\tmp\hook-mvp-a32-smoke-handoff.json`.
- The handoff artifact contained `atomic_item_id: HOOK-MVP-001-A22`, `gate_status: blocked`, concrete scope blocking reasons, and the full smoke attempted command.
- `git diff --check` passed.

---

## 15.33 Atomic Slice: `HOOK-MVP-001-A33`

```text
HOOK-MVP-001-A33: require mounted pre-edit guard in smoke
```

Scope:

- Add an explicit full-smoke option for workflows that require the mounted `pre-edit` guard to run.
- Block when the selected contract set does not include a `pre-edit` contract and the requirement is enabled.
- Keep default full-smoke behavior flexible when the requirement is not enabled.
- Preserve the MVP boundary: no wrapper, daemon, tool-call interception, state mutation, or automatic scope expansion.

Acceptance criteria:

- `run_runtime_hooks_smoke.py` accepts `--require-pre-edit-guard`.
- Smoke with `--require-pre-edit-guard` blocks when no `pre-edit` contract is selected.
- Smoke with `--require-pre-edit-guard` passes when a passing `pre-edit` contract is selected.
- CLI output includes the missing-guard blocking reason.
- README documents when to use the requirement option.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `--require-pre-edit-guard` to `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Added blocking behavior when no `pre-edit` contract is selected while the requirement is enabled.
- Kept default full smoke behavior unchanged when the requirement is not enabled.
- Added focused tests for missing required guard, selected passing guard, and CLI blocking output.
- Updated README guidance for when to use the requirement option.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --require-pre-edit-guard --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_edit_sample.json --require-pre-edit-guard --json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported 18 tests OK.
- Full test suite reported 97 tests OK.
- Missing required `pre-edit` guard CLI returned exit code 1, `status: blocked`, and blocking reason `pre-edit guard required but no pre-edit contract was selected`.
- Selected passing `pre-edit` guard CLI returned `status: pass`, `pre_edit_guard.status: pass`, and `allowed_to_edit: true`.
- `git diff --check` passed.

---

## 15.34 Atomic Slice: `HOOK-MVP-001-A34`

```text
HOOK-MVP-001-A34: require pre-edit contract for smoke handoff output
```

Scope:

- Block full smoke when `--pre-edit-handoff-note-out` is provided but no `pre-edit` contract is selected.
- Prevent manual/orchestrator workflows from thinking a handoff artifact was available when the mounted guard never ran.
- Keep passing and blocked `pre-edit` handoff behavior from A32 unchanged.
- Preserve the MVP boundary: no wrapper, daemon, tool-call interception, state mutation, or automatic scope expansion.

Acceptance criteria:

- Smoke with `--pre-edit-handoff-note-out` and only non-`pre-edit` contracts returns blocked.
- No handoff artifact is written when the required `pre-edit` contract is missing.
- CLI output includes the missing pre-edit handoff output blocking reason.
- Existing blocked `pre-edit` handoff output behavior still works.
- README documents the no-silent-skip behavior.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added blocking behavior when `--pre-edit-handoff-note-out` is provided but no selected contract has `gate: pre-edit`.
- Kept existing blocked `pre-edit` handoff artifact behavior unchanged.
- Added focused tests for function and CLI missing-`pre-edit` handoff output behavior.
- Updated README guidance so handoff output cannot be silently skipped when the guard was not selected.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --pre-edit-handoff-note-out C:\tmp\hook-mvp-a34-missing-handoff.json --json`.
- Ran `Test-Path C:\tmp\hook-mvp-a34-missing-handoff.json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported 20 tests OK.
- Full test suite reported 99 tests OK.
- Missing `pre-edit` handoff output CLI returned exit code 1, `status: blocked`, and blocking reason `pre-edit handoff output requested but no pre-edit contract was selected`.
- No handoff artifact was written for the missing-guard case.
- `git diff --check` passed.

---

## 15.35 Atomic Slice: `HOOK-MVP-001-A35`

```text
HOOK-MVP-001-A35: handoff artifact directory hygiene
```

Scope:

- Add a conventional local output directory for generated blocked handoff artifacts.
- Ignore generated files under `runtime-hooks/handoffs/` while keeping the directory trackable.
- Document that handoff artifacts are local runtime outputs, not durable source state.
- Keep this slice repo hygiene only: no helper behavior changes, wrapper, daemon, tool-call interception, or state mutation.

Acceptance criteria:

- `runtime-hooks/handoffs/.gitignore` exists.
- Generated files under `runtime-hooks/handoffs/` are ignored by Git.
- README documents the generated artifact directory boundary.
- `git diff --check` passes.
- `git check-ignore` confirms a representative handoff JSON path is ignored.

Non-goals:

- No helper behavior changes.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/handoffs/.gitignore`.
- Kept generated handoff artifacts ignored while preserving the directory as a conventional local output target.
- Updated README guidance to clarify that generated handoff artifacts are local runtime outputs, not durable source state.

Validation actions:

- Ran `git diff --check`.
- Ran `git check-ignore -v runtime-hooks\handoffs\blocked-pre-edit.json`.

Direct result:

- `git diff --check` passed.
- `git check-ignore` reported `runtime-hooks/handoffs/.gitignore:2:*` for the representative blocked handoff JSON path.

---

## 15.36 Atomic Slice: `HOOK-MVP-001-A36`

```text
HOOK-MVP-001-A36: first mounted hook closeout
```

Scope:

- Close out the first mounted hook phase after A28 through A35.
- Summarize the mounted gate, mount layer, enforcement mode, pass/blocked behavior, smoke requirement option, handoff artifact output, and ignored local output directory.
- Separate completed mounted guard work from deferred next-phase work.
- Keep this slice documentation-only: no helper behavior changes, wrapper, daemon, tool-call interception, or state mutation.

Current mounted hook state:

- Mounted gate: `pre-edit`.
- Mount layer: manual or orchestrator step.
- Enforcement mode: hard block.
- Passing result: `allowed_to_edit: true`.
- Blocked result: `allowed_to_edit: false`, `next_allowed_action: handoff`, and optional ignored handoff artifact output.
- Full smoke can require the mounted guard with `--require-pre-edit-guard`.
- Generated handoff artifacts under `runtime-hooks/handoffs/` are ignored by Git.

Deferred next-phase work:

- Project-specific contract generation.
- Durable orchestrator-state mutation.
- Real wrapper, daemon, or broad tool-call interception.
- Automatic scope expansion, approval, commit, revert, or completion decisions.

Safe next options:

- Pause HOOK-MVP-001 here after the first mounted hook phase.
- Design project-specific contract generation.
- Design orchestrator-state persistence.
- Start a separate spec for real runtime interception / wrapper / daemon.

Acceptance criteria:

- README includes first mounted hook closeout status.
- Backlog summarizes completed mounted hook state after A28 through A35.
- Backlog separates safe next options from completed work.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added first mounted hook closeout status to `runtime-hooks/README.md`.
- Added A36 closeout summary, current mounted hook state, deferred next-phase work, and safe next options to this backlog.
- Preserved the boundary that the mounted guard is not full runtime interception.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.37 Atomic Slice: `HOOK-MVP-001-A37`

```text
HOOK-MVP-001-A37: first project-specific pre-edit contract target
```

Scope:

- Add the first project-specific `pre-edit` contract target for a concrete atomic item.
- Keep project-specific contracts separate from examples and sample fixtures.
- Validate the target through the mounted `pre-edit` guard and full smoke with `--require-pre-edit-guard`.
- Keep this slice target-only: no contract generator, wrapper, daemon, tool-call interception, or state mutation.

Acceptance criteria:

- `runtime-hooks/contracts/hook_mvp_001_a37_pre_edit_contract.json` exists.
- The contract declares `gate: pre-edit` and `atomic_item_id: HOOK-MVP-001-A37`.
- The contract proposes only the A37 contract, README, and backlog files.
- The mounted `pre-edit` guard returns `status: pass` and `allowed_to_edit: true`.
- Full smoke with `--require-pre-edit-guard` returns `status: pass`.
- README distinguishes project-specific contracts from examples and fixtures.
- `git diff --check` passes.

Non-goals:

- No contract generation helper.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a37_pre_edit_contract.json`.
- Added README guidance distinguishing project-specific contracts from examples and fixtures.
- Added the first project-specific full-smoke command using `--require-pre-edit-guard`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a37_pre_edit_contract.json --repo-root . --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a37_pre_edit_contract.json --require-pre-edit-guard --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and `next_allowed_action: edit`.
- Full smoke returned `status: pass`, `next_allowed_action: ready`, `pre_edit_guard.status: pass`, and `pre_edit_guard.allowed_to_edit: true`.
- Full test suite reported 99 tests OK.
- `git diff --check` passed.

---

## 15.38 Atomic Slice: `HOOK-MVP-001-A38`

```text
HOOK-MVP-001-A38: contracts directory usage guidance
```

Scope:

- Add directory-level guidance for project-specific runtime hook contracts.
- Clarify the difference between `runtime-hooks/contracts/`, sample fixtures, examples, and generated handoff outputs.
- Document the mounted guard and full smoke commands for the first project-specific target.
- Keep this slice documentation-only: no helper behavior changes, generator, wrapper, daemon, tool-call interception, or state mutation.

Acceptance criteria:

- `runtime-hooks/contracts/README.md` exists.
- The contracts README explains when to use project-specific contracts.
- The contracts README includes mounted guard and full smoke validation commands.
- The root runtime hooks README points to the contracts README.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract generation helper.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic scope expansion or human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/README.md`.
- Documented when to use project-specific contracts.
- Documented the mounted guard and full smoke validation commands for the first project-specific target.
- Updated root `runtime-hooks/README.md` to point to the contracts directory guidance.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.39 Atomic Slice: `HOOK-MVP-001-A39`

```text
HOOK-MVP-001-A39: project-specific contract generation design boundary
```

Scope:

- Describe project-specific contract generation as a manual design boundary, not
  an implemented generator.
- Identify the source fields required before drafting a project-specific gate
  contract.
- Require the mounted `pre-edit` guard before editing scoped files from a new
  project-specific contract.
- Keep this slice documentation-only: no helper behavior changes, automatic
  generator, wrapper, daemon, tool-call interception, or state mutation.

Acceptance criteria:

- `runtime-hooks/contracts/README.md` explains the contract generation design
  boundary.
- The contracts README lists the source fields needed before drafting a
  project-specific contract.
- The root runtime hooks README states that contract generation is not
  implemented.
- `runtime-hooks/contracts/hook_mvp_001_a39_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Full smoke with `--require-pre-edit-guard` passes for the A39 contract.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No durable orchestrator-state mutation.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a39_pre_edit_contract.json`.
- Added contract generation design-boundary guidance to
  `runtime-hooks/contracts/README.md`.
- Clarified in `runtime-hooks/README.md` that contract generation is not
  implemented.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a39_pre_edit_contract.json --repo-root . --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a39_pre_edit_contract.json --require-pre-edit-guard --json`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Full smoke returned `status: pass`, `next_allowed_action: ready`,
  `pre_edit_guard.status: pass`, and `pre_edit_guard.allowed_to_edit: true`.
- `git diff --check` passed.

---

## 15.40 Atomic Slice: `HOOK-MVP-001-A40`

```text
HOOK-MVP-001-A40: gate-result state patch proposal boundary
```

Scope:

- Define a state patch proposal shape for handing runtime hook gate results to
  an orchestrator.
- Add a sample patch proposal artifact for a passing `pre-edit` gate.
- Clarify that patch proposals do not mutate durable orchestrator state by
  themselves.
- Preserve orchestrator ownership over workflow cursor advancement, queue
  mutation, human decisions, scope expansion, merge policy, and commit
  checkpoints.

Acceptance criteria:

- `runtime-hooks/README.md` documents the state patch proposal shape.
- `runtime-hooks/contracts/README.md` lists the A40 project-specific contract.
- `runtime-hooks/examples/hook_mvp_001_a40_gate_result_state_patch_proposal.json`
  exists.
- The example patch proposal includes source, gate status, proposed workflow
  step movement, queue patch, validation artifact, checkpoint status, human
  decision status, scope decision status, commit checkpoint note, and boundary
  notes.
- The README states that the runtime hook MVP does not apply the patch.
- `runtime-hooks/contracts/hook_mvp_001_a40_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Full smoke with `--require-pre-edit-guard` passes for the A40 contract.
- The patch proposal JSON parses successfully.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a40_pre_edit_contract.json`.
- Added the A40 contract target to `runtime-hooks/contracts/README.md`.
- Added
  `runtime-hooks/examples/hook_mvp_001_a40_gate_result_state_patch_proposal.json`.
- Added state patch proposal shape guidance to `runtime-hooks/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a40_pre_edit_contract.json --repo-root . --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a40_pre_edit_contract.json --require-pre-edit-guard --json`.
- Ran `python -m json.tool runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Full smoke returned `status: pass`, `next_allowed_action: ready`,
  `pre_edit_guard.status: pass`, and `pre_edit_guard.allowed_to_edit: true`.
- Patch proposal JSON parsed successfully.
- `git diff --check` passed.

---

## 15.41 Atomic Slice: `HOOK-MVP-001-A41`

```text
HOOK-MVP-001-A41: blocked gate-result state patch proposal example
```

Scope:

- Add a blocked state patch proposal example for a blocked `pre-edit` gate.
- Preserve concrete blocking reasons from the blocked gate result in both the
  top-level proposal and proposed blocked queue entry.
- Keep workflow advancement disabled for the blocked proposal.
- Point README readers to both passing and blocked patch proposal examples.
- Keep this slice example/documentation-only: no helper behavior changes,
  automatic state mutation, wrapper, daemon, tool-call interception, or scope
  expansion.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a41_blocked_gate_result_state_patch_proposal.json`
  exists.
- The blocked proposal has `gate_status: blocked` and
  `next_allowed_action: handoff`.
- The blocked proposal has `workflow_step.advance_allowed: false`.
- The blocked proposal includes a `queue_patch` with `to: blocked`.
- The blocked proposal preserves concrete blocking reasons.
- `runtime-hooks/README.md` points to both passing and blocked patch proposal
  examples and states neither applies the patch.
- `runtime-hooks/contracts/README.md` lists the A41 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a41_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Full smoke with `--require-pre-edit-guard` passes for the A41 contract.
- The blocked patch proposal JSON parses successfully.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a41_pre_edit_contract.json`.
- Added
  `runtime-hooks/examples/hook_mvp_001_a41_blocked_gate_result_state_patch_proposal.json`.
- Updated `runtime-hooks/README.md` to point to both passing and blocked patch
  proposal examples.
- Added the A41 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a41_pre_edit_contract.json --repo-root . --json`.
- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --repo-root . --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a41_pre_edit_contract.json --require-pre-edit-guard --json`.
- Ran `python -m json.tool runtime-hooks\examples\hook_mvp_001_a41_blocked_gate_result_state_patch_proposal.json`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- A22 blocked guard returned `status: blocked`, `allowed_to_edit: false`,
  `next_allowed_action: handoff`, and the expected allowed-scope and
  forbidden-scope blocking reasons.
- Full smoke returned `status: pass`, `next_allowed_action: ready`,
  `pre_edit_guard.status: pass`, and `pre_edit_guard.allowed_to_edit: true`.
- Blocked patch proposal JSON parsed successfully.
- `git diff --check` passed.

---

## 15.42 Atomic Slice: `HOOK-MVP-001-A42`

```text
HOOK-MVP-001-A42: state patch proposal validator
```

Scope:

- Add a deterministic validator for runtime hook gate-result state patch
  proposal artifacts.
- Validate required fields, source metadata, workflow step shape, queue patch
  shape, commit checkpoint note, artifact type, patch intent, gate, gate status,
  and basic pass/blocked semantics.
- Add focused tests for passing, blocked, malformed, and semantically mismatched
  proposal artifacts.
- Add the validator to the fresh-clone environment check.
- Document how to run the validator.

Acceptance criteria:

- `runtime-hooks/scripts/validate_state_patch_proposal.py` exists.
- `runtime-hooks/contracts/README.md` lists the A42 project-specific contract.
- The validator accepts the A40 passing patch proposal example.
- The validator accepts the A41 blocked patch proposal example.
- The validator blocks missing required fields.
- The validator blocks a passing proposal that includes blocking reasons.
- The validator blocks a blocked proposal without blocking reasons.
- The validator blocks a blocked proposal that allows workflow advancement.
- Focused validator tests pass.
- The full test suite passes.
- `runtime-hooks/scripts/check_runtime_hooks_environment.py` checks the new
  validator file.
- README documents the validator command and boundary.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a42_pre_edit_contract.json`.
- Added the A42 contract target to `runtime-hooks/contracts/README.md`.
- Added `runtime-hooks/scripts/validate_state_patch_proposal.py`.
- Added `tests/runtime_hooks/test_validate_state_patch_proposal.py`.
- Added the new helper to the runtime hook environment check.
- Documented the state patch proposal validator command in
  `runtime-hooks/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a42_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_state_patch_proposal`.
- Ran `python runtime-hooks\scripts\validate_state_patch_proposal.py runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json`.
- Ran `python runtime-hooks\scripts\validate_state_patch_proposal.py runtime-hooks\examples\hook_mvp_001_a41_blocked_gate_result_state_patch_proposal.json --json`.
- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused state patch proposal validator tests reported 7 tests OK.
- A40 passing patch proposal returned `status: pass` and `gate_status: pass`.
- A41 blocked patch proposal returned `status: pass` and
  `gate_status: blocked`.
- Runtime hook environment tests reported 6 tests OK.
- Full test suite reported 106 tests OK.
- `git diff --check` passed.

---

## 15.43 Atomic Slice: `HOOK-MVP-001-A43`

```text
HOOK-MVP-001-A43: full smoke state patch proposal validation
```

Scope:

- Extend the full smoke helper to accept repeated state patch proposal artifact
  paths.
- Validate selected proposals with
  `runtime-hooks/scripts/validate_state_patch_proposal.py`.
- Include proposal paths and summarized proposal validation results in smoke
  output.
- Keep this as aggregation-only: no patch application, durable state mutation,
  wrapper, daemon, tool-call interception, or automatic scope expansion.

Acceptance criteria:

- `run_runtime_hooks_smoke.py` accepts repeated `--state-patch-proposal`
  arguments.
- Passing and blocked proposal examples can be selected together and return
  summarized `state_patch_proposal_results`.
- Invalid proposal artifacts block full smoke with concrete reasons.
- CLI JSON output includes `state_patch_proposal_paths` and
  `state_patch_proposal_results`.
- Markdown output includes a state patch proposal results section.
- README documents the combined smoke command and boundary.
- `runtime-hooks/contracts/README.md` lists the A43 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a43_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a43_pre_edit_contract.json`.
- Added `--state-patch-proposal` support to
  `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Added state patch proposal paths and result summaries to smoke output.
- Added focused smoke tests for passing proposal selection, invalid proposal
  blocking, CLI JSON output, and markdown output.
- Documented the combined smoke command in `runtime-hooks/README.md`.
- Added the A43 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a43_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a43_pre_edit_contract.json --require-pre-edit-guard --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 22 tests OK.
- Combined A43 smoke returned `status: pass`, `next_allowed_action: ready`,
  `pre_edit_guard.status: pass`, and one passing
  `state_patch_proposal_results` entry.
- Full test suite reported 108 tests OK.
- `git diff --check` passed.

---

## 15.44 Atomic Slice: `HOOK-MVP-001-A44`

```text
HOOK-MVP-001-A44: require state patch proposal in smoke
```

Scope:

- Add an explicit full-smoke option for workflows that require state patch
  proposal validation to run.
- Block when the selected smoke command does not include a state patch proposal
  artifact and the requirement is enabled.
- Preserve optional state patch proposal validation when the requirement is not
  enabled.
- Keep this as smoke gating only: no patch application, durable state mutation,
  wrapper, daemon, tool-call interception, or automatic scope expansion.

Acceptance criteria:

- `run_runtime_hooks_smoke.py` accepts `--require-state-patch-proposal`.
- Smoke with `--require-state-patch-proposal` blocks when no proposal artifact
  is selected.
- Smoke with `--require-state-patch-proposal` passes when a valid proposal
  artifact is selected.
- CLI output includes the missing-proposal blocking reason.
- README documents when to use the requirement option.
- `runtime-hooks/contracts/README.md` lists the A44 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a44_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a44_pre_edit_contract.json`.
- Added `--require-state-patch-proposal` to
  `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Added focused smoke tests for missing and selected required proposal
  validation.
- Documented the requirement option in `runtime-hooks/README.md`.
- Added the A44 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a44_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a44_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a44_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 25 tests OK.
- Required proposal smoke with a selected A40 proposal returned `status: pass`,
  `next_allowed_action: ready`, and one passing
  `state_patch_proposal_results` entry.
- Required proposal smoke without a selected proposal returned exit code 1,
  `status: blocked`, and blocking reason `state patch proposal required but no
  state patch proposal was selected`.
- Full test suite reported 111 tests OK.
- `git diff --check` passed.

---

## 15.45 Atomic Slice: `HOOK-MVP-001-A45`

```text
HOOK-MVP-001-A45: pre-edit guard and proposal consistency smoke
```

Scope:

- Add a consistency check when full smoke requires both the mounted `pre-edit`
  guard and state patch proposal validation.
- Require at least one selected `pre-edit` state patch proposal whose
  `gate_status` matches the mounted guard status.
- Block mismatched guard/proposal status with a concrete reason.
- Keep this as smoke consistency checking only: no patch application, durable
  state mutation, wrapper, daemon, tool-call interception, or automatic scope
  expansion.

Acceptance criteria:

- Smoke passes when a passing `pre-edit` guard is paired with a passing
  `pre-edit` proposal.
- Smoke blocks when a passing `pre-edit` guard is paired only with a blocked
  `pre-edit` proposal.
- Smoke does not add a mismatch reason when a blocked `pre-edit` guard is paired
  with a blocked `pre-edit` proposal.
- CLI combined A45 smoke with a matching A40 proposal passes.
- README documents the consistency check and boundary.
- `runtime-hooks/contracts/README.md` lists the A45 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a45_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a45_pre_edit_contract.json`.
- Added pre-edit guard/proposal status consistency checking to
  `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Added focused smoke tests for matching, mismatched, and blocked matching
  guard/proposal combinations.
- Documented the consistency check in `runtime-hooks/README.md`.
- Added the A45 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a45_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a45_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 28 tests OK.
- A45 matching smoke returned `status: pass`, `next_allowed_action: ready`,
  `pre_edit_guard.status: pass`, and matching `pre-edit/pass`
  `state_patch_proposal_results`.
- Full test suite reported 114 tests OK.
- `git diff --check` passed.

---

## 15.46 Atomic Slice: `HOOK-MVP-001-A46`

```text
HOOK-MVP-001-A46: consistency check output
```

Scope:

- Add machine-readable `consistency_checks` output to full smoke results.
- Report pre-edit guard/state patch proposal consistency pass as a pass check.
- Report pre-edit guard/state patch proposal mismatch as a blocked check.
- Ensure early blocked smoke paths include `consistency_checks: []`.
- Document the new output field.
- Keep this as observability only: no gate semantic changes beyond A45, no patch
  application, durable state mutation, wrapper, daemon, tool-call interception,
  or automatic scope expansion.

Acceptance criteria:

- Full smoke JSON includes `consistency_checks`.
- Matching required pre-edit guard/proposal smoke includes a passing consistency
  check.
- Mismatched required pre-edit guard/proposal smoke includes a blocked
  consistency check and blocking reason.
- Early blocked environment-smoke path includes an empty `consistency_checks`
  list.
- Markdown output includes a consistency checks section.
- README documents the machine-readable consistency check field.
- `runtime-hooks/contracts/README.md` lists the A46 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a46_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a46_pre_edit_contract.json`.
- Added `consistency_checks` to `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Added focused smoke assertions for passing, blocked, and early blocked
  consistency check output.
- Documented `consistency_checks` in `runtime-hooks/README.md`.
- Added the A46 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a46_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a46_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 28 tests OK.
- A46 matching smoke returned `status: pass`, `next_allowed_action: ready`, and
  one passing `consistency_checks` entry with `guard_status: pass`.
- Full test suite reported 114 tests OK.
- `git diff --check` passed.

---

## 15.47 Atomic Slice: `HOOK-MVP-001-A47`

```text
HOOK-MVP-001-A47: proposal source contract consistency
```

Scope:

- Expose state patch proposal source gate contract metadata from the proposal
  validator.
- Include proposal source gate contract and validation artifact metadata in full
  smoke summaries.
- Strengthen the required pre-edit guard/proposal consistency check so a
  matching proposal must reference the selected pre-edit contract, not merely
  match `gate_status`.
- Add a matching A47 passing proposal example and a stale-proposal blocking
  test.
- Keep this as smoke consistency checking only: no patch application, durable
  state mutation, wrapper, daemon, tool-call interception, automatic scope
  expansion, or automatic human-governance decision.

Acceptance criteria:

- State patch proposal validation exposes `source_gate_contract`,
  `validation_artifact`, and `atomic_item_id`.
- Full smoke summarizes proposal source gate contract metadata.
- Required pre-edit guard plus state patch proposal smoke passes when both
  `gate_status` and selected contract source match.
- Required pre-edit guard plus state patch proposal smoke blocks when a stale
  passing proposal points at a different pre-edit contract.
- The blocking reason names the expected selected pre-edit contract.
- `runtime-hooks/contracts/README.md` lists the A47 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused state patch proposal validator tests pass.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json`.
- Added
  `runtime-hooks/examples/hook_mvp_001_a47_gate_result_state_patch_proposal.json`.
- Added proposal metadata output for `atomic_item_id`,
  `source_gate_contract`, and `validation_artifact`.
- Strengthened required pre-edit guard/proposal consistency checking to require
  a matching selected pre-edit contract source.
- Added focused tests for matching source-contract consistency and stale
  proposal blocking.
- Documented the source-contract consistency check in `runtime-hooks/README.md`.
- Added the A47 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a47_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_state_patch_proposal`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a47_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a47_gate_result_state_patch_proposal.json --json`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a47_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused state patch proposal validator tests reported 7 tests OK.
- Focused runtime hook smoke tests reported 29 tests OK.
- A47 matching smoke returned `status: pass`, `next_allowed_action: ready`, and
  a passing `consistency_checks` entry with expected contract path
  `runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json`.
- Stale A40 proposal smoke returned exit code 1, `status: blocked`, and
  blocking reason `state patch proposal does not match selected pre-edit
  contract and guard status:
  runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json`.
- Full test suite reported 115 tests OK.
- `git diff --check` passed.

---

## 15.48 Atomic Slice: `HOOK-MVP-001-A48`

```text
HOOK-MVP-001-A48: matched proposal trace output
```

Scope:

- Add matched proposal trace metadata to passing pre-edit guard/proposal
  consistency checks.
- Report matched proposal path, atomic item ID, source gate contract, and
  validation artifact when a proposal satisfies the selected pre-edit contract.
- Keep blocked consistency checks explicit by leaving matched proposal fields
  empty.
- Keep this as smoke observability only: no patch application, durable state
  mutation, wrapper, daemon, tool-call interception, automatic scope expansion,
  or automatic human-governance decision.

Acceptance criteria:

- Passing pre-edit guard/proposal consistency checks report the matched proposal
  path.
- Passing pre-edit guard/proposal consistency checks report matched proposal
  source metadata.
- Blocked pre-edit guard/proposal consistency checks keep matched proposal
  fields empty.
- `runtime-hooks/contracts/README.md` lists the A48 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a48_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a48_pre_edit_contract.json`.
- Added matched proposal trace metadata to passing
  `pre-edit-guard-state-patch-proposal` consistency checks.
- Kept blocked consistency checks explicit with empty matched proposal fields.
- Documented matched proposal trace output in `runtime-hooks/README.md`.
- Added the A48 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a48_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a47_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a47_gate_result_state_patch_proposal.json --json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 29 tests OK.
- A47 matching smoke returned `status: pass`, `next_allowed_action: ready`, and
  a passing `consistency_checks` entry with `matched_proposal_path`,
  `matched_atomic_item_id`, `matched_source_gate_contract`, and
  `matched_validation_artifact`.
- Full test suite reported 115 tests OK.
- `git diff --check` passed.

---

## 15.49 Atomic Slice: `HOOK-MVP-001-A49`

```text
HOOK-MVP-001-A49: markdown consistency trace output
```

Scope:

- Extend markdown smoke output for consistency checks with expected pre-edit
  contract paths.
- Print matched proposal path, atomic item ID, source gate contract, and
  validation artifact when a consistency check passes.
- Print consistency mismatch reasons in markdown output when a check blocks.
- Keep this as presentation-only smoke output: no JSON semantic expansion, patch
  application, durable state mutation, wrapper, daemon, tool-call interception,
  automatic scope expansion, or automatic human-governance decision.

Acceptance criteria:

- Markdown smoke output reports expected pre-edit contract paths for consistency
  checks.
- Markdown smoke output reports matched proposal trace metadata when a
  consistency check passes.
- Markdown smoke output reports mismatch reasons when a consistency check
  blocks.
- `runtime-hooks/contracts/README.md` lists the A49 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a49_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a49_pre_edit_contract.json`.
- Added markdown consistency-check trace lines for expected contract path,
  matched proposal path, matched atomic item ID, matched source gate contract,
  matched validation artifact, and blocked reasons.
- Added focused markdown smoke tests for passing trace output and blocked reason
  output.
- Documented markdown consistency trace output in `runtime-hooks/README.md`.
- Added the A49 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a49_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\contracts\hook_mvp_001_a47_pre_edit_contract.json --require-pre-edit-guard --require-state-patch-proposal --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a47_gate_result_state_patch_proposal.json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 31 tests OK.
- A47 matching markdown smoke returned `status: pass`, `next_allowed_action:
  ready`, and printed expected contract path plus matched proposal trace fields.
- Full test suite reported 117 tests OK.
- `git diff --check` passed.

---

## 15.50 Atomic Slice: `HOOK-MVP-001-A50`

```text
HOOK-MVP-001-A50: markdown proposal source trace output
```

Scope:

- Extend markdown state patch proposal results with proposal path.
- Print proposal atomic item ID, source gate contract, and validation artifact
  in markdown output.
- Keep this as presentation-only smoke output: no JSON semantic expansion, patch
  application, durable state mutation, wrapper, daemon, tool-call interception,
  automatic scope expansion, or automatic human-governance decision.

Acceptance criteria:

- Markdown state patch proposal results report proposal path.
- Markdown state patch proposal results report atomic item ID.
- Markdown state patch proposal results report source gate contract and
  validation artifact.
- `runtime-hooks/contracts/README.md` lists the A50 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a50_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a50_pre_edit_contract.json`.
- Added markdown state patch proposal result trace lines for proposal path,
  atomic item ID, source gate contract, and validation artifact.
- Added focused markdown smoke coverage for state patch proposal trace output.
- Documented markdown proposal source trace output in `runtime-hooks/README.md`.
- Added the A50 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a50_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --state-patch-proposal runtime-hooks\examples\hook_mvp_001_a40_gate_result_state_patch_proposal.json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 32 tests OK.
- Direct markdown smoke returned `status: pass`, `next_allowed_action: ready`,
  and printed proposal path, `HOOK-MVP-001-A40`, source gate contract, and
  validation artifact.
- Full test suite reported 118 tests OK.
- `git diff --check` passed.

---

## 15.51 Atomic Slice: `HOOK-MVP-001-A51`

```text
HOOK-MVP-001-A51: markdown gate result trace output
```

Scope:

- Extend markdown gate results with validated contract paths.
- Print each gate result `next_allowed_action` in markdown output.
- Keep this as presentation-only smoke output: no JSON semantic expansion, gate
  behavior change, patch application, durable state mutation, wrapper, daemon,
  tool-call interception, automatic scope expansion, or automatic
  human-governance decision.

Acceptance criteria:

- Markdown gate results report validated contract paths.
- Markdown gate results report each gate next allowed action.
- `runtime-hooks/contracts/README.md` lists the A51 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a51_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a51_pre_edit_contract.json`.
- Added markdown gate result trace lines for validated contract path and
  gate-level next allowed action.
- Added focused markdown smoke coverage for gate result trace output.
- Documented markdown gate result trace output in `runtime-hooks/README.md`.
- Added the A51 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a51_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 33 tests OK.
- Direct markdown smoke returned `status: pass`, `next_allowed_action: ready`,
  and printed the validated pre-run contract path plus gate-level
  `next_allowed_action: edit`.
- Full test suite reported 119 tests OK.
- `git diff --check` passed.

---

## 15.52 Atomic Slice: `HOOK-MVP-001-A52`

```text
HOOK-MVP-001-A52: markdown pre-edit guard trace output
```

Scope:

- Extend markdown mounted pre-edit guard output with `allowed_to_edit`.
- Print mounted guard contract path and next allowed action in markdown output.
- Preserve optional handoff note path output when present.
- Keep this as presentation-only smoke output: no JSON semantic expansion, gate
  behavior change, patch application, durable state mutation, wrapper, daemon,
  tool-call interception, automatic scope expansion, or automatic
  human-governance decision.

Acceptance criteria:

- Markdown pre-edit guard output reports `allowed_to_edit`.
- Markdown pre-edit guard output reports mounted guard contract path.
- Markdown pre-edit guard output reports mounted guard next allowed action.
- `runtime-hooks/contracts/README.md` lists the A52 project-specific contract.
- `runtime-hooks/contracts/hook_mvp_001_a52_pre_edit_contract.json` passes the
  mounted `pre-edit` guard.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No durable orchestrator-state mutation.
- No orchestrator state persistence helper.
- No automatic patch application.
- No automatic contract generation, discovery, repair, or scope expansion.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No broad tool-call interception.
- No automatic human-governance decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/contracts/hook_mvp_001_a52_pre_edit_contract.json`.
- Added markdown mounted pre-edit guard trace lines for `allowed_to_edit`,
  contract path, guard-level next allowed action, and optional handoff note path.
- Added focused markdown smoke coverage for mounted pre-edit guard trace output.
- Documented markdown pre-edit guard trace output in `runtime-hooks/README.md`.
- Added the A52 contract target to `runtime-hooks/contracts/README.md`.

Validation actions:

- Ran `python runtime-hooks\scripts\enforce_pre_edit_gate.py runtime-hooks\contracts\hook_mvp_001_a52_pre_edit_contract.json --repo-root . --json`.
- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_edit_sample.json`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Mounted `pre-edit` guard returned `status: pass`, `allowed_to_edit: true`, and
  `next_allowed_action: edit`.
- Focused runtime hook smoke tests reported 34 tests OK.
- Direct markdown smoke returned `status: pass`, `next_allowed_action: ready`,
  and printed mounted pre-edit guard `allowed_to_edit: true`, contract path, and
  guard-level `next_allowed_action: edit`.
- Full test suite reported 120 tests OK.
- `git diff --check` passed.

---

# 16. 長期方向

此方向可能逐步演化為：

- Agent Runtime Governance
- Spec-Driven Execution Runtime
- Skill Dispatch Control Layer
- Multi-Agent Coordination Runtime
- Verification-Centric AI Engineering Workflow

---
