# 6.4 自动化测试契约

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.4/data/test-contracts/data-manager-formulas.json`、`6.4/data/tests/data-manager-contracts.json`

## 6.4 33项公式与88项常量副本回归契约

ID: `test.64.dm-formulas-and-constant-audit`；状态: `candidate`；证据: `source-reviewed`

命令: `dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release -- --battle-formulas "{EXACT_SAMPLE_ROOT}"`

目标: DataManager.Core的公式模型、公式族校验和常量签名/多站点写入；命令在含data管理器/和形象管理器/的匹配源码工作区执行。；变更范围: 前三项测试内部建立临时核心文件副本并在副本修改/复读/回填，finally清理副本；重定位探测只读。构建仅产生bin/obj，不应修改原始游戏样本。

断言：

- 公式条目与Definitions数量一致（本快照33项），公式步骤、证据、名称和引用常量完整。
- 本快照88项常量在此精确样本中58项命中；仅适用且完整签名匹配者允许写入，其余只读。
- 逐项修改、复读、核对原始文件字节再回填；成对字段保持主站点位移，附加站点与主值一致。
- 非法曲线组合返回Error且文件SHA不变；只改命中上限产生Warning并可正常提交、复读。
- 原地址完整命中的非可选签名须恰好1处；可选布局缺失不自动宣称兼容。
- 执行前后源EXE SHA保持相同；本契约不证明游戏内命中/伤害已验收。
- 随后执行：dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --battle-formula-write "{EXACT_SAMPLE_ROOT}"
- 随后执行：dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-audit "{EXACT_SAMPLE_ROOT}"
- 随后执行：dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-relocations "{EXACT_SAMPLE_ROOT}" 6.4

必需产物：

- 固定源码来源SHA与精确样本EXE SHA
- BATTLE_FORMULA_TESTS_OK、BATTLE_FORMULA_WRITE_OK、ENGINE_CONSTANT_AUDIT_OK标记和退出码
- 逐布局exact/relocate/hits日志及源样本不变记录

失败含义：断言失败表示源码模型、实际字段布局、共享约束或事务回读不一致；保留失败日志并保持candidate，不能以旧统计或只读跳过冒充适用项通过。


补充命令：

- dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --battle-formula-write "{EXACT_SAMPLE_ROOT}"
- dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-audit "{EXACT_SAMPLE_ROOT}"
- dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-relocations "{EXACT_SAMPLE_ROOT}" 6.4

本轮执行：

- `date`：2026-11-02
- `sourceVersion`：1.2026.1101.114
- `level`：tool-isolated-copy-and-static-verification
- `runIds`：["6.4-battle-formulas", "6.4-battle-formula-write", "6.4-engine-constant-audit", "6.4-engine-constant-relocations"]
- `exitCodes`：[0, 0, 0, 0]
- `gameRuntimeVerified`：false
## 6.4识别、交换、事务历史和四方向迁移契约

ID: `test.64.data-manager.compatibility`；状态: `canonical`；证据: `source-reviewed`

命令: `dotnet run --project data管理器/src/DataManager.Tests -c Release -- --ccz64-compatibility "<BASE64>" "<BASE65>" "<BASE66>"`

目标: Windows/.NET源工作区中的洗隋9112、6.5及6.6原样基底；测试自动复制核心文件。；变更范围: 只修改系统临时目录的独立基底副本、交换文件和测试历史；结束复核三个原件四核心SHA。

断言：

- 四核心精确识别ccz-6.4/64-xisui-v1；兼容识别不能绕过消费者；目录名不参与判断。
- 名称池恰为180×16只读；R/S、地形和撤退仅在对应消费链通过后出现；策略扩展缺证保持不可用。
- 全部已加载物理表CSV、含数据业务页XLSX原样回导ChangedCells=0，草稿不变；交换元数据保留6.4身份，跨Profile直接导入拒绝。
- 人物/R/S/地形等首末记录跨表保存，仅字段区间改变；磁盘复读正确，保存历史撤回逐字节恢复，重做再撤回成立。
- 6.4到6.5、6.5到6.4、6.4到6.6、6.6到6.4四向迁移按TableKey/ID/字段及目标Codec转换；人物数值、16位R指定、辅助物品实际效果仅改目标字节，源文件不变。
- 只接受冻结的6.4旧LayoutRevision及当前布局；未知修订和6.5/6.6历史身份拒绝。

必需产物：

- CCZ64_EXCHANGE_OK（表数由实际加载结果报告）
- CCZ64_UI_OK seven business pages
- 四条CCZ64_MIGRATION_OK及CCZ64_COMPATIBILITY_TESTS_OK
- 测试前后原件核心SHA比较结果

失败含义：可能是版本识别、消费者、物理布局、元数据/Codec隔离、事务或历史身份错误；不得通过放宽门禁接受。

## 6.4配置消费者、损坏降级与旧历史兼容契约

ID: `test.64.data-manager.configuration-consumers`；状态: `canonical`；证据: `source-reviewed`

命令: `dotnet run --project data管理器/src/DataManager.Tests -c Release -- --ccz64-configuration "<BASE64>"`

目标: 洗隋9112完整消费者及6.4冻结上一版布局；变更范围: 临时副本中改人物首末行、26许可首末行、撤退首末文本和损坏消费者副本；原件只读。

断言：

- RetreatQuotes、PersonDefaults、EquipmentPermissions、SpecialCriticalMap四条完整消费链均匹配合法PE32 x86节及唯一函数。
- 撤退49×200、首末文本与原生ID0..48一致；人物49即使将Data+15改为小数也不得出现专属撤退行。
- 人物首末记录+27级别/+28经验/+29..31默认装备及80×35记录的全部26个许可首末字段可写；新增装备值经原生类型与255规则校验。
- 保存只修改预期字段范围，磁盘复读正确；数据值变化不改变消费链LayoutRevision，撤回和重做逐字节保持。
- 十处损坏消费者只关闭相关能力；重复完整函数、空文件或非法PE拒绝。损坏人物链将+27..31设Preserve，损坏许可链将+9..34设Preserve；普通武力字段继续可用。
- 只对白名单冻结清单重算得到的旧6.4修订开放原位置普通字段CSV/history兼容；旧保留列不能伪装成新装备字段，未知修订拒绝。

必需产物：

- CCZ64_CONFIGURATION_TESTS_OK
- 原始四核心SHA不变断言
- 消费者损坏和重复函数拒绝断言

失败含义：完整链匹配、映射、字段隔离、局部降级或旧历史白名单失效；不能退回单条地址引用或长度放行。

## 6.4逐字段首末记录写回边界矩阵契约

ID: `test.64.data-manager.field-writeback-boundaries`；状态: `canonical`；证据: `source-reviewed`

命令: `dotnet run --project data管理器/src/DataManager.Tests -c Release -- --ccz64-field-writeback "<BASE64>"`

目标: 当前6.4 Profile可编辑字段的首末记录、数值和文本物理边界；变更范围: 游戏数据仅修改系统临时副本；报告写入源工作区data管理器/验证/6.4适配-20261022/字段写回矩阵.csv（会更新已有报告）；原样基底保持只读。

断言：

- 每个受测字段首末记录写后按Codec复读，仅允许字段区间变化。
- 字符串遵循GBK字节预算，保留尾部和未修改字节。
- 只读、保留、未验证和缺失表明确记录跳过或不适用，不能算作通过。
- 失败数必须为0；矩阵覆盖不是所有中间行和所有取值穷举。

必需产物：

- data管理器/验证/6.4适配-20261022/字段写回矩阵.csv
- FIELD_WRITEBACK_MATRIX_REPORT=报告路径
- 通过字段边界/明确未测或不适用/失败计数及原件SHA不变结果

失败含义：字段宽度、编码、边界、能力或事务行为不符；须定位实际失败行，不能用总体通过数量掩盖。
