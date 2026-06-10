# PB-FU-004 — 用 OOA / Force / Pattern 視角補強 Drill Down 與 Spec DA

> Status: Draft
> Type: Playbook Foundation Upgrade
> Scope: Spec Drill Down / Spec DA / Proposal Decision
> Purpose: 將軟體設計模式中的 OOA、Forces、Pattern、Pattern Language 等概念，轉譯成可插入 AI Workflow / SDCV 的結構化分析方法。

---

## 1. 核心摘要

這份 Playbook 的目標不是學會完整的設計模式體系，而是把設計模式背後的「思考介面」抽取出來，用來補強既有的 Drill Down、Spec DA 與 Proposal Decision。

重點不在於背誦名詞，而是把名詞當成有固定 I/O 的分析模組：

```text
Requirement
↓
OOA View
↓
Force Analysis
↓
Well-defined Context
↓
Pattern / Proposal Selection
↓
Implementation Form
```

對應到 SDCV / AI Workflow：

```text
Prompt
↓
Spec Drill Down
↓
Spec DA
↓
Proposal Generation
↓
Proposal Decision
↓
Skill / Script / Implementation
```

---

## 2. 這不是新流程，而是補強視角

這份 Playbook 不要求把現有流程推翻重練。

它的定位是：

```text
現有 Drill Down / Spec DA
+
OOA / Force / Pattern Lens
=
更結構化、更可驗證、更可複用的分析流程
```

也就是說，OOA、Force、Pattern 不是新的主流程，而是可以插入既有節點的分析 lens。

---

## 3. 概念映射

| 設計模式語彙 | 在 SDCV / AI Workflow 中的對應 |
|---|---|
| OOA | Spec Drill Down / Domain Modeling |
| Object | 一級公民 / 可被追蹤的核心概念 |
| Actor | 使用者、Agent、系統角色、外部服務 |
| Relationship | 責任、依賴、授權、資料流 |
| Force | Constraint、Gate、Tradeoff、Risk、Fitness Function |
| Well-defined Context | 明確邊界的 Spec / Context Window |
| Pattern | 已驗證的 Proposal / 可重用解法 |
| Pattern Selection | Proposal Decision |
| Pattern Language | Playbook / Skill Catalog / Workflow Composition |
| Form | Script / Code / Agent Action / Runtime Structure |

---

## 4. 為什麼這對 Drill Down 有用

一般 Drill Down 常問：

```text
目標是什麼？
限制是什麼？
成功條件是什麼？
風險是什麼？
```

加入 OOA 視角後，會多問：

```text
系統裡有哪些 Actor？
有哪些核心 Object？
Object 之間有什麼 Relationship？
誰擁有什麼資訊？
誰負責什麼行為？
哪些概念應該被提升為一級公民？
```

這能避免需求分析只停留在文字描述，而沒有形成可設計、可驗證、可演化的結構。

---

## 5. OOA View 的固定 I/O

### Input

```text
Raw Requirement
User Prompt
Existing Spec
Feature Request
Bug Report
Workflow Description
```

### Output

```text
Actors
Objects
Relationships
Responsibilities
Ownership
Missing Domain Concepts
Potential First-class Entities
```

### Transform

```text
從「我要做什麼」
轉換成
「系統中有哪些角色、物件、關係與責任」
```

---

## 6. OOA Drill Down Checklist

在 Spec Drill Down 階段，加入以下問題：

### 6.1 Actor

```text
誰會使用這個系統？
誰會觸發這個流程？
誰會審核結果？
誰會接收輸出？
誰可以中止或回滾？
有哪些外部系統或服務參與？
```

### 6.2 Object

```text
這個需求中有哪些核心物件？
哪些物件需要被追蹤？
哪些物件有生命週期？
哪些物件會被修改？
哪些物件應該成為一級公民？
哪些概念目前只是文字，但其實應該被建模？
```

### 6.3 Relationship

```text
誰依賴誰？
誰擁有誰？
誰批准誰？
誰產生誰？
誰驗證誰？
誰能改變誰的狀態？
哪些關係是同步？哪些關係是非同步？
```

### 6.4 Responsibility

```text
每個 Actor / Object 的責任是什麼？
有沒有責任過度集中？
有沒有責任模糊？
有沒有某個物件同時扮演太多角色？
有沒有該存在但尚未命名的責任單位？
```

---

## 7. 範例：讓 AI 自動修改程式

### Raw Requirement

```text
讓 AI 自動修改程式。
```

### 一般 Drill Down

```text
AI 要修改什麼檔案？
修改依據是什麼？
誰核准？
怎麼驗證？
失敗怎麼 rollback？
```

### OOA Drill Down

```text
Actors:
- Human
- Agent
- Verification Runner
- Version Control System

Objects:
- Spec
- Proposal
- Code Change
- Patch
- Verification Result
- Approval
- Rollback Plan

Relationships:
- Human approves Proposal
- Proposal generates Patch
- Patch modifies Code
- Verification Runner validates Patch
- Verification Result gates Merge
- Rollback Plan restores previous state
```

### 洞察

原本看起來只是：

```text
Agent 修改 Code
```

但經過 OOA 後會發現：

```text
Proposal
Approval
Verification Result
Rollback Plan
```

都可能應該是一級公民，而不是流程中的隱性文字。

---

## 8. Force Analysis 的固定 I/O

Force 的價值在於：不要太快愛上解法，而是先找出真正造成設計壓力的因素。

### Input

```text
OOA Output
Requirement
Constraints
Risks
Tradeoffs
Change Points
Failure Modes
```

### Output

```text
Named Forces
Problem Definition
Design Pressure
Decision Criteria
Proposal Evaluation Basis
```

### Transform

```text
從「我想用什麼解法」
轉換成
「目前真正的設計壓力是什麼」
```

---

## 9. 常見 Force 類型

| Force | 意義 | 可能導向的解法 |
|---|---|---|
| Change Rate | 規則或需求變化頻繁 | Strategy、Rule Engine、Config、Plugin |
| Coupling Pressure | 模組彼此過度依賴 | Interface、Adapter、Observer、Event Bus |
| Context Pollution | Context 容易混雜或污染 | Router、Context Isolation、Scoped Memory |
| Verification Risk | 輸出可能錯誤或不可驗證 | DA、Test、Guardrail、Verifier |
| Ownership Ambiguity | 責任歸屬不清 | Domain Object、Role Boundary、Explicit Contract |
| Lifecycle Complexity | 物件狀態或生命週期複雜 | State Machine、State Pattern、Workflow Engine |
| Repetition | 相似流程重複出現 | Skill、Script、Template、Playbook |
| Human Approval Need | 需要人類決策或授權 | Approval Gate、Proposal Review、Checkpoint |
| Cost Constraint | Token、時間、計算資源有限 | Script First、Caching、Router、Compression |
| Failure Recovery | 失敗後需要恢復 | Rollback、Snapshot、Compensation Action |

---

## 10. Force 對 Proposal Decision 的補強

原本 Proposal Decision 可能比較：

```text
成本
風險
維護性
可擴充性
```

加入 Force 後，每個 Proposal 都必須回答：

```text
這個 Proposal 解決的是哪個 Force？
這個 Force 是否真實存在？
這個 Proposal 是否過度設計？
是否有更小的解法可以處理同一個 Force？
如果 Force 消失，這個 Proposal 是否仍然必要？
```

---

## 11. Proposal Decision Matrix with Force

| Proposal | Declared Force | Evidence | Cost | Risk | Fit | Decision |
|---|---|---|---|---|---|---|
| Router | Context Pollution | 多類任務混在同一 context，造成輸出不穩 | Medium | Medium | High | Accept |
| Skill | Repetition | 同類流程反覆出現，且可抽象成固定 I/O | Medium | Low | High | Accept |
| Hook | Verification Risk | 高風險操作需要前後檢查 | Low | Low | High | Accept |
| Factory | Object Creation Complexity | 目前建立流程尚未複雜 | Medium | Medium | Low | Reject |
| Singleton | Shared Global State | 只是想方便存取，不是真的只能一個 | Low | High | Low | Reject |

---

## 12. Spec DA 加入 OOA / Force 視角

Spec DA 不只檢查「哪裡可能錯」，也要檢查模型是否完整。

### 12.1 OOA DA Questions

```text
是否遺漏 Actor？
是否遺漏 Object？
是否遺漏 Relationship？
是否有錯誤的 Ownership？
是否有未命名但重要的 Domain Concept？
是否有某個 Object 被當成純文字處理，但其實需要被追蹤？
是否有 Actor 被隱含在流程中，但沒有明確權限與責任？
```

### 12.2 Force DA Questions

```text
這個 Force 是否真實存在？
這個 Force 是否只是偏見或想像？
這個 Force 的證據是什麼？
目前選擇的解法是否真的對應這個 Force？
是否用太大的 Pattern 解太小的問題？
是否只是因為看見 if-else 就想套 Strategy？
是否只是因為看到狀態就想套 State Pattern？
是否只是因為想全域存取就套 Singleton？
```

---

## 13. Pattern 的重新定義

在這份 Playbook 中，Pattern 不被視為藝術品，也不是炫技工具。

Pattern 應被視為：

```text
歷史上被多次驗證過的 Proposal
```

也就是：

```text
Repeated Problem
+
Known Forces
+
Reusable Solution Form
=
Pattern
```

因此 Pattern Selection 等價於：

```text
根據 Context / Force 選擇已驗證過的 Proposal
```

而不是：

```text
看到某個表面特徵就套某個模式
```

---

## 14. Pattern Language 對 Playbook 的啟發

Pattern Language 的重點不是單一 Pattern，而是 Pattern 之間如何組合。

對應到 SDCV：

```text
Playbook
↓
Skill
↓
Script
↓
Hook
↓
Verification
```

這其實也是一種 Pattern Language。

重點是：

```text
不是保存每個解法
而是保存解法之間的組合語法
```

---

## 15. 可插入現有流程的位置

### 15.1 OOA 插入 Spec Drill Down

```text
Prompt
↓
Spec Drill Down
   + OOA View
↓
Well-defined Spec
```

### 15.2 Force 插入 Proposal Generation / Decision

```text
Well-defined Spec
↓
Force Analysis
↓
Proposal Generation
↓
Proposal Decision
```

### 15.3 Pattern Language 插入 Playbook / Skill Catalog

```text
Repeated Workflow
↓
Extract Skill
↓
Compose Playbook
↓
Reusable Pattern Language
```

### 15.4 Form 插入 Implementation

```text
Selected Proposal / Pattern
↓
Implementation Form
↓
Script / Code / Agent Action
↓
Verification
```

---

## 16. Mini Workflow

```text
1. 收到 Requirement
2. 用 OOA 拆出 Actor / Object / Relationship
3. 用 DA 檢查是否遺漏重要概念
4. 找出主要 Forces
5. 定義 Well-defined Context
6. 根據 Forces 產生 Proposal
7. 用 Proposal Decision 選最小有效解
8. 必要時映射到 Pattern / Skill / Script
9. 實作成 Form
10. 驗證是否真的解決原始 Force
```

---

## 17. Prompt Template：OOA Drill Down

```text
請用 OOA 視角分析以下需求。

需求：
{{requirement}}

請輸出：
1. Actors：有哪些角色、人、Agent、外部系統？
2. Objects：有哪些核心物件、資料、狀態、產物？
3. Relationships：它們之間有什麼依賴、授權、產生、驗證、修改關係？
4. Responsibilities：每個 Actor / Object 的責任是什麼？
5. Missing Concepts：是否有目前隱含但應該明確建模的概念？
6. First-class Candidates：哪些概念應該被提升為一級公民？
```

---

## 18. Prompt Template：Force Analysis

```text
請針對以下 Spec / OOA 結果進行 Force Analysis。

Spec / OOA：
{{spec_or_ooa}}

請輸出：
1. 主要 Forces：列出造成設計壓力的因素。
2. 每個 Force 的證據：為什麼它真實存在？
3. 可能造成的失敗模式：如果不處理會怎樣？
4. 對應 Proposal：有哪些可能解法？
5. 最小有效解：哪個解法能用最低成本處理核心 Force？
6. 過度設計風險：哪些解法目前不值得採用？
```

---

## 19. Prompt Template：Spec DA with OOA / Force

```text
請扮演 Spec DA，使用 OOA 與 Force 視角挑戰以下設計。

設計內容：
{{design}}

請檢查：
1. 是否遺漏 Actor？
2. 是否遺漏 Object？
3. 是否遺漏 Relationship？
4. 是否有責任歸屬不清？
5. 是否有錯誤的 Ownership？
6. 是否有 Force 沒被處理？
7. 是否有 Proposal 宣稱解決某個 Force，但其實沒有？
8. 是否有過度抽象或過度套用模式？
9. 是否有更小、更直接的解法？
10. 最後請給出修正版建議。
```

---

## 20. Prompt Template：Proposal Decision with Force

```text
請針對以下 Proposal 做 Decision Review。

Context：
{{context}}

Forces：
{{forces}}

Proposals：
{{proposals}}

請輸出表格：
- Proposal
- 對應 Force
- Force 證據
- 解決程度
- 成本
- 風險
- 是否過度設計
- Decision: Accept / Reject / Defer
- Reason

最後請選出最小有效解。
```

---

## 21. 實作準則

### 21.1 不要為了 Pattern 而 Pattern

```text
Bad:
看到 if-else → Strategy
看到狀態 → State Pattern
想全域存取 → Singleton
物件建立 → Factory
```

```text
Good:
Force 成立
↓
Context 明確
↓
Pattern / Proposal 對應
↓
選最小有效解
```

### 21.2 先問 Force，再問 Pattern

```text
不要問：這裡能不能用 Strategy？
要問：這裡的變化點是否真的需要被抽象？
```

```text
不要問：這裡是不是 State Pattern？
要問：這裡是否真的有複雜狀態轉移與狀態行為差異？
```

```text
不要問：這裡是不是要 Factory？
要問：物件建立邏輯是否真的複雜到需要獨立封裝？
```

---

## 22. 一句話原則

> OOA 幫助看見結構，Force 幫助看見設計壓力，Pattern 幫助選擇已驗證解法，Form 幫助落地成可執行實作。

---

## 23. 最小可用版本

若不想導入完整流程，只要先加入兩個檢查點即可。

### 在 Spec Drill Down 加入

```text
Actor / Object / Relationship 是什麼？
```

### 在 Proposal Decision 加入

```text
這個 Proposal 解決什麼 Force？
```

這兩個問題就能吸收本 Playbook 的大部分價值。

---

## 24. Meta：這份 Playbook 的本質

這份 Playbook 是一種跨領域概念蒸餾。

它將軟體設計模式中的：

```text
OOA
Force
Pattern
Pattern Language
Form
```

蒸餾成 SDCV / AI Workflow 可用的：

```text
Drill Down Lens
DA Checklist
Proposal Decision Criteria
Skill Extraction Rule
Implementation Gate
```

也就是：

```text
不是保存每個名詞
而是保存名詞背後的生成規則
```

---

## 25. Recommended Usage

在未來每次做 Spec Drill Down、Spec DA 或 Proposal Decision 時，可以加入以下三句：

```text
1. 用 OOA 看，這裡有哪些 Actor / Object / Relationship？
2. 用 Force 看，真正的設計壓力是什麼？
3. 用 Pattern / Proposal 看，最小有效解是什麼？
```

這就是 PB-FU-004 的核心用法。
