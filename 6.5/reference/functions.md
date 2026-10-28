# 6.5 函数与入口

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/functions/engine-effect-assignment.json`、`6.5/data/functions/legacy-effect-dispatchers.json`、`6.5/data/functions/runtime-functions.json`

| 函数 | 地址 | 调用约定/输入 | 返回 | 含义 | 状态/证据 |
|---|---|---|---|---|---|
| `fn.65.3890.assignment-provider` 加强版6.5未加密3890四参数特效渠道提供器 | `0x0041301E` (va) | ECX unit; four stack arguments; ret 0x10; {'ECX': '当前单位', 'ebp+8': '个人/兵种selector', 'ebp+0C': '装备selector', 'ebp+10': '聚合模式', 'ebp+14': '效果值模式'} | {'EAX': '按调用链聚合后的数值；不能单凭参数将其叫作布尔'} | 从00500C3B取活动表，调用4198BE读取3加1共享N，再经43C794读装备与413009寄存器聚合，随后处理独立专属/套装来源。 | `canonical` / `static-verified` |
| `fn.65.3890.assignment-reader` 加强版6.5未加密38903加1活动特效读取器 | `0x004198BE` (va) | register context plus two stack arguments; ret 8; {'EDX': '活动表基址', 'ECX': '单位上下文', 'AX': '由外层取得的人物匹配token', 'ebp+8': '个人selector', 'ebp+0C': '聚合模式'} | {'EAX': '人物与兵种两来源按模式聚合后的共享N'} | 入口将selector左移3；人物匹配+0/+2/+4，兵种匹配+6；两类命中均读+7。 | `canonical` / `static-verified` |
| `fn.65.3890.assignment-id-writer` 加强版6.5未加密3890活动特效ID分配写入器 | `0x00408811` (va) | one stack argument; ret 4; {'ebp+8': '经426E64解析的配置流；effectId/slotIndex/token'} | 未声明稳定业务返回值 | 40883D校验effectId上界；slot0..2写UInt16人物，slot3只写+6的BYTE兵种；不改+7共享N。 | `canonical` / `static-verified` |
| `fn.65.3890.job-selector-match` 加强版6.5未加密3890兵种匹配与族函数ABI | `0x00422DA8` (va) | two stack arguments; ret 8; {'ebp+8': '槽中兵种ID', 'ebp+0C': '单位详细兵种ID'} | AL=0匹配，AL=1不匹配 | 槽ID>=80拒绝；精确标志开启时比ID，否则按族并要求分配ID<=当前ID；FF自然拒绝。 | `canonical` / `static-verified` |
| `fn.65.effect-dispatch-600000` 特技类型 #1 | `0x00600000` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60002a` MP恢复 (个人=1B, 装备=01) | `0x0060002A` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600054` 特技类型 #3 | `0x00600054` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60007e` 子类型3 | `0x0060007E` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6000c2` 子类型6 | `0x006000C2` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600127` 属性下降 (个人=0C, 装备=5E) | `0x00600127` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600151` 子类型D | `0x00600151` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6001a0` 状态特技#1 | `0x006001A0` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6001ca` 状态特技#2 | `0x006001CA` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6001f4` 状态特技#3 | `0x006001F4` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60021e` 状态特技#4 | `0x0060021E` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600248` 状态特技#5 | `0x00600248` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600272` 状态特技#6 | `0x00600272` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60029c` 状态特技#7 | `0x0060029C` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6002c6` 引导攻击 (个人=18, 装备=36) | `0x006002C6` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6002f0` 状态特技#9 | `0x006002F0` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60031a` 必定暴击 (个人=1A, 装备=29) | `0x0060031A` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600344` 特效调度函数 600344 | `0x00600344` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60036e` 特效调度函数 60036E | `0x0060036E` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600398` 特效调度函数 600398 | `0x00600398` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6003c2` 特效调度函数 6003C2 | `0x006003C2` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6003ec` 特效调度函数 6003EC | `0x006003EC` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600416` 特效调度函数 600416 | `0x00600416` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600440` 特效调度函数 600440 | `0x00600440` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60046a` 特效调度函数 60046A | `0x0060046A` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600494` 特效调度函数 600494 | `0x00600494` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6004be` 特效调度函数 6004BE | `0x006004BE` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6004e8` 特效调度函数 6004E8 | `0x006004E8` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600512` 特效调度函数 600512 | `0x00600512` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60053c` 特效调度函数 60053C | `0x0060053C` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600566` 特效调度函数 600566 | `0x00600566` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600590` 特效调度函数 600590 | `0x00600590` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6005ba` 特效调度函数 6005BA | `0x006005BA` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6005e4` 特效调度函数 6005E4 | `0x006005E4` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60060e` 特效调度函数 60060E | `0x0060060E` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60064b` 已知调度函数 (个人=2D, 装备=3B) | `0x0060064B` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600675` 已知调度函数 | `0x00600675` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60069f` 特效调度函数 60069F | `0x0060069F` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6006c9` 特效调度函数 6006C9 | `0x006006C9` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6006f3` 特效调度函数 6006F3 | `0x006006F3` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60071d` 已知调度函数 (个人=32, 装备=44) | `0x0060071D` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600747` 特效调度函数 600747 | `0x00600747` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600771` 特效调度函数 600771 | `0x00600771` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60079b` 特效调度函数 60079B | `0x0060079B` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6007c5` 特效调度函数 6007C5 | `0x006007C5` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6007ef` 特效调度函数 6007EF | `0x006007EF` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600819` 二次行动 (个人=38, 装备=5A) | `0x00600819` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600843` 特效调度函数 600843 | `0x00600843` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60086d` 特效调度函数 60086D | `0x0060086D` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600897` 特效调度函数 600897 | `0x00600897` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6008c1` 特效调度函数 6008C1 | `0x006008C1` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6008eb` 特效调度函数 6008EB | `0x006008EB` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600915` 特效调度函数 600915 | `0x00600915` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-60093f` 特效调度函数 60093F | `0x0060093F` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600969` 特效调度函数 600969 | `0x00600969` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600993` 特效调度函数 600993 | `0x00600993` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6009bd` 特效调度函数 6009BD | `0x006009BD` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-6009e7` 特效调度函数 6009E7 | `0x006009E7` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.effect-dispatch-600a11` 特效调度函数 600A11 | `0x00600A11` (va) | unknown; AL 可选子类型；单位上下文和四参数桩契约来自调用者 | EAX=核心特效判定结果（历史文档口径） | 按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。 | `candidate` / `legacy-structured` |
| `fn.65.data-id-to-runtime-character` 数据 ID 转人物记录指针 | `0x004061E4` (va) | unknown; DataId | RuntimeCharacter* | 将逻辑人物 ID 映射到 0x48 字节运行时人物记录。 | `canonical` / `static-verified` |
| `fn.65.battlefield-id-to-tactical-unit` 战场 ID 转战术单位指针 | `0x004061F9` (va) | unknown; BattlefieldUnitId | TacticalUnit* | 将战场槽 ID 映射到 0x30 字节战术单位记录。 | `canonical` / `static-verified` |
| `fn.65.tactical-unit-to-runtime-character` 战术单位转人物记录指针 | `0x0040658F` (va) | unknown; TacticalUnit* | RuntimeCharacter* | 读取战术单位 data_id 并映射到人物记录。 | `canonical` / `static-verified` |
| `fn.65.detailed-job-id-to-record` 详细兵种 ID 转记录 | `0x0041B782` (va) | unknown; DetailedJobId | DetailedJobRecord* | 返回 0x23 字节详细兵种记录。 | `canonical` / `static-verified` |
| `fn.65.job-family-id-to-terrain-record` 兵种系 ID 转地形记录 | `0x0041B7D4` (va) | unknown; JobFamilyId | JobFamilyTerrainRecord* | 返回 0x3C 字节兵种系地形记录。 | `canonical` / `static-verified` |
| `fn.65.consumable-item-id-to-count` 消耗品 ID 转数量字节 | `0x00414F65` (va) | unknown; ItemId | uint8* | 按 item_id-150 映射到消耗品数量数组。 | `canonical` / `static-verified` |
| `fn.65.item-id-to-record` 物品 ID 转物品记录 | `0x004837C2` (va) | unknown; ItemId | ItemRecord* | 返回 0x19 字节物品记录；地址查询 0x004837C2 应命中本条。 | `canonical` / `static-verified` |
| `fn.65.strategy-id-to-record` 策略 ID 转策略记录 | `0x00484002` (va) | unknown; StrategyId | StrategyRecord* | 返回 0x61 字节策略记录。 | `canonical` / `static-verified` |
| `fn.65.recalculate-character` 人物能力重算 | `0x004075DF` (va) | thiscall-or-register-context; ECX=person_record_ptr; stack: person_record_ptr:u32; callee cleanup 4 bytes | void | 按人物基础属性、兵种和装备重算派生能力。 | `canonical` / `static-verified` |
| `fn.65.revive-tactical-unit` 战场复活 | `0x004092C7` (va) | unknown; battlefield placement args | void | 6.5/6.4 战场单位复活入口。 | `canonical` / `static-verified` |
| `fn.65.weather-refresh` 天气刷新 | `0x0041D9D1` (va) | unknown; weather context | void | 刷新天气相关战场状态；Python 扳手仅保留历史调用入口。 | `canonical` / `static-verified` |
| `fn.65.direction-refresh` 战场转向刷新 | `0x00457428` (va) | thiscall-or-register-context; ECX=DWORD[0x004B5DF0]; stack: direction:u32, data_id:u32, flags:u32 | void | 参数依次为 direction、data_id、flags。 | `canonical` / `static-verified` |
| `fn.65.position-refresh` 战场坐标刷新 | `0x004594DD` (va) | thiscall-or-register-context; ECX=DWORD[0x004B5DF0]; stack: direction:u32, y:u32, x:u32, data_id:u32 | void | 参数依次为 direction、y、x、data_id。 | `canonical` / `static-verified` |
| `fn.65.attack-entry` 物理攻击入口 | `0x0043DADA` (va) | unknown; combat context | void | 进入物理攻击流程并准备范围描述符。 | `canonical` / `static-verified` |
| `fn.65.attack-selector` 攻击范围选择器 | `0x0045533D` (va) | unknown; attacker/range | void | 准备中心坐标和 packed range descriptor，在 0x004553F8 调用范围分派。 | `canonical` / `static-verified` |
| `fn.65.attack-dispatch` 攻击范围分派 | `0x00436511` (va) | thiscall-or-register-context; ECX=runtime_unit_ptr; stack: [EBP+08]=center_coordinate, [EBP+0C..0F]=packed_range_descriptor; callee cleanup 16 bytes | void | 读取范围指针表并分派几何展开。 | `canonical` / `static-verified` |
| `fn.65.attack-geometry` 攻击几何展开 | `0x00436616` (va) | unknown; center/range segment | void | 把以 FFFF 终止的两字节相对坐标段展开为地图坐标。 | `canonical` / `static-verified` |
| `fn.65.attack-append-target` 攻击目标追加 | `0x00437AFF` (va) | unknown; coordinate/filter | void | 落地坐标、过滤单位并追加到范围目标缓冲。 | `canonical` / `static-verified` |
| `fn.65.map-unit-lookup` 地图坐标查战场单位 | `0x00435884` (va) | unknown; x,y | BattlefieldUnitId | 把地图格坐标映射到战场单位。 | `canonical` / `static-verified` |
| `fn.65.pierce-loader` 穿透值装载 | `0x0040782D` (va) | unknown; unit/effect | uint8 | 从 0x00407881 穿透值表装载穿透类型。 | `canonical` / `static-verified` |
| `fn.65.combat-context-init` 战斗上下文初始化 | `0x00406282` (va) | unknown; attacker/target | void | 初始化物理上下文并写入穿透范围字段。 | `canonical` / `static-verified` |
| `fn.65.pierce-expand-wrapper` 穿透范围扩展包装器 | `0x004364C7` (va) | thiscall-or-register-context; ECX=tactical_unit_ptr; stack: target_battle_id, pierce_byte, output_buffer, filter_or_fallback_args | void | 转入 0x00435CE9 按穿透码展开目标。 | `canonical` / `static-verified` |
| `fn.65.pierce-geometry-dispatch` 穿透几何分派 | `0x00435CE9` (va) | unknown; center/code/output/filter | void | 按 0..0x0B 穿透/效果码分派几何。 | `canonical` / `static-verified` |
| `fn.65.pierce-append-target` 穿透目标追加 | `0x00435BF2` (va) | unknown; coordinate/output/filter | void | 追加穿透/效果范围目标。 | `canonical` / `static-verified` |
| `fn.65.target-consumer` 攻击目标消费与伤害写入 | `0x004361B1` (va) | unknown; target array/context | void | 消费目标数组并进入伤害/效果写入。 | `canonical` / `static-verified` |
| `fn.65.core-effect-engine` 核心特效引擎 | `0x004101D9` (va) | unknown; effect context | result | 核心特效分派入口；具体分支仍应按调用点复核。 | `canonical` / `static-verified` |

## ABI与使用边界

- `fn.65.3890.assignment-provider`（画像 `profile.ccz65.unencrypted.3890.scan`）：413070是尾部mov esp,ebp，实际入口41301E；413073 ret10h。
- `fn.65.3890.assignment-provider`（画像 `profile.ccz65.unencrypted.3890.scan`）：与6.6读取行宽、个人selector处理不同；不得仅以共同地址认定相同实现。
- `fn.65.3890.assignment-reader`（画像 `profile.ccz65.unencrypted.3890.scan`）：419928是退出序列，入口为4198BE。
- `fn.65.3890.assignment-reader`（画像 `profile.ccz65.unencrypted.3890.scan`）：原始读取器不以selector255短路；洗隋有效行仅0..179，3890仅0..254，255可能越界，不能作为通用禁用协议。
- `fn.65.3890.assignment-id-writer`（画像 `profile.ccz65.unencrypted.3890.scan`）：408839为实际写段，408865为函数尾，不是函数入口或N写入口。
- `fn.65.3890.job-selector-match`（画像 `profile.ccz65.unencrypted.3890.scan`）：内部40687C族函数：洗隋cdecl，由调用者清理栈；3890 ret4，由被调清理栈。同地址并不保证相同ABI。
