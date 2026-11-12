# 6.4 全局地址

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.4/data/globals/effect-name-table.json`、`6.4/data/globals/name-tables.json`

| 全局量 | 地址 | 宽度 | 含义 | 状态/证据 |
|---|---|---|---|---|
| `global.64.effect-name-table.9112` 远距/穿透攻击特效名与范围码名称表 | `0x0040620A` (va) | 40 | 6.4 没有 6.5/6.6 的 16 字节特效名表（0x4CC600 同址全 0）。特效名以独立字符串出现：0x4FFB10「远距攻击-物理」、0x4FFB20「远距攻击-策略」、0x4FFDA0「穿透攻击 两格」、0x4FFDB0「穿透攻击 十字」。范围码名称表在 0x40620A，10 个 DWORD 字符指针（范围码 0..9）：无/十字/九宫/没羽箭/两格/六格/大没羽箭/三格/方格/横扫。 | `candidate` / `static-verified` |
| `global.64.range-code-name-table.9112` 范围码名称表（10 项） | `0x0040620A` (va) | 40 | 10 项指针数组，索引=范围码 0..9：无/十字/九宫/没羽箭/两格/六格/大没羽箭/三格/方格/横扫。6.5 扩为 12 项（新增 环击/溅射），6.6 同址 12 槽（末项字符串区被改写，仅 11 项可解析）。消费者 0x462275。 | `candidate` / `static-verified` |
| `global.64.effect-name-tables-split.9112` 特效名分表（三段） | `0x0048BC50` (va) | 340 | 6.4 特效名为三段连续指针数组：0x48BC50(13)/0x48BC88(41)/0x48BD34(31)，合计 85 项；6.5 合并为 0x48BC50 60 项（<0x3C）+ 0x5003F8 39 项，6.6 改用 0x4CC600 的 16 字节记录表。 | `candidate` / `static-verified` |
| `global.64.misc-name-tables.9112` 布尔/职业/能力名表 | `0x0040CC97` (va) | 20 | 0x40CC97 5 项（否/是/全能/文官/武将）；0x42A8D2 7 项（全能力/攻击力/防御力/精神力/爆发力/士气/移动力）；0x479DF4 与 0x47A4B5 各 5 项五能力名。 | `candidate` / `static-verified` |
| `global.64.strategy-name-table.9112` 策略名表 | `0x004FF480` (va) | 108 | 27 项指针数组（全部下降/连续移动/生命交换/经验加倍…），6.5 迁至 0x4FFFF0；0x4FF4F0 起 16 项占位名「策略0017…」。 | `candidate` / `static-verified` |
