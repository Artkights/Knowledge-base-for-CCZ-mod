# 双 AI 自动落盘：Codex notify 钩子 + 定时会话摘要

## 结论速览

- **Codex 侧已能"每轮自动落盘"**：`~/.codex/config.toml` 的 `notify` 指向 `大鲸鱼产生专用\_codex_notify.py`；
  它把每轮最后答复写进 `AI协作\会话摘要\codex-自动落盘-<日期>.md`，**并转发给原 computer-use 命令**（功能不受影响）。
- **会话摘要已定时重建**：计划任务 `CCZ-KB-Digest`（每 30 分钟）→ `_digest.cmd` → `_digest_run.py` → `_会话摘要.mjs`
  → `AI协作\会话摘要\<日期>.md`；实测 13:36:38 触发 / 13:36:40 出结果。
- **DSH 一步可读**：MCP 工具 `mcp__kb__digest_read`（读摘要）/ `digest_build`（立即重建）。
- **★ 血泪教训（.cmd 里绝不能有中文）**：中文 .cmd 在**计划任务**下表现为"任务成功(exit 0)但什么都没生成" ——
  cmd 按代码页解码 .cmd，node 收到乱码路径。**正确姿势：.cmd 全 ASCII + `%~dp0` 定位，中文路径交给 .py**。
- 仍然**做不到**"实时推送/上下文全互通"：两个 AI 都是"被叫醒才动"；能做的是把**落盘自动化**、把**读取降到一步**。

## 适用版本

- Codex CLI/桌面版 0.162.0-alpha.17.2（`notify` 字段 + `agent-turn-complete` 载荷，二进制内实测存在）
- DSH 桌面版；Node v24.21.0（自带 `zstdDecompressSync`）
- 计划任务 `CCZ-KB-Digest`：Administrator / Interactive / Limited

## 已确认事实

1. **Codex notify 载荷**：argv 里带一个 JSON，含 `type=agent-turn-complete` / `turn-id` / `last-assistant-message` / `input-messages`。
   `_codex_notify.py` 会把**原始 argv 全量记档**到 `大鲸鱼产生专用\_codex通知原始参数.log`（格式变了能立刻发现）。
2. **转发是必要的**：原 notify 是 `codex-computer-use.exe turn-ended`；新钩子内部再调它，保持行为不变。
3. **DSH 会话文件是"多帧 zstd 拼接"**：实测单个 `session.v4.jsonl.zstd` 含 **1019 个独立帧**，
   一次性解压只能拿到第一帧（会话头）⇒ 必须按魔数 `28 B5 2F FD` 切帧、逐帧解压。
4. **可抽取事件**：`user/message`→`data.content[].text`；`assistant/message`→`data.message.content[]`（挑 `type=text`）；
   `tool/call`→`data.name`；`time` 为毫秒时间戳。
5. **Codex 会话**：`~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`，每行 `{timestamp, ordinal, type, payload}`；
   `type=response_item & payload.type=message & payload.role∈{user,assistant}`。
6. **★ .cmd 中文坑（计划任务版）**：同一个 .cmd 手动跑正常、计划任务里"成功但无产物"（任务环境代码页不同）。
   根因 = .cmd 里写了中文路径；改 `"%~dp0_digest_run.py"` 后一次通过（`%~dp0` 运行时展开，文件本身纯 ASCII）。
7. **计划任务**：`-RepetitionDuration ([TimeSpan]::MaxValue)` 会报 `P99999999DT23H59M59S` 越界 ⇒ 用 `3650 天`；
   `schtasks /create /tr` 带引号路径在 PowerShell 里极易拆错 ⇒ 优先 `ScheduledTasks` 模块。

## 实现·使用方法

### Codex 每轮自动落盘（已接线）

```toml
# ~/.codex/config.toml
notify = [ '<python.exe 全路径>', '<工作区>\\大鲸鱼产生专用\\_codex_notify.py' ]
```

- 改动前备份：`~/.codex/config.toml.bak_before_notify_<时间戳>`（备份里的 notify 行是**原值**，可直接回滚）
- 产物：`AI协作\会话摘要\codex-自动落盘-<日期>.md`；诊断：`大鲸鱼产生专用\_codex通知原始参数.log`
- 自测（不必真跑 Codex）：用 Python 以真实 JSON 调用 `_codex_notify.py`

### 定时摘要（已注册）

```
schtasks /query /tn "CCZ-KB-Digest"                 :: 查看
Start-ScheduledTask -TaskName CCZ-KB-Digest         :: 立即跑一次
```

链路：`_digest.cmd`（纯 ASCII）→ `_digest_run.py`（中文路径在这里）→ `_会话摘要.mjs` → `AI协作\会话摘要\<日期>.md`；
日志：`大鲸鱼产生专用\_会话摘要_任务.log`（每次一行 `[时间] OK/FAIL`）。

### 两个 AI 怎么用

- **DSH**：`mcp__kb__digest_read` / `mcp__kb__digest_build`
- **Codex**：直接读 `AI协作\会话摘要\<日期>.md` 与 `codex-自动落盘-<日期>.md`（见 `AI协作\给Codex的常驻指令.md`）

## 风险与边界

- **notify 只覆盖"轮末"**：中途工具调用/思考不落盘；要完整过程仍看会话摘要。
- **摘要是有损的**：单条截断 160/220 字符，且只覆盖最近 N 小时（默认 12）。
- **摘要文件是只读产物**：每次重建会覆盖当天文件，人/AI 都不要手改。
- 摘要器会扫到所有会话（含子代理），DSH 侧按 `cwd == 本工作区` 过滤。
- `.cmd` 一律纯 ASCII + `%~dp0`：以后所有计划任务/自启动封装都照此办理。

## 证据来源

- 工具源码：`大鲸鱼产生专用\_会话摘要.mjs`、`_digest.cmd`、`_digest_run.py`、`_codex_notify.py`
- 实测：`_会话摘要_任务.log` = `[2026-10-15 13:36:40] OK … DSH 会话 6 个 / Codex 会话 49 个 / 共 1769 行`
- notify 自测：`_codex通知原始参数.log` 的 `test-2` 行（真实 JSON）+ `codex-自动落盘-2026-10-15.md` 已写入
- 计划任务：`Get-ScheduledTaskInfo -TaskName CCZ-KB-Digest` → LastRunTime 13:36:36 / LastTaskResult 0
- 相关页：`Codex与DSH协同-共享知识库与MCP.md`、`Git版本管理与GitHub共享方案.md`

## 待验证项

- **P1**：Codex **真机回合**触发 notify 的端到端证据（本轮代理 `127.0.0.1:1088` 未运行、`codex exec` 连不上，没测成）。
- **P2**：摘要里混入了 Codex 子代理/内部评估的 rollout，是否需要按 `session_meta` 过滤。
- **P2**：30 分钟是否过频（单次约 1.5 秒，可按需改 60 分钟）。
