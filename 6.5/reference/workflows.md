# 6.5 自动化制作工作流

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/workflows/data-manager-workflows.json`、`6.5/data/workflows/local-review-20261028.json`、`6.5/data/workflows/production-workflows.json`

## 物理表 CSV 导入导出与写后复读

ID: `workflow.data-manager.physical-csv-roundtrip`；状态: `canonical`；证据: `source-reviewed-tests`

目标：让每个底层物理表生成可重新导入当前打开项目的 CSV，并通过字段级补丁保护未拆字节。

输入：

- 项目根目录和检测出的 Profile/Variant
- 单个物理 TableKey CSV 或业务页批量草稿
- 源文件 SHA-256

步骤：

1. 检测 Profile/Variant、文件长度、源 SHA 和当前布局 revision；拒绝元数据不匹配的 CSV。
2. 按 UTF-8 BOM、UTF-16 LE/BE、GBK 和 RFC4180 解析；检查稳定 ID、复合键、未知列、重复 ID、只读列和数值边界。
3. 使用当前 RecordCodec 和专用名称池/辅助分组服务把逻辑字段映射为字段级补丁，保留 Preserve、RawHex、槽尾和未拆字段。
4. 将所有相关物理文件加入一个 WorkspaceTransaction 草稿；预览冲突和 SHA 变化后一次提交。
5. 临时文件原子替换，按同一 Codec 重新读取字段、复读关联表和验证 SHA；失败恢复全部目标文件与历史快照。

门禁：

- Variant 必须与 CSV 元数据一致
- 只读/不可用表不得自动写入
- 跨表业务页禁止只提交部分关联文件
- 未知数值可保留并显示证据状态，不能静默转换

产物：

- 每个物理表独立 CSV
- 字段级补丁和 SHA 审计记录
- 写后复读结果和可撤回历史

回滚：

- 提交前保留目标文件和 SHA 快照
- 任何复读或边界失败恢复本次所有文件，源项目不修改

## 一键迁移源基底到目标基底

ID: `workflow.data-manager.cross-profile-migration`；状态: `canonical`；证据: `source-reviewed`

目标：将源基底数据表、专用二进制结构与全量已支持 E5/DLL/Face/Tou/R/S/图标/动画/地图/场景/配置和音视频资源迁移到目标；后台预览、可取消审阅、事务回滚，保留目标引擎并逐项报告格式/消费者限制。

输入：

- 源目录（第一选择）
- 目标目录（第二选择）
- 双方 Profile/Variant、文件 SHA、E5/DLL 资源目录

步骤：

1. 在后台任务探测源/目标 Profile、Variant、文件边界、E5/DLL 位图资源、R/S/策略消费者和证据 SHA；UI 线程仅节流显示阶段进度，不在控件中逐条构造数十万差异行。
2. 按 TableKey+逻辑 ID+字段生成字段级和资源级差异；跨 Variant 通过目标 Codec/逻辑字段映射，禁止复制源物理偏移。特效名称池保留目标词汇并完全跳过，特效号/值/分配槽仍迁移。DLL 小/大图按已验证配对转换为目标 E5 2N+1/2N+2 并逐像素复读。扩展物品 ID256..511 在目标缺少消费者/加载器时合为一条整段 Ignored，不能伪装为图标或逐行可写记录。
3. 虚拟化差异审阅表，默认全部跳过；按文件/逻辑模块或稀疏索引选择覆盖、合并、跳过。筛选和批量选择只操作索引，不循环 DataGridView.Rows；Ignored 整段仅作诊断、不可选，Incompatible 保留具体原因和目标原值。
4. 在目标卷临时副本执行字段补丁、专用结构写回和资源转换；节流报告预览/复制/校验进度，支持取消。进入“提交目标”或“回滚”后屏蔽取消，避免半提交。
5. 验证临时副本结构、字段、资源尺寸/像素、Profile/Variant、SHA 和历史；备份目标核心文件与资源，逐文件原子替换并写后复读。历史决策按连续 ID 区间和合并 ByteChunk 压缩，仍保留完整前后字节恢复能力。
6. 已选择项目若缺失文件、格式转换不兼容、目标 SHA 改变或边界/复读失败，则停止并从备份反向原子恢复目标，清理临时文件和未提交历史。Ignored 整段与主动跳过项目不参与写入；四张拓展表可物理迁移但独立报告目标运行时能力，不以复制文件宣称游戏功能已生效。源目录始终只读且 SHA 不变。

门禁：

- 源目录必须只读；源/目标在预览后重新校验 SHA 和 Profile/Variant
- 未验证 R/S 区域、不可转换 DLL/E5、未知引擎 EXE/插件 DLL 或缺少目标消费者的已请求功能列为 Incompatible；扩展物品 ID256..511 缺少加载器/消费者则整段 Ignored。两类诊断均不可选择覆盖，不能假报告已在游戏生效。
- 资源转换仅允许已验证的 Itemicon.dll→E5/ Mgcicon.dll→E5 文件名配对；8bpp palette index0、24bpp透明规则、不透明目标透明色和多语言差异均须通过检查
- 虚拟差异视图不得因筛选/批量编辑丢失或误选行；用户关闭对话框不能绕过提交/回滚保护
- 目标每个 Codec/资源边界、临时副本复读、原子替换和最终 SHA 必须通过
- 资源发现递归使用扩展名白名单 .e5/.dll/.exe/.ini/.eex/.jpg/.jpeg/.png/.bmp/.gif/.ico/.webp/.tif/.tiff/.avi/.mp4/.dat/.bin/.map/.wav/.mp3/.ogg/.mid/.midi/.wma/.flac，以及无扩展名 SETTINGE5；逐个完整文件比较 SHA，不以 UI 预览数量裁切。
- 点开头的工具历史/备份/Git 目录、重解析点和不在白名单的存档 .e5s/.exs 不迁移；物理表仅排除工作区实际解析出的路径，不按文件名误排除其它目录同名图像档案。根目录 6400/51200 字节 Item/Itemmsg 由扩展 DATA 专用服务识别，不能当普通资源。
- 根目录/E5 同名有效资源按目标既有路径对齐，不创建遮蔽副本；源或目标存在多个有效候选时报告冲突。已知图片 DLL 为 Itemicon/Mgcicon/Tou/Cmdicon/Mapatr；未知 EXE/DLL 不作为普通资源覆盖目标引擎。
- 头像数据必须以 UInt16LE 迁移并保持大于255的值；兵种 S 图库逻辑0..239与人物 S=0默认、1..32特殊三转、33+单转使用独立命名空间，不能按相同数字错配。

产物：

- 源/目标 Profile 与文件库存
- 字段级/逻辑记录级/资源级差异预览及逐项决策
- 目标备份、临时副本、转换候选和 SHA/复读报告
- 压缩迁移历史、回滚报告；成功时目标数据/资源可重新打开读取
- Ignored 整段日志与 Unmapped/运行时能力诊断分开，保持特效名称池为目标词汇

回滚：

- 任何文件或资源失败时，提交期间反向原子恢复全部已替换目标文件和历史 manifest
- 删除临时目标/转换候选；保留备份供诊断；源目录文件、SHA 和资源始终不变

## 形象资源新增替换删除与引用警告

ID: `workflow.data-manager.image-resource-transaction`；状态: `canonical`；证据: `source-reviewed`

目标：在统一形象设定页复刻形象管理器的资源预览和增删改，并把资源修改集中在资源事务。

输入：

- 资源类别和逻辑 ID
- 素材文件或替换帧
- 当前资源目录和已用物理 ID

步骤：

1. 后台读取缓存的资源目录和文件指纹，按中文资源类别列出 R/S、头像/Tou、宝物/策略图标、大小动画、攻击/穿透范围、场景/地图/其他图片；同名根目录扩展 DATA 不作为图像档案，真正双档案冲突必须提示。 Meff 的索引、缩略图、点击播放、间隔读取和原生平面读取统一经过专用动画包读取；不能只凭可枚举或代表帧成功判定图库播放通过。
2. 校验资源 Codec、E5 配对、帧尺寸和 S job/turn 映射；DLL→E5 仅走已验证转换器并逐像素检查透明规则、尺寸和语言，资源新增/替换/删除前生成引用警告。
3. 建立资源 before/after SHA 和字节快照；普通可追加资源默认追加，Item/Mtem 小大配对共同处理、孤立尾前插入完整对。兵种 S 固定槽仅原位导入/替换或清空 mov/atk/spc，不物理删除、不前移、不追加到人物库；其它可重排资源不自动修改 Data、策略、脚本或地图引用。
4. 在资源事务中原子提交 E5/DLL/目录帧，统一历史视图记录来源；失败时按 SHA 反向恢复，显式失效 Catalog/缩略图/动画缓存。

门禁：

- 资源文件必须通过有效图像档案几何校验；根目录扩展 Item.e5 不能遮蔽 E5/Item.e5，真双图片冲突不得随机选择
- Item.e5 与 Mtem.e5 逻辑 N 均必须同时具有物理 #2N+1/#2N+2；转换/编辑不得丢小图或只更新大图
- R/S 未通过消费者和 PE 映射证据时只读预览；资源编号变化仅显示外部引用警告
- 提交后尺寸、帧、像素、SHA 和历史复读通过
- 兵种 S 逻辑0..239固定槽清空必须保持三档案条目数、后续 stored bytes和全部编号；仅支持已验证RAW/8bpp BMP像素索引清空，未知格式拒绝。人物 S 追加与兵种固定槽编辑严格分开。
- Meff 非零四字节目录尾部仅在 Meff 专用入口兼容，普通 E5 仍严格拒绝；执行 test.data-manager.animation-preview-ui 覆盖点击后50ms间隔和原生平面，源SHA不变。预览兼容不自动授予损坏索引或未知资源写入权限。

产物：

- 资源预览/变更结果
- 引用警告
- 可回滚资源快照和历史

回滚：

- 资源事务失败时原子恢复 before 快照

## WinForms 依赖系统 .NET 8 的单 EXE 轻量发布与内置资源

ID: `workflow.data-manager.single-executable-publish`；状态: `canonical`；证据: `source-reviewed`

目标：分发仅含一个 EXE 的 Windows x64 应用，由目标系统提供 .NET 8 Windows Desktop Runtime，并在用户项目保存数据、资源与历史。

输入：

- .NET 8 SDK 与当前 Release 源码；目标机已安装 .NET 8 Windows Desktop Runtime（Windows x64）
- DataManager.App及引用的Core/Images/ImageManager.Core
- 嵌入Profile JSON、内置帮助、Doro-white.ico与SingleFileWinX64.pubxml；全新且不含历史 runtime 文件的发布输出目录

步骤：

1. 构建当前 Release 源码，执行所需 console 回归；检查发布 Profile 为 win-x64、SelfContained=false、PublishSingleFile=true、UseAppHost=true，禁用裁剪/ReadyToRun及native/all-content自解压。
2. 在包含 data管理器/ 的源工作区根执行 dotnet publish data管理器/src/DataManager.App/DataManager.App.csproj --configuration Release -p:PublishProfile=SingleFileWinX64 --output <new-publish-directory>；输出到新目录，避免历史自包含 runtime 残留。
3. 验证仅有 data管理器.exe，记录版本/大小/SHA-256，不携带 runtime、DLL、独立 PDB 或旁置配置/帮助；核对 Profile/帮助和图标嵌入资源，ApplicationIcon 与窗口图标使用同一 ICO。
4. 在已记录 Runtime 版本的 Windows x64 环境，从独立目录启动 EXE；按 test.data-manager.single-executable-publish 检查启动和资源。可另用 --verify-bundle <report-json> <sample-root> 生成只读报告，放在样本外并复核源 SHA。
5. 报告明确写明需要 .NET 8 Windows Desktop Runtime（Windows x64）。将本机已安装Runtime的启动结果、尚未执行的独立干净系统/无Runtime测试分别记录，不引用旧自包含报告证明当前包免安装。

门禁：

- 禁止PublishTrimmed，WinForms/反射/资源发现未做裁剪闭环。
- 发布目录单 EXE 与系统 Runtime 前置条件必须同时成立；发现 coreclr/hostfxr/hostpolicy 或旧 runtime DLL 时换全新输出复核，不宣称自包含。
- 项目数据、资源、导出、备份、历史继续在项目目录，应用只读目录不得阻止编辑可写项目。
- 本机已有 Runtime 的启动成功只覆盖该环境；未安装 Runtime 的提示/干净 OS 未实测须明确标注，不虚构启动成功。

产物：

- 单个data管理器.exe，独立记录文件版本/大小/SHA256及完整发布文件清单
- framework-dependent 配置、嵌入资源/图标检查和 Runtime/OS/架构对应的实际启动结果
- 可复现发布命令及必需安装 .NET 8 Windows Desktop Runtime（Windows x64）的说明

回滚：

- 发布不改游戏目录；保留上一发布版，启动或烟测失败时使用上一产物。

## 按宝物类别编辑辅助与消耗品并以 CSV/字节隔离验收

ID: `workflow.data-manager.item-category-editing`；状态: `canonical`；证据: `source-reviewed-tests-and-recorded-local-regression`

目标：从已识别的物理 Codec 和类别语义生成可编辑业务字段，保持 CSV 物理列名与相邻原始字节，并以临时副本复读控制写入风险。

输入：

- 项目根目录、精确 Profile/Variant、当前 System.ini DefID/AssID、源文件 SHA-256
- 待编辑 TableKey/物品 ID、当前行原始字节及工作区草稿；物理布局引用 format.data-manager.item-codecs
- 对应 struct.65.item-category-semantics 或 struct.66.item-category-semantics；消耗品目录引用 mechanism.shared.consumable-effect-namespace，未确认效果保留数字和证据状态

步骤：

1. 记录样本身份、数据 SHA、表边界和当前 Codec；区分准确 EXE 画像与编辑器可用的布局 Variant。F36 山贼国庆五例绑定 profile.ccz66.shanzai.guoqing.f36，强制兼容Variant不改变样本身份。
2. 按当前版本结构和类别构造业务字段：武器/防具保留初始属性、特效值和成长；辅助使用特效值与适用兵种；消耗品显示独立道具效果号及参数低/高字节。复用已有结构实体，不把所有物理列重解释为通用装备属性。
3. 图鉴采用勾选写入0/1，适用兵种采用保留未知值的下拉，价格显示255表示不可买卖；原始保留字段集中显示其物理位置。通过当前 Codec 把UI及CSV导入值覆盖到草稿，切换同表不同类别时重建布局，回访记录恢复草稿。
4. 先在临时副本执行 test.data-manager.item-semantic-editing：核对真实五例、类别切换、当前草稿、CSV旧列名及目标字节隔离；不把测试中的受控编辑直接应用到原始基底。
5. 实际编辑提交前输出字段级差异，核对类别相关目标字节与源 SHA；使用现有工作区事务原子保存、复读当前 Codec 字段并比较非目标字节，CSV导出/回导验证无意外差异。
6. 输出物理写回与业务显示验收，另列游戏内消费者未验证部分；消耗品名称目录或可编辑保留值不等同于游戏参数功能已确认。

门禁：

- Profile/Variant、System.ini边界和物理表几何必须一致；固定地址不得跨画像套用。
- 使用物理旧列名CSV，不把特殊效果值或适用兵种业务别名写成新的物理字段；未知值保留数字，不自动归零或转成其它类别。
- 保存前磁盘及基线不变；保存后只有审阅的字段字节变化，跨类别切换不得残留旧控件或产生浏览草稿。
- 图鉴主动编辑写0/1；辅助适用兵种与兵种装备许可是独立机制，不合并写回。无明确意义的原始字段即使可编辑也须显示证据限制。
- 真实回归依赖样本存在与当前哈希；F36五例成功不能升级历史old-shanzhai未知画像，也不证明游戏内运行语义。

产物：

- 类别正确的宝物编辑草稿、字段级补丁/目标字节清单
- 物理列兼容CSV、限定目标字节的整文件复读、源SHA与工作区历史
- 真实五例/合成类别回归结果及未确认游戏消费者的独立诊断

回滚：

- 提交前保留全部关联文件内容/SHA及工作区历史快照；任何边界、源SHA、Codec复读或非目标字节比较失败都拒绝提交或恢复整个事务。
- 回归只改临时副本，结束删除；原始基底不参与受控测试编辑，保留截图/日志供定位。

## 人物R/S实际变更同步磁盘存档与分组回滚

ID: `workflow.shared.appearance-save-synchronization`；状态: `candidate`；证据: `source-reviewed`

目标：更改人物指定或关联图片后，只同步受影响人物的已保存R/S字段，保留剧情换装和存档其他字节。

输入：

- 经过当前EXE消费者/PE/I/O链验证的布局
- 本次最终已保存的人物R/S变更或解压后图片实际差异
- 当前项目原生存档和合法关联索引/统计

步骤：

1. 校验人物R/S消费者、首段保存读取地址、Win32 I/O、场景分支和分段长度；由地址差推导E5S字段，不按版本名套固定偏移。
2. 按最终已保存值和解压后资源差异找出受影响人物；未保存草稿不参与，目录/压缩偏移变化但图片内容一致不扩大范围。
3. 只枚举当前项目SV直接子文件及当前版本私有自动档索引；排除公共/索引E5S、EXS、备份和重定向目录。将E5S与必须更新的统计/索引组成原子恢复组。
4. 逐组检查格式、来源SHA、关联SHA；写入对应R/S字段，更新已识别统计SHA和已有索引Hash。提交前复核整组，写后逐字节复读。
5. 报告更新/一致/跳过数量及原因；准备失败跳过本组，写入失败恢复本组；主数据/图片/历史失败时回滚本次成功组并保留外部改写冲突。

门禁：

- 未知扩容、截断、损坏或关联SHA不符整组跳过；部分结果不能报全部完成。
- 只修改本次目标R或S；不做全表统一，不重排人物引用。
- 历史运行记录仅离线副本验收，未完成本轮游戏窗口人工读档观察。

产物：

- 字段级存档差异及索引/统计校验结果
- 分组成功/跳过/失败报告
- 数据或图片统一历史中的备份与恢复信息

回滚：

- 成功组与主操作一起撤回/重做；恢复前检查原始/候选SHA，外部改写时保留其内容并报告冲突。
- 迁移只同步真实目标档，不把源存档迁往目标。

## ModPackage 自动化交付

ID: `workflow.65.mod-package-delivery`；状态: `candidate`；证据: `legacy-structured`

目标：把人物、兵种、物品、资源和 R/S 设计转换为可审计的增量包。

输入：

- 目标项目画像
- 槽位规划
- 结构化表更新
- 资源和剧本变更

步骤：

1. 冻结版本画像和槽位
2. 生成增量包与清单
3. 静态预览
4. 写测试副本
5. 逐域复读
6. 执行相关烟测
7. 推广或 direct 写入
8. 保存报告和备份

门禁：

- 不自动改槽位
- 资源未预览不写编号
- 剧本非白名单命令必须走完整树
- 失败域不得被无关烟测掩盖

产物：

- 变更包
- 写前/写后差异
- 备份
- 复读结果
- 烟测结果

回滚：

- 恢复备份
- 拒绝继续推广
- 保留失败报告

## 引擎特效注入制作

ID: `workflow.65.effect-injection`；状态: `candidate`；证据: `legacy-structured`

目标：从特效语义生成可审计的 Hook、桩函数、代码洞和回跳方案。

输入：

- 目标 EXE 画像
- 触发语义
- 单位上下文
- 特效号和效果值规则

步骤：

1. 确认目标样本和入口
2. 复核调用点 ABI
3. 选择标准桩或内联桩
4. 分配代码洞
5. 计算 CALL/JMP 重定位
6. 记录原字节和覆盖长度
7. 检查冲突
8. 写测试副本
9. 静态复读和实机验证

门禁：

- 地址绑定画像
- 覆盖完整指令
- 旧字节必须匹配
- 代码洞不得重叠
- 寄存器和栈必须守恒

产物：

- 补丁配方
- 参数点
- 冲突矩阵
- 回滚字节
- 验证报告

回滚：

- 逆序恢复已写站点
- 恢复页保护
- 标记样本污染并停止写入

## 特效工作台复盘与验收

ID: `workflow.65.effect-workbench-acceptance`；状态: `candidate`；证据: `legacy-structured`

目标：把特效扫描、能力判定、预览、写入和复读组织为单一可追踪任务。

输入：

- 目标 EXE
- 特效目录
- 预期机制
- 证据包

步骤：

1. 识别画像
2. 扫描当前安装状态
3. 生成能力矩阵
4. 构建写入预览
5. 核对冲突和参数
6. 应用到测试目标
7. 复读字节和行为
8. 更新证据状态

门禁：

- 扫描相似不等于已安装
- 静态能力不能自动提升为运行时能力
- 任一冲突阻断写入

产物：

- 扫描清单
- 能力矩阵
- 应用报告
- 证据升级记录

回滚：

- 按补丁记录恢复原字节
- 保留失败时样本和日志

## R 剧本模板克隆

ID: `workflow.65.r-script-template-clone`；状态: `candidate`；证据: `legacy-structured`

目标：复用成熟 R 剧本的 Scene/Section/Command 布局，仅替换受控文本和人物编号。

输入：

- 同版本成熟模板
- 目标 R 剧本
- 文本槽映射
- R 人物映射

步骤：

1. 复读模板结构
2. 导出可见文本槽
3. 建立人物映射
4. 执行写前断言
5. 完整树写测试副本
6. 圆程复读
7. 实机烟测

门禁：

- Scene/Section/Command 数保持一致
- 0x72 默认不改
- Section 末尾 0x00 保留
- R 人物编号同场景唯一

产物：

- 目标 EEX
- 逐命令结构差异
- 文本与人物映射
- 实机结果

回滚：

- 保留模板副本
- 结构不一致时丢弃目标写入

## 人物 R/S 像素形象制作

ID: `workflow.65.rs-sprite-production`；状态: `candidate`；证据: `legacy-structured`

目标：从角色设定和样例库制作可导入的 R/S 像素资源。

输入：

- 角色设定
- 动作和方向清单
- 同类样例
- 目标资源尺寸和调色板

步骤：

1. 筛选同构样例
2. 制作代表帧
3. 人工审阅轮廓和装备
4. 扩展动作/方向
5. 校验帧条尺寸
6. 预览 E5 替换
7. 导入测试槽
8. 实机审阅

门禁：

- 先代表帧后全套
- 不从异构样例拼接关键部位
- 编号映射必须复读

产物：

- 帧条
- 样例和选择理由
- 图号映射
- 审阅结论

回滚：

- 恢复资源备份
- 保留上一版通过审阅的帧条

## 地图底图与 Hexzmap 同步发布

ID: `workflow.65.map-terrain-publish`；状态: `candidate`；证据: `legacy-structured`

目标：保持视觉地图、地形格和剧本坐标一致。

输入：

- Map JPG
- Hexzmap 块
- 地图槽
- 部署和触发坐标

步骤：

1. 确认地图槽和尺寸
2. 校验 Hexzmap 格数
3. 检查必经格和触发格
4. 同步发布底图与地形
5. 复读关键坐标
6. 运行一致性烟测
7. 实机寻路验证

门禁：

- 不得新增无 Hexzmap 绑定的地图号
- 视觉道路不等于地形可通行
- 部署/增援/Boss 邻接格必须可站立

产物：

- 地图资源
- 地形块
- 坐标审计
- 一致性报告

回滚：

- 恢复地图和 Hexzmap 两份备份，禁止只回滚其中一份

## 战场自动化与调试

ID: `workflow.65.automated-battle-debug`；状态: `candidate`；证据: `legacy-structured`

目标：用稳定触发、快照和复读定位战场脚本或引擎行为。

输入：

- 可复现关卡
- 触发事件
- 目标单位和坐标
- 预期状态变化

步骤：

1. 冻结测试存档和随机条件
2. 记录写前单位状态
3. 执行单一触发
4. 采集脚本/内存结果
5. 对比预期字段
6. 缩小到命令或函数入口
7. 重复验证

门禁：

- 一次只改变一个变量
- 失败必须区分脚本、资源、地形和引擎层
- 自动化结果需人工画面复核

产物：

- 最小复现步骤
- 状态快照
- 地址/命令定位
- 回归用例

回滚：

- 恢复测试存档和测试副本
