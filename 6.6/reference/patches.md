# 6.6 Hook、补丁与定位器

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/patches/xiaoan-semantic-locators.json`、`6.6/data/patches/xiaoan-speed-patch-sites.json`

## 原生 Z 加速函数定位器

ID: `locator.66.xiaoan.native-super`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`

签名: `55 8B EC B9 ?? ?? ?? ?? B8 ?? ?? ?? ?? 80 38 00 0F 85 ?? ?? ?? ?? C6 00 01 80 31 01 80 39 01 75 44`

扫描范围: PE32 executable sections of the loaded image

命中规则: exactly one match

- 提取：`nativeSuper=match`
- 提取：`nativeSuperState=absolute operand at match+4 length1`
- 提取：`nativeSuperBusy=absolute operand at match+9 length1`

## 公共等待包装器定位器

ID: `locator.66.xiaoan.wait-wrapper`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`

签名: `55 8B EC E8 ?? ?? ?? ?? 85 C0 75|EB 07 E8 ?? ?? ?? ?? EB F0 5D C3`

扫描范围: PE32 executable sections of the loaded image

命中规则: exactly one match; accept 0x75 or 0xEB at match+10

- 提取：`wait=match`
- 提取：`waitCall=match+3`
- 提取：`waitBranch=match+10`
- 提取：`nativeStage=CALL target at match+3`
- 提取：`pump=CALL target at match+12`

## 原生阶段函数定位器

ID: `locator.66.xiaoan.native-stage`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`

签名: `55 8B EC 0F B7 05 ?? ?? ?? ?? 0F B6 C8 85 C9 75 04 8B C1 EB 04 C1 E8 08 40`

扫描范围: 128 bytes from the nativeStage CALL target in PE32 executable sections

命中规则: function prologue must start exactly at the resolved nativeStage target

- 提取：`match must equal nativeStage CALL target`
- 提取：`speed=absolute operand at match+6 length2`
- 提取：`phase/phaseTable/phaseCounter from nested phase block`
- 提取：`sleep/deadline from two pacing CALL rel32 targets`

## 通用延迟函数定位器

ID: `locator.66.xiaoan.delay`；类型: `semantic-locator`；画像: `profile.ccz66.xiaoan.fixture.25d`

签名: `55 8B EC FF 75 08 E8 ?? ?? ?? ?? E8 ?? ?? ?? ?? F7 D8 1B C0 40 85 C0 75 07 E8 ?? ?? ?? ?? EB EB 5D C2 04 00`

扫描范围: PE32 executable sections of the loaded image

命中规则: exactly one match and both CALL targets must equal the resolved deadline and pump functions

- 提取：`delay=match`
- 提取：`CALL at +11 must target deadline`
- 提取：`CALL at +25 must target pump`

## 对白函数立即返回

ID: `patch.66.xiaoan.dialog`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042D5B0` (va) | `55 8B EC E8` | `C2 0C 00 E8` | function-entry-prefix | 4 | False |

执行流：RET 0x000C 在入口立即返回；第 4 字节只是不可达填充，不能作为完整指令执行。


## 地图文字函数立即返回

ID: `patch.66.xiaoan.map-text`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004332A6` (va) | `55 8B EC 6A` | `C2 10 00 6A` | function-entry-prefix | 4 | False |

执行流：RET 0x0010 在入口立即返回；第 4 字节只是不可达填充。


## 通用延迟函数立即返回

ID: `patch.66.xiaoan.delay`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00422DBA` (va) | `55 8B EC` | `C2 04 00` | function-entry | 3 | True |

执行流：以 RET 0x0004 替换完整三字节函数序言，立即返回并弹出一个参数。


## R 流程等待 CALL 空操作化

ID: `patch.66.xiaoan.r-wait`；类型: `instruction-replacement`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00429964` (va) | `E8 7C 2B 00 00` | `90 90 90 90 90` | whole-instruction | 5 | True |

执行流：删除到公共等待包装器 0x0042C4E5 的 CALL；原 CALL 下一地址为 0x00429969。


## 公共等待中的 nativeStage CALL 重定向

ID: `patch.66.xiaoan.wait-call`；类型: `call-retarget`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042C4E8` (va) | `E8 F3 8B 04 00` | `E8 ?? ?? ?? ??` | whole-instruction-rel32 | 5 | True |

执行流：超级 S 时 CALL 到 SuperYieldBridge；阶段加速时 CALL 到 LegacyPhaseBridge；两者互斥。


ABI: 被调函数为 __cdecl、无显式参数、EAX 返回 int；CALL 后继续执行 0x0042C4ED。

桩入口: `SuperYieldBridge or LegacyPhaseBridge through a near thunk`

返回: `0x0042C4ED`

重定位: `rel32 = thunk - (0x0042C4E8 + 5)`；`near thunk encodes mov eax, absolute32; jmp eax`

## 加速修饰键立即数字段

ID: `patch.66.xiaoan.input-modifier`；类型: `operand-patch`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00413324` (va) | `10` | `10 (VK_SHIFT); 11 (VK_CONTROL)` | immediate-operand-only | 1 | False |

执行流：修改 CMP EAX, imm8 的立即数；完整上下文从 0x00413322 起为 83 F8 <key> 75 0F。


## 第三类对白函数立即返回

ID: `patch.66.xiaoan.dialog3`；类型: `entry-short-circuit`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042DB2C` (va) | `55 8B EC 6A` | `C2 04 00 6A` | function-entry-prefix | 4 | False |

执行流：RET 0x0004 在入口立即返回；第 4 字节只是不可达填充。


## 额外延迟分支跳过

ID: `patch.66.xiaoan.extra-delay`；类型: `instruction-replacement`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00415B40` (va) | `D1 E0` | `EB 06` | whole-instruction | 2 | True |

执行流：把 SHL EAX,1 改为 JMP short +6，跳过后续延迟调用准备。


## 原生超级加速等待分支

ID: `patch.66.xiaoan.wait-branch`；类型: `instruction-replacement`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042C4EF` (va) | `75 07` | `EB 07` | whole-instruction | 2 | True |

执行流：原生 Z 超级加速把 JNZ +7 改为 JMP +7；小暗接管前会识别并还原这一原生状态。


## 对白显示延迟调用跳过

ID: `patch.66.xiaoan.dialog-display`；类型: `control-transfer-prefix`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x0042C812` (va) | `E8 29` | `EB 1D` | instruction-prefix-terminal-transfer | 2 | False |

执行流：用 JMP short +0x1D 覆盖 CALL 的前两字节；跳转使剩余三个 rel32 字节不可达。


## 扩展显示延迟调用跳过

ID: `patch.66.xiaoan.extended-display`；类型: `control-transfer-prefix`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00455CE5` (va) | `E8 56` | `EB F5` | instruction-prefix-terminal-transfer | 2 | False |

执行流：用 JMP short -11 覆盖 CALL 的前两字节；跳转使剩余三个 rel32 字节不可达。


## 原生 Z 切换函数入口重定向

ID: `patch.66.xiaoan.native-super`；类型: `entry-jump`；画像: `profile.ccz66.xiaoan.fixture.25d`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004250E6` (va) | `55 8B EC B9 DB` | `E9 ?? ?? ?? ??` | function-entry-terminal-transfer | 5 | False |

执行流：JMP rel32 到 NativeToggleBridge；原序言和 MOV ECX,imm32 的首两字节被覆盖，原函数不再顺序执行。


ABI: NativeToggleBridge 为 __cdecl、无参数、void；保留原调用者的栈布局。

桩入口: `NativeToggleBridge through a near thunk`

返回: `bridge RET returns directly to the original caller`

重定位: `rel32 = thunk - (0x004250E6 + 5)`；`near thunk encodes mov eax, absolute32; jmp eax`
