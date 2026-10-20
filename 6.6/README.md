# 6.6 引擎与制作知识

本目录保存 6.6 独立结构、小暗 v0.7 加速引擎事实，以及从历史资料恢复的 6.6/6.6x 指令和补丁候选。小暗 v0.7 是加速补丁，不是天气补丁；`PL天气补丁6.6` 半成品不构成正式知识来源。

固定正式地址绑定测试样本 `profile.ccz66.xiaoan.fixture.25d`，其它作品应使用 masked signature 重新定位。`profile.ccz66x.legacy-patch-family` 只保存旧补丁地址命名空间，没有精确样本 SHA，其下记录一律不得自动应用。

推荐依次读取 `reference/profiles.md`、`functions.md`、`globals.md`、`structures.md`、`patches.md`、`mechanisms.md` 和 `script-commands.md`。E5、EEX、Hexzmap 与分段物品表是跨版本单一事实，见 `../6.5/reference/file-formats.md`，不重复维护。

使用 `python tools/query_kb.py "查询词" --version 6.6` 检索；增加 `--status candidate` 可专门审查历史候选。

宝物类别读写见 [structures.md](reference/structures.md) 中的 `struct.66.item-category-semantics`，天毒珠、太平要术等五个辅助样本绑定当前 `profile.ccz66.shanzai.guoqing.f36` 及其配套数据文件哈希。不同名称/图标布局仍须选择对应 Codec；不能按“五例都能读取”推定旧山贼 EXE 已验证。消耗品的共享候选目录统一维护在 [6.5 mechanisms.md](../6.5/reference/mechanisms.md)，原始字节与用户标签来源见 [sources](../sources/item-semantic-byte-evidence.json)。
