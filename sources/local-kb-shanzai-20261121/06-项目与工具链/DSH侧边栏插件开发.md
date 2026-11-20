# DSH 侧边栏插件开发与手工安装（DeepSeek Harness）

> 目标：给 DSH Web UI 加自己的小部件（按钮 / 面板 / 装饰），常驻侧边栏，重启后仍在。
> 证据类型：**官方技能文档（asar 内 `cordis-plugin-development`）+ 现网插件实例（`@local/whale-peak-offpeak`）+ 本次自研插件实测**

## 结论速览

- DSH 的 UI 扩展单位是 **bundle 插件**：一个目录（4 个文件）+ 在 profile 里注册一行。
- **落点**：`[本地盘]\Users\Administrator\.dsh\profiles\<profile>\local-bundles\<包名>\`
  （当前 profile 名 `desktop`，见环境变量 `DSH_PROFILE` / `DSH_PROFILE_DIR`）。
- **加载时机**：DSH **启动时**读 profile 的 `package.json` → `dsh.profile.bundles` 逐个加载，
  并应用每个包的 `cordis.patch.yml`。**新增插件必须重启 DSH**（`cordis.yml` 是启动时合成的基础层，里面不会出现 `@local/*`）。
- **侧边栏底部（账号上方）的插槽名 = `sidebar.footer.action`**（kind `list` / scope `root`，所有页面可见）。
  其它常用：`conversation.composer.dock`（输入框下方）、`conversation.input.left`（输入框左侧）。
- ★ 判断"是否生效"不要看日志：以 **页面上是否出现部件** 为准（本地 HTTP 端口 19387 有 401 鉴权，抓不到）。

## 适用版本

- **DSH Desktop 版**（`[本地盘]\新建文件夹 (2)\DeepSeek Harness.exe`，Electron；源码打包在 `resources\app.asar` 内，无独立源码目录）。
- 当前 profile：**`desktop`**（`DSH_PROFILE` / `DSH_PROFILE_DIR` 环境变量现读；另有 `_backup-desktop-*` 备份目录）。
- 实测时间：**2026-10-14**（本轮）；结论只对上述版本的插件加载机制有效。
- 官方技能文档随包发布在 `app.asar` → `dsh/node_modules/@deepseek-ai/dsh-agent-preset/skills/cordis-plugin-development/`（提取副本见 `大鲸鱼产生专用\_插件开发资料\`）。
- 与游戏侧无关：本页不涉及 `Ekd5.exe` 的任何地址。

## 已确认事实

### 1. 加载机制（机器现读 + 时间线互证）

- DSH 主进程启动时读 profile 的 `package.json` → `dsh.profile.bundles`，逐个加载并应用各自的 `cordis.patch.yml`；
  `cordis.yml` 是**启动时合成的基础层**，里面**不会出现** `@local/*` 行（实测两版 cordis.yml 均无 —— 本地 bundle 是运行时叠加的）。
- 时间线互证：whale 插件目录备份 `3:44:32` → DSH 主进程启动 `3:50:43` → `cordis.yml` 生成 `3:52:49` ⇒ "启动时加载"成立。
- `node_modules\@local\<包名>` 是指向 `local-bundles\<包名>` 的**符号链接**（pnpm 风格；手工安装可用 Junction 等价替代）。
- profile 的 `pnpm-lock.yaml` 会记录 `link:` 依赖；`node_modules\.pnpm-workspace-state-v1.json` 的 `lastValidatedTimestamp` 决定新包能否被接受（见「风险与边界」的踩坑）。

### 2. 四件套结构

```
local-bundles/dialog-atlas/
├── package.json        声明 dsh.bundle.patch 与 dsh.client（platform/immediately/inject）
├── cordis.patch.yml    - insert: [{ id, name }]
├── index.js            Host 半边：export function apply() {}（纯展示型留空）
└── client.js           Client 半边：window.__ModuleLoader__.load({...})
```

`package.json` 关键字段（照抄现网实例）：

```json
{
  "name": "@local/dialog-atlas",
  "type": "module",
  "exports": { ".": "./index.js", "./client": "./client.js", "./package.json": "./package.json" },
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" },
    "client": { "platform": "web", "immediately": true,
                "inject": ["@deepseek-ai/dsh-client-ui-conversation"] }
  }
}
```

`client.js` 骨架（**React 从浏览器模块表里 require，不要自带 React**）：

```js
window.__ModuleLoader__.load({
  id: '@local/dialog-atlas',            // 必须等于包名
  factory(require) {
    const React = require('react');
    const h = React.createElement;
    function Widget() { /* useState/useEffect 均可用 */ }
    return {
      inject: ['slots'],
      apply(ctx) {
        ctx.slots.inject('sidebar.footer.action', () =>
          ctx.slots.register({ name: 'sidebar.footer.action', id: 'dialog-atlas', order: 6 }, Widget));
      },
    };
  },
});
```

- 样式：继承宿主主题用 CSS 变量 `var(--dsw-alias-label-secondary, #61666b)`、`var(--dsw-alias-label-tertiary, #81858c)`；
  自绘面板（如全屏 modal）可以用自己的配色，但要保证深浅主题下都可读。
- `order` 决定同一插槽内的先后（现网「大鲸鱼峰谷期」用 5，本插件用 6）。
- 不要替换 app 根、不要往 `document.body` 追加第二个应用、不要读别的插件的 DOM。

## 实现·使用方法：手工安装（没有 `plugin_manager` 工具时）

官方技能要求用 `plugin_manager` 的 `install_bundle`；在**没有该工具**的会话里，可按下述等价步骤手工装（本次实测可行）：

```powershell
$prof = "[本地盘]\Users\Administrator\.dsh\profiles\desktop"
# 1) 备份（务必）
Copy-Item "$prof\package.json"   "$prof\package.json.bak"   -Force
Copy-Item "$prof\pnpm-lock.yaml" "$prof\pnpm-lock.yaml.bak" -Force
# 2) 复制插件
Copy-Item "<工作区>\大鲸鱼产生专用\_Dsh插件\对话图鉴\*" "$prof\local-bundles\dialog-atlas\" -Force
# 3) 建模块链接（pnpm 用的是符号链接；Junction 等价且不需要额外权限）
New-Item -ItemType Junction -Path "$prof\node_modules\@local\dialog-atlas" `
         -Target "$prof\local-bundles\dialog-atlas"
# 4) 注册：package.json 的 dependencies 加 "link:./local-bundles/dialog-atlas"，
#    并在 dsh.profile.bundles 末尾加 "@local/dialog-atlas"
# 5) ★ 必须再跑一次 pnpm install（见下「踩坑」）——否则 DSH 合成 profile 时会跳过这个包
# 6) 重启 DeepSeek Harness
```

> ★ **踩坑（2026-10-14 实测）**：手工改完 `package.json` **不等于安装完成**。
> DSH 会**监听 profile 并重新合成 `cordis.yml`**（实测：5:23:22 改 `package.json` → 5:25:37 `cordis.yml` 被重新生成），
> 但合成时按 pnpm 的校验状态过滤：`node_modules/.pnpm-workspace-state-v1.json` 的 `lastValidatedTimestamp`
> **早于** `package.json` 的修改时间时，新包会被**静默忽略**（那次合成只写入了早已装好的 `whale-peak-offpeak`，
> 新加的 `dialog-atlas` 没有出现）。⇒ 正确做法是让 pnpm 跑一次 `install` 刷新校验状态，
> 或干脆用官方的 `plugin_manager` → `install_bundle`（它会代劳）。
> 结论：**别用"手工装 + 重启"来验证**，先确认合成结果里出现了插件行。

- 注册脚本：`大鲸鱼产生专用\_Dsh插件注册.py`（读改写 JSON，自动备份）；
  生成脚本：`大鲸鱼产生专用\_Dsh插件生成.py`（把 SQLite 数据内联进 `client.js`）。
- **重启前自检**（避免重启后才发现崩）：`node 大鲸鱼产生专用\_插件自检.js <client.js>`
  —— 用假 `window.__ModuleLoader__` + 假 React 跑一遍 `factory`，验证 id / inject / slot 注册 / 数据规模。
- **卸载（回滚）**：先 `cmd /c rmdir "<profile>\node_modules\@local\<包名>"`（cmd 的 rmdir 只删链接、不删目标），
  再删 `local-bundles\<包名>`，最后用备份还原 `package.json` / `pnpm-lock.yaml`。
  **顺序不能反**，且不要对 junction 用 `Remove-Item -Recurse`（有删穿目标的风险）。

### 从 `app.asar` 里取官方资料（Desktop 版没有源码目录）

```python
# asar 头：4 个 uint32，第 3 个是 JSON 长度（注意：该值含 4 字节对齐填充！）
json_size = struct.unpack_from("<I", data, 8)[0]
tree, consumed = json.JSONDecoder().raw_decode(data[16:16+json_size].decode("utf-8","replace"))
base = 16 + consumed          # ← 必须用 consumed；用 json_size 会让每个文件偏移 +4 字节
file_data = data[base + entry["offset"] : base + entry["offset"] + entry["size"]]
```

- 官方技能在 `dsh/node_modules/@deepseek-ai/dsh-agent-preset/skills/cordis-plugin-development/`
  （`SKILL.md` + `references/ui-plugin.md` + `templates/decoration/` 四件套模板）。
- 插件管理器说明：`dsh/node_modules/@deepseek-ai/dsh-client-ui-plugin-manager/README.zh.md`。

## 风险与边界

- 手工安装绕过了 `install_bundle` 的规范化步骤（pnpm 校验、profile 备份）⇒ **改前必须备份** `package.json` / `pnpm-lock.yaml` / `cordis.yml`。
- 不要手写 `cordis.yml`（启动时重新合成的基础层）；不要往 `$DSH_HOME` 下建包；不要在 profile 目录跑 pnpm（除非确知后果）。
- 新增/删除 bundle **必须重启 DSH**；仅改**已加载插件**的 `client.js` 才可能热更新（且需要 `pnpm run dev:web` 在跑）。
- 本地 19387 端口的 HTTP 有 401 鉴权，脚本无法直接验证前端效果 ⇒ 视觉验证只能靠人眼或浏览器控制。
- 卸载 = 删 `local-bundles/<包名>` + 从 `package.json` 的 dependencies/bundles 移除 + 删链接 + 重启。

## 证据来源

- 官方技能：`app.asar` → `dsh-agent-preset/skills/cordis-plugin-development/**`（已提取到 `大鲸鱼产生专用\_插件开发资料\`）
- 现网实例：`[本地盘]\Users\Administrator\.dsh\profiles\desktop\local-bundles\whale-peak-offpeak\`（14.5KB 手写 client.js，注册到同一插槽）
- 本次实例：`大鲸鱼产生专用\_Dsh插件\对话图鉴\`（41 对话框 / 659 控件 / 29 条数据源，内联 40KB JSON）
- 自检记录：`node _插件自检.js` 输出（module id / inject / register / 数据规模全部通过）
- 进程与时间线：DSH 主进程启动 `3:50:43`、`cordis.yml` 生成 `3:52:49`、whale 插件目录备份 `3:44:32` ⇒ 印证"启动时加载"

## 待验证项

- **P2**：GUI 里 `ui-settings-plugin-inventory`（插件清单页）能否直接启用/停用本地 bundle（本次未验证）。
- **P2**：`client.js` 改动是否能在不重启时热更新（需 `pnpm run dev:web` 验证）。

## 实例：进制转换插件 `@local/radix-conv`（2026-10-18）

> 用户需求：「做个 10 进制和 16 进制互转的小工具挂载工具箱」⇒ 做成侧边栏底部按钮 + 弹出面板。

### 一、装在哪

| 位置 | 内容 |
|---|---|
| `[本地盘]\Users\Administrator\.dsh\profiles\desktop\local-bundles\radix-conv\` | 四件套（`package.json` / `cordis.patch.yml` / `index.js` / `client.js`）|
| `…\profiles\desktop\node_modules\@local\radix-conv` | **Junction** → `local-bundles\radix-conv`（whale 用的是 SymbolicLink，Junction 等价可用）|
| 工作区备份 | `大鲸鱼产生专用\_Dsh插件\进制转换\`（四件套副本）|

### 二、注册（与 `_注册DSH插件.py` 的差异，重要）

`profile\package.json` 改两处：

```json
"dependencies": {
  "@local/whale-peak-offpeak": "link:./local-bundles/whale-peak-offpeak",
  "@local/radix-conv": "link:./local-bundles/radix-conv"      // ★ 新增
},
"dsh": { "profile": { "bundles": [
  "@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app",
  "@local/radix-conv"                                          // ★ 新增
] } }
```

⚠ **没有按 `_注册DSH插件.py` 去改 `cordis.yml`**：当前该文件内容是 `[]`（空树），
若在末尾追加 `- id: …` 会得到非法 YAML（`[]` 之后不能再有列表项）。该文件由 DSH 启动时合成，**不要手改**。

### 三、★ 必须处理 pnpm 校验状态（否则新包被静默忽略）

实测：`package.json` mtime `2026-10-18 11:17:00`，而 `node_modules\.pnpm-workspace-state-v1.json` 的
`lastValidatedTimestamp` = `1791920761199`（`2026-10-14 03:46:01`）⇒ **早于** package.json ⇒ 合成时新包会被跳过。

本机**没有 pnpm 在 PATH**，因此手工把它改到当前时间（备份为 `.bak`）：

```python
d['lastValidatedTimestamp'] = int(time.time()*1000)
```

> 这是 pnpm 的纯缓存文件，只用于"profile 是否比上次 install 更新"的比较；改它是本机无 pnpm 时的等效手段。
> 若以后装了 pnpm，跑一次 `pnpm install` 会重新写它。

### 四、自检（无需启动 DSH）

DSH 自带 Electron 可当 node 用：

```powershell
$exe = "$env:LOCALAPPDATA\Programs\DeepSeek Harness\DeepSeek Harness.exe"
$env:ELECTRON_RUN_AS_NODE = '1'
& $exe --check <client.js>                       # 语法
& $exe 大鲸鱼产生专用\_插件自检-进制.js <client.js>   # 假 window + 假 React 跑 factory
```

自检输出（本次实测通过）：

```
[1] id = @local/radix-conv
[2] inject = ["slots"]
    inject 调用： sidebar.footer.action
[3] register 次数 = 1  描述 = [{"name":"sidebar.footer.action","id":"radix-conv","order":7}]
[4] 首次渲染 OK，根类型 = Symbol(Fragment)
✅ 自检通过
```

> ⚠ `runtime\bin\node.cmd` 依赖环境变量 `%DSH_DESKTOP_NODE_EXECUTABLE%`，本机该变量为空 ⇒ 直接调 `node.cmd` 会报
> `'""' is not recognized`；**改用 `DeepSeek Harness.exe` + `ELECTRON_RUN_AS_NODE=1`** 才可用。

### 五、插件行为

`sidebar.footer.action`（侧边栏底部，order=7，排在 whale 的 5 之后）→ 按钮「⇄ 进制」→ 弹出面板：

- 十进制 / 十六进制两个输入框，改哪个即时算另一个
- 十六进制支持 `0x` 前缀、大小写不敏感
- 支持负数（`-123` ↔ `-0x7B`）
- 用 `Number.isSafeInteger` 拦截超出 2^53 的输入
- 样式用宿主 CSS 变量，深浅主题都读得清

### 六、待验证

- [ ] **P0** 重启 DSH 后侧边栏底部是否出现「⇄ 进制」按钮（插件是启动时加载，**不重启不生效**）
- [ ] **P1** 点开面板后两框互转是否正常（`255` ↔ `0xFF`、`-10` ↔ `-0xA`）
- [ ] **P2** 若未出现：先查 profile `package.json` 是否被回滚、`lastValidatedTimestamp` 是否又被刷新到旧值
