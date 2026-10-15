# 6.6 机制与调用链

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/mechanisms/xiaoan-speed-chain.json`

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
