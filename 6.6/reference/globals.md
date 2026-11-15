# 6.6 全局地址

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/globals/effect-assignment-defaults-8ba1.json`、`6.6/data/globals/effect-name-table.json`、`6.6/data/globals/f36-shanzai-globals.json`、`6.6/data/globals/name-tables.json`、`6.6/data/globals/shanzai-20261027-globals.json`、`6.6/data/globals/shanzai-item-globals.json`、`6.6/data/globals/strategy-effect-tables-8ba1.json`、`6.6/data/globals/xiaoan-speed-globals.json`

| 全局量 | 地址 | 宽度 | 含义 | 状态/证据 |
|---|---|---|---|---|
| `global.66.effect-assignment-defaults.8ba1` 6.6 信奈基底：0x511000 内置特效分配默认表（256×16） | `0x00511000` (va) | 4096 | 0x500C3B 的初值就是 0x511000，指向 .text3 内嵌的 256 条 16 字节特效分配记录；不需要外部文件即可静态枚举。每条记录 = 4 个 (word 人物ID, byte 特效值) 槽（+0/+3/+6/+9）+ 2 个 (byte 兵种ID, byte 特效值) 槽（+0xC/+0xE）。人物槽按 0x40BE7D 的人物ID精确匹配，1024 是空人物哨兵，不是通配符；兵种槽按 0x406610 的兵种精确匹配，0xFF 是空兵种哨兵，不是通配符。0x42F998 在 0x505F68==0 时允许“同兵种组且记录兵种<=单位兵种”的近似匹配。0x50E000 的同尺寸装备分配表在文件内全 0，但可由 0x411C4A（0x47D8DF 跳表第 10 项）在运行时写入。 | `candidate` / `static-verified` |
| `global.66.effect-name-table.f20c` 特效名称表与范围码名称表 | `0x004CC600` (va) | 16 | 16 字节/条，索引=特效号，+0x0F 为分类码。穿透攻击 149..151 位于 0x4CCF50..0x4CCF70，远距攻击 155..157 位于 0x4CCFB0..0x4CCFD0（名称均只写「穿透攻击」/「远距攻击」，后缀由范围码决定）。范围码名称表在 0x40620A，12 个 DWORD 字符指针（0..11），内容与 6.5 的 0x40CEE9 表一致。 | `candidate` / `static-verified` |
| `global.66.f36.physical-context` F36 物理攻击上下文基址 | `0x004927F0` (va) | 0 | 当前样本中被多处直接引用的物理攻击上下文；旧教程字段名、数组容量和时序尚未逐项动态确认。 | `canonical` / `static-verified` |
| `global.66.f36.strategy-context` F36 策略上下文基址 | `0x00497AF8` (va) | 0 | 当前样本中被策略结算代码直接引用的上下文基址；偏移字段和策略效果生命周期保持待动态验证。 | `canonical` / `static-verified` |
| `global.66.f36.item-context` F36 物品使用上下文基址 | `0x00497750` (va) | 0 | 当前样本中被道具使用代码直接引用的上下文基址；字段语义不能从基址引用单独推出。 | `canonical` / `static-verified` |
| `global.66.f36.character-pointer-slot` F36 人物表指针槽 | `0x004CEA00` (pointerSlot) | 4 | 人物记录数组的运行时指针槽；当前记录步长为 0x48。 | `canonical` / `static-verified` |
| `global.66.range-code-name-table.f20c` 范围码名称表（12 槽） | `0x0040620A` (va) | 48 | 12 个指针槽（0..11），内容与 6.5 的 0x40CEE9 一致；末项 0x48E7F3（溅射）所在字符串区已被改写，按字符串扫描仅 11 项可解析。消费者两处：0x428385（参数类型 0x0B）与 0x460558（参数类型 0x0C）。 | `candidate` / `static-verified` |
| `global.66.misc-name-tables.f20c` 地形/兵种/兵种系/武器名表 | `0x0048BDB4` (va) | 132 | 地形 33 项基址 0x48BDB0（0 平原 … 7 雪原，6.6 起第 7 项改为「雪原」）；兵种 80 项基址 0x48BEA8（0 群雄/1 人杰/2 小刀手…）；兵种系 40 项基址 0x48C570；武器类别 15 项基址 0x48BC04。取用方式同为直接立即数寻址 [reg*4+imm32]，无中间指针表；兵种名唯一引用为叶子 getter 0x401120（三基底同址），无静态调用者。 | `candidate` / `static-verified` |
| `global.66.qi.pool` 6.6 集气池数组 | `0x004930C8` (va) | 1000 | - | `canonical` / `sample-verified` |
| `global.66.qi.gate-switch` 6.6 集气分流开关（4018 与前置门） | `0x00505EC8` (va) | 4 | - | `canonical` / `sample-verified` |
| `global.66.surround.target-list` 6.6 周边目标 slot 列表与引导目标数 | `0x00500EA5` (va) | 1 | - | `candidate` / `sample-verified` |
| `global.66.effect-value.type-table` 6.6 效果值类型码表 A（类别/档位） | `0x004CB6BA` (va) | 7 | - | `canonical` / `sample-verified` |
| `global.66.effect-value.value-table` 6.6 效果值类型码表 B（字节值表） | `0x004CB5CA` (va) | 48 | - | `candidate` / `sample-verified` |
| `global.66.item-effect-class-dispatch` 6.6 装备效果类号分发表 | `0x00430000` (va) | 32 | - | `canonical` / `sample-verified` |
| `global.66.strategy-effect-name-pools.8ba1` 6.6 信奈基底：兵种/装备特效名称池与关键 ID | `0x004CC600` (va) | 16 | 两条独立名称池，均为 16 字节/条、GBK/NUL 结尾。兵种池 VA 0x4CC600（文件 0x9E800，256 条），末字节 +0x0F 为分类码；装备池 VA 0x4CB7A0（文件 0x9D9A0，230 条，起始 ID 0x1A）。同名 ID 在不同池语义不同。 | `candidate` / `static-verified` |
| `global.66.strategy-per-id-tables.8ba1` 6.6 信奈基底：每策略 144 字节表（标志/效果类/AI/命中/学习/系数/门控/比率） | `0x004D14E0` (va) | 144 | 8 张按策略 ID 索引的表，文件偏移 0xA2CE0..0xA39D8；前 6 张步长 1×144，0x4D21B0 为 40 字节伤害类型比率表。运行时只加载前 0x90 条策略（0x484002 的记录数组 0x4A3E77×0x61）。 | `candidate` / `static-verified` |
| `global.66.effect-query-buffers.8ba1` 6.6 信奈基底：特效查询指针槽与运行态标志 | `0x00500C3B` (va) | 4 | 查询管线的运行态数据槽。0x500C3B 是特效分配表指针，初值 0x511000，直接指向 .text3 内嵌的 256 条默认表；0x50E000 是装备分配表，文件内全 0，运行时可被 0x411C4A（0x47D8DF 跳表第 10 项）写入；0x505F78=0x400 是 0x4101D9 的特殊键阈值；0x500AD7=1 时 0x43C01D 走快速路径；0x505F0C 参与自动使用门禁。 | `candidate` / `static-verified` |
| `global.66.xiaoan.native-super-state` 原生超级加速状态 | `0x00500ADB` (va) | 1 | 0/1 开关状态 | `canonical` / `sample-verified` |
| `global.66.xiaoan.native-super-busy` 原生超级加速忙标志 | `0x00500E0C` (va) | 1 | 防重入忙标志 | `canonical` / `sample-verified` |
| `global.66.xiaoan.phase` 当前阶段 | `0x004B3D18` (va) | 1 | 0..2 阶段索引 | `canonical` / `sample-verified` |
| `global.66.xiaoan.speed` 原生速度值 | `0x00500AD8` (va) | 2 | nativeStage 读取的 uint16 速度值；低字节为 0 时阶段逻辑会额外调用 deadline-check。 | `canonical` / `sample-verified` |
| `global.66.xiaoan.phase-table` 三阶段延迟表 | `0x004750DC` (va) | 3 | 三个连续 uint8，按 phase 索引。value>50 表示固定 delay=value-50；value<=50 表示 50 次计数周期内前 value-1 次休眠 1 ms、其余为 0 ms。 | `canonical` / `sample-verified` |
| `global.66.xiaoan.phase-counter` 阶段计数器 | `0x004750DF` (va) | 1 | 紧随 phaseTable 的 uint8 计数器；value<=50 时先加 1，达到 50 后减 50 回绕。 | `canonical` / `sample-verified` |
