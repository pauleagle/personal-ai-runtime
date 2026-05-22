# Pro-kit Claude → Codex 對齊索引

> 來源：`external-source/claude-code-mini-course/upstream/clone/claude-code-mini-course/pro-kit/`
> 目標：將原本面向 Claude Code 的 pro-kit，依原始步驟順序與核心意圖，改寫成 Codex 視角的可攜工作流。

## 整體轉換原則

| Claude Code 原假設 | Codex 版改寫 |
| --- | --- |
| `CLAUDE.md` 是主要規則入口 | `AGENTS.md` 是 Codex 入口；建議另有 `000_Agent/CORE_RULES.md` 作為 AI 無關母規則 |
| `~/.claude/skills/` 是官方 skill 位置 | `000_Agent/skills/` 是可見、可攜、可同步的主位置；Claude 需要時才做 symlink 相容 |
| `AskUserQuestion` 選項框 | Codex 用簡短逐題訪談；Default 模式下可做保守合理假設 |
| Claude slash command，例如 `/cards`、`/landing` | Codex 可用自然語言觸發，或讀取對應 `SKILL.md` 執行 |
| Claude MCP / settings / commands | Codex 以 CLI / API / plugin / browser 分層判斷；全域設定需先確認與備份 |
| 以 Claude Code 生態為主 | 以「資料屬於使用者」為主，可映射到 Codex、Claude、Gemini 或未來工具 |

## 文件對照

| 原始檔 | Codex 版 | 核心意圖 |
| --- | --- | --- |
| `01-agent-folder-setup.md` | [01-agent-folder-setup.md](01-agent-folder-setup.md) | 建立 AI 分身資料層：資料夾、規則、記憶、daily log、下一步作業 |
| `02-skill-creator-bootstrap.md` | [02-skill-creator-bootstrap.md](02-skill-creator-bootstrap.md) | 安裝 / 建立 skill-creator，並真的產出第一個自訂 skill |
| `03-tool-integration.md` | [03-tool-integration.md](03-tool-integration.md) | 先產生外部工具整合計畫，不把安裝步驟寫死 |
| `04-brainstorm.md` | [04-brainstorm.md](04-brainstorm.md) | 動手前先釐清需求、提出方案、寫計畫書 |
| `05-social-cards.md` | [05-social-cards.md](05-social-cards.md) | 安裝圖卡產生器，以 HTML 模板 + Playwright 穩定輸出 PNG |
| `06-landing-page.md` | [06-landing-page.md](06-landing-page.md) | 用引導問答產出銷售頁，先文案結構再設計與預覽 |
| `07-cross-device-sync.md` | [07-cross-device-sync.md](07-cross-device-sync.md) | 把 AI 規則、記憶、skills 可攜化，支援跨裝置與跨 AI 遷移 |

## 建議閱讀順序

1. 先讀 `01`：建立資料層與 Codex 規則入口。
2. 再讀 `02`：把第一個重複工作變成 skill。
3. 接著讀 `04`：把「先規劃再動手」變成預設工作方式。
4. 有外部服務需求時讀 `03`。
5. 有內容製作需求時讀 `05` / `06`。
6. 準備跨裝置或跨 AI 時讀 `07`。

## Codex 執行提醒

- 不修改 upstream 原始 pro-kit。
- 編輯中文 Markdown 時使用 UTF-8。
- 對既有規則檔採追加與邊界標記，不覆蓋。
- 涉及網路、安裝套件、全域設定、登入或 symlink 時，先說明風險並取得使用者同意。
- 涉及最新外部工具資訊時，必須查官方文件，不靠記憶。
