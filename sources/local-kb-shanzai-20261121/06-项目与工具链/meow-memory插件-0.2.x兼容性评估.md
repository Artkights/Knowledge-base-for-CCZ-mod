# meow-memory（DSH 跨会话记忆插件）— 0.2.x 兼容性评估

## 结论速览

- `meow-memory` 0.31.0 是真实存在的 DSH 专用插件（GitHub `Phant0Meow/dsh-meow-memory`，npm `meow-memory`，MIT，零运行时依赖，SQLite 存 `.dsh-meow/memory.db`）。
- **本机暂不安装到 `desktop` 主 profile**：本机 DSH 为 `0.2.1-rc.2`，插件 README 只声明适配 `0.1.5`；open issues #72/#53/#58/#54 明确 0.2.x 下折叠/注入横条失效，#66 是 dream 后工具集被锁成 9 个工具、必须重启 DSH，#35 是冷启动窗口不显示，#60 是宿主进程无法退出。
- **它不是跨 AI 共享记忆**：插件只由 DSH bundle 加载，Codex / TRAE 不加载；数据库按工作区独立。现有 `kb` MCP 的 `memory_*`（`ai使用库\AI协作\记忆库\记忆.jsonl`）仍是 DSH/Codex/TRAE 三方共用记忆层。
- 给协作者的口径：**等作者修复 0.2.x 后再评估**；如要试装，先在隔离 profile / 可丢弃工作区做，并备份 `~/.dsh/profiles/desktop`，不要在主游戏任务进行中的会话上装。

## 适用版本

| 项 | 值 |
|---|---|
| 本机 DSH | `0.2.1-rc.2`（`dsh --version`） |
| Profile | `desktop`（`[本地盘]\Users\Administrator\.dsh\profiles\desktop`） |
| 宿主 Node / pnpm | `24.21.0` / `11.28.5`（`resources\runtime\versions.json`） |
| 插件 | `meow-memory` 0.31.0（npm 最新，2026-10-08 发布；GitHub main 最后提交 2026-10-17） |
| 插件声明兼容 | dsh `0.1.5`（含 0.1.5-rc.1；实测 0.1.1-rc.2 旧版行为一致） |
| OS | Windows 10 19045 |
| 当前安装状态 | 未安装：`profiles\desktop\node_modules\meow-memory` 不存在 |

## 已确认事实

- 仓库与 npm 包均存在；npm 页面显示 0.31.0、30 个版本、周下载 1,519（2026-10-21 抓取）。
- 插件形态：`dsh.bundle.patch` + `dsh.client.platform=web`；`main=lib/index.js`、`exports ./client`；`files` 只发 `lib/`、`cordis.patch.yml` 等预构建产物。
- 运行时要求 Node ≥ 22.13（`node:sqlite`）；本机 Node 24.21.0 满足。
- 记忆工具（README 列 8 个）：`memory_remember` / `memory_search` / `memory_project` / `memory_find_similar` / `memory_read` / `memory_update` / `memory_dream` / `memory_home`，另有 `/dream` 命令。
- 七层：soul / user / project（含 subcategory）/ fact / lesson / topic / rules；每层一张 SQLite 表。
- 注入机制：首轮长期记忆快照（独立 plugin snapshot，不改写用户 prompt）；第二轮起每条用户消息关键词命中 top-2；命中打分 = 交集分 × idf × 覆盖率 × 艾宾浩斯衰减 × importance × title 加成，`memory_search` 另用 BM25 × 近期权重；静态 guide section 固定文本，缓存友好。
- 记忆整理：窗口空闲 ≥180 分钟触发 dream（默认峰时 09:00–12:00、14:00–18:00 抑制）；连续 ≥7 个工具 step 触发反思。
- **0.2.x 兼容问题（open，未随 0.31.0 修复）**：
  - #72：dsh 0.2.1-rc.2 + meow-memory main，折叠/注入横条全缺；根因是 `chat.order` 漏 context 节点、`getTurn` key 失配、注入行 key 不匹配；issue 内给出修法 commit 59bf004 / e0948b8，未见已发布修复。
  - #53：dsh 0.2.0-rc.2 把 `conversation.composer.dock` props 改成空 `{}`，四套折叠横条静默失效；v0.31.0 同款 `props?.useChat` 写法仍受影响。
  - #58：0.2.0-rc.2 `slots.inject` 回调未触发，dock 条目从未注册。
  - #54：0.2.0-rc.2 重启后新会话 fold 锚点为 0、dream 任务卡不显示。
  - #66：0.31.0 在 dream/reflect 后把会话工具集锁成 9 个（只剩 `memory_*` + `load_workspace_dependencies`），需重启 dsh 才恢复。
  - #35：0.2.0-rc.2 + dsh-desktop，安装 0.29.0 后冷启动窗口不显示，宿主子进程 startup 阶段退出。
  - #60：dream 调度器/心跳定时器未 unref，宿主进程无法退出，桌面端更新报 graceful teardown 失败。

## 实现·使用方法（仅作参考，本机未执行）

### 安装（若将来版本兼容）

```powershell
# 官方推荐：从 GitHub 装（会跑 prepare 构建）
dsh plugin --profile desktop add github:Phant0Meow/dsh-meow-memory

# 或从 npm 装（包内有预构建 lib/）
dsh plugin --profile desktop add meow-memory

# 卸载
dsh plugin --profile desktop remove meow-memory
```

- pnpm ≥10 默认阻止安装期构建脚本，首次 `add` 若提示 `allowBuilds`，按提示把键加入 `profiles\desktop\pnpm-workspace.yaml` 后重跑。
- 装完必须重启 DSH；新会话才加载插件。
- 手动方式（开发者）：把包 junction 到 `profiles\desktop\node_modules\meow-memory`，再把 `meow-memory` 加进 profile `package.json` 的 `dsh.profile.bundles`，重启 DSH。

### 配置（profile patch 或 `cordis.patch.yml`）

```yaml
- id: meow-memory
  name: 'meow-memory'
  config:
    enabled: true
    projectDir: '.dsh-meow'
    promptLang: 'zh'      # 首次使用必须显式配置；填不存在的值会静默落回中文包
    hitTopK: 2
    dream:
      enabled: true
      idleMinutes: 180
```

- 设置页有「喵记忆」标签页，字段级保存、可单项恢复默认；保存后热重载/重启插件生效。
- 数据位置：`<工作区>\.dsh-meow\memory.db`，会话去重记录 `sessions/<id>.json`。
- 记忆语言由 `promptLang` 决定（zh/en/pt-br），影响模型写条目与关键词提取。

### 对协作者的可用性

| 协作者 | 能否使用 | 说明 |
|---|---|---|
| DSH | 可以（版本兼容时） | 只有 DSH 加载插件 bundle；工具名 `memory_*` |
| Codex | 不能 | 不加载 DSH bundle；继续用 `kb` MCP 的 `memory_*` |
| TRAE | 不能 | 同上；TRAE 不加载 DSH 插件，只通过 `kb` MCP 共享 |
| 共享记忆 | 不共享 | meow-memory 的 SQLite 是 DSH 单方；与 `ai使用库\AI协作\记忆库\记忆.jsonl` 是两套 |

## 风险与边界

- **安装即改 profile**：`dsh plugin add` 会写入 profile 的依赖与锁文件；是否自动加入 `dsh.profile.bundles` 取决于 dsh plugin 版本。安装前备份 `~/.dsh/profiles/desktop`（至少 `package.json`、`pnpm-lock.yaml`、`pnpm-workspace.yaml`、`cordis.patch.yml`）。
- **重启风险**：本机 DSH 参与游戏任务协作；重启会中断当前 DSH 会话，且 #35 报告冷启动可能不弹窗。
- **工具集锁死**：#66 在 dream 后把会话工具集锁到 9 个，影响 DSH 正常读/写/执行；只有重启恢复。
- **UI 静默失效**：0.2.x 的折叠/注入横条缺失不报错，容易误判“插件没工作”；实际核心注入/工具可能仍在，需单独验证。
- **记忆不共享**：不要把它当成 DSH/Codex/TRAE 的共同记忆；三方协作仍以 `kb` MCP 的记忆层 + 知识库页 + 台账/交接为准。
- **promptLang 逐字匹配**：填 `pt` 之类不存在的值不报错，会静默落回中文包。
- **数据目录**：`.dsh-meow/` 会出现在每个工作区；若纳入 git，需要像 `记忆库/备份` 一样做忽略策略。

## 证据来源

- GitHub 仓库：http[本地盘]//github.com/Phant0Meow/dsh-meow-memory（README 功能/安装/兼容性；CHANGELOG）
- npm：http[本地盘]//www.npmjs.com/package/meow-memory（0.31.0，30 versions，MIT，周下载 1,519）
- 包清单：http[本地盘]//raw.githubusercontent.com/Phant0Meow/dsh-meow-memory/main/package.json
- Open issues（2026-10-21 抓取）：#72、#53、#58、#54、#66、#35、#60
- 本机实测：
  - `dsh --version` → `0.2.1-rc.2`
  - `[本地盘]\Users\Administrator\.dsh\profiles\desktop\package.json`（bundles 无 meow-memory）
  - `Test-Path ...\node_modules\meow-memory` → `False`
  - `resources\runtime\versions.json` → node 24.21.0 / pnpm 11.28.5
- 本页由 TRAE 依据上述公开资料与本机只读检查整理；未安装、未重启 DSH、未修改 profile。

## 待验证项

- **P0**：0.2.x 修复是否已合并/发布（关注 #72 的 59bf004、e0948b8 与后续 release；当前 npm 最新仍是 0.31.0）。
- **P0**：#66 工具集锁死是否有修复；在修复前不做主 profile 安装。
- **P1**：0.2.1-rc.2 上核心注入/记忆工具是否仍可用，还是仅 UI 折叠条失效（#72 只证明 UI 层断点）。
- **P1**：隔离 profile / 可丢弃工作区试装的完整步骤与回滚（备份 profile、`dsh plugin remove`、删除 `.dsh-meow`）。
- **P2**：与现有 `kb` 记忆层的分工：若将来 DSH 单方使用 meow-memory，是否需要把关键条目同步到共享 `记忆.jsonl`，避免三方记忆分叉。
- **P2**：`.dsh-meow` 的 git 忽略与备份策略。

---
（本页仅评估，不代表已安装或已启用。）
