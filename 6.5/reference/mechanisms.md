# 6.5 机制与调用链

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/mechanisms/engine-mechanisms.json`

## 物理攻击范围到目标消费调用链

ID: `mechanism.65.physical-attack-targeting`

1. `fn.65.attack-entry`：物理攻击入口
2. `fn.65.attack-selector`：准备中心坐标和 packed range
3. `fn.65.attack-dispatch`：按范围 ID/段分派
4. `fn.65.attack-geometry`：展开相对坐标
5. `fn.65.map-unit-lookup`：坐标转单位
6. `fn.65.attack-append-target`：过滤并追加目标
7. `fn.65.target-consumer`：消费目标并写伤害/效果

穿透分支：`fn.65.pierce-loader` -> `fn.65.combat-context-init` -> `fn.65.pierce-expand-wrapper` -> `fn.65.pierce-geometry-dispatch` -> `fn.65.pierce-append-target` -> `fn.65.target-consumer`

## ID、战术单位和运行时记录转换链

ID: `mechanism.65.id-pointer-conversion`

1. `fn.65.battlefield-id-to-tactical-unit`：战场 ID 到 0x30 记录
2. `fn.65.tactical-unit-to-runtime-character`：战术记录到 0x48 人物记录
