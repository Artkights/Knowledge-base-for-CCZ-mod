# Codex CLI 两条通道与中转成本

## 结论速览

- Codex CLI 有**两条互不相通的凭据通道**，本机均已实测可用（2026-10-15）。
- **默认走官方 ChatGPT / Plus 订阅**（包月不限次，日常一律用这条）。
- **中转 `ai.gmncode.com` 已配好可用**，但**同一次极短对话实测贵 6.4 倍**（2,589 → 16,689 tokens）。
- 原因：中转要做 Responses→Chat 协议转换，**每次请求都把整个系统提示 + 工具定义重发一遍**。
- **中转只在 Plus 额度撞墙时兜底**；日常不要用，否则按量扣钱且性价比极差。
- ⚠️ Codex CLI（Rust/reqwest）**不读 Windows 系统代理**，只认 `HTTP_PROXY`/`HTTPS_PROXY` 环境变量。

## 适用版本

- 与游戏版本无关，纯工具链配置。适用本机 Codex CLI `0.162.0-alpha.17.2`。
- 样本无关；结论不随 `Ekd5.exe` SHA 变化。

## 已确认事实

### 1. 两条通道对比（实测 2026-10-15）

| | **① 官方 ChatGPT / Plus** | **② 中转 ai.gmncode.com** |
|---|---|---|
| 凭据 | `~/.codex/auth.json` 的 OAuth token | `GMNCODE_API_KEY` 环境变量 |
| 服务端 | `chatgpt.com/backend-api` | 中转站服务器 |
| 计费 | **Plus 月费（$20 包在内）** | **中转余额（按 token 扣）** |
| 模型 | `gpt-6.1-sol` 等官方档位 | relay 映射的 7 个档位 |
| 同题 token 消耗 | **2,589** | **16,689（6.4×）** |
| 合规 | 官方允许 | 违反 OpenAI 用户协议 |
| 数据 | 直连 OpenAI | 经过第三方服务器 |

**两条通道互不相通**：用中转不会消耗、也不保护 Plus 额度。

### 2. 中转站可用模型（实测 `/v1/models` 返回 200）

```
gpt-5.5    gpt-5.6    gpt-5.6-sol    gpt-6
gpt-6-astra    gpt-6-sol    gpt-6.1-sol
```

注意：**没有 Luna 档位**（`gpt-5.6-luna` 不在列表里），所以中转上无法用鹈鹕测试做降智基线对比。

### 3. 端到端实测记录

| 测试 | 命令 | 结果 |
|---|---|---|
| 密钥有效性 | `curl -H "Authorization: Bearer $KEY" /v1/models` | ✅ 200，7 个模型 |
| 中转直连对话 | `curl -X POST /v1/chat/completions` | ✅ `RELAY_OK`，usage 4134 |
| **Codex 走中转** | `codex exec -c model_provider="gmncode" -m "gpt-6-sol" ...` | ✅ `provider: gmncode`，`RELAY_VIA_CODEX_OK` |
| **Codex 走官方** | `codex exec ...` | ✅ `provider: openai`，`OFFICIAL_CHANNEL_OK` |

### 4. 配置位置

| 项 | 位置 |
|---|---|
| 中转 provider | `~/.codex/config.toml` 的 `[model_providers.gmncode]`（`base_url`/`env_key`/`wire_api="responses"`） |
| 中转密钥 | 用户环境变量 `GMNCODE_API_KEY`（67 字符） |
| 代理 | 系统代理 `127.0.0.1:1088`（桌面版用）+ 环境变量 `HTTP_PROXY`/`HTTPS_PROXY`/`ALL_PROXY`（CLI 用） |
| provider 备份 | `~/.codex/config.toml.bak-before-relay` |

⚠️ `config.toml` 里的 `model_provider = "gmncode"` **是注释状态** ⇒ 默认走官方。
若要改默认，取消该行注释，但**不建议**（会让日常调用走贵 6 倍的中转）。

## 实现/使用方法

### 封装脚本 `大鲸鱼产生专用\_codex.cmd`

自动定位 `codex.exe`（版本目录 hash 会随自动更新变化）、自动注入代理与 relay 密钥。

```bat
rem 官方 Plus（默认，日常用）
_codex.cmd exec "你的提示词"

rem 中转（Plus 额度用完时兜底）
_codex.cmd exec --relay "你的提示词"

rem 查看状态（exe 路径 / 登录状态 / 密钥 / 代理端口）
_codex.cmd status

rem 列出中转可用模型
_codex.cmd relay-model
```

脚本会在执行前打印所用通道，例如：
`[codex] channel=relay  model=gpt-6-sol  (pay-per-token, ~6.4x cost)`

### 直接调用（不用封装脚本）

```powershell
$env:HTTPS_PROXY="htt[本地盘]//127.0.0.1:1088"; $env:HTTP_PROXY=$env:HTTPS_PROXY
$cli = "$env:LOCALAPPDATA\OpenAI\Codex\bin\<hash>\codex.exe"

# 官方
& $cli exec "..."

# 中转
& $cli exec -c model_provider="gmncode" -m "gpt-6-sol" "..."
```

## 风险与边界

1. **成本失控风险（最重要）**：中转按量扣钱且贵 6.4 倍。让 agent 自动 fallback 到中转，
   可能在无人在场时把余额烧光。**建议保持手动切换**，或至少让每次切换都在日志里留痕。
2. **合规风险**：用中转违反 OpenAI 用户协议；若与 Plus 账号同 IP 同账号混用，
   有触发风控的可能。**要用于敏感任务时，用独立的密钥与账号。**
3. **数据外泄**：中转请求经过第三方服务器。**不要用它处理未发布的 MOD 工程或私有代码。**
4. **降智风险**：中转普遍存在用小模型冒充大模型的情况。本项目无 Luna 基线，
   无法用鹈鹕测试对比 ⇒ **对输出质量要求高时不要用中转**。
5. **代理依赖**：`codex` CLI 不读系统代理，只认环境变量。HZVPN 没跑（1088 无监听）时
   两条通道都会失败 —— 这是**通道前提**，不是密钥问题。

## 证据来源

- 实测命令与返回：本页「已确认事实 3」四条测试记录（2026-10-15）。
- 配置：`~/.codex/config.toml`、`HKCU\Environment` 的 `GMNCODE_API_KEY`。
- 封装脚本：`大鲸鱼产生专用\_codex.cmd`（本页「实现/使用方法」）。
- 脚本惯例参考：`大鲸鱼产生专用\_git.cmd`（ASCII-only、PATH-free）。

## 待验证项

- [ ] 中转余额还剩多少（未查到余额接口；需登录 `http[本地盘]//ai.gmncode.com/keys` 查看）。
- [ ] Codex CLI 报「额度耗尽」时的**具体错误格式** —— 决定能否安全地做自动 fallback。
- [ ] 中转上 `gpt-6-astra` 是否为真货（需自建基线，无法用 Luna 对比）。
## 2026-10-21 追加：每回合 "Reconnecting 1/5 … 5/5" 的根因与修法（`respect_system_proxy`）

**现象**：每个回合先刷 `Reconnecting 1/5 … 5/5`（数十秒～几分钟），之后照常出答案；**次数固定为 5，且最终总能成功**。

**日志判据**（Codex `0.163.0-alpha.10.2`，读 `~/.codex/logs_2.sqlite` 的 target 字段，2026-10-21 现读）：
- `codex_core::responses_retry`：`stream disconnected - retrying sampling request (1/5 … 5/5) ... sampling_error=request timed out`
- 紧随 `codex_core::client`：`falling back to HTTP`（WebSocket 传输失败后回退 HTTP）
- 同刻 `codex_http_client::request` 已是 `transport="responses_http"` 且能拿到 Cloudflare 响应头 ⇒ **网络本身通**，失败发生在「直连 / WebSocket 握手」阶段
- 客户端提示文案在 `codex.exe` 内为 `Reconnecting... %d/%d`

**根因**：内置 provider `openai` 默认 `supports_websockets=true`，而 `respect_system_proxy` 默认 `false`（`codex features list` 显示 `under development / false`）⇒ 在必须走代理的网络里先直连超时，按 `stream_max_retries=5` 重试完才回退 HTTP / 代理。

**修法**（`~/.codex/config.toml`，官方特性开关；改完**必须重启 ChatGPT/Codex**）：

```toml
[features]
respect_system_proxy = true
```

- 判据：`codex features list` 中 `respect_system_proxy` 由 `false` → **`true`**；`codex doctor` 报 `✓ config loaded`。
- 回滚：改动前备份 `[本地盘]\Users\Administrator\.codex\config.toml.bak_before_respect_proxy_20261021-2048`（改前 SHA `1851242C…` → 改后 `176DA338…`，只多该 4 行）。

**边界（实测，2026-10-21）**：
- 内置 provider ID **不能覆盖**：`[model_providers.openai]` 写任何字段都报
  `model_providers contains reserved built-in provider IDs: openai. Built-in providers cannot be overridden.`
  ⇒ 无法直接给内置 provider 加 `supports_websockets=false`。
- `responses_websockets` / `responses_websockets_v2` 在 0.163 已是 `removed`（有效值 false），**不是**可用开关。
- 备选路线（已在临时 `CODEX_HOME` 实测可把 transport 切到 `responses_http`，但**未采用**）：自定义 provider
  `openai-http`（`base_url=http[本地盘]//chatgpt.com/backend-api/codex`、`wire_api=responses`、`requires_openai_auth=true`、`supports_websockets=false`、**不设 `env_key`**）；风险是模型目录拉取与桌面端 provider 路由变化。

**未验证**：重启后的实机回合对照（判据 = `logs_2.sqlite` 里 `responses_retry` 不再出现）。
## 2026-10-25 追加：429「exceeded retry limit」来源定案（与本页两条 Codex 通道无关）

- **现象**：21:51:32 桌面端把 `exceeded retry limit, last status: 429 Too Many Requests` 作为首条输入注入新会话（query_source=sdk，不是用户手打）。
- **证据**（现读 `~/.qoder-cn/logs/runs/2026-10-25T19-43-47-591+08-00-nv9vc6-p33096/qodercli.log`）：
  - 旧会话 `49503407…` 在 21:34:47~21:51:17 共 69 条 `model.request.attempt_failed`：`error_code="model_queued"`、`status=403`、`{"code":"10605","modelKey":"qfmodel","retryAfterSeconds":30,"subCode":"CALL_COUNT_LIMIT","isQueued":true}`、`retryable=false`。
  - 同段 21:51:18/28/31/32 与 21:53:44，`GET http[本地盘]//gateway.qoder.com.cn/api/v5/service/region/endpoints` 经 `proxyUrl=htt[本地盘]//127.0.0.1:1088`（进程 xray.exe）报 `UND_ERR_CONNECT_TIMEOUT`。
  - 旧会话模型统计：qfmodel 652 次 / dfmodel 52 次；新会话（dfmodel）本轮 `model.response.completed` 正常。
- **结论**：429 来自 **Qoder 自家模型网关**（qfmodel 的调用计数/排队限制，叠加代理连接超时拉长重试），**不是**官方 Plus，**不是** `ai.gmncode.com` 中转，也不是工作区脚本。**不要**因此切 Codex 中转（贵 6.4 倍且无关）。
- **处置顺序**：① 降低同账号并发（旧会话 + recap + skill-evolution 分支同跑）并等 30s 重试；② 视需要给 `gateway.qoder.com.cn` 加代理例外（系统级改动，需用户批准）；③ 换 dfmodel。

## 2026-10-30 19:18 追加：中转模型目录已扩容到 11 个（含 gpt-6.1-sol / gpt-5.6-terra），两档实跑通

- 现读 /v1/models（走 1088 代理与直连均 HTTP 200）= 11 个，比本页第 2 节记录的 7 个多 4 个：
  gpt-5.3-codex-spark / gpt-5.5 / gpt-5.6 / gpt-5.6-luna / gpt-5.6-sol / gpt-5.6-terra /
  gpt-6(Astra) / gpt-6-astra / gpt-6-luna / gpt-6-sol / gpt-6.1-sol。
  ⇒ 本页第 2 节「没有 Luna 档位」已被证伪（现有 5.6-luna / 6-luna 两个），鹈鹕降智基线对比现在可做。
- 实测（2026-10-30 19:18，codex exec --skip-git-repo-check -m <model> -c model_provider=gmncode "只回复四个字：通道正常"）：
  - gpt-6.1-sol：EXIT=0，正文「通道正常」，tokens used 32,307；
  - gpt-5.6-terra：EXIT=0，正文「通道正常」，tokens used 27,279。
  ⇒ 两档都是真能出话的，不是列表里挂着而已。
- 成本口径再确认：4 个字的回答就吃掉 2.7~3.2 万 token（Responses→Chat 转换把系统提示 + 工具定义整包重发）。
  ⇒ 仍是「Plus 撞墙才兜底」，不是日常通道。
- 凭据不可互换（回答「能不能拿 Codex 的 key 用中转」）：中转只认它自己签发的 GMNCODE_API_KEY
  （本机 67 字符、sk- 前缀，存于 HKCU\Environment）；官方通道只认 ~/.codex/auth.json 的 OAuth。
  一条命令判定手里那把 key 属于哪边：curl -H "Authorization: Bearer <key>" http[本地盘]//ai.gmncode.com/v1/models ⇒ 200 才算中转 key。
- 脚本现状：_codex.cmd 的 RELAY_MODEL 硬编码 gpt-6-sol（第 51 行）⇒ 要换 6.1-sol / terra 必须
  走裸命令 codex exec -c model_provider=gmncode -m "gpt-6.1-sol" ...，或给脚本加 --model 透传（尚未改）。
- 附带噪声（与本页主题无关）：config.toml 的 request_max_retries / stream_max_retries 已被 0.16x 判为 unrecognized 并忽略。

## 2026-10-30 追加（重要纠正）：6.1 系模型**官方 key 就有**，不是中转独有；桌面端列表来自 models_cache.json

- 官方 key（`sk-proj-` **项目密钥**，存于 `~/.codex/auth.json` 的 `OPENAI_API_KEY`，164 字符）实测：
  `GET http[本地盘]//api.openai.com/v1/models` ⇒ **200**，字段数 **130**，其中含 **`gpt-6.1-sol` / `gpt-6.1-terra`**（还有 `gpt-6-sol`/`gpt-6-astra`/`gpt-6-luna`/`gpt-5.6-sol`/`gpt-5.6-terra`/`gpt-5.6-luna`/`gpt-5.3-codex`/`gpt-5.1-codex-max`）。
  同把 key 打中转 `ai.gmncode.com/v1/models` ⇒ **401 `INVALID_API_KEY`**。
  ⇒ 上一条“要 6.1-sol 只能走中转”的说法**作废**：官方直连即可，且不吃中转那 6.4 倍溢价。
  ⇒ 真实计费也验过：`gpt-5-mini` + `max_completion_tokens` ⇒ 200，`total_tokens 23`（注意 `max_tokens` 已被拒，必须用 `max_completion_tokens`）。

- **桌面端“模型下拉里没有新模型”的机制**（本次实查）：列表数据源是 `~/.codex/models_cache.json`，
  顶层字段 `fetched_at / etag / client_version / identity / models[]`，每条模型用 **`slug`**（不是 `id`）+ `display_name` + `priority` + `context_window`。
  该文件**只在客户端启动时读一次** ⇒ 服务端新增模型后，必须**完全退出 Codex 再打开**（只关窗口不够）。
  现读值：`client_version=0.163.0`、共 10 条，`gpt-6.1-sol` priority=1 / `gpt-6.1-terra` priority=3（均 500k 上下文），`gpt-6-luna` priority=5（272k）。

- **config.toml 三项优化（2026-10-30，备份 `config.toml.bak_before_optimize_20261030-193122`，改前 SHA 前 16 位 `A429AF7AF690C22B`）**：
  1. `model = "gpt-6-luna"` → **`"gpt-6.1-sol"`**（理由：priority 1 + 500k；`codex exec -m gpt-6.1-sol` 官方通道 EXIT=0）。
  2. 删除 `stream_max_retries` / `request_max_retries` —— 0.163 已判 unrecognized 并**忽略**，留着误导。
  3. 新增顶层 `suppress_unstable_features_warning = true`（`respect_system_proxy` 属 under-development，每次启动刷警告）。
  4. `[plugins."stop-that-shit@stop-that-shit"]` 的 `enabled` **true → false**（注释早已写“已关闭”，值与注释矛盾；症状 `hook: UserPromptSubmit Failed`）。
  **验收判据**：`codex doctor` ⇒ `config.toml parse ok`、`model gpt-6.1-sol · openai`；不带 `-m` 的 `codex exec` ⇒ EXIT=0 且 output 里不再出现 `is ignored` / `unstable features` / `hook ... Failed`。

### 2026-10-30 附录：插件精简实测只省 5.5%（同一句话 token 对照）

- 关掉 9 个插件（browser / computer-use / unified-computer-use / visualize / documents / pdf / spreadsheets / presentations / template-creator）后，
  `codex exec "回复一个字：好"` 的 `tokens used` **30,330 → 28,676（−1,654，−5.5%）**。
- ⇒ 结论：那 ~3 万底座的大头是**系统提示本体 + 工作区 AGENTS.md + 技能目录**，不是插件工具定义。
  **省 token 的杠杆是轮次与 reasoning effort，不是关插件**（此前“关插件省一大截”的估计偏乐观，已按实测修正）。
- 用户裁决（2026-10-30）：不设预算限制、插件全部恢复（`enabled=true` 11 个）；`stop-that-shit` 仍为 false（它的问题是 hook 报错，与省 token 无关）。

## 2026-10-31 追加：Codex 网络体检口径（端点、判据、实测耗时）

- 两个端点别混：①对话 `http[本地盘]//api.openai.com/v1/responses`（模型描述 `prefer_websockets: true`，首选 wss，失败回退 HTTP）；
  ②模型清单 `http[本地盘]//chatgpt.com/backend-api/codex/models?client_version=0.163.0`（必须带 `Authorization: Bearer`，不带凭据一律 403，不是网络问题）。
- 实测耗时（2026-10-31 16:0x，本机 1088）：`api.openai.com/v1/models` 直连 3.8s（DNS 0.01／TLS 2.35）/ 经代理 3.8s；
  模型清单 直连 5.5s / 经代理 12.5s；wss 直连 101 但握手 20s，经代理超时。
- 日志判据（`~/.codex/logs_2.sqlite` 的 `logs` 表，正文在 `feedback_log_body` 尾部）：
  `codex_core::responses_retry` + `stream disconnected - retrying (n/5) ... sampling_error=request timed out`，
  同时出现 `codex_api::endpoint::responses_websocket` 的 `connecting to websocket: ws[本地盘]//api.openai.com/v1/responses`
  ⇒ wss 走不通，界面表现「正在重新连接 5/5 · request timed out」。
- `codex_models_manager::manager` + `failed to refresh available models: request timed out` ⇒ **非致命**：
  清单接口 5.5s 仍超过客户端内部超时，退回 `~/.codex/models_cache.json`，只让下拉不更新，不影响对话。
- 处置：`NO_PROXY` 追加 `chatgpt.com,api.openai.com,*.openai.com`（直连 5.5s vs 代理 12.5s），对 models 刷新超时无效（客户端写死超时，无配置旋钮）；
  `openai-http` provider（`supports_websockets=false`）**实验失败、不采用**（一次缺 `OPENAI_API_KEY`、一次 200s 未返回），配置块保留但 `model_provider` 仍注释。
- 踩坑：改 `NO_PROXY` 时曾**直接覆盖**原值丢掉 70+ 条名单 ⇒ **改 PATH/NO_PROXY 类变量必须先读原值再追加**，改完回读长度与关键项自检。
