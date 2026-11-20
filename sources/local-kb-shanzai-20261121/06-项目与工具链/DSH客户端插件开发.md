# DSH 客户端插件开发

## 结论速览

- **DSH 支持本地客户端插件**：能往 Web GUI 里加自己的按钮 / 面板（侧边栏、输入区）。
- 插件放在 **profile 目录**（可写）：`[本地盘]\Users\Administrator\.dsh\profiles\desktop\local-bundles\<名>\`。
- 注册需要**四处**都到位，缺一不可；**`node_modules\@local\<名>` 符号链接最易漏**。
- **改动后必须重启 DSH**（插件在启动时注册）。
- 本机无独立 node，但可用 `ELECTRON_RUN_AS_NODE=1 "<DSH>\DeepSeek Harness.exe" x.mjs` 当 node 跑自检。

## 适用版本

- DeepSeek Harness 桌面版（profile `desktop`）。cordis 应用架构。

## 已确认事实

### 1. DSH 的运行结构（进程命令行实测）

```
"[本地盘]\新建文件夹 (2)\DeepSeek Harness.exe"                      ← Electron 主进程
"…\DeepSeek Harness.exe" --expose-internals
    "…\resources\app.asar\dsh\node_modules\@deepseek-ai\dsh-desktop-host\lib\index.js"
    "…\resources\app.asar\dsh"                                 ← DSH 根
    "[本地盘]\Users\Administrator\.dsh\profiles\desktop"             ← ★ profile（可写）
    "…\resources\runtime\primary-runtime"
    "…\resources\runtime\pnpm\bin\pnpm.mjs"
    "…\resources\runtime\bin"
```

- `app.asar`（115.7 MB）只是**打包的 Electron 壳**，Web GUI 前端不在里面。
- 扩展点在 **profile 目录**，不在 asar —— 这是插件能做的前提。

### 2. 插件目录结构

```
local-bundles\<名>\
   package.json        包声明（含 dsh.client / dsh.bundle）
   index.js            Host 半边（export function apply(){}）
   client.js           Client 半边（window.__ModuleLoader__.load(...)）
   cordis.patch.yml    - insert: [{id, name}]
   icon.svg
   <数据文件>           可选（也可把数据内嵌进 client.js）
```

`package.json` 模板：

```json
{
  "name": "@local/<名>",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "description": "……",
  "icon": "./icon.svg",
  "exports": { ".": "./index.js", "./client": "./client.js", "./package.json": "./package.json" },
  "meta": { "title": "显示名", "description": "……" },
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" },
    "client": {
      "platform": "web",
      "immediately": true,
      "inject": ["@deepseek-ai/dsh-client-ui-conversation"]
    }
  }
}
```

### 3. Client 半边契约（照抄 `local-bundles\whale-peak-offpeak\client.js`）

```js
window.__ModuleLoader__.load({
  id: '@local/<名>',            // 与 package.json 的 name 一致
  factory(require) {
    const React = require('react');
    const h = React.createElement;
    function MyButton() { /* React 组件 */ }
    return {
      inject: ['slots'],
      apply(ctx) {
        ctx.slots.inject('sidebar.footer.action', () =>
          ctx.slots.register(
            { name: 'sidebar.footer.action', id: '<名>', order: 3 },
            MyButton));
      },
    };
  },
});
```

**可用槽位**（实测自 whale 插件注释）：

| 槽位 | 位置 |
|---|---|
| `sidebar.footer.action` | 侧边栏底部、账号上方（kind:list / scope:root，全页面可见） |
| `conversation.input.left` | 输入框左侧工具区（"+" 按钮右边） |
| `conversation.composer.dock` | 输入框下方状态行 |

- `order` 决定同槽内排序（实测：同一槽里 `order` 大的更靠上）。
- `index.js` 可以完全空：`export function apply() {}`（纯展示型插件不需要 Host 资源）。

### 4. 注册四处（缺一不可）

| # | 位置 | 内容 |
|---|---|---|
| 1 | `local-bundles\<名>\` | 插件文件本体 |
| 2 | `profile\package.json` → `dependencies` | `"@local/<名>": "link:./local-bundles/<名>"` |
| 3 | `profile\package.json` → `dsh.profile.bundles` | 追加 `"@local/<名>"` |
| 4 | `profile\cordis.yml` | 末尾追加 `- id: <名>` / `name: '@local/<名>'` |
| 5 | **`profile\node_modules\@local\<名>`** | **符号链接 → `..\..\local-bundles\<名>`** |

> ⚠️ 第 5 项最容易漏。DSH 通过 `node_modules` 解析插件包，
> 没有链接就**加载不到**（而且不一定报错）。
> 建链接：`cmd /c mklink /D "<profile>\node_modules\@local\<名>" "..\..\local-bundles\<名>"`
> （需要管理员权限）

### 5. 数据怎么给 Client

Client 运行在浏览器环境，**不能读本地文件**。三个方案：

| 方案 | 可靠性 | 说明 |
|---|---|---|
| **内嵌进 client.js** | ★★★ | 把数据写成 `const DATA = {...}`；零网络依赖，**推荐** |
| `fetch('./x.json')` | ★ | 基准路径取决于页面 URL，可能 404 |
| `import.meta.url` | ★ | DSH 的 `__ModuleLoader__` 不是标准 ESM，`import.meta` 可能不存在 |

⇒ 本项目的「特技叠加面板」采用**内嵌**方案：
Python 侧扫描 EXE → 生成 `skills.json` → `_生成插件client.py` 把精简数据写进 `client.js`。

### 6. 本机跑 node 的办法

没有独立 node（`runtime\bin\node` 只是 shell 包装脚本）。用 Electron：

```powershell
$env:ELECTRON_RUN_AS_NODE='1'
& '[本地盘]\新建文件夹 (2)\DeepSeek Harness.exe' script.mjs
# => node v24.18.1
```

```bat
:: 1) 生成插件数据（扫描 Ekd5.exe）
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_生成叠加数据.py

:: 2) 把数据内嵌进 client.js
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_生成插件client.py

:: 3) 注册插件（改 profile 配置，自动备份）
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_注册DSH插件.py --name skill-stack-panel --apply

:: 4) 自检（结构 + 槽位注册 + 数据）
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_查JS语法.py
$env:ELECTRON_RUN_AS_NODE='1'
& '[本地盘]\新建文件夹 (2)\DeepSeek Harness.exe' 大鲸鱼产生专用\_插件加载自检.mjs

:: 5) 重启 DSH 生效
大鲸鱼产生专用\_pyrun.cmd 大鲸鱼产生专用\_重启DSH.py
```

## 风险与边界

- **改 profile 配置有风险**：`cordis.yml` 由 DSH 生成维护，手工插入条目虽实测有效，
  但 DSH 升级后可能被覆盖 → 重跑注册脚本即可。注册脚本**每次改动前自动备份**。
- **重启会中断当前会话**：属预期。
- 插件代码出错可能**影响 GUI 加载** ⇒ 改完务必先跑 `_查JS语法.py` 与 `_插件加载自检.mjs`。
- 不要把插件做成"直接写游戏文件"：写 `Ekd5.exe` 必须走写锁流程（游戏进程检查 /
  跨进程锁 / SHA 校验 / 备份 / 复读 / 审计）。插件的职责是**查看 + 决策 + 导出**。

## 证据来源

- 现成样例：`~\.dsh\profiles\desktop\local-bundles\whale-peak-offpeak\`（大鲸鱼峰谷期插件）。
- 进程命令行实测（`Win32_Process`）。
- 自研样例：`local-bundles\skill-stack-panel\`（特技叠加面板），
  自检输出：`__ModuleLoader__.load` 调用 1 次 / id 正确 / `inject:["slots"]` /
  已注册到 `sidebar.footer.action` / 组件返回元素树 / 内嵌 254 条数据解析成功。

## 待验证项

- **P1**：确认插件在 GUI 里出现且位置符合预期（重启后人工确认）。
- **P2**：`order` 与上下位置的精确关系（当前实测：order 大的靠上）。
- **P2**：把更多小工具做成插件（工具箱、叠加方式导出、只读监控等）。
