# 6.6 自动化测试契约

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/test-contracts/data-manager-formulas.json`、`6.6/data/test-contracts/engine-effect-assignment.json`

## 6.6 33项公式与88项常量副本回归契约

ID: `test.66.dm-formulas-and-constant-audit`；状态: `candidate`；证据: `source-reviewed`

命令: `dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release -- --battle-formulas "{EXACT_SAMPLE_ROOT}"`

目标: DataManager.Core的公式模型、公式族校验和常量签名/多站点写入；命令在含data管理器/和形象管理器/的匹配源码工作区执行。；变更范围: 前三项测试内部建立临时核心文件副本并在副本修改/复读/回填，finally清理副本；重定位探测只读。构建仅产生bin/obj，不应修改原始游戏样本。

断言：

- 公式条目与Definitions数量一致（本快照33项），公式步骤、证据、名称和引用常量完整。
- 本快照88项常量在此精确样本中80项命中；仅适用且完整签名匹配者允许写入，其余只读。
- 逐项修改、复读、核对原始文件字节再回填；成对字段保持主站点位移，附加站点与主值一致。
- 非法曲线组合返回Error且文件SHA不变；只改命中上限产生Warning并可正常提交、复读。
- 原地址完整命中的非可选签名须恰好1处；可选布局缺失不自动宣称兼容。
- 执行前后源EXE SHA保持相同；本契约不证明游戏内命中/伤害已验收。
- 随后执行：dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --battle-formula-write "{EXACT_SAMPLE_ROOT}"
- 随后执行：dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-audit "{EXACT_SAMPLE_ROOT}"
- 随后执行：dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-relocations "{EXACT_SAMPLE_ROOT}" 6.6

必需产物：

- 固定源码来源SHA与精确样本EXE SHA
- BATTLE_FORMULA_TESTS_OK、BATTLE_FORMULA_WRITE_OK、ENGINE_CONSTANT_AUDIT_OK标记和退出码
- 逐布局exact/relocate/hits日志及源样本不变记录

失败含义：断言失败表示源码模型、实际字段布局、共享约束或事务回读不一致；保留失败日志并保持candidate，不能以旧统计或只读跳过冒充适用项通过。


补充命令：

- dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --battle-formula-write "{EXACT_SAMPLE_ROOT}"
- dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-audit "{EXACT_SAMPLE_ROOT}"
- dotnet run --project "data管理器/src/DataManager.Tests/DataManager.Tests.csproj" --configuration Release --no-build -- --engine-constant-relocations "{EXACT_SAMPLE_ROOT}" 6.6

本轮执行：

- `date`：2026-11-02
- `sourceVersion`：1.2026.1101.114
- `level`：tool-isolated-copy-and-static-verification
- `runIds`：["6.6-battle-formulas", "6.6-battle-formula-write", "6.6-engine-constant-audit", "6.6-engine-constant-relocations"]
- `exitCodes`：[0, 0, 0, 0]
- `gameRuntimeVerified`：false
## 三子页特效分配与复合绑定回归

ID: `test.66.engine-effect-assignment-regression`；状态: `canonical`；证据: `sample-verified`

命令: `dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj -c Release -- --engine-effect-native <workspace> && dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj -c Release -- --engine-effect-contracts <sample> && dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj -c Release -- --engine-effect-assignments <sample>`

目标: DataManager.Core/App引擎扫描、分配池、原生适配器与统一事务；变更范围: 只修改临时复制工程；真实基底SHA必须保持不变

断言：

- 装备16的37号共享关系可同时表现HP与回合恢复消费者
- HP/MP同号共存、单独卸下255、重扫保持另一能力
- 00413009不作为四参数分配项
- 兵种槽按*2→*1→*0且满槽二选一替换或取消
- 同一调用地址不同表索引不覆盖草稿
- 变长PE专用节写入失败与历史撤回恢复原长度
- NativeEffectAdapter四样本装卸逐字节恢复且FF守卫可复读
- 详情卸下255与分配页原生HP联合事务共享唯一FF守卫载荷，写后语义复读及撤回原SHA/长度
- 普通偶数类型的非FF selector不构成已分配归属；消耗品不在装备共享组
- 四参数入口排除413009后的路径/守卫/DNF等差异只来自该聚合器，通过独立CFG贡献审计
- 未知兵种布局不显示虚假*0，并展示实际只读诊断

必需产物：

- 静态复核-ABI与活动表.json
- 临时工程写前/写后SHA与历史记录
- 1280x720与1920x1080分配页截图

失败含义：任一断言失败表示当前样本的扫描契约、布局验证、绑定关系或事务回滚不满足写回门禁，必须保持只读并检查报告。
