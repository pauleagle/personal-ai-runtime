# Codex 版：跨裝置同步與 AI 大腦可攜化

> 對齊來源：`pro-kit/07-cross-device-sync.md`
> 原始定位：把 Claude Code 的 settings、skills、memory 等搬到可見母體資料夾，透過 symlink / GitHub / 雲端同步變成可攜資產。
> Codex 改寫定位：建立多 AI 可攜資料層，讓 Codex、Claude Code、Gemini CLI 或未來工具都能讀同一份核心規則、記憶與技能。

## 核心意圖

07 的重點不是「同步」本身，而是「不要讓 AI 分身綁死在某個工具的隱藏資料夾」。

Codex 版保留三層目的：

1. **可見**：規則、記憶、skills 放在使用者看得到的資料夾。
2. **可備份**：GitHub / 雲端 / 本機備份能保護資料。
3. **可遷移**：換電腦或換 AI 工具時，能用 symlink 或入口檔接上。

## Claude → Codex 步驟對齊

| Claude 原 section | 原始核心意圖 | Codex 對應做法 |
| --- | --- | --- |
| Section A：前情偵測 | 確認跑過 pro-kit 01，檢查 `.claude/` | 檢查 `000_Agent/`、`AGENTS.md`、`CORE_RULES.md`、可選 `~/.claude` / `~/.codex` |
| A-3 裝置訪談 | 根據裝置與雲端偏好推薦同步方案 | Codex 保留裝置 / 雲端 / GitHub / 體檢頻率四題 |
| Section B：強制備份 | 動 `.claude/` 前先備份，避免毀掉設定 | Codex 對任何工具隱藏資料夾都先備份：`~/.claude`、`~/.codex` 等 |
| Section C：建立同步架構 | 母體放雲端，隱藏資料夾用 symlink 指回 | Codex 建多 AI 母體：`000_Agent/`、`CORE_RULES.md`、各工具入口檔 |
| Section D：GitHub 版控 | 私有 repo / 公開 repo `.gitignore` 不同 | Codex 同樣分 private / public，嚴格排除 secrets 與私密記憶 |
| Section E：sync-health.sh | 定期驗證 symlink 與 memory | Codex 建通用 `sync-health`，檢查 Codex / Claude / memory / skills |
| Section F：MIGRATION.md | 未來換電腦 / 換 AI 有手冊 | Codex 擴充多 AI 遷移段落 |
| Section G：完成清單 | 跑最終體檢 | Codex 檢查母體、symlink、規則、記憶、git、備份 |

## Section A：前情偵測與訪談

### A-1. 偵測 pro-kit 01 是否完成

檢查：

```text
000_Agent/
000_Agent/skills/
000_Agent/memory/MEMORY.md
AGENTS.md
000_Agent/CORE_RULES.md
```

若沒有 `000_Agent/`，停止並請使用者先跑 01。07 是可攜化擴充，不是從零建立資料層。

### A-2. 偵測工具隱藏資料夾

只讀檢查：

- `~/.codex/`
- `~/.claude/`
- `~/.config/` 內使用者指定的 AI 工具目錄

分類：

| 類型 | 是否同步 | 說明 |
| --- | --- | --- |
| 規則 | 可同步 | `AGENTS.md`、`CLAUDE.md`、`CORE_RULES.md` |
| skills / commands | 可同步 | 可攜 SOP 與命令 |
| hooks / agents | 視內容 | 若含絕對路徑要改 `$HOME` 或相對路徑 |
| credentials | 不同步 | 每台機器各自登入 |
| local settings | 不同步 | 常含本機路徑 |
| cache / snapshots / session state | 不同步 | 跨機同步會衝突 |

### A-3. 四題訪談

確認：

1. 裝置組合：單機、多台 Mac、Mac + Windows、Windows / Linux、其他。
2. 同步管道：iCloud、Dropbox、Google Drive、OneDrive、只靠 GitHub、讓 Codex 推薦。
3. GitHub 備份：私有 repo、公開 repo、不用、之後再說。
4. 體檢頻率：每週、異常時手動、每天 cron、自行決定。

推薦邏輯：

- 多台 Mac：iCloud。
- Mac + Windows：Dropbox 或 Google Drive。
- Windows / Linux：OneDrive、Google Drive 或 Dropbox。
- 單機：本機母體 + GitHub 私有 repo。

## Section B：強制備份

任何移動或 symlink 前都先備份。

範例：

```bash
cp -a "$HOME/.claude" "$HOME/claude-backup-YYYYMMDD-HHMMSS"
cp -a "$HOME/.codex" "$HOME/codex-backup-YYYYMMDD-HHMMSS"
```

Codex 注意：

- Windows PowerShell 下應使用 `Copy-Item -Recurse`，並確認目標路徑。
- 備份後比對檔案數或至少列出備份內容。
- 若備份失敗，停止。

## Section C：決定母體資料夾

母體資料夾應放在「使用者平常會讀 Markdown 的地方」。

範例：

- Obsidian vault：放在 vault 本體內。
- iCloud：`~/Library/Mobile Documents/.../My-Agent/`
- Dropbox：`~/Dropbox/My-Agent/`
- Google Drive：`~/Library/CloudStorage/.../My Drive/My-Agent/`
- OneDrive：`~/OneDrive/My-Agent/`
- GitHub only：`~/My-Agent/`

原則：

- 母體在雲端資料夾內。
- symlink 在工具隱藏資料夾或專案入口。
- 不把 symlink 放進雲端資料夾後期待雲端正確同步 target。

## Section D：建立多 AI 可攜架構

母體建議：

```text
My-Agent/
  AGENTS.md
  CLAUDE.md              # 可選相容層
  GEMINI.md              # 可選相容層
  000_Agent/
    CORE_RULES.md
    skills/
    workflows/
    memory/
    knowledge/
    scripts/
    MIGRATION.md
  100_Todo/
  200_Reference/
```

入口策略：

| AI 工具 | 入口 | 建議 |
| --- | --- | --- |
| Codex | `AGENTS.md` | 引用 `000_Agent/CORE_RULES.md` |
| Claude Code | `CLAUDE.md` | 引用同一份 `CORE_RULES.md` |
| Gemini | `GEMINI.md` | 可選，引用同一份母規則 |
| 未來工具 | 依工具慣例 | 建薄入口檔，不複製整份規則 |

`AGENTS.md` 範例：

```markdown
# AGENTS.md

請先閱讀 `000_Agent/CORE_RULES.md`。
本專案的 skills 位於 `000_Agent/skills/`，記憶位於 `000_Agent/memory/MEMORY.md`。
```

## Section E：搬移與 symlink

### E-1. Claude Code 相容項目

可搬：

- `settings.json`
- `CLAUDE.md`
- `hooks/`
- `commands/`
- `agents/`
- `skills/`

不可搬：

- `.credentials.json`
- `settings.local.json`
- `projects/`
- `shell-snapshots/`
- `todos/`
- `statsig/`

步驟：

1. 確認原位置存在且不是 symlink。
2. 移到母體 `.claude/`。
3. 在原位置建立 symlink。
4. 驗證 symlink target 存在。

### E-2. Codex 相容項目

Codex 對工作區 `AGENTS.md` 友善，因此優先策略是：

- 在每個需要 Codex 讀取的 repo 放 `AGENTS.md`。
- `AGENTS.md` 引用母體 `CORE_RULES.md`。
- 若要跨多 repo 共用，可用 symlink，但要注意 Windows 權限。

不建議同步：

- Codex 認證
- 本機快取
- session state

### E-3. Windows / PowerShell symlink

Windows 可用：

```powershell
New-Item -ItemType SymbolicLink -Path "C:\path\to\AGENTS.md" -Target "C:\path\to\My-Agent\AGENTS.md"
```

需要開發者模式或管理員權限。若使用 WSL，則在 WSL 內用 `ln -s`，但路徑需一致。

## Section F：GitHub 版控備份

若使用者同意：

```bash
git init -b main
```

私有 repo `.gitignore`：

```gitignore
.env
.env.*
**/credentials.json
**/.credentials.json
*.key
node_modules/
.venv*/
__pycache__/
*.log
.DS_Store
Thumbs.db
```

公開 repo 追加：

```gitignore
000_Agent/memory/MEMORY.md
000_Agent/memory/daily/
100_Todo/drafts/
100_Todo/archive/
300_Journal/
```

commit 前必做：

- `git status --short`
- 檢查是否有 secrets
- 公開 repo 要特別排除私人記憶與草稿

## Section G：sync-health 腳本

建立：

```text
000_Agent/scripts/sync-health.sh
```

檢查項目：

1. `AGENTS.md` 是否存在且可讀。
2. `000_Agent/CORE_RULES.md` 是否存在。
3. `000_Agent/memory/MEMORY.md` 是否存在。
4. `000_Agent/skills/` 是否存在。
5. 若有 `~/.claude/skills` symlink，target 是否存在。
6. 若有 `CLAUDE.md` symlink，target 是否存在。
7. 若有 git repo，是否有未提交變更。

輸出應區分：

- OK：正常
- WARN：可用但建議處理
- FAIL：會導致 AI 失憶或讀不到 skill

## Section H：MIGRATION.md

建立：

```text
000_Agent/MIGRATION.md
```

內容包含：

```markdown
# AI 大腦遷移手冊

## 當前架構

- 母體資料夾：
- 同步管道：
- GitHub repo：
- Codex 入口：`AGENTS.md`
- 母規則：`000_Agent/CORE_RULES.md`
- 記憶：`000_Agent/memory/MEMORY.md`
- 體檢腳本：`000_Agent/scripts/sync-health.sh`

## 換新電腦

1. 取得母體資料夾（雲端同步或 git clone）。
2. 建立工具入口檔 / symlink。
3. 各 AI 工具重新登入認證。
4. 跑 `sync-health.sh`。

## 換到 Codex

1. 確認工作區有 `AGENTS.md`。
2. `AGENTS.md` 引用 `000_Agent/CORE_RULES.md`。
3. 確認 `000_Agent/skills/` 與 `000_Agent/memory/` 可讀。
4. 開新 Codex session，要求先讀規則與記憶。

## 換到 Claude Code

1. 確認 `CLAUDE.md` 引用同一份 `CORE_RULES.md`。
2. 若需要 slash skill，設定 `~/.claude/skills` 指向 `000_Agent/skills/`。
3. 重新登入 Claude Code，不同步 credentials。

## 還原

若 symlink 或搬移出錯，使用 `~/claude-backup-*` 或 `~/codex-backup-*` 還原。
```

## Section I：完成檢查

- `000_Agent/` 存在
- `AGENTS.md` 存在
- `000_Agent/CORE_RULES.md` 存在
- `000_Agent/memory/MEMORY.md` 可讀
- `000_Agent/skills/` 可讀
- 備份資料夾存在
- symlink target 都存在
- `.gitignore` 已擋 secrets
- `sync-health.sh` 已建立
- `MIGRATION.md` 已建立
- 已提醒使用者在新 session 驗證

## 完成後提醒

告訴使用者：

1. 重開 Codex / AI 工具 session。
2. 若有第二台電腦，照 `MIGRATION.md` 建入口與 symlink。
3. AI 變笨、skill 消失、記憶讀不到時，先跑 `sync-health.sh`。
4. 不要同步 credentials；每台機器各自登入。
