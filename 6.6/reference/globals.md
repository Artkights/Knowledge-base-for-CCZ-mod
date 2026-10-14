# 6.6 全局地址

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/globals/xiaoan-speed-globals.json`

| 全局量 | 地址 | 宽度 | 含义 |
|---|---|---|---|
| `global.66.xiaoan.native-super-state` 原生超级加速状态 | `0x00500ADB` (va) | 1 | 0/1 开关状态 |
| `global.66.xiaoan.native-super-busy` 原生超级加速忙标志 | `0x00500E0C` (va) | 1 | 防重入忙标志 |
| `global.66.xiaoan.phase` 当前阶段 | `0x004B3D18` (va) | 1 | 0..2 阶段索引 |
| `global.66.xiaoan.speed` 原生速度值 | `0x00500AD8` (va) | 2 | nativeStage 读取的 uint16 速度值；低字节为 0 时阶段逻辑会额外调用 deadline-check。 |
| `global.66.xiaoan.phase-table` 三阶段延迟表 | `0x004750DC` (va) | 3 | 三个连续 uint8，按 phase 索引。value>50 表示固定 delay=value-50；value<=50 表示 50 次计数周期内前 value-1 次休眠 1 ms、其余为 0 ms。 |
| `global.66.xiaoan.phase-counter` 阶段计数器 | `0x004750DF` (va) | 1 | 紧随 phaseTable 的 uint8 计数器；value<=50 时先加 1，达到 50 后减 50 回绕。 |
