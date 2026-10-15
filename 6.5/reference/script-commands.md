# 6.5 剧本指令

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/scripts/script-commands.json`

> `candidate` 指令可用于解析器设计和样本比对；参数语义未复核前不得驱动自动改写。

| ID | Opcode/子命令 | 名称 | 分类 | 参数槽 | 状态/证据 |
|---|---|---|---|---|---|
| `script.65.opcode-00` | `0x00` | 事件结束 | `structure-flow` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-01` | `0x01` | 子事件设定 | `structure-flow` | P1:子事件编号[事件/子事件编号]; P2:启用标志[布尔/开关标志]; P3:触发阶段/状态[数值/枚举]; P4:后续流程[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-02` | `0x02` | 内部信息 | `structure-flow` | P1:信息编号[文本编号候选]; P2:显示方式[布尔/开关标志]; P3:关联人物/头像[人物/部队编号]; P4:流程/标志[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-03` | `0x03` | else | `structure-flow` | P1:跳转/块编号[分支/跳转目标]; P2:分支层级/标志[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-04` | `0x04` | 询问测试 | `structure-flow` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-05` | `0x05` | 变量测试 | `structure-flow` | P1:变量编号[变量编号]; P2:比较方式[比较符]; P3:比较值[数值/枚举]; P4:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-06` | `0x06` | 我军出场限制 | `structure-flow` | P1:我军人物/出场位[人物/部队编号]; P2:允许/禁止标志[布尔/开关标志]; P3:数量/位置[数量/时间] | `candidate` / `legacy-structured` |
| `script.65.opcode-07` | `0x07` | 出战测试 | `structure-flow` | P1:人物/出战位[人物/部队编号]; P2:比较方式[比较符]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-08` | `0x08` | 菜单处理 | `structure-flow` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-09` | `0x09` | 延时 | `structure-flow` | P1:等待时间[数量/时间]; P2:等待方式[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-0a` | `0x0A` | 初始化局部变量 | `structure-flow` | P1:局部变量编号[变量编号]; P2:初始值[数值/枚举]; P3:初始化方式[运算/赋值方式] | `candidate` / `legacy-structured` |
| `script.65.opcode-0b` | `0x0B` | 变量赋值 | `structure-flow` | P1:变量编号[变量编号]; P2:赋值/运算方式[运算/赋值方式]; P3:新值/来源值[数值/枚举]; P4:作用域/后续标志[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-0c` | `0x0C` | 结束Section | `structure-flow` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-0d` | `0x0D` | 结束Scene | `structure-flow` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-0e` | `0x0E` | 战斗失败 | `structure-flow` | P1:失败原因/分支[数值/枚举]; P2:失败文本/演出[文本编号候选]; P3:后续跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-0f` | `0x0F` | 结局设定 | `structure-flow` | P1:结局/路线编号[数值/枚举]; P2:角色/阵营[人物/部队编号]; P3:保存标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-10` | `0x10` | 许子将指导 | `structure-flow` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-11` | `0x11` | 剧本跳转 | `structure-flow` | P1:目标剧本/关卡[地图/剧本编号]; P2:进入方式[数值/枚举]; P3:保留状态[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-12` | `0x12` | 选择框 | `structure-flow` | P1:选择框编号[文本编号候选]; P2:选项数量[数量/时间]; P3:默认项/标志[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-13` | `0x13` | case | `structure-flow` | P1:case 值[数值/枚举]; P2:跳转/块编号[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-14` | `0x14` | 对话 | `text-audio-visual` | P1:说话人/头像[人物/部队编号]; P2:文本编号[文本编号候选]; P3:表情/朝向[方向/朝向]; P4:显示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-15` | `0x15` | 对话2 | `text-audio-visual` | P1:说话人/头像[人物/部队编号]; P2:文本编号[文本编号候选]; P3:表情/窗口样式[数值/枚举]; P4:显示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-16` | `0x16` | 信息 | `text-audio-visual` | P1:信息文本编号[文本编号候选]; P2:显示方式[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-17` | `0x17` | 场所名 | `text-audio-visual` | P1:场所文本编号[文本编号候选]; P2:显示方式[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-18` | `0x18` | 事件名称设定 | `text-audio-visual` | P1:事件名文本编号[文本编号候选]; P2:保存/显示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-19` | `0x19` | 胜利条件 | `text-audio-visual` | P1:胜利条件文本[文本编号候选]; P2:条件类型[数值/枚举]; P3:关联人物/地点[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-1a` | `0x1A` | 显示胜利条件 | `text-audio-visual` | P1:显示标志[布尔/开关标志]; P2:文本编号[文本编号候选] | `candidate` / `legacy-structured` |
| `script.65.opcode-1b` | `0x1B` | 撤退信息是否显示设定 | `text-audio-visual` | P1:显示标志[布尔/开关标志]; P2:作用对象/阵营[阵营/行动方] | `candidate` / `legacy-structured` |
| `script.65.opcode-1c` | `0x1C` | 绘图 | `text-audio-visual` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-1d` | `0x1D` | 调色板设定 | `text-audio-visual` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-1e` | `0x1E` | 武将重绘 | `text-audio-visual` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-1f` | `0x1F` | 地图视点切换 | `text-audio-visual` | P1:X坐标/目标[X 坐标/目标]; P2:Y坐标[Y 坐标/目标]; P3:移动速度/等待[数量/时间] | `candidate` / `legacy-structured` |
| `script.65.opcode-20` | `0x20` | 武将头像状态设置 | `text-audio-visual` | P1:人物/头像[人物/部队编号]; P2:头像状态[数值/枚举]; P3:显示/保留标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-21` | `0x21` | 战场物体添加 | `text-audio-visual` | P1:物体编号/类型[数值/枚举]; P2:X坐标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:状态/朝向[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-22` | `0x22` | 动画 | `text-audio-visual` | P1:动画编号[数值/枚举]; P2:X坐标/目标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-23` | `0x23` | 音效 | `text-audio-visual` | P1:音效编号[音效编号]; P2:播放方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-24` | `0x24` | CD音轨 | `text-audio-visual` | P1:音乐/CD轨道[音乐/CD 轨道]; P2:播放方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-25` | `0x25` | 武将进入指定地点测试 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:目标X坐标[X 坐标/目标]; P3:目标Y坐标[Y 坐标/目标]; P4:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-26` | `0x26` | 武将进入指定区域测试 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:区域X1[X 坐标/目标]; P3:区域Y1[Y 坐标/目标]; P4:区域X2[X 坐标/目标]; P5:区域Y2[Y 坐标/目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-27` | `0x27` | 背景显示 | `trigger-r-scene` | P1:背景编号[数值/枚举]; P2:显示方式[数值/枚举]; P3:等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-28` | `0x28` | 自由R启动指令 | `trigger-r-scene` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-29` | `0x29` | 地图头像显示 | `trigger-r-scene` | P1:人物/头像[人物/部队编号]; P2:X坐标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:状态/表情[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-2a` | `0x2A` | 地图头像移动 | `trigger-r-scene` | P1:人物/头像[人物/部队编号]; P2:目标X坐标[X 坐标/目标]; P3:目标Y坐标[Y 坐标/目标]; P4:速度/等待[数量/时间] | `candidate` / `legacy-structured` |
| `script.65.opcode-2b` | `0x2B` | 地图头像消失 | `trigger-r-scene` | P1:人物/头像[人物/部队编号]; P2:消失方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-2c` | `0x2C` | 地图文字显示 | `trigger-r-scene` | P1:文字编号[文本编号候选]; P2:X坐标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:显示方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-2d` | `0x2D` | 武将点击测试 | `trigger-r-scene` | P1:人物/对象[人物/部队编号]; P2:比较/状态[比较符]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-2e` | `0x2E` | 武将相邻测试 | `trigger-r-scene` | P1:武将A[人物/部队编号]; P2:武将B[人物/部队编号]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-2f` | `0x2F` | 清除人物 | `trigger-r-scene` | P1:人物/部队编号[人物/部队编号]; P2:清除方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-30` | `0x30` | 武将出现 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:X坐标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:朝向[方向/朝向] | `candidate` / `legacy-structured` |
| `script.65.opcode-31` | `0x31` | 武将消失 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:消失方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-32` | `0x32` | 武将移动 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:目标X坐标[X 坐标/目标]; P3:目标Y坐标[Y 坐标/目标]; P4:速度/等待[数量/时间] | `candidate` / `legacy-structured` |
| `script.65.opcode-33` | `0x33` | 武将转向 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:朝向[方向/朝向] | `candidate` / `legacy-structured` |
| `script.65.opcode-34` | `0x34` | 武将动作 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:动作编号[数值/枚举]; P3:等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-35` | `0x35` | 武将形象改变 | `trigger-r-scene` | P1:武将/部队编号[人物/部队编号]; P2:R/S形象编号[数值/枚举]; P3:刷新/保留标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-36` | `0x36` | 武将状态测试 | `variables-deployment` | P1:武将/部队编号[人物/部队编号]; P2:状态类别[UnitStatus]; P3:比较方式[比较符]; P4:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-37` | `0x37` | 钱、章节编号、忠奸测试 | `variables-deployment` | P1:测试类型[数值/枚举]; P2:比较方式[比较符]; P3:比较值[数值/枚举]; P4:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-38` | `0x38` | 武将能力设定 | `variables-deployment` | P1:武将/人物编号[人物/部队编号]; P2:能力类别[能力类别]; P3:操作方式[运算/赋值方式]; P4:目标数值[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-39` | `0x39` | 武将等级提升 | `variables-deployment` | P1:武将/人物编号[人物/部队编号]; P2:提升等级/经验[数量/时间]; P3:提示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-3a` | `0x3A` | 钱、章节编号、忠奸设置 | `variables-deployment` | P1:设置类型[数值/枚举]; P2:操作方式[运算/赋值方式]; P3:目标数值[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-3b` | `0x3B` | 武将加入 | `variables-deployment` | P1:武将/人物编号[人物/部队编号]; P2:加入方式[数值/枚举]; P3:提示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-3c` | `0x3C` | 武将加入测试 | `variables-deployment` | P1:武将/人物编号[人物/部队编号]; P2:状态比较[比较符]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-3d` | `0x3D` | 获得物品 | `variables-deployment` | P1:物品/装备编号[物品编号]; P2:数量/等级[数量/时间]; P3:提示/标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-3e` | `0x3E` | 加入装备设定 | `variables-deployment` | P1:武将/人物编号[人物/部队编号]; P2:装备槽位[数值/枚举]; P3:物品/装备编号[物品编号]; P4:等级/经验[数量/时间] | `candidate` / `legacy-structured` |
| `script.65.opcode-3f` | `0x3F` | 回合测试 | `variables-deployment` | P1:回合变量[数值/枚举]; P2:比较方式[比较符]; P3:比较值[数量/时间]; P4:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-40` | `0x40` | 行动方测试 | `variables-deployment` | P1:行动方/阵营[阵营/行动方]; P2:比较方式[比较符]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-41` | `0x41` | 战场人数测试 | `variables-deployment` | P1:阵营/范围[阵营/行动方]; P2:比较方式[比较符]; P3:人数值[数量/时间]; P4:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-42` | `0x42` | 战斗胜利测试 | `variables-deployment` | P1:胜利类型[战斗/单挑结果]; P2:比较方式[比较符]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-43` | `0x43` | 战斗失败测试 | `variables-deployment` | P1:失败类型[战斗/单挑结果]; P2:比较方式[比较符]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-44` | `0x44` | 战斗初始化 | `variables-deployment` | P1:初始化段/编号[数值/枚举]; P2:地图/关卡编号[地图/剧本编号]; P3:天气/环境[Weather]; P4:保留状态[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-45` | `0x45` | 战场全局变量 | `variables-deployment` | P1:变量编号[变量编号]; P2:操作方式[运算/赋值方式]; P3:数值[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-46` | `0x46` | 友军出场设定 | `variables-deployment` | P1:友军人物/部队[人物/部队编号]; P2:出场标志[布尔/开关标志]; P3:X坐标[X 坐标/目标]; P4:Y坐标[Y 坐标/目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-47` | `0x47` | 敌军出场设定 | `variables-deployment` | P1:敌军人物/部队[人物/部队编号]; P2:出场标志[布尔/开关标志]; P3:X坐标[X 坐标/目标]; P4:Y坐标[Y 坐标/目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-48` | `0x48` | 敌方装备设定 | `variables-deployment` | P1:人物/部队[人物/部队编号]; P2:武器编码[数值/枚举]; P3:武器等级[数量/时间]; P4:防具编码[数值/枚举]; P5:防具等级[数量/时间]; P6:辅助编码[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-49` | `0x49` | 战斗结束 | `variables-deployment` | P1:结束类型[战斗/单挑结果]; P2:后续剧本/分支[分支/跳转目标]; P3:奖励/结算标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-4a` | `0x4A` | 我军出场强制设定 | `variables-deployment` | P1:我军人物[人物/部队编号]; P2:强制标志[布尔/开关标志]; P3:出场位置[数量/时间] | `candidate` / `legacy-structured` |
| `script.65.opcode-4b` | `0x4B` | 我军出场设定 | `variables-deployment` | P1:我军人物[人物/部队编号]; P2:出场标志[布尔/开关标志]; P3:出场位置[数量/时间] | `candidate` / `legacy-structured` |
| `script.65.opcode-4c` | `0x4C` | 隐藏武将出现 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:X坐标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:朝向/阵营[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-4d` | `0x4D` | 武将状态变更 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:状态类别[UnitStatus]; P3:操作方式[运算/赋值方式] | `candidate` / `legacy-structured` |
| `script.65.opcode-4e` | `0x4E` | 武将方针变更 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:AI 方针[AiPolicy]; P3:目标人物/地点[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-4f` | `0x4F` | 战场转向设置 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:朝向[方向/朝向] | `candidate` / `legacy-structured` |
| `script.65.opcode-50` | `0x50` | 战场动作设定 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:动作编号[数值/枚举]; P3:等待/循环标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-51` | `0x51` | 战场恢复行动权 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:恢复方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-52` | `0x52` | 兵种改变 | `battle-operations` | P1:武将/人物编号[人物/部队编号]; P2:兵种/职业编号[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-53` | `0x53` | 战场撤退 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:撤退方式[数值/枚举]; P3:提示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-54` | `0x54` | 战场撤退确认 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:比较方式[比较符]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-55` | `0x55` | 战场复活 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:X坐标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:HP/状态[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-56` | `0x56` | 天气类别设定 | `battle-operations` | P1:天气类别[Weather]; P2:变化/锁定标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-57` | `0x57` | 当前天气设定 | `battle-operations` | P1:当前天气[Weather]; P2:显示/刷新标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-58` | `0x58` | 战场障碍设定 | `battle-operations` | P1:障碍/对象编号[数值/枚举]; P2:X坐标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:状态[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-59` | `0x59` | 战利品 | `battle-operations` | P1:物品/奖励编号[物品编号]; P2:数量/金钱[数值/枚举]; P3:显示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-5a` | `0x5A` | 战场操作开始 | `battle-operations` | P1:操作阶段[数值/枚举]; P2:控制阵营[阵营/行动方] | `candidate` / `legacy-structured` |
| `script.65.opcode-5b` | `0x5B` | 战场高亮区域 | `battle-operations` | P1:区域X1[X 坐标/目标]; P2:区域Y1[Y 坐标/目标]; P3:区域X2[X 坐标/目标]; P4:区域Y2[Y 坐标/目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-5c` | `0x5C` | 战场高亮人物 | `battle-operations` | P1:武将/部队编号[人物/部队编号]; P2:显示方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-5d` | `0x5D` | 回合上限设定 | `battle-operations` | P1:回合上限[数量/时间]; P2:提示/失败标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-5e` | `0x5E` | 武将不同测试 | `battle-operations` | P1:武将A[人物/部队编号]; P2:武将B[人物/部队编号]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-5f` | `0x5F` | 单挑结束 | `duel-extensions` | P1:结束方式[战斗/单挑结果]; P2:后续跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-60` | `0x60` | 单挑武将出场 | `duel-extensions` | P1:武将A[人物/部队编号]; P2:武将B[人物/部队编号]; P3:出场位置/方向[方向/朝向] | `candidate` / `legacy-structured` |
| `script.65.opcode-61` | `0x61` | 单挑胜负显示 | `duel-extensions` | P1:胜者/武将A[人物/部队编号]; P2:败者/武将B[人物/部队编号]; P3:胜负结果[战斗/单挑结果]; P4:文本/演出编号[文本编号候选] | `candidate` / `legacy-structured` |
| `script.65.opcode-62` | `0x62` | 单挑阵亡 | `duel-extensions` | P1:阵亡/撤退武将[人物/部队编号]; P2:处理方式[战斗/单挑结果] | `candidate` / `legacy-structured` |
| `script.65.opcode-63` | `0x63` | 单挑对话 | `duel-extensions` | P1:说话武将[人物/部队编号]; P2:文本编号[文本编号候选]; P3:表情/方向[方向/朝向] | `candidate` / `legacy-structured` |
| `script.65.opcode-64` | `0x64` | 单挑动作 | `duel-extensions` | P1:动作武将[人物/部队编号]; P2:动作编号[数值/枚举]; P3:等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-65` | `0x65` | 单挑攻击1 | `duel-extensions` | P1:攻击方[人物/部队编号]; P2:防御方[人物/部队编号]; P3:攻击动作/结果[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-66` | `0x66` | 单挑攻击2 | `duel-extensions` | P1:攻击方[人物/部队编号]; P2:防御方[人物/部队编号]; P3:攻击动作/结果[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-67` | `0x67` | 章名 | `duel-extensions` | P1:章名文本编号[文本编号候选]; P2:显示方式[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-68` | `0x68` | 单挑开始 | `duel-extensions` | P1:单挑编号/场景[数值/枚举]; P2:武将A[人物/部队编号]; P3:武将B[人物/部队编号] | `candidate` / `legacy-structured` |
| `script.65.opcode-69` | `0x69` | 旁白 | `duel-extensions` | P1:旁白文本编号[文本编号候选]; P2:显示方式[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-6a` | `0x6A` | Game Over指令 | `duel-extensions` | P1:失败/结束类型[战斗/单挑结果]; P2:显示文本/演出[文本编号候选] | `candidate` / `legacy-structured` |
| `script.65.opcode-6b` | `0x6B` | 法术 | `duel-extensions` | P1:策略/法术编号[策略/法术编号]; P2:施法者[人物/部队编号]; P3:目标/坐标X[X 坐标/目标]; P4:坐标Y/效果值[Y 坐标/目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-6c` | `0x6C` | 武将能力复制 | `duel-extensions` | P1:来源武将[人物/部队编号]; P2:目标武将[人物/部队编号]; P3:能力类别[能力类别] | `candidate` / `legacy-structured` |
| `script.65.opcode-6d` | `0x6D` | 相对复活或移动 | `duel-extensions` | P1:武将/部队编号[人物/部队编号]; P2:相对X[X 坐标/目标]; P3:相对Y[Y 坐标/目标]; P4:方式/标志[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-6e` | `0x6E` | 概率测试 | `duel-extensions` | P1:概率值[数量/时间]; P2:比较/随机方式[数值/枚举]; P3:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-6f` | `0x6F` | 丢弃物品 | `duel-extensions` | P1:物品/装备编号[物品编号]; P2:数量/槽位[数量/时间]; P3:提示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-70` | `0x70` | 能力选择复制 | `advanced-system` | P1:来源武将[人物/部队编号]; P2:目标武将[人物/部队编号]; P3:能力类别[能力类别]; P4:复制方式[运算/赋值方式] | `candidate` / `legacy-structured` |
| `script.65.opcode-71` | `0x71` | 特效请求 | `advanced-system` | P1:特效编号[数值/枚举]; P2:X坐标/目标[X 坐标/目标]; P3:Y坐标[Y 坐标/目标]; P4:等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-72` | `0x72` | 信息传送 | `advanced-system` | P1:源编号/变量[变量编号]; P2:目标编号/变量[变量编号]; P3:传送方式[运算/赋值方式] | `candidate` / `legacy-structured` |
| `script.65.opcode-73` | `0x73` | 人物五围和测试 | `advanced-system` | P1:武将/人物编号[人物/部队编号]; P2:能力类别[能力类别]; P3:比较方式[比较符]; P4:比较值[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-74` | `0x74` | 开/禁存档 | `advanced-system` | P1:存档开关[布尔/开关标志]; P2:作用范围[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-75` | `0x75` | S特殊形象指定 | `advanced-system` | P1:武将/人物编号[人物/部队编号]; P2:S形象/特殊形象编号[数值/枚举]; P3:刷新/保留标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-76` | `0x76` | 无条件跳转 | `advanced-system` | P1:跳转目标[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-77` | `0x77` | 变量运算 | `advanced-system` | P1:变量编号[变量编号]; P2:运算方式[运算/赋值方式]; P3:运算值[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-78` | `0x78` | 整型变量赋值 | `advanced-system` | P1:变量编号[变量编号]; P2:变量类型[数值/枚举]; P3:赋值方式[运算/赋值方式]; P4:赋值内容[数值/枚举] | `candidate` / `legacy-structured` |
| `script.65.opcode-79` | `0x79` | 变量测试 | `advanced-system` | P1:变量编号[变量编号]; P2:变量类型[数值/枚举]; P3:比较方式[比较符]; P4:比较值[数值/枚举]; P5:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-7a` | `0x7A` | 对话3 | `advanced-system` | P1:说话人/头像[人物/部队编号]; P2:文本编号[文本编号候选]; P3:窗口/表情[数值/枚举]; P4:显示标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.65.opcode-7b` | `0x7B` | 信息传送测试 | `advanced-system` | P1:源编号/变量[变量编号]; P2:目标编号/变量[变量编号]; P3:比较方式[比较符]; P4:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-00` | `0x72 / 0` | 信息传送 0: 武将改名 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-01` | `0x72 / 1` | 信息传送 1: 对指定人物释放法术 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-02` | `0x72 / 2` | 信息传送 2: 对指定地点释放法术 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-03` | `0x72 / 3` | 信息传送 3: 对指定范围施放法术 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-04` | `0x72 / 4` | 信息传送 4: 习得策略 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-05` | `0x72 / 5` | 信息传送 5: 习得特技 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-06` | `0x72 / 6` | 信息传送 6: 习得必杀 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-07` | `0x72 / 7` | 信息传送 7: 商店商家变更 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-08` | `0x72 / 8` | 信息传送 8: 战场地图扩展 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-09` | `0x72 / 9` | 信息传送 9: 结局角色展示 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-10` | `0x72 / 10` | 信息传送 10: 装备专属和套装 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-11` | `0x72 / 11` | 信息传送 11: 限定AI行动范围(逐个) | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-12` | `0x72 / 12` | 信息传送 12: S插图 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-13` | `0x72 / 13` | 信息传送 13: 剧本调用函数 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-14` | `0x72 / 14` | 信息传送 14: 战场明暗变化 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-15` | `0x72 / 15` | 信息传送 15: 更换动图 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-16` | `0x72 / 16` | 信息传送 16: 清理离队武将信息 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-17` | `0x72 / 17` | 信息传送 17: 限制区域AI行动范围（范围） | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-18` | `0x72 / 18` | 信息传送 18: 全队成员提升到平均等级 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-19` | `0x72 / 19` | 信息传送 19: 清除一个特殊指针变量 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-20` | `0x72 / 20` | 信息传送 20: 待开发 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-21` | `0x72 / 21` | 信息传送 21: 部队行动标识 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-22` | `0x72 / 22` | 信息传送 22: 结局设置 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-23` | `0x72 / 23` | 信息传送 23: 指定武将列传 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-24` | `0x72 / 24` | 信息传送 24: 指定武将点击语音 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-25` | `0x72 / 25` | 信息传送 25: R数字 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-26` | `0x72 / 26` | 信息传送 26: 产生一个随机数 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-27` | `0x72 / 27` | 信息传送 27: 清空指定武将的功勋 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-28` | `0x72 / 28` | 信息传送 28: R插图 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-29` | `0x72 / 29` | 信息传送 29: pl版指令 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-30` | `0x72 / 30` | 信息传送 30: R文字 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-31` | `0x72 / 31` | 信息传送 31: 只使用战场的一个矩形范围 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-32` | `0x72 / 32` | 信息传送 32: 控制动态图 | `information-transfer` | - | `candidate` / `legacy-structured` |
| `script.65.opcode-72-sub-33` | `0x72 / 33` | 信息传送 33: 设置一个矩形范围的黑幕 | `information-transfer` | - | `candidate` / `legacy-structured` |
