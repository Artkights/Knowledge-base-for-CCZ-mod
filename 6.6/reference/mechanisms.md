# 6.6 机制与调用链

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/mechanisms/f36-shanzai-ollydbg-research.json`、`6.6/data/mechanisms/shanzai-20261027-mechanisms.json`、`6.6/data/mechanisms/xiaoan-speed-chain.json`

## 从旧 OllyDbg 地址迁移到 F36 样本

ID: `mechanism.66.f36.ollydbg-migration`；状态: `candidate`；证据: `source-reviewed`

1. `fn.66.f36.data-id-to-character-record`：先确认人物记录步长和指针槽
2. `fn.66.f36.battlefield-id-to-unit-record`：再确认战场单位记录入口和寄存器契约
3. `fn.66.f36.data-id-to-battlefield-id`：最后用遍历函数核对哨兵和边界

## F36 SP 累积代码与旧 00410FFF 补丁的偏移差异

ID: `mechanism.66.f36.sp-accumulation-layout`；状态: `candidate`；证据: `static-verified`


计算规则：

- `当前序列：MOV EDX,[EBP+8] -> CMP CL,2 -> JL 0041100C -> SHR EDX,1 / SHR EDX,2`
- `旧回复候选：把 00410FFF 和 00411003 附近的 SHR 改为 XOR EDX,EDX，并在 00411005 补 NOP`
- `迁移结论：先以完整指令和当前原字节重定位；没有 F36 expectedBytes 时保持只读`

## 6.6 集气模式（4018）判定链：双门、两套公式与必中

ID: `mechanism.66.qi.judgement`；状态: `canonical`；证据: `sample-verified`

1. `global.66.qi.gate-switch`：先查第一道门 [0x505FDC]==0，再查第二道门 [0x505EC8]==1；任一不满足回原版随机路径
2. `global.66.qi.pool`：按 模式%16 定位集气字节，按 战场编号 定位单位 4 字节组
3. `fn.66.qi.gate-check`：按 模式&1 选攻击方/防守方公式，返回值即是否触发

计算规则：

- `门：([0x505FDC]==0) AND ([0x505EC8]==1) 才走集气；否则 call 0x43786B 原版随机`
- `攻击方（模式&1==0）：池 + 本次值 >= 100 ⇒ 返回 1 且 池 -= 100`
- `防守方（模式&1==1）：池 + 100 - 传入值 < 100 ⇒ 闪避触发；等价于 池 += (100 - 命中率)`
- `命中率被钳在 [25,100]（0x0043B4E3 `B8 19 00 00 00` 下限 25）；命中率 >= 100 时 0x0043B526 `73 0C` 跳过集气判定，池不再上涨 ⇒ 必中`
- `连击免写回：0x00428814 `cmp [ebp+0xC],0` 且 0x0042881A `cmp byte [0x492DF8],1` ⇒ 模式 0 且连击进行中时本次不改连击池`
- `必中点另有两处：0x0043B60A `cmp byte [0x500E9B],0`（非零即必中）、0x0043B4E8 起 21 字节 NOP 后的块（4018 + [0x4B3D18]==0 + 攻击者 unit+5==0 ⇒ 命中率置 0x64）`

## 小暗 S 超级加速等待链

ID: `mechanism.66.xiaoan.super-s`；状态: `canonical`；证据: `sample-verified`

1. `fn.66.xiaoan.wait-wrapper`：公共等待循环
2. `fn.66.xiaoan.native-stage`：检查原生阶段是否完成
3. `fn.66.xiaoan.message-pump`：未完成时处理窗口消息
4. `patch.66.xiaoan.wait-call`：仅对白名单调用者路由到 SuperYieldBridge
5. `patch.66.xiaoan.extended-display`：跳过扩展显示延迟

S 等待白名单返回地址：

`0x00401F6F`, `0x00401FAE`, `0x00403096`, `0x004030CC`, `0x0040D43F`, `0x0041DB77`, `0x00421A20`, `0x00423981`, `0x00423C63`, `0x004249F7`, `0x0042C537`, `0x0042C6BC`, `0x004371B1`, `0x0043721C`, `0x00453777`, `0x0045380B`, `0x004549DA`

列表是 CALL 返回地址（call-site+5），不是函数入口；R 专用等待调用者明确排除。

## 原生三阶段延迟计算

ID: `mechanism.66.xiaoan.phase-delay`；状态: `canonical`；证据: `source-reviewed`

1. `global.66.xiaoan.phase`：读取 uint8 阶段索引；仅 0..2 有效
2. `global.66.xiaoan.phase-table`：读取 value = phaseTable[phase]
3. `global.66.xiaoan.phase-counter`：value<=50 时递增并按 50 回绕
4. `fn.66.xiaoan.sleep`：调用 Sleep(delay)
5. `fn.66.xiaoan.deadline-check`：speed 低字节为 0 时额外调用

计算规则：

- `value > 50: delay = value - 50`
- `value <= 50: counter = counter + 1; delay = (counter < value ? 1 : 0)`
- `counter >= 50: counter = counter - 50`
- `Sleep(delay); if ((speed & 0xFF) == 0) deadline(); return 1`
