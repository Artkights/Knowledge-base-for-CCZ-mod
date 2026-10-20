# 6.6 数据结构

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/structures/data-manager-physical-tables.json`、`6.6/data/structures/f36-shanzai-structures.json`、`6.6/data/structures/item-category-semantics.json`、`6.6/data/structures/runtime-structures.json`

## 66-standard-v1 人物（persons 物理表）

ID: `struct.66.disk.66-standard-v1.persons`；状态: `canonical`；证据: `source-reviewed`

步长: `0x20` (32)

索引公式: `Data.e5 + 0x18C + (ID - 0) * 0x20 + field_offset; ID=0..1023`

存储：`Data.e5`；起点：`0x18C` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x818C`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 13 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `头像` | `0xD` | 2 | `uint16le` | 头像；字段策略 Editable |
| `撤退台词` | `0xF` | 1 | `uint8` | 撤退台词；字段策略 Editable |
| `暴击台词` | `0x10` | 1 | `uint8` | 暴击台词；字段策略 Editable |
| `Army` | `0x11` | 1 | `uint8` | Army；字段策略 Editable |
| `武力` | `0x12` | 1 | `uint8` | 武力；字段策略 Editable |
| `统帅` | `0x13` | 1 | `uint8` | 统帅；字段策略 Editable |
| `智力` | `0x14` | 1 | `uint8` | 智力；字段策略 Editable |
| `敏捷` | `0x15` | 1 | `uint8` | 敏捷；字段策略 Editable |
| `士气` | `0x16` | 1 | `uint8` | 士气；字段策略 Editable |
| `初始HP` | `0x17` | 2 | `uint16le` | 初始HP；字段策略 Editable |
| `初始MP` | `0x19` | 1 | `uint8` | 初始MP；字段策略 Editable |
| `兵种` | `0x1A` | 1 | `uint8` | 兵种；字段策略 Editable；引用 detailed-jobs |
| `级别` | `0x1B` | 1 | `uint8` | 级别；字段策略 Preserve |
| `经验` | `0x1C` | 1 | `uint8` | 经验；字段策略 Preserve |
| `默认武器` | `0x1D` | 1 | `uint8` | 默认武器；字段策略 Editable；引用 items |
| `默认防具` | `0x1E` | 1 | `uint8` | 默认防具；字段策略 Editable；引用 items |
| `默认辅助` | `0x1F` | 1 | `uint8` | 默认辅助；字段策略 Editable；引用 items |

## 66-standard-v1 人物列传（person-biography 物理表）

ID: `struct.66.disk.66-standard-v1.person-biography`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x2D050 + (ID - 0) * 0xC8 + field_offset; ID=0..1023`

存储：`Imsg.e5`；起点：`0x2D050` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x5F050`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `人物列传` | `0x0` | 200 | `fixed-string` | 人物列传；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 宝物（0-103）（items-low 物理表）

ID: `struct.66.disk.66-standard-v1.items-low`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `Data.e5 + 0x818C + (ID - 0) * 0x19 + field_offset; ID=0..103`

存储：`Data.e5`；起点：`0x818C` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x8BB4`。

能力：`Editable`；Codec：`item-66-15-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 15 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `图标` | `0xF` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x0F UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `保留10` | `0x10` | 1 | `bytes` | 保留10；字段策略 Preserve |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `保留14` | `0x14` | 1 | `bytes` | 保留14；字段策略 Preserve |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-standard-v1 宝物（104-254）（items-high 物理表）

ID: `struct.66.disk.66-standard-v1.items-high`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `Star.e5 + 0x0 + (ID - 104) * 0x19 + field_offset; ID=104..254`

存储：`Star.e5`；起点：`0x0` (fileOffset)；记录数：`151`；ID 起点：`104`；结束偏移（不含）：`0xEBF`。

能力：`Editable`；Codec：`item-66-15-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 6359 | True | `201B4BE3D7183A215A28F54D74C4D3A86CA150B21DEAB5A2F3DB08686B185D55` |
| 新改曹操传6.6修正版 | 6359 | True | `991E2032C87C000FA66F34C5D85F90932057E00EC8E60FCDA9F21430D64E1822` |
| 清儿吕布传 | 6359 | True | `018CABF3376833891F9A1C9112BD1FC8419D14618382FF545578BF682EA800A9` |
| 烈焰同盟6.6x | 10200 | True | `6FBF137C9D2F5CB9884747B59FE5D82A68096B34B762E65496E2BF1ABB7AC3C9` |
| 复刻版6.6山贼 | 6359 | True | `0F196332ECF2E845EA1D93AC2E7762DAADBACC0EBF802CCE697BB1C06BAE6EB9` |
| 复刻版6.6山贼国庆 | 6359 | True | `AA3D4F925C5D7A64759A7F9CDC40EE2DFDCDBDCDEAE086AE436CAF24490C7ED2` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 15 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `图标` | `0xF` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x0F UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `保留10` | `0x10` | 1 | `bytes` | 保留10；字段策略 Preserve |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `保留14` | `0x14` | 1 | `bytes` | 保留14；字段策略 Preserve |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-standard-v1 宝物说明（0-103）（item-description-low 物理表）

ID: `struct.66.disk.66-standard-v1.item-description-low`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x5F050 + (ID - 0) * 0xC8 + field_offset; ID=0..103`

存储：`Imsg.e5`；起点：`0x5F050` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x64190`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 宝物说明（104-254）（item-description-high 物理表）

ID: `struct.66.disk.66-standard-v1.item-description-high`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x64190 + (ID - 104) * 0xC8 + field_offset; ID=104..254`

存储：`Imsg.e5`；起点：`0x64190` (fileOffset)；记录数：`151`；ID 起点：`104`；结束偏移（不含）：`0x6B788`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 兵种系（job-series 物理表）

ID: `struct.66.disk.66-standard-v1.job-series`；状态: `canonical`；证据: `source-reviewed`

步长: `0x9` (9)

索引公式: `Ekd5.exe + 0x8B010 + (ID - 0) * 0x9 + field_offset; ID=0..39`

存储：`Ekd5.exe`；起点：`0x8B010` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0x8B178`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 9 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 兵种系·地形发挥（job-series-terrain 物理表）

ID: `struct.66.disk.66-standard-v1.job-series-terrain`；状态: `canonical`；证据: `source-reviewed`

步长: `0x3C` (60)

索引公式: `Data.e5 + 0xA8A4 + (ID - 0) * 0x3C + field_offset; ID=0..39`

存储：`Data.e5`；起点：`0xA8A4` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xB204`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `平原` | `0x0` | 1 | `uint8` | 平原；字段策略 Editable |
| `草原` | `0x1` | 1 | `uint8` | 草原；字段策略 Editable |
| `树林` | `0x2` | 1 | `uint8` | 树林；字段策略 Editable |
| `荒地` | `0x3` | 1 | `uint8` | 荒地；字段策略 Editable |
| `山地` | `0x4` | 1 | `uint8` | 山地；字段策略 Editable |
| `岩山` | `0x5` | 1 | `uint8` | 岩山；字段策略 Editable |
| `山崖` | `0x6` | 1 | `uint8` | 山崖；字段策略 Editable |
| `雪原` | `0x7` | 1 | `uint8` | 雪原；字段策略 Editable |
| `桥梁` | `0x8` | 1 | `uint8` | 桥梁；字段策略 Editable |
| `浅滩` | `0x9` | 1 | `uint8` | 浅滩；字段策略 Editable |
| `沼泽` | `0xA` | 1 | `uint8` | 沼泽；字段策略 Editable |
| `池塘` | `0xB` | 1 | `uint8` | 池塘；字段策略 Editable |
| `小河` | `0xC` | 1 | `uint8` | 小河；字段策略 Editable |
| `大河` | `0xD` | 1 | `uint8` | 大河；字段策略 Editable |
| `栅栏` | `0xE` | 1 | `uint8` | 栅栏；字段策略 Editable |
| `城墙` | `0xF` | 1 | `uint8` | 城墙；字段策略 Editable |
| `城内` | `0x10` | 1 | `uint8` | 城内；字段策略 Editable |
| `城门` | `0x11` | 1 | `uint8` | 城门；字段策略 Editable |
| `城池` | `0x12` | 1 | `uint8` | 城池；字段策略 Editable |
| `关隘` | `0x13` | 1 | `uint8` | 关隘；字段策略 Editable |
| `鹿砦` | `0x14` | 1 | `uint8` | 鹿砦；字段策略 Editable |
| `村庄` | `0x15` | 1 | `uint8` | 村庄；字段策略 Editable |
| `兵营` | `0x16` | 1 | `uint8` | 兵营；字段策略 Editable |
| `民居` | `0x17` | 1 | `uint8` | 民居；字段策略 Editable |
| `宝物库` | `0x18` | 1 | `uint8` | 宝物库；字段策略 Editable |
| `水池` | `0x19` | 1 | `uint8` | 水池；字段策略 Editable |
| `火` | `0x1A` | 1 | `uint8` | 火；字段策略 Editable |
| `船` | `0x1B` | 1 | `uint8` | 船；字段策略 Editable |
| `祭坛` | `0x1C` | 1 | `uint8` | 祭坛；字段策略 Editable |
| `地下` | `0x1D` | 1 | `uint8` | 地下；字段策略 Editable |

## 66-standard-v1 兵种系·移动消耗（job-series-move-cost 物理表）

ID: `struct.66.disk.66-standard-v1.job-series-move-cost`；状态: `canonical`；证据: `source-reviewed`

步长: `0x3C` (60)

索引公式: `Data.e5 + 0xA8C2 + (ID - 0) * 0x3C + field_offset; ID=0..39`

存储：`Data.e5`；起点：`0xA8C2` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xB222`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `平原` | `0x0` | 1 | `uint8` | 平原；字段策略 Editable |
| `草原` | `0x1` | 1 | `uint8` | 草原；字段策略 Editable |
| `树林` | `0x2` | 1 | `uint8` | 树林；字段策略 Editable |
| `荒地` | `0x3` | 1 | `uint8` | 荒地；字段策略 Editable |
| `山地` | `0x4` | 1 | `uint8` | 山地；字段策略 Editable |
| `岩山` | `0x5` | 1 | `uint8` | 岩山；字段策略 Editable |
| `山崖` | `0x6` | 1 | `uint8` | 山崖；字段策略 Editable |
| `雪原` | `0x7` | 1 | `uint8` | 雪原；字段策略 Editable |
| `桥梁` | `0x8` | 1 | `uint8` | 桥梁；字段策略 Editable |
| `浅滩` | `0x9` | 1 | `uint8` | 浅滩；字段策略 Editable |
| `沼泽` | `0xA` | 1 | `uint8` | 沼泽；字段策略 Editable |
| `池塘` | `0xB` | 1 | `uint8` | 池塘；字段策略 Editable |
| `小河` | `0xC` | 1 | `uint8` | 小河；字段策略 Editable |
| `大河` | `0xD` | 1 | `uint8` | 大河；字段策略 Editable |
| `栅栏` | `0xE` | 1 | `uint8` | 栅栏；字段策略 Editable |
| `城墙` | `0xF` | 1 | `uint8` | 城墙；字段策略 Editable |
| `城内` | `0x10` | 1 | `uint8` | 城内；字段策略 Editable |
| `城门` | `0x11` | 1 | `uint8` | 城门；字段策略 Editable |
| `城池` | `0x12` | 1 | `uint8` | 城池；字段策略 Editable |
| `关隘` | `0x13` | 1 | `uint8` | 关隘；字段策略 Editable |
| `鹿砦` | `0x14` | 1 | `uint8` | 鹿砦；字段策略 Editable |
| `村庄` | `0x15` | 1 | `uint8` | 村庄；字段策略 Editable |
| `兵营` | `0x16` | 1 | `uint8` | 兵营；字段策略 Editable |
| `民居` | `0x17` | 1 | `uint8` | 民居；字段策略 Editable |
| `宝物库` | `0x18` | 1 | `uint8` | 宝物库；字段策略 Editable |
| `水池` | `0x19` | 1 | `uint8` | 水池；字段策略 Editable |
| `火` | `0x1A` | 1 | `uint8` | 火；字段策略 Editable |
| `船` | `0x1B` | 1 | `uint8` | 船；字段策略 Editable |
| `祭坛` | `0x1C` | 1 | `uint8` | 祭坛；字段策略 Editable |
| `地下` | `0x1D` | 1 | `uint8` | 地下；字段策略 Editable |

## 66-standard-v1 兵种系·兵种相克（job-series-counter 物理表）

ID: `struct.66.disk.66-standard-v1.job-series-counter`；状态: `canonical`；证据: `source-reviewed`

步长: `0x28` (40)

索引公式: `Ekd5.exe + 0xA3280 + (ID - 0) * 0x28 + field_offset; ID=0..39`

存储：`Ekd5.exe`；起点：`0xA3280` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xA38C0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `对兵种系 0` | `0x0` | 1 | `uint8` | 对兵种系 0；字段策略 Editable |
| `对兵种系 1` | `0x1` | 1 | `uint8` | 对兵种系 1；字段策略 Editable |
| `对兵种系 2` | `0x2` | 1 | `uint8` | 对兵种系 2；字段策略 Editable |
| `对兵种系 3` | `0x3` | 1 | `uint8` | 对兵种系 3；字段策略 Editable |
| `对兵种系 4` | `0x4` | 1 | `uint8` | 对兵种系 4；字段策略 Editable |
| `对兵种系 5` | `0x5` | 1 | `uint8` | 对兵种系 5；字段策略 Editable |
| `对兵种系 6` | `0x6` | 1 | `uint8` | 对兵种系 6；字段策略 Editable |
| `对兵种系 7` | `0x7` | 1 | `uint8` | 对兵种系 7；字段策略 Editable |
| `对兵种系 8` | `0x8` | 1 | `uint8` | 对兵种系 8；字段策略 Editable |
| `对兵种系 9` | `0x9` | 1 | `uint8` | 对兵种系 9；字段策略 Editable |
| `对兵种系 10` | `0xA` | 1 | `uint8` | 对兵种系 10；字段策略 Editable |
| `对兵种系 11` | `0xB` | 1 | `uint8` | 对兵种系 11；字段策略 Editable |
| `对兵种系 12` | `0xC` | 1 | `uint8` | 对兵种系 12；字段策略 Editable |
| `对兵种系 13` | `0xD` | 1 | `uint8` | 对兵种系 13；字段策略 Editable |
| `对兵种系 14` | `0xE` | 1 | `uint8` | 对兵种系 14；字段策略 Editable |
| `对兵种系 15` | `0xF` | 1 | `uint8` | 对兵种系 15；字段策略 Editable |
| `对兵种系 16` | `0x10` | 1 | `uint8` | 对兵种系 16；字段策略 Editable |
| `对兵种系 17` | `0x11` | 1 | `uint8` | 对兵种系 17；字段策略 Editable |
| `对兵种系 18` | `0x12` | 1 | `uint8` | 对兵种系 18；字段策略 Editable |
| `对兵种系 19` | `0x13` | 1 | `uint8` | 对兵种系 19；字段策略 Editable |
| `对兵种系 20` | `0x14` | 1 | `uint8` | 对兵种系 20；字段策略 Editable |
| `对兵种系 21` | `0x15` | 1 | `uint8` | 对兵种系 21；字段策略 Editable |
| `对兵种系 22` | `0x16` | 1 | `uint8` | 对兵种系 22；字段策略 Editable |
| `对兵种系 23` | `0x17` | 1 | `uint8` | 对兵种系 23；字段策略 Editable |
| `对兵种系 24` | `0x18` | 1 | `uint8` | 对兵种系 24；字段策略 Editable |
| `对兵种系 25` | `0x19` | 1 | `uint8` | 对兵种系 25；字段策略 Editable |
| `对兵种系 26` | `0x1A` | 1 | `uint8` | 对兵种系 26；字段策略 Editable |
| `对兵种系 27` | `0x1B` | 1 | `uint8` | 对兵种系 27；字段策略 Editable |
| `对兵种系 28` | `0x1C` | 1 | `uint8` | 对兵种系 28；字段策略 Editable |
| `对兵种系 29` | `0x1D` | 1 | `uint8` | 对兵种系 29；字段策略 Editable |
| `对兵种系 30` | `0x1E` | 1 | `uint8` | 对兵种系 30；字段策略 Editable |
| `对兵种系 31` | `0x1F` | 1 | `uint8` | 对兵种系 31；字段策略 Editable |
| `对兵种系 32` | `0x20` | 1 | `uint8` | 对兵种系 32；字段策略 Editable |
| `对兵种系 33` | `0x21` | 1 | `uint8` | 对兵种系 33；字段策略 Editable |
| `对兵种系 34` | `0x22` | 1 | `uint8` | 对兵种系 34；字段策略 Editable |
| `对兵种系 35` | `0x23` | 1 | `uint8` | 对兵种系 35；字段策略 Editable |
| `对兵种系 36` | `0x24` | 1 | `uint8` | 对兵种系 36；字段策略 Editable |
| `对兵种系 37` | `0x25` | 1 | `uint8` | 对兵种系 37；字段策略 Editable |
| `对兵种系 38` | `0x26` | 1 | `uint8` | 对兵种系 38；字段策略 Editable |
| `对兵种系 39` | `0x27` | 1 | `uint8` | 对兵种系 39；字段策略 Editable |

## 66-standard-v1 兵种系·兵种属性（job-series-attributes 物理表）

ID: `struct.66.disk.66-standard-v1.job-series-attributes`；状态: `canonical`；证据: `source-reviewed`

步长: `0x28` (40)

索引公式: `Ekd5.exe + 0xA38C0 + (ID - 0) * 0x28 + field_offset; ID=0..7`

存储：`Ekd5.exe`；起点：`0xA38C0` (fileOffset)；记录数：`8`；ID 起点：`0`；结束偏移（不含）：`0xA3A00`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 行号和 UInt8 几何来自读取器与 Profile；移动声音、移动速度、攻击声音、兵种类型的枚举名称由用户确认，未冒充逆向或引擎运行时验证。未列出的数值保留数字并允许按字段边界编辑。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 属性行 ID | 名称 | 值语义 | 语义来源 |
|---:|---|---|---|
| 0 | 移动声音 | 0：马蹄；1：车轮；2：脚步；3：无声；4：引擎；5：预设1；6：预设2 | `user-confirmed-semantics` |
| 1 | 移动速度 | 0：快速；1：慢速 | `user-confirmed-semantics` |
| 2 | 攻击声音 | 0：剑；1：其他；2：爆炸1；3：爆炸2；4：火箭筒；5：枪声（连射）；6：枪声（点射）；7：火焰喷射；8：毒气喷射 | `user-confirmed-semantics` |
| 3 | 远程兵种 | 未在此确认 | `source-reviewed-row-label` |
| 4 | 攻击延迟 | 未在此确认 | `source-reviewed-row-label` |
| 5 | 兵种类型 | 0：全能；1：文官；2：武将 | `user-confirmed-semantics` |
| 6 | 策略伤害 | 未在此确认 | `source-reviewed-row-label` |
| 7 | 参与围攻 | 未在此确认 | `source-reviewed-row-label` |

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `兵种系 0` | `0x0` | 1 | `uint8` | 兵种系 0；字段策略 Editable |
| `兵种系 1` | `0x1` | 1 | `uint8` | 兵种系 1；字段策略 Editable |
| `兵种系 2` | `0x2` | 1 | `uint8` | 兵种系 2；字段策略 Editable |
| `兵种系 3` | `0x3` | 1 | `uint8` | 兵种系 3；字段策略 Editable |
| `兵种系 4` | `0x4` | 1 | `uint8` | 兵种系 4；字段策略 Editable |
| `兵种系 5` | `0x5` | 1 | `uint8` | 兵种系 5；字段策略 Editable |
| `兵种系 6` | `0x6` | 1 | `uint8` | 兵种系 6；字段策略 Editable |
| `兵种系 7` | `0x7` | 1 | `uint8` | 兵种系 7；字段策略 Editable |
| `兵种系 8` | `0x8` | 1 | `uint8` | 兵种系 8；字段策略 Editable |
| `兵种系 9` | `0x9` | 1 | `uint8` | 兵种系 9；字段策略 Editable |
| `兵种系 10` | `0xA` | 1 | `uint8` | 兵种系 10；字段策略 Editable |
| `兵种系 11` | `0xB` | 1 | `uint8` | 兵种系 11；字段策略 Editable |
| `兵种系 12` | `0xC` | 1 | `uint8` | 兵种系 12；字段策略 Editable |
| `兵种系 13` | `0xD` | 1 | `uint8` | 兵种系 13；字段策略 Editable |
| `兵种系 14` | `0xE` | 1 | `uint8` | 兵种系 14；字段策略 Editable |
| `兵种系 15` | `0xF` | 1 | `uint8` | 兵种系 15；字段策略 Editable |
| `兵种系 16` | `0x10` | 1 | `uint8` | 兵种系 16；字段策略 Editable |
| `兵种系 17` | `0x11` | 1 | `uint8` | 兵种系 17；字段策略 Editable |
| `兵种系 18` | `0x12` | 1 | `uint8` | 兵种系 18；字段策略 Editable |
| `兵种系 19` | `0x13` | 1 | `uint8` | 兵种系 19；字段策略 Editable |
| `兵种系 20` | `0x14` | 1 | `uint8` | 兵种系 20；字段策略 Editable |
| `兵种系 21` | `0x15` | 1 | `uint8` | 兵种系 21；字段策略 Editable |
| `兵种系 22` | `0x16` | 1 | `uint8` | 兵种系 22；字段策略 Editable |
| `兵种系 23` | `0x17` | 1 | `uint8` | 兵种系 23；字段策略 Editable |
| `兵种系 24` | `0x18` | 1 | `uint8` | 兵种系 24；字段策略 Editable |
| `兵种系 25` | `0x19` | 1 | `uint8` | 兵种系 25；字段策略 Editable |
| `兵种系 26` | `0x1A` | 1 | `uint8` | 兵种系 26；字段策略 Editable |
| `兵种系 27` | `0x1B` | 1 | `uint8` | 兵种系 27；字段策略 Editable |
| `兵种系 28` | `0x1C` | 1 | `uint8` | 兵种系 28；字段策略 Editable |
| `兵种系 29` | `0x1D` | 1 | `uint8` | 兵种系 29；字段策略 Editable |
| `兵种系 30` | `0x1E` | 1 | `uint8` | 兵种系 30；字段策略 Editable |
| `兵种系 31` | `0x1F` | 1 | `uint8` | 兵种系 31；字段策略 Editable |
| `兵种系 32` | `0x20` | 1 | `uint8` | 兵种系 32；字段策略 Editable |
| `兵种系 33` | `0x21` | 1 | `uint8` | 兵种系 33；字段策略 Editable |
| `兵种系 34` | `0x22` | 1 | `uint8` | 兵种系 34；字段策略 Editable |
| `兵种系 35` | `0x23` | 1 | `uint8` | 兵种系 35；字段策略 Editable |
| `兵种系 36` | `0x24` | 1 | `uint8` | 兵种系 36；字段策略 Editable |
| `兵种系 37` | `0x25` | 1 | `uint8` | 兵种系 37；字段策略 Editable |
| `兵种系 38` | `0x26` | 1 | `uint8` | 兵种系 38；字段策略 Editable |
| `兵种系 39` | `0x27` | 1 | `uint8` | 兵种系 39；字段策略 Editable |

## 66-standard-v1 兵种（detailed-jobs 物理表）

ID: `struct.66.disk.66-standard-v1.detailed-jobs`；状态: `canonical`；证据: `source-reviewed`

步长: `0x9` (9)

索引公式: `Ekd5.exe + 0xD18D0 + (ID - 0) * 0x9 + field_offset; ID=0..79`

存储：`Ekd5.exe`；起点：`0xD18D0` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0xD1BA0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 9 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 兵种说明（detailed-job-description 物理表）

ID: `struct.66.disk.66-standard-v1.detailed-job-description`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x11170 + (ID - 0) * 0xC8 + field_offset; ID=0..79`

存储：`Imsg.e5`；起点：`0x11170` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0x14FF0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `兵种说明` | `0x0` | 200 | `fixed-string` | 兵种说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 兵种成长与装备（detailed-job-growth 物理表）

ID: `struct.66.disk.66-standard-v1.detailed-job-growth`；状态: `canonical`；证据: `source-reviewed`

步长: `0x23` (35)

索引公式: `Data.e5 + 0x9DB4 + (ID - 0) * 0x23 + field_offset; ID=0..79`

存储：`Data.e5`；起点：`0x9DB4` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0xA8A4`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `移动力成长` | `0x0` | 1 | `uint8` | 移动力成长；字段策略 Editable |
| `攻击范围` | `0x1` | 1 | `uint8` | 攻击范围；字段策略 Editable |
| `攻击成长` | `0x2` | 1 | `uint8` | 攻击成长；字段策略 Editable |
| `防御成长` | `0x3` | 1 | `uint8` | 防御成长；字段策略 Editable |
| `精神成长` | `0x4` | 1 | `uint8` | 精神成长；字段策略 Editable |
| `爆发成长` | `0x5` | 1 | `uint8` | 爆发成长；字段策略 Editable |
| `士气成长` | `0x6` | 1 | `uint8` | 士气成长；字段策略 Editable |
| `HP成长` | `0x7` | 1 | `uint8` | HP成长；字段策略 Editable |
| `MP成长` | `0x8` | 1 | `uint8` | MP成长；字段策略 Editable |
| `普通剑` | `0x9` | 1 | `uint8` | 普通剑；字段策略 Editable |
| `特殊剑` | `0xA` | 1 | `uint8` | 特殊剑；字段策略 Editable |
| `普通枪` | `0xB` | 1 | `uint8` | 普通枪；字段策略 Editable |
| `特殊枪` | `0xC` | 1 | `uint8` | 特殊枪；字段策略 Editable |
| `普通弓` | `0xD` | 1 | `uint8` | 普通弓；字段策略 Editable |
| `特殊弓` | `0xE` | 1 | `uint8` | 特殊弓；字段策略 Editable |
| `普通刀` | `0xF` | 1 | `uint8` | 普通刀；字段策略 Editable |
| `特殊刀` | `0x10` | 1 | `uint8` | 特殊刀；字段策略 Editable |
| `普通炮车` | `0x11` | 1 | `uint8` | 普通炮车；字段策略 Editable |
| `特殊炮车` | `0x12` | 1 | `uint8` | 特殊炮车；字段策略 Editable |
| `普通锤` | `0x13` | 1 | `uint8` | 普通锤；字段策略 Editable |
| `特殊锤` | `0x14` | 1 | `uint8` | 特殊锤；字段策略 Editable |
| `普通斧` | `0x15` | 1 | `uint8` | 普通斧；字段策略 Editable |
| `特殊斧` | `0x16` | 1 | `uint8` | 特殊斧；字段策略 Editable |
| `普通扇` | `0x17` | 1 | `uint8` | 普通扇；字段策略 Editable |
| `特殊扇` | `0x18` | 1 | `uint8` | 特殊扇；字段策略 Editable |
| `普通宝剑` | `0x19` | 1 | `uint8` | 普通宝剑；字段策略 Editable |
| `特殊宝剑` | `0x1A` | 1 | `uint8` | 特殊宝剑；字段策略 Editable |
| `普通将剑` | `0x1B` | 1 | `uint8` | 普通将剑；字段策略 Editable |
| `特殊将剑` | `0x1C` | 1 | `uint8` | 特殊将剑；字段策略 Editable |
| `普通铠甲` | `0x1D` | 1 | `uint8` | 普通铠甲；字段策略 Editable |
| `特殊铠甲` | `0x1E` | 1 | `uint8` | 特殊铠甲；字段策略 Editable |
| `普通衣服` | `0x1F` | 1 | `uint8` | 普通衣服；字段策略 Editable |
| `特殊衣服` | `0x20` | 1 | `uint8` | 特殊衣服；字段策略 Editable |
| `普通袍服` | `0x21` | 1 | `uint8` | 普通袍服；字段策略 Editable |
| `特殊袍服` | `0x22` | 1 | `uint8` | 特殊袍服；字段策略 Editable |

## 66-standard-v1 兵种穿透（detailed-job-penetration 物理表）

ID: `struct.66.disk.66-standard-v1.detailed-job-penetration`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0x6C81 + (ID - 0) * 0x1 + field_offset; ID=0..79`

存储：`Ekd5.exe`；起点：`0x6C81` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0x6CD1`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `穿透` | `0x0` | 1 | `uint8` | 穿透；字段策略 Editable |

## 66-standard-v1 策略（strategies 物理表）

ID: `struct.66.disk.66-standard-v1.strategies`；状态: `canonical`；证据: `source-reviewed`

步长: `0x61` (97)

索引公式: `Data.e5 + 0xB204 + (ID - 0) * 0x61 + field_offset; ID=0..143`

存储：`Data.e5`；起点：`0xB204` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xE894`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 11 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `策略类型` | `0xB` | 1 | `uint8` | 策略类型；字段策略 Editable |
| `施展对象` | `0xC` | 1 | `uint8` | 施展对象；字段策略 Editable |
| `施法范围` | `0xD` | 1 | `uint8` | 施法范围；字段策略 Editable |
| `穿透范围` | `0xE` | 1 | `uint8` | 穿透范围；字段策略 Editable |
| `策略消耗` | `0xF` | 1 | `uint8` | 策略消耗；字段策略 Editable |
| `策略图标` | `0x10` | 1 | `uint8` | 策略图标；字段策略 Editable |
| `兵种00学习等级` | `0x11` | 1 | `uint8` | 兵种00学习等级；字段策略 Editable |
| `兵种01学习等级` | `0x12` | 1 | `uint8` | 兵种01学习等级；字段策略 Editable |
| `兵种02学习等级` | `0x13` | 1 | `uint8` | 兵种02学习等级；字段策略 Editable |
| `兵种03学习等级` | `0x14` | 1 | `uint8` | 兵种03学习等级；字段策略 Editable |
| `兵种04学习等级` | `0x15` | 1 | `uint8` | 兵种04学习等级；字段策略 Editable |
| `兵种05学习等级` | `0x16` | 1 | `uint8` | 兵种05学习等级；字段策略 Editable |
| `兵种06学习等级` | `0x17` | 1 | `uint8` | 兵种06学习等级；字段策略 Editable |
| `兵种07学习等级` | `0x18` | 1 | `uint8` | 兵种07学习等级；字段策略 Editable |
| `兵种08学习等级` | `0x19` | 1 | `uint8` | 兵种08学习等级；字段策略 Editable |
| `兵种09学习等级` | `0x1A` | 1 | `uint8` | 兵种09学习等级；字段策略 Editable |
| `兵种10学习等级` | `0x1B` | 1 | `uint8` | 兵种10学习等级；字段策略 Editable |
| `兵种11学习等级` | `0x1C` | 1 | `uint8` | 兵种11学习等级；字段策略 Editable |
| `兵种12学习等级` | `0x1D` | 1 | `uint8` | 兵种12学习等级；字段策略 Editable |
| `兵种13学习等级` | `0x1E` | 1 | `uint8` | 兵种13学习等级；字段策略 Editable |
| `兵种14学习等级` | `0x1F` | 1 | `uint8` | 兵种14学习等级；字段策略 Editable |
| `兵种15学习等级` | `0x20` | 1 | `uint8` | 兵种15学习等级；字段策略 Editable |
| `兵种16学习等级` | `0x21` | 1 | `uint8` | 兵种16学习等级；字段策略 Editable |
| `兵种17学习等级` | `0x22` | 1 | `uint8` | 兵种17学习等级；字段策略 Editable |
| `兵种18学习等级` | `0x23` | 1 | `uint8` | 兵种18学习等级；字段策略 Editable |
| `兵种19学习等级` | `0x24` | 1 | `uint8` | 兵种19学习等级；字段策略 Editable |
| `兵种20学习等级` | `0x25` | 1 | `uint8` | 兵种20学习等级；字段策略 Editable |
| `兵种21学习等级` | `0x26` | 1 | `uint8` | 兵种21学习等级；字段策略 Editable |
| `兵种22学习等级` | `0x27` | 1 | `uint8` | 兵种22学习等级；字段策略 Editable |
| `兵种23学习等级` | `0x28` | 1 | `uint8` | 兵种23学习等级；字段策略 Editable |
| `兵种24学习等级` | `0x29` | 1 | `uint8` | 兵种24学习等级；字段策略 Editable |
| `兵种25学习等级` | `0x2A` | 1 | `uint8` | 兵种25学习等级；字段策略 Editable |
| `兵种26学习等级` | `0x2B` | 1 | `uint8` | 兵种26学习等级；字段策略 Editable |
| `兵种27学习等级` | `0x2C` | 1 | `uint8` | 兵种27学习等级；字段策略 Editable |
| `兵种28学习等级` | `0x2D` | 1 | `uint8` | 兵种28学习等级；字段策略 Editable |
| `兵种29学习等级` | `0x2E` | 1 | `uint8` | 兵种29学习等级；字段策略 Editable |
| `兵种30学习等级` | `0x2F` | 1 | `uint8` | 兵种30学习等级；字段策略 Editable |
| `兵种31学习等级` | `0x30` | 1 | `uint8` | 兵种31学习等级；字段策略 Editable |
| `兵种32学习等级` | `0x31` | 1 | `uint8` | 兵种32学习等级；字段策略 Editable |
| `兵种33学习等级` | `0x32` | 1 | `uint8` | 兵种33学习等级；字段策略 Editable |
| `兵种34学习等级` | `0x33` | 1 | `uint8` | 兵种34学习等级；字段策略 Editable |
| `兵种35学习等级` | `0x34` | 1 | `uint8` | 兵种35学习等级；字段策略 Editable |
| `兵种36学习等级` | `0x35` | 1 | `uint8` | 兵种36学习等级；字段策略 Editable |
| `兵种37学习等级` | `0x36` | 1 | `uint8` | 兵种37学习等级；字段策略 Editable |
| `兵种38学习等级` | `0x37` | 1 | `uint8` | 兵种38学习等级；字段策略 Editable |
| `兵种39学习等级` | `0x38` | 1 | `uint8` | 兵种39学习等级；字段策略 Editable |
| `兵种40学习等级` | `0x39` | 1 | `uint8` | 兵种40学习等级；字段策略 Editable |
| `兵种41学习等级` | `0x3A` | 1 | `uint8` | 兵种41学习等级；字段策略 Editable |
| `兵种42学习等级` | `0x3B` | 1 | `uint8` | 兵种42学习等级；字段策略 Editable |
| `兵种43学习等级` | `0x3C` | 1 | `uint8` | 兵种43学习等级；字段策略 Editable |
| `兵种44学习等级` | `0x3D` | 1 | `uint8` | 兵种44学习等级；字段策略 Editable |
| `兵种45学习等级` | `0x3E` | 1 | `uint8` | 兵种45学习等级；字段策略 Editable |
| `兵种46学习等级` | `0x3F` | 1 | `uint8` | 兵种46学习等级；字段策略 Editable |
| `兵种47学习等级` | `0x40` | 1 | `uint8` | 兵种47学习等级；字段策略 Editable |
| `兵种48学习等级` | `0x41` | 1 | `uint8` | 兵种48学习等级；字段策略 Editable |
| `兵种49学习等级` | `0x42` | 1 | `uint8` | 兵种49学习等级；字段策略 Editable |
| `兵种50学习等级` | `0x43` | 1 | `uint8` | 兵种50学习等级；字段策略 Editable |
| `兵种51学习等级` | `0x44` | 1 | `uint8` | 兵种51学习等级；字段策略 Editable |
| `兵种52学习等级` | `0x45` | 1 | `uint8` | 兵种52学习等级；字段策略 Editable |
| `兵种53学习等级` | `0x46` | 1 | `uint8` | 兵种53学习等级；字段策略 Editable |
| `兵种54学习等级` | `0x47` | 1 | `uint8` | 兵种54学习等级；字段策略 Editable |
| `兵种55学习等级` | `0x48` | 1 | `uint8` | 兵种55学习等级；字段策略 Editable |
| `兵种56学习等级` | `0x49` | 1 | `uint8` | 兵种56学习等级；字段策略 Editable |
| `兵种57学习等级` | `0x4A` | 1 | `uint8` | 兵种57学习等级；字段策略 Editable |
| `兵种58学习等级` | `0x4B` | 1 | `uint8` | 兵种58学习等级；字段策略 Editable |
| `兵种59学习等级` | `0x4C` | 1 | `uint8` | 兵种59学习等级；字段策略 Editable |
| `兵种60学习等级` | `0x4D` | 1 | `uint8` | 兵种60学习等级；字段策略 Editable |
| `兵种61学习等级` | `0x4E` | 1 | `uint8` | 兵种61学习等级；字段策略 Editable |
| `兵种62学习等级` | `0x4F` | 1 | `uint8` | 兵种62学习等级；字段策略 Editable |
| `兵种63学习等级` | `0x50` | 1 | `uint8` | 兵种63学习等级；字段策略 Editable |
| `兵种64学习等级` | `0x51` | 1 | `uint8` | 兵种64学习等级；字段策略 Editable |
| `兵种65学习等级` | `0x52` | 1 | `uint8` | 兵种65学习等级；字段策略 Editable |
| `兵种66学习等级` | `0x53` | 1 | `uint8` | 兵种66学习等级；字段策略 Editable |
| `兵种67学习等级` | `0x54` | 1 | `uint8` | 兵种67学习等级；字段策略 Editable |
| `兵种68学习等级` | `0x55` | 1 | `uint8` | 兵种68学习等级；字段策略 Editable |
| `兵种69学习等级` | `0x56` | 1 | `uint8` | 兵种69学习等级；字段策略 Editable |
| `兵种70学习等级` | `0x57` | 1 | `uint8` | 兵种70学习等级；字段策略 Editable |
| `兵种71学习等级` | `0x58` | 1 | `uint8` | 兵种71学习等级；字段策略 Editable |
| `兵种72学习等级` | `0x59` | 1 | `uint8` | 兵种72学习等级；字段策略 Editable |
| `兵种73学习等级` | `0x5A` | 1 | `uint8` | 兵种73学习等级；字段策略 Editable |
| `兵种74学习等级` | `0x5B` | 1 | `uint8` | 兵种74学习等级；字段策略 Editable |
| `兵种75学习等级` | `0x5C` | 1 | `uint8` | 兵种75学习等级；字段策略 Editable |
| `兵种76学习等级` | `0x5D` | 1 | `uint8` | 兵种76学习等级；字段策略 Editable |
| `兵种77学习等级` | `0x5E` | 1 | `uint8` | 兵种77学习等级；字段策略 Editable |
| `兵种78学习等级` | `0x5F` | 1 | `uint8` | 兵种78学习等级；字段策略 Editable |
| `兵种79学习等级` | `0x60` | 1 | `uint8` | 兵种79学习等级；字段策略 Editable |

## 66-standard-v1 策略说明（strategy-description 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-description`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x0 + (ID - 0) * 0xC8 + field_offset; ID=0..143`

存储：`Imsg.e5`；起点：`0x0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0x7080`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略说明` | `0x0` | 200 | `fixed-string` | 策略说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 策略扩展标记（strategy-extension 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-extension`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2CE0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2CE0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2D70`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-standard-v1 策略伤害类型（strategy-damage-type 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-damage-type`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA30D0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA30D0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3160`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-standard-v1 策略伤害系数（strategy-damage-ratio 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-damage-ratio`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA3040 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA3040` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA30D0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-standard-v1 策略命中率（strategy-hit-rate 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-hit-rate`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2F20 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2F20` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2FB0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-standard-v1 效果索引（strategy-learning 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-learning`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2FB0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2FB0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3040`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-standard-v1 战场AI策略限制（strategy-battle-ai 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-battle-ai`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2E00 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2E00` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2E90`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-standard-v1 练武场AI策略限制（strategy-training-ai 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-training-ai`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2E90 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2E90` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2F20`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-standard-v1 兵种特效分配（class-effects 物理表）

ID: `struct.66.disk.66-standard-v1.class-effects`；状态: `canonical`；证据: `source-reviewed`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0xD9000 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0xD9000` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0xD9FF0`。

能力：`Editable`；Codec：`effect-66-16-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `武将1` | `0x0` | 2 | `uint16le` | 武将1；字段策略 Editable；引用 persons |
| `武将1特效值` | `0x2` | 1 | `uint8` | 武将1特效值；字段策略 Editable |
| `武将2` | `0x3` | 2 | `uint16le` | 武将2；字段策略 Editable；引用 persons |
| `武将2特效值` | `0x5` | 1 | `uint8` | 武将2特效值；字段策略 Editable |
| `武将3` | `0x6` | 2 | `uint16le` | 武将3；字段策略 Editable；引用 persons |
| `武将3特效值` | `0x8` | 1 | `uint8` | 武将3特效值；字段策略 Editable |
| `武将4` | `0x9` | 2 | `uint16le` | 武将4；字段策略 Editable；引用 persons |
| `武将4特效值` | `0xB` | 1 | `uint8` | 武将4特效值；字段策略 Editable |
| `兵种1` | `0xC` | 1 | `uint8` | 兵种1；字段策略 Editable；引用 detailed-jobs |
| `兵种1特效值` | `0xD` | 1 | `uint8` | 兵种1特效值；字段策略 Editable |
| `兵种2` | `0xE` | 1 | `uint8` | 兵种2；字段策略 Editable；引用 detailed-jobs |
| `兵种2特效值` | `0xF` | 1 | `uint8` | 兵种2特效值；字段策略 Editable |

## 66-standard-v1 人物专属、套装专属（personal-effects 物理表）

ID: `struct.66.disk.66-standard-v1.personal-effects`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0xDF800 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0xDF800` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0xE07F0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `武将1` | `0x0` | 2 | `uint16le` | 武将1；字段策略 Editable；引用 persons |
| `装备1` | `0x2` | 1 | `uint8` | 装备1；字段策略 Editable；引用 items |
| `特效值1` | `0x3` | 1 | `uint8` | 特效值1；字段策略 Editable |
| `武将2` | `0x4` | 2 | `uint16le` | 武将2；字段策略 Editable；引用 persons |
| `装备2` | `0x6` | 1 | `uint8` | 装备2；字段策略 Editable；引用 items |
| `特效值2` | `0x7` | 1 | `uint8` | 特效值2；字段策略 Editable |
| `装备3-1` | `0x8` | 1 | `uint8` | 装备3-1；字段策略 Editable；引用 items |
| `装备3-2` | `0x9` | 1 | `uint8` | 装备3-2；字段策略 Editable；引用 items |
| `装备3-3` | `0xA` | 1 | `uint8` | 装备3-3；字段策略 Editable；引用 items |
| `特效值3` | `0xB` | 1 | `uint8` | 特效值3；字段策略 Editable |
| `装备4-1` | `0xC` | 1 | `uint8` | 装备4-1；字段策略 Editable；引用 items |
| `装备4-2` | `0xD` | 1 | `uint8` | 装备4-2；字段策略 Editable；引用 items |
| `装备4-3` | `0xE` | 1 | `uint8` | 装备4-3；字段策略 Editable；引用 items |
| `特效值4` | `0xF` | 1 | `uint8` | 特效值4；字段策略 Editable |

## 66-standard-v1 人物暴击台词（person-critical-quotes 物理表）

ID: `struct.66.disk.66-standard-v1.person-critical-quotes`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x222E0 + (ID - 0) * 0xC8 + field_offset; ID=0..98`

存储：`Imsg.e5`；起点：`0x222E0` (fileOffset)；记录数：`99`；ID 起点：`0`；结束偏移（不含）：`0x27038`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `台词` | `0x0` | 200 | `fixed-string` | 台词；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 人物撤退台词（person-retreat-quotes 物理表）

ID: `struct.66.disk.66-standard-v1.person-retreat-quotes`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x78050 + (ID - 0) * 0xC8 + field_offset; ID=0..48`

存储：`Imsg.e5`；起点：`0x78050` (fileOffset)；记录数：`49`；ID 起点：`0`；结束偏移（不含）：`0x7A698`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 只使用 +491600 的 49×200 区；+440200 仅用于旧区冲突诊断。450000 字节 Imsg 样本不满足边界，必须 unavailable。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `台词` | `0x0` | 200 | `fixed-string` | 台词；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 人物R形象指定（person-r-assign 物理表）

ID: `struct.66.disk.66-standard-v1.person-r-assign`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x2` (2)

索引公式: `Ekd5.exe + 0xE1000 + (ID - 0) * 0x2 + field_offset; ID=0..1023`

存储：`Ekd5.exe`；起点：`0xE1000` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0xE1800`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `R形象ID` | `0x0` | 2 | `uint16le` | R形象ID；字段策略 Editable |

## 66-standard-v1 人物S形象指定（person-s-assign 物理表）

ID: `struct.66.disk.66-standard-v1.person-s-assign`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x2` (2)

索引公式: `Ekd5.exe + 0xD2800 + (ID - 0) * 0x2 + field_offset; ID=0..1023`

存储：`Ekd5.exe`；起点：`0xD2800` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0xD3000`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `S形象ID` | `0x0` | 2 | `uint16le` | S形象ID；字段策略 Editable |

## 66-standard-v1 战役名称（scenario-names 物理表）

ID: `struct.66.disk.66-standard-v1.scenario-names`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0xC350 + (ID - 0) * 0xC8 + field_offset; ID=0..98`

存储：`Imsg.e5`；起点：`0xC350` (fileOffset)；记录数：`99`；ID 起点：`0`；结束偏移（不含）：`0x110A8`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `战役名称` | `0x0` | 200 | `fixed-string` | 战役名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 商店数据（shops 物理表）

ID: `struct.66.disk.66-standard-v1.shops`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x24` (36)

索引公式: `Data.e5 + 0x8BB4 + (ID - 0) * 0x24 + field_offset; ID=0..127`

存储：`Data.e5`；起点：`0x8BB4` (fileOffset)；记录数：`128`；ID 起点：`0`；结束偏移（不含）：`0x9DB4`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `开关仓库人物` | `0x0` | 2 | `uint16le` | 开关仓库人物；字段策略 Editable；引用 persons |
| `买卖物品人物` | `0x2` | 2 | `uint16le` | 买卖物品人物；字段策略 Editable；引用 persons |
| `装备0` | `0x4` | 1 | `uint8` | 装备0；字段策略 Editable；引用 items |
| `装备1` | `0x5` | 1 | `uint8` | 装备1；字段策略 Editable；引用 items |
| `装备2` | `0x6` | 1 | `uint8` | 装备2；字段策略 Editable；引用 items |
| `装备3` | `0x7` | 1 | `uint8` | 装备3；字段策略 Editable；引用 items |
| `装备4` | `0x8` | 1 | `uint8` | 装备4；字段策略 Editable；引用 items |
| `装备5` | `0x9` | 1 | `uint8` | 装备5；字段策略 Editable；引用 items |
| `装备6` | `0xA` | 1 | `uint8` | 装备6；字段策略 Editable；引用 items |
| `装备7` | `0xB` | 1 | `uint8` | 装备7；字段策略 Editable；引用 items |
| `装备8` | `0xC` | 1 | `uint8` | 装备8；字段策略 Editable；引用 items |
| `装备9` | `0xD` | 1 | `uint8` | 装备9；字段策略 Editable；引用 items |
| `装备10` | `0xE` | 1 | `uint8` | 装备10；字段策略 Editable；引用 items |
| `装备11` | `0xF` | 1 | `uint8` | 装备11；字段策略 Editable；引用 items |
| `装备12` | `0x10` | 1 | `uint8` | 装备12；字段策略 Editable；引用 items |
| `装备13` | `0x11` | 1 | `uint8` | 装备13；字段策略 Editable；引用 items |
| `装备14` | `0x12` | 1 | `uint8` | 装备14；字段策略 Editable；引用 items |
| `装备15` | `0x13` | 1 | `uint8` | 装备15；字段策略 Editable；引用 items |
| `物品0` | `0x14` | 1 | `uint8` | 物品0；字段策略 Editable；引用 items |
| `物品1` | `0x15` | 1 | `uint8` | 物品1；字段策略 Editable；引用 items |
| `物品2` | `0x16` | 1 | `uint8` | 物品2；字段策略 Editable；引用 items |
| `物品3` | `0x17` | 1 | `uint8` | 物品3；字段策略 Editable；引用 items |
| `物品4` | `0x18` | 1 | `uint8` | 物品4；字段策略 Editable；引用 items |
| `物品5` | `0x19` | 1 | `uint8` | 物品5；字段策略 Editable；引用 items |
| `物品6` | `0x1A` | 1 | `uint8` | 物品6；字段策略 Editable；引用 items |
| `物品7` | `0x1B` | 1 | `uint8` | 物品7；字段策略 Editable；引用 items |
| `物品8` | `0x1C` | 1 | `uint8` | 物品8；字段策略 Editable；引用 items |
| `物品9` | `0x1D` | 1 | `uint8` | 物品9；字段策略 Editable；引用 items |
| `物品10` | `0x1E` | 1 | `uint8` | 物品10；字段策略 Editable；引用 items |
| `物品11` | `0x1F` | 1 | `uint8` | 物品11；字段策略 Editable；引用 items |
| `物品12` | `0x20` | 1 | `uint8` | 物品12；字段策略 Editable；引用 items |
| `物品13` | `0x21` | 1 | `uint8` | 物品13；字段策略 Editable；引用 items |
| `物品14` | `0x22` | 1 | `uint8` | 物品14；字段策略 Editable；引用 items |
| `物品15` | `0x23` | 1 | `uint8` | 物品15；字段策略 Editable；引用 items |

## 66-standard-v1 兵种特效名称（effect-names 物理表）

ID: `struct.66.disk.66-standard-v1.effect-names`；状态: `canonical`；证据: `source-reviewed`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0x9E800 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0x9E800` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x9F7F0`。

能力：`ReadOnly`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.5 兵种特效名称原始名称区，行尾可能含额外参数；使用专用名称池解析，物理表只读。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 16 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 兵种特效说明（effect-descriptions 物理表）

ID: `struct.66.disk.66-standard-v1.effect-descriptions`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x14FF0 + (ID - 0) * 0xC8 + field_offset; ID=0..254`

存储：`Imsg.e5`；起点：`0x14FF0` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x21728`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `说明` | `0x0` | 200 | `fixed-string` | 说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 人物特效拓展（effect-archive 物理表）

ID: `struct.66.disk.66-standard-v1.effect-archive`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x400` (1024)

索引公式: `Effect.e5 + 0x0 + (ID - 0) * 0x400 + field_offset; ID=0..1023`

存储：`Effect.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x100000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | - | - | `-` |
| 新改曹操传6.6修正版 | - | - | `-` |
| 清儿吕布传 | - | - | `-` |
| 烈焰同盟6.6x | - | - | `-` |
| 复刻版6.6山贼 | - | - | `-` |
| 复刻版6.6山贼国庆 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `槽0特效号` | `0x0` | 1 | `uint8` | 槽0特效号；字段策略 Editable |
| `槽1特效号` | `0x4` | 1 | `uint8` | 槽1特效号；字段策略 Editable |
| `槽2特效号` | `0x8` | 1 | `uint8` | 槽2特效号；字段策略 Editable |
| `槽3特效号` | `0xC` | 1 | `uint8` | 槽3特效号；字段策略 Editable |
| `槽4特效号` | `0x10` | 1 | `uint8` | 槽4特效号；字段策略 Editable |
| `槽5特效号` | `0x14` | 1 | `uint8` | 槽5特效号；字段策略 Editable |
| `槽6特效号` | `0x18` | 1 | `uint8` | 槽6特效号；字段策略 Editable |
| `槽7特效号` | `0x1C` | 1 | `uint8` | 槽7特效号；字段策略 Editable |
| `槽8特效号` | `0x20` | 1 | `uint8` | 槽8特效号；字段策略 Editable |
| `槽9特效号` | `0x24` | 1 | `uint8` | 槽9特效号；字段策略 Editable |
| `槽10特效号` | `0x28` | 1 | `uint8` | 槽10特效号；字段策略 Editable |
| `槽11特效号` | `0x2C` | 1 | `uint8` | 槽11特效号；字段策略 Editable |
| `槽12特效号` | `0x30` | 1 | `uint8` | 槽12特效号；字段策略 Editable |
| `槽13特效号` | `0x34` | 1 | `uint8` | 槽13特效号；字段策略 Editable |
| `槽14特效号` | `0x38` | 1 | `uint8` | 槽14特效号；字段策略 Editable |
| `槽15特效号` | `0x3C` | 1 | `uint8` | 槽15特效号；字段策略 Editable |
| `槽16特效号` | `0x40` | 1 | `uint8` | 槽16特效号；字段策略 Editable |
| `槽17特效号` | `0x44` | 1 | `uint8` | 槽17特效号；字段策略 Editable |
| `槽18特效号` | `0x48` | 1 | `uint8` | 槽18特效号；字段策略 Editable |
| `槽19特效号` | `0x4C` | 1 | `uint8` | 槽19特效号；字段策略 Editable |
| `槽20特效号` | `0x50` | 1 | `uint8` | 槽20特效号；字段策略 Editable |
| `槽21特效号` | `0x54` | 1 | `uint8` | 槽21特效号；字段策略 Editable |
| `槽22特效号` | `0x58` | 1 | `uint8` | 槽22特效号；字段策略 Editable |
| `槽23特效号` | `0x5C` | 1 | `uint8` | 槽23特效号；字段策略 Editable |
| `槽24特效号` | `0x60` | 1 | `uint8` | 槽24特效号；字段策略 Editable |
| `槽25特效号` | `0x64` | 1 | `uint8` | 槽25特效号；字段策略 Editable |
| `槽26特效号` | `0x68` | 1 | `uint8` | 槽26特效号；字段策略 Editable |
| `槽27特效号` | `0x6C` | 1 | `uint8` | 槽27特效号；字段策略 Editable |
| `槽28特效号` | `0x70` | 1 | `uint8` | 槽28特效号；字段策略 Editable |
| `槽29特效号` | `0x74` | 1 | `uint8` | 槽29特效号；字段策略 Editable |
| `槽30特效号` | `0x78` | 1 | `uint8` | 槽30特效号；字段策略 Editable |
| `槽31特效号` | `0x7C` | 1 | `uint8` | 槽31特效号；字段策略 Editable |
| `槽32特效号` | `0x80` | 1 | `uint8` | 槽32特效号；字段策略 Editable |
| `槽33特效号` | `0x84` | 1 | `uint8` | 槽33特效号；字段策略 Editable |
| `槽34特效号` | `0x88` | 1 | `uint8` | 槽34特效号；字段策略 Editable |
| `槽35特效号` | `0x8C` | 1 | `uint8` | 槽35特效号；字段策略 Editable |
| `槽36特效号` | `0x90` | 1 | `uint8` | 槽36特效号；字段策略 Editable |
| `槽37特效号` | `0x94` | 1 | `uint8` | 槽37特效号；字段策略 Editable |
| `槽38特效号` | `0x98` | 1 | `uint8` | 槽38特效号；字段策略 Editable |
| `槽39特效号` | `0x9C` | 1 | `uint8` | 槽39特效号；字段策略 Editable |
| `槽40特效号` | `0xA0` | 1 | `uint8` | 槽40特效号；字段策略 Editable |
| `槽41特效号` | `0xA4` | 1 | `uint8` | 槽41特效号；字段策略 Editable |
| `槽42特效号` | `0xA8` | 1 | `uint8` | 槽42特效号；字段策略 Editable |
| `槽43特效号` | `0xAC` | 1 | `uint8` | 槽43特效号；字段策略 Editable |
| `槽44特效号` | `0xB0` | 1 | `uint8` | 槽44特效号；字段策略 Editable |
| `槽45特效号` | `0xB4` | 1 | `uint8` | 槽45特效号；字段策略 Editable |
| `槽46特效号` | `0xB8` | 1 | `uint8` | 槽46特效号；字段策略 Editable |
| `槽47特效号` | `0xBC` | 1 | `uint8` | 槽47特效号；字段策略 Editable |
| `槽48特效号` | `0xC0` | 1 | `uint8` | 槽48特效号；字段策略 Editable |
| `槽49特效号` | `0xC4` | 1 | `uint8` | 槽49特效号；字段策略 Editable |
| `槽50特效号` | `0xC8` | 1 | `uint8` | 槽50特效号；字段策略 Editable |
| `槽51特效号` | `0xCC` | 1 | `uint8` | 槽51特效号；字段策略 Editable |
| `槽52特效号` | `0xD0` | 1 | `uint8` | 槽52特效号；字段策略 Editable |
| `槽53特效号` | `0xD4` | 1 | `uint8` | 槽53特效号；字段策略 Editable |
| `槽54特效号` | `0xD8` | 1 | `uint8` | 槽54特效号；字段策略 Editable |
| `槽55特效号` | `0xDC` | 1 | `uint8` | 槽55特效号；字段策略 Editable |
| `槽56特效号` | `0xE0` | 1 | `uint8` | 槽56特效号；字段策略 Editable |
| `槽57特效号` | `0xE4` | 1 | `uint8` | 槽57特效号；字段策略 Editable |
| `槽58特效号` | `0xE8` | 1 | `uint8` | 槽58特效号；字段策略 Editable |
| `槽59特效号` | `0xEC` | 1 | `uint8` | 槽59特效号；字段策略 Editable |
| `槽60特效号` | `0xF0` | 1 | `uint8` | 槽60特效号；字段策略 Editable |
| `槽61特效号` | `0xF4` | 1 | `uint8` | 槽61特效号；字段策略 Editable |
| `槽62特效号` | `0xF8` | 1 | `uint8` | 槽62特效号；字段策略 Editable |
| `槽63特效号` | `0xFC` | 1 | `uint8` | 槽63特效号；字段策略 Editable |
| `槽64特效号` | `0x100` | 1 | `uint8` | 槽64特效号；字段策略 Editable |
| `槽65特效号` | `0x104` | 1 | `uint8` | 槽65特效号；字段策略 Editable |
| `槽66特效号` | `0x108` | 1 | `uint8` | 槽66特效号；字段策略 Editable |
| `槽67特效号` | `0x10C` | 1 | `uint8` | 槽67特效号；字段策略 Editable |
| `槽68特效号` | `0x110` | 1 | `uint8` | 槽68特效号；字段策略 Editable |
| `槽69特效号` | `0x114` | 1 | `uint8` | 槽69特效号；字段策略 Editable |
| `槽70特效号` | `0x118` | 1 | `uint8` | 槽70特效号；字段策略 Editable |
| `槽71特效号` | `0x11C` | 1 | `uint8` | 槽71特效号；字段策略 Editable |
| `槽72特效号` | `0x120` | 1 | `uint8` | 槽72特效号；字段策略 Editable |
| `槽73特效号` | `0x124` | 1 | `uint8` | 槽73特效号；字段策略 Editable |
| `槽74特效号` | `0x128` | 1 | `uint8` | 槽74特效号；字段策略 Editable |
| `槽75特效号` | `0x12C` | 1 | `uint8` | 槽75特效号；字段策略 Editable |
| `槽76特效号` | `0x130` | 1 | `uint8` | 槽76特效号；字段策略 Editable |
| `槽77特效号` | `0x134` | 1 | `uint8` | 槽77特效号；字段策略 Editable |
| `槽78特效号` | `0x138` | 1 | `uint8` | 槽78特效号；字段策略 Editable |
| `槽79特效号` | `0x13C` | 1 | `uint8` | 槽79特效号；字段策略 Editable |
| `槽80特效号` | `0x140` | 1 | `uint8` | 槽80特效号；字段策略 Editable |
| `槽81特效号` | `0x144` | 1 | `uint8` | 槽81特效号；字段策略 Editable |
| `槽82特效号` | `0x148` | 1 | `uint8` | 槽82特效号；字段策略 Editable |
| `槽83特效号` | `0x14C` | 1 | `uint8` | 槽83特效号；字段策略 Editable |
| `槽84特效号` | `0x150` | 1 | `uint8` | 槽84特效号；字段策略 Editable |
| `槽85特效号` | `0x154` | 1 | `uint8` | 槽85特效号；字段策略 Editable |
| `槽86特效号` | `0x158` | 1 | `uint8` | 槽86特效号；字段策略 Editable |
| `槽87特效号` | `0x15C` | 1 | `uint8` | 槽87特效号；字段策略 Editable |
| `槽88特效号` | `0x160` | 1 | `uint8` | 槽88特效号；字段策略 Editable |
| `槽89特效号` | `0x164` | 1 | `uint8` | 槽89特效号；字段策略 Editable |
| `槽90特效号` | `0x168` | 1 | `uint8` | 槽90特效号；字段策略 Editable |
| `槽91特效号` | `0x16C` | 1 | `uint8` | 槽91特效号；字段策略 Editable |
| `槽92特效号` | `0x170` | 1 | `uint8` | 槽92特效号；字段策略 Editable |
| `槽93特效号` | `0x174` | 1 | `uint8` | 槽93特效号；字段策略 Editable |
| `槽94特效号` | `0x178` | 1 | `uint8` | 槽94特效号；字段策略 Editable |
| `槽95特效号` | `0x17C` | 1 | `uint8` | 槽95特效号；字段策略 Editable |
| `槽96特效号` | `0x180` | 1 | `uint8` | 槽96特效号；字段策略 Editable |
| `槽97特效号` | `0x184` | 1 | `uint8` | 槽97特效号；字段策略 Editable |
| `槽98特效号` | `0x188` | 1 | `uint8` | 槽98特效号；字段策略 Editable |
| `槽99特效号` | `0x18C` | 1 | `uint8` | 槽99特效号；字段策略 Editable |
| `槽100特效号` | `0x190` | 1 | `uint8` | 槽100特效号；字段策略 Editable |
| `槽101特效号` | `0x194` | 1 | `uint8` | 槽101特效号；字段策略 Editable |
| `槽102特效号` | `0x198` | 1 | `uint8` | 槽102特效号；字段策略 Editable |
| `槽103特效号` | `0x19C` | 1 | `uint8` | 槽103特效号；字段策略 Editable |
| `槽104特效号` | `0x1A0` | 1 | `uint8` | 槽104特效号；字段策略 Editable |
| `槽105特效号` | `0x1A4` | 1 | `uint8` | 槽105特效号；字段策略 Editable |
| `槽106特效号` | `0x1A8` | 1 | `uint8` | 槽106特效号；字段策略 Editable |
| `槽107特效号` | `0x1AC` | 1 | `uint8` | 槽107特效号；字段策略 Editable |
| `槽108特效号` | `0x1B0` | 1 | `uint8` | 槽108特效号；字段策略 Editable |
| `槽109特效号` | `0x1B4` | 1 | `uint8` | 槽109特效号；字段策略 Editable |
| `槽110特效号` | `0x1B8` | 1 | `uint8` | 槽110特效号；字段策略 Editable |
| `槽111特效号` | `0x1BC` | 1 | `uint8` | 槽111特效号；字段策略 Editable |
| `槽112特效号` | `0x1C0` | 1 | `uint8` | 槽112特效号；字段策略 Editable |
| `槽113特效号` | `0x1C4` | 1 | `uint8` | 槽113特效号；字段策略 Editable |
| `槽114特效号` | `0x1C8` | 1 | `uint8` | 槽114特效号；字段策略 Editable |
| `槽115特效号` | `0x1CC` | 1 | `uint8` | 槽115特效号；字段策略 Editable |
| `槽116特效号` | `0x1D0` | 1 | `uint8` | 槽116特效号；字段策略 Editable |
| `槽117特效号` | `0x1D4` | 1 | `uint8` | 槽117特效号；字段策略 Editable |
| `槽118特效号` | `0x1D8` | 1 | `uint8` | 槽118特效号；字段策略 Editable |
| `槽119特效号` | `0x1DC` | 1 | `uint8` | 槽119特效号；字段策略 Editable |
| `槽120特效号` | `0x1E0` | 1 | `uint8` | 槽120特效号；字段策略 Editable |
| `槽121特效号` | `0x1E4` | 1 | `uint8` | 槽121特效号；字段策略 Editable |
| `槽122特效号` | `0x1E8` | 1 | `uint8` | 槽122特效号；字段策略 Editable |
| `槽123特效号` | `0x1EC` | 1 | `uint8` | 槽123特效号；字段策略 Editable |
| `槽124特效号` | `0x1F0` | 1 | `uint8` | 槽124特效号；字段策略 Editable |
| `槽125特效号` | `0x1F4` | 1 | `uint8` | 槽125特效号；字段策略 Editable |
| `槽126特效号` | `0x1F8` | 1 | `uint8` | 槽126特效号；字段策略 Editable |
| `槽127特效号` | `0x1FC` | 1 | `uint8` | 槽127特效号；字段策略 Editable |
| `槽128特效号` | `0x200` | 1 | `uint8` | 槽128特效号；字段策略 Editable |
| `槽129特效号` | `0x204` | 1 | `uint8` | 槽129特效号；字段策略 Editable |
| `槽130特效号` | `0x208` | 1 | `uint8` | 槽130特效号；字段策略 Editable |
| `槽131特效号` | `0x20C` | 1 | `uint8` | 槽131特效号；字段策略 Editable |
| `槽132特效号` | `0x210` | 1 | `uint8` | 槽132特效号；字段策略 Editable |
| `槽133特效号` | `0x214` | 1 | `uint8` | 槽133特效号；字段策略 Editable |
| `槽134特效号` | `0x218` | 1 | `uint8` | 槽134特效号；字段策略 Editable |
| `槽135特效号` | `0x21C` | 1 | `uint8` | 槽135特效号；字段策略 Editable |
| `槽136特效号` | `0x220` | 1 | `uint8` | 槽136特效号；字段策略 Editable |
| `槽137特效号` | `0x224` | 1 | `uint8` | 槽137特效号；字段策略 Editable |
| `槽138特效号` | `0x228` | 1 | `uint8` | 槽138特效号；字段策略 Editable |
| `槽139特效号` | `0x22C` | 1 | `uint8` | 槽139特效号；字段策略 Editable |
| `槽140特效号` | `0x230` | 1 | `uint8` | 槽140特效号；字段策略 Editable |
| `槽141特效号` | `0x234` | 1 | `uint8` | 槽141特效号；字段策略 Editable |
| `槽142特效号` | `0x238` | 1 | `uint8` | 槽142特效号；字段策略 Editable |
| `槽143特效号` | `0x23C` | 1 | `uint8` | 槽143特效号；字段策略 Editable |
| `槽144特效号` | `0x240` | 1 | `uint8` | 槽144特效号；字段策略 Editable |
| `槽145特效号` | `0x244` | 1 | `uint8` | 槽145特效号；字段策略 Editable |
| `槽146特效号` | `0x248` | 1 | `uint8` | 槽146特效号；字段策略 Editable |
| `槽147特效号` | `0x24C` | 1 | `uint8` | 槽147特效号；字段策略 Editable |
| `槽148特效号` | `0x250` | 1 | `uint8` | 槽148特效号；字段策略 Editable |
| `槽149特效号` | `0x254` | 1 | `uint8` | 槽149特效号；字段策略 Editable |
| `槽150特效号` | `0x258` | 1 | `uint8` | 槽150特效号；字段策略 Editable |
| `槽151特效号` | `0x25C` | 1 | `uint8` | 槽151特效号；字段策略 Editable |
| `槽152特效号` | `0x260` | 1 | `uint8` | 槽152特效号；字段策略 Editable |
| `槽153特效号` | `0x264` | 1 | `uint8` | 槽153特效号；字段策略 Editable |
| `槽154特效号` | `0x268` | 1 | `uint8` | 槽154特效号；字段策略 Editable |
| `槽155特效号` | `0x26C` | 1 | `uint8` | 槽155特效号；字段策略 Editable |
| `槽156特效号` | `0x270` | 1 | `uint8` | 槽156特效号；字段策略 Editable |
| `槽157特效号` | `0x274` | 1 | `uint8` | 槽157特效号；字段策略 Editable |
| `槽158特效号` | `0x278` | 1 | `uint8` | 槽158特效号；字段策略 Editable |
| `槽159特效号` | `0x27C` | 1 | `uint8` | 槽159特效号；字段策略 Editable |
| `槽160特效号` | `0x280` | 1 | `uint8` | 槽160特效号；字段策略 Editable |
| `槽161特效号` | `0x284` | 1 | `uint8` | 槽161特效号；字段策略 Editable |
| `槽162特效号` | `0x288` | 1 | `uint8` | 槽162特效号；字段策略 Editable |
| `槽163特效号` | `0x28C` | 1 | `uint8` | 槽163特效号；字段策略 Editable |
| `槽164特效号` | `0x290` | 1 | `uint8` | 槽164特效号；字段策略 Editable |
| `槽165特效号` | `0x294` | 1 | `uint8` | 槽165特效号；字段策略 Editable |
| `槽166特效号` | `0x298` | 1 | `uint8` | 槽166特效号；字段策略 Editable |
| `槽167特效号` | `0x29C` | 1 | `uint8` | 槽167特效号；字段策略 Editable |
| `槽168特效号` | `0x2A0` | 1 | `uint8` | 槽168特效号；字段策略 Editable |
| `槽169特效号` | `0x2A4` | 1 | `uint8` | 槽169特效号；字段策略 Editable |
| `槽170特效号` | `0x2A8` | 1 | `uint8` | 槽170特效号；字段策略 Editable |
| `槽171特效号` | `0x2AC` | 1 | `uint8` | 槽171特效号；字段策略 Editable |
| `槽172特效号` | `0x2B0` | 1 | `uint8` | 槽172特效号；字段策略 Editable |
| `槽173特效号` | `0x2B4` | 1 | `uint8` | 槽173特效号；字段策略 Editable |
| `槽174特效号` | `0x2B8` | 1 | `uint8` | 槽174特效号；字段策略 Editable |
| `槽175特效号` | `0x2BC` | 1 | `uint8` | 槽175特效号；字段策略 Editable |
| `槽176特效号` | `0x2C0` | 1 | `uint8` | 槽176特效号；字段策略 Editable |
| `槽177特效号` | `0x2C4` | 1 | `uint8` | 槽177特效号；字段策略 Editable |
| `槽178特效号` | `0x2C8` | 1 | `uint8` | 槽178特效号；字段策略 Editable |
| `槽179特效号` | `0x2CC` | 1 | `uint8` | 槽179特效号；字段策略 Editable |
| `槽180特效号` | `0x2D0` | 1 | `uint8` | 槽180特效号；字段策略 Editable |
| `槽181特效号` | `0x2D4` | 1 | `uint8` | 槽181特效号；字段策略 Editable |
| `槽182特效号` | `0x2D8` | 1 | `uint8` | 槽182特效号；字段策略 Editable |
| `槽183特效号` | `0x2DC` | 1 | `uint8` | 槽183特效号；字段策略 Editable |
| `槽184特效号` | `0x2E0` | 1 | `uint8` | 槽184特效号；字段策略 Editable |
| `槽185特效号` | `0x2E4` | 1 | `uint8` | 槽185特效号；字段策略 Editable |
| `槽186特效号` | `0x2E8` | 1 | `uint8` | 槽186特效号；字段策略 Editable |
| `槽187特效号` | `0x2EC` | 1 | `uint8` | 槽187特效号；字段策略 Editable |
| `槽188特效号` | `0x2F0` | 1 | `uint8` | 槽188特效号；字段策略 Editable |
| `槽189特效号` | `0x2F4` | 1 | `uint8` | 槽189特效号；字段策略 Editable |
| `槽190特效号` | `0x2F8` | 1 | `uint8` | 槽190特效号；字段策略 Editable |
| `槽191特效号` | `0x2FC` | 1 | `uint8` | 槽191特效号；字段策略 Editable |
| `槽192特效号` | `0x300` | 1 | `uint8` | 槽192特效号；字段策略 Editable |
| `槽193特效号` | `0x304` | 1 | `uint8` | 槽193特效号；字段策略 Editable |
| `槽194特效号` | `0x308` | 1 | `uint8` | 槽194特效号；字段策略 Editable |
| `槽195特效号` | `0x30C` | 1 | `uint8` | 槽195特效号；字段策略 Editable |
| `槽196特效号` | `0x310` | 1 | `uint8` | 槽196特效号；字段策略 Editable |
| `槽197特效号` | `0x314` | 1 | `uint8` | 槽197特效号；字段策略 Editable |
| `槽198特效号` | `0x318` | 1 | `uint8` | 槽198特效号；字段策略 Editable |
| `槽199特效号` | `0x31C` | 1 | `uint8` | 槽199特效号；字段策略 Editable |
| `槽200特效号` | `0x320` | 1 | `uint8` | 槽200特效号；字段策略 Editable |
| `槽201特效号` | `0x324` | 1 | `uint8` | 槽201特效号；字段策略 Editable |
| `槽202特效号` | `0x328` | 1 | `uint8` | 槽202特效号；字段策略 Editable |
| `槽203特效号` | `0x32C` | 1 | `uint8` | 槽203特效号；字段策略 Editable |
| `槽204特效号` | `0x330` | 1 | `uint8` | 槽204特效号；字段策略 Editable |
| `槽205特效号` | `0x334` | 1 | `uint8` | 槽205特效号；字段策略 Editable |
| `槽206特效号` | `0x338` | 1 | `uint8` | 槽206特效号；字段策略 Editable |
| `槽207特效号` | `0x33C` | 1 | `uint8` | 槽207特效号；字段策略 Editable |
| `槽208特效号` | `0x340` | 1 | `uint8` | 槽208特效号；字段策略 Editable |
| `槽209特效号` | `0x344` | 1 | `uint8` | 槽209特效号；字段策略 Editable |
| `槽210特效号` | `0x348` | 1 | `uint8` | 槽210特效号；字段策略 Editable |
| `槽211特效号` | `0x34C` | 1 | `uint8` | 槽211特效号；字段策略 Editable |
| `槽212特效号` | `0x350` | 1 | `uint8` | 槽212特效号；字段策略 Editable |
| `槽213特效号` | `0x354` | 1 | `uint8` | 槽213特效号；字段策略 Editable |
| `槽214特效号` | `0x358` | 1 | `uint8` | 槽214特效号；字段策略 Editable |
| `槽215特效号` | `0x35C` | 1 | `uint8` | 槽215特效号；字段策略 Editable |
| `槽216特效号` | `0x360` | 1 | `uint8` | 槽216特效号；字段策略 Editable |
| `槽217特效号` | `0x364` | 1 | `uint8` | 槽217特效号；字段策略 Editable |
| `槽218特效号` | `0x368` | 1 | `uint8` | 槽218特效号；字段策略 Editable |
| `槽219特效号` | `0x36C` | 1 | `uint8` | 槽219特效号；字段策略 Editable |
| `槽220特效号` | `0x370` | 1 | `uint8` | 槽220特效号；字段策略 Editable |
| `槽221特效号` | `0x374` | 1 | `uint8` | 槽221特效号；字段策略 Editable |
| `槽222特效号` | `0x378` | 1 | `uint8` | 槽222特效号；字段策略 Editable |
| `槽223特效号` | `0x37C` | 1 | `uint8` | 槽223特效号；字段策略 Editable |
| `槽224特效号` | `0x380` | 1 | `uint8` | 槽224特效号；字段策略 Editable |
| `槽225特效号` | `0x384` | 1 | `uint8` | 槽225特效号；字段策略 Editable |
| `槽226特效号` | `0x388` | 1 | `uint8` | 槽226特效号；字段策略 Editable |
| `槽227特效号` | `0x38C` | 1 | `uint8` | 槽227特效号；字段策略 Editable |
| `槽228特效号` | `0x390` | 1 | `uint8` | 槽228特效号；字段策略 Editable |
| `槽229特效号` | `0x394` | 1 | `uint8` | 槽229特效号；字段策略 Editable |
| `槽230特效号` | `0x398` | 1 | `uint8` | 槽230特效号；字段策略 Editable |
| `槽231特效号` | `0x39C` | 1 | `uint8` | 槽231特效号；字段策略 Editable |
| `槽232特效号` | `0x3A0` | 1 | `uint8` | 槽232特效号；字段策略 Editable |
| `槽233特效号` | `0x3A4` | 1 | `uint8` | 槽233特效号；字段策略 Editable |
| `槽234特效号` | `0x3A8` | 1 | `uint8` | 槽234特效号；字段策略 Editable |
| `槽235特效号` | `0x3AC` | 1 | `uint8` | 槽235特效号；字段策略 Editable |
| `槽236特效号` | `0x3B0` | 1 | `uint8` | 槽236特效号；字段策略 Editable |
| `槽237特效号` | `0x3B4` | 1 | `uint8` | 槽237特效号；字段策略 Editable |
| `槽238特效号` | `0x3B8` | 1 | `uint8` | 槽238特效号；字段策略 Editable |
| `槽239特效号` | `0x3BC` | 1 | `uint8` | 槽239特效号；字段策略 Editable |
| `槽240特效号` | `0x3C0` | 1 | `uint8` | 槽240特效号；字段策略 Editable |
| `槽241特效号` | `0x3C4` | 1 | `uint8` | 槽241特效号；字段策略 Editable |
| `槽242特效号` | `0x3C8` | 1 | `uint8` | 槽242特效号；字段策略 Editable |
| `槽243特效号` | `0x3CC` | 1 | `uint8` | 槽243特效号；字段策略 Editable |
| `槽244特效号` | `0x3D0` | 1 | `uint8` | 槽244特效号；字段策略 Editable |
| `槽245特效号` | `0x3D4` | 1 | `uint8` | 槽245特效号；字段策略 Editable |
| `槽246特效号` | `0x3D8` | 1 | `uint8` | 槽246特效号；字段策略 Editable |
| `槽247特效号` | `0x3DC` | 1 | `uint8` | 槽247特效号；字段策略 Editable |
| `槽248特效号` | `0x3E0` | 1 | `uint8` | 槽248特效号；字段策略 Editable |
| `槽249特效号` | `0x3E4` | 1 | `uint8` | 槽249特效号；字段策略 Editable |
| `槽250特效号` | `0x3E8` | 1 | `uint8` | 槽250特效号；字段策略 Editable |
| `槽251特效号` | `0x3EC` | 1 | `uint8` | 槽251特效号；字段策略 Editable |
| `槽252特效号` | `0x3F0` | 1 | `uint8` | 槽252特效号；字段策略 Editable |
| `槽253特效号` | `0x3F4` | 1 | `uint8` | 槽253特效号；字段策略 Editable |
| `槽254特效号` | `0x3F8` | 1 | `uint8` | 槽254特效号；字段策略 Editable |
| `槽255特效号` | `0x3FC` | 1 | `uint8` | 槽255特效号；字段策略 Editable |
| `槽0特效值` | `0x1` | 1 | `uint8` | 槽0特效值；字段策略 Editable |
| `槽1特效值` | `0x5` | 1 | `uint8` | 槽1特效值；字段策略 Editable |
| `槽2特效值` | `0x9` | 1 | `uint8` | 槽2特效值；字段策略 Editable |
| `槽3特效值` | `0xD` | 1 | `uint8` | 槽3特效值；字段策略 Editable |
| `槽4特效值` | `0x11` | 1 | `uint8` | 槽4特效值；字段策略 Editable |
| `槽5特效值` | `0x15` | 1 | `uint8` | 槽5特效值；字段策略 Editable |
| `槽6特效值` | `0x19` | 1 | `uint8` | 槽6特效值；字段策略 Editable |
| `槽7特效值` | `0x1D` | 1 | `uint8` | 槽7特效值；字段策略 Editable |
| `槽8特效值` | `0x21` | 1 | `uint8` | 槽8特效值；字段策略 Editable |
| `槽9特效值` | `0x25` | 1 | `uint8` | 槽9特效值；字段策略 Editable |
| `槽10特效值` | `0x29` | 1 | `uint8` | 槽10特效值；字段策略 Editable |
| `槽11特效值` | `0x2D` | 1 | `uint8` | 槽11特效值；字段策略 Editable |
| `槽12特效值` | `0x31` | 1 | `uint8` | 槽12特效值；字段策略 Editable |
| `槽13特效值` | `0x35` | 1 | `uint8` | 槽13特效值；字段策略 Editable |
| `槽14特效值` | `0x39` | 1 | `uint8` | 槽14特效值；字段策略 Editable |
| `槽15特效值` | `0x3D` | 1 | `uint8` | 槽15特效值；字段策略 Editable |
| `槽16特效值` | `0x41` | 1 | `uint8` | 槽16特效值；字段策略 Editable |
| `槽17特效值` | `0x45` | 1 | `uint8` | 槽17特效值；字段策略 Editable |
| `槽18特效值` | `0x49` | 1 | `uint8` | 槽18特效值；字段策略 Editable |
| `槽19特效值` | `0x4D` | 1 | `uint8` | 槽19特效值；字段策略 Editable |
| `槽20特效值` | `0x51` | 1 | `uint8` | 槽20特效值；字段策略 Editable |
| `槽21特效值` | `0x55` | 1 | `uint8` | 槽21特效值；字段策略 Editable |
| `槽22特效值` | `0x59` | 1 | `uint8` | 槽22特效值；字段策略 Editable |
| `槽23特效值` | `0x5D` | 1 | `uint8` | 槽23特效值；字段策略 Editable |
| `槽24特效值` | `0x61` | 1 | `uint8` | 槽24特效值；字段策略 Editable |
| `槽25特效值` | `0x65` | 1 | `uint8` | 槽25特效值；字段策略 Editable |
| `槽26特效值` | `0x69` | 1 | `uint8` | 槽26特效值；字段策略 Editable |
| `槽27特效值` | `0x6D` | 1 | `uint8` | 槽27特效值；字段策略 Editable |
| `槽28特效值` | `0x71` | 1 | `uint8` | 槽28特效值；字段策略 Editable |
| `槽29特效值` | `0x75` | 1 | `uint8` | 槽29特效值；字段策略 Editable |
| `槽30特效值` | `0x79` | 1 | `uint8` | 槽30特效值；字段策略 Editable |
| `槽31特效值` | `0x7D` | 1 | `uint8` | 槽31特效值；字段策略 Editable |
| `槽32特效值` | `0x81` | 1 | `uint8` | 槽32特效值；字段策略 Editable |
| `槽33特效值` | `0x85` | 1 | `uint8` | 槽33特效值；字段策略 Editable |
| `槽34特效值` | `0x89` | 1 | `uint8` | 槽34特效值；字段策略 Editable |
| `槽35特效值` | `0x8D` | 1 | `uint8` | 槽35特效值；字段策略 Editable |
| `槽36特效值` | `0x91` | 1 | `uint8` | 槽36特效值；字段策略 Editable |
| `槽37特效值` | `0x95` | 1 | `uint8` | 槽37特效值；字段策略 Editable |
| `槽38特效值` | `0x99` | 1 | `uint8` | 槽38特效值；字段策略 Editable |
| `槽39特效值` | `0x9D` | 1 | `uint8` | 槽39特效值；字段策略 Editable |
| `槽40特效值` | `0xA1` | 1 | `uint8` | 槽40特效值；字段策略 Editable |
| `槽41特效值` | `0xA5` | 1 | `uint8` | 槽41特效值；字段策略 Editable |
| `槽42特效值` | `0xA9` | 1 | `uint8` | 槽42特效值；字段策略 Editable |
| `槽43特效值` | `0xAD` | 1 | `uint8` | 槽43特效值；字段策略 Editable |
| `槽44特效值` | `0xB1` | 1 | `uint8` | 槽44特效值；字段策略 Editable |
| `槽45特效值` | `0xB5` | 1 | `uint8` | 槽45特效值；字段策略 Editable |
| `槽46特效值` | `0xB9` | 1 | `uint8` | 槽46特效值；字段策略 Editable |
| `槽47特效值` | `0xBD` | 1 | `uint8` | 槽47特效值；字段策略 Editable |
| `槽48特效值` | `0xC1` | 1 | `uint8` | 槽48特效值；字段策略 Editable |
| `槽49特效值` | `0xC5` | 1 | `uint8` | 槽49特效值；字段策略 Editable |
| `槽50特效值` | `0xC9` | 1 | `uint8` | 槽50特效值；字段策略 Editable |
| `槽51特效值` | `0xCD` | 1 | `uint8` | 槽51特效值；字段策略 Editable |
| `槽52特效值` | `0xD1` | 1 | `uint8` | 槽52特效值；字段策略 Editable |
| `槽53特效值` | `0xD5` | 1 | `uint8` | 槽53特效值；字段策略 Editable |
| `槽54特效值` | `0xD9` | 1 | `uint8` | 槽54特效值；字段策略 Editable |
| `槽55特效值` | `0xDD` | 1 | `uint8` | 槽55特效值；字段策略 Editable |
| `槽56特效值` | `0xE1` | 1 | `uint8` | 槽56特效值；字段策略 Editable |
| `槽57特效值` | `0xE5` | 1 | `uint8` | 槽57特效值；字段策略 Editable |
| `槽58特效值` | `0xE9` | 1 | `uint8` | 槽58特效值；字段策略 Editable |
| `槽59特效值` | `0xED` | 1 | `uint8` | 槽59特效值；字段策略 Editable |
| `槽60特效值` | `0xF1` | 1 | `uint8` | 槽60特效值；字段策略 Editable |
| `槽61特效值` | `0xF5` | 1 | `uint8` | 槽61特效值；字段策略 Editable |
| `槽62特效值` | `0xF9` | 1 | `uint8` | 槽62特效值；字段策略 Editable |
| `槽63特效值` | `0xFD` | 1 | `uint8` | 槽63特效值；字段策略 Editable |
| `槽64特效值` | `0x101` | 1 | `uint8` | 槽64特效值；字段策略 Editable |
| `槽65特效值` | `0x105` | 1 | `uint8` | 槽65特效值；字段策略 Editable |
| `槽66特效值` | `0x109` | 1 | `uint8` | 槽66特效值；字段策略 Editable |
| `槽67特效值` | `0x10D` | 1 | `uint8` | 槽67特效值；字段策略 Editable |
| `槽68特效值` | `0x111` | 1 | `uint8` | 槽68特效值；字段策略 Editable |
| `槽69特效值` | `0x115` | 1 | `uint8` | 槽69特效值；字段策略 Editable |
| `槽70特效值` | `0x119` | 1 | `uint8` | 槽70特效值；字段策略 Editable |
| `槽71特效值` | `0x11D` | 1 | `uint8` | 槽71特效值；字段策略 Editable |
| `槽72特效值` | `0x121` | 1 | `uint8` | 槽72特效值；字段策略 Editable |
| `槽73特效值` | `0x125` | 1 | `uint8` | 槽73特效值；字段策略 Editable |
| `槽74特效值` | `0x129` | 1 | `uint8` | 槽74特效值；字段策略 Editable |
| `槽75特效值` | `0x12D` | 1 | `uint8` | 槽75特效值；字段策略 Editable |
| `槽76特效值` | `0x131` | 1 | `uint8` | 槽76特效值；字段策略 Editable |
| `槽77特效值` | `0x135` | 1 | `uint8` | 槽77特效值；字段策略 Editable |
| `槽78特效值` | `0x139` | 1 | `uint8` | 槽78特效值；字段策略 Editable |
| `槽79特效值` | `0x13D` | 1 | `uint8` | 槽79特效值；字段策略 Editable |
| `槽80特效值` | `0x141` | 1 | `uint8` | 槽80特效值；字段策略 Editable |
| `槽81特效值` | `0x145` | 1 | `uint8` | 槽81特效值；字段策略 Editable |
| `槽82特效值` | `0x149` | 1 | `uint8` | 槽82特效值；字段策略 Editable |
| `槽83特效值` | `0x14D` | 1 | `uint8` | 槽83特效值；字段策略 Editable |
| `槽84特效值` | `0x151` | 1 | `uint8` | 槽84特效值；字段策略 Editable |
| `槽85特效值` | `0x155` | 1 | `uint8` | 槽85特效值；字段策略 Editable |
| `槽86特效值` | `0x159` | 1 | `uint8` | 槽86特效值；字段策略 Editable |
| `槽87特效值` | `0x15D` | 1 | `uint8` | 槽87特效值；字段策略 Editable |
| `槽88特效值` | `0x161` | 1 | `uint8` | 槽88特效值；字段策略 Editable |
| `槽89特效值` | `0x165` | 1 | `uint8` | 槽89特效值；字段策略 Editable |
| `槽90特效值` | `0x169` | 1 | `uint8` | 槽90特效值；字段策略 Editable |
| `槽91特效值` | `0x16D` | 1 | `uint8` | 槽91特效值；字段策略 Editable |
| `槽92特效值` | `0x171` | 1 | `uint8` | 槽92特效值；字段策略 Editable |
| `槽93特效值` | `0x175` | 1 | `uint8` | 槽93特效值；字段策略 Editable |
| `槽94特效值` | `0x179` | 1 | `uint8` | 槽94特效值；字段策略 Editable |
| `槽95特效值` | `0x17D` | 1 | `uint8` | 槽95特效值；字段策略 Editable |
| `槽96特效值` | `0x181` | 1 | `uint8` | 槽96特效值；字段策略 Editable |
| `槽97特效值` | `0x185` | 1 | `uint8` | 槽97特效值；字段策略 Editable |
| `槽98特效值` | `0x189` | 1 | `uint8` | 槽98特效值；字段策略 Editable |
| `槽99特效值` | `0x18D` | 1 | `uint8` | 槽99特效值；字段策略 Editable |
| `槽100特效值` | `0x191` | 1 | `uint8` | 槽100特效值；字段策略 Editable |
| `槽101特效值` | `0x195` | 1 | `uint8` | 槽101特效值；字段策略 Editable |
| `槽102特效值` | `0x199` | 1 | `uint8` | 槽102特效值；字段策略 Editable |
| `槽103特效值` | `0x19D` | 1 | `uint8` | 槽103特效值；字段策略 Editable |
| `槽104特效值` | `0x1A1` | 1 | `uint8` | 槽104特效值；字段策略 Editable |
| `槽105特效值` | `0x1A5` | 1 | `uint8` | 槽105特效值；字段策略 Editable |
| `槽106特效值` | `0x1A9` | 1 | `uint8` | 槽106特效值；字段策略 Editable |
| `槽107特效值` | `0x1AD` | 1 | `uint8` | 槽107特效值；字段策略 Editable |
| `槽108特效值` | `0x1B1` | 1 | `uint8` | 槽108特效值；字段策略 Editable |
| `槽109特效值` | `0x1B5` | 1 | `uint8` | 槽109特效值；字段策略 Editable |
| `槽110特效值` | `0x1B9` | 1 | `uint8` | 槽110特效值；字段策略 Editable |
| `槽111特效值` | `0x1BD` | 1 | `uint8` | 槽111特效值；字段策略 Editable |
| `槽112特效值` | `0x1C1` | 1 | `uint8` | 槽112特效值；字段策略 Editable |
| `槽113特效值` | `0x1C5` | 1 | `uint8` | 槽113特效值；字段策略 Editable |
| `槽114特效值` | `0x1C9` | 1 | `uint8` | 槽114特效值；字段策略 Editable |
| `槽115特效值` | `0x1CD` | 1 | `uint8` | 槽115特效值；字段策略 Editable |
| `槽116特效值` | `0x1D1` | 1 | `uint8` | 槽116特效值；字段策略 Editable |
| `槽117特效值` | `0x1D5` | 1 | `uint8` | 槽117特效值；字段策略 Editable |
| `槽118特效值` | `0x1D9` | 1 | `uint8` | 槽118特效值；字段策略 Editable |
| `槽119特效值` | `0x1DD` | 1 | `uint8` | 槽119特效值；字段策略 Editable |
| `槽120特效值` | `0x1E1` | 1 | `uint8` | 槽120特效值；字段策略 Editable |
| `槽121特效值` | `0x1E5` | 1 | `uint8` | 槽121特效值；字段策略 Editable |
| `槽122特效值` | `0x1E9` | 1 | `uint8` | 槽122特效值；字段策略 Editable |
| `槽123特效值` | `0x1ED` | 1 | `uint8` | 槽123特效值；字段策略 Editable |
| `槽124特效值` | `0x1F1` | 1 | `uint8` | 槽124特效值；字段策略 Editable |
| `槽125特效值` | `0x1F5` | 1 | `uint8` | 槽125特效值；字段策略 Editable |
| `槽126特效值` | `0x1F9` | 1 | `uint8` | 槽126特效值；字段策略 Editable |
| `槽127特效值` | `0x1FD` | 1 | `uint8` | 槽127特效值；字段策略 Editable |
| `槽128特效值` | `0x201` | 1 | `uint8` | 槽128特效值；字段策略 Editable |
| `槽129特效值` | `0x205` | 1 | `uint8` | 槽129特效值；字段策略 Editable |
| `槽130特效值` | `0x209` | 1 | `uint8` | 槽130特效值；字段策略 Editable |
| `槽131特效值` | `0x20D` | 1 | `uint8` | 槽131特效值；字段策略 Editable |
| `槽132特效值` | `0x211` | 1 | `uint8` | 槽132特效值；字段策略 Editable |
| `槽133特效值` | `0x215` | 1 | `uint8` | 槽133特效值；字段策略 Editable |
| `槽134特效值` | `0x219` | 1 | `uint8` | 槽134特效值；字段策略 Editable |
| `槽135特效值` | `0x21D` | 1 | `uint8` | 槽135特效值；字段策略 Editable |
| `槽136特效值` | `0x221` | 1 | `uint8` | 槽136特效值；字段策略 Editable |
| `槽137特效值` | `0x225` | 1 | `uint8` | 槽137特效值；字段策略 Editable |
| `槽138特效值` | `0x229` | 1 | `uint8` | 槽138特效值；字段策略 Editable |
| `槽139特效值` | `0x22D` | 1 | `uint8` | 槽139特效值；字段策略 Editable |
| `槽140特效值` | `0x231` | 1 | `uint8` | 槽140特效值；字段策略 Editable |
| `槽141特效值` | `0x235` | 1 | `uint8` | 槽141特效值；字段策略 Editable |
| `槽142特效值` | `0x239` | 1 | `uint8` | 槽142特效值；字段策略 Editable |
| `槽143特效值` | `0x23D` | 1 | `uint8` | 槽143特效值；字段策略 Editable |
| `槽144特效值` | `0x241` | 1 | `uint8` | 槽144特效值；字段策略 Editable |
| `槽145特效值` | `0x245` | 1 | `uint8` | 槽145特效值；字段策略 Editable |
| `槽146特效值` | `0x249` | 1 | `uint8` | 槽146特效值；字段策略 Editable |
| `槽147特效值` | `0x24D` | 1 | `uint8` | 槽147特效值；字段策略 Editable |
| `槽148特效值` | `0x251` | 1 | `uint8` | 槽148特效值；字段策略 Editable |
| `槽149特效值` | `0x255` | 1 | `uint8` | 槽149特效值；字段策略 Editable |
| `槽150特效值` | `0x259` | 1 | `uint8` | 槽150特效值；字段策略 Editable |
| `槽151特效值` | `0x25D` | 1 | `uint8` | 槽151特效值；字段策略 Editable |
| `槽152特效值` | `0x261` | 1 | `uint8` | 槽152特效值；字段策略 Editable |
| `槽153特效值` | `0x265` | 1 | `uint8` | 槽153特效值；字段策略 Editable |
| `槽154特效值` | `0x269` | 1 | `uint8` | 槽154特效值；字段策略 Editable |
| `槽155特效值` | `0x26D` | 1 | `uint8` | 槽155特效值；字段策略 Editable |
| `槽156特效值` | `0x271` | 1 | `uint8` | 槽156特效值；字段策略 Editable |
| `槽157特效值` | `0x275` | 1 | `uint8` | 槽157特效值；字段策略 Editable |
| `槽158特效值` | `0x279` | 1 | `uint8` | 槽158特效值；字段策略 Editable |
| `槽159特效值` | `0x27D` | 1 | `uint8` | 槽159特效值；字段策略 Editable |
| `槽160特效值` | `0x281` | 1 | `uint8` | 槽160特效值；字段策略 Editable |
| `槽161特效值` | `0x285` | 1 | `uint8` | 槽161特效值；字段策略 Editable |
| `槽162特效值` | `0x289` | 1 | `uint8` | 槽162特效值；字段策略 Editable |
| `槽163特效值` | `0x28D` | 1 | `uint8` | 槽163特效值；字段策略 Editable |
| `槽164特效值` | `0x291` | 1 | `uint8` | 槽164特效值；字段策略 Editable |
| `槽165特效值` | `0x295` | 1 | `uint8` | 槽165特效值；字段策略 Editable |
| `槽166特效值` | `0x299` | 1 | `uint8` | 槽166特效值；字段策略 Editable |
| `槽167特效值` | `0x29D` | 1 | `uint8` | 槽167特效值；字段策略 Editable |
| `槽168特效值` | `0x2A1` | 1 | `uint8` | 槽168特效值；字段策略 Editable |
| `槽169特效值` | `0x2A5` | 1 | `uint8` | 槽169特效值；字段策略 Editable |
| `槽170特效值` | `0x2A9` | 1 | `uint8` | 槽170特效值；字段策略 Editable |
| `槽171特效值` | `0x2AD` | 1 | `uint8` | 槽171特效值；字段策略 Editable |
| `槽172特效值` | `0x2B1` | 1 | `uint8` | 槽172特效值；字段策略 Editable |
| `槽173特效值` | `0x2B5` | 1 | `uint8` | 槽173特效值；字段策略 Editable |
| `槽174特效值` | `0x2B9` | 1 | `uint8` | 槽174特效值；字段策略 Editable |
| `槽175特效值` | `0x2BD` | 1 | `uint8` | 槽175特效值；字段策略 Editable |
| `槽176特效值` | `0x2C1` | 1 | `uint8` | 槽176特效值；字段策略 Editable |
| `槽177特效值` | `0x2C5` | 1 | `uint8` | 槽177特效值；字段策略 Editable |
| `槽178特效值` | `0x2C9` | 1 | `uint8` | 槽178特效值；字段策略 Editable |
| `槽179特效值` | `0x2CD` | 1 | `uint8` | 槽179特效值；字段策略 Editable |
| `槽180特效值` | `0x2D1` | 1 | `uint8` | 槽180特效值；字段策略 Editable |
| `槽181特效值` | `0x2D5` | 1 | `uint8` | 槽181特效值；字段策略 Editable |
| `槽182特效值` | `0x2D9` | 1 | `uint8` | 槽182特效值；字段策略 Editable |
| `槽183特效值` | `0x2DD` | 1 | `uint8` | 槽183特效值；字段策略 Editable |
| `槽184特效值` | `0x2E1` | 1 | `uint8` | 槽184特效值；字段策略 Editable |
| `槽185特效值` | `0x2E5` | 1 | `uint8` | 槽185特效值；字段策略 Editable |
| `槽186特效值` | `0x2E9` | 1 | `uint8` | 槽186特效值；字段策略 Editable |
| `槽187特效值` | `0x2ED` | 1 | `uint8` | 槽187特效值；字段策略 Editable |
| `槽188特效值` | `0x2F1` | 1 | `uint8` | 槽188特效值；字段策略 Editable |
| `槽189特效值` | `0x2F5` | 1 | `uint8` | 槽189特效值；字段策略 Editable |
| `槽190特效值` | `0x2F9` | 1 | `uint8` | 槽190特效值；字段策略 Editable |
| `槽191特效值` | `0x2FD` | 1 | `uint8` | 槽191特效值；字段策略 Editable |
| `槽192特效值` | `0x301` | 1 | `uint8` | 槽192特效值；字段策略 Editable |
| `槽193特效值` | `0x305` | 1 | `uint8` | 槽193特效值；字段策略 Editable |
| `槽194特效值` | `0x309` | 1 | `uint8` | 槽194特效值；字段策略 Editable |
| `槽195特效值` | `0x30D` | 1 | `uint8` | 槽195特效值；字段策略 Editable |
| `槽196特效值` | `0x311` | 1 | `uint8` | 槽196特效值；字段策略 Editable |
| `槽197特效值` | `0x315` | 1 | `uint8` | 槽197特效值；字段策略 Editable |
| `槽198特效值` | `0x319` | 1 | `uint8` | 槽198特效值；字段策略 Editable |
| `槽199特效值` | `0x31D` | 1 | `uint8` | 槽199特效值；字段策略 Editable |
| `槽200特效值` | `0x321` | 1 | `uint8` | 槽200特效值；字段策略 Editable |
| `槽201特效值` | `0x325` | 1 | `uint8` | 槽201特效值；字段策略 Editable |
| `槽202特效值` | `0x329` | 1 | `uint8` | 槽202特效值；字段策略 Editable |
| `槽203特效值` | `0x32D` | 1 | `uint8` | 槽203特效值；字段策略 Editable |
| `槽204特效值` | `0x331` | 1 | `uint8` | 槽204特效值；字段策略 Editable |
| `槽205特效值` | `0x335` | 1 | `uint8` | 槽205特效值；字段策略 Editable |
| `槽206特效值` | `0x339` | 1 | `uint8` | 槽206特效值；字段策略 Editable |
| `槽207特效值` | `0x33D` | 1 | `uint8` | 槽207特效值；字段策略 Editable |
| `槽208特效值` | `0x341` | 1 | `uint8` | 槽208特效值；字段策略 Editable |
| `槽209特效值` | `0x345` | 1 | `uint8` | 槽209特效值；字段策略 Editable |
| `槽210特效值` | `0x349` | 1 | `uint8` | 槽210特效值；字段策略 Editable |
| `槽211特效值` | `0x34D` | 1 | `uint8` | 槽211特效值；字段策略 Editable |
| `槽212特效值` | `0x351` | 1 | `uint8` | 槽212特效值；字段策略 Editable |
| `槽213特效值` | `0x355` | 1 | `uint8` | 槽213特效值；字段策略 Editable |
| `槽214特效值` | `0x359` | 1 | `uint8` | 槽214特效值；字段策略 Editable |
| `槽215特效值` | `0x35D` | 1 | `uint8` | 槽215特效值；字段策略 Editable |
| `槽216特效值` | `0x361` | 1 | `uint8` | 槽216特效值；字段策略 Editable |
| `槽217特效值` | `0x365` | 1 | `uint8` | 槽217特效值；字段策略 Editable |
| `槽218特效值` | `0x369` | 1 | `uint8` | 槽218特效值；字段策略 Editable |
| `槽219特效值` | `0x36D` | 1 | `uint8` | 槽219特效值；字段策略 Editable |
| `槽220特效值` | `0x371` | 1 | `uint8` | 槽220特效值；字段策略 Editable |
| `槽221特效值` | `0x375` | 1 | `uint8` | 槽221特效值；字段策略 Editable |
| `槽222特效值` | `0x379` | 1 | `uint8` | 槽222特效值；字段策略 Editable |
| `槽223特效值` | `0x37D` | 1 | `uint8` | 槽223特效值；字段策略 Editable |
| `槽224特效值` | `0x381` | 1 | `uint8` | 槽224特效值；字段策略 Editable |
| `槽225特效值` | `0x385` | 1 | `uint8` | 槽225特效值；字段策略 Editable |
| `槽226特效值` | `0x389` | 1 | `uint8` | 槽226特效值；字段策略 Editable |
| `槽227特效值` | `0x38D` | 1 | `uint8` | 槽227特效值；字段策略 Editable |
| `槽228特效值` | `0x391` | 1 | `uint8` | 槽228特效值；字段策略 Editable |
| `槽229特效值` | `0x395` | 1 | `uint8` | 槽229特效值；字段策略 Editable |
| `槽230特效值` | `0x399` | 1 | `uint8` | 槽230特效值；字段策略 Editable |
| `槽231特效值` | `0x39D` | 1 | `uint8` | 槽231特效值；字段策略 Editable |
| `槽232特效值` | `0x3A1` | 1 | `uint8` | 槽232特效值；字段策略 Editable |
| `槽233特效值` | `0x3A5` | 1 | `uint8` | 槽233特效值；字段策略 Editable |
| `槽234特效值` | `0x3A9` | 1 | `uint8` | 槽234特效值；字段策略 Editable |
| `槽235特效值` | `0x3AD` | 1 | `uint8` | 槽235特效值；字段策略 Editable |
| `槽236特效值` | `0x3B1` | 1 | `uint8` | 槽236特效值；字段策略 Editable |
| `槽237特效值` | `0x3B5` | 1 | `uint8` | 槽237特效值；字段策略 Editable |
| `槽238特效值` | `0x3B9` | 1 | `uint8` | 槽238特效值；字段策略 Editable |
| `槽239特效值` | `0x3BD` | 1 | `uint8` | 槽239特效值；字段策略 Editable |
| `槽240特效值` | `0x3C1` | 1 | `uint8` | 槽240特效值；字段策略 Editable |
| `槽241特效值` | `0x3C5` | 1 | `uint8` | 槽241特效值；字段策略 Editable |
| `槽242特效值` | `0x3C9` | 1 | `uint8` | 槽242特效值；字段策略 Editable |
| `槽243特效值` | `0x3CD` | 1 | `uint8` | 槽243特效值；字段策略 Editable |
| `槽244特效值` | `0x3D1` | 1 | `uint8` | 槽244特效值；字段策略 Editable |
| `槽245特效值` | `0x3D5` | 1 | `uint8` | 槽245特效值；字段策略 Editable |
| `槽246特效值` | `0x3D9` | 1 | `uint8` | 槽246特效值；字段策略 Editable |
| `槽247特效值` | `0x3DD` | 1 | `uint8` | 槽247特效值；字段策略 Editable |
| `槽248特效值` | `0x3E1` | 1 | `uint8` | 槽248特效值；字段策略 Editable |
| `槽249特效值` | `0x3E5` | 1 | `uint8` | 槽249特效值；字段策略 Editable |
| `槽250特效值` | `0x3E9` | 1 | `uint8` | 槽250特效值；字段策略 Editable |
| `槽251特效值` | `0x3ED` | 1 | `uint8` | 槽251特效值；字段策略 Editable |
| `槽252特效值` | `0x3F1` | 1 | `uint8` | 槽252特效值；字段策略 Editable |
| `槽253特效值` | `0x3F5` | 1 | `uint8` | 槽253特效值；字段策略 Editable |
| `槽254特效值` | `0x3F9` | 1 | `uint8` | 槽254特效值；字段策略 Editable |
| `槽255特效值` | `0x3FD` | 1 | `uint8` | 槽255特效值；字段策略 Editable |
| `槽0经验` | `0x2` | 1 | `uint8` | 槽0经验；字段策略 Editable |
| `槽1经验` | `0x6` | 1 | `uint8` | 槽1经验；字段策略 Editable |
| `槽2经验` | `0xA` | 1 | `uint8` | 槽2经验；字段策略 Editable |
| `槽3经验` | `0xE` | 1 | `uint8` | 槽3经验；字段策略 Editable |
| `槽4经验` | `0x12` | 1 | `uint8` | 槽4经验；字段策略 Editable |
| `槽5经验` | `0x16` | 1 | `uint8` | 槽5经验；字段策略 Editable |
| `槽6经验` | `0x1A` | 1 | `uint8` | 槽6经验；字段策略 Editable |
| `槽7经验` | `0x1E` | 1 | `uint8` | 槽7经验；字段策略 Editable |
| `槽8经验` | `0x22` | 1 | `uint8` | 槽8经验；字段策略 Editable |
| `槽9经验` | `0x26` | 1 | `uint8` | 槽9经验；字段策略 Editable |
| `槽10经验` | `0x2A` | 1 | `uint8` | 槽10经验；字段策略 Editable |
| `槽11经验` | `0x2E` | 1 | `uint8` | 槽11经验；字段策略 Editable |
| `槽12经验` | `0x32` | 1 | `uint8` | 槽12经验；字段策略 Editable |
| `槽13经验` | `0x36` | 1 | `uint8` | 槽13经验；字段策略 Editable |
| `槽14经验` | `0x3A` | 1 | `uint8` | 槽14经验；字段策略 Editable |
| `槽15经验` | `0x3E` | 1 | `uint8` | 槽15经验；字段策略 Editable |
| `槽16经验` | `0x42` | 1 | `uint8` | 槽16经验；字段策略 Editable |
| `槽17经验` | `0x46` | 1 | `uint8` | 槽17经验；字段策略 Editable |
| `槽18经验` | `0x4A` | 1 | `uint8` | 槽18经验；字段策略 Editable |
| `槽19经验` | `0x4E` | 1 | `uint8` | 槽19经验；字段策略 Editable |
| `槽20经验` | `0x52` | 1 | `uint8` | 槽20经验；字段策略 Editable |
| `槽21经验` | `0x56` | 1 | `uint8` | 槽21经验；字段策略 Editable |
| `槽22经验` | `0x5A` | 1 | `uint8` | 槽22经验；字段策略 Editable |
| `槽23经验` | `0x5E` | 1 | `uint8` | 槽23经验；字段策略 Editable |
| `槽24经验` | `0x62` | 1 | `uint8` | 槽24经验；字段策略 Editable |
| `槽25经验` | `0x66` | 1 | `uint8` | 槽25经验；字段策略 Editable |
| `槽26经验` | `0x6A` | 1 | `uint8` | 槽26经验；字段策略 Editable |
| `槽27经验` | `0x6E` | 1 | `uint8` | 槽27经验；字段策略 Editable |
| `槽28经验` | `0x72` | 1 | `uint8` | 槽28经验；字段策略 Editable |
| `槽29经验` | `0x76` | 1 | `uint8` | 槽29经验；字段策略 Editable |
| `槽30经验` | `0x7A` | 1 | `uint8` | 槽30经验；字段策略 Editable |
| `槽31经验` | `0x7E` | 1 | `uint8` | 槽31经验；字段策略 Editable |
| `槽32经验` | `0x82` | 1 | `uint8` | 槽32经验；字段策略 Editable |
| `槽33经验` | `0x86` | 1 | `uint8` | 槽33经验；字段策略 Editable |
| `槽34经验` | `0x8A` | 1 | `uint8` | 槽34经验；字段策略 Editable |
| `槽35经验` | `0x8E` | 1 | `uint8` | 槽35经验；字段策略 Editable |
| `槽36经验` | `0x92` | 1 | `uint8` | 槽36经验；字段策略 Editable |
| `槽37经验` | `0x96` | 1 | `uint8` | 槽37经验；字段策略 Editable |
| `槽38经验` | `0x9A` | 1 | `uint8` | 槽38经验；字段策略 Editable |
| `槽39经验` | `0x9E` | 1 | `uint8` | 槽39经验；字段策略 Editable |
| `槽40经验` | `0xA2` | 1 | `uint8` | 槽40经验；字段策略 Editable |
| `槽41经验` | `0xA6` | 1 | `uint8` | 槽41经验；字段策略 Editable |
| `槽42经验` | `0xAA` | 1 | `uint8` | 槽42经验；字段策略 Editable |
| `槽43经验` | `0xAE` | 1 | `uint8` | 槽43经验；字段策略 Editable |
| `槽44经验` | `0xB2` | 1 | `uint8` | 槽44经验；字段策略 Editable |
| `槽45经验` | `0xB6` | 1 | `uint8` | 槽45经验；字段策略 Editable |
| `槽46经验` | `0xBA` | 1 | `uint8` | 槽46经验；字段策略 Editable |
| `槽47经验` | `0xBE` | 1 | `uint8` | 槽47经验；字段策略 Editable |
| `槽48经验` | `0xC2` | 1 | `uint8` | 槽48经验；字段策略 Editable |
| `槽49经验` | `0xC6` | 1 | `uint8` | 槽49经验；字段策略 Editable |
| `槽50经验` | `0xCA` | 1 | `uint8` | 槽50经验；字段策略 Editable |
| `槽51经验` | `0xCE` | 1 | `uint8` | 槽51经验；字段策略 Editable |
| `槽52经验` | `0xD2` | 1 | `uint8` | 槽52经验；字段策略 Editable |
| `槽53经验` | `0xD6` | 1 | `uint8` | 槽53经验；字段策略 Editable |
| `槽54经验` | `0xDA` | 1 | `uint8` | 槽54经验；字段策略 Editable |
| `槽55经验` | `0xDE` | 1 | `uint8` | 槽55经验；字段策略 Editable |
| `槽56经验` | `0xE2` | 1 | `uint8` | 槽56经验；字段策略 Editable |
| `槽57经验` | `0xE6` | 1 | `uint8` | 槽57经验；字段策略 Editable |
| `槽58经验` | `0xEA` | 1 | `uint8` | 槽58经验；字段策略 Editable |
| `槽59经验` | `0xEE` | 1 | `uint8` | 槽59经验；字段策略 Editable |
| `槽60经验` | `0xF2` | 1 | `uint8` | 槽60经验；字段策略 Editable |
| `槽61经验` | `0xF6` | 1 | `uint8` | 槽61经验；字段策略 Editable |
| `槽62经验` | `0xFA` | 1 | `uint8` | 槽62经验；字段策略 Editable |
| `槽63经验` | `0xFE` | 1 | `uint8` | 槽63经验；字段策略 Editable |
| `槽64经验` | `0x102` | 1 | `uint8` | 槽64经验；字段策略 Editable |
| `槽65经验` | `0x106` | 1 | `uint8` | 槽65经验；字段策略 Editable |
| `槽66经验` | `0x10A` | 1 | `uint8` | 槽66经验；字段策略 Editable |
| `槽67经验` | `0x10E` | 1 | `uint8` | 槽67经验；字段策略 Editable |
| `槽68经验` | `0x112` | 1 | `uint8` | 槽68经验；字段策略 Editable |
| `槽69经验` | `0x116` | 1 | `uint8` | 槽69经验；字段策略 Editable |
| `槽70经验` | `0x11A` | 1 | `uint8` | 槽70经验；字段策略 Editable |
| `槽71经验` | `0x11E` | 1 | `uint8` | 槽71经验；字段策略 Editable |
| `槽72经验` | `0x122` | 1 | `uint8` | 槽72经验；字段策略 Editable |
| `槽73经验` | `0x126` | 1 | `uint8` | 槽73经验；字段策略 Editable |
| `槽74经验` | `0x12A` | 1 | `uint8` | 槽74经验；字段策略 Editable |
| `槽75经验` | `0x12E` | 1 | `uint8` | 槽75经验；字段策略 Editable |
| `槽76经验` | `0x132` | 1 | `uint8` | 槽76经验；字段策略 Editable |
| `槽77经验` | `0x136` | 1 | `uint8` | 槽77经验；字段策略 Editable |
| `槽78经验` | `0x13A` | 1 | `uint8` | 槽78经验；字段策略 Editable |
| `槽79经验` | `0x13E` | 1 | `uint8` | 槽79经验；字段策略 Editable |
| `槽80经验` | `0x142` | 1 | `uint8` | 槽80经验；字段策略 Editable |
| `槽81经验` | `0x146` | 1 | `uint8` | 槽81经验；字段策略 Editable |
| `槽82经验` | `0x14A` | 1 | `uint8` | 槽82经验；字段策略 Editable |
| `槽83经验` | `0x14E` | 1 | `uint8` | 槽83经验；字段策略 Editable |
| `槽84经验` | `0x152` | 1 | `uint8` | 槽84经验；字段策略 Editable |
| `槽85经验` | `0x156` | 1 | `uint8` | 槽85经验；字段策略 Editable |
| `槽86经验` | `0x15A` | 1 | `uint8` | 槽86经验；字段策略 Editable |
| `槽87经验` | `0x15E` | 1 | `uint8` | 槽87经验；字段策略 Editable |
| `槽88经验` | `0x162` | 1 | `uint8` | 槽88经验；字段策略 Editable |
| `槽89经验` | `0x166` | 1 | `uint8` | 槽89经验；字段策略 Editable |
| `槽90经验` | `0x16A` | 1 | `uint8` | 槽90经验；字段策略 Editable |
| `槽91经验` | `0x16E` | 1 | `uint8` | 槽91经验；字段策略 Editable |
| `槽92经验` | `0x172` | 1 | `uint8` | 槽92经验；字段策略 Editable |
| `槽93经验` | `0x176` | 1 | `uint8` | 槽93经验；字段策略 Editable |
| `槽94经验` | `0x17A` | 1 | `uint8` | 槽94经验；字段策略 Editable |
| `槽95经验` | `0x17E` | 1 | `uint8` | 槽95经验；字段策略 Editable |
| `槽96经验` | `0x182` | 1 | `uint8` | 槽96经验；字段策略 Editable |
| `槽97经验` | `0x186` | 1 | `uint8` | 槽97经验；字段策略 Editable |
| `槽98经验` | `0x18A` | 1 | `uint8` | 槽98经验；字段策略 Editable |
| `槽99经验` | `0x18E` | 1 | `uint8` | 槽99经验；字段策略 Editable |
| `槽100经验` | `0x192` | 1 | `uint8` | 槽100经验；字段策略 Editable |
| `槽101经验` | `0x196` | 1 | `uint8` | 槽101经验；字段策略 Editable |
| `槽102经验` | `0x19A` | 1 | `uint8` | 槽102经验；字段策略 Editable |
| `槽103经验` | `0x19E` | 1 | `uint8` | 槽103经验；字段策略 Editable |
| `槽104经验` | `0x1A2` | 1 | `uint8` | 槽104经验；字段策略 Editable |
| `槽105经验` | `0x1A6` | 1 | `uint8` | 槽105经验；字段策略 Editable |
| `槽106经验` | `0x1AA` | 1 | `uint8` | 槽106经验；字段策略 Editable |
| `槽107经验` | `0x1AE` | 1 | `uint8` | 槽107经验；字段策略 Editable |
| `槽108经验` | `0x1B2` | 1 | `uint8` | 槽108经验；字段策略 Editable |
| `槽109经验` | `0x1B6` | 1 | `uint8` | 槽109经验；字段策略 Editable |
| `槽110经验` | `0x1BA` | 1 | `uint8` | 槽110经验；字段策略 Editable |
| `槽111经验` | `0x1BE` | 1 | `uint8` | 槽111经验；字段策略 Editable |
| `槽112经验` | `0x1C2` | 1 | `uint8` | 槽112经验；字段策略 Editable |
| `槽113经验` | `0x1C6` | 1 | `uint8` | 槽113经验；字段策略 Editable |
| `槽114经验` | `0x1CA` | 1 | `uint8` | 槽114经验；字段策略 Editable |
| `槽115经验` | `0x1CE` | 1 | `uint8` | 槽115经验；字段策略 Editable |
| `槽116经验` | `0x1D2` | 1 | `uint8` | 槽116经验；字段策略 Editable |
| `槽117经验` | `0x1D6` | 1 | `uint8` | 槽117经验；字段策略 Editable |
| `槽118经验` | `0x1DA` | 1 | `uint8` | 槽118经验；字段策略 Editable |
| `槽119经验` | `0x1DE` | 1 | `uint8` | 槽119经验；字段策略 Editable |
| `槽120经验` | `0x1E2` | 1 | `uint8` | 槽120经验；字段策略 Editable |
| `槽121经验` | `0x1E6` | 1 | `uint8` | 槽121经验；字段策略 Editable |
| `槽122经验` | `0x1EA` | 1 | `uint8` | 槽122经验；字段策略 Editable |
| `槽123经验` | `0x1EE` | 1 | `uint8` | 槽123经验；字段策略 Editable |
| `槽124经验` | `0x1F2` | 1 | `uint8` | 槽124经验；字段策略 Editable |
| `槽125经验` | `0x1F6` | 1 | `uint8` | 槽125经验；字段策略 Editable |
| `槽126经验` | `0x1FA` | 1 | `uint8` | 槽126经验；字段策略 Editable |
| `槽127经验` | `0x1FE` | 1 | `uint8` | 槽127经验；字段策略 Editable |
| `槽128经验` | `0x202` | 1 | `uint8` | 槽128经验；字段策略 Editable |
| `槽129经验` | `0x206` | 1 | `uint8` | 槽129经验；字段策略 Editable |
| `槽130经验` | `0x20A` | 1 | `uint8` | 槽130经验；字段策略 Editable |
| `槽131经验` | `0x20E` | 1 | `uint8` | 槽131经验；字段策略 Editable |
| `槽132经验` | `0x212` | 1 | `uint8` | 槽132经验；字段策略 Editable |
| `槽133经验` | `0x216` | 1 | `uint8` | 槽133经验；字段策略 Editable |
| `槽134经验` | `0x21A` | 1 | `uint8` | 槽134经验；字段策略 Editable |
| `槽135经验` | `0x21E` | 1 | `uint8` | 槽135经验；字段策略 Editable |
| `槽136经验` | `0x222` | 1 | `uint8` | 槽136经验；字段策略 Editable |
| `槽137经验` | `0x226` | 1 | `uint8` | 槽137经验；字段策略 Editable |
| `槽138经验` | `0x22A` | 1 | `uint8` | 槽138经验；字段策略 Editable |
| `槽139经验` | `0x22E` | 1 | `uint8` | 槽139经验；字段策略 Editable |
| `槽140经验` | `0x232` | 1 | `uint8` | 槽140经验；字段策略 Editable |
| `槽141经验` | `0x236` | 1 | `uint8` | 槽141经验；字段策略 Editable |
| `槽142经验` | `0x23A` | 1 | `uint8` | 槽142经验；字段策略 Editable |
| `槽143经验` | `0x23E` | 1 | `uint8` | 槽143经验；字段策略 Editable |
| `槽144经验` | `0x242` | 1 | `uint8` | 槽144经验；字段策略 Editable |
| `槽145经验` | `0x246` | 1 | `uint8` | 槽145经验；字段策略 Editable |
| `槽146经验` | `0x24A` | 1 | `uint8` | 槽146经验；字段策略 Editable |
| `槽147经验` | `0x24E` | 1 | `uint8` | 槽147经验；字段策略 Editable |
| `槽148经验` | `0x252` | 1 | `uint8` | 槽148经验；字段策略 Editable |
| `槽149经验` | `0x256` | 1 | `uint8` | 槽149经验；字段策略 Editable |
| `槽150经验` | `0x25A` | 1 | `uint8` | 槽150经验；字段策略 Editable |
| `槽151经验` | `0x25E` | 1 | `uint8` | 槽151经验；字段策略 Editable |
| `槽152经验` | `0x262` | 1 | `uint8` | 槽152经验；字段策略 Editable |
| `槽153经验` | `0x266` | 1 | `uint8` | 槽153经验；字段策略 Editable |
| `槽154经验` | `0x26A` | 1 | `uint8` | 槽154经验；字段策略 Editable |
| `槽155经验` | `0x26E` | 1 | `uint8` | 槽155经验；字段策略 Editable |
| `槽156经验` | `0x272` | 1 | `uint8` | 槽156经验；字段策略 Editable |
| `槽157经验` | `0x276` | 1 | `uint8` | 槽157经验；字段策略 Editable |
| `槽158经验` | `0x27A` | 1 | `uint8` | 槽158经验；字段策略 Editable |
| `槽159经验` | `0x27E` | 1 | `uint8` | 槽159经验；字段策略 Editable |
| `槽160经验` | `0x282` | 1 | `uint8` | 槽160经验；字段策略 Editable |
| `槽161经验` | `0x286` | 1 | `uint8` | 槽161经验；字段策略 Editable |
| `槽162经验` | `0x28A` | 1 | `uint8` | 槽162经验；字段策略 Editable |
| `槽163经验` | `0x28E` | 1 | `uint8` | 槽163经验；字段策略 Editable |
| `槽164经验` | `0x292` | 1 | `uint8` | 槽164经验；字段策略 Editable |
| `槽165经验` | `0x296` | 1 | `uint8` | 槽165经验；字段策略 Editable |
| `槽166经验` | `0x29A` | 1 | `uint8` | 槽166经验；字段策略 Editable |
| `槽167经验` | `0x29E` | 1 | `uint8` | 槽167经验；字段策略 Editable |
| `槽168经验` | `0x2A2` | 1 | `uint8` | 槽168经验；字段策略 Editable |
| `槽169经验` | `0x2A6` | 1 | `uint8` | 槽169经验；字段策略 Editable |
| `槽170经验` | `0x2AA` | 1 | `uint8` | 槽170经验；字段策略 Editable |
| `槽171经验` | `0x2AE` | 1 | `uint8` | 槽171经验；字段策略 Editable |
| `槽172经验` | `0x2B2` | 1 | `uint8` | 槽172经验；字段策略 Editable |
| `槽173经验` | `0x2B6` | 1 | `uint8` | 槽173经验；字段策略 Editable |
| `槽174经验` | `0x2BA` | 1 | `uint8` | 槽174经验；字段策略 Editable |
| `槽175经验` | `0x2BE` | 1 | `uint8` | 槽175经验；字段策略 Editable |
| `槽176经验` | `0x2C2` | 1 | `uint8` | 槽176经验；字段策略 Editable |
| `槽177经验` | `0x2C6` | 1 | `uint8` | 槽177经验；字段策略 Editable |
| `槽178经验` | `0x2CA` | 1 | `uint8` | 槽178经验；字段策略 Editable |
| `槽179经验` | `0x2CE` | 1 | `uint8` | 槽179经验；字段策略 Editable |
| `槽180经验` | `0x2D2` | 1 | `uint8` | 槽180经验；字段策略 Editable |
| `槽181经验` | `0x2D6` | 1 | `uint8` | 槽181经验；字段策略 Editable |
| `槽182经验` | `0x2DA` | 1 | `uint8` | 槽182经验；字段策略 Editable |
| `槽183经验` | `0x2DE` | 1 | `uint8` | 槽183经验；字段策略 Editable |
| `槽184经验` | `0x2E2` | 1 | `uint8` | 槽184经验；字段策略 Editable |
| `槽185经验` | `0x2E6` | 1 | `uint8` | 槽185经验；字段策略 Editable |
| `槽186经验` | `0x2EA` | 1 | `uint8` | 槽186经验；字段策略 Editable |
| `槽187经验` | `0x2EE` | 1 | `uint8` | 槽187经验；字段策略 Editable |
| `槽188经验` | `0x2F2` | 1 | `uint8` | 槽188经验；字段策略 Editable |
| `槽189经验` | `0x2F6` | 1 | `uint8` | 槽189经验；字段策略 Editable |
| `槽190经验` | `0x2FA` | 1 | `uint8` | 槽190经验；字段策略 Editable |
| `槽191经验` | `0x2FE` | 1 | `uint8` | 槽191经验；字段策略 Editable |
| `槽192经验` | `0x302` | 1 | `uint8` | 槽192经验；字段策略 Editable |
| `槽193经验` | `0x306` | 1 | `uint8` | 槽193经验；字段策略 Editable |
| `槽194经验` | `0x30A` | 1 | `uint8` | 槽194经验；字段策略 Editable |
| `槽195经验` | `0x30E` | 1 | `uint8` | 槽195经验；字段策略 Editable |
| `槽196经验` | `0x312` | 1 | `uint8` | 槽196经验；字段策略 Editable |
| `槽197经验` | `0x316` | 1 | `uint8` | 槽197经验；字段策略 Editable |
| `槽198经验` | `0x31A` | 1 | `uint8` | 槽198经验；字段策略 Editable |
| `槽199经验` | `0x31E` | 1 | `uint8` | 槽199经验；字段策略 Editable |
| `槽200经验` | `0x322` | 1 | `uint8` | 槽200经验；字段策略 Editable |
| `槽201经验` | `0x326` | 1 | `uint8` | 槽201经验；字段策略 Editable |
| `槽202经验` | `0x32A` | 1 | `uint8` | 槽202经验；字段策略 Editable |
| `槽203经验` | `0x32E` | 1 | `uint8` | 槽203经验；字段策略 Editable |
| `槽204经验` | `0x332` | 1 | `uint8` | 槽204经验；字段策略 Editable |
| `槽205经验` | `0x336` | 1 | `uint8` | 槽205经验；字段策略 Editable |
| `槽206经验` | `0x33A` | 1 | `uint8` | 槽206经验；字段策略 Editable |
| `槽207经验` | `0x33E` | 1 | `uint8` | 槽207经验；字段策略 Editable |
| `槽208经验` | `0x342` | 1 | `uint8` | 槽208经验；字段策略 Editable |
| `槽209经验` | `0x346` | 1 | `uint8` | 槽209经验；字段策略 Editable |
| `槽210经验` | `0x34A` | 1 | `uint8` | 槽210经验；字段策略 Editable |
| `槽211经验` | `0x34E` | 1 | `uint8` | 槽211经验；字段策略 Editable |
| `槽212经验` | `0x352` | 1 | `uint8` | 槽212经验；字段策略 Editable |
| `槽213经验` | `0x356` | 1 | `uint8` | 槽213经验；字段策略 Editable |
| `槽214经验` | `0x35A` | 1 | `uint8` | 槽214经验；字段策略 Editable |
| `槽215经验` | `0x35E` | 1 | `uint8` | 槽215经验；字段策略 Editable |
| `槽216经验` | `0x362` | 1 | `uint8` | 槽216经验；字段策略 Editable |
| `槽217经验` | `0x366` | 1 | `uint8` | 槽217经验；字段策略 Editable |
| `槽218经验` | `0x36A` | 1 | `uint8` | 槽218经验；字段策略 Editable |
| `槽219经验` | `0x36E` | 1 | `uint8` | 槽219经验；字段策略 Editable |
| `槽220经验` | `0x372` | 1 | `uint8` | 槽220经验；字段策略 Editable |
| `槽221经验` | `0x376` | 1 | `uint8` | 槽221经验；字段策略 Editable |
| `槽222经验` | `0x37A` | 1 | `uint8` | 槽222经验；字段策略 Editable |
| `槽223经验` | `0x37E` | 1 | `uint8` | 槽223经验；字段策略 Editable |
| `槽224经验` | `0x382` | 1 | `uint8` | 槽224经验；字段策略 Editable |
| `槽225经验` | `0x386` | 1 | `uint8` | 槽225经验；字段策略 Editable |
| `槽226经验` | `0x38A` | 1 | `uint8` | 槽226经验；字段策略 Editable |
| `槽227经验` | `0x38E` | 1 | `uint8` | 槽227经验；字段策略 Editable |
| `槽228经验` | `0x392` | 1 | `uint8` | 槽228经验；字段策略 Editable |
| `槽229经验` | `0x396` | 1 | `uint8` | 槽229经验；字段策略 Editable |
| `槽230经验` | `0x39A` | 1 | `uint8` | 槽230经验；字段策略 Editable |
| `槽231经验` | `0x39E` | 1 | `uint8` | 槽231经验；字段策略 Editable |
| `槽232经验` | `0x3A2` | 1 | `uint8` | 槽232经验；字段策略 Editable |
| `槽233经验` | `0x3A6` | 1 | `uint8` | 槽233经验；字段策略 Editable |
| `槽234经验` | `0x3AA` | 1 | `uint8` | 槽234经验；字段策略 Editable |
| `槽235经验` | `0x3AE` | 1 | `uint8` | 槽235经验；字段策略 Editable |
| `槽236经验` | `0x3B2` | 1 | `uint8` | 槽236经验；字段策略 Editable |
| `槽237经验` | `0x3B6` | 1 | `uint8` | 槽237经验；字段策略 Editable |
| `槽238经验` | `0x3BA` | 1 | `uint8` | 槽238经验；字段策略 Editable |
| `槽239经验` | `0x3BE` | 1 | `uint8` | 槽239经验；字段策略 Editable |
| `槽240经验` | `0x3C2` | 1 | `uint8` | 槽240经验；字段策略 Editable |
| `槽241经验` | `0x3C6` | 1 | `uint8` | 槽241经验；字段策略 Editable |
| `槽242经验` | `0x3CA` | 1 | `uint8` | 槽242经验；字段策略 Editable |
| `槽243经验` | `0x3CE` | 1 | `uint8` | 槽243经验；字段策略 Editable |
| `槽244经验` | `0x3D2` | 1 | `uint8` | 槽244经验；字段策略 Editable |
| `槽245经验` | `0x3D6` | 1 | `uint8` | 槽245经验；字段策略 Editable |
| `槽246经验` | `0x3DA` | 1 | `uint8` | 槽246经验；字段策略 Editable |
| `槽247经验` | `0x3DE` | 1 | `uint8` | 槽247经验；字段策略 Editable |
| `槽248经验` | `0x3E2` | 1 | `uint8` | 槽248经验；字段策略 Editable |
| `槽249经验` | `0x3E6` | 1 | `uint8` | 槽249经验；字段策略 Editable |
| `槽250经验` | `0x3EA` | 1 | `uint8` | 槽250经验；字段策略 Editable |
| `槽251经验` | `0x3EE` | 1 | `uint8` | 槽251经验；字段策略 Editable |
| `槽252经验` | `0x3F2` | 1 | `uint8` | 槽252经验；字段策略 Editable |
| `槽253经验` | `0x3F6` | 1 | `uint8` | 槽253经验；字段策略 Editable |
| `槽254经验` | `0x3FA` | 1 | `uint8` | 槽254经验；字段策略 Editable |
| `槽255经验` | `0x3FE` | 1 | `uint8` | 槽255经验；字段策略 Editable |
| `槽0剩余回合` | `0x3` | 1 | `uint8` | 槽0剩余回合；字段策略 Editable |
| `槽1剩余回合` | `0x7` | 1 | `uint8` | 槽1剩余回合；字段策略 Editable |
| `槽2剩余回合` | `0xB` | 1 | `uint8` | 槽2剩余回合；字段策略 Editable |
| `槽3剩余回合` | `0xF` | 1 | `uint8` | 槽3剩余回合；字段策略 Editable |
| `槽4剩余回合` | `0x13` | 1 | `uint8` | 槽4剩余回合；字段策略 Editable |
| `槽5剩余回合` | `0x17` | 1 | `uint8` | 槽5剩余回合；字段策略 Editable |
| `槽6剩余回合` | `0x1B` | 1 | `uint8` | 槽6剩余回合；字段策略 Editable |
| `槽7剩余回合` | `0x1F` | 1 | `uint8` | 槽7剩余回合；字段策略 Editable |
| `槽8剩余回合` | `0x23` | 1 | `uint8` | 槽8剩余回合；字段策略 Editable |
| `槽9剩余回合` | `0x27` | 1 | `uint8` | 槽9剩余回合；字段策略 Editable |
| `槽10剩余回合` | `0x2B` | 1 | `uint8` | 槽10剩余回合；字段策略 Editable |
| `槽11剩余回合` | `0x2F` | 1 | `uint8` | 槽11剩余回合；字段策略 Editable |
| `槽12剩余回合` | `0x33` | 1 | `uint8` | 槽12剩余回合；字段策略 Editable |
| `槽13剩余回合` | `0x37` | 1 | `uint8` | 槽13剩余回合；字段策略 Editable |
| `槽14剩余回合` | `0x3B` | 1 | `uint8` | 槽14剩余回合；字段策略 Editable |
| `槽15剩余回合` | `0x3F` | 1 | `uint8` | 槽15剩余回合；字段策略 Editable |
| `槽16剩余回合` | `0x43` | 1 | `uint8` | 槽16剩余回合；字段策略 Editable |
| `槽17剩余回合` | `0x47` | 1 | `uint8` | 槽17剩余回合；字段策略 Editable |
| `槽18剩余回合` | `0x4B` | 1 | `uint8` | 槽18剩余回合；字段策略 Editable |
| `槽19剩余回合` | `0x4F` | 1 | `uint8` | 槽19剩余回合；字段策略 Editable |
| `槽20剩余回合` | `0x53` | 1 | `uint8` | 槽20剩余回合；字段策略 Editable |
| `槽21剩余回合` | `0x57` | 1 | `uint8` | 槽21剩余回合；字段策略 Editable |
| `槽22剩余回合` | `0x5B` | 1 | `uint8` | 槽22剩余回合；字段策略 Editable |
| `槽23剩余回合` | `0x5F` | 1 | `uint8` | 槽23剩余回合；字段策略 Editable |
| `槽24剩余回合` | `0x63` | 1 | `uint8` | 槽24剩余回合；字段策略 Editable |
| `槽25剩余回合` | `0x67` | 1 | `uint8` | 槽25剩余回合；字段策略 Editable |
| `槽26剩余回合` | `0x6B` | 1 | `uint8` | 槽26剩余回合；字段策略 Editable |
| `槽27剩余回合` | `0x6F` | 1 | `uint8` | 槽27剩余回合；字段策略 Editable |
| `槽28剩余回合` | `0x73` | 1 | `uint8` | 槽28剩余回合；字段策略 Editable |
| `槽29剩余回合` | `0x77` | 1 | `uint8` | 槽29剩余回合；字段策略 Editable |
| `槽30剩余回合` | `0x7B` | 1 | `uint8` | 槽30剩余回合；字段策略 Editable |
| `槽31剩余回合` | `0x7F` | 1 | `uint8` | 槽31剩余回合；字段策略 Editable |
| `槽32剩余回合` | `0x83` | 1 | `uint8` | 槽32剩余回合；字段策略 Editable |
| `槽33剩余回合` | `0x87` | 1 | `uint8` | 槽33剩余回合；字段策略 Editable |
| `槽34剩余回合` | `0x8B` | 1 | `uint8` | 槽34剩余回合；字段策略 Editable |
| `槽35剩余回合` | `0x8F` | 1 | `uint8` | 槽35剩余回合；字段策略 Editable |
| `槽36剩余回合` | `0x93` | 1 | `uint8` | 槽36剩余回合；字段策略 Editable |
| `槽37剩余回合` | `0x97` | 1 | `uint8` | 槽37剩余回合；字段策略 Editable |
| `槽38剩余回合` | `0x9B` | 1 | `uint8` | 槽38剩余回合；字段策略 Editable |
| `槽39剩余回合` | `0x9F` | 1 | `uint8` | 槽39剩余回合；字段策略 Editable |
| `槽40剩余回合` | `0xA3` | 1 | `uint8` | 槽40剩余回合；字段策略 Editable |
| `槽41剩余回合` | `0xA7` | 1 | `uint8` | 槽41剩余回合；字段策略 Editable |
| `槽42剩余回合` | `0xAB` | 1 | `uint8` | 槽42剩余回合；字段策略 Editable |
| `槽43剩余回合` | `0xAF` | 1 | `uint8` | 槽43剩余回合；字段策略 Editable |
| `槽44剩余回合` | `0xB3` | 1 | `uint8` | 槽44剩余回合；字段策略 Editable |
| `槽45剩余回合` | `0xB7` | 1 | `uint8` | 槽45剩余回合；字段策略 Editable |
| `槽46剩余回合` | `0xBB` | 1 | `uint8` | 槽46剩余回合；字段策略 Editable |
| `槽47剩余回合` | `0xBF` | 1 | `uint8` | 槽47剩余回合；字段策略 Editable |
| `槽48剩余回合` | `0xC3` | 1 | `uint8` | 槽48剩余回合；字段策略 Editable |
| `槽49剩余回合` | `0xC7` | 1 | `uint8` | 槽49剩余回合；字段策略 Editable |
| `槽50剩余回合` | `0xCB` | 1 | `uint8` | 槽50剩余回合；字段策略 Editable |
| `槽51剩余回合` | `0xCF` | 1 | `uint8` | 槽51剩余回合；字段策略 Editable |
| `槽52剩余回合` | `0xD3` | 1 | `uint8` | 槽52剩余回合；字段策略 Editable |
| `槽53剩余回合` | `0xD7` | 1 | `uint8` | 槽53剩余回合；字段策略 Editable |
| `槽54剩余回合` | `0xDB` | 1 | `uint8` | 槽54剩余回合；字段策略 Editable |
| `槽55剩余回合` | `0xDF` | 1 | `uint8` | 槽55剩余回合；字段策略 Editable |
| `槽56剩余回合` | `0xE3` | 1 | `uint8` | 槽56剩余回合；字段策略 Editable |
| `槽57剩余回合` | `0xE7` | 1 | `uint8` | 槽57剩余回合；字段策略 Editable |
| `槽58剩余回合` | `0xEB` | 1 | `uint8` | 槽58剩余回合；字段策略 Editable |
| `槽59剩余回合` | `0xEF` | 1 | `uint8` | 槽59剩余回合；字段策略 Editable |
| `槽60剩余回合` | `0xF3` | 1 | `uint8` | 槽60剩余回合；字段策略 Editable |
| `槽61剩余回合` | `0xF7` | 1 | `uint8` | 槽61剩余回合；字段策略 Editable |
| `槽62剩余回合` | `0xFB` | 1 | `uint8` | 槽62剩余回合；字段策略 Editable |
| `槽63剩余回合` | `0xFF` | 1 | `uint8` | 槽63剩余回合；字段策略 Editable |
| `槽64剩余回合` | `0x103` | 1 | `uint8` | 槽64剩余回合；字段策略 Editable |
| `槽65剩余回合` | `0x107` | 1 | `uint8` | 槽65剩余回合；字段策略 Editable |
| `槽66剩余回合` | `0x10B` | 1 | `uint8` | 槽66剩余回合；字段策略 Editable |
| `槽67剩余回合` | `0x10F` | 1 | `uint8` | 槽67剩余回合；字段策略 Editable |
| `槽68剩余回合` | `0x113` | 1 | `uint8` | 槽68剩余回合；字段策略 Editable |
| `槽69剩余回合` | `0x117` | 1 | `uint8` | 槽69剩余回合；字段策略 Editable |
| `槽70剩余回合` | `0x11B` | 1 | `uint8` | 槽70剩余回合；字段策略 Editable |
| `槽71剩余回合` | `0x11F` | 1 | `uint8` | 槽71剩余回合；字段策略 Editable |
| `槽72剩余回合` | `0x123` | 1 | `uint8` | 槽72剩余回合；字段策略 Editable |
| `槽73剩余回合` | `0x127` | 1 | `uint8` | 槽73剩余回合；字段策略 Editable |
| `槽74剩余回合` | `0x12B` | 1 | `uint8` | 槽74剩余回合；字段策略 Editable |
| `槽75剩余回合` | `0x12F` | 1 | `uint8` | 槽75剩余回合；字段策略 Editable |
| `槽76剩余回合` | `0x133` | 1 | `uint8` | 槽76剩余回合；字段策略 Editable |
| `槽77剩余回合` | `0x137` | 1 | `uint8` | 槽77剩余回合；字段策略 Editable |
| `槽78剩余回合` | `0x13B` | 1 | `uint8` | 槽78剩余回合；字段策略 Editable |
| `槽79剩余回合` | `0x13F` | 1 | `uint8` | 槽79剩余回合；字段策略 Editable |
| `槽80剩余回合` | `0x143` | 1 | `uint8` | 槽80剩余回合；字段策略 Editable |
| `槽81剩余回合` | `0x147` | 1 | `uint8` | 槽81剩余回合；字段策略 Editable |
| `槽82剩余回合` | `0x14B` | 1 | `uint8` | 槽82剩余回合；字段策略 Editable |
| `槽83剩余回合` | `0x14F` | 1 | `uint8` | 槽83剩余回合；字段策略 Editable |
| `槽84剩余回合` | `0x153` | 1 | `uint8` | 槽84剩余回合；字段策略 Editable |
| `槽85剩余回合` | `0x157` | 1 | `uint8` | 槽85剩余回合；字段策略 Editable |
| `槽86剩余回合` | `0x15B` | 1 | `uint8` | 槽86剩余回合；字段策略 Editable |
| `槽87剩余回合` | `0x15F` | 1 | `uint8` | 槽87剩余回合；字段策略 Editable |
| `槽88剩余回合` | `0x163` | 1 | `uint8` | 槽88剩余回合；字段策略 Editable |
| `槽89剩余回合` | `0x167` | 1 | `uint8` | 槽89剩余回合；字段策略 Editable |
| `槽90剩余回合` | `0x16B` | 1 | `uint8` | 槽90剩余回合；字段策略 Editable |
| `槽91剩余回合` | `0x16F` | 1 | `uint8` | 槽91剩余回合；字段策略 Editable |
| `槽92剩余回合` | `0x173` | 1 | `uint8` | 槽92剩余回合；字段策略 Editable |
| `槽93剩余回合` | `0x177` | 1 | `uint8` | 槽93剩余回合；字段策略 Editable |
| `槽94剩余回合` | `0x17B` | 1 | `uint8` | 槽94剩余回合；字段策略 Editable |
| `槽95剩余回合` | `0x17F` | 1 | `uint8` | 槽95剩余回合；字段策略 Editable |
| `槽96剩余回合` | `0x183` | 1 | `uint8` | 槽96剩余回合；字段策略 Editable |
| `槽97剩余回合` | `0x187` | 1 | `uint8` | 槽97剩余回合；字段策略 Editable |
| `槽98剩余回合` | `0x18B` | 1 | `uint8` | 槽98剩余回合；字段策略 Editable |
| `槽99剩余回合` | `0x18F` | 1 | `uint8` | 槽99剩余回合；字段策略 Editable |
| `槽100剩余回合` | `0x193` | 1 | `uint8` | 槽100剩余回合；字段策略 Editable |
| `槽101剩余回合` | `0x197` | 1 | `uint8` | 槽101剩余回合；字段策略 Editable |
| `槽102剩余回合` | `0x19B` | 1 | `uint8` | 槽102剩余回合；字段策略 Editable |
| `槽103剩余回合` | `0x19F` | 1 | `uint8` | 槽103剩余回合；字段策略 Editable |
| `槽104剩余回合` | `0x1A3` | 1 | `uint8` | 槽104剩余回合；字段策略 Editable |
| `槽105剩余回合` | `0x1A7` | 1 | `uint8` | 槽105剩余回合；字段策略 Editable |
| `槽106剩余回合` | `0x1AB` | 1 | `uint8` | 槽106剩余回合；字段策略 Editable |
| `槽107剩余回合` | `0x1AF` | 1 | `uint8` | 槽107剩余回合；字段策略 Editable |
| `槽108剩余回合` | `0x1B3` | 1 | `uint8` | 槽108剩余回合；字段策略 Editable |
| `槽109剩余回合` | `0x1B7` | 1 | `uint8` | 槽109剩余回合；字段策略 Editable |
| `槽110剩余回合` | `0x1BB` | 1 | `uint8` | 槽110剩余回合；字段策略 Editable |
| `槽111剩余回合` | `0x1BF` | 1 | `uint8` | 槽111剩余回合；字段策略 Editable |
| `槽112剩余回合` | `0x1C3` | 1 | `uint8` | 槽112剩余回合；字段策略 Editable |
| `槽113剩余回合` | `0x1C7` | 1 | `uint8` | 槽113剩余回合；字段策略 Editable |
| `槽114剩余回合` | `0x1CB` | 1 | `uint8` | 槽114剩余回合；字段策略 Editable |
| `槽115剩余回合` | `0x1CF` | 1 | `uint8` | 槽115剩余回合；字段策略 Editable |
| `槽116剩余回合` | `0x1D3` | 1 | `uint8` | 槽116剩余回合；字段策略 Editable |
| `槽117剩余回合` | `0x1D7` | 1 | `uint8` | 槽117剩余回合；字段策略 Editable |
| `槽118剩余回合` | `0x1DB` | 1 | `uint8` | 槽118剩余回合；字段策略 Editable |
| `槽119剩余回合` | `0x1DF` | 1 | `uint8` | 槽119剩余回合；字段策略 Editable |
| `槽120剩余回合` | `0x1E3` | 1 | `uint8` | 槽120剩余回合；字段策略 Editable |
| `槽121剩余回合` | `0x1E7` | 1 | `uint8` | 槽121剩余回合；字段策略 Editable |
| `槽122剩余回合` | `0x1EB` | 1 | `uint8` | 槽122剩余回合；字段策略 Editable |
| `槽123剩余回合` | `0x1EF` | 1 | `uint8` | 槽123剩余回合；字段策略 Editable |
| `槽124剩余回合` | `0x1F3` | 1 | `uint8` | 槽124剩余回合；字段策略 Editable |
| `槽125剩余回合` | `0x1F7` | 1 | `uint8` | 槽125剩余回合；字段策略 Editable |
| `槽126剩余回合` | `0x1FB` | 1 | `uint8` | 槽126剩余回合；字段策略 Editable |
| `槽127剩余回合` | `0x1FF` | 1 | `uint8` | 槽127剩余回合；字段策略 Editable |
| `槽128剩余回合` | `0x203` | 1 | `uint8` | 槽128剩余回合；字段策略 Editable |
| `槽129剩余回合` | `0x207` | 1 | `uint8` | 槽129剩余回合；字段策略 Editable |
| `槽130剩余回合` | `0x20B` | 1 | `uint8` | 槽130剩余回合；字段策略 Editable |
| `槽131剩余回合` | `0x20F` | 1 | `uint8` | 槽131剩余回合；字段策略 Editable |
| `槽132剩余回合` | `0x213` | 1 | `uint8` | 槽132剩余回合；字段策略 Editable |
| `槽133剩余回合` | `0x217` | 1 | `uint8` | 槽133剩余回合；字段策略 Editable |
| `槽134剩余回合` | `0x21B` | 1 | `uint8` | 槽134剩余回合；字段策略 Editable |
| `槽135剩余回合` | `0x21F` | 1 | `uint8` | 槽135剩余回合；字段策略 Editable |
| `槽136剩余回合` | `0x223` | 1 | `uint8` | 槽136剩余回合；字段策略 Editable |
| `槽137剩余回合` | `0x227` | 1 | `uint8` | 槽137剩余回合；字段策略 Editable |
| `槽138剩余回合` | `0x22B` | 1 | `uint8` | 槽138剩余回合；字段策略 Editable |
| `槽139剩余回合` | `0x22F` | 1 | `uint8` | 槽139剩余回合；字段策略 Editable |
| `槽140剩余回合` | `0x233` | 1 | `uint8` | 槽140剩余回合；字段策略 Editable |
| `槽141剩余回合` | `0x237` | 1 | `uint8` | 槽141剩余回合；字段策略 Editable |
| `槽142剩余回合` | `0x23B` | 1 | `uint8` | 槽142剩余回合；字段策略 Editable |
| `槽143剩余回合` | `0x23F` | 1 | `uint8` | 槽143剩余回合；字段策略 Editable |
| `槽144剩余回合` | `0x243` | 1 | `uint8` | 槽144剩余回合；字段策略 Editable |
| `槽145剩余回合` | `0x247` | 1 | `uint8` | 槽145剩余回合；字段策略 Editable |
| `槽146剩余回合` | `0x24B` | 1 | `uint8` | 槽146剩余回合；字段策略 Editable |
| `槽147剩余回合` | `0x24F` | 1 | `uint8` | 槽147剩余回合；字段策略 Editable |
| `槽148剩余回合` | `0x253` | 1 | `uint8` | 槽148剩余回合；字段策略 Editable |
| `槽149剩余回合` | `0x257` | 1 | `uint8` | 槽149剩余回合；字段策略 Editable |
| `槽150剩余回合` | `0x25B` | 1 | `uint8` | 槽150剩余回合；字段策略 Editable |
| `槽151剩余回合` | `0x25F` | 1 | `uint8` | 槽151剩余回合；字段策略 Editable |
| `槽152剩余回合` | `0x263` | 1 | `uint8` | 槽152剩余回合；字段策略 Editable |
| `槽153剩余回合` | `0x267` | 1 | `uint8` | 槽153剩余回合；字段策略 Editable |
| `槽154剩余回合` | `0x26B` | 1 | `uint8` | 槽154剩余回合；字段策略 Editable |
| `槽155剩余回合` | `0x26F` | 1 | `uint8` | 槽155剩余回合；字段策略 Editable |
| `槽156剩余回合` | `0x273` | 1 | `uint8` | 槽156剩余回合；字段策略 Editable |
| `槽157剩余回合` | `0x277` | 1 | `uint8` | 槽157剩余回合；字段策略 Editable |
| `槽158剩余回合` | `0x27B` | 1 | `uint8` | 槽158剩余回合；字段策略 Editable |
| `槽159剩余回合` | `0x27F` | 1 | `uint8` | 槽159剩余回合；字段策略 Editable |
| `槽160剩余回合` | `0x283` | 1 | `uint8` | 槽160剩余回合；字段策略 Editable |
| `槽161剩余回合` | `0x287` | 1 | `uint8` | 槽161剩余回合；字段策略 Editable |
| `槽162剩余回合` | `0x28B` | 1 | `uint8` | 槽162剩余回合；字段策略 Editable |
| `槽163剩余回合` | `0x28F` | 1 | `uint8` | 槽163剩余回合；字段策略 Editable |
| `槽164剩余回合` | `0x293` | 1 | `uint8` | 槽164剩余回合；字段策略 Editable |
| `槽165剩余回合` | `0x297` | 1 | `uint8` | 槽165剩余回合；字段策略 Editable |
| `槽166剩余回合` | `0x29B` | 1 | `uint8` | 槽166剩余回合；字段策略 Editable |
| `槽167剩余回合` | `0x29F` | 1 | `uint8` | 槽167剩余回合；字段策略 Editable |
| `槽168剩余回合` | `0x2A3` | 1 | `uint8` | 槽168剩余回合；字段策略 Editable |
| `槽169剩余回合` | `0x2A7` | 1 | `uint8` | 槽169剩余回合；字段策略 Editable |
| `槽170剩余回合` | `0x2AB` | 1 | `uint8` | 槽170剩余回合；字段策略 Editable |
| `槽171剩余回合` | `0x2AF` | 1 | `uint8` | 槽171剩余回合；字段策略 Editable |
| `槽172剩余回合` | `0x2B3` | 1 | `uint8` | 槽172剩余回合；字段策略 Editable |
| `槽173剩余回合` | `0x2B7` | 1 | `uint8` | 槽173剩余回合；字段策略 Editable |
| `槽174剩余回合` | `0x2BB` | 1 | `uint8` | 槽174剩余回合；字段策略 Editable |
| `槽175剩余回合` | `0x2BF` | 1 | `uint8` | 槽175剩余回合；字段策略 Editable |
| `槽176剩余回合` | `0x2C3` | 1 | `uint8` | 槽176剩余回合；字段策略 Editable |
| `槽177剩余回合` | `0x2C7` | 1 | `uint8` | 槽177剩余回合；字段策略 Editable |
| `槽178剩余回合` | `0x2CB` | 1 | `uint8` | 槽178剩余回合；字段策略 Editable |
| `槽179剩余回合` | `0x2CF` | 1 | `uint8` | 槽179剩余回合；字段策略 Editable |
| `槽180剩余回合` | `0x2D3` | 1 | `uint8` | 槽180剩余回合；字段策略 Editable |
| `槽181剩余回合` | `0x2D7` | 1 | `uint8` | 槽181剩余回合；字段策略 Editable |
| `槽182剩余回合` | `0x2DB` | 1 | `uint8` | 槽182剩余回合；字段策略 Editable |
| `槽183剩余回合` | `0x2DF` | 1 | `uint8` | 槽183剩余回合；字段策略 Editable |
| `槽184剩余回合` | `0x2E3` | 1 | `uint8` | 槽184剩余回合；字段策略 Editable |
| `槽185剩余回合` | `0x2E7` | 1 | `uint8` | 槽185剩余回合；字段策略 Editable |
| `槽186剩余回合` | `0x2EB` | 1 | `uint8` | 槽186剩余回合；字段策略 Editable |
| `槽187剩余回合` | `0x2EF` | 1 | `uint8` | 槽187剩余回合；字段策略 Editable |
| `槽188剩余回合` | `0x2F3` | 1 | `uint8` | 槽188剩余回合；字段策略 Editable |
| `槽189剩余回合` | `0x2F7` | 1 | `uint8` | 槽189剩余回合；字段策略 Editable |
| `槽190剩余回合` | `0x2FB` | 1 | `uint8` | 槽190剩余回合；字段策略 Editable |
| `槽191剩余回合` | `0x2FF` | 1 | `uint8` | 槽191剩余回合；字段策略 Editable |
| `槽192剩余回合` | `0x303` | 1 | `uint8` | 槽192剩余回合；字段策略 Editable |
| `槽193剩余回合` | `0x307` | 1 | `uint8` | 槽193剩余回合；字段策略 Editable |
| `槽194剩余回合` | `0x30B` | 1 | `uint8` | 槽194剩余回合；字段策略 Editable |
| `槽195剩余回合` | `0x30F` | 1 | `uint8` | 槽195剩余回合；字段策略 Editable |
| `槽196剩余回合` | `0x313` | 1 | `uint8` | 槽196剩余回合；字段策略 Editable |
| `槽197剩余回合` | `0x317` | 1 | `uint8` | 槽197剩余回合；字段策略 Editable |
| `槽198剩余回合` | `0x31B` | 1 | `uint8` | 槽198剩余回合；字段策略 Editable |
| `槽199剩余回合` | `0x31F` | 1 | `uint8` | 槽199剩余回合；字段策略 Editable |
| `槽200剩余回合` | `0x323` | 1 | `uint8` | 槽200剩余回合；字段策略 Editable |
| `槽201剩余回合` | `0x327` | 1 | `uint8` | 槽201剩余回合；字段策略 Editable |
| `槽202剩余回合` | `0x32B` | 1 | `uint8` | 槽202剩余回合；字段策略 Editable |
| `槽203剩余回合` | `0x32F` | 1 | `uint8` | 槽203剩余回合；字段策略 Editable |
| `槽204剩余回合` | `0x333` | 1 | `uint8` | 槽204剩余回合；字段策略 Editable |
| `槽205剩余回合` | `0x337` | 1 | `uint8` | 槽205剩余回合；字段策略 Editable |
| `槽206剩余回合` | `0x33B` | 1 | `uint8` | 槽206剩余回合；字段策略 Editable |
| `槽207剩余回合` | `0x33F` | 1 | `uint8` | 槽207剩余回合；字段策略 Editable |
| `槽208剩余回合` | `0x343` | 1 | `uint8` | 槽208剩余回合；字段策略 Editable |
| `槽209剩余回合` | `0x347` | 1 | `uint8` | 槽209剩余回合；字段策略 Editable |
| `槽210剩余回合` | `0x34B` | 1 | `uint8` | 槽210剩余回合；字段策略 Editable |
| `槽211剩余回合` | `0x34F` | 1 | `uint8` | 槽211剩余回合；字段策略 Editable |
| `槽212剩余回合` | `0x353` | 1 | `uint8` | 槽212剩余回合；字段策略 Editable |
| `槽213剩余回合` | `0x357` | 1 | `uint8` | 槽213剩余回合；字段策略 Editable |
| `槽214剩余回合` | `0x35B` | 1 | `uint8` | 槽214剩余回合；字段策略 Editable |
| `槽215剩余回合` | `0x35F` | 1 | `uint8` | 槽215剩余回合；字段策略 Editable |
| `槽216剩余回合` | `0x363` | 1 | `uint8` | 槽216剩余回合；字段策略 Editable |
| `槽217剩余回合` | `0x367` | 1 | `uint8` | 槽217剩余回合；字段策略 Editable |
| `槽218剩余回合` | `0x36B` | 1 | `uint8` | 槽218剩余回合；字段策略 Editable |
| `槽219剩余回合` | `0x36F` | 1 | `uint8` | 槽219剩余回合；字段策略 Editable |
| `槽220剩余回合` | `0x373` | 1 | `uint8` | 槽220剩余回合；字段策略 Editable |
| `槽221剩余回合` | `0x377` | 1 | `uint8` | 槽221剩余回合；字段策略 Editable |
| `槽222剩余回合` | `0x37B` | 1 | `uint8` | 槽222剩余回合；字段策略 Editable |
| `槽223剩余回合` | `0x37F` | 1 | `uint8` | 槽223剩余回合；字段策略 Editable |
| `槽224剩余回合` | `0x383` | 1 | `uint8` | 槽224剩余回合；字段策略 Editable |
| `槽225剩余回合` | `0x387` | 1 | `uint8` | 槽225剩余回合；字段策略 Editable |
| `槽226剩余回合` | `0x38B` | 1 | `uint8` | 槽226剩余回合；字段策略 Editable |
| `槽227剩余回合` | `0x38F` | 1 | `uint8` | 槽227剩余回合；字段策略 Editable |
| `槽228剩余回合` | `0x393` | 1 | `uint8` | 槽228剩余回合；字段策略 Editable |
| `槽229剩余回合` | `0x397` | 1 | `uint8` | 槽229剩余回合；字段策略 Editable |
| `槽230剩余回合` | `0x39B` | 1 | `uint8` | 槽230剩余回合；字段策略 Editable |
| `槽231剩余回合` | `0x39F` | 1 | `uint8` | 槽231剩余回合；字段策略 Editable |
| `槽232剩余回合` | `0x3A3` | 1 | `uint8` | 槽232剩余回合；字段策略 Editable |
| `槽233剩余回合` | `0x3A7` | 1 | `uint8` | 槽233剩余回合；字段策略 Editable |
| `槽234剩余回合` | `0x3AB` | 1 | `uint8` | 槽234剩余回合；字段策略 Editable |
| `槽235剩余回合` | `0x3AF` | 1 | `uint8` | 槽235剩余回合；字段策略 Editable |
| `槽236剩余回合` | `0x3B3` | 1 | `uint8` | 槽236剩余回合；字段策略 Editable |
| `槽237剩余回合` | `0x3B7` | 1 | `uint8` | 槽237剩余回合；字段策略 Editable |
| `槽238剩余回合` | `0x3BB` | 1 | `uint8` | 槽238剩余回合；字段策略 Editable |
| `槽239剩余回合` | `0x3BF` | 1 | `uint8` | 槽239剩余回合；字段策略 Editable |
| `槽240剩余回合` | `0x3C3` | 1 | `uint8` | 槽240剩余回合；字段策略 Editable |
| `槽241剩余回合` | `0x3C7` | 1 | `uint8` | 槽241剩余回合；字段策略 Editable |
| `槽242剩余回合` | `0x3CB` | 1 | `uint8` | 槽242剩余回合；字段策略 Editable |
| `槽243剩余回合` | `0x3CF` | 1 | `uint8` | 槽243剩余回合；字段策略 Editable |
| `槽244剩余回合` | `0x3D3` | 1 | `uint8` | 槽244剩余回合；字段策略 Editable |
| `槽245剩余回合` | `0x3D7` | 1 | `uint8` | 槽245剩余回合；字段策略 Editable |
| `槽246剩余回合` | `0x3DB` | 1 | `uint8` | 槽246剩余回合；字段策略 Editable |
| `槽247剩余回合` | `0x3DF` | 1 | `uint8` | 槽247剩余回合；字段策略 Editable |
| `槽248剩余回合` | `0x3E3` | 1 | `uint8` | 槽248剩余回合；字段策略 Editable |
| `槽249剩余回合` | `0x3E7` | 1 | `uint8` | 槽249剩余回合；字段策略 Editable |
| `槽250剩余回合` | `0x3EB` | 1 | `uint8` | 槽250剩余回合；字段策略 Editable |
| `槽251剩余回合` | `0x3EF` | 1 | `uint8` | 槽251剩余回合；字段策略 Editable |
| `槽252剩余回合` | `0x3F3` | 1 | `uint8` | 槽252剩余回合；字段策略 Editable |
| `槽253剩余回合` | `0x3F7` | 1 | `uint8` | 槽253剩余回合；字段策略 Editable |
| `槽254剩余回合` | `0x3FB` | 1 | `uint8` | 槽254剩余回合；字段策略 Editable |
| `槽255剩余回合` | `0x3FF` | 1 | `uint8` | 槽255剩余回合；字段策略 Editable |

## 66-standard-v1 特效成长拓展（effect-messages 物理表）

ID: `struct.66.disk.66-standard-v1.effect-messages`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x8` (8)

索引公式: `Effectmsg.e5 + 0x0 + (ID - 0) * 0x8 + field_offset; ID=0..254`

存储：`Effectmsg.e5`；起点：`0x0` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x7F8`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | - | - | `-` |
| 新改曹操传6.6修正版 | - | - | `-` |
| 清儿吕布传 | - | - | `-` |
| 烈焰同盟6.6x | - | - | `-` |
| 复刻版6.6山贼 | - | - | `-` |
| 复刻版6.6山贼国庆 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `Enabled` | `0x0` | 1 | `uint8` | Enabled；字段策略 Editable |
| `Param1` | `0x1` | 1 | `uint8` | Param1；字段策略 Editable |
| `Param2` | `0x2` | 1 | `uint8` | Param2；字段策略 Editable |
| `Param3` | `0x3` | 1 | `uint8` | Param3；字段策略 Editable |
| `Param4` | `0x4` | 1 | `uint8` | Param4；字段策略 Editable |
| `Param5` | `0x5` | 1 | `uint8` | Param5；字段策略 Editable |
| `Param6` | `0x6` | 1 | `uint8` | Param6；字段策略 Editable |
| `Param7` | `0x7` | 1 | `uint8` | Param7；字段策略 Editable |

## 66-standard-v1 策略学习拓展（strategy-study-extended 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-study-extended`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x40` (64)

索引公式: `MeffStudy.e5 + 0x0 + (ID - 0) * 0x40 + field_offset; ID=0..1023`

存储：`MeffStudy.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x10000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | - | - | `-` |
| 新改曹操传6.6修正版 | - | - | `-` |
| 清儿吕布传 | - | - | `-` |
| 烈焰同盟6.6x | - | - | `-` |
| 复刻版6.6山贼 | - | - | `-` |
| 复刻版6.6山贼国庆 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略0ID` | `0x0` | 1 | `uint8` | 策略0ID；字段策略 Editable |
| `策略1ID` | `0x2` | 1 | `uint8` | 策略1ID；字段策略 Editable |
| `策略2ID` | `0x4` | 1 | `uint8` | 策略2ID；字段策略 Editable |
| `策略3ID` | `0x6` | 1 | `uint8` | 策略3ID；字段策略 Editable |
| `策略4ID` | `0x8` | 1 | `uint8` | 策略4ID；字段策略 Editable |
| `策略5ID` | `0xA` | 1 | `uint8` | 策略5ID；字段策略 Editable |
| `策略6ID` | `0xC` | 1 | `uint8` | 策略6ID；字段策略 Editable |
| `策略7ID` | `0xE` | 1 | `uint8` | 策略7ID；字段策略 Editable |
| `策略8ID` | `0x10` | 1 | `uint8` | 策略8ID；字段策略 Editable |
| `策略9ID` | `0x12` | 1 | `uint8` | 策略9ID；字段策略 Editable |
| `策略10ID` | `0x14` | 1 | `uint8` | 策略10ID；字段策略 Editable |
| `策略11ID` | `0x16` | 1 | `uint8` | 策略11ID；字段策略 Editable |
| `策略12ID` | `0x18` | 1 | `uint8` | 策略12ID；字段策略 Editable |
| `策略13ID` | `0x1A` | 1 | `uint8` | 策略13ID；字段策略 Editable |
| `策略14ID` | `0x1C` | 1 | `uint8` | 策略14ID；字段策略 Editable |
| `策略15ID` | `0x1E` | 1 | `uint8` | 策略15ID；字段策略 Editable |
| `策略16ID` | `0x20` | 1 | `uint8` | 策略16ID；字段策略 Editable |
| `策略17ID` | `0x22` | 1 | `uint8` | 策略17ID；字段策略 Editable |
| `策略18ID` | `0x24` | 1 | `uint8` | 策略18ID；字段策略 Editable |
| `策略19ID` | `0x26` | 1 | `uint8` | 策略19ID；字段策略 Editable |
| `策略20ID` | `0x28` | 1 | `uint8` | 策略20ID；字段策略 Editable |
| `策略21ID` | `0x2A` | 1 | `uint8` | 策略21ID；字段策略 Editable |
| `策略22ID` | `0x2C` | 1 | `uint8` | 策略22ID；字段策略 Editable |
| `策略23ID` | `0x2E` | 1 | `uint8` | 策略23ID；字段策略 Editable |
| `策略24ID` | `0x30` | 1 | `uint8` | 策略24ID；字段策略 Editable |
| `策略25ID` | `0x32` | 1 | `uint8` | 策略25ID；字段策略 Editable |
| `策略26ID` | `0x34` | 1 | `uint8` | 策略26ID；字段策略 Editable |
| `策略27ID` | `0x36` | 1 | `uint8` | 策略27ID；字段策略 Editable |
| `策略28ID` | `0x38` | 1 | `uint8` | 策略28ID；字段策略 Editable |
| `策略29ID` | `0x3A` | 1 | `uint8` | 策略29ID；字段策略 Editable |
| `策略30ID` | `0x3C` | 1 | `uint8` | 策略30ID；字段策略 Editable |
| `策略31ID` | `0x3E` | 1 | `uint8` | 策略31ID；字段策略 Editable |
| `策略0次数` | `0x1` | 1 | `uint8` | 策略0次数；字段策略 Editable |
| `策略1次数` | `0x3` | 1 | `uint8` | 策略1次数；字段策略 Editable |
| `策略2次数` | `0x5` | 1 | `uint8` | 策略2次数；字段策略 Editable |
| `策略3次数` | `0x7` | 1 | `uint8` | 策略3次数；字段策略 Editable |
| `策略4次数` | `0x9` | 1 | `uint8` | 策略4次数；字段策略 Editable |
| `策略5次数` | `0xB` | 1 | `uint8` | 策略5次数；字段策略 Editable |
| `策略6次数` | `0xD` | 1 | `uint8` | 策略6次数；字段策略 Editable |
| `策略7次数` | `0xF` | 1 | `uint8` | 策略7次数；字段策略 Editable |
| `策略8次数` | `0x11` | 1 | `uint8` | 策略8次数；字段策略 Editable |
| `策略9次数` | `0x13` | 1 | `uint8` | 策略9次数；字段策略 Editable |
| `策略10次数` | `0x15` | 1 | `uint8` | 策略10次数；字段策略 Editable |
| `策略11次数` | `0x17` | 1 | `uint8` | 策略11次数；字段策略 Editable |
| `策略12次数` | `0x19` | 1 | `uint8` | 策略12次数；字段策略 Editable |
| `策略13次数` | `0x1B` | 1 | `uint8` | 策略13次数；字段策略 Editable |
| `策略14次数` | `0x1D` | 1 | `uint8` | 策略14次数；字段策略 Editable |
| `策略15次数` | `0x1F` | 1 | `uint8` | 策略15次数；字段策略 Editable |
| `策略16次数` | `0x21` | 1 | `uint8` | 策略16次数；字段策略 Editable |
| `策略17次数` | `0x23` | 1 | `uint8` | 策略17次数；字段策略 Editable |
| `策略18次数` | `0x25` | 1 | `uint8` | 策略18次数；字段策略 Editable |
| `策略19次数` | `0x27` | 1 | `uint8` | 策略19次数；字段策略 Editable |
| `策略20次数` | `0x29` | 1 | `uint8` | 策略20次数；字段策略 Editable |
| `策略21次数` | `0x2B` | 1 | `uint8` | 策略21次数；字段策略 Editable |
| `策略22次数` | `0x2D` | 1 | `uint8` | 策略22次数；字段策略 Editable |
| `策略23次数` | `0x2F` | 1 | `uint8` | 策略23次数；字段策略 Editable |
| `策略24次数` | `0x31` | 1 | `uint8` | 策略24次数；字段策略 Editable |
| `策略25次数` | `0x33` | 1 | `uint8` | 策略25次数；字段策略 Editable |
| `策略26次数` | `0x35` | 1 | `uint8` | 策略26次数；字段策略 Editable |
| `策略27次数` | `0x37` | 1 | `uint8` | 策略27次数；字段策略 Editable |
| `策略28次数` | `0x39` | 1 | `uint8` | 策略28次数；字段策略 Editable |
| `策略29次数` | `0x3B` | 1 | `uint8` | 策略29次数；字段策略 Editable |
| `策略30次数` | `0x3D` | 1 | `uint8` | 策略30次数；字段策略 Editable |
| `策略31次数` | `0x3F` | 1 | `uint8` | 策略31次数；字段策略 Editable |

## 66-standard-v1 锻造（forge 物理表）

ID: `struct.66.disk.66-standard-v1.forge`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x40` (64)

索引公式: `Forge.e5 + 0x0 + (ID - 0) * 0x40 + field_offset; ID=0..1023`

存储：`Forge.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x10000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | - | - | `-` |
| 新改曹操传6.6修正版 | - | - | `-` |
| 清儿吕布传 | - | - | `-` |
| 烈焰同盟6.6x | - | - | `-` |
| 复刻版6.6山贼 | - | - | `-` |
| 复刻版6.6山贼国庆 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 30 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `材料1ID` | `0x1E` | 2 | `uint16le` | 材料1ID；字段策略 Editable |
| `材料2ID` | `0x21` | 2 | `uint16le` | 材料2ID；字段策略 Editable |
| `材料3ID` | `0x24` | 2 | `uint16le` | 材料3ID；字段策略 Editable |
| `材料4ID` | `0x27` | 2 | `uint16le` | 材料4ID；字段策略 Editable |
| `材料5ID` | `0x2A` | 2 | `uint16le` | 材料5ID；字段策略 Editable |
| `材料6ID` | `0x2D` | 2 | `uint16le` | 材料6ID；字段策略 Editable |
| `材料7ID` | `0x30` | 2 | `uint16le` | 材料7ID；字段策略 Editable |
| `材料8ID` | `0x33` | 2 | `uint16le` | 材料8ID；字段策略 Editable |
| `材料1数量` | `0x20` | 1 | `uint8` | 材料1数量；字段策略 Editable |
| `材料2数量` | `0x23` | 1 | `uint8` | 材料2数量；字段策略 Editable |
| `材料3数量` | `0x26` | 1 | `uint8` | 材料3数量；字段策略 Editable |
| `材料4数量` | `0x29` | 1 | `uint8` | 材料4数量；字段策略 Editable |
| `材料5数量` | `0x2C` | 1 | `uint8` | 材料5数量；字段策略 Editable |
| `材料6数量` | `0x2F` | 1 | `uint8` | 材料6数量；字段策略 Editable |
| `材料7数量` | `0x32` | 1 | `uint8` | 材料7数量；字段策略 Editable |
| `材料8数量` | `0x35` | 1 | `uint8` | 材料8数量；字段策略 Editable |
| `价格` | `0x36` | 4 | `uint32le` | 价格；字段策略 Editable |
| `保留58` | `0x3A` | 1 | `bytes` | 保留58；字段策略 Preserve |
| `材料项数` | `0x3A` | 1 | `uint8` | 材料项数；字段策略 Editable |
| `保留59` | `0x3B` | 1 | `bytes` | 保留59；字段策略 Preserve |
| `商店编号` | `0x3B` | 1 | `uint8` | 商店编号；字段策略 Editable |
| `标记` | `0x3C` | 1 | `uint8` | 标记；字段策略 Editable |
| `保留61` | `0x3D` | 1 | `bytes` | 保留61；字段策略 Preserve |
| `剩余次数` | `0x3D` | 1 | `uint8` | 剩余次数；字段策略 Editable |

## 66-standard-v1 策略大动画（strategy-big-animation 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-big-animation`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA31F0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA31F0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3280`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `动画ID` | `0x0` | 1 | `uint8` | 动画ID；字段策略 Editable |

## 66-standard-v1 策略小动画（strategy-small-animation 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-small-animation`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA3160 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA3160` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA31F0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `动画ID` | `0x0` | 1 | `uint8` | 动画ID；字段策略 Editable |

## 66-standard-v1 兵种系·辅助装备分组（job-series-accessory-groups 物理表）

ID: `struct.66.disk.66-standard-v1.job-series-accessory-groups`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `不解析占位 offset=0；实际地址由 VA 0x0044C341 经目标 PE 节表映射；参见 format.65.accessory-job-groups`

存储：`Ekd5.exe`；起点：-；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x1`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 辅助分组不是定长物理表；请在兵种系的辅助分组业务页使用 PE 地址/FF 分隔专用服务及专用 CSV。禁止解码此占位偏移或导出 EXE 文件头。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `Raw` | `0x0` | 1 | `bytes` | Raw；字段策略 Preserve |

## 66-standard-v1 策略施展地形（strategy-terrain-availability 物理表）

ID: `struct.66.disk.66-standard-v1.strategy-terrain-availability`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0x1FECC + (ID - 0) * 0x1 + field_offset; ID=0..29`

存储：`Ekd5.exe`；起点：`0x1FECC` (fileOffset)；记录数：`30`；ID 起点：`0`；结束偏移（不含）：`0x1FEEA`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略施展地形掩码` | `0x0` | 1 | `uint8` | 策略施展地形掩码；字段策略 Editable |

## 66-standard-v1 装备特效名称池（1A-57）（item-effect-names-low 物理表）

ID: `struct.66.disk.66-standard-v1.item-effect-names-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x375` (885)

索引公式: `Ekd5.exe + 0x8A9E8 + (ID - 0) * 0x375 + field_offset; ID=0..0`

存储：`Ekd5.exe`；起点：`0x8A9E8` (fileOffset)；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x8AD5D`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 装备特效名称使用 item-effect-names-66 固定 16 字节名称池，禁止读取或写入 6.5 低段变长池偏移。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `RawHex` | `0x0` | 885 | `bytes` | RawHex；字段策略 Preserve |

## 66-standard-v1 装备特效名称池（58-7F）（item-effect-names-high 物理表）

ID: `struct.66.disk.66-standard-v1.item-effect-names-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x170` (368)

索引公式: `Ekd5.exe + 0x9F800 + (ID - 0) * 0x170 + field_offset; ID=0..0`

存储：`Ekd5.exe`；起点：`0x9F800` (fileOffset)；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x9F970`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 装备特效名称使用 item-effect-names-66 固定 16 字节名称池，禁止读取或写入 6.5 高段变长池偏移。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `RawHex` | `0x0` | 368 | `bytes` | RawHex；字段策略 Preserve |

## 66-standard-v1 必杀（finishing-moves 物理表）

ID: `struct.66.disk.66-standard-v1.finishing-moves`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Data.e5 + 0xE894 + (ID - 0) * 0x10 + field_offset; ID=0..95`

存储：`Data.e5`；起点：`0xE894` (fileOffset)；记录数：`96`；ID 起点：`0`；结束偏移（不含）：`0xEE94`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 61379 | True | `7FCDC8654256CD8D985E160689D5141FFFC10B14A32A8BD2B2CFA069B1F8C68A` |
| 新改曹操传6.6修正版 | 61379 | True | `8B89067B87265277B1EB872569A14F67D158D1E37B4032F6E7460806EF5743BF` |
| 清儿吕布传 | 61379 | True | `512F9B07547ABD739FFA67265D3DC6819B56B8D63AA61ACF93202D34BFAA2C63` |
| 烈焰同盟6.6x | 61379 | True | `AF8CE2DB83AA018A18534FB47C87AF5307F6FB4F7A3E49F636F1BDA8D3AA52C2` |
| 复刻版6.6山贼 | 61379 | True | `C4B57DD0A9DC3EF2A7FE4D6A36EEAF0F7EDEA06BF2F6407B1A8AE3252E5807CE` |
| 复刻版6.6山贼国庆 | 61379 | True | `6341D98825B5C2B466DC9817870FDDC084834EC006765EC1C97113CC16E5C6BC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 11 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `图标` | `0xB` | 1 | `bytes` | 图标；字段策略 Preserve |
| `攻击范围` | `0xC` | 1 | `uint8` | 攻击范围；字段策略 Editable |
| `穿透范围` | `0xD` | 1 | `uint8` | 穿透范围；字段策略 Editable |
| `消耗SP` | `0xE` | 1 | `uint8` | 消耗SP；字段策略 Editable |

## 66-standard-v1 必杀说明（finishing-move-description 物理表）

ID: `struct.66.disk.66-standard-v1.finishing-move-description`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x7080 + (ID - 0) * 0xC8 + field_offset; ID=0..95`

存储：`Imsg.e5`；起点：`0x7080` (fileOffset)；记录数：`96`；ID 起点：`0`；结束偏移（不含）：`0xBB80`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `说明` | `0x0` | 200 | `fixed-string` | 说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 物品获取说明（0-103）（item-acquisition-low 物理表）

ID: `struct.66.disk.66-standard-v1.item-acquisition-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x6B5F8 + (ID - 0) * 0xC8 + field_offset; ID=0..103`

存储：`Imsg.e5`；起点：`0x6B5F8` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x70738`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 旧 HexTable.xml 明确 Enable=false；Imsg 6.5 基底长度不足，且区域与物品说明/撤退区重叠。未取得消费代码前禁止读取或写回。
- 旧 HexTable.xml 的 Enable=false；6.5 文件边界不足，6.6 旧区域与宝物说明/撤退区域冲突且未确认消费引用，禁止读取或写入。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `物品获取说明` | `0x0` | 200 | `fixed-string` | 物品获取说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 物品获取说明（104-199）（item-acquisition-high 物理表）

ID: `struct.66.disk.66-standard-v1.item-acquisition-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x70738 + (ID - 104) * 0xC8 + field_offset; ID=104..199`

存储：`Imsg.e5`；起点：`0x70738` (fileOffset)；记录数：`96`；ID 起点：`104`；结束偏移（不含）：`0x75238`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 旧 HexTable.xml 明确 Enable=false；高段区域与低段获取说明/撤退区存在重叠语义，未取得消费代码前禁止读取或写回。
- 旧 HexTable.xml 的 Enable=false；6.5 文件边界不足，6.6 旧区域与宝物说明/撤退区域冲突且未确认消费引用，禁止读取或写入。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 501400 | True | `D47770DA9028EA22881216CD662F71BA08BF49685F593DB069062D965BFD6428` |
| 新改曹操传6.6修正版 | 501400 | True | `4784E7B3F1DE192E63537E70B146DB3799A61542EDBC91056869BAF76066CE08` |
| 清儿吕布传 | 501400 | True | `69E26C8274FAB9EFF33A21A2534B2861DF3987BDCCC73B568BFCB5C1F002C838` |
| 烈焰同盟6.6x | 501400 | True | `38CFAF608F90619A0BA5ACFE6E1AB71D0E35244FCEFC725FD86436C58B84CE27` |
| 复刻版6.6山贼 | 857117 | True | `A959F248DF6EF5518280EAFEBB5970B318662FA64D354AFFCF23504938146464` |
| 复刻版6.6山贼国庆 | 857117 | True | `13D5D6112B254B47028C60CF2AC13388DC752C31BBD203E4261E62D20D525E2E` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `物品获取说明` | `0x0` | 200 | `fixed-string` | 物品获取说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 宝物扩展（256-511）（items-extended 物理表）

ID: `struct.66.disk.66-standard-v1.items-extended`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `Item.e5 + 0x0 + (ID - 256) * 0x19 + field_offset; ID=256..511`

存储：`Item.e5`；起点：`0x0` (fileOffset)；记录数：`256`；ID 起点：`256`；结束偏移（不含）：`0x1900`。

能力：`Editable`；Codec：`item-65-17-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | - | - | `-` |
| 新改曹操传6.6修正版 | - | - | `-` |
| 清儿吕布传 | - | - | `-` |
| 烈焰同盟6.6x | - | - | `-` |
| 复刻版6.6山贼 | - | - | `-` |
| 复刻版6.6山贼国庆 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 17 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；引用 effect-names；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `图标` | `0x14` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x14 UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-standard-v1 宝物扩展说明（256-511）（item-description-extended 物理表）

ID: `struct.66.disk.66-standard-v1.item-description-extended`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Itemmsg.e5 + 0x0 + (ID - 256) * 0xC8 + field_offset; ID=256..511`

存储：`Itemmsg.e5`；起点：`0x0` (fileOffset)；记录数：`256`；ID 起点：`256`；结束偏移（不含）：`0xC800`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | - | - | `-` |
| 新改曹操传6.6修正版 | - | - | `-` |
| 清儿吕布传 | - | - | `-` |
| 烈焰同盟6.6x | - | - | `-` |
| 复刻版6.6山贼 | - | - | `-` |
| 复刻版6.6山贼国庆 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 装备特效名称池（6.6，1A-FF）（item-effect-names-66 物理表）

ID: `struct.66.disk.66-standard-v1.item-effect-names-66`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0x9D9A0 + (ID - 26) * 0x10 + field_offset; ID=26..255`

存储：`Ekd5.exe`；起点：`0x9D9A0` (fileOffset)；记录数：`230`；ID 起点：`26`；结束偏移（不含）：`0x9E800`。

能力：`ReadOnly`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 固定 16 字节名称池，专用名称池服务负责解析/写入，物理页只读。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 曹操传6.6-V7.16 | 1130496 | True | `34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA` |
| 新改曹操传6.6修正版 | 1130496 | True | `4A4FD8DDBF83E5F0B769D1B97BF8F6E6431C3AB42892024A354228212D3D06A4` |
| 清儿吕布传 | 1413120 | True | `88EC708A24718868090F70256D09086E83C92FAB0613C7B8D3742EF974D3564D` |
| 烈焰同盟6.6x | 1173504 | True | `D4C6EA15A527C62283CAEADEFAC112109D0B5D63D66AD25BE1D1FD2413EF6EE2` |
| 复刻版6.6山贼 | 1148928 | True | `25D488C874A08553903CDAD9A07FF6FBCD1A38EE6C6B6386F40152DA963D833A` |
| 复刻版6.6山贼国庆 | 1148928 | True | `A34635474CDBBA4AB4844A599D7A3346CE3276C45EB4D1EE7F3D3A8D65D45EEC` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 16 | `fixed-string` | 名称；字段策略 ReadOnly；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-standard-v1 特殊暴击人物分配（动态物理表）

ID: `struct.66.disk.66-standard-v1.person-critical-special-map`；状态: `canonical`；证据: `source-reviewed-pe-reference-gated`

步长: `0x4` (4)

索引公式: `Ekd5.exe + 0x89C30 + specialSlot * 4; specialSlot=0..20; Imsg.e5 quoteOffset=140000 + specialSlot*200`

存储：`Ekd5.exe`；起点：`0x89C30` (fileOffset)；记录数：`21`；ID 起点：`0`；结束偏移（不含）：`0x89C84`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`not applicable`。

写入门禁：

- 需验证目标 PE 可执行区对该区域的引用、21 个 UInt32 值和文件边界；不能只检查原始固定偏移。
- 普通模式清空此人物所有特殊槽到 1024，再写普通类型 0..25 和三句共享台词。
- 特殊模式保持普通类型作为回退；绑定所选槽并清除本人物其它特殊槽；被其它人物占用时先预览并显式覆盖。
- 模式、绑定、人物字段和 Imsg 文本一次跨表事务提交；任何校验失败不产生部分草稿。

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `人物ID` | `0x0` | 4 | `uint32le` | 绑定人物 ID 0..1023，1024 为空槽；数值不是 Imsg 行号，记录主键 ID/槽号才对应特殊台词行。 |

## 66-legacy-data-v1 人物（persons 物理表）

ID: `struct.66.disk.66-legacy-data-v1.persons`；状态: `canonical`；证据: `source-reviewed`

步长: `0x20` (32)

索引公式: `Data.e5 + 0x18C + (ID - 0) * 0x20 + field_offset; ID=0..1023`

存储：`Data.e5`；起点：`0x18C` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x818C`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 13 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `头像` | `0xD` | 2 | `uint16le` | 头像；字段策略 Editable |
| `撤退台词` | `0xF` | 1 | `uint8` | 撤退台词；字段策略 Editable |
| `暴击台词` | `0x10` | 1 | `uint8` | 暴击台词；字段策略 Editable |
| `Army` | `0x11` | 1 | `uint8` | Army；字段策略 Editable |
| `武力` | `0x12` | 1 | `uint8` | 武力；字段策略 Editable |
| `统帅` | `0x13` | 1 | `uint8` | 统帅；字段策略 Editable |
| `智力` | `0x14` | 1 | `uint8` | 智力；字段策略 Editable |
| `敏捷` | `0x15` | 1 | `uint8` | 敏捷；字段策略 Editable |
| `士气` | `0x16` | 1 | `uint8` | 士气；字段策略 Editable |
| `初始HP` | `0x17` | 2 | `uint16le` | 初始HP；字段策略 Editable |
| `初始MP` | `0x19` | 1 | `uint8` | 初始MP；字段策略 Editable |
| `兵种` | `0x1A` | 1 | `uint8` | 兵种；字段策略 Editable；引用 detailed-jobs |
| `级别` | `0x1B` | 1 | `uint8` | 级别；字段策略 Preserve |
| `经验` | `0x1C` | 1 | `uint8` | 经验；字段策略 Preserve |
| `默认武器` | `0x1D` | 1 | `uint8` | 默认武器；字段策略 Editable；引用 items |
| `默认防具` | `0x1E` | 1 | `uint8` | 默认防具；字段策略 Editable；引用 items |
| `默认辅助` | `0x1F` | 1 | `uint8` | 默认辅助；字段策略 Editable；引用 items |

## 66-legacy-data-v1 人物列传（person-biography 物理表）

ID: `struct.66.disk.66-legacy-data-v1.person-biography`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x2D050 + (ID - 0) * 0xC8 + field_offset; ID=0..1023`

存储：`Imsg.e5`；起点：`0x2D050` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x5F050`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `人物列传` | `0x0` | 200 | `fixed-string` | 人物列传；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 宝物（0-103）（items-low 物理表）

ID: `struct.66.disk.66-legacy-data-v1.items-low`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `Data.e5 + 0x818C + (ID - 0) * 0x19 + field_offset; ID=0..103`

存储：`Data.e5`；起点：`0x818C` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x8BB4`。

能力：`Editable`；Codec：`item-65-17-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 17 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；引用 effect-names；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `图标` | `0x14` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x14 UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-legacy-data-v1 宝物（104-254）（items-high 物理表）

ID: `struct.66.disk.66-legacy-data-v1.items-high`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `Star.e5 + 0x0 + (ID - 104) * 0x19 + field_offset; ID=104..254`

存储：`Star.e5`；起点：`0x0` (fileOffset)；记录数：`151`；ID 起点：`104`；结束偏移（不含）：`0xEBF`。

能力：`Editable`；Codec：`item-65-17-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 6359 | True | `32D1D6B82D26C0ADF841E5BD746760EBA602CF2B579671E36AA60974AFE98766` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 17 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；引用 effect-names；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `图标` | `0x14` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x14 UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-legacy-data-v1 宝物说明（0-103）（item-description-low 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-description-low`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x5F050 + (ID - 0) * 0xC8 + field_offset; ID=0..103`

存储：`Imsg.e5`；起点：`0x5F050` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x64190`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 宝物说明（104-254）（item-description-high 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-description-high`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x64190 + (ID - 104) * 0xC8 + field_offset; ID=104..254`

存储：`Imsg.e5`；起点：`0x64190` (fileOffset)；记录数：`151`；ID 起点：`104`；结束偏移（不含）：`0x6B788`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 兵种系（job-series 物理表）

ID: `struct.66.disk.66-legacy-data-v1.job-series`；状态: `canonical`；证据: `source-reviewed`

步长: `0x9` (9)

索引公式: `Ekd5.exe + 0x8B010 + (ID - 0) * 0x9 + field_offset; ID=0..39`

存储：`Ekd5.exe`；起点：`0x8B010` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0x8B178`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 9 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 兵种系·地形发挥（job-series-terrain 物理表）

ID: `struct.66.disk.66-legacy-data-v1.job-series-terrain`；状态: `canonical`；证据: `source-reviewed`

步长: `0x3C` (60)

索引公式: `Data.e5 + 0xA8A4 + (ID - 0) * 0x3C + field_offset; ID=0..39`

存储：`Data.e5`；起点：`0xA8A4` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xB204`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `平原` | `0x0` | 1 | `uint8` | 平原；字段策略 Editable |
| `草原` | `0x1` | 1 | `uint8` | 草原；字段策略 Editable |
| `树林` | `0x2` | 1 | `uint8` | 树林；字段策略 Editable |
| `荒地` | `0x3` | 1 | `uint8` | 荒地；字段策略 Editable |
| `山地` | `0x4` | 1 | `uint8` | 山地；字段策略 Editable |
| `岩山` | `0x5` | 1 | `uint8` | 岩山；字段策略 Editable |
| `山崖` | `0x6` | 1 | `uint8` | 山崖；字段策略 Editable |
| `雪原` | `0x7` | 1 | `uint8` | 雪原；字段策略 Editable |
| `桥梁` | `0x8` | 1 | `uint8` | 桥梁；字段策略 Editable |
| `浅滩` | `0x9` | 1 | `uint8` | 浅滩；字段策略 Editable |
| `沼泽` | `0xA` | 1 | `uint8` | 沼泽；字段策略 Editable |
| `池塘` | `0xB` | 1 | `uint8` | 池塘；字段策略 Editable |
| `小河` | `0xC` | 1 | `uint8` | 小河；字段策略 Editable |
| `大河` | `0xD` | 1 | `uint8` | 大河；字段策略 Editable |
| `栅栏` | `0xE` | 1 | `uint8` | 栅栏；字段策略 Editable |
| `城墙` | `0xF` | 1 | `uint8` | 城墙；字段策略 Editable |
| `城内` | `0x10` | 1 | `uint8` | 城内；字段策略 Editable |
| `城门` | `0x11` | 1 | `uint8` | 城门；字段策略 Editable |
| `城池` | `0x12` | 1 | `uint8` | 城池；字段策略 Editable |
| `关隘` | `0x13` | 1 | `uint8` | 关隘；字段策略 Editable |
| `鹿砦` | `0x14` | 1 | `uint8` | 鹿砦；字段策略 Editable |
| `村庄` | `0x15` | 1 | `uint8` | 村庄；字段策略 Editable |
| `兵营` | `0x16` | 1 | `uint8` | 兵营；字段策略 Editable |
| `民居` | `0x17` | 1 | `uint8` | 民居；字段策略 Editable |
| `宝物库` | `0x18` | 1 | `uint8` | 宝物库；字段策略 Editable |
| `水池` | `0x19` | 1 | `uint8` | 水池；字段策略 Editable |
| `火` | `0x1A` | 1 | `uint8` | 火；字段策略 Editable |
| `船` | `0x1B` | 1 | `uint8` | 船；字段策略 Editable |
| `祭坛` | `0x1C` | 1 | `uint8` | 祭坛；字段策略 Editable |
| `地下` | `0x1D` | 1 | `uint8` | 地下；字段策略 Editable |

## 66-legacy-data-v1 兵种系·移动消耗（job-series-move-cost 物理表）

ID: `struct.66.disk.66-legacy-data-v1.job-series-move-cost`；状态: `canonical`；证据: `source-reviewed`

步长: `0x3C` (60)

索引公式: `Data.e5 + 0xA8C2 + (ID - 0) * 0x3C + field_offset; ID=0..39`

存储：`Data.e5`；起点：`0xA8C2` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xB222`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `平原` | `0x0` | 1 | `uint8` | 平原；字段策略 Editable |
| `草原` | `0x1` | 1 | `uint8` | 草原；字段策略 Editable |
| `树林` | `0x2` | 1 | `uint8` | 树林；字段策略 Editable |
| `荒地` | `0x3` | 1 | `uint8` | 荒地；字段策略 Editable |
| `山地` | `0x4` | 1 | `uint8` | 山地；字段策略 Editable |
| `岩山` | `0x5` | 1 | `uint8` | 岩山；字段策略 Editable |
| `山崖` | `0x6` | 1 | `uint8` | 山崖；字段策略 Editable |
| `雪原` | `0x7` | 1 | `uint8` | 雪原；字段策略 Editable |
| `桥梁` | `0x8` | 1 | `uint8` | 桥梁；字段策略 Editable |
| `浅滩` | `0x9` | 1 | `uint8` | 浅滩；字段策略 Editable |
| `沼泽` | `0xA` | 1 | `uint8` | 沼泽；字段策略 Editable |
| `池塘` | `0xB` | 1 | `uint8` | 池塘；字段策略 Editable |
| `小河` | `0xC` | 1 | `uint8` | 小河；字段策略 Editable |
| `大河` | `0xD` | 1 | `uint8` | 大河；字段策略 Editable |
| `栅栏` | `0xE` | 1 | `uint8` | 栅栏；字段策略 Editable |
| `城墙` | `0xF` | 1 | `uint8` | 城墙；字段策略 Editable |
| `城内` | `0x10` | 1 | `uint8` | 城内；字段策略 Editable |
| `城门` | `0x11` | 1 | `uint8` | 城门；字段策略 Editable |
| `城池` | `0x12` | 1 | `uint8` | 城池；字段策略 Editable |
| `关隘` | `0x13` | 1 | `uint8` | 关隘；字段策略 Editable |
| `鹿砦` | `0x14` | 1 | `uint8` | 鹿砦；字段策略 Editable |
| `村庄` | `0x15` | 1 | `uint8` | 村庄；字段策略 Editable |
| `兵营` | `0x16` | 1 | `uint8` | 兵营；字段策略 Editable |
| `民居` | `0x17` | 1 | `uint8` | 民居；字段策略 Editable |
| `宝物库` | `0x18` | 1 | `uint8` | 宝物库；字段策略 Editable |
| `水池` | `0x19` | 1 | `uint8` | 水池；字段策略 Editable |
| `火` | `0x1A` | 1 | `uint8` | 火；字段策略 Editable |
| `船` | `0x1B` | 1 | `uint8` | 船；字段策略 Editable |
| `祭坛` | `0x1C` | 1 | `uint8` | 祭坛；字段策略 Editable |
| `地下` | `0x1D` | 1 | `uint8` | 地下；字段策略 Editable |

## 66-legacy-data-v1 兵种系·兵种相克（job-series-counter 物理表）

ID: `struct.66.disk.66-legacy-data-v1.job-series-counter`；状态: `canonical`；证据: `source-reviewed`

步长: `0x28` (40)

索引公式: `Ekd5.exe + 0xA3280 + (ID - 0) * 0x28 + field_offset; ID=0..39`

存储：`Ekd5.exe`；起点：`0xA3280` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xA38C0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `对兵种系 0` | `0x0` | 1 | `uint8` | 对兵种系 0；字段策略 Editable |
| `对兵种系 1` | `0x1` | 1 | `uint8` | 对兵种系 1；字段策略 Editable |
| `对兵种系 2` | `0x2` | 1 | `uint8` | 对兵种系 2；字段策略 Editable |
| `对兵种系 3` | `0x3` | 1 | `uint8` | 对兵种系 3；字段策略 Editable |
| `对兵种系 4` | `0x4` | 1 | `uint8` | 对兵种系 4；字段策略 Editable |
| `对兵种系 5` | `0x5` | 1 | `uint8` | 对兵种系 5；字段策略 Editable |
| `对兵种系 6` | `0x6` | 1 | `uint8` | 对兵种系 6；字段策略 Editable |
| `对兵种系 7` | `0x7` | 1 | `uint8` | 对兵种系 7；字段策略 Editable |
| `对兵种系 8` | `0x8` | 1 | `uint8` | 对兵种系 8；字段策略 Editable |
| `对兵种系 9` | `0x9` | 1 | `uint8` | 对兵种系 9；字段策略 Editable |
| `对兵种系 10` | `0xA` | 1 | `uint8` | 对兵种系 10；字段策略 Editable |
| `对兵种系 11` | `0xB` | 1 | `uint8` | 对兵种系 11；字段策略 Editable |
| `对兵种系 12` | `0xC` | 1 | `uint8` | 对兵种系 12；字段策略 Editable |
| `对兵种系 13` | `0xD` | 1 | `uint8` | 对兵种系 13；字段策略 Editable |
| `对兵种系 14` | `0xE` | 1 | `uint8` | 对兵种系 14；字段策略 Editable |
| `对兵种系 15` | `0xF` | 1 | `uint8` | 对兵种系 15；字段策略 Editable |
| `对兵种系 16` | `0x10` | 1 | `uint8` | 对兵种系 16；字段策略 Editable |
| `对兵种系 17` | `0x11` | 1 | `uint8` | 对兵种系 17；字段策略 Editable |
| `对兵种系 18` | `0x12` | 1 | `uint8` | 对兵种系 18；字段策略 Editable |
| `对兵种系 19` | `0x13` | 1 | `uint8` | 对兵种系 19；字段策略 Editable |
| `对兵种系 20` | `0x14` | 1 | `uint8` | 对兵种系 20；字段策略 Editable |
| `对兵种系 21` | `0x15` | 1 | `uint8` | 对兵种系 21；字段策略 Editable |
| `对兵种系 22` | `0x16` | 1 | `uint8` | 对兵种系 22；字段策略 Editable |
| `对兵种系 23` | `0x17` | 1 | `uint8` | 对兵种系 23；字段策略 Editable |
| `对兵种系 24` | `0x18` | 1 | `uint8` | 对兵种系 24；字段策略 Editable |
| `对兵种系 25` | `0x19` | 1 | `uint8` | 对兵种系 25；字段策略 Editable |
| `对兵种系 26` | `0x1A` | 1 | `uint8` | 对兵种系 26；字段策略 Editable |
| `对兵种系 27` | `0x1B` | 1 | `uint8` | 对兵种系 27；字段策略 Editable |
| `对兵种系 28` | `0x1C` | 1 | `uint8` | 对兵种系 28；字段策略 Editable |
| `对兵种系 29` | `0x1D` | 1 | `uint8` | 对兵种系 29；字段策略 Editable |
| `对兵种系 30` | `0x1E` | 1 | `uint8` | 对兵种系 30；字段策略 Editable |
| `对兵种系 31` | `0x1F` | 1 | `uint8` | 对兵种系 31；字段策略 Editable |
| `对兵种系 32` | `0x20` | 1 | `uint8` | 对兵种系 32；字段策略 Editable |
| `对兵种系 33` | `0x21` | 1 | `uint8` | 对兵种系 33；字段策略 Editable |
| `对兵种系 34` | `0x22` | 1 | `uint8` | 对兵种系 34；字段策略 Editable |
| `对兵种系 35` | `0x23` | 1 | `uint8` | 对兵种系 35；字段策略 Editable |
| `对兵种系 36` | `0x24` | 1 | `uint8` | 对兵种系 36；字段策略 Editable |
| `对兵种系 37` | `0x25` | 1 | `uint8` | 对兵种系 37；字段策略 Editable |
| `对兵种系 38` | `0x26` | 1 | `uint8` | 对兵种系 38；字段策略 Editable |
| `对兵种系 39` | `0x27` | 1 | `uint8` | 对兵种系 39；字段策略 Editable |

## 66-legacy-data-v1 兵种系·兵种属性（job-series-attributes 物理表）

ID: `struct.66.disk.66-legacy-data-v1.job-series-attributes`；状态: `canonical`；证据: `source-reviewed`

步长: `0x28` (40)

索引公式: `Ekd5.exe + 0xA38C0 + (ID - 0) * 0x28 + field_offset; ID=0..7`

存储：`Ekd5.exe`；起点：`0xA38C0` (fileOffset)；记录数：`8`；ID 起点：`0`；结束偏移（不含）：`0xA3A00`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 行号和 UInt8 几何来自读取器与 Profile；移动声音、移动速度、攻击声音、兵种类型的枚举名称由用户确认，未冒充逆向或引擎运行时验证。未列出的数值保留数字并允许按字段边界编辑。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 属性行 ID | 名称 | 值语义 | 语义来源 |
|---:|---|---|---|
| 0 | 移动声音 | 0：马蹄；1：车轮；2：脚步；3：无声；4：引擎；5：预设1；6：预设2 | `user-confirmed-semantics` |
| 1 | 移动速度 | 0：快速；1：慢速 | `user-confirmed-semantics` |
| 2 | 攻击声音 | 0：剑；1：其他；2：爆炸1；3：爆炸2；4：火箭筒；5：枪声（连射）；6：枪声（点射）；7：火焰喷射；8：毒气喷射 | `user-confirmed-semantics` |
| 3 | 远程兵种 | 未在此确认 | `source-reviewed-row-label` |
| 4 | 攻击延迟 | 未在此确认 | `source-reviewed-row-label` |
| 5 | 兵种类型 | 0：全能；1：文官；2：武将 | `user-confirmed-semantics` |
| 6 | 策略伤害 | 未在此确认 | `source-reviewed-row-label` |
| 7 | 参与围攻 | 未在此确认 | `source-reviewed-row-label` |

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `兵种系 0` | `0x0` | 1 | `uint8` | 兵种系 0；字段策略 Editable |
| `兵种系 1` | `0x1` | 1 | `uint8` | 兵种系 1；字段策略 Editable |
| `兵种系 2` | `0x2` | 1 | `uint8` | 兵种系 2；字段策略 Editable |
| `兵种系 3` | `0x3` | 1 | `uint8` | 兵种系 3；字段策略 Editable |
| `兵种系 4` | `0x4` | 1 | `uint8` | 兵种系 4；字段策略 Editable |
| `兵种系 5` | `0x5` | 1 | `uint8` | 兵种系 5；字段策略 Editable |
| `兵种系 6` | `0x6` | 1 | `uint8` | 兵种系 6；字段策略 Editable |
| `兵种系 7` | `0x7` | 1 | `uint8` | 兵种系 7；字段策略 Editable |
| `兵种系 8` | `0x8` | 1 | `uint8` | 兵种系 8；字段策略 Editable |
| `兵种系 9` | `0x9` | 1 | `uint8` | 兵种系 9；字段策略 Editable |
| `兵种系 10` | `0xA` | 1 | `uint8` | 兵种系 10；字段策略 Editable |
| `兵种系 11` | `0xB` | 1 | `uint8` | 兵种系 11；字段策略 Editable |
| `兵种系 12` | `0xC` | 1 | `uint8` | 兵种系 12；字段策略 Editable |
| `兵种系 13` | `0xD` | 1 | `uint8` | 兵种系 13；字段策略 Editable |
| `兵种系 14` | `0xE` | 1 | `uint8` | 兵种系 14；字段策略 Editable |
| `兵种系 15` | `0xF` | 1 | `uint8` | 兵种系 15；字段策略 Editable |
| `兵种系 16` | `0x10` | 1 | `uint8` | 兵种系 16；字段策略 Editable |
| `兵种系 17` | `0x11` | 1 | `uint8` | 兵种系 17；字段策略 Editable |
| `兵种系 18` | `0x12` | 1 | `uint8` | 兵种系 18；字段策略 Editable |
| `兵种系 19` | `0x13` | 1 | `uint8` | 兵种系 19；字段策略 Editable |
| `兵种系 20` | `0x14` | 1 | `uint8` | 兵种系 20；字段策略 Editable |
| `兵种系 21` | `0x15` | 1 | `uint8` | 兵种系 21；字段策略 Editable |
| `兵种系 22` | `0x16` | 1 | `uint8` | 兵种系 22；字段策略 Editable |
| `兵种系 23` | `0x17` | 1 | `uint8` | 兵种系 23；字段策略 Editable |
| `兵种系 24` | `0x18` | 1 | `uint8` | 兵种系 24；字段策略 Editable |
| `兵种系 25` | `0x19` | 1 | `uint8` | 兵种系 25；字段策略 Editable |
| `兵种系 26` | `0x1A` | 1 | `uint8` | 兵种系 26；字段策略 Editable |
| `兵种系 27` | `0x1B` | 1 | `uint8` | 兵种系 27；字段策略 Editable |
| `兵种系 28` | `0x1C` | 1 | `uint8` | 兵种系 28；字段策略 Editable |
| `兵种系 29` | `0x1D` | 1 | `uint8` | 兵种系 29；字段策略 Editable |
| `兵种系 30` | `0x1E` | 1 | `uint8` | 兵种系 30；字段策略 Editable |
| `兵种系 31` | `0x1F` | 1 | `uint8` | 兵种系 31；字段策略 Editable |
| `兵种系 32` | `0x20` | 1 | `uint8` | 兵种系 32；字段策略 Editable |
| `兵种系 33` | `0x21` | 1 | `uint8` | 兵种系 33；字段策略 Editable |
| `兵种系 34` | `0x22` | 1 | `uint8` | 兵种系 34；字段策略 Editable |
| `兵种系 35` | `0x23` | 1 | `uint8` | 兵种系 35；字段策略 Editable |
| `兵种系 36` | `0x24` | 1 | `uint8` | 兵种系 36；字段策略 Editable |
| `兵种系 37` | `0x25` | 1 | `uint8` | 兵种系 37；字段策略 Editable |
| `兵种系 38` | `0x26` | 1 | `uint8` | 兵种系 38；字段策略 Editable |
| `兵种系 39` | `0x27` | 1 | `uint8` | 兵种系 39；字段策略 Editable |

## 66-legacy-data-v1 兵种（detailed-jobs 物理表）

ID: `struct.66.disk.66-legacy-data-v1.detailed-jobs`；状态: `canonical`；证据: `source-reviewed`

步长: `0x9` (9)

索引公式: `Ekd5.exe + 0xD18D0 + (ID - 0) * 0x9 + field_offset; ID=0..79`

存储：`Ekd5.exe`；起点：`0xD18D0` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0xD1BA0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 9 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 兵种说明（detailed-job-description 物理表）

ID: `struct.66.disk.66-legacy-data-v1.detailed-job-description`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x11170 + (ID - 0) * 0xC8 + field_offset; ID=0..79`

存储：`Imsg.e5`；起点：`0x11170` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0x14FF0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `兵种说明` | `0x0` | 200 | `fixed-string` | 兵种说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 兵种成长与装备（detailed-job-growth 物理表）

ID: `struct.66.disk.66-legacy-data-v1.detailed-job-growth`；状态: `canonical`；证据: `source-reviewed`

步长: `0x23` (35)

索引公式: `Data.e5 + 0x9DB4 + (ID - 0) * 0x23 + field_offset; ID=0..79`

存储：`Data.e5`；起点：`0x9DB4` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0xA8A4`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `移动力成长` | `0x0` | 1 | `uint8` | 移动力成长；字段策略 Editable |
| `攻击范围` | `0x1` | 1 | `uint8` | 攻击范围；字段策略 Editable |
| `攻击成长` | `0x2` | 1 | `uint8` | 攻击成长；字段策略 Editable |
| `防御成长` | `0x3` | 1 | `uint8` | 防御成长；字段策略 Editable |
| `精神成长` | `0x4` | 1 | `uint8` | 精神成长；字段策略 Editable |
| `爆发成长` | `0x5` | 1 | `uint8` | 爆发成长；字段策略 Editable |
| `士气成长` | `0x6` | 1 | `uint8` | 士气成长；字段策略 Editable |
| `HP成长` | `0x7` | 1 | `uint8` | HP成长；字段策略 Editable |
| `MP成长` | `0x8` | 1 | `uint8` | MP成长；字段策略 Editable |
| `普通剑` | `0x9` | 1 | `uint8` | 普通剑；字段策略 Editable |
| `特殊剑` | `0xA` | 1 | `uint8` | 特殊剑；字段策略 Editable |
| `普通枪` | `0xB` | 1 | `uint8` | 普通枪；字段策略 Editable |
| `特殊枪` | `0xC` | 1 | `uint8` | 特殊枪；字段策略 Editable |
| `普通弓` | `0xD` | 1 | `uint8` | 普通弓；字段策略 Editable |
| `特殊弓` | `0xE` | 1 | `uint8` | 特殊弓；字段策略 Editable |
| `普通刀` | `0xF` | 1 | `uint8` | 普通刀；字段策略 Editable |
| `特殊刀` | `0x10` | 1 | `uint8` | 特殊刀；字段策略 Editable |
| `普通炮车` | `0x11` | 1 | `uint8` | 普通炮车；字段策略 Editable |
| `特殊炮车` | `0x12` | 1 | `uint8` | 特殊炮车；字段策略 Editable |
| `普通锤` | `0x13` | 1 | `uint8` | 普通锤；字段策略 Editable |
| `特殊锤` | `0x14` | 1 | `uint8` | 特殊锤；字段策略 Editable |
| `普通斧` | `0x15` | 1 | `uint8` | 普通斧；字段策略 Editable |
| `特殊斧` | `0x16` | 1 | `uint8` | 特殊斧；字段策略 Editable |
| `普通扇` | `0x17` | 1 | `uint8` | 普通扇；字段策略 Editable |
| `特殊扇` | `0x18` | 1 | `uint8` | 特殊扇；字段策略 Editable |
| `普通宝剑` | `0x19` | 1 | `uint8` | 普通宝剑；字段策略 Editable |
| `特殊宝剑` | `0x1A` | 1 | `uint8` | 特殊宝剑；字段策略 Editable |
| `普通将剑` | `0x1B` | 1 | `uint8` | 普通将剑；字段策略 Editable |
| `特殊将剑` | `0x1C` | 1 | `uint8` | 特殊将剑；字段策略 Editable |
| `普通铠甲` | `0x1D` | 1 | `uint8` | 普通铠甲；字段策略 Editable |
| `特殊铠甲` | `0x1E` | 1 | `uint8` | 特殊铠甲；字段策略 Editable |
| `普通衣服` | `0x1F` | 1 | `uint8` | 普通衣服；字段策略 Editable |
| `特殊衣服` | `0x20` | 1 | `uint8` | 特殊衣服；字段策略 Editable |
| `普通袍服` | `0x21` | 1 | `uint8` | 普通袍服；字段策略 Editable |
| `特殊袍服` | `0x22` | 1 | `uint8` | 特殊袍服；字段策略 Editable |

## 66-legacy-data-v1 兵种穿透（detailed-job-penetration 物理表）

ID: `struct.66.disk.66-legacy-data-v1.detailed-job-penetration`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0x6C81 + (ID - 0) * 0x1 + field_offset; ID=0..79`

存储：`Ekd5.exe`；起点：`0x6C81` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0x6CD1`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `穿透` | `0x0` | 1 | `uint8` | 穿透；字段策略 Editable |

## 66-legacy-data-v1 策略（strategies 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategies`；状态: `canonical`；证据: `source-reviewed`

步长: `0x61` (97)

索引公式: `Data.e5 + 0xB204 + (ID - 0) * 0x61 + field_offset; ID=0..143`

存储：`Data.e5`；起点：`0xB204` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xE894`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 11 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `策略类型` | `0xB` | 1 | `uint8` | 策略类型；字段策略 Editable |
| `施展对象` | `0xC` | 1 | `uint8` | 施展对象；字段策略 Editable |
| `施法范围` | `0xD` | 1 | `uint8` | 施法范围；字段策略 Editable |
| `穿透范围` | `0xE` | 1 | `uint8` | 穿透范围；字段策略 Editable |
| `策略消耗` | `0xF` | 1 | `uint8` | 策略消耗；字段策略 Editable |
| `策略图标` | `0x10` | 1 | `uint8` | 策略图标；字段策略 Editable |
| `兵种00学习等级` | `0x11` | 1 | `uint8` | 兵种00学习等级；字段策略 Editable |
| `兵种01学习等级` | `0x12` | 1 | `uint8` | 兵种01学习等级；字段策略 Editable |
| `兵种02学习等级` | `0x13` | 1 | `uint8` | 兵种02学习等级；字段策略 Editable |
| `兵种03学习等级` | `0x14` | 1 | `uint8` | 兵种03学习等级；字段策略 Editable |
| `兵种04学习等级` | `0x15` | 1 | `uint8` | 兵种04学习等级；字段策略 Editable |
| `兵种05学习等级` | `0x16` | 1 | `uint8` | 兵种05学习等级；字段策略 Editable |
| `兵种06学习等级` | `0x17` | 1 | `uint8` | 兵种06学习等级；字段策略 Editable |
| `兵种07学习等级` | `0x18` | 1 | `uint8` | 兵种07学习等级；字段策略 Editable |
| `兵种08学习等级` | `0x19` | 1 | `uint8` | 兵种08学习等级；字段策略 Editable |
| `兵种09学习等级` | `0x1A` | 1 | `uint8` | 兵种09学习等级；字段策略 Editable |
| `兵种10学习等级` | `0x1B` | 1 | `uint8` | 兵种10学习等级；字段策略 Editable |
| `兵种11学习等级` | `0x1C` | 1 | `uint8` | 兵种11学习等级；字段策略 Editable |
| `兵种12学习等级` | `0x1D` | 1 | `uint8` | 兵种12学习等级；字段策略 Editable |
| `兵种13学习等级` | `0x1E` | 1 | `uint8` | 兵种13学习等级；字段策略 Editable |
| `兵种14学习等级` | `0x1F` | 1 | `uint8` | 兵种14学习等级；字段策略 Editable |
| `兵种15学习等级` | `0x20` | 1 | `uint8` | 兵种15学习等级；字段策略 Editable |
| `兵种16学习等级` | `0x21` | 1 | `uint8` | 兵种16学习等级；字段策略 Editable |
| `兵种17学习等级` | `0x22` | 1 | `uint8` | 兵种17学习等级；字段策略 Editable |
| `兵种18学习等级` | `0x23` | 1 | `uint8` | 兵种18学习等级；字段策略 Editable |
| `兵种19学习等级` | `0x24` | 1 | `uint8` | 兵种19学习等级；字段策略 Editable |
| `兵种20学习等级` | `0x25` | 1 | `uint8` | 兵种20学习等级；字段策略 Editable |
| `兵种21学习等级` | `0x26` | 1 | `uint8` | 兵种21学习等级；字段策略 Editable |
| `兵种22学习等级` | `0x27` | 1 | `uint8` | 兵种22学习等级；字段策略 Editable |
| `兵种23学习等级` | `0x28` | 1 | `uint8` | 兵种23学习等级；字段策略 Editable |
| `兵种24学习等级` | `0x29` | 1 | `uint8` | 兵种24学习等级；字段策略 Editable |
| `兵种25学习等级` | `0x2A` | 1 | `uint8` | 兵种25学习等级；字段策略 Editable |
| `兵种26学习等级` | `0x2B` | 1 | `uint8` | 兵种26学习等级；字段策略 Editable |
| `兵种27学习等级` | `0x2C` | 1 | `uint8` | 兵种27学习等级；字段策略 Editable |
| `兵种28学习等级` | `0x2D` | 1 | `uint8` | 兵种28学习等级；字段策略 Editable |
| `兵种29学习等级` | `0x2E` | 1 | `uint8` | 兵种29学习等级；字段策略 Editable |
| `兵种30学习等级` | `0x2F` | 1 | `uint8` | 兵种30学习等级；字段策略 Editable |
| `兵种31学习等级` | `0x30` | 1 | `uint8` | 兵种31学习等级；字段策略 Editable |
| `兵种32学习等级` | `0x31` | 1 | `uint8` | 兵种32学习等级；字段策略 Editable |
| `兵种33学习等级` | `0x32` | 1 | `uint8` | 兵种33学习等级；字段策略 Editable |
| `兵种34学习等级` | `0x33` | 1 | `uint8` | 兵种34学习等级；字段策略 Editable |
| `兵种35学习等级` | `0x34` | 1 | `uint8` | 兵种35学习等级；字段策略 Editable |
| `兵种36学习等级` | `0x35` | 1 | `uint8` | 兵种36学习等级；字段策略 Editable |
| `兵种37学习等级` | `0x36` | 1 | `uint8` | 兵种37学习等级；字段策略 Editable |
| `兵种38学习等级` | `0x37` | 1 | `uint8` | 兵种38学习等级；字段策略 Editable |
| `兵种39学习等级` | `0x38` | 1 | `uint8` | 兵种39学习等级；字段策略 Editable |
| `兵种40学习等级` | `0x39` | 1 | `uint8` | 兵种40学习等级；字段策略 Editable |
| `兵种41学习等级` | `0x3A` | 1 | `uint8` | 兵种41学习等级；字段策略 Editable |
| `兵种42学习等级` | `0x3B` | 1 | `uint8` | 兵种42学习等级；字段策略 Editable |
| `兵种43学习等级` | `0x3C` | 1 | `uint8` | 兵种43学习等级；字段策略 Editable |
| `兵种44学习等级` | `0x3D` | 1 | `uint8` | 兵种44学习等级；字段策略 Editable |
| `兵种45学习等级` | `0x3E` | 1 | `uint8` | 兵种45学习等级；字段策略 Editable |
| `兵种46学习等级` | `0x3F` | 1 | `uint8` | 兵种46学习等级；字段策略 Editable |
| `兵种47学习等级` | `0x40` | 1 | `uint8` | 兵种47学习等级；字段策略 Editable |
| `兵种48学习等级` | `0x41` | 1 | `uint8` | 兵种48学习等级；字段策略 Editable |
| `兵种49学习等级` | `0x42` | 1 | `uint8` | 兵种49学习等级；字段策略 Editable |
| `兵种50学习等级` | `0x43` | 1 | `uint8` | 兵种50学习等级；字段策略 Editable |
| `兵种51学习等级` | `0x44` | 1 | `uint8` | 兵种51学习等级；字段策略 Editable |
| `兵种52学习等级` | `0x45` | 1 | `uint8` | 兵种52学习等级；字段策略 Editable |
| `兵种53学习等级` | `0x46` | 1 | `uint8` | 兵种53学习等级；字段策略 Editable |
| `兵种54学习等级` | `0x47` | 1 | `uint8` | 兵种54学习等级；字段策略 Editable |
| `兵种55学习等级` | `0x48` | 1 | `uint8` | 兵种55学习等级；字段策略 Editable |
| `兵种56学习等级` | `0x49` | 1 | `uint8` | 兵种56学习等级；字段策略 Editable |
| `兵种57学习等级` | `0x4A` | 1 | `uint8` | 兵种57学习等级；字段策略 Editable |
| `兵种58学习等级` | `0x4B` | 1 | `uint8` | 兵种58学习等级；字段策略 Editable |
| `兵种59学习等级` | `0x4C` | 1 | `uint8` | 兵种59学习等级；字段策略 Editable |
| `兵种60学习等级` | `0x4D` | 1 | `uint8` | 兵种60学习等级；字段策略 Editable |
| `兵种61学习等级` | `0x4E` | 1 | `uint8` | 兵种61学习等级；字段策略 Editable |
| `兵种62学习等级` | `0x4F` | 1 | `uint8` | 兵种62学习等级；字段策略 Editable |
| `兵种63学习等级` | `0x50` | 1 | `uint8` | 兵种63学习等级；字段策略 Editable |
| `兵种64学习等级` | `0x51` | 1 | `uint8` | 兵种64学习等级；字段策略 Editable |
| `兵种65学习等级` | `0x52` | 1 | `uint8` | 兵种65学习等级；字段策略 Editable |
| `兵种66学习等级` | `0x53` | 1 | `uint8` | 兵种66学习等级；字段策略 Editable |
| `兵种67学习等级` | `0x54` | 1 | `uint8` | 兵种67学习等级；字段策略 Editable |
| `兵种68学习等级` | `0x55` | 1 | `uint8` | 兵种68学习等级；字段策略 Editable |
| `兵种69学习等级` | `0x56` | 1 | `uint8` | 兵种69学习等级；字段策略 Editable |
| `兵种70学习等级` | `0x57` | 1 | `uint8` | 兵种70学习等级；字段策略 Editable |
| `兵种71学习等级` | `0x58` | 1 | `uint8` | 兵种71学习等级；字段策略 Editable |
| `兵种72学习等级` | `0x59` | 1 | `uint8` | 兵种72学习等级；字段策略 Editable |
| `兵种73学习等级` | `0x5A` | 1 | `uint8` | 兵种73学习等级；字段策略 Editable |
| `兵种74学习等级` | `0x5B` | 1 | `uint8` | 兵种74学习等级；字段策略 Editable |
| `兵种75学习等级` | `0x5C` | 1 | `uint8` | 兵种75学习等级；字段策略 Editable |
| `兵种76学习等级` | `0x5D` | 1 | `uint8` | 兵种76学习等级；字段策略 Editable |
| `兵种77学习等级` | `0x5E` | 1 | `uint8` | 兵种77学习等级；字段策略 Editable |
| `兵种78学习等级` | `0x5F` | 1 | `uint8` | 兵种78学习等级；字段策略 Editable |
| `兵种79学习等级` | `0x60` | 1 | `uint8` | 兵种79学习等级；字段策略 Editable |

## 66-legacy-data-v1 策略说明（strategy-description 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-description`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x0 + (ID - 0) * 0xC8 + field_offset; ID=0..143`

存储：`Imsg.e5`；起点：`0x0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0x7080`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略说明` | `0x0` | 200 | `fixed-string` | 策略说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 策略扩展标记（strategy-extension 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-extension`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2CE0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2CE0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2D70`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-legacy-data-v1 策略伤害类型（strategy-damage-type 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-damage-type`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA30D0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA30D0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3160`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-legacy-data-v1 策略伤害系数（strategy-damage-ratio 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-damage-ratio`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA3040 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA3040` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA30D0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-legacy-data-v1 策略命中率（strategy-hit-rate 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-hit-rate`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2F20 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2F20` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2FB0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-legacy-data-v1 效果索引（strategy-learning 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-learning`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2FB0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2FB0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3040`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-legacy-data-v1 战场AI策略限制（strategy-battle-ai 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-battle-ai`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2E00 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2E00` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2E90`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-legacy-data-v1 练武场AI策略限制（strategy-training-ai 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-training-ai`；状态: `canonical`；证据: `source-reviewed`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2E90 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2E90` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2F20`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-legacy-data-v1 兵种特效分配（class-effects 物理表）

ID: `struct.66.disk.66-legacy-data-v1.class-effects`；状态: `canonical`；证据: `source-reviewed`

步长: `0x8` (8)

索引公式: `Ekd5.exe + 0xD9000 + (ID - 0) * 0x8 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0xD9000` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0xD97F8`。

能力：`Editable`；Codec：`effect-65-8-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `一号武将` | `0x0` | 2 | `uint16le` | 一号武将；字段策略 Editable；引用 persons |
| `二号武将` | `0x2` | 2 | `uint16le` | 二号武将；字段策略 Editable；引用 persons |
| `三号武将` | `0x4` | 2 | `uint16le` | 三号武将；字段策略 Editable；引用 persons |
| `兵种` | `0x6` | 1 | `uint8` | 兵种；字段策略 Editable；引用 detailed-jobs |
| `特效值` | `0x7` | 1 | `uint8` | 特效值；字段策略 Editable |

## 66-legacy-data-v1 人物专属、套装专属（personal-effects 物理表）

ID: `struct.66.disk.66-legacy-data-v1.personal-effects`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0xDF800 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0xDF800` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0xE07F0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `武将1` | `0x0` | 2 | `uint16le` | 武将1；字段策略 Editable；引用 persons |
| `装备1` | `0x2` | 1 | `uint8` | 装备1；字段策略 Editable；引用 items |
| `特效值1` | `0x3` | 1 | `uint8` | 特效值1；字段策略 Editable |
| `武将2` | `0x4` | 2 | `uint16le` | 武将2；字段策略 Editable；引用 persons |
| `装备2` | `0x6` | 1 | `uint8` | 装备2；字段策略 Editable；引用 items |
| `特效值2` | `0x7` | 1 | `uint8` | 特效值2；字段策略 Editable |
| `装备3-1` | `0x8` | 1 | `uint8` | 装备3-1；字段策略 Editable；引用 items |
| `装备3-2` | `0x9` | 1 | `uint8` | 装备3-2；字段策略 Editable；引用 items |
| `装备3-3` | `0xA` | 1 | `uint8` | 装备3-3；字段策略 Editable；引用 items |
| `特效值3` | `0xB` | 1 | `uint8` | 特效值3；字段策略 Editable |
| `装备4-1` | `0xC` | 1 | `uint8` | 装备4-1；字段策略 Editable；引用 items |
| `装备4-2` | `0xD` | 1 | `uint8` | 装备4-2；字段策略 Editable；引用 items |
| `装备4-3` | `0xE` | 1 | `uint8` | 装备4-3；字段策略 Editable；引用 items |
| `特效值4` | `0xF` | 1 | `uint8` | 特效值4；字段策略 Editable |

## 66-legacy-data-v1 人物暴击台词（person-critical-quotes 物理表）

ID: `struct.66.disk.66-legacy-data-v1.person-critical-quotes`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x222E0 + (ID - 0) * 0xC8 + field_offset; ID=0..98`

存储：`Imsg.e5`；起点：`0x222E0` (fileOffset)；记录数：`99`；ID 起点：`0`；结束偏移（不含）：`0x27038`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `台词` | `0x0` | 200 | `fixed-string` | 台词；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 人物撤退台词（person-retreat-quotes 物理表）

ID: `struct.66.disk.66-legacy-data-v1.person-retreat-quotes`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x78050 + (ID - 0) * 0xC8 + field_offset; ID=0..48`

存储：`Imsg.e5`；起点：`0x78050` (fileOffset)；记录数：`49`；ID 起点：`0`；结束偏移（不含）：`0x7A698`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 只使用 +491600 的 49×200 区；+440200 仅用于旧区冲突诊断。450000 字节 Imsg 样本不满足边界，必须 unavailable。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | False | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `台词` | `0x0` | 200 | `fixed-string` | 台词；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 人物R形象指定（person-r-assign 物理表）

ID: `struct.66.disk.66-legacy-data-v1.person-r-assign`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x2` (2)

索引公式: `Ekd5.exe + 0xE1000 + (ID - 0) * 0x2 + field_offset; ID=0..1023`

存储：`Ekd5.exe`；起点：`0xE1000` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0xE1800`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `R形象ID` | `0x0` | 2 | `uint16le` | R形象ID；字段策略 Editable |

## 66-legacy-data-v1 人物S形象指定（person-s-assign 物理表）

ID: `struct.66.disk.66-legacy-data-v1.person-s-assign`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x2` (2)

索引公式: `Ekd5.exe + 0xD2800 + (ID - 0) * 0x2 + field_offset; ID=0..1023`

存储：`Ekd5.exe`；起点：`0xD2800` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0xD3000`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `S形象ID` | `0x0` | 2 | `uint16le` | S形象ID；字段策略 Editable |

## 66-legacy-data-v1 战役名称（scenario-names 物理表）

ID: `struct.66.disk.66-legacy-data-v1.scenario-names`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0xC350 + (ID - 0) * 0xC8 + field_offset; ID=0..98`

存储：`Imsg.e5`；起点：`0xC350` (fileOffset)；记录数：`99`；ID 起点：`0`；结束偏移（不含）：`0x110A8`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `战役名称` | `0x0` | 200 | `fixed-string` | 战役名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 商店数据（shops 物理表）

ID: `struct.66.disk.66-legacy-data-v1.shops`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x24` (36)

索引公式: `Data.e5 + 0x8BB4 + (ID - 0) * 0x24 + field_offset; ID=0..127`

存储：`Data.e5`；起点：`0x8BB4` (fileOffset)；记录数：`128`；ID 起点：`0`；结束偏移（不含）：`0x9DB4`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `开关仓库人物` | `0x0` | 2 | `uint16le` | 开关仓库人物；字段策略 Editable；引用 persons |
| `买卖物品人物` | `0x2` | 2 | `uint16le` | 买卖物品人物；字段策略 Editable；引用 persons |
| `装备0` | `0x4` | 1 | `uint8` | 装备0；字段策略 Editable；引用 items |
| `装备1` | `0x5` | 1 | `uint8` | 装备1；字段策略 Editable；引用 items |
| `装备2` | `0x6` | 1 | `uint8` | 装备2；字段策略 Editable；引用 items |
| `装备3` | `0x7` | 1 | `uint8` | 装备3；字段策略 Editable；引用 items |
| `装备4` | `0x8` | 1 | `uint8` | 装备4；字段策略 Editable；引用 items |
| `装备5` | `0x9` | 1 | `uint8` | 装备5；字段策略 Editable；引用 items |
| `装备6` | `0xA` | 1 | `uint8` | 装备6；字段策略 Editable；引用 items |
| `装备7` | `0xB` | 1 | `uint8` | 装备7；字段策略 Editable；引用 items |
| `装备8` | `0xC` | 1 | `uint8` | 装备8；字段策略 Editable；引用 items |
| `装备9` | `0xD` | 1 | `uint8` | 装备9；字段策略 Editable；引用 items |
| `装备10` | `0xE` | 1 | `uint8` | 装备10；字段策略 Editable；引用 items |
| `装备11` | `0xF` | 1 | `uint8` | 装备11；字段策略 Editable；引用 items |
| `装备12` | `0x10` | 1 | `uint8` | 装备12；字段策略 Editable；引用 items |
| `装备13` | `0x11` | 1 | `uint8` | 装备13；字段策略 Editable；引用 items |
| `装备14` | `0x12` | 1 | `uint8` | 装备14；字段策略 Editable；引用 items |
| `装备15` | `0x13` | 1 | `uint8` | 装备15；字段策略 Editable；引用 items |
| `物品0` | `0x14` | 1 | `uint8` | 物品0；字段策略 Editable；引用 items |
| `物品1` | `0x15` | 1 | `uint8` | 物品1；字段策略 Editable；引用 items |
| `物品2` | `0x16` | 1 | `uint8` | 物品2；字段策略 Editable；引用 items |
| `物品3` | `0x17` | 1 | `uint8` | 物品3；字段策略 Editable；引用 items |
| `物品4` | `0x18` | 1 | `uint8` | 物品4；字段策略 Editable；引用 items |
| `物品5` | `0x19` | 1 | `uint8` | 物品5；字段策略 Editable；引用 items |
| `物品6` | `0x1A` | 1 | `uint8` | 物品6；字段策略 Editable；引用 items |
| `物品7` | `0x1B` | 1 | `uint8` | 物品7；字段策略 Editable；引用 items |
| `物品8` | `0x1C` | 1 | `uint8` | 物品8；字段策略 Editable；引用 items |
| `物品9` | `0x1D` | 1 | `uint8` | 物品9；字段策略 Editable；引用 items |
| `物品10` | `0x1E` | 1 | `uint8` | 物品10；字段策略 Editable；引用 items |
| `物品11` | `0x1F` | 1 | `uint8` | 物品11；字段策略 Editable；引用 items |
| `物品12` | `0x20` | 1 | `uint8` | 物品12；字段策略 Editable；引用 items |
| `物品13` | `0x21` | 1 | `uint8` | 物品13；字段策略 Editable；引用 items |
| `物品14` | `0x22` | 1 | `uint8` | 物品14；字段策略 Editable；引用 items |
| `物品15` | `0x23` | 1 | `uint8` | 物品15；字段策略 Editable；引用 items |

## 66-legacy-data-v1 兵种特效名称（effect-names 物理表）

ID: `struct.66.disk.66-legacy-data-v1.effect-names`；状态: `canonical`；证据: `source-reviewed`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0x9E800 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0x9E800` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x9F7F0`。

能力：`ReadOnly`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.5 兵种特效名称原始名称区，行尾可能含额外参数；使用专用名称池解析，物理表只读。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 16 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 兵种特效说明（effect-descriptions 物理表）

ID: `struct.66.disk.66-legacy-data-v1.effect-descriptions`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x14FF0 + (ID - 0) * 0xC8 + field_offset; ID=0..254`

存储：`Imsg.e5`；起点：`0x14FF0` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x21728`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `说明` | `0x0` | 200 | `fixed-string` | 说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 人物特效拓展（effect-archive 物理表）

ID: `struct.66.disk.66-legacy-data-v1.effect-archive`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x400` (1024)

索引公式: `Effect.e5 + 0x0 + (ID - 0) * 0x400 + field_offset; ID=0..1023`

存储：`Effect.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x100000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `槽0特效号` | `0x0` | 1 | `uint8` | 槽0特效号；字段策略 Editable |
| `槽1特效号` | `0x4` | 1 | `uint8` | 槽1特效号；字段策略 Editable |
| `槽2特效号` | `0x8` | 1 | `uint8` | 槽2特效号；字段策略 Editable |
| `槽3特效号` | `0xC` | 1 | `uint8` | 槽3特效号；字段策略 Editable |
| `槽4特效号` | `0x10` | 1 | `uint8` | 槽4特效号；字段策略 Editable |
| `槽5特效号` | `0x14` | 1 | `uint8` | 槽5特效号；字段策略 Editable |
| `槽6特效号` | `0x18` | 1 | `uint8` | 槽6特效号；字段策略 Editable |
| `槽7特效号` | `0x1C` | 1 | `uint8` | 槽7特效号；字段策略 Editable |
| `槽8特效号` | `0x20` | 1 | `uint8` | 槽8特效号；字段策略 Editable |
| `槽9特效号` | `0x24` | 1 | `uint8` | 槽9特效号；字段策略 Editable |
| `槽10特效号` | `0x28` | 1 | `uint8` | 槽10特效号；字段策略 Editable |
| `槽11特效号` | `0x2C` | 1 | `uint8` | 槽11特效号；字段策略 Editable |
| `槽12特效号` | `0x30` | 1 | `uint8` | 槽12特效号；字段策略 Editable |
| `槽13特效号` | `0x34` | 1 | `uint8` | 槽13特效号；字段策略 Editable |
| `槽14特效号` | `0x38` | 1 | `uint8` | 槽14特效号；字段策略 Editable |
| `槽15特效号` | `0x3C` | 1 | `uint8` | 槽15特效号；字段策略 Editable |
| `槽16特效号` | `0x40` | 1 | `uint8` | 槽16特效号；字段策略 Editable |
| `槽17特效号` | `0x44` | 1 | `uint8` | 槽17特效号；字段策略 Editable |
| `槽18特效号` | `0x48` | 1 | `uint8` | 槽18特效号；字段策略 Editable |
| `槽19特效号` | `0x4C` | 1 | `uint8` | 槽19特效号；字段策略 Editable |
| `槽20特效号` | `0x50` | 1 | `uint8` | 槽20特效号；字段策略 Editable |
| `槽21特效号` | `0x54` | 1 | `uint8` | 槽21特效号；字段策略 Editable |
| `槽22特效号` | `0x58` | 1 | `uint8` | 槽22特效号；字段策略 Editable |
| `槽23特效号` | `0x5C` | 1 | `uint8` | 槽23特效号；字段策略 Editable |
| `槽24特效号` | `0x60` | 1 | `uint8` | 槽24特效号；字段策略 Editable |
| `槽25特效号` | `0x64` | 1 | `uint8` | 槽25特效号；字段策略 Editable |
| `槽26特效号` | `0x68` | 1 | `uint8` | 槽26特效号；字段策略 Editable |
| `槽27特效号` | `0x6C` | 1 | `uint8` | 槽27特效号；字段策略 Editable |
| `槽28特效号` | `0x70` | 1 | `uint8` | 槽28特效号；字段策略 Editable |
| `槽29特效号` | `0x74` | 1 | `uint8` | 槽29特效号；字段策略 Editable |
| `槽30特效号` | `0x78` | 1 | `uint8` | 槽30特效号；字段策略 Editable |
| `槽31特效号` | `0x7C` | 1 | `uint8` | 槽31特效号；字段策略 Editable |
| `槽32特效号` | `0x80` | 1 | `uint8` | 槽32特效号；字段策略 Editable |
| `槽33特效号` | `0x84` | 1 | `uint8` | 槽33特效号；字段策略 Editable |
| `槽34特效号` | `0x88` | 1 | `uint8` | 槽34特效号；字段策略 Editable |
| `槽35特效号` | `0x8C` | 1 | `uint8` | 槽35特效号；字段策略 Editable |
| `槽36特效号` | `0x90` | 1 | `uint8` | 槽36特效号；字段策略 Editable |
| `槽37特效号` | `0x94` | 1 | `uint8` | 槽37特效号；字段策略 Editable |
| `槽38特效号` | `0x98` | 1 | `uint8` | 槽38特效号；字段策略 Editable |
| `槽39特效号` | `0x9C` | 1 | `uint8` | 槽39特效号；字段策略 Editable |
| `槽40特效号` | `0xA0` | 1 | `uint8` | 槽40特效号；字段策略 Editable |
| `槽41特效号` | `0xA4` | 1 | `uint8` | 槽41特效号；字段策略 Editable |
| `槽42特效号` | `0xA8` | 1 | `uint8` | 槽42特效号；字段策略 Editable |
| `槽43特效号` | `0xAC` | 1 | `uint8` | 槽43特效号；字段策略 Editable |
| `槽44特效号` | `0xB0` | 1 | `uint8` | 槽44特效号；字段策略 Editable |
| `槽45特效号` | `0xB4` | 1 | `uint8` | 槽45特效号；字段策略 Editable |
| `槽46特效号` | `0xB8` | 1 | `uint8` | 槽46特效号；字段策略 Editable |
| `槽47特效号` | `0xBC` | 1 | `uint8` | 槽47特效号；字段策略 Editable |
| `槽48特效号` | `0xC0` | 1 | `uint8` | 槽48特效号；字段策略 Editable |
| `槽49特效号` | `0xC4` | 1 | `uint8` | 槽49特效号；字段策略 Editable |
| `槽50特效号` | `0xC8` | 1 | `uint8` | 槽50特效号；字段策略 Editable |
| `槽51特效号` | `0xCC` | 1 | `uint8` | 槽51特效号；字段策略 Editable |
| `槽52特效号` | `0xD0` | 1 | `uint8` | 槽52特效号；字段策略 Editable |
| `槽53特效号` | `0xD4` | 1 | `uint8` | 槽53特效号；字段策略 Editable |
| `槽54特效号` | `0xD8` | 1 | `uint8` | 槽54特效号；字段策略 Editable |
| `槽55特效号` | `0xDC` | 1 | `uint8` | 槽55特效号；字段策略 Editable |
| `槽56特效号` | `0xE0` | 1 | `uint8` | 槽56特效号；字段策略 Editable |
| `槽57特效号` | `0xE4` | 1 | `uint8` | 槽57特效号；字段策略 Editable |
| `槽58特效号` | `0xE8` | 1 | `uint8` | 槽58特效号；字段策略 Editable |
| `槽59特效号` | `0xEC` | 1 | `uint8` | 槽59特效号；字段策略 Editable |
| `槽60特效号` | `0xF0` | 1 | `uint8` | 槽60特效号；字段策略 Editable |
| `槽61特效号` | `0xF4` | 1 | `uint8` | 槽61特效号；字段策略 Editable |
| `槽62特效号` | `0xF8` | 1 | `uint8` | 槽62特效号；字段策略 Editable |
| `槽63特效号` | `0xFC` | 1 | `uint8` | 槽63特效号；字段策略 Editable |
| `槽64特效号` | `0x100` | 1 | `uint8` | 槽64特效号；字段策略 Editable |
| `槽65特效号` | `0x104` | 1 | `uint8` | 槽65特效号；字段策略 Editable |
| `槽66特效号` | `0x108` | 1 | `uint8` | 槽66特效号；字段策略 Editable |
| `槽67特效号` | `0x10C` | 1 | `uint8` | 槽67特效号；字段策略 Editable |
| `槽68特效号` | `0x110` | 1 | `uint8` | 槽68特效号；字段策略 Editable |
| `槽69特效号` | `0x114` | 1 | `uint8` | 槽69特效号；字段策略 Editable |
| `槽70特效号` | `0x118` | 1 | `uint8` | 槽70特效号；字段策略 Editable |
| `槽71特效号` | `0x11C` | 1 | `uint8` | 槽71特效号；字段策略 Editable |
| `槽72特效号` | `0x120` | 1 | `uint8` | 槽72特效号；字段策略 Editable |
| `槽73特效号` | `0x124` | 1 | `uint8` | 槽73特效号；字段策略 Editable |
| `槽74特效号` | `0x128` | 1 | `uint8` | 槽74特效号；字段策略 Editable |
| `槽75特效号` | `0x12C` | 1 | `uint8` | 槽75特效号；字段策略 Editable |
| `槽76特效号` | `0x130` | 1 | `uint8` | 槽76特效号；字段策略 Editable |
| `槽77特效号` | `0x134` | 1 | `uint8` | 槽77特效号；字段策略 Editable |
| `槽78特效号` | `0x138` | 1 | `uint8` | 槽78特效号；字段策略 Editable |
| `槽79特效号` | `0x13C` | 1 | `uint8` | 槽79特效号；字段策略 Editable |
| `槽80特效号` | `0x140` | 1 | `uint8` | 槽80特效号；字段策略 Editable |
| `槽81特效号` | `0x144` | 1 | `uint8` | 槽81特效号；字段策略 Editable |
| `槽82特效号` | `0x148` | 1 | `uint8` | 槽82特效号；字段策略 Editable |
| `槽83特效号` | `0x14C` | 1 | `uint8` | 槽83特效号；字段策略 Editable |
| `槽84特效号` | `0x150` | 1 | `uint8` | 槽84特效号；字段策略 Editable |
| `槽85特效号` | `0x154` | 1 | `uint8` | 槽85特效号；字段策略 Editable |
| `槽86特效号` | `0x158` | 1 | `uint8` | 槽86特效号；字段策略 Editable |
| `槽87特效号` | `0x15C` | 1 | `uint8` | 槽87特效号；字段策略 Editable |
| `槽88特效号` | `0x160` | 1 | `uint8` | 槽88特效号；字段策略 Editable |
| `槽89特效号` | `0x164` | 1 | `uint8` | 槽89特效号；字段策略 Editable |
| `槽90特效号` | `0x168` | 1 | `uint8` | 槽90特效号；字段策略 Editable |
| `槽91特效号` | `0x16C` | 1 | `uint8` | 槽91特效号；字段策略 Editable |
| `槽92特效号` | `0x170` | 1 | `uint8` | 槽92特效号；字段策略 Editable |
| `槽93特效号` | `0x174` | 1 | `uint8` | 槽93特效号；字段策略 Editable |
| `槽94特效号` | `0x178` | 1 | `uint8` | 槽94特效号；字段策略 Editable |
| `槽95特效号` | `0x17C` | 1 | `uint8` | 槽95特效号；字段策略 Editable |
| `槽96特效号` | `0x180` | 1 | `uint8` | 槽96特效号；字段策略 Editable |
| `槽97特效号` | `0x184` | 1 | `uint8` | 槽97特效号；字段策略 Editable |
| `槽98特效号` | `0x188` | 1 | `uint8` | 槽98特效号；字段策略 Editable |
| `槽99特效号` | `0x18C` | 1 | `uint8` | 槽99特效号；字段策略 Editable |
| `槽100特效号` | `0x190` | 1 | `uint8` | 槽100特效号；字段策略 Editable |
| `槽101特效号` | `0x194` | 1 | `uint8` | 槽101特效号；字段策略 Editable |
| `槽102特效号` | `0x198` | 1 | `uint8` | 槽102特效号；字段策略 Editable |
| `槽103特效号` | `0x19C` | 1 | `uint8` | 槽103特效号；字段策略 Editable |
| `槽104特效号` | `0x1A0` | 1 | `uint8` | 槽104特效号；字段策略 Editable |
| `槽105特效号` | `0x1A4` | 1 | `uint8` | 槽105特效号；字段策略 Editable |
| `槽106特效号` | `0x1A8` | 1 | `uint8` | 槽106特效号；字段策略 Editable |
| `槽107特效号` | `0x1AC` | 1 | `uint8` | 槽107特效号；字段策略 Editable |
| `槽108特效号` | `0x1B0` | 1 | `uint8` | 槽108特效号；字段策略 Editable |
| `槽109特效号` | `0x1B4` | 1 | `uint8` | 槽109特效号；字段策略 Editable |
| `槽110特效号` | `0x1B8` | 1 | `uint8` | 槽110特效号；字段策略 Editable |
| `槽111特效号` | `0x1BC` | 1 | `uint8` | 槽111特效号；字段策略 Editable |
| `槽112特效号` | `0x1C0` | 1 | `uint8` | 槽112特效号；字段策略 Editable |
| `槽113特效号` | `0x1C4` | 1 | `uint8` | 槽113特效号；字段策略 Editable |
| `槽114特效号` | `0x1C8` | 1 | `uint8` | 槽114特效号；字段策略 Editable |
| `槽115特效号` | `0x1CC` | 1 | `uint8` | 槽115特效号；字段策略 Editable |
| `槽116特效号` | `0x1D0` | 1 | `uint8` | 槽116特效号；字段策略 Editable |
| `槽117特效号` | `0x1D4` | 1 | `uint8` | 槽117特效号；字段策略 Editable |
| `槽118特效号` | `0x1D8` | 1 | `uint8` | 槽118特效号；字段策略 Editable |
| `槽119特效号` | `0x1DC` | 1 | `uint8` | 槽119特效号；字段策略 Editable |
| `槽120特效号` | `0x1E0` | 1 | `uint8` | 槽120特效号；字段策略 Editable |
| `槽121特效号` | `0x1E4` | 1 | `uint8` | 槽121特效号；字段策略 Editable |
| `槽122特效号` | `0x1E8` | 1 | `uint8` | 槽122特效号；字段策略 Editable |
| `槽123特效号` | `0x1EC` | 1 | `uint8` | 槽123特效号；字段策略 Editable |
| `槽124特效号` | `0x1F0` | 1 | `uint8` | 槽124特效号；字段策略 Editable |
| `槽125特效号` | `0x1F4` | 1 | `uint8` | 槽125特效号；字段策略 Editable |
| `槽126特效号` | `0x1F8` | 1 | `uint8` | 槽126特效号；字段策略 Editable |
| `槽127特效号` | `0x1FC` | 1 | `uint8` | 槽127特效号；字段策略 Editable |
| `槽128特效号` | `0x200` | 1 | `uint8` | 槽128特效号；字段策略 Editable |
| `槽129特效号` | `0x204` | 1 | `uint8` | 槽129特效号；字段策略 Editable |
| `槽130特效号` | `0x208` | 1 | `uint8` | 槽130特效号；字段策略 Editable |
| `槽131特效号` | `0x20C` | 1 | `uint8` | 槽131特效号；字段策略 Editable |
| `槽132特效号` | `0x210` | 1 | `uint8` | 槽132特效号；字段策略 Editable |
| `槽133特效号` | `0x214` | 1 | `uint8` | 槽133特效号；字段策略 Editable |
| `槽134特效号` | `0x218` | 1 | `uint8` | 槽134特效号；字段策略 Editable |
| `槽135特效号` | `0x21C` | 1 | `uint8` | 槽135特效号；字段策略 Editable |
| `槽136特效号` | `0x220` | 1 | `uint8` | 槽136特效号；字段策略 Editable |
| `槽137特效号` | `0x224` | 1 | `uint8` | 槽137特效号；字段策略 Editable |
| `槽138特效号` | `0x228` | 1 | `uint8` | 槽138特效号；字段策略 Editable |
| `槽139特效号` | `0x22C` | 1 | `uint8` | 槽139特效号；字段策略 Editable |
| `槽140特效号` | `0x230` | 1 | `uint8` | 槽140特效号；字段策略 Editable |
| `槽141特效号` | `0x234` | 1 | `uint8` | 槽141特效号；字段策略 Editable |
| `槽142特效号` | `0x238` | 1 | `uint8` | 槽142特效号；字段策略 Editable |
| `槽143特效号` | `0x23C` | 1 | `uint8` | 槽143特效号；字段策略 Editable |
| `槽144特效号` | `0x240` | 1 | `uint8` | 槽144特效号；字段策略 Editable |
| `槽145特效号` | `0x244` | 1 | `uint8` | 槽145特效号；字段策略 Editable |
| `槽146特效号` | `0x248` | 1 | `uint8` | 槽146特效号；字段策略 Editable |
| `槽147特效号` | `0x24C` | 1 | `uint8` | 槽147特效号；字段策略 Editable |
| `槽148特效号` | `0x250` | 1 | `uint8` | 槽148特效号；字段策略 Editable |
| `槽149特效号` | `0x254` | 1 | `uint8` | 槽149特效号；字段策略 Editable |
| `槽150特效号` | `0x258` | 1 | `uint8` | 槽150特效号；字段策略 Editable |
| `槽151特效号` | `0x25C` | 1 | `uint8` | 槽151特效号；字段策略 Editable |
| `槽152特效号` | `0x260` | 1 | `uint8` | 槽152特效号；字段策略 Editable |
| `槽153特效号` | `0x264` | 1 | `uint8` | 槽153特效号；字段策略 Editable |
| `槽154特效号` | `0x268` | 1 | `uint8` | 槽154特效号；字段策略 Editable |
| `槽155特效号` | `0x26C` | 1 | `uint8` | 槽155特效号；字段策略 Editable |
| `槽156特效号` | `0x270` | 1 | `uint8` | 槽156特效号；字段策略 Editable |
| `槽157特效号` | `0x274` | 1 | `uint8` | 槽157特效号；字段策略 Editable |
| `槽158特效号` | `0x278` | 1 | `uint8` | 槽158特效号；字段策略 Editable |
| `槽159特效号` | `0x27C` | 1 | `uint8` | 槽159特效号；字段策略 Editable |
| `槽160特效号` | `0x280` | 1 | `uint8` | 槽160特效号；字段策略 Editable |
| `槽161特效号` | `0x284` | 1 | `uint8` | 槽161特效号；字段策略 Editable |
| `槽162特效号` | `0x288` | 1 | `uint8` | 槽162特效号；字段策略 Editable |
| `槽163特效号` | `0x28C` | 1 | `uint8` | 槽163特效号；字段策略 Editable |
| `槽164特效号` | `0x290` | 1 | `uint8` | 槽164特效号；字段策略 Editable |
| `槽165特效号` | `0x294` | 1 | `uint8` | 槽165特效号；字段策略 Editable |
| `槽166特效号` | `0x298` | 1 | `uint8` | 槽166特效号；字段策略 Editable |
| `槽167特效号` | `0x29C` | 1 | `uint8` | 槽167特效号；字段策略 Editable |
| `槽168特效号` | `0x2A0` | 1 | `uint8` | 槽168特效号；字段策略 Editable |
| `槽169特效号` | `0x2A4` | 1 | `uint8` | 槽169特效号；字段策略 Editable |
| `槽170特效号` | `0x2A8` | 1 | `uint8` | 槽170特效号；字段策略 Editable |
| `槽171特效号` | `0x2AC` | 1 | `uint8` | 槽171特效号；字段策略 Editable |
| `槽172特效号` | `0x2B0` | 1 | `uint8` | 槽172特效号；字段策略 Editable |
| `槽173特效号` | `0x2B4` | 1 | `uint8` | 槽173特效号；字段策略 Editable |
| `槽174特效号` | `0x2B8` | 1 | `uint8` | 槽174特效号；字段策略 Editable |
| `槽175特效号` | `0x2BC` | 1 | `uint8` | 槽175特效号；字段策略 Editable |
| `槽176特效号` | `0x2C0` | 1 | `uint8` | 槽176特效号；字段策略 Editable |
| `槽177特效号` | `0x2C4` | 1 | `uint8` | 槽177特效号；字段策略 Editable |
| `槽178特效号` | `0x2C8` | 1 | `uint8` | 槽178特效号；字段策略 Editable |
| `槽179特效号` | `0x2CC` | 1 | `uint8` | 槽179特效号；字段策略 Editable |
| `槽180特效号` | `0x2D0` | 1 | `uint8` | 槽180特效号；字段策略 Editable |
| `槽181特效号` | `0x2D4` | 1 | `uint8` | 槽181特效号；字段策略 Editable |
| `槽182特效号` | `0x2D8` | 1 | `uint8` | 槽182特效号；字段策略 Editable |
| `槽183特效号` | `0x2DC` | 1 | `uint8` | 槽183特效号；字段策略 Editable |
| `槽184特效号` | `0x2E0` | 1 | `uint8` | 槽184特效号；字段策略 Editable |
| `槽185特效号` | `0x2E4` | 1 | `uint8` | 槽185特效号；字段策略 Editable |
| `槽186特效号` | `0x2E8` | 1 | `uint8` | 槽186特效号；字段策略 Editable |
| `槽187特效号` | `0x2EC` | 1 | `uint8` | 槽187特效号；字段策略 Editable |
| `槽188特效号` | `0x2F0` | 1 | `uint8` | 槽188特效号；字段策略 Editable |
| `槽189特效号` | `0x2F4` | 1 | `uint8` | 槽189特效号；字段策略 Editable |
| `槽190特效号` | `0x2F8` | 1 | `uint8` | 槽190特效号；字段策略 Editable |
| `槽191特效号` | `0x2FC` | 1 | `uint8` | 槽191特效号；字段策略 Editable |
| `槽192特效号` | `0x300` | 1 | `uint8` | 槽192特效号；字段策略 Editable |
| `槽193特效号` | `0x304` | 1 | `uint8` | 槽193特效号；字段策略 Editable |
| `槽194特效号` | `0x308` | 1 | `uint8` | 槽194特效号；字段策略 Editable |
| `槽195特效号` | `0x30C` | 1 | `uint8` | 槽195特效号；字段策略 Editable |
| `槽196特效号` | `0x310` | 1 | `uint8` | 槽196特效号；字段策略 Editable |
| `槽197特效号` | `0x314` | 1 | `uint8` | 槽197特效号；字段策略 Editable |
| `槽198特效号` | `0x318` | 1 | `uint8` | 槽198特效号；字段策略 Editable |
| `槽199特效号` | `0x31C` | 1 | `uint8` | 槽199特效号；字段策略 Editable |
| `槽200特效号` | `0x320` | 1 | `uint8` | 槽200特效号；字段策略 Editable |
| `槽201特效号` | `0x324` | 1 | `uint8` | 槽201特效号；字段策略 Editable |
| `槽202特效号` | `0x328` | 1 | `uint8` | 槽202特效号；字段策略 Editable |
| `槽203特效号` | `0x32C` | 1 | `uint8` | 槽203特效号；字段策略 Editable |
| `槽204特效号` | `0x330` | 1 | `uint8` | 槽204特效号；字段策略 Editable |
| `槽205特效号` | `0x334` | 1 | `uint8` | 槽205特效号；字段策略 Editable |
| `槽206特效号` | `0x338` | 1 | `uint8` | 槽206特效号；字段策略 Editable |
| `槽207特效号` | `0x33C` | 1 | `uint8` | 槽207特效号；字段策略 Editable |
| `槽208特效号` | `0x340` | 1 | `uint8` | 槽208特效号；字段策略 Editable |
| `槽209特效号` | `0x344` | 1 | `uint8` | 槽209特效号；字段策略 Editable |
| `槽210特效号` | `0x348` | 1 | `uint8` | 槽210特效号；字段策略 Editable |
| `槽211特效号` | `0x34C` | 1 | `uint8` | 槽211特效号；字段策略 Editable |
| `槽212特效号` | `0x350` | 1 | `uint8` | 槽212特效号；字段策略 Editable |
| `槽213特效号` | `0x354` | 1 | `uint8` | 槽213特效号；字段策略 Editable |
| `槽214特效号` | `0x358` | 1 | `uint8` | 槽214特效号；字段策略 Editable |
| `槽215特效号` | `0x35C` | 1 | `uint8` | 槽215特效号；字段策略 Editable |
| `槽216特效号` | `0x360` | 1 | `uint8` | 槽216特效号；字段策略 Editable |
| `槽217特效号` | `0x364` | 1 | `uint8` | 槽217特效号；字段策略 Editable |
| `槽218特效号` | `0x368` | 1 | `uint8` | 槽218特效号；字段策略 Editable |
| `槽219特效号` | `0x36C` | 1 | `uint8` | 槽219特效号；字段策略 Editable |
| `槽220特效号` | `0x370` | 1 | `uint8` | 槽220特效号；字段策略 Editable |
| `槽221特效号` | `0x374` | 1 | `uint8` | 槽221特效号；字段策略 Editable |
| `槽222特效号` | `0x378` | 1 | `uint8` | 槽222特效号；字段策略 Editable |
| `槽223特效号` | `0x37C` | 1 | `uint8` | 槽223特效号；字段策略 Editable |
| `槽224特效号` | `0x380` | 1 | `uint8` | 槽224特效号；字段策略 Editable |
| `槽225特效号` | `0x384` | 1 | `uint8` | 槽225特效号；字段策略 Editable |
| `槽226特效号` | `0x388` | 1 | `uint8` | 槽226特效号；字段策略 Editable |
| `槽227特效号` | `0x38C` | 1 | `uint8` | 槽227特效号；字段策略 Editable |
| `槽228特效号` | `0x390` | 1 | `uint8` | 槽228特效号；字段策略 Editable |
| `槽229特效号` | `0x394` | 1 | `uint8` | 槽229特效号；字段策略 Editable |
| `槽230特效号` | `0x398` | 1 | `uint8` | 槽230特效号；字段策略 Editable |
| `槽231特效号` | `0x39C` | 1 | `uint8` | 槽231特效号；字段策略 Editable |
| `槽232特效号` | `0x3A0` | 1 | `uint8` | 槽232特效号；字段策略 Editable |
| `槽233特效号` | `0x3A4` | 1 | `uint8` | 槽233特效号；字段策略 Editable |
| `槽234特效号` | `0x3A8` | 1 | `uint8` | 槽234特效号；字段策略 Editable |
| `槽235特效号` | `0x3AC` | 1 | `uint8` | 槽235特效号；字段策略 Editable |
| `槽236特效号` | `0x3B0` | 1 | `uint8` | 槽236特效号；字段策略 Editable |
| `槽237特效号` | `0x3B4` | 1 | `uint8` | 槽237特效号；字段策略 Editable |
| `槽238特效号` | `0x3B8` | 1 | `uint8` | 槽238特效号；字段策略 Editable |
| `槽239特效号` | `0x3BC` | 1 | `uint8` | 槽239特效号；字段策略 Editable |
| `槽240特效号` | `0x3C0` | 1 | `uint8` | 槽240特效号；字段策略 Editable |
| `槽241特效号` | `0x3C4` | 1 | `uint8` | 槽241特效号；字段策略 Editable |
| `槽242特效号` | `0x3C8` | 1 | `uint8` | 槽242特效号；字段策略 Editable |
| `槽243特效号` | `0x3CC` | 1 | `uint8` | 槽243特效号；字段策略 Editable |
| `槽244特效号` | `0x3D0` | 1 | `uint8` | 槽244特效号；字段策略 Editable |
| `槽245特效号` | `0x3D4` | 1 | `uint8` | 槽245特效号；字段策略 Editable |
| `槽246特效号` | `0x3D8` | 1 | `uint8` | 槽246特效号；字段策略 Editable |
| `槽247特效号` | `0x3DC` | 1 | `uint8` | 槽247特效号；字段策略 Editable |
| `槽248特效号` | `0x3E0` | 1 | `uint8` | 槽248特效号；字段策略 Editable |
| `槽249特效号` | `0x3E4` | 1 | `uint8` | 槽249特效号；字段策略 Editable |
| `槽250特效号` | `0x3E8` | 1 | `uint8` | 槽250特效号；字段策略 Editable |
| `槽251特效号` | `0x3EC` | 1 | `uint8` | 槽251特效号；字段策略 Editable |
| `槽252特效号` | `0x3F0` | 1 | `uint8` | 槽252特效号；字段策略 Editable |
| `槽253特效号` | `0x3F4` | 1 | `uint8` | 槽253特效号；字段策略 Editable |
| `槽254特效号` | `0x3F8` | 1 | `uint8` | 槽254特效号；字段策略 Editable |
| `槽255特效号` | `0x3FC` | 1 | `uint8` | 槽255特效号；字段策略 Editable |
| `槽0特效值` | `0x1` | 1 | `uint8` | 槽0特效值；字段策略 Editable |
| `槽1特效值` | `0x5` | 1 | `uint8` | 槽1特效值；字段策略 Editable |
| `槽2特效值` | `0x9` | 1 | `uint8` | 槽2特效值；字段策略 Editable |
| `槽3特效值` | `0xD` | 1 | `uint8` | 槽3特效值；字段策略 Editable |
| `槽4特效值` | `0x11` | 1 | `uint8` | 槽4特效值；字段策略 Editable |
| `槽5特效值` | `0x15` | 1 | `uint8` | 槽5特效值；字段策略 Editable |
| `槽6特效值` | `0x19` | 1 | `uint8` | 槽6特效值；字段策略 Editable |
| `槽7特效值` | `0x1D` | 1 | `uint8` | 槽7特效值；字段策略 Editable |
| `槽8特效值` | `0x21` | 1 | `uint8` | 槽8特效值；字段策略 Editable |
| `槽9特效值` | `0x25` | 1 | `uint8` | 槽9特效值；字段策略 Editable |
| `槽10特效值` | `0x29` | 1 | `uint8` | 槽10特效值；字段策略 Editable |
| `槽11特效值` | `0x2D` | 1 | `uint8` | 槽11特效值；字段策略 Editable |
| `槽12特效值` | `0x31` | 1 | `uint8` | 槽12特效值；字段策略 Editable |
| `槽13特效值` | `0x35` | 1 | `uint8` | 槽13特效值；字段策略 Editable |
| `槽14特效值` | `0x39` | 1 | `uint8` | 槽14特效值；字段策略 Editable |
| `槽15特效值` | `0x3D` | 1 | `uint8` | 槽15特效值；字段策略 Editable |
| `槽16特效值` | `0x41` | 1 | `uint8` | 槽16特效值；字段策略 Editable |
| `槽17特效值` | `0x45` | 1 | `uint8` | 槽17特效值；字段策略 Editable |
| `槽18特效值` | `0x49` | 1 | `uint8` | 槽18特效值；字段策略 Editable |
| `槽19特效值` | `0x4D` | 1 | `uint8` | 槽19特效值；字段策略 Editable |
| `槽20特效值` | `0x51` | 1 | `uint8` | 槽20特效值；字段策略 Editable |
| `槽21特效值` | `0x55` | 1 | `uint8` | 槽21特效值；字段策略 Editable |
| `槽22特效值` | `0x59` | 1 | `uint8` | 槽22特效值；字段策略 Editable |
| `槽23特效值` | `0x5D` | 1 | `uint8` | 槽23特效值；字段策略 Editable |
| `槽24特效值` | `0x61` | 1 | `uint8` | 槽24特效值；字段策略 Editable |
| `槽25特效值` | `0x65` | 1 | `uint8` | 槽25特效值；字段策略 Editable |
| `槽26特效值` | `0x69` | 1 | `uint8` | 槽26特效值；字段策略 Editable |
| `槽27特效值` | `0x6D` | 1 | `uint8` | 槽27特效值；字段策略 Editable |
| `槽28特效值` | `0x71` | 1 | `uint8` | 槽28特效值；字段策略 Editable |
| `槽29特效值` | `0x75` | 1 | `uint8` | 槽29特效值；字段策略 Editable |
| `槽30特效值` | `0x79` | 1 | `uint8` | 槽30特效值；字段策略 Editable |
| `槽31特效值` | `0x7D` | 1 | `uint8` | 槽31特效值；字段策略 Editable |
| `槽32特效值` | `0x81` | 1 | `uint8` | 槽32特效值；字段策略 Editable |
| `槽33特效值` | `0x85` | 1 | `uint8` | 槽33特效值；字段策略 Editable |
| `槽34特效值` | `0x89` | 1 | `uint8` | 槽34特效值；字段策略 Editable |
| `槽35特效值` | `0x8D` | 1 | `uint8` | 槽35特效值；字段策略 Editable |
| `槽36特效值` | `0x91` | 1 | `uint8` | 槽36特效值；字段策略 Editable |
| `槽37特效值` | `0x95` | 1 | `uint8` | 槽37特效值；字段策略 Editable |
| `槽38特效值` | `0x99` | 1 | `uint8` | 槽38特效值；字段策略 Editable |
| `槽39特效值` | `0x9D` | 1 | `uint8` | 槽39特效值；字段策略 Editable |
| `槽40特效值` | `0xA1` | 1 | `uint8` | 槽40特效值；字段策略 Editable |
| `槽41特效值` | `0xA5` | 1 | `uint8` | 槽41特效值；字段策略 Editable |
| `槽42特效值` | `0xA9` | 1 | `uint8` | 槽42特效值；字段策略 Editable |
| `槽43特效值` | `0xAD` | 1 | `uint8` | 槽43特效值；字段策略 Editable |
| `槽44特效值` | `0xB1` | 1 | `uint8` | 槽44特效值；字段策略 Editable |
| `槽45特效值` | `0xB5` | 1 | `uint8` | 槽45特效值；字段策略 Editable |
| `槽46特效值` | `0xB9` | 1 | `uint8` | 槽46特效值；字段策略 Editable |
| `槽47特效值` | `0xBD` | 1 | `uint8` | 槽47特效值；字段策略 Editable |
| `槽48特效值` | `0xC1` | 1 | `uint8` | 槽48特效值；字段策略 Editable |
| `槽49特效值` | `0xC5` | 1 | `uint8` | 槽49特效值；字段策略 Editable |
| `槽50特效值` | `0xC9` | 1 | `uint8` | 槽50特效值；字段策略 Editable |
| `槽51特效值` | `0xCD` | 1 | `uint8` | 槽51特效值；字段策略 Editable |
| `槽52特效值` | `0xD1` | 1 | `uint8` | 槽52特效值；字段策略 Editable |
| `槽53特效值` | `0xD5` | 1 | `uint8` | 槽53特效值；字段策略 Editable |
| `槽54特效值` | `0xD9` | 1 | `uint8` | 槽54特效值；字段策略 Editable |
| `槽55特效值` | `0xDD` | 1 | `uint8` | 槽55特效值；字段策略 Editable |
| `槽56特效值` | `0xE1` | 1 | `uint8` | 槽56特效值；字段策略 Editable |
| `槽57特效值` | `0xE5` | 1 | `uint8` | 槽57特效值；字段策略 Editable |
| `槽58特效值` | `0xE9` | 1 | `uint8` | 槽58特效值；字段策略 Editable |
| `槽59特效值` | `0xED` | 1 | `uint8` | 槽59特效值；字段策略 Editable |
| `槽60特效值` | `0xF1` | 1 | `uint8` | 槽60特效值；字段策略 Editable |
| `槽61特效值` | `0xF5` | 1 | `uint8` | 槽61特效值；字段策略 Editable |
| `槽62特效值` | `0xF9` | 1 | `uint8` | 槽62特效值；字段策略 Editable |
| `槽63特效值` | `0xFD` | 1 | `uint8` | 槽63特效值；字段策略 Editable |
| `槽64特效值` | `0x101` | 1 | `uint8` | 槽64特效值；字段策略 Editable |
| `槽65特效值` | `0x105` | 1 | `uint8` | 槽65特效值；字段策略 Editable |
| `槽66特效值` | `0x109` | 1 | `uint8` | 槽66特效值；字段策略 Editable |
| `槽67特效值` | `0x10D` | 1 | `uint8` | 槽67特效值；字段策略 Editable |
| `槽68特效值` | `0x111` | 1 | `uint8` | 槽68特效值；字段策略 Editable |
| `槽69特效值` | `0x115` | 1 | `uint8` | 槽69特效值；字段策略 Editable |
| `槽70特效值` | `0x119` | 1 | `uint8` | 槽70特效值；字段策略 Editable |
| `槽71特效值` | `0x11D` | 1 | `uint8` | 槽71特效值；字段策略 Editable |
| `槽72特效值` | `0x121` | 1 | `uint8` | 槽72特效值；字段策略 Editable |
| `槽73特效值` | `0x125` | 1 | `uint8` | 槽73特效值；字段策略 Editable |
| `槽74特效值` | `0x129` | 1 | `uint8` | 槽74特效值；字段策略 Editable |
| `槽75特效值` | `0x12D` | 1 | `uint8` | 槽75特效值；字段策略 Editable |
| `槽76特效值` | `0x131` | 1 | `uint8` | 槽76特效值；字段策略 Editable |
| `槽77特效值` | `0x135` | 1 | `uint8` | 槽77特效值；字段策略 Editable |
| `槽78特效值` | `0x139` | 1 | `uint8` | 槽78特效值；字段策略 Editable |
| `槽79特效值` | `0x13D` | 1 | `uint8` | 槽79特效值；字段策略 Editable |
| `槽80特效值` | `0x141` | 1 | `uint8` | 槽80特效值；字段策略 Editable |
| `槽81特效值` | `0x145` | 1 | `uint8` | 槽81特效值；字段策略 Editable |
| `槽82特效值` | `0x149` | 1 | `uint8` | 槽82特效值；字段策略 Editable |
| `槽83特效值` | `0x14D` | 1 | `uint8` | 槽83特效值；字段策略 Editable |
| `槽84特效值` | `0x151` | 1 | `uint8` | 槽84特效值；字段策略 Editable |
| `槽85特效值` | `0x155` | 1 | `uint8` | 槽85特效值；字段策略 Editable |
| `槽86特效值` | `0x159` | 1 | `uint8` | 槽86特效值；字段策略 Editable |
| `槽87特效值` | `0x15D` | 1 | `uint8` | 槽87特效值；字段策略 Editable |
| `槽88特效值` | `0x161` | 1 | `uint8` | 槽88特效值；字段策略 Editable |
| `槽89特效值` | `0x165` | 1 | `uint8` | 槽89特效值；字段策略 Editable |
| `槽90特效值` | `0x169` | 1 | `uint8` | 槽90特效值；字段策略 Editable |
| `槽91特效值` | `0x16D` | 1 | `uint8` | 槽91特效值；字段策略 Editable |
| `槽92特效值` | `0x171` | 1 | `uint8` | 槽92特效值；字段策略 Editable |
| `槽93特效值` | `0x175` | 1 | `uint8` | 槽93特效值；字段策略 Editable |
| `槽94特效值` | `0x179` | 1 | `uint8` | 槽94特效值；字段策略 Editable |
| `槽95特效值` | `0x17D` | 1 | `uint8` | 槽95特效值；字段策略 Editable |
| `槽96特效值` | `0x181` | 1 | `uint8` | 槽96特效值；字段策略 Editable |
| `槽97特效值` | `0x185` | 1 | `uint8` | 槽97特效值；字段策略 Editable |
| `槽98特效值` | `0x189` | 1 | `uint8` | 槽98特效值；字段策略 Editable |
| `槽99特效值` | `0x18D` | 1 | `uint8` | 槽99特效值；字段策略 Editable |
| `槽100特效值` | `0x191` | 1 | `uint8` | 槽100特效值；字段策略 Editable |
| `槽101特效值` | `0x195` | 1 | `uint8` | 槽101特效值；字段策略 Editable |
| `槽102特效值` | `0x199` | 1 | `uint8` | 槽102特效值；字段策略 Editable |
| `槽103特效值` | `0x19D` | 1 | `uint8` | 槽103特效值；字段策略 Editable |
| `槽104特效值` | `0x1A1` | 1 | `uint8` | 槽104特效值；字段策略 Editable |
| `槽105特效值` | `0x1A5` | 1 | `uint8` | 槽105特效值；字段策略 Editable |
| `槽106特效值` | `0x1A9` | 1 | `uint8` | 槽106特效值；字段策略 Editable |
| `槽107特效值` | `0x1AD` | 1 | `uint8` | 槽107特效值；字段策略 Editable |
| `槽108特效值` | `0x1B1` | 1 | `uint8` | 槽108特效值；字段策略 Editable |
| `槽109特效值` | `0x1B5` | 1 | `uint8` | 槽109特效值；字段策略 Editable |
| `槽110特效值` | `0x1B9` | 1 | `uint8` | 槽110特效值；字段策略 Editable |
| `槽111特效值` | `0x1BD` | 1 | `uint8` | 槽111特效值；字段策略 Editable |
| `槽112特效值` | `0x1C1` | 1 | `uint8` | 槽112特效值；字段策略 Editable |
| `槽113特效值` | `0x1C5` | 1 | `uint8` | 槽113特效值；字段策略 Editable |
| `槽114特效值` | `0x1C9` | 1 | `uint8` | 槽114特效值；字段策略 Editable |
| `槽115特效值` | `0x1CD` | 1 | `uint8` | 槽115特效值；字段策略 Editable |
| `槽116特效值` | `0x1D1` | 1 | `uint8` | 槽116特效值；字段策略 Editable |
| `槽117特效值` | `0x1D5` | 1 | `uint8` | 槽117特效值；字段策略 Editable |
| `槽118特效值` | `0x1D9` | 1 | `uint8` | 槽118特效值；字段策略 Editable |
| `槽119特效值` | `0x1DD` | 1 | `uint8` | 槽119特效值；字段策略 Editable |
| `槽120特效值` | `0x1E1` | 1 | `uint8` | 槽120特效值；字段策略 Editable |
| `槽121特效值` | `0x1E5` | 1 | `uint8` | 槽121特效值；字段策略 Editable |
| `槽122特效值` | `0x1E9` | 1 | `uint8` | 槽122特效值；字段策略 Editable |
| `槽123特效值` | `0x1ED` | 1 | `uint8` | 槽123特效值；字段策略 Editable |
| `槽124特效值` | `0x1F1` | 1 | `uint8` | 槽124特效值；字段策略 Editable |
| `槽125特效值` | `0x1F5` | 1 | `uint8` | 槽125特效值；字段策略 Editable |
| `槽126特效值` | `0x1F9` | 1 | `uint8` | 槽126特效值；字段策略 Editable |
| `槽127特效值` | `0x1FD` | 1 | `uint8` | 槽127特效值；字段策略 Editable |
| `槽128特效值` | `0x201` | 1 | `uint8` | 槽128特效值；字段策略 Editable |
| `槽129特效值` | `0x205` | 1 | `uint8` | 槽129特效值；字段策略 Editable |
| `槽130特效值` | `0x209` | 1 | `uint8` | 槽130特效值；字段策略 Editable |
| `槽131特效值` | `0x20D` | 1 | `uint8` | 槽131特效值；字段策略 Editable |
| `槽132特效值` | `0x211` | 1 | `uint8` | 槽132特效值；字段策略 Editable |
| `槽133特效值` | `0x215` | 1 | `uint8` | 槽133特效值；字段策略 Editable |
| `槽134特效值` | `0x219` | 1 | `uint8` | 槽134特效值；字段策略 Editable |
| `槽135特效值` | `0x21D` | 1 | `uint8` | 槽135特效值；字段策略 Editable |
| `槽136特效值` | `0x221` | 1 | `uint8` | 槽136特效值；字段策略 Editable |
| `槽137特效值` | `0x225` | 1 | `uint8` | 槽137特效值；字段策略 Editable |
| `槽138特效值` | `0x229` | 1 | `uint8` | 槽138特效值；字段策略 Editable |
| `槽139特效值` | `0x22D` | 1 | `uint8` | 槽139特效值；字段策略 Editable |
| `槽140特效值` | `0x231` | 1 | `uint8` | 槽140特效值；字段策略 Editable |
| `槽141特效值` | `0x235` | 1 | `uint8` | 槽141特效值；字段策略 Editable |
| `槽142特效值` | `0x239` | 1 | `uint8` | 槽142特效值；字段策略 Editable |
| `槽143特效值` | `0x23D` | 1 | `uint8` | 槽143特效值；字段策略 Editable |
| `槽144特效值` | `0x241` | 1 | `uint8` | 槽144特效值；字段策略 Editable |
| `槽145特效值` | `0x245` | 1 | `uint8` | 槽145特效值；字段策略 Editable |
| `槽146特效值` | `0x249` | 1 | `uint8` | 槽146特效值；字段策略 Editable |
| `槽147特效值` | `0x24D` | 1 | `uint8` | 槽147特效值；字段策略 Editable |
| `槽148特效值` | `0x251` | 1 | `uint8` | 槽148特效值；字段策略 Editable |
| `槽149特效值` | `0x255` | 1 | `uint8` | 槽149特效值；字段策略 Editable |
| `槽150特效值` | `0x259` | 1 | `uint8` | 槽150特效值；字段策略 Editable |
| `槽151特效值` | `0x25D` | 1 | `uint8` | 槽151特效值；字段策略 Editable |
| `槽152特效值` | `0x261` | 1 | `uint8` | 槽152特效值；字段策略 Editable |
| `槽153特效值` | `0x265` | 1 | `uint8` | 槽153特效值；字段策略 Editable |
| `槽154特效值` | `0x269` | 1 | `uint8` | 槽154特效值；字段策略 Editable |
| `槽155特效值` | `0x26D` | 1 | `uint8` | 槽155特效值；字段策略 Editable |
| `槽156特效值` | `0x271` | 1 | `uint8` | 槽156特效值；字段策略 Editable |
| `槽157特效值` | `0x275` | 1 | `uint8` | 槽157特效值；字段策略 Editable |
| `槽158特效值` | `0x279` | 1 | `uint8` | 槽158特效值；字段策略 Editable |
| `槽159特效值` | `0x27D` | 1 | `uint8` | 槽159特效值；字段策略 Editable |
| `槽160特效值` | `0x281` | 1 | `uint8` | 槽160特效值；字段策略 Editable |
| `槽161特效值` | `0x285` | 1 | `uint8` | 槽161特效值；字段策略 Editable |
| `槽162特效值` | `0x289` | 1 | `uint8` | 槽162特效值；字段策略 Editable |
| `槽163特效值` | `0x28D` | 1 | `uint8` | 槽163特效值；字段策略 Editable |
| `槽164特效值` | `0x291` | 1 | `uint8` | 槽164特效值；字段策略 Editable |
| `槽165特效值` | `0x295` | 1 | `uint8` | 槽165特效值；字段策略 Editable |
| `槽166特效值` | `0x299` | 1 | `uint8` | 槽166特效值；字段策略 Editable |
| `槽167特效值` | `0x29D` | 1 | `uint8` | 槽167特效值；字段策略 Editable |
| `槽168特效值` | `0x2A1` | 1 | `uint8` | 槽168特效值；字段策略 Editable |
| `槽169特效值` | `0x2A5` | 1 | `uint8` | 槽169特效值；字段策略 Editable |
| `槽170特效值` | `0x2A9` | 1 | `uint8` | 槽170特效值；字段策略 Editable |
| `槽171特效值` | `0x2AD` | 1 | `uint8` | 槽171特效值；字段策略 Editable |
| `槽172特效值` | `0x2B1` | 1 | `uint8` | 槽172特效值；字段策略 Editable |
| `槽173特效值` | `0x2B5` | 1 | `uint8` | 槽173特效值；字段策略 Editable |
| `槽174特效值` | `0x2B9` | 1 | `uint8` | 槽174特效值；字段策略 Editable |
| `槽175特效值` | `0x2BD` | 1 | `uint8` | 槽175特效值；字段策略 Editable |
| `槽176特效值` | `0x2C1` | 1 | `uint8` | 槽176特效值；字段策略 Editable |
| `槽177特效值` | `0x2C5` | 1 | `uint8` | 槽177特效值；字段策略 Editable |
| `槽178特效值` | `0x2C9` | 1 | `uint8` | 槽178特效值；字段策略 Editable |
| `槽179特效值` | `0x2CD` | 1 | `uint8` | 槽179特效值；字段策略 Editable |
| `槽180特效值` | `0x2D1` | 1 | `uint8` | 槽180特效值；字段策略 Editable |
| `槽181特效值` | `0x2D5` | 1 | `uint8` | 槽181特效值；字段策略 Editable |
| `槽182特效值` | `0x2D9` | 1 | `uint8` | 槽182特效值；字段策略 Editable |
| `槽183特效值` | `0x2DD` | 1 | `uint8` | 槽183特效值；字段策略 Editable |
| `槽184特效值` | `0x2E1` | 1 | `uint8` | 槽184特效值；字段策略 Editable |
| `槽185特效值` | `0x2E5` | 1 | `uint8` | 槽185特效值；字段策略 Editable |
| `槽186特效值` | `0x2E9` | 1 | `uint8` | 槽186特效值；字段策略 Editable |
| `槽187特效值` | `0x2ED` | 1 | `uint8` | 槽187特效值；字段策略 Editable |
| `槽188特效值` | `0x2F1` | 1 | `uint8` | 槽188特效值；字段策略 Editable |
| `槽189特效值` | `0x2F5` | 1 | `uint8` | 槽189特效值；字段策略 Editable |
| `槽190特效值` | `0x2F9` | 1 | `uint8` | 槽190特效值；字段策略 Editable |
| `槽191特效值` | `0x2FD` | 1 | `uint8` | 槽191特效值；字段策略 Editable |
| `槽192特效值` | `0x301` | 1 | `uint8` | 槽192特效值；字段策略 Editable |
| `槽193特效值` | `0x305` | 1 | `uint8` | 槽193特效值；字段策略 Editable |
| `槽194特效值` | `0x309` | 1 | `uint8` | 槽194特效值；字段策略 Editable |
| `槽195特效值` | `0x30D` | 1 | `uint8` | 槽195特效值；字段策略 Editable |
| `槽196特效值` | `0x311` | 1 | `uint8` | 槽196特效值；字段策略 Editable |
| `槽197特效值` | `0x315` | 1 | `uint8` | 槽197特效值；字段策略 Editable |
| `槽198特效值` | `0x319` | 1 | `uint8` | 槽198特效值；字段策略 Editable |
| `槽199特效值` | `0x31D` | 1 | `uint8` | 槽199特效值；字段策略 Editable |
| `槽200特效值` | `0x321` | 1 | `uint8` | 槽200特效值；字段策略 Editable |
| `槽201特效值` | `0x325` | 1 | `uint8` | 槽201特效值；字段策略 Editable |
| `槽202特效值` | `0x329` | 1 | `uint8` | 槽202特效值；字段策略 Editable |
| `槽203特效值` | `0x32D` | 1 | `uint8` | 槽203特效值；字段策略 Editable |
| `槽204特效值` | `0x331` | 1 | `uint8` | 槽204特效值；字段策略 Editable |
| `槽205特效值` | `0x335` | 1 | `uint8` | 槽205特效值；字段策略 Editable |
| `槽206特效值` | `0x339` | 1 | `uint8` | 槽206特效值；字段策略 Editable |
| `槽207特效值` | `0x33D` | 1 | `uint8` | 槽207特效值；字段策略 Editable |
| `槽208特效值` | `0x341` | 1 | `uint8` | 槽208特效值；字段策略 Editable |
| `槽209特效值` | `0x345` | 1 | `uint8` | 槽209特效值；字段策略 Editable |
| `槽210特效值` | `0x349` | 1 | `uint8` | 槽210特效值；字段策略 Editable |
| `槽211特效值` | `0x34D` | 1 | `uint8` | 槽211特效值；字段策略 Editable |
| `槽212特效值` | `0x351` | 1 | `uint8` | 槽212特效值；字段策略 Editable |
| `槽213特效值` | `0x355` | 1 | `uint8` | 槽213特效值；字段策略 Editable |
| `槽214特效值` | `0x359` | 1 | `uint8` | 槽214特效值；字段策略 Editable |
| `槽215特效值` | `0x35D` | 1 | `uint8` | 槽215特效值；字段策略 Editable |
| `槽216特效值` | `0x361` | 1 | `uint8` | 槽216特效值；字段策略 Editable |
| `槽217特效值` | `0x365` | 1 | `uint8` | 槽217特效值；字段策略 Editable |
| `槽218特效值` | `0x369` | 1 | `uint8` | 槽218特效值；字段策略 Editable |
| `槽219特效值` | `0x36D` | 1 | `uint8` | 槽219特效值；字段策略 Editable |
| `槽220特效值` | `0x371` | 1 | `uint8` | 槽220特效值；字段策略 Editable |
| `槽221特效值` | `0x375` | 1 | `uint8` | 槽221特效值；字段策略 Editable |
| `槽222特效值` | `0x379` | 1 | `uint8` | 槽222特效值；字段策略 Editable |
| `槽223特效值` | `0x37D` | 1 | `uint8` | 槽223特效值；字段策略 Editable |
| `槽224特效值` | `0x381` | 1 | `uint8` | 槽224特效值；字段策略 Editable |
| `槽225特效值` | `0x385` | 1 | `uint8` | 槽225特效值；字段策略 Editable |
| `槽226特效值` | `0x389` | 1 | `uint8` | 槽226特效值；字段策略 Editable |
| `槽227特效值` | `0x38D` | 1 | `uint8` | 槽227特效值；字段策略 Editable |
| `槽228特效值` | `0x391` | 1 | `uint8` | 槽228特效值；字段策略 Editable |
| `槽229特效值` | `0x395` | 1 | `uint8` | 槽229特效值；字段策略 Editable |
| `槽230特效值` | `0x399` | 1 | `uint8` | 槽230特效值；字段策略 Editable |
| `槽231特效值` | `0x39D` | 1 | `uint8` | 槽231特效值；字段策略 Editable |
| `槽232特效值` | `0x3A1` | 1 | `uint8` | 槽232特效值；字段策略 Editable |
| `槽233特效值` | `0x3A5` | 1 | `uint8` | 槽233特效值；字段策略 Editable |
| `槽234特效值` | `0x3A9` | 1 | `uint8` | 槽234特效值；字段策略 Editable |
| `槽235特效值` | `0x3AD` | 1 | `uint8` | 槽235特效值；字段策略 Editable |
| `槽236特效值` | `0x3B1` | 1 | `uint8` | 槽236特效值；字段策略 Editable |
| `槽237特效值` | `0x3B5` | 1 | `uint8` | 槽237特效值；字段策略 Editable |
| `槽238特效值` | `0x3B9` | 1 | `uint8` | 槽238特效值；字段策略 Editable |
| `槽239特效值` | `0x3BD` | 1 | `uint8` | 槽239特效值；字段策略 Editable |
| `槽240特效值` | `0x3C1` | 1 | `uint8` | 槽240特效值；字段策略 Editable |
| `槽241特效值` | `0x3C5` | 1 | `uint8` | 槽241特效值；字段策略 Editable |
| `槽242特效值` | `0x3C9` | 1 | `uint8` | 槽242特效值；字段策略 Editable |
| `槽243特效值` | `0x3CD` | 1 | `uint8` | 槽243特效值；字段策略 Editable |
| `槽244特效值` | `0x3D1` | 1 | `uint8` | 槽244特效值；字段策略 Editable |
| `槽245特效值` | `0x3D5` | 1 | `uint8` | 槽245特效值；字段策略 Editable |
| `槽246特效值` | `0x3D9` | 1 | `uint8` | 槽246特效值；字段策略 Editable |
| `槽247特效值` | `0x3DD` | 1 | `uint8` | 槽247特效值；字段策略 Editable |
| `槽248特效值` | `0x3E1` | 1 | `uint8` | 槽248特效值；字段策略 Editable |
| `槽249特效值` | `0x3E5` | 1 | `uint8` | 槽249特效值；字段策略 Editable |
| `槽250特效值` | `0x3E9` | 1 | `uint8` | 槽250特效值；字段策略 Editable |
| `槽251特效值` | `0x3ED` | 1 | `uint8` | 槽251特效值；字段策略 Editable |
| `槽252特效值` | `0x3F1` | 1 | `uint8` | 槽252特效值；字段策略 Editable |
| `槽253特效值` | `0x3F5` | 1 | `uint8` | 槽253特效值；字段策略 Editable |
| `槽254特效值` | `0x3F9` | 1 | `uint8` | 槽254特效值；字段策略 Editable |
| `槽255特效值` | `0x3FD` | 1 | `uint8` | 槽255特效值；字段策略 Editable |
| `槽0经验` | `0x2` | 1 | `uint8` | 槽0经验；字段策略 Editable |
| `槽1经验` | `0x6` | 1 | `uint8` | 槽1经验；字段策略 Editable |
| `槽2经验` | `0xA` | 1 | `uint8` | 槽2经验；字段策略 Editable |
| `槽3经验` | `0xE` | 1 | `uint8` | 槽3经验；字段策略 Editable |
| `槽4经验` | `0x12` | 1 | `uint8` | 槽4经验；字段策略 Editable |
| `槽5经验` | `0x16` | 1 | `uint8` | 槽5经验；字段策略 Editable |
| `槽6经验` | `0x1A` | 1 | `uint8` | 槽6经验；字段策略 Editable |
| `槽7经验` | `0x1E` | 1 | `uint8` | 槽7经验；字段策略 Editable |
| `槽8经验` | `0x22` | 1 | `uint8` | 槽8经验；字段策略 Editable |
| `槽9经验` | `0x26` | 1 | `uint8` | 槽9经验；字段策略 Editable |
| `槽10经验` | `0x2A` | 1 | `uint8` | 槽10经验；字段策略 Editable |
| `槽11经验` | `0x2E` | 1 | `uint8` | 槽11经验；字段策略 Editable |
| `槽12经验` | `0x32` | 1 | `uint8` | 槽12经验；字段策略 Editable |
| `槽13经验` | `0x36` | 1 | `uint8` | 槽13经验；字段策略 Editable |
| `槽14经验` | `0x3A` | 1 | `uint8` | 槽14经验；字段策略 Editable |
| `槽15经验` | `0x3E` | 1 | `uint8` | 槽15经验；字段策略 Editable |
| `槽16经验` | `0x42` | 1 | `uint8` | 槽16经验；字段策略 Editable |
| `槽17经验` | `0x46` | 1 | `uint8` | 槽17经验；字段策略 Editable |
| `槽18经验` | `0x4A` | 1 | `uint8` | 槽18经验；字段策略 Editable |
| `槽19经验` | `0x4E` | 1 | `uint8` | 槽19经验；字段策略 Editable |
| `槽20经验` | `0x52` | 1 | `uint8` | 槽20经验；字段策略 Editable |
| `槽21经验` | `0x56` | 1 | `uint8` | 槽21经验；字段策略 Editable |
| `槽22经验` | `0x5A` | 1 | `uint8` | 槽22经验；字段策略 Editable |
| `槽23经验` | `0x5E` | 1 | `uint8` | 槽23经验；字段策略 Editable |
| `槽24经验` | `0x62` | 1 | `uint8` | 槽24经验；字段策略 Editable |
| `槽25经验` | `0x66` | 1 | `uint8` | 槽25经验；字段策略 Editable |
| `槽26经验` | `0x6A` | 1 | `uint8` | 槽26经验；字段策略 Editable |
| `槽27经验` | `0x6E` | 1 | `uint8` | 槽27经验；字段策略 Editable |
| `槽28经验` | `0x72` | 1 | `uint8` | 槽28经验；字段策略 Editable |
| `槽29经验` | `0x76` | 1 | `uint8` | 槽29经验；字段策略 Editable |
| `槽30经验` | `0x7A` | 1 | `uint8` | 槽30经验；字段策略 Editable |
| `槽31经验` | `0x7E` | 1 | `uint8` | 槽31经验；字段策略 Editable |
| `槽32经验` | `0x82` | 1 | `uint8` | 槽32经验；字段策略 Editable |
| `槽33经验` | `0x86` | 1 | `uint8` | 槽33经验；字段策略 Editable |
| `槽34经验` | `0x8A` | 1 | `uint8` | 槽34经验；字段策略 Editable |
| `槽35经验` | `0x8E` | 1 | `uint8` | 槽35经验；字段策略 Editable |
| `槽36经验` | `0x92` | 1 | `uint8` | 槽36经验；字段策略 Editable |
| `槽37经验` | `0x96` | 1 | `uint8` | 槽37经验；字段策略 Editable |
| `槽38经验` | `0x9A` | 1 | `uint8` | 槽38经验；字段策略 Editable |
| `槽39经验` | `0x9E` | 1 | `uint8` | 槽39经验；字段策略 Editable |
| `槽40经验` | `0xA2` | 1 | `uint8` | 槽40经验；字段策略 Editable |
| `槽41经验` | `0xA6` | 1 | `uint8` | 槽41经验；字段策略 Editable |
| `槽42经验` | `0xAA` | 1 | `uint8` | 槽42经验；字段策略 Editable |
| `槽43经验` | `0xAE` | 1 | `uint8` | 槽43经验；字段策略 Editable |
| `槽44经验` | `0xB2` | 1 | `uint8` | 槽44经验；字段策略 Editable |
| `槽45经验` | `0xB6` | 1 | `uint8` | 槽45经验；字段策略 Editable |
| `槽46经验` | `0xBA` | 1 | `uint8` | 槽46经验；字段策略 Editable |
| `槽47经验` | `0xBE` | 1 | `uint8` | 槽47经验；字段策略 Editable |
| `槽48经验` | `0xC2` | 1 | `uint8` | 槽48经验；字段策略 Editable |
| `槽49经验` | `0xC6` | 1 | `uint8` | 槽49经验；字段策略 Editable |
| `槽50经验` | `0xCA` | 1 | `uint8` | 槽50经验；字段策略 Editable |
| `槽51经验` | `0xCE` | 1 | `uint8` | 槽51经验；字段策略 Editable |
| `槽52经验` | `0xD2` | 1 | `uint8` | 槽52经验；字段策略 Editable |
| `槽53经验` | `0xD6` | 1 | `uint8` | 槽53经验；字段策略 Editable |
| `槽54经验` | `0xDA` | 1 | `uint8` | 槽54经验；字段策略 Editable |
| `槽55经验` | `0xDE` | 1 | `uint8` | 槽55经验；字段策略 Editable |
| `槽56经验` | `0xE2` | 1 | `uint8` | 槽56经验；字段策略 Editable |
| `槽57经验` | `0xE6` | 1 | `uint8` | 槽57经验；字段策略 Editable |
| `槽58经验` | `0xEA` | 1 | `uint8` | 槽58经验；字段策略 Editable |
| `槽59经验` | `0xEE` | 1 | `uint8` | 槽59经验；字段策略 Editable |
| `槽60经验` | `0xF2` | 1 | `uint8` | 槽60经验；字段策略 Editable |
| `槽61经验` | `0xF6` | 1 | `uint8` | 槽61经验；字段策略 Editable |
| `槽62经验` | `0xFA` | 1 | `uint8` | 槽62经验；字段策略 Editable |
| `槽63经验` | `0xFE` | 1 | `uint8` | 槽63经验；字段策略 Editable |
| `槽64经验` | `0x102` | 1 | `uint8` | 槽64经验；字段策略 Editable |
| `槽65经验` | `0x106` | 1 | `uint8` | 槽65经验；字段策略 Editable |
| `槽66经验` | `0x10A` | 1 | `uint8` | 槽66经验；字段策略 Editable |
| `槽67经验` | `0x10E` | 1 | `uint8` | 槽67经验；字段策略 Editable |
| `槽68经验` | `0x112` | 1 | `uint8` | 槽68经验；字段策略 Editable |
| `槽69经验` | `0x116` | 1 | `uint8` | 槽69经验；字段策略 Editable |
| `槽70经验` | `0x11A` | 1 | `uint8` | 槽70经验；字段策略 Editable |
| `槽71经验` | `0x11E` | 1 | `uint8` | 槽71经验；字段策略 Editable |
| `槽72经验` | `0x122` | 1 | `uint8` | 槽72经验；字段策略 Editable |
| `槽73经验` | `0x126` | 1 | `uint8` | 槽73经验；字段策略 Editable |
| `槽74经验` | `0x12A` | 1 | `uint8` | 槽74经验；字段策略 Editable |
| `槽75经验` | `0x12E` | 1 | `uint8` | 槽75经验；字段策略 Editable |
| `槽76经验` | `0x132` | 1 | `uint8` | 槽76经验；字段策略 Editable |
| `槽77经验` | `0x136` | 1 | `uint8` | 槽77经验；字段策略 Editable |
| `槽78经验` | `0x13A` | 1 | `uint8` | 槽78经验；字段策略 Editable |
| `槽79经验` | `0x13E` | 1 | `uint8` | 槽79经验；字段策略 Editable |
| `槽80经验` | `0x142` | 1 | `uint8` | 槽80经验；字段策略 Editable |
| `槽81经验` | `0x146` | 1 | `uint8` | 槽81经验；字段策略 Editable |
| `槽82经验` | `0x14A` | 1 | `uint8` | 槽82经验；字段策略 Editable |
| `槽83经验` | `0x14E` | 1 | `uint8` | 槽83经验；字段策略 Editable |
| `槽84经验` | `0x152` | 1 | `uint8` | 槽84经验；字段策略 Editable |
| `槽85经验` | `0x156` | 1 | `uint8` | 槽85经验；字段策略 Editable |
| `槽86经验` | `0x15A` | 1 | `uint8` | 槽86经验；字段策略 Editable |
| `槽87经验` | `0x15E` | 1 | `uint8` | 槽87经验；字段策略 Editable |
| `槽88经验` | `0x162` | 1 | `uint8` | 槽88经验；字段策略 Editable |
| `槽89经验` | `0x166` | 1 | `uint8` | 槽89经验；字段策略 Editable |
| `槽90经验` | `0x16A` | 1 | `uint8` | 槽90经验；字段策略 Editable |
| `槽91经验` | `0x16E` | 1 | `uint8` | 槽91经验；字段策略 Editable |
| `槽92经验` | `0x172` | 1 | `uint8` | 槽92经验；字段策略 Editable |
| `槽93经验` | `0x176` | 1 | `uint8` | 槽93经验；字段策略 Editable |
| `槽94经验` | `0x17A` | 1 | `uint8` | 槽94经验；字段策略 Editable |
| `槽95经验` | `0x17E` | 1 | `uint8` | 槽95经验；字段策略 Editable |
| `槽96经验` | `0x182` | 1 | `uint8` | 槽96经验；字段策略 Editable |
| `槽97经验` | `0x186` | 1 | `uint8` | 槽97经验；字段策略 Editable |
| `槽98经验` | `0x18A` | 1 | `uint8` | 槽98经验；字段策略 Editable |
| `槽99经验` | `0x18E` | 1 | `uint8` | 槽99经验；字段策略 Editable |
| `槽100经验` | `0x192` | 1 | `uint8` | 槽100经验；字段策略 Editable |
| `槽101经验` | `0x196` | 1 | `uint8` | 槽101经验；字段策略 Editable |
| `槽102经验` | `0x19A` | 1 | `uint8` | 槽102经验；字段策略 Editable |
| `槽103经验` | `0x19E` | 1 | `uint8` | 槽103经验；字段策略 Editable |
| `槽104经验` | `0x1A2` | 1 | `uint8` | 槽104经验；字段策略 Editable |
| `槽105经验` | `0x1A6` | 1 | `uint8` | 槽105经验；字段策略 Editable |
| `槽106经验` | `0x1AA` | 1 | `uint8` | 槽106经验；字段策略 Editable |
| `槽107经验` | `0x1AE` | 1 | `uint8` | 槽107经验；字段策略 Editable |
| `槽108经验` | `0x1B2` | 1 | `uint8` | 槽108经验；字段策略 Editable |
| `槽109经验` | `0x1B6` | 1 | `uint8` | 槽109经验；字段策略 Editable |
| `槽110经验` | `0x1BA` | 1 | `uint8` | 槽110经验；字段策略 Editable |
| `槽111经验` | `0x1BE` | 1 | `uint8` | 槽111经验；字段策略 Editable |
| `槽112经验` | `0x1C2` | 1 | `uint8` | 槽112经验；字段策略 Editable |
| `槽113经验` | `0x1C6` | 1 | `uint8` | 槽113经验；字段策略 Editable |
| `槽114经验` | `0x1CA` | 1 | `uint8` | 槽114经验；字段策略 Editable |
| `槽115经验` | `0x1CE` | 1 | `uint8` | 槽115经验；字段策略 Editable |
| `槽116经验` | `0x1D2` | 1 | `uint8` | 槽116经验；字段策略 Editable |
| `槽117经验` | `0x1D6` | 1 | `uint8` | 槽117经验；字段策略 Editable |
| `槽118经验` | `0x1DA` | 1 | `uint8` | 槽118经验；字段策略 Editable |
| `槽119经验` | `0x1DE` | 1 | `uint8` | 槽119经验；字段策略 Editable |
| `槽120经验` | `0x1E2` | 1 | `uint8` | 槽120经验；字段策略 Editable |
| `槽121经验` | `0x1E6` | 1 | `uint8` | 槽121经验；字段策略 Editable |
| `槽122经验` | `0x1EA` | 1 | `uint8` | 槽122经验；字段策略 Editable |
| `槽123经验` | `0x1EE` | 1 | `uint8` | 槽123经验；字段策略 Editable |
| `槽124经验` | `0x1F2` | 1 | `uint8` | 槽124经验；字段策略 Editable |
| `槽125经验` | `0x1F6` | 1 | `uint8` | 槽125经验；字段策略 Editable |
| `槽126经验` | `0x1FA` | 1 | `uint8` | 槽126经验；字段策略 Editable |
| `槽127经验` | `0x1FE` | 1 | `uint8` | 槽127经验；字段策略 Editable |
| `槽128经验` | `0x202` | 1 | `uint8` | 槽128经验；字段策略 Editable |
| `槽129经验` | `0x206` | 1 | `uint8` | 槽129经验；字段策略 Editable |
| `槽130经验` | `0x20A` | 1 | `uint8` | 槽130经验；字段策略 Editable |
| `槽131经验` | `0x20E` | 1 | `uint8` | 槽131经验；字段策略 Editable |
| `槽132经验` | `0x212` | 1 | `uint8` | 槽132经验；字段策略 Editable |
| `槽133经验` | `0x216` | 1 | `uint8` | 槽133经验；字段策略 Editable |
| `槽134经验` | `0x21A` | 1 | `uint8` | 槽134经验；字段策略 Editable |
| `槽135经验` | `0x21E` | 1 | `uint8` | 槽135经验；字段策略 Editable |
| `槽136经验` | `0x222` | 1 | `uint8` | 槽136经验；字段策略 Editable |
| `槽137经验` | `0x226` | 1 | `uint8` | 槽137经验；字段策略 Editable |
| `槽138经验` | `0x22A` | 1 | `uint8` | 槽138经验；字段策略 Editable |
| `槽139经验` | `0x22E` | 1 | `uint8` | 槽139经验；字段策略 Editable |
| `槽140经验` | `0x232` | 1 | `uint8` | 槽140经验；字段策略 Editable |
| `槽141经验` | `0x236` | 1 | `uint8` | 槽141经验；字段策略 Editable |
| `槽142经验` | `0x23A` | 1 | `uint8` | 槽142经验；字段策略 Editable |
| `槽143经验` | `0x23E` | 1 | `uint8` | 槽143经验；字段策略 Editable |
| `槽144经验` | `0x242` | 1 | `uint8` | 槽144经验；字段策略 Editable |
| `槽145经验` | `0x246` | 1 | `uint8` | 槽145经验；字段策略 Editable |
| `槽146经验` | `0x24A` | 1 | `uint8` | 槽146经验；字段策略 Editable |
| `槽147经验` | `0x24E` | 1 | `uint8` | 槽147经验；字段策略 Editable |
| `槽148经验` | `0x252` | 1 | `uint8` | 槽148经验；字段策略 Editable |
| `槽149经验` | `0x256` | 1 | `uint8` | 槽149经验；字段策略 Editable |
| `槽150经验` | `0x25A` | 1 | `uint8` | 槽150经验；字段策略 Editable |
| `槽151经验` | `0x25E` | 1 | `uint8` | 槽151经验；字段策略 Editable |
| `槽152经验` | `0x262` | 1 | `uint8` | 槽152经验；字段策略 Editable |
| `槽153经验` | `0x266` | 1 | `uint8` | 槽153经验；字段策略 Editable |
| `槽154经验` | `0x26A` | 1 | `uint8` | 槽154经验；字段策略 Editable |
| `槽155经验` | `0x26E` | 1 | `uint8` | 槽155经验；字段策略 Editable |
| `槽156经验` | `0x272` | 1 | `uint8` | 槽156经验；字段策略 Editable |
| `槽157经验` | `0x276` | 1 | `uint8` | 槽157经验；字段策略 Editable |
| `槽158经验` | `0x27A` | 1 | `uint8` | 槽158经验；字段策略 Editable |
| `槽159经验` | `0x27E` | 1 | `uint8` | 槽159经验；字段策略 Editable |
| `槽160经验` | `0x282` | 1 | `uint8` | 槽160经验；字段策略 Editable |
| `槽161经验` | `0x286` | 1 | `uint8` | 槽161经验；字段策略 Editable |
| `槽162经验` | `0x28A` | 1 | `uint8` | 槽162经验；字段策略 Editable |
| `槽163经验` | `0x28E` | 1 | `uint8` | 槽163经验；字段策略 Editable |
| `槽164经验` | `0x292` | 1 | `uint8` | 槽164经验；字段策略 Editable |
| `槽165经验` | `0x296` | 1 | `uint8` | 槽165经验；字段策略 Editable |
| `槽166经验` | `0x29A` | 1 | `uint8` | 槽166经验；字段策略 Editable |
| `槽167经验` | `0x29E` | 1 | `uint8` | 槽167经验；字段策略 Editable |
| `槽168经验` | `0x2A2` | 1 | `uint8` | 槽168经验；字段策略 Editable |
| `槽169经验` | `0x2A6` | 1 | `uint8` | 槽169经验；字段策略 Editable |
| `槽170经验` | `0x2AA` | 1 | `uint8` | 槽170经验；字段策略 Editable |
| `槽171经验` | `0x2AE` | 1 | `uint8` | 槽171经验；字段策略 Editable |
| `槽172经验` | `0x2B2` | 1 | `uint8` | 槽172经验；字段策略 Editable |
| `槽173经验` | `0x2B6` | 1 | `uint8` | 槽173经验；字段策略 Editable |
| `槽174经验` | `0x2BA` | 1 | `uint8` | 槽174经验；字段策略 Editable |
| `槽175经验` | `0x2BE` | 1 | `uint8` | 槽175经验；字段策略 Editable |
| `槽176经验` | `0x2C2` | 1 | `uint8` | 槽176经验；字段策略 Editable |
| `槽177经验` | `0x2C6` | 1 | `uint8` | 槽177经验；字段策略 Editable |
| `槽178经验` | `0x2CA` | 1 | `uint8` | 槽178经验；字段策略 Editable |
| `槽179经验` | `0x2CE` | 1 | `uint8` | 槽179经验；字段策略 Editable |
| `槽180经验` | `0x2D2` | 1 | `uint8` | 槽180经验；字段策略 Editable |
| `槽181经验` | `0x2D6` | 1 | `uint8` | 槽181经验；字段策略 Editable |
| `槽182经验` | `0x2DA` | 1 | `uint8` | 槽182经验；字段策略 Editable |
| `槽183经验` | `0x2DE` | 1 | `uint8` | 槽183经验；字段策略 Editable |
| `槽184经验` | `0x2E2` | 1 | `uint8` | 槽184经验；字段策略 Editable |
| `槽185经验` | `0x2E6` | 1 | `uint8` | 槽185经验；字段策略 Editable |
| `槽186经验` | `0x2EA` | 1 | `uint8` | 槽186经验；字段策略 Editable |
| `槽187经验` | `0x2EE` | 1 | `uint8` | 槽187经验；字段策略 Editable |
| `槽188经验` | `0x2F2` | 1 | `uint8` | 槽188经验；字段策略 Editable |
| `槽189经验` | `0x2F6` | 1 | `uint8` | 槽189经验；字段策略 Editable |
| `槽190经验` | `0x2FA` | 1 | `uint8` | 槽190经验；字段策略 Editable |
| `槽191经验` | `0x2FE` | 1 | `uint8` | 槽191经验；字段策略 Editable |
| `槽192经验` | `0x302` | 1 | `uint8` | 槽192经验；字段策略 Editable |
| `槽193经验` | `0x306` | 1 | `uint8` | 槽193经验；字段策略 Editable |
| `槽194经验` | `0x30A` | 1 | `uint8` | 槽194经验；字段策略 Editable |
| `槽195经验` | `0x30E` | 1 | `uint8` | 槽195经验；字段策略 Editable |
| `槽196经验` | `0x312` | 1 | `uint8` | 槽196经验；字段策略 Editable |
| `槽197经验` | `0x316` | 1 | `uint8` | 槽197经验；字段策略 Editable |
| `槽198经验` | `0x31A` | 1 | `uint8` | 槽198经验；字段策略 Editable |
| `槽199经验` | `0x31E` | 1 | `uint8` | 槽199经验；字段策略 Editable |
| `槽200经验` | `0x322` | 1 | `uint8` | 槽200经验；字段策略 Editable |
| `槽201经验` | `0x326` | 1 | `uint8` | 槽201经验；字段策略 Editable |
| `槽202经验` | `0x32A` | 1 | `uint8` | 槽202经验；字段策略 Editable |
| `槽203经验` | `0x32E` | 1 | `uint8` | 槽203经验；字段策略 Editable |
| `槽204经验` | `0x332` | 1 | `uint8` | 槽204经验；字段策略 Editable |
| `槽205经验` | `0x336` | 1 | `uint8` | 槽205经验；字段策略 Editable |
| `槽206经验` | `0x33A` | 1 | `uint8` | 槽206经验；字段策略 Editable |
| `槽207经验` | `0x33E` | 1 | `uint8` | 槽207经验；字段策略 Editable |
| `槽208经验` | `0x342` | 1 | `uint8` | 槽208经验；字段策略 Editable |
| `槽209经验` | `0x346` | 1 | `uint8` | 槽209经验；字段策略 Editable |
| `槽210经验` | `0x34A` | 1 | `uint8` | 槽210经验；字段策略 Editable |
| `槽211经验` | `0x34E` | 1 | `uint8` | 槽211经验；字段策略 Editable |
| `槽212经验` | `0x352` | 1 | `uint8` | 槽212经验；字段策略 Editable |
| `槽213经验` | `0x356` | 1 | `uint8` | 槽213经验；字段策略 Editable |
| `槽214经验` | `0x35A` | 1 | `uint8` | 槽214经验；字段策略 Editable |
| `槽215经验` | `0x35E` | 1 | `uint8` | 槽215经验；字段策略 Editable |
| `槽216经验` | `0x362` | 1 | `uint8` | 槽216经验；字段策略 Editable |
| `槽217经验` | `0x366` | 1 | `uint8` | 槽217经验；字段策略 Editable |
| `槽218经验` | `0x36A` | 1 | `uint8` | 槽218经验；字段策略 Editable |
| `槽219经验` | `0x36E` | 1 | `uint8` | 槽219经验；字段策略 Editable |
| `槽220经验` | `0x372` | 1 | `uint8` | 槽220经验；字段策略 Editable |
| `槽221经验` | `0x376` | 1 | `uint8` | 槽221经验；字段策略 Editable |
| `槽222经验` | `0x37A` | 1 | `uint8` | 槽222经验；字段策略 Editable |
| `槽223经验` | `0x37E` | 1 | `uint8` | 槽223经验；字段策略 Editable |
| `槽224经验` | `0x382` | 1 | `uint8` | 槽224经验；字段策略 Editable |
| `槽225经验` | `0x386` | 1 | `uint8` | 槽225经验；字段策略 Editable |
| `槽226经验` | `0x38A` | 1 | `uint8` | 槽226经验；字段策略 Editable |
| `槽227经验` | `0x38E` | 1 | `uint8` | 槽227经验；字段策略 Editable |
| `槽228经验` | `0x392` | 1 | `uint8` | 槽228经验；字段策略 Editable |
| `槽229经验` | `0x396` | 1 | `uint8` | 槽229经验；字段策略 Editable |
| `槽230经验` | `0x39A` | 1 | `uint8` | 槽230经验；字段策略 Editable |
| `槽231经验` | `0x39E` | 1 | `uint8` | 槽231经验；字段策略 Editable |
| `槽232经验` | `0x3A2` | 1 | `uint8` | 槽232经验；字段策略 Editable |
| `槽233经验` | `0x3A6` | 1 | `uint8` | 槽233经验；字段策略 Editable |
| `槽234经验` | `0x3AA` | 1 | `uint8` | 槽234经验；字段策略 Editable |
| `槽235经验` | `0x3AE` | 1 | `uint8` | 槽235经验；字段策略 Editable |
| `槽236经验` | `0x3B2` | 1 | `uint8` | 槽236经验；字段策略 Editable |
| `槽237经验` | `0x3B6` | 1 | `uint8` | 槽237经验；字段策略 Editable |
| `槽238经验` | `0x3BA` | 1 | `uint8` | 槽238经验；字段策略 Editable |
| `槽239经验` | `0x3BE` | 1 | `uint8` | 槽239经验；字段策略 Editable |
| `槽240经验` | `0x3C2` | 1 | `uint8` | 槽240经验；字段策略 Editable |
| `槽241经验` | `0x3C6` | 1 | `uint8` | 槽241经验；字段策略 Editable |
| `槽242经验` | `0x3CA` | 1 | `uint8` | 槽242经验；字段策略 Editable |
| `槽243经验` | `0x3CE` | 1 | `uint8` | 槽243经验；字段策略 Editable |
| `槽244经验` | `0x3D2` | 1 | `uint8` | 槽244经验；字段策略 Editable |
| `槽245经验` | `0x3D6` | 1 | `uint8` | 槽245经验；字段策略 Editable |
| `槽246经验` | `0x3DA` | 1 | `uint8` | 槽246经验；字段策略 Editable |
| `槽247经验` | `0x3DE` | 1 | `uint8` | 槽247经验；字段策略 Editable |
| `槽248经验` | `0x3E2` | 1 | `uint8` | 槽248经验；字段策略 Editable |
| `槽249经验` | `0x3E6` | 1 | `uint8` | 槽249经验；字段策略 Editable |
| `槽250经验` | `0x3EA` | 1 | `uint8` | 槽250经验；字段策略 Editable |
| `槽251经验` | `0x3EE` | 1 | `uint8` | 槽251经验；字段策略 Editable |
| `槽252经验` | `0x3F2` | 1 | `uint8` | 槽252经验；字段策略 Editable |
| `槽253经验` | `0x3F6` | 1 | `uint8` | 槽253经验；字段策略 Editable |
| `槽254经验` | `0x3FA` | 1 | `uint8` | 槽254经验；字段策略 Editable |
| `槽255经验` | `0x3FE` | 1 | `uint8` | 槽255经验；字段策略 Editable |
| `槽0剩余回合` | `0x3` | 1 | `uint8` | 槽0剩余回合；字段策略 Editable |
| `槽1剩余回合` | `0x7` | 1 | `uint8` | 槽1剩余回合；字段策略 Editable |
| `槽2剩余回合` | `0xB` | 1 | `uint8` | 槽2剩余回合；字段策略 Editable |
| `槽3剩余回合` | `0xF` | 1 | `uint8` | 槽3剩余回合；字段策略 Editable |
| `槽4剩余回合` | `0x13` | 1 | `uint8` | 槽4剩余回合；字段策略 Editable |
| `槽5剩余回合` | `0x17` | 1 | `uint8` | 槽5剩余回合；字段策略 Editable |
| `槽6剩余回合` | `0x1B` | 1 | `uint8` | 槽6剩余回合；字段策略 Editable |
| `槽7剩余回合` | `0x1F` | 1 | `uint8` | 槽7剩余回合；字段策略 Editable |
| `槽8剩余回合` | `0x23` | 1 | `uint8` | 槽8剩余回合；字段策略 Editable |
| `槽9剩余回合` | `0x27` | 1 | `uint8` | 槽9剩余回合；字段策略 Editable |
| `槽10剩余回合` | `0x2B` | 1 | `uint8` | 槽10剩余回合；字段策略 Editable |
| `槽11剩余回合` | `0x2F` | 1 | `uint8` | 槽11剩余回合；字段策略 Editable |
| `槽12剩余回合` | `0x33` | 1 | `uint8` | 槽12剩余回合；字段策略 Editable |
| `槽13剩余回合` | `0x37` | 1 | `uint8` | 槽13剩余回合；字段策略 Editable |
| `槽14剩余回合` | `0x3B` | 1 | `uint8` | 槽14剩余回合；字段策略 Editable |
| `槽15剩余回合` | `0x3F` | 1 | `uint8` | 槽15剩余回合；字段策略 Editable |
| `槽16剩余回合` | `0x43` | 1 | `uint8` | 槽16剩余回合；字段策略 Editable |
| `槽17剩余回合` | `0x47` | 1 | `uint8` | 槽17剩余回合；字段策略 Editable |
| `槽18剩余回合` | `0x4B` | 1 | `uint8` | 槽18剩余回合；字段策略 Editable |
| `槽19剩余回合` | `0x4F` | 1 | `uint8` | 槽19剩余回合；字段策略 Editable |
| `槽20剩余回合` | `0x53` | 1 | `uint8` | 槽20剩余回合；字段策略 Editable |
| `槽21剩余回合` | `0x57` | 1 | `uint8` | 槽21剩余回合；字段策略 Editable |
| `槽22剩余回合` | `0x5B` | 1 | `uint8` | 槽22剩余回合；字段策略 Editable |
| `槽23剩余回合` | `0x5F` | 1 | `uint8` | 槽23剩余回合；字段策略 Editable |
| `槽24剩余回合` | `0x63` | 1 | `uint8` | 槽24剩余回合；字段策略 Editable |
| `槽25剩余回合` | `0x67` | 1 | `uint8` | 槽25剩余回合；字段策略 Editable |
| `槽26剩余回合` | `0x6B` | 1 | `uint8` | 槽26剩余回合；字段策略 Editable |
| `槽27剩余回合` | `0x6F` | 1 | `uint8` | 槽27剩余回合；字段策略 Editable |
| `槽28剩余回合` | `0x73` | 1 | `uint8` | 槽28剩余回合；字段策略 Editable |
| `槽29剩余回合` | `0x77` | 1 | `uint8` | 槽29剩余回合；字段策略 Editable |
| `槽30剩余回合` | `0x7B` | 1 | `uint8` | 槽30剩余回合；字段策略 Editable |
| `槽31剩余回合` | `0x7F` | 1 | `uint8` | 槽31剩余回合；字段策略 Editable |
| `槽32剩余回合` | `0x83` | 1 | `uint8` | 槽32剩余回合；字段策略 Editable |
| `槽33剩余回合` | `0x87` | 1 | `uint8` | 槽33剩余回合；字段策略 Editable |
| `槽34剩余回合` | `0x8B` | 1 | `uint8` | 槽34剩余回合；字段策略 Editable |
| `槽35剩余回合` | `0x8F` | 1 | `uint8` | 槽35剩余回合；字段策略 Editable |
| `槽36剩余回合` | `0x93` | 1 | `uint8` | 槽36剩余回合；字段策略 Editable |
| `槽37剩余回合` | `0x97` | 1 | `uint8` | 槽37剩余回合；字段策略 Editable |
| `槽38剩余回合` | `0x9B` | 1 | `uint8` | 槽38剩余回合；字段策略 Editable |
| `槽39剩余回合` | `0x9F` | 1 | `uint8` | 槽39剩余回合；字段策略 Editable |
| `槽40剩余回合` | `0xA3` | 1 | `uint8` | 槽40剩余回合；字段策略 Editable |
| `槽41剩余回合` | `0xA7` | 1 | `uint8` | 槽41剩余回合；字段策略 Editable |
| `槽42剩余回合` | `0xAB` | 1 | `uint8` | 槽42剩余回合；字段策略 Editable |
| `槽43剩余回合` | `0xAF` | 1 | `uint8` | 槽43剩余回合；字段策略 Editable |
| `槽44剩余回合` | `0xB3` | 1 | `uint8` | 槽44剩余回合；字段策略 Editable |
| `槽45剩余回合` | `0xB7` | 1 | `uint8` | 槽45剩余回合；字段策略 Editable |
| `槽46剩余回合` | `0xBB` | 1 | `uint8` | 槽46剩余回合；字段策略 Editable |
| `槽47剩余回合` | `0xBF` | 1 | `uint8` | 槽47剩余回合；字段策略 Editable |
| `槽48剩余回合` | `0xC3` | 1 | `uint8` | 槽48剩余回合；字段策略 Editable |
| `槽49剩余回合` | `0xC7` | 1 | `uint8` | 槽49剩余回合；字段策略 Editable |
| `槽50剩余回合` | `0xCB` | 1 | `uint8` | 槽50剩余回合；字段策略 Editable |
| `槽51剩余回合` | `0xCF` | 1 | `uint8` | 槽51剩余回合；字段策略 Editable |
| `槽52剩余回合` | `0xD3` | 1 | `uint8` | 槽52剩余回合；字段策略 Editable |
| `槽53剩余回合` | `0xD7` | 1 | `uint8` | 槽53剩余回合；字段策略 Editable |
| `槽54剩余回合` | `0xDB` | 1 | `uint8` | 槽54剩余回合；字段策略 Editable |
| `槽55剩余回合` | `0xDF` | 1 | `uint8` | 槽55剩余回合；字段策略 Editable |
| `槽56剩余回合` | `0xE3` | 1 | `uint8` | 槽56剩余回合；字段策略 Editable |
| `槽57剩余回合` | `0xE7` | 1 | `uint8` | 槽57剩余回合；字段策略 Editable |
| `槽58剩余回合` | `0xEB` | 1 | `uint8` | 槽58剩余回合；字段策略 Editable |
| `槽59剩余回合` | `0xEF` | 1 | `uint8` | 槽59剩余回合；字段策略 Editable |
| `槽60剩余回合` | `0xF3` | 1 | `uint8` | 槽60剩余回合；字段策略 Editable |
| `槽61剩余回合` | `0xF7` | 1 | `uint8` | 槽61剩余回合；字段策略 Editable |
| `槽62剩余回合` | `0xFB` | 1 | `uint8` | 槽62剩余回合；字段策略 Editable |
| `槽63剩余回合` | `0xFF` | 1 | `uint8` | 槽63剩余回合；字段策略 Editable |
| `槽64剩余回合` | `0x103` | 1 | `uint8` | 槽64剩余回合；字段策略 Editable |
| `槽65剩余回合` | `0x107` | 1 | `uint8` | 槽65剩余回合；字段策略 Editable |
| `槽66剩余回合` | `0x10B` | 1 | `uint8` | 槽66剩余回合；字段策略 Editable |
| `槽67剩余回合` | `0x10F` | 1 | `uint8` | 槽67剩余回合；字段策略 Editable |
| `槽68剩余回合` | `0x113` | 1 | `uint8` | 槽68剩余回合；字段策略 Editable |
| `槽69剩余回合` | `0x117` | 1 | `uint8` | 槽69剩余回合；字段策略 Editable |
| `槽70剩余回合` | `0x11B` | 1 | `uint8` | 槽70剩余回合；字段策略 Editable |
| `槽71剩余回合` | `0x11F` | 1 | `uint8` | 槽71剩余回合；字段策略 Editable |
| `槽72剩余回合` | `0x123` | 1 | `uint8` | 槽72剩余回合；字段策略 Editable |
| `槽73剩余回合` | `0x127` | 1 | `uint8` | 槽73剩余回合；字段策略 Editable |
| `槽74剩余回合` | `0x12B` | 1 | `uint8` | 槽74剩余回合；字段策略 Editable |
| `槽75剩余回合` | `0x12F` | 1 | `uint8` | 槽75剩余回合；字段策略 Editable |
| `槽76剩余回合` | `0x133` | 1 | `uint8` | 槽76剩余回合；字段策略 Editable |
| `槽77剩余回合` | `0x137` | 1 | `uint8` | 槽77剩余回合；字段策略 Editable |
| `槽78剩余回合` | `0x13B` | 1 | `uint8` | 槽78剩余回合；字段策略 Editable |
| `槽79剩余回合` | `0x13F` | 1 | `uint8` | 槽79剩余回合；字段策略 Editable |
| `槽80剩余回合` | `0x143` | 1 | `uint8` | 槽80剩余回合；字段策略 Editable |
| `槽81剩余回合` | `0x147` | 1 | `uint8` | 槽81剩余回合；字段策略 Editable |
| `槽82剩余回合` | `0x14B` | 1 | `uint8` | 槽82剩余回合；字段策略 Editable |
| `槽83剩余回合` | `0x14F` | 1 | `uint8` | 槽83剩余回合；字段策略 Editable |
| `槽84剩余回合` | `0x153` | 1 | `uint8` | 槽84剩余回合；字段策略 Editable |
| `槽85剩余回合` | `0x157` | 1 | `uint8` | 槽85剩余回合；字段策略 Editable |
| `槽86剩余回合` | `0x15B` | 1 | `uint8` | 槽86剩余回合；字段策略 Editable |
| `槽87剩余回合` | `0x15F` | 1 | `uint8` | 槽87剩余回合；字段策略 Editable |
| `槽88剩余回合` | `0x163` | 1 | `uint8` | 槽88剩余回合；字段策略 Editable |
| `槽89剩余回合` | `0x167` | 1 | `uint8` | 槽89剩余回合；字段策略 Editable |
| `槽90剩余回合` | `0x16B` | 1 | `uint8` | 槽90剩余回合；字段策略 Editable |
| `槽91剩余回合` | `0x16F` | 1 | `uint8` | 槽91剩余回合；字段策略 Editable |
| `槽92剩余回合` | `0x173` | 1 | `uint8` | 槽92剩余回合；字段策略 Editable |
| `槽93剩余回合` | `0x177` | 1 | `uint8` | 槽93剩余回合；字段策略 Editable |
| `槽94剩余回合` | `0x17B` | 1 | `uint8` | 槽94剩余回合；字段策略 Editable |
| `槽95剩余回合` | `0x17F` | 1 | `uint8` | 槽95剩余回合；字段策略 Editable |
| `槽96剩余回合` | `0x183` | 1 | `uint8` | 槽96剩余回合；字段策略 Editable |
| `槽97剩余回合` | `0x187` | 1 | `uint8` | 槽97剩余回合；字段策略 Editable |
| `槽98剩余回合` | `0x18B` | 1 | `uint8` | 槽98剩余回合；字段策略 Editable |
| `槽99剩余回合` | `0x18F` | 1 | `uint8` | 槽99剩余回合；字段策略 Editable |
| `槽100剩余回合` | `0x193` | 1 | `uint8` | 槽100剩余回合；字段策略 Editable |
| `槽101剩余回合` | `0x197` | 1 | `uint8` | 槽101剩余回合；字段策略 Editable |
| `槽102剩余回合` | `0x19B` | 1 | `uint8` | 槽102剩余回合；字段策略 Editable |
| `槽103剩余回合` | `0x19F` | 1 | `uint8` | 槽103剩余回合；字段策略 Editable |
| `槽104剩余回合` | `0x1A3` | 1 | `uint8` | 槽104剩余回合；字段策略 Editable |
| `槽105剩余回合` | `0x1A7` | 1 | `uint8` | 槽105剩余回合；字段策略 Editable |
| `槽106剩余回合` | `0x1AB` | 1 | `uint8` | 槽106剩余回合；字段策略 Editable |
| `槽107剩余回合` | `0x1AF` | 1 | `uint8` | 槽107剩余回合；字段策略 Editable |
| `槽108剩余回合` | `0x1B3` | 1 | `uint8` | 槽108剩余回合；字段策略 Editable |
| `槽109剩余回合` | `0x1B7` | 1 | `uint8` | 槽109剩余回合；字段策略 Editable |
| `槽110剩余回合` | `0x1BB` | 1 | `uint8` | 槽110剩余回合；字段策略 Editable |
| `槽111剩余回合` | `0x1BF` | 1 | `uint8` | 槽111剩余回合；字段策略 Editable |
| `槽112剩余回合` | `0x1C3` | 1 | `uint8` | 槽112剩余回合；字段策略 Editable |
| `槽113剩余回合` | `0x1C7` | 1 | `uint8` | 槽113剩余回合；字段策略 Editable |
| `槽114剩余回合` | `0x1CB` | 1 | `uint8` | 槽114剩余回合；字段策略 Editable |
| `槽115剩余回合` | `0x1CF` | 1 | `uint8` | 槽115剩余回合；字段策略 Editable |
| `槽116剩余回合` | `0x1D3` | 1 | `uint8` | 槽116剩余回合；字段策略 Editable |
| `槽117剩余回合` | `0x1D7` | 1 | `uint8` | 槽117剩余回合；字段策略 Editable |
| `槽118剩余回合` | `0x1DB` | 1 | `uint8` | 槽118剩余回合；字段策略 Editable |
| `槽119剩余回合` | `0x1DF` | 1 | `uint8` | 槽119剩余回合；字段策略 Editable |
| `槽120剩余回合` | `0x1E3` | 1 | `uint8` | 槽120剩余回合；字段策略 Editable |
| `槽121剩余回合` | `0x1E7` | 1 | `uint8` | 槽121剩余回合；字段策略 Editable |
| `槽122剩余回合` | `0x1EB` | 1 | `uint8` | 槽122剩余回合；字段策略 Editable |
| `槽123剩余回合` | `0x1EF` | 1 | `uint8` | 槽123剩余回合；字段策略 Editable |
| `槽124剩余回合` | `0x1F3` | 1 | `uint8` | 槽124剩余回合；字段策略 Editable |
| `槽125剩余回合` | `0x1F7` | 1 | `uint8` | 槽125剩余回合；字段策略 Editable |
| `槽126剩余回合` | `0x1FB` | 1 | `uint8` | 槽126剩余回合；字段策略 Editable |
| `槽127剩余回合` | `0x1FF` | 1 | `uint8` | 槽127剩余回合；字段策略 Editable |
| `槽128剩余回合` | `0x203` | 1 | `uint8` | 槽128剩余回合；字段策略 Editable |
| `槽129剩余回合` | `0x207` | 1 | `uint8` | 槽129剩余回合；字段策略 Editable |
| `槽130剩余回合` | `0x20B` | 1 | `uint8` | 槽130剩余回合；字段策略 Editable |
| `槽131剩余回合` | `0x20F` | 1 | `uint8` | 槽131剩余回合；字段策略 Editable |
| `槽132剩余回合` | `0x213` | 1 | `uint8` | 槽132剩余回合；字段策略 Editable |
| `槽133剩余回合` | `0x217` | 1 | `uint8` | 槽133剩余回合；字段策略 Editable |
| `槽134剩余回合` | `0x21B` | 1 | `uint8` | 槽134剩余回合；字段策略 Editable |
| `槽135剩余回合` | `0x21F` | 1 | `uint8` | 槽135剩余回合；字段策略 Editable |
| `槽136剩余回合` | `0x223` | 1 | `uint8` | 槽136剩余回合；字段策略 Editable |
| `槽137剩余回合` | `0x227` | 1 | `uint8` | 槽137剩余回合；字段策略 Editable |
| `槽138剩余回合` | `0x22B` | 1 | `uint8` | 槽138剩余回合；字段策略 Editable |
| `槽139剩余回合` | `0x22F` | 1 | `uint8` | 槽139剩余回合；字段策略 Editable |
| `槽140剩余回合` | `0x233` | 1 | `uint8` | 槽140剩余回合；字段策略 Editable |
| `槽141剩余回合` | `0x237` | 1 | `uint8` | 槽141剩余回合；字段策略 Editable |
| `槽142剩余回合` | `0x23B` | 1 | `uint8` | 槽142剩余回合；字段策略 Editable |
| `槽143剩余回合` | `0x23F` | 1 | `uint8` | 槽143剩余回合；字段策略 Editable |
| `槽144剩余回合` | `0x243` | 1 | `uint8` | 槽144剩余回合；字段策略 Editable |
| `槽145剩余回合` | `0x247` | 1 | `uint8` | 槽145剩余回合；字段策略 Editable |
| `槽146剩余回合` | `0x24B` | 1 | `uint8` | 槽146剩余回合；字段策略 Editable |
| `槽147剩余回合` | `0x24F` | 1 | `uint8` | 槽147剩余回合；字段策略 Editable |
| `槽148剩余回合` | `0x253` | 1 | `uint8` | 槽148剩余回合；字段策略 Editable |
| `槽149剩余回合` | `0x257` | 1 | `uint8` | 槽149剩余回合；字段策略 Editable |
| `槽150剩余回合` | `0x25B` | 1 | `uint8` | 槽150剩余回合；字段策略 Editable |
| `槽151剩余回合` | `0x25F` | 1 | `uint8` | 槽151剩余回合；字段策略 Editable |
| `槽152剩余回合` | `0x263` | 1 | `uint8` | 槽152剩余回合；字段策略 Editable |
| `槽153剩余回合` | `0x267` | 1 | `uint8` | 槽153剩余回合；字段策略 Editable |
| `槽154剩余回合` | `0x26B` | 1 | `uint8` | 槽154剩余回合；字段策略 Editable |
| `槽155剩余回合` | `0x26F` | 1 | `uint8` | 槽155剩余回合；字段策略 Editable |
| `槽156剩余回合` | `0x273` | 1 | `uint8` | 槽156剩余回合；字段策略 Editable |
| `槽157剩余回合` | `0x277` | 1 | `uint8` | 槽157剩余回合；字段策略 Editable |
| `槽158剩余回合` | `0x27B` | 1 | `uint8` | 槽158剩余回合；字段策略 Editable |
| `槽159剩余回合` | `0x27F` | 1 | `uint8` | 槽159剩余回合；字段策略 Editable |
| `槽160剩余回合` | `0x283` | 1 | `uint8` | 槽160剩余回合；字段策略 Editable |
| `槽161剩余回合` | `0x287` | 1 | `uint8` | 槽161剩余回合；字段策略 Editable |
| `槽162剩余回合` | `0x28B` | 1 | `uint8` | 槽162剩余回合；字段策略 Editable |
| `槽163剩余回合` | `0x28F` | 1 | `uint8` | 槽163剩余回合；字段策略 Editable |
| `槽164剩余回合` | `0x293` | 1 | `uint8` | 槽164剩余回合；字段策略 Editable |
| `槽165剩余回合` | `0x297` | 1 | `uint8` | 槽165剩余回合；字段策略 Editable |
| `槽166剩余回合` | `0x29B` | 1 | `uint8` | 槽166剩余回合；字段策略 Editable |
| `槽167剩余回合` | `0x29F` | 1 | `uint8` | 槽167剩余回合；字段策略 Editable |
| `槽168剩余回合` | `0x2A3` | 1 | `uint8` | 槽168剩余回合；字段策略 Editable |
| `槽169剩余回合` | `0x2A7` | 1 | `uint8` | 槽169剩余回合；字段策略 Editable |
| `槽170剩余回合` | `0x2AB` | 1 | `uint8` | 槽170剩余回合；字段策略 Editable |
| `槽171剩余回合` | `0x2AF` | 1 | `uint8` | 槽171剩余回合；字段策略 Editable |
| `槽172剩余回合` | `0x2B3` | 1 | `uint8` | 槽172剩余回合；字段策略 Editable |
| `槽173剩余回合` | `0x2B7` | 1 | `uint8` | 槽173剩余回合；字段策略 Editable |
| `槽174剩余回合` | `0x2BB` | 1 | `uint8` | 槽174剩余回合；字段策略 Editable |
| `槽175剩余回合` | `0x2BF` | 1 | `uint8` | 槽175剩余回合；字段策略 Editable |
| `槽176剩余回合` | `0x2C3` | 1 | `uint8` | 槽176剩余回合；字段策略 Editable |
| `槽177剩余回合` | `0x2C7` | 1 | `uint8` | 槽177剩余回合；字段策略 Editable |
| `槽178剩余回合` | `0x2CB` | 1 | `uint8` | 槽178剩余回合；字段策略 Editable |
| `槽179剩余回合` | `0x2CF` | 1 | `uint8` | 槽179剩余回合；字段策略 Editable |
| `槽180剩余回合` | `0x2D3` | 1 | `uint8` | 槽180剩余回合；字段策略 Editable |
| `槽181剩余回合` | `0x2D7` | 1 | `uint8` | 槽181剩余回合；字段策略 Editable |
| `槽182剩余回合` | `0x2DB` | 1 | `uint8` | 槽182剩余回合；字段策略 Editable |
| `槽183剩余回合` | `0x2DF` | 1 | `uint8` | 槽183剩余回合；字段策略 Editable |
| `槽184剩余回合` | `0x2E3` | 1 | `uint8` | 槽184剩余回合；字段策略 Editable |
| `槽185剩余回合` | `0x2E7` | 1 | `uint8` | 槽185剩余回合；字段策略 Editable |
| `槽186剩余回合` | `0x2EB` | 1 | `uint8` | 槽186剩余回合；字段策略 Editable |
| `槽187剩余回合` | `0x2EF` | 1 | `uint8` | 槽187剩余回合；字段策略 Editable |
| `槽188剩余回合` | `0x2F3` | 1 | `uint8` | 槽188剩余回合；字段策略 Editable |
| `槽189剩余回合` | `0x2F7` | 1 | `uint8` | 槽189剩余回合；字段策略 Editable |
| `槽190剩余回合` | `0x2FB` | 1 | `uint8` | 槽190剩余回合；字段策略 Editable |
| `槽191剩余回合` | `0x2FF` | 1 | `uint8` | 槽191剩余回合；字段策略 Editable |
| `槽192剩余回合` | `0x303` | 1 | `uint8` | 槽192剩余回合；字段策略 Editable |
| `槽193剩余回合` | `0x307` | 1 | `uint8` | 槽193剩余回合；字段策略 Editable |
| `槽194剩余回合` | `0x30B` | 1 | `uint8` | 槽194剩余回合；字段策略 Editable |
| `槽195剩余回合` | `0x30F` | 1 | `uint8` | 槽195剩余回合；字段策略 Editable |
| `槽196剩余回合` | `0x313` | 1 | `uint8` | 槽196剩余回合；字段策略 Editable |
| `槽197剩余回合` | `0x317` | 1 | `uint8` | 槽197剩余回合；字段策略 Editable |
| `槽198剩余回合` | `0x31B` | 1 | `uint8` | 槽198剩余回合；字段策略 Editable |
| `槽199剩余回合` | `0x31F` | 1 | `uint8` | 槽199剩余回合；字段策略 Editable |
| `槽200剩余回合` | `0x323` | 1 | `uint8` | 槽200剩余回合；字段策略 Editable |
| `槽201剩余回合` | `0x327` | 1 | `uint8` | 槽201剩余回合；字段策略 Editable |
| `槽202剩余回合` | `0x32B` | 1 | `uint8` | 槽202剩余回合；字段策略 Editable |
| `槽203剩余回合` | `0x32F` | 1 | `uint8` | 槽203剩余回合；字段策略 Editable |
| `槽204剩余回合` | `0x333` | 1 | `uint8` | 槽204剩余回合；字段策略 Editable |
| `槽205剩余回合` | `0x337` | 1 | `uint8` | 槽205剩余回合；字段策略 Editable |
| `槽206剩余回合` | `0x33B` | 1 | `uint8` | 槽206剩余回合；字段策略 Editable |
| `槽207剩余回合` | `0x33F` | 1 | `uint8` | 槽207剩余回合；字段策略 Editable |
| `槽208剩余回合` | `0x343` | 1 | `uint8` | 槽208剩余回合；字段策略 Editable |
| `槽209剩余回合` | `0x347` | 1 | `uint8` | 槽209剩余回合；字段策略 Editable |
| `槽210剩余回合` | `0x34B` | 1 | `uint8` | 槽210剩余回合；字段策略 Editable |
| `槽211剩余回合` | `0x34F` | 1 | `uint8` | 槽211剩余回合；字段策略 Editable |
| `槽212剩余回合` | `0x353` | 1 | `uint8` | 槽212剩余回合；字段策略 Editable |
| `槽213剩余回合` | `0x357` | 1 | `uint8` | 槽213剩余回合；字段策略 Editable |
| `槽214剩余回合` | `0x35B` | 1 | `uint8` | 槽214剩余回合；字段策略 Editable |
| `槽215剩余回合` | `0x35F` | 1 | `uint8` | 槽215剩余回合；字段策略 Editable |
| `槽216剩余回合` | `0x363` | 1 | `uint8` | 槽216剩余回合；字段策略 Editable |
| `槽217剩余回合` | `0x367` | 1 | `uint8` | 槽217剩余回合；字段策略 Editable |
| `槽218剩余回合` | `0x36B` | 1 | `uint8` | 槽218剩余回合；字段策略 Editable |
| `槽219剩余回合` | `0x36F` | 1 | `uint8` | 槽219剩余回合；字段策略 Editable |
| `槽220剩余回合` | `0x373` | 1 | `uint8` | 槽220剩余回合；字段策略 Editable |
| `槽221剩余回合` | `0x377` | 1 | `uint8` | 槽221剩余回合；字段策略 Editable |
| `槽222剩余回合` | `0x37B` | 1 | `uint8` | 槽222剩余回合；字段策略 Editable |
| `槽223剩余回合` | `0x37F` | 1 | `uint8` | 槽223剩余回合；字段策略 Editable |
| `槽224剩余回合` | `0x383` | 1 | `uint8` | 槽224剩余回合；字段策略 Editable |
| `槽225剩余回合` | `0x387` | 1 | `uint8` | 槽225剩余回合；字段策略 Editable |
| `槽226剩余回合` | `0x38B` | 1 | `uint8` | 槽226剩余回合；字段策略 Editable |
| `槽227剩余回合` | `0x38F` | 1 | `uint8` | 槽227剩余回合；字段策略 Editable |
| `槽228剩余回合` | `0x393` | 1 | `uint8` | 槽228剩余回合；字段策略 Editable |
| `槽229剩余回合` | `0x397` | 1 | `uint8` | 槽229剩余回合；字段策略 Editable |
| `槽230剩余回合` | `0x39B` | 1 | `uint8` | 槽230剩余回合；字段策略 Editable |
| `槽231剩余回合` | `0x39F` | 1 | `uint8` | 槽231剩余回合；字段策略 Editable |
| `槽232剩余回合` | `0x3A3` | 1 | `uint8` | 槽232剩余回合；字段策略 Editable |
| `槽233剩余回合` | `0x3A7` | 1 | `uint8` | 槽233剩余回合；字段策略 Editable |
| `槽234剩余回合` | `0x3AB` | 1 | `uint8` | 槽234剩余回合；字段策略 Editable |
| `槽235剩余回合` | `0x3AF` | 1 | `uint8` | 槽235剩余回合；字段策略 Editable |
| `槽236剩余回合` | `0x3B3` | 1 | `uint8` | 槽236剩余回合；字段策略 Editable |
| `槽237剩余回合` | `0x3B7` | 1 | `uint8` | 槽237剩余回合；字段策略 Editable |
| `槽238剩余回合` | `0x3BB` | 1 | `uint8` | 槽238剩余回合；字段策略 Editable |
| `槽239剩余回合` | `0x3BF` | 1 | `uint8` | 槽239剩余回合；字段策略 Editable |
| `槽240剩余回合` | `0x3C3` | 1 | `uint8` | 槽240剩余回合；字段策略 Editable |
| `槽241剩余回合` | `0x3C7` | 1 | `uint8` | 槽241剩余回合；字段策略 Editable |
| `槽242剩余回合` | `0x3CB` | 1 | `uint8` | 槽242剩余回合；字段策略 Editable |
| `槽243剩余回合` | `0x3CF` | 1 | `uint8` | 槽243剩余回合；字段策略 Editable |
| `槽244剩余回合` | `0x3D3` | 1 | `uint8` | 槽244剩余回合；字段策略 Editable |
| `槽245剩余回合` | `0x3D7` | 1 | `uint8` | 槽245剩余回合；字段策略 Editable |
| `槽246剩余回合` | `0x3DB` | 1 | `uint8` | 槽246剩余回合；字段策略 Editable |
| `槽247剩余回合` | `0x3DF` | 1 | `uint8` | 槽247剩余回合；字段策略 Editable |
| `槽248剩余回合` | `0x3E3` | 1 | `uint8` | 槽248剩余回合；字段策略 Editable |
| `槽249剩余回合` | `0x3E7` | 1 | `uint8` | 槽249剩余回合；字段策略 Editable |
| `槽250剩余回合` | `0x3EB` | 1 | `uint8` | 槽250剩余回合；字段策略 Editable |
| `槽251剩余回合` | `0x3EF` | 1 | `uint8` | 槽251剩余回合；字段策略 Editable |
| `槽252剩余回合` | `0x3F3` | 1 | `uint8` | 槽252剩余回合；字段策略 Editable |
| `槽253剩余回合` | `0x3F7` | 1 | `uint8` | 槽253剩余回合；字段策略 Editable |
| `槽254剩余回合` | `0x3FB` | 1 | `uint8` | 槽254剩余回合；字段策略 Editable |
| `槽255剩余回合` | `0x3FF` | 1 | `uint8` | 槽255剩余回合；字段策略 Editable |

## 66-legacy-data-v1 特效成长拓展（effect-messages 物理表）

ID: `struct.66.disk.66-legacy-data-v1.effect-messages`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x8` (8)

索引公式: `Effectmsg.e5 + 0x0 + (ID - 0) * 0x8 + field_offset; ID=0..254`

存储：`Effectmsg.e5`；起点：`0x0` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x7F8`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `Enabled` | `0x0` | 1 | `uint8` | Enabled；字段策略 Editable |
| `Param1` | `0x1` | 1 | `uint8` | Param1；字段策略 Editable |
| `Param2` | `0x2` | 1 | `uint8` | Param2；字段策略 Editable |
| `Param3` | `0x3` | 1 | `uint8` | Param3；字段策略 Editable |
| `Param4` | `0x4` | 1 | `uint8` | Param4；字段策略 Editable |
| `Param5` | `0x5` | 1 | `uint8` | Param5；字段策略 Editable |
| `Param6` | `0x6` | 1 | `uint8` | Param6；字段策略 Editable |
| `Param7` | `0x7` | 1 | `uint8` | Param7；字段策略 Editable |

## 66-legacy-data-v1 策略学习拓展（strategy-study-extended 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-study-extended`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x40` (64)

索引公式: `MeffStudy.e5 + 0x0 + (ID - 0) * 0x40 + field_offset; ID=0..1023`

存储：`MeffStudy.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x10000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略0ID` | `0x0` | 1 | `uint8` | 策略0ID；字段策略 Editable |
| `策略1ID` | `0x2` | 1 | `uint8` | 策略1ID；字段策略 Editable |
| `策略2ID` | `0x4` | 1 | `uint8` | 策略2ID；字段策略 Editable |
| `策略3ID` | `0x6` | 1 | `uint8` | 策略3ID；字段策略 Editable |
| `策略4ID` | `0x8` | 1 | `uint8` | 策略4ID；字段策略 Editable |
| `策略5ID` | `0xA` | 1 | `uint8` | 策略5ID；字段策略 Editable |
| `策略6ID` | `0xC` | 1 | `uint8` | 策略6ID；字段策略 Editable |
| `策略7ID` | `0xE` | 1 | `uint8` | 策略7ID；字段策略 Editable |
| `策略8ID` | `0x10` | 1 | `uint8` | 策略8ID；字段策略 Editable |
| `策略9ID` | `0x12` | 1 | `uint8` | 策略9ID；字段策略 Editable |
| `策略10ID` | `0x14` | 1 | `uint8` | 策略10ID；字段策略 Editable |
| `策略11ID` | `0x16` | 1 | `uint8` | 策略11ID；字段策略 Editable |
| `策略12ID` | `0x18` | 1 | `uint8` | 策略12ID；字段策略 Editable |
| `策略13ID` | `0x1A` | 1 | `uint8` | 策略13ID；字段策略 Editable |
| `策略14ID` | `0x1C` | 1 | `uint8` | 策略14ID；字段策略 Editable |
| `策略15ID` | `0x1E` | 1 | `uint8` | 策略15ID；字段策略 Editable |
| `策略16ID` | `0x20` | 1 | `uint8` | 策略16ID；字段策略 Editable |
| `策略17ID` | `0x22` | 1 | `uint8` | 策略17ID；字段策略 Editable |
| `策略18ID` | `0x24` | 1 | `uint8` | 策略18ID；字段策略 Editable |
| `策略19ID` | `0x26` | 1 | `uint8` | 策略19ID；字段策略 Editable |
| `策略20ID` | `0x28` | 1 | `uint8` | 策略20ID；字段策略 Editable |
| `策略21ID` | `0x2A` | 1 | `uint8` | 策略21ID；字段策略 Editable |
| `策略22ID` | `0x2C` | 1 | `uint8` | 策略22ID；字段策略 Editable |
| `策略23ID` | `0x2E` | 1 | `uint8` | 策略23ID；字段策略 Editable |
| `策略24ID` | `0x30` | 1 | `uint8` | 策略24ID；字段策略 Editable |
| `策略25ID` | `0x32` | 1 | `uint8` | 策略25ID；字段策略 Editable |
| `策略26ID` | `0x34` | 1 | `uint8` | 策略26ID；字段策略 Editable |
| `策略27ID` | `0x36` | 1 | `uint8` | 策略27ID；字段策略 Editable |
| `策略28ID` | `0x38` | 1 | `uint8` | 策略28ID；字段策略 Editable |
| `策略29ID` | `0x3A` | 1 | `uint8` | 策略29ID；字段策略 Editable |
| `策略30ID` | `0x3C` | 1 | `uint8` | 策略30ID；字段策略 Editable |
| `策略31ID` | `0x3E` | 1 | `uint8` | 策略31ID；字段策略 Editable |
| `策略0次数` | `0x1` | 1 | `uint8` | 策略0次数；字段策略 Editable |
| `策略1次数` | `0x3` | 1 | `uint8` | 策略1次数；字段策略 Editable |
| `策略2次数` | `0x5` | 1 | `uint8` | 策略2次数；字段策略 Editable |
| `策略3次数` | `0x7` | 1 | `uint8` | 策略3次数；字段策略 Editable |
| `策略4次数` | `0x9` | 1 | `uint8` | 策略4次数；字段策略 Editable |
| `策略5次数` | `0xB` | 1 | `uint8` | 策略5次数；字段策略 Editable |
| `策略6次数` | `0xD` | 1 | `uint8` | 策略6次数；字段策略 Editable |
| `策略7次数` | `0xF` | 1 | `uint8` | 策略7次数；字段策略 Editable |
| `策略8次数` | `0x11` | 1 | `uint8` | 策略8次数；字段策略 Editable |
| `策略9次数` | `0x13` | 1 | `uint8` | 策略9次数；字段策略 Editable |
| `策略10次数` | `0x15` | 1 | `uint8` | 策略10次数；字段策略 Editable |
| `策略11次数` | `0x17` | 1 | `uint8` | 策略11次数；字段策略 Editable |
| `策略12次数` | `0x19` | 1 | `uint8` | 策略12次数；字段策略 Editable |
| `策略13次数` | `0x1B` | 1 | `uint8` | 策略13次数；字段策略 Editable |
| `策略14次数` | `0x1D` | 1 | `uint8` | 策略14次数；字段策略 Editable |
| `策略15次数` | `0x1F` | 1 | `uint8` | 策略15次数；字段策略 Editable |
| `策略16次数` | `0x21` | 1 | `uint8` | 策略16次数；字段策略 Editable |
| `策略17次数` | `0x23` | 1 | `uint8` | 策略17次数；字段策略 Editable |
| `策略18次数` | `0x25` | 1 | `uint8` | 策略18次数；字段策略 Editable |
| `策略19次数` | `0x27` | 1 | `uint8` | 策略19次数；字段策略 Editable |
| `策略20次数` | `0x29` | 1 | `uint8` | 策略20次数；字段策略 Editable |
| `策略21次数` | `0x2B` | 1 | `uint8` | 策略21次数；字段策略 Editable |
| `策略22次数` | `0x2D` | 1 | `uint8` | 策略22次数；字段策略 Editable |
| `策略23次数` | `0x2F` | 1 | `uint8` | 策略23次数；字段策略 Editable |
| `策略24次数` | `0x31` | 1 | `uint8` | 策略24次数；字段策略 Editable |
| `策略25次数` | `0x33` | 1 | `uint8` | 策略25次数；字段策略 Editable |
| `策略26次数` | `0x35` | 1 | `uint8` | 策略26次数；字段策略 Editable |
| `策略27次数` | `0x37` | 1 | `uint8` | 策略27次数；字段策略 Editable |
| `策略28次数` | `0x39` | 1 | `uint8` | 策略28次数；字段策略 Editable |
| `策略29次数` | `0x3B` | 1 | `uint8` | 策略29次数；字段策略 Editable |
| `策略30次数` | `0x3D` | 1 | `uint8` | 策略30次数；字段策略 Editable |
| `策略31次数` | `0x3F` | 1 | `uint8` | 策略31次数；字段策略 Editable |

## 66-legacy-data-v1 锻造（forge 物理表）

ID: `struct.66.disk.66-legacy-data-v1.forge`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x40` (64)

索引公式: `Forge.e5 + 0x0 + (ID - 0) * 0x40 + field_offset; ID=0..1023`

存储：`Forge.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x10000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 30 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `材料1ID` | `0x1E` | 2 | `uint16le` | 材料1ID；字段策略 Editable |
| `材料2ID` | `0x21` | 2 | `uint16le` | 材料2ID；字段策略 Editable |
| `材料3ID` | `0x24` | 2 | `uint16le` | 材料3ID；字段策略 Editable |
| `材料4ID` | `0x27` | 2 | `uint16le` | 材料4ID；字段策略 Editable |
| `材料5ID` | `0x2A` | 2 | `uint16le` | 材料5ID；字段策略 Editable |
| `材料6ID` | `0x2D` | 2 | `uint16le` | 材料6ID；字段策略 Editable |
| `材料7ID` | `0x30` | 2 | `uint16le` | 材料7ID；字段策略 Editable |
| `材料8ID` | `0x33` | 2 | `uint16le` | 材料8ID；字段策略 Editable |
| `材料1数量` | `0x20` | 1 | `uint8` | 材料1数量；字段策略 Editable |
| `材料2数量` | `0x23` | 1 | `uint8` | 材料2数量；字段策略 Editable |
| `材料3数量` | `0x26` | 1 | `uint8` | 材料3数量；字段策略 Editable |
| `材料4数量` | `0x29` | 1 | `uint8` | 材料4数量；字段策略 Editable |
| `材料5数量` | `0x2C` | 1 | `uint8` | 材料5数量；字段策略 Editable |
| `材料6数量` | `0x2F` | 1 | `uint8` | 材料6数量；字段策略 Editable |
| `材料7数量` | `0x32` | 1 | `uint8` | 材料7数量；字段策略 Editable |
| `材料8数量` | `0x35` | 1 | `uint8` | 材料8数量；字段策略 Editable |
| `价格` | `0x36` | 4 | `uint32le` | 价格；字段策略 Editable |
| `保留58` | `0x3A` | 1 | `bytes` | 保留58；字段策略 Preserve |
| `材料项数` | `0x3A` | 1 | `uint8` | 材料项数；字段策略 Editable |
| `保留59` | `0x3B` | 1 | `bytes` | 保留59；字段策略 Preserve |
| `商店编号` | `0x3B` | 1 | `uint8` | 商店编号；字段策略 Editable |
| `标记` | `0x3C` | 1 | `uint8` | 标记；字段策略 Editable |
| `保留61` | `0x3D` | 1 | `bytes` | 保留61；字段策略 Preserve |
| `剩余次数` | `0x3D` | 1 | `uint8` | 剩余次数；字段策略 Editable |

## 66-legacy-data-v1 策略大动画（strategy-big-animation 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-big-animation`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA31F0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA31F0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3280`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `动画ID` | `0x0` | 1 | `uint8` | 动画ID；字段策略 Editable |

## 66-legacy-data-v1 策略小动画（strategy-small-animation 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-small-animation`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA3160 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA3160` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA31F0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `动画ID` | `0x0` | 1 | `uint8` | 动画ID；字段策略 Editable |

## 66-legacy-data-v1 兵种系·辅助装备分组（job-series-accessory-groups 物理表）

ID: `struct.66.disk.66-legacy-data-v1.job-series-accessory-groups`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `不解析占位 offset=0；实际地址由 VA 0x0044C341 经目标 PE 节表映射；参见 format.65.accessory-job-groups`

存储：`Ekd5.exe`；起点：-；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x1`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 辅助分组不是定长物理表；请在兵种系的辅助分组业务页使用 PE 地址/FF 分隔专用服务及专用 CSV。禁止解码此占位偏移或导出 EXE 文件头。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `Raw` | `0x0` | 1 | `bytes` | Raw；字段策略 Preserve |

## 66-legacy-data-v1 策略施展地形（strategy-terrain-availability 物理表）

ID: `struct.66.disk.66-legacy-data-v1.strategy-terrain-availability`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0x1FECC + (ID - 0) * 0x1 + field_offset; ID=0..29`

存储：`Ekd5.exe`；起点：`0x1FECC` (fileOffset)；记录数：`30`；ID 起点：`0`；结束偏移（不含）：`0x1FEEA`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略施展地形掩码` | `0x0` | 1 | `uint8` | 策略施展地形掩码；字段策略 Editable |

## 66-legacy-data-v1 装备特效名称池（1A-57）（item-effect-names-low 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-effect-names-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x375` (885)

索引公式: `Ekd5.exe + 0x8A9E8 + (ID - 0) * 0x375 + field_offset; ID=0..0`

存储：`Ekd5.exe`；起点：`0x8A9E8` (fileOffset)；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x8AD5D`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 装备特效名称使用 item-effect-names-66 固定 16 字节名称池，禁止读取或写入 6.5 低段变长池偏移。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `RawHex` | `0x0` | 885 | `bytes` | RawHex；字段策略 Preserve |

## 66-legacy-data-v1 装备特效名称池（58-7F）（item-effect-names-high 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-effect-names-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x170` (368)

索引公式: `Ekd5.exe + 0x9F800 + (ID - 0) * 0x170 + field_offset; ID=0..0`

存储：`Ekd5.exe`；起点：`0x9F800` (fileOffset)；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x9F970`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 装备特效名称使用 item-effect-names-66 固定 16 字节名称池，禁止读取或写入 6.5 高段变长池偏移。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `RawHex` | `0x0` | 368 | `bytes` | RawHex；字段策略 Preserve |

## 66-legacy-data-v1 必杀（finishing-moves 物理表）

ID: `struct.66.disk.66-legacy-data-v1.finishing-moves`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Data.e5 + 0xE894 + (ID - 0) * 0x10 + field_offset; ID=0..95`

存储：`Data.e5`；起点：`0xE894` (fileOffset)；记录数：`96`；ID 起点：`0`；结束偏移（不含）：`0xEE94`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 61379 | True | `608A7E1D75EA0F179DABB850C66CF236FF9E55EB4A323F0CB213A92E7BF6FDDA` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 11 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `图标` | `0xB` | 1 | `bytes` | 图标；字段策略 Preserve |
| `攻击范围` | `0xC` | 1 | `uint8` | 攻击范围；字段策略 Editable |
| `穿透范围` | `0xD` | 1 | `uint8` | 穿透范围；字段策略 Editable |
| `消耗SP` | `0xE` | 1 | `uint8` | 消耗SP；字段策略 Editable |

## 66-legacy-data-v1 必杀说明（finishing-move-description 物理表）

ID: `struct.66.disk.66-legacy-data-v1.finishing-move-description`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x7080 + (ID - 0) * 0xC8 + field_offset; ID=0..95`

存储：`Imsg.e5`；起点：`0x7080` (fileOffset)；记录数：`96`；ID 起点：`0`；结束偏移（不含）：`0xBB80`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | True | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `说明` | `0x0` | 200 | `fixed-string` | 说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 物品获取说明（0-103）（item-acquisition-low 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-acquisition-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x6B5F8 + (ID - 0) * 0xC8 + field_offset; ID=0..103`

存储：`Imsg.e5`；起点：`0x6B5F8` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x70738`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 旧 HexTable.xml 明确 Enable=false；Imsg 6.5 基底长度不足，且区域与物品说明/撤退区重叠。未取得消费代码前禁止读取或写回。
- 旧 HexTable.xml 的 Enable=false；6.5 文件边界不足，6.6 旧区域与宝物说明/撤退区域冲突且未确认消费引用，禁止读取或写入。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | False | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `物品获取说明` | `0x0` | 200 | `fixed-string` | 物品获取说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 物品获取说明（104-199）（item-acquisition-high 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-acquisition-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x70738 + (ID - 104) * 0xC8 + field_offset; ID=104..199`

存储：`Imsg.e5`；起点：`0x70738` (fileOffset)；记录数：`96`；ID 起点：`104`；结束偏移（不含）：`0x75238`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 旧 HexTable.xml 明确 Enable=false；高段区域与低段获取说明/撤退区存在重叠语义，未取得消费代码前禁止读取或写回。
- 旧 HexTable.xml 的 Enable=false；6.5 文件边界不足，6.6 旧区域与宝物说明/撤退区域冲突且未确认消费引用，禁止读取或写入。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 450000 | False | `ECE53215506167C5E53F0A39092392813BBB30D5F06337A393B73D9DD3FA3545` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `物品获取说明` | `0x0` | 200 | `fixed-string` | 物品获取说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 宝物扩展（256-511）（items-extended 物理表）

ID: `struct.66.disk.66-legacy-data-v1.items-extended`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `Item.e5 + 0x0 + (ID - 256) * 0x19 + field_offset; ID=256..511`

存储：`Item.e5`；起点：`0x0` (fileOffset)；记录数：`256`；ID 起点：`256`；结束偏移（不含）：`0x1900`。

能力：`Editable`；Codec：`item-65-17-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 17 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；引用 effect-names；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `图标` | `0x14` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x14 UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-legacy-data-v1 宝物扩展说明（256-511）（item-description-extended 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-description-extended`；状态: `canonical`；证据: `source-reviewed`

步长: `0xC8` (200)

索引公式: `Itemmsg.e5 + 0x0 + (ID - 256) * 0xC8 + field_offset; ID=256..511`

存储：`Itemmsg.e5`；起点：`0x0` (fileOffset)；记录数：`256`；ID 起点：`256`；结束偏移（不含）：`0xC800`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 装备特效名称池（6.6，1A-FF）（item-effect-names-66 物理表）

ID: `struct.66.disk.66-legacy-data-v1.item-effect-names-66`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0x9D9A0 + (ID - 26) * 0x10 + field_offset; ID=26..255`

存储：`Ekd5.exe`；起点：`0x9D9A0` (fileOffset)；记录数：`230`；ID 起点：`26`；结束偏移（不含）：`0x9E800`。

能力：`ReadOnly`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 固定 16 字节名称池，专用名称池服务负责解析/写入，物理页只读。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 厚黑6.6 | 1130496 | True | `A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 16 | `fixed-string` | 名称；字段策略 ReadOnly；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-legacy-data-v1 特殊暴击人物分配（动态物理表）

ID: `struct.66.disk.66-legacy-data-v1.person-critical-special-map`；状态: `canonical`；证据: `source-reviewed-pe-reference-gated`

步长: `0x4` (4)

索引公式: `Ekd5.exe + 0x89C30 + specialSlot * 4; specialSlot=0..20; Imsg.e5 quoteOffset=140000 + specialSlot*200`

存储：`Ekd5.exe`；起点：`0x89C30` (fileOffset)；记录数：`21`；ID 起点：`0`；结束偏移（不含）：`0x89C84`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`not applicable`。

写入门禁：

- 需验证目标 PE 可执行区对该区域的引用、21 个 UInt32 值和文件边界；不能只检查原始固定偏移。
- 普通模式清空此人物所有特殊槽到 1024，再写普通类型 0..25 和三句共享台词。
- 特殊模式保持普通类型作为回退；绑定所选槽并清除本人物其它特殊槽；被其它人物占用时先预览并显式覆盖。
- 模式、绑定、人物字段和 Imsg 文本一次跨表事务提交；任何校验失败不产生部分草稿。

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `人物ID` | `0x0` | 4 | `uint32le` | 绑定人物 ID 0..1023，1024 为空槽；数值不是 Imsg 行号，记录主键 ID/槽号才对应特殊台词行。 |

## 66-shanzhai-legacy 人物（persons 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.persons`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x20` (32)

索引公式: `Data.e5 + 0x18C + (ID - 0) * 0x20 + field_offset; ID=0..1023`

存储：`Data.e5`；起点：`0x18C` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x818C`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 13 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `头像` | `0xD` | 2 | `uint16le` | 头像；字段策略 Editable |
| `撤退台词` | `0xF` | 1 | `uint8` | 撤退台词；字段策略 Editable |
| `暴击台词` | `0x10` | 1 | `uint8` | 暴击台词；字段策略 Editable |
| `Army` | `0x11` | 1 | `uint8` | Army；字段策略 Editable |
| `武力` | `0x12` | 1 | `uint8` | 武力；字段策略 Editable |
| `统帅` | `0x13` | 1 | `uint8` | 统帅；字段策略 Editable |
| `智力` | `0x14` | 1 | `uint8` | 智力；字段策略 Editable |
| `敏捷` | `0x15` | 1 | `uint8` | 敏捷；字段策略 Editable |
| `士气` | `0x16` | 1 | `uint8` | 士气；字段策略 Editable |
| `初始HP` | `0x17` | 2 | `uint16le` | 初始HP；字段策略 Editable |
| `初始MP` | `0x19` | 1 | `uint8` | 初始MP；字段策略 Editable |
| `兵种` | `0x1A` | 1 | `uint8` | 兵种；字段策略 Editable；引用 detailed-jobs |
| `级别` | `0x1B` | 1 | `uint8` | 级别；字段策略 Preserve |
| `经验` | `0x1C` | 1 | `uint8` | 经验；字段策略 Preserve |
| `默认武器` | `0x1D` | 1 | `uint8` | 默认武器；字段策略 Editable；引用 items |
| `默认防具` | `0x1E` | 1 | `uint8` | 默认防具；字段策略 Editable；引用 items |
| `默认辅助` | `0x1F` | 1 | `uint8` | 默认辅助；字段策略 Editable；引用 items |

## 66-shanzhai-legacy 人物列传（person-biography 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.person-biography`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x2D050 + (ID - 0) * 0xC8 + field_offset; ID=0..1023`

存储：`Imsg.e5`；起点：`0x2D050` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x5F050`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `人物列传` | `0x0` | 200 | `fixed-string` | 人物列传；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 宝物（0-103）（items-low 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.items-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x19` (25)

索引公式: `Data.e5 + 0x818C + (ID - 0) * 0x19 + field_offset; ID=0..103`

存储：`Data.e5`；起点：`0x818C` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x8BB4`。

能力：`Editable`；Codec：`item-66-15-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 15 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `图标` | `0xF` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x0F UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `保留10` | `0x10` | 1 | `bytes` | 保留10；字段策略 Preserve |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `保留14` | `0x14` | 1 | `bytes` | 保留14；字段策略 Preserve |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-shanzhai-legacy 宝物（104-254）（items-high 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.items-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x19` (25)

索引公式: `Star.e5 + 0x0 + (ID - 104) * 0x19 + field_offset; ID=104..254`

存储：`Star.e5`；起点：`0x0` (fileOffset)；记录数：`151`；ID 起点：`104`；结束偏移（不含）：`0xEBF`。

能力：`Editable`；Codec：`item-66-15-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 15 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `图标` | `0xF` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x0F UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `保留10` | `0x10` | 1 | `bytes` | 保留10；字段策略 Preserve |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `保留14` | `0x14` | 1 | `bytes` | 保留14；字段策略 Preserve |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-shanzhai-legacy 宝物说明（0-103）（item-description-low 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-description-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x5F050 + (ID - 0) * 0xC8 + field_offset; ID=0..103`

存储：`Imsg.e5`；起点：`0x5F050` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x64190`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 宝物说明（104-254）（item-description-high 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-description-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x64190 + (ID - 104) * 0xC8 + field_offset; ID=104..254`

存储：`Imsg.e5`；起点：`0x64190` (fileOffset)；记录数：`151`；ID 起点：`104`；结束偏移（不含）：`0x6B788`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 兵种系（job-series 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.job-series`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x9` (9)

索引公式: `Ekd5.exe + 0x8B010 + (ID - 0) * 0x9 + field_offset; ID=0..39`

存储：`Ekd5.exe`；起点：`0x8B010` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0x8B178`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 9 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 兵种系·地形发挥（job-series-terrain 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.job-series-terrain`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x3C` (60)

索引公式: `Data.e5 + 0xA8A4 + (ID - 0) * 0x3C + field_offset; ID=0..39`

存储：`Data.e5`；起点：`0xA8A4` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xB204`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `平原` | `0x0` | 1 | `uint8` | 平原；字段策略 Editable |
| `草原` | `0x1` | 1 | `uint8` | 草原；字段策略 Editable |
| `树林` | `0x2` | 1 | `uint8` | 树林；字段策略 Editable |
| `荒地` | `0x3` | 1 | `uint8` | 荒地；字段策略 Editable |
| `山地` | `0x4` | 1 | `uint8` | 山地；字段策略 Editable |
| `岩山` | `0x5` | 1 | `uint8` | 岩山；字段策略 Editable |
| `山崖` | `0x6` | 1 | `uint8` | 山崖；字段策略 Editable |
| `雪原` | `0x7` | 1 | `uint8` | 雪原；字段策略 Editable |
| `桥梁` | `0x8` | 1 | `uint8` | 桥梁；字段策略 Editable |
| `浅滩` | `0x9` | 1 | `uint8` | 浅滩；字段策略 Editable |
| `沼泽` | `0xA` | 1 | `uint8` | 沼泽；字段策略 Editable |
| `池塘` | `0xB` | 1 | `uint8` | 池塘；字段策略 Editable |
| `小河` | `0xC` | 1 | `uint8` | 小河；字段策略 Editable |
| `大河` | `0xD` | 1 | `uint8` | 大河；字段策略 Editable |
| `栅栏` | `0xE` | 1 | `uint8` | 栅栏；字段策略 Editable |
| `城墙` | `0xF` | 1 | `uint8` | 城墙；字段策略 Editable |
| `城内` | `0x10` | 1 | `uint8` | 城内；字段策略 Editable |
| `城门` | `0x11` | 1 | `uint8` | 城门；字段策略 Editable |
| `城池` | `0x12` | 1 | `uint8` | 城池；字段策略 Editable |
| `关隘` | `0x13` | 1 | `uint8` | 关隘；字段策略 Editable |
| `鹿砦` | `0x14` | 1 | `uint8` | 鹿砦；字段策略 Editable |
| `村庄` | `0x15` | 1 | `uint8` | 村庄；字段策略 Editable |
| `兵营` | `0x16` | 1 | `uint8` | 兵营；字段策略 Editable |
| `民居` | `0x17` | 1 | `uint8` | 民居；字段策略 Editable |
| `宝物库` | `0x18` | 1 | `uint8` | 宝物库；字段策略 Editable |
| `水池` | `0x19` | 1 | `uint8` | 水池；字段策略 Editable |
| `火` | `0x1A` | 1 | `uint8` | 火；字段策略 Editable |
| `船` | `0x1B` | 1 | `uint8` | 船；字段策略 Editable |
| `祭坛` | `0x1C` | 1 | `uint8` | 祭坛；字段策略 Editable |
| `地下` | `0x1D` | 1 | `uint8` | 地下；字段策略 Editable |

## 66-shanzhai-legacy 兵种系·移动消耗（job-series-move-cost 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.job-series-move-cost`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x3C` (60)

索引公式: `Data.e5 + 0xA8C2 + (ID - 0) * 0x3C + field_offset; ID=0..39`

存储：`Data.e5`；起点：`0xA8C2` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xB222`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `平原` | `0x0` | 1 | `uint8` | 平原；字段策略 Editable |
| `草原` | `0x1` | 1 | `uint8` | 草原；字段策略 Editable |
| `树林` | `0x2` | 1 | `uint8` | 树林；字段策略 Editable |
| `荒地` | `0x3` | 1 | `uint8` | 荒地；字段策略 Editable |
| `山地` | `0x4` | 1 | `uint8` | 山地；字段策略 Editable |
| `岩山` | `0x5` | 1 | `uint8` | 岩山；字段策略 Editable |
| `山崖` | `0x6` | 1 | `uint8` | 山崖；字段策略 Editable |
| `雪原` | `0x7` | 1 | `uint8` | 雪原；字段策略 Editable |
| `桥梁` | `0x8` | 1 | `uint8` | 桥梁；字段策略 Editable |
| `浅滩` | `0x9` | 1 | `uint8` | 浅滩；字段策略 Editable |
| `沼泽` | `0xA` | 1 | `uint8` | 沼泽；字段策略 Editable |
| `池塘` | `0xB` | 1 | `uint8` | 池塘；字段策略 Editable |
| `小河` | `0xC` | 1 | `uint8` | 小河；字段策略 Editable |
| `大河` | `0xD` | 1 | `uint8` | 大河；字段策略 Editable |
| `栅栏` | `0xE` | 1 | `uint8` | 栅栏；字段策略 Editable |
| `城墙` | `0xF` | 1 | `uint8` | 城墙；字段策略 Editable |
| `城内` | `0x10` | 1 | `uint8` | 城内；字段策略 Editable |
| `城门` | `0x11` | 1 | `uint8` | 城门；字段策略 Editable |
| `城池` | `0x12` | 1 | `uint8` | 城池；字段策略 Editable |
| `关隘` | `0x13` | 1 | `uint8` | 关隘；字段策略 Editable |
| `鹿砦` | `0x14` | 1 | `uint8` | 鹿砦；字段策略 Editable |
| `村庄` | `0x15` | 1 | `uint8` | 村庄；字段策略 Editable |
| `兵营` | `0x16` | 1 | `uint8` | 兵营；字段策略 Editable |
| `民居` | `0x17` | 1 | `uint8` | 民居；字段策略 Editable |
| `宝物库` | `0x18` | 1 | `uint8` | 宝物库；字段策略 Editable |
| `水池` | `0x19` | 1 | `uint8` | 水池；字段策略 Editable |
| `火` | `0x1A` | 1 | `uint8` | 火；字段策略 Editable |
| `船` | `0x1B` | 1 | `uint8` | 船；字段策略 Editable |
| `祭坛` | `0x1C` | 1 | `uint8` | 祭坛；字段策略 Editable |
| `地下` | `0x1D` | 1 | `uint8` | 地下；字段策略 Editable |

## 66-shanzhai-legacy 兵种系·兵种相克（job-series-counter 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.job-series-counter`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x28` (40)

索引公式: `Ekd5.exe + 0xA3280 + (ID - 0) * 0x28 + field_offset; ID=0..39`

存储：`Ekd5.exe`；起点：`0xA3280` (fileOffset)；记录数：`40`；ID 起点：`0`；结束偏移（不含）：`0xA38C0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `对兵种系 0` | `0x0` | 1 | `uint8` | 对兵种系 0；字段策略 Editable |
| `对兵种系 1` | `0x1` | 1 | `uint8` | 对兵种系 1；字段策略 Editable |
| `对兵种系 2` | `0x2` | 1 | `uint8` | 对兵种系 2；字段策略 Editable |
| `对兵种系 3` | `0x3` | 1 | `uint8` | 对兵种系 3；字段策略 Editable |
| `对兵种系 4` | `0x4` | 1 | `uint8` | 对兵种系 4；字段策略 Editable |
| `对兵种系 5` | `0x5` | 1 | `uint8` | 对兵种系 5；字段策略 Editable |
| `对兵种系 6` | `0x6` | 1 | `uint8` | 对兵种系 6；字段策略 Editable |
| `对兵种系 7` | `0x7` | 1 | `uint8` | 对兵种系 7；字段策略 Editable |
| `对兵种系 8` | `0x8` | 1 | `uint8` | 对兵种系 8；字段策略 Editable |
| `对兵种系 9` | `0x9` | 1 | `uint8` | 对兵种系 9；字段策略 Editable |
| `对兵种系 10` | `0xA` | 1 | `uint8` | 对兵种系 10；字段策略 Editable |
| `对兵种系 11` | `0xB` | 1 | `uint8` | 对兵种系 11；字段策略 Editable |
| `对兵种系 12` | `0xC` | 1 | `uint8` | 对兵种系 12；字段策略 Editable |
| `对兵种系 13` | `0xD` | 1 | `uint8` | 对兵种系 13；字段策略 Editable |
| `对兵种系 14` | `0xE` | 1 | `uint8` | 对兵种系 14；字段策略 Editable |
| `对兵种系 15` | `0xF` | 1 | `uint8` | 对兵种系 15；字段策略 Editable |
| `对兵种系 16` | `0x10` | 1 | `uint8` | 对兵种系 16；字段策略 Editable |
| `对兵种系 17` | `0x11` | 1 | `uint8` | 对兵种系 17；字段策略 Editable |
| `对兵种系 18` | `0x12` | 1 | `uint8` | 对兵种系 18；字段策略 Editable |
| `对兵种系 19` | `0x13` | 1 | `uint8` | 对兵种系 19；字段策略 Editable |
| `对兵种系 20` | `0x14` | 1 | `uint8` | 对兵种系 20；字段策略 Editable |
| `对兵种系 21` | `0x15` | 1 | `uint8` | 对兵种系 21；字段策略 Editable |
| `对兵种系 22` | `0x16` | 1 | `uint8` | 对兵种系 22；字段策略 Editable |
| `对兵种系 23` | `0x17` | 1 | `uint8` | 对兵种系 23；字段策略 Editable |
| `对兵种系 24` | `0x18` | 1 | `uint8` | 对兵种系 24；字段策略 Editable |
| `对兵种系 25` | `0x19` | 1 | `uint8` | 对兵种系 25；字段策略 Editable |
| `对兵种系 26` | `0x1A` | 1 | `uint8` | 对兵种系 26；字段策略 Editable |
| `对兵种系 27` | `0x1B` | 1 | `uint8` | 对兵种系 27；字段策略 Editable |
| `对兵种系 28` | `0x1C` | 1 | `uint8` | 对兵种系 28；字段策略 Editable |
| `对兵种系 29` | `0x1D` | 1 | `uint8` | 对兵种系 29；字段策略 Editable |
| `对兵种系 30` | `0x1E` | 1 | `uint8` | 对兵种系 30；字段策略 Editable |
| `对兵种系 31` | `0x1F` | 1 | `uint8` | 对兵种系 31；字段策略 Editable |
| `对兵种系 32` | `0x20` | 1 | `uint8` | 对兵种系 32；字段策略 Editable |
| `对兵种系 33` | `0x21` | 1 | `uint8` | 对兵种系 33；字段策略 Editable |
| `对兵种系 34` | `0x22` | 1 | `uint8` | 对兵种系 34；字段策略 Editable |
| `对兵种系 35` | `0x23` | 1 | `uint8` | 对兵种系 35；字段策略 Editable |
| `对兵种系 36` | `0x24` | 1 | `uint8` | 对兵种系 36；字段策略 Editable |
| `对兵种系 37` | `0x25` | 1 | `uint8` | 对兵种系 37；字段策略 Editable |
| `对兵种系 38` | `0x26` | 1 | `uint8` | 对兵种系 38；字段策略 Editable |
| `对兵种系 39` | `0x27` | 1 | `uint8` | 对兵种系 39；字段策略 Editable |

## 66-shanzhai-legacy 兵种系·兵种属性（job-series-attributes 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.job-series-attributes`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x28` (40)

索引公式: `Ekd5.exe + 0xA38C0 + (ID - 0) * 0x28 + field_offset; ID=0..7`

存储：`Ekd5.exe`；起点：`0xA38C0` (fileOffset)；记录数：`8`；ID 起点：`0`；结束偏移（不含）：`0xA3A00`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 行号和 UInt8 几何来自读取器与 Profile；移动声音、移动速度、攻击声音、兵种类型的枚举名称由用户确认，未冒充逆向或引擎运行时验证。未列出的数值保留数字并允许按字段边界编辑。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 属性行 ID | 名称 | 值语义 | 语义来源 |
|---:|---|---|---|
| 0 | 移动声音 | 0：马蹄；1：车轮；2：脚步；3：无声；4：引擎；5：预设1；6：预设2 | `user-confirmed-semantics` |
| 1 | 移动速度 | 0：快速；1：慢速 | `user-confirmed-semantics` |
| 2 | 攻击声音 | 0：剑；1：其他；2：爆炸1；3：爆炸2；4：火箭筒；5：枪声（连射）；6：枪声（点射）；7：火焰喷射；8：毒气喷射 | `user-confirmed-semantics` |
| 3 | 远程兵种 | 未在此确认 | `source-reviewed-row-label` |
| 4 | 攻击延迟 | 未在此确认 | `source-reviewed-row-label` |
| 5 | 兵种类型 | 0：全能；1：文官；2：武将 | `user-confirmed-semantics` |
| 6 | 策略伤害 | 未在此确认 | `source-reviewed-row-label` |
| 7 | 参与围攻 | 未在此确认 | `source-reviewed-row-label` |

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `兵种系 0` | `0x0` | 1 | `uint8` | 兵种系 0；字段策略 Editable |
| `兵种系 1` | `0x1` | 1 | `uint8` | 兵种系 1；字段策略 Editable |
| `兵种系 2` | `0x2` | 1 | `uint8` | 兵种系 2；字段策略 Editable |
| `兵种系 3` | `0x3` | 1 | `uint8` | 兵种系 3；字段策略 Editable |
| `兵种系 4` | `0x4` | 1 | `uint8` | 兵种系 4；字段策略 Editable |
| `兵种系 5` | `0x5` | 1 | `uint8` | 兵种系 5；字段策略 Editable |
| `兵种系 6` | `0x6` | 1 | `uint8` | 兵种系 6；字段策略 Editable |
| `兵种系 7` | `0x7` | 1 | `uint8` | 兵种系 7；字段策略 Editable |
| `兵种系 8` | `0x8` | 1 | `uint8` | 兵种系 8；字段策略 Editable |
| `兵种系 9` | `0x9` | 1 | `uint8` | 兵种系 9；字段策略 Editable |
| `兵种系 10` | `0xA` | 1 | `uint8` | 兵种系 10；字段策略 Editable |
| `兵种系 11` | `0xB` | 1 | `uint8` | 兵种系 11；字段策略 Editable |
| `兵种系 12` | `0xC` | 1 | `uint8` | 兵种系 12；字段策略 Editable |
| `兵种系 13` | `0xD` | 1 | `uint8` | 兵种系 13；字段策略 Editable |
| `兵种系 14` | `0xE` | 1 | `uint8` | 兵种系 14；字段策略 Editable |
| `兵种系 15` | `0xF` | 1 | `uint8` | 兵种系 15；字段策略 Editable |
| `兵种系 16` | `0x10` | 1 | `uint8` | 兵种系 16；字段策略 Editable |
| `兵种系 17` | `0x11` | 1 | `uint8` | 兵种系 17；字段策略 Editable |
| `兵种系 18` | `0x12` | 1 | `uint8` | 兵种系 18；字段策略 Editable |
| `兵种系 19` | `0x13` | 1 | `uint8` | 兵种系 19；字段策略 Editable |
| `兵种系 20` | `0x14` | 1 | `uint8` | 兵种系 20；字段策略 Editable |
| `兵种系 21` | `0x15` | 1 | `uint8` | 兵种系 21；字段策略 Editable |
| `兵种系 22` | `0x16` | 1 | `uint8` | 兵种系 22；字段策略 Editable |
| `兵种系 23` | `0x17` | 1 | `uint8` | 兵种系 23；字段策略 Editable |
| `兵种系 24` | `0x18` | 1 | `uint8` | 兵种系 24；字段策略 Editable |
| `兵种系 25` | `0x19` | 1 | `uint8` | 兵种系 25；字段策略 Editable |
| `兵种系 26` | `0x1A` | 1 | `uint8` | 兵种系 26；字段策略 Editable |
| `兵种系 27` | `0x1B` | 1 | `uint8` | 兵种系 27；字段策略 Editable |
| `兵种系 28` | `0x1C` | 1 | `uint8` | 兵种系 28；字段策略 Editable |
| `兵种系 29` | `0x1D` | 1 | `uint8` | 兵种系 29；字段策略 Editable |
| `兵种系 30` | `0x1E` | 1 | `uint8` | 兵种系 30；字段策略 Editable |
| `兵种系 31` | `0x1F` | 1 | `uint8` | 兵种系 31；字段策略 Editable |
| `兵种系 32` | `0x20` | 1 | `uint8` | 兵种系 32；字段策略 Editable |
| `兵种系 33` | `0x21` | 1 | `uint8` | 兵种系 33；字段策略 Editable |
| `兵种系 34` | `0x22` | 1 | `uint8` | 兵种系 34；字段策略 Editable |
| `兵种系 35` | `0x23` | 1 | `uint8` | 兵种系 35；字段策略 Editable |
| `兵种系 36` | `0x24` | 1 | `uint8` | 兵种系 36；字段策略 Editable |
| `兵种系 37` | `0x25` | 1 | `uint8` | 兵种系 37；字段策略 Editable |
| `兵种系 38` | `0x26` | 1 | `uint8` | 兵种系 38；字段策略 Editable |
| `兵种系 39` | `0x27` | 1 | `uint8` | 兵种系 39；字段策略 Editable |

## 66-shanzhai-legacy 兵种（detailed-jobs 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.detailed-jobs`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x9` (9)

索引公式: `Ekd5.exe + 0xD18D0 + (ID - 0) * 0x9 + field_offset; ID=0..79`

存储：`Ekd5.exe`；起点：`0xD18D0` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0xD1BA0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 9 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 兵种说明（detailed-job-description 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.detailed-job-description`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x11170 + (ID - 0) * 0xC8 + field_offset; ID=0..79`

存储：`Imsg.e5`；起点：`0x11170` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0x14FF0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `兵种说明` | `0x0` | 200 | `fixed-string` | 兵种说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 兵种成长与装备（detailed-job-growth 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.detailed-job-growth`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x23` (35)

索引公式: `Data.e5 + 0x9DB4 + (ID - 0) * 0x23 + field_offset; ID=0..79`

存储：`Data.e5`；起点：`0x9DB4` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0xA8A4`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `移动力成长` | `0x0` | 1 | `uint8` | 移动力成长；字段策略 Editable |
| `攻击范围` | `0x1` | 1 | `uint8` | 攻击范围；字段策略 Editable |
| `攻击成长` | `0x2` | 1 | `uint8` | 攻击成长；字段策略 Editable |
| `防御成长` | `0x3` | 1 | `uint8` | 防御成长；字段策略 Editable |
| `精神成长` | `0x4` | 1 | `uint8` | 精神成长；字段策略 Editable |
| `爆发成长` | `0x5` | 1 | `uint8` | 爆发成长；字段策略 Editable |
| `士气成长` | `0x6` | 1 | `uint8` | 士气成长；字段策略 Editable |
| `HP成长` | `0x7` | 1 | `uint8` | HP成长；字段策略 Editable |
| `MP成长` | `0x8` | 1 | `uint8` | MP成长；字段策略 Editable |
| `普通剑` | `0x9` | 1 | `uint8` | 普通剑；字段策略 Editable |
| `特殊剑` | `0xA` | 1 | `uint8` | 特殊剑；字段策略 Editable |
| `普通枪` | `0xB` | 1 | `uint8` | 普通枪；字段策略 Editable |
| `特殊枪` | `0xC` | 1 | `uint8` | 特殊枪；字段策略 Editable |
| `普通弓` | `0xD` | 1 | `uint8` | 普通弓；字段策略 Editable |
| `特殊弓` | `0xE` | 1 | `uint8` | 特殊弓；字段策略 Editable |
| `普通刀` | `0xF` | 1 | `uint8` | 普通刀；字段策略 Editable |
| `特殊刀` | `0x10` | 1 | `uint8` | 特殊刀；字段策略 Editable |
| `普通炮车` | `0x11` | 1 | `uint8` | 普通炮车；字段策略 Editable |
| `特殊炮车` | `0x12` | 1 | `uint8` | 特殊炮车；字段策略 Editable |
| `普通锤` | `0x13` | 1 | `uint8` | 普通锤；字段策略 Editable |
| `特殊锤` | `0x14` | 1 | `uint8` | 特殊锤；字段策略 Editable |
| `普通斧` | `0x15` | 1 | `uint8` | 普通斧；字段策略 Editable |
| `特殊斧` | `0x16` | 1 | `uint8` | 特殊斧；字段策略 Editable |
| `普通扇` | `0x17` | 1 | `uint8` | 普通扇；字段策略 Editable |
| `特殊扇` | `0x18` | 1 | `uint8` | 特殊扇；字段策略 Editable |
| `普通宝剑` | `0x19` | 1 | `uint8` | 普通宝剑；字段策略 Editable |
| `特殊宝剑` | `0x1A` | 1 | `uint8` | 特殊宝剑；字段策略 Editable |
| `普通将剑` | `0x1B` | 1 | `uint8` | 普通将剑；字段策略 Editable |
| `特殊将剑` | `0x1C` | 1 | `uint8` | 特殊将剑；字段策略 Editable |
| `普通铠甲` | `0x1D` | 1 | `uint8` | 普通铠甲；字段策略 Editable |
| `特殊铠甲` | `0x1E` | 1 | `uint8` | 特殊铠甲；字段策略 Editable |
| `普通衣服` | `0x1F` | 1 | `uint8` | 普通衣服；字段策略 Editable |
| `特殊衣服` | `0x20` | 1 | `uint8` | 特殊衣服；字段策略 Editable |
| `普通袍服` | `0x21` | 1 | `uint8` | 普通袍服；字段策略 Editable |
| `特殊袍服` | `0x22` | 1 | `uint8` | 特殊袍服；字段策略 Editable |

## 66-shanzhai-legacy 兵种穿透（detailed-job-penetration 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.detailed-job-penetration`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0x6C81 + (ID - 0) * 0x1 + field_offset; ID=0..79`

存储：`Ekd5.exe`；起点：`0x6C81` (fileOffset)；记录数：`80`；ID 起点：`0`；结束偏移（不含）：`0x6CD1`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `穿透` | `0x0` | 1 | `uint8` | 穿透；字段策略 Editable |

## 66-shanzhai-legacy 策略（strategies 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategies`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x61` (97)

索引公式: `Data.e5 + 0xB204 + (ID - 0) * 0x61 + field_offset; ID=0..143`

存储：`Data.e5`；起点：`0xB204` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xE894`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 11 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `策略类型` | `0xB` | 1 | `uint8` | 策略类型；字段策略 Editable |
| `施展对象` | `0xC` | 1 | `uint8` | 施展对象；字段策略 Editable |
| `施法范围` | `0xD` | 1 | `uint8` | 施法范围；字段策略 Editable |
| `穿透范围` | `0xE` | 1 | `uint8` | 穿透范围；字段策略 Editable |
| `策略消耗` | `0xF` | 1 | `uint8` | 策略消耗；字段策略 Editable |
| `策略图标` | `0x10` | 1 | `uint8` | 策略图标；字段策略 Editable |
| `兵种00学习等级` | `0x11` | 1 | `uint8` | 兵种00学习等级；字段策略 Editable |
| `兵种01学习等级` | `0x12` | 1 | `uint8` | 兵种01学习等级；字段策略 Editable |
| `兵种02学习等级` | `0x13` | 1 | `uint8` | 兵种02学习等级；字段策略 Editable |
| `兵种03学习等级` | `0x14` | 1 | `uint8` | 兵种03学习等级；字段策略 Editable |
| `兵种04学习等级` | `0x15` | 1 | `uint8` | 兵种04学习等级；字段策略 Editable |
| `兵种05学习等级` | `0x16` | 1 | `uint8` | 兵种05学习等级；字段策略 Editable |
| `兵种06学习等级` | `0x17` | 1 | `uint8` | 兵种06学习等级；字段策略 Editable |
| `兵种07学习等级` | `0x18` | 1 | `uint8` | 兵种07学习等级；字段策略 Editable |
| `兵种08学习等级` | `0x19` | 1 | `uint8` | 兵种08学习等级；字段策略 Editable |
| `兵种09学习等级` | `0x1A` | 1 | `uint8` | 兵种09学习等级；字段策略 Editable |
| `兵种10学习等级` | `0x1B` | 1 | `uint8` | 兵种10学习等级；字段策略 Editable |
| `兵种11学习等级` | `0x1C` | 1 | `uint8` | 兵种11学习等级；字段策略 Editable |
| `兵种12学习等级` | `0x1D` | 1 | `uint8` | 兵种12学习等级；字段策略 Editable |
| `兵种13学习等级` | `0x1E` | 1 | `uint8` | 兵种13学习等级；字段策略 Editable |
| `兵种14学习等级` | `0x1F` | 1 | `uint8` | 兵种14学习等级；字段策略 Editable |
| `兵种15学习等级` | `0x20` | 1 | `uint8` | 兵种15学习等级；字段策略 Editable |
| `兵种16学习等级` | `0x21` | 1 | `uint8` | 兵种16学习等级；字段策略 Editable |
| `兵种17学习等级` | `0x22` | 1 | `uint8` | 兵种17学习等级；字段策略 Editable |
| `兵种18学习等级` | `0x23` | 1 | `uint8` | 兵种18学习等级；字段策略 Editable |
| `兵种19学习等级` | `0x24` | 1 | `uint8` | 兵种19学习等级；字段策略 Editable |
| `兵种20学习等级` | `0x25` | 1 | `uint8` | 兵种20学习等级；字段策略 Editable |
| `兵种21学习等级` | `0x26` | 1 | `uint8` | 兵种21学习等级；字段策略 Editable |
| `兵种22学习等级` | `0x27` | 1 | `uint8` | 兵种22学习等级；字段策略 Editable |
| `兵种23学习等级` | `0x28` | 1 | `uint8` | 兵种23学习等级；字段策略 Editable |
| `兵种24学习等级` | `0x29` | 1 | `uint8` | 兵种24学习等级；字段策略 Editable |
| `兵种25学习等级` | `0x2A` | 1 | `uint8` | 兵种25学习等级；字段策略 Editable |
| `兵种26学习等级` | `0x2B` | 1 | `uint8` | 兵种26学习等级；字段策略 Editable |
| `兵种27学习等级` | `0x2C` | 1 | `uint8` | 兵种27学习等级；字段策略 Editable |
| `兵种28学习等级` | `0x2D` | 1 | `uint8` | 兵种28学习等级；字段策略 Editable |
| `兵种29学习等级` | `0x2E` | 1 | `uint8` | 兵种29学习等级；字段策略 Editable |
| `兵种30学习等级` | `0x2F` | 1 | `uint8` | 兵种30学习等级；字段策略 Editable |
| `兵种31学习等级` | `0x30` | 1 | `uint8` | 兵种31学习等级；字段策略 Editable |
| `兵种32学习等级` | `0x31` | 1 | `uint8` | 兵种32学习等级；字段策略 Editable |
| `兵种33学习等级` | `0x32` | 1 | `uint8` | 兵种33学习等级；字段策略 Editable |
| `兵种34学习等级` | `0x33` | 1 | `uint8` | 兵种34学习等级；字段策略 Editable |
| `兵种35学习等级` | `0x34` | 1 | `uint8` | 兵种35学习等级；字段策略 Editable |
| `兵种36学习等级` | `0x35` | 1 | `uint8` | 兵种36学习等级；字段策略 Editable |
| `兵种37学习等级` | `0x36` | 1 | `uint8` | 兵种37学习等级；字段策略 Editable |
| `兵种38学习等级` | `0x37` | 1 | `uint8` | 兵种38学习等级；字段策略 Editable |
| `兵种39学习等级` | `0x38` | 1 | `uint8` | 兵种39学习等级；字段策略 Editable |
| `兵种40学习等级` | `0x39` | 1 | `uint8` | 兵种40学习等级；字段策略 Editable |
| `兵种41学习等级` | `0x3A` | 1 | `uint8` | 兵种41学习等级；字段策略 Editable |
| `兵种42学习等级` | `0x3B` | 1 | `uint8` | 兵种42学习等级；字段策略 Editable |
| `兵种43学习等级` | `0x3C` | 1 | `uint8` | 兵种43学习等级；字段策略 Editable |
| `兵种44学习等级` | `0x3D` | 1 | `uint8` | 兵种44学习等级；字段策略 Editable |
| `兵种45学习等级` | `0x3E` | 1 | `uint8` | 兵种45学习等级；字段策略 Editable |
| `兵种46学习等级` | `0x3F` | 1 | `uint8` | 兵种46学习等级；字段策略 Editable |
| `兵种47学习等级` | `0x40` | 1 | `uint8` | 兵种47学习等级；字段策略 Editable |
| `兵种48学习等级` | `0x41` | 1 | `uint8` | 兵种48学习等级；字段策略 Editable |
| `兵种49学习等级` | `0x42` | 1 | `uint8` | 兵种49学习等级；字段策略 Editable |
| `兵种50学习等级` | `0x43` | 1 | `uint8` | 兵种50学习等级；字段策略 Editable |
| `兵种51学习等级` | `0x44` | 1 | `uint8` | 兵种51学习等级；字段策略 Editable |
| `兵种52学习等级` | `0x45` | 1 | `uint8` | 兵种52学习等级；字段策略 Editable |
| `兵种53学习等级` | `0x46` | 1 | `uint8` | 兵种53学习等级；字段策略 Editable |
| `兵种54学习等级` | `0x47` | 1 | `uint8` | 兵种54学习等级；字段策略 Editable |
| `兵种55学习等级` | `0x48` | 1 | `uint8` | 兵种55学习等级；字段策略 Editable |
| `兵种56学习等级` | `0x49` | 1 | `uint8` | 兵种56学习等级；字段策略 Editable |
| `兵种57学习等级` | `0x4A` | 1 | `uint8` | 兵种57学习等级；字段策略 Editable |
| `兵种58学习等级` | `0x4B` | 1 | `uint8` | 兵种58学习等级；字段策略 Editable |
| `兵种59学习等级` | `0x4C` | 1 | `uint8` | 兵种59学习等级；字段策略 Editable |
| `兵种60学习等级` | `0x4D` | 1 | `uint8` | 兵种60学习等级；字段策略 Editable |
| `兵种61学习等级` | `0x4E` | 1 | `uint8` | 兵种61学习等级；字段策略 Editable |
| `兵种62学习等级` | `0x4F` | 1 | `uint8` | 兵种62学习等级；字段策略 Editable |
| `兵种63学习等级` | `0x50` | 1 | `uint8` | 兵种63学习等级；字段策略 Editable |
| `兵种64学习等级` | `0x51` | 1 | `uint8` | 兵种64学习等级；字段策略 Editable |
| `兵种65学习等级` | `0x52` | 1 | `uint8` | 兵种65学习等级；字段策略 Editable |
| `兵种66学习等级` | `0x53` | 1 | `uint8` | 兵种66学习等级；字段策略 Editable |
| `兵种67学习等级` | `0x54` | 1 | `uint8` | 兵种67学习等级；字段策略 Editable |
| `兵种68学习等级` | `0x55` | 1 | `uint8` | 兵种68学习等级；字段策略 Editable |
| `兵种69学习等级` | `0x56` | 1 | `uint8` | 兵种69学习等级；字段策略 Editable |
| `兵种70学习等级` | `0x57` | 1 | `uint8` | 兵种70学习等级；字段策略 Editable |
| `兵种71学习等级` | `0x58` | 1 | `uint8` | 兵种71学习等级；字段策略 Editable |
| `兵种72学习等级` | `0x59` | 1 | `uint8` | 兵种72学习等级；字段策略 Editable |
| `兵种73学习等级` | `0x5A` | 1 | `uint8` | 兵种73学习等级；字段策略 Editable |
| `兵种74学习等级` | `0x5B` | 1 | `uint8` | 兵种74学习等级；字段策略 Editable |
| `兵种75学习等级` | `0x5C` | 1 | `uint8` | 兵种75学习等级；字段策略 Editable |
| `兵种76学习等级` | `0x5D` | 1 | `uint8` | 兵种76学习等级；字段策略 Editable |
| `兵种77学习等级` | `0x5E` | 1 | `uint8` | 兵种77学习等级；字段策略 Editable |
| `兵种78学习等级` | `0x5F` | 1 | `uint8` | 兵种78学习等级；字段策略 Editable |
| `兵种79学习等级` | `0x60` | 1 | `uint8` | 兵种79学习等级；字段策略 Editable |

## 66-shanzhai-legacy 策略说明（strategy-description 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-description`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x0 + (ID - 0) * 0xC8 + field_offset; ID=0..143`

存储：`Imsg.e5`；起点：`0x0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0x7080`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略说明` | `0x0` | 200 | `fixed-string` | 策略说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 策略扩展标记（strategy-extension 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-extension`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2CE0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2CE0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2D70`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-shanzhai-legacy 策略伤害类型（strategy-damage-type 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-damage-type`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA30D0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA30D0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3160`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-shanzhai-legacy 策略伤害系数（strategy-damage-ratio 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-damage-ratio`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA3040 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA3040` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA30D0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-shanzhai-legacy 策略命中率（strategy-hit-rate 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-hit-rate`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2F20 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2F20` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2FB0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-shanzhai-legacy 效果索引（strategy-learning 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-learning`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2FB0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2FB0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3040`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-shanzhai-legacy 战场AI策略限制（strategy-battle-ai 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-battle-ai`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2E00 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2E00` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2E90`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-shanzhai-legacy 练武场AI策略限制（strategy-training-ai 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-training-ai`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA2E90 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA2E90` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA2F20`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `内容` | `0x0` | 1 | `uint8` | 内容；字段策略 Editable |

## 66-shanzhai-legacy 兵种特效分配（class-effects 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.class-effects`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0xD9000 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0xD9000` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0xD9FF0`。

能力：`Editable`；Codec：`effect-66-16-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `武将1` | `0x0` | 2 | `uint16le` | 武将1；字段策略 Editable；引用 persons |
| `武将1特效值` | `0x2` | 1 | `uint8` | 武将1特效值；字段策略 Editable |
| `武将2` | `0x3` | 2 | `uint16le` | 武将2；字段策略 Editable；引用 persons |
| `武将2特效值` | `0x5` | 1 | `uint8` | 武将2特效值；字段策略 Editable |
| `武将3` | `0x6` | 2 | `uint16le` | 武将3；字段策略 Editable；引用 persons |
| `武将3特效值` | `0x8` | 1 | `uint8` | 武将3特效值；字段策略 Editable |
| `武将4` | `0x9` | 2 | `uint16le` | 武将4；字段策略 Editable；引用 persons |
| `武将4特效值` | `0xB` | 1 | `uint8` | 武将4特效值；字段策略 Editable |
| `兵种1` | `0xC` | 1 | `uint8` | 兵种1；字段策略 Editable；引用 detailed-jobs |
| `兵种1特效值` | `0xD` | 1 | `uint8` | 兵种1特效值；字段策略 Editable |
| `兵种2` | `0xE` | 1 | `uint8` | 兵种2；字段策略 Editable；引用 detailed-jobs |
| `兵种2特效值` | `0xF` | 1 | `uint8` | 兵种2特效值；字段策略 Editable |

## 66-shanzhai-legacy 人物专属、套装专属（personal-effects 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.personal-effects`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0xDF800 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0xDF800` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0xE07F0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `武将1` | `0x0` | 2 | `uint16le` | 武将1；字段策略 Editable；引用 persons |
| `装备1` | `0x2` | 1 | `uint8` | 装备1；字段策略 Editable；引用 items |
| `特效值1` | `0x3` | 1 | `uint8` | 特效值1；字段策略 Editable |
| `武将2` | `0x4` | 2 | `uint16le` | 武将2；字段策略 Editable；引用 persons |
| `装备2` | `0x6` | 1 | `uint8` | 装备2；字段策略 Editable；引用 items |
| `特效值2` | `0x7` | 1 | `uint8` | 特效值2；字段策略 Editable |
| `装备3-1` | `0x8` | 1 | `uint8` | 装备3-1；字段策略 Editable；引用 items |
| `装备3-2` | `0x9` | 1 | `uint8` | 装备3-2；字段策略 Editable；引用 items |
| `装备3-3` | `0xA` | 1 | `uint8` | 装备3-3；字段策略 Editable；引用 items |
| `特效值3` | `0xB` | 1 | `uint8` | 特效值3；字段策略 Editable |
| `装备4-1` | `0xC` | 1 | `uint8` | 装备4-1；字段策略 Editable；引用 items |
| `装备4-2` | `0xD` | 1 | `uint8` | 装备4-2；字段策略 Editable；引用 items |
| `装备4-3` | `0xE` | 1 | `uint8` | 装备4-3；字段策略 Editable；引用 items |
| `特效值4` | `0xF` | 1 | `uint8` | 特效值4；字段策略 Editable |

## 66-shanzhai-legacy 人物暴击台词（person-critical-quotes 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.person-critical-quotes`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x222E0 + (ID - 0) * 0xC8 + field_offset; ID=0..98`

存储：`Imsg.e5`；起点：`0x222E0` (fileOffset)；记录数：`99`；ID 起点：`0`；结束偏移（不含）：`0x27038`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `台词` | `0x0` | 200 | `fixed-string` | 台词；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 人物撤退台词（person-retreat-quotes 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.person-retreat-quotes`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x78050 + (ID - 0) * 0xC8 + field_offset; ID=0..48`

存储：`Imsg.e5`；起点：`0x78050` (fileOffset)；记录数：`49`；ID 起点：`0`；结束偏移（不含）：`0x7A698`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 只使用 +491600 的 49×200 区；+440200 仅用于旧区冲突诊断。450000 字节 Imsg 样本不满足边界，必须 unavailable。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `台词` | `0x0` | 200 | `fixed-string` | 台词；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 人物R形象指定（person-r-assign 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.person-r-assign`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x2` (2)

索引公式: `Ekd5.exe + 0xE1000 + (ID - 0) * 0x2 + field_offset; ID=0..1023`

存储：`Ekd5.exe`；起点：`0xE1000` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0xE1800`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `R形象ID` | `0x0` | 2 | `uint16le` | R形象ID；字段策略 Editable |

## 66-shanzhai-legacy 人物S形象指定（person-s-assign 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.person-s-assign`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x2` (2)

索引公式: `Ekd5.exe + 0xD2800 + (ID - 0) * 0x2 + field_offset; ID=0..1023`

存储：`Ekd5.exe`；起点：`0xD2800` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0xD3000`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `S形象ID` | `0x0` | 2 | `uint16le` | S形象ID；字段策略 Editable |

## 66-shanzhai-legacy 战役名称（scenario-names 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.scenario-names`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0xC350 + (ID - 0) * 0xC8 + field_offset; ID=0..98`

存储：`Imsg.e5`；起点：`0xC350` (fileOffset)；记录数：`99`；ID 起点：`0`；结束偏移（不含）：`0x110A8`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `战役名称` | `0x0` | 200 | `fixed-string` | 战役名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 商店数据（shops 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.shops`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x24` (36)

索引公式: `Data.e5 + 0x8BB4 + (ID - 0) * 0x24 + field_offset; ID=0..127`

存储：`Data.e5`；起点：`0x8BB4` (fileOffset)；记录数：`128`；ID 起点：`0`；结束偏移（不含）：`0x9DB4`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `开关仓库人物` | `0x0` | 2 | `uint16le` | 开关仓库人物；字段策略 Editable；引用 persons |
| `买卖物品人物` | `0x2` | 2 | `uint16le` | 买卖物品人物；字段策略 Editable；引用 persons |
| `装备0` | `0x4` | 1 | `uint8` | 装备0；字段策略 Editable；引用 items |
| `装备1` | `0x5` | 1 | `uint8` | 装备1；字段策略 Editable；引用 items |
| `装备2` | `0x6` | 1 | `uint8` | 装备2；字段策略 Editable；引用 items |
| `装备3` | `0x7` | 1 | `uint8` | 装备3；字段策略 Editable；引用 items |
| `装备4` | `0x8` | 1 | `uint8` | 装备4；字段策略 Editable；引用 items |
| `装备5` | `0x9` | 1 | `uint8` | 装备5；字段策略 Editable；引用 items |
| `装备6` | `0xA` | 1 | `uint8` | 装备6；字段策略 Editable；引用 items |
| `装备7` | `0xB` | 1 | `uint8` | 装备7；字段策略 Editable；引用 items |
| `装备8` | `0xC` | 1 | `uint8` | 装备8；字段策略 Editable；引用 items |
| `装备9` | `0xD` | 1 | `uint8` | 装备9；字段策略 Editable；引用 items |
| `装备10` | `0xE` | 1 | `uint8` | 装备10；字段策略 Editable；引用 items |
| `装备11` | `0xF` | 1 | `uint8` | 装备11；字段策略 Editable；引用 items |
| `装备12` | `0x10` | 1 | `uint8` | 装备12；字段策略 Editable；引用 items |
| `装备13` | `0x11` | 1 | `uint8` | 装备13；字段策略 Editable；引用 items |
| `装备14` | `0x12` | 1 | `uint8` | 装备14；字段策略 Editable；引用 items |
| `装备15` | `0x13` | 1 | `uint8` | 装备15；字段策略 Editable；引用 items |
| `物品0` | `0x14` | 1 | `uint8` | 物品0；字段策略 Editable；引用 items |
| `物品1` | `0x15` | 1 | `uint8` | 物品1；字段策略 Editable；引用 items |
| `物品2` | `0x16` | 1 | `uint8` | 物品2；字段策略 Editable；引用 items |
| `物品3` | `0x17` | 1 | `uint8` | 物品3；字段策略 Editable；引用 items |
| `物品4` | `0x18` | 1 | `uint8` | 物品4；字段策略 Editable；引用 items |
| `物品5` | `0x19` | 1 | `uint8` | 物品5；字段策略 Editable；引用 items |
| `物品6` | `0x1A` | 1 | `uint8` | 物品6；字段策略 Editable；引用 items |
| `物品7` | `0x1B` | 1 | `uint8` | 物品7；字段策略 Editable；引用 items |
| `物品8` | `0x1C` | 1 | `uint8` | 物品8；字段策略 Editable；引用 items |
| `物品9` | `0x1D` | 1 | `uint8` | 物品9；字段策略 Editable；引用 items |
| `物品10` | `0x1E` | 1 | `uint8` | 物品10；字段策略 Editable；引用 items |
| `物品11` | `0x1F` | 1 | `uint8` | 物品11；字段策略 Editable；引用 items |
| `物品12` | `0x20` | 1 | `uint8` | 物品12；字段策略 Editable；引用 items |
| `物品13` | `0x21` | 1 | `uint8` | 物品13；字段策略 Editable；引用 items |
| `物品14` | `0x22` | 1 | `uint8` | 物品14；字段策略 Editable；引用 items |
| `物品15` | `0x23` | 1 | `uint8` | 物品15；字段策略 Editable；引用 items |

## 66-shanzhai-legacy 兵种特效名称（effect-names 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.effect-names`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0x9E800 + (ID - 0) * 0x10 + field_offset; ID=0..254`

存储：`Ekd5.exe`；起点：`0x9E800` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x9F7F0`。

能力：`ReadOnly`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.5 兵种特效名称原始名称区，行尾可能含额外参数；使用专用名称池解析，物理表只读。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 16 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 兵种特效说明（effect-descriptions 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.effect-descriptions`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x14FF0 + (ID - 0) * 0xC8 + field_offset; ID=0..254`

存储：`Imsg.e5`；起点：`0x14FF0` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x21728`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `说明` | `0x0` | 200 | `fixed-string` | 说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 人物特效拓展（effect-archive 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.effect-archive`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x400` (1024)

索引公式: `Effect.e5 + 0x0 + (ID - 0) * 0x400 + field_offset; ID=0..1023`

存储：`Effect.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x100000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `槽0特效号` | `0x0` | 1 | `uint8` | 槽0特效号；字段策略 Editable |
| `槽1特效号` | `0x4` | 1 | `uint8` | 槽1特效号；字段策略 Editable |
| `槽2特效号` | `0x8` | 1 | `uint8` | 槽2特效号；字段策略 Editable |
| `槽3特效号` | `0xC` | 1 | `uint8` | 槽3特效号；字段策略 Editable |
| `槽4特效号` | `0x10` | 1 | `uint8` | 槽4特效号；字段策略 Editable |
| `槽5特效号` | `0x14` | 1 | `uint8` | 槽5特效号；字段策略 Editable |
| `槽6特效号` | `0x18` | 1 | `uint8` | 槽6特效号；字段策略 Editable |
| `槽7特效号` | `0x1C` | 1 | `uint8` | 槽7特效号；字段策略 Editable |
| `槽8特效号` | `0x20` | 1 | `uint8` | 槽8特效号；字段策略 Editable |
| `槽9特效号` | `0x24` | 1 | `uint8` | 槽9特效号；字段策略 Editable |
| `槽10特效号` | `0x28` | 1 | `uint8` | 槽10特效号；字段策略 Editable |
| `槽11特效号` | `0x2C` | 1 | `uint8` | 槽11特效号；字段策略 Editable |
| `槽12特效号` | `0x30` | 1 | `uint8` | 槽12特效号；字段策略 Editable |
| `槽13特效号` | `0x34` | 1 | `uint8` | 槽13特效号；字段策略 Editable |
| `槽14特效号` | `0x38` | 1 | `uint8` | 槽14特效号；字段策略 Editable |
| `槽15特效号` | `0x3C` | 1 | `uint8` | 槽15特效号；字段策略 Editable |
| `槽16特效号` | `0x40` | 1 | `uint8` | 槽16特效号；字段策略 Editable |
| `槽17特效号` | `0x44` | 1 | `uint8` | 槽17特效号；字段策略 Editable |
| `槽18特效号` | `0x48` | 1 | `uint8` | 槽18特效号；字段策略 Editable |
| `槽19特效号` | `0x4C` | 1 | `uint8` | 槽19特效号；字段策略 Editable |
| `槽20特效号` | `0x50` | 1 | `uint8` | 槽20特效号；字段策略 Editable |
| `槽21特效号` | `0x54` | 1 | `uint8` | 槽21特效号；字段策略 Editable |
| `槽22特效号` | `0x58` | 1 | `uint8` | 槽22特效号；字段策略 Editable |
| `槽23特效号` | `0x5C` | 1 | `uint8` | 槽23特效号；字段策略 Editable |
| `槽24特效号` | `0x60` | 1 | `uint8` | 槽24特效号；字段策略 Editable |
| `槽25特效号` | `0x64` | 1 | `uint8` | 槽25特效号；字段策略 Editable |
| `槽26特效号` | `0x68` | 1 | `uint8` | 槽26特效号；字段策略 Editable |
| `槽27特效号` | `0x6C` | 1 | `uint8` | 槽27特效号；字段策略 Editable |
| `槽28特效号` | `0x70` | 1 | `uint8` | 槽28特效号；字段策略 Editable |
| `槽29特效号` | `0x74` | 1 | `uint8` | 槽29特效号；字段策略 Editable |
| `槽30特效号` | `0x78` | 1 | `uint8` | 槽30特效号；字段策略 Editable |
| `槽31特效号` | `0x7C` | 1 | `uint8` | 槽31特效号；字段策略 Editable |
| `槽32特效号` | `0x80` | 1 | `uint8` | 槽32特效号；字段策略 Editable |
| `槽33特效号` | `0x84` | 1 | `uint8` | 槽33特效号；字段策略 Editable |
| `槽34特效号` | `0x88` | 1 | `uint8` | 槽34特效号；字段策略 Editable |
| `槽35特效号` | `0x8C` | 1 | `uint8` | 槽35特效号；字段策略 Editable |
| `槽36特效号` | `0x90` | 1 | `uint8` | 槽36特效号；字段策略 Editable |
| `槽37特效号` | `0x94` | 1 | `uint8` | 槽37特效号；字段策略 Editable |
| `槽38特效号` | `0x98` | 1 | `uint8` | 槽38特效号；字段策略 Editable |
| `槽39特效号` | `0x9C` | 1 | `uint8` | 槽39特效号；字段策略 Editable |
| `槽40特效号` | `0xA0` | 1 | `uint8` | 槽40特效号；字段策略 Editable |
| `槽41特效号` | `0xA4` | 1 | `uint8` | 槽41特效号；字段策略 Editable |
| `槽42特效号` | `0xA8` | 1 | `uint8` | 槽42特效号；字段策略 Editable |
| `槽43特效号` | `0xAC` | 1 | `uint8` | 槽43特效号；字段策略 Editable |
| `槽44特效号` | `0xB0` | 1 | `uint8` | 槽44特效号；字段策略 Editable |
| `槽45特效号` | `0xB4` | 1 | `uint8` | 槽45特效号；字段策略 Editable |
| `槽46特效号` | `0xB8` | 1 | `uint8` | 槽46特效号；字段策略 Editable |
| `槽47特效号` | `0xBC` | 1 | `uint8` | 槽47特效号；字段策略 Editable |
| `槽48特效号` | `0xC0` | 1 | `uint8` | 槽48特效号；字段策略 Editable |
| `槽49特效号` | `0xC4` | 1 | `uint8` | 槽49特效号；字段策略 Editable |
| `槽50特效号` | `0xC8` | 1 | `uint8` | 槽50特效号；字段策略 Editable |
| `槽51特效号` | `0xCC` | 1 | `uint8` | 槽51特效号；字段策略 Editable |
| `槽52特效号` | `0xD0` | 1 | `uint8` | 槽52特效号；字段策略 Editable |
| `槽53特效号` | `0xD4` | 1 | `uint8` | 槽53特效号；字段策略 Editable |
| `槽54特效号` | `0xD8` | 1 | `uint8` | 槽54特效号；字段策略 Editable |
| `槽55特效号` | `0xDC` | 1 | `uint8` | 槽55特效号；字段策略 Editable |
| `槽56特效号` | `0xE0` | 1 | `uint8` | 槽56特效号；字段策略 Editable |
| `槽57特效号` | `0xE4` | 1 | `uint8` | 槽57特效号；字段策略 Editable |
| `槽58特效号` | `0xE8` | 1 | `uint8` | 槽58特效号；字段策略 Editable |
| `槽59特效号` | `0xEC` | 1 | `uint8` | 槽59特效号；字段策略 Editable |
| `槽60特效号` | `0xF0` | 1 | `uint8` | 槽60特效号；字段策略 Editable |
| `槽61特效号` | `0xF4` | 1 | `uint8` | 槽61特效号；字段策略 Editable |
| `槽62特效号` | `0xF8` | 1 | `uint8` | 槽62特效号；字段策略 Editable |
| `槽63特效号` | `0xFC` | 1 | `uint8` | 槽63特效号；字段策略 Editable |
| `槽64特效号` | `0x100` | 1 | `uint8` | 槽64特效号；字段策略 Editable |
| `槽65特效号` | `0x104` | 1 | `uint8` | 槽65特效号；字段策略 Editable |
| `槽66特效号` | `0x108` | 1 | `uint8` | 槽66特效号；字段策略 Editable |
| `槽67特效号` | `0x10C` | 1 | `uint8` | 槽67特效号；字段策略 Editable |
| `槽68特效号` | `0x110` | 1 | `uint8` | 槽68特效号；字段策略 Editable |
| `槽69特效号` | `0x114` | 1 | `uint8` | 槽69特效号；字段策略 Editable |
| `槽70特效号` | `0x118` | 1 | `uint8` | 槽70特效号；字段策略 Editable |
| `槽71特效号` | `0x11C` | 1 | `uint8` | 槽71特效号；字段策略 Editable |
| `槽72特效号` | `0x120` | 1 | `uint8` | 槽72特效号；字段策略 Editable |
| `槽73特效号` | `0x124` | 1 | `uint8` | 槽73特效号；字段策略 Editable |
| `槽74特效号` | `0x128` | 1 | `uint8` | 槽74特效号；字段策略 Editable |
| `槽75特效号` | `0x12C` | 1 | `uint8` | 槽75特效号；字段策略 Editable |
| `槽76特效号` | `0x130` | 1 | `uint8` | 槽76特效号；字段策略 Editable |
| `槽77特效号` | `0x134` | 1 | `uint8` | 槽77特效号；字段策略 Editable |
| `槽78特效号` | `0x138` | 1 | `uint8` | 槽78特效号；字段策略 Editable |
| `槽79特效号` | `0x13C` | 1 | `uint8` | 槽79特效号；字段策略 Editable |
| `槽80特效号` | `0x140` | 1 | `uint8` | 槽80特效号；字段策略 Editable |
| `槽81特效号` | `0x144` | 1 | `uint8` | 槽81特效号；字段策略 Editable |
| `槽82特效号` | `0x148` | 1 | `uint8` | 槽82特效号；字段策略 Editable |
| `槽83特效号` | `0x14C` | 1 | `uint8` | 槽83特效号；字段策略 Editable |
| `槽84特效号` | `0x150` | 1 | `uint8` | 槽84特效号；字段策略 Editable |
| `槽85特效号` | `0x154` | 1 | `uint8` | 槽85特效号；字段策略 Editable |
| `槽86特效号` | `0x158` | 1 | `uint8` | 槽86特效号；字段策略 Editable |
| `槽87特效号` | `0x15C` | 1 | `uint8` | 槽87特效号；字段策略 Editable |
| `槽88特效号` | `0x160` | 1 | `uint8` | 槽88特效号；字段策略 Editable |
| `槽89特效号` | `0x164` | 1 | `uint8` | 槽89特效号；字段策略 Editable |
| `槽90特效号` | `0x168` | 1 | `uint8` | 槽90特效号；字段策略 Editable |
| `槽91特效号` | `0x16C` | 1 | `uint8` | 槽91特效号；字段策略 Editable |
| `槽92特效号` | `0x170` | 1 | `uint8` | 槽92特效号；字段策略 Editable |
| `槽93特效号` | `0x174` | 1 | `uint8` | 槽93特效号；字段策略 Editable |
| `槽94特效号` | `0x178` | 1 | `uint8` | 槽94特效号；字段策略 Editable |
| `槽95特效号` | `0x17C` | 1 | `uint8` | 槽95特效号；字段策略 Editable |
| `槽96特效号` | `0x180` | 1 | `uint8` | 槽96特效号；字段策略 Editable |
| `槽97特效号` | `0x184` | 1 | `uint8` | 槽97特效号；字段策略 Editable |
| `槽98特效号` | `0x188` | 1 | `uint8` | 槽98特效号；字段策略 Editable |
| `槽99特效号` | `0x18C` | 1 | `uint8` | 槽99特效号；字段策略 Editable |
| `槽100特效号` | `0x190` | 1 | `uint8` | 槽100特效号；字段策略 Editable |
| `槽101特效号` | `0x194` | 1 | `uint8` | 槽101特效号；字段策略 Editable |
| `槽102特效号` | `0x198` | 1 | `uint8` | 槽102特效号；字段策略 Editable |
| `槽103特效号` | `0x19C` | 1 | `uint8` | 槽103特效号；字段策略 Editable |
| `槽104特效号` | `0x1A0` | 1 | `uint8` | 槽104特效号；字段策略 Editable |
| `槽105特效号` | `0x1A4` | 1 | `uint8` | 槽105特效号；字段策略 Editable |
| `槽106特效号` | `0x1A8` | 1 | `uint8` | 槽106特效号；字段策略 Editable |
| `槽107特效号` | `0x1AC` | 1 | `uint8` | 槽107特效号；字段策略 Editable |
| `槽108特效号` | `0x1B0` | 1 | `uint8` | 槽108特效号；字段策略 Editable |
| `槽109特效号` | `0x1B4` | 1 | `uint8` | 槽109特效号；字段策略 Editable |
| `槽110特效号` | `0x1B8` | 1 | `uint8` | 槽110特效号；字段策略 Editable |
| `槽111特效号` | `0x1BC` | 1 | `uint8` | 槽111特效号；字段策略 Editable |
| `槽112特效号` | `0x1C0` | 1 | `uint8` | 槽112特效号；字段策略 Editable |
| `槽113特效号` | `0x1C4` | 1 | `uint8` | 槽113特效号；字段策略 Editable |
| `槽114特效号` | `0x1C8` | 1 | `uint8` | 槽114特效号；字段策略 Editable |
| `槽115特效号` | `0x1CC` | 1 | `uint8` | 槽115特效号；字段策略 Editable |
| `槽116特效号` | `0x1D0` | 1 | `uint8` | 槽116特效号；字段策略 Editable |
| `槽117特效号` | `0x1D4` | 1 | `uint8` | 槽117特效号；字段策略 Editable |
| `槽118特效号` | `0x1D8` | 1 | `uint8` | 槽118特效号；字段策略 Editable |
| `槽119特效号` | `0x1DC` | 1 | `uint8` | 槽119特效号；字段策略 Editable |
| `槽120特效号` | `0x1E0` | 1 | `uint8` | 槽120特效号；字段策略 Editable |
| `槽121特效号` | `0x1E4` | 1 | `uint8` | 槽121特效号；字段策略 Editable |
| `槽122特效号` | `0x1E8` | 1 | `uint8` | 槽122特效号；字段策略 Editable |
| `槽123特效号` | `0x1EC` | 1 | `uint8` | 槽123特效号；字段策略 Editable |
| `槽124特效号` | `0x1F0` | 1 | `uint8` | 槽124特效号；字段策略 Editable |
| `槽125特效号` | `0x1F4` | 1 | `uint8` | 槽125特效号；字段策略 Editable |
| `槽126特效号` | `0x1F8` | 1 | `uint8` | 槽126特效号；字段策略 Editable |
| `槽127特效号` | `0x1FC` | 1 | `uint8` | 槽127特效号；字段策略 Editable |
| `槽128特效号` | `0x200` | 1 | `uint8` | 槽128特效号；字段策略 Editable |
| `槽129特效号` | `0x204` | 1 | `uint8` | 槽129特效号；字段策略 Editable |
| `槽130特效号` | `0x208` | 1 | `uint8` | 槽130特效号；字段策略 Editable |
| `槽131特效号` | `0x20C` | 1 | `uint8` | 槽131特效号；字段策略 Editable |
| `槽132特效号` | `0x210` | 1 | `uint8` | 槽132特效号；字段策略 Editable |
| `槽133特效号` | `0x214` | 1 | `uint8` | 槽133特效号；字段策略 Editable |
| `槽134特效号` | `0x218` | 1 | `uint8` | 槽134特效号；字段策略 Editable |
| `槽135特效号` | `0x21C` | 1 | `uint8` | 槽135特效号；字段策略 Editable |
| `槽136特效号` | `0x220` | 1 | `uint8` | 槽136特效号；字段策略 Editable |
| `槽137特效号` | `0x224` | 1 | `uint8` | 槽137特效号；字段策略 Editable |
| `槽138特效号` | `0x228` | 1 | `uint8` | 槽138特效号；字段策略 Editable |
| `槽139特效号` | `0x22C` | 1 | `uint8` | 槽139特效号；字段策略 Editable |
| `槽140特效号` | `0x230` | 1 | `uint8` | 槽140特效号；字段策略 Editable |
| `槽141特效号` | `0x234` | 1 | `uint8` | 槽141特效号；字段策略 Editable |
| `槽142特效号` | `0x238` | 1 | `uint8` | 槽142特效号；字段策略 Editable |
| `槽143特效号` | `0x23C` | 1 | `uint8` | 槽143特效号；字段策略 Editable |
| `槽144特效号` | `0x240` | 1 | `uint8` | 槽144特效号；字段策略 Editable |
| `槽145特效号` | `0x244` | 1 | `uint8` | 槽145特效号；字段策略 Editable |
| `槽146特效号` | `0x248` | 1 | `uint8` | 槽146特效号；字段策略 Editable |
| `槽147特效号` | `0x24C` | 1 | `uint8` | 槽147特效号；字段策略 Editable |
| `槽148特效号` | `0x250` | 1 | `uint8` | 槽148特效号；字段策略 Editable |
| `槽149特效号` | `0x254` | 1 | `uint8` | 槽149特效号；字段策略 Editable |
| `槽150特效号` | `0x258` | 1 | `uint8` | 槽150特效号；字段策略 Editable |
| `槽151特效号` | `0x25C` | 1 | `uint8` | 槽151特效号；字段策略 Editable |
| `槽152特效号` | `0x260` | 1 | `uint8` | 槽152特效号；字段策略 Editable |
| `槽153特效号` | `0x264` | 1 | `uint8` | 槽153特效号；字段策略 Editable |
| `槽154特效号` | `0x268` | 1 | `uint8` | 槽154特效号；字段策略 Editable |
| `槽155特效号` | `0x26C` | 1 | `uint8` | 槽155特效号；字段策略 Editable |
| `槽156特效号` | `0x270` | 1 | `uint8` | 槽156特效号；字段策略 Editable |
| `槽157特效号` | `0x274` | 1 | `uint8` | 槽157特效号；字段策略 Editable |
| `槽158特效号` | `0x278` | 1 | `uint8` | 槽158特效号；字段策略 Editable |
| `槽159特效号` | `0x27C` | 1 | `uint8` | 槽159特效号；字段策略 Editable |
| `槽160特效号` | `0x280` | 1 | `uint8` | 槽160特效号；字段策略 Editable |
| `槽161特效号` | `0x284` | 1 | `uint8` | 槽161特效号；字段策略 Editable |
| `槽162特效号` | `0x288` | 1 | `uint8` | 槽162特效号；字段策略 Editable |
| `槽163特效号` | `0x28C` | 1 | `uint8` | 槽163特效号；字段策略 Editable |
| `槽164特效号` | `0x290` | 1 | `uint8` | 槽164特效号；字段策略 Editable |
| `槽165特效号` | `0x294` | 1 | `uint8` | 槽165特效号；字段策略 Editable |
| `槽166特效号` | `0x298` | 1 | `uint8` | 槽166特效号；字段策略 Editable |
| `槽167特效号` | `0x29C` | 1 | `uint8` | 槽167特效号；字段策略 Editable |
| `槽168特效号` | `0x2A0` | 1 | `uint8` | 槽168特效号；字段策略 Editable |
| `槽169特效号` | `0x2A4` | 1 | `uint8` | 槽169特效号；字段策略 Editable |
| `槽170特效号` | `0x2A8` | 1 | `uint8` | 槽170特效号；字段策略 Editable |
| `槽171特效号` | `0x2AC` | 1 | `uint8` | 槽171特效号；字段策略 Editable |
| `槽172特效号` | `0x2B0` | 1 | `uint8` | 槽172特效号；字段策略 Editable |
| `槽173特效号` | `0x2B4` | 1 | `uint8` | 槽173特效号；字段策略 Editable |
| `槽174特效号` | `0x2B8` | 1 | `uint8` | 槽174特效号；字段策略 Editable |
| `槽175特效号` | `0x2BC` | 1 | `uint8` | 槽175特效号；字段策略 Editable |
| `槽176特效号` | `0x2C0` | 1 | `uint8` | 槽176特效号；字段策略 Editable |
| `槽177特效号` | `0x2C4` | 1 | `uint8` | 槽177特效号；字段策略 Editable |
| `槽178特效号` | `0x2C8` | 1 | `uint8` | 槽178特效号；字段策略 Editable |
| `槽179特效号` | `0x2CC` | 1 | `uint8` | 槽179特效号；字段策略 Editable |
| `槽180特效号` | `0x2D0` | 1 | `uint8` | 槽180特效号；字段策略 Editable |
| `槽181特效号` | `0x2D4` | 1 | `uint8` | 槽181特效号；字段策略 Editable |
| `槽182特效号` | `0x2D8` | 1 | `uint8` | 槽182特效号；字段策略 Editable |
| `槽183特效号` | `0x2DC` | 1 | `uint8` | 槽183特效号；字段策略 Editable |
| `槽184特效号` | `0x2E0` | 1 | `uint8` | 槽184特效号；字段策略 Editable |
| `槽185特效号` | `0x2E4` | 1 | `uint8` | 槽185特效号；字段策略 Editable |
| `槽186特效号` | `0x2E8` | 1 | `uint8` | 槽186特效号；字段策略 Editable |
| `槽187特效号` | `0x2EC` | 1 | `uint8` | 槽187特效号；字段策略 Editable |
| `槽188特效号` | `0x2F0` | 1 | `uint8` | 槽188特效号；字段策略 Editable |
| `槽189特效号` | `0x2F4` | 1 | `uint8` | 槽189特效号；字段策略 Editable |
| `槽190特效号` | `0x2F8` | 1 | `uint8` | 槽190特效号；字段策略 Editable |
| `槽191特效号` | `0x2FC` | 1 | `uint8` | 槽191特效号；字段策略 Editable |
| `槽192特效号` | `0x300` | 1 | `uint8` | 槽192特效号；字段策略 Editable |
| `槽193特效号` | `0x304` | 1 | `uint8` | 槽193特效号；字段策略 Editable |
| `槽194特效号` | `0x308` | 1 | `uint8` | 槽194特效号；字段策略 Editable |
| `槽195特效号` | `0x30C` | 1 | `uint8` | 槽195特效号；字段策略 Editable |
| `槽196特效号` | `0x310` | 1 | `uint8` | 槽196特效号；字段策略 Editable |
| `槽197特效号` | `0x314` | 1 | `uint8` | 槽197特效号；字段策略 Editable |
| `槽198特效号` | `0x318` | 1 | `uint8` | 槽198特效号；字段策略 Editable |
| `槽199特效号` | `0x31C` | 1 | `uint8` | 槽199特效号；字段策略 Editable |
| `槽200特效号` | `0x320` | 1 | `uint8` | 槽200特效号；字段策略 Editable |
| `槽201特效号` | `0x324` | 1 | `uint8` | 槽201特效号；字段策略 Editable |
| `槽202特效号` | `0x328` | 1 | `uint8` | 槽202特效号；字段策略 Editable |
| `槽203特效号` | `0x32C` | 1 | `uint8` | 槽203特效号；字段策略 Editable |
| `槽204特效号` | `0x330` | 1 | `uint8` | 槽204特效号；字段策略 Editable |
| `槽205特效号` | `0x334` | 1 | `uint8` | 槽205特效号；字段策略 Editable |
| `槽206特效号` | `0x338` | 1 | `uint8` | 槽206特效号；字段策略 Editable |
| `槽207特效号` | `0x33C` | 1 | `uint8` | 槽207特效号；字段策略 Editable |
| `槽208特效号` | `0x340` | 1 | `uint8` | 槽208特效号；字段策略 Editable |
| `槽209特效号` | `0x344` | 1 | `uint8` | 槽209特效号；字段策略 Editable |
| `槽210特效号` | `0x348` | 1 | `uint8` | 槽210特效号；字段策略 Editable |
| `槽211特效号` | `0x34C` | 1 | `uint8` | 槽211特效号；字段策略 Editable |
| `槽212特效号` | `0x350` | 1 | `uint8` | 槽212特效号；字段策略 Editable |
| `槽213特效号` | `0x354` | 1 | `uint8` | 槽213特效号；字段策略 Editable |
| `槽214特效号` | `0x358` | 1 | `uint8` | 槽214特效号；字段策略 Editable |
| `槽215特效号` | `0x35C` | 1 | `uint8` | 槽215特效号；字段策略 Editable |
| `槽216特效号` | `0x360` | 1 | `uint8` | 槽216特效号；字段策略 Editable |
| `槽217特效号` | `0x364` | 1 | `uint8` | 槽217特效号；字段策略 Editable |
| `槽218特效号` | `0x368` | 1 | `uint8` | 槽218特效号；字段策略 Editable |
| `槽219特效号` | `0x36C` | 1 | `uint8` | 槽219特效号；字段策略 Editable |
| `槽220特效号` | `0x370` | 1 | `uint8` | 槽220特效号；字段策略 Editable |
| `槽221特效号` | `0x374` | 1 | `uint8` | 槽221特效号；字段策略 Editable |
| `槽222特效号` | `0x378` | 1 | `uint8` | 槽222特效号；字段策略 Editable |
| `槽223特效号` | `0x37C` | 1 | `uint8` | 槽223特效号；字段策略 Editable |
| `槽224特效号` | `0x380` | 1 | `uint8` | 槽224特效号；字段策略 Editable |
| `槽225特效号` | `0x384` | 1 | `uint8` | 槽225特效号；字段策略 Editable |
| `槽226特效号` | `0x388` | 1 | `uint8` | 槽226特效号；字段策略 Editable |
| `槽227特效号` | `0x38C` | 1 | `uint8` | 槽227特效号；字段策略 Editable |
| `槽228特效号` | `0x390` | 1 | `uint8` | 槽228特效号；字段策略 Editable |
| `槽229特效号` | `0x394` | 1 | `uint8` | 槽229特效号；字段策略 Editable |
| `槽230特效号` | `0x398` | 1 | `uint8` | 槽230特效号；字段策略 Editable |
| `槽231特效号` | `0x39C` | 1 | `uint8` | 槽231特效号；字段策略 Editable |
| `槽232特效号` | `0x3A0` | 1 | `uint8` | 槽232特效号；字段策略 Editable |
| `槽233特效号` | `0x3A4` | 1 | `uint8` | 槽233特效号；字段策略 Editable |
| `槽234特效号` | `0x3A8` | 1 | `uint8` | 槽234特效号；字段策略 Editable |
| `槽235特效号` | `0x3AC` | 1 | `uint8` | 槽235特效号；字段策略 Editable |
| `槽236特效号` | `0x3B0` | 1 | `uint8` | 槽236特效号；字段策略 Editable |
| `槽237特效号` | `0x3B4` | 1 | `uint8` | 槽237特效号；字段策略 Editable |
| `槽238特效号` | `0x3B8` | 1 | `uint8` | 槽238特效号；字段策略 Editable |
| `槽239特效号` | `0x3BC` | 1 | `uint8` | 槽239特效号；字段策略 Editable |
| `槽240特效号` | `0x3C0` | 1 | `uint8` | 槽240特效号；字段策略 Editable |
| `槽241特效号` | `0x3C4` | 1 | `uint8` | 槽241特效号；字段策略 Editable |
| `槽242特效号` | `0x3C8` | 1 | `uint8` | 槽242特效号；字段策略 Editable |
| `槽243特效号` | `0x3CC` | 1 | `uint8` | 槽243特效号；字段策略 Editable |
| `槽244特效号` | `0x3D0` | 1 | `uint8` | 槽244特效号；字段策略 Editable |
| `槽245特效号` | `0x3D4` | 1 | `uint8` | 槽245特效号；字段策略 Editable |
| `槽246特效号` | `0x3D8` | 1 | `uint8` | 槽246特效号；字段策略 Editable |
| `槽247特效号` | `0x3DC` | 1 | `uint8` | 槽247特效号；字段策略 Editable |
| `槽248特效号` | `0x3E0` | 1 | `uint8` | 槽248特效号；字段策略 Editable |
| `槽249特效号` | `0x3E4` | 1 | `uint8` | 槽249特效号；字段策略 Editable |
| `槽250特效号` | `0x3E8` | 1 | `uint8` | 槽250特效号；字段策略 Editable |
| `槽251特效号` | `0x3EC` | 1 | `uint8` | 槽251特效号；字段策略 Editable |
| `槽252特效号` | `0x3F0` | 1 | `uint8` | 槽252特效号；字段策略 Editable |
| `槽253特效号` | `0x3F4` | 1 | `uint8` | 槽253特效号；字段策略 Editable |
| `槽254特效号` | `0x3F8` | 1 | `uint8` | 槽254特效号；字段策略 Editable |
| `槽255特效号` | `0x3FC` | 1 | `uint8` | 槽255特效号；字段策略 Editable |
| `槽0特效值` | `0x1` | 1 | `uint8` | 槽0特效值；字段策略 Editable |
| `槽1特效值` | `0x5` | 1 | `uint8` | 槽1特效值；字段策略 Editable |
| `槽2特效值` | `0x9` | 1 | `uint8` | 槽2特效值；字段策略 Editable |
| `槽3特效值` | `0xD` | 1 | `uint8` | 槽3特效值；字段策略 Editable |
| `槽4特效值` | `0x11` | 1 | `uint8` | 槽4特效值；字段策略 Editable |
| `槽5特效值` | `0x15` | 1 | `uint8` | 槽5特效值；字段策略 Editable |
| `槽6特效值` | `0x19` | 1 | `uint8` | 槽6特效值；字段策略 Editable |
| `槽7特效值` | `0x1D` | 1 | `uint8` | 槽7特效值；字段策略 Editable |
| `槽8特效值` | `0x21` | 1 | `uint8` | 槽8特效值；字段策略 Editable |
| `槽9特效值` | `0x25` | 1 | `uint8` | 槽9特效值；字段策略 Editable |
| `槽10特效值` | `0x29` | 1 | `uint8` | 槽10特效值；字段策略 Editable |
| `槽11特效值` | `0x2D` | 1 | `uint8` | 槽11特效值；字段策略 Editable |
| `槽12特效值` | `0x31` | 1 | `uint8` | 槽12特效值；字段策略 Editable |
| `槽13特效值` | `0x35` | 1 | `uint8` | 槽13特效值；字段策略 Editable |
| `槽14特效值` | `0x39` | 1 | `uint8` | 槽14特效值；字段策略 Editable |
| `槽15特效值` | `0x3D` | 1 | `uint8` | 槽15特效值；字段策略 Editable |
| `槽16特效值` | `0x41` | 1 | `uint8` | 槽16特效值；字段策略 Editable |
| `槽17特效值` | `0x45` | 1 | `uint8` | 槽17特效值；字段策略 Editable |
| `槽18特效值` | `0x49` | 1 | `uint8` | 槽18特效值；字段策略 Editable |
| `槽19特效值` | `0x4D` | 1 | `uint8` | 槽19特效值；字段策略 Editable |
| `槽20特效值` | `0x51` | 1 | `uint8` | 槽20特效值；字段策略 Editable |
| `槽21特效值` | `0x55` | 1 | `uint8` | 槽21特效值；字段策略 Editable |
| `槽22特效值` | `0x59` | 1 | `uint8` | 槽22特效值；字段策略 Editable |
| `槽23特效值` | `0x5D` | 1 | `uint8` | 槽23特效值；字段策略 Editable |
| `槽24特效值` | `0x61` | 1 | `uint8` | 槽24特效值；字段策略 Editable |
| `槽25特效值` | `0x65` | 1 | `uint8` | 槽25特效值；字段策略 Editable |
| `槽26特效值` | `0x69` | 1 | `uint8` | 槽26特效值；字段策略 Editable |
| `槽27特效值` | `0x6D` | 1 | `uint8` | 槽27特效值；字段策略 Editable |
| `槽28特效值` | `0x71` | 1 | `uint8` | 槽28特效值；字段策略 Editable |
| `槽29特效值` | `0x75` | 1 | `uint8` | 槽29特效值；字段策略 Editable |
| `槽30特效值` | `0x79` | 1 | `uint8` | 槽30特效值；字段策略 Editable |
| `槽31特效值` | `0x7D` | 1 | `uint8` | 槽31特效值；字段策略 Editable |
| `槽32特效值` | `0x81` | 1 | `uint8` | 槽32特效值；字段策略 Editable |
| `槽33特效值` | `0x85` | 1 | `uint8` | 槽33特效值；字段策略 Editable |
| `槽34特效值` | `0x89` | 1 | `uint8` | 槽34特效值；字段策略 Editable |
| `槽35特效值` | `0x8D` | 1 | `uint8` | 槽35特效值；字段策略 Editable |
| `槽36特效值` | `0x91` | 1 | `uint8` | 槽36特效值；字段策略 Editable |
| `槽37特效值` | `0x95` | 1 | `uint8` | 槽37特效值；字段策略 Editable |
| `槽38特效值` | `0x99` | 1 | `uint8` | 槽38特效值；字段策略 Editable |
| `槽39特效值` | `0x9D` | 1 | `uint8` | 槽39特效值；字段策略 Editable |
| `槽40特效值` | `0xA1` | 1 | `uint8` | 槽40特效值；字段策略 Editable |
| `槽41特效值` | `0xA5` | 1 | `uint8` | 槽41特效值；字段策略 Editable |
| `槽42特效值` | `0xA9` | 1 | `uint8` | 槽42特效值；字段策略 Editable |
| `槽43特效值` | `0xAD` | 1 | `uint8` | 槽43特效值；字段策略 Editable |
| `槽44特效值` | `0xB1` | 1 | `uint8` | 槽44特效值；字段策略 Editable |
| `槽45特效值` | `0xB5` | 1 | `uint8` | 槽45特效值；字段策略 Editable |
| `槽46特效值` | `0xB9` | 1 | `uint8` | 槽46特效值；字段策略 Editable |
| `槽47特效值` | `0xBD` | 1 | `uint8` | 槽47特效值；字段策略 Editable |
| `槽48特效值` | `0xC1` | 1 | `uint8` | 槽48特效值；字段策略 Editable |
| `槽49特效值` | `0xC5` | 1 | `uint8` | 槽49特效值；字段策略 Editable |
| `槽50特效值` | `0xC9` | 1 | `uint8` | 槽50特效值；字段策略 Editable |
| `槽51特效值` | `0xCD` | 1 | `uint8` | 槽51特效值；字段策略 Editable |
| `槽52特效值` | `0xD1` | 1 | `uint8` | 槽52特效值；字段策略 Editable |
| `槽53特效值` | `0xD5` | 1 | `uint8` | 槽53特效值；字段策略 Editable |
| `槽54特效值` | `0xD9` | 1 | `uint8` | 槽54特效值；字段策略 Editable |
| `槽55特效值` | `0xDD` | 1 | `uint8` | 槽55特效值；字段策略 Editable |
| `槽56特效值` | `0xE1` | 1 | `uint8` | 槽56特效值；字段策略 Editable |
| `槽57特效值` | `0xE5` | 1 | `uint8` | 槽57特效值；字段策略 Editable |
| `槽58特效值` | `0xE9` | 1 | `uint8` | 槽58特效值；字段策略 Editable |
| `槽59特效值` | `0xED` | 1 | `uint8` | 槽59特效值；字段策略 Editable |
| `槽60特效值` | `0xF1` | 1 | `uint8` | 槽60特效值；字段策略 Editable |
| `槽61特效值` | `0xF5` | 1 | `uint8` | 槽61特效值；字段策略 Editable |
| `槽62特效值` | `0xF9` | 1 | `uint8` | 槽62特效值；字段策略 Editable |
| `槽63特效值` | `0xFD` | 1 | `uint8` | 槽63特效值；字段策略 Editable |
| `槽64特效值` | `0x101` | 1 | `uint8` | 槽64特效值；字段策略 Editable |
| `槽65特效值` | `0x105` | 1 | `uint8` | 槽65特效值；字段策略 Editable |
| `槽66特效值` | `0x109` | 1 | `uint8` | 槽66特效值；字段策略 Editable |
| `槽67特效值` | `0x10D` | 1 | `uint8` | 槽67特效值；字段策略 Editable |
| `槽68特效值` | `0x111` | 1 | `uint8` | 槽68特效值；字段策略 Editable |
| `槽69特效值` | `0x115` | 1 | `uint8` | 槽69特效值；字段策略 Editable |
| `槽70特效值` | `0x119` | 1 | `uint8` | 槽70特效值；字段策略 Editable |
| `槽71特效值` | `0x11D` | 1 | `uint8` | 槽71特效值；字段策略 Editable |
| `槽72特效值` | `0x121` | 1 | `uint8` | 槽72特效值；字段策略 Editable |
| `槽73特效值` | `0x125` | 1 | `uint8` | 槽73特效值；字段策略 Editable |
| `槽74特效值` | `0x129` | 1 | `uint8` | 槽74特效值；字段策略 Editable |
| `槽75特效值` | `0x12D` | 1 | `uint8` | 槽75特效值；字段策略 Editable |
| `槽76特效值` | `0x131` | 1 | `uint8` | 槽76特效值；字段策略 Editable |
| `槽77特效值` | `0x135` | 1 | `uint8` | 槽77特效值；字段策略 Editable |
| `槽78特效值` | `0x139` | 1 | `uint8` | 槽78特效值；字段策略 Editable |
| `槽79特效值` | `0x13D` | 1 | `uint8` | 槽79特效值；字段策略 Editable |
| `槽80特效值` | `0x141` | 1 | `uint8` | 槽80特效值；字段策略 Editable |
| `槽81特效值` | `0x145` | 1 | `uint8` | 槽81特效值；字段策略 Editable |
| `槽82特效值` | `0x149` | 1 | `uint8` | 槽82特效值；字段策略 Editable |
| `槽83特效值` | `0x14D` | 1 | `uint8` | 槽83特效值；字段策略 Editable |
| `槽84特效值` | `0x151` | 1 | `uint8` | 槽84特效值；字段策略 Editable |
| `槽85特效值` | `0x155` | 1 | `uint8` | 槽85特效值；字段策略 Editable |
| `槽86特效值` | `0x159` | 1 | `uint8` | 槽86特效值；字段策略 Editable |
| `槽87特效值` | `0x15D` | 1 | `uint8` | 槽87特效值；字段策略 Editable |
| `槽88特效值` | `0x161` | 1 | `uint8` | 槽88特效值；字段策略 Editable |
| `槽89特效值` | `0x165` | 1 | `uint8` | 槽89特效值；字段策略 Editable |
| `槽90特效值` | `0x169` | 1 | `uint8` | 槽90特效值；字段策略 Editable |
| `槽91特效值` | `0x16D` | 1 | `uint8` | 槽91特效值；字段策略 Editable |
| `槽92特效值` | `0x171` | 1 | `uint8` | 槽92特效值；字段策略 Editable |
| `槽93特效值` | `0x175` | 1 | `uint8` | 槽93特效值；字段策略 Editable |
| `槽94特效值` | `0x179` | 1 | `uint8` | 槽94特效值；字段策略 Editable |
| `槽95特效值` | `0x17D` | 1 | `uint8` | 槽95特效值；字段策略 Editable |
| `槽96特效值` | `0x181` | 1 | `uint8` | 槽96特效值；字段策略 Editable |
| `槽97特效值` | `0x185` | 1 | `uint8` | 槽97特效值；字段策略 Editable |
| `槽98特效值` | `0x189` | 1 | `uint8` | 槽98特效值；字段策略 Editable |
| `槽99特效值` | `0x18D` | 1 | `uint8` | 槽99特效值；字段策略 Editable |
| `槽100特效值` | `0x191` | 1 | `uint8` | 槽100特效值；字段策略 Editable |
| `槽101特效值` | `0x195` | 1 | `uint8` | 槽101特效值；字段策略 Editable |
| `槽102特效值` | `0x199` | 1 | `uint8` | 槽102特效值；字段策略 Editable |
| `槽103特效值` | `0x19D` | 1 | `uint8` | 槽103特效值；字段策略 Editable |
| `槽104特效值` | `0x1A1` | 1 | `uint8` | 槽104特效值；字段策略 Editable |
| `槽105特效值` | `0x1A5` | 1 | `uint8` | 槽105特效值；字段策略 Editable |
| `槽106特效值` | `0x1A9` | 1 | `uint8` | 槽106特效值；字段策略 Editable |
| `槽107特效值` | `0x1AD` | 1 | `uint8` | 槽107特效值；字段策略 Editable |
| `槽108特效值` | `0x1B1` | 1 | `uint8` | 槽108特效值；字段策略 Editable |
| `槽109特效值` | `0x1B5` | 1 | `uint8` | 槽109特效值；字段策略 Editable |
| `槽110特效值` | `0x1B9` | 1 | `uint8` | 槽110特效值；字段策略 Editable |
| `槽111特效值` | `0x1BD` | 1 | `uint8` | 槽111特效值；字段策略 Editable |
| `槽112特效值` | `0x1C1` | 1 | `uint8` | 槽112特效值；字段策略 Editable |
| `槽113特效值` | `0x1C5` | 1 | `uint8` | 槽113特效值；字段策略 Editable |
| `槽114特效值` | `0x1C9` | 1 | `uint8` | 槽114特效值；字段策略 Editable |
| `槽115特效值` | `0x1CD` | 1 | `uint8` | 槽115特效值；字段策略 Editable |
| `槽116特效值` | `0x1D1` | 1 | `uint8` | 槽116特效值；字段策略 Editable |
| `槽117特效值` | `0x1D5` | 1 | `uint8` | 槽117特效值；字段策略 Editable |
| `槽118特效值` | `0x1D9` | 1 | `uint8` | 槽118特效值；字段策略 Editable |
| `槽119特效值` | `0x1DD` | 1 | `uint8` | 槽119特效值；字段策略 Editable |
| `槽120特效值` | `0x1E1` | 1 | `uint8` | 槽120特效值；字段策略 Editable |
| `槽121特效值` | `0x1E5` | 1 | `uint8` | 槽121特效值；字段策略 Editable |
| `槽122特效值` | `0x1E9` | 1 | `uint8` | 槽122特效值；字段策略 Editable |
| `槽123特效值` | `0x1ED` | 1 | `uint8` | 槽123特效值；字段策略 Editable |
| `槽124特效值` | `0x1F1` | 1 | `uint8` | 槽124特效值；字段策略 Editable |
| `槽125特效值` | `0x1F5` | 1 | `uint8` | 槽125特效值；字段策略 Editable |
| `槽126特效值` | `0x1F9` | 1 | `uint8` | 槽126特效值；字段策略 Editable |
| `槽127特效值` | `0x1FD` | 1 | `uint8` | 槽127特效值；字段策略 Editable |
| `槽128特效值` | `0x201` | 1 | `uint8` | 槽128特效值；字段策略 Editable |
| `槽129特效值` | `0x205` | 1 | `uint8` | 槽129特效值；字段策略 Editable |
| `槽130特效值` | `0x209` | 1 | `uint8` | 槽130特效值；字段策略 Editable |
| `槽131特效值` | `0x20D` | 1 | `uint8` | 槽131特效值；字段策略 Editable |
| `槽132特效值` | `0x211` | 1 | `uint8` | 槽132特效值；字段策略 Editable |
| `槽133特效值` | `0x215` | 1 | `uint8` | 槽133特效值；字段策略 Editable |
| `槽134特效值` | `0x219` | 1 | `uint8` | 槽134特效值；字段策略 Editable |
| `槽135特效值` | `0x21D` | 1 | `uint8` | 槽135特效值；字段策略 Editable |
| `槽136特效值` | `0x221` | 1 | `uint8` | 槽136特效值；字段策略 Editable |
| `槽137特效值` | `0x225` | 1 | `uint8` | 槽137特效值；字段策略 Editable |
| `槽138特效值` | `0x229` | 1 | `uint8` | 槽138特效值；字段策略 Editable |
| `槽139特效值` | `0x22D` | 1 | `uint8` | 槽139特效值；字段策略 Editable |
| `槽140特效值` | `0x231` | 1 | `uint8` | 槽140特效值；字段策略 Editable |
| `槽141特效值` | `0x235` | 1 | `uint8` | 槽141特效值；字段策略 Editable |
| `槽142特效值` | `0x239` | 1 | `uint8` | 槽142特效值；字段策略 Editable |
| `槽143特效值` | `0x23D` | 1 | `uint8` | 槽143特效值；字段策略 Editable |
| `槽144特效值` | `0x241` | 1 | `uint8` | 槽144特效值；字段策略 Editable |
| `槽145特效值` | `0x245` | 1 | `uint8` | 槽145特效值；字段策略 Editable |
| `槽146特效值` | `0x249` | 1 | `uint8` | 槽146特效值；字段策略 Editable |
| `槽147特效值` | `0x24D` | 1 | `uint8` | 槽147特效值；字段策略 Editable |
| `槽148特效值` | `0x251` | 1 | `uint8` | 槽148特效值；字段策略 Editable |
| `槽149特效值` | `0x255` | 1 | `uint8` | 槽149特效值；字段策略 Editable |
| `槽150特效值` | `0x259` | 1 | `uint8` | 槽150特效值；字段策略 Editable |
| `槽151特效值` | `0x25D` | 1 | `uint8` | 槽151特效值；字段策略 Editable |
| `槽152特效值` | `0x261` | 1 | `uint8` | 槽152特效值；字段策略 Editable |
| `槽153特效值` | `0x265` | 1 | `uint8` | 槽153特效值；字段策略 Editable |
| `槽154特效值` | `0x269` | 1 | `uint8` | 槽154特效值；字段策略 Editable |
| `槽155特效值` | `0x26D` | 1 | `uint8` | 槽155特效值；字段策略 Editable |
| `槽156特效值` | `0x271` | 1 | `uint8` | 槽156特效值；字段策略 Editable |
| `槽157特效值` | `0x275` | 1 | `uint8` | 槽157特效值；字段策略 Editable |
| `槽158特效值` | `0x279` | 1 | `uint8` | 槽158特效值；字段策略 Editable |
| `槽159特效值` | `0x27D` | 1 | `uint8` | 槽159特效值；字段策略 Editable |
| `槽160特效值` | `0x281` | 1 | `uint8` | 槽160特效值；字段策略 Editable |
| `槽161特效值` | `0x285` | 1 | `uint8` | 槽161特效值；字段策略 Editable |
| `槽162特效值` | `0x289` | 1 | `uint8` | 槽162特效值；字段策略 Editable |
| `槽163特效值` | `0x28D` | 1 | `uint8` | 槽163特效值；字段策略 Editable |
| `槽164特效值` | `0x291` | 1 | `uint8` | 槽164特效值；字段策略 Editable |
| `槽165特效值` | `0x295` | 1 | `uint8` | 槽165特效值；字段策略 Editable |
| `槽166特效值` | `0x299` | 1 | `uint8` | 槽166特效值；字段策略 Editable |
| `槽167特效值` | `0x29D` | 1 | `uint8` | 槽167特效值；字段策略 Editable |
| `槽168特效值` | `0x2A1` | 1 | `uint8` | 槽168特效值；字段策略 Editable |
| `槽169特效值` | `0x2A5` | 1 | `uint8` | 槽169特效值；字段策略 Editable |
| `槽170特效值` | `0x2A9` | 1 | `uint8` | 槽170特效值；字段策略 Editable |
| `槽171特效值` | `0x2AD` | 1 | `uint8` | 槽171特效值；字段策略 Editable |
| `槽172特效值` | `0x2B1` | 1 | `uint8` | 槽172特效值；字段策略 Editable |
| `槽173特效值` | `0x2B5` | 1 | `uint8` | 槽173特效值；字段策略 Editable |
| `槽174特效值` | `0x2B9` | 1 | `uint8` | 槽174特效值；字段策略 Editable |
| `槽175特效值` | `0x2BD` | 1 | `uint8` | 槽175特效值；字段策略 Editable |
| `槽176特效值` | `0x2C1` | 1 | `uint8` | 槽176特效值；字段策略 Editable |
| `槽177特效值` | `0x2C5` | 1 | `uint8` | 槽177特效值；字段策略 Editable |
| `槽178特效值` | `0x2C9` | 1 | `uint8` | 槽178特效值；字段策略 Editable |
| `槽179特效值` | `0x2CD` | 1 | `uint8` | 槽179特效值；字段策略 Editable |
| `槽180特效值` | `0x2D1` | 1 | `uint8` | 槽180特效值；字段策略 Editable |
| `槽181特效值` | `0x2D5` | 1 | `uint8` | 槽181特效值；字段策略 Editable |
| `槽182特效值` | `0x2D9` | 1 | `uint8` | 槽182特效值；字段策略 Editable |
| `槽183特效值` | `0x2DD` | 1 | `uint8` | 槽183特效值；字段策略 Editable |
| `槽184特效值` | `0x2E1` | 1 | `uint8` | 槽184特效值；字段策略 Editable |
| `槽185特效值` | `0x2E5` | 1 | `uint8` | 槽185特效值；字段策略 Editable |
| `槽186特效值` | `0x2E9` | 1 | `uint8` | 槽186特效值；字段策略 Editable |
| `槽187特效值` | `0x2ED` | 1 | `uint8` | 槽187特效值；字段策略 Editable |
| `槽188特效值` | `0x2F1` | 1 | `uint8` | 槽188特效值；字段策略 Editable |
| `槽189特效值` | `0x2F5` | 1 | `uint8` | 槽189特效值；字段策略 Editable |
| `槽190特效值` | `0x2F9` | 1 | `uint8` | 槽190特效值；字段策略 Editable |
| `槽191特效值` | `0x2FD` | 1 | `uint8` | 槽191特效值；字段策略 Editable |
| `槽192特效值` | `0x301` | 1 | `uint8` | 槽192特效值；字段策略 Editable |
| `槽193特效值` | `0x305` | 1 | `uint8` | 槽193特效值；字段策略 Editable |
| `槽194特效值` | `0x309` | 1 | `uint8` | 槽194特效值；字段策略 Editable |
| `槽195特效值` | `0x30D` | 1 | `uint8` | 槽195特效值；字段策略 Editable |
| `槽196特效值` | `0x311` | 1 | `uint8` | 槽196特效值；字段策略 Editable |
| `槽197特效值` | `0x315` | 1 | `uint8` | 槽197特效值；字段策略 Editable |
| `槽198特效值` | `0x319` | 1 | `uint8` | 槽198特效值；字段策略 Editable |
| `槽199特效值` | `0x31D` | 1 | `uint8` | 槽199特效值；字段策略 Editable |
| `槽200特效值` | `0x321` | 1 | `uint8` | 槽200特效值；字段策略 Editable |
| `槽201特效值` | `0x325` | 1 | `uint8` | 槽201特效值；字段策略 Editable |
| `槽202特效值` | `0x329` | 1 | `uint8` | 槽202特效值；字段策略 Editable |
| `槽203特效值` | `0x32D` | 1 | `uint8` | 槽203特效值；字段策略 Editable |
| `槽204特效值` | `0x331` | 1 | `uint8` | 槽204特效值；字段策略 Editable |
| `槽205特效值` | `0x335` | 1 | `uint8` | 槽205特效值；字段策略 Editable |
| `槽206特效值` | `0x339` | 1 | `uint8` | 槽206特效值；字段策略 Editable |
| `槽207特效值` | `0x33D` | 1 | `uint8` | 槽207特效值；字段策略 Editable |
| `槽208特效值` | `0x341` | 1 | `uint8` | 槽208特效值；字段策略 Editable |
| `槽209特效值` | `0x345` | 1 | `uint8` | 槽209特效值；字段策略 Editable |
| `槽210特效值` | `0x349` | 1 | `uint8` | 槽210特效值；字段策略 Editable |
| `槽211特效值` | `0x34D` | 1 | `uint8` | 槽211特效值；字段策略 Editable |
| `槽212特效值` | `0x351` | 1 | `uint8` | 槽212特效值；字段策略 Editable |
| `槽213特效值` | `0x355` | 1 | `uint8` | 槽213特效值；字段策略 Editable |
| `槽214特效值` | `0x359` | 1 | `uint8` | 槽214特效值；字段策略 Editable |
| `槽215特效值` | `0x35D` | 1 | `uint8` | 槽215特效值；字段策略 Editable |
| `槽216特效值` | `0x361` | 1 | `uint8` | 槽216特效值；字段策略 Editable |
| `槽217特效值` | `0x365` | 1 | `uint8` | 槽217特效值；字段策略 Editable |
| `槽218特效值` | `0x369` | 1 | `uint8` | 槽218特效值；字段策略 Editable |
| `槽219特效值` | `0x36D` | 1 | `uint8` | 槽219特效值；字段策略 Editable |
| `槽220特效值` | `0x371` | 1 | `uint8` | 槽220特效值；字段策略 Editable |
| `槽221特效值` | `0x375` | 1 | `uint8` | 槽221特效值；字段策略 Editable |
| `槽222特效值` | `0x379` | 1 | `uint8` | 槽222特效值；字段策略 Editable |
| `槽223特效值` | `0x37D` | 1 | `uint8` | 槽223特效值；字段策略 Editable |
| `槽224特效值` | `0x381` | 1 | `uint8` | 槽224特效值；字段策略 Editable |
| `槽225特效值` | `0x385` | 1 | `uint8` | 槽225特效值；字段策略 Editable |
| `槽226特效值` | `0x389` | 1 | `uint8` | 槽226特效值；字段策略 Editable |
| `槽227特效值` | `0x38D` | 1 | `uint8` | 槽227特效值；字段策略 Editable |
| `槽228特效值` | `0x391` | 1 | `uint8` | 槽228特效值；字段策略 Editable |
| `槽229特效值` | `0x395` | 1 | `uint8` | 槽229特效值；字段策略 Editable |
| `槽230特效值` | `0x399` | 1 | `uint8` | 槽230特效值；字段策略 Editable |
| `槽231特效值` | `0x39D` | 1 | `uint8` | 槽231特效值；字段策略 Editable |
| `槽232特效值` | `0x3A1` | 1 | `uint8` | 槽232特效值；字段策略 Editable |
| `槽233特效值` | `0x3A5` | 1 | `uint8` | 槽233特效值；字段策略 Editable |
| `槽234特效值` | `0x3A9` | 1 | `uint8` | 槽234特效值；字段策略 Editable |
| `槽235特效值` | `0x3AD` | 1 | `uint8` | 槽235特效值；字段策略 Editable |
| `槽236特效值` | `0x3B1` | 1 | `uint8` | 槽236特效值；字段策略 Editable |
| `槽237特效值` | `0x3B5` | 1 | `uint8` | 槽237特效值；字段策略 Editable |
| `槽238特效值` | `0x3B9` | 1 | `uint8` | 槽238特效值；字段策略 Editable |
| `槽239特效值` | `0x3BD` | 1 | `uint8` | 槽239特效值；字段策略 Editable |
| `槽240特效值` | `0x3C1` | 1 | `uint8` | 槽240特效值；字段策略 Editable |
| `槽241特效值` | `0x3C5` | 1 | `uint8` | 槽241特效值；字段策略 Editable |
| `槽242特效值` | `0x3C9` | 1 | `uint8` | 槽242特效值；字段策略 Editable |
| `槽243特效值` | `0x3CD` | 1 | `uint8` | 槽243特效值；字段策略 Editable |
| `槽244特效值` | `0x3D1` | 1 | `uint8` | 槽244特效值；字段策略 Editable |
| `槽245特效值` | `0x3D5` | 1 | `uint8` | 槽245特效值；字段策略 Editable |
| `槽246特效值` | `0x3D9` | 1 | `uint8` | 槽246特效值；字段策略 Editable |
| `槽247特效值` | `0x3DD` | 1 | `uint8` | 槽247特效值；字段策略 Editable |
| `槽248特效值` | `0x3E1` | 1 | `uint8` | 槽248特效值；字段策略 Editable |
| `槽249特效值` | `0x3E5` | 1 | `uint8` | 槽249特效值；字段策略 Editable |
| `槽250特效值` | `0x3E9` | 1 | `uint8` | 槽250特效值；字段策略 Editable |
| `槽251特效值` | `0x3ED` | 1 | `uint8` | 槽251特效值；字段策略 Editable |
| `槽252特效值` | `0x3F1` | 1 | `uint8` | 槽252特效值；字段策略 Editable |
| `槽253特效值` | `0x3F5` | 1 | `uint8` | 槽253特效值；字段策略 Editable |
| `槽254特效值` | `0x3F9` | 1 | `uint8` | 槽254特效值；字段策略 Editable |
| `槽255特效值` | `0x3FD` | 1 | `uint8` | 槽255特效值；字段策略 Editable |
| `槽0经验` | `0x2` | 1 | `uint8` | 槽0经验；字段策略 Editable |
| `槽1经验` | `0x6` | 1 | `uint8` | 槽1经验；字段策略 Editable |
| `槽2经验` | `0xA` | 1 | `uint8` | 槽2经验；字段策略 Editable |
| `槽3经验` | `0xE` | 1 | `uint8` | 槽3经验；字段策略 Editable |
| `槽4经验` | `0x12` | 1 | `uint8` | 槽4经验；字段策略 Editable |
| `槽5经验` | `0x16` | 1 | `uint8` | 槽5经验；字段策略 Editable |
| `槽6经验` | `0x1A` | 1 | `uint8` | 槽6经验；字段策略 Editable |
| `槽7经验` | `0x1E` | 1 | `uint8` | 槽7经验；字段策略 Editable |
| `槽8经验` | `0x22` | 1 | `uint8` | 槽8经验；字段策略 Editable |
| `槽9经验` | `0x26` | 1 | `uint8` | 槽9经验；字段策略 Editable |
| `槽10经验` | `0x2A` | 1 | `uint8` | 槽10经验；字段策略 Editable |
| `槽11经验` | `0x2E` | 1 | `uint8` | 槽11经验；字段策略 Editable |
| `槽12经验` | `0x32` | 1 | `uint8` | 槽12经验；字段策略 Editable |
| `槽13经验` | `0x36` | 1 | `uint8` | 槽13经验；字段策略 Editable |
| `槽14经验` | `0x3A` | 1 | `uint8` | 槽14经验；字段策略 Editable |
| `槽15经验` | `0x3E` | 1 | `uint8` | 槽15经验；字段策略 Editable |
| `槽16经验` | `0x42` | 1 | `uint8` | 槽16经验；字段策略 Editable |
| `槽17经验` | `0x46` | 1 | `uint8` | 槽17经验；字段策略 Editable |
| `槽18经验` | `0x4A` | 1 | `uint8` | 槽18经验；字段策略 Editable |
| `槽19经验` | `0x4E` | 1 | `uint8` | 槽19经验；字段策略 Editable |
| `槽20经验` | `0x52` | 1 | `uint8` | 槽20经验；字段策略 Editable |
| `槽21经验` | `0x56` | 1 | `uint8` | 槽21经验；字段策略 Editable |
| `槽22经验` | `0x5A` | 1 | `uint8` | 槽22经验；字段策略 Editable |
| `槽23经验` | `0x5E` | 1 | `uint8` | 槽23经验；字段策略 Editable |
| `槽24经验` | `0x62` | 1 | `uint8` | 槽24经验；字段策略 Editable |
| `槽25经验` | `0x66` | 1 | `uint8` | 槽25经验；字段策略 Editable |
| `槽26经验` | `0x6A` | 1 | `uint8` | 槽26经验；字段策略 Editable |
| `槽27经验` | `0x6E` | 1 | `uint8` | 槽27经验；字段策略 Editable |
| `槽28经验` | `0x72` | 1 | `uint8` | 槽28经验；字段策略 Editable |
| `槽29经验` | `0x76` | 1 | `uint8` | 槽29经验；字段策略 Editable |
| `槽30经验` | `0x7A` | 1 | `uint8` | 槽30经验；字段策略 Editable |
| `槽31经验` | `0x7E` | 1 | `uint8` | 槽31经验；字段策略 Editable |
| `槽32经验` | `0x82` | 1 | `uint8` | 槽32经验；字段策略 Editable |
| `槽33经验` | `0x86` | 1 | `uint8` | 槽33经验；字段策略 Editable |
| `槽34经验` | `0x8A` | 1 | `uint8` | 槽34经验；字段策略 Editable |
| `槽35经验` | `0x8E` | 1 | `uint8` | 槽35经验；字段策略 Editable |
| `槽36经验` | `0x92` | 1 | `uint8` | 槽36经验；字段策略 Editable |
| `槽37经验` | `0x96` | 1 | `uint8` | 槽37经验；字段策略 Editable |
| `槽38经验` | `0x9A` | 1 | `uint8` | 槽38经验；字段策略 Editable |
| `槽39经验` | `0x9E` | 1 | `uint8` | 槽39经验；字段策略 Editable |
| `槽40经验` | `0xA2` | 1 | `uint8` | 槽40经验；字段策略 Editable |
| `槽41经验` | `0xA6` | 1 | `uint8` | 槽41经验；字段策略 Editable |
| `槽42经验` | `0xAA` | 1 | `uint8` | 槽42经验；字段策略 Editable |
| `槽43经验` | `0xAE` | 1 | `uint8` | 槽43经验；字段策略 Editable |
| `槽44经验` | `0xB2` | 1 | `uint8` | 槽44经验；字段策略 Editable |
| `槽45经验` | `0xB6` | 1 | `uint8` | 槽45经验；字段策略 Editable |
| `槽46经验` | `0xBA` | 1 | `uint8` | 槽46经验；字段策略 Editable |
| `槽47经验` | `0xBE` | 1 | `uint8` | 槽47经验；字段策略 Editable |
| `槽48经验` | `0xC2` | 1 | `uint8` | 槽48经验；字段策略 Editable |
| `槽49经验` | `0xC6` | 1 | `uint8` | 槽49经验；字段策略 Editable |
| `槽50经验` | `0xCA` | 1 | `uint8` | 槽50经验；字段策略 Editable |
| `槽51经验` | `0xCE` | 1 | `uint8` | 槽51经验；字段策略 Editable |
| `槽52经验` | `0xD2` | 1 | `uint8` | 槽52经验；字段策略 Editable |
| `槽53经验` | `0xD6` | 1 | `uint8` | 槽53经验；字段策略 Editable |
| `槽54经验` | `0xDA` | 1 | `uint8` | 槽54经验；字段策略 Editable |
| `槽55经验` | `0xDE` | 1 | `uint8` | 槽55经验；字段策略 Editable |
| `槽56经验` | `0xE2` | 1 | `uint8` | 槽56经验；字段策略 Editable |
| `槽57经验` | `0xE6` | 1 | `uint8` | 槽57经验；字段策略 Editable |
| `槽58经验` | `0xEA` | 1 | `uint8` | 槽58经验；字段策略 Editable |
| `槽59经验` | `0xEE` | 1 | `uint8` | 槽59经验；字段策略 Editable |
| `槽60经验` | `0xF2` | 1 | `uint8` | 槽60经验；字段策略 Editable |
| `槽61经验` | `0xF6` | 1 | `uint8` | 槽61经验；字段策略 Editable |
| `槽62经验` | `0xFA` | 1 | `uint8` | 槽62经验；字段策略 Editable |
| `槽63经验` | `0xFE` | 1 | `uint8` | 槽63经验；字段策略 Editable |
| `槽64经验` | `0x102` | 1 | `uint8` | 槽64经验；字段策略 Editable |
| `槽65经验` | `0x106` | 1 | `uint8` | 槽65经验；字段策略 Editable |
| `槽66经验` | `0x10A` | 1 | `uint8` | 槽66经验；字段策略 Editable |
| `槽67经验` | `0x10E` | 1 | `uint8` | 槽67经验；字段策略 Editable |
| `槽68经验` | `0x112` | 1 | `uint8` | 槽68经验；字段策略 Editable |
| `槽69经验` | `0x116` | 1 | `uint8` | 槽69经验；字段策略 Editable |
| `槽70经验` | `0x11A` | 1 | `uint8` | 槽70经验；字段策略 Editable |
| `槽71经验` | `0x11E` | 1 | `uint8` | 槽71经验；字段策略 Editable |
| `槽72经验` | `0x122` | 1 | `uint8` | 槽72经验；字段策略 Editable |
| `槽73经验` | `0x126` | 1 | `uint8` | 槽73经验；字段策略 Editable |
| `槽74经验` | `0x12A` | 1 | `uint8` | 槽74经验；字段策略 Editable |
| `槽75经验` | `0x12E` | 1 | `uint8` | 槽75经验；字段策略 Editable |
| `槽76经验` | `0x132` | 1 | `uint8` | 槽76经验；字段策略 Editable |
| `槽77经验` | `0x136` | 1 | `uint8` | 槽77经验；字段策略 Editable |
| `槽78经验` | `0x13A` | 1 | `uint8` | 槽78经验；字段策略 Editable |
| `槽79经验` | `0x13E` | 1 | `uint8` | 槽79经验；字段策略 Editable |
| `槽80经验` | `0x142` | 1 | `uint8` | 槽80经验；字段策略 Editable |
| `槽81经验` | `0x146` | 1 | `uint8` | 槽81经验；字段策略 Editable |
| `槽82经验` | `0x14A` | 1 | `uint8` | 槽82经验；字段策略 Editable |
| `槽83经验` | `0x14E` | 1 | `uint8` | 槽83经验；字段策略 Editable |
| `槽84经验` | `0x152` | 1 | `uint8` | 槽84经验；字段策略 Editable |
| `槽85经验` | `0x156` | 1 | `uint8` | 槽85经验；字段策略 Editable |
| `槽86经验` | `0x15A` | 1 | `uint8` | 槽86经验；字段策略 Editable |
| `槽87经验` | `0x15E` | 1 | `uint8` | 槽87经验；字段策略 Editable |
| `槽88经验` | `0x162` | 1 | `uint8` | 槽88经验；字段策略 Editable |
| `槽89经验` | `0x166` | 1 | `uint8` | 槽89经验；字段策略 Editable |
| `槽90经验` | `0x16A` | 1 | `uint8` | 槽90经验；字段策略 Editable |
| `槽91经验` | `0x16E` | 1 | `uint8` | 槽91经验；字段策略 Editable |
| `槽92经验` | `0x172` | 1 | `uint8` | 槽92经验；字段策略 Editable |
| `槽93经验` | `0x176` | 1 | `uint8` | 槽93经验；字段策略 Editable |
| `槽94经验` | `0x17A` | 1 | `uint8` | 槽94经验；字段策略 Editable |
| `槽95经验` | `0x17E` | 1 | `uint8` | 槽95经验；字段策略 Editable |
| `槽96经验` | `0x182` | 1 | `uint8` | 槽96经验；字段策略 Editable |
| `槽97经验` | `0x186` | 1 | `uint8` | 槽97经验；字段策略 Editable |
| `槽98经验` | `0x18A` | 1 | `uint8` | 槽98经验；字段策略 Editable |
| `槽99经验` | `0x18E` | 1 | `uint8` | 槽99经验；字段策略 Editable |
| `槽100经验` | `0x192` | 1 | `uint8` | 槽100经验；字段策略 Editable |
| `槽101经验` | `0x196` | 1 | `uint8` | 槽101经验；字段策略 Editable |
| `槽102经验` | `0x19A` | 1 | `uint8` | 槽102经验；字段策略 Editable |
| `槽103经验` | `0x19E` | 1 | `uint8` | 槽103经验；字段策略 Editable |
| `槽104经验` | `0x1A2` | 1 | `uint8` | 槽104经验；字段策略 Editable |
| `槽105经验` | `0x1A6` | 1 | `uint8` | 槽105经验；字段策略 Editable |
| `槽106经验` | `0x1AA` | 1 | `uint8` | 槽106经验；字段策略 Editable |
| `槽107经验` | `0x1AE` | 1 | `uint8` | 槽107经验；字段策略 Editable |
| `槽108经验` | `0x1B2` | 1 | `uint8` | 槽108经验；字段策略 Editable |
| `槽109经验` | `0x1B6` | 1 | `uint8` | 槽109经验；字段策略 Editable |
| `槽110经验` | `0x1BA` | 1 | `uint8` | 槽110经验；字段策略 Editable |
| `槽111经验` | `0x1BE` | 1 | `uint8` | 槽111经验；字段策略 Editable |
| `槽112经验` | `0x1C2` | 1 | `uint8` | 槽112经验；字段策略 Editable |
| `槽113经验` | `0x1C6` | 1 | `uint8` | 槽113经验；字段策略 Editable |
| `槽114经验` | `0x1CA` | 1 | `uint8` | 槽114经验；字段策略 Editable |
| `槽115经验` | `0x1CE` | 1 | `uint8` | 槽115经验；字段策略 Editable |
| `槽116经验` | `0x1D2` | 1 | `uint8` | 槽116经验；字段策略 Editable |
| `槽117经验` | `0x1D6` | 1 | `uint8` | 槽117经验；字段策略 Editable |
| `槽118经验` | `0x1DA` | 1 | `uint8` | 槽118经验；字段策略 Editable |
| `槽119经验` | `0x1DE` | 1 | `uint8` | 槽119经验；字段策略 Editable |
| `槽120经验` | `0x1E2` | 1 | `uint8` | 槽120经验；字段策略 Editable |
| `槽121经验` | `0x1E6` | 1 | `uint8` | 槽121经验；字段策略 Editable |
| `槽122经验` | `0x1EA` | 1 | `uint8` | 槽122经验；字段策略 Editable |
| `槽123经验` | `0x1EE` | 1 | `uint8` | 槽123经验；字段策略 Editable |
| `槽124经验` | `0x1F2` | 1 | `uint8` | 槽124经验；字段策略 Editable |
| `槽125经验` | `0x1F6` | 1 | `uint8` | 槽125经验；字段策略 Editable |
| `槽126经验` | `0x1FA` | 1 | `uint8` | 槽126经验；字段策略 Editable |
| `槽127经验` | `0x1FE` | 1 | `uint8` | 槽127经验；字段策略 Editable |
| `槽128经验` | `0x202` | 1 | `uint8` | 槽128经验；字段策略 Editable |
| `槽129经验` | `0x206` | 1 | `uint8` | 槽129经验；字段策略 Editable |
| `槽130经验` | `0x20A` | 1 | `uint8` | 槽130经验；字段策略 Editable |
| `槽131经验` | `0x20E` | 1 | `uint8` | 槽131经验；字段策略 Editable |
| `槽132经验` | `0x212` | 1 | `uint8` | 槽132经验；字段策略 Editable |
| `槽133经验` | `0x216` | 1 | `uint8` | 槽133经验；字段策略 Editable |
| `槽134经验` | `0x21A` | 1 | `uint8` | 槽134经验；字段策略 Editable |
| `槽135经验` | `0x21E` | 1 | `uint8` | 槽135经验；字段策略 Editable |
| `槽136经验` | `0x222` | 1 | `uint8` | 槽136经验；字段策略 Editable |
| `槽137经验` | `0x226` | 1 | `uint8` | 槽137经验；字段策略 Editable |
| `槽138经验` | `0x22A` | 1 | `uint8` | 槽138经验；字段策略 Editable |
| `槽139经验` | `0x22E` | 1 | `uint8` | 槽139经验；字段策略 Editable |
| `槽140经验` | `0x232` | 1 | `uint8` | 槽140经验；字段策略 Editable |
| `槽141经验` | `0x236` | 1 | `uint8` | 槽141经验；字段策略 Editable |
| `槽142经验` | `0x23A` | 1 | `uint8` | 槽142经验；字段策略 Editable |
| `槽143经验` | `0x23E` | 1 | `uint8` | 槽143经验；字段策略 Editable |
| `槽144经验` | `0x242` | 1 | `uint8` | 槽144经验；字段策略 Editable |
| `槽145经验` | `0x246` | 1 | `uint8` | 槽145经验；字段策略 Editable |
| `槽146经验` | `0x24A` | 1 | `uint8` | 槽146经验；字段策略 Editable |
| `槽147经验` | `0x24E` | 1 | `uint8` | 槽147经验；字段策略 Editable |
| `槽148经验` | `0x252` | 1 | `uint8` | 槽148经验；字段策略 Editable |
| `槽149经验` | `0x256` | 1 | `uint8` | 槽149经验；字段策略 Editable |
| `槽150经验` | `0x25A` | 1 | `uint8` | 槽150经验；字段策略 Editable |
| `槽151经验` | `0x25E` | 1 | `uint8` | 槽151经验；字段策略 Editable |
| `槽152经验` | `0x262` | 1 | `uint8` | 槽152经验；字段策略 Editable |
| `槽153经验` | `0x266` | 1 | `uint8` | 槽153经验；字段策略 Editable |
| `槽154经验` | `0x26A` | 1 | `uint8` | 槽154经验；字段策略 Editable |
| `槽155经验` | `0x26E` | 1 | `uint8` | 槽155经验；字段策略 Editable |
| `槽156经验` | `0x272` | 1 | `uint8` | 槽156经验；字段策略 Editable |
| `槽157经验` | `0x276` | 1 | `uint8` | 槽157经验；字段策略 Editable |
| `槽158经验` | `0x27A` | 1 | `uint8` | 槽158经验；字段策略 Editable |
| `槽159经验` | `0x27E` | 1 | `uint8` | 槽159经验；字段策略 Editable |
| `槽160经验` | `0x282` | 1 | `uint8` | 槽160经验；字段策略 Editable |
| `槽161经验` | `0x286` | 1 | `uint8` | 槽161经验；字段策略 Editable |
| `槽162经验` | `0x28A` | 1 | `uint8` | 槽162经验；字段策略 Editable |
| `槽163经验` | `0x28E` | 1 | `uint8` | 槽163经验；字段策略 Editable |
| `槽164经验` | `0x292` | 1 | `uint8` | 槽164经验；字段策略 Editable |
| `槽165经验` | `0x296` | 1 | `uint8` | 槽165经验；字段策略 Editable |
| `槽166经验` | `0x29A` | 1 | `uint8` | 槽166经验；字段策略 Editable |
| `槽167经验` | `0x29E` | 1 | `uint8` | 槽167经验；字段策略 Editable |
| `槽168经验` | `0x2A2` | 1 | `uint8` | 槽168经验；字段策略 Editable |
| `槽169经验` | `0x2A6` | 1 | `uint8` | 槽169经验；字段策略 Editable |
| `槽170经验` | `0x2AA` | 1 | `uint8` | 槽170经验；字段策略 Editable |
| `槽171经验` | `0x2AE` | 1 | `uint8` | 槽171经验；字段策略 Editable |
| `槽172经验` | `0x2B2` | 1 | `uint8` | 槽172经验；字段策略 Editable |
| `槽173经验` | `0x2B6` | 1 | `uint8` | 槽173经验；字段策略 Editable |
| `槽174经验` | `0x2BA` | 1 | `uint8` | 槽174经验；字段策略 Editable |
| `槽175经验` | `0x2BE` | 1 | `uint8` | 槽175经验；字段策略 Editable |
| `槽176经验` | `0x2C2` | 1 | `uint8` | 槽176经验；字段策略 Editable |
| `槽177经验` | `0x2C6` | 1 | `uint8` | 槽177经验；字段策略 Editable |
| `槽178经验` | `0x2CA` | 1 | `uint8` | 槽178经验；字段策略 Editable |
| `槽179经验` | `0x2CE` | 1 | `uint8` | 槽179经验；字段策略 Editable |
| `槽180经验` | `0x2D2` | 1 | `uint8` | 槽180经验；字段策略 Editable |
| `槽181经验` | `0x2D6` | 1 | `uint8` | 槽181经验；字段策略 Editable |
| `槽182经验` | `0x2DA` | 1 | `uint8` | 槽182经验；字段策略 Editable |
| `槽183经验` | `0x2DE` | 1 | `uint8` | 槽183经验；字段策略 Editable |
| `槽184经验` | `0x2E2` | 1 | `uint8` | 槽184经验；字段策略 Editable |
| `槽185经验` | `0x2E6` | 1 | `uint8` | 槽185经验；字段策略 Editable |
| `槽186经验` | `0x2EA` | 1 | `uint8` | 槽186经验；字段策略 Editable |
| `槽187经验` | `0x2EE` | 1 | `uint8` | 槽187经验；字段策略 Editable |
| `槽188经验` | `0x2F2` | 1 | `uint8` | 槽188经验；字段策略 Editable |
| `槽189经验` | `0x2F6` | 1 | `uint8` | 槽189经验；字段策略 Editable |
| `槽190经验` | `0x2FA` | 1 | `uint8` | 槽190经验；字段策略 Editable |
| `槽191经验` | `0x2FE` | 1 | `uint8` | 槽191经验；字段策略 Editable |
| `槽192经验` | `0x302` | 1 | `uint8` | 槽192经验；字段策略 Editable |
| `槽193经验` | `0x306` | 1 | `uint8` | 槽193经验；字段策略 Editable |
| `槽194经验` | `0x30A` | 1 | `uint8` | 槽194经验；字段策略 Editable |
| `槽195经验` | `0x30E` | 1 | `uint8` | 槽195经验；字段策略 Editable |
| `槽196经验` | `0x312` | 1 | `uint8` | 槽196经验；字段策略 Editable |
| `槽197经验` | `0x316` | 1 | `uint8` | 槽197经验；字段策略 Editable |
| `槽198经验` | `0x31A` | 1 | `uint8` | 槽198经验；字段策略 Editable |
| `槽199经验` | `0x31E` | 1 | `uint8` | 槽199经验；字段策略 Editable |
| `槽200经验` | `0x322` | 1 | `uint8` | 槽200经验；字段策略 Editable |
| `槽201经验` | `0x326` | 1 | `uint8` | 槽201经验；字段策略 Editable |
| `槽202经验` | `0x32A` | 1 | `uint8` | 槽202经验；字段策略 Editable |
| `槽203经验` | `0x32E` | 1 | `uint8` | 槽203经验；字段策略 Editable |
| `槽204经验` | `0x332` | 1 | `uint8` | 槽204经验；字段策略 Editable |
| `槽205经验` | `0x336` | 1 | `uint8` | 槽205经验；字段策略 Editable |
| `槽206经验` | `0x33A` | 1 | `uint8` | 槽206经验；字段策略 Editable |
| `槽207经验` | `0x33E` | 1 | `uint8` | 槽207经验；字段策略 Editable |
| `槽208经验` | `0x342` | 1 | `uint8` | 槽208经验；字段策略 Editable |
| `槽209经验` | `0x346` | 1 | `uint8` | 槽209经验；字段策略 Editable |
| `槽210经验` | `0x34A` | 1 | `uint8` | 槽210经验；字段策略 Editable |
| `槽211经验` | `0x34E` | 1 | `uint8` | 槽211经验；字段策略 Editable |
| `槽212经验` | `0x352` | 1 | `uint8` | 槽212经验；字段策略 Editable |
| `槽213经验` | `0x356` | 1 | `uint8` | 槽213经验；字段策略 Editable |
| `槽214经验` | `0x35A` | 1 | `uint8` | 槽214经验；字段策略 Editable |
| `槽215经验` | `0x35E` | 1 | `uint8` | 槽215经验；字段策略 Editable |
| `槽216经验` | `0x362` | 1 | `uint8` | 槽216经验；字段策略 Editable |
| `槽217经验` | `0x366` | 1 | `uint8` | 槽217经验；字段策略 Editable |
| `槽218经验` | `0x36A` | 1 | `uint8` | 槽218经验；字段策略 Editable |
| `槽219经验` | `0x36E` | 1 | `uint8` | 槽219经验；字段策略 Editable |
| `槽220经验` | `0x372` | 1 | `uint8` | 槽220经验；字段策略 Editable |
| `槽221经验` | `0x376` | 1 | `uint8` | 槽221经验；字段策略 Editable |
| `槽222经验` | `0x37A` | 1 | `uint8` | 槽222经验；字段策略 Editable |
| `槽223经验` | `0x37E` | 1 | `uint8` | 槽223经验；字段策略 Editable |
| `槽224经验` | `0x382` | 1 | `uint8` | 槽224经验；字段策略 Editable |
| `槽225经验` | `0x386` | 1 | `uint8` | 槽225经验；字段策略 Editable |
| `槽226经验` | `0x38A` | 1 | `uint8` | 槽226经验；字段策略 Editable |
| `槽227经验` | `0x38E` | 1 | `uint8` | 槽227经验；字段策略 Editable |
| `槽228经验` | `0x392` | 1 | `uint8` | 槽228经验；字段策略 Editable |
| `槽229经验` | `0x396` | 1 | `uint8` | 槽229经验；字段策略 Editable |
| `槽230经验` | `0x39A` | 1 | `uint8` | 槽230经验；字段策略 Editable |
| `槽231经验` | `0x39E` | 1 | `uint8` | 槽231经验；字段策略 Editable |
| `槽232经验` | `0x3A2` | 1 | `uint8` | 槽232经验；字段策略 Editable |
| `槽233经验` | `0x3A6` | 1 | `uint8` | 槽233经验；字段策略 Editable |
| `槽234经验` | `0x3AA` | 1 | `uint8` | 槽234经验；字段策略 Editable |
| `槽235经验` | `0x3AE` | 1 | `uint8` | 槽235经验；字段策略 Editable |
| `槽236经验` | `0x3B2` | 1 | `uint8` | 槽236经验；字段策略 Editable |
| `槽237经验` | `0x3B6` | 1 | `uint8` | 槽237经验；字段策略 Editable |
| `槽238经验` | `0x3BA` | 1 | `uint8` | 槽238经验；字段策略 Editable |
| `槽239经验` | `0x3BE` | 1 | `uint8` | 槽239经验；字段策略 Editable |
| `槽240经验` | `0x3C2` | 1 | `uint8` | 槽240经验；字段策略 Editable |
| `槽241经验` | `0x3C6` | 1 | `uint8` | 槽241经验；字段策略 Editable |
| `槽242经验` | `0x3CA` | 1 | `uint8` | 槽242经验；字段策略 Editable |
| `槽243经验` | `0x3CE` | 1 | `uint8` | 槽243经验；字段策略 Editable |
| `槽244经验` | `0x3D2` | 1 | `uint8` | 槽244经验；字段策略 Editable |
| `槽245经验` | `0x3D6` | 1 | `uint8` | 槽245经验；字段策略 Editable |
| `槽246经验` | `0x3DA` | 1 | `uint8` | 槽246经验；字段策略 Editable |
| `槽247经验` | `0x3DE` | 1 | `uint8` | 槽247经验；字段策略 Editable |
| `槽248经验` | `0x3E2` | 1 | `uint8` | 槽248经验；字段策略 Editable |
| `槽249经验` | `0x3E6` | 1 | `uint8` | 槽249经验；字段策略 Editable |
| `槽250经验` | `0x3EA` | 1 | `uint8` | 槽250经验；字段策略 Editable |
| `槽251经验` | `0x3EE` | 1 | `uint8` | 槽251经验；字段策略 Editable |
| `槽252经验` | `0x3F2` | 1 | `uint8` | 槽252经验；字段策略 Editable |
| `槽253经验` | `0x3F6` | 1 | `uint8` | 槽253经验；字段策略 Editable |
| `槽254经验` | `0x3FA` | 1 | `uint8` | 槽254经验；字段策略 Editable |
| `槽255经验` | `0x3FE` | 1 | `uint8` | 槽255经验；字段策略 Editable |
| `槽0剩余回合` | `0x3` | 1 | `uint8` | 槽0剩余回合；字段策略 Editable |
| `槽1剩余回合` | `0x7` | 1 | `uint8` | 槽1剩余回合；字段策略 Editable |
| `槽2剩余回合` | `0xB` | 1 | `uint8` | 槽2剩余回合；字段策略 Editable |
| `槽3剩余回合` | `0xF` | 1 | `uint8` | 槽3剩余回合；字段策略 Editable |
| `槽4剩余回合` | `0x13` | 1 | `uint8` | 槽4剩余回合；字段策略 Editable |
| `槽5剩余回合` | `0x17` | 1 | `uint8` | 槽5剩余回合；字段策略 Editable |
| `槽6剩余回合` | `0x1B` | 1 | `uint8` | 槽6剩余回合；字段策略 Editable |
| `槽7剩余回合` | `0x1F` | 1 | `uint8` | 槽7剩余回合；字段策略 Editable |
| `槽8剩余回合` | `0x23` | 1 | `uint8` | 槽8剩余回合；字段策略 Editable |
| `槽9剩余回合` | `0x27` | 1 | `uint8` | 槽9剩余回合；字段策略 Editable |
| `槽10剩余回合` | `0x2B` | 1 | `uint8` | 槽10剩余回合；字段策略 Editable |
| `槽11剩余回合` | `0x2F` | 1 | `uint8` | 槽11剩余回合；字段策略 Editable |
| `槽12剩余回合` | `0x33` | 1 | `uint8` | 槽12剩余回合；字段策略 Editable |
| `槽13剩余回合` | `0x37` | 1 | `uint8` | 槽13剩余回合；字段策略 Editable |
| `槽14剩余回合` | `0x3B` | 1 | `uint8` | 槽14剩余回合；字段策略 Editable |
| `槽15剩余回合` | `0x3F` | 1 | `uint8` | 槽15剩余回合；字段策略 Editable |
| `槽16剩余回合` | `0x43` | 1 | `uint8` | 槽16剩余回合；字段策略 Editable |
| `槽17剩余回合` | `0x47` | 1 | `uint8` | 槽17剩余回合；字段策略 Editable |
| `槽18剩余回合` | `0x4B` | 1 | `uint8` | 槽18剩余回合；字段策略 Editable |
| `槽19剩余回合` | `0x4F` | 1 | `uint8` | 槽19剩余回合；字段策略 Editable |
| `槽20剩余回合` | `0x53` | 1 | `uint8` | 槽20剩余回合；字段策略 Editable |
| `槽21剩余回合` | `0x57` | 1 | `uint8` | 槽21剩余回合；字段策略 Editable |
| `槽22剩余回合` | `0x5B` | 1 | `uint8` | 槽22剩余回合；字段策略 Editable |
| `槽23剩余回合` | `0x5F` | 1 | `uint8` | 槽23剩余回合；字段策略 Editable |
| `槽24剩余回合` | `0x63` | 1 | `uint8` | 槽24剩余回合；字段策略 Editable |
| `槽25剩余回合` | `0x67` | 1 | `uint8` | 槽25剩余回合；字段策略 Editable |
| `槽26剩余回合` | `0x6B` | 1 | `uint8` | 槽26剩余回合；字段策略 Editable |
| `槽27剩余回合` | `0x6F` | 1 | `uint8` | 槽27剩余回合；字段策略 Editable |
| `槽28剩余回合` | `0x73` | 1 | `uint8` | 槽28剩余回合；字段策略 Editable |
| `槽29剩余回合` | `0x77` | 1 | `uint8` | 槽29剩余回合；字段策略 Editable |
| `槽30剩余回合` | `0x7B` | 1 | `uint8` | 槽30剩余回合；字段策略 Editable |
| `槽31剩余回合` | `0x7F` | 1 | `uint8` | 槽31剩余回合；字段策略 Editable |
| `槽32剩余回合` | `0x83` | 1 | `uint8` | 槽32剩余回合；字段策略 Editable |
| `槽33剩余回合` | `0x87` | 1 | `uint8` | 槽33剩余回合；字段策略 Editable |
| `槽34剩余回合` | `0x8B` | 1 | `uint8` | 槽34剩余回合；字段策略 Editable |
| `槽35剩余回合` | `0x8F` | 1 | `uint8` | 槽35剩余回合；字段策略 Editable |
| `槽36剩余回合` | `0x93` | 1 | `uint8` | 槽36剩余回合；字段策略 Editable |
| `槽37剩余回合` | `0x97` | 1 | `uint8` | 槽37剩余回合；字段策略 Editable |
| `槽38剩余回合` | `0x9B` | 1 | `uint8` | 槽38剩余回合；字段策略 Editable |
| `槽39剩余回合` | `0x9F` | 1 | `uint8` | 槽39剩余回合；字段策略 Editable |
| `槽40剩余回合` | `0xA3` | 1 | `uint8` | 槽40剩余回合；字段策略 Editable |
| `槽41剩余回合` | `0xA7` | 1 | `uint8` | 槽41剩余回合；字段策略 Editable |
| `槽42剩余回合` | `0xAB` | 1 | `uint8` | 槽42剩余回合；字段策略 Editable |
| `槽43剩余回合` | `0xAF` | 1 | `uint8` | 槽43剩余回合；字段策略 Editable |
| `槽44剩余回合` | `0xB3` | 1 | `uint8` | 槽44剩余回合；字段策略 Editable |
| `槽45剩余回合` | `0xB7` | 1 | `uint8` | 槽45剩余回合；字段策略 Editable |
| `槽46剩余回合` | `0xBB` | 1 | `uint8` | 槽46剩余回合；字段策略 Editable |
| `槽47剩余回合` | `0xBF` | 1 | `uint8` | 槽47剩余回合；字段策略 Editable |
| `槽48剩余回合` | `0xC3` | 1 | `uint8` | 槽48剩余回合；字段策略 Editable |
| `槽49剩余回合` | `0xC7` | 1 | `uint8` | 槽49剩余回合；字段策略 Editable |
| `槽50剩余回合` | `0xCB` | 1 | `uint8` | 槽50剩余回合；字段策略 Editable |
| `槽51剩余回合` | `0xCF` | 1 | `uint8` | 槽51剩余回合；字段策略 Editable |
| `槽52剩余回合` | `0xD3` | 1 | `uint8` | 槽52剩余回合；字段策略 Editable |
| `槽53剩余回合` | `0xD7` | 1 | `uint8` | 槽53剩余回合；字段策略 Editable |
| `槽54剩余回合` | `0xDB` | 1 | `uint8` | 槽54剩余回合；字段策略 Editable |
| `槽55剩余回合` | `0xDF` | 1 | `uint8` | 槽55剩余回合；字段策略 Editable |
| `槽56剩余回合` | `0xE3` | 1 | `uint8` | 槽56剩余回合；字段策略 Editable |
| `槽57剩余回合` | `0xE7` | 1 | `uint8` | 槽57剩余回合；字段策略 Editable |
| `槽58剩余回合` | `0xEB` | 1 | `uint8` | 槽58剩余回合；字段策略 Editable |
| `槽59剩余回合` | `0xEF` | 1 | `uint8` | 槽59剩余回合；字段策略 Editable |
| `槽60剩余回合` | `0xF3` | 1 | `uint8` | 槽60剩余回合；字段策略 Editable |
| `槽61剩余回合` | `0xF7` | 1 | `uint8` | 槽61剩余回合；字段策略 Editable |
| `槽62剩余回合` | `0xFB` | 1 | `uint8` | 槽62剩余回合；字段策略 Editable |
| `槽63剩余回合` | `0xFF` | 1 | `uint8` | 槽63剩余回合；字段策略 Editable |
| `槽64剩余回合` | `0x103` | 1 | `uint8` | 槽64剩余回合；字段策略 Editable |
| `槽65剩余回合` | `0x107` | 1 | `uint8` | 槽65剩余回合；字段策略 Editable |
| `槽66剩余回合` | `0x10B` | 1 | `uint8` | 槽66剩余回合；字段策略 Editable |
| `槽67剩余回合` | `0x10F` | 1 | `uint8` | 槽67剩余回合；字段策略 Editable |
| `槽68剩余回合` | `0x113` | 1 | `uint8` | 槽68剩余回合；字段策略 Editable |
| `槽69剩余回合` | `0x117` | 1 | `uint8` | 槽69剩余回合；字段策略 Editable |
| `槽70剩余回合` | `0x11B` | 1 | `uint8` | 槽70剩余回合；字段策略 Editable |
| `槽71剩余回合` | `0x11F` | 1 | `uint8` | 槽71剩余回合；字段策略 Editable |
| `槽72剩余回合` | `0x123` | 1 | `uint8` | 槽72剩余回合；字段策略 Editable |
| `槽73剩余回合` | `0x127` | 1 | `uint8` | 槽73剩余回合；字段策略 Editable |
| `槽74剩余回合` | `0x12B` | 1 | `uint8` | 槽74剩余回合；字段策略 Editable |
| `槽75剩余回合` | `0x12F` | 1 | `uint8` | 槽75剩余回合；字段策略 Editable |
| `槽76剩余回合` | `0x133` | 1 | `uint8` | 槽76剩余回合；字段策略 Editable |
| `槽77剩余回合` | `0x137` | 1 | `uint8` | 槽77剩余回合；字段策略 Editable |
| `槽78剩余回合` | `0x13B` | 1 | `uint8` | 槽78剩余回合；字段策略 Editable |
| `槽79剩余回合` | `0x13F` | 1 | `uint8` | 槽79剩余回合；字段策略 Editable |
| `槽80剩余回合` | `0x143` | 1 | `uint8` | 槽80剩余回合；字段策略 Editable |
| `槽81剩余回合` | `0x147` | 1 | `uint8` | 槽81剩余回合；字段策略 Editable |
| `槽82剩余回合` | `0x14B` | 1 | `uint8` | 槽82剩余回合；字段策略 Editable |
| `槽83剩余回合` | `0x14F` | 1 | `uint8` | 槽83剩余回合；字段策略 Editable |
| `槽84剩余回合` | `0x153` | 1 | `uint8` | 槽84剩余回合；字段策略 Editable |
| `槽85剩余回合` | `0x157` | 1 | `uint8` | 槽85剩余回合；字段策略 Editable |
| `槽86剩余回合` | `0x15B` | 1 | `uint8` | 槽86剩余回合；字段策略 Editable |
| `槽87剩余回合` | `0x15F` | 1 | `uint8` | 槽87剩余回合；字段策略 Editable |
| `槽88剩余回合` | `0x163` | 1 | `uint8` | 槽88剩余回合；字段策略 Editable |
| `槽89剩余回合` | `0x167` | 1 | `uint8` | 槽89剩余回合；字段策略 Editable |
| `槽90剩余回合` | `0x16B` | 1 | `uint8` | 槽90剩余回合；字段策略 Editable |
| `槽91剩余回合` | `0x16F` | 1 | `uint8` | 槽91剩余回合；字段策略 Editable |
| `槽92剩余回合` | `0x173` | 1 | `uint8` | 槽92剩余回合；字段策略 Editable |
| `槽93剩余回合` | `0x177` | 1 | `uint8` | 槽93剩余回合；字段策略 Editable |
| `槽94剩余回合` | `0x17B` | 1 | `uint8` | 槽94剩余回合；字段策略 Editable |
| `槽95剩余回合` | `0x17F` | 1 | `uint8` | 槽95剩余回合；字段策略 Editable |
| `槽96剩余回合` | `0x183` | 1 | `uint8` | 槽96剩余回合；字段策略 Editable |
| `槽97剩余回合` | `0x187` | 1 | `uint8` | 槽97剩余回合；字段策略 Editable |
| `槽98剩余回合` | `0x18B` | 1 | `uint8` | 槽98剩余回合；字段策略 Editable |
| `槽99剩余回合` | `0x18F` | 1 | `uint8` | 槽99剩余回合；字段策略 Editable |
| `槽100剩余回合` | `0x193` | 1 | `uint8` | 槽100剩余回合；字段策略 Editable |
| `槽101剩余回合` | `0x197` | 1 | `uint8` | 槽101剩余回合；字段策略 Editable |
| `槽102剩余回合` | `0x19B` | 1 | `uint8` | 槽102剩余回合；字段策略 Editable |
| `槽103剩余回合` | `0x19F` | 1 | `uint8` | 槽103剩余回合；字段策略 Editable |
| `槽104剩余回合` | `0x1A3` | 1 | `uint8` | 槽104剩余回合；字段策略 Editable |
| `槽105剩余回合` | `0x1A7` | 1 | `uint8` | 槽105剩余回合；字段策略 Editable |
| `槽106剩余回合` | `0x1AB` | 1 | `uint8` | 槽106剩余回合；字段策略 Editable |
| `槽107剩余回合` | `0x1AF` | 1 | `uint8` | 槽107剩余回合；字段策略 Editable |
| `槽108剩余回合` | `0x1B3` | 1 | `uint8` | 槽108剩余回合；字段策略 Editable |
| `槽109剩余回合` | `0x1B7` | 1 | `uint8` | 槽109剩余回合；字段策略 Editable |
| `槽110剩余回合` | `0x1BB` | 1 | `uint8` | 槽110剩余回合；字段策略 Editable |
| `槽111剩余回合` | `0x1BF` | 1 | `uint8` | 槽111剩余回合；字段策略 Editable |
| `槽112剩余回合` | `0x1C3` | 1 | `uint8` | 槽112剩余回合；字段策略 Editable |
| `槽113剩余回合` | `0x1C7` | 1 | `uint8` | 槽113剩余回合；字段策略 Editable |
| `槽114剩余回合` | `0x1CB` | 1 | `uint8` | 槽114剩余回合；字段策略 Editable |
| `槽115剩余回合` | `0x1CF` | 1 | `uint8` | 槽115剩余回合；字段策略 Editable |
| `槽116剩余回合` | `0x1D3` | 1 | `uint8` | 槽116剩余回合；字段策略 Editable |
| `槽117剩余回合` | `0x1D7` | 1 | `uint8` | 槽117剩余回合；字段策略 Editable |
| `槽118剩余回合` | `0x1DB` | 1 | `uint8` | 槽118剩余回合；字段策略 Editable |
| `槽119剩余回合` | `0x1DF` | 1 | `uint8` | 槽119剩余回合；字段策略 Editable |
| `槽120剩余回合` | `0x1E3` | 1 | `uint8` | 槽120剩余回合；字段策略 Editable |
| `槽121剩余回合` | `0x1E7` | 1 | `uint8` | 槽121剩余回合；字段策略 Editable |
| `槽122剩余回合` | `0x1EB` | 1 | `uint8` | 槽122剩余回合；字段策略 Editable |
| `槽123剩余回合` | `0x1EF` | 1 | `uint8` | 槽123剩余回合；字段策略 Editable |
| `槽124剩余回合` | `0x1F3` | 1 | `uint8` | 槽124剩余回合；字段策略 Editable |
| `槽125剩余回合` | `0x1F7` | 1 | `uint8` | 槽125剩余回合；字段策略 Editable |
| `槽126剩余回合` | `0x1FB` | 1 | `uint8` | 槽126剩余回合；字段策略 Editable |
| `槽127剩余回合` | `0x1FF` | 1 | `uint8` | 槽127剩余回合；字段策略 Editable |
| `槽128剩余回合` | `0x203` | 1 | `uint8` | 槽128剩余回合；字段策略 Editable |
| `槽129剩余回合` | `0x207` | 1 | `uint8` | 槽129剩余回合；字段策略 Editable |
| `槽130剩余回合` | `0x20B` | 1 | `uint8` | 槽130剩余回合；字段策略 Editable |
| `槽131剩余回合` | `0x20F` | 1 | `uint8` | 槽131剩余回合；字段策略 Editable |
| `槽132剩余回合` | `0x213` | 1 | `uint8` | 槽132剩余回合；字段策略 Editable |
| `槽133剩余回合` | `0x217` | 1 | `uint8` | 槽133剩余回合；字段策略 Editable |
| `槽134剩余回合` | `0x21B` | 1 | `uint8` | 槽134剩余回合；字段策略 Editable |
| `槽135剩余回合` | `0x21F` | 1 | `uint8` | 槽135剩余回合；字段策略 Editable |
| `槽136剩余回合` | `0x223` | 1 | `uint8` | 槽136剩余回合；字段策略 Editable |
| `槽137剩余回合` | `0x227` | 1 | `uint8` | 槽137剩余回合；字段策略 Editable |
| `槽138剩余回合` | `0x22B` | 1 | `uint8` | 槽138剩余回合；字段策略 Editable |
| `槽139剩余回合` | `0x22F` | 1 | `uint8` | 槽139剩余回合；字段策略 Editable |
| `槽140剩余回合` | `0x233` | 1 | `uint8` | 槽140剩余回合；字段策略 Editable |
| `槽141剩余回合` | `0x237` | 1 | `uint8` | 槽141剩余回合；字段策略 Editable |
| `槽142剩余回合` | `0x23B` | 1 | `uint8` | 槽142剩余回合；字段策略 Editable |
| `槽143剩余回合` | `0x23F` | 1 | `uint8` | 槽143剩余回合；字段策略 Editable |
| `槽144剩余回合` | `0x243` | 1 | `uint8` | 槽144剩余回合；字段策略 Editable |
| `槽145剩余回合` | `0x247` | 1 | `uint8` | 槽145剩余回合；字段策略 Editable |
| `槽146剩余回合` | `0x24B` | 1 | `uint8` | 槽146剩余回合；字段策略 Editable |
| `槽147剩余回合` | `0x24F` | 1 | `uint8` | 槽147剩余回合；字段策略 Editable |
| `槽148剩余回合` | `0x253` | 1 | `uint8` | 槽148剩余回合；字段策略 Editable |
| `槽149剩余回合` | `0x257` | 1 | `uint8` | 槽149剩余回合；字段策略 Editable |
| `槽150剩余回合` | `0x25B` | 1 | `uint8` | 槽150剩余回合；字段策略 Editable |
| `槽151剩余回合` | `0x25F` | 1 | `uint8` | 槽151剩余回合；字段策略 Editable |
| `槽152剩余回合` | `0x263` | 1 | `uint8` | 槽152剩余回合；字段策略 Editable |
| `槽153剩余回合` | `0x267` | 1 | `uint8` | 槽153剩余回合；字段策略 Editable |
| `槽154剩余回合` | `0x26B` | 1 | `uint8` | 槽154剩余回合；字段策略 Editable |
| `槽155剩余回合` | `0x26F` | 1 | `uint8` | 槽155剩余回合；字段策略 Editable |
| `槽156剩余回合` | `0x273` | 1 | `uint8` | 槽156剩余回合；字段策略 Editable |
| `槽157剩余回合` | `0x277` | 1 | `uint8` | 槽157剩余回合；字段策略 Editable |
| `槽158剩余回合` | `0x27B` | 1 | `uint8` | 槽158剩余回合；字段策略 Editable |
| `槽159剩余回合` | `0x27F` | 1 | `uint8` | 槽159剩余回合；字段策略 Editable |
| `槽160剩余回合` | `0x283` | 1 | `uint8` | 槽160剩余回合；字段策略 Editable |
| `槽161剩余回合` | `0x287` | 1 | `uint8` | 槽161剩余回合；字段策略 Editable |
| `槽162剩余回合` | `0x28B` | 1 | `uint8` | 槽162剩余回合；字段策略 Editable |
| `槽163剩余回合` | `0x28F` | 1 | `uint8` | 槽163剩余回合；字段策略 Editable |
| `槽164剩余回合` | `0x293` | 1 | `uint8` | 槽164剩余回合；字段策略 Editable |
| `槽165剩余回合` | `0x297` | 1 | `uint8` | 槽165剩余回合；字段策略 Editable |
| `槽166剩余回合` | `0x29B` | 1 | `uint8` | 槽166剩余回合；字段策略 Editable |
| `槽167剩余回合` | `0x29F` | 1 | `uint8` | 槽167剩余回合；字段策略 Editable |
| `槽168剩余回合` | `0x2A3` | 1 | `uint8` | 槽168剩余回合；字段策略 Editable |
| `槽169剩余回合` | `0x2A7` | 1 | `uint8` | 槽169剩余回合；字段策略 Editable |
| `槽170剩余回合` | `0x2AB` | 1 | `uint8` | 槽170剩余回合；字段策略 Editable |
| `槽171剩余回合` | `0x2AF` | 1 | `uint8` | 槽171剩余回合；字段策略 Editable |
| `槽172剩余回合` | `0x2B3` | 1 | `uint8` | 槽172剩余回合；字段策略 Editable |
| `槽173剩余回合` | `0x2B7` | 1 | `uint8` | 槽173剩余回合；字段策略 Editable |
| `槽174剩余回合` | `0x2BB` | 1 | `uint8` | 槽174剩余回合；字段策略 Editable |
| `槽175剩余回合` | `0x2BF` | 1 | `uint8` | 槽175剩余回合；字段策略 Editable |
| `槽176剩余回合` | `0x2C3` | 1 | `uint8` | 槽176剩余回合；字段策略 Editable |
| `槽177剩余回合` | `0x2C7` | 1 | `uint8` | 槽177剩余回合；字段策略 Editable |
| `槽178剩余回合` | `0x2CB` | 1 | `uint8` | 槽178剩余回合；字段策略 Editable |
| `槽179剩余回合` | `0x2CF` | 1 | `uint8` | 槽179剩余回合；字段策略 Editable |
| `槽180剩余回合` | `0x2D3` | 1 | `uint8` | 槽180剩余回合；字段策略 Editable |
| `槽181剩余回合` | `0x2D7` | 1 | `uint8` | 槽181剩余回合；字段策略 Editable |
| `槽182剩余回合` | `0x2DB` | 1 | `uint8` | 槽182剩余回合；字段策略 Editable |
| `槽183剩余回合` | `0x2DF` | 1 | `uint8` | 槽183剩余回合；字段策略 Editable |
| `槽184剩余回合` | `0x2E3` | 1 | `uint8` | 槽184剩余回合；字段策略 Editable |
| `槽185剩余回合` | `0x2E7` | 1 | `uint8` | 槽185剩余回合；字段策略 Editable |
| `槽186剩余回合` | `0x2EB` | 1 | `uint8` | 槽186剩余回合；字段策略 Editable |
| `槽187剩余回合` | `0x2EF` | 1 | `uint8` | 槽187剩余回合；字段策略 Editable |
| `槽188剩余回合` | `0x2F3` | 1 | `uint8` | 槽188剩余回合；字段策略 Editable |
| `槽189剩余回合` | `0x2F7` | 1 | `uint8` | 槽189剩余回合；字段策略 Editable |
| `槽190剩余回合` | `0x2FB` | 1 | `uint8` | 槽190剩余回合；字段策略 Editable |
| `槽191剩余回合` | `0x2FF` | 1 | `uint8` | 槽191剩余回合；字段策略 Editable |
| `槽192剩余回合` | `0x303` | 1 | `uint8` | 槽192剩余回合；字段策略 Editable |
| `槽193剩余回合` | `0x307` | 1 | `uint8` | 槽193剩余回合；字段策略 Editable |
| `槽194剩余回合` | `0x30B` | 1 | `uint8` | 槽194剩余回合；字段策略 Editable |
| `槽195剩余回合` | `0x30F` | 1 | `uint8` | 槽195剩余回合；字段策略 Editable |
| `槽196剩余回合` | `0x313` | 1 | `uint8` | 槽196剩余回合；字段策略 Editable |
| `槽197剩余回合` | `0x317` | 1 | `uint8` | 槽197剩余回合；字段策略 Editable |
| `槽198剩余回合` | `0x31B` | 1 | `uint8` | 槽198剩余回合；字段策略 Editable |
| `槽199剩余回合` | `0x31F` | 1 | `uint8` | 槽199剩余回合；字段策略 Editable |
| `槽200剩余回合` | `0x323` | 1 | `uint8` | 槽200剩余回合；字段策略 Editable |
| `槽201剩余回合` | `0x327` | 1 | `uint8` | 槽201剩余回合；字段策略 Editable |
| `槽202剩余回合` | `0x32B` | 1 | `uint8` | 槽202剩余回合；字段策略 Editable |
| `槽203剩余回合` | `0x32F` | 1 | `uint8` | 槽203剩余回合；字段策略 Editable |
| `槽204剩余回合` | `0x333` | 1 | `uint8` | 槽204剩余回合；字段策略 Editable |
| `槽205剩余回合` | `0x337` | 1 | `uint8` | 槽205剩余回合；字段策略 Editable |
| `槽206剩余回合` | `0x33B` | 1 | `uint8` | 槽206剩余回合；字段策略 Editable |
| `槽207剩余回合` | `0x33F` | 1 | `uint8` | 槽207剩余回合；字段策略 Editable |
| `槽208剩余回合` | `0x343` | 1 | `uint8` | 槽208剩余回合；字段策略 Editable |
| `槽209剩余回合` | `0x347` | 1 | `uint8` | 槽209剩余回合；字段策略 Editable |
| `槽210剩余回合` | `0x34B` | 1 | `uint8` | 槽210剩余回合；字段策略 Editable |
| `槽211剩余回合` | `0x34F` | 1 | `uint8` | 槽211剩余回合；字段策略 Editable |
| `槽212剩余回合` | `0x353` | 1 | `uint8` | 槽212剩余回合；字段策略 Editable |
| `槽213剩余回合` | `0x357` | 1 | `uint8` | 槽213剩余回合；字段策略 Editable |
| `槽214剩余回合` | `0x35B` | 1 | `uint8` | 槽214剩余回合；字段策略 Editable |
| `槽215剩余回合` | `0x35F` | 1 | `uint8` | 槽215剩余回合；字段策略 Editable |
| `槽216剩余回合` | `0x363` | 1 | `uint8` | 槽216剩余回合；字段策略 Editable |
| `槽217剩余回合` | `0x367` | 1 | `uint8` | 槽217剩余回合；字段策略 Editable |
| `槽218剩余回合` | `0x36B` | 1 | `uint8` | 槽218剩余回合；字段策略 Editable |
| `槽219剩余回合` | `0x36F` | 1 | `uint8` | 槽219剩余回合；字段策略 Editable |
| `槽220剩余回合` | `0x373` | 1 | `uint8` | 槽220剩余回合；字段策略 Editable |
| `槽221剩余回合` | `0x377` | 1 | `uint8` | 槽221剩余回合；字段策略 Editable |
| `槽222剩余回合` | `0x37B` | 1 | `uint8` | 槽222剩余回合；字段策略 Editable |
| `槽223剩余回合` | `0x37F` | 1 | `uint8` | 槽223剩余回合；字段策略 Editable |
| `槽224剩余回合` | `0x383` | 1 | `uint8` | 槽224剩余回合；字段策略 Editable |
| `槽225剩余回合` | `0x387` | 1 | `uint8` | 槽225剩余回合；字段策略 Editable |
| `槽226剩余回合` | `0x38B` | 1 | `uint8` | 槽226剩余回合；字段策略 Editable |
| `槽227剩余回合` | `0x38F` | 1 | `uint8` | 槽227剩余回合；字段策略 Editable |
| `槽228剩余回合` | `0x393` | 1 | `uint8` | 槽228剩余回合；字段策略 Editable |
| `槽229剩余回合` | `0x397` | 1 | `uint8` | 槽229剩余回合；字段策略 Editable |
| `槽230剩余回合` | `0x39B` | 1 | `uint8` | 槽230剩余回合；字段策略 Editable |
| `槽231剩余回合` | `0x39F` | 1 | `uint8` | 槽231剩余回合；字段策略 Editable |
| `槽232剩余回合` | `0x3A3` | 1 | `uint8` | 槽232剩余回合；字段策略 Editable |
| `槽233剩余回合` | `0x3A7` | 1 | `uint8` | 槽233剩余回合；字段策略 Editable |
| `槽234剩余回合` | `0x3AB` | 1 | `uint8` | 槽234剩余回合；字段策略 Editable |
| `槽235剩余回合` | `0x3AF` | 1 | `uint8` | 槽235剩余回合；字段策略 Editable |
| `槽236剩余回合` | `0x3B3` | 1 | `uint8` | 槽236剩余回合；字段策略 Editable |
| `槽237剩余回合` | `0x3B7` | 1 | `uint8` | 槽237剩余回合；字段策略 Editable |
| `槽238剩余回合` | `0x3BB` | 1 | `uint8` | 槽238剩余回合；字段策略 Editable |
| `槽239剩余回合` | `0x3BF` | 1 | `uint8` | 槽239剩余回合；字段策略 Editable |
| `槽240剩余回合` | `0x3C3` | 1 | `uint8` | 槽240剩余回合；字段策略 Editable |
| `槽241剩余回合` | `0x3C7` | 1 | `uint8` | 槽241剩余回合；字段策略 Editable |
| `槽242剩余回合` | `0x3CB` | 1 | `uint8` | 槽242剩余回合；字段策略 Editable |
| `槽243剩余回合` | `0x3CF` | 1 | `uint8` | 槽243剩余回合；字段策略 Editable |
| `槽244剩余回合` | `0x3D3` | 1 | `uint8` | 槽244剩余回合；字段策略 Editable |
| `槽245剩余回合` | `0x3D7` | 1 | `uint8` | 槽245剩余回合；字段策略 Editable |
| `槽246剩余回合` | `0x3DB` | 1 | `uint8` | 槽246剩余回合；字段策略 Editable |
| `槽247剩余回合` | `0x3DF` | 1 | `uint8` | 槽247剩余回合；字段策略 Editable |
| `槽248剩余回合` | `0x3E3` | 1 | `uint8` | 槽248剩余回合；字段策略 Editable |
| `槽249剩余回合` | `0x3E7` | 1 | `uint8` | 槽249剩余回合；字段策略 Editable |
| `槽250剩余回合` | `0x3EB` | 1 | `uint8` | 槽250剩余回合；字段策略 Editable |
| `槽251剩余回合` | `0x3EF` | 1 | `uint8` | 槽251剩余回合；字段策略 Editable |
| `槽252剩余回合` | `0x3F3` | 1 | `uint8` | 槽252剩余回合；字段策略 Editable |
| `槽253剩余回合` | `0x3F7` | 1 | `uint8` | 槽253剩余回合；字段策略 Editable |
| `槽254剩余回合` | `0x3FB` | 1 | `uint8` | 槽254剩余回合；字段策略 Editable |
| `槽255剩余回合` | `0x3FF` | 1 | `uint8` | 槽255剩余回合；字段策略 Editable |

## 66-shanzhai-legacy 特效成长拓展（effect-messages 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.effect-messages`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x8` (8)

索引公式: `Effectmsg.e5 + 0x0 + (ID - 0) * 0x8 + field_offset; ID=0..254`

存储：`Effectmsg.e5`；起点：`0x0` (fileOffset)；记录数：`255`；ID 起点：`0`；结束偏移（不含）：`0x7F8`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `Enabled` | `0x0` | 1 | `uint8` | Enabled；字段策略 Editable |
| `Param1` | `0x1` | 1 | `uint8` | Param1；字段策略 Editable |
| `Param2` | `0x2` | 1 | `uint8` | Param2；字段策略 Editable |
| `Param3` | `0x3` | 1 | `uint8` | Param3；字段策略 Editable |
| `Param4` | `0x4` | 1 | `uint8` | Param4；字段策略 Editable |
| `Param5` | `0x5` | 1 | `uint8` | Param5；字段策略 Editable |
| `Param6` | `0x6` | 1 | `uint8` | Param6；字段策略 Editable |
| `Param7` | `0x7` | 1 | `uint8` | Param7；字段策略 Editable |

## 66-shanzhai-legacy 策略学习拓展（strategy-study-extended 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-study-extended`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x40` (64)

索引公式: `MeffStudy.e5 + 0x0 + (ID - 0) * 0x40 + field_offset; ID=0..1023`

存储：`MeffStudy.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x10000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略0ID` | `0x0` | 1 | `uint8` | 策略0ID；字段策略 Editable |
| `策略1ID` | `0x2` | 1 | `uint8` | 策略1ID；字段策略 Editable |
| `策略2ID` | `0x4` | 1 | `uint8` | 策略2ID；字段策略 Editable |
| `策略3ID` | `0x6` | 1 | `uint8` | 策略3ID；字段策略 Editable |
| `策略4ID` | `0x8` | 1 | `uint8` | 策略4ID；字段策略 Editable |
| `策略5ID` | `0xA` | 1 | `uint8` | 策略5ID；字段策略 Editable |
| `策略6ID` | `0xC` | 1 | `uint8` | 策略6ID；字段策略 Editable |
| `策略7ID` | `0xE` | 1 | `uint8` | 策略7ID；字段策略 Editable |
| `策略8ID` | `0x10` | 1 | `uint8` | 策略8ID；字段策略 Editable |
| `策略9ID` | `0x12` | 1 | `uint8` | 策略9ID；字段策略 Editable |
| `策略10ID` | `0x14` | 1 | `uint8` | 策略10ID；字段策略 Editable |
| `策略11ID` | `0x16` | 1 | `uint8` | 策略11ID；字段策略 Editable |
| `策略12ID` | `0x18` | 1 | `uint8` | 策略12ID；字段策略 Editable |
| `策略13ID` | `0x1A` | 1 | `uint8` | 策略13ID；字段策略 Editable |
| `策略14ID` | `0x1C` | 1 | `uint8` | 策略14ID；字段策略 Editable |
| `策略15ID` | `0x1E` | 1 | `uint8` | 策略15ID；字段策略 Editable |
| `策略16ID` | `0x20` | 1 | `uint8` | 策略16ID；字段策略 Editable |
| `策略17ID` | `0x22` | 1 | `uint8` | 策略17ID；字段策略 Editable |
| `策略18ID` | `0x24` | 1 | `uint8` | 策略18ID；字段策略 Editable |
| `策略19ID` | `0x26` | 1 | `uint8` | 策略19ID；字段策略 Editable |
| `策略20ID` | `0x28` | 1 | `uint8` | 策略20ID；字段策略 Editable |
| `策略21ID` | `0x2A` | 1 | `uint8` | 策略21ID；字段策略 Editable |
| `策略22ID` | `0x2C` | 1 | `uint8` | 策略22ID；字段策略 Editable |
| `策略23ID` | `0x2E` | 1 | `uint8` | 策略23ID；字段策略 Editable |
| `策略24ID` | `0x30` | 1 | `uint8` | 策略24ID；字段策略 Editable |
| `策略25ID` | `0x32` | 1 | `uint8` | 策略25ID；字段策略 Editable |
| `策略26ID` | `0x34` | 1 | `uint8` | 策略26ID；字段策略 Editable |
| `策略27ID` | `0x36` | 1 | `uint8` | 策略27ID；字段策略 Editable |
| `策略28ID` | `0x38` | 1 | `uint8` | 策略28ID；字段策略 Editable |
| `策略29ID` | `0x3A` | 1 | `uint8` | 策略29ID；字段策略 Editable |
| `策略30ID` | `0x3C` | 1 | `uint8` | 策略30ID；字段策略 Editable |
| `策略31ID` | `0x3E` | 1 | `uint8` | 策略31ID；字段策略 Editable |
| `策略0次数` | `0x1` | 1 | `uint8` | 策略0次数；字段策略 Editable |
| `策略1次数` | `0x3` | 1 | `uint8` | 策略1次数；字段策略 Editable |
| `策略2次数` | `0x5` | 1 | `uint8` | 策略2次数；字段策略 Editable |
| `策略3次数` | `0x7` | 1 | `uint8` | 策略3次数；字段策略 Editable |
| `策略4次数` | `0x9` | 1 | `uint8` | 策略4次数；字段策略 Editable |
| `策略5次数` | `0xB` | 1 | `uint8` | 策略5次数；字段策略 Editable |
| `策略6次数` | `0xD` | 1 | `uint8` | 策略6次数；字段策略 Editable |
| `策略7次数` | `0xF` | 1 | `uint8` | 策略7次数；字段策略 Editable |
| `策略8次数` | `0x11` | 1 | `uint8` | 策略8次数；字段策略 Editable |
| `策略9次数` | `0x13` | 1 | `uint8` | 策略9次数；字段策略 Editable |
| `策略10次数` | `0x15` | 1 | `uint8` | 策略10次数；字段策略 Editable |
| `策略11次数` | `0x17` | 1 | `uint8` | 策略11次数；字段策略 Editable |
| `策略12次数` | `0x19` | 1 | `uint8` | 策略12次数；字段策略 Editable |
| `策略13次数` | `0x1B` | 1 | `uint8` | 策略13次数；字段策略 Editable |
| `策略14次数` | `0x1D` | 1 | `uint8` | 策略14次数；字段策略 Editable |
| `策略15次数` | `0x1F` | 1 | `uint8` | 策略15次数；字段策略 Editable |
| `策略16次数` | `0x21` | 1 | `uint8` | 策略16次数；字段策略 Editable |
| `策略17次数` | `0x23` | 1 | `uint8` | 策略17次数；字段策略 Editable |
| `策略18次数` | `0x25` | 1 | `uint8` | 策略18次数；字段策略 Editable |
| `策略19次数` | `0x27` | 1 | `uint8` | 策略19次数；字段策略 Editable |
| `策略20次数` | `0x29` | 1 | `uint8` | 策略20次数；字段策略 Editable |
| `策略21次数` | `0x2B` | 1 | `uint8` | 策略21次数；字段策略 Editable |
| `策略22次数` | `0x2D` | 1 | `uint8` | 策略22次数；字段策略 Editable |
| `策略23次数` | `0x2F` | 1 | `uint8` | 策略23次数；字段策略 Editable |
| `策略24次数` | `0x31` | 1 | `uint8` | 策略24次数；字段策略 Editable |
| `策略25次数` | `0x33` | 1 | `uint8` | 策略25次数；字段策略 Editable |
| `策略26次数` | `0x35` | 1 | `uint8` | 策略26次数；字段策略 Editable |
| `策略27次数` | `0x37` | 1 | `uint8` | 策略27次数；字段策略 Editable |
| `策略28次数` | `0x39` | 1 | `uint8` | 策略28次数；字段策略 Editable |
| `策略29次数` | `0x3B` | 1 | `uint8` | 策略29次数；字段策略 Editable |
| `策略30次数` | `0x3D` | 1 | `uint8` | 策略30次数；字段策略 Editable |
| `策略31次数` | `0x3F` | 1 | `uint8` | 策略31次数；字段策略 Editable |

## 66-shanzhai-legacy 锻造（forge 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.forge`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x40` (64)

索引公式: `Forge.e5 + 0x0 + (ID - 0) * 0x40 + field_offset; ID=0..1023`

存储：`Forge.e5`；起点：`0x0` (fileOffset)；记录数：`1024`；ID 起点：`0`；结束偏移（不含）：`0x10000`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 30 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `材料1ID` | `0x1E` | 2 | `uint16le` | 材料1ID；字段策略 Editable |
| `材料2ID` | `0x21` | 2 | `uint16le` | 材料2ID；字段策略 Editable |
| `材料3ID` | `0x24` | 2 | `uint16le` | 材料3ID；字段策略 Editable |
| `材料4ID` | `0x27` | 2 | `uint16le` | 材料4ID；字段策略 Editable |
| `材料5ID` | `0x2A` | 2 | `uint16le` | 材料5ID；字段策略 Editable |
| `材料6ID` | `0x2D` | 2 | `uint16le` | 材料6ID；字段策略 Editable |
| `材料7ID` | `0x30` | 2 | `uint16le` | 材料7ID；字段策略 Editable |
| `材料8ID` | `0x33` | 2 | `uint16le` | 材料8ID；字段策略 Editable |
| `材料1数量` | `0x20` | 1 | `uint8` | 材料1数量；字段策略 Editable |
| `材料2数量` | `0x23` | 1 | `uint8` | 材料2数量；字段策略 Editable |
| `材料3数量` | `0x26` | 1 | `uint8` | 材料3数量；字段策略 Editable |
| `材料4数量` | `0x29` | 1 | `uint8` | 材料4数量；字段策略 Editable |
| `材料5数量` | `0x2C` | 1 | `uint8` | 材料5数量；字段策略 Editable |
| `材料6数量` | `0x2F` | 1 | `uint8` | 材料6数量；字段策略 Editable |
| `材料7数量` | `0x32` | 1 | `uint8` | 材料7数量；字段策略 Editable |
| `材料8数量` | `0x35` | 1 | `uint8` | 材料8数量；字段策略 Editable |
| `价格` | `0x36` | 4 | `uint32le` | 价格；字段策略 Editable |
| `保留58` | `0x3A` | 1 | `bytes` | 保留58；字段策略 Preserve |
| `材料项数` | `0x3A` | 1 | `uint8` | 材料项数；字段策略 Editable |
| `保留59` | `0x3B` | 1 | `bytes` | 保留59；字段策略 Preserve |
| `商店编号` | `0x3B` | 1 | `uint8` | 商店编号；字段策略 Editable |
| `标记` | `0x3C` | 1 | `uint8` | 标记；字段策略 Editable |
| `保留61` | `0x3D` | 1 | `bytes` | 保留61；字段策略 Preserve |
| `剩余次数` | `0x3D` | 1 | `uint8` | 剩余次数；字段策略 Editable |

## 66-shanzhai-legacy 策略大动画（strategy-big-animation 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-big-animation`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA31F0 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA31F0` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA3280`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `动画ID` | `0x0` | 1 | `uint8` | 动画ID；字段策略 Editable |

## 66-shanzhai-legacy 策略小动画（strategy-small-animation 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-small-animation`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0xA3160 + (ID - 0) * 0x1 + field_offset; ID=0..143`

存储：`Ekd5.exe`；起点：`0xA3160` (fileOffset)；记录数：`144`；ID 起点：`0`；结束偏移（不含）：`0xA31F0`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `动画ID` | `0x0` | 1 | `uint8` | 动画ID；字段策略 Editable |

## 66-shanzhai-legacy 兵种系·辅助装备分组（job-series-accessory-groups 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.job-series-accessory-groups`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `不解析占位 offset=0；实际地址由 VA 0x0044C341 经目标 PE 节表映射；参见 format.65.accessory-job-groups`

存储：`Ekd5.exe`；起点：-；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x1`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 辅助分组不是定长物理表；请在兵种系的辅助分组业务页使用 PE 地址/FF 分隔专用服务及专用 CSV。禁止解码此占位偏移或导出 EXE 文件头。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `Raw` | `0x0` | 1 | `bytes` | Raw；字段策略 Preserve |

## 66-shanzhai-legacy 策略施展地形（strategy-terrain-availability 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.strategy-terrain-availability`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x1` (1)

索引公式: `Ekd5.exe + 0x1FECC + (ID - 0) * 0x1 + field_offset; ID=0..29`

存储：`Ekd5.exe`；起点：`0x1FECC` (fileOffset)；记录数：`30`；ID 起点：`0`；结束偏移（不含）：`0x1FEEA`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。
- 静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `策略施展地形掩码` | `0x0` | 1 | `uint8` | 策略施展地形掩码；字段策略 Editable |

## 66-shanzhai-legacy 装备特效名称池（1A-57）（item-effect-names-low 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-effect-names-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x375` (885)

索引公式: `Ekd5.exe + 0x8A9E8 + (ID - 0) * 0x375 + field_offset; ID=0..0`

存储：`Ekd5.exe`；起点：`0x8A9E8` (fileOffset)；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x8AD5D`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 装备特效名称使用 item-effect-names-66 固定 16 字节名称池，禁止读取或写入 6.5 低段变长池偏移。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `RawHex` | `0x0` | 885 | `bytes` | RawHex；字段策略 Preserve |

## 66-shanzhai-legacy 装备特效名称池（58-7F）（item-effect-names-high 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-effect-names-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x170` (368)

索引公式: `Ekd5.exe + 0x9F800 + (ID - 0) * 0x170 + field_offset; ID=0..0`

存储：`Ekd5.exe`；起点：`0x9F800` (fileOffset)；记录数：`1`；ID 起点：`0`；结束偏移（不含）：`0x9F970`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 装备特效名称使用 item-effect-names-66 固定 16 字节名称池，禁止读取或写入 6.5 高段变长池偏移。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `RawHex` | `0x0` | 368 | `bytes` | RawHex；字段策略 Preserve |

## 66-shanzhai-legacy 必杀（finishing-moves 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.finishing-moves`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Data.e5 + 0xE894 + (ID - 0) * 0x10 + field_offset; ID=0..95`

存储：`Data.e5`；起点：`0xE894` (fileOffset)；记录数：`96`；ID 起点：`0`；结束偏移（不含）：`0xEE94`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 11 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `图标` | `0xB` | 1 | `bytes` | 图标；字段策略 Preserve |
| `攻击范围` | `0xC` | 1 | `uint8` | 攻击范围；字段策略 Editable |
| `穿透范围` | `0xD` | 1 | `uint8` | 穿透范围；字段策略 Editable |
| `消耗SP` | `0xE` | 1 | `uint8` | 消耗SP；字段策略 Editable |

## 66-shanzhai-legacy 必杀说明（finishing-move-description 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.finishing-move-description`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x7080 + (ID - 0) * 0xC8 + field_offset; ID=0..95`

存储：`Imsg.e5`；起点：`0x7080` (fileOffset)；记录数：`96`；ID 起点：`0`；结束偏移（不含）：`0xBB80`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `说明` | `0x0` | 200 | `fixed-string` | 说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 物品获取说明（0-103）（item-acquisition-low 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-acquisition-low`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x6B5F8 + (ID - 0) * 0xC8 + field_offset; ID=0..103`

存储：`Imsg.e5`；起点：`0x6B5F8` (fileOffset)；记录数：`104`；ID 起点：`0`；结束偏移（不含）：`0x70738`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 旧 HexTable.xml 明确 Enable=false；Imsg 6.5 基底长度不足，且区域与物品说明/撤退区重叠。未取得消费代码前禁止读取或写回。
- 旧 HexTable.xml 的 Enable=false；6.5 文件边界不足，6.6 旧区域与宝物说明/撤退区域冲突且未确认消费引用，禁止读取或写入。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `物品获取说明` | `0x0` | 200 | `fixed-string` | 物品获取说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 物品获取说明（104-199）（item-acquisition-high 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-acquisition-high`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Imsg.e5 + 0x70738 + (ID - 104) * 0xC8 + field_offset; ID=104..199`

存储：`Imsg.e5`；起点：`0x70738` (fileOffset)；记录数：`96`；ID 起点：`104`；结束偏移（不含）：`0x75238`。

能力：`Unavailable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 旧 HexTable.xml 明确 Enable=false；高段区域与低段获取说明/撤退区存在重叠语义，未取得消费代码前禁止读取或写回。
- 旧 HexTable.xml 的 Enable=false；6.5 文件边界不足，6.6 旧区域与宝物说明/撤退区域冲突且未确认消费引用，禁止读取或写入。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `物品获取说明` | `0x0` | 200 | `fixed-string` | 物品获取说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 宝物扩展（256-511）（items-extended 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.items-extended`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x19` (25)

索引公式: `Item.e5 + 0x0 + (ID - 256) * 0x19 + field_offset; ID=256..511`

存储：`Item.e5`；起点：`0x0` (fileOffset)；记录数：`256`；ID 起点：`256`；结束偏移（不含）：`0x1900`。

能力：`Editable`；Codec：`item-65-17-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。
- 15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 17 | `fixed-string` | 名称；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |
| `宝物类型` | `0x11` | 1 | `uint8` | 宝物类型；字段策略 Editable；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `装备特效号` | `0x12` | 1 | `uint8` | 装备特效号；字段策略 Editable；引用 effect-names；此为逻辑字段，6.6 15 字节 Codec 可根据原始 +0x12=2/3 交换实际写入位置，见专用 Codec 契约；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。 |
| `价格（/100）` | `0x13` | 1 | `uint8` | 价格（/100）；字段策略 Editable；价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。 |
| `图标` | `0x14` | 1 | `uint8` | 图标；字段策略 Editable；本 Variant 使用 +0x14 UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始 |
| `初始能力` | `0x15` | 1 | `uint8` | 初始能力；字段策略 Editable；物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。 |
| `装备特效值` | `0x16` | 1 | `uint8` | 装备特效值；字段策略 Editable；物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。 |
| `能力成长` | `0x17` | 1 | `uint8` | 能力成长；字段策略 Editable；物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。 |
| `宝物图鉴` | `0x18` | 1 | `uint8` | 宝物图鉴；字段策略 Editable；图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。 |

## 66-shanzhai-legacy 宝物扩展说明（256-511）（item-description-extended 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-description-extended`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0xC8` (200)

索引公式: `Itemmsg.e5 + 0x0 + (ID - 256) * 0xC8 + field_offset; ID=256..511`

存储：`Itemmsg.e5`；起点：`0x0` (fileOffset)；记录数：`256`；ID 起点：`256`；结束偏移（不含）：`0xC800`。

能力：`Editable`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | - | - | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `宝物说明` | `0x0` | 200 | `fixed-string` | 宝物说明；字段策略 Editable；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 装备特效名称池（6.6，1A-FF）（item-effect-names-66 物理表）

ID: `struct.66.disk.66-shanzhai-legacy.item-effect-names-66`；状态: `candidate`；证据: `inherited-or-unavailable-source-layout`

步长: `0x10` (16)

索引公式: `Ekd5.exe + 0x9D9A0 + (ID - 26) * 0x10 + field_offset; ID=26..255`

存储：`Ekd5.exe`；起点：`0x9D9A0` (fileOffset)；记录数：`230`；ID 起点：`26`；结束偏移（不含）：`0x9E800`。

能力：`ReadOnly`；Codec：`fixed-record-v1`；字节序：`little`；编码：`GBK for strings`。

- 物理文件布局和运行时内存记录是不同实体。
- canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。

写入门禁：

- 不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。
- 文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。
- 仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。
- 提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。
- 6.6 固定 16 字节名称池，专用名称池服务负责解析/写入，物理页只读。

| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |
|---|---:|---|---|
| 旧工具登记山贼样本 | 1146880 | True | `-` |

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 16 | `fixed-string` | 名称；字段策略 ReadOnly；GBK，零终止或固定宽度填充，不允许截断多字节字符 |

## 66-shanzhai-legacy 特殊暴击人物分配（动态物理表）

ID: `struct.66.disk.66-shanzhai-legacy.person-critical-special-map`；状态: `candidate`；证据: `source-reviewed-pe-reference-gated`

步长: `0x4` (4)

索引公式: `Ekd5.exe + 0x89C30 + specialSlot * 4; specialSlot=0..20; Imsg.e5 quoteOffset=140000 + specialSlot*200`

存储：`Ekd5.exe`；起点：`0x89C30` (fileOffset)；记录数：`21`；ID 起点：`0`；结束偏移（不含）：`0x89C84`。

能力：`RuntimeProbeRequired`；Codec：`fixed-record-v1`；字节序：`little`；编码：`not applicable`。

写入门禁：

- 需验证目标 PE 可执行区对该区域的引用、21 个 UInt32 值和文件边界；不能只检查原始固定偏移。
- 普通模式清空此人物所有特殊槽到 1024，再写普通类型 0..25 和三句共享台词。
- 特殊模式保持普通类型作为回退；绑定所选槽并清除本人物其它特殊槽；被其它人物占用时先预览并显式覆盖。
- 模式、绑定、人物字段和 Imsg 文本一次跨表事务提交；任何校验失败不产生部分草稿。

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `人物ID` | `0x0` | 4 | `uint32le` | 绑定人物 ID 0..1023，1024 为空槽；数值不是 Imsg 行号，记录主键 ID/槽号才对应特殊台词行。 |

## F36 人物运行时记录

ID: `struct.66.f36.character-record`；状态: `canonical`；证据: `static-verified`

步长: `0x48` (72)

索引公式: `DWORD[0x004CEA00] + data_id * 0x48 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `record_key_low12` | `0x0` | 2 | `uint16` | 当前转换函数使用的记录键低 12 位 |
| `job_id` | `0x2B` | 1 | `uint8` | 当前样本转换链读取的兵种字段 |

## F36 战场单位记录

ID: `struct.66.f36.battle-unit-record`；状态: `canonical`；证据: `static-verified`

步长: `0x30` (48)

索引公式: `0x004A7B20 + battlefield_id * 0x30 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `data_id_or_unit_key` | `0x0` | 4 | `uint32` | 当前 0043E4D6 转换循环解引用并比较的首字段；具体编码仍需运行时确认 |

## F36 物品记录

ID: `struct.66.f36.item-record`；状态: `canonical`；证据: `static-verified`

步长: `0x19` (25)

索引公式: `0x0049F820 + item_id * 0x19 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `name` | `0x0` | 15 | `fixed-string` | 名称；编码和终止规则需按资源样本复读 |
| `icon` | `0xF` | 1 | `uint8` | 图标编号 |
| `effect_value` | `0x16` | 1 | `uint8` | 普通装备特效值；辅助保留；消耗品参数高字节。运行时该字段消费仍按原静态证据边界，不推广为所有类别通用效果值。 |

## F36 策略记录

ID: `struct.66.f36.strategy-record`；状态: `canonical`；证据: `static-verified`

步长: `0x61` (97)

索引公式: `0x004A3E77 + strategy_id * 0x61 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `opaque_strategy_payload` | `0x0` | 97 | `opaque-bytes` | 记录步长已由静态乘法确认；字段语义仍需逐项复核 |

## 6.6 宝物按类别解释与字段读写契约

ID: `struct.66.item-category-semantics`；状态: `canonical`；证据: `legacy-source-reviewed-sample-bytes-editor-roundtrip`

步长: `0x19` (25)

索引公式: `row = Data.e5[0x818C + ID*25] for 0<=ID<=103; row = Star.e5[(ID-104)*25] for 104<=ID<=254; field = row + field_offset`

- 本实体说明类别语义；物理文件基址、名称/图标布局和每个Variant的写入门禁由既有物理表实体负责。
- 分类先读取本项目System.ini的DefID/AssID（缺失时70/109），再结合ID区段、当前草稿和Codec类别标记，不能按特效号大小臆测类别。
- 辅助适用兵种的0..39是兵种系编号，名称来自当前项目；它不是detailed-job-growth的26个普通装备许可列。
- 业务名称可变，CSV继续使用原物理列名；固定6.5与动态6.6不能靠相同列名直接复制字节。
- 同表跨类别切换必须更新布局和选项；摘要从草稿按原始类别标记选地址，不能只读OriginalFileBytes。
- 五例绑定当前F36 EXE与B392 Star数据哈希；测试强制66-shanzhai-legacy仅用于相同Codec的字段回归，不证明旧1146880字节EXE画像可写。

写入门禁：

- 源文件SHA、Profile/Variant、25字节行边界和字段范围均通过后，只对主动修改字段生成补丁。
- 已知图鉴/辅助适用兵种/参数可编辑；空或保留字节只在明确的原始字段入口编辑，未修改必须原样保持。
- 6.6名称布局的Preserve字节仍不开放普通字段编辑；类别变化不自动改写保留字节。
- 保存前草稿可整体撤回；保存后按相同Codec复读并逐字节限制变更范围，失败回滚；本契约不证明游戏内效果已经运行。

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `类型或实际特效` | `0x11` | 1 | `uint8` | 普通武器/防具为装备类型；辅助/消耗品为实际特效号。6.6动态Codec以原始+0x12是否2/3决定逻辑列映射。 |
| `特效或类别标记` | `0x12` | 1 | `uint8` | 普通武器/防具为装备特效号；辅助=2、消耗品=3类别标记，不得显示成枪许可或普通装备特效。 |
| `价格` | `0x13` | 1 | `uint8` | 价格单位100；255表示不可买卖。辅助+0x17是适用兵种，不是价格。 |
| `初始属性或辅助效果或参数低字节` | `0x15` | 1 | `uint8` | 武器/防具=初始属性；辅助=特殊效果值；消耗品=LE UInt16参数低字节。原CSV列名初始能力。 |
| `装备效果或保留或参数高字节` | `0x16` | 1 | `uint8` | 武器/防具=特殊效果值；辅助=空/保留；消耗品=参数高字节。原CSV列名装备特效值。 |
| `成长或适用兵种或保留` | `0x17` | 1 | `uint8` | 武器/防具=能力成长；辅助=适用兵种系ID（255=所有兵种）；消耗品=空/保留。原CSV列名能力成长。 |
| `图鉴` | `0x18` | 1 | `uint8` | 图鉴标记。勾选框主动修改写0/1，未主动修改的非零原值保持；不在只读浏览时归一化。 |

样本字段复核：

| ID | 名称 | 特效值 +0x15 | 适用兵种 +0x17 | 价格 +0x13 | 图鉴 +0x18 |
|---:|---|---:|---|---:|---:|
| 154 | 天毒珠 | 1 | 6：侠客 | 255 | 1 |
| 156 | 太平要术 | 5 | 0：君主 | 255 | 1 |
| 157 | 天毒珠（仿） | 60 | 6：侠客 | 255 | 1 |
| 149 | 左氏春秋 | 22 | 255：所有兵种 | 255 | 1 |
| 139 | 凌风赤兔 | 7 | 27：上将 | 255 | 1 |

## 6.6 特效分配记录（4+2）

ID: `struct.66.effect-assignment`；状态: `canonical`；证据: `source-reviewed`

步长: `0x10` (16)

索引公式: `DWORD[resolved effect pointer slot] + effect_id * 0x10 + field_offset`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `character_1` | `0x0` | 2 | `uint16` | 人物 1 |
| `character_value_1` | `0x2` | 1 | `uint8` | 人物 1 特效值 |
| `character_2` | `0x3` | 2 | `uint16` | 人物 2 |
| `character_value_2` | `0x5` | 1 | `uint8` | 人物 2 特效值 |
| `character_3` | `0x6` | 2 | `uint16` | 人物 3 |
| `character_value_3` | `0x8` | 1 | `uint8` | 人物 3 特效值 |
| `character_4` | `0x9` | 2 | `uint16` | 人物 4 |
| `character_value_4` | `0xB` | 1 | `uint8` | 人物 4 特效值 |
| `job_1` | `0xC` | 1 | `uint8` | 兵种 1 |
| `job_value_1` | `0xD` | 1 | `uint8` | 兵种 1 特效值 |
| `job_2` | `0xE` | 1 | `uint8` | 兵种 2 |
| `job_value_2` | `0xF` | 1 | `uint8` | 兵种 2 特效值 |

## 6.6 物品记录

ID: `struct.66.item-record`；状态: `canonical`；证据: `source-reviewed`

步长: `0x19` (25)

索引公式: `Data.e5 + 0x818C + item_id*0x19 for 0..103; Star.e5 + (item_id-104)*0x19 for 104..254; ID255 reserved`

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `name` | `0x0` | 15 | `fixed-string` | 名称 |
| `icon` | `0xF` | 1 | `uint8` | 图标 |
| `effect_or_type` | `0x11` | 1 | `uint8` | 特效或类型 |
| `equipment_effect_or_category` | `0x12` | 1 | `uint8` | 装备特效或类别 |
| `price` | `0x13` | 1 | `uint8` | 价格单位100，255不可买卖。 |
| `ability` | `0x15` | 1 | `uint8` | 普通装备初始属性；辅助特效值；消耗品参数低字节；按类别解释。 |
| `effect_value` | `0x16` | 1 | `uint8` | 普通装备特效值；辅助保留；消耗品参数高字节。运行时该字段消费仍按原静态证据边界，不推广为所有类别通用效果值。 |
| `growth` | `0x17` | 1 | `uint8` | 普通装备成长；辅助适用兵种；消耗品保留。 |
| `catalog_flag` | `0x18` | 1 | `uint8` | 图鉴/宝物标志 |
