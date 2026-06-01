# Prompt To Playbook

## 目的

Prompt To Playbook 是將一次性 prompt、成功案例、重複出現的任務指令，整理成 `agent-playbooks/<name>.md` 的流程。

它的目標是把臨時、局部、容易散落在對話中的操作經驗，抽象成可重複維護的人類可讀 playbook。

## 核心原則

一次性 prompt 不是 playbook。

Playbook 應保留：

- 流程要解決的問題
- 可重複使用的判斷原則
- 適用與不適用時機
- agent 應遵守的行為規則
- 可直接複製使用的標準 prompt
- 建議輸出格式

Prompt To Playbook 只負責把臨時 prompt 抽象成 playbook。除非使用者明確要求，否則不應繼續萃取成一般任務 skill。

## 適用時機

- 使用者提供一段成功的一次性 prompt，想保存成可重複流程
- 同一類任務指令在多次對話中反覆出現
- 某個操作流程已逐漸穩定，但尚未整理成 playbook
- 需要把對話中的經驗、決策規則或檢查清單整理成 `agent-playbooks/<name>.md`
- 需要先建立 playbook，之後再視需要萃取成 skill

## 不適用時機

- 只是要執行一次 prompt，不需要保存流程
- 只是要修改既有 playbook 的少量文字
- 內容仍高度不穩定，尚無法抽象成通用流程
- 使用者明確要求直接建立一般任務 skill
- 臨時 prompt 涉及敏感資料、一次性環境或不可泛化的專案細節

## 整理規則

整理 prompt 時，agent 應先判斷：

1. 這段 prompt 想解決什麼重複問題
2. 哪些內容是一次性背景，哪些內容可抽象成流程
3. 哪些條件代表應該使用這個流程
4. 哪些條件代表不應該使用這個流程
5. 哪些規則是 agent 執行時必須遵守的
6. 哪些輸出格式能讓結果穩定、可檢查
7. playbook 檔名應如何命名

agent 應移除或改寫：

- 只對單次任務有效的稱呼、日期、檔名或環境細節
- 過度依賴當次對話上下文的句子
- 未經確認的假設
- 會讓 agent 自動做超出 playbook 範圍行為的指令

agent 應保留或抽象：

- 成功 prompt 的核心意圖
- 可重複使用的判斷標準
- 需要先詢問使用者的條件
- 需要避免的行為
- 已被證明有效的輸出章節

## Agent 行為規則

agent 在執行 prompt-to-playbook 時，應先判斷使用者要的是：

1. 只分析 prompt 是否適合成為 playbook
2. 建立新的 playbook
3. 更新既有 playbook
4. 將多個 prompt 合併成同一個 playbook

若目標 playbook 位於本機 `agent-playbooks/`，應先用 deterministic 檢查取得來源檔、目標路徑、README 對照列、既有狀態與 mapped skill 證據；再判斷 prompt 是否值得抽象、如何泛化，以及是否需要更新 README 狀態。

若使用者只要求建立 playbook，不應自動建立一般任務 skill。

若新建立的 playbook 不存在於 `agent-playbooks/README.md` 的 Playbook / Skill 對照表中，agent 應加入新列，Skill 欄位填 `-`，狀態標記為 `draft`。

若更新的 playbook 已存在於對照表，且已對應 skill，agent 應將狀態調整為 `skill-extracted`，表示 playbook 已變更但尚未重新複查同步。

若 prompt 內容不足以抽象成通用流程，agent 應先提出缺口或建議範圍，而不是硬寫成規範。

若 prompt 包含專案特定細節，agent 應將它們改寫成條件、範例或待確認事項，避免讓 playbook 只適用於單一情境。

## 標準 Prompt

請協助將以下一次性 prompt、成功案例或重複任務指令整理成 playbook。

請將它抽象成 `agent-playbooks/<name>.md`，並符合 `agent-playbooks/README.md` 的風格與結構。

請注意：

1. 只建立或更新 playbook
2. 不要自動萃取成一般任務 skill
3. 保留可重複使用的目的、原則、適用時機與行為規則
4. 移除或泛化只屬於單次任務的細節
5. 補上標準 Prompt 與建議輸出格式
6. 如有必要，更新 `agent-playbooks/README.md` 的對照表
7. 新增 playbook 時標記為 `draft`
8. 修改已對應 skill 的 playbook 時，先將狀態調整為 `skill-extracted`

## 建議輸出格式

### Prompt Assessment

目前 prompt 的可抽象程度：

- ...

### Proposed Playbook

建議建立或更新的 playbook：

- ...

### Generalized Rules

已抽象出的通用規則：

- ...

### Removed Or Generalized Details

已移除或泛化的一次性細節：

- ...

### Files To Change

預計影響的檔案：

- ...

### Open Questions

需要確認的地方：

- ...
