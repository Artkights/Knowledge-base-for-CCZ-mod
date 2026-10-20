# 6.5 引擎与制作知识

默认画像为 `profile.ccz65.unencrypted.f9a`，固定 VA 只能用于该样本；派生作品必须先核对画像、原字节和调用语义。

`data/` 是结构化事实源，`reference/` 是生成的浏览页。本目录同时包含 `canonical` 正式事实与 `candidate` 历史技术记录。候选可用于定位、解析器和迁移方案，但不能在缺少原字节或运行时证据时自动写回。

推荐读取顺序：

1. `reference/profiles.md`、`functions.md`、`globals.md`、`structures.md`、`file-formats.md`；
2. `effect-stubs.md`、`patches.md`、`mechanisms.md`；
3. `script-commands.md`；
4. `workflows.md`、`test-contracts.md`、`case-studies.md`。

使用 `python tools/query_kb.py "查询词" --version 6.5` 可同时检索正式事实和候选；增加 `--canonical-only` 只返回正式事实。

宝物读写从 [structures.md](reference/structures.md) 中的 `struct.65.item-category-semantics` 开始，结合 [file-formats.md](reference/file-formats.md) 中的 `format.data-manager.item-codecs` 核对类别、物理偏移与 CSV 列名。消耗品目录见 [mechanisms.md](reference/mechanisms.md) 中的 `mechanism.shared.consumable-effect-namespace`；标签、样本原值与游戏运行时证据分别记录，目录整体仍为候选。小型字节证据见 [item-semantic-byte-evidence.json](../sources/item-semantic-byte-evidence.json)，回归步骤见 [test-contracts.md](reference/test-contracts.md)。
