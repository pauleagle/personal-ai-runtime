# Codex 版：外部工具整合計畫

> 對齊來源：`pro-kit/03-tool-integration.md`
> 原始定位：幫 Claude Code 訪談常用工具，產出「整合計畫文件」，之後每次挑一個工具再查最新方式安裝。
> Codex 改寫定位：建立外部工具整合 backlog，明確區分 CLI / API / MCP / plugin / browser，避免一次裝太多與吃掉上下文。

## 改寫重點

原文的重要轉折是：這份 pro-kit 不再把 Gmail、Notion、Firecrawl 等安裝步驟寫死，而是先產生計畫文件，未來執行時再上網查最新官方方式。Codex 版完整保留這個意圖。

Codex 執行外部整合時要特別注意：

- 任何「最新安裝方式」都不可憑記憶，必須查官方文件或可信來源。
- 需要網路、安裝套件、登入、寫全域設定時，依權限規則詢問或升級。
- 憑證不可寫進 `AGENTS.md`、`CORE_RULES.md` 或對話摘要；應放 `.env`、系統 keychain、官方 CLI auth store 或使用者指定秘密管理方式。
- 計畫文件是本輪主要產物，不是立刻把所有工具裝完。

## Claude → Codex 步驟對齊

| Claude 原 section | 原始核心意圖 | Codex 對應做法 |
| --- | --- | --- |
| 先看 MCP / API / CLI 決策表 | 打破「外部工具 = MCP」的直覺 | Codex 也採 CLI → API → MCP / plugin → browser 的順序 |
| Section A：工具訪談 | 問 Email、Calendar、Notion、Obsidian、抓網頁、GitHub / Slack / Linear | Codex 逐項確認工具、用途、頻率、讀寫需求、敏感程度 |
| A-6 確認清單 | 避免 AI 自作主張多裝工具 | Codex 產出待整合清單並請使用者確認，不安裝未確認工具 |
| Section B：整合計畫文件 | 把訪談結果寫入 `100_Todo/integrations/`，之後慢慢執行 | Codex 建同等計畫文件，並加入「未來 Codex session 執行指引」 |
| B-3 未來 AI 指引 | 下次挑工具時必須查最新官方安裝方式 | Codex 明寫必須用 web / 官方 docs 驗證 |
| Section C：AI 能幹清單 | 記錄已整合工具能做什麼 | Codex 建 `000_Agent/knowledge/我的 AI 能幹清單.md` |
| Section D：排錯速查 | OAuth、Notion 權限、MCP 不見等常見問題 | Codex 建 troubleshooting，並改寫為 CLI / API / connector 通用排錯 |
| Section E：個人工具清單 | 讓 AI 理解使用者整體工具組合與淘汰經驗 | Codex 建 `我的工具清單.md`，供推薦、比較、工作流優化時讀取 |

## Section A：工具訪談

### A-1. 訪談維度

逐項確認：

1. Email：Gmail、Outlook、其他 / 不需要。
2. 行事曆：Google Calendar、Apple Calendar、Outlook Calendar、其他 / 不需要。
3. 筆記與知識管理：Notion、Obsidian、本地 Markdown、其他 / 不需要。
4. 網頁資料抓取：常用、偶爾、不需要。
5. 程式與專案工具：GitHub、GitLab、Linear、Jira、Slack、Teams、其他。
6. 內容與發布工具：WordPress、Webflow、Kit、Substack、社群平台等。

每個工具都記錄：

- 用途：讀資料、寫資料、產出草稿、查詢狀態、通知、部署等。
- 使用頻率：每天、每週、偶爾。
- 權限敏感度：是否涉及信件、客戶資料、金流、私密筆記。
- 可接受路線：CLI、API、connector / plugin、瀏覽器自動化。

### A-2. 路線判斷

決策順序：

1. **CLI 優先**：已有官方或穩定 CLI，例如 `gh`。
2. **REST API 次之**：CLI 不足，但 API 穩定且可用 token 控制權限。
3. **MCP / connector / plugin**：需要 AI 工具自動可見、或官方提供成熟 connector。
4. **瀏覽器自動化**：沒有 API 或必須操作 UI 時才用。

例子：

| 工具 | 初步建議 | 原因 |
| --- | --- | --- |
| GitHub | CLI `gh` | 穩定、可驗證、不吃上下文 |
| Google Calendar | 官方 connector / CLI / API 視環境 | 需查最新支援 |
| Notion | API 寫入、必要時 connector 讀取 | 權限與資料庫分享要明確 |
| Obsidian | 本地檔案 | vault 在磁碟上，Codex 可直接讀寫 |
| Firecrawl | MCP / API | 視使用者帳號與額度 |

### A-3. 確認範圍

Codex 在本輪只做：

- 產生整合計畫
- 產生 AI 能幹清單骨架
- 產生個人工具清單骨架

不做：

- 不立刻安裝所有 CLI
- 不寫 `.env` 真實 token
- 不改全域 MCP / plugin 設定
- 不登入任何服務

除非使用者明確改口要求「現在就整合某個工具」。

## Section B：產生整合計畫文件

### B-1. 路徑

優先：

```text
100_Todo/integrations/YYYY-MM-DD-tool-integration-plan.md
```

若沒有 `100_Todo/`：

```text
tool-integration-plan.md
```

### B-2. 文件模板

```markdown
---
created: YYYY-MM-DD
status: in-progress
source: pro-kit 03 Codex rewrite
---

# 外部工具整合計畫

> 這份文件記錄要接到 Codex / AI 工作流的工具。
> 執行整合時，必須先查官方最新文件，再決定 CLI / API / MCP / connector / browser 路線。

## 決策原則

1. CLI 優先：不吃上下文，行為可驗證。
2. REST API 次之：控制精準，但要安全管理 token。
3. MCP / connector / plugin：只在真的需要 AI 自動使用工具時採用。
4. Browser automation：沒有穩定 API 時最後使用。

## 工具清單

### 🟡 [工具名] - 尚未整合

- 用途：
- 使用頻率：
- 敏感資料：
- 初步建議路線：
- 替代路線：

**執行時必查**

- [ ] 官方目前推薦的 AI / CLI / API 整合方式
- [ ] 認證方式與權限範圍
- [ ] 是否有官方 CLI
- [ ] 是否有官方 REST API
- [ ] 是否有官方或可信 MCP / connector
- [ ] 安裝是否會寫全域設定

**安裝 checklist**

- [ ] 使用者確認路線
- [ ] 取得或完成授權
- [ ] 憑證放入安全位置，不寫進規則檔
- [ ] 安裝 / 設定完成
- [ ] 跑一個真實驗證案例
- [ ] 回寫本計畫與 AI 能幹清單

**備註**

- 實際採用路線：
- 版本：
- 驗證指令：
- 踩坑：

## 進度總覽

- 🟡 尚未整合：N
- 🟢 已整合：0
- 🔴 放棄：0
```

### B-3. 未來 Codex session 執行指引

把以下段落寫進計畫文件底部：

```markdown
---

## 給未來 Codex 執行時的指引

當使用者說「從這份計畫挑 [工具名] 來裝」時：

1. 先確認工具、用途、讀寫範圍與敏感資料。
2. 使用 web 查官方文件與最新推薦整合方式。
3. 比較 CLI / API / MCP / connector / browser。
4. 向使用者說明推薦路線、替代路線、風險與需要的權限。
5. 取得同意後再安裝或修改設定。
6. 用真實案例驗證，不只看安裝成功訊息。
7. 回寫本計畫，把該工具標成已整合，並寫入實際路線、版本、驗證指令與踩坑。
8. 同步更新 `000_Agent/knowledge/我的 AI 能幹清單.md`。
```

## Section C：建立 AI 能幹清單

建立：

```text
000_Agent/knowledge/我的 AI 能幹清單.md
```

若沒有 `000_Agent/`，建立：

```text
my-ai-capabilities.md
```

模板：

```markdown
---
updated: YYYY-MM-DD
---

# 我的 AI 能幹清單

> 每次整合完成一個工具，都回來更新這份清單。

## 🟢 已整合的工具

（尚無）

## 📋 待整合工具

參考：`100_Todo/integrations/YYYY-MM-DD-tool-integration-plan.md`

## 新增工具能力的格式

### [工具名]（[路線]｜整合日期：YYYY-MM-DD）

- 能做：
- 不能做：
- 需要我確認的操作：
- 風險或限制：

**試試看的指令**

- ...
```

## Section D：排錯速查

可寫入：

```text
000_Agent/knowledge/tool-integration-troubleshooting.md
```

內容：

```markdown
# 外部工具整合排錯速查

## Auth / OAuth

- Token 過期：重新授權。
- 權限不足：檢查 scope。
- 不要把 token 寫進 `AGENTS.md`、`CORE_RULES.md`、`MEMORY.md`。

## API

- 404：通常是資源 ID 錯、權限不足、或 integration 沒被分享。
- 429：額度或 rate limit，應退避重試。
- 401 / 403：憑證或權限問題。

## CLI

- 指令不存在：檢查是否安裝、PATH 是否生效。
- 已安裝但未登入：跑官方 auth status。
- 多帳號：確認目前使用哪個 profile / account。

## MCP / connector / plugin

- 工具不見：檢查設定檔、server 是否啟動、工具是否被目前 session 載入。
- server hang：重啟工具或停用該 MCP。
- 上下文變肥：檢討是否應改用 CLI / API。

## Browser automation

- UI 改版：selector 可能失效。
- 登入狀態：可能需要使用者瀏覽器 profile。
- 寫入操作：必須讓使用者確認。
```

## Section E：建立個人工具清單

建立：

```text
000_Agent/knowledge/我的工具清單.md
```

模板：

```markdown
---
updated: YYYY-MM-DD
---

# 我的數位工具清單

> AI 在推薦工具、比較方案、優化工作流前，應先讀這份清單。

## 我用這些工具做這些事

### 通訊與信箱

- **工具名** - 用途、頻率、為什麼選它

### 行事曆與排程

### 筆記與知識管理

### 程式開發與自動化

### 設計與內容創作

### 資料與追蹤

### 金流與訂閱

## 我的工作流組合

- [工具 A] → [工具 B] → [工具 C]：

## 已淘汰的工具

- **工具名** - 用過多久、為什麼淘汰、換成什麼

## 未來想評估的工具

- **工具名** - 想解決什麼問題、何時評估
```

## 完成檢查

- 已完成工具訪談與確認範圍
- 已建立整合計畫文件
- 每個工具都有用途、初步路線、必查問題、安裝 checklist
- 計畫底部有未來 Codex 執行指引
- 已建立 AI 能幹清單
- 已建立個人工具清單
- 已建立或更新排錯速查
- 本輪沒有安裝使用者未要求的外部工具
