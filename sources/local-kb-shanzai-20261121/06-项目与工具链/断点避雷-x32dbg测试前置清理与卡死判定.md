# 断点避雷 —— x32dbg 测试前置清理与"卡死"判定（复刻版6.6山贼）

## 结论速览

- **一 attach 就"点不动"的头号原因不是你的断点**：x64dbg 会**自动给每个已加载模块挂 TLS 回调断点**。
  本机搜狗输入法一串模块（`sogoutsf.ime`/`sogoupy.ime`/`picface.dll`/`ichat_bundle.dll`…）
  实测一次 attach 就有 **12 个**这种断点，游戏因此频繁暂停、`Responding=False`，鼠标点击全部失效。
  ⇒ **attach 后第一条命令永远是 `breakpoint_delete_all`，再设自己的断点**；并**先杀掉搜狗进程**。
- **`debug_run` 连按十几次都停在同一 eip，且那个地址没有断点** ⇒ 十有八九是
  **EFLAGS 里的 TF（单步陷阱，bit8=0x100）没清**，不是断点、也不是游戏卡死。
  判据：`debug_step_into` 能往前走一步。处置：`register_set eflags=0x00000202` 后 `debug_run` 即 running。
- **条件断点的 `hit_count` 无条件自增** ⇒ 它只证明"执行到该地址 N 次"，**不证明条件成立、也不证明暂停过**。
  要证明"我的条件写得对"，必须做**对照实验**（把条件换成另一个已知一定会发生的值，看它能不能暂停）。
- **不要用 `byte:[0x501BF9]==5` 当"策略"条件**：实测策略/物理命中当下读到 `0x501BF9 = 0xFF`
  （分发器最后一次写入的残值），永不等于 5。**策略判别直接判上下文指针 `[ebp-4]`**
  （`0x497AF8` = 策略 / `0x4927F0` = 物理）。
- **`memory_read` 不能用来判断"这里有没有断点"**：软断点处 x64dbg 回显的是**原始字节**。
  判断用 `breakpoint_get` / `breakpoint_list`。

## 适用版本

- 样本 `Ekd5.exe` SHA256 `4A761A94A72D80D17A260E9BCBA0E0A4F2F6C8469CCE0C2F19BDEF2D0A0427CF`（干净样本）。
- x32dbg：`[本地盘]\新建文件夹\snapshot_2026-05-27_12-11\release\x32\x32dbg.exe`，MCP 桥端口 3000。
- 客户端：`大鲸鱼产生专用\_x32dbg.py`（`tools` / `schema` / `call` / `run` / `state`）。

## 已确认事实

### 1. x64dbg 自动 TLS 回调断点（搜狗模块）

attach 后 `breakpoint_list` 实测返回 **12 个**断点，其中 1 个是自己的，其余全是
`TLS 回调断点 N (<模块>)`：`sogoupy.ime`×3、`systembeautify_bundle.dll`、`picface.dll`、
`isgpet_bundle.dll`、`ichat_bundle.dll`、`sogoupy…`。

- **症状**：游戏 `state=paused`、`eip = sogoutsf.ime+0xACC90`（实测）、`Ekd5.Responding=False`、
  点击"是"后确认框**不消失**。
- **对照**：`breakpoint_delete_all`（deleted_count=12）→ 重设自己的断点 → 再点"是"，
  **确认框 0.0 秒消失**。⇒ 因果闭环。
- **加重因素**：搜狗后台进程（`SGTool`×2、`SogouCloud`）在跑时更容易触发；用户口径
  「每次都是搜狗模块，测试时候杀掉他」⇒ **测试前直接杀**（`sogoutsf.ime` 已注入 Ekd5 的
  部分杀不掉，只能靠删 TLS 断点）。

### 2. TF（单步陷阱）残留导致假"卡死"

- **现象**：`debug_run` 连续 12 次全部返回
  `{"eip":"0x0043F27F","state":"paused","stop_reason":"breakpoint_or_exception"}`，eip 一次都不动。
- **排除**：`breakpoint_get 0x43F27F` → `No breakpoint at address`；`breakpoint_list` 只剩自己那 1 个；
  `memory_read 0x43F27F` = `E9 48 CB FF FF`（原生 `jmp 0x43BDCC`，没有 `CC`）。
- **定案**：`register_list` 读到 `eflags = 0x00200344` ⇒ **bit8(0x100) TF 置位**。
  `debug_step_into` 能走一步（eip 0x43F27F → 0x43BDCC）⇒ 进程可动，是调试器在单步死循环。
- **处置**：`register_set {"name":"eflags","value":"0x00000202"}` → `debug_run` 立刻
  `{"state":"running"}`，eip 转到 `0x77A74C6C`（ntdll 空闲）。**游戏全程存活**。
- **判据口诀**：**eip 逐次相同 + 该地址无断点 + memory 无 CC + step 能动 ⇒ 先查 TF**。

### 3. 条件断点的两件事必须分开证明

| 要证明 | 手段 | 不能证明 |
|---|---|---|
| 地址**执行过** | `hit_count` 增长 | 条件成立、暂停过 |
| 条件**表达式正确** | **对照实验**：换个已知必中的值，看能不能暂停 | — |
| 命中时的**实值** | 暂停后 `eval_expression` / `register_get` / `memory_read` | — |

本轮对照实验（2026-10-18）：
- 断点 `0x4064D5`，条件 `dword:[ebp-4]==0x4927F0`（物理上下文）⇒ **命中并暂停**，
  暂停时 `eval_expression "[ebp-4]"` = `0x004927F0` ✓、`byte:[0x501BF9]` = `0x000000FF`。
  ⇒ 证明 `dword:[ebp-4]` 取值链与比较都正确；换成 `==0x497AF8` 时没暂停，
  就**不是**"条件写错"，而是**真的没发生过**。

### 4. `stop_reason` 的语义

插件把所有非 running 状态折叠成 `breakpoint_or_exception`：
**TF 单步、INT3、异常、真断点，全都是这一个字符串**。
⇒ 不能拿它当"命中了断点"的证据。

### 5. `memory_read` 与断点的关系

软断点是 x64dbg 把首字节换成 `CC` 并在读内存/反汇编时**还原显示**。
本轮 `0x43F27F` 在**有**隐藏停止原因的情况下仍读回原生 `E9`。
⇒ **判"有没有断点"只能靠 `breakpoint_get` / `breakpoint_list`**，不能看字节。

### 6. 「一次命令读多处」的坑（我本人踩的）

一次 `pwsh` 里用不同的参数文件读多个地址时，**输出只有 `"data":` 没有地址**，
我据标签把 `0x497AF8` 的 64 字节当成 `0x4927F0` 读了 ⇒ 差点把策略号当成攻击者 slot。
**规矩**：同一命令里多处读取，**每个 `"data":` 前必须自己 `echo` 出地址**，禁止只靠注释对齐。

## 实现·使用方法（测试前清场清单，照抄）

```bat
:: ① 杀搜狗（用户口径：测试时候杀掉他）
powershell -NoProfile -Command "Get-Process | ?{ $_.Name -match 'sogou|SGTool|SogouCloud|PicFace|isgpet|ichat|systembeautify' } | Stop-Process -Force"

:: ② 游戏先进战场，再 attach
python 大鲸鱼产生专用\_自动读档进战场.py --go-safe
python 大鲸鱼产生专用\_42结束回合.py --probe        :: 必须 sw4018=1

:: ③ 起 x32dbg，等 3000 端口（会先 404，正常；MCP 端点是 /mcp）
:: ④ attach
python 大鲸鱼产生专用\_x32dbg.py call debug_attach_pid <args.json>   :: {"pid":N,"attach_break":false}

:: ⑤ ★ 清掉 x64dbg 自动 TLS 断点（否则一点就卡）
python 大鲸鱼产生专用\_x32dbg.py call breakpoint_delete_all <empty.json>

:: ⑥ 只设自己的断点（≤3 个），并做对照实验确认条件有效
python 大鲸鱼产生专用\_x32dbg.py call breakpoint_set <args.json>            :: {"address":"0x4064D5","type":"software"}
python 大鲸鱼产生专用\_x32dbg.py call breakpoint_set_condition <cond.json>  :: {"address":"0x4064D5","condition":"dword:[ebp-4]==0x497AF8"}

:: ⑦ 死规则：循环放行到 running 且 Responding
python 大鲸鱼产生专用\_先放行再叫人.py --no-bp

:: ⑧ 卡住时先查 TF
python 大鲸鱼产生专用\_x32dbg.py call register_list           :: 看 eflags 有没有 0x100
python 大鲸鱼产生专用\_x32dbg.py call register_set <efl.json> :: {"name":"eflags","value":"0x00000202"}

:: ⑨ 收尾固定顺序
breakpoint_delete_all  ->  debug_run（放行）  ->  视情况 debug_stop
```

## 风险与边界

- `register_set eflags` 会改**寄存器**（不是内存/代码），暂停态下改完立即 `debug_run`；本轮游戏存活无异常。
- `breakpoint_delete_all` 会连**别人的/历史残留的**断点一起删；本会话内确认没有并行会话在同一 x32dbg 上工作才可这么做。
- 杀搜狗只解决"新线程触发 TLS 回调"，**已经注入 Ekd5 的 `sogoutsf.ime` 杀不掉**，仍需第 ⑤ 步删断点。
- 附加会让被调试进程退出后**变僵尸**（`HasExited=True` 仍占进程表）⇒ **写 `Ekd5.exe` 前必须先关 x32dbg**。
- `script_execute` / `script_get_last_result` 在本 bundle **不可用**
  （`-32003 Method not allowed: script.execute`）⇒ 别指望用脚本 `bplist`/`bc`，只能用 `breakpoint_*` 工具族。

## 证据来源

- 实机（2026-10-18 本会话，干净样本）：
  `breakpoint_list` 12 个含 TLS 断点 → `breakpoint_delete_all` `deleted_count=12` →
  复测确认框"消失=0.0s"（此前 3.0s 不消失）。
  `debug_run` ×12 停在 `0x43F27F` → `eflags=0x00200344` → `register_set eflags=0x202` → `state=running`。
  对照实验 `dword:[ebp-4]==0x4927F0` 命中，`[ebp-4]=0x004927F0`、`byte:[0x501BF9]=0xFF`。
- 工具源码：`大鲸鱼产生专用\_先放行再叫人.py`、`_x32dbg.py`、`_x32保活.py`、`_等命中读数.py`。
- 规则：`AGENTS.md` §6（x32dbg 常规辅助）、§7（先放行再叫人）。
- 相关页：`03-机制详解\特技0x71-策略反击-设计与实现.md`（钩点 `0x4064D5` 的语义争议）。

## 待验证项

- **P1**：x64dbg 的 "Break on TLS callbacks" 能否在设置里关掉（比每次 `breakpoint_delete_all` 更彻底）；
  关掉后新加载模块是否还会自动挂。未测。
- **P1**：TF 是谁置的（本轮怀疑是"删除断点后 x64dbg 原地单步过断点"残留），未定案；
  可按"删断点后立刻查一次 eflags"复现。
- **P2**：`_x32保活.py` 会在 0.05 秒内把断点命中一并放行 ⇒ **它在跑的时候不能用来抓命中现场**，
  两者互斥，需要"只放行非目标地址"的保活变体。


## ★ 2026-10-21 纠正：卡在 `gdi32full.dll` 的 TLS 回调**不是搜狗**，是 x32dbg 的「TLS 回调断点」设置

- **搜狗已卸载**（2026-10-19，记忆 `m1135`）。2026-10-21 复核：卸载项无搜狗、`[本地盘]\Program Files (x86)\SogouInput` 等目录不存在、无 sogou 进程/服务、`Keyboard Layouts` 无搜狗项、`HKCU\Keyboard Layout\Preload` 只有 `00000804`，系统 `.ime` 只剩 `msctfime.ime`；另装了 **QQ拼音 6.7**（走 msctfime，不是搜狗）。
- **真因（现读）**：`[本地盘]\新建文件夹\snapshot_2026-05-27_12-11\release\x32\x32dbg.ini` 里 `TlsCallbacks=1`、`TlsCallbacksSystem=1`
  ⇒ x32dbg 给**每一个已加载模块（含系统 DLL，如 `gdi32full.dll`）**的 TLS 回调各挂一个断点；线程创建/退出时系统会遍历各 DLL 的 TLS 回调 ⇒ 命中 ⇒ 暂停。**与输入法无关**。
- **旧口径作废**：本页 §1 与 `00-总览与规范\最小必读集与症状索引.md:292`、`06-项目与工具链\逆向调试工具链总纲-x32dbg与MCP.md:91` 的"搜狗 `SogouTSF.ime` 的 TLS 回调"是 2026-10-14 的现场归因（当时搜狗确在注入，抓到 `sogoutsf.ime+0xACC90` 假崩溃，见 `更新记录.md:13299`）；用户已定口径「**搜狗是代指**」。
- **新口径**：看到"停在 `某模块.dll` 的 TLS 回调" = **模块 TLS 回调断点**，不是输入法；模块名随机（`gdi32full`/`msctfime`/任意游戏侧 DLL 都可能）。
- **处置（按优先级）**：① x32dbg `Options → Preferences → Events` 取消 `TLS Callbacks` 与 `System DLLs`（或**关闭 x32dbg 后**把 ini 两行改 `0`）；② attach 后第一条永远 `breakpoint_delete_all`；③ 兜底 `_x32保活.py`（轮询 paused 即放行）。


### ★ 2026-10-21 21:5x 治理完成（实测判据，已生效）

- **改**：`x32dbg.ini` 的 `TlsCallbacks` 1→0、`TlsCallbacksSystem` 1→0（备份 `大鲸鱼产生专用\_归档\x32dbg.ini.bak_20261021_214435`）。
- **判据（前 → 后）**：
  - 配置：`TlsCallbacks=1 | TlsCallbacksSystem=1` → `TlsCallbacks=0 | TlsCallbacksSystem=0`；
  - 断点表：attach 后原会生成一串 `TLS callback` 断点（搜狗/系统 DLL 十余条）→ 现 `debug_attach_pid` 后 `breakpoint_list` 返回 `{"breakpoints": [], "count": 0}`（TLS 命中 0）；
  - 运行态：attach 后直接 `state=running`、`Ekd5.Responding=True`，无需 `_x32保活.py`。
- **⚠ 本次踩的坑（事故，别再犯）**：MCP 桥**没有 detach 接口**（`script_execute` 对 `detach` 返回 `Method not allowed: script.execute`）；**直接 Stop-Process 关 x32dbg ⇒ 被调试的 Ekd5 一起被终止**（调试器-被调试者同生共死），且 `debug_stop` 的语义也是"关闭目标进程"。
  **正确顺序**：x32dbg 里 `File → Detach`（或先 `debug_stop` 前确认游戏可弃）→ 再关调试器 → 再改 ini。
- **另一个坑**：旧实例被 kill 后 `127.0.0.1:3000` 处于 `TIME_WAIT`，新实例**绑不上端口**（表现为 MCP 全部 connection refused）⇒ 再起一次 x32dbg 才恢复（实测第二次 +5s 就 LISTEN）。排查命令：`Get-NetTCPConnection -LocalPort 3000 -State Listen`。


## ★★ 2026-10-21 22:0x / 22:4x 两次实测事故：后台轮询持有断点 ⇒ 游戏卡死

- **现象**：游戏「卡住」，`debug_get_state.state=paused`，`Ekd5.Responding=True`（进程没死，只是被冻住），用户点不动。
- **共同根因**：我在**后台**跑「轮询 → 命中读数 → `debug_run` 放行」的脚本，并把断点留在进程里跨回合存在。脚本一旦被我 `job_kill`（或异常退出、或 MCP 调用卡顿），**没人放行** ⇒ 进程停在断点上无限期挂起。
  - 这不是补丁/游戏问题，**也不是 TLS 回调**（当时断点表只有我设的那 1 个）。
- **强制规则（此后不得违反）**：
  1. **任何会暂停的断点，必须在同一操作回合内放行并删除**；严禁「设完断点就等用户操作、下个回合再收」。
  2. **禁止**用后台作业（`run_in_background`）持有断点做长时间抓取；要抓就用**同回合前台短窗口**，或改用**命中不暂停**的手段（日志断点 / 条件恒假只涨 `hit_count`）。
  3. 抓取脚本必须 `try/finally`：`breakpoint_delete_all` + `debug_run`。
  4. 收工自检：`breakpoint_list` 应为 `count=0`，`state=running`，`Responding=True`。
- **卡死急救三步**（实测 2 次，第 2 次即恢复）：
  ```
  python 大鲸鱼产生专用\_x32dbg.py call breakpoint_delete_all
  循环 python 大鲸鱼产生专用\_x32dbg.py state → 若 paused 则 call debug_run（≤8 次）
  python 大鲸鱼产生专用\_x32dbg.py state   # 期望 running
  Get-Process Ekd5 | Select Id,Responding  # 期望 True
  ```
- **抓参数的第二个坑（同期）**：`debug_get_state` 与 `register_list` 是两次独立调用，会读到**不一致现场**
  （实测出现过 `eip=0x43F27F`，但读出的 `arg1/arg2` 却是 `0x412B33` 那一帧的值）。
  ⇒ **必须用 `context_get_basic` 一次原子拿全 + `if eip != 目标地址: 直接放行`**；否则会把别处的寄存器当成目标帧下结论。
- 相关产物（2026-10-24 已归档到 `大鲸鱼产生专用\_归档\一次性\20261024\`）：`_tmp_T3抓参数.py`（v1，有竞态，勿用）、`_tmp_T3抓参数v2.py`（原子读）、`_tmp_T3抓护卫.py`（带 finally）。


### ★ 2026-10-21 23:0x 负结果：本环境的「零暂停断点」两条路都不通（已实测，别再试）

| 方案 | 实测 | 结论 |
|---|---|---|
| `breakpoint_set_log`（以为命中不暂停） | `breakpoint_get` 返回 `is_log_breakpoint: true`，但在 `0x4061F9` 上**每命中必停**：连续 6 秒 `state=paused`，命中 7 次 | **这条路不通**：本桥的日志断点是"带日志文本的普通软件断点"，**没有 silent 语义** |
| `breakpoint_set_condition` 条件恒假 `1==0`（以为只涨 hit_count） | 返回 `success:true`，但 `breakpoint_get` 的 `condition=null`（**条件没落库**）；6 秒内仍
 暂停 2 次，之后跑起来并累到 `hit_count=2730` | **这条路也不通**：条件不可靠，不能拿"计数"当证据 |

- **结论**：本 MCP 桥目前**没有可用的"命中不暂停"手段**。要实机取证，只剩两条：
  1. **同回合前台短窗口**（我全程盯着，命中 0.3~0.5 秒内放行，允许短暂停顿）；
  2. **纯静态定案**（优先，能用库内栈对应表+反汇编推出来的就别上断点）。
- **自检脚本（留档，可复跑）**：`大鲸鱼产生专用\_归档\一次性\20261024\_tmp_静默断点自检.py`、`_tmp_条件恒假自检.py`（同目录）。

## 7. 挂点测试必经前置：先排除 0x43F27F/TF 伪停点（2026-10-25 固化）

每次使用 x32dbg 做任何业务挂点采样，必须按以下顺序执行，缺一步就不能把停点计入业务命中：

1. 读取 debug_get_state、breakpoint_list、EFLAGS、EIP；先确认当前是否已经 paused、是否存在其他会话断点。
2. 若 breakpoint_list 为空而 EIP=0x43F27F，检查 EFLAGS bit8（TF=0x100）。TF=1 时，先只清 TF，保留其它标志位，再确认 state=running；不得把该停点记成断点命中。
3. 0x43F27F 归类为 0x43F1E8~0x43F27F 预览/实战共用特技修正链尾；它只执行无条件 jmp 0x43BDCC，不是 0x44E0D9、0x44E540、0x44E54D 的入口。
4. 只有 state=running、TF=0、断点列表只含本轮登记的目标点后，才允许布置业务断点；hit_count 只能证明地址执行过，不能证明条件成立或真实攻击发生。
5. 采样结束必须先删除本轮自有断点，再复读 breakpoint_list、debug_get_state、EFLAGS；发现非目标停点时停止采样，不盲目 debug_run。

本条是挂点测试的硬前置，适用于普通行动、策略先手、先手攻击、斗将和转移策略链；证据依据为 0x43F27F 当前字节、共享预览链静态结构及 TF=0x100 导致的实测伪停点。


## 8. 2026-10-26 工具护栏修复：默认不再盲目 debug_run

- **当前样本复读**：`Ekd5.exe` SHA256=`2B279F3F0A917B1BD6E6F812E473DFB4B06A4101F38903EE1092EF3BDB70652A`；`exe_bytes(0x43F27F,8)`=`E9 48 CB FF FF 90 90 90`，说明该处仍是原生无条件 `jmp 0x43BDCC`，不是软件断点字节。
- **配置排除**：当前 `x32dbg.ini` 已为 `TlsCallbacks=0`、`TlsCallbacksSystem=0`；本轮不再把反复停在 `0x43F27F` 归因于 TLS 自动断点。
- **重复根因收口**：旧版 `_x32保活.py` 对所有 `state=paused` 直接 `debug_run`，且后台保留断点；旧版 `_42起桥并附加.py` attach 后未固定先 `breakpoint_delete_all`，随后对暂停态连续盲放行；旧版 `_先放行再叫人.py` 也未先核对 EIP/EFLAGS。三者会把 TF 单步陷阱、业务断点和未知异常混成同一条 `breakpoint_or_exception`。
- **已改既有工具（未新建脚本）**：
  1. `_x32保活.py` 默认只接受“`EIP=0x43F27F` + 该地址不在 `breakpoint_list` + `EFLAGS&0x100`”这一可证伪条件，清 TF 后才 `debug_run`；业务断点、无断点异常、TF 不明均立即停止。旧行为仅显式 `--legacy` 可用，禁止用于业务取证。
  2. `_42起桥并附加.py` attach 返回后第一条命令固定 `breakpoint_delete_all`，只在确认 TF 伪停点时清 TF/放行；未知暂停返回非零并保持现场。
  3. `_先放行再叫人.py` 复用 `_x32保活.py` 的同一判定，不再自己循环盲放行。
- **离线验证**：三脚本 `py_compile` 全部通过；模拟 TF 现场得到 `EFLAGS 0x00200344→0x00200244`、返回 `running`；模拟业务断点 `0x405E9A` 得到“保持暂停、不盲目继续”。无游戏时安全保活运行 1 秒恢复 0 次，`_42起桥并附加.py --check` 正确报告 `Ekd5.exe 不在运行`。
- **运行时边界**：以上是工具护栏修复，不等于实机已闭环。下一次实机必须先确认 `breakpoint_list`、`context_get_basic(EIP/EFLAGS)`、`state=running`、`Responding=True`，再按用户新规则单次最多推进 5 回合；若 `0x43F27F` 再出现而 TF=0，立即停测并保留现场，不得重复 `debug_run`。
- **证据等级**：当前字节/配置=静态复读；工具行为=源码复核+离线模拟；“实机不再重复停点”=待下一次≤5回合动态对照。


## 9. 2026-10-26 实机复现与完整修复闭环

- **复现条件**：当前基底 SHA=`2B279F3F0A917B1BD6E6F812E473DFB4B06A4101F38903EE1092EF3BDB70652A`，No.001，`4018=1`，挂接后 `breakpoint_list=[]`、初始 `state=running`。自动战斗批次严格只尝试 1 回合。
- **停点现场**：批次动作后复读 `state=paused`、`EIP=0x43F27F`；`breakpoint_list=[]`；`context_get_basic` 的 `EFLAGS=0x00200344`（`TF=0x100`）；游戏仍在战场 `phase=1`、`enemy_alive=50`，但 `Responding=False`。线程表共 20 条，其中当前线程外 19 条 `is_suspended=true`，Windows 线程也显示 `WaitReason=Suspended`。这把“TF 伪停点”和“线程组未恢复”两段因果同时钉死。
- **修复动作**：修正 `context_get_basic` 的真实 `registers[].{name,value}` 解析；安全护栏清 `TF` 后执行 `debug_run`，再遍历 `thread_list`，对仍为 `is_suspended=true` 的线程逐一调用既有 `thread_resume`。本次现场先恢复 1 条后该线程退出，再恢复剩余 18 条。
- **修复后判据**：x32dbg `state=running`、`breakpoint_list=[]`、EIP 转到 `0x76F0A0BC`/`0x76F087FC`；`_42起桥并附加.py --check` 复读 `Responding=True`、`battle=true`、`4018=1`；`_42结束回合.py --probe` 复读 `phase=2`、`enemy_alive=49`、`alive=53`。随后只读轮询 6 次（间隔 0.5 秒）均为 `state=running`，没有再次回到 `0x43F27F`。
- **边界**：这次只完成 1 回合尝试及停点修复，没有继续第二回合；因此证明的是“TF+线程组半冻结已可识别和恢复”，不是业务挂点参数语义闭环。
- **最终定性**：`0x43F27F` 重复吃亏的根因不是 EXE 字节、不是 TLS 配置、也不是业务入口；是 x32dbg 在单步陷阱后只恢复当前线程，旧工具又无条件 `debug_run`，导致其余线程持续 `Suspended`。后续实机必须把“清 TF + 恢复 debugger-suspended 线程 + Responding=True”作为同一前置判据。
