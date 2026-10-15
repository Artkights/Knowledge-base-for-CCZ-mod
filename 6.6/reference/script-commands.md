# 6.6 剧本指令

<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->

结构化事实来源：`6.6/data/scripts/script-command-extensions.json`

> `candidate` 指令可用于解析器设计和样本比对；参数语义未复核前不得驱动自动改写。

| ID | Opcode/子命令 | 名称 | 分类 | 参数槽 | 状态/证据 |
|---|---|---|---|---|---|
| `script.66.opcode-72-sub-02` | `0x72 / 2` | 人物/部队传送扩展 | `information-transfer-extension` | P1:子类型=2[数值/枚举]; P2:人物/部队[人物/部队编号]; P3:阵营[阵营/行动方]; P4:参数A[数值/枚举]; P5:参数B[数值/枚举] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-03` | `0x72 / 3` | 人物/部队测试扩展 | `information-transfer-extension` | P1:子类型=3[数值/枚举]; P2:人物/部队[人物/部队编号]; P3:阵营[阵营/行动方]; P4:比较方式[比较符]; P5:成立后跳转[分支/跳转目标] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-05` | `0x72 / 5` | 复合人物/兵种/特效 | `information-transfer-extension` | P1:子类型=5[数值/枚举]; P2:人物位1[人物/部队编号]; P3:人物位2[人物/部队编号]; P4:人物位3[人物/部队编号]; P5:人物位4[人物/部队编号]; P6:兵种位1[数值/枚举]; P7:兵种位2[数值/枚举]; P8:独立特效值[数值/枚举] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-12` | `0x72 / 12` | DT动态图 | `information-transfer-extension` | P1:子类型=12[数值/枚举]; P2:DT图号[数值/枚举]; P3:X坐标[X 坐标/目标]; P4:Y坐标[Y 坐标/目标]; P5:显示方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-14` | `0x72 / 14` | 6.6演出扩展 | `information-transfer-extension` | P1:子类型=14[数值/枚举]; P2:资源/对象编号[数值/枚举]; P3:X坐标/目标[X 坐标/目标]; P4:Y坐标/参数[Y 坐标/目标]; P5:显示/等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-28` | `0x72 / 28` | 6.6演出扩展 | `information-transfer-extension` | P1:子类型=28[数值/枚举]; P2:资源/对象编号[数值/枚举]; P3:参数A[数值/枚举]; P4:参数B[数值/枚举]; P5:显示/等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-30` | `0x72 / 30` | 6.6演出扩展 | `information-transfer-extension` | P1:子类型=30[数值/枚举]; P2:资源/对象编号[数值/枚举]; P3:参数A[数值/枚举]; P4:参数B[数值/枚举]; P5:显示/等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-31` | `0x72 / 31` | U_select命令图标 | `information-transfer-extension` | P1:子类型=31[数值/枚举]; P2:命令图标编号[数值/枚举]; P3:X坐标[X 坐标/目标]; P4:Y坐标[Y 坐标/目标]; P5:显示方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-32` | `0x72 / 32` | DT动态图扩展 | `information-transfer-extension` | P1:子类型=32[数值/枚举]; P2:DT图号[数值/枚举]; P3:X坐标[X 坐标/目标]; P4:Y坐标[Y 坐标/目标]; P5:显示方式[数值/枚举] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-34` | `0x72 / 34` | 6.6演出扩展 | `information-transfer-extension` | P1:子类型=34[数值/枚举]; P2:参数A[数值/枚举]; P3:参数B[数值/枚举]; P4:参数C[数值/枚举]; P5:显示/等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-35` | `0x72 / 35` | 6.6演出扩展 | `information-transfer-extension` | P1:子类型=35[数值/枚举]; P2:参数A[数值/枚举]; P3:参数B[数值/枚举]; P4:参数C[数值/枚举]; P5:显示/等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
| `script.66.opcode-72-sub-36` | `0x72 / 36` | 6.6演出扩展 | `information-transfer-extension` | P1:子类型=36[数值/枚举]; P2:参数A[数值/枚举]; P3:参数B[数值/枚举]; P4:参数C[数值/枚举]; P5:显示/等待标志[布尔/开关标志] | `candidate` / `legacy-structured` |
