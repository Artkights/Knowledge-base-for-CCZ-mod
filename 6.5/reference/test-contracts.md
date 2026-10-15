# 6.5 自动化测试契约

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/tests/smoke-test-contracts.json`

## R/S eex 只读烟测

ID: `test.65.smoke-rs-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-smoke`

目标: R/S eex 只读烟测；变更范围: 否

断言：

- 明确验证 RS\R_.eex/S_.eex 索引不混入 E5S，验证 B形象指定器偏移、头像预览和 E5 110 索引表预览

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 旧版完整剧本深度烟测

ID: `test.65.smoke-legacy-scenario-depth-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-scenario-depth-smoke`

目标: 旧版完整剧本深度烟测；变更范围: 否

断言：

- 遍历全部 R/S eex，使用迭代方式统计旧版完整树命令数和最大子事件嵌套深度，防止递归枚举再次引入 StackOverflow

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## R/S eex 核心写入烟测

ID: `test.65.smoke-write`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --write`

目标: R/S eex 核心写入烟测；变更范围: 只写测试副本

断言：

- 当前等价于 R/S 核心写入验证：复制测试副本，写 RS\R_00.eex 文本和 Ekd5.exe 人物 R/S 指定表，备份并复读校验

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## R/S eex 核心写入烟测

ID: `test.65.smoke-rs-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-write-smoke`

目标: R/S eex 核心写入烟测；变更范围: 只写测试副本

断言：

- 与 --write 主线相同，名称更明确；若 S_00.eex 战场标题容量为 0，输出 BATTLEFIELD_TITLE_WRITE_SMOKE_SKIPPED 后继续验证胜败条件、部署、地图和 Hexzmap

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 战场标题/胜败条件写回烟测

ID: `test.65.smoke-rs-text-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-text-write-smoke`

目标: 战场标题/胜败条件写回烟测；变更范围: 只写测试副本

断言：

- 单独验证 S 剧本文本写回；标题容量不足只跳过标题子项，不阻断胜败条件结构保存和复读

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 战场部署写回烟测

ID: `test.65.smoke-rs-deployment-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-deployment-write-smoke`

目标: 战场部署写回烟测；变更范围: 只写测试副本

断言：

- 单独验证 46/47/4B 部署、空槽自动绑定、AI/坐标和单位状态写回

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 独立单关语义命令烟测

ID: `test.65.smoke-standalone-semantic-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --standalone-semantic-smoke`

目标: 独立单关语义命令烟测；变更范围: 否

断言：

- 验证 typed event 编译为真实命令草稿，禁止 turn_start/area_entered 继续用文本标签冒充触发

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 独立单关黄金样例烟测

ID: `test.65.smoke-standalone-golden-samples-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --standalone-golden-samples-smoke`

目标: 独立单关黄金样例烟测；变更范围: 否

断言：

- 固定三英战、救援战、Boss 决战，验证角色识别、R/S 命令图、资源阻断和报告等级

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 严格可玩预览烟测

ID: `test.65.smoke-strict-playable-preview-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --strict-playable-preview-smoke`

目标: 严格可玩预览烟测；变更范围: 否

断言：

- 验证 strict_playable_preview 会因缺资源、结构草稿和 runtime gate 阻止 playable/runtime 等级

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 地图/Hexzmap 一致性烟测

ID: `test.65.smoke-map-terrain-consistency-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --map-terrain-consistency-smoke`

目标: 地图/Hexzmap 一致性烟测；变更范围: 否

断言：

- 校验 Map JPG、Hexzmap 索引、格数、decoded length 和可编辑块一致

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## E5/动态链接库 图片资源目录与条目替换烟测

ID: `test.65.smoke-e5-image-replace-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --e5-image-replace-smoke`

目标: E5/动态链接库 图片资源目录与条目替换烟测；变更范围: 只写测试副本

断言：

- 先复制常见图片 E5 和图标 动态链接库 到测试副本，校验 Face/Pmapobj/Unit_/Hitarea/Effarea/Logo/Mmap/U_select/Gate/Weather 等 E5 资源目录与 Itemicon/Mgcicon/Cmdicon 动态链接库图标编号预览，再生成小 PNG 替换 Unit_mov.e5 单个 110 索引图号，复读条目字节并验证备份/JSON 报告

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 旧版 MFC 对话框 复刻烟测

ID: `test.65.smoke-legacy-mfc-dialog-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-mfc-dialog-smoke`

目标: 旧版 MFC 对话框 复刻烟测；变更范围: 否

断言：

- 从旧 OnEditModify() 解析 101 个命令号到 71 个对话框 的分派，校验 C# 分派表、旧 .rc 资源、71 个显式行为目录、Dialog_114 34 个模板，并逐个实例化旧式对话框 执行初始化/提交

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 战场单位状态写回烟测

ID: `test.65.smoke-battlefield-unit-status-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --battlefield-unit-status-write-smoke`

目标: 战场单位状态写回烟测；变更范围: 只写测试副本

断言：

- 复制 S_00.eex 到测试副本，直接从旧版脚本树构造 46/47 TargetKey，验证等级/兵种级/AI、48 装备、52 兵种改变和 5 条 38 五维写回；断言 48 在部署段，52/38 在同 Section 的 1C 绘图 下方，并校验 4081=1/0 包裹

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 角色默认装备写回烟测

ID: `test.65.smoke-role-default-equipment-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --role-default-equipment-smoke`

目标: 角色默认装备写回烟测；变更范围: 只写测试副本

断言：

- 验证 6.5-0 人物 尾三字节字段 武器/防具/辅助 无未命名 padding；抽样人物 ID 162 读取 46/90/143；角色设定聚合表派生 武器名/防具名/辅助名；测试副本写入 0/70/109 后直接校验 Data.e5 @ 0x18C + id0x20 + 0x1D..0x1F，再恢复原值并复读

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 特效包读写烟测

ID: `test.65.smoke-effect-package-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --effect-package-smoke`

目标: 特效包读写烟测；变更范围: 只写测试副本

断言：

- 验证 EffectPackage 的宝物特效、兵种特效、个人/套装专属和补丁草案入口；覆盖宝物绑定自动发现删除、兵种分配固定清空、个人/套装专属只改指定槽位和删除清空 14 列

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 商店/物品读取烟测

ID: `test.65.smoke-shop-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --shop-smoke`

目标: 商店/物品读取烟测；变更范围: 否

断言：

- 验证商店数据、人物名、物品低/高段、装备/道具下拉、物品详情和 CSV/批量编辑路径；用于确认引擎感知物品表解析没有回退

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 全局数字参数证据护栏

ID: `test.65.smoke-global-numeric-evidence-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-evidence-smoke`

目标: 全局数字参数证据护栏；变更范围: 否

断言：

- 验证旧形象指定器左侧全局数字项当前可写项为 LevelLimit/UpgradeExperience 加 5 个低风险 leaf；AbilityThreshold/EquipmentExp/Merit/PromotionLevelSecond/MiddleEquipmentLevel 继续锁定，父级组合 key 拒绝写入，System.ini 未暴露截图数字项偏移，并确认 CMF smoke 示例地址 0048D3C4 在当前 6.5 基底映射为文本片段而非 等级上限/升级经验

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 全局数字参数静态候选查询

ID: `test.65.smoke-global-numeric-query-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-query-smoke`

目标: 全局数字参数静态候选查询；变更范围: 否

断言：

- 生成 CCZModStudio_Reports\DebugEvidence\global-numeric-query\\global-numeric-query-report.json，断言静态候选查询不会把待验证字段升级为可写；已验证字段必须显式列出官方 diff 写回目标

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 全局数字参数官方 diff 实验准备

ID: `test.65.smoke-global-numeric-discovery-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-discovery-smoke`

目标: 全局数字参数官方 diff 实验准备；变更范围: 只写测试副本

断言：

- 生成普通 before/official_case/official_tool，并生成低风险 noop_case、7 个 leaf case、对应 official_tool_<caseKey> 与 low-risk-experiment-report.json；初始 compare 必须保持 NeedsManualOfficialDiff，不自动晋级字段

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 全局数字参数版本护栏

ID: `test.65.smoke-global-numeric-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-write-smoke`

目标: 全局数字参数版本护栏；变更范围: 只写测试副本

断言：

- 同一入口额外复制标准 6.6 基底，断言所有 6.5 固定偏移项均为“版本锁定”、不暴露目标偏移，preview 拒绝且 Ekd5.exe SHA256 不变

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 能力档位补丁扫描/写回烟测

ID: `test.65.smoke-ability-tier-patch-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --ability-tier-patch-smoke`

目标: 能力档位补丁扫描/写回烟测；变更范围: 只写测试副本

断言：

- 显式扫描本地 6.5 未加密基底 Ekd5.exe 的档位函数、5 个 call site、封顶点和显示表；预览 6 档分支合并与 10 档迁移阻断；在测试副本中写 6 档并复读，再写回 7 档并复读，确认备份和 JSON 报告存在

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 剧本专属/套装文本烟测

ID: `test.65.smoke-exclusive-set-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --exclusive-set-smoke`

目标: 剧本专属/套装文本烟测；变更范围: 否

断言：

- 扫描 R/S eex 的 72 信息传送子功能 10，验证专属/套装文本解析、人物/物品/特效名映射和格式容错

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## E5S 存档/旧探针兼容检查

ID: `test.65.smoke-legacy-e5s-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-e5s-smoke`

目标: E5S 存档/旧探针兼容检查；变更范围: 否

断言：

- 只检查 SV\.E5S 是否存在、B形象指定器 中 CountSV、文本线索和旧命令探针；输出会标注 compat_only_not_rs_script

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。 

## 历史全量探针

ID: `test.65.smoke-legacy-all-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-all-smoke`

目标: 历史全量探针；变更范围: 可能按旧逻辑继续运行

断言：

- 仅用于追溯旧实现，不作为当前主线成功标准；其中仍可能包含未清理的 SV004.E5S 历史断言

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。
