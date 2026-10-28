# 6.6 自动化测试契约

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/test-contracts/engine-effect-assignment.json`

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
