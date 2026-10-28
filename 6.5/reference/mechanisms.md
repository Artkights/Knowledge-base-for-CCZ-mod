# 6.5 机制与调用链

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/mechanisms/consumable-effects.json`、`6.5/data/mechanisms/engine-assignment-field-policy.json`、`6.5/data/mechanisms/engine-mechanisms.json`、`6.5/data/mechanisms/engine-physical-binding-groups.json`、`6.5/data/mechanisms/engine-scan-lifecycle.json`、`6.5/data/mechanisms/engine-scan-operand-provenance.json`、`6.5/data/mechanisms/engine-scan-performance-equivalence.json`、`6.5/data/mechanisms/reviewed-stub-scanner-reference.json`

## 消耗品独立特效目录 0x1A–0x3D 与证据分层

ID: `mechanism.shared.consumable-effect-namespace`；状态: `candidate`；证据: `editor-source-reviewed-user-labels-and-sample-supported-inference`


写入策略：

允许作为编辑器目录显示、人工检索和候选语义提示；禁止仅凭目录标签或源码Confirmed标记自动写入游戏特效号、参数或补丁。人工物理编辑仍需目标Profile/Codec、字段范围、原始字节保留、差异白名单和保存后复读门禁；新增游戏语义应先补目标消费者或运行时证据。

## 特效字段可写性、共享N与255命名空间

ID: `mechanism.shared.effect-assignment-field-and-selector-contract`；状态: `canonical`；证据: `static-verified`

同一数值255在物品槽、装备selector、个人selector、兵种槽中有不同契约；字段布局、玩法语义和工具支持状态分别管理。


计算规则：

- `9112洗隋是180x8，3890是255x8，25D及F20C已验证6.6是255x16；F9A的3加1结构保留其独立画像。`
- `8字节行只有1个兵种槽，整行共享N；16字节行2个兵种槽、每个人物与兵种槽各自N。`
- `已证明的物理字段可按宽度/边界/原字节直接编辑；未命名效果、没有消费者或管理器尚未实现分配，不等于字段不存在或不可写。`
- `代码参数编辑仍须唯一来源、完整指令边界、ABI、影响范围和冲突证明；字段可写不能绕过这些条件。`
- `兵种槽FF为空；槽ID80..254异常占用保留。物品装备位FF代表未装备，与装备记录的effect字段FF不同。`
- `原始装备匹配器直接比较低字节；只有已安装并复读通过的装备子通道FF守卫才能保证selectorFF未分配，且必须保留个人结果与聚合。`
- `个人selectorFF不能自动禁用；8字节读取器没有通用FF短路，64有效范围0..179、65为0..254。`
- `HP/MP原生能力绑定、四参数消费者绑定、人物/兵种活动表、专属/套装表应分别建模，通过共享selector及触发条件展示复合效果。`
- `代码改绑以物理定义字段组为权限与冲突单位；同组全部别名联动。已知装备号但字段未定位者单列；装备号也未知者不算已迁移，不封锁独立已定位字段。`

写入策略：

先读取物理布局和当前原字节，再建立草稿及影响清单；共享N写入需展示整行全部受影响对象；已经定位的N等UInt8数值字段0..255不能因工具目前仅开放部分命名效果而被错误拒绝；selector和行ID仍遵守各自合法范围。

## 物理攻击范围到目标消费调用链

ID: `mechanism.65.physical-attack-targeting`；状态: `canonical`；证据: `static-verified`

1. `fn.65.attack-entry`：物理攻击入口
2. `fn.65.attack-selector`：准备中心坐标和 packed range
3. `fn.65.attack-dispatch`：按范围 ID/段分派
4. `fn.65.attack-geometry`：展开相对坐标
5. `fn.65.map-unit-lookup`：坐标转单位
6. `fn.65.attack-append-target`：过滤并追加目标
7. `fn.65.target-consumer`：消费目标并写伤害/效果

穿透分支：`fn.65.pierce-loader` -> `fn.65.combat-context-init` -> `fn.65.pierce-expand-wrapper` -> `fn.65.pierce-geometry-dispatch` -> `fn.65.pierce-append-target` -> `fn.65.target-consumer`

## ID、战术单位和运行时记录转换链

ID: `mechanism.65.id-pointer-conversion`；状态: `canonical`；证据: `static-verified`

1. `fn.65.battlefield-id-to-tactical-unit`：战场 ID 到 0x30 记录
2. `fn.65.tactical-unit-to-runtime-character`：战术记录到 0x48 人物记录

## 物理定义字段绑定组与跨效果别名联动

ID: `mechanism.shared.physical-field-binding-groups`；状态: `canonical`；证据: `sample-verified`

装备改绑按已证明的物理定义字段分组；多个效果与循环/包装实例引用同一字段时一起转移。已解析装备号而字段未定位者单列；装备号也未知者不算已迁移，已定位组仍可写。


计算规则：

- `以当前EXE及原字节为证据，按操作数文件偏移与宽度分组；组内保存完整调用实例身份、别名效果号和所有已定位消费者。`
- `循环/表/包装/Nested展开本身不构成禁写理由；仅当实际定义唯一、写计划及原指令宽度已证明时开放该物理字段。`
- `一个效果号可能有多个独立物理绑定组；同一物理组也可能覆盖多个效果号。宝物池按组展示，兵种活动行只保留一个规范实例。`
- `分配、转移或卸下一个组时同步全部别名草稿，预览所有共享消费者与宝物；同一字段提出不同目标时拒绝提交。`
- `已解析装备匹配号而字段未定位的消费者可单列位置及原因；装备号也未知者不算已迁移。部分消费者夹具只证明另一未知消费者不封锁已定位组，不证明未知行一定可见。`
- `卸下后的FF源字段保留在目录中，安装并复读装备子通道守卫后仍可再次分配；不得把个人selector改成255。`
- `自动分号保留所有已知只读消费者占用的装备selector，避免新宝物误接入既有效果。`
- `所有消费者都参与物理来源危险共享检测，包括只读或未解析参数保留的定义链；来源跨装备/个人/模式等不同参数角色时阻断改写，只有装备角色内部共享可按组联动。`
- `完整MOV EAX,imm32已经定义全部32位，无须先XOR；宽度API按字节比较4。只有完整32位XOR/SUB同寄存器清零证明高位，AX/AL或混合部分寄存器清零不能冒充。`

边界：

- 观测组ID只属于指定精确样本，不能用偏移或别名数量识别其他构建。
- 隔离副本测试证明字段联动和写回边界，不证明战斗中的玩法结算。

写入策略：

只对实际已定位组声明转移范围；同步别名、检测字节重叠及不同目标，统一备份事务后重新扫描并复读全部组成员。

## 引擎扫描代次隔离与分层内容指纹缓存

ID: `mechanism.shared.engine-scan-lifecycle-and-fingerprint`；状态: `canonical`；证据: `sample-verified`

扫描报告、说明与分配目录按各自内容指纹复用；后台结果另受项目与扫描代次约束，取消或切项目后的旧成功和异常均不能覆盖当前状态。


计算规则：

- `相同EXE与说明内容SHA切换子页复用同一报告和分配目录。缓存命中不能仅依赖路径、长度或mtime。`
- `取消后允许立即启动新代次；即使项目根目录与SHA相同，旧代次的晚到成功或异常仍被忽略。`
- `切项目使旧成功和异常失效；控件关闭与切项目在真实Application.Run消息循环及非法跨线程检查下验证。`
- `EXE同mtime而内容变化使完整结构报告失效；恢复旧SHA可复用已缓存的旧报告。`
- `Imsg同mtime内容变化只刷新说明：worker、FunctionRoles、IndirectCalls、Wrappers结构集合保留同一引用；恢复SHA重用原报告。`
- `Data低位与Star高位物品的内存草稿或同mtime外部编辑使分配目录失效；同一引擎结构报告继续复用。`

边界：

- 该机制说明管理器缓存和异步生命周期，不是游戏引擎的运行时效果缓存。
- 11项结果使用临时副本，四个真实核心源文件SHA保持不变。
- Name来自EXE名称槽；Imsg刷新只替换Description及说明槽元数据，不刷新名称。

## 引擎扫描守卫操作数来源与跨块调用写回判定

ID: `mechanism.65.engine-scan-operand-provenance`；状态: `canonical`；证据: `static-verified`

守卫分支、参数来源、运行时行为分别记录。最短路径可用于说明一条可达路径，不能替代所有路径或将未定=0宣称为完全证明。


计算规则：

- `先按真实跳转目标拆分基本块，防止重叠解码将目标吞入前块。`
- `块内从后向前找最后一次定义；支持mov/movzx/lea/add/sub/and/or/xor/imul。`
- `找不到时向至多4个前驱追溯，深度3，visited防环；定义不一致降级为未定。`
- `被调函数写EAX标记调用返回值；确定写ECX/EDX标记调用写回。`
- `含嵌套call或超过解码上限时只标记可能被写，不能冒充确定返回值。`

边界：

- 上述历史调用数包含00413009，后续ABI纠正后四参数计数为97/181/199，不可混用作当前基线。
- 6.6仍有一条对象字段链未见基址定义；三样本各有两条调用后寄存器可能写回尾部。
- Capstone独立复核证明指令字节与解码一致，不等于运行时效果已验证。
- 后续多路径DNF/决策点/循环重复求值应保留，不能回退为最多12条最短路径。

写入策略：

只将唯一可写参数来源开放写入；共享/多定义或未知内存保留诊断。

## 三基底扫描上下文缓存与完整输出等价

ID: `mechanism.shared.engine-scan-context-cache-equivalence`；状态: `canonical`；证据: `sample-verified`

指定性能快照对国庆F20C、6.5的3890、洗隋6.4的9112执行相同扫描，摘要各统计3轮；完整报告逐字节相同，冷扫中位数分别降低68.91%、79.48%、82.82%。另保留36D8的3轮与2.2.0的单轮附加对照。


计算规则：

- `同一次扫描复用PE、指令、函数、跳转与调用图上下文；减少重复分析和中间分配，不减少结果字段或条件枚举。`
- `先固定每轮EXE SHA和实现源快照；以完整报告文件SHA及逐字节比较证明本次样本的输出一致。`
- `计量以summary.json声明的3轮摘要为准；原始metrics额外保留初始optimized轮，不能把所有行重新混算成同一中位数。`

边界：

- 洗隋91121D4B与刘备副本36D8010F分别统计，不能交换画像；核心三基底为F20C/3890/9112。
- 只证明保存报告对应输入和实现快照的输出等价，不代表游戏动态行为或所有未来样本。
- 耗时受环境和进程状态影响；摘要不是跨机器保证。baseline/optimized的源快照和样本身份必须保留。
- 加强版2.2.0仅1轮对照，不纳入三基底n3结论。
- 共用服务、字段组写回和界面生命周期分别引用独立完成日志；性能输出等价不能代替这些事务与交互结论。

## 6.5pl参考桩扫描器的覆盖与反例

ID: `mechanism.65pl.reference-scanner-coverage-and-counterexamples`；状态: `candidate`；证据: `source-reviewed`

参考实现只提供候选扫描思路，不复制源码，不授权自动写入；目标地址由用户画像配置。


计算规则：

- `覆盖标准四push、包装、mov al动态、参数化与参数循环桩，并保留调用VA/目标/push位置。`
- `push imm8的selector按已确认低字节契约还原，模式与寄存器契约不能全局截断。`
- `_parse对3push及多push仅作模板解释，不证明被调读取数目、顺序和含义。`
- `_moval_nums实际收集同函数push eax之前的mov al；不能证明候选来自同一执行分支，注释所述中途call限制未完整落实。`
- `arg_stub_range将起始imm32与局部cmp上限拼合，未证明二者属于同一循环及实际参数链。`
- `新扫描器应以CFG、定义来源、完整实例身份和被调ABI补足证据；将旧形态用作覆盖清单与反例测试。`

边界：

- 原文只记录一个6.5pl分析样本，不提供当前国庆F20C的装备分类表、地址或ABI。
- 调用者与返回消费者共同决定语义；413009虽被核心调用，但不是四参数入口。
- 参考仓库采用非商业许可；本知识条目只归纳算法事实和限制，不引入参考代码。
