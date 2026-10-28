# 6.6 Hook、补丁与定位器

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/patches/legacy-effect-injections.json`、`6.6/data/patches/shanzai-20261027-patches.json`、`6.6/data/patches/xiaoan-semantic-locators.json`、`6.6/data/patches/xiaoan-speed-patch-sites.json`

## 【修改記錄整理】

ID: `patch.66.legacy-fff6575df186`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00407FC7` (va) | `-` | `0A` | legacy-od-block | 1 | - |
| `0x00419B69` (va) | `-` | `0A` | legacy-od-block | 1 | - |
| `0x00409A43` (va) | `-` | `03` | legacy-od-block | 1 | - |
| `0x00417F23` (va) | `-` | `03` | legacy-od-block | 1 | - |
| `0x00423E9D` (va) | `-` | `6E` | legacy-od-block | 1 | - |
| `0x00423EA1` (va) | `-` | `6E` | legacy-od-block | 1 | - |
| `0x0042AC99` (va) | `-` | `6E` | legacy-od-block | 1 | - |
| `0x00407301` (va) | `-` | `63` | legacy-od-block | 1 | - |
| `0x00407309` (va) | `-` | `5A` | legacy-od-block | 1 | - |
| `0x00407311` (va) | `-` | `55` | legacy-od-block | 1 | - |
| `0x00407319` (va) | `-` | `46` | legacy-od-block | 1 | - |
| `0x00407305` (va) | `-` | `0B` | legacy-od-block | 1 | - |
| `0x0040730D` (va) | `-` | `08` | legacy-od-block | 1 | - |
| `0x00407315` (va) | `-` | `07` | legacy-od-block | 1 | - |
| `0x0040731D` (va) | `-` | `06` | legacy-od-block | 1 | - |
| `0x00407321` (va) | `-` | `05` | legacy-od-block | 1 | - |
| `0x00406CB5` (va) | `-` | `0A` | legacy-od-block | 1 | - |
| `0x00406CB9` (va) | `-` | `0A` | legacy-od-block | 1 | - |
| `0x00472DCF` (va) | `-` | `1B C5 48 00 1D C5 48 00 1F C5 48 00 21 C5 48 00 23 C5 48 00 25 C5 48 00 27 C5 48 00 29 C5 48 00 2B C5 48 00 2D C5 48 00` | legacy-od-block | 40 | - |
| `0x00478206` (va) | `-` | `CB 2D 47 00` | legacy-od-block | 4 | - |
| `0x0048C51B` (va) | `-` | `31 00 32 00 33 00 34 00 35 00 36 00 37 00 38 00 39 00 58 00` | legacy-od-block | 20 | - |
| `0x0043BD40` (va) | `-` | `72 11 2B 45 F0 31 D2 B9 03 00 00 00 F7 F1 01 45 FC EB 3B 8B 45 F0 2B 45 E0 31 D2 B9 03 00 00 00 F7 F1 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 50 FF 75 FC E8 1B 3D 04 00 83 C4 08 85 C0 75 01 40 89 45 FC 8B 4D D4 E8 CA 74 FD FF 85 C0 74 21 50 8B 4D 08 E8 AC 39 00 00 5A 2B C2 3C 00 7D 11 F7 D8 6B C0 05 FF 75 FC 50 E8 21 9D FE FF 01 45 FC FF 75 D4 FF 75 08 E8 71 A9 FE FF 83 F8 64 74 11 FF 75 FC 50 E8 05 9D FE FF 85 C0 75 01 40 89 45 FC 8B 4D D4` | legacy-od-block | 159 | - |
| `0x0043BD36` (va) | `-` | `19` | legacy-od-block | 1 | - |
| `0x0043BD48` (va) | `-` | `05` | legacy-od-block | 1 | - |
| `0x0043BD5C` (va) | `-` | `05` | legacy-od-block | 1 | - |
| `0x0043C126` (va) | `-` | `04` | legacy-od-block | 1 | - |
| `0x0043C139` (va) | `-` | `05` | legacy-od-block | 1 | - |
| `0x00424262` (va) | `-` | `14` | legacy-od-block | 1 | - |
| `0x0042426A` (va) | `-` | `0A` | legacy-od-block | 1 | - |
| `0x00421340` (va) | `-` | `04` | legacy-od-block | 1 | - |
| `0x00436479` (va) | `-` | `02` | legacy-od-block | 1 | - |
| `0x004240CE` (va) | `-` | `01 08 10 C0` | legacy-od-block | 4 | - |
| `0x0043F617` (va) | `-` | `22` | legacy-od-block | 1 | - |
| `0x0043F643` (va) | `-` | `22` | legacy-od-block | 1 | - |
| `0x0043F66F` (va) | `-` | `22` | legacy-od-block | 1 | - |
| `0x0043F69B` (va) | `-` | `22` | legacy-od-block | 1 | - |
| `0x0043F6C7` (va) | `-` | `22` | legacy-od-block | 1 | - |
| `0x00457409` (va) | `-` | `4C` | legacy-od-block | 1 | - |
| `0x00457417` (va) | `-` | `4D` | legacy-od-block | 1 | - |
| `0x004749BA` (va) | `-` | `19` | legacy-od-block | 1 | - |
| `0x00420ACC` (va) | `-` | `05 05 01 0C 0C 0C 0C 06 07 06 06 06 06 06 05 01 01 01 01 01 01 01 01 01 01 06 01 06 0F 08` | legacy-od-block | 30 | - |
| `0x0044C341` (va) | `-` | `FF 0C 12 13 1A FF 02 04 13 FF 03 0C FF` | legacy-od-block | 13 | - |
| `0x00406006` (va) | `-` | `E9 F5 4A 01 00 90` | legacy-od-block | 6 | - |
| `0x0041AB00` (va) | `-` | `8B 4D E0 6A 01 6A 01 6A 00 68 B2 00 00 00 E8 C6 56 FF FF 85 C0 74 0E 8B 4D E0 8B 49 10 39 4D DC 72 03 89 4D DC 8B 4D DC 8B 55 FC E9 DB B4 FE FF` | legacy-od-block | 48 | - |
| `0x0041AB08` (va) | `-` | `44` | legacy-od-block | 1 | - |
| `0x0041AB0A` (va) | `-` | `32` | legacy-od-block | 1 | - |

## 【6.6冥想回蓝百分比】：按百分比回蓝

ID: `patch.66.legacy-f4f49a0dea9f`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0041E3FD` (va) | `-` | `E9 1B 67 00 00 90` | legacy-od-block | 6 | - |
| `0x00424B1D` (va) | `-` | `51 52 8B 0D FC 7A 49 00 E8 65 27 FE FF 51 6A 32 E8 A7 0F 00 00 5A 59 8A D0 F7 DA E9 D2 98 FF FF` | legacy-od-block | 32 | - |
| `0x00424B2C` (va) | `-` | `32` | legacy-od-block | 1 | - |

## 骑马攻击（对骑兵类兵种增加效果值比例伤害）步兵攻击（对步兵类兵种增加效果值比例伤害）克制骑兵（受到骑兵类攻击伤害减轻效果值比例）克制步兵（受到步兵类攻击伤害减轻效果值比例）偷袭攻击（从侧面攻击物理伤害增加25%，背面攻击物理伤害增加50%）

ID: `patch.66.legacy-30ece703adf4`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043BEC6` (va) | `-` | `E8 35 69 09 00` | legacy-od-block | 5 | - |
| `0x004D2700` (va) | `-` | `55 8B EC 33 C0 50 8B 4D 08 80 79 0E 07 74 10 BA C2 E8 48 00 66 81 3A FF FF 74 04 FF 32 EB 03 FF 71 06 8B 4D 0C 8A 41 0F 8B D0 83 E2 01 85 D2 75 16 8A 51 07 3A 55 F9 74 26 77 06 3C 00 74 24 EB 1A 3C 02 74 1E EB 14 8A 51 06 3A 55 F8 74 10 77 06 3C 01 74 06 EB 0C 3C 03 75 08 33 C0 EB 06 B0 01 EB 02 B0 02 6B C0 19 50 FF 75 10 E8 68 33 F5 FF 01 45 10 01 45 FC 8B 4D 0C E8 91 3F F3 FF 3C 01 74 19 80 3D 9A 0E 50 00 01 75 10 6A 19 FF 75 10 E8 43 33 F5 FF 01 45 10 01 45 FC 8B 45 10 EB 03 8B 45 FC 8B E5 5D C2 0C 00` | legacy-od-block | 170 | - |
| `0x004D27E1` (va) | `-` | `55 8B EC E8 BE 8C F6 FF 3C 27 77 0D 25 FF 00 00 00 8A 80 C0 20 4D 00 EB 02 31 C0 8B E5 5D C3 55 8B EC FF 75 14 FF 75 10 FF 75 0C FF 75 08 E8 64 04 F4 FF 89 45 10 6A 00 6A 01 68 00 00 00 00 68 79 00 00 00 8B 4D 08 E8 AC D9 F3 FF 85 C0 74 1B 50 8B 4D 0C E8 A7 FF FF FF 83 F8 00 75 0D 58 FF 75 10 50 E8 90 32 F5 FF 01 45 10 6A 00 6A 01 68 00 00 00 00 68 7A 00 00 00 8B 4D 08 E8 77 D9 F3 FF 85 C0 74 1B 50 8B 4D 0C E8 72 FF FF FF 83 F8 02 75 0D 58 FF 75 10 50 E8 5B 32 F5 FF 01 45 10 6A 00 6A 01 68 00 00 00 00 68 7B 00 00 00 8B 4D 0C E8 42 D9 F3 FF 85 C0 74 1B 50 8B 4D 08 E8 3D FF FF FF 83 F8 00 75 0D 58 FF 75 10 50 E8 26 32 F5 FF 29 45 10 6A 00 6A 01 68 00 00 00 00 68 7C 00 00 00 8B 4D 0C E8 0D D9 F3 FF 85 C0 74 1B 50 8B 4D 08 E8 08 FF FF FF 83 F8 02 75 0D 58 FF 75 10 50 E8 F1 31 F5 FF 29 45 10 6A 01 6A 01 68 00 00 00 00 68 7D 00 00 00 8B 4D 08 E8 D8 D8 F3 FF 85 C0 74 11 FF 75 10 FF 75 0C FF 75 08 E8 ED FD FF FF 89 45 10 8B 45 10 8B E5 5D C2 10 00` | legacy-od-block | 318 | - |
| `0x004D281C` (va) | `-` | `80` | legacy-od-block | 1 | - |
| `0x004D2821` (va) | `-` | `AA` | legacy-od-block | 1 | - |
| `0x004D2851` (va) | `-` | `81` | legacy-od-block | 1 | - |
| `0x004D2856` (va) | `-` | `AC` | legacy-od-block | 1 | - |
| `0x004D2886` (va) | `-` | `82` | legacy-od-block | 1 | - |
| `0x004D288B` (va) | `-` | `AB` | legacy-od-block | 1 | - |
| `0x004D28BB` (va) | `-` | `83` | legacy-od-block | 1 | - |
| `0x004D28C0` (va) | `-` | `AD` | legacy-od-block | 1 | - |
| `0x004D28F0` (va) | `-` | `84` | legacy-od-block | 1 | - |
| `0x004D28F5` (va) | `-` | `AE` | legacy-od-block | 1 | - |

## 建言闪退

ID: `patch.66.legacy-a6f65e5c4325`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C6A9` (va) | `-` | `83 7D F0 05 77 11 FF 75 FC FF 75 F8 FF 75 EC E8 FC DF FD FF 89 45 FC 8B 45 FC 8B 4D F8 80 7D F0 0E 75 19 03 41 14 50 8B 4D F4 E8 B7 AB FC FF 59 3B C8 76 22 8B 4D F8 2B 41 14 EB 17 03 41 10 50 8B 4D F4 E8 72 AB FC FF 59 3B C8 76 09 8B 4D F8 2B 41 10 89 45 FC 8B 45 FC 8B E5 5D C2 0C 00` | legacy-od-block | 95 | - |
| `0x0045F4F4` (va) | `-` | `8B 0D 84 5E 4B 00` | legacy-od-block | 6 | - |
| `0x0040732E` (va) | `-` | `51 E8 AA 71 02 00 59 8B 55 08 E8 00 FB 02 00 5D C2 04 00` | legacy-od-block | 19 | - |
| `0x0043FAE7` (va) | `-` | `3C 02` | legacy-od-block | 2 | - |
| `0x0040D597` (va) | `-` | `A1 A1 A5 A5 A1 A2 A4 A3 A3 A6 A2 A4 A3` | legacy-od-block | 13 | - |
| `0x004E606C` (va) | `-` | `E8 8A 03 F2 FF 90 90 90 90 90 90 90 90` | legacy-od-block | 13 | - |
| `0x0040C807` (va) | `-` | `51 6A 01 E8 9A 31 04 00 85 C0 74 04 83 45 F8 64 FF 75 F8 E8 91 26 05 00 90 90` | legacy-od-block | 26 | - |
| `0x00434258` (va) | `-` | `C2 08 00` | legacy-od-block | 3 | - |

## 从上到下分别是 V X S A B （16进制）

ID: `patch.66.legacy-e78c92a13196`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00407301` (va) | `-` | `7D` | legacy-od-block | 1 | - |
| `0x00407309` (va) | `-` | `64` | legacy-od-block | 1 | - |
| `0x00407311` (va) | `-` | `5A` | legacy-od-block | 1 | - |
| `0x00407319` (va) | `-` | `50` | legacy-od-block | 1 | - |
| `0x00407321` (va) | `-` | `46` | legacy-od-block | 1 | - |

## 【6.6x KF】修正杀敌加成卡死

ID: `patch.66.legacy-9f145c7e71e7`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00407180` (va) | `-` | `E8 3B 53 03 00` | legacy-od-block | 5 | - |
| `0x004071B5` (va) | `-` | `E8 06 53 03 00` | legacy-od-block | 5 | - |
| `0x004071EA` (va) | `-` | `E8 D1 52 03 00` | legacy-od-block | 5 | - |
| `0x0040721F` (va) | `-` | `E8 9C 52 03 00` | legacy-od-block | 5 | - |
| `0x00407254` (va) | `-` | `E8 67 52 03 00` | legacy-od-block | 5 | - |
| `0x0043C4C0` (va) | `-` | `55 8B EC 51 51 8B 55 08 D1 E2 0F B7 44 11 11 FF 75 08 E8 CD 00 00 00 FF 75 08 E8 E8 02 00 00 8B 4D F8` | legacy-od-block | 34 | - |

## 保底全伤害，因为是固定值没有成长性，不好设置特效值，现在效果改为 保底自身等级+N

ID: `patch.66.legacy-70286c122d3d`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00433FF4` (va) | `-` | `E8 0B 02 00 00` | legacy-od-block | 5 | - |
| `0x004341B7` (va) | `-` | `8B 4D 0C E8 B5 E4 FD FF 01 45 FC 8B 4D 10 E8 C5 23 FD FF E8 94 30 FD FF 50 8B 4D 10 E8 28 73 FE FF 59 6B C0 64 33 D2 F7 F9 83 F8 32 77 10 8B 45 FC 50 6A 1E E8 E9 18 FF FF 59 03 C1 EB 01 58 39 45 08 72 03 8B 45 08 8B E5 5D C2 0C 00 55 8B EC 6A 00 6A 01 68 00 00 00 00 68 D8 00 00 00 8B 4D 0C E8 BC BF FD FF 85 C0 74 2B 50 8B 4D 0C E8 65 23 FD FF E8 34 30 FD FF 50 E8 A4 18 FF FF 39 45 08 72 05 89 45 08 EB 0D FF 75 08 6A 14 E8 90 18 FF FF 29 45 08 8B 45 08 83 F8 00 77 01 40 8B E5 5D C2 0C 00` | legacy-od-block | 164 | - |

## 修复提升周围buff bug的，并正确改为3个

ID: `patch.66.legacy-a283e7c5143c`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042F8DD` (va) | `-` | `E9 5C 0A 00 00 8B 45 F8 3C 0A 0F 83 A7 00 00 00 33 D2 3C 06 72 05 8B D0 83 EA 05` | legacy-od-block | 27 | - |
| `0x0043033E` (va) | `-` | `33 C0 6A 03 50 50 E9 99 F5 FF FF` | legacy-od-block | 11 | - |
| `0x0042F897` (va) | `-` | `04 89` | legacy-od-block | 2 | - |

## 只适用6.6xKF-241特技引擎，增加【致命一击】【众矢之的】【逆境减伤】特效值显示后缀（1=攻击 2=策略 3=ALL）

ID: `patch.66.legacy-80d08ed1e077`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00428351` (va) | `-` | `3C 0F 73 2A 3C 0D 75 0B FE C9 8D 8C 89 70 C4 48 00 EB 68 3C 0C 75 0A 3E 8D 0C CD B0 AE 41 00 EB 5A 3C 0E 75 0B 8D 8C 89 CB AF 41 00 EB 4D` | legacy-od-block | 46 | - |
| `0x0001A3D0` (fileOffset) | `-` | `B9 A5 BB F7 00 B2 DF C2 D4 00 41 4C 4C 00` | legacy-ue-block | 14 | - |
| `0x0009EB3F` (fileOffset) | `-` | `0F` | legacy-ue-block | 1 | - |
| `0x0009ED3F` (fileOffset) | `-` | `0F` | legacy-ue-block | 1 | - |
| `0x0009F32F` (fileOffset) | `-` | `0F` | legacy-ue-block | 1 | - |

## 九宫范围内的友军被攻击时，目标强制转为自己，目标被围攻时无效。（和先手触发的时机相同，例如，奋战或[连击]不会触发先手，这个也无法触发）

ID: `patch.66.legacy-642886b45da3`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004105C8` (va) | `-` | `E8 CB A4 00 00 90 85 C0 74 02 87 D1 52 51` | legacy-od-block | 14 | - |
| `0x0043ACA2` (va) | `-` | `E8 F1 FD FD FF 90 90 90 90` | legacy-od-block | 9 | - |
| `0x0043DB63` (va) | `-` | `EB 15 FF 75 08 FF 75 10 E8 AC 33 FD FF 8A 4D F4 88 4D 10 3C FF 74 1B 8A 55 10 8B 4D 08 8B 49 04 85 C0 74 02 87 CA 52 51 B9 F0 27 49 00 E8 5C 89 FC FF 8B 4D 08 FF 75 FC E8 A4 E5 FE FF 84 C0 74 03 88 4D FC 8A 4D FC FF 75 08 E8 F7 47 FE FF 8B E5 5D C2 10 00` | legacy-od-block | 85 | - |
| `0x00410F23` (va) | `-` | `E8 94 9B 00 00` | legacy-od-block | 5 | - |
| `0x0041AA98` (va) | `-` | `8B 54 24 FC 8B 4C 24 F0 8B 49 04 C3 55 8B EC 6A 01 6A 01 68 00 00 00 00 68 DA 00 00 00 E8 1F 57 FF FF 5D C3 55 8B EC 6A 00 51 E8 32 B7 FE FF 51 33 C0 50 50 B8 11 7C 41 00 39 45 10 74 7F E8 C9 FF FF FF 85 C0 75 76 6A 00 6A 01 6A 01 6A 02 8B 4D F4 E8 05 E7 FE FF 8B 45 FC 8A 88 48 C7 4A 00 80 F9 FF 74 58 3A 4D F8 74 4E E8 F2 B6 FE FF 89 4D EC 6A 08 E8 D7 94 00 00 85 C0 75 3B 8B 4D EC E8 87 FF FF FF 85 C0 74 2F 3C 01 74 1A 8B 4D 18 E8 93 4D 02 00 8B 4D EC FF 71 04 FF 75 18 E8 F5 7F FF FF 85 C0 74 11 8B 4D EC 8B 41 10 3B 45 F0 76 06 89 45 F0 89 4D F4 FF 45 FC EB 9A 8B 4D F4 8B 45 18 89 45 08 83 7D F0 00 74 35 8A 41 04 88 45 14 FF 75 08 51 E8 CA 71 00 00 8B 4D F4 0F B6 41 04 05 04 04 00 00 50 68 E0 AF 41 00 E8 D3 EA 03 00 8B 4D F4 51 FF 75 08 E8 A7 71 00 00 8B 4D F4 8B E5 5D C3` | legacy-od-block | 261 | - |
| `0x0041AFE0` (va) | `-` | `D0 DD C9 CB CE E1 D6 F7 A3 A1 00` | legacy-od-block | 11 | - |
| `0x0041AAAC` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041AAB1` (va) | `-` | `DA` | legacy-od-block | 1 | - |
| `0x0041AAE4` (va) | `-` | `01` | legacy-od-block | 1 | - |
| `0x0041AB7B` (va) | `-` | `04 04` | legacy-od-block | 2 | - |

## 【6.6x】致死不触发转移伤害

ID: `patch.66.legacy-66aacc7e1454`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004182B1` (va) | `-` | `FF 75 EC E8 D7 27 00 00 3B D1 90 90 73 5B` | legacy-od-block | 14 | - |
| `0x0041AA90` (va) | `-` | `55 8B EC 8D 84 88 84 00 00 00 8B 10 3E 8B 4D 08 8B 49 10 8B E5 5D C2 04 00` | legacy-od-block | 25 | - |

## 【Star6.6x】调整强化穿透攻击

ID: `patch.66.legacy-1f1d447d975e`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00407878` (va) | `-` | `E8 D2 31 01 00` | legacy-od-block | 5 | - |
| `0x0041AA4F` (va) | `-` | `55 8B EC 50 33 C0 38 05 DC 5F 50 00 75 19 8B 45 08 E8 05 29 04 00 8B 4D FC 85 45 08 74 08 8A 81 7C AA 41 00 EB 01 91 8B E5 5D C2 04 00 04 02 03 08 07 05 06 05 06 01 0A` | legacy-od-block | 56 | - |

## 附加特技到回合数必失效

ID: `patch.66.legacy-9782f818e821`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042FC62` (va) | `-` | `B8 01 00 00 00 90 90 90` | legacy-od-block | 8 | - |

## 化力为疗：特效值的概率将伤害转化为自身回复（概率默认伪随机）

ID: `patch.66.legacy-b41e1ef7698d`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00405AA1` (va) | `-` | `52 E8 AD 72 00 00 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 5A E8 42 72 00 00` | legacy-od-block | 29 | - |
| `0x0040CD00` (va) | `-` | `55 8B EC 6A 00 52 6A 00 6A 00 FF 75 20 FF 75 24 8B 4D 2C FF 31 FF 71 01 8B 4D 08 E8 66 3C 04 00 8B E5 5D C3 55 8B EC 6A 00 6A 01 68 57 00 00 00 68 C0 00 00 00 E8 9F 34 00 00 5D C3 55 8B EC 6A 00 6A 01 68 00 00 00 00 68 C1 00 00 00 E8 87 34 00 00 5D C3 55 8B EC FF 75 1C FF 75 28 E8 9E 01 00 00 89 45 28 FF 75 1C FF 75 18 E8 EC 01 00 00 8B E5 5D C3` | legacy-od-block | 116 | - |
| `0x0040CF00` (va) | `-` | `55 8B EC 8B 4D 0C E8 19 FE FF FF 85 C0 74 44 50 33 C0 B9 F5 1B 50 00 E8 09 8F 04 00 59 3B C1 77 32 8B 4D 0C E8 D7 E5 00 00 3B 45 08 74 25 50 8B 4D 0C E8 58 96 FF FF E8 27 A3 FF FF 59 2B C1 8B 4D 08 3B C1 72 08 6B C9 02 29 4D 08 EB 05 03 C1 29 45 08 8B 45 08 8B E5 5D C2 08 00 55 8B EC 6A 00 6A 00 6A 01 8B 4D 08 E8 CF FD FF FF 85 C0 74 7F 8B 55 0C 8B 45 FC 3C 06 74 26 8A 4A 18 80 F9 03 76 15 8B 45 F4 01 45 F8 8B 4D 0C 52 6A 00 FF 75 FC E8 8A C8 FF FF 5A D1 65 F4 42 FF 45 FC EB D3 83 7D F8 00 74 27 33 C0 40 89 45 FC 8B 45 FC 3C 06 77 3C F6 45 F8 01 74 0C 8B 4D 08 48 6A 01 50 E8 5B C8 FF FF FF 45 FC D1 6D F8 EB DF 8B 4D 0C E8 7D 5C 06 00 85 C0 8B 4D 0C 8B 45 08 0F 45 C8 6A 06 E8 2B 2B 07 00 6A 00 50 E8 31 C8 FF FF 8B E5 5D C2 08 00` | legacy-od-block | 246 | - |
| `0x0040CD2C` (va) | `-` | `57` | legacy-od-block | 1 | - |
| `0x0040CD31` (va) | `-` | `C0` | legacy-od-block | 1 | - |
| `0x0040CD44` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0040CD49` (va) | `-` | `C1` | legacy-od-block | 1 | - |

## 辅助移动力-个人特效号（宝物号默认原始）

ID: `patch.66.legacy-e83cc4741f0a`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004072E9` (va) | `-` | `E8 7A 72 02 00` | legacy-od-block | 5 | - |
| `0x0042E568` (va) | `-` | `55 8B 4C 24 0C 8B EC 03 4D 08 51 6A 00 6A 01 6A 00 68 B1 00 00 00 8B 4D 18 E8 09 6C FF FF 01 45 FC 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 6A 00 6A 01 68 00 00 00 00 68 F6 00 00 00 8B 4D 18 E8 E0 6B FF FF 85 C0 74 0D 59 3B C8 77 04 33 C9 EB 05 2B C8 EB 01 59 8B 45 10 3B C8 7F 02 8B C1 5D C3` | legacy-od-block | 100 | - |
| `0x0042E57A` (va) | `-` | `B4` | legacy-od-block | 1 | - |
| `0x0042E59E` (va) | `-` | `88` | legacy-od-block | 1 | - |
| `0x0042E5A3` (va) | `-` | `B5` | legacy-od-block | 1 | - |

## 每行显示宝物最大数量（目前设置5，可自行调整，数值输入十六进制）

ID: `patch.66.legacy-2b2bf1f59374`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0047073C` (va) | `-` | `05` | legacy-od-block | 1 | - |
| `0x00470746` (va) | `-` | `0A` | legacy-od-block | 1 | - |

## 拆分四系增伤（无法使用形象指定器里的宝物修改来调整序号）

ID: `patch.66.legacy-a7f795d67fbf`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C210` (va) | `-` | `8B 4D DC 80 F9 00 75 06 B0 77 B1 38 EB 3A 80 F9 01 75 06 B0 78 B1 38 EB 2F 80 F9 02 75 06 B0 79 B1 38 EB 24 80 F9 03 75 06 B0 7A B1 38 EB 19 80 F9 26 75 06 B0 7B B1 38 EB 0E 8B 4D F0 E8 6B 9B FC FF 85 C0 74 22 EB 14 6A 00 6A 01 51 50 8B 4D F0 31 C0 E8 71 3F FD FF 85 C0 74 0C 50 FF 75 FC E8 64 98 FE FF 01 45 FC 8B 4D 08 51 8B 4D F0 E8 B0 22 FF FF` | legacy-od-block | 116 | - |
| `0x0042E534` (va) | `-` | `55 8B EC 6A 00 6A 01 68 FF 00 00 00 68 28 00 00 00 E8 8F 1C FE FF 85 C0 74 04 33 C0 EB 10 6A 00 6A 01 6A 43 6A 29 8B 4D 08 E8 77 1C FE FF 8B E5 5D C2 04 00` | legacy-od-block | 52 | - |
| `0x0043C219` (va) | `-` | `28` | legacy-od-block | 1 | - |
| `0x0043C21B` (va) | `-` | `38` | legacy-od-block | 1 | - |
| `0x0043C224` (va) | `-` | `28` | legacy-od-block | 1 | - |
| `0x0043C226` (va) | `-` | `38` | legacy-od-block | 1 | - |
| `0x0043C22F` (va) | `-` | `28` | legacy-od-block | 1 | - |
| `0x0043C231` (va) | `-` | `38` | legacy-od-block | 1 | - |
| `0x0043C23A` (va) | `-` | `28` | legacy-od-block | 1 | - |
| `0x0043C23C` (va) | `-` | `38` | legacy-od-block | 1 | - |
| `0x0043C245` (va) | `-` | `28` | legacy-od-block | 1 | - |
| `0x0043C247` (va) | `-` | `38` | legacy-od-block | 1 | - |
| `0x0042E557` (va) | `-` | `43` | legacy-od-block | 1 | - |
| `0x0042E559` (va) | `-` | `29` | legacy-od-block | 1 | - |
| `0x0042E53C` (va) | `-` | `FF` | legacy-od-block | 1 | - |
| `0x0042E541` (va) | `-` | `28` | legacy-od-block | 1 | - |

## 暴击伤害增幅 K%：计算暴击伤害时，在原加成基础上额外增加K%（加算，非乘算）。

ID: `patch.66.legacy-590df7beeba4`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00405F02` (va) | `-` | `FF 75 F4 FF 75 DC FF 75 D8 E8 37 84 02 00 90 90 90 90 90 90 90` | legacy-od-block | 21 | - |
| `0x0042E4FD` (va) | `-` | `55 8B EC 8B 4D 10 8B 49 0C 6A 00 6A 01 6A 00 6A 70 E8 C6 1C FE FF 8B 4D 0C D1 F9 85 C0 74 02 03 C8 8B 55 08 FF 32 51 E8 B0 75 FF FF 8B 55 08 01 02 8B E5 5D C2 0C 00` | legacy-od-block | 55 | - |

## 宝物特效

ID: `patch.66.legacy-d8bf47aca205`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00417A5A` (va) | `-` | `E9 E8 68 01 00` | legacy-od-block | 5 | - |
| `0x0042E347` (va) | `-` | `E8 40 EB FE FF 50 8B 4D 08 6A 01 6A 01 6A 00 68 6D 00 00 00 E8 79 1E FE FF 85 C0 74 46 8B 4D 08 83 C1 2E 8A 01 25 FF 00 00 00 B9 19 00 00 00 F7 E1 05 20 F8 49 00 83 C0 11 8A 08 80 F9 01 75 05 58 B0 06 EB 1F 80 F9 03 75 05 58 B0 13 EB 15 80 F9 05 75 05 58 B0 08 EB 0B 80 F9 07 75 05 58 B0 20 EB 01 58 E9 AF 96 FE FF` | legacy-od-block | 105 | - |
| `0x0042E355` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0042E357` (va) | `-` | `6D` | legacy-od-block | 1 | - |

## 受到的策略治疗效果加强X%

ID: `patch.66.legacy-c958756253a7`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C6A9` (va) | `-` | `FF 75 FC FF 75 F8 FF 75 EC E8 02 E0 FD FF 89 45 FC 8B 45 FC 8B 4D F8 80 7D F0 0E 75 19 03 41 14 50 8B 4D F4 E8 BD AB FC FF 59 3B C8 76 22 8B 4D F8 2B 41 14 EB 17 03 41 10 50 8B 4D F4 E8 78 AB FC FF 59 3B C8 76 09 8B 4D F8 2B 41 10 89 45 FC 8B 45 FC 8B E5 5D C2 0C 00` | legacy-od-block | 89 | - |
| `0x0041A6B9` (va) | `-` | `55 8B EC 6A 01 6A 01 68 00 00 00 00 68 B6 00 00 00 8B 4D 0C E8 07 5B FF FF 85 C0 74 0C FF 75 10 50 E8 FA B3 00 00 01 45 10 6A 01 6A 01 68 00 00 00 00 68 B7 00 00 00 8B 4D 14 E8 E1 5A FF FF 85 C0 74 0C FF 75 10 50 E8 D4 B3 00 00 01 45 10 8B 45 10 6A 01 6A 01 68 00 00 00 00 68 F1 00 00 00 8B 4D 0C E8 B8 5A FF FF 85 C0 74 18 83 F8 64 72 07 B8 00 00 00 00 EB 0F FF 75 10 50 E8 9F B3 00 00 29 45 10 8B 45 10 8B E5 5D C2 0C 00` | legacy-od-block | 141 | - |
| `0x0041A6C1` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041A6C6` (va) | `-` | `B6` | legacy-od-block | 1 | - |
| `0x0041A6E7` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041A6EC` (va) | `-` | `B7` | legacy-od-block | 1 | - |
| `0x0041A710` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041A715` (va) | `-` | `FF` | legacy-od-block | 1 | - |

## 【免疫物理攻击】

ID: `patch.66.legacy-93e89196aacf`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00428961` (va) | `-` | `17 B6 43 00` | legacy-od-block | 4 | - |
| `0x0043B4CA` (va) | `-` | `E8 48 01 00 00` | legacy-od-block | 5 | - |
| `0x0043B617` (va) | `-` | `55 8B EC 33 C0 50 51 83 EC 08 80 3D 9A 0E 50 00 02 74 29 FF 75 0C E8 6B 04 00 00 85 C0 74 1F` | legacy-od-block | 31 | - |
| `0x0043BA83` (va) | `-` | `55 8B EC 6A 01 6A 00 68 FF 00 00 00 68 F0 00 00 00 E8 40 47 FD FF 8B E5 5D C3 55 8B EC 8B 4D 08 E8 DB FF FF FF 85 C0 74 04 33 C0 EB 05 B8 01 00 00 00 8B E5 5D C2 04 00` | legacy-od-block | 56 | - |
| `0x0043BF0E` (va) | `-` | `E9 1C FD FF FF 90 90` | legacy-od-block | 7 | - |
| `0x0043BC2F` (va) | `-` | `50 FF 75 08 E8 65 FE FF FF 85 C0 75 05 33 C0 89 45 FC 8B 45 FC 8B 4D 08 8B 49 10 E9 C4 02 00 00` | legacy-od-block | 32 | - |

## 攻击命中后可以清空敌人的MP（无视MP防御）。

ID: `patch.66.legacy-12db9daf127d`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00405FB0` (va) | `-` | `E9 BE 6C 00 00 90 90 90` | legacy-od-block | 8 | - |
| `0x0040CC73` (va) | `-` | `FF 75 F4 FF 75 E0 E8 23 00 00 00 85 C0 74 12 33 C9 89 4D D4 8B 55 FC 8B 4D F4 89 84 91 54 02 00 00 8B 4D E0 E8 10 44 01 00 E9 14 93 FF FF 55 8B EC 6A 00 8B 4D 0C 8B 49 0C 6A 00 6A 01 68 00 00 00 00 68 B3 00 00 00 E8 1A 35 00 00 85 C0 74 08 8B 4D 08 E8 75 5B 06 00 8B E5 5D C2 08 00` | legacy-od-block | 94 | - |
| `0x0040CCB1` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0040CCB6` (va) | `-` | `B3` | legacy-od-block | 1 | - |

## 个人特效起始号，特技后缀类型改为C，能正常显示二穿 三穿（宝物号默认原始）

ID: `patch.66.legacy-e9c578987127`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0040785C` (va) | `-` | `E8 E7 5B 05 00` | legacy-od-block | 5 | - |
| `0x0045D435` (va) | `-` | `55 8B EC 6A 00 6A 02 6A 33 04 95 50 E8 49 7D FC FF 5D C3 55 8B EC 6A 00 51 8B 45 FC 3C 06 73 11 8B 4D F8 E8 D8 FF FF FF 85 C0 75 07 FF 45 FC EB E8 33 C0 8B E5 5D C3` | legacy-od-block | 55 | - |
| `0x0045D43F` (va) | `-` | `FF` | legacy-od-block | 1 | - |
| `0x0045F452` (va) | `-` | `06` | legacy-od-block | 1 | - |

## 【破坏能力-策略】施放策略命中敌人后，破坏其能力。(降能力，八阵图，四神，拓展策略无效)

ID: `patch.66.legacy-d8a080078b2d`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042305E` (va) | `-` | `FF 75 FC E8 5C B3 00 00 E9 45 B3 00 00` | legacy-od-block | 13 | - |
| `0x0042E3B0` (va) | `-` | `6A 01 6A 00 8B 55 FC FF B2 06 05 00 00 E9 A9 4C FF FF 55 8B EC 6A 00 6A 00 6A 00 6A 00 8B 55 08 8B 4A 08 E8 E0 F0 02 00 85 C0 0F 84 AC 00 00 00 89 45 FC 8B 55 08 0F B6 0A E8 14 5C 05 00 E8 19 43 01 00 83 F8 13 0F 83 90 00 00 00 83 F8 0F 73 09 83 F8 07 0F 83 82 00 00 00 33 C0 89 45 F8 EB 03 FE 45 F8 8B 45 F8 8B 55 08 8A 4C 10 0D 80 F9 FF 74 69 80 B8 F9 7E 49 00 00 74 5E 88 4A 0C E8 C5 7D FD FF 83 7D FC 40 74 41 33 C0 89 45 F4 8B 45 FC 89 45 F0 EB 0E FF 45 F4 D1 E8 89 45 F0 83 7D F4 06 73 35 8B 45 F0 83 E0 01 85 C0 74 17 8B 55 08 33 C9 8A 4A 0C E8 8D 7D FD FF 6A 00 FF 75 F4 E8 AB B3 FD FF 8B 45 F0 EB CC 6A 06 E8 91 16 05 00 6A 00 50 E8 97 B3 FD FF EB 85 8B E5 5D C2 04 00` | legacy-od-block | 226 | - |
| `0x0045D4B8` (va) | `-` | `55 8B EC 6A 00 6A 01 6A 00 04 7D 50 E8 23 2D FB FF 5D C3 55 8B EC 6A 00 51 8B 45 FC 3C 03 73 11 8B 4D F8 E8 D8 FF FF FF 85 C0 75 07 FF 45 FC EB E8 33 C0 8B E5 5D C3` | legacy-od-block | 55 | - |
| `0x0045D4AB` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0045D4AF` (va) | `-` | `7D` | legacy-od-block | 1 | - |
| `0x0045F4C2` (va) | `-` | `03` | legacy-od-block | 1 | - |

## 能力6档+强化成长，特效值1 2 4 8 16分别对应攻防精敏士，可叠加

ID: `patch.66.legacy-da7457091d7a`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004072F2` (va) | `-` | `55 8B EC 8B 45 08 3C 04 77 30 8A 44 08 21 3C 32 72 04 B0 06 EB 26 3C 2D 7C 04 B0 05 EB 1E 3C 28 7C 04 B0 04 EB 16 3C 23 7C 04 B0 03 EB 0E 3C 23 7C 04 B0 02 EB 06 B0 01 EB 02 33 C0 E8 AB 71 02 00 8B 55 08 E8 02 FB 02 00 5D C2 04 00` | legacy-od-block | 77 | - |
| `0x0042E4DE` (va) | `-` | `55 8B EC 50 E8 08 F0 02 00 85 C0 74 0D 8B 4D 10 D3 E8 83 E0 01 D1 E0 01 45 FC 58 8B E5 5D C3` | legacy-od-block | 31 | - |
| `0x0045D4DC` (va) | `-` | `55 8B EC 6A 00 6A 01 6A 00 04 7A 50 E8 A2 7C FC FF 5D C3 55 8B EC 6A 00 51 8B 45 FC 3C 03 73 11 8B 4D F8 E8 D8 FF FF FF 85 C0 75 07 FF 45 FC EB E8 33 C0 8B E5 5D C3` | legacy-od-block | 55 | - |
| `0x0042E4BA` (va) | `-` | `55 8B EC 8B 45 08 2C A0 6B C0 03 8D 54 08 50 8B 45 08 66 89 02 C6 42 01 00 51 52 E8 0C AE FE FF 5D C2 04 00` | legacy-od-block | 36 | - |
| `0x0046B231` (va) | `-` | `E8 84 32 FC FF` | legacy-od-block | 5 | - |
| `0x00478205` (va) | `-` | `BA DB 2D 47 00` | legacy-od-block | 5 | - |
| `0x00472DDF` (va) | `-` | `24 C5 48 00` | legacy-od-block | 4 | - |
| `0x00406CB5` (va) | `-` | `06` | legacy-od-block | 1 | - |
| `0x00406CB9` (va) | `-` | `06` | legacy-od-block | 1 | - |
| `0x0045D4E6` (va) | `-` | `7A` | legacy-od-block | 1 | - |
| `0x0045F4F9` (va) | `-` | `03` | legacy-od-block | 1 | - |
| `0x0008AF24` (fileOffset) | `-` | `43 00 42 00 41 00 53 00 58 00 56 00` | legacy-ue-block | 12 | - |

## 【固定增伤 K】：自身攻击计算最终伤害时，伤害固定增加K（无视减伤，但不无视限制伤害），K为设定值或特效值。

ID: `patch.66.legacy-9779a39ce330`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043BEE8` (va) | `-` | `E9 6F 2B 00 00 90 90 90` | legacy-od-block | 8 | - |
| `0x0043EA5C` (va) | `-` | `FF 75 D4 FF 75 FC E8 69 A5 00 00 89 45 FC FF 75 08 FF 75 D4 FF 75 FC E8 DB A4 00 00 89 45 FC 8B 4D 08 E8 6D D9 FF FF E9 67 D4 FF FF` | legacy-od-block | 44 | - |
| `0x00448F53` (va) | `-` | `55 8B EC 8B 4D 0C E8 31 D6 FB FF E8 6D D6 FB FF 50 6A 00 6A 01 68 00 00 00 00 68 A5 00 00 00 8B 4D 0C E8 5F 72 FC FF 85 C0 74 0E 83 F8 01 75 09 8B 45 FC 6B C0 01 83 C0 05 03 45 08 50 6A 00 6A 01 68 00 00 00 00 68 A6 00 00 00 8B 4D 10 E8 33 72 FC FF 85 C0 74 1F 83 F8 01 75 09 8B 45 FC 6B C0 01 83 C0 05 8B 4D F8 2B C8 83 F9 00 7F 03 33 C9 41 8B C1 EB 01 58 8B E5 5D C2 0C 00 55 8B EC 6A 00 68 B0 00 00 00 6A 00 6A 00 33 C0 89 45 F4 EB 03 FF 45 F4 83 7D F4 05 74 3D 8B 4D 0C 8B 55 F4 03 55 F8 52 E8 37 00 00 00 85 C0 74 22 89 45 F0 8B 4D 0C E8 83 D5 FB FF 8B 55 F4 3E FF 14 95 00 00 43 00 50 FF 75 F0 E8 B9 CA FD FF 83 C0 00 03 45 FC 89 45 FC EB BA 03 45 08 8B E5 5D C2 08 00 55 8B EC 6A 00 6A 01 68 00 00 00 00 FF 75 08 E8 91 71 FC FF 8B E5 5D C2 04 00` | legacy-od-block | 251 | - |
| `0x00448F69` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00448F6E` (va) | `-` | `A5` | legacy-od-block | 1 | - |
| `0x00448F88` (va) | `-` | `01` | legacy-od-block | 1 | - |
| `0x00448F8B` (va) | `-` | `05` | legacy-od-block | 1 | - |
| `0x00448F95` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00448F9A` (va) | `-` | `A6` | legacy-od-block | 1 | - |
| `0x00448FB4` (va) | `-` | `01` | legacy-od-block | 1 | - |
| `0x00448FB7` (va) | `-` | `05` | legacy-od-block | 1 | - |
| `0x0044903C` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00448FD6` (va) | `-` | `A0 00 00 00` | legacy-od-block | 4 | - |
| `0x00449022` (va) | `-` | `00` | legacy-od-block | 1 | - |

## 个人特效起始号（宝物号默认原始）

ID: `patch.66.legacy-6003ea65ce5f`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043F8FB` (va) | `-` | `E8 7F DB 01 00` | legacy-od-block | 5 | - |
| `0x0045D46C` (va) | `-` | `55 8B EC 6A 00 6A 01 6A 32 04 9B 50 E8 5C 2D FB FF 5D C3 55 8B EC 6A 00 51 8B 45 FC 3C 06 73 11 8B 4D F8 E8 D8 FF FF FF 85 C0 75 07 FF 45 FC EB E8 33 C0 8B E5 5D C2 0C 00` | legacy-od-block | 57 | - |
| `0x0045D476` (va) | `-` | `FF` | legacy-od-block | 1 | - |
| `0x0045F489` (va) | `-` | `06` | legacy-od-block | 1 | - |

## 建议先注入 连击 反击等特技、再注入此补丁

ID: `patch.66.legacy-7d8b034c6cf0`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00406128` (va) | `-` | `E8 B3 DF 0D 00` | legacy-od-block | 5 | - |
| `0x004131E4` (va) | `-` | `E8 F7 0E 0D 00` | legacy-od-block | 5 | - |
| `0x004E40E0` (va) | `-` | `55 8B EC 83 EC 08 51 FF 71 0C 8A 49 01 E8 07 21 F2 FF 6A 00 6A 03 51 6A 03 FF 75 F0 E8 AA 91 F2 FF 89 45 FC 89 55 F8 8B 4D F0 6A 01 6A 01 6A 42 6A 34 E8 C2 C0 F2 FF 85 C0 74 04 B0 64 EB 35 8B 4D F0 6A 01 6A 01 68 00 00 00 00 68 B8 00 00 00 E8 A4 C0 F2 FF 85 C0 74 10 8B 4D F4 83 3D F4 2D 49 00 01 75 04 B0 64 EB 0B FF 75 F8 FF 75 FC E8 B6 1B F2 FF 89 45 FC 8B 4D F0 6A 00 6A 01 68 00 00 00 00 68 B9 00 00 00 68 FF 00 00 00 68 FF 00 00 00 6A 00 E8 87 A8 00 00 85 C0 74 06 03 45 FC 89 45 FC 8B 4D F0 6A 00 6A 01 68 00 00 00 00 68 BA 00 00 00 68 FF 00 00 00 68 FF 00 00 00 6A 00 E8 5B A8 00 00 85 C0 74 0A 0F B6 0D 48 0C 50 00 0F AF C1 03 45 FC 83 F8 64 76 02 B0 64 89 45 FC 8B 45 FC 8B 4D F0 6A 00 6A 01 68 00 00 00 00 68 F0 00 00 00 68 FF 00 00 00 68 FF 00 00 00 6A 00 E8 1B A8 00 00 85 C0 74 11 39 45 FC 76 05 29 45 FC EB 07 C7 45 FC 00 00 00 00 8B 45 FC 8B E5 5D C3` | legacy-od-block | 289 | - |
| `0x004EEA00` (va) | `-` | `55 8B EC 51 FF 75 20 FF 75 1C FF 75 18 FF 75 14 E8 C4 17 F2 FF 50 FF 75 20 FF 75 1C FF 75 10 FF 75 0C 8B 4D FC E8 AF 17 F2 FF 85 C0 74 08 8B 45 08 3B 45 F8 73 03 8B 45 F8 8B E5 5D C3` | legacy-od-block | 61 | - |
| `0x004E308D` (va) | `-` | `E8 4E 10 00 00` | legacy-od-block | 5 | - |
| `0x004E30B8` (va) | `-` | `E8 23 10 00 00` | legacy-od-block | 5 | - |
| `0x004E4127` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004E412C` (va) | `-` | `B8` | legacy-od-block | 1 | - |
| `0x004E415F` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004E4164` (va) | `-` | `B9` | legacy-od-block | 1 | - |
| `0x004E418B` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004E4190` (va) | `-` | `BA` | legacy-od-block | 1 | - |
| `0x004E415F` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004E4164` (va) | `-` | `BB` | legacy-od-block | 1 | - |

## 【反击成双】反击时必定触发连击。

ID: `patch.66.legacy-e821f02f5c6f`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0040653C` (va) | `-` | `6A 00 E8 9E CB 0D 00` | legacy-od-block | 7 | - |
| `0x00406555` (va) | `-` | `E8 A6 CA 0D 00` | legacy-od-block | 5 | - |
| `0x0043BE95` (va) | `-` | `E9 8A 72 0A 00 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90` | legacy-od-block | 37 | - |
| `0x004E3000` (va) | `-` | `55 8B EC 6A 01 51 8A 51 10 88 51 01 8B 49 0C 6A 00 6A 01 6A 42 6A 35 E8 BD D1 F2 FF 85 C0 74 15 8B 4D F8 6A 01 E8 B7 00 00 00 7D 09 C6 45 FC 01 E9 97 00 00 00 83 3D 04 2E 49 00 00 76 65 8B 4D F8 6A 01 E8 99 00 00 00 7E 06 C6 45 FC 00 EB 7C 8B 4D F8 8B 49 0C 6A 01 6A 01 6A 7F 68 A0 00 00 00 E8 73 D1 F2 FF 85 C0 74 06 C6 45 FC 01 EB 5C 8B 4D F8 8B 49 0C 6A 01 6A 01 6A 7F 68 A1 00 00 00 E8 53 D1 F2 FF 85 C0 74 25 8B 4D F8 E8 27 2C F2 FF 6A 00 50 E8 0E 57 F4 FF 85 C0 75 2E 88 45 FC EB 29 8B 4D F8 6A 01 E8 34 00 00 00 7E 06 C6 45 FC 00 EB 17 8B 4D F8 E8 FC 2B F2 FF 6A 00 50 E8 E3 56 F4 FF 85 C0 75 03 88 45 FC 8B 55 F8 33 C0 89 82 04 06 00 00 8B 45 FC 8B E5 5D C3 90 90 90 55 8B EC 51 8B 49 0C 6A 00 6A 01 6A 7F 68 A2 00 00 00 E8 E1 D0 F2 FF 85 C0 75 03 33 C0 40 40 83 7D 08 00 75 0B 8B 4D FC 38 81 08 06 00 00 EB 0A 8B 4D FC 48 38 81 08 06 00 00 8B E5 5D C2 04 00 90 90 90 FF 75 10 FF 75 D4 FF 75 FC E8 0A 00 00 00 89 45 FC E9 60 8D F5 FF 90 90 55 8B EC 6A 00 83 7D 10 01 75 10 8B 4D 0C FF 75 0C FF 75 08 E8 5E 00 00 00 EB 54 83 3D 04 2E 49 00 00 76 11 8B 4D 0C FF 75 0C FF 75 08 E8 45 00 00 00 89 45 08 8B 4D 0C E8 AF 00 00 00 85 C0 75 10 8B 4D 08 6B C1 03 C1 E8 02 85 C0 75 01 40 EB 1E 89 45 FC 33 C0 A0 F8 2D 49 00 90 0F AF 45 FC 83 C0 0B FF 75 08 50 E8 31 29 F4 FF 03 45 08 8B E5 5D C2 0C 00 90 90 55 8B EC 6A 00 6A 00 6A 00 6A 01 6A 7F 68 A3 00 00 00 E8 0F D0 F2 FF 85 C0 74 43 89 45 FC 8B 4D 0C E8 27 83 F3 FF 89 45 F8 8B 4D 0C E8 AB 33 F2 FF E8 7A 40 F2 FF 8B C8 2B 45 F8 6B C0 64 33 D2 F7 F9 D1 E8 85 C0 74 11 3B 45 FC 76 03 8B 45 FC 50 FF 75 08 E8 CD 28 F4 FF 03 45 08 EB 0E 8B 4D 08 6B C1 03 C1 E8 02 85 C0 75 01 40 8B E5 5D C2 08 00 90 90 90 55 8B EC 6A 00 6A 01 6A 7F 68 A4 00 00 00 E8 9E CF F2 FF 5D C3` | legacy-od-block | 573 | - |
| `0x004E305B` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004E305D` (va) | `-` | `B4` | legacy-od-block | 1 | - |
| `0x004E307B` (va) | `-` | `6A` | legacy-od-block | 1 | - |
| `0x004E307D` (va) | `-` | `48` | legacy-od-block | 1 | - |
| `0x004E30ED` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004E30EF` (va) | `-` | `B5` | legacy-od-block | 1 | - |
| `0x004E31BF` (va) | `-` | `6A` | legacy-od-block | 1 | - |
| `0x004E31C1` (va) | `-` | `48` | legacy-od-block | 1 | - |
| `0x004E3230` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004E3232` (va) | `-` | `B5` | legacy-od-block | 1 | - |
| `0x004E319E` (va) | `-` | `00` | legacy-od-block | 1 | - |

## 生命越低受到的减伤越高，最大减少75%。

ID: `patch.66.legacy-2be608b1a628`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043BE7C` (va) | `-` | `E9 25 2C 00 00 90` | legacy-od-block | 6 | - |
| `0x0043EAA6` (va) | `-` | `6A 01 FF 75 08 FF 75 FC E8 9B A5 00 00 89 45 FC 83 7D 10 00 0F 85 D5 D3 FF FF E9 BC D3 FF FF` | legacy-od-block | 31 | - |
| `0x0043C2A0` (va) | `-` | `6A 02 FF 75 08 FF 75 FC E8 A1 CD 00 00 89 45 FC` | legacy-od-block | 16 | - |
| `0x0044904E` (va) | `-` | `55 8B EC 8B 4D 0C E8 6D 00 00 00 85 C0 74 58 83 7D 10 01 74 07 B9 01 00 00 00 EB 05 B9 02 00 00 00 3B C8 74 42 50 8B 4D 0C E8 84 24 FD FF 89 45 FC 8B 4D 0C E8 08 D5 FB FF E8 D7 E1 FB FF 8B C8 2B 45 FC 6B C0 50 33 D2 F7 F9 85 C0 74 19 FF 75 08 50 E8 34 CA FD FF 39 45 08 73 0D 33 C0 83 7D 10 01 75 01 40 EB 09 33 C0 8B 4D 08 2B C8 8B C1 8B E5 5D C2 0C 00 90 90 55 8B EC 6A 00 6A 01 68 00 00 00 00 68 B2 00 00 00 E8 FD 70 FC FF 8B E5 5D C3` | legacy-od-block | 146 | - |
| `0x004490CE` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004490D3` (va) | `-` | `B2` | legacy-od-block | 1 | - |

## 1、手动单挑闪退

ID: `patch.66.legacy-ef421f42b61f`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004521A2` (va) | `-` | `74 10 C6 41 F8 FF B8 00 E0 01 00 E8 AD F3 FA FF EB 05 E8 5E F4 FA FF 89 45 F8 E8 B4 9E FD FF 02 55 08 02 45 0C 8A F0 52 E8 BA 15 FB FF 89 45 F4 69 C0 00 1B 00 00 01 45 F8 E8 93 F3 FA FF 03 45 F4 89 45 F0 E8 7E F4 FA FF 03 45 F4 8D 90 80 0C 00 00 89 55 D4 8D 90 C0 12 00 00 89 55 D8 8D 90 40 1F 00 00 89 55 DC B9 08 3D 4B 00 8A 41 05 83 E0 01 89 45 D0 8A 45 08 6B D0 30 89 55 EC 8A 45 10 6B C8 30 03 CA 89 4D E4 8A 45 0C 6B D0 30 89 55 E8 8A 45 14 6B C8 30 03 CA 89 4D E0 8B 4D FC 8D 45 08 E8 D1 2E FB FF E8 8C C3 FC FF` | legacy-od-block | 173 | - |
| `0x0042D20F` (va) | `-` | `38 15 D0 5E 50 00` | legacy-od-block | 6 | - |
| `0x00419CB7` (va) | `-` | `68 B1 B1 48 00 68 38 2F 49 00 E8 DA 5D FF FF 83 C4 0C FF 75 E4 68 A5 B1 48 00` | legacy-od-block | 26 | - |
| `0x0043A48A` (va) | `-` | `6A 0B E8 26 2C 03 00 6A 00 6A 00 FF 75 0C 8B 45 08 E8 26 DD 03 00 89 55 F0 8D 4D F8 8B 10 89 11 8B 45 0C 83 C0 07 6B C0 09 05 00 E0 4C 00 50 FF 75 F0 8D 4D F8 51 FF 75 0C FF 75 08 E8 C7 F6 FD FF 90 90` | legacy-od-block | 67 | - |
| `0x0043B75E` (va) | `-` | `3C 21 75 19 8B 4D D8 90 90 90 90 90 90 90 90 90 90 81 39 D2 00 00 00 73 04` | legacy-od-block | 25 | - |

## 无视【减少策略伤害X%】的效果

ID: `patch.66.legacy-f1d4cba29fdb`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C22A` (va) | `-` | `90 90 90 90 90 90 90 90 90 90 90 90` | legacy-od-block | 12 | - |
| `0x0043C242` (va) | `-` | `8B 4D F0 E8 73 9B FC FF 85 C0 0F 84 90 0E 00 00 EB 18` | legacy-od-block | 18 | - |
| `0x0043C266` (va) | `-` | `0F 84 76 0E 00 00 E9 65 0E 00 00 90 90 90` | legacy-od-block | 14 | - |
| `0x0043D0D6` (va) | `-` | `50 FF 75 FC E8 FA 89 FE FF 01 45 FC 6A 01 6A 01 6A 00 68 EF 00 00 00 8B 4D F0 E8 E4 30 FD FF 85 C0 0F 84 74 F1 FF FF E9 9E F1 FF FF` | legacy-od-block | 44 | - |
| `0x0043D0E7` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0043D0E9` (va) | `-` | `EF` | legacy-od-block | 1 | - |

## 策伤保底，造成策略的伤害不小于N，设置N=16-30时为百分比，其他数值为固定值，如果本次伤害本就大于保底数值，则会增伤20%

ID: `patch.66.legacy-56d5012ecd95`；类型: `legacy-injection`；画像: `profile.ccz66x.legacy-patch-family`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C2D5` (va) | `-` | `E9 4E 02 00 00 90 90 90` | legacy-od-block | 8 | - |
| `0x0043C528` (va) | `-` | `E8 4B 67 FD FF 89 45 FC FF 75 0C FF 75 08 FF 75 F0 FF 75 FC E8 6D 0E 00 00 89 45 FC E9 91 FD FF FF` | legacy-od-block | 33 | - |
| `0x0043D3AE` (va) | `-` | `55 8B EC 6A 00 6A 01 6A 2F 68 D4 00 00 00 8B 4D 0C E8 15 2E FD FF 85 C0 74 30 50 83 F8 10 72 16 83 F8 1F 73 11 8B 4D 14 E8 88 9E FC FF FF 75 FC 50 E8 F5 86 FE FF 39 45 08 72 12 6A 14 FF 75 08 E8 E6 86 FE FF 01 45 08 EB 06 8B 45 08 89 45 08 6A 00 6A 01 6A 00 68 D5 00 00 00 8B 4D 10 E8 C8 2D FD FF 85 C0 74 31 50 89 45 FC 83 F8 10 72 16 83 F8 1F 73 11 8B 4D 14 E8 38 9E FC FF FF 75 FC 50 E8 A5 86 FE FF 39 45 08 73 10 6A 14 FF 75 08 E8 96 86 FE FF 29 45 08 8B 45 08 8B E5 5D C2 10 00` | legacy-od-block | 161 | - |
| `0x0043D3B6` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0043D3B8` (va) | `-` | `FF` | legacy-od-block | 1 | - |
| `0x0043D403` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0043D405` (va) | `-` | `FF` | legacy-od-block | 1 | - |

## 6.6 装备页一行显示 7 个属性（call 重定向到 helper）

ID: `patch.66.equip-ability-row`；类型: `instruction-replacement`；画像: `profile.ccz66.shanzai.work.1b25`；状态: `candidate`；证据: `sample-verified`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00476FB6` (va) | `E8 0D B0 FE FF` | `E8 AD B5 05 00` | whole-instruction | 5 | True |

执行流：5 字节整条 call 替换为 5 字节 call，不改指令边界；原目标 0x00461FC8 是 ret 0x10 形态（0x00462048 现读 `C2 10 00 90`），helper 必须保持同一契约。


## 原生 Z 加速函数定位器

ID: `locator.66.xiaoan.native-super`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `source-reviewed`

签名: `55 8B EC B9 ?? ?? ?? ?? B8 ?? ?? ?? ?? 80 38 00 0F 85 ?? ?? ?? ?? C6 00 01 80 31 01 80 39 01 75 44`

扫描范围: PE32 executable sections of the loaded image

命中规则: exactly one match

- 提取：`nativeSuper=match`
- 提取：`nativeSuperState=absolute operand at match+4 length1`
- 提取：`nativeSuperBusy=absolute operand at match+9 length1`

## 公共等待包装器定位器

ID: `locator.66.xiaoan.wait-wrapper`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `source-reviewed`

签名: `55 8B EC E8 ?? ?? ?? ?? 85 C0 75|EB 07 E8 ?? ?? ?? ?? EB F0 5D C3`

扫描范围: PE32 executable sections of the loaded image

命中规则: exactly one match; accept 0x75 or 0xEB at match+10

- 提取：`wait=match`
- 提取：`waitCall=match+3`
- 提取：`waitBranch=match+10`
- 提取：`nativeStage=CALL target at match+3`
- 提取：`pump=CALL target at match+12`

## 原生阶段函数定位器

ID: `locator.66.xiaoan.native-stage`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `source-reviewed`

签名: `55 8B EC 0F B7 05 ?? ?? ?? ?? 0F B6 C8 85 C9 75 04 8B C1 EB 04 C1 E8 08 40`

扫描范围: 128 bytes from the nativeStage CALL target in PE32 executable sections

命中规则: function prologue must start exactly at the resolved nativeStage target

- 提取：`match must equal nativeStage CALL target`
- 提取：`speed=absolute operand at match+6 length2`
- 提取：`phase/phaseTable/phaseCounter from nested phase block`
- 提取：`sleep/deadline from two pacing CALL rel32 targets`

## 通用延迟函数定位器

ID: `locator.66.xiaoan.delay`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `source-reviewed`

签名: `55 8B EC FF 75 08 E8 ?? ?? ?? ?? E8 ?? ?? ?? ?? F7 D8 1B C0 40 85 C0 75 07 E8 ?? ?? ?? ?? EB EB 5D C2 04 00`

扫描范围: PE32 executable sections of the loaded image

命中规则: exactly one match and both CALL targets must equal the resolved deadline and pump functions

- 提取：`delay=match`
- 提取：`CALL at +11 must target deadline`
- 提取：`CALL at +25 must target pump`

## 对白函数立即返回

ID: `patch.66.xiaoan.dialog`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042D5B0` (va) | `55 8B EC E8` | `C2 0C 00 E8` | function-entry-prefix | 4 | False |

执行流：RET 0x000C 在入口立即返回；第 4 字节只是不可达填充，不能作为完整指令执行。


## 地图文字函数立即返回

ID: `patch.66.xiaoan.map-text`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004332A6` (va) | `55 8B EC 6A` | `C2 10 00 6A` | function-entry-prefix | 4 | False |

执行流：RET 0x0010 在入口立即返回；第 4 字节只是不可达填充。


## 通用延迟函数立即返回

ID: `patch.66.xiaoan.delay`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00422DBA` (va) | `55 8B EC` | `C2 04 00` | function-entry | 3 | True |

执行流：以 RET 0x0004 替换完整三字节函数序言，立即返回并弹出一个参数。


## R 流程等待 CALL 空操作化

ID: `patch.66.xiaoan.r-wait`；类型: `instruction-replacement`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00429964` (va) | `E8 7C 2B 00 00` | `90 90 90 90 90` | whole-instruction | 5 | True |

执行流：删除到公共等待包装器 0x0042C4E5 的 CALL；原 CALL 下一地址为 0x00429969。


## 公共等待中的 nativeStage CALL 重定向

ID: `patch.66.xiaoan.wait-call`；类型: `call-retarget`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042C4E8` (va) | `E8 F3 8B 04 00` | `E8 ?? ?? ?? ??` | whole-instruction-rel32 | 5 | True |

执行流：超级 S 时 CALL 到 SuperYieldBridge；阶段加速时 CALL 到 LegacyPhaseBridge；两者互斥。


ABI: 被调函数为 __cdecl、无显式参数、EAX 返回 int；CALL 后继续执行 0x0042C4ED。

桩入口: `SuperYieldBridge or LegacyPhaseBridge through a near thunk`

返回: `0x0042C4ED`

重定位: `rel32 = thunk - (0x0042C4E8 + 5)`；`near thunk encodes mov eax, absolute32; jmp eax`

## 加速修饰键立即数字段

ID: `patch.66.xiaoan.input-modifier`；类型: `operand-patch`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00413324` (va) | `10` | `10 (VK_SHIFT); 11 (VK_CONTROL)` | immediate-operand-only | 1 | False |

执行流：修改 CMP EAX, imm8 的立即数；完整上下文从 0x00413322 起为 83 F8 <key> 75 0F。


## 第三类对白函数立即返回

ID: `patch.66.xiaoan.dialog3`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042DB2C` (va) | `55 8B EC 6A` | `C2 04 00 6A` | function-entry-prefix | 4 | False |

执行流：RET 0x0004 在入口立即返回；第 4 字节只是不可达填充。


## 额外延迟分支跳过

ID: `patch.66.xiaoan.extra-delay`；类型: `instruction-replacement`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00415B40` (va) | `D1 E0` | `EB 06` | whole-instruction | 2 | True |

执行流：把 SHL EAX,1 改为 JMP short +6，跳过后续延迟调用准备。


## 原生超级加速等待分支

ID: `patch.66.xiaoan.wait-branch`；类型: `instruction-replacement`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042C4EF` (va) | `75 07` | `EB 07` | whole-instruction | 2 | True |

执行流：原生 Z 超级加速把 JNZ +7 改为 JMP +7；小暗接管前会识别并还原这一原生状态。


## 对白显示延迟调用跳过

ID: `patch.66.xiaoan.dialog-display`；类型: `control-transfer-prefix`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042C812` (va) | `E8 29` | `EB 1D` | instruction-prefix-terminal-transfer | 2 | False |

执行流：用 JMP short +0x1D 覆盖 CALL 的前两字节；跳转使剩余三个 rel32 字节不可达。


## 扩展显示延迟调用跳过

ID: `patch.66.xiaoan.extended-display`；类型: `control-transfer-prefix`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00455CE5` (va) | `E8 56` | `EB F5` | instruction-prefix-terminal-transfer | 2 | False |

执行流：用 JMP short -11 覆盖 CALL 的前两字节；跳转使剩余三个 rel32 字节不可达。


## 原生 Z 切换函数入口重定向

ID: `patch.66.xiaoan.native-super`；类型: `entry-jump`；画像: `profile.ccz66.xiaoan.fixture.25d`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004250E6` (va) | `55 8B EC B9 DB` | `E9 ?? ?? ?? ??` | function-entry-terminal-transfer | 5 | False |

执行流：JMP rel32 到 NativeToggleBridge；原序言和 MOV ECX,imm32 的首两字节被覆盖，原函数不再顺序执行。


ABI: NativeToggleBridge 为 __cdecl、无参数、void；保留原调用者的栈布局。

桩入口: `NativeToggleBridge through a near thunk`

返回: `bridge RET returns directly to the original caller`

重定位: `rel32 = thunk - (0x004250E6 + 5)`；`near thunk encodes mov eax, absolute32; jmp eax`
