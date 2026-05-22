# Codex 版：AI 分身資料層初始化

> 對齊來源：`pro-kit/01-agent-folder-setup.md`
> 原始定位：給 Claude Code 跑的「AI 分身起始助手 by 雷小蒙」
> Codex 改寫定位：建立 Codex / 多 AI 都能讀懂的可攜資料層、規則層、記憶層與技能層。

## 改寫原則

這份文件不是逐字翻譯，而是把 Claude Code 版的執行意圖轉成 Codex 可操作流程：

- Claude 的 `CLAUDE.md` 對應到 Codex 的 `AGENTS.md`，並建議抽出 AI 無關母規則 `000_Agent/CORE_RULES.md`。
- Claude 的 `AskUserQuestion` 對應到 Codex 的簡短逐題訪談；在 Default 模式下，若答案可從上下文合理推斷，就保守執行。
- Claude 的 `Write` / `Edit` 對應到 Codex 的「先讀再改」，文件編輯優先用 `apply_patch`，PowerShell 讀寫要指定 UTF-8。
- Claude 的 `~/.claude/skills` symlink 對應到「可選的跨工具映射」；Codex 的主體資料仍放在專案可見的 `000_Agent/skills/`。
- 原始檔案一律不動，只寫入 `external-source/claude-code-mini-course/extracted/pro-kit/` 或使用者指定的目標工作區。

## Claude → Codex 步驟對齊

| Claude 原 section | 原始核心意圖 | Codex 對應做法 |
| --- | --- | --- |
| Section A：角色與需求訪談 | 先理解使用者角色、主要工作、內容平台與是否需要日記，再決定資料夾 | 用逐題中文訪談或合理預設取得同樣四類資訊；結果寫入初始化紀錄 |
| A-1 確認目錄 | 先定義 AI 分身母資料夾，之後所有操作以此為根 | 確認 workspace / mother path；若在既有 repo，避免在錯誤路徑建資料層 |
| A-2 AskUserQuestion 四題 | 用低負擔選項框收斂需求 | Codex 沒有該工具時改用短問題；不要一次問太多自由題 |
| Section B：建立資料夾結構 | 建 000/100/200/300 主骨架，避免新手照抄過多空資料夾 | 建立同樣主骨架，並說明每層如何被 Codex 使用 |
| B-1.5 README 說明卡 | 空資料夾要有說明，避免使用者迷路 | 在 `skills/`、`workflows/` 寫入 Codex 可攜說明卡 |
| B-5 Skills symlink | 讓 Claude 原生 skill 讀取位置指向專案可見資料夾 | 改成可選跨工具映射；Codex 優先讀 `000_Agent/skills/`，Claude 使用者才處理 symlink |
| Section C：接管 CLAUDE.md / MEMORY.md | 建立規則與記憶，且絕不覆蓋既有檔 | 建立 / 追加 `AGENTS.md`、`000_Agent/CORE_RULES.md`、`MEMORY.md`；保留 `CLAUDE.md` 作為相容層 |
| C-1 重疊偵測 | 防止同義規則重複吃 context | Codex 先掃描既有規則，重疊則只追加缺漏或註明不重複 |
| C-3 daily log | 讓初始化本身被記錄 | 建立 `000_Agent/memory/daily/YYYY-MM-DD.md` |
| Section D 明天作業 | 引導使用者餵作品與建立第一個 skill | Codex 版保留：放入過去作品、下一輪建立 skill |
| Section E 自驗清單 | 最後檢查資料夾、規則、記憶、placeholder | Codex 跑 PowerShell / shell 檢查；確認 UTF-8 與未替換 placeholder |

## Section A：角色與需求訪談

### A-1. 確認母資料夾

先確認資料層要建立在哪裡。可給使用者三個選項：

1. 本機簡單版：`~/Documents/my-agent/`
2. 雲端同步版：iCloud / Dropbox / Google Drive / OneDrive 底下的 `my-agent/`
3. 既有專案版：使用目前 repo 根目錄

Codex 執行注意：

- 在 Windows / PowerShell 內處理路徑時，使用實際絕對路徑並避免混用 WSL 路徑。
- 若目前是 repo，先跑 `git status --short`，只新增目標檔，不碰無關變更。
- 若使用者沒指定，且目前 workspace 已是明確專案，預設在目前 workspace 建資料層。

### A-2. 取得四組需求答案

逐題確認：

1. 主要角色：內容創作者 / 創業者 / 上班族顧問 / 自由工作者 / 其他。
2. AI 最常幫忙的事：寫作、研究、規劃會議、知識管理、其他。
3. 主要產出平台：社群、長文、Email、影音、其他。
4. 是否啟用每日反思 / 日記。

若使用者不想回答，Codex 採保守預設：

- 建核心 `000_Agent/`、`100_Todo/`、`200_Reference/`
- 不建 `300_Journal/`
- 只建通用 drafts / references，不預判太多平台子資料夾

### A-3. 回述與執行承諾

在建立檔案前，用一句話回述：

```text
我會依你的角色與產出平台，建立可攜的 Codex 資料層：資料夾骨架、AGENTS.md / CORE_RULES.md、MEMORY.md、daily log，以及後續建立 skill 的起點。
```

## Section B：建立資料夾結構

### B-1. 核心骨架

固定建立：

```text
000_Agent/
  skills/
  workflows/
  memory/
    daily/
  knowledge/
100_Todo/
  drafts/
  projects/
  archive/
200_Reference/
  writing-samples/
  past-work/
  templates/
```

各層用途：

- `000_Agent/`：AI 協作核心，放規則、記憶、skills、workflows、工具知識。
- `100_Todo/`：正在做的事，包含草稿、專案、待歸檔成果。
- `200_Reference/`：讓 AI 學你的參考素材，包含過去作品、語氣範例、模板。
- `300_Journal/`：可選，放每日反思與個人時序紀錄。

### B-2. 日記資料夾

若使用者選擇啟用：

```text
300_Journal/YYYY-MM/
```

同時在 `AGENTS.md` / `CORE_RULES.md` 加入：

```markdown
- 若使用者要求 session 收尾或每日反思，將整理內容寫入 `300_Journal/YYYY-MM/`。
```

### B-3. 依平台建立子資料夾

只依使用者實際勾選建立，不要全部預建：

| 平台 | drafts | references |
| --- | --- | --- |
| 社群 | `100_Todo/drafts/social-posts/` | `200_Reference/writing-samples/social/` |
| 長文 | `100_Todo/drafts/articles/` | `200_Reference/writing-samples/articles/` |
| Email | `100_Todo/drafts/emails/` | `200_Reference/writing-samples/emails/`、`200_Reference/templates/email-templates/` |
| 影音 | `100_Todo/drafts/scripts/` | `200_Reference/writing-samples/scripts/` |

### B-4. 空資料夾說明卡

`000_Agent/skills/README.md`：

```markdown
# skills/ - AI 工作手冊

這裡放可重複使用的任務 SOP。每個子資料夾是一個 skill，至少包含 `SKILL.md`。

每份 skill 建議說清楚：
- 何時使用
- 需要讀哪些資料
- 執行步驟
- 輸出格式
- 驗證方式
- 迭代紀錄
```

`000_Agent/workflows/README.md`：

```markdown
# workflows/ - 固定多步驟流程

workflow 是你會主動觸發的一整套流程，例如晨間整理、週報、發文前檢查。

skill 是方法；workflow 是把多個方法串起來的儀式。
```

### B-5. Skills 路徑與 symlink

Codex 版預設不強制建立 `~/.claude/skills` symlink。原因：

- Codex 可以直接讀工作區內的 `000_Agent/skills/`。
- symlink 涉及使用者全域工具設定，風險比單純建專案檔高。
- 若使用者也使用 Claude Code，才執行相容設定。

相容策略：

1. 偵測 `~/.claude/skills` 是否存在。
2. 若不存在且使用者同意，建立 symlink 指向 `000_Agent/skills/`。
3. 若已存在且有內容，先備份或詢問是否合併，不可覆蓋。
4. 若已是 symlink，確認 target 是否正確。

## Section C：建立規則與記憶

### C-1. 建立 AI 無關母規則 `CORE_RULES.md`

建議新增：

```text
000_Agent/CORE_RULES.md
```

內容骨架：

```markdown
# AI 分身核心規則

## 協作方式

- 預設用繁體中文與使用者溝通。
- 修改檔案前先讀相關上下文。
- 不覆蓋使用者既有內容；需要整合時先追加或詢問。
- 草稿輸出優先放到 `100_Todo/drafts/` 或使用者指定位置。
- 需要模仿語氣時，先讀 `200_Reference/writing-samples/`。

## 資料路由

- `000_Agent/`：規則、記憶、skills、workflows、工具知識
- `100_Todo/`：正在做的事與草稿
- `200_Reference/`：學習素材與模板
- `300_Journal/`：每日反思（若啟用）

## 自我進化

- 使用者糾正偏好時，寫入 `000_Agent/memory/MEMORY.md`。
- 同錯誤重複兩次以上，建議升級到規則檔。
- 流程重複三次以上，主動建議整理成 skill 或 workflow。
```

### C-2. 建立 / 更新 `AGENTS.md`

Codex 的入口是 `AGENTS.md`。若不存在，建立：

```markdown
# AGENTS.md

請先閱讀 `000_Agent/CORE_RULES.md`，並依其中的資料路由、記憶與自我進化規則協作。
```

若已存在，追加邊界區塊：

```markdown
<!-- AI 分身起始助手紀錄:START -->

請先閱讀 `000_Agent/CORE_RULES.md`。
本專案的 AI 協作資料層位於：

- `000_Agent/`
- `100_Todo/`
- `200_Reference/`

<!-- AI 分身起始助手紀錄:END -->
```

重跑時：

- 若已有 START / END，詢問是否更新該區塊。
- 若沒有邊界標記，追加到最後。
- 若發現同義規則已存在，不重複追加；在 daily log 記錄「略過重疊規則」。

### C-3. `CLAUDE.md` 相容層

若使用者仍使用 Claude Code，可建立：

```markdown
# CLAUDE.md

請先閱讀 `000_Agent/CORE_RULES.md`。
```

若已有 `CLAUDE.md`，不可覆蓋，只追加相容提示。

### C-4. 建立 `MEMORY.md`

位置：

```text
000_Agent/memory/MEMORY.md
```

內容：

```markdown
# AI 分身記憶

> 跨 session 的偏好、回饋、踩坑與環境速查。

## 使用者偏好

（待累積）

## Feedback

（待累積）

## 踩坑筆記

（待累積）

## 環境速查

| 項目 | 值 |
| --- | --- |
| AI 分身母資料夾 | `待填` |
| 建立日期 | `YYYY-MM-DD` |
| Codex 入口 | `AGENTS.md` |
| 母規則 | `000_Agent/CORE_RULES.md` |
```

若已存在，追加「初始化紀錄」區塊，不清空原記憶。

### C-5. Daily log

建立：

```text
000_Agent/memory/daily/YYYY-MM-DD.md
```

初始內容：

```markdown
# YYYY-MM-DD Session Log

## 今天做了什麼

- 跑了 Codex 版 AI 分身資料層初始化。
- 建立 `000_Agent/` / `100_Todo/` / `200_Reference/`。
- 建立或更新 `AGENTS.md` / `CORE_RULES.md`。
- 建立 `MEMORY.md` 與 daily log。

## 下一步

- 把 5-10 份過去作品放入 `200_Reference/writing-samples/`。
- 挑一個高頻任務整理成第一個 skill。
```

## Section D：使用者作業

Codex 完成初始化後，保留原文的核心作業：

1. 餵過去作品：把好文章、email、提案、腳本放進 `200_Reference/`。
2. 建第一個 skill：優先挑每天或每週高頻重複任務。
3. 重開 session：讓 Codex 在新 session 中讀到 `AGENTS.md`。

Codex 版提醒：

```text
今天先不要急著建更多資料夾。資料層的價值來自真實素材與真實工作流，而不是空架構。
```

## Section E：完成檢查

執行後檢查：

- `000_Agent/skills/README.md` 存在
- `000_Agent/workflows/README.md` 存在
- `000_Agent/CORE_RULES.md` 存在
- `AGENTS.md` 存在，且有起始助手邊界區塊或引用 `CORE_RULES.md`
- `000_Agent/memory/MEMORY.md` 存在
- `000_Agent/memory/daily/YYYY-MM-DD.md` 存在
- 若啟用日記，`300_Journal/YYYY-MM/` 存在
- 沒有未替換 placeholder：`[用戶名字]`、`[YYYY-MM-DD]`、`[Q1]`
- upstream 原始檔沒有變動

## Codex 執行口徑

完成時用短訊息告訴使用者：

- 建了哪些資料夾
- 規則入口是哪個檔案
- 記憶檔在哪裡
- 下一步要放哪些參考素材
- 若也使用 Claude Code，是否已建立相容層或需要另行處理 symlink
