# 6.5 机制与调用链

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/mechanisms/consumable-effects.json`、`6.5/data/mechanisms/engine-mechanisms.json`

## 消耗品独立特效目录 0x1A–0x3D 与证据分层

ID: `mechanism.shared.consumable-effect-namespace`；状态: `candidate`；证据: `editor-source-reviewed-user-labels-and-sample-supported-inference`

- usage：用于当前数据管理器的消耗品下拉标签、检索、数字保留和候选语义提示。
- profileBoundary：6.5 与 6.6 共享此候选标签目录，不共享物品表固定地址、名称布局或类别/实际特效号的物理绑定；必须先按目标 Profile 和 Codec 确认类别及实际效果字段。
- runtimeVerification：本实体未收录逐编号 EXE 分发表、调用约定、参数消费或游戏内运行结果。编辑器目录中的 Confirmed 只表示目录命中，不能解释为 runtime-verified。

- kind：consumable-effect-byte
- minimum：0x1A
- maximum：0x3D
- count：36
- storageWidth：1
- meaning：消耗品实际特效号的目录命名空间，与装备特效名称目录分开；同一数值不得自动套用装备特效名称。

| 特效号 | 十进制 | 名称 | 含义 | 证据 | 6.5 字节样本 |
|---|---:|---|---|---|---|
| `0x1A` | 26 | 恢复生命 | 目录描述为按效果值恢复 HP；具体参数消费仍需目标基底验证。 | `editor-source-reviewed-sample-and-fixed-name-table-reported` | 150：恢复用豆; 151：恢复用麦; 152：恢复用米; 170：粟; 171：麦; 172：精粮; 173：空闲 |
| `0x1B` | 27 | 恢复 MP | 目录描述为按效果值恢复 MP；具体参数消费仍需目标基底验证。 | `editor-source-reviewed-sample-and-fixed-name-table-reported` | 153：神秘水; 154：神秘酒 |
| `0x1C` | 28 | 治疗混乱 | 解除混乱状态的目录标签。 | `editor-source-reviewed-sample-reported` | 156：兴奋剂 |
| `0x1D` | 29 | 治疗中毒 | 解除中毒状态的目录标签。 | `editor-source-reviewed-sample-reported` | 155：解毒药 |
| `0x1E` | 30 | 治疗麻痹 | 解除麻痹状态的目录标签。 | `editor-source-reviewed-sample-reported` | 157：膏药 |
| `0x1F` | 31 | 治疗禁咒 | 解除禁咒或封锁状态的目录标签。 | `editor-source-reviewed-sample-reported` | 158：止咳药 |
| `0x20` | 32 | 恢复异常状态 | 解除异常状态的目录标签；具体状态集合未在本实体验证。 | `editor-source-reviewed-sample-reported` | 159：万能药 |
| `0x21` | 33 | 武力上升 | 提升武力的目录标签。 | `editor-source-reviewed-sample-reported` | 161：武力果 |
| `0x22` | 34 | 统率上升 | 提升统率的目录标签。 | `editor-source-reviewed-sample-reported` | 162：统帅果 |
| `0x23` | 35 | 智力上升 | 提升智力的目录标签。 | `editor-source-reviewed-sample-reported` | 163：智力果 |
| `0x24` | 36 | 敏捷上升 | 提升敏捷的目录标签。 | `editor-source-reviewed-sample-reported` | 164：敏捷果 |
| `0x25` | 37 | 运气上升 | 提升运气的目录标签。 | `editor-source-reviewed-sample-reported` | 165：好运果 |
| `0x26` | 38 | 增加经验 | 按效果值增加经验的目录描述；单位和边界需另核对。 | `editor-source-reviewed-sample-reported` | 166：经验果 |
| `0x27` | 39 | 兵种进阶 | 印绶或兵种进阶的目录标签。 | `editor-source-reviewed-sample-and-fixed-name-table-reported` | 160：印绶 |
| `0x28` | 40 | 恢复SP | 恢复 SP 的用户标签；具体参数消费未核对。 | `user-label-confirmed-conflict-preserved` | — |
| `0x29` | 41 | 获得功勋 | 按效果值增加功勋的目录描述；具体参数消费未核对。 | `editor-source-reviewed-sample-reported` | 169：功勋书 |
| `0x2A` | 42 | HP上升 | 提升 HP 的用户标签；目录描述为永久提升，运行时持久性尚需核对。 | `user-label-confirmed-editor-sample-reported` | 167：仙桃 |
| `0x2B` | 43 | MP上升 | MP上升的候选映射；目录描述为永久提升，运行时持久性尚需核对。 | `sample-supported-inference` | 168：仙酒 |
| `0x2C` | 44 | 2C道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x2D` | 45 | 2D道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x2E` | 46 | 2E道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x2F` | 47 | 2F道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x30` | 48 | 30道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x31` | 49 | 单挑 | 单挑类道具的用户标签；目标选择和参数语义未核对。 | `user-label-confirmed` | — |
| `0x32` | 50 | 学会策略 | 学习策略的用户标签；策略ID所在字段和边界未在本实体确认。 | `user-label-confirmed` | — |
| `0x33` | 51 | 使用策略 | 使用策略的用户标签；策略ID、目标及消耗规则未在本实体确认。 | `user-label-confirmed` | — |
| `0x34` | 52 | 附加技能 | 附加技能的用户标签；技能ID和持续规则未在本实体确认。 | `user-label-confirmed` | — |
| `0x35` | 53 | 35道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x36` | 54 | 36道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x37` | 55 | 37道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x38` | 56 | 38道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x39` | 57 | 39道具号 | 按十六进制编号显示；不推导该编号对应的实际游戏操作。 | `user-display-label-confirmed` | — |
| `0x3A` | 58 | 任务物品 | 任务物品的用户标签；任务检查条件未在本实体确认。 | `user-label-confirmed` | — |
| `0x3B` | 59 | 合成材料 | 合成材料的用户标签；合成消费链未在本实体确认。 | `user-label-confirmed` | — |
| `0x3C` | 60 | 工具物品 | 工具物品的用户标签；具体工具行为未在本实体确认。 | `user-label-confirmed` | — |
| `0x3D` | 61 | 装备升级 | 装备升级的目录标签；升级等级、装备能力及参数模式需目标基底验证。 | `editor-source-reviewed-sample-and-fixed-name-table-reported` | 174：装备升级书 |

- 0x1A–0x27、0x29、0x3D 的来源是现有目录源码及其指向的6.5样本/6.6固定名称表线索。本轮未把这些线索提升为逐效果的运行时验证。
- 0x28、0x2A、0x31–0x34、0x3A–0x3C 为本轮用户提供的标签；0x2C–0x30、0x35–0x39 为用户指定的数字显示标签。
- 0x2B=MP上升为有仙酒样本线索支持的冲突消解推定。原请求重复写了0x28，不应在知识库中伪称用户明确给出0x2B。
- 6.5与6.6共用候选标签目录，不等于各基底共享实际特效字节位置或参数行为。实际特效号必须由类别感知Codec读取，效果参数必须依据独立物理/消费者证据解释。

- 目录范围外或尚未确认的编号保留原始数值，并显示“未确认道具特效 0xXX”；不得用装备特效名称补全，也不得自动改写未知编号或参数。数字道具号标签只是保留编号的显示策略。

写入策略：允许作为编辑器目录显示、人工检索和候选语义提示；禁止仅凭目录标签或源码Confirmed标记自动写入游戏特效号、参数或补丁。人工物理编辑仍需目标Profile/Codec、字段范围、原始字节保留、差异白名单和保存后复读门禁；新增游戏语义应先补目标消费者或运行时证据。

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
