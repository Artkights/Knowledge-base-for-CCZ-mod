# 曹操传 MOD 引擎知识库

本仓库是一份面向人和机器的二进制技术知识库。结构化 JSON 是唯一事实来源；`reference/` Markdown 全部由工具生成。

## 什么是有用内容

能直接支持逆向、制作或自动化查询的内容：已绑定版本画像的 VA/RVA/文件偏移，函数 ABI 与参数，调用链，表基址、步长、字段偏移、编码、空值，文件头和目录项，以及包含旧字节、覆盖长度、桩入口、回跳和重定位的 Hook 配方。

## 什么是无用内容

仅介绍源码文件作用、构建/测试过程、发布历史、工具接入、治理约束、重复摘要，或没有样本画像和含义的裸地址。这类内容不进入正式知识树；旧条目的处置见 `sources/cleanup-report.json`。

## 读取顺序

1. 选择 `6.5`、`6.5pl`、`6.6` 或 `legacy`。
2. 读取该版本 `README.md`，再查根目录 `index.json`。
3. 需要精确事实时读取条目的 `canonicalDataPath`；Markdown 只用于浏览。
4. `research/` 不属于默认事实，不能直接用于写回。

## 地址规则

每个地址必须声明 `va`、`rva`、`fileOffset`、`pointerSlot` 或 `resolvedRuntimeAddress`。固定地址必须绑定 `profile`；同名函数在不同版本中不得合并。

## 复现

运行 `python tools/query_kb.py "0x004837C2" --version 6.5` 查询完整实体。更新数据后运行 `python tools/build_reference.py`、`python tools/build_index.py` 和 `python tools/validate_kb.py`；生成器在干净克隆中应产生零差异。
