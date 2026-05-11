# Playbook To Skill

## 目的

Playbook To Skill 是將 `agent-playbooks/` 中的人類可讀流程規格，萃取成 `agent-skills/<skill-name>/SKILL.md` 的整理流程。

它的目標是讓 playbook 保留背景、原則與標準 prompt，同時讓 skill 成為短版、命令式、可被 Codex 載入執行的規則。

## 核心原則

Playbook 和 skill 不是同一種文件。

Playbook 應保留：

- 流程存在的目的
- 背景脈絡與設計意圖
- 適用與不適用時機
- 人類可讀的標準 prompt
- 建議輸出格式

Skill 應保留：

- 清楚的 `name` 與 `description`
- 觸發情境
- agent 必須執行的 workflow
- agent 必須遵守的 rules
- 必要的輸出格式

## 適用時機

- 已有 playbook，想萃取成 Codex skill
- 已有 skill，想確認是否仍對齊 playbook
- playbook 已逐漸變成可重複執行的 agent 工作流程
- 需要補齊 playbook 與 skill 的對照關係
- 需要把一次性 prompt 整理成可維護的 playbook，再萃取成 skill

## 不適用時機

- 只是新增一段普通文件，不需要 Codex 自動載入
- 只是修正 playbook 錯字或小段文字
- skill 的行為尚未穩定，仍在快速試驗
- playbook 只是暫時性的專案筆記
- 使用者只要求討論想法，尚未要求建立或修改檔案

## 工作流程

1. 先閱讀目標 playbook 與 `agent-playbooks/README.md`
2. 判斷 playbook 是否符合目前資料夾的風格與結構
3. 視需要補齊 playbook 的目的、核心原則、適用時機、不適用時機、Agent 行為規則、標準 Prompt 與建議輸出格式
4. 判斷哪些內容應保留在 playbook，哪些內容應萃取到 skill
5. 建立或更新 `agent-skills/<skill-name>/SKILL.md`
6. 確認 skill 使用短版、命令式、可執行的規則
7. 確認 skill frontmatter 只包含必要的 `name` 與 `description`
8. 若有 skill validator，執行驗證
9. 更新 `agent-playbooks/README.md` 的 Playbook / Skill 對照表

## Playbook 整理規則

整理 playbook 時，agent 應：

- 保留人類可讀的背景與設計理由
- 補齊適用時機與不適用時機
- 讓標準 Prompt 可以直接複製使用
- 讓 Agent 行為規則比標準 Prompt 更精準
- 避免把 playbook 寫成只有單一任務適用
- 避免把 skill frontmatter 或過度工具化的內容放入 playbook

## Skill 萃取規則

萃取 skill 時，agent 應：

- 使用與 playbook 對應的短小 hyphen-case 名稱
- 在 `description` 中寫清楚用途與觸發情境
- 將背景說明壓縮成一小段 purpose
- 將流程改寫成命令式 workflow
- 將限制改寫成 rules
- 只保留 agent 執行時必要的輸出格式
- 避免複製 playbook 全文
- 避免產生不必要的 README、references、assets 或 scripts

## 狀態更新規則

更新 `agent-playbooks/README.md` 的 Playbook / Skill 對照表時，agent 應使用以下狀態語義：

- `draft`：只有 playbook，尚未穩定
- `skill-extracted`：已從 playbook 萃取出 skill
- `aligned`：playbook 與 skill 已複查並同步
- `deprecated`：不建議繼續使用

剛完成 skill 萃取時，狀態應標為 `skill-extracted`。

只有在重新複查 playbook 與 skill，並確認兩者內容同步後，才應標為 `aligned`。

## Agent 行為規則

agent 在執行 playbook-to-skill 時，應先判斷使用者要的是：

1. 只整理 playbook
2. 只建立或更新 skill
3. 同時整理 playbook 並萃取 skill
4. 檢查 playbook 與 skill 是否對齊

若使用者只要求先建立 playbook，不應自動建立 skill。

若使用者要求萃取 skill，agent 應在修改後驗證：

- skill 是否有合法 frontmatter
- skill `description` 是否足以觸發正確情境
- skill body 是否短版、命令式、可執行
- playbook 與 skill 是否保留相同核心意圖
- `agent-playbooks/README.md` 對照表是否需要更新

## 標準 Prompt

請協助將這份 playbook 萃取成 Codex skill。

請先檢查 playbook 是否符合 `agent-playbooks/README.md` 的風格與結構，再判斷哪些內容應保留在 playbook，哪些內容應放入 `agent-skills/<skill-name>/SKILL.md`。

請建立或更新對應 skill，並確保：

1. playbook 保留人類可讀的目的、原則與標準 prompt
2. skill 使用短版、命令式、可執行的規則
3. skill frontmatter 包含清楚的 `name` 與 `description`
4. 不產生不必要的附屬文件
5. 驗證 skill 結構
6. 依狀態定義更新 Playbook / Skill 對照表

## 建議輸出格式

### Playbook Assessment

目前 playbook 的狀態：

- ...

### Extraction Strategy

建議萃取策略：

- ...

### Skill Structure

預計建立或更新的 skill：

- ...

### Files To Change

預計影響的檔案：

- ...

### Validation

需要執行或已執行的驗證：

- ...

### Open Questions

需要確認的地方：

- ...
