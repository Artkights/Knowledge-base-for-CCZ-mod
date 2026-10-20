# 6.5 自动化测试契约

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.5/data/tests/data-manager-test-contracts.json`、`6.5/data/tests/smoke-test-contracts.json`

## 6.5/6.6 Profile 与 Variant 检测

ID: `test.data-manager.profile-variant-detection`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj --configuration Release --no-build -- --core-regression <sample-root>`

目标: ProfileRegistry、ProfileAugmentationService 和三种 6.6 Variant；变更范围: 临时样本副本中的 Profile/Variant metadata

断言：

- 检测 6.5、6.6 standard、17-byte legacy 的样本指纹/文件长度；old-shanzhai 仅有候选布局，不虚构完整指纹
- 6.6 不继承 6.5 R/S/terrain 写入能力而绕过动态门禁
- 不可用/候选布局显式报告原因
- 这是自定义 console runner，不是 dotnet test/xUnit；--no-build 前须使用同一配置构建。--core-regression 显式接收存在的样本根目录；不能把未提供样本时的纯合成测试成功当作本地样本写回验收。

必需产物：

- Profile/Variant 检测报告
- 源 SHA-256
- 布局 revision
- console exit code 0 and CORE_REGRESSION_TESTS_OK; selected sample root exists

失败含义：Profile 或 Variant 误判会使 CSV、Codec 和迁移字段映射失效，必须阻止写入。

## 物理表字段写回与边界复读

ID: `test.data-manager.physical-table-roundtrip`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj --configuration Release --no-build -- --core-regression <sample-root>`

目标: 人物、兵种系、兵种、策略、宝物、特效、商店和四个拓展物理表；变更范围: 复制项目中的 Data.e5/Star.e5/Ekd5.exe/Imsg.e5/Effect.e5/Effectmsg.e5/MeffStudy.e5/Forge.e5

断言：

- 只改变目标字段字节并保留 Preserve/RawHex/未拆字段
- 跨表台词、策略学习、装备许可和商店一次提交
- 写后按当前 Variant Codec 复读并验证 SHA/历史
- 边界不足、只读能力、特殊占位值和未知枚举得到明确诊断
- 这是自定义 console runner，不是 dotnet test/xUnit；--no-build 前须使用同一配置构建。--core-regression 显式接收存在的样本根目录；不能把未提供样本时的纯合成测试成功当作本地样本写回验收。

必需产物：

- before/after SHA
- 字段级补丁列表
- 复读值和回滚快照
- console exit code 0 and CORE_REGRESSION_TESTS_OK; selected sample root exists

失败含义：任何字段/边界/复读失败都必须回滚整个页面事务。

## 专用二进制结构证据门禁

ID: `test.data-manager.special-binary-evidence`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj --configuration Release --no-build -- --core-regression <sample-root>`

目标: 特殊暴击映射、R/S、策略地形、辅助分组、6.5/6.6 名称池；变更范围: 复制项目的 Ekd5.exe/Imsg.e5 与资源目录

断言：

- VA→文件偏移映射正确，PE 可执行消费者签名和源 SHA 才能开放写入
- R/S 资源目录/帧尺寸/数值边界和 System.ini 门禁生效
- 策略地形只在消费者签名验证后写回
- 辅助分组 FF/0x90/重复/越界检查阻止非法写入
- 这是自定义 console runner，不是 dotnet test/xUnit；--no-build 前须使用同一配置构建。--core-regression 显式接收存在的样本根目录；不能把未提供样本时的纯合成测试成功当作本地样本写回验收。

必需产物：

- 证据等级与拒绝原因
- 专用结构复读
- 目标范围外原始字节摘要
- console exit code 0 and CORE_REGRESSION_TESTS_OK; selected sample root exists

失败含义：若门禁被绕过，可能把其它代码或资源区域当作表写坏；测试失败必须保持只读。

## CSV round-trip、跨 Variant 迁移和回滚

ID: `test.data-manager.csv-and-migration`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `$env:DATAMANAGER_TEST_BASE='<sample-root>'; dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj --configuration Release --no-build`

目标: 物理表 CSV、业务批量 CSV、虚拟迁移审阅、DLL/E5 资源转换、一键迁移和 R/S/资源差异；变更范围: 源项目只读；临时目标副本和备份

断言：

- UTF-8 BOM、UTF-16、GBK 和错误元数据按契约处理；中文文件名/字段名与旧英文别名均可往返。
- 同 Variant 与跨 Variant 使用目标 Codec/逻辑字段映射；禁止把源物理偏移直接复制到目标。
- 预览在后台任务执行并节流进度；60 万级差异使用虚拟表和索引批量选择，筛选不会逐条删除 UI 行，也不会误选不可映射记录。
- Itemicon.dll 与 Mgcicon.dll 仅在已验证配对下转换到 E5；转换保留尺寸/像素、小大图配对、奇数尾和目标未选字节，透明规则及不透明透明色冲突得到断言。
- 默认跳过并逐项覆盖/合并/跳过；源 SHA 始终不变。迁移进入提交/回滚阶段后关闭取消，失败完整恢复目标文件、资源和历史。
- 临时目标重新打开后字段、物理专用结构、资源 SHA、Profile/Variant 和写后复读均一致；已选择的缺失文件、容器/转换失败必须回滚。扩展物品缺少目标消费者/加载器时整段 Ignored、不可写；四拓展文件的物理迁入与游戏运行时支持分别报告。
- 这是自定义 console runner，不是 dotnet test/xUnit；无实际样本根目录时只能执行合成契约，不能把合成成功当成本地真实基底写回验收。
- 特效名称池按迁移策略完全跳过并保持目标原字节，不阻断逻辑特效号、特效值、分配槽及其它模块。
- 资源发现覆盖完整 R/S/Face/Tou/图标/动画/地图/场景、配置、音视频白名单文件；比较和复读完整文件 SHA，不能只迁移当前 UI 列出的前255头像或可见帧。
- 头像字段 Data.e5 记录+13 为 UInt16LE；大于255的值不得截断，+15撤退与+16暴击相邻字节不因头像迁移而改变。兵种与人物 S 命名空间按各自映射解析。
- Windows只读目标资源迁移成功后恢复原文件属性；只读源资源内容与属性保持不变，新增目标不继承源只读位。晚期资源替换被句柄阻止时恢复之前文件内容/属性和SHA并清理tmp；文件系统允许替换打开文件时按完整成功提交验收，不能强行宣称发生回滚。

必需产物：

- CSV schema/Profile/Variant/TableKey 元数据和中文文件/列名
- 后台预览进度、虚拟审阅决策、不可映射原因
- 迁移前后 SHA、目标备份、转换像素/尺寸复读、回滚报告
- console exit code 0；对应 runner 输出 DATA_MANAGER_CORE_TESTS_OK、MIGRATION_UI_TESTS_OK、MIGRATION_IMAGE_CONVERSION_TESTS_OK 或 REAL_PROJECT_MIGRATION_TESTS_OK；真实命令必须提供存在的样本根目录

失败含义：任何已选择项目的映射/资源转换/像素复读、源或目标 SHA 漂移、目标写入失败必须停止并恢复目标；明确 Ignored 的整段扩展物品保持目标原值，不作为完成迁入。不能把四拓展文件物理可读等同为目标游戏具备相应消费者。

## Profile、Codec、知识库和本地样本离线一致性

ID: `test.data-manager.layout-knowledge-offline`；状态: `canonical`；证据: `source-reviewed-offline-checker`

命令: `python data管理器/验证/check-layout-knowledge.py --workspace <source-workspace> --kb <knowledge-base> --report <report-json>`

目标: 4 个 Variant 的物理表、运行时特殊台词分配表、来源 SHA 和 10 个本地 EXE 的 PE 消费者；变更范围: 游戏、Profile、源码和知识库仅只读；可选参数仅输出新的 JSON 报告

断言：

- 知识库表文件、起点、ID、行数/宽度、字段展开及当前 Codec 与 ProfileRegistry 继承/覆盖结果一致；特殊台词表槽号与 personId 分别检查。
- 每个登记来源文件 SHA 必须与当前源码一致；console runner、中文 CSV、范围 field+1 和统一历史来源规则仍出现在已审读实现中。
- 10 个本地 EXE 的实际 SHA、原证据 SHA、PE32 节边界、唯一 R/S/策略地形消费者、操作数 VA→文件偏移、写入节和掩码宽度分别检查；缺少样本或无法由逐字节历史补丁解释的 SHA 漂移明确失败。
- 合法历史修改的样本只在内存中反向验证每个补丁的新旧字节、before/after SHA、长度及非重叠边界，完整重建原证据 SHA 后仅记录衍生关系；不得伪称原样样本，也不为未知 EXE 放宽运行时门禁。
- 本地派生 EXE 不匹配 Profile 指纹时仅做独立证据/边界检查并列诊断；没有虚构自动版本识别结果。
- 四个 Variant 的两个分段宝物表均具有名为图标的 UInt8 Editable 字段：6.5/17 字节兼容为 +0x14，6.6 标准/旧山贼候选为 +0x0F；15 字节布局的 +0x10/+0x14 仍为 Preserve。
- 兵种系属性行语义与用户确认枚举一致，并单独标注 user-confirmed-semantics；不将界面名称确认升级为逆向或运行时验证。
- 本地 E5/Item.e5 目录逐项校验边界；逻辑图标 N 对应小图 #2N+1/大图 #2N+2，奇数尾条目独立诊断并保留；静态脚本不改写资源。
- 资源绑定/追加 console 测试另验证默认大图像素、等比预览、奇数尾前插入新完整对、尾 stored bytes/DecodedLength 不变、既有编号不变以及 Undo/Redo 逐字节恢复；离线脚本本身不执行这些写入测试。
- 450000 字节 Imsg 无法覆盖 6.6 +491600 撤退表时列为必须拒绝加载；旧 item-acquisition 两表保持 Unavailable。
- 脚本是静态一致性验收，不替代资源容量或游戏运行时实测，也不授予 candidate 条目自动写回。
- Item.e5 与 Mtem.e5 均按逻辑 N→物理 #2N+1/#2N+2 检查；Mtem 不得回退到旧 N+1 公式。
- 根目录 18 州 Item.e5/Itemmsg.e5 扩展 DATA 与 E5/Item.e5 图像档案按有效图像几何分离；同名有效双档案产生诊断。
- 资源转换契约检查源 8bpp palette index0、源24bpp黑色/247品红、目标24bpp仅247品红透明、无压缩 BMP24、尺寸/非透明像素保留及不透明247品红拒绝。
- 扩展物品 ID256..511 在源/目标加载器或消费者不通过时为一条不可写 Ignored 整段；四张拓展表可作为物理数据迁入和复读，但目标缺少对应消费者时必须独立列出运行时 Incompatible，不能宣称游戏功能已生效。
- 人物头像登记为 Data.e5 +396+personId×32+13、宽2字节 UInt16LE、Editable，+15/+16相邻台词字段不合并；Face/Tou 资源逻辑 ID 不再按 UInt8 截断。
- 兵种 S 图库逻辑0..239→物理1..240；人物 S=1→物理241起，S=0依赖当前兵种，两个命名空间不能混用。
- 源码审读记录名称池完全跳过、Ignored与Unmapped分列、资源白名单全档案迁移；不以静态脚本通过代替真实样本全迁移与游戏运行时验收。
- 资源绑定console测试对共同容量有限的兵种S目录确认固定槽数量；清空首槽后mov/atk/spc条目数不变、选中槽像素索引为0、下一槽stored bytes逐字节保持。人物S与兵种S展示分开；兵种导入不得追加到人物库。静态离线脚本不替代该写入测试。

必需产物：

- layout_knowledge_passed 与计数
- JSON report 包含相对样本路径、源 SHA、目标地址/大小和诊断，不包含本机绝对路径

失败含义：布局、源码 SHA 或独立样本证据漂移必须先更新事实源及复核门禁，不能以生成索引通过替代真实一致性。

## 图片来源标签、初始选中状态与内置说明

ID: `test.data-manager.image-ui-presentation`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj --configuration Release --no-build -- --ui-presentation`

目标: 详情表格/辅助分组/历史/迁移表格的选择反馈、SearchableIdComboBox、资源分类出处和嵌入帮助；变更范围: 离屏 WinForms 窗体及内存合成资源描述符；不读取或改写游戏样本

断言：

- 普通详情表初始化后没有默认蓝色首行或当前单元格；表头选择背景等于正常背景。
- 有焦点时保留系统蓝色选择反馈，失焦后显示淡灰选择；高对比模式遵守系统颜色，不删除用户当前单元格。
- 辅助分组保留当前行与右侧联动；程序绑定下拉文字取消默认全选，用户主动选择的文字在异步选项回填后保留。
- 分类名称使用当前项目真实容器：宝物 Item.e5 或 Itemicon.dll；天气图片（Weather.e5）；战场地形（Pmap.e5）；S 组合保留三个 Unit 文件。
- 使用说明可由程序集直接读取，不依赖 EXE 旁边的 Markdown 文件。
- 真实MainForm加载6.5/6.6人物页后，1280×720与1920×1080首次显示、尺寸变化和切换人物均无程序绑定蓝选残留；标签继承真实字体/DPI后完整显示。

必需产物：

- console exit code 0 and UI_PRESENTATION_TESTS_OK
- 同配置构建日志；本测试不替代可见窗口和高 DPI 人工验收

失败含义：错误的自动选择或绑定回填可能覆盖用户编辑；来源标签或帮助缺失会导致用户无法定位资源或单文件帮助不可用。

## 原生动作条与当前套 AI 参考图像素往返

ID: `test.data-manager.rs-strip-and-atlas`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `dotnet run --project 形象管理器/src/ImageManager.Tests/ImageManager.Tests.csproj --configuration Release --no-build -- --rs-exchange`

目标: R/S 原生 BMP 动作条、当前套参考总图、像素复原、格式保持和逐帧替换；变更范围: 系统临时目录中的合成 E5/RAW/BMP/PNG 资源及动作条；完成后删除，真实参考样本只读

断言：

- R 正背两条为 48×1280；S mov/atk/spc 三条为 48×528、64×768、48×240，输出 BMP24 并保持帧序。
- 默认只导出当前套，显式全转导出才生成 turn 子目录；兵种 S 与将领 S 目录互不混用。
- 同一 Unit 档案多个编号批量替换形成一个候选档案，修改不相互覆盖；尺寸错误不写原档案。
- S 第二套参考图仅绑定该套 28 帧和真实物理图号，不改变第一/第三套的 stored bytes；默认仅生成 PNG 与提示词。
- 原尺寸、2倍和4倍固定格位经默认最近邻还原逐像素一致；非整数尺寸修复保留 AI 新内容，不自动缩回原人物占区。
- 取消、缺帧、无法解释的错格及越界输入阻止提交；旧三转参考图 API 仍能通过兼容回归。
- RAW/BMP8/BMP24/PNG 原编码、尾部及未编辑重复颜色索引保留；外来索引不被当作目标索引直接复用。
- 天气单帧编辑只改选中 216×50 帧，完整 216×200 条带替换仍保持四帧结构。
- Face64×80 RAW8及可选2字节尾部、BMP24 R/S无修改逐字节一致；Face/Tou关联替换保持原编码和尺寸。
- 真实WinForms消息循环验证默认最近邻/Geometry None、当前S第二套28帧与显式旧84帧切换；切换或关闭取消任务，迟到输出释放且不覆盖新候选，调用者帧所有权不变。

必需产物：

- console exit code 0；结果行失败 0
- 动作条尺寸与帧数、当前套帧描述符、像素哈希和未编辑 stored bytes 断言
- --atlas-regression 使用的真实样本是否存在须单独注明，不能用合成成功冒充真实样本验收

失败含义：导出/替换协议、目标槽或还原核错误会覆盖其他转数、改变像素风格或丢失原编码字节，失败时拒绝提交。

## 依赖系统 .NET 8 的 Windows x64 单 EXE 发布与嵌入资源验收

ID: `test.data-manager.single-executable-publish`；状态: `canonical`；证据: `source-reviewed-publish-profile`

命令: `dotnet publish data管理器/src/DataManager.App/DataManager.App.csproj --configuration Release -p:PublishProfile=SingleFileWinX64 --output <publish-directory>`

目标: framework-dependent WinForms 单 EXE、系统 Windows Desktop Runtime 依赖和嵌入图标/Profile/帮助；变更范围: 全新发布目录、样本目录外的验收报告与截图；原始游戏样本只读，编辑仅使用临时副本

断言：

- 在全新而非历史输出目录执行发布；目录仅留下 data管理器.exe，不含旁置 DLL/PDB/deps.json/runtimeconfig.json、hostfxr、hostpolicy、coreclr 或其它 .NET runtime 文件。
- SingleFileWinX64 当前配置为 RuntimeIdentifier=win-x64、SelfContained=false、PublishSingleFile=true、UseAppHost=true；PublishTrimmed/PublishReadyToRun/IncludeNativeLibrariesForSelfExtract/IncludeAllContentForSelfExtract 均为 false，不把历史自包含发布结论用于本模式。
- 运行前置条件是 .NET 8 Windows Desktop Runtime（Windows x64）；单 EXE 只说明分发文件数，不表示无需安装运行时，也不能用无效 DOTNET_ROOT 声称程序自带运行时。
- 应用 Profile、帮助、必要资源和 Doro-white.ico 随 EXE 分发；ApplicationIcon 与运行时窗口图标使用同一 ICO，开发/测试宿主不借用测试程序图标。图标资源存在与窗口图标检查不等于各 Windows Shell 显示位置均已人工验收。
- 当前发布报告只记录 Windows x64、已安装 Windows Desktop Runtime 8.0.8 环境的启动成功；没有执行独立虚拟机或卸载运行时试验，无运行时环境的提示行为须保留未实测状态。
- --verify-bundle 可另行只读检查嵌入资源、物理表、图片、中文 CSV、迁移预览和两尺寸窗体；报告必须位于样本外并复核源 SHA。旧自包含 bundle 的历史报告不能替代当前 framework-dependent 产物验收。

必需产物：

- 当前源码同配置构建/发布日志、发布目录完整文件清单、EXE 文件版本/大小/SHA-256
- SelfContained=false 等发布属性、外部 .NET 8 Windows Desktop Runtime（Windows x64）依赖和嵌入图标记录
- 启动环境的 OS/架构及已安装 Runtime 版本、实际启动结果；独立干净系统及无 Runtime 环境未实测时明确标注

失败含义：输出多文件或带入旧 runtime 表示发布目录/配置不符合单 EXE 契约；目标缺少 Desktop Runtime 属于明确的系统前置条件，不应通过重新声明自包含绕过。资源/图标缺失或已满足 Runtime 条件仍不能启动时阻止交付。

## 旧 BMP、动画载荷与天气帧条编解码专项

ID: `test.data-manager.bmp-animation-weather-codecs`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `dotnet run --project 形象管理器/src/ImageManager.CodecTests/ImageManager.CodecTests.csproj --configuration Release -- <source-workspace> --diagnostics`

目标: BMP4/8/24/32、CORE12、RAW8/BMP/PNG策略动画、Weather216×50四帧与调色板缓存；变更范围: 临时合成资源与三套Weather复制项目，结束删除；3套真实原始样本只读，动画无修改重建在内存生成候选字节

断言：

- 4/8bpp自身RGBTRIPLE/RGBQUAD调色板优先，保留字节不作alpha；top-down/bottom-up、stride padding、重复颜色旧索引和未知尾部保持。
- 无修改BMP往返逐字节一致；单像素索引修改只改对应一个像素字节。
- 项目tsb优先于嵌入tsb；外部同长度同mtime修改仍按SHA失效；缺少项目palette时使用有效内置palette而非静默灰度。
- RAW8与嵌入BMP/PNG动画按记录引用顺序播放、边界正确；附加palette和未知尾部保持，替换平面后复读结构一致。
- 真实样本每个Weather条目拆成4个216×50帧，按纵向拼回原索引逐字节一致；帧1修改保留帧0/2/3。
- 真实动画全部解码、无修改重建逐字节一致；已确认的palette/位置/透明度预览与完整游戏背景/特殊辅助遮罩合成分别报告，不相互替代。
- 样本不存在时runner会打印跳过；只有3套样本均存在且出现各自统计才可声明真实15天气条目和269动画条目验收。
- 三个Weather临时项目分别执行完整条与单帧PlanReplace→Commit→History Undo→Redo，E5复读和SHA恢复一致；原样本字节不变。
- 混合版专项从workspace根执行：固定版本private=6识别6.6，未知RAW Item不遮蔽171对DLL图标；六套6.6引擎版本检查8断言，不能以此授予未知RAW图标写入。
- ItemIconDerivation在BMP4/8模板下保留原位深、palette、padding、未变重复索引与tail，避免大图推导小图时退化成24bpp。

必需产物：

- console exit code 0；全部通过断言计数
- 三套样本每套5天气条目，动画69/71/129的实际统计
- --diagnostics日志显示payload格式、记录数、主/次平面、tail及降级提示

失败含义：头部、palette或动画分界错误会把非像素数据读成乱码或破坏原索引；结构/字节复读失败时不能提交候选资源。

## Weather与Meff/Mcall动态预览及异步取消界面验收

ID: `test.data-manager.animation-preview-ui`；状态: `canonical`；证据: `source-reviewed-tests`

命令: `dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj --configuration Release --no-build -- --animation-preview-ui <sample-root>`

目标: 真实Weather/Meff/Mcall资源、播放控件和取消/释放门禁；变更范围: 真实基底只读；临时目录生成非零目录尾部 Meff 等合成资源并于结束删除；WinForms 消息循环改变内存控件，源文件 SHA 前后比较

断言：

- Weather按四张216×50帧加载；暂停、下一帧和速度调整有效，不把整张216×200当单帧。
- 真实 Meff/Mcall 在图库点击后按播放记录解码并自动播放；记录所选样本实际帧数，不把某基底固定帧数套用其它样本。十八州修复报告观测 Meff 17 帧、Mcall00 26 帧。
- 非零四字节目录尾部的合成 Meff：普通 E5Archive.TryOpen 必须拒绝，Meff 专用读取返回原动画包字节；缩略图、图库点击后的两帧自动播放与 50ms 间隔、1×1 原生平面读取均成功，源 SHA 不变。
- 图库解码后读取播放间隔必须复用 StrategyAnimationResourceCodec.ReadPackageBytes，不得再次走普通 E5Archive.Open 导致整项预览失败；索引枚举或代表帧解码成功不能替代点击播放验收。
- 连续选项、切换资源及Dispose取消旧请求；迟到结果不回填新资源，旧Bitmap被释放。
- 有位移和透明百分比的公共播放画布5×2与原生编辑平面2×1分离，不把位移/alpha烘焙进资源替换。
- 所有真实源资源SHA保持不变；本测试不宣称完整游戏场景/特殊辅助遮罩及引擎时钟一致。

必需产物：

- 同配置预先构建日志；所声明的 6.5/6.6 样本分别运行，console exit code 0 与 ANIMATION_PREVIEW_UI_TESTS_OK
- 非零尾部合成例的普通 E5 拒绝、Meff 专用点击播放/50ms 间隔/原生平面及 SHA 断言
- 实际样本与 Weather/Meff/Mcall 帧数、公共画布/原生平面尺寸、源 SHA；十八州 Meff 修复报告的 SHA 为 E7E6DB63A567053F5A5DF8AD16D09CE42F9818A2CE148AA6F3B4C54E66F85357

失败含义：动态预览拆帧、播放或生命周期错误；失败时不得把缓存/合成画布写回目标资源。

## 宝物类别编辑、辅助五例与消耗品草稿/CSV/字节隔离回归

ID: `test.data-manager.item-semantic-editing`；状态: `canonical`；证据: `source-reviewed-tests-and-recorded-local-regression`

命令: `dotnet run --project data管理器/src/DataManager.Tests/DataManager.Tests.csproj --configuration Release --no-build -- --item-semantic-editing <workspace-root>`

目标: ItemSemanticResolver、宝物类别业务编辑器和原物理列 CSV；6.5 固定 Codec 与 6.6 动态 Codec 的类别别名/字节写回；变更范围: 所有保存仅针对 TestSupport.CreateCoreCopy 生成的临时核心文件副本；合成样本的 System.ini/Star.e5 和往返 CSV 在副本内修改，结束删除副本。另在 <workspace-root>/data管理器/验证/2026-10-20-宝物读写修复 生成或覆盖 宝物154-天毒珠.png；原始基底保持只读。

断言：

- 工作区必须同时存在 基底/复刻版6.6山贼 国庆 与 基底/加强版6.5未加密版；缺失明确失败，不以合成测试代替真实五例。--no-build 前使用同一配置构建，这是自定义 console runner 而非 dotnet test。
- 真实样本 Star.e5 的五条 25 字节记录独立检查：ID154 天毒珠=特效值1/适用兵种6侠客，ID156 太平要术=5/0君主，ID157 天毒珠（仿）=60/6侠客，ID149 左氏春秋=22/255所有兵种，ID139 凌风赤兔=7/27上将；分别检查 +0x15/+0x17，均 +0x13价格255、+0x18图鉴1。
- 真实五例正序及逆序重复切换后，名称、当前语义和 UI 数值一致，适用兵种下拉及图鉴勾选可编辑，价格提示包含255表示不可买卖；仅浏览不得产生工作区或面板草稿。
- 真实154编辑实际特效号、特效值9、适用兵种27、价格99、图鉴0及保留值77；Resolver 立即反映当前草稿，切往156再返回保留编辑值，保存前原始基线与磁盘 Star.e5 均不变化。
- 真实154及合成辅助保存后仅允许目标行 +0x11/+0x13/+0x15/+0x16/+0x17/+0x18 变化；核心文件全部逐字节对比预期，并以 Resolver 复读目标字节、确认工作区不再脏。
- 6.5和6.6合成行109辅助、104防具、150消耗品在同一 items-high 表交替切换，必须按类别重建布局，无旧字段/值残留且不生成修改；辅助没有初始/成长字段，普通防具没有辅助/消耗品编辑器，消耗品下拉使用独立道具目录。
- 辅助原物理字段 CSV 保持初始能力/装备特效值/能力成长/价格（/100）/宝物图鉴列名，不改为业务别名；原样导入 ChangedCells=0；修改六字段导入 ChangedCells=6，Resolver 读取草稿并保存到上述六个目标字节，二次导出回导无变化。
- 合成消耗品独立编辑实际特效号0x3D、参数低字节0x34/高字节0x12、+0x17保留值33、图鉴1；不显示初始属性/成长/辅助适用兵种，摘要更新为装备升级。仅允许 +0x11/+0x15/+0x16/+0x17/+0x18 变化，不凭 UI 编辑证明参数已被游戏消费者使用。

必需产物：

- console exit code 0 与 ITEM_SEMANTIC_EDITING_TESTS_OK，同配置构建日志及实际样本存在记录
- 真实五例字节/名称断言、各次保存的完整核心文件逐字节预期比较和 CSV ChangedCells 断言
- 临时副本生成的宝物154截图；截图不包含真实图标资源，不作为资源缺失或真实多显示器高 DPI 验收依据

失败含义：类别映射、重绑定、草稿同步或 CSV 别名错误可能改写相邻/保留字节；任何独立样本断言或整文件预期比较失败须拒绝交付，保留原始源并重新核对布局，不放宽断言。通过不代表游戏内行为/未知参数语义已验证。

## R/S eex 只读烟测

ID: `test.65.smoke-rs-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-smoke`

目标: R/S eex 只读烟测；变更范围: 否

断言：

- 明确验证 RS\R_.eex/S_.eex 索引不混入 E5S，验证 B形象指定器偏移、头像预览和 E5 110 索引表预览

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 旧版完整剧本深度烟测

ID: `test.65.smoke-legacy-scenario-depth-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-scenario-depth-smoke`

目标: 旧版完整剧本深度烟测；变更范围: 否

断言：

- 遍历全部 R/S eex，使用迭代方式统计旧版完整树命令数和最大子事件嵌套深度，防止递归枚举再次引入 StackOverflow

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## R/S eex 核心写入烟测

ID: `test.65.smoke-write`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --write`

目标: R/S eex 核心写入烟测；变更范围: 只写测试副本

断言：

- 当前等价于 R/S 核心写入验证：复制测试副本，写 RS\R_00.eex 文本和 Ekd5.exe 人物 R/S 指定表，备份并复读校验

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## R/S eex 核心写入烟测

ID: `test.65.smoke-rs-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-write-smoke`

目标: R/S eex 核心写入烟测；变更范围: 只写测试副本

断言：

- 与 --write 主线相同，名称更明确；若 S_00.eex 战场标题容量为 0，输出 BATTLEFIELD_TITLE_WRITE_SMOKE_SKIPPED 后继续验证胜败条件、部署、地图和 Hexzmap

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 战场标题/胜败条件写回烟测

ID: `test.65.smoke-rs-text-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-text-write-smoke`

目标: 战场标题/胜败条件写回烟测；变更范围: 只写测试副本

断言：

- 单独验证 S 剧本文本写回；标题容量不足只跳过标题子项，不阻断胜败条件结构保存和复读

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 战场部署写回烟测

ID: `test.65.smoke-rs-deployment-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --rs-deployment-write-smoke`

目标: 战场部署写回烟测；变更范围: 只写测试副本

断言：

- 单独验证 46/47/4B 部署、空槽自动绑定、AI/坐标和单位状态写回

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 独立单关语义命令烟测

ID: `test.65.smoke-standalone-semantic-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --standalone-semantic-smoke`

目标: 独立单关语义命令烟测；变更范围: 否

断言：

- 验证 typed event 编译为真实命令草稿，禁止 turn_start/area_entered 继续用文本标签冒充触发

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 独立单关黄金样例烟测

ID: `test.65.smoke-standalone-golden-samples-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --standalone-golden-samples-smoke`

目标: 独立单关黄金样例烟测；变更范围: 否

断言：

- 固定三英战、救援战、Boss 决战，验证角色识别、R/S 命令图、资源阻断和报告等级

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 严格可玩预览烟测

ID: `test.65.smoke-strict-playable-preview-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --strict-playable-preview-smoke`

目标: 严格可玩预览烟测；变更范围: 否

断言：

- 验证 strict_playable_preview 会因缺资源、结构草稿和 runtime gate 阻止 playable/runtime 等级

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 地图/Hexzmap 一致性烟测

ID: `test.65.smoke-map-terrain-consistency-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --map-terrain-consistency-smoke`

目标: 地图/Hexzmap 一致性烟测；变更范围: 否

断言：

- 校验 Map JPG、Hexzmap 索引、格数、decoded length 和可编辑块一致

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## E5/动态链接库 图片资源目录与条目替换烟测

ID: `test.65.smoke-e5-image-replace-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --e5-image-replace-smoke`

目标: E5/动态链接库 图片资源目录与条目替换烟测；变更范围: 只写测试副本

断言：

- 先复制常见图片 E5 和图标 动态链接库 到测试副本，校验 Face/Pmapobj/Unit_/Hitarea/Effarea/Logo/Mmap/U_select/Gate/Weather 等 E5 资源目录与 Itemicon/Mgcicon/Cmdicon 动态链接库图标编号预览，再生成小 PNG 替换 Unit_mov.e5 单个 110 索引图号，复读条目字节并验证备份/JSON 报告

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 旧版 MFC 对话框 复刻烟测

ID: `test.65.smoke-legacy-mfc-dialog-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-mfc-dialog-smoke`

目标: 旧版 MFC 对话框 复刻烟测；变更范围: 否

断言：

- 从旧 OnEditModify() 解析 101 个命令号到 71 个对话框 的分派，校验 C# 分派表、旧 .rc 资源、71 个显式行为目录、Dialog_114 34 个模板，并逐个实例化旧式对话框 执行初始化/提交

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 战场单位状态写回烟测

ID: `test.65.smoke-battlefield-unit-status-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --battlefield-unit-status-write-smoke`

目标: 战场单位状态写回烟测；变更范围: 只写测试副本

断言：

- 复制 S_00.eex 到测试副本，直接从旧版脚本树构造 46/47 TargetKey，验证等级/兵种级/AI、48 装备、52 兵种改变和 5 条 38 五维写回；断言 48 在部署段，52/38 在同 Section 的 1C 绘图 下方，并校验 4081=1/0 包裹

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 角色默认装备写回烟测

ID: `test.65.smoke-role-default-equipment-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --role-default-equipment-smoke`

目标: 角色默认装备写回烟测；变更范围: 只写测试副本

断言：

- 验证 6.5-0 人物 尾三字节字段 武器/防具/辅助 无未命名 padding；抽样人物 ID 162 读取 46/90/143；角色设定聚合表派生 武器名/防具名/辅助名；测试副本写入 0/70/109 后直接校验 Data.e5 @ 0x18C + id0x20 + 0x1D..0x1F，再恢复原值并复读

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 特效包读写烟测

ID: `test.65.smoke-effect-package-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --effect-package-smoke`

目标: 特效包读写烟测；变更范围: 只写测试副本

断言：

- 验证 EffectPackage 的宝物特效、兵种特效、个人/套装专属和补丁草案入口；覆盖宝物绑定自动发现删除、兵种分配固定清空、个人/套装专属只改指定槽位和删除清空 14 列

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 商店/物品读取烟测

ID: `test.65.smoke-shop-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --shop-smoke`

目标: 商店/物品读取烟测；变更范围: 否

断言：

- 验证商店数据、人物名、物品低/高段、装备/道具下拉、物品详情和 CSV/批量编辑路径；用于确认引擎感知物品表解析没有回退

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 全局数字参数证据护栏

ID: `test.65.smoke-global-numeric-evidence-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-evidence-smoke`

目标: 全局数字参数证据护栏；变更范围: 否

断言：

- 验证旧形象指定器左侧全局数字项当前可写项为 LevelLimit/UpgradeExperience 加 5 个低风险 leaf；AbilityThreshold/EquipmentExp/Merit/PromotionLevelSecond/MiddleEquipmentLevel 继续锁定，父级组合 key 拒绝写入，System.ini 未暴露截图数字项偏移，并确认 CMF smoke 示例地址 0048D3C4 在当前 6.5 基底映射为文本片段而非 等级上限/升级经验

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 全局数字参数静态候选查询

ID: `test.65.smoke-global-numeric-query-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-query-smoke`

目标: 全局数字参数静态候选查询；变更范围: 否

断言：

- 生成 CCZModStudio_Reports\DebugEvidence\global-numeric-query\\global-numeric-query-report.json，断言静态候选查询不会把待验证字段升级为可写；已验证字段必须显式列出官方 diff 写回目标

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 全局数字参数官方 diff 实验准备

ID: `test.65.smoke-global-numeric-discovery-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-discovery-smoke`

目标: 全局数字参数官方 diff 实验准备；变更范围: 只写测试副本

断言：

- 生成普通 before/official_case/official_tool，并生成低风险 noop_case、7 个 leaf case、对应 official_tool_<caseKey> 与 low-risk-experiment-report.json；初始 compare 必须保持 NeedsManualOfficialDiff，不自动晋级字段

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 全局数字参数版本护栏

ID: `test.65.smoke-global-numeric-write-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --global-numeric-write-smoke`

目标: 全局数字参数版本护栏；变更范围: 只写测试副本

断言：

- 同一入口额外复制标准 6.6 基底，断言所有 6.5 固定偏移项均为“版本锁定”、不暴露目标偏移，preview 拒绝且 Ekd5.exe SHA256 不变

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 能力档位补丁扫描/写回烟测

ID: `test.65.smoke-ability-tier-patch-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --ability-tier-patch-smoke`

目标: 能力档位补丁扫描/写回烟测；变更范围: 只写测试副本

断言：

- 显式扫描本地 6.5 未加密基底 Ekd5.exe 的档位函数、5 个 call site、封顶点和显示表；预览 6 档分支合并与 10 档迁移阻断；在测试副本中写 6 档并复读，再写回 7 档并复读，确认备份和 JSON 报告存在

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 剧本专属/套装文本烟测

ID: `test.65.smoke-exclusive-set-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --exclusive-set-smoke`

目标: 剧本专属/套装文本烟测；变更范围: 否

断言：

- 扫描 R/S eex 的 72 信息传送子功能 10，验证专属/套装文本解析、人物/物品/特效名映射和格式容错

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## E5S 存档/旧探针兼容检查

ID: `test.65.smoke-legacy-e5s-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-e5s-smoke`

目标: E5S 存档/旧探针兼容检查；变更范围: 否

断言：

- 只检查 SV\.E5S 是否存在、B形象指定器 中 CountSV、文本线索和旧命令探针；输出会标注 compat_only_not_rs_script

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。

## 历史全量探针

ID: `test.65.smoke-legacy-all-smoke`；状态: `candidate`；证据: `legacy-structured`

命令: `dotnet <SMOKE_TESTS_DLL> --legacy-all-smoke`

目标: 历史全量探针；变更范围: 可能按旧逻辑继续运行

断言：

- 仅用于追溯旧实现，不作为当前主线成功标准；其中仍可能包含未清理的 SV004.E5S 历史断言

必需产物：

- console result
- test-copy diff when mutation is enabled

失败含义：该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。
