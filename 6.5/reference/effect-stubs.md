# 6.5 特效桩函数

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/stubs/effect-stubs.json`

> 候选桩地址不是空闲代码洞。复用前必须核对目标样本原字节、调用约定、覆盖范围和占用冲突。

| 桩函数 | 地址 | 风格 | 效果值/叠加 | 特效 ID（装备/个人） | 调度器/核心 | 状态/证据 |
|---|---|---|---|---|---|---|
| `stub.65.standard-4210d0` 引导攻击标准特效桩 | `0x004210D0` (va) | `standard-dispatch` | boolean / False | 54 / 24 | `0x006002C6` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.standard-421106` MP恢复标准特效桩 | `0x00421106` (va) | `standard-dispatch` | value / True | 27 / 1 | `0x0060002A` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.standard-421175` 二次行动标准特效桩 | `0x00421175` (va) | `standard-dispatch` | boolean / False | 90 / 56 | `0x00600819` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-472c41` 随机状态攻击内联特效桩 | `0x00472C41` (va) | `inline-core-call` | boolean / False | 94 / 11 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-4259af` 策略附带随机异常状态内联特效桩 | `0x004259AF` (va) | `inline-core-call` | value / False | 0 / 192 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-472d5f` 攻击附带属性下降内联特效桩 | `0x00472D5F` (va) | `inline-core-call` | boolean / False | 94 / 12 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-4528ff` 回MP攻击内联特效桩 | `0x004528FF` (va) | `inline-core-call` | value / False | 0 / 173 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-41a5bc` 策略偷钱内联特效桩 | `0x0041A5BC` (va) | `inline-core-call` | boolean / False | 0 / 170 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-445f6d` 策略冲锋内联特效桩 | `0x00445F6D` (va) | `inline-core-call` | value / False | 0 / 176 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-446170` 聚势伐谋内联特效桩 | `0x00446170` (va) | `inline-core-call` | value / False | 0 / 177 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-41ab03` 殭屍大法内联特效桩 | `0x0041AB03` (va) | `inline-core-call` | boolean / False | 0 / 178 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-441d1f` 多多益善内联特效桩 | `0x00441D1F` (va) | `inline-core-call` | boolean / False | 0 / 179 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-43d307` 敌潮逆噬内联特效桩 | `0x0043D307` (va) | `inline-core-call` | value / False | 0 / 180 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-4529b5` 盛气凌人内联特效桩 | `0x004529B5` (va) | `inline-core-call` | boolean / False | 0 / 191 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-4d3500` 大杀四方内联特效桩 | `0x004D3500` (va) | `inline-core-call` | value / False | 0 / 193 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-43d0e2` 无视策略减伤内联特效桩 | `0x0043D0E2` (va) | `inline-core-call` | boolean / False | 0 / 239 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-43d3ae` 策略保底内联特效桩 | `0x0043D3AE` (va) | `inline-core-call` | value / False | 0 / 255 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-43d3f9` 策略限伤内联特效桩 | `0x0043D3F9` (va) | `inline-core-call` | value / False | 0 / 255 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.inline-4072ca` 辅助五维特技加成内联特效桩 | `0x004072CA` (va) | `inline-core-call` | value / False | 0 / 190 | `-` / `fn.65.core-effect-engine` | `candidate` / `legacy-structured` |
| `stub.65.special-41aa98` 护卫特殊判定桩 | `0x0041AA98` (va) | `special-wrapper` | - / - | 0 / 209 | `-` / `-` | `candidate` / `legacy-structured` |
| `stub.65.special-41aa4f` 强化攻击穿透特殊判定桩 | `0x0041AA4F` (va) | `special-wrapper` | - / - | 0 / 221 | `-` / `-` | `candidate` / `legacy-structured` |

标准/内联桩参数压栈顺序：`effectValueFlag -> stackingFlag -> equipmentEffectId -> personalEffectId`。
