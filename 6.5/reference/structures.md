# 6.5 数据结构

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/structures/runtime-structures.json`

## 战术单位记录

ID: `struct.65.tactical-unit`；状态: `canonical`；证据: `static-verified`

步长: `0x30` (48)

索引公式: `0x004A7B20 + battlefield_id * 0x30 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `data_id` | `0x0` | 2 | `uint16` | 逻辑人物 ID |
| `data_id_container` | `0x0` | 4 | `uint32` | 包含 data_id 的四字节容器 |
| `battle_sprite_id` | `0x4` | 1 | `uint8` | 战场形象 ID |
| `packed_display_state` | `0x4` | 4 | `uint32` | 包含形象/阵营/坐标的显示状态 |
| `side` | `0x5` | 1 | `uint8` | 阵营/敌我 |
| `x` | `0x6` | 1 | `uint8` | 地图 X |
| `y` | `0x7` | 1 | `uint8` | 地图 Y |
| `action` | `0xD` | 1 | `uint8` | 行动状态 |
| `ai` | `0xE` | 1 | `uint8` | AI 状态 |
| `direction` | `0xF` | 1 | `uint8` | 朝向 |
| `hp` | `0x10` | 4 | `uint32` | 当前 HP |
| `mp` | `0x14` | 4 | `uint32` | 当前 MP |
| `attributes` | `0x18` | 6 | `bytes` | 战场临时属性块 |

## 运行时人物记录

ID: `struct.65.runtime-character`；状态: `canonical`；证据: `static-verified`

步长: `0x48` (72)

索引公式: `DWORD[0x004CEA00] + data_id * 0x48 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `unknown_06` | `0x6` | 2 | `bytes` | 未知 |
| `name` | `0x8` | 8 | `fixed-string` | 人物名 |
| `derived_attack` | `0x11` | 2 | `uint16` | 派生攻击 |
| `derived_defense` | `0x13` | 2 | `uint16` | 派生防御 |
| `derived_spirit` | `0x15` | 2 | `uint16` | 派生精神 |
| `derived_agility` | `0x17` | 2 | `uint16` | 派生爆发 |
| `derived_morale` | `0x19` | 2 | `uint16` | 派生士气 |
| `hp_max` | `0x1B` | 4 | `uint32` | 最大 HP |
| `mp_max` | `0x1F` | 2 | `uint16` | 最大 MP |
| `base_strength` | `0x21` | 1 | `uint8` | 基础武力 |
| `base_command` | `0x22` | 1 | `uint8` | 基础统率 |
| `base_intelligence` | `0x23` | 1 | `uint8` | 基础智力 |
| `base_agility` | `0x24` | 1 | `uint8` | 基础敏捷 |
| `base_luck` | `0x25` | 1 | `uint8` | 基础运气 |
| `appearance` | `0x27` | 1 | `uint8` | 形象 |
| `retreat` | `0x29` | 1 | `uint8` | 撤退状态 |
| `friendly_flag` | `0x2A` | 1 | `uint8` | 友军标志 |
| `job` | `0x2B` | 1 | `uint8` | 详细兵种 ID |
| `level` | `0x2C` | 1 | `uint8` | 等级 |
| `experience` | `0x2D` | 1 | `uint8` | 经验 |
| `weapon` | `0x2E` | 1 | `uint8` | 武器 ID |
| `weapon_level` | `0x2F` | 1 | `uint8` | 武器等级 |
| `weapon_experience` | `0x30` | 1 | `uint8` | 武器经验 |
| `armor` | `0x31` | 1 | `uint8` | 防具 ID |
| `armor_level` | `0x32` | 1 | `uint8` | 防具等级 |
| `armor_experience` | `0x33` | 1 | `uint8` | 防具经验 |
| `accessory` | `0x34` | 1 | `uint8` | 辅助装备 ID |
| `kills` | `0x35` | 2 | `uint16` | 击破数 |
| `unknown_44` | `0x44` | 2 | `bytes` | 未知 |
| `unknown_46` | `0x46` | 2 | `bytes` | 未知 |

## 物品记录

ID: `struct.65.item-record`；状态: `canonical`；证据: `static-verified`

步长: `0x19` (25)

索引公式: `0x004A1140 + item_id * 0x19 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `name` | `0x0` | 17 | `fixed-string` | 物品名存储区；文本容量 0x10 |
| `type` | `0x11` | 1 | `uint8` | 物品类型 |
| `effect_id` | `0x12` | 1 | `uint8` | 装备特效号 |
| `price_div_100` | `0x13` | 1 | `uint8` | 价格除以 100 |
| `icon` | `0x14` | 1 | `uint8` | 图标 |
| `initial_value` | `0x15` | 1 | `uint8` | 初始能力 |
| `effect_value` | `0x16` | 1 | `uint8` | 特效值 |
| `growth` | `0x17` | 1 | `uint8` | 成长 |
| `gallery` | `0x18` | 1 | `uint8` | 宝物图鉴标志 |

## 详细兵种记录

ID: `struct.65.detailed-job-record`；状态: `canonical`；证据: `static-verified`

步长: `0x23` (35)

索引公式: `0x004A2A27 + job_id * 0x23 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `movement` | `0x0` | 1 | `uint8` | 移动力 |
| `attack_range` | `0x1` | 1 | `uint8` | 攻击范围 ID |
| `attack_growth` | `0x2` | 1 | `uint8` | 攻击成长 |
| `defense_growth` | `0x3` | 1 | `uint8` | 防御成长 |
| `spirit_growth` | `0x4` | 1 | `uint8` | 精神成长 |
| `agility_growth` | `0x5` | 1 | `uint8` | 爆发成长 |
| `morale_growth` | `0x6` | 1 | `uint8` | 士气成长 |
| `hp_growth` | `0x7` | 1 | `uint8` | HP 成长 |
| `mp_growth` | `0x8` | 1 | `uint8` | MP 成长 |
| `equipment_eligibility` | `0x9` | 26 | `bytes` | 可装备类别矩阵 |

## 兵种系地形记录

ID: `struct.65.job-family-terrain-record`；状态: `canonical`；证据: `static-verified`

步长: `0x3C` (60)

索引公式: `0x004A3517 + family_id * 0x3C + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `terrain_adaptation` | `0x0` | 30 | `bytes` | 30 类地形适应 |
| `movement_cost` | `0x1E` | 30 | `bytes` | 30 类地形移动消耗 |

## 6.5 特效分配记录（3+1）

ID: `struct.65.effect-assignment`；状态: `canonical`；证据: `static-verified`

步长: `0x8` (8)

索引公式: `DWORD[0x00500C3B] + effect_id * 8 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `character_1` | `0x0` | 2 | `uint16` | 人物槽 1 |
| `character_2` | `0x2` | 2 | `uint16` | 人物槽 2 |
| `character_3` | `0x4` | 2 | `uint16` | 人物槽 3 |
| `job_1` | `0x6` | 1 | `uint8` | 兵种槽 |
| `shared_value` | `0x7` | 1 | `uint8` | 本行共享特效值 |

## 必杀分配记录

ID: `struct.65.fatal-assignment`；状态: `canonical`；证据: `static-verified`

步长: `0x10` (16)

索引公式: `0x00511800 + fatal_id * 16 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `character_1` | `0x0` | 2 | `uint16` | 人物 1 |
| `level_1` | `0x2` | 1 | `uint8` | 人物 1 等级 |
| `character_2` | `0x3` | 2 | `uint16` | 人物 2 |
| `level_2` | `0x5` | 1 | `uint8` | 人物 2 等级 |
| `character_3` | `0x6` | 2 | `uint16` | 人物 3 |
| `level_3` | `0x8` | 1 | `uint8` | 人物 3 等级 |
| `character_4` | `0x9` | 2 | `uint16` | 人物 4 |
| `level_4` | `0xB` | 1 | `uint8` | 人物 4 等级 |
| `character_5` | `0xC` | 2 | `uint16` | 人物 5 |
| `level_5` | `0xE` | 1 | `uint8` | 人物 5 等级 |
| `effect_value` | `0xF` | 1 | `uint8` | 必杀特效值 |

## 仓库记录

ID: `struct.65.warehouse-record`；状态: `canonical`；证据: `static-verified`

步长: `0x3` (3)

索引公式: `0x004B0783 + slot * 3 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `item_id` | `0x0` | 1 | `uint8` | 物品 ID |
| `level` | `0x1` | 1 | `uint8` | 等级 |
| `experience` | `0x2` | 1 | `uint8` | 经验 |

## 策略记录

ID: `struct.65.strategy-record`；状态: `canonical`；证据: `static-verified`

步长: `0x61` (97)

索引公式: `0x004A3E77 + strategy_id * 0x61 + field_offset`

字段尚未解析，见研究队列。

## 攻击范围坐标段

ID: `struct.65.range-segment`；状态: `canonical`；证据: `static-verified`

步长: `0x4` (4)

索引公式: `DWORD[0x004D1400 + range_id * 4] 指向 int8 dx,int8 dy 对；0xFFFF 终止`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `delta_x` | `0x0` | 1 | `int8` | 相对 X |
| `delta_y` | `0x1` | 1 | `int8` | 相对 Y |
