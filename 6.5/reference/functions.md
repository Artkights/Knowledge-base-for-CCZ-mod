# 6.5 函数与入口

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/functions/runtime-functions.json`

| 函数 | 地址 | 调用约定/输入 | 返回 | 含义 |
|---|---|---|---|---|
| `fn.65.data-id-to-runtime-character` 数据 ID 转人物记录指针 | `0x004061E4` (va) | unknown; DataId | RuntimeCharacter* | 将逻辑人物 ID 映射到 0x48 字节运行时人物记录。 |
| `fn.65.battlefield-id-to-tactical-unit` 战场 ID 转战术单位指针 | `0x004061F9` (va) | unknown; BattlefieldUnitId | TacticalUnit* | 将战场槽 ID 映射到 0x30 字节战术单位记录。 |
| `fn.65.tactical-unit-to-runtime-character` 战术单位转人物记录指针 | `0x0040658F` (va) | unknown; TacticalUnit* | RuntimeCharacter* | 读取战术单位 data_id 并映射到人物记录。 |
| `fn.65.detailed-job-id-to-record` 详细兵种 ID 转记录 | `0x0041B782` (va) | unknown; DetailedJobId | DetailedJobRecord* | 返回 0x23 字节详细兵种记录。 |
| `fn.65.job-family-id-to-terrain-record` 兵种系 ID 转地形记录 | `0x0041B7D4` (va) | unknown; JobFamilyId | JobFamilyTerrainRecord* | 返回 0x3C 字节兵种系地形记录。 |
| `fn.65.consumable-item-id-to-count` 消耗品 ID 转数量字节 | `0x00414F65` (va) | unknown; ItemId | uint8* | 按 item_id-150 映射到消耗品数量数组。 |
| `fn.65.item-id-to-record` 物品 ID 转物品记录 | `0x004837C2` (va) | unknown; ItemId | ItemRecord* | 返回 0x19 字节物品记录；地址查询 0x004837C2 应命中本条。 |
| `fn.65.strategy-id-to-record` 策略 ID 转策略记录 | `0x00484002` (va) | unknown; StrategyId | StrategyRecord* | 返回 0x61 字节策略记录。 |
| `fn.65.recalculate-character` 人物能力重算 | `0x004075DF` (va) | thiscall-or-register-context; ECX=person_record_ptr; stack: person_record_ptr:u32; callee cleanup 4 bytes | void | 按人物基础属性、兵种和装备重算派生能力。 |
| `fn.65.revive-tactical-unit` 战场复活 | `0x004092C7` (va) | unknown; battlefield placement args | void | 6.5/6.4 战场单位复活入口。 |
| `fn.65.weather-refresh` 天气刷新 | `0x0041D9D1` (va) | unknown; weather context | void | 刷新天气相关战场状态；Python 扳手仅保留历史调用入口。 |
| `fn.65.direction-refresh` 战场转向刷新 | `0x00457428` (va) | thiscall-or-register-context; ECX=DWORD[0x004B5DF0]; stack: direction:u32, data_id:u32, flags:u32 | void | 参数依次为 direction、data_id、flags。 |
| `fn.65.position-refresh` 战场坐标刷新 | `0x004594DD` (va) | thiscall-or-register-context; ECX=DWORD[0x004B5DF0]; stack: direction:u32, y:u32, x:u32, data_id:u32 | void | 参数依次为 direction、y、x、data_id。 |
| `fn.65.attack-entry` 物理攻击入口 | `0x0043DADA` (va) | unknown; combat context | void | 进入物理攻击流程并准备范围描述符。 |
| `fn.65.attack-selector` 攻击范围选择器 | `0x0045533D` (va) | unknown; attacker/range | void | 准备中心坐标和 packed range descriptor，在 0x004553F8 调用范围分派。 |
| `fn.65.attack-dispatch` 攻击范围分派 | `0x00436511` (va) | thiscall-or-register-context; ECX=runtime_unit_ptr; stack: [EBP+08]=center_coordinate, [EBP+0C..0F]=packed_range_descriptor; callee cleanup 16 bytes | void | 读取范围指针表并分派几何展开。 |
| `fn.65.attack-geometry` 攻击几何展开 | `0x00436616` (va) | unknown; center/range segment | void | 把以 FFFF 终止的两字节相对坐标段展开为地图坐标。 |
| `fn.65.attack-append-target` 攻击目标追加 | `0x00437AFF` (va) | unknown; coordinate/filter | void | 落地坐标、过滤单位并追加到范围目标缓冲。 |
| `fn.65.map-unit-lookup` 地图坐标查战场单位 | `0x00435884` (va) | unknown; x,y | BattlefieldUnitId | 把地图格坐标映射到战场单位。 |
| `fn.65.pierce-loader` 穿透值装载 | `0x0040782D` (va) | unknown; unit/effect | uint8 | 从 0x00407881 穿透值表装载穿透类型。 |
| `fn.65.combat-context-init` 战斗上下文初始化 | `0x00406282` (va) | unknown; attacker/target | void | 初始化物理上下文并写入穿透范围字段。 |
| `fn.65.pierce-expand-wrapper` 穿透范围扩展包装器 | `0x004364C7` (va) | thiscall-or-register-context; ECX=tactical_unit_ptr; stack: target_battle_id, pierce_byte, output_buffer, filter_or_fallback_args | void | 转入 0x00435CE9 按穿透码展开目标。 |
| `fn.65.pierce-geometry-dispatch` 穿透几何分派 | `0x00435CE9` (va) | unknown; center/code/output/filter | void | 按 0..0x0B 穿透/效果码分派几何。 |
| `fn.65.pierce-append-target` 穿透目标追加 | `0x00435BF2` (va) | unknown; coordinate/output/filter | void | 追加穿透/效果范围目标。 |
| `fn.65.target-consumer` 攻击目标消费与伤害写入 | `0x004361B1` (va) | unknown; target array/context | void | 消费目标数组并进入伤害/效果写入。 |
| `fn.65.core-effect-engine` 核心特效引擎 | `0x004101D9` (va) | unknown; effect context | result | 核心特效分派入口；具体分支仍应按调用点复核。 |
