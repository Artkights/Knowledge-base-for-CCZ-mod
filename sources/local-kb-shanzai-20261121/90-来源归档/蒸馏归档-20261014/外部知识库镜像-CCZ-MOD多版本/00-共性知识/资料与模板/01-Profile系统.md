<!-- generated-kb-entry -->
<!-- source: data管理器/知识库/01-Profile系统.md -->
<!-- version: shared -->
<!-- topic: data-manager -->
<!-- status: canonical -->
<!-- evidence: external-source -->

# Profile 系统

## 结论速览

用户只选择 6.5 或 6.6；布局变体是 6.6 Profile 内部的物理格式差异。`ResolvedProfile` 是读取、编辑、保存和历史校验共同使用的最终定义。

## 适用版本

`ccz-6.5` 与 `ccz-6.6`。配置随核心程序集作为嵌入资源发布，运行时不依赖工作目录中额外的 JSON 文件。

## 已确认事实

- `DataProfile` 保存版本、显示名、默认布局和可用变体。
- `ProfileVariant` 保存布局 ID、样本指纹和表覆盖。
- `ProfileMatchResult` 保存匹配等级、检测方法、证据、冲突与手动覆盖状态。
- `ResolvedProfile` 保存最终表定义、模块和稳定的 `LayoutRevision`。
- 表定义包含 `RecordCodecKey`、`VerificationLevel` 和布局来源。

## 实现与使用方法

6.6 配置继承 6.5 共性表，然后只覆盖物品记录、兵种特效分配和验证等级。启动时会校验字段范围不越过行宽，并根据 Profile、变体、表几何、字段与 codec 计算 `LayoutRevision`。修改任何物理布局定义都会产生新的修订值。

## 风险与边界

手动覆盖只影响当前会话，不写入项目配置。切换 Profile 或变体会重新加载所有表、引用和派生列。历史条目的修订值不同则禁止字节重放。

## 证据来源

`ProfileRegistry`、两个 Profile JSON、Profile 单元测试和跨布局历史冲突测试。

## 待验证项

当前没有通用的第三方 Profile 插件机制；新增版本应进入受测试的内置配置，而不是直接接受任意外部结构定义。
