# Cross-Agent Model Delegation

## 目的

在 Claude Code 與 Codex 互為 subagent 的工作中，標準化 agent 如何把工作**指派給對方 runtime 的特定模型**，並在指派失敗時正確歸因。

這份 playbook 解決的不是「呼叫另一個 agent」，而是兩個更容易出錯的問題：

- 主 agent 的原生 subagent 機制**不能直接指定對方 runtime 的模型**，必須透過中介 runtime 轉手；不理解這一層，會誤以為某個 `model:` 欄位可以填對方的模型名。
- 模型指派失敗有多種成因（CLI 版本、帳號方案、殘留 daemon、模型名拼寫），錯誤訊息長得很像，但處置方式完全不同。歸因錯了就會反覆做無效的重試或升級。

## 核心原則

- **先確認鏈路，再確認模型。** 分不清是「模型不可用」還是「模型名根本沒傳到伺服器」，任何重試都是猜測。
- **模型可用性是伺服器決定的，不是本地。** 本地 CLI 接受一個模型名，不代表後端會接受；反之本地的 metadata 警告也不代表不能用。
- **不要在 playbook 裡記錄「目前有哪些模型可用」。** 那是會過期的快照。記錄**如何探測**，讓讀的人得到當下的答案。
- **升級 CLI 之後，不要相信第一次呼叫的結果。** 長駐或臨時 daemon 可能跨越升級點，沿用舊的連線。
- **預設不指定模型。** 只有使用者明確要求特定模型時才指定；否則交給對方 runtime 的預設值。
- **指定模型是 runtime 控制參數，不是任務內容。** 不要把 `--model` / `--effort` 混進要傳給對方的自然語言任務文字裡。

## 適用時機

- 使用者明確要求用某個特定模型執行一段委派工作（例如指定推理較強或較省的模型）。
- 委派呼叫回報模型相關錯誤，需要判斷是版本、帳號、還是名稱問題。
- 升級任一方的 CLI 之後，要驗證委派鏈路仍然完整。
- 想確認某個模型在目前帳號與 CLI 版本下是否真的可用，而不是憑記憶假設。
- 需要向使用者解釋為什麼某個 `model:` 欄位填不進對方的模型名。

## 不適用時機

- 使用者沒有指定模型，且預設模型能完成任務 — 不要為了「用更好的模型」自行加上 `--model`。
- 只是要呼叫對方 agent，不涉及模型選擇。
- 問題明顯不在模型層（例如任務本身失敗、sandbox 權限不足、repo 未 trust）。
- 需要處理 credential、API key 或帳號方案升級 — 這些回報邊界，不自行操作。

## 委派拓樸

兩個 runtime 的 subagent 機制都是**兩層**的，這是理解一切錯誤的前提：

```text
主 agent（決定要委派）
    ↓ 用自己的原生 subagent 機制起一個殼層
殼層 subagent（跑在主 agent 自己的模型上）
    ↓ 透過中介 runtime 呼叫對方 CLI，這裡才傳得了對方的模型名
對方 runtime 的指定模型（實際執行工作的人）
```

關鍵推論：**主 agent 原生 subagent 定義裡的 `model:` 欄位，指的永遠是「驅動殼層的自家模型」，不是「實際幹活的對方模型」。** 想指定對方模型，只能透過第二層的 runtime 參數。

---

## 工作流程：Claude → 指定模型的 Codex subagent

### 1. 確認鏈路可用

先用最小任務確認 Codex CLI 本身能通，不帶任何模型指定：

```bash
codex exec --skip-git-repo-check "Reply exactly: OK"
```

若這一步就失敗，問題不在模型層，停止往下走。

### 2. 探測目標模型是否可用

不要憑記憶假設某個模型存在或可用。逐一探測：

```bash
codex exec -m <model-name> --skip-git-repo-check "Reply exactly: OK"
```

回傳 `OK` 即代表該模型在**目前的 CLI 版本與帳號方案下**可用。

### 3. 依錯誤訊息歸因

`codex exec` 的模型層失敗會回 HTTP 400，但訊息內容決定處置方式：

| 訊息特徵 | 成因 | 處置 |
|---|---|---|
| `requires a newer version of Codex` | 本地 CLI 版本太舊，後端拒絕服務新模型 | 升級 CLI，然後**必讀第 5 節** |
| `is not supported when using Codex with a ChatGPT account` | 帳號方案的模型白名單不含此模型 | 換模型，或回報使用者需要升級方案；升級 CLI 沒有用 |

另有一個**非致命**的本地警告，不要誤判為失敗：

```text
warning: Model metadata for `<model>` not found. Defaulting to fallback metadata
```

這代表本地 CLI 不認識該模型名，但**請求仍會送出**。若後端接受，任務照常完成。它通常是「CLI 該升級了」的前兆，而不是錯誤本身。

> 這兩種訊息是實際觀察到的形態。若遇到其他 400 訊息，先如實記錄原文再歸因，不要硬套進上表。

### 4. 發動委派

確認模型可用後，用 Codex plugin 的 subagent 入口：

```text
/codex:rescue --model <model-name> <要 Codex 做的事>
/codex:rescue --model <model-name> --effort <none|minimal|low|medium|high|xhigh> <任務>
```

行為規則：

- `--model` 與 `--effort` 是 runtime 控制參數，**要從任務文字中剝離**，不要當成任務描述的一部分傳下去。
- 非別名的模型名會**原樣直通**到後端，所以任意合法全名都能用。
- plugin 只註冊了少量短別名，其餘一律寫全名。別名對照可在 plugin 的 `MODEL_ALIASES` 查證，不要憑記憶推測某個縮寫存在。
- plugin 的 companion script 位於版本化路徑 `~/.claude/plugins/cache/openai-codex/codex/<version>/scripts/`，**會隨 plugin 更新被覆寫**。不要直接改它，也不要把該路徑寫死進其他腳本。

### 5. 升級 CLI 後的 daemon 陷阱

**這是最容易誤判的一種失敗。**

Codex plugin 的委派不走 `codex exec`，而是經由 `app-server-broker` 起一個 `codex app-server` 連線。升級 CLI 之後：

- 直接跑 `codex exec -m <model>` 已經成功，
- 但同時間走 plugin 委派**仍然回報升級前的舊版本錯誤**。

原因是該次呼叫沿用了**升級前就已啟動**的 broker 進程，裡面抱著舊的 app-server。這些 broker 是每次呼叫的臨時進程、會自行退出。

診斷：

```bash
ps -eo pid,lstart,args | grep -E "app-server-broker|codex app-server" | grep -v grep
```

比對進程啟動時間與 CLI 升級時間。若進程早於升級，等它結束後重跑即可，**不要據此判斷 plugin 壞掉、也不要重複升級**。

### 6. 驗證標準

模型委派至少做三層驗證，缺一層就可能誤判：

- **CLI 直呼**：`codex exec -m <model> ...` 回傳預期字串。
- **委派鏈路**：透過 `/codex:rescue --model <model>` 回傳預期字串（證明模型名真的穿過了中介 runtime）。
- **預設路徑**：不帶 `--model` 呼叫一次，確認 Codex 設定檔的預設模型沒有壞。

第三層特別重要：Codex 的預設模型寫在 `~/.codex/config.toml`。**若預設模型失效，所有不帶 `--model` 的委派都會失敗**，包含 plugin 的 review gate 等自動觸發路徑。這種壞法是靜默的，不主動驗證就不會發現。

---

## 工作流程：Codex → 指定模型的 Claude subagent

本方向有兩條容易混淆的路徑：

- `claude -p --model <model>` 會啟動一個指定模型的外部 Claude worker；適合單一 bounded job，但它本身是 Claude session，不是由 Claude `Agent` tool 產生的 subagent。
- `claude --agents ... -p ...` 先啟動 Claude coordinator，再由其 `Agent` tool 指派自訂 subagent；`model` 寫在 subagent definition，這才是嚴格意義的「指定模型 Claude subagent」。

兩條路徑都已實際驗證。以下用 CLI 直呼探測模型可用性，並以第二條路徑驗證完整委派鏈路。

### 1. 確認鏈路可用

先確認 Claude Code 已登入，再用不指定模型的最小任務驗證基礎鏈路：

```bash
claude auth status
claude --safe-mode --tools "" --permission-mode dontAsk \
  --no-session-persistence --output-format json \
  -p 'Reply exactly: OK'
```

判定標準：

- `claude auth status` 的 `loggedIn` 必須是 `true`。
- 最小任務必須回傳 `result: "OK"`、`is_error: false` 且 process exit code 為 `0`。
- 若這一步失敗，先處理登入、網路、sandbox 或 safe-mode 下的基礎模型問題；不要直接歸因到目標模型。

`--safe-mode` 適合排除 hooks、plugins、自訂 agents 與專案設定干擾，但也會停用自訂 subagent。它只能用在本節的 CLI 直呼探測，**不要帶進第 4 節的真正 subagent 委派**。

### 2. 探測目標模型是否可用

用指定模型做相同的無工具最小請求：

```bash
claude --safe-mode --tools "" --permission-mode dontAsk \
  --no-session-persistence --output-format json \
  --model <model-name> \
  -p 'Reply exactly: OK'
```

不要只看 `result`。JSON 回傳還必須同時滿足：

- `is_error: false`
- process exit code 為 `0`
- `modelUsage` 含有實際執行的目標模型

`sonnet`、`opus`、`haiku` 這類 alias 會隨 provider 與時間解析到不同版本；若任務要求「某一模型家族的當前預設」，用 alias。若要求可重現的精確模型，使用當下已探測成功的完整 model ID，但不要把會過期的 ID 寫死在本 playbook。

### 3. 依錯誤訊息歸因

目前實際觀察到的模型層失敗形態如下：

| 訊息特徵 | 成因 | 處置 |
|---|---|---|
| exit code `1`、`is_error: true`、`api_error_status: 404`，且結果含 `There's an issue with the selected model (...)` / `It may not exist or you may not have access to it` | 後端不接受該模型；錯誤文字刻意合併「模型不存在」與「帳號無權限」，單靠此訊息無法再細分 | 啟動互動式 `claude` 後用 `/model` picker，或改用官方 alias 探測；再查 `claude auth status` 與帳號方案。不要只因 404 就升級 CLI 或方案 |

這個 404 與 Codex 側的 400 不同，也沒有提供「名稱錯誤」和「方案不含」的可靠細分。若 alias 成功、完整 model ID 失敗，優先懷疑 model ID 已過期或不屬於目前 provider；若 alias 與完整 ID 都失敗，再查帳號權限。遇到其他訊息時保留完整 JSON、exit code 與 stderr，再新增歸因規則，不要套用未觀察過的字串。

### 4. 發動委派

若只需要一個指定模型的外部 worker，可直接呼叫：

```bash
claude --model <model-name> \
  --no-session-persistence --output-format json \
  -p '<bounded task>'
```

若要求真正的 Claude `Agent` subagent，使用 inline `--agents` definition，並以 `@` mention 保證該 subagent 被呼叫：

```bash
claude \
  --agents '{
    "bounded-worker": {
      "description": "Execute one bounded delegated job and return a structured report.",
      "prompt": "Stay within the supplied scope and return the requested report only.",
      "tools": ["Read", "Grep", "Glob", "Bash"],
      "model": "<model-name>",
      "maxTurns": 20
    }
  }' \
  --no-session-persistence --output-format json \
  -p 'Use @bounded-worker for this task: <bounded task>'
```

行為規則：

- 目標模型寫在 `--agents` JSON 的 `model` 欄位，不能混進 `<bounded task>`。
- coordinator 的模型與 subagent 的模型是兩個獨立控制面。除非使用者也指定 coordinator，否則不要額外加頂層 `--model`。
- `@bounded-worker` 是委派保證；只在自然語言中說「可考慮使用 worker」可能被 coordinator 判斷為不需委派。
- coordinator 必須保有 `Agent` tool。若另外使用頂層 `--tools` 限縮整個 session，工具集合至少要涵蓋 `Agent` 與 worker definition 需要的工具；worker 本身再由 definition 的 `tools` 做 allowlist。
- 實作型任務應把 allowed scope、forbidden scope、validation requirements 與 output contract 完整放進 `<bounded task>`；若已有 JSON job contract，先依 `atomic-subagent-runner` validator 驗證。
- 若要可重複解析結果，保留 `--output-format json`，必要時再加 `--json-schema`；不要只擷取畫面上的最後一句文字。

### 5. Claude session 與設定優先序陷阱

這條路徑沒有 Codex plugin 的 `app-server-broker`；每次 `claude -p` 都可用新的非互動 session，因此不應照搬「等舊 broker 自行退出」的診斷。不過 Claude 有自己的殘留狀態與優先序陷阱：

- `CLAUDE_CODE_SUBAGENT_MODEL` 的優先序高於單次 `Agent` invocation、subagent definition 的 `model` 與主 session 模型。若實際 `modelUsage` 和 definition 不符，先檢查這個環境變數。
- filesystem subagent（`~/.claude/agents/` 或 `.claude/agents/`）在 session 啟動時載入；session 中途修改後要用 `/agents` 重新載入或重開 session。inline `--agents` 不受舊檔案快取影響，適合一次性委派。
- `--resume` / `--continue` 會接續既有 session 狀態，不適合做 stateless model probe。探測與 bounded job 預設使用 `--no-session-persistence`，也不要搭配 resume/continue。
- `claude --bg` 與 `claude agents` 管理的是獨立背景 sessions；已啟動的 agent 不會因之後修改預設模型或 agent definition 而自動切換。需要新設定時應建立新 session。
- 使用者預設模型通常在 `~/.claude/settings.json` 的 `model`；專案還可能由 `.claude/settings.json` 或 `.claude/settings.local.json` 覆寫。頂層 `--model` 與 `ANTHROPIC_MODEL` 也會影響主 session；不要只查單一檔案就宣稱已找到實際來源。

### 6. 驗證標準

模型委派同樣做三層驗證：

- **CLI 直呼**：`claude --model <model> ... -p 'Reply exactly: OK'` 成功，且 `modelUsage` 含目標模型。
- **委派鏈路**：用與實際工作相同的 `--agents` definition 與 `@worker` 呼叫，subagent 回傳唯一 marker，且整體 JSON 的 `modelUsage` 含目標模型。只看到 coordinator 的成功文字不算通過。
- **預設路徑**：不帶頂層 `--model` 呼叫一次，確認 `~/.claude/settings.json`、專案 settings 與 `ANTHROPIC_MODEL` 合成後的預設路徑仍可用。

第三層若失效，所有省略頂層 `--model` 的 Claude 呼叫都可能失敗，包含依賴預設 coordinator 的自動委派。若 subagent definition 省略 `model` 或使用 `inherit`，它也會繼承這條失效路徑。驗證報告應記錄 CLI 版本、auth provider、alias 實際解析結果、`modelUsage`、exit code 與是否存在模型相關環境變數；這些是會過期的環境快照，只放工作日誌或 handoff，不寫進 playbook 正文。

---

## 待觀察與 Router 萃取研究

以下項目是非阻塞研究 backlog，**不是目前 workflow 的既定規則**。在取得可重複證據前，保持 playbook 為 `draft`，不要把假設寫進錯誤歸因表或自動切換模型。

### OBS-01：流量或配額耗盡時的委派回傳

待自然遇到 subscription usage、API quota 或其他 provider 配額耗盡時，觀察 CLI 直呼、跨 agent 委派與預設路徑是否回傳不同形態。不要為了完成觀察而刻意耗盡流量或付費點數。

每次樣本至少記錄：

- runtime、CLI 版本、auth provider 與不含私人帳務資料的方案類型
- 呼叫路徑：CLI 直呼、外部 worker、真正 subagent、背景 session 或預設路徑
- 指定的 alias / model ID，以及回傳的實際 `modelUsage`
- process exit code、HTTP / API status、完整錯誤 JSON、stderr、`retry-after` 或 cooldown 提示
- coordinator 是否成功啟動、worker 是否實際被呼叫、是否自動 fallback 到其他模型
- 同一最小 prompt 在另一 runtime 或另一可用模型是否成功
- 配額恢復後，同一路徑是否不改設定即可恢復

觀察結果應分類為：

| 分類 | 意義 |
|---|---|
| `distinct-response` | 配額耗盡有穩定、可辨識的專屬 status / error shape |
| `shared-response` | 與模型不存在、無權限或一般 4xx/5xx 共用訊息，無法單靠回傳細分 |
| `partial-signal` | 只有部分路徑、header、usage 欄位或 coordinator/worker 邊界能辨識 |
| `not-observable` | 委派回傳沒有可靠差異，必須依 provider 帳務或 usage surface 判斷 |

只有在至少一個方向取得可重複樣本後，才把對應 signature 加入前面的錯誤歸因表。一次性文字或 UI 通知只放工作日誌，不直接升級成耐久規則。

#### Claude 側補充判斷

以下第一點來自 Claude 對自家 runtime 的認識，依 RTR-01 的證據優先序屬於**模型自述（claim）**，取得自然樣本前不得寫入歸因表：

- （claim）Claude 的流量層錯誤預期有兩族不同形態：subscription 用量視窗耗盡（harness 層訊息，帶 reset 時間提示，可能不出現在 JSON error 欄位）與 API 層 `429 rate_limit_error` / `529 overloaded_error`（API error shape，可能帶 `retry-after`）。兩者觀察面不同，取樣時 auth provider 必須分開記錄，否則兩族樣本會互相污染。
- （結構判斷）同一個 CLI session 內的 coordinator 與 subagent 通常沿用同一 auth principal；委派本身不會建立新的 entitlement，因此**不能假設 subagent 能繞過原帳號的配額限制**。但「同一 auth principal」不足以證明 quota pool 的粒度：provider 仍可能依帳號、runtime、模型、access mode、時間窗或 credits 分池。同 runtime 換模型與跨 runtime fallback 都只能列為候選，是否有效須由 live probe 證明；配額狀態應同時記錄 `auth_principal`、`quota_scope`（未知時明記 `unknown`）、模型與 access mode，不能只以 runtime 為單位推定。

### OBS-02：新模型上線或計價／entitlement 轉換

模型剛上線、alias 改指新版本，或模型從 subscription included 轉為 credits / points / API-only 等模式時，委派可能出現三種情況：直接拒絕、成功但 usage / cost metadata 改變，或委派結果完全看不出計價模式。這些都是待觀察假設，不預先指定哪一種會發生。

使用同一個最小 prompt 做轉換前後或不同 entitlement 的對照，除 OBS-01 欄位外再記錄：

- alias 在當下實際解析到的 model ID
- CLI picker、官方 model catalog 或帳務 surface 顯示的 access mode
- response 中是否出現 cost、credits、service tier、fallback 或 entitlement 欄位
- CLI 直呼成功時，委派鏈路是否仍因 coordinator / worker 使用不同方案而失敗
- 不帶 `--model` 時，預設 alias 是否因轉換而改走另一模型

**成功回傳不等於仍屬訂閱流量，也不等於已扣點數。** 若 response 沒有 billing signal，應明確記為 `not-observable`，不要從 `total_cost_usd`、token usage 或模型名稱自行推算實際扣款。涉及實際付費探測前，先取得使用者同意並設定可接受的上限。

特定日期、剛上線的模型名與即將改制的商業資訊是觀察觸發快照，應留在工作日誌或 handoff；本節只保留可跨時間重用的轉換檢查方法。

#### Claude 側補充判斷

- **已預告的 entitlement 轉換是一次性自然實驗窗口。** 與 OBS-01 的「等自然遇到」不同，轉換常有已知日期；錯過轉換點就無法重建相同 entitlement 下的「轉換前」對照組。因此對照採樣值得在已知轉換日**之前**主動排程（同一最小 prompt + 同一呼叫路徑）。轉換前樣本只能稱為「目前 entitlement 內可用」，不能直接稱為免費；轉換後的第一次採樣若可能扣點數，先取得使用者同意。
- **alias 漂移與模型上線不同步。** `opus` / `sonnet` / `haiku` 這類 family alias 改指新版本的時點，和新模型可用的時點是兩個獨立事件。轉換觀察應同時記錄 alias 呼叫與精確 model ID 呼叫的結果，否則無法區分「模型行為變了」與「alias 指向變了」。
- **「後端已服務、本地 CLI 未認識」的窗口兩側都可能存在。** Codex 側已有實測形態（metadata fallback 警告、版本 gating 400）；Claude 側對應形態尚無樣本，遇到剛上線模型時記錄是否有等價的本地警告或版本 gating，補進第 3 節歸因表。

### RTR-01：Capability-Aware Model Router（提案）

未來萃取 skill 時，可考慮把「使用哪個 runtime / model」拆成 deterministic filter 加 LLM judgement 的 hybrid router。模型對自家模型族的特性描述可以是輸入，但不能作為唯一依據；模型知識可能落後於 rollout、alias 或帳號 entitlement。

建議證據優先序：

1. 使用者明確指定的 runtime、模型、預算、延遲或資料邊界。
2. 當下 CLI / provider 的 live availability、auth、quota 與 entitlement probe。
3. 官方 model catalog、runtime picker、CLI metadata 或 provider 文件。
4. 本地可追蹤的任務實績、eval、失敗率、延遲與成本紀錄。
5. 各 runtime 或模型對自身／對方模型特性的結構化自述；標記為 claim，不視為已驗證事實。

#### Claude 側補充判斷：模型自述的三個結構性邊界

原始發想是「各模型會知道自家當前哪幾個的特性／擅長點，可模板化取得」。Claude 側支持模板化，但自述有三個結構性邊界，模板設計必須內建，否則第 5 級證據會被高估：

1. **Training-memory coverage 盲點。** 若一條 claim 的唯一來源是 `training-memory`，且可驗證的 knowledge coverage / cutoff 早於候選模型上線日，該 claim 應判無效，而不是只降信心。但模型未必能可靠自述精確 cutoff；模板應要求填來源與 coverage，無可靠 metadata 時標成 `unknown`。若同一 claim 有 `harness-injected`、官方資料或 `live-probe` 證據，不能因 training cutoff 較早就一併否決，應分來源評估。
2. **家族不對稱性是 heuristic，不是硬規則。** 模板化取得自述時仍優先**各問各家**：向 Claude 取 Claude 家 claim、向 Codex 取 GPT 家 claim；純 `training-memory` 的跨家 claim 預設較低信心。但跨家 claim 若直接引用官方 catalog、runtime metadata 或 live probe，可依該證據本身提升信心，不應只因回答者屬於另一家就設固定上限。
3. **Harness 注入是獨立 provenance，不保證固定新鮮度。** runtime 的 system prompt 可能注入比 training memory 新的 model metadata，但內容仍可能簡化、延遲或只描述預設模型。自述模板應要求每條 claim 區分 `training-memory`、`harness-injected`、`official-catalog` 或 `live-probe`，並記錄可得的 `observed_at`；在未核對更新時間前，不要只因來源是 harness 就預設其證據等級必然介於官方 catalog 與模型記憶之間。

自述模板的最小輸出契約可直接沿用下方候選 schema：每條 claim 填 `strength_claims` 與 `confidence`，`observed_at` 填詢問時間，`evidence` 分別標注 `training-memory` / `harness-injected` / `official-catalog` / `live-probe`，不要把多來源壓成單一標籤。

Router 輸入至少包含：

- 任務類型：探索、實作、除錯、架構、review、長文整合或機械轉換
- 複雜度、不確定性、可逆性與錯誤成本
- 上下文量、工具需求、是否需要跨檔案修改或背景執行
- 延遲、成本、流量與點數限制
- 是否要求精確 model ID，或允許 family alias / fallback
- 資料邊界、provider 限制與人工確認需求

候選模型資料可先正規化為下列概念欄位；這只是 skill 萃取時的 schema 候選，不是目前已接受的 machine contract：

```json
{
  "runtime": "claude|codex|other",
  "model": "alias-or-model-id",
  "availability": "available|unavailable|unknown",
  "access_mode": "subscription|credits|api|unknown",
  "quota_scope": "account|runtime|model|access-mode|unknown",
  "strength_claims": [],
  "constraints": [],
  "evidence": [],
  "observed_at": "timestamp",
  "confidence": "low|medium|high"
}
```

建議 routing 順序：

1. 先套用使用者硬限制與資料邊界。
2. 排除 live probe 已確認不可用、配額耗盡或 entitlement 不符的候選。
3. 在剩餘候選中，依任務訊號選擇「足以完成任務」而非抽象上最強的模型。
4. 回傳選擇理由、證據新鮮度、信心、替代候選與是否需要先 probe。
5. 若只有低信心自述、會觸發付費點數、或 fallback 會違反使用者明確模型要求，停在 human decision gate。

Router 不應靜默覆寫使用者指定模型。未指定模型時，也不應每次都強制選模；只有任務特徵、成本／流量狀態或可用性證據足以改變預設路徑時，才啟動 routing judgement。

可考慮的 extraction map：

| Skill 候選 | Profile | 責任 |
|---|---|---|
| `cross-agent-model-delegation` | `hybrid` | root：決定是否需要跨 runtime 委派，整合 probe、router、執行與回報 |
| `cross-agent-model-probe` | `script` / `hybrid` | 收集版本、auth、availability、error shape、`modelUsage` 與 entitlement signal |
| `cross-agent-model-router` | `hybrid` | 依任務特徵與證據選候選，輸出理由、信心、fallback 與 human gate |

在 OBS-01 / OBS-02 沒有足夠樣本、候選 schema 與 routing eval 尚未穩定前，不建立上述 skills。

---

## Agent 行為規則

- 使用者沒有指定模型時，不要自行加上 `--model`。
- 不要把 `--model` / `--effort` 這類 runtime 參數當成任務文字傳給對方模型。
- 不要憑記憶宣稱某個模型可用或不可用；先探測，再回答。
- 不要把「本地 metadata 警告」當成「模型不可用」。
- 看到 Codex 400 或 Claude 404 時，先讀完整訊息再歸因；Codex 的 `requires a newer version`、`not supported ... account` 與 Claude 合併「不存在／無權限」的 404，能判定的粒度不同。
- 升級 CLI 之後委派仍失敗時，依 runtime 查殘留狀態：Codex plugin 查 broker；Claude 查 resume/background session、agent definition 是否重載與模型環境變數優先序。**不要不分方向地重複升級。**
- 不要直接修改 plugin cache 目錄下的檔案 — plugin 更新會覆寫，改動留不住。若真有需求，改上游或在 repo 內包一層。
- 修改對方 runtime 的設定檔（例如 `~/.codex/config.toml` 或 `~/.claude/settings.json`）前先備份，並在回報中說明備份位置。
- 若探測結果顯示需要升級帳號方案或處理 credential，回報邊界與使用者可自行執行的命令，不要自行操作。
- 不要為了觀察配額錯誤而刻意耗盡流量，也不要在未取得同意前用付費點數探測 entitlement 轉換。
- 不要把模型自述直接當成 router truth；至少與 live availability 或另一項可追蹤證據交叉檢查。
- 不要從共用 auth principal 直接推導共用 quota pool；quota scope 未經觀察時保持 `unknown`。
- 只有純 `training-memory` claim 才能依 knowledge cutoff / coverage 淘汰；harness、官方 catalog 與 live probe 證據應分開判讀。
- 驗證結果若含版本號、模型白名單這類會過期的事實，寫進工作日誌或 handoff，**不要寫進本 playbook 正文**。

## 標準 Prompt

```text
請依照 cross-agent model delegation 流程，確認目前環境能否把 subagent 工作指派給對方 runtime 的指定模型。先用不帶模型指定的最小呼叫確認鏈路可用，再逐一探測目標模型；若 Codex 回報 400 或 Claude 回報 404，請完整保留錯誤 JSON / 訊息並依各 runtime 已驗證的粒度歸因，不要把 Claude 合併的「不存在／無權限」訊息過度細分。確認模型可用後，分別驗證 CLI 直呼、委派鏈路與預設模型路徑三層。若剛升級過 CLI，Codex plugin 請檢查跨越升級點的 broker；Claude 請檢查 resume/background session、agent definition 重載與模型環境變數優先序。回報時請把「耐久的判斷規則」與「這次觀察到的版本與模型快照」分開列出。
```

## 建議輸出格式

```md
## 鏈路確認

- 不帶模型指定的最小呼叫:
- 結果:

## 模型探測

| 模型 | CLI 直呼 | 委派鏈路 | 錯誤訊息原文 |
|---|---|---|---|

## 歸因

- 成因分類:
- 處置:
- 已排除的可能:

## 三層驗證

- CLI 直呼:
- 委派鏈路:
- 預設模型路徑:

## 環境快照（會過期，不寫入 playbook）

- CLI 版本:
- 當下可用模型:
- 設定檔預設模型:
- 備份位置:

## 配額 / Entitlement 觀察（僅觸發 OBS-01 / OBS-02 時）

- 觀察項目:
- 呼叫路徑:
- response / exit code / status:
- `modelUsage` / fallback:
- billing signal:
- 分類（distinct / shared / partial / not-observable）:
- 是否為自然樣本或已核准的付費探測:

## Router 判斷（僅觸發 RTR-01 時）

- 任務訊號與硬限制:
- 候選模型與證據新鮮度:
- 選擇的 runtime / model:
- 理由與信心:
- 替代候選 / fallback:
- 是否需要 human decision:

## 交接

- 是否需要使用者處理（方案升級 / credential / 系統套件）:
- 是否應更新 playbook 的判斷規則:
```

## Skill 萃取候選

兩個方向目前都已有實際模型探測與委派鏈路證據，但錯誤歸因樣本仍少，**暫不立即萃取成 skill**。

待此流程在不同 CLI 版本、配額狀態或 entitlement 環境重複使用，且 provider/model 參數、structured output、候選模型 schema 與 routing eval 穩定之後，再依 RTR-01 的 extraction map 評估 root / probe / router skills。委派拓樸、兩種 runtime 的 session/daemon 陷阱、商業模式轉換背景與研究歷史留在本 playbook。
