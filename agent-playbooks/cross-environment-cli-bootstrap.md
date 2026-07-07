# Cross-Environment CLI Bootstrap

## 目的

在跨 Windows / WSL / sandbox / 遠端 shell 的工作中，標準化 agent 如何發現、補齊與驗證常用 CLI、script helper 與 user-local 工具。

這份 playbook 解決的不是「安裝某一個工具」，而是避免 agent 在缺少 `jq`、`shellcheck`、`python` shim、`uv`、`hf` 這類工具時，臨場用不一致的方法處理，或在沒有 sudo 權限時停在半途。

## 核心原則

- 先盤點再安裝：用 `command -v`、`--version`、PATH 檢查確認缺口。
- 優先不污染系統：沒有明確需求時，不用 root 安裝；可用 user-local 就放到 `~/.local/bin`。
- 尊重權限邊界：跨 `/mnt/c`、workspace 外路徑、系統套件管理器、網路下載都要符合 sandbox / escalation 規則。
- 工具補齊後必須跑任務級驗證，不只看版本。
- 一次性 glue script 可放 `/tmp`，但重複出現的流程應提升成 playbook 或 skill。
- 不把 token、private key、model weights、generated artifacts 或下載的臨時 binary 寫進 repo。

## 適用時機

- WSL 或新 shell session 缺少常用 CLI，例如 `jq`、`shellcheck`、`python`、`uv`、`hf`。
- 使用者沒有 sudo / 不在 sudoers，但任務仍可透過 user-local 工具完成。
- 需要跨 Windows controller workspace 與 WSL runtime workspace 同步 handoff、worklog 或驗證證據。
- 任務需要小型 deterministic helper script 來避免長文本複製、重複追加或路徑同步錯誤。
- 需要讓 repo-local `agent-skills/` 被 Codex session 看見，且應先用 repo script 做 bootstrap。
- 同一類工具補齊流程開始反覆出現，準備日後萃取成 skill。

## 不適用時機

- 工具已存在且版本足以完成任務。
- 任務只需要一次簡單 shell command，不涉及安裝、跨路徑寫入或長文本同步。
- 安裝會改變系統安全狀態、需要管理員密碼、或使用者未授權。
- 需要處理 secret、credential、license-gated model weights；這些只記錄邊界與操作建議，不複製內容。
- 可以用現有語言標準庫可靠完成的小查詢，不必為了偏好安裝新 CLI。

## 標準流程

### 1. 盤點環境

- 確認 OS / shell / 架構：
  - `uname -m`
  - `command -v apt-get || true`
  - `printf '%s\n' "$PATH"`
- 檢查目標工具：
  - `command -v jq || true`
  - `command -v shellcheck || true`
  - `command -v python || true`
  - `command -v python3 || true`
  - `command -v uv || true`
  - `command -v hf || true`
- 檢查 repo 或任務實際需要，不要把「可能有用」當成安裝理由。

### 2. 選擇安裝策略

優先順序：

1. 已存在工具：直接使用並記錄版本。
2. Repo 內既有 script / wrapper：優先使用，不重新發明。
3. User-local binary 或 shim：安裝到 `~/.local/bin`，前提是 PATH 已包含或可安全加入。
4. Package manager：只有在使用者允許、sandbox 允許、且有 sudo / root 權限時才使用。
5. 語言 fallback：例如用 Python JSON parser 暫代 `jq`，但應記錄這是 fallback。
6. 明確 blocked：若沒有安全安裝路徑，回報缺口與使用者可手動執行的命令。

### 3. User-Local 安裝規則

- 目標目錄預設為 `~/.local/bin`。
- 建立前確認 PATH：
  - 若 `~/.local/bin` 不在 PATH，先詢問是否要更新 shell profile，或只在當前命令用絕對路徑。
- 常見工具：
  - `python` shim：`ln -s /usr/bin/python3 ~/.local/bin/python`
  - `jq`：使用官方 release binary，下載後 `chmod +x`，驗證 `jq --version`
  - `shellcheck`：使用官方 release tarball，抽出 binary，驗證 `shellcheck --version`
- 網路下載必須使用官方來源，並在回報中寫明來源類型與版本；若可取得 checksum，優先驗證。

### 4. 臨時 Script 規則

- 一次性同步、長文本追加、防重複 marker、跨路徑 copy 這類工作，可在 `/tmp` 建立臨時 helper。
- 臨時 script 應具備：
  - 明確 input / output path。
  - UTF-8 讀寫。
  - Idempotent guard，例如 marker 存在就不重複追加。
  - 不讀寫 secret。
  - 不被 commit。
- 若同類 `/tmp` helper 第二次出現，應考慮整理成 repo script 或 skill script。

### 5. 跨 Windows / WSL 寫入規則

- `/home/...` 和 `/mnt/c/...` 要視為不同 workspace / 權限邊界。
- 寫入 `/mnt/c` 前先確認是否在 sandbox writable roots 外；若是，依 escalation 規則請求使用者允許。
- 對 handoff / worklog 類文字檔，明確使用 UTF-8。
- Windows controller repo 與 WSL runtime repo 可能不同步；回報時分別列出 status，不要把其中一邊狀態當成另一邊。

### 6. 驗證標準

安裝後至少做三層驗證：

- Tool resolution：
  - `command -v <tool>`
- Version：
  - `<tool> --version`
- Task-level smoke：
  - `jq`：解析一個小 JSON。
  - `python` shim：`python --version` 與簡單 import。
  - `shellcheck`：檢查目標 shell scripts。
  - `uv` / `hf`：只跑不含 secret 的版本或 help / auth status 檢查。

### 7. Repo Agent Skills Symlink Bootstrap

當 repo 內 `agent-skills/` 是 skill source of truth，而目前 agent session（Codex 或 Claude）尚未看見這些 skills 時，先使用 repo script，不要先萃取成 skill。

標準入口：

```bash
scripts/sync-agent-skills-to-agents.sh
```

預設行為：

- Source: `<repo>/agent-skills`
- Targets: `${CODEX_HOME:-$HOME/.codex}/skills` 與 `${CLAUDE_HOME:-$HOME/.claude}/skills`
- 可用 `--agents codex` 或 `--agents claude` 只同步單一 agent。
- 只 symlink 具有 `SKILL.md` 的 skill directory。
- 已存在且指向正確 source 的 symlink 保持不變。
- 同名目標若不是 symlink，或 symlink 指向其他位置，視為 conflict 並停止完成狀態，不自動覆蓋。

安全檢查：

```bash
scripts/sync-agent-skills-to-agents.sh --dry-run
find -L ~/.codex/skills -maxdepth 2 -name SKILL.md -print
find -L ~/.claude/skills -maxdepth 2 -name SKILL.md -print
```

若環境使用非預設 agent home：

```bash
CODEX_HOME=/path/to/codex-home CLAUDE_HOME=/path/to/claude-home scripts/sync-agent-skills-to-agents.sh
```

完成後，如果目前 agent session 仍看不到新 skills，開新的 session 是最穩定的 reload 方式。

## Agent 行為規則

- 不要因為缺 CLI 就直接放棄；先找 user-local 或 fallback。
- 不要在未經允許時要求 broad sudo、改 system PATH、改 shell profile、或寫入 `/usr/local/bin`。
- 不要用 package manager 安裝一大包「可能需要」的工具；只補任務實際需要的最小工具。
- 不要把下載的 binary、tarball、cache、generated outputs 放進 repo。
- 若使用 `/tmp` script，最後要說明它是一次性工具、用途、是否已寫入 repo。
- 若環境沒有 sudo，回報要區分「不能 apt install」與「任務仍可透過 user-local 完成」。
- 若工具版本可能影響後續任務，將版本寫入 handoff 或工作日誌。

## 標準 Prompt

```text
請依照 cross-environment CLI bootstrap 流程，檢查目前 Windows/WSL/sandbox 環境缺少的任務必要 CLI。先盤點 PATH、工具存在性與版本；若缺工具，優先使用 user-local 安裝或安全 fallback，不要假設有 sudo。安裝後請跑版本與任務級 smoke 驗證，並回報哪些工具被安裝、放在哪裡、是否需要後續推送或記錄到 handoff。
```

## 建議輸出格式

```md
## 環境盤點

- OS / shell:
- PATH 重點:
- 缺少工具:

## 採用策略

- 使用既有工具:
- User-local 安裝:
- Fallback:
- Blocked:

## 驗證

- Tool versions:
- Task-level smoke:

## 交接

- 已安裝位置:
- 不納入 repo 的臨時檔:
- 後續是否應萃取成 skill:
```

## Skill 萃取候選

若此流程再次使用，建議萃取成 `user-local-cli-bootstrap` 或 `cross-environment-cli-bootstrap` skill。Skill 只需保留短版觸發條件、安裝策略、驗證規則與輸出格式；詳細背景與設計理由留在本 playbook。
