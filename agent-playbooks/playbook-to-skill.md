# Playbook To Skill

## 目的

Playbook To Skill 是將 `agent-playbooks/` 中的人類可讀流程規格，整理、對齊或萃取成一個或多個 `agent-skills/<skill-name>/SKILL.md` 的流程。

它的目標是讓 playbook 保留背景、原則、設計意圖與標準 prompt，同時讓 skill 成為短版、命令式、可被 Codex 載入執行的規則。大型 playbook 不應被強行壓成單一巨大 skill；若它包含多個可獨立觸發、執行與驗證的 workflow，應先建立 extraction map，再決定 root/orchestrator skill 與 child skills。

## 核心原則

Playbook 和 skill 不是同一種文件。

Playbook 應保留：

- 流程存在的目的
- 背景脈絡與設計意圖
- 適用與不適用時機
- 人類可讀的標準 prompt
- 建議輸出格式
- 大型 workflow 的階段、脈絡與維護說明

Skill 應保留：

- 清楚的 `name` 與 `description`
- purpose
- trigger conditions
- workflow
- mandatory rules
- boundaries
- validation
- output format

Skill 不應保留：

- 長篇背景故事
- 設計歷史
- 一次性專案脈絡
- 過長範例
- 尚未穩定的想法
- playbook 全文
- 不必要的 README、references、assets、scripts

### Script-first minimization

能用 script 就不用 LLM。

例行 README inventory 與 mapping 檢查應先跑 audit helper：

```powershell
python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json
```

這個 helper 會解析 `agent-playbooks/README.md` 與 `agent-skills/README.md`，檢查 status / profile 是否屬於允許值、對應 playbook / skill 檔案是否存在、`SKILL.md` frontmatter 的 `name` 是否和資料夾名稱一致，並在 skill 有 `scripts/` 但未記錄 Windows 加 Linux/POSIX/macOS invocation coverage 或平台限制時提出 warning。

在 playbook-to-skill 流程中，凡是可由 deterministic command、parser、validator 或檔案讀取確認的事實，應先用工具確認，再讓 LLM 做解讀、比較與決策。

若需要新增 reusable skill script，預設同時支援 Windows 與 Linux。優先使用一份 portable implementation，例如 Python，再用薄 PowerShell / POSIX shell wrapper 改善呼叫體驗；若無法跨平台，必須在 skill 中明確寫出限制與驗證缺口。

優先用 script / command 確認：

- `agent-playbooks/README.md` 與 `agent-skills/README.md` 的 inventory rows
- 對應 playbook / skill 檔案是否存在
- `SKILL.md` frontmatter 是否可解析
- `name` 是否與資料夾名稱一致
- README status 是否屬於允許值
- 有 `scripts/` 的 skill 是否記錄 Windows 與 Linux/POSIX/macOS invocation coverage，或明確記錄平台限制 / validation gap
- one-to-many mapping 是否列出 root skill
- git diff / status 是否只包含預期檔案
- validator / test command 是否通過

LLM 應保留給：

- 判斷 playbook 與 skill 的核心意圖是否一致
- 判斷 workflow、rules、output contract 是否語意對齊
- 評估是否需要 single-skill、multi-skill 或 orchestrator-plus-children
- 產生 extraction strategy、gap analysis 與 human-readable recommendation

## 適用時機

- 已有 playbook，想萃取成一個 Codex skill
- 已有大型 playbook，想拆成 root/orchestrator skill 與多個 child skills
- 已有 playbook 與 skill，想確認兩者是否仍對齊
- playbook 已修改，需要重新同步到對應 skill
- 需要補齊 playbook、skill 與 README 的對照關係
- 需要先建立 extraction map，暫不修改檔案

## 不適用時機

- 只是新增一段普通文件，不需要 Codex 自動載入
- 只是修正 playbook 錯字或小段文字，且不影響 skill 行為
- skill 的行為尚未穩定，仍在快速試驗
- playbook 只是暫時性的專案筆記
- 使用者只要求討論想法，尚未要求建立或修改檔案
- 大型 playbook 的 child skill 邊界仍不清楚，且使用者尚未要求實作；此時應先輸出 assessment 或 extraction map

## Extraction Modes

1. `single-skill`
   - 適用於 playbook 本身是一個清楚、單一、可重複執行的 agent workflow。
   - 輸出一個 `agent-skills/<skill-name>/SKILL.md`。
   - Skill body 應比 playbook 更短、更命令式，不複製 playbook 全文。

2. `multi-skill`
   - 適用於大型 playbook 內含多個可獨立觸發、可獨立執行、可獨立驗證的 workflow。
   - 不應強行壓成單一巨大 skill。
   - 應先建立 extraction map，再決定 root/orchestrator skill、child skills 與 shared skills。

3. `orchestrator-plus-children`
   - 適用於大型 workflow playbook。
   - Root/orchestrator skill 只負責判斷階段、調度子 skill、控制上下文與輸出。
   - Child skills 負責具體可執行動作，例如 preflight、decomposition、review、verification、gate、summary 等。

4. `alignment-check`
   - 適用於已經有 playbook 與 skill，但需要確認兩者是否同步。
   - 應檢查核心意圖、觸發條件、workflow、rules、output contract 與 validation 是否一致。
   - 若只做檢查且沒有修改，應回報差異與建議，不直接改檔。

5. `resync-after-playbook-change`
   - 適用於 playbook 已修改，但對應 skill 尚未同步。
   - 應比較 playbook 的新規則與既有 skill，更新 skill 與 README 狀態。
   - 若 README 狀態因 playbook 先改而被降為 `skill-extracted`，同步檢查完成後才可恢復 `aligned` 或 `aligned-with-followups`。

## Multi-skill Extraction Rule

大型 playbook 如果同時包含多個階段、不同 trigger、不同 output contract、不同驗證規則，應優先考慮 multi-skill extraction。

不應把 playbook 壓成單一 skill 的情境：

- playbook 同時描述多個可單獨啟動的 workflow
- 不同章節需要不同輸出格式或驗證規則
- 某些步驟可在其他任務中重複使用
- 單一 skill 會變得過長，導致 Codex 載入後難以抓住可執行規則
- playbook 包含大量人類維護脈絡、設計理由或標準 prompt

應建立 root/orchestrator skill 的情境：

- 大型流程需要先判斷目前階段，再決定呼叫哪個子流程
- 使用者可能只要求其中一段 child workflow
- root 需要負責上下文控制、輸出整合、狀態檢查或 gating
- 多個 child skills 共享同一份 playbook 的目的、邊界或 README 對照關係

應拆出 child skill 的條件：

- 它有明確且可獨立描述的 trigger
- 它能在不載入整份大型 playbook 的情況下執行
- 它有自己的 workflow、mandatory rules、validation 或 output contract
- 它的責任範圍可用一句話描述
- 它可能被 root skill 或其他 workflow 重複使用
- 它的輸出能交回 root skill 或使用者，且 handoff 清楚

不應拆出 child skill 的情境：

- 該段只是 root workflow 中的一個小檢查點
- 該段沒有獨立 trigger 或獨立 output
- 拆分後會讓 agent 需要讀更多檔案才能做同一件事
- 該段仍是尚未穩定的想法或一次性專案脈絡

Multi-skill extraction 前應先提出 extraction map：

```md
### Extraction Map

| Playbook Section | Proposed Skill | Skill Type | Trigger | Responsibility | Keep In Playbook? |
| --- | --- | --- | --- | --- | --- |
| ... | ... | root / child / shared | ... | ... | yes / no / partial |
```

欄位定義：

- `Playbook Section`：來源章節或規則群。
- `Proposed Skill`：建議的 `agent-skills/<name>/`。
- `Skill Type`：`root`、`child` 或 `shared`。
- `Trigger`：何時載入或執行該 skill。
- `Responsibility`：該 skill 的單一責任。
- `Keep In Playbook?`：背景脈絡是否保留在人類可讀 playbook 中；可用 `yes`、`no` 或 `partial`。

Playbook / skill / README 更新規則：

- 不要把完整 playbook 全文複製進 skill。
- Root skill 應只保留調度、階段判斷、上下文控制與輸出整合規則。
- Child skill 應只保留自己的 trigger、workflow、rules、validation 與 output format。
- Playbook 應保留大型 workflow 的背景、設計理由、完整階段圖、標準 prompt 與 extraction map。
- `agent-playbooks/README.md` 應能表達一份 playbook 對應多個 skills 的關係。
- `agent-skills/README.md` 應列出新增或更新的 root、child、shared skills。
- 若 root skill 已建立但 child skills 尚未全部完成，狀態應標記為 `skill-extracted`，不要標記為 `aligned`。
- 只有 playbook、root skill、child skills 全部複查同步後，才可標記為 `aligned`。

## 工作流程

1. 先用 script-first checks 取得可機械驗證的事實，例如 README rows、檔案存在性、frontmatter、資料夾名稱、狀態值、git diff/status 與 validator 結果。
2. 再閱讀目標 playbook、`agent-playbooks/README.md`、`agent-skills/README.md` 與既有對應 skill。
3. 判斷使用者要的是 assessment、單一 skill、root/orchestrator skill、多個 child skills、extraction map、alignment check，或 playbook change resync。
4. 判斷 extraction mode：`single-skill`、`multi-skill`、`orchestrator-plus-children`、`alignment-check` 或 `resync-after-playbook-change`。
5. 若使用者沒有明確要求修改檔案，先輸出 assessment 與 extraction strategy，不直接改檔。
6. 若 playbook 過大或包含多個獨立 workflow，先提出 extraction map，不直接建立單一巨大 skill。
7. 視需要補齊 playbook 的目的、核心原則、適用時機、不適用時機、Agent 行為規則、標準 Prompt 與建議輸出格式。
8. 判斷哪些內容應保留在 playbook，哪些內容應萃取到 root、child 或 shared skill。
9. 建立或更新 `agent-skills/<skill-name>/SKILL.md`。
10. 確認每個 skill 使用短版、命令式、可執行的規則。
11. 若新增 reusable skill script，確認 Windows 與 Linux invocation 都有文件，且路徑處理避免硬編碼單一 OS separator。
12. 確認每個 skill frontmatter 只包含必要的 `name` 與 `description`。
13. 更新 `agent-playbooks/README.md` 與 `agent-skills/README.md` 的對照表與狀態。
14. 若有 skill validator，執行驗證；若沒有，做手動結構檢查。

## Playbook 整理規則

整理 playbook 時，agent 應：

- 保留人類可讀的背景與設計理由
- 補齊適用時機與不適用時機
- 讓標準 Prompt 可以直接複製使用
- 讓 Agent 行為規則比標準 Prompt 更精準
- 避免把 playbook 寫成只有單一任務適用
- 避免把 skill frontmatter 或過度工具化的內容放入 playbook
- 若要拆成多個 skills，保留 extraction map 與 root/child 分工說明

## Skill 萃取規則

萃取 skill 時，agent 應保留：

- `name`
- `description`
- purpose
- trigger conditions
- workflow
- mandatory rules
- boundaries
- validation
- output format

萃取 skill 時，agent 不應保留：

- 長篇背景故事
- 設計歷史
- 一次性專案脈絡
- 過長範例
- 尚未穩定的想法
- playbook 全文
- 不必要的 README、references、assets、scripts

萃取規則：

- 使用與 playbook 對應的短小 hyphen-case 名稱。
- 在 `description` 中寫清楚用途與觸發情境。
- 將背景說明壓縮成一小段 purpose。
- 將流程改寫成命令式 workflow。
- 將限制改寫成 rules。
- 只保留 agent 執行時必要的輸出格式。
- 對大型 playbook，優先拆分 root/orchestrator skill 與 child skills，而不是產生單一巨大 skill。
- 避免產生不必要的 README、references、assets 或 scripts。

## README 狀態規則

更新 `agent-playbooks/README.md` 的 Playbook / Skill 對照表時，agent 應使用以下狀態語義：

- `draft`：只有 playbook，尚未穩定。
- `skill-extracted`：已從 playbook 萃取出 skill，但尚未完成整體同步複查。
- `aligned`：playbook 與所有對應 skills 已複查並同步。
- `aligned-with-followups`：playbook 與所有對應 skills 已複查並同步，且仍可照常使用；但 playbook 內有已記錄的 proposed follow-up backlog，未來可另開 resync / refinement。
- `deprecated`：不建議繼續使用。

Multi-skill 情境：

- 若一份 playbook 對應多個 skills，README 對照表應能表達一對多關係。
- Skill 欄可列出 root skill 與 child skills；root/orchestrator skill 應放在最前。
- 若 child skills 很多，可在 README 表格使用簡短列表，並在 playbook 內保留完整 extraction map。
- 若 root skill 已建立但 child skills 尚未全部完成，狀態應標記為 `skill-extracted`。
- 只有 playbook、root skill、child skills 全部複查同步後，才可標記為 `aligned`。
- 若 playbook 已修改但 skill 尚未同步，狀態應從 `aligned` 調整為 `skill-extracted`。
- 若 playbook 只新增非阻塞 follow-up backlog，且沒有改變現行 workflow、trigger、rules、output contract 或 skill extraction map，可標記為 `aligned-with-followups`，不必降回 `skill-extracted`。
- 若 follow-up backlog 已被實作並同步到對應 skills，狀態可恢復為 `aligned`；若 follow-up 需要但尚未同步的 skill 行為變更，則應降為 `skill-extracted`。
- 若只建立 extraction map 而尚未建立 skill，通常仍維持 `draft`，除非已有部分 skills 存在。

## Agent 行為規則

agent 在執行 playbook-to-skill 時，應先判斷使用者要的是：

1. 只評估 playbook 是否適合萃取成 skill
2. 建立或更新單一 skill
3. 建立 root/orchestrator skill
4. 建立多個 child skills
5. 建立 extraction map 但暫不修改檔案
6. 檢查 playbook 與既有 skill 是否同步
7. 將已修改 playbook 重新同步到 skill

若使用者沒有明確要求修改檔案，應先輸出 assessment 與 extraction strategy，不要直接改檔。

執行 assessment、alignment check 或 resync 時，應先跑可用的 deterministic checks。不要讓 LLM 憑印象推斷 inventory row、檔案存在、frontmatter 合法性、status 值、git diff 或 validator 結果。

若 playbook 過大或包含多個獨立 workflow，agent 不應直接建立單一巨大 skill，應先提出 multi-skill extraction map。

若使用者要求萃取 skill，agent 應在修改後驗證：

- skill 是否有合法 frontmatter
- skill `description` 是否足以觸發正確情境
- skill body 是否短版、命令式、可執行
- playbook 與 skill 是否保留相同核心意圖
- root/orchestrator skill 與 child skills 的責任是否清楚
- `agent-playbooks/README.md` 與 `agent-skills/README.md` 對照表是否需要更新

## 標準 Prompt

請協助將這份 playbook 整理、對齊或萃取成 Codex skill。

請先檢查 playbook 是否符合 `agent-playbooks/README.md` 的風格與結構，再判斷 extraction mode：

- `single-skill`
- `multi-skill`
- `orchestrator-plus-children`
- `alignment-check`
- `resync-after-playbook-change`

請注意：

1. 若 playbook 是單一穩定 workflow，可以建立或更新一個 `agent-skills/<skill-name>/SKILL.md`
2. 若 playbook 過大或包含多個獨立 workflow，不要直接壓成單一巨大 skill
3. 若需要 multi-skill extraction，先提出 extraction map
4. Root/orchestrator skill 只負責階段判斷、調度、上下文控制與輸出整合
5. Child skills 只負責具體可執行動作與各自的 validation / output contract
6. Skill 必須短版、命令式、可執行，不複製 playbook 全文
7. 依狀態定義更新 Playbook / Skill 對照表
8. 若有 validator，請執行驗證

## 建議輸出格式

### Playbook Assessment

目前 playbook 的狀態：

- ...

### Extraction Mode

建議模式：

- single-skill / multi-skill / orchestrator-plus-children / alignment-check / resync-after-playbook-change

### Extraction Strategy

建議萃取策略：

- ...

### Extraction Map

| Playbook Section | Proposed Skill | Skill Type | Trigger | Responsibility | Keep In Playbook? |
| --- | --- | --- | --- | --- | --- |
| ... | ... | root / child / shared | ... | ... | yes / no / partial |

### Files To Change

預計影響的檔案：

- ...

### README Updates

需要更新的對照表：

- ...

### Validation

需要執行或已執行的驗證：

- ...

### Open Questions

需要確認的地方：

- ...
