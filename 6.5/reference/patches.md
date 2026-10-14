# 6.5 Hook、补丁与定位器

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/patches/hook-recipes.json`

## 攻击范围分派 Hook

ID: `patch.65.attack-dispatch-hook`；类型: `hook`；画像: `profile.ccz65.unencrypted.f9a`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00436511` (va) | `55 8B EC 51 33 C0` | `-` | - | 6 | True |

ABI: ECX=runtime-unit; [EBP+08]=center; [EBP+0C..0F]=packed range bytes; callee ret 0x10

桩入口: `custom attack range dispatcher`

返回: `preserve original caller contract`

重定位: `range pointer table or replacement table`

## 攻击选择器 CALL Hook

ID: `patch.65.attack-selector-call-hook`；类型: `call-retarget`；画像: `profile.ccz65.unencrypted.f9a`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004553F8` (va) | `E8 14 11 FE FF` | `-` | - | 5 | True |

ABI: 保持中心坐标、packed range descriptor、mode bit 和调用者栈布局

桩入口: `replacement selector callee`

返回: `0x004553FD`

重定位: `rel32 target`

## 穿透扩展 Hook

ID: `patch.65.pierce-expand-hook`；类型: `hook`；画像: `profile.ccz65.unencrypted.f9a`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x004364C7` (va) | `55 8B EC 51 51` | `-` | - | 5 | True |

ABI: ECX=tactical-unit; 参数含 target battle id、pierce byte、output buffer、filter/fallback

桩入口: `custom pierce expander`

返回: `preserve wrapper return contract`

重定位: 无

## 穿透几何分派 Hook

ID: `patch.65.pierce-dispatch-hook`；类型: `hook`；画像: `profile.ccz65.unencrypted.f9a`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00435CE9` (va) | `55 8B EC 51 33 C0 50` | `-` | - | 7 | True |

ABI: center coordinate; pierce/effect code; output buffer; filter/fallback

桩入口: `custom geometry dispatcher`

返回: `preserve original callee contract`

重定位: 无

## 物理攻击回复/回 MP 注入入口

ID: `patch.65.physical-recovery-hook`；类型: `hook`；画像: `profile.ccz65.unencrypted.f9a`

| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |
|---|---|---|---|---:|---|
| `0x00418335` (va) | `None` | `-` | - | - | False |

ABI: 待从具体注入实现补齐寄存器、flags 和栈契约

桩入口: `injected recovery body`

返回: `None`

重定位: 无
