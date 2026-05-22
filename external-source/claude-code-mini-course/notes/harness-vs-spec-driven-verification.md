# Harness 與 Spec-Driven Change Verification 對照筆記

## 來源與使用限制

- Primary local source workspace: `external-source/claude-code-mini-course/`
- Related open reference: `external-source/learn-claude-code/`
- Internal reference: `agent-playbooks/spec-driven-change-verification-workflow-playbook.md`
- Note type: private external-source reading note / workflow comparison

`claude-code-mini-course` 的來源工作區標記為 restricted paid-course material。這份筆記只保留高階理解、個人對照與後續萃取方向；不要複製課程原文、範例細節或可替代原課程材料的內容。

若後續要把這份筆記萃取成公開 playbook、skill、prompt 或 knowledge，需先確認來源權利與 attribution 邊界。

## 核心理解

Claude Code 類工具可以從兩層來看：

```text
model agency
  -> 模型本身的理解、推理、規劃與行動能力

harness
  -> 讓模型能觀測環境、使用工具、執行動作、受到權限限制與保存工作脈絡的工程層
```

多數應用開發者實際上不是在訓練 agent，而是在建構 agent harness。

可用一個簡化公式理解：

```text
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions
```

模型負責推理與決策；harness 決定模型能看見什麼、能做什麼、如何被限制、如何被驗證，以及什麼時候需要人類介入。

## 與 Spec-Driven Verification 的關係

`spec-driven-change-verification-workflow` 可以定位成 coding agent harness 裡的治理層與驗證層。

它不是要替模型寫死所有行動，而是提供一組工作環境規則：

```text
Spec clarity
  -> Plan challenge
  -> Atomic decomposition
  -> Implementation
  -> Diff-aware verification
  -> Mutation review
  -> Human governance
  -> Spec / test evolution
```

也就是說，spec-driven workflow 不是 agent 本身，而是讓 agent 在修改程式、測試與文件時能被 correctness contract、驗證結果與 human decision 約束的 harness component。

## 對照表

| Harness component | Spec-driven workflow 對應 |
|---|---|
| Tools | test runner、mutation testing、diff analysis、JIT test suggestion |
| Knowledge | `SPEC.md`、playbook、skill、外部來源筆記、project conventions |
| Observation | git diff、test result、mutation survived、risk / gap、review feedback |
| Action Interfaces | implement atomic item、update spec、補 test、提出 decision proposal |
| Permissions | scope control、human decision gate、breaking change 停下來、禁止未授權擴大範圍 |

這個對照可以幫助區分：

- 模型能力：理解任務、推理方案、產生候選修改
- harness 能力：提供工具、限制權限、保存規格、驗證結果、要求決策
- governance 能力：判斷何時可繼續、何時要停下來、何時要更新 spec

## 最重要的交集：Atomic Task

Harness 設計強調工具與行動應該 atomic、可組合、描述清楚。

Spec-driven workflow 也採用類似概念：

```text
main workflow
  -> workflow slices
  -> selected workflow
  -> atomic implementation items
```

每個 atomic item 應小到可以：

- 單獨實作
- 單獨測試
- 單獨 review
- trace back 到 spec reference、acceptance criteria、error condition 或 risk item

整理成一句話：

> Harness 提供 agent 能行動的世界；atomic workflow 定義 agent 每次行動的最小安全單位。

## Skill Loading 的啟發

Skill loading 的核心啟發是：不要把所有規則、知識與背景一次塞進 prompt，而是讓 agent 在需要時載入相關能力。

這可以對應到 personal-ai-runtime 的分工：

```text
agent-playbooks/
  人類可讀，保留背景、設計意圖、流程脈絡

agent-skills/
  agent 可載入，保留短版、命令式、可執行規則
```

因此 spec-driven workflow 不一定要變成單一巨大 skill。它可以拆成多個可按需載入的技能或流程：

- preflight-protocol
- spec-drill-down
- devils-advocate-review
- workflow-atomic-decomposition
- diff-analysis
- jit-test-suggestion
- mutation-result-review
- human-decision-proposal

這讓 agent harness 更接近 modular capability loading，而不是單一超大 system prompt。

## Protocols 的啟發

Team / collaboration protocols 的價值在於把協作變成可追蹤的狀態機，而不是一句「問人一下」。

對應到 spec-driven workflow，human decision gate 可以視為 protocol：

```text
gap found
  -> classify gap
  -> propose options
  -> request human decision
  -> update spec / tests / implementation
  -> rerun verification
```

這裡的重點不是人類手動驗證所有細節，而是人類治理 correctness：

- 是否接受 behavior change
- 是否更新 spec
- 是否拒絕 change
- 是否要求補測試
- 是否拆分 scope

## Devil's Advocate 在 Harness 裡的位置

Devil's Advocate Review 可以視為 harness 裡的風險觀測器與計畫閘門。

它應在 plan / spec 定稿前挑戰：

- 隱含假設
- 過度設計
- edge cases
- 架構衝突
- migration risk
- 測試成本
- spec / implementation 脫鉤風險
- readable output 是否被誤當成 verified truth

這一層不直接產生功能，而是提高後續實作與驗證的可信度。

## 可萃取方向

這份筆記後續可萃取成：

- harness glossary：定義 tools、knowledge、observation、action interface、permission boundary
- coding-agent verification harness checklist
- spec-driven workflow 的 harness framing 小節
- human decision protocol playbook
- atomic item execution checklist
- skill loading 與 playbook / skill 分層規則

目前不建議直接萃取成公開 skill，因為 `claude-code-mini-course` 來源有使用限制。若萃取內容主要來自 open reference 或個人重新表述，仍應保留 attribution 與來源邊界說明。

## 一句話總結

Claude Code 類工具提醒我們：多數時候，我們不是在寫 agent 的 intelligence，而是在寫 agent 的 harness。

`spec-driven-change-verification-workflow` 則可以定位成：

> 一套讓 coding agent 在修改程式時，能被 spec、test、diff、mutation result 與 human decision 約束的 verification harness。

它的價值不是限制模型變笨，而是讓模型的行動有邊界、有證據、有回饋、有治理。

