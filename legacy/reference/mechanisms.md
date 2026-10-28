# legacy 机制与调用链

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`legacy/data/mechanisms/star175-modifier-mechanisms.json`

## 6.2 策略秒杀属于策略伤害计算分支

ID: `legacy.mechanism.62.star175.strategy-instant-kill`；状态: `legacy-reference`；证据: `legacy-structured`

论坛回复明确说明没有独立的策略秒杀函数；原版海啸、眩晕是在策略伤害计算中追加判断，满足条件时直接以目标当前 HP 作为伤害。


## 6.2 策略天气与四神装备限制已重写

ID: `legacy.mechanism.62.star175.weather-gear-rewrite`；状态: `legacy-reference`；证据: `legacy-structured`

回复给出 6.2 策略天气限制和四神装备/天气检查的关键位置，并指出 star175 已将策略天气限制简写，不能再像旧版一样逐策略控制。


## star175 修改器的版本和工具兼容门禁

ID: `legacy.mechanism.62.star175.modifier-compatibility`；状态: `legacy-reference`；证据: `source-reviewed`

修改器按 EXE/Imsg 和版本分发；6.0 与 6.1 地址会变化，6.2 需要更新后的 CM 数据。修改界面禁用某项表示目标 EXE 不支持该项，不是需要猜密码或强行写入。
