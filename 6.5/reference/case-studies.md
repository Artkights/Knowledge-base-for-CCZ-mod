# 6.5 制作案例

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/cases/production-cases.json`

## 安西军传 Data ModPackage

ID: `case.65.anxi-data-package`；状态: `candidate`；证据: `legacy-case-record`

目标：把人物、兵种和职业设计批量写入独立基底。

输入：

- 1005 个表更新
- 人物 260 行
- 兵种系 40 行
- 详细职业 80 行

过程：

- preview
- apply-test-copy
- 表域烟测
- 复读
- promote

结果：

- 表写入烟测通过
- 生成 Data/Imsg/Ekd5 备份和报告

可复用结论：

- 纯 Data 包不应被无关地图烟测阻断
- 基础表、特效分配和资源替换应拆包
- 中文必须按目标表编码复读

## 安西军传台词小包

ID: `case.65.anxi-quote-package`；状态: `candidate`；证据: `legacy-case-record`

目标：只更新暴击、撤退台词和特殊暴击人物表，避免重刷全量 Data。

输入：

- 撤退台词 49 行
- 特殊暴击人物 21 行
- 普通暴击 8 组三句

过程：

- 生成小包
- 静态检查
- 测试副本写入
- EffectPackage 写 EXE 表
- 三项复读

结果：

- 测试副本和正式基底复读一致
- 禁止读写 EXE patch 并行执行

可复用结论：

- 文本小改应独立成包
- EXE patch 必须带 expectedOldBytesHex
- 读写依赖操作不能并行

## 安西 R_01 模板克隆迭代

ID: `case.65.anxi-r01-template-clone`；状态: `candidate`；证据: `legacy-case-record`

目标：从成熟 R_01 模板复用完整结构，并逐步修复文本、人物和 R/S 入口。

输入：

- 刘备 6.4 R_01 模板
- 安西目标文本
- 人物映射
- 出战名单

过程：

- 克隆 10 Scene/13 Section/501 Command
- 修正换行和背景
- 清理 0x02 内部信息
- 保证 R 人物实例唯一
- 同步 0x06/0x4A/0x4B

结果：

- 避免自造短结构在 Section 4 卡死
- 形成 507/173 命令规模的最终 R/S 入口样板

可复用结论：

- 完整结构优先于从零拼接
- 剧情露脸人物不等于已加入我军
- 入口人数、名单和部署槽必须一致

## 物理攻击后恢复 MP 复合特效试点

ID: `case.65.mp-recovery-effect-pilot`；状态: `candidate`；证据: `legacy-case-record`

目标：验证从特效蓝图到桩、参数、注入和验收的模块化路径。

输入：

- 物理攻击结算点
- 四参数特效判定
- 伤害值
- MP 字段

过程：

- 定义触发和公式
- 选择内联桩
- 生成代码洞和回跳
- 绑定特效号参数
- 测试副本复读
- 实机验证

结果：

- 形成可复用特效蓝图和写入凭据要求

可复用结论：

- 蓝图必须声明读取和写入字段
- 参数位宽必须与机器码一致
- 发布内容必须与验收样本一致

## 刘备 6.4 R/S 模板学习

ID: `case.65.liu-bei-rs-template`；状态: `candidate`；证据: `legacy-case-record`

目标：从成熟旧版关卡抽取 R 玩家切换、S 初始化和战中事件结构。

输入：

- R_01.eex
- S_01.eex
- 完整树复读结果

过程：

- 统计 Scene/Section/Command
- 识别 R 出战入口
- 识别 S 初始化部署
- 保留高风险命令原参数
- 迁移前做版本复核

结果：

- 提供 R 剧本克隆和 S 战场结构的历史样板

可复用结论：

- 跨版本只复用结构，不复制裸地址
- 高风险命令保留原参数
- 迁移后必须圆程复读
