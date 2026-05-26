# Agent Playbooks

`agent-playbooks/` 存放 personal-ai-runtime 中給人類與 agent 共同閱讀的流程規格。

Playbook 描述一個工作流程的目的、原則、適用場景、行為規則與建議輸出。它不是短版技能指令，也不是單次 prompt 集合；當某個 playbook 需要被 Codex 自動載入與執行時，再從 playbook 萃取成 `agent-skills/<skill-name>/SKILL.md`。

## Playbook 的角色

Playbook 應回答：

- 這個流程要解決什麼問題
- 什麼時候應該使用
- 什麼時候不應該使用
- agent 在執行前應該先判斷什麼
- 哪些行為必須避免
- 建議使用什麼 prompt 或輸出格式
- 若要萃取成 skill，哪些規則需要保留

Playbook 可以保留背景脈絡與設計意圖；skill 應只保留 agent 執行時必要的短規則。

## 建議結構

新的 playbook 建議使用以下結構，並依實際需求刪減：

```md
# Playbook Name

## 目的

說明這個流程要解決的問題，以及它存在的原因。

## 核心原則

列出不隨專案變動的判斷原則。

## 適用時機

列出應該啟用這個流程的情境。

## 不適用時機

列出不需要啟用這個流程，或啟用後容易過度處理的情境。

## 檢查項目 / 格式原則 / 工作流程

依 playbook 類型選擇合適名稱，列出 agent 或人類需要檢查的事項。

## Agent 行為規則

說明 agent 應該做什麼、避免什麼，以及何時需要先詢問使用者。

## 標準 Prompt

提供一段可直接交給 agent 的中文 prompt。

## 建議輸出格式

定義 agent 回報結果時建議使用的章節。
```

## 寫作風格

- 以繁體中文撰寫，保留必要的英文術語，例如 `CHANGELOG.md`、release history、commit log、tag、API。
- 使用明確、可執行的句子，避免只寫抽象理念。
- 優先描述判斷規則，而不是描述某一次任務的結果。
- 條列應短而具體，讓 agent 能直接轉成行動。
- 標準 Prompt 可以比較口語；行為規則應更精準。
- 不要把大量實作細節、歷史原因或臨時討論塞進 playbook。
- 不要把 playbook 寫成只能用於單一專案或單一日期的紀錄。

## 與 Skill 的關係

Playbook 與 skill 應保持以下分工：

- `agent-playbooks/<name>.md`：人類可讀的流程說明，保留目的、背景、原則與標準 prompt。
- `agent-skills/<name>/SKILL.md`：agent 執行時載入的短版規則，包含 frontmatter、觸發描述、workflow、rules、輸出格式。

從 playbook 萃取 skill 時，應保留核心意圖與限制，但改寫成命令式、精簡、可執行的規則。

Skill 不應只是複製 playbook 全文。若 playbook 有背景說明、設計理由或較長範例，通常應留在 playbook，不放進 `SKILL.md`。

大型 playbook 可以對應多個 skills。此時 root/orchestrator skill 應負責階段判斷、調度與輸出整合，child skills 則負責可獨立觸發、執行與驗證的子流程。Playbook 應保留完整 extraction map；README 對照表可在 Skill 欄列出 root skill 與必要的 child/shared skills，root skill 應放在最前。

## 狀態定義

| 狀態 | 意義 |
|---|---|
| `draft` | 只有 playbook，尚未穩定 |
| `skill-extracted` | 已從 playbook 萃取出 skill |
| `aligned` | playbook 與 skill 已複查並同步 |
| `deprecated` | 不建議繼續使用 |

若一份 playbook 對應多個 skills，只有 playbook、root skill、child skills 與 shared skills 全部複查同步後，才可標記為 `aligned`。若 root skill 已建立但 child skills 尚未全部完成，或 playbook 修改後 skill 尚未重新同步，狀態應維持或調整為 `skill-extracted`。

## Playbook / Skill 對照表

| Playbook | Skill | 狀態 | 說明 |
|---|---|---|---|
| `preflight-protocol.md` | `preflight-protocol/` | `aligned` | 任務開始前的理解、假設、不確定處、風險與下一步檢查 |
| `scope-control.md` | - | `draft` | 執行中控制任務範圍，避免未要求功能與過度修改 |
| `completion-check.md` | - | `draft` | 完成後根據成功標準驗收結果並回報殘餘風險 |
| `changelog-normalization.md` | `changelog-normalization/` | `aligned` | 將 changelog 草稿或混合紀錄整理成穩定 release history |
| `playbook-to-skill.md` | `playbook-to-skill/` | `aligned` | 將人類可讀 playbook 萃取成單一或多個短版、命令式 Codex skills，並支援 alignment / resync |
| `prompt-to-playbook.md` | `prompt-to-playbook/` | `aligned` | 將一次性 prompt、成功案例或重複任務指令整理成可維護 playbook |
| `personal-ai-assistant-bootstrap.md` | - | `draft` | 建立或更新個人 AI 分身資料層，包含資料夾骨架、入口規則、記憶、private context 引用與 skill 候選整理 |
| `chat-to-note.md` | - | `draft` | 將聊天回答、AI 草稿或貼上的 Markdown 片段整理成乾淨、可維護且保留來源邊界的 note |
| `spec-driven-change-verification-workflow-playbook.md` | `spec-driven-change-verification/` + child skills | `aligned` | 以 spec、diff、mutation testing、atomic orchestration 與人工決策控制程式、測試和規格的共同演進；root skill 與 child skills 已依 extraction map 複查同步 |
| `external-source-to-playbook.md` | - | `draft` | 將 `external-source/` 中的外部來源整理成帶有來源、license 與 attribution 資訊的 playbook |
| `external-source-repo-import.md` | - | `draft` | 將外部 Git repository 匯入 `external-source/`，建立 metadata、notes、extracted、upstream 與 `.gitignore` 規則 |
| `external-source-copyright-notice-review.md` | - | `draft` | 補查外部來源中非標準 license 檔的版權、授權、重用與公開分享限制 notice |
| `external-source-to-rag-source.md` | - | `draft` | 將 `external-source/` 來源轉成帶有 rights、license manifest 與處理紀錄的 RAG source workspace |
| `nested-module-git-initialization.md` | `nested-module-git-initialization/` | `aligned` | 整理 `modules/` 或 `poc-modules/` 子專案時檢查獨立 Git 邊界，必要時執行 `git init` |
| `release-preflight.md` | - | `draft` | 發版、tag、README、CHANGELOG 與 Git 狀態檢查流程 |
| `utf8-traditional-chinese-defaults.md` | `utf8-traditional-chinese-defaults/` | `aligned` | 文件讀寫預設 UTF-8、繁體中文優先，並在 PowerShell 文字輸出時明確使用 `-Encoding UTF8` |

## 命名

- 檔名使用小寫英文與 hyphen，例如 `preflight-protocol.md`。
- 名稱應描述流程本身，而不是一次性任務。
- 若未來會萃取成 skill，playbook 檔名應盡量與 skill 資料夾名稱一致。

## 維護原則

- 修改 skill 前，先檢查對應 playbook 是否也需要更新。
- 修改 playbook 後，檢查對應 skill 是否仍符合核心原則。
- 若 playbook 逐漸變成可重複執行的 agent 工作流程，應考慮萃取成 skill。
- 若內容只是暫時性的專案筆記，不應放入 `agent-playbooks/`。
