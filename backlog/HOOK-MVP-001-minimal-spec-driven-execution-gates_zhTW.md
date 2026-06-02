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

# 16. 長期方向

此方向可能逐步演化為：

- Agent Runtime Governance
- Spec-Driven Execution Runtime
- Skill Dispatch Control Layer
- Multi-Agent Coordination Runtime
- Verification-Centric AI Engineering Workflow

---
