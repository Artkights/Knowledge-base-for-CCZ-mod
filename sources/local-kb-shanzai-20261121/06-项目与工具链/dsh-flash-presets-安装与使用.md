# dsh-flash-presets（DSH Flash 预设）安装与使用

## 结论速览

- 仓库：`http[本地盘]//github.com/LarryE135/dsh-flash-presets`（DSH 组合包 `dsh.bundle`，MIT）。
- 安装（desktop profile，2026-10-21 已执行成功）：`dsh plugin --profile desktop add github:LarryE135/dsh-flash-presets` → 依赖 `dsh-flash-presets 0.2.1` 已写入 `~/.dsh/profiles/desktop/package.json` 的 `dsh.profile.bundles`。
- **desktop profile 由 Electron 应用独占管理**：`dsh --profile desktop --dump-config` 会报 `profile "desktop" is managed exclusively by the Electron application` ⇒ **必须重启 DSH 桌面应用**才能加载 v1/v2/v3；CLI 不能热加载，也看不到 dump。
- 预设影响三件事：**预算与轮数（按轮计）**、**工具输出的折叠/裁剪**、**判定任务完成的标准**；不提升模型能力，只决定一次会话花多少轮、在哪停、用什么标准收尾。

## 预设

| 预设 | id | order | 规则条数 | 压缩 | 用途 |
|---|---|---|---|---|---|
| v1 | `flash-lean-ptc-v1` | 21 | 14 | 0.3 / 50k | 上下文余量优先，任务偏长 |
| v2 | `flash-lean-ptc-v2` | 22 | 12 | 0.25 / 20k | 与 v1 同代，更省，保守选择 |
| v3 | `flash-lean-ptc-v3` | 27 | 13 | 0.25 / 20k | **默认**（lean-v3，对齐 DSH 0.2.1-rc.2） |

三者可同时安装，在预设列表里逐项选择，互不影响。

## 用户补充的使用要点（2026-10-21 用户口径）

1. **使用前先装并应用 MSI 版 PowerShell 7 或 Git Bash**（仅这一点就有不少提升；不会装就问「大肥鱼」）。
2. **输出最好不要低于 120k**。
3. **这是目标导向插件**：只有目标明确、验收标准准确时才稳定发挥上限，且越清晰效果越好；**验收标准不明确的前端工作（或 Oneshot 样例）效果可能不及预期**。
4. 编写提示词时**可以对「大肥鱼」狠点**，主动要求 **Token maxxxing** 或应用高标准（原理类似 RP），不确定时结合 **plan mode** 使用。
5. 插件的开发与测试**围绕洛谷公开题库**展开，按 **Token 消耗 / 完成用时 / 步数 / 运行时内存占用与时间加权**评价，**有一定局限性**；后续反响好会做其他方向适配。

## 安装/更新/卸载（README 原文要点）

- 组合包：`dsh plugin --profile <web|desktop|headless|acp> add github:LarryE135/dsh-flash-presets`；GUI「插件 → 添加插件」填同一地址等效。
- 更新：重复执行 `add`，或先 `remove` 再 `add`。
- 卸载：从 `dsh.profile.bundles` 与依赖移除后重装依赖；脚本写入的托管块用 `scripts/install.sh --uninstall` 清除。
- 脚本方式（Windows）：`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install.ps1 [-Profile desktop] [-Uninstall]`；安装器先备份 `cordis.patch.yml.bak-<时间戳>`。
- 校验：`node scripts/verify-presets.mjs` / `verify-yaml.mjs` / `compose-bundle-patch.mjs --check`。

## 已安装状态（2026-10-21）

- `~/.dsh/profiles/desktop/package.json` 依赖：`dsh-flash-presets: github:LarryE135/dsh-flash-presets`；`dsh.profile.bundles` 末尾已含 `dsh-flash-presets`。
- 包内 `cordis.patch.yml` 含 3 个 `insert`（`preset-flash-lean-ptc-v1/v2/v3`），`presets/*.patch.yml` 齐全。
- **待生效**：重启 DSH 桌面应用后，在「插件 → 预设」中选择 v3（默认）。

## 风险与边界

- 未验证：macOS 真机；native 模式同规模对照（README 自述）。
- 插件改的是 profile 配置（`cordis.patch.yml` 托管块 + `dsh.profile.bundles`），**不改宿主代码、不动共享工具注册表**。
- 重启 DSH 会中断当前会话；建议在会话收尾/空闲时重启。
- 若重启后预设列表没有 v1/v2/v3：检查 `package.json` 的 `dsh.profile.bundles` 是否仍含 `dsh-flash-presets`，或重跑一次 `add`。

## 证据来源

- 仓库 README（2026-10-21 抓取，raw.githubusercontent.com，7850 字节）。
- 本地安装输出：`dsh plugin --profile desktop add github:LarryE135/dsh-flash-presets` → `dependencies: + dsh-flash-presets 0.2.1` / `Done in 9.7s`。
- `dsh --version` = `0.2.1-rc.2`；`dsh --profile desktop --dump-config` 报 Electron 独占。
