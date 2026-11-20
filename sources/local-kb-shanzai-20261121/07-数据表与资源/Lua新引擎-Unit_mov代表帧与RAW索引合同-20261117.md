# Lua新引擎Unit_mov代表帧与RAW索引合同：C5/C6

## 一、结论速览

只验Unit_mov代表包，复用C1载荷。条目0的RAW帧4索引PNG往返相等；条目135的24bpp BMP帧4完整RGB与手算逐行BGR解码相等。C5灰度示意仍仅是索引；C6已从当前Pmpalet/Spalet生产链独立复算该RAW帧基础RGBA，未猜定某一个Spalet或工具tsb。

## 二、样本与既有实现

EXE SHA=26A980627F1CC399A20D7BF50C36FB20E0A92C46C73E38EC83FE915D1A855101；参考Unit_mov SHA=4F47AD39987590CE4C61171F1DF6C4BE2E86EF2DF429BC796575555AB4407C2A，15950412B，与C1相等。复用现有Ls12解包、C1 manifest、Pillow及反汇编工作台。原件/正式游戏只读，无实机。

## 三、帧与reader合同

4FE690登记width48、移动frame_indices=[4,5]，5022F0按max+1建6帧缓冲；536810的frame步长=48*48*4，536730按frame_index定位。536880区分标准图与RAW，RAW按len/width得高度，537030以索引0透明，其余查5B0768。

## 四、代表载荷与未知区

RAW条目0从原包7008起25344B=48*48*11，帧4相对[9216,11520)，2304B、1020个透明索引；未知尾部0。BMP条目135从3428448起76086B，为48*528/24bpp BI_RGB、off54/stride144/正height底向上，帧4颜色可独立解码。原载荷完整保留；帧6..10不由本次移动注册请求，未裁掉，也未给未知动作名。

## 五、判据与可复跑

资源清点与解包.py unit-frame：RAW原索引=PNG回读索引；BMP手算原始BGR逐行转换=Pillow RGB切片=PNG回读RGB，全部通过。RAW帧SHA=88CFD188979DB893A2A30F6EBEFC6698F2176E653FB86CA09519419B225995C3；RGB帧像素SHA=9A0E0FFF7177A70C5A5252275D9E29BEFAF55D47649EC4746A9A10470EE5305E。

## 六、C6已关闭该代表帧基础配色

413D40按selector0/1/2分别读取Pmpalet/Spalet/Logo_p条目到949130，768通道shr4后经4344E0生成5B0768；RAW索引0透明，其余查表。军营/R背景fallback选Pmpalet；战场部署4DACA5选Spalet(map_id)；actor RAW消费的是同一全局表，没有独立每actor palette参数。

Pmpalet115+Spalet59共174条目，本帧62个非零用色索引（max173、需522B）全部有载荷覆盖且量化后同色。短表738/711B未提供的末尾可能保留前态，不能补零；但不影响本帧用色。已按文件B/R/G高半字节公式与native逐指令模拟独立复算，PNG回读相等；RGBA SHA=5936FA3F5F227D319B20155BD06838B19D907C2A103D54DFCC07DBEC7097A7CC。无需为此帧基础色动态取样。

[新增C6报告](../../../lua引擎/资源解包/Unit_mov色表生产链与基础配色-C6-20261117.md)。其它索引/帧、瞬时fade、actor后处理与最终绘制仍开放；本次只关闭该代表帧基础配色，不反复列为同一待办。

## 七、证据与接续

[研究报告](../../../lua引擎/资源解包/Unit_mov代表帧与调色板合同-C5-20261117.md)，机器证据位于大鲸鱼产生专用/lua引擎/资源解包/C5-Unit_mov-20261117，含CFG、代表帧解码验收、RAW索引bin/示意PNG及BMP RGB PNG。未重跑全包清点/拆分，未遍列全部格式，未进入战场；该代表帧基础色已由C6闭合；继续其它有判别力的资源/生命周期与整体解析主线。
