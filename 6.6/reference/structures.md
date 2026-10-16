# 6.6 数据结构

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/structures/f36-shanzai-structures.json`、`6.6/data/structures/runtime-structures.json`

## F36 人物运行时记录

ID: `struct.66.f36.character-record`；状态: `canonical`；证据: `static-verified`

步长: `0x48` (72)

索引公式: `DWORD[0x004CEA00] + data_id * 0x48 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `record_key_low12` | `0x0` | 2 | `uint16` | 当前转换函数使用的记录键低 12 位 |
| `job_id` | `0x2B` | 1 | `uint8` | 当前样本转换链读取的兵种字段 |

## F36 战场单位记录

ID: `struct.66.f36.battle-unit-record`；状态: `canonical`；证据: `static-verified`

步长: `0x30` (48)

索引公式: `0x004A7B20 + battlefield_id * 0x30 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `data_id_or_unit_key` | `0x0` | 4 | `uint32` | 当前 0043E4D6 转换循环解引用并比较的首字段；具体编码仍需运行时确认 |

## F36 物品记录

ID: `struct.66.f36.item-record`；状态: `canonical`；证据: `static-verified`

步长: `0x19` (25)

索引公式: `0x0049F820 + item_id * 0x19 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `name` | `0x0` | 15 | `fixed-string` | 名称；编码和终止规则需按资源样本复读 |
| `icon` | `0xF` | 1 | `uint8` | 图标编号 |
| `effect_value` | `0x16` | 1 | `uint8` | 特效值候选字段 |

## F36 策略记录

ID: `struct.66.f36.strategy-record`；状态: `canonical`；证据: `static-verified`

步长: `0x61` (97)

索引公式: `0x004A3E77 + strategy_id * 0x61 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `opaque_strategy_payload` | `0x0` | 97 | `opaque-bytes` | 记录步长已由静态乘法确认；字段语义仍需逐项复核 |

## 6.6 特效分配记录（4+2）

ID: `struct.66.effect-assignment`；状态: `canonical`；证据: `source-reviewed`

步长: `0x10` (16)

索引公式: `DWORD[resolved effect pointer slot] + effect_id * 0x10 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `character_1` | `0x0` | 2 | `uint16` | 人物 1 |
| `character_value_1` | `0x2` | 1 | `uint8` | 人物 1 特效值 |
| `character_2` | `0x3` | 2 | `uint16` | 人物 2 |
| `character_value_2` | `0x5` | 1 | `uint8` | 人物 2 特效值 |
| `character_3` | `0x6` | 2 | `uint16` | 人物 3 |
| `character_value_3` | `0x8` | 1 | `uint8` | 人物 3 特效值 |
| `character_4` | `0x9` | 2 | `uint16` | 人物 4 |
| `character_value_4` | `0xB` | 1 | `uint8` | 人物 4 特效值 |
| `job_1` | `0xC` | 1 | `uint8` | 兵种 1 |
| `job_value_1` | `0xD` | 1 | `uint8` | 兵种 1 特效值 |
| `job_2` | `0xE` | 1 | `uint8` | 兵种 2 |
| `job_value_2` | `0xF` | 1 | `uint8` | 兵种 2 特效值 |

## 6.6 物品记录

ID: `struct.66.item-record`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `split Data.e5/Star.e5 table + item_id*0x19`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `name` | `0x0` | 15 | `fixed-string` | 名称 |
| `icon` | `0xF` | 1 | `uint8` | 图标 |
| `effect_or_type` | `0x11` | 1 | `uint8` | 特效或类型 |
| `equipment_effect_or_category` | `0x12` | 1 | `uint8` | 装备特效或类别 |
| `price` | `0x13` | 1 | `uint8` | 价格字段 |
| `ability` | `0x15` | 1 | `uint8` | 能力 |
| `effect_value` | `0x16` | 1 | `uint8` | 特效值 |
| `growth` | `0x17` | 1 | `uint8` | 成长 |
| `catalog_flag` | `0x18` | 1 | `uint8` | 图鉴/宝物标志 |
