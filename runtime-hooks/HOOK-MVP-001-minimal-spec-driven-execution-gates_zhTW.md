# HOOK-MVP-001 Minimal Spec-Driven Execution Gates

Version: v0.1-draft  
Status: MVP / Experimental  
Category: Runtime Governance  
Related:
- spec-driven-change-verification-workflow-playbook
- preflight-protocol
- devil-advocate-review
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

# 12. 長期方向

此方向可能逐步演化為：

- Agent Runtime Governance
- Spec-Driven Execution Runtime
- Skill Dispatch Control Layer
- Multi-Agent Coordination Runtime
- Verification-Centric AI Engineering Workflow

---
