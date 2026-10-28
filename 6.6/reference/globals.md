# 6.6 全局地址

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/globals/f36-shanzai-globals.json`、`6.6/data/globals/shanzai-20261027-globals.json`、`6.6/data/globals/shanzai-item-globals.json`、`6.6/data/globals/xiaoan-speed-globals.json`

| 全局量 | 地址 | 宽度 | 含义 | 状态/证据 |
|---|---|---|---|---|
| `global.66.f36.physical-context` F36 物理攻击上下文基址 | `0x004927F0` (va) | 0 | 当前样本中被多处直接引用的物理攻击上下文；旧教程字段名、数组容量和时序尚未逐项动态确认。 | `canonical` / `static-verified` |
| `global.66.f36.strategy-context` F36 策略上下文基址 | `0x00497AF8` (va) | 0 | 当前样本中被策略结算代码直接引用的上下文基址；偏移字段和策略效果生命周期保持待动态验证。 | `canonical` / `static-verified` |
| `global.66.f36.item-context` F36 物品使用上下文基址 | `0x00497750` (va) | 0 | 当前样本中被道具使用代码直接引用的上下文基址；字段语义不能从基址引用单独推出。 | `canonical` / `static-verified` |
| `global.66.f36.character-pointer-slot` F36 人物表指针槽 | `0x004CEA00` (pointerSlot) | 4 | 人物记录数组的运行时指针槽；当前记录步长为 0x48。 | `canonical` / `static-verified` |
| `global.66.qi.pool` 6.6 集气池数组 | `0x004930C8` (va) | 1000 | - | `canonical` / `sample-verified` |
| `global.66.qi.gate-switch` 6.6 集气分流开关（4018 与前置门） | `0x00505EC8` (va) | 4 | - | `canonical` / `sample-verified` |
| `global.66.surround.target-list` 6.6 周边目标 slot 列表与引导目标数 | `0x00500EA5` (va) | 1 | - | `candidate` / `sample-verified` |
| `global.66.effect-value.type-table` 6.6 效果值类型码表 A（类别/档位） | `0x004CB6BA` (va) | 7 | - | `canonical` / `sample-verified` |
| `global.66.effect-value.value-table` 6.6 效果值类型码表 B（字节值表） | `0x004CB5CA` (va) | 48 | - | `candidate` / `sample-verified` |
| `global.66.item-effect-class-dispatch` 6.6 装备效果类号分发表 | `0x00430000` (va) | 32 | - | `canonical` / `sample-verified` |
| `global.66.xiaoan.native-super-state` 原生超级加速状态 | `0x00500ADB` (va) | 1 | 0/1 开关状态 | `canonical` / `sample-verified` |
| `global.66.xiaoan.native-super-busy` 原生超级加速忙标志 | `0x00500E0C` (va) | 1 | 防重入忙标志 | `canonical` / `sample-verified` |
| `global.66.xiaoan.phase` 当前阶段 | `0x004B3D18` (va) | 1 | 0..2 阶段索引 | `canonical` / `sample-verified` |
| `global.66.xiaoan.speed` 原生速度值 | `0x00500AD8` (va) | 2 | nativeStage 读取的 uint16 速度值；低字节为 0 时阶段逻辑会额外调用 deadline-check。 | `canonical` / `sample-verified` |
| `global.66.xiaoan.phase-table` 三阶段延迟表 | `0x004750DC` (va) | 3 | 三个连续 uint8，按 phase 索引。value>50 表示固定 delay=value-50；value<=50 表示 50 次计数周期内前 value-1 次休眠 1 ms、其余为 0 ms。 | `canonical` / `sample-verified` |
| `global.66.xiaoan.phase-counter` 阶段计数器 | `0x004750DF` (va) | 1 | 紧随 phaseTable 的 uint8 计数器；value<=50 时先加 1，达到 50 后减 50 回绕。 | `canonical` / `sample-verified` |
