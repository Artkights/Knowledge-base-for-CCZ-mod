# Codex ⇄ DSH 协同：共享知识库与 MCP（kb）

## 结论速览

- **规则层零迁移**：Codex 在项目根自动读 `AGENTS.md`（实测 `codex debug prompt-input` 的模型可见输入里已含本库的 `4018=1`、`小暗` 等条目）⇒ 不需要为 Codex 另写一套规则。
- **知识层零迁移**：知识库就是磁盘上的 Markdown，两个 AI 读同一批页面、写同一批页面；"共享"= 同一份文件 + 同一组 MCP 工具。
- **Codex 的 MCP 只认 `~/.codex/config.toml`**（`[mcp_servers.*]`）。**项目级 `.codex/config.toml` 在 0.162 不生效**（`codex mcp get kb` 实测找不到）。
- **DSH 的 MCP 客户端是随包的 `@deepseek-ai/dsh-mcp-client`，默认不启用任何服务器**；在 `cordis.patch.yml` 插 `mcp-kb` 条目后 **必须重启 DSH** 才生效。
- 两边工具名同形：`mcp__kb__<tool>`；服务脚本 `大鲸鱼产生专用\_知识库MCP服务.py`（纯标准库、只读优先、**没有任何写 EXE 的能力**）。
- **协议兼容关键**：DSH 客户端连接前先发 `server/discover` 探测代际；本服务回 `-32601` ⇒ 被判 legacy ⇒ 走经典 `initialize`（应答版本 `2025-11-25`）。

## 适用版本

- **Codex**：CLI `0.162.0-alpha.17.2`（`[本地盘]\Users\Administrator\AppData\Local\OpenAI\Codex\bin\9614f1d9b40d9c4f\codex.exe`）、桌面版 `26.1007.71326`（`CODEX_HOME=[本地盘]\Users\Administrator\.codex`）。
- **DSH**：asar 内 `@deepseek-ai/dsh-mcp-client@0.2.0-rc.2`（支持协议 `2025-11-25` / `2026-07-28`）、`@modelcontextprotocol/client@2.0.0`。
- **python**：`[本地盘]\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`（自带 pefile/capstone/keystone）。
- 本页只适用于本工作区（复刻版 6.6 山贼）；换样本/换版本要重跑自检。

## 已确认事实

1. **Codex 读 AGENTS.md**：`codex debug prompt-input '测试'`（工作目录 = 本工作区）输出中 `4018` 出现 6 次、`小暗` 9 次、`复刻版` 5 次 ⇒ 指令层已共享。
2. **项目级 Codex 配置不生效**：本工作区 `.codex/config.toml` 写好 `[mcp_servers.kb]` 后，`codex mcp get kb` 仍报 `No MCP server named 'kb' found`；`codex mcp list` 只显示用户级配置里的服务器。
3. **Codex 注册方式**：`codex mcp add kb --env PYTHONUTF8=1 -- <python> <脚本>` ⇒ 写入 `~/.codex/config.toml`；`codex mcp list` 显示 `kb ... Status=enabled`。中文路径按 UTF-16 码点核对过：`66F9 64CD 4F20` = 曹操传（不是乱码）。
4. **DSH 工具命名**：`mcp__<serverName>__<rawName>`，与 Codex / Claude Code 同形（取自 `dsh-mcp-client/README.zh.md`）。
5. **DSH 版本协商**：客户端先发 `server/discover`；SDK 的 `classifyRpcError` 对**除 `-32022` 之外的任何错误码**都判 `legacy`（`-32001/-32020/-32021` 显式列入"不作为代际证据"）。
6. **stdio 分帧**：换行分隔 JSON —— `serializeMessage = JSON.stringify(msg) + "\n"`，`ReadBuffer.readMessage()` 按 `\n` 切；方法名沿用经典集（`initialize`/`tools/list`/`tools/call`）。
7. **initialize 版本口径**：官方服务端 SDK = `SUPPORTED.includes(requested) ? requested : LATEST`（从 Codex 自带 code-review 的 `server.mjs` 源码读到）；本服务对 2023~2025 代际回显、2026+ 一律降级到 `2025-11-25`。
8. **asar 文件区起点 = `8 + 头字段[1]`（= `16 + json_size - 4`）**：早期按 `16 + json_size` 提取会**每个文件少开头 4 字节**（`package.json` 丢 `{\n  `、`function` 变 `tion`）。修正后提取的 `yaml@2.9.1` 可被 node `require` 正常解析。
9. **kb 服务自检 28 项全绿**（`_知识库MCP自检.py`）：含两种握手、14 个工具、写盘 BOM、越界拒绝、非法地址拒绝。
10. **写盘边界**：MCP 只能写知识库目录与 `ai使用库\AI协作\` 内的 `.md`，写前自动备份到 `AI协作\_mcp写备份\`；**没有写 `Ekd5.exe` 的能力**（写 EXE 仍只走 `_dsh写锁.py`）。
11. **Codex 侧连接已实测**：`codex exec -s read-only -C <工作区>` 输出里出现
    `mcp: kb/ledger_read started`，模型的可见工具名是 **`mcp__kb__ledger_read`** ⇒ 服务已被 Codex 成功拉起并注册工具。
    该次调用被 `MCP tool call requires approval, but approval policy is never` 拦下 —— 这是 **Codex 的审批策略**（`-s read-only`），不是服务或路径问题。
12. **DSH 侧同样形态**：安装好的 `mcp-kb` 条目在 `cordis.patch.yml`（YAML 7 条目、`ENTRY` 回读一致），重启后应出现 `mcp__kb__*`（**尚未重启验证**）。

## 实现·使用方法

### 1) Codex 侧（已配置）

```
codex mcp add kb --env PYTHONUTF8=1 --env PYTHONIOENCODING=utf-8 -- ^
  "[本地盘]\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" ^
  "[本地盘]\ccz\曹操传6.6-V7.30 解压密码：66\复刻版6.6山贼\大鲸鱼产生专用\_知识库MCP服务.py"
codex mcp list          # 应看到 kb / Status=enabled
codex mcp get kb        # 查看完整配置
```

- 配置备份：`~/.codex/config.toml.bak_before_kbmcp_20261015`。
- 在该工作区开 Codex 会话时，工具名形如 `mcp__kb__kb_search`。

### 2) DSH 侧（写入完成，**重启后生效**）

```
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_注册DSH_MCP.py            # 检查
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_注册DSH_MCP.py --apply    # 写入（幂等）
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_注册DSH_MCP.py --remove   # 摘除
```

- 落点：`%USERPROFILE%\.dsh\profiles\desktop\cordis.patch.yml` 的 `mcp-kb` 条目（带 `# >>> dsh-kb-mcp` 标记，可精确摘除）。
- 写前自动备份、写后用 **真 js-yaml 解析**校验（从 app.asar 提取的 `yaml@2.9.1` + DSH 自带 node），解析失败自动回滚。

### 3) 日常协作流程（两个 AI 同一套）

1. **开工**：`handoff_read`（交接）+ `ledger_read`（台账末尾）→ `kb_index` 看「按任务查」→ `kb_search`/`kb_read` 取 2~5 页，只看页首「结论速览」。
2. **要机器事实**：`sample_timeline`（当前 SHA + 补丁判定）、`exe_info`、`exe_bytes`（VA 自动映射文件偏移）。
3. **落盘**：`kb_write_page`（新页/追加）+ `kb_changelog_append`（更新记录一行）+ `ledger_append`（台账一行，让另一个 AI 接得上）。
4. **收工**：`handoff_write` 覆盖 `交接.md`，只留现状。

### 4) 工具清单（服务名 `kb`，共 14 个）

| 工具 | 作用 |
|---|---|
| `kb_index` | 分类页数 + README「按任务查」 |
| `kb_search` | 全文检索（空格=与、`-`=排除、可选正则） |
| `kb_read` / `kb_list` / `kb_recent` | 读页（或按关键词定位）/ 列页 / 看最近改动 |
| `kb_write_page` | 写页（overwrite/append，自动备份 + BOM） |
| `kb_changelog_append` | 追加 `00-总览与规范\更新记录.md` |
| `ledger_append` / `ledger_read` | 共享台账追加 / 读取 |
| `handoff_read` / `handoff_write` | 交接文件读 / 覆盖写 |
| `sample_timeline` | 跑 `_样本时间线.py`（当前 SHA + 逐补丁判定） |
| `exe_info` / `exe_bytes` | Ekd5.exe 只读概览 / 字节复读（VA↔文件偏移） |

## 风险与边界

- **重启 DSH 才生效**：本次只写了配置，未重启（重启会中断当前会话）；重启后要确认工具表里出现 `mcp__kb__*`。
- **不要依赖项目级 Codex 配置**：`.codex/config.toml` 仅作留档；实际生效的是用户级 `~/.codex/config.toml`。Codex 升级后重跑 `codex mcp add` 即可。
- **并发写无锁**：两个 AI 同时写同一页会互相覆盖 ⇒ 约定"追加优先、整页覆盖前先 `kb_recent` 看时间戳"，且每次写都有 `_mcp写备份`。
- **会话历史不互通**：DSH 会话在 `~\.dsh\sessions\**\session.v4.jsonl.zstd`（zstd，本机 python 无 zstandard 模块），Codex 会话在 `~\.codex\sessions`。跨 AI 的"上下文"只能靠知识库 + 台账 + 交接，**不要指望互相读会话**。
- **MCP 不是写锁**：任何写 `Ekd5.exe` 的动作仍然必须有 `_dsh写锁.py` 的三重校验；本服务刻意不提供该能力。
- `sample_timeline` 会真的启动子进程跑脚本（默认超时 180 s，MCP 侧调用超时设 300 s）。

## 证据来源

- 工具源码：`大鲸鱼产生专用\_知识库MCP服务.py`、`_知识库MCP自检.py`、`_注册DSH_MCP.py`、`_yaml校验.cjs`。
- 提取物（只读，来自 DSH 的 `app.asar`）：`大鲸鱼产生专用\_asar_mcp\dsh-mcp-client__README.zh.md`、`_vendor_yaml\`。
- 命令输出证据：`codex debug prompt-input`、`codex mcp list` / `mcp get kb`、`_知识库MCP自检.py`（28/28）、`_注册DSH_MCP.py --apply`（YAML 解析 7 条目 + ENTRY 回读）、`大鲸鱼产生专用\_codex_mcp验证.log`。
- 本页不写样本 SHA：SHA 会被并发会话改写，一律以 `sample_timeline` 现读为准。

## 待验证项

- **P1**：重启 DSH 后，工具表里是否真的出现 `mcp__kb__*`（含 `kb_index`）——本次未重启，未验证。
- **P1**：Codex **桌面版**是否与 CLI 同源读 `~/.codex/config.toml` 的 `kb`（配置同源，但未在 GUI 里单测）。
- **P2**：Codex 侧一次**真正执行成功**的工具调用证据。现状：`_codex_mcp验证.log` 已证明"服务能拉起 + 工具能列出"，
  但那次调用被 Codex 审批策略（`-s read-only`）拦下；绕过审批的复测 `_codex_mcp验证2.log` 因**模型侧网络重连失败**没有产出回复
  （与 MCP 无关）。自检脚本 `_知识库MCP自检.py` 已用同一协议覆盖了 `tools/call` 全路径。
- **P2**：两个 AI 并发写同一页的冲突概率与是否需要文件锁。

## ★ 坑（2026-10-15 实测）：`kb_write_page` 的 `path` 是**页名模糊匹配**，同名文件会互相覆盖

- 现象：连续两次 `mcp__kb__kb_write_page`，`path` 分别是
  `06-项目与工具链\可复用Skills\engine-feature-development\SKILL.md` 与
  `…\可复用Skills\x32dbg-debugging\SKILL.md` —— **两次都写进了同一页**，
  第二次把第一次**覆盖**（返回信息里两次都显示 `...\engine-feature-development\SKILL.md`，
  且第二次生成了对同一文件的 `_mcp写备份\..._SKILL.md`）。
- 根因：页面工具按**页名/文件名**（这里是 `SKILL.md`）做模糊定位，不保证区分不同目录下的同名文件。
- **处置/纪律**：写 `SKILL.md` / `README.md` / `index.md` 这类**会重名**的文件时，
  改用文件系统写工具（DSH 的 `write` / `edit`，Codex 的直接文件写）**走精确路径**；
  用 MCP 页面工具只写**全库唯一命名**的页面（如 `逆向方法层-行为契约与五级证据.md`）。
- 复核手法：写完立刻 `Get-ChildItem` 列目录 + 读每个文件首 3 行，确认 `frontmatter name` 与目录名一致。
- 相关：`大鲸鱼产生专用\_知识库MCP服务.py`（若要彻底修，应让 `kb_write_page` 对含分隔符的 `path` 只做精确匹配，
  不回落模糊搜索）。

---

## ★ 2026-10-19 23:30 事故：Codex 侧 `config.toml` 被重置（**登录没丢，配置丢了**）

### 现象与判据

- **登录其实正常**：`~/.codex/auth.json` 仍为 `auth_mode=chatgpt`，`tokens` 四项（id/access/refresh/account_id）**全部非空**，
  `last_refresh = 2026-10-19T15:26:16Z`（本地 23:26，即当时刚刷新过）⇒ **不是登录被清**。
- **被重置的是配置**：`config.toml` 于 **23:29:37** 被重写为 3467 B，丢掉三样：
  1. **`[mcp_servers.kb]`**（共享知识库 MCP —— 掉了 Codex 就读不到台账/知识库工具）；
  2. **`sandbox_mode` / `approval_policy`**（用户 03:15 选的 Full access 被打回默认 `workspace-write`+`on-request`，弹窗会重新阻塞）；
  3. **`.codex` 下所有 `config.toml.bak_*` 备份也被清空**（只剩 config.toml 本体）。
- 识别标志：Codex 的 `AI协作\会话摘要\codex-自动落盘-<日期>.md` **停止增长**（本次停在 20:35）。

### 恢复步骤（实测有效）

1. **先把配置备份到应用清理不到的地方**：`大鲸鱼产生专用\_config备份\config.toml.<时间>`；
2. 在 `config.toml` **顶层**（第一个 `[section]` 之前）确认/补回：
   ```toml
   sandbox_mode = "danger-full-access"
   approval_policy = "never"
   ```
3. 在文件**末尾**追加（python 路径用随包解释器，服务脚本用绝对路径）：
   ```toml
   [mcp_servers.kb]
   command = '[本地盘]\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe'
   args = ['<工作区>\大鲸鱼产生专用\_知识库MCP服务.py']
   ```
4. `tomllib` 解析校验 + `_codex.cmd mcp list` 应能看到 `kb`；
5. **重启 Codex 应用**（配置在启动时读取）→ 再看 `codex-自动落盘-<今天>.md` 是否恢复增长。

> ⚠ 教训：**登录/注销类操作可能连带重写 config.toml 并清掉备份**。每次登录后跑一遍上面第 4 步的两条校验。
2026-10-21 协作规则遗留项收口：新增 大鲸鱼产生专用\\_交接CAS.py，使用 task_id + revision + owner 做条件更新；claim 创建 revision=1，update/release 必须携带 expected_revision 且三项完全匹配，成功后 revision 单调加一，冲突拒绝写入；状态写入 ai使用库\\AI协作\\交接-CAS.json，临时文件配合 os.replace，并用短时互斥锁避免并发覆盖。_codex.cmd 已支持 exec --prompt-file 文件 和 exec --relay --prompt-file 文件，借助 codex exec - 从标准输入读取提示词；文件不存在时在调用前拒绝。m1332 仅核对，未调用记忆写入或更新接口。

## ★ 2026-10-21 代落盘约定（用户裁决：Codex 审批策略保持 never）

- **背景**：Codex `~/.codex/config.toml` 的 `approval_policy = "never"`；其 MCP 工具调用需要审批（`MCP tool call requires approval, but approval policy is never`）⇒ **写类工具（`kb_write_page` / `ledger_append` / `kb_changelog_append`）被拒**，读类可跑。
- **用户裁决（2026-10-21）**：**不改 `approval_policy`**（保持 `never`，避免全文审批弹窗），改走「**DSH 代落盘**」。
- **流程**：
  1. Codex 只负责读 + 分析 + 出结论；每轮结论由 `_codex_notify.py` 自动写入 `ai使用库\AI协作\会话摘要\codex-自动落盘-<日期>.md`。
  2. DSH 开工/收工时用 `digest_read` 或直接读该摘要，识别「本轮未落盘结论」。
  3. DSH 用同一套 `mcp__kb__*` 工具补写：结论 → 对应知识库页（append）、`kb_changelog_append`、`ledger_append`；在追加段注明「Codex 静态分析，DSH 代落」与目标 SHA。
  4. Codex 恢复写能力后（若将来改审批策略），再切回自写自落。
- **禁止**：DSH 代落时不得改 Codex 摘要原文（它是只读的自动落盘文件）；只写知识库/更新记录/台账。
- **当前积压**：`0x45D513` 更正、`0x40 狂妄` 共享层（已代落，见 `第3批.md`/`第1批.md`）；`0xE8/E9`（已代落）；下一轮若再有新结论按同法处理。

## ★ 2026-10-21 追补：Codex 待落盘「实时检测」机制（用户要求「做好检测、实时同步落盘」）

- **入口**：`python 大鲸鱼产生专用\_codex健康.py --pending`
  - 扫描 `AI协作\会话摘要\codex-自动落盘-<今天>.md` 的**最近 3 轮**，按 `Transport closed / 尚未完成合规落盘 / 待服务恢复后补写 / 没有合规写入 / 未落盘 / 无法写入 / 没有绕过 MCP` 标记分组。
  - 结果写入 `AI协作\会话摘要\_代落盘队列.md`（列出轮次标题、行号、命中句）；`_代落盘已完成.json` 里的轮次会被跳过（DSH 补完后把轮次标题写进去）。
  - 退出码：0 = 无待落盘；1 = 有（队列非空）。
- **触发**：`_codex_notify.py`（Codex 每轮结束的 notify 钩子）末尾会顺带跑一次 `--pending`（`subprocess.run(..., timeout=15)`，失败不影响摘要落盘）⇒ **Codex 每出一轮，队列自动刷新**，不需计划任务（计划任务 `CCZ-Codex-Pending` 创建被 ACL 拒绝，已放弃）。
- **DSH 侧约定**：开工/收工先看 `_代落盘队列.md`；队列非空时按轮补写知识库 + 更新记录 + 台账，补完把轮次标题追加到 `_代落盘已完成.json`。
- **验证**（2026-10-21 21:13）：`--pending` 返回「无待落盘（最近 3 轮无未落盘标记）」、exit 0；模拟 `_codex_notify.py` 后队列 mtime 刷新到 21:13:59。
- **边界**：脚本只能**检测+排队**，不能自动判断"该写哪个页/哪段"——真正落盘仍需 DSH（或人）按队列处理。


## ★★ 2026-10-21 22:16 实测：共享台账时间戳**已比真实时钟超前约 70 分钟**（多会话漂移）

- **实测**：本机系统时间 `2026-10-21 22:15:36`（China Standard Time），而台账末尾三条是 `23:07 / 23:08 / 23:20 / 23:26`。
- **后果**：`ledger_append` 默认用**系统时间**，于是任何正常追加都会被判「**时间倒退**」而拒绝（本人今晚被拒 2 次；Trae 也被拒 1 次，被迫显式传 23:08）。
- **滚雪球机制**：A 写了未来时间 → B 为了通过单调校验只能写更晚 → 漂移越来越大。**禁止用"往前编时间"当常规解法**，它只会让账本继续跑飞。
- **真实时间与台账的换算（今晚）**：台账时间 ≈ 真实时间 **+70 分钟** 左右。
- **临时口径（照这个做）**：
  1. 追加前先 `Get-Date` 看**真实时间**；
  2. 若真实时间 ≤ 台账末条，**在 `what` 里显式标注 `（真实时间 HH:MM，台账已漂移）`**，并把 `time` 传到"末条 +2 分钟"即可通过校验；
  3. 不要回头改历史行、不要删除行。
- **根治**：检查 Codex 侧（及其它写库端）的**系统时钟/时区**是否偏了整整 1 小时（本机是 CST，无夏令时）；对齐后新行会自然回落到真实时间，届时应在新一轮**明确记录"时钟已校正"**，避免后人以为又倒退。
- 相关：`_mcp写备份\` 的文件名用的是**真实时间**（如 `20261021_215845`），可当作对表基准。

## ★ 2026-10-24 第三个客户端：Qoder Desktop 注册 kb MCP（实测通过）

**现象与判据（前）**：Qoder Desktop 会话内 `mcp_list({keyword:"kb"})` → `{"tools":[],"total":0}`；`manage_app_mcp list_servers` 只有 4 个 `sourceKind=plugin` 服务，`get_config(user)` 条目数 = 0
⇒ **注册块缺失，不是服务脚本坏**（与本页 2026-10-19「Codex `config.toml` 被重置」同型故障）。

**写入前校验**：`PYTHONUTF8=1 python 大鲸鱼产生专用\_知识库MCP自检.py` → **通过 30 项 / 失败 0 项**（用系统 Python 3.14.8 跑，非 DSH 运行时）。

**注册配置**（Qoder **user 级**自定义连接器，`transport=stdio`，入口 = `qoder-settings` 的 `manage_app_mcp add`）：

```json
{ "command": "[本地盘]\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python314\\python.exe",
  "args":  ["[本地盘]\\ccz\\曹操传6.6-V7.30 解压密码：66\\复刻版6.6山贼\\大鲸鱼产生专用\\_知识库MCP服务.py"],
  "env":   {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"} }
```

- **解释器故意与 Codex/TRAE 不同**：那两侧用 `~\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`（3.12.14）；它属于 DSH 客户端，**DSH 卸载/升级就断**。Qoder 侧改用独立的系统 Python，已实测 30/30 能起。
- 三个客户端读写的都是**同一份磁盘服务与同一个 `CACHE`**，没有第二份知识副本。

**生效判据（后）**：`get_server` → `status="ready"`、`sourceKind="custom"`、`sourceEntryKey="kb"`；`list_tools` → **total 23**。
⚠ 本页上节「工具清单（服务名 `kb`，共 14 个）」**已过时**：现为 **23 个** = `kb_*` 7（`index/search/read/list/recent/write_page/changelog_append`）+ `ledger_*` 2 + `handoff_*` 2 + `sample_timeline`/`exe_info`/`exe_bytes` 3 + `memory_*` 7（`remember/recall/recent/bootstrap/forget/update/stats`）+ `digest_*` 2。
⚠ **会话内可见性**：Qoder 只在**新会话/重启**后才把 `mcp__kb__*` 挂进会话工具表；同一会话内 `mcp_list` 可能仍为空 —— **判据看 `manage_app_mcp list_tools` 的 total，别看会话工具表**。

### 入口选择修订（对齐 AGENTS.md §0.0d「先走 mcp__kb__kb_search」）

- 当前客户端**有** `mcp__kb__` → 用它（实测 0.19~0.35 s）；**没有**（未重启的会话、或别的客户端）→ 直接 `python 大鲸鱼产生专用\_知识检索.py "<词>"`（实测 1.2~1.9 s）。
- **两者不等价**（2026-10-24 实测）：`kb_search`（`_知识库MCP服务.py:396 t_kb_search`）**不含** `_知识检索.py` 的三项能力 —— 中文复合词分词 `zh_split`、同义词表 `SYNONYMS`、进制等价 `expand_num`。整串 vs 分词的**召回差**：

| 查询 | `kb_search`（整串） | `_知识检索.py`（分词后文档级） |
|---|---|---|
| `特技优化` | 4 页 | **25 页** |
| `转移策略伤害` | 11 页 | 11 页（同） |
| `中毒物理易伤` | 22 页 | 22 页（同） |
| `剧本性能画像` | **0 页** | **8 页** |
| `伤害预览不同步` | **0 页** | **15 页** |

⇒ 口径：**多字中文词组用 CLI**（否则会拿到「全库无此词」的假阴性）；**地址/码值/函数名用 MCP**（更快，且这些不需要分词）。

### 2026-10-24 修订：Qoder kb 重载与固定探针

上节 219～229 行『kb_search 不含中文分词／多字中文词组用 CLI』是 P0-3 修改前的旧口径，自此作废；现服务已复用 `zh_split`、同义词与进制扩展。修改 `_知识库MCP服务.py` 后，Qoder 用 `manage_app_mcp retry` 重载 serverId `62878af7-1b0c-4cdb-bd4d-24699ecdfcee`，再确认 `status=ready`；仅看到工具可调用不足以证明新版已加载。

固定探针已加入 `_知识库MCP自检.py` 的只读检索段：`剧本性能画像` 必须出现 `中文自动分词`＋`剧本 + 性能画像`，且专题页 `08-剧本与战场/剧本特技性能画像与三条落地路线.md` 进入前 6 条；`伤害预览不同步` 必须出现 `伤害预览 + 不同步`。

判据：Qoder 重载前，两个实时 MCP 查询分别只有 3 页／2 页、均无分词标记，专题页缺失；重载后分别为 5 页／5 页，分词标记均出现，专题页命中，自检 33/33、服务 `ready`。
#### 2026-10-24 修订：`kb_index` 小节按标题层级截取

`t_kb_index` 旧逻辑遇到任意 `#`/`###` 标题都重算开关，导致 `section=按任务查` 在 `### 1.1` 即停止，只回目标标题。现记录目标标题层级：下级标题与正文保留，同级或更高级标题才结束；无匹配时仍回退完整 README，原有语义不变。

判据：修复前实时 MCP 只回 `## 1. 按任务查`；修复并重载后返回 1.1～1.9 的下级标题与表格，且不包含下一个 `## 2` 章节。`_知识库MCP自检.py` 新增“保留下级标题与表格／止于下一同级标题”两项回归，自检 35/35。
## 2026-10-24 交接 CAS v1：每任务结构化真相源

- 状态源由单文件 `AI协作\交接-CAS.json` 改为 `AI协作\交接-CAS\<task_id>.json`；旧文件仅作历史快照，不再读写。
- 固定字段：`schema_version=1`、`task_id/revision/owner/status/goal/scope{target,base_sha256}/state{summary,next_action,blockers}/evidence[{kind,ref}]/created_at/updated_at`。
- `status` 仅 `active/blocked/done/cancelled`；`release` 清空 owner，默认回 `active`，完成/取消需显式 `--status`。
- 每任务独立锁与临时文件 + `os.replace`；更新/释放必须匹配 `task_id+owner+expected_revision`，成功后 revision 加一。
- `read` 无参数返回 `{schema_version,tasks}`；`_开场.py` 已改为汇总 active/blocked 任务，无活动任务时显示最近 3 个。
- 判据：隔离 CLI 回归覆盖 claim/update/release、过期 revision、错误 owner、终态拒绝、并行任务、空数组清空、开场读取；两个并发 claim/update 均只有一个成功。
- 命令口径见 `ai使用库\AI协作\README.md`「交接 CAS 锁」节。
### 2026-10-24 追加：CAS 只读渲染、体检与过龄提示

- `_交接CAS.py render`：只向 stdout 输出交接 Markdown，列出 active/blocked；无活动任务时列最近 3 个终态任务。**不写** `交接.md` / `交接-当前.md`，避免未经确认覆盖人读页或破坏硬链接。
- `_交接CAS.py check`：只读校验 schema/字段类型、孤立 `.lock` 与 `.tmp`、活动任务过龄、`scope.target` 的当前 SHA 与 `base_sha256` 差异；错误退出 1，仅警告退出 0。基线不同只告警，因为任务推进后本就应变化。
- `_开场.py`：active/blocked 超过 24 小时未更新时显示「可能失联，未自动释放」，只提示、不抢 owner。
- 判据：隔离测试覆盖无目录/正常/基线漂移/孤儿锁与临时文件/25 小时过龄/损坏 JSON/并发 claim；render 前后任务目录文件列表不变；真实目录 render 与 check 均通过，源码归档 SHA 一致。
- 旧版快照已由用户确认并原样归档为 `ai使用库\AI协作\交接-历史\交接-CAS-20261021-archive-close.json`（原 `交接-CAS.json`，269 B，SHA256 `2DDCD97E…D482DC8A` 保持不变）；归档后旧路径不存在，不迁移字段、不参与任何读写。

### 2026-10-24 追加：交接硬链接修复、收工门禁、会话串联

- `_交接CAS.py fix-link`：默认取 `交接-当前.md`/`交接.md` 中 mtime 较新的一份为真相，两份先备份到
  `AI协作\_mcp写备份\交接链接修复_<时间>\`，再删除别名并 `os.link` 重建；完成后校验 `samefile` 与 `nlink≥2`。
- `_自检.py` Q 项：硬链接、CAS JSON（schema/字段/文件名=task_id/状态/过龄）、旧单文件复活、CAS 与交接页同步；
  `--strict` 下任何 `✗` 返回 1。断链提示直接给出 `fix-link` 命令。
- `_收工门禁.py`：`release --status done` 的前置闸门（summary/blockers/evidence/交接页与台账 mtime/严格自检）；
  失败拒绝写盘，`--skip-checks` 仅在用户明确要求时使用。
- 留痕 `session`：`_开工门禁 --full` 新建会话，`_开场` / `_查库门禁` / `_落盘结论` 共用；
  `_查库门禁.py --status --session [ID]` 查看该会话的开场→查库→落盘链条。
- 判据：`_测门禁闸门.py` 50/50 通过；真实自检 28 项 0 `✗`；`fix-link` 后 `nlink=2`、`samefile=True`。
## ★ 2026-10-25 Codex「MCP 地址经常断开」根因与修复

**现象**：Codex 会话反复报 `tool call failed for kb/...` / `Caused by: Transport closed`；新增的 `_自检.py` S2 实测最近 60 分钟 4 次（09:42）。

**根因（Codex 侧生命周期，不是服务崩溃/配置丢失）**：
- `~/.codex/logs_2.sqlite` 的 `codex_core::mcp_tool_call` WARN 全部是 `Transport closed`，且都发生在 `code_mode.broker.invoke_tool` 内（`aborted=false`）。
- 紧邻的 `rmcp::service` 日志：`server_name=kb ... serve finished quit_reason=Cancelled` / `task cancelled`，随后立刻重新 `Service initialized`。
- 同一时刻 `tool_catalog` 仍报 `available_server_count=6 unavailable_server_count=0 tool_count=315` ⇒ 服务可用。
- `_知识库MCP自检.py` 全绿；服务日志无崩溃栈，只有正常 `call ... ok` 与校验类 `ValueError`。
⇒ **Codex 每轮/每 cell 取消 kb stdio 服务后，code-mode 仍在途的调用撞上已关闭的传输**；多线程/多会话并存时更明显（实测 6 个 kb 实例）。

**修复（已落地）**：
1. `~/.codex/config.toml` 的 `[mcp_servers.kb]` 增加 `startup_timeout_sec = 120`、`tool_timeout_sec = 300`；改前备份 `大鲸鱼产生专用\_config备份\config.toml.20261025_094207`；`codex mcp list` 校验仍识别 `kb`。
2. **必须重启 Codex 应用**才生效（配置在启动时读取）。
3. 持续关注：`_自检.py` 新增 **S2**（读 `logs_2.sqlite` 最近 60 分钟 `Transport closed` 计数，只读），随既有计划任务 `CCZ-SelfCheck`（下次 10:03）写入 `_自检提醒.md`；**S** 仍是服务侧 `--quick` 健康。

**残留/下一步**：若重启后仍频繁出现，改用 Codex 支持的 **streamable HTTP**（`codex mcp add --url`）让所有线程共享一个常驻服务；当前 `_知识库MCP服务.py` 仅 stdio，需另做 HTTP 包装（未实现）。
### ★ 2026-10-25 追加：改用 streamable HTTP（已实施）

- 新工具 `大鲸鱼产生专用\_知识库MCP_HTTP包装.py`：**唯一常驻子进程** `_知识库MCP服务.py` + HTTP 端点 `127.0.0.1:8765/mcp`；JSON-RPC id 全局重写、多客户端解复用、initialize 回 `Mcp-Session-Id`、子进程死亡自动重启。
- 实测：`--self-test` 通过（protocol=2025-06-18、tools=23、kb_search ok）；**两会话并发各 5 次（同 id 1..5）0 错误**；Codex 实连日志 `POST /mcp 200/202`、`initialize from codex-mcp-client`（同一子进程 `sessions=15`）；`codex mcp get kb` → `transport: streamable_http`。
- 配置：`~/.codex/config.toml` 与 **项目级 `.codex/config.toml`** 均改为 `[mcp_servers.kb] url="htt[本地盘]//127.0.0.1:8765/mcp"` + `startup_timeout_sec=120` / `tool_timeout_sec=300`；备份 `_config备份\config.toml.20261025_095440`、`project-config.toml.20261025_095617`。
- ⚠ **修正本页 :22 的旧结论**：0.162 项目级配置不生效；**26.1013 实测会合并**——项目级仍写 stdio `kb` 时，与全局 `url` 合并会报 `url is not supported for stdio`。**两处必须同时改**。
- 常驻/自愈：启动文件夹 `CCZ-MCP-HTTP.vbs`（pythonw 隐藏启动）；`_自检.py` 新增 **S3**（`/health` 探测，掉线用 WMI 拉起）与 **S2**（Codex 侧 `Transport closed` 计数），随 `CCZ-SelfCheck` 每 30 分钟跑。
- 残留：Codex 应用可能仍持有旧 stdio 连接，**重启 Codex 后所有线程才统一走 HTTP**；`GET /mcp` 回 405（不发服务端推送，规范允许），Codex 实测接受。
### ★ 2026-10-25 追加：Codex 报 `os error 10061` 的真实根因与三层自愈（已闭环）

- **症状**：Codex **桌面版**弹 `codexstream disconnected before completion: 由于目标计算机积极拒绝，无法连接。(os error 10061)`，同一时刻 kb 工具全部不可用。
- **根因（实测，不是网络/代理/DNS）**：`127.0.0.1:8765` 无进程监听。`~/.codex/config.toml` 的 `[mcp_servers.kb] url="htt[本地盘]//127.0.0.1:8765/mcp"` 是 HTTP 端点，包装进程一死，Codex 建链即被拒 ⇒ 会话流中断。旁证：`_知识库MCP_HTTP_child.log` 最后一次 `initialize from codex-mcp-client` 停在 18:02:33，之后到 18:55 无任何请求；系统代理 `ProxyEnable=0`（xray 1088 活着），排除代理与 DNS 污染。
- **第一层失效点（真正让"自启"从来没生效的）**：自启动 `CCZ-MCP-HTTP.vbs` 当时是 **UTF-8 无 BOM**，`wscript` 按 ANSI(GBK) 解码 ⇒ 中文路径乱码 ⇒ `sh.Run` 指向不存在的文件、静默失败。**修法**：改存 **UTF-16LE + BOM**（VBS 里出现非 ASCII 路径必须如此，否则 wscript 读不了）。
- **第二层（有效但慢）**：`CCZ-SelfCheck`（每 30 分钟）→ `_自检.py` S3 的 WMI 兜底是**有效**的：实测父进程 `WmiPrvSE` 拉起 pythonw，19:02:57 自愈成功，`_自检提醒.md` 写 `[✓] S3 kb HTTP 掉线后已自愈`。但它最慢要等 30 分钟，且 18:53 那次任务本身返回 `0x800710E0`、没跑到 S3。
- **第三层（本次新增）**：计划任务 `CCZ-MCP-KeepAlive`，每 2 分钟跑一次同一个自启动 VBS。`serve()` **先 bind 探测再起子进程**，所以已有实例时新实例只写 `port 8765 busy -> exit (已有实例)` 后退出，不会产生孤儿 child，也不会抢端口。
- **判据（实测对照）**：已有实例时触发任务 ⇒ 日志 `port 8765 busy -> exit`、服务不受影响；杀掉 wrapper(5632)+child(33696) ⇒ 8765 监听数=0；再触发任务 ⇒ 8 秒内 `listen htt[本地盘]//127.0.0.1:8765/mcp (child pid=8496)`、`/health={"status":"ok","child_alive":true}`、任务 `Last Result=0`。
- **人工恢复三步**：① 探活 `python 大鲸鱼产生专用\_知识库MCP_HTTP包装.py --check`；② 拉起 `schtasks /run /tn CCZ-MCP-KeepAlive`（或跑 `python 大鲸鱼产生专用\_自检.py`）；③ **重启 Codex 应用**（MCP 连接在应用启动时建立，不重启会沿用旧的失败状态）。
- ⚠ **新建计划任务需要提权**：未提权执行 `schtasks /create` 直接 `ERROR: Access is denied.`；本次用 `Start-Process schtasks -Verb RunAs` 完成注册（任务 XML 见本次会话，UTF-16 写入 `%TEMP%\ccz_keepalive.xml`）。
- ⚠ **未闭环**：18:53 那次 `CCZ-SelfCheck` 的 `0x800710E0` 在 TaskScheduler/Operational 里查不到事件，原因未定；现由 2 分钟看门狗覆盖，不再依赖它兜底。
### ★ 2026-10-25 20:27 台账「未来时间戳」的量化补证（库内既有口径见下，**不是新发现**）

- **库内既有口径**（先查库才看到）：`03-机制详解/特技族逐族反汇编-第4批.md:2024`「共享台账仍有未来时间戳，**未伪造倒退时间**」、同页 `:2070`「继续不伪造倒退时间」⇒ 处置原则早已定案 = **宁可台账行不写，也不填假时间**。本轮台账行**遵此不补**，成果只落知识页 + 交接页。
- **本轮新增的只是量化证据**（排除"时区/时钟口径差"这一种误判方向）：
  - 本机 `date` = `2026-10-25 20:26 (UTC+08:00)`；
  - `ledger_append` 在 19:56 被拒，报「早于台账最后一条 2026-10-26 01:21」；
  - 30 分钟后复取：台账**真实 mtime = 2026-10-25 20:21**，而末条**声明时间已到 2026-10-26 05:34**；
  - ⇒ 真实时间走 30 分钟、声明时间走约 4 小时（≈8 倍速）。时区/时钟差只会是**固定整点偏移**，不会出现倍速 ⇒ 判定为**逐行自拟递增**，与库内「未来时间戳」说法一致，并把它从"疑似"升级为"已量化"。
- **使用影响（开工先读台账末尾 20 行时的注意事项）**：台账的**时间轴不可用于跨 AI 排序**，要看先后请用 `git log` / 文件 mtime / `_落盘留痕.jsonl`，不要信台账前缀时间。
- **候选修法（未实施，需用户拍板）**：① `ledger_append` 增加「声明时间 > 系统时间 + 容差 ⇒ 拒绝」的闸门，把透支挡在写入前；② 时间由服务端强制 `datetime.now()`，不接受调用方传入；③ 在「给Codex的常驻指令」里禁止自拟时间。
- ⚠ **顺带记一条工具坑（新）**：`_落盘结论.py --text` 传含反引号的正文会被 Git Bash 当命令替换执行（实测报 `ledger_append: command not found` 并吃掉正文），**含反引号/长正文一律走 `--text-file`**。
- 证据类型 = 命令现读（`date` / `stat` / `grep -oE` / `_查库门禁.py` 留痕 20:27:32）；**未改任何工具、未写台账、未动 EXE/Data.e5/剧本/存档**。
### ★ 2026-10-25 20:36 修复：`ledger_append` 时间闸门（本页 `:184` 记录的「真实时间被自己拒死」已闭环）

**症状（本页 `:181/:184` 早已登记）**：台账一旦被自拟的未来时间戳透支，`ledger_append` 默认用系统时间，
任何正常追加都被判「时间倒退」而拒绝 ⇒ 表现是"工具把自己的正确用法锁死了"。

**改了什么（`大鲸鱼产生专用\_知识库MCP服务.py` 的 `t_ledger_append`，三处）**：

1. **新增未来时间闸门**：声明时间 > 系统时间 + `LEDGER_FUTURE_TOL_MIN = 5` 分钟 ⇒ **直接拒绝**，
   报错里带"超前多少分钟"和"去掉 time 参数即可用系统时间"。自拟未来时间戳从此在这个入口**写不进去**。
2. **单调锚点钳到系统时间**：旧判据 `本条 < 台账末条` 改成 `本条 < min(台账末条, 系统分钟)`。
   透支台账不再把真实时间的行永久拒死 ⇒ **宁可留警告，也不拒人**。
3. **比较口径统一抹到分钟**（`now_min = now.replace(second=0, microsecond=0)`）：
   ⚠ 这是本次修复自己踩出来的坑 —— 默认时间戳只到分钟（秒=00），而 `now` 带秒，
   第一版写成 `min(b, now)` 后 `20:31:00 < 20:31:45` **恒成立**，真实时间行仍被拒；
   **凡与分钟精度时间戳比较，系统时间必须先 `replace(second=0)`**。
   同时报错文案不再把台账末条谎称成"有效锚点"，改打印真正参与比较的那个时刻。
4. **透支时改为出声提醒**（不再拒写）：追加成功但返回体带
   `⚠ 台账末条声明时间 … 已在未来（透支 N 分钟）⇒ 有会话自拟过时间戳；本行按真实时间追加，
   跨 AI 排序请改用文件 mtime / _落盘留痕.jsonl，不要信台账时间。`

**判据与实测（临时台账，末条伪造为未来时间 `2026-10-26 05:34`；六例全对）**：

| 例 | 输入 | 期望 | 实测 |
|---|---|---|---|
| C1 | 真实系统时间 | 通过 + 透支警告 | 通过，警告"透支 540 分钟" ✓ |
| C2 | `2027-01-01 00:00` | 拒 | 「超前 96686 分钟（容差 5）」✓ |
| C3 | 系统 +3 分钟 | 通过（容差内） | 通过 ✓ |
| C4 | 系统 −2 小时 | 拒 | 「早于台账有效锚点 20:34」✓ |
| C5 | 不传 `time` | 通过 | 通过 + 透支警告 ✓ |
| C6 | `2026-10-25 25:99` | 拒 | 「time 格式非法」✓ |

**回归凭据**：`_知识库MCP自检.py --write-test` **43 项全过、0 失败**；
新增两项常驻检查（`台账未来时间被拒` / `台账时间倒退被拒`，两条都是纯拒绝、不写盘，故 `--quick` 也跑）；
自检里的 `ledger_append`（系统时间）在真实台账已被 Codex 透支到 `2026-10-26 05:34` 的情况下**成功落行**，
即修复在真实台账上成立，不只是临时台账。

**边界（必须知道，别以为闸门万能）**：
- 闸门只装在 **`ledger_append` 这个入口**；直接编辑 `共享台账.md` 的会话不受约束 ⇒
  Codex 侧 10-25 晚仍在写未来时间戳（`04:58 / 05:16 / 05:34`），**台账时间轴依旧不可用于跨 AI 排序**。
- 排序请用：文件 mtime、`_落盘留痕.jsonl`、`_改动总账.md`、或 `git log`。
- ⚠ 改完 `.py` 后**已在跑的 kb MCP 进程不一定会重载**：本次实测在会话续接后新进程已用上新代码
  （20:35 真实时间行被接受即为凭据）；若你的会话里仍报「时间倒退」，先重启 kb MCP 再判断。

## ★ 2026-11-03 事故：启动脚本丢失 ⇒ 每 2 分钟弹「Windows Script Host 无法找到脚本文件」

**现象**：桌面反复弹窗
`无法找到脚本文件 "[本地盘]\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\CCZ-MCP-HTTP.vbs"`（约每 2 分钟一次）。

**根因（两层，实测）**：
1. 启动脚本 `CCZ-MCP-HTTP.vbs` **已从 Startup 文件夹消失**（服务本体与包装脚本仍在：`大鲸鱼产生专用\_知识库MCP_HTTP包装.py`，
   8765 当时仍 `status=ok / child_alive=true`）⇒ 不是服务坏了，只是"自启+看门狗"的入口文件没了。
2. 计划任务 **`CCZ-MCP-KeepAlive`（每 2 分钟）** 的 `Task To Run` 仍写死指向该 Startup 路径
   ⇒ 每次触发 `wscript.exe` 打开一个不存在的文件 ⇒ WSH 报错弹窗（**任务 `Last Result` 仍可能为 0，别只看返回值**）。

**判据对照（前 → 后）**：
- 前：Startup 目录仅 3 个 `.lnk` + `desktop.ini`，无 `CCZ-MCP-HTTP.vbs`；`schtasks /query /tn CCZ-MCP-KeepAlive /v` 的 `Task To Run` 指向该缺失路径。
- 后：重建 `CCZ-MCP-HTTP.vbs`（**UTF-16LE + BOM**，618 B，前 2 字节 `FF FE`）⇒ `cscript //nologo` 退出码 0、无弹窗；
  `schtasks /run /tn CCZ-MCP-KeepAlive` → `Last Result=0`、`Status=Ready`；`htt[本地盘]//127.0.0.1:8765/health` 仍 `ok`、8765 监听数 = 1（**没有起出第二个实例**）。

**重建内容（照抄）**：
```vbs
Option Explicit
Dim sh, py, script
Set sh = CreateObject("WScript.Shell")
py = "[本地盘]\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\pythonw.exe"
script = "[本地盘]\ccz\曹操传6.6-V7.30 解压密码：66\复刻版6.6山贼\大鲸鱼产生专用\_知识库MCP_HTTP包装.py"
sh.Run """" & py & """ """ & script & """ --serve", 0, False
```
- ⚠ **必须存成 UTF-16LE + BOM**（本页 :300 的既有坑：UTF-8 无 BOM 时 wscript 按 ANSI 解码中文路径 ⇒ 静默失败）。
- 写盘命令口径：`[System.IO.File]::WriteAllText($dst,$vbs,[System.Text.Encoding]::Unicode)`。

**诊断顺序（下次同类弹窗照此走，别先删任务）**：
① 看弹窗里的**脚本路径** → ② `Get-ChildItem Startup` 看文件是否在 → ③ `schtasks /query /tn CCZ-xxx /v` 看 `Task To Run` 是否指向该路径 →
④ `Invoke-WebRequest htt[本地盘]//127.0.0.1:8765/health` 判断服务本体是否还活着 → ⑤ 当场重建入口文件并用 `cscript` 静默验证（**不要用 `wscript` 验证，失败会再弹一次**）→ ⑥ 手动 `/run` 任务复核 `Last Result` 与监听数。
- **禁止**：脚本丢了就直接删 `CCZ-MCP-KeepAlive`——那会同时失去"掉线 2 分钟内自愈"的能力（本页 :296 那节的第三层兜底）。


## 2026-11-06 tool_docstring首部匹配修复与当前入口验收

对应待验16532“开工检索失败/长时间无输出”的检索子缺陷，已仅修`_知识检索.py:tool_docstring`：模块首部锚定、逐行注释、r/u前缀和配对三引号，移除DOTALL下`#.*`跨行嵌套回溯；源码SHA `E0368ECC372525B13D2FD655EAB89B07DBE09C52029C97C669C6E3D4319B755E`。签名/UTF-8-sig/errors=replace/extra_lines与正文去重保留。11常规夹具逐字相同、6真实工具的后续文本误摘单列纠正、3首部断言/增长夹具/py_compile通过；不为保留旧错误摘取而回退。

本次直接调用现有CLI，每条45秒上限：`B10手动准入`退出0、5.990秒，KB3/docstring0/合计9；`43F6DB`退出0、3.232秒，KB35/docstring4/合计54。前者没有直接docstring命中，后者实际召回`_追属性取值链.py`、`_阵亡收集链探针.py`、`_生成逐鹿HP上限破坏.py`、`_战斗链地形图.py`。这是当次检索快照，不承诺所有措辞召回。日志：`大鲸鱼产生专用/战斗内核双收敛/检索修复定向验收-20261106/`。默认查询自动完成一次增量缓存更新，未显式重建索引。

root另提供有界55秒的`--full`复验：PID35688、退出0、10.531秒、bounded_stop=false，日志到达步8与“门禁跑完”。仍有18条旧补丁期望不符、旧缓存提示、x32状态stopped及格式门命中232处；不等于检查全绿，也不证明旧13分钟挂起唯一根因。旧verify tuple打印异常未在本次路径复现，仍待单独修；capture与失败重试未改。证据：`开工门禁-docstring修复后有界复验-20261106.log/json`及`知识检索docstring首部匹配修复-20261106.md/json`（同B项目）。本项不修改B9/B10冻结源或来源政策。
