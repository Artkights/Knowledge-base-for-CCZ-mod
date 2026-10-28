# 6.4 函数与入口

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.4/data/functions/engine-effect-assignment.json`

| 函数 | 地址 | 调用约定/输入 | 返回 | 含义 | 状态/证据 |
|---|---|---|---|---|---|
| `fn.64.xisui.assignment-provider` 洗隋6.4四参数特效渠道提供器 | `0x0041301E` (va) | ECX unit; four stack arguments; ret 0x10; {'ECX': '当前单位', 'ebp+8': '个人/兵种selector', 'ebp+0C': '装备selector', 'ebp+10': '聚合模式', 'ebp+14': '效果值模式'} | {'EAX': '按调用链聚合后的数值；不能单凭参数将其叫作布尔'} | 从00500C3B取活动表，调用4198BE读取3加1共享N，再经43C794读装备与413009寄存器聚合，随后处理独立专属/套装来源。 | `canonical` / `static-verified` |
| `fn.64.xisui.assignment-reader` 洗隋6.43加1活动特效读取器 | `0x004198BE` (va) | register context plus two stack arguments; ret 8; {'EDX': '活动表基址', 'ECX': '单位上下文', 'AX': '由外层取得的人物匹配token', 'ebp+8': '个人selector', 'ebp+0C': '聚合模式'} | {'EAX': '人物与兵种两来源按模式聚合后的共享N'} | 入口将selector左移3；人物匹配+0/+2/+4，兵种匹配+6；两类命中均读+7。 | `canonical` / `static-verified` |
| `fn.64.xisui.assignment-id-writer` 洗隋6.4活动特效ID分配写入器 | `0x00408811` (va) | one stack argument; ret 4; {'ebp+8': '经426E64解析的配置流；effectId/slotIndex/token'} | 未声明稳定业务返回值 | 40883D校验effectId上界；slot0..2写UInt16人物，slot3只写+6的BYTE兵种；不改+7共享N。 | `canonical` / `static-verified` |
| `fn.64.xisui.job-selector-match` 洗隋6.4兵种匹配与族函数ABI | `0x00422DA8` (va) | two stack arguments; ret 8; {'ebp+8': '槽中兵种ID', 'ebp+0C': '单位详细兵种ID'} | AL=0匹配，AL=1不匹配 | 槽ID>=80拒绝；精确标志开启时比ID，否则按族并要求分配ID<=当前ID；FF自然拒绝。 | `canonical` / `static-verified` |

## ABI与使用边界

- `fn.64.xisui.assignment-provider`（画像 `profile.ccz64.xisui.9112`）：413070是尾部mov esp,ebp，实际入口41301E；413073 ret10h。
- `fn.64.xisui.assignment-provider`（画像 `profile.ccz64.xisui.9112`）：与6.6读取行宽、个人selector处理不同；不得仅以共同地址认定相同实现。
- `fn.64.xisui.assignment-reader`（画像 `profile.ccz64.xisui.9112`）：419928是退出序列，入口为4198BE。
- `fn.64.xisui.assignment-reader`（画像 `profile.ccz64.xisui.9112`）：原始读取器不以selector255短路；洗隋有效行仅0..179，3890仅0..254，255可能越界，不能作为通用禁用协议。
- `fn.64.xisui.assignment-id-writer`（画像 `profile.ccz64.xisui.9112`）：408839为实际写段，408865为函数尾，不是函数入口或N写入口。
- `fn.64.xisui.job-selector-match`（画像 `profile.ccz64.xisui.9112`）：内部40687C族函数：洗隋cdecl，由调用者清理栈；3890 ret4，由被调清理栈。同地址并不保证相同ABI。
