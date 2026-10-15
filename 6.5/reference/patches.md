# 6.5 Hook、补丁与定位器

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/patches/hook-recipes.json`、`6.5/data/patches/legacy-effect-injections.json`

## 攻击范围分派 Hook

ID: `patch.65.attack-dispatch-hook`；类型: `hook`；画像: `profile.ccz65.unencrypted.f9a`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00436511` (va) | `55 8B EC 51 33 C0` | `-` | - | 6 | True |

ABI: ECX=runtime-unit; [EBP+08]=center; [EBP+0C..0F]=packed range bytes; callee ret 0x10

桩入口: `custom attack range dispatcher`

返回: `preserve original caller contract`

重定位: `range pointer table or replacement table`

## 攻击选择器 CALL Hook

ID: `patch.65.attack-selector-call-hook`；类型: `call-retarget`；画像: `profile.ccz65.unencrypted.f9a`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004553F8` (va) | `E8 14 11 FE FF` | `-` | - | 5 | True |

ABI: 保持中心坐标、packed range descriptor、mode bit 和调用者栈布局

桩入口: `replacement selector callee`

返回: `0x004553FD`

重定位: `rel32 target`

## 穿透扩展 Hook

ID: `patch.65.pierce-expand-hook`；类型: `hook`；画像: `profile.ccz65.unencrypted.f9a`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004364C7` (va) | `55 8B EC 51 51` | `-` | - | 5 | True |

ABI: ECX=tactical-unit; 参数含 target battle id、pierce byte、output buffer、filter/fallback

桩入口: `custom pierce expander`

返回: `preserve wrapper return contract`

重定位: 无

## 穿透几何分派 Hook

ID: `patch.65.pierce-dispatch-hook`；类型: `hook`；画像: `profile.ccz65.unencrypted.f9a`；状态: `canonical`；证据: `sample-verified`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00435CE9` (va) | `55 8B EC 51 33 C0 50` | `-` | - | 7 | True |

ABI: center coordinate; pierce/effect code; output buffer; filter/fallback

桩入口: `custom geometry dispatcher`

返回: `preserve original callee contract`

重定位: 无

## 信息传送29 根据大兵种号指定S

ID: `patch.65.legacy-edd0a288a663`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0047D953` (va) | `-` | `CF 94 42 00` | legacy-od-block | 4 | - |
| `0x004294CF` (va) | `-` | `55 8B EC FF 75 08 E8 8A D9 FF FF 3D 00 04 00 00 73 4C 42 01 55 08 50 50 E8 F8 CC FD FF E8 1B 2A FE FF 50 FF 75 08 E8 6A D9 FF FF 42 01 55 08 50 FF 75 08 E8 5D D9 FF FF 85 D2 74 22 42 01 55 08 83 F8 28 73 EB 39 45 F8 75 E6 8B 55 FC 8B 45 F4 D1 E2 66 89 82 00 10 50 00 E8 23 55 FE FF 8B E5 5D C2 04 00` | legacy-od-block | 100 | - |

## 【噬心毒咒 v3】策略攻击伤害结算后，遍历所有受击目标，概率使其陷入随机异常状态（中毒/麻痹/禁咒/混乱），概率由特效值%控制

ID: `patch.65.legacy-e899f90fd0b2`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004259AF` (va) | `-` | `E9 73 4C FF FF` | legacy-od-block | 5 | - |
| `0x0041A627` (va) | `-` | `8B 4D FC 90 90 90 90 90 90 90 90 90 90 90 90 90 0F B6 49 01 E8 B9 BB FE FF 6A 00 6A 01 6A 00 68 C0 00 00 00 E8 89 5B FF FF 85 C0 0F 84 77 00 00 00 57 89 C7 C7 45 F8 00 00 00 00 8B 4D FC 8B 45 F8 0F B6 54 01 0D 80 FA FF 74 5C 83 BC 81 08 01 00 00 01 7C 49 6A 64 E8 90 54 06 00 39 F8 73 3E 8B 4D FC 8B 45 F8 0F B6 4C 01 0D E8 62 BB FE FF 6A 04 E8 75 54 06 00 8A 51 1E 83 F8 00 74 19 83 F8 01 74 0A 83 F8 02 74 0A 80 CA 03 EB 0D 80 CA C0 EB 08 80 CA 30 EB 03 80 CA 0C 88 51 1E FF 45 F8 83 7D F8 73 7C 94 5F 8B 4D FC E8 57 88 00 00 E9 D8 B2 00 00` | legacy-od-block | 181 | - |
| `0x0041A645` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041A647` (va) | `-` | `C0` | legacy-od-block | 1 | - |

## 【回mp攻击】:物理攻击后获得当前伤害乘特效值的mp。

ID: `patch.65.legacy-d602c42968b0`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00418335` (va) | `-` | `E9 C2 A5 03 00` | legacy-od-block | 5 | - |
| `0x004528FC` (va) | `-` | `8B 4D AC 6A 00 6A 01 6A 00 68 AD 00 00 00 E8 CA D8 FB FF 85 C0 74 67 8B 4D 08 36 8B 89 84 00 00 00 83 F9 00 74 58 50 51 E8 B0 31 FD FF 8B 4D A4 E8 5E 3C FB FF 0F B7 49 1F 8B 55 A4 36 8B 52 14 2B CA 3B C1 7F 02 EB 02 8B C1 8B D0 6B D2 02 8B C8 2B CA 8B 55 08 50 6A 00 6A 00 6A 00 6A 00 51 6A 00 FF 32 FF 32 B9 00 01 00 00 E8 1A E0 FF FF 8B 95 34 FF FF FF 8B 45 D4 36 01 42 14 59 8B 45 F4 85 C0 E9 B6 59 FC FF` | legacy-od-block | 136 | - |
| `0x00452904` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00452906` (va) | `-` | `AD` | legacy-od-block | 1 | - |

## 【回mp攻击】:物理攻击后获得当前伤害乘特效值的mp。

ID: `patch.65.legacy-54b2fc7fb712`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00418335` (va) | `-` | `E9 C2 A5 03 00 90 90` | legacy-od-block | 7 | - |
| `0x004528FC` (va) | `-` | `8B 4D AC 6A 00 6A 01 6A 00 68 AD 00 00 00 E8 CA D8 FB FF 85 C0 74 67 8B 4D 08 36 8B 89 84 00 00 00 83 F9 00 74 58 50 51 E8 B0 31 FD FF 8B 4D A4 E8 5E 3C FB FF EB 57 90 90 90 90 90 90 90 90 90 2B CA 3B C1 7F 02 EB 02 8B C1 8B D0 6B D2 02 8B C8 2B CA 8B 55 08 50 6A 00 6A 00 6A 00 6A 00 51 6A 00 FF 32 FF 32 B9 00 01 00 00 E8 1A E0 FF FF 8B 95 34 FF FF FF 8B 45 D4 36 01 42 14 59 8B 45 F4 85 C0 0F 84 CC 59 FC FF E9 B0 59 FC FF 50 E8 FF 48 FB FF 51 33 D2 8B 4D 08 8A 11 8B CA E8 5A 38 FB FF 36 8B 51 14 59 58 EB 8C` | legacy-od-block | 171 | - |
| `0x00452904` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00452906` (va) | `-` | `AD` | legacy-od-block | 1 | - |

## 【多多益善】：周围友军每多一名则加一格攻击范围（当到这一类攻击范围极限则不再增加），可与远距攻击叠加并且发动时无视四象征罗

ID: `patch.65.legacy-9f850eaa8be9`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043F936` (va) | `-` | `E9 E1 23 00 00` | legacy-od-block | 5 | - |
| `0x00441D1C` (va) | `-` | `8B 4D FC 50 6A 01 6A 01 6A 00 68 B3 00 00 00 E8 A9 E4 FC FF 85 C0 0F 84 30 01 00 00 6A 02 8B 4D FC E8 CE 49 FC FF 3C 01 75 04 6A 04 EB 02 6A 05 8B 4D FC E8 F6 9E FD FF 83 F8 01 0F 84 0B 01 00 00 50 8B 45 F0 83 F8 00 75 0A B8 01 00 00 00 E9 E7 00 00 00 83 F8 01 75 0A B8 06 00 00 00 E9 D8 00 00 00 83 F8 02 75 0A B8 03 00 00 00 E9 C9 00 00 00 83 F8 03 75 0A B8 04 00 00 00 E9 BA 00 00 00 83 F8 05 75 0A B8 13 00 00 00 E9 AB 00 00 00 83 F8 06 75 0A B8 0C 00 00 00 E9 9C 00 00 00 83 F8 07 75 0A B8 08 00 00 00 E9 8D 00 00 00 83 F8 09 75 0A B8 1F 00 00 00 E9 7E 00 00 00 83 F8 0C 75 0A B8 0D 00 00 00 EB 72 90 90 90 83 F8 0E 75 0A B8 0F 00 00 00 EB 63 90 90 90 83 F8 10 75 07 B8 11 00 00 00 EB 54 83 F8 11 75 07 B8 12 00 00 00 EB 48 83 F8 15 75 07 B8 16 00 00 00 EB 3C 83 F8 17 75 07 B8 18 00 00 00 EB 30 83 F8 19 75 07 B8 1A 00 00 00 EB 24 83 F8 1B 75 07 B8 1C 00 00 00 EB 18 83 F8 1C 75 07 B8 1D 00 00 00 EB 0C 83 F8 1E 75 07 B8 1F 00 00 00 EB 00 8B 4D EC 3B 4D E8 7D 0C 83 45 EC 01 E9 F9 FE FF FF 8B 45 F0 88 45 F8 58 6A 04 E9 C5 DA FF FF` | legacy-od-block | 346 | - |
| `0x00441D25` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00441D27` (va) | `-` | `B3` | legacy-od-block | 1 | - |

## 【大杀四方】：击杀敌人后可再次行动（物理/策略均有效），每回合限触发N次（N为特效值），不可叠加

ID: `patch.65.legacy-b538d55769eb`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004037FF` (va) | `-` | `E8 1C FD 0C 00` | legacy-od-block | 5 | - |
| `0x00420F97` (va) | `-` | `E8 84 26 0B 00` | legacy-od-block | 5 | - |
| `0x0044AF8F` (va) | `-` | `E9 6C 86 08 00` | legacy-od-block | 5 | - |
| `0x00412D79` (va) | `-` | `90 90` | legacy-od-block | 2 | - |
| `0x00412D7B` (va) | `-` | `E9 D0 07 0C 00` | legacy-od-block | 5 | - |
| `0x004D3500` (va) | `-` | `6A 00 6A 01 68 00 00 00 00 68 C1 00 00 00 E8 C6 CC F3 FF C3` | legacy-od-block | 20 | - |
| `0x004D3520` (va) | `-` | `55 8B EC 51 8B F8 E8 90 FF FF FF 8B 4D FC 8B 49 0C 8B F9 E8 C8 FF FF FF 85 C0 74 10 0F B6 D0 8A 47 24 24 7F 3A C2 73 04 80 4F 24 80 59 C9 C3` | legacy-od-block | 47 | - |
| `0x004D3620` (va) | `-` | `55 89 E5 51 89 C7 E8 90 FE FF FF 8B 4D FC 8B 49 08 89 CF E8 C8 FE FF FF 85 C0 74 10 0F B6 D0 8A 47 24 24 7F 38 D0 73 04 80 4F 24 80 59 C9 C3` | legacy-od-block | 47 | - |
| `0x004D3590` (va) | `-` | `55 8B EC 51 0F B6 4D 08 E8 5C 2C F3 FF F6 41 24 80 74 2B 80 61 24 7F 8A 41 0C 3C 02 75 20 FE 41 24 6A 06 E8 D8 30 F3 FF 68 88 00 00 00 6A 06 FF 71 04 E8 E3 B0 F6 FF 83 C4 0C B0 01 EB 02 32 C0 59 8B E5 5D C2 04 00` | legacy-od-block | 71 | - |
| `0x004D3600` (va) | `-` | `C6 41 24 00 0F B6 45 DC C6 80 00 8B 50 00 00 E9 83 79 F7 FF` | legacy-od-block | 20 | - |
| `0x004D3550` (va) | `-` | `0F B6 55 08 80 BA 00 8B 50 00 00 75 0E E8 13 DC F4 FF 85 C0 74 05 E9 1E F8 F3 FF FF 75 08 E8 1D 00 00 00 84 C0 74 0A B8 01 00 00 00 E9 2F F8 F3 FF 33 C0 E9 28 F8 F3 FF` | legacy-od-block | 56 | - |
| `0x004D350A` (va) | `-` | `C1` | legacy-od-block | 1 | - |
| `0x004D3505` (va) | `-` | `00` | legacy-od-block | 1 | - |

## 九宫范围内的友军被攻击时，目标强制转为自己，目标被围攻时无效。（和先手触发的时机相同，例如，奋战或[连击]不会触发先手，这个也无法触发）

ID: `patch.65.legacy-77c10654d72c`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004105C8` (va) | `-` | `E8 CB A4 00 00 90 85 C0 74 02 87 D1 52 51` | legacy-od-block | 14 | - |
| `0x0043ACA2` (va) | `-` | `E8 F1 FD FD FF 90 90 90 90` | legacy-od-block | 9 | - |
| `0x0043DB3E` (va) | `-` | `E8 55 CF FD FF 90 90 90 90 90 90 90 90 85 C0 74 02 87 CA` | legacy-od-block | 19 | - |
| `0x00410F23` (va) | `-` | `E8 94 9B 00 00` | legacy-od-block | 5 | - |
| `0x0041AA98` (va) | `-` | `8B 54 24 FC 8B 4C 24 F0 8B 49 04 C3 55 8B EC 6A 01 6A 01 68 00 00 00 00 68 D1 00 00 00 E8 1F 57 FF FF 5D C3 55 8B EC 6A 00 51 E8 32 B7 FE FF 51 33 C0 50 50 B8 11 7C 41 00 39 45 10 74 7F E8 C9 FF FF FF 85 C0 75 76 6A 00 6A 01 6A 01 6A 02 8B 4D F4 E8 05 E7 FE FF 8B 45 FC 8A 88 48 C7 4A 00 80 F9 FF 74 58 3A 4D F8 74 4E E8 F2 B6 FE FF 89 4D EC 6A 08 E8 D7 94 00 00 85 C0 75 3B 8B 4D EC E8 87 FF FF FF 85 C0 74 2F 3C 01 74 1A 8B 4D 18 E8 93 4D 02 00 8B 4D EC FF 71 04 FF 75 18 E8 F5 7F FF FF 85 C0 74 11 8B 4D EC 8B 41 10 3B 45 F0 76 06 89 45 F0 89 4D F4 FF 45 FC EB 9A 8B 4D F4 8B 45 18 89 45 08 83 7D F0 00 74 37 8A 41 04 88 45 14 FF 75 08 51 E8 36 78 00 00 C6 05 FC 5E 50 00 01 8B 4D F4 0F B6 41 04 50 68 E0 AF 41 00 E8 D1 EA 03 00 8B 4D F4 51 FF 75 08 E8 11 78 00 00 8B 4D F4 8B E5 5D C3` | legacy-od-block | 263 | - |
| `0x0041AFE0` (va) | `-` | `D0 DD C9 CB CE E1 D6 F7 A3 A1 00` | legacy-od-block | 11 | - |
| `0x0041AAAC` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041AAB1` (va) | `-` | `D1` | legacy-od-block | 1 | - |
| `0x0041AAE4` (va) | `-` | `01` | legacy-od-block | 1 | - |
| `0x0041AB79` (va) | `-` | `01` | legacy-od-block | 1 | - |

## 【敌潮逆噬】：拥有特效者周围敌军全能力下降周围敌军人数*K%，K为特效值

ID: `patch.65.legacy-397b2cfb9705`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043CB4C` (va) | `-` | `E9 B6 07 00 00` | legacy-od-block | 5 | - |
| `0x0043D307` (va) | `-` | `6A 00 6A 01 6A 00 68 B4 00 00 00 E8 C2 2E FD FF 84 C0 0F 84 87 00 00 00 8B 4D F0 8A 51 06 8B 4D FC 38 51 06 76 0B 8A 51 06 8B 4D F0 2A 51 06 EB 03 2A 51 06 80 FA 01 77 66 8B 4D F0 8A 51 07 8B 4D FC 38 51 07 76 0B 8A 51 07 8B 4D F0 2A 51 07 EB 03 2A 51 07 80 FA 01 77 45 8B 4D FC 80 79 05 02 74 0B 8B 4D F0 80 79 05 02 75 33 EB 09 8B 4D F0 80 79 05 02 74 28 8B 4D FC 50 E8 89 93 FC FF 3C 01 75 04 6A 05 EB 02 6A 04 8B 4D FC E8 B1 E8 FD FF 8B 8D 4C F9 FF FF 0F AF C1 29 45 F8 58 8B 4D FC E9 A3 F7 FF FF` | legacy-od-block | 167 | - |
| `0x0043D30C` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0043D30E` (va) | `-` | `B4` | legacy-od-block | 1 | - |

## 【殭屍大法】：拥有mp防御时生效，当将损失mp大于当前hp时，按当前hp扣mp

ID: `patch.65.legacy-3358d026a5fa`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00406006` (va) | `-` | `E9 F5 4A 01 00 90` | legacy-od-block | 6 | - |
| `0x0041AB00` (va) | `-` | `8B 4D E0 6A 01 6A 01 6A 00 68 B2 00 00 00 E8 C6 56 FF FF 85 C0 74 0E 8B 4D E0 8B 49 10 39 4D DC 72 03 89 4D DC 8B 4D DC 8B 55 FC E9 DB B4 FE FF` | legacy-od-block | 48 | - |
| `0x0041AB08` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041AB0A` (va) | `-` | `B2` | legacy-od-block | 1 | - |

## 【盛气凌人】：暴击时使攻击目标全部6项属性各降1档，个人号BF，装备号00（无法通过装备获取）

ID: `patch.65.legacy-d7dfa1a7f16d`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00472D92` (va) | `-` | `E9 10 FC FD FF 90` | legacy-od-block | 6 | - |
| `0x004529A7` (va) | `-` | `B8 F0 27 49 00 83 B8 04 06 00 00 00 74 34 8B 4D F8 6A 01 6A 01 6A 00 68 BF 00 00 00 E8 11 D8 FB FF 85 C0 74 1D C7 45 FC 00 00 00 00 6A 00 FF 75 FC 8B 4D 0C E8 41 6E FB FF FF 45 FC 83 7D FC 06 7C EA 89 EC 5D C2 08 00` | legacy-od-block | 72 | - |
| `0x004529BD` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x004529BF` (va) | `-` | `BF` | legacy-od-block | 1 | - |

## 【策略偷钱】我军或友军策略攻击我军可以获得等同策略伤害的金钱，敌军策略攻击我军会减少等同策略伤害的金钱

ID: `patch.65.legacy-518736e260ba`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004259B4` (va) | `-` | `E9 EE 4B FF FF 90 90 90 90` | legacy-od-block | 9 | - |
| `0x0041A5A7` (va) | `-` | `8B 4D FC 83 B9 08 01 00 00 01 7C 66 0F B6 49 01 E8 3D BC FE FF 6A 01 6A 01 6A 00 68 AA 00 00 00 E8 0D 5C FF FF 85 C0 74 49 3E 8B 4D FC 0F B6 49 0D E8 1C BC FE FF 3E 8B 45 FC 8B 80 08 01 00 00 6B C0 01 BA 7C 07 4B 00 80 79 05 02 72 18 8B 0A 03 C8 81 F9 3F 42 0F 00 73 04 01 02 EB 14 C7 02 3F 42 0F 00 EB 0C 39 02 76 04 29 02 EB 04 33 C0 89 02 8B 4D FC 8B 81 50 05 00 00 E9 92 B3 00 00` | legacy-od-block | 128 | - |
| `0x0041A5C1` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041A5C3` (va) | `-` | `AA` | legacy-od-block | 1 | - |

## 【策略冲锋】：策略伤害增加策略攻击前移动步数*K*1%，K为特效值

ID: `patch.65.legacy-fc944ad335d5`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C2B0` (va) | `-` | `E9 B5 9C 00 00` | legacy-od-block | 5 | - |
| `0x00445F6A` (va) | `-` | `3E 8B 4D F0 6A 00 6A 01 6A 00 68 B0 00 00 00 E8 5B A2 FC FF 85 C0 74 1A 0F B6 0D 48 0C 50 00 85 C9 74 0F 0F AF C1 FF 75 FC 50 E8 40 FB FD FF 01 45 FC E9 14 63 FF FF` | legacy-od-block | 55 | - |
| `0x00445F73` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00445F75` (va) | `-` | `B0` | legacy-od-block | 1 | - |

## 【聚势伐谋】：策略伤害增加（被策略攻击者周围同阵营人数+1（被策略攻击者））*K%，K为特效值

ID: `patch.65.legacy-d485271ee4a7`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C2B5` (va) | `-` | `E9 B2 9E 00 00` | legacy-od-block | 5 | - |
| `0x0044616C` (va) | `-` | `3E 8B 4D F0 6A 00 6A 01 6A 00 68 B1 00 00 00 E8 59 A0 FC FF 85 C0 74 2E 50 8B 4D 08 E8 83 05 FC FF 3C 01 75 04 6A 04 EB 02 6A 05 8B 4D 08 E8 AB 5A FD FF 8B 4D DC 0F AF C1 FF 75 FC 50 E8 2B F9 FD FF 01 45 FC 58 E9 03 61 FF FF` | legacy-od-block | 75 | - |
| `0x00446175` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x00446177` (va) | `-` | `B1` | legacy-od-block | 1 | - |

## 宝物-个人

ID: `patch.65.legacy-8eeb3c8fcd2c`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00407831` (va) | `-` | `90 90 90 90 90 90 90 90 90 B8 9A 0E 50 00 80 38 02 75 11 8A 48 01 E8 CC 70 01 00 E8 D6 D5 07 00 84 C0 75 28 6A 05 6A 00 6A 33 8B 4D FC E8 B0 53 00 00 85 C0 75 0E 8B 4D FC E8 A1 ED FF FF 8A 80 81 78 40 00 8B 4D FC E8 D2 31 01 00` | legacy-od-block | 76 | - |
| `0x0041AA4F` (va) | `-` | `55 8B EC 50 33 C0 38 05 DC 5F 50 00 75 20 6A 00 6A 03 6A 00 68 DD 00 00 00 E8 22 A7 00 00 8B 4D FC 85 C0 74 08 8A 81 81 AA 41 00 EB 01 91 8B E5 5D C3 04 02 03 08 07 0B 06 05 06 01 0A 0B` | legacy-od-block | 62 | - |
| `0x0041AA62` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0041AA64` (va) | `-` | `DD` | legacy-od-block | 1 | - |

## 整形变量4003=X，则攻击造成的最小伤害=攻击力*X%，会吃增伤特技和暴击的加成，对敌我双方皆有效。

ID: `patch.65.legacy-094abf000c04`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043BD58` (va) | `-` | `E9 A5 13 00 00 90 90 90 90 90 90 90 90 90 90 90` | legacy-od-block | 16 | - |
| `0x0043D102` (va) | `-` | `E8 97 29 04 00 83 C4 08 85 C0 75 01 40 89 45 FC FF 75 E0 FF 75 FC E8 08 00 00 00 89 45 FC E9 43 EC FF FF 55 8B EC 8B 45 0C 0F B6 0D 8C 5E 50 00 85 C9 74 12 0F AF C8 8B C1 B9 64 00 00 00 99 F7 F9 3B 45 08 7D 03 8B 45 08 5D C2 08 00` | legacy-od-block | 77 | - |

## 无视【减少策略伤害X%】的效果

ID: `patch.65.legacy-b9b3f5706176`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C242` (va) | `-` | `8B 4D F0 E8 73 9B FC FF 85 C0 0F 84 90 0E 00 00 EB 18` | legacy-od-block | 18 | - |
| `0x0043C266` (va) | `-` | `0F 84 76 0E 00 00 E9 65 0E 00 00 90 90 90` | legacy-od-block | 14 | - |
| `0x0043D0D6` (va) | `-` | `50 FF 75 FC E8 FA 89 FE FF 01 45 FC 6A 01 6A 01 6A 00 68 EF 00 00 00 8B 4D F0 E8 E4 30 FD FF 85 C0 0F 84 74 F1 FF FF E9 9E F1 FF FF` | legacy-od-block | 44 | - |
| `0x0043D0E7` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0043D0E9` (va) | `-` | `EF` | legacy-od-block | 1 | - |

## 策伤保底，造成策略的伤害不小于N，设置N=16-30时为百分比，其他数值为固定值，如果本次伤害本就大于保底数值，则会增伤20%

ID: `patch.65.legacy-f0258ed93731`；类型: `legacy-injection`；画像: `profile.ccz65.unencrypted.f9a`；状态: `candidate`；证据: `legacy-patch-bytes`

> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0043C2D5` (va) | `-` | `E9 4E 02 00 00 90 90 90` | legacy-od-block | 8 | - |
| `0x0043C528` (va) | `-` | `E8 7D 67 FD FF 89 45 FC FF 75 0C FF 75 08 FF 75 F0 FF 75 FC E8 6D 0E 00 00 89 45 FC E9 91 FD FF FF` | legacy-od-block | 33 | - |
| `0x0043D3AE` (va) | `-` | `55 8B EC 6A 00 6A 01 6A 2F 68 D4 00 00 00 8B 4D 0C E8 15 2E FD FF 85 C0 74 30 50 83 F8 10 72 16 83 F8 1F 73 11 8B 4D 14 E8 88 9E FC FF FF 75 FC 50 E8 F5 86 FE FF 39 45 08 72 12 6A 14 FF 75 08 E8 E6 86 FE FF 01 45 08 EB 06 8B 45 08 89 45 08 6A 00 6A 01 6A 00 68 D5 00 00 00 8B 4D 10 E8 C8 2D FD FF 85 C0 74 31 50 89 45 FC 83 F8 10 72 16 83 F8 1F 73 11 8B 4D 14 E8 38 9E FC FF FF 75 FC 50 E8 A5 86 FE FF 39 45 08 73 10 6A 14 FF 75 08 E8 96 86 FE FF 29 45 08 8B 45 08 8B E5 5D C2 10 00` | legacy-od-block | 161 | - |
| `0x0043D3B6` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0043D3B8` (va) | `-` | `FF` | legacy-od-block | 1 | - |
| `0x0043D403` (va) | `-` | `00` | legacy-od-block | 1 | - |
| `0x0043D405` (va) | `-` | `FF` | legacy-od-block | 1 | - |
