# Personal AI Assistant Bootstrap

## 目的

這份 playbook 用來建立或更新個人 AI 分身資料層，讓 Codex、Claude Code 或其他 agent 能用同一套可攜資料夾理解使用者的規則、記憶、參考素材與後續 skill 候選。

它適合把一次性的「幫我建立個人數位分身」對話，整理成可重複執行的流程：先建立資料層，再記錄 private context 的引用方式，最後把未來可能萃取成 skill 的項目先沉澱成 playbook。

## 核心原則

- 先確認目標母資料夾，再建立任何資料層檔案。
- 預設採保守骨架，不預判使用者平台、職業或日記需求。
- 規則、記憶、參考素材與工作草稿要分層放置，避免混在同一個資料夾。
- private context 只記錄路徑與使用規則，不複製、摘要或外洩私人內容。
- 若某個流程預期未來會變成 skill，先建立 playbook 並標記為 `draft`，除非使用者明確要求，否則不直接萃取 skill。
- 文件讀寫使用 UTF-8；中文內容預設使用繁體中文。

## 適用時機

- 使用者要求建立「個人 AI 分身」、「個人數位分身」或可跨 agent 使用的資料層。
- 使用者指定一個目標資料夾，想把規則、記憶、參考素材與草稿路由固定下來。
- 使用者提供 private context 路徑，想讓 agent 在需要個人脈絡時參照。
- 初始化流程中出現未來可能建立 skill 的任務，例如高頻寫作流程、研究流程、反思流程或資料整理流程。
- 需要把成功的初始化對話整理成可維護 playbook，之後再視穩定度萃取成 skill。

## 不適用時機

- 使用者只是要建立一般專案資料夾，沒有 agent 規則、記憶或 skill 候選需求。
- 使用者明確要求直接建立 Codex skill，而不是先整理 playbook。
- 目標內容高度私人且使用者不允許記錄路徑或規則。
- 使用者只要一次性整理檔案，不需要跨 session 的資料層。
- 既有資料層規則衝突嚴重，且無法從上下文判斷應保留哪一套規則。

## 工作流程

1. 讀取來源規格或既有資料層文件，例如初始化說明、`AGENTS.md`、`CORE_RULES.md`、`MEMORY.md`。
2. 確認目標母資料夾；若目標在 sandbox 可寫範圍外，先請求使用者允許外部寫入。
3. 檢查目標資料夾是否已存在，並讀取既有入口檔，避免覆蓋使用者內容。
4. 若使用者沒有提供角色、常用任務、主要平台與日記偏好，採保守預設：只建立核心骨架，不啟用日記，不預建平台子資料夾。
5. 建立或確認核心骨架：
   - `000_Agent/skills/`
   - `000_Agent/workflows/`
   - `000_Agent/memory/daily/`
   - `000_Agent/knowledge/`
   - `100_Todo/drafts/`
   - `100_Todo/projects/`
   - `100_Todo/archive/`
   - `200_Reference/writing-samples/`
   - `200_Reference/past-work/`
   - `200_Reference/templates/`
6. 建立或更新入口與規則文件：
   - `AGENTS.md` 作為 Codex 入口。
   - `000_Agent/CORE_RULES.md` 作為 AI 無關母規則。
   - `CLAUDE.md` 作為 Claude Code 相容層（若適用）。
   - `000_Agent/memory/MEMORY.md` 作為跨 session 記憶。
   - `000_Agent/memory/daily/YYYY-MM-DD.md` 作為初始化紀錄。
7. 若使用者提供 private context 路徑，只在規則與記憶中加入路徑引用與使用邊界，不讀取或複製內容，除非使用者明確要求。
8. 檢查初始化過程中是否有預期建立 skill 的項目：
   - 若只是模糊提醒，例如「挑一個高頻任務」，先保留為下一步，不硬寫成 skill。
   - 若已有可重複流程或成功案例，使用 `prompt-to-playbook` 流程在 `agent-playbooks/` 建立 draft playbook。
   - 更新 `agent-playbooks/README.md` 對照表，Skill 欄填 `-`，狀態填 `draft`。
9. 驗證必要檔案存在、UTF-8 讀寫正常、沒有未替換 placeholder，並確認來源規格或無關工作區沒有被修改。

## Agent 行為規則

- 修改檔案前先讀相關上下文；已存在的 `AGENTS.md`、`CORE_RULES.md`、`MEMORY.md` 不可直接覆蓋。
- 對既有檔案追加時，使用邊界標記或清楚章節，避免重複寫入同義規則。
- 不要建立全平台、全職業、全工作流的空資料夾；只有使用者指定或上下文足夠明確時才建立細分資料夾。
- 不要自動建立 `~/.claude/skills` symlink；涉及全域工具設定時需先取得使用者同意。
- 不要把 private context 的內容搬到一般資料層、playbook、skill 或回覆中。
- 若寫入 Windows 路徑中的 Markdown，注意 PowerShell 反引號跳脫問題，避免把 Markdown code span 寫壞。
- 若要把預期 skill 項目落地，先建 playbook；只有使用者明確要求「萃取成 skill」時，才進一步修改 `agent-skills/`。

## 標準 Prompt

請依下列資訊建立或更新我的個人 AI 分身資料層，並把未來可能萃取成 skill 的穩定流程先整理成 playbook。

請遵守：

1. 目標母資料夾：`<target-root>`。
2. 來源規格：`<source-spec-or-existing-rules>`。
3. private context 路徑（可選）：`<private-context-path>`。
4. 預設用繁體中文與 UTF-8。
5. 先讀既有檔案，不覆蓋使用者內容。
6. 若沒有足夠偏好資訊，採保守骨架，不預建平台子資料夾，也不啟用日記。
7. private context 只記錄引用路徑與使用邊界，不複製內容。
8. 如果流程中出現預期建立 skill 的項目，請先在 `agent-playbooks/` 建立或更新 playbook，並在 README 對照表標記為 `draft`；不要直接建立 skill，除非我明確要求。
9. 完成後回報建立了哪些資料夾、入口檔、記憶檔、playbook 與驗證結果。

## 建議輸出格式

### 建立結果

- 目標母資料夾：
- 建立或更新的核心資料夾：
- 建立或更新的入口檔：

### Private Context

- 是否登記 private context 路徑：
- 是否讀取或複製 private context 內容：

### Skill 候選與 Playbook

- 發現的 skill 候選：
- 新增或更新的 playbook：
- README 對照表狀態：

### 驗證

- 必要檔案檢查：
- placeholder / NUL 檢查：
- 未修改的來源或無關檔案：

### 下一步

- 建議放入的參考素材：
- 適合下一輪整理成 skill 的高頻任務：
