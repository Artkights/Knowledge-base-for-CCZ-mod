# 6.5 文件格式

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/file-formats/binary-formats.json`、`6.5/data/file-formats/data-manager-formats.json`

## E5 索引资源封包

ID: `format.e5.indexed-archive`；状态: `canonical`；证据: `source-reviewed`

字节序: `big for directory fields`

目录项字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `stored_length` | `0x0` | 4 | `uint32be` | 封包中实际字节数 |
| `decoded_length` | `0x4` | 4 | `uint32be` | 解码后字节数 |
| `payload_offset` | `0x8` | 4 | `uint32be` | 相对文件开头的负载偏移 |

- stored_length != decoded_length 表示 LS12 压缩
- 首项 payload_offset 决定目录项数量
- 完全相同的负载范围允许共享；其它相交范围为异常
- 未压缩负载可按 BMP/JPG/PNG/RAW 魔数或尺寸识别

## EEX 文件识别魔数

ID: `format.eex.probed-header`；状态: `canonical`；证据: `source-reviewed`

字节序: `not applicable to the verified magic`

头记录字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `magic` | `0x0` | 4 | `bytes` | 固定字节 45 45 58 00，即 ASCII EEX\0 |

- offset 0x00 的四字节魔数用于识别 EEX 文件

## Hexzmap 地形目录

ID: `format.hexzmap.terrain-directory`；状态: `canonical`；证据: `source-reviewed`

字节序: `big for directory fields`

目录项字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `segment_length` | `0x0` | 4 | `uint32be` | 存储段长度 |
| `decoded_length` | `0x4` | 4 | `uint32be` | 解码长度/长度副本 |
| `file_offset` | `0x8` | 4 | `uint32be` | 段起始文件偏移 |


## 6.5/6.6 分段物品表存储

ID: `format.item.split-data-star`；状态: `canonical`；证据: `source-reviewed`

字节序: `little`

- 合计 255 条，逻辑 ID 0..254；Data.e5 +33164 保存 0..103，Star.e5 +0 保存 104..254，均 25 字节。
- 6.5 和 6.6 17 字节兼容 Variant 名称区 0x11 字节、图标为 +0x14；6.6 标准/旧山贼候选 Variant 名称区 0x0F 字节、图标为 +0x0F，+0x10/+0x14 是 Preserve 原始字节。各 Variant 的图标字段统一名为图标、类型 UInt8、字段策略 Editable。
- 图标值 N 从 0 开始，对应 E5/Item.e5 的小图 #2N+1 与大图 #2N+2；不能将逻辑图标号、1 起始 E5 图号和版本内字节偏移混用。
- 6.6 15 字节记录 +0x11/+0x12 的类型/特效动态语义与原始类别标记有关，必须使用目标 Codec，不能按字段名固定偏移迁移。

## 物品 6.5/6.6 记录 Codec

ID: `format.data-manager.item-codecs`；状态: `canonical`；证据: `source-reviewed`

字节序: `little`

目录项字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `名称` | `0x0` | 17 | `bytes` | 6.5/17 字节变体 GBK 定长字段；6.6/15 字节变体为 15 字节 |
| `图标（15 字节名称布局）` | `0xF` | 1 | `uint8` | 6.6 标准/旧山贼候选布局使用 +0x0F UInt8 图标号；物理字段名统一为图标，字段策略 Editable；+0x10、+0x14 保持 Preserve。 |
| `图标（17 字节名称布局）` | `0x14` | 1 | `uint8` | 6.5 与 6.6 17 字节兼容 Variant 使用 +0x14 UInt8 图标号；物理字段名统一为图标，字段策略 Editable。 |
| `类别/特效逻辑字段` | `0x11` | 2 | `uint8-pair` | 6.6 15 字节 Codec 读取原始 +0x12；原始 +0x12 为 2/3 时，宝物类型来自 +0x12、装备特效号来自 +0x11；普通行反向读取。 |
| `价格` | `0x13` | 1 | `uint8` | 价格单位100；255表示不可买卖，不能用辅助+0x17替代。 |
| `类别相关尾部` | `0x15` | 4 | `uint8[4]` | 按类别解释：武器/防具为初始属性、特效值、成长、图鉴；辅助为特效值、保留、适用兵种、图鉴；消耗品为LE参数低/高字节、保留、图鉴。 |

- 物理记录分布在 Data.e5 104 条和 Star.e5 151 条，逻辑 ID 0..254。
- 6.6 普通装备的装备特效号不能写成 2/3，否则会改变物理类别；辅助/消耗行的宝物类型只能保留类别标记 2/3。
- 17 字节与 15 字节迁移只映射已确认逻辑字段；类别不兼容时保留目标记录并报告冲突，不能按偏移整行复制。
- 图标逻辑值 N 从 0 开始；E5/Item.e5 的小图为物理图号 #2N+1、大图为 #2N+2。字段读写和迁移只处理当前 Variant 的图标字节，不能将 15 字节布局的 +0x14 当作图标写回。
- UTF-8/UTF-16/GBK CSV 导入必须先按当前 Variant Codec 生成字段补丁，拒绝修改 Preserve/ReadOnly 字段。
- 18 州根目录 Item.e5 可能为扩展 ID256..511 的 256×25=6400 字节记录，Itemmsg.e5 为 256×200=51200 字节说明；与 E5/Item.e5 图标无关。文件几何与 PE 可执行消费者同时成立才识别为扩展 DATA；缺少目标消费者及已验证 ExtendData 加载器时整段标记 Ignored（不可选择写入），不能覆盖图标档案或按 256 个独立冲突误导选择。
- 扩展 DATA 的配套 ExtendData.dll SHA256 为 F2827380837060ADB43CEE0B0E399A2E8812A4507B4B2425C928A6D960AA7B11；物品消费者完整指令签名 81 E9 00 01 00 00 6B C9 19 03 0D 1C 00 4F 00，说明消费者 25 FF 00 00 00 B9 C8 00 00 00 F7 E1 8B 0D 24 00 4F 00，必须位于 PE 可执行节。
- 双方加载器/消费者通过后才按原始文件迁移；+0x12/+0x13/+0x14 的运行时轮转不重复作用到磁盘文件。
- 物理CSV列名与业务语义分离：辅助效果写初始能力(+0x15)、适用兵种写能力成长(+0x17)，图鉴主动修改写0/1；未修改字节保留。
- item-name-icon-layout 为互斥Variant的布局overlay：17字节名称布局不含+0x0F图标，15字节名称布局在+0x0F存图标；按Profile选择一种，不能同时解析为两个可写字段。
- 消耗品实际特效号来自+0x11，使用独立道具目录；固定17字节Codec的实际特效逻辑列是宝物类型，动态15字节Codec是装备特效号。
- ID255不创建有效物品行；标准Data/Star读取0..103和104..254；根Item/Itemmsg读取256..511且必须分别检查表几何和运行时加载器。

## 6.5 辅助装备兵种系分组

ID: `format.65.accessory-job-groups`；状态: `canonical`；证据: `source-reviewed`

字节序: `not applicable`

头记录字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `起始 VA` | `0x0` | 4 | `va` | 0x0044C341；运行时通过 PE 节表映射为文件偏移 |
| `分隔符` | `0x0` | 1 | `uint8` | FF 开始、组间和末尾分隔 |
| `兵种系 ID` | `0x1` | 1 | `uint8` | 0..39；同一组不允许重复 |
| `安全区` | `0x0` | 144 | `bytes` | 最多探测 0x90 字节；分组序列后必须为连续 0x90 填充 |

- 解析必须验证 FF 开头/结尾、空组、重复 ID、越界 ID 和连续 0x90 安全区。
- 写回使用目标 PE 虚拟地址映射出的文件偏移，不把占位 DataTable offset=0 当作数据；事务保存后复读分组并回滚。
- CSV 逻辑行使用 groupIndex、jobSeriesId；迁移按逻辑分组重建目标 PE 区域，目标安全区不足时报告冲突。

## 装备特效名称池

ID: `format.data-manager.effect-name-pools`；状态: `canonical`；证据: `source-reviewed`

字节序: `not applicable`

- 6.5 使用两个 GBK 变长池：逻辑起始 ID 0x1A 和 0x58，最多解析 62/40 个名称；零分隔、保留槽尾和后续非零字节，改名不得移动后续字符串。
- 6.6 使用 Ekd5.exe 文件偏移 0x9D9A0，230 个 16 字节槽，逻辑 ID 0x1A..0xFF；每槽最多 15 个 GBK 字节并保留终止符后的原始参数字节。
- 6.6 固定池写入前必须检查哨兵槽 0/28/56/72 的原始文本，或通过已检查历史回溯；全池零终止、GBK 可解码且至少 40 个非空槽时才可替代哨兵证据。
- 名称池是专用 binary service；物理页显示只读但业务页可创建字段级名称补丁，写后必须按原逻辑 ID 精确复读。
- 一键迁移忽略所有特效名称池（effect-names、item-effect-names-low/high/66），只迁移逻辑特效号、特效值和分配槽；保持目标名称及具体词汇。名称池布局、容量或只读差异不生成迁移差异、不阻断其它数字字段；业务页手工改名仍走上述专用写入门禁。

## 人物暴击/撤退台词映射

ID: `format.data-manager.person-quotes`；状态: `canonical`；证据: `source-reviewed`

字节序: `little for selectors`

- 人物 Data.e5 +396 的每条 32 字节记录，+0x10 是普通暴击类型 0..25；普通类型 t 对应 Imsg.e5 +140000 的文本槽 21+t×3、22+t×3、23+t×3，每槽 200 字节 GBK。三句文本由同类型人物共享。
- 特殊分配表 Ekd5.exe 文件偏移 +0x89C30，21×UInt32LE，主键/行号 specialSlot=0..20 才是 Imsg 暴击文本槽；该行 UInt32 值为绑定人物 ID 0..1023，1024 表示空槽。绝不能把单元格的 personId 当成 Imsg 行号。
- 特殊绑定优先于普通类型；同人物出现多个特殊绑定时 Resolve 按表顺序取首个匹配槽。特殊模式绑定目标槽、清除该人物其它槽到 1024，并保留原普通类型作回退。目标槽属于他人时预览占用者，未显式覆盖不得修改草稿。
- 切回普通模式时清除此人物的所有特殊绑定到 1024，写入普通类型并编辑三句共享文本。模式、映射、人物详情与 Imsg 修改进入同一个页面草稿，支持一次撤回/重做；长度校验或冲突失败不产生部分更改。
- 撤退文本按人物 ID 0..48 对应行；人物 +0x0F 原始撤退字段不参与该文本行索引，保留原值。6.5 文本区 +440200、6.6 +491600，均为 49×200。6.6 +440200 只诊断冲突，450000 字节 Imsg 不满足新区域边界。
- 写入特殊映射前必须通过 PE 可执行区引用及 21 个 UInt32 值的范围证据；缺少验证时人物暴击模式/绑定及文本编辑均拒绝。

## R/S 形象指定表证据门禁

ID: `format.data-manager.rs-assignment`；状态: `canonical`；证据: `consumer-signature-and-pe-mapping`

字节序: `little`

目录项字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `R` | `0xE1000` | 2 | `uint16le` | 1024 行；6.5 及经独立 PE 消费者确认的 6.6 样本，VA 0x50F800 映射到此文件偏移，按索引×2 |
| `S` | `0xD2800` | 2 | `uint16le` | 1024 行 UInt16LE；经独立 PE 消费者确认的样本 VA 0x501000 映射 raw 0xD2800，先把人物 ID×2，再读取 word 并区分 S=0、1..32 和 >=33。 |

- 6.5 已知 EXE SHA 或经逐字节历史回溯到已知 SHA 时可写；本项目 INI FileHead/RFileHead 有冲突立即拒绝。未知 EXE 仅有 INI 与资源边界不能证明消费引用，因此最多只读。
- 6.6 独立消费者签名从目标 PE 可执行节唯一定位 R 的 movzx word[eax*2+VA]、S 的人物 ID×2/UInt16/0/33 分支，读取操作数 VA 并按目标 PE 节表映射；要求 1024×2 区域处于完整可写节、不互相重叠，R 的人物 ID 换算调用目标也在可执行节。
- 本轮证据集为 10 个可执行文件（1 个 6.5、9 个 6.6/6.6x，包括独立指定器附带 EXE）；常见目标为 R VA 0x50F800→raw 0xE1000、S VA 0x501000→raw 0xD2800；实际写入只使用目标探测结果。
- 6.6 INI 有 FileHead/RFileHead 时必须与独立探测一致；无 INI 时以消费者和 PE 映射为准。静态配置 Unavailable 不等于所有 6.6 不可用：运行时证据通过后升级 Editable，否则禁止读取继承偏移。
- 本条只给出源码及静态样本证据，不代替资源容量、人物引用和引擎运行时实测。
- 人物 S 指定字段与兵种形象库是两个命名空间：人物 S=1 指向特殊人物物理槽 #241 起，兵种形象逻辑 ID=1 则指向物理槽 #2；不能因数值相同混用。人物 S=0 依赖人物当前兵种/转职，完整映射见形象资源布局。

## 策略施展地形掩码

ID: `format.data-manager.strategy-terrain`；状态: `canonical`；证据: `consumer-signature-and-pe-mapping`

字节序: `little`

目录项字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `terrainMask` | `0x1FECC` | 1 | `uint8` | 6.5 30 项低四位火/水/风/地掩码；6.6 通过 VA 0x420ACC→raw 0x1FECC 消费者确认，策略类由 1<<类 与掩码分支 |

- 6.5 30×UInt8 低四位火/水/风/地种类掩码；它是地形到策略元素类别的全局许可表，不是每个策略独立的 30 地形表。高位保留/不支持写入，当前数值边界 0..15。
- 6.6 在目标 PE 可执行节唯一匹配完整 20 字节 UInt8 地形读取/AND 消费者，提取表 VA 并映射完整 30 字节区；还需至少两个真实相对调用，且其中一个调用者证明策略类别 0..3→1<<类别并传入地形/掩码。
- 典型样本消费者 VA 0x419587/raw 0x18987，表 VA 0x420ACC/raw 0x1FECC。工具不依赖这些常数直接开写，使用消费者操作数映射后的目标偏移。
- 30 项中任一值含低四位之外数据，或签名/调用者/边界不成立时不可用。保存后源 SHA 与逐项复读仍必须通过。

## 拓展四表

ID: `format.data-manager.extended-tables`；状态: `canonical`；证据: `source-reviewed`

字节序: `little`

目录项字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `Effect.e5` | `0x0` | 1024 | `256 slot records` | 1024 行，每行 256 槽×4 字节，共 1048576 字节；每槽 +0 特效号 UInt8、+1 特效值 UInt8、+2..3 Preserve 原始字节。 |
| `Effectmsg.e5` | `0x0` | 8 | `uint8[8]` | 255 行×8 字节，共 2040 字节；启用与 7 个原始参数。 |
| `MeffStudy.e5` | `0x0` | 64 | `32 two-byte records` | 1024 行，每行 32 槽×2 字节，共 65536 字节；每槽 +0 策略ID UInt8，+1 次数 UInt8，不能按单 UInt16 语义解释。 |
| `Forge.e5` | `0x0` | 64 | `structured 64-byte record` | 1024 行×64 字节，共 65536 字节；GBK 名称30字节、8个材料ID UInt16/数量UInt8、结果和保留字段，详见物理表字段。 |

- 四表逐物理表 CSV；每次导入携带 Profile/Variant/TableKey/schema 元数据，事务一次提交并记录源 SHA。

## 形象管理器资源布局

ID: `format.data-manager.image-resources`；状态: `canonical`；证据: `source-reviewed-tests`

字节序: `big for E5 directory; codec-specific payload`

- Pmapobj.e5 每个 R 逻辑资源为正/背两个 E5 条目，每面 20 帧、48×64；逻辑资源编号从 0 开始，物理 E5 条目从 1 开始。
- Unit_mov.e5/Unit_atk.e5/Unit_spc.e5 分别按 48×48×11、64×64×12、48×48×5 帧解码；三档案共同物理容量取目录条目数最小值，只列共同完整可用槽。兵种形象单独命名空间：逻辑 ID 0..min(239,共同容量-1) 对应物理 #ID+1，不从人物 S=1 的特殊区生成兵种形象。
- 人物 S=0 为默认兵种：jobId 0..59 先算 effectiveJob=(jobId/3 的整数商)×3+(turn-1)，物理图号 effectiveJob×3+1；jobId 60..79 为单转，物理图号 jobId×3+1。
- 人物 S=1..32 为特殊三转，物理图号 241+(S-1)×3+(turn-1)；S>=33 为单转，物理图号 337+(S-33)。
- turn 只能 1..3；兵种库的 0..239 槽与人物库相互独立，人物下拉只接受人物模式并额外提供默认 S=0。
- 人物头像字段是 Data.e5 +396+personId×32+13（等价文件偏移 0x199+personId×0x20）的 UInt16LE，0..65535；不可按 UInt8 截断 255 以上编号。
- +15 撤退字段、+16 普通暴击字段相邻，写头像只能修改 +13..14。
- Face/Tou 逻辑头像 N 与该字段直接相等；头像 0 使用 Face.e5 #1..8 八表情，N>=1 使用 Face.e5 #N+8，Tou.dll 取对应物理图号+300 的 RT_BITMAP，优先语言 2052。
- Meff.e5 小动画和 McallNN.e5 大动画按策略字段编号解析。
- Item.e5 与 Mtem.e5 都是小/大图配对档案：逻辑图标 N 对应 E5 物理条目 #2N+1（small）和 #2N+2（large），N 从 0 开始；不能把 Mtem 解释为 N+1，也不能只读其中一帧。配对宝物/策略图标的新增、替换、删除必须同时处理两帧。
- 6.5 DLL 资源按小/大位图对组成 0 起始逻辑 ID；样本逻辑 0 对应 RT_BITMAP 100/101。DLL→E5 时物理目标条目为 2N+1/2N+2，DLL 资源 ID 不是 Data 图标字段值。
- 图像转换透明规则固定为：源 8bpp DIB 以 palette index 0 为透明，不按 RGB 蓝色判断；源 24bpp 的 RGB(247,0,255) 与黑色透明；目标 24bpp 仅 RGB(247,0,255) 透明。输出无压缩 BMP24，逐像素保留非透明 RGB 与原尺寸；若不透明像素撞目标透明色，转换必须失败。
- 根目录 Item.e5/Itemmsg.e5 可能是 18 州扩展 DATA（Item 256×25、Itemmsg 256×200），不能遮蔽 E5/Item.e5 图像档案；资源目录只接收通过几何和首条图像验证的有效图像档案，同名有效双档案必须报告冲突。
- 迁移资源按完整档案/文件 SHA 比较并复制或转换，不按界面当前可见缩略图、选中帧、头像 255 或 S 下拉项截断；Face/Tou、R/S 三档案、小大图、地图、音视频及配置分别清点。完整资源迁入仍须满足目标消费者、格式转换与资源引用规则，不宣称不兼容引擎代码能够直接生效。
- 多个 6.6 样本末尾有孤立物理条目；它不构成新逻辑图标。新增完整小/大对插入孤立尾之前，既有编号和尾部 stored bytes/DecodedLength 保持不变；历史撤回/重做按整个档案逐字节恢复。
- 业务页默认预览大图，按原图宽高比适配区域，不能把大小图或动画帧拉伸成固定比例；资源缺失或未知数值显示无图，不回退到相邻图号。
- 可重排资源的删除/重排只在资源事务中进行并显示外部引用警告，不自动更新 Data、策略、脚本或地图编号；兵种 S 固定槽仅清空，不物理删除或前移。
- 兵种 S 的逻辑0..239为固定物理槽；删除不是移除目录项，而是在 Unit_mov/Unit_atk/Unit_spc 中同步把所选槽的全部帧像素索引清零，保持原尺寸、物理目录条目数及所有后续编号。RAW保留末尾额外字节，8bpp BMP保留头/调色板及未编辑载荷；未验证格式拒绝清空。
- 兵种 S 页的“新增”表示向选中的既有固定槽导入/替换，不允许向人物将领 S 命名空间尾部追加。原人物 S 的追加入口不构成兵种扩容；兵种固定槽的像素修改应原位写回，复制追加必须拒绝。
- 兵种固定槽清空事务登记 ReferencePolicy=fixed-slot-clear；不能套用普通资源删除的前移重排策略。仍保留 before/after SHA与整档案快照供撤回/重做；同一事务修改mov/atk/spc全部关联文件。
- 原生动作条、当前套AI参考图与BMP/动画子格式分别登记独立协议；原生导出R为正背两条、S为mov/atk/spc三条，不能用参考总图替代原生导出。
- 形象设定中文分类名称后附当前descriptor实际出处文件：6.5宝物为Itemicon.dll、6.6为Item.e5；Pmap.e5显示战场地形，Weather.e5显示天气图片。内部ResourceKey与物理相对路径不因显示标签修改。
- 引擎版本与图标容器独立：固定PE版本FilePrivatePart=6可判为6.6，即使本地化FileVersion文本为旧1,0,0,1或仍使用Itemicon/Mgcicon DLL。IsUsableResourcePath要求Item/Mtem首条为标准图片，未知RAW几何不按大小图配对读取，回退已验证DLL。厚黑6.6混合样本E5/Item.e5为126条（106×1024、20×1026字节），不因此假设63对图标；实际Itemicon.dll为171对16/32图。
- Meff规范路径优先E5/Meff.e5；十八州样本目录四字节尾部可非零，必须用OpenMeff专用读取，普通E5保持严格零尾部。缩略图、完整解码、播放间隔、导出和原生平面均复用ReadPackageBytes；只让首帧解码成功仍会导致图库点击播放失败。

## 攻击与穿透范围字段到预览图号的映射

ID: `format.data-manager.range-resource-numbering`；状态: `canonical`；证据: `source-reviewed`

字节序: `not applicable`

- 兵种/策略的范围数值为从 0 开始的字段；Hitarea.e5（攻击/施法范围）和 Effarea.e5（穿透范围）的普通 E5 资源图号从 1 开始。唯一映射是 physicalImageNumber=fieldValue+1。
- ResolveRangePreview 负责加一次 1，DecodeRangeFirstFrameAsync 把该物理图号直接交给普通 E5 预览；后续不能再次加 1。示例：字段0→#1，字段12→#13。
- 负数、整数溢出、缺失资源、不可预览 Codec 或图号超过资源条目数时显示无图；不因预览缺图更改原始字段。
- 范围图片只说明编号预览，不授权据图片反推攻击坐标段或更改运行时范围结构。

## 中文 CSV 交换名称及旧表头兼容

ID: `format.data-manager.chinese-csv-aliases`；状态: `canonical`；证据: `source-reviewed-tests`

字节序: `encoding-specific`

- 导出文件名使用物理表中文显示名，首列为编号；物理字段可以用中文别名显示（Army→部队原始值、HP→气血、MP→策略值），它们不是新的二进制字段。
- 导入首列同时接受 ID（不区分大小写）、编号、记录编号；同一文件同时出现两个编号别名必须整体拒绝，不能重复映射主键。字段接受原物理名、ExportName 和中文显示名；同一字段被多列别名重复映射也拒绝。
- 元数据 #DataManagerCSV,1,ProfileId,VariantId,TableKey,LayoutRevision 保持稳定机器标识，独立于中文文件名；重命名文件后仍按 TableKey 识别。旧无元数据文件允许目标校验后导入。
- 批量导入同时接受旧 TableKey 或中文文件名别名，歧义、多文件指向同一表、未知列、只读更改与重复 ID 均在事务前拒绝。导出前检查中文文件名唯一性，避免覆盖。
- 支持 UTF-8 BOM、UTF-16 LE/BE、GBK 和 CSV 引号/换行。CSV 完整原样回导允许保留旧未知数值，不会静默规范化原始字节；真正修改仍检查当前 Codec 与字段范围。

## 统一历史的来源标识和恢复路由

ID: `format.data-manager.unified-history-sources`；状态: `canonical`；证据: `source-reviewed`

字节序: `not applicable`

- 统一列表是两个日志的只读投影，按时间降序展示；数据来源固定为“数据”，形象来源固定为“形象”，不能只靠 OperationId 或显示行号判断来源。
- 数据历史读取项目 .data管理器历史/manifest.jsonl，保留 schema2.0、ProfileId、VariantId、LayoutRevision、文件 before/after SHA、字段和字节补丁；恢复路由回 ProjectWorkspace.UndoSaved/RedoSaved。
- 形象历史使用项目 .data管理器形象历史 根和原 HistoryService 的项目路径哈希子目录；日志为 History/history.jsonl，快照位于 History/snapshots/<operationId>；恢复由 ResourceHistoryAdapter 调用原 HistoryService。
- 不移动、不合并写入、不重写任何已有来源日志；展示保留来源、操作 ID、时间、目标路径、before/after SHA 和状态。形象 Undo/Redo 过渡记录不是可再撤回的原始修改，须选带文件快照的原记录。
- 两类恢复各自验证当前目标 SHA 和快照 SHA；冲突时阻止覆盖。形象恢复成功后使资源缓存失效，数据恢复继续使用原 Profile/Variant/布局身份与逐字节检查。
- 密集连续物理字段的历史按文件级 before/after SHA 与合并后的连续 ByteChunk 保存；迁移决策日志按表/字段/动作压缩为连续 ID 区间，稀疏 ID 保留空洞。撤回/重做仍逐字节校验 SHA，不以压缩日志替代字节快照。
- 迁移决策日志把整段忽略单独记录在 Ignored 数组，含 TableKey、FieldName、Kind=Ignored、Reason、RecordIdRanges；与真正无法映射的 Unmapped 分开。Ignored 不在可写白名单，即使手工提供覆盖/合并选择也不会提交。特效名称池按策略完全跳过，不伪造为无法映射失败。

## R/S 原生动作条交换格式

ID: `format.data-manager.rs-native-strip-exchange`；状态: `canonical`；证据: `source-reviewed`

字节序: `Windows BMP little-endian; source E5 directory big-endian`

索引公式: `动作条像素 y = frameIndex * frameHeight + localY；物理条目/转数沿用当前逻辑资源 FrameDescriptor，不重新推导跨命名空间编号。`

- 文件：`R<ID>/front.bmp`；48×1280；20帧，每帧48×64
- 文件：`R<ID>/back.bmp`；48×1280；20帧，每帧48×64
- 文件：`S<ID>/mov.bmp`；48×528；11帧，每帧48×48
- 文件：`S<ID>/atk.bmp`；64×768；12帧，每帧64×64
- 文件：`S<ID>/spc.bmp`；48×240；5帧，每帧48×48

- 导出图片与AI参考图分离。原生动作条按工具整合包协议导出24bpp BMP，透明区域写当前项目palette的索引0键色；兼容导入RGB(247,0,255)与RGB(255,0,255)，回写时转换成目标原有透明键色。DrawImageUnscaled保留像素格，不交给GDI隐式编码生成灰度索引BMP。
- 默认仅当前套：R正背两条，S移动/攻击/特技三条。显式allTurns另导出turn1/turn2/turn3子目录；不影响默认参考图的当前套规则。
- 兵种S使用兵种S<ID>目录，与将领S<ID>目录分开；写回保持FrameDescriptor中的物理槽和Turn。
- 替换可仅提供部分动作，未提供动作和其他转数保留。BMP或PNG尺寸/帧序不符必须拒绝；同一动作同时存在多个别名或扩展名产生歧义则拒绝。
- R正面接受front/x/1、背面接受back/y/2文件名；S接受mov/atk/spc。完整路径或包含逻辑形象子目录均能定位。
- 8bpp BMP保留原索引及palette后送入RsImportService；RAW/BMP真实写回保留源容器未拆字节和尾部，在一次多文件资源事务提交。

## 当前套参考总图与像素导回协议

ID: `format.data-manager.current-set-reference-atlas`；状态: `canonical`；证据: `source-reviewed`

字节序: `PNG network byte order; application frame descriptors preserve source physical IDs`

- ReferenceAtlasContext为当前逻辑资源的非拥有视图。S只筛选当前preferredTurn的28帧且要求同一物理图号；无该Turn时取首个真实可用套；R保留40帧。
- 默认输出一张键色PNG和提示词，透明观察版由IncludeTransparent显式选择；旧接口透明版行为保留兼容。参考图不写JSON manifest，也不依赖目录内遗留JSON。
- R布局40帧，front0..19再back0..19，单格64×64、7列，总画布448×448；帧本身保持48×64。
- S当前套布局348×348：mov0..5、mov6..10、spc0..4占48像素三行，atk0..3、4..7、8..11占64像素三行；帧距2像素，分区保持既有布局。
- 导出倍率仅1/2/4，用最近邻等整数放大；提示词逐项写出实际输出画布与各帧矩形，不允许平台自行转1024/1536、添加外边距、合并格子或填占保留空格。
- 默认导回Kernel=NearestNeighbor、GeometryMode=None，只按格位恢复一次原生像素网格，不强迫AI新角色缩成原人物轮廓或相同基线；旧AlignToReferenceOccupancy仅为显式选项。
- 输入必须无损PNG；AI实际画布可经格式修复配准到标准格位，但先逐帧拆分再处理，禁止把整张大图模糊缩小当最终结果。
- 保留AI新服装、武器和身形，原项目帧用作格位和动作参照。缺帧、占保留格、无法解释的错格阻止提交；低置信度、蒙版或裁切必须在确认窗审查。
- 最终量化回目标项目调色板并保留目标帧描述符；参考套导回不能覆盖其他转数或另一个S命名空间。

## Weather.e5 216×50 四帧竖条与消费者

ID: `format.data-manager.weather-four-frame-strip`；状态: `canonical`；证据: `static-verified`

字节序: `E5目录big-endian；条目RAW8像素按行连续，无BMP头`

索引公式: `frame k pixel(x,y) = decoded[k*216*50 + y*216 + x], k=0..3, x=0..215, y=0..49`

每条解压大小: `43200` 字节。

帧几何: `216×50`；帧数: `4`；条带: `216×200`。

- 文件：`Weather.e5`
- 文件：`E5/Weather.e5`

消费者画像：`profile.ccz65.weather-reviewed.3890`；定位：`0x44a36f` (va)；文件位置：`0x4976f` (fileOffset)；样本SHA256：`3890CC3247163D30CD0A2F3412E06A83E7270AA9324B6E358D84EFAED07DC08C`。

- `frame-index-times-rgb-stride`：文件 `0x49799` / VA `0x44a399`；原字节 `0F B6 41 18 69 C0 90 7E 00 00`。
- `frame-dimensions-height-width`：文件 `0x497ae` / VA `0x44a3ae`；原字节 `6A 32 68 D8 00 00 00`。
- `increment-and-four-frame-wrap`：文件 `0x497c9` / VA `0x44a3c9`；原字节 `FE 41 18 80 61 18 03`。

消费者画像：`profile.ccz66.weather-reviewed.2594`；定位：`0x44a399` (va)；文件位置：`0x49799` (fileOffset)；样本SHA256：`2594711168EA58258E40F3D804BF982DC376B58711C8E562EBE6B16E87A56B82`。

- `frame-index-times-rgb-stride`：文件 `0x49799` / VA `0x44a399`；原字节 `0F B6 41 18 69 C0 90 7E 00 00`。
- `frame-dimensions-height-width`：文件 `0x497ae` / VA `0x44a3ae`；原字节 `6A 32 68 D8 00 00 00`。
- `increment-and-four-frame-wrap`：文件 `0x497da` / VA `0x44a3da`；原字节 `FE 41 18 80 61 18 03`。

- 两个复核样本均为5个E5条目，每条解压43200字节；该乘积也等于240×180，不能只凭总长度猜尺寸。
- 6.5消费者使用frameIndex×0x7E90作为RGB帧字节偏移，push高度0x32和宽度0xD8；frameIndex增1后AND3，静态证明四帧循环与216×50几何。
- 6.6V10.1相同尺寸/步长/循环字节也存在，函数中间调用不同；仅记录静态消费者，不声称对6.6全部运行时播放速率/混合行为完成追踪。
- 预览按0、1、2、3自上而下循环；条目逻辑ID=imageNumber-1。未知几何拒绝预览并保留原资源，不能套用240×180单帧。

## 旧 BMP 自身调色板与无损索引像素写回

ID: `format.data-manager.bmp-indexed-preserving-edit`；状态: `canonical`；证据: `source-reviewed`

字节序: `little-endian BMP fields; palette channel order source-specific`

目录项字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `BMP file pixel offset` | `0xA` | 4 | `uint32le` | 像素起点，不得假定固定54或1078 |
| `DIB header size` | `0xE` | 4 | `uint32le` | 当前验证12/40/52/56/108/124字节；12字节CORE使用RGBTRIPLE，其余RGBQUAD |

- BMP魔数BM优先走BMP解析，禁止按裸RAW8读取BMP头/调色板为像素。自身4/8bpp palette优先；RGBQUAD第4字节是保留值，不能把常见零值解释为透明alpha。
- 无压缩BI_RGB的4、8、24、32bpp按当前验证布局编辑，stride=((width*bits+31)/32)*4；有符号高度决定top-down/bottom-up。4bpp高半字节为偶数x、低半字节为奇数x。
- 像素修改克隆原载荷，只改目标像素；BMP头、bit depth、palette、每行padding、32bpp第4保留字节及图尾保持。压缩或未验证布局保留原文件并拒绝按RAW重写。
- 未改变颜色的像素优先沿用旧索引，含重复调色板颜色也不因重新量化改变索引；修改颜色量化到自身palette，索引越界必须报错。
- RAW8资源使用项目有效Spalet，再查tsb及内置工具整合包tsb。Spalet每色B/R/G三字节；tsb每色B/G/R/保留四字节，两者第4字节不作alpha。
- 所有有效调色板均缺失时仅允许灰度预览，CanWrite=false，RequireWritePalette拒绝写回；不能以灰度fallback覆盖原彩色资源。
- 此格式门禁不改变DLL图标迁移的独立透明规则；RGB可视相同不表示索引身份可互换。
- 宝物小图由大图2×2预乘alpha平均推导；写回既有BMP4/8时调用原模板Rebuild，保留自身palette、位深、重复色索引、头、padding和尾部，不能强制转24bpp。

## Meff/Mcall 20 字节记录与 RAW8/嵌入 BMP 动画载荷

ID: `format.data-manager.strategy-animation-payload`；状态: `canonical`；证据: `source-reviewed`

字节序: `E5目录big-endian；解压后的20字节记录与BMP字段little-endian`

索引公式: `recordCount=decoded[0]+1; payloadStart=recordCount*20; playback step k uses record k+1; raw plane p offset=payloadStart+p*width*height; embedded image plane p rectangle=(0,p*height,width,height)`

- 文件：`Meff.e5`
- 文件：`Mcall*.e5`

头记录字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `播放步数` | `0x0` | 1 | `uint8` | 不含首头记录的播放记录数，总20字节记录数为本值加1 |
| `主平面数` | `0x1` | 1 | `uint8` | 播放记录主平面索引应小于此值 |
| `辅助计数/旧标记` | `0x2` | 1 | `uint8` | 部分样本作为辅助平面数；不满足完整载荷计数时只使用主平面并保留原字节，混合语义未完整确认 |
| `原始标记` | `0x2` | 2 | `uint16le` | 原样保留，不能把未知位强制清零 |
| `播放时钟参数` | `0x4` | 4 | `int32le` | 6.5消费者把此值除50转为tick；编辑器只提供30..2000ms范围的便于观察的间隔，不据此声称完整游戏时序相同 |
| `帧宽` | `0x8` | 4 | `int32le` | 每个平面像素宽度，当前Codec接受1..640 |
| `帧高` | `0xC` | 4 | `int32le` | 每个平面像素高度，当前Codec接受1..640 |
| `声音/尾参数` | `0x10` | 4 | `int32le` | 原始参数仅记录/保留，不由图片编辑重新生成 |

播放记录字段：

| 字段 | 偏移 | 宽度 | 类型 | 含义 |
|---|---:|---:|---|---|
| `主平面索引` | `0x0` | 1 | `uint8` | 0基平面索引；按记录顺序播放，不按平面存储顺序播放 |
| `附加调色板选择` | `0x1` | 1 | `uint8` | RAW8使用：255为默认palette；非255且尾部有完整768字节槽时选择该槽 |
| `辅助平面索引` | `0x2` | 1 | `uint8` | 只作边界检查/保留，辅助层混合及定位未完全逆向 |
| `读取次平面分支参数` | `0x4` | 4 | `int32le` | 非零时消费者读取次平面；不能直接解释为普通overlay或简单叠加开关，原记录保持 |
| `X位置` | `0x8` | 4 | `int32le` | 公共预览画布中的水平位置；保持原记录，绝对值超过4096拒绝无限画布 |
| `透明混合参数` | `0x3` | 1 | `uint8` | 已确认分支按4+6×值计算前景颜色百分比；编辑器用于预览alpha，游戏场景与特殊遮罩不在此完成合成 |
| `Y位置` | `0xC` | 4 | `int32le` | 公共预览画布中的垂直位置；保持原记录，绝对值超过4096拒绝无限画布 |
| `未拆参数` | `0x10` | 4 | `bytes-preserve` | 未完全确认语义，图片替换不修改 |

消费者画像：`profile.ccz65.weather-reviewed.3890`；定位：`0x402537` (va)；文件位置：`0x1937` (fileOffset)；样本SHA256：`3890CC3247163D30CD0A2F3412E06A83E7270AA9324B6E358D84EFAED07DC08C`。

- `header-primary-count`：文件 `0x19be` / VA `0x4025be`；原字节 `0F B6 41 1D`。
- `primary-plane-loop-bound`：文件 `0x1c38` / VA `0x402838`；原字节 `3A 50 1D`。
- `secondary-plane-loop-bound`：文件 `0x1c5d` / VA `0x40285d`；原字节 `3A 50 1E`。
- `header-clock-read`：文件 `0x1b5e` / VA `0x40275e`；原字节 `8B 41 20`。
- `record-primary-plane`：文件 `0x1cf8` / VA `0x4028f8`；原字节 `0F B6 41 30`。
- `conditional-secondary-read`：文件 `0x1d2e` / VA `0x40292e`；原字节 `83 79 34 00`。
- `record-secondary-reference`：文件 `0x1d54` / VA `0x402954`；原字节 `0F B6 41 32`。
- `secondary-count-before-palette`：文件 `0x1d83` / VA `0x402983`；原字节 `0F B6 41 1E`。
- `record-extra-palette-selector`：文件 `0x1d8e` / VA `0x40298e`；原字节 `80 79 31 FF`。
- `record-percent-mix-parameter`：文件 `0x207f` / VA `0x402c7f`；原字节 `0F B6 51 33`。

- 容器条目解压后先算20字节记录区，再在payloadStart检查BMP/PNG/JPEG魔数；嵌入图片自身位深/palette/行padding应先解析，不能把BM头和调色板当RAW8像素。
- 嵌入图应宽度等于帧宽、高度能被帧高整除；实际平面数为stripHeight/frameHeight，并要求至少覆盖主平面。RAW8按声明主/辅助计数和完整载荷边界拆分，未知剩余尾字节保留。
- 18州Mcall09/10和6.6 Mcall00包含嵌入24bpp BMP的样本；6.5 Mcall00存在768字节附加palette尾部。不同Mcall文件不能套用单一RAW8公式。
- RAW8附加palette每槽256×3=768字节，通道B/R/G；相同平面若有多套实际生效palette，则单平面图片替换拒绝歧义，原始字节不变。
- 播放帧按记录主索引与该记录palette生成，索引0透明；未知次平面与百分比混合参数不伪装已经正确合成，预览明确标注位置/透明度与场景/辅助遮罩保留。
- 替换平面以OriginalBytes为快照，保持记录区逐字节相同、未选平面和尾部不变；BMP自身palette/位深按目标模板保持。重建后重新Inspect/Decode确认结构和可读性。
- 6.5静态调用链读取record+3并乘6加4后进入417024→40690C→415A64的百分比透明混合；虽然另一段装载次平面，不能据此把其写成普通图层叠加。精确地址只适用于绑定的静态样本，不跨版本复用。
- 位置预览取record+8/+12的int32LE并为整段播放生成固定公共画布；防止边界抖动与大图分配，绝对偏移限定4096、总画布像素不超过16777216。
- Meff规范路径优先E5/Meff.e5；十八州样本目录四字节尾部可非零，必须用OpenMeff专用读取，普通E5保持严格零尾部。缩略图、完整解码、播放间隔、导出和原生平面均复用ReadPackageBytes；只让首帧解码成功仍会导致图库点击播放失败。

写入策略：已确认主平面图片可按当前目标载荷模板替换；未知辅助层/混合语义仅保留，不按普通单帧覆盖整个解压动画。

## Face头像标准图片与64×80 RAW8载荷

ID: `format.data-manager.face-payload`；状态: `canonical`；证据: `source-reviewed-tests`

字节序: `E5 directory big-endian; standard-image codec-specific; RAW8 byte indices`

- 先检测BMP/PNG/JPEG等标准图像魔数并以图像自身尺寸/调色板解码；不把标准图片头当RAW索引。
- 非标准头像载荷仅在长度5120或5122字节时接受为64×80 RAW8；前5120字节为逐行索引，末尾可选2字节原样保留。其它未知长度拒绝猜测。
- RAW8以当前项目有效palette解码；新增/替换按目标原容器编码和64×80几何重建，标准BMP沿用原位深/自身palette/头尾。输入尺寸不同采用最近邻等比居中覆盖，不进行双线性模糊缩放。
- Face和Tou配对资源修改仍经同一资源事务提交；没有编辑时RAW/BMP载荷逐字节相同。没有验证消费者的样本不据此开放任意头像尺寸。
- 本条为格式与编辑器Codec证据，不把某个本地化旧版号样本的PE地址泛化为全部6.5/6.6地址。

写入策略：只修改通过标准图片或64×80 RAW8几何验证的目标；保持源编码、调色板、尾部和关联事务。
