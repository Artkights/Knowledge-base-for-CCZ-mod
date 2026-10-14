# 6.5 全局地址

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/globals/runtime-globals.json`

| 全局量 | 地址 | 宽度 | 含义 |
|---|---|---|---|
| `global.65.tactical-unit-array` 战术单位数组 | `0x004A7B20` (va) | 0 | 0x30 字节记录数组 |
| `global.65.runtime-character-pointer` 运行时人物表指针槽 | `0x004CEA00` (pointerSlot) | 4 | 解引用后得到 1024×0x48 人物表 |
| `global.65.strategy-table` 策略运行时表 | `0x004A3E77` (va) | 0 | 0x61 字节记录 |
| `global.65.item-table` 物品运行时表 | `0x004A1140` (va) | 0 | 255×0x19 字节 |
| `global.65.detailed-job-table` 详细兵种表 | `0x004A2A27` (va) | 0 | 80×0x23 字节 |
| `global.65.job-family-terrain-table` 兵种系地形表 | `0x004A3517` (va) | 0 | 40×0x3C 字节 |
| `global.65.consumable-counts` 消耗品数量数组 | `0x00510C80` (va) | 105 | item_id 150..254，各 1 字节 |
| `global.65.warehouse` 仓库记录表 | `0x004B0783` (va) | 600 | 200×3 字节 |
| `global.65.money` 金钱 | `0x004B077C` (va) | 4 | 全局金钱值 |
| `global.65.alignment` 路线/阵营标志 | `0x004B0782` (va) | 1 | 全局路线标志 |
| `global.65.merit` 人物功勋表 | `0x00508000` (va) | 0 | 扩展版功勋数据 |
| `global.65.merit-pool` 功勋池 | `0x00505F40` (va) | 0 | 功勋相关全局池 |
| `global.65.save-state` 存档状态 | `0x004B0770` (va) | 0 | 存档/流程全局状态 |
| `global.65.battle-state` 战场状态 | `0x004B3D08` (va) | 0 | 战场流程状态 |
| `global.65.battle-sp` 战场 SP | `0x00501C00` (va) | 0 | 战场 SP 数据 |
| `global.65.job-names` 兵种名称表 | `0x005000D0` (va) | 0 | 兵种名称数据 |
| `global.65.effect-pointer` 特效分配表指针槽 | `0x00500C3B` (pointerSlot) | 4 | 解引用得到 255×8 字节 3+1 特效表 |
| `global.65.exclusive-effect` 专属/套装表 | `0x0050E400` (va) | 0 | 每特效 16 字节 |
| `global.65.fatal-table` 必杀分配表 | `0x00511800` (va) | 0 | 80×16 字节 |
| `global.65.bool-variables` 布尔变量位集 | `0x00492FC8` (va) | 512 | 4096 位，MSB0 |
| `global.65.int-variables` 整数变量数组 | `0x00502000` (va) | 16384 | 4096×signed int32 |
| `global.65.pointer-variables` 指针变量数组 | `0x00506000` (va) | 1924 | 481×uint32 |
| `global.65.physical-context` 物理攻击上下文 | `0x004927F0` (va) | 0 | 目标、伤害、效果和穿透字段容器 |
| `global.65.strategy-context` 策略上下文 | `0x00497AF8` (va) | 0 | 策略结算上下文 |
| `global.65.item-context` 物品上下文 | `0x00497750` (va) | 0 | 物品使用上下文 |
| `global.65.range-pointer-table` 范围指针表 | `0x004D1400` (va) | 1024 | 256 个 uint32 范围段指针 |
| `global.65.pierce-value-table` 穿透值表 | `0x00407881` (va) | 0 | 穿透类型值表 |
| `global.65.range-target-buffer` 范围目标临时缓冲 | `0x004AC748` (va) | 0 | 几何展开后的候选目标 |
| `global.65.range-target-write-index` 目标写入索引 | `0x004B2C34` (va) | 4 | 范围目标缓冲写位置 |
| `global.65.range-target-sentinel` 目标哨兵 | `0x004B2C28` (va) | 4 | 范围目标终止/状态值 |
| `global.65.battle-ui-context` 战场 UI this 指针槽 | `0x004B5DF0` (pointerSlot) | 4 | 转向和坐标刷新函数的 ECX 来源 |
