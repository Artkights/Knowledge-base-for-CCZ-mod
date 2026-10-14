# 6.6 函数与入口

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/functions/xiaoan-speed-functions.json`

| 函数 | 地址 | 调用约定/输入 | 返回 | 含义 |
|---|---|---|---|---|
| `fn.66.xiaoan.wait-wrapper` 公共等待包装器 | `0x0042C4E5` (va) | __cdecl; 无显式参数；读取隐式游戏状态 | EAX=int completion flag | 先调用 nativeStage；EAX 非零时返回，EAX 为零时调用消息泵并循环。SiteWaitCall=+3，SiteWaitBranch=+10。 |
| `fn.66.xiaoan.native-stage` 原生阶段加速函数 | `0x004750E0` (va) | __cdecl; 无显式参数；读取 speed、phase、phaseTable、phaseCounter | EAX=int completion flag | 读取 speed、phase、phaseTable、phaseCounter，调用 sleep/deadline 完成阶段节拍。 |
| `fn.66.xiaoan.native-super` 原生 Z 超级加速切换函数 | `0x004250E6` (va) | __cdecl; 无显式参数；读取并写入 native state/busy bytes | void | 切换原生超级加速站点并维护 state/busy。 |
| `fn.66.xiaoan.message-pump` 等待循环消息泵 | `0x0047EAC4` (va) | __cdecl; none | void | wait+12 的 CALL rel32 目标；S 加速仍调用它保持消息处理。 |
| `fn.66.xiaoan.deadline-check` 阶段截止判断 | `0x0040C19D` (va) | __cdecl; implicit clock state | EAX=int/bool | nativeStage pacing 块第二个 CALL rel32 目标。 |
| `fn.66.xiaoan.sleep` 阶段休眠函数 | `0x00411195` (va) | __stdcall; stack: duration:uint32; callee cleanup 4 bytes | void | nativeStage pacing 块第一个 CALL rel32 目标。 |

## 已确认调用点

- `fn.66.xiaoan.native-super`：`0x004132E3` (va)；指令 `E8 ?? ?? ?? ??`；Z 键处理分支中的 CALL；rel32 目标必须解析为 0x004250E6，下一地址为 0x004132E8。
