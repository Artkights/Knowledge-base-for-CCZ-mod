# TRAE 接入 MCP：x64dbg 调试桥 + 本地知识库（第三个 AI）

## 结论速览

1. **TRAE SOLO 已通过 MCP 接上同一份磁盘数据**（不是副本）：`kb` 服务 23 个工具、`x64dbg` 服务 81 个工具，合计 104 个。
2. **x64dbg 的 MCP 端点必须带 `/sse`**：`htt[本地盘]//127.0.0.1:3000/sse`。裸地址 `htt[本地盘]//127.0.0.1:3000` 只返回健康检查 JSON `{"status":"ok","service":"x64dbg-mcp"}`，**不是 MCP 端点，填了连不上**。
3. `kb` 用 stdio（Python 直接起脚本），**不需要 `cwd`** —— 脚本用 `__file__` 定位 ROOT，实测带/不带 cwd 都能正常 `initialize` + `tools/list`。
4. **TRAE 手动配置一次只能保存一个 server**（实测报错原文「每次只能保存一个 MCP Server 配置」），必须**分两次贴**：
   - `[本地盘]\Users\Administrator\Desktop\trae-mcp-1-x64dbg.json`（89 B）
   - `[本地盘]\Users\Administrator\Desktop\trae-mcp-2-kb.json`（398 B）
   - 合并版 `trae-mcp-config.json` 仅作存档，**不能直接贴给 TRAE**。
5. `x64dbg` 的 3000 端口**随 x32dbg 启动**而存在，调试器没开就必然连不上。

## 适用版本

| 项 | 版本/路径 |
|---|---|
| 客户端 | TRAE SOLO（MCP 设置 → 本地 → 手动配置，粘贴 JSON） |
| x64dbg MCP | `x64dbg-mcp 1.0.11`（插件，随 x32dbg 启动） |
| kb MCP | `kb 1.0.0`（`大鲸鱼产生专用\_知识库MCP服务.py`，65 KB，2026-10-17） |
| Python | `[本地盘]\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe` |
| 其他 AI | DSH、Codex 与本服务共用同一 `ai使用库` |

## 已确认事实（均为实测，非推断）

- 端口 3000 监听中，进程 `x32dbg`（`[本地盘]\新建文件夹\snapshot_2026-05-27_12-11\release\x32\x32dbg.exe`）。
- `GET /` → 200 `{"status":"ok","service":"x64dbg-mcp"}`（**健康检查**）；`GET /health`、`/tools` → 404。
- `GET /sse` → `text/event-stream`，首帧 `event: endpoint` / `data: /message`（标准 MCP SSE 传输）。
- `POST /message` + `initialize` → **202**；同一 SSE 流回 `{"serverInfo":{"name":"x64dbg-mcp","version":"1.0.11"}}`。
- `POST /message` + `tools/list` → **81 个工具**，含 `breakpoint_*`（set/delete/enable/set_condition/set_log/reset_hitcount）、`debug_*`（attach_pid/run/pause/restart/get_state/init）、`assembler_assemble`、`context_get_snapshot`/`context_compare_snapshots`、`bookmark_*`、内存/寄存器读写。
- `kb` stdio `initialize` → `{"serverInfo":{"name":"kb","version":"1.0.0"}}`；`tools/list` → **23 个工具**：`kb_index`/`kb_search`/`kb_read`/`kb_list`/`kb_recent`/`kb_write_page`/`ledger_read`/`ledger_append`/`handoff_read`/`handoff_write`/`memory_*`（7 个）/`digest_read`/`digest_build`/`exe_info`/`exe_bytes`/`sample_timeline` 等。
- `kb` 脚本内含 `ROOT = os.path.dirname(HERE)`，**无 cwd 依赖**；带 cwd 与不带 cwd 两种方式握手结果完全一致。
- 中文路径（`曹操传6.6-V7.30 解压密码：66\复刻版6.6山贼\...`）在 JSON 里必须以 `\\` 转义且原样保留，不能改写或省略空格。
- **TRAE 的注册文件 `%APPDATA%\Trae CN\User\mcp.json` 里同时存在 `x64dbg` 与 `kb` 两个 key**（2026-10-21 13:34:15 修改）⇒ **分两次贴不会互相覆盖**，TRAE 会合并进同一个 `mcpServers`；反倒是「合并 JSON 一次贴」被对话框拒（见上一条）。
- 工具名带 server 前缀：TRAE 会话里显示为 `mcp_kb_*` / `mcp_x64dbg_*`（不是裸的 `kb_index`）。
- kb 的 stdio 进程实测由客户端各自拉起：`codex.exe` → pid 9092、`DeepSeek Harness.exe` → pid 19840、`Trae CN.exe` → pid 7788（父进程 5656），**三个独立实例**。
- x64dbg MCP 的连接由 `Trae CN` 持有（`127.0.0.1:49427 → 3000`，Established）。
- **TRAE 的「手动配置」是单 server 校验**：一次贴两个（`{"mcpServers":{"a":...,"b":...}}`）会被拒，红框 + 报错「每次只能保存一个 MCP Server 配置」，**确认按钮点不动**；拆成两个只含一个 key 的 JSON 分别贴即可。

## 实现·使用方法

### 1) 配置 JSON（可直接粘贴到 TRAE「手动配置」）

```json
{
  "mcpServers": {
    "x64dbg": {
      "url": "htt[本地盘]//127.0.0.1:3000/sse"
    },
    "kb": {
      "command": "[本地盘]\\Users\\Administrator\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe",
      "args": [
        "[本地盘]\\ccz\\曹操传6.6-V7.30 解压密码：66\\复刻版6.6山贼\\大鲸鱼产生专用\\_知识库MCP服务.py"
      ],
      "env": {
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

### 2) 若 TRAE 报「缺少 type 字段」

```json
{
  "mcpServers": {
    "x64dbg": { "type": "sse", "url": "htt[本地盘]//127.0.0.1:3000/sse" }
  }
}
```

### 3) 自检命令（连不上时按顺序排查）

```powershell
# ① 调试桥活着吗
curl.exe --noproxy '*' htt[本地盘]//127.0.0.1:3000/

# ② MCP 端点通吗（应看到 event: endpoint）
curl.exe --noproxy '*' -N --max-time 3 htt[本地盘]//127.0.0.1:3000/sse

# ③ 3000 端口是谁在听
Get-NetTCPConnection -LocalPort 3000 -State Listen | ForEach-Object { Get-Process -Id $_.OwningProcess }

# ④ kb 脚本与 python 是否都在
Test-Path '[本地盘]\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe'
Test-Path -LiteralPath '[本地盘]\ccz\曹操传6.6-V7.30 解压密码：66\复刻版6.6山贼\大鲸鱼产生专用\_知识库MCP服务.py'
```

### 4) 给 TRAE 的开场白（建议原样发给它）

> 开工先调 `memory_bootstrap` 拿铁律，再 `handoff_read` 看当前交接；收工用 `ledger_append` 记一行（who=TRAE）。

## 风险与边界

- **3000 端口依赖 x32dbg 进程**：调试器关闭后 TRAE 侧工具全失效，但 TRAE 不一定报错，可能只是"没有工具"。
- **三方并发写知识库**：DSH / Codex / TRAE 共用同一目录。同一页以**最后写入**为准，`kb_write_page` 自带备份但**不合并**；改前先 `kb_read`。
- **三个 kb 实例同时常驻**（2026-10-21 实测：codex pid 9092 / DSH pid 19840 / TRAE pid 7788）⇒ `ledger_append` 是追加写相对安全，但**同一页并发 `kb_write_page` 会互相覆盖**；`memory_*` 的 JSONL 追加同理。真要并行干活时，按"谁先认领谁写"分工，别同时改同一页。
- **写 `Ekd5.exe` 的红线不变**：必须走 `大鲸鱼产生专用\_dsh写锁.py`，本 MCP 不提供写 EXE 的能力（只有只读 `exe_bytes`/`exe_info`）。
- **战斗类测试铁律不变**：任何伤害/暴击/闪避/连击测试，前置条件必须是**集气模式 `4018=1`**。
- **127.0.0.1 只对本机有效**：TRAE 若装在别的机器/容器里连不上，需改用内网 IP 并确认插件绑定地址。
- **`/sse` 是长连接**：浏览器直接打开会一直挂着（curl 会超时退出），这是正常现象，不是故障。

## 证据来源

- 实测（2026-10-21 13:2x）：`GET /`、`GET /sse`、`POST /message`（initialize/tools/list）的 HTTP 码与响应体；`tools/list` 返回 81 项工具名。
- 实测（同日）：kb stdio 双路握手（带 cwd / 不带 cwd）各得 `kb 1.0.0` + 23 工具。
- 文件：`[本地盘]\Users\Administrator\Desktop\trae-mcp-config.json`（462 字节，`json.load` 往返校验通过）。
- 交接：`ai使用库\AI协作\交接.md` §「第三个 AI 接入：TRAE SOLO」。
- 台账：2026-10-21 13:3x 条目。

## 待验证项

0. **已解决（2026-10-21 13:36 用户截图）**：TRAE「MCP Servers 管理」列表同时出现 `kb` 与 `x64dbg`，两条均带绿勾、开关为开 ⇒ **接受无 `type` 的 `url` 条目**；**stdio 的 `env` 未阻断启动**（kb 能加载）。剩余：逐行展开核工具数。
1. ~~TRAE 的 MCP 客户端是否接受无 `type` 的 `url` 条目~~ → **接受**（x64dbg 仅 `url` 即通过）。
2. ~~TRAE 的 stdio 服务是否继承 `env` 字段~~ → **未阻断**（kb 已加载）；但中文路径是否真被正确解析，需调一次 `kb_index` 才算闭环。
3. ~~工具数量与前缀~~ → **已确认**：TRAE 会话工具列表显示为 `mcp_kb_*` / `mcp_x64dbg_*`（带 server 前缀）；kb 的 stdio 进程由 `Trae CN.exe` 拉起（pid 7788 / 父 5656），x64dbg 连接由 TRAE 持有（`49427 → 3000` Established）。
4. 三方同时跑 `digest_build` 是否会争用同一个摘要文件（尚未验证）。
