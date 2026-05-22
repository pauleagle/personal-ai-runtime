# Codex 版：引導式 Landing Page 生成

> 對齊來源：`pro-kit/06-landing-page.md`
> 原始定位：安裝 Claude Code 的 `/landing` skill，透過 17 題問答產出銷售頁。
> Codex 改寫定位：建立 Codex 可用的 landing page 生成工作流，讓頁面先有銷售結構，再進入設計與預覽驗證。

## 核心意圖

原文要避免 AI 直接生成「看起來像 AI 的頁面」：抽象漸層、亂配色、文案空泛。真正的流程是：

1. 先問產品定位。
2. 再補齊銷售頁內容。
3. 再套設計系統。
4. 最後產出 HTML、預覽、修改。

Codex 版保留此順序，並加入前端驗證要求。

## Claude → Codex 步驟對齊

| Claude 原 section | 原始核心意圖 | Codex 對應做法 |
| --- | --- | --- |
| Section A：偵測環境 | 找到 skill 目錄、備份既有 landing、偵測 UUPM | 優先 `000_Agent/skills/landing/`；已存在先備份；UUPM 改為可選依賴 |
| Section B：sparse checkout | 只抓 `skills/landing-page/` | Codex 同樣抓完整資料夾，不只抓 `SKILL.md` |
| Section C：搬到 INSTALL_PATH | 放到正式 skill 位置 | 放進 `000_Agent/skills/landing/` |
| Section D：UUPM | 若有 UUPM，頁面設計品質更穩；沒有也 fallback | Codex 詢問是否安裝；不裝則使用 fallback design rules |
| Section E：驗證 | 確認 skill、references、templates、frontmatter | Codex 也驗證產出頁能預覽、手機版不爆版 |
| 使用流程 | `/landing` 逐題問答，生成銷售頁 | Codex 以自然語言或 skill 啟動，保留 17 題的順序與分組 |

## Section A：安裝位置與環境

### A-1. Skill 位置

優先：

```text
000_Agent/skills/landing/
```

若使用者需要 Claude Code 相容，再同步到：

```text
~/.claude/skills/landing/
```

### A-2. 已存在處理

若 `landing/` 已存在：

```text
landing.bak.YYYYMMDD-HHMMSS/
```

不要覆蓋使用者改過的模板或 references。

### A-3. UUPM 偵測

原文偵測 UI UX Pro Max（UUPM）。Codex 版採三種狀態：

- 已安裝：可讀取 / 使用 UUPM 規則。
- 未安裝但使用者願意裝：依官方最新方式安裝，需網路與同意。
- 未安裝且使用者跳過：使用 `references/fallback-design-rules.md`。

## Section B：取得 skill 完整資料夾

原始 sparse checkout：

```bash
git init -q
git remote add origin https://github.com/lifehacker-tw/claude-code-mini-course.git
git config core.sparseCheckout true
echo "skills/landing-page/" >> .git/info/sparse-checkout
git pull --depth 1 origin master
```

完整結構至少要有：

```text
landing/
  SKILL.md
  README.md
  references/
    question-bank.md
    uupm-integration.md
    fallback-design-rules.md
  templates/
    base.html
    countdown.js
```

缺少 `question-bank.md` 會失去引導問題；缺少 `base.html` 會失去輸出模板。不要只補空檔。

## Section C：使用流程

觸發：

```text
/landing
幫我做一頁線上課銷售頁
幫這個活動做 landing page
```

Codex 應把訪談分成三段。

### C-1. 產品定位

確認：

1. 頁面類型：活動、線上課、服務、數位產品。
2. 目標受眾。
3. 受眾痛點。
4. 核心承諾。

每題給範例：

- 好答案：具體到對象、情境、結果。
- 壞答案：抽象、萬用、看不出差異。

### C-2. 內容填入

依序收集：

1. Hero 標題
2. Hero 副標
3. Hook / 痛點段落
4. 產品或課程介紹
5. 學到 / 得到什麼
6. 見證或案例（可選）
7. 適合誰
8. 不適合誰
9. 時間 / 地點 / 交付形式
10. 價格 / 方案
11. 講師 / 品牌介紹
12. FAQ

使用者卡住時，Codex 可以根據前文產生 3 個候選，但要讓使用者挑。

### C-3. CTA 與倒數

確認：

- 主要 CTA 文案
- 報名 / 購買 / 訂閱連結
- 是否有截止時間
- 是否需要倒數計時器
- 是否需要 sticky CTA bar

## Section D：生成頁面

輸出建議：

```text
100_Todo/landing-pages/[slug]/
  answers.json
  index.html
  assets/
  README.md
```

`answers.json` 是重跑與 restyle 的關鍵。之後要改文案或重套樣式，不必重新訪談。

頁面區塊順序：

1. Hero
2. Hook / Pain
3. About
4. What you get
5. Social proof（可選）
6. Who it is for
7. Details
8. Pricing
9. CTA
10. Instructor / brand
11. FAQ

## Section E：設計規則

### 有 UUPM 時

- 依產品類型與產業挑字體、色彩、元件節奏。
- 參考 `references/uupm-integration.md`。

### fallback 時

- 讀 `references/fallback-design-rules.md`。
- 避免紫色漸層、抽象圓球、空泛 hero。
- 第一屏必須清楚看到產品名稱或 offer。
- CTA 要明確，不只寫「了解更多」。
- 手機版優先檢查。

## Section F：預覽與驗證

產出後：

1. 開啟本地預覽或直接開 `index.html`。
2. 用 Browser / Playwright 截圖檢查桌面版。
3. 檢查手機寬度。
4. 確認倒數計時不遮住內容。
5. 確認 sticky CTA 不在 hero 前就干擾閱讀。

前端驗證清單：

- Hero 有具體 offer。
- 首屏沒有大段空話。
- 圖片或素材語意正確，不用無關 stock 感圖片。
- 文字不溢出、不重疊。
- CTA 連結可點。
- FAQ 不是 placeholder。

## Section G：重跑與改版

若使用者說：

```text
重新套風格
改文案重跑
/landing --restyle [slug]
```

Codex 應：

1. 讀取 `100_Todo/landing-pages/[slug]/answers.json`。
2. 詢問要改文案、設計、或兩者。
3. 保留原答案備份。
4. 重新生成 `index.html`。
5. 再跑預覽驗證。

## 完成檢查

- `000_Agent/skills/landing/SKILL.md` 存在
- `references/question-bank.md` 存在
- `references/fallback-design-rules.md` 存在
- `templates/base.html` 存在
- UUPM 狀態已記錄：已安裝 / 跳過 / fallback
- 產出的 landing page 有 `answers.json`
- `index.html` 可預覽
- 手機版與桌面版都檢查過
