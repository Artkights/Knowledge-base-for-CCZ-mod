<!-- generated-kb-entry -->
<!-- source: 工具整合包/本地知识库/06-项目与工具链/PL天气补丁迁移与复刻版6.6山贼实现方案.md -->
<!-- version: 6.6 -->
<!-- topic: tools-validation -->
<!-- status: canonical -->
<!-- evidence: local-or-test-evidence -->

# PL 天气补丁迁移与复刻版 6.6 山贼实现方案

## 适用范围与结论

本页针对 `老版游戏制作工具/pl补丁` 到 `基底/复刻版6.6山贼` 的雨雪天气补丁迁移。目标样本身份：`Ekd5.exe` SHA256 `6929FE0DB049935EEC793CE785D431947E48BED406ED94233F9B3A9C6DB4BCB8`；原始 `Koeicda.dll` SHA256 `623ED0D19DFF5F3675C70BDE1CD19E3411BB613E321B4F37058D5FD688052E62`。

结论：旧补丁不能直接覆盖 6.6 的 `Koeicda.dll`。旧 DLL 导出 12 个 `CDAudio*`，当前 6.6 `Ekd5.exe` 静态导入表使用 12 个函数，而目标原始 DLL 完整导出 20 个；必须使用 6.6 原始 DLL 的备份作为转发目标，构建 x86 20 导出兼容代理。

## 旧 PL 补丁静态证据

`老版游戏制作工具/pl补丁` 包含 `koeicda.dll`、`Koeicda_org.dll`、`GearNtKe.dll`、`patch/pl_06.ini`、雨雪各 8 帧 JPG、`0.jpg`、`rain.mp3` 和 `snow.mp3`。雨雪图片及兜底图均为 `1920x1440`、24bpp RGB JPEG。旧 DLL 中确认了 `./patch/rain/*.jpg`、`./patch/snow/*.jpg`、`./patch/0.jpg`、MCI 命令 `open/play/pause`，以及 `EffectWindow`、`EffectMenu`、`STATIC`、`SmallMap` 字符串。

旧 `Koeicda.dll` SHA256：`52E41560903EE81E0685ABDCA9E13EEE6CA4A0322693CEC3E093AEC5EB935AC7`，依赖 MFC/GDI+/WINMM 等运行库，并非只提供原版 CD 音轨转发。旧 `GearNtKe.dll` SHA256：`6037FBF6BA06FB8E2C276C87736A9F98FFE96F0A47C9CC7DD682BFB24F021AC5`，导出 `AddProcess/GetSpeed/OldSetTimer/SetSpeed/UnIntercept`，用途是计时器/速度拦截候选，完整运行时语义未动态确认。

## 6.6 兼容边界

6.6 `Ekd5.exe` 当前静态导入表实际使用 12 个 `CDAudio*` 入口：`Pause/Stop/GetDriveLetter/Resume/GetPlayingPos/IsPlaying/Terminate/Initialize/GetNumDrives/Open/GetNumTracks/PlayTrack`。目标原始 `Koeicda.dll` 导出表完整提供 20 个入口；旧 PL DLL 也只有 12 个。为兼容潜在其它调用者和保持原始 ABI，代理按 20 导出构建；不能把旧 PL DLL 或其 `Koeicda_org.dll` 当作 6.6 原始 DLL。

旧资料中关于把 `0x00C60000` 全局搬到 `0x00D60000` 的经验只适用于其它版本。当前 6.6 `Ekd5.exe` 同时存在 `0x00C60000` 和 `0x00D60000` 常量引用，不能做全局替换；固定地址 Hook 必须先绑定 SHA、原字节和动态现场。

6.6 原生 `E5/Weather.e5` 与 PL 外部 JPG 覆盖层是两个独立资源系统。PL 帧不直接写入 `Weather.e5`。

## 已落地的实现包

本仓库已新增 `工具整合包/PL天气补丁6.6`：

- `patch/`：从旧补丁复制并校验的雨雪帧、音频、兜底图和 74 行 `pl_06.ini`。
- `patch/pl_06.named.ini`：命名配置草案；未动态验证的旧参数保留为行号，不强行解释。
- `pl66.manifest.json`：目标 SHA、20 个必需导出、资源大小/SHA 和状态字段。
- `native/PLWeatherProxy.cpp`、`native/Koeicda.def`、`native/BUILD.txt`：x86 MSVC 代理源码与构建命令。
- `install.ps1`、`uninstall.ps1`：目标版本校验、完整备份、资源复制、安装报告和按清单卸载。
- `GearNtKe.legacy.dll`：旧 DLL 仅作证据归档，不作为 6.6 活跃实现安装。

代理源码当前提供 20 个导出、原始 DLL 转发、GDI+ 叠加窗口、雨帧后台加载、窗口跟随和 MCI 音效生命周期骨架。构建前不替换目标游戏 DLL；`pl66.manifest.json` 中 `proxyBuild/runtimeWeatherProbe/startupTest` 保持 `pending`，直到 x86 构建和实机验证完成。

## 目标实现契约

### 代理 DLL

- 运行目录中的原始 `Koeicda.dll` 先备份为 `Koeicda_original_6.6.dll`。
- 新代理加载该备份并转发全部 20 个导出；缺失导出使用稳定桩，不能让主程序加载失败。
- 编译目标为 PE32 x86，优先 `/MT`，避免 MFC/VC 运行库缺失。
- 不修改 `Ekd5.exe` 导入表，不使用旧 PL 的 `Koeicda_org.dll`。

### 覆盖窗口

- 无边框、分层、透明点击穿透窗口，跟随游戏客户区。
- 图片后台预加载，双缓冲绘制，窗口大小和 DPI 变化时重算缩放。
- 游戏最小化、退出或窗口重建时释放窗口、计时器、线程和 GDI+ 资源。
- 资源路径相对于代理 DLL/manifest 目录，不依赖当前工作目录。

### 天气与音效

- 模式分为关闭、雨、雪、自动；原生天气值和 PL 覆盖状态分开记录。
- 雨/雪切换先停止另一别名，再打开并循环播放目标 MP3。
- 返回菜单、切换战场、关闭天气和进程退出都必须停止并关闭 MCI 别名。
- 原生天气字段和切换函数先做动态探针；在确认前保留手动模式，不启用固定地址 Hook。

### GearNtKe

保留旧导出名只为兼容，实际实现应把速度限制在天气帧计时器，不得改写战斗、AI、菜单或鼠标全局速度。`GearNtKe.legacy.dll` 不应由安装器复制为活跃 DLL。

## 安装与回滚

`install.ps1` 只接受目标 SHA 匹配的 6.6 目录，检查资源完整性和 `native/Koeicda.dll` 是否已构建；安装前将原始 DLL 备份到时间戳目录并保存 `Koeicda_original_6.6.dll`，随后逐项复制 `patch/` 并写入 `pl66.install.json`。失败时应恢复所有已替换文件。

`uninstall.ps1` 只删除 manifest 清单中的 PL 资源，恢复 `Koeicda_original_6.6.dll`，不删除用户其它 `patch` 文件。若备份缺失或目标文件被外部修改，应停止并报告，不静默覆盖。

### 2026-09-15 构建记录

已在 Visual Studio 2022 Community x86 环境以 `/MT` 构建并放入 `工具整合包/PL天气补丁6.6/普罗补丁-小暗6.6版`：`Koeicda.dll` 为 PE32/i386，SHA-256 `994F6D151A99A2B51BC370B2454EDF38844FFAE8E040B508725F02D9F1702170`，导出 20 个 `CDAudio` 函数；`GearNtKe.dll` 为 PE32/i386，SHA-256 `0B1BA61D5259510CC4EDFF8001A1C29328F5E04B4DE2469391E13CA947777758`，导出 5 个兼容接口。代理启动时读取 `patch/pl_06.named.ini`，默认关闭天气；手动 Rain/Snow 模式会加载对应帧和循环音频，Auto 在原生天气探针完成前安全降级为关闭。

### 2026-09-15 加速适配修订

原先的 `GearNtKe.dll` 只有空壳导出，调用 `SetSpeed` 不会改变 6.6 游戏行为。现改为在游戏进程内解析主模块 PE 导入表，仅替换 `KERNEL32!Sleep` 与 `USER32!SetTimer` 的 IAT 项：等待和普通窗口计时器按倍率缩短，PL 覆盖层窗口句柄单独排除，避免天气帧被二次加速。`Koeicda.dll` 工作线程会加载同目录的 `GearNtKe.dll` 并调用 `AddProcess`，结束时调用 `UnIntercept`。

命名配置新增 `[Speed]`：`Enabled=1`、`Factor=2`、`MinFactor=1`、`MaxFactor=8`；运行时 `F6` 在默认倍率和 1 倍间切换，`F7/F8` 调整倍率。此方案不写入固定 6.5 地址，也不修改锻造、特效学习、存档或原生 CD 音频逻辑。已在 6.6 基底启动 5 秒无立即崩溃；完整战斗速度和菜单交互仍需实机长时间验证。

### 启动崩溃修复记录

首版 IAT 代理在 6.6 基底中触发 `0xC0000005`。原因是导入表扫描未验证 RVA/目录边界，遇到 6.6 的导入布局时可能访问无效 thunk。现已加入 DOS/NT 签名、导入目录大小、RVA 范围和 thunk 上限校验；`Sleep`/`SetTimer` 代理只在确认有效条目后写入。修复后的 `Ekd5.exe` 启动烟测可持续运行，未再立即退出。当前基底和发布包已同步修复版 `GearNtKe.dll`（SHA-256 `FD4A223CE766D38B88FCBCD9BA5AC8DAE4A1206A591A11CE6C8067835746B07D`）。

固定字节 `PatchApplyService` 仍用于 EXE 定长补丁；DLL 替换、导出检查和多文件事务必须由 PL 专用安装器负责。

### 边框菜单调整

6.6 `ExtendData.dll` 的 UTF-16 资源中确认存在“特技学习”“锻造大商店”菜单文字。当前基底与发布包已将显示文字替换为“超级加速”“加速设置”，并在基底保留 `ExtendData.dll.beforePLSpeed` 备份。倍率实际控制由 `GearNtKe.dll` 的 F6/F7/F8 热键完成；菜单命令回调尚未完成动态确认，因此应使用热键控制，避免点击位置触发未适配的旧扩展逻辑。

## 验收矩阵

静态：20 导入/导出一致、x86 PE、资源尺寸和 SHA、MP3 可解码、无未提供运行库依赖。启动：原版与代理版均可启动，原生 CD 音频可播放/暂停/恢复/停止。运行：普通/雨/雪、雨雪切换、关闭、菜单、战场切换、窗口化/全屏、DPI、Alt+Tab、窗口尺寸变化。稳定性：30 分钟运行、100 次快速切换、退出后无线程/计时器/MCI/GDI 泄漏。回滚：安装中断恢复原 SHA，外部修改时卸载拒绝覆盖。

## 证据等级与待验证项

已证实：文件清单、SHA、图片规格、MCI 字符串、旧 DLL 导出差异、6.6 导入函数清单。静态部分证据：`EffectWindow/EffectMenu` 的实际消息和窗口生命周期、`GearNtKe` 的完整 Hook 语义、`pl_06.ini` 74 行字段含义。待验证：6.6 原生天气值读取、自动模式映射、覆盖层菜单交互、全屏/DPI 行为、代理与原生 CD 音轨并存。

## 关联页面

- `01-核心引擎/复刻版6.6山贼特效与扩展接口.md`
- `09-版本与外部资料/复刻版6.6山贼基底身份与静态分析总览.md`
- `06-项目与工具链/旧扳手调试器源码对照.md`
- `07-数据表与资源/图片处理-E5资源.md`
- `90-来源归档/散落资料整合索引.md`
- `CCZModStudio/Assets/Package/RootDocs/普罗工具整合包使用说明.md`

## 版本与证据边界

- 本条目由发布整理流程归档。
- 具体结论必须结合上方版本、状态和证据等级使用。

## 结论速览

- 本条目整理了当前版本可检索的主题结论；具体使用前必须结合证据等级。

## 适用版本

- 以本目录版本入口和条目元数据为准，不能直接套用到其它版本。

## 已确认事实

- 正文中的确定性结论来自原始知识库整理；仍需以来源索引和纠错台账复核。

## 实现/使用方法

- 先阅读本条目的主体内容，再按版本入口、证据等级和来源索引执行。

## 风险与边界

- 未经目标版本样本、复读、烟测或实机验证的内容，不得作为默认写回依据。

## 证据来源

- 原始来源、哈希和处理状态见根目录 `90-来源归档/source-manifest.csv`。

## 待验证项

- 后续验证应补充目标版本样本、结构复读、烟测或实机证据。
