# 6.6 函数与入口

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/functions/f36-shanzai-functions.json`、`6.6/data/functions/xiaoan-speed-functions.json`

| 函数 | 地址 | 调用约定/输入 | 返回 | 含义 | 状态/证据 |
|---|---|---|---|---|---|
| `fn.66.f36.data-id-to-character-record` F36 Data 号到人物记录 | `0x004061E4` (va) | __stdcall; [EBP+0x8] 的 16 位 Data 号；调用者随后使用 ECX | ECX = DWORD[0x004CEA00] + (input & 0xFFFF) * 0x48；RET 4 清理栈参数 | 当前样本中可复核的 0x48 人物记录定位入口。EAX 及 EFLAGS 不作为稳定返回契约。 | `canonical` / `static-verified` |
| `fn.66.f36.battlefield-id-to-unit-record` F36 战场编号到单位记录 | `0x004061F9` (va) | register-context; CL 中的战场编号 | ECX = 0x004A7B20 + (CL & 0xFF) * 0x30；RET 不清理栈 | 当前样本中可复核的战场单位记录定位入口。 | `canonical` / `static-verified` |
| `fn.66.f36.item-id-to-record` F36 物品号到物品记录 | `0x004837C2` (va) | register-context; ECX 中的物品号 | ECX = 0x0049F820 + item_id * 0x19 | 当前样本中可复核的物品记录定位入口。 | `canonical` / `static-verified` |
| `fn.66.f36.strategy-id-to-record` F36 策略号到策略记录 | `0x00484002` (va) | register-context; ECX 中的策略号 | ECX = 0x004A3E77 + strategy_id * 0x61 | 当前样本中可复核的策略记录定位入口。 | `canonical` / `static-verified` |
| `fn.66.f36.data-id-to-battlefield-id` F36 Data 号到战场编号循环 | `0x0043E4D6` (va) | __cdecl-like-stack-input; [EBP+0x8] 目标 Data/记录键；内部遍历战场编号 0..0xF9 | EAX = 命中的编号，未命中时 EAX = 0xFF；当前代码没有 RET n | 静态控制流证明了 0xFF 未命中哨兵和 004061F9 单位遍历；参数实际命名仍需动态样本确认。 | `canonical` / `static-verified` |
| `fn.66.f36.record-pointer-to-battlefield-id` F36 记录指针到战场编号候选 | `0x00477ADC` (va) | __fastcall-candidate; ECX/param_1 指向记录；内部调用 00482715 取首字低 12 位 | 控制流会遍历单位并在未命中时设置 AL=0xFF，但当前样本的最终寄存器返回契约尚未闭环 | 保留为迁移候选；不可直接套用旧教程的 AL/ECX 解释。 | `candidate` / `static-candidate` |
| `fn.66.f36.record-pointer-to-battlefield-id-alt` F36 记录值到战场编号候选二 | `0x004796DC` (va) | __cdecl-like-stack-input; [EBP+0x8] 比较值；内部遍历单位并调用 0045F670 | EAX = 命中编号；无命中路径以预压入的 0xFFFF 返回 | 当前指令序列支持 0xFFFF 哨兵和单位遍历，但输入值的业务命名仍需动态确认。 | `canonical` / `static-verified` |
| `fn.66.xiaoan.wait-wrapper` 公共等待包装器 | `0x0042C4E5` (va) | __cdecl; 无显式参数；读取隐式游戏状态 | EAX=int completion flag | 先调用 nativeStage；EAX 非零时返回，EAX 为零时调用消息泵并循环。SiteWaitCall=+3，SiteWaitBranch=+10。 | `canonical` / `sample-verified` |
| `fn.66.xiaoan.native-stage` 原生阶段加速函数 | `0x004750E0` (va) | __cdecl; 无显式参数；读取 speed、phase、phaseTable、phaseCounter | EAX=int completion flag | 读取 speed、phase、phaseTable、phaseCounter，调用 sleep/deadline 完成阶段节拍。 | `canonical` / `sample-verified` |
| `fn.66.xiaoan.native-super` 原生 Z 超级加速切换函数 | `0x004250E6` (va) | __cdecl; 无显式参数；读取并写入 native state/busy bytes | void | 切换原生超级加速站点并维护 state/busy。 | `canonical` / `sample-verified` |
| `fn.66.xiaoan.message-pump` 等待循环消息泵 | `0x0047EAC4` (va) | __cdecl; none | void | wait+12 的 CALL rel32 目标；S 加速仍调用它保持消息处理。 | `canonical` / `sample-verified` |
| `fn.66.xiaoan.deadline-check` 阶段截止判断 | `0x0040C19D` (va) | __cdecl; implicit clock state | EAX=int/bool | nativeStage pacing 块第二个 CALL rel32 目标。 | `canonical` / `sample-verified` |
| `fn.66.xiaoan.sleep` 阶段休眠函数 | `0x00411195` (va) | __stdcall; stack: duration:uint32; callee cleanup 4 bytes | void | nativeStage pacing 块第一个 CALL rel32 目标。 | `canonical` / `sample-verified` |

## 已确认调用点

- `fn.66.xiaoan.native-super`：`0x004132E3` (va)；指令 `E8 ?? ?? ?? ??`；Z 键处理分支中的 CALL；rel32 目标必须解析为 0x004250E6，下一地址为 0x004132E8。
