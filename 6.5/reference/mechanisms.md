# 6.5 机制与调用链

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/mechanisms/attack-range-consumption.json`、`6.5/data/mechanisms/consumable-effects.json`、`6.5/data/mechanisms/data-manager-current-contracts.json`、`6.5/data/mechanisms/data-manager-formulas.json`、`6.5/data/mechanisms/data-manager-strategy-semantics.json`、`6.5/data/mechanisms/effect-range-binding.json`、`6.5/data/mechanisms/engine-ability-display-table.json`、`6.5/data/mechanisms/engine-ai-and-terrain.json`、`6.5/data/mechanisms/engine-ai-branch-2-13-15.json`、`6.5/data/mechanisms/engine-ai-branch-346-scoring.json`、`6.5/data/mechanisms/engine-ai-branch-712-scoring.json`、`6.5/data/mechanisms/engine-ai-cross-base-audit.json`、`6.5/data/mechanisms/engine-ai-damage-scoring.json`、`6.5/data/mechanisms/engine-ai-handler-constants-66.json`、`6.5/data/mechanisms/engine-anchor-relocation-66.json`、`6.5/data/mechanisms/engine-api-name-table.json`、`6.5/data/mechanisms/engine-arithmetic-immediates-census.json`、`6.5/data/mechanisms/engine-armor-exp-cross-base.json`、`6.5/data/mechanisms/engine-assignment-field-policy.json`、`6.5/data/mechanisms/engine-auto-battle-flags.json`、`6.5/data/mechanisms/engine-avi-player.json`、`6.5/data/mechanisms/engine-battle-mode-byte.json`、`6.5/data/mechanisms/engine-battle-script-actions.json`、`6.5/data/mechanisms/engine-battle-unit-table.json`、`6.5/data/mechanisms/engine-battle-viewport-context.json`、`6.5/data/mechanisms/engine-capacity-and-sentinels.json`、`6.5/data/mechanisms/engine-cell-byte-map.json`、`6.5/data/mechanisms/engine-cell-flag-writer.json`、`6.5/data/mechanisms/engine-char-exp-cross-base.json`、`6.5/data/mechanisms/engine-character-accessors.json`、`6.5/data/mechanisms/engine-character-adaptation-table.json`、`6.5/data/mechanisms/engine-color-palette.json`、`6.5/data/mechanisms/engine-crit-combo-mode.json`、`6.5/data/mechanisms/engine-cross-base-audit-late.json`、`6.5/data/mechanisms/engine-current-record-pointer.json`、`6.5/data/mechanisms/engine-damage-apply-mode.json`、`6.5/data/mechanisms/engine-dialog-framework.json`、`6.5/data/mechanisms/engine-dialog-workarea-4fff68.json`、`6.5/data/mechanisms/engine-dialog332-confirm.json`、`6.5/data/mechanisms/engine-dialog332-refresh.json`、`6.5/data/mechanisms/engine-embedded-byte-tables.json`、`6.5/data/mechanisms/engine-equipment-growth.json`、`6.5/data/mechanisms/engine-equipment-slot-bound.json`、`6.5/data/mechanisms/engine-font-name-table.json`、`6.5/data/mechanisms/engine-formula-site-audit.json`、`6.5/data/mechanisms/engine-general-constants.json`、`6.5/data/mechanisms/engine-general-coverage.json`、`6.5/data/mechanisms/engine-global-mode-flags.json`、`6.5/data/mechanisms/engine-global-ui-state-block.json`、`6.5/data/mechanisms/engine-grid-bound-correction.json`、`6.5/data/mechanisms/engine-grid-dimension-pair.json`、`6.5/data/mechanisms/engine-history-intel-341.json`、`6.5/data/mechanisms/engine-hit-height-modifier.json`、`6.5/data/mechanisms/engine-hit-retry-cross-base.json`、`6.5/data/mechanisms/engine-item-effect-code-and-range-table.json`、`6.5/data/mechanisms/engine-item-loader-64-parser.json`、`6.5/data/mechanisms/engine-item-price-boundary.json`、`6.5/data/mechanisms/engine-item-record-fields.json`、`6.5/data/mechanisms/engine-item-record-normalization.json`、`6.5/data/mechanisms/engine-item-record-table.json`、`6.5/data/mechanisms/engine-item-type-action-mapping-66.json`、`6.5/data/mechanisms/engine-item-type-classification.json`、`6.5/data/mechanisms/engine-job-attribute-matrix.json`、`6.5/data/mechanisms/engine-job-penetration.json`、`6.5/data/mechanisms/engine-layer-block-constants.json`、`6.5/data/mechanisms/engine-layer-buffer-11.json`、`6.5/data/mechanisms/engine-level-context-struct.json`、`6.5/data/mechanisms/engine-mechanisms.json`、`6.5/data/mechanisms/engine-memory-arenas.json`、`6.5/data/mechanisms/engine-merit-table.json`、`6.5/data/mechanisms/engine-money-global.json`、`6.5/data/mechanisms/engine-movement-terrain.json`、`6.5/data/mechanisms/engine-new-anchors-batch-66.json`、`6.5/data/mechanisms/engine-payment-chain.json`、`6.5/data/mechanisms/engine-personal-exp-cross-base.json`、`6.5/data/mechanisms/engine-physical-binding-groups.json`、`6.5/data/mechanisms/engine-physical-damage-chain.json`、`6.5/data/mechanisms/engine-physical-level-table.json`、`6.5/data/mechanisms/engine-physical-range-correction.json`、`6.5/data/mechanisms/engine-quick-window-host.json`、`6.5/data/mechanisms/engine-random-variant-table.json`、`6.5/data/mechanisms/engine-save-file-format.json`、`6.5/data/mechanisms/engine-save-load-constants.json`、`6.5/data/mechanisms/engine-scan-lifecycle.json`、`6.5/data/mechanisms/engine-scan-operand-provenance.json`、`6.5/data/mechanisms/engine-scan-performance-equivalence.json`、`6.5/data/mechanisms/engine-script-context-caches.json`、`6.5/data/mechanisms/engine-script-handler-capacity.json`、`6.5/data/mechanisms/engine-script-number-parser.json`、`6.5/data/mechanisms/engine-script-opcodes-7c-7d.json`、`6.5/data/mechanisms/engine-settings-block-fields.json`、`6.5/data/mechanisms/engine-settings-dialog-kankyou.json`、`6.5/data/mechanisms/engine-shop-growth.json`、`6.5/data/mechanisms/engine-slot-type-candidate.json`、`6.5/data/mechanisms/engine-sound-settings.json`、`6.5/data/mechanisms/engine-strategy-direction-weather.json`、`6.5/data/mechanisms/engine-table-506800.json`、`6.5/data/mechanisms/engine-target-direction-score.json`、`6.5/data/mechanisms/engine-temp-attribute-block.json`、`6.5/data/mechanisms/engine-text-buffers-save-header.json`、`6.5/data/mechanisms/engine-training-ground-context.json`、`6.5/data/mechanisms/engine-turn-weather-state.json`、`6.5/data/mechanisms/engine-unit-alloc-records.json`、`6.5/data/mechanisms/engine-unit-slot-arrays.json`、`6.5/data/mechanisms/engine-unit-status-bitfield.json`、`6.5/data/mechanisms/engine-weapon-exp-cross-base.json`、`6.5/data/mechanisms/param-display-name-resolution.json`、`6.5/data/mechanisms/public-reverse-analysis-methods.json`、`6.5/data/mechanisms/reviewed-stub-scanner-reference.json`、`6.5/data/mechanisms/script-command-dispatch.json`、`6.5/data/mechanisms/script-execution.json`、`6.5/data/mechanisms/script-jump-window.json`、`6.5/data/mechanisms/script-main-loop.json`、`6.5/data/mechanisms/script-short-param.json`、`6.5/data/mechanisms/strategy-and-range-chains.json`、`6.5/data/mechanisms/strategy-attribute-tables.json`、`6.5/data/mechanisms/strategy-damage-hit-resolution.json`

## 范围落格与格状态/槽号分层写入

ID: `mechanism.65.attack-range-grid-write.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.attack-append-target`：0x437AFF：边界检查后落格
2. `fn.65.cell-slot-reader.3890`：0x435884：读 P 层返回格内单位槽号

## 必杀范围 +0xC/+0xD 的真实消费链

ID: `mechanism.65.fatal-range-consumption.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.data-table-init-root.3890`：0x41B639 初始化总入口
2. `fn.65.data-e5-block1-init.3890`：同属初始化序列；块 5 由 0x41B834 处理
3. `global.65.fatal-record-table.3890`：0x4A7510 保存 97×16 必杀记录
4. `fn.65.fatal-field-d-reader.3890`：0x484E27 读取 +0xD 作为可用性判定
5. `fn.65.fatal-field-c-reader.3890`：0x43F8C0 读取 +0xC 进入特殊目标判定
6. `fn.65.pierce-loader`：0x40782D 在 [0x500E9A]==2 时经 0x41E918 取必杀记录

## 消耗品独立特效目录 0x1A–0x3D 与证据分层

ID: `mechanism.shared.consumable-effect-namespace`；状态: `candidate`；证据: `editor-source-reviewed-user-labels-and-sample-supported-inference`


写入策略：

允许作为编辑器目录显示、人工检索和候选语义提示；禁止仅凭目录标签或源码Confirmed标记自动写入游戏特效号、参数或补丁。人工物理编辑仍需目标Profile/Codec、字段范围、原始字节保留、差异白名单和保存后复读门禁；新增游戏语义应先补目标消费者或运行时证据。

## 文本物理槽宽、严格GBK有效载荷与原槽尾部保护

ID: `mechanism.shared.data-manager-text-payload-budget`；状态: `canonical`；证据: `source-reviewed-current-implementation`

磁盘槽宽、允许修改的文本载荷和运行时消费者证据是三个独立量。当前管理器采用严格GBK/CP936字节预算；原值未改保留整个槽，主动修改才校验编码、容量、NUL和隐藏尾部。


文本字节预算：

| 表 | 物理槽宽 | 最大载荷 | 必须终止符 | 说明 |
|---|---:|---:|---|---|
| persons | 13 | 12 | True |  |
| strategies | 11 | 10 | True |  |
| items-low, items-high, items-extended | [15, 17] | 14 | True | 15/17为物理名称槽宽；当前物品初始化消费者使运行时名称第15字节为NUL，不能据物理宽度允许输入15/17字节。 |
| job-series, detailed-jobs | 9 | 8 | True |  |
| finishing-moves | 11 | 10 | True |  |
| forge | 30 | 29 | True |  |
| effect-names, item-effect-names-66 | 16 | 15 | True |  |
| Imsg.e5中的200字节文本字段 | 200 | 200 | False | 读取缓冲区另附NUL；满200个GBK字节可合法保存，不能统一减成199。 |

写入策略：

仅给当前已定位且允许编辑的字段提供文本预算，不改变ReadOnly/Preserve/Unavailable或授予未知区域写入能力。

原槽保护：

- 找到首个NUL后，从下一字节寻找首个非零保留字节i；当前可增长预算至多i-1，保留终止符及尾部。
- 新值不能用GBK表示或含嵌入NUL时拒绝，不能静默截断或以问号代写；GBK不可用不回退UTF-8。
- 原无效字节以私用占位区分于真实问号并记录警告；未改字段仍保存原槽，改该文本时要求替换不可编码占位。
- CR、LF、尾空格和控制码按原字节保留并计入预算；不会TrimEnd或统一换行。
- 旧超预算名称不因打开、相同CSV回导或保存其他字段被清洗；未知窄槽始终以其真实槽宽收窄预算。

消费者证据边界：

- `verifiedExecutableSha256`：["3890CC3247163D30CD0A2F3412E06A83E7270AA9324B6E358D84EFAED07DC08C", "34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA", "A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282"]
- `unknown`：当前EXE完整指纹不匹配时，即使局部消费者签名相同仍标保守策略；6.4及其他改版不能继承这三份EXE的完整运行时证据。
- `conservativeNames`：必杀与锻造的10/29字节是当前保守保存策略，实际字符串消费者尚未完整核定。

## 拓展初始表、个人活动表与EXS恢复的证据边界

ID: `mechanism.shared.data-manager-extension-runtime-boundary`；状态: `canonical`；证据: `source-reviewed-current-implementation`

Effect、Effectmsg、MeffStudy、Forge的物理记录解析、管理器编辑能力和目标游戏消费者分别判断；文件存在或临时副本写后可复读，均不能证明该引擎已启用拓展功能。EXS可能恢复运行时状态，修改初始e5不保证覆盖旧档。


解析与编辑规则：

- 按当前文件的完整记录数及容量上限加载，不因打开/保存自动扩容；截断、超容量、缺文件只关闭受影响分类。
- 根目录Item.e5是可选数据来源；E5/Item.e5是图标档案，不能因同名读取为扩展数据。
- Effect.e5每人物256个四字节槽，活动表每特效行按人物/兵种匹配；二者索引方向不同，不能把扩展槽存在当成该EXE已执行扩展读取链。
- 扩展Effect槽ID255是该扩展协议的空槽/结束项，回合255是永久；这个空值契约不能移植为原生活动表个人selector255。
- Effect已有槽只改ID/值时保留经验和回合；新填空槽默认经验0、回合255；主动清空写FF 00 00 FF，整理移动完整四字节并保留顺序与重复。
- MeffStudy查询可能扫描全部32槽，但扣次/关末清理可能首空停止；次数255无限，清空FF 00，整理需显式操作。
- Effectmsg成长ID255保留只读；允许成长按非零判断，原2/255不自动归一成1。
- 锻造物品ID低字节255为空；已有255/511/65535等原编码未修改时保留。
- 迁移/CSV创建物理文件不注入消费者或替换扩展DLL；6.4继承几何不构成独立消费者证据。

运行时边界：

要证明玩法已生效，须另有精确样本、插件/加载器及消费者证据和相应游戏运行验收；本实体只确认当前离线管理器的处理与限制。

## 6.5 公式与常量读取、签名重定位及同值字段契约

ID: `mechanism.65.dm-formula-constant-contract`；状态: `candidate`；证据: `source-reviewed`

当前源码定义33项公式和88项常量；本精确样本实读71项常量，其余17项按适用基底/签名保持只读。历史文档24、86、87项为阶段性计数。


计算规则：

- `先按当前Profile版本选择可用布局；固定地址必须使用目标PE的ImageBase、节RVA和RawPointer映射，不将VA减0x400C00推广为通用公式。`
- `有RelativePointerVa时先映射并读取DWORD指针，再加RelativeOffset；随后对主字段、成对与附加字段逐个核对签名及值。`
- `先尝试表指针相对位置与所有精确布局；仅显式Relocate且唯一签名命中时允许重定位。代码字段在可执行节扫描，表值槽按已声明数据范围处理。`
- `PrefixMask/SuffixMask的0字节是通配，非0按原值比较；call相对位移可掩码忽略，不以其字节偶然一致证明兼容。`
- `成对/附加站点从主命中地址与原始相对差推导，禁止独立漂移到别的函数；每处签名必须满足，同值必须一致。`
- `一批相同常量ID只能有一个目标值；公式共用常量联动显示；不能用界面显示名称代替稳定ID。`

边界：

- 源码中的公式计算是对引擎的解释，保留candidate；站点静态字节核对不等于实战玩法验证。
- 指令内的移位/LEA结构、枚举、表行宽、开关和动态特效值不自动变成可写立即数。6.6疾风每点增伤明确是兵种槽N这一例外。
- 个人selector255无通用安全空值；9112只有0..179、3890只有0..254有效行。兵种ID255空槽和装备FF子通道守卫是独立协议。
- 名称相同、VA相同或同属6.6不能继承本样本字段；其它构建先重做画像和消费者核验。

补充说明：

- 规范化结构字段包含全部命中常量的实际原字节、宽度、签名和相对站点；来源报告保留不适用项及只读原因。
- 6.6疾风公式为(12−目标能力)×N/100，+12是代码补正，N来自特效117活动表槽；6.4/6.5为目标能力低于N时按(N−能力)×5/100追加，5是代码项。
- 物理/策略基础伤害均取攻方等级+25；武力/统帅或智力只参与双方能力差项，纠正旧文“武力/智力+25”。

写入策略：

- 本条候选用于设计和复核；执行修改须使用当前实现、匹配样本、原字节与签名门禁，并完成隔离副本测试。
- 公式族先ValidateEdits：范围、同ID冲突、曲线基础顺序、除数非零；Error拒绝整批，Warning明确提示后才提交。
- 统一整文件备份、等长候选、来源SHA冲突检测、提交、复读每个目标值与所有同步站点；失败恢复整组，外部改写冲突不可覆盖。

## 6.5 命中率曲线（物理/策略共用）

ID: `mechanism.65.dm-formula-hit-curve`；状态: `candidate`；证据: `source-reviewed`

把攻方能力与守方能力相比：攻方 ≥ 守方 2 倍直接 100%；1～2 倍是 90%～100%；1/2～1 倍是 60%～90%；低于一半只剩 30%～45%。物理命中比敏捷，策略命中比智力和士气之和。


计算规则：

- `1. 准备：A=攻方能力，D=守方能力；物理命中比敏捷；策略命中比智力+士气。`
- `2. 满命中：A ≥ D×2 → 命中率 = 100；达到两倍直接满命中。`
- `3. 高段：D ≤ A < D×2 → 90 + (A−D)×10/D；90～100。`
- `4. 中段：D/2 ≤ A < D → 60 + (A−D/2)×30/(D/2)；60～90。`
- `5. 低段：A < D/2 → 30 + max(A−D/3,0)×30/(D/3)；30～45。`
- `6. 封顶：命中率 = min(结果, 100)；不超过上限。`
- `7. 6.6 下限：命中率 = max(结果, —)；仅 6.6 有下限。`

### 输入、结构量与共用常量

- 满命中倍率：2；攻方 ≥ 守方×2 直接满命中；只读（指令编码）
- 高段基础：90；1～2 倍区间的起点；引用 mechanism.65.dm-constant-hit-curve-high-base
- 高段系数：10；1～2 倍区间每差 1 点加多少；引用 mechanism.65.dm-constant-hit-curve-high-coef
- 中段基础：60；1/2～1 倍区间的起点；引用 mechanism.65.dm-constant-hit-curve-mid-base
- 中段系数：30；1/2～1 倍区间每差 1 点加多少；引用 mechanism.65.dm-constant-hit-curve-mid-coef
- 低段除数：3；低于一半时先除以几；引用 mechanism.65.dm-constant-hit-curve-low-divisor
- 低段基础：30；低于一半时的起点；引用 mechanism.65.dm-constant-hit-curve-low-base
- 低段系数：30；低于一半时每差 1 点加多少；引用 mechanism.65.dm-constant-hit-curve-low-coef
- 命中上限：100；最高命中率；引用 mechanism.65.dm-constant-hit-curve-cap
- 6.6 命中下限：—；6.6 判定入口的最低命中率；不适用此基底

补充说明：

- 曲线函数 6.4 0x0043B50C，6.5/6.6 0x0043B53A；三基底同值。6.6 判定入口 0x0043B4DE 把最低值钳到 25。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 物理命中/闪避

ID: `mechanism.65.dm-formula-physical-hit`；状态: `candidate`；证据: `source-reviewed`

物理伤害函数先过命中判定：拿双方敏捷代入命中率曲线。6.4/6.5 命中率 ≥85% 时，第一次没打中会再判一次，命中率扣 10%，最多判 2 次；6.6 用最低命中率 25 的下限钳制。


计算规则：

- `1. 准备：A=攻方敏捷，D=守方敏捷；物理命中看敏捷。`
- `2. 套曲线：命中率 = 命中率曲线(A,D)；套用命中率曲线。`
- `3. 二次判定：6.4/6.5：未命中且命中率 ≥ 85 → 再判一次，命中率 −10；最多 {hit-retry-count} 次；6.6 不适用。`
- `4. 6.6 下限：命中率 = max(结果, —)；最低 25；6.4/6.5 不适用。`
- `5. 结果：命中 → 进入伤害结算；未命中 → 显示闪避；最终结果。`

### 输入、结构量与共用常量

- 计算属性：敏捷；物理命中看双方敏捷；只读（公式输入）
- 二次判定阈值：85；命中率达到多少才允许再判一次；引用 mechanism.65.dm-constant-hit-retry-threshold
- 二次判定扣减：10；再判一次时命中率扣多少；引用 mechanism.65.dm-constant-hit-retry-deduction
- 最多判定次数：2；最多判几次；引用 mechanism.65.dm-constant-hit-retry-count
- 6.6 命中下限：—；6.6 判定入口的最低命中率；不适用此基底

补充说明：

- 6.4 判定 0x0043B4BA、命中桩 0x0043B60B；6.5/6.6 判定 0x0043B4B6、命中桩 0x0043B600（同址不同分支）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 策略命中/闪避

ID: `mechanism.65.dm-formula-strategy-hit`；状态: `candidate`；证据: `source-reviewed`

策略伤害函数先过命中判定：攻方（智力+士气）对守方（智力+士气）套命中率曲线。6.4/6.5 同样有 85% 以上的补判；6.6 用最低命中率 25 的下限钳制。


计算规则：

- `1. 准备：A=攻方智力+士气，D=守方智力+士气；策略命中看智力与士气。`
- `2. 套曲线：命中率 = 命中率曲线(A,D)；套用命中率曲线。`
- `3. 二次判定：6.4/6.5：未命中且命中率 ≥ 85 → 再判一次，命中率 −10；最多 {hit-retry-count} 次；6.6 不适用。`
- `4. 6.6 下限：命中率 = max(结果, —)；最低 25；6.4/6.5 不适用。`
- `5. 结果：命中 → 进入策略伤害结算；未命中 → 显示策略闪避；最终结果。`

### 输入、结构量与共用常量

- 计算属性：智力+士气；策略命中看双方智力与士气；只读（公式输入）
- 二次判定阈值：85；命中率达到多少才允许再判一次；引用 mechanism.65.dm-constant-hit-retry-threshold
- 二次判定扣减：10；再判一次时命中率扣多少；引用 mechanism.65.dm-constant-hit-retry-deduction
- 最多判定次数：2；最多判几次；引用 mechanism.65.dm-constant-hit-retry-count
- 6.6 命中下限：—；6.6 判定入口的最低命中率；不适用此基底

补充说明：

- 6.4/6.5 命中桩 0x0043B6F3，取能力类型 2 与 4；6.6 命中桩 0x0043B730（同逻辑搬移）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 暴击/连击率曲线（共用）

ID: `mechanism.65.dm-formula-rate-curve`；状态: `candidate`；证据: `source-reviewed`

把攻方能力与守方能力相比：攻方 ≥ 守方 3 倍直接 100%；2～3 倍是 20%～100%；1～2 倍是 2%～20%；攻方低于守方时只剩 1%。物理暴击和策略暴击比士气，连击比敏捷。


计算规则：

- `1. 准备：A=攻方能力，D=守方能力；暴击比士气；连击比敏捷。`
- `2. 满率：A ≥ D×3 → 发动率 = 100；达到倍数直接满。`
- `3. 高段：D×2 ≤ A < D×3 → 20 + (A−D×2)×80/D；20～100。`
- `4. 低段：D ≤ A < D×2 → 2 + (A−D)×18/D；2～20。`
- `5. 低于守方：A < D → 1；低于守方只剩 1%。`
- `6. 封顶：发动率 = min(结果, 100)；不超过上限。`

### 输入、结构量与共用常量

- 满率倍率：3；攻方能力达到守方几倍就必发动；引用 mechanism.65.dm-constant-rate-curve-full-multiplier
- 高段倍率：2；高段的守方基准倍数；只读（指令编码）
- 高段系数：80；2～3 倍区间每差 1 点加多少；引用 mechanism.65.dm-constant-rate-curve-high-coef
- 高段基础：20；2～3 倍区间的起点；引用 mechanism.65.dm-constant-rate-curve-high-base
- 低段系数：18；1～2 倍区间每差 1 点加多少；引用 mechanism.65.dm-constant-rate-curve-low-coef
- 低段基础：2；1～2 倍区间的起点；引用 mechanism.65.dm-constant-rate-curve-low-base
- 最低发动率：1；攻方低于守方时的基础值；只读（指令编码）
- 发动率上限：100；最高发动率；引用 mechanism.65.dm-constant-rate-curve-cap

补充说明：

- 曲线函数 0x00405D0A（三基底同址同值）；物理暴击入口 0x00405E80，策略暴击入口 0x0040CA68，连击入口 0x004060D2。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 物理暴击

ID: `mechanism.65.dm-formula-physical-crit`；状态: `candidate`；证据: `source-reviewed`

先用双方士气算暴击率，再按暴击率随机判定。命中暴击后，额外伤害 = 原伤害 × (暴击率+100)/2 / 100；暴击率 0 → +50%，100 → +100%。三基底都进入集气池：6.4 池 0，6.5/6.6 池 2。6.6 再叠加特效 112 的返回值。


计算规则：

- `1. 准备：A=攻方士气，D=守方士气；物理暴击看士气。`
- `2. 套曲线：暴击率 = 发动率曲线(A,D)；套用发动率曲线。`
- `3. 封顶：暴击率 = min(暴击率, 100)；不超过上限。`
- `4. 随机：0..99 随机数与暴击率比较；随机判定。`
- `5. 集气：通过后进入集气池 2；6.4 池 0；6.5/6.6 池 2。`
- `6. 额外伤害：额外伤害 = 原伤害 × (暴击率+100)/2 / 100；暴击率 0 → +50%；100 → +100%。`
- `7. 特效112：6.6 再叠加特效 112 的返回值；仅 6.6。`

### 输入、结构量与共用常量

- 计算属性：士气；物理暴击看双方士气；只读（公式输入）
- 暴击率上限：100；最高暴击率；引用 mechanism.65.dm-constant-physical-crit-cap
- 伤害除数：2；暴击率除以几再加伤；只读（指令编码）
- 集气模式：2；物理暴击集气池编号；引用 mechanism.65.dm-constant-physical-crit-pool
- 暴击无效特效：0x31/0x41；0x412CF4：索引0x70 命中则允许暴击，否则按索引0x30；选择子随基底不同；只读（公式输入）

补充说明：

- 物理暴击函数 0x00405E80；暴击率来源 0x0040C7D8（能力类型 4）；伤害追加 6.4/6.5 0x00405F02，6.6 0x0042E4FD（sar / 2）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 策略暴击

ID: `mechanism.65.dm-formula-strategy-crit`；状态: `candidate`；证据: `source-reviewed`

先用双方士气算暴击率，再按暴击率随机判定。命中暴击后，额外伤害 = 原伤害 × (暴击率+100)/4 / 100；暴击率 0 → +25%，100 → +50%。三基底都进入集气池：6.4 池 0，6.5/6.6 池 18。


计算规则：

- `1. 准备：A=攻方士气，D=守方士气；策略暴击看士气。`
- `2. 套曲线：暴击率 = 发动率曲线(A,D)；套用发动率曲线。`
- `3. 封顶：暴击率 = min(暴击率, 100)；不超过上限。`
- `4. 随机：0..99 随机数与暴击率比较；随机判定。`
- `5. 集气：通过后进入集气池 18；6.4 池 0；6.5/6.6 池 18。`
- `6. 额外伤害：额外伤害 = 原伤害 × (暴击率+100)/4 / 100；暴击率 0 → +25%；100 → +50%。`

### 输入、结构量与共用常量

- 计算属性：士气；策略暴击看双方士气；只读（公式输入）
- 暴击率上限：100；最高暴击率；引用 mechanism.65.dm-constant-strategy-crit-cap
- 伤害除数：4；暴击率除以几再加伤；只读（指令编码）
- 集气模式：18；策略暴击集气池编号；引用 mechanism.65.dm-constant-strategy-crit-pool

补充说明：

- 策略暴击函数 0x0040CA68；暴击率包装 0x0040CADA；伤害追加 0x0040CAEB（shr eax,2）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 连击率

ID: `mechanism.65.dm-formula-combo-rate`；状态: `candidate`；证据: `source-reviewed`

先用双方敏捷算连击率，再随机判定是否追加一击。拥有特效 52 时不再看曲线，直接使用特效 52 的发动率。三基底都会进入集气池，池号默认 0。


计算规则：

- `1. 准备：A=攻方敏捷，D=守方敏捷；连击看敏捷。`
- `2. 特效52：有特效 52 → 连击率 = 100；默认 100。`
- `3. 套曲线：否则 连击率 = 发动率曲线(A,D)；套用发动率曲线。`
- `4. 集气：通过后进入集气池 0；三基底默认 0。`
- `5. 结果：随机判定是否追加一击；最终结果。`

### 输入、结构量与共用常量

- 计算属性：敏捷；连击看双方敏捷；只读（公式输入）
- 特效52 满率：100；有特效 52 时的连击率；引用 mechanism.65.dm-constant-active-combo-chance
- 集气模式：0；连击集气池编号；引用 mechanism.65.dm-constant-combo-pool

补充说明：

- 连击函数 0x004060D2；连击率来源 0x00405CB9（能力类型 3）；特效 52 桩 6.4 0x00405CF7、6.5/6.6 0x004E411B 与 0x004E4145。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 连击伤害

ID: `mechanism.65.dm-formula-combo-damage`；状态: `candidate`；证据: `source-reviewed`

没有强化连击时，连击伤害会逐次衰减；有强化连击/连击上限类特效后，后续连击不再衰减，并在原伤害上再加这个固定百分比。默认 0 表示只不衰减、不加伤。6.4 同址为空，未收录。


计算规则：

- `1. 连击基数：第 N 次连击使用连击伤害基数；N≥2。`
- `2. 无强化：无强化连击：按引擎内部系数逐次衰减；衰减系数不暴露为常量。`
- `3. 有强化：有强化连击：不再逐次衰减；强化连击类特效。`
- `4. 固定增伤：追加固定百分比 0%；默认 0。`

### 输入、结构量与共用常量

- 连击固定增伤：0；每次连击额外加多少；引用 mechanism.65.dm-constant-combo-damage-bonus

补充说明：

- 函数 0x004E313C；6.5/6.6 指令 0x004E319C 执行 imul eax,[ebp-4]; add eax,本值，再按百分比追加。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 主动连击发动率

ID: `mechanism.65.dm-formula-active-combo`；状态: `candidate`；证据: `source-reviewed`

特效 52 返回的数值直接作为追加一击的概率：100 = 每次都追加，50 = 一半机会。这个值就是主动连击的发动率。


计算规则：

- `1. 取发动率：特效 52 返回 100；默认 100。`
- `2. 钳制：概率函数把上限钳到 100；0x00437896 / 0x004287A8。`
- `3. 随机：与 0..99 随机数比较；成功则追加一击。`

### 输入、结构量与共用常量

- 主动连击发动率：100；追加一击的概率；引用 mechanism.65.dm-constant-active-combo-chance

补充说明：

- 特效 52 桩 6.4 0x00405CF7、6.5/6.6 0x004E411B 与 0x004E4145，字节 B0 64；概率函数 0x00437896 / 0x004287A8 把上限钳到 100 后与 0..99 随机数比较。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 引导攻击追加次数

ID: `mechanism.65.dm-formula-guided-attack`；状态: `candidate`；证据: `source-reviewed`

击杀目标后自动寻找下一个目标继续攻击。总攻击次数 = 这个值 + 1：6.4 默认 4（共五次），6.5/6.6 默认 2（共三次）。


计算规则：

- `1. 击杀：击杀目标后寻找下一个目标；引导链。`
- `2. 循环：已追加次数 < 2 且找到目标 → 继续攻击；按次数循环。`
- `3. 总次数：总攻击次数 = 2 + 1；6.4 默认 4（共 5 次）；6.5/6.6 默认 2（共 3 次）。`

### 输入、结构量与共用常量

- 引导攻击追加次数：2；击杀后再引导几次；引用 mechanism.65.dm-constant-guided-attack-count

补充说明：

- 引导循环 0x004212F1：inc 计数后 cmp 本值；6.4/6.5/6.6 指令 0x0042133D，字节 80 7D F8 ?? 73。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 奋战攻击目标数

ID: `mechanism.65.dm-formula-furious-attack`；状态: `candidate`；证据: `source-reviewed`

奋战会依次攻击一组相邻目标，引导攻击共用这份列表。8 = 周围八格全算，4 = 只算十字四格。


计算规则：

- `1. 建列表：构建相邻目标列表；方向表 0x004359F5。`
- `2. 限制：列表最多 8 个目标；8=八格；4=十字。`
- `3. 攻击：依次攻击列表内目标；0x00417C67。`
- `4. 共用：引导攻击共用这份列表；0x004212F1。`

### 输入、结构量与共用常量

- 奋战攻击目标数：8；一次奋战打几个目标；引用 mechanism.65.dm-constant-furious-attack-targets

补充说明：

- 列表构建 6.4/6.5 0x00405BE8、6.6 0x00405BF2；循环 cmp 本值后查方向表；6.4/6.5 指令 0x00405C16、6.6 0x00405C13。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 物理攻击伤害

ID: `mechanism.65.dm-formula-physical-damage`；状态: `candidate`；证据: `source-reviewed`

伤害 = 攻方等级 + 25，再用攻方武力与守方统帅算能力差：攻方高就加“差值÷2”，守方高就减“差值÷2”；最低保底 1 点。之后才结算突破、偷袭、疾风、固定增伤、吸血、猛击、盾反等特效。


计算规则：

- `1. 基础：伤害 = 攻方等级 + 25；基础伤害。`
- `2. 能力差：差 = 攻方武力 − 守方统帅；能力差。`
- `3. 攻方更高：伤害 += 差/2；除以 2 为指令编码。`
- `4. 守方更高：伤害 −= |差|/2；除以 2 为指令编码。`
- `5. 保底：伤害 < 1 → 1；最低 1 点。`
- `6. 特效：之后结算突破、偷袭、疾风、固定增伤、吸血、猛击、盾反；特效链。`

### 输入、结构量与共用常量

- 物理攻击基础伤害：25；能力差之外先加的固定伤害；引用 mechanism.65.dm-constant-physical-damage-base
- 能力差除数：2；双方武力/统帅差除以几；只读（指令编码）
- 保底伤害：1；最低打掉多少；只读（指令编码）
- 疾风攻击每点增伤：5；6.4/6.5 目标能力每低 1 点加 5%；6.6 为特效值 N 的倍率；引用 mechanism.65.dm-constant-swift-attack-bonus
- 疾风攻击补正值（6.6）：—；6.6 用 12 − 目标能力，再乘特效值 N；不适用此基底
- 突破攻击伤害加成：40；突破后伤害加多少百分比；引用 mechanism.65.dm-constant-breakthrough-damage-bonus
- 偷袭攻击每档增伤：25；侧击/背击每档加多少；引用 mechanism.65.dm-constant-sneak-attack-step
- 固定值基础加成：10；固定增伤/减伤的基础值；引用 mechanism.65.dm-constant-fixed-damage-basis
- 吸血攻击吸取上限：100；最多按伤害的几成回血；引用 mechanism.65.dm-constant-drain-attack-cap
- 猛击伤害比例上限：100；猛击最多打掉目标当前 HP 的几成；引用 mechanism.65.dm-constant-heavy-strike-cap
- 盾反反弹比例上限：100；盾反最多反弹攻击者当前 HP 的几成；引用 mechanism.65.dm-constant-shield-counter-cap

边界：

- 基础是攻方等级而非武力；武力仅用于对守方统帅的差值。
- 6.6疾风分支未见负值钳制；目标能力≥12的实战后果仍需独立验证，不能在公式中补一个max(0,…)。

补充说明：

- 物理伤害函数 0x0043BC62：基础经 0x0043BD2F call 0x00412674（0x4065D0 读 char+0x2C 等级）取攻方等级，加 25 在 0x0043BD34；能力对 0/1 来自 0x0043BCF5；能力差 shr 1 在 0x0043BD45/0x0043BD52；保底 inc eax 在 0x0043BD64。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 策略攻击伤害

ID: `mechanism.65.dm-formula-strategy-damage`；状态: `candidate`；证据: `source-reviewed`

伤害 = 攻方等级 + 25，再用攻方智力与守方智力算能力差：攻方高就加“差值÷3”，守方高就减“差值÷3”；最低保底 1 点。之后才结算策伤保底/限伤、MP辅助、绝对策略伤害、化险为夷、攻守兼备等特效。


计算规则：

- `1. 基础：伤害 = 攻方等级 + 25；基础伤害。`
- `2. 能力差：差 = 攻方智力 − 守方智力；能力差。`
- `3. 除数：伤害 += 差 / 3；除数默认 3。`
- `4. 保底：伤害 < 1 → 1；最低 1 点。`
- `5. 特效：之后结算策伤保底/限伤、MP辅助、绝对策略伤害、化险为夷、攻守兼备、孤勇者；特效链。`

### 输入、结构量与共用常量

- 策略攻击基础伤害：25；能力差之外先加的固定伤害；引用 mechanism.65.dm-constant-strategy-damage-base
- 策略伤害能力差除数：3；双方智力差除以几；引用 mechanism.65.dm-constant-strategy-damage-divisor
- 保底伤害：1；最低打掉多少；只读（指令编码）
- 策伤保底追加比例：20；已高于保底时再加多少；引用 mechanism.65.dm-constant-strategy-floor-bonus
- MP辅助策略基础加成：—；按剩余 MP 加伤时额外加多少；不适用此基底
- 绝对策略伤害追加比例：—；已高于下限时再加多少；不适用此基底
- 限制策略伤害额外减伤：—；未超上限时再减多少；不适用此基底
- 化险为夷最大伤害比例：—；一次伤害最多占最大 HP 的几成；不适用此基底
- 金钱防御每点伤害消耗：—；每挡 1 点伤害花多少金钱；不适用此基底
- 攻守兼备增伤触发 HP 线：—；一方 HP 不低于几成才增伤；不适用此基底
- 攻守兼备减伤触发 HP 线：—；另一方 HP 不高于几成才减伤；不适用此基底
- 孤勇者减伤上限：—；周围敌人越少最多减到几成；不适用此基底

边界：

- 基础是攻方等级而非智力；智力仅用于双方差值，后续策略倍率表及特效消费者须保持原执行次序。

补充说明：

- 策略伤害函数 6.4/6.5 入口 0x0043C022，6.6 同段；基础经 0x0043C0F6 call 0x00412674（0x4065D0 读 char+0x2C 等级）取攻方等级，加 25 在 0x0043C0FE（6.6 0x0043C10A 起）；能力对 2/2 在 0x0043C0F3；能力差除以 3 在成对 0x0043C126/0x0043C139；保底在 0x0047FA9E。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 普通反击伤害

ID: `mechanism.65.dm-formula-counter-damage`；状态: `candidate`；证据: `source-reviewed`

没有强化反击时，反击伤害 = 原攻击伤害 × 3 / 4。有强化反击时改按已损失 HP 比例加成，不走这份固定份数。6.4 未定位到同一份固定份数。


计算规则：

- `1. 无强化反击：伤害 = 原伤害 × 3 / 4；默认 3/4。`
- `2. 有强化反击：按已损失 HP 比例加成；不走固定份数。`
- `3. 6.4：同址为空，不适用；显示 —。`

### 输入、结构量与共用常量

- 普通反击伤害份数：3；反击按攻击伤害的几份结算；引用 mechanism.65.dm-constant-counter-damage-share

补充说明：

- 反击伤害函数 0x004E31B3；6.5/6.6 指令 0x004E3214 执行 imul eax,ecx,3; shr eax,2；6.4 同址为空。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 个人经验

ID: `mechanism.65.dm-formula-personal-exp`；状态: `candidate`；证据: `source-reviewed`

设攻方等级 AL、守方等级 DL。基础经验 = 2×clamp(DL−AL,−1,47)+6。若本次伤害 ≥ 目标当前 HP（击杀）：目标 Data 号等于全局 0x496C96 时额外 +48，否则额外 +64/(max(AL−DL,0)+2)。0x496C96 由战场变量装载 0x004122C1 从剧本变量 0x02 写入；最后乘经验倍率；同一行动多次攻击只把最大值写进 ctx+428。


计算规则：

- `1. 准备：AL=攻方等级，DL=守方等级；等级读取 0x004065D0；攻方 ctx+8，守方 ctx+1。`
- `2. 基础：基础 = 2×clamp(DL−AL,−1,47) + 6；等级差限制在 −1..47，全部整数运算。`
- `3. 击杀判定：本次伤害 ≥ 目标当前 HP → 击杀；目标 HP 由 0x0041B500 读取。`
- `4. 特殊目标：目标 Data 号 = 0x496C96 → 额外 +48；0x00406604 读 word [0x492F90+0x3D06]。`
- `5. 普通击杀：否则 额外 += 64 / (max(AL−DL,0)+2)；整数除法向下取整。`
- `6. 倍率：经验 = 经验 × (第8项能力+100)/100；倍率函数 0x00421053；0x00403D5A 还会翻倍。`
- `7. 写入：ctx+428 = max(旧值, 本次经验)；同一行动多次攻击只保留最大值。`

### 输入、结构量与共用常量

- 等级差下限：-1；守方低于攻方多少级仍按 -1 计算；只读（指令编码）
- 等级差上限：47；守方高于攻方多少级后封顶；只读（指令编码）
- 基础经验值：6；每次攻击的基础经验；引用 mechanism.65.dm-constant-personal-exp-base
- 击杀固定加成：48；击杀 0x496C96 指定目标时额外加多少；引用 mechanism.65.dm-constant-personal-exp-kill-flat
- 击杀经验分子：64；普通击杀经验的分子；引用 mechanism.65.dm-constant-personal-exp-kill-ratio-num
- 击杀除数偏移：2；除数 = max(攻方−守方,0)+本值；引用 mechanism.65.dm-constant-personal-exp-kill-ratio-offset
- 经验倍率基础：100；倍率 = (第8项能力+本值)/100；引用 mechanism.65.dm-constant-exp-multiplier-base
- 击杀判定来源：ctx+0x84；ctx+0x84+索引×4（攻击前HP）与 0x41B500 当前 HP 比较，≥ 视为击杀；只读（公式输入）
- 特殊目标来源：0x496C96；由战场变量装载 0x4122C1 从剧本变量 0x02 写入 0x496C96；只读（公式输入）
- 同行动取最大：取最大值；多次攻击只累计最高一次；只读（公式输入）
- 道具增加经验：0x0041CD4D；道具效果 0x26：当前经验 + 道具效果值；只读（公式结构）
- 道具效果值：item+15；道具记录 +0x15 的 WORD；只读（公式输入）

补充说明：

- 个人经验 0x004037A3（6.4/6.5 同码，6.6 同址重排）；主路径 6.5 0x00406023 调用、0x00406043 写 ctx+428。等级差钳位 0x00403847/0x0040384D，基础 0x00403855；击杀 6.4/6.5 0x00403824/0x0040383A/0x00403834，6.6 0x0040381E/0x00403833/0x0040382E；特殊目标装载 0x004122C1（表 0x004123BE）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 武器经验

ID: `mechanism.65.dm-formula-weapon-exp`；状态: `candidate`；证据: `source-reviewed`

经验开关 ctx+600≠0 且武器槽有装备才结算。造成 HP 或 MP 伤害时：经验 = 基础值；攻方等级高于守方 −1；暴击 +1。没有造成任何伤害时直接取“无伤害值”。最后乘经验倍率并累加到 ctx+42C。


计算规则：

- `1. 条件：ctx+600≠0 且武器槽有装备；否则本次武器经验为 0。`
- `2. 基础：经验 = 2；造成 HP 或 MP 伤害时走这一档。`
- `3. 等级差：攻方等级 > 守方等级 → 经验 −1；0x00403903 dec ecx。`
- `4. 暴击：ctx+604 ≠ 0 → 经验 +1；ctx+604 由物理暴击 0x00405F1A 置 1。`
- `5. 无伤害：HP/MP 伤害都为 0 → 经验 = 2；直接覆盖，不再走基础值。`
- `6. 倍率：经验 = 经验 × (第8项能力+100)/100；0x00421053；0x00403D5A 两处翻倍同样生效。`
- `7. 写入：ctx+42C += 经验；每次攻击累加。`

### 输入、结构量与共用常量

- 武器经验基础值：2；造成伤害时每次加多少；引用 mechanism.65.dm-constant-weapon-exp-base
- 攻方等级高：-1；攻方等级高于守方时 -1；只读（指令编码）
- 暴击加成：+1；暴击时 +1；只读（指令编码）
- 无伤害值：2；未造成 HP/MP 伤害时取本值；引用 mechanism.65.dm-constant-weapon-exp-no-damage
- 武器类型门控：0/0xA；6.4：0x4067CE(武器) 为 0 或 0xA 才计经验；6.5/6.6 该判断被 jmp 短路（任意类型都计）；只读（公式输入）
- 经验倍率基础：100；倍率 = (第8项能力+本值)/100；引用 mechanism.65.dm-constant-exp-multiplier-base
- 结算累加：累加；累加到 ctx+42C；只读（公式输入）

补充说明：

- 武器经验 0x00403870：基础立即数 0x004038FA（6.4/6.6 为 3，6.5 为 2）；等级 −1 在 0x00403903 dec ecx；暴击 +1 在 0x00403910 inc ecx（ctx+604 由 0x00405F1A 置 1）；无伤害立即数 0x00403919（6.4/6.5 为 2，6.6 为 1）。写入 0x00406054 add [ctx+42C],eax。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 防具经验

ID: `mechanism.65.dm-formula-armor-exp`；状态: `candidate`；证据: `source-reviewed`

目标阵营字节 [unit+5] 非 0（不是我方）才结算。基础值按防具槽逐个记；攻方等级低于守方 −1；没有造成 HP/MP 伤害时从基础上扣无伤害值。乘经验倍率后按防具槽写入 ctx+430+槽×4。


计算规则：

- `1. 条件：目标阵营字节 [unit+5] ≠ 0 才结算；0x0043FF54 判定目标不是我方。`
- `2. 基础：经验 = 3；每件防具分别结算。`
- `3. 等级差：攻方等级 < 守方等级 → 经验 −1；0x00403AF3 dec dword [ebp-4]。`
- `4. 无伤害：HP/MP 伤害都为 0 → 经验 −2；结果 = 基础 − 扣减。`
- `5. 倍率：经验 = 经验 × (第8项能力+100)/100；0x00421053；0x00403D5A 两处翻倍同样生效。`
- `6. 写入：ctx+430+防具槽×4 = 经验；0x00406074。`

### 输入、结构量与共用常量

- 防具经验基础值：3；每件防具的基础经验；引用 mechanism.65.dm-constant-armor-exp-base
- 攻方等级低：-1；攻方等级低于守方时 -1；只读（指令编码）
- 无伤害扣减：2；未造成 HP/MP 伤害时从基础上扣多少；引用 mechanism.65.dm-constant-armor-exp-no-damage
- 目标阵营门控：非我军；0x43FF54(守方单位) = (byte[unit+5] != 0)，即只对非我军目标计防具经验；只读（公式输入）
- 经验倍率基础：100；倍率 = (第8项能力+本值)/100；引用 mechanism.65.dm-constant-exp-multiplier-base
- 结算写入：按槽写入；按防具槽写入 ctx+430；只读（公式输入）

补充说明：

- 防具经验 0x00403A8A：基础立即数 0x00403A8E（3/3/4）；等级 −1 在 0x00403AF3 dec；无伤害扣减立即数 0x00403AFB（1/2/3）；写入 0x00406074。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 策略经验

ID: `mechanism.65.dm-formula-strategy-exp`；状态: `candidate`；证据: `source-reviewed`

策略记录 +0x0B 的类型为 2 时固定 +20；类型为 1 时走普通档。其余情况若是伤害类策略且造成击杀：攻方低于守方时 8×级差+32（封顶 200），攻方高于守方时 max(32−4×级差,0) 且最低 10；未击杀走普通档：攻方低于守方时 4×级差+10（封顶 100），攻方高于守方时 max(10−级差÷2,0) 且最低 5。目标 Data 号等于 0x496C96 时经验 ×2，最后乘经验倍率。策略经验实际分三路缓存：个人经验取最大值写 ctx+0x502（0x0044DE9E），武器经验取最大值写 ctx+0x506（0x00421363），防具经验按策略 ID 写 ctx+0x50A+ID（0x00421409）；再由 0x0041A0AC 统一结算到 0x004088CD 与 0x004082DD（6.4 入口 0x00451085）。


计算规则：

- `1. 条件：ctx+54C ≠ 0 才结算；启用开关；否则经验为 0。`
- `2. 类型：策略记录 +0x0B：2 → +20；1 → 普通档；其他 → 伤害判定；0x00425AC7 读取类型字节。`
- `3. 击杀档：攻方<守方：8×级差+32（≤200）；攻方≥守方：max(32−4×级差,0)，最低 10；伤害类策略且击杀目标时生效。`
- `4. 普通档：攻方<守方：4×级差+10（≤100）；攻方≥守方：max(10−级差÷2,0)，最低 5；未击杀或类型 1 走这一档。`
- `5. 特殊目标：目标 Data 号 = 0x496C96 → 经验 ×2；0x00406604 比较。`
- `6. 倍率：经验 = 经验 × (第8项能力+100)/100；倍率函数 0x00421053。`

### 输入、结构量与共用常量

- 策略类型字段：0/1/2；策略记录 +0x0B：2=固定加成，1=普通档，其他=伤害判定；只读（公式输入）
- 类型2固定经验：20；类型 2 直接加多少；只读（指令编码）
- 击杀档·每级：8；攻方低于守方时每级加多少；只读（指令编码）
- 击杀档·基础：32；击杀经验基础值；只读（指令编码）
- 击杀档·上限：200；击杀经验封顶；只读（指令编码）
- 击杀档·高等级每级扣：4；攻方高于守方时每级扣多少；只读（指令编码）
- 击杀档·最低：10；高等级时最少给多少；只读（指令编码）
- 普通档·每级：4；攻方低于守方时每级加多少；只读（指令编码）
- 普通档·基础：10；普通经验基础值；只读（指令编码）
- 普通档·上限：100；普通经验封顶；只读（指令编码）
- 普通档·高等级每级扣：÷2；攻方高于守方时每级扣一半；只读（指令编码）
- 普通档·最低：5；高等级时最少给多少；只读（指令编码）
- 特殊目标翻倍：×2；目标 Data 号 = 0x496C96 时经验 ×2；只读（指令编码）
- 经验倍率基础：100；倍率 = (第8项能力+本值)/100；引用 mechanism.65.dm-constant-exp-multiplier-base
- 结算入口：0x00421053；乘倍率并写入经验缓存；只读（公式输入）
- 个人经验缓存：ctx+0x502；ctx+0x502：同一策略取最大值；只读（公式输入）
- 武器经验缓存：ctx+0x506；ctx+0x506：同一策略取最大值；只读（公式输入）
- 防具经验缓存：ctx+0x50A；ctx+0x50A+策略ID（66 项字节）；只读（公式输入）
- 缓存应用：0x0041A0AC；个人+武器经验统一结算入口；只读（公式结构）
- 策略武器经验：0x00421363；0x421363 计算武器经验值；只读（公式结构）
- 武器经验基础：4；使用策略时给武器经验的基础加成；只读（公式输入）
- 武器等级差：-1；自身等级高于目标时扣 1；只读（公式输入）
- 武器门槛：2/0xA；武器类型为 2 或 0xA 才计入；只读（公式输入）

补充说明：

- 策略经验 0x00420EFB（6.4/6.5 同码，6.6 重排）；启用开关 ctx+54C；类型读取 0x00425AC7 movzx eax,byte [ecx+0Bh]，策略记录 0x00484002 imul ecx,61h + 0x4A3E77。6.5 立即数：+20 0x00420F25、击杀 0x00420FB5/0x00420FBC/0x00420FCD/0x00420FDE、普通 0x00421001/0x00421008/0x0042102E、翻倍 0x00420FE8。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 每回合经验（特效 3/4/5）

ID: `mechanism.65.dm-formula-per-turn-exp`；状态: `candidate`；证据: `source-reviewed`

每回合结算函数 0x0043CE15 循环 3 次，依次查询第 3/4/5 项（个人经验、武器经验、防具经验）的值，累加后再乘经验倍率 0x00407FAA（装备侧第 8 类成长累计 + 100）；个人经验加进 char 经验并走升级结算 0x004088CD，武器/防具经验分别走 0x004082DD 槽 0 / 槽 1。选择器表 0x0043CFCD 是装备侧的道具类型过滤值：0x0043CEE9-0x0043CEFC 把 i+3 与表值传给 0x004101D9，0x0041301E 再经 0x0043C794 调 0x00407A17 检查装备（槽 0/1 须为宝物且道具 +0x14 == 表值，槽 2 比 +0x11），命中才由 0x00407AF2 累加对应装备值；未命中时装备侧贡献为 0，因此表值本身会改变结果，而不只是标签。6.4/6.6 用 0x1D/0x1E，6.5 用 0。三件特效都为 0 时跳过结算。


计算规则：

- `1. 读取：循环 3 次查询特效 3/4/5 的值；0x004101D9；槽号 = i+3，表 0x0043CFCD 作为道具类型过滤值。`
- `2. 倍率：× (第 8 项能力 + 100) / 100；0x00407FAA + 0x00425AD9。`
- `3. 个人：个人经验加进 char 经验 → 0x004088CD 升级；0x0043CF9C-0x0043CFAA。`
- `4. 装备：武器槽 0 / 防具槽 1 → 0x004082DD；0x0043CFB7 / 0x0043CFC4。`
- `5. 边界：三件特效值都为 0 时跳过结算；0x0043CF26-0x0043CF42。`

### 输入、结构量与共用常量

- 循环上限：3；每回合结算 3 个经验特效；只读（指令编码）
- 选择器表：00 00 00；0x0043CFCD 三字节；装备/道具类型过滤值；只读（公式输入）
- 个人/装备 selector：3/4/5；个人 selector = i+3（经验/武器经验/防具经验）；只读（公式输入）
- 特效查询：0x4101D9；四参数查询：个人/装备/聚合/取值；只读（公式结构）
- 经验倍率：0x407FAA/0x425AD9；× (第 8 项能力 + 100) / 100；只读（公式结构）
- 个人经验结算：0x4088CD；acc[0] → char 经验 → 升级；只读（公式结构）
- 武器经验结算：0x4082DD(0)；acc[1] → 装备槽 0；只读（公式结构）
- 防具经验结算：0x4082DD(1)；acc[2] → 装备槽 1；只读（公式结构）
- 当前HP/MP写入：0x0043F6DB/0x0043F715；unit+0x10 / +0x14 = min(新值, 最大HP/MP)；无符号比较、无下限（超大/负值会被钳到上限）；只读（公式输入）

补充说明：

- 结算入口 6.4 0x0043CE15、6.5 0x0043CDF5、6.6 0x0043CDDD（主体从 0x0043CE20 起同址）；特效查询 0x004101D9 → 0x0041301E → 0x0043C794；装备过滤 0x00407A17/0x00407A1E；装备值累加 0x00407AF2 + 0x00407BA6（op=0，求和，上限 255）；倍率 0x00407FAA + 0x00425AD9；个人经验 0x004088CD；装备经验 0x004082DD；selector 表 0x0043CFCD。同函数 HP/MP 结算：0x4210F4（槽 0；选择子 6.4/6.5 0x1A、6.6 0x67）、0x421106（槽 1，选择子 0x1B）、0x42109C/0x42109A（选择子 0x44，6.4/6.5 只走 0x43C794，6.6 走 0x42518F 槽 0x32）；平坦项 0x417B5A（6.6 0x428A25）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 经验倍率与翻倍

ID: `mechanism.65.dm-formula-exp-multiplier`；状态: `candidate`；证据: `source-reviewed`

经验 = 经验 × (0x00407C35 索引 8 的装备侧成长累计 + 100) / 100。之后 0x00403D5A 再判两个条件：攻方为我军且槽位标志 0x501B00 非 0 → ×2；全局字节 0x500E9A == 1 → ×2。个人、武器、防具、策略经验都走这一条，两处翻倍因此同样作用于武器经验与防具经验。0x501B00 的逐槽标志可由 S 剧本命令 0x39/0x3A 置 3（调度表 0x00420C8E 索引 34/35 → 跳转条目 10 = 0x00420BFD：`cmp al,0x14` 后写 `[0x501B00+部队序号]=3`，序号 <20），并由命令 0x0A 的初始化函数 0x00415ACA 清零 0x501B00 起 0x140 个 DWORD；0x500E9A == 1 有静态写入（6.5 `0x41D69B` 置 1、`0x44EA34` 置 0、`0x4516FC` 自增，另有 `0x410594/0x4225F1/0x423377/0x4233EE/0x465FE0` 的 WORD 写点），阶段判定可达；按静态顺序最多 ×4，尚未实机验证。


计算规则：

- `1. 取能力：P = 角色第 8 项基础能力；0x00407C35 索引 8；6.6 0x00407C29。`
- `2. 倍率：倍率 = (P + 100) / 100；百分比计算 0x00425AD9。`
- `3. 乘算：经验 = 经验 × 倍率；向下取整。`
- `4. 翻倍一：攻方为我军且 0x501B00[部队序号] ≠ 0 → 经验 ×2；0x0042545F 读取；命令 0x39/0x3A 经 0x00420BFD 置 3，命令 0x0A 经 0x00415ACA 清零。`
- `5. 翻倍二：全局 0x500E9A == 1 → 经验 ×2；0x00403D6C；6.5 0x41D69B 置 1、0x44EA34 置 0、0x4516FC 自增。`
- `6. 适用：个人、武器、防具、策略经验共用；各经验函数末尾都调用 0x00421053。`

### 输入、结构量与共用常量

- 倍率基础值：100；倍率 = (第8项能力+本值)/100；引用 mechanism.65.dm-constant-exp-multiplier-base
- 倍率来源能力：第8项；角色第 8 项基础能力；只读（公式输入）
- 翻倍条件一：×2；攻方为我军且 0x501B00[槽位] 非 0；只读（公式输入）
- 翻倍条件二：×2；全局字节 0x500E9A == 1；只读（公式输入）
- 百分比计算：÷100；经验×百分比÷100；只读（公式输入）

补充说明：

- 倍率函数 0x00421053（6.6 入口 0x0042104F）：0x00407FAA = 0x00407C35(索引 8) + 100（立即数 0x00407FB9）；0x00407C35 汇总装备侧第 8 类数值（0x00429AD7 过滤类别、0x0040B3D7 按 (装备等级−1)×道具 +0x17 累加、宝物命中时 0x00452825 对索引≥7 原样返回），因此倍率来源是装备成长而非角色五维；0x00425AD9 做 经验×百分比/100；翻倍函数 0x00403D5A（0x0042545F 读 0x501B00、0x00403D6C 读 0x500E9A）。调用点：个人经验 0x00403865、武器经验 0x00403926、防具经验 0x00403B09、策略经验 0x0042103B（6.6 对应 0x00403926/0x00403B09/0x0042102A 调 0x0042104F）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 五维功勋记录

ID: `mechanism.65.dm-formula-merit-record`；状态: `candidate`；证据: `source-reviewed`

永久功勋记录地址 = 0x508400 + 角色ID×14。字段 0..4 分别为五维功勋，字段 5/6 为 HP/MP 功勋。基础能力读取函数 0x00407C35（6.6 0x00407C29）在 0x0041055D 读对应字段并叠加；只有我军（char+2A==0）参与叠加。写入函数 0x00408B52 支持模式 0 设值、1 累加、2 扣减，角色 ID ≥ 102 直接丢弃；0x508400 只有读取与两条剧本命令写入。战斗事件与道具效果 0x29（获得功勋）写入另一张表：0x508000 + ID×10 的 5 个 2 字节字段，累加函数 0x42AB8E 在 0x500E9A==1 且（0x505FDC==0 或 0x505F5C≠0）时把值 ×2；策略使用经 0x42AA22 给字段 1 加 2（0x2D 类 +4）；6.5/6.6 由 0x423EAD 清零 5 字段并累计到 0x505F40，6.4 无 0x423EAD 对应函数，只有 0x408FA0 在战后按 char+2 位图清理并累计。累加前 0x42AB8E 调 0x412A87/0x42518F 查询特效 0x45（6.5 名称“获得功勋”、6.6“功勋卓著”）；总额 0x505F40 由 0x456CB4/0x456DA6 消费（缓冲区 0x4FF3B8/0x4FFF68/0x500B60），静态未发现写入永久功勋 0x508400。战后每个单位另由 0x42A8EE 给本场战功字段 0 +1，并按条件表（6.4/6.5 0x407826、6.6 0x41A139，内容均为 00 03 04）给字段 3（战斗上下文 +608≥1）与字段 4（+604==1）各 +1；6.6 的派发入口搬到 0x40DC5C。0x423F4B 在开关 0x505FA8 与 char+2 允许位下，用本场战功按 0x42AC8F 的递增成本（50/65/75…）抵扣成长值，连续开关 0x501A74；三开关初值 0，默认关闭。


计算规则：

- `1. 定位：记录 = 0x508400 + 角色ID×14；角色 ID 来自单位首 WORD。`
- `2. 字段：字段 0..4 五维；5 HP；6 MP；每个字段 2 字节有符号。`
- `3. 读取：基础能力 += 功勋[字段]（仅我军）；0x0041055D/0x00407D74；char+2A≠0 跳过。`
- `4. 写入：0x00408B52：模式 0 设 / 1 加 / 2 减；角色 ID ≥ 102 直接丢弃。`
- `5. 剧本设置：命令 0x11..0x1F → 字段 0..6，模式 0 设置；0x004203D2 调用 0x00408B52。`
- `6. 剧本奖励：5 个剧本变量 → 角色ID/值/模式/字段/操作类型；0x00412007；变量表 0x00421492。`
- `7. 本场战功：记录 = 0x508000 + 角色ID×10（5 字段）；0x0042ACD2；道具效果 0x29 走这里。`
- `8. 累加：add word [记录+字段×2]：特效0x45值 + 增点（可×2，或整条放弃）；0x0042AB8E；0x500E9A==1 且 0x505FDC==0 时增点×2；0x505FDC≠0 且 0x505F5C≠0 时放弃；0x501B00[序号]≠0 再加一遍增点。`
- `9. 派发：0x42A9C4 全字段（击杀/可变增点）；0x42A9F7 字段2+1；击杀 0x0040380B/0x00420FA3；行动结算 0x0042309F（6.6 改到 0x0043BE08/0x0043BE74）。`
- `10. 结算：清零 5 字段并累计到 0x505F40；6.5/6.6 0x00423EAD；6.4 由 0x00408FA0 清理并累计。`

### 输入、结构量与共用常量

- 表基址：0x508400；功勋表起址；只读（公式输入）
- 行宽：14；每个角色 14 字节；只读（指令编码）
- 字段：7 项；0..4 五维、5 HP、6 MP；只读（公式输入）
- 角色上限：102；ID ≥ 102 直接丢弃；只读（指令编码）
- 读取入口：0x0041055D；叠加到基础能力；只读（公式输入）
- 写入入口：0x00408B52；模式 0 设 / 1 加 / 2 减；只读（公式输入）
- 取记录：0x004224A8；返回表内记录；只读（公式输入）
- 仅我军叠加：char+2A=0；非我军不参与加成；只读（公式输入）
- 剧本设置命令：0x11..0x1F；命令 0x11..0x1F 映射字段 0..6，模式 0 设置；只读（公式输入）
- 剧本奖励命令：5 变量；读 5 个剧本变量后写功勋并同步基础能力；只读（公式输入）
- 本场战功表：0x508000；0x508000 + ID×10（5 个 2 字节字段）；只读（公式输入）
- 本场战功取记录：0x0042ACD2；战斗事件与道具 0x29 的写入入口；只读（公式输入）
- 战功累加：0x0042AB8E；add word [记录+字段×2]；可被 ×2；只读（公式输入）
- 累加翻倍条件：0x500E9A/0x505FDC/0x505F5C；0x500E9A==1 且 0x505FDC==0 时增点×2；0x505FDC≠0 且 0x505F5C≠0 时整条放弃累加；只读（公式输入）
- 累加第三路：0x501B00；0x477ADC 按武将ID找到单位槽且 0x501B00[槽]≠0 时再累加一遍原始增点（非翻倍）；只读（公式输入）
- 战功全字段派发：0x0042A9C4；0x42A9C4(增点)：取记录后对字段 0..4 逐条累加；只读（公式结构）
- 战功单字段派发：0x0042A9F7；0x42A9F7：字段 2 固定 +1；6.6 改到伤害链调用；只读（公式结构）
- 战功字段1/3派发：0x0042A96D；0x42A96D：每目标字段 1 +1；该目标无任何伤害记录时字段 3 再 +1；只读（公式结构）
- 伤害记录数组：ctx+0x84/0x254；ctx+84h 与 ctx+254h：按目标槽的 dword 记录；两项都为 0 视为无伤害；只读（公式输入）
- 战后条件表派发：0x0042AADB；0x42AADB：表项 3/4 才累加（加的是表项值本身），其余表项跳过；6.6 表为 05 06 06 → 恒不加；只读（公式结构）
- 成长值→能力写入：9999；0x43A409(武将记录,字段,flag)：v=成长值+0x408A60(...)；我军只增不减；0x406ECA 写 word[rec+字段*2+0x11]，上限 9999；只读（公式结构）
- 固定 +1：0x0042A8EE；0x42A8EE 给字段 0 加 1；只读（公式输入）
- 条件表：00 03 04 01 03 02；战斗事件 +1 字段的条件表；6.6 迁至 0x41A139（内容相同）；只读（公式输入）
- 6.6 战后派发入口：—；6.6 以 0x40DC5C 按条件表派发字段 0..2；不适用此基底
- 战功兑换成长值：0x00423F4B；0x423F4B 用本场战功抵扣成长值（开关 0x505FA8、连续 0x501A74）；只读（公式结构）
- 出阵计数表：0x508A00；战斗后按武将 ID 自增的出阵次数表；只读（公式输入）
- 本场战功结算：0x00423EAD；清零 5 字段并累计到 0x505F40；只读（公式输入）
- 本场战功清理：0x00408FA0；按 char+2 位图清零本场战功；只读（公式输入）
- 道具功勋分派：0x29/0x2A；效果 0x29 写本场战功；0x2A/0x2B 写永久 HP/MP 功勋；只读（公式输入）
- 本场战功总额：0x00423EAD；清零 5 字段并把旧值累计到 0x505F40（开关 0x505F3C 无静态写入，消费入口 0x456CB4 受 0x505FA8 门控）；只读（公式结构）
- 战功链总开关：0x505FA8；0x505FA8/0x501A74/0x505FAC 均只有读点，无静态写入；只读（公式输入）
- 道具功勋分派：0x29/0x2A；效果 0x29 写本场战功；0x2A/0x2B 写永久 HP/MP 功勋；只读（公式输入）
- 本场战功总额：0x00423EAD；清零 5 字段并把旧值累计到 0x505F40（开关 0x505F3C 无静态写入，消费入口 0x456CB4 受 0x505FA8 门控）；只读（公式结构）
- 战功链总开关：0x505FA8；0x505FA8/0x501A74/0x505FAC 均只有读点，无静态写入；只读（公式输入）
- 道具功勋入口：0x004224D4；道具效果 0x29 获得功勋；只读（公式输入）
- 策略战功：2/4；策略使用 +2；0x2D 类 +4；只读（公式输入）
- 策略战功入口：0x0042AA22；0x42AA22 把值加到字段 1；只读（公式结构）
- 道具HP/MP上升：0x0042255C-0x0042258C；效果 0x2A/0x2B 同时加最大 HP/MP 与功勋字段 5/6；只读（公式输入）
- 上升上限：65535；最大 HP/MP 与功勋字段钳到 65535；只读（指令编码）
- 上升字段偏移：+0xA；功勋字段 5/6 从记录 +0xA 开始；只读（公式输入）

补充说明：

- 读取 0x0041055D；基础能力叠加 6.4/6.5 0x00407D74、6.6 0x00407D7F；写入 0x00408B52（0x004120AD、0x004203D2）；取永久记录 0x004224A8；本场战功取记录 0x0042ACD2（0x508000+ID×10）；累加 0x0042AB8E；战后派发 0x0042A8EE/0x0042AADB（6.6 0x0040DC5C）；条件表 0x00407826（6.6 0x0041A139）；兑换 0x00423F4B（开关 0x505FA8/0x501A74）；出阵计数 0x00406080 读 0x507800（6.4）/0x508A00（6.5·6.6）；结算 6.5/6.6 0x00423EAD（6.4 无对应函数）；清理/累计 0x00408FA0（0x0044ECBD 调用）；道具入口 0x004224D4。除 0x423EAD 与 6.6 派发入口外三基底同址。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 战功点分配（五维成长）

ID: `mechanism.65.dm-formula-merit-allocation`；状态: `candidate`；证据: `source-reviewed`

分配函数 0x0046206C：若 0x505FAC 非 0 且 0x5083FC 非 0，则 pool = 0x5083FC × 第二实参。对 5 个槽位 i：v = char[0x21+i]；v 达到上限（6.4 为 100，6.5/6.6 为 110）跳过；v < 80 时门槛 50，否则门槛 = (v−79)×10+55；pool ≥ 门槛时 pool −= 门槛、v+1、word[char+0x11+2i]+1，并在同槽位继续；余额经 0x42ACD2/0x42AB8E 写回本场战功。6.4 在函数内内联循环，6.5/6.6 调用 0x42AC8F（第三实参 1 时只判不扣）。


计算规则：

- `1. 取点：pool = 0x5083FC × 第二实参；计数器战后 +1，上限 255。`
- `2. 定位：i = 0..4；v = char[0x21+i]；槽位值即当前成长档。`
- `3. 上限：v ≥ 100（6.4）/110（6.5/6.6）跳过；0x004620D1 / 0x0042AC98。`
- `4. 门槛：v < 80 时 50；否则 (v−79)×10+55；0x004620D5/0x0042ACA4。`
- `5. 扣点：pool ≥ 门槛 → pool −= 门槛，v++；0x004620DE/0x0042ACC2。`
- `6. 提升：word[char+0x11+2i]++；与成长值同步。`
- `7. 循环：同槽位继续，直到不足门槛；6.4 内联；6.5/6.6 0x0042AC8F。`
- `8. 余额：转回本场战功 0x508000 表；0x004620EA-0x004620F6。`

### 输入、结构量与共用常量

- 分配函数：0x0046206C；0x46206C：点数×倍率后按门槛提升五维；只读（公式结构）
- 点数计数器：0x5083FC；战后累计点；上限 255，并同步到单位 +2；只读（公式输入）
- 分配开关：0x505FAC；0x505FAC 非 0 才分配；只读（公式输入）
- 槽位数：5；每次分配 5 个槽位；只读（指令编码）
- 成长值字段：char+0x21；槽位当前值 char+0x21+i；只读（公式输入）
- 能力字段：char+0x11；提升写入 char+0x11+2i；只读（公式输入）
- 成长值上限（6.4）：—；6.4 槽位值到 100 不再提升；不适用此基底
- 成长值上限（6.5/6.6）：110；6.5/6.6 槽位值到 110 不再提升；只读（指令编码）
- 门槛基础：50；槽位值 <80 时每点消耗 50；只读（公式输入）
- 门槛分界：80；槽位值达到 80 后改用递增门槛；只读（公式输入）
- 门槛系数：10；高段每差 1 点增加 10；只读（公式输入）
- 门槛偏移：55；高段门槛 = (值−79)×10+55；只读（公式输入）
- 倍率（0x409639/0x42AD3B）：25；对应调用点压栈的第二实参；只读（公式输入）
- 倍率（0x40C386/0x44CD8D）：25；对应调用点压栈的第二实参；只读（公式输入）
- 6.4 内联分配：—；6.4 在 0x46206C 内直接循环；不适用此基底
- 门槛函数（6.5/6.6）：0x0042AC8F；0x42AC8F 查门槛并返回消耗；只读（公式结构）
- 余额转入：0x0042ACD2/0x0042AB8E；分配余额写回本场战功；只读（公式结构）

补充说明：

- 四调用点第二实参：6.4 恒 1；6.5 恒 25；6.6 0x409639/0x42AD3B 为 50、0x40C386/0x44CD8D 为 10。计数器 6.4/6.5 0x4719A9、6.6 0x40BB05，上限 255；分配函数 0x46206C（0x46208A/0x462093/0x46209E）；门槛 0x4620D1-0x4620FE 与 0x42AC94-0x42ACCF；倍率点 0x409639/0x40C386/0x42AD3B/0x44CD8D。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 战场变量装载（特殊目标等）

ID: `mechanism.65.dm-formula-battle-variable-load`；状态: `candidate`；证据: `source-reviewed`

装载函数 0x004122C1 按表 0x004123BE 读取 10 个剧本变量（0x004183F7），再写入 0x494FD0、0x496C9F、0x492F90+0x3D0E、0x501BF4、0x496C94/96、0x496C98/9A 等全局。第 6 个读取值（剧本变量 0x02）写入 0x496C96，并在 0x496C94 记录“值 != 0xFFFF”的有效标志；个人经验用它和击杀目标 Data 号比较。变量/命令的剧本名称尚未闭环。


计算规则：

- `1. 入口：S 剧本命令 0x45：调度 0x00410A38 索引 67；0x004109E6 `sub eax,2`；6.4/6.5 处理 0x004122C1，6.6 0x004122C3。`
- `2. 读表：按 0x004123BE 的 10 个索引读取剧本变量；0x004183F7；16 位哨兵 0x8000（索引 2 用 0x80000000）时整条命令返回 5。`
- `3. 装载：写 0x494FD0、0x496C9F、0x492F90+0x3D0E；第 4 值 6.4 写 0x496E23（阈值 80），6.5/6.6 写 0x501BF4（阈值 60）；0x0041231C-0x0041234D；v>阈值时存 256-(v-阈值)。`
- `4. 目标：第 6/8 个值（均为剧本变量 0x02）写 0x496C96 / 0x496C98+0x496C9A；0x00412369 / 0x0041237D。`
- `5. 有效标志：值 != 0xFFFF → 0x496C94/0x496C98 = 1；第 9/10 值写 0x496E21/0x496E22；0x00412357/0x00412374/0x00412398/0x004123A9。`
- `6. 保留槽：第 5/7 个值（剧本变量 0x32）读入后未被消费；本轮逐字节复核；0x505F64 置 0xFFFF。`

### 输入、结构量与共用常量

- 变量表：26 26 04 3E 32 02 32 02 47 22；10 个剧本变量索引；只读（公式输入）
- 特殊目标写入：0x496C96；第 6 个读取值写入特殊目标全局；只读（公式输入）
- 有效标志：0x496C94；值 != 0xFFFF 时置 1；只读（指令编码）
- 第二目标写入：0x496C98/9A；第 8 个读取值写入第二目标全局；只读（公式输入）
- 战场标志：0x494FD0；第 1 个读取值 !=0 → 0x494FD0；只读（公式输入）
- 其它写入：0x496C9F 等；第 2/3/4 个值分别写 0x496C9F、0x492F90+0x3D0E、0x501BF4；只读（公式输入）
- 命令名称：未闭环；剧本变量 0x02 的命令语义尚未闭环；只读（公式输入）

补充说明：

- 装载 0x004122C1；变量表 0x004123BE = 26 26 04 3E 32 02 32 02 47 22；读取 0x004183F7；写入 0x0041231C-0x0041238C（0x494FD0、0x496C9F、0x492F90+0x3D0E、0x501BF4、0x496C94/96、0x496C98/9A）。三基底同址。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 角色升级经验

ID: `mechanism.65.dm-formula-char-level-exp`；状态: `candidate`；证据: `source-reviewed`

角色经验结算 0x004088CD：读当前经验 char+0x2D、等级 char+0x2C，循环扣减阈值并升级（0x00408D52 做成长），满级后写 255。阈值：6.4 固定 150、上限 80；6.5 每 20 级一档，阈值 = (min(等级/20,3)+3)×50（150/200/250/300），上限 60；6.6 固定 250、上限 99。6.5 的分段阈值在同一次结算中只算一次。


计算规则：

- `1. 读取：L=等级 char+0x2C，E=经验 char+0x2D；0x004065D0 / 0x004065C7。`
- `2. 阈值：6.4：150；6.5：(min(L/20,3)+3)×50；6.6：250；6.5 由 0x0040D21D 现算。`
- `3. 升级：E ≥ 阈值 且 L < 60 → E -= 阈值，L++；升级成长 0x00408D52。`
- `4. 写回：未满级写 E；满级写 255；char+0x2D。`
- `5. 边界：6.5 的分段阈值在同一次结算中只算一次；一次结算内不随升级重算。`

### 输入、结构量与共用常量

- 最大等级：60；角色经验结算的最高等级；引用 mechanism.65.dm-constant-char-exp-max-level
- 每级经验（6.4/6.6）：—；6.4/6.6 每升一级所需经验；不适用此基底
- 等级分段（6.5）：20；每多少级提高一档；引用 mechanism.65.dm-constant-char-exp-band-65
- 每档增量（6.5）：50；阈值 = (min(等级/分段,3)+3)×本值；引用 mechanism.65.dm-constant-char-exp-step-65
- 档位上限（6.5）：3；分段最多计 3 档；只读（指令编码）
- 等级字段：char+2C；角色等级 char+0x2C；只读（公式输入）
- 经验字段：char+2D；角色经验 char+0x2D；只读（公式输入）
- 满级经验：255；满级后经验写 255；只读（指令编码）

补充说明：

- 角色经验 0x004088CD；经验 getter 0x004065C7、等级 getter 0x004065D0；升级成长 0x00408D52；6.5 阈值函数 0x0040D21D（分段 20 在 0x0040D225、档位上限 3 在 0x0040D230/0x0040D235、增量 50 在 0x0040D23B）。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 装备升级经验

ID: `mechanism.65.dm-formula-equip-level-exp`；状态: `candidate`；证据: `source-reviewed`

装备经验结算 0x004082DD：只处理槽位 0（武器）与 1（防具），经验在 char+0x2E+槽×3+2、等级在 +1。阈值按道具记录 +0x11 的 bit0 分宝物/普通；宝物 200、普通 100（6.4/6.6）或 150（6.5）。上限宝物 9/9/15、普通 5/5/9。循环扣减并调用 0x004083C6 做装备成长；满级后经验写 255。使用策略还会按策略 ID 计算一笔装备经验：基础 3（6.6 4），目标等级更高时 −1，乘经验倍率后缓存到 ctx+0x50A+ID，再写入防具槽 1（0x00421409 → 0x004082DD）。


计算规则：

- `1. 读取：槽位 0/1，等级 char+0x2E+槽×3+1，经验 +2；0x004032DF / 0x00409680。`
- `2. 阈值：宝物 200；普通 150；0x0040B4E1 判道具 +0x11 bit0。`
- `3. 升级：经验 ≥ 阈值 且 等级 < 上限 → 扣减、升级、成长；装备成长 0x004083C6。`
- `4. 上限：宝物 9；普通 5；到上限后不再升级。`
- `5. 写回：满级写 255，否则写剩余经验；0x0040329B。`
- `6. 归属：武器经验进槽 0，防具经验进槽 1；0x00406C95 / 0x00405B05。`

### 输入、结构量与共用常量

- 宝物经验阈值：200；带宝物标记的装备每级经验；引用 mechanism.65.dm-constant-equip-exp-threshold-special
- 普通经验阈值：150；普通装备每级经验；引用 mechanism.65.dm-constant-equip-exp-threshold-normal
- 宝物等级上限：9；宝物装备最高等级；引用 mechanism.65.dm-constant-equip-level-cap-special
- 普通等级上限：5；普通装备最高等级；引用 mechanism.65.dm-constant-equip-level-cap-normal
- 满级经验标记：0xFF；装备到上限后经验写 0xFF（不再累计）；只读（指令编码）
- 升级后回调：0x004083C6；写等级（0x403286）后调 0x4083C6(charID, slot)；校验 ID<0x400、槽≤1，走脚本派发；只读（公式输入）
- 宝物判定：bit0；道具记录 +0x11 的 bit0；只读（公式输入）
- 处理槽位：0/1；只处理武器槽 0 / 防具槽 1；只读（指令编码）
- 等级字段：char+0x2F；char+0x2E+槽×3+1；只读（公式输入）
- 经验字段：char+0x30；char+0x2E+槽×3+2；只读（公式输入）
- 满级经验：255；满级后经验写 255；只读（指令编码）
- 策略防具经验：3；使用策略时给防具经验的基础加成；只读（公式输入）
- 防具经验加成条件：type=0；施放类型为 0 且 ctx+0x108+索引×4 非 0 时才加基础值；只读（公式输入）
- 防具经验加成条件：type=0；施放类型为 0 且 ctx+0x108+索引×4 非 0 时才加基础值；只读（公式输入）
- 策略等级差：-1；目标等级更高时扣 1；只读（公式输入）
- 策略禁用查询：0x00450931；0x450931 扫 0x508C00 的 FF 分隔表；6.6 为 NOP；只读（公式输入）
- 特技习得查询：0x0041873E；0x41873E 扫 5 条 3 字节表项（技能ID word + 需求等级 byte）；只读（公式输入）
- 特技数据表：0x00511800；0x41E907(i)=dword[0x500C37]+i×0x10（80 条）；静态为 5 个 {00 04 01}+尾 01 的占位记录；只读（公式输入）
- 特技习得查询：0x0041873E；0x41873E 扫 5 条 3 字节表项（技能ID word + 需求等级 byte）；只读（公式输入）
- 特技数据表：0x00511800；0x41E907(i)=dword[0x500C37]+i×0x10（80 条）；只读（公式输入）
- 策略禁用查询：0x00450931；0x450931 扫 0x508C00 的 FF 分隔表；6.6 为 NOP；只读（公式输入）
- 特技习得查询：0x0041873E；0x41873E 扫 5 条 3 字节表项（技能ID word + 需求等级 byte）；只读（公式输入）
- 特技数据表：0x00511800；0x41E907(i)=dword[0x500C37]+i×0x10（80 条）；静态为 5 个 {00 04 01}+尾 01 的占位记录；只读（公式输入）
- 策略经验入口：0x00421409；按策略 ID 计算并写入防具经验槽 1；只读（公式结构）

补充说明：

- 装备经验 0x004082DD；宝物判定 0x0040B4E1（+0x11 bit0）；等级 getter 0x004032DF、经验 getter 0x00409680、等级 setter 0x00403286、经验 setter 0x0040329B；满级标记 0x0040839D；武器槽调用 0x00406C95、防具槽调用 0x00405B05。
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 能力/成长/HP/MP 写入分派

ID: `mechanism.65.dm-formula-ability-write`；状态: `candidate`；证据: `source-reviewed`

增量入口 0x406ECA：字段 0..4 写五维 word[rec+0x11+i×2]，min(旧+值,9999)；字段 5 写最大 HP（dword +0x1B，会顺带清零 +0x1D/+0x1E）；字段 6 写最大 MP（word +0x1F）；字段 7/8 改当前 HP/MP（走 0x45AA37，模式字节 0x505F30=1 表示增加）；字段 9 无操作；字段 10..14 写成长值 byte[rec+字段+0x17]，封顶 100；字段 15 写 0x501A84 的单位槽字节。直接设置入口 0x407027 用 min(值,0x270F)/min(值,0xFFFF) 覆盖同名字段，字段 7/8 置 0x505F30=2 直设。


计算规则：

- `1. 准备：字段 0..4 五维、5 最大 HP、6 最大 MP、7/8 当前 HP/MP、10..14 成长值、15 单位槽字节；0x00406ED2 cmp al,0Fh 后按字段分派。`
- `2. 五维/HP/MP 增量：0x47FA89(旧,值,—) = min(旧+值,—)；模式 1 时旧值取 0，等价直写。`
- `3. 成长值：byte[rec+字段+0x17] = min(旧+值,—)；字段 10..14 对应成长值 0..4。`
- `4. 当前 HP/MP：置 0x505F30=— → 0x45AA37 按模式改当前值；0 扣减(保底1)、1 增加、2 直设。`
- `5. 直接设置：0x407027 用 min(值,0x270F) / min(值,0xFFFF) 覆盖；S 剧本命令模式 0；模式 2 先取基准再相减。`

### 输入、结构量与共用常量

- 能力/HP/MP 增量上限：9999；0x47FA89(旧,值,cap)=min(旧+值,cap) 的封顶值；只读（公式结构）
- 成长值封顶：100；字段 10..14 写成长值 byte[rec+字段+0x17] 的上限；只读（公式结构）
- 最大 HP 直接设置上限：65535；0x407027 字段 5 写 dword[rec+0x1B] 的封顶；只读（公式结构）
- HP/MP 变更模式：0/1/2；0x505F30：0 扣减(保底1)、1 增加、2 直接设为值；只读（公式结构）

补充说明：

- 0x00406ECA：0x00406ED2 cmp al,0Fh；0x00406EDC cmp dword [ebp+10h],1；0x00406EE7 push 270Fh；0x00406F09 sub eax,5 + 0x00406F0C jmp [eax*4+406FC5h]；表 0x406FC5 三基底同为 13 6F 40/31 6F 40/96 6F 40/96 6F 40/B8 6F 40；0x00406F1E push dword [ecx+1Bh]；0x00406F2C mov dword [ecx+1Bh],eax；0x00406F5B push 64h；0x00406F88 add ecx,501A84h；0x00406F96 mov byte [505F30h],1；0x00407083 mov byte [505F30h],2；0x0040DA4D mov ecx,dword [505F30h]；0x00407027 直接设置（0x00407042 cmp dx,270Fh / 0x00407058 cmp edx,0FFFFh / 0x004070BD mov word [ecx+4],dx + 0x00423E30）；0x0045AA37 索引 7/8 → 0x0041B500/0x0043F6DB、0x00472840/0x0043F715
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 兵种成长档位与前置积分

ID: `mechanism.65.dm-formula-troop-tier`；状态: `candidate`；证据: `source-reviewed`

兵种 ID 必须 ≤0x3B（59）；0x408A60 以 20 级为块：基础 = v(当前兵种)×max(等级−(兵种%3)×20,0) + v(前兵种)×min(等级,(兵种%3)×20)（%3==2 时先按 40 级比较）。升级条件 0x41D3DC 要求等级 ≥ (兵种%3+1)×20，兵种%3==2 或兵种>59 直接不可升。HP/MP 重算 0x4149CF 额外加 0x413FAC：6.4/6.5 = 2×Σ v(兵种−1..兵种−r)，6.6 = 2×r×v(当前兵种)。


计算规则：

- `1. 准备：兵种 = byte[rec+0x2B]，等级 = byte[rec+0x2C]，兵种 ≤ 59；0x00408A73 cmp al,3Bh。`
- `2. 分档：r = 兵种 % 3；块长 20；0x0041FBF8 mov cl,3；0x00408A66 push 14h。`
- `3. 基础：v(当前兵种)×max(等级−r×块长,0) + v(前兵种)×min(等级,r×块长)；r==2 时先按 2×块长 比较（0x00408A8B shl ecx,1）。`
- `4. 前置积分：HP/MP 额外 + 2×Σ v(兵种−1..兵种−r)；0x00413FF9 shl dword [ebp-4],1；6.6 改为 2×r×v(当前兵种)。`
- `5. 升级条件：等级 ≥ (r+1)×块长；r==2 或兵种 > 59 不可升；0x0041D42E inc edx；0x0041D406 cmp edx,2。`

### 输入、结构量与共用常量

- 兵种档位长度：20；0x408A60 的块长，也是升级阈值单位；只读（公式结构）
- 兵种 ID 上限：59；超过 59 的兵种不参与成长计算；只读（公式结构）
- 档位除数：3；兵种 ID 按 %3 分档；只读（公式结构）
- 前置积分倍数：2；0x413FAC 末尾对累加值左移 1 位；只读（公式结构）

补充说明：

- 0x00408A66 push 14h（块长）；0x00408A73 cmp al,3Bh；0x00408A8B shl ecx,1（%3==2 时按 40 比较）；0x0041FBF8 mov cl,3 + 0x0041FBFA idiv ecx（兵种%3）；0x0041D3EB cmp al,3Bh；0x0041D406 cmp edx,2；0x0041D42E inc edx + 0x0041D42F imul edx,[ebp-8]；0x00413FF9 shl dword [ebp-4],1；0x00414A3B call 0x00413FAC
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 兵种提升执行

ID: `mechanism.65.dm-formula-troop-up`；状态: `candidate`；证据: `source-reviewed`

流程：编号 0x7F 时先 0x41D124 解析目标；0xFF 直接退出；取 unit/officer 后 0x406610 读兵种、inc 后 0x40E01F 写回 byte[rec+0x2B]（兵种 +1）；接着字段 5/6（最大 HP/MP）各加 0x413FAC(字段, rec, 1) = 2×v(前兵种)；随后 0x401D4E 缓冲拷贝、0x44FA7E/0x44FA1F 取文本、10 帧演出循环，最后 0x42F699(2, “兵种提升”文本 0x48B698, 新兵种) 与 UI 刷新。升级条件不在此函数，见 0x41D3DC。


计算规则：

- `1. 定位：编号 0x7F → 0x41D124 解析目标；0xFF 直接退出；0x0041D478/0x0041D482。`
- `2. 取记录：0x4061F9(槽) 取战场单位，0x40658F 取武将记录；0x0041D48E/0x0041D496。`
- `3. 兵种+1：byte[rec+0x2B] = troop + 1；0x0041D510 inc eax；0x0040E025 mov byte [ecx+2Bh],al。`
- `4. 补正：最大 HP/MP 各 += 2×v(前兵种)（0x413FAC(字段,rec,1)）；0x0041D52C/0x0041D53A，循环字段 5..6。`
- `5. 演出与提示：10 帧循环 + 提示文本 0x48B698；0x0041D5B2 cmp [ebp-4],0Ah；0x0041D653 push 48B698h。`

### 输入、结构量与共用常量

- 兵种提升增量：1；0x41D468 把 byte[rec+0x2B] 设为 troop+1；只读（公式结构）
- 提升演出帧数：10；兵种提升动画的循环次数；只读（公式结构）

补充说明：

- 0x0041D468 三基底前 8 字节 55 8B EC 6A 05 51 6A 01；0x0041D478 编号 7Fh 分支；0x0041D489 mov byte [edx+3],al；0x0041D48E call 0x004061F9；0x0041D50B call 0x00406610；0x0041D510 inc eax；0x0041D515 call 0x0040E01F；0x0041D52C call 0x00413FAC + 0x0041D53A call 0x00406ECA；0x0041D5B2 cmp dword [ebp-4],0Ah；0x0041D653 push 48B698h + 0x0041D65A call 0x0042F699
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 装备成长累计（经验倍率基数）

ID: `mechanism.65.dm-formula-equip-growth`；状态: `candidate`；证据: `source-reviewed`

0x407C35(索引) 对武器/防具两槽逐件累加：先取 0x40B3D7(道具记录, 装备等级) = (等级−1)×byte[道具+0x17]（仅当 0x40B444 映射类型 ≤1），再用 0x429AD7 做类别过滤（类别 0x0A 对索引 0/2 例外），最后对宝物（+0x11 bit0）且类别映射等于索引的装备追加 0x4200F8(道具+0x16, 装备等级) 与 0x452825(单位, 索引)。结果加 100 即经验倍率（0x407FAA）。


计算规则：

- `1. 取装备：槽 0/1：0x4065F0 取道具 ID，0xFF 跳过；0x4837C2 取道具记录；0x00407C55/0x00407C63。`
- `2. 基础成长：0x40B3D7 = (装备等级−1)×byte[道具+0x17]（门控 0x40B444 ≤ 1）；0x0040B3FB 循环；0x0040C464 cmp eax,1。`
- `3. 类别过滤：0x429AD7 返回 0 才计入（类别 0x0A 对索引 0/2 例外）；0x00429AE5 cmp al,0Ah；6.6 该过滤在 0x405670。`
- `4. 宝物附加：宝物且 0x40678E(item)==索引 → 0x4200F8(道具+0x16, 等级) + 0x452825；0x00407CA5/0x00407CAD/0x00407CB8；6.6 0x004200F5。`
- `5. 汇总：返回值 + 100 = 经验倍率（0x407FAA）；0x00407FB7 add eax,64h。`

### 输入、结构量与共用常量

- 每级成长字段：+0x17；道具记录 +0x17 的字节即每级成长值；只读（公式结构）
- 类型门控上界：1；0x40B444 映射值 ≤1 才计每级成长；只读（公式结构）
- 宝物类别例外值：0x0A；0x429AD7：类别 0x0A 对索引 0/2 也视为匹配；只读（公式结构）

补充说明：

- 0x00407C35 循环 0x00407C49 cmp al,1；0x00407C5A call 0x004032DF；0x00407C6C call 0x0040B3D7；0x00407C7A call 0x00429AD7（6.6 0x00405670）；0x00407C94 add [ebp-0Ch],eax；0x00407CA5 call 0x0040B4E1；0x00407C98 call 0x0040678E；0x00407CA5 call 0x0044661A；0x00407CAD call 0x004200F8（6.6 0x004200F5）；0x00407CB8 call 0x00452825；0x0040B3FB 循环 cmp [ebp-8],al；0x0040B444 movzx eax,byte [ecx+11h] + 0x0040B44B cmp al,14h + 0x0040B453 cmp al,1Ah；0x0040C464 cmp eax,1
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 宝物成长与百分比换算

ID: `mechanism.65.dm-formula-treasure-growth`；状态: `candidate`；证据: `source-reviewed`

0x4200F8(道具+0x16, 等级) 按道具 +0x14 类型分支：6.5 下 0x1F → +等级、0x55 → ×(等级+1)、0x2F → ×等级+0x1E、0x33(原值4)→+3、0x32→×2、0x36/0x42/0x46→+1、其它→×3/2；等级≥10 再查表 0x46236F[类型−0x1A]（0xFE 表示不覆盖）。随后 0x452825(索引) 在 索引<7 且 0x46230F[索引]==2 时取该字段当前能力（0..4 word+0x11+i×2、5 dword+0x1B、6 word+0x1F），用 0x425AD9 换算为 能力×成长/100。


计算规则：

- `1. 取类型与值：eax=道具+0x16（值），byte[eax-2]=道具+0x14（类型），dl=装备等级；0x004200FE/0x00420101。`
- `2. 类型分支：0x1F→+等级；0x55→×(等级+1)；0x2F→×等级+30；0x33→+3；0x32→×2；0x36/0x42/0x46→+1；其它→×3/2；0x00420131/0x004200DD/0x004200ED/0x00420166。`
- `3. 高等级查表：等级≥10 → byte[0x46236F + (类型−0x1A)]，0xFE 时不覆盖；0x00420177/0x0042017A/0x00420180。`
- `4. 门控：0x452825：索引<7 且 0x46230F[索引]==2 才应用；0x00452839 cmp al,7；0x00452842 cmp byte [eax+46230Fh],2。`
- `5. 换算：结果 = 0x425AD9(当前能力, 成长值) = 能力×成长/100；0x0045287D call 0x00425AD9；0x00425AE5 mov ecx,64h。`

### 输入、结构量与共用常量

- 百分比除数：100；0x425AD9 = a×b/100 的除数；只读（公式结构）
- 宝物门控值：2；0x46230F[索引]==2 才应用宝物成长；只读（公式结构）
- 宝物成长表哨兵：0xFE；0x46236F 表值 0xFE 表示不覆盖；只读（公式结构）

补充说明：

- 0x004200FB movzx edx,dl；0x004200FE movzx ecx,byte [eax]；0x00420101 movzx eax,byte [eax-2]；0x00420131 add cl,dl；0x004200DD imul ecx,edx；0x004200ED add ecx,1Eh；0x00420166 imul ecx,ecx,3 + 0x00420169 shr ecx,1；0x00420177 sub eax,1Ah + 0x0042017A mov al,[eax+46236Fh] + 0x00420180 cmp al,0FEh；0x00452842 cmp byte [eax+46230Fh],2；0x00452865 mov cx,word [edx+eax*2]；0x0045287D call 0x00425AD9；0x00425AE5 mov ecx,64h
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 能力成长缺口与基准补正

ID: `mechanism.65.dm-formula-growth-gap`；状态: `candidate`；证据: `source-reviewed`

流程：索引 ≥5 直接返回传入值；否则 0x42518F(0x3D, 0x5C, 选择子, 0) 查特效（0x40B922 判阵营后走 0x4101D9 或 0x41301E），特效值非 0 时作为每级基准，否则用 (兵种字节 + 成长档) >> 1；随后 基准×等级 + byte[rec+索引+0x21] + 永久功勋，减去当前能力并取下界 0，再加传入成长值；同时返回合成值（edx）供 0x452825 作为宝物成长基数。6.6 入口 0x436E02，基准改走 0x407D48。


计算规则：

- `1. 索引门：索引 ≥5 → 直接返回传入成长值（ecx=0）；0x00436DE9 cmp dword [ebp+8],5。`
- `2. 特效查询：0x42518F(0x3D, 0x5C, 选择子, 0) → 0x4101D9 / 0x41301E；0x00436DF3-0x00436DFB；6.4 选择子 1。`
- `3. 基准：特效值非 0 用它；否则 (兵种字节 + 成长档) >> 1；0x00436E1E/0x00436E26/0x00436E32/0x00436E3A。`
- `4. 合成：基准×等级 + 成长值 byte[rec+索引+0x21] + 永久功勋；0x00436E46 imul eax,edx；0x00436E68 call 0x0041055D。`
- `5. 取差：max(合成值 − 当前能力, 0) + 传入值；edx=合成值；0x00436E82/0x00436E8D/0x00436E8F/0x00436E91。`

### 输入、结构量与共用常量

- 缺口索引上限：5；索引 ≥5 不走基准补正；只读（公式结构）
- 基准合成除数：2；(兵种字节 + 成长档) >> 1 的除数；只读（公式结构）
- 特效查询参数：0x3D/0x5C；0x42518F(0x3D, 0x5C, 6.4=1/6.5·6.6=2, 0)；只读（公式结构）

补充说明：

- 0x00436DE9 cmp dword [ebp+8],5 + 0x00436DED jae；0x00436DF3-D [ebp+8] 压栈 0x3D/0x5C/选择子/0；0x00436E17 call 0x00406610；0x00436E1E call 0x0041B782；0x00436E26 call 0x00436CA3；0x00436E32 call 0x0041A534；0x00436E3A shr eax,1；0x00436E42 movzx edx,byte [ecx+2Ch] + 0x00436E46 imul eax,edx；0x00436E52 add eax,edx（+0x21 成长值）；0x00436E68 call 0x0041055D；0x00436E82 movzx edx,word [ecx+edx]；0x00436E8D mov eax,edx + 0x00436E8F sub eax,edx + 0x00436E91 add eax,[ebp-8]
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 特效查询分派（我方/敌方）

ID: `mechanism.65.dm-formula-effect-dispatch`；状态: `candidate`；证据: `source-reviewed`

0x42518F(索引, 选择子, 模式, 0) 把 4 参透传给 0x40B922（判定 0x40B913()==3，0x40B913=0x41EDEF(0x4AC63C)），返回 1 走 0x4101D9（按 unit 直查，内部先 0x426A07(0,0,0,0,0) 取默认并与 0x505F78 比较），返回 0 走 0x41301E（0x40BE7D 取 ID → 0x4198BE(0x500C3B, …) → 0x43C794 → 0x413009 → 0x40BF2F）。6.4 的 0x42518F 起 44 字节为 90（函数不存在），等价函数 0x412A87，5 处调用点全部指向它。


计算规则：

- `1. 入口：0x42518F(索引, 选择子, 模式, 0) 原样透传 4 参；6.4 为 0x412A87；0x0042518F；6.4 0x00412A87。`
- `2. 阵营判定：0x40B922 = (0x40B913()==3)，0x40B913 = 0x41EDEF(0x4AC63C)；0x0040B92C cmp al,3；0x0040B916 mov ecx,4AC63Ch。`
- `3. 我方：返回 1 → 0x4101D9：先 0x426A07(0,0,0,0,0)，再与 0x505F78 比较；0x004101E4/0x004101F3。`
- `4. 敌方：返回 0 → 0x41301E：0x40BE7D → 0x4198BE(0x500C3B) → 0x43C794 → 0x413009 → 0x40BF2F；0x00413022/0x00413037/0x00413049/0x00413053。`
- `5. 参数差异：模式：6.4 为 1，6.5/6.6 为 2；索引 0x3D、选择子 0x5C 不变；6.4 0x00436DF5 push 1；6.5 0x00436DF5 push 2。`

### 输入、结构量与共用常量

- 分派判定值：3；0x40B922 = (0x40B913()==3)，为 1 走 0x4101D9；只读（公式结构）
- 查询模式：1/2；0x436DE1 调 0x42518F 的第三参；只读（公式结构）
- 索引/选择子：0x3D/0x5C；0x436DE1 查特效用的索引与选择子；只读（公式结构）

补充说明：

- 0x0042518F push 4 参 + 0x0042519F call 0x0040B922 + 0x004251AB call 0x004101D9 + 0x004251B2 call 0x0041301E + 0x004251BA ret 10h；0x0040B922 cmp al,3 + sete cl；0x0040B913 call 0x41EDEF(0x4AC63Ch)；6.4 0x00412A87 同形；0x004101D9 0x004101E4 call 0x426A07；0x004101F3 cmp ecx,[505F78h]；0x0041301E 0x00413022 call 0x40BE7D + 0x00413037 call 0x4198BE + 0x00413049 call 0x43C794 + 0x00413053 call 0x413009
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 模式字节与特效合并规则

ID: `mechanism.65.dm-formula-merge-mode`；状态: `candidate`；证据: `source-reviewed`

0x40B913 直接返回 byte[0x4AC63C]（0x41EDEF 仅是 byte[ecx]），0x40B922 将其与 3 比较；0x4AC63C 的静态写点：0x416A78 置 2、0x416A91 自增到 3、0x43C015 置 3（紧邻策略伤害入口 0x43C022），初值 0。合并函数 0x40BF2F(mode,a,b)：0 求和、1 取大、3 按位或、其它在 a==7 时保留否则取大；0x413009 在 mode==2 且 edx==0 时把 edx 设为 eax 再合并。


计算规则：

- `1. 模式字节：0x40B913() = byte[0x4AC63C]（0x41EDEF 只是 byte[ecx]）；0x0041EDF2 movzx eax,byte [ecx]；0x0040B916 mov ecx,4AC63Ch。`
- `2. 静态写点：置 2：6.4 0x4426E7 / 6.5·6.6 0x416A78；自增：6.4 0x442700 / 6.5·6.6 0x416A91；置 3：6.4·6.5 0x43C015 / 6.6 0x43C010；0x004426E7/0x00416A78；0x00442700/0x00416A91；0x0043C015；6.6 0x0043C010。`
- `3. 分派：byte[0x4AC63C]==3 → 0x4101D9，否则 0x41301E；0x0040B92C cmp al,3；0x0040B92E sete cl。`
- `4. 合并规则：0x40BF2F：0=和、1=取大、3=或、其它 a==7 保留否则取大；0x0040BF36/0x0040BF3F/0x0040BF4C/0x0040BF50。`
- `5. 包装：0x413009：mode==2 且 edx==0 时 edx=eax，再 0x40BF2F；0x0041300C/0x00413015/0x00413017。`

### 输入、结构量与共用常量

- 模式字节地址：0x4AC63C；0x4AC63C：初值 0；0x416A78 写 2、0x416A91 自增、0x43C015 写 3；只读（公式结构）
- 分派值：3；byte[0x4AC63C]==3 时走 0x4101D9；只读（公式结构）
- 合并模式：0/1/3/7；0x40BF2F：0=和、1=取大、3=按位或、其它原值 7 保留否则取大；只读（公式结构）
- 模式置2入口：0x416A75；进段函数：置 2 → 调用 → 自增到 3；只读（公式结构）
- 模式置3位置：0x43C015；结算前置 3 的写点；只读（公式结构）

补充说明：

- 0x0040B916 mov ecx,4AC63Ch；0x0040B91B call 0x0041EDEF；0x0041EDF2 movzx eax,byte [ecx]；0x0040B92C cmp al,3 + 0x0040B92E sete cl；0x00416A78 C6 05 3C C6 4A 00 02；0x00416A91 FE 05 3C C6 4A 00；0x0043C015 C6 05 3C C6 4A 00 03；0x0040BF32 test ecx,ecx + 0x0040BF36 add eax,edx + 0x0040BF4C or eax,edx + 0x0040BF50 cmp al,7；0x0041300C cmp ecx,2 + 0x00413015 mov edx,eax + 0x00413017 call 0x0040BF2F
- 本条描述当前源码对引擎公式的解释，未逐条完成游戏内运行验收；多版本位置提示仅为来源原文，实际站点以所引用精确画像常量实体为准。

写入策略：

本机制候选不授权自动写回。固定结构值保持只读；有knowledgeRef的常量依其画像、字段签名、范围和统一事务契约修改。

## 6.5 引导攻击追加次数：代码固定值

ID: `mechanism.65.dm-constant-guided-attack-count`；状态: `candidate`；证据: `source-reviewed`

击杀目标后最多再引导几次；总攻击次数 = 这个值 + 1。6.4 默认 4（共五次），6.5/6.6 默认 2（共三次）。部分改版基底写 255 表示基本不限次数。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "guided-attack-count",
  "title": "引导攻击追加次数",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00421340",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00020740",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "80 7D F8",
        "suffix": "73 16",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "80 7D F8",
        "actualSuffix": "73 16"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00421340"
      ]
    }
  ]
}
```

补充说明：

- 引导循环 0x004212F1：inc byte [ebp-8] 后 cmp byte [ebp-8], 本值；指令 0x0042133D 字节 80 7D F8 ?? 73。
- 本条是6.5精确样本的代码固定值；值单位：次。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 奋战攻击目标数：代码固定值

ID: `mechanism.65.dm-constant-furious-attack-targets`；状态: `candidate`；证据: `source-reviewed`

奋战会依次打几个相邻目标，引导共用这份列表。8 = 周围八格全算，4 = 只算十字四格。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "furious-attack-targets",
  "title": "奋战攻击目标数",
  "value": 8,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405C16",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00005016",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "08",
      "signature": {
        "prefix": "FE 45 F4 80 7D F4",
        "suffix": "73 3A FF 75 F4 8D 4D FC 51",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "FE 45 F4 80 7D F4",
        "actualSuffix": "73 3A FF 75 F4 8D 4D FC 51"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405C16"
      ]
    }
  ]
}
```

补充说明：

- 列表构建 0x00405BE8（6.6 为 0x00405BF2）：循环 cmp 本值后查 0x004359F5 方向表、过滤并写入 0x00500E9D 目标列表；0x00417C67 逐项执行攻击，0x004212F1 负责引导链。
- 本条是6.5精确样本的代码固定值；值单位：人。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 主动连击发动率：代码固定值

ID: `mechanism.65.dm-constant-active-combo-chance`；状态: `candidate`；证据: `source-reviewed`

拥有主动连击时，追加一击的发动概率：100 = 每次都追加，50 = 一半机会。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "active-combo-chance",
  "title": "主动连击发动率",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004E411C",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000B591C",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "04 B0",
        "suffix": "EB 35 8B",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "04 B0",
        "actualSuffix": "EB 35 8B"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x004E4146",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000B5946",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "75 04 B0",
        "suffix": "EB 0B FF",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "75 04 B0",
        "actualSuffix": "EB 0B FF"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004E411C"
      ]
    },
    {
      "label": "6.5/6.6 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004E4146"
      ]
    }
  ]
}
```

补充说明：

- 特效 52 桩：确认特效 52（0x34）后 mov al,本值（6.4 指令 0x00405CF7，6.5/6.6 指令 0x004E411B 与 0x004E4145，字节均为 B0 64）；返回值直接作为概率实参传给 0x00437896，该函数把上限钳到 100 后与 0..99 随机数比较。双枪攻击桩 0x004060D2 与 0x004E3000 也按它判定追加一击。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 普通反击伤害份数：代码固定值

ID: `mechanism.65.dm-constant-counter-damage-share`；状态: `candidate`；证据: `source-reviewed`

没有强化反击时，反击伤害按攻击伤害的几份结算：3 = 75%，4 = 全额，2 = 50%。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "counter-damage-share",
  "title": "普通反击伤害份数",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004E3216",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000B4A16",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "0E 8B 4D 08 6B C1",
        "suffix": "C1 E8 02 85 C0 75",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0E 8B 4D 08 6B C1",
        "actualSuffix": "C1 E8 02 85 C0 75"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004E3216"
      ]
    }
  ]
}
```

补充说明：

- 特效 72 强化反击的伤害函数 0x004E31B3：没有该特效时执行 imul eax,ecx,3; shr eax,2（6.5/6.6 指令 0x004E3214，字节 6B C1 ?? C1 E8 02），即反击伤害 = 攻击伤害的 3/4；有该特效时改走损失 HP 比例加成。6.4 同址为空，不适用。
- 本条是6.5精确样本的代码固定值；值单位：份。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 突破攻击台词：文本槽

ID: `mechanism.65.dm-constant-breakthrough-quote`；状态: `candidate`；证据: `source-reviewed`

突破攻击触发时显示的固定台词，最多 8 个汉字；超出会被截断。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "breakthrough-quote",
  "title": "突破攻击台词",
  "value": "唔，好强的气势。",
  "nature": "文本槽",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00500CFF",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000D24FF",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 16,
      "expectedFieldBytes": "DF ED A3 AC BA C3 C7 BF B5 C4 C6 F8 CA C6 A1 A3",
      "signature": {
        "prefix": "",
        "suffix": "",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "",
        "actualSuffix": ""
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": []
}
```

补充说明：

- Ekd5.exe 固定 16 字节文本槽，文件偏移 0xD24FF；6.4/6.5/6.6 三个基底的槽内容都能按 GBK 解出完整句子。
- 本条是6.5精确样本的文本槽；值单位：文字。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 突破攻击伤害加成：代码固定值

ID: `mechanism.65.dm-constant-breakthrough-damage-bonus`；状态: `candidate`；证据: `source-reviewed`

突破攻击触发时伤害额外增加的百分比：40 = 伤害×1.4，0 = 不加成。伤害增幅走自己的装备值。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "breakthrough-damage-bonus",
  "title": "突破攻击伤害加成",
  "value": 40,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004110C1",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000104C1",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "28",
      "signature": {
        "prefix": "B0",
        "suffix": "83 7D 08 01 74",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "B0",
        "actualSuffix": "83 7D 08 01 74"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004110C1"
      ]
    }
  ]
}
```

补充说明：

- 伤害函数 0x0043BC62 在 0x0043BE1B 调用 0x00411072：确认特效 97 突破后执行 mov al,本值（指令 0x004110C0），再由 0x00425AD9 按 伤害×百分比/100 追加；三基底同址同值 40。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 吸血攻击吸取上限：代码固定值

ID: `mechanism.65.dm-constant-drain-attack-cap`；状态: `candidate`；证据: `source-reviewed`

吸血攻击最多按造成伤害的百分之几回血：100 = 全额回血，50 = 最多回一半。6.6 同名特技为“以战养战”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "drain-attack-cap",
  "title": "吸血攻击吸取上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00406B9A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00005F9A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "E8 00 00 00 00 85 C0 74 00 3C",
        "suffix": "76 02 B0 64 FF 35 00 00 00 00 50 E8",
        "prefixMask": "01 00 00 00 00 01 01 01 00 01",
        "suffixMask": "01 01 01 00 01 01 00 00 00 00 01 01",
        "actualPrefix": "E8 44 96 00 00 85 C0 74 3D 3C",
        "actualSuffix": "76 02 B0 64 FF 35 BD E8 48 00 50 E8"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x00406B9E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00005F9E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "76 02 B0",
        "suffix": "FF 35",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "76 02 B0",
        "actualSuffix": "FF 35"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00406B9A"
      ]
    },
    {
      "label": "全部基底 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00406B9E"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x00406B3C：确认特效 20 后用 cmp al,本值（0x00406B99）和 mov al,本值（0x00406B9D）成对把吸取比例钳到上限，再按 伤害×比例/100 回血；三基底同址同值 100。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 铁索横江邻接方向数：代码固定值

ID: `mechanism.65.dm-constant-iron-chain-directions`；状态: `candidate`；证据: `source-reviewed`

铁索横江会检查几个方向的相邻友军：4 = 十字四格，8 = 八方格。改大后斜向相邻的友军也会纳入连锁。6.6 同名特技为“一步剑围”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "iron-chain-directions",
  "title": "铁索横江邻接方向数",
  "value": 4,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00412B7A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00011F7A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "04",
      "signature": {
        "prefix": "8B 45 FC 3C",
        "suffix": "73 40 8D 4D F0 51",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 45 FC 3C",
        "actualSuffix": "73 40 8D 4D F0 51"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00412B7A"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x00412B5F：按方向循环 call 0x0041031C 取邻格、0x00435884 取单位、0x00406710 比阵营并查询特效 96；循环上限 cmp al,本值（6.4/6.5 指令 0x00412B79、6.6 0x00412B7A，字节 3C ?? 73）。三基底同值 4。
- 本条是6.5精确样本的代码固定值；值单位：方向。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 猛击伤害比例上限：代码固定值

ID: `mechanism.65.dm-constant-heavy-strike-cap`；状态: `candidate`；证据: `source-reviewed`

猛击额外造成目标当前 HP 的百分之几伤害；这里限制这个百分比最大能到多少。100 = 最多打掉目标当前 HP 的量。6.6 同名特技为“势不可挡”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "heavy-strike-cap",
  "title": "猛击伤害比例上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00422036",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00021436",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "55 8B EC 8B 4D 08 E8 68 9F FE FF 85 C0 74 14 3C",
        "suffix": "76 02",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "55 8B EC 8B 4D 08 E8 68 9F FE FF 85 C0 74 14 3C",
        "actualSuffix": "76 02"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x0042203A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0002143A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "02 B0",
        "suffix": "50 6A 08",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "02 B0",
        "actualSuffix": "50 6A 08"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00422036"
      ]
    },
    {
      "label": "6.5 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0042203A"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x00422026：确认特效 114 后用 cmp al,本值 与 mov al,本值 成对钳制，再由 0x004220D3 按 目标当前HP×N/100 追加伤害；6.4 在 0x00422039/0x0042203D，6.5/6.6 在 0x00422036/0x0042203A。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 盾反反弹比例上限：代码固定值

ID: `mechanism.65.dm-constant-shield-counter-cap`；状态: `candidate`；证据: `source-reviewed`

盾反额外反弹攻击者当前 HP 的百分之几伤害；这里限制这个百分比最大能到多少。100 = 最多反弹攻击者当前 HP 的量。6.4 名称“花枪驭敌”，6.6 名称“厄难毒体”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "shield-counter-cap",
  "title": "盾反反弹比例上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0042205F",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0002145F",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "E8 51 9F FE FF 85 C0 74 14 3C",
        "suffix": "76 02",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "E8 51 9F FE FF 85 C0 74 14 3C",
        "actualSuffix": "76 02"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x00422063",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00021463",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "02 B0",
        "suffix": "50 6A 02",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "02 B0",
        "actualSuffix": "50 6A 02"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0042205F"
      ]
    },
    {
      "label": "6.5 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00422063"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x00422026：确认特效 115 后用 cmp al,本值 与 mov al,本值 成对钳制，再由 0x004220D3 按 攻击者当前HP×N/100 反弹；6.4 在 0x004220B5/0x004220B9，6.5/6.6 在 0x0042205F/0x00422063。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 神魔附体属性上限：代码固定值

ID: `mechanism.65.dm-constant-demon-stat-cap`；状态: `candidate`；证据: `source-reviewed`

神魔附体提升单项属性时最多算到多少；9999 是原版上限。6.6 同名特技为“洗髓易筋”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "demon-stat-cap",
  "title": "神魔附体属性上限",
  "value": 9999,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043C517",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003B917",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 4,
      "expectedFieldBytes": "0F 27 00 00",
      "signature": {
        "prefix": "03 45 FC 3D",
        "suffix": "72 05",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "03 45 FC 3D",
        "actualSuffix": "72 05"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x0043C51E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003B91E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 4,
      "expectedFieldBytes": "0F 27 00 00",
      "signature": {
        "prefix": "72 05 B8",
        "suffix": "8B E5 5D",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "72 05 B8",
        "actualSuffix": "8B E5 5D"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043C517"
      ]
    },
    {
      "label": "6.5 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043C51E"
      ]
    }
  ]
}
```

补充说明：

- 属性写入函数 0x0043C4D3 由 0x0040715A/0x0040718F/0x004071C4/0x004071F9/0x0040722E 五个神魔附体消费者调用；6.5 在 0x0043C516/0x0043C51D 把结果钳到 9999，6.6 在 0x0043C521/0x0043C528。两处同值。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 疾风攻击每点增伤：代码固定值

ID: `mechanism.65.dm-constant-swift-attack-bonus`；状态: `candidate`；证据: `source-reviewed`

本项为代码固定每点增伤5%；目标能力A低于特效值N才触发，追加伤害=原伤害×(N−A)×5/100。N是触发门槛，5是本项立即数。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "swift-attack-bonus",
  "title": "疾风攻击每点增伤",
  "value": 5,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043BD88",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003B188",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "05",
      "signature": {
        "prefix": "D8 6B C0",
        "suffix": "FF 75",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "D8 6B C0",
        "actualSuffix": "FF 75"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043BD88"
      ]
    }
  ]
}
```

补充说明：

- 当前物理伤害入口为0x0043BC62；来源中0x0043BC5A是历史定位提示，不能登记为本公式入口。实际字段与签名以本条精确样本站点为准。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 物理攻击基础伤害：代码固定值

ID: `mechanism.65.dm-constant-physical-damage-base`；状态: `candidate`；证据: `source-reviewed`

物理攻击在能力差之外先加的固定伤害；默认25。改大后所有物理攻击都会更疼。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "physical-damage-base",
  "title": "物理攻击基础伤害",
  "value": 25,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043BD36",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003B136",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "19",
      "signature": {
        "prefix": "8B 4D D4 E8 40 69 FD FF 83 C0",
        "suffix": "89 45 FC 8B 45",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D D4 E8 40 69 FD FF 83 C0",
        "actualSuffix": "89 45 FC 8B 45"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043BD36"
      ]
    }
  ]
}
```

补充说明：

- 物理伤害函数 0x0043BC62 在 0x0043BD34 执行 add eax,本值（字节 83 C0 19），随后才按双方能力差增减；三基底同址同值25。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 策略攻击基础伤害：代码固定值

ID: `mechanism.65.dm-constant-strategy-damage-base`；状态: `candidate`；证据: `source-reviewed`

策略/精神力攻击在能力差之外先加的固定伤害；默认25。改大后所有策略攻击都会更疼。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "strategy-damage-base",
  "title": "策略攻击基础伤害",
  "value": 25,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043C101",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003B501",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "19",
      "signature": {
        "prefix": "01 45 FC 83 45 FC",
        "suffix": "90 90 90 90",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "01 45 FC 83 45 FC",
        "actualSuffix": "90 90 90 90"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043C101"
      ]
    }
  ]
}
```

补充说明：

- 策略伤害函数在 6.4/6.5 的 0x0043C0FE、6.6 的 0x0043C115 执行 add [ebp-4],本值（字节 83 45 FC 19）；三基底同值25。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 策略伤害能力差除数：代码固定值

ID: `mechanism.65.dm-constant-strategy-damage-divisor`；状态: `candidate`；证据: `source-reviewed`

策略伤害里双方能力差除以几；默认3。改大后能力差影响变小，改1影响最大。两处必须同时改。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "strategy-damage-divisor",
  "title": "策略伤害能力差除数",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043C126",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003B526",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 4,
      "expectedFieldBytes": "03 00 00 00",
      "signature": {
        "prefix": "2B 45 E8 99 B9",
        "suffix": "F7 F1 03 45 FC",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "2B 45 E8 99 B9",
        "actualSuffix": "F7 F1 03 45 FC"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x0043C139",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003B539",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 4,
      "expectedFieldBytes": "03 00 00 00",
      "signature": {
        "prefix": "2B 45 EC 99 B9",
        "suffix": "F7 F1 50 FF 75",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "2B 45 EC 99 B9",
        "actualSuffix": "F7 F1 50 FF 75"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043C126"
      ]
    },
    {
      "label": "全部基底 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043C139"
      ]
    }
  ]
}
```

补充说明：

- 策略伤害高位/低位两分支都执行 mov ecx,本值; div ecx（指令 0x0043C126 与 0x0043C139，字节 B9 ?? ?? ?? ?? F7 F1）；三基底同址同值3。
- 本条是6.5精确样本的代码固定值；值单位：倍。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 化力为疗每点伤害MP消耗：代码固定值

ID: `mechanism.65.dm-constant-convert-heal-mp-cost`；状态: `candidate`；证据: `source-reviewed`

化力为疗用 MP 抵扣伤害时，每 1 点伤害消耗的 MP；默认 2。改大后同样伤害更耗 MP，改小更省。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "convert-heal-mp-cost",
  "title": "化力为疗每点伤害MP消耗",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040D0A8",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C4A8",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "2B 48 10 3B CA 72 0D 6B D2",
        "suffix": "3E 29 55 B8 3E 29 55 EC EB 0A",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "2B 48 10 3B CA 72 0D 6B D2",
        "actualSuffix": "3E 29 55 B8 3E 29 55 EC EB 0A"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D0A8"
      ]
    }
  ]
}
```

补充说明：

- 6.5 特效 193 消费者 0x0040D057 的 MP 抵伤分支：MP 足够时执行 imul edx,本值（指令 0x0040D0A6，字节 6B D2 ??），随后把伤害与 MP 各扣一次；6.4/6.6 无该序列。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 夺锐攻击能力上限：代码固定值

ID: `mechanism.65.dm-constant-sharpen-attack-cap`；状态: `candidate`；证据: `source-reviewed`

夺锐攻击把目标六项能力的数值上限压到本值；默认 3。六项能力同值，写入时 12 处同步。仅 6.5 有该处理函数。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "sharpen-attack-cap",
  "title": "夺锐攻击能力上限",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040D0E1",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C4E1",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "0F B6 49 18 83 F9",
        "suffix": "7E 14",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F B6 49 18 83 F9",
        "actualSuffix": "7E 14"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x0040D0F7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C4F7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "8B 4D E0 36 C6 41 18",
        "suffix": "8B 4D E0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D E0 36 C6 41 18",
        "actualSuffix": "8B 4D E0"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D101",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C501",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "0F B6 49 19 83 F9",
        "suffix": "7E 14",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F B6 49 19 83 F9",
        "actualSuffix": "7E 14"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D117",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C517",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "8B 4D E0 36 C6 41 19",
        "suffix": "8B 4D E0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D E0 36 C6 41 19",
        "actualSuffix": "8B 4D E0"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D121",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C521",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "0F B6 49 1A 83 F9",
        "suffix": "7E 14",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F B6 49 1A 83 F9",
        "actualSuffix": "7E 14"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D137",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C537",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "8B 4D E0 36 C6 41 1A",
        "suffix": "8B 4D E0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D E0 36 C6 41 1A",
        "actualSuffix": "8B 4D E0"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D141",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C541",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "0F B6 49 1B 83 F9",
        "suffix": "7E 14",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F B6 49 1B 83 F9",
        "actualSuffix": "7E 14"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D157",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C557",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "8B 4D E0 36 C6 41 1B",
        "suffix": "8B 4D E0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D E0 36 C6 41 1B",
        "actualSuffix": "8B 4D E0"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D161",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C561",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "0F B6 49 1C 83 F9",
        "suffix": "7E 14",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F B6 49 1C 83 F9",
        "actualSuffix": "7E 14"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D177",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C577",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "8B 4D E0 36 C6 41 1C",
        "suffix": "8B 4D E0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D E0 36 C6 41 1C",
        "actualSuffix": "8B 4D E0"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D181",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C581",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "0F B6 49 1D 83 F9",
        "suffix": "7E 14",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F B6 49 1D 83 F9",
        "actualSuffix": "7E 14"
      }
    },
    {
      "role": "extra",
      "address": {
        "kind": "va",
        "value": "0x0040D197",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C597",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "8B 4D E0 36 C6 41 1D",
        "suffix": "8B 4D F4",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D E0 36 C6 41 1D",
        "actualSuffix": "8B 4D F4"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D0E1"
      ]
    },
    {
      "label": "6.5 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D0F7"
      ]
    },
    {
      "label": "6.5 附加 0x0040D101",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D101"
      ]
    },
    {
      "label": "6.5 附加 0x0040D117",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D117"
      ]
    },
    {
      "label": "6.5 附加 0x0040D121",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D121"
      ]
    },
    {
      "label": "6.5 附加 0x0040D137",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D137"
      ]
    },
    {
      "label": "6.5 附加 0x0040D141",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D141"
      ]
    },
    {
      "label": "6.5 附加 0x0040D157",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D157"
      ]
    },
    {
      "label": "6.5 附加 0x0040D161",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D161"
      ]
    },
    {
      "label": "6.5 附加 0x0040D177",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D177"
      ]
    },
    {
      "label": "6.5 附加 0x0040D181",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D181"
      ]
    },
    {
      "label": "6.5 附加 0x0040D197",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D197"
      ]
    }
  ]
}
```

补充说明：

- 6.5 特效 194 消费者 0x0040D057 第一段：确认特效 194 后，对单位 +18h..+1Dh 六项能力逐项 cmp 本值（83 F9 ??）并 mov 本值（36 C6 41 ?? ??）；主 cmp 0x0040D0E1、主 mov 0x0040D0F7，另 10 处分布在 +19h..+1Dh。12 条签名在 6.5 各唯一，6.4/6.6 无该序列。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 风驰电掣伤害除数：代码固定值

ID: `mechanism.65.dm-constant-wind-rush-damage-divisor`；状态: `candidate`；证据: `source-reviewed`

风驰电掣的加成按百分比算出后还要再除以本值；6.5 默认 11，6.6 默认 10。改大后同特效值增伤变少。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "wind-rush-damage-divisor",
  "title": "风驰电掣伤害除数",
  "value": 11,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0041A51C",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0001991C",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 4,
      "expectedFieldBytes": "0B 00 00 00",
      "signature": {
        "prefix": "0F AF 45 FC FF 75 08 50 E8 00 00 00 00 33 D2 B9",
        "suffix": "F7 F1 01 45 08 8B 45 08",
        "prefixMask": "01 01 01 01 01 01 01 01 01 00 00 00 00 01 01 01",
        "suffixMask": null,
        "actualPrefix": "0F AF 45 FC FF 75 08 50 E8 C0 B5 00 00 33 D2 B9",
        "actualSuffix": "F7 F1 01 45 08 8B 45 08"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0041A51C"
      ]
    }
  ]
}
```

补充说明：

- 函数 6.5 0x0041A4EC（6.4 同址为 nop）、6.6 0x0041A7BA：原特效值经 0x0043F74F 折算后按 0x00425AD9 追加，再执行 xor edx,edx; mov ecx,本值; div ecx; add [ebp+8],eax；6.5 指令 0x0041A51B（立即数 0x0041A51C，文件 +0x1991C），6.6 0x0041A7EF（立即数 0x0041A7F0，文件 +0x19BF0），均为 4 字节。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 策略命中/格挡率上限：代码固定值

ID: `mechanism.65.dm-constant-strategy-hit-cap`；状态: `candidate`；证据: `source-reviewed`

策略命中或格挡的最终概率最多到这个数；默认100%。改小后策略更容易被挡住。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "strategy-hit-cap",
  "title": "策略命中/格挡率上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B9E7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003ADE7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "89 45 F0 0F B6 45 F0 3C",
        "suffix": "76 02 B0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "89 45 F0 0F B6 45 F0 3C",
        "actualSuffix": "76 02 B0"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x0043B9EB",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003ADEB",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "76 02 B0",
        "suffix": "5E 8B E5 5D C2 0C 00",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "76 02 B0",
        "actualSuffix": "5E 8B E5 5D C2 0C 00"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B9E7"
      ]
    },
    {
      "label": "6.4/6.5 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B9EB"
      ]
    }
  ]
}
```

补充说明：

- 函数片段 0x0043B8A0 末尾：概率先由命中曲线 0x0043B53A 算出，再叠加特效 27/28（策略命中）、29（格挡）、39（逆乱阴阳）；0x0043B9E6 cmp al,100，超过就 mov al,100。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 逆乱阴阳命中加成：代码固定值

ID: `mechanism.65.dm-constant-chaos-yin-yang-hit-bonus`；状态: `candidate`；证据: `source-reviewed`

拥有逆乱阴阳时，策略命中概率直接加这个百分点，最多到 100%；默认 10。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "chaos-yin-yang-hit-bonus",
  "title": "逆乱阴阳命中加成",
  "value": 10,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B9D6",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003ADD6",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "0A",
      "signature": {
        "prefix": "85 C0 74 0F 6A 64 6A",
        "suffix": "FF 75 F0 E8 AA 40 04 00",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "85 C0 74 0F 6A 64 6A",
        "actualSuffix": "FF 75 F0 E8 AA 40 04 00"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B9D6"
      ]
    }
  ]
}
```

补充说明：

- 函数片段 0x0043B8A0：确认特效 39（0x00405DBD）后执行 push 100、push 本值、push 当前概率、call 0x0047FA89（返回 min(100, 概率+本值)）；立即数 0x0043B9D6。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 特效屏蔽方向数：代码固定值

ID: `mechanism.65.dm-constant-effect-screen-directions`；状态: `candidate`；证据: `source-reviewed`

屏蔽/邻格类特技枚举几个方向：4 = 十字四格，8 = 八方格。6.4/6.5 默认 4，6.6 默认 8。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "effect-screen-directions",
  "title": "特效屏蔽方向数",
  "value": 4,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004253AA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000247AA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "04",
      "signature": {
        "prefix": "8B 45 F4 3C",
        "suffix": "73 42 8D 4D E8 51 8B 4D FC E8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 45 F4 3C",
        "actualSuffix": "73 42 8D 4D E8 51 8B 4D FC E8"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004253AA"
      ]
    }
  ]
}
```

补充说明：

- 指令 0x004253A9 cmp al, 本值；循环经 0x0041031C 取邻格并查询 0x74/0x75 通道。
- 本条是6.5精确样本的代码固定值；值单位：方向。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 特效屏蔽内层方向数：代码固定值

ID: `mechanism.65.dm-constant-screen-inner-directions`；状态: `candidate`；证据: `source-reviewed`

特效屏蔽内层判定的方向数：4 = 十字。通常要和外层方向数一起放宽，只改这个看不到效果。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "screen-inner-directions",
  "title": "特效屏蔽内层方向数",
  "value": 4,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040F1E9",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000E5E9",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "04",
      "signature": {
        "prefix": "8B 45 F4 3C",
        "suffix": "73 51 8D 4D E8 51 8B 4D FC",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 45 F4 3C",
        "actualSuffix": "73 51 8D 4D E8 51 8B 4D FC"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040F1E9"
      ]
    }
  ]
}
```

补充说明：

- 谓词 0x0040F1AC：call 0x0041031C 取邻格后循环 cmp al, 本值（指令 0x0040F1E8）。
- 本条是6.5精确样本的代码固定值；值单位：方向。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 穿越移动判定方向数：代码固定值

ID: `mechanism.65.dm-constant-pass-through-directions`；状态: `candidate`；证据: `source-reviewed`

穿越移动检查几个方向的可通行格：4 = 十字四格，8 = 八方格。三基底默认 4。6.6 同名特技为“无人之境”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "pass-through-directions",
  "title": "穿越移动判定方向数",
  "value": 4,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00437D8A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003718A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "04",
      "signature": {
        "prefix": "8B 45 F0 3C",
        "suffix": "73 47 50 FF 75 F4 E8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 45 F0 3C",
        "actualSuffix": "73 47 50 FF 75 F4 E8"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00437D8A"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x00437D59：按方向循环 call 0x004359F5 取邻格、0x00435884 查单位、0x0042E2B7 判定通行；循环 cmp 本值（6.4 0x00437DB8、6.5 0x00437D89、6.6 0x00437D9A）。
- 本条是6.5精确样本的代码固定值；值单位：方向。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 状态强化/周围能力范围：代码固定值

ID: `mechanism.65.dm-constant-aura-range`；状态: `candidate`；证据: `source-reviewed`

周围能力枚举几格：9 = 自身 + 八方，4 = 自身 + 三方向。6.4/6.5 默认 9，6.6 默认 4。6.6 同名特技为“兼济天下”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "aura-range",
  "title": "状态强化/周围能力范围",
  "value": 9,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00422151",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00021551",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "09",
      "signature": {
        "prefix": "FF 45 F8 8B 45 F8 3C",
        "suffix": "73 57 85 C0 75 05 8B",
        "prefixMask": null,
        "suffixMask": "01 00 01 01 01 01 01",
        "actualPrefix": "FF 45 F8 8B 45 F8 3C",
        "actualSuffix": "73 57 85 C0 75 05 8B"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00422151"
      ]
    }
  ]
}
```

补充说明：

- 循环 0x0042214A：FF 45 F8（inc [ebp-8]）、8B 45 F8（mov eax,[ebp-8]）、3C 本值（cmp al,imm）、73 相对跳转、85 C0 75 05；索引 0 单独表示当前单位自身，其余索引映射方向表。签名必须包含循环头，只写 cmp 后缀会在异引擎上误匹配到其他循环上界。
- 本条是6.5精确样本的代码固定值；值单位：格。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 连击固定增伤：代码固定值

ID: `mechanism.65.dm-constant-combo-damage-bonus`；状态: `candidate`；证据: `source-reviewed`

强化连击/连击上限类特效触发后，连击伤害不再逐次衰减，并在原伤害上额外加这个固定百分比；0 = 只不衰减，10 = 每次连击多 10%。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "combo-damage-bonus",
  "title": "连击固定增伤",
  "value": 0,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004E319E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000B499E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "00",
      "signature": {
        "prefix": "0F AF 45 FC 83 C0",
        "suffix": "FF 75 08 50 E8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F AF 45 FC 83 C0",
        "actualSuffix": "FF 75 08 50 E8"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004E319E"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x004E313C（6.4 同址为空）：确认特效后执行 imul eax,[ebp-4]; add eax,本值（6.5/6.6 指令 0x004E319C，字节 0F AF 45 FC 83 C0 ??），再按百分比追加。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 逆境减伤最大比例：代码固定值

ID: `mechanism.65.dm-constant-adversity-reduction-cap`；状态: `candidate`；证据: `source-reviewed`

生命越低减伤越高；这里限制最多按已损失生命的多少比例减伤。80 = 最多减 80%。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "adversity-reduction-cap",
  "title": "逆境减伤最大比例",
  "value": 80,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00449093",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00048493",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "50",
      "signature": {
        "prefix": "2B 45 FC 6B C0",
        "suffix": "33 D2 F7 F9 85 C0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "2B 45 FC 6B C0",
        "actualSuffix": "33 D2 F7 F9 85 C0"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00449093"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x0044904E：确认特效后算 (最大HP-当前HP)×本值/最大HP，再按该比例减少伤害；6.5/6.6 指令 0x00449091 字节 6B C0 50。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 偷袭攻击每档增伤：代码固定值

ID: `mechanism.65.dm-constant-sneak-attack-step`；状态: `candidate`；证据: `source-reviewed`

侧击按 1 档、背击按 2 档，每档增加这个百分比；25 = 侧击 +25%、背击 +50%。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "sneak-attack-step",
  "title": "偷袭攻击每档增伤",
  "value": 25,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004D2767",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000A3F67",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "19",
      "signature": {
        "prefix": "B0 02 6B C0",
        "suffix": "50 FF 75 10 E8 68 33 F5 FF 01",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "B0 02 6B C0",
        "actualSuffix": "50 FF 75 10 E8 68 33 F5 FF 01"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004D2767"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x004D2700：按方向关系得到 0/1/2 档后 imul eax,本值（6.5/6.6 指令 0x004D2765，字节 6B C0 19），再按百分比追加；6.4 偷袭攻击走另一套按特效值的公式，不适用。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 固定值基础加成：代码固定值

ID: `mechanism.65.dm-constant-fixed-damage-basis`；状态: `candidate`；证据: `source-reviewed`

特效值为 1 时走固定值模式：加成 = 单位等级÷2 + 本值；增伤和减伤共用。6.5 默认 10，6.6 默认 15。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "fixed-damage-basis",
  "title": "固定值基础加成",
  "value": 10,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00448F8B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0004838B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "0A",
      "signature": {
        "prefix": "8B 45 FC D1 E8 90 83 C0",
        "suffix": "03 45 08 50 6A 00",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 45 FC D1 E8 90 83 C0",
        "actualSuffix": "03 45 08 50 6A 00"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x00448FB7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000483B7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "0A",
      "signature": {
        "prefix": "8B 45 FC D1 E8 90 83 C0",
        "suffix": "8B 4D F8 2B C8 83 F9 00",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 45 FC D1 E8 90 83 C0",
        "actualSuffix": "8B 4D F8 2B C8 83 F9 00"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00448F8B"
      ]
    },
    {
      "label": "6.5/6.6 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00448FB7"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x00448F53：确认增伤/减伤特效后，若特效值为 1 则取单位等级（单位+0x2C）÷2 再加本值；6.5 指令 0x00448F89/0x00448FB5 字节 83 C0 0A，6.6 同址 83 C0 0F。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 策伤保底追加比例：代码固定值

ID: `mechanism.65.dm-constant-strategy-floor-bonus`；状态: `candidate`；证据: `source-reviewed`

策略伤害已经高于保底（或低于限伤）时，额外增加/扣减的百分比；默认 20%。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "strategy-floor-bonus",
  "title": "策伤保底追加比例",
  "value": 20,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043D3EA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003C7EA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "14",
      "signature": {
        "prefix": "39 45 08 72 12 6A",
        "suffix": "FF 75 08 E8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "39 45 08 72 12 6A",
        "actualSuffix": "FF 75 08 E8"
      }
    },
    {
      "role": "paired",
      "address": {
        "kind": "va",
        "value": "0x0043D43A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003C83A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "14",
      "signature": {
        "prefix": "39 45 08 73 10 6A",
        "suffix": "FF 75 08 E8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "39 45 08 73 10 6A",
        "actualSuffix": "FF 75 08 E8"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043D3EA"
      ]
    },
    {
      "label": "6.5 成对",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043D43A"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x0043D3AE：保底分支 0x0043D3E9、限伤分支 0x0043D439 均 push 本值（字节 6A 14），再按 伤害×本值/100 增减；6.4/6.6 同址无这条公式。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 趁虚攻击虚弱阈值：代码固定值

ID: `mechanism.65.dm-constant-exploit-weakness-threshold`；状态: `candidate`；证据: `source-reviewed`

统计 6 项能力中数值低于本阈值的项数，每低一项按特效值追加伤害；默认 3。6.5 同名特技为“落井下石”。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "exploit-weakness-threshold",
  "title": "趁虚攻击虚弱阈值",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043EA40",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003DE40",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "83 FA 06 73 0D 8B 4D 0C 80 7C 11 18",
        "suffix": "7D 01 40 EB",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 FA 06 73 0D 8B 4D 0C 80 7C 11 18",
        "actualSuffix": "7D 01 40 EB"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043EA40"
      ]
    }
  ]
}
```

补充说明：

- 函数 0x0043EA00（6.5 为 0x0043EA12）：循环 6 项能力，`cmp byte [单位+18h+索引],本值`，低于就计数，再 imul 特效值；6.5 立即数 0x0043EA40（文件 +0x3DE40），6.6 0x0043EA31（文件 +0x3DE31）。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 吸收金钱获得倍率：代码固定值

ID: `mechanism.65.dm-constant-money-absorb-multiplier`；状态: `candidate`；证据: `source-reviewed`

吸收金钱结算时，按本次累计伤害 × 本值 计算金钱；6.4 默认 2 倍，6.5/6.6 默认 1 倍。改 0 就不结算金钱。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "money-absorb-multiplier",
  "title": "吸收金钱获得倍率",
  "value": 1,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00406BFF",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00005FFF",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "01",
      "signature": {
        "prefix": "A1 BD E8 48 00 6B C0",
        "suffix": "BA 7C 07 4B 00 80 F9 02",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "A1 BD E8 48 00 6B C0",
        "actualSuffix": "BA 7C 07 4B 00 80 F9 02"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00406BFF"
      ]
    }
  ]
}
```

补充说明：

- 特效 21 消费者 0x00406B3C：读累计伤害全局 0x0048E8BD 后执行 imul eax,本值（指令 0x00406BFD，字节 6B C0 ??），再按阵营结算全局金钱 0x004B077C（上限 999999）；三基底同址，6.4 立即数 2，6.5/6.6 为 1。
- 本条是6.5精确样本的代码固定值；值单位：倍。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 神锋沥辉保底加成：代码固定值

ID: `mechanism.65.dm-constant-fengfeng-floor-bonus`；状态: `candidate`；证据: `source-reviewed`

拥有神锋沥辉（6.5 同名特技为“削铁如泥”）时，按比例追加伤害的保底百分点；6.5 默认 10，6.6 默认 6。改 0 就只按计算值加成。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "fengfeng-floor-bonus",
  "title": "神锋沥辉保底加成",
  "value": 10,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0042426A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0002366A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "0A",
      "signature": {
        "prefix": "6A 00 E8 00 00 00 00 83 C0",
        "suffix": "50 E8 00 00 00 00 01 45 08",
        "prefixMask": "01 00 01 00 00 00 00 01 01",
        "suffixMask": "01 01 00 00 00 00 01 01 01",
        "actualPrefix": "6A 14 E8 6C 78 FE FF 83 C0",
        "actualSuffix": "50 E8 68 18 00 00 01 45 08"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0042426A"
      ]
    }
  ]
}
```

补充说明：

- 特效 111 消费者 0x0042423D（6.4 同址为 nop）：读表值后 push 100/20、call 0x0040BAD4 除以 100/20，再 add eax,本值，最后按百分比追加伤害；6.5 字节 83 C0 0A，6.6 为 83 C0 06，前后 call 位移在签名里用掩码忽略。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 商店卖出价格比例分子：代码固定值

ID: `mechanism.65.dm-constant-shop-sell-price-numerator`；状态: `candidate`；证据: `source-reviewed`

卖出价 = 买入价 × 本值 / 4；默认 3，即卖出价为买入价的 75%。分母固定 4，改本值可整体调整卖出比例。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "shop-sell-price-numerator",
  "title": "商店卖出价格比例分子",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040B48D",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000A88D",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "6B C0 64 6B C0",
        "suffix": "99 83 E2 03 03 C2 C1 F8 02",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "6B C0 64 6B C0",
        "actualSuffix": "99 83 E2 03 03 C2 C1 F8 02"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040B48D"
      ]
    }
  ]
}
```

补充说明：

- 卖出价函数 0x0040B477：读道具价格字节 +12h 后 imul 100、imul 本值，再执行 cdq/and edx,3/add/sar 2（除以 4）；立即数 0x0040B48D（文件 +0xA88D）。三基底与信奈同址同值；本行只改分子，分母由 0x0040B490 与 0x0040B495 两处固定为 4。
- 本条是6.5精确样本的代码固定值；值单位：倍（分母4）。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 命中率上限：代码固定值

ID: `mechanism.65.dm-constant-hit-curve-cap`；状态: `candidate`；证据: `source-reviewed`

命中率曲线最高只能到本值；三基底默认 100。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-cap",
  "title": "命中率上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B54A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A94A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "39 55 08 72 04 B0",
        "suffix": "EB 66 8B 55 08 3B",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "39 55 08 72 04 B0",
        "actualSuffix": "EB 66 8B 55 08 3B"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B54A"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数 6.4 0x0043B50C、6.5/6.6 0x0043B53A：39 55 08 72 04 B0 64；立即数 6.4 0x0043B51C、6.5/6.6 0x0043B54A。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 命中率曲线·高段基础值

ID: `mechanism.65.dm-constant-hit-curve-high-base`；状态: `candidate`；证据: `source-reviewed`

攻方能力是守方 1～2 倍时，高段从本值起算；默认 90。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-high-base",
  "title": "高段基础值",
  "value": 90,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B56B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A96B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "5A",
      "signature": {
        "prefix": "33 D2 F7 75 0C 83 C0",
        "suffix": "EB 45 8B 4D 0C",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "33 D2 F7 75 0C 83 C0",
        "actualSuffix": "EB 45 8B 4D 0C"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B56B"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数：83 C0 5A；6.4 立即数 0x0043B53D，6.5/6.6 0x0043B56B。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 命中率曲线·高段每点系数

ID: `mechanism.65.dm-constant-hit-curve-high-coef`；状态: `candidate`；证据: `source-reviewed`

高段能力每高 1 点加本值/D；默认 10。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-high-coef",
  "title": "高段每点系数",
  "value": 10,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B563",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A963",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "0A",
      "signature": {
        "prefix": "83 C4 08 6B C0",
        "suffix": "33 D2 F7 75 0C",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 C4 08 6B C0",
        "actualSuffix": "33 D2 F7 75 0C"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B563"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数：6B C0 0A；6.4 立即数 0x0043B535，6.5/6.6 0x0043B563。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 中段基础值：代码固定值

ID: `mechanism.65.dm-constant-hit-curve-mid-base`；状态: `candidate`；证据: `source-reviewed`

攻方能力是守方一半到一倍时，中段从本值起算；默认 60。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-mid-base",
  "title": "中段基础值",
  "value": 60,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B58C",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A98C",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "3C",
      "signature": {
        "prefix": "33 D2 F7 F1 83 C0",
        "suffix": "EB 24 8B 45 0C",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "33 D2 F7 F1 83 C0",
        "actualSuffix": "EB 24 8B 45 0C"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B58C"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数：83 C0 3C；6.4 立即数 0x0043B55E，6.5/6.6 0x0043B58C。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 中段每点系数：代码固定值

ID: `mechanism.65.dm-constant-hit-curve-mid-coef`；状态: `candidate`；证据: `source-reviewed`

中段每高 1 点加本值/(D/2)；默认 30。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-mid-coef",
  "title": "中段每点系数",
  "value": 30,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B584",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A984",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "1E",
      "signature": {
        "prefix": "83 C4 08 6B C0",
        "suffix": "59 33 D2 F7 F1",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 C4 08 6B C0",
        "actualSuffix": "59 33 D2 F7 F1"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B584"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数：6B C0 1E；6.4 立即数 0x0043B556，6.5/6.6 0x0043B584。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 低段守方除数：代码固定值

ID: `mechanism.65.dm-constant-hit-curve-low-divisor`；状态: `candidate`；证据: `source-reviewed`

攻方低于守方一半时，先按守方能力除以本值作为低段基准；默认 3。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-low-divisor",
  "title": "低段守方除数",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B595",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A995",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 4,
      "expectedFieldBytes": "03 00 00 00",
      "signature": {
        "prefix": "33 D2 B9",
        "suffix": "F7 F1 50 50 FF",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "33 D2 B9",
        "actualSuffix": "F7 F1 50 50 FF"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B595"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数：33 D2 B9 03 00 00 00 F7 F1；6.4 立即数 0x0043B567，6.5/6.6 0x0043B595。
- 本条是6.5精确样本的代码固定值；值单位：倍。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 命中率曲线·低段基础值

ID: `mechanism.65.dm-constant-hit-curve-low-base`；状态: `candidate`；证据: `source-reviewed`

低段起点；默认 30。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-low-base",
  "title": "低段基础值",
  "value": 30,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B5B2",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A9B2",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "1E",
      "signature": {
        "prefix": "59 F7 F1 83 C0",
        "suffix": "5D C2 08 00 90",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "59 F7 F1 83 C0",
        "actualSuffix": "5D C2 08 00 90"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B5B2"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数：83 C0 1E；6.4 立即数 0x0043B584，6.5/6.6 0x0043B5B2。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 命中率曲线·低段每点系数

ID: `mechanism.65.dm-constant-hit-curve-low-coef`；状态: `candidate`；证据: `source-reviewed`

低段每高 1 点加本值/(D/除数)；默认 30。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-curve-low-coef",
  "title": "低段每点系数",
  "value": 30,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B5AA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A9AA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "1E",
      "signature": {
        "prefix": "83 C4 08 6B C0",
        "suffix": "33 D2 59 F7 F1",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 C4 08 6B C0",
        "actualSuffix": "33 D2 59 F7 F1"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B5AA"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数：6B C0 1E；6.4 立即数 0x0043B57C，6.5/6.6 0x0043B5AA。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 最多命中判定次数：代码固定值

ID: `mechanism.65.dm-constant-hit-retry-count`；状态: `candidate`；证据: `source-reviewed`

6.4/6.5 高命中未打中时最多再判几次；默认 2。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-retry-count",
  "title": "最多命中判定次数",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B50A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A90A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "80 7D F0",
        "suffix": "73 27 FF 75",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "80 7D F0",
        "actualSuffix": "73 27 FF 75"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B50A"
      ]
    }
  ]
}
```

补充说明：

- 6.4 80 7D F8 02 73 1A，立即数 0x0043B4E9；6.5 80 7D F0 02 73 27，立即数 0x0043B50A。
- 本条是6.5精确样本的代码固定值；值单位：次。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 二次判定触发阈值：代码固定值

ID: `mechanism.65.dm-constant-hit-retry-threshold`；状态: `candidate`；证据: `source-reviewed`

首次命中率达到本值才会补判；默认 85。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-retry-threshold",
  "title": "二次判定触发阈值",
  "value": 85,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B528",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A928",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "55",
      "signature": {
        "prefix": "83 7D F4",
        "suffix": "72 09 83 6D",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 7D F4",
        "actualSuffix": "72 09 83 6D"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B528"
      ]
    }
  ]
}
```

补充说明：

- 6.4 83 7D FC 55 72 06，立即数 0x0043B4FD；6.5 83 7D F4 55 72 09，立即数 0x0043B528。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 二次判定命中扣减：代码固定值

ID: `mechanism.65.dm-constant-hit-retry-deduction`；状态: `candidate`；证据: `source-reviewed`

补判时命中率扣本值；默认 10。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "hit-retry-deduction",
  "title": "二次判定命中扣减",
  "value": 10,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0043B52E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0003A92E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "0A",
      "signature": {
        "prefix": "83 6D F4",
        "suffix": "FE 45 F0 EB D3",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 6D F4",
        "actualSuffix": "FE 45 F0 EB D3"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0043B52E"
      ]
    }
  ]
}
```

补充说明：

- 6.4 83 6D FC 0A EB DD，立即数 0x0043B503；6.5 83 6D F4 0A FE 45 F0，立即数 0x0043B52E。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 满发动率所需倍数：代码固定值

ID: `mechanism.65.dm-constant-rate-curve-full-multiplier`；状态: `candidate`；证据: `source-reviewed`

攻方能力达到守方本值倍时直接满发动；默认 3。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "rate-curve-full-multiplier",
  "title": "满发动率所需倍数",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405D14",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00005114",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "8B 4D 08 6B C9",
        "suffix": "39 4D 0C 72 04",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B 4D 08 6B C9",
        "actualSuffix": "39 4D 0C 72 04"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405D14"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数 0x00405D0A：8B 4D 08 6B C9 03；立即数 0x00405D14。
- 本条是6.5精确样本的代码固定值；值单位：倍。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 发动率上限：代码固定值

ID: `mechanism.65.dm-constant-rate-curve-cap`；状态: `candidate`；证据: `source-reviewed`

暴击/连击率最高到本值；默认 100。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "rate-curve-cap",
  "title": "发动率上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405D1B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000511B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "39 4D 0C 72 04 B0",
        "suffix": "EB 37 8B 4D 08",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "39 4D 0C 72 04 B0",
        "actualSuffix": "EB 37 8B 4D 08"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405D1B"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数 0x00405D0A：39 4D 0C 72 04 B0 64；立即数 0x00405D1B。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 发动率曲线·高段每点系数

ID: `mechanism.65.dm-constant-rate-curve-high-coef`；状态: `candidate`；证据: `source-reviewed`

2～3 倍区间每高 1 点加本值/D；默认 80。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "rate-curve-high-coef",
  "title": "高段每点系数",
  "value": 80,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405D2F",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000512F",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "50",
      "signature": {
        "prefix": "2B C1 6B C0",
        "suffix": "33 D2 F7 75 08",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "2B C1 6B C0",
        "actualSuffix": "33 D2 F7 75 08"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405D2F"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数 0x00405D0A：2B C1 6B C0 50；立即数 0x00405D2F。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 发动率曲线·高段基础值

ID: `mechanism.65.dm-constant-rate-curve-high-base`；状态: `candidate`；证据: `source-reviewed`

2～3 倍区间起点；默认 20。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "rate-curve-high-base",
  "title": "高段基础值",
  "value": 20,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405D37",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00005137",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "14",
      "signature": {
        "prefix": "33 D2 F7 75 08 83 C0",
        "suffix": "EB 1B 8B 45 0C",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "33 D2 F7 75 08 83 C0",
        "actualSuffix": "EB 1B 8B 45 0C"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405D37"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数 0x00405D0A：83 C0 14；立即数 0x00405D37。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 发动率曲线·低段每点系数

ID: `mechanism.65.dm-constant-rate-curve-low-coef`；状态: `candidate`；证据: `source-reviewed`

1～2 倍区间每高 1 点加本值/D；默认 18。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "rate-curve-low-coef",
  "title": "低段每点系数",
  "value": 18,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405D47",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00005147",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "12",
      "signature": {
        "prefix": "2B 45 08 6B C0",
        "suffix": "33 D2 F7 75 08",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "2B 45 08 6B C0",
        "actualSuffix": "33 D2 F7 75 08"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405D47"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数 0x00405D0A：2B 45 08 6B C0 12；立即数 0x00405D47。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 发动率曲线·低段基础值

ID: `mechanism.65.dm-constant-rate-curve-low-base`；状态: `candidate`；证据: `source-reviewed`

1～2 倍区间起点；默认 2。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "rate-curve-low-base",
  "title": "低段基础值",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405D4F",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000514F",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "33 D2 F7 75 08 83 C0",
        "suffix": "EB 03 33 C0 40",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "33 D2 F7 75 08 83 C0",
        "actualSuffix": "EB 03 33 C0 40"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405D4F"
      ]
    }
  ]
}
```

补充说明：

- 曲线函数 0x00405D0A：83 C0 02；立即数 0x00405D4F。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 物理暴击率上限：代码固定值

ID: `mechanism.65.dm-constant-physical-crit-cap`；状态: `candidate`；证据: `source-reviewed`

物理暴击率最高到本值；默认 100。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "physical-crit-cap",
  "title": "物理暴击率上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405ED7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000052D7",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "89 45 DC 83 F8",
        "suffix": "77 10",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "89 45 DC 83 F8",
        "actualSuffix": "77 10"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405ED7"
      ]
    }
  ]
}
```

补充说明：

- 物理暴击 0x00405E80：83 F8 64 77 10；立即数 0x00405ED7。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 物理暴击集气池：代码固定值

ID: `mechanism.65.dm-constant-physical-crit-pool`；状态: `candidate`；证据: `source-reviewed`

物理暴击判定进入的集气池编号；6.4 为 0，6.5/6.6 为 2。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "physical-crit-pool",
  "title": "物理暴击集气池",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00405EDB",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000052DB",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "77 10 6A",
        "suffix": "50 E8 C6 28 02 00 85 C0 74 3E",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "77 10 6A",
        "actualSuffix": "50 E8 C6 28 02 00 85 C0 74 3E"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00405EDB"
      ]
    }
  ]
}
```

补充说明：

- 物理暴击 0x00405E80：77 10 6A 00/02 50 E8 ... 85 C0 74 3E；6.4 调用 0x00437896，6.5/6.6 调用 0x004287A8；立即数 0x00405EDB。
- 本条是6.5精确样本的代码固定值；值单位：池号。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 策略暴击率上限：代码固定值

ID: `mechanism.65.dm-constant-strategy-crit-cap`；状态: `candidate`；证据: `source-reviewed`

策略暴击率最高到本值；默认 100。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "strategy-crit-cap",
  "title": "策略暴击率上限",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040CAA5",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000BEA5",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "50 83 F8",
        "suffix": "77 10",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "50 83 F8",
        "actualSuffix": "77 10"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040CAA5"
      ]
    }
  ]
}
```

补充说明：

- 策略暴击 0x0040CA68：6.4 89 45 F8 83 F8 64 77 10；6.5/6.6 50 83 F8 64 77 10；立即数 0x0040CAD8 / 0x0040CAA5。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 策略暴击集气池：代码固定值

ID: `mechanism.65.dm-constant-strategy-crit-pool`；状态: `candidate`；证据: `source-reviewed`

策略暴击判定进入的集气池编号；6.4 为 0，6.5/6.6 为 18。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "strategy-crit-pool",
  "title": "策略暴击集气池",
  "value": 18,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040CAA9",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000BEA9",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "12",
      "signature": {
        "prefix": "77 10 6A",
        "suffix": "50 E8 F8 BC 01 00 85 C0 74 1D",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "77 10 6A",
        "actualSuffix": "50 E8 F8 BC 01 00 85 C0 74 1D"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040CAA9"
      ]
    }
  ]
}
```

补充说明：

- 策略暴击 0x0040CA68：77 10 6A 00/12 50 E8 ... 85 C0 74 1D；6.4 调用 0x00437896，6.5/6.6 调用 0x004287A8；立即数 0x0040CADC / 0x0040CAA9。
- 本条是6.5精确样本的代码固定值；值单位：池号。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 连击集气池：代码固定值

ID: `mechanism.65.dm-constant-combo-pool`；状态: `candidate`；证据: `source-reviewed`

连击判定进入的集气池编号；三基底默认 0。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "combo-pool",
  "title": "连击集气池",
  "value": 0,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040612E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000552E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "00",
      "signature": {
        "prefix": "E8 B3 DF 0D 00 6A",
        "suffix": "50 E8 73 26 02 00 85 C0 75 03",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "E8 B3 DF 0D 00 6A",
        "actualSuffix": "50 E8 73 26 02 00 85 C0 75 03"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5/6.6",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040612E"
      ]
    }
  ]
}
```

补充说明：

- 连击 0x004060D2：6.4 E8 8C FB FF FF 6A 00 50 E8 61 17 03 00 85 C0 75 03；6.5/6.6 E8 B3 DF 0D 00 6A 00 50 E8 73 26 02 00 85 C0 75 03；立即数 0x0040612E。
- 本条是6.5精确样本的代码固定值；值单位：池号。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 个人经验·击杀固定加成：代码固定值

ID: `mechanism.65.dm-constant-personal-exp-kill-flat`；状态: `candidate`；证据: `source-reviewed`

击杀指定目标时，击杀经验改为固定加成本值；默认 48。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "personal-exp-kill-flat",
  "title": "个人经验·击杀固定加成",
  "value": 48,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00403824",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002C24",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "30",
      "signature": {
        "prefix": "75 06 83 45 FC",
        "suffix": "EB 19 8B 45 F4",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "75 06 83 45 FC",
        "actualSuffix": "EB 19 8B 45 F4"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00403824"
      ]
    }
  ]
}
```

补充说明：

- 个人经验 0x004037A3 击杀分支：6.4/6.5 指令 0x00403821 add dword [ebp-4],30h（立即数 0x00403824）；6.6 指令 0x0040381B（立即数 0x0040381E）。比较来源 0x00406604 读取 word [0x492F90+0x3D06]。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 个人经验·击杀经验分子：代码固定值

ID: `mechanism.65.dm-constant-personal-exp-kill-ratio-num`；状态: `candidate`；证据: `source-reviewed`

击杀非指定目标时，额外经验 = 本值 ÷（攻方等级−守方等级 + 除数偏移）；等级差为负按 0 算。默认 64。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "personal-exp-kill-ratio-num",
  "title": "个人经验·击杀经验分子",
  "value": 64,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040383A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002C3A",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "40",
      "signature": {
        "prefix": "8B C8 33 D2 B0",
        "suffix": "F7 F1 01 45 FC",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "8B C8 33 D2 B0",
        "actualSuffix": "F7 F1 01 45 FC"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040383A"
      ]
    }
  ]
}
```

补充说明：

- 个人经验 0x004037A3：6.4/6.5 指令 0x00403839 mov al,40h（立即数 0x0040383A）；6.6 指令 0x00403832（立即数 0x00403833）；随后 div ecx。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 个人经验·击杀除数偏移：代码固定值

ID: `mechanism.65.dm-constant-personal-exp-kill-ratio-offset`；状态: `candidate`；证据: `source-reviewed`

击杀经验的除数 = max(攻方等级−守方等级,0) + 本值；默认 2。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "personal-exp-kill-ratio-offset",
  "title": "个人经验·击杀除数偏移",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00403834",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002C34",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "33 C0 04",
        "suffix": "8B C8 33 D2 B0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "33 C0 04",
        "actualSuffix": "8B C8 33 D2 B0"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00403834"
      ]
    }
  ]
}
```

补充说明：

- 个人经验 0x004037A3：6.4/6.5 指令 0x00403833 add al,2（立即数 0x00403834）；6.6 指令 0x0040382D（立即数 0x0040382E）。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 个人经验基础值：代码固定值

ID: `mechanism.65.dm-constant-personal-exp-base`；状态: `candidate`；证据: `source-reviewed`

个人经验基础值：基础经验 = 2×等级差 + 本值；默认 6。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "personal-exp-base",
  "title": "个人经验基础值",
  "value": 6,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00403855",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002C55",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "06",
      "signature": {
        "prefix": "B0 2F 8D 4C 00",
        "suffix": "01 4D FC 8B 45 F8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "B0 2F 8D 4C 00",
        "actualSuffix": "01 4D FC 8B 45 F8"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00403855"
      ]
    }
  ]
}
```

补充说明：

- 个人经验 0x004037A3：三基底同址 0x00403852 lea ecx,[eax+eax+6]，位移立即数 0x00403855。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 经验倍率基础值：代码固定值

ID: `mechanism.65.dm-constant-exp-multiplier-base`；状态: `candidate`；证据: `source-reviewed`

经验倍率 = (角色第 8 项基础能力 + 本值) / 100；默认 100。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "exp-multiplier-base",
  "title": "经验倍率基础值",
  "value": 100,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00407FB9",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x000073B9",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "64",
      "signature": {
        "prefix": "0F B6 C0 83 C0",
        "suffix": "5D C3",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "0F B6 C0 83 C0",
        "actualSuffix": "5D C3"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00407FB9"
      ]
    }
  ]
}
```

补充说明：

- 经验倍率函数 0x00407FAA：push 8; call 0x00407C35（6.6 为 0x00407C29）; movzx eax,al; add eax,64h（立即数 0x00407FB9）；三基底同址。
- 本条是6.5精确样本的代码固定值；值单位：%。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 武器经验基础值：代码固定值

ID: `mechanism.65.dm-constant-weapon-exp-base`；状态: `candidate`；证据: `source-reviewed`

武器经验基础值：造成伤害时每次加多少；6.5 默认 2，6.4/6.6 默认 3。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "weapon-exp-base",
  "title": "武器经验基础值",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004038FA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002CFA",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "83 BC 88 84 00 00 00 00 75 0A 83 BC 88 54 02 00 00 00 74 1D B1",
        "suffix": "8B 45 F4 3B 45 F0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 BC 88 84 00 00 00 00 75 0A 83 BC 88 54 02 00 00 00 74 1D B1",
        "actualSuffix": "8B 45 F4 3B 45 F0"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004038FA"
      ]
    }
  ]
}
```

补充说明：

- 武器经验 0x00403870：6.4/6.5 指令 0x004038F9 mov cl,2；6.6 同址 mov cl,3；立即数 0x004038FA，随后按等级差 −1、暴击 +1。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 武器经验无伤害值：代码固定值

ID: `mechanism.65.dm-constant-weapon-exp-no-damage`；状态: `candidate`；证据: `source-reviewed`

没有造成 HP/MP 伤害时，武器经验直接取本值；6.4/6.5 默认 2，6.6 默认 1。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "weapon-exp-no-damage",
  "title": "武器经验无伤害值",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00403919",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002D19",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "EB 04 C6 45 FC",
        "suffix": "8B 45 F8 8B 48 08",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "EB 04 C6 45 FC",
        "actualSuffix": "8B 45 F8 8B 48 08"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00403919"
      ]
    }
  ]
}
```

补充说明：

- 武器经验 0x00403870：无伤害分支 0x00403916 mov byte [ebp-4],本值（立即数 0x00403919）。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 防具经验基础值：代码固定值

ID: `mechanism.65.dm-constant-armor-exp-base`；状态: `candidate`；证据: `source-reviewed`

每件防具的经验基础值；6.4/6.5 默认 3，6.6 默认 4。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "armor-exp-base",
  "title": "防具经验基础值",
  "value": 3,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00403A8E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002E8E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "03",
      "signature": {
        "prefix": "55 8B EC 6A",
        "suffix": "51 83 EC 10 E8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "55 8B EC 6A",
        "actualSuffix": "51 83 EC 10 E8"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00403A8E"
      ]
    }
  ]
}
```

补充说明：

- 防具经验 0x00403A8A：入口 0x00403A8D push 本值（立即数 0x00403A8E）；随后按等级差 −1、无伤害扣减。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 防具经验无伤害扣减：代码固定值

ID: `mechanism.65.dm-constant-armor-exp-no-damage`；状态: `candidate`；证据: `source-reviewed`

没有造成 HP/MP 伤害时从基础上扣多少；6.4 默认 1，6.5 默认 2，6.6 默认 3。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "armor-exp-no-damage",
  "title": "防具经验无伤害扣减",
  "value": 2,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00403AFB",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00002EFB",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "02",
      "signature": {
        "prefix": "EB 04 83 6D FC",
        "suffix": "8B 45 F8 40 50",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "EB 04 83 6D FC",
        "actualSuffix": "8B 45 F8 40 50"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00403AFB"
      ]
    }
  ]
}
```

补充说明：

- 防具经验 0x00403A8A：无伤害分支 0x00403AF8 sub dword [ebp-4],本值（立即数 0x00403AFB）。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 角色升级·最大等级：代码固定值

ID: `mechanism.65.dm-constant-char-exp-max-level`；状态: `candidate`；证据: `source-reviewed`

角色经验结算的最高等级；6.4 默认 80，6.5 默认 60，6.6 默认 99。部分改版基底设为 100。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "char-exp-max-level",
  "title": "角色升级·最大等级",
  "value": 60,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x004088D3",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00007CD3",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "3C",
      "signature": {
        "prefix": "55 8B EC 33 C0 B0",
        "suffix": "E9 1E 49 00 00",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "55 8B EC 33 C0 B0",
        "actualSuffix": "E9 1E 49 00 00"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x004088D3"
      ]
    }
  ]
}
```

补充说明：

- 角色经验 0x004088CD：6.4/6.6 在 0x004088D2 mov al,本值；6.5 同址 mov al,本值 后跳 0x0040D1F7。立即数 0x004088D3。
- 本条是6.5精确样本的代码固定值；值单位：级。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 角色升级·等级分段（6.5）：代码固定值

ID: `mechanism.65.dm-constant-char-exp-band-65`；状态: `candidate`；证据: `source-reviewed`

6.5 角色升级经验的等级分段：每多少级提高一档；默认 20。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "char-exp-band-65",
  "title": "角色升级·等级分段（6.5）",
  "value": 20,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040D226",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C626",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 4,
      "expectedFieldBytes": "14 00 00 00",
      "signature": {
        "prefix": "E8 AB 93 FF FF B9",
        "suffix": "31 D2 F7 F1 83 F8 03",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "E8 AB 93 FF FF B9",
        "actualSuffix": "31 D2 F7 F1 83 F8 03"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D226"
      ]
    }
  ]
}
```

补充说明：

- 6.5 阈值函数 0x0040D21D：0x0040D225 mov ecx,本值（4 字节立即数 0x0040D226），随后用等级除以本值。
- 本条是6.5精确样本的代码固定值；值单位：级。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 角色升级·每档增量（6.5）：代码固定值

ID: `mechanism.65.dm-constant-char-exp-step-65`；状态: `candidate`；证据: `source-reviewed`

6.5 角色升级经验每档增量：阈值 = (min(等级/分段,3)+3)×本值；默认 50。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "char-exp-step-65",
  "title": "角色升级·每档增量（6.5）",
  "value": 50,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040D23D",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000C63D",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "32",
      "signature": {
        "prefix": "83 C0 03 6B C0",
        "suffix": "5D C3",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "83 C0 03 6B C0",
        "actualSuffix": "5D C3"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040D23D"
      ]
    }
  ]
}
```

补充说明：

- 6.5 阈值函数 0x0040D21D：0x0040D23B imul eax,本值（立即数 0x0040D23D）。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 装备升级·宝物经验阈值：代码固定值

ID: `mechanism.65.dm-constant-equip-exp-threshold-special`；状态: `candidate`；证据: `source-reviewed`

带宝物标记的武器/防具每升一级所需经验；三基底默认 200。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "equip-exp-threshold-special",
  "title": "装备升级·宝物经验阈值",
  "value": 200,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00408319",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00007719",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "C8",
      "signature": {
        "prefix": "33 D2 85 C0 74 05 80 C2",
        "suffix": "EB 03",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "33 D2 85 C0 74 05 80 C2",
        "actualSuffix": "EB 03"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00408319"
      ]
    }
  ]
}
```

补充说明：

- 装备经验 0x004082DD：0x00408317 add dl,本值（立即数 0x00408319）；宝物判定 0x0040B4E1 读道具记录 +0x11 的 bit0。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 装备升级·普通经验阈值：代码固定值

ID: `mechanism.65.dm-constant-equip-exp-threshold-normal`；状态: `candidate`；证据: `source-reviewed`

普通武器/防具每升一级所需经验；6.4/6.6 默认 100，6.5 默认 150。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "equip-exp-threshold-normal",
  "title": "装备升级·普通经验阈值",
  "value": 150,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040831E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000771E",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "96",
      "signature": {
        "prefix": "EB 03 80 C2",
        "suffix": "89 55 E8",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "EB 03 80 C2",
        "actualSuffix": "89 55 E8"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040831E"
      ]
    }
  ]
}
```

补充说明：

- 装备经验 0x004082DD：0x0040831C add dl,本值（立即数 0x0040831E）。
- 本条是6.5精确样本的代码固定值；值单位：点。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 装备升级·宝物等级上限：代码固定值

ID: `mechanism.65.dm-constant-equip-level-cap-special`；状态: `candidate`；证据: `source-reviewed`

带宝物标记的装备最高等级；6.4/6.5 默认 9，6.6 默认 15。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "equip-level-cap-special",
  "title": "装备升级·宝物等级上限",
  "value": 9,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x00408327",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x00007727",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "09",
      "signature": {
        "prefix": "89 55 E8 85 C0 74 04 B0",
        "suffix": "EB 02 B0",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "89 55 E8 85 C0 74 04 B0",
        "actualSuffix": "EB 02 B0"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "全部基底",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x00408327"
      ]
    }
  ]
}
```

补充说明：

- 装备经验 0x004082DD：0x00408326 mov al,本值（立即数 0x00408327）。
- 本条是6.5精确样本的代码固定值；值单位：级。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## 6.5 装备升级·普通等级上限：代码固定值

ID: `mechanism.65.dm-constant-equip-level-cap-normal`；状态: `candidate`；证据: `source-reviewed`

普通装备最高等级；6.4/6.5 默认 5，6.6 默认 9。


### 精确样本站点与签名


消费者证据：

```json
{
  "constantId": "equip-level-cap-normal",
  "title": "装备升级·普通等级上限",
  "value": 5,
  "nature": "代码固定值",
  "sites": [
    {
      "role": "primary",
      "address": {
        "kind": "va",
        "value": "0x0040832B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "fileAddress": {
        "kind": "fileOffset",
        "value": "0x0000772B",
        "profile": "profile.ccz65.unencrypted.3890.scan",
        "evidence": "static-verified"
      },
      "width": 1,
      "expectedFieldBytes": "05",
      "signature": {
        "prefix": "EB 02 B0",
        "suffix": "88 45 F8 8A 45 08 50 8B 4D EC",
        "prefixMask": null,
        "suffixMask": null,
        "actualPrefix": "EB 02 B0",
        "actualSuffix": "88 45 F8 8A 45 08 50 8B 4D EC"
      }
    }
  ],
  "signatureMatches": true,
  "relocationChecks": [
    {
      "label": "6.4/6.5",
      "hits": 1,
      "relocate": true,
      "optional": false,
      "addresses": [
        "0x0040832B"
      ]
    }
  ]
}
```

补充说明：

- 装备经验 0x004082DD：0x0040832A mov al,本值（立即数 0x0040832B）。
- 本条是6.5精确样本的代码固定值；值单位：级。代码立即数不登记成全局变量。
- 知识条目为源码审阅候选，站点原字节已只读核对；未由此授权自动补丁，也未执行游戏内效果验收。

写入策略：

- 必须重验样本身份、当前PE映射、字段原字节及前后签名；掩码0为通配，非0必须精确匹配。
- 成对及附加字段必须与主字段保持已证明相对位移、各自签名和同值；全部站点在同一整文件候选中等长修改，失败整组回滚。
- 此候选缺少通用补丁配方的完整指令边界与跨版本ABI证据；使用已验证源码实现及其事务，不依据本条自动改写其它构建。

## data 管理器策略页：界面描述与引擎语义对照

ID: `mechanism.65.dm-strategy-attribute-semantics`；状态: `canonical`；证据: `static-verified`

策略页把三组不同东西放在同一页面：Data.e5 的 0x61 字节记录、Ekd5.exe 的 10 张 144 字节子表、以及一个 30 字节全局地形表。字段名称大多正确，但 多个字段的语义/标签与引擎不符，另有若干 UI 选项缺少证据。


补充说明：

- data 管理器显示名已恢复为原有名称：界面为类型索引/命中上限/伤害系数/战场AI策略/练武场AI策略/效果索引/策略扩展标记；Profile 与 CSV 仍用策略类型索引/策略命中率/策略伤害系数/战场AI策略限制/练武场AI策略限制/策略扩展标记。功能修正保留：施展对象上限 2；战场/练武场 AI 上限 15；伤害类型上限 4；6.4/6.5 扩展位从策略页完全隐藏，6.6 只显示 bit0/bit1 两个可写复选框。
- 6.6 策略页的扩展位复选框名称为“策略模仿”（bit0）和“辅助穿透”（bit1）；bits2-7 不显示，但写回使用 (原值 & 0xFC) | (编辑位 & 0x03) 保留原值。
- 文件布局与运行时布局不同：0x40D73C 把文件 +0x0B..+0x0F 重排为运行时的对象/范围/穿透/MP/类型；data 管理器按文件偏移编辑是正确的。
- 语义错误：strategy-learning“效果索引”是 AI 类别位掩码；命中率是模式码；战场/练武场 AI 是评分处理器编号。
- 空属性：6.4/6.5 的策略扩展标记是 0x90 填充，不是可编辑策略属性。
- 旧界面名：strategy-learning 为“类型索引”，strategy-effect-class 为“效果索引”；后者的物理字段名仍是“效果类”，两者不是同一张表。
- 缺失：运行时 68 行边界、AI 16 项处理器映射、动画 0xFF/0x64+ 约定；命中码 0..4 已全量解析。
- 策略页区块标题已恢复为“效果与拓展”；strategy-learning 仍是 AI 类别掩码，界面旧名为“类型索引”。
- 是否伤血：0x415EFA 只返回 type<4；0..3 在全部直接消费者中完全等价，4 不伤血，>=4 同样被门控；6.4/6.5 由 ID 0x46/0x16 绕过门控，6.6 由策略类型 0x1E/0x06 绕过；显示函数只把精确的 4 显示为 0。
- 命中模式：0=基础×90/100、1=绝对100、2=能力曲线、3=基础×34/100、4=基础×50/100；>=5 是基础×值/100，不是无条件绝对百分比；最终封顶 100。6.4 额外在 0x406610 返回 0xFF 时置 0；6.6 效果读取改用 0x42518F。
- 位编辑器在实体重绑时抑制 CheckedChanged 提交，切换策略不会把中间复选框状态写成瞬态草稿；测试用未保存草稿在策略 0/104 间往返验证。
- 本实体只描述 data 管理器策略页与其引擎语义的对应关系，不授权任何自动写回。
- 界面标签取自 BusinessEditorPanel.FieldLabel/GetFlags 与 Profile 字段名；引擎语义取自 6.5 3EF7 静态反汇编。
- 6.4/6.5/6.6 的字段偏移一致；差异集中在 0xA2CE0 的含义和 6.6 效果类范围。
- 待确认：穿透范围 7 与运行时 +0x0D 的专属消费者；0x425AF0 的掩码不能直接当作策略证据。

## 穿透攻击-xx：以特效参数替换穿透范围

ID: `mechanism.65.pierce-attack-replacement.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.pierce-loader`：0x40782D 穿透加载入口
2. `fn.65.pierce-effect-chain.3890`：0x40CC13 顺序查 0x77..0x7F
3. `fn.65.param-getter-gated.3890`：0x42518F 逐个取特效参数
4. `fn.65.pierce-expand-wrapper`：0x4364C7 接收穿透码并展开
5. `fn.65.strategy-range-dispatch.3890`：0x435CE9 12 分支几何展开
6. `fn.65.attack-append-target`：0x437AFF 落格

## 远距攻击-xx：候选范围码并入范围块（叠加/替换）

ID: `mechanism.65.longrange-attack-overlay.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.fatal-field-c-reader.3890`：0x43F8C0 主范围 + 候选槽
2. `fn.65.longrange-effect-helper-9d.3890`：0x9D 八向 → 候选 1
3. `fn.65.longrange-effect-helper-9e.3890`：0x9E 没羽箭 → 候选 6
4. `fn.65.longrange-effect-chain.3890`：0x9F..0xA4 首个 → 候选=参数值
5. `fn.65.attack-selector`：0x45533D 读取 dword[unit+6] 范围块
6. `fn.65.attack-dispatch`：0x436511 循环 4 槽逐码查 0x4D1400 并集

## 人物能力显示值跳转表 0x430000（6.5/6.4 为 0x46902B）

ID: `mechanism.65.ability-display-table.3ef7`；状态: `candidate`；证据: `static-verified`

0x430000（6.5/6.4 为 0x46902B）是 8 项人物能力显示值计算跳转表，目标 0x40715A/718F/71C4/71F9/722E/7263/728F/72BB 三基底完全一致。索引 0..4 读取人物记录 +0x11/+0x13/+0x15/+0x17/+0x19 的五个 word，加上装备加成（0x407C29/0x407C35）与额外加成（0x436E02/0x436DE1）后封顶 0x270F（9999）；索引 5/6 计算 +0x1B/+0x1F 两个 word 资源上限（封顶 0xFFFF/0x270F）；索引 7 以 +0x2B 兵种 ID 计算兵种相关值。状态对话框在 0x45C97E 循环 0..4，以 SetDlgItemInt(0x400+idx, value) 显示五项能力。


## 策略 AI 字节的 16 分支评分分派

ID: `mechanism.65.strategy-ai-dispatch.3ef7`；状态: `candidate`；证据: `static-verified`

strategy-battle-ai 与 strategy-training-ai 的每策略字节不是位掩码，而是 0..15 的处理分支索引。0x4395DC 按 strategy_id 取字节，经固定 16 项跳转表 0x43A140 进入对应评分分支，把权重累加到 [ebp-4]。byte[0x505FDC] 选择战斗表或训练表。


## 策略地形可用性位掩码

ID: `mechanism.65.strategy-terrain-bitmask.3ef7`；状态: `canonical`；证据: `static-verified`

0x420ACC 是 30 字节地形位掩码表（每种地形一个字节）。0x419587(terrain, mask) 返回 table[terrain] & mask。策略使用检查在 mask 为 0 时返回“不能在这里使用。”；同一链路还使用“不能对我方部队使用。”。表在 6.4/6.5/6.6 完全相同。


## AI 评分剩余分支 2/13/14/15

ID: `mechanism.65.ai-branch-2-13-14-15.3ef7`；状态: `canonical`；证据: `static-verified`

分支 2：0x4078D1>40 且 0x43FFB9==0 时 +100，并按 [ebp+0x18] 追加 0x438917；分支 13 无追加；分支 14/15 按状态偏移 0x18/0x1A/0x35 与阈值 3 追加 10。至此 0..15 全部分支已记录。


## AI 评分分支 3/4/6 的权重与阈值

ID: `mechanism.65.ai-branch-3-4-6-scoring.3ef7`；状态: `canonical`；证据: `static-verified`

AI 分支 3/4/6：分支 3 以 HP/5 与 30 阈值给 +20；分支 4 以命中 35 给 +26（80 再 +26）；分支 6 以兵种属性行5==2 或命中 60 给 +25，80 再 +7。


## AI 评分分支 7/8/9/10/11/12 的权重与阈值

ID: `mechanism.65.ai-branch-7-12-scoring.3ef7`；状态: `canonical`；证据: `static-verified`

分支 7/8/9：0x439CFE 为真 +50，策略 0x28/0x2B 追加 5/10；分支 10：属性比较 +6；分支 11：4 项位表/权重表最大 +5；分支 12：状态/策略 0x39/兵种 9/0/0x13 分支 +15。


## 策略 AI 分派表与处理体的三基底一致性

ID: `mechanism.65.ai-dispatch-handler-cross-base.3ef7`；状态: `canonical`；证据: `static-verified`

0x43A140 的 16 项跳转表三基底完全一致；处理体仅部分一致：6.4/6.5 有 10/12 相同（分支6/11不同），6.6 仅 3/12 相同（分支3/10/13相同）。


## AI 伤害比例评分（分支 0/1/5）

ID: `mechanism.65.ai-damage-ratio-scoring.3ef7`；状态: `canonical`；证据: `static-verified`

策略 AI 分支 0/1/5 以伤害/目标 HP 百分比评分：ratio=damage*100/HP，0 取 1；ratio==100 时累加 100，否则覆盖累计分；策略 ID 0x44 追加 0x417A5E 结果；0x14..0x24 另有特判。


## 6.6 AI 处理体常量与调用目标逐项重定位

ID: `mechanism.65.ai-handler-constants-66.3ef7`；状态: `canonical`；证据: `static-verified`

6.6 的 16 个 AI 处理体入口与 6.5 完全一致，但同位置常量被系统性替换：0x1B→0x23、0x35→0x41、0x39→0x59、0x27/0x28/0x2B→0x37/0x38/0x3B、0x44→0x2B、0x14→0x1E、0x10→0x13、0x0F→0x12；调用目标 0x43FFB9→0x4190E8、0x438917→0x438914、0x43B6F3→0x43B730、0x406764→0x41832B、0x43C022→0x43C01D、0x417A5E→0x417A61；内嵌评分下限表 0x4395D8 搬到 0x412793（4 字节 19/1E/23/19=25/30/35/25，内容不变），配套方向掩码表 0x4240D2 为 03/0C/30/C0。处理体 0/1/5 另有结构重排。


## 6.5→6.6 全局数据锚点重定位映射（27 组配对）

ID: `mechanism.65.anchor-relocation-66.3ef7`；状态: `candidate`；证据: `static-verified`

以 dataRefs 的引用函数签名做 Jaccard 配对，得到 27 组 6.5→6.6 全局锚点映射：原 0x4CE76C..0x4CE7FE UI/战斗全局块迁到 0x500AAC..0x500ADE（逐字段、非固定位移），0x511000→0x508C00、0x511400→0x4CB1C0、0x511E40→0x4930C8；.text 内嵌数据 0x407826→0x41A139、0x407D1A→0x476891。高置信 8 组（Jaccard≥0.82）。第 68 轮以同址操作数复核，新增 9 组字段级映射并更正 UI 模式字段：0x4CE79F→0x500AD7（原误记为 0x500AD3）。


## .api 段动态 API 名称表：DLL 名 + 槽位组（名称VA-0x400000-2）

ID: `mechanism.65.api-name-table.3ef7`；状态: `candidate`；证据: `static-verified`

.api 段位于 0x4BE000（VirtualSize 0x10000、可执行），先连续存放 DLL 名，再按 DLL 顺序存放槽位组（每组若干 dword、以 0 结束）。槽位静态值 = 名称字符串VA - 0x400000 - 2，运行期替换为真实函数指针，调用方统一 call dword ptr [slot]。6.4/6.5：5 个 DLL（USER32/KERNEL32/Msimg32/GDI32/Jpg）、表起 0x4BE036、12 槽（LoadImageA@0x4BE036、SetLayeredWindowAttributes@0x4BE03A、GetPrivateProfileIntA@0x4BE042、GetLocalTime@0x4BE046、TransparentBlt@0x4BE04E、AlphaBlend@0x4BE052、GetBitmapBits@0x4BE05A、SetBitmapBits@0x4BE05E、JpgInit@0x4BE066、JpgRead@0x4BE06A、JpgFree@0x4BE06E、PngRead@0x4BE072），其中 TransparentBlt/AlphaBlend 无静态消费点。6.6：增加 GDIPLUS.dll，表起 0x4BE042，新增 10 个 GDI+ 槽（GdiplusStartup@0x4BE086、GdiplusShutdown@0x4BE08A、GdipDeleteGraphics@0x4BE08E、GdipCreateBitmapFromScan0@0x4BE092、GdipBitmapLockBits@0x4BE096、GdipBitmapUnlockBits@0x4BE09A、GdipDrawImageRectRectI@0x4BE09E、GdipCreateFromHDC@0x4BE0A2、GdipCreateImageAttributes@0x4BE0A6、GdipSetImageAttributesColorMatrix@0x4BE0AA），API 名称串整体后移到 0x4BE100。GDI+ 消费链（第135轮）：启动 0x4829DB 依次 GdiplusStartup(&0x4CEA70, input v1, NULL) → GdipCreateImageAttributes(&0x4CEA74) → SetUnhandledExceptionFilter(0x482990)（旧过滤器存 0x4BCCB4）；位图链 0x42FE04 用 GdipCreateFromHDC([0x4B9948]/[0x4B9970] → 0x4CEA78/0x4CEA7C)、GdipCreateBitmapFromScan0(0x4B7750+arg, 格式 0x21808)、GdipBitmapLockBits/UnlockBits(0x4CEA80)；绘制 0x41A4D6/0x41A5D1/0x41A693 调 GdipDrawImageRectRectI(0x4CEA78, [0x4B7798], unit=2)；颜色矩阵 0x42FE84 以 0x47FD13 清 0xC8 字节、写 4 个 1.0f 对角线并用 arg/divisor 作缩放，0x42FECF 调 GdipSetImageAttributesColorMatrix(0x4CEA74)。GdiplusShutdown 与 GdipDeleteGraphics 无真实调用点。其余 API 消费点：GetPrivateProfileIntA 用于 AutoDll.ini（0x4069E4/0x4069FE/0x406A18）、GetLocalTime 用于存档时间戳（0x40535C 写 SYSTEMTIME 到 0x501AD0）、SetLayeredWindowAttributes 用于窗口透明（0x4102EE，6.6 另加 0x479BD7）、Get/SetBitmapBits（0x408A15/0x4089DC，6.6 0x408A1B/0x4089E2）、LoadImageA（0x44D2C0）、Jpg/Png 解码链（0x420DBF/0x420DDD/0x420E1D/0x420E2A/0x416236，6.6 PngRead 0x416244）。6.6 段首复用（第143轮）：0x4BE004/0x4BE006/0x4BE008 被当作对话框暂存字，0x46D0F8 以 [0x4BE006] 作自动关闭标志（-1 时下一个 WM_INITDIALOG 立即 SendMessageA(hwnd,0x591) 关闭），0x4793BB 打开模板 343「说明介绍」前写 -1、返回后清 0x4BE004/0x4BE008。


## 三基底算术立即数普查与 6.6 新结构（21 字节文本表、0x500030 图标表）

ID: `mechanism.65.arithmetic-immediates-census.3ef7`；状态: `candidate`；证据: `static-verified`

用 arith_immediates.py 对三基底可执行节统计 imul 立即数（107/106/122 种）与 shl/shr/sar 立即数（29/29/26 种）。共享高频公式常量集中在 3、0x30(48)、0x1B00(6912)、0x10、6、4、0x64(100)、0x14(20) 等。6.6 独有小立即数揭示：21 字节文本记录步长 0x15（表基 +0x662，替代 6.5 默认 0x14/+0x4BE，旧表保留给类型 2；0x32/+0xA4 表不变），以及 0x12C=300 的状态图标横向间距（0x41EB48，配合 0x500030 的 16 字节步长表）。


## 防具经验基础值与无伤害扣减（三基底）

ID: `mechanism.65.armor-exp-cross-base.3ef7`；状态: `canonical`；证据: `static-verified`

防具经验函数 0x403A8A..0x403B11：基础值 6.4=3、6.5=3、6.6=4；无伤害路径分别扣 1/2/3；当前 HP 低于攻击前值时再扣 1。


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

## 自动战斗标志 0x4B4250+0x64/+0x68（AI 托管选目标与自动结算）

ID: `mechanism.65.auto-battle-flags.3ef7`；状态: `candidate`；证据: `static-verified`

0x4B4250+0x64（dword）与 +0x68（dword）是自动战斗/AI 托管标志。0x412F84：+0x64==1 时交换目标指针并 call 0x4389BD(候选,0)（AI 最优单位评分选择）；0x412F9B：+0x68==1 且 [ebp-0xC]==1 时进入同一 AI 分支；0x43E823：byte[0x501A6E]!=0 且 0x41C330(0x4B3D08)==0 且 +0x64!=0 时依次 call 0x44DA7A(0)/0x44DA7A(1)（自动结算/结束）。0x44DA7A(side) 是一方单位的行动顺序生成器：arg!=0 遍历槽 0x00..0x3A、arg==0 遍历 0x3C..0xF9，先把全体单位 byte[unit+0x0B] 置 0xFF（0x44F980），再按 9 项分派表 0x44DC37 逐 pass 处理，用全局计数器从 0 递增写回 +0x0B。9 项依次为 0x44DB12/0x44DB3F/0x44DB5D/0x44DB6B/0x44DBAA/0x44DBEF/0x44DBFA/0x44DC10/0x44DC05：分支0 若 0x4225FB(unit)!=0 且兵种系 byte[0x4D2200+系]==9（仅系 0x12）则置 0x75 延后；分支1 word[unit+6] 经 0x417B5A 判定；分支2 0x439CFE；分支3 若 byte[0x505F7C]==2 调 0x44DC5B 按桶表 0x44DCCC 做 6 级排序并跳到分支8，否则用 0x43FFB9（0x4D2188 表，1 特判、否则 al^2）且兵种系!=9 才分配；分支4 若 0x505F7C==0 直接跳分支8，否则取 0x40658F(unit) 记录 byte[+0x2B] 兵种 ID→0x41B782(0x4A2A27+ID*0x23) 的 0x23 字节记录，0x436CA3 读 +0x02/+0x03，任一>=4 即分配；分支5 0x4281AF（0x4D2138 表）；分支6 0x43FF6E（0x4D20E8 表项==0）；分支7 剩余 +0x0B==0xFF 者分配；分支8 +0x0B==0x75 者分配。0x418C90 读 byte[unit+0x0C]，仅==2 的单位参与。0x505F7C 在 6.5 EXE 内无静态写入点（原版恒 0，有效 pass 为 0/1/2/3/8）。写入方穷举：6.5 Ekd5.exe 中 266 处 mov reg,0x4B4250 的 45 条窗口内只有两处读取，绝对地址 0x4B42B4/0x4B42B8 无引用，add reg,0x64/0x68 间接写入也不存在；Cmdicon/Mgcicon/GearNtKe/Itemicon/Mapatr/Jpg/zlib 七个 DLL 也无 0x4B42B4/0x4B42B8 立即数。同目录 AutoDLL.ini 提供 EnableAutoSave/Resize/EnableFastKey 开关，与读取分支语义相容但无静态一一对应证据。


## AVI 动画播放模块：avivideo MCI 命令常量与 0x41EF96 点击跳过钩子

ID: `mechanism.65.avi-player.3ef7`；状态: `candidate`；证据: `static-verified`

AVI 动画通过 avivideo MCI 设备播放：0x41F032 MCI_OPEN(0x803, flags 0x2000 MCI_OPEN_TYPE, element "avivideo")；0x41F08D/0x41F5F6 MCI_SEEK(0x807, flags 0x100 MCI_SEEK_TO_START)；0x41EFE7/0x41F0A1/0x41F7C5 MCI_PLAY(0x806, flags 1 MCI_NOTIFY)；0x41F16A MCI_WINDOW(0x841, flags 0x40000 MCI_ANIM_WINDOW_STATE, state 5)；0x41F188/0x41F81A MCI_STATUS(0x814, flags 0x100 MCI_STATUS_ITEM)，状态值 0x20E=播放/0x211=暂停；0x41F737 MCI_WHERE(0x843, flags 0x20000)；0x41F8C1 MCI_PAUSE(0x809)；0x41F11D MCI_OPEN(0x803, flags 0x30200=MCI_ANIM_OPEN_PARENT 0x20000|MCI_ANIM_OPEN_WS 0x10000|MCI_OPEN_ELEMENT 0x200，i=0..4 最多重试 5 次)；0x42F76D MCI_STOP(0x808)、0x42F77F MCI_CLOSE(0x804)。设备 ID 存 word[0x497AE0]，播放窗口 0x497A9C，钩子 0x497A98；0x41F1DF 安装 SetWindowsHookExA(3=WH_GETMESSAGE, proc 0x41EF96)。钩子 0x41EF96 在 MSG.message==0x201（WM_LBUTTONDOWN）且窗口匹配 [0x497A90+0xC] 时置 [0x497A90]=1，实现点击跳过动画；否则在 [0x497A90+4]==0 时发 MCI_PLAY 并 CallNextHookEx。片名常量：LOGO.AVI/OPEN.AVI/END.AVI/PRESS.AVI（0x48B6E8..0x48B702）；错误文案「开启动画文件失败。」「不能播放动画文件%s。」「打开文件%s时出错。」「%sOpenErr」。0x41F1F1 以 MessageBoxA(title=0x48C8D8, text=0x48B734, 0x30=MB_ICONWARNING) 报错。MCI 消息全图（第136轮，按调用点回溯 push）：0x41F08D/0x41F5F6 = MCI_SEEK(0x807, flags 0x100=TO_START)；0x41F0A1/0x41EFE7/0x41F7C5 = MCI_PLAY(0x806,1)；0x41F16A = MCI_WINDOW(0x841,0x40000)；0x41F188/0x41F81A = MCI_STATUS(0x814,0x100)，状态值 0x20E=PLAY/0x211=PAUSE；0x41F737 = MCI_WHERE(0x843,0x20000=SOURCE)；0x41F8C1 = MCI_PAUSE(0x809)；0x41F11D = MCI_OPEN(0x803,0x30200)。BGM(sequencer) 链：0x42F7C3 MCI_OPEN(0x803,0x202=MCI_OPEN_ELEMENT|MCI_WAIT)，类型串 0x486934="sequencer"，元素名格式串 0x486910=".\SoundTrk\%02u-AudioTrack %02u.mp3"；0x42F7E1 MCI_PLAY(0x806,0x10000)；0x42F820 MCI_SETAUDIO(0x873)，flags 0x1800000=MCI_DGV_SETAUDIO_ITEM(0x800000)|MCI_DGV_SETAUDIO_VALUE(0x1000000)，参数 item=0x4002=MCI_DGV_SETAUDIO_VOLUME、value=音量×10；0x42F840 MCI_PAUSE(0x809)；0x42F862 MCI_RESUME(0x855)；0x42F76D MCI_STOP(0x808)；0x42F77F MCI_CLOSE(0x804)。设置 +0x03=音量（0x42E218 取控件 0x411 TBM_GETPOS(0x400)→+0x03→0x42F7FC×0xA→MCI_SETAUDIO）。


## 战场模式字节 0x4B3D18 与移动力覆盖 0x48E8C2

ID: `mechanism.65.battle-mode-byte.3ef7`；状态: `candidate`；证据: `static-verified`

0x4B3D18 是战场状态基址 0x4B3D08 的 +0x10 字节开关，值 0/1/>=2 控制是否使用 0x48E8C2 的临时移动力覆盖；0x48E8C2 以 0xFFFF 为哨兵，0x438986 写入、0x438997 复位，0x43896D 循环经 0x4389BD 物理伤害评分并写 0x4B2C30。0x425325 在模式>=2 时仅允许当前单位 0x4B5DF0 使用覆盖。


## 剧本战斗指令族与行动权重置

ID: `mechanism.65.battle-script-action-family.3ef7`；状态: `canonical`；证据: `static-verified`

剧本战斗指令族 0x3F/0x40/0x51/0x56/0x57/0x5D 的处理器与常量已定位。0x51 循环最多 250 个战场对象，过滤 byte[obj+0xC]==2，清除 obj+0xD 的 6 位与 obj+0x1E 的指定位，并把 obj+0x10 写为 min(取值, 原值)；随后调用 0x453AC3(0x4B4250) 与 0x44A88A(0x4B3D08)。


## 战场单位占位表 0x4B3D21（250×5）

ID: `mechanism.65.battle-unit-table.3ef7`；状态: `canonical`；证据: `static-verified`

0x4B3D21 为 250 条 ×5 字节的战场对象/单位占位表：byte0/1=x/y，byte2=类型（0x11 特殊，0x1A/0x1B 变体），byte3=对象 id（0xFF 空，0xFFFFFFFF 清除），byte4=图层（4..0xC8 走 +0x1F40 层，否则 +0x640 层；0xFF 空）。0x4560F3 以 i*5 扫描并在 byte3==0xFF 时结束，0x43B420 比较前两字节坐标。表范围 0x4B3D21..0x4B4222，后接 0x4B422C 网格尺寸对；0x1B00 为单个地图层字节数。


## 战场视口/滚动上下文 0x4B4250

ID: `mechanism.65.battle-viewport-context.3ef7`；状态: `canonical`；证据: `static-verified`

0x4B4250 是战场视口/滚动上下文，三基底字段集合一致（各 19 项）：+0x04/+0x08 为像素原点（由地图记录 [0x4CEA08]+0x1B/+0x1F 载入），+0x14/+0x18 为视口宽高（像素，0x45503F 以 /0x30 得瓦片数），+0x24/+0x28/+0x34/+0x38 为视口矩形，+0x2C/+0x30 为目标/中心，+0x3C/+0x40 为额外偏移，+0x20/+0x22 为屏幕/面板宽高，+0x54/+0x55 为待处理滚动目标字节对（0xFF 哨兵），+0x61 为滚动模式（0=默认 shift1；1/2=限位1 shift3；3=限位2 shift5），+0x64/+0x68 为只读模式标志（候选自动战斗/快速结算，未发现直接写点），+0x1B85 为使用效果码槽 0。像素↔瓦片换算统一用 0x30（48px），助手 0x40BAD4 为有符号除法。居中函数 0x45503F(centerX,centerY)：byte[0x505FDC]==0 才执行；tilesW=dword[+0x14]/0x30、tilesH=dword[+0x18]/0x30；half=(tiles-sign)>>1；0x47FAD0(center,half) 返回 byte；再按 byte[0x4B422C]/byte[0x4B422D] 夹紧；最后 call 0x454CEF(x,y) 设滚动位置。0x454CEF 把 +0x04/+0x08 除以 0x30 得当前瓦片，调 0x45461C 预处理；目标瓦片与当前相同则直接返回，否则算 old-new 的 deltaX/deltaY 进入滚动分支。0x45461C 读取 +0x54/+0x55 并清为 0xFF，按 +0x61 选择限位/位移，两值均有效时调 0x45218F 并 0x476882 刷新。0x45218F(dx,dy,shiftX,shiftY)：tileX=byte[0x40D344(dword[+0x04])]+dx、tileY 同；byte[0x505FDC]!=0 走 0x1E000 + 0x40155F，否则 0x401617；index=0x403789(x,y)、dest=base+index*0x1B00；附加 +0xC80/+0x12C0/+0x1F40 子区与全局格数组 0x4BE880；flag=byte[0x4B3D08+5]&1；四个像素坐标 ×0x30 后交 0x41E5DB。


## 引擎全局容量、循环上限与哨兵契约

ID: `mechanism.65.engine-capacity-and-sentinels.3ef7`；状态: `canonical`；证据: `static-verified`

三基底共享的主要容量：人物 1024×72、战场单位 250、物品 255×25、兵种 80×35、兵种系 40×60、策略 144×97、效果 255×8、必杀 80×16、仓库 200×3、范围段 256、地形 30、天气 5×6、商店 127×40。0xFF/0x8000/0x80000000/0xFFFF/0x50/0xFA/0x3FF 是空值、越界或无操作哨兵。


## 40×40 逐格字节数组 0x4BE880

ID: `mechanism.65.cell-byte-map.3ef7`；状态: `candidate`；证据: `static-verified`

0x4BE880 为 40×40（0x640=1600 字节）逐格字节数组，0xFF 表示空；0x40DC1D 用 0x47FD13 以 0xFF 初始化整个 0x640 字节（参数 !=1 时另写 word[0x5073B8]=0xFFFF）。索引与格标志一致：0x403789(coord)=y*width+x。8 处引用：0x405123（取格字节，并按层号*0x1B00 选层、按 0xC 步长读 0x506800 表，表项 +8 为指针、0x2828 为标记）、0x40AF38、0x40B0A6、0x40B134、0x415407（同址加基址后读取）、0x40D4B5（≠0xFF 走 0x4525DA，==0xFF 走 0x41606C 绘制）、0x40DC2A（memset 初始化）、0x452218（滚动核心内 index += 0x4BE880）。


## 地图格标志 0x4934B0 写入函数 0x42A5D6 与全图 and 0x0C/test 0xD 遍历

ID: `mechanism.65.cell-flag-writer.3ef7`；状态: `candidate`；证据: `static-verified`

0x42A5D6(coord, mask, on)：index=0x403789(coord)=y*width+x，addr=0x4934B0+index；on!=0 时 byte |= mask（置位前若 (byte&0xD)==0 记 edx=1），on==0 时 byte ^= mask；随后 test 0xD 并返回状态变化。mask 由调用方传入（常见 1/4/8/0xC）。唯一直接调用点 0x42A666 以固定 mask=8 在矩形区域内逐格标记（bit3=范围标记）；另一条链为 0x4D1400 效果范围表 → 0x41E254 枚举 → 回调 0x42A708（x<[0x4B422C]、y<[0x4B422D] 检查，on==0 时先经 0x42A74A 矩形判定）→ 0x42A5D6。0x42AAA5 在 [ebp-8]!=1 且 [ebp+8]<2 时对 0..0x63F 全图执行 byte &= 0x0C（清 bit0/1、保留 bit2/3）。0x42A43E 以 x<[0x4B422C]、y<[0x4B422D] 遍历全图，每格 test 0xD 并用 0x1B00 计算层偏移。


## 角色经验结算常量三基底对照

ID: `mechanism.65.char-level-exp-cross-base.3ef7`；状态: `canonical`；证据: `static-verified`

0x4088CD 的三基底常量：6.4 最大等级 80、固定阈值 150；6.5 最大等级 60、阈值按 20 级分段 150/200/250/300；6.6 最大等级 99、固定阈值 250。升级循环与成长 0x408D52 相同。


## 运行时人物记录 72 字节访问器簇

ID: `mechanism.65.runtime-character-accessors.3ef7`；状态: `canonical`；证据: `static-verified`

人物记录 1024×72，基址 [0x4CEA00]；+0x2B 兵种、+0x2C 等级、+0x2D 经验、+0x2E 起 3 个装备槽（每槽 3 字节）。6 个访问器三基底字节一致。


## 人物模板表 0x4A3E77（68×97，+0x11 起 80 兵种字节）与 0x41CEAB 索引

ID: `mechanism.65.character-adaptation-table.3ef7`；状态: `candidate`；证据: `static-verified`

0x4A3E77 为运行期填充的 97 字节记录表，容量 144 条（0x90），文件初始化 68 条（0x44）：头部 +0x00..+0x0B 为内联名称字符串（0x423A7D 以 "%s" 输出），+0x0C 为 0x418C90 读取并经受 0x41CE8B(2) 随机替换的字节，+0x0D 被复制到单位 +0xC/+0xD，+0x0F 与方向/攻击码同构（0x44270C），+0x11..+0x60 为 80 个兵种字节（0x4845B2 以 record+0x11+job 取值）。区段结束 0x4A7507，下一表基址 0x4A7510，再后为 0x4A7D8E 的 80×35 兵种表。0x4303C8 的 20 个值穷尽消费链后仍只用于与 0x0B 的合法性比较。 第85轮补充：+0x0C 为动作/图像编号（0x401DFF→0x41CE8B(2) 随机替换链索引）；+0x0D 为组别/候选索引（0x4244E5 以 byte[template+0xD] 索引栈上候选列表，选中值同时写入单位 +0xD 与 +0xC；0x4233F8(2) 取类别值并经 0x417B77 校验）。


## 256 项 RGB 调色板 0x4CB1C0（6.5/6.4 为 0x511400）

ID: `mechanism.65.color-palette.3ef7`；状态: `candidate`；证据: `static-verified`

0x4CB1C0（6.6）/0x511400（6.5、6.4）是 256 项 dword 调色板（0x400 字节，格式 0x00RRGGBB，三基底逐字节相同，sha256 6BC92B09…）。0x00F700FF 为透明色键。颜色用于像素合成（0x4034F6）、GDI 画刷（0x4647E8 CreateSolidBrush）、阵营/伤害数字颜色（0x42E195 取索引 0x1F/0x3A/0x12 或 0x12/0x28/0x12）。0x45B6E3 把调色板转换为 0x497770 的 256×3 4-bit RGB 表：6.5/6.4 由调用方传入源/目的，6.6 硬编码源 0x4CB1C0、目的 0x497770，调用点 0x42B9FB 位于战斗初始化链。


## 暴击/连击模式 0x505EC8 与暴击值数组 0x511E40/0x4930C8

ID: `mechanism.65.crit-combo-mode.3ef7`；状态: `candidate`；证据: `static-verified`

0x505EC8 为 6.5/6.6 新增战斗模式字节（6.4 无引用）。mode==1 时暴击计算 0x4284C5（6.6: 0x445D40）读取每单位 4 字节暴击值数组高字节，>=100 取反，并以 0x48E0C9『暴击』输出；mode>1 时 0x43B4B6 以 mode 为上限、0x505EC4 为下限，每 10 点追加最多 2 段伤害，对应『连击』。数组 6.5 为 0x511E40，6.6 重定位为 0x4930C8。


## 第 96–111 轮新函数的三基底同址哈希审计

ID: `mechanism.65.cross-base-audit-late.3ef7`；状态: `candidate`；证据: `static-verified`

对第 96–111 轮新函数做同址 SHA1 对照：0x40BE7D（指针→索引）三基底完全一致；0x42A5D6（格标志写入）与 0x42A708（范围回调）为 6.4=6.5、6.6 不同；0x47FA40/0x47F9E2（内存池分配）同样 6.4=6.5、6.6 不同；0x41F952（点数加减）、0x456CB4（332 确认）、0x42A43E（全图遍历）三基底各异。


## 全局当前人物记录指针 0x500E28 与指针→索引 0x40BE7D

ID: `mechanism.65.current-record-pointer.3ef7`；状态: `candidate`；证据: `static-verified`

0x500E28 存当前选中人物的记录指针。写入点：0x469FD1（列表选择变化，新指针 != [obj+0x20] 时写 0x500E28、同步 [obj+0x20] 并调 0x4698AF）与 0x4787F9（角色面板打开，把 [ebp-0x7C] 写入并用 0x4CE77D 调 0x401126）。读取点：0x401129/0x40F0FE/0x412A3F/0x44D4EA/0x456CCE。0x40BE7D(ptr) 用 (ptr-dword[0x4CEA00])/0x48 把记录指针换算为人物下标（0x48=72 为记录大小）；332 确认处理 0x456CB4 用它把 0x500E28 转成下标后经 0x42ACD2 访问 0x508000 功勋表。


## 伤害落点 0x411072 与战斗模式字节 0x500E9A/0x500E9B

ID: `mechanism.65.damage-apply-mode.3ef7`；状态: `candidate`；证据: `static-verified`

0x411072 以 ecx 接收伤害、栈参 mode/目标/来源；若 byte[0x500E9A]==1 或 0x426B33(目标)!=0，追加 40% 伤害；mode!=0 时置 0x505EFC=1 并调用 0x4594EA 结算。0x500E9A 为战斗模式/伤害加成开关（0/1/2，初始 0），0x500E9B 为战斗表现开关（11 处引用）。


## 通用模态对话框框架：模板 332/340/341、DlgProc 0x46D0F8、分派器 0x46D221 与状态字节 0x48E8C1

ID: `mechanism.65.dialog-framework.3ef7`；状态: `candidate`；证据: `static-verified`

0x418C34 是通用「是/否」确认框包装：ConfirmDialog(parent, text, caption, mode) 先以 0x475600 在栈上构造 vtable=0x487410 的对象，0x46F982 写入 +0x0C=mode、+0x10=text、+0x14=caption，再由 0x46D098 调用 DialogBoxParamA(hInstance=dword[0x4B6A60], 模板 0x154, parent, DlgProc=0x46D0F8, dwInitParam=&obj)；返回码 6（IDYES/「是」）时返回 1。模板 340 布局：是=ID 6、否=ID 7、图标静态控件 ID 0xFFFF（ord 137）、正文静态控件 ID 0x534；标题 6.5=三国志曹操传、6.4=三国志刘备传、6.6 同 6.4。0x46D0F8 在 WM_INITDIALOG 建 0x4B68E8 辅助对象并写 [obj+4]=hwnd，随后把消息交给 0x46D221；0x46D221 的消息表：0x2→vt+0x14、0x110→vt+0x08 与 vt+0x0C、0x111→取消/0x42F 特殊路径与 vt+0x10、0x30F→0x47252B+vt[0]、0x135/0x136/0x138→vt+0x20/+0x18/+0x1C、0x311→0x403B14、默认→vt[0]。vt[0]=0x46F2E7 在 WM_COMMAND 时 EndDialog(hwnd, wParam&0xFFFF)，所以按钮 ID 直接成为返回码。模板 332 为功勋点数分配框（26 控件：1030..1034 五维标签、2006..2010 数值、2022..2026 加、2027..2031 减、2011 点数、2001 重置、2 确认、1235 人物列表），由 0x418BC8 打开并把 0x48E8C1 置 1；模板 341 为历史情报框（6.5 列表+「信息筛选」，6.6 改为 SysTabControl32），由 0x41C3D7 打开并把 0x48E8C1 置 2。0x48E8C1 即模态对话框状态字节（0=空闲/1=332/2=341）。6.6 的 DlgProc 增加客户区拖动（WM_LBUTTONDOWN 0x201→SendMessageA 0xA1/2）与自定义消息 0x591，并把 WM_COMMAND 拆到 0x46D345（含 0xAD9、0x14、0x42F 常量与 0x42CA5E 类判定）。6.5/6.4 的对话框 9pt 宋体由 0x42124E（固定字面 0x48B6CC、charset 0x86、outPrecision 4）创建，6.6 改为 0x42A269→0x41EBA3(face=0x500030)。


## 332 对话框工作区 0x4FFF68：五项值/+0x14 点数池/+0x0A 第二数组/+0x21 字段

ID: `mechanism.65.dialog-workarea-4fff68.3ef7`；状态: `candidate`；证据: `static-verified`

0x4FFF68 是模板 332 的工作区：+0x00..+0x09 为五项经验值（word×5，由 0x40123E 从参数数组拷入），+0x0A 起为第二组 word×5 = 五项升级阈值（0x40123E 调 0x42AC8F 后写入），+0x14 为剩余点数池（dword，0x41F952 加减），+0x21 为每项记录的等级字节（0x40123E/0x423F75/0x4620C7 作为 level 参数并在升级时 +1）。0x42AC8F(expWordPtr,level,mode) 阈值公式：level>=0x6E 返回 -1；level<0x50(80) 阈值=0x32(50)；level>=0x50 阈值=(level-0x4F)*0x0A+0x37（80 级=65、每级 +10）；mode!=1 时循环扣减经验并递增等级。0x40123E(hwnd,expArray,baseRec,i) 依次：写 workarea[i] 经验、算阈值写 workarea[+0x0A+i*2]、0x4129E5(hwnd,0x7D6,workarea,i) 刷新数值、0x415F10(hwnd,i+0x7E6,[ebp-8],workarea+0x14) 刷新剩余点数。引用点：0x401241、0x41F956、0x4108E0、0x456CC4、0x456DAB；0x42AC8F 调用点：0x401268、0x423EFF、0x423F75、0x4620C7。0x505F40（全局池）与 0x4FFF68+0x14（对话框池）的静态同步点未找到。


## 模板 332 对话框类 vtable 0x44A6B5 与 WM_COMMAND 处理 0x456CB4（五维复选框掩码）

ID: `mechanism.65.dialog332-confirm.3ef7`；状态: `candidate`；证据: `static-verified`

模板 332（功勋/五维分配框）的对话框类由 0x410EED 构造：call 0x40E03D 基类 → 0x463322 构造 +0x2C 子对象 → 写 vtable 0x44A6B5（10 槽：0x44D4D2/0x46E81F/0x46F9BA/0x401216/0x456CB4/0x46E9DB/0x40E310/0x42C5EC/0x40E370/0x40E3D0）。WM_COMMAND 槽为 0x456CB4：若 byte[0x505FA8]==0 或 0x42ACD2(0) 返回 0xFF 则直接 EndDialog(hwnd,0xFF)；否则复制 5 个 word，循环 i=0..4 对 GetDlgItem(hwnd,0x406+i) 调 0x41B8AF（SendMessageA 0xF0=BM_GETCHECK==1）组成 5 位掩码写对象 +2；当 [edx+0x14]!=0、byte[ecx-4]!=1 且掩码非空时，把 dx 加到最低置位项对应的 word；最后 EndDialog(hwnd,0xFF)。0x42ACD2(index)：index<0x66 且 ([ebp+8]==1 或 byte[record+0x2A]!=0xFF) 时返回 index*0x0A+0x508000，否则 al=0xFF；0x508000 为 102 条 ×0x0A 记录表。界面刷新（第153轮）：0x4129E5(hDlg,id,ptr,idx) 用 "%d/%d"（0x500C5F，v2==0xFFFF 时用空串 0x48E8B7）刷新 0x7D6+idx 的当前/阈值文本并调 0x423EF1；0x423EF1 用 3 字节步长名称表 0x486ACB（武/统/智/敏/运）与 0x42AC8F 阈值生成 "%s(%d)"（0x48643D）写入 0x406+idx；0x415F10(hDlg,id,flagA,flagB)=EnableWindow(GetDlgItem(id),flagB)+EnableWindow(GetDlgItem(id+5),flagA)，在 332 中 id=0x7E6+idx（加号）、id+5=0x7EB+idx（减号），加号由记录[+0x14]（剩余点数）控制、减号由可否回退标志控制。模板 332 资源共 26 控件、221×111 DLU、宋体 9：确认 0x2、右大静态「功勋」、0x406..0x40A 五维标签、0x7D6..0x7DA 值、0x7E6..0x7EA "+"、0x7EB..0x7EF "-"、点数 0x7DB、重置 0x7D1、左侧 0x4D3（class ord 131）。


## 模板 332 刷新链 0x4108DB/0x456DA6/0x41F952（五维复选框与控件 ID）

ID: `mechanism.65.dialog332-refresh.3ef7`；状态: `candidate`；证据: `static-verified`

0x4108DB 是模板 332 的刷新入口：先压入 0/0x4FFF68/0x505F40；若 [对象+0x14] != [记录+0]（记录变化）则 0x456DA6(1,hwnd,index) 重建显示；否则循环 i=0..4，用 GetDlgItem(hwnd,0x406+i)+0x41B8AF 读 5 个复选框状态，对未勾选项以 0x41F952(id=0x7EB+i, value) 返还点数。0x41F952 是加减处理：ID 0x7E6..0x7EA（2022..2026，加号）把 value 加到 word[0x4FFF68+i*2] 并从 dword[0x4FFF68+0x14] 扣池；ID 0x7EB..0x7EF（2027..2031，减号）反向并从池返还。0x456DA6 内以 0x42ACD2(索引) 取 0x508000 表项并循环 5 项调 0x4781C6(index,value,0,0)。控件 ID：复选框 0x406..0x40A、数值 0x7D6..0x7DA、加号 0x7E6..0x7EA、减号 0x7EB..0x7EF、点数 0x7DB、重置 0x7D1、确认 0x2。


## 内嵌字节映射表 0x41CEAB（33项）与 0x4303C8（20项，6.6）

ID: `mechanism.65.embedded-byte-tables.3ef7`；状态: `candidate`；证据: `static-verified`

0x41CEAB 是 33 字节随机替换表，三基底字节完全一致（hash 1b66f63ab303fa0a）：读取函数 f(mod,idx)=(0x4101D9 随机值 & mod)!=0 ? table[idx] : idx，6.4/6.5 入口 0x41CE8B、6.6 入口 0x41CE8C，索引来自对象 +0xC（getter 0x418C90）。0x4303C8 是 6.6 独有的 20 字节物品类型表（hash c54301dd32761700），0x43038B 读取装备槽0物品的 +0x11 类型后查表，调用链 0x43F931→0x417A38→0x43038B；表仅覆盖类型 0..0x13，之后为 0x90 填充。


## 装备升级经验阈值与等级上限（三基底）

ID: `mechanism.65.equipment-growth-thresholds.3ef7`；状态: `canonical`；证据: `static-verified`

0x408304..0x40832C 按 0x40B4E1 的普通/特殊分支写入装备升级阈值与等级上限。6.4 普通 100/5、特殊 200/9；6.5 普通 150/5、特殊 200/9；6.6 普通 100/9、特殊 200/15。


## 装备槽数量与访问边界

ID: `mechanism.65.equipment-slot-bound.3ef7`；状态: `canonical`；证据: `static-verified`

装备槽数量为 3（下标 0..2），每槽 3 字节；0x4065F0 = byte[record+0x2E+slot*3]，多个调用点用 slot<3 上界比较。


## 6.6 字体名称表 0x500030 与 CreateFontA 包装 0x41EBA3

ID: `mechanism.65.font-name-table.3ef7`；状态: `candidate`；证据: `static-verified`

6.6 在 0x500030 新增 5 项字体名称表（16 字节/项，GBK 内联字符串）：0 宋体、1 楷体、2 黑体、3 仿宋、4 微软雅黑；6.5 同址为指针表、6.4 为小值数据。0x41EBA3 包装 CreateFontA：nHeight=[ebp+8]、nWidth=[ebp+0xC]、nWeight=[ebp+0x10]、lpszFace=[ebp+0x14]，字符集固定 0x86（GB2312_CHARSET）、质量 4（PROOF_QUALITY）、其余 0。字重常量 0x190=400、0x258=600、0x2BC=700；字高统一 MulDiv(pt, GetDeviceCaps(LOGPIXELSY=0x5A), 72)。0x41EB48 以 byte[unit+0x19]*0x10+0x500030 选择字体。


## 公式常量站点三基底一致性审计

ID: `mechanism.65.formula-site-cross-base-audit.3ef7`；状态: `canonical`；证据: `static-verified`

对 160 个带地址提示的公式常量和 91 个 dm-constant 精确站点做三基底同址比较：6.5 的 91 个期望字节全部匹配；同一 VA 在 6.4 仅 38/91、6.6 仅 45/91 匹配；464 个站点观测中 235 个三基底完全一致、229 个存在差异。


## 引擎通用常量与全局表锚点普查（三基底）

ID: `mechanism.65.engine-general-constant-census.3ef7`；状态: `candidate`；证据: `static-verified`

对三基底全部可执行节做线性反汇编并建立函数级常量/数据引用索引：6.4 为 481963 条指令/3287 个函数，6.5 为 488079/3372，6.6 为 503694/3552。以 EXE 内嵌表地址为锚点定位通用系统：兵种相克 0x4D1A80、兵种属性矩阵 0x4D20C0、策略战斗 AI 0x4D1600、策略训练 AI 0x4D1690、策略地形可用性 0x420ACC；特效专属表被排除在通用常量清单之外。


边界：

- 函数计数依赖启发式边界，嵌入数据和尾部共享会造成合并/拆分，不能当作语义等价证明。
- 签名聚类只比较前 32 条指令，不证明函数整体相同。
- 常量频次只用于排序工作清单，不用于推断语义。
- 普查不包含特效参数、特效 ID 和单个特效专属数值。

## 兵种相克百分比表与物理伤害乘算

ID: `mechanism.65.job-series-counter.3ef7`；状态: `canonical`；证据: `static-verified`

兵种相克是 EXE 内嵌的 40×40 字节表，索引为攻击方兵种系×40+防守方兵种系，值为百分比（100 中性）。物理伤害在基础值、能力差与随机修正之后按该百分比乘算，非 100 时结果至少为 1。三基底共用字节完全一致的查表与乘算代码，但表值分别不同。


## 引擎通用常量覆盖台账 v14（第 1–149 轮）

ID: `mechanism.65.engine-general-coverage.3ef7`；状态: `candidate`；证据: `static-verified`

第 1–149 轮覆盖 98 个通用域（列表实数）：77 resolved、19 partial、2 unresolved。第 140–149 轮新增/提升：40 条文本对象写入方 0x42AF6F（索引>=0x28 跳过、'0' 停用、'*' 引用 0x506000 字符串指针表）、练武场上下文 +0x04/+0x08/+0x09/+0x0A 与 0x3FE 单位表上界哨兵（0..0x3FD 有效）、0x4237F9 费用公式（等级×10 或 2×0x40D8A9）与 0x423820 资金校验/0x43BFD4 扣款、0x42DE63 三模式选择框与 0x423842 分派、剧本取参器 0x4183F7 类型码（1/4/5/2/0x38/0x39，变量间接 ~ax-1→0x502000）与主分派表 0x410A38 全 126 项（0x68 练武场、0x72 信息传送、0x76 区间守卫、0x77 变量算术）、设置块 +0x05 场景类别缓存（章节 3 存档头 +0x04 来源）。剩余缺口集中在 0x423842 edx 运行期值、0x4A3E77 运行期槽位、11 层逐层用途、0x4B4250+0x64/+0x68 写入方、0x42C9FC 0x2E31 文本表、0x47D8DF 子命令业务语义。


## 全局模式开关 0x505EC8/0x4B3D18 与 6.6 命中门控

ID: `mechanism.65.global-mode-flags-hit-gate.3ef7`；状态: `canonical`；证据: `static-verified`

6.6 命中门控的 dword[0x502000+0xFB2*4] 实际等于 0x505EC8。6.6 三条件为 0x505EC8==0、0x4B3D18==0、unit+5==0，全满足时命中置 100。0x505EC8 在 6.5 还用于 AI 评估与命中重试的 byte==1 分支。


## UI/战斗/插件全局状态区 0x500AAC..0x500ADF 与 6.5 字段映射

ID: `mechanism.65.global-ui-state-block.3ef7`；状态: `candidate`；证据: `static-verified`

6.6 0x500AAC..0x500ADF 是 UI/战斗/插件共享的紧凑全局区：0x500AAC 列表框项索引（SendMessageA LB_GETITEMDATA 0x199）、0x500ABC CmdIcon.dll 模块句柄（LoadLibraryA 结果）、0x500AC0 当前战场单位指针、0x500AC8 行动单位指针、0x500ACD 当前动作码、0x500ACE 重入计数、0x500AD2 UI 命令 ID（WndProc WM_COMMAND）、0x500AD3 伤害应用标志、0x500AD7 UI 模式、0x500AD8 输入状态字、0x500ADC/0x500ADD 两位十进制数、0x500ADA 有效物品计数、0x500ADE AutoDll.ini 启用标志、0x500ADB Z 键热补丁开关；0x500AE0 为 0x90 字节 UI/绘制状态结构。字段在 6.5 分散于 0x4CE74C..0x4CE7FF，逐字段对应而非等距搬移。


## 0x4B422C 网格边界字语义更正

ID: `mechanism.65.grid-bound-word-correction.3ef7`；状态: `candidate`；证据: `static-verified`

0x4B422C（word）不是地图宽高，而是可保存/恢复的 2 字节网格/光标边界字。6.4/6.5 在 0x4516BF 写 0x0104、在 0x4D11C7 写 0x0105；6.6 同址为 NOP。该条更正第 8 轮“地图宽高”的初判。


## 全局二维网格尺寸字 0x4B422C/0x4B422D

ID: `mechanism.65.grid-dimension-pair.3ef7`；状态: `canonical`；证据: `static-verified`

0x4B422C 为网格宽度/行跨度，0x4B422D 为高度。0x403789 以 y*width+x 计算索引，0x404E30 以 x<width、y<height 做边界检查，0x44C1C2 读取资源头两字节后分配 0x640 字节并按 width*height 拷贝。0x4516BF/0x4D11C7 分别设置 4×1 与 5×1，列表 UI 复用同一全局；0x41D2B8 从 0x500AA0+0x12 快照恢复。


## 历史情报模板 341：宿主 0x41C3D7 与文本打开链 0x42F699

ID: `mechanism.65.history-intel-341.3ef7`；状态: `candidate`；证据: `static-verified`

历史情报入口 0x41C3D7：工作区 0x4FFF80。当 [workarea+8] 指向的首 dword 为 0 或 byte[0x492E20]>=4 时，以 0x48E88C 为文本基址（章节>=4 用 0x48E88C+0xB 变体）调 0x42F699(0, base) 打开文本；否则置 byte[0x48E8C1]=2，以 DialogBoxParamA(hInstance,0x155=341,hwnd,0x46D0F8) 打开「历史情报」对话框，返回后清 0。0x42F699 先 0x42F214(&arg,0x4B1A18,1) 初始化，再 0x42C602/0x42C557 准备文本，按 byte[0x500CB0]==1 与 arg 分支绘制/翻页。模板 341 为 DLGTEMPLATE 241×265、标题「历史情报」、2 控件：0x407（class ord 133 信息筛选下拉框）与静态「信息筛选」。


## 命中率的高度/方向坐标修正

ID: `mechanism.65.hit-height-direction-modifier.3ef7`；状态: `canonical`；证据: `static-verified`

命中率在基础曲线后按攻守坐标与朝向修正：class 0/1/2 分别追加 0/5/10 个百分点比例；满足 0x406710(defender)!=1 与 byte[0x500E9A]==1 时再追加 5%；0x408EEE 封顶 100、用 0x410EDB 取下限并保底 1。


## 命中重试机制的三基底差异

ID: `mechanism.65.hit-retry-cross-base.3ef7`；状态: `canonical`；证据: `static-verified`

6.4/6.5 使用“最多 2 次、命中>=85、每次扣 10”的重试循环；6.5 额外在 byte[0x505EC8]==1 时跳过。6.6 删除循环，改为 dword[0x502000+0xFB2*4]、byte[0x4B3D18]、byte[unit+5] 三条件门控，条件全满足时命中置 100。


## 物品使用效果码 +0x10 与效果范围表 0x4D1400（36项）

ID: `mechanism.65.item-effect-code-and-range-table.3ef7`；状态: `canonical`；证据: `static-verified`

物品 +0x10 为使用效果码（0xFF=无，有效 0x01..0x25）；使用时写入 0x4B4250+0x1B85 的 4 槽效果缓冲，0x41E307 逐槽调用 0x45288B。效果码经 0x4D1400 的 36 项 dword 指针表映射到 0xFFFF 结尾的 word 列表；每个 word 的低/高字节为两个半径，0x436616 生成四角并调用 0x437AFF 写地图格，6.6 的 0x42A840 以同样四角做命中判定。该表三基底 hash 不同，差异集中在 [03]/[06]/[09]/[10]/[18]，6.6 新增 0x42A6B8/0x42A7FD 两个消费者。


## 6.4 物品装载链与 0x41FECC 解析式旋转

ID: `mechanism.65.item-loader-64-parser.3ef7`；状态: `canonical`；证据: `static-verified`

6.4 物品装载链：0x41B639 初始化序列 → 0x41B666 载入 DATA.E5 块0（人物）→ 0x47D988 载入块1（物品）到复用缓冲 [0x496F60] → 0x47D9E1 有界解析循环调用 0x41FECC 逐条重排 +0x12..+0x14 → 读 star.e5（ReadFile 容量 0x1022）→ 0x43E67C 复制 0x3B6 dword（0xED8=152条）→ 解析槽 104..254 → 0x41BABB 统计有效物品数到 0x4CE7BE。6.4 槽位上限同为 255。更正第 55 轮“6.4 无旋转”：旋转由 0x41FECC 完成而非内联。


## 商店价格字段 item+0x13 的消费边界（负结果）

ID: `mechanism.65.item-price-consumption-boundary.3ef7`；状态: `candidate`；证据: `static-verified`

扫描三基底全部可执行节的 mem.disp==0x13 后，未发现 item+0x13 的直接价格读取或 ×100 计算；唯一同偏移读取 0x4010EE 是记录 dword 重排。商店列表 0x466AE3 只读取物品 ID 与可用性布尔值。价格消费链尚未闭合，不登记为公式。


## 物品记录 25 字节字段语义与 DATA.E5+star.e5 装载链

ID: `mechanism.65.item-record-fields.3ef7`；状态: `canonical`；证据: `static-verified`

25 字节物品记录字段逐项展开：+0x10 使用效果码、+0x11 类型码、+0x12 买价/100、+0x14 装备子类型、+0x15 基础值、+0x17 每级成长、+0x18 存在/启用标志；+0x13 仍未定名。装载链为 DATA.E5 块1（104 条）＋ star.e5（6.5 0xED8=152 条、6.6 0x27D8=408 条）拼接：6.5 归一化 255 槽、6.6 归一化 512 槽；6.5/6.6 装载时内联旋转 +0x12..+0x14（同哈希 4aabbdb8c85a23bf），6.4 经 0x41FECC 解析式完成同一重排。买价 0x40E070=byte[+0x12]×0x64，卖价 0x40B477=买价的 75%（0xFF→0xFFFF），配合 0x4673xx 排序比较器闭合价格消费链。0x40B3D7 给出 value=byte[+0x15]+(count-1)×byte[+0x17]。6.6 新增 20 项类型表 0x4303C8。


## 物品记录装载后的 0x12..0x14 旋转

ID: `mechanism.65.item-record-normalization.3ef7`；状态: `canonical`；证据: `static-verified`

物品表装载后对每条记录清空 +0x0E，并旋转 +0x12..0x14：新[0x12]=旧[0x13]，新[0x13]=旧[0x14]，新[0x14]=旧[0x12]。6.5 装载到 0x4A1140，循环 0xFF；6.6 装载到 0x49F820，循环 0x200；6.4 已重定位。


## 物品/装备记录表 0x4A1140（6.6: 0x49F820）

ID: `mechanism.65.item-record-table.3ef7`；状态: `canonical`；证据: `static-verified`

物品/装备记录在 6.4/6.5 基址 0x4A1140、步长 0x19（25 字节）、索引 0..0xFF；6.5 有 55 处基址引用。6.6 不再引用 0x4A1140，改用 0x49F820 并通过访问器 0x4837C2（index*0x19+0x49F820）取记录；记录 +0x11 字段在 0x4303B4 以 byte 读取。


## 6.6 物品类型→动作/特效编号映射表 0x4303C8 与消费链

ID: `mechanism.65.item-type-action-mapping-66.3ef7`；状态: `candidate`；证据: `static-verified`

6.6 独有 0x4303C8 为 20 字节映射表（01 06 05 13 07 08 01 20 15 16 00 01 06 0C 00 01 00 01 0C 0D），索引为物品记录 +0x11 类型码 0..0x13，输出动作/特效编号 0..32。唯一消费链为 0x43F8C0→0x417A38→0x43038B：先 0x41CE8C(1) 随机替换，再 0x430351（0x42518F(0x6D,0,1,0)）评分门控；评分==0 返回随机替换值，否则读装备槽 0 物品（rec+0x2E）类型并查表。调用方随后与哨兵 0x0B 比较，0x423FE8(4) 非零时强制 0x0B。6.5 同位置走 0x4E4000 搜索包装 + 0x417A35 随机替换，不做类型映射。


## 物品类型分类与子类型映射

ID: `mechanism.65.item-type-classification.3ef7`；状态: `canonical`；证据: `static-verified`

物品类型分类：item+0x11 <20→0；20..25→1；>=26→item+0x14 子类型。子类型映射：<26→type/2；>=26→item+0x14+11。三基底字节一致。


## 兵种属性矩阵 8×40 与第 6 行伤害百分比

ID: `mechanism.65.job-series-attribute-matrix.3ef7`；状态: `candidate`；证据: `static-verified`

0x4D20C0 是 8 行×40 兵种系的字节矩阵。第 6 行（0x4D21B0）是 90..130 的百分比修正，策略伤害后段按 damage*row6[series]/100 乘算；第 5 行是 0..2 枚举并被 AI 评分比较 ==2；其余行为布尔/占位标志。三基底矩阵不同。


## 兵种穿透/属性码表 80×1

ID: `mechanism.65.detailed-job-penetration.3ef7`；状态: `candidate`；证据: `static-verified`

0x407881 是 80 字节的兵种属性码表，按兵种 ID（unit+0x2B）索引。0x40782D 在模式/状态/哨兵检查通过后返回 table[jobId]；0 为缺省，6.5 还出现 1/4/9/10，6.6 出现 1/4/7/9。


## 图层/图块缓冲常量：0x1B00、0x6C00、0x12900、0x3000、0xC000 与 0x430020 拷贝函数

ID: `mechanism.65.layer-block-constants.3ef7`；状态: `candidate`；证据: `static-verified`

高频 imul 常量构成本图块/图层缓冲布局：0x1B00=6912 为战场单层字节数（第 53 轮），0x6C00=27648=4×0x1B00（4 层），0x12900=76032=11×0x1B00（11 层）；0x3000=12288=64×64×3（24bpp 图块），0xC000=49152=4×0x3000（128×128）。0x430020（紧随 0x430000 跳转表之后）接受宽高参数，观察到 0x30(48)/0x40(64) 两种块拷贝。0x40446E 以 byte[0x4927F0]×0x12900 选择记录块；0x41ED07 以 byte[rec+0xD]×0x12900+0xF300 定位图像数据。


## 11 层图层块 0x12900：0xF300/0x6C00 偏移、0x4303C4 块拷贝与 0x43E549 方向映射

ID: `mechanism.65.layer-buffer-11.3ef7`；状态: `candidate`；证据: `static-verified`

图层块大小 0x12900 = 11 × 0x1B00（单层 0x1B00=6912，4 层 0x6C00，6 层 0xA200，8 层 0xD800，9 层 0xF300）。6.5 中共 22 处 0x12900 引用；层偏移按 0x1B00 对齐：0x6C00=第 4 层、0xA200=第 6 层、0xD800=第 8 层、0xF300=第 9 层，其余层经基址+n*0x1B00 或寄存器偏移访问。0x43FE2C 按 byte[obj+4]*0x12900 从 0x4AB00C 池分配并整块清零；0x41C7E9 在非战斗模式（0x505FDC==0）以 byte[rec+2]*0x12900+0xA200 取块，否则 push 0x6C00 + 0x4B7A20 调 0x408ECA。0x40446E 以 byte[0x4927F0]*0x12900 选块，并用 0x43E549 把方向 0/1/2/3 映射为 1/2/0/2；0x41ED07 以 byte[record+0xD]*0x12900+0xF300 取源（第 9/10 层），按 0x6C00 目标步长循环 2 次调 0x4303C4 复制 0x30×0x30 块。0x4303C4(src,dst,w,h)：3 字节/像素，经 0x41C444 保留目标 alpha 写入源 RGB。0x448BCE 另经 0x4015B1（0x4AE4C8 池）分配 0x37800 临时合成区（0x448B96）：源为 byte[+0xD]*0x12900+0xD800 的 0x30×0x30 块，经 0x4303C4 拷入后循环 9 次，每次 0x47FCFD 拷 0x6C00（=0x60×0x60×3 帧）、0x40690C 白色 0xFFFFFF 绘制、0x443C1D 按 0x60×0x60 贴图；0x37800=0x6C00×8+0x1800，实际单帧仅用 0x6C00。地图图形页（第129轮）：0x1E900 = 0x12900 层块 + 0xC000 尾块，是 0x4AAFF4 竞技场内的页步长；页 0 基址 0x24C00、页 1 基址 0x43500；页尾缓冲基址 0x37500=页0+0x12900（每页步长同为 0x1E900），页内第 4 层 0x2B800=页0+0x6C00；0x40155F(offset)=0x47FA40(0x4AAFF4,0,0,4)。


## 关卡/地图全局描述结构 0x500AE0（0x90 字节，6.5 为 0x500AA0）

ID: `mechanism.65.level-context-struct.3ef7`；状态: `candidate`；证据: `static-verified`

0x500AE0 是 0x90 字节关卡/地图全局描述结构（6.5 对应 0x500AA0，均 20 处引用；初始化 0x415CD5 以 0x47FD13(0,0x90,0x500AE0) 清零）。已定位字段：+0x00 首指针（0x420173 作 this）、+0x08 计数（0x40A56F +5）、+0x0C 关卡/资源状态 ID（0x41D29B→[+0xC80]，0x40ADAB 反向恢复并置 0x3CFFFF）、+0x10 模式（cmp 1/2）、+0x11 开关（0/1）、+0x12 地图宽高字节对（写入 0x4B422C）、+0x14 子窗口句柄（非 0 时替代 0x4B6A68）、+0x1A 辅助 word（→[+0x642]）、+0x1C 表指针。


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

## 三个全局内存池 0x4AE4A8/0x4AE4C8/0x4AB00C 与分配器 0x47FA40

ID: `mechanism.65.memory-arenas.3ef7`；状态: `candidate`；证据: `static-verified`

三个全局内存池：0x4AE4A8（包装 0x40162C）、0x4AE4C8（0x4015B1）、0x4AB00C（0x401655）。包装以 eax=size、对齐 4 调 0x47FA40(arena,size,0,4)。0x47FA40：edx=min(size,dword[arena+4]) 容量钳位；按 byte[arena+0x10] 分派——模式 1/4 返回 dword[arena+0xC]+size 的线性指针，模式 2 调 0x47F9E2(size,flag,extra)，其他返回 0。模式 2 的 0x47F9E2 以 0x4000（16KB）为块粒度：esi=size>>14、size&=0x3FFF，循环最多 4 次调用 0x47F96C（本构建为空桩 ret 8）。第95轮 0x41ED07 的图层缓冲即经 0x401655 从 0x4AB00C 池分配。


## 功勋分配表 0x508000（102×5 word）与点数池 0x505F40/0x505F3C

ID: `mechanism.65.merit-table.3ef7`；状态: `candidate`；证据: `static-verified`

0x508000 是 102 人（0x66）× 5 个 word（0x0A 字节）的功勋分配结果表，由 0x42ACD2(index)=index*0x0A+0x508000 访问（index<0x66 且 [arg]==1 或 byte[record+0x2A]!=0xFF 时有效，否则 0xFF）。332 确认处理 0x456CB4 把 0x406..0x40A 五个复选框（武/统/智/敏/运）的掩码写入单位记录 +2，并把 0x505F40 传给 0x40BE7D 显示。0x408FA0：byte[0x505F3C]==0 时返回，否则遍历 i=0..0x65，按 byte[record+2] 掩码把未勾选维度的 word 清零，并通过 xchg 把原值累计后加回 dword[0x505F40]（返还公式=被清除项之和）。0x423EAD：0x42ACD2(0) 有效时清零五项，arg!=0 且 byte[0x505F3C]!=0 时同样把原值之和加回 0x505F40。0x505F40 的 5 处静态引用只有两处累加与三处传参，未发现减法点。


## 金钱全局 0x4B077C 与 999999 上限

ID: `mechanism.65.money-global.3ef7`；状态: `canonical`；证据: `static-verified`

0x4B077C 为金钱 dword。0x406C00 结算 0x48E8BD 累加金额：job byte+5>=2 时加到金钱并封顶 0xF423F(999999)，否则从金钱扣除（不足归零），随后清零 0x48E8BD 与 0x500C48。0x423820 比较价格；0x414E92 扣 1000；0x43C00F 扣任意金额。0x406C00 三基底字节一致。


## 移动消耗、地形适应与地图边界

ID: `mechanism.65.movement-terrain-and-map-bounds.3ef7`；状态: `canonical`；证据: `static-verified`

Data.e5 块 4（0xA8A4，0x960）解码为 40 兵种系×60 字节的运行时表（基址 0x4A3517，步长 0x3C）。每行前 30 字节为地形适应（0x41F62A），后 30 字节为移动消耗（0x4060C4），0xFF 不可通行。0x4065AD 取移动消耗；0x46CC12 在可通行时返回适应值；0x459380 做通行判定。地图边界由 0x4B422C/0x4B422D 的宽高字节控制。


## 6.6 独占/搬移锚点批语义：0x487634、0x48693E、0x500BA0、0x493AF0、0x4934B0、0x501BD2、0x501BF0

ID: `mechanism.65.new-anchors-batch-66.3ef7`；状态: `candidate`；证据: `static-verified`

7 个 6.6 独占/搬移锚点：0x487634 为视口像素尺寸打包 dword（low16=宽×48，high16=高×48；0x451B3F 由网格字 0x4B422C/0x4B422D 计算，0x47B59D 置 640×400=0x1900280）；0x48693E 为 BMP 位深标志（0x20=32bpp，否则 24bpp；0x41625B 从图像头写入，0x40E87E 决定 ×4/×3），6.5/6.4 对应 0x4CE73C；0x500BA0 为 0xFFFF 空哨兵的 word 数组（6.5/6.4 为 0x4FFDF6）；0x493AF0 为按 ID-0xA0 索引的字节计数数组（带 0xFF/cl 钳位增减）；0x4934B0 为 0xC/0xD 掩码字节标志数组；0x501BD2 为 >=2 时启用新分支的模式字节；0x501BF0 为地图可见矩形缓存 dword（b0=left、b1=top、b2=width、b3=height；0=不受限；0x4362E6 点-矩形判定，宽高×0x30 驱动视口）。


## 统一支付链与练武菜单价格

ID: `mechanism.65.payment-chain.3ef7`；状态: `canonical`；证据: `static-verified`

0x4237F9 计算价格：mode 0 取 byte[unit+0x17]*2*10，mode 1 取 byte[unit+0x2C]*10；0x423820 比较 0x4B077C 并在不足时提示 0x500CA7；0x43BFD4 显示 0x500C9C『支付%d金？』，确认后扣款并写 0x4AC63C=3。0x474E0E 的 普通模式/单挑模式/自动提升 菜单由 0x423842 处理。


## 个人经验公式常量的三基底一致性

ID: `mechanism.65.personal-exp-cross-base.3ef7`；状态: `canonical`；证据: `static-verified`

个人经验函数 0x4037A3 的常量在 6.4/6.5/6.6 一致：基础 2×等级差+6、等级差钳位 -1..47、特殊击杀 +48、普通击杀 64/(max(攻方等级-守方等级,0)+2)。审计中的同址差异是函数体移位；6.6 额外有 [ebp-0xC]==0 守卫。


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

## 物理伤害主链通用常量与 6.6 分支差异

ID: `mechanism.65.physical-damage-constant-chain.3ef7`；状态: `canonical`；证据: `static-verified`

物理伤害主函数 0x43BC62 的非特效路径：攻方等级+25，双方能力差/2（低方保底 1），特殊差值分支 6.4/6.5 为 abs(diff)*5%，6.6 为 (12-diff)*N%，随后兵种相克百分比，最后 0x4E6000 处理。关键常量 25/2/1/5/12/100 均给出站点字节。


## 物理伤害等级差百分比表 0x4D1A80 与随机浮动

ID: `mechanism.65.physical-level-table.3ef7`；状态: `canonical`；证据: `static-verified`

0x426737 以攻方/守方等级映射值 a、d 计算 idx=a+d*40，查 41×41 表 0x4D1A80，再叠加守方随机值、减去攻方随机值，负值归零；返回 100 不缩放，否则 damage=damage*pct/100 且至少 1。函数三基底同哈希，6.6 仅重平衡表首值（100→80/95）。


## 物理伤害距离/范围修正 0x4E6000

ID: `mechanism.65.physical-range-correction.3ef7`；状态: `canonical`；证据: `static-verified`

物理伤害链末尾 0x4E6000 依次调用 0x4E0000（范围查询，参数 0/0xFF/0xFF/0xC4/0xFF/1/0）与 0x4E008F（mode 1 与 mode 0 距离判定）；仅当 mode1 命中且 mode0 未命中时按 0x425AD9 对伤害做百分比缩放，返回 base+修正。坐标取自 job 记录 +6 字的高低字节。该函数不读取天气或临时属性块。


## 四快捷窗口宿主 0x496F38（模板 297）与设置 +0x10 显示开关

ID: `mechanism.65.quick-window-host.3ef7`；状态: `candidate`；证据: `static-verified`

0x496F38 是四快捷窗口宿主：+0x00..+0x0C 为 4 个窗口句柄，+0x10 为 4 位隐藏掩码（bit=1 隐藏，结束时常清 0），+0x14/+0x18/+0x1C 在初始化时置 1（+0x14+i*4 另存各窗图像句柄）。0x419949(this,flag) 负责创建与布局：对每个空句柄调用 CreateDialogParamA(hInstance=[0x4B6A60]、模板 0x129（RT_DIALOG 297：53×56、宋体 9 号、单静态控件 ord 128）、父窗 [0x4B6A68]、过程 0x4195AA、init=i)；随后对 dword[0x505F00] 位未置的槽位 MoveWindow(handle,x0-0x5A,y0-0x32*(i+1),0x32,0x32,1)；flag==0 时 ShowWindow(handle,5)+RedrawWindow(handle,0,0,0x101)；结束 call 0x4768C0 并把 +0x10 清 0（全部可见）。业务语义（第152轮）：对话框过程 0x4195AA 在 WM_INITDIALOG 按 lParam=i 用 0x423C4B(0x155+i) 加载图像 341..344 并 SendMessage(静态 0x56B=1387, STM_SETIMAGE 0xF7) 显示；点击 0x56B 时 0x4196F8 以 0x409B11 反查索引，先隐藏全部（0x423CCE），再按索引执行 0=「%s，卖掉物资！」、1=「%s，买进物资！」（后接 0x461CF6(1)）、2=「%s！打开仓库！」（后接 0x461C88），格式串位于 0x48B49B+index*0xF，%s=0x40C755(byte[0x407D1A+index]) 取当前武将名（0x407D1A={01,01,00}）；索引 3 为场景切换：0x418597(0x492F90,1) 检查双方 20 槽名单非空后 ShowWindow([0x4B7508],0)、0x41196C(0)、置 dword[0x4AE4C0]=1（0x40B900 消费该标志）。设置 +0x10 是该组窗口的显示开关：0x41196C(arg) 写入 +0x10，章节==2（0x41EDEF(0x4AC63C)==2）时立即调 0x426BA0；0x426BA0=0x426B52(0x4034D2())，0x426B52(value) 以 0x406431=GetMenuState(GetMenu([0x4B6A68]),1,0x400)&1 读取菜单第 1 项勾选位，与 value 不同才应用：0x4759BC(value) 经 0x41F445 向 [0x4B6A8C] 与表 0x48EA90（步长 0x14，最多 13 项）广播 WM_USER+1(0x401)/wParam=0x65，并以 EnableMenuItem 启用菜单 0..2；随后 value==0 调 0x423CCE 置 bit0..3（隐藏），value!=0 调 0x44852B 清 bit0..3（显示）。0x411991 在章节!=3（0x40B922()==0）且 +0x10!=0 时，以 byte[0x501FFF]==0 ? flag=1 : flag=0 调 0x419949(0x496F38,flag)。0x501FFF 是快捷窗口展开状态：0x415B9C 置 1（脚本操作码 0x06 打开分支 0x415B4F）、0x40700A 置 0（关闭分支），0x4137AB 在关闭前调 0x429CAB，0x42A183 回城时按原状态重建。0x4B09DB 是出战/参战部队数量（1..20，第155轮更正）：0x415B96 写入 max(param2,1)、0x415BB1/0x415BF3 关闭分支写 1；读取点 0x416526（索引边界）、0x418628/0x4186D9（名册收集与 0x45E6B3 数组构建）、0x41E8AB（小地图标记绘制上界）。操作码 0x06 还经 0x415C0D 把最多 5 个类型 0x38 的敌 ID 写入 word[0x4B09DC+idx*2]（0x4B0A2C 循环）、5 个类型 0x39 的我方 ID 写入 word[0x4B0A04+idx*2]（0x4B0A30 循环），各 20 槽。


## 33 项随机变体编号表 0x41CEAB 与 0x41CE8C 替换函数

ID: `mechanism.65.random-variant-table.3ef7`；状态: `candidate`；证据: `static-verified`

0x41CEAB 是 33 项（索引 0..32）随机变体编号表，三基底逐字节相同（01 06 03 04 12 13 0C 08 12 1F 0A 00 0D 21 0F 16 11 12 25 0C 0C 16 22 01 20 1D 03 1C 1D 23 1F 03 24）。0x41CE8C(mod, code) 先用 0x41CDEE 计算 (0x4101D9(0x5A+mod,0x76,3,0) & mod)，非零时返回 table[code]，否则原样返回。人物模板链 0x401DFF 以模板 +0xC 为索引、mod=2 使用该表，结果被 5 个调用点作为动作/图像编号使用；6.6 物品类型动作链（0x43038B）以 mod=1 使用同一表。0x21（33）是编号越界哨兵，遇到时改走 0x43F8C0 默认计算。


## 存档文件四区块布局：A 0x30000 / B 0xD4F0 / C 0x313D / D 战场状态

ID: `mechanism.65.save-file-format.3ef7`；状态: `candidate`；证据: `static-verified`

保存入口 0x40531A：0x4288F4 生成 SV\SV%03u.E5S → 0x418F5C(mode=2) 打开 → 经 .api 段 [0x4BE046] 间接钩子（参数 0x501AD0）→ 依次写 4 个区块：A 0x30000 字节（源 0x501000）；B 0xD4F0 字节（源 0x496F60，由 0x4053CC 序列化：魔数 5、+1..+4 四个头字节、+5/+0x1B 两段字符串、+0x32 的 0x2BC 字节章对象、+0x2EE 的 word、+0x2F0 的 0x80×0x24 记录、+0x14F0 的 0x400×0x30 单位记录）；C 0x313D 字节（0x405524 按 0xFA0/0x181/2/8/0x800×4/8/0x0A 顺序打包 0x492F90）；D 战场状态（0x407A37，源 0x4B3D08：魔数 5、+1/+2 字节、+0x1E 头、0xFA 个单位、0x640 尾）。读取入口 0x41888D：0x418F5C(mode=0) → 0x419184 读 0x30000 并校验首字节==5 → byte[0x500FFF]=1 → 正式读 0x30000 到 0x501000 → 0x419102 读 0xD4F0 → 读 0x313D → 0x4189DA 读战场区块 → 关闭并返回 1。文件对象 0x418F5C/0x419102/0x419184/0x41923C/0x4192C5 三基底同哈希；0x408F2E 单位记录序列化 0x30 字节三基底同哈希；区块 C/D 在 6.4=6.5、6.6 不同，但 6.6 读取端仍用 0x30000/0xD4F0/0x313D/魔数5。


## 存档/读档槽位编号与文件命名常量

ID: `mechanism.65.save-load-constants.3ef7`；状态: `canonical`；证据: `static-verified`

存档编号 n=(slot==0x14)?0:page*20+slot+1；页字节 6.4/6.5=0x4CE78F、6.6=0x500ACF。6.5/6.6 用 'SV\SV%03u.E5S'，6.4 用 'SV\SV%s.E5S' 加三位补零串；外层路径 'E5\%s'。保存 UI 0x40526B、读取 UI 0x405696（6.6: 0x40569C）、保存执行 0x40531A、文件名构建 0x4288F4（6.4: 0x4288F3）、路径包装 0x4138BE（6.6: 0x42BA60）。槽位 0x14 为自动存档。


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

## 剧本解释器上下文与脚本地址缓存 0x500AB0/0x500AB4

ID: `mechanism.65.script-context-caches.3ef7`；状态: `candidate`；证据: `static-verified`

剧本解释器上下文是带 vtable 的对象（[ctx]=vtable）：+0x00 vtable、+0x08 脚本流累计字节计数（0x416C54 后 add [ctx+8], eax+5）、+0x0C 脚本流读取地址（绝对地址，0x4183F7 的读取起点，并参与缓存公式）、+0x10 opcode 快照、+0x14 等待中的分支目标地址（-1 哨兵）、+0x2C 执行中标志、+0x2E 当前动作码、+0x34 开关。0x500AB0=[ctx+0xC]-2（动作码 1 分支，0x410A0B）；0x500AB4=[ctx+0xC]+0x40FCB2(ctx)（[ctx+0x14]<0 分支，0x41088B）。6.4/6.5 对应槽位为 0x4CE74C（0x410A0B）与 0x4CE75C（0x410891）。消费链：操作码 0x76 处理器 0x416C41（两基底处理表 0x410A38 第 118 项）先用 0x4183F7 读 4 字节操作数推进 ctx，再以 [0x500AB0,0x500AB4] 区间判定当前位置（6.5 用 [edx-0x10] 读 0x4CE74C，6.6 用 [edx-4] 读 0x500AB0），命中时 cl=0x76 哨兵，与 0x4109E6/0x4105FF 的 0x76 特判衔接。0x4109E6 以 0x40FCB2 取得的动作码写入 +0x2E，并以其-2 索引 0x410A38 处理表（6.6 上限 0x7B，6.5 为 0x79）；0x4105FF 为解释器主分派，0x410857 为动作处理器。取参器 0x4183F7（第149轮）：先以 0x40FCB2 从 ctx+0x2E 读 token 再按 type 分派——type=1 原样返回 token，type=4 走 0x40FC90（数值/负号，负值时 byte[ebp-0x10]<0x6E 才取 -eax），type=5 走 0x40FC62 返回文本指针，type=2/0x38/0x39 读 word 且 0xEFFF<=ax<0xFFFF 时按 ~ax-1 索引 dword[0x502000+idx*4]，其余（3/9/0x4F）为纯 word。主分派表 0x410A38 在 6.5 为 126 项（索引=opcode-2，0x7A..0x7F 空实现 0x4D0000）：0x68=0x4103F0 练武场命令（操作数类型表 0x40E388={0x02,0x02,0x4F}）、0x72=0x47D89E 信息传送（类型 4,5）、0x76=0x416C41 区间守卫（类型 4）、0x77=0x416C87 变量算术（类型表 0x416C82={0x51,0x04,0x53,0x52,0x04}，按目标类型 0/1/2 解析 0x506000 字符串表或 0x502000 变量地址，运算码 p2>=3 时偶数 div、奇数 imul，经 0x425AD9 与 0x410471 写回）。0x77 的 0x506000 字符串表项上限 0x12F（303），0x502000 变量上限 0x1000。三基底 EXE 内无剧本命令中文名表（GBK「信息传送」「练武场」命中 0，仅运行时文本存在）。


## 剧本处理表容量、索引偏移与空实现区间

ID: `mechanism.65.script-handler-capacity.3ef7`；状态: `canonical`；证据: `static-verified`

0x410A38 为 126 项 dword，索引=opcode-2，覆盖 0x02..0x7F。0x7A/0x7B 自 6.4 已实现（0x416DCD/0x415093）；6.4/6.5 的 0x7C..0x7F 全为 0x4D0000；6.6 新增 0x7C/0x7D（0x4284A2/0x47E9F0），仅 0x7E..0x7F 为空。第149轮补：0x68=0x4103F0（练武场命令，操作数类型 0x40E388={0x02,0x02,0x4F}）、0x72=0x47D89E（信息传送，类型 4/5）、0x76=0x416C41（区间守卫，类型 4）、0x77=0x416C87（变量算术，类型 0x416C82={0x51,0x04,0x53,0x52,0x04}）；6.5 去重后 121 个不同处理器，6.4 同，6.6 为 123（新增 0x7C/0x7D）；6.6 的 0x68 处理器地址偏移为 0x4103EE。


## 数字记号解析器 0x426E64（- 负号 / * 变量引用）与全局变量数组 0x502000

ID: `mechanism.65.script-number-parser.3ef7`；状态: `candidate`；证据: `static-verified`

0x426E64(src) 解析十进制整数记号：起始可带 '-'（负号）与 '*'（变量引用）前缀，随后读取连续 '0'..'9'；返回 eax=数值、edx=已消费字符数（前缀数+位数），无数字返回 0。'*' 前缀表示 eax=dword[0x502000+value*4]，'-' 前缀对结果取负。0x502000 是全局 dword 变量数组：写入 0x407932/0x42CAF2/0x42CC2D；读取 0x41516B/0x416CFE/0x416D42/0x418493/0x4202E2/0x4246B4/0x425C93/0x426863/0x426EED/0x43B502。0x42C6C5(stream,N,size,dst) 循环 N 次调用 0x426E64，把 eax 写入 dst，并把 stream 前进 edx+1（跳过记号后的分隔符）。0x502000 另有按单位槽写入路径（第146轮）：0x407932 以槽 idx 写 dword[0x502000+idx*4] = (byte[unit+0xD]&2)>=2 ? 1 : 0（unit 由 0x4061F9 取得），说明该数组也被单位行动/状态分支使用。


## 脚本处理体 0x7A/0x7B/0x7C/0x7D 与 6.6 新增项

ID: `mechanism.65.script-opcodes-7c-7d.3ef7`；状态: `canonical`；证据: `static-verified`

0x7A 自 6.4 已实现：0x416DCD 取参后 call 0x4202D8，变量表 0x502000，溢出提示 0x500CC0『变量值溢出』。0x7B 自 6.4 已实现：0x415093 按 0..5 六种操作符比较。6.6 新增 0x7C/0x7D：0x7C 用 0x42DB2C 解析最多 5 个操作数并 call 0x40CB00；0x7D 用子表 0x47EA2F 分派 5 类条件（装备/状态、数值阈值、单位存在、地形、天气）。


## 设置块 0x4B0770 字段与设置项索引 0/1/2（0x40E1D0/0x415E19/0x408808）

ID: `mechanism.65.settings-block-fields.3ef7`；状态: `candidate`；证据: `static-verified`

0x4B0770 是 0x2BC 字节的设置块（存档区块B +0x32 整体复制）。字段：+0x00 选项位掩码（bit0=背景音乐、bit1=音效、bit2=战斗时窗口自动最大化、bit3=战斗时自动显示战场缩小图、bit4=会话窗口不自动关闭；0x41B90F 从 0x406..0x40A 读取）、+0x01 讯息显示速度索引（0/1/2=快/普通/慢，0x40B..0x40D）、+0x02 武将移动速度索引（0/1/2，0x40E..0x410）、+0x03 音量字节（0..100：0x42E218 取控件 0x411 的 TBM_GETPOS(0x400) 写入 +0x03，经 0x42F7FC ×0xA 作 MCI 0x873 参数）、+0x05 场景类别缓存（唯一读取点 0x405412：存档头构造 0x4053CC 在章节 byte[0x4AC63C]==3 时写入头 +0x04，否则用 0x44F9A0 返回 byte[0x4AC63D]；写入点 0x44D2FF 从初始化器 byte[+0] 复制、0x42C0BA 清理置 0）、+0x06 word 为设置项索引1（0x415E19 返回 min(word/2,0x7F)）、+0x0C dword 为设置项索引0（0x40E1D0 直接返回）、+0x10 标志（0x41196C 写入，0x426BA0→0x426B52 应用，1=显示/0=隐藏 4 个快捷窗口）、+0x12 byte 为设置项索引2（0x408808 返回）。0x4118DB..0x41196B 按索引 0/1/2 分派到三个 getter，并与旧值比较返回 -1/0/1（0x4183F7 读到 0x80000000/0x8000 时返回 5 表示无效）。0x41196C 写 +0x10 后，若 0x41EDEF(0x4AC63C)==2（章节 2）则调 0x426BA0；0x411991 在 0x40B922()==0 且 +0x10!=0 时按 0x501FFF 调 0x419949(0x496F38,flag)。存档头写入链（0x4053E4..0x40543B）：区块B +0x01/+0x02 取 0x41EDEF(0x4AC63C)；+0x03 取 0x415E19(0x4B0770)；+0x04 当 byte[0x4AC63C]==3 时取 byte[0x4B0770+0x05]，否则取 0x44F9A0(0x4AC63C)；+0x05 起 strcpy(0x4A1128)，随后 push 0x4B0758 写第二段字符串；+0x32 起由 0x40C482 复制整个设置块。+0x10 另有独立字节 getter 0x4034D2（mov ecx,0x4B0770; movzx eax,byte[ecx+0x10]; ret）。


## 环境设定对话框 KANKYOU：控件清单与设置块 +0x00/+0x01/+0x02/+0x03 写入

ID: `mechanism.65.settings-dialog-kankyou.3ef7`；状态: `candidate`；证据: `static-verified`

环境设定是命名 RT_DIALOG「KANKYOU」：DIALOGEX 220×195、标题「环境设定」、宋体 9pt、25 控件；由 0x44F8EB 以 DialogBoxParamA(模板名 0x48B600="KANKYOU", 父窗 0x4B6A68, 过程 0x41BAD7) 打开。控件：1 确定、2 取消、0x406 听背景音乐、0x407 听音效、0x408 战斗时窗口自动最大化、0x409 战斗时自动显示战场缩小图、0x40A 会话窗口不自动关闭、0x40B/0x40C/0x40D 讯息显示速度 快/普通/慢、0x40E/0x40F/0x410 武将移动速度 快/普通/慢、0x411 msctls_trackbar32 音量滑条、0x412 与静态「音量」、0x5D0 花色下拉框（候选串格式 0x486444="花色%d"）、0x5D1 加速下拉框（0x48644B="加速%d"）、0x4D3 19 段状态条。OK 处理 0x41B90F 写设置块：+0x00 = 0x406..0x40A 五复选框位掩码（bit0 背景音乐、bit1 音效、bit2 窗口最大化、bit3 战场缩小图、bit4 会话窗口不自动关闭）；+0x01 = 讯息显示速度索引（0/1/2）；+0x02 = 武将移动速度索引（0/1/2）。音量由 WM_HSCROLL(0x114) → 0x42E218 读 0x411 的 TBM_GETPOS 写 +0x03 并经 0x42F7FC 应用。过程 0x41BAD7：id=1 保存并确定、id=2 关闭、id=0x5D0 通知码 9 触发 owner-draw 动画、id=0x4D3 预览、WM_INITDIALOG→0x41BD7F。初始化回填（第139轮）：i=0..4 取 +0x00 第 i 位写控件 0x406+i；两组 s=0..1 取 byte[0x4B0770+1+s]（+0x01/+0x02）作为选中索引写 0x40B+s*3+i；0x4D3 收到 0x13 次消息 0x180；0x5D0/0x5D1 先发 0x14B。与 OK 写入链完全对称，三项界面设置映射闭合。


## 商店运行时表与物品可用性判定

ID: `mechanism.65.shop-runtime-and-item-usability.3ef7`；状态: `canonical`；证据: `static-verified`

Data.e5 块 2（0x8BB4，0x1200 字节，128×36）由 0x41B7F0 解码为 127 行×40 字节的运行时表，基址指针在 [0x4CEA04]，访问器 0x41B7E2。每行含 2 个仓库/买卖人物 ID、16 个装备槽和 16 个物品槽。0x466AE3 构造 16 槽列表，并对每个物品调用 0x407961 得到可用性/装备适性布尔值。


## 兵种成长表与装备适性字节

ID: `mechanism.65.job-growth-equipment-compatibility.3ef7`；状态: `canonical`；证据: `static-verified`

兵种成长表来自 Data.e5 块 3（0x9DB4，0xAF0 字节，80×35），运行时基址 0x4A2A27，行步长 0x23，访问器 0x41B782。前 9 字节是九项成长值，后 26 字节是装备类型适性；0x41C60F 读取 byte[9+物品类型] 作为可用性/装备适性判定。


## 装备槽与物品类型区间对应候选

ID: `mechanism.65.equipment-slot-type-candidate.3ef7`；状态: `candidate`；证据: `static-verified`

装备槽 3 个，物品类型阈值 20/26 分成三段；提出候选对应 slot0=type<20、slot1=20..25、slot2=>=26。尚未由命名表或界面文案直接证明。


## 音效播放与设置位 0x4B0770：SE_* 分段、sndPlaySoundA 标志、0x474777 模式

ID: `mechanism.65.sound-settings.3ef7`；状态: `candidate`；证据: `static-verified`

音效统一由 0x474777(voice, soundId, mode, force) 播放：先以 0x474596(2)=byte[0x4B0770]&2 判断音效总开关，soundId 分三段——<0x64 用 WAV\SE00.WAV（0x48E825），0x64..0xC7 用 WAV\SE_M_xx.WAV（0x48E830，id-=0x64），0xC8..0xD0 用 WAV\SE_E_xx.WAV（0x48E83C，id-=0xC8），>=0xD1 返回 0；两位十进制数按 idiv 10 写入路径 +9/+10，0x418ED4 转绝对路径。sndPlaySoundA 标志基值 3（SND_ASYNC|SND_NODEFAULT），循环 |8（SND_LOOP），不打断 |0x10（SND_NOSTOP）。mode=1 时同曲或 force 不重启；0xFFFF 强制一次性；0 循环；其他 N 为最多 N 次重试（间隔 0x42C522(6)）。停止函数 0x474652 调 sndPlaySoundA(0,0) 并清 voice。语音由 0x4090EE 走 SE_V_%03u.WAV（0x48E810）。设置块 0x4B0770：0x41EDEF 返回 byte[0]（bit1=音效开关），0x415E19 返回 min(word[+6]/2,0x7F)，两者分别写入存档区块B 的 +0x02/+0x03。


## 策略伤害的方向/天气/地形百分比修正

ID: `mechanism.65.strategy-damage-direction-weather.3ef7`；状态: `canonical`；证据: `static-verified`

策略伤害在兵种系第 6 行百分比之后追加方向/天气/地形百分比：方向码 0 时兵种系 0x1E +40、地形码 2/0x17 +25；方向码 1/3/0x26 时天气 ID>=2 +25；方向码 2 时另一侧兵种系==7 +25；最终 damage=damage*累计百分比/100。


## 小地图 tile 描述符表 0x506800（20 项×3 字节，含 12 字节视图）

ID: `mechanism.65.table-506800.3ef7`；状态: `candidate`；证据: `static-verified`

0x506800 是共享基址的两种记录视图。3 字节标记视图（每项 3 字节、容量 0x14=20）：绘制循环 0x41E898 以 i<byte[0x4B09DB]（出战部队数）且 i<0x14 为界，条目 byte0=源 y×0xC、byte1=源 x×0xC、byte2=源页×0x21C0，目标=页基+i×0x1B0，调 0x47E09B 绘 12×12；byte0==0xFF 终止；即每个出战单位一项小地图标记。12 字节记录视图（0x405063/0x405101/0x4263B3）：0x405063 取 [rec]/[rec+4] 两 dword 交 0x4376EA 并按 byte[0x4B422D] 地图高度遍历；0x405101 以 [rec+8] 为 word 数组指针（0x2828 或 0xFF 终止）线性查找单位 ID，按 0x4BE880+0x1B00×page 地图页缓冲写入；0x4263B3 以 0xC 步长 memmove 删除记录并调整后续 [rec+8]。两视图启用条件由页缓冲/步长区分：标记视图 0x21C0 源页 + 0x1B0 槽步长（战斗小地图刷新），记录视图 0x4BE880+0x1B00×page + 0xA8C000 临时分配（地图记录构建期）。写入 0x415EA1 以 index*3+0x506800 写 dword：b0=v1、b1=v2、b2=v4、b3=0xFF（高字节落在下一项首字节作终止哨兵）。


## 四方向目标/位置评分 0x4101D9 与物理百分比修正

ID: `mechanism.65.target-direction-score.3ef7`；状态: `candidate`；证据: `static-verified`

0x4101D9 解析单位后计算基准评分，再按最多 4 个方向枚举候选位置，用 0x41301E 评分、0x413009 合并较优值，返回 eax 分数与 edx 附带值。0x413272 以 (0,1,0x4E,0x76) 调用；0x426737 把守方评分加到、攻方评分减到等级差百分比上。


## 单位 +0x18 六槽临时属性块（0/3/6 三档）

ID: `mechanism.65.temp-attribute-block.3ef7`；状态: `candidate`；证据: `static-verified`

单位记录 +0x18..+0x1D 为 6 槽临时属性块：稳定档位 0/3/6 = -1/中性/+1，1/2/4/5 为过渡帧。0x414361 增减一档（三基底同哈希），0x45AA37 写入（0..5 直写，>=6 走 0x45AB49 跳转表），0x43C940 推进过渡，0x43D038 用 0x3F 掩码清理，0x436F49 以 3 初始化。0x4237D7 统计非中性槽，0x43EA12 统计负向槽并参与伤害/评分；AI 分支 14/15 以 >3 与 <3 加权。


## 存档头文本缓冲 0x4A1128（0x16）/0x4B0758 与脚本解析 0x417DF6

ID: `mechanism.65.text-buffers-save-header.3ef7`；状态: `candidate`；证据: `static-verified`

0x4A1128 是 0x16（22 字节）脚本文本缓冲：启动序列 0x404C80 中 0x47FD13(0x4A1128,0,0x16) 清零；0x417DF6 解析文本（'*' 控制码、'\n&' 结束、逐字符写入）。0x4B0758 是另一段 UI 文本缓冲（0x4125BB→0x47622D 绘制链）。保存区块B 的 +0x005 与 +0x01B 分别用 0x47FC7D(strcpy) 复制这两个缓冲，因此存档保留当时的消息文本。


## 练武场上下文 0x500AA0/0x500AE0：初始化 0x418F05 与模板 330 控件

ID: `mechanism.65.training-ground-context.3ef7`；状态: `candidate`；证据: `static-verified`

0x500AA0（6.6 为 0x500AE0）是练武场上下文（0x90 字节）。0x418F05（三基底同哈希 47ca7661c8fbfedd，6.6 同址同字节）写入 +0x00=eax（人物记录指针，已由 0x405BA2→0x41D0AE→0x4065D0=byte[record+0x2C] 等级→SetDlgItemInt(0x559) 确认）、+0x04=[ebp+8]、+0x08=[ebp+0xC]（0x40A56F 以 byte[+8]+5 作装载数量参数）、+0x09=edx（dword 覆盖 +0x09..+0x0C，+0x0A 强制 1）、+0x1C=dword[0x4CEA08]（地图记录指针）、+0x10=byte[0x505FDC]（模式）、+0x11=byte[0x500D8F]（场景计数，0x41E6A7 自增），随后 DialogBoxParamA(模板 0x14A=330, hwnd=0x4B6A68, DlgProc=0x4207B2)。字段语义（第148轮）：+0x04 为第二单位记录指针（0x41E6A4 传 0x4061E4(对方槽)，0x41ECAE 传常量 1），EXE 内无读取点；+0x08 为数量（战场路径 count=5，脚本处理器 0x4103F0 取第三操作数，类型表 0x40E388={0x02,0x02,0x4F}），唯一读取点 0x40A56F 以 byte[+8]+5 作 0x4789D6 装载数量（邻近 U_SELECT.E5/UNIT_ATK.E5/UNIT_SPC.E5/UNIT_MOV.E5 于 0x48BBA0）；+0x09..+0x0C 为瞬态参数（0x41E6A4 写 0，0x41ECAE 写费用参数），无读取点且随后被战场备份覆盖；+0x0A 为回合计数（0x43837E cmp 0x0A 上限并 inc，格式串 0x500C58「回合数 %d/%d」）。0x41E6A4 有两个调用者：0x4103F0 脚本操作码处理器（操作数校验 <0x400 且互不相等）与 0x425F19 战场初始化（count=5）。0x41ECAE 为训练入口：0x4237F9 费用校验（flag 低字节==0 → 2×0x40D8A9()；否则 等级 byte[rec+0x2C]×10；0x40D8A9 返回 1 或场景记录 byte[+0x17]，若 byte[+0x19]>=5 提示 0x500CB1「目前无需练武了」），0x423820 与资金 dword[0x4B077C] 比较（超出显示 0x500CA7「资金不足」），0x43BFD4 以 0x500C9C「支付%d金？」经 0x42F699 确认后扣款并置 byte[0x4AC63C]=3。0x42DE63(text=0x500C7E「普通模式/单挑模式/自动提升」, id=0x3FE, 3) 是通用选择框（布局表 0x42DDBB），0x423842(choice+1) 分派：2=单挑→0x43DBBE 取对手→0x41ECAE(rec,0)；1=普通→0x45E6B3→0x41ECAE(rec,edx)；3=自动提升→edx×1000→0x423820→0x43BFD4→显示 0x500E30「全队等级提升」。0x3FE 为单位表上界哨兵：0x43EE4C/0x43EF0E/0x46C329 三处遍历均以 <0x3FE 为上界（有效槽 0..0x3FD），0x41ECAE 以 0x4061E4(0x3FE) 取空记录；同一常量复用为选择框 ID。战斗退出 0x415C86 先把 ctx+0x5C..+0x6C（0x500AFC..）复制回 0x4B3C80 的两条单位记录，再 memset(ctx,0xD0,0)（0x47FD13），置 byte[0x500B57]=0xFF。进入练武场时 0x45165F（6.6 为 0x40ADA3）备份战场状态：+0x0C=dword[engine+0xC80] 后写 0x003CFFFF；+0x1A=word[engine+0x642] 后写 0xFFFF；+0x12=word[0x4B422C] 后写 0x0104；+0x1C 记录的 +0x1B/+0x1F 存 0x4B4250+4/+8 后清零。对话框过程 0x4207B2 在消息 2（WM_DESTROY）时调用 0x41D27A 恢复上述字段，并以 0x40762F(0x4A7B20,0x4A8660,0x500B84,0x500AFC) 恢复字符串配置。+0x14 为练武场窗口句柄缓存（0x40B3A6 读取，0 时回退 GetActiveWindow）。0x418F05 仅两个调用者：0x41E6D6（0x4061E4 两次取记录）与 0x41ECD6（0x4237F9 计价非 0 → 0x4061E4(0x3FE)）。模板 330 标题「练武场」，DLGTEMPLATE、48 控件、250x151 DLU、9pt 宋体：左右两个人物面板（姓名 1371/1368、Lv 1372/1369、HP 1373/1384、SP 1374/1385、Exp 1375/1386、攻击 1376/1387、防御 1377/1388、精神 1378/1389、爆发 1379/1390、士气 1380/1391），操作按钮 开始 1287/突击 1290/防御 1288/回避 1289/逃跑 1291，回合数标签 1437 与回合值 1075，左侧大面板 1219。0x4207B2 入口读取 [+0x10] 与 [+0x11]；0x41D0AE 是 SetDlgItemInt 包装（0x4065D0 取值），0x405BA2 以 nID=0x559 刷新右方 Lv。资源 330 三基底均 1480 字节、48 项但哈希各不相同。


## 回合数、回合上限、行动方与天气全局状态

ID: `mechanism.65.turn-action-weather-state.3ef7`；状态: `canonical`；证据: `static-verified`

战场状态基址 0x4B3D08：+0x2 为 0 基当前回合，+0x3 为回合上限，+0x4 为当前天气，+0x11 为天气类别。回合测试 current=byte[0x4B3D0A]+1 与目标比较（>=/</==）；回合上限写入 byte[0x4B3D0B] 并封顶 0xFF；行动方由 0x41C330(0x4B3D08) 返回；天气指令写入类别/当前天气，转换表 0x48E100 为 5×6，值为天气 ID 0..4。


## 单位五维分配记录 0x508000（0x66 槽×10 字节）与 0x505F40 全局池回退

ID: `mechanism.65.unit-alloc-records.3ef7`；状态: `candidate`；证据: `static-verified`

0x508000 是单位五维分配记录数组：槽 0..0x65（102 个），每槽 0x0A 字节 = 5 个 word（记录地址 0x508000+i*0x0A）。取指针函数 0x42ACD2(slot,mode)：slot>=0x66 返回 0xFF；mode!=1 且 byte[unit+0x2A]==0xFF 也返回 0xFF；否则返回记录指针。回退链 0x408FA0：当 byte[0x505F3C]!=0 时遍历 i<0x66，取单位后以 byte[unit+0x02] 的 5 位掩码判定，第 k 位为 0 则把记录 word[+2k] 清零，并把旧值累加进 dword[0x505F40]（全局点数池）。该记录与 332 工作区 0x4FFF68 的五维 word×5 同构：0x508000 为持久记录，0x4FFF68+0x00..0x09 为对话框临时经验、+0x0A..0x13 为升级阈值；0x4FFF68+0x14 为对话框剩余点数池，与 0x505F40 分属两池。


## 单位槽位数组 +0x84/+0x254/+0x430 与金钱/HP 联动

ID: `mechanism.65.unit-slot-arrays.3ef7`；状态: `candidate`；证据: `static-verified`

0x405998 从 dword[unit+0x84+index*4] 取 slot0、[unit+0x254+index*4] 取 slot1、[unit+0x430+index*4] 取 slot2。0x405AB6 把 slot0 累加到 0x48E8BD 并从 unit+0x10 扣除，slot1 走 0x472840/0x43F715；0x421278 对同一 +0x84 数组按 (slot0-1)*10 收费并置 1。


## 单位 +0x1E 四位状态组与 +0x10 部署字段

ID: `mechanism.65.unit-status-bitfield.3ef7`；状态: `candidate`；证据: `static-verified`

unit+0x10 由 0x41B500 直接返回，为 0 时 0x426B33 返回 2（未部署/已撤退候选）；否则 0x426B33 返回 byte[unit+0x1E] 第 3 组 2-bit 状态值（mask 8）。0x411072 在 0x426B33 非 0 时追加 40% 伤害。unit+0x1E 为 4 组 × 2 bit 状态字节。


## 武器经验基础值与无伤害路径（三基底）

ID: `mechanism.65.weapon-exp-cross-base.3ef7`；状态: `canonical`；证据: `static-verified`

武器经验段 0x4038DF..0x403930：基础值 6.4=3、6.5=2、6.6=3；无伤害路径 6.4=2、6.5=2、6.6=1。伤害高于攻击前值时减 1，ctx+0x604 非零时加 1。


## 特效参数显示名解析（范围码→名称）

ID: `mechanism.65.param-display-name-resolution.3890`；状态: `candidate`；证据: `static-verified`

1. `global.65.range-code-name-table.3890`：范围码 0..11 名称指针数组
2. `global.65.effect-name-tables.3890`：特效名分表（按类别/ID 段）
3. `global.65.ability-name-table.3890`：五/六能力名

## 6.5pl 核心特效引擎反汇编分析契约

ID: `mechanism.65pl.public-core-engine-analysis`；状态: `candidate`；证据: `source-reviewed`

把核心入口、调用者预检、核心处理和上层消费拆成独立证据链。固定地址只作为 6.5pl 参考样本线索，不能直接迁移到其它构建。


计算规则：

- `从桩或调用点向上找真实入口，记录调用点、模块偏移和完整函数边界。`
- `按 x86 栈帧还原四个参数，核对 push 顺序、ret N/add esp、ECX/EDX 使用和寄存器守恒。`
- `沿预检、查表、累加、test/cmp 和条件跳转追踪每一条路径，并继续追到返回值消费者。`
- `将静态结论拆成边界、调用关系、参数位置、分支方向和数值语义；只有运行时或文件读回才能升级对应证据。`

边界：

- 不能把 test eax,eax 的零/非零直接命名为命中、成功或效果生效。
- 不能只凭效果值、叠加标志或函数名推断返回值语义。
- 调用者、预检函数和结果消费者缺一时，条目保持 candidate。

## 6.5pl 特效调度器交叉引用与消费者追踪

ID: `mechanism.65pl.public-dispatcher-analysis`；状态: `candidate`；证据: `source-reviewed`

以特效桩交叉引用为入口定位调度器，先还原上下文和预检读取，再覆盖全部返回路径与上层消费。


计算规则：

- `收集所有调用者和被调目标，区分标准桩、包装桩和直接核心调用。`
- `记录 ECX、EDX、栈参数、预检读取位置、调度器返回和每个条件跳转。`
- `把调度器到核心入口、再到调用者消费的路径画成 CFG/调用图，保留未覆盖分支。`
- `将“非零跳过核心”“返回值被比较”“返回值进入伤害或效果写入”等事实分别登记。`

边界：

- 413009 被核心调用不等于四参数入口。
- 任何效果名称都必须由调用者和返回消费者共同证明。

## 6.5pl 特效桩参数与清栈契约复原

ID: `mechanism.65pl.public-stub-abi-reconstruction`；状态: `candidate`；证据: `source-reviewed`

从桩的压栈序列和函数收尾恢复效果值、叠加标记、装备特效 ID、个人特效 ID 的候选参数契约。


计算规则：

- `从高栈地址向 [ebp+08]/[ebp+0C] 方向还原参数，而不是按源码表面顺序猜测。`
- `区分 push imm8/imm32、push eax/ecx、add al/eax 基数和 thiscall 的 ECX 上下文。`
- `用 ret N、add esp,N、完整函数边界和返回消费者交叉核对参数个数与清栈责任。`
- `对三 push、多 push、动态 mov al 和参数循环只记录形态候选，不授予写回权限。`

边界：

- 压栈顺序不能单独证明参数语义。
- 短函数或跨函数准备必须回到 CFG 和原始字节逐项复核。

## 6.5pl 对象编号、记录步长与事务区边界

ID: `mechanism.65pl.public-object-identity-analysis`；状态: `candidate`；证据: `source-reviewed`

区分战场编号、人物 Data 号、DataRecord、战术单位和物理攻击事务区；记录步长与索引公式只能在当前画像内使用。


计算规则：

- `先确认编号的来源和宽度，再使用基址、步长和字段偏移。`
- `读取宽度不等于字段语义宽度；局部变量不等于持久结构字段。`
- `同名“单位”在战场槽、人物记录和调用帧中必须使用不同实体身份。`

边界：

- 未绑定精确样本时不把这些地址写入 canonical 函数或补丁。

## 反汇编与行为分析的分层证据模型

ID: `mechanism.65pl.reverse-engineering-evidence-layers`；状态: `candidate`；证据: `source-reviewed`


边界：

- 每条结论必须写目标样本、来源、证据层级和未覆盖边界。
- 条件断点命中计数不等于条件成立。
- 运行时临时写入必须立即读回并恢复。

补充说明：

- static：可证明 函数边界, 调用关系, 参数位置, 分支方向；不能单独证明 玩法效果已生效, 返回值的最终命名
- runtime-readback：可证明 具体分支命中, 指针和值在当前场景的变化；不能单独证明 永久补丁正确, 未覆盖路径安全
- file-readback：可证明 原字节/替换字节/长度/布局；不能单独证明 游戏内结果
- controlled-path：可证明 受控启动和路径观察；不能单独证明 所有场景覆盖
- in-game-acceptance：可证明 目标场景可见行为；不能单独证明 其它版本地址可复用

## 参考桩扫描器的 CFG 与操作数来源补证方法

ID: `mechanism.65pl.reference-scanner-hardening`；状态: `candidate`；证据: `source-reviewed`

将只读扫描器的形态候选转化为可复核结论时，必须加入 CFG、定义来源、实例身份和被调 ABI 证据。


计算规则：

- `PE32 头、节表、VA/RVA/文件偏移映射和边界先校验；不跨节读取。`
- `E8 目标扫描和 push 形态扫描只产生候选，输出命中原始字节和调用 VA。`
- `以基本块为单位追踪 EAX/ECX/EDX 最后定义和前驱路径，禁止跨分支拼接 mov al 或循环上限。`
- `把标准四 push、包装、动态参数、参数范围等形态分别统计，并逐项回到反汇编器复核。`
- `只有完整函数边界、调用约定、返回消费者和负例测试都成立时，才可升级为实现依据。`

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

## 剧本指令执行链（取 token → 查表 → 处理函数 → 取参）

ID: `mechanism.65.script-command-dispatch.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.script-token-reader.3890`：0x40FCB2 读 16 位 token
2. `fn.65.script-command-dispatch.3890`：0x4109E6 取低字节为 opcode
3. `global.65.script-command-dispatch-table.3890`：0x410A38[opcode-2]
4. `fn.65.script-param-get.3890`：0x4183F7 按序号取参数
5. `fn.65.script-ascii-number.3890`：0x426E64 解析数字/-/* 语法
6. `global.65.script-event-table.3890`：0x49CF68 运行时记录表（写入结果）

## 剧本（TR.E5）执行与事件表

ID: `mechanism.65.script-execution.3890`；状态: `candidate`；证据: `static-verified`

1. `global.65.script-event-table.3890`：0x49CF68 事件表 128×0x40
2. `fn.65.script-event-slot.3890`：0x426AA8 槽号→地址（+n*0x40）
3. `fn.65.script-event-iterate.3890`：0x42A049 遍历与分派
4. `format.65.script-command-record.3890`：指令记录读取
5. `fn.65.script-record-field-reader.3890`：0x42A100 字段读取样例

## 剧本跳转窗口（else / Section 的实现）

ID: `mechanism.65.script-jump-window.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.script-command-dispatch.3890`：0x4109E6 写 0x4CE74C（窗口起点）
2. `struct.65.script-context.3890`：ctx+0x0C 当前偏移
3. `global.65.script-control-codes.3890`：控制码 6/8 只作信号

## 剧本主循环（0x4180F9）与帧执行

ID: `mechanism.65.script-main-loop.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.script-interpret-frame.3890`：0x4100A1 单帧执行（计数驱动）
2. `global.65.script-vtable.3890`：虚表 +8 = 0x4109E6 分派器
3. `global.65.script-control-codes.3890`：控制码 3 退出单帧循环

## 剧本“短参数”假说的否定（0x42/0x43 的 byte[ecx+1] 归属更正）

ID: `mechanism.65.script-short-param.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.script-stream-readers.3890`：0x40FCB2 读 16 位 token
2. `fn.65.script-command-dispatch.3890`：取低字节为 opcode
3. `struct.65.script-context.3890`：ctx 本身没有 +1 短参数字段

## 策略解析调用链（施放→命中→伤害/状态/治疗→经验）

ID: `mechanism.65.strategy-resolution-chain.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.strategy-cast-entry.3890`：0x417982 施放入口/门控
2. `fn.65.strategy-mp-check.3890`：0x417AF6 MP 可用性
3. `fn.65.strategy-mp-cost.3890`：0x417B27 成本
4. `fn.65.strategy-hit-stub.3890`：0x43B6F3 命中模式
5. `fn.65.strategy-hit-curve.3890`：0x43B53A 命中曲线
6. `fn.65.strategy-damage.3890`：0x43C022 伤害
7. `fn.65.strategy-status-value.3890`：0x43C5DF 状态数值
8. `fn.65.strategy-heal.3890`：0x43C31D 治疗
9. `fn.65.strategy-exp.3890`：0x420EFB 经验
10. `fn.65.strategy-range-dispatch.3890`：0x435CE9 范围展开
11. `fn.65.strategy-animation-tier.3890`：0x401DFF 演出类型拓展

## 攻击/必杀范围等级拓展链（四向→九宫→没羽）

ID: `mechanism.65.attack-range-tier-expansion.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.fatal-range-selector.3890`：0x43F8C0 取必杀范围/特殊判定
2. `fn.65.attack-range-wrapper.3890`：0x417A35 包装并传 default=1
3. `fn.65.attack-range-tier-check.3890`：0x41CDEE 按 特效号=r+0x5A 判定
4. `fn.65.attack-range-tier-map.3890`：0x41CE8B 查 0x41CEAB 返回下一级
5. `fn.65.attack-dispatch`：0x436511 按范围码查 0x4D1400 展开
6. `fn.65.attack-append-target`：0x437AFF 边界/阵营/去重落格

## 穿透范围调用链（加载→包装→12 分支→落格）

ID: `mechanism.65.pierce-range-chain.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.pierce-loader`：0x40782D 按单位类型查 0x407881 表/必杀分支
2. `fn.65.pierce-expand-wrapper`：0x4364C7 取单位/角色后转 0x435CE9
3. `fn.65.strategy-range-dispatch.3890`：0x435CE9 12 分支展开
4. `fn.65.pierce-geometry-dispatch`：0x436616 四向/四角几何展开
5. `fn.65.pierce-append-target`：0x437AFF 落格与去重

## 策略模仿与强化策略穿透：标志位置、映射表与范围拓展对照

ID: `mechanism.65.strategy-mimic-and-penetration.3890`；状态: `candidate`；证据: `static-verified`

1. `fn.65.strategy-mimic-effect.3890`：0x4210BE 查询特效 0x2D(45) 策略模仿
2. `fn.65.strategy-mimic-selection.3890`：0x43E02A/0x465A2E 在特效 45 命中后进入 0x41DC78/0x465AC0
3. `fn.65.strategy-mimic-selection.3890`：选择器用 0x4D17B0 的 8 位类别掩码筛选，无独立模仿位
4. `fn.65.strategy-penetration-enhancement.3890`：0x44282D 取穿透码并查询特效 0xB6(182)，命中后查 0x442871
5. `fn.65.attack-range-tier-check.3890`：0x41CDEE 按特效 r+0x5A 判定并查 0x41CEAB，作为对照

## 策略属性子表：144 字节表映射与真实语义（6.5 3EF7）

ID: `mechanism.65.strategy-attribute-tables.3ef7`；状态: `canonical`；证据: `static-verified`

6.5 的 0xA2CE0..0xA31F0 是 10 张连续 144 字节表；每张按策略 ID 直接索引。其中 0xA2CE0 是填充区，0xA2D70 是效果类分派表，其余 8 张才是实例属性。


补充说明：

- 10 张表连续排列，步长 0x90；0xA2CE0 是唯一无消费者的填充表。
- 表映射：0xA2CE0 填充；0xA2D70 效果类；0xA2E00 战场AI；0xA2E90 练武场AI；0xA2F20 命中模式；0xA2FB0 AI类别位掩码；0xA3040 伤害百分比；0xA30D0 伤害门控；0xA3160 小动画；0xA31F0 大动画。
- 命中模式码：显示映射 0→90、1→100、2→100、3→34、4→50；战斗命中桩对 2 走无调整分支，3/4 走条件分支，>=5 直接百分比。
- AI 战场/练武场表的值 0x00..0x0F 是 16 项评分处理器编号，不是限制位。
- 0x4D17B0 的 bit6 在样本中仅回归、bit7 仅节能连击；四神策略实际为 0x00，UI 的“绝/四神”位名不成立。
- 0xA2D70 效果类表不在 Profile 中，由 StrategyEffectClassProbe 的签名探测确定；6.4/6.5 最大类 0x24，6.6 最大类 0x29。
- 运行时只有 68 条策略记录；本页所有 144 行值中，ID>=68 的行不会被三基底启动加载器读入。

## 策略是否伤血与命中模式：三基底全量解析

ID: `mechanism.65.strategy-damage-hit-resolution.3ef7`；状态: `canonical`；证据: `static-verified`

strategy-damage-type 是伤害门控，不是四种独立伤害类型：0..3 行为完全等价，4 表示不伤血，>=4 同样被门控，但显示函数只把精确的 4 显示为 0；ID 0x46/0x16 绕过门控。strategy-hit-rate 是命中模式/基础命中率选择器：0..4 为特殊模式，>=5 为百分比乘数；模式 2 使用能力曲线，模式 3/4 固定 34/50 后仍乘基础值并受状态/效果修正，最终上限 100。
